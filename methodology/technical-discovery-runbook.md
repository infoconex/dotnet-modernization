# .NET Technical Discovery — Step-by-Step Guide

Follow this guide alongside the [blank baseline template](../templates/application-baseline.md). Its **62 numbered headings match the baseline exactly, in the same order**, and no separate DISC phase numbering is required. Record results in the application's **copied baseline**, not here.

**Before item 1:** Replace `<Application Name>` in the copied baseline title with the actual application name. Immediately below it, replace `<Application description>` with a factual description of what the application does, its users/consumers, and core responsibilities; verify against the README, documentation and source. For RecordSift, the copy already has its name and description.

**Recording rules:** A single-value field contains only one value (for example `Library`, `Public`, `MIT`, a precise version, `True`, a path, or a URL). Keep citations, assumptions, and explanations in the evidence manifest or a specifically designated table evidence column. For a numbered table, the number identifies **the entire dataset**, never its columns or rows. Add one record per applicable item. Mark unavailable checks `Not checked`, `Not executed` or `Not applicable` accurately.

**Environment boundary:** RecordSift itself is Windows-only. Perform its operator-run host, restore, build and test checks on **Windows**, not on Linux, macOS or WSL. Existing GitHub Actions results are separate from local operator execution. Start with native Git, PowerShell, .NET SDK, NuGet and MSBuild commands; use custom scripts only after their necessity and portability are understood. Do not reset worktrees, modify source, publish packages or deploy as part of discovery. Confirm explicit approval before restore/build/test operations.

## Application information

### 1. Application Type

Inspect the README, project file and architecture documentation. Classify the application with **one concise value** such as `Library`, `Console application`, `Desktop application`, `Service` or `Web application`. For RecordSift, the type is `Library`. Put implementation details in the description below the title, not this field.

### 2. Repository Visibility

Inspect repository visibility in the hosting service. Record `Public` or `Private`. A locally available clone does not prove a repository is public.

### 3. License

Read the repository's actual `LICENSE` and any package licensing metadata. Record an SPDX identifier such as `MIT` where appropriate. Keep the source link in the evidence manifest.

### 4. Supported Operating Systems

Read the supported-platform statement in README and release/consumer guidance, not the operating system of the discovery machine. Record one supported OS per repeat entry or a concise list. For RecordSift record `Windows`; its .NET Framework target belongs in the project inventory.

### 5. HTTPS Clone URL

Use the hosting service's **Clone → HTTPS** address. Record the exact URL, such as `https://github.com/infoconex/RecordSift.git`, without a citation suffix. Do not run a clone merely to collect this address.

### 6. SSH Clone URL

Use the hosting service's **Clone → SSH** address. This is metadata, **not** an SSH authentication test. For GitHub a conventional value is `git@github.com:infoconex/RecordSift.git`.

### 7. Repository Default Branch

Read the repository host's **default branch** designation. Record one branch name, such as `main`, not the currently checked out detached HEAD.

### 8. Published Application Version

Identify the published application version, if one exists. If the project distributes only a library package rather than a standalone application, record `Not applicable` or the publisher-documented application version only when explicitly supported. Do not confuse source manifest, assembly and package versions.

### 9. Published Package Version

Check the official package registry/release listing. For RecordSift, NuGet.org lists `0.1.0`. Enter only the version number; put the URL in item 11.

### 10. Published Release URL

Copy the full official published release URL, not a short link label. For RecordSift: `https://github.com/infoconex/RecordSift/releases/tag/v0.1.0`.

### 11. Published Package URL

Copy the full registry package URL, e.g. `https://www.nuget.org/packages/RecordSift/0.1.0`. Keep package and release URLs distinct.

### 12. Source Manifest Version

Read the tracked package manifest, such as `packaging/RecordSift.nuspec`. Record its version **as declared**, even if it differs from a published version. RecordSift declares `0.1.0-rc.1` in this source file.

### 13. Assembly Version

