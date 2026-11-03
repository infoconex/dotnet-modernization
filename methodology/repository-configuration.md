# Repository configuration and tooling modernization

Use this assessment during discovery to decide whether **existing or potential repository-wide .NET configuration** would make an application easier to build, test, maintain or secure. The goal is to **consider** relevant mechanisms, not to introduce every possible file.

This is a reusable assessment aid, **not** proof that a mechanism applies to a particular codebase. Tool versions, project styles, import chains, package-management formats and test runners can change what a file actually does. Record observed behavior in the application's dated evaluation.

## Configuration mechanisms to consider

The inventory is deliberately practical, not an exhaustive catalog of every .NET configuration format.

| Mechanism | Responsibility | Applicability and key evaluation question |
|---|---|---|
| `global.json` | Select the SDK used by the `dotnet` CLI, including roll-forward policy; can also declare MSBuild SDK versions. | Does SDK selection improve repeatability across developer machines and CI? It does **not** change a project's target framework or by itself pin Visual Studio's MSBuild. |
| `.editorconfig` | File-scoped whitespace, C#/.NET code-style preferences and supported analyzer severities. | Are rules consistent and actually enforced by the relevant IDE, compiler/analyzer and format commands? Check editor-vs-build behavior. |
| `.globalconfig` | Global Roslyn analyzer configuration not organized by file globs. | Is project-wide analyzer configuration necessary, and how is it included by the evaluated project/tooling? Do not assume it is needed alongside `.editorconfig`. |
| `Directory.Build.props` | Shared MSBuild properties evaluated at the point of import. | Which values are genuinely identical across projects? Inspect the **actual** import chain and project-specific override precedence, especially for traditional projects. |
| `Directory.Build.targets` | Shared MSBuild targets and settings imported later in the standard build path. | Is there a demonstrated reusable build behavior? Evaluate import timing; do not add synthetic targets merely for centralization. |
| `Directory.Packages.props` | NuGet Central Package Management (CPM) versions for `PackageReference` projects. | Are projects using `PackageReference` and compatible NuGet tooling? It does not centrally version existing `packages.config` entries. |
| `NuGet.Config` / `nuget.config` | Package sources, restore policy, source mapping and related settings. | Are restores deterministic and secure across hosts, with approved sources and without committed credentials? Account for config layering and command-line overrides. |
| `packages.lock.json` | Lock the resolved dependency graph for supported `PackageReference` restores. | Would locked restore and transitive-dependency visibility help? Check how lock files are generated, maintained and enforced in CI. |
| `.config/dotnet-tools.json` | Manifest for repository-local .NET CLI tools. | Are formatter, generator or validation tool versions currently implicit? Can contributors restore and invoke exactly the supported tools? |
| `Directory.Build.rsp` | Default arguments for supported command-line MSBuild invocations. | Is there a real, reproducible CLI-only need? Response files are not applied to builds inside the Visual Studio IDE; check invocation behavior. |
| `Directory.Solution.props` | Properties for the separate MSBuild **solution build**. | Is solution-wide orchestration necessary? These settings do **not** automatically become project-level properties and are not applied to solution builds inside Visual Studio. |
| `Directory.Solution.targets` | Targets for the separate MSBuild **solution build**. | Is there a concrete solution-build requirement? Confirm the supported MSBuild version and command-line-only applicability. |
| `.runsettings` | Settings for VSTest-compatible test execution and data collection. | Does the application's runner support this format, and is test configuration repeated or inconsistent? Do not assume NUnit ConsoleRunner consumes it. |
| `testconfig.json` | Configuration for Microsoft.Testing.Platform (MTP) and compatible test frameworks. | Only investigate if the selected test platform uses it; it is **not** a drop-in replacement for every `.runsettings`-based runner. |

Other relevant configuration (such as `.sln`/`.slnx`, project-level properties, analyzer packages and CI workflow definitions) should be inventoried when it affects the proposed change. A file can exist without providing any worthwhile modernization opportunity.

## Discovery process

