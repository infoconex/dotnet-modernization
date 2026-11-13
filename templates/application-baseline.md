# `<Application Name>` — Discovery baseline

**Description:** `<Application description>`

[Step-by-Step Instructions](../methodology/technical-discovery-runbook.md)

## Application information

| Field | Value |
|---|---|
| 1. Application Type |  |
| 2. Repository Visibility |  |
| 3. License |  |
| 4. Supported Operating Systems |  |
| 5. HTTPS Clone URL |  |
| 6. SSH Clone URL |  |
| 7. Repository Default Branch |  |
| 8. Published Application Version |  |
| 9. Published Package Version |  |
| 10. Published Release URL |  |
| 11. Published Package URL |  |
| 12. Source Manifest Version |  |
| 13. Assembly Version |  |
| 14. File Version |  |

### 15. Consumers and Entry Points

| Consumer or Entry Point | Type | Source or Evidence |
|---|---|---|
|   |   |   |

## Discovery information

| Field | Value |
|---|---|
| 16. Discovery By |  |
| 17. Discovery Date |  |

## Discovery host and prerequisite tools

| Field | Value |
|---|---|
| 18. Operating System Name |  |
| 19. Operating System Version |  |
| 20. Operating System Build |  |
| 21. Operating System Architecture |  |
| 22. PowerShell Version |  |
| 23. Git Version |  |

### 24. .NET SDK Inventory

| SDK Version | Installation Path |
|---|---|
|   |   |

### 25. .NET Runtime Inventory

| Runtime Name | Runtime Version | Installation Path |
|---|---|---|
|   |   |   |

| Field | Value |
|---|---|
| 26. MSBuild Version |  |
| 27. MSBuild Installation Source |  |
| 28. NuGet CLI Version |  |

### 29. .NET Framework Targeting Pack Inventory

| Framework Version | Installed | Location |
|---|---|---|
|   |   |   |

### 30. Test Runner Inventory

| Runner Name | Runner Version | Source or Location |
|---|---|---|
|   |   |   |

## Source revision and checkout

| Field | Value |
|---|---|
| 31. Discovery Folder |  |
| 32. Selected Source Branch or Tag |  |
| 33. Source Commit SHA |  |
| 34. Working Tree Clean |  |
| 35. Detached HEAD |  |

## Solution and project inventory

### 36. Solutions

Prefer one row per solution. Group configurations and platforms only when their **valid pairings**, project-build mappings and exclusions can be recorded without ambiguity; state conditional differences in the last column or use separate scoped rows when needed. Listed names alone do not prove every configuration/platform combination exists.

| Solution Path | Format | Format Version | Declared IDE Version | Configurations | Platforms | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

### 37. Projects

One row per project wherever possible. Use project name first (link to the project file when available), group direct references by name, and put the repository-relative project file path last **in this authoritative inventory**. Subsequent project tables use linked names and omit repeated path columns. Preserve all frameworks/platforms and split only when differences cannot be represented unambiguously.

| Project | Role | Format | Target Framework(s) | Language Version | Output Type | MSBuild Platform(s) | SDK or ToolsVersion | Direct Project References | Project Path |
|---|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |   |

## Project settings and evaluated values

### 38. Compiler Settings

One row per project whenever possible. D/R means Debug/Release in that order; show one value when both have identical declarations. `Not declared` is not an evaluated default. Document shared exact conditions once; label exceptions or additional configurations and properties explicitly.

