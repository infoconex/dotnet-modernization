import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gates


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'source'
        self.root.mkdir()
        self.dest = self.base / 'evidence'

    def gate(self, ident, code, **extra):
        return {'id': ident, 'command': [sys.executable, '-c', code], **extra}

    def plan(self, *entries):
        return {'schema_version': 1, 'gates': list(entries)}

    def test_success_and_intentional_negative_are_separate(self):
        plan = self.plan(self.gate('positive', 'print("OK")'),
                         self.gate('negative', 'import sys;sys.exit(2)', kind='negative', expected_exit_codes=[2]))
        result = gates.run_plan(plan, self.root, self.dest)
        self.assertEqual(result['overall'], 'passed')
        self.assertEqual(result['summary']['expected_negative'], 1)
        self.assertEqual((self.dest / 'positive.log').read_text().strip(), 'OK')
        self.assertTrue((self.dest / 'results.json').is_file())

    def test_negative_control_must_actually_fail(self):
        with self.assertRaisesRegex(ValueError, 'negative control'):
            p = self.plan(self.gate('negative', 'pass', kind='negative', expected_exit_codes=[0]))
            path = self.base / 'plan.json'
            path.write_text(json.dumps(p))
            gates.load_plan(path)
        result = gates.run_plan(self.plan(self.gate('negative', 'pass', kind='negative', expected_exit_codes=[1])),
                                self.root, self.dest)
        self.assertEqual(result['gates'][0]['status'], 'failed')
        self.assertNotEqual(result['overall'], 'passed')

    def test_nunit_3_metrics_enforced(self):
        (self.root / 'tests.xml').write_text('<test-run total="10" passed="9" failed="0" skipped="1" />')
        gate = self.gate('tests', 'pass', nunit_xml={'path': 'tests.xml', 'expected': {'total': 10, 'passed': 9, 'failed': 0, 'skipped': 1}})
        report = gates.run_plan(self.plan(gate), self.root, self.dest)
        self.assertEqual(report['gates'][0]['status'], 'passed')
        gate['nunit_xml']['expected']['passed'] = 10
        report = gates.run_plan(self.plan(gate), self.root, self.dest)
        self.assertEqual(report['gates'][0]['status'], 'failed')
        self.assertIn('NUnit counts', report['gates'][0]['reason'])

    def test_missing_binary_and_fail_fast_not_executed(self):
        missing = {'id': 'absent', 'command': ['this-command-does-not-exist-anywhere-987']}
        report = gates.run_plan(self.plan(missing, self.gate('later', 'pass')), self.root, self.dest, fail_fast=True)
        self.assertEqual([x['status'] for x in report['gates']], ['blocked', 'not_executed'])
        self.assertEqual(report['overall'], 'incomplete_or_failed')

    def test_timeout_is_explicit(self):
        report = gates.run_plan(self.plan(self.gate('slow', 'import time;time.sleep(3)', timeout_seconds=1)),
                                self.root, self.dest)
        self.assertEqual(report['gates'][0]['status'], 'timed_out')

    def test_cwd_cannot_escape_source(self):
        report = gates.run_plan(self.plan(self.gate('escape', 'pass', cwd='..')), self.root, self.dest)
        self.assertEqual(report['gates'][0]['status'], 'failed')

    def test_source_sha_mismatch_blocks_before_any_command(self):
        with self.assertRaisesRegex(ValueError, 'expected_commit'):
            gates.run_plan({**self.plan(self.gate('should-not-execute', 'pass')),
                            'expected_commit': 'f' * 40}, self.root, self.dest)
        self.assertFalse((self.dest / 'should-not-execute.log').exists())

    def test_plan_schema_rejects_duplicate_or_shell_command(self):
        p = self.plan(self.gate('same', 'pass'), self.gate('same', 'pass'))
        path = self.base / 'p.json'
        path.write_text(json.dumps(p))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            gates.load_plan(path)
        p = self.plan({'id': 'shell', 'command': 'echo hello'})
        path.write_text(json.dumps(p))
        with self.assertRaisesRegex(ValueError, 'argv'):
            gates.load_plan(path)

    def test_output_must_be_outside_checkout(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            gates.run_plan(self.plan(self.gate('hi', 'pass')), self.root, self.root / 'evidence')


if __name__ == '__main__':
    unittest.main()
