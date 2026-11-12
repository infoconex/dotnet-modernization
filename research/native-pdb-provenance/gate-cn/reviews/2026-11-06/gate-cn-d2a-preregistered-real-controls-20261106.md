# Gate C-N — D2a preregistered real Windows classic-PDB compiler-output negative controls

**Recorded before any D2a CI execution** · **Date 2026-11-06 Pacific** · **Authority:** [conditional user approval; five-role model agreement](https://github.com/infoconex/dotnet-modernization/issues/80#issuecomment-6696966829). **Scope:** research only, one disposable non-RecordSift traditional net48 project, hosted Windows runner; no real RecordSift, no production gate, no NuGet install or Source Link production. **Independent human reviewers:** NOT appointed.

## Threat and provenance boundary

Trusted inputs: immutable repository checkout plus GitHub-hosted Windows runner, a private single-run capture, the user's specified D2a authorization, installed MSBuild/Csc and the checked-in dummy C# source. The runner itself witnesses that a clean directory preceded each /t:Rebuild and captures immediately afterward; this establishes runner-local experiment evidence, **not external cryptographic attestation of the actual compiler process, a signed manifest or tamper-resistant custody**. SHA256 hashes protect candidate byte identity *inside this trust boundary*; CodeView RSDS GUID+age ↔ PDB Info GUID+age is only PE/PDB internal pairing. MSBuild task logger must report exactly one Csc TaskStarted, one structured Source input set, and successful matching TaskFinished in a controlled one-node build. Only classic Windows PDB from locally generated source; arbitrary generators, PPDB, hostile PDB and full trust of unknown MSBuild tooling outside scope.

## Preregistered tests / expected failure mechanisms

**Positive P-A:** compile original immutable C# source (no external package) from clean bin/obj with /t:Rebuild on windows-2022, DebugType=pdbonly, .NET Framework 4.8 C# 7.3; uniquely observe matching full TaskContext Csc start/source/successful finish; attest SHA256 of emitted DLL/PDB and native PE/PDB RSDS pair; load copied **exact** DLL in isolated PowerShell CLR host and confirm actual Assembly.Location/loaded file SHA and invoke a method. **Positive P-B:** repeat same physical source content with alternate DefineConstants changing a compiled method body. Verify actual output bytes differ, each real pair internally valid. Private full hashes/paths/flags stay ephemeral.

| ID | One controlled mutation from approved positive and actual fixture | Exact expected fixed code | Required preconditions; otherwise INCONCLUSIVE |
| --- | --- | --- | --- |
| D2a-N01 | Retain genuine P-A paired DLL/PDB, withhold current unique Csc event witness | `MISSING_FRESH_CSC_OUTPUT_ATTESTATION` | Confirm real P-A pair previously passes and on-disk files unchanged |
| D2a-N02 | Select P-B valid compiler outputs but bind witness from P-A (different controlled compiler DefineConstants / option fingerprint) | `INVOCATION_OPTIONS_OR_OUTPUT_SHA_MISMATCH` | P-A and P-B genuinely compile **same tracked source bytes** with different flag and **different output DLL SHA256**; event identity is real |
| D2a-N03 | Preserve P-B event + sealed B hashes, overwrite candidate DLL/PDB with internally valid P-A pair | `OUTPUT_INVOCATION_SHA_MISMATCH` | Both real PDB pairs match their PE, and original P-B passes; pair swap alone causes failure |
| D2a-N04 | Run isolated CLR test host against a copy of real P-A DLL, while expecting sealed P-B candidate SHA | `CANDIDATE_TEST_DLL_NOT_ATTESTED` | Clean child CLR process loads exact passed path, invokes public method and obtains observed Assembly.Location/file hash (no simulated module identity) |
| D2a-N05 | Set independently observed prebuild output-dir freshness flag FALSE for otherwise matching P-B event/pair | `OUTPUT_ROOT_NOT_FRESH` | Real P-B passes with flag TRUE; this is a **freshness-assertion control**; absence of a fresh-root side channel is **not proof** that old bytes were emitted by Csc |

Each negative starts with a positive check; rejection must reach the named intended gate and match the expected code. Unrelated missing tools, compilation errors, Csc-event ambiguities, missing native symbols, failed CLR loads, or output pairs with identical DLL hash mean **INCONCLUSIVE**, not success. Logs/report must not print source path, source contents, private Csc arguments, original PDBs or binary digests. Include pass/fail per case, exact head commit, workflow/run/job ID, fixed status/limitations.

## Stopping criteria

If the real P-B output digest does not differ from P-A, **stop** N02/N03 and report INCONCLUSIVE; don't force false success. If any pairing or Csc capture fails, fail closed and report exact fixed-category diagnostic without path details. If the PowerShell CLR module witness cannot run, report N04 INCONCLUSIVE. No retry by silently switching the target/runtime, no running broad EXP-043/044 or modifying frozen RecordSift.

**Required cleanup:** private capture and any repo-local fixture bin/obj deleted via `if: always()`; upload only allowlisted category/count report if validated, no private or raw artifact retention. Capture exact execution SHA and workflow IDs from GitHub API independently of self-reported records. This preregistration is not evidence of execution.

**Release dispositions remain:** managed Gate C `UNSATISFIED`, native Gate C-N production `NOT_AUTHORIZED`, Source Link production `HOLD`. D2b/production and human reviewers/custody remain future separately authorized decisions.
