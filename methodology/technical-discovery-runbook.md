# .NET Technical Discovery — Step-by-Step Guide

Follow this guide alongside the [blank baseline template](../templates/application-baseline.md). Its **62 numbered headings match the baseline exactly, in the same order**, and no separate DISC phase numbering is required. Record results in the application's **copied baseline**, not here.

**Before item 1:** Replace `<Application Name>` in the copied baseline title with the actual application name. Immediately below it, replace `<Application description>` with a factual description of what the application does, its users/consumers, and core responsibilities; verify against the README, documentation and source. For RecordSift, the copy already has its name and description.

**Recording rules:** A single-value field contains only one value (for example `Library`, `Public`, `MIT`, a precise version, `True`, a path, or a URL). Keep citations, assumptions, and explanations in the evidence manifest or a specifically designated table evidence column. For a numbered table, the number identifies **the entire dataset**, never its columns or rows. Prefer one row per project for project-scoped inventories, with unique project name first and the relative project path last; group multiple references, packages or properties without losing their distinct values. Keep separate rows when different scopes or evidence cannot be combined accurately. Mark unavailable checks `Not checked`, `Not executed` or `Not applicable` accurately.

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

For traditional .NET Framework projects, check the applicable **reference assemblies / targeting pack**, not merely the presence of a runtime. For RecordSift check that the .NET Framework 4.8 reference assembly `mscorlib.dll` is present, rather than checking for an empty directory. Use the printed pack path as the table `Location` and the file-check result as `Installed`. Add one row per framework actually checked. If missing, see the [.NET Framework Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).

```powershell
$pack = Join-Path $env:ProgramFiles 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8'
if (${env:ProgramFiles(x86)}) { $pack = Join-Path ${env:ProgramFiles(x86)} 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8' }
$pack
$referenceAssembly = Join-Path $pack 'mscorlib.dll'
Test-Path -LiteralPath $referenceAssembly
```

**How to populate each column (left to right):**

- **Framework Version:** The framework and version being checked.
- **Installed:** True or False based on the reference-assembly file check; this does not verify a working compiler or build.
- **Location:** The exact path checked.

### 30. Test Runner Inventory

Identify the actual test runner from test project manifests or CI definitions, then check its installed version when possible. Record one runner per row; the package's declared version is not necessarily the locally installed runner. For RecordSift the declared runner is `NUnit.ConsoleRunner 3.17.0` in the test `packages.config`.

**How to populate each column (left to right):**

- **Runner Name:** Name the test runner, such as NUnit ConsoleRunner.
- **Runner Version:** The runner version, noting declared vs actually installed provenance separately.
- **Source or Location:** The verified executable or declared package source.

## Source revision and checkout

### 31. Discovery Folder

Choose an existing **parent directory** for the isolated discovery checkout and prepare a unique timestamped destination. Do **not** clone yet: select the source branch/tag (item 32) and pin its immutable commit SHA (item 33) **before** downloading or checking out source.

Run the following in a Windows PowerShell session that you will continue using for item 33:

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

**Safety gate:** This creates only the parent folder. It does not overwrite, delete, reset or clone an existing repository. Record the destination in item 31; if it exists, choose a new unused name. Keep `$remoteUrl` and `$destination` in the same PowerShell session for item 33.

### 32. Selected Source Branch or Tag

Record the exact branch or tag **chosen as the source**, for example `main`. This is a selected remote ref, not proof the final local checkout remains attached to that branch (see item 35). Confirm it against repository metadata before pinning the SHA.

### 33. Source Commit SHA

Choose and record a **full immutable commit SHA** for the selected source ref (item 32) before cloning. Obtain it from the repository host or a read-only remote-ref query; confirm that the SHA belongs to the intended repository/ref. For RecordSift, the previously selected source SHA is `1809d06c0fade59e4769d16e0f8eaf10fa426004`.

