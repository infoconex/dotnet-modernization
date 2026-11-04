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

**Use one row per project, with Debug and Release side-by-side as columns**, not separate rows. For projects with additional named configurations, add the relevant configuration columns. Keep related settings in focused tables rather than creating an excessively wide matrix. Only include properties relevant to the application and its modernization evaluation.

**Compiler settings**

| Project | DebugType (Debug) | DebugType (Release) | Optimize (Debug) | Optimize (Release) | DefineConstants (Debug) | DefineConstants (Release) |
|---|---|---|---|---|---|---|
| <project> | <value> | <value> | <value> | <value> | <value> | <value> |

**Output and validation settings**

| Project | OutputPath (Debug) | OutputPath (Release) | WarningLevel (Debug) | WarningLevel (Release) | WarningsAsErrors (Debug) | WarningsAsErrors (Release) | DocumentationFile (Debug) | DocumentationFile (Release) |
|---|---|---|---|---|---|---|---|---|
| <project> | <value> | <value> | <value> | <value> | <value> | <value> | <value> | <value> |

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

### Dependencies

Each external dependency/package occupies **one row** when individual versions are relevant. Record NuGet declaration format, package feeds and project-reference topology without repeating the project inventory.

| Package / dependency | Declared version | Resolved version, if verified |
|---|---|---|
| <package name> | <version> | <version or not verified> |

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
