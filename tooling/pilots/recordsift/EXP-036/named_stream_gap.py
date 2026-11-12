#!/usr/bin/env python3
"""Bounded structural native Windows-PDB named-stream contrast, metadata only.

This is not a managed document checksum reader or proof of physical absence.
Use only trusted, locally compiled PDBs. Never include raw PDB, source or paths
in emitted evidence.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tooling" / "validators"))
from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview


def summarize(dll, pdb):
    streams = read_msf(Path(pdb).read_bytes())
    guid, age, names = parse_named_streams(streams[1], len(streams))
    if (guid, age) != read_pe_codeview(Path(dll).read_bytes()):
        raise ValueError("PE/PDB CodeView GUID and age do not match")
    source = [i for name, i in names.items()
              if name.upper().startswith("/SRC/FILES/")]
    sourcelink = [i for name, i in names.items()
                  if name.lower().startswith("sourcelink")]
    return {
        "pe_pdb_identity": "MATCHED",
        "pdb_format": "MSF7 classic Windows PDB",
        "named_stream_count": len(names),
        "src_files_named_stream_count": len(source),
        "src_files_nonempty_stream_count": sum(
            1 for i in source if streams[i] is not None and len(streams[i]) > 0
        ),
        "src_files_total_bytes": sum(
            len(streams[i]) if streams[i] is not None else 0 for i in source
        ),
        "source_link_named_stream_count": len(sourcelink),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-sha1-dll", required=True, type=Path)
    parser.add_argument("--fixture-sha1-pdb", required=True, type=Path)
    parser.add_argument("--fixture-sha256-dll", required=True, type=Path)
    parser.add_argument("--fixture-sha256-pdb", required=True, type=Path)
    parser.add_argument("--csv-dll", required=True, type=Path)
    parser.add_argument("--csv-pdb", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = {
        "research_gate": "DIAGNOSTIC_ONLY",
        "scope": "exact named PDB stream categories, not document checksum authenticity",
        "fixture_sha1": summarize(args.fixture_sha1_dll, args.fixture_sha1_pdb),
        "fixture_sha256": summarize(args.fixture_sha256_dll, args.fixture_sha256_pdb),
        "actual_frozen_csv": summarize(args.csv_dll, args.csv_pdb),
        "limitations": [
            "A missing named /SRC/FILES stream is not proof that no checksums exist elsewhere",
            "A nonempty source-file stream does not establish document checksum authenticity",
            "No PDB binaries or source bytes are retained",
        ],
    }
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print("Compared managed fixture and frozen CSV native MSF7 named-stream categories")
    for key in ("fixture_sha1", "fixture_sha256", "actual_frozen_csv"):
        row = result[key]
        print("{}: /SRC/FILES/ streams={} nonempty={} SourceLink streams={}".format(
            key, row["src_files_named_stream_count"],
            row["src_files_nonempty_stream_count"],
            row["source_link_named_stream_count"],
        ))


if __name__ == "__main__":
    main()
