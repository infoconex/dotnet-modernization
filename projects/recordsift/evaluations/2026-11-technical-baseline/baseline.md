# RecordSift — Discovery baseline

**Description:** RecordSift is a Windows .NET Framework 4.8 class library that imports CSV and XLSX records, maps source columns to typed models, validates records, and returns structured diagnostics and optional reports.

[Step-by-Step Instructions](../../../../methodology/technical-discovery-runbook.md)

## Application information

| Field | Value |
|---|---|
| 1. Application Type | Library |
| 2. Repository Visibility | Public |
| 3. License | MIT |
| 4. Supported Operating Systems | Windows |
| 5. HTTPS Clone URL | `https://github.com/infoconex/RecordSift.git` |
| 6. SSH Clone URL | `git@github.com:infoconex/RecordSift.git` |
| 7. Repository Default Branch | `main` |
| 8. Published Application Version | `0.1.0` |
| 9. Published Package Version | `0.1.0` |
| 10. Published Release URL | `https://github.com/infoconex/RecordSift/releases/tag/v0.1.0` |
| 11. Published Package URL | `https://www.nuget.org/packages/RecordSift/0.1.0` |
| 12. Source Manifest Version | `0.1.0-rc.1` |
| 13. Assembly Version | `0.1.0.0` |
| 14. File Version | `0.1.0.0` |

### 15. Consumers and Entry Points

| Consumer or Entry Point | Type | Source or Evidence |
|---|---|---|
| RecordSift.Application.Importing.Csv.CsvImporter<T> | Library API | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Csv/CsvImporter.cs |
| RecordSift.Application.Importing.Xlsx.XlsxImporter<T> | Library API | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Xlsx/XlsxImporter.cs |
| tests/ReleaseConsumer | Test consumer | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/ReleaseConsumer/Program.cs |

## Discovery information

| Field | Value |
|---|---|
| 16. Discovery By | Not recorded |
| 17. Discovery Date | `2026-11-12` |

## Discovery host and prerequisite tools

| Field | Value |
|---|---|
| 18. Operating System Name | Not checked |
| 19. Operating System Version | Not checked |
| 20. Operating System Build | Not checked |
| 21. Operating System Architecture | Not checked |
| 22. PowerShell Version | Not checked |
| 23. Git Version | Not checked |

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
| 26. MSBuild Version | Not checked |
| 27. MSBuild Installation Source | Not checked |
| 28. NuGet CLI Version | Not checked |

### 29. .NET Framework Targeting Pack Inventory

| Framework Version | Installed | Location |
|---|---|---|
|   |   |   |

### 30. Test Runner Inventory

| Runner Name | Runner Version | Source or Location |
|---|---|---|
| NUnit ConsoleRunner | 3.17.0 | tests/RecordSift.Domain.Tests/packages.config |

## Source revision and checkout

| Field | Value |
|---|---|
| 31. Discovery Folder | Not recorded |
| 32. Selected Source Branch or Tag | `main` |
| 33. Source Commit SHA | `1809d06c0fade59e4769d16e0f8eaf10fa426004` |
| 34. Working Tree Clean | Not checked |
| 35. Detached HEAD | Not checked |

## Solution and project inventory

### 36. Solutions

| Solution Path | Format | Format Version | Declared IDE Version | Configuration | Platform | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Debug | Any CPU | All 10 projects mapped to build |
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Release | Any CPU | All 10 projects mapped to build |

### 37. Projects

| Project Path | Role | Project Format | Target Framework | Language Version | Output Type | MSBuild Platform | SDK or ToolsVersion | Direct Project Reference |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

## Project settings and evaluated values

### 38. Compiler Settings

| Project Path | Configuration | Framework | Property | Declared Value | Condition |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 39. Output and Validation Settings

| Project Path | Configuration | Property | Declared Value | Condition |
|---|---|---|---|---|
|   |   |   |   |   |

### 40. Project Metadata and Imports

| Project Path | Metadata or Import Name | Declared Value | Source File |
|---|---|---|---|
|   |   |   |   |

### 41. Evaluated MSBuild Properties

| Project Path | Configuration | Framework | Property | Evaluated Value | Declared Value | Evidence |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## Repository structure and dependencies

### 42. Repository Directories

| Directory | Purpose |
|---|---|
|   |   |

### 43. Repository Configuration

| File or Mechanism | Present | Scope | Setting Name | Setting Value | Import or Precedence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 44. NuGet Package Declarations

| Project Path | Package ID | Declared Version | Declaration File | Configured Feed | Purpose |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 45. Other External Dependencies

| Consumer | Dependency | Type or Mechanism | Declaration Source | Version or Identity | Resolution or Location |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

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

| Artifact | Version | Attribute | Attribute Value | Release URL | Evidence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

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
