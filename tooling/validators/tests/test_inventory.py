import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import inventory


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, text):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
        return p

    def test_traditional_and_sdk_style_scoped_source_inventory(self):
        self.write('Legacy/Legacy.csproj', '''<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
          <PropertyGroup><TargetFrameworkVersion>v4.8</TargetFrameworkVersion><LangVersion>7.3</LangVersion></PropertyGroup>
          <PropertyGroup Condition="'$(Configuration)' == 'Release'"><Optimize>true</Optimize></PropertyGroup>
          <ItemGroup><ProjectReference Include="../Core/Core.csproj" />
            <Reference Include="Vendor.Lib"><HintPath>../lib/Vendor.Lib.dll</HintPath></Reference>
            <COMReference Include="LegacyCom"><Guid>{123}</Guid></COMReference></ItemGroup></Project>''')
        self.write('Core/Core.csproj', '''<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFrameworks>net8.0;net10.0</TargetFrameworks></PropertyGroup>
            <ItemGroup Condition="'$(TargetFramework)' == 'net8.0'"><PackageReference Include="Some.Package" Version="1.2.3" /></ItemGroup></Project>''')
        self.write('Legacy/packages.config', '<packages><package id="Legacy.Package" version="4.5.6" targetFramework="net48" /></packages>')
        self.write('Directory.Packages.props', '<Project><ItemGroup><PackageVersion Include="Centrally.Managed" Version="2.0.0" /></ItemGroup></Project>')
        self.write('pkg/lib.nuspec', '<package><metadata><dependencies><group targetFramework="net48"><dependency id="Legacy.Package" version="[4.5.6]" /></group></dependencies></metadata></package>')
        self.write('legacy.sln', '')
        self.write('obj/Skip.csproj', '<Project/>')
        self.write('bin/packages.config', '<packages/>')
        obj = inventory.generate(self.root)
        self.assertEqual(len(obj['projects']), 2)
        self.assertEqual(len(obj['solutions']), 1)
        self.assertEqual(len(obj['packages_config']), 1)
        self.assertEqual(len(obj['nuspec'][0]['dependencies']), 1)
        self.assertEqual(obj['central_package_versions'][0]['Include'], 'Centrally.Managed')
        legacy = next(p for p in obj['projects'] if p['path'].startswith('Legacy/'))
        core = next(p for p in obj['projects'] if p['path'].startswith('Core/'))
        self.assertEqual(legacy['sdk_declarations'], [])
        self.assertEqual(len(legacy['com_references']), 1)
        self.assertEqual(len(legacy['project_references']), 1)
        self.assertEqual(legacy['assembly_references'][0]['metadata']['HintPath']['value'], '../lib/Vendor.Lib.dll')
        self.assertEqual([p['group_condition'] for p in legacy['properties'] if p['name'] == 'Optimize'], ["'$(Configuration)' == 'Release'"])
        self.assertEqual(core['sdk_declarations'][0]['value'], 'Microsoft.NET.Sdk')
        self.assertEqual(core['package_references'][0]['Version'], '1.2.3')
        self.assertFalse(any('Skip' in p['path'] for p in obj['projects']))
        self.assertTrue(any('Runtime service dependencies' in t for t in obj['limitations']))
        self.assertFalse(obj['errors'])

    def test_redacts_sensitive_msbuild_values(self):
        self.write('Safe.csproj', '<Project><PropertyGroup><ApiKey>do-not-expose</ApiKey><Password>abc</Password><Company>Public</Company></PropertyGroup><ItemGroup><Reference Include="X"><Credential>private</Credential></Reference></ItemGroup></Project>')
        data = inventory.generate(self.root)
        project = data['projects'][0]
        values = {item['name']: item['declared_value'] for item in project['properties']}
        self.assertEqual(values['ApiKey'], '<redacted>')
        self.assertEqual(values['Password'], '<redacted>')
        self.assertEqual(values['Company'], 'Public')
        self.assertEqual(project['assembly_references'][0]['metadata']['Credential']['value'], '<redacted>')

    def test_malformed_source_is_partial_not_a_success(self):
        self.write('Broken.csproj', '<Project><PropertyGroup>')
        self.write('Good.csproj', '<Project/>')
        output = self.root / 'result.json'
        self.assertEqual(inventory.main(['--source', str(self.root), '--output', str(output)]), 2)
        result = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(len(result['projects']), 1)
        self.assertEqual(result['errors'][0]['path'], 'Broken.csproj')

    def test_expected_commit_mismatch_exits_nonzero(self):
        self.write('Good.csproj', '<Project/>')
        output = self.root / 'result.json'
        self.assertEqual(inventory.main(['--source', str(self.root), '--output', str(output),
                                         '--expect-commit', '0' * 40]), 2)
        self.assertTrue(output.exists())


if __name__ == '__main__':
    unittest.main()
