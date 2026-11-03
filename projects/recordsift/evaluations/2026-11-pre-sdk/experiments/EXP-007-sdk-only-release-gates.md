# EXP-007 — SDK-only Windows release compatibility gates

**Evaluation:** [RecordSift pre-SDK](../README.md)  
**Issue:** [dotnet-modernization #2](https://github.com/infoconex/dotnet-modernization/issues/2)  
**Date:** November 2, 2026  
**Application:** `infoconex/RecordSift`, canonical baseline `main` at `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Isolated experiment branch:** `discovery/sdk-only-release-gates-20261102`  
**Experiment workflow commits:** first `7340c3409a755060cea33265cbcf129d4778832d`; final corrected control `7df8be3374e292c6957ab22dcd9966dc30138b19`  
**Work state:** Complete (investigation documented; no application changes)  
**Evidence outcome:** **Partially verified:** complete restore/build/NUnit, positive XML, public API and package archive contents; current packaging/consumer verification scripts do not finish in the minimal environment. Causes isolated below.

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

[Run 41576091787](https://github.com/infoconex/RecordSift/actions/runs/41576091787), experiment workflow commit `5775fb98c7d30866ae24d0aaee721548bc71c591`, was launched to invoke each **unchanged** verification script from Windows PowerShell 5.1 after explicitly loading `System.IO.Compression.FileSystem` into the child process. This distinguishes implicit assembly-loading assumptions from subsequent Build Tools/compiler requirements. The run confirmed XML/API again but its package step was **inconclusive** because the temporary wrapper misquoted a parameter name; see the diagnosis below.

## Control-run diagnosis

[Run 41576091787](https://github.com/infoconex/RecordSift/actions/runs/41576091787), [artifact 13202929618](https://github.com/infoconex/RecordSift/actions/runs/41576091787/artifacts/13202929618), again verified the 419-test baseline, XML documentation and 425 API entries. The first package invocation failed on PowerShell parameter binding: the **experimental harness** quoted `-OutputDirectory` as a string, which was misinterpreted as a positional value for `PackageVersion`. This is a test-harness defect, **not** an application packaging failure. The clean consumer was not executed because no package was produced. Do not use this run to infer packaging or consumer portability.

A corrected isolated invocation (unquoted parameter name, quoted parameter value, with the compression assembly loaded in each fresh Windows PowerShell process) was committed as `7df8be3374e292c6957ab22dcd9966dc30138b19` and launched in [run 41576608287](https://github.com/infoconex/RecordSift/actions/runs/41576608287). Its first attempt was **blocked before Docker image pull** because the GitHub Windows runner could not connect to \\.\\pipe\\docker_engine; no build or gate was attempted. GitHub Actions [re-run attempt 2](https://github.com/infoconex/RecordSift/actions/runs/41576608287) executed the corrected experiment. Its per-gate results and retained artifact are documented below.

## Corrected control: actual packaging and consumer outcomes

**Execution:** [run 41576608287, attempt 2](https://github.com/infoconex/RecordSift/actions/runs/41576608287), workflow SHA `7df8be3374e292c6957ab22dcd9966dc30138b19`; diagnostic [artifact 13204365812](https://github.com/infoconex/RecordSift/actions/runs/41576608287/artifacts/13204365812). The Docker image digest, reverified in this run, was `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25`. Container had no Visual Studio IDE, Build Tools or standalone `MSBuild.exe`. Explicit compression-assembly preload was confined to the experimental invocation.

| Gate | True observation | Scope of conclusion |
|---|---|---|
| NuGet restore; ten-project Release build; five NUnit suites | **PASS**: 419 tests, 418 passed, 0 failed, 1 intentionally skipped | SDK-only build and .NET Framework execution reconfirmed. |
| Positive XML documentation validation | **PASS**, all five XML docs contain members (179/101/8/2/9) | The `-Negative` MSBuild compiler-enforcement control was **not run**. |
| Windows PowerShell 5.1 compiled public API/metadata baseline | **PASS**, all 425 entries | API parity within the recorded .NET Framework 4.8 environment. |
| Create an unpublished `0.1.0-rc.1` `.nupkg` via NuGet | **PACK SUCCEEDED**, archive produced | NuGet packed expected assemblies, XML, README, license and notices. |
| Existing packaging validation script | **FAIL** on `THIRD-PARTY-NOTICES.md` string comparison | The artifact's **packed notice bytes exactly equal staged source bytes** (2,655 bytes); the script compares a `StreamReader`-decoded UTF-8 entry with PowerShell 5.1 `Get-Content -Raw` text. The no-BOM UTF-8 notice includes an em dash; the failure is consistent with implicit ANSI-vs-UTF-8 decoding, **not** package byte corruption. The decoding explanation is derived from source and artifact inspection, not a separate direct encoding-control run. |
| Install unpublished package in independent NuGet consumer | **INSTALL SUCCEEDED** | The candidate and dependencies were retrieved and installed from the local feed + NuGet.org. |
| Existing clean-consumer verification script | **FAIL** before compilation: `Installed package missing RecordSift.Domain.xml` | The `.nupkg` **does contain** `lib/net48/RecordSift.Domain.xml` and all five XML files. Container inventory includes `NUGET_XMLDOC_MODE=skip`; this explains an environment-dependent extraction omission. The script's later `vswhere`/Visual Studio Roslyn requirement was **not reached** and remains an independently observed source dependency. |

**Artifact cross-check, reproducible without changing RecordSift:** Download artifact 13204365812. Extract nested `sdk-only-local-package/RecordSift.0.1.0-rc.1.nupkg` and compare its `THIRD-PARTY-NOTICES.md` raw bytes to `sdk-only-local-package/staging/THIRD-PARTY-NOTICES.md`: they match exactly. Inspect the `.nupkg` central directory to confirm `lib/net48/` contains five RecordSift DLLs and five XML documentation files. Compare the install-failure log `sdk-only-gate-clean-consumer.log` with the environment inventory and NuGet installation output. These checks confirm an existing validator/environment mismatch rather than a missing packaged file.

## Conclusion and recommendations (not implementation authorization)

**Verified:** SDK-only Windows without Visual Studio Build Tools supports full RecordSift build/NUnit, positive XML docs, compiled API verification, **NuGet package generation**, and independent **package installation** under the isolated experimental conditions.

**Not verified:** passing the entire *unchanged* packaging and consumer **validation scripts** or compiling/executing the independently installed consumer with no Build Tools. Explicit encoding in text comparisons, controlling `NUGET_XMLDOC_MODE`, and removing consumer-script `vswhere`/VS-Roslyn assumptions are candidate **future implementation work**, not changes authorized by this evaluation. The negative CS1591 documentation gate also retains a VS MSBuild dependency.

**Disposition:** The scoped investigation is complete with a **partially verified** outcome and concrete tooling blockers. Do not describe the overall failing GitHub Actions run as an application failure, or claim end-to-end SDK-only release equivalence. Preserve experimental branch and artifact locators as evidence; RecordSift `main` remains unchanged.
