#!/usr/bin/env python3
"""Gate C-N experimental live adapter for trusted local classic Windows PDBs.

This deliberately narrow adapter reuses EXP-041/042/043's actual native,
physical-byte and structured Csc verifiers. It accepts an externally reviewed
compilation manifest rather than assuming RecordSift's assembly layout.
RESEARCH ONLY: no production release or general generator support.
Never use PDB source names as filesystem paths or disclose private evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from classic_pdb_document_checksums import VerificationError
from exp041_compiler_input_audit import read_capture, verify as verify_native
from exp042_source_provenance import verify_provenance
from exp043_five_pdb_audit import source_pdb_inventory, summarize_native

SCHEMA = "gate-cn-live-manifest-v1"
SAFE_LABEL = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]{0,79}$")
SHA = re.compile(r"^[0-9a-f]{40}$")
COMPONENT_FIELDS = {
    "component", "project_dir", "assembly_name", "evidence_dir",
    "capture_dir", "expected_native_documents", "expected_tracked_inputs",
    "expected_generated_inputs", "producer_contract",
}
ROOT_FIELDS = {"schema", "authorization", "application_repository",
               "application_commit", "components"}
PRODUCER_CONTRACT = "EXP042_MONIKER_ONE_PER_COMPONENT"
MAX_COMPONENTS = 32


def require(condition, code):
    if not condition:
        raise VerificationError(code)


def unique_object(pairs):
    output = {}
    for key, value in pairs:
        require(key not in output, "DUPLICATE_MANIFEST_JSON_KEY")
        output[key] = value
    return output


def load_manifest(path):
    require(path.is_file() and 0 < path.stat().st_size <= 128 * 1024,
            "MANIFEST_MISSING_OR_OVERSIZED")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"),
                              object_pairs_hook=unique_object,
                              parse_constant=lambda _: require(False, "INVALID_JSON_CONSTANT"))
    except VerificationError:
        raise
    except (ValueError, UnicodeError):
        raise VerificationError("INVALID_MANIFEST_JSON") from None
    validate_manifest(manifest)
    return manifest


def relative_parts(value):
    require(type(value) is str and 0 < len(value) <= 240
            and "\\\\" not in value and ":" not in value
            and not value.startswith("/"), "UNSAFE_MANIFEST_RELATIVE_PATH")
    parts = value.split("/")
    require(all(p not in ("", ".", "..") and len(p) <= 80
                and SAFE_LABEL.fullmatch(p) for p in parts),
            "UNSAFE_MANIFEST_RELATIVE_PATH")
    return PurePosixPath(*parts)


def validate_manifest(manifest):
    require(type(manifest) is dict and set(manifest) == ROOT_FIELDS
            and manifest["schema"] == SCHEMA
            and manifest["authorization"] == "DESIGN_VALIDATION_ONLY"
            and type(manifest["application_repository"]) is str
            and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
                             manifest["application_repository"])
            and type(manifest["application_commit"]) is str
            and SHA.fullmatch(manifest["application_commit"]),
            "LIVE_MANIFEST_ROOT_INVALID")
    components = manifest["components"]
    require(type(components) is list and 0 < len(components) <= MAX_COMPONENTS,
            "LIVE_COMPONENT_UNIVERSE_INVALID")
    seen_names, seen_projects, seen_evidence = set(), set(), set()
    for item in components:
        require(type(item) is dict and set(item) == COMPONENT_FIELDS,
                "LIVE_COMPONENT_SCHEMA_INVALID")
        name, assembly = item["component"], item["assembly_name"]
        require(type(name) is str and SAFE_LABEL.fullmatch(name)
                and type(assembly) is str and SAFE_LABEL.fullmatch(assembly),
                "LIVE_COMPONENT_NAME_INVALID")
        project = str(relative_parts(item["project_dir"]))
        evidence = str(relative_parts(item["evidence_dir"]))
        capture = str(relative_parts(item["capture_dir"]))
        require("/" not in capture and capture in
                ("source-inputs-private", "exp041-original-inputs-private"),
                "UNSUPPORTED_CAPTURE_LAYOUT")
        require(name.casefold() not in seen_names
                and project.casefold() not in seen_projects
                and evidence.casefold() not in seen_evidence,
                "DUPLICATE_LIVE_COMPONENT_OR_INPUT")
        seen_names.add(name.casefold())
        seen_projects.add(project.casefold())
        seen_evidence.add(evidence.casefold())
        total = item["expected_native_documents"]
        tracked = item["expected_tracked_inputs"]
        generated = item["expected_generated_inputs"]
        require(type(total) is int and 1 < total <= 1024
                and type(tracked) is int and tracked >= 1
                and type(generated) is int and generated == 1
                and total == tracked + generated
                and item["producer_contract"] == PRODUCER_CONTRACT,
                "UNSUPPORTED_LIVE_COMPILER_INPUT_ORIGIN_SCOPE")
    return manifest


def inside(root, relative):
    root = root.resolve(strict=True)
    path = root.joinpath(*relative_parts(relative).parts)
    require(path.resolve(strict=False).is_relative_to(root),
            "MANIFEST_PATH_ESCAPES_TRUSTED_ROOT")
    return path


def verify_roots(app, evidence):
    a, e = app.resolve(strict=True), evidence.resolve(strict=True)
    require(a.is_dir() and e.is_dir() and a != e
            and not a.is_relative_to(e) and not e.is_relative_to(a),
            "PRIVATE_EVIDENCE_ROOT_NOT_ISOLATED")
    return a, e


def verify_checkout(app, expected, repository):
    """Fail if the exact immutable source revision or tracked tree is wrong."""
    try:
        head = subprocess.run(
            ["git", "-C", str(app), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=15, check=False)
        origin = subprocess.run(
            ["git", "-C", str(app), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=15, check=False)
        diff = subprocess.run(
            ["git", "-C", str(app), "diff", "--name-only", "HEAD", "--"],
            capture_output=True, text=True, timeout=15, check=False)
        url = origin.stdout.strip()
        allowed = {"https://github.com/" + repository,
                   "git@github.com:" + repository,
                   "ssh://git@github.com/" + repository}
        require(origin.returncode == 0 and url.removesuffix(".git") in allowed
                and head.returncode == 0 and head.stdout.strip() == expected
                and diff.returncode == 0 and not diff.stdout.strip(),
                "APPLICATION_COMMIT_OR_TRACKED_WORKTREE_INVALID")
    except (OSError, subprocess.TimeoutExpired):
        raise VerificationError("APPLICATION_GIT_ATTESTATION_UNAVAILABLE") from None


def run_component(app, evidence, item):
    """Real original-byte and source-key comparisons, synthetic tests use mocks.

    No alternate generated-source contracts are inferred from source location.
    Unrecognized, external and additional generated inputs fail closed.
    """
    name = item["component"]
    result = {"component": name, "status": "BLOCKED"}
    try:
        project = inside(app, item["project_dir"])
        stem = item["assembly_name"]
        dll = inside(project, "bin/Release/" + stem + ".dll")
        pdb = inside(project, "bin/Release/" + stem + ".pdb")
        private = inside(evidence, item["evidence_dir"])
        capture = inside(private, item["capture_dir"])
        producer = Path(str(capture) + "-producer")
        require(producer.resolve(strict=False).is_relative_to(private.resolve(strict=True)),
                "PRODUCER_PATH_ESCAPES_PRIVATE_EVIDENCE")
        require(dll.is_file() and 0 < dll.stat().st_size <= 64 * 1024 * 1024
                and pdb.is_file() and 0 < pdb.stat().st_size <= 128 * 1024 * 1024,
                "LOCAL_PE_PDB_MISSING_OR_OVERSIZED")
        private_log = inside(private, "msbuild-diagnostic-private.log")
        require(private_log.is_file() and 0 < private_log.stat().st_size <= 40 * 1024 * 1024,
                "PRIVATE_DIAGNOSTIC_MISSING_OR_OVERSIZED")
        native, dbi = source_pdb_inventory(dll, pdb)
        records, _ = read_capture(capture)
        actual = verify_native(native, dbi, records, app)
        provenance = verify_provenance(
            records, inside(private, "msbuild-preprocessed.xml"),
            private_log.read_text(encoding="utf-8-sig", errors="replace"),
            producer, project,
            inside(private, "exp042-csc-parameters-private.tsv"))
        count = item["expected_native_documents"]
        origins = actual["origin_categories"]
        produced = provenance["intermediate_producer"]
        # Private captured bytes must still equal the exact files after Csc.
        unchanged = all(p.is_file() and p.stat().st_size <= 16*1024*1024
                        and hashlib.sha256(p.read_bytes()).digest() ==
                        hashlib.sha256(raw).digest()
                        for p, raw, _ in records)
        require(len(native) == count and len(records) == count
                and actual["native_source_documents"] == count
                and actual["original_input_sha256_or_sha1_matches"] == count
                and actual["native_documents_without_captured_input"] == 0
                and actual["native_inventory"] == "COVERED_BY_CAPTURE"
                and origins == {
                    "checked_in": item["expected_tracked_inputs"],
                    "intermediate_location_producer_unverified": 1,
                }
                and unchanged,
                "ORIGINAL_PHYSICAL_INPUT_ORIGIN_OR_BYTE_SCOPE_INCOMPLETE")
        require(provenance["evaluated_csc_source_binding"] ==
                "CORECOMPILE_CSC_USES_COMPILE_ITEMS"
                and provenance["structured_csc_task_parameter_evidence"] ==
                "STRUCTURED_CSC_TASK_INPUT_EVENT"
                and provenance["effective_csc_sources_verification"] ==
                "MATCHED_INDEPENDENT_TASK_PARAMETER"
                and provenance["effective_csc_source_count"] == count
                and produced["producer_status"] ==
                "VERIFIED_TARGET_EXECUTION_AND_BYTES"
                and produced["producer_target_name"] ==
                "GenerateTargetFrameworkMonikerAttribute"
                and produced["output_matches_private_compiler_input"] is True
                and produced["output_previously_absent"] is True
                and produced["generator_task_executed"] is True,
                "CSC_OR_MONIKER_PROVENANCE_INCOMPLETE")
        # This result reports only counts and fixed categories, not identities.
        result.update(summarize_native(native, dbi))
        require(result["native_named_vs_dbi_c13"] == "MATCHED",
                "NATIVE_DOCUMENT_SET_INCOMPLETE")
        result["original_bytes_verified"] = count
        result["actual_csc_sources_verified"] = count
        result["generated_inputs_verified"] = 1
        result["status"] = "RESEARCH_VERIFIED"
    except Exception:
        # Never echo exception details: untrusted path/errors may contain bytes.
        result = {"component": name, "status": "BLOCKED",
                  "failure_category": "LIVE_COMPONENT_FAILED_CLOSED"}
    return result


def run(manifest, app, evidence):
    validate_manifest(manifest)
    app, evidence = verify_roots(app, evidence)
    verify_checkout(app, manifest["application_commit"],
                    manifest["application_repository"])
    results = [run_component(app, evidence, c) for c in manifest["components"]]
    return {
        "schema": "gate-cn-live-research-result-v1",
        "verdict": ("SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED"
                    if all(x["status"] == "RESEARCH_VERIFIED" for x in results)
                    else "INCOMPLETE_RESEARCH_ONLY"),
        "required_components": len(manifest["components"]),
        "results": results,
        "legacy_gate_c": "UNSATISFIED",
        "gate_cn_release_acceptance": "NOT_AUTHORIZED",
        "source_link_adoption": "HOLD",
        "not_proven": "Generated input contracts other than one EXP042 moniker per component; cross-app live execution, post-Csc runtime trust, original release/consumer acceptance, managed checksum APIs, Visual Studio/debugger operation or hostile PDB safety",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("manifest", "app-root", "evidence-root", "output"):
        parser.add_argument("--" + key, required=True, type=Path)
    args = parser.parse_args()
    try:
        require(not args.output.exists(), "RESEARCH_OUTPUT_ALREADY_EXISTS")
        manifest = load_manifest(args.manifest)
        result = run(manifest, args.app_root, args.evidence_root)
        require(not args.output.resolve(strict=False).is_relative_to(
                    args.app_root.resolve(strict=True)),
                "SANITIZED_OUTPUT_MUST_BE_OUTSIDE_APP")
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
        print("Gate C-N live adapter:", result["verdict"],
              "Gate C UNSATISFIED; Source Link HOLD")
        return 0 if result["verdict"] == "SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED" else 2
    except Exception:
        print("GATE_CN_LIVE_FAIL_CLOSED: PRIVATE_OR_UNSUPPORTED_INPUT",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
