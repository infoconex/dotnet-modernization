# RecordSift — Discovery baseline

**Description:** RecordSift is a Windows .NET Framework 4.8 class library that imports CSV and XLSX records, maps source columns to typed models, validates records, and returns structured diagnostics and optional reports.

[Step-by-Step Instructions](../../../../methodology/technical-discovery-runbook.md)

## Discovery information

| Field | Value |
|---|---|
| 1. Discovery By | Not recorded |
| 2. Discovery Date | `2026-11-12` |
| 3. Discovery Status | In progress |
| 4. Discovery Completed Date | Not completed |

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

**A. Known Consumers**

| Consumer | Type | Evidence |
|---|---|---|
| `tests/ReleaseConsumer` | Test application | [Clean NuGet consumer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/ReleaseConsumer/Program.cs) |

**External production consumers:** Not identified in the inspected source or consumer documentation. A test consumer is not evidence of a deployed production application.

**B. Public Entry Points**

Only operations documented or demonstrated for **direct invocation by a consumer** are listed. Public supporting classes and delegate callbacks are not automatically consumer entry points.

| Entry Point | Purpose | Evidence |
|---|---|---|
| `CsvImporter<T>.Import` | Import CSV records | [CSV importer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Csv/CsvImporter.cs) |
| `CsvStreamImporterAdapter<T>.Import` | Import CSV from a byte stream | [CSV stream adapter source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs) |
| `XlsxImporter<T>.Import` | Import XLSX records | [XLSX importer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Application/Importing/Xlsx/XlsxImporter.cs) |
| `JsonImportResultSerializerAdapter.Serialize` | Generate JSON diagnostic reports | [JSON serializer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/JsonImportResultSerializerAdapter.cs) |
| `ReadableImportResultFormatterAdapter.Format` | Generate readable reports | [Readable formatter source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/ReadableImportResultFormatterAdapter.cs) |
| `CsvImportResultSerializerAdapter.Serialize` | Generate diagnostic CSV reports | [Diagnostic CSV serializer source](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Infrastructure.Reporting/CsvImportResultSerializerAdapter.cs) |

The [getting-started guide](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md) and [clean consumer example](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/tests/ReleaseConsumer/Program.cs) demonstrate or document these direct-call operations. `PrimitivePropertyMapper<T>.Map` is deliberately **not** listed: consumers supply it as an importer callback, rather than calling it directly in the documented import workflow.

## Discovery host and prerequisite tools

**Existing CI evidence:** [Windows host/tool inventory research job](https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480), executed 2026-11-13 UTC from draft RecordSift research PR #273. The job checked out the immutable application source `1809d06c0fade59e4769d16e0f8eaf10fa426004` on hosted `windows-2022` runner image `20261112.366.7` (`win22`). This is a **specific ephemeral CI machine**, not the operator's Windows environment. A separate [2026-11-12 application build/test run](https://github.com/infoconex/RecordSift/actions/runs/43146607664/job/130945777245) used an earlier runner image; its values are retained as historical evidence, not merged into the new image's complete tool inventory.

| Field | Existing CI Runner | Operator Local |
|---|---|---|
| 20. Operating System Name | Microsoft Windows Server 2022 Datacenter | Microsoft Windows 11 Pro |
| 21. Operating System Version | `10.0.20348` | `10.0.26300` |
| 22. Operating System Build | `20348` | `26300` |
| 23. Operating System Architecture | 64-bit | 64-bit |
| 24. PowerShell Version | `7.6.10` | `7.7.0` |
| 25. Git Version | `2.56.1.windows.1` | `2.56.0.windows.4` |

**Operator-provided local Windows OS output (EV-017, 2026-11-13):** The operator supplied four columns from the read-only `Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture` command (items 20–23). These values are operator-reported, not a CI measurement. PowerShell version, working directory and exit code were not recorded **for that OS command**. The operator subsequently reported PowerShell `7.7.0` from `D:\RecordSift` (EV-018). The operator subsequently reported local Git `2.56.0.windows.4` from `D:\RecordSift` (EV-019). Local tool items 26–31 remain unverified.

### 26. .NET SDK Inventory

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

**Scope:** All 12 SDK versions are the observed output of `dotnet --list-sdks` for the research runner. Their reported paths are SDK installation roots, not a claim that each version has a different path. **Operator-local evidence (EV-020, 2026-11-13):** `dotnet --list-sdks` at `D:\RecordSift` reported exactly three installed SDK versions: `8.0.428`, `9.0.321`, and `10.0.404`, all under `C:\Program Files\dotnet\sdk`. All three versions are also listed in the independent CI runner's 12-entry inventory. The different inventory sizes are not evidence of a build failure or a requirement to install the missing CI versions. This command does not enumerate .NET runtimes.

### 27. .NET Runtime Inventory

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

**Scope:** The 29 .NET runtime rows above were captured by `dotnet --list-runtimes` on the 2026-11-13 research runner. The separately labeled .NET Framework CLR observation comes from the earlier NUnit run, not from that command; its CLR version does not independently identify the .NET Framework product version. The research runner also recorded .NET Framework 4.x registry values and a direct v4.8 reference-assembly check (item 31). **Operator-local evidence (EV-021, 2026-11-13):** The operator reported 13 installed modern .NET runtime entries from `dotnet --list-runtimes` in `D:\RecordSift`. Nine exact name/version pairs also appear in the independent 29-entry CI inventory; four additional local entries are `Microsoft.NETCore.App` and `Microsoft.WindowsDesktop.App` at `6.0.36` and `7.0.20`. The inventory difference alone does not establish a RecordSift compatibility failure. Neither CLI command enumerates .NET Framework 4.8, which is separately checked in item 31.

