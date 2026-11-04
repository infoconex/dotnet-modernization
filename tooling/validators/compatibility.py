#!/usr/bin/env python3
"""Capture and compare scoped .NET compatibility evidence, without building an application."""
import argparse
from collections import Counter
import hashlib
import datetime as dt
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

from provenance import require_commit, snapshot

VERSION = 1
MAX_INPUT = 16 * 1024 * 1024
MAX_ZIP_ENTRIES = 10000
MAX_NUSPEC = 2 * 1024 * 1024
MAX_DIFF = 100
COMPONENTS = ('api', 'assemblies', 'resources', 'packages', 'tests')
IDENTITY = ('name', 'version', 'culture', 'public_key_token', 'file_version', 'informational_version')


def load_json(path):
    if path.stat().st_size > MAX_INPUT:
        raise ValueError('input exceeds 16 MiB')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def relative_file(root, raw):
    if not isinstance(raw, str) or not raw:
        raise ValueError('evidence filename must be a nonempty relative path')
    path = (root / raw).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('evidence file must exist inside the source checkout')
    if path.stat().st_size > MAX_INPUT:
        raise ValueError('input exceeds 16 MiB')
    return path


def named_paths(root, items, kind):
    if not isinstance(items, list) or not items:
        raise ValueError(kind + ' requires a nonempty list')
    names = set()
    values = []
    for item in items:
        if not isinstance(item, dict) or set(item) != {'id', 'path'}:
            raise ValueError(kind + ' entries require id and path')
        ident = item['id']
        if not isinstance(ident, str) or not ident or '/' in ident or '\\' in ident:
            raise ValueError('invalid evidence item id')
        if ident in names:
            raise ValueError('duplicate evidence item id')
        names.add(ident)
        values.append((ident, relative_file(root, item['path'])))
    return values


