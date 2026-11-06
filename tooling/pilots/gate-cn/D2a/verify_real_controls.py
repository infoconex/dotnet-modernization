#!/usr/bin/env python3
"""D2a: real net48 compiler-output, classic-PDB and actual CLR-load research.

Only checked-in public dummy source, ephemeral hosted Windows runner and ONE
traditional .NET Framework 4.8 project. Never invoke from a release gate.
Only category-only sanitized JSON leaves the private local evidence directory.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

REPO_VALIDATORS = Path(__file__).resolve().parents[3] / "validators"
sys.path.insert(0, str(REPO_VALIDATORS))
from native_windows_pdb_sourcelink import (
    parse_named_streams, read_msf, read_pe_codeview
)


class Failure(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def require(condition, code):
    if not condition:
        raise Failure(code)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def genuine_pair(dll, pdb):
    """Parse *actual* classic PDB/PE structures; no fake signature providers."""
    try:
        streams = read_msf(pdb.read_bytes())
        guid_age = parse_named_streams(streams[1], len(streams))[:2]
        pe_guid_age = read_pe_codeview(dll.read_bytes())
    except (OSError, ValueError, IndexError, TypeError, OverflowError) as ex:
        raise Failure("INVALID_REAL_NATIVE_PE_PDB") from None
    require(pe_guid_age == guid_age, "INVALID_REAL_NATIVE_PE_PDB")
    return True


def actual_event(private_variant, label):
    """The unique completed Csc event is captured by the separate real logger."""
    raw = (private_variant / "csc-witness.tsv").read_text(encoding="ascii")
    items = raw.strip().split("\t")
    require(len(items) == 4 and items[0:2] ==
            ["STATUS", "UNIQUE_COMPLETED_CSC"], "MISSING_FRESH_CSC_OUTPUT_ATTESTATION")
    require(len(items[2]) > 2 and items[3].isdigit() and
            1 <= int(items[3]) <= 16, "MISSING_FRESH_CSC_OUTPUT_ATTESTATION")
    return label + ":" + items[2]


def build_seal(variant, label):
    """Immediately sealed local runner witness, NOT external Csc attestation."""
    dll = variant / "D2a.Probe.dll"
    pdb = variant / "D2a.Probe.pdb"
    require(dll.is_file() and pdb.is_file(), "REAL_OUTPUT_MISSING")
    genuine_pair(dll, pdb)
    return {
        "event": actual_event(variant, label),
        "options": (variant / "options.txt").read_text(encoding="ascii").strip(),
        "dll": sha(dll), "pdb": sha(pdb)
    }


def verify_live(event, options, dll, pdb, seal, *, root_fresh):
    """Fail-closed on one intended category with real output bytes and PDB pair."""
    require(root_fresh, "OUTPUT_ROOT_NOT_FRESH")
    require(event is not None, "MISSING_FRESH_CSC_OUTPUT_ATTESTATION")
    require(event == seal["event"] and options == seal["options"],
            "INVOCATION_OPTIONS_OR_OUTPUT_SHA_MISMATCH")
    require(dll.is_file() and pdb.is_file(), "REAL_OUTPUT_MISSING")
    genuine_pair(dll, pdb)
    require(sha(dll) == seal["dll"] and sha(pdb) == seal["pdb"],
            "OUTPUT_INVOCATION_SHA_MISMATCH")
    return True


def run_loaded(assembly, loader):
    """New Windows PowerShell 5.1 child process: actual .NET Framework CLR load."""
    p = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive",
         "-ExecutionPolicy", "Bypass", "-File", str(loader),
         "-AssemblyPath", str(assembly)],
        capture_output=True, text=True, timeout=30, check=False
    )
    require(p.returncode == 0, "REAL_CLR_LOAD_INCONCLUSIVE")
    try:
        value = json.loads(p.stdout.strip())
        require(value["loaded_location"].casefold() ==
                str(assembly.resolve()).casefold(), "REAL_CLR_LOCATION_MISMATCH")
        require(value["method_value"] in (101, 202),
                "REAL_CLR_METHOD_RESULT_UNEXPECTED")
        require(len(value["loaded_sha256"]) == 64, "REAL_CLR_IDENTITY_INVALID")
        return value
    except (ValueError, KeyError, AttributeError, TypeError):
        raise Failure("REAL_CLR_WITNESS_INVALID") from None


def verify_loaded_candidate(witness, approved_sha, approved_value):
    require(witness["loaded_sha256"] == approved_sha and
            witness["method_value"] == approved_value,
            "CANDIDATE_TEST_DLL_NOT_ATTESTED")
    return True


def expect_negative(identifier, expected, action, results):
    try:
        action()
    except Failure as error:
        require(error.code == expected, "WRONG_NEGATIVE_FAILURE_STAGE")
        results.append({
            "id": identifier, "status": "PASS",
            "expected_failure_category": expected,
            "observed_failure_category": error.code,
            "positive_control": "PASS"
        })
        return
    raise Failure("INVALID_NEGATIVE_ACCEPTED")


def run(root, loader):
    a, b = root / "variant-a", root / "variant-b"
    seal_a, seal_b = build_seal(a, "real-compile-a"), build_seal(b, "real-compile-b")
    require(seal_a["dll"] != seal_b["dll"], "OPTION_VARIANTS_NOT_DISTINGUISHABLE")
    require(seal_a["options"] != seal_b["options"], "COMPILER_OPTIONS_NOT_DISTINCT")
    require(seal_a["event"] != seal_b["event"], "CSC_INVOCATIONS_NOT_DISTINCT")
    require(seal_a["options"] == "D2A_BASE" and seal_b["options"] == "D2A_ALT",
            "WRONG_CONTROLLED_BUILD_OPTIONS")

    # Real pair and sealed byte identity positivity for each variant.
    assert verify_live(seal_a["event"], seal_a["options"], a / "D2a.Probe.dll",
                       a / "D2a.Probe.pdb", seal_a, root_fresh=True)
    assert verify_live(seal_b["event"], seal_b["options"], b / "D2a.Probe.dll",
                       b / "D2a.Probe.pdb", seal_b, root_fresh=True)

    results = []
    # N01: real A valid paired output; no *new* Csc witness is supplied.
    expect_negative("D2a-N01", "MISSING_FRESH_CSC_OUTPUT_ATTESTATION",
                    lambda: verify_live(None, seal_a["options"],
                                        a / "D2a.Probe.dll", a / "D2a.Probe.pdb",
                                        seal_a, root_fresh=True), results)

    # N02: same physical source bytes (checked by orchestration), but
    # actual A Csc/options witness is substituted for B sealed output.
    expect_negative("D2a-N02", "INVOCATION_OPTIONS_OR_OUTPUT_SHA_MISMATCH",
                    lambda: verify_live(seal_a["event"], seal_a["options"],
                                        b / "D2a.Probe.dll", b / "D2a.Probe.pdb",
                                        seal_b, root_fresh=True), results)

    # N03: both actual pairs are valid native symbols; substitute complete A
    # while retaining B's independently captured event + postbuild sealed SHA.
    expect_negative("D2a-N03", "OUTPUT_INVOCATION_SHA_MISMATCH",
                    lambda: verify_live(seal_b["event"], seal_b["options"],
                                        a / "D2a.Probe.dll", a / "D2a.Probe.pdb",
                                        seal_b, root_fresh=True), results)

    # N04: actually copy and load each real DLL with the .NET Framework CLR.
    consumer = root / "disposable-consumer"
    require(not consumer.exists(), "CONSUMER_ROOT_PREEXISTING")
    consumer.mkdir()
    candidate = consumer / "D2a.Probe.dll"
    shutil.copyfile(b / "D2a.Probe.dll", candidate)
    real_b = run_loaded(candidate, loader)
    require(real_b["loaded_sha256"] == sha(candidate), "REAL_CLR_HASH_UNSTABLE")
    assert verify_loaded_candidate(real_b, seal_b["dll"], 202)
    candidate.unlink()
    shutil.copyfile(a / "D2a.Probe.dll", candidate)
    real_a = run_loaded(candidate, loader)
    require(real_a["loaded_sha256"] == sha(candidate), "REAL_CLR_HASH_UNSTABLE")
    require(real_a["method_value"] == 101, "REAL_CLR_WRONG_MUTATION")
    expect_negative("D2a-N04", "CANDIDATE_TEST_DLL_NOT_ATTESTED",
                    lambda: verify_loaded_candidate(real_a, seal_b["dll"], 202),
                    results)

    # N05: tamper with independent freshness declaration of a genuine B pair.
    expect_negative("D2a-N05", "OUTPUT_ROOT_NOT_FRESH",
                    lambda: verify_live(seal_b["event"], seal_b["options"],
                                        b / "D2a.Probe.dll", b / "D2a.Probe.pdb",
                                        seal_b, root_fresh=False), results)
    require(len(results) == 5, "WRONG_NEGATIVE_COUNT")
    return {
        "experiment": "D2a",
        "scope": "one disposable traditional net48 native-PDB Windows project",
        "real_compiler_positives": 2,
        "actual_netfx_clr_load_positives": 1,
        "controls": results,
        "verdict": "RESEARCH_NEGATIVES_PASSED_REAL_FIXTURE_ONLY",
        "limit": "local trusted runner event/output seal; not cryptographic Csc causation, manifest signer, NuGet chain or release authority",
        "gate_c": "UNSATISFIED",
        "gate_cn_release": "NOT_AUTHORIZED",
        "production_source_link": "HOLD"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-root", required=True, type=Path)
    parser.add_argument("--loader", required=True, type=Path)
    parser.add_argument("--sanitized-output", required=True, type=Path)
    args = parser.parse_args()
    try:
        require(not args.sanitized_output.exists(), "SANITIZED_REPORT_EXISTS")
        result = run(args.private_root, args.loader)
        args.sanitized_output.write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n",
            encoding="ascii"
        )
        print("D2a REAL Windows native PDB 2 positive builds, 5 targeted negatives PASS")
        print("RESEARCH ONLY; Gate C UNSATISFIED; C-N release NOT_AUTHORIZED; Source Link HOLD")
    except Failure as e:
        print("D2a INCONCLUSIVE/FAILED_CLOSED: " + e.code, file=sys.stderr)
        raise SystemExit(2)
    except Exception:
        # Do not leak raw filesystem paths, source strings, symbols or Csc args.
        print("D2a INCONCLUSIVE/FAILED_CLOSED: PRIVATE_RUNNER_ERROR", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()
