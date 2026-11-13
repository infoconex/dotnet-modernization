# RecordSift — Technical discovery report

This is the working RecordSift discovery report for **source commit `1809d06c0fade59e4769d16e0f8eaf10fa426004`**. The operator follows the [step-by-step guide](../../../../../methodology/technical-discovery-runbook.md) on Windows and shares results. The assistant fills this form using those results.

**Current status:** GitHub source-only inspection (November 12, 2026); **no user-run local commands, tool-version checks, restore, build or tests have been received**. Historical evaluations use different source revisions.

- **Every field has a permanent ID**, such as `F-006` for Git version. The guide uses these same IDs.
- **One answer per field.** For project, solution, package and execution tables, use a new row for each item; each column keeps the same field ID. Identify the item by its project/path/name.
- Leave unanswered fields as **Not checked**, **Not executed** or **Not applicable**. Do not copy results from an older source revision as new results.
- Link to actual output or relevant excerpts, and avoid secrets/personal paths. See the [variation guide](../../../../methodology/baseline-variation-guide.md) when builds have conditional settings or multiple frameworks.
- This records facts, not modernization recommendations.

## A. Discovery setup — DISC-001 and DISC-004

| Field | What to fill in | Result |
|---|---|---|
| F-001 | Person or system performing discovery | Not checked |
| F-002 | Discovery date, time and time zone | Not checked |
| F-003 | Dated discovery folder | Not checked |
| F-004 | Operating system, version/build, architecture | Not checked |
| F-005 | PowerShell version (if used) | Not checked |
| F-006 | Git version | Not checked |
| F-007 | Installed .NET SDKs and runtimes | Not checked |
| F-008 | MSBuild / Visual Studio Build Tools version and source | Not checked |
| F-009 | Standalone NuGet CLI version | Not checked |
| F-010 | Framework targeting packs needed and found | Not checked |
| F-011 | Test runner and version | Not checked |
| F-012 | Selected source branch or tag | `main` — GitHub observed, local checkout pending |
| F-013 | Exact source commit SHA | [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) — selected source SHA, **local checkout not verified** |
| F-014 | Local checkout status (clean/changes/detached) | Not checked |
| F-015 | Verification date (if distinct from inspection date) | Not checked |
| F-016 | Overall evidence status | Partial — source-only GitHub inspection; local execution pending |

**Evidence for prerequisites and checkout:** [EV-001–003](evidence/manifest.md) for GitHub source preflight only; local command output not available.

## B. Application — DISC-002 and DISC-003

| Field | What to fill in | Result |
|---|---|---|
| F-101 | Application name | RecordSift |
| F-102 | What the application does / application type | Windows/.NET Framework 4.8 CSV/XLSX import, validation and reporting library — source README |
| F-103 | Public or private repository | Public GitHub repository (source inspected) |
| F-104 | HTTPS clone URL | `https://github.com/infoconex/RecordSift.git` |
| F-105 | SSH clone URL, if used | Not checked |
| F-106 | Repository default branch | `main` (observed November 12, 2026) |
| F-107 | License | MIT — source README |
| F-108 | Supported operating systems | Windows — source README; operator Windows version not checked |
| F-109 | Published application or package version | 0.1.0 — described as published in source README; not independently verified |
| F-110 | Published release/package URL | Not checked |
| F-111 | Source manifest version | Not checked |
| F-112 | Assembly version | Not checked |
| F-113 | File version | Not checked |
| F-114 | Consumers or entry points | Not checked |

### Solutions (repeat one row per solution)

| F-201 Solution path | F-202 Format | F-203 Format version | F-204 Declared IDE version | F-205 Configurations | F-206 Platforms | F-207 Solution membership/build exclusions |
|---|---|---|---|---|---|---|
| `RecordSift.sln` — [EV-002](evidence/manifest.md) | Not checked | Not checked | Not checked | Not checked | Not checked | Membership not checked |

### Projects (repeat one row per project, including standalone projects)

