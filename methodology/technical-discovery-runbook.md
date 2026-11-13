# .NET Technical Discovery — Step-by-Step Guide

Follow these steps in order to document an existing .NET application.

Don't change the application or publish anything as part of discovery.

## DISC-001 — Check prerequisites, acquire clean source and identify the exact revision

**Purpose:** verify the **application's required host platform** and tooling before starting, then acquire the exact source revision in a predictable local folder. A **fresh, timestamped checkout** is preferred for a repeatable case study. Reusing an existing checkout is permitted when its state is inspected and documented. This is **step one**, not an assumption that Git, .NET, MSBuild or NuGet are already installed.

**Platform rule:** this runbook applies to different .NET project types, but **each application evaluation must declare its supported OS and use an appropriate host from DISC-001 onward**. A Windows-only application such as RecordSift must be discovered and verified on Windows, even though some Git and source-inspection commands could technically run elsewhere. Do not substitute Linux, macOS or WSL for Windows without a separately authorized and clearly classified compatibility investigation. Other projects may specify different hosts.

### A. Preflight — confirm the tools before cloning

Run these commands **individually** in PowerShell, beginning with the operating-system check:

```powershell
[System.Runtime.InteropServices.RuntimeInformation]::OSDescription
[System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture
$PSVersionTable.PSVersion
Get-Command git -ErrorAction SilentlyContinue
git --version
Get-Command dotnet -ErrorAction SilentlyContinue
Get-Command msbuild -ErrorAction SilentlyContinue
Get-Command nuget -ErrorAction SilentlyContinue
```

**Before cloning, compare the reported host OS with the application's declared platform requirement.** Stop and select an approved host if they are incompatible. For Windows-specific applications, record the Windows version/build and architecture from a Windows-native query such as `Get-CimInstance Win32_OperatingSystem`. Do not present WSL as Windows application verification. `Get-Command` only reports what is on **PATH**; a missing result does not establish the software is absent from the computer. If Git is not available, stop before cloning. Record the PowerShell and Git versions and the found/not-on-PATH state of the other commands. Do **not** invoke unavailable commands or install anything automatically.

**Distinguish requirements by phase and project, not just by tool name:**

| Tool/prerequisite | When it is needed | Applicability and notes |
|---|---|---|
| PowerShell and **Git** | **Required for this PowerShell/Git acquisition procedure** | Git 2.23+ for `git switch`; Git source operations are independent of .NET version and project format |
| Network access and writable folder | Fresh clone | Clone downloads Git objects and creates a new directory; existing checkout/offline source requires a different documented path |
| .NET SDK / `dotnet` | Later **only for applicable** SDK CLI inspection, MSBuild evaluation or builds | Not universally required by all traditional .NET Framework projects; installed SDK ≠ .NET Framework targeting pack |
| MSBuild / Visual Studio Build Tools | Later for applicable MSBuild project evaluation and builds | Actual implementation and components depend on project format, target, OS and build process; `msbuild` may exist only in a Developer PowerShell |
| Standalone NuGet CLI | Later when the application's documented restore uses `nuget.exe`, including some `packages.config` repositories | Not universally required for SDK-style `PackageReference` projects |
| Targeting packs, test runners and other platform prerequisites | Later before an approved build/test | Framework, project and host-specific; verify at DISC-004 and before DISC-008–010, not inferred from a tool being on PATH |

Use the required platform from the beginning, **not only when running builds and tests**. **The preflight is an availability screen, not the complete environment inventory**: DISC-004 captures exact SDK/runtime/targeting-pack/MSBuild/NuGet versions and origins. Missing later tools become named readiness gaps, not fabricated successes or automatic installation tasks.

### B. Create a dated, likely unique discovery checkout

**Preferred:** create a new folder named `<Repository>-discovery-YYYY-MM-DD-HHmmss` using the **operator's local timestamp**. The date and time make concurrent evaluations distinguishable; the collision check protects an existing directory. Use a standard parent folder under the user's home directory, or record an approved alternative.

Below, substitute the real repository name and remote URL. These commands are ordinary PowerShell and native Git operations, **not a collector script**. Execute them one at a time after the preflight.

