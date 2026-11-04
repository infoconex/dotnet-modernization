#!/usr/bin/env python3
"""Compare metadata-only PE snapshots from three independently validated builds.

Exactly the same Git source is used for all three builds. This reports raw PE
and IL changes, not semantic equivalence or a deterministic-build verdict.
"""
import argparse
import json
from pathlib import Path
import sys

SCHEMA = 1


def read_snapshot(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(data, dict) or data.get('schema_version') != SCHEMA or \
            data.get('kind') != 'managed-pe-provenance':
        raise ValueError('Expected managed-pe-provenance schema version 1')
    assemblies = data.get('assemblies')
    if not isinstance(assemblies, list) or not assemblies:
        raise ValueError('No managed assemblies in PE evidence')
    result = {}
    for assembly in assemblies:
        if not isinstance(assembly, dict) or \
                not isinstance(assembly.get('assembly'), str) or not assembly['assembly'] or \
                not isinstance(assembly.get('file_sha256'), str) or len(assembly['file_sha256']) != 64 or \
                not isinstance(assembly.get('mvid'), str) or \
                not isinstance(assembly.get('method_bodies'), dict) or \
                not isinstance(assembly.get('debug_directory'), list) or \
                not isinstance(assembly.get('coff_timestamp_hex'), str):
            raise ValueError('Missing required PE evidence')
        if assembly['assembly'] in result:
            raise ValueError('Duplicate assembly name')
        result[assembly['assembly']] = assembly
    return result


def compare_pair(baseline, other):
    if set(baseline) != set(other):
        raise ValueError('Assembly names differ or required evidence is missing')
    output = {}
    for name in sorted(baseline):
        left, right = baseline[name], other[name]
        left_methods, right_methods = left['method_bodies'], right['method_bodies']
        tokens = sorted(set(left_methods) | set(right_methods))
        changed_methods = [token for token in tokens if
                           left_methods.get(token) != right_methods.get(token)]
        keys = ('bytes', 'mvid', 'coff_timestamp_hex', 'pe_kind',
                'assembly_version', 'method_body_count', 'method_il_total_bytes', 'debug_directory')
        changed_fields = [field for field in keys if left.get(field) != right.get(field)]
        output[name] = {
            'status': 'identical_binary' if left['file_sha256'] == right['file_sha256'] else 'different_binary',
            'baseline_file_sha256': left['file_sha256'],
            'candidate_file_sha256': right['file_sha256'],
            'changed_metadata_fields': changed_fields,
            'changed_method_il_tokens': changed_methods,
            'method_il_tokens_match': not changed_methods,
            'mvid_changed': left['mvid'] != right['mvid'],
            'coff_timestamp_changed': left['coff_timestamp_hex'] != right['coff_timestamp_hex'],
            'debug_directory_changed': left['debug_directory'] != right['debug_directory'],
        }
    return {
        'assemblies': output,
        'identical_binaries': sum(v['status'] == 'identical_binary' for v in output.values()),
        'different_binaries': sum(v['status'] == 'different_binary' for v in output.values()),
        'changed_method_il_assemblies': [
            name for name in sorted(output) if not output[name]['method_il_tokens_match']]
    }


def compare_three(original, independent, same_path_rebuild):
    a, b, c = [read_snapshot(p) for p in (original, independent, same_path_rebuild)]
    if set(a) != set(b) or set(a) != set(c):
        raise ValueError('Three builds must report identical sets of assembly identities')
    return {
        'schema_version': SCHEMA, 'kind': 'pe-reproducibility-comparison',
        'source_constraint': 'all builds verified against the SAME source Git commit by outer pilot',
        'assembly_names': sorted(a),
        'independent_worktree': compare_pair(a, b),
        'same_worktree_rebuild': compare_pair(a, c),
        'interpretation': [
            'A binary mismatch is a byte-level observation, not a CLR compatibility failure.',
            'Raw IL byte equality is narrower than full assembly byte equality and not a semantic equivalence proof.',
            'MVID, COFF and CodeView/PDB fields are observations. Their changes do not prove the only cause of byte differences.',
            'Builds are not declared hermetic; distinct worktrees, build times and package caches may differ.',
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', type=Path, required=True)
    parser.add_argument('--independent', type=Path, required=True)
    parser.add_argument('--same-path-rebuild', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error('Output evidence already exists; use a fresh destination')
    try:
        report = compare_three(args.original, args.independent, args.same_path_rebuild)
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as error:
        print(f'PE comparison failed closed: {type(error).__name__}: {error}', file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    for label in ('independent_worktree', 'same_worktree_rebuild'):
        case = report[label]
        print(label, 'identical:', case['identical_binaries'],
              'different:', case['different_binaries'],
              'raw-IL-changed-assemblies:', len(case['changed_method_il_assemblies']))
        for name, entry in case['assemblies'].items():
            print(' ', name, entry['status'], 'mvid_changed:', entry['mvid_changed'],
                  'coff_changed:', entry['coff_timestamp_changed'],
                  'debug_changed:', entry['debug_directory_changed'],
                  'raw_il_changes:', len(entry['changed_method_il_tokens']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
