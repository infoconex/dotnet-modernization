# `<Application>` — Technical discovery form and report

This is the **single form** completed during discovery. Use the [step-by-step guide](../methodology/technical-discovery-runbook.md) to gather results. The person performing the checks provides output; the assistant fills in the form.

- **Every field has a permanent ID**, such as `F-006` for Git version. The guide uses these same IDs.
- **One answer per field.** For project, solution, package and execution tables, use a new row for each item; each column keeps the same field ID. Identify the item by its project/path/name.
- Leave unanswered fields as **Not checked**, **Not executed** or **Not applicable**. Do not copy results from an older source revision as new results.
- Link to actual output or relevant excerpts, and avoid secrets/personal paths. See the [variation guide](../methodology/baseline-variation-guide.md) when builds have conditional settings or multiple frameworks.
- This records facts, not modernization recommendations.

## A. Discovery setup — DISC-001 and DISC-004

| Field | What to fill in | Result |
|---|---|---|
| F-001 | Person or system performing discovery | `<operator>` |
| F-002 | Discovery date, time and time zone | `<date/time>` |
| F-003 | Dated discovery folder | `<folder or not yet created>` |
| F-004 | Operating system, version/build, architecture | `<actual result>` |
| F-005 | PowerShell version (if used) | `<actual result>` |
| F-006 | Git version | `<actual result>` |
| F-007 | Installed .NET SDKs and runtimes | `<versions or not installed>` |
| F-008 | MSBuild / Visual Studio Build Tools version and source | `<actual result>` |
| F-009 | Standalone NuGet CLI version | `<actual result>` |
| F-010 | Framework targeting packs needed and found | `<versions or check result>` |
| F-011 | Test runner and version | `<runner/version or not checked>` |
| F-012 | Selected source branch or tag | `<ref>` |
| F-013 | Exact source commit SHA | `<full SHA>` |
| F-014 | Local checkout status (clean/changes/detached) | `<actual status or not checked>` |
| F-015 | Verification date (if distinct from inspection date) | `<date or not executed>` |
| F-016 | Overall evidence status | `<verified/partial/blocked/not executed>` |

**Evidence for prerequisites and checkout:** `<link or not yet available>`

## B. Application — DISC-002 and DISC-003

| Field | What to fill in | Result |
|---|---|---|
| F-101 | Application name | `<name>` |
| F-102 | What the application does / application type | `<purpose and type>` |
| F-103 | Public or private repository | `<visibility>` |
| F-104 | HTTPS clone URL | `<URL>` |
| F-105 | SSH clone URL, if used | `<URL or not applicable>` |
| F-106 | Repository default branch | `<branch>` |
| F-107 | License | `<license or unknown>` |
| F-108 | Supported operating systems | `<OS/platform>` |
| F-109 | Published application or package version | `<version and source>` |
| F-110 | Published release/package URL | `<URL or not applicable>` |
| F-111 | Source manifest version | `<value and source>` |
| F-112 | Assembly version | `<value and source>` |
| F-113 | File version | `<value and source>` |
| F-114 | Consumers or entry points | `<library/API/desktop/service, consumers>` |

### Solutions (repeat one row per solution)

| F-201 Solution path | F-202 Format | F-203 Format version | F-204 Declared IDE version | F-205 Configurations | F-206 Platforms | F-207 Solution membership/build exclusions |
|---|---|---|---|---|---|---|
| `<.sln/.slnx>` | `<format>` | `<value/—>` | `<value/—>` | `<configurations>` | `<platforms>` | `<projects/notes>` |

### Projects (repeat one row per project, including standalone projects)

| F-211 Project path | F-212 Role | F-213 Project format | F-214 Target framework(s) | F-215 Language version | F-216 Output type | F-217 MSBuild Platform | F-218 SDK / ToolsVersion | F-219 Direct project references |
|---|---|---|---|---|---|---|---|---|
| `<project file>` | `<production/test/tool>` | `<SDK-style/traditional>` | `<framework(s)>` | `<version>` | `<output type>` | `<platform>` | `<SDK/version>` | `<paths>` |

## C. Project settings — DISC-003 and DISC-005

Record values declared in source separately from MSBuild-evaluated results. For conditional or multi-targeted properties, add rows showing the project, configuration, platform and framework. Debug and Release are examples, not mandatory configurations.

**Compiler settings (repeat per project and configuration as needed)**

| F-301 Project/configuration | F-302 DebugType | F-303 Optimize | F-304 DefineConstants | F-305 Other compiler settings / conditions |
|---|---|---|---|---|
| `<project/configuration>` | `<value>` | `<value>` | `<value>` | `<details>` |

**Output and validation settings**

| F-311 Project/configuration | F-312 OutputPath | F-313 WarningLevel | F-314 WarningsAsErrors | F-315 DocumentationFile |
|---|---|---|---|---|
| `<project/configuration>` | `<path>` | `<value>` | `<value>` | `<path or not declared>` |

**Project metadata and imports**

| F-321 Project | F-322 Default configuration | F-323 IsTestProject | F-324 FileAlignment | F-325 AppDesignerFolder | F-326 Imports / shared properties |
|---|---|---|---|---|---|
| `<project>` | `<value>` | `<value or —>` | `<value or —>` | `<value or —>` | `<imports or —>` |

