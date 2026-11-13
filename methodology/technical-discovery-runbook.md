# .NET Technical Discovery — Step-by-Step Guide

Follow these steps in order to document an existing .NET application.

Don't change the application or publish anything as part of discovery.

## DISC-001 — Check tools and get a clean copy of the source

### 1. Check your computer and tools

- Use a computer that supports the application. **RecordSift requires Windows.**
- Run **one command at a time**. Keep each tool in its own command snippet, with its actual result directly underneath. If a command cannot run, record the error instead of inventing a version.
- These examples use PowerShell on Windows. For another OS, use its native system-information command.

**Windows version** (for Windows applications):

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

- **Record:** Windows edition, version, build, and architecture.

**PowerShell:**

```powershell
$PSVersionTable.PSVersion
```

- **Record:** PowerShell version.

**Git:**

```powershell
git --version
```

- **Record:** Git version. Git 2.23+ is needed for the `git switch` command used below. If Git is unavailable, stop before cloning.

**.NET SDK:**

```powershell
dotnet --info
```

- **Record:** installed SDK/runtime information, or a command-not-found error.

**MSBuild:**

```powershell
msbuild -version -nologo
```

- **Record:** MSBuild version or **not found on PATH**. On Windows it may be available only in a Visual Studio Developer PowerShell.

**Standalone NuGet CLI:**

```powershell
nuget help
```

- **Record:** NuGet CLI version shown in the output, or **not found on PATH**.

**.NET Framework 4.8 targeting pack** (when needed on Windows):

```powershell
Test-Path "\${env:ProgramFiles(x86)}\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8"
```

- **Record:** `True` or `False`. `True` confirms only that the standard directory exists; later build checks establish whether targeting actually works.

- **Needed now:** supported OS, PowerShell, Git, network access, and a writable folder.
- **Needed later:** the build tools, targeting packs, and test runners required by the actual projects. A missing command on PATH does not always mean the tool is uninstalled.
- **Do not install or change tools automatically.** Record what is available first.

### 2. Create a dated discovery folder

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
- **Save:** Windows and tool details, folder name, commit SHA, Git status, and any errors. Remove passwords, tokens, and personal paths before sharing.
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

## DISC-003 — Check project types and target frameworks

- Open each project file (`.csproj`, `.fsproj`, or `.vbproj`).
- Check whether it uses an SDK declaration or traditional MSBuild imports.
- Look for `TargetFramework`, `TargetFrameworks`, or `TargetFrameworkVersion`.
- Note project references, output type, language version, and configuration-specific settings.
- **Save:** each project's path, project type, declared framework(s), and important differences.
- An SDK-style project can still target .NET Framework. Don't guess settings that aren't declared.

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

## DISC-006 — Find shared configuration files

- Look for `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `NuGet.Config` / `nuget.config`, and `.editorconfig`.
- Check nested directories, project imports, and relevant machine/user settings when they affect the build.
- **Save:** file paths, key settings, and which projects they apply to.
- A missing file isn't automatically a problem or a reason to create one.

## DISC-007 — List dependencies

- Read `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, and any central package versions.
- Look for local DLLs, native components, COM references, and external services when applicable.
- If the .NET SDK is available, view configured NuGet sources:

```powershell
dotnet nuget list source
```

- **Save:** package names/versions, project references, other dependencies, and configured feeds. Review feed URLs for sensitive details before sharing.
- **Don't restore packages yet.** A listed source or package declaration doesn't prove a package was downloaded.

## DISC-008 — Restore dependencies

- Find the application's existing restore instructions first.
- Check which tool and dependency format it uses: some `packages.config` projects use `nuget restore`; many `PackageReference` projects use `dotnet restore`.
- **Before running:** confirm the selected command, package sources, credentials if needed, and where files will be written. Restore may update caches or generate files.
- Run the appropriate native command **after the operator has approved the step**.
- **Save:** exact command, tool version, result, errors, and any generated files. Don't change package versions or bypass missing feeds to make the restore pass.

## DISC-009 — Build the application

- Find the existing build instructions or CI commands.
- Confirm the solution/projects, Debug or Release, platform, framework, and required tools.
- Use the matching native build command. For example, SDK-style projects may use `dotnet build`; traditional Windows projects may use `MSBuild.exe`.
- **Before running:** confirm the command and its side effects. A `Rebuild` can remove previous build outputs.
- **Save:** command, configuration, success/failure, warnings/errors, and output files.
- One successful project build doesn't prove every project or configuration builds.

## DISC-010 — Run the tests

- List every test project and the test runner it uses.
- Find the existing test commands in documentation or CI.
- Use `dotnet test` only when supported; other projects may need NUnit, VSTest, or another runner.
- **Before running:** confirm that the test command and environment are appropriate.
- **Save:** tests found, passed, failed, skipped, runner version, and which test projects actually ran.
- Don't report "all tests passed" if an expected test project wasn't executed.

## DISC-011 — Review CI, packaging, and deployment

- Read the existing GitHub Actions or other CI/CD configuration.
- Note build/test commands, runner OS, SDK/tool versions, artifacts, packaging, and deployment requirements.
- Check existing workflow runs separately from the workflow files. Don't start releases or deployments.
- **Save:** what the pipeline is configured to do and what existing runs actually completed.
- A workflow file alone doesn't prove that it ran successfully.

## DISC-012 — Find existing compatibility checks

- Look for tests or reports covering public APIs, assembly versions, resources, XML documentation, packages, consumers, and application-specific behavior.
- **Save:** the check's location, any existing results, and which source revision those results belong to.
- Mark checks that have not been run against the selected commit.
- Don't create extra checks just to fill out the list.

## DISC-013 — Review results and missing information

- Go through the discovery notes, command outputs, and failures.
- Check that results match the **same commit, project, configuration, and environment** before comparing them.
- Note whether a problem came from the application, a missing tool, or the command itself.
- **Save:** what's confirmed, what failed, what's still unknown, and what needs another check.
- Keep old test results labeled as historical; don't present them as new runs.

## DISC-014 — Finish the technical baseline

- Fill in the [application baseline template](../templates/application-baseline.md) using what you actually found.
- Link to the commands and outputs in the [execution log](../templates/discovery-execution-log.md) and your project's evidence files.
- Check that another engineer can find the same source, understand the setup, and repeat the steps.
- List any missing results instead of guessing.
- Save the final baseline with its source commit and discovery date. Modernization recommendations come afterward.

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
- **Reusable templates:** `templates/discovery-execution-log.md` and `templates/application-baseline.md`.
- **Application results:** `projects/<app>/evaluations/<dated-discovery>/` in this repository.
- **Application source and build workflows:** the application's own repository.
- **Blog article:** `infoconex/coding-blog`; use selected results and link back to the complete discovery records.