Read `AssemblyVersion` in the applicable `Properties/AssemblyInfo.cs` (or generated assembly metadata for SDK-style projects). Record the declared value; if assemblies differ, explain the scope and use a per-assembly table rather than implying one universal value. Do not claim the binaries have been inspected.

### 14. File Version

Read `AssemblyFileVersion` separately from `AssemblyVersion` in the relevant assembly metadata. Record only its version, e.g. `0.1.0.0`; do not append an `AssemblyInfo` citation in the value.

### 15. Consumers and Entry Points

Inspect public entry-point documentation, production project output types, exported APIs and known consumer examples. **One row per distinct consumer/entry point**, with supporting documentation or source. Example: `Consuming .NET Framework app | Library consumer | docs/usage/getting-started.md`. Do not assert that a test consumer is a deployed application.

**How to populate each column (left to right):**

- **Consumer or Entry Point:** Identify the consuming application or exposed entry point.
- **Type:** Classify it, such as library API or consumer.
- **Source or Evidence:** Link to source, API documentation, or usage evidence.

**Illustrative example only; not a new observed finding:**

| Consumer or Entry Point | Type | Source or Evidence |
|---|---|---|
| RecordSift library consumer | Library API | docs/usage/getting-started.md |

## Discovery information

### 16. Discovery By

Record the actual person performing this discovery; do not infer the name from repository ownership or an illustrative example. If not provided, use `Not recorded` rather than inventing an operator.

### 17. Discovery Date

Record the single date this discovery began in `YYYY-MM-DD` format. Do **not** add evidence-collection dates to each item. External CI run dates remain intrinsic to CI records in item 51.

## Discovery host and prerequisite tools

### 18. Operating System Name

Use Windows (required for RecordSift); record the **Caption** output from the command below. This is the discovery host, not the application's supported OS (item 4).

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

**One OS command populates items 18–21.** Run it once, record four separate values, and do not repeat it for each heading.

### 19. Operating System Version

From the same Windows OS command, record **Version** and nothing else.

Use the output from the command in item 18.

### 20. Operating System Build

From the same Windows OS command, record **BuildNumber** only.

Use the output from the command in item 18.

### 21. Operating System Architecture

From the same Windows OS command, record **OSArchitecture** only.

Use the output from the command in item 18.

### 22. PowerShell Version

