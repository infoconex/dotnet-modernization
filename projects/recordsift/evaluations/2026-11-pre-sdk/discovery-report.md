# RecordSift — Pre-SDK Modernization Discovery Report

**Investigation date:** November 2, 2026  
**Canonical production baseline:** `infoconex/RecordSift`, branch `main`, commit `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Scope:** .NET Framework 4.8, C# 7.3, ten traditional projects (five production; five NUnit 3 tests). No change to `main`, production code, target framework, language version, packages or released artifacts.

## A. Executive summary

The most valuable changes before SDK conversion are (1) bring the local `run_tests.ps1` entry point into parity with CI, as it omits the XLSX test assembly; (2) capture and enforce a build/test/API/package/resource compatibility baseline; (3) centralize genuinely identical compiler properties, beginning with `LangVersion=7.3`, using `Directory.Build.props` without changing import order; (4) publish the prerequisites and known build tools from a reproducible Windows container, distinguishing the VS IDE from Build Tools; (5) reconcile tooling assumptions such as Windows PowerShell 5.1 for the reflection-based API comparison.

**Proof:** an isolated Windows CI job centralized `LangVersion` across all ten projects, rebuilt, checked 425 API/package metadata entries and XML docs, validated an unpublished NuGet package, and reran NUnit: **419 discovered / 418 passed / 0 failed / 1 skipped**, both before and after. A separate .NET Framework SDK container reproduced the full build and tests. **A further controlled experiment using the official .NET 10 SDK Windows container, with neither Visual Studio IDE nor Build Tools installed, successfully restored dependencies, built all ten unchanged traditional projects using `dotnet msbuild`, and ran the same NUnit suite (419/418/0/1).** The experiments establish build/test feasibility without Build Tools for RecordSift, not necessarily that all packaging and validation scripts are Build Tools independent.

## B. Current repository assessment

| Project category | Findings |
|---|---|
| Production | RecordSift.Domain, RecordSift.Application, RecordSift.Infrastructure.Csv, RecordSift.Infrastructure.Xlsx, RecordSift.Infrastructure.Reporting |
| Tests | One NUnit test project corresponding to each production project |
| Framework and language | `TargetFrameworkVersion=v4.8`, `LangVersion=7.3` in ten `.csproj` files |
| Compilation | `OutputType=Library`, `AnyCPU`, Debug/Release, `WarningLevel=4`; traditional explicit `Compile` items |
| Common build | `Microsoft.CSharp.targets` imported in all ten; `Microsoft.Common.props` is reached transitively via the imported targets, not as an explicit early import |
| Production-specific | XML docs and warning `CS1591` treated as an error; preserve logical resource names |
| Assembly version | Production assembly identity and file version `0.1.0.0` |
| Dependencies | `packages.config`, restored using `nuget restore RecordSift.sln -PackagesDirectory packages -ConfigFile NuGet.Config`; dependency auditing already in CI |
| Package | Custom `packaging/RecordSift.nuspec`; five `lib/net48` DLLs and XML docs; README, MIT license, third-party notices, and pinned dependency declarations |
| Style | Existing `.editorconfig` with an IDE1006 naming gate executed by `dotnet format style` |
| Source baseline | GitHub Actions `windows-2022`, Visual Studio 2022 MSBuild, Windows PowerShell reflection validation, five NUnit suites, consumer test |

### Configuration inventory and centralization guidance

| Setting | Projects | Value(s) / usage | Candidate | Rationale |
|---|---:|---|---|---|
| `LangVersion` | 10 | `7.3` | **Yes — tested** | Identical, independently verified after extraction to shared props |
| `WarningLevel` | 10 | `4` | Yes, separately verify | Shared compiler convention |
| `TargetFrameworkVersion` | 10 | `v4.8` | Later | API verifier directly reads project XML; avoid altering source of metadata yet |
| `OutputType` | 10 | Library | Optional | No benefit unless consolidating substantial settings |
| Configuration/Platform | 10 | Debug, Release; AnyCPU | Not initially | Condition-based settings, solution mapping and output assumptions |
| `OutputPath` | 10 | Project-relative `bin/Debug`, `bin/Release` | No | Scripts, package staging and tests depend on layout |
| Debug/Release flags | 10 | Debug symbols, optimization, constants | Not initially | Conditional semantics; compare effective values before editing |
| `WarningsAsErrors` | 5 production | `1591` | Maybe under `src/` only | Test projects intentionally excluded; no urgent need |
| `DocumentationFile` | 5 production | Assembly-specific XML paths | No | Consumer package expects five named XML outputs |
| `AssemblyInfo.cs` | Multiple projects | Versioned assembly attributes; different titles, descriptions, COM metadata | No | Exact identity is compatibility contract; avoid generated duplicates in SDK migration |
| `EmbeddedResource.LogicalName` | Resource-bearing projects | Deliberate `RecordSift.Resources.*` names | No | Preserve identities during SDK conversion |
| `ProjectReference` | Various | Explicit project GUID metadata and references | No | Early Common.props import experiment broke project-reference resolution |
| Package versions | Package-owning projects | Pinned `packages.config` versions | No | Central packages file applies to `PackageReference`, not current system |

**Known direct coupling:** `scripts/verify_public_api.ps1` reads `$project.Project.PropertyGroup[0].TargetFrameworkVersion` rather than MSBuild's evaluated value. Therefore changes to framework declaration placement could trigger a false incompatibility report. `scripts/run_tests.ps1` assembles four DLLs, omitting `RecordSift.Infrastructure.Xlsx.Tests`, whereas CI runs five. Documentation mentions an older 379-test count; actual current baseline is 419.

**Resource identities to preserve:** `RecordSift.Resources.CsvMessages.resources`, `RecordSift.Resources.DomainMessages.resources`, `RecordSift.Resources.ReportingMessages.resources`.

## C. Clean-environment evaluation

### Existing GitHub runner (verified)

- Windows Server 2022 Datacenter, 10.0.20348 (runner image `20261026.347.1` on experimental run).
- Visual Studio 2022 Enterprise, MSBuild `17.14.60.43110`, `C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\MSBuild.exe`.
- C# compiler `4.14.0-3.26424.7` at `...\Bin\Roslyn\csc.exe`.
- Installed SDKs: `8.0.133`, `8.0.206`, `8.0.319`, `8.0.427`, `9.0.123`, `9.0.205`, `9.0.320`, `10.0.114`, `10.0.204`, `10.0.303`, `10.0.403`. Selected SDK `10.0.403`.
- NuGet CLI `7.9.0.83`, `C:\ProgramData\Chocolatey\bin\nuget.exe`.
- .NET Framework 4.8 reference assemblies present.
- Docker CLI and engine `29.7.2`, Windows containers.
- Relevant environment: `DOTNET_MULTILEVEL_LOOKUP=0`, `DOTNET_NOLOGO=1`, `DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1`, `RUNNER_OS=Windows`, `ImageOS=win22`.

### Windows container (verified)

A cached **historical** `mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2022` image was used strictly to prove feasibility, immutable digest `sha256:460dedaed73224f73ff10dc3ad754d0ed250aa57bcdf6c5052a811b4b7e29345`. It is **not currently a supported image tag**. The container started on a Windows Server 2022 GitHub runner using process isolation, mounted the source checkout, restored packages, compiled all ten projects and executed NUnit (419/418/0/1).

In-container inventory: VS **Build Tools** 2022 (no full IDE), MSBuild `17.14.23.42201`, NuGet `6.14.0.116`, .NET SDK `9.0.305`, .NET Framework 4.8 reference assemblies present. Windows build 20348. Thus: full IDE not required; Build Tools were in fact present.

Microsoft's **currently supported** `mcr.microsoft.com/dotnet/framework/sdk:4.8.1-windowsservercore-ltsc2022` registry manifest was verified to exist, but the image has not been pulled or executed. Future published examples should use that supported tag, resolve and record its immutable digest, and rerun the inventory and 419-test baseline.

### .NET SDK-only Windows container (verified, no Visual Studio or Build Tools)

**Actual image:** `mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022`, verified image digest `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25` (GitHub Actions [41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239)). A Windows Server 2022 host ran it successfully with **process isolation**. Container inventory: OS `10.0.20348`, SDK `10.0.403`, `dotnet msbuild` **18.9.15.52412**, compiler at `C:\Program Files\dotnet\sdk\10.0.403\Roslyn\bincore\csc.dll`, .NET 10 runtime `10.0.14`; **Visual Studio IDE absent, Build Tools absent, `MSBuild.exe` not found**. A .NET Framework runtime was present in Server Core; .NET Framework 4.8 targeting assemblies were initially absent. `Microsoft.NETFramework.ReferenceAssemblies.net48` version `1.0.3` and NuGet CLI `6.14.0.116` were added *only inside the disposable container*, not to the repository.

**Observed command sequence:**

1. `dotnet msbuild src/RecordSift.Domain/RecordSift.Domain.csproj /t:Rebuild /p:Configuration=Release ...` failed `MSB3644` (missing .NET Framework 4.8 reference assemblies), as expected.
2. Install `Microsoft.NETFramework.ReferenceAssemblies.net48` 1.0.3 using standalone NuGet CLI, locate its `build/.NETFramework/v4.8` directory, and pass `TargetFrameworkRootPath` and `FrameworkPathOverride` explicitly. The unchanged Domain project then **built successfully** with `dotnet msbuild`.
3. `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory C:\repo\packages -ConfigFile NuGet.Config` **passed**.
4. `dotnet msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /p:TargetFrameworkRootPath=... /p:FrameworkPathOverride=... /v:minimal` **passed** for all ten traditional projects.
5. `nunit3-console.exe` executed all five test assemblies **419 total / 418 passed / 0 failed / 1 skipped**.

This **establishes RecordSift compilation and NUnit execution without Visual Studio Build Tools**, while retaining Windows and the .NET Framework runtime. It does *not* yet establish that all existing packaging, public API reflection, XML negative-test and standalone-consumer scripts run without additional tool changes: those scripts were not exercised in this SDK-only container. The source branch is `discovery/sdk-only-20261102`, workflow commit `231ae63f8a0435dbc8a1b7a5a4319d4ec8bd0825`; diagnostic logs are [archived as run artifact](https://github.com/infoconex/RecordSift/actions/runs/41486238239/artifacts/13162920363).

For a published walkthrough, use the immutable digest or verify the image's digest at execution time; distinguish the independently installed framework reference assemblies from runtime/SDK components already present in the base image.

### Clean Windows VM (not executed)

Use when SDK-only container setup or constraints prevent isolating build dependencies. Start without Visual Studio or Build Tools; inventory each added component. Distinguish executable Windows/.NET Framework requirements from compile-only requirements.

Windows container rules: Windows host with Windows Engine, matching Server Core version for process isolation; Hyper-V isolation for appropriate mismatches only where virtualization is supported; Linux .NET containers cannot execute .NET Framework 4.8 test assemblies.

## D. Experimental evidence and result status

| Experiment | Environment | Result | Evidence |
|---|---|---|---|
| CI at baseline commit | Existing Windows runner | **Passed**: five projects and tests; 419 tests, 418 pass, 1 skip | [CI 41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| API gate, XML docs, unpublished package, consumer checks | Existing Windows runner | **Passed**: 425 API/metadata entries, DLL/XML docs, stable and prerelease consumers | [CI 41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910), [consumer 41392848814](https://github.com/infoconex/RecordSift/actions/runs/41392848814) |
| Run API gate via PowerShell 7 | Disposable runner | **Failed**: framework reflection differences (`ISpanFormattable`, `_Exception`); not evidence of RecordSift code regression | [probe 41483895096](https://github.com/infoconex/RecordSift/actions/runs/41483895096) |
| Run API gate via Windows PowerShell 5.1 | Disposable runner | **Passed**, identical approved baseline | [probe 41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| Legacy `dotnet msbuild` of Domain | VS-equipped runner | **Passed**; **does not** prove Build Tools independence | [probe 41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| Root `Directory.Build.props` custom evaluated property | Traditional project on Windows runner | **Passed**, custom marker imported without explicit early project import | [probe 41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| Root `Directory.Build.targets` custom target | Traditional project | **Passed** | [probe 41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| Add `Microsoft.Common.props` early to all projects | Disposable working copy | **Failed** `MSB3107` on many project-reference metadata records; reason still requires separate isolation | [probe 41484290488](https://github.com/infoconex/RecordSift/actions/runs/41484290488) |
| Centralize `LangVersion=7.3` without altering import order | Disposable working copy | **Passed**: ten-project rebuild; before/after NUnit 419/418/0/1; 425 API entries; XML docs; package | [probe 41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| Start Windows SDK container, inventory VS Build Tools | Docker on Windows runner | **Passed** | [container probe 41484601947](https://github.com/infoconex/RecordSift/actions/runs/41484601947) |
| Restore, build, and run NUnit within cached Windows SDK container | Docker on Windows runner | **Passed**: 419 tests, 418 pass, 0 fail, 1 skip | [container probe 41484891489](https://github.com/infoconex/RecordSift/actions/runs/41484891489) |
| Unmodified traditional Domain project in SDK-only container, without .NET Framework references | .NET 10 SDK Windows container, no Build Tools | **Failed as expected**: `MSB3644` targeting pack absent | [SDK-only probe 41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| Traditional Domain build after installing net48 reference assemblies | Same SDK-only container | **Passed**, no VS/Build Tools | [SDK-only probe 41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| Restore and rebuild all ten unchanged traditional projects via `dotnet msbuild` | Same SDK-only container | **Passed**, no VS/Build Tools | [SDK-only probe 41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| Run all five NUnit suites inside SDK-only container | Same SDK-only container | **Passed**: 419/418/0/1 | [SDK-only probe 41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| Run supported current 4.8.1 SDK image | Windows runner | **Not executed**; registry tag manifest verified only | Outstanding verification |
| SDK selection with disposable `global.json` | Windows runner | **Passed**: unpinned/fixed `10.0.403`; feature-band `10.0.303` + `latestFeature` resolved to `10.0.403`; deliberately nonexistent fixed SDK failed | [SDK-selection probe 41486700576](https://github.com/infoconex/RecordSift/actions/runs/41486700576) |
| Conditional shared property vs local project override | Disposable Windows checkout | **Passed**: unconditional shared `LangVersion=7.3` overwrote local 7.2; conditional shared default preserved local 7.2 | [SDK-selection probe 41486700576](https://github.com/infoconex/RecordSift/actions/runs/41486700576) |
| Formatter under proposed `global.json`, or rebuild with it | Disposable environment | **Not executed** | Required before recommending a permanent SDK pin |

**Experiment tracking:** Branch `discovery/pre-sdk-20261102` contains the temporary workflow (`main` untouched); successful run commit `0708839ada521c0ee606c70541201a8b28ed6a25` and [preprocessed/NUnit artifact](https://github.com/infoconex/RecordSift/actions/runs/41484769924/artifacts/13160583419). Branch `discovery/pre-sdk-container-20261102` contains the disposable container workflow; successful run commit `ea443d3e61de7ac8bc60d33e5d5c6abfb20f229c` and [container evidence run](https://github.com/infoconex/RecordSift/actions/runs/41484891489). Additional isolated workflows are on `discovery/sdk-only-20261102` and `discovery/props-sdk-selection-20261102`. All experimental branches should be deleted only after evidence is archived. No experiments were merged into `main`.

### Commands to reproduce

Run on Windows with the prerequisites inventoried, and keep scripts under their documented PowerShell version:

```powershell
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1

