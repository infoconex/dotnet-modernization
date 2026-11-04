# <Application> — Application baseline

**Repository:** <owner/repository>  
**Baseline commit:** <full immutable SHA>  
**Source inventory date:** <YYYY-MM-DD> · **Verification date:** <YYYY-MM-DD or not executed>  
**Evidence status:** <verified / partial / blocked; identify gaps>

Document the **unchanged application**. Record facts once, using exact source values and evidence. Move modernization findings and recommendations into the evaluation, not this baseline. See the [evaluation process](../methodology/evaluation-process.md#2-establish-the-baseline).

## 1. Application overview

<One short paragraph: what the application does, its intended consumers and application type.>

| Attribute | Value |
|---|---|
| Application name | <name> |
| Application type | <library, API, service, desktop, etc.> |
| Git provider | <GitHub, etc.> |
| Repository | <owner/name> |
| Visibility | <public/private> |
| Repository URL | <browser link> |
| HTTPS clone URL | <URL> |
| SSH clone URL | <URL> |
| Default branch | <branch> |
| Baseline commit | <full SHA> |
| License | <license> |
| Supported OS | <OS/platform> |
| Published application/package version | <value and source> |
| Source manifest version | <value and source> |
| Assembly version | <value and source, if applicable> |
| File version | <value and source, if applicable> |

Only include attributes that apply. Keep distinct version concepts in separate rows.

## 2. Solution and projects

### Solutions

One row per solution. If no solution exists, inventory standalone project entry points instead.

| Solution path | Format | Format version | Declared IDE version | Configurations | Platforms |
|---|---|---|---|---|---|
| <.sln/.slnx path> | <format> | <actual declaration or —> | <actual declaration or —> | <configurations> | <platforms> |

Document relevant solution-level build inclusion/exclusions, nested solution folders and project mappings **only where present or important**. Solution versions are not evidence of an installed toolchain.

### Project inventory

**One row for each project** in scope, including standalone projects not included in any solution. Record that project's own values; do not assume all projects share the same settings.

| Project path/name | Role | Format | Target framework(s) | Language version | Output type | Platform | ToolsVersion / SDK | Direct project references |
|---|---|---|---|---|---|---|---|---|
| <project file> | <production/test/tool> | <traditional/SDK-style> | <TFM(s)> | <language/version> | <Library/Exe/etc.> | <AnyCPU/x64/etc.> | <value> | <declared direct refs or —> |

### Project-specific configuration

**Use one row per project.** Include separate Debug and Release columns **only when their declared values differ**; collapse identical values and verified configuration-based path patterns into one column. When a project has different values that cannot be expressed with a shared pattern, show each configuration explicitly. Treat additional configurations similarly. Keep related settings in focused tables and include only properties relevant to the evaluation.

**Compiler settings**

| Project | DebugType (Debug) | DebugType (Release) | Optimize (Debug) | Optimize (Release) | DefineConstants (Debug) | DefineConstants (Release) |
|---|---|---|---|---|---|---|
| <project> | <value> | <value> | <value> | <value> | <value> | <value> |

**Output and validation settings**

Use a single column for a property when both configurations declare the same value or follow a clearly verified configuration-based path pattern. Show per-configuration values only for exceptions.

| Project | OutputPath | WarningLevel | WarningsAsErrors | DocumentationFile |
|---|---|---|---|---|
| <project> | <shared value or `bin\\<Configuration>\\`> | <shared value or Debug/Release values> | <shared value or —> | <shared value, path pattern, or —> |

`<Configuration>` in a path is a **display placeholder** for verified Debug/Release paths, not an MSBuild expression. For any project whose two configurations differ beyond the placeholder, show the actual Debug and Release values explicitly rather than implying they match.

**Project-wide metadata**

| Project | Default Configuration | IsTestProject | FileAlignment | AppDesignerFolder | Custom imports |
|---|---|---|---|---|---|
| <project> | <value> | <value or —> | <value or —> | <value or —> | <import(s)> |

Record additional settings (e.g., DebugSymbols, signing, resources, platform targets, generated code) in the relevant focused table when applicable. `—` means **not declared**, not an evaluated default. The baseline captures **source declarations** separately from values evaluated by MSBuild; don't present source-only inspection as an executed property comparison.

## 3. Repository structure and configuration

| Directory | Purpose |
|---|---|
| <directory> | <one-line purpose, not a count of files> |

Record existing modernization and build configuration files, including relevant *absent* mechanisms, without generating an exhaustive list of unrelated filenames.

| File or mechanism | Present? | Existing purpose |
|---|---|---|
| <file/path> | <yes/no/unknown> | <current use or —> |

Tracked-source presence does not establish whether the toolchain imports other or generated configuration files. **Absence is not an implementation recommendation.**

## 4. Dependencies and build

### External dependencies

Capture **all externally supplied dependencies**, not only NuGet packages. Project-to-project references are already in the project inventory; do not duplicate them here. Use a NuGet table for package declarations and a separate table **only when other external dependency mechanisms are present**. If none are declared, say so briefly. Record both build-time and runtime dependencies, and distinguish source inspection from executed discovery.

**NuGet package declarations**

Record one row per project/package declaration. Different projects may use `packages.config`, `PackageReference`, centrally managed versions, or a mixture.

| Project | Package | Declared version | Declared in | Eligible feed(s) |
|---|---|---|---|---|
| <project> | <package ID> | <version or range> | <linked `packages.config`, project `PackageReference`, central-version file if applicable> | <configured source key(s), or not established> |

The configured feed is **not necessarily the actual download origin**. Capture package-source mappings, NuGet restore overrides and source configuration. Add a verified **Resolved version** or **Observed origin** column when useful evidence exists; otherwise record the gap once. Keep the distributable package's own dependency metadata (such as a `.nuspec`) separate from project declarations.

**Other external dependencies (when present)**

| Project / consumer | Dependency | Type / reference mechanism | Declared at | Version / identity | Location / resolution |
|---|---|---|---|---|---|
| <project> | <Vendor.Library.dll> | <assembly `Reference` with `HintPath`> | <linked project file> | <assembly identity/version if declared> | <relative/absolute path, verified or unresolved> |
| <project> | <COM component> | <`COMReference`, `COMFileReference` or runtime activation> | <project file or code link> | <type-library GUID/major/minor, ProgID if known> | <registered on host / interop DLL / unknown> |
| <project> | <native library> | <P/Invoke or dynamic native load> | <code or build manifest> | <DLL name/version/architecture> | <deployment path or runtime search behavior> |
| <application> | <database/service> | <runtime service/API dependency> | <documented configuration or code> | <endpoint type/protocol/version if applicable> | <host/environment; omit secrets> |

Additional mechanisms may include framework references, GAC-resolved assemblies, reference assemblies, custom build tasks, generated code, shared files, native packages or deployment-installed components. **Do not equate `Reference` without `HintPath` with proven GAC resolution**: an actual build or loader trace may be needed. For COM, include registration, platform bitness and interop requirements if known. For local DLLs, identify whether the referenced file is tracked, generated, installed externally, or missing. Source-only scans may not reveal reflection, runtime COM activation, native loading or external-service calls; mark those as **not assessed** rather than absent.

### Build environment

| Attribute | Observed value |
|---|---|
| OS / runner | <OS and version> |
| MSBuild version | <observed version and tool provenance> |
| .NET SDK version | <observed version or not applicable> |
| NuGet version | <observed version or not applicable> |
| Test runner version | <observed version> |

### Entry points

| Operation | Command, script or workflow |
|---|---|
| Restore | <exact command> |
| Build | <exact command / configuration> |
| Full tests | <runner/workflow> |
| Compatibility checks | <links to scripts/commands> |
| Packaging | <entry point, when applicable> |
| Consumer/deployment verification | <entry point, when applicable> |

## 5. Verification results

| Compatibility gate | Result | Evidence |
|---|---|---|
| Dependency restore | <passed / failed / not executed> | <run, immutable SHA> |
| Solution/project build | <passed / failed / not executed; configuration> | <run> |
| Automated tests | <discovered / passed / failed / skipped; detail in test table if useful> | <run/artifact> |
| Public API compatibility | <result or not applicable> | <contract snapshot/run> |
| Assembly identity | <result or not applicable> | <snapshot/run> |
| Embedded resource identity | <result, not executed or not applicable> | <snapshot/run> |
| XML documentation | <result or not applicable> | <run/artifact> |
| Package contents | <result or not applicable> | <artifact/run> |
| Package metadata | <result or not applicable> | <manifest/run> |
| Dependency validation | <result or not applicable> | <restore/validator run> |
| Vulnerability audit | <result or not executed> | <audit run> |
| Installed-package consumer | <result or not applicable> | <consumer run> |
| Application-specific integration checks | <result or not applicable> | <run/artifact> |

Use one row per separately checked fact, with the actual result and its evidence. Remove inapplicable gates or explicitly mark them as such. Reuse suitable existing evidence from the same baseline SHA; do not rerun sufficient checks just to fill a template.

## 6. Known issues and verification gaps

| Existing observation or unverified check | Impact on the baseline |
|---|---|
| <source-backed discrepancy or named gap> | <brief factual significance> |

**Baseline disposition:** <accepted / accepted with gaps / further evidence needed>

This record is **source and verification evidence only**. Modernization hypotheses, decisions and remediation plans belong in the evaluation's experiment, findings and roadmap documents.
