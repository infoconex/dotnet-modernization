# `<Application>` — Discovery baseline

Copy this **blank baseline** into a dated application discovery folder. Fill in the answers as you follow the [step-by-step instructions](../methodology/technical-discovery-runbook.md). This template contains no actual findings.

- Each number identifies one report field. Keep the same numbers in every copy.
- For solutions, projects, settings, dependencies and commands, add a row for each item; column numbers stay the same.
- Leave fields blank until checked. Use **Not applicable**, **Not checked**, or **Not executed** where appropriate when completing a copy.
- Link actual outputs when available. Don't include passwords or other secrets.

## A. Discovery setup — DISC-001 and DISC-004

**1. Recorder:** `<person performing discovery>`

**2. Recorded Date:** `<YYYY-MM-DD>`

| Field | What to record | Answer |
|---|---|---|
| 3 | Dated discovery folder | `<folder or not yet created>` |
| 4 | Operating system, version/build, architecture | `<actual result>` |
| 5 | PowerShell version (if used) | `<actual result>` |
| 6 | Git version | `<actual result>` |
| 7 | Installed .NET SDKs and runtimes | `<versions or not installed>` |
| 8 | MSBuild / Visual Studio Build Tools version and source | `<actual result>` |
| 9 | Standalone NuGet CLI version | `<actual result>` |
| 10 | Framework targeting packs needed and found | `<versions or check result>` |
| 11 | Test runner and version | `<runner/version or not checked>` |
| 12 | Selected source branch or tag | `<ref>` |
| 13 | Exact source commit SHA | `<full SHA>` |
| 14 | Local checkout status (clean/changes/detached) | `<actual status or not checked>` |
| 15 | Verification date (if distinct from inspection date) | `<date or not executed>` |
| 16 | Overall evidence status | `<verified/partial/blocked/not executed>` |

Link supporting command output from field **115** when a copy is completed.

## B. Application — DISC-002 and DISC-003

| Field | What to fill in | Result |
|---|---|---|
| 17 | Application name | `<name>` |
| 18 | What the application does / application type | `<purpose and type>` |
| 19 | Public or private repository | `<visibility>` |
| 20 | HTTPS clone URL | `<URL>` |
| 21 | SSH clone URL, if used | `<URL or not applicable>` |
| 22 | Repository default branch | `<branch>` |
| 23 | License | `<license or unknown>` |
| 24 | Supported operating systems | `<OS/platform>` |
| 25 | Published application or package version | `<version and source>` |
| 26 | Published release/package URL | `<URL or not applicable>` |
| 27 | Source manifest version | `<value and source>` |
| 28 | Assembly version | `<value and source>` |
| 29 | File version | `<value and source>` |
| 30 | Consumers or entry points | `<library/API/desktop/service, consumers>` |

### Solutions (repeat one row per solution)

| 31 Solution path | 32 Format | 33 Format version | 34 Declared IDE version | 35 Configurations | 36 Platforms | 37 Solution membership/build exclusions |
|---|---|---|---|---|---|---|
| `<.sln/.slnx>` | `<format>` | `<value/—>` | `<value/—>` | `<configurations>` | `<platforms>` | `<projects/notes>` |

### Projects (repeat one row per project, including standalone projects)

| 38 Project path | 39 Role | 40 Project format | 41 Target framework(s) | 42 Language version | 43 Output type | 44 MSBuild Platform | 45 SDK / ToolsVersion | 46 Direct project references |
|---|---|---|---|---|---|---|---|---|
| `<project file>` | `<production/test/tool>` | `<SDK-style/traditional>` | `<framework(s)>` | `<version>` | `<output type>` | `<platform>` | `<SDK/version>` | `<paths>` |

## C. Project settings — DISC-003 and DISC-005

Record values declared in source separately from MSBuild-evaluated results. For conditional or multi-targeted properties, add rows showing the project, configuration, platform and framework. Debug and Release are examples, not mandatory configurations.

**Compiler settings (repeat per project and configuration as needed)**

| 47 Project/configuration | 48 DebugType | 49 Optimize | 50 DefineConstants | 51 Other compiler settings / conditions |
|---|---|---|---|---|
| `<project/configuration>` | `<value>` | `<value>` | `<value>` | `<details>` |

**Output and validation settings**

| 52 Project/configuration | 53 OutputPath | 54 WarningLevel | 55 WarningsAsErrors | 56 DocumentationFile |
|---|---|---|---|---|
| `<project/configuration>` | `<path>` | `<value>` | `<value>` | `<path or not declared>` |

**Project metadata and imports**

| 57 Project | 58 Default configuration | 59 IsTestProject | 60 FileAlignment | 61 AppDesignerFolder | 62 Imports / shared properties |
|---|---|---|---|---|---|
| `<project>` | `<value>` | `<value or —>` | `<value or —>` | `<value or —>` | `<imports or —>` |

**63 — Evaluated MSBuild properties and differences:** `<project/configuration/property/result/evidence, or not evaluated>`

## D. Repository folders and configuration — DISC-006

