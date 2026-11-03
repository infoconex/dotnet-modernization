# EXP-013 — PackageReference migration tooling and existing Windows CI readiness

**Research date:** November 3, 2026  
**Tracking:** [issue #15](https://github.com/infoconex/dotnet-modernization/issues/15)  
**Application baseline:** frozen `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8` (`main` and `research/dotnet-modernization` unchanged).  
**Disposable application experiment branch:** `research/migration-ci-exp013-20261103`; commits only the isolated `.github/workflows/research-exp013-migration-ci.yml`. Any temporary PackageReference conversions remain in GitHub Actions' checkout and are never committed to the application.  
**Documentation branch:** `research/recordsift-migration-ci-exp013-20261103`, for a separate **draft PR, not merged**.  
**Prior evidence:** [EXP-011 dependency inventory, draft PR #12](https://github.com/infoconex/dotnet-modernization/pull/12) and [EXP-012 manual exact-pins PackageReference migration, draft PR #14](https://github.com/infoconex/dotnet-modernization/pull/14).  
**Status:** **Completed:** CI tooling, original-format baseline controls, and candidate format-aware architecture validator positive/negative controls verified. The actual Visual Studio GUI wizard was **not executed**.

## Research boundaries

This research deliberately separates three questions that should not be conflated:

1. **What migration mechanisms are actually available?** Microsoft documents a **Visual Studio UI** command for supported traditional C# projects. It performs dependency classification, gives the user top-level choices and writes a migration report and backup. Merely running our hand-authored conversion in EXP-012 does **not** exercise or predict that UI's choice of top-level package references.
2. **Does the existing Windows CI work unchanged after format conversion?** The source contains restore commands, package/configuration audits, a pinned Roslyn formatter, NUnit runner-path assumptions, API metadata baselines, consumer scripts, and release protections. Check each separately; do not assume all pass because a Release build and 419 tests passed.
3. **What is a minimal and defensible preparation plan?** Research/document only. No SDK conversion, changes to package versions or application source, workflow replacements, releases, or package publication.

## Migration tooling: supported path versus the experiments

[Microsoft's `packages.config` migration procedure](https://learn.microsoft.com/en-us/nuget/consume-packages/migrate-packages-config-to-package-reference) documents:
- Visual Studio 2017 **15.7+** supports `Migrate packages.config to PackageReference...`, invoked from Solution Explorer's **References** node or `packages.config` context menu. It is **not supported for ASP.NET and C++ project types**; RecordSift is composed of traditional C# class libraries and tests, so those named exclusions do not apply.
- The UI analyzes packages into likely **top-level** and **transitive** sets. The user can choose to elevate packages to top-level. It automatically does so for packages with certain non-transitive assets (`build`, `buildCrossTargeting`, `contentFiles`, `analyzers`) or `developmentDependency=true`.
- The wizard **backs up** project/package files, reports classified dependencies and any detected compatibility issues, and writes its report to the backup location. Its report is an input to review, **not** a guarantee of compatible runtime dependencies or exact version parity.
- Some `install.ps1`, `content`, XDT and `lib`-root behaviors are incompatible with PackageReference; treat the warning/report and actual package contents as authoritative for each migrated application.
- Microsoft documents the migration as a **UI workflow**, not a headless `nuget.exe migrate` action. Our checked-in GitHub Actions experiment runs a manually constructed conversion. **The actual Visual Studio wizard was not executed and no wizard report was produced in this investigation.** Do not invent a comparison or represent the heuristic direct-only EXP-012 experiment as its output.
- [PackageReference documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files) confirms traditional .NET Framework C# project support and the global-packages restore layout; the provided version `Version="4.5.5"` denotes a minimum preference, unlike exact `Version="[4.5.5]"`.

**Relevant RecordSift observation:** EXP-011 found `NUnit.ConsoleRunner 3.17.0` with `developmentDependency=true` and tool files, and `NUnit 3.14.0` with build props. Under Microsoft's documented migrator rules, these warrant careful explicit review rather than automatically treating every installed package as safely transitive. No actual wizard classification of RecordSift has been observed.

### If the GUI wizard is eventually executed under separate approval

In a **disposable copy**, open the frozen solution in a supported Visual Studio IDE; migrate **one project at a time**, retain its backup/migration log, and record which packages it chose as top-level. Compare its XML `PackageReference` items, selected `project.assets.json` versions, assets, imports, assembly references, test-runner behavior, binding redirects and output DLLs with EXP-012's all-exact candidate **before** approving or changing other projects. Preserve the full 419/418/0/1, compiled public API/identity, five XML files, package and clean consumer verification as acceptance gates. This is a *future procedure*, **not an assertion that the wizard was tested**.

## Existing CI dependency inventory (source inspection)

The following table is a **source-only audit** of the frozen application repository, unless a run is explicitly linked. Full end-to-end executions of production workflows after actual migration were **not** authorized and not performed. The experiments run in a separate research workflow and never publish.

| Workflow and step | Existing assumption | Scope / likely action for future approved migration |
|---|---|---|
| `windows-net48.yml` → Restore `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config` | Assumes packages.config style in step name; the NuGet CLI command may also restore PackageReference. | Run unchanged command in disposable exact-pins migrated checkout. Check seven generated `project.assets.json`; distinguish NuGet CLI restore from `MSBuild /t:Restore`, which EXP-012 already proved. |
| `windows-net48.yml` → MSBuild Release | Uses Visual Studio `vswhere`; classic net48 builds | EXP-012 verified VS MSBuild restore/build under PackageReference. Doesn't establish a Visual Studio-independent host. |
| `windows-net48.yml` → positive XML + NFR-010 API | Verifier reads raw `packages.config` for 11 package metadata entries | EXP-012 confirmed original 425-entry gate fails; the **414 compiled API/identity** entries pass when a *temporary copy* of the approved baseline omits only those source-only records. Future CI should deliberately separate source/package policy from compiled API identity rather than silently approving lost metadata. |
| `windows-net48.yml` → tampered API negative control | Uses original verifier and baseline | Keep negative enforcement meaningful after adapting verifier; not independently tested for converted format as a production gate. |
| `windows-net48.yml` → `dotnet format style ... --no-restore ... IDE1006` | Assumes formatter can load traditional solution and NuGet assets | Evaluate identical command in migrated disposable workspace; don't infer parity from EXP-008's unchanged-format test. |
| `windows-net48.yml` → five NUnit suites plus NFR-002/003/filter checks | Runner hardcoded under `packages/NUnit.ConsoleRunner.3.17.0/tools` | `PackageReference` restores to global packages, not necessarily the solution folder. EXP-012 separately installed the same runner as temporary workaround. Office-free/firewall/category checks were **not** rerun after migration; retain as future acceptance evidence. |
| `windows-net48.yml` → dependency-audit job | Reads several specific production/test `packages.config` files, asserts counts/pinned IDs; then runs `nuget restore` and checks NU1900–NU1905 warnings | **Direct source-format break expected** once those files are removed. Experiment both unchanged input failure and a candidate read-only audit of all 17 exact `PackageReference` XML elements. A future gate must preserve dependency and architectural policy, not just pass restore. |
| `windows-net48.yml` → local candidate / negative CS1591 | Uses hand-authored `.nuspec`, compiled Release outputs and Visual Studio MSBuild | EXP-012 passed for full exact-pins candidate. No release publication allowed in research. |
| `verify-rc-consumer.yml` | Same legacy-named restore; builds, packages both RC and stable **locally**, invokes independent net48 consumers | EXP-012 already executed RC package/consumer after manual VS MSBuild restore; no independent full CI workflow re-run after changing restore route. No publication. |
| `adversarial-extended.yml`, `extended-adversarial.yml` | Use `nuget restore`, VS MSBuild and NUnit in the solution `packages/` location or other test-specific assumptions | Existing source coupling suggests runner provisioning changes; adversarial tests not executed for converted candidate. |
| `validate-docs.yml` | Python documentation, architecture, core messages and test metadata checks | No direct `packages.config` reference in workflow. Optional Windows host source probes are not the same as the normal **Ubuntu CI** execution. |
| `prepare-0.1-release.yml`, `publish-release.yml` | Guard main SHA, successful check-run names, owner-approved promotion; use NuGet restore and original packaging scripts | **Do not trigger** during research. Changing required CI checks or workflow path must not weaken exact-source, environment approval or package provenance controls. |
| `recover-recordsift-0.1-release.yml` | One-time published 0.1.0 artifact/release reconciliation | Historical workflow; not a migration target and must not rerun as experimental work. |
| `scripts/run_tests.ps1` | Hardcoded runner location and **omits XLSX test assembly** | Existing defect predates PackageReference, tracked separately. Do not conflate with migration result. |

## Experimental design and evidence boundaries

**Disposable branch:** `research/migration-ci-exp013-20261103` from immutable main baseline; commits **one workflow**. The in-job candidate performs EXP-012's seven-project/17-entry exact-pinned PackageReference conversion and the same original/migrated Release builds, 419 baseline/migrated tests, five XML outputs, 414 compiled API/identity snapshot checks, unpublished local RC package + installed consumer, and negative CS1591. Those are **controls** so the CI-specific probes are evaluated against a known functioning source.

**New probes (must inspect completed logs):**
1. Run the original CI `nuget.exe restore ... -PackagesDirectory packages -ConfigFile NuGet.Config` **unchanged after conversion**, check all seven asset files.
2. Prove the original audit's `Get-Content tests/RecordSift.Domain.Tests/packages.config` fails once the file is removed, and validate the same **17 exact-pinned PackageReference** identities/versions in the seven .csproj files via an alternative **experimental, uncommitted** XML check.
3. Run the exact `dotnet format style RecordSift.sln --no-restore --verify-no-changes --diagnostics IDE1006 --severity error --verbosity normal` command and record exit code and log. Do not suppress a failure.
4. Run six existing docs/architecture validation scripts on the **Windows** runner as additional probes if Python exists; report each exit code and the host limitation.
5. Observe the `nuget help` command listing for a `migrate` subcommand; absence is *narrow evidence*, not proof no other private/unrelated tool exists.

**Evidence:** workflow source SHA, GitHub run and artifact IDs, OS/MSBuild/SDK/NuGet/PowerShell, JSON status matrix, NUnit XMLs and formatter output. The migration experiment does **not** run the actual GUI wizard and is not equivalent to executing every production workflow end-to-end.

## Verified Windows CI execution and negative controls

**Execution [41736927515](https://github.com/infoconex/RecordSift/actions/runs/41736927515):** [artifact 13279955880](https://github.com/infoconex/RecordSift/actions/runs/41736927515/artifacts/13279955880), workflow SHA `79eaa43b6cc6dc83bf093f247cc2e3d19d8eaa99`. **Result: completed successfully**, including full exact-pins migration/consumer gates, restored assets, original CLI restore, 17/17 experimental package audit, unchanged formatter, six docs scripts (four passed, two failed in the *post-build Windows probe*). The overall workflow was green because those two probes intentionally record individual negative results.

**Confirmatory execution [41737351278](https://github.com/infoconex/RecordSift/actions/runs/41737351278):** [artifact 13278713864](https://github.com/infoconex/RecordSift/actions/runs/41737351278/artifacts/13278713864), workflow SHA `e06968f12c5da80b3445769595e90eed2207157e`. **Result: completed successfully** with additional unchanged-format *pre-migration* source validation, formatter diagnostic verbosity and `obj/` cleanup controls.

**Tool inventory:** Windows NT `10.0.20348.0`, GitHub `windows-2022`, .NET SDK `10.0.403`, NuGet CLI `7.9.0.83`, PowerShell `7.6.9`, Visual Studio 2022 Enterprise MSBuild `17.14.60.43110`. `nuget help` did not list a `migrate` command; **no Visual Studio GUI wizard was executed**. All exact-pins `PackageReference` edits were ephemeral.

| CI question | Verified observation | Interpretation |
|---|---|---|
| Original pre-migration baseline | `nuget restore`, Release build, 419/418/0/1 NUnit **passed** | Original RecordSift contract reproduced |
| Exact-17 `PackageReference` migration | MSBuild restore, ten Release projects, 419/418/0/1 NUnit, five XML docs **passed** | Source-format migration is feasible in traditional net48 |
| Compiled API/identity | **414 entries passed**, after filtering 11 *source-only* `packages.config` records into a temporary reference copy | **Unchanged 425-entry full verifier fails**; do not classify it as green |
| Local unpublished NuGet RC + independent installed consumer / Getting Started samples | **Passed** | Consumer compatibility verified only for all-17-exact-pins candidate |
| Negative CS1591 docs | **Passed** | Existing compiler enforcement still works |
| **Original CI `nuget.exe restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config`** after PackageReference conversion | **Passed**, with all **seven `project.assets.json`** present | Existing restore CLI **does not need replacement** solely because package-management format changed |
| Original dependency audit reading `tests/RecordSift.Domain.Tests/packages.config` | **Expected fail:** absent file, exactly as source predicts | Existing CI inventory validation **must** be adapted; do not delete the policy |
| Experimental format-aware pin audit (XML `PackageReference`) | **17/17 exact entries across seven projects passed** | A replacement can preserve pin enforcement without relying on deleted file paths; candidate not committed |
| Identical `dotnet format style RecordSift.sln --no-restore --verify-no-changes --diagnostics IDE1006 --severity error --verbosity normal` | **Exit 0** | Current naming/style check is compatible in tested Windows host |
| Formatter diagnostic repeat with `--verbosity diagnostic` | **Exit 0**, no lines containing warning/fail/unable/exception | Normal command printed a generic workspace warning; diagnostic run did not identify actionable migration warnings. Don't claim all possible warnings eliminated. |
| `validate_docs.py`, `verify_getting_started_samples.py`, `validate_test_metadata.py`, `validate_constant_names.py` | All **exit 0** in Windows post-build probe | No change required based on this limited execution |
| `validate_architecture_layers.py` | **Exit 1** after original `packages.config` build, **exit 1** after converted build and again **exit 1 after removing all 10 transient `obj/` directories** | Two distinct issues: pre-existing generated `obj/**/*.cs` scanning; **real migration incompatibility** because script still demands a raw `ExcelDataReader` `Reference` element |
| `validate_core_messages.py` | **Exit 1** after original build and after migrated build; **exit 0 after deleting generated `obj/` directories** | Pre-existing post-build order issue, **not** caused by PackageReference |
| GUI migrator classification/backup/compatibility report | **Not executed; no report** | Can't claim wizard direct/transitive choices or parity |

**Specific architecture guard:** frozen `scripts/validate_architecture_layers.py` lines **323–324** demand a `<Reference Include="ExcelDataReader">` item. The converted XLSX project correctly has a `<PackageReference Include="ExcelDataReader" Version="[3.9.0]">` instead. That guard must recognize the new dependency representation **without weakening the rule** that only the XLSX infrastructure adapter owns the vendor parser dependency. The current frozen source verifier's `rglob("*.cs")` also includes generated assembly-attribute files under `obj` when run after a build; this affects the original `packages.config` baseline too. The separate, clean Ubuntu docs workflow was **not** invoked against a migrated branch: post-build Windows probes are not evidence of its results.

**Final architecture control: VERIFIED.** [GitHub Actions run 41737816926](https://github.com/infoconex/RecordSift/actions/runs/41737816926), immutable workflow SHA `933c74ec916468ce1e4a5c0c0878ca56a360bc36`, [artifact **13279522277**](https://github.com/infoconex/RecordSift/actions/runs/41737816926/artifacts/13279522277), completed **successfully**. After the usual exact-pins migration, full compatibility, original-restore/formatter/audit and `obj` cleanup controls, the research workflow **temporarily edited only the in-workspace copy** of `scripts/validate_architecture_layers.py` to accept `ExcelDataReader` from either XML `Reference` **or** `PackageReference` items. The candidate **passed** on the migrated project (**exit 0**). As a negative control, it temporarily removed `<PackageReference Include="ExcelDataReader" ...>` from the migrated XLSX project and reran the candidate validator, which correctly **rejected** the missing dependency (**exit 1**, explicit XLSX vendor dependency error). The experiment restored the original source validator and project file in `finally`; no application changes were committed. **The protection is preserved**, rather than bypassed. Results are not implementation authorization.

**Non-migration caveat:** The existing `scripts/run_tests.ps1` still omits the XLSX assembly; experiment uses all five DLLs explicitly and confirms 419/418/0/1. Do not claim that unmodified script establishes full suite parity.

### Experiment-harness history

- Initial branch-only workflow `ec9ae3fe4a0bed5a83606307661709e994692eb4` was not triggered because its push filter contained the wrong branch.
- [41736825889](https://github.com/infoconex/RecordSift/actions/runs/41736825889) stopped immediately because the workflow's source-integrity check contained the wrong workflow filename; this was a **harness error**.
- [41736927515](https://github.com/infoconex/RecordSift/actions/runs/41736927515) verified the core CI compatibility and revealed the architecture/core-resource Python gate behavior.
- [41737351278](https://github.com/infoconex/RecordSift/actions/runs/41737351278) established original-format baseline failures, isolated `obj`-generated-file noise and confirmed the persistent XLSX dependency declaration mismatch.
- **[41737816926](https://github.com/infoconex/RecordSift/actions/runs/41737816926)**, workflow SHA `933c74ec916468ce1e4a5c0c0878ca56a360bc36`, artifact **13279522277**, verified both the temporary format-aware architecture validator and its ability to reject removal of `ExcelDataReader`. Also repeated original NuGet restore, 17/17 exact-pins audit, 419-suite baseline, local package/clean consumer, CS1591 and IDE1006 parity.

**Research interpretation:** A green top-level experimental workflow is not evidence that every included negative probe passed. Preserve individual exit statuses and compare the original and migrated project formats. Do not conflate the production Ubuntu docs workflow's clean-checkout operation with these explicitly **Windows post-build** probes.

## Recommendation framework (not implementation approval)

- Favor a **small shared, format-aware restore/verification script** only if its savings across multiple CI workflows justify abstraction; otherwise change the few affected commands explicitly and keep CI readable.
- Preserve explicit package-version auditing and architecture/dependency restrictions after transitioning from raw `packages.config`; verify the **resolved** graph as a separate control. The EXP-012 direct-only experiment proved four **unapproved dependency downgrades** despite passing all 419 tests.
- Repair the 425-entry API gate to check **414 compiled/identity** entries and **11 source-format-independent package dependencies** as two distinct checks, or design an equally strong unified format-aware verifier. Do not simply delete 11 lines to claim an unchanged gate passed.
- Keep the existing 0.1 publication and provenance workflow intact during research. Any rollout of workflow and checker changes requires standalone approval, an exact baseline and comprehensive Windows CI/consumer evidence.
- Do not invent an automated Visual Studio migration-tool result. If GUI wizard parity genuinely matters, perform a separately approved Visual Studio IDE experiment and retain its classification/compatibility report.

**No application implementation, branch merges, release or NuGet publishing is authorized.** Any documentation pull request remains a draft until stakeholder review.
