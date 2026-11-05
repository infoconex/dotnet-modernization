#!/usr/bin/env python3
"""Verify remote Git bytes for every uniquely identified owned .cs source in native PDB LLVM inventory."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
from sourcelink_remote_source import verify, EXPECTED_SHA

PROJECT_PREFIX = 'src/RecordSift.Infrastructure.Csv/'
MIN_DOCUMENTS = 4
MAX_DOCUMENTS = 32
DOCUMENT_RE = re.compile(r'(?i)([A-Za-z_][A-Za-z_0-9]*\.cs)\b')


def selected_source_files(inventory, source_root):
    # Only include source files independently listed by LLVM, not every URL
    # theoretically reachable through the wildcard Source Link template.
    owned = list((source_root / PROJECT_PREFIX).rglob('*.cs'))
    by_leaf = {}
    for path in owned:
        key = path.name.casefold()
        if key in by_leaf:
            raise ValueError('Ambiguous source filename within owned project')
        by_leaf[key] = path.relative_to(source_root).as_posix()
    selected = set()
    for line in inventory.splitlines():
        if '.cs' not in line.casefold():
            continue
        if '(no checksum)' not in line.lower() and 'checksum' not in line.lower():
            # LLVM -files line formatting may change. Do not accept
            # miscellaneous C# text as a PDB source document record.
            continue
        names = DOCUMENT_RE.findall(line)
        if len(names) != 1:
            raise ValueError('Ambiguous PDB source document line')
        name = names[0].casefold()
        if name in by_leaf:
            selected.add(by_leaf[name])
        elif 'RecordSift.Infrastructure.Csv' in line:
            raise ValueError('Unmatched document belonging to CSV project')
    result = sorted(selected)
    if not MIN_DOCUMENTS <= len(result) <= MAX_DOCUMENTS:
        raise ValueError('PDB native inventory did not enumerate expected owned source documents')
    if PROJECT_PREFIX + 'CsvStreamImporterAdapter.cs' not in result:
        raise ValueError('Original EXP-028 selected source absent from independent document inventory')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--pdb', required=True, type=Path)
    p.add_argument('--source-root', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    if a.output.exists():
        p.error('Refusing to overwrite evidence')
    try:
        root = a.source_root.resolve(strict=True)
        run = subprocess.run(['llvm-pdbutil', 'dump', '-modules', '-files', '-l', str(a.pdb)],
                             check=True, capture_output=True, text=True, timeout=45)
        paths = selected_source_files(run.stdout, root)
        docs = [verify(a.pdb, root, path) for path in paths]
        if len(docs) != len(paths) or any(x['exact_frozen_sha'] != EXPECTED_SHA for x in docs):
            raise ValueError('Not all enumerated owned source documents passed Git blob parity')
        result = {
            'experiment':'EXP-034', 'frozen_commit': EXPECTED_SHA,
            'native_pdb_inventory': 'independent_llvm_file_reference_rows',
            'documents_verified': len(docs), 'all_selected_mappings_and_git_blobs_match': True,
            'documents': docs,
            'limitation':'Scans owned independently listed CSV sources; not PDB per-document checksum records, external/generated files or debugger UI'
        }
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n',encoding='utf-8')
        print('EXP-034 verified',len(docs),'independently listed actual PDB source URLs against frozen Git blobs')
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as e:
        p.exit(2,'EXP-034 failed closed: '+type(e).__name__+'\n')


if __name__ == '__main__':
    main()