```powershell
$repository = 'REPOSITORY'
$remoteUrl = 'https://github.com/OWNER/REPOSITORY.git'
$discoveryRoot = Join-Path (Join-Path $HOME 'source') 'discoveries'
New-Item -ItemType Directory -Path $discoveryRoot -Force
$discoveryFolder = "$repository-discovery-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
$destination = Join-Path $discoveryRoot $discoveryFolder
Test-Path -LiteralPath $destination
```

**Continue only when `Test-Path` returns `False`.** If it returns `True`, create a different timestamped name and check again. Do not delete or reuse a folder merely to force a clean checkout. The parent-directory creation can write new directories; it does not delete existing source.

Clone without automatically checking out a potentially moving default branch, then select the **full, known baseline commit SHA**:

```powershell
git clone --no-checkout $remoteUrl $destination
Set-Location -LiteralPath $destination
git switch --detach FULL_COMMIT_SHA
```

Run the clone and checkout individually and stop on any error. The detached HEAD is intentional. The clone downloads source and writes only the new destination; the switch populates tracked files from the pinned commit. Neither modifies the remote repository. Git 2.23+ supports `git switch`. Do not include credentials in recorded URLs.

**Alternative — existing checkout:** navigate to the existing repository, inspect its current HEAD and status first, and record why a fresh clone was not used. Do **not** run `git pull`, `git reset`, `git clean` or branch-switch commands just to make existing files appear clean. A repository that is not in Git needs its own verified immutable source-identification method.

### C. Verify the checkout

From inside the chosen checkout, run individually:

```powershell
git rev-parse --show-toplevel
git rev-parse HEAD
git branch --show-current
git status --porcelain=v1 --untracked-files=all
git remote get-url origin
```

For a fresh, detached checkout we **expect** the selected full SHA, an empty branch name, and empty porcelain status. These remain expectations until the operator supplies actual output. Check separately for submodules or externally sourced build inputs if the application uses them.

**Evidence:** the actual PowerShell/Git preflight, initial availability of later tools, clone method and timestamped folder name, redacted source/remote identity, source revision, checkout status, command failures and side effects. Redact secrets, user paths and private information in the shared evidence while retaining meaningful context.

**Stop/check:** if Git is unavailable, the destination exists, cloning or switching fails, HEAD differs from the recorded SHA, or the new working tree is unexpectedly dirty, preserve the actual output and resolve the mismatch before DISC-002.

**Important limit:** clean tracked source is not a clean build environment. SDKs, MSBuild, targeting packs, NuGet cache, user-level configuration and network feeds are checked later. An untested tool is never reported as "verified" merely because this preflight found a command name.

## DISC-002 — Inventory solutions and projects

**Purpose:** identify every solution and project, not merely the projects reachable from the first solution.

```powershell
git ls-files "*.sln" "*.slnx" "*.slnf" "*.csproj" "*.fsproj" "*.vbproj"
dotnet --version
dotnet sln .\RecordSift.sln list
```

The `RecordSift.sln` path above is **illustrative and project-specific**; substitute an actual discovered solution, or omit `dotnet sln` if the repository has none. `dotnet sln ... list` requires a compatible .NET SDK; if unavailable, inspect the solution file directly. Capture standalone projects, multi-solution overlaps, solution filters, project roles and project references. A solution filter is a subset view, not a new project graph.

**Applicability:** Git listing is generic; `dotnet sln` applies only where an SDK supports the solution format. **Evidence:** tracked paths are source-inspected; CLI solution listing is tool-interpreted, not a build.

## DISC-003 — Identify project formats and declared targets

Inspect a representative project file and each materially different project. Record `<Project Sdk=...>` / imported SDK indicators, traditional imports, `TargetFramework`, `TargetFrameworks`, `TargetFrameworkVersion`, project role, language, output type, configurations, project references and conditional declarations.

**Applicability:** SDK-style and traditional projects can both target .NET Framework; target framework alone does not identify project format. Multi-targeting and conditional values must be scoped per project/target/configuration.

**Evidence:** file path and relevant source lines at the frozen SHA. Do not infer evaluated defaults from omitted XML declarations.

## DISC-004 — Check toolchain availability and versions

Run the commands supported **on the actual host**, recording "not installed" rather than forcing substitutions:

