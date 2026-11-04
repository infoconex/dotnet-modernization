import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import toolchain


class ToolchainTests(unittest.TestCase):
    def test_sdk_and_runtime_lines(self):
        sdk = {'status': 'ok', 'output': '8.0.428 [/opt/dotnet/sdk]\n10.0.403 [/opt/dotnet/sdk]\nnoise'}
        rt = {'status': 'ok', 'output': 'Microsoft.NETCore.App 10.0.14 [/opt/dotnet/shared/Microsoft.NETCore.App]'}
        self.assertEqual(len(toolchain.list_sdk_lines(sdk)), 2)
        self.assertEqual(toolchain.list_runtime_lines(rt)[0]['name'], 'Microsoft.NETCore.App')
        self.assertEqual(toolchain.list_sdk_lines({'status': 'not_installed'}), [])

    def test_no_dotnet_or_nuget_is_observed_not_invented(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(toolchain.shutil, 'which', return_value=None):
            report = toolchain.collect(folder)
        self.assertEqual(report['tools']['dotnet']['status'], 'not_installed')
        self.assertEqual(report['tools']['nuget']['status'], 'not_installed')
        self.assertEqual(report['sdk_targeting_packs'], [])

    def test_dotnet_selection_and_probe_failure_kept_distinct(self):
        def which(name):
            return '/usr/bin/' + name if name == 'dotnet' else None

        def probe(argv, cwd):
            if '--version' in argv:
                return {'status': 'failed', 'exit_code': 145, 'output': ''}
            if '--list-sdks' in argv:
                return {'status': 'ok', 'output': '10.0.403 [/opt/disabled/sdk]\n'}
            if '--list-runtimes' in argv:
                return {'status': 'ok', 'output': ''}
            return {'status': 'failed', 'exit_code': 1}

        with tempfile.TemporaryDirectory() as folder, patch.object(toolchain.shutil, 'which', side_effect=which), \
             patch.object(toolchain, 'probe', side_effect=probe):
            report = toolchain.collect(folder)
        self.assertEqual(report['tools']['dotnet']['selection']['status'], 'failed')
        self.assertEqual(report['tools']['dotnet']['sdks'][0]['version'], '10.0.403')
        self.assertIsNone(report['tools']['dotnet']['selection']['version'])

    def test_inventory_output_cannot_modify_source(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(toolchain.main(['--source', folder, '--output', str(Path(folder) / 'out.json')]), 2)


if __name__ == '__main__':
    unittest.main()
