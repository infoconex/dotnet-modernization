#!/usr/bin/env python3
"""Verify selected Source Link PDB mapping resolves to exact immutable Git source bytes.

Read-only network fetch to one allowlisted raw.githubusercontent.com origin.
This does NOT inspect PDB C13 per-document checksum records or debugger behavior.
"""
import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import urllib.parse
import urllib.request

from native_windows_pdb_sourcelink import (
    EXPECTED_SHA, parse_named_streams, read_msf,
)

MAX_SOURCE_BYTES = 1024 * 1024
ROOT = 'https://raw.githubusercontent.com/infoconex/RecordSift/'


def mapping_from_pdb(pdb):
    streams = read_msf(pathlib.Path(pdb).read_bytes())
    _, _, named = parse_named_streams(streams[1], len(streams))
    indices = [(name, idx) for name, idx in named.items()
               if re.fullmatch(r'sourcelink(?:\$\d+)?', name, re.I)]
    if len(indices) != 1:
        raise ValueError('Expected exactly one actual Source Link named PDB stream')
    raw = streams[indices[0][1]]
    if raw is None or len(raw) > 1024 * 1024:
        raise ValueError('Missing or excessive Source Link data')
    obj = json.loads(raw.rstrip(b'\0').decode('utf-8', 'strict'))
    docs = obj.get('documents') if isinstance(obj, dict) else None
    if not isinstance(docs, dict) or len(docs) != 1:
        raise ValueError('Expected one bounded Source Link documents mapping')
    return docs


def derive_raw_url(mappings, relative_file, sha=EXPECTED_SHA):
    if not isinstance(relative_file, str):
        raise ValueError('Invalid relative filename type')
    path = relative_file.replace('\\', '/')
    if (not path.startswith('src/') or '..' in path.split('/') or
        '//' in path or '\0' in path or '?' in path or '#' in path):
        raise ValueError('Only validated owned src/ file paths permitted')
    if len(mappings) != 1:
        raise ValueError('Expected unambiguous Source Link mapping')
    pattern, template = next(iter(mappings.items()))
    if (not isinstance(pattern, str) or not isinstance(template, str) or
        pattern.count('*') != 1 or template.count('*') != 1 or
        '\\' in pattern or '\\' in template or not pattern.startswith('/_/')):
        raise ValueError('Unsupported or unsafe Source Link mapping wildcard')
    normalized_pdb_path = '/_/' + path
    prefix, suffix = pattern.split('*')
    if not normalized_pdb_path.startswith(prefix) or not normalized_pdb_path.endswith(suffix):
        raise ValueError('Frozen source path does not match compiled Source Link PDB mapping')
    wildcard = normalized_pdb_path[len(prefix):len(normalized_pdb_path)-len(suffix) if suffix else None]
    if not wildcard:
        raise ValueError('Empty Source Link wildcard')
    raw_url = template.replace('*', wildcard)
    parsed = urllib.parse.urlsplit(raw_url)
    expected_prefix = ROOT + sha + '/'
    if (parsed.scheme != 'https' or parsed.hostname != 'raw.githubusercontent.com' or
        parsed.username or parsed.password or parsed.port or parsed.query or parsed.fragment or
        not raw_url.startswith(expected_prefix) or
        parsed.path != urllib.parse.urlsplit(expected_prefix + path).path):
        raise ValueError('Source Link template did not resolve to exact frozen raw Git blob URL')
    return raw_url


def verify(pdb, source_root, relative_file, sha=EXPECTED_SHA, fetch=None):
    source_root = pathlib.Path(source_root).resolve(strict=True)
    head = subprocess.run(['git', '-C', str(source_root), 'rev-parse', 'HEAD'],
                          capture_output=True, check=True, text=True).stdout.strip()
    if head != sha:
        raise ValueError('Local source HEAD does not match frozen provenance')
    path = pathlib.Path(relative_file)
    full = (source_root / path).resolve(strict=True)
    if not full.is_relative_to(source_root) or not full.is_file():
        raise ValueError('Source file escapes frozen checkout')
    tracked = subprocess.run(['git', '-C', str(source_root), 'ls-files', '--error-unmatch', '--', relative_file],
                             capture_output=True, text=True, check=False)
    if tracked.returncode != 0:
        raise ValueError('Source file not tracked in frozen Git index')
    local = full.read_bytes()
    if len(local) > MAX_SOURCE_BYTES or not local:
        raise ValueError('Working-tree source exceeds byte-size budget')
    # A Windows checkout may have CRLF while raw.githubusercontent.com returns
    # the immutable Git blob (normally LF). HEAD and "tracked" alone do NOT
    # establish that a working-tree file is unmodified.
    diff = subprocess.run(['git', '-C', str(source_root), 'diff', '--quiet', 'HEAD',
                           '--', relative_file], check=False)
    if diff.returncode != 0:
        raise ValueError('Local worktree source differs from frozen Git revision or diff failed')
    blob = subprocess.run(['git', '-C', str(source_root), 'show', sha + ':' + relative_file],
                          check=True, capture_output=True).stdout
    if not blob or len(blob) > MAX_SOURCE_BYTES:
        raise ValueError('Frozen Git object exceeds source size budget')
    url = derive_raw_url(mapping_from_pdb(pdb), relative_file, sha)
    if fetch is None:
        req = urllib.request.Request(url, headers={'User-Agent': 'RecordSift-ReadOnly-SourceLink-Probe'})
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status != 200 or response.geturl() != url:
                raise ValueError('Remote source response failed allowlisted URL/no-redirect check')
            remote = response.read(MAX_SOURCE_BYTES + 1)
    else:
        remote = fetch(url)
    if not isinstance(remote, bytes) or len(remote) > MAX_SOURCE_BYTES or remote != blob:
        raise ValueError('Remote Git source bytes do not match exact frozen Git blob')
    checkout_equal = local == blob
    return {'schema_version': 2, 'source_link_mapping_to_raw_url': 'verified',
            'exact_frozen_sha': sha, 'relative_tracked_source': relative_file,
            'source_bytes': len(blob), 'sha256_frozen_git_blob_and_remote': hashlib.sha256(blob).hexdigest(),
            'working_tree_bytes': len(local),
            'sha256_local_worktree': hashlib.sha256(local).hexdigest(),
            'working_tree_byte_equal_git_blob': checkout_equal,
            'worktree_difference_consistent_with_crlf_conversion':
                (not checkout_equal and local.replace(b'\r\n', b'\n') == blob),
            'warning': 'PDB per-file checksum record and real debugger stepping not inspected.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdb', type=pathlib.Path, required=True)
    p.add_argument('--source-root', type=pathlib.Path, required=True)
    p.add_argument('--relative-file', required=True)
    p.add_argument('--output', type=pathlib.Path, required=True)
    a = p.parse_args()
    if a.output.exists():
        p.error('Refusing overwrite of retained research evidence')
    try:
        report = verify(a.pdb, a.source_root, a.relative_file)
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
        print('PASS: mapped frozen raw Git source bytes match immutable blob SHA256',
              report['sha256_frozen_git_blob_and_remote'])
    except (ValueError, OSError, KeyError, TypeError, UnicodeError, subprocess.CalledProcessError,
            urllib.error.URLError, json.JSONDecodeError) as error:
        p.exit(2, 'Frozen Source Link URL verification failed closed: ' + str(error)[:300] + '\n')


if __name__ == '__main__':
    main()
