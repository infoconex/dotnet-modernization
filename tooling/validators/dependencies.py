#!/usr/bin/env python3
"""Inspect available NuGet restore assets and legacy local package evidence; never restore."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys

from provenance import snapshot, require_commit
import xml.etree.ElementTree as ET

SCHEMA_VERSION = 1
MAX_FILE = 32 * 1024 * 1024
SKIP = {'.git', '.vs', 'bin', 'node_modules', 'packages', '__pycache__', '.idea'}


def parse_json(path):
    if path.stat().st_size > MAX_FILE:
        raise ValueError('restore JSON exceeds inventory size limit')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def parse_xml(path):
    if path.stat().st_size > MAX_FILE:
        raise ValueError('packages XML exceeds inventory size limit')
    return ET.parse(path).getroot()


def key_split(ref):
    return ref.rsplit('/', 1) if '/' in ref else [ref, None]


def assets_record(path, rel):
    data = parse_json(path)
    if not isinstance(data, dict) or not isinstance(data.get('targets'), dict):
        raise ValueError('missing targets; file is not recognized NuGet assets JSON')
    libraries = data.get('libraries', {})
    if not isinstance(libraries, dict):
        raise ValueError('invalid libraries map')
    direct_by_tfm = {}
    for tfm, deps in data.get('project', {}).get('frameworks', {}).items():
        if isinstance(deps, dict):
            for alias in {tfm, deps.get('targetAlias', tfm)}:
                if alias:
                    direct_by_tfm[alias] = list((deps.get('dependencies') or {}).keys())
    group_direct = data.get('projectFileDependencyGroups', {})
    result = {'path': rel, 'source_kind': 'project.assets.json', 'version': data.get('version'),
              'targets': [], 'library_metadata_count': len(libraries),
              'package_folders_count': len(data.get('packageFolders', {})),
              'direct_classification_source': 'project.frameworks.dependencies and projectFileDependencyGroups',
              'limitations': ['Assets reflect the last restore represented by this file, not a fresh restore or download.',
                              'Package feed acquisition and vulnerability status are not established.',
                              'RID-specific assets and target frameworks must be inspected separately.']}
    for target, nodes in sorted(data['targets'].items()):
        if not isinstance(nodes, dict):
            raise ValueError('invalid restore target libraries')
        tfm = target.split('/')[0]
        classification_known = tfm in direct_by_tfm or tfm in group_direct
        top = {x.lower() for x in direct_by_tfm.get(tfm, [])}
        for dep in (group_direct.get(tfm, []) or []):
            if isinstance(dep, str):
                top.add(re.split(r'\s*[<>=\[(]', dep, maxsplit=1)[0].strip().lower())
        resolved_by_id = {}
        for full, item in nodes.items():
            if not isinstance(item, dict):
                raise ValueError('invalid target library entry')
            id_, version = key_split(full)
            resolved_by_id.setdefault(id_.lower(), []).append({'name': full, 'version': version})
        elements = []
        for full, item in sorted(nodes.items()):
            id_, version = key_split(full)
            dep_edges = []
            for dep, constraint in sorted((item.get('dependencies') or {}).items()):
                resolved = resolved_by_id.get(dep.lower(), [])
                dep_edges.append({'id': dep, 'requested': str(constraint),
                                  'resolved': resolved[0]['name'] if len(resolved) == 1 else None,
                                  'resolution': 'unique' if len(resolved) == 1 else 'ambiguous' if resolved else 'not_in_target'})
            info = libraries.get(full, {})
            elements.append({'id': id_, 'version': version, 'library_key': full,
                             'kind': item.get('type', info.get('type', 'unknown')),
                             'declared_direct': id_.lower() in top if classification_known else None,
                             'dependencies': dep_edges,
                             'compile_assets': len(item.get('compile', {})),
                             'runtime_assets': len(item.get('runtime', {})),
                             'native_assets': len(item.get('native', {})),
                             'has_metadata': full in libraries})
        result['targets'].append({'target': target, 'framework': tfm, 'libraries': elements,
                                  'direct_ids_from_restore': sorted(top),
                                  'direct_classification_available': classification_known})
    return result


def legacy_record(path, rel, packages_dir=None):
    root = parse_xml(path)
    package_dir = Path(packages_dir).resolve() if packages_dir else None
    entries = []
    for item in root.iter():
        if item.tag.rsplit('}', 1)[-1] != 'package':
            continue
        id_, version = item.get('id'), item.get('version')
        if not id_ or not version:
            raise ValueError('packages.config entry missing id or version')
        observation = 'not_checked'
        if package_dir is not None:
            candidate = package_dir / (id_ + '.' + version)
            if candidate.is_dir() and candidate.resolve().is_relative_to(package_dir):
                observation = 'directory_present'
            else:
                observation = 'not_found_in_supplied_folder'
        entries.append({'id': id_, 'version': version, 'targetFramework': item.get('targetFramework'),
                        'allowedVersions': item.get('allowedVersions'),
                        'local_package_directory': observation})
    return {'path': rel, 'source_kind': 'packages.config', 'packages': entries,
            'resolution': 'declared_versions_with_optional_directory_presence',
            'limitations': ['packages.config declarations are not a complete resolved dependency graph.',
                            'Directory presence is not package authenticity, restored provenance or file/reference parity.',
                            'Legacy NuGet dependency relationships need separate nuspec/restore analysis.']}


def collect(source, packages_dir=None):
    source = Path(source).resolve(strict=True)
    if not source.is_dir():
        raise ValueError('source must be a directory')
    if packages_dir is not None:
        packages_dir = Path(packages_dir).resolve(strict=True)
        if not packages_dir.is_dir():
            raise ValueError('packages directory must be a directory')
    record = {'schema_version': SCHEMA_VERSION, 'kind': 'available-dependency-resolution-evidence',
              'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'source_root': str(source),
              'source': snapshot(source),
              'assets': [], 'legacy': [], 'errors': [],
              'limitations': ['No restore executed. Missing assets or package directories remain unresolved.',
                              'Package source configuration and download provenance are not verified.',
                              'System/GAC/COM/native runtime dependencies and dynamic loading are not assessed.',
                              'Files in obj/ may be stale relative to the current source commit.']}
    for parent, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not (Path(parent) / d).is_symlink())
        for name in sorted(files):
            path = Path(parent) / name
            if path.is_symlink():
                continue
            rel = path.relative_to(source).as_posix()
            try:
                if name == 'project.assets.json' and path.parent.name == 'obj':
                    record['assets'].append(assets_record(path, rel))
                elif name.lower() == 'packages.config':
                    record['legacy'].append(legacy_record(path, rel, packages_dir))
            except (OSError, ValueError, ET.ParseError, KeyError, TypeError) as ex:
                record['errors'].append({'path': rel, 'problem': type(ex).__name__})
    record['resolution_status'] = ('partial' if record['errors'] else 'assets_available' if record['assets']
                                   else 'legacy_metadata_only' if record['legacy'] else 'no_restore_evidence')
    return record


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--packages-dir', type=Path, help='Optional legacy packages cache root; directory presence only')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--expect-commit', help='Require an exact 40-character Git SHA')
    args = p.parse_args(argv)
    try:
        source = args.source.resolve(strict=True)
        output = args.output.resolve()
        if output == source or output.is_relative_to(source):
            raise ValueError('output must be outside checkout')
        require_commit(snapshot(source)['commit'], args.expect_commit)
        report = collect(source, args.packages_dir)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print(f"Dependency evidence: {report['resolution_status']} | {output}")
        return 1 if report['errors'] or report['resolution_status'] == 'no_restore_evidence' else 0
    except (OSError, ValueError) as exc:
        print(f'ERROR: {type(exc).__name__}: {str(exc)[:200]}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
