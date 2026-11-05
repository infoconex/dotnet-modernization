"""Negative and positive synthetic native PDB source inventory matching controls."""
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from sourcelink_all_owned_sources import selected_source_files

OWNED=['CharacterLimitedTextReader.cs','CsvRecordReaderAdapter.cs','CsvStreamImporterAdapter.cs','MalformedCsvException.cs']

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=pathlib.Path(self.temp.name)
        project=self.root/'src'/'RecordSift.Infrastructure.Csv'
        project.mkdir(parents=True)
        for name in OWNED:
            (project/name).write_text('class Sample {}',encoding='utf8')
    def lines(self, names=OWNED):
        return '\n'.join(' - (no checksum) /_/src/RecordSift.Infrastructure.Csv/'+name for name in names)
    def test_full_owned_pdb_inventory(self):
        r=selected_source_files(self.lines(),self.root)
        self.assertEqual(len(r),4)
        self.assertTrue(all(x.startswith('src/RecordSift.Infrastructure.Csv/') for x in r))
    def test_duplicate_llvm_file_row_does_not_double_count(self):
        r=selected_source_files(self.lines()+ '\n'+self.lines([OWNED[0]]),self.root)
        self.assertEqual(len(r),4)
    def test_missing_primary_importer_fails(self):
        with self.assertRaisesRegex(ValueError,'expected'):
            selected_source_files(self.lines(OWNED[:2]),self.root)
    def test_unknown_owned_filename_fails(self):
        with self.assertRaisesRegex(ValueError,'Unmatched'):
            selected_source_files(self.lines()+ '\n - (no checksum) /_/src/RecordSift.Infrastructure.Csv/Changed.cs',self.root)
    def test_unrelated_text_does_not_count(self):
        with self.assertRaisesRegex(ValueError,'expected'):
            selected_source_files('\n'.join('Compiler emitted '+x for x in OWNED),self.root)
    def test_ambiguous_named_files_fail(self):
        (self.root/'src'/'RecordSift.Infrastructure.Csv'/'Properties').mkdir()
        (self.root/'src'/'RecordSift.Infrastructure.Csv'/'Properties'/OWNED[0]).write_text('class A {}')
        with self.assertRaisesRegex(ValueError,'Ambiguous'):
            selected_source_files(self.lines(),self.root)

if __name__=='__main__':
    unittest.main()
