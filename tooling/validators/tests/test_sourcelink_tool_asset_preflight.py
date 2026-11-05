"""Synthetic negative controls: metadata inspection only, no package execution."""
import copy
import pathlib
import sys
import unittest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from sourcelink_tool_asset_preflight import PINS, evaluate


def template():
    pkg_names={'microsoft.sourcelink.github':'Microsoft.SourceLink.GitHub',
      'microsoft.sourcelink.common':'Microsoft.SourceLink.Common',
      'microsoft.build.tasks.git':'Microsoft.Build.Tasks.Git','system.io.hashing':'System.IO.Hashing'}
    result=[]
    for (key,version), digest in PINS.items():
        name=pkg_names[key]
        task=key!='system.io.hashing'
        dlls=[f'tools/netframework/{name}.dll'] if task else []
        if key in ('microsoft.sourcelink.github','microsoft.build.tasks.git'):
            dlls.extend('tools/netframework/'+x for x in ('System.Buffers.dll','System.Memory.dll','System.IO.Hashing.dll'))
        result.append({'id':name,'version':version,'archive_sha256':digest,
          'assets':{'tools':dlls,'lib':[] if task else ['lib/net462/System.IO.Hashing.dll'],
                    'runtimes':[],'build':[],'buildTransitive':[]},
          'msbuild_import_candidates':[f'build/{name}.targets'] if task else []})
    return {'schema_version':1,'kind':'pinned-nuget-archive-build-asset-audit','packages':result}


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.data=template()

    def entry(self,name):
        return next(p for p in self.data['packages'] if p['id']==name)

    def expect_rejected(self):
        with self.assertRaises(ValueError):evaluate(self.data)

    def test_positive_only_proves_presence(self):
        r=evaluate(self.data)
        self.assertEqual(r['result'],'BUILD_TOOL_ASSET_PRESENCE_VERIFIED_NOT_RUNTIME_ISOLATION')
        self.assertTrue(r['not_proven'])

    def test_missing_memory_rejected(self):
        self.entry('Microsoft.SourceLink.GitHub')['assets']['tools'].remove('tools/netframework/System.Memory.dll')
        self.expect_rejected()

    def test_missing_task_assembly_rejected(self):
        self.entry('Microsoft.Build.Tasks.Git')['assets']['tools'].remove('tools/netframework/Microsoft.Build.Tasks.Git.dll')
        self.expect_rejected()

    def test_missing_common_target_rejected(self):
        self.entry('Microsoft.SourceLink.Common')['msbuild_import_candidates'].clear()
        self.expect_rejected()

    def test_runtime_lib_in_task_rejected(self):
        self.entry('Microsoft.SourceLink.Common')['assets']['lib'].append('lib/net48/Injected.dll')
        self.expect_rejected()

    def test_missing_hashing_lib_rejected(self):
        self.entry('System.IO.Hashing')['assets']['lib'].clear()
        self.expect_rejected()

    def test_wrong_package_sha_rejected(self):
        self.entry('System.IO.Hashing')['archive_sha256']='0'*64
        self.expect_rejected()

    def test_duplicate_packages_rejected(self):
        self.data['packages'][-1]=copy.deepcopy(self.data['packages'][0])
        self.expect_rejected()

    def test_unexpected_package_rejected(self):
        self.data['packages'][0]['id']='Different.Package'
        self.expect_rejected()

    def test_bad_schema_rejected(self):
        self.data['schema_version']=2
        self.expect_rejected()


if __name__=='__main__':
    unittest.main()