| Field | Existing CI Runner | Operator Local |
|---|---|---|
| 28. MSBuild Version | `17.14.60.43110` | `4.8.10001.0` |
| 29. MSBuild Installation Source | Visual Studio Enterprise 2022 | Windows .NET Framework |
| 30. NuGet CLI Version | `8.0.0.137` | `7.9.0.83` |

**Tool provenance:** The [research job](https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480) resolved MSBuild at `C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\MSBuild.exe` through Visual Studio `vswhere` and resolved `nuget.exe` from `C:\ProgramData\Chocolatey\bin\nuget.exe`. These locations are runner observations, not operator-local paths.

**Operator-local NuGet inventory (EV-028, 2026-11-13):** Executing `nuget help` at `PS D:\RecordSift>` reported `NuGet Version: 7.9.0.83` followed by the standard CLI usage and command listing. The operator did not report `nuget.exe`'s executable path or a separate process exit code. This verifies the locally invoked NuGet CLI version but does not establish package sources, restore behavior, or compatibility with the CI runner's `8.0.0.137` version.

**Operator-local MSBuild evidence (EV-022–027, 2026-11-13):** The unqualified `msbuild -version -nologo` command was not recognized in the operator's PowerShell session (EV-022). A filtered Visual Studio `vswhere` query returned no matching MSBuild path (EV-023); the unfiltered registered-instance query returned only SQL Server Management Studio 22 (EV-024). The operator reported uninstalling Visual Studio 2026 Professional and planning a later Community installation (EV-025). A standard-directory search found `MSBuild.exe` in the Windows .NET Framework `Framework` and `Framework64` directories (EV-026). **Direct execution** of `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe` returned **`4.8.10001.0`** (EV-027), establishing the local legacy MSBuild version and `Windows .NET Framework` source recorded above. This is **not** the modern Visual Studio MSBuild `17.14.60.43110` recorded on the CI runner. The operator's modern VS MSBuild installation remains unverified until after the Community installation; the 32-bit legacy executable was not separately version-checked. Items 30–31 can be checked now without any installation.

### 31. .NET Framework Targeting Pack Inventory

| Environment | Framework Version | Installed | Location |
|---|---|---|---|
| Existing CI runner | `v4.8` | True | `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8` |
| Operator local | `v4.8` | False | `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8` |

**Direct CI file verification:** The [research job](https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480) confirmed `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8\mscorlib.dll` and `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8\RedistList\FrameworkList.xml` both exist. This establishes reference-assembly availability **on that runner**, rather than inferring it from a successful build. The runner's .NET Framework Full registry values were `Release=533509` and `Version=4.8.09221`; these are observed product-registration values, not a new minimum requirement for RecordSift.

**Operator-local targeting pack check (EV-029, 2026-11-13):** At `PS D:\RecordSift>`, the operator printed the computed local v4.8 reference-assembly directory `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8`. The direct `Test-Path -LiteralPath $referenceAssembly` check for `mscorlib.dll` returned **`False`**. The required v4.8 reference-assembly file is not present at that location on the operator's Windows desktop; this does **not** establish the presence or absence of the runtime, other pack files, or the cause. CI independently verified the corresponding file exists there (EV-016). This is a local build-prerequisite gap to revisit after installing the .NET Framework 4.8 developer/targeting pack, potentially alongside Visual Studio Community.

### 32. Test Runner Inventory

| Runner Name | Runner Version | Source or Location |
|---|---|---|
| NUnit ConsoleRunner (declared) | 3.17.0 | tests/RecordSift.Domain.Tests/packages.config |
| NUnit ConsoleRunner (operator local) | 3.17.0 | `D:\RecordSift\packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe` |

**Operator-local runner location (EV-030, 2026-11-13):** From `D:\RecordSift`, the operator searched for `nunit3-console.exe` on PATH and recursively within `.\packages`. The search returned `D:\RecordSift\packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe`. This confirms a locally discoverable executable in a `NUnit.ConsoleRunner.3.17.0` package directory; the package-directory version is `3.17.0`. **Direct version check (EV-031):** The operator then executed `nunit3-console.exe --version` using the discovered local path. It reported `NUnit Console 3.17.0+685c5b542b5e9ba632c905f0bd514a773d9758af (Release)`, independently confirming executable version **`3.17.0`**, consistent with the declared dependency. This version query did not run any RecordSift tests and does not establish the existing checkout matches the frozen discovery SHA.

## Source revision and checkout

| Field | Value |
|---|---|
| 33. Discovery Folder | `$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400` |
| 34. Selected Source Branch or Tag | `main` |
| 35. Source Commit SHA | `1809d06c0fade59e4769d16e0f8eaf10fa426004` |
| 36. Source Committer Date (UTC) | `2026-11-12T03:12:18Z` |
| 37. Working Tree Clean | True |
| 38. Detached HEAD | True |

**36. Source Committer Date (UTC)** records the timestamp of the exact commit being evaluated. It comes from the pinned [Git commit metadata](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004); it is **not** the discovery date, checkout time, first push, or release publication time. The operator has now performed an isolated local checkout at the selected revision (EV-033); the source committer date was also corroborated using local Git metadata. Working-tree cleanliness is still unverified.

