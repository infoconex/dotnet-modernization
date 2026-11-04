#!/usr/bin/env python3
"""EXP-017 adapter: compare real locally built packages and prove byte-level negative controls.

Runs only after the unmodified EXP-015 Windows research pilot has independently
built the baseline and disposable conditional LangVersion candidate.
"""
import argparse
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tooling' / 'validators'))
import compatibility
import package_payload

SOURCE_SHA = '8358780829458854a4b0356df5ac5e685f0a34c8'
TARGET = 'lib/net48/RecordSift.Domain.dll'


def repository_metadata(package):
    with zipfile.ZipFile(package) as archive:
        roots = [name for name in archive.namelist()
                 if '/' not in name and name.lower().endswith('.nuspec')]
        if len(roots) != 1:
            raise ValueError('Expected exactly one package manifest')
        xml = ET.fromstring(archive.read(roots[0]))
        node = xml.find('./{*}metadata/{*}repository')
        if node is None:
            raise ValueError('Package repository metadata is missing')
        return {'branch': node.attrib.get('branch'), 'commit': node.attrib.get('commit'),
                'url': node.attrib.get('url')}


def mutate_one_member(original, destination):
    """Synthetic *in-memory* package mutation only; never modify application DLLs."""
    with zipfile.ZipFile(original, 'r') as before, zipfile.ZipFile(destination, 'w') as after:
        items = before.infolist()
        targets = [entry for entry in items if entry.filename == TARGET]
        if len(targets) != 1:
            raise ValueError('Expected exactly one RecordSift.Domain.dll member')
        for entry in items:
            if entry.is_dir():
                after.writestr(entry, b'')
                continue
            data = before.read(entry.filename)
            if entry.filename == TARGET:
                if not data:
                    raise ValueError('Cannot mutate empty DLL')
                data = bytes([data[0] ^ 1]) + data[1:]
            after.writestr(entry, data)


def execute(evidence):
    if not evidence.is_dir():
        raise ValueError('EXP-015 evidence root does not exist')
    baseline = evidence / 'baseline-evidence' / 'local-package' / 'RecordSift.0.1.0.nupkg'
    candidate = evidence / 'candidate-evidence' / 'local-package' / 'RecordSift.0.1.0.nupkg'
    candidate_report = json.loads((evidence / 'candidate-report.json').read_text(encoding='utf-8-sig'))
    if candidate_report['baseline_source_sha'] != SOURCE_SHA or candidate_report['comparison_result'] != 'matched':
        raise ValueError('EXP-015 real candidate compatibility gates not accepted')
    candidate_sha = candidate_report['ephemeral_candidate_sha']
    for sha in (SOURCE_SHA, candidate_sha):
        if len(sha) != 40 or not all(c in '0123456789abcdef' for c in sha):
            raise ValueError('Invalid original or candidate commit SHA')

    # Baseline + candidate are *real independently compiled package archives*.
    real = package_payload.compare_packages(baseline, candidate)
    if real['overall'] in ('error', 'incomplete'):
        raise ValueError('Actual package comparison failed: ' + real['overall'])
    original = repository_metadata(baseline)
    changed = repository_metadata(candidate)
    if original['commit'] != SOURCE_SHA or changed['commit'] != candidate_sha:
        raise ValueError('Repository provenance commit does not match actual source revisions')
    if original['url'] != changed['url']:
        raise ValueError('Package repository URLs unexpectedly differ')

    # Positive control: same-package byte comparison must match.
    identical = package_payload.compare_packages(baseline, baseline)
    if identical['overall'] != 'identical_archive_and_entries':
        raise ValueError('Same-package positive control did not match')

    # Negative: keep every package entry *path* unchanged, but change a single
    # byte of actual DLL payload in a disposable package copy (never pushed).
    mutated_path = evidence / 'intentionally-mutated-archive.nupkg'
    mutate_one_member(baseline, mutated_path)
    mutated = package_payload.compare_packages(baseline, mutated_path)
    if mutated['overall'] != 'different_entries' or mutated['changed_member_count'] != 1 or \
            mutated['entry_differences'][0]['path'] != TARGET or \
            mutated['entry_differences'][0]['kind'] != 'bytes_changed' or \
            not mutated['member_path_sets_match']:
        raise ValueError('Byte mutation was not precisely detected')
    if compatibility.package_contract(baseline) != compatibility.package_contract(mutated_path):
        raise ValueError('Logical-only comparator unexpectedly detected byte mutation')

    # Incomplete evidence must fail closed.
    missing = package_payload.compare_packages(baseline, evidence / 'missing.nupkg')
    if missing['overall'] != 'incomplete':
        raise ValueError('Missing package was incorrectly accepted')

    # Keep real observations descriptive: both identical and differing member
    # digests are valid experimental findings, not assumed compatibility claims.
    summary = {
        'experiment': 'EXP-017',
        'baseline_sha': SOURCE_SHA,
        'baseline_tree_sha': candidate_report['baseline_tree_sha'],
        'ephemeral_candidate_sha': candidate_sha,
        'candidate_tree_sha': candidate_report['candidate_tree_sha'],
        'source_edit': 'conditional LangVersion migration in disposable checkout, unchanged EXP-015',
        'real_package_comparison': real,
        'repository_metadata': {'baseline': original, 'candidate': changed},
        'positive_same_archive': identical['overall'],
        'negative_one_Dll_member_byte': {
            'expected_path': TARGET,
            'result': mutated['overall'],
            'difference': mutated['entry_differences'][0],
            'logical_contract_unchanged': True,
        },
        'missing_package_evidence': missing['overall'],
        'source_integrity': 'all candidate commits local to the GitHub Actions runner; none pushed',
        'limitations': [
            'Exact SHA-256 of package and named uncompressed members; not a proof of IL or runtime semantic equivalence.',
            'Different ZIP container bytes alone may be caused by entry timestamp/compression/layout differences.',
            'A package member may differ due to deterministic-build inputs, compiler paths, version stamping or source code.',
            'Diffing packages does not identify malicious content and is not a security scan.',
            'Repository branch metadata is captured as observed, without assuming correct semantics.',
        ],
    }
    (evidence / 'package-payload-report.json').write_text(
        json.dumps(summary, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('EXP-017 source contract comparison:', candidate_report['comparison_result'])
    print('EXP-017 real package member-byte result:', real['overall'])
    print('EXP-017 real package changed members:', real['changed_member_count'])
    for entry in real['entry_differences']:
        print('  ' + entry['kind'] + ' ' + entry['path'])
    print('EXP-017 same-package positive:', identical['overall'])
    print('EXP-017 one-member negative:', mutated['overall'], TARGET)
    print('EXP-017 missing package evidence:', missing['overall'])
    print('EXP-017 baseline repository metadata:', original)
    print('EXP-017 candidate repository metadata:', changed)
    print('PASS: EXP-017 exact-byte observation + valid positive/negative/fail-closed controls')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--exp015-evidence', type=Path, required=True)
    args = parser.parse_args()
    execute(args.exp015_evidence.resolve())
