# RecordSift technical discovery — Evidence manifest

**Evaluation:** [November 2026 native-first technical baseline](../README.md)  
**Frozen source commit:** `1809d06c0fade59e4769d16e0f8eaf10fa426004`  
**Status:** Source-inspected application facts and existing GitHub Actions evidence are available for the selected commit. **No operator-run Windows discovery commands have been captured** in this evaluation. GitHub CI results and the operator's local machine are different environments.

| Evidence ID | Discovery context | Source / trace | Method and provenance | What it establishes / limitations |
|---|---|---|---|---|
| EV-001 | Baseline item 33 (selected revision) | [Immutable application commit](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) | Source metadata inspected via connected GitHub | Identifies the repository revision selected for this walkthrough. **Does not** establish operator local HEAD, working-tree state, or toolchain. |
| EV-002 | Baseline items 36–37, 42–44, 50 (source inventory) | [Tracked tree at frozen SHA](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004) | GitHub tree source-inspected | Records observed solution, project, repository configuration and workflow *paths*. Does not prove effective imports, solution membership, or commands executed. |
| EV-003 | Application description and baseline items 1–4 | [README at frozen SHA](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) | Source-inspected product documentation | Documents the application's own Windows/.NET Framework 4.8 description; not independently verified project evaluation or runtime execution. |
| EV-004 | Baseline fields 3 and 6–7 | [GitHub source repository](https://github.com/infoconex/RecordSift) and [LICENSE](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/LICENSE) | Repository metadata and tracked license file | License and default branch. SSH address is the repository clone URL, not an authenticated SSH connection test. |
| EV-005 | Baseline fields 8–11 | [README at selected SHA](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) · [GitHub v0.1.0 release](https://github.com/infoconex/RecordSift/releases/tag/v0.1.0) · [NuGet 0.1.0](https://www.nuget.org/packages/RecordSift/0.1.0) | Published release/package references | Published version and exact release/package URLs are distinct from the tracked prerelease nuspec version. |
| EV-006 | Baseline field 12 | [Tracked package manifest](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/packaging/RecordSift.nuspec) | Source declaration | `version=0.1.0-rc.1` is the version in source, not the published package. |
| EV-007 | Baseline fields 13–14 | [Production AssemblyInfo](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/src/RecordSift.Domain/Properties/AssemblyInfo.cs) | Source declaration | AssemblyVersion and AssemblyFileVersion are both `0.1.0.0`; this does not by itself verify a compiled DLL's metadata. |
| EV-008 | CI build and tests at selected SHA | [Windows build/test run](https://github.com/infoconex/RecordSift/actions/runs/43146607664) | Existing GitHub Actions run, succeeded at `1809d06c…`; job steps and logs inspected | Windows restore, Release build, API/XML/style checks and NUnit suites succeeded. NUnit results: 419 discovered, 418 passed, 0 failed, 1 skipped. This is **not** an operator-run local verification. |
| EV-009 | CI consumer verification at selected SHA | [Windows package/consumer run](https://github.com/infoconex/RecordSift/actions/runs/43146607706) | Existing GitHub Actions run, succeeded at `1809d06c…`; job steps and logs inspected | Unpublished package/clean consumer validation passed; not evidence of a fresh local consumer run. |
| EV-010 | CI docs verification at selected SHA | [Documentation validation run](https://github.com/infoconex/RecordSift/actions/runs/43146607615) | Existing GitHub Actions run, succeeded at `1809d06c…`; steps inspected | Documentation/engineering checks passed on Ubuntu; **does not** imply application cross-platform support. |

## Rules for new evidence

- Record **Discovery Date** once in the completed baseline; separate collection dates are not required for individual evidence records. Keep any dates that are inherent to an external record (such as a CI run date) as part of that source's factual information.
- Link each new artifact/output to its numbered baseline item and the complete source SHA. For executed operations, capture command, tool version, host/environment, **exit code**, output/result and retained artifact location.
- Keep **actual raw output** or a durable faithful excerpt separately from any generated report. Give exact GitHub Actions run/artifact IDs and note expiry; commit small redacted text where useful.
- Use source-inspected, tool-evaluated, existing CI-executed, and operator-executed classifications separately; preserve historical provenance. An earlier evaluation run is not new evidence for this SHA unless its exact scope is verified.
- Do not commit credentials, secret-bearing configuration, generated packages, restored dependencies or large binaries. Report missing/blocked/unexecuted checks explicitly.
- Add links to actual artifacts only when they exist. No placeholder file trees or invented screenshots/logs.

## Baseline value provenance

- Keep values in the baseline's **Value** column atomic (for example, `Library`, `Public`, `MIT`, `Windows`, a version, SHA, or exact URL). Do not append citation titles, provenance prose, or execution caveats to those values.
- Source links and qualifications belong in this manifest. Fields **1–7** are supported by EV-003/EV-004; **8–11** by EV-005; **12** by EV-006; **13–14** by EV-007. Local machine fields **18–30** remain unverified until the operator supplies tool output.
