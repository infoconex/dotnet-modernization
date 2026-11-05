#!/usr/bin/env python3
"""Fail-closed structural Windows PDB Source Link stream and DLL identity reader.

Reads MSF7 superblock, indexed stream directory, PDB Info Stream named stream
hash map, Source Link JSON, and managed DLL's PE/COFF CodeView RSDS record.
Never loads or executes assembly or debug symbols. Not a document checksum reader.
"""
import argparse
import json
import pathlib
import re
import struct
import sys

MAGIC = b'Microsoft C/C++ MSF 7.00\r\n\x1aDS\x00\x00\x00'
MAX_PDB = 128 * 1024 * 1024
MAX_STREAM = 16 * 1024 * 1024
EXPECTED_SHA = '8358780829458854a4b0356df5ac5e685f0a34c8'


def _u32(buf, off):
    if off < 0 or off + 4 > len(buf):
        raise ValueError('Truncated 32-bit PDB structure')
    return struct.unpack_from('<I', buf, off)[0]


def _block(raw, block_size, num_blocks, index):
    if index >= num_blocks:
        raise ValueError('Out-of-range PDB MSF block')
    start = index * block_size
    if start + block_size > len(raw):
        raise ValueError('Truncated PDB block')
    return raw[start:start + block_size]


def _stream_data(raw, block_size, num_blocks, blocks, length):
    if length > MAX_STREAM:
        raise ValueError('Oversized PDB stream')
    needed = (length + block_size - 1) // block_size
    if len(blocks) != needed:
        raise ValueError('PDB stream block count mismatch')
    return b''.join(_block(raw, block_size, num_blocks, i) for i in blocks)[:length]


def read_msf(raw):
    if not raw.startswith(MAGIC) or len(raw) < 56 or len(raw) > MAX_PDB:
        raise ValueError('Not a supported bounded Windows MSF7 PDB')
    block_size, fpm, num_blocks, directory_size, unused, map_block = struct.unpack_from('<6I', raw, 32)
    if block_size not in (512,1024,2048,4096) or num_blocks * block_size != len(raw):
        raise ValueError('Invalid MSF7 block count or size')
    if fpm not in (1,2) or not 0 < directory_size <= MAX_STREAM:
        raise ValueError('Invalid MSF7 directory / free block map')
    dir_blocks = (directory_size + block_size - 1) // block_size
    if dir_blocks * 4 > block_size:
        raise ValueError('Unsupported multi-page MSF directory block map; fail closed')
    block_map = _block(raw, block_size, num_blocks, map_block)
    directory_ids = [_u32(block_map, i * 4) for i in range(dir_blocks)]
    directory = _stream_data(raw, block_size, num_blocks, directory_ids, directory_size)
    count = _u32(directory, 0)
    if not 2 <= count <= 65536 or 4 + 4 * count > len(directory):
        raise ValueError('Invalid MSF stream count')
    sizes = [_u32(directory, 4 + i * 4) for i in range(count)]
    pos = 4 + count * 4
    streams = []
    for size in sizes:
        if size == 0xffffffff:
            streams.append(None)
            continue
        if size > MAX_STREAM:
            raise ValueError('Unbounded MSF stream')
        n = (size + block_size - 1) // block_size
        if pos + n * 4 > len(directory):
            raise ValueError('Truncated MSF stream block index array')
        numbers = [_u32(directory, pos + i * 4) for i in range(n)]
        pos += n * 4
        streams.append(_stream_data(raw, block_size, num_blocks, numbers, size))
    if pos != len(directory):
        raise ValueError('Trailing bytes in MSF stream directory')
    if streams[1] is None or len(streams[1]) < 32:
        raise ValueError('Missing PDB Info Stream')
    return streams


def parse_named_streams(info, count):
    if len(info) < 32:
        raise ValueError('Short PDB Info Stream')
    guid, age = info[12:28], _u32(info,8)
    string_length = _u32(info,28)
    pos = 32
    if string_length > len(info) - pos:
        raise ValueError('Invalid PDB named-string buffer')
    names_data = info[pos:pos + string_length]
    pos += string_length
    size = _u32(info,pos);capacity=_u32(info,pos+4);pos+=8
    if size > 10000 or capacity > 65536 or size > capacity:
        raise ValueError('Invalid PDB name hash table size')
    bitsets=[]
    for _ in range(2):
        words = _u32(info,pos);pos+=4
        if words > (capacity + 31) // 32 + 1 or pos + 4 * words > len(info):
            raise ValueError('Invalid PDB named stream bitset')
        values=[_u32(info,pos+4*i) for i in range(words)]
        pos+=words*4
        bitsets.append(values)
    present = sum(x.bit_count() for x in bitsets[0])
    if present != size or pos + size * 8 > len(info):
        raise ValueError('Inconsistent PDB named stream hash table')
    names={}
    for _ in range(size):
        offset=_u32(info,pos);stream_index=_u32(info,pos+4);pos+=8
        if offset >= string_length or stream_index >= count:
            raise ValueError('Invalid named stream key/index')
        end=names_data.find(b'\0',offset)
        if end < 0:
            raise ValueError('Unterminated PDB named stream')
        name=names_data[offset:end].decode('utf-8','strict')
        if name in names:
            raise ValueError('Duplicate named stream')
        names[name]=stream_index
    return guid,age,names


