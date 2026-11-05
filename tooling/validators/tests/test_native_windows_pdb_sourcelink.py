"""Tests exercise byte-structured synthetic MSF7 PDBs + PE/COFF RSDS, no symbols or DLL execution."""
import json
import pathlib
import struct
import sys
import tempfile
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from native_windows_pdb_sourcelink import inspect,read_msf,read_pe_codeview,MAGIC,EXPECTED_SHA

def fixture():
    guid=bytes(range(16))
    url='https://raw.githubusercontent.com/infoconex/RecordSift/'+EXPECTED_SHA+'/*'
    payload=json.dumps({'documents':{'/_/*':url}}).encode()
    name=b'sourcelink\0'
    info=(struct.pack('<III',20000404,0,1)+guid+
          struct.pack('<I',len(name))+name+
          struct.pack('<II',1,2)+struct.pack('<II',1,1)+struct.pack('<II',1,0)+
          struct.pack('<II',0,2))
    assert len(info)<512 and len(payload)<512
    size=512
    directory=struct.pack('<IIIIII',3,0xffffffff,len(info),len(payload),5,6)
    blob=bytearray(size*7)
    blob[:len(MAGIC)]=MAGIC
    struct.pack_into('<6I',blob,32,size,1,7,len(directory),0,3)
    struct.pack_into('<I',blob,3*size,4)
    blob[4*size:4*size+len(directory)]=directory
    blob[5*size:5*size+len(info)]=info
    blob[6*size:6*size+len(payload)]=payload
    pe=bytearray(0x300)
    pe[:2]=b'MZ'
    struct.pack_into('<I',pe,0x3c,0x80)
    pe[0x80:0x84]=b'PE\0\0'
    struct.pack_into('<H',pe,0x80+6,1)
    struct.pack_into('<H',pe,0x80+20,0xe0)
    opt=0x80+24
    struct.pack_into('<H',pe,opt,0x10b)
    struct.pack_into('<II',pe,opt+96+6*8,0x2000,28)
    section=opt+0xe0
    struct.pack_into('<IIII',pe,section+8,0x200,0x2000,0x200,0x200)
    struct.pack_into('<IIII',pe,0x200+12,2,24,0x2040,0x240)
    pe[0x240:0x244]=b'RSDS'
    pe[0x244:0x254]=guid
    struct.pack_into('<I',pe,0x254,1)
    return blob,pe

class NativePdbTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir=pathlib.Path(self.temp.name)
        self.pdb=self.dir/'fixture.pdb'
        self.dll=self.dir/'fixture.dll'
        self.pdb_data,self.dll_data=fixture()
        self.write()

    def write(self):
        self.pdb.write_bytes(self.pdb_data)
        self.dll.write_bytes(self.dll_data)

    def test_positive_native_pdb_and_pe_identity(self):
        r=inspect(self.pdb,self.dll)
        self.assertEqual(r['pe_codeview_pdb_identity'],'matched')
        self.assertEqual(r['source_link_stream_count'],1)
        self.assertEqual(r['document_mapping_count'],1)
        self.assertEqual(len(read_msf(self.pdb.read_bytes())),3)

    def test_reject_wrong_pe_guid(self):
        self.dll_data[0x244]^=1;self.write()
        with self.assertRaisesRegex(ValueError,'does not match'):inspect(self.pdb,self.dll)

    def test_reject_pdb_signature(self):
        self.pdb_data[0]=0;self.write()
        with self.assertRaises(ValueError):inspect(self.pdb,self.dll)

    def test_reject_out_of_range_directory_page(self):
        struct.pack_into('<I',self.pdb_data,3*512,888);self.write()
        with self.assertRaises(ValueError):inspect(self.pdb,self.dll)

    def test_reject_truncated_stream_directory(self):
        struct.pack_into('<I',self.pdb_data,32+12,8);self.write()
        with self.assertRaises(ValueError):inspect(self.pdb,self.dll)

    def test_reject_bad_named_stream_index(self):
        info_name_start=5*512+28
        name_length=struct.unpack_from('<I',self.pdb_data,info_name_start)[0]
        value_at=5*512+32+name_length+8+8+8+4
        struct.pack_into('<I',self.pdb_data,value_at,99);self.write()
        with self.assertRaises(ValueError):inspect(self.pdb,self.dll)

    def test_reject_missing_sourcelink_name(self):
        off=5*512+32
        self.pdb_data[off:off+10]=b'other_data';self.write()
        with self.assertRaisesRegex(ValueError,'No native PDB Source Link'):inspect(self.pdb,self.dll)

    def test_reject_wrong_commit_in_mapping(self):
        loc=6*512
        segment=bytes(self.pdb_data[loc:loc+512])
        self.assertIn(EXPECTED_SHA.encode(),segment)
        self.pdb_data[loc:loc+512]=segment.replace(EXPECTED_SHA.encode(),b'0'*40)
        self.write()
        with self.assertRaisesRegex(ValueError,'exact frozen SHA'):inspect(self.pdb,self.dll)

    def test_reject_malformed_source_link_json(self):
        self.pdb_data[6*512:6*512+1]=b'!'
        self.write()
        with self.assertRaises(ValueError):inspect(self.pdb,self.dll)

    def test_reject_no_pe_codeview(self):
        self.dll_data[0x240:0x244]=b'FAIL';self.write()
        with self.assertRaisesRegex(ValueError,'RSDS'):inspect(self.pdb,self.dll)

if __name__=='__main__':
    unittest.main()
