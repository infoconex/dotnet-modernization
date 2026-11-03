# Experiment index

All RecordSift experiments use **application production baseline** `main` at `8358780829458854a4b0356df5ac5e685f0a34c8`. Temporary workflows were committed only to disposable `discovery/*` branches; in-workspace experimental changes were not committed to application main.

| ID | Experiment | Observed outcome | Run |
|---|---|---|---|
| [EXP-001](EXP-001-baseline.md) | Windows build, all tests, API/package/consumer baseline | Verified | [Main CI](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| [EXP-002](EXP-002-shared-properties.md) | Centralize LangVersion without import edits | Verified, full parity | [41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| [EXP-003](EXP-003-framework-sdk-container.md) | .NET Framework SDK Windows container build/test | Verified, VS Build Tools present | [41484891489](https://github.com/infoconex/RecordSift/actions/runs/41484891489) |
| [EXP-004](EXP-004-sdk-only-build.md) | Windows .NET SDK-only build/test with no VS Build Tools | Verified, all 419 tests | [41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| [EXP-005](EXP-005-sdk-selection-and-overrides.md) | global.json SDK selection and shared property override | Verified selection/precedence; formatter untested | [41486700576](https://github.com/infoconex/RecordSift/actions/runs/41486700576) |
| [EXP-006](EXP-006-msbuild-imports.md) | MSBuild import/targets checks and early Common.props | Working existing import path; early import regression | [41484290488](https://github.com/infoconex/RecordSift/actions/runs/41484290488) |
| [EXP-007](EXP-007-sdk-only-release-gates.md) | SDK-only XML/API/package/consumer gates | Complete, partially verified: XML/API, NuGet pack and install pass; full validation blocked by environment assumptions | [Corrected run](https://github.com/infoconex/RecordSift/actions/runs/41576608287) |

| [EXP-011](EXP-011-nuget-dependency-inventory.md) | Inspect full legacy NuGet package inventory, restored nuspec graph/assets and migration risks without application changes | **Verified:** 7 config files, 17 entries, 13 pinned IDs/restored packages, 11 production nuspec dependencies, 13 existing HintPath DLLs; future PackageReference graph not executed | [41728933974](https://github.com/infoconex/RecordSift/actions/runs/41728933974) |

See [evidence manifest](../evidence/manifest.md) for immutable container digests, artifact IDs and corrected/failed runs.

**Interpretation:** A workflow can pass while an intentionally unsuccessful negative control demonstrates a missing dependency. State the result of each command, not merely its enclosing workflow.
