import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pe_variation


def pe(name='Example.Domain', file_hash='a', mvid='00000000-0000-0000-0000-000000000001',
       timestamp='12345678', debug=None, methods=None):
    return {
        'assembly': name, 'filename': name + '.dll', 'bytes': 128,
        'file_sha256': file_hash * 64, 'mvid': mvid,
        'coff_timestamp_hex': timestamp, 'pe_kind': 'PE32',
        'assembly_version': '1.0.0.0',
        'method_body_count': len(methods or {'06000001': {'size': 1, 'sha256': 'e' * 64}}),
        'method_il_total_bytes': 1,
        'method_bodies': methods or {'06000001': {'size': 1, 'sha256': 'e' * 64}},
        'debug_directory': [] if debug is None else debug,
    }


class PeVariationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.original = self.root / 'original.json'
        self.second = self.root / 'other.json'
        self.third = self.root / 'again.json'

    def save(self, path, values):
        path.write_text(json.dumps({'schema_version': 1, 'kind': 'managed-pe-provenance',
                                    'assemblies': values}), encoding='utf-8')

    def test_identical_pe_is_reported_without_overclaiming(self):
        for path in (self.original, self.second, self.third):
            self.save(path, [pe()])
        report = pe_variation.compare_three(self.original, self.second, self.third)
        for key in ('independent_worktree', 'same_worktree_rebuild'):
            self.assertEqual(report[key]['identical_binaries'], 1)
            self.assertEqual(report[key]['different_binaries'], 0)
            self.assertFalse(report[key]['changed_method_il_assemblies'])

    def test_distinguishes_mvid_and_coff_drift_from_unchanged_il(self):
        self.save(self.original, [pe()])
        self.save(self.second, [pe(file_hash='b',
                                   mvid='00000000-0000-0000-0000-000000000002',
                                   timestamp='87654321')])
        self.save(self.third, [pe(file_hash='c', debug=[{'type': 'CodeView', 'codeview_guid': 'abc'}])])
        report = pe_variation.compare_three(self.original, self.second, self.third)
        independent = report['independent_worktree']['assemblies']['Example.Domain']
        repeated = report['same_worktree_rebuild']['assemblies']['Example.Domain']
        self.assertTrue(independent['mvid_changed'])
        self.assertTrue(independent['coff_timestamp_changed'])
        self.assertTrue(independent['method_il_tokens_match'])
        self.assertEqual(independent['changed_method_il_tokens'], [])
        self.assertTrue(repeated['debug_directory_changed'])
        self.assertFalse(repeated['mvid_changed'])

    def test_method_body_byte_regression_detected(self):
        self.save(self.original, [pe()])
        changed = {'06000001': {'size': 1, 'sha256': 'f' * 64}}
        self.save(self.second, [pe(file_hash='b', methods=changed)])
        self.save(self.third, [pe()])
        report = pe_variation.compare_three(self.original, self.second, self.third)
        self.assertEqual(report['independent_worktree']['changed_method_il_assemblies'], ['Example.Domain'])
        self.assertEqual(report['independent_worktree']['assemblies']['Example.Domain']['changed_method_il_tokens'], ['06000001'])

    def test_missing_assembly_fails_closed(self):
        self.save(self.original, [pe()])
        self.save(self.second, [pe(name='Example.Other')])
        self.save(self.third, [pe()])
        with self.assertRaisesRegex(ValueError, 'identical sets'):
            pe_variation.compare_three(self.original, self.second, self.third)

    def test_duplicate_assembly_names_fail_closed(self):
        self.save(self.original, [pe(), pe()])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            pe_variation.read_snapshot(self.original)

    def test_missing_mvid_fails_closed(self):
        item = pe()
        del item['mvid']
        self.save(self.original, [item])
        with self.assertRaisesRegex(ValueError, 'Missing required'):
            pe_variation.read_snapshot(self.original)

    def test_invalid_version_fails_closed(self):
        self.original.write_text('{"schema_version":0,"assemblies":[]}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'schema version'):
            pe_variation.read_snapshot(self.original)

    def test_cli_exit_and_no_overwrite(self):
        for path in (self.original, self.second, self.third):
            self.save(path, [pe()])
        output = self.root / 'report.json'
        cmd = [sys.executable, str(Path(pe_variation.__file__)), '--original', str(self.original),
               '--independent', str(self.second), '--same-path-rebuild', str(self.third),
               '--output', str(output)]
        run = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['kind'],
                         'pe-reproducibility-comparison')
        again = subprocess.run(cmd, capture_output=True, text=True)
        self.assertNotEqual(again.returncode, 0)
        self.assertIn('already exists', again.stderr)


if __name__ == '__main__':
    unittest.main()
