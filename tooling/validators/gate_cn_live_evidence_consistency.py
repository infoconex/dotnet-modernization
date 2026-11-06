#!/usr/bin/env python3
"""EXP-044 research-only secondary sanity checks of one sanitized live report.

The checker NEVER sees private compiler inputs or PDBs and cannot reproduce
original physical source bytes. The external scope pins a historical run and
expected compiler-input counts; GitHub archive authentication is a separate
CI step. No release-gate authorization is emitted.
"""
import argparse
import json
from pathlib import Path
import re
import sys

from gate_cn_evidence_consistency import EvidenceError, read_json, require, integer

SHA = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
ALGORITHMS = {"NONE", "MD5", "SHA1", "SHA256"}
ROOT = {"schema", "application_repository", "application_commit", "verdict",
        "required_components", "results", "legacy_gate_c",
        "gate_cn_release_acceptance", "source_link_adoption", "not_proven"}
COMPONENT = {"component", "status", "named_native_documents", "dbi_documents",
             "c13_documents", "line_referenced_documents", "c13_checksum_records",
             "c13_algorithm_counts", "native_named_vs_dbi_c13",
             "native_pe_pdb_identity_matched", "original_bytes_verified",
             "actual_csc_sources_verified", "generated_inputs_verified"}
UNPROVEN = (
    "Other source generators, arbitrary compiler layouts or input origins, "
    "application-specific release/consumer acceptance, managed checksum APIs, "
    "Visual Studio/debugger operation, hostile PDB safety, independent "
    "release approval or production adoption"
)


def validate(scope, report):
    require(type(scope) is dict and
            set(scope) == {"schema", "authorization", "application_repository",
                           "application_commit", "component",
                           "expected_native_documents", "expected_tracked_inputs",
                           "expected_generated_inputs", "source_evidence"} and
            scope["schema"] == "gate-cn-exp044-sanitized-scope-v1" and
            scope["authorization"] == "DESIGN_VALIDATION_ONLY" and
            scope["application_repository"] == "infoconex/dotnet-modernization" and
            type(scope["application_commit"]) is str and
            bool(SHA.fullmatch(scope["application_commit"])) and
            scope["component"] == "AnotherLibrary.Core" and
            scope["expected_native_documents"] == 2 and
            scope["expected_tracked_inputs"] == 1 and
            scope["expected_generated_inputs"] == 1,
            "EXP044_EXTERNAL_SCOPE_INVALID")
    evidence = scope["source_evidence"]
    require(type(evidence) is dict and
            set(evidence) == {"run_id", "workflow_id", "executing_research_sha",
                              "artifact_id", "artifact_zip_sha256"} and
            all(integer(evidence.get(k)) and evidence[k] > 0
                for k in ("run_id", "workflow_id", "artifact_id")) and
            type(evidence["executing_research_sha"]) is str and
            evidence["executing_research_sha"] == scope["application_commit"] and
            type(evidence["artifact_zip_sha256"]) is str and
            bool(DIGEST.fullmatch(evidence["artifact_zip_sha256"])),
            "EXP044_HISTORICAL_ARTIFACT_SCOPE_INVALID")
    require(type(report) is dict and set(report) == ROOT and
            report["schema"] == "gate-cn-live-research-result-v1" and
            report["application_repository"] == scope["application_repository"] and
            report["application_commit"] == scope["application_commit"] and
            report["verdict"] == "SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED" and
            report["required_components"] == 1 and
            report["legacy_gate_c"] == "UNSATISFIED" and
            report["gate_cn_release_acceptance"] == "NOT_AUTHORIZED" and
            report["source_link_adoption"] == "HOLD" and
            report["not_proven"] == UNPROVEN,
            "EXP044_REPORT_POLICY_OR_SCHEMA_INVALID")
    results = report["results"]
    require(type(results) is list and len(results) == 1 and
            type(results[0]) is dict and set(results[0]) == COMPONENT,
            "EXP044_COMPONENT_UNIVERSE_INVALID")
    r = results[0]
    expected = scope["expected_native_documents"]
    require(r["component"] == scope["component"] and
            r["status"] == "RESEARCH_VERIFIED" and
            all(integer(r.get(k)) and r[k] == expected for k in (
                "named_native_documents", "dbi_documents", "c13_documents",
                "original_bytes_verified", "actual_csc_sources_verified")) and
            r["generated_inputs_verified"] == scope["expected_generated_inputs"] and
            r["native_pe_pdb_identity_matched"] is True and
            r["native_named_vs_dbi_c13"] == "MATCHED" and
            integer(r.get("line_referenced_documents")) and
            r["line_referenced_documents"] <= expected,
            "EXP044_LIVE_INPUT_OR_DOCUMENT_SCOPE_INCONSISTENT")
    counts = r["c13_algorithm_counts"]
    require(integer(r.get("c13_checksum_records")) and
            r["c13_checksum_records"] >= expected and
            type(counts) is dict and
            set(counts) <= ALGORITHMS and
            all(integer(v) for v in counts.values()) and
            sum(counts.values()) == r["c13_checksum_records"],
            "EXP044_C13_AGGREGATES_INVALID")
    return {
        "verdict": "AGGREGATES_CONSISTENT_RESEARCH_ONLY",
        "application_commit": scope["application_commit"],
        "components": 1,
        "native_document_records": expected,
        "original_bytes_asserted": expected,
        "generated_inputs_asserted": scope["expected_generated_inputs"],
        "legacy_gate_c": "UNSATISFIED",
        "gate_cn_release_acceptance": "NOT_AUTHORIZED",
        "source_link_adoption": "HOLD",
        "warning": "Live original bytes and document identities not independently recomputed from sanitized aggregate JSON",
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--scope", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    try:
        result = validate(read_json(a.scope), read_json(a.report))
        print(json.dumps(result, sort_keys=True))
        return 0
    except EvidenceError as ex:
        print("EXP044_AGGREGATE_RESEARCH_FAIL_CLOSED:", str(ex),
              file=sys.stderr)
        return 2
    except Exception:
        print("EXP044_AGGREGATE_RESEARCH_FAIL_CLOSED: INPUT_OR_RUNTIME_INVALID",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
