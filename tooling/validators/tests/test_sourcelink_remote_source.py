"""Source Link raw URL safety, revision specificity, and wildcard resolution fixture tests."""
import pathlib
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sourcelink_remote_source import derive_raw_url, verify, EXPECTED_SHA, ROOT

FILE = 'src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs'
SOURCE = {'/_/*': ROOT + EXPECTED_SHA + '/*'}


class RemoteSourceTests(unittest.TestCase):
    def test_correct_frozen_url(self):
        self.assertEqual(derive_raw_url(SOURCE, FILE), ROOT + EXPECTED_SHA + '/' + FILE)

    def test_reject_wrong_git_commit(self):
        with self.assertRaisesRegex(ValueError, 'exact frozen'):
            derive_raw_url({'/_/*': ROOT + '0'*40 + '/*'}, FILE)

    def test_reject_unknown_host(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/_/*': 'https://example.com/x/' + EXPECTED_SHA + '/*'}, FILE)

    def test_reject_http_url(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/_/*': 'http://raw.githubusercontent.com/infoconex/RecordSift/' + EXPECTED_SHA + '/*'}, FILE)

    def test_reject_userinfo_in_url(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/_/*': 'https://username@raw.githubusercontent.com/infoconex/RecordSift/' + EXPECTED_SHA + '/*'}, FILE)

    def test_reject_path_traversal(self):
        with self.assertRaisesRegex(ValueError, 'owned'):
            derive_raw_url(SOURCE, 'src/../secrets.txt')

    def test_reject_external_filename(self):
        with self.assertRaisesRegex(ValueError, 'owned'):
            derive_raw_url(SOURCE, 'C:/agent/data.cs')

    def test_reject_ambiguous_source_maps(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/_/*': SOURCE['/_/*'], '/another/*': SOURCE['/_/*']}, FILE)

    def test_reject_missing_wildcard(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/_/': SOURCE['/_/*']}, FILE)

    def test_reject_query_in_remote_url(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/_/*': SOURCE['/_/*'] + '?token=x'}, FILE)

    def test_reject_different_path_mapping(self):
        with self.assertRaises(ValueError):
            derive_raw_url({'/app/*': SOURCE['/_/*']}, FILE)


class ActualFileParityControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.target = self.root / FILE
        self.target.parent.mkdir(parents=True)
        self.source_bytes = b'// simulated frozen C# source\\npublic class A {}\\n'
        self.target.write_bytes(self.source_bytes)

    def mock_git(self, sha=EXPECTED_SHA, tracked=True):
        return [
            SimpleNamespace(stdout=sha + '\\n', returncode=0),
            SimpleNamespace(stdout=FILE + '\\n', returncode=0 if tracked else 1),
        ]

    def test_verified_remote_bytes_are_identical(self):
        with patch('sourcelink_remote_source.mapping_from_pdb', return_value=SOURCE), patch(
            'sourcelink_remote_source.subprocess.run', side_effect=self.mock_git()):
            result = verify(self.root / 'fixture.pdb', self.root, FILE,
                            fetch=lambda url: self.source_bytes)
        self.assertEqual(result['source_link_mapping_to_raw_url'], 'verified')
        self.assertEqual(result['source_bytes'], len(self.source_bytes))

    def test_modified_remote_bytes_rejected(self):
        with patch('sourcelink_remote_source.mapping_from_pdb', return_value=SOURCE), patch(
            'sourcelink_remote_source.subprocess.run', side_effect=self.mock_git()):
            with self.assertRaisesRegex(ValueError, 'do not match'):
                verify(self.root / 'fixture.pdb', self.root, FILE,
                       fetch=lambda url: self.source_bytes + b'changed')

    def test_wrong_checked_out_commit_rejected(self):
        with patch('sourcelink_remote_source.subprocess.run',
                   return_value=SimpleNamespace(stdout='0'*40, returncode=0)):
            with self.assertRaisesRegex(ValueError, 'HEAD does not match'):
                verify(self.root / 'fixture.pdb', self.root, FILE,
                       fetch=lambda url: self.source_bytes)

    def test_untracked_file_rejected(self):
        with patch('sourcelink_remote_source.subprocess.run',
                   side_effect=self.mock_git(tracked=False)):
            with self.assertRaisesRegex(ValueError, 'not tracked'):
                verify(self.root / 'fixture.pdb', self.root, FILE,
                       fetch=lambda url: self.source_bytes)

    def test_empty_source_rejected(self):
        self.target.write_bytes(b'')
        with patch('sourcelink_remote_source.subprocess.run',
                   side_effect=self.mock_git()):
            with self.assertRaisesRegex(ValueError, 'size budget'):
                verify(self.root / 'fixture.pdb', self.root, FILE,
                       fetch=lambda url: b'')


if __name__ == '__main__':
    unittest.main()
