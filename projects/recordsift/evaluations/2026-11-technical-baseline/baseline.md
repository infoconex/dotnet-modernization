# RecordSift — Discovery baseline

**Description:** RecordSift is a Windows .NET Framework 4.8 class library that imports CSV and XLSX records, maps source columns to typed models, validates records, and returns structured diagnostics and optional reports.

[Step-by-Step Instructions](../../../../methodology/technical-discovery-runbook.md)

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By | Not recorded |
| 2. Discovery Date | `2026-11-12` |
| 3. Discovery Status | Completed with gaps |
| 4. Discovery Completed Date | `2026-11-13` |

## Application information

| Field | Value |
|---|---|
| 5. Application Type | Library |
| 6. Repository Visibility | Public |
| 7. License | MIT |
| 8. Supported Operating Systems | Windows |
| 9. HTTPS Clone URL | `https://github.com/infoconex/RecordSift.git` |
| 10. SSH Clone URL | `git@github.com:infoconex/RecordSift.git` |
| 11. Repository Default Branch | `main` |
| 12. Published Application Version | Not applicable |
| 13. Published Package Version | `0.1.0` |
| 14. Published Release URL | `https://github.com/infoconex/RecordSift/releases/tag/v0.1.0` |
| 15. Published Package URL | `https://www.nuget.org/packages/RecordSift/0.1.0` |
| 16. Source Manifest Version | `0.1.0-rc.1` |
| 17. Assembly Version | `0.1.0.0` |
| 18. File Version | `0.1.0.0` |

### 19. Consumers and Entry Points

Known consumers and public entry points are limited to documented or demonstrated direct use. No external production consumer was identified.

**A. Known Consumers**

| Consumer | Type | Evidence |
|---|---|---|
| `tests/ReleaseConsumer` | Test application | [Clean NuGet consumer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/ReleaseConsumer/Program.cs) |

**External production consumers:** Not identified.

**B. Public Entry Points**

| Entry Point | Purpose | Evidence |
|---|---|---|
| `CsvImporter<T>.Import` | Import CSV records | [CSV importer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Csv/CsvImporter.cs) |
| `CsvStreamImporterAdapter<T>.Import` | Import CSV from a byte stream | [CSV stream adapter source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs) |
| `XlsxImporter<T>.Import` | Import XLSX records | [XLSX importer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Xlsx/XlsxImporter.cs) |
| `JsonImportResultSerializerAdapter.Serialize` | Generate JSON diagnostic reports | [JSON serializer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/JsonImportResultSerializerAdapter.cs) |
| `ReadableImportResultFormatterAdapter.Format` | Generate readable reports | [Readable formatter source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/ReadableImportResultFormatterAdapter.cs) |
| `CsvImportResultSerializerAdapter.Serialize` | Generate diagnostic CSV reports | [Diagnostic CSV serializer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/CsvImportResultSerializerAdapter.cs) |

| Field | Existing CI Runner | Operator Local |
|---|---|---|
| 20. Operating System Name | Microsoft Windows Server 2022 Datacenter | Microsoft Windows 11 Pro |
| 21. Operating System Version | `10.0.20348` | `10.0.26300` |
| 22. Operating System Build | `20348` | `26300` |
| 23. Operating System Architecture | 64-bit | 64-bit |
| 24. PowerShell Version | `7.6.10` | `7.7.0` |
| 25. Git Version | `2.56.1.windows.1` | `2.56.0.windows.4` |

### 26. .NET SDK Inventory

Observed SDK inventory; CI runner and operator workstation are separate environments.

| Environment | SDK Version | Installation Path |
|---|---|---|
| Existing CI runner | `8.0.134` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `8.0.206` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `8.0.319` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `8.0.428` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `9.0.124` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `9.0.205` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `9.0.321` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `10.0.115` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `10.0.204` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `10.0.303` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `10.0.404` | `C:\Program Files\dotnet\sdk` |
| Existing CI runner | `11.0.100` | `C:\Program Files\dotnet\sdk` |
| Operator local | `8.0.428` | `C:\Program Files\dotnet\sdk` |
| Operator local | `9.0.321` | `C:\Program Files\dotnet\sdk` |
| Operator local | `10.0.404` | `C:\Program Files\dotnet\sdk` |
| Operator isolated | `11.0.100` | `$HOME\dotnet-sdks\11.0.100` |
| Operator isolated | `11.0.100-rc.2.26504.105` | `$HOME\dotnet-sdks\11.0.100-rc.2.26504.105` |
| Operator isolated | `10.0.404` | `$HOME\dotnet-sdks\10.0.404` |
| Operator isolated | `10.0.303` | `$HOME\dotnet-sdks\10.0.303` |
| Operator isolated | `9.0.205` | `$HOME\dotnet-sdks\9.0.205` |

