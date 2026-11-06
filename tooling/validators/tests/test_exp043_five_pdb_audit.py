"""EXP-043 isolated controls: all five, privacy, missing and divergent PDB inputs."""
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from exp043_five_pdb_audit import (
    COMPONENTS, SLUGS, require_all_five, audit, source_pdb_inventory,
    summarize_native, VerificationError,
)


class FiveProductionPdbTests(unittest.TestCase):
    def test_fixed_expected_component_universe(self):
        self.assertEqual(COMPONENTS, ("Domain", "Application",
                         "Infrastructure.Csv", "Infrastructure.Reporting",
                         "Infrastructure.Xlsx"))
        self.assertEqual(len(set(SLUGS)), 5)
        require_all_five(COMPONENTS)
        with self.assertRaises(VerificationError):
            require_all_five(COMPONENTS[:-1])
        with self.assertRaises(VerificationError):
            require_all_five(tuple(reversed(COMPONENTS)))

    def test_summarize_exposes_no_sensitive_native_keys_or_hashes(self):
        native = {"/src/files/private/location/Secret.cs": {
            "algorithm": "sha256", "digest": b"x" * 32
        }}
        dbi = {"dbi": set(native), "c13": set(native),
               "lines": set(native), "c13_records": 1,
               "c13_algorithm_counts": {"NONE": 1}}
        result = summarize_native(native, dbi)
        self.assertEqual(result["named_native_documents"], 1)
        self.assertEqual(result["native_named_vs_dbi_c13"], "MATCHED")
        self.assertNotIn("private", str(result))
        self.assertNotIn("Secret", str(result))

    def test_dbi_and_named_native_disagreement_not_reported_matched(self):
        result = summarize_native({"/src/files/a": {}},
                {"dbi": {"/src/files/b"}, "c13": {"/src/files/a"},
                 "lines": set(), "c13_records": 1,
                 "c13_algorithm_counts": {}})
        self.assertEqual(result["native_named_vs_dbi_c13"],
                         "UNMATCHED_OR_NOT_INJECTED")

    def test_missing_native_pdb_is_blocked_with_no_path_in_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = audit(Path(tmp)/"private-source-root",
                           Path(tmp)/"private-workroot", "inventory")
        self.assertEqual(len(result["results"]), 5)
        self.assertFalse(result["all_five_verified"])
        self.assertEqual({x["status"] for x in result["results"]},
                         {"BLOCKED"})
        self.assertNotIn(tmp, str(result))

    def test_all_five_requires_all_distinct_candidates_and_producers(self):
        with tempfile.TemporaryDirectory() as tmp:
            app = Path(tmp)/"app"
            evidence = Path(tmp)/"evidence"
            for slug in SLUGS:
                p = (evidence/"exp024" if slug == "csv" else
                     evidence/"remaining"/slug)
                p.mkdir(parents=True)
                (p/"msbuild-diagnostic-private.log").write_text("private",
                                                               encoding="utf-8")
            native = {"/src/files/private/a.cs": {
                "algorithm": "sha256", "digest": hashlib.sha256(b"a").digest()
            }}
            dbi = {"status": "DBI_PARSED", "dbi": set(native),
                   "c13": set(native), "lines": set(),
                   "c13_records": 1, "c13_algorithm_counts": {"NONE": 1}}
            sample = [(Path(tmp)/"private"/"a.cs", b"a", "a.cs")]
            original = {"original_input_sha256_or_sha1_matches": 1,
                        "native_documents_without_captured_input": 0,
                        "origin_categories": {"checked_in": 1},
                        "native_documents_without_line_references": [{}],
                        "native_inventory": "COVERED_BY_CAPTURE"}
            actual = {"effective_csc_source_count": 1,
                      "effective_csc_sources_verification": "MATCHED_INDEPENDENT_TASK_PARAMETER",
                      "structured_csc_task_parameter_evidence": "STRUCTURED_CSC_TASK_INPUT_EVENT",
                      "intermediate_producer": {
                          "producer_status": "VERIFIED_TARGET_EXECUTION_AND_BYTES"},
                      "diagnostic_text_evidence_status": "INCONCLUSIVE"}
            with mock.patch("exp043_five_pdb_audit.source_pdb_inventory",
                            return_value=(native,dbi)), \
                 mock.patch("exp043_five_pdb_audit.read_capture",
                            return_value=(sample, [])), \
                 mock.patch("exp043_five_pdb_audit.verify_native",
                            return_value=original), \
                 mock.patch("exp043_five_pdb_audit.verify_provenance",
                            return_value=actual):
                result = audit(app, evidence, "candidate")
                self.assertTrue(result["all_five_verified"])
                self.assertEqual([x["component"] for x in result["results"]],
                                 list(COMPONENTS))
                self.assertEqual(sum(x["original_bytes_verified"]
                                     for x in result["results"]), 5)
                self.assertNotIn(tmp, str(result))
                downgraded = dict(original, native_inventory="INCOMPLETE")
                with mock.patch("exp043_five_pdb_audit.verify_native",
                                return_value=downgraded):
                    failed = audit(app, evidence, "candidate")
                    self.assertFalse(failed["all_five_verified"])
                    self.assertEqual({x["status"] for x in failed["results"]},
                                     {"INCOMPLETE"})

    def test_non_exception_payload_fails_closed_sanitized(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("exp043_five_pdb_audit.source_pdb_inventory",
                            side_effect=RuntimeError(tmp + "/secret/source.cs")):
                r = audit(Path(tmp), Path(tmp), "inventory")
                self.assertTrue(all(x["failure_category"] ==
                                    "TRUSTED_SYMBOL_AUDIT_FAILED_CLOSED"
                                    for x in r["results"]))
                self.assertNotIn(tmp, str(r))


if __name__ == "__main__":
    unittest.main()
