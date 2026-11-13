# .NET Technical Discovery — Step-by-Step Guide

Copy the blank [baseline template](../templates/application-baseline.md) for the application you are evaluating. Use the steps below to determine each numbered field's value. **Write answers only in the copy, never in this guide or the original template.**

Don't change the application or publish anything as part of discovery.

## DISC-001 — Check tools and get a clean copy of the source

### Record discovery details

1. **Discovery By:** Enter the name of the person performing the discovery (field 1).
2. **Discovery Date:** Enter the date discovery is being performed (`YYYY-MM-DD`) (field 2).

### Check prerequisites

- Run each check separately. Enter its result **only in the numbered field of your copied [baseline](../templates/application-baseline.md)**. Do not write results in this guide.
- Use a computer supported by the application. **RecordSift requires Windows.**

**4–7. Windows — name, version, build, architecture (required for RecordSift)**

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

- If not running Windows, use a Windows computer before continuing.
- Record the OS name (**4**), version (**5**), build (**6**) and architecture (**7**) separately.

**8. PowerShell Version — Windows PowerShell 5.1 or PowerShell 7 required**

```powershell
$PSVersionTable.PSVersion
```

- If unavailable, use Windows PowerShell or [install PowerShell for Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).
- Record the version shown.

**9. Git Version — required; minimum version 2.23**

```powershell
git --version
```