```powershell
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
msbuild -version -nologo
nuget help
```

`msbuild` requires a suitable MSBuild installation on PATH, often a Visual Studio Developer PowerShell on Windows; `nuget` requires a standalone NuGet CLI. Their absence is not evidence that the application cannot build. `dotnet --info` does **not** establish that .NET Framework targeting packs or Visual Studio Build Tools are installed.

**Capture:** OS/architecture, SDK/runtime list, actual MSBuild implementation/version, NuGet CLI version, Visual Studio/Build Tools and .NET Framework targeting-pack prerequisites where applicable. Record tools as preinstalled versus explicitly supplied. Avoid dumping all environment variables.

## DISC-005 — Inspect imported and evaluated build settings

First inspect declared project and repository configuration, including `Directory.Build.props`, `Directory.Build.targets`, imported `.props`/`.targets`, `global.json`, conditional settings, compiler properties and custom targets.

For MSBuild **17.8+**, on a compatible project and host, try property queries *without building*:

```powershell
msbuild .\path\to\project.csproj -getProperty:TargetFramework -getProperty:TargetFrameworkVersion -p:Configuration=Release
```

The path is a placeholder, not a RecordSift command. On some supported toolchains, `dotnet msbuild` can perform the same property query; **do not assume** it can evaluate every traditional project. Record command, MSBuild version, configuration/platform, framework and environment. For multi-targeting, repeat under explicitly selected target frameworks and configurations when applicable.

**Capture separately:** source declarations, evaluated output, and any conflicts. MSBuild evaluation may differ from values after target execution; **no successful build is established**. If `-getProperty` is unsupported, record "not evaluated" and retain source inspection without installing or upgrading tools solely to fill a row.

## DISC-006 — Inventory central configuration

Use `git ls-files` or direct source inspection to locate relevant `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `nuget.config`/`NuGet.Config`, `.editorconfig`, `.globalconfig`, local tool manifests, response files and project-specific imports.

For each relevant mechanism, record its location, applicability, declared settings and (where verified) actual import/precedence. Configuration can be nested or supplied by a user, machine, SDK, environment or command line. **A missing file is an observation, not a recommendation to add it.**

## DISC-007 — Inventory dependencies without restoring

Inspect `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, central package versions, NuGet source configuration, native/COM/local DLL dependencies and documented external services.

```powershell
dotnet nuget list source
```

This **lists configured NuGet sources** on hosts with the applicable SDK; it does not prove which feed a restore uses or which packages resolve. Review feed URLs before sharing. The separate NuGet CLI has its own source-inspection commands where installed. Record declaration scope, source location and relevant versions; don't conflate package declarations, restored packages, a produced assembly, and a published package's consumer dependencies.

**Do not restore yet.** Package graphs from existing assets/lock files may be inspected as artifacts, but their existence alone does not prove a current successful restore or locked-mode enforcement.

## DISC-008 — Reproduce dependency restore (approved execution only)

Choose **the application's documented working restore command** and confirm the tool/format match. For example, an application using `packages.config` may require standalone `nuget restore <solution>` and an explicit packages directory; applicable SDK-style/`PackageReference` projects often use `dotnet restore <solution>`. Neither should be substituted automatically for the other.

Record the exact command, feed/configuration scope, package cache and generated-file side effects, tool version, source SHA, outcome, and any produced assets or lock-file behavior. A successful restore verifies **that restore invocation**; graph completeness, feed provenance and locked-mode enforcement require their own supporting evidence.

If the environment is missing packages, credentials or feeds, record "blocked"; do not create new credentials, change package versions, or bypass feed restrictions.

## DISC-009 — Perform build verification (approved execution only)

Find existing documented commands in scripts, workflows or developer instructions **before selecting an invocation**. Identify intended solution/projects, configuration, platform, framework, host/toolchain and any restore prerequisite.

For a compatible SDK-style project, `dotnet build <solution> --configuration Release` is a *candidate*, not a universal command. Traditional Windows projects may require `MSBuild.exe <solution> /t:Build /p:Configuration=Release` with a particular platform, build tools and targeting packs. `Rebuild` removes existing build outputs; do not substitute it without accounting for that side effect.

