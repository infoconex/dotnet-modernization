# RecordSift — Verified application baseline

**Source:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift) · `main@8358780829458854a4b0356df5ac5e685f0a34c8`  
**Verification:** November 2, 2026 · **Source inventory:** November 3, 2026  
**Status:** Source inventory verified; existing Windows CI compatibility baseline verified. Evaluated MSBuild properties and unexecuted variants are **not** assumed verified.

This document records **the unchanged starting state**, not proposed modernization work. Technical explanations and recommendations are maintained in [experiments](experiments/README.md), [findings](findings.md), and the [roadmap](roadmap.md).

## 1. Application overview

RecordSift is a Windows-only .NET Framework 4.8 class library for importing CSV/XLSX records, schema mapping, validation, diagnostics and reporting. It is distributed through NuGet. [Application README](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/README.md).

| Attribute | Value |
|---|---|
| Application name | RecordSift |
| Application type | Class library |
| Git host | GitHub |
| Git repository | `infoconex/RecordSift` |
| Visibility | Public |
| Repository URL | [infoconex/RecordSift](https://github.com/infoconex/RecordSift) |
| HTTPS clone URL | `https://github.com/infoconex/RecordSift.git` |
| SSH clone URL | `git@github.com:infoconex/RecordSift.git` |
| Default branch | `main` |
| Baseline commit | `8358780829458854a4b0356df5ac5e685f0a34c8` |
| License | MIT |
| Supported operating system | Windows |
| Published NuGet version | `0.1.0` |
| Tracked `.nuspec` version | `0.1.0-rc.1` |
| Production assembly version | `0.1.0.0` |
| Production file version | `0.1.0.0` |

## 2. Solution and projects

### Solution

| Attribute | Value |
|---|---|
| Solution file | [`RecordSift.sln`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/RecordSift.sln) |
| Solution format | Visual Studio `.sln` |
| Format version | `12.00` |
| Declared Visual Studio version | `16.0.28701.123` |
| Declared minimum Visual Studio version | `10.0.40219.1` |
| Debug configuration | `Debug\|Any CPU` |
| Release configuration | `Release\|Any CPU` |

### Projects

Each project appears separately; settings are taken from its own `.csproj` at the baseline commit. Direct references are shown by project suffix (for example, `Domain` means `RecordSift.Domain`).

| Project | Role | Format | Framework | C# | Output | ToolsVersion | Direct project references |
|---|---|---|---|---|---|---|---|
| [`RecordSift.Domain`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Domain/RecordSift.Domain.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | — |
| [`RecordSift.Application`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Application/RecordSift.Application.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Domain` |
| [`RecordSift.Infrastructure.Csv`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Infrastructure.Xlsx`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Infrastructure.Reporting`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Domain.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Domain` |
| [`RecordSift.Application.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Infrastructure.Csv.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Application.Tests`, `Infrastructure.Csv`, `Application`, `Domain` |
| [`RecordSift.Infrastructure.Xlsx.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Infrastructure.Xlsx`, `Application`, `Domain` |
| [`RecordSift.Infrastructure.Reporting.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `15.0` | `Infrastructure.Csv`, `Infrastructure.Reporting`, `Application`, `Domain` |

### Project-specific configuration

A dash means **not declared in that project**, not necessarily an evaluated default. `WarningLevel`, `WarningsAsErrors` and XML documentation settings shown are declared in Debug/Release configurations.

| Project | WarningLevel | WarningsAsErrors | XML docs | IsTestProject | FileAlignment | AppDesignerFolder |
|---|---|---|---|---|---|---|
| `Domain` | `4` | `1591`, `1591` | Yes | — | `512` | `Properties` |
| `Application` | `4` | `1591`, `1591` | Yes | — | `512` | `Properties` |
| `Infrastructure.Csv` | `4` | `1591`, `1591` | Yes | — | `512` | `Properties` |
| `Infrastructure.Xlsx` | `4` | `1591`, `1591` | Yes | — | — | — |
| `Infrastructure.Reporting` | `4` | `1591`, `1591` | Yes | — | `512` | — |
| `Domain.Tests` | `4` | — | No | `true` | `512` | `Properties` |
| `Application.Tests` | `4` | — | No | `true` | `512` | `Properties` |
| `Infrastructure.Csv.Tests` | `4` | — | No | `true` | `512` | `Properties` |
| `Infrastructure.Xlsx.Tests` | `4` | — | No | `true` | — | — |
| `Infrastructure.Reporting.Tests` | `4` | — | No | `true` | `512` | — |

### Settings declared consistently across all ten projects

| Setting | Debug | Release |
|---|---|---|
| Default configuration | `Debug` | `Debug` (if not overridden) |
| Default platform | `AnyCPU` | `AnyCPU` |
| `DebugType` | `full` | `pdbonly` |
| `Optimize` | `false` | `true` |
| `DefineConstants` | `DEBUG;TRACE` | `TRACE` |
| `OutputPath` | `bin\\Debug\\` | `bin\\Release\\` |

All ten projects explicitly import `$(MSBuildToolsPath)\\Microsoft.CSharp.targets`. Production projects declare per-project XML documentation paths; the test projects do not. The tables describe **source declarations**, not independently evaluated MSBuild values.

## 3. Repository structure and configuration

### Directory structure

| Directory | Purpose |
|---|---|
| `src/` | Production source code |
| `tests/` | Automated tests and consumer verification |
| `docs/` | Requirements, specifications, architecture and user/release documentation |
| `scripts/` | Build, test, validation and packaging scripts |
| `packaging/` | NuGet package definition |
| `.github/` | Repository workflows, contribution templates and automation instructions |

### Existing configuration files

| File or mechanism | Present | Current purpose |
|---|---|---|
| `.editorconfig` | Yes | Formatting, C# style and IDE1006 naming rules |
| `NuGet.Config` | Yes | NuGet restore and audit sources |
| `packages.config` | Yes | Per-project NuGet dependencies |
| `.gitignore` | Yes | Ignored build, test and package outputs |
| `AGENTS.md` | Yes | Engineering instructions |
| `.github/copilot-instructions.md` | Yes | Copilot instructions |
| `Directory.Build.props` | No | — |
| `Directory.Build.targets` | No | — |
| `Directory.Build.rsp` | No | — |
| `Directory.Solution.props` | No | — |
| `Directory.Solution.targets` | No | — |
| `Directory.Packages.props` | No | — |
| `global.json` | No | — |
| `packages.lock.json` | No | — |

“Present” means tracked in the baseline commit; generated, imported and machine-wide settings are outside this source inventory.

## 4. Dependencies and build

### Dependencies and packaging

| Area | Starting state / source |
|---|---|
| NuGet declaration | Seven `packages.config`, **17 entries**, **13 unique package IDs**; **13 explicit DLL `HintPath` references**; [EXP-011](experiments/EXP-011-nuget-dependency-inventory.md) |
| Production package dependencies | **11 exact-pinned `net48` dependencies** in [`RecordSift.nuspec`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/packaging/RecordSift.nuspec), including CsvHelper 33.1.0, ExcelDataReader 3.9.0, System.Memory 4.5.5, System.Buffers 4.5.1, Unsafe 6.0.0, Microsoft.Bcl.AsyncInterfaces 8.0.0, Microsoft.Bcl.HashCode 1.1.1 |
| Test framework / runner | NUnit **3.14.0**, separate NUnit.ConsoleRunner **3.17.0** |
| Package contents | Five `lib/net48` DLLs and five XML docs, README, license, third-party notices |
| NuGet feeds | `NuGet.Config`: nuget.org package and audit sources |

### Verified build environment and entry points

| Component / operation | Baseline |
|---|---|
| CI OS and tool provenance | GitHub-hosted `windows-2022` (Windows Server 2022); Visual Studio 2022 Enterprise tooling **preinstalled** |
| Actual MSBuild | **17.14.60.43110**, discovered through Visual Studio `vswhere` in Windows CI |
| Installed SDK / NuGet CLI | SDK **10.0.403**; NuGet CLI **7.9.0.83** (environment inventory, **not** a repository SDK pin) |
| Restore | `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config` |
| Release build | `msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release "/p:Platform=Any CPU"` |
| Full NUnit | All five assemblies from `.github/workflows/windows-net48.yml` |
| API / XML validation | `scripts/verify_public_api.ps1` (**Windows PowerShell 5.1**); `scripts/verify_xml_documentation.ps1` |
| Package and consumer checks | `scripts/build_release_candidate.ps1`; `scripts/verify_clean_consumer.ps1` |
| Style and source guards | `dotnet format style` / IDE1006, Python architecture/test/metadata/documentation guards |

## 5. Verification results

EXP-001 established the historical **Release** baseline against the pinned unchanged application source, using Visual Studio-backed Windows CI. These are executed results, not simply project XML declarations.

| NUnit assembly | Discovered | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| Domain.Tests | 123 | 123 | 0 | 0 |
| Application.Tests | 62 | 62 | 0 | 0 |
| Infrastructure.Csv.Tests | 132 | 131 | 0 | 1 |
| Infrastructure.Reporting.Tests | 54 | 54 | 0 | 0 |
| Infrastructure.Xlsx.Tests | 48 | 48 | 0 | 0 |
| **Total** | **419** | **418** | **0** | **1** |

| Compatibility gate | Verified baseline / evidence |
|---|---|
| Restore, full Release build, NUnit, XML docs, API/package metadata | [Windows build and test run #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910); **425 API/metadata entries**, **five production XML docs** |
| Clean installed-package consumers | [Consumer run #41392848814](https://github.com/infoconex/RecordSift/actions/runs/41392848814) |
| Engineering documentation checks | [Docs run #41392848879](https://github.com/infoconex/RecordSift/actions/runs/41392848879) |

The skipped CSV test is deliberate. The CI baseline included Visual Studio; it does **not** prove that Visual Studio Build Tools are required to build the application. SDK-only experiments have separate evidence.

## 6. Known issues and verification gaps

| Observation | Baseline implication |
|---|---|
| `scripts/run_tests.ps1` runs four suites, omitting XLSX, at the frozen `main` commit | CI runs **all five**; previously authorized [RecordSift PR #258](https://github.com/infoconex/RecordSift/pull/258) corrected the local runner on **`release/0.2` only** |
| Some legacy engineering documentation says **379 tests** | Verified baseline is **419 discovered / 418 passed / 0 failed / 1 skipped** |
| API verifier reads raw project XML and `packages.config` | Format/configuration changes may require a separately evaluated compatibility-check update ([EXP-012](experiments/EXP-012-packagereference-isolation.md), [EXP-013](experiments/EXP-013-migration-tooling-ci-readiness.md)) |
| API verifier depends on Windows PowerShell **5.1** | A PowerShell 7 attempt produced spurious reflection differences; retain host provenance |
| Project properties were inventoried from source XML | Not a complete evaluated-property inventory for every Configuration/Platform combination |
| Existing CI proves Release compatibility in a tool-rich environment | Not proof of arbitrary custom/Debug gates, SDK-only negative cases, or cross-platform runtime support |

**Comparison contract for future changes:** Restore → complete Release build → five NUnit suites → 425-entry API/metadata check → assembly/resource identities → XML documentation → NuGet layout/dependencies → clean consumer verification, with every executed, failed and omitted gate recorded. Do not require byte-identical hashes unless deterministic identity is an explicit contract.

