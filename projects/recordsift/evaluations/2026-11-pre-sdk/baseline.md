# RecordSift — Verified baseline

**Repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Branch / full commit:** main / `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Verification date:** November 2, 2026

## Source and project inventory

Five production projects: RecordSift.Domain, RecordSift.Application, RecordSift.Infrastructure.Csv, RecordSift.Infrastructure.Xlsx, and RecordSift.Infrastructure.Reporting. Five corresponding NUnit test projects.

All ten use traditional, non-SDK-style `*.csproj` files, `TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, `OutputType=Library`, `AnyCPU`, `WarningLevel=4`, explicit compile/reference items, Debug/Release configurations, and imports of `Microsoft.CSharp.targets`.

Production-specific configuration generates XML documentation and enforces `CS1591` for documentation. Production assembly version is `0.1.0.0`. Preserve exact assembly and file metadata, project dependency ordering, output layouts, and per-assembly XML docs.

### Repository identity and immutable source snapshot (November 3, 2026 inventory)

The **application identity** is distinct from its Git hosting details and from the published package identity. Values below were inspected in the **unchanged** application tree at `8358780829458854a4b0356df5ac5e685f0a34c8`. GitHub metadata was observed on November 3, 2026; hosting settings can change and are **not** inferred from a source commit.

