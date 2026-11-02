# EXP-004 — Build traditional .NET Framework without Visual Studio Build Tools

**Objective:** Separate actual build requirements from tools incidentally installed on a preconfigured runner.  
**Baseline application:** infoconex/RecordSift main at `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Experimental workflow branch:** `discovery/sdk-only-20261102`  
**Experimental workflow SHA:** `231ae63f8a0435dbc8a1b7a5a4319d4ec8bd0825`  
**Work state:** Complete  
**Evidence outcome:** Verified: compilation and NUnit do not require VS IDE or Build Tools

## Environment

**Official Windows image:**

    mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022

**Immutable digest:**

    sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25

The image ran in **process isolation** on the GitHub `windows-2022` host. In-container inventory:
- OS: Windows Server 2022 Datacenter `10.0.20348`.
- VS IDE: **absent**.
- Visual Studio Build Tools: **absent**.
- Standalone `MSBuild.exe`: not found.
- .NET SDK: `10.0.403`.
- `dotnet msbuild`: `18.9.15.52412`.
- SDK compiler: `C:\Program Files\dotnet\sdk\10.0.403\Roslyn\bincore\csc.dll`.
- .NET 10 runtimes present at `10.0.14`; Windows .NET Framework runtime present.
- .NET Framework 4.8 **reference assemblies initially absent**.
- `DOTNET_RUNNING_IN_CONTAINER=true`, `DOTNET_SDK_VERSION=10.0.403` and `NUGET_XMLDOC_MODE=skip` among reported container variables.

**Added during experimentation only (outside repo):**
- NuGet CLI `6.14.0.116`.
- `Microsoft.NETFramework.ReferenceAssemblies.net48` package **1.0.3**, yielding v4.8 reference assemblies under `C:\sdktools\packages\...`.

## Test sequence and actual results

1. Unmodified traditional Domain project using `dotnet msbuild` **without** net48 targeting references: **failed** with `MSB3644` (expected negative control).
2. Install only standalone NuGet CLI and net48 targeting reference assemblies; pass `TargetFrameworkRootPath` and `FrameworkPathOverride` explicitly: **Domain built**.
3. Restore all existing `packages.config` dependencies with NuGet CLI: **passed**.
4. Rebuild complete unchanged traditional solution using SDK-provided MSBuild: **all ten projects built**.
5. Run all five NUnit suites in the same container: **419 discovered / 418 passed / 0 failed / 1 skipped**.

Representative commands, with paths resolved from the installed reference-assemblies package:

    dotnet msbuild src\RecordSift.Domain\RecordSift.Domain.csproj /t:Rebuild /p:Configuration=Release "/p:TargetFrameworkRootPath=<ref-pack-build-root>" "/p:FrameworkPathOverride=<v4.8-directory>"

    nuget restore RecordSift.sln -NonInteractive -PackagesDirectory C:\repo\packages -ConfigFile NuGet.Config

    dotnet msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release "/p:Platform=Any CPU" "/p:TargetFrameworkRootPath=<ref-pack-build-root>" "/p:FrameworkPathOverride=<v4.8-directory>" /v:minimal

Exact container orchestration, installation steps, paths and NUnit arguments are preserved in the [isolated workflow](https://github.com/infoconex/RecordSift/blob/231ae63f8a0435dbc8a1b7a5a4319d4ec8bd0825/.github/workflows/pre-sdk-sdk-only.yml).

## Evidence

- [Successful Windows SDK-only experiment](https://github.com/infoconex/RecordSift/actions/runs/41486238239).
- Archived diagnostic artifact **13162920363** (`sdk-only-windows-discovery-41486238239`).
- Container digest and tool inventory above.

## Conclusion and scope

**Verified:** RecordSift's existing traditional .NET Framework 4.8 projects can restore, compile and execute their full NUnit suite without VS IDE or Visual Studio Build Tools, while keeping Windows and the .NET Framework runtime.

**Not verified:** full API-checker, XML verification, packaging, security audit and clean installed-package consumer scripts inside this same minimal environment. Do not claim end-to-end release readiness or cross-platform support from this experiment.
