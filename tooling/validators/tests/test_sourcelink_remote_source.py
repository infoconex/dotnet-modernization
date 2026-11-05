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

    def mock_git(self, sha=EXPECTED_SHA, tracked=True, changed=False, blob=None):
        return [
            SimpleNamespace(stdout=sha, returncode=0),
            SimpleNamespace(stdout=FILE, returncode=0 if tracked else 1),
            SimpleNamespace(stdout=b'', returncode=1 if changed else 0),
            SimpleNamespace(stdout=self.source_bytes if blob is None else blob, returncode=0),
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

    def test_worktree_modified_against_frozen_head_is_rejected(self):
        with patch('sourcelink_remote_source.subprocess.run',
                   side_effect=self.mock_git(changed=True)):
            with self.assertRaisesRegex(ValueError, 'differs from frozen'):
                verify(self.root / 'fixture.pdb', self.root, FILE,
                       fetch=lambda url: self.source_bytes)

    def test_remote_matches_dirty_checkout_but_not_immutable_blob_rejected(self):
        different_blob = b'file content in original Git object'
        with patch('sourcelink_remote_source.mapping_from_pdb', return_value=SOURCE), patch(
            'sourcelink_remote_source.subprocess.run',
            side_effect=self.mock_git(blob=different_blob)):
            with self.assertRaisesRegex(ValueError, 'exact frozen Git blob'):
                verify(self.root / 'fixture.pdb', self.root, FILE,
                       fetch=lambda url: self.source_bytes)

    def test_worktree_crlf_differs_but_git_blob_and_remote_match(self):
        git_blob = b'first\nsecond\n'
        self.target.write_bytes(b'first\r\nsecond\r\n')
        with patch('sourcelink_remote_source.mapping_from_pdb', return_value=SOURCE), patch(
            'sourcelink_remote_source.subprocess.run',
            side_effect=self.mock_git(blob=git_blob)):
            result = verify(self.root / 'fixture.pdb', self.root, FILE,
                            fetch=lambda url: git_blob)
        self.assertFalse(result['working_tree_byte_equal_git_blob'])
        self.assertTrue(result['worktree_difference_consistent_with_crlf_conversion'])
        self.assertEqual(result['source_bytes'], len(git_blob))


if __name__ == '__main__':
    unittest.main()
