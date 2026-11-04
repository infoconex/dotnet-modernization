import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dependencies


class DependenciesTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name) / 'app'
        self.root.mkdir()

    def write(self, name, content):
        p = self.root / name
        p.parent.mkdir(exist_ok=True, parents=True)
        p.write_text(content)
        return p

    def test_assets_is_target_specific_and_resolves_edges(self):
        data = {'version': 3,
                'projectFileDependencyGroups': {'net8.0': ['CsvTool >= 2.1.0']},
                'project': {'frameworks': {'net8.0': {'dependencies': {'CsvTool': {'target': 'Package', 'version': '[2.1.0, )'}}}}},
                'libraries': {'CsvTool/2.1.0': {'type': 'package'}, 'Utility/1.0.0': {'type': 'package'}},
                'targets': {'net8.0': {
                    'CsvTool/2.1.0': {'type': 'package', 'dependencies': {'Utility': '1.0.0'},
                                      'compile': {'lib/net8.0/CsvTool.dll': {}}, 'runtime': {'lib/net8.0/CsvTool.dll': {}}},
                    'Utility/1.0.0': {'type': 'package', 'compile': {'lib/net8.0/Utility.dll': {}}}},
                    'net8.0/win-x64': {'CsvTool/2.1.0': {'type': 'package', 'dependencies': {'Utility': '1.0.0'}},
                                       'Utility/1.0.0': {'type': 'package'}}},
                'packageFolders': {'C:/cache': {}}}
        self.write('project/obj/project.assets.json', json.dumps(data))
        report = dependencies.collect(self.root)
        self.assertEqual(report['resolution_status'], 'assets_available')
        self.assertEqual(len(report['assets'][0]['targets']), 2)
        nodes = report['assets'][0]['targets'][0]['libraries']
        top = next(n for n in nodes if n['id'] == 'CsvTool')
        self.assertTrue(top['declared_direct'])
        self.assertEqual(top['dependencies'][0]['resolved'], 'Utility/1.0.0')
        self.assertEqual(top['compile_assets'], 1)
        self.assertFalse(next(n for n in nodes if n['id'] == 'Utility')['declared_direct'])

    def test_legacy_config_only_does_not_claim_complete_dependency_graph(self):
        self.write('Legacy/packages.config', '<packages><package id="Vendor.Library" version="1.2.3" targetFramework="net48" /></packages>')
        pkg = Path(self.t.name) / 'packages'
        (pkg / 'Vendor.Library.1.2.3').mkdir(parents=True)
        report = dependencies.collect(self.root, pkg)
        self.assertEqual(report['resolution_status'], 'legacy_metadata_only')
        legacy = report['legacy'][0]
        self.assertEqual(legacy['packages'][0]['local_package_directory'], 'directory_present')
        self.assertIn('not a complete resolved dependency graph', legacy['limitations'][0])

    def test_missing_and_malformed_assets_not_silently_accepted(self):
        self.assertEqual(dependencies.collect(self.root)['resolution_status'], 'no_restore_evidence')
        self.write('A/obj/project.assets.json', '{broken')
        result = dependencies.collect(self.root)
        self.assertEqual(result['resolution_status'], 'partial')
        self.assertEqual(result['errors'][0]['path'], 'A/obj/project.assets.json')

    def test_missing_direct_classification_is_unknown_not_transitive(self):
        data = {'version': 3, 'targets': {'net8.0': {'Unknown/1.0.0': {'type': 'package'}}},
                'libraries': {'Unknown/1.0.0': {'type': 'package'}}}
        self.write('App/obj/project.assets.json', json.dumps(data))
        report = dependencies.collect(self.root)
        target = report['assets'][0]['targets'][0]
        self.assertFalse(target['direct_classification_available'])
        self.assertIsNone(target['libraries'][0]['declared_direct'])

    def test_output_must_not_contaminate_checkout(self):
        self.assertEqual(dependencies.main(['--source', str(self.root), '--output', str(self.root / 'result.json')]), 2)


if __name__ == '__main__':
    unittest.main()
