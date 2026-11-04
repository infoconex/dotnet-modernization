"""Synthetic pinned NuGet ZIP controls for the generic metadata-only asset inspector."""
import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import nuget_build_assets as mod

NUSPEC = b"""<?xml version="1.0"?>
<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">
 <metadata><id>Microsoft.SourceLink.GitHub</id><version>10.0.403</version>
 <authors>Microsoft</authors><description>fixture</description>
 <dependencies><group targetFramework=".NETFramework4.7.2">
  <dependency id="Microsoft.Build.Tasks.Git" version="[10.0.403,)" />
  <dependency id="Microsoft.SourceLink.Common" version="[10.0.403,)" />
 </group></dependencies>
 </metadata></package>"""


class NugetBuildAssetAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.archive = self.root / 'package.nupkg'

    def create(self, content=None):
        if content is None:
            content = {
                'Microsoft.SourceLink.GitHub.nuspec': NUSPEC,
                'build/Microsoft.SourceLink.GitHub.props': b'<Project />',
                'build/Microsoft.SourceLink.GitHub.targets': b'<Project />',
                'tools/Tool.dll': b'not executed',
            }
        with zipfile.ZipFile(self.archive, 'w') as archive:
            for name, value in content.items():
                archive.writestr(name, value)
        return self.archive

    def test_valid_assets_and_dependency_metadata(self):
        self.create()
        result = mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')
        self.assertEqual(result['archive_member_count'], 4)
        self.assertEqual(len(result['declared_dependencies']), 2)
        self.assertIn('build/Microsoft.SourceLink.GitHub.targets',
                      result['msbuild_import_candidates'])
        self.assertEqual(len(result['assets']['tools']), 1)
        self.assertEqual(result['assets']['lib'], [])
        self.assertTrue(result['metadata_only_no_target_execution'])

    def test_manifest_is_repeatable_and_requires_ids(self):
        self.create()
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'packages': [{'id': 'Microsoft.SourceLink.GitHub',
                                                      'version': '10.0.403',
                                                      'path': str(self.archive)}]}))
        first = mod.audit(manifest)
        self.assertEqual(first['schema_version'], 1)
        self.assertEqual(first['kind'], 'pinned-nuget-archive-build-asset-audit')
        self.assertEqual(len(first['packages']), 1)
        self.assertEqual(first, mod.audit(manifest))

    def test_identity_mismatch_fails_closed(self):
        self.create()
        with self.assertRaisesRegex(ValueError, 'Unexpected embedded'):
            mod.inspect(self.archive, 'Microsoft.Build.Tasks.Git', '10.0.403')

    def test_missing_nuspec_fails_closed(self):
        self.create({'build/Target.targets': b'no nuspec'})
        with self.assertRaisesRegex(ValueError, 'one embedded'):
            mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')

    def test_zip_traversal_fails_closed(self):
        self.create({'Microsoft.SourceLink.GitHub.nuspec': NUSPEC,
                     '../outside.txt': b'escape'})
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')

    def test_double_backslash_path_fails_closed(self):
        self.create({'Microsoft.SourceLink.GitHub.nuspec': NUSPEC, 'build\\bad.targets': b'bad'})
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')

    def test_duplicate_casefold_path_fails_closed(self):
        with zipfile.ZipFile(self.archive, 'w') as archive:
            archive.writestr('Microsoft.SourceLink.GitHub.nuspec', NUSPEC)
            archive.writestr('build/Thing.props', b'first')
            archive.writestr('BUILD/thing.props', b'second')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')

    def test_symlink_fails_closed(self):
        with zipfile.ZipFile(self.archive, 'w') as archive:
            archive.writestr('Microsoft.SourceLink.GitHub.nuspec', NUSPEC)
            entry = zipfile.ZipInfo('build/Untrusted.targets')
            entry.create_system = 3
            entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(entry, 'source')
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')

    def test_malformed_nuspec_fails_closed(self):
        self.create({'Microsoft.SourceLink.GitHub.nuspec': b'<package><metadata>'})
        with self.assertRaises(Exception):
            mod.inspect(self.archive, 'Microsoft.SourceLink.GitHub', '10.0.403')

    def test_duplicate_package_in_manifest_fails_closed(self):
        self.create()
        entry = {'id': 'Microsoft.SourceLink.GitHub', 'version': '10.0.403', 'path': str(self.archive)}
        manifest = self.root / 'manifest.json'
        manifest.write_text(json.dumps({'packages': [entry, entry]}))
        with self.assertRaisesRegex(ValueError, 'Duplicate pinned'):
            mod.audit(manifest)

    def test_missing_archive_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'Missing or oversized'):
            mod.inspect(self.root / 'missing.nupkg', 'Microsoft.SourceLink.GitHub', '10.0.403')


if __name__ == '__main__':
    unittest.main()
