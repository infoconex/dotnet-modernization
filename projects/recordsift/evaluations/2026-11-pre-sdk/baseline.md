# RecordSift — Verified baseline

**Repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Branch / full commit:** main / `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Verification date:** November 2, 2026

## Source and project inventory

Five production projects: RecordSift.Domain, RecordSift.Application, RecordSift.Infrastructure.Csv, RecordSift.Infrastructure.Xlsx, and RecordSift.Infrastructure.Reporting. Five corresponding NUnit test projects.

All ten use traditional, non-SDK-style `*.csproj` files, `TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, `OutputType=Library`, `AnyCPU`, `WarningLevel=4`, explicit compile/reference items, Debug/Release configurations, and imports of `Microsoft.CSharp.targets`.

Production-specific configuration generates XML documentation and enforces `CS1591` for documentation. Production assembly version is `0.1.0.0`. Preserve exact assembly and file metadata, project dependency ordering, output layouts, and per-assembly XML docs.

### Actual repeated settings

| Setting | Projects | Candidate | Reason |
|---|---:|---|---|
| C# language version 7.3 | 10 | Yes, verified | Identical across projects; safe isolated centralization tested. |
| Warning level 4 | 10 | Maybe later | Duplicated but change still requires evaluated-property proof. |
| Target .NET Framework v4.8 | 10 | Not yet | Public API checker reads raw project XML; centralization breaks current script assumption. |
| Debug/Release and output paths | 10 | Not initially | Existing build, test, and packaging paths depend on layout. |
| XML documentation and CS1591 | 5 production | Optional within src | Intentionally different from test projects. |
| Resource logical names | Resource-bearing projects | No | Exact names are compatibility contracts. |
| Package versions | Package-owning projects | Not with Directory.Packages.props yet | Current restore uses packages.config, not PackageReference. |

## NuGet and packaging

`NuGet.Config` explicitly defines sources/audit sources. Dependencies are declared in pinned `packages.config` files. CI uses standalone `nuget restore`. Packaging is defined by `packaging/RecordSift.nuspec`, including five `lib/net48` DLLs, XML documentation, README/license/notices and explicit dependencies.

Important resource identities:
- `RecordSift.Resources.CsvMessages.resources`
- `RecordSift.Resources.DomainMessages.resources`
- `RecordSift.Resources.ReportingMessages.resources`

## Baseline verification

| NUnit assembly | Discovered | Passed | Skipped |
|---|---:|---:|---:|
| Domain.Tests | 123 | 123 | 0 |
| Application.Tests | 62 | 62 | 0 |
| Infrastructure.Csv.Tests | 132 | 131 | 1 |
| Infrastructure.Reporting.Tests | 54 | 54 | 0 |
| Infrastructure.Xlsx.Tests | 48 | 48 | 0 |
| **Total** | **419** | **418** | **1** |

**Failed tests: 0.** The CSV skip is intentional, not an unexpected test failure. Existing validation confirms **425 public-API/packaging-metadata entries**, generated XML documentation and NuGet packaging. Existing CI also ran clean local package consumer and engineering-documentation workflows.

- [Main Windows build and tests](https://github.com/infoconex/RecordSift/actions/runs/41392848910)
- [Clean Windows consumer](https://github.com/infoconex/RecordSift/actions/runs/41392848814)
- [Engineering docs validation](https://github.com/infoconex/RecordSift/actions/runs/41392848879)

## Known documentation and script inconsistencies

- `scripts/run_tests.ps1` locally runs **four** assemblies, omitting Infrastructure.Xlsx.Tests. The CI workflow runs **five**. Always use the five-suite baseline when judging changes.
- Some engineering documentation says **379 tests**; the observed total is **419**.
- `scripts/verify_public_api.ps1` reads `$project.Project.PropertyGroup[0].TargetFrameworkVersion` from raw XML. Moving framework declaration to imported props would require first updating the checker to use evaluated MSBuild properties.
- The Windows PowerShell 5.1 host is significant for API verification: an initial experimental use of PowerShell 7 produced spurious reflection differences.

## Expected compatibility gates

Restore → Release build all ten projects → full five-suite NUnit (419/418/0/1) → 425-entry API/metadata baseline → assembly and embedded-resource identity checks → XML docs → package layout and dependency checks → clean installed-package consumer tests.

Do not interpret changed binary hashes or timestamps as compatibility failure unless deterministic equality is part of an explicit requirement.
