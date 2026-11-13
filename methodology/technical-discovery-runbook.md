# .NET Technical Discovery — Step-by-Step Guide

**Purpose:** Explain how to evaluate each numbered field in the [blank discovery baseline](../templates/application-baseline.md). Copy that baseline before starting, then enter actual findings **only in the copy**. Never record results in this guide.

**For single-value fields, enter only the value:** one category (such as `Library`), status (`Public`), version, date, SHA, or complete URL. Do not append comments, evidence-source labels, or explanatory qualifications in the Value cell. Record provenance and interpretation in an evidence manifest or a table's explicitly labeled evidence column, not by changing the meaning of a field.

A number identifies a **single field** or a **dataset/table**. For a numbered table, its headings define the columns and **each row is one record**. Add rows when a project has multiple frameworks, configurations, references, or other instances. Keep source-declared values separate from observed, evaluated and executed results. Use `Not checked`, `Not executed` or `Not applicable` when warranted; don't guess. Retain evidence and redact personal paths, tokens and credentials.

These commands are Windows PowerShell examples. Use the host appropriate to the application. **RecordSift requires a Windows host, not WSL, Linux or macOS.** Do not change application source or publish anything during discovery.

## DISC-001 — Record discovery details, check tools, and create a clean source checkout

### Name and describe the application

- In the **copied baseline**, replace `<Application Name>` in the top-level heading with the application's actual name. The title should read `<Application Name> — Discovery baseline`. RecordSift's copied baseline already has the application name in its title.
- On the line **immediately below the title**, replace `<Application description>` with a concise, factual paragraph describing what the application does, its main responsibilities, and its intended users or consumers. Start with the README and application documentation; corroborate important claims using source when possible.
- **Do not create separate numbered fields for the application name or description.** They belong in the title and paragraph, not in the Application Information table. Keep modernization recommendations out of the description.
- Keep the instructions link below the description. This guide contains no recorded answers.

### Identify the discovery

- **16. Discovery By:** Enter the name of the person doing the discovery.
- **17. Discovery Date:** Enter the date the discovery began, in `YYYY-MM-DD` format. Use this date for the overall assessment; do not capture a separate collection date for every piece of evidence.
- **18. Discovery Folder:** Record the actual timestamped checkout folder created below, not a planned path.

### Check the Windows host

**23. Operating System Name; 24. Operating System Version; 25. Operating System Build; 26. Operating System Architecture**

Run this built-in Windows command:

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

- Set **23** from `Caption`, **24** from `Version`, **25** from `BuildNumber`, and **26** from `OSArchitecture`. Each field gets only its own value.
- If the application requires Windows and you're not on Windows, switch to a supported Windows host before proceeding.

**27. PowerShell Version — Windows PowerShell 5.1 or PowerShell 7**

```powershell
$PSVersionTable.PSVersion
```

- Enter the version in **27**. If PowerShell isn't available, see [Microsoft's installation instructions](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).

**28. Git Version — required; minimum 2.23 for `git switch`**

```powershell
git --version
```

