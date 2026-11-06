#!/usr/bin/env python3
"""Gate C-N research-only aggregate consistency check; NEVER a release gate.

Accepts sanitized EXP-043 native/managed report JSON plus an *externally
reviewed* pilot scope. Does not recompute any source digest or authenticate
GitHub executions, artifacts, PE/PDB pairs or Csc inputs. It may only emit
AGGREGATES_CONSISTENT_RESEARCH_ONLY or a fixed failure category.
"""
import argparse
import json
from pathlib import Path
import re
import sys


class EvidenceError(Exception):
    """Use fixed string codes only; never propagate source data."""


COMPONENT_NAMES = re.compile(r"^[A-Za-z][A-Za-z0-9.]{0,79}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
NATIVE_ROOT = {
    "experiment", "phase", "scope", "required_components", "all_five_verified",
    "results", "gate_c", "source_link_adoption", "not_proven", "privacy",
}
NATIVE_ITEM = {
    "component", "status", "named_native_documents", "dbi_documents",
    "c13_documents", "line_referenced_documents", "c13_checksum_records",
    "c13_algorithm_counts", "native_named_vs_dbi_c13",
    "captured_original_inputs", "original_bytes_verified",
    "native_missing_original_bytes", "native_origin_categories",
    "no_line_native_documents", "actual_csc_task_source_count",
    "actual_csc_task_source_binding", "structured_event",
    "generated_source_producer", "diagnostic_text_source_observation",
    "native_inventory",
}
MANAGED_ROOT = {
    "experiment", "phase", "results", "all_five_readers_audited",
    "managed_checksum_gate_c", "source_link_adoption", "privacy", "limitation",
}
MANAGED_ITEM = {
    "component", "status", "native_source_documents", "dnlib", "cecil",
    "reader_document_agreement", "reader_documents_subset_of_native",
    "reader_documents_match_native_line_references",
    "native_documents_not_exposed_by_both_readers",
}
READER_COUNTS = {
    "managed_document_count", "managed_document_checksum_exposed",
    "managed_document_checksum_missing",
}
ORIGIN_KEYS = {"checked_in", "intermediate_location_producer_unverified"}
C13_ALGORITHMS = {"NONE", "MD5", "SHA1", "SHA256"}


def require(predicate, code):
    if not predicate:
        raise EvidenceError(code)


def integer(value):
    return type(value) is int and value >= 0


def read_json(path):
    require(path.is_file() and path.stat().st_size <= 128 * 1024,
            "INPUT_MISSING_OR_OVERSIZED")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def bad_constant(_):
        raise EvidenceError("INVALID_JSON_CONSTANT")

    try:
        return json.loads(path.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique,
                          parse_constant=bad_constant)
    except EvidenceError:
        raise
    except (UnicodeError, ValueError):
        raise EvidenceError("INVALID_JSON_ENCODING_OR_SYNTAX") from None


def scope_components(scope):
    require(type(scope) is dict and scope.get("schema") ==
            "gate-cn-research-scope-v1", "SCOPE_SCHEMA_INVALID")
    require(scope.get("authorization") == "DESIGN_VALIDATION_ONLY",
            "SCOPE_APPROVAL_INVALID")
    require(type(scope.get("application_repository")) is str and
            bool(scope["application_repository"]) and
            type(scope.get("application_commit")) is str and
            bool(SHA.fullmatch(scope["application_commit"])),
            "SCOPE_APPLICATION_IDENTITY_INVALID")
    evidence = scope.get("source_evidence")
    require(type(evidence) is dict and
            integer(evidence.get("run_id")) and evidence["run_id"] > 0 and
            integer(evidence.get("artifact_id")) and evidence["artifact_id"] > 0 and
            type(evidence.get("artifact_zip_sha256")) is str and
            bool(DIGEST.fullmatch(evidence["artifact_zip_sha256"])) and
            type(evidence.get("executing_research_sha")) is str and
            bool(SHA.fullmatch(evidence["executing_research_sha"])),
            "SCOPE_EVIDENCE_LOCATORS_INVALID")
    items = scope.get("required_components")
    require(type(items) is list and bool(items) and len(items) <= 128,
            "SCOPE_COMPONENTS_INVALID")
    expected = {}
    for item in items:
        require(type(item) is dict and
                set(item) == {"component", "expected_native_documents",
                              "expected_generated_inputs", "expected_line_documents",
                              "expected_c13_records", "expected_c13_algorithms"},
                "SCOPE_COMPONENT_INVALID")
        name = item["component"]
        require(type(name) is str and bool(COMPONENT_NAMES.fullmatch(name)) and
                name not in expected and
                integer(item["expected_native_documents"]) and
                item["expected_native_documents"] > 0 and
                integer(item["expected_generated_inputs"]) and
                item["expected_generated_inputs"] <= item["expected_native_documents"] and
                integer(item["expected_line_documents"]) and
                item["expected_line_documents"] <= item["expected_native_documents"] and
                integer(item["expected_c13_records"]) and
                item["expected_c13_records"] >= item["expected_native_documents"] and
                type(item["expected_c13_algorithms"]) is dict and
                set(item["expected_c13_algorithms"]) <= C13_ALGORITHMS and
                all(integer(v) for v in item["expected_c13_algorithms"].values()) and
                sum(item["expected_c13_algorithms"].values()) == item["expected_c13_records"],
                "SCOPE_COMPONENT_INVALID")
        expected[name] = item
    return expected


def component_map(report, expected, allowed_root, allowed_item, invalid):
    require(type(report) is dict and set(report) == allowed_root, invalid)
    items = report.get("results")
    require(type(items) is list and len(items) == len(expected), invalid)
    by_name = {}
    for item in items:
        require(type(item) is dict and set(item) == allowed_item, invalid)
        name = item.get("component")
        require(type(name) is str and name in expected and name not in by_name,
                invalid)
        by_name[name] = item
    require(set(by_name) == set(expected), invalid)
    return by_name


def validate(scope, native, managed):
    """Secondary aggregation check. No live compiler/PDB provenance is rederived."""
    expected = scope_components(scope)
    require(native.get("experiment") == "EXP-043" and
            native.get("phase") == "candidate" and
            native.get("scope") ==
            "all five frozen trusted Windows net48 candidate production PDBs" and
            native.get("gate_c") == "UNSATISFIED" and
            native.get("source_link_adoption") == "HOLD" and
            native.get("all_five_verified") is True and
            integer(native.get("required_components")) and
            native["required_components"] == len(expected),
            "NATIVE_REPORT_POLICY_OR_PHASE_INVALID")
    require(managed.get("experiment") == "EXP-043" and
            managed.get("phase") == "two_pinned_managed_reader_exposure" and
            managed.get("all_five_readers_audited") is True and
            managed.get("managed_checksum_gate_c") == "UNSATISFIED" and
            managed.get("source_link_adoption") == "HOLD",
            "MANAGED_REPORT_POLICY_OR_PHASE_INVALID")
    nr = component_map(native, expected, NATIVE_ROOT, NATIVE_ITEM,
                       "NATIVE_COMPONENT_UNIVERSE_INVALID")
    mr = component_map(managed, expected, MANAGED_ROOT, MANAGED_ITEM,
                       "MANAGED_COMPONENT_UNIVERSE_INVALID")
    total_native = total_managed = total_checked_in = total_generated = 0
    for name in expected:
        n, m, rule = nr[name], mr[name], expected[name]
        count = rule["expected_native_documents"]
        keys = ("named_native_documents", "dbi_documents", "c13_documents",
                "captured_original_inputs", "original_bytes_verified",
                "actual_csc_task_source_count")
        require(all(integer(n.get(k)) and n[k] == count for k in keys) and
                n.get("status") == "VERIFIED" and
                n.get("native_inventory") == "COVERED_BY_CAPTURE" and
                n.get("native_named_vs_dbi_c13") == "MATCHED" and
                n.get("actual_csc_task_source_binding") ==
                    "MATCHED_INDEPENDENT_TASK_PARAMETER" and
                n.get("structured_event") == "STRUCTURED_CSC_TASK_INPUT_EVENT" and
                n.get("generated_source_producer") ==
                    "VERIFIED_TARGET_EXECUTION_AND_BYTES" and
                n.get("native_missing_original_bytes") == 0,
                "NATIVE_COMPONENT_PROVENANCE_INCONSISTENT")
        require(integer(n.get("line_referenced_documents")) and
                integer(n.get("no_line_native_documents")) and
                n["line_referenced_documents"] + n["no_line_native_documents"] == count and
                n["line_referenced_documents"] == rule["expected_line_documents"],
                "NATIVE_LINE_DOCUMENT_COUNTS_INVALID")
        origins = n.get("native_origin_categories")
        require(type(origins) is dict and set(origins) <= ORIGIN_KEYS and
                all(integer(v) for v in origins.values()) and
                sum(origins.values()) == count and
                origins.get("intermediate_location_producer_unverified", 0) ==
                    rule["expected_generated_inputs"] and
                origins.get("checked_in", 0) ==
                    count - rule["expected_generated_inputs"],
                "NATIVE_SOURCE_ORIGIN_COUNTS_INVALID")
        algorithms = n.get("c13_algorithm_counts")
        require(type(algorithms) is dict and set(algorithms) <= C13_ALGORITHMS and
                all(integer(v) for v in algorithms.values()) and
                integer(n.get("c13_checksum_records")) and
                sum(algorithms.values()) == n["c13_checksum_records"] and
                n["c13_checksum_records"] == rule["expected_c13_records"] and
                algorithms == rule["expected_c13_algorithms"],
                "C13_RECORD_COUNTS_INVALID")
        require(m.get("status") == "VERIFIED_READER_LIMITATION" and
                m.get("reader_document_agreement") == "MATCHED" and
                m.get("reader_documents_subset_of_native") is True and
                m.get("reader_documents_match_native_line_references") is True and
                integer(m.get("native_source_documents")) and
                m["native_source_documents"] == count and
                integer(m.get("native_documents_not_exposed_by_both_readers")) and
                m["native_documents_not_exposed_by_both_readers"] ==
                    n["no_line_native_documents"],
                "MANAGED_NATIVE_IDENTITY_ASSERTION_INVALID")
        for reader in ("dnlib", "cecil"):
            vals = m.get(reader)
            require(type(vals) is dict and set(vals) == READER_COUNTS and
                    all(integer(v) for v in vals.values()) and
                    vals["managed_document_count"] ==
                        n["line_referenced_documents"] and
                    vals["managed_document_checksum_exposed"] +
                        vals["managed_document_checksum_missing"] ==
                        vals["managed_document_count"],
                    "MANAGED_READER_COUNTS_INVALID")
        require(m["dnlib"] == m["cecil"], "MANAGED_READER_AGGREGATE_DISAGREEMENT")
        total_native += count
        total_managed += n["line_referenced_documents"]
        total_generated += rule["expected_generated_inputs"]
        total_checked_in += count - rule["expected_generated_inputs"]
    return {
        "verdict": "AGGREGATES_CONSISTENT_RESEARCH_ONLY",
        "native_document_records": total_native,
        "managed_line_documents": total_managed,
        "tracked_compiler_inputs": total_checked_in,
        "generated_compiler_inputs": total_generated,
        "components": len(expected),
        "legacy_gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "gate_cn_release_acceptance": "NOT_AUTHORIZED",
        "warning": "Report assertions only: original source bytes, identities, artifact and GitHub execution are NOT independently authenticated by this checker",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scope", required=True, type=Path)
    p.add_argument("--native-report", required=True, type=Path)
    p.add_argument("--managed-report", required=True, type=Path)
    args = p.parse_args()
    try:
        result = validate(read_json(args.scope), read_json(args.native_report),
                          read_json(args.managed_report))
        print(json.dumps(result, sort_keys=True))
    except EvidenceError as ex:
        print("GATE_CN_RESEARCH_FAIL_CLOSED:", str(ex), file=sys.stderr)
        return 2
    except Exception:
        print("GATE_CN_RESEARCH_FAIL_CLOSED: INPUT_OR_RUNTIME_INVALID",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