| F-211 Project path | F-212 Role | F-213 Project format | F-214 Target framework(s) | F-215 Language version | F-216 Output type | F-217 MSBuild Platform | F-218 SDK / ToolsVersion | F-219 Direct project references |
|---|---|---|---|---|---|---|---|---|
| `src/RecordSift.Domain/RecordSift.Domain.csproj` — [EV-002](evidence/manifest.md) | production path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `src/RecordSift.Application/RecordSift.Application.csproj` — [EV-002](evidence/manifest.md) | production path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj` — [EV-002](evidence/manifest.md) | production path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj` — [EV-002](evidence/manifest.md) | production path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj` — [EV-002](evidence/manifest.md) | production path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj` — [EV-002](evidence/manifest.md) | test path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj` — [EV-002](evidence/manifest.md) | test path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj` — [EV-002](evidence/manifest.md) | test path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj` — [EV-002](evidence/manifest.md) | test path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |
| `tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj` — [EV-002](evidence/manifest.md) | test path (inferred) | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |

## C. Project settings — DISC-003 and DISC-005

Record values declared in source separately from MSBuild-evaluated results. For conditional or multi-targeted properties, add rows showing the project, configuration, platform and framework. Debug and Release are examples, not mandatory configurations.

**Compiler settings (repeat per project and configuration as needed)**

| F-301 Project/configuration | F-302 DebugType | F-303 Optimize | F-304 DefineConstants | F-305 Other compiler settings / conditions |
|---|---|---|---|---|
| Not checked | Not checked | Not checked | Not checked | Not checked |

**Output and validation settings**

| F-311 Project/configuration | F-312 OutputPath | F-313 WarningLevel | F-314 WarningsAsErrors | F-315 DocumentationFile |
|---|---|---|---|---|
| Not checked | Not checked | Not checked | Not checked | Not checked |

**Project metadata and imports**

| F-321 Project | F-322 Default configuration | F-323 IsTestProject | F-324 FileAlignment | F-325 AppDesignerFolder | F-326 Imports / shared properties |
|---|---|---|---|---|---|
| Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |

**F-327 — Evaluated MSBuild properties and differences:** Not checked

## D. Repository folders and configuration — DISC-006

**Directories (repeat as needed)**

| F-401 Directory | F-402 Purpose |
|---|---|
| `src` | production project files found — [EV-002](evidence/manifest.md) |
| `tests` | test project files found — [EV-002](evidence/manifest.md) |

**Configuration files (including files that are absent)**

| F-411 File / mechanism | F-412 Present? | F-413 Current purpose / value | F-414 Scope, imports or precedence |
|---|---|---|---|
| `.editorconfig` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `NuGet.Config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `src/RecordSift.Infrastructure.Csv/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `src/RecordSift.Infrastructure.Xlsx/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `tests/RecordSift.Application.Tests/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `tests/RecordSift.Domain.Tests/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `tests/RecordSift.Infrastructure.Csv.Tests/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `tests/RecordSift.Infrastructure.Reporting.Tests/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `tests/RecordSift.Infrastructure.Xlsx.Tests/packages.config` | Yes, tracked at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `global.json` | No tracked root file at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `Directory.Build.props` | No tracked root file at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `Directory.Build.targets` | No tracked root file at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |
| `Directory.Packages.props` | No tracked root file at frozen SHA | Contents not checked | Scope/imports not checked — [EV-002](evidence/manifest.md) |

