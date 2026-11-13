# .NET Technical Discovery — Step-by-Step Guide

Follow these steps in order to document an existing .NET application.

Don't change the application or publish anything as part of discovery.

## DISC-001 — Check tools and get a clean copy of the source

### 1. Check required tools

- Run each check separately. The **F-number** on its Result line is the matching field in the [discovery form](../templates/application-baseline.md). Write the result here and share it so I can update the report.
- Use a computer supported by the application. **RecordSift requires Windows.**

**Windows — required for RecordSift; use a supported Windows version**

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

**F-004 — Result:** ____________________

- If not running Windows, use a Windows computer before continuing.
- Record the Windows version, build, and architecture.

**PowerShell — required; Windows PowerShell 5.1 or PowerShell 7**

```powershell
$PSVersionTable.PSVersion
```

**F-005 — Result:** ____________________

- If unavailable, use Windows PowerShell or [install PowerShell for Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).
- Record the version shown.

**Git — required; minimum version 2.23**

```powershell
git --version
```

**F-006 — Result:** ____________________

- If missing or older than 2.23, [install Git for Windows](https://git-scm.com/install/win), reopen PowerShell, and run the command again.
- Record the installed version. Git 2.23+ supports `git switch`, which we'll use below.

**.NET SDK — optional for checkout; version depends on later commands**

```powershell
dotnet --info
```

**F-007 — Result:** ____________________

- If missing and needed for a later step, [install the appropriate .NET SDK](https://dotnet.microsoft.com/en-us/download).
- Record installed SDK and runtime versions. An SDK alone doesn't provide .NET Framework targeting packs.

**MSBuild — needed for applicable builds; compatible version depends on the project**

```powershell
msbuild -version -nologo
```

**F-008 — Result:** ____________________

- If not found, first try **Visual Studio Developer PowerShell**. If still unavailable and needed, [install Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the required .NET components.
- Record the installed version. The optional `-getProperty` command in DISC-005 requires MSBuild 17.8+.

**Standalone NuGet CLI — needed for some restores, including RecordSift**

```powershell
nuget help
```

**F-009 — Result:** ____________________

- If unavailable and needed for restore, [install the NuGet CLI](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli).
- Record the version shown. No universal minimum version is assumed here.

**.NET Framework 4.8 targeting pack — needed to build RecordSift**

```powershell
Test-Path "${env:ProgramFiles(x86)}\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8"
```

**F-010 — Result:** ____________________

- If `False`, check the installed Visual Studio components or [install the .NET Framework 4.8 Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).
- Record `True` or `False`. A directory check doesn't prove that a build will succeed.

- **To start cloning:** Windows (for RecordSift), PowerShell, Git, internet access, and a writable folder are required.
- **Before restore, build, or tests:** resolve any other tools the application needs. Don't install optional tools just to complete this checklist.
- **F-011** (test runner) is completed later in DISC-010 if it isn't known now.

### 2. Create a dated discovery folder

**Fields to fill:** **F-001** (operator), **F-002** (date/time), **F-003** (dated folder), **F-012** (selected branch/tag), **F-104** (HTTPS clone URL).

- Use a **new folder** for each discovery run. The name includes the repository, `discovery`, and a local date/time stamp.
- Replace `REPOSITORY` and the example URL with the real application details.
- Run these PowerShell commands one at a time:

```powershell
$repository = 'REPOSITORY'
$remoteUrl = 'https://github.com/OWNER/REPOSITORY.git'
$discoveryRoot = Join-Path (Join-Path $HOME 'source') 'discoveries'
New-Item -ItemType Directory -Path $discoveryRoot -Force
$discoveryFolder = "$($repository)-discovery-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
$destination = Join-Path $discoveryRoot $discoveryFolder
Test-Path -LiteralPath $destination
```

- **Continue only if `Test-Path` returns `False`.** If the folder exists, choose a new timestamp. Never delete an existing checkout to make room.
- Clone the repository and select the **exact commit** chosen for discovery, not a moving branch:

```powershell
git clone --no-checkout $remoteUrl $destination
Set-Location -LiteralPath $destination
git switch --detach FULL_COMMIT_SHA
```

- Run each command separately. Stop if the clone or checkout fails.
- The download creates a new local repository and the checkout creates its source files. Neither changes the remote repository.
- If you're using an existing checkout instead, inspect it before changing branches. Don't reset or clean it.

### 3. Confirm the checkout

**Fields to fill:** **F-013** (actual full source SHA), **F-014** (checkout status), **F-106** (default branch when known), **F-731–F-734** (actual command results when captured).

Run these from inside the repository:

```powershell
git rev-parse --show-toplevel
git rev-parse HEAD
git branch --show-current
git status --porcelain=v1 --untracked-files=all
git remote get-url origin
```

- Check that `HEAD` matches the intended full commit SHA.
- A blank branch name is normal for a detached checkout.
- A blank status means no tracked changes or untracked files were reported. It doesn't check ignored build outputs.
- Record the actual output for **F-001–F-014** as applicable. Do not share passwords, tokens or private paths.
- If the commit differs or files are unexpectedly changed, stop and investigate.
- A clean checkout doesn't mean the computer's SDKs, NuGet cache, or build tools are clean; we'll check those later.

## DISC-002 — List solutions and projects

- From the repository root, list the tracked solution and project files:

```powershell
git ls-files "*.sln" "*.slnx" "*.slnf" "*.csproj" "*.fsproj" "*.vbproj"
```

- For each solution, use the .NET SDK **if available and compatible**:

```powershell
dotnet sln .\path\to\solution.sln list
```

- Replace the example path with a real solution path. If the SDK can't read the solution, open the solution file instead.
- **Save:** solutions, projects inside each solution, and projects outside any solution. Note project roles such as application, library, or tests.
- A solution filter may list only part of the solution; don't treat it as a complete inventory.
- Fill **F-101–F-110** (application and repository details), **F-201–F-207** (one row per solution), and **F-211–F-212** (project paths and roles).

**Fields F-101–F-110, F-201–F-207, F-211–F-212 — Result:** ____________________

## DISC-003 — Check project types and target frameworks

- Open each project file (`.csproj`, `.fsproj`, or `.vbproj`).
- Check whether it uses an SDK declaration or traditional MSBuild imports.
- Look for `TargetFramework`, `TargetFrameworks`, or `TargetFrameworkVersion`.
- Note project references, output type, language version, and configuration-specific settings.
- **Save:** each project's path, project type, declared framework(s), and important differences.
- An SDK-style project can still target .NET Framework. Don't guess settings that aren't declared.
- Fill **F-111–F-114** (versions and consumers), **F-213–F-219** (project details), and **F-301–F-326** (source-declared settings, only where applicable).

**Fields F-111–F-114, F-213–F-219, F-301–F-326 — Result:** ____________________

## DISC-004 — Record installed build tools

- Use the results from DISC-001. Check any tool that wasn't fully identified.
- Run each command separately and write its result directly below it.

**.NET SDKs:**

```powershell
dotnet --list-sdks
```

- **Record:** SDK versions and locations, or the error.

**.NET runtimes:**

```powershell
dotnet --list-runtimes
```

- **Record:** runtime versions and locations, or the error.

**MSBuild:**

```powershell
msbuild -version -nologo
```

- **Record:** version and which installation supplied it. If unavailable in normal PowerShell, try a Visual Studio Developer PowerShell and note the difference.

**NuGet CLI:**

```powershell
nuget help
```

- **Record:** version and path, or the error.

- Check any remaining framework targeting packs and test runners required by the project. Give each its own command and recorded result when identified.
- **Save:** tool versions, paths, missing prerequisites, and any differences between PowerShell environments.
- The .NET SDK does **not** guarantee a .NET Framework targeting pack is installed.
- Update **F-007–F-011** with detailed versions, and **F-617** for any second host such as CI. Don't record a tool as installed unless verified.

**Fields F-007–F-011, F-617 — Result:** ____________________

## DISC-005 — Check MSBuild settings

- Read the project files and their imported `.props` and `.targets` files.
- Look for shared settings, conditions, compiler options, and imports.
- With **MSBuild 17.8 or later**, try this on a compatible project:

```powershell
msbuild .\path\to\project.csproj -getProperty:TargetFramework -getProperty:TargetFrameworkVersion -p:Configuration=Release
```

- Replace the path and configuration. Repeat where projects or configurations differ.
- **Save:** settings found in files and settings returned by MSBuild. They may differ.
- This command checks property values; it **doesn't build the project**. If your MSBuild version doesn't support it, record that and continue with file inspection.
- Fill **F-327** with evaluated property values and relevant differences from declared values. Update **F-301–F-326** only when additional evidence changes them.

**Fields F-327; F-301–F-326 if needed — Result:** ____________________

## DISC-006 — Find shared configuration files

- Look for `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `NuGet.Config` / `nuget.config`, and `.editorconfig`.
- Check nested directories, project imports, and relevant machine/user settings when they affect the build.
- **Save:** file paths, key settings, and which projects they apply to.
- A missing file isn't automatically a problem or a reason to create one.
- Fill **F-401–F-402** (folders) and **F-411–F-414** (configuration paths, existence, settings, scope). Use one row per folder or file.

**Fields F-401–F-402, F-411–F-414 — Result:** ____________________

## DISC-007 — List dependencies

- Read `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, and any central package versions.
- Look for local DLLs, native components, COM references, and external services when applicable.
- If the .NET SDK is available, view configured NuGet sources:

```powershell
dotnet nuget list source
```

- **Save:** package names/versions, project references, other dependencies, and configured feeds. Review feed URLs for sensitive details before sharing.
- **Don't restore packages yet.** A listed source or package declaration doesn't prove a package was downloaded.
- Fill **F-501–F-506** for each NuGet package and **F-511–F-516** for other dependencies. Note packages and feeds not checked.

**Fields F-501–F-506, F-511–F-516 — Result:** ____________________

## DISC-008 — Restore dependencies

- Find the application's existing restore instructions first.
- Check which tool and dependency format it uses: some `packages.config` projects use `nuget restore`; many `PackageReference` projects use `dotnet restore`.
- **Before running:** confirm the selected command, package sources, credentials if needed, and where files will be written. Restore may update caches or generate files.
- Run the appropriate native command **after the operator has approved the step**.
- **Save:** exact command, tool version, result, errors, and any generated files. Don't change package versions or bypass missing feeds to make the restore pass.
- Fill **F-611** (restore command), **F-701** (outcome) and **F-731–F-734** (actual command, exit code, evidence).

**Fields F-611, F-701, F-731–F-734 — Result:** ____________________

## DISC-009 — Build the application

- Find the existing build instructions or CI commands.
- Confirm the solution/projects, Debug or Release, platform, framework, and required tools.
- Use the matching native build command. For example, SDK-style projects may use `dotnet build`; traditional Windows projects may use `MSBuild.exe`.
- **Before running:** confirm the command and its side effects. A `Rebuild` can remove previous build outputs.
- **Save:** command, configuration, success/failure, warnings/errors, and output files.
- One successful project build doesn't prove every project or configuration builds.
- Fill **F-612** (build command), **F-626** (outputs/warnings), **F-702** (outcome) and **F-731–F-734** (actual execution).

**Fields F-612, F-626, F-702, F-731–F-734 — Result:** ____________________

## DISC-010 — Run the tests

- List every test project and the test runner it uses.
- Find the existing test commands in documentation or CI.
- Use `dotnet test` only when supported; other projects may need NUnit, VSTest, or another runner.
- **Before running:** confirm that the test command and environment are appropriate.
- **Save:** tests found, passed, failed, skipped, runner version, and which test projects actually ran.
- Don't report "all tests passed" if an expected test project wasn't executed.
- Fill **F-011** (runner), **F-613** (command), **F-621–F-625** (test counts and included assemblies), **F-703** (outcome), and **F-731–F-734** (execution).

**Fields F-011, F-613, F-621–F-625, F-703, F-731–F-734 — Result:** ____________________

## DISC-011 — Review CI, packaging, and deployment

- Read the existing GitHub Actions or other CI/CD configuration.
- Note build/test commands, runner OS, SDK/tool versions, artifacts, packaging, and deployment requirements.
- Check existing workflow runs separately from the workflow files. Don't start releases or deployments.
- **Save:** what the pipeline is configured to do and what existing runs actually completed.
- A workflow file alone doesn't prove that it ran successfully.
- Fill **F-614–F-617** (existing check/packaging/deployment commands and alternate hosts) and **F-627–F-630** (CI, runs, packaging, runtime requirements).

**Fields F-614–F-617, F-627–F-630 — Result:** ____________________

## DISC-012 — Find existing compatibility checks

- Look for tests or reports covering public APIs, assembly versions, resources, XML documentation, packages, consumers, and application-specific behavior.
- **Save:** the check's location, any existing results, and which source revision those results belong to.
- Mark checks that have not been run against the selected commit.
- Don't create extra checks just to fill out the list.
- Fill applicable **F-704–F-713** check outcomes. Each must say passed, failed, not executed, not checked or not applicable; link existing results.

**Fields F-704–F-713 — Result:** ____________________

## DISC-013 — Review results and missing information

- Go through the discovery notes, command outputs, and failures.
- Check that results match the **same commit, project, configuration, and environment** before comparing them.
- Note whether a problem came from the application, a missing tool, or the command itself.
- **Save:** what's confirmed, what failed, what's still unknown, and what needs another check.
- Keep old test results labeled as historical; don't present them as new runs.
- Fill **F-801–F-803** for each gap or problem and **F-901–F-903** for per-step status and evidence.

**Fields F-801–F-803, F-901–F-903 — Result:** ____________________

## DISC-014 — Finish the technical baseline

- Fill in the [application baseline template](../templates/application-baseline.md) using what you actually found.
- Add the actual commands, results and evidence links to the [discovery report](../templates/application-baseline.md).
- Check that another engineer can find the same source, understand the setup, and repeat the steps.
- List any missing results instead of guessing.
- Save the final baseline with its source commit and discovery date. Modernization recommendations come afterward.
- Fill **F-015–F-016** (verification date/status) and **F-911–F-913** (disposition, reviewer, next action). Finish **F-901–F-903** for all 14 steps.

**Fields F-015–F-016, F-901–F-903, F-911–F-913 — Result:** ____________________

## Optional — Create scripts later

- **Start with manual native commands.** Add a script only when it makes repeated work or reporting easier.
- Make repository paths, projects, frameworks, configurations, and output locations configurable.
- State **where it works**: SDK-style or traditional projects, .NET Framework or modern .NET, Windows or other supported hosts.
- Separate combinations **you've tested** from those you haven't.
- Keep original command outputs and errors; don't let a summary hide failures.
- Make file changes and other side effects clear. Don't publish or modify application source as part of discovery.
- Keep RecordSift-only helpers in the project area unless they've been tested for broader reuse.

## Where to keep the results

- **Instructions:** `methodology/technical-discovery-runbook.md`.
- **Full report template:** `templates/application-baseline.md`.
- **Completed application report and supporting evidence:** `projects/<app>/evaluations/<dated-discovery>/` in this repository.
- **Application source and build workflows:** the application's own repository.
- **Blog article:** `infoconex/coding-blog`; use selected results and link back to the complete discovery records.
