# .NET Technical Discovery — Step-by-Step Guide

Follow this guide alongside the [blank baseline template](../templates/application-baseline.md). All **60 discovery items** are numbered in ascending order (1–60) throughout the baseline, template and runbook. Discovery information comes first, then application information and the remaining verification steps; no separate phase numbering is required. Record results in the application's copied baseline, not here.

**Before recording item 1:** Replace `<Application Name>` in the copied baseline title with the actual application name. Immediately below it, replace `<Application description>` with a factual description of what the application does, its users/consumers, and core responsibilities; verify against the README, documentation and source. For RecordSift, the copy already has its name and description.

**Recording rules:** A single-value field contains only one value (for example `Library`, `Public`, `MIT`, a precise version, `True`, a path, or a URL). Keep citations, assumptions, and explanations in the evidence manifest or a specifically designated table evidence column. For a numbered table, the number identifies **the entire dataset**, never its columns or rows. Prefer one row per project for project-scoped inventories, with unique linked project names first; item 40 records the canonical project path once, and later project tables reference it without repeating path columns; group multiple references, packages or properties without losing their distinct values. Keep separate rows when different scopes or evidence cannot be combined accurately. Mark unavailable checks `Not checked`, `Not executed` or `Not applicable` accurately.

**Environment boundary:** RecordSift itself is Windows-only. Perform its operator-run host, restore, build and test checks on **Windows**, not on Linux, macOS or WSL. Existing GitHub Actions results are separate from local operator execution. Start with native Git, PowerShell, .NET SDK, NuGet and MSBuild commands; use custom scripts only after their necessity and portability are understood. Do not reset worktrees, modify source, publish packages or deploy as part of discovery. Confirm explicit approval before restore/build/test operations.

## Discovery information

### 1. Discovery By

Record the actual discovery operator. Never infer identity from the repository owner or commit author. Use `Not recorded` until supplied.

### 2. Discovery Date

Record the discovery start date (`YYYY-MM-DD`). Do not confuse it with a commit date, release date, CI run or discovery completion date.

### 3. Discovery Status

Use `Not started`, `In progress`, `Blocked`, `Completed`, or `Completed with gaps`, based on actual work. RecordSift remains `In progress` while required operator Windows verification is outstanding. A completed CI run is not an operator-local check.

### 4. Discovery Completed Date

Use `YYYY-MM-DD` only when discovery is actually completed. For `Completed with gaps`, document every unresolved or deferred check and its explicitly accepted limitation in items 59–60; record acceptance evidence in the evidence manifest where available. Otherwise use `Not completed`.

**Consistency:** `Completed` means all required applicable discovery checks are verified and no material gaps remain unresolved. `Completed with gaps` means required verification has been performed to the agreed scope and remaining gaps have been documented and explicitly accepted; do not infer acceptance from silence. If required work is still pending without accepted deferral, keep item 3 as `In progress` or `Blocked` and item 4 as `Not completed`. Do not require a separate disposition, reviewer or review-date field.

## Application information

### 5. Application Type

Inspect the README, project file and architecture documentation. Classify the application with **one concise value** such as `Library`, `Console application`, `Desktop application`, `Service` or `Web application`. For RecordSift, the type is `Library`. Put implementation details in the description below the title, not this field.

### 6. Repository Visibility

Inspect repository visibility in the hosting service. Record `Public` or `Private`. A locally available clone does not prove a repository is public.

### 7. License

Read the repository's actual `LICENSE` and any package licensing metadata. Record an SPDX identifier such as `MIT` where appropriate. Keep the source link in the evidence manifest.

### 8. Supported Operating Systems

Read the supported-platform statement in README and release/consumer guidance, not the operating system of the discovery machine. Record one supported OS per repeat entry or a concise list. For RecordSift record `Windows`; its .NET Framework target belongs in the project inventory.

### 9. HTTPS Clone URL

Use the hosting service's **Clone → HTTPS** address. Record the exact URL, such as `https://github.com/infoconex/RecordSift.git`, without a citation suffix. Do not run a clone merely to collect this address.

### 10. SSH Clone URL

Use the hosting service's **Clone → SSH** address. This is metadata, **not** an SSH authentication test. For GitHub a conventional value is `git@github.com:infoconex/RecordSift.git`.

### 11. Repository Default Branch

Read the repository host's **default branch** designation. Record one branch name, such as `main`, not the currently checked out detached HEAD.

### 12. Published Application Version

Identify the published application version, if one exists. If the project distributes only a library package rather than a standalone application, record `Not applicable` or the publisher-documented application version only when explicitly supported. Do not confuse source manifest, assembly and package versions.

### 13. Published Package Version

Check the official package registry/release listing. For RecordSift, NuGet.org lists `0.1.0`. Enter only the version number; put the URL in item 15.

### 14. Published Release URL

Copy the full official published release URL, not a short link label. For RecordSift: `https://github.com/infoconex/RecordSift/releases/tag/v0.1.0`.

### 15. Published Package URL

Copy the full registry package URL, e.g. `https://www.nuget.org/packages/RecordSift/0.1.0`. Keep package and release URLs distinct.

### 16. Source Manifest Version

Read the tracked package manifest, such as `packaging/RecordSift.nuspec`. Record its version **as declared**, even if it differs from a published version. RecordSift declares `0.1.0-rc.1` in this source file.

### 17. Assembly Version

Read `AssemblyVersion` in the applicable `Properties/AssemblyInfo.cs` (or generated assembly metadata for SDK-style projects). Record the declared value; if assemblies differ, explain the scope and use a per-assembly table rather than implying one universal value. Do not claim the binaries have been inspected.

### 18. File Version

Read `AssemblyFileVersion` separately from `AssemblyVersion` in the relevant assembly metadata. Record only its version, e.g. `0.1.0.0`; do not append an `AssemblyInfo` citation in the value.

### 19. Consumers and Entry Points

Inspect the application's README, actual usage guides, public interface definitions and **demonstrated consumer calls** at the pinned source revision. Record two distinct inventories under this **one numbered discovery item**. Distinguish what the product exposes from what other software is actually known to consume. A publicly visible symbol alone does **not** establish that it is a recommended, supported or directly invoked integration point.

**A. Known Consumers**

- **Consumer:** Name a specific application/system or executable example supported by evidence. An example consumer is a test or sample, **not** a production deployment.
- **Type:** A concise evidence-based classification, such as `Production application`, `Test application`, `Sample application` or `External system`. Do not infer installed or deployed consumers from the intended audience or package-download availability.
- **Evidence:** An exact consumer project, usage source, configuration/dependency reference, or recorded integration validation linked to its revision. For external deployments, identify evidence limits.
- **External production consumers:** If none can be verified, record `Not identified` outside the table rather than inventing rows. A general getting-started tutorial describes **potential** consumers, not known deployed ones.

| Consumer | Type | Evidence |
|---|---|---|
| `tests/ReleaseConsumer` | Test application | `tests/ReleaseConsumer/Program.cs` (illustrative RecordSift source path) |

**B. Public Entry Points**

Select only operations with **positive documentation or demonstration that a consumer directly invokes them**. These may be application APIs, explicit commands, HTTP routes, or other declared external integration surfaces appropriate to the application type.

