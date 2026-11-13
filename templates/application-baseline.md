# `<Application>` — Technical discovery report

**Repository:** `<owner/repository browser link>`  
**Baseline source ref:** `<branch, tag, or detached commit>`  
**Baseline commit:** `<full immutable SHA>`  
**Source inventory date:** `<YYYY-MM-DD>` · **Verification date:** `<YYYY-MM-DD or not executed>`  
**Evidence status:** `<verified / partial / blocked; identify gaps>`

This is the **single complete report** of what was found during discovery. An assistant fills it in from actual results shared by the person following the [step-by-step guide](../methodology/technical-discovery-runbook.md). Record facts once, include links to supporting output, and mark anything not yet checked. Use the [variation guide](../methodology/baseline-variation-guide.md) when a project has different configurations, frameworks or build systems. Modernization recommendations belong elsewhere.

## Discovery details

**Executed by:** `<name/role or operator label>`  
**Execution date / time zone:** `<date and time zone or not executed>`  
**Discovery folder:** `<dated folder or not yet created>`  
**Local checkout status:** `<clean/changes observed/not checked>`

### Prerequisites and tool versions

Record the **actual** result for every tool checked. The commands, minimum versions and installation instructions live in the [guide](../methodology/technical-discovery-runbook.md), not here.

| Tool or prerequisite | Version or result found | Status | Evidence |
|---|---|---|---|
| Operating system / architecture | `<version/build/architecture>` | `<checked/not checked>` | `<link or —>` |
| PowerShell | `<version>` | `<checked/not checked>` | `<link or —>` |
| Git | `<version>` | `<checked/not checked>` | `<link or —>` |
| .NET SDK / runtimes | `<versions or not installed>` | `<checked/not applicable/not checked>` | `<link or —>` |
| MSBuild / Visual Studio Build Tools | `<version / installation source>` | `<checked/not checked>` | `<link or —>` |
| NuGet CLI | `<version>` | `<checked/not applicable/not checked>` | `<link or —>` |
| Framework targeting pack(s) | `<pack/version or not found>` | `<checked/not applicable/not checked>` | `<link or —>` |
| Test runner(s) | `<name/version>` | `<checked/not applicable/not checked>` | `<link or —>` |

### What was checked

Use the guide's DISC numbers to summarize the results. **Not executed** is a valid result.

| Step | Result | Evidence / missing information |
|---|---|---|
| DISC-001 — Tools and checkout | `<result or not executed>` | `<link or missing item>` |
| DISC-002 — Solutions and projects | `<result or not checked>` | `<link or missing item>` |
| DISC-003 — Project types and targets | `<result or not checked>` | `<link or missing item>` |
| DISC-004 — Build-tool versions | `<result or not checked>` | `<link or missing item>` |
| DISC-005 — MSBuild settings | `<result or not checked>` | `<link or missing item>` |
| DISC-006 — Shared configuration | `<result or not checked>` | `<link or missing item>` |
| DISC-007 — Dependencies | `<result or not checked>` | `<link or missing item>` |
| DISC-008 — Restore | `<result or not executed>` | `<link or missing item>` |
| DISC-009 — Build | `<result or not executed>` | `<link or missing item>` |
| DISC-010 — Tests | `<result or not executed>` | `<link or missing item>` |
| DISC-011 — CI and packaging | `<result or not checked>` | `<link or missing item>` |
| DISC-012 — Compatibility checks | `<result or not checked>` | `<link or missing item>` |
| DISC-013 — Review results | `<result or not checked>` | `<link or missing item>` |
| DISC-014 — Final review | `<result or not completed>` | `<link or missing item>` |

### Collected command results

For commands actually run, record the **exact command, what happened, and where the output was saved**. Add rows as needed. Use the full source SHA and relevant project/configuration when the scope changes.

| Step | Command and scope | Actual result / exit code | Output or evidence link |
|---|---|---|---|
| `DISC-NNN` | `<command, project, configuration>` | `<result and code, or not captured>` | `<link or output excerpt>` |

## 1. Application overview

`<One short paragraph: what the application does, its intended consumers and application type.>`

| Attribute | Value |
|---|---|
| Application name | `<name>` |
| Application type | `<library, API, service, desktop, etc.>` |
| Visibility | `<public/private>` |
| HTTPS clone URL | `<URL>` |
| SSH clone URL | `<URL>` |
| Default branch | `<branch>` |
| License | `<license>` |
| Supported OS | `<OS/platform>` |
| Published application/package version | `<value and source>` |
| Published package or release URL | `<exact public/package/release URL, if applicable>` |
| Source manifest version | `<value and source>` |
| Assembly version | `<value and source, if applicable>` |
| File version | `<value and source, if applicable>` |

