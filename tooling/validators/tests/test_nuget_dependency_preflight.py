"""Synthetic stdlib tests for the read-only NuGet dependency preflight."""
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from nuget_dependency_preflight import preflight, version_range_contains, framework_tuple


def archive(dest, name, ver, groups):
    entries = ''
    for framework, deps in groups:
        label = (' targetFramework="' + framework + '"') if framework else ''
        entries += '<group' + label + '>'
        for dependency, minimum in deps:
            entries += '<dependency id="' + dependency + '" version="' + escape(minimum, {'"': '&quot;'}) + '" />'
        entries += '</group>'
    raw = f'<package><metadata><id>{name}</id><version>{ver}</version><dependencies>{entries}</dependencies></metadata></package>'
    with zipfile.ZipFile(dest, 'w') as z:
        z.writestr(name+'.nuspec', raw)


class Checks(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.dir = pathlib.Path(self.t.name)
        self.cfg = self.dir/'packages.config'
        self.cfg.write_text('<packages><package id="System.Buffers" version="4.5.1" targetFramework="net48" />'
                            '<package id="System.Memory" version="4.5.5" targetFramework="net48" /></packages>')

    def run_packages(self, specs):
        selected = []
        for n, v, groups in specs:
            p = self.dir / (n + '.' + v + '.nupkg')
            archive(p, n, v, groups)
            selected.append({'id': n, 'version': v, 'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()})
        m = self.dir/'manifest.json'
        m.write_text(json.dumps({'packages': selected}))
        return preflight(self.cfg, m)

    def test_detects_two_existing_application_version_conflicts(self):
        r = self.run_packages([
            ('Microsoft.SourceLink.GitHub', '10.0.403', [('net472', [('System.IO.Hashing','10.0.14')])]),
            ('System.IO.Hashing','10.0.14',[('net462',[('System.Buffers','4.6.1'),('System.Memory','4.6.3')]),
                                             ('net8.0',[])])])
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertEqual({i['dependency'] for i in r['conflicts']}, {'System.Buffers','System.Memory'})
        self.assertEqual(len(r['unresolved_dependencies']),0)
        self.assertEqual(next(p['dependency_group'] for p in r['tool_packages'] if p['id']=='System.IO.Hashing'),'net462')

    def test_modeled_four_package_provider_chain_still_conflicts(self):
        r = self.run_packages([
            ('Microsoft.SourceLink.GitHub', '10.0.403', [('net472', [
                ('Microsoft.Build.Tasks.Git','10.0.403'),
                ('Microsoft.SourceLink.Common','10.0.403'),
                ('System.IO.Hashing','10.0.14')])]),
            ('Microsoft.Build.Tasks.Git','10.0.403',[('net472',[('System.IO.Hashing','10.0.14')])]),
            ('Microsoft.SourceLink.Common','10.0.403',[('net472',[])]),
            ('System.IO.Hashing','10.0.14',[('net462',[
                ('System.Buffers','4.6.1'),('System.Memory','4.6.3')]),('net10.0',[])])
        ])
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertEqual({x['dependency'] for x in r['conflicts']}, {'System.Buffers','System.Memory'})
        self.assertEqual(len(r['unresolved_dependencies']), 0)
        self.assertEqual(len(r['dependency_edges']), 6)

    def test_compatible_is_only_metadata_pass(self):
        r = self.run_packages([('Tool','1.2.3',[('net472',[('System.Buffers','[4.5.1,5.0.0)')])])])
        self.assertEqual(r['status'], 'PASS_METADATA_ONLY')

    def test_unresolved_dependency_not_a_closed_graph(self):
        r = self.run_packages([('Tool','1.2.3',[('net472',[('Missing.Tool','1.0.0')])])])
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertEqual(r['unresolved_dependencies'][0]['dependency'], 'Missing.Tool')

    def test_tool_package_overlap_blocks(self):
        r = self.run_packages([('System.Buffers','4.6.1',[('net462',[])])])
        self.assertEqual(r['status'], 'BLOCKED')
        self.assertEqual(len(r['baseline_version_overlaps']),1)

    def test_nearest_compatible_framework_selected(self):
        r = self.run_packages([('Tool','1.2.3',[('net462',[('System.Buffers','4.5.1')]),
                                                    ('net472',[('System.Memory','4.5.5')]),
                                                    ('net8.0',[('Missing','10.0')])])])
        self.assertEqual(r['status'], 'PASS_METADATA_ONLY')
        self.assertEqual(r['dependency_edges'][0]['dependency'], 'System.Memory')

    def test_no_compatible_group_fails_closed(self):
        with self.assertRaises(ValueError):
            self.run_packages([('Tool','1.2.3',[('net8.0',[])])])

    def test_archive_mismatch_fails_closed(self):
        p = self.dir/'tool.nupkg'
        archive(p, 'Tool', '1.0.0', [('net472', [])])
        m = self.dir/'manifest.json'
        m.write_text(json.dumps({'packages':[{'id':'Tool','version':'1.0.0','path':str(p),
                                              'sha256': '0'*64}]}))
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            preflight(self.cfg, m)

    def test_exact_and_ranges(self):
        self.assertTrue(version_range_contains('[4.6.1]', '4.6.1'))
        self.assertFalse(version_range_contains('[4.6.1]', '4.6.2'))
        self.assertTrue(version_range_contains('[4.6.1,)', '4.6.2'))
        self.assertFalse(version_range_contains('(4.6.1,)', '4.6.1'))
        self.assertFalse(version_range_contains('[4.6.1,5.0.0)', '5.0.0'))

    def test_duplicate_dependencies_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate declared dependency'):
            self.run_packages([('Tool','1.0.0',[('net472',[('System.Memory','4.0.0'),
                ('system.memory','4.1.0')])])])

    def test_duplicate_equivalent_framework_groups_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Ambiguous duplicate compatible framework'):
            self.run_packages([('Tool','1.0.0',[('net472',[]),('.NETFramework4.7.2',[])])])

    def test_mixed_dependency_groups_rejected(self):
        p = self.dir/'tool.nupkg'
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('Tool.nuspec', '<package><metadata><id>Tool</id><version>1.0.0</version>'
                       '<dependencies><group targetFramework="net472"/>'
                       '<dependency id="System.Memory" version="4.5.5"/>'
                       '</dependencies></metadata></package>')
        m = self.dir/'manifest.json'
        m.write_text(json.dumps({'packages':[{'id':'Tool','version':'1.0.0',
            'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}))
        with self.assertRaisesRegex(ValueError, 'Mixed grouped and ungrouped'):
            preflight(self.cfg, m)

    def test_multiple_dependencies_sections_rejected(self):
        p = self.dir/'tool.nupkg'
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('Tool.nuspec', '<package><metadata><id>Tool</id><version>1.0.0</version>'
                       '<dependencies><group targetFramework="net472"/></dependencies>'
                       '<dependencies><group targetFramework="net472"/></dependencies>'
                       '</metadata></package>')
        m = self.dir/'manifest.json'
        m.write_text(json.dumps({'packages':[{'id':'Tool','version':'1.0.0',
            'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}))
        with self.assertRaisesRegex(ValueError, 'Multiple dependencies'):
            preflight(self.cfg, m)

    def test_net_framework_not_net8(self):
        self.assertEqual(framework_tuple('net48'), (4,8,0))
        self.assertEqual(framework_tuple('.NETFramework4.7.2'), (4,7,2))
        self.assertIsNone(framework_tuple('net8.0'))


if __name__ == '__main__':
    unittest.main()
