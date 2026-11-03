# Verified and partially verified findings

**Evidence baseline:** RecordSift main `8358780829458854a4b0356df5ac5e685f0a34c8`. A finding records observations, not approval to implement.

| ID | Finding | Evidence status | Source |
|---|---|---|---|
| F-001 | The Windows CI baseline discovers 419 NUnit tests; 418 pass, none fail, one is explicitly skipped. | Verified | [Baseline](baseline.md) |
| F-002 | The local test runner omits XLSX tests even though CI runs all five test assemblies. | Verified source inspection | [Baseline](baseline.md) |
| F-003 | Traditional projects automatically consume a root Directory.Build.props in RecordSift's *current* import chain. | Verified | [Shared-property experiment](experiments/EXP-002-shared-properties.md) |
| F-004 | Moving common LangVersion=7.3 to shared props without import edits preserves the tested build, API, XML and NUnit behavior. | Verified | [Shared-property experiment](experiments/EXP-002-shared-properties.md) |
| F-005 | An unconditional late shared value overwrites an earlier project LangVersion; a conditional shared default permits the project override. | Verified | [Override experiment](experiments/EXP-005-sdk-selection-and-overrides.md) |
| F-006 | Directory.Build.targets can execute under traditional projects, but there is no demonstrated need for an additional shared target. | Verified mechanism; policy recommendation | [MSBuild imports](experiments/EXP-006-msbuild-imports.md) |
| F-007 | Inserting an early Microsoft.Common.props import in this traditional solution caused MSB3107 project-reference errors. | Verified failed experiment | [MSBuild imports](experiments/EXP-006-msbuild-imports.md) |
| F-008 | A .NET Framework SDK Windows container restores, builds all ten projects and runs all five test suites; it contains Visual Studio Build Tools. | Verified | [Container feasibility](experiments/EXP-003-framework-sdk-container.md) |
| F-009 | A Windows .NET SDK-only image **without VS IDE or Build Tools** can compile all ten unchanged traditional projects and run all 419 NUnit tests after explicit net48 references and NuGet CLI are provided. | Verified | [SDK-only experiment](experiments/EXP-004-sdk-only-build.md) |
| F-010 | Without the targeting pack, SDK-only compilation fails MSB3644; adding it resolves the demonstrated missing-reference blocker. | Verified negative/positive controls | [SDK-only experiment](experiments/EXP-004-sdk-only-build.md) |
| F-011 | global.json selects fixed SDK and feature-band roll-forward as expected; missing fixed SDK prevents SDK command execution. | Verified selection only | [SDK selection](experiments/EXP-005-sdk-selection-and-overrides.md) |
| F-012 | The raw-XML public API checker creates coupling to the location of TargetFrameworkVersion in project files. | Verified source inspection | [Baseline](baseline.md) |
| F-013 | Windows PowerShell 7 changes the reflection-based API comparison result; the corrected Windows PowerShell 5.1 run passes. | Verified execution difference | [Evidence](evidence/manifest.md) |
| F-014 | The SDK-only container's compilation and NUnit success does **not** prove all API, XML, packaging and clean-consumer scripts run without Build Tools. | Explicit scope limit | [Risks](risks.md) |
| F-015 | In a clean SDK-only Windows container, the five XML documentation files and all 425 compiled API/metadata entries passed their existing checks using Windows PowerShell 5.1. | Verified execution | [EXP-007 first run](experiments/EXP-007-sdk-only-release-gates.md) |
| F-016 | Existing local-packaging and consumer scripts fail in the minimal PowerShell environment when `ZipFile` is not resolved; second isolated run tests explicit `System.IO.Compression.FileSystem` preload to isolate the blocker. | Verified initial failure; root-cause control pending | [EXP-007](experiments/EXP-007-sdk-only-release-gates.md) |

## Application-specific interpretation

The highest immediate-value work is **safety and maintenance**: correct the all-suite local test command and reduce genuinely identical compiler configuration. Tool independence can also be obtained without SDK conversion, but should be treated as a separate, optional workstream until end-to-end release validation is complete.

For generalizable lessons, create dedicated notes under [research](../../../../research/README.md) only when they apply beyond RecordSift and can cite primary-source documentation.