| Field | Observed value / source |
|---|---|
| Git host / repository kind | GitHub, public, original (not fork), not archived; Git source control |
| Repository / owner | `infoconex/RecordSift` |
| Browser URL | [https://github.com/infoconex/RecordSift](https://github.com/infoconex/RecordSift) |
| HTTPS clone | `https://github.com/infoconex/RecordSift.git` |
| SSH clone | `git@github.com:infoconex/RecordSift.git` |
| Default branch | `main`; baseline pinned to `8358780829458854a4b0356df5ac5e685f0a34c8` |
| Source tree character | One repository with one traditional Visual Studio solution and ten project files; **not** ten independently versioned repositories |
| GitHub description | No repository description set at inspection; application description is taken from the checked-in README, **not invented from metadata** |
| Application | RecordSift: reusable Windows-only net48 CSV/XLSX import, schema/mapping/validation, diagnostics and reporting **class library**; no web service, UI or standalone executable ([README](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/README.md)) |
| License | MIT (`LICENSE`) |
| Published version | Public `RecordSift` NuGet package **0.1.0** (release identity per README); the **tracked** `packaging/RecordSift.nuspec` still declares **0.1.0-rc.1** |
| Compiled assembly identity | Production `AssemblyVersion` **0.1.0.0**; `AssemblyFileVersion` **0.1.0.0** observed in `Properties/AssemblyInfo.cs` (separate from the NuGet version) |
| Supported application/runtime | Windows / .NET Framework **4.8**; source uses C# **7.3** |
| Existing separate branch changes | A previously authorized test-runner fix exists on `release/0.2` (PR #258), **not** on this immutable `main` snapshot |

**Version provenance matters:** Git tag/release, NuGet package version, tracked nuspec metadata, assembly/file versions, solution format, project `ToolsVersion`, installed MSBuild version and SDK version are different concepts. Record each separately; do not infer build behavior solely from the declaration.

### Repository directory and configuration-file inventory

The Git tree has one `.sln`, **zero `.slnx`**, ten `.csproj`, three `.resx`, seven `packages.config`, and eight GitHub Actions workflows. The source includes six PowerShell `.ps1` scripts and six Python `.py` validation scripts; this is a *tracked source inventory*, not proof that every script runs in every workflow.

| Location | Baseline responsibility / noteworthy contents |
|---|---|
| `src/` | Five production assemblies under Domain, Application, Infrastructure.Csv, Infrastructure.Xlsx and Infrastructure.Reporting |
| `tests/` | Five corresponding NUnit test assemblies; `tests/ReleaseConsumer/` contains independent consumer assets |
| `docs/` | Requirements, scenarios, specifications, architecture/ADRs, compatibility snapshot, testing, release, samples and usage |
| `scripts/` | Local NUnit runner, release candidate packaging, public API/XML validation, consumer checks and Python source/metadata guards |
| `packaging/` | `RecordSift.nuspec` and packaging documentation; source package version and distribution files |
| `.github/workflows/` | Eight checked-in workflows covering Windows build/test, dependency/security, consumer, docs, stress/adversarial and release operations |
| `.github/ISSUE_TEMPLATE/`, `.github/agents/` | Issue and repository-specific AI workflows |
| Repository root | `RecordSift.sln`, `.editorconfig`, `.gitignore`, `NuGet.Config`, `AGENTS.md`, `README.md`, `LICENSE`, `THIRD-PARTY-NOTICES.md` |

**Pre-existing modernization/configuration mechanisms at the frozen commit:**

| Mechanism | Baseline state | Implication for later evaluation |
|---|---|---|
| `.editorconfig` | **Present** at root: UTF-8/LF, indentation, C# style and naming rules; CI invokes Roslyn `IDE1006` | Inspect and preserve existing semantic style rules before proposing replacements |
| `NuGet.Config` | **Present**: nuget.org restore and vulnerability-audit sources | Capture effective feeds, authentication dependencies and restore behavior; do not expose credentials |
| `packages.config` | **Present, 7 files** (CSV and XLSX adapters, all five test projects) | Legacy package declaration model; baseline for EXP-011–013 |
| `Directory.Build.props` | **Absent** (no tracked copy at any level) | EXP-002/005 introduce **temporary experimental** shared defaults; absence is not a recommendation to add |
| `Directory.Build.targets` | **Absent** | EXP-006 and targets source audit found no demonstrated shared custom target requirement |
| `global.json` | **Absent** | No repo-specific .NET SDK pin; EXP-005/008 test temporary candidate pins |
| `Directory.Packages.props` | **Absent** | No central NuGet package-version management |
| `Directory.Solution.props`, `Directory.Solution.targets`, `Directory.Solution.rsp` | **Absent** | No tracked solution-level shared MSBuild customization |
| `Directory.Build.rsp` | **Absent** | No tracked shared build command-line response file |
| `.globalconfig`, `.ruleset` | **Absent** | Existing analyzer enforcement lives in `.editorconfig` and CI |
| `packages.lock.json` | **Absent** | `packages.config` version pins are **not** a resolved-graph lockfile |
| `.gitattributes` | **Absent** | No tracked repository-specific Git attributes |
| `.gitignore` | **Present**; excludes `.vs/`, `bin/`, `obj/`, `packages/`, `TestResults/`, user files and `*.nupkg` | Build outputs and package downloads are not part of tracked source |
| `AGENTS.md`, `.github/copilot-instructions.md` | **Present** | Preserve repository engineering/AI instructions when investigating source changes |

**Scope rule:** "Absent" means **no tracked file in this Git tree**. Imported toolchain defaults, machine-wide NuGet settings, environment variables or generated files may still affect actual builds. Document declared configuration, **evaluated configuration**, and host/tool provenance separately.

### Solution topology and declared compatibility

| Solution attribute | Frozen source declaration |
|---|---|
| Solution file / kind | `RecordSift.sln`, classic Visual Studio solution; **no `.slnx`** |
| Solution file format | `Microsoft Visual Studio Solution File, Format Version 12.00` |
| Declared Visual Studio generation | `# Visual Studio Version 16`; `VisualStudioVersion = 16.0.28701.123` |
| Declared minimum VS version | `MinimumVisualStudioVersion = 10.0.40219.1` (**declaration**, not a verified working toolchain) |
| Project representation | Ten C# project entries with legacy C# project type GUID `{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}` |
| Solution build configurations | `Debug|Any CPU`, `Release|Any CPU`; all ten projects mapped to ActiveCfg and Build.0 for both |
| Project XML/tools version | Traditional MSBuild XML namespace; `ToolsVersion="15.0"`, `DefaultTargets="Build"`; `Microsoft.CSharp.targets` explicit import |
| Project-level configuration | Conditional `Debug|AnyCPU` and `Release|AnyCPU` settings; solution **"Any CPU"** spelling differs from project **"AnyCPU"** and MSBuild platform mapping |
| Output and target | Every project `OutputType=Library`, `TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, default `Platform=AnyCPU` |
| Actual verified CI compiler | Preinstalled Visual Studio 2022 MSBuild **17.14.60.43110** on `windows-2022` in EXP-001; *not* the old declared solution/ToolsVersion |
| CI SDK/restore tools | SDK **10.0.403**, NuGet CLI **7.9.0.83** observed in EXP-001 environment; these are separate tools with separate provenance |

A solution's **Visual Studio version line is not the compiler version**; `ToolsVersion` is not the target framework; `AssemblyVersion` is not the package version. For .NET solutions in other repositories, inspect `.slnx` if it exists, and enumerate every `.sln`/`.slnx` and every `.csproj` **including projects omitted from solution files**. Do not infer which project configurations actually compile from project names alone; check solution mappings and evaluated MSBuild properties.

### Individual project inventory and source reference topology

All ten entries below have `OutputType=Library`, net48, C# 7.3, `ToolsVersion=15.0`, Debug/Release AnyCPU and distinct `AssemblyName`/`RootNamespace`. References below are **declared direct project references**, not necessarily the transitive runtime closure.

| Project (`src/` or `tests/`) | Role / direct project references | Noteworthy external/source contract |
|---|---|---|
| `src/RecordSift.Domain` | Production domain; **no project references** | System/System.Core; `RecordSift.Resources.DomainMessages.resources` |
| `src/RecordSift.Application` | Production orchestration; `Domain` | System/System.Core; `RecordSift.Resources.CsvMessages.resources` |
| `src/RecordSift.Infrastructure.Csv` | Production CSV adapter; `Application`, `Domain` | CsvHelper and pinned compatibility libraries through `HintPath` |
| `src/RecordSift.Infrastructure.Xlsx` | Production XLSX adapter; `Application`, `Domain` | ExcelDataReader 3.9.0, compression/XML/framework refs |
| `src/RecordSift.Infrastructure.Reporting` | Production reporting; `Application`, `Domain` | `RecordSift.Resources.ReportingMessages.resources` |
| `tests/RecordSift.Domain.Tests` | NUnit tests; `Domain` | `NUnit 3.14.0`; `IsTestProject=true` |
| `tests/RecordSift.Application.Tests` | NUnit tests; `Application`, `Domain` | `NUnit 3.14.0`; `IsTestProject=true` |
| `tests/RecordSift.Infrastructure.Csv.Tests` | NUnit tests; `Application.Tests`, `Infrastructure.Csv`, `Application`, `Domain` | Noteworthy test-to-test project reference; NUnit |
| `tests/RecordSift.Infrastructure.Xlsx.Tests` | NUnit tests; `Infrastructure.Xlsx`, `Application`, `Domain` | NUnit and framework compression/XML references |
| `tests/RecordSift.Infrastructure.Reporting.Tests` | NUnit tests; `Infrastructure.Csv`, `Infrastructure.Reporting`, `Application`, `Domain` | Noteworthy cross-adapter **test** dependency on CSV; NUnit |

**Explicit project GUIDs** identify projects in this traditional solution. Preserve the one-to-one mapping of name, path, GUID, project type and solution configuration during any project-format conversion; [RecordSift.sln at baseline](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/RecordSift.sln) is the source of record. An inventory should also flag projects **outside** solution files, unsupported/cross-target project references, project cycles, package vendor leaks across architecture layers, missing referenced files, imported source files, analyzers, generated resources and pre/post-build events when present.

**Source items and behavior:** Project files contain explicit `Compile` items, compiler defines/optimization/debug settings, `Reference`/`HintPath` and `ProjectReference` paths, and production-only `DocumentationFile`/`WarningsAsErrors=1591` XML contracts. Three production projects include explicit `EmbeddedResource` logical names. Such details can be silently changed by SDK default globbing, implicit SDK assembly attributes or resource-name generation. The project-property audit below retains their configuration distinctions.

### Restore/build/verification workflow entry points

| Operation | Baseline source / command | Actual verification status |
|---|---|---|
| Restore | `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config` | **Executed** in existing Windows CI; `packages.config` is the source format |
| Release build | `msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release "/p:Platform=Any CPU"` | **Executed** in existing CI using VS `vswhere` discovery of MSBuild |
| Full NUnit | `.github/workflows/windows-net48.yml` runs all five test DLLs using `packages/NUnit.ConsoleRunner.3.17.0/tools/nunit3-console.exe` | **419 discovered / 418 passed / 0 failed / 1 skipped** |
| Local filtered NUnit | `scripts/run_tests.ps1` invokes a pinned runner and emits NUnit XML | **Original baseline script omits XLSX**; previously corrected on `release/0.2` only |
| API identity | `scripts/verify_public_api.ps1`; `docs/compatibility/public-api-net48.txt` | **425 API/metadata entries**, using Windows PowerShell 5.1, compiled DLLs and raw csproj/`packages.config` reads |
| Production XML | `scripts/verify_xml_documentation.ps1`; five production XML docs and negative CS1591 CI control | Verified in original VS-backed CI; later SDK-only experiments have their own separate outcomes |
| Package generation | `scripts/build_release_candidate.ps1`, `packaging/RecordSift.nuspec` | **Unpublished** local package/metadata validation in CI; no publication authorized by this evaluation |
| Clean consumers | `scripts/verify_clean_consumer.ps1` and `.github/workflows/verify-rc-consumer.yml` | Baseline package install and executable consumers verified using VS-dependent tool discovery |
| Source/architecture checks | `scripts/validate_*.py`, `.editorconfig` IDE1006 via `dotnet format style` | Observed in CI; some validators interpret raw legacy `Reference`/source XML and/or inspect generated `obj` files post-build (EXP-013) |
| Documentation validation | `.github/workflows/validate-docs.yml` uses an Ubuntu runner | Source validation distinct from Windows compilation/test |
| Release automation | `.github/workflows/prepare-0.1-release.yml`, `publish-release.yml` and release recovery workflows | **Documented workflow definitions only**; their presence is not authority to publish |

**CI/automation inventory:** eight tracked workflows: `windows-net48.yml`, `verify-rc-consumer.yml`, `validate-docs.yml`, `adversarial-extended.yml`, `extended-adversarial.yml`, `prepare-0.1-release.yml`, `publish-release.yml`, and `recover-recordsift-0.1-release.yml`. Record triggers, branch filters, OS, commands, tool discovery, secret/feed assumptions, release permissions and actual run status **per workflow**, rather than declaring all eight verified.

**Declared vs executed:** This expanded inventory comes from files/GitHub metadata; the EXP-001 CI results are the separate **executed evidence**. An absent tracked SDK pin does not prove no SDK is installed; a solution minimum-VS declaration does not prove it builds with VS 2010; green NUnit does not establish total coverage; and successful corrected EXP-009 consumer commands do not make unchanged scripts compatible. Do not rerun already sufficient evidence merely to populate an inventory.

### Actual repeated settings — complete project-property audit (November 3, 2026)

**Method:** source-only inspection of all five production and five test `.csproj` files from `RecordSift/research/dotnet-modernization`, pinned to `8358780829458854a4b0356df5ac5e685f0a34c8` (identical to the frozen `main`). Reviewed each unconditional, Debug, and Release `PropertyGroup`; this table concerns values **declared in project XML**, not all properties evaluated by MSBuild or the behavior of hypothetical configurations. No new build was run for this audit.

| Property | Exact baseline declaration / coverage | Research disposition |
|---|---|---|
| `LangVersion` | `7.3` in **10/10**, unconditional | **First candidate:** identical and previously verified in [EXP-002](experiments/EXP-002-shared-properties.md). Use conditional shared default to preserve overrides; see [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md). |
| `WarningLevel` | `4` in Debug and Release for **10/10** (**20** declarations) | **Optional lower-priority candidate:** identical but grouped by `Configuration\|Platform`; unconditional placement changes nonstandard configurations. [EXP-010](experiments/EXP-010-warninglevel-centralization.md) later verified an explicitly scoped conditional default, overrides, Debug/Release build and consumer gates. Adoption is not authorized. |
| `TargetFrameworkVersion` | `v4.8` in **10/10**, unconditional | **Keep local:** `scripts/verify_public_api.ps1` reads its raw project-XML location. Moving it changes the validator's inputs before any framework migration. |
| `Configuration`, `Platform` | Unconditional defaults `Debug` and `AnyCPU`, respectively, in **10/10** | **Keep local:** the conditional Debug/Release property groups are evaluated before RecordSift's current late `Directory.Build.props` import. Late defaults cannot retroactively activate a group that already evaluated. |
| `OutputType` | `Library` in **10/10** | **Keep local:** little practical benefit; retain explicit project identity/shape until a distinct need is established. |
| `DebugSymbols` | `true` in Debug for **10/10**; no explicit Release value | **Keep local:** absence in Release is part of the declared pattern. |
| `DebugType` | `full` (Debug), `pdbonly` (Release), **10/10** | **Keep local:** compiler/PDB behavior is configuration-specific; no centralization test. |
| `Optimize` | `false` (Debug), `true` (Release), **10/10** | **Keep local:** changes compilation behavior; avoid coupling to unrelated modernization. |
| `DefineConstants` | `DEBUG;TRACE` (Debug), `TRACE` (Release), **10/10** | **Keep local:** part of configuration-specific compiled behavior and source conditional compilation. |
| `OutputPath` | `bin\Debug\` and `bin\Release\`, **10/10** | **Keep local:** existing build scripts, NUnit discovery, package staging, and consumer checks rely on these paths. |
| `DocumentationFile` | Per-project `bin\{Debug\|Release}\RecordSift.<Component>.xml` in **5/5 production projects only**; absent from test projects | **Keep local:** exact XML output paths are contract/packaging inputs; file name is project-specific and intended production-only. |
| `WarningsAsErrors` | `1591` in Debug and Release for **5/5 production** projects only; absent in tests | **Keep local for now:** preserves compiler `CS1591` behavior only for public production APIs; don't equate with enabling `TreatWarningsAsErrors` everywhere. |
| `IsTestProject` | `true` in **5/5 test** projects only | **Keep local:** it distinguishes test from production projects; a nested `tests/Directory.Build.props` would require explicit composition with root defaults if both are used. |
| `FileAlignment` | `512` in **8/10**; absent in two projects | **Keep local:** do not infer that absent declarations can be safely replaced with an explicit common value without checking evaluated defaults/output metadata. |
| `AppDesignerFolder` | `Properties` in **6/10**; absent in four projects | **Keep local:** not a uniform setting, little modernization value. |
| `ProjectGuid` | Unique GUID in **10/10** | **Never homogenize:** project identity. |
| `AssemblyName`, `RootNamespace` | Distinct names in **10/10** | **Keep local:** identity, resource names and API/packaging compatibility; avoid assumption that a derived name is equivalent. |

Additional non-property distinctions (explicit `Compile`, `Reference`, `ProjectReference`, `EmbeddedResource`/`LogicalName` items, and `packages.config`) are outside the scope of shared compiler defaults. Each of the ten projects imports `$(MSBuildToolsPath)\Microsoft.CSharp.targets`, with no other explicit targets import.

### Why source duplication does not imply safe property movement

1. **Current import order matters.** [EXP-006](experiments/EXP-006-msbuild-imports.md) found that `Directory.Build.props` is imported **late** in these particular traditional projects, via the existing targets chain. An early `Microsoft.Common.props` import attempt failed (`MSB3107`). Do not generalize this late timing to all MSBuild or SDK-style projects.
2. **A shared default must respect project overrides.** EXP-005 showed that unconditional shared `LangVersion=7.3` overwrote a test project-level `7.2`; conditional assignment `Condition="'$(LangVersion)' == ''"` retained it. The exact proposed `Directory.Build.props` is *illustrative, not committed*:

   ```xml
   <Project>
     <PropertyGroup>
       <LangVersion Condition="'$(LangVersion)' == ''">7.3</LangVersion>
     </PropertyGroup>
   </Project>
   ```

3. **Not all shared values are available at the right time.** Do not move `Configuration`/`Platform` defaults into a file imported after project configuration groups have been evaluated; this could affect which groups apply. Retaining `TargetFrameworkVersion`, project identities, XML documentation paths, resource logical names and output paths avoids known toolchain/API/consumer dependencies.
4. **Keep experiments atomic.** The verified scope for EXP-002 is `LangVersion` in a Release parity run (419 discovered / 418 passed / 0 failed / 1 intentionally skipped, 425 API/metadata entries, XML and local package validation); other property moves and Debug parity are **not verified** by that run. `WarningLevel` was later evaluated separately in [EXP-010](experiments/EXP-010-warninglevel-centralization.md), including Debug/Release build, conditional Custom *property evaluation*, override, XML/assembly and clean consumer checks; **arbitrary Custom configurations were not compiled**. Recheck actual evaluated values with `MSBuild -getProperty` and import locations with `/pp`.

## NuGet and packaging

`NuGet.Config` explicitly defines sources/audit sources. Dependencies are declared in pinned `packages.config` files. CI uses standalone `nuget restore`. Packaging is defined by `packaging/RecordSift.nuspec`, including five `lib/net48` DLLs, XML documentation, README/license/notices and explicit dependencies.

Important resource identities:
- `RecordSift.Resources.CsvMessages.resources`
- `RecordSift.Resources.DomainMessages.resources`
- `RecordSift.Resources.ReportingMessages.resources`

### Legacy dependency graph and package/source version snapshot

[EXP-011](experiments/EXP-011-nuget-dependency-inventory.md) reconciles the **seven** declared `packages.config` files, **17 package entries**, **13 unique restored package IDs**, **13 existing HintPath DLL files**, and **11 exact-pinned production dependencies** declared in the hand-authored `RecordSift.nuspec`. The source/package distinction matters: NuGet package metadata, direct vs transitive project references, selected restore versions and exact assembly file locations are different questions.

Examples of exact versions in the tracked package metadata include CsvHelper **33.1.0**, ExcelDataReader **3.9.0**, System.Memory **4.5.5**, System.Buffers **4.5.1**, System.Runtime.CompilerServices.Unsafe **6.0.0**, Microsoft.Bcl.AsyncInterfaces **8.0.0**, and Microsoft.Bcl.HashCode **1.1.1**. NUnit **3.14.0** and the separate NUnit.ConsoleRunner **3.17.0** are test/tool dependencies, not production package dependencies. `NuGet.Config` explicitly points package and audit sources to nuget.org.

**Risk exposed by baseline scope:** [EXP-012](experiments/EXP-012-packagereference-isolation.md) later demonstrated that reducing migrated references to apparent direct dependencies can silently select four **older** transitive versions even when NUnit passes. The baseline must capture **effective restore versions** as well as declarations before dependency/format changes. `packages.config` is not a lockfile. Security/audit status is time-specific, not a guarantee about future vulnerabilities.

## Baseline verification

| NUnit assembly | Discovered | Passed | Skipped |
|---|---:|---:|---:|
| Domain.Tests | 123 | 123 | 0 |
| Application.Tests | 62 | 62 | 0 |
| Infrastructure.Csv.Tests | 132 | 131 | 1 |
| Infrastructure.Reporting.Tests | 54 | 54 | 0 |
| Infrastructure.Xlsx.Tests | 48 | 48 | 0 |
| **Total** | **419** | **418** | **1** |

**Failed tests: 0.** The CSV skip is intentional, not an unexpected test failure. Existing validation confirms **425 public-API/packaging-metadata entries**, generated XML documentation and NuGet packaging. Existing CI also ran clean local package consumer and engineering-documentation workflows.

- [Main Windows build and tests](https://github.com/infoconex/RecordSift/actions/runs/41392848910)
- [Clean Windows consumer](https://github.com/infoconex/RecordSift/actions/runs/41392848814)
- [Engineering docs validation](https://github.com/infoconex/RecordSift/actions/runs/41392848879)

## Known documentation and script inconsistencies

- At the frozen main SHA, `scripts/run_tests.ps1` locally runs **four** assemblies, omitting Infrastructure.Xlsx.Tests, while main CI runs **five**. The previously approved [PR #258](https://github.com/infoconex/RecordSift/pull/258) corrected this **on `release/0.2` only**. Use the five-suite baseline for research; no duplicate fix or application branch promotion is authorized by this evaluation.
- Some engineering documentation says **379 tests**; the observed total is **419**.
- `scripts/verify_public_api.ps1` reads `$project.Project.PropertyGroup[0].TargetFrameworkVersion` from raw XML. Moving framework declaration to imported props would require first updating the checker to use evaluated MSBuild properties.
- The Windows PowerShell 5.1 host is significant for API verification: an initial experimental use of PowerShell 7 produced spurious reflection differences.

## Expected compatibility gates

Restore → Release build all ten projects → full five-suite NUnit (419/418/0/1) → 425-entry API/metadata baseline → assembly and embedded-resource identity checks → XML docs → package layout and dependency checks → clean installed-package consumer tests.

Do not interpret changed binary hashes or timestamps as compatibility failure unless deterministic equality is part of an explicit requirement.