**Operator-local discovery destination (EV-032, 2026-11-13):** The operator ran the item 33 PowerShell block, creating the parent discovery directory and printing an unused timestamped destination under their Windows home folder. The recorded path uses `$HOME` for the personal account-directory prefix in this public baseline, preserving the exact relative folder name and timestamp. **At that step**, only the parent directory was prepared; the actual clone and detached checkout were performed afterward (EV-033). Source branch `main` (item 34), pinned source SHA (item 35), and source committer date (item 36) were already independently established from GitHub. **Operator-local checkout and commit verification (EV-033):** The operator executed `git clone --no-checkout` to the previously unused destination, changed into the new checkout, and executed `git switch --detach` at the pinned `1809d06c0fade59e4769d16e0f8eaf10fa426004`. Git reported `HEAD is now at 1809d06`. The independent `git rev-parse HEAD` returned the exact pinned SHA, `git remote get-url origin` returned `https://github.com/infoconex/RecordSift.git`, and the commit metadata check returned `2026-11-12T03:12:18Z` in UTC. The safety checks for clone, switch and SHA mismatch did not throw. The original home-directory username is masked in the public baseline. This **verifies the isolated local source revision and corroborates item 36**, not a clean working tree: the clean-tree check for item 37 subsequently returned no output (EV-034), confirming `True` for the porcelain status snapshot (excluding ignored files); the operator subsequently reported that `git branch --show-current` produced no branch name (EV-035), verifying item 38 `True` alongside the successful pinned detached checkout (EV-033).

## Solution and project inventory

### 39. Solutions

One row per solution. The frozen `RecordSift.sln` declares **Debug** and **Release** configurations for the **Any CPU** platform. All ten projects are members of the solution, and all ten have `Build.0` mappings for **both** configurations; no build exclusions are declared for these two solution configurations. These are source-declared mappings, not independently executed builds.

**Operator-local solution filename inventory (EV-036, 2026-11-13):** Within the clean isolated checkout pinned to `1809d06c0fade59e4769d16e0f8eaf10fa426004`, the operator ran `git ls-files "*.sln" "*.slnx" "*.slnf"` and reported exactly one tracked path: `RecordSift.sln`. This independently corroborates the frozen source's single solution filename, but **does not yet independently validate local solution membership, format, header, configuration/platform pairs, or `Build.0` mappings**. **Local membership enumeration (EV-037):** The operator ran `dotnet sln .\RecordSift.sln list` from the pinned isolated checkout using .NET SDK `10.0.404`. All ten expected project paths were returned: five production projects (`src/`) and five test projects (`tests/`). The exact observed paths are `src\RecordSift.Application\RecordSift.Application.csproj`, `src\RecordSift.Domain\RecordSift.Domain.csproj`, `src\RecordSift.Infrastructure.Csv\RecordSift.Infrastructure.Csv.csproj`, `src\RecordSift.Infrastructure.Reporting\RecordSift.Infrastructure.Reporting.csproj`, `src\RecordSift.Infrastructure.Xlsx\RecordSift.Infrastructure.Xlsx.csproj`, `tests\RecordSift.Application.Tests\RecordSift.Application.Tests.csproj`, `tests\RecordSift.Domain.Tests\RecordSift.Domain.Tests.csproj`, `tests\RecordSift.Infrastructure.Csv.Tests\RecordSift.Infrastructure.Csv.Tests.csproj`, `tests\RecordSift.Infrastructure.Reporting.Tests\RecordSift.Infrastructure.Reporting.Tests.csproj`, `tests\RecordSift.Infrastructure.Xlsx.Tests\RecordSift.Infrastructure.Xlsx.Tests.csproj`. At that stage this independently verified **solution membership**, while the solution header, Debug/Release configuration pairs and `Build.0` mappings still required local text inspection; the later EV-038 completed that verification. **Observed first-run side effect:** The .NET 10 CLI displayed its first-run initialization banner and reported `Installed an ASP.NET Core HTTPS development certificate`; it offered a separate `dotnet dev-certs https --trust` command, which the operator did not run. The transcript also displayed a telemetry notice. No package restore, project build or test invocation was reported. The certificate creation means this command cannot be characterized as strictly side-effect-free on a first-run SDK. Inspect solution text without invoking .NET tooling when strict no-side-effect collection is required.

**Operator-local solution text inspection (EV-038, 2026-11-13):** The operator executed `Get-Content -LiteralPath .\RecordSift.sln` in the pinned isolated checkout and supplied the solution text. The header declares `.sln` format **`12.00`**, `VisualStudioVersion = 16.0.28701.123`, and `MinimumVisualStudioVersion = 10.0.40219.1`. It contains **10 project declarations**, five under `src/` and five under `tests/`, matching the independent `dotnet sln list` enumeration (EV-037). The only declared solution configuration/platform pairs are `Debug|Any CPU` and `Release|Any CPU`. Each of the 10 project GUIDs has a matching `.ActiveCfg` and `.Build.0` entry for **both** combinations: **20 `ActiveCfg` and 20 `Build.0` declarations** in all, with no declared solution-level build exclusions for these two configurations. This locally corroborates the existing source-inspected row below. Reading the file is **not evidence of a successful build**, and no restore, build or test was run.

| Solution Path | Format | Format Version | Declared IDE Version | Configurations | Platforms | Membership / Build Exclusions |
|---|---|---|---|---|---|---|
| RecordSift.sln | .sln | 12.00 | 16.0.28701.123 | Debug, Release | Any CPU | All 10 projects mapped to build in both Debug and Release; no declared build exclusions |

### 40. Projects

One row per project; direct references are grouped by project name. Each linked project name opens the immutable source file; the full repository-relative project path is recorded here as the authoritative mapping for subsequent project tables, which use linked project names without repeating paths.

**Operator-local project file enumeration (EV-039, 2026-11-13):** From the clean, detached checkout at the pinned SHA, `git ls-files "*.csproj" "*.fsproj" "*.vbproj"` returned **exactly ten tracked project files**, five under `src/` and five under `tests/`. Every returned path corresponds to one of the ten solution members independently verified in item 39 (EV-037–038); **no additional tracked C#, F# or Visual Basic project file** was reported. This independently confirms project-file count, names, paths and the absence of tracked projects outside the solution. It does **not** independently verify each `.csproj` file's framework, language version, output type, ToolsVersion, platform defaults or direct project references; those values were originally supported by existing source-inspected baseline evidence and have now been corroborated by local XML inspection (EV-040).

