# EXP-015 — real baseline-versus-candidate LangVersion centralization

**Date:** November 4, 2026. **Status:** Proposed experiment: not yet CI verified.
**Application:** infoconex/RecordSift at immutable source commit 8358780829458854a4b0356df5ac5e685f0a34c8.
**Predecessors:** [EXP-002](EXP-002-shared-properties.md) established feasibility; [EXP-005](EXP-005-sdk-selection-and-overrides.md) established override behavior; [EXP-014](EXP-014-real-binary-metadata-pilot.md) extracted real assembly metadata but compared two captures of the same binaries.
**Authorization:** Isolated research only; no RecordSift push, merge, publication, production pipeline change or framework conversion.

## Hypothesis

Centralizing ten identical C# language-version declarations into one conditional root Directory.Build.props preserves the evaluated settings and observable compatibility contracts when **the frozen baseline and a changed candidate are built independently**.

## Isolated change and workflow

The [research-only workflow](../../../../../.github/workflows/validate-recordsift-langversion-candidate.yml) calls the [EXP-015 adapter](../../../../../tooling/pilots/recordsift/EXP-015/run.ps1) on Windows 2022.

1. Verify exact frozen RecordSift SHA and an initially clean checkout. Create an independent detached baseline Git worktree.
2. Remove exactly one existing LangVersion 7.3 element in each of five production and five test projects. Create Directory.Build.props with a conditional default of 7.3 when LangVersion is otherwise empty. Do not change imports, code, dependencies or framework.
3. Require exactly eleven changed files. Commit the candidate **locally in the ephemeral runner only** (never push). Record its SHA and patch for replay.
4. Evaluate all ten projects in Debug and Release on both source revisions (40 cells); require the effective C# version to remain 7.3.
5. Restore and rebuild all ten projects separately in Release. Run the existing 425-entry public API/package metadata verification, five XML documentation checks, all five NUnit suites, unpublished local NuGet package validation and installed independent consumer on **each** worktree.
6. Extract actual compiled public API, assembly identity and resource-name manifests from the five production assemblies per revision. Independently capture and compare source-verified snapshots of APIs, identities, resources, NuGet package contracts and test cases.
7. Preserve internal repeat and deliberately changed **external evidence** negative controls from EXP-014 on both revisions. Require a separate baseline-versus-candidate result of **matched**; missing components are failures, not success.

Unlike EXP-014, the two principal source revisions and their independently built binaries are different. The candidate commit SHA exists only on CI, so the retained patch and deterministic source transformation are essential replay evidence. Distinct worktree build and restore roots minimize accidental baseline/candidate contamination.

## Acceptance and evidence retention

Acceptance requires all individually named gates to pass: 40/40 property evaluations, two ten-project Release builds, two original 425-entry checks, two five-suite NUnit runs each discovering 419 tests (418 pass, zero fail, one known skip), XML and consumer/package gates on both sides, independent metadata extraction, complete captured evidence and a clean-source comparator match.

Retain for 30 days: candidate.patch, candidate-report.json, toolchain.json, property-matrix.json, both source snapshots, both detailed pilot reports, test XML, metadata manifests, negative-control comparisons and the outer compatibility comparison. Do **not** upload compiled DLLs or NuGet packages. Their exact SHA-256 fingerprints are included in evidence.

A passed workflow is not, by itself, proof of compatibility. An unexplained difference must be investigated and documented. No component may be omitted or comparator semantics weakened to make an experiment pass.

## Limitations

- Builds/tests/consumers are Release-only; Debug effective settings are checked but Debug binaries are not built. Additional custom configurations and platforms are not assessed.
- Historical 425 mixed API/metadata entries and the metadata extractor's 443 distinct records use different contracts. Compare each format only with its own equivalent.
- NuGet package comparison checks selected package metadata and payload *paths*, not byte-identical package or DLL contents. Review package and assembly fingerprints separately.
- This does not certify assembly binding, native/COM dependencies, runtime portability, signing, interop, all consumers, security, localization bytes, performance or build determinism.
- The adapter contains RecordSift-specific expectations intentionally; reusable comparators and metadata extraction remain application-agnostic.
- The GitHub runner/toolchain is a mutable environment. Record actual versions and source identities. A clean Git proof worktree is not a cryptographic build attestation.
- Research success does **not** authorize production adoption.

## Review lenses before approval

| Review perspective | Potential weakness | Safeguard or gap |
|---|---|---|
| .NET modernization | Property precedence and unsupported configurations | Conditional default, 40-cell matrix; custom configurations deferred |
| MSBuild/NuGet | Actual compared dependency and package contracts | Independent restores/packaging, per-side source SHAs; package-byte identity unverified |
| Architecture | One-off pilot duplicating shared infrastructure | Existing EXP-014 runner parameterized minimally; comparator and extractor reused |
| Test/release | Same binary accidentally compared twice | Independent worktrees, separate builds, distinct source commits and external comparison |
| Security/supply chain | Unauthorized publishing and CI write access | Read-only GitHub credentials, disposable local commit, metadata-only uploads |
| Developer experience | Confusing planned work with verified evidence | Explicit pending state and replayable patch, command and CI evidence |

These are review perspectives to test, **not a claim that independent reviewers have signed off**. Record actual CI results and reviewer concerns once available.