### 27. .NET Runtime Inventory

Observed runtime inventory. CLR 4.x evidence is separate from `dotnet --list-runtimes`.

| Environment | Runtime Name | Runtime Version | Installation Path |
|---|---|---|---|
| Existing CI runner | `Microsoft.AspNetCore.App` | `6.0.48` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `8.0.6` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `8.0.22` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `8.0.34` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `9.0.6` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `9.0.23` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `10.0.8` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `10.0.11` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `10.0.15` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.AspNetCore.App` | `11.0.0` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `6.0.48` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `8.0.6` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `8.0.22` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `8.0.34` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `9.0.6` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `9.0.23` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `10.0.8` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `10.0.11` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `10.0.15` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.NETCore.App` | `11.0.0` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `8.0.6` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `8.0.22` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `8.0.34` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `9.0.6` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `9.0.23` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `10.0.8` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `10.0.11` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `10.0.15` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Existing CI runner | `Microsoft.WindowsDesktop.App` | `11.0.0` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Earlier CI runner (NUnit, 2026-11-12) | .NET Framework CLR | `v4.0.30319.42000` | Not checked |
| Operator local | `Microsoft.AspNetCore.App` | `8.0.34` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Operator local | `Microsoft.AspNetCore.App` | `9.0.23` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Operator local | `Microsoft.AspNetCore.App` | `10.0.15` | `C:\Program Files\dotnet\shared\Microsoft.AspNetCore.App` |
| Operator local | `Microsoft.NETCore.App` | `6.0.36` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Operator local | `Microsoft.NETCore.App` | `7.0.20` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Operator local | `Microsoft.NETCore.App` | `8.0.34` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Operator local | `Microsoft.NETCore.App` | `9.0.23` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Operator local | `Microsoft.NETCore.App` | `10.0.15` | `C:\Program Files\dotnet\shared\Microsoft.NETCore.App` |
| Operator local | `Microsoft.WindowsDesktop.App` | `6.0.36` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Operator local | `Microsoft.WindowsDesktop.App` | `7.0.20` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Operator local | `Microsoft.WindowsDesktop.App` | `8.0.34` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Operator local | `Microsoft.WindowsDesktop.App` | `9.0.23` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |
| Operator local | `Microsoft.WindowsDesktop.App` | `10.0.15` | `C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App` |

| Field | Existing CI Runner | Operator Local |
|---|---|---|
| 28. MSBuild Version | `17.14.60.43110` | `4.8.10001.0` |
| 29. MSBuild Installation Source | Visual Studio Enterprise 2022 | Windows .NET Framework |
| 30. NuGet CLI Version | `8.0.0.137` | `7.9.0.83` |

### 31. .NET Framework Targeting Pack Inventory

The standard machine-wide v4.8 reference-assembly path was absent locally. NuGet-provided references enabled the verified SDK-only build (EV-081).

| Environment | Framework Version | Installed | Location |
|---|---|---|---|
| Existing CI runner | `v4.8` | True | `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8` |
| Operator local | `v4.8` | False | `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8` |

### 32. Test Runner Inventory

NUnit ConsoleRunner 3.17.0 was verified and used successfully across five local suites (EV-081).

| Runner Name | Runner Version | Source or Location |
|---|---|---|
| NUnit ConsoleRunner (declared) | 3.17.0 | tests/RecordSift.Domain.Tests/packages.config |
| NUnit ConsoleRunner (operator local) | 3.17.0 | `D:\RecordSift\packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe` |

| Field | Value |
|---|---|
| 33. Discovery Folder | `$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400` |
| 34. Selected Source Branch or Tag | `main` |
| 35. Source Commit SHA | `1809d06c0fade59e4769d16e0f8eaf10fa426004` |
| 36. Source Committer Date (UTC) | `2026-11-12T03:12:18Z` |
| 37. Working Tree Clean | True |
| 38. Detached HEAD | True |

### 39. Solutions

One solution, with Debug and Release / Any CPU configurations.

| Solution Path | Format | Format Version | Declared IDE Version | Configurations | Platforms | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Debug, Release | Any CPU | All 10 projects mapped to build in both Debug and Release; no declared build exclusions |

### 40. Projects

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

### 41. Compiler Settings

Source-declared values; effective compiler switches are not inferred.

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

### 42. Output and Validation Settings

