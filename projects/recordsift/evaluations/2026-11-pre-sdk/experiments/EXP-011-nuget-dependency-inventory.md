# EXP-011 — Legacy NuGet dependency inventory and PackageReference readiness

**Assessment:** November 3, 2026  
**Tracking:** [Issue #11](https://github.com/infoconex/dotnet-modernization/issues/11)  
**RecordSift frozen baseline:** `8358780829458854a4b0356df5ac5e685f0a34c8` (`main` and `research/dotnet-modernization` unchanged).  
**Research-only RecordSift branch:** `research/nuget-graph-20261103`, adding **only** an isolated GitHub Actions workflow, `.github/workflows/research-exp011-nuget-graph.yml`. No committed `.csproj`, package, `packages.config`, `.nuspec`, `NuGet.Config`, or product script changes.  
**Successful definitive execution:** [GitHub Actions 41728933974](https://github.com/infoconex/RecordSift/actions/runs/41728933974), workflow commit `a94381f97843d692265e805aeb899e616c60a7bb`, [artifact 13274828527](https://github.com/infoconex/RecordSift/actions/runs/41728933974/artifacts/13274828527). Earlier [41728599985](https://github.com/infoconex/RecordSift/actions/runs/41728599985), artifact 13275169273, verified the full inventory except the stricter final HintPath-file check.  
**Outcome:** **Verified** pinned source and clean restore/package metadata consistency. **Not verified:** automatic top-level/transitive classification for PackageReference, an actual migration, changed consumer package behavior, or post-migration tests. Follow-up run adds strict validation of resolved HintPaths; see below.

## Objective and hypothesis

The established RecordSift baseline uses `packages.config` (not `PackageReference`) in classic non-SDK .NET Framework 4.8 projects and a hand-maintained `packaging/RecordSift.nuspec`. Determine **what the current package graph is**, whether declared versions, restored packages and the public NuGet dependency list agree, and identify concrete migration hazards without prematurely converting packages, changing tools, or upgrading dependencies.

A `packages.config` entry describes a *package installed in that project*, not necessarily a historically **top-level** dependency; this format flattens direct and transitive package dependencies. NuGet's Visual Studio migrator attempts to identify primary packages, but those classifications and post-migration restore/build behavior are **not proved by this inventory**.

## Methods and environment

1. Inspect every `src/**/packages.config`, `tests/**/packages.config`, all ten original `.csproj` source files, `packaging/RecordSift.nuspec`, `NuGet.Config`, and existing Windows dependency-audit CI.
2. In isolated Windows Actions, verify the experiment branch changes **only** the workflow relative to the exact frozen baseline SHA. Do **not** edit project files.
3. Execute the existing command in solution root: `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config -Verbosity normal`.
4. Reconcile 17 `packages.config` elements, all 13 restored `packages/<ID>.<version>/` directories, 11 production `.nuspec` exact dependency declarations, and explicit project assembly `HintPath` references.
5. Open each restored `*.nupkg` **read-only** and inspect its embedded `.nuspec` XML for dependency groups by target framework; enumerate `lib`, `build`, `buildTransitive`, `content`, `contentFiles` and `tools` assets in the extracted packages.
6. Preserve a machine-readable JSON snapshot and full NuGet restore log as an uploaded Actions artifact; record the material findings in this durable Markdown file.

| Property | Observed Windows runner |
|---|---|
| OS | GitHub `windows-2022`, Windows NT `10.0.20348.0` |
| .NET SDK | `10.0.403` |
| Visual Studio MSBuild | VS 2022 Enterprise `MSBuild.exe`, `17.14.60.43110` |
| NuGet executable | `nuget.exe` `7.9.0.83`; preinstalled on hosted Windows runner |
| PowerShell | `pwsh` `7.6.9` |
| Package source | Existing `NuGet.Config` clears package sources and specifies `https://api.nuget.org/v3/index.json`; separate NuGet audit source uses nuget.org |
| Access/secrets | Public NuGet source; no added secrets or publication credentials |
| Product source edits | **None**; a clean restore downloaded packages to the workflow's disposable workspace |

**Exact executed workflow and script:** [research workflow at definitive immutable SHA](https://github.com/infoconex/RecordSift/blob/a94381f97843d692265e805aeb899e616c60a7bb/.github/workflows/research-exp011-nuget-graph.yml). The uploaded JSON records each declared package, all dependency groups (including non-net48 groups, which must **not** be mistaken for selected net48 dependencies), enumerated assets, HintPaths and tool versions.

## Verified baseline — projects and version declarations

| Area | Project(s) | Pinned `packages.config` entries |
|---|---|---|
| Domain, Application, Reporting (production) | `RecordSift.Domain`, `RecordSift.Application`, `RecordSift.Infrastructure.Reporting` | **No `packages.config`**; framework/project references only |
| CSV adapter | `RecordSift.Infrastructure.Csv` | `CsvHelper 33.1.0`; `Microsoft.Bcl.AsyncInterfaces 8.0.0`; `Microsoft.Bcl.HashCode 1.1.1`; `Microsoft.CSharp 4.7.0`; `System.Memory 4.5.5`; `System.Buffers 4.5.1`; `System.Numerics.Vectors 4.5.0`; `System.Runtime.CompilerServices.Unsafe 6.0.0`; `System.Threading.Tasks.Extensions 4.5.4` (**9**) |
| XLSX adapter | `RecordSift.Infrastructure.Xlsx` | `ExcelDataReader 3.9.0`; `System.ValueTuple 4.5.0` (**2**) |
| All five test projects | `RecordSift.*.Tests` | `NUnit 3.14.0` (**5** entries) |
| Test runner tooling | `RecordSift.Domain.Tests` only | `NUnit.ConsoleRunner 3.17.0` with `developmentDependency=true` (**1**) |

**Exact observed cardinalities:** 10 `.csproj` projects; **7** package config files; **17** declarations across those files; **13** distinct package IDs; **13** restored package directories; **11** production package IDs and exactly **11** hand-maintained `RecordSift.nuspec` dependency entries. Each production `.nuspec` entry is an **exact** bracketed version `[x.y.z]` matching its corresponding `packages.config` version, with no duplicate production IDs. Source declarations showed **zero multiple-version conflicts per package ID**. The NuGet restore was successful and logged no `NU1900`–`NU1905` warnings **in that run**, not a security guarantee for future dates.

There are **13** explicit assembly `HintPath` references across the projects: 7 CSV DLLs, 1 XLSX DLL, and 5 `nunit.framework` DLLs. **Definitive run 41728933974 validated all 13 against real existing restored assembly files**, not just directory names. The other package entries do not each imply a direct C# assembly reference; for example, the NUnit console runner is an executable used by scripts. The XLSX project's source has doubled path separators in its HintPath text; the final harness handled those correctly and verified its DLL exists.

## Metadata-derived dependency relationships (framework-sensitive)

All edges below were read from the **downloaded package's embedded `.nuspec`**. These are dependency declarations for matching/relevant .NET Framework groups, **not** a demonstrated post-migration NuGet graph or an assertion about historical install intent.

| Package / applicable nuspec group | Declared dependency edges | Relevance |
|---|---|---|
| `CsvHelper 33.1.0`, `.NETFramework4.8` | `Microsoft.Bcl.AsyncInterfaces >=8.0.0`; `Microsoft.Bcl.HashCode >=1.1.1`; `Microsoft.CSharp >=4.7.0`; `System.Memory >=4.5.0` | Explains why several CSV listed packages are potential transitive candidates; the **actual pinned System.Memory is 4.5.5**. |
| `ExcelDataReader 3.9.0`, `.NETFramework4.6.2` fallback | `System.ValueTuple >=4.5.0` | XLSX's second package has an upstream dependency explanation, but must verify selection under a real new restore. |
| `Microsoft.Bcl.AsyncInterfaces 8.0.0`, `.NETFramework4.6.2` fallback | `System.Threading.Tasks.Extensions >=4.5.4` | Runtime support chain. |
| `System.Memory 4.5.5`, `.NETFramework4.6.1` fallback | `System.Buffers >=4.5.1`; `System.Numerics.Vectors >=4.5.0`; `System.Runtime.CompilerServices.Unsafe >=4.5.3` | **Actual Unsafe is pinned 6.0.0**, considerably newer than the package-declared lower bound. |
| `System.Threading.Tasks.Extensions 4.5.4`, `.NETFramework4.6.1` fallback | `System.Runtime.CompilerServices.Unsafe >=4.5.3` | Another edge to Unsafe. |

**Important:** The string `4.5.0` in an upstream package's dependency metadata means a *minimum*, not an exact lock; the existing `packages.config` file independently pins `System.Memory 4.5.5`. Similarly `System.Runtime.CompilerServices.Unsafe 6.0.0` is already pinned despite `>=4.5.3` upstream requirements. A `PackageReference` migration that drops explicit entries would allow the transitive resolver to choose a different closure. It might pick the same versions, but the current evidence **does not prove that**. Distinguish exact `[4.5.5]` constraints from unbracketed minimum `4.5.5` when specifying `PackageReference`; decide separately whether a lockfile is beneficial for an application or its consumers.

The full artifact includes metadata for other target frameworks (e.g., .NET Standard, Mono, Windows, .NET Core). Those are retained to audit but are **not** all applied to `net48` and should never be combined into a hypothetical net48 graph.

## Asset- and build-system-specific considerations

| Restored package | Actual evidence | Migration interpretation |
|---|---|---|
| `NUnit 3.14.0` | Contains `build/NUnit.props`; all five test projects explicitly declare NUnit, and each has a direct `nunit.framework` HintPath | Retain NUnit as an explicit test dependency; separately verify whether the build props are imported or matter during any future conversion. Mere presence does not prove execution. |
| `NUnit.ConsoleRunner 3.17.0` | Tool-only package, no `lib` assemblies; **71** enumerated tool files, `developmentDependency=true`; existing CI invokes `packages/NUnit.ConsoleRunner.3.17.0/tools/nunit3-console.exe` | **Avoid silently removing or reclassifying as transitive.** Test execution is coupled to the legacy solution `packages/` path; redesign/test tooling separately only with approval and full 419-case verification. Do not include the runner in published library dependencies. |
| `Microsoft.Bcl.AsyncInterfaces 8.0.0` | `buildTransitive/net461/Microsoft.Bcl.AsyncInterfaces.targets` and `buildTransitive/net462/_._` | Restore contains transitive build assets; applicability and behavior under `PackageReference` must be tested, not inferred from file names. |
| `System.Runtime.CompilerServices.Unsafe 6.0.0` | `buildTransitive/netcoreapp2.0/*.targets` and a `netcoreapp3.1` marker | Assets exist but these are **not automatically applicable to net48**; don't claim a net48 build effect. |
| Other production packages in this inventory | No `build`, `buildTransitive`, `tools`, `content`, or `contentFiles` files detected in restored extracted folders | This is a file-inventory observation; installation scripts, binding redirects, package-selection behavior, and a future migration remain unverified. |

**Source coupling:** The five production projects are packaged through a hand-authored `.nuspec` and scripts that explicitly stage five assemblies and XML files. The eleven `.nuspec` dependency declarations form a **public consumer contract**. Do not assume changing the developer project's package-management format may also silently rewrite that contract, packaging layout, required runtime DLLs or clean consumer behavior.

## Disposition: do not migrate now

**Verified as a baseline:** repository package declarations, 11 exact production .nuspec dependencies, restored package metadata, successful original NuGet restore, the observed 13 assembly HintPaths and presence of tool/build assets. This fulfills the inventory-first part of [risk R-008](../risks.md) without implementing it.

**Still unverified:** which packages should become top-level after an actual migration, NuGet resolver-selected graph, exact DLL copy-local and binding-redirect effects, project asset and analyzer/build import changes, package contract and installed consumer parity, and post-conversion tooling. `NUnit.ConsoleRunner` and the `packages/`-based scripts deserve special attention. Historical source/metadata inspection cannot establish an actual successful PackageReference or SDK-style migration.

**Recommendation:**
1. **Retain current `packages.config`, `NuGet.Config`, project HintPaths and `.nuspec` for this pre-SDK research phase.** No new `Directory.Packages.props` or `packages.lock.json` is warranted solely to satisfy this inventory exercise.
2. For a separately approved conversion assessment, capture a **fresh immutable baseline**, try the supported Visual Studio `packages.config` migrator in an isolated branch, save its top-level/transitive and compatibility reports, and compare `net48` resolved assets and packages across all project layers. Favor isolating **package-management format conversion from SDK-style conversion**, so any behavior change has one likely cause.
3. Preserve the intentional `System.Memory 4.5.5` and `Unsafe 6.0.0` selections until equivalent effective versions are demonstrated; use explicit version bounds or a suitable lock approach **where justified**, and avoid treating plain `PackageReference Version="4.5.5"` as exact.
4. Validate production-only package dependencies, test runner location, complete 419-suite NUnit baseline, 425 API metadata entries, five XML docs, binding redirects, output assembly closure, package contents and independent clean consumer. Changes would require **new explicit implementation authorization**.
5. Add central package management **only when** actual `PackageReference` use and shared version-management needs justify it. NuGet Central Package Management can be used with non-SDK `PackageReference` projects; it does **not** centrally manage legacy `packages.config` files.

References (current primary documentation, consulted during assessment):
- [NuGet packages.config reference](https://learn.microsoft.com/en-us/nuget/reference/packages-config) — exact installed versions, developmentDependency.
- [NuGet package dependency resolution](https://learn.microsoft.com/en-us/nuget/concepts/dependency-resolution) — distinct graph-resolution semantics.
- [Microsoft's packages.config migration procedure](https://learn.microsoft.com/en-us/nuget/consume-packages/migrate-packages-config-to-package-reference) — migrator analysis and assets requiring explicit dependencies.
- [PackageReference semantics and lockfiles](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files).
- [NuGet exact vs minimum version notation](https://learn.microsoft.com/en-us/nuget/concepts/package-versioning) — `[x]` exact versus `x` minimum.
- [Central Package Management](https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management) — applies to `PackageReference` projects including traditional project files.

## Experiment harness history and caveats

- [41727583881](https://github.com/infoconex/RecordSift/actions/runs/41727583881) — **harness defect:** PowerShell strict mode rejected an optional `developmentDependency` attribute not present on most `packages.config` elements.
- [41727738688](https://github.com/infoconex/RecordSift/actions/runs/41727738688) — restored all 13 packages and matched 17 entries/11 manifest dependencies, then **harness assumption:** `.nuspec` metadata is inside `.nupkg` and is not extracted as a sidecar file.
- [41727961185](https://github.com/infoconex/RecordSift/actions/runs/41727961185) and [41728086856](https://github.com/infoconex/RecordSift/actions/runs/41728086856) — **invalid YAML harness edits** after a string-substitution mistake and unintended duplicated tail; no product checks/jobs were performed.
- [41728191457](https://github.com/infoconex/RecordSift/actions/runs/41728191457) — after valid clean restore/package inspection, PowerShell strict mode rejected an empty XML `Reference` property on a project group with no references. Switched to explicit XML selection.
- [41728365433](https://github.com/infoconex/RecordSift/actions/runs/41728365433) — after successful restore/package inspection, PowerShell reserved automatic `$PID` variable name collided with a harness local; renamed it.
- **[41728599985](https://github.com/infoconex/RecordSift/actions/runs/41728599985)** — complete initial read-only inventory succeeded; [artifact 13275169273](https://github.com/infoconex/RecordSift/actions/runs/41728599985/artifacts/13275169273) contains JSON and restore log. No application failure was demonstrated.
- **[41728933974](https://github.com/infoconex/RecordSift/actions/runs/41728933974)**, workflow `a94381f97843d692265e805aeb899e616c60a7bb`, [artifact 13274828527](https://github.com/infoconex/RecordSift/actions/runs/41728933974/artifacts/13274828527) — **final green run**. Verified all original inventory checks **and all 13 actual HintPath assembly files**, including the XLSX path with doubled separators. Artifact JSON `resolvedFilePresent=true` for all 13; working source checkout remained unchanged. The present study is complete.

**Not rerun in this read-only inventory:** C# compile, NUnit, public API, XML-documentation validation, NuGet packing or clean consumer. Those have separate established baseline evidence in [EXP-001](EXP-001-baseline.md), [EXP-009 draft](https://github.com/infoconex/dotnet-modernization/pull/8) and [EXP-010 draft](https://github.com/infoconex/dotnet-modernization/pull/10). Cite them without pretending those gates ran during EXP-011.

**No implementation or merge approval:** all documentation is a draft until stakeholder review, and existing documentation PRs #4–#10 remain independent/unmerged. Keep findings independent of their pending file changes and reconcile at the eventual review.
