# RecordSift — Current technical discovery (November 2026)

**Application:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Current discovery source:** `modernization/case-study` at [`68fdee8210f2cde71674250ce56d110b8ffeeac3`](https://github.com/infoconex/RecordSift/commit/68fdee8210f2cde71674250ce56d110b8ffeeac3)  
**Comparison branch:** `main` at [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004)  
**Historical pre-SDK source:** `main` at [`8358780829458854a4b0356df5ac5e685f0a34c8`](https://github.com/infoconex/RecordSift/commit/8358780829458854a4b0356df5ac5e685f0a34c8)  
**Discovery date:** 2026-11-11  
**Phase:** source-backed application discovery; compatibility execution at the case-study SHA not performed  
**Scope/approval:** repository inspection and documentation-only discovery in `dotnet-modernization`, authorized by the application owner on 2026-11-11. No RecordSift source changes, experiments, release actions or merges authorized by this record.  
**Record status:** source inspection completed for the scoped paths; runtime verification at the case-study SHA **not executed**.

## Objective and evidence boundaries

Document **how RecordSift is technically assembled, configured, built, tested and delivered**, at an immutable source revision, with an explicit distinction between source inspection and executed evidence. Record relevant platform and compatibility contracts without evaluating improvements or prescribing changes. Modernization opportunity assessment is a separate later activity.

The companion [technical baseline](baseline.md) owns source configuration, project/dependency inventory, build and test commands, compatibility evidence and outstanding execution gates. Detailed normative behavior remains in RecordSift's [functional and nonfunctional requirements](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/requirements/functional.md), [scenario specifications](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/scenarios/README.md) and [test traceability](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/testing/traceability.md); link to these instead of duplicating 108 scenarios.

Evidence notation used below:

- **Source-inspected, current case-study SHA:** the named file or implementation is present and expresses the described behavior. It does **not** establish that code ran at `68fdee8210f2cde71674250ce56d110b8ffeeac3`.
- **Reused execution, another SHA:** a linked CI or experiment actually ran on the stated original source and environment; its result is not silently promoted to this case-study SHA.
- **Not executed / unresolved:** no matching run was performed or the described question cannot be answered from the inspected evidence.

## Application context and technical boundaries

RecordSift is a synchronous **Windows/.NET Framework 4.8 C# class library** used by consumer applications to import CSV/XLSX and obtain typed results, diagnostics and optional reports. It is not a hosted service. These facts establish the application type, its consumer boundary and the format-specific infrastructure—not an invitation to duplicate functional requirements. [Application README](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/README.md) · [Architecture](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/engineering/architecture.md).

Its five production projects separate Domain contracts, Application orchestration/ports, CSV and XLSX input adapters, and reporting adapters. Five corresponding NUnit test projects provide verification infrastructure. Detailed behavioral requirements and 108 acceptance scenarios remain authoritative in the [RecordSift specifications](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/scenarios/README.md), not in the modernization discovery.

## Technical discovery navigation

| Area | Source-backed current observation | Detailed technical record |
|---|---|---|
| Repository, solution and projects | `RecordSift.sln`, ten traditional projects, five production plus five test assemblies | [Baseline identity and project graph](baseline.md#2-solution-and-dependency-boundaries) |
| Frameworks and compiler | `TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, per-project configuration and MSBuild imports | [Project configuration](baseline.md#project-configuration-and-important-contracts) |
| Shared/repository settings | `.editorconfig` and `nuget.config` present; other relevant files enumerated by presence or absence | [Configuration inventory](baseline.md#3-repository-configuration-dependencies-and-packaging) |
| Dependencies and restore | `packages.config`, pinned parser/NUnit packages, NuGet feeds and packaging manifests | [Dependency and packaging inventory](baseline.md#3-repository-configuration-dependencies-and-packaging) |
| Development environment | Windows runners, Visual Studio MSBuild, NuGet CLI, PowerShell, formatter and NUnit tooling | [Build and verification commands](baseline.md#4-build-test-and-verification-entry-points) |
| Tests and CI/CD | Five NUnit suites, local scenario-filtering script, GitHub Actions build/documentation/consumer workflows | [Verification entry points](baseline.md#4-build-test-and-verification-entry-points) |
| Compatibility and delivery | Public net48 API snapshot (425 entries), seven JSON fixtures, packaged DLL/XML docs, Windows/net48 deployment boundary | [Compatibility evidence](baseline.md#5-compatibility-and-test-evidence) |

The linked baseline is the **sole detailed technical inventory**. Values identified in source are not automatically tool-evaluated or executed. Missing configuration files are facts, not requests to add them. This discovery records evidence gaps without evaluating modernization opportunities.

## Historical-to-current reconciliation

The [preserved 2026-11 pre-SDK evaluation](https://github.com/infoconex/dotnet-modernization/blob/main/projects/recordsift/evaluations/2026-11-pre-sdk/README.md) is anchored to `8358780829458854a4b0356df5ac5e685f0a34c8`. A GitHub comparison of that commit against `68fdee8210f2cde71674250ce56d110b8ffeeac3` reports **six commits and 21 changed files**, with **no changes to `src/` or `tests/` files** in that comparison. This supports reuse of *source-shape observations* where the compared files are identical; it does not create a new runtime verification result. [Historical discovery](https://github.com/infoconex/dotnet-modernization/blob/main/projects/recordsift/evaluations/2026-11-pre-sdk/discovery-report.md) · [historical findings](https://github.com/infoconex/dotnet-modernization/blob/main/projects/recordsift/evaluations/2026-11-pre-sdk/findings.md).

- **Historical F-002 is superseded as a present source defect.** The old local test script omitted XLSX; [current `scripts/run_tests.ps1`](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/scripts/run_tests.ps1) enumerates all five assemblies, and the [Windows workflow](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/.github/workflows/windows-net48.yml) includes a local-runner parity step. The current script's execution at `68fdee8210f2cde71674250ce56d110b8ffeeac3` was **not** performed here.
- **The case-study branch is distinct from main.** [Compare current branches](https://github.com/infoconex/RecordSift/compare/main...modernization/case-study): two commits ahead, zero behind at inspection, with a `nuget.config` case/contents change, dedicated workflow and modernization documents plus selected workflow/document synchronization; no `src/` or `tests/` difference.
- **NuGet configuration stage is already in the case-study branch.** The [stage record](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/modernization/stages/nuget-config/README.md) reports earlier positive/negative NuGet restore controls on a different SHA. Record the tested stage revision separately; do not claim that stage's exact tests ran at `68fdee8210f2cde71674250ce56d110b8ffeeac3` or propose it as a missing future stage.
- **Current branch governance overrides old instructions.** [`AGENTS.md`](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/AGENTS.md) sends ordinary issue work to protected `main` and reserves the case-study branch for isolated work, while [scenario authoring instructions](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/scenarios/README.md) still say to target retired `release/0.1`. The [documentation index](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/README.md) confirms publication of 0.1.0 in its current header but retains an older “not yet verified” publication sentence. Treat these as **documentation drift**, not changes in product behavior. Any correction belongs in a separately authorized RecordSift docs PR.
- **Historical research is not implementation approval.** Earlier SDK-only, centralized-property, PackageReference and Source Link experiments stay tied to their recorded environments and decisions; none implies the case-study branch adopted them. [Historical decisions](https://github.com/infoconex/dotnet-modernization/blob/main/projects/recordsift/evaluations/2026-11-pre-sdk/decisions.md) · [experiment index](https://github.com/infoconex/dotnet-modernization/blob/main/projects/recordsift/evaluations/2026-11-pre-sdk/experiments/README.md).

## Verification status and material gaps

| Claim or gate | Status at this discovery | Evidence / limit |
|---|---|---|
| Repository tree, application source, project/manifest contents, five-suite runner | **Source-inspected** at `68fdee8210f2cde71674250ce56d110b8ffeeac3` | Links above and [baseline](baseline.md); no compilation performed |
| Windows build/test/documentation/consumer workflows | **Executed at `main@1809d06c0fade59e4769d16e0f8eaf10fa426004`**, not case-study SHA | [Windows CI #43146607664](https://github.com/infoconex/RecordSift/actions/runs/43146607664), [consumer #43146607706](https://github.com/infoconex/RecordSift/actions/runs/43146607706), [docs #43146607615](https://github.com/infoconex/RecordSift/actions/runs/43146607615) |
| Historic full compatibility count: 419 discovered / 418 passed / 0 failed / 1 skipped; 425 API entries | **Reused historical execution** at older SHA; 425 entries also **source-counted** in current checked-in text snapshot | [Historical discovery](https://github.com/infoconex/dotnet-modernization/blob/main/projects/recordsift/evaluations/2026-11-pre-sdk/discovery-report.md), [current API baseline](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/compatibility/public-api-net48.txt); not a current case-study execution result |
| Exact case-study SHA Windows restore/build/NUnit/API/consumer gates | **Not executed** | Branch-specific `nuget.config` and workflow changes mean main/historical runs cannot substitute for an exact-SHA verification |
| Actual behavior on a future modern .NET target, portability, full async/streaming, exhaustive security/performance | **Not assessed / not authorized** | Current release is Windows/net48; [compatibility policy](https://github.com/infoconex/RecordSift/blob/68fdee8210f2cde71674250ce56d110b8ffeeac3/docs/compatibility/README.md) requires independent future gates |

**Discovery disposition:** The relevant *current source structure, behavior pathways, normative evidence links and known discrepancies* are documented, but the **case-study execution baseline remains open**. Do not report the application as runtime-verified at `68fdee8210f2cde71674250ce56d110b8ffeeac3` until corresponding exact-SHA Windows checks are executed and their results recorded. A prior or current-main green workflow is supporting context, not a substitute.

## Next independent action

Review this source-backed discovery and the linked technical [baseline](baseline.md); then, **if separately authorized**, run the unchanged application compatibility gates on the exact case-study SHA in an appropriate Windows environment and record the results. Keep modernization assessment, source changes, documentation remediation and publication as separate decisions. The initial methodology refinement is proposed in [dotnet-modernization PR #97](https://github.com/infoconex/dotnet-modernization/pull/97); it is not assumed merged.
