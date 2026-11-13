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
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Domain/RecordSift.Domain.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Application/RecordSift.Application.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Domain/RecordSift.Domain.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../RecordSift.Application.Tests/RecordSift.Application.Tests.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Application/RecordSift.Application.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Domain/RecordSift.Domain.csproj |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Application/RecordSift.Application.csproj |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Domain/RecordSift.Domain.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Application/RecordSift.Application.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Test | Traditional | net48 | 7.3 | Library | AnyCPU | 15.0 | ../../src/RecordSift.Domain/RecordSift.Domain.csproj |

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
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | All | net48 | LangVersion | 7.3 | Unconditional |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Debug | net48 | DebugSymbols | true |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Debug | net48 | DebugType | full |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Debug | net48 | Optimize | false |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Debug | net48 | DefineConstants | DEBUG;TRACE |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Release | net48 | DebugType | pdbonly |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Release | net48 | Optimize | true |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Release | net48 | DefineConstants | TRACE |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |

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
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Debug | OutputPath | bin\Debug\ |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Debug | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Debug\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Release | OutputPath | bin\Release\ |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Release | WarningLevel | 4 |  '$(Configuration)\|$(Platform)' == 'Release\|AnyCPU'  |

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
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Configuration | Debug | tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | FileAlignment | 512 | tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | AppDesignerFolder | Properties | tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | IsTestProject | true | tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj |
| tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Configuration | Debug | tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | FileAlignment | 512 | tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | AppDesignerFolder | Properties | tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | IsTestProject | true | tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj |
| tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Configuration | Debug | tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | FileAlignment | 512 | tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | AppDesignerFolder | Properties | tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | IsTestProject | true | tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj |
| tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Configuration | Debug | tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | IsTestProject | true | tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj |
| tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Configuration | Debug | tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | FileAlignment | 512 | tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | IsTestProject | true | tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj |
| tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj | Import | $(MSBuildToolsPath)\Microsoft.CSharp.targets | tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj |

### 41. Evaluated MSBuild Properties

| Project Path | Configuration | Framework | Property | Evaluated Value | Declared Value | Evidence |
|---|---|---|---|---|---|---|
|   |   |   |   |   |   |   |

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

| File or Mechanism | Present | Scope | Setting Name | Setting Value | Import or Precedence |
|---|---|---|---|---|---|
| NuGet.Config | True | Repository | packageSources.nuget.org | https://api.nuget.org/v3/index.json | NuGet.Config |
| NuGet.Config | True | Repository | auditSources.nuget.org-audit | https://api.nuget.org/v3/index.json | NuGet.Config |
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

### 44. NuGet Package Declarations

| Project Path | Package ID | Declared Version | Declaration File | Configured Feed | Purpose |
|---|---|---|---|---|---|
| src/RecordSift.Infrastructure.Csv | CsvHelper | 33.1.0 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | Microsoft.Bcl.AsyncInterfaces | 8.0.0 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | Microsoft.Bcl.HashCode | 1.1.1 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | Microsoft.CSharp | 4.7.0 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | System.Memory | 4.5.5 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | System.Buffers | 4.5.1 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | System.Numerics.Vectors | 4.5.0 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | System.Runtime.CompilerServices.Unsafe | 6.0.0 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Csv | System.Threading.Tasks.Extensions | 4.5.4 | src/RecordSift.Infrastructure.Csv/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Xlsx | ExcelDataReader | 3.9.0 | src/RecordSift.Infrastructure.Xlsx/packages.config | nuget.org | Production |
| src/RecordSift.Infrastructure.Xlsx | System.ValueTuple | 4.5.0 | src/RecordSift.Infrastructure.Xlsx/packages.config | nuget.org | Production |
| tests/RecordSift.Application.Tests | NUnit | 3.14.0 | tests/RecordSift.Application.Tests/packages.config | nuget.org | Test framework |
| tests/RecordSift.Domain.Tests | NUnit | 3.14.0 | tests/RecordSift.Domain.Tests/packages.config | nuget.org | Test framework |
| tests/RecordSift.Domain.Tests | NUnit.ConsoleRunner | 3.17.0 | tests/RecordSift.Domain.Tests/packages.config | nuget.org | Test runner |
| tests/RecordSift.Infrastructure.Csv.Tests | NUnit | 3.14.0 | tests/RecordSift.Infrastructure.Csv.Tests/packages.config | nuget.org | Test framework |
| tests/RecordSift.Infrastructure.Reporting.Tests | NUnit | 3.14.0 | tests/RecordSift.Infrastructure.Reporting.Tests/packages.config | nuget.org | Test framework |
| tests/RecordSift.Infrastructure.Xlsx.Tests | NUnit | 3.14.0 | tests/RecordSift.Infrastructure.Xlsx.Tests/packages.config | nuget.org | Test framework |

### 45. Other External Dependencies