Only include applicable fields. Multiple applications, runtime environments or separately versioned artifacts may require scoped rows. Keep distinct version concepts separate.

## 2. Solution and projects

### Solutions

One row per solution (`.sln`, `.slnx`, and relevant filters). Support **none, one or several** solutions, overlapping project memberships and standalone projects. Where mapping varies, add per-configuration/project build-inclusion detail.

| Solution path | Format | Format version | Declared IDE version | Configurations | Platforms |
|---|---|---|---|---|---|
| `<.sln/.slnx path>` | `<format>` | `<actual declaration or —>` | `<actual declaration or —>` | `<configurations>` | `<platforms>` |

Document relevant solution-level build inclusion/exclusions, nested solution folders and project mappings **only where present or important**. Solution versions are not evidence of an installed toolchain.

### Project inventory

**One row per project**, including projects outside solutions. Record conditional, inherited, multi-targeted or configuration-specific values at their actual scope. **MSBuild Platform** refers to the project's `Platform` property; `PlatformTarget`, `Prefer32Bit`, RIDs and effective architecture are distinct settings (see the variation guide).

| Project path/name | Role | Format | Target framework(s) | Language version | Output type | MSBuild Platform | ToolsVersion / SDK | Direct project references |
|---|---|---|---|---|---|---|---|---|
| `<project file>` | `<production/test/tool>` | `<traditional/SDK-style>` | `<TFM(s)>` | `<language/version>` | `<Library/Exe/etc.>` | `<AnyCPU/x64/etc.>` | `<value>` | `<declared direct refs or —>` |

### Project-specific configuration

**Use one row per project in each relevant table.** Separate Debug/Release columns only where values differ; combine identical values and verified path patterns. Support additional named configurations, platforms, target frameworks and conditional/inherited properties using additional columns or focused tables. `Debug` and `Release` are examples, not guaranteed configurations.

**Compiler settings**

