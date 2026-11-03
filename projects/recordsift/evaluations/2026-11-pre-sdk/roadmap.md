# Recommended implementation roadmap

These are **discovery-supported recommendations**, not applied RecordSift changes.

**Current boundary:** research and documentation only. Source-inspection findings and conditional implementation ideas are **not authorization** to alter RecordSift, merge into either repository's `main`, or publish packages. Changes are disposable unless a later independent stakeholder approval explicitly authorizes implementation.

## Priority matrix

| Candidate | Immediate value | Risk | Effort | SDK preparation | Recommendation |
|---|---|---|---|---|---|
| Fix four-versus-five local test coverage | High | Low | Low | High | Before SDK, first |
| Capture reproducible compatibility gates | High | Low | Medium | High | Before SDK |
| Centralize identical LangVersion with Directory.Build.props | High | Low–medium | Low | High | Before SDK; already POC verified |
| Standardize local tool and PowerShell assumptions | High | Low–medium | Medium | Medium | Before SDK or independently |
| SDK-only Windows build/test workflow | High | Low–medium | Medium | Medium | Optional before SDK; feasible |
| Condition-based shared warning level 4 | Medium | Low–medium, **unverified** | Low | Medium | Optional **separate experiment**, not included in EXP-002 |
| global.json pin/roll-forward | Medium | Low–medium | Low | Medium | Optional after formatter test |
| Directory.Build.targets with no actual reusable build behavior | Low | Medium | Medium | Low | Not recommended |
| Additional .rsp / Directory.Solution.* files without requirements | Low | Medium | Low | Low | Not recommended |
| Early Microsoft.Common.props import | Low | High, observed failure | Medium | Low | Not recommended |
| packages.config to PackageReference / Directory.Packages.props | Migration value | Medium–high | Medium | High | During SDK conversion |

## RecordSift property-by-property evaluation (November 3, 2026)

[F-020 and the complete 10-project matrix](baseline.md) classify **19 distinct declared MSBuild properties**. Project-source duplication alone is not sufficient evidence that relocation preserves evaluated values or build behavior. [EXP-002](experiments/EXP-002-shared-properties.md) independently verified **only** `LangVersion` centralization; [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md) showed the required conditional default when a project has its own override.

| Candidate / concern | Recommended disposition | Reason / evidence |
|---|---|---|
| Shared `LangVersion=7.3` in all 10 projects | **Recommend as the single initial centralization candidate**, but only after review/explicit authorization | An isolated Release build/tests/API/XML/package experiment passed; a conditional shared default preserved a project-level override. No original project files changed during research. |
| Shared `WarningLevel=4` in Debug and Release for all 10 projects | **Optional second, separate experiment; not verified for movement** | 20 repeated declarations, but source groups are conditional. Moving to an unconditional default changes applicability for configurations outside those groups; inspect evaluated property and error/warning behavior. |
| Production-only `WarningsAsErrors=1591`, per-project XML documentation output | **Keep project-local** pending a distinct requirement | This is a deliberate source/test distinction and includes unique XML output paths and CS1591 enforcement. Moving it into nested files adds import/composition risk. |
| `Configuration`, `Platform`, `OutputPath`, `DebugType`, `Optimize`, `DefineConstants`, `DebugSymbols` | **Keep project-local** | Conditional groups are evaluated before the present late props import; package/test scripts and compiler/runtime behavior depend on these choices. |
| `TargetFrameworkVersion=v4.8` | **Keep project-local** | Raw-XML compatibility verifier expects it in each project; centralization requires an independent tooling change and its own evidence. |
| `OutputType`, `FileAlignment`, `AppDesignerFolder`, `IsTestProject` | **Keep project-local** | Minimal benefit, partial coverage or purposeful differences across projects. |
| `ProjectGuid`, `AssemblyName`, `RootNamespace`, resource identities and explicit items | **Do not homogenize** | These identify projects, assemblies, resources, references and packaging contracts. |

**If a future owner approves a limited shared-properties experiment:** start from the frozen `RecordSift/research/dotnet-modernization` branch, run `MSBuild -getProperty` and `/pp` before and after, preserve project-local overrides, and compare Debug **and** Release, all ten project builds, five NUnit suites (419 total / 418 pass / 0 fail / 1 skip), 425 API/metadata entries, assembly/resources, XML output, unpublished NuGet package layout and independent clean consumer. Keep candidate moves isolated so failures can be attributed. Preserve failed controls and distinguish the earlier demonstrated Release parity from new, unexecuted checks.

