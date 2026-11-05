#!/usr/bin/env python3
"""Inspect native Windows PDB CodeView C13 file checksum records structurally.

Strict bounds, known digest algorithms, and real source hash comparison.
No DLL/PDB is executed or uploaded. Unsupported formats fail closed.
"""
import argparse
import hashlib
import json
import pathlib
import struct
import sys

from native_windows_pdb_sourcelink import EXPECTED_SHA, read_msf

K_STRING_TABLE = 0xF3
K_FILE_CHECKSUMS = 0xF4
HASH_TYPES = {1: ('md5', 16), 2: ('sha1', 20), 3: ('sha256', 32)}


def u16(buf, i):
    if i < 0 or i + 2 > len(buf):
        raise ValueError('Truncated PDB CodeView 16-bit record')
    return struct.unpack_from('<H', buf, i)[0]


def u32(buf, i):
    if i < 0 or i + 4 > len(buf):
        raise ValueError('Truncated PDB CodeView 32-bit record')
    return struct.unpack_from('<I', buf, i)[0]


def modules_from_dbi(dbi):
    if not dbi or len(dbi) < 64:
        raise ValueError('Missing PDB DBI stream')
    if u32(dbi, 0) != 0xFFFFFFFF:
        raise ValueError('Unexpected PDB DBI signature')
    size = u32(dbi, 24)
    if size < 64 or 64 + size > len(dbi) or size > 16 * 1024 * 1024:
        raise ValueError('Unsupported PDB module info substream size')
    limit = 64 + size
    pos = 64
    modules = []
    while pos < limit:
        if pos + 64 > limit:
            raise ValueError('Incomplete PDB ModInfo record')
        stream = u16(dbi, pos + 34)
        sym, c11, c13 = struct.unpack_from('<III', dbi, pos + 36)
        name_end = dbi.find(b'\0', pos + 64, limit)
        if name_end < 0:
            raise ValueError('Unterminated PDB module name')
        obj_end = dbi.find(b'\0', name_end + 1, limit)
        if obj_end < 0:
            raise ValueError('Unterminated PDB object name')
        nxt = (obj_end + 4) & ~3
        if nxt <= pos or nxt > limit:
            raise ValueError('PDB module info record alignment error')
        modules.append({'stream':stream, 'sym_bytes':sym, 'c11_bytes':c11, 'c13_bytes':c13})
        pos = nxt
    if not modules or pos != limit:
        raise ValueError('Missing/incomplete DBI module table')
    return modules


def parse_c13_chunks(c13):
    offset=0
    chunks=[]
    while offset < len(c13):
        if offset + 8 > len(c13):
            raise ValueError('Truncated C13 subsection header')
        kind, length = struct.unpack_from('<II', c13, offset)
        start=offset+8
        if length > len(c13) - start:
            raise ValueError('Truncated C13 subsection payload')
        chunks.append((kind, c13[start:start+length]))
        offset=(start+length+3)&~3
        if offset > len(c13):
            raise ValueError('Invalid C13 subsection padding')
    return chunks


def parse_file_checksums(strings, content):
    if not strings or strings[0] != 0:
        raise ValueError('Missing C13 null-rooted string table')
    out=[]
    off=0
    while off < len(content):
        if off + 6 > len(content):
            raise ValueError('Truncated C13 file checksum header')
        name_off=u32(content, off)
        length=content[off+4]
        kind=content[off+5]
        if kind not in HASH_TYPES or HASH_TYPES[kind][1] != length:
            raise ValueError('Unsupported C13 checksum kind/size')
        end=off+6+length
        if end > len(content) or name_off >= len(strings):
            raise ValueError('Out-of-bounds C13 checksum or file name')
        terminator=strings.find(b'\0', name_off)
        if terminator < 0:
            raise ValueError('Unterminated C13 source filename')
        filename=strings[name_off:terminator].decode('utf-8','strict')
        if not filename:
            raise ValueError('Empty C13 source path')
        algorithm,_=HASH_TYPES[kind]
        out.append({'path':filename, 'algorithm':algorithm, 'digest':content[off+6:end]})
        off=(end+3)&~3
        if off > len(content):
            raise ValueError('Incorrect C13 checksum record alignment')
    return out


