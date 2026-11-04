import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import compatibility


class CompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name) / 'application'
        self.root.mkdir()
        self.out = Path(self.work.name) / 'evidence'

    def put(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding='utf-8')
        return target

    def init_git(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.test', 'commit', '-m', 'fixture', '-q'], check=True)
        return subprocess.check_output(['git', '-C', str(self.root), 'rev-parse', 'HEAD'], text=True).strip()

    def api(self, text='# generated\nassembly My.Lib version=1.0.0.0\nT My.Lib.Thing\n'):
        return self.put('contracts/api.txt', text)

    def assemblies(self, version='1.0.0.0'):
        return self.put('contracts/assemblies.json',
                        json.dumps({'schema_version': 1, 'assemblies': [{
                            'name': 'My.Lib', 'version': version, 'culture': 'neutral', 'public_key_token': 'null'}]}))

    def resources(self, values=None):
        if values is None:
            values = ['My.Lib.Messages.resources']
        return self.put('contracts/resources.json',
                        json.dumps({'schema_version': 1, 'assemblies': [{
                            'name': 'My.Lib', 'resources': values}]}))

    def nuget(self, name='sample.1.0.0.nupkg', dep_version='[2.1.0]', extra=False,
              version='1.0.0', unsafe=False):
        path = self.root / name
        nuspec = (f'<package xmlns="http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd">'
                  f'<metadata><id>sample</id><version>{version}</version><dependencies>'
                  f'<group targetFramework="net48"><dependency id="CsvHelper" version="{dep_version}" />'
                  f'</group></dependencies></metadata></package>')
        with zipfile.ZipFile(path, 'w') as package:
            package.writestr('sample.nuspec', nuspec)
            package.writestr('lib/net48/My.Lib.dll', b'example bytes')
            if extra:
                package.writestr('lib/net48/Other.dll', b'example')
            if unsafe:
                package.writestr('../outside.dll', b'evil')
        return path

    def nunit(self, name='tests.xml', failed=False):
        result = 'Failed' if failed else 'Passed'
        return self.put(name, f'''<test-run total="2" passed="{0 if failed else 1}" failed="{1 if failed else 0}" skipped="1" inconclusive="0">
          <test-suite><test-case fullname="Thing.Works" result="{result}"/>
          <test-case fullname="Thing.Skipped" result="Skipped" label="Ignored"/></test-suite></test-run>''')

    def spec(self):
        return {'schema_version': 1, 'components': {
            'api': 'contracts/api.txt',
            'assemblies': 'contracts/assemblies.json',
            'resources': 'contracts/resources.json',
            'packages': [{'id': 'library', 'path': 'sample.1.0.0.nupkg'}],
            'tests': [{'id': 'unit', 'path': 'tests.xml'}]}}

    def complete(self):
        self.api()
        self.assemblies()
        self.resources()
        self.nuget()
        self.nunit()

    def test_all_five_contracts_match_and_preserve_source(self):
        self.complete()
        sha = self.init_git()
        old = compatibility.capture(self.root, self.spec(), sha)
        new = compatibility.capture(self.root, self.spec(), sha)
        report = compatibility.compare(old, new)
        self.assertEqual(report['overall'], 'matched')
        self.assertEqual(report['provenance'], 'clean_committed')
        self.assertEqual(set(report['components']), set(compatibility.COMPONENTS))
        self.assertTrue(all(v['status'] == 'matched' for v in report['components'].values()))
        self.assertEqual(old['components']['tests']['data']['unit']['counts']['skipped'], 1)
        self.assertEqual(len(old['components']['packages']['input_artifacts'][0]['sha256']), 64)
        self.assertEqual(old['components']['packages']['data']['library']['dependencies'][0]['target_framework'], 'net48')
        self.assertIn('T My.Lib.Thing', old['components']['api']['data'])
        self.assertFalse(list(self.root.glob('evidence*')))

    def test_api_addition_removal_and_package_dependency_change_detected(self):
        self.complete()
        old = compatibility.capture(self.root, self.spec())
        self.api('T My.Lib.Changed\n')
        self.nuget(dep_version='[3.0.0]')
        new = compatibility.capture(self.root, self.spec())
        report = compatibility.compare(old, new)
        self.assertEqual(report['overall'], 'changes_detected')
        self.assertEqual(report['components']['api']['status'], 'changed')
        self.assertEqual(report['components']['packages']['status'], 'changed')
        self.assertTrue(any('dependencies' in x['path'] for x in report['components']['packages']['differences']))
        self.assertTrue(any(x['change'] == 'added' for x in report['components']['api']['differences']))
        self.assertTrue(any(x['change'] == 'removed' for x in report['components']['api']['differences']))

    def test_assembly_resource_and_test_case_drift_detected(self):
        self.complete()
        old = compatibility.capture(self.root, self.spec())
        self.assemblies('2.0.0.0')
        self.resources(['My.Lib.New.resources'])
        self.nunit(failed=True)
        new = compatibility.capture(self.root, self.spec())
        report = compatibility.compare(old, new)
        self.assertEqual(report['overall'], 'changes_detected')
        for section in ('assemblies', 'resources', 'tests'):
            self.assertEqual(report['components'][section]['status'], 'changed')
        self.assertIn('/unit/cases/Thing.Works/result',
                      [x['path'] for x in report['components']['tests']['differences']])

    def test_package_timestamps_and_bytes_ignored_but_payload_paths_detected(self):
        self.nuget()
        before = compatibility.package_contract(self.root / 'sample.1.0.0.nupkg')
        with zipfile.ZipFile(self.root / 'sample.1.0.0.nupkg', 'w') as zip_file:
            zip_file.writestr('sample.nuspec', '<package><metadata><id>sample</id><version>1.0.0</version><dependencies><group targetFramework="net48"><dependency id="CsvHelper" version="[2.1.0]"/></group></dependencies></metadata></package>')
            zip_file.writestr('lib/net48/My.Lib.dll', b'completely different binary')
            zip_file.writestr('package/services/metadata/core-properties/auto.psmdcp', b'changing metadata')
        after = compatibility.package_contract(self.root / 'sample.1.0.0.nupkg')
        self.assertEqual(before, after)
        self.nuget(extra=True)
        self.assertIn('lib/net48/Other.dll', compatibility.package_contract(self.root / 'sample.1.0.0.nupkg')['payload_paths'])

    def test_package_byte_fingerprint_changes_without_false_contract_drift(self):
        self.nuget()
        spec = {'schema_version': 1, 'components': {'packages': [{'id': 'library', 'path': 'sample.1.0.0.nupkg'}]}}
        before = compatibility.capture(self.root, spec)
        with zipfile.ZipFile(self.root / 'sample.1.0.0.nupkg', 'w') as archive:
            archive.writestr('sample.nuspec', '<package><metadata><id>sample</id><version>1.0.0</version><dependencies><group targetFramework="net48"><dependency id="CsvHelper" version="[2.1.0]"/></group></dependencies></metadata></package>')
            archive.writestr('lib/net48/My.Lib.dll', b'different DLL bytes')
        after = compatibility.capture(self.root, spec)
        result = compatibility.compare(before, after)
        self.assertEqual(result['components']['packages']['status'], 'matched')
        self.assertNotEqual(result['components']['packages']['baseline_input_artifacts'][0]['sha256'],
                            result['components']['packages']['candidate_input_artifacts'][0]['sha256'])

    def test_nuspec_additional_reference_and_content_contract_changes(self):
        path = self.root / 'sample.1.0.0.nupkg'
        def create(reference):
            nuspec = (f'<package minClientVersion="3.0"><metadata><id>sample</id><version>1.0.0</version>'
                      f'<dependencies><group targetFramework="net48" /></dependencies>'
                      f'<references><group targetFramework="net48"><reference file="{reference}" /></group></references>'
                      f'<frameworkReferences><group targetFramework="net6.0">'
                      f'<frameworkReference name="Microsoft.AspNetCore.App" /></group></frameworkReferences>'
                      f'<frameworkAssemblies><frameworkAssembly assemblyName="System.Xml" targetFramework="net48" /></frameworkAssemblies>'
                      f'<contentFiles><files include="any/any/*" buildAction="Content" copyToOutput="true"/></contentFiles>'
                      f'<packageTypes><packageType name="Dependency" /></packageTypes>'
                      f'</metadata></package>')
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('sample.nuspec', nuspec)
                archive.writestr('lib/net48/A.dll', b'bytes')
        create('A.dll')
        before = compatibility.package_contract(path)
        self.assertEqual(before['dependency_groups'], ['net48'])
        self.assertEqual(before['min_client_version'], '3.0')
        self.assertEqual(set(before['additional_contracts']),
                         {'references', 'frameworkReferences', 'frameworkAssemblies', 'contentFiles', 'packageTypes'})
        create('B.dll')
        after = compatibility.package_contract(path)
        self.assertEqual(before['payload_paths'], after['payload_paths'])
        self.assertNotEqual(before['additional_contracts'], after['additional_contracts'])

    def test_missing_category_and_incomplete_capture_are_not_green(self):
        self.api()
        baseline = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}})
        missing = compatibility.capture(self.root, {'schema_version': 1, 'components': {'assemblies': 'not-there.json'}})
        self.assertEqual(missing['components']['assemblies']['status'], 'error')
        report = compatibility.compare(baseline, missing)
        self.assertEqual(report['overall'], 'incomplete')
        self.assertEqual(report['components']['api']['status'], 'missing_evidence')

    def test_external_artifacts_keep_clean_git_source_and_detect_api_drift(self):
        self.api()
        sha = self.init_git()
        artifacts = self.out / 'generated'
        artifacts.mkdir(parents=True)
        (artifacts / 'public-api.txt').write_text('T Fixture.Original\\n')
        spec = {'schema_version': 1, 'components': {'api': 'public-api.txt'}}
        baseline = compatibility.capture(self.root, spec, sha, artifacts_root=artifacts)
        self.assertEqual(baseline['source']['dirty_paths'], [])
        self.assertEqual(baseline['artifacts_root'], str(artifacts))
        (artifacts / 'public-api.txt').write_text('T Fixture.Changed\\n')
        candidate = compatibility.capture(self.root, spec, sha, artifacts_root=artifacts)
        result = compatibility.compare(baseline, candidate)
        self.assertEqual(result['overall'], 'changes_detected')
        self.assertEqual(result['provenance'], 'clean_committed')

    def test_no_git_provenance_cannot_yield_verified_match(self):
        self.api()
        obj = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}})
        self.assertEqual(compatibility.compare(obj, obj)['overall'], 'matched_unverified_provenance')

    def test_dirty_candidate_cannot_yield_verified_match(self):
        self.api()
        sha = self.init_git()
        before = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}}, sha)
        self.put('scratch.txt', 'untracked')
        after = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}}, sha)
        self.assertEqual(compatibility.compare(before, after)['overall'], 'matched_unverified_provenance')

    def test_mismatched_expected_sha_prevents_capture(self):
        self.api()
        self.init_git()
        with self.assertRaises(ValueError):
            compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}},
                                  '0' * 40)

    def test_unsafe_package_archive_is_rejected(self):
        self.nuget(unsafe=True)
        with self.assertRaisesRegex(ValueError, 'unsafe package'):
            compatibility.package_contract(self.root / 'sample.1.0.0.nupkg')

    def test_nunit_mismatched_total_and_duplicate_cases_rejected(self):
        self.nunit()
        self.put('tests.xml', '<test-run total="3" passed="1" failed="0" skipped="1"><test-case fullname="T" result="Passed"/></test-run>')
        with self.assertRaisesRegex(ValueError, 'inconsistent'):
            compatibility.tests_contract(self.root / 'tests.xml')
        self.put('tests.xml', '<test-run total="2" passed="2" failed="0" skipped="0"><test-case fullname="T" result="Passed"/><test-case fullname="T" result="Passed"/></test-run>')
        with self.assertRaisesRegex(ValueError, 'unique'):
            compatibility.tests_contract(self.root / 'tests.xml')

    def test_duplicate_api_and_invalid_manifests_rejected(self):
        p = self.api('A\nA\n')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            compatibility.api_lines(p)
        self.put('contracts/assemblies.json', '{"schema_version":1,"assemblies":[{"name":"Lib","version":"1.0"},{"name":"Lib","version":"2.0"}]}')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            compatibility.assembly_contract(self.root / 'contracts/assemblies.json', 'assemblies')
        self.put('contracts/resources.json', '{"schema_version":1,"assemblies":[{"name":"Lib","resources":["X","X"]}]}')
        with self.assertRaisesRegex(ValueError, 'unique'):
            compatibility.assembly_contract(self.root / 'contracts/resources.json', 'resources')

    def test_output_file_cannot_be_inside_source(self):
        self.api()
        spec = self.put('spec.json', json.dumps({'schema_version': 1, 'components': {'api': 'contracts/api.txt'}}))
        target = self.root / 'report.json'
        self.assertEqual(compatibility.main(['capture', '--source', str(self.root), '--spec', str(spec),
                                             '--output', str(target)]), 2)
        self.assertFalse(target.exists())

    def test_compare_cli_nonzero_for_missing_git_or_changes(self):
        self.api()
        x = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}})
        self.out.mkdir()
        before = self.out / 'before.json'
        after = self.out / 'after.json'
        before.write_text(json.dumps(x))
        after.write_text(json.dumps(x))
        self.assertEqual(compatibility.main(['compare', '--baseline', str(before), '--candidate', str(after),
                                            '--output', str(self.out / 'comparison.json')]), 1)
        self.assertEqual(json.loads((self.out / 'comparison.json').read_text())['overall'], 'matched_unverified_provenance')

    def test_compare_cannot_overwrite_source_snapshot(self):
        self.api()
        report = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'contracts/api.txt'}})
        self.out.mkdir()
        path = self.out / 'snapshot.json'
        path.write_text(json.dumps(report))
        self.assertEqual(compatibility.main(['compare', '--baseline', str(path), '--candidate', str(path),
                                            '--output', str(path)]), 2)
        self.assertEqual(json.loads(path.read_text())['kind'], 'compatibility-snapshot')

    def test_capture_errors_report_without_exception(self):
        report = compatibility.capture(self.root, {'schema_version': 1, 'components': {'api': 'missing.txt'}})
        self.assertEqual(len(report['capture_errors']), 1)
        self.assertEqual(report['components']['api']['status'], 'error')

    def test_spec_paths_must_stay_in_checkout(self):
        with self.assertRaises(ValueError):
            compatibility.relative_file(self.root, '../outside.txt')
        with self.assertRaises(ValueError):
            compatibility.capture(self.root, {'schema_version': 1, 'components': {'nothing': 'file'}})


if __name__ == '__main__':
    unittest.main()
