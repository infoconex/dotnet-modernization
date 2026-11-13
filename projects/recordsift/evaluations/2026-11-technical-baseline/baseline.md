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
| 8. Published Application Version | Not applicable |
| 9. Published Package Version | `0.1.0` |
| 10. Published Release URL | `https://github.com/infoconex/RecordSift/releases/tag/v0.1.0` |
| 11. Published Package URL | `https://www.nuget.org/packages/RecordSift/0.1.0` |
| 12. Source Manifest Version | `0.1.0-rc.1` |
| 13. Assembly Version | `0.1.0.0` |
| 14. File Version | `0.1.0.0` |

### 15. Consumers and Entry Points

| Consumer or Entry Point | Type | Source or Evidence |
|---|---|---|
| `RecordSift.Application.Importing.Csv.CsvImporter<T>` | Library API | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Csv/CsvImporter.cs |
| `RecordSift.Application.Importing.Xlsx.XlsxImporter<T>` | Library API | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Xlsx/XlsxImporter.cs |
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

*Not checked — no operator-run Windows SDK inventory has been supplied.*

### 25. .NET Runtime Inventory

| Runtime Name | Runtime Version | Installation Path |
|---|---|---|

*Not checked — no operator-run Windows runtime inventory has been supplied.*

| Field | Value |
|---|---|
| 26. MSBuild Version | Not checked |
| 27. MSBuild Installation Source | Not checked |
| 28. NuGet CLI Version | Not checked |

### 29. .NET Framework Targeting Pack Inventory

| Framework Version | Installed | Location |
|---|---|---|

*Not checked — the local .NET Framework 4.8 reference-assembly file has not been inspected.*

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

One row per solution. The frozen `RecordSift.sln` declares **Debug** and **Release** configurations for the **Any CPU** platform. All ten projects are members of the solution, and all ten have `Build.0` mappings for **both** configurations; no build exclusions are declared for these two solution configurations. These are source-declared mappings, not independently executed builds.

| Solution Path | Format | Format Version | Declared IDE Version | Configurations | Platforms | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Debug, Release | Any CPU | All 10 projects mapped to build in both Debug and Release; no declared build exclusions |

### 37. Projects

One row per project; direct references are grouped by project name. Each linked project name opens the immutable source file; the full repository-relative project path is recorded here as the authoritative mapping for subsequent project tables, which use linked project names without repeating paths.

| Project | Role | Format | Target Framework(s) | Language Version | Output Type | MSBuild Platform(s) | SDK or ToolsVersion | Direct Project References | Project Path |
|---|---|---|---|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | Production | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | None | `src/RecordSift.Domain/RecordSift.Domain.csproj` |
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | Production | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Domain | `src/RecordSift.Application/RecordSift.Application.csproj` |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | Production | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Application<br>RecordSift.Domain | `src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj` |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | Production | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Application<br>RecordSift.Domain | `src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj` |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | Production | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Application<br>RecordSift.Domain | `src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj` |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | Test | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Domain | `tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj` |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | Test | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Application<br>RecordSift.Domain | `tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj` |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | Test | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Application.Tests<br>RecordSift.Infrastructure.Csv<br>RecordSift.Application<br>RecordSift.Domain | `tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj` |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | Test | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Infrastructure.Xlsx<br>RecordSift.Application<br>RecordSift.Domain | `tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj` |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | Test | Traditional | v4.8 | 7.3 | Library | AnyCPU | 15.0 | RecordSift.Infrastructure.Csv<br>RecordSift.Infrastructure.Reporting<br>RecordSift.Application<br>RecordSift.Domain | `tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj` |

## Project settings and evaluated values

### 38. Compiler Settings

These are **source-declared** compiler properties, not independently evaluated MSBuild values. D/R means Debug / Release. Shared source conditions: Debug = `'$(Configuration)|$(Platform)' == 'Debug|AnyCPU'`; Release = `'$(Configuration)|$(Platform)' == 'Release|AnyCPU'`. `LangVersion` is unconditional. `Not declared` means no corresponding source declaration and does not imply `false`.