Run the PowerShell version command below. Record only the complete version (e.g. `7.4.7`), not your username or environment details. Windows PowerShell 5.1 or modern PowerShell 7 may be used; if unavailable, follow [Microsoft's Windows installation guide](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).

```powershell
$PSVersionTable.PSVersion.ToString()
```

### 23. Git Version

Run the Git version command below and record only the version number. `git switch` requires Git 2.23 or later. If missing, install [Git for Windows](https://git-scm.com/install/win) before cloning.

```powershell
git --version
```

### 24. .NET SDK Inventory

Run `dotnet --list-sdks` and add **one row for each installed SDK** with its version and installation path. If no `dotnet` CLI is installed, record the check as blocked; do not fabricate SDK rows. The .NET SDK is not necessarily required just to clone traditional projects. Install only a needed SDK from [Microsoft .NET downloads](https://dotnet.microsoft.com/en-us/download).

```powershell
dotnet --list-sdks
```

**How to populate each column (left to right):**

- **SDK Version:** One installed SDK version per row.
- **Installation Path:** The installation directory returned by the SDK command.

### 25. .NET Runtime Inventory

Run `dotnet --list-runtimes` and add one row per reported runtime family, version and installation path. The list of modern .NET runtimes does **not** establish installation of the .NET Framework 4.8 targeting pack.

```powershell
dotnet --list-runtimes
```

**How to populate each column (left to right):**

- **Runtime Name:** Runtime family or host, such as Microsoft.NETCore.App.
- **Runtime Version:** Its exact installed version.
- **Installation Path:** The directory reported by the runtime command.

### 26. MSBuild Version

Run `msbuild -version -nologo` from Visual Studio Developer PowerShell, or another command environment with MSBuild on PATH. Record the reported version. A missing PATH entry is not proof MSBuild is uninstalled; use Visual Studio's Developer PowerShell or `vswhere`. [Build Tools installation](https://visualstudio.microsoft.com/downloads/).

```powershell
msbuild -version -nologo
```

### 27. MSBuild Installation Source

Identify the MSBuild installation source separately, such as `Visual Studio 2022 Enterprise` or the verified location of MSBuild.exe. If using `Get-Command msbuild`, the `Source` property identifies the executable path. Do not use the version number in this field.

```powershell
Get-Command msbuild -ErrorAction SilentlyContinue | Select-Object Source
```

### 28. NuGet CLI Version

Run `nuget help` and record the version that the CLI prints. If NuGet is missing, follow [Microsoft's NuGet CLI installation guide](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli). This is not the version of a NuGet package referenced by the application.

```powershell
nuget help
```

### 29. .NET Framework Targeting Pack Inventory

For traditional .NET Framework projects, check the applicable **reference assemblies / targeting pack**, not merely the presence of a runtime. For RecordSift inspect the .NET Framework 4.8 reference assemblies directory with the command below. Use the output path shown by the command as the `Location` in the table. Add one row for each framework checked, with exact bool and checked path. If missing, see the [.NET Framework Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).

```powershell
$pack = Join-Path $env:ProgramFiles 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8'
if (${env:ProgramFiles(x86)}) { $pack = Join-Path ${env:ProgramFiles(x86)} 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8' }
$pack
Test-Path -LiteralPath $pack
```

**How to populate each column (left to right):**

- **Framework Version:** The framework and version being checked.
- **Installed:** True or False based on an actual installation check.
- **Location:** The exact path checked.

### 30. Test Runner Inventory

Identify the actual test runner from test project manifests or CI definitions, then check its installed version when possible. Record one runner per row; the package's declared version is not necessarily the locally installed runner. For RecordSift the declared runner is `NUnit.ConsoleRunner 3.17.0` in the test `packages.config`.

**How to populate each column (left to right):**

- **Runner Name:** Name the test runner, such as NUnit ConsoleRunner.
- **Runner Version:** The runner version, noting declared vs actually installed provenance separately.
- **Source or Location:** The verified executable or declared package source.

## Source revision and checkout

### 31. Discovery Folder

Choose an existing **parent directory** under which discovery checkouts can be created. Form a timestamped destination with `discovery` in its name, confirm it does not exist, then perform a clean `git clone --no-checkout`. Use the commands below as individual PowerShell invocations. This must not clean or delete an existing repository.

```powershell
$repository = 'RecordSift'
$remoteUrl = 'https://github.com/infoconex/RecordSift.git'
$discoveryRoot = Join-Path (Join-Path $HOME 'source') 'discoveries'
New-Item -ItemType Directory -Path $discoveryRoot -Force | Out-Null
$discoveryFolder = "$repository-discovery-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
$destination = Join-Path $discoveryRoot $discoveryFolder
$alreadyExists = Test-Path -LiteralPath $destination
$alreadyExists
if ($alreadyExists) { throw 'Discovery destination already exists; generate a new timestamp and stop.' }
git clone --no-checkout $remoteUrl $destination
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed. Stop before proceeding.' }
Set-Location -LiteralPath $destination
```

**Safety gate:** The command now **throws before cloning** if the destination exists. Generate a different timestamp rather than cleaning/deleting an existing folder. This clone creates files and requires network access. On failure, stop before items 33–35.

### 32. Selected Source Branch or Tag

Record the exact branch or tag **chosen as the source**, for example `main`. This is a selected remote ref, not proof the final local checkout remains attached to that branch (see item 35). Confirm it against repository metadata before pinning the SHA.

### 33. Source Commit SHA

Choose and record a **full immutable commit SHA** before checking out source. For RecordSift, the previously selected source SHA is `1809d06c0fade59e4769d16e0f8eaf10fa426004`. After the clean clone from item 31, use the commands below to detach at and verify that SHA. Never substitute a moving branch tip silently.

```powershell
$selectedCommit = '1809d06c0fade59e4769d16e0f8eaf10fa426004'
git switch --detach $selectedCommit
if ($LASTEXITCODE -ne 0) { throw 'Commit checkout failed. Stop before proceeding.' }
git rev-parse HEAD
git remote get-url origin
```

The commit must be present in the new clone. If this command fails, do not continue pretending checkout was successful. A detached checkout intentionally leaves item 35 = `True`.

### 34. Working Tree Clean

Run `git status --porcelain=v1 --untracked-files=all` **inside the cloned repository**. An empty result supports `True` for a clean working tree (tracked and untracked, excluding ignored files); any lines require review. Record only `True` or `False`. Do not run `git clean` or `git reset --hard`.

```powershell
git status --porcelain=v1 --untracked-files=all
```

### 35. Detached HEAD

Run `git branch --show-current` in the selected checkout. A blank branch name after `git switch --detach` indicates a detached HEAD; record `True`. An attached branch name indicates `False`. The actual SHA from item 33 is still authoritative.

```powershell
git branch --show-current
```

## Solution and project inventory

### 36. Solutions

Enumerate tracked solution files; inspect each solution header and project configuration mappings. For RecordSift `RecordSift.sln` declares format 12.00, Visual Studio 16 and Debug/Release × Any CPU. Use **one row per solution/configuration/platform combination**. `dotnet sln <path> list` is optional if a suitable SDK is installed; reading the solution source is always valid.

```powershell
git ls-files "*.sln" "*.slnx" "*.slnf"
# When a compatible .NET SDK is installed:
dotnet sln .\RecordSift.sln list
```

**How to populate each column (left to right):**

- **Solution Path:** The repository-relative solution file.
- **Format:** Solution format, such as .sln.
- **Format Version:** Format version declared in file header.
- **Declared IDE Version:** Visual Studio version declared in the solution header.
- **Configuration:** Each solution configuration.
- **Platform:** Each solution platform.
- **Membership / Build Exclusions:** Relevant project membership or exclusions for this combination.

**Illustrative example only; not a new observed finding:**

| Solution Path | Format | Format Version | Declared IDE Version | Configuration | Platform | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Release | Any CPU | 10 projects |

### 37. Projects

Enumerate tracked projects, including projects not listed in the solution. Inspect each project XML for its project type, target framework, output, language version, platform and direct references. **Repeat the project row for multiple target frameworks or direct project references**. For RecordSift the current baseline has ten traditional `.csproj` projects (five production, five tests) that target `v4.8` and declare `LangVersion=7.3`.

```powershell
git ls-files "*.csproj" "*.fsproj" "*.vbproj"
```

**How to populate each column (left to right):**

- **Project Path:** Relative path of the project file.
- **Role:** Production, test, tool, or other evidenced role.
- **Project Format:** Traditional vs SDK-style.
- **Target Framework:** One target framework for this row.
- **Language Version:** Declared language version or Not declared.
- **Output Type:** Library, Exe, WinExe, or other declared output.
- **MSBuild Platform:** Declared MSBuild Platform value.
- **SDK or ToolsVersion:** The declared SDK or ToolsVersion.
- **Direct Project Reference:** One direct referenced project path; repeat the row for more references.

**Illustrative example only; not a new observed finding:**

| Project Path | Role | Project Format | Target Framework | Language Version | Output Type | MSBuild Platform | SDK or ToolsVersion | Direct Project Reference |
|---|---|---|---|---|---|---|---|---|
| src/RecordSift.Domain/RecordSift.Domain.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | ToolsVersion 15.0 | None |

## Project settings and evaluated values

### 38. Compiler Settings

Read project XML under each unconditional or conditional `PropertyGroup`. Enter **one row per project, configuration, framework and compiler property** (e.g. `LangVersion`, `DebugType`, `Optimize`, `DefineConstants`). Preserve the actual condition and whether the value was merely declared in XML.

```powershell
Get-Content .\src\RecordSift.Domain\RecordSift.Domain.csproj
```

**How to populate each column (left to right):**

- **Project Path:** Source project path.
- **Configuration:** Configuration scope of this declaration.
- **Framework:** Target framework context.
- **Property:** One compiler property, such as LangVersion or Optimize.
- **Declared Value:** Its source-declared value.
- **Condition:** The condition that controls it or Unconditional.

### 39. Output and Validation Settings

Read project XML for `OutputPath`, `WarningLevel`, `WarningsAsErrors`, `DocumentationFile` and related properties. Enter one property per project/configuration row. A missing declaration is **not** proof of a particular evaluated default.

**How to populate each column (left to right):**

- **Project Path:** Source project path.
- **Configuration:** Applicable configuration.
- **Property:** One output/validation property.
- **Declared Value:** Declared value.
- **Condition:** Condition controlling that value.

### 40. Project Metadata and Imports

Inspect project-wide properties (`IsTestProject`, `FileAlignment`, `AppDesignerFolder`) and imported `.props`/`.targets` files. Record one metadata/import item per row and its source file; don't combine metadata names in a value cell.

**How to populate each column (left to right):**

- **Project Path:** Source project path.
- **Metadata or Import Name:** One metadata item or import name.
- **Declared Value:** Value or import path, as declared.
- **Source File:** File in which that declaration occurs.

### 41. Evaluated MSBuild Properties

Read declared properties first. When compatible **MSBuild 17.8 or later** is available, query individual evaluated properties with `-getProperty` using explicit configuration and framework. Record only actual MSBuild output under `Evaluated Value`; leave as Not checked if the operator hasn't executed it. A successful CI build alone doesn't establish this inventory.

```powershell
msbuild .\src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:TargetFrameworkVersion -getProperty:LangVersion -p:Configuration=Release
```

The property-query option depends on MSBuild version. On older installations, record `Not checked` and note the incompatibility, rather than calling source XML an evaluated property. Do not build just to satisfy this query.

**How to populate each column (left to right):**

- **Project Path:** Source project path.
- **Configuration:** Configuration evaluated.
- **Framework:** Target framework or framework context.
- **Property:** One property queried.
- **Evaluated Value:** Value actually emitted by MSBuild.
- **Declared Value:** Source-declared value if relevant.
- **Evidence:** Captured command/output location; not a presumed default.

## Repository structure and dependencies

### 42. Repository Directories

Use `git ls-files` or an equivalent tracked-tree listing to identify meaningful source, test, documentation, script, packaging and workflow directories. One row per directory and its evidenced purpose. Do not invent directories.

```powershell
git ls-files
```

**How to populate each column (left to right):**

- **Directory:** Tracked directory path.
- **Purpose:** Its demonstrated role.

### 43. Repository Configuration

Inspect `NuGet.Config`, `.editorconfig`, `global.json`, `Directory.Build.props/targets`, `Directory.Packages.props`, `.gitignore` and nested equivalents. Use one row **per setting** with source/scope and precedence. Absence from the tracked tree does not prove a machine-level setting or inherited MSBuild import is absent.

```powershell
git ls-files "NuGet.Config" ".editorconfig" "global.json" "Directory.*.props" "Directory.*.targets" "Directory.Packages.props"
```

**How to populate each column (left to right):**

- **File or Mechanism:** Tracked configuration path or discovered mechanism.
- **Present:** Whether verified present in the scoped source/environment.
- **Scope:** Repository, directory, project or machine scope.
- **Setting Name:** One named setting per row.
- **Setting Value:** That setting's actual value.
- **Import or Precedence:** How it is imported or which setting has precedence.

### 44. NuGet Package Declarations

Read `packages.config`, `PackageReference` and central versions as appropriate. Add one row per **package declaration per consuming project**. The feed column is configured source information and must **not** be described as proven download origin. Inspect sources via `dotnet nuget list source` if the SDK is present or the corresponding NuGet CLI command.

```powershell
dotnet nuget list source
```

This command requires the .NET CLI. If only NuGet CLI is available, use an equivalent `nuget sources List -ConfigFile NuGet.Config` command, without asserting the configured feed is the actual download origin.

**How to populate each column (left to right):**

- **Project Path:** Consuming project path.
- **Package ID:** Package identifier as declared.
- **Declared Version:** Exact declared version.
- **Declaration File:** Project, packages.config, or central declaration file.
- **Configured Feed:** Configured eligible feed, not asserted download origin.
- **Purpose:** Production, test framework, tool, or other purpose.

**Illustrative example only; not a new observed finding:**

| Project Path | Package ID | Declared Version | Declaration File | Configured Feed | Purpose |
|---|---|---|---|---|---|
| src/RecordSift.Infrastructure.Csv | CsvHelper | 33.1.0 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |

### 45. Other External Dependencies

Inspect project `Reference`/`HintPath`, `COMReference`/`COMFileReference`, native dependencies, executables, services and other external systems. One row per consumer/dependency; record unknown resolution explicitly. Project XML inspection alone cannot rule out dynamic runtime loading.

**How to populate each column (left to right):**

- **Consumer:** Project or component consuming the dependency.
- **Dependency:** Non-NuGet assembly, COM, native library, service or other dependency.
- **Type or Mechanism:** Declared dependency mechanism.
- **Declaration Source:** Source of the declaration.
- **Version or Identity:** Declared identity or version.
- **Resolution or Location:** Whether/how it was actually resolved, or Not checked.

## Restore, build, tests and delivery

### 46. Operation Commands

Inspect existing documentation, build scripts and CI workflows first. Record exact **configured** native commands and their affected project/configuration. For RecordSift these include `nuget restore`, `msbuild ... /t:Rebuild`, NUnit and existing compatibility scripts. Prefer manual execution of existing tools before creating wrappers. List a command here **before** choosing whether it is safe to execute.

**How to populate each column (left to right):**

- **Operation:** Restore, Build, Test, Pack, Check or another operation.
- **Project or Solution:** Affected solution/project/assembly.
- **Configuration:** Applicable configuration or Not applicable.
- **Platform:** Applicable MSBuild platform or Not applicable.
- **Command or Workflow:** Exact existing command or CI workflow entry point.
- **Source:** Source file documenting the command.

### 47. Restore Outcomes

Determine the appropriate native restore path based on project format: traditional `packages.config` may require `nuget restore`, while PackageReference projects may use SDK/MSBuild restore. Record the proposed exact command in item 46, inspect feeds/credentials/network/write effects, and get operator approval before execution. Report actual results only; cite existing CI runs separately from local checks.

```powershell
nuget restore .\RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
```

**Write/network operation.** Do not run automatically as part of reviewing this guide. Only run after confirming operator approval, feeds and workspace. Existing CI restore results may instead be reported with their exact run links and environment.

**How to populate each column (left to right):**

- **Source Revision:** Immutable source revision actually restored.
- **Target:** Project/solution targeted.
- **Outcome:** Passed, Failed, Blocked or Not executed.
- **Error or Note:** Observed diagnostic or Not applicable.
- **Evidence:** Exact output or CI run proving the result.

### 48. Build Outcomes

Review current build instructions and configured CI invocation. For RecordSift use Windows MSBuild with the same Release and Any CPU settings as CI. Builds write outputs; confirm the intended workspace and side effects with the operator first. Capture the actual build result and diagnostic counts if present, rather than claiming success from source declarations.

```powershell
msbuild .\RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
```

**Write/build operation.** Execute only after confirming approval and the correct Windows host. The configured CI command uses `Rebuild`; do not silently change it to `Build` or vice versa.

**How to populate each column (left to right):**

- **Source Revision:** Immutable source revision actually built.
- **Target:** Solution/project target.
- **Configuration:** Build configuration.
- **Platform:** MSBuild platform.
- **Outcome:** Passed, Failed, Blocked or Not executed.
- **Warning Count:** Observed warning count or Not recorded.
- **Error Count:** Observed error count or Not recorded.
- **Output or Evidence:** Build output and/or CI evidence.

### 49. Test Outcomes

Identify the test runner and **all intended test assemblies**. On RecordSift, a full suite spans five NUnit assemblies. After a successful appropriate build and operator approval, use the existing `scripts/run_tests.ps1` (or CI's runner command) and read the NUnit XML report. One row per executed assembly; do not substitute a previous run at another SHA.

```powershell
.\scripts\run_tests.ps1 -Level All
```

**Test execution.** Requires restored packages and built Release test assemblies. Execute only with operator approval and the correct Windows environment.

**How to populate each column (left to right):**

- **Source Revision:** Source SHA tested.
- **Test Project or Assembly:** Test project or built test assembly.
- **Runner:** Test runner name and version if known.
- **Discovered:** Discovered test count.
- **Passed:** Passed count.
- **Failed:** Failed count.
- **Skipped:** Skipped count.
- **Outcome:** Result of that execution.
- **Evidence:** Actual test result or CI run.

**Illustrative example only; not a new observed finding:**

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
| <exact SHA> | RecordSift.Infrastructure.Csv.Tests | NUnit | 132 | 131 | 0 | 1 | Passed | <CI log or report URL> |

### 50. CI Workflows

Inspect the tracked `.github/workflows/*.yml` definitions. One row per workflow/trigger/runner/job command as needed. Distinguish **configured CI** from actual execution, and never infer that release workflows ran merely because definitions exist.

```powershell
git ls-files ".github/workflows/*.yml" ".github/workflows/*.yaml"
```

**How to populate each column (left to right):**

- **Workflow Path:** Workflow file path.
- **Trigger:** Events that trigger it.
- **Runner OS:** Runner OS declared by a job.
- **Configured Command:** One command configured in that workflow; repeat rows.
- **Artifact or Deployment:** Produced artifact or deployment action, if any.

### 51. CI Runs

Read actual GitHub Actions run records, including their full source SHA, conclusion, run URL and run date. One row per run. For the selected RecordSift SHA there are existing successful build/test, consumer and documentation workflows. Their outcomes are **CI evidence**, not evidence that the operator's Windows host is configured.

The run date is an intrinsic part of the external workflow record; it is **not** a per-evidence collection date.

**How to populate each column (left to right):**

- **Workflow:** Workflow name.
- **Run URL:** URL of the specific run.
- **Commit SHA:** Actual tested source SHA.
- **Outcome:** Recorded conclusion/status.
- **Date:** Run date as part of the external CI record.

### 52. Package and Release Artifacts

Read published registry/release metadata separately from source `.nuspec` and generated CI-local packages. One row per artifact/attribute. Do not call a locally created release candidate a published package. Retain the artifact's source/evidence URL.

**How to populate each column (left to right):**

- **Artifact:** Package or release artifact name.
- **Version:** Published or source-declared version.
- **Attribute:** One artifact property, such as nuspec version or included DLL.
- **Attribute Value:** Value of that property.
- **Release URL:** Actual public release URL or Not published.
- **Evidence:** Source/CI proof of that exact property.

### 53. Runtime and Deployment Requirements

Read consumer guidance, architecture and package manifests for OS, target frameworks, runtimes, dependencies and deployment constraints. One requirement per row with the environment where it applies; do not assume a requirement is installed on the operator's machine.

**How to populate each column (left to right):**

- **Requirement:** One runtime, OS, installer, service or deployment requirement.
- **Type:** Classification of requirement.
- **Target Environment:** Where the requirement applies.
- **Source or Evidence:** Source that establishes the requirement.

### 54. Compatibility Checks

Identify existing compatibility gates (public API, assembly identity, XML documentation, package contents, vulnerability audit, consumer tests, resource identity, expected negative controls). A check is passed only when there is an actual result and matching source revision; unexecuted checks remain Not executed.

**How to populate each column (left to right):**

- **Check Type:** Specific compatibility check.
- **Target:** Affected project/library/package.
- **Method or Command:** Actual check command or procedure.
- **Outcome:** Passed, Failed, Blocked or Not executed.
- **Commit SHA:** Exact source SHA to which evidence applies.
- **Evidence:** Output, test report or CI run.

## Evidence and completion

### 55. Executed Command Evidence

After executing a command, record its exact invocation, working directory, tool version, exit code, outcome and saved output in a row tied to a **baseline item number**. Use actual logs where available, redact secrets and retain failed output too. Do not present a planned command or an inspected CI YAML line as a locally executed command.

Do not claim the discovery operator executed CI commands when only GitHub workflow logs were inspected.

**How to populate each column (left to right):**

- **Baseline Item:** The baseline item number supported by this execution.
- **Command:** Exact command executed.
- **Working Directory:** Directory in which command ran.
- **Tool Version:** Tool and version actually used.
- **Target or Configuration:** Project, configuration or applicable scope.
- **Exit Code:** Observed process exit code or Not recorded.
- **Outcome:** Passed, Failed or Blocked.
- **Output or Evidence:** Location of saved output; do not embed secrets.

**Illustrative example only; not a new observed finding:**

| Baseline Item | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
| 34 | git status --porcelain=v1 --untracked-files=all | <checkout> | Git 2.47.0 | Repository | 0 | Passed | <saved console output> |

### 56. Findings and Gaps

Record each unresolved issue, source limitation, missing verification or cross-environment difference on its own row. Link its evidence and state one next check, rather than contaminating a simple value field with commentary.

**How to populate each column (left to right):**

- **Finding:** One concrete finding or unverified question.
- **Impact:** What risk or decision it affects.
- **Evidence:** Proof or precise gap source.
- **Next Check:** Next verification action.

### 57. Discovery Item Status

For each numbered baseline item, record whether it is `Complete`, `Partial`, `Blocked` or `Not checked`. Point to evidence or the exact missing information. This is a tracking table, **not a second execution-phase numbering system**.

**How to populate each column (left to right):**

- **Baseline Item:** Baseline item number, for example 18 or 48.
- **Status:** Complete, Partial, Blocked or Not checked.
- **Evidence or Missing Information:** Source supporting status or missing evidence.

### 58. Overall Baseline Disposition

Set one overall state such as `Complete`, `Complete with gaps` or `More verification needed` based on what has and has not actually been checked. Do not claim completion while required Windows preflight and checkout verification are outstanding.

### 59. Reviewed By

Record the reviewer who actually checked the baseline, or `Not reviewed`. This is not automatically the same person as the discovery operator.

### 60. Review Date

Record the actual baseline **review date** (`YYYY-MM-DD`), or `Not reviewed`. This is a governance date; it does not require evidence dates on every row.

### 61. Next Action

Name one concrete next action, for example `Run Windows preflight and verify source checkout`. Avoid a generic instruction such as `Continue`.

### 62. Deferred Checks

Document intentionally omitted checks with reason and trigger for revisit, one row per check. For example: `Local Release build | Windows host not inventoried | After DISC host/checkout checks`; use baseline item numbers instead of outdated DISC phase identifiers.

**How to populate each column (left to right):**

- **Check:** Specific check deferred.
- **Reason Deferred:** Why it was not performed.
- **Revisit When:** When and under what prerequisite to retry it.

## Completion and validation

1. Confirm every baseline number 1–62 has either an observed value, applicable dataset rows, or a documented `Not checked`/`Not executed`/`Not applicable` disposition.
2. Verify the source revision, host, configuration, and provenance of every build/test/compatibility claim. A CI result must not be relabeled as a local run.
3. Keep raw tool output and relevant CI links in the evidence manifest without copying secrets; don't add evidence dates to every entry.
4. Review the recorded gaps and deferred checks. Leave modernization recommendations outside this factual baseline.

The [RecordSift baseline](../projects/recordsift/evaluations/2026-11-technical-baseline/baseline.md) is a worked, partially populated example. Its checked source and existing CI records must be distinguished from operator-run Windows commands still outstanding.