Check relevant `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, NuGet configuration, `.editorconfig` and nested imports. A missing file does not imply a change is necessary.

## E. Dependencies — DISC-007 and DISC-008

**NuGet declarations (repeat per project/package)**

| F-501 Project | F-502 Package ID | F-503 Version | F-504 Declared in | F-505 Configured feed(s) | F-506 Purpose |
|---|---|---|---|---|---|
| Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |

**Other dependencies (repeat only when present)**

| F-511 Project/consumer | F-512 Dependency | F-513 Mechanism/type | F-514 Source file | F-515 Version/identity | F-516 Resolution/location |
|---|---|---|---|---|---|
| Not checked | Not checked | Not checked | Not checked | Not checked | Not checked |

A configured feed is not proof that a package was restored from it. Keep secrets out of the report.

## F. Build, tests, CI and release — DISC-008 through DISC-012

**Existing commands (record the exact command or entry point found in application documentation/CI)**

| Field | Operation | Command or existing entry point |
|---|---|---|
| F-611 | Restore | Not checked |
| F-612 | Build (configuration/platform) | Not checked |
| F-613 | Full tests | Not checked |
| F-614 | Compatibility checks | Not checked |
| F-615 | Packaging | Not checked |
| F-616 | Consumer/deployment | Not checked |
| F-617 | Alternate host/CI toolchain details | Not checked |

**Test counts and executed artifacts**

| Field | What to fill in | Actual result |
|---|---|---|
| F-621 | Tests discovered | Not checked |
| F-622 | Tests passed | Not checked |
| F-623 | Tests failed | Not checked |
| F-624 | Tests skipped | Not checked |
| F-625 | Test projects/assemblies actually executed | Not checked |
| F-626 | Build warnings/errors and important outputs | Not checked |
| F-627 | CI workflow names, triggers and commands | Not checked |
| F-628 | CI runs checked and their exact source SHA | Not checked |
| F-629 | Package contents/metadata and release evidence | Not checked |
| F-630 | Runtime / deployment requirements | Not checked |

**Checks and outcomes (include the supporting evidence with each result)**

| Field | Check | Outcome and evidence |
|---|---|---|
| F-701 | Dependency restore | Not checked |
| F-702 | Build | Not checked |
| F-703 | Automated tests | Not checked |
| F-704 | Public API | Not checked |
| F-705 | Assembly identity | Not checked |
| F-706 | Resources | Not checked |
| F-707 | XML documentation | Not checked |
| F-708 | Package contents | Not checked |
| F-709 | Package metadata | Not checked |
| F-710 | Dependency validation | Not checked |
| F-711 | Vulnerability audit | Not checked |
| F-712 | Installed-package consumer | Not checked |
| F-713 | Application integration checks | Not checked |

**Executed commands (repeat one row per actual execution, including failures)**

| F-731 Step | F-732 Exact command, scope and tool | F-733 Result and exit code | F-734 Output / evidence link |
|---|---|---|---|
| Not executed | Not executed | Not executed | No local output available |

## G. Review and completion — DISC-013 and DISC-014

**Open issues and missing checks (repeat as needed)**

| F-801 Gap or finding | F-802 Impact | F-803 Evidence / next check |
|---|---|---|
| Operator tools and local checkout not checked | Restore, build and tests remain unexecuted | Complete DISC-001 first; GitHub source preflight [EV-001–003](evidence/manifest.md) |

**Step completion (one row per DISC step)**

| F-901 Step | F-902 Result/status | F-903 Evidence or missing information |
|---|---|---|
| `DISC-001` | Not executed in this evaluation | Pending user-run results |
| `DISC-002` | Partial — GitHub tracked-path preflight only | [EV-002](evidence/manifest.md), no local verification |
| `DISC-003` | Not executed in this evaluation | Pending user-run results |
| `DISC-004` | Not executed in this evaluation | Pending user-run results |
| `DISC-005` | Not executed in this evaluation | Pending user-run results |
| `DISC-006` | Partial — GitHub tracked-path preflight only | [EV-002](evidence/manifest.md), no local verification |
| `DISC-007` | Not executed in this evaluation | Pending user-run results |
| `DISC-008` | Not executed in this evaluation | Pending user-run results |
| `DISC-009` | Not executed in this evaluation | Pending user-run results |
| `DISC-010` | Not executed in this evaluation | Pending user-run results |
| `DISC-011` | Partial — GitHub tracked-path preflight only | [EV-002](evidence/manifest.md), no local verification |
| `DISC-012` | Not executed in this evaluation | Pending user-run results |
| `DISC-013` | Not executed in this evaluation | Pending user-run results |
| `DISC-014` | Not executed in this evaluation | Pending user-run results |

| Field | Final review | Result |
|---|---|---|
| F-911 | Overall baseline disposition | Further checks needed — user-run discovery not started |
| F-912 | Report reviewed by/date | Not checked |
| F-913 | Next action or deferred checks | DISC-001: Windows prerequisites, dated fresh clone and exact SHA verification |

This form records **what exists and what was observed**. Proposals to modernize the application are separate.

## Initial source inspection (not a user-run discovery)

- **Source:** [RecordSift at frozen SHA](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004)
- **Date/method:** November 12, 2026, assistant inspection via connected GitHub
- **Established from tracked tree:** one solution, ten C# project paths, seven tracked `packages.config` files, root `NuGet.Config`, root `.editorconfig`, and eight workflow definitions. See [EV-001–003](evidence/manifest.md).
- **Not established:** operator Windows version, tool versions, a local clean checkout, evaluated MSBuild properties, dependency restore or test/build success.
