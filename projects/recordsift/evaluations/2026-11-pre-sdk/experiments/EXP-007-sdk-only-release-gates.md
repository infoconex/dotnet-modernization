# EXP-007 — SDK-only Windows release compatibility gates

**Evaluation:** [RecordSift pre-SDK](../README.md)  
**Issue:** [dotnet-modernization #2](https://github.com/infoconex/dotnet-modernization/issues/2)  
**Date:** November 2, 2026  
**Application:** `infoconex/RecordSift`, canonical baseline `main` at `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Isolated experiment branch:** `discovery/sdk-only-release-gates-20261102`  
**Experiment workflow commit:** `7340c3409a755060cea33265cbcf129d4778832d`  
**Work state:** In progress (workflow launched)  
**Evidence outcome:** Not yet verified; do not claim gate results before inspecting the run.

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

## Execution evidence

- [GitHub Actions run 41575562993](https://github.com/infoconex/RecordSift/actions/runs/41575562993): launched; inspect job logs and artifacts before concluding.
- Separate logs expected: `sdk-only-gate-xml-positive.log`, `sdk-only-gate-api-425.log`, `sdk-only-gate-local-package.log`, `sdk-only-gate-clean-consumer.log`, plus `sdk-only-release-gates.json` (latter gates only when prerequisites succeed).

## Pending verification/disposition

The workflow was queued when this note was opened. After its completion record actual per-gate results, environment and image digest, failure diagnostics, artifact IDs and any gates not executed. A failing or blocked gate must **not** be reported as release compatibility success. A successful *build/test* does not guarantee consumer toolchain independence. No permanent application implementation is authorized.
