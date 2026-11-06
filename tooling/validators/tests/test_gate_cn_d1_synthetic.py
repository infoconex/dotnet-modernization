"""D1 TDD contracts: 11 scoped synthetic fail-closed negatives and paired positives.

No RecordSift, compiler, real PDB, package install, GitHub request or private bytes.
Each negative first proves its corresponding unmodified fixture succeeds.
"""
import copy
import hashlib
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate_cn_d1_synthetic import (
    Approval, Candidate, CompilerEvent, CompiledOutput, Rejected,
    authorize_scope, verify_candidate_bindings, verify_compiler_output,
    canonical_sha256,
)


def digest(value):
    return hashlib.sha256(value).hexdigest()


def approved_scope():
    return {
        "schema": "gate-cn-d1-synthetic-v1",
        "application_commit": "a" * 40,
        "components": [
            {
                "assembly": "Example.Core",
                "project": "src/Example.Core/Example.Core.csproj",
                "target": "CoreCompile",
                "framework": "net48",
                "configuration": "Release",
                "platform": "AnyCPU",
                "sources": [
                    {"path": "src/Example.Core/Core.cs",
                     "origin": "tracked", "sha256": digest(b"core source")},
                    {"path": "src/Example.Core/obj/FrameworkAttribute.cs",
                     "origin": "moniker", "sha256": digest(b"generated core")},
                ],
            },
            {
                "assembly": "Example.Parsing",
                "project": "src/Example.Parsing/Example.Parsing.csproj",
                "target": "CoreCompile",
                "framework": "net48",
                "configuration": "Release",
                "platform": "AnyCPU",
                "sources": [
                    {"path": "src/Example.Parsing/Parser.cs",
                     "origin": "tracked", "sha256": digest(b"parser source")},
                    {"path": "src/Example.Parsing/obj/FrameworkAttribute.cs",
                     "origin": "moniker", "sha256": digest(b"generated parser")},
                ],
            },
        ],
    }


def scope_inputs():
    expected = approved_scope()
    approval = Approval(
        manifest_sha256=canonical_sha256(expected),
        reviewer_identity="independent-synthetic-approver",
        expires_at=2000,
        revoked=False,
    )
    # The approval registry is a separate fixture argument. The code under
    # test cannot manufacture or amend the trusted record.
    return expected, copy.deepcopy(expected["components"]), approval


def candidate_inputs():
    candidates = {
        "Example.Core": Candidate("1.0.0", digest(b"core dll")),
        "Example.Parsing": Candidate("1.0.0", digest(b"parsing dll")),
    }
    required = {
        "Core.Tests": ("Example.Core",),
        "Parsing.Tests": ("Example.Parsing", "Example.Core"),
    }
    suites = {
        name: {assembly: candidates[assembly] for assembly in names}
        for name, names in required.items()
    }
    selected = Candidate("1.0.0", digest(b"approved synthetic nupkg"))
    return candidates, required, suites, selected, selected


def compiler_inputs():
    event = CompilerEvent(
        run_identity="test-run-1",
        task_identity="node1-project1-target1-task1",
        compiler_sources=("Core.cs", "FrameworkAttribute.cs"),
        compiler_options_sha256=digest(b"/debug:pdbonly /deterministic+"),
        output_dll="isolated/bin/Core.dll",
        output_pdb="isolated/bin/Core.pdb",
        completed=True,
    )
    output = CompiledOutput(
        run_identity=event.run_identity,
        dll_sha256=digest(b"new compiled output"),
        pdb_sha256=digest(b"new native pdb"),
        pe_codeview_guid_age="ab12:1",
        pdb_info_guid_age="ab12:1",
    )
    sealed = copy.deepcopy(output)
    return event, output, sealed


