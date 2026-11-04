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

| Project | Role | Format | Framework | C# | Output | Platform | ToolsVersion | Direct project references |
|---|---|---|---|---|---|---|---|---|
| [`RecordSift.Domain`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Domain/RecordSift.Domain.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | — |
| [`RecordSift.Application`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Application/RecordSift.Application.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Domain` |
| [`RecordSift.Infrastructure.Csv`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Infrastructure.Xlsx`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Infrastructure.Reporting`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | Production | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Domain.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Domain` |
| [`RecordSift.Application.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Application`, `Domain` |
| [`RecordSift.Infrastructure.Csv.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Application.Tests`, `Infrastructure.Csv`, `Application`, `Domain` |
| [`RecordSift.Infrastructure.Xlsx.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Infrastructure.Xlsx`, `Application`, `Domain` |
| [`RecordSift.Infrastructure.Reporting.Tests`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | Test | Traditional | `v4.8` | `7.3` | `Library` | `AnyCPU` | `15.0` | `Infrastructure.Csv`, `Infrastructure.Reporting`, `Application`, `Domain` |

### Project-specific configuration

One row per project; Debug and Release are side-by-side **columns**. `—` means a value is **not declared** in that project/configuration, not that the evaluated value is empty.

**Compiler settings**

| Project | DebugType (Debug) | DebugType (Release) | Optimize (Debug) | Optimize (Release) | DefineConstants (Debug) | DefineConstants (Release) | DebugSymbols (Debug) | DebugSymbols (Release) |
|---|---|---|---|---|---|---|---|---|
| `Domain` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Application` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Infrastructure.Csv` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Infrastructure.Xlsx` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Infrastructure.Reporting` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Domain.Tests` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Application.Tests` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Infrastructure.Csv.Tests` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Infrastructure.Xlsx.Tests` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |
| `Infrastructure.Reporting.Tests` | `full` | `pdbonly` | `false` | `true` | `DEBUG;TRACE` | `TRACE` | `true` | — |

**Output and validation settings**

| Project | OutputPath (Debug) | OutputPath (Release) | WarningLevel (Debug) | WarningLevel (Release) | WarningsAsErrors (Debug) | WarningsAsErrors (Release) | DocumentationFile (Debug) | DocumentationFile (Release) |
|---|---|---|---|---|---|---|---|---|
| `Domain` | `bin\Debug\` | `bin\Release\` | `4` | `4` | `1591` | `1591` | `bin\Debug\RecordSift.Domain.xml` | `bin\Release\RecordSift.Domain.xml` |
| `Application` | `bin\Debug\` | `bin\Release\` | `4` | `4` | `1591` | `1591` | `bin\Debug\RecordSift.Application.xml` | `bin\Release\RecordSift.Application.xml` |
| `Infrastructure.Csv` | `bin\Debug\` | `bin\Release\` | `4` | `4` | `1591` | `1591` | `bin\Debug\RecordSift.Infrastructure.Csv.xml` | `bin\Release\RecordSift.Infrastructure.Csv.xml` |
| `Infrastructure.Xlsx` | `bin\Debug\` | `bin\Release\` | `4` | `4` | `1591` | `1591` | `bin\Debug\RecordSift.Infrastructure.Xlsx.xml` | `bin\Release\RecordSift.Infrastructure.Xlsx.xml` |
| `Infrastructure.Reporting` | `bin\Debug\` | `bin\Release\` | `4` | `4` | `1591` | `1591` | `bin\Debug\RecordSift.Infrastructure.Reporting.xml` | `bin\Release\RecordSift.Infrastructure.Reporting.xml` |
| `Domain.Tests` | `bin\Debug\` | `bin\Release\` | `4` | `4` | — | — | — | — |
| `Application.Tests` | `bin\Debug\` | `bin\Release\` | `4` | `4` | — | — | — | — |
| `Infrastructure.Csv.Tests` | `bin\Debug\` | `bin\Release\` | `4` | `4` | — | — | — | — |
| `Infrastructure.Xlsx.Tests` | `bin\Debug\` | `bin\Release\` | `4` | `4` | — | — | — | — |
| `Infrastructure.Reporting.Tests` | `bin\Debug\` | `bin\Release\` | `4` | `4` | — | — | — | — |

**Project-wide metadata**

| Project | Default Configuration | IsTestProject | FileAlignment | AppDesignerFolder | C# targets import |
|---|---|---|---|---|---|
| `Domain` | `Debug` | — | `512` | `Properties` | `Microsoft.CSharp.targets` |
| `Application` | `Debug` | — | `512` | `Properties` | `Microsoft.CSharp.targets` |
| `Infrastructure.Csv` | `Debug` | — | `512` | `Properties` | `Microsoft.CSharp.targets` |
| `Infrastructure.Xlsx` | `Debug` | — | — | — | `Microsoft.CSharp.targets` |
| `Infrastructure.Reporting` | `Debug` | — | `512` | — | `Microsoft.CSharp.targets` |
| `Domain.Tests` | `Debug` | `true` | `512` | `Properties` | `Microsoft.CSharp.targets` |
| `Application.Tests` | `Debug` | `true` | `512` | `Properties` | `Microsoft.CSharp.targets` |
| `Infrastructure.Csv.Tests` | `Debug` | `true` | `512` | `Properties` | `Microsoft.CSharp.targets` |
| `Infrastructure.Xlsx.Tests` | `Debug` | `true` | — | — | `Microsoft.CSharp.targets` |
| `Infrastructure.Reporting.Tests` | `Debug` | `true` | `512` | — | `Microsoft.CSharp.targets` |

The values above are declared in the frozen source, not measured by an independent MSBuild property-evaluation run.

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

### NuGet dependencies

RecordSift uses `packages.config` for project dependency declarations and [`RecordSift.nuspec`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/packaging/RecordSift.nuspec) for distributable package metadata. Recorded `.nuspec` dependency versions:

| Package | Declared version |
|---|---|
| `CsvHelper` | `33.1.0` |
| `ExcelDataReader` | `3.9.0` |
| `Microsoft.Bcl.AsyncInterfaces` | `8.0.0` |
| `Microsoft.Bcl.HashCode` | `1.1.1` |
| `Microsoft.CSharp` | `4.7.0` |
| `System.Memory` | `4.5.5` |
| `System.Buffers` | `4.5.1` |
| `System.Numerics.Vectors` | `4.5.0` |
| `System.Runtime.CompilerServices.Unsafe` | `6.0.0` |
| `System.Threading.Tasks.Extensions` | `4.5.4` |
| `System.ValueTuple` | `4.5.0` |

| Attribute | Value |
|---|---|
| Project dependency declaration format | `packages.config` |
| NuGet package source | nuget.org |
| NuGet audit source | nuget.org |
| Test framework version | NUnit `3.14.0` |
| Test runner version | NUnit.ConsoleRunner `3.17.0` |
| Package output framework | `net48` |

[EXP-011](experiments/EXP-011-nuget-dependency-inventory.md) records the package-declaration and resolved-reference inventory.

### Build environment

| Attribute | Observed value |
|---|---|
| CI build OS | Windows Server 2022 (`windows-2022` runner) |
| Visual Studio | 2022 Enterprise (preinstalled on runner) |
| MSBuild version | `17.14.60.43110` |
| .NET SDK version observed | `10.0.403` |
| NuGet CLI version observed | `7.9.0.83` |

### Build and verification entry points

| Operation | Command or script |
|---|---|
| Restore | `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config` |
| Release build | `msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release "/p:Platform=Any CPU"` |
| Full suite | [`.github/workflows/windows-net48.yml`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/.github/workflows/windows-net48.yml) |
| Local tests | `scripts/run_tests.ps1` |
| Public API verification | `scripts/verify_public_api.ps1` |
| XML documentation verification | `scripts/verify_xml_documentation.ps1` |
| Package creation | `scripts/build_release_candidate.ps1` |
| Consumer verification | [`.github/workflows/verify-rc-consumer.yml`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/.github/workflows/verify-rc-consumer.yml) |
| Documentation checks | [`.github/workflows/validate-docs.yml`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/.github/workflows/validate-docs.yml) |
| C# naming checks | `dotnet format style` with `IDE1006` |

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

| Compatibility gate | Result | Evidence |
|---|---|---|
| NuGet restore | Passed | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Release solution build | Passed; ten projects | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| NUnit tests | Passed; see assembly-level counts above | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Public API compatibility | Passed; included in the **425-entry combined API/metadata snapshot** | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Assembly identity | Passed as part of the API/metadata snapshot; no standalone count | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Embedded resource identity | Separate comparison not recorded in EXP-001 | [Pinned project files](https://github.com/infoconex/RecordSift/tree/8358780829458854a4b0356df5ac5e685f0a34c8/src) |
| Package metadata | Passed as part of the API/metadata snapshot; no standalone count | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| XML documentation | Passed; five production XML documents | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| NuGet package contents | Passed; unpublished release-candidate package | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Pinned dependency validation | Passed | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| NuGet vulnerability audit | Passed for the baseline run | [Windows CI #41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Installed NuGet package consumer | Passed | [Consumer CI #41392848814](https://github.com/infoconex/RecordSift/actions/runs/41392848814) |
| Engineering documentation validation | Passed | [Documentation CI #41392848879](https://github.com/infoconex/RecordSift/actions/runs/41392848879) |

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

**Future comparisons:** Reuse the applicable gates above, record any check not executed, and compare observable contracts rather than raw binary hashes unless deterministic byte identity is explicitly required.

