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
| NuGet.Config | True | Repository | packageSources.nuget.org | https://api.nuget.org/v3/index.json | Repository override |
| NuGet.Config | True | Repository | auditSources.nuget.org-audit | https://api.nuget.org/v3/index.json | Repository override |
| .editorconfig | True | Repository | EditorConfig rules | See source file | Root |
| .gitignore | True | Repository | Ignore rules | See source file | Root |
| AGENTS.md | True | Repository | Agent instructions | See source file | Root |
| .github/copilot-instructions.md | True | Repository | AI instructions | See source file | .github/ |
| Directory.Build.props | False | Tracked source | Not applicable | Not applicable | Not evaluated |
| Directory.Build.targets | False | Tracked source | Not applicable | Not applicable | Not evaluated |
| Directory.Packages.props | False | Tracked source | Not applicable | Not applicable | Not evaluated |
| global.json | False | Tracked source | Not applicable | Not applicable | Not evaluated |

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
| RecordSift production projects | .NET Framework assemblies | Framework Reference | 10 project files | net48 | Framework resolved by MSBuild (CI) |
| RecordSift.Infrastructure.Xlsx | System.IO.Compression | Framework Reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | net48 | Framework resolved by MSBuild (CI) |
| RecordSift.Infrastructure.Xlsx | System.Data | Framework Reference | src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj | net48 | Framework resolved by MSBuild (CI) |

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
