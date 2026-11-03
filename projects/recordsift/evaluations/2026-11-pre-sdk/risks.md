# Open questions and risks

**Baseline:** RecordSift main `8358780829458854a4b0356df5ac5e685f0a34c8`.

| ID | Gap or risk | Classification | Required follow-up |
|---|---|---|---|
| R-001 | The **unchanged** packaging/consumer scripts do not pass in SDK-only Windows: Windows PowerShell 5.1 notice decoding differs from ZIP UTF-8, `NUGET_XMLDOC_MODE=skip` prevents extracted XML, and the consumer script hardcodes VS `vswhere`/Roslyn. **EXP-009 verified the complete positive release path with temporary fixes**, including both independent consumers, but the optional CS1591 negative compiler check remains VS-dependent and not run without Build Tools. A raw `dotnet exec csc.dll` path is sensitive to SDK layouts. | Corrected positive path verified; original validation non-portable; CS1591 negative not executed | [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), [EXP-009](experiments/EXP-009-sdk-only-release-validation.md). Recommend only optional, separately approved scoped portability fixes if release-toolchain independence has value. |
| R-002 | Supported .NET Framework SDK image tag 4.8.1-windowsservercore-ltsc2022 had a resolvable manifest but was not pulled/executed in this investigation. | Not executed | Pull, record digest/tool inventory and rerun 419-test baseline. |
| R-003 | Formatter behavior with a repository-pinned global.json was not independently verified. | Not executed | Test dotnet format style under candidate SDKs, including CI provisioning. |
| R-004 | Early import of Microsoft.Common.props caused MSB3107 reference metadata errors. | Verified regression | Do not introduce this import; investigate root cause only if a requirement arises. |
| R-005 | Centralizing TargetFrameworkVersion would break assumptions in verify_public_api.ps1. | Known source coupling | Refactor checker to consume evaluated settings before changing framework property placement. |
| R-006 | PowerShell 7 produced reflection differences during API checks. | Verified environment sensitivity | Keep Windows PowerShell 5.1 until an invariant comparison is verified. |
| R-007 | Local run_tests.ps1 omits the XLSX test assembly; old documentation mentions 379 tests. | Known reliability defect | Correct both and rerun all five suites. |
| R-008 | Future PackageReference conversion may alter the dependency graph and hand-authored .nuspec declarations. | Future migration risk | Inventory direct/transitive dependencies and compare produced/consumed packages during SDK conversion. |
| R-009 | Actions artifacts are subject to retention; external image tags can be mutable. | Evidence reproducibility | Record image digests, full commands and durable conclusions; retain key logs or rerun. |

These are risks or follow-ups, **not a claim that RecordSift is currently broken**. Do not treat the build/test demonstration as certification of full release toolchain independence.