class D1SyntheticContractTests(unittest.TestCase):
    def blocked(self, code, action):
        with self.assertRaises(Rejected) as raised:
            action()
        self.assertEqual(raised.exception.category, code)

    def authorized(self, manifest, observed, approval, builder="research-builder"):
        return authorize_scope(
            manifest, observed, approval,
            build_identity=builder, current_time=1000,
        )

    def candidate_bound(self, candidates, required, suites, approved, selected):
        return verify_candidate_bindings(
            candidates, required, suites, approved, selected
        )

    def compiler_bound(self, event, output, sealed, empty=True):
        return verify_compiler_output(
            (event,) if event is not None else (),
            output, sealed,
            output_root_was_empty=empty,
            required_run_identity="test-run-1",
        )

    def test_m_n01_missing_approved_component(self):
        manifest, actual, authority = scope_inputs()
        self.assertTrue(self.authorized(manifest, actual, authority))
        self.blocked("D1_COMPONENT_UNIVERSE_MISMATCH",
                     lambda: self.authorized(manifest, actual[:1], authority))

    def test_m_n02_unapproved_extra_component(self):
        manifest, actual, authority = scope_inputs()
        self.assertTrue(self.authorized(manifest, actual, authority))
        extra = copy.deepcopy(actual[0])
        extra["assembly"] = "Example.Unauthorized"
        extra["project"] = "src/Example.Unauthorized/Other.csproj"
        self.blocked("D1_COMPONENT_UNIVERSE_MISMATCH",
                     lambda: self.authorized(manifest, actual + [extra], authority))

    def test_m_n03_modified_replayed_or_self_authorized_approval(self):
        manifest, actual, authority = scope_inputs()
        self.assertTrue(self.authorized(manifest, actual, authority))
        altered = copy.deepcopy(manifest)
        altered["application_commit"] = "b" * 40
        self.blocked("D1_MANIFEST_APPROVAL_MISMATCH",
                     lambda: self.authorized(altered, actual, authority))
        expired = Approval(authority.manifest_sha256,
                           authority.reviewer_identity, 999, False)
        self.blocked("D1_APPROVAL_EXPIRED_OR_REVOKED",
                     lambda: self.authorized(manifest, actual, expired))
        revoked = Approval(authority.manifest_sha256,
                           authority.reviewer_identity, 2000, True)
        self.blocked("D1_APPROVAL_EXPIRED_OR_REVOKED",
                     lambda: self.authorized(manifest, actual, revoked))
        self_signed = Approval(authority.manifest_sha256, "research-builder",
                               2000, False)
        self.blocked("D1_APPROVAL_NOT_INDEPENDENT",
                     lambda: self.authorized(manifest, actual, self_signed))

    def test_m_n04_equal_counts_but_wrong_source_identity(self):
        manifest, actual, authority = scope_inputs()
        self.assertTrue(self.authorized(manifest, actual, authority))
        changed = copy.deepcopy(actual)
        changed[0]["sources"][0]["path"] = "src/Example.Core/Swap.cs"
        self.assertEqual(len(changed[0]["sources"]),
                         len(actual[0]["sources"]))
        self.blocked("D1_COMPILER_SOURCE_SET_MISMATCH",
                     lambda: self.authorized(manifest, changed, authority))

    def test_m_n05_case_fold_collision_or_unapproved_origin(self):
        manifest, actual, authority = scope_inputs()
        self.assertTrue(self.authorized(manifest, actual, authority))
        duplicate = copy.deepcopy(actual)
        duplicate.append(copy.deepcopy(actual[0]))
        duplicate[-1]["assembly"] = "example.core"
        self.blocked("D1_DUPLICATE_COMPONENT_IDENTITY",
                     lambda: self.authorized(manifest, duplicate, authority))
        unexpected = copy.deepcopy(actual)
        unexpected[1]["sources"][1]["origin"] = "external"
        self.blocked("D1_COMPILER_SOURCE_SET_MISMATCH",
                     lambda: self.authorized(manifest, unexpected, authority))

    def test_b_n01_missing_required_suite_copy(self):
        candidates, required, suites, approved, selected = candidate_inputs()
        self.assertTrue(self.candidate_bound(candidates, required, suites,
                                            approved, selected))
        changed = copy.deepcopy(suites)
        del changed["Parsing.Tests"]["Example.Core"]
        self.blocked("D1_MANDATORY_COPY_LOCAL_MISSING",
                     lambda: self.candidate_bound(candidates, required,
                                                  changed, approved, selected))

    def test_b_n02_version_equal_dll_replacement(self):
        candidates, required, suites, approved, selected = candidate_inputs()
        self.assertTrue(self.candidate_bound(candidates, required, suites,
                                            approved, selected))
        changed = copy.deepcopy(suites)
        changed["Parsing.Tests"]["Example.Core"] = Candidate(
            "1.0.0", digest(b"different dll same version"))
        self.blocked("D1_CANDIDATE_COPY_LOCAL_HASH_MISMATCH",
                     lambda: self.candidate_bound(candidates, required,
                                                  changed, approved, selected))

    def test_b_n04_same_version_unexpected_selected_package(self):
        candidates, required, suites, approved, selected = candidate_inputs()
        self.assertTrue(self.candidate_bound(candidates, required, suites,
                                            approved, selected))
        changed = Candidate("1.0.0", digest(b"alternate feed same package id/version"))
        self.blocked("D1_PACKAGE_ARCHIVE_IDENTITY_MISMATCH",
                     lambda: self.candidate_bound(candidates, required,
                                                  suites, approved, changed))

    def test_i_n01_old_paired_output_without_current_csc(self):
        event, output, sealed = compiler_inputs()
        self.assertTrue(self.compiler_bound(event, output, sealed))
        self.blocked("D1_CSC_EVENT_MISSING_OR_AMBIGUOUS",
                     lambda: self.compiler_bound(None, output, sealed))

    def test_i_n03_substitute_valid_internal_pair_with_other_bytes(self):
        event, output, sealed = compiler_inputs()
        self.assertTrue(self.compiler_bound(event, output, sealed))
        # Different bytes but internally matching PE RSDS/PDB identity:
        swapped = CompiledOutput(output.run_identity,
                                 digest(b"other dll"), digest(b"other pdb"),
                                 "cd34:1", "cd34:1")
        self.blocked("D1_COMPILER_OUTPUT_HASH_MISMATCH",
                     lambda: self.compiler_bound(event, swapped, sealed))

    def test_i_n05_nonempty_output_root_even_with_matching_pair(self):
        event, output, sealed = compiler_inputs()
        self.assertTrue(self.compiler_bound(event, output, sealed))
        self.blocked("D1_OUTPUT_ROOT_NOT_FRESH",
                     lambda: self.compiler_bound(event, output, sealed,
                                                 empty=False))


if __name__ == "__main__":
    unittest.main()