def pdb_checksums(pdb):
    streams=read_msf(pathlib.Path(pdb).read_bytes())
    if len(streams) <= 3:
        raise ValueError('Missing DBI stream index 3')
    modules=modules_from_dbi(streams[3])
    checks=[]
    processed=0
    for mod in modules:
        size=mod['c13_bytes']
        stream=mod['stream']
        if not size:
            continue
        if stream==0xFFFF or stream >= len(streams) or streams[stream] is None:
            raise ValueError('Missing expected module C13 stream')
        data=streams[stream]
        start=mod['sym_bytes']+mod['c11_bytes']
        if start+size > len(data):
            raise ValueError('Truncated PDB module C13 source range')
        chunks=parse_c13_chunks(data[start:start+size])
        strings=[payload for kind,payload in chunks if kind==K_STRING_TABLE]
        hashed=[payload for kind,payload in chunks if kind==K_FILE_CHECKSUMS]
        if len(strings)!=1 and hashed:
            raise ValueError('No unambiguous local C13 source string table for checksums')
        if len(strings)==1:
            for blob in hashed:
                checks.extend(parse_file_checksums(strings[0],blob))
        processed+=1
    if not checks:
        raise ValueError('No supported C13 document checksum records found')
    return {'module_count':len(modules),'c13_module_count':processed,'entries':checks}


def compare(pdb, source_root, relative_source):
    root=pathlib.Path(source_root).resolve(strict=True)
    source=(root / relative_source).resolve(strict=True)
    if not source.is_relative_to(root) or not source.is_file():
        raise ValueError('Source file not contained in checkout')
    if '..' in pathlib.PurePosixPath(relative_source).parts or not relative_source.startswith('src/'):
        raise ValueError('Expected an owned tracked source relative path')
    data=pdb_checksums(pdb)
    expected='/_/'+relative_source
    matches=[row for row in data['entries'] if row['path'].replace('\\','/') == expected]
    if len(matches)!=1:
        raise ValueError('Expected exactly one normalized PDB document checksum entry; matched=' + str(len(matches)) +
                         '; C13 documents=' + str(len(data['entries'])))
    row=matches[0]
    recorded=row['digest']
    computed=hashlib.new(row['algorithm'],source.read_bytes()).digest()
    if recorded != computed:
        raise ValueError('PDB recorded source checksum does not match frozen source file')
    return {'format':'windows-msf7','frozen_git_revision':EXPECTED_SHA,
            'normalized_document_path':'verified_no_local_agent_path',
            'selected_relative_document':relative_source,'checksum_kind':row['algorithm'],
            'checksum_hex':recorded.hex(),'checksum_record_matches_frozen_source':True,
            'pdb_module_count':data['module_count'],'pdb_c13_module_count':data['c13_module_count'],
            'pdb_document_checksum_records':len(data['entries']),
            'scope':'Selected document only; other documents, external sources and debugger stepping not verified.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdb',required=True,type=pathlib.Path)
    p.add_argument('--source-root',required=True,type=pathlib.Path)
    p.add_argument('--relative-source',required=True)
    p.add_argument('--output',required=True,type=pathlib.Path)
    a=p.parse_args()
    if a.output.exists():
        p.error('Refusing to overwrite existing evidence')
    try:
        report=compare(a.pdb,a.source_root,a.relative_source)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
        print('PASS: C13 document digest matches frozen source:', report['checksum_kind'],report['checksum_hex'])
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, struct.error) as error:
        p.exit(2,'Native PDB C13 document checksum gate failed closed: '+str(error)[:350]+'\n')


if __name__=='__main__':
    main()