1. **Inventory reality.** Locate existing files and applicable parent-directory configuration; record project formats, target frameworks, SDK/MSBuild/NuGet versions, test platform and CI commands. Identify duplicated, conflicting or environment-dependent settings.
2. **Check applicability and scope.** Determine which configuration files the actual tools load, in what order, and whether settings affect individual projects, solution builds, restore, analysis, testing or just the editor. A file name alone does not establish that its behavior is active.
3. **Identify a concrete benefit.** State the maintenance, consistency, security, reproducibility or compatibility problem the proposed change would solve. Prefer smaller changes with measurable outcomes; **do not** recommend adopting a file solely because it is available.
4. **Consider interactions.** Check MSBuild import/override precedence, SDK selection and installed SDKs, NuGet config layering and `packages.config` vs `PackageReference`, formatter/analyzer enforcement, and test-runner compatibility.
5. **Test a minimal hypothesis.** Use an isolated copy/branch, record the exact baseline SHA and environment, and capture evaluated properties or tool selection **before and after**. Include a negative control when it answers a real question.
6. **Verify contracts.** Run the relevant restore/build/test/API/resource/XML-doc/package/consumer/security gates. Report failures, skips and checks not executed; distinguish a successful workflow from successful individual experiment steps.
7. **Record a disposition.** Treat findings as evidence, recommendations as proposals, approved decisions as explicit authorization, and implementations as separately verified changes in the application repository.

## Suggested assessment entry

Keep entries short; do not create empty documents or experiments for inapplicable files. Use the [evaluation overview template](../templates/evaluation-overview.md) to summarize the applicable areas.

| Area or file | Applicability | Assessment state | Observation or question | Proposed action / evidence |
|---|---|---|---|---|
| `<file or mechanism>` | Applicable / Not applicable / Undetermined | Evaluated / Deferred / Not yet assessed | `<specific observation or question>` | `<no change, hypothesis, experiment or evidence link>` |

- **Evaluated:** inspected or tested with documented results; evidence outcome (verified, partially verified, etc.) is recorded **separately**.
- **Deferred:** applicable or potentially useful but intentionally outside the current evaluation, with a reason.
- **Not applicable:** project format, test runner or other explicit constraint makes the mechanism irrelevant.
- **Not yet assessed:** may be relevant but has not been examined; do not silently label it supported or rejected.
- **Undetermined applicability** is legitimate when the environment or imports have not yet been inventoried.

No assessment state implies that a proposed change is approved or implemented.

## First application example: RecordSift

The [RecordSift November 2026 pre-SDK evaluation](../projects/recordsift/evaluations/2026-11-pre-sdk/README.md) already documents specific evidence: root `Directory.Build.props` with shared `LangVersion` passed its isolated compatibility checks; `Directory.Build.targets` imports were observed but no new target was warranted; and `global.json` SDK selection/roll-forward was tested, while pinned-SDK formatter/build behavior remains unverified.

That does **not** establish that the other mechanisms above are appropriate for RecordSift or for traditional .NET Framework projects generally. The original dated evaluation remains its own evidence record, not a universal configuration recommendation.

## Primary references

- Microsoft: [Customize the build by folder](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory).
- Microsoft: [Customize solution builds](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-solution-build).
- Microsoft: [MSBuild response files](https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild-response-files).
- Microsoft: [Configuration files for code analysis rules](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/configuration-files).
- Microsoft: [Global.json overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json).
- Microsoft: [NuGet central package management](https://learn.microsoft.com/en-us/nuget/consume-packages/Central-Package-Management).
- Microsoft: [NuGet.Config reference](https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file).
- Microsoft: [NuGet PackageReference and lock files](https://learn.microsoft.com/en-us/nuget/consume-packages/package-references-in-project-files).
- Microsoft: [Install local .NET tools](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-tool-install).
- Microsoft: [Configure tests using runsettings](https://learn.microsoft.com/en-us/visualstudio/test/configure-unit-tests-by-using-a-dot-runsettings-file).
- Microsoft: [Microsoft.Testing.Platform configuration](https://learn.microsoft.com/en-us/dotnet/core/testing/microsoft-testing-platform-config).

**Assessment added:** November 2, 2026. Verify support and behavior against the tool versions used by each application.
