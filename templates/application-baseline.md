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

One row per project wherever possible. Use project name first (link to the project file when available), group direct references by name, and put the repository-relative project file path last. Preserve all frameworks/platforms and split only when differences cannot be represented unambiguously.

| Project | Role | Format | Target Framework(s) | Language Version | Output Type | MSBuild Platform(s) | SDK or ToolsVersion | Direct Project References | Project Path |
|---|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |   |

## Project settings and evaluated values

### 38. Compiler Settings

One row per project whenever possible. D/R means Debug/Release in that order; show one value when both have identical declarations. `Not declared` is not an evaluated default. Document shared exact conditions once; label exceptions or additional configurations and properties explicitly.

| Project | Framework(s) | LangVersion | DebugSymbols (D/R) | DebugType (D/R) | Optimize (D/R) | DefineConstants (D/R) | Conditions / Exceptions | Project Path |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

### 39. Output and Validation Settings

One row per project when practical. Use Debug/Release values where declarations differ, one value where identical, and `Not declared` where absent; do not infer evaluated defaults. Preserve other properties and exceptional conditions.

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions | Project Path |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

### 40. Project Metadata and Imports

One row per project. Give each named metadata property a column and list distinct imports together. **Configuration Fallback** is a source-declared value used when `$(Configuration)` is empty, not a verified evaluated/build configuration; record its condition where relevant. `Not declared` means absent from project source, not evaluated false. Preserve exceptional conditional/import scope.

| Project | Configuration Fallback | IsTestProject | FileAlignment | AppDesignerFolder | Imports | Additional Metadata / Conditions | Project Path |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 41. Evaluated MSBuild Properties

One row per project when possible. Enter only observed evaluated values, labeled by configuration/platform/framework, and distinguish source declarations from evaluated outputs. Link exact command/output; do not populate from XML or successful build alone.

| Project | Configuration / Framework / Platform | Evaluated Properties (name=value) | Declared Properties for Comparison | Evidence | Project Path |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

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

One row per consuming project where unambiguous. List **each package ID, declared version and purpose** together, one per line, alongside version source and configured feed(s). Qualify any differing per-package conditions or feeds rather than merging incompatible details. Configured feed is not proven acquisition origin.

| Project | Packages (ID — Version — Purpose) | Declaration / Version Source | Configured Feed(s) | Project Path |
|---|---|---|---|---|
|   |   |   |   |   |

### 45. Non-NuGet Dependencies

Separate **framework assembly references** from **other non-NuGet dependencies**. Project references are in item 37 and NuGet-managed dependencies in item 44. Use linked project names first and paths last; preserve exact names, mechanisms, versions, source/conditions and resolution evidence. `Not declared` is not `Not checked`, and missing project declarations do not establish the absence of runtime or dynamically loaded dependencies.

**A. Framework Assembly References**

| Project | Framework References | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source | Project Path |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

**B. Other Non-NuGet Dependencies**

Examples include native libraries, COM components, non-NuGet third-party assemblies and external service dependencies. If no declarations are found, write an explicit source-scoped finding **below** the table and identify outstanding runtime checks; do not invent a dependency or use `None` to mean that checks were not performed.

| Project | Dependencies | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source | Project Path |
|---|---|---|---|---|---|---|

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

| Workflow Path | Trigger | Runner OS | Configured Command | Artifact or Deployment |
|---|---|---|---|---|
|   |   |   |   |   |

### 51. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
|   |   |   |   |   |

### 52. Package and Release Artifacts

Record separately the source used for **discovery**, the source targeted by the **published Git tag**, and the source actually verified for the **published package**. Git committer timestamps are not source creation/push dates; publication timestamps are separate. Use full SHAs and UTC `YYYY-MM-DDTHH:MM:SSZ`; never infer package source from a release tag without package-specific evidence.

| Artifact | Version | Attribute | Attribute Value | Release URL | Evidence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**Source revision provenance**

| Source Context | Source Commit SHA | Committer Date (UTC) | Verification |
|---|---|---|---|
|   |   |   |   |

**Publication timestamps**

| Published Artifact | Published At (UTC) | Evidence |
|---|---|---|
|   |   |   |
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

| Baseline Item | Status | Evidence or Missing Information |
|---|---|---|
|   |   |   |

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
