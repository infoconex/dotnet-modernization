# Recommended implementation roadmap

These are **discovery-supported recommendations**, not applied RecordSift changes.

## Priority matrix

| Candidate | Immediate value | Risk | Effort | SDK preparation | Recommendation |
|---|---|---|---|---|---|
| Recognize existing local runner correction on `release/0.2` | High | Already implemented on that branch | No new implementation | High | **Historical fix PR #258**; do not duplicate or promote automatically |
| Capture reproducible compatibility gates | High | Low | Medium | High | Before SDK |
| Centralize identical LangVersion with Directory.Build.props | High | Low–medium | Low | High | Before SDK; already POC verified |
| Standardize local tool and PowerShell assumptions | High | Low–medium | Medium | Medium | Before SDK or independently |
| SDK-only Windows build/test workflow | High | Low–medium | Medium | Medium | Optional before SDK; feasible |
| Condition-based shared warning levels | Modest | Low with scoped condition | Low | Medium | **EXP-010 verified**; optional because level 4 is already default |
| global.json pin/roll-forward | Conditional | SDK provisioning/update responsibility | Low | Medium | **EXP-008 verified formatter** under pins 10.0.303 and 10.0.403; optional |
| Directory.Build.targets with no actual reusable build behavior | Low | Medium | Medium | Low | Not recommended |
| Additional .rsp / Directory.Solution.* files without requirements | Low | Medium | Low | Low | Not recommended |
| Early Microsoft.Common.props import | Low | High, observed failure | Medium | Low | Not recommended |
| `packages.config` to exact-pinned `PackageReference` | Optional future migration | Medium–high; verification/tooling adaptations | Medium–high | May precede or follow SDK conversion independently | **EXP-012 verified experimental parity; not implementation-approved**. Do not introduce central management while using `packages.config`. |

## Dependency-aware sequence

1. **Agree on acceptance baseline.** Use [baseline](baseline.md), preserve five NUnit suites, 425 approved API/metadata entries, XML docs, resource and assembly identity, local package and consumer checks. Document skipped or unavailable gates.
2. **Recognize existing local test parity work.** Previously approved RecordSift PR #258 already corrected `scripts/run_tests.ps1` on `release/0.2`; it is **not on `main`**. Do not reimplement or promote it under research authorization. Always compare all five suites (419/418/0/1).
3. **Create minimal shared compiler defaults.** Move identical LangVersion=7.3 from all ten projects into root Directory.Build.props, without adding an early import. Use conditional assignment where project-specific override must remain possible. Compare evaluated properties; execute the complete gate.
4. **Consider other duplication one setting at a time.** WarningLevel may qualify. Keep output directories, documentation files, resource names, assembly metadata and TargetFrameworkVersion project-specific for now.
5. **Document the verified Windows toolchain options.** EXP-004 proved SDK-only Windows build/all five tests without VS Build Tools; EXP-009 proved adapted package/consumer **positive gates** but the unmodified release scripts still fail and SDK-only negative CS1591 was not executed. A new release path needs independent approval and complete gates.
6. **Treat SDK pinning as an operational choice, not a research gap.** EXP-008 already verified the actual formatter and Release/test/XML/API gates under 10.0.303 and 10.0.403. A `global.json` file is optional; plan SDK provisioning if adopted.
7. **Defer migration decisions.** EXP-012 proved exact-pinned PackageReference independently of SDK-style conversion on traditional net48 projects; EXP-013 identified format-sensitive CI checks. Separate format migration from dependency cleanup and SDK-style conversion. If proceeding later, preserve current framework/C# and API/resources/consumer contract until separately tested.

## Verification for substantive application changes

Restore → Release build of all ten → NUnit 419 discovered / 418 pass / 0 fail / 1 expected skip → **unchanged 425-entry API+package-metadata contract** (or separately approved format-aware equivalent that preserves the same policy) → assembly/resource identity → five XML docs → .nuspec contents, effective dependencies and clean consumer → Windows CI. EXP-012's 414 compiled API/identity pass is **not** a pass of the unchanged 425-entry gate.

A change can be implemented independently when its only dependency is the baseline; the shared-properties change benefits from fixing the local test runner first. Do not change application main, merge or publish based solely on this roadmap.

## Coverage of the 34 proposed RecordSift investigations

The earlier planning backlog identified **34 candidate investigations in six workstreams** (the source heading incorrectly said seven). The crosswalk below reconciles those candidates with this evaluation; it is **not** a second implementation plan or a claim that all investigations are complete. Evidence states refer to the **frozen November 2026 baseline**, and no change to RecordSift's `main` is implied. This evaluation's scope remains **pre-SDK discovery**. Conversion, runtime migration and related post-conversion work should use new dated evaluations with their own baseline SHAs if pursued.

