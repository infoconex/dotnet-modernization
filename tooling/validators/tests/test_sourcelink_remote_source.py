"""Source Link raw URL safety, revision specificity, and wildcard resolution fixture tests."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from sourcelink_remote_source import derive_raw_url, EXPECTED_SHA, ROOT

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


if __name__ == '__main__':
    unittest.main()
