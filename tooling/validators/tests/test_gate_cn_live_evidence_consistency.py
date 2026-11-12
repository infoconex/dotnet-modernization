"""EXP-044 immutable sanitized report replay controls, not PDB authentication."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate_cn_evidence_consistency import EvidenceError, read_json
from gate_cn_live_evidence_consistency import validate, UNPROVEN

ROOT = Path(__file__).resolve().parents[3]
SCOPE_PATH = (ROOT / "research/native-pdb-provenance/gate-cn/"
              "gate-cn-exp044-evidence-scope.json")


def fixture():
    scope = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    report = {
        "schema": "gate-cn-live-research-result-v1",
        "application_repository": scope["application_repository"],
        "application_commit": scope["application_commit"],
        "verdict": "SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED",
        "required_components": 1,
        "results": [{
            "component": "AnotherLibrary.Core",
            "status": "RESEARCH_VERIFIED",
            "named_native_documents": 2,
            "dbi_documents": 2,
            "c13_documents": 2,
            "line_referenced_documents": 1,
            "c13_checksum_records": 2,
            "c13_algorithm_counts": {"NONE": 2},
            "native_named_vs_dbi_c13": "MATCHED",
            "native_pe_pdb_identity_matched": True,
            "original_bytes_verified": 2,
            "actual_csc_sources_verified": 2,
            "generated_inputs_verified": 1,
        }],
        "legacy_gate_c": "UNSATISFIED",
        "gate_cn_release_acceptance": "NOT_AUTHORIZED",
        "source_link_adoption": "HOLD",
        "not_proven": UNPROVEN,
    }
    return scope, report


class EXP044SanitizedEvidenceTests(unittest.TestCase):
    def test_positive_report_remains_research_only(self):
        scope, report = fixture()
        result = validate(scope, report)
        self.assertEqual(result["verdict"], "AGGREGATES_CONSISTENT_RESEARCH_ONLY")
        self.assertEqual(result["original_bytes_asserted"], 2)
        self.assertEqual(result["gate_cn_release_acceptance"], "NOT_AUTHORIZED")
        self.assertEqual(result["legacy_gate_c"], "UNSATISFIED")

    def fail_mutation(self, fn):
        scope, report = fixture()
        fn(scope, report)
        with self.assertRaises(EvidenceError):
            validate(scope, report)

    def test_missing_or_duplicate_component(self):
        self.fail_mutation(lambda s,r: r.update(results=[]))
        self.fail_mutation(lambda s,r: r["results"].append(copy.deepcopy(r["results"][0])))

    def test_compiler_count_forgery(self):
        self.fail_mutation(lambda s,r: r["results"][0].update(actual_csc_sources_verified=1))
        self.fail_mutation(lambda s,r: r["results"][0].update(original_bytes_verified=1))

    def test_wrong_native_dbi_or_c13_universe(self):
        self.fail_mutation(lambda s,r: r["results"][0].update(dbi_documents=1))
        self.fail_mutation(lambda s,r: r["results"][0].update(c13_documents=1))
        self.fail_mutation(lambda s,r: r["results"][0].update(native_named_vs_dbi_c13="UNMATCHED"))

    def test_wrong_repository_or_executing_commit(self):
        self.fail_mutation(lambda s,r: r.update(application_commit="0" * 40))
        self.fail_mutation(lambda s,r: r.update(application_repository="other/repo"))
        self.fail_mutation(lambda s,r: s["source_evidence"].update(executing_research_sha="0"*40))

    def test_wrong_artifact_identity_format(self):
        self.fail_mutation(lambda s,r: s["source_evidence"].update(artifact_id=0))
        self.fail_mutation(lambda s,r: s["source_evidence"].update(artifact_zip_sha256="X"*64))
        self.fail_mutation(lambda s,r: s["source_evidence"].update(workflow_id="not-an-id"))
        self.fail_mutation(lambda s,r: s["source_evidence"].update(sanitized_json_sha256="bad"))

    def test_wrong_generator_or_missing_pe_pair(self):
        self.fail_mutation(lambda s,r: r["results"][0].update(generated_inputs_verified=0))
        self.fail_mutation(lambda s,r: r["results"][0].update(native_pe_pdb_identity_matched=False))

    def test_c13_impossible_count_or_algorithm(self):
        self.fail_mutation(lambda s,r: r["results"][0].update(c13_checksum_records=1))
        self.fail_mutation(lambda s,r: r["results"][0].update(c13_algorithm_counts={"SHA512":2}))
        self.fail_mutation(lambda s,r: r["results"][0].update(line_referenced_documents=3))

    def test_policy_promotion_and_missing_nonclaims(self):
        self.fail_mutation(lambda s,r: r.update(gate_cn_release_acceptance="APPROVED"))
        self.fail_mutation(lambda s,r: r.update(source_link_adoption="GO"))
        self.fail_mutation(lambda s,r: r.update(not_proven=""))

    def test_unauthorized_free_text_field(self):
        self.fail_mutation(lambda s,r: r["results"][0].update(source_path="C:/private.cs"))
        self.fail_mutation(lambda s,r: r.update(private_diagnostic="C:/private.cs"))

    def test_bool_not_valid_count(self):
        self.fail_mutation(lambda s,r: r["results"][0].update(original_bytes_verified=True))
        self.fail_mutation(lambda s,r: r.update(required_components=True))

    def test_duplicate_json_key_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/"corrupt.json"
            path.write_text('{"a":1,"a":2}',encoding="utf-8")
            with self.assertRaises(EvidenceError):
                read_json(path)
            path.write_text('{"a": NaN}',encoding="utf-8")
            with self.assertRaises(EvidenceError):
                read_json(path)


if __name__ == "__main__":
    unittest.main()