Do not read an existing CI check as proof of a new migration scenario. In particular, Release build/test success does not prove Debug parity, executing five NUnit suites does not establish code coverage, and successful SDK-only build/NUnit does not certify packaging/consumer independence. The [current status](status.md), [findings](findings.md), [risks](risks.md), and individual [experiments](experiments/README.md) remain authoritative for exact results.

### 1. Application baseline and compatibility (1–6)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 1 | Solution/project inventory | Verified source inventory | [Baseline](baseline.md) |
| 2 | Reproducible build | Release baseline build verified; Debug builds verified only in scoped EXP-010 property experiment, not all variants | [Baseline](baseline.md), [EXP-010](experiments/EXP-010-warninglevel-centralization.md) |
| 3 | All-suite local testing | Five-suite main CI verified; local runner omission corrected only on `release/0.2` by PR #258, main baseline unchanged | [Baseline](baseline.md), [PR #258](https://github.com/infoconex/RecordSift/pull/258) |
| 4 | Public API compatibility | 425-entry baseline verified; enforce on future changes | [EXP-001](experiments/EXP-001-baseline.md) |
| 5 | Assembly/resource/XML contracts | Baseline identities documented; compare on each change | [Baseline](baseline.md) |
| 6 | Packaging and consumers | Existing packaging/clean consumer CI passed | [Evidence](evidence/manifest.md) |

### 2. MSBuild configuration (7–12)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 7 | Actual MSBuild imports | Verified, including failed early-import control | [EXP-006](experiments/EXP-006-msbuild-imports.md) |
| 8 | Shared project properties | EXP-002/005 conditional `LangVersion` parity verified; full 19-property inventory completed; no application change | [EXP-002](experiments/EXP-002-shared-properties.md), [Property inventory](baseline.md) |
| 9 | Project override behavior | Conditional default verified; no implementation | [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md) |
| 10 | Shared build targets | Targets import works, no custom build targets or reusable behavior found in ten-project source audit; adding file not justified | [EXP-006](experiments/EXP-006-msbuild-imports.md), [Targets audit finding F-019](findings.md) |
| 11 | Response/solution build customization | No need demonstrated; no adoption experiment | [Risks](risks.md) |
| 12 | Raw project-XML assumptions | API checker coupling observed; refactor not implemented | [Baseline](baseline.md) |

