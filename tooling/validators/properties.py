#!/usr/bin/env python3
"""Capture evaluated MSBuild properties (not a build, API check or import graph)."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from provenance import snapshot, require_commit

SCHEMA_VERSION = 1
MAX_OUTPUT = 4096
PROPERTY_NAME = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
SENSITIVE = re.compile(r'password|secret|credential|connection.?string|access.?token|api.?key|private.?key', re.I)
PROJECT_TYPES = {'.csproj', '.vbproj', '.fsproj', '.vcxproj', '.wixproj', '.sqlproj'}
CONTEXT_KEYS = {'Configuration', 'Platform', 'TargetFramework', 'RuntimeIdentifier'}


def guard_name(name):
    if not isinstance(name, str) or not PROPERTY_NAME.fullmatch(name) or SENSITIVE.search(name):
        raise ValueError('invalid or potentially sensitive MSBuild property name')
    return name


def parse_matrix(matrix):
    if not isinstance(matrix, dict) or matrix.get('schema_version') != SCHEMA_VERSION:
        raise ValueError('matrix requires schema_version: 1')
    props = matrix.get('properties')
    if not isinstance(props, list) or not props or len(props) > 60:
        raise ValueError('matrix needs 1..60 property names')
    for name in props:
        guard_name(name)
    if len(set(props)) != len(props):
        raise ValueError('duplicate requested property name')
    contexts = matrix.get('contexts', [{}])
    if not isinstance(contexts, list) or not contexts or len(contexts) > 36:
        raise ValueError('matrix requires 1..36 contexts')
    for context in contexts:
        if not isinstance(context, dict) or not set(context).issubset(CONTEXT_KEYS):
            raise ValueError('unsupported MSBuild context; supported: Configuration, Platform, TargetFramework, RuntimeIdentifier')
        for key, value in context.items():
            if not isinstance(value, str) or not value or len(value) > 120 or re.search(r'[;\r\n%"\x00]', value):
                raise ValueError(f'unsafe context value for {key}')
    return props, contexts


def within(root, raw):
    if not isinstance(raw, str) or not raw:
        raise ValueError('project path must be nonempty')
    candidate = (root / raw).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file() or candidate.suffix.lower() not in PROJECT_TYPES:
        raise ValueError('project must be an MSBuild project file within checkout')
    return candidate


def evaluate(source, projects, matrix, engine, timeout=30):
    source = Path(source).resolve(strict=True)
    if not source.is_dir():
        raise ValueError('source must be a directory')
    props, contexts = parse_matrix(matrix)
    if not isinstance(engine, list) or not engine or not all(isinstance(x, str) and x for x in engine):
        raise ValueError('engine must be a reviewed argv prefix')
    if timeout < 1 or timeout > 300:
        raise ValueError('timeout must be 1..300 seconds')
    paths = [within(source, path) for path in projects]
    report = {'schema_version': SCHEMA_VERSION, 'kind': 'evaluated-msbuild-properties',
              'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'source_root': str(source), 'source': snapshot(source), 'engine_argv': engine, 'projects': [],
              'limitations': [
                  'Property values come from MSBuild project evaluation with the supplied context; no build target is invoked.',
                  'MSBuild imports, SDK resolvers and project evaluation can execute host-specific code; use trusted disposable checkouts.',
                  'Empty output cannot distinguish an unset property from an explicitly empty one.',
                  'Not a complete import graph; compare source XML and use a separate /pp investigation when required.',
                  'A successful property query does not prove Debug/Release build, API, tests, packages or consumer parity.']}
    for path in paths:
        item = {'path': path.relative_to(source).as_posix(), 'contexts': []}
        report['projects'].append(item)
        for context in contexts:
            ctx = {'settings': context, 'properties': {}}
            item['contexts'].append(ctx)
            for prop in props:
                argv = engine + [str(path), '-nologo', '-verbosity:quiet', '-getProperty:' + prop] + [
                    '-property:' + k + '=' + v for k, v in sorted(context.items())]
                try:
                    run = subprocess.run(argv, cwd=source, capture_output=True, text=True,
                                         errors='replace', timeout=timeout, check=False)
                    if run.returncode == 0 and len(run.stdout) <= MAX_OUTPUT:
                        value = run.stdout.strip()
                        ctx['properties'][prop] = {'status': 'empty_or_undefined' if not value else 'evaluated',
                                                   'value': value}
                    else:
                        codes = sorted(set(re.findall(r'\bMSB\d{4}\b', run.stderr or '')))
                        ctx['properties'][prop] = {'status': 'failed', 'exit_code': run.returncode,
                                                   'error_codes': codes, 'output_truncated': len(run.stdout) > MAX_OUTPUT}
                except subprocess.TimeoutExpired:
                    ctx['properties'][prop] = {'status': 'timed_out'}
                except OSError:
                    ctx['properties'][prop] = {'status': 'blocked'}
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--project', required=True, action='append', help='Relative project path; repeat for multiple')
    parser.add_argument('--matrix', required=True, type=Path, help='Reviewed JSON property names and contexts')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--engine', choices=('dotnet', 'msbuild'), default='dotnet')
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--expect-commit', help='Require an exact 40-character Git SHA')
    args = parser.parse_args(argv)
    try:
        src = args.source.resolve(strict=True)
        out = args.output.resolve()
        if out == src or out.is_relative_to(src):
            raise ValueError('output must be outside application checkout')
        require_commit(snapshot(src)['commit'], args.expect_commit)
        executable = shutil.which(args.engine)
        if executable is None:
            raise ValueError(f'{args.engine} unavailable on PATH')
        command = [executable, 'msbuild'] if args.engine == 'dotnet' else [executable]
        matrix = json.loads(args.matrix.read_text(encoding='utf-8'))
        result = evaluate(src, args.project, matrix, command, args.timeout)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        bad = sum(p['status'] in ('failed', 'timed_out', 'blocked') for project in result['projects']
                  for context in project['contexts'] for p in context['properties'].values())
        print(f'MSBuild property queries: {out} | failed/blocked={bad}')
        return 1 if bad else 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'ERROR: {type(exc).__name__}: {str(exc)[:200]}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