| Project | Framework(s) | LangVersion | DebugSymbols (D/R) | DebugType (D/R) | Optimize (D/R) | DefineConstants (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | v4.8 | 7.3 | true / Not declared | full / pdbonly | false / true | DEBUG;TRACE / TRACE | None |

### 39. Output and Validation Settings

These are **source-declared** values. D/R means Debug / Release and uses the same shared conditions recorded in item 38. A single value is used when Debug and Release declarations agree. `Not declared` means the property is absent, not that MSBuild evaluated it as false or empty.

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Domain.xml` / `bin\Release\RecordSift.Domain.xml` | None |
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Application.xml` / `bin\Release\RecordSift.Application.xml` | None |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Infrastructure.Csv.xml` / `bin\Release\RecordSift.Infrastructure.Csv.xml` | None |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Infrastructure.Xlsx.xml` / `bin\Release\RecordSift.Infrastructure.Xlsx.xml` | None |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | `bin\Debug\` / `bin\Release\` | 4 | 1591 | `bin\Debug\RecordSift.Infrastructure.Reporting.xml` / `bin\Release\RecordSift.Infrastructure.Reporting.xml` | None |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | `bin\Debug\` / `bin\Release\` | 4 | Not declared | Not declared | None |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | `bin\Debug\` / `bin\Release\` | 4 | Not declared | Not declared | None |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | `bin\Debug\` / `bin\Release\` | 4 | Not declared | Not declared | None |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | `bin\Debug\` / `bin\Release\` | 4 | Not declared | Not declared | None |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | `bin\Debug\` / `bin\Release\` | 4 | Not declared | Not declared | None |

### 40. Project Metadata and Imports

These are project-file metadata and **explicit** imports, not evaluated MSBuild values. **Configuration Fallback** is the source-declared `Debug` value only when `$(Configuration)` is empty; it does **not** establish the configuration used during an actual build. `Not declared` means the property was absent from the inspected project XML. Each project name links to its immutable source file; the authoritative repository-relative project paths are in item 37.

| Project | Configuration Fallback | IsTestProject | FileAlignment | AppDesignerFolder | Imports | Additional Metadata / Conditions |
|---|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | Debug | Not declared | 512 | Properties | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | Debug | Not declared | 512 | Properties | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | Debug | Not declared | 512 | Properties | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | Debug | Not declared | Not declared | Not declared | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | Debug | Not declared | 512 | Not declared | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | Debug | true | 512 | Properties | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | Debug | true | 512 | Properties | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | Debug | true | 512 | Properties | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | Debug | true | Not declared | Not declared | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | Debug | true | 512 | Not declared | `$(MSBuildToolsPath)\Microsoft.CSharp.targets` | None |

### 41. Evaluated MSBuild Properties

No independent local MSBuild `-getProperty` evaluation has been executed for this frozen revision. The project-specific table below is reserved for observed values, using linked project names and the authoritative paths in item 37; a successful CI build does not populate it.

| Project | Configuration / Framework / Platform | Evaluated Properties (name=value) | Declared Properties for Comparison | Evidence |
|---|---|---|---|---|

*Not checked — no local MSBuild property evaluation has been executed.*

## Repository structure and dependencies

### 42. Repository Directories

| Directory | Purpose |
|---|---|
| src/ | Production code |
| tests/ | Automated tests and release consumer |
| docs/ | Requirements, specifications and guides |
| scripts/ | Build, test and validation utilities |
| packaging/ | Package manifests |
| .github/workflows/ | CI and release automation |

### 43. Repository Configuration

NuGet entries below are **declared in the frozen repository source**, not an inventory of effective settings on a Windows machine. The `clear` entries remove previously inherited entries **within their respective source collections**; later configuration layers or command-line choices can still affect effective behavior. The declared feeds are not verified download or audit origins.

| File or Mechanism | Present | Scope | Setting Name | Setting Value | Import or Precedence |
|---|---|---|---|---|---|
| NuGet.Config | True | Repository | packageSources.clear | True | Clears previously inherited package source entries in this collection |
| NuGet.Config | True | Repository | packageSources.nuget.org | https://api.nuget.org/v3/index.json | Declared package source following clear |
| NuGet.Config | True | Repository | auditSources.clear | True | Clears previously inherited audit source entries in this collection |
| NuGet.Config | True | Repository | auditSources.nuget.org-audit | https://api.nuget.org/v3/index.json | Declared audit source following clear |
| .editorconfig | True | Repository | root | true | Root-level EditorConfig |
| .editorconfig | True | Repository | charset | utf-8 | [*] |
| .editorconfig | True | Repository | indent_style | space | [*] |
| .editorconfig | True | Repository | dotnet_diagnostic.IDE1006.severity | error | C# analyzer |
| .gitignore | True | Repository | File present | True | Git ignore rules |
| AGENTS.md | True | Repository | File present | True | Repository instructions |
| .github/copilot-instructions.md | True | Repository | File present | True | GitHub AI instructions |
| Directory.Build.props | False | Tracked repository | Not applicable | Not applicable | Not evaluated |
| Directory.Build.targets | False | Tracked repository | Not applicable | Not applicable | Not evaluated |
| Directory.Packages.props | False | Tracked repository | Not applicable | Not applicable | Not evaluated |
| global.json | False | Tracked repository | Not applicable | Not applicable | Not evaluated |

**NuGet sections not declared in this source file:** `disabledPackageSources`, `packageSourceMapping`, `trustedSigners`, `packageSourceCredentials`, `clientCertificates`, `apikeys`, `config` (including signature policy, storage paths, proxy, request limits and push defaults), `packageRestore`, `packageManagement`, `bindingRedirects`, `solution`, `activePackageSource` (legacy), and version-dependent sections such as `minPublishAgeExceptions`. No additional NuGet configuration sections are declared in the inspected file. This is **not** a claim that any such settings are absent from the operator's machine.

**Effective NuGet configuration:** Not checked. No operator-run Windows inspection of the configuration hierarchy, enabled/disabled sources, credentials/policies, package-source mapping, audit behavior, or command-line/environment overrides has been provided. Do not infer effective defaults or the feeds actually used during restore from source XML alone.
### 44. NuGet Package Declarations

These are **17 source-declared package references** across seven consuming projects and **13 distinct package IDs**. The project summary keeps package counts easy to scan; the catalog preserves the exact package ID/version-to-project and declaration-source relationships. All seven inspected `packages.config` files declare `targetFramework=net48`. Source-declared package references are not proof of successful restore or actual package acquisition origin.

**A. Packages by project**

| Project | Package Count | Declaration Source | Configured Feed(s) |
|---|---:|---|---|
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | 9 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | 2 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/packages.config) | nuget.org |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | 1 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/packages.config) | nuget.org |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | 2 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config) | nuget.org |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | 1 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/packages.config) | nuget.org |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | 1 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/packages.config) | nuget.org |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | 1 | [packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/packages.config) | nuget.org |

**B. Package catalog**

One row per distinct **package ID and declared version**. Each consumer and its manifest are linked to the frozen revision; versions declared differently in other projects would remain separate rows.

| Package ID | Version | Referenced By | Declaration Source(s) | Configured Feed(s) |
|---|---|---|---|---|
| CsvHelper | 33.1.0 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| Microsoft.Bcl.AsyncInterfaces | 8.0.0 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| Microsoft.Bcl.HashCode | 1.1.1 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| Microsoft.CSharp | 4.7.0 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| System.Memory | 4.5.5 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| System.Buffers | 4.5.1 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| System.Numerics.Vectors | 4.5.0 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| System.Runtime.CompilerServices.Unsafe | 6.0.0 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| System.Threading.Tasks.Extensions | 4.5.4 | [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | [RecordSift.Infrastructure.Csv packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/packages.config) | nuget.org |
| ExcelDataReader | 3.9.0 | [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | [RecordSift.Infrastructure.Xlsx packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/packages.config) | nuget.org |
| System.ValueTuple | 4.5.0 | [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | [RecordSift.Infrastructure.Xlsx packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/packages.config) | nuget.org |
| NUnit | 3.14.0 | [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj)<br>[RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj)<br>[RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj)<br>[RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj)<br>[RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | [RecordSift.Application.Tests packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/packages.config)<br>[RecordSift.Domain.Tests packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config)<br>[RecordSift.Infrastructure.Csv.Tests packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/packages.config)<br>[RecordSift.Infrastructure.Reporting.Tests packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/packages.config)<br>[RecordSift.Infrastructure.Xlsx.Tests packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/packages.config) | nuget.org |
| NUnit.ConsoleRunner | 3.17.0 | [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | [RecordSift.Domain.Tests packages.config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/packages.config) | nuget.org |

**Additional declared package metadata:** NUnit.ConsoleRunner (`3.17.0`): `developmentDependency=true`. No additional package classifications are inferred. The `nuget.org` entries are eligible sources declared by the inspected repository configuration, **not** independently verified origins for each package. Effective feeds and restore resolution remain `Not checked`.

### 45. Non-NuGet Dependencies

Inventory **framework assembly references** separately from other **non-NuGet dependencies**. Project references belong in item 37 and NuGet packages in item 44. The entries below are source declarations from the frozen commit, not proof of installed assemblies or successful resolution. Linked project names resolve to canonical project paths in item 37. Runtime discovery, dynamically loaded dependencies and external service usage have not been comprehensively checked.

**A. Framework Assembly References**

One row per project. All listed assemblies are explicitly referenced as framework assemblies in the linked project file; their version/identity is not declared, and resolution has not been checked locally.

| Project | Framework References | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source |
|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | System<br>System.Core | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | System<br>System.Core | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | System<br>System.Core | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | System<br>System.Core<br>System.IO.Compression<br>System.Data<br>System.Xml | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | System<br>System.Core<br>System.Runtime.Serialization<br>System.Xml | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | System<br>System.Core | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | System<br>System.Core | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | System<br>System.Core | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | System<br>System.Core<br>System.IO.Compression<br>System.Xml | Framework assembly reference | Not declared | Not checked locally | Project file |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | System<br>System.Core<br>Microsoft.VisualBasic<br>System.Web.Extensions | Framework assembly reference | Not declared | Not checked locally | Project file |

**B. Other Non-NuGet Dependencies**

Use this table for separately declared third-party or locally distributed assemblies not managed by NuGet, COM components, native binaries, external services, and other verified non-NuGet dependencies. Preserve per-dependency identity, mechanism, version, source and resolution; split project rows when attributes differ.

| Project | Dependencies | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source |
|---|---|---|---|---|---|

*No additional non-NuGet dependency declarations identified in the ten inspected `.csproj` files at the frozen source SHA. External services, dynamically loaded components and actual runtime dependency resolution have **not** been comprehensively checked; this is not a conclusion that none exist.*


## Restore, build, tests and delivery

### 46. Operation Commands

| Operation | Project or Solution | Configuration | Platform | Command or Workflow | Source |
|---|---|---|---|---|---|
| Restore | RecordSift.sln | Not applicable | Not applicable | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | .github/workflows/windows-net48.yml |
| Build | RecordSift.sln | Release | Any CPU | msbuild .\RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | docs/engineering/baseline.md |
| Test | Five NUnit assemblies | Release | Any CPU | .\scripts\run_tests.ps1 -Level All | scripts/run_tests.ps1 |
| API verification | Production assemblies | Release | Any CPU | .\scripts\verify_public_api.ps1 | .github/workflows/windows-net48.yml |
| XML documentation | Production assemblies | Release | Any CPU | .\scripts\verify_xml_documentation.ps1 | .github/workflows/windows-net48.yml |
| IDE1006 style | RecordSift.sln | Not applicable | Not applicable | dotnet format style RecordSift.sln --no-restore --verify-no-changes --diagnostics IDE1006 --severity error --verbosity normal | .github/workflows/windows-net48.yml |
| Package | RecordSift | Release | Any CPU | .\scripts\build_release_candidate.ps1 -OutputDirectory $feed | .github/workflows/verify-rc-consumer.yml |
| Installed consumer | RecordSift | Release | Any CPU | .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | .github/workflows/verify-rc-consumer.yml |

### 47. Restore Outcomes

| Source Revision | Target | Outcome | Error or Note | Evidence |
|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Passed | Not applicable | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Passed | Not applicable | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

### 48. Build Outcomes

| Source Revision | Target | Configuration | Platform | Outcome | Warning Count | Error Count | Output or Evidence |
|---|---|---|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Release | Any CPU | Passed | Not recorded | Not recorded | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Release | Any CPU | Passed | Not recorded | Not recorded | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

### 49. Test Outcomes

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Domain.Tests | NUnit ConsoleRunner 3.17.0 | 123 | 123 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Application.Tests | NUnit ConsoleRunner 3.17.0 | 62 | 62 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Csv.Tests | NUnit ConsoleRunner 3.17.0 | 132 | 131 | 0 | 1 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Reporting.Tests | NUnit ConsoleRunner 3.17.0 | 54 | 54 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Xlsx.Tests | NUnit ConsoleRunner 3.17.0 | 48 | 48 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |

### 50. CI Workflows

These are **configured source definitions**, not proof that every job ran. Group identical commands by workflow, job/stage, runner, configured output and applicable triggers. The recorded commands are representative **exact command excerpts** from the pinned workflow definitions, not an exhaustive list of every step. Keep job-specific prerequisites and publication/deployment gates distinct.

| Workflow Path | Trigger(s) | Job / Stage | Runner OS | Configured Command | Artifact or Deployment |
|---|---|---|---|---|---|
| .github/workflows/windows-net48.yml | push, pull_request, workflow_dispatch | `build-test` / Restore packages.config dependencies | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | NUnit XML |
| .github/workflows/windows-net48.yml | push, pull_request, workflow_dispatch | `build-test` / Build separate Domain, Application and Infrastructure projects with MSBuild | windows-2022 | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | Build outputs |
| .github/workflows/verify-rc-consumer.yml | push, pull_request, workflow_dispatch | `verify-consumer` / Build unpublished package and run installed consumer | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | Installed consumer verification |
| .github/workflows/validate-docs.yml | push, pull_request, workflow_dispatch | `docs` / Validate versioned requirements and Markdown links | ubuntu-latest | python3 scripts/validate_docs.py | Documentation validation |
| .github/workflows/adversarial-extended.yml | push, pull_request, workflow_dispatch | `extended-adversarial` / Restore pinned dependencies | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Adversarial test evidence |
| .github/workflows/extended-adversarial.yml | push, pull_request, workflow_dispatch | `bounded-adversarial-stress` / Repeat bounded adversarial tests with sampled memory and process timeouts | windows-2022 | & .\scripts\run_adversarial_stress.ps1 -Iterations $iterations -MaximumPrivateMegabytes $maximumMiB -PerProcessTimeoutSeconds 90 | Bounded stress evidence |
| .github/workflows/prepare-0.1-release.yml | workflow_dispatch | `prepare` / Build stable package, independently install and execute net48 consumer, record SHA256 | windows-2022 | & .\scripts\build_release_candidate.ps1 -OutputDirectory $output -PackageVersion '0.1.0' | Prepared package artifact |
| .github/workflows/publish-release.yml | workflow_dispatch | `prepare` / Restore exact pinned packages | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Validated package |
| .github/workflows/publish-release.yml | workflow_dispatch | `publish` / Publish exact package to nuget.org | ubuntu-24.04 | dotnet nuget push "dist/RecordSift.$RELEASE_VERSION.nupkg" --api-key "$NUGET_API_KEY" --source https://api.nuget.org/v3/index.json | NuGet publish |
| .github/workflows/publish-release.yml | workflow_dispatch | `verify_public` / Independently install and run actual published package | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -FromNuGetOrg -PackageVersion $env:RELEASE_VERSION -ExpectedSourceCommit $env:GITHUB_SHA | Public-feed consumer |
| .github/workflows/publish-release.yml | workflow_dispatch | `github_release` / Publish release with verified package and checksum | ubuntu-24.04 | gh release view "$tag" --repo "$GITHUB_REPOSITORY" --json url,tagName | GitHub release |
| .github/workflows/recover-recordsift-0.1-release.yml | workflow_dispatch | `verify_public` / Validate installed package and run isolated net48 consumer | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -FromNuGetOrg -PackageVersion '0.1.0' -ExpectedSourceCommit $env:PUBLISHED_SOURCE_SHA | Published package verification |
| .github/workflows/recover-recordsift-0.1-release.yml | workflow_dispatch | `github_release` / Reconcile exact original artifact and create GitHub release | ubuntu-24.04 | gh release view v0.1.0 --repo "$GITHUB_REPOSITORY" --json url,tagName,targetCommitish | Release reconciliation |

**Trigger and job conditions:** For the push and pull-request workflows, event branch filters are defined in their pinned YAML; listing an event alone does not imply every branch matches. `workflow_dispatch` is manual. `prepare-0.1-release.yml` job `prepare`, `publish-release.yml` job `prepare` and recovery job `verify_public` each require `github.ref == 'refs/heads/main'`. Other job/step conditions, inputs and dependencies remain authoritative in the linked source workflow files; commands can be conditional even when a workflow trigger is permitted.

**Release and deployment sequence:** `publish-release.yml` runs `prepare` (Windows package build and provenance), then `publish` (Ubuntu, protected `nuget-release` environment requiring owner approval, OIDC authentication and NuGet push), then `verify_public` (Windows independent public-feed consumer), then `github_release` (Ubuntu tag/release creation following successful verification). The table retains the original `gh release view` verification command; its containing step also invokes `gh release create`. The separate `recover-recordsift-0.1-release.yml` does **not** republish the package: `verify_public` checks the original public package and `github_release` reconciles the original artifact/tag/release.

**Execution evidence boundary:** Source-defined triggers and commands do not establish observed execution, successful publication or deployment. Separately recorded CI runs and release evidence in the evidence manifest establish only their specific verified runs.

### 51. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
| Windows .NET Framework 4.8 build and test | https://github.com/infoconex/RecordSift/actions/runs/43146607664 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Verify internal release candidate in clean Windows consumer | https://github.com/infoconex/RecordSift/actions/runs/43146607706 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Validate engineering documentation | https://github.com/infoconex/RecordSift/actions/runs/43146607615 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |

### 52. Package and Release Artifacts

Source declarations, **unpublished CI artifacts**, and **published distributions** are recorded separately. The dates below identify the source snapshot, a CI verification result, or a publication event; they are not interchangeable. Dates/times use UTC, with day-only precision where an exact time is unverified.

**A. Source package declarations**

| Declaration | Declared Version | Source Committer Date (UTC) | Evidence |
|---|---|---|---|
| [packaging/RecordSift.nuspec](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/packaging/RecordSift.nuspec) | `0.1.0-rc.1` | `2026-11-12T03:12:18Z` | [Frozen source commit](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) |

The source timestamp is the frozen Git **committer date**; it does not establish when the nuspec's version was first introduced.

**B. CI package artifacts and verification**

| Artifact | Version | Verification Result | Verification Completed (UTC) | Evidence |
|---|---|---|---|---|
| Unpublished CI package | `0.1.0-rc.1` | Passed (local-feed consumer; not published) | `2026-11-12T03:13:13Z` | [Windows package/consumer CI](https://github.com/infoconex/RecordSift/actions/runs/43146607706/job/130945777078) |
| Unpublished CI stable-package candidate | `0.1.0` | Passed (local-feed consumer; not published) | `2026-11-12T03:13:19Z` | [Windows package/consumer CI](https://github.com/infoconex/RecordSift/actions/runs/43146607706/job/130945777078) |

Completion times above are the timestamps of the final **PASS** messages in existing CI logs, not a new operator execution or timestamps for GitHub-hosted downloadable workflow artifacts.

**C. Published artifacts**

| Artifact | Version | Status | Publication Date (UTC) | Evidence |
|---|---|---|---|---|
| RecordSift NuGet.org package | `0.1.0` | Published | `2026-11-01` (date verified; exact registry publication time not checked) | [NuGet.org package](https://www.nuget.org/packages/RecordSift/0.1.0) · [Public-feed consumer verification](https://github.com/infoconex/RecordSift/actions/runs/41355904536/job/124995742204) |
| GitHub Release `v0.1.0` | `v0.1.0` | Published | `2026-11-01T22:12:43Z` | [GitHub Release](https://github.com/infoconex/RecordSift/releases/tag/v0.1.0) |

Each distribution has its own record. NuGet package upload acceptance was previously observed, but that timestamp is **not** used as the registry publication time. Public-feed consumer CI confirms the package was available on **2026-11-01**; the precise initial listing/publication time on NuGet.org has **not** been independently verified. GitHub Release `published_at` is official release metadata. The NuGet.org publication date and the GitHub Release publication timestamp must not be inferred from each other.

**Source revision provenance** — the UTC timestamps below are Git *committer dates*, not guaranteed SHA creation or GitHub push times. The discovery checkout revision is different from the published release/package source.

| Source Context | Source Commit SHA | Committer Date (UTC) | Verification |
|---|---|---|---|
| Frozen discovery source (`main`) | [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) | `2026-11-12T03:12:18Z` | Commit metadata inspected; local checkout not verified |
| Published GitHub release tag (`v0.1.0`) | [`2db5c86bc26010afcb83c2e455d2471d8c9340d6`](https://github.com/infoconex/RecordSift/commit/2db5c86bc26010afcb83c2e455d2471d8c9340d6) | `2026-11-01T21:13:46Z` | Git tag and release metadata verified |
| Published NuGet package (`RecordSift 0.1.0`) | [`2db5c86bc26010afcb83c2e455d2471d8c9340d6`](https://github.com/infoconex/RecordSift/commit/2db5c86bc26010afcb83c2e455d2471d8c9340d6) | `2026-11-01T21:13:46Z` | Existing [public-feed verification CI](https://github.com/infoconex/RecordSift/actions/runs/41355904536/job/124995742204) confirmed package source; this is not an independently repeated download in this discovery |

**Package provenance boundary:** Existing [recovery CI](https://github.com/infoconex/RecordSift/actions/runs/41355904536/job/124995909555) verified the original package SHA-256 `c6e96f76693358125346d31829bc8a016c75af13aab3261566a6e6033f7c052a` and `SOURCE_COMMIT.txt` against `2db5c86bc26010afcb83c2e455d2471d8c9340d6` before creating the release. The actual public-feed consumer verification reported that same source SHA. The discovery has **not** independently downloaded the NuGet package or its GitHub release assets; this is existing CI evidence, not a new operator execution.
### 53. Runtime and Deployment Requirements

| Requirement | Type | Target Environment | Source or Evidence |
|---|---|---|---|
| Windows | Supported operating system | RecordSift consumer | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md |
| .NET Framework 4.8 | Target framework | Consuming application | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md |
| No Excel installation required | Runtime constraint | XLSX reader | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md |

### 54. Compatibility Checks

| Check Type | Target | Method or Command | Outcome | Commit SHA | Evidence |
|---|---|---|---|---|---|
| NuGet restore | RecordSift.sln | nuget restore | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| Release build | RecordSift.sln | MSBuild Rebuild | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| NUnit | Five test assemblies | NUnit 3.17.0 | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| Public API | Five production DLLs | verify_public_api.ps1 | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| XML documentation | Production XML | verify_xml_documentation.ps1 | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| IDE1006 naming | RecordSift.sln | dotnet format style | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| NuGet vulnerability audit | Pinned dependencies | NuGet audit | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| Installed package consumer | Unpublished NuGet candidates | verify_clean_consumer.ps1 | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |
| Documentation validation | Documentation | Python scripts | Passed | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | https://github.com/infoconex/RecordSift/actions/runs/43146607615 |

## Evidence and completion

### 55. Executed Command Evidence

| Baseline Item | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
| 47 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | GitHub Actions Windows checkout | NuGet CLI (version not logged) | RecordSift.sln | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 48 | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | GitHub Actions Windows checkout | MSBuild 17.14.60.43110 | Release; Any CPU | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 49 | & .\scripts\run_tests.ps1 | GitHub Actions Windows checkout | NUnit ConsoleRunner 3.17.0 | Five Release test assemblies | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 54 | & .\scripts\verify_public_api.ps1 | GitHub Actions Windows checkout | PowerShell (version not logged) | net48 Release | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 52 | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | GitHub Actions Windows checkout | PowerShell (version not logged) | Local candidate package | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

### 56. Findings and Gaps

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
| Windows discovery machine not inventoried | Cannot assert local tool/readiness baseline | Items 18–29 | Perform Windows host and tool version commands |
| Clean local checkout not verified | Local filesystem and Git state remain unknown | Items 31–35 | Clone selected SHA into unique discovery folder |
| Evaluated MSBuild values not independently queried | Declared project properties may differ from evaluated settings | Item 41 | Run MSBuild property queries from Windows Developer PowerShell |
| CI outcomes are not local execution evidence | CI success cannot verify operator environment | Items 47–49 | Restore, build and run tests in the approved Windows checkout |

### 57. Discovery Item Status

Track three independent evidence dimensions for all 62 baseline items. **Source Inspection** means pinned source files, repository metadata, external public artifact metadata or discovery documentation were inspected; it does **not** mean a command ran. **Existing CI** refers only to reviewed GitHub-hosted runs or their logs. **Operator Local** refers only to actual work on the operator's machine, not CI runner execution. A populated item is not automatically locally verified.

**Status definitions:** Source Inspection uses `Verified` (source/metadata documented), `Partial` (source-only view leaves relevant verification gaps), `Not checked`, or `Not applicable`. Existing CI uses `Passed` (relevant completed CI checks succeeded), `Verified` (run/log/evidence inspected without claiming a new local execution), `Not checked`, or `Not applicable`. Operator Local uses `Passed`/`Failed` only for observed operator-executed checks, `Not executed` for required operations not performed, `Not recorded` for missing operator-supplied information, and `Not applicable` when that item does not require an operator-local check. These status dimensions are **not** substitutes for the final disposition or review approval.

| Baseline Item | Source Inspection | Existing CI | Operator Local | Evidence or Missing Information |
|---|---|---|---|---|
| 1 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 2 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 3 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 4 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 5 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 6 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 7 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 8 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 9 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 10 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 11 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 12 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 13 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 14 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 15 | Verified | Not applicable | Not applicable | EV-003–EV-007 |
| 16 | Not applicable | Not applicable | Not recorded | Operator identity not supplied |
| 17 | Verified | Not applicable | Not applicable | Evaluation README |
| 18 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 19 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 20 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 21 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 22 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 23 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 24 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 25 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 26 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 27 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 28 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 29 | Not applicable | Not applicable | Not executed | Operator Windows host output missing |
| 30 | Verified | Passed | Not executed | Declared runner; local installation not checked |
| 31 | Not applicable | Not applicable | Not executed | No local discovery folder recorded |
| 32 | Verified | Not applicable | Not applicable | EV-004 |
| 33 | Verified | Verified | Not executed | Selected SHA; no local checkout verified |
| 34 | Not applicable | Not applicable | Not executed | Local Git verification pending |
| 35 | Not applicable | Not applicable | Not executed | Local Git verification pending |
| 36 | Verified | Not applicable | Not applicable | EV-011 |
| 37 | Verified | Not applicable | Not applicable | EV-011 |
| 38 | Verified | Not applicable | Not applicable | EV-011 |
| 39 | Verified | Not applicable | Not applicable | EV-011 |
| 40 | Verified | Not applicable | Not applicable | EV-011 |
| 41 | Not applicable | Not checked | Not executed | MSBuild evaluated-property query not executed |
| 42 | Verified | Not applicable | Not applicable | EV-002 |
| 43 | Partial | Not checked | Not executed | Tracked settings checked; effective precedence not evaluated |
| 44 | Verified | Not applicable | Not applicable | EV-012 |
| 45 | Partial | Not checked | Not executed | Static dependency inspection only |
| 46 | Verified | Not applicable | Not applicable | EV-013 |
| 47 | Verified | Passed | Not executed | CI restore passed; local restore not executed |
| 48 | Verified | Passed | Not executed | CI build passed; local build not executed |
| 49 | Verified | Passed | Not executed | CI NUnit passed; local suite not executed |
| 50 | Verified | Not applicable | Not applicable | EV-013 |
| 51 | Not applicable | Verified | Not applicable | EV-008–EV-010 |
| 52 | Verified | Passed | Not executed | EV-006, EV-009; EV-005 (published artifacts); exact NuGet registry publication time not checked |
| 53 | Verified | Not applicable | Not applicable | EV-003 |
| 54 | Verified | Passed | Not executed | EV-008–EV-010 |
| 55 | Not applicable | Verified | Not executed | CI command evidence; no operator execution |
| 56 | Verified | Not applicable | Not applicable | Known gaps documented |
| 57 | Verified | Not applicable | Not applicable | Status table populated; operator checks outstanding |
| 58 | Verified | Not applicable | Not applicable | Assessment remains incomplete |
| 59 | Not applicable | Not applicable | Not applicable | Review not performed |
| 60 | Not applicable | Not applicable | Not applicable | Review not performed |
| 61 | Verified | Not applicable | Not applicable | Operator action pending |
| 62 | Verified | Not applicable | Not executed | Pending checks documented |

**Unresolved verification and review:** No operator-run Windows preflight, clean checkout, MSBuild property evaluation, restore, build or test has been captured in this evaluation. Existing CI at the frozen source SHA does not verify local tooling or deployment/runtime conditions. Items 59–60 are **Not reviewed**; the overall item 58 disposition remains **More verification needed**. A `Not applicable` cell means that particular evidence channel is not required for that item, **not** that the full discovery is approved.

| Field | Value |
|---|---|
| 58. Overall Baseline Disposition | More verification needed |
| 59. Reviewed By | Not reviewed |
| 60. Review Date | Not reviewed |
| 61. Next Action | Verify Windows prerequisites and clean checkout (items 18–35) |

### 62. Deferred Checks

| Check | Reason Deferred | Revisit When |
|---|---|---|
| Windows toolchain preflight | No operator Windows command outputs | When Windows host is available |
| Local checkout verification | No isolated Windows discovery folder created | After host prerequisite checks |
| Evaluated MSBuild properties | Requires compatible Windows MSBuild and project checkout | After checkout and tool check |
| Local restore/build/test | Operator approval and environment verification required | After source checkout and side-effect review |

This baseline records observed application facts and verification outcomes, not proposed modernization work.