### 3. Tooling and environments (13–19)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 13 | Windows runner inventory | Verified installed/preinstalled toolchain | [EXP-001](experiments/EXP-001-baseline.md) |
| 14 | Framework SDK container | Historical image tested; supported 4.8.1 image not executed | [EXP-003](experiments/EXP-003-framework-sdk-container.md) |
| 15 | Build without VS Build Tools | SDK-only restore/build/five NUnit suites verified; EXP-009 additionally verifies *temporarily corrected* packaging/consumer positive path (not original scripts) | [EXP-004](experiments/EXP-004-sdk-only-build.md), [EXP-009](experiments/EXP-009-sdk-only-release-validation.md) |
| 16 | Full SDK-only release validation | EXP-007 remains **historically partial**; EXP-009 later verified modified UTF-8 notice/ZIP XML/SDK Roslyn clean consumers and all four samples. Original scripts fail unchanged; SDK-only negative CS1591 **not run** | [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), [EXP-009](experiments/EXP-009-sdk-only-release-validation.md) |
| 17 | Clean Windows VM | Not executed; optional alternative environment | [Original discovery](discovery-report.md) |
| 18 | Consistent local build/test commands | Original local runner defect resolved only on `release/0.2` (#258); freeze main. Document full five-suite command without duplicating fix | [PR #258](https://github.com/infoconex/RecordSift/pull/258), [Baseline](baseline.md) |
| 19 | Tool discovery and PowerShell host | PowerShell 5.1/7 difference verified; standardization pending | [EXP-006](experiments/EXP-006-msbuild-imports.md) |

### 4. Repository configuration and dependencies (20–24)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 20 | SDK selection with global.json | Exact SDK pins 10.0.303 and 10.0.403 **verified** with actual IDE1006 formatter, ten Release projects, 419 NUnit, five XML and 425 API entries; pin adoption optional | [EXP-008](experiments/EXP-008-pinned-sdk-formatter-build.md) |
| 21 | EditorConfig/analyzer enforcement | Existing `.editorconfig`/IDE1006 gate verified with pinned SDKs and migrated PackageReference project format; broader analyzer policy changes deferred | [EXP-008](experiments/EXP-008-pinned-sdk-formatter-build.md), [EXP-013](experiments/EXP-013-migration-tooling-ci-readiness.md) |
| 22 | NuGet restore sources and audit | Existing NuGet source/audit baseline verified; EXP-013 confirmed unchanged NuGet CLI restore works with exact-pinned PackageReference, but raw-config pin audit needs format-aware alternative | [EXP-013](experiments/EXP-013-migration-tooling-ci-readiness.md) |
| 23 | Direct/transitive dependency inventory | EXP-011 inventoried 7 configs/17 declarations/13 unique restored IDs, 11 exact production `.nuspec` entries, 13 HintPaths; EXP-012 resolved exact-pinned vs direct-only graphs and observed four version downgrades | [EXP-011](experiments/EXP-011-nuget-dependency-inventory.md), [EXP-012](experiments/EXP-012-packagereference-isolation.md) |
| 24 | Dependency support/security review | Original NuGet audit gate exists; broader supply-chain support/security review and remediation remain separate, not proven by package-inventory experiment | [Baseline](baseline.md), [Risks](risks.md) |

### 5. SDK-style conversion preparation (25–30)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 25 | Conversion tools and approach | EXP-012 verified manual exact-pinned PackageReference **without SDK-style conversion**; EXP-013 audited CI. Microsoft's Visual Studio GUI migrator **not executed**; its dependency classifications/report remain unknown | [EXP-012](experiments/EXP-012-packagereference-isolation.md), [EXP-013](experiments/EXP-013-migration-tooling-ci-readiness.md) |
| 26 | Assembly metadata conversion | Future evaluation; preserve current attributes | [Baseline](baseline.md) |
| 27 | Compile/resource item globs | Future evaluation; preserve explicit logical names | [Baseline](baseline.md) |
| 28 | PackageReference/central versions | EXP-012: temporary PackageReference conversion of 7 traditional net48 projects with 17 exact pins passed build/419 NUnit/414 compiled API/5 XML/local package/clean consumer/negative CS1591, but unchanged 425-entry raw-metadata check fails. Direct-only candidate downgraded four transitive versions despite tests; central package management not evaluated | [EXP-012](experiments/EXP-012-packagereference-isolation.md), [R-008](risks.md) |
| 29 | SDK packaging and test tooling | EXP-012 required separately provisioned legacy NUnit runner; original `.nuspec` package/consumer gates passed for full exact pins. Post-SDK conversion packaging/tooling remains **unexecuted** | [EXP-012](experiments/EXP-012-packagereference-isolation.md), [Baseline](baseline.md) |
| 30 | Post-conversion parity | Post-**SDK-style** parity remains **not executed**. Pre-SDK PackageReference format change parity with documented exception verified only in EXP-012/013 | [Evidence standards](../../../../methodology/evidence-standards.md), [EXP-012](experiments/EXP-012-packagereference-isolation.md) |

### 6. Runtime, language, architecture and CI (31–34)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 31 | Modern .NET runtime | Future separately baselined evaluation; not executed | [Evaluation process](../../../../methodology/evaluation-process.md) |
| 32 | New C# features and analyzers | Future independent candidate; not contingent on conversion | [Catalog](../../../../methodology/investigation-catalog.md) |
| 33 | Architecture/platform dependencies | EXP-013 tested original vs converted XLSX vendor architecture guard: original raw `Reference` fails under PackageReference; temporary format-aware guard passes positive and rejects missing ExcelDataReader. Broader architecture/platform migration not assessed | [EXP-013](experiments/EXP-013-migration-tooling-ci-readiness.md) |
| 34 | Post-conversion CI/CD/release | EXP-013 existing `nuget restore` and IDE1006 formatter pass after exact-pinned PackageReference; raw package audit, API metadata and NUnit provisioning need targeted future adaptation. Full modified production CI/release workflow not executed | [EXP-013](experiments/EXP-013-migration-tooling-ci-readiness.md) |

**Proposed immediate value (still not authorized for application implementation):** acknowledge the runner fix already on `release/0.2`, preserve complete 419-case CI gates, and consider the previously verified conditional shared `LangVersion` as the first *new* small application change if later approved. **Optional operational choices:** `global.json`, SDK-only Windows tooling and properly scoped `WarningLevel`. **Defer:** PackageReference implementation, deliberate version cleanup (four actual downgrades in direct-only EXP-012), SDK-style conversion, runtime/platform changes and broad CI rewrites until independently scoped. [Consolidated review](review-2026-11-03-consolidated-research.md) distinguishes verified evidence and proposals.