| Project | DebugType (Debug) | DebugType (Release) | Optimize (Debug) | Optimize (Release) | DefineConstants (Debug) | DefineConstants (Release) |
|---|---|---|---|---|---|---|
| `<project>` | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` | `<value>` |

**Output and validation settings**

Show identical or verified patterned values once; split configuration columns when they differ.

| Project | OutputPath | WarningLevel | WarningsAsErrors | DocumentationFile |
|---|---|---|---|---|
| `<project>` | `<shared value or configuration path pattern>` | `<shared value or named configuration values>` | `<shared value or not declared>` | `<shared value, path pattern, or not declared>` |

`<Configuration>` in a path is a **display placeholder** for verified Debug/Release paths, not an MSBuild expression. For any project whose two configurations differ beyond the placeholder, show the actual Debug and Release values explicitly rather than implying they match.

**Project-wide metadata**

| Project | Default Configuration | IsTestProject | FileAlignment | AppDesignerFolder | Custom imports |
|---|---|---|---|---|---|
| `<project>` | `<value>` | `<value or —>` | `<value or —>` | `<value or —>` | `<import(s)>` |

Record additional settings (e.g., DebugSymbols, signing, resources, platform targets, generated code) in the relevant focused table when applicable. `—` means **not declared**, not an evaluated default. The baseline captures **source declarations** separately from values evaluated by MSBuild; don't present source-only inspection as an executed property comparison.

## 3. Repository structure and configuration

| Directory | Purpose |
|---|---|
| `<directory>` | `<one-line purpose, not a count of files>` |

Record meaningful existing and absent configuration files. Check root, nested, imported, machine/user, and CI scopes when they may affect evaluation; do not list unrelated files just to fill the table.

| File or mechanism | Present? | Existing purpose |
|---|---|---|
| `<file/path>` | `<yes/no/unknown>` | `<current use or —>` |

Tracked-source presence does not establish whether the toolchain imports other or generated configuration files. **Absence is not an implementation recommendation.**

## 4. Dependencies and build

### External dependencies

Include **non-NuGet** dependencies only when evidenced, and do not repeat project references from Section 2. Distinguish source declarations from verified runtime dependencies; state unassessed categories briefly.

**NuGet package declarations**

Record one row per project/package declaration. Identify its source file (`packages.config`, project `PackageReference`, central version source where applicable) and its usage. See the variation guide for conditional versions, feeds and target frameworks.

| Project | Package | Declared version | Declared in | Eligible feed(s) | Usage |
|---|---|---|---|---|---|
| `<project>` | `<package ID>` | `<version or range>` | `<declaration file and central version file if applicable>` | `<configured feed(s) or not established>` | `<production, test, tool, or other evidenced purpose>` |

The **Usage** column identifies the consuming project's purpose; it does **not** establish whether a package was historically direct or transitive. Capture configured feeds separately from **verified acquisition origin**. If the latter is unverified, note that once. Relate package-owned assemblies to their package instead of duplicating them. Published `.nuspec` dependencies are a separate consumer contract.

**Other external dependencies (when present)**

| Project / consumer | Dependency | Type / reference mechanism | Declared at | Version / identity | Location / resolution |
|---|---|---|---|---|---|
| `<project>` | `<Vendor.Library.dll>` | `<managed Reference with HintPath>` | `<linked project file>` | `<assembly identity/version if declared>` | `<relative/absolute path, verified or unresolved>` |
| `<project>` | `<COM component>` | `<COMReference, COMFileReference or runtime activation>` | `<project file or code link>` | `<type-library GUID/version, ProgID if known>` | `<registration, interop binary, or unknown>` |
| `<project>` | `<native library>` | `<P/Invoke or dynamic native load>` | `<code or build manifest>` | `<DLL name/version/architecture>` | `<deployment path or runtime search behavior>` |
| `<application>` | `<database/service>` | `<runtime service/API dependency>` | `<documented configuration or code>` | `<endpoint type/protocol/version if applicable>` | `<host/environment; omit secrets>` |

Use the [variation guide](../methodology/baseline-variation-guide.md#4-external-dependency-fields) for framework, GAC, COM, native and runtime cases. Record **not assessed** rather than claiming runtime mechanisms absent based only on project XML.

### Build environment

Tool versions for the operator's machine belong in **Discovery details** above. Add an additional environment table here only when CI, a VM, a container, or another host uses materially different tools or configurations. Record the host, relevant versions, and supporting evidence; do not copy the same local environment twice.

### Entry points

Distinguish entry points by solution, configuration, platform, target framework, CI matrix or deployment environment where their commands differ.

| Operation | Command, script or workflow |
|---|---|
| Restore | `<exact command>` |
| Build | `<exact command / configuration>` |
| Full tests | `<runner/workflow>` |
| Compatibility checks | `<links to scripts/commands>` |
| Packaging | `<entry point, when applicable>` |
| Consumer/deployment verification | `<entry point, when applicable>` |

## 5. Verification results

| Compatibility gate | Result | Evidence |
|---|---|---|
| Dependency restore | `<passed / failed / not executed>` | `<run, immutable SHA>` |
| Solution/project build | `<passed / failed / not executed; configuration>` | `<run>` |
| Automated tests | `<discovered / passed / failed / skipped; detail in test table if useful>` | `<run/artifact>` |
| Public API compatibility | `<result or not applicable>` | `<contract snapshot/run>` |
| Assembly identity | `<result or not applicable>` | `<snapshot/run>` |
| Embedded resource identity | `<result, not executed or not applicable>` | `<snapshot/run>` |
| XML documentation | `<result or not applicable>` | `<run/artifact>` |
| Package contents | `<result or not applicable>` | `<artifact/run>` |
| Package metadata | `<result or not applicable>` | `<manifest/run>` |
| Dependency validation | `<result or not applicable>` | `<restore/validator run>` |
| Vulnerability audit | `<result or not executed>` | `<audit run>` |
| Installed-package consumer | `<result or not applicable>` | `<consumer run>` |
| Application-specific integration checks | `<result or not applicable>` | `<run/artifact>` |

Use one row per independently checked fact **and execution combination where outcomes differ** (configuration, OS, TFM, platform, consumer). Distinguish passed, failed, partial, blocked, not executed and not applicable; preserve deliberate negative controls and harness failures separately. Remove unrelated gates or mark them not applicable. Reuse suitable existing evidence from the same baseline SHA; do not rerun sufficient checks just to fill a template.

## 6. Known issues and verification gaps

| Existing observation or unverified check | Impact on the baseline |
|---|---|
| `<source-backed discrepancy or named gap>` | `<brief factual significance>` |

**Baseline disposition:** `<accepted / accepted with gaps / further evidence needed>`

This record is **source and verification evidence only**. Modernization hypotheses, decisions and remediation plans belong in the evaluation's experiment, findings and roadmap documents.
