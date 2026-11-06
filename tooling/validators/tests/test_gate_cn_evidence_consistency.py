"""Synthetic, independent fail-closed controls for *secondary* Gate C-N reports.

These controls do NOT validate a physical PDB or original compiler-source bytes.
"""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stderr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate_cn_evidence_consistency import (EvidenceError, read_json, validate,
                                          scope_components, main)

REPO = Path(__file__).resolve().parents[3]
SCOPE_PATH = (REPO / "projects/recordsift/evaluations/2026-11-pre-sdk/"
              "gate-cn-recordsift-scope.json")


def fixture():
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    native = {
        "experiment": "EXP-043", "phase": "candidate",
        "scope": "all five frozen trusted Windows net48 candidate production PDBs",
        "required_components": len(scope["required_components"]),
        "all_five_verified": True, "results": [], "gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "not_proven": [
            "existing managed-reader checksum Gate C",
            "authentic Visual Studio Package Manager project installation",
            "live debugger source stepping",
            "hostile or arbitrary PDB parsing safety",
        ],
        "privacy": ("fixed public component labels and aggregate numbers only; "
                    "no original paths, source bytes, PDB contents, private "
                    "command lines, or digests"),
    }
    managed = {
        "experiment": "EXP-043", "phase": "two_pinned_managed_reader_exposure",
        "all_five_readers_audited": True, "results": [],
        "managed_checksum_gate_c": "UNSATISFIED",
        "source_link_adoption": "HOLD",
        "privacy": ("only native/managed counts, checksum exposure counts and "
                    "fixed categories; source names, URLs, hashes, PDBs and "
                    "private stdout never uploaded"),
        "limitation": ("dnlib and Cecil managed reader API exposure is not a "
                       "complete native document inventory or authentic debugger operation"),
    }
    for s in scope["required_components"]:
        count = s["expected_native_documents"]
        generated = s["expected_generated_inputs"]
        lines = s["expected_line_documents"]
        nonline = count - lines
        c13_records = s["expected_c13_records"]
        native["results"].append({
            "component": s["component"], "status": "VERIFIED",
            "named_native_documents": count, "dbi_documents": count,
            "c13_documents": count, "line_referenced_documents": lines,
            "c13_checksum_records": c13_records,
            "c13_algorithm_counts": copy.deepcopy(s["expected_c13_algorithms"]),
            "native_named_vs_dbi_c13": "MATCHED",
            "captured_original_inputs": count, "original_bytes_verified": count,
            "native_missing_original_bytes": 0,
            "native_origin_categories": {"checked_in": count - generated,
                                         "intermediate_location_producer_unverified": generated},
            "no_line_native_documents": nonline,
            "actual_csc_task_source_count": count,
            "actual_csc_task_source_binding": "MATCHED_INDEPENDENT_TASK_PARAMETER",
            "structured_event": "STRUCTURED_CSC_TASK_INPUT_EVENT",
            "generated_source_producer": "VERIFIED_TARGET_EXECUTION_AND_BYTES",
            "diagnostic_text_source_observation": "INCONCLUSIVE",
            "native_inventory": "COVERED_BY_CAPTURE",
        })
        probe = {
            "managed_document_count": lines,
            "managed_document_checksum_exposed": s["expected_managed_checksum_exposed"],
            "managed_document_checksum_missing": lines - s["expected_managed_checksum_exposed"],
        }
        managed["results"].append({
            "component": s["component"], "status": "VERIFIED_READER_LIMITATION",
            "native_source_documents": count,
            "dnlib": copy.deepcopy(probe), "cecil": copy.deepcopy(probe),
            "reader_document_agreement": "MATCHED",
            "reader_documents_subset_of_native": True,
            "reader_documents_match_native_line_references": True,
            "native_documents_not_exposed_by_both_readers": nonline,
        })
    return scope, native, managed