Source-declared values. Production-only XML documentation and warning declarations are distinguished from test projects. `<Configuration>` denotes `Debug` or `Release` in displayed paths; it is documentation shorthand, not a literal declared MSBuild value. 

| Project | OutputPath (D/R) | WarningLevel (D/R) | WarningsAsErrors (D/R) | DocumentationFile (D/R) | Conditions / Exceptions |
|---|---|---|---|---|---|
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | `bin\<Configuration>\` | 4 | 1591 | `bin\<Configuration>\RecordSift.Domain.xml` | None |
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | `bin\<Configuration>\` | 4 | 1591 | `bin\<Configuration>\RecordSift.Application.xml` | None |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | `bin\<Configuration>\` | 4 | 1591 | `bin\<Configuration>\RecordSift.Infrastructure.Csv.xml` | None |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | `bin\<Configuration>\` | 4 | 1591 | `bin\<Configuration>\RecordSift.Infrastructure.Xlsx.xml` | None |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | `bin\<Configuration>\` | 4 | 1591 | `bin\<Configuration>\RecordSift.Infrastructure.Reporting.xml` | None |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | `bin\<Configuration>\` | 4 | Not declared | Not declared | None |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | `bin\<Configuration>\` | 4 | Not declared | Not declared | None |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | `bin\<Configuration>\` | 4 | Not declared | Not declared | None |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | `bin\<Configuration>\` | 4 | Not declared | Not declared | None |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | `bin\<Configuration>\` | 4 | Not declared | Not declared | None |

### 43. Project Metadata and Imports

Explicit project-file metadata and imports, not evaluated values.

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

### 44. Evaluated MSBuild Properties

Observed CI-evaluated MSBuild properties (EV-015). Empty properties do not establish compiler flags.

| Project | Configuration / Framework / Platform | Evaluated Properties (name=value) | Declared Properties for Comparison | Evidence |
|---|---|---|---|---|
| [RecordSift.Application](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/RecordSift.Application.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Application`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=bin\\<Configuration>\\RecordSift.Application.xml` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` in Debug and Release | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Domain](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/RecordSift.Domain.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Domain`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=bin\\<Configuration>\\RecordSift.Domain.xml` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` in Debug and Release | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Infrastructure.Csv](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Infrastructure.Csv`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=bin\\<Configuration>\\RecordSift.Infrastructure.Csv.xml` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` in Debug and Release | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Infrastructure.Reporting](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Infrastructure.Reporting`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=bin\\<Configuration>\\RecordSift.Infrastructure.Reporting.xml` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` in Debug and Release | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Infrastructure.Xlsx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Infrastructure.Xlsx`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=bin\\<Configuration>\\RecordSift.Infrastructure.Xlsx.xml` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` in Debug and Release | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Application.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Application.Tests`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=(empty)` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` not declared | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Domain.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Domain.Tests`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=(empty)` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` not declared | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Infrastructure.Csv.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Infrastructure.Csv.Tests`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=(empty)` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` not declared | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Infrastructure.Reporting.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Infrastructure.Reporting.Tests`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=(empty)` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` not declared | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |
| [RecordSift.Infrastructure.Xlsx.Tests](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj) | Debug and Release / `v4.8` / `AnyCPU` | `AssemblyName=RecordSift.Infrastructure.Xlsx.Tests`; `TargetFrameworkVersion=v4.8`; `LangVersion=7.3`; `OutputType=Library`; `Optimize(Debug)=false`; `Optimize(Release)=true`; `DocumentationFile=(empty)` | Same source declarations for framework, language, output type, configuration-scoped optimization and `DocumentationFile` not declared | [CI evaluation](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) |

### 45. Repository Directories

| Directory | Purpose |
|---|---|
| .github/ | Repository-level Copilot instructions and pull request template |
| .github/ISSUE_TEMPLATE/ | Bug report and individual requirement issue templates |
| .github/agents/ | Requirements review and TDD coaching agent definitions |
| .github/workflows/ | CI and release automation |
| docs/ | Requirements, specifications and guides |
| packaging/ | Package manifests |
| scripts/ | Build, test and validation utilities |
| src/ | Production code |
| tests/ | Automated tests and release consumer |

| Tracked file | Verified purpose |
|---|---|
| `.github/ISSUE_TEMPLATE/bug_report.yml` | Defect report form requesting reproduction, expected/actual behavior, environment and sanitized diagnostics |
| `.github/ISSUE_TEMPLATE/requirement.yml` | Single FR/NFR or engineering requirement with acceptance scenarios, verification and dependency fields |
| `.github/agents/requirements-reviewer.agent.md` | Requirements and scenario-to-test traceability review guidance; read/search tools |
| `.github/agents/tdd-coach.agent.md` | TDD red/green/refactor coaching with requirements and test evidence traceability |
| `.github/copilot-instructions.md` | Repository-wide Copilot guidance on architecture, C# conventions, branches, TDD and validation |
| `.github/pull_request_template.md` | Pull request scope, evidence, compatibility, risk, traceability and review checklist |

### 46. Repository Configuration

**A. Configuration file inventory**

| File | Present | Purpose |
|---|---|---|
| [NuGet.Config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/NuGet.Config) | Yes | Package and audit sources |
| [.editorconfig](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.editorconfig) | Yes | Formatting, C# style, naming and diagnostics |
| [.gitignore](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.gitignore) | Yes | Tracked-file exclusion patterns |
| [AGENTS.md](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/AGENTS.md) | Yes | Repository agent instructions |
| [.github/copilot-instructions.md](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/copilot-instructions.md) | Yes | Copilot instructions |
| `Directory.Build.props` | No | Central build properties |
| `Directory.Build.targets` | No | Central build targets |
| `Directory.Packages.props` | No | Central package versions |
| `global.json` | No | SDK selection |

**B. [NuGet.Config](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/NuGet.Config) — package and audit configuration**

| Setting | Declared value / observation | Meaning |
|---|---|---|
| `packageSources` | `<clear />` | Clears inherited entries in this collection |
| `packageSources.nuget.org` | `https://api.nuget.org/v3/index.json` | Declared package feed |
| `auditSources` | `<clear />` | Clears inherited audit-source entries |
| `auditSources.nuget.org-audit` | `https://api.nuget.org/v3/index.json` | Declared audit feed |
| Explicit CLI source query | One enabled `nuget.org` source | `dotnet nuget list source --configfile .\NuGet.Config`; file-only query |

The explicit CLI query verified one enabled source **for the specified repository file only**. It did not establish inherited effective settings, actual download provenance, or a successful restore.

**C. [.editorconfig](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.editorconfig) — formatting, style and naming**

| Category | Settings / values | Applies to |
|---|---|---|
| General | `root=true`<br>`charset=utf-8`<br>`end_of_line=lf`<br>`indent_style=space`<br>Final newline required<br>Trailing whitespace trimmed | Root and `[*]` |
| Indentation | `indent_size=4` for C#/CSX<br>`indent_size=2` for project, props, targets, config and XML | `[*.{cs,csx}]`, `[*.{csproj,props,targets,config,xml}]` |
| Markdown | `trim_trailing_whitespace=false` | `[*.md]` |
| Imports | System directives first<br>Import groups not separated | `[*.{cs,csx}]` |
| C# style | Qualification of field/property/method/event `false:suggestion`<br>Predefined types `true:suggestion`<br>`var` built-in types `false:suggestion`<br>`var` when type apparent `true:suggestion`<br>`var` elsewhere `false:suggestion`<br>Block-scoped namespaces<br>Braces preferred | `[*.{cs,csx}]` |
| Diagnostics | `IDE1006=error` | `[*.{cs,csx}]` |
| Naming — shared C# | Constants PascalCase (including private constants)<br>Interfaces `I` prefix<br>Locals and parameters camelCase<br>Naming rules have `error` severity | `[*.{cs,csx}]` |
| Naming — production | Types and members PascalCase<br>Private instance fields `_camelCase`<br>Private static fields `s_camelCase`<br>Naming rules have `error` severity | `[src/**/*.cs]` |

The C# style preferences marked `suggestion` are not equivalent to errors. Production-only naming rules use `[src/**/*.cs]` rather than applying to every test file. Exact keys, symbolic names, accessibilities, modifiers and individual scopes are preserved in the [full configuration inventory](evidence/manifest.md#repository-configuration-original-item-46-inventory) and frozen source.

**D. Other configuration files**

[.gitignore](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.gitignore), [AGENTS.md](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/AGENTS.md) and [.github/copilot-instructions.md](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/copilot-instructions.md) are tracked. Their contents are documented by source links; they are not interchangeable with NuGet, EditorConfig or centralized MSBuild settings.

### 47. NuGet Package Declarations

Seven `packages.config` files, 17 declarations and 13 distinct pinned package IDs. Feed settings are declared, not proof of download origin.

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

### 48. Non-NuGet Dependencies

Framework references and other non-NuGet dependencies are separate inventories; dynamic runtime dependencies are not fully established.

**A. Framework Assembly References**

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

| Project | Dependencies | Type / Mechanism | Version / Identity | Resolution / Location | Declaration Source |
|---|---|---|---|---|---|

**C. Tracked internal resources and test fixtures — not third-party dependencies**

| Project | Tracked File | Declared Project Inclusion | Role / Scope |
|---|---|---|---|
| RecordSift.Application | [src/RecordSift.Application/Messages/Resources/CsvMessages.resx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Messages/Resources/CsvMessages.resx) | `EmbeddedResource`; logical resource name `RecordSift.Resources.CsvMessages.resources` | Internal production message resource |
| RecordSift.Domain | [src/RecordSift.Domain/Diagnostics/Resources/DomainMessages.resx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/Diagnostics/Resources/DomainMessages.resx) | `EmbeddedResource`; logical resource name `RecordSift.Resources.DomainMessages.resources` | Internal production message resource |
| RecordSift.Infrastructure.Reporting | [src/RecordSift.Infrastructure.Reporting/Resources/ReportingMessages.resx](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/Resources/ReportingMessages.resx) | `EmbeddedResource`; logical resource name `RecordSift.Resources.ReportingMessages.resources` | Internal production message resource |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/csv-provenance.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/csv-provenance.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/empty-import.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/empty-import.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/rejected-records.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/rejected-records.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/source-failure.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/source-failure.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/successful-import.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/successful-import.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/xlsx-provenance.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/xlsx-provenance.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |
| RecordSift.Infrastructure.Reporting.Tests | [tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/xlsx-source-failure.json](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/RecordSift.Infrastructure.Reporting.Tests/Fixtures/Compatibility/xlsx-source-failure.json) | `None Include="Fixtures\\Compatibility\\*.json"`; `CopyToOutputDirectory=PreserveNewest` | Compatibility test fixture |

### 49. Operation Commands

| Operation | Project or Solution | Configuration | Platform | Command or Workflow | Source |
|---|---|---|---|---|---|
| Restore (CI) | RecordSift.sln | Not applicable | Not applicable | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | .github/workflows/windows-net48.yml:38; .github/workflows/verify-rc-consumer.yml:29 |
| Build (CI) | RecordSift.sln | Release | Any CPU | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | .github/workflows/windows-net48.yml:43–47 |
| Build (documented local) | RecordSift.sln | Release | Any CPU | msbuild .\RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' | docs/engineering/baseline.md:19 |
| Test (CI direct NUnit, per assembly) | Five NUnit Release assemblies | Release | Windows 2022 | `& $runner $assemblies[$layer] "--result=TestResults/nunit-$layer.xml;format=nunit3" --noheader` | .github/workflows/windows-net48.yml:86–152 (default unfiltered CI branch; five separate invocations) |
| Test (CI direct NUnit, targeted) | Five NUnit Release assemblies | Release | Windows 2022 | `& $runner $assemblies.domain $assemblies.application $assemblies.adapter $assemblies.reporting $assemblies.xlsx "--where=$filter" "--result=TestResults/nunit-targeted.xml;format=nunit3" --noheader` | .github/workflows/windows-net48.yml:114–125 (manual filtered CI branch) |
| Test (CI full) | Five NUnit assemblies | Release | Any CPU | & .\scripts\run_tests.ps1 | .github/workflows/windows-net48.yml:154–169; scripts/run_tests.ps1 defaults Level=All |
| Test (supported explicit full) | Five NUnit assemblies | Release | Any CPU | .\scripts\run_tests.ps1 -Level All | scripts/run_tests.ps1:4–10 (valid but not exact CI command) |
| Test (CI filtered) | Five NUnit assemblies | Release | Any CPU | & .\scripts\run_tests.ps1 -Level Integration -Verification Acceptance -Requirement FR-017 -Scenario FR-017-SC01 | .github/workflows/windows-net48.yml:171–179 |
| Test (negative no-selection) | Five NUnit assemblies | Release | Any CPU | & .\scripts\run_tests.ps1 -Requirement FR-999 | .github/workflows/windows-net48.yml:181–188 (expected rejection) |
| Public API | Production assemblies | Release | Any CPU | & .\scripts\verify_public_api.ps1 | .github/workflows/windows-net48.yml:52–55 |
| Public API (negative gate) | Production assemblies | Release | Any CPU | & .\scripts\verify_public_api.ps1 -BaselineFile $tampered | .github/workflows/windows-net48.yml:56–69 (expected rejection) |
| XML documentation | Production assemblies | Release | Any CPU | & .\scripts\verify_xml_documentation.ps1 | .github/workflows/windows-net48.yml:48–51 |
| XML documentation (negative gate) | Production assemblies | Release | Any CPU | & .\scripts\verify_xml_documentation.ps1 -Negative | .github/workflows/windows-net48.yml:272–275 |
| IDE1006 style | RecordSift.sln | Not applicable | Not applicable | & dotnet format style RecordSift.sln --no-restore --verify-no-changes --diagnostics IDE1006 --severity error --verbosity normal | .github/workflows/windows-net48.yml:70–79 |
| NuGet audit restore | RecordSift.sln | Not applicable | Not applicable | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config -Verbosity normal | .github/workflows/windows-net48.yml:398–405 |
| Release candidate packaging | RecordSift | Release | Any CPU | & .\scripts\build_release_candidate.ps1 -OutputDirectory $feed | .github/workflows/verify-rc-consumer.yml:41–43 |
| Installed consumer verification | RecordSift | Release | Any CPU | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | .github/workflows/verify-rc-consumer.yml:41–44 |

| Test assembly | Release assembly path | Minimum discovered in unfiltered CI | Unfiltered result file |
|---|---|---:|---|
| Domain | `tests\RecordSift.Domain.Tests\bin\Release\RecordSift.Domain.Tests.dll` | 121 | `TestResults/nunit-domain.xml` |
| Application | `tests\RecordSift.Application.Tests\bin\Release\RecordSift.Application.Tests.dll` | 62 | `TestResults/nunit-application.xml` |
| CSV adapter | `tests\RecordSift.Infrastructure.Csv.Tests\bin\Release\RecordSift.Infrastructure.Csv.Tests.dll` | 122 | `TestResults/nunit-adapter.xml` |
| Reporting | `tests\RecordSift.Infrastructure.Reporting.Tests\bin\Release\RecordSift.Infrastructure.Reporting.Tests.dll` | 49 | `TestResults/nunit-reporting.xml` |
| XLSX | `tests\RecordSift.Infrastructure.Xlsx.Tests\bin\Release\RecordSift.Infrastructure.Xlsx.Tests.dll` | 33 | `TestResults/nunit-xlsx.xml` |
| **Total** | **Five separately invoked assemblies** | **387** | **NUnit3 XML** |

### 50. Restore Outcomes

Historical exact-commit CI restore and audit steps passed (EV-062). No fresh local NuGet restore was executed.

| Source Revision | Target | Outcome | Error or Note | Evidence |
|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln (Windows build/test CI) | Passed | `Restore packages.config dependencies` step succeeded in job `130945777245`; checkout SHA confirmed in job log | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln (independent consumer CI) | Passed | `Restore packages.config dependencies` step succeeded in job `130945777078`; checkout SHA confirmed in job log | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln (NuGet audit restore CI) | Passed | Audit job `130945777594` succeeded; log reports no `NU1900–NU1905` warnings; checkout SHA confirmed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |

### 51. Build Outcomes

Historical CI builds and the isolated SDK-only local Release build passed. Local execution built all ten projects (EV-081).

| Source Revision | Target | Configuration | Platform | Outcome | Warning Count | Error Count | Output or Evidence |
|---|---|---|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Release | Any CPU | Passed | Not recorded | Not recorded | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Release | Any CPU | Passed | Not recorded | Not recorded | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln (isolated operator-local copy) | Release | Not separately asserted | Passed (10/10 projects, 0.8 seconds) | 0 reported | 0 reported | EV-081; operator PowerShell output |

### 52. Test Outcomes

Five local NUnit suites: **419 discovered, 418 passed, 0 failed, 1 explicit skip** (EV-081). Existing CI independently reported matching results.

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Domain.Tests | NUnit ConsoleRunner 3.17.0 | 123 | 123 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Application.Tests | NUnit ConsoleRunner 3.17.0 | 62 | 62 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Csv.Tests | NUnit ConsoleRunner 3.17.0 | 132 | 131 | 0 | 1 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Reporting.Tests | NUnit ConsoleRunner 3.17.0 | 54 | 54 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Xlsx.Tests | NUnit ConsoleRunner 3.17.0 | 48 | 48 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |

### 53. CI Workflows

| Workflow Path | Triggers | Jobs | Runner OS | Purpose | Artifact or Deployment |
|---|---|---|---|---|---|
| [windows-net48.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/windows-net48.yml) | push, pull_request, workflow_dispatch | `build-test` | windows-2022 | Restore, build, NUnit and quality checks | Build and test evidence |
| [verify-rc-consumer.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/verify-rc-consumer.yml) | push, pull_request, workflow_dispatch | `verify-consumer` | windows-2022 | Build unpublished package and verify installed consumer | Consumer verification |
| [validate-docs.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/validate-docs.yml) | push, pull_request, workflow_dispatch | `docs` | ubuntu-latest | Validate engineering documentation and links | Documentation checks |
| [adversarial-extended.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/adversarial-extended.yml) | push, pull_request, workflow_dispatch | `extended-adversarial` | windows-2022 | Restore dependencies and test adversarial cases | Adversarial results |
| [extended-adversarial.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/extended-adversarial.yml) | push, pull_request, workflow_dispatch | `bounded-adversarial-stress` | windows-2022 | Run bounded stress tests with resource limits | Stress results |
| [prepare-0.1-release.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/prepare-0.1-release.yml) | workflow_dispatch | `prepare` | windows-2022 | Build package, verify consumer, record checksum | Prepared package |
| [publish-release.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/publish-release.yml) | workflow_dispatch | `prepare`, `publish`, `verify_public`, `github_release` | windows-2022, ubuntu-24.04 | Validate, publish, verify public package and create release | NuGet package and GitHub release |
| [recover-recordsift-0.1-release.yml](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/.github/workflows/recover-recordsift-0.1-release.yml) | workflow_dispatch | `verify_public`, `github_release` | windows-2022, ubuntu-24.04 | Verify published package and reconcile GitHub release | Release recovery |

**Conditions and gates:** Declared events may have branch/path filters, and job-specific conditions or dependencies can further constrain execution. The publishing workflow uses dependent jobs and a protected NuGet publication environment. Release recovery verifies an already-published package and should not be interpreted as a second package publication.

### 54. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
| Windows .NET Framework 4.8 build and test | https://github.com/infoconex/RecordSift/actions/runs/43146607664 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Verify internal release candidate in clean Windows consumer | https://github.com/infoconex/RecordSift/actions/runs/43146607706 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Validate engineering documentation | https://github.com/infoconex/RecordSift/actions/runs/43146607615 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |

### 55. Package and Release Artifacts

Source package declarations, unpublished CI package candidates and published artifacts are distinct.

**A. Source package declarations**

| Declaration | Declared Version | Source Committer Date (UTC) | Evidence |
|---|---|---|---|
| [packaging/RecordSift.nuspec](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/packaging/RecordSift.nuspec) | `0.1.0-rc.1` | `2026-11-12T03:12:18Z` | [Frozen source commit](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) |

**B. CI package artifacts and verification**

| Artifact | Version | Verification Result | Verification Completed (UTC) | Evidence |
|---|---|---|---|---|
| Unpublished CI package | `0.1.0-rc.1` | Passed (local-feed consumer; not published) | `2026-11-12T03:13:13Z` | [Windows package/consumer CI](https://github.com/infoconex/RecordSift/actions/runs/43146607706/job/130945777078) |
| Unpublished CI stable-package candidate | `0.1.0` | Passed (local-feed consumer; not published) | `2026-11-12T03:13:19Z` | [Windows package/consumer CI](https://github.com/infoconex/RecordSift/actions/runs/43146607706/job/130945777078) |

**C. Published artifacts**

| Artifact | Version | Status | Publication Date (UTC) | Evidence |
|---|---|---|---|---|
| RecordSift NuGet.org package | `0.1.0` | Published | `2026-11-01` (date verified; exact registry publication time not checked) | [NuGet.org package](https://www.nuget.org/packages/RecordSift/0.1.0) · [Public-feed consumer verification](https://github.com/infoconex/RecordSift/actions/runs/41355904536/job/124995742204) |
| GitHub Release `v0.1.0` | `v0.1.0` | Published | `2026-11-01T22:12:43Z` | [GitHub Release](https://github.com/infoconex/RecordSift/releases/tag/v0.1.0) |

| Source Context | Source Commit SHA | Committer Date (UTC) | Verification |
|---|---|---|---|
| Frozen discovery source (`main`) | [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) | `2026-11-12T03:12:18Z` | Commit metadata inspected; isolated local detached checkout verified (EV-033–035) |
| Published GitHub release tag (`v0.1.0`) | [`2db5c86bc26010afcb83c2e455d2471d8c9340d6`](https://github.com/infoconex/RecordSift/commit/2db5c86bc26010afcb83c2e455d2471d8c9340d6) | `2026-11-01T21:13:46Z` | Git tag and release metadata verified |
| Published NuGet package (`RecordSift 0.1.0`) | [`2db5c86bc26010afcb83c2e455d2471d8c9340d6`](https://github.com/infoconex/RecordSift/commit/2db5c86bc26010afcb83c2e455d2471d8c9340d6) | `2026-11-01T21:13:46Z` | Existing [public-feed verification CI](https://github.com/infoconex/RecordSift/actions/runs/41355904536/job/124995742204) confirmed package source; this is not an independently repeated download in this discovery |

### 56. Runtime and Deployment Requirements

| Requirement | Type | Target Environment | Source or Evidence |
|---|---|---|---|
| Windows | Supported operating system | RecordSift consumer | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md |
| .NET Framework 4.8 | Target framework | Consuming application | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md |
| No Excel installation required | Runtime constraint | XLSX reader | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md |

### 57. Compatibility Checks

Historical CI gates passed. The local SDK-only procedure separately verified building and standard NUnit tests; other CI gates were not independently rerun locally.

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

### 58. Executed Command Evidence

Detailed historical commands, environments, outputs and exit status are preserved in the [evidence manifest](evidence/manifest.md#detailed-executed-command-inventory-preserved-from-baseline-item-58), including the original item-58 inventory.

| Execution category | Outcome | Evidence |
|---|---|---|
| Frozen-source CI restore, build, test and quality gates | Passed | EV-062–063; items 50–57 |
| Operator-local SDK-only ten-project Release build | Passed | EV-071, EV-081 |
| Operator-local five standard NUnit suites | 418 passed, 0 failed, 1 explicit skip | EV-072, EV-081 |
| Final frozen checkout revision and cleanliness | Clean, detached, verified | EV-082 |

### 59. Findings and Gaps

All ten projects and five standard NUnit suites passed locally. 

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
| Machine-wide .NET Framework v4.8 reference assemblies absent at standard location | The local path check was negative, but NuGet package-provided v4.8 reference assemblies 1.0.3 allowed successful compilation and testing; no machine-wide Developer Pack installation is required for this verified approach | Item 31; EV-029, EV-065, EV-081 | Revisit only if another tool or workflow requires the machine-wide pack |
| SDK MSBuild differs from historical CI Visual Studio MSBuild | The local complete build and standard NUnit suites passed with SDK MSBuild 18.9.15.53019, while CI used Visual Studio MSBuild. Tooling parity is not exact, but observed build/test outcomes agree | Items 28–29, 51–52; EV-063, EV-065, EV-081 | Verify strict tool parity only if required for a specific compatibility question |
| Local package acquisition differs from CI restore | The validated script stages exact versions already cached under the user profile; it does not execute `nuget restore` or establish clean-machine package acquisition | Items 47, 50, 57; EV-062, EV-068, EV-081 | Repeat on a separately prepared host only if clean-room reproducibility is in scope |
| NUnit runner working-directory side effects | The first manual test run wrote ten untracked diagnostic files in the frozen checkout. Targeted cleanup restored clean Git status; later consolidated execution used an isolated `TestResults` working directory and emitted no source-status warning | EV-072–074, EV-081 | Keep an explicit work directory and verify Git cleanliness after future runs |
| Evaluated build-policy properties are not equivalent to compiler switches | CI evaluation found empty values for `Deterministic`, `TreatWarningsAsErrors` and `PlatformTarget`; this does not establish effective compiler flags | Item 44; [CI evidence](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) | Inspect actual compiler commands if modernization requires policy parity |
| Historical branch references in guidance | Some frozen source AI/PR guidance references `release/0.1`; present-day suitability is not established | Item 45; EV-045 | Check current branch policy before any separate RecordSift guidance change |
| Production/test validation declarations differ | Production projects explicitly declare `WarningsAsErrors=1591` and `DocumentationFile` whereas test projects do not; this is a declaration difference, not a failed validation | Item 42; EV-042 | Evaluate the desired test-project policy during modernization planning |

### 60. Deferred Checks

The three deferrals below were explicitly accepted (EV-083). Discovery is **Completed with gaps**.

| Check | Reason Deferred | Revisit When |
|---|---|---|
| Independent clean-host restore and SDK-only reproducibility | The successful local script used previously cached dependencies; a second clean Windows host and fresh package restoration have not been tested | If verifying setup from an empty cache or distribution of the procedure beyond this host |
| Exact operator-to-CI MSBuild evaluation/command parity | Historical CI used Visual Studio MSBuild and evaluated project properties; local SDK compilation/testing verified functionality but not every evaluated property or compiler flag | If an upgrade decision depends on compiler switches or environment-specific MSBuild behavior |
| Separate machine-wide Developer Pack or Visual Studio installation | Standard-path targeting assembly is absent; validated local build/test works with package-provided references and SDK MSBuild | Only if a newly identified tool requires these installations |