- Enter the reported version in **28**. If missing or too old, [install Git for Windows](https://git-scm.com/install/win), reopen PowerShell and repeat this check. Stop before cloning if Git is unavailable.

**29. .NET SDK Inventory; 30. .NET Runtime Inventory — not required merely to clone**

```powershell
dotnet --info
```

- Check whether the SDK is available. DISC-004 uses dedicated commands to fill the **29** and **30** tables. If absent and needed later, [install the appropriate .NET SDK](https://dotnet.microsoft.com/en-us/download). No particular modern SDK version is assumed for all legacy projects.

**31. MSBuild Version; 32. MSBuild Installation Source — needed for supported builds**

```powershell
msbuild -version -nologo
```

- Enter the version in **31** and the location/product supplying MSBuild in **32**. If not found on PATH, try Visual Studio Developer PowerShell before concluding it is uninstalled. If required, obtain [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the appropriate .NET Framework components.

**33. NuGet CLI Version — needed for some restores, including RecordSift**

```powershell
nuget help
```

- Enter the reported version in **33**. If not found and needed, follow the [NuGet CLI installation guide](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli).

**34. .NET Framework Targeting Pack Inventory — applicable to traditional .NET Framework builds**

```powershell
Test-Path "${env:ProgramFiles(x86)}\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8"
```

- For RecordSift, add a row with `Framework Version` = `.NET Framework 4.8`, `Installed` = the actual `True` or `False` result, and `Location` = the path checked. Repeat for any other required targeting packs.
- If missing, check Visual Studio components or the [.NET Framework 4.8 Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).
- A directory existing does not prove that an application builds.

**35. Test Runner Inventory** is populated after identifying the actual runners at DISC-010. Its columns are `Runner Name`, `Runner Version` and `Source or Location`; create one row per runner.

### Select and isolate the source

- **5. HTTPS Clone URL:** Record the repository's actual HTTPS clone address.
- **19. Selected Source Branch or Tag:** Record the branch/tag used when choosing the snapshot, if applicable.
- **20. Source Commit SHA:** Record the full immutable SHA you actually checked out.
- **21. Working Tree Clean:** Record whether `git status` shows tracked or untracked changes.
- **22. Detached HEAD:** Record whether the checkout is detached.
- **7. Repository Default Branch:** Record the default branch shown by the repository host, not an assumption based on your checkout.

Create a **new timestamped folder** with `discovery` in the name, avoiding any existing directory. Replace the example repository and URL first. Run each command individually:

```powershell
$repository = 'REPOSITORY'
```

```powershell
$remoteUrl = 'https://github.com/OWNER/REPOSITORY.git'
```

```powershell
$discoveryRoot = Join-Path (Join-Path $HOME 'source') 'discoveries'
```

```powershell
New-Item -ItemType Directory -Path $discoveryRoot -Force
```

```powershell
$discoveryFolder = "$($repository)-discovery-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
```

```powershell
$destination = Join-Path $discoveryRoot $discoveryFolder
```

```powershell
Test-Path -LiteralPath $destination
```

**Continue only if the result is `False`**. Choose a new timestamp if the destination already exists; never delete, reset or overwrite another checkout.

```powershell
git clone --no-checkout $remoteUrl $destination
```

```powershell
Set-Location -LiteralPath $destination
```

```powershell
git switch --detach FULL_COMMIT_SHA
```

Replace `FULL_COMMIT_SHA` with the selected immutable commit. Stop on errors. A fresh checkout does not mean SDK installations or caches are clean.

### Verify what was actually checked out

Run each command from inside the checkout:

```powershell
git rev-parse --show-toplevel
```

```powershell
git rev-parse HEAD
```

```powershell
git branch --show-current
```

```powershell
git status --porcelain=v1 --untracked-files=all
```

```powershell
git remote get-url origin
```

- Confirm that `HEAD` matches **20**. A blank branch name indicates a detached checkout for **22**; blank porcelain status supports a clean working tree for **21** (but does not cover ignored files).
- Use the actual folder for **18** and remote URL for **5**. Record failures or nonstandard states rather than assuming success.
- If working in an existing checkout instead, inspect it first; do **not** reset or clean it.

## DISC-002 — Inventory the application, solutions and projects

- Check that the application name in the baseline title and the description immediately underneath it accurately reflect the README, application documentation and source. Revise those two lines if source inspection reveals a mistake.
- Complete **1. Application Type**, **2. Repository Visibility**, **3. License**, **4. Supported Operating Systems**, and **6. SSH Clone URL** (if used), using repository metadata and source rather than guesses.
- For application version concepts, keep **8. Published Application Version**, **9. Published Package Version**, **10. Published Release URL**, **11. Published Package URL**, **12. Source Manifest Version**, **13. Assembly Version**, and **14. File Version** separate. Record the source of each.
- **15. Consumers and Entry Points** is a table: `Consumer or Entry Point` names the executable, library API, service or consumer; `Type` classifies it; `Source or Evidence` links to the declaration, documentation or observed usage. One row per identified entry point/consumer.

List tracked solution and project files:

```powershell
git ls-files "*.sln" "*.slnx" "*.slnf" "*.csproj" "*.fsproj" "*.vbproj"
```

Where an installed SDK supports the solution, list its members:

```powershell
dotnet sln .\path\to\solution.sln list
```

**36. Solutions — one row per solution and meaningful configuration/platform combination.**

Columns:
- `Solution Path`: tracked relative path to the solution
- `Format`: `.sln`, `.slnx` or relevant filter format
- `Format Version` and `Declared IDE Version`: values declared by the solution, not locally installed IDE versions
- `Configuration` and `Platform`: solution-level choices, e.g. Debug and Any CPU
- `Membership / Build Exclusions`: projects included, excluded, or mapped differently by that combination

**37. Projects — one row per project and applicable target framework.**

Columns:
- `Project Path`: repository-relative project file, including projects outside solutions
- `Role`: production, test, tool or other evidenced purpose
- `Project Format`: SDK-style or traditional
- `Target Framework`: declared framework or one framework per row for multitargeting
- `Language Version`: declared language version, or note that it is not declared
- `Output Type`: library, executable, etc.
- `MSBuild Platform`: the MSBuild `Platform` value, distinct from processor target
- `SDK or ToolsVersion`: whichever project mechanism is declared
- `Direct Project Reference`: one referenced project path per row; repeat the project row for multiple direct references, and do not confuse direct and transitive dependencies

*Illustrative project row only—not a RecordSift finding:*

| Project Path | Role | Project Format | Target Framework | Language Version | Output Type | MSBuild Platform | SDK or ToolsVersion | Direct Project Reference |
|---|---|---|---|---|---|---|---|---|
| `src/Example.Core/Example.Core.csproj` | Library | Traditional | `net48` | 7.3 | Library | AnyCPU | ToolsVersion 15.0 | None |

A solution listing is not proof that every project was built, and source paths alone do not establish the effective target framework.

## DISC-003 — Read project declarations and conditional settings

- Inspect each `.csproj`, `.fsproj` or `.vbproj`. Determine SDK-style versus traditional imports, `TargetFramework` / `TargetFrameworks` / `TargetFrameworkVersion`, project references and conditional values.
- Complete and refine **37. Projects** based on actual declarations. An SDK-style project can still target .NET Framework.

**38. Compiler Settings** — one row per project, configuration, framework, and property. `Project Path` identifies the file; `Configuration` and `Framework` identify the context; `Property` could be `DebugType`, `Optimize` or `DefineConstants`; `Declared Value` gives the source declaration; `Condition` records the MSBuild condition.

**39. Output and Validation Settings** — `Project Path` and `Configuration` identify the scope; `Property` names settings such as `OutputPath`, `WarningLevel`, `TreatWarningsAsErrors` or `DocumentationFile`; `Declared Value` and `Condition` identify the declaration and when it applies.

**40. Project Metadata and Imports** — `Project Path` identifies the project; `Metadata or Import Name` names `IsTestProject`, `FileAlignment`, `AppDesignerFolder` or an imported props/targets file; `Declared Value` records the value/path; `Source File` shows where it was declared.

Use one record per property rather than packing several unrelated settings into a cell. Keep source declarations distinct from the evaluated values in DISC-005.

## DISC-004 — Complete the toolchain inventory

Run one native command at a time. Use earlier prerequisite results rather than repeating checks needlessly.

**29. .NET SDK Inventory**

```powershell
dotnet --list-sdks
```

For **each installed SDK**, record one row. `SDK Version` is its version; `Installation Path` is the location shown. If the command fails, record that as a check failure rather than an SDK row.

**30. .NET Runtime Inventory**

```powershell
dotnet --list-runtimes
```

For **each runtime**, record `Runtime Name` (e.g. runtime family), `Runtime Version` and `Installation Path`.

For MSBuild (**31**, **32**) and NuGet (**33**), use the individual checks from DISC-001 and note which installation supplied the tool. Recheck in Visual Studio Developer PowerShell when needed. For **34. .NET Framework Targeting Pack Inventory**, add a row per pack actually checked; do not infer the installed state from the SDK list.

**35. Test Runner Inventory** is completed when the project's actual runner is identified. `Runner Name` and `Runner Version` come from its native version output or verified package/runner installation; `Source or Location` identifies that origin.

## DISC-005 — Evaluate MSBuild settings without building

- Read project files and applicable imported `.props` and `.targets` files first.
- If MSBuild **17.8 or later** is available and compatible, try the native property query:

```powershell
msbuild .\path\to\project.csproj -getProperty:TargetFramework -getProperty:TargetFrameworkVersion -p:Configuration=Release
```

**41. Evaluated MSBuild Properties** — one row per property and evaluated configuration. `Project Path` identifies the evaluated project; `Configuration` and `Framework` identify the context; `Property` names the evaluated setting; `Evaluated Value` is actual output; `Declared Value` is the relevant source declaration (when known); `Evidence` points to the command/output.

If this MSBuild version cannot evaluate those properties, record the limitation instead of reporting source declarations as evaluated results.

## DISC-006 — Inspect directories and shared configuration

- Look for `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, NuGet configuration, `.editorconfig`, nested files and conditional imports.

**42. Repository Directories** — `Directory` is a relative path and `Purpose` is its evidenced role. One row per meaningful directory.

**43. Repository Configuration** — `File or Mechanism` is a path or inherited mechanism; `Present` is a checked yes/no (not an assumption); `Scope` identifies the directory, project or environment affected; `Setting Name` and `Setting Value` represent **one setting per row**; `Import or Precedence` describes how the setting applies. Repeat rows for multiple settings in one file.

A missing tracked file does not establish that no machine-level, imported, user-level or generated configuration applies.

## DISC-007 — Inventory dependencies without restoring

- Read `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, central package versions, and evidenced non-NuGet dependencies.
- List configured feeds when the SDK is available:

```powershell
dotnet nuget list source
```

**44. NuGet Package Declarations** — one row per package **per consuming project**. `Project Path` is its consumer; `Package ID` and `Declared Version` come from the declaration; `Declaration File` identifies `packages.config`, the project, or central source; `Configured Feed` is the configured source where relevant, **not proven acquisition origin**; `Purpose` is an evidenced production, test or tool role.

*Illustrative declaration row only:*

| Project Path | Package ID | Declared Version | Declaration File | Configured Feed | Purpose |
|---|---|---|---|---|---|
| `tests/Example.Tests/Example.Tests.csproj` | `Example.Testing` | 1.2.3 | `packages.config` | `nuget.org` | Test |

**45. Other External Dependencies** — `Consumer` identifies the project or component; `Dependency` names the item; `Type or Mechanism` distinguishes managed assembly, native DLL, COM, service/API, etc.; `Declaration Source` locates the relevant reference; `Version or Identity` records what is known; `Resolution or Location` records verified resolution or explicitly unknown.

Do not restore yet. A declared package or configured feed is not evidence of a successful restore.

## DISC-008 — Restore dependencies only after reviewing side effects

- Find existing application/CI restore instructions. Determine whether traditional `packages.config` projects use `nuget restore`, or PackageReference projects use `dotnet restore` or an MSBuild restore.
- Review credentials, feeds, caches, generated files and other writes **with the operator** before running the command.

**46. Operation Commands** — add a row for the discovered restore command: `Operation` = restore; `Project or Solution` is the target; `Configuration` and `Platform` describe applicable scope; `Command or Workflow` is the exact native invocation; `Source` is documentation or CI identifying it.

**47. Restore Outcomes** — one row per attempted restore. `Source Revision` is the checked-out SHA; `Target` is the solution/project; `Outcome` is passed, failed or blocked; `Error or Note` captures relevant diagnostic; `Evidence` links to the command output. If not run, mark not executed in the copied baseline.

**55. Executed Command Evidence** is the shared audit table for restore, build, tests and other actual commands. Its columns are explained at DISC-013. Never mark a planned command as executed.

## DISC-009 — Build the application in the observed configuration

- Identify existing build commands and the intended project/solution, configuration, platform and framework. Choose `msbuild` or `dotnet build` according to the actual project.
- Review write side effects before execution. Do not substitute Rebuild for Build without approval.

In **46. Operation Commands**, add a build row with the exact command and scope.

**48. Build Outcomes** — one row per revision, build target, configuration and platform. `Source Revision` pins the commit; `Target` is the solution or project; `Configuration` and `Platform` identify build settings; `Outcome` is pass/fail/blocked/not executed; `Warning Count` and `Error Count` are observed diagnostics, not estimates; `Output or Evidence` links to logs or generated outputs.

Repeat for distinct build combinations. Record actual execution in **55**.

## DISC-010 — Run the application's existing tests

- Identify test projects and the actual runner. The appropriate command may be `dotnet test`, VSTest, NUnit or a project-specific runner. Confirm environment and side effects before executing.
- Populate **35. Test Runner Inventory** with one row per runner. Add the test command to **46. Operation Commands**.

**49. Test Outcomes** — one row per test project/assembly and execution scope. `Source Revision` pins the tested commit; `Test Project or Assembly` identifies what actually ran; `Runner` names the tool; `Discovered`, `Passed`, `Failed` and `Skipped` are individual counts; `Outcome` states the check result; `Evidence` points to runner output.

*Illustrative test row only—not an observed execution:*

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
| `<commit SHA>` | `Example.Tests` | VSTest | 12 | 11 | 0 | 1 | Passed | `<report path>` |

Only report a test suite as fully passed when expected test projects were actually included. Capture actual executions in **55**.

## DISC-011 — Review CI, packages and deployment

- Read existing CI/CD definitions and distinguish what they **configure** from actual runs. Do not trigger deployment or releases during discovery.

**50. CI Workflows** — `Workflow Path` locates the definition; `Trigger` identifies push, pull request or manual triggers; `Runner OS` is the declared host; `Configured Command` records one configured invocation per row; repeat the workflow row for additional commands; `Artifact or Deployment` describes produced outputs or destinations.

**51. CI Runs** — one row per checked run. `Workflow` identifies it; `Run URL` links the exact run; `Commit SHA` pins its source; `Outcome` records its actual result; `Date` is when it ran.

**52. Package and Release Artifacts** — `Artifact` is the package/file; `Version` is the published version; `Attribute` names one observed package/content/metadata property and `Attribute Value` holds its value; repeat the artifact row for other attributes; `Release URL` links to it; `Evidence` supports the observation.

**53. Runtime and Deployment Requirements** — `Requirement` describes the dependency or setting; `Type` classifies it (runtime, OS, service, installer, etc.); `Target Environment` identifies where required; `Source or Evidence` supports it. Use a separate row per requirement.

Add any applicable packaging, compatibility, consumer or deployment commands to **46**. Record alternate CI toolchains in the relevant tool inventory with their host identified.

## DISC-012 — Identify existing compatibility checks

- Look for checks of public APIs, assembly identity, embedded resources, XML documentation, package contents/metadata, dependency validation, vulnerability audits, installed consumers and application behavior.

**54. Compatibility Checks** — one row per distinct check. `Check Type` names the compatibility concern; `Target` identifies the application/component; `Method or Command` records how it is checked; `Outcome` states passed/failed/not executed/not applicable; `Commit SHA` identifies the source revision; `Evidence` links to actual results.

Do not invent new checks just to fill the table, and do not apply results from a different commit without labeling them historical.

## DISC-013 — Reconcile results and gaps

**55. Executed Command Evidence** — one row for every actual command that matters to reproducing a finding. `Discovery Step` identifies the `DISC-###` section; `Command` is the exact invocation; `Working Directory` is where it ran; `Tool Version` records its environment; `Target or Configuration` clarifies scope; `Exit Code` is observed when available; `Outcome` says passed/failed/blocked; `Output or Evidence` points to the captured output.

*Illustrative evidence row only—not an actual result:*

| Discovery Step | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
| `DISC-002` | `git ls-files "*.csproj"` | `<checkout root>` | Git 2.45.0 | Repository | 0 | Passed | `<saved output path>` |

**56. Findings and Gaps** — one row per gap. `Finding` describes the verified issue or missing information; `Impact` explains why it matters; `Evidence` points to a source; `Next Check` names the next concrete verification step.

**57. Discovery Step Status** — one row per `DISC-001` through `DISC-014`. `Step ID` identifies it; `Status` is done/partial/blocked/not executed; `Evidence or Missing Information` makes that assessment traceable.

Check that results refer to the correct commit, host, project, framework and configuration. Distinguish a missing tool from an application failure.

## DISC-014 — Review and finish the baseline

- **58. Overall Baseline Disposition:** Record complete, complete with gaps, or more verification needed.
- **59. Reviewed By:** Enter the reviewer.
- **60. Review Date:** Enter the date reviewed.
- **61. Next Action:** Record one concrete next action.

**62. Deferred Checks** — one row per intentional deferral. `Check` identifies it; `Reason Deferred` explains why it could not or should not run; `Revisit When` specifies the trigger for revisiting it.

The discovery uses one Discovery Date. Keep a CI run's actual date when it is part of the CI run record. Make sure the copied baseline contains observed answers, relevant repeated rows, evidence links and clearly identified gaps. Keep modernization proposals separate.

## Optional — Create scripts only after manual discovery

- Start with individual native Git, SDK, NuGet, MSBuild and test commands. Consider wrappers only to improve repeatability or output formatting after manual results are understood.
- Make paths, project formats, frameworks, configurations, operating systems and output destinations configurable.
- Clearly label what was tested on Windows/traditional .NET Framework projects versus what is portable to other applications; do not imply a RecordSift-specific script works everywhere.
- Preserve raw outputs and errors. Do not publish or modify application source as part of discovery.

## Where to keep the results

- **Guide:** `methodology/technical-discovery-runbook.md` (instructions, definitions and illustrative rows, never findings).
- **Blank template:** [`templates/application-baseline.md`](../templates/application-baseline.md) (copy before each discovery).
- **Filled application baseline and evidence:** `projects/<app>/evaluations/<dated-discovery>/`.
- **Case study:** the [blank RecordSift baseline](../projects/recordsift/evaluations/2026-11-technical-baseline/baseline.md) is ready for user-run Windows discovery.
- **Blog:** publish selected observations and evidence separately in `infoconex/coding-blog` only when authorized.
