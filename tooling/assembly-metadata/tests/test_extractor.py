"""Black-box integration checks. Requires .NET 10 SDK; no NuGet add-ons."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parent.parent
PROJECT = SOURCE / 'src' / 'AssemblyMetadata.csproj'
FIXTURE = SOURCE / 'tests' / 'Fixture'

@unittest.skipUnless(shutil.which('dotnet'), '.NET SDK is not installed')
class ExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not shutil.which('dotnet'):
            return
        cls.temp = tempfile.TemporaryDirectory()
        cls.scratch = Path(cls.temp.name)
        shutil.copy2(SOURCE / 'global.json', cls.scratch / 'global.json')
        version = subprocess.run(['dotnet', '--version'], cwd=cls.scratch, capture_output=True, text=True, check=True)
        assert version.stdout.strip() == '10.0.403', version.stdout
        cls.fixture = cls.scratch / 'fixture'
        shutil.copytree(FIXTURE, cls.fixture)
        cls.app = cls.scratch / 'extractor'
        shutil.copytree(PROJECT.parent, cls.app)
        cls.build(cls.app / PROJECT.name)
        cls.build(cls.fixture / 'Fixture.csproj')
        cls.binary = cls.fixture / 'bin' / 'Release' / 'net10.0' / 'Fixture.Library.dll'
        cls.program = cls.app / 'bin' / 'Release' / 'net10.0' / 'AssemblyMetadata.dll'
        assert cls.binary.is_file() and cls.program.is_file()

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'temp'):
            cls.temp.cleanup()

    @classmethod
    def build(cls, project):
        run = subprocess.run(['dotnet', 'build', str(project), '-c', 'Release', '-v', 'quiet', '-nologo'],
                             cwd=cls.scratch, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             timeout=120, check=False)
        if run.returncode != 0:
            raise AssertionError(f'Build failed: {project}\n{run.stdout[:6000]}')

    def extract(self, binary, output):
        return subprocess.run(['dotnet', str(self.program), '--assembly', str(binary),
                               '--output-dir', str(output)], capture_output=True,
                              cwd=self.scratch, text=True, timeout=30, check=False)

    def test_public_surface_identity_resource_and_comparator_formats(self):
        dest = self.scratch / 'baseline-evidence'
        run = self.extract(self.binary, dest)
        self.assertEqual(run.returncode, 0, run.stderr)
        ident = json.loads((dest / 'assembly-identities.json').read_text())
        self.assertEqual(ident['schema_version'], 1)
        self.assertEqual(ident['assemblies'][0]['name'], 'Fixture.Library')
        self.assertEqual(ident['assemblies'][0]['version'], '2.3.4.5')
        self.assertEqual(ident['assemblies'][0]['public_key_token'], 'null')
        self.assertEqual(ident['assemblies'][0]['file_version'], '2.3.4.6')
        self.assertIn('2.3.4', ident['assemblies'][0]['informational_version'])
        resources = json.loads((dest / 'resources.json').read_text())
        self.assertIn('Fixture.Messages.resources', resources['assemblies'][0]['resources'])
        lines = (dest / 'public-api.txt').read_text().splitlines()
        self.assertTrue(any('type Fixture.Namespace.Sample`1 ' in x for x in lines))
        self.assertTrue(any('type Fixture.Namespace.Sample`1+Nested' in x for x in lines))
        self.assertTrue(any('method Fixture.Namespace.Sample`1.Echo' in x and 'System.Int32' in x for x in lines))
        self.assertTrue(any('method Fixture.Namespace.Sample`1.Echo' in x and 'System.String' in x for x in lines))
        self.assertTrue(any('method Fixture.Namespace.Sample`1.Process' in x and 'protected_internal' in x for x in lines))
        self.assertTrue(any('property Fixture.Namespace.Sample`1.Value' in x for x in lines))
        self.assertTrue(any('event Fixture.Namespace.Sample`1.Changed' in x for x in lines))
        self.assertTrue(any('field Fixture.Namespace.Sample`1.Number' in x and 'value=42' in x for x in lines))
        self.assertTrue(any('method Fixture.Namespace.Sample`1.WithDefault' in x and 'default=7' in x for x in lines))
        self.assertTrue(any('field Fixture.Namespace.Kind.One' in x and 'value=1' in x for x in lines))
        self.assertFalse(any('Invisible' in x or 'Secret' in x or 'Hidden' in x for x in lines))
        self.assertEqual(lines, sorted(set(lines)))
        sys.path.insert(0, str(SOURCE.parent / 'validators'))
        import compatibility
        self.assertTrue(compatibility.assembly_contract(dest / 'assembly-identities.json', 'assemblies'))
        self.assertTrue(compatibility.assembly_contract(dest / 'resources.json', 'resources'))
        self.assertTrue(compatibility.api_lines(dest / 'public-api.txt'))

    def test_signature_change_detected_and_repeatability(self):
        first = self.scratch / 'compare-original'
        self.assertEqual(self.extract(self.binary, first).returncode, 0)
        self.assertEqual(self.extract(self.binary, self.scratch / 'repeat').returncode, 0)
        self.assertEqual((first / 'public-api.txt').read_bytes(),
                         (self.scratch / 'repeat' / 'public-api.txt').read_bytes())
        source = self.fixture / 'Api.cs'
        before = source.read_text()
        self.assertIn('Echo(int number)', before)
        source.write_text(before.replace('Echo(int number)', 'Echo(double number)'))
        self.build(self.fixture / 'Fixture.csproj')
        second = self.scratch / 'compare-changed'
        self.assertEqual(self.extract(self.binary, second).returncode, 0)
        self.assertNotEqual((first / 'public-api.txt').read_bytes(), (second / 'public-api.txt').read_bytes())
        sys.path.insert(0, str(SOURCE.parent / 'validators'))
        import compatibility
        changes = compatibility.differences(compatibility.api_lines(first / 'public-api.txt'),
                                            compatibility.api_lines(second / 'public-api.txt'))
        self.assertTrue(any('System.Int32' in str(x) for x in changes))
        self.assertTrue(any('System.Double' in str(x) for x in changes))

    def test_public_constant_value_change_is_detected(self):
        baseline = self.scratch / 'constants-before'
        self.assertEqual(self.extract(self.binary, baseline).returncode, 0)
        candidate_fixture = self.scratch / 'fixture-constants-changed'
        shutil.copytree(FIXTURE, candidate_fixture)
        source = candidate_fixture / 'Api.cs'
        source.write_text(source.read_text().replace('public const int Number = 42',
                                                     'public const int Number = 99'))
        self.build(candidate_fixture / 'Fixture.csproj')
        candidate = self.scratch / 'constants-after'
        path = candidate_fixture / 'bin' / 'Release' / 'net10.0' / 'Fixture.Library.dll'
        self.assertEqual(self.extract(path, candidate).returncode, 0)
        before = (baseline / 'public-api.txt').read_text()
        after = (candidate / 'public-api.txt').read_text()
        self.assertIn('value=42', before)
        self.assertIn('value=99', after)
        self.assertNotEqual(before, after)

    def test_external_evidence_root_integrates_with_clean_source_provenance(self):
        artifacts = self.scratch / 'external-capture'
        self.assertEqual(self.extract(self.binary, artifacts).returncode, 0)
        source = self.scratch / 'recorded-checkout'
        source.mkdir()
        (source / 'README.md').write_text('synthetic, source-only attribution test')
        subprocess.run(['git', 'init', '-q', str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(source), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.test', 'commit',
                        '-m', 'fixture', '-q'], check=True)
        sha = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'],
                                      text=True).strip()
        sys.path.insert(0, str(SOURCE.parent / 'validators'))
        import compatibility
        spec = {'schema_version': 1, 'components': {'api': 'public-api.txt',
                'assemblies': 'assembly-identities.json', 'resources': 'resources.json'}}
        baseline = compatibility.capture(source, spec, sha, artifacts_root=artifacts)
        candidate = compatibility.capture(source, spec, sha, artifacts_root=artifacts)
        self.assertFalse(baseline['capture_errors'])
        self.assertEqual(compatibility.compare(baseline, candidate)['overall'], 'matched')
        self.assertEqual(baseline['source']['dirty_paths'], [])

    def test_invalid_binary_and_in_place_output_are_rejected(self):
        wrong = self.scratch / 'not-a-pe.dll'
        wrong.write_bytes(b'not managed assembly')
        p = self.extract(wrong, self.scratch / 'invalid')
        self.assertNotEqual(p.returncode, 0)
        self.assertFalse((self.scratch / 'invalid' / 'public-api.txt').exists())
        same = self.extract(self.binary, self.binary.parent)
        self.assertNotEqual(same.returncode, 0)
        good = self.scratch / 'not-empty'
        good.mkdir()
        (good / 'stale.txt').write_text('stale')
        self.assertNotEqual(self.extract(self.binary, good).returncode, 0)

if __name__ == '__main__':
    unittest.main()