**No new MSBuild or CI run was performed for this property inventory.**

## Dependency-aware sequence

1. **Agree on acceptance baseline.** Use [baseline](baseline.md), preserve five NUnit suites, 425 approved API/metadata entries, XML docs, resource and assembly identity, local package and consumer checks. Document skipped or unavailable gates.
2. **Repair local testing parity.** Modify `scripts/run_tests.ps1` *in RecordSift only after approval* to include XLSX. Confirm 419/418/0/1 and normal CI.
3. **Create minimal shared compiler defaults.** Move identical LangVersion=7.3 from all ten projects into root Directory.Build.props, without adding an early import. Use conditional assignment where project-specific override must remain possible. Compare evaluated properties; execute the complete gate.
4. **Consider other duplication one setting at a time.** WarningLevel may qualify. Keep output directories, documentation files, resource names, assembly metadata and TargetFrameworkVersion project-specific for now.
5. **Document a fully inventoried clean Windows environment.** Favor an immutable .NET SDK-only image for educational build/test independence; separately qualify complete API/packaging/consumer scripts. Do not claim release equivalence prematurely.
6. **Consider SDK selection after actual formatter/CI test.** Make any global.json choice deliberate and documented.
7. **Only then evaluate SDK-style conversion.** Preserve current framework and C# while converting project format; defer PackageReference/central package management to a separately verified stage if appropriate.

## Verification for substantive application changes

Restoration → Release build of all ten → NUnit 419 discovered / 418 pass / 0 fail / 1 expected skip → public API 425 entries → assembly versions and logical resources → five XML docs → .nuspec/package contents, dependencies and clean consumer verification → Windows CI.

A change can be implemented independently when its only dependency is the baseline; the shared-properties change benefits from fixing the local test runner first. Do not change application main, merge or publish based solely on this roadmap.

## Coverage of the 34 proposed RecordSift investigations

The earlier planning backlog identified **34 candidate investigations in six workstreams** (the source heading incorrectly said seven). The crosswalk below reconciles those candidates with this evaluation; it is **not** a second implementation plan or a claim that all investigations are complete. Evidence states refer to the **frozen November 2026 baseline**, and no change to RecordSift's `main` is implied. This evaluation's scope remains **pre-SDK discovery**. Conversion, runtime migration and related post-conversion work should use new dated evaluations with their own baseline SHAs if pursued.

Do not read an existing CI check as proof of a new migration scenario. In particular, Release build/test success does not prove Debug parity, executing five NUnit suites does not establish code coverage, and successful SDK-only build/NUnit does not certify packaging/consumer independence. The [current status](status.md), [findings](findings.md), [risks](risks.md), and individual [experiments](experiments/README.md) remain authoritative for exact results.

### 1. Application baseline and compatibility (1–6)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 1 | Solution/project inventory | Verified source inventory | [Baseline](baseline.md) |
| 2 | Reproducible build | Release CI verified; Debug parity not established | [Baseline](baseline.md) |
| 3 | All-suite local testing | Five-suite CI verified; local XLSX omission unresolved | [Status](status.md) |
| 4 | Public API compatibility | 425-entry baseline verified; enforce on future changes | [EXP-001](experiments/EXP-001-baseline.md) |
| 5 | Assembly/resource/XML contracts | Baseline identities documented; compare on each change | [Baseline](baseline.md) |
| 6 | Packaging and consumers | Existing packaging/clean consumer CI passed | [Evidence](evidence/manifest.md) |

### 2. MSBuild configuration (7–12)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 7 | Actual MSBuild imports | Verified, including failed early-import control | [EXP-006](experiments/EXP-006-msbuild-imports.md) |
| 8 | Shared project properties | Property-by-property source audit completed: **LangVersion** centralization verified by POC, **WarningLevel** optional unverified follow-up; preserve other project-specific declarations. No permanent application implementation. | [F-020](findings.md), [baseline](baseline.md), [EXP-002](experiments/EXP-002-shared-properties.md) |
| 9 | Project override behavior | Conditional default verified; no implementation | [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md) |
| 10 | Shared build targets | Import verified; no new target justified | [EXP-006](experiments/EXP-006-msbuild-imports.md) |
| 11 | Response/solution build customization | No need demonstrated; no adoption experiment | [Risks](risks.md) |
| 12 | Raw project-XML assumptions | API checker coupling observed; refactor not implemented | [Baseline](baseline.md) |

