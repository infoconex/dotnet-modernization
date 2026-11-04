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

**Every in-scope project gets its own row**, including projects outside solutions. Do not infer uniform settings from the solution name or the first project. Each row reports that project's actual declared values; if two projects happen to share a setting, both rows still show its value.

| Project path/name | Role | Format | Target framework(s) | Language version | Output type | ToolsVersion / SDK | Direct project references |
|---|---|---|---|---|---|---|---|
| <source or test project path> | <production/test/tool> | <traditional/SDK-style> | <TFM(s)> | <language/version> | <Library/Exe/WinExe/etc.> | <value> | <direct references or —> |

### Project configuration

Keep one row **per project** for build settings relevant to the evaluation. Add separate project-specific tables only when needed to avoid an excessively wide table. Use `—` for **not explicitly declared**, not for an assumed default.

| Project | WarningLevel | WarningsAsErrors | XML documentation | IsTestProject | Notable settings / resources |
|---|---|---|---|---|---|
| <project> | <declared value or —> | <value or —> | <path, yes/no or —> | <value or —> | <only relevant additional differences> |

When an actual source audit confirms that a setting is identical across all projects, a **single compact shared-settings table with explicit coverage** is sufficient for those settings. Don't use a shared-settings claim before checking every project. Distinguish source-declared values from evaluated MSBuild properties.

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

| Gate | Result | Evidence |
|---|---|---|
| Restore and build | <passed / failed / not run, configuration> | <run, immutable SHA> |
| Full tests | <discovered/passed/failed/skipped> | <run/artifact> |
| API/assembly/resource/XML compatibility | <relevant values and outcome> | <run/artifact> |
| Packaging and consumer checks | <outcome or not applicable> | <run/artifact> |

Summarize additional application-specific gates only where useful. Reuse suitable existing evidence from the same baseline SHA; do not rerun sufficient checks just to fill a template.

## 6. Known issues and verification gaps

| Existing observation or unverified check | Impact on the baseline |
|---|---|
| <source-backed discrepancy or named gap> | <brief factual significance> |

**Baseline disposition:** <accepted / accepted with gaps / further evidence needed>

This record is **source and verification evidence only**. Modernization hypotheses, decisions and remediation plans belong in the evaluation's experiment, findings and roadmap documents.