- If missing or older than 2.23, [install Git for Windows](https://git-scm.com/install/win), reopen PowerShell, and run the command again.
- Record the installed version. Git 2.23+ supports `git switch`, which we'll use below.

**10–11. .NET SDK Version and .NET Runtime Version — optional for checkout**

```powershell
dotnet --info
```

- If missing and needed for a later step, [install the appropriate .NET SDK](https://dotnet.microsoft.com/en-us/download).
- Record installed SDK versions (**10**) and runtime versions (**11**) separately. Repeat for each version. An SDK alone doesn't provide .NET Framework targeting packs.

**12–13. MSBuild Version and MSBuild Installation Source — required for applicable builds**

```powershell
msbuild -version -nologo
```

- If not found, first try **Visual Studio Developer PowerShell**. If still unavailable and needed, [install Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the required .NET components.
- Record MSBuild version (**12**) separately from its installation source (**13**). The optional `-getProperty` command in DISC-005 requires MSBuild 17.8+.

**14. NuGet CLI Version — required for some restores, including RecordSift**

```powershell
nuget help
```

- If unavailable and needed for restore, [install the NuGet CLI](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli).
- Record the version shown. No universal minimum version is assumed here.

**15–16. .NET Framework 4.8 Targeting Pack Version and Installed — required for RecordSift build**

```powershell
Test-Path "${env:ProgramFiles(x86)}\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8"
```

- If `False`, check the installed Visual Studio components or [install the .NET Framework 4.8 Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).
- Set **15** to `.NET Framework 4.8` and **16** to the actual `True`/`False` directory result. A directory check doesn't prove the build succeeds.

- **To start cloning:** Windows (for RecordSift), PowerShell, Git, internet access, and a writable folder are required.
- **Before restore, build, or tests:** resolve any other tools the application needs. Don't install optional tools just to complete this checklist.
- **17–18** (test runner) is completed later in DISC-010 if it isn't known now.

### Create a dated discovery folder

**Baseline fields:** **3** (Discovery Folder), **19** (Selected Source Branch or Tag), **29** (HTTPS Clone URL). Complete fields **1** and **2** from the discovery information above.

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

**Fields to fill:** **20** (actual full source SHA), **21** (working-tree clean?), **22** (detached HEAD?), **31** (default branch when known), **160–167** (actual command results when captured).

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
- Fill **25–37** (application and repository details), **43–50** (one row per solution), and **51–52** (project paths and roles).

- **Report fields:** 25–37, 43–50, 51–52. Add the findings directly to the copied baseline.

## DISC-003 — Check project types and target frameworks

- Open each project file (`.csproj`, `.fsproj`, or `.vbproj`).
- Check whether it uses an SDK declaration or traditional MSBuild imports.
- Look for `TargetFramework`, `TargetFrameworks`, or `TargetFrameworkVersion`.
- Note project references, output type, language version, and configuration-specific settings.
- **Save:** each project's path, project type, declared framework(s), and important differences.
- An SDK-style project can still target .NET Framework. Don't guess settings that aren't declared.
- Fill **38–42** (versions and consumers), **53–60** (project details), and **47–51, 52–56, 57–62** (source-declared settings, only where applicable).

- **Report fields:** 38–42, 53–60, 61–68, 69–74, 75–82. Add the findings directly to the copied baseline.

## DISC-004 — Record installed build tools

- Use the results from DISC-001. Check any tool that wasn't fully identified.
- Run each command separately and enter the output in the indicated baseline field.

**.NET SDKs:**

```powershell
dotnet --list-sdks
```

- Record each installed SDK version in field **10**, repeating the value for each SDK; record any error or missing installation.

**.NET runtimes:**

```powershell
dotnet --list-runtimes
```

- Record each runtime version in field **11**, repeating it for each runtime.

**MSBuild:**

```powershell
msbuild -version -nologo
```

- Enter MSBuild version in field **12** and installation source in field **13**. If unavailable in normal PowerShell, try Visual Studio Developer PowerShell.

**NuGet CLI:**

```powershell
nuget help
```

- Enter the NuGet CLI version (or command error) in field **14**.

- Check any remaining framework targeting packs and test runners required by the project. Give each its own command and recorded result when identified.
- **Save:** tool versions, paths, missing prerequisites, and any differences between PowerShell environments.
- The .NET SDK does **not** guarantee a .NET Framework targeting pack is installed.
- Update **10–18** with detailed versions, and **124–126** for any second host such as CI. Don't record a tool as installed unless verified.

- **Report fields:** 10–18, 124–126. Add the findings directly to the copied baseline.

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
- Fill **83–89** with evaluated property values and relevant differences from declared values. Update **47–51, 52–56, 57–62** only when additional evidence changes them.

- **Report fields:** 83–89; 61–68, 69–74, 75–82 if needed. Add the findings directly to the copied baseline.

## DISC-006 — Find shared configuration files

- Look for `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `NuGet.Config` / `nuget.config`, and `.editorconfig`.
- Check nested directories, project imports, and relevant machine/user settings when they affect the build.
- **Save:** file paths, key settings, and which projects they apply to.
- A missing file isn't automatically a problem or a reason to create one.
- Fill **90–91** (folders) and **92–98** (configuration paths, existence, settings, scope). Use one row per folder or file.

- **Report fields:** 90–91, 92–98. Add the findings directly to the copied baseline.

## DISC-007 — List dependencies

- Read `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, and any central package versions.
- Look for local DLLs, native components, COM references, and external services when applicable.
- If the .NET SDK is available, view configured NuGet sources:

```powershell
dotnet nuget list source
```

- **Save:** package names/versions, project references, other dependencies, and configured feeds. Review feed URLs for sensitive details before sharing.
- **Don't restore packages yet.** A listed source or package declaration doesn't prove a package was downloaded.
- Fill **99–104** for each NuGet package and **105–114** for other dependencies. Note packages and feeds not checked.

- **Report fields:** 99–104, 105–114. Add the findings directly to the copied baseline.

## DISC-008 — Restore dependencies

- Find the application's existing restore instructions first.
- Check which tool and dependency format it uses: some `packages.config` projects use `nuget restore`; many `PackageReference` projects use `dotnet restore`.
- **Before running:** confirm the selected command, package sources, credentials if needed, and where files will be written. Restore may update caches or generate files.
- Run the appropriate native command **after the operator has approved the step**.
- **Save:** exact command, tool version, result, errors, and any generated files. Don't change package versions or bypass missing feeds to make the restore pass.
- Fill **115** (restore command), **147** (outcome) and **160–167** (actual command, exit code, evidence).

- **Report fields:** 115, 147, 160–167. Add the findings directly to the copied baseline.

## DISC-009 — Build the application

- Find the existing build instructions or CI commands.
- Confirm the solution/projects, Debug or Release, platform, framework, and required tools.
- Use the matching native build command. For example, SDK-style projects may use `dotnet build`; traditional Windows projects may use `MSBuild.exe`.
- **Before running:** confirm the command and its side effects. A `Rebuild` can remove previous build outputs.
- **Save:** command, configuration, success/failure, warnings/errors, and output files.
- One successful project build doesn't prove every project or configuration builds.
- Fill **116–118** (build command), **133–135** (outputs/warnings), **148** (outcome) and **160–167** (actual execution).

- **Report fields:** 116–118, 133–135, 148, 160–167. Add the findings directly to the copied baseline.

## DISC-010 — Run the tests

- List every test project and the test runner it uses.
- Find the existing test commands in documentation or CI.
- Use `dotnet test` only when supported; other projects may need NUnit, VSTest, or another runner.
- **Before running:** confirm that the test command and environment are appropriate.
- **Save:** tests found, passed, failed, skipped, runner version, and which test projects actually ran.
- Don't report "all tests passed" if an expected test project wasn't executed.
- Fill **17–18** (runner), **119** (command), **127–132** (test counts and included assemblies), **149** (outcome), and **160–167** (execution).

- **Report fields:** 17–18, 119, 127–132, 149, 160–167. Add the findings directly to the copied baseline.

## DISC-011 — Review CI, packaging, and deployment

- Read the existing GitHub Actions or other CI/CD configuration.
- Note build/test commands, runner OS, SDK/tool versions, artifacts, packaging, and deployment requirements.
- Check existing workflow runs separately from the workflow files. Don't start releases or deployments.
- **Save:** what the pipeline is configured to do and what existing runs actually completed.
- A workflow file alone doesn't prove that it ran successfully.
- Fill **120–126** (existing check/packaging/deployment commands and alternate hosts) and **136–146** (CI, runs, packaging, runtime requirements).

- **Report fields:** 120–126, 136–146. Add the findings directly to the copied baseline.

## DISC-012 — Find existing compatibility checks

- Look for tests or reports covering public APIs, assembly versions, resources, XML documentation, packages, consumers, and application-specific behavior.
- **Save:** the check's location, any existing results, and which source revision those results belong to.
- Mark checks that have not been run against the selected commit.
- Don't create extra checks just to fill out the list.
- Fill applicable **150–159** check outcomes. Each must say passed, failed, not executed, not checked or not applicable; link existing results.

- **Report fields:** 150–159. Add the findings directly to the copied baseline.

## DISC-013 — Review results and missing information

- Go through the discovery notes, command outputs, and failures.
- Check that results match the **same commit, project, configuration, and environment** before comparing them.
- Note whether a problem came from the application, a missing tool, or the command itself.
- **Save:** what's confirmed, what failed, what's still unknown, and what needs another check.
- Keep old test results labeled as historical; don't present them as new runs.
- Fill **168–171** for each gap or problem and **172–176** for per-step status and evidence.

- **Report fields:** 168–171, 172–176. Add the findings directly to the copied baseline.

## DISC-014 — Finish the technical baseline

- Update the application's **discovery report** with the facts that have actually been collected.
- Record actual commands, results and evidence links with their field numbers. Do not copy unanswered questions into the report.
- Check that another engineer can find the same source, understand the setup, and repeat the steps.
- List any missing results instead of guessing.
- Save the final baseline with its source commit and discovery date. Modernization recommendations come afterward.
- Fill **23–24** (verification date/status) and **177–181** (disposition, reviewer, next action). Finish **172–176** for all 14 steps.

- **Report fields:** 23–24, 172–176, 177–181. Add the findings directly to the copied baseline.

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