def read_pe_codeview(pe):
    if len(pe) < 256 or pe[:2] != b'MZ':
        raise ValueError('Invalid managed DLL PE header')
    peoff=_u32(pe,0x3c)
    if peoff + 24 > len(pe) or pe[peoff:peoff+4] != b'PE\0\0':
        raise ValueError('Invalid PE/COFF signature')
    sections=struct.unpack_from('<H',pe,peoff+6)[0]
    optional_len=struct.unpack_from('<H',pe,peoff+20)[0]
    opt=peoff+24
    if opt+optional_len > len(pe):
        raise ValueError('Truncated optional PE header')
    magic=struct.unpack_from('<H',pe,opt)[0]
    data_dir_base=opt+(96 if magic==0x10b else 112 if magic==0x20b else -1)
    if data_dir_base < opt or data_dir_base + 8*7 > opt+optional_len:
        raise ValueError('Missing PE debug data directory')
    debug_rva, debug_len=struct.unpack_from('<II',pe,data_dir_base+6*8)
    sectionbase=opt+optional_len
    if not debug_rva or debug_len < 28 or debug_len > 65536:
        raise ValueError('Missing or oversized PE debug directory')
    def rva_file(rva):
        for i in range(sections):
            p=sectionbase+i*40
            if p+40>len(pe):
                raise ValueError('Truncated PE section table')
            virtual_size,virtual_address,raw_size,raw_offset=struct.unpack_from('<IIII',pe,p+8)
            if virtual_address <= rva < virtual_address+max(virtual_size,raw_size):
                out=raw_offset+(rva-virtual_address)
                if out>=len(pe):break
                return out
        raise ValueError('PE debug RVA unmapped')
    off=rva_file(debug_rva)
    if off+debug_len > len(pe):
        raise ValueError('Truncated debug directory')
    matches=[]
    for j in range(debug_len//28):
        pos=off+28*j
        debug_type=_u32(pe,pos+12)
        size=_u32(pe,pos+16)
        ptr=_u32(pe,pos+24)
        if debug_type==2 and size>=24 and ptr+size<=len(pe) and pe[ptr:ptr+4]==b'RSDS':
            matches.append((pe[ptr+4:ptr+20],_u32(pe,ptr+20)))
    if len(matches)!=1:
        raise ValueError('Expected exactly one matching PE CodeView RSDS record')
    return matches[0]


def inspect(pdb, dll, sha=EXPECTED_SHA):
    streams=read_msf(pathlib.Path(pdb).read_bytes())
    guid,age,named=parse_named_streams(streams[1],len(streams))
    if read_pe_codeview(pathlib.Path(dll).read_bytes())!=(guid,age):
        raise ValueError('PE CodeView RSDS GUID/age does not match native PDB')
    entries=[(n,i) for n,i in named.items() if re.fullmatch(r'sourcelink\$\d+',n,re.I)]
    if not entries:
        raise ValueError('No native PDB Source Link named streams (srcsrv is not sufficient)')
    documents={}
    for name,i in entries:
        if streams[i] is None or len(streams[i])>MAX_STREAM:
            raise ValueError('Missing Source Link stream bytes')
        raw=streams[i].rstrip(b'\0')
        data=json.loads(raw.decode('utf-8','strict'))
        if not isinstance(data,dict) or not isinstance(data.get('documents'),dict) or not data['documents']:
            raise ValueError('Malformed Source Link JSON documents')
        for path,url in data['documents'].items():
            if not isinstance(path,str) or not isinstance(url,str) or sha not in url or not url.startswith('https://'):
                raise ValueError('Source Link mapping absent exact frozen SHA or HTTPS')
            if path in documents:
                raise ValueError('Duplicate PDB document mapping key')
            documents[path]=url
    return {'format':'windows-msf7','pe_codeview_pdb_identity':'matched',
            'source_link_stream_count':len(entries),'document_mapping_count':len(documents),
            'source_commit':sha,'native_source_link_json':'structurally_parsed',
            'limitation':'Document table checksum records and remote bytes not yet independently validated.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdb',type=pathlib.Path,required=True)
    p.add_argument('--dll',type=pathlib.Path,required=True)
    p.add_argument('--output',type=pathlib.Path,required=True)
    args=p.parse_args()
    if args.output.exists():
        p.error('Refusing overwrite of evidence')
    try:
        result=inspect(args.pdb,args.dll)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        print('VERIFIED',result['format'],result['pe_codeview_pdb_identity'],
              result['document_mapping_count'],'source mappings')
    except (OSError,ValueError,KeyError,TypeError,UnicodeError,struct.error,json.JSONDecodeError) as e:
        p.exit(2,'Native PDB structural validation failed closed: '+str(e)+'\n')


if __name__=='__main__':
    main()
