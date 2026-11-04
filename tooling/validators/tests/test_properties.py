import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import properties


class FakeRun:
    def __init__(self, out='', code=0, err=''):
        self.stdout = out
        self.stderr = err
        self.returncode = code


class PropertyTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / 'app'
        self.root.mkdir()
        (self.root / 'lib.csproj').write_text('<Project/>')

    def test_evaluated_properties_with_context_and_errors(self):
        seen = []
        def fake(argv, **kwargs):
            seen.append(argv)
            if '-getProperty:WarningLevel' in argv:
                return FakeRun(code=1, err='MSB1234: hidden secret would never be saved')
            if '-getProperty:LangVersion' in argv:
                return FakeRun('7.3\n')
            return FakeRun('')
        matrix = {'schema_version': 1, 'properties': ['LangVersion', 'WarningLevel', 'DefineConstants'],
                  'contexts': [{'Configuration': 'Release', 'Platform': 'AnyCPU'}]}
        with patch.object(properties, 'snapshot', return_value={'commit': None, 'branch': None, 'dirty_paths': None}), \
             patch.object(properties.subprocess, 'run', side_effect=fake):
            report = properties.evaluate(self.root, ['lib.csproj'], matrix, ['fake-msbuild'])
        observed = report['projects'][0]['contexts'][0]['properties']
        self.assertEqual(observed['LangVersion']['value'], '7.3')
        self.assertEqual(observed['WarningLevel']['error_codes'], ['MSB1234'])
        self.assertEqual(observed['DefineConstants']['status'], 'empty_or_undefined')
        self.assertIn('-property:Configuration=Release', seen[0])
        self.assertNotIn('secret', json.dumps(report))

    def test_matrix_rejects_injection_sensitive_and_duplicate_values(self):
        for item in [
            {'schema_version': 1, 'properties': ['Password']},
            {'schema_version': 1, 'properties': ['OutputPath', 'OutputPath']},
            {'schema_version': 1, 'properties': ['LangVersion'], 'contexts': [{'Configuration': 'Debug;Evil=yes'}]},
            {'schema_version': 1, 'properties': ['LangVersion'], 'contexts': [{'Unexpected': 'x'}]},
        ]:
            with self.assertRaises(ValueError):
                properties.parse_matrix(item)

    def test_reject_project_outside_checkout(self):
        with self.assertRaises(ValueError):
            properties.evaluate(self.root, ['../outside.csproj'],
                                {'schema_version': 1, 'properties': ['LangVersion']}, ['fake'])

    def test_timeout_and_missing_binary_are_nonpassing(self):
        matrix = {'schema_version': 1, 'properties': ['LangVersion']}
        with patch.object(properties.subprocess, 'run', side_effect=FileNotFoundError()):
            report = properties.evaluate(self.root, ['lib.csproj'], matrix, ['fake'])
        self.assertEqual(report['projects'][0]['contexts'][0]['properties']['LangVersion']['status'], 'blocked')
        self.assertEqual(properties.main(['--source', str(self.root), '--project', 'lib.csproj',
                                          '--matrix', str(self.root / 'missing.json'), '--output', str(self.root / 'out.json')]), 2)


if __name__ == '__main__':
    unittest.main()