# Host/tool inventory
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber
& $msbuild -version -nologo
dotnet --list-sdks
dotnet --list-runtimes
dotnet --version
nuget help | Select-Object -First 3
docker version
docker info --format '{{.OSType}} {{.OperatingSystem}}'

# Restore, compile, inspect an unchanged traditional project
nuget restore RecordSift.sln -PackagesDirectory packages -ConfigFile NuGet.Config -NonInteractive
& $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
& $msbuild src/RecordSift.Domain/RecordSift.Domain.csproj '/pp:domain.pp.xml' /p:Configuration=Release
& $msbuild src/RecordSift.Domain/RecordSift.Domain.csproj '-getProperty:LangVersion' /p:Configuration=Release
& $msbuild RecordSift.sln '/bl:RecordSift.binlog' /p:Configuration=Release

# Public API check uses Windows PowerShell 5.1 reflection semantics
powershell.exe -NoProfile -NonInteractive -File scripts/verify_public_api.ps1

# The existing scripts/run_tests.ps1 is NOT the complete test suite: it omits XLSX.
$runner = '.\packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe'
$assemblies = @('Domain','Application','Infrastructure.Csv','Infrastructure.Reporting','Infrastructure.Xlsx') |
  ForEach-Object { "tests\RecordSift.$_.Tests\bin\Release\RecordSift.$_.Tests.dll" }
