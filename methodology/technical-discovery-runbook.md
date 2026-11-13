# .NET Technical Discovery — Step-by-Step Guide

Follow these steps in order to document an existing .NET application.

Don't change the application or publish anything as part of discovery.

## DISC-001 — Check tools and get a clean copy of the source

### Record discovery details

1. **Recorder:** Enter the person performing the discovery.
2. **Recorded Date:** Enter the date discovery is being performed (`YYYY-MM-DD`).

### Check prerequisites

- Run each check separately. Enter its result **only in the numbered field of your copied [baseline](../templates/application-baseline.md)**. Do not write results in this guide.
- Use a computer supported by the application. **RecordSift requires Windows.**

**4. Windows — required for RecordSift; use a supported Windows version**

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

- If not running Windows, use a Windows computer before continuing.
- Record the Windows version, build, and architecture.

**5. PowerShell — required; Windows PowerShell 5.1 or PowerShell 7**

```powershell
$PSVersionTable.PSVersion
```

- If unavailable, use Windows PowerShell or [install PowerShell for Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).
- Record the version shown.

**6. Git — required; minimum version 2.23**

```powershell
git --version
```

- If missing or older than 2.23, [install Git for Windows](https://git-scm.com/install/win), reopen PowerShell, and run the command again.
- Record the installed version. Git 2.23+ supports `git switch`, which we'll use below.

**7. .NET SDK — optional for checkout; version depends on later commands**

```powershell
dotnet --info
```

- If missing and needed for a later step, [install the appropriate .NET SDK](https://dotnet.microsoft.com/en-us/download).
- Record installed SDK and runtime versions. An SDK alone doesn't provide .NET Framework targeting packs.

**8. MSBuild — needed for applicable builds; compatible version depends on the project**

```powershell
msbuild -version -nologo
```

- If not found, first try **Visual Studio Developer PowerShell**. If still unavailable and needed, [install Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the required .NET components.
- Record the installed version. The optional `-getProperty` command in DISC-005 requires MSBuild 17.8+.

**9. Standalone NuGet CLI — needed for some restores, including RecordSift**

```powershell
nuget help
```

- If unavailable and needed for restore, [install the NuGet CLI](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli).
- Record the version shown. No universal minimum version is assumed here.

**10. .NET Framework 4.8 targeting pack — needed to build RecordSift**

```powershell
Test-Path "${env:ProgramFiles(x86)}\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8"
```

- If `False`, check the installed Visual Studio components or [install the .NET Framework 4.8 Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).
- Record `True` or `False`. A directory check doesn't prove that a build will succeed.

- **To start cloning:** Windows (for RecordSift), PowerShell, Git, internet access, and a writable folder are required.
- **Before restore, build, or tests:** resolve any other tools the application needs. Don't install optional tools just to complete this checklist.
- **11** (test runner) is completed later in DISC-010 if it isn't known now.

### Create a dated discovery folder

**Report fields:** **3** (dated folder), **12** (source branch/tag), **20** (HTTPS clone URL). Fields **1** and **2** were collected above.

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

### Confirm the checkout

**Fields to fill:** **13** (actual full source SHA), **14** (checkout status), **22** (default branch when known), **112–115** (actual command results when captured).

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
- Record actual values in the report using their field numbers. Do not share passwords, tokens or private paths.
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
- Fill **17–26** (application and repository details), **31–37** (one row per solution), and **38–39** (project paths and roles).

- **Report fields:** 17–26, 31–37, 38–39. Add the findings directly to the copied baseline.

## DISC-003 — Check project types and target frameworks

- Open each project file (`.csproj`, `.fsproj`, or `.vbproj`).
- Check whether it uses an SDK declaration or traditional MSBuild imports.
- Look for `TargetFramework`, `TargetFrameworks`, or `TargetFrameworkVersion`.
- Note project references, output type, language version, and configuration-specific settings.
- **Save:** each project's path, project type, declared framework(s), and important differences.
- An SDK-style project can still target .NET Framework. Don't guess settings that aren't declared.
- Fill **27–30** (versions and consumers), **40–46** (project details), and **47–51, 52–56, 57–62** (source-declared settings, only where applicable).

- **Report fields:** 27–30, 40–46, 47–51, 52–56, 57–62. Add the findings directly to the copied baseline.

## DISC-004 — Record installed build tools

- Use the results from DISC-001. Check any tool that wasn't fully identified.
- Run each command separately and enter the output in the indicated baseline field.

**.NET SDKs:**

```powershell
dotnet --list-sdks
```

- Enter installed SDK versions and locations (or the error) in field **7**.

**.NET runtimes:**

```powershell
dotnet --list-runtimes
```

- Enter runtime versions and locations (or the error) in field **7**.

**MSBuild:**

```powershell
msbuild -version -nologo
```

- Enter the version and installation source in field **8**. If unavailable in normal PowerShell, try Visual Studio Developer PowerShell.

**NuGet CLI:**

```powershell
nuget help
```

- Enter the version/path (or error) in field **9**.

- Check any remaining framework targeting packs and test runners required by the project. Give each its own command and recorded result when identified.
- **Save:** tool versions, paths, missing prerequisites, and any differences between PowerShell environments.
- The .NET SDK does **not** guarantee a .NET Framework targeting pack is installed.
- Update **7–11** with detailed versions, and **88** for any second host such as CI. Don't record a tool as installed unless verified.

- **Report fields:** 7–11, 88. Add the findings directly to the copied baseline.

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
- Fill **63** with evaluated property values and relevant differences from declared values. Update **47–51, 52–56, 57–62** only when additional evidence changes them.

- **Report fields:** 63; 47–51, 52–56, 57–62 if needed. Add the findings directly to the copied baseline.

## DISC-006 — Find shared configuration files

- Look for `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `NuGet.Config` / `nuget.config`, and `.editorconfig`.
- Check nested directories, project imports, and relevant machine/user settings when they affect the build.
- **Save:** file paths, key settings, and which projects they apply to.
- A missing file isn't automatically a problem or a reason to create one.
- Fill **64–65** (folders) and **66–69** (configuration paths, existence, settings, scope). Use one row per folder or file.

- **Report fields:** 64–65, 66–69. Add the findings directly to the copied baseline.

## DISC-007 — List dependencies

- Read `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, and any central package versions.
- Look for local DLLs, native components, COM references, and external services when applicable.
- If the .NET SDK is available, view configured NuGet sources:

```powershell
dotnet nuget list source
```

- **Save:** package names/versions, project references, other dependencies, and configured feeds. Review feed URLs for sensitive details before sharing.
- **Don't restore packages yet.** A listed source or package declaration doesn't prove a package was downloaded.
- Fill **70–75** for each NuGet package and **76–81** for other dependencies. Note packages and feeds not checked.

- **Report fields:** 70–75, 76–81. Add the findings directly to the copied baseline.

## DISC-008 — Restore dependencies

- Find the application's existing restore instructions first.
- Check which tool and dependency format it uses: some `packages.config` projects use `nuget restore`; many `PackageReference` projects use `dotnet restore`.
- **Before running:** confirm the selected command, package sources, credentials if needed, and where files will be written. Restore may update caches or generate files.
- Run the appropriate native command **after the operator has approved the step**.
- **Save:** exact command, tool version, result, errors, and any generated files. Don't change package versions or bypass missing feeds to make the restore pass.
- Fill **82** (restore command), **99** (outcome) and **112–115** (actual command, exit code, evidence).

- **Report fields:** 82, 99, 112–115. Add the findings directly to the copied baseline.

## DISC-009 — Build the application

- Find the existing build instructions or CI commands.
- Confirm the solution/projects, Debug or Release, platform, framework, and required tools.
- Use the matching native build command. For example, SDK-style projects may use `dotnet build`; traditional Windows projects may use `MSBuild.exe`.
- **Before running:** confirm the command and its side effects. A `Rebuild` can remove previous build outputs.
- **Save:** command, configuration, success/failure, warnings/errors, and output files.
- One successful project build doesn't prove every project or configuration builds.
- Fill **83** (build command), **94** (outputs/warnings), **100** (outcome) and **112–115** (actual execution).

- **Report fields:** 83, 94, 100, 112–115. Add the findings directly to the copied baseline.

## DISC-010 — Run the tests

- List every test project and the test runner it uses.
- Find the existing test commands in documentation or CI.
- Use `dotnet test` only when supported; other projects may need NUnit, VSTest, or another runner.
- **Before running:** confirm that the test command and environment are appropriate.
- **Save:** tests found, passed, failed, skipped, runner version, and which test projects actually ran.
- Don't report "all tests passed" if an expected test project wasn't executed.
- Fill **11** (runner), **84** (command), **89–93** (test counts and included assemblies), **101** (outcome), and **112–115** (execution).

- **Report fields:** 11, 84, 89–93, 101, 112–115. Add the findings directly to the copied baseline.

## DISC-011 — Review CI, packaging, and deployment

- Read the existing GitHub Actions or other CI/CD configuration.
- Note build/test commands, runner OS, SDK/tool versions, artifacts, packaging, and deployment requirements.
- Check existing workflow runs separately from the workflow files. Don't start releases or deployments.
- **Save:** what the pipeline is configured to do and what existing runs actually completed.
- A workflow file alone doesn't prove that it ran successfully.
- Fill **85–88** (existing check/packaging/deployment commands and alternate hosts) and **95–98** (CI, runs, packaging, runtime requirements).

- **Report fields:** 85–88, 95–98. Add the findings directly to the copied baseline.

## DISC-012 — Find existing compatibility checks

- Look for tests or reports covering public APIs, assembly versions, resources, XML documentation, packages, consumers, and application-specific behavior.
- **Save:** the check's location, any existing results, and which source revision those results belong to.
- Mark checks that have not been run against the selected commit.
- Don't create extra checks just to fill out the list.
- Fill applicable **102–111** check outcomes. Each must say passed, failed, not executed, not checked or not applicable; link existing results.

- **Report fields:** 102–111. Add the findings directly to the copied baseline.

## DISC-013 — Review results and missing information

- Go through the discovery notes, command outputs, and failures.
- Check that results match the **same commit, project, configuration, and environment** before comparing them.
- Note whether a problem came from the application, a missing tool, or the command itself.
- **Save:** what's confirmed, what failed, what's still unknown, and what needs another check.
- Keep old test results labeled as historical; don't present them as new runs.
- Fill **116–118** for each gap or problem and **119–121** for per-step status and evidence.

- **Report fields:** 116–118, 119–121. Add the findings directly to the copied baseline.

## DISC-014 — Finish the technical baseline

- Update the application's **discovery report** with the facts that have actually been collected.
- Record actual commands, results and evidence links with their field numbers. Do not copy unanswered questions into the report.
- Check that another engineer can find the same source, understand the setup, and repeat the steps.
- List any missing results instead of guessing.
- Save the final baseline with its source commit and discovery date. Modernization recommendations come afterward.
- Fill **15–16** (verification date/status) and **122–124** (disposition, reviewer, next action). Finish **119–121** for all 14 steps.

- **Report fields:** 15–16, 119–121, 122–124. Add the findings directly to the copied baseline.

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
- **Blank baseline template:** [templates/application-baseline.md](../templates/application-baseline.md). Copy this for each discovery and fill the copy, not the template.
- **Completed baseline and supporting evidence:** `projects/<app>/evaluations/<dated-discovery>/` in this repository.
- **Application source and build workflows:** the application's own repository.
- **Blog article:** `infoconex/coding-blog`; use selected results and link back to the complete discovery records.
