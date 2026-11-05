"""Structural native Windows PDB C13 checksum subrecord regression tests."""
import hashlib
import pathlib
import struct
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from windows_pdb_document_checksums import (
    parse_file_checksums, parse_c13_chunks, modules_from_dbi, pdb_global_string_table, K_STRING_TABLE, K_FILE_CHECKSUMS
)

NAME=b'/_/src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs'
CONTENT=b'public class Example {}\n'


def checksum_blob(name_offset=1, kind=3, payload=None):
    if payload is None:
        payload=hashlib.sha256(CONTENT).digest()
    data=struct.pack('<IBB',name_offset,len(payload),kind)+payload
    return data+b'\0'*((-len(data))%4)


def chunk(kind,payload):
    raw=struct.pack('<II',kind,len(payload))+payload
    return raw+b'\0'*((-len(raw))%4)


class C13Safety(unittest.TestCase):
    def test_parses_real_sha256_source_checksum(self):
        row=parse_file_checksums(b'\0'+NAME+b'\0',checksum_blob())[0]
        self.assertEqual(row['path'],NAME.decode())
        self.assertEqual(row['algorithm'],'sha256')
        self.assertEqual(row['digest'],hashlib.sha256(CONTENT).digest())

    def test_parses_c13_subsections(self):
        c13=chunk(K_STRING_TABLE,b'\0'+NAME+b'\0')+chunk(K_FILE_CHECKSUMS,checksum_blob())
        sections=parse_c13_chunks(c13)
        self.assertEqual(len(sections),2)
        self.assertEqual(sections[1][0],K_FILE_CHECKSUMS)

    def test_reject_unknown_checksum_kind(self):
        with self.assertRaises(ValueError):parse_file_checksums(b'\0'+NAME+b'\0',checksum_blob(kind=99))

    def test_reject_wrong_digest_length(self):
        with self.assertRaises(ValueError):parse_file_checksums(b'\0'+NAME+b'\0',checksum_blob(payload=b'1'*12))

    def test_reject_out_of_bounds_string_offset(self):
        with self.assertRaises(ValueError):parse_file_checksums(b'\0'+NAME+b'\0',checksum_blob(name_offset=9000))

    def test_reject_nonterminated_string(self):
        with self.assertRaises(ValueError):parse_file_checksums(b'\0'+NAME,checksum_blob())

    def test_reject_missing_string_table_root(self):
        with self.assertRaises(ValueError):parse_file_checksums(NAME+b'\0',checksum_blob())

    def test_reject_truncated_subsection(self):
        data=struct.pack('<II',K_FILE_CHECKSUMS,100)+b'zero'
        with self.assertRaises(ValueError):parse_c13_chunks(data)

    def test_reject_truncated_checksum_entry(self):
        with self.assertRaises(ValueError):parse_file_checksums(b'\0'+NAME+b'\0',b'\0'*5)

    def test_reject_missing_dbi(self):
        with self.assertRaises(ValueError):modules_from_dbi(b'')

    def test_parses_global_pdb_names_string_table(self):
        strings=b'\0'+NAME+b'\0'
        blob=struct.pack('<III',0xEFFEEFFE,1,len(strings))+strings
        streams=[None,b'PDBINFO',None,None,blob]
        with patch('windows_pdb_document_checksums.parse_named_streams',return_value=(None,1,{'/names':4})):
            self.assertEqual(pdb_global_string_table(streams),strings)

    def test_reject_bad_global_pdb_names_signature(self):
        blob=struct.pack('<III',0,1,3)+b'\0x\0'
        with patch('windows_pdb_document_checksums.parse_named_streams',return_value=(None,1,{'/names':4})):
            with self.assertRaises(ValueError):pdb_global_string_table([None,b'PDBINFO',None,None,blob])

    def test_parses_dbi_module_info(self):
        record=bytearray(64)
        struct.pack_into('<H',record,34,8)
        struct.pack_into('<III',record,36,20,0,48)
        record.extend(b'Module\0Obj\0')
        record.extend(b'\0'*((-len(record))%4))
        hdr=bytearray(64)
        struct.pack_into('<I',hdr,0,0xffffffff)
        struct.pack_into('<I',hdr,24,len(record))
        rows=modules_from_dbi(bytes(hdr+record))
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['stream'],8)
        self.assertEqual(rows[0]['c13_bytes'],48)

if __name__=='__main__':
    unittest.main()