& $runner @assemblies '--result=TestResults/all-nunit.xml;format=nunit3' --noheader
```

The source-controlled experimental workflows include the temporary property movement, preprocessed project files, exact command invocations, and NUnit XML. Be careful not to treat `MSBuild` output zip/package cryptographic hashes as a stable compatibility oracle: package timestamps, staging and metadata can change hashes while behavior and contract remain the same.

## E. Modernization opportunity matrix

Ratings use High / Medium / Low for **immediate benefit**, **risk**, **effort**, **SDK preparation**, and **lasting value**. High risk is undesirable; a high benefit is desirable.

| Opportunity | Benefit | Risk | Effort | SDK prep | Lasting value | Classification |
|---|---|---|---|---|---|---|
| Fix local all-tests command to include XLSX | High | Low | Low | High | High | **Before SDK** |
| Inventory toolchain, API/resources/package and output contract | High | Low | Low–Med | High | High | **Before SDK** |
| Centralize `LangVersion` in root `Directory.Build.props` | High | Low in proven POC | Low | High | High | **Before SDK** |
| Centralize verified same `WarningLevel` | Medium | Low | Low | Medium | High | **Before SDK** |
| Supported SDK image for reproducible builds | High | Low–Med | Medium | High | High | **Before SDK** |
| Standardize API validation host/runtime | High | Low–Med | Low–Med | High | High | **Before SDK** |
| Consolidate simple tool discovery and local instructions | Medium | Low–Med | Medium | Medium | High | **Optional before SDK** |
| Feature-band `global.json` after formatter validation | Medium | Low–Med | Low | Medium | High | **Optional before SDK** |
| Review current `.editorconfig` / NuGet.Config | Medium | Low | Low | Medium | High | **Before SDK, inspection only** |
| Add `Directory.Build.targets` with synthetic checks | Low | Medium | Medium | Low | Low | **Not recommended** |
| Add `.rsp` / `.Solution.*` without an observed need | Low | Medium | Low–Med | Low | Low | **Not recommended** |
| Add early Common.props import to all projects | Low | High (observed failure) | Medium | Low | Low | **Not recommended** |
| Eliminate Build Tools from the build/test command | High | Low–Med, POC verified | Medium | High | High | **Optional before SDK; verified feasible** |
| `packages.config` → `PackageReference` | Primarily migration | Medium–High | Medium | High | High | **During SDK migration** |
| `Directory.Packages.props` | Later | Medium | Medium | High | High | **With PackageReference** |
| Automatic assembly metadata and default resource globs | Low now | High | Medium | High | High | **During SDK migration** |

## F. Recommended execution order

1. **Preserve baseline evidence and align local testing:** correct the four-versus-five test project discrepancy; execute all 419 tests. Capture 425-entry API baseline, five XML documentation files, five DLL identities, embedded resources, .nuspec, consumer sample parity. Do not alter framework/version.
2. **Document baseline tool discovery:** make the exact NuGet, MSBuild, compiler and test dependencies explicit. Keep API reflection validation on Windows PowerShell 5.1 unless the checker is independently made runtime-invariant.
3. **Introduce the minimal tested root `Directory.Build.props`:** centralize `LangVersion=7.3` only; no early import; test effective property in all 10; rerun build, tests, XML, API, package and consumers.
4. **Review optional additional repeated compiler settings** one at a time. Preserve project-level overrides. Do not centralize `TargetFrameworkVersion` until `verify_public_api.ps1` no longer reads raw XML.
5. **Reproduce on a currently supported 4.8.1 Windows SDK image**, pin image digest, document tools and repeat full tests; avoid recommending an unsupported cached tag.
6. **Document and independently reproduce the successful SDK-only Windows build** from the immutable official .NET SDK image, standalone NuGet CLI and net48 reference assemblies. Then test existing API/package/consumer verification scripts separately; do not assume those are already tool-independent.
7. **Optionally control .NET SDK selection** after testing formatter/workspace compatibility and CI provisions suitable SDKs.
8. **Move to SDK-style and package management conversion in separate, future phases.** Preserve assembly attributes, resources, API surface and custom packaging semantics.

**Verification gates at every substantive change:** restore → full Release build → 419 NUnit discovery / 418 passing / 1 expected skip → 425 API/metadata entries → XML documentation → assembly/resource identity comparison → local `.nupkg` validation → clean installed-package consumer checks. For tool-only changes, rerun the applicable gates and record omissions.

## G. Recommended article series

The introductory article should be an overview and navigation page. Six standalone, tightly scoped practical follow-ups:

1. **Start with evidence: baseline a .NET Framework application** — prerequisites: RecordSift checkout/Windows. Exercise: restore, compile, all five NUnit suites, API/package/consumer checks. Outcome: known-safe point of comparison. Verify: 419/418/0/1, 425 API entries.
2. **What does MSBuild really import? Understanding traditional project evaluation** — prerequisites: baseline; MSBuild. Exercise: `/pp`, `-getProperty`, compare Common.props import position and Directory.Build props/targets probes. Outcome: explain import timing and overrides. Verify: marker/target evaluation; no source change.
3. **Centralize common properties safely with Directory.Build.props** — prerequisites: previous two. Exercise: isolated movement of `LangVersion=7.3` from 10 projects, no early import. Outcome: one value to maintain, preserved behavior. Verify: effective property, build, 419 tests, 425 API entries, package.
4. **Build .NET Framework in a Windows container—and know exactly what's installed** — prerequisites: Windows Docker host. Exercise: supported Server Core 2022 4.8.1 SDK container; inventory/digest, restore, compile, five test suites. Outcome: reproducible environment, understand Build Tools vs full IDE. Verify: tools and test parity.
5. **Do traditional .NET Framework projects need Visual Studio Build Tools?** — prerequisites: Windows containers and pinned .NET SDK image. Exercise: SDK-only image with intentional missing-reference-assembly failure, add only NuGet and net48 targeting references, build traditional projects using `dotnet msbuild` and run five test assemblies. Outcome: demonstrated ability to eliminate Build Tools for RecordSift compilation/tests, while retaining Windows/.NET Framework. Verify: exact digest, inventory and 419/418/0/1 results. **Experiment verified; publication should also document remaining script limitations.**
6. **Protect the contracts SDK conversion can accidentally change** — prerequisites: baseline. Exercise: assembly identity, explicit resources, generated AssemblyInfo, XML docs, `packages.config` and hand-built nuspec inventory. Outcome: migration acceptance criteria. Verify: API/resource/dependency/package parity.

Place `Directory.Build.targets`, `.editorconfig`, `NuGet.Config`, `global.json` and `.rsp` in appropriate comparison sidebars or an integrated repository configuration article rather than five thin articles. The SDK-style conversion and PackageReference migration belong to a subsequent series.

## H. Open questions and risks

- **Build Tools independence:** **resolved for build and NUnit tests** with official .NET 10 SDK Windows container; still **unverified for all validation/packaging scripts**, especially `verify_xml_documentation.ps1` and `verify_clean_consumer.ps1` which use Visual Studio discovery/compiler paths.
- **Supported image:** the supported current `4.8.1-windowsservercore-ltsc2022` tag exists but must be pulled and exercised; publish its immutable image digest.
- **Early import:** `MSB3107` project-reference metadata errors when artificially importing Common.props early; isolate root cause if early properties are ever genuinely needed. Do not make this a prerequisite for the proven LangVersion centralization.
- **API verifier runtime sensitivity:** PowerShell 7 reflection produces framework API differences; fix validation runtime or code before broadening tooling support.
- **`global.json`:** SDK selection and roll-forward were verified, including absent-SDK failure; formatter compatibility under pinning and a pinned complete build were not tested. Current formatter logs workspace-loading warnings. Do not add a repository-level pin solely from selection behavior.
- **Local test parity:** XLSX is omitted from `scripts/run_tests.ps1`; the current CI all-project run is authoritative.
- **Raw XML coupling:** target framework is read from project XML by API script; shared property movement can produce misleading failures.
- **NuGet migration:** separate top-level and transitive dependencies, preserve the `.nuspec` explicit dependency graph and standalone consumer behavior.
- **Distribution:** locally validated stable and RC packages do not imply permission to publish; no external release actions were taken.
- **Experimental branches:** four disposable branches remain for evidence; archive logs and delete when appropriate; none were merged.

## I. Recommended next action

**First ensure the documented local `All` test command runs all five projects, including XLSX; rerun the complete baseline and CI.** This is an independent low-risk improvement and a necessary safety prerequisite for modernization.

Then, **implement the already proven minimal `Directory.Build.props` centralization of `LangVersion=7.3`**, preserving the existing import order, and run the full verification suite. It provides immediate maintenance value—one place to update a currently identical compiler setting—and remains useful during and after SDK conversion.

### Primary sources

- Microsoft, [Customize the build by folder](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory)
- Microsoft, [Customize solution builds](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-solution-build)
- Microsoft, [MSBuild build logs](https://learn.microsoft.com/en-us/visualstudio/msbuild/obtaining-build-logs-with-msbuild)
- Microsoft, [.NET Framework SDK container images](https://github.com/microsoft/dotnet-framework-docker/blob/main/README.sdk.md)
- Microsoft, [Windows container version compatibility](https://learn.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility)
- Microsoft, [`global.json`](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json)
- Microsoft, [NuGet Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/Central-Package-Management)
- Microsoft, [Upgrade Assistant deprecation](https://learn.microsoft.com/en-us/dotnet/core/porting/upgrade-assistant-how-to-upgrade)
- Microsoft, [default `dotnet new` templates](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-new-sdk-templates)
- `dotnet/try-convert`, [archived repository](https://github.com/dotnet/try-convert)