| Consumer | Dependency | Type or Mechanism | Declaration Source | Version or Identity | Resolution or Location |
|---|---|---|---|---|---|
| src/RecordSift.Domain/RecordSift.Domain.csproj | System | Framework assembly reference | src/RecordSift.Domain/RecordSift.Domain.csproj | Not declared | Not checked locally |
| src/RecordSift.Domain/RecordSift.Domain.csproj | System.Core | Framework assembly reference | src/RecordSift.Domain/RecordSift.Domain.csproj | Not declared | Not checked locally |
| src/RecordSift.Application/RecordSift.Application.csproj | System | Framework assembly reference | src/RecordSift.Application/RecordSift.Application.csproj | Not declared | Not checked locally |
| src/RecordSift.Application/RecordSift.Application.csproj | System.Core | Framework assembly reference | src/RecordSift.Application/RecordSift.Application.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | System | Framework assembly reference | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | System.Core | Framework assembly reference | src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | System | Framework assembly reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | System.Core | Framework assembly reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | System.IO.Compression | Framework assembly reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | System.Data | Framework assembly reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | System.Xml | Framework assembly reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | System | Framework assembly reference | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | System.Core | Framework assembly reference | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | System.Runtime.Serialization | Framework assembly reference | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Not declared | Not checked locally |
| src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | System.Xml | Framework assembly reference | src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj | Not declared | Not checked locally |

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

| Workflow Path | Trigger | Runner OS | Configured Command | Artifact or Deployment |
|---|---|---|---|---|
| .github/workflows/windows-net48.yml | push | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | NUnit XML |
| .github/workflows/windows-net48.yml | pull_request | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | NUnit XML |
| .github/workflows/windows-net48.yml | workflow_dispatch | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | NUnit XML |
| .github/workflows/windows-net48.yml | push | windows-2022 | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | Build outputs |
| .github/workflows/windows-net48.yml | pull_request | windows-2022 | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | Build outputs |
| .github/workflows/windows-net48.yml | workflow_dispatch | windows-2022 | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | Build outputs |
| .github/workflows/verify-rc-consumer.yml | push | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | Installed consumer verification |
| .github/workflows/verify-rc-consumer.yml | pull_request | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | Installed consumer verification |
| .github/workflows/verify-rc-consumer.yml | workflow_dispatch | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | Installed consumer verification |
| .github/workflows/validate-docs.yml | push | ubuntu-latest | python3 scripts/validate_docs.py | Documentation validation |
| .github/workflows/validate-docs.yml | pull_request | ubuntu-latest | python3 scripts/validate_docs.py | Documentation validation |
| .github/workflows/validate-docs.yml | workflow_dispatch | ubuntu-latest | python3 scripts/validate_docs.py | Documentation validation |
| .github/workflows/adversarial-extended.yml | push | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Adversarial test evidence |
| .github/workflows/adversarial-extended.yml | pull_request | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Adversarial test evidence |
| .github/workflows/adversarial-extended.yml | workflow_dispatch | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Adversarial test evidence |
| .github/workflows/extended-adversarial.yml | push | windows-2022 | & .\scripts\run_adversarial_stress.ps1 -Iterations $iterations -MaximumPrivateMegabytes $maximumMiB -PerProcessTimeoutSeconds 90 | Bounded stress evidence |
| .github/workflows/extended-adversarial.yml | pull_request | windows-2022 | & .\scripts\run_adversarial_stress.ps1 -Iterations $iterations -MaximumPrivateMegabytes $maximumMiB -PerProcessTimeoutSeconds 90 | Bounded stress evidence |
| .github/workflows/extended-adversarial.yml | workflow_dispatch | windows-2022 | & .\scripts\run_adversarial_stress.ps1 -Iterations $iterations -MaximumPrivateMegabytes $maximumMiB -PerProcessTimeoutSeconds 90 | Bounded stress evidence |
| .github/workflows/prepare-0.1-release.yml | workflow_dispatch | windows-2022 | & .\scripts\build_release_candidate.ps1 -OutputDirectory $output -PackageVersion '0.1.0' | Prepared package artifact |
| .github/workflows/publish-release.yml | workflow_dispatch | windows-2022 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Validated package |
| .github/workflows/publish-release.yml | workflow_dispatch | ubuntu-24.04 | dotnet nuget push "dist/RecordSift.$RELEASE_VERSION.nupkg" --api-key "$NUGET_API_KEY" --source https://api.nuget.org/v3/index.json | NuGet publish |
| .github/workflows/publish-release.yml | workflow_dispatch | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -FromNuGetOrg -PackageVersion $env:RELEASE_VERSION -ExpectedSourceCommit $env:GITHUB_SHA | Public-feed consumer |
| .github/workflows/publish-release.yml | workflow_dispatch | ubuntu-24.04 | gh release view "$tag" --repo "$GITHUB_REPOSITORY" --json url,tagName | GitHub release |
| .github/workflows/recover-recordsift-0.1-release.yml | workflow_dispatch | windows-2022 | & .\scripts\verify_clean_consumer.ps1 -FromNuGetOrg -PackageVersion '0.1.0' -ExpectedSourceCommit $env:PUBLISHED_SOURCE_SHA | Published package verification |
| .github/workflows/recover-recordsift-0.1-release.yml | workflow_dispatch | ubuntu-24.04 | gh release view v0.1.0 --repo "$GITHUB_REPOSITORY" --json url,tagName,targetCommitish | Release reconciliation |

