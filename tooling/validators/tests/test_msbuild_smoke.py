"""Integration smoke test for installed dotnet MSBuild; skipped on SDK-less hosts."""
from pathlib import Path
import shutil
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import properties


class DotnetMsbuildSmoke(unittest.TestCase):
    @unittest.skipUnless(shutil.which('dotnet'), 'dotnet not installed on this host')
    def test_actual_evaluated_properties_without_build_or_restore(self):
        with tempfile.TemporaryDirectory() as workspace:
            root = Path(workspace)
            (root / 'Legacy.csproj').write_text('''<Project><PropertyGroup>
              <LangVersion>7.3</LangVersion>
              <WarningLevel Condition="'$(Configuration)' == 'Release'">4</WarningLevel>
              </PropertyGroup></Project>''', encoding='utf-8')
            matrix = {'schema_version': 1, 'properties': ['LangVersion', 'WarningLevel'],
                      'contexts': [{'Configuration': 'Release'}, {'Configuration': 'Debug'}]}
            report = properties.evaluate(root, ['Legacy.csproj'], matrix, [shutil.which('dotnet'), 'msbuild'])
            contexts = report['projects'][0]['contexts']
            self.assertEqual(contexts[0]['properties']['LangVersion']['value'], '7.3')
            self.assertEqual(contexts[0]['properties']['WarningLevel']['value'], '4')
            self.assertEqual(contexts[1]['properties']['LangVersion']['value'], '7.3')
            self.assertIn(contexts[1]['properties']['WarningLevel']['status'], {'evaluated', 'empty_or_undefined'})


if __name__ == '__main__':
    unittest.main()