**Directories (repeat as needed)**

| 64 Directory | 65 Purpose |
|---|---|
| `<path>` | `<what belongs here>` |

**Configuration files (including files that are absent)**

| 66 File / mechanism | 67 Present? | 68 Current purpose / value | 69 Scope, imports or precedence |
|---|---|---|---|
| `<path or mechanism>` | `<yes/no/not checked>` | `<settings>` | `<projects/configuration>` |

Check relevant `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, NuGet configuration, `.editorconfig` and nested imports. A missing file does not imply a change is necessary.

## E. Dependencies — DISC-007 and DISC-008

**NuGet declarations (repeat per project/package)**

| 70 Project | 71 Package ID | 72 Version | 73 Declared in | 74 Configured feed(s) | 75 Purpose |
|---|---|---|---|---|---|
| `<project>` | `<package>` | `<declared version>` | `<packages.config/PackageReference/etc.>` | `<sources or not checked>` | `<production/test/tool>` |

**Other dependencies (repeat only when present)**

| 76 Project/consumer | 77 Dependency | 78 Mechanism/type | 79 Source file | 80 Version/identity | 81 Resolution/location |
|---|---|---|---|---|---|
| `<project>` | `<DLL/COM/native/service>` | `<how used>` | `<location declared>` | `<version/identity>` | `<verified or unknown>` |

A configured feed is not proof that a package was restored from it. Keep secrets out of the report.

## F. Build, tests, CI and release — DISC-008 through DISC-012

**Existing commands (record the exact command or entry point found in application documentation/CI)**

| Field | Operation | Command or existing entry point |
|---|---|---|
| 82 | Restore | `<actual command>` |
| 83 | Build (configuration/platform) | `<actual command>` |
| 84 | Full tests | `<actual command>` |
| 85 | Compatibility checks | `<commands/scripts>` |
| 86 | Packaging | `<command/workflow or N/A>` |
| 87 | Consumer/deployment | `<command/workflow or N/A>` |
| 88 | Alternate host/CI toolchain details | `<host and versions if different>` |

**Test counts and executed artifacts**

| Field | What to fill in | Actual result |
|---|---|---|
| 89 | Tests discovered | `<number or not executed>` |
| 90 | Tests passed | `<number or not executed>` |
| 91 | Tests failed | `<number or not executed>` |
| 92 | Tests skipped | `<number or not executed>` |
| 93 | Test projects/assemblies actually executed | `<list or not executed>` |
| 94 | Build warnings/errors and important outputs | `<summary, links or not executed>` |
| 95 | CI workflow names, triggers and commands | `<paths and details>` |
| 96 | CI runs checked and their exact source SHA | `<run IDs / status or not checked>` |
| 97 | Package contents/metadata and release evidence | `<location and outcome or not checked>` |
| 98 | Runtime / deployment requirements | `<requirements or not applicable>` |

**Checks and outcomes (include the supporting evidence with each result)**

| Field | Check | Outcome and evidence |
|---|---|---|
| 99 | Dependency restore | `<pass/fail/blocked/not executed; link>` |
| 100 | Build | `<result/configuration; link>` |
| 101 | Automated tests | `<result/test scope; link>` |
| 102 | Public API | `<result or not applicable; link>` |
| 103 | Assembly identity | `<result or not applicable; link>` |
| 104 | Resources | `<result or not applicable; link>` |
| 105 | XML documentation | `<result or not applicable; link>` |
| 106 | Package contents | `<result or not applicable; link>` |
| 107 | Package metadata | `<result or not applicable; link>` |
| 108 | Dependency validation | `<result or not applicable; link>` |
| 109 | Vulnerability audit | `<result or not executed; link>` |
| 110 | Installed-package consumer | `<result or not applicable; link>` |
| 111 | Application integration checks | `<result or not applicable; link>` |

**Executed commands (repeat one row per actual execution, including failures)**

| 112 Step | 113 Exact command, scope and tool | 114 Result and exit code | 115 Output / evidence link |
|---|---|---|---|
| `<DISC-###>` | `<command and project/config/host>` | `<result/exit code>` | `<location or not captured>` |

## G. Review and completion — DISC-013 and DISC-014

**Open issues and missing checks (repeat as needed)**

| 116 Gap or finding | 117 Impact | 118 Evidence / next check |
|---|---|---|
| `<missing tool, error, or source-backed fact>` | `<why it matters>` | `<link or next action>` |

**Step completion (one row per DISC step)**

| 119 Step | 120 Result/status | 121 Evidence or missing information |
|---|---|---|
| `<DISC-001…DISC-014>` | `<done/partial/blocked/not executed>` | `<link/notes>` |

| Field | Final review | Result |
|---|---|---|
| 122 | Overall baseline disposition | `<complete/complete with gaps/further checks needed>` |
| 123 | Report reviewed by/date | `<reviewer/date or pending>` |
| 124 | Next action or deferred checks | `<short summary>` |

Complete a copied baseline using observed facts only. Modernization proposals belong in separate documents.
