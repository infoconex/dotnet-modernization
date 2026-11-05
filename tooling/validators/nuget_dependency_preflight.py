#!/usr/bin/env python3
"""Read-only NuGet archive dependency preflight for traditional .NET Framework projects.

This is conservative metadata analysis, NOT NuGet resolution, target execution,
application build, PDB verification, or proof of MSBuild-host isolation.
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")
NUMERIC = re.compile(r"^\d+(?:\.\d+){1,3}$")
NETFX = re.compile(r"^(?:\.netframework|net)(\d+)(?:\.(\d+))?(?:\.(\d+))?$", re.I)
MAX_ARCHIVE = 96 * 1024 * 1024
MAX_NUSPEC = 1024 * 1024


def strip_ns(tag):
    return tag.split('}', 1)[-1]


def numeric_version(value):
    if not NUMERIC.fullmatch(value):
        raise ValueError('Unrecognized NuGet version (fail-closed): ' + value)
    numbers = tuple(map(int, value.split('.')))
    return numbers + (0,) * (4 - len(numbers))


def version_range_contains(spec, value):
    """Accept only common exact, minimum and numeric bounded NuGet ranges."""
    actual = numeric_version(value)
    s = spec.strip()
    if not s:
        raise ValueError('Missing dependency version range')
    if s[0] not in '([':
        return actual >= numeric_version(s)
    if s[-1] not in ')]':
        raise ValueError('Malformed NuGet dependency range: ' + s)
    if ',' not in s:
        if s[0] != '[' or s[-1] != ']':
            raise ValueError('Malformed exact dependency range: ' + s)
        return actual == numeric_version(s[1:-1])
    left, right = (v.strip() for v in s[1:-1].split(',', 1))
    if not left and not right:
        raise ValueError('Unbounded dependency range is not a reproducible pin')
    if left:
        lower = numeric_version(left)
        if actual < lower or (actual == lower and s[0] == '('):
            return False
    if right:
        upper = numeric_version(right)
        if actual > upper or (actual == upper and s[-1] == ')'):
            return False
    return True


def framework_tuple(text):
    s = text.strip().lower().replace(' ', '')
    if not s:
        return None
    m = NETFX.match(s)
    if not m:
        return None
    if s.startswith('.netframework'):
        bits = [int(n) for n in m.groups() if n is not None]
        return tuple((bits + [0, 0])[:3])
    compact = m.group(1)
    if m.group(2) is None and len(compact) in (2, 3) and compact.startswith('4'):
        return (int(compact[0]), int(compact[1]), int(compact[2:]) if len(compact) == 3 else 0)
    if compact == '4' and m.group(2) is not None:
        return (4, int(m.group(2)), int(m.group(3) or 0))
    return None


def parse_packages_config(path):
    root = ET.parse(path).getroot()
    if strip_ns(root.tag) != 'packages':
        raise ValueError('Expected packages.config <packages> root')
    out = {}
    for p in root:
        if strip_ns(p.tag) != 'package':
            raise ValueError('Unknown packages.config element')
        id_, ver = p.get('id', ''), p.get('version', '')
        if not ID.fullmatch(id_):
            raise ValueError('Invalid application package ID')
        numeric_version(ver)
        key = id_.lower()
        if key in out:
            raise ValueError('Duplicate application package ID')
        out[key] = {'id': id_, 'version': ver, 'targetFramework': p.get('targetFramework')}
    return out


def select_dependencies(metadata, target):
    deps_nodes = [node for node in metadata if strip_ns(node.tag) == 'dependencies']
    if len(deps_nodes) > 1:
        raise ValueError('Multiple dependencies declarations are ambiguous')
    deps_parent = deps_nodes[0] if deps_nodes else None
    if deps_parent is None:
        return [], 'no dependencies'
    groups = [g for g in deps_parent if strip_ns(g.tag) == 'group']
    if groups and len(groups) != len(list(deps_parent)):
        raise ValueError('Mixed grouped and ungrouped dependencies are ambiguous')
    if groups:
        typed = []
        for g in groups:
            fw = g.get('targetFramework', '').strip()
            parsed = framework_tuple(fw)
            if parsed is not None and parsed <= target:
                typed.append((parsed, g, fw))
        if typed:
            best = max(item[0] for item in typed)
            matches = [item for item in typed if item[0] == best]
            if len(matches) != 1:
                raise ValueError('Ambiguous duplicate compatible framework dependency groups')
            _, chosen, chosen_fw = matches[0]
        else:
            generic = [g for g in groups if not g.get('targetFramework', '').strip()]
            if len(generic) != 1:
                raise ValueError('No unequivocal compatible .NET Framework dependency group')
            chosen, chosen_fw = generic[0], 'generic'
        children = list(chosen)
    else:
        chosen_fw = 'generic'
        children = list(deps_parent)
    out = []
    seen_dependencies = set()
    for x in children:
        if strip_ns(x.tag) != 'dependency':
            raise ValueError('Unsupported dependency element')
        name, rng = x.get('id', ''), x.get('version', '')
        if not ID.fullmatch(name):
            raise ValueError('Invalid dependency ID')
        if name.lower() in seen_dependencies:
            raise ValueError('Duplicate declared dependency ID in selected framework group')
        seen_dependencies.add(name.lower())
        version_range_contains(rng, '0.0')
        out.append({'id': name, 'version_range': rng})
    return out, chosen_fw


def inspect_package(path, name, ver, target, expected_sha256):
    p = pathlib.Path(path)
    if not p.is_file() or not 0 < p.stat().st_size <= MAX_ARCHIVE:
        raise ValueError('Missing or oversized archive: ' + str(p))
    if not re.fullmatch(r'[0-9a-fA-F]{64}', expected_sha256):
        raise ValueError('Missing or invalid pinned SHA-256')
    raw = p.read_bytes()
    observed_sha256 = hashlib.sha256(raw).hexdigest()
    if observed_sha256 != expected_sha256.lower():
        raise ValueError('Pinned NuGet archive SHA-256 mismatch: ' + name)
    with zipfile.ZipFile(p) as z:
        infos = z.infolist()
        if len(infos) > 5000:
            raise ValueError('Too many NuGet archive members')
        nuspecs = [e for e in infos if e.filename.lower().endswith('.nuspec')]
        if len(nuspecs) != 1 or nuspecs[0].file_size > MAX_NUSPEC:
            raise ValueError('Ambiguous or oversized nuspec')
        if len(set(e.filename.casefold() for e in infos)) != len(infos):
            raise ValueError('Duplicate case-insensitive archive entries')
        root = ET.fromstring(z.read(nuspecs[0]))
    if strip_ns(root.tag) != 'package':
        raise ValueError('Invalid nuspec package root')
    metadata_nodes = [e for e in root if strip_ns(e.tag) == 'metadata']
    if len(metadata_nodes) != 1:
        raise ValueError('Expected exactly one nuspec metadata element')
    metadata = metadata_nodes[0]
    attributes = {strip_ns(e.tag): (e.text or '').strip() for e in metadata}
    if attributes.get('id', '').lower() != name.lower() or attributes.get('version') != ver:
        raise ValueError('Archive ID/version does not match manifest: ' + name)
    deps, selected_fw = select_dependencies(metadata, target)
    return {'id': name, 'version': ver, 'dependency_group': selected_fw,
            'archive_sha256': observed_sha256, 'dependencies': deps}


def preflight(config, manifest, target='net48'):
    fw = framework_tuple(target)
    if fw is None:
        raise ValueError('Target must be .NET Framework, e.g. net48')
    baseline = parse_packages_config(config)
    source = json.loads(pathlib.Path(manifest).read_text(encoding='utf-8'))
    entries = source.get('packages')
    if not isinstance(entries, list) or not entries or len(entries) > 100:
        raise ValueError('Manifest requires 1..100 pinned tool package archives')
    chosen = {}
    for e in entries:
        name, ver = e['id'], e['version']
        if not ID.fullmatch(name):
            raise ValueError('Invalid tool package ID')
        numeric_version(ver)
        key = name.lower()
        if key in chosen:
            raise ValueError('Duplicate selected package (ambiguous resolution)')
        chosen[key] = inspect_package(e['path'], name, ver, fw, e['sha256'])
    conflicts, unresolved, edges, overlap = [], [], [], []
    for key, pkg in chosen.items():
        if key in baseline:
            old = baseline[key]['version']
            if old != pkg['version']:
                overlap.append({'id': pkg['id'], 'baseline': old, 'proposed': pkg['version']})
        for dep in pkg['dependencies']:
            depkey = dep['id'].lower()
            item = chosen.get(depkey)
            if item is not None:
                source_type = 'selected tool package'
            elif depkey in baseline:
                item = baseline[depkey]
                source_type = 'existing application package'
            else:
                unresolved.append({'parent': pkg['id'], 'dependency': dep['id'], 'required': dep['version_range']})
                continue
            satisfied = version_range_contains(dep['version_range'], item['version'])
            edge = {'parent': pkg['id'], 'dependency': dep['id'], 'required': dep['version_range'],
                    'selected': item['version'], 'source': source_type, 'satisfied': satisfied}
            edges.append(edge)
            if not satisfied:
                conflicts.append(edge)
    return {'schema_version': 1, 'kind': 'metadata-only-netfx-tool-dependency-preflight',
            'target': target, 'original_application_packages': sorted(baseline.values(), key=lambda e: e['id'].lower()),
            'tool_packages': sorted(chosen.values(), key=lambda e: e['id'].lower()),
            'dependency_edges': edges, 'baseline_version_overlaps': overlap,
            'conflicts': conflicts, 'unresolved_dependencies': unresolved,
            'status': 'PASS_METADATA_ONLY' if not (conflicts or unresolved or overlap) else 'BLOCKED',
            'limitations': ['Metadata selection uses conservative .NET Framework group selection, not official NuGet resolution.',
                            'No packages installed, no MSBuild target executed, no runtime/tool-host isolation established.',
                            'Archive bytes match manifest hashes; original archive provenance/feed and updated advisories require independent review.',
                            'Passing this check does not authorize a production dependency change.']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packages-config', required=True, type=pathlib.Path)
    parser.add_argument('--manifest', required=True, type=pathlib.Path)
    parser.add_argument('--target', default='net48')
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args(argv)
    try:
        if args.output.exists():
            raise ValueError('Refusing to overwrite existing evidence')
        report = preflight(args.packages_config, args.manifest, args.target)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(report['status'], 'conflicts=', len(report['conflicts']), 'unresolved=',
              len(report['unresolved_dependencies']), 'overlaps=',len(report['baseline_version_overlaps']))
        return 0 if report['status'] == 'PASS_METADATA_ONLY' else 2
    except (OSError, ValueError, KeyError, TypeError, ET.ParseError, zipfile.BadZipFile) as exc:
        print('PRE-FLIGHT ERROR (fail closed):', type(exc).__name__, str(exc)[:350], file=sys.stderr)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