With the unique destination prepared in item 31, use `git clone --no-checkout` and detach at that exact SHA. The selected SHA must be available in the new clone. Execute these commands **in the same PowerShell session** as item 31:

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
```

**Safety gate:** Cloning creates a new folder and uses network access, but never modifies an existing checkout. On any failure, stop and inspect the partial destination without deleting or resetting it automatically. A successful detached checkout intentionally leaves item 35 = `True`.

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

### 38. Compiler Settings

Inspect project XML `PropertyGroup` declarations. Pivot declared compiler properties into columns so **one project generally occupies one row**. Avoid one row per property/configuration. D/R means **Debug then Release**; use a single value only when the declaration is identical in both. `Not declared` is different from `false` or a tool-evaluated default. For other configurations/frameworks or exceptional property conditions, add clearly labeled columns/scoped values or rows without discarding differences.

```powershell
Get-Content .\src\RecordSift.Domain\RecordSift.Domain.csproj
```

For the current RecordSift projects, shared conditions are `'$(Configuration)|$(Platform)' == 'Debug|AnyCPU'` for D and `'$(Configuration)|$(Platform)' == 'Release|AnyCPU'` for R; `LangVersion` is unconditional. Document these exact conditions **once above the table**, then note exceptions per project if any. These conditions are source declarations, not evidence of effective MSBuild values.

**How to populate each column (left to right):**

- **Project:** Unique project name or link.
- **Framework(s):** Target framework(s) within which the declarations apply.
- **LangVersion:** Unconditional language-version declaration, or separately scoped values.
- **DebugSymbols (D/R):** Exact declarations per configuration; `Not declared` if absent.
- **DebugType (D/R):** Debug and Release source values.
- **Optimize (D/R):** Debug and Release source values.
- **DefineConstants (D/R):** Exact per-configuration constants.
- **Conditions / Exceptions:** Deviations from the shared conditions, additional configurations, or `None`.
- **Project Path:** Repository-relative project file path, last.

**Illustrative RecordSift declaration (not evaluated compiler output):**

| Project | Framework(s) | LangVersion | DebugSymbols (D/R) | DebugType (D/R) | Optimize (D/R) | DefineConstants (D/R) | Conditions / Exceptions | Project Path |
|---|---|---|---|---|---|---|---|---|
| RecordSift.Domain | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None | src/RecordSift.Domain/RecordSift.Domain.csproj |

### 39. Output and Validation Settings

Read source XML declarations for `OutputPath`, `WarningLevel`, `WarningsAsErrors`, `DocumentationFile` and additional validation settings. Represent **one project per row** using separate property columns. Use D/R pairs when declared values differ and **one value** when the same value is declared for both configurations. Keep exact paths, not assumed defaults. If a setting is absent, record `Not declared` rather than infer its evaluated value. Reuse the shared Debug/Release condition definitions from item 38; label exceptions explicitly.

**How to populate each column (left to right):**

- **Project:** Unique project name or link.
- **OutputPath (D/R):** Output directories for both configurations, in Debug/Release order.
- **WarningLevel (D/R):** One value if identical, or an ordered pair.
- **WarningsAsErrors (D/R):** Exact compiler warning identifiers or `Not declared`.
- **DocumentationFile (D/R):** Exact generated-documentation paths or `Not declared`.
- **Conditions / Exceptions:** Additional source conditions or nonstandard settings.
- **Project Path:** Repository-relative project file path, last.

**Illustrative RecordSift source declarations:**

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions | Project Path |
|---|---|---|---|---|---|---|
| RecordSift.Domain | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Domain.xml` / `bin\Release\RecordSift.Domain.xml` | None | src/RecordSift.Domain/RecordSift.Domain.csproj |

### 40. Project Metadata and Imports

Inspect project-wide metadata (such as `Configuration`, `IsTestProject`, `FileAlignment` and `AppDesignerFolder`) and `Import` declarations. Use **one row per project**, with named metadata **as columns**, and put the project path last. Multiple imports can share one cell; preserve the actual paths and conditional scopes. Missing properties must be `Not declared`, not an assumed value. If imports declare properties or conditions beyond project XML, keep them distinct from source-local metadata.

**How to populate each column (left to right):**

- **Project:** Unique project name or link.
- **Default Configuration:** Explicit configuration declaration, or `Not declared`.
- **IsTestProject:** Declared value, or `Not declared`.
- **FileAlignment:** Declared value, or `Not declared`.
- **AppDesignerFolder:** Declared value, or `Not declared`.
- **Imports:** All relevant explicit imports; no invented implicit imports.
- **Additional Metadata / Conditions:** Other observed declarations or exceptional scope.
- **Project Path:** Repository-relative project file path, last.

### 41. Evaluated MSBuild Properties

