# EXP-015 — real baseline-versus-candidate LangVersion centralization

**Date:** November 4, 2026. **Status:** **Verified for the selected contracts**, Windows Actions [run #41867710477](https://github.com/infoconex/dotnet-modernization/actions/runs/41867710477). No RecordSift implementation approved.
**Application:** infoconex/RecordSift at immutable source commit 8358780829458854a4b0356df5ac5e685f0a34c8.
**Predecessors:** [EXP-002](EXP-002-shared-properties.md) established feasibility; [EXP-005](EXP-005-sdk-selection-and-overrides.md) established override behavior; [EXP-014](EXP-014-real-binary-metadata-pilot.md) extracted real assembly metadata but compared two captures of the same binaries.
**Authorization:** Isolated research only; no RecordSift push, merge, publication, production pipeline change or framework conversion.

## Hypothesis

Centralizing ten identical C# language-version declarations into one conditional root Directory.Build.props preserves the evaluated settings and observable compatibility contracts when **the frozen baseline and a changed candidate are built independently**.

## Isolated change and workflow

The [research-only workflow](../archives/workflows/validate-recordsift-langversion-candidate.yml) calls the [EXP-015 adapter](../../../../../tooling/pilots/recordsift/EXP-015/run.ps1) on Windows 2022.

1. Verify exact frozen RecordSift SHA and an initially clean checkout. Create an independent detached baseline Git worktree.
2. Remove exactly one existing LangVersion 7.3 element in each of five production and five test projects. Create Directory.Build.props with a conditional default of 7.3 when LangVersion is otherwise empty. Do not change imports, code, dependencies or framework.
3. Require exactly eleven changed files. Commit the candidate **locally in the ephemeral runner only** (never push). Record its SHA and patch for replay.
4. Evaluate all ten projects in Debug and Release on both source revisions (40 cells); require the effective C# version to remain 7.3.
5. Restore and rebuild all ten projects separately in Release. Run the existing 425-entry public API/package metadata verification, five XML documentation checks, all five NUnit suites, unpublished local NuGet package validation and installed independent consumer on **each** worktree.
6. Extract actual compiled public API, assembly identity and resource-name manifests from the five production assemblies per revision. Independently capture and compare source-verified snapshots of APIs, identities, resources, NuGet package contracts and test cases.
7. Preserve internal repeat and deliberately changed **external evidence** negative controls from EXP-014 on both revisions. Require a separate baseline-versus-candidate result of **matched**; missing components are failures, not success.

Unlike EXP-014, the two principal source revisions and their independently built binaries are different. The candidate commit SHA exists only on CI, so the retained patch and deterministic source transformation are essential replay evidence. The adapter also records both Git **tree SHAs**, because local commit timestamps can change the ephemeral candidate commit SHA across reruns even when the material source tree is identical. A tree hash identifies source contents, not a remotely retrievable branch or proof that all build inputs were hermetic. Distinct worktree build and restore roots minimize accidental baseline/candidate contamination.

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

These are review perspectives applied to the observed evidence, **not a claim that six independent human reviewers have signed off**. Remaining limitations are tracked below; production implementation still requires separate approval.


## Executed result (November 4, 2026)

**Successful Windows 2022 Actions run:** [41867710477](https://github.com/infoconex/dotnet-modernization/actions/runs/41867710477) at modernization PR head 5b65563c9c5321d14aa8782bda05e5c9bae90a04 (the later documentation-only PR commits do not alter the tested script or workflow). Job 126706175711 completed successfully. RecordSift frozen source was 8358780829458854a4b0356df5ac5e685f0a34c8 and the **ephemeral CI-local candidate commit** was f43fb2c30ba40f237b80e31ddd667e5f935a1c4d. This candidate commit was NOT pushed to GitHub.

| Executed check | Baseline | Candidate |
|---|---|---|
| Separate worktree and full Release restore/rebuild of ten projects | Pass | Pass |
| Evaluated LangVersion for ten Debug and ten Release projects | 20/20 equals 7.3 | 20/20 equals 7.3 |
| Existing combined API/package-metadata guard | 425/425 | 425/425 |
| Five production XML checks | Pass | Pass |
| NUnit (five separate test assemblies) | 419 total / 418 passed / 0 failed / 1 skipped | 419 / 418 / 0 / 1 |
| NuGet package build, metadata, five DLLs and XML assets | Pass | Pass |
| Independent installed net48 consumer and four Getting Started examples | Pass | Pass |
| Metadata-only extractor from actual compiled Release DLLs | 5 assemblies, 443 API records | 5 assemblies, 443 API records |
| Repeated internal source-scoped metadata snapshot | matched | matched |
| Deliberately altered external evidence control | changes_detected | changes_detected |

**Outer comparison:** baseline-versus-candidate compatibility.py reported **matched**: public API metadata, assembly identity, embedded-resource logical names, package logical contract and NUnit case outcomes matched with separate clean Git source provenance. This demonstrates one controlled pre-SDK candidate and is not broad runtime/binary or build reproducibility certification.

**Distinct NuGet archive bytes:** baseline SHA-256 C4433F7087261305CBC388A010724855ED74CBCCB436C7487A6A3D2C8277868E; candidate SHA-256 37CEBC416D15AD8356480BF8BBFC0C3649261A2C0C86B48A0F9456DEA1B97543. The logical package contract matched, but archive contents were **not byte-identical**. The packager embeds the respective source revision, so differences must not be misrepresented as behavioral regressions or proof of reproducibility. **Supply-chain provenance caveat:** the application-owned packager separately writes a fixed repository branch value of main even for this detached, locally committed candidate. The package is unpublished and this incorrect branch label is not used as evidence of where the candidate was committed; a future packager/provenance assessment must treat it as a source-metadata limitation.

**Research evidence:** [artifact 13343291183](https://github.com/infoconex/dotnet-modernization/actions/runs/41867710477/artifacts/13343291183), name recordsift-exp015-candidate-evidence, reported ZIP SHA-256 15f11869b56bb3ef07e651e67eaf790783bc46bde2ee799df42a51c1663c9f6a, 30-day retention. Contains source patch, property matrix, machine-readable comparison and per-side manifests/reports/NUnit; intentionally excludes DLLs and .nupkg bytes.

**Dependency acquisition caveat:** separate restore folders demonstrate isolated effective dependency use, **not** that each package was fetched anew from a specific source; NuGet feeds, caches and actual acquisition paths need independent provenance evidence when required.

**Toolchain observations:** windows-2022; Visual Studio 2022 MSBuild 17.14.60 on hosted runner, original application remains C# 7.3 / .NET Framework 4.8, metadata reader .NET SDK pinned 10.0.403. No publish, release, or application source-branch modifications. The Actions upload step emitted a Node.js runtime deprecation warning for a pinned upload-artifact action; this was **not** a build/verification failure but warrants normal CI-dependency monitoring.

**Review disposition:** The evidence supports recommending conditional shared LangVersion as a low-risk configuration option for a future separately approved implementation. The proof is configuration-specific: 40 evaluated properties, not every custom configuration; Release and consumers were executed, Debug build behavior beyond property evaluation was not. Missing assembly-binding, external consumer, native/COM, complete package bytes and secure supply-chain guarantees remain explicit boundaries. Do not generalize a single application's successful candidate to other projects without their own baseline and gates.