- **Entry Point:** Identify the specific directly invoked operation, such as `CsvImporter<T>.Import`; do not list a class merely because it is public.
- **Purpose:** Brief description of the observable consumer-facing capability.
- **Evidence:** Link the exact source definition **and/or** consumer invocation or official usage guidance at the pinned revision. Prefer evidence of an actual direct call over visibility alone.
- **Exclusions:** Avoid private/internal helpers, public implementation classes without consumer-facing invocation evidence, and methods passed as delegates/callbacks rather than directly called. For example, RecordSift consumer code passes `PrimitivePropertyMapper<T>.Map` to its importer; that **does not** make `Map` a direct-call entry point in this inventory. Public API compatibility inventories belong in their own evidence and should not be copied wholesale into item 19.

| Entry Point | Purpose | Evidence |
|---|---|---|
| `CsvImporter<T>.Import` | Import CSV records | `docs/usage/getting-started.md` and `src/RecordSift.Application/Importing/Csv/CsvImporter.cs` (illustrative RecordSift paths) |

Do not mistake a test consumer for a deployed application, assume undiscovered consumer integrations are absent, or use a list of all exported symbols as a substitute for documented direct consumer operations.

## Discovery host and prerequisite tools

**Two environments:** For items 20–31 record **Existing CI Runner** and **Operator Local** independently. Cite the CI job/run, evaluated source SHA, execution date and runner image/version. A workflow's `runs-on` declaration identifies only a requested runner label, not installed tool versions; a present-day runner-image inventory does not prove a historical job's environment. Populate CI values only from **actual job logs or output**, keep unknown values `Not checked`, and describe partial observations separately. Operator values require separate operator-executed commands; do not copy CI values into the local column. The baseline tables use separate CI/local columns for scalar items 20–25 and 28–30, and environment-scoped rows for inventories 26, 27 and 31.