Read declared properties first. With **MSBuild 17.8 or later**, run the documented `-getProperty` query for each configuration/framework/platform that matters ([Microsoft documentation](https://learn.microsoft.com/en-us/visualstudio/msbuild/evaluate-items-and-properties)). Multiple property names can be included in one query. Use **one row per project** where possible, with property `name=value` pairs grouped under **explicit** configuration/framework/platform scopes. Retain a separate column for declared values, and cite the **actual command/output**. Split rows for different scopes only if grouping would obscure real value differences; never fabricate a value from source XML or a passing CI build.

```powershell
msbuild .\src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:TargetFrameworkVersion,LangVersion -p:Configuration=Debug -p:Platform=AnyCPU
msbuild .\src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:TargetFrameworkVersion,LangVersion -p:Configuration=Release -p:Platform=AnyCPU
```

The property-query option requires an appropriate MSBuild version. These are **evaluation-only** commands; do not add build targets. On an older installation record `Not checked` and note the tooling limitation.

**How to populate each column (left to right):**

- **Project:** Unique project name or link.
- **Configuration / Framework / Platform:** Exact combination(s) actually evaluated; label each when grouped.
- **Evaluated Properties (name=value):** Exact MSBuild output, scoped to its corresponding combination.
- **Declared Properties for Comparison:** Exact source declarations, separately identified.
- **Evidence:** Saved command/output or exact other execution evidence.
- **Project Path:** Repository-relative project file path, last.

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
### 44. NuGet Package Declarations

Inspect `packages.config`, `PackageReference` and central package versions. Prefer **one row per consuming project** and list every package as **ID — declared version — purpose** within its Packages cell (one line per package, separated by `<br>` in GitHub Markdown when needed). Do not collapse different declared versions of the same package or lose per-package conditions. The declaration/version source can be displayed once when shared; otherwise label the individual package's source or use separate scoped rows. The package feed is only the **configured** source, not proven actual download origin. Record complete project path last.

To inspect repository-configured sources with a compatible .NET SDK:

```powershell
dotnet nuget list source --configfile .\NuGet.Config
```

The `--configfile` option requires .NET 6 SDK or later. When only NuGet CLI is present, use `nuget sources List -ConfigFile NuGet.Config` as applicable. A configured feed does not establish acquisition origin.

**How to populate each column (left to right):**

- **Project:** Unique consuming project name or link.
- **Packages (ID — Version — Purpose):** Every package ID, its precise declared version and purpose, kept together per package.
- **Declaration / Version Source:** Source file(s), including central versions and relevant conditions.
- **Configured Feed(s):** Configured eligible sources (or `Not checked`), with package-specific distinctions where needed.
- **Project Path:** Repository-relative consuming project file path, last.

**Illustrative RecordSift grouping:**

| Project | Packages (ID — Version — Purpose) | Declaration / Version Source | Configured Feed(s) | Project Path |
|---|---|---|---|---|
| RecordSift.Domain.Tests | NUnit — 3.14.0 — Test framework<br>NUnit.ConsoleRunner — 3.17.0 — Test runner | packages.config (within project directory) | nuget.org | tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj |

### 45. Other External Dependencies

Inspect project `Reference`/`HintPath`, `COMReference`/`COMFileReference`, native libraries, services, and other non-NuGet dependencies. Prefer **one row per consumer/project**, listing all distinct dependencies together. If they share type, declared identity and resolution, those fields can be represented once. When attributes differ, annotate the affected dependency (or use separate scoped rows) to avoid losing per-dependency metadata. Do not repeat direct project references from item 37 or NuGet packages from item 44. Project-file declarations cannot rule out runtime dynamic loading.

**How to populate each column (left to right):**

- **Project:** Unique consuming project/component name or link.
- **Dependencies:** All distinct non-NuGet dependency names.
- **Type / Mechanism:** Source-declared reference mechanism(s), with mappings if mixed.
- **Version / Identity:** Exact version or identity, or `Not declared`.
- **Resolution / Location:** Verified resolution, or `Not checked`, not assumed availability.
- **Declaration Source:** Source(s) of these declarations.
- **Project Path:** Repository-relative project file path, last.

**Illustrative RecordSift source references:**

| Project | Dependencies | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source | Project Path |
|---|---|---|---|---|---|---|
| RecordSift.Domain | System; System.Core | Framework assembly reference | Not declared | Not checked locally | RecordSift.Domain.csproj | src/RecordSift.Domain/RecordSift.Domain.csproj |

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
