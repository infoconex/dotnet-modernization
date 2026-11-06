"""Non-RecordSift synthetic controls for Gate C-N's narrow live adapter.

Native PE/PDB file parsing is intentionally mocked here; actual original-byte
hashes, private snapshots, producer and structured Csc checks are exercised.
EXP-043 retains the separate real native-PDB parser and compatibility proof.
"""
import base64
import copy
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from classic_pdb_document_checksums import VerificationError, source_key
from gate_cn_live_provenance import (load_manifest, validate_manifest, inside,
                                     run, run_component, verify_roots)

APPLICATION_SHA = "8358780829458854a4b0356df5ac5e685f0a34c8"


def manifest():
    return {
        "schema": "gate-cn-live-manifest-v1",
        "authorization": "DESIGN_VALIDATION_ONLY",
        "application_repository": "example/NonRecordSift",
        "application_commit": APPLICATION_SHA,
        "components": [{
            "component": "AnotherLibrary.Core",
            "project_dir": "src/AnotherLibrary.Core",
            "assembly_name": "AnotherLibrary.Core",
            "evidence_dir": "capture/independent-core",
            "capture_dir": "source-inputs-private",
            "expected_native_documents": 2,
            "expected_tracked_inputs": 1,
            "expected_generated_inputs": 1,
            "producer_contract": "EXP042_MONIKER_ONE_PER_COMPONENT",
        }],
    }


class SyntheticLiveFixture:
    def __init__(self, root):
        self.root = root
        self.app = root / "app"
        self.evidence = root / "evidence"
        self.project = self.app / "src" / "AnotherLibrary.Core"
        self.private = self.evidence / "capture" / "independent-core"
        self.capture = self.private / "source-inputs-private"
        self.producer = self.private / "source-inputs-private-producer"
        for directory in (self.capture, self.producer,
                          self.project / "obj" / "Release",
                          self.project / "bin" / "Release"):
            directory.mkdir(parents=True)
        (self.project / "bin" / "Release" /
         "AnotherLibrary.Core.dll").write_bytes(b"FAKE_TRUSTED_PE_FOR_MOCK_ONLY")
        (self.project / "bin" / "Release" /
         "AnotherLibrary.Core.pdb").write_bytes(b"FAKE_TRUSTED_PDB_FOR_MOCK_ONLY")
        self.tracked = self.project / "Tracked.cs"
        self.generated = (self.project / "obj" / "Release" /
                          "Framework.AssemblyAttributes.cs")
        self.inputs = [
            (self.tracked, b"public class Tracked {}\r\n"),
            (self.generated, b"[assembly:System.Runtime.Versioning.TargetFramework(\"v4.8\")]\r\n"),
        ]
        rows = ["PATHMAP\t"]
        for i, (path, raw) in enumerate(self.inputs):
            path.write_bytes(raw)
            (self.capture / ("input-%04d.bin" % i)).write_bytes(raw)
            encoded = base64.b64encode(str(path).encode("utf-8")).decode("ascii")
            rows.append(str(i) + "\t" + encoded + "\t" +
                        hashlib.sha256(raw).hexdigest())
        (self.capture / "input-manifest.tsv").write_text(
            "\n".join(rows) + "\n", encoding="ascii")
        (self.private / "msbuild-preprocessed.xml").write_text(
            '<Project><Target Name="CoreCompile"><Csc Sources="@(Compile)" />'
            '</Target></Project>', encoding="utf-8")
        (self.private / "msbuild-diagnostic-private.log").write_text(
            'Target "GenerateTargetFrameworkMonikerAttribute" in file "X":\n'
            ' Task "WriteLinesToFile"\n'
            ' Done building target "GenerateTargetFrameworkMonikerAttribute"\n',
            encoding="utf-8")
        events = ["STATUS\tCSC_TASK_PARAMETER_EVENT", "COUNT\t2"]
        events += [base64.b64encode(str(p).encode("utf-8")).decode("ascii")
                   for p, _ in self.inputs]
        (self.private / "exp042-csc-parameters-private.tsv").write_text(
            "\n".join(events) + "\n", encoding="ascii")
        (self.producer / "producer-before.flag").write_bytes(b"PREPARED_ABSENT")
        self.producer_after = self.producer / "producer-after.tsv"
        self.producer_after.write_text(
            "PRODUCER\t" +
            base64.b64encode(str(self.generated).encode("utf-8")).decode("ascii") +
            "\t" + hashlib.sha256(self.inputs[1][1]).hexdigest() + "\n",
            encoding="ascii")
        self.native = {
            source_key(str(p)): {
                "algorithm": "sha256", "digest": hashlib.sha256(raw).digest()
            }
            for p, raw in self.inputs
        }
        keys = set(self.native)
        self.dbi = {
            "status": "DBI_PARSED", "dbi": keys, "c13": keys,
            "lines": {source_key(str(self.tracked))},
            "c13_records": 2, "c13_algorithm_counts": {"NONE": 2},
        }

    def classify(self, path, unused_repo):
        return ("intermediate_location_producer_unverified"
                if path.name == self.generated.name else "checked_in")

    def execute(self, specification=None, native=None, dbi=None):
        with mock.patch("gate_cn_live_provenance.verify_checkout"), \
             mock.patch("gate_cn_live_provenance.source_pdb_inventory",
                        return_value=(native if native is not None else self.native,
                                      dbi if dbi is not None else self.dbi)), \
             mock.patch("exp041_compiler_input_audit.classify_origin",
                        side_effect=self.classify), \
             redirect_stdout(io.StringIO()):
            return run(specification or manifest(), self.app, self.evidence)


class GateCNLiveResearchAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fixture = SyntheticLiveFixture(Path(self.temp.name))

    def test_real_original_byte_hash_and_csc_producer_checks_for_non_recordsift_label(self):
        result = self.fixture.execute()
        self.assertEqual(result["verdict"], "SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED",
                         result["results"][0].get("failure_category"))
        self.assertEqual(result["results"][0]["component"], "AnotherLibrary.Core")
        self.assertEqual(result["application_repository"], "example/NonRecordSift")
        self.assertEqual(result["application_commit"], APPLICATION_SHA)
        self.assertIs(result["results"][0]["native_pe_pdb_identity_matched"], True)
        self.assertEqual(result["results"][0]["original_bytes_verified"], 2)
        self.assertEqual(result["results"][0]["generated_inputs_verified"], 1)
        self.assertEqual(result["legacy_gate_c"], "UNSATISFIED")
        self.assertEqual(result["gate_cn_release_acceptance"], "NOT_AUTHORIZED")
        self.assertEqual(result["source_link_adoption"], "HOLD")
        self.assertNotIn(self.temp.name, str(result))
        self.assertNotIn("Tracked.cs", str(result))

    def test_individual_real_provenance_primitives_cross_platform(self):
        # Synthetic-only diagnostics: identify precise host-sensitive primitive
        # without exposing real source paths or weakening production fail-closed.
        from exp041_compiler_input_audit import read_capture, verify as verify_native
        from exp042_source_provenance import verify_provenance
        fx = self.fixture
        with mock.patch("exp041_compiler_input_audit.classify_origin",
                        side_effect=fx.classify), redirect_stdout(io.StringIO()):
            records, _ = read_capture(fx.capture)
            verified = verify_native(fx.native, fx.dbi, records, fx.app)
            self.assertEqual(verified["native_inventory"], "COVERED_BY_CAPTURE")
            evidence = verify_provenance(
                records, fx.private / "msbuild-preprocessed.xml",
                (fx.private / "msbuild-diagnostic-private.log").read_text(encoding="utf-8-sig"),
                fx.producer, fx.project,
                fx.private / "exp042-csc-parameters-private.tsv")
        self.assertEqual(evidence["effective_csc_sources_verification"],
                         "MATCHED_INDEPENDENT_TASK_PARAMETER")
        self.assertEqual(evidence["intermediate_producer"]["producer_status"],
                         "VERIFIED_TARGET_EXECUTION_AND_BYTES")

    def test_trusted_path_confinement_preserves_observed_source_spelling(self):
        fx = self.fixture
        project = inside(fx.app, "src/AnotherLibrary.Core")
        private = inside(fx.evidence, "capture/independent-core")
        capture = inside(private, "source-inputs-private")
        self.assertEqual(str(project), str(fx.project))
        self.assertEqual(str(capture), str(fx.capture))
        self.assertEqual(fx.execute()["verdict"],
                         "SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED")

    def test_actual_post_csc_physical_byte_mutation_fails(self):
        self.fixture.tracked.write_bytes(b"MODIFIED AFTER CAPTURE")
        result = self.fixture.execute()
        self.assertEqual(result["verdict"], "INCOMPLETE_RESEARCH_ONLY")

    def test_actual_original_digest_mismatch_fails(self):
        native = copy.deepcopy(self.fixture.native)
        native[source_key(str(self.fixture.tracked))]["digest"] = b"x" * 32
        result = self.fixture.execute(native=native)
        self.assertEqual(result["results"][0]["status"], "BLOCKED")

    def test_full_native_identity_universe_mismatch_fails(self):
        dbi = copy.deepcopy(self.fixture.dbi)
        dbi["dbi"].remove(source_key(str(self.fixture.tracked)))
        self.assertEqual(self.fixture.execute(dbi=dbi)["verdict"],
                         "INCOMPLETE_RESEARCH_ONLY")

    def test_private_csc_structured_event_changed_fails(self):
        events = self.fixture.private / "exp042-csc-parameters-private.tsv"
        events.write_text(
            "STATUS\tCSC_TASK_PARAMETER_EVENT\nCOUNT\t2\n" +
            base64.b64encode(b"someone-else.cs").decode() + "\n" +
            base64.b64encode(str(self.fixture.generated).encode()).decode() + "\n",
            encoding="ascii")
        self.assertEqual(self.fixture.execute()["verdict"],
                         "INCOMPLETE_RESEARCH_ONLY")

    def test_missing_actual_producer_execution_fails(self):
        log = self.fixture.private / "msbuild-diagnostic-private.log"
        log.write_text("No observed generated-target execution", encoding="utf-8")
        self.assertEqual(self.fixture.execute()["verdict"],
                         "INCOMPLETE_RESEARCH_ONLY")

    def test_generated_byte_mismatch_fails(self):
        self.fixture.producer_after.write_text(
            "PRODUCER\t" +
            base64.b64encode(str(self.fixture.generated).encode()).decode() +
            "\t" + "0" * 64 + "\n", encoding="ascii")
        self.assertEqual(self.fixture.execute()["verdict"],
                         "INCOMPLETE_RESEARCH_ONLY")

    def test_external_untracked_source_origin_fails(self):
        self.fixture.classify = lambda p, r: ("external" if p.name == "Tracked.cs"
                                              else "intermediate_location_producer_unverified")
        self.assertEqual(self.fixture.execute()["verdict"],
                         "INCOMPLETE_RESEARCH_ONLY")

    def test_missing_input_snapshot_fails(self):
        (self.fixture.capture / "input-0001.bin").unlink()
        self.assertEqual(self.fixture.execute()["verdict"],
                         "INCOMPLETE_RESEARCH_ONLY")

    def test_missing_binary_is_blocked_without_private_path(self):
        with mock.patch("gate_cn_live_provenance.verify_checkout"), \
             redirect_stdout(io.StringIO()):
            result = run(manifest(), self.fixture.app, self.fixture.evidence)
        self.assertEqual(result["results"][0]["status"], "BLOCKED")
        self.assertNotIn(self.temp.name, str(result))

    def test_additional_generated_sources_rejected_in_manifest(self):
        m = manifest()
        m["components"][0]["expected_generated_inputs"] = 2
        with self.assertRaises(VerificationError):
            validate_manifest(m)

    def test_zero_generated_sources_rejected_in_manifest(self):
        m = manifest()
        m["components"][0]["expected_generated_inputs"] = 0
        with self.assertRaises(VerificationError):
            validate_manifest(m)

    def test_unrecognized_producer_contract_rejected(self):
        m = manifest()
        m["components"][0]["producer_contract"] = "ROSLYN_SOURCE_GENERATOR"
        with self.assertRaises(VerificationError):
            validate_manifest(m)

    def test_extra_external_input_in_scope_rejected(self):
        m = manifest()
        m["components"][0]["expected_native_documents"] = 3
        m["components"][0]["expected_tracked_inputs"] = 1
        m["components"][0]["expected_generated_inputs"] = 2
        with self.assertRaises(VerificationError):
            validate_manifest(m)

    def test_duplicate_component_or_evidence_alias_rejected(self):
        m = manifest()
        cloned = dict(m["components"][0], component="OtherComponent")
        m["components"].append(cloned)
        with self.assertRaises(VerificationError):
            validate_manifest(m)

    def test_traversal_absolute_and_windows_paths_rejected(self):
        for value in ("../other", "/etc/passwd", "C:/private", "src\\traversal",
                      "src//double", "src/./dot"):
            with self.subTest(value=value):
                m = manifest()
                m["components"][0]["project_dir"] = value
                with self.assertRaises(VerificationError):
                    validate_manifest(m)

    def test_symlink_outside_root_rejected(self):
        target = self.fixture.root / "outside"
        target.mkdir()
        alias = self.fixture.app / "escape"
        try:
            alias.symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable on this Windows runner")
        with self.assertRaises(VerificationError):
            inside(self.fixture.app, "escape/private.dll")

    def test_private_evidence_inside_source_tree_rejected(self):
        with self.assertRaises(VerificationError):
            verify_roots(self.fixture.app, self.fixture.project)

    def test_invalid_and_duplicate_json_keys_fail(self):
        path = self.fixture.root / "manifest.json"
        path.write_text('{"schema": "x", "schema": "y"}', encoding="utf-8")
        with self.assertRaises(VerificationError):
            load_manifest(path)
        path.write_text('{"schema":NaN}', encoding="utf-8")
        with self.assertRaises(VerificationError):
            load_manifest(path)

    def test_missing_component_universe_fails(self):
        m = manifest()
        m["components"] = []
        with self.assertRaises(VerificationError):
            validate_manifest(m)

    def test_manifest_cannot_promote_gate_status(self):
        m = manifest()
        m["authorization"] = "RELEASE_ACCEPTED"
        with self.assertRaises(VerificationError):
            validate_manifest(m)


if __name__ == "__main__":
    unittest.main()
