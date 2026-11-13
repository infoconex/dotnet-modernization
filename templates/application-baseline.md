# `<Application Name>` — Discovery baseline

**Description:** `<Application description>`

[Step-by-Step Instructions](../methodology/technical-discovery-runbook.md)

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By |  |
| 2. Discovery Date |  |
| 3. Discovery Status |  |
| 4. Discovery Completed Date |  |

**Status guidance:** Use `Not started`, `In progress`, `Blocked`, `Completed` or `Completed with gaps`. Enter `Discovery Completed Date` in `YYYY-MM-DD` only after completion and review; otherwise use `Not completed`. Keep the overall disposition (item 61), reviewer (item 62), review date (item 63) and outstanding checks consistent with this summary. Discovery dates are distinct from source commit, CI and publication dates.

## Application information

| Field | Value |
|---|---|
| 5. Application Type |  |
| 6. Repository Visibility |  |
| 7. License |  |
| 8. Supported Operating Systems |  |
| 9. HTTPS Clone URL |  |
| 10. SSH Clone URL |  |
| 11. Repository Default Branch |  |
| 12. Published Application Version |  |
| 13. Published Package Version |  |
| 14. Published Release URL |  |
| 15. Published Package URL |  |
| 16. Source Manifest Version |  |
| 17. Assembly Version |  |
| 18. File Version |  |

### 19. Consumers and Entry Points

| Consumer or Entry Point | Type | Source or Evidence |
|---|---|---|
|   |   |   |


## Discovery host and prerequisite tools

| Field | Value |
|---|---|
| 20. Operating System Name |  |
| 21. Operating System Version |  |
| 22. Operating System Build |  |
| 23. Operating System Architecture |  |
| 24. PowerShell Version |  |
| 25. Git Version |  |

### 26. .NET SDK Inventory

| SDK Version | Installation Path |
|---|---|
|   |   |

### 27. .NET Runtime Inventory

| Runtime Name | Runtime Version | Installation Path |
|---|---|---|
|   |   |   |

| Field | Value |
|---|---|
| 28. MSBuild Version |  |
| 29. MSBuild Installation Source |  |
| 30. NuGet CLI Version |  |

### 31. .NET Framework Targeting Pack Inventory

| Framework Version | Installed | Location |
|---|---|---|
|   |   |   |

### 32. Test Runner Inventory

| Runner Name | Runner Version | Source or Location |
|---|---|---|
|   |   |   |

## Source revision and checkout

| Field | Value |
|---|---|
| 33. Discovery Folder |  |
| 34. Selected Source Branch or Tag |  |
| 35. Source Commit SHA |  |
| 36. Source Committer Date (UTC) |  |
| 37. Working Tree Clean |  |
| 38. Detached HEAD |  |

