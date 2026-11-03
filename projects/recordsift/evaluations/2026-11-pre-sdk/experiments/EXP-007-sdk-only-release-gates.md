# EXP-007 — SDK-only Windows release compatibility gates

**Evaluation:** [RecordSift pre-SDK](../README.md)  
**Issue:** [dotnet-modernization #2](https://github.com/infoconex/dotnet-modernization/issues/2)  
**Date:** November 2, 2026  
**Application:** `infoconex/RecordSift`, canonical baseline `main` at `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Isolated experiment branch:** `discovery/sdk-only-release-gates-20261102`  
**Experiment workflow commit:** `7340c3409a755060cea33265cbcf129d4778832d`  
**Work state:** In progress (second controlled diagnostic launched)  
**Evidence outcome:** Partially verified: XML/API gates passed; package and consumer failed in first run. Second isolation control pending.

## Objective and hypothesis

Determine whether RecordSift's **existing** XML documentation, public API, package creation and clean consumer compatibility gates operate in a Windows .NET SDK-only container without Visual Studio IDE or Build Tools. The earlier [EXP-004](EXP-004-sdk-only-build.md) already verified ten-project compilation and five NUnit suites; it did **not** run these release gates.

## Environment and experiment

The isolated workflow [pre-sdk-sdk-only-release-gates.yml](https://github.com/infoconex/RecordSift/blob/7340c3409a755060cea33265cbcf129d4778832d/.github/workflows/pre-sdk-sdk-only-release-gates.yml) reuses the SDK-only image `mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022` and explicit NuGet CLI 6.14.0.116 + `Microsoft.NETFramework.ReferenceAssemblies.net48` 1.0.3 provisioning from EXP-004. Compare the **image digest captured by this run** to the previously verified `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25`, rather than assume a tag stayed immutable.

The workflow builds the unchanged traditional solution and checks NUnit baseline (419 total/0 failed/1 skipped) before invoking the original verification scripts through Windows PowerShell 5.1. Each gate gets a separate diagnostic log and outcome, and the run uploads `TestResults/sdk-only-*` artifacts even if a gate fails. No production application files are edited or committed.

## Source inspection before execution

- `scripts/verify_xml_documentation.ps1` checks five XML documentation outputs in its **positive mode**, without needing Visual Studio. Its optional **negative mode** invokes Visual Studio `MSBuild.exe`.
- `scripts/verify_public_api.ps1` uses reflection to compare compiled APIs and project metadata against `docs/compatibility/public-api-net48.txt`. Earlier runs demonstrated Windows PowerShell 5.1 / PowerShell 7 behavioral differences; this workflow uses 5.1.
- `scripts/build_release_candidate.ps1` invokes NuGet pack and requires `git` to stamp the exact source commit; Git availability in SDK-only container must be checked.
- `scripts/verify_clean_consumer.ps1` explicitly finds Visual Studio MSBuild and its `Roslyn/csc.exe` through `vswhere` to build an installed .NET Framework consumer. An unchanged consumer gate may be blocked by this tool assumption even if the SDK-only solution builds. This is **source-inspection evidence**, not a runtime result.

## Actual results — first run (negative control)

[Run 41575562993](https://github.com/infoconex/RecordSift/actions/runs/41575562993), experimental commit `7340c3409a755060cea33265cbcf129d4778832d`, failed **as a workflow**, correctly reporting incomplete release verification. Logs retained in [artifact 13203417992](https://github.com/infoconex/RecordSift/actions/runs/41575562993/artifacts/13203417992).

| Gate | Observed result | Reproducible interpretation |
|---|---|---|
| SDK-only .NET Framework reference pack negative control | MSB3644 as expected without references | Targeting pack absent, not an application regression |
| Restore / ten-project Release build | Passed | Build Tools absent; `dotnet msbuild` available |
| NUnit five test assemblies | **419 discovered, 418 passed, 0 failed, 1 skipped** | Reconfirmed unchanged functional baseline |
| XML documentation (positive mode) | **Passed** | Five nonempty XML files: 179/101/8/2/9 entries |
| Public API/metadata check | **Passed** | Windows PowerShell 5.1 verified all **425** baseline entries |
| Local package creation/validation | **Failed** | Windows PowerShell could not resolve `[IO.Compression.ZipFile]` during validation |
| Clean installed-package consumer | **Failed** | Windows PowerShell could not resolve `[System.IO.Compression.ZipFile]` before reaching compiler/tool discovery |

The container inventory confirmed NuGet CLI **present** after installation, Git CLI **present**, and Visual Studio IDE, Build Tools and standalone `MSBuild.exe` **absent**. These are direct run observations, not assumptions from source. **Do not yet attribute consumer failure to VS tooling**: the first encountered obstacle was the compression assembly.

## Follow-up control — no application code changes

[Run 41576091787](https://github.com/infoconex/RecordSift/actions/runs/41576091787), experiment workflow commit `5775fb98c7d30866ae24d0aaee721548bc71c591`, was launched to invoke each **unchanged** verification script from Windows PowerShell 5.1 after explicitly loading `System.IO.Compression.FileSystem` into the child process. This distinguishes implicit assembly-loading assumptions from subsequent Build Tools/compiler requirements. The result was pending at the time of this update.

## Control-run diagnosis

[Run 41576091787](https://github.com/infoconex/RecordSift/actions/runs/41576091787), [artifact 13202929618](https://github.com/infoconex/RecordSift/actions/runs/41576091787/artifacts/13202929618), again verified the 419-test baseline, XML documentation and 425 API entries. The first package invocation failed on PowerShell parameter binding: the **experimental harness** quoted `-OutputDirectory` as a string, which was misinterpreted as a positional value for `PackageVersion`. This is a test-harness defect, **not** an application packaging failure. The clean consumer was not executed because no package was produced. Do not use this run to infer packaging or consumer portability.

A corrected isolated invocation (unquoted parameter name, quoted parameter value, with the compression assembly loaded in each fresh Windows PowerShell process) was committed as `7df8be3374e292c6957ab22dcd9966dc30138b19` and launched in [run 41576608287](https://github.com/infoconex/RecordSift/actions/runs/41576608287). Its release-gate outcomes are pending evidence review.

## Limitations and next evidence

The first run verifies SDK-only XML/API compatibility and documents missing implicit assembly loading in two validation scripts. It does **not** establish full release/consumer toolchain independence. Inspect the second run's per-gate logs, source and image digest, artifact and failure chain before closing the investigation. The published application scripts are unchanged. No application implementation is authorized.
