#!/usr/bin/env python3
"""Fail-closed native Windows PDB negative control: no Source Link stream, valid DLL/PDB identity.

A successful negative check proves absence was actually observed in a valid
compiled symbol pair; it does NOT certify Source Link feature acceptance.
"""
import argparse
import json
from pathlib import Path
import re
from native_windows_pdb_sourcelink import read_msf,parse_named_streams,read_pe_codeview


def inspect_absence(pdb, dll):
    streams=read_msf(Path(pdb).read_bytes())
    guid,age,names=parse_named_streams(streams[1],len(streams))
    if read_pe_codeview(Path(dll).read_bytes())!=(guid,age):
        raise ValueError('PE CodeView and PDB GUID/age differ')
    source=[n for n in names if re.fullmatch(r'sourcelink(?:\$\d+)?', n, re.I)]
    if source:
        raise ValueError('Unexpected embedded Source Link metadata in negative control')
    return {
      'schema_version':1,'pdb_format':'native-windows-msf7',
      'pe_pdb_codeview_identity':'verified_match',
      'source_link_named_stream_count':0,
      'status':'VERIFIED_NATIVE_SOURCE_LINK_ABSENT_NEGATIVE_CONTROL',
      'limitation':'Not a Source Link compatibility success; no-remote or local-file-origin metadata must be evaluated independently.'
    }


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdb',required=True,type=Path)
    p.add_argument('--dll',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    try:
        if a.output.exists():raise ValueError('Refusing to overwrite evidence')
        result=inspect_absence(a.pdb,a.dll)
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        print(result['status'])
    except (ValueError,TypeError,OSError,KeyError) as e:
        p.exit(2,'Negative control failed closed: '+str(e)+'\n')