### 3. Tooling and environments (13–19)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 13 | Windows runner inventory | Verified installed/preinstalled toolchain | [EXP-001](experiments/EXP-001-baseline.md) |
| 14 | Framework SDK container | Historical image tested; supported 4.8.1 image not executed | [EXP-003](experiments/EXP-003-framework-sdk-container.md) |
| 15 | Build without VS Build Tools | Restore/build/all five NUnit suites verified; later EXP-007 confirms XML/API and local NuGet pack/install, not full release parity | [EXP-004](experiments/EXP-004-sdk-only-build.md), [EXP-007](experiments/EXP-007-sdk-only-release-gates.md) |
| 16 | Full SDK-only release validation | **Complete investigation, partially verified:** XML and 425-entry API checks passed; NuGet package creation and installation passed. Unchanged packaging validator failed on notice text comparison despite byte-identical bytes; clean-consumer validator stopped on XML omission during install. Standalone consumer compilation/execution and full SDK-only release parity **not verified**. | [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), [R-001](risks.md) |
| 17 | Clean Windows VM | Not executed; optional alternative environment | [Original discovery](discovery-report.md) |
| 18 | Consistent local build/test commands | Proposed; local test parity must be corrected first | [Status](status.md) |
| 19 | Tool discovery and PowerShell host | PowerShell 5.1/7 difference verified; standardization pending | [EXP-006](experiments/EXP-006-msbuild-imports.md) |

### 4. Repository configuration and dependencies (20–24)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 20 | SDK selection with global.json | Selection/negative control verified; pinned formatter/build untested | [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md) |
| 21 | EditorConfig/analyzer enforcement | Existing naming gate observed; broader rule review pending | [Original discovery](discovery-report.md) |
| 22 | NuGet restore sources and audit | Existing CI restore/audit verified; changes not proposed | [Baseline](baseline.md) |
| 23 | Direct/transitive dependency inventory | Pinned packages inspected; systematic transitive map pending | [Risks](risks.md) |
| 24 | Dependency support/security review | Existing audit gate verified; broader support/remediation review pending | [Evidence](evidence/manifest.md) |

### 5. SDK-style conversion preparation (25–30)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 25 | Conversion tools and approach | Future evaluation; not compared or approved | [Risks](risks.md) |
| 26 | Assembly metadata conversion | Future evaluation; preserve current attributes | [Baseline](baseline.md) |
| 27 | Compile/resource item globs | Future evaluation; preserve explicit logical names | [Baseline](baseline.md) |
| 28 | PackageReference/central versions | Future dependency migration; not executed | [R-008](risks.md) |
| 29 | SDK packaging and test tooling | Future evaluation; existing contracts remain | [Baseline](baseline.md) |
| 30 | Post-conversion parity | Future mandatory acceptance criteria; not executed | [Evidence standards](../../../../methodology/evidence-standards.md) |

### 6. Runtime, language, architecture and CI (31–34)

| # | Investigation | Baseline disposition / remaining work | Current evidence |
|---|---|---|---|
| 31 | Modern .NET runtime | Future separately baselined evaluation; not executed | [Evaluation process](../../../../methodology/evaluation-process.md) |
| 32 | New C# features and analyzers | Future independent candidate; not contingent on conversion | [Catalog](../../../../methodology/investigation-catalog.md) |
| 33 | Architecture/platform dependencies | Broader investigation deferred; can run independently | [Catalog](../../../../methodology/investigation-catalog.md) |
| 34 | Post-conversion CI/CD/release | Future evaluation; pre-SDK CI improvements can be independent | [Catalog](../../../../methodology/investigation-catalog.md) |

**Immediate implementation candidates (subject to approval):** correct `scripts/run_tests.ps1` and stale test-count documentation, then evaluate the already proven minimal `Directory.Build.props` change. **Separate follow-up work:** if full SDK-only release parity is required, address and verify the documented EXP-007 packaging-text, installed-XML and Visual Studio toolchain assumptions with explicit application implementation approval; independently consider supported container versions, dependency/security and analyzer settings when justified. **New evaluations:** SDK-style conversion, PackageReference migration, runtime/platform changes and larger architecture/CI redesigns if justified. Independent investigations need not wait for these later phases.
