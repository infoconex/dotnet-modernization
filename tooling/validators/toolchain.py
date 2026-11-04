#!/usr/bin/env python3
"""Read-only, bounded inventory of selected .NET build tools; not a complete host audit."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

SCHEMA_VERSION = 1
COMMAND_TIMEOUT = 20
MAX_OUTPUT = 32768


def probe(argv, cwd):
    """Execute a known, argument-vector tool probe, never a shell command."""
    try:
        proc = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=COMMAND_TIMEOUT,
                              text=True, errors='replace', check=False)
        output = (proc.stdout or '')[:MAX_OUTPUT]
        return {'status': 'ok' if proc.returncode == 0 else 'failed',
                'exit_code': proc.returncode, 'output': output,
                'truncated': len(proc.stdout or '') > MAX_OUTPUT}
    except FileNotFoundError:
        return {'status': 'not_installed'}
    except subprocess.TimeoutExpired:
        return {'status': 'timed_out'}
    except OSError as exc:
        return {'status': 'blocked', 'reason': type(exc).__name__}


def list_sdk_lines(result):
    if result['status'] != 'ok':
        return []
    values = []
    for line in result['output'].splitlines():
        m = re.fullmatch(r'\s*([^\s\[\]]+)\s+\[([^\]\r\n]+)\]\s*', line)
        if m:
            values.append({'version': m.group(1), 'base_path': m.group(2)})
    return values


def list_runtime_lines(result):
    if result['status'] != 'ok':
        return []
    values = []
    for line in result['output'].splitlines():
        m = re.fullmatch(r'\s*(\S+)\s+(\S+)\s+\[([^\]\r\n]+)\]\s*', line)
        if m:
            values.append({'name': m.group(1), 'version': m.group(2), 'path': m.group(3)})
    return values


def dotnet_packs(sdks):
    roots = set()
    for item in sdks:
        base = Path(item['base_path'])
        if base.name.lower() == 'sdk':
            roots.add(base.parent)
    for variable in ('DOTNET_ROOT', 'DOTNET_ROOT_X86'):
        if os.environ.get(variable):
            roots.add(Path(os.environ[variable]))
    found = []
    for root in sorted(roots, key=str):
        packs = root / 'packs'
        if packs.is_dir():
            for package in sorted(packs.iterdir()):
                if package.is_dir():
                    versions = sorted(p.name for p in package.iterdir() if p.is_dir())
                    found.append({'pack': package.name, 'versions': versions, 'root': str(root)})
    return found


def framework_reference_directories():
    if os.name != 'nt':
        return []
    root = os.environ.get('ProgramFiles(x86)')
    if not root:
        return []
    folder = Path(root) / 'Reference Assemblies' / 'Microsoft' / 'Framework' / '.NETFramework'
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if p.is_dir() and p.name.startswith('v'))


def collect(source):
    source = Path(source).resolve(strict=True)
    if not source.is_dir():
        raise ValueError('source must be a directory')
    tools = {}
    dotnet_path = shutil.which('dotnet')
    if dotnet_path:
        dotnet_version = probe([dotnet_path, '--version'], source)
        sdk_result = probe([dotnet_path, '--list-sdks'], source)
        runtime_result = probe([dotnet_path, '--list-runtimes'], source)
        msbuild = probe([dotnet_path, 'msbuild', '-version', '-nologo'], source)
        tools['dotnet'] = {'path': dotnet_path,
                           'selection': {'status': dotnet_version['status'],
                                         'version': dotnet_version.get('output', '').strip() if dotnet_version['status'] == 'ok' else None},
                           'sdks': list_sdk_lines(sdk_result), 'sdk_probe_status': sdk_result['status'],
                           'runtimes': list_runtime_lines(runtime_result), 'runtime_probe_status': runtime_result['status'],
                           'msbuild': {'status': msbuild['status'], 'version_output': msbuild.get('output', '').strip() if msbuild['status'] == 'ok' else None}}
        packs = dotnet_packs(tools['dotnet']['sdks'])
    else:
        tools['dotnet'] = {'status': 'not_installed'}
        packs = []
    for name, cmd in [('msbuild', ['-version', '-nologo']), ('nuget', ['help'])]:
        path = shutil.which(name)
        if path:
            result = probe([path] + cmd, source)
            lines = result.get('output', '').splitlines()
            tools[name] = {'path': path, 'status': result['status'],
                           'banner': '\n'.join(lines[:3])[:512] if result['status'] == 'ok' else None,
                           'truncated': result.get('truncated', False)}
        else:
            tools[name] = {'status': 'not_installed'}
    return {'schema_version': SCHEMA_VERSION, 'kind': 'observed-toolchain-inventory',
            'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
            'host': {'os': platform.platform(), 'architecture': platform.machine(), 'python': platform.python_version()},
            'source_root': str(source), 'tools': tools, 'sdk_targeting_packs': packs,
            'framework_reference_versions': framework_reference_directories(),
            'limitations': [
                'PATH tool probes, dotnet SDK packs and conventional framework reference folders only; not an exhaustive machine inventory.',
                'Tool availability and version do not prove application restore, build, tests or compatibility.',
                'SDK selection is evaluated in the supplied checkout; global.json can cause dotnet --version to fail.',
                'Visual Studio IDE, COM registration, native SDKs, MSBuild extensions and standalone targeting packs outside probed locations are not comprehensively assessed.',
                'Probe commands are not authenticated provenance; image digest and tool installation origin require separate evidence.']}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(argv)
    try:
        source = args.source.resolve(strict=True)
        out = args.output.resolve()
        if out == source or out.is_relative_to(source):
            raise ValueError('output must be outside source checkout')
        report = collect(source)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f'Toolchain inventory: {out}')
        return 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
