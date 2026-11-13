# `<Application>` — Discovery baseline

**Blank, reusable template.** Copy this file for each application. The [step-by-step guide](../methodology/technical-discovery-runbook.md) explains how to evaluate each numbered field and populate every table.

A numbered **field** records one value. A numbered **table** records one kind of repeatable data (such as projects or dependencies). Its column headings describe the data within each row and have **no field numbers**. Add one row per applicable item and repeat rows as needed. All values below are deliberately blank; enter answers only into a copied baseline. If a check is not applicable, missing, or unexecuted, describe that in the copy and link evidence as appropriate. Do not include secrets.

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By |  |
| 2. Discovery Date |  |
| 3. Discovery Folder |  |

## Host and prerequisite tools

| Field | Value |
|---|---|
| 4. Operating System Name |  |
| 5. Operating System Version |  |
| 6. Operating System Build |  |
| 7. Operating System Architecture |  |
| 8. PowerShell Version |  |
| 9. Git Version |  |

### 10. .NET SDK Inventory

| SDK Version | Installation Path |
|---|---|
|   |   |

### 11. .NET Runtime Inventory

| Runtime Name | Runtime Version | Installation Path |
|---|---|---|
|   |   |   |

| Field | Value |
|---|---|
| 12. MSBuild Version |  |
| 13. MSBuild Installation Source |  |
| 14. NuGet CLI Version |  |

### 15. .NET Framework Targeting Pack Inventory

| Framework Version | Installed | Location |
|---|---|---|
|   |   |   |

### 16. Test Runner Inventory

| Runner Name | Runner Version | Source or Location |
|---|---|---|
|   |   |   |

## Source and checkout

| Field | Value |
|---|---|
| 17. HTTPS Clone URL |  |
| 18. Selected Source Branch or Tag |  |
| 19. Source Commit SHA |  |
| 20. Working Tree Clean |  |
| 21. Detached HEAD |  |
| 22. Repository Default Branch |  |
| 23. Verification Date |  |
| 24. Evidence Status |  |

## Application overview

| Field | Value |
|---|---|
| 25. Application Name |  |
| 26. Application Purpose |  |
| 27. Application Type |  |
| 28. Repository Visibility |  |
| 29. SSH Clone URL |  |
| 30. License |  |
| 31. Supported Operating Systems |  |
| 32. Published Application Version |  |
| 33. Published Package Version |  |
| 34. Published Release URL |  |
| 35. Published Package URL |  |
| 36. Source Manifest Version |  |
| 37. Assembly Version |  |
| 38. File Version |  |

### 39. Consumers and Entry Points

| Consumer or Entry Point | Type | Source or Evidence |
|---|---|---|
|   |   |   |

## Solution and project inventory

### 40. Solutions

| Solution Path | Format | Format Version | Declared IDE Version | Configuration | Platform | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

### 41. Projects

| Project Path | Role | Project Format | Target Framework | Language Version | Output Type | MSBuild Platform | SDK or ToolsVersion | Project References |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

## Project settings and evaluated values

### 42. Compiler Settings

| Project Path | Configuration | Framework | Property | Declared Value | Condition |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 43. Output and Validation Settings

| Project Path | Configuration | Property | Declared Value | Condition |
|---|---|---|---|---|
|   |   |   |   |   |

### 44. Project Metadata and Imports

| Project Path | Metadata or Import Name | Declared Value | Source File |
|---|---|---|---|
|   |   |   |   |

### 45. Evaluated MSBuild Properties

| Project Path | Configuration | Framework | Property | Evaluated Value | Declared Value | Evidence |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

## Repository structure and dependencies

### 46. Repository Directories

| Directory | Purpose |
|---|---|
|   |   |

### 47. Repository Configuration

| File or Mechanism | Present | Scope | Setting Name | Setting Value | Import or Precedence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 48. NuGet Package Declarations

| Project Path | Package ID | Declared Version | Declaration File | Configured Feed | Purpose |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 49. Other External Dependencies

| Consumer | Dependency | Type or Mechanism | Declaration Source | Version or Identity | Resolution or Location |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

## Restore, build, tests and delivery

### 50. Operation Commands

| Operation | Project or Solution | Configuration | Platform | Command or Workflow | Source |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

### 51. Restore Outcomes

| Source Revision | Target | Outcome | Error or Note | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

### 52. Build Outcomes

| Source Revision | Target | Configuration | Platform | Outcome | Warning Count | Error Count | Output or Evidence |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 53. Test Outcomes

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |   |

### 54. CI Workflows

| Workflow Path | Trigger | Runner OS | Build or Test Commands | Artifact or Deployment |
|---|---|---|---|---|
|   |   |   |   |   |

### 55. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
|   |   |   |   |   |

### 56. Package and Release Artifacts

| Artifact | Version | Contents or Metadata | Release URL | Evidence |
|---|---|---|---|---|
|   |   |   |   |   |

### 57. Runtime and Deployment Requirements

| Requirement | Type | Target Environment | Source or Evidence |
|---|---|---|---|
|   |   |   |   |

### 58. Compatibility Checks

| Check Type | Target | Method or Command | Outcome | Commit SHA | Evidence |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

## Evidence and completion

### 59. Executed Command Evidence

| Discovery Step | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |   |

### 60. Findings and Gaps

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
|   |   |   |   |

### 61. Discovery Step Status

| Step ID | Status | Evidence or Missing Information |
|---|---|---|
|   |   |   |

| Field | Value |
|---|---|
| 62. Overall Baseline Disposition |  |
| 63. Reviewed By |  |
| 64. Review Date |  |
| 65. Next Action |  |

### 66. Deferred Checks

| Check | Reason Deferred | Revisit When |
|---|---|---|
|   |   |   |

This baseline is a record of collected facts, not a modernization recommendation.
