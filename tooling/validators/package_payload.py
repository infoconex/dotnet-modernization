#!/usr/bin/env python3
"""Bounded, no-extraction byte inventory for independently built NuGet ZIP packages.

This is an orthogonal check to compatibility.py's logical package contract.
A matching public API is not evidence that payload bytes are identical.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import zipfile

SCHEMA = 1
MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
MAX_MEMBERS = 10000
MAX_MEMBER_BYTES = 256 * 1024 * 1024
MAX_TOTAL_UNCOMPRESSED = 1024 * 1024 * 1024
CHUNK = 1024 * 1024


def digest_stream(stream):
    hashed = hashlib.sha256()
    count = 0
    while True:
        data = stream.read(CHUNK)
        if not data:
            break
        count += len(data)
        hashed.update(data)
    return hashed.hexdigest(), count


def safe_path(name):
    if not name or '\x00' in name or '\\' in name or name.startswith('/'):
        return False
    if re.match(r'^[a-zA-Z]:', name):
        return False
    segments = name.rstrip('/').split('/')
    return bool(segments) and all(x not in ('', '.', '..') for x in segments)


def inspect_package(path):
    """Return ZIP container digest and exact uncompressed member-byte digests.

    No payload is extracted, executed or loaded as an assembly.
    Reject malformed, ambiguous and oversized archives; no partial success.
    """
    path = Path(path)
    archive_size = path.stat().st_size
    if archive_size > MAX_ARCHIVE_BYTES:
        raise ValueError('package archive exceeds size limit')
    with path.open('rb') as data:
        archive_digest, _ = digest_stream(data)
    members = {}
    with zipfile.ZipFile(path, 'r') as archive:
        items = archive.infolist()
        if len(items) > MAX_MEMBERS:
            raise ValueError('too many ZIP members')
        total_size = 0
        unique_names = set()
        for info in items:
            name = info.filename
            if not safe_path(name):
                raise ValueError('unsafe ZIP member path')
            key = name.rstrip('/').casefold()
            if key in unique_names:
                raise ValueError('duplicate or case-colliding ZIP member')
            unique_names.add(key)
            mode = (info.external_attr >> 16) & 0xFFFF
            if stat.S_IFMT(mode) == stat.S_IFLNK:
                raise ValueError('ZIP symlinks are unsupported')
            if info.flag_bits & 0x1:
                raise ValueError('encrypted ZIP member is unsupported')
            if info.file_size < 0 or info.file_size > MAX_MEMBER_BYTES:
                raise ValueError('ZIP member exceeds size limit')
            total_size += info.file_size
            if total_size > MAX_TOTAL_UNCOMPRESSED:
                raise ValueError('ZIP expands beyond size limit')
            if info.is_dir():
                continue
            with archive.open(info, 'r') as stream:
                digest, size = digest_stream(stream)
            if size != info.file_size:
                raise ValueError('ZIP entry size mismatch')
            members[name] = {'size': size, 'sha256': digest}
        manifests = [name for name in members
                     if '/' not in name and name.lower().endswith('.nuspec')]
        if len(manifests) != 1:
            raise ValueError('package must contain exactly one root nuspec')
    return {'archive_sha256': archive_digest, 'archive_bytes': archive_size,
            'member_count': len(members), 'members': dict(sorted(members.items()))}


def compare_packages(baseline, candidate):
    try:
        left, right = inspect_package(baseline), inspect_package(candidate)
    except FileNotFoundError:
        return {'schema_version': SCHEMA, 'kind': 'package-byte-comparison',
                'overall': 'incomplete', 'reason': 'required package missing'}
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile,
            zipfile.LargeZipFile, EOFError, NotImplementedError) as error:
        return {'schema_version': SCHEMA, 'kind': 'package-byte-comparison',
                'overall': 'error', 'reason': type(error).__name__,
                'detail': str(error)[:160]}
    before, after = left['members'], right['members']
    changes = []
    for name in sorted(set(before) | set(after)):
        if name not in before:
            changes.append({'path': name, 'kind': 'added', 'candidate': after[name]})
        elif name not in after:
            changes.append({'path': name, 'kind': 'removed', 'baseline': before[name]})
        elif before[name] != after[name]:
            changes.append({'path': name, 'kind': 'bytes_changed',
                            'baseline': before[name], 'candidate': after[name]})
    if changes:
        status = 'different_entries'
    elif left['archive_sha256'] != right['archive_sha256']:
        status = 'different_container_same_entries'
    else:
        status = 'identical_archive_and_entries'
    return {'schema_version': SCHEMA, 'kind': 'package-byte-comparison',
            'overall': status,
            'baseline': {key: val for key, val in left.items() if key != 'members'},
            'candidate': {key: val for key, val in right.items() if key != 'members'},
            'entry_differences': changes,
            'changed_member_count': len(changes),
            'member_path_sets_match': set(before) == set(after),
            'limits': {'max_archive_bytes': MAX_ARCHIVE_BYTES,
                       'max_members': MAX_MEMBERS, 'max_member_bytes': MAX_MEMBER_BYTES,
                       'max_total_uncompressed_bytes': MAX_TOTAL_UNCOMPRESSED},
            'scope': 'exact ZIP archive bytes and uncompressed named member bytes; not semantic binary equivalence',
            'interpretation': 'Source, environment and signing provenance must be supplied separately.'}


def run(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error('output report already exists; use a new evidence directory')
    if args.output.resolve() in (args.baseline.resolve(), args.candidate.resolve()):
        parser.error('output report must not overwrite package')
    report = compare_packages(args.baseline, args.candidate)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print('Package byte comparison:', report['overall'])
    if report['overall'] == 'identical_archive_and_entries':
        return 0
    return 2 if report['overall'] == 'error' else 1


if __name__ == '__main__':
    sys.exit(run())