def input_fingerprint(root, path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return {'path': path.relative_to(root).as_posix(), 'sha256': digest.hexdigest()}


def api_lines(path):
    lines = [x.strip() for x in path.read_text(encoding='utf-8-sig').splitlines()
             if x.strip() and not x.lstrip().startswith('#')]
    if len(lines) != len(set(lines)):
        raise ValueError('duplicate public API/metadata records')
    return sorted(lines)


def assembly_contract(path, category):
    raw = load_json(path)
    if not isinstance(raw, dict) or raw.get('schema_version') != VERSION or not isinstance(raw.get('assemblies'), list):
        raise ValueError('assembly/resource manifest requires schema_version 1 and assemblies list')
    result = {}
    for assembly in raw['assemblies']:
        if not isinstance(assembly, dict) or not isinstance(assembly.get('name'), str) or not assembly['name']:
            raise ValueError('assembly manifest entry lacks name')
        name = assembly['name']
        if name in result:
            raise ValueError('duplicate assembly name')
        if category == 'assemblies':
            if any(key not in IDENTITY for key in assembly):
                raise ValueError('unknown identity field')
            if not isinstance(assembly.get('version'), str) or not assembly['version']:
                raise ValueError('assembly identity requires a version')
            if any(not isinstance(val, str) for val in assembly.values()):
                raise ValueError('assembly identity must contain strings')
            result[name] = {k: assembly[k] for k in IDENTITY if k in assembly}
        else:
            resources = assembly.get('resources')
            if set(assembly) != {'name', 'resources'} or not isinstance(resources, list):
                raise ValueError('resource manifest requires name/resources')
            if not all(isinstance(r, str) and r for r in resources) or len(resources) != len(set(resources)):
                raise ValueError('resource names must be nonempty and unique')
            result[name] = sorted(resources)
    if not result:
        raise ValueError('assembly/resource manifest must not be empty')
    return result


def xml_tag(element):
    return element.tag.rsplit('}', 1)[-1]


def nuspec_contract(data):
    root = ET.fromstring(data)
    if xml_tag(root) != 'package':
        raise ValueError('NuGet manifest must contain package root')
    metadata = next((e for e in root if xml_tag(e) == 'metadata'), None)
    if metadata is None:
        raise ValueError('NuGet metadata missing')
    def field(name):
        return next(((e.text or '').strip() for e in metadata if xml_tag(e) == name), None)
    ident, version = field('id'), field('version')
    if not ident or not version:
        raise ValueError('NuGet id/version missing')
    dependencies = []
    for deps in metadata:
        if xml_tag(deps) != 'dependencies':
            continue
        for dep in deps.iter():
            if xml_tag(dep) != 'dependency':
                continue
            group = None
            # Parent groups are the only meaningful enclosing dependency condition here.
            for part in deps:
                if dep in list(part) and xml_tag(part) == 'group':
                    group = part.get('targetFramework')
                    break
            dependencies.append({'id': dep.get('id'), 'version': dep.get('version'),
                                 'target_framework': group, 'include': dep.get('include'),
                                 'exclude': dep.get('exclude')})
    if any(not d['id'] or not d['version'] for d in dependencies):
        raise ValueError('NuGet dependency lacks id or version')
    return {'id': ident, 'version': version,
            'dependencies': sorted(dependencies, key=lambda x: (
                x['target_framework'] or '', x['id'].lower(), x['version']))}


def package_contract(path):
    try:
        with zipfile.ZipFile(path) as archive:
            files = archive.infolist()
            if len(files) > MAX_ZIP_ENTRIES:
                raise ValueError('package has too many ZIP entries')
            paths = [f.filename.replace('\\', '/') for f in files if not f.is_dir()]
            if len(paths) != len(set(paths)):
                raise ValueError('duplicate package ZIP entry names')
            if any(p.startswith('/') or p.startswith('../') or
                   any(x in ('', '.', '..') for x in p.split('/')) or ':' in p.split('/')[0]
                   for p in paths):
                raise ValueError('unsafe package archive path')
            manifests = [p for p in paths if '/' not in p and p.lower().endswith('.nuspec')]
            if len(manifests) != 1:
                raise ValueError('package must contain exactly one root nuspec')
            info = archive.getinfo(manifests[0])
            if info.file_size > MAX_NUSPEC:
                raise ValueError('oversized NuGet manifest')
            manifest = nuspec_contract(archive.read(manifests[0]))
            # Generated OPC relationship/signature/core-property entries are not behavioral payload.
            payload = sorted(p for p in paths if p != manifests[0] and not (
                p.startswith('_rels/') or p.startswith('package/services/metadata/core-properties/') or
                p in ('[Content_Types].xml', '.signature.p7s')))
            return {**manifest, 'payload_paths': payload,
                    'payload_policy': 'paths-only; timestamps and file bytes excluded'}
    except (zipfile.BadZipFile, RuntimeError) as exc:
        raise ValueError('unreadable nupkg') from exc


def tests_contract(path):
    root = ET.parse(path).getroot()
    if xml_tag(root) != 'test-run':
        raise ValueError('NUnit 3 requires test-run root')
    counts = {}
    for key in ('total', 'passed', 'failed', 'skipped', 'inconclusive'):
        value = root.attrib.get(key, '0' if key == 'inconclusive' else None)
        if value is None:
            raise ValueError('NUnit test-run is missing ' + key)
        counts[key] = int(value)
        if counts[key] < 0:
            raise ValueError('NUnit counts must be nonnegative')
    cases = {}
    for item in root.iter():
        if xml_tag(item) != 'test-case':
            continue
        name, result = item.get('fullname'), item.get('result')
        if not name or not result or name in cases:
            raise ValueError('NUnit case requires unique fullname and result')
        cases[name] = {'result': result, 'label': item.get('label')}
    if len(cases) != counts['total'] or sum(counts[k] for k in ('passed', 'failed', 'skipped', 'inconclusive')) != counts['total']:
        raise ValueError('NUnit totals are inconsistent or test-case evidence incomplete')
    observed = {k: 0 for k in ('passed', 'failed', 'skipped', 'inconclusive')}
    for case in cases.values():
        outcome = case['result'].lower()
        if outcome not in observed:
            raise ValueError('unsupported NUnit case result: ' + outcome)
        observed[outcome] += 1
    if any(counts[k] != observed[k] for k in observed):
        raise ValueError('NUnit test-case outcomes do not match run totals')
    return {'counts': counts, 'cases': dict(sorted(cases.items()))}


def capture(source, specification, expected_commit=None):
    source = Path(source).resolve(strict=True)
    if not source.is_dir():
        raise ValueError('source must be a directory')
    if not isinstance(specification, dict) or specification.get('schema_version') != VERSION:
        raise ValueError('specification requires schema_version 1')
    comps = specification.get('components')
    if not isinstance(comps, dict) or not comps or set(comps) - set(COMPONENTS):
        raise ValueError('specification needs supported components')
    provenance = snapshot(source)
    require_commit(provenance['commit'], expected_commit)
    report = {'schema_version': VERSION, 'kind': 'compatibility-snapshot',
              'captured_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'source': provenance, 'components': {}, 'capture_errors': [],
              'limitations': [
                  'Inputs must be generated by separate, trusted build/validation commands; this collector does not build or inspect DLL metadata.',
                  'API/assembly/resource manifests are caller-generated contracts, not independently verified CLR reflection.',
                  'NuGet packages compare logical metadata and entry paths, not byte hashes, signatures or installed-consumer behavior.',
                  'NUnit comparison detects reported test identity/outcome changes but not runtime behavior beyond those results.']}
    for component, inputs in comps.items():
        try:
            if component in ('api', 'assemblies', 'resources'):
                path = relative_file(source, inputs)
                data = (api_lines(path) if component == 'api' else assembly_contract(path, component))
                artifacts = [input_fingerprint(source, path)]
            else:
                paths = named_paths(source, inputs, component)
                data = {k: (package_contract(v) if component == 'packages' else tests_contract(v))
                        for k, v in paths}
                artifacts = [dict(id=k, **input_fingerprint(source, v)) for k, v in paths]
            if not data:
                raise ValueError('requested evidence is empty')
            report['components'][component] = {'status': 'captured', 'data': data,
                                               'input_artifacts': artifacts}
        except (OSError, ValueError, KeyError, TypeError, ET.ParseError, UnicodeError,
                json.JSONDecodeError, zipfile.LargeZipFile) as exc:
            report['components'][component] = {'status': 'error'}
            report['capture_errors'].append({'component': component, 'problem': type(exc).__name__,
                                             'detail': str(exc)[:200]})
    return report


def differences(before, after):
    """Structured deterministic recursive changes, bounded for readable reports."""
    found = []
    def walk(left, right, path):
        if len(found) > MAX_DIFF:
            return
        if isinstance(left, dict) and isinstance(right, dict):
            for key in sorted(set(left) | set(right)):
                if key not in left:
                    found.append({'path': path + '/' + key, 'change': 'added', 'candidate': right[key]})
                elif key not in right:
                    found.append({'path': path + '/' + key, 'change': 'removed', 'baseline': left[key]})
                else:
                    walk(left[key], right[key], path + '/' + key)
                if len(found) > MAX_DIFF:
                    return
        elif isinstance(left, list) and isinstance(right, list):
            old = Counter(json.dumps(x, sort_keys=True) for x in left)
            new = Counter(json.dumps(x, sort_keys=True) for x in right)
            for v in sorted(old.keys() | new.keys()):
                if old[v] > new[v]:
                    found.append({'path': path, 'change': 'removed',
                                  'baseline': json.loads(v), 'count': old[v] - new[v]})
                elif new[v] > old[v]:
                    found.append({'path': path, 'change': 'added',
                                  'candidate': json.loads(v), 'count': new[v] - old[v]})
                if len(found) > MAX_DIFF: return
        elif left != right:
            found.append({'path': path, 'change': 'changed', 'baseline': left, 'candidate': right})
    walk(before, after, '')
    return found


def compare(baseline, candidate):
    for label, obj in (('baseline', baseline), ('candidate', candidate)):
        if not isinstance(obj, dict) or obj.get('schema_version') != VERSION or obj.get('kind') != 'compatibility-snapshot':
            raise ValueError(label + ' must be a compatibility snapshot schema v1')
    a, b = baseline.get('components', {}), candidate.get('components', {})
    if not isinstance(a, dict) or not isinstance(b, dict):
        raise ValueError('snapshot components must be objects')
    if any(not isinstance(v, dict) or v.get('status') not in ('captured', 'error') or
           (v.get('status') == 'captured' and 'data' not in v)
           for v in list(a.values()) + list(b.values())):
        raise ValueError('snapshot component lacks required status/data')
    names = sorted(set(a) | set(b))
    if not names or set(names) - set(COMPONENTS):
        raise ValueError('no comparable recognized components')
    report = {'schema_version': VERSION, 'kind': 'compatibility-comparison',
              'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'baseline_source': baseline.get('source'), 'candidate_source': candidate.get('source'),
              'components': {}, 'overall': 'incomplete'}
    for name in names:
        if name not in a or name not in b or a[name].get('status') != 'captured' or b[name].get('status') != 'captured':
            report['components'][name] = {'status': 'missing_evidence'}
            continue
        left, right = a[name]['data'], b[name]['data']
        changed = left != right
        diff = differences(left, right) if changed else []
        report['components'][name] = {'status': 'changed' if changed else 'matched',
                                       'differences': diff[:MAX_DIFF],
                                       'diff_truncated': len(diff) > MAX_DIFF,
                                       'baseline_input_artifacts': a[name].get('input_artifacts'),
                                       'candidate_input_artifacts': b[name].get('input_artifacts')}
    statuses = [v['status'] for v in report['components'].values()]
    sources = [baseline.get('source') or {}, candidate.get('source') or {}]
    if not all(isinstance(x, dict) for x in sources):
        raise ValueError('invalid source provenance')
    verified = all(isinstance(x.get('commit'), str) and len(x['commit']) == 40
                   and x.get('dirty_paths') == [] for x in sources)
    report['provenance'] = 'clean_committed' if verified else 'unverified_or_dirty'
    if 'missing_evidence' in statuses:
        report['overall'] = 'incomplete'
    elif 'changed' in statuses:
        report['overall'] = 'changes_detected'
    else:
        report['overall'] = 'matched' if verified else 'matched_unverified_provenance'
    report['limitations'] = [
        'Matched means only the explicitly requested evidence contracts matched, not a certified modernization or a package security clearance.',
        'Skipped/unrequested contracts and test execution coverage require separate decisions and gates.',
        'Full API manifests, assembly identity and embedded-resource extraction must be provided by trusted application tooling.',
        'File payload changes inside an unchanged NuGet package path are not detected by this logical package comparison.']
    return report


def write_report(path, report, protected_roots=()):
    path = Path(path).resolve()
    if any(path == root or path.is_relative_to(root) for root in protected_roots):
        raise ValueError('output must be outside source checkout')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + '\n', encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    a = sub.add_parser('capture')
    a.add_argument('--source', type=Path, required=True)
    a.add_argument('--spec', type=Path, required=True)
    a.add_argument('--output', type=Path, required=True)
    a.add_argument('--expect-commit')
    b = sub.add_parser('compare')
    b.add_argument('--baseline', type=Path, required=True)
    b.add_argument('--candidate', type=Path, required=True)
    b.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == 'capture':
            source = args.source.resolve(strict=True)
            if args.output.resolve() == source or args.output.resolve().is_relative_to(source):
                raise ValueError('output must be outside source checkout')
            report = capture(source, load_json(args.spec), args.expect_commit)
            write_report(args.output, report, [source])
            print('Snapshot: ' + ', '.join(f'{k}={v["status"]}' for k, v in report['components'].items()))
            return 1 if report['capture_errors'] else 0
        baseline, candidate = load_json(args.baseline), load_json(args.candidate)
        if args.output.resolve() in (args.baseline.resolve(), args.candidate.resolve()):
            raise ValueError('comparison output cannot overwrite a source snapshot')
        report = compare(baseline, candidate)
        write_report(args.output, report)
        print('Compatibility comparison: ' + report['overall'])
        return 0 if report['overall'] == 'matched' else 1
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(f'ERROR: {type(exc).__name__}: {str(exc)[:200]}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
