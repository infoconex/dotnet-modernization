# RecordSift — Technical baseline (in progress)

**Application repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Source branch observed:** `main`  
**Source revision frozen:** [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004)  
**Initial source inspection:** 2026-11-12 (GitHub repository tree/README)  
**Required discovery host:** Windows (application scope per README; actual operator OS/version/build not yet collected)  
**Local checkout and working tree:** **Not examined** — pending DISC-001 operator commands  
**Executed verification date:** **Not executed in this evaluation**  
**Current disposition:** Partial source inspection only; no evaluated or executed application verification claimed.

This is the actual **working** RecordSift technical baseline, not a copy of the reusable template's unobserved placeholder rows. As DISC steps complete, fill in applicable fields using the [full application baseline template](../../../../templates/application-baseline.md) and [variation guide](../../../../methodology/baseline-variation-guide.md). Record individual commands/results in the [execution log](execution-log.md) and refer to [evidence](evidence/manifest.md), not large pasted logs here. Do not import historical outcomes as new results.

## Application identity

The [application README at the frozen SHA](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) describes RecordSift as a Windows/.NET Framework 4.8 CSV/XLSX import and validation library. This is **a source documentation statement**, not independent verification of evaluated target frameworks, host runtime support, or build success.

| Field | Source-inspected observation | Evidence |
|---|---|---|
| Repository | `infoconex/RecordSift` | EV-001 |
| Frozen source commit | `1809d06c0fade59e4769d16e0f8eaf10fa426004` | EV-001 |
| Declared product scope | CSV/XLSX import, validation and diagnostics | EV-003 |
| Declared platform/framework | Windows / .NET Framework 4.8 per README | EV-003 |
| Solution path | `RecordSift.sln` | EV-002 |
| Local source changes | Not yet inspected | DISC-001 |
| Discovery host | Windows required; actual OS/version/build not yet verified | DISC-001 |
| Build configuration / MSBuild evaluation | Not yet inspected/evaluated | DISC-003/005 |

## Source project inventory

The immutable repository tree contains ten `.csproj` paths. Project names and `src`/`tests` directory roles below are **path-based inventory**, not a verified MSBuild project graph or evidence that all ten projects are built by the solution.

| Repository path | Source directory role |
|---|---|
| `src/RecordSift.Domain/RecordSift.Domain.csproj` | `src` |
| `src/RecordSift.Application/RecordSift.Application.csproj` | `src` |
| `src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj` | `src` |
| `src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj` | `src` |
| `src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj` | `src` |
| `tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj` | `tests` |
| `tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj` | `tests` |
| `tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj` | `tests` |
| `tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj` | `tests` |
| `tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj` | `tests` |

**Pending DISC-002/003:** solution membership, project formats, actual declared target frameworks, configurations/platforms, project references and relevant per-project differences.

## Repository configuration inventory — tracked paths only

**Observed:** root `.editorconfig`, `NuGet.Config` and seven `packages.config` files (two `src`, five `tests`), plus eight `.github/workflows/*.yml` files. All are tracked at the frozen revision [EV-002]. Their content, applicable precedence and execution status still require dedicated inspection.

**Not present in the inspected tracked tree at those exact names:** root `global.json`, root `Directory.Build.props`, root `Directory.Build.targets` and root `Directory.Packages.props`. This does **not** establish their applicability, evaluated absence, user/machine defaults, or whether creating them would help.

**Pending DISC-005/006/007:** conditional imports, shared files and nesting, tool-managed configuration, package declarations and source/restore behavior.

## Environment, build, test and delivery evidence

| Area | This evaluation's status | Next step |
|---|---|---|
| Operator OS, SDKs, runtimes, targeting packs, MSBuild, NuGet CLI | **Not inspected** | DISC-004 |
| Evaluated MSBuild settings and imports | **Not evaluated** | DISC-005 |
| Restore and resolved dependencies | **Not executed** | DISC-008 (operator review/approval first) |
| Build output | **Not executed** | DISC-009 (operator review/approval first) |
| Test discovery/execution and counts | **Not executed** | DISC-010 (operator review/approval first) |
| CI definitions | Tracked workflow files identified, **not examined** | DISC-011 |
| CI runs at this exact SHA | **Not verified** | DISC-011 |
| Packaging/runtime/compatibility gates | **Not inspected or executed** | DISC-011/012 |

A previous [pre-SDK modernization evaluation](../2026-11-pre-sdk/README.md) uses a different frozen revision and is historical background. Its command outputs and test counts do not verify this snapshot.

## Verification gaps and next action

**Gap:** the actual local checkout, host/toolchain, evaluated project settings and current execution evidence are unknown.

**Next:** perform DISC-001 manually; retain the original output, confirm whether the checkout matches the frozen SHA, then proceed one step at a time. Facts will be populated here after evidence is checked. Keep modernization assessment and suggestions in a separate evaluation record.
