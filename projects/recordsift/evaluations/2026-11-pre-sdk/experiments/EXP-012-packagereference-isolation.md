# EXP-012 — Isolated `packages.config` to `PackageReference` migration without SDK-style conversion

**Assessment date:** November 3, 2026  
**Tracking:** [Issue #13](https://github.com/infoconex/dotnet-modernization/issues/13)  
**Canonical RecordSift baseline:** `8358780829458854a4b0356df5ac5e685f0a34c8` (`main` and `research/dotnet-modernization` remain unchanged).  
**Disposable application branch:** `research/package-reference-exp012-20261103`; it adds **only** `.github/workflows/research-exp012-packagereference.yml`. The seven project-file edits and removals of `packages.config` occur **only in a disposable GitHub Actions workspace** and are never committed to RecordSift.  
**Documentation branch:** `research/recordsift-package-reference-exp012-20261103` on `infoconex/dotnet-modernization`, as a separate draft PR pending review.  
**Previous inventory:** [EXP-011](https://github.com/infoconex/dotnet-modernization/pull/12) exists on unmerged [draft PR #12](https://github.com/infoconex/dotnet-modernization/pull/12); this link is intentionally to the related draft because the canonical docs `main` does not yet contain that file.  
**Overall status:** **Complete: full compatibility verified for all-17-exact-pins candidate; direct-only variant demonstrated actual version drift despite passing builds/tests.** The unchanged legacy 425-entry API gate fails as a documented negative control because it reads removed `packages.config` files; the **414 compiled API/identity entries** and all other compatibility checks pass in an isolated corrective comparison. No conversion approved for application implementation.

## Goal and controlled scope

Assess whether a traditional .NET Framework **4.8**, C# **7.3**, non-SDK solution can move from `packages.config` to `PackageReference` **without first converting project format or changing target runtime**. Preserve the exact known versions and isolate changes to one variable (dependency management format) before experimenting with direct-only dependency simplification or SDK conversion.

This is an **in-workspace manual comparison**, **not** a run of the Visual Studio automated `Migrate packages.config to PackageReference` wizard. It must not be interpreted as proof that the wizard chooses the same references or metadata.

## Frozen input and experiment design

- Five production and five test traditional C# projects, seven `packages.config` files and **17** pinned package entries (13 unique package IDs).
- Current hand-maintained published `RecordSift.nuspec` explicitly lists 11 production package IDs at bracketed **exact** versions. The migration experiment leaves it unchanged.
- Each temporary `PackageReference` mirrors the original `packages.config` ID/version using exact `Version="[x.y.z]"`, rather than a bare minimum version. This deliberately preserves all 17 entries, including candidates that may become transitive later.
- Remove only C# assembly `<Reference>` elements pointing to the legacy `packages/` folder and each `<None Include="packages.config" />`. Preserve all framework references, project references, compiler options, target version, resource identities and output paths.
- Remove the seven `packages.config` files only in the ephemeral checkout. The experiment changes no `.nuspec`, `NuGet.Config`, source C#, tests, public APIs, CI release workflows, version or library source.
- Baseline command: `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config`; normal Visual Studio MSBuild Release rebuild and all five NUnit suites.
- Candidate command: `MSBuild.exe RecordSift.sln /t:Restore /p:RestoreConfigFile=NuGet.Config`, then `/t:Rebuild /p:Configuration=Release /p:Platform="Any CPU"`. Inspect `obj/project.assets.json` for each of the seven package-managed projects.
- The original NUnit scripts use `packages/NUnit.ConsoleRunner.3.17.0/tools/nunit3-console.exe`. With `PackageReference`, NuGet restores to a global cache, not the legacy solution packages location. **The experiment explicitly installs NUnit.ConsoleRunner 3.17.0 into `packages/` solely as test-harness compatibility**, rather than silently treating the original tooling as unchanged.
- For public API checks, run the **unchanged** legacy validator as a control. If it rejects missing raw `packages.config` metadata, compare the compiled API and identity records against a **temporary, in-workspace filtered copy** of the original approved API baseline, excluding only the 11 legacy package declarations. Never weaken or alter the committed production verifier or approved baseline.
- If parity succeeds, subsequently verify production XML docs and intentional CS1591 enforcement, the 419/418/0/1 five-suite baseline, unpublished package and independent clean consumer. Note where a gate was not reached. Any package is **unpublished** research output, not a release candidate.

## Environment

GitHub hosted `windows-2022`, Windows NT `10.0.20348.0`; VS 2022 Enterprise MSBuild; Windows PowerShell 5.1 for API verification, PowerShell 7.6.9 for orchestration, .NET SDK 10.0.403, and NuGet CLI 7.9.0.83. These tools are preinstalled on the hosted runner; no Visual Studio requirement was removed by the PackageReference experiment. The supported target remains .NET Framework 4.8.

**Reproducible procedure:** [experiment workflow on research branch](https://github.com/infoconex/RecordSift/blob/research/package-reference-exp012-20261103/.github/workflows/research-exp012-packagereference.yml). The branch only adds this workflow; the application baseline is the exact immutable SHA above.

## Executed result: initial workflow

**Initial workflow:** [GitHub Actions 41734336487](https://github.com/infoconex/RecordSift/actions/runs/41734336487), workflow SHA `80931140924e60052a5d4584af0985c97d33d83e`, [artifact 13276673751](https://github.com/infoconex/RecordSift/actions/runs/41734336487/artifacts/13276673751).

| Gate | Observed | Interpretation |
|---|---|---|
| Source branch diff | Workflow only | No application changes committed |
| Existing `nuget restore` / Release rebuild | **Passed** | Original input builds |
| Baseline NUnit 5 suites | **419 total / 418 passed / 0 failed / 1 intentionally skipped** | Reproducible behavioral control |
| Seven `packages.config` files replaced in disposable checkout with 17 exact `PackageReference` declarations | **Completed** | No SDK-style conversion performed |
| `MSBuild.exe /t:Restore` | **Passed** | Classic non-SDK .NET Framework projects support PackageReference restore |
| `obj/project.assets.json` | **Seven found** | Confirmed resolver graph generation and preservation of `CsvHelper/33.1.0`, `System.Memory/4.5.5`, `System.Runtime.CompilerServices.Unsafe/6.0.0`, and other packages |
| Migrated Release rebuild | **Passed** | All ten original DLL names present |
| NUnit ConsoleRunner available at legacy path | **Yes, but by explicit separate `nuget install`** | Test tooling needs migration attention |
| Migrated NUnit five-suite check | **419 total / 418 passed / 0 failed / 1 skipped** | Baseline parity with test-harness workaround |
| Positive XML documentation | **Passed** | All five production assemblies, members **179/101/8/2/9** |
| **Unmodified public API/metadata verifier** | **Failed**: 11 `package` lines missing | Script reads `src/*/packages.config`, which is correctly absent after migration. The 11 absent lines are package-management **source metadata**, not automatically a changed compiled C# public API. |
| Local NuGet package / clean consumer / negative CS1591 | **Not reached** | These gates were performed **only in the corrected follow-up**, not the initial run |

The raw verifier `scripts/verify_public_api.ps1` lines 105–110 explicitly load `packages.config` and emit `package <assembly> <id>=<version>`. Lines 194–200 compare all emitted lines with `docs/compatibility/public-api-net48.txt`. The resulting 11 missing entries explain exactly why the original check fails in this migration. **Do not change the approved baseline merely to turn the check green.** A future compatibility gate must understand both metadata formats or separate compiled API signature/assembly identity from package and consumer-dependency policy.

**Key observation:** The new `project.assets.json` files list project-to-project references as `RecordSift.* / 1.0.0` entries as well as NuGet packages. Those synthetic project graph entries are **not** external NuGet dependencies and must not be counted as package conflicts or published dependencies. RecordSift product `.nuspec` remains the independent authority for consumer package dependencies under this experiment.

## Follow-up controls and final outcome

Second workflow [41734675914](https://github.com/infoconex/RecordSift/actions/runs/41734675914) temporarily subtracts **only** the 11 raw `package` records from a copied approved baseline, then runs the unchanged compiled reflection comparator against its remaining entries. This is a diagnostic to distinguish real compiled API drift from known source-format metadata coupling. The untouched full validator is still run and expected to fail on the same 11 records.

**Follow-up result: verified.** [Successful Actions run 41734675914](https://github.com/infoconex/RecordSift/actions/runs/41734675914), workflow SHA `e5dac596a65aeba6a0059e4642d1f29f2c526518`; [artifact 13277228780](https://github.com/infoconex/RecordSift/actions/runs/41734675914/artifacts/13277228780) contains both NUnit XML results, package assets JSON, the experiment's structured outcome, and the temporary compiled-only API baseline. The unchanged full API check still fails intentionally on the 11 deleted raw package declarations. A **second** invocation of the unchanged checker, with a **temporary filtered baseline** preserving all other entries, passed **414 compiled API and identity entries**.

| Compatibility gate | Successful follow-up run |
|---|---|
| Original `nuget restore` + Release build + five-suite NUnit baseline | **PASS**; 419/418/0/1 |
| Seven traditional-project conversions; 17 exact `PackageReference` items | **PASS**, only disposable checkout |
| PackageReference `MSBuild /t:Restore`, seven `obj/project.assets.json` and expected pinned versions | **PASS** |
| Migrated Release build, 10 assembly-name parity check | **PASS** |
| NUnit, with separate explicit NuGet installation of the legacy console runner | **PASS**; 419/418/0/1 |
| Five generated XML documentation files | **PASS**; counts 179/101/8/2/9 |
| Original `verify_public_api.ps1` using committed full baseline | **EXPECTED FAIL**; 11 `packages.config` entries missing |
| Unchanged reflection checker against temporary baseline excluding **only** 11 source-only package lines | **PASS**; 414 compiled API/identity entries |
| Create and validate unpublished internal 0.1.0-rc.1 package with original package script | **PASS**; five net48 DLLs/XMLs, licenses/notices, dependencies |
| Independent NuGet-installed net48 consumer + all four Getting Started CSV/XLSX samples | **PASS** |
| Negative CS1591 compiler-enforcement check | **PASS**, deliberately undocumented public member rejected |

The **unpublished experimental package** has SHA-256 `D9A7C2C08191AABB30B9CD343446CC225A2EA012612D1A26AEDFB5A67E387BAD`. This is not publishable release evidence: the original packaging script labels the package with a workflow commit even though only the workflow is committed and the project-file conversion exists solely within the temporary checkout. **No NuGet publication occurred.**

No production script, application branch, approved 425-entry baseline, `.nuspec`, or release workflow was modified. These results prove parity for the **all-17-exact-pins manual candidate and tested gates**, not for a real Visual Studio automated migrator. A separately executed **direct-only heuristic** experiment, described next, proves NuGet resolves different versions when nine apparent transitive references are removed; it does **not** demonstrate consumer/release compatibility. The original 425-entry verifier remains incompatible with the source-format change and must not be counted as a passed unchanged gate.

## Direct-only dependency hypothesis — completed, **version drift confirmed**

**Definitive run:** [41735278846](https://github.com/infoconex/RecordSift/actions/runs/41735278846), workflow SHA `63eaad20986cdf429fd64f248a5c2a3f9223f857`, [artifact 13278931281](https://github.com/infoconex/RecordSift/actions/runs/41735278846/artifacts/13278931281). This single run repeated **all full-exact-pins baseline and migration gates successfully** before its separate direct-only experiment.

**Controlled transformation:** from the proven 17-exact-reference candidate, remove **nine** production PackageReferences considered *potentially transitive* based on package metadata: keep only `CsvHelper [33.1.0]` in the CSV adapter and `ExcelDataReader [3.9.0]` in the XLSX adapter. Leave five `NUnit [3.14.0]` test references and `NUnit.ConsoleRunner [3.17.0]` (private development tool) unchanged, for **eight explicit package declarations**. This is a **research heuristic**, not confirmed Visual Studio migrator output nor a recommendation to delete nine references.

Perform a fresh MSBuild PackageReference restore and examine actual resolved `project.assets.json`. Compare the CSV graph against the full-pinned candidate; then rebuild and rerun all five NUnit assemblies, XML documentation and the 414-entry compiled API/identity comparison.

| Package | Full exact-pins candidate (verified) | Direct-only candidate (verified) | Implication |
|---|---|---|---|
| `CsvHelper` | **33.1.0** | **33.1.0** | Direct root unchanged |
| `Microsoft.Bcl.AsyncInterfaces` | 8.0.0 | 8.0.0 | No version drift observed |
| `Microsoft.Bcl.HashCode` | 1.1.1 | 1.1.1 | No version drift observed |
| `Microsoft.CSharp` | 4.7.0 | 4.7.0 | No version drift observed |
| **`System.Buffers`** | **4.5.1** | **4.4.0** | **Unapproved downgrade** |
| **`System.Memory`** | **4.5.5** | **4.5.0** | **Unapproved downgrade** |
| **`System.Numerics.Vectors`** | **4.5.0** | **4.4.0** | **Unapproved downgrade** |
| **`System.Runtime.CompilerServices.Unsafe`** | **6.0.0** | **4.5.3** | **Unapproved downgrade** |
| `System.Threading.Tasks.Extensions` | 4.5.4 | 4.5.4 | No version drift observed |
| `ExcelDataReader` / `System.ValueTuple` | 3.9.0 / 4.5.0 | 3.9.0 / 4.5.0 | XLSX dependency versions unchanged |

**Direct-only execution:** restored successfully; all ten traditional projects compiled successfully in Release; NUnit **419 discovered, 418 passed, 0 failed, 1 skipped**; five positive production XML files passed; the **414 compiled API/identity entries** passed with the temporary format-independent baseline. This **does not** establish security, runtime/binding-redirect parity beyond tested cases, stability for other environments, or intended dependency version equivalence. **The local package/clean consumer and negative CS1591 gates were not repeated in direct-only mode**—they passed earlier in this same run for the full-pins candidate, which is a *different dependency graph*.

**Strong conclusion:** A `PackageReference` conversion followed immediately by automatic removal of apparent transitive dependencies **silently changes four version selections** even though builds/tests/API succeed. Do not bundle cleanup with the format conversion. Preserve exact constraints first, then perform independent intentional version-change reviews with explicit approval and complete package/consumer verification.

The unpublished package SHA-256 from the full-pins stage of this definitive run was `147D3B223297101EBD367BB21FEA8E14C00D2B84DB33625134D58A535DE9765E`. It was built **before** the direct-only test and is not a release artifact. The 41734675914 artifact hash differs because the exploratory package metadata includes the workflow commit; **byte-identical package reproducibility was neither expected nor required**.

## Risks and recommendations (evidence-based)

1. **Technically verified** for the controlled all-17-exact-pins candidate across original/migrated builds, NUnit, compiled API/identity subset, XML, unpublished packaging, independent consumers and CS1591. The current unmodified 425-entry gate **still fails** for 11 source-only package records, and the legacy NUnit console path still needs a separately installed tool.
2. **Source-format coupling in the API baseline validator is proven.** If a future PackageReference change is approved, adapt its source-package checking to the evaluated dependency model and keep a separate explicit policy check for the hand-maintained `.nuspec`. Do not weaken compiled API and identity checks.
3. **Legacy NUnit tool path requires a decision.** This experiment can run the same tests with a separately installed runner, but the unchanged `nuget restore` no longer provisions it at the assumed legacy location. Modernize the test runner separately after authorization, and verify all 419 tests.
4. Retaining **17 exact** references establishes dependency-version parity for the deliberate test. **The executed direct-only variant changed four resolved versions (Memory, Unsafe, Buffers, Vectors), even as all five NUnit suites and compiled API checks passed.** This is direct evidence against combining migration with automatic dependency simplification. Evaluate each potential dependency removal separately, including exact version policy and .NET Framework binding redirects.
5. Any future project conversion must test the existing package staging and consumer scripts. Other unmerged documentation branches may overlap the experiment index/status; reconcile at review.
6. **No changes to application main, release/0.2 or released NuGet packages. No implementation authorization.**

## References

- [Microsoft: PackageReference in project files](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files) — traditional .NET Framework project support, minimum versus exact versions, transitive asset selection and global packages.
- [Microsoft: Migrate packages.config to PackageReference](https://learn.microsoft.com/en-us/nuget/consume-packages/migrate-packages-config-to-package-reference) — supported Visual Studio migration reports and special-package behavior.
- [Microsoft: NuGet restore in MSBuild](https://learn.microsoft.com/en-us/nuget/reference/msbuild-targets) — separate restore and build targets.
- [EXP-011 dependency inventory (draft)](https://github.com/infoconex/dotnet-modernization/pull/12) — read-only source and package metadata baseline.

All observations here refer to an **experimental checkout**, not an approved application implementation.