Record exit code, warnings/errors, products, environment and exact scope. A build of one project or Debug configuration does not verify all solution projects or a Release package.

## DISC-010 — Inventory and execute tests (approved execution only)

Identify every test project/assembly, framework, runner, filtering rules and the established local/CI commands. Use `dotnet test` **only where the project and runner support it**. Other applications may use standalone NUnit, VSTest, or application-specific runners.

Capture tests discovered, executed, passed, failed, skipped, configuration, platform, target framework, complete assembly coverage, runner version, and any result/coverage artifacts. "All tests passed" is unsupported if an expected test assembly was omitted. An execution result does not establish comprehensive functional coverage.

## DISC-011 — Inspect CI/CD, packaging and deployment

Read repository workflow definitions and existing run evidence without triggering new releases or deployments. Identify triggers, runner images, toolchains, source SHAs, restore/build/test commands, retention, artifacts, secrets *names only*, packaging and distribution.

Record definition (source-inspected) separately from completed run logs (historical executed evidence). Review runtime/hosting prerequisites appropriate to libraries, services, desktop or web applications. A package manifest or workflow definition does not prove a released artifact exists.

## DISC-012 — Identify existing compatibility evidence

Find existing checks for public API and assembly identities, resources, XML documentation, serialization contracts, package consumers, native dependencies and other relevant contracts. Link to existing snapshots and scripts.

Record whether each check was merely defined, previously executed for a different revision, or actually run for the selected baseline. Do not rerun or add gates without a justified scope; functional scenarios remain in their established documentation.

## DISC-013 — Reconcile and close evidence gaps

Compare **like scopes only**: the same source SHA, project, target framework, configuration, platform, toolchain and relevant environment. Distinguish failed application behavior, missing environment prerequisites and faulty harness/command setup.

Mark each significant finding with evidence type, provenance and status: verified for stated scope, partially verified, blocked, failed, not executed, not applicable or unresolved. Preserve negative results and exact failure diagnostics. Never copy old test counts into a fresh verification column.

## DISC-014 — Produce and review the baseline

Populate [`templates/application-baseline.md`](../templates/application-baseline.md) with **observed** applicable fields, not speculative examples. Link evidence through the execution log and manifest; avoid duplicating raw logs in the baseline.

Check that a second engineer can identify the exact source, reproduce applicable inspection and verification commands, find outputs, understand gaps and separate **discovery facts** from later modernization decisions. Date/freeze the baseline; a later source SHA requires a separate snapshot or clearly scoped follow-up.

## When should a reusable script be created?

**Not during the initial native-command walkthrough by default.** After manual execution, evaluate whether automation materially reduces repetition, reliably normalizes complex results or improves traceability.

A proposed collector must have:
- A defined **input contract** (repository, solution/project paths, framework, configuration, platform, command/tool versions, output location). No hardcoded RecordSift paths.
- A **supported-applicability matrix**, including SDK-style/traditional, target framework families, operating systems/toolchains; distinguish *tested*, *documented but untested*, *unsupported* and *unknown*. One successful RecordSift run verifies only that tested combination.
- A reviewable **side-effect contract**: read-only wherever practical; explicit approval for restore/build/modified files; no publishing, source changes, credentials, or hidden network activity.
- Raw output preserved with true exit codes and immutable source identifiers; report summaries cite the raw evidence and never hide skipped/failed operations.
- Formatting/reporting separated from command execution where practical. Test both expected output and failure handling, with fixtures from genuinely different environments before claiming portability.

Record the proposed benefit and validation results before adding any script to the reusable tooling tree. A project-specific helper belongs with its project unless or until its broader applicability is demonstrated.

## Documentation ownership

- **Reusable instructions:** `methodology/technical-discovery-runbook.md`.
- **Reusable recording schema:** `templates/discovery-execution-log.md` plus the existing `templates/application-baseline.md`.
- **Application-specific records, results and evidence:** `projects/<app>/evaluations/<dated-scope>/` in this repository. Retain historical evaluations as separate immutable evidence.
- **Application code and existing CI:** the application repository; do not alter them for a read-only discovery.
- **Publication drafts and images:** `infoconex/coding-blog`. The article selectively demonstrates findings and links to the canonical technical records; it is not an authoritative evidence store.