**Operator-local project XML declaration verification (EV-040, 2026-11-13):** In the isolated pinned checkout, the operator parsed all ten tracked `.csproj` files with PowerShell `[xml]` and `Get-Content -Raw`, and printed each project's declared target framework, language, output type, platform, root `ToolsVersion`/SDK attributes and direct `ProjectReference` paths. The output matches **all ten project rows below**: each has `TargetFrameworkVersion=v4.8`, `LangVersion=7.3`, `OutputType=Library`, `Platform=AnyCPU`, root `ToolsVersion=15.0` and an empty root `Sdk` attribute (traditional project format). All recorded direct project-reference sets match, including the `RecordSift.Application.Tests` reference from `RecordSift.Infrastructure.Csv.Tests`. No `TargetFramework` or `TargetFrameworks` element was declared in these project files. The query collects distinct XML values without preserving each property's conditional scope; this is **source-declaration evidence only**, not evaluated MSBuild property values, a verified build, or a dependency restore.

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

### 41. Compiler Settings

These are **source-declared** compiler properties, not independently evaluated MSBuild values. D/R means Debug / Release. Shared source conditions: Debug = `'$(Configuration)|$(Platform)' == 'Debug|AnyCPU'`; Release = `'$(Configuration)|$(Platform)' == 'Release|AnyCPU'`. `LangVersion` is unconditional. `Not declared` means no corresponding source declaration and does not imply `false`.

**Operator-local compiler declaration verification (EV-041, 2026-11-13):** In the isolated checkout pinned to `1809d06c0fade59e4769d16e0f8eaf10fa426004`, the operator read all ten tracked `.csproj` files as XML and examined each `PropertyGroup`, preserving its `Condition` value. The output contained **three relevant property groups for every project (30 groups total)**: unconditional `LangVersion=7.3`; condition `'$(Configuration)|$(Platform)' == 'Debug|AnyCPU'` declaring `DebugSymbols=true`, `DebugType=full`, `Optimize=false`, `DefineConstants=DEBUG;TRACE`; and condition `'$(Configuration)|$(Platform)' == 'Release|AnyCPU'` declaring `DebugType=pdbonly`, `Optimize=true`, `DefineConstants=TRACE`. There were **no differences across the ten projects** in these properties/conditions. `DebugSymbols` was **not declared in the inspected Release groups**, and must not be reported as explicitly `false`. All source-declaration values in the table below are now independently corroborated locally; the output does **not** establish effective values after imports, actual compiler switches, successful builds or test execution.

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

These are **source-declared** values. D/R means Debug / Release and uses the same shared conditions recorded in item 41. A single value is used when Debug and Release declarations agree. `Not declared` means the property is absent, not that MSBuild evaluated it as false or empty.

