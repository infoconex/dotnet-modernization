#!/usr/bin/env python3
"""Read-only native MSF7 stream byte inventory, independent of managed readers.

A digest hit is only evidence of bytes somewhere in a trusted PDB, not proof
of an associated managed source document. A miss cannot prove universal absence.
No PDBs, sources, digest values or private paths are retained.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tooling" / "validators"))
from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview

VARIANTS = (
    "explicit-sha256",
    "implicit-checksum",
    "deterministic-only",
    "deterministic-pathmap",
    "deterministic-pathmap-sourcelink",
)
CSV_SOURCES = (
    "CharacterLimitedTextReader.cs",
    "CsvRecordReaderAdapter.cs",
    "CsvStreamImporterAdapter.cs",
    "MalformedCsvException.cs",
)

def inspect(dll, pdb, sources):
    streams = read_msf(pdb.read_bytes())
    guid, age, _ = parse_named_streams(streams[1], len(streams))
    if read_pe_codeview(dll.read_bytes()) != (guid, age):
        raise ValueError("PE/PDB CodeView identity mismatch")
    if not sources:
        raise ValueError("Missing owned source inputs")
    results = []
    for source in sources:
        original = source.read_bytes()
        if not original:
            raise ValueError("Empty owned source input")
        digests = {
            name: hashlib.new(name, original).digest()
            for name in ("sha1", "sha256")
        }
        mutated = hashlib.sha256(original + b"\\x01").digest()
        observed = {
            name: sum(value.count(digest) for value in streams if value is not None)
            for name, digest in digests.items()
        }
        mutation_hits = sum(value.count(mutated) for value in streams if value is not None)
        if mutation_hits:
            raise ValueError("Mutated-source negative digest unexpectedly present")
        results.append({
            "source_name": source.name,
            "sha1_digest_raw_occurrences": observed["sha1"],
            "sha256_digest_raw_occurrences": observed["sha256"],
            "post_compile_mutation_negative": "NO_RAW_DIGEST_OCCURRENCE",
        })
    return {
        "pdb_identity": "MATCHED",
        "stream_count": len(streams),
        "source_digests": results,
    }

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fixture-root", required=True, type=Path)
    ap.add_argument("--application-root", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    if args.output.exists():
        ap.error("Refusing to overwrite existing evidence")
    fixture = args.fixture_root
    source = fixture / "EXP037-source" / "DifferentialSource.cs"
    reports = {}
    for label in VARIANTS:
        directory = fixture / ("EXP037-" + label)
        reports[label] = inspect(
            directory / "Differential.dll",
            directory / "Differential.pdb",
            [source],
        )
    csv = args.application_root / "src" / "RecordSift.Infrastructure.Csv"
    reports["frozen_csv_candidate"] = inspect(
        csv / "bin" / "Release" / "RecordSift.Infrastructure.Csv.dll",
        csv / "bin" / "Release" / "RecordSift.Infrastructure.Csv.pdb",
        [csv / name for name in CSV_SOURCES],
    )
    control = reports["explicit-sha256"]["source_digests"][0]
    result = {
        "experiment": "EXP-037",
        "method": "read_only_byte_search_across_validated_native_MSF7_streams",
        "raw_sha256_positive_control": (
            "PASS" if control["sha256_digest_raw_occurrences"] > 0 else "NOT_CALIBRATED"
        ),
        "results": reports,
        "boundary": (
            "Raw digest byte presence does not prove a native document record, "
            "checksum association or reader correctness; an absent raw pattern "
            "does not prove no digests exist in other encodings/representations."
        ),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("EXP-037 read-only native MSF7 digest byte inventory; calibrated:",
          result["raw_sha256_positive_control"])
    for label, evidence in reports.items():
        print(label, "sha256 raw digest occurrence counts:",
              [entry["sha256_digest_raw_occurrences"] for entry in evidence["source_digests"]])

if __name__ == "__main__":
    main()