### 51. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
| Windows .NET Framework 4.8 build and test | https://github.com/infoconex/RecordSift/actions/runs/43146607664 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Verify internal release candidate in clean Windows consumer | https://github.com/infoconex/RecordSift/actions/runs/43146607706 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Validate engineering documentation | https://github.com/infoconex/RecordSift/actions/runs/43146607615 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |

### 52. Package and Release Artifacts

| Artifact | Version | Attribute | Attribute Value | Release URL | Evidence |
|---|---|---|---|---|---|
| RecordSift | 0.1.0 | Published package | NuGet.org | https://github.com/infoconex/RecordSift/releases/tag/v0.1.0 | https://www.nuget.org/packages/RecordSift/0.1.0 |
| RecordSift | 0.1.0-rc.1 | Source nuspec version | 0.1.0-rc.1 | Not applicable | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/packaging/RecordSift.nuspec |
| RecordSift | 0.1.0-rc.1 | CI package build | Passed | Not published | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |
| RecordSift | 0.1.0 | CI local stable-package test | Passed | Not published | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

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

| Baseline Item | Status | Evidence or Missing Information |
|---|---|---|
| 1 | Complete | EV-003–EV-007 |
| 2 | Complete | EV-003–EV-007 |
| 3 | Complete | EV-003–EV-007 |
| 4 | Complete | EV-003–EV-007 |
| 5 | Complete | EV-003–EV-007 |
| 6 | Complete | EV-003–EV-007 |
| 7 | Complete | EV-003–EV-007 |
| 8 | Complete | EV-003–EV-007 |
| 9 | Complete | EV-003–EV-007 |
| 10 | Complete | EV-003–EV-007 |
| 11 | Complete | EV-003–EV-007 |
| 12 | Complete | EV-003–EV-007 |
| 13 | Complete | EV-003–EV-007 |
| 14 | Complete | EV-003–EV-007 |
| 15 | Complete | EV-003–EV-007 |
| 16 | Not checked | Operator identity not supplied |
| 17 | Complete | Evaluation README |
| 18 | Not checked | Operator Windows host output missing |
| 19 | Not checked | Operator Windows host output missing |
| 20 | Not checked | Operator Windows host output missing |
| 21 | Not checked | Operator Windows host output missing |
| 22 | Not checked | Operator Windows host output missing |
| 23 | Not checked | Operator Windows host output missing |
| 24 | Not checked | Operator Windows host output missing |
| 25 | Not checked | Operator Windows host output missing |
| 26 | Not checked | Operator Windows host output missing |
| 27 | Not checked | Operator Windows host output missing |
| 28 | Not checked | Operator Windows host output missing |
| 29 | Not checked | Operator Windows host output missing |
| 30 | Partial | Declared runner; local installation not checked |
| 31 | Not checked | No local discovery folder recorded |
| 32 | Complete | EV-004 |
| 33 | Partial | Selected SHA; no local checkout verified |
| 34 | Not checked | Local Git verification pending |
| 35 | Not checked | Local Git verification pending |
| 36 | Complete | EV-011 |
| 37 | Complete | EV-011 |
| 38 | Complete | EV-011 |
| 39 | Complete | EV-011 |
| 40 | Complete | EV-011 |
| 41 | Not checked | MSBuild evaluated-property query not executed |
| 42 | Complete | EV-002 |
| 43 | Partial | Tracked settings checked; effective precedence not evaluated |
| 44 | Complete | EV-012 |
| 45 | Partial | Static dependency inspection only |
| 46 | Complete | EV-013 |
| 47 | Partial | CI restore passed; local restore not executed |
| 48 | Partial | CI build passed; local build not executed |
| 49 | Partial | CI NUnit passed; local suite not executed |
| 50 | Complete | EV-013 |
| 51 | Complete | EV-008–EV-010 |
| 52 | Complete | EV-006, EV-009 |
| 53 | Complete | EV-003 |
| 54 | Complete | EV-008–EV-010 |
| 55 | Partial | CI command evidence; no operator execution |
| 56 | Partial | Known gaps documented |
| 57 | Partial | Status table populated; operator checks outstanding |
| 58 | Partial | Assessment remains incomplete |
| 59 | Not checked | Review not performed |
| 60 | Not checked | Review not performed |
| 61 | Partial | Operator action pending |
| 62 | Partial | Pending checks documented |

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
