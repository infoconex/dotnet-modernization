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
| src/RecordSift.Domain/RecordSift.Domain.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | None |
| src/RecordSift.Application/RecordSift.Application.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Production | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Domain/RecordSift.Domain.csproj |

## Project settings and evaluated values

### 38. Compiler Settings

| Project Path | Configuration | Framework | Property | Declared Value | Condition |
|---|---|---|---|---|---|
| src/RecordSift.Domain/RecordSift.Domain.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |

### 39. Output and Validation Settings

| Project Path | Configuration | Property | Declared Value | Condition |
|---|---|---|---|---|
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | DocumentationFile | bin\Debug\RecordSift.Domain.xml |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Debug | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | DocumentationFile | bin\Release\RecordSift.Domain.xml |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Release | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | DocumentationFile | bin\Debug\RecordSift.Application.xml |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Debug | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | DocumentationFile | bin\Release\RecordSift.Application.xml |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Application/RecordSift.Application.csproj | Release | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | DocumentationFile | bin\Debug\RecordSift.Infrastructure.Csv.xml |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Debug | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | DocumentationFile | bin\Release\RecordSift.Infrastructure.Csv.xml |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Release | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | DocumentationFile | bin\Debug\RecordSift.Infrastructure.Xlsx.xml |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Debug | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | DocumentationFile | bin\Release\RecordSift.Infrastructure.Xlsx.xml |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Release | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | DocumentationFile | bin\Debug\RecordSift.Infrastructure.Reporting.xml |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Debug | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | DocumentationFile | bin\Release\RecordSift.Infrastructure.Reporting.xml |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Release | WarningsAsErrors | 1591 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |

### 40. Project Metadata and Imports

| Project Path | Metadata or Import Name | Declared Value | Source File |
|---|---|---|---|
| src/RecordSift.Domain/RecordSift.Domain.csproj | Configuration | Debug | src/RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Domain/RecordSift.Domain.csproj | FileAlignment | 512 | src/RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Domain/RecordSift.Domain.csproj | AppDesignerFolder | Properties | src/RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Domain/RecordSift.Domain.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | src/RecordSift.Domain/RecordSift.Domain.csproj |
| src/RecordSift.Application/RecordSift.Application.csproj | Configuration | Debug | src/RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Application/RecordSift.Application.csproj | FileAlignment | 512 | src/RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Application/RecordSift.Application.csproj | AppDesignerFolder | Properties | src/RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Application/RecordSift.Application.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | src/RecordSift.Application/RecordSift.Application.csproj |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Configuration | Debug | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | FileAlignment | 512 | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | AppDesignerFolder | Properties | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Configuration | Debug | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Configuration | Debug | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | FileAlignment | 512 | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj |

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
