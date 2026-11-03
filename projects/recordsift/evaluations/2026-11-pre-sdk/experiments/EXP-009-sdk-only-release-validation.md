# EXP-009 — SDK-only Windows packaging and consumer follow-up

**Date:** November 3, 2026  
**Tracking:** [dotnet-modernization issue #7](https://github.com/infoconex/dotnet-modernization/issues/7)  
**Predecessor:** [EXP-007](EXP-007-sdk-only-release-gates.md) (preserved, not retroactively changed)  
**Frozen application baseline:** `infoconex/RecordSift` `main` = `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Disposable app research branch:** `research/sdk-only-release-followup-20261103` (created directly from the frozen baseline)  
**Research-only changes:** a GitHub Actions workflow. During execution it creates untracked temporary *copies* of the packaging and consumer scripts in the ephemeral checkout. No permanent production scripts or application source are committed, merged or released.

## Purpose and success criteria

Determine which failures of the existing NuGet packaging and independent consumer validation in EXP-007 are attributable to Windows PowerShell decoding, NuGet extraction configuration, or explicit Visual Studio compiler discovery—not to changed RecordSift behavior. A complete positive result requires the existing ten-project build, all five NUnit assemblies, 425-entry API check, XML check, unpublished package creation/validation, independent package installation, both standalone net48/C# 7.3 consumer compilations and executions, and absence of Visual Studio IDE or Build Tools.

## Existing controls and diagnostic design

1. **Notice comparison:** Reproduce the original package validator with unchanged script; compare the no-BOM UTF-8 notice with PowerShell 5.1 default decoding, explicit `Get-Content -Encoding UTF8`, .NET UTF-8, and the exact ZIP entry text; test a disposable script copy whose notice reader specifies UTF-8.
2. **NuGet XML extraction:** Use the original clean-consumer script under inherited `NUGET_XMLDOC_MODE=skip` (negative), then `none` (positive extraction control). Preserve the first encountered failure in each execution.
3. **Compiler discovery:** Run a disposable clean-consumer script copy, replacing only the Visual Studio `vswhere` / `Roslyn\csc.exe` lookup and invocation with `dotnet exec` of the SDK-provided `Roslyn\bincore\csc.dll` and explicit .NET Framework 4.8 reference assemblies. Compile and execute both `ReleaseConsumer/Program.cs` and `ReleaseConsumer/GettingStartedSamples.cs`, against freshly installed NuGet binaries rather than source-tree outputs.
4. **Evidence discipline:** Keep the unmodified baseline scripts as negative controls, separate environment/harness failures from application failures, preserve failed runs and unexecuted gates, and do not treat a green workflow alone as sufficient proof.

Microsoft documents that Windows PowerShell 5.1 uses its ANSI encoding for BOM-less files read by `Get-Content` by default ([PowerShell character encoding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding)). Microsoft also documents `NUGET_XMLDOC_MODE` values `skip`, `compress`, and `none` (regular file extraction) ([NuGet environment variables](https://learn.microsoft.com/en-us/nuget/reference/cli-reference/cli-ref-environment-variables)). These sources motivate, but do not substitute for, the runtime controls.

## Environment

Use GitHub Actions `windows-2022` with a Windows Server Core 2022 container based on `mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022`, historically captured as digest `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25`. Reconfirm the digest in each run. The container provides .NET SDK 10.0.403 and its MSBuild/Roslyn, Windows PowerShell 5.1 and the installed Windows .NET Framework runtime, but **not** Visual Studio Build Tools. Explicitly provision NuGet CLI 6.14.0.116 and `Microsoft.NETFramework.ReferenceAssemblies.net48` 1.0.3 before the traditional MSBuild restore/build. The targeting assemblies and runtime are distinct prerequisites.

Reproduction workflow:
[research-exp009-sdk-only-release.yml](https://github.com/infoconex/RecordSift/blob/research/sdk-only-release-followup-20261103/.github/workflows/research-exp009-sdk-only-release.yml).
The workflow records commands, environment, package output, test results, and per-gate logs in `TestResults/sdk-only-*` uploaded with `if: always()`.

## Evidence log

| Event | Run and workflow SHA | Actual observations | Interpretation |
|---|---|---|---|
| First workflow revision | [run 41707695201](https://github.com/infoconex/RecordSift/actions/runs/41707695201), `abfce77d277c0854d478152808a2591801afbc08` | Immutable image digest rechecked; no VS Build Tools; Release ten-project build, 419 tests (418 pass / 0 fail / 1 skip), XML and 425-entry API checks passed. Original package notice comparison and clean consumer still failed as EXP-007 predicted. In Windows PowerShell 5.1, default notice text **differed** from explicit UTF-8 decoding; explicit UTF-8 matched .NET UTF-8 decoding of all 2,655 source bytes. | Directly verifies the original PowerShell decoding mismatch; ZIP-entry comparison did **not** complete because the new probe omitted an explicit compression-assembly load. That error is a **new harness defect**, not a package defect. |
| Corrected compression-loading control | [run 41707884452](https://github.com/infoconex/RecordSift/actions/runs/41707884452), `290634e3d5ef12cc870af5ea4fa2761eba3c9032` | **Execution to be checked against finished job logs before claiming a result.** | Adds explicit `System.IO.Compression.FileSystem` load only to the temporary probe; should reach direct ZIP text control and corrected-script executions. |

**At this documentation checkpoint:** XML extraction under `none`, SDK-based consumer compilation and execution, and corrected package-validator success are **not yet verified by a completed run**. Do not treat the proposal as an achieved result.

## Decision boundary and risks

- No packaging or consumer script change is approved for permanent implementation.
- Explicit encoding is low risk for the known UTF-8 reviewed notices; avoid replacing content validation with a weaker check. A raw byte comparison is an alternative if the contract is byte identity.
- Restoring XML extraction may alter installed package filesystem content but not the package archive; scope the environment override to the consumer-verification process rather than broadly changing global machine settings.
- Direct SDK Roslyn invocation requires explicit framework references and an SDK path/version; it may be more brittle than a small, independently restored consumer project built with `dotnet msbuild`. Distinguish a demonstration from a recommended production method.
- The optional CS1591 **negative** documentation check currently uses Visual Studio MSBuild through `vswhere` and is **not** covered by the positive XML check; do not silently claim this gate has become independent.
- The business case for complete SDK-only release independence remains open; the existing Windows CI release validation already passes with Visual Studio available. The best near-term benefit may be documenting the smaller SDK-only *build/test* developer environment rather than redesigning release validation.

**Disposition:** research underway; historical EXP-007 conclusions remain intact. Final evidence classification and recommendation require inspection of corrected run steps/logs and artifacts.
