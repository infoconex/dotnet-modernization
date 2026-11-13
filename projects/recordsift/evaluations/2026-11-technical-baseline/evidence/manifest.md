# RecordSift technical discovery — Evidence manifest

**Evaluation:** [November 2026 native-first technical baseline](../README.md)  
**Frozen source commit:** `1809d06c0fade59e4769d16e0f8eaf10fa426004`  
**Status:** Source-inspected application facts and existing GitHub Actions evidence are available for the selected commit. **No operator-run Windows discovery commands have been captured** in this evaluation. GitHub CI results and the operator's local machine are different environments.

| Evidence ID | Discovery context | Source / trace | Method and provenance | What it establishes / limitations |
|---|---|---|---|---|
| EV-001 | Baseline item 33 (selected revision) | [Immutable application commit](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) | Source metadata inspected via connected GitHub | Identifies the repository revision selected for this walkthrough. **Does not** establish operator local HEAD, working-tree state, or toolchain. |
| EV-002 | Baseline items 36–37, 42–44, 50 (source inventory) | [Tracked tree at frozen SHA](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004) | GitHub tree source-inspected | Records observed solution, project, repository configuration and workflow *paths*. Does not prove effective imports, solution membership, or commands executed. |
| EV-003 | Application description and baseline items 1–4 | [README at frozen SHA](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) | Source-inspected product documentation | Documents the application's own Windows/.NET Framework 4.8 description; not independently verified project evaluation or runtime execution. |
| EV-004 | Baseline fields 3 and 6–7 | [GitHub source repository](https://github.com/infoconex/RecordSift) and [LICENSE](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/LICENSE) | Repository metadata and tracked license file | License and default branch. SSH address is the repository clone URL, not an authenticated SSH connection test. |
| EV-005 | Baseline fields 8–11 | [README at selected SHA](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) · [GitHub v0.1.0 release](https://github.com/infoconex/RecordSift/releases/tag/v0.1.0) · [NuGet 0.1.0](https://www.nuget.org/packages/RecordSift/0.1.0) | Published release/package references | Published version and exact release/package URLs are distinct from the tracked prerelease nuspec version. |
| EV-006 | Baseline field 12 | [Tracked package manifest](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/packaging/RecordSift.nuspec) | Source declaration | `version=0.1.0-rc.1` is the version in source, not the published package. |
| EV-007 | Baseline fields 13–14 | [Production AssemblyInfo](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/Properties/AssemblyInfo.cs) | Source declaration | AssemblyVersion and AssemblyFileVersion are both `0.1.0.0`; this does not by itself verify a compiled DLL's metadata. |
| EV-008 | CI build and tests at selected SHA | [Windows build/test run](https://github.com/infoconex/RecordSift/actions/runs/43146607664) | Existing GitHub Actions run, succeeded at `1809d06c…`; job steps and logs inspected | Windows restore, Release build, API/XML/style checks and NUnit suites succeeded. NUnit results: 419 discovered, 418 passed, 0 failed, 1 skipped. This is **not** an operator-run local verification. |
| EV-009 | CI consumer verification at selected SHA | [Windows package/consumer run](https://github.com/infoconex/RecordSift/actions/runs/43146607706) | Existing GitHub Actions run, succeeded at `1809d06c…`; job steps and logs inspected | Unpublished package/clean consumer validation passed; not evidence of a fresh local consumer run. |
| EV-010 | CI docs verification at selected SHA | [Documentation validation run](https://github.com/infoconex/RecordSift/actions/runs/43146607615) | Existing GitHub Actions run, succeeded at `1809d06c…`; steps inspected | Documentation/engineering checks passed on Ubuntu; **does not** imply application cross-platform support. |
| EV-011 | Baseline 36–40 | [Solution](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/RecordSift.sln) · [Production project](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) · [Test project](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | Pinned solution and ten project XML files inspected | Solution configuration and project compiler/output/metadata **declared** values. No independent MSBuild -getProperty evaluation. |
| EV-012 | Baseline 43–45 | [Tracked NuGet.Config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/NuGet.Config) · [Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) · [Xlsx packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/packages.config) · [NUnit packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config) | Pinned repository configuration and seven packages.config manifests inspected | 17 package declarations, 13 distinct package IDs, declared framework references, and root NuGet.Config with packageSources/auditSources clear directives followed by nuget.org endpoints. No other NuGet sections (including disabledPackageSources) are declared **in this file**. Configured feeds do not establish actual download/audit origins or effective user/machine settings; no local inspection was performed. |
| EV-013 | Baseline 46 and 50 | [Windows CI workflow](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/windows-net48.yml) · [Consumer workflow](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/verify-rc-consumer.yml) · [Documentation workflow](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/validate-docs.yml) · [Release workflow](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/publish-release.yml) | Eight workflows inspected at pinned revision; selected exact invocations transcribed | Configured commands, trigger/runner choices, and release workflows are **configuration**, not proof that every workflow was executed. |
| EV-014 | Baseline 55–62 | [Exact commit Windows CI](https://github.com/infoconex/RecordSift/actions/runs/43146607664) · [Consumer run](https://github.com/infoconex/RecordSift/actions/runs/43146607706) · [Docs run](https://github.com/infoconex/RecordSift/actions/runs/43146607615) | Existing CI job steps/logs inspected; discovery gaps classified | CI commands were executed on GitHub-hosted runners; no operator Windows host or clean checkout commands have been supplied. Warning/error counts and individual command process exit codes are not invented. |

## Rules for new evidence

- Record **Discovery Date** once in the completed baseline; separate collection dates are not required for individual evidence records. Keep any dates that are inherent to an external record (such as a CI run date) as part of that source's factual information.
- Link each new artifact/output to its numbered baseline item and the complete source SHA. For executed operations, capture command, tool version, host/environment, **exit code**, output/result and retained artifact location.
- Keep **actual raw output** or a durable faithful excerpt separately from any generated report. Give exact GitHub Actions run/artifact IDs and note expiry; commit small redacted text where useful.
- Use source-inspected, tool-evaluated, existing CI-executed, and operator-executed classifications separately; preserve historical provenance. An earlier evaluation run is not new evidence for this SHA unless its exact scope is verified.
- Do not commit credentials, secret-bearing configuration, generated packages, restored dependencies or large binaries. Report missing/blocked/unexecuted checks explicitly.
- Add links to actual artifacts only when they exist. No placeholder file trees or invented screenshots/logs.

## Baseline value provenance

- Keep values in the baseline's **Value** column atomic (for example, `Library`, `Public`, `MIT`, `Windows`, a version, SHA, or exact URL). Do not append citation titles, provenance prose, or execution caveats to those values.
- Source links and qualifications belong in this manifest. Fields **1–7** are supported by EV-003/EV-004; **8–11** by EV-005; **12** by EV-006; **13–14** by EV-007. Local machine fields **18–30** remain unverified until the operator supplies tool output.

## Command review against source and tool documentation

The procedures follow baseline item order. **No local Windows commands were executed by the discovery operator in this evaluation.** The classifications below distinguish a command reviewed for correctness from a command actually observed in existing Windows CI.

| Baseline item | Native command / procedure | Review outcome | Execution evidence |
|---|---|---|---|
| 18–21 | `Get-CimInstance Win32_OperatingSystem` | Correct Windows CIM query for host caption, version, build and architecture; map four outputs to separate fields | Operator not executed |
| 22 | `$PSVersionTable.PSVersion.ToString()` | Standard PowerShell self-report; output not supplied | Operator not executed |
| 23 | `git --version` | Correct Git version command | Operator not executed |
| 24–25 | `dotnet --list-sdks` and `dotnet --list-runtimes` | Appropriate SDK and runtime inventories, not a .NET Framework targeting-pack check | Operator not executed |
| 26–27 | `msbuild -version -nologo` and `Get-Command msbuild` | Appropriate version and PATH-location checks; Developer PowerShell may be needed | Operator not executed; CI records MSBuild 17.14.60.43110 |
| 28 | `nuget help` | NuGet CLI prints version information | Operator not executed; NuGet CI restore succeeded |
| 29 | `Test-Path` for `v4.8\mscorlib.dll` under .NET Framework reference assemblies | Tests a specific local reference-assembly file, not just the existence of an empty directory or build success | Operator not executed |
| 31–35 | Prepare unused destination; select source ref and SHA; then `git clone --no-checkout`, `git switch --detach`, `git rev-parse HEAD`, `git status`, `git branch --show-current` | Ordering corrected: selection and SHA pinning precede clone; destination collision guard, stop-on-error and SHA comparison reviewed; real checkout unverified | Operator not executed |
| 36–37 | `git ls-files` solution/project patterns and optional `dotnet sln ... list` | Correct source inventory workflow; source project files and solution independently inspected via GitHub at selected SHA | Local commands not executed |
| 38–40 | Inspect project XML via `Get-Content` | Source declarations verified from ten current project files, but not MSBuild evaluated defaults | Local command not executed |
| 41 | `msbuild -getProperty:TargetFrameworkVersion,LangVersion -p:Configuration=Release -p:Platform=AnyCPU` | [Microsoft-documented MSBuild 17.8+](https://learn.microsoft.com/en-us/visualstudio/msbuild/evaluate-items-and-properties) syntax with explicit project configuration/platform; no targets requested, so property evaluation does not request a build | Operator not executed |
| 42–43 | `git ls-files` tracked directories/configuration | Tracked-tree inspection completed through GitHub; effective machine-level imports remain unknown | Local command not executed |
| 44 | `dotnet nuget list source --configfile .\NuGet.Config` | [Microsoft-documented .NET 6+](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-nuget-list-source) option; reads only the specified config rather than inherited settings | Operator not executed |
| 47 | `nuget restore` from the repository workflow | Exact-commit Windows CI step succeeded; creates/restores package files | [Windows run 43146607664](https://github.com/infoconex/RecordSift/actions/runs/43146607664); operator not executed |
| 48 | Release `msbuild ... /t:Rebuild` | Exact-commit Windows CI step succeeded; builds files and may modify output directories | [Windows run 43146607664](https://github.com/infoconex/RecordSift/actions/runs/43146607664); operator not executed |
| 49 | `.\scripts\run_tests.ps1 -Level All` | Parameter and Release artifact prerequisites verified against existing script; CI executed the same script with its default `All` level | [Windows run 43146607664](https://github.com/infoconex/RecordSift/actions/runs/43146607664); operator not executed |
| 50–51 | `git ls-files .github/workflows` and GitHub Actions run lookups | Tracked workflow definitions and exact-commit run records inspected; not every defined release workflow has been executed in this discovery | Existing exact-commit runs EV-008–EV-010 |

### Review of remaining numbered instructions

The non-command or primarily documentary steps have also been reviewed against their intended evidence and field shape:

| Baseline items | Procedure review | Execution boundary |
|---|---|---|
| 1–15 | Repository, published artifact, source metadata, and public API/consumer identity checked at the selected SHA; scalar values remain atomic and links are retained in the evidence manifest | Source/registry inspection only |
| 16–17 | Discovery operator is not inferred; the baseline records the actual discovery-start date | Operator identity not supplied |
| 30 | NUnit runner version is a declared package value and is corroborated in existing CI, not a local installation inventory | Operator installation not checked |
| 32–33 | Source ref and SHA have been selected from immutable repository evidence before any new checkout | No operator checkout |
| 38–40 | Compiler, output and metadata/import entries are tied to project XML rather than guessed effective defaults | Project XML read; local evaluation pending |
| 45–46 | Non-NuGet reference declarations and operation commands are separated from evaluated dependency resolution and execution | Source inspection only |
| 52–54 | Published artifacts, runtime requirements and compatibility checks are distinct; verified CI results retain their source SHA | No additional operator tests |
| 55–58 | Existing CI commands are identified as CI execution; local missing values, findings, item status and overall disposition are explicit | Overall baseline remains incomplete |
| 59–62 | No reviewer is invented; no review date is inferred; specific next action and deferred checks are documented | Formal owner review and Windows preflight pending |

The review is a **source and documentation validation**, not an assertion that all PowerShell commands have been run successfully on the operator's Windows machine. Commands for restore, Rebuild and tests require an agreed execution environment and side-effect approval.