**Operator-local output and validation declaration verification (EV-042, 2026-11-13):** The operator inspected all ten tracked `.csproj` files as XML in the pinned isolated checkout, preserving each `PropertyGroup` condition. The console output contained exactly **20 relevant declaration groups**: one for `Debug|AnyCPU` and one for `Release|AnyCPU` in every project. All ten declare `OutputPath=bin\Debug\` or `bin\Release\`, respectively, and `WarningLevel=4` in both groups. All **five production** projects additionally declare `WarningsAsErrors=1591` and configuration-specific `DocumentationFile=bin\Debug\<project>.xml` / `bin\Release\<project>.xml`; none of the **five test** projects declares either field in the inspected groups. The other queried fields (`TreatWarningsAsErrors`, `NoWarn`, `WarningsNotAsErrors`, `GenerateDocumentationFile`) were not declared in these inspected `PropertyGroup` elements. These observations match the item 42 table, but are **source declarations**, not evaluated compiler options or confirmation that XML files were generated. The production/test distinction is a documented policy difference, not automatically a defect.

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

### 43. Project Metadata and Imports

These are project-file metadata and **explicit** imports, not evaluated MSBuild values. **Configuration Fallback** is the source-declared `Debug` value only when `$(Configuration)` is empty; it does **not** establish the configuration used during an actual build. `Not declared` means the property was absent from the inspected project XML. Each project name links to its immutable source file; the authoritative repository-relative project paths are in item 40.

**Operator-local project metadata and import verification (EV-043, 2026-11-13):** In the isolated pinned checkout, the operator read all ten tracked `.csproj` files as XML and reported declared `Configuration`, `IsTestProject`, `FileAlignment`, `AppDesignerFolder` and explicit `Import` nodes together with their node or parent conditions. **All ten projects** declare `Configuration=Debug` only when `'$(Configuration)' == ''` (a **fallback**, not an observed Debug build). All **five test projects** explicitly declare `IsTestProject=true`; that property is **not declared** in the five production project files. `FileAlignment=512` is unconditionally declared in **eight projects** and absent in both Xlsx projects. `AppDesignerFolder=Properties` is unconditionally declared in **six projects** (Application, Domain and Csv production/test pairs) and absent in the four Reporting/Xlsx projects. Every project has the same unconditional explicit import, `$(MSBuildToolsPath)\Microsoft.CSharp.targets`. The operator's output agrees with all ten source-inspected rows below. Imports were **listed, not executed**, and source fallback conditions were **not evaluated**. No local restore, build or test was run.

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

**Actual CI evaluation:** [Windows MSBuild property query](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) (run [43501555831](https://github.com/infoconex/RecordSift/actions/runs/43501555831)) executed on 2026-11-13 using MSBuild `17.14.60.43110`, `windows-2022` runner image `20261101.353.1`, and the exact frozen source commit `1809d06c0fade59e4769d16e0f8eaf10fa426004`. The read-only workflow used `-getProperty` without a build or restore target and successfully evaluated **18 named properties × 10 projects × 2 configurations (Debug and Release, AnyCPU)**. The complete machine-readable output is retained as CI artifact `recordsift-msbuild-item44-43501555831` (EV-015). These are **CI runner evaluations**, not operator-local checks.

**Common evaluated values:** `WarningLevel=4`, `DebugType=full` and `DefineConstants=DEBUG;TRACE` in Debug, versus `DebugType=pdbonly` and `DefineConstants=TRACE` in Release; `OutputPath` resolves to the corresponding `bin\\Debug\\` or `bin\\Release\\`. `DebugSymbols=true` in Debug and empty in Release. `TargetFramework`, `PlatformTarget`, `TreatWarningsAsErrors`, `Deterministic`, `GenerateDocumentationFile`, `Nullable` and `ContinuousIntegrationBuild` all returned **empty strings** for all 20 evaluations; an empty value must **not** be interpreted as explicit `false` or proof of a compiler's actual switch setting.

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

**Comparison result:** The directly declared values inspected for the included core properties, configuration-dependent values, assembly names and XML documentation paths match the corresponding evaluated results for all ten projects. No divergence was found in those comparisons. The full CI artifact retains all 18 queried values per project/configuration, including values not repeated in this summary table. Exact effective compiler switches and an independent operator-local evaluation remain outside the scope of this CI property query.

## Repository structure and dependencies

### 45. Repository Directories

| Directory | Purpose |
|---|---|
| src/ | Production code |
| tests/ | Automated tests and release consumer |
| docs/ | Requirements, specifications and guides |
| scripts/ | Build, test and validation utilities |
| packaging/ | Package manifests |
| .github/workflows/ | CI and release automation |

### 46. Repository Configuration

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
### 47. NuGet Package Declarations

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

### 48. Non-NuGet Dependencies

Inventory **framework assembly references** separately from other **non-NuGet dependencies**. Project references belong in item 40 and NuGet packages in item 47. The entries below are source declarations from the frozen commit, not proof of installed assemblies or successful resolution. Linked project names resolve to canonical project paths in item 40. Runtime discovery, dynamically loaded dependencies and external service usage have not been comprehensively checked.

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

### 49. Operation Commands

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

### 50. Restore Outcomes

| Source Revision | Target | Outcome | Error or Note | Evidence |
|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Passed | Not applicable | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Passed | Not applicable | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

### 51. Build Outcomes

| Source Revision | Target | Configuration | Platform | Outcome | Warning Count | Error Count | Output or Evidence |
|---|---|---|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Release | Any CPU | Passed | Not recorded | Not recorded | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.sln | Release | Any CPU | Passed | Not recorded | Not recorded | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

### 52. Test Outcomes

| Source Revision | Test Project or Assembly | Runner | Discovered | Passed | Failed | Skipped | Outcome | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Domain.Tests | NUnit ConsoleRunner 3.17.0 | 123 | 123 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Application.Tests | NUnit ConsoleRunner 3.17.0 | 62 | 62 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Csv.Tests | NUnit ConsoleRunner 3.17.0 | 132 | 131 | 0 | 1 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Reporting.Tests | NUnit ConsoleRunner 3.17.0 | 54 | 54 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 1809d06c0fade59e4769d16e0f8eaf10fa426004 | RecordSift.Infrastructure.Xlsx.Tests | NUnit ConsoleRunner 3.17.0 | 48 | 48 | 0 | 0 | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |

### 53. CI Workflows

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

### 54. CI Runs

| Workflow | Run URL | Commit SHA | Outcome | Date |
|---|---|---|---|---|
| Windows .NET Framework 4.8 build and test | https://github.com/infoconex/RecordSift/actions/runs/43146607664 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Verify internal release candidate in clean Windows consumer | https://github.com/infoconex/RecordSift/actions/runs/43146607706 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |
| Validate engineering documentation | https://github.com/infoconex/RecordSift/actions/runs/43146607615 | 1809d06c0fade59e4769d16e0f8eaf10fa426004 | Success | 2026-11-12 |

### 55. Package and Release Artifacts

Source declarations, **unpublished CI artifacts**, and **published distributions** are recorded separately. The dates below identify the source snapshot, a CI verification result, or a publication event; they are not interchangeable. Dates/times use UTC, with day-only precision where an exact time is unverified.

**A. Source package declarations**

| Declaration | Declared Version | Source Committer Date (UTC) | Evidence |
|---|---|---|---|
| [packaging/RecordSift.nuspec](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/packaging/RecordSift.nuspec) | `0.1.0-rc.1` | `2026-11-12T03:12:18Z` | [Frozen source commit](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) |

The source timestamp is the frozen Git **committer date**; it does not establish when the nuspec's version was first introduced. The local detached checkout independently returned the same committer timestamp for the selected SHA (EV-033).

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
### 56. Runtime and Deployment Requirements

| Requirement | Type | Target Environment | Source or Evidence |
|---|---|---|---|
| Windows | Supported operating system | RecordSift consumer | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md |
| .NET Framework 4.8 | Target framework | Consuming application | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md |
| No Excel installation required | Runtime constraint | XLSX reader | https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/docs/usage/getting-started.md |

### 57. Compatibility Checks

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

### 58. Executed Command Evidence

| Baseline Item | Command | Working Directory | Tool Version | Target or Configuration | Exit Code | Outcome | Output or Evidence |
|---|---|---|---|---|---|---|---|
| 50 | nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | GitHub Actions Windows checkout | NuGet CLI (version not logged) | RecordSift.sln | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 51 | & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | GitHub Actions Windows checkout | MSBuild 17.14.60.43110 | Release; Any CPU | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 52 | & .\scripts\run_tests.ps1 | GitHub Actions Windows checkout | NUnit ConsoleRunner 3.17.0 | Five Release test assemblies | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 57 | & .\scripts\verify_public_api.ps1 | GitHub Actions Windows checkout | PowerShell (version not logged) | net48 Release | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607664 |
| 57 | & .\scripts\verify_clean_consumer.ps1 -CandidateDirectory $feed | GitHub Actions Windows checkout | PowerShell (version not logged) | Local candidate package | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43146607706 |

| 20 | Get-CimInstance Win32_OperatingSystem -ErrorAction Stop | GitHub Actions research runner | PowerShell Core 7.6.10 | OS name/version/build/architecture | Not applicable | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 24 | $PSVersionTable.PSVersion.ToString() | GitHub Actions research runner | PowerShell Core 7.6.10 | PowerShell version | Not applicable | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 25 | git --version | GitHub Actions research runner | Git 2.56.1.windows.1 | Git version | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 26 | & $dotnet.Source --list-sdks | GitHub Actions research runner | dotnet CLI | 12 SDK entries | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 27 | & $dotnet.Source --list-runtimes | GitHub Actions research runner | dotnet CLI | 29 .NET runtime entries | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 28 | & $msbuildPath -version -nologo | GitHub Actions research runner | MSBuild 17.14.60.43110 | MSBuild version | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 30 | & $nugetCommand.Source help | GitHub Actions research runner | NuGet 8.0.0.137 | NuGet CLI version | Not recorded | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |
| 31 | Test-Path -LiteralPath $referenceAssembly -PathType Leaf; Test-Path -LiteralPath $frameworkList -PathType Leaf | GitHub Actions research runner | PowerShell Core 7.6.10 | Targeting reference files | Not applicable | Passed | https://github.com/infoconex/RecordSift/actions/runs/43514868868/job/132194144480 |

| 20–23 | Get-CimInstance Win32_OperatingSystem \| Select-Object Caption, Version, BuildNumber, OSArchitecture | Operator PowerShell session (directory not recorded) | PowerShell version not yet checked | Windows OS identity, version, build, architecture | Not recorded | Output supplied | EV-017; operator-provided result in discovery conversation, 2026-11-13 |

| 24 | $PSVersionTable.PSVersion.ToString() | Operator PowerShell session (`D:\RecordSift`) | PowerShell 7.7.0 (self-reported) | Active PowerShell version | Not recorded | Output supplied | EV-018; operator-provided output in discovery conversation, 2026-11-13 |

| 25 | git --version | Operator PowerShell session (`D:\RecordSift`) | Git 2.56.0.windows.4 (self-reported) | Git version | Not recorded | Output supplied | EV-019; operator-provided output in discovery conversation, 2026-11-13 |

| 26 | dotnet --list-sdks | Operator PowerShell session (`D:\RecordSift`) | .NET CLI (selected SDK version not separately queried) | Three installed SDKs: 8.0.428, 9.0.321, 10.0.404 | Not recorded | Output supplied | EV-020; operator-provided output in discovery conversation, 2026-11-13 |

| 27 | dotnet --list-runtimes | Operator PowerShell session (`D:\RecordSift`) | .NET CLI (selected SDK version not separately queried) | Thirteen installed modern .NET runtime name/version/path entries | Not recorded | Output supplied | EV-021; operator-provided output in discovery conversation, 2026-11-13 |

| 28 | msbuild -version -nologo | Operator PowerShell session (`D:\RecordSift`) | Not resolved on PATH | Version query (no MSBuild executable located) | Not recorded | Command not recognized; no version returned | EV-022; operator-provided PowerShell error in discovery conversation, 2026-11-13 |

| 28–29 | vswhere -latest -products * -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Operator PowerShell session (`D:\RecordSift`) | Visual Studio Installer vswhere (version not reported) | Find registered MSBuild installations; locator path existed | Not recorded | No matching MSBuild path returned | EV-023; operator-provided console output with no results, 2026-11-13 |

| 28–29 | vswhere -all -products * -format json (ConvertFrom-Json; select displayName, installationVersion, installationPath) | Operator PowerShell session (`D:\RecordSift`) | vswhere (version not reported) | Registered Visual Studio-family instance list | Not recorded | Only SQL Server Management Studio 22 instance reported | EV-024; operator-provided console output in discovery conversation, 2026-11-13 |

| 28–29 | Get-ChildItem -LiteralPath $root -Filter MSBuild.exe -File -Recurse (standard-directory search) | Operator PowerShell session (`D:\RecordSift`) | PowerShell 7.7.0 | Search common local Visual Studio and .NET Framework MSBuild locations | Not recorded | Two paths under `C:\Windows\Microsoft.NET\Framework` and `Framework64` reported; no modern VS-path match reported | EV-026; operator-provided search output in discovery conversation, 2026-11-13 |

| 28–29 | & "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe" -version -nologo | Operator PowerShell session (`D:\RecordSift`) | Windows .NET Framework MSBuild 4.8.10001.0 | Legacy MSBuild executable version | Not recorded | Version 4.8.10001.0 returned | EV-027; operator-provided console output in discovery conversation, 2026-11-13 |

| 30 | nuget help | Operator PowerShell session (`D:\RecordSift`) | NuGet 7.9.0.83 (reported by CLI) | NuGet CLI version and available commands | Not recorded | Printed NuGet version 7.9.0.83 and command usage | EV-028; operator-provided console output in discovery conversation, 2026-11-13 |

| 31 | $pack; Test-Path -LiteralPath $referenceAssembly | Operator PowerShell session (`D:\RecordSift`) | PowerShell 7.7.0 | .NET Framework v4.8 `mscorlib.dll` at `C:\Program Files (x86)\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8` | Not recorded | False (required reference assembly not present at checked path) | EV-029; operator-provided console output in discovery conversation, 2026-11-13 |

| 32 | Get-Command nunit3-console.exe; Get-ChildItem .\packages -Filter nunit3-console.exe -File -Recurse | Operator PowerShell session (`D:\RecordSift`) | PowerShell 7.7.0 | Locate local NUnit ConsoleRunner executable | Not recorded | One executable path found under NUnit.ConsoleRunner.3.17.0 package directory | EV-030; operator-provided PowerShell output in discovery conversation, 2026-11-13 |

| 32 | & ".\packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe" --version | Operator PowerShell session (`D:\RecordSift`) | NUnit ConsoleRunner 3.17.0 (Release) | Installed NUnit executable version | Not recorded | Version `3.17.0+685c5b542b5e9ba632c905f0bd514a773d9758af` reported | EV-031; operator-provided output in discovery conversation, 2026-11-13 |

| 33 | New-Item -ItemType Directory; Join-Path; Test-Path -LiteralPath $destination; $destination | Operator PowerShell session (`D:\RecordSift`) | PowerShell 7.7.0 | Unique timestamped discovery destination under operator home directory | Not recorded | Destination `$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400` printed; no clone performed | EV-032; operator-provided console output in discovery conversation, 2026-11-13; home-directory account name generalized in public evidence |

| 33–36 | git clone --no-checkout $remoteUrl $destination; git switch --detach $selectedCommit; git rev-parse HEAD; git remote get-url origin; git show -s --format='%cI' HEAD | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | Git 2.56.0.windows.4 (previously observed, EV-019) | RecordSift origin, pinned source SHA and UTC committer timestamp | Not recorded separately | Clone/checkout succeeded; HEAD exact match; origin URL correct; UTC committer date matched | EV-033; operator-provided PowerShell transcript in discovery conversation, 2026-11-13; home prefix masked |

| 37 | git status --porcelain=v1 --untracked-files=all | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | Git 2.56.0.windows.4 (previously observed, EV-019) | Tracked changes and untracked files in pinned isolated checkout (ignored files excluded) | Not recorded separately | No output; working tree clean under requested status scope | EV-034; operator-provided PowerShell transcript in discovery conversation, 2026-11-13; home directory prefix masked |

| 38 | git branch --show-current | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | Git 2.56.0.windows.4 (previously observed, EV-019) | Current local branch name in pinned discovery checkout | Not recorded | Operator reported no output; detached HEAD confirmed with earlier detached checkout | EV-035; operator statement in discovery conversation, 2026-11-13; terminal transcript for this command not supplied |

| 39 | git ls-files "*.sln" "*.slnx" "*.slnf" | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | Git 2.56.0.windows.4 (previously observed, EV-019) | Tracked solution files at pinned source SHA | Not recorded | One tracked solution file: `RecordSift.sln` | EV-036; operator-provided output in discovery conversation, 2026-11-13 |

| 39 | dotnet sln .\RecordSift.sln list | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | .NET SDK 10.0.404 | Enumerate solution membership at pinned SHA | Not recorded | 10 project paths reported: 5 production and 5 test; SDK first-run banner reported installing ASP.NET Core HTTPS development certificate | EV-037; operator-provided PowerShell console output in discovery conversation, 2026-11-13 |

| 39 | Get-Content -LiteralPath .\RecordSift.sln | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | PowerShell 7.7.0 (previously observed, EV-018) | Inspect solution format, IDE versions, 10 project declarations and Debug/Release build mappings | Not applicable (PowerShell read operation) | Header and 2 solution configuration pairs matched; 10 projects with 20 ActiveCfg and 20 Build.0 mappings; no declared build exclusions | EV-038; operator-provided PowerShell transcript in discovery conversation, 2026-11-13 |

| 40 | git ls-files "*.csproj" "*.fsproj" "*.vbproj" | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | Git 2.56.0.windows.4 (previously observed, EV-019) | Tracked project file inventory across whole selected repository | Not recorded | Exactly 10 .csproj files: 5 source and 5 test; all match solution membership, no other tracked project files returned | EV-039; operator-provided console output in discovery conversation, 2026-11-13 |

| 40 | git ls-files '*.csproj' '*.fsproj' '*.vbproj'; [xml] Get-Content -LiteralPath $file -Raw; SelectNodes for framework, language, output, platform and ProjectReference | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | PowerShell 7.7.0 (previously observed, EV-018) | All ten project files: root SDK/ToolsVersion and declared XML properties and direct project references | Not recorded | Ten project summaries matched the pinned source-inspected item 40 table, including all direct references; no restore/build/test | EV-040; operator-provided PowerShell output in discovery conversation, 2026-11-13 |

| 41 | git ls-files '*.csproj'; Get-Content -LiteralPath $file -Raw; XML PropertyGroup and Condition inspection | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | PowerShell 7.7.0 (previously observed, EV-018) | All ten projects; unconditional and Debug/Release source compiler declarations | Not recorded separately | 30 relevant property groups across 10 projects; all source-declared LangVersion, DebugSymbols, DebugType, Optimize and DefineConstants values and conditions matched item 41 | EV-041; operator-provided PowerShell transcript in discovery conversation, 2026-11-13 |

| 42 | git ls-files '*.csproj'; Get-Content -LiteralPath $file -Raw; inspect OutputPath, WarningLevel, WarningsAsErrors, DocumentationFile and other validation properties with PropertyGroup conditions | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | PowerShell 7.7.0 (previously observed, EV-018) | Ten projects, Debug/Release source output and validation declarations | Not recorded separately | 20 Debug/Release groups; all declare output path and warning level 4; production-only WarningsAsErrors 1591 and XML documentation paths; test groups omit both | EV-042; operator-provided PowerShell transcript in discovery conversation, 2026-11-13 |

| 43 | git ls-files '*.csproj'; Get-Content -LiteralPath $file -Raw; inspect Configuration, IsTestProject, FileAlignment, AppDesignerFolder and Import nodes with conditions | Operator PowerShell session (`$HOME\source\discoveries\RecordSift-discovery-2026-11-13-145400`) | PowerShell 7.7.0 (previously observed, EV-018) | Ten projects: conditional configuration fallback, test metadata, alignment, designer folder and explicit imports | Not recorded separately | Ten fallback Debug declarations; five explicit test flags; eight file-alignment and six designer-folder declarations; all ten import Microsoft.CSharp.targets unconditionally | EV-043; operator-provided PowerShell transcript in discovery conversation, 2026-11-13 |

### 59. Findings and Gaps

| Finding | Impact | Evidence | Next Check |
|---|---|---|---|
| Operator Windows development-tool readiness incomplete | Local OS, PowerShell, Git, SDK/runtime inventories verified (EV-017–021); legacy .NET Framework MSBuild `4.8.10001.0` verified (EV-027), NuGet CLI `7.9.0.83` verified (EV-028), and NUnit ConsoleRunner `3.17.0` executable version verified (EV-030–031). Modern Visual Studio MSBuild is not verified after the Professional uninstall (EV-022–026); the v4.8 reference-assembly check returned `False` (EV-029). This prevents treating local .NET Framework 4.8 build prerequisites as satisfied | Items 20–32; EV-016–031 | Proceed to isolated checkout preparation (item 33) for source inspection; after Community/developer-pack installation verify modern MSBuild and repeat v4.8 reference-assembly check before local build |
| Required .NET Framework 4.8 reference assembly missing at local checked path | Operator's direct `Test-Path` for `v4.8\mscorlib.dll` returned `False` versus `True` in CI; this is a confirmed local build-prerequisite gap at that path, not a RecordSift source-code failure or proof the runtime is missing | Item 31; EV-016, EV-029 | Install or restore the .NET Framework 4.8 developer/targeting pack as appropriate, then repeat the direct file check before attempting a local build |
| NUnit executable verified; local tests not yet executed | Local `nunit3-console.exe --version` reported `3.17.0`, consistent with the declared package (EV-030–031); no operator-local tests or checkout SHA verification have occurred | Item 32; EV-030–031 | Record test execution only after isolated source checkout, build prerequisites and approved build/test execution |
| Isolated checkout and source declarations through metadata/imports verified | The pinned clean detached checkout, solution and ten tracked project source files were corroborated (EV-033–040). Conditional compiler settings and output/validation declarations were confirmed locally (EV-041–042). Project metadata and explicit imports were also independently checked (EV-043), confirming the conditional Debug fallback, five `IsTestProject=true` flags, selective alignment/designer-folder declarations and shared unconditional C# targets import. These are project-file declarations; they do not establish effective MSBuild values, successful imports or build outcomes | Items 33–43; EV-032–043 | Item 44 already has CI-evaluated properties (EV-015); defer operator-local property parity until modern MSBuild and targeting pack are available. Next inspect tracked repository directory structure (item 45) |
| Operator-local MSBuild evaluation outstanding | CI evaluated 20 project/configuration scopes; local tool/import differences remain unverified | Item 44; EV-015 | Evaluate the same properties on an approved operator Windows checkout if local parity is required |
| Build-policy properties not explicitly set in evaluated results | `Deterministic`, `TreatWarningsAsErrors` and `PlatformTarget` returned empty strings; the output alone does not establish compiler-switch behavior | Item 44; [CI evidence](https://github.com/infoconex/RecordSift/actions/runs/43501555831/job/132148357265) | Inspect actual compiler invocations and existing build gates before proposing policy changes |
| Production/test validation declaration difference | Source inspection and operator-local XML confirmation show `WarningsAsErrors=1591` and `DocumentationFile` for five production projects in both Debug/Release, but neither property is declared in the five test project groups. The difference may be intentional and is not evidence of disabled warnings or failed documentation generation | Item 42; EV-042 | Preserve the distinction; review the intended policy when assessing modernization improvements, without changing the frozen baseline |
| CI outcomes are not local execution evidence | CI success cannot verify operator environment | Items 50–52 | Restore, build and run tests in the approved Windows checkout |

### 60. Deferred Checks

| Check | Reason Deferred | Revisit When |
|---|---|---|
| Modern Visual Studio MSBuild verification | Local legacy .NET Framework MSBuild `4.8.10001.0` (items 28–29, EV-027), NuGet CLI `7.9.0.83` (item 30, EV-028), and NUnit ConsoleRunner `3.17.0` (item 32, EV-031) verified; modern Visual Studio MSBuild corresponding to CI has not been observed since Professional was uninstalled | After Visual Studio Community installation, verify modern MSBuild executable version and path; proceed with isolated checkout/source inspection without claiming local build readiness |
| .NET Framework 4.8 targeting-pack remediation | The required v4.8 reference assembly `mscorlib.dll` is absent at the checked desktop location (EV-029), unlike the CI runner (EV-016) | After developer/targeting pack installation, rerun item 31 direct file check before local build |
| Local restore/build/test readiness | Local pinned checkout is clean (EV-034) and detached (EV-035), but modern Visual Studio MSBuild and the v4.8 reference assembly have not been verified available (EV-022–029) | After Visual Studio Community and .NET Framework 4.8 developer/targeting tools are installed and checked; read-only source inventory can proceed now |
| Operator-local MSBuild property parity | Existing CI evaluated the frozen source (EV-015); local tool/import parity remains unverified | If local parity is required, after host preflight and checkout |
| Local restore/build/test | Operator approval and environment verification required | After source checkout and side-effect review |

This baseline records observed application facts and verification outcomes, not proposed modernization work.