**F-327 — Evaluated MSBuild properties and differences:** `<project/configuration/property/result/evidence, or not evaluated>`

## D. Repository folders and configuration — DISC-006

**Directories (repeat as needed)**

| F-401 Directory | F-402 Purpose |
|---|---|
| `<path>` | `<what belongs here>` |

**Configuration files (including files that are absent)**

| F-411 File / mechanism | F-412 Present? | F-413 Current purpose / value | F-414 Scope, imports or precedence |
|---|---|---|---|
| `<path or mechanism>` | `<yes/no/not checked>` | `<settings>` | `<projects/configuration>` |

Check relevant `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, NuGet configuration, `.editorconfig` and nested imports. A missing file does not imply a change is necessary.

## E. Dependencies — DISC-007 and DISC-008

**NuGet declarations (repeat per project/package)**

| F-501 Project | F-502 Package ID | F-503 Version | F-504 Declared in | F-505 Configured feed(s) | F-506 Purpose |
|---|---|---|---|---|---|
| `<project>` | `<package>` | `<declared version>` | `<packages.config/PackageReference/etc.>` | `<sources or not checked>` | `<production/test/tool>` |

**Other dependencies (repeat only when present)**

| F-511 Project/consumer | F-512 Dependency | F-513 Mechanism/type | F-514 Source file | F-515 Version/identity | F-516 Resolution/location |
|---|---|---|---|---|---|
| `<project>` | `<DLL/COM/native/service>` | `<how used>` | `<location declared>` | `<version/identity>` | `<verified or unknown>` |

A configured feed is not proof that a package was restored from it. Keep secrets out of the report.

## F. Build, tests, CI and release — DISC-008 through DISC-012

**Existing commands (record the exact command or entry point found in application documentation/CI)**

| Field | Operation | Command or existing entry point |
|---|---|---|
| F-611 | Restore | `<actual command>` |
| F-612 | Build (configuration/platform) | `<actual command>` |
| F-613 | Full tests | `<actual command>` |
| F-614 | Compatibility checks | `<commands/scripts>` |
| F-615 | Packaging | `<command/workflow or N/A>` |
| F-616 | Consumer/deployment | `<command/workflow or N/A>` |
| F-617 | Alternate host/CI toolchain details | `<host and versions if different>` |

**Test counts and executed artifacts**

| Field | What to fill in | Actual result |
|---|---|---|
| F-621 | Tests discovered | `<number or not executed>` |
| F-622 | Tests passed | `<number or not executed>` |
| F-623 | Tests failed | `<number or not executed>` |
| F-624 | Tests skipped | `<number or not executed>` |
| F-625 | Test projects/assemblies actually executed | `<list or not executed>` |
| F-626 | Build warnings/errors and important outputs | `<summary, links or not executed>` |
| F-627 | CI workflow names, triggers and commands | `<paths and details>` |
| F-628 | CI runs checked and their exact source SHA | `<run IDs / status or not checked>` |
| F-629 | Package contents/metadata and release evidence | `<location and outcome or not checked>` |
| F-630 | Runtime / deployment requirements | `<requirements or not applicable>` |

**Checks and outcomes (include the supporting evidence with each result)**

| Field | Check | Outcome and evidence |
|---|---|---|
| F-701 | Dependency restore | `<pass/fail/blocked/not executed; link>` |
| F-702 | Build | `<result/configuration; link>` |
| F-703 | Automated tests | `<result/test scope; link>` |
| F-704 | Public API | `<result or not applicable; link>` |
| F-705 | Assembly identity | `<result or not applicable; link>` |
| F-706 | Resources | `<result or not applicable; link>` |
| F-707 | XML documentation | `<result or not applicable; link>` |
| F-708 | Package contents | `<result or not applicable; link>` |
| F-709 | Package metadata | `<result or not applicable; link>` |
| F-710 | Dependency validation | `<result or not applicable; link>` |
| F-711 | Vulnerability audit | `<result or not executed; link>` |
| F-712 | Installed-package consumer | `<result or not applicable; link>` |
| F-713 | Application integration checks | `<result or not applicable; link>` |

**Executed commands (repeat one row per actual execution, including failures)**

| F-731 Step | F-732 Exact command, scope and tool | F-733 Result and exit code | F-734 Output / evidence link |
|---|---|---|---|
| `<DISC-###>` | `<command and project/config/host>` | `<result/exit code>` | `<location or not captured>` |

## G. Review and completion — DISC-013 and DISC-014

**Open issues and missing checks (repeat as needed)**

| F-801 Gap or finding | F-802 Impact | F-803 Evidence / next check |
|---|---|---|
| `<missing tool, error, or source-backed fact>` | `<why it matters>` | `<link or next action>` |

**Step completion (one row per DISC step)**

| F-901 Step | F-902 Result/status | F-903 Evidence or missing information |
|---|---|---|
| `<DISC-001…DISC-014>` | `<done/partial/blocked/not executed>` | `<link/notes>` |

| Field | Final review | Result |
|---|---|---|
| F-911 | Overall baseline disposition | `<complete/complete with gaps/further checks needed>` |
| F-912 | Report reviewed by/date | `<reviewer/date or pending>` |
| F-913 | Next action or deferred checks | `<short summary>` |

This form records **what exists and what was observed**. Proposals to modernize the application are separate.
