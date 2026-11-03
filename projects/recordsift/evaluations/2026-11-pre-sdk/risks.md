# Open questions and risks

**Baseline:** RecordSift main `8358780829458854a4b0356df5ac5e685f0a34c8`.

| ID | Gap or risk | Classification | Required follow-up |
|---|---|---|---|
| R-001 | In SDK-only Windows, build/tests/XML/API and NuGet pack/install pass, but the unchanged packaging validator rejects a notice text comparison and the consumer validator cannot find XML docs omitted from extraction under `NUGET_XMLDOC_MODE=skip`. Full consumer execution and negative XML enforcement remain unverified. | Partially verified; investigation complete | [EXP-007](experiments/EXP-007-sdk-only-release-gates.md). Consider explicit UTF-8 handling, NuGet XML extraction configuration and consumer compiler-tool independence only under separate implementation approval. |
| R-002 | Supported .NET Framework SDK image tag 4.8.1-windowsservercore-ltsc2022 had a resolvable manifest but was not pulled/executed in this investigation. | Not executed | Pull, record digest/tool inventory and rerun 419-test baseline. |
| R-003 | Original risk — formatter with an exact SDK pin — **resolved for tested versions 10.0.303 and 10.0.403**. The remaining risk is operational: an uninstalled strict pin blocks `dotnet` commands; changing the pin needs coordinated developer/CI provisioning and maintenance. | **Compatibility verified; optional adoption tradeoff untested** | [EXP-008](experiments/EXP-008-pinned-sdk-formatter-build.md) proves actual existing IDE1006 formatter, Release build/NUnit/XML/API. [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md) already proves absent-SDK negative control. Only recommend adoption if an explicit reproducibility goal and SDK provision/update policy are agreed. |
| R-004 | Early import of Microsoft.Common.props caused MSB3107 reference metadata errors. | Verified regression | Do not introduce this import; investigate root cause only if a requirement arises. |
| R-005 | Centralizing TargetFrameworkVersion would break assumptions in verify_public_api.ps1. | Known source coupling | Refactor checker to consume evaluated settings before changing framework property placement. |
| R-006 | PowerShell 7 produced reflection differences during API checks. | Verified environment sensitivity | Keep Windows PowerShell 5.1 until an invariant comparison is verified. |
| R-007 | Local run_tests.ps1 omits the XLSX test assembly; old documentation mentions 379 tests. | Known reliability defect | Correct both and rerun all five suites. |
| R-008 | Future PackageReference conversion may alter the dependency graph and hand-authored .nuspec declarations. | Future migration risk | Inventory direct/transitive dependencies and compare produced/consumed packages during SDK conversion. |
| R-009 | Actions artifacts are subject to retention; external image tags can be mutable. | Evidence reproducibility | Record image digests, full commands and durable conclusions; retain key logs or rerun. |

These are risks or follow-ups, **not a claim that RecordSift is currently broken**. Do not treat the build/test demonstration as certification of full release toolchain independence.
