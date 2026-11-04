# RecordSift — Verified application baseline

**Source:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift) · `main@8358780829458854a4b0356df5ac5e685f0a34c8`  
**Verification:** November 2, 2026 · **Source inventory:** November 3, 2026  
**Status:** Source inventory verified; existing Windows CI compatibility baseline verified. Evaluated MSBuild properties and unexecuted variants are **not** assumed verified.

This document records **the unchanged starting state**, not proposed modernization work. Technical explanations and recommendations are maintained in [experiments](experiments/README.md), [findings](findings.md), and the [roadmap](roadmap.md).

## 1. Application overview

RecordSift is an MIT-licensed, Windows-only **.NET Framework 4.8 class library** for CSV/XLSX import, schema mapping, validation, diagnostics and reporting. Consumers install its NuGet package; it has no standalone UI, service or executable. See the [application README](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/README.md).

| Attribute | Baseline value |
|---|---|
| Source host / type | GitHub; public Git repository; single solution with multiple related class-library projects; not a fork or archived |
| Repository / browse | `infoconex/RecordSift` · [repository](https://github.com/infoconex/RecordSift) |
| Clone (HTTPS / SSH) | `https://github.com/infoconex/RecordSift.git` · `git@github.com:infoconex/RecordSift.git` |
| Default branch / frozen commit | `main` / `8358780829458854a4b0356df5ac5e685f0a34c8` |
| License | MIT |
| Framework / language / runtime | .NET Framework **4.8** / C# **7.3** / **Windows** |
| Published NuGet package | `RecordSift` **0.1.0**, per README and public release |
| Tracked `.nuspec` package version | **0.1.0-rc.1** in `packaging/RecordSift.nuspec` |
| Production assembly / file versions | **0.1.0.0** / **0.1.0.0**, from `Properties/AssemblyInfo.cs` |
| Repository description field | Unset on GitHub at inventory time; description above comes from source README |

Source revision and public GitHub metadata were inspected separately; the latter may change. The published NuGet version, tracked `.nuspec` version and compiled assembly versions are **different version identifiers**.

## 2. Repository inventory

| Path | Contents |
|---|---|
| `src/` | Five production projects: Domain, Application, CSV, XLSX, Reporting |
| `tests/` | Five NUnit project suites; `ReleaseConsumer/` assets |
| `docs/` | Requirements, specifications, architecture, compatibility, testing, release and usage documentation |
| `scripts/` | Restore-related validation, test runner, API/XML checks, packaging and consumer checks |
| `packaging/` | `RecordSift.nuspec` and package documentation |
| `.github/workflows/` | Eight build, test, documentation, consumer, stress and release workflows |
| Repository root | `RecordSift.sln`, `NuGet.Config`, `.editorconfig`, `.gitignore`, `AGENTS.md`, `README.md`, `LICENSE`, `THIRD-PARTY-NOTICES.md` |

The pinned Git tree contains **one `.sln`**, **no `.slnx`**, **ten `.csproj`**, **three `.resx`**, **seven `packages.config`**, **six `.ps1`**, **six `.py`** and **eight GitHub Actions workflows**. No project file lies outside the one solution.

### Existing configuration files

Inventory reflects **tracked files in the frozen commit**, not machine-wide or generated settings.

| Mechanism | State | Current use / location |
|---|---|---|
| `.editorconfig` | Present | Root style, formatting and IDE1006 naming enforcement |
| `NuGet.Config` | Present | nuget.org restore and vulnerability-audit feeds |
| `packages.config` | Present (7) | CSV and XLSX production adapters and all five test projects |
| `.gitignore` | Present | Excludes `.vs/`, `bin/`, `obj/`, `packages/`, `TestResults/`, `*.nupkg`, user files |
| `AGENTS.md`, `.github/copilot-instructions.md` | Present | Repository-specific engineering/AI instructions |
| `Directory.Build.props`, `Directory.Build.targets`, `Directory.Build.rsp` | Absent | No tracked shared MSBuild configuration |
| `Directory.Solution.props`, `.targets`, `.rsp` | Absent | No tracked solution-level customization |
| `global.json` | Absent | No tracked repository-level SDK pin |
| `Directory.Packages.props`, `packages.lock.json` | Absent | No tracked central versions or dependency lockfile |
| `.globalconfig`, `.ruleset`, `.gitattributes` | Absent | No tracked files of these types |

Absence is an **observation**, not a recommendation to introduce a file. See [EXP-002–EXP-013](experiments/README.md) for evaluation of particular mechanisms.

## 3. Solution and projects

### Solution identity

| Attribute | Declared value |
|---|---|
| Solution | [`RecordSift.sln`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/RecordSift.sln) (classic Visual Studio `.sln`; no `.slnx`) |
| Solution format | **12.00** |
| Declared Visual Studio version | **16**; `VisualStudioVersion=16.0.28701.123` |
| Declared minimum Visual Studio version | `10.0.40219.1` |
| Project entries | Ten traditional C# projects, type GUID `{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}` |
| Solution configurations | `Debug\|Any CPU`, `Release\|Any CPU`; all ten projects included in both builds |
| Project format / tool declaration | Traditional MSBuild XML, `ToolsVersion=15.0`, `DefaultTargets=Build`, `Microsoft.CSharp.targets` import |

These are **source declarations**. The actual CI MSBuild compiler/version is recorded in Section 4. Solution `Any CPU` maps to project `AnyCPU`.

### Project inventory and direct references

All ten projects declare **`TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, `OutputType=Library`, `AnyCPU`**, distinct `AssemblyName`/`RootNamespace` and project GUIDs. Every project uses explicit `Compile`/`Reference` items rather than SDK default item globs. Names below represent paths under `src/` or `tests/`; references are **direct project references**, not transitive runtime dependency claims.

| Project | Layer | Direct project references | Noteworthy declarations |
|---|---|---|---|
| `RecordSift.Domain` | Production | None | Domain messages resource |
| `RecordSift.Application` | Production | Domain | CSV messages resource |
| `RecordSift.Infrastructure.Csv` | Production | Application, Domain | CsvHelper/vendor compatibility assemblies |
| `RecordSift.Infrastructure.Xlsx` | Production | Application, Domain | ExcelDataReader, framework compression/XML |
| `RecordSift.Infrastructure.Reporting` | Production | Application, Domain | Reporting messages resource |
| `RecordSift.Domain.Tests` | NUnit tests | Domain | `IsTestProject=true` |
| `RecordSift.Application.Tests` | NUnit tests | Application, Domain | `IsTestProject=true` |
| `RecordSift.Infrastructure.Csv.Tests` | NUnit tests | Application.Tests, Infrastructure.Csv, Application, Domain | Test-to-test project reference |
| `RecordSift.Infrastructure.Xlsx.Tests` | NUnit tests | Infrastructure.Xlsx, Application, Domain | NUnit; compression/XML refs |
| `RecordSift.Infrastructure.Reporting.Tests` | NUnit tests | Infrastructure.Csv, Infrastructure.Reporting, Application, Domain | Cross-adapter test reference |

Project-specific paths/GUIDs are in the pinned [solution](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/RecordSift.sln) and [`src/`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/src) / [`tests/`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/tests) project files. Three production `EmbeddedResource` logical names are `RecordSift.Resources.DomainMessages.resources`, `RecordSift.Resources.CsvMessages.resources` and `RecordSift.Resources.ReportingMessages.resources`.

### Project configuration inventory

Source-only audit of all ten `.csproj` files at the pinned commit; values below are **declared**, not a separate MSBuild property-evaluation run.

| Property or group | Declared values and coverage |
|---|---|
| `LangVersion`; `TargetFrameworkVersion`; `OutputType` | `7.3`; `v4.8`; `Library` — **10/10** |
| `Configuration`; `Platform` defaults | `Debug`; `AnyCPU` — **10/10** |
| `WarningLevel` | `4` — **20 declarations** (Debug/Release × 10 projects) |
| `DebugSymbols` | `true` in Debug — **10/10**; no explicit Release value |
| `DebugType`; `Optimize` | Debug: `full`/`false`; Release: `pdbonly`/`true` — **10/10** |
| `DefineConstants` | Debug `DEBUG;TRACE`; Release `TRACE` — **10/10** |
| `OutputPath` | `bin\\Debug\\` and `bin\\Release\\` — **10/10** |
| `DocumentationFile`; `WarningsAsErrors` | Five production projects only: per-assembly Debug/Release XML file paths; `1591` in both configurations; absent from tests |
| `IsTestProject` | `true` in the five test projects only |
| `FileAlignment`; `AppDesignerFolder` | `512` in **8/10**; `Properties` in **6/10**, respectively |
| `ProjectGuid`; `AssemblyName`; `RootNamespace` | Unique or project-specific identity in all ten projects |

The `scripts/verify_public_api.ps1` compatibility verifier directly reads the first raw project `PropertyGroup` for `TargetFrameworkVersion`; it does **not** resolve imported MSBuild properties. The import timing/override behavior of shared files is investigated separately in [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md) and [EXP-006](experiments/EXP-006-msbuild-imports.md).

## 4. Dependencies and build

### Dependencies and packaging

| Area | Starting state / source |
|---|---|
| NuGet declaration | Seven `packages.config`, **17 entries**, **13 unique package IDs**; **13 explicit DLL `HintPath` references**; [EXP-011](experiments/EXP-011-nuget-dependency-inventory.md) |
| Production package dependencies | **11 exact-pinned `net48` dependencies** in [`RecordSift.nuspec`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/packaging/RecordSift.nuspec), including CsvHelper 33.1.0, ExcelDataReader 3.9.0, System.Memory 4.5.5, System.Buffers 4.5.1, Unsafe 6.0.0, Microsoft.Bcl.AsyncInterfaces 8.0.0, Microsoft.Bcl.HashCode 1.1.1 |
| Test framework / runner | NUnit **3.14.0**, separate NUnit.ConsoleRunner **3.17.0** |
| Package contents | Five `lib/net48` DLLs and five XML docs, README, license, third-party notices |
| NuGet feeds | `NuGet.Config`: nuget.org package and audit sources |

Version declarations are not equivalent to the **effective resolved package graph**. That difference was tested in [EXP-012](experiments/EXP-012-packagereference-isolation.md); do not treat a `packages.config` pin as a lockfile.

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

Eight tracked workflows: `windows-net48.yml`, `verify-rc-consumer.yml`, `validate-docs.yml`, `adversarial-extended.yml`, `extended-adversarial.yml`, `prepare-0.1-release.yml`, `publish-release.yml`, `recover-recordsift-0.1-release.yml`. Source definitions are in [`.github/workflows/`](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/.github/workflows). Documentation CI also uses `ubuntu-latest`. **Workflow presence is not proof that every defined gate has executed.**

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