class GateCNResearchConsistencyTests(unittest.TestCase):
    def test_external_scope_is_complete_and_frozen(self):
        scope, _, _ = fixture()
        names = scope_components(scope)
        self.assertEqual(tuple(names), ("Domain", "Application", "Infrastructure.Csv",
                                         "Infrastructure.Reporting", "Infrastructure.Xlsx"))
        self.assertEqual(scope["application_commit"],
                         "8358780829458854a4b0356df5ac5e685f0a34c8")
        self.assertEqual(scope["source_evidence"]["workflow_id"], 408976399)
        self.assertTrue(all(x["expected_managed_checksum_exposed"] == 0
                            for x in scope["required_components"]))

    def test_consistent_synthetic_aggregates_are_never_a_release_pass(self):
        scope, n, m = fixture()
        actual = validate(scope, n, m)
        self.assertEqual(actual["verdict"], "AGGREGATES_CONSISTENT_RESEARCH_ONLY")
        self.assertEqual(actual["native_document_records"], 64)
        self.assertEqual(actual["generated_compiler_inputs"], 5)
        self.assertEqual(actual["managed_line_documents"], 46)
        self.assertEqual(actual["legacy_gate_c"], "UNSATISFIED")
        self.assertEqual(actual["gate_cn_release_acceptance"], "NOT_AUTHORIZED")
        self.assertEqual(actual["source_link_adoption"], "HOLD")

    def assert_invalid(self, change):
        scope, n, m = fixture()
        change(scope, n, m)
        with self.assertRaises(EvidenceError):
            validate(scope, n, m)

    def test_missing_project_fails(self):
        self.assert_invalid(lambda s, n, m: n["results"].pop())

    def test_duplicate_project_does_not_hide_missing_project(self):
        self.assert_invalid(lambda s, n, m: n["results"].__setitem__(1, n["results"][0]))

    def test_unapproved_scope_is_rejected(self):
        self.assert_invalid(lambda s, n, m: s.update(authorization="RELEASE_APPROVED"))

    def test_manifest_only_self_reported_universe_cannot_shrink(self):
        self.assert_invalid(lambda s, n, m: s["required_components"].pop())

    def test_managed_reader_exact_line_key_assertion_required(self):
        self.assert_invalid(lambda s, n, m:
                            m["results"][0].update(reader_documents_match_native_line_references=False))

    def test_native_line_count_change_conflicting_with_external_scope_rejected(self):
        def mutate(s, n, m):
            # This mutates counts; it does NOT verify same-count source identities.
            n["results"][0]["line_referenced_documents"] -= 1
            n["results"][0]["no_line_native_documents"] += 1
        self.assert_invalid(mutate)

    def test_coordinated_line_count_change_conflicting_with_scope_rejected(self):
        def mutate(s, n, m):
            original = n["results"][0]["line_referenced_documents"]
            n["results"][0]["line_referenced_documents"] = original - 1
            n["results"][0]["no_line_native_documents"] += 1
            m["results"][0]["native_documents_not_exposed_by_both_readers"] += 1
            for reader in ("dnlib", "cecil"):
                m["results"][0][reader]["managed_document_count"] -= 1
                m["results"][0][reader]["managed_document_checksum_missing"] -= 1
        self.assert_invalid(mutate)

    def test_equal_c13_algorithm_arithmetic_but_wrong_frozen_counts_rejected(self):
        def mutate(s, n, m):
            n["results"][0]["c13_checksum_records"] += 1
            n["results"][0]["c13_algorithm_counts"]["NONE"] += 1
        self.assert_invalid(mutate)

    def test_corrupted_csc_input_count_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0].update(actual_csc_task_source_count=23))

    def test_original_bytes_incomplete_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0].update(original_bytes_verified=23))

    def test_missing_producer_attestation_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0].update(generated_source_producer="UNKNOWN"))

    def test_origin_count_mismatch_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0]["native_origin_categories"].update(checked_in=999))

    def test_false_native_dbi_c13_equality_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0].update(native_named_vs_dbi_c13="UNMATCHED"))

    def test_c13_algorithm_count_mismatch_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0]["c13_algorithm_counts"].update(NONE=999))

    def test_none_is_count_not_document_hash(self):
        scope, n, m = fixture()
        self.assertEqual(validate(scope, n, m)["verdict"],
                         "AGGREGATES_CONSISTENT_RESEARCH_ONLY")
        n["results"][0]["c13_algorithm_counts"] = {"SHA512": 28}
        with self.assertRaises(EvidenceError):
            validate(scope, n, m)

    def test_checksum_count_cannot_be_boolean(self):
        self.assert_invalid(lambda s, n, m:
                            m["results"][0]["dnlib"].update(managed_document_checksum_exposed=True))

    def test_managed_reader_disagreement_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            m["results"][0]["cecil"].update(managed_document_checksum_exposed=1,
                                                               managed_document_checksum_missing=22))

    def test_both_reader_checksum_exposure_counts_cannot_be_coordinately_forged(self):
        def mutate(s, n, m):
            for reader in ("dnlib", "cecil"):
                m["results"][0][reader]["managed_document_checksum_exposed"] = 1
                m["results"][0][reader]["managed_document_checksum_missing"] -= 1
        self.assert_invalid(mutate)

    def test_original_scope_rejects_missing_checksum_expectation(self):
        self.assert_invalid(lambda s, n, m:
                            s["required_components"][0].pop("expected_managed_checksum_exposed"))

    def test_free_text_privacy_disclosure_rejected(self):
        self.assert_invalid(lambda s, n, m: n.update(privacy="C:/private/source.cs"))
        self.assert_invalid(lambda s, n, m: m.update(limitation="C:/private/source.cs"))
        self.assert_invalid(lambda s, n, m:
                            n["results"][0].update(diagnostic_text_source_observation="C:/private"))

    def test_stated_unproven_gates_cannot_be_removed(self):
        self.assert_invalid(lambda s, n, m: n.update(not_proven=[]))

    def test_gate_c_policy_cannot_be_silently_promoted(self):
        self.assert_invalid(lambda s, n, m: n.update(gate_c="SATISFIED"))
        self.assert_invalid(lambda s, n, m: m.update(source_link_adoption="GO"))

    def test_extra_sensitive_field_rejected_by_allowlist(self):
        self.assert_invalid(lambda s, n, m:
                            n["results"][0].update(original_source_path="C:/secrets/private.cs"))

    def test_duplicate_json_keys_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "bad.json"
            path.write_text('{"results": [], "results": []}', encoding="utf-8")
            with self.assertRaises(EvidenceError):
                read_json(path)

    def test_unknown_native_evidence_field_fails_closed(self):
        self.assert_invalid(lambda s, n, m:
                            n.update(private_symbol_bytes="SENSITIVE"))

    def test_missing_executing_sha_locator_rejected(self):
        self.assert_invalid(lambda s, n, m:
                            s["source_evidence"].update(executing_research_sha=""))

    def test_cli_outputs_only_fixed_success_or_error_codes(self):
        scope, n, m = fixture()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name, obj in (("scope.json", scope), ("n.json", n), ("m.json", m)):
                (root / name).write_text(json.dumps(obj), encoding="utf-8")
            argv = ["gate_cn_evidence_consistency.py", "--scope", str(root/"scope.json"),
                    "--native-report", str(root/"n.json"),
                    "--managed-report", str(root/"m.json")]
            original = sys.argv
            try:
                sys.argv = argv
                # main writes sanitized categories; never a release approval.
                with io.StringIO() as out:
                    from contextlib import redirect_stdout
                    with redirect_stdout(out):
                        self.assertEqual(main(), 0)
                    self.assertIn("AGGREGATES_CONSISTENT_RESEARCH_ONLY", out.getvalue())
                n["results"][0]["status"] = "BLOCKED"
                (root / "n.json").write_text(json.dumps(n), encoding="utf-8")
                with redirect_stderr(io.StringIO()) as err:
                    self.assertEqual(main(), 2)
                    self.assertIn("GATE_CN_RESEARCH_FAIL_CLOSED", err.getvalue())
                    self.assertNotIn(td, err.getvalue())
            finally:
                sys.argv = original


if __name__ == "__main__":
    unittest.main()