| Project | Framework(s) | LangVersion | DebugSymbols (D/R) | DebugType (D/R) | Optimize (D/R) | DefineConstants (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 39. Output and Validation Settings

One row per project when practical. Use Debug/Release values where declarations differ, one value where identical, and `Not declared` where absent; do not infer evaluated defaults. Preserve other properties and exceptional conditions.

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 40. Project Metadata and Imports

One row per project. Give each named metadata property a column and list distinct imports together. **Configuration Fallback** is a source-declared value used when `$(Configuration)` is empty, not a verified evaluated/build configuration; record its condition where relevant. `Not declared` means absent from project source, not evaluated false. Preserve exceptional conditional/import scope.

| Project | Configuration Fallback | IsTestProject | FileAlignment | AppDesignerFolder | Imports | Additional Metadata / Conditions |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

### 41. Evaluated MSBuild Properties

One row per project when possible. Enter only observed evaluated values, labeled by configuration/platform/framework, and distinguish source declarations from evaluated outputs. Link exact command/output; do not populate from XML or successful build alone.

| Project | Configuration / Framework / Platform | Evaluated Properties (name=value) | Declared Properties for Comparison | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

## Repository structure and dependencies

### 42. Repository Directories

| Directory | Purpose |
|---|---|
|   |   |

### 43. Repository Configuration

Record **declared source settings** in the table, including NuGet `clear` directives and explicitly disabled feeds. Summarize absent NuGet configuration sections once rather than adding empty rows. **Effective** user/machine/CLI settings are separate and remain `Not checked` until verified. Never record secrets; follow step 43 in the [runbook](../methodology/technical-discovery-runbook.md).

| File or Mechanism | Present | Scope | Setting Name | Setting Value | Import or Precedence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**NuGet sections not declared in inspected source:** 

**Effective NuGet configuration:** Not checked

### 44. NuGet Package Declarations

Capture each declared package **ID and exact version** and all consuming projects without adding inferred package classifications. Use the project inventory in item 37 for canonical project paths; link each unique project name to its source here. Keep project-level counts in A and one row per distinct package ID/version in B. Preserve package-specific declaration attributes (for example `developmentDependency`, target framework or conditions) in a short note or additional evidence column if material. Separate source-declared eligible feeds from effective package acquisition, which requires independent verification.

**A. Packages by project**

| Project | Package Count | Declaration Source | Configured Feed(s) |
|---|---:|---|---|
|   |   |   |   |

**B. Package catalog**

| Package ID | Version | Referenced By | Declaration Source(s) | Configured Feed(s) |
|---|---|---|---|---|
|   |   |   |   |   |

**Additional declared package metadata and unresolved restore verification:**


### 45. Non-NuGet Dependencies

Separate **framework assembly references** from **other non-NuGet dependencies**. Project references are in item 37 and NuGet-managed dependencies in item 44. Use linked project names first and authoritative paths from item 37 rather than repeating path columns; preserve exact names, mechanisms, versions, source/conditions and resolution evidence. `Not declared` is not `Not checked`, and missing project declarations do not establish the absence of runtime or dynamically loaded dependencies.

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

### 46. Operation Commands

| Operation | Project or Solution | Configuration | Platform | Command or Workflow | Source |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 47. Restore Outcomes

| Source Revision | Target | Outcome | Error or Note | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

### 48. Build Outcomes

| Source Revision | Target | Configuration | Platform | Outcome | Warning Count | Error Count | Output or Evidence |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 49. Test Outcomes

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

### 50. CI Workflows

Record one row per distinct **workflow + job/stage + configured command + runner/output** and group only the event triggers under which that same record applies. Distinct jobs, branch or event conditions, runner types, commands, output artifacts, approvals, deployment gates and workflow dependencies must not disappear through grouping. Link workflow paths to pinned source when practical. This table is an inventory of **configured commands**, not execution evidence; its selected command excerpts need not represent every step in the workflow.

| Workflow Path | Trigger(s) | Job / Stage | Runner OS | Configured Command | Artifact or Deployment |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**Trigger conditions, job dependencies and deployment/approval gates:**

**Observed CI execution evidence (separate from source declarations):**


### 51. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
|   |   |   |   |   |

### 52. Package and Release Artifacts

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
### 53. Runtime and Deployment Requirements

| Requirement | Type | Target Environment | Source or Evidence |
|---|---|---|---|
|   |   |   |   |

### 54. Compatibility Checks

| Check Type | Target | Method or Command | Outcome | Commit SHA | Evidence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

## Evidence and completion

### 55. Executed Command Evidence

| Baseline Item | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 56. Findings and Gaps

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
|   |   |   |   |

### 57. Discovery Item Status

Create **one row for every numbered baseline item (1–62)** and track evidence channels independently. The dimensions below refer to what was actually inspected or executed; they do **not** imply that all required discovery work has been completed. Preserve the original evidence IDs, links, missing information, and unresolved checks in the last column.

**Status meanings:** **Source Inspection:** `Verified` (exact source, external public metadata, repository metadata or documented discovery facts checked), `Partial` (source evidence available but material checks still open), `Not checked`, `Not applicable`. **Existing CI:** `Passed` (relevant checks completed successfully on a documented SHA), `Verified` (CI log/run evidence inspected), `Not checked`, `Not applicable`. **Operator Local:** `Passed` / `Failed` (actually executed by operator, with evidence), `Not executed` (check required but not run), `Not recorded` (operator-supplied information missing), `Not applicable` (no operator-local check is required for this particular item). For any relevant failure, record details in evidence; never relabel CI success as local success.

| Baseline Item | Source Inspection | Existing CI | Operator Local | Evidence or Missing Information |
|---|---|---|---|---|
|   |   |   |   |   |

**Unresolved operator checks and review status:**

| Field | Value |
|---|---|
| 58. Overall Baseline Disposition |  |
| 59. Reviewed By |  |
| 60. Review Date |  |
| 61. Next Action |  |

### 62. Deferred Checks

| Check | Reason Deferred | Revisit When |
|---|---|---|
|   |   |   |

This baseline records observed application facts and verification outcomes, not proposed modernization work.