**Verified RecordSift CI example:** The [Windows restore, MSBuild and NUnit job](https://github.com/infoconex/RecordSift/actions/runs/43146607664/job/130945777245), for commit `1809d06c0fade59e4769d16e0f8eaf10fa426004`, ran on `windows-2022` image `20261101.353.1` on 2026-11-12 UTC. Its logs report Windows Server 2022 (`10.0.20348`), Git `2.56.0.windows.4`, MSBuild `17.14.60.43110` (Visual Studio 2022 Enterprise) and selected SDK `10.0.403`. PowerShell 7 was invoked without recording its exact version, and NuGet restore succeeded without recording its CLI version. NUnit reported the .NET Framework CLR version `v4.0.30319.42000`; a successful `net48` build does not prove an individually inventoried targeting pack. These observations are **CI evidence only**, not operator-local results.

**Follow-up CI-only inventory (2026-11-13):** [Read-only job `43514868868`](https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480) queried the newer `windows-2022` image `20261112.366.7`, checked out the same frozen RecordSift source SHA, and captured all 12 SDKs, 29 modern .NET runtimes, OS architecture, exact PowerShell/Git/MSBuild/NuGet versions, and physical .NET Framework v4.8 reference files. Record this as runner-specific CI evidence (EV-016), **not** an operator-local preflight. Older CI results can differ because the image changes; retain dated source references for each.

### 20. Operating System Name

Use Windows (required for RecordSift); record the **Caption** output from the command below. This is the discovery host, not the application's supported OS (item 8).

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

**One OS command populates operator-local items 20–23.** Run it once, record four separate values, and do not repeat it for each heading. For CI, use recorded job OS metadata where available, and never infer the architecture from an operating-system name or build number.

### 21. Operating System Version

From the same Windows OS command, record **Version** and nothing else.

Use the output from the command in item 20.

### 22. Operating System Build

From the same Windows OS command, record **BuildNumber** only.

Use the output from the command in item 20.

### 23. Operating System Architecture

From the same Windows OS command, record **OSArchitecture** only.

Use the output from the command in item 20.

### 24. PowerShell Version

For **operator local**, run the PowerShell version command below. Record only the complete version (e.g. `7.4.7`), not your username or environment details. Windows PowerShell 5.1 or modern PowerShell 7 may be used; if unavailable, follow [Microsoft's Windows installation guide](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).

```powershell
$PSVersionTable.PSVersion.ToString()
```

### 25. Git Version

For **operator local**, run the Git version command below and record only the version number. `git switch` requires Git 2.23 or later. If missing, install [Git for Windows](https://git-scm.com/install/win) before cloning.

```powershell
git --version
```

### 26. .NET SDK Inventory

Record SDKs separately for each environment. A CI `dotnet --version` log only proves **one selected SDK version**, not a complete SDK inventory or installation path. For **operator local**, run `dotnet --list-sdks` and add **one row for each installed SDK** with its version and installation path. If no `dotnet` CLI is installed, record the check as blocked; do not fabricate SDK rows. The .NET SDK is not necessarily required just to clone traditional projects. Install only a needed SDK from [Microsoft .NET downloads](https://dotnet.microsoft.com/en-us/download).

```powershell
dotnet --list-sdks
```

**How to populate each column (left to right):**

- **Environment:** `Existing CI runner` or `Operator local`.
- **SDK Version:** The observed SDK version; label any single-version CI evidence as partial when a complete inventory was not recorded.
- **Installation Path:** The actual observed installation directory, or `Not checked`.

### 27. .NET Runtime Inventory

Capture runtimes separately by environment. A CI NUnit log showing `.NET Framework CLR v4.0.30319.42000` is a **CLR observation**, not a complete modern .NET runtime inventory or exact .NET Framework product version. For **operator local**, run `dotnet --list-runtimes` and add one row per reported runtime family, version and installation path. The list of modern .NET runtimes does **not** establish installation of the .NET Framework 4.8 targeting pack.

```powershell
dotnet --list-runtimes
```

**How to populate each column (left to right):**

- **Environment:** `Existing CI runner` or `Operator local`.
- **Runtime Name:** The observed runtime family or host, such as `Microsoft.NETCore.App` or `.NET Framework CLR`.
- **Runtime Version:** The exact observed version (do not infer the framework product version from CLR information).
- **Installation Path:** The directory reported in that environment, or `Not checked`.

### 28. MSBuild Version

For **operator local**, run `msbuild -version -nologo` from Visual Studio Developer PowerShell, or another command environment with MSBuild on PATH. Record the reported version. A missing PATH entry is not proof MSBuild is uninstalled; use Visual Studio's Developer PowerShell or `vswhere`. [Build Tools installation](https://visualstudio.microsoft.com/downloads/).

```powershell
msbuild -version -nologo
```

### 29. MSBuild Installation Source

Identify the MSBuild installation source separately in **each environment**, such as `Visual Studio 2022 Enterprise` or the verified location of MSBuild.exe. If using `Get-Command msbuild`, the `Source` property identifies the executable path. Do not use the version number in this field.

```powershell
Get-Command msbuild -ErrorAction SilentlyContinue | Select-Object Source
```

### 30. NuGet CLI Version

For **operator local**, run `nuget help` and record the version that the CLI prints. Do not infer a CI NuGet CLI version merely because a restore succeeded. If NuGet is missing, follow [Microsoft's NuGet CLI installation guide](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli). This is not the version of a NuGet package referenced by the application.

```powershell
nuget help
```

### 31. .NET Framework Targeting Pack Inventory

For each environment, record the actual **reference-assembly / targeting-pack** check. A successful CI build targeting .NET Framework 4.8 shows build capability but **does not verify** the targeting-pack file or path; use `Not checked` for `Installed` and `Location` unless a direct file check was performed. For traditional .NET Framework projects, check the applicable **reference assemblies / targeting pack**, not merely the presence of a runtime. For RecordSift check that the .NET Framework 4.8 reference assembly `mscorlib.dll` is present, rather than checking for an empty directory. Use the printed pack path as the table `Location` and the file-check result as `Installed`. Add one row per framework actually checked. If missing, see the [.NET Framework Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).

```powershell
$pack = Join-Path $env:ProgramFiles 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8'
if (${env:ProgramFiles(x86)}) { $pack = Join-Path ${env:ProgramFiles(x86)} 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8' }
$pack
$referenceAssembly = Join-Path $pack 'mscorlib.dll'
Test-Path -LiteralPath $referenceAssembly
```

**How to populate each column (left to right):**

- **Environment:** `Existing CI runner` or `Operator local`.
- **Framework Version:** The framework and version being checked.
- **Installed:** `True` or `False` only from the actual reference-assembly file check, otherwise `Not checked`.
- **Location:** The actual path checked, or `Not checked`.

### 32. Test Runner Inventory

Identify the actual test runner from test project manifests or CI definitions, then check its installed version when possible. Record one runner per row; the package's declared version is not necessarily the locally installed runner. For RecordSift the declared runner is `NUnit.ConsoleRunner 3.17.0` in the test `packages.config`.

**How to populate each column (left to right):**

- **Runner Name:** Name the test runner, such as NUnit ConsoleRunner.
- **Runner Version:** The runner version, noting declared vs actually installed provenance separately.
- **Source or Location:** The verified executable or declared package source.

## Source revision and checkout

### 33. Discovery Folder

Choose an existing **parent directory** for the isolated discovery checkout and prepare a unique timestamped destination. Do **not** clone yet: select the source branch/tag (item 34) and pin its immutable commit SHA (item 35) **before** downloading or checking out source.

Run the following in a Windows PowerShell session that you will continue using for item 35:

```powershell
$repository = 'RecordSift'
$remoteUrl = 'https://github.com/infoconex/RecordSift.git'
$discoveryRoot = Join-Path (Join-Path $HOME 'source') 'discoveries'
New-Item -ItemType Directory -Path $discoveryRoot -Force | Out-Null
$discoveryFolder = "${repository}-discovery-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
$destination = Join-Path $discoveryRoot $discoveryFolder
if (Test-Path -LiteralPath $destination) { throw 'Discovery destination already exists; generate a new timestamp and stop.' }
$destination
```

**Safety gate:** This creates only the parent folder. It does not overwrite, delete, reset or clone an existing repository. Record the destination in item 33; if it exists, choose a new unused name. Keep `$remoteUrl` and `$destination` in the same PowerShell session for item 35.

### 34. Selected Source Branch or Tag

Record the exact branch or tag **chosen as the source**, for example `main`. This is a selected remote ref, not proof the final local checkout remains attached to that branch (see item 38). Confirm it against repository metadata before pinning the SHA.

### 35. Source Commit SHA

Choose and record a **full immutable commit SHA** for the selected source ref (item 34) before cloning. Obtain it from the repository host or a read-only remote-ref query; confirm that the SHA belongs to the intended repository/ref. For RecordSift, the previously selected source SHA is `1809d06c0fade59e4769d16e0f8eaf10fa426004`. Keep item 35 **SHA only**. In item 36, **Source Committer Date (UTC)**, record the pinned commit's Git *committer date* in UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`). Read it from the **same exact SHA** through GitHub's commit metadata (before cloning) or the read-only Git command below (after checkout); retain the same evidence in item 55's separate source-provenance table. This timestamp is **not** the discovery date (item 2), author date, clone/checkout time, GitHub push time or release publication time. A Git committer date does not reliably establish when the revision was first created or pushed.

With the unique destination prepared in item 33, use `git clone --no-checkout` and detach at that exact SHA. The selected SHA must be available in the new clone. Execute these commands **in the same PowerShell session** as item 33:

```powershell
$selectedCommit = '1809d06c0fade59e4769d16e0f8eaf10fa426004'
if (Test-Path -LiteralPath $destination) { throw 'Discovery destination already exists; refuse to clone over it.' }
git clone --no-checkout $remoteUrl $destination
if ($LASTEXITCODE -ne 0) { throw 'Git clone failed. Stop before proceeding.' }
Set-Location -LiteralPath $destination
git switch --detach $selectedCommit
if ($LASTEXITCODE -ne 0) { throw 'Commit checkout failed. Stop before proceeding.' }
$actualCommit = (git rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $actualCommit -ne $selectedCommit) { throw 'Checked-out SHA does not match the selected commit.' }
$actualCommit
git remote get-url origin

# Read the Git committer timestamp for the exact checked-out SHA.
$rawCommitterDate = (git show -s --format='%cI' HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($rawCommitterDate)) { throw 'Failed to read selected commit date.' }
$sourceCommitterDateUtc = [DateTimeOffset]::Parse($rawCommitterDate).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss'Z'")
$sourceCommitterDateUtc
```

**Safety gate:** Cloning creates a new folder and uses network access, but never modifies an existing checkout. On any failure, stop and inspect the partial destination without deleting or resetting it automatically. A successful detached checkout intentionally leaves item 38 = `True`. The read-only `git show` reports **commit metadata**, not the time the checkout happened; compare its SHA to the pinned source. If item 35 was populated from remote Git metadata before checkout, the UTC committer date may be recorded even while items 37–38 remain `Not checked`.

### 36. Source Committer Date (UTC)

Record the **Git committer timestamp** for the exact selected SHA from item 35, in UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`). It can be retrieved from immutable commit metadata before cloning or from the read-only `git show -s --format='%cI' HEAD` in the preceding checkout procedure. Use `Not checked` if unavailable, and never present a commit's committer date as a first push, discovery start, checkout timestamp or release publication. Item 55 retains the source provenance.

### 37. Working Tree Clean

Run `git status --porcelain=v1 --untracked-files=all` **inside the cloned repository**. An empty result supports `True` for a clean working tree (tracked and untracked, excluding ignored files); any lines require review. Record only `True` or `False`. Do not run `git clean` or `git reset --hard`.

```powershell
git status --porcelain=v1 --untracked-files=all
```

### 38. Detached HEAD

Run `git branch --show-current` in the selected checkout. A blank branch name after `git switch --detach` indicates a detached HEAD; record `True`. An attached branch name indicates `False`. The actual SHA from item 35 is still authoritative.

```powershell
git branch --show-current
```

## Solution and project inventory

### 39. Solutions

Enumerate tracked `.sln`, `.slnx` and `.slnf` solution files. Inspect each solution's format/header, **actual** solution configuration/platform combinations, project membership, each project's active configuration mapping and the build/skip mappings. Prefer **one row per solution**, grouping configurations and platforms **only when the actual combinations and membership/build differences remain unambiguous**. Do **not** infer a Cartesian product from separate configuration and platform lists: for example, `Debug, Release` and `Any CPU, x64` do not by themselves establish that all four combinations exist. Record the exact valid pairs and project-specific exceptions in the **Membership / Build Exclusions** column, or retain separate scoped rows if that is clearer. Distinguish `Build.0` source declarations from successful actual builds.

For RecordSift at the frozen SHA, `RecordSift.sln` declares solution format `12.00`, Visual Studio version `16.0.28701.123`, and only two solution configurations: `Debug|Any CPU` and `Release|Any CPU`. All ten projects are present and have `Build.0` mappings in both; these can safely share one row.

```powershell
git ls-files "*.sln" "*.slnx" "*.slnf"
# Optional when a compatible .NET SDK is installed; may trigger first-run SDK initialization (see warning below):
dotnet sln .\RecordSift.sln list
# Inspect the tracked solution text for declared configuration/build mapping evidence:
Get-Content -LiteralPath .\RecordSift.sln
```

**First-run side-effect warning:** `dotnet sln ... list` does not restore packages, build projects or run tests, but a .NET SDK invoked for the first time may perform machine/user-profile initialization, including creating an ASP.NET Core HTTPS development certificate. It may also display telemetry information. This is **not** a guaranteed side-effect-free command. When strictly read-only inspection is required, prefer `git ls-files` and `Get-Content -LiteralPath .\RecordSift.sln` to inspect solution membership, header and configuration mappings directly, and omit the optional `dotnet sln` invocation. If a .NET CLI is invoked and first-run setup occurs, record the side effect as separate environment evidence; do not infer that a development certificate is trusted from its creation. Treat solution listing as membership evidence only, not build success or configuration mapping verification.

**How to populate each column (left to right):**

- **Solution Path:** Repository-relative solution file path.
- **Format:** Tracked solution format, such as `.sln`.
- **Format Version:** Explicitly declared solution format version; `Not declared` if absent.
- **Declared IDE Version:** Explicit IDE version in the solution header; `Not declared` if absent.
- **Configurations:** Names of declared solution configurations, e.g. `Debug, Release`.
- **Platforms:** Names of declared solution platforms, e.g. `Any CPU`; these are **solution** platform labels, not necessarily the same text as each project's MSBuild platform.
- **Membership / Build Exclusions:** Verified project membership; explicit supported configuration/platform **pairs** if grouping separate lists would be ambiguous; project-specific active-configuration mappings, `Build.0` inclusion/exclusion and other exceptions by configuration. Record `Not checked` for mappings not inspected. Do not treat source mapping as execution evidence.

**Illustrative source-derived RecordSift example (not a new local build):**

| Solution Path | Format | Format Version | Declared IDE Version | Configurations | Platforms | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Debug, Release | Any CPU | All 10 projects mapped to build in both Debug and Release; no declared build exclusions |

### 40. Projects

Enumerate tracked projects, including those outside the solution. Read each project XML to identify format, framework(s), output type, language version, platform, tools version/SDK, and **all** direct project references. Prefer **one row per project**. Use the short, unique project name in the first column, optionally linked to its project file; keep the repository-relative `.csproj` path in the last column. List multiple direct references together by project name, rather than duplicating every other property. Preserve conditional target frameworks, platforms, or other exceptions explicitly; split a project into multiple scoped rows only if a single row would lose a real distinction.

```powershell
git ls-files "*.csproj" "*.fsproj" "*.vbproj"
```

**How to populate each column (left to right):**

- **Project:** Unique project name (link to pinned source project file when available).
- **Role:** Production, Test, Tool or another observed role.
- **Format:** Traditional or SDK-style, as declared.
- **Target Framework(s):** Every declared framework; label any conditional scope.
- **Language Version:** Source declaration or `Not declared`; qualify per-target differences.
- **Output Type:** Library, Exe, WinExe or other declared value.
- **MSBuild Platform(s):** Declared Platform value(s); do not confuse with PlatformTarget.
- **SDK or ToolsVersion:** SDK identifier or ToolsVersion, as actually declared.
- **Direct Project References:** All direct referenced project names, or `None`.
- **Project Path:** Full repository-relative project file path, **last**.

**Illustrative source-based example (all references on one row):**

| Project | Role | Format | Target Framework(s) | Language Version | Output Type | MSBuild Platform(s) | SDK or ToolsVersion | Direct Project References | Project Path |
|---|---|---|---|---|---|---|---|---|---|
| RecordSift.Infrastructure.Csv | Production | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Application; RecordSift.Domain | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |

## Project settings and evaluated values

### 41. Compiler Settings

Inspect project XML `PropertyGroup` declarations. Pivot declared compiler properties into columns so **one project generally occupies one row**. Avoid one row per property/configuration. D/R means **Debug then Release**; use a single value only when the declaration is identical in both. `Not declared` is different from `false` or a tool-evaluated default. For other configurations/frameworks or exceptional property conditions, add clearly labeled columns/scoped values or rows without discarding differences.

```powershell
Get-Content .\src\RecordSift.Domain\RecordSift.Domain.csproj
```

For the current RecordSift projects, shared conditions are `'$(Configuration)|$(Platform)' == 'Debug|AnyCPU'` for D and `'$(Configuration)|$(Platform)' == 'Release|AnyCPU'` for R; `LangVersion` is unconditional. Document these exact conditions **once above the table**, then note exceptions per project if any. These conditions are source declarations, not evidence of effective MSBuild values.

**How to populate each column (left to right):**

- **Project:** Unique project name linked to its exact source project file, with its canonical path in item 40. Qualify duplicate names; for non-project consumers link the evidence source.
- **Framework(s):** Target framework(s) within which the declarations apply.
- **LangVersion:** Unconditional language-version declaration, or separately scoped values.
- **DebugSymbols (D/R):** Exact declarations per configuration; `Not declared` if absent.
- **DebugType (D/R):** Debug and Release source values.
- **Optimize (D/R):** Debug and Release source values.
- **DefineConstants (D/R):** Exact per-configuration constants.
- **Conditions / Exceptions:** Deviations from the shared conditions, additional configurations, or `None`.

**Illustrative RecordSift declaration (not evaluated compiler output):**

| Project | Framework(s) | LangVersion | DebugSymbols (D/R) | DebugType (D/R) | Optimize (D/R) | DefineConstants (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |

### 42. Output and Validation Settings

Read source XML declarations for `OutputPath`, `WarningLevel`, `WarningsAsErrors`, `DocumentationFile` and additional validation settings. Represent **one project per row** using separate property columns. Use D/R pairs when declared values differ and **one value** when the same value is declared for both configurations. Keep exact paths, not assumed defaults. If a setting is absent, record `Not declared` rather than infer its evaluated value. Reuse the shared Debug/Release condition definitions from item 41; label exceptions explicitly.

**How to populate each column (left to right):**

- **Project:** Unique project name linked to its exact source project file, with its canonical path in item 40. Qualify duplicate names; for non-project consumers link the evidence source.
- **OutputPath (D/R):** Output directories for both configurations, in Debug/Release order.
- **WarningLevel (D/R):** One value if identical, or an ordered pair.
- **WarningsAsErrors (D/R):** Exact compiler warning identifiers or `Not declared`.
- **DocumentationFile (D/R):** Exact generated-documentation paths or `Not declared`.
- **Conditions / Exceptions:** Additional source conditions or nonstandard settings.

**Illustrative RecordSift source declarations:**

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Domain.xml` / `bin\Release\RecordSift.Domain.xml` | None |

### 43. Project Metadata and Imports

Inspect project-wide metadata (such as `Configuration`, `IsTestProject`, `FileAlignment` and `AppDesignerFolder`) and `Import` declarations. Use **one row per project**, with named metadata **as columns**, and link the project name to the canonical path recorded in item 40. Multiple imports can share one cell; preserve the actual paths and conditional scopes. Missing properties must be `Not declared`, not an assumed value. For `Configuration`, record the **declared fallback** only when the project source specifies a default for an otherwise empty `$(Configuration)`. Record the associated condition; do **not** claim it is the actual selected or evaluated configuration. For example, `<Configuration Condition=" '$(Configuration)' == '' ">Debug</Configuration>` means **Configuration Fallback = `Debug`**, not an observed Debug build. Actual evaluated configurations belong in item 44, and executed build configurations in items 49–52. If imports declare properties or conditions beyond project XML, keep them distinct from source-local metadata.

**How to populate each column (left to right):**

- **Project:** Unique project name linked to its exact source project file, with its canonical path in item 40. Qualify duplicate names; for non-project consumers link the evidence source.
- **Configuration Fallback:** Conditional fallback value from project source (for example `Debug` when `$(Configuration)` is empty), or `Not declared`. It is **not** the evaluated MSBuild `Configuration` or proof of a Debug build.
- **IsTestProject:** Declared value, or `Not declared`.
- **FileAlignment:** Declared value, or `Not declared`.
- **AppDesignerFolder:** Declared value, or `Not declared`.
- **Imports:** All relevant explicit imports; no invented implicit imports.
- **Additional Metadata / Conditions:** Other observed declarations or exceptional scope.

### 44. Evaluated MSBuild Properties

Read declared properties first. With **MSBuild 17.8 or later**, run the documented `-getProperty` query for each configuration/framework/platform that matters ([Microsoft documentation](https://learn.microsoft.com/en-us/visualstudio/msbuild/evaluate-items-and-properties)). Multiple property names can be included in one query. Use **one row per project** where possible, with property `name=value` pairs grouped under **explicit** configuration/framework/platform scopes. Retain a separate column for declared values, and cite the **actual command/output**. Split rows for different scopes only if grouping would obscure real value differences; never fabricate a value from source XML or a passing CI build.

```powershell
msbuild .\src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:TargetFrameworkVersion,LangVersion -p:Configuration=Debug -p:Platform=AnyCPU
msbuild .\src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:TargetFrameworkVersion,LangVersion -p:Configuration=Release -p:Platform=AnyCPU
```

The property-query option requires an appropriate MSBuild version. These are **evaluation-only** commands; do not add build targets. On an older installation record `Not checked` and note the tooling limitation.

**How to populate each column (left to right):**

- **Project:** Unique project name linked to its exact source project file, with its canonical path in item 40. Qualify duplicate names; for non-project consumers link the evidence source.
- **Configuration / Framework / Platform:** Exact combination(s) actually evaluated; label each when grouped.
- **Evaluated Properties (name=value):** Exact MSBuild output, scoped to its corresponding combination.
- **Declared Properties for Comparison:** Exact source declarations, separately identified.
- **Evidence:** Saved command/output or exact other execution evidence.

## Repository structure and dependencies

### 45. Repository Directories

Use `git ls-files` or an equivalent tracked-tree listing to identify meaningful source, test, documentation, script, packaging and workflow directories. One row per directory and its evidenced purpose. Do not invent directories.

```powershell
git ls-files
```

**How to populate each column (left to right):**

- **Directory:** Tracked directory path.
- **Purpose:** Its demonstrated role.

### 46. Repository Configuration

Inspect tracked `NuGet.Config` / `nuget.config`, `.editorconfig`, `global.json`, `Directory.Build.props/targets`, `Directory.Packages.props`, `.gitignore` and nested equivalents. Use **one row per observed setting** with its precise source and scope; distinguish a repository declaration from an **effective value** returned by tooling. Absence from the tracked tree does not rule out inherited user/machine settings, additional settings outside the checkout or implicit MSBuild imports.

```powershell
git ls-files "NuGet.Config" "nuget.config" "*NuGet.Config" "*nuget.config" ".editorconfig" "*.editorconfig" ".gitignore" "AGENTS.md" ".github/copilot-instructions.md" "global.json" "*global.json" "*Directory.Build.props" "*Directory.Build.targets" "*Directory.Packages.props"
```

**NuGet configuration discovery — inspect every applicable section**, not only feed URLs. See [Microsoft's NuGet.Config reference](https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file) and [configuration precedence guidance](https://learn.microsoft.com/en-us/nuget/consume-packages/configuring-nuget-behavior/).

- **Package and audit feeds:** `packageSources`, `auditSources`, `disabledPackageSources` (including the boolean state by feed), `activePackageSource` (deprecated in modern NuGet), and `packageSourceMapping` (package patterns by source). Record each `<clear />` separately: it discards previously inherited entries **for that collection**, not for every setting.
- **Supply-chain and transport security:** `trustedSigners` (trust-policy identities and certificate *fingerprints only* where safe), `config.signatureValidationMode`, and per-source `protocolVersion`, `allowInsecureConnections`, `disableTLSCertificateValidation`. Capture when options are version-dependent; for example `auditSources` was added in NuGet 6.12.
- **Credentials and certificates:** `packageSourceCredentials`, `clientCertificates`, `apikeys`, and proxy credentials. Record **presence, mechanism and scope only**, never a password, token, API key, certificate private key, raw credential-bearing URL, or unredacted secret value.
- **Storage, restore and installation:** `config.repositoryPath` (packages.config), `config.globalPackagesFolder` (PackageReference), `config.dependencyVersion`, `config.updatePackageLastAccessTime`, `packageRestore`, `packageManagement`, `bindingRedirects`, `solution` and `fallbackPackageFolders` when supported.
- **Network and publication:** `config.defaultPushSource`, `config.maxHttpRequestsPerSource`, proxy / `no_proxy` settings, source protocol settings, and applicable minimum-package-publication-age controls or exceptions (where the installed NuGet version supports them).
- **Other settings:** Record any additional actual XML section, key, condition, environment-variable substitution, per-project configuration or NuGet/MSBuild override that changes behavior. Inspect all configuration files in scope, not just this checklist.

For the **repository source** inventory, enter each actually declared setting (including `clear` entries and whether a named feed is explicitly disabled). When an important section is not present, list the absent **section names once in a short note** rather than emitting dozens of empty or `Not declared` table rows. `disabledPackageSources` **not declared** does *not* establish that all sources are enabled in the effective environment. Distinguish `Not declared` (source absence), `Not checked` (runtime state not observed) and `Not applicable` (genuinely irrelevant). Avoid confusing default NuGet behavior with a declared value.

**Effective configuration is a separate, later Windows operator check.** After tool preflight and isolated checkout, inspect inherited user/machine/directory configuration, selected tool version, environment/MSBuild variables, and command-line `--source`/`-Source`, `--configfile`/`-ConfigFile` and `RestoreSources` overrides. A `clear` in a nearer config can replace earlier sources; later applicable overrides can still alter behavior. The safe, read-only commands below list **configured package sources**, not actual download provenance, effective audit settings, credentials or every NuGet configuration key:

```powershell
# Run from the checked-out repository directory with .NET 6 SDK or later:
dotnet nuget list source --format Detailed --configfile .\NuGet.Config
dotnet nuget list source --format Detailed
```

The first command uses **only** the specified file; the second uses the applicable configuration hierarchy from the working directory. If the .NET CLI is unavailable, use an equivalent compatible `nuget sources List -ConfigFile NuGet.Config` for the **file-only** listing and a plain `nuget sources List` for the effective source list. Do not execute restore/build/test, install packages or change configuration as part of these read-only inspection steps. **Review and redact** all tool output and inspected configuration (including URLs, usernames, environment-variable expansions, proxies and certificates) before saving or sharing evidence. Record `Not checked` if no approved operator output exists.

**How to populate each column (left to right):**

- **File or Mechanism:** Tracked configuration file or separately verified effective mechanism.
- **Present:** `True`/`False` for inspected repository declarations; `Not checked` for unobserved effective settings.
- **Scope:** Repository, subdirectory, project, user, machine or command invocation — label which was actually inspected.
- **Setting Name:** Exact named key/section, for example `packageSources.clear`, `packageSources.nuget.org` or `disabledPackageSources.MyFeed`.
- **Setting Value:** Source-declared value or a *sanitized*, genuinely evaluated value; secret-bearing settings use `Configured` / `Not declared` rather than their contents.
- **Import or Precedence:** Source context, `clear` effect, conditional version applicability, inherited precedence or `Not checked` when effective behavior is unverified.

**RecordSift-specific scope:** The pinned repository `NuGet.Config` declares `packageSources` and `auditSources`, each with `<clear />` followed by a nuget.org URL. It does **not** declare `disabledPackageSources` or other optional NuGet configuration sections. This is source inspection, **not** proof of enabled feeds, tool defaults, authentication, local effective settings or feeds used during CI or a future local restore.
### 47. NuGet Package Declarations

Inspect every tracked `packages.config`, project-level `PackageReference`, and applicable `Directory.Packages.props` or other central version declarations. Record **direct, source-declared** dependencies by consuming project and exact declared version; do not invent package classifications. Do not combine versions, direct and transitive dependencies, or distinct conditional declarations as though they were equivalent. NuGet package restore or feed acquisition has **not** been established simply by finding a source declaration.

**A. Packages by project — one row per consuming project.**

- **Project:** Unique, linked project name referring to its exact source at the selected frozen commit; resolve its canonical `.csproj` path through item 40.
- **Package Count:** Count of declared packages for that project in the inspected scope, with no duplicate counting across different version sources. Where conditions create variants, state the scope explicitly rather than reporting a misleading total.
- **Declaration Source:** Direct links to the actual `packages.config`, project `PackageReference` and/or central package-version source. Preserve separate source/version links if different packages have distinct provenance.
- **Configured Feed(s):** Eligible package sources declared in the relevant configuration files, or `Not checked`. Do not call these the observed origins of installed packages.

**B. Package catalog — one row per distinct package ID and declared version.**

- **Package ID:** The exact package identifier, without appended usage notes.
- **Version:** The exact declared version, range or central-version expression where applicable; if a property or condition remains unevaluated, label that distinction. Separate rows when the same ID is declared with different versions.
- **Referenced By:** **Every** consuming project as its own linked name, using line breaks within a cell when a version is shared. A count such as `Five test projects` is not a substitute for individually identifiable consumers.
- **Declaration Source(s):** Direct source evidence for each consumer's declaration and version (including centrally managed versions). When many consumers share a version, maintain an unambiguous consumer-to-source mapping.
- **Configured Feed(s):** Source-declared eligible feeds, or `Not checked`; preserve differences by consumer or scope rather than implying a single effective source.

Preserve additional package declaration metadata such as `targetFramework`, `developmentDependency`, conditions, version overrides and applicable package-source mapping in an explicit metadata note or column if needed for fidelity. Do not infer package classifications solely from the consuming project. A package already listed in item 47 should not also appear in item 48 as a separate non-NuGet dependency.

To inspect repository-configured sources with a compatible .NET SDK:

```powershell
dotnet nuget list source --configfile .\NuGet.Config
```

The `--configfile` option requires .NET 6 SDK or later. When only NuGet CLI is present, `nuget sources List -ConfigFile NuGet.Config` is a comparable file-scoped check. These commands identify **configured sources**, not the actual source of an acquired package. Step 46 separately inventories the configuration hierarchy and potential inherited/disabled settings; do not call effective source selection verified without runtime evidence.

**Illustrative RecordSift project summary (from pinned source, not a new restore):**

| Project | Package Count | Declaration Source | Configured Feed(s) |
|---|---:|---|---|
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | 2 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config) | nuget.org |

**Illustrative catalog rows:**

| Package ID | Version | Referenced By | Declaration Source(s) | Configured Feed(s) |
|---|---|---|---|---|
| NUnit | 3.14.0 | [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config) | nuget.org |
| NUnit.ConsoleRunner | 3.17.0 | [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config) | nuget.org |

In the complete inventory, `NUnit` also identifies the other four consuming test projects individually. The pinned `NUnit.ConsoleRunner` declaration additionally sets `developmentDependency=true`; that is a source attribute, **not** an inferred package-purpose classification.


### 48. Non-NuGet Dependencies

Identify source-declared dependencies **not managed as NuGet packages**, but distinguish ordinary .NET **framework assembly references** from **other non-NuGet dependencies**. Inspect project `Reference` / `HintPath`, `COMReference` / `COMFileReference`, imported project files, source-level native loading (`DllImport`, `LibraryImport`, and dynamic loads), configuration-driven integrations, externally hosted services and documented deployment/runtime prerequisites. Do not repeat project references from item 40 or NuGet dependencies from item 47 (even if a NuGet package is also represented by a `Reference` / `HintPath` in traditional project files).

**A. Framework Assembly References**

Inventory standard target-framework assembly references declared in the project's XML (for example `System`, `System.Core` and `System.Xml`). One project per row when the values have common source/type/version/resolution. Retain all distinct assembly identities and any source-declared versions, conditions, aliases or reference-specific overrides. Record `Not declared` for absent reference version metadata and `Not checked locally` for resolution unless supported by independent build/evaluation evidence. Do **not** infer a resolved assembly version merely from `TargetFrameworkVersion`; the .NET Framework targeting pack and actual project imports must still be checked.

**B. Other Non-NuGet Dependencies**

Record native DLLs, COM components, locally supplied third-party DLLs, file- or registry-based components, external service dependencies and similar dependencies **separately**. Prefer one row per consuming project/component if the dependencies have identical attributes; split rows when versions, source conditions, location or resolution differ. For each dependency, preserve names, type/mechanism, declared version or identity, resolved/expected location, original declaration/evidence source, and the uniquely linked project identity; for dependencies outside the project inventory, record an exact source path/link in the Declaration Source column.

**How to populate the columns (left to right) in both tables:**

- **Project:** Unique project name linked to its exact source project file, with its canonical path in item 40. Qualify duplicate names; for non-project consumers link the evidence source.
- **Framework References / Dependencies:** Each distinct assembly/dependency name, grouped only without losing associated attributes.
- **Type / Mechanism:** `Framework assembly reference` for A; the specific native, COM, file, service or other mechanism for B.
- **Version / Identity:** Exact source-declared version/identity if any; otherwise `Not declared`.
- **Resolution / Location:** Verified runtime/tool resolution or location; otherwise `Not checked locally`, not an assumed installation.
- **Declaration Source:** Exact source file, inspected import, documented runtime evidence or test/CI source.

**If nothing was declared:** Leave B's data rows empty and state **“No additional non-NuGet dependency declarations identified in the inspected [files/scope]”** below the table. Separately state `Not checked` for runtime/dynamic-loading and deployed-environment dependencies if those were not inspected. Do not assert `None` or imply absence of dependencies from a static project-file search alone. Likewise, source-level import or service evidence is not proof of actual runtime resolution.

**Illustrative RecordSift framework references (A):**

| Project | Framework References | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source |
|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | System; System.Core | Framework assembly reference | Not declared | Not checked locally | RecordSift.Domain.csproj |

**RecordSift other non-NuGet dependencies (B):** No additional non-NuGet declarations were identified in the ten inspected `.csproj` files at the pinned SHA. Source inspection does **not** establish the absence of native or dynamic runtime dependencies or external services, and those runtime checks remain outstanding.


## Restore, build, tests and delivery

### 49. Operation Commands

Inspect existing documentation, build scripts and CI workflows first. Record exact **configured** native commands and their affected project/configuration. For RecordSift these include `nuget restore`, `msbuild ... /t:Rebuild`, NUnit and existing compatibility scripts. Prefer manual execution of existing tools before creating wrappers. List a command here **before** choosing whether it is safe to execute.

**How to populate each column (left to right):**

- **Operation:** Restore, Build, Test, Pack, Check or another operation.
- **Project or Solution:** Affected solution/project/assembly.
- **Configuration:** Applicable configuration or Not applicable.
- **Platform:** Applicable MSBuild platform or Not applicable.
- **Command or Workflow:** Exact existing command or CI workflow entry point.
- **Source:** Source file documenting the command.

### 50. Restore Outcomes

Determine the appropriate native restore path based on project format: traditional `packages.config` may require `nuget restore`, while PackageReference projects may use SDK/MSBuild restore. Record the proposed exact command in item 49, inspect feeds/credentials/network/write effects, and get operator approval before execution. Report actual results only; cite existing CI runs separately from local checks.

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

### 51. Build Outcomes

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

### 52. Test Outcomes

Identify the test runner and **all intended test assemblies**. On RecordSift, a full suite spans five NUnit assemblies. After a successful appropriate build and operator approval, use the existing `scripts/run_tests.ps1` (or CI's runner command) and read the NUnit XML report. One row per executed assembly; do not substitute a previous run at another SHA.

```powershell
.\scripts\run_tests.ps1 -Level All
```

**Test execution.** Requires restored packages and built Release test assemblies. Execute only with operator approval and the correct Windows environment. The existing `scripts/run_tests.ps1` is the project's runner wrapper; first inspect its behavior and its dependency on `NUnit.ConsoleRunner.3.17.0`. No new wrapper is required.

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

### 53. CI Workflows

Inspect all tracked `.github/workflows/*.yml` and `.yaml` files, including jobs, stages/steps, event triggers, branch/path filters, job `if` conditions, runner labels, matrix choices, `needs` dependencies, environment approvals and artifact/deployment actions. **Prefer one row per unique workflow + job/stage + command + runner + output/gate**, grouping event triggers only when the remaining attributes (including applicable conditions) are genuinely identical. Do **not** fold different jobs, runner operating systems, deployment steps, outputs or conditional execution into one row. In particular, `workflow_dispatch` is manual, and permission to trigger a workflow does not mean all jobs execute for every event.

```powershell
git ls-files ".github/workflows/*.yml" ".github/workflows/*.yaml"
```

Inspect the YAML source to establish the exact events and job/stage placement. The `on` event list may be constrained by `branches`, `paths`, etc.; job `if`, step-level `if`, strategy matrices and upstream `needs` can further narrow execution. When grouping a trigger list would hide distinct conditions, **use separate scoped rows or explicit trigger-specific conditions**, not an unqualified shared trigger list. Preserve exact configured commands (or clearly state that the selected command is one excerpt from a longer step), and include a source link to the workflow file.

**How to populate each column (left to right):**

- **Workflow Path:** Repository-relative workflow YAML path, preferably linked to frozen source.
- **Trigger(s):** Applicable event names (for example `push, pull_request, workflow_dispatch`), grouped only for identical command/stage records. Record branch/path/event restrictions alongside the table when relevant, and never imply all repository branches trigger it.
- **Job / Stage:** Exact job ID and step/stage name for the recorded command. Distinguish different stages in the same job, and distinct jobs sharing the same command.
- **Runner OS:** Declared `runs-on` value(s) for the specific job; expand or qualify any matrix/conditional runner choice.
- **Configured Command:** The actual source-declared command, retained in full for the selected record; use separate rows for materially different commands or relevant condition scopes. A command excerpt does not establish every step in the job.
- **Artifact or Deployment:** Actual configured output, artifact, publication or deployment intent. Distinguish a file produced locally from an uploaded artifact and from a published package/release. Identify protected environments and required approval gates in an adjacent note.

**Additional notes below the table:** List significant job `needs` dependencies, branch restrictions, conditional job/step execution, environment reviewer/approval requirements, provenance checks and publication stages. Do not infer a deployment from a `gh release view` command alone; verify if the same step includes `gh release create` and whether it is guarded by upstream successful jobs. Treat a one-time release-recovery workflow separately from the ordinary publication workflow; recovery may validate an already-published package without pushing another package.

**Source versus observed execution:** A configured command, trigger, artifact upload or deployment step is **source-inspected configuration**, not proof of a successful run. Record actual workflow runs in item 54 and the evidence manifest with exact run ID, commit SHA, status and relevant logs; only those observations establish what ran.

**Illustrative RecordSift examples from pinned source:**

| Workflow Path | Trigger(s) | Job / Stage | Runner OS | Configured Command | Artifact or Deployment |
|---|---|---|---|---|---|
| .github/workflows/windows-net48.yml | push, pull_request, workflow_dispatch | `build-test` / Restore packages.config dependencies | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | NUnit XML |
| .github/workflows/publish-release.yml | workflow_dispatch | `publish` / Publish exact package to nuget.org | ubuntu-24.04 | dotnet nuget push "dist/RecordSift.$RELEASE_VERSION.nupkg" --api-key "$NUGET_API_KEY" --source https://api.nuget.org/v3/index.json | NuGet publish (protected `nuget-release` environment) |

For the first example, the trigger list has branch filters in the workflow source. For the second, the `prepare` job requires `main`; the `publish` job needs `prepare`, and the protected environment requires owner approval before NuGet publication. Neither example, by itself, establishes that the workflow actually ran.


### 54. CI Runs

Read actual GitHub Actions run records, including their full source SHA, conclusion, run URL and run date. One row per run. For the selected RecordSift SHA there are existing successful build/test, consumer and documentation workflows. Their outcomes are **CI evidence**, not evidence that the operator's Windows host is configured.

The run date is an intrinsic part of the external workflow record; it is **not** a per-evidence collection date.

**How to populate each column (left to right):**

- **Workflow:** Workflow name.
- **Run URL:** URL of the specific run.
- **Commit SHA:** Actual tested source SHA.
- **Outcome:** Recorded conclusion/status.
- **Date:** Run date as part of the external CI record.

### 55. Package and Release Artifacts

Inspect the tracked package manifest, existing CI build and consumer verification evidence, the official NuGet registry and GitHub release/tag metadata **separately**. Never confuse a version declaration, an unpublished local CI package, and a publicly distributed artifact. Collect **one meaningful completion or snapshot date for each record**, not each internal phase of the release pipeline. Source, CI and published artifact evidence are distinct from operator-local commands; do not claim a new operator execution on the basis of existing GitHub Actions logs.

**A. Source package declarations**

- **Declaration:** Exact source manifest path (for example `packaging/RecordSift.nuspec`) linked to the frozen discovery source SHA.
- **Declared Version:** The version **in source at the frozen commit**, not a previously published version unless separately proven.
- **Source Committer Date (UTC):** The frozen source commit's Git committer timestamp, `YYYY-MM-DDTHH:MM:SSZ`. This date describes the **source snapshot**, not when the manifest first acquired that version.
- **Evidence:** Linked exact manifest and the Git commit object, not a release download inferred from version equality.

**B. CI package artifacts and verification**

- **Artifact:** Identify the CI-created package or candidate and whether it was published. A locally built `0.1.0` stable-version package is **not** automatically the NuGet.org `0.1.0` package.
- **Version:** Exact CI artifact's declared package version.
- **Verification Result:** Explicit observed result and validation type (for example local-feed clean consumer `Passed`); distinguish **unpublished** CI artifacts from published releases and distinguish source-defined steps from verified execution.
- **Verification Completed (UTC):** One UTC timestamp for the final successful verification of **that candidate**. Prefer a result-specific log PASS timestamp; if only overall job completion is available, label it as such. Do not confuse the workflow's start time, package creation, later uploads or a CI job on a different SHA with verification completion.
- **Evidence:** Exact CI run/job and, when available, specific verification logs. Leave results/dates `Not checked` or `Not executed` when appropriate.

**C. Published artifacts**

Use **one row per independently published distribution** (for example one NuGet.org package and a separate GitHub Release) even if names/versions match.

- **Artifact:** Distribution and artifact identity (e.g., `RecordSift NuGet.org package` versus `GitHub Release v0.1.0`).
- **Version:** Exact public version or tag, without combining distribution channels.
- **Status:** Verified public availability/registry listing, not inferred solely from a configured release workflow.
- **Publication Date (UTC):** One verified publication date/time per independently published artifact. Use `YYYY-MM-DDTHH:MM:SSZ` for an exact official publication timestamp. Use `YYYY-MM-DD` **with an explicit day-only qualification** when reliable publication/availability evidence proves the day but not the exact publication time. If even the day is not verified, use `Not checked`. **Do not** substitute an upload-accepted time, artifact creation date, Git commit date, GitHub Release publication date for NuGet, or a date from a different artifact.
- **Evidence:** Official registry/package page or metadata, direct GitHub Release link, and supporting successful **public-feed** verification, with source limitations stated. Store detailed publishing-stage evidence in the manifest, not as intermediate timestamp rows in the baseline.

**Source revision provenance (one row per distinct source context)**

1. **Frozen discovery source:** Item 35's full selected SHA and Git **committer timestamp** (item 36) in UTC. Do not imply the operator performed a local checkout if only the remote source was inspected.
2. **Published release tag:** Resolve the tag's target **commit** (dereference annotated tags when needed); capture the full Git SHA and the target commit's UTC committer timestamp. Do not assume the release source matches frozen discovery source or current default branch.
3. **Published package source:** Verify its source SHA from package-specific provenance, such as embedded metadata, an exact `SOURCE_COMMIT.txt` manifest/checksum or a public-feed consumer verification. If unsupported, record `Not verified` — never assume it equals the tag. Link the precise evidence, distinguishing an existing CI result from a new package download.

For all exact timestamps use `YYYY-MM-DDTHH:MM:SSZ`, and full 40-character Git SHAs. Commit author/committer dates may differ; neither guarantees original SHA creation, first push or publication date. For local commits, the following is a read-only source metadata query:

```powershell
git show -s --format='%H%n%cI%n%aI' HEAD
```

The output gives full SHA, committer ISO timestamp (potentially offset from UTC), and author ISO timestamp. **Convert any offset to UTC**, check the selected revision and label committer date explicitly. For pre-clone inventory and public releases, inspect the Git host's commit/tag metadata read-only.

**RecordSift example (frozen source versus distribution):**

- `packaging/RecordSift.nuspec` at `1809d06c0fade59e4769d16e0f8eaf10fa426004` declares `0.1.0-rc.1`; source committer timestamp is `2026-11-12T03:12:18Z`.
- Existing [Windows consumer CI run](https://github.com/infoconex/RecordSift/actions/runs/43146607706) recorded successful **unpublished** local-feed consumer verification for `0.1.0-rc.1` at `2026-11-12T03:13:13Z` and a separately constructed `0.1.0` candidate at `2026-11-12T03:13:19Z`. These are existing log PASS timestamps, not new local runs.
- Published `RecordSift 0.1.0` on NuGet.org is a **separate distribution** from [GitHub Release v0.1.0](https://github.com/infoconex/RecordSift/releases/tag/v0.1.0). The package was independently verified available from the public feed on `2026-11-01`, but its exact official NuGet listing/publication time has not been checked. GitHub Release metadata reports `published_at=2026-11-01T22:12:43Z`. Do not copy the latter timestamp to NuGet.
- The published release tag and independently verified published package source refer to `2db5c86bc26010afcb83c2e455d2471d8c9340d6`, with committer date `2026-11-01T21:13:46Z`. Existing [reconciliation and public-feed CI](https://github.com/infoconex/RecordSift/actions/runs/41355904536) provide the package provenance evidence; this discovery has **not** independently downloaded the original package.

The baseline's three artifact tables and the separate source-revision provenance table preserve these distinctions. Keep sensitive source/package credentials out of the evidence.
### 56. Runtime and Deployment Requirements

Read consumer guidance, architecture and package manifests for OS, target frameworks, runtimes, dependencies and deployment constraints. One requirement per row with the environment where it applies; do not assume a requirement is installed on the operator's machine.

**How to populate each column (left to right):**

- **Requirement:** One runtime, OS, installer, service or deployment requirement.
- **Type:** Classification of requirement.
- **Target Environment:** Where the requirement applies.
- **Source or Evidence:** Source that establishes the requirement.

### 57. Compatibility Checks

Identify existing compatibility gates (public API, assembly identity, XML documentation, package contents, vulnerability audit, consumer tests, resource identity, expected negative controls). A check is passed only when there is an actual result and matching source revision; unexecuted checks remain Not executed.

**How to populate each column (left to right):**

- **Check Type:** Specific compatibility check.
- **Target:** Affected project/library/package.
- **Method or Command:** Actual check command or procedure.
- **Outcome:** Passed, Failed, Blocked or Not executed.
- **Commit SHA:** Exact source SHA to which evidence applies.
- **Evidence:** Output, test report or CI run.

## Evidence and completion

### 58. Executed Command Evidence

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
| 37 | git status --porcelain=v1 --untracked-files=all | <checkout> | Git 2.47.0 | Repository | 0 | Passed | <saved console output> |

### 59. Findings and Gaps

Record each unresolved issue, source limitation, missing verification or cross-environment difference on its own row. Link its evidence and state one next check, rather than contaminating a simple value field with commentary.

**How to populate each column (left to right):**

- **Finding:** One concrete finding or unverified question.
- **Impact:** What risk or decision it affects.
- **Evidence:** Proof or precise gap source.
- **Next Check:** Next verification action.


**Evidence discipline:** Keep the verified value and its CI/local context in the numbered item, cite supporting source or run evidence in the evidence manifest, and record specific outstanding checks in this findings table or in item 60 (Deferred Checks). An unobserved value should be `Not checked` or `Not executed` as applicable. Do **not** create a parallel status row for every discovery item, infer a complete tool inventory from one version string, or treat CI success as local execution.

### 60. Deferred Checks

Document intentionally omitted checks with reason and trigger for revisit, one row per check. For example: `Local Release build | Windows host not inventoried | After host inventory (items 20–31) and checkout verification (items 33–38)`; use baseline item numbers instead of outdated DISC phase identifiers.

**How to populate each column (left to right):**

- **Check:** Specific check deferred.
- **Reason Deferred:** Why it was not performed.
- **Revisit When:** When and under what prerequisite to retry it.

## Completion and validation

1. Confirm every baseline number 1–60 has either an observed value, applicable dataset rows, or a documented `Not checked`/`Not executed`/`Not applicable` disposition. Use the field values, environment-specific evidence and item 59 gaps; no duplicate item-by-item status matrix is required.
2. Verify the source revision, host, configuration, and provenance of every build/test/compatibility claim. A CI result must not be relabeled as a local run.
3. Keep raw tool output and relevant CI links in the evidence manifest without copying secrets; don't add evidence dates to every entry.
4. Check that items 3–4 reflect the true discovery progress and that outstanding gaps and deferred checks appear in items 59–60. Keep discovery `In progress` or `Blocked` until mandatory checks are completed or remaining exceptions are explicitly accepted. Leave modernization recommendations outside this factual baseline.

The [RecordSift baseline](../projects/recordsift/evaluations/2026-11-technical-baseline/baseline.md) is a worked, partially populated example. Its checked source and existing CI records must be distinguished from operator-run Windows commands still outstanding.