**36. Source Committer Date (UTC)** is a numbered field immediately after item 35: record the Git committer timestamp for the exact selected commit in UTC ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`), not the discovery date, checkout time, author date, push date or release publication date. Record evidence separately. Keep item 35's SHA value atomic and retain the same source provenance in item 55.

## Solution and project inventory

### 39. Solutions

Prefer one row per solution. Group configurations and platforms only when their **valid pairings**, project-build mappings and exclusions can be recorded without ambiguity; state conditional differences in the last column or use separate scoped rows when needed. Listed names alone do not prove every configuration/platform combination exists.

| Solution Path | Format | Format Version | Declared IDE Version | Configurations | Platforms | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

### 40. Projects

One row per project wherever possible. Use project name first (link to the project file when available), group direct references by name, and put the repository-relative project file path last **in this authoritative inventory**. Subsequent project tables use linked names and omit repeated path columns. Preserve all frameworks/platforms and split only when differences cannot be represented unambiguously.

| Project | Role | Format | Target Framework(s) | Language Version | Output Type | MSBuild Platform(s) | SDK or ToolsVersion | Direct Project References | Project Path |
|---|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |   |

## Project settings and evaluated values

### 41. Compiler Settings

One row per project whenever possible. D/R means Debug/Release in that order; show one value when both have identical declarations. `Not declared` is not an evaluated default. Document shared exact conditions once; label exceptions or additional configurations and properties explicitly.

| Project | Framework(s) | LangVersion | DebugSymbols (D/R) | DebugType (D/R) | Optimize (D/R) | DefineConstants (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 42. Output and Validation Settings

One row per project when practical. Use Debug/Release values where declarations differ, one value where identical, and `Not declared` where absent; do not infer evaluated defaults. Preserve other properties and exceptional conditions.

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 43. Project Metadata and Imports

One row per project. Give each named metadata property a column and list distinct imports together. **Configuration Fallback** is a source-declared value used when `$(Configuration)` is empty, not a verified evaluated/build configuration; record its condition where relevant. `Not declared` means absent from project source, not evaluated false. Preserve exceptional conditional/import scope.

| Project | Configuration Fallback | IsTestProject | FileAlignment | AppDesignerFolder | Imports | Additional Metadata / Conditions |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

### 44. Evaluated MSBuild Properties

One row per project when possible. Enter only observed evaluated values, labeled by configuration/platform/framework, and distinguish source declarations from evaluated outputs. Link exact command/output; do not populate from XML or successful build alone.

| Project | Configuration / Framework / Platform | Evaluated Properties (name=value) | Declared Properties for Comparison | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

## Repository structure and dependencies

### 45. Repository Directories

| Directory | Purpose |
|---|---|
|   |   |

### 46. Repository Configuration

Record **declared source settings** in the table, including NuGet `clear` directives and explicitly disabled feeds. Summarize absent NuGet configuration sections once rather than adding empty rows. **Effective** user/machine/CLI settings are separate and remain `Not checked` until verified. Never record secrets; follow step 46 in the [runbook](../methodology/technical-discovery-runbook.md).

| File or Mechanism | Present | Scope | Setting Name | Setting Value | Import or Precedence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**NuGet sections not declared in inspected source:** 

**Effective NuGet configuration:** Not checked

### 47. NuGet Package Declarations

Capture each declared package **ID and exact version** and all consuming projects without adding inferred package classifications. Use the project inventory in item 40 for canonical project paths; link each unique project name to its source here. Keep project-level counts in A and one row per distinct package ID/version in B. Preserve package-specific declaration attributes (for example `developmentDependency`, target framework or conditions) in a short note or additional evidence column if material. Separate source-declared eligible feeds from effective package acquisition, which requires independent verification.

**A. Packages by project**

| Project | Package Count | Declaration Source | Configured Feed(s) |
|---|---:|---|---|
|   |   |   |   |

**B. Package catalog**

| Package ID | Version | Referenced By | Declaration Source(s) | Configured Feed(s) |
|---|---|---|---|---|
|   |   |   |   |   |

**Additional declared package metadata and unresolved restore verification:**


### 48. Non-NuGet Dependencies

Separate **framework assembly references** from **other non-NuGet dependencies**. Project references are in item 40 and NuGet-managed dependencies in item 47. Use linked project names first and authoritative paths from item 40 rather than repeating path columns; preserve exact names, mechanisms, versions, source/conditions and resolution evidence. `Not declared` is not `Not checked`, and missing project declarations do not establish the absence of runtime or dynamically loaded dependencies.

**A. Framework Assembly References**

| Project | Framework References | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**B. Other Non-NuGet Dependencies**

Examples include native libraries, COM components, non-NuGet third-party assemblies and external service dependencies. If no declarations are found, write an explicit source-scoped finding **below** the table and identify outstanding runtime checks; do not invent a dependency or use `None` to mean that checks were not performed.

| Project | Dependencies | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source |
|---|---|---|---|---|---|

*Source-inspection result and unresolved runtime checks:*


## Restore, build, tests and delivery

### 49. Operation Commands

| Operation | Project or Solution | Configuration | Platform | Command or Workflow | Source |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 50. Restore Outcomes

| Source Revision | Target | Outcome | Error or Note | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

### 51. Build Outcomes

| Source Revision | Target | Configuration | Platform | Outcome | Warning Count | Error Count | Output or Evidence |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 52. Test Outcomes

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

### 53. CI Workflows

Record one row per distinct **workflow + job/stage + configured command + runner/output** and group only the event triggers under which that same record applies. Distinct jobs, branch or event conditions, runner types, commands, output artifacts, approvals, deployment gates and workflow dependencies must not disappear through grouping. Link workflow paths to pinned source when practical. This table is an inventory of **configured commands**, not execution evidence; its selected command excerpts need not represent every step in the workflow.

| Workflow Path | Trigger(s) | Job / Stage | Runner OS | Configured Command | Artifact or Deployment |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**Trigger conditions, job dependencies and deployment/approval gates:**

**Observed CI execution evidence (separate from source declarations):**


### 54. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
|   |   |   |   |   |

### 55. Package and Release Artifacts

Keep source declarations, CI-produced artifacts and **independent published distributions** in separate tables. Use **one meaningful UTC date/time per row**, labeling the event; do not turn an upload attempt, upload acceptance or source commit timestamp into a confirmed publication timestamp. Use `YYYY-MM-DDTHH:MM:SSZ` for verified exact UTC timestamps and `YYYY-MM-DD` only when a day is verified but the exact time is not. Include direct evidence links, and do not claim CI evidence is a new operator execution.

**A. Source package declarations**

| Declaration | Declared Version | Source Committer Date (UTC) | Evidence |
|---|---|---|---|
|   |   |   |   |

**B. CI package artifacts and verification**

| Artifact | Version | Verification Result | Verification Completed (UTC) | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

**C. Published artifacts**

| Artifact | Version | Status | Publication Date (UTC) | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

Keep **NuGet package** and **GitHub release** as distinct rows even when they share version numbers. If only the publication day can be established, label the precision. If the date itself is unavailable, record `Not checked` rather than substituting another distribution's timestamp or an upload-acceptance date.

**Source revision provenance**

| Source Context | Source Commit SHA | Committer Date (UTC) | Verification |
|---|---|---|---|
|   |   |   |   |

Git committer dates are not guaranteed source creation or push times, and neither commit timestamps nor CI verification timestamps are publication dates. Preserve exact source-commit provenance and evidence separately from the artifact dates.

**Package provenance and verification limits:**
### 56. Runtime and Deployment Requirements

| Requirement | Type | Target Environment | Source or Evidence |
|---|---|---|---|
|   |   |   |   |

### 57. Compatibility Checks

| Check Type | Target | Method or Command | Outcome | Commit SHA | Evidence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

## Evidence and completion

### 58. Executed Command Evidence

| Baseline Item | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 59. Findings and Gaps

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
|   |   |   |   |

### 60. Discovery Item Status

Create **one row for every numbered baseline item (1–65)** and track evidence channels independently. The dimensions below refer to what was actually inspected or executed; they do **not** imply that all required discovery work has been completed. Preserve the original evidence IDs, links, missing information, and unresolved checks in the last column.

**Status meanings:** **Source Inspection:** `Verified` (exact source, external public metadata, repository metadata or documented discovery facts checked), `Partial` (source evidence available but material checks still open), `Not checked`, `Not applicable`. **Existing CI:** `Passed` (relevant checks completed successfully on a documented SHA), `Verified` (CI log/run evidence inspected), `Not checked`, `Not applicable`. **Operator Local:** `Passed` / `Failed` (actually executed by operator, with evidence), `Not executed` (check required but not run), `Not recorded` (operator-supplied information missing), `Not applicable` (no operator-local check is required for this particular item). For any relevant failure, record details in evidence; never relabel CI success as local success.

| Baseline Item | Source Inspection | Existing CI | Operator Local | Evidence or Missing Information |
|---|---|---|---|---|
|   |   |   |   |   |

**Unresolved operator checks and review status:**

| Field | Value |
|---|---|
| 61. Overall Baseline Disposition |  |
| 62. Reviewed By |  |
| 63. Review Date |  |
| 64. Next Action |  |

### 65. Deferred Checks

| Check | Reason Deferred | Revisit When |
|---|---|---|
|   |   |   |

This baseline records observed application facts and verification outcomes, not proposed modernization work.
