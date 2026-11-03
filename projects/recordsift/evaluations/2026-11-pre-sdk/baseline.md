# RecordSift — Verified baseline

**Repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Branch / full commit:** main / `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Verification date:** November 2, 2026

## Source and project inventory

Five production projects: RecordSift.Domain, RecordSift.Application, RecordSift.Infrastructure.Csv, RecordSift.Infrastructure.Xlsx, and RecordSift.Infrastructure.Reporting. Five corresponding NUnit test projects.

All ten use traditional, non-SDK-style `*.csproj` files, `TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, `OutputType=Library`, `AnyCPU`, `WarningLevel=4`, explicit compile/reference items, Debug/Release configurations, and imports of `Microsoft.CSharp.targets`.

Production-specific configuration generates XML documentation and enforces `CS1591` for documentation. Production assembly version is `0.1.0.0`. Preserve exact assembly and file metadata, project dependency ordering, output layouts, and per-assembly XML docs.

### Actual repeated settings — complete project-property audit (November 3, 2026)

**Method:** source-only inspection of all five production and five test `.csproj` files from `RecordSift/research/dotnet-modernization`, pinned to `8358780829458854a4b0356df5ac5e685f0a34c8` (identical to the frozen `main`). Reviewed each unconditional, Debug, and Release `PropertyGroup`; this table concerns values **declared in project XML**, not all properties evaluated by MSBuild or the behavior of hypothetical configurations. No new build was run for this audit.

| Property | Exact baseline declaration / coverage | Research disposition |
|---|---|---|
| `LangVersion` | `7.3` in **10/10**, unconditional | **First candidate:** identical and previously verified in [EXP-002](experiments/EXP-002-shared-properties.md). Use conditional shared default to preserve overrides; see [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md). |
| `WarningLevel` | `4` in Debug and Release for **10/10** (**20** declarations) | **Second candidate only:** identical but grouped by `Configuration|Platform`; moving to an unconditional file could also affect nonstandard configurations. No isolated parity experiment yet. |
| `TargetFrameworkVersion` | `v4.8` in **10/10**, unconditional | **Keep local:** `scripts/verify_public_api.ps1` reads its raw project-XML location. Moving it changes the validator's inputs before any framework migration. |
| `Configuration`, `Platform` | Unconditional defaults `Debug` and `AnyCPU`, respectively, in **10/10** | **Keep local:** the conditional Debug/Release property groups are evaluated before RecordSift's current late `Directory.Build.props` import. Late defaults cannot retroactively activate a group that already evaluated. |
| `OutputType` | `Library` in **10/10** | **Keep local:** little practical benefit; retain explicit project identity/shape until a distinct need is established. |
| `DebugSymbols` | `true` in Debug for **10/10**; no explicit Release value | **Keep local:** absence in Release is part of the declared pattern. |
| `DebugType` | `full` (Debug), `pdbonly` (Release), **10/10** | **Keep local:** compiler/PDB behavior is configuration-specific; no centralization test. |
| `Optimize` | `false` (Debug), `true` (Release), **10/10** | **Keep local:** changes compilation behavior; avoid coupling to unrelated modernization. |
| `DefineConstants` | `DEBUG;TRACE` (Debug), `TRACE` (Release), **10/10** | **Keep local:** part of configuration-specific compiled behavior and source conditional compilation. |
| `OutputPath` | `bin\\Debug\\` and `bin\\Release\\`, **10/10** | **Keep local:** existing build scripts, NUnit discovery, package staging, and consumer checks rely on these paths. |
| `DocumentationFile` | Per-project `bin\\{Debug|Release}\\RecordSift.<Component>.xml` in **5/5 production projects only**; absent from test projects | **Keep local:** exact XML output paths are contract/packaging inputs; file name is project-specific and intended production-only. |
| `WarningsAsErrors` | `1591` in Debug and Release for **5/5 production** projects only; absent in tests | **Keep local for now:** preserves compiler `CS1591` behavior only for public production APIs; don't equate with enabling `TreatWarningsAsErrors` everywhere. |
| `IsTestProject` | `true` in **5/5 test** projects only | **Keep local:** it distinguishes test from production projects; a nested `tests/Directory.Build.props` would require explicit composition with root defaults if both are used. |
| `FileAlignment` | `512` in **8/10**; absent in two projects | **Keep local:** do not infer that absent declarations can be safely replaced with an explicit common value without checking evaluated defaults/output metadata. |
| `AppDesignerFolder` | `Properties` in **6/10**; absent in four projects | **Keep local:** not a uniform setting, little modernization value. |
| `ProjectGuid` | Unique GUID in **10/10** | **Never homogenize:** project identity. |
| `AssemblyName`, `RootNamespace` | Distinct names in **10/10** | **Keep local:** identity, resource names and API/packaging compatibility; avoid assumption that a derived name is equivalent. |

Additional non-property distinctions (explicit `Compile`, `Reference`, `ProjectReference`, `EmbeddedResource`/`LogicalName` items, and `packages.config`) are outside the scope of shared compiler defaults. Each of the ten projects imports `$(MSBuildToolsPath)\\Microsoft.CSharp.targets`, with no other explicit targets import.

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
4. **Keep experiments atomic.** The verified scope for EXP-002 is `LangVersion` in a Release parity run (419 discovered / 418 passed / 0 failed / 1 intentionally skipped, 425 API/metadata entries, XML and local package validation); other property moves and Debug parity are **not verified** by that run. Evaluate `WarningLevel` separately, including normal/exceptional `Configuration|Platform` values, overrides, generated XML/assembly and clean consumer checks. Recheck actual evaluated values with `MSBuild -getProperty` and import locations with `/pp`.

## NuGet and packaging

`NuGet.Config` explicitly defines sources/audit sources. Dependencies are declared in pinned `packages.config` files. CI uses standalone `nuget restore`. Packaging is defined by `packaging/RecordSift.nuspec`, including five `lib/net48` DLLs, XML documentation, README/license/notices and explicit dependencies.

Important resource identities:
- `RecordSift.Resources.CsvMessages.resources`
- `RecordSift.Resources.DomainMessages.resources`
- `RecordSift.Resources.ReportingMessages.resources`

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

- `scripts/run_tests.ps1` locally runs **four** assemblies, omitting Infrastructure.Xlsx.Tests. The CI workflow runs **five**. Always use the five-suite baseline when judging changes.
- Some engineering documentation says **379 tests**; the observed total is **419**.
- `scripts/verify_public_api.ps1` reads `$project.Project.PropertyGroup[0].TargetFrameworkVersion` from raw XML. Moving framework declaration to imported props would require first updating the checker to use evaluated MSBuild properties.
- The Windows PowerShell 5.1 host is significant for API verification: an initial experimental use of PowerShell 7 produced spurious reflection differences.

## Expected compatibility gates

Restore → Release build all ten projects → full five-suite NUnit (419/418/0/1) → 425-entry API/metadata baseline → assembly and embedded-resource identity checks → XML docs → package layout and dependency checks → clean installed-package consumer tests.

Do not interpret changed binary hashes or timestamps as compatibility failure unless deterministic equality is part of an explicit requirement.
