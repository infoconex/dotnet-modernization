#!/usr/bin/env python3
"""EXP-043: sanitized five-assembly native-PDB and actual Csc source audit.

Only locally built, trusted native PDBs. Never treat document keys as disk
paths. Never publish raw original paths, source bytes, compiler arguments,
PDBs or digest values. Input and output paths supplied by trusted workflow.
"""
import argparse
import json
from pathlib import Path
import sys

from classic_pdb_document_checksums import VerificationError, normalized_key, parse_injected_source
from native_windows_pdb_sourcelink import read_msf, parse_named_streams, read_pe_codeview
from native_pdb_document_inventory import dbi_source_inventory
from exp041_compiler_input_audit import read_capture, verify as verify_native
from exp042_source_provenance import verify_provenance

COMPONENTS = (
    "Domain", "Application", "Infrastructure.Csv",
    "Infrastructure.Reporting", "Infrastructure.Xlsx",
)
SLUGS = ("domain", "application", "csv", "reporting", "xlsx")


def source_pdb_inventory(dll, pdb):
    streams = read_msf(pdb.read_bytes())
    guid, age, named = parse_named_streams(streams[1], len(streams))
    if read_pe_codeview(dll.read_bytes()) != (guid, age):
        raise VerificationError("NATIVE_PE_PDB_IDENTITY_MISMATCH")
    native = {}
    for name, stream_id in named.items():
        if normalized_key(name).startswith("/src/files/"):
            key = normalized_key(name)
            if key in native or not (0 <= stream_id < len(streams)):
                raise VerificationError("DUPLICATE_OR_OUT_OF_RANGE_NATIVE_SOURCE")
            native[key] = parse_injected_source(streams[stream_id])
    dbi = dbi_source_inventory(streams, named)
    if dbi["status"] != "DBI_PARSED":
        raise VerificationError("DBI_UNAVAILABLE")
    return native, dbi


def sanitize_error(ex):
    # Never pass arbitrary exceptions; e.g., OS errors may include source paths.
    return str(ex) if isinstance(ex, VerificationError) else "TRUSTED_SYMBOL_AUDIT_FAILED_CLOSED"


def summarize_native(native, dbi):
    return {
        "named_native_documents": len(native),
        "dbi_documents": len(dbi["dbi"]),
        "c13_documents": len(dbi["c13"]),
        "line_referenced_documents": len(dbi["lines"]),
        "c13_checksum_records": dbi["c13_records"],
        "c13_algorithm_counts": dbi["c13_algorithm_counts"],
        "native_named_vs_dbi_c13": (
            "MATCHED" if set(native) == dbi["dbi"] == dbi["c13"]
            else "UNMATCHED_OR_NOT_INJECTED"
        ),
    }


def require_all_five(items):
    if tuple(items) != COMPONENTS:
        raise VerificationError("ALL_FIVE_PRODUCTION_COMPONENTS_REQUIRED")


def audit(app, evidence, phase):
    results = []
    require_all_five(COMPONENTS)
    for component, slug in zip(COMPONENTS, SLUGS):
        name = "RecordSift." + component
        project = app / "src" / name
        dll = project / "bin" / "Release" / (name + ".dll")
        pdb = project / "bin" / "Release" / (name + ".pdb")
        item = {"component": component, "status": "INCOMPLETE"}
        try:
            native, dbi = source_pdb_inventory(dll, pdb)
            item.update(summarize_native(native, dbi))
            if phase == "inventory":
                item["status"] = "INVENTORIED_ONLY"
            else:
                private = (evidence / "exp024" if slug == "csv" else
                           evidence / "remaining" / slug)
                capture = (private / "exp041-original-inputs-private"
                           if slug == "csv" else private / "source-inputs-private")
                producer = Path(str(capture) + "-producer")
                records, _ = read_capture(capture)
                native_result = verify_native(native, dbi, records, app)
                provenance = verify_provenance(
                    records,
                    private / "msbuild-preprocessed.xml",
                    (private / "msbuild-diagnostic-private.log").read_text(encoding="utf-8-sig", errors="replace"),
                    producer, project,
                    (private / "exp042-csc-parameters-private.tsv"),
                )
                item["captured_original_inputs"] = len(records)
                item["original_bytes_verified"] = native_result["original_input_sha256_or_sha1_matches"]
                item["native_missing_original_bytes"] = native_result["native_documents_without_captured_input"]
                item["native_origin_categories"] = native_result["origin_categories"]
                item["no_line_native_documents"] = len(native_result["native_documents_without_line_references"])
                item["actual_csc_task_source_count"] = provenance["effective_csc_source_count"]
                item["actual_csc_task_source_binding"] = provenance["effective_csc_sources_verification"]
                item["structured_event"] = provenance["structured_csc_task_parameter_evidence"]
                item["generated_source_producer"] = provenance["intermediate_producer"]["producer_status"]
                item["diagnostic_text_source_observation"] = provenance["diagnostic_text_evidence_status"]
                item["native_inventory"] = native_result["native_inventory"]
                item["status"] = (
                    "VERIFIED" if native_result["native_inventory"] == "COVERED_BY_CAPTURE"
                    and provenance["effective_csc_sources_verification"] ==
                        "MATCHED_INDEPENDENT_TASK_PARAMETER"
                    and provenance["intermediate_producer"]["producer_status"] ==
                        "VERIFIED_TARGET_EXECUTION_AND_BYTES"
                    else "INCOMPLETE"
                )
        except Exception as ex:
            item["status"] = "BLOCKED"
            item["failure_category"] = sanitize_error(ex)
        results.append(item)
    return {
        "experiment": "EXP-043",
        "phase": phase,
        "scope": ("EXP024 candidate CSV plus four original baseline PDBs, read-only" if phase == "inventory" else "all five frozen trusted Windows net48 candidate production PDBs"),
        "required_components": len(COMPONENTS),
        "all_five_verified": phase == "candidate" and all(
            x["status"] == "VERIFIED" for x in results),
        "results": results,
        "gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "not_proven": [
            "existing managed-reader checksum Gate C",
            "authentic Visual Studio Package Manager project installation",
            "live debugger source stepping",
            "hostile or arbitrary PDB parsing safety",
        ],
        "privacy": "fixed public component labels and aggregate numbers only; no original paths, source bytes, PDB contents, private command lines, or digests",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--app-root", required=True, type=Path)
    p.add_argument("--evidence-root", required=True, type=Path)
    p.add_argument("--phase", choices=("inventory", "candidate"), required=True)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    try:
        if args.output.exists():
            raise VerificationError("SANITIZED_OUTPUT_ALREADY_EXISTS")
        result = audit(args.app_root, args.evidence_root, args.phase)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
        print("EXP043", args.phase, "five production PDBs:",
              ", ".join(x["component"] + "=" + x["status"] for x in result["results"]),
              "Gate C UNSATISFIED; Source Link HOLD")
        if args.phase == "candidate" and not result["all_five_verified"]:
            sys.exit(2)
        if any(x["status"] == "BLOCKED" for x in result["results"]):
            sys.exit(2)
    except Exception as ex:
        print("EXP043 FAIL CLOSED:", sanitize_error(ex), file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
