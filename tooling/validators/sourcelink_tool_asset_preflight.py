#!/usr/bin/env python3
"""Read-only inventory assertion for pinned .NET Framework Source Link task assets.

No task DLL is loaded, no NuGet packages are installed, and no MSBuild runs.
The assertion establishes only a candidate for isolated build tasks.
"""
import argparse
import json
from pathlib import Path

PINS = {
    ('microsoft.sourcelink.github', '10.0.403'): '9c3252f8cbe1547bf8c12b7c65a7bc28985bab2d598ff97c13e0104c22d80cd5',
    ('microsoft.sourcelink.common', '10.0.403'): 'e99d7aea402042d04faa4971709718ebf256406b4c59f700cb1c8a739859c6a2',
    ('microsoft.build.tasks.git', '10.0.403'): '9d21a711e9fce96b34e8c02f10069bc66a381d84a2912e65a14dc9c411135e29',
    ('system.io.hashing', '10.0.14'): '86917bafb634c4d06dd7f07c5f745141fea220f64e13e7657680e81dac68f941',
}
TASK_NAMES = {
    'microsoft.sourcelink.github': 'Microsoft.SourceLink.GitHub',
    'microsoft.sourcelink.common': 'Microsoft.SourceLink.Common',
    'microsoft.build.tasks.git': 'Microsoft.Build.Tasks.Git',
}
BUNDLED = ('System.Buffers.dll', 'System.Memory.dll', 'System.IO.Hashing.dll')


def evaluate(audit):
    if audit.get('schema_version') != 1 or audit.get('kind') != 'pinned-nuget-archive-build-asset-audit':
        raise ValueError('Unrecognized input audit')
    pkgs = audit.get('packages')
    if not isinstance(pkgs, list) or len(pkgs) != 4:
        raise ValueError('Expected exactly four pinned toolchain packages')
    lookup = {}
    for pkg in pkgs:
        key = (pkg['id'].lower(), pkg['version'])
        if key in lookup or key not in PINS:
            raise ValueError('Duplicate or unexpected package in input inventory')
        if pkg.get('archive_sha256', '').lower() != PINS[key]:
            raise ValueError('Pinned package SHA-256 mismatch')
        lookup[key] = pkg
    if len(lookup) != len(PINS):
        raise ValueError('Missing expected pinned package')
    rows = []
    for key, pkg in sorted(lookup.items()):
        assets = pkg.get('assets')
        if not isinstance(assets, dict):
            raise ValueError('Missing structured archive asset inventory')
        for group in ('tools', 'lib', 'runtimes', 'build', 'buildTransitive'):
            values = assets.get(group)
            if not isinstance(values, list) or any(not isinstance(x, str) for x in values) or len(set(values)) != len(values):
                raise ValueError('Invalid or duplicate asset entries in ' + group)
        imports = pkg.get('msbuild_import_candidates')
        if not isinstance(imports, list):
            raise ValueError('Missing import-candidate inventory')
        name = TASK_NAMES.get(key[0])
        if name:
            required = {f'tools/netframework/{name}.dll'}
            if key[0] in ('microsoft.sourcelink.github', 'microsoft.build.tasks.git'):
                required.update('tools/netframework/' + x for x in BUNDLED)
            absent = required - set(assets['tools'])
            if absent:
                raise ValueError('Missing bundled netframework tool assets: ' + ','.join(sorted(absent)))
            if assets['lib'] or assets['runtimes']:
                raise ValueError('Unexpected runtime/lib assembly assets in build task package')
            if f'build/{name}.targets' not in imports:
                raise ValueError('Missing traditional project .targets import candidate')
            category = 'build-tool-candidate-only'
        else:
            if 'lib/net462/System.IO.Hashing.dll' not in assets['lib']:
                raise ValueError('Missing separate net462 System.IO.Hashing runtime assembly')
            category = 'separate-library-runtime-risk'
        rows.append({'id':pkg['id'],'version':pkg['version'],'archive_sha256':PINS[key],
                     'classification':category, 'tools_entries':len(assets['tools']),
                     'library_entries':len(assets['lib']), 'runtime_entries':len(assets['runtimes'])})
    return {'schema_version':1,'result':'BUILD_TOOL_ASSET_PRESENCE_VERIFIED_NOT_RUNTIME_ISOLATION',
            'packages':rows,
            'not_proven':['Actual MSBuild process module load paths','Effect of NuGet packages.config installation on application references',
                          'Runtime output or consumer package safety','Correct Source Link PDB/source hash mapping']}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--audit',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    if a.output.exists():
        p.error('Refusing to overwrite existing evidence')
    try:
        result=evaluate(json.loads(a.audit.read_text(encoding='utf-8')))
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    except (OSError,ValueError,TypeError,KeyError) as ex:
        p.exit(2,'Preflight failed closed: '+str(ex)+'\n')
    print(result['result'])


if __name__=='__main__':
    main()
