# <Application> — Verified application baseline

**Repository:** <owner/repo, browser URL> · **Baseline commit:** <full SHA>  
**Inventory date:** <YYYY-MM-DD> · **Verification date:** <YYYY-MM-DD or not executed>  
**Evidence state:** <source inspection status; executed compatibility status>

This is the **unchanged starting state**, not an experiment report or modernization proposal. Record each fact **once** under the six sections below, cite its pinned source or executed evidence, and explicitly note unknowns. For a small application, use a short equivalent section in the [evaluation overview](evaluation-overview.md) rather than copying this file. The [evaluation process](../methodology/evaluation-process.md#2-establish-the-baseline) describes how to collect and verify the information; don't repeat its instructions here.

## 1. Application overview

One short paragraph describing the application, its purpose, workload type (library/API/web/desktop/service/CLI), consumers, supported OS/runtime and relevant constraints.

| Attribute | Value / source |
|---|---|
| Repository provider/type, visibility, owner and name | <Git host, app repository/monorepo, owner/repo> |
| Browser URL; HTTPS and SSH clone URLs | <URLs> |
| Default branch and immutable baseline SHA | <branch and full commit SHA> |
| Application identity, ownership and license | <name, repository metadata/README/license> |
| Supported framework(s), runtime/OS/architecture | <target(s) and confirmed support scope> |
| Published release/package version(s) | <version and release/feed source; observed date> |
| Source package, assembly, file and product versions | <distinct values and manifests/assembly metadata> |

**Note only consequential discrepancies** (e.g., NuGet's published version differs from the checked-in `.nuspec`). Do not conflate solution format, declared Visual Studio version, MSBuild/SDK, target framework, C# version, assembly version and package version.

## 2. Repository inventory

| Directory | Purpose |
|---|---|
| <src/tests/docs/scripts/config/packaging/CI/deployment path> | <one-line description> |

Document the **existing** modernization/configuration mechanisms here—present or absent from the pinned tree. Keep the table to applicable mechanisms, including shared MSBuild `Directory.Build.*` and `Directory.Solution.*`, `global.json`, `.editorconfig`, `NuGet.Config`, `packages.config`, `Directory.Packages.props`, `packages.lock.json`, relevant analyzer/Git files, application settings and CI/AI instruction files. Do **not** list every imaginable absent file if it has no bearing on the evaluation.

| File or mechanism | Present / absent | Location and **current** purpose |
|---|---|---|
| <name> | <state> | <pinned source path, setting(s)> |

Absence is an observation, not a recommendation. Machine-wide, generated or imported settings must be distinguished from tracked files.

## 3. Solution and projects

| Solution | Format / declared version(s) | Configurations and platforms | Included projects / build mappings |
|---|---|---|---|
| <.sln/.slnx path, or none> | <actual format-specific metadata> | <Debug/Release/Custom; Any CPU/x64/etc.> | <counts, ActiveCfg/Build inclusion and exceptions> |

Include all relevant solutions, project paths and standalone projects **outside** solutions; note filters/folders/explicit dependencies when present. Never assume `.slnx` uses the same version/GUID serialization as `.sln`.

Use one project row per project (or link to a complete pinned inventory for a very large repository); state common values **once above the table**.

| Project/path | Kind, format and output | Framework(s), language, configuration | Direct project references | Notable differences |
|---|---|---|---|---|
| <project> | <SDK/traditional, Library/Exe/Web/Test> | <TFMs/C#, Debug/Release/platform> | <direct references> | <GUID/identity/version/resources/extra imports> |

Summarize configuration differences **once** in a compact property table if relevant to the evaluation: `LangVersion`, compiler warnings, define constants, optimize/debug, output paths, `IsTestProject`, `DocumentationFile`, signing, source globs, resources/assembly identity and imported props/targets. Distinguish **declared** values from MSBuild **evaluated** values; document the tool used only if an evaluation actually ran.

## 4. Dependencies and build

| Topic | Baseline | Source or execution evidence |
|---|---|---|
| Project, direct NuGet and resolved package graph | <counts/versions/sources, links to detail> | <csproj/packages.config/restore> |
| Framework, external assemblies, generators and build prerequisites | <required tools/SDKs/targeting packs/interop> | <project/host inventory> |
| Actual build environment and tools | <OS, MSBuild, SDK, NuGet, test runner, versions/paths/provenance> | <executed workflow/run> |
| Restore/build/test/pack commands | <commands and relevant configurations> | <scripts/CI> |
| CI/CD, packaging, deployment/consumer entry points | <workflow paths and artifacts> | <workflow definitions and executed evidence> |

Include significant environment/host dependencies, release contracts, resource inputs and nondefault build steps **once** here. Package declarations, effective restored versions and compiled assembly references are separate; don't infer one from another. Don't include secrets.

## 5. Verification results

| Gate | Result and meaningful counts/contract | Executed evidence |
|---|---|---|
| Restore and complete build | <configuration; pass/fail/not run> | <CI run, commit, command> |
| Automated tests | <discovered/passed/failed/skipped per suite or link> | <test output/run> |
| Public API, assembly/resource/XML contracts | <baseline count/identity> | <snapshot/run> |
| Package layout, dependency closure and clean consumer | <status/version/format> | <package/consumer run> |
| Relevant platform/integration/other checks | <result or N/A/not executed> | <run/limits> |

A green workflow is not proof that every gate ran. Reuse valid existing evidence for the **same pinned source**; do not repeat tests merely to populate a document. Test counts do not establish code coverage or absence of defects.

## 6. Known issues and verification gaps

| Issue, discrepancy or unverified assumption | Impact on baseline comparability |
|---|---|
| <specific observation and source> | <why it matters, link to existing investigation if any> |

**Comparison contract:** <the gates that subsequent experiments must preserve>  
**Baseline status:** <accepted verified reference / accepted with named gaps / more evidence needed>

Keep this section factual. Record modernization hypotheses, implementation recommendations, risks and decisions in the **evaluation's** [findings/experiments/roadmap](evaluation-overview.md), rather than expanding the baseline into a second investigation report.
