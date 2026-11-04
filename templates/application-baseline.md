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

### NuGet dependencies

Record package dependencies **per project**, because different projects within one solution can use different NuGet declaration formats, versions or feeds. Link each declaration to its own source file; do not infer the declaration format from another project. For larger repositories, link to an equivalent complete inventory rather than duplicating it.

| Project | Package | Declared version | Declared in | Eligible feed(s) |
|---|---|---|---|---|
| <project> | <package ID> | <version or version range> | <linked `packages.config` / `PackageReference` and central-version source if applicable> | <source key(s) or not established> |

**Declaration location** and **package origin** are different facts. `PackageReference` lives in a project file and can obtain its version from `Directory.Packages.props`; `packages.config` lists installed packages for a project, including dependency packages. A repository may contain both project styles. Capture the configured feeds, any `packageSourceMapping` rules and restore overrides from applicable NuGet configuration. If individually verified package origins differ, add an **Observed origin** column with supporting restore evidence; otherwise state once that individual origins were not established. Package caches can satisfy restore without downloading from a feed. When declared and restored versions differ, record the resolved version as a separate column or link to the resolved package graph.

Keep **distributable package dependencies** (for example, a library's `.nuspec` metadata) distinct from the project's package declarations and from test/build tooling dependencies. Do not copy the same version inventory into two tables unless those declarations differ.

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
