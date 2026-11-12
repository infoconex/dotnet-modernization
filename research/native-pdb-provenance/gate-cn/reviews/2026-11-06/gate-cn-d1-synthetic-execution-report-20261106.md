# Gate C-N D1 — synthetic negative-control execution report

**Date:** 2026-11-06 Pacific · **Status:** D1 SYNTHETIC CONTRACT TESTS PASSED / P0 PRODUCTION EVIDENCE GAPS REMAIN OPEN.  
**Stakeholder authorization:** [Option A explicitly approved, issue #80](https://github.com/infoconex/dotnet-modernization/issues/80#issuecomment-6695492076).  
**Research implementation:** [draft stacked PR #81](https://github.com/infoconex/dotnet-modernization/pull/81) based on [draft PR #74](https://github.com/infoconex/dotnet-modernization/pull/74); neither merged.  
**Unmodified source review baseline:** research `719275bb16feed7a8cd2eb7afeb7ae3cb7117991`; RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8`.

## 1. Independently fetched actual CI evidence

| Evidence | Actual immutable event | Disposition |
| --- | --- | --- |
| [D1 initial green CI run 42293951337](https://github.com/infoconex/dotnet-modernization/actions/runs/42293951337) | SHA `4dfe0c4a415b2bdea2f3ab5a06b4c6a998926593`; 11 unittest cases executed, 11 passed; job `128154229917` | PASS on initial package archive hash-only contract |
| [D1 strengthened test-first run 42294206303](https://github.com/infoconex/dotnet-modernization/actions/runs/42294206303) | SHA `2979486f6f080bb0d1bc3ddf345093563c4c59bb`; import of newly specified `PackageSelection` intentionally failed before implementing contract | **EXPECTED TDD RED**, not successful evidence; no test cases were executed |
| **[D1 strengthened green CI run 42294228797](https://github.com/infoconex/dotnet-modernization/actions/runs/42294228797)** | **SHA `3864ee686900fdd95e4fe46aa89c2706a4a75bb6`**; job `128155189816`; actual unittest output `Ran 11 tests in 0.001s`, `OK` and individually named all 11 tests `ok` | **PASS — authoritative D1 synthetic test execution** |
| [Reusable tooling CI run 42293950877](https://github.com/infoconex/dotnet-modernization/actions/runs/42293950877) | Initial head `4dfe0c4a415b2bdea2f3ab5a06b4c6a998926593`; GitHub metadata SUCCESS | PASS; separate general tooling smoke validation |

The audit used authenticated connected GitHub run/job metadata and downloaded job logs. The test code and code review are stored in Git at the exact successful executing SHA:
- [Research-only contract module](https://github.com/infoconex/dotnet-modernization/blob/3864ee686900fdd95e4fe46aa89c2706a4a75bb6/tooling/validators/gate_cn_d1_synthetic.py)
- [TDD negative test cases](https://github.com/infoconex/dotnet-modernization/blob/3864ee686900fdd95e4fe46aa89c2706a4a75bb6/tooling/validators/tests/test_gate_cn_d1_synthetic.py)
- [Least-privilege synthetic-only workflow](https://github.com/infoconex/dotnet-modernization/blob/3864ee686900fdd95e4fe46aa89c2706a4a75bb6/.github/workflows/validate-gate-cn-d1-synthetic.yml)

**Interpretation:** The 11 unittest cases each begin by asserting acceptance of a valid companion fixture; then one or more controlled mutations must raise the **precise** `Rejected.category` named below. Actual green execution confirms these assertions were reached, not simply that a runtime exception occurred. Three test methods include several related negative subcases. Total: **11 paired positives and 17 explicit fixed-category rejection assertions in 11 unittest methods**. No real code signing or native PDB/PE/compiler invocation/actual package/CLR load is exercised.

## 2. Exact executed synthetic controls

| ID | Negative mutation in synthetic fixture | Expected asserted category | Observed CI method |
| --- | --- | --- | --- |
| M-N01 | Omit one approved component | `D1_COMPONENT_UNIVERSE_MISMATCH` | PASS |
| M-N02 | Add unapproved assembly/project | `D1_COMPONENT_UNIVERSE_MISMATCH` | PASS |
| M-N03 | Change approved manifest hash, expire/revoke authorization, self-approve | `D1_MANIFEST_APPROVAL_MISMATCH`, `D1_APPROVAL_EXPIRED_OR_REVOKED`, `D1_APPROVAL_NOT_INDEPENDENT` | PASS (four variants) |
| M-N04 | Preserve count but replace one compiler source identity | `D1_COMPILER_SOURCE_SET_MISMATCH` | PASS |
| M-N05 | Duplicate component under case-fold alias or substitute unsupported source origin | `D1_DUPLICATE_COMPONENT_IDENTITY`, `D1_COMPILER_SOURCE_SET_MISMATCH` | PASS (two variants) |
| B-N01 | Delete one mandatory test-suite copy-local assembly | `D1_MANDATORY_COPY_LOCAL_MISSING` | PASS |
| B-N02 | Substitute DLL with same assembly version and different SHA256 | `D1_CANDIDATE_COPY_LOCAL_HASH_MISMATCH` | PASS |
| B-N04 | Select same-version wrong package hash/feed, wrong package ID, or wrong feed with same archive SHA | `D1_PACKAGE_ARCHIVE_IDENTITY_MISMATCH` | PASS (three variants) |
| I-N01 | Remove Csc task event, leave internally paired output | `D1_CSC_EVENT_MISSING_OR_AMBIGUOUS` | PASS |
| I-N03 | Substitute internally paired DLL/PDB with different SHA256 and valid pair marker | `D1_COMPILER_OUTPUT_HASH_MISMATCH` | PASS |
| I-N05 | Prepopulate supposedly fresh output root with an otherwise valid pair | `D1_OUTPUT_ROOT_NOT_FRESH` | PASS |

These are **real executions of synthetic contract tests**, not actual build/packaging/CLR experiments. The intentionally failed first strengthened run is only a test-first implementation-history record; do not present it as an observed CV-03 stale-binary failure.

## 3. Architecture, constraints and privacy

- The D1 contracts are dependency-free Python value objects, typed fixed error categories and pure functions. Tests use independent in-memory approval and sealed-output **fakes**, not third-party APIs. Source/target inputs are synthetic, not from RecordSift.
- Production authority is **NOT PROVEN**: canonical SHA256 comparison against a test-supplied `Approval` record does not authenticate a human signature, immutable governance store, independent custodian or approved release policy. It demonstrates only the explicit decision rules.
- Compiler causation is **NOT PROVEN**: a synthetic `CompilerEvent` and independently supplied `CompiledOutput` seal do not demonstrate a real Csc task created those bytes. MSBuild node correlation, freshness timestamps and toolchain custody remain future D2/P1 work.
- Candidate load binding is **NOT PROVEN**: package IDs, feed, SHA and suite DLL identities are modeled as synthetic value objects; there is no NuGet selection, net48 consumer, CLR loading or actual native-PDB mutation.
- The new workflow has `contents: read` permission, pinned checkout, no raw evidence, no artifact upload, no package publish and no RecordSift checkout. Inputs are in-memory constants; CI logs contain only test names, Python version and fixed release HOLD text. The workflow exercises its own checkout only.

## 4. Decisions and remaining evidence gaps

**D1 synthetic objectives: completed / PASS for 11 scoped controls; P0 release readiness: remains BLOCKED.** The existing live validator and previously completed EXP-043/044 application evidence were neither changed nor rerun. This report **does not** add a new experiment claim to EXP-043/044 and must not reclassify the original source review findings as demonstrated real false passes.

**Next research authorization:** independently approve a **D2 scoped, disposable, non-RecordSift traditional net48 Windows classic-native-PDB fixture**, subject to a preregistered limited plan. Prioritize actual stale paired output (I-N01/I-N02/I-N03), one real candidate binary/mandatory suite load swap (B-N01/B-N02/B-N03), and isolated package feed/runtime selection proof (B-N04/B-N05) only where feasible. Enforce exact check-stage failures, positive/negative pairs, immutable CI SHA, privacy-safe evidence, and no production RecordSift changes. If D2 implementation requires production-oriented changes, stop for new explicit authorization.

**Human authority still missing:** [issue #77](https://github.com/infoconex/dotnet-modernization/issues/77) independent reviewer appointments, actual protected manifest owner, custodian/retention/revocation decision and explicit future release/legacy-Gate-C disposition. Synthetic personas do not count as human acceptance. Keep issue #80 P0 release checkboxes OPEN until those real controls exist.

**No merges. No production gate implementation or activation. Managed checksum Gate C UNSATISFIED; native Gate C-N release NOT_AUTHORIZED; Source Link production HOLD.**
