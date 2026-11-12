#!/usr/bin/env python3
"""Read-only audit of pinned NuGet archives; never imports or executes package assets."""
import argparse
import hashlib
import json
import pathlib
import re
import stat
import sys
import xml.etree.ElementTree as ET
import zipfile

MAX_ARCHIVE_BYTES = 96 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 256 * 1024 * 1024
MAX_MEMBERS = 5000
MAX_NUSPEC_BYTES = 1024 * 1024
PACKAGE_NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$')
PACKAGE_VERSION = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.+-]{0,127}$')


def _strip_namespace(tag):
    return tag.split('}', 1)[-1]


def _single_child(node, name):
    matches = [child for child in node if _strip_namespace(child.tag) == name]
    if len(matches) != 1:
        raise ValueError('Expected exactly one nuspec ' + name)
    return matches[0]


def _reject_raw_central_directory_backslashes(archive_bytes, start, count):
    """Inspect raw ZIP central-directory filename bytes before platform path normalization.

    Python's zipfile.ZipInfo normalizes backslash separators on Windows. Relying
    only on decoded ZipInfo.filename would make our safety check OS-dependent.
    """
    pos = start
    for _ in range(count):
        if pos < 0 or pos + 46 > len(archive_bytes) or archive_bytes[pos:pos + 4] != b'PK\x01\x02':
            raise ValueError('Invalid raw ZIP central directory')
        n = int.from_bytes(archive_bytes[pos + 28:pos + 30], 'little')
        extra = int.from_bytes(archive_bytes[pos + 30:pos + 32], 'little')
        comment = int.from_bytes(archive_bytes[pos + 32:pos + 34], 'little')
        end = pos + 46 + n + extra + comment
        if end > len(archive_bytes):
            raise ValueError('Truncated raw ZIP central directory member')
        raw_name = archive_bytes[pos + 46:pos + 46 + n]
        if b'\\' in raw_name:
            raise ValueError('Unsafe raw ZIP path separator')
        pos = end


def inspect(archive, expected_id, expected_version):
    if not PACKAGE_NAME.fullmatch(expected_id) or not PACKAGE_VERSION.fullmatch(expected_version):
        raise ValueError('Invalid package ID or version')
    archive = pathlib.Path(archive)
    if not archive.is_file() or archive.stat().st_size > MAX_ARCHIVE_BYTES:
        raise ValueError('Missing or oversized pinned NuGet archive')
    archive_bytes = archive.read_bytes()
    archive_hash = hashlib.sha256(archive_bytes).hexdigest()
    with zipfile.ZipFile(archive, 'r') as nuget:
        members = nuget.infolist()
        _reject_raw_central_directory_backslashes(archive_bytes, nuget.start_dir, len(members))
        if len(members) > MAX_MEMBERS:
            raise ValueError('NuGet archive has too many members')
        seen = set()
        total = 0
        valid_files = []
        for member in members:
            raw = member.filename
            norm = raw.replace('\\', '/')
            segments = norm.split('/')
            if not raw or raw.startswith(('/', '\\')) or '\\' in raw or ':' in raw or (
                any(segment in ('', '.', '..') for segment in segments if segment != '') or
                (member.flag_bits & 1) or
                stat.S_IFMT((member.external_attr >> 16) & 0xFFFF) == stat.S_IFLNK
            ):
                raise ValueError('Unsafe, encrypted or invalid NuGet ZIP member')
            if raw.endswith('/'):
                continue
            if any(segment == '' for segment in segments):
                raise ValueError('Empty ZIP path component')
            if norm.casefold() in seen:
                raise ValueError('Duplicate case-insensitive NuGet member')
            seen.add(norm.casefold())
            total += member.file_size
            if total > MAX_UNCOMPRESSED_BYTES:
                raise ValueError('Uncompressed NuGet content exceeds budget')
            valid_files.append(raw)
        manifests = [name for name in valid_files if name.lower().endswith('.nuspec')]
        if len(manifests) != 1:
            raise ValueError('Expected exactly one embedded .nuspec')
        nuspec_info = nuget.getinfo(manifests[0])
        if nuspec_info.file_size > MAX_NUSPEC_BYTES:
            raise ValueError('Oversized package manifest')
        data = nuget.read(manifests[0])
        root = ET.fromstring(data)
        metadata = _single_child(root, 'metadata')
        actual_id = (_single_child(metadata, 'id').text or '').strip()
        actual_version = (_single_child(metadata, 'version').text or '').strip()
        if actual_id.lower() != expected_id.lower() or actual_version.lower() != expected_version.lower():
            raise ValueError('Unexpected embedded NuGet package identity/version')
        deps = []
        for node in metadata.iter():
            if _strip_namespace(node.tag) == 'dependency':
                deps.append({'id': node.attrib.get('id', ''), 'version_range': node.attrib.get('version', '')})
        deps.sort(key=lambda x: x['id'].casefold())
        assets = {'build': [], 'buildTransitive': [], 'tools': [], 'lib': [], 'runtimes': [], 'other': []}
        for name in valid_files:
            category = name.split('/')[0]
            category = category if category in assets else 'other'
            assets[category].append(name)
        for values in assets.values():
            values.sort()
        import_candidates = sorted(name for name in valid_files if
                                   name.lower().endswith(('.props', '.targets')))
        return {
            'id': actual_id, 'version': actual_version, 'archive_bytes': archive.stat().st_size,
            'archive_sha256': archive_hash, 'archive_member_count': len(valid_files),
            'embedded_manifest': manifests[0], 'declared_dependencies': deps,
            'msbuild_import_candidates': import_candidates, 'assets': assets,
            'metadata_only_no_target_execution': True,
        }


def audit(manifest):
    data = json.loads(pathlib.Path(manifest).read_text(encoding='utf-8'))
    entries = data.get('packages')
    if not isinstance(entries, list) or not entries or len(entries) > 24:
        raise ValueError('Manifest must contain between 1 and 24 pinned packages')
    results = []
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or not all(k in entry for k in ('id', 'version', 'path')):
            raise ValueError('A package entry requires id, version and path')
        identity = (entry['id'].lower(), entry['version'].lower())
        if identity in seen:
            raise ValueError('Duplicate pinned package identity')
        seen.add(identity)
        results.append(inspect(entry['path'], entry['id'], entry['version']))
    results.sort(key=lambda x: (x['id'].casefold(), x['version']))
    return {'schema_version': 1, 'kind': 'pinned-nuget-archive-build-asset-audit',
            'packages': results,
            'limitations': [
                'Downloaded packages were never executed or extracted by this auditor.',
                'An archive containing props/targets does not prove a traditional csproj imports or runs them.',
                'NuGet dependency declarations are not proof of full transitive resolution or a safe dependency graph.',
                'A no-lib-assets observation does not prove assembly outputs or NuGet distributions are unchanged.',
                'Security advisories and latest-version policy are documented separately and must be rechecked before installing.',
                'This is package inspection only, not Source Link PDB or debugger verification.'
            ]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=pathlib.Path)
    parser.add_argument('--output', required=True, type=pathlib.Path)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error('Refusing to overwrite existing audit evidence')
    try:
        result = audit(args.manifest)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        for item in result['packages']:
            print(item['id'], item['version'], item['archive_sha256'],
                  'imports:', len(item['msbuild_import_candidates']),
                  'dependencies:', len(item['declared_dependencies']))
        return 0
    except (OSError, ValueError, TypeError, KeyError, zipfile.BadZipFile, ET.ParseError) as ex:
        print('NuGet read-only audit failed closed:', type(ex).__name__, str(ex)[:250], file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
