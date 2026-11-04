import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import provenance


class ProvenanceTests(unittest.TestCase):
    def test_guard_rejects_absent_and_wrong_revision(self):
        with self.assertRaisesRegex(ValueError, 'expected Git commit'):
            provenance.require_commit(None, 'a' * 40)
        with self.assertRaisesRegex(ValueError, '40-character'):
            provenance.require_commit(None, 'main')
        provenance.require_commit('a' * 40, 'A' * 40)

    def test_actual_git_revision_recorded(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d)
            subprocess.run(['git', 'init', '-q', str(p)], check=True)
            subprocess.run(['git', '-C', str(p), '-c', 'user.name=Example', '-c', 'user.email=example@example.test',
                            'commit', '--allow-empty', '-m', 'fixture', '-q'], check=True)
            snap = provenance.snapshot(p)
            self.assertEqual(len(snap['commit']), 40)
            provenance.require_commit(snap['commit'], snap['commit'])
            (p / 'untracked.txt').write_text('sample')
            self.assertIn('?? untracked.txt', provenance.snapshot(p)['dirty_paths'])


if __name__ == '__main__':
    unittest.main()
