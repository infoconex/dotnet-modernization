# `<Application Name>` — Discovery baseline

**Description:** `<Application description>`

[Step-by-Step Instructions](../methodology/technical-discovery-runbook.md)

**Reading rule:** Keep this baseline concise: values, inventories, outcomes, actionable findings and short evidence references only. Full command transcripts, environment diagnostics, failed attempts, historical corrections and supporting explanations belong in the separate evidence manifest. Do not remove verified data from inventory tables to reduce length.

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By |  |
| 2. Discovery Date |  |
| 3. Discovery Status |  |
| 4. Discovery Completed Date |  |

**Status guidance:** Use `Not started`, `In progress`, `Blocked`, `Completed` or `Completed with gaps`. Enter `Discovery Completed Date` in `YYYY-MM-DD` only when the discovery is genuinely complete, with remaining gaps explicitly documented and accepted where applicable; otherwise use `Not completed`. Assess completion using the evidence recorded in the numbered items, item 59 (Findings and Gaps), and item 60 (Deferred Checks); no separate disposition or reviewer/date fields are needed. Discovery dates are distinct from source commit, CI and publication dates.

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

Separate **known consuming applications or systems** from the **public operations intended to be invoked directly by a consumer**. Use one row per verified consumer or distinct direct-call operation; cite source or usage evidence rather than inferring behavior from visibility or naming.

**A. Known Consumers**

| Consumer | Type | Evidence |
|---|---|---|
|   |   |   |

**External production consumers:** 

Use `Not identified` if none can be established from the inspected evidence; do not invent integrations or treat tests, samples and CI tools as deployed production applications.

**B. Public Entry Points**

| Entry Point | Purpose | Evidence |
|---|---|---|
|   |   |   |

Only include entry points that are **documented or demonstrated as direct consumer operations** (for example, a caller-invoked API method, executable command, HTTP endpoint or message handler). Do not include every public class or method, internal implementation detail, or callbacks merely passed to another API. An empty catalog is preferable to a speculative one.

## Discovery host and prerequisite tools

Record **Existing CI Runner** and **Operator Local** independently. CI values require logs from an executed job associated with the evaluated source SHA; identify the job, date and runner image/version. A runner label or current image inventory is not proof of the tool versions in a historical run. Use `Not checked` for unknown values; explain partial observations below their table. Do not substitute CI evidence for the operator's local environment.

**CI evidence (run/job link, source SHA, execution date, runner image/version):**

| Field | Existing CI Runner | Operator Local |
|---|---|---|
| 20. Operating System Name |  |  |
| 21. Operating System Version |  |  |
| 22. Operating System Build |  |  |
| 23. Operating System Architecture |  |  |
| 24. PowerShell Version |  |  |
| 25. Git Version |  |  |

**Partial CI observations or missing values:**

### 26. .NET SDK Inventory

| Environment | SDK Version | Installation Path |
|---|---|---|
|   |   |   |

**Inventory completeness and limitations:** 

### 27. .NET Runtime Inventory

| Environment | Runtime Name | Runtime Version | Installation Path |
|---|---|---|---|
|   |   |   |   |

**Inventory completeness and limitations:**

| Field | Existing CI Runner | Operator Local |
|---|---|---|
| 28. MSBuild Version |  |  |
| 29. MSBuild Installation Source |  |  |
| 30. NuGet CLI Version |  |  |

**Partial CI observations or missing values:**

### 31. .NET Framework Targeting Pack Inventory

| Environment | Framework Version | Installed | Location |
|---|---|---|---|
|   |   |   |   |

**Targeting-pack verification scope:** A successful build does not establish the exact installed reference-assembly file or its location.

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

One row per project when practical. Use Debug/Release values where declarations differ, one value where identical, and `Not declared` where absent; do not infer evaluated defaults. Preserve other properties and exceptional conditions. `<Configuration>` denotes `Debug` or `Release` in displayed paths; it is documentation shorthand, not a literal declared MSBuild value. The exact per-configuration declarations remain in the source and evidence. For example, `bin\<Configuration>\` represents the two declared paths `bin\Debug\` and `bin\Release\`.

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

Use **one file-inventory table**, with permanent links for existing files and plain text for absent files. Then create **separate settings tables for each configuration file that has meaningful settings**, using columns suited to that file. Group repetitive settings by category when this remains unambiguous; retain exact individual keys, values, conditions and applicability scopes in the evidence manifest. Do not hide important exceptions or collapse declared values into claims about effective behavior. Include nested/overriding files where present. Never record secrets.

**A. Configuration file inventory**

| File (link to pinned source when present) | Present | Purpose |
|---|---|---|
|   |   |   |

**B. NuGet configuration — [link to configuration file]**

| Setting / Section | Declared value / observation | Meaning / scope |
|---|---|---|
|   |   |   |

**C. EditorConfig — [link to configuration file]**

| Category | Settings / values | Applies to |
|---|---|---|
|   |   |   |

**D. Other configuration files**

Add a dedicated settings table for `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props` or another file **when present and meaningful**. For descriptive instructions or ignore files, a short purpose and pinned link may be sufficient. Distinguish source inspection, explicit file-only CLI queries, and effective inherited settings; use `Not checked` where needed.

**Evidence:** Link to the full, exact setting inventory and verification records in the evidence manifest.

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

Record **one row per distinct workflow file**. Summarize its declared triggers, all distinct job IDs, runner operating systems, purpose, and artifacts or deployments. Link the workflow source. Record significant branch/path filters, conditional job execution, matrices, dependencies, approvals, protected environments and exceptions below the table without creating repeated workflow rows. Commands and detailed execution history belong in the workflow source and evidence manifest; do not mistake configured behavior for a successful execution.

| Workflow Path | Triggers | Jobs | Runner OS | Purpose | Artifact or Deployment |
|---|---|---|---|---|---|
|   |   |   |   |   |   |

**Conditions, dependencies and approval gates:**

**Observed runs:** See item 54 and the evidence manifest.

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

| Execution Category | Outcome | Evidence |
|---|---|---|
|   |   |   |

### 59. Findings and Gaps

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
|   |   |   |   |

### 60. Deferred Checks

| Check | Reason Deferred | Revisit When |
|---|---|---|
|   |   |   |

This baseline records observed application facts and verification outcomes, not proposed modernization work.
