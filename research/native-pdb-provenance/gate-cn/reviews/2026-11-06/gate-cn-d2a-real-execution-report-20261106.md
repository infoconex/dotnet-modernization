# Gate C-N D2a — real Windows compiler, native PDB and net48 CLR negative-control report

**Date:** 2026-11-06 Pacific · **Disposition:** FIVE REAL-FIXTURE RESEARCH CONTROLS PASSED; NOT PRODUCTION ACCEPTANCE.  
**Conditional stakeholder authorization and five simulated engineering-role consensus:** [issue #80](https://github.com/infoconex/dotnet-modernization/issues/80#issuecomment-6696966829). This remains an author-context role synthesis; **no independent humans or outside AI team convened**.  
**Preregistration precedes live CI:** [D2a preregistered matrix, commit fdf43f1](https://github.com/infoconex/dotnet-modernization/blob/fdf43f12d083208d4260f7bdd89bc0ccd9be849e/methodology/acceptance-gates/reviews/2026-11-06/gate-cn-d2a-preregistered-real-controls-20261106.md).  
**Code/experiment review at executing SHA:** `c2f6e3bb50ac0e53b56845118092314c7f8d1434`. This research SHA is **not** the original frozen Gate C-N implementation review baseline `719275bb16feed7a8cd2eb7afeb7ae3cb7117991`, and neither research change modifies frozen RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8`.

## Primary actual Windows CI evidence

- **[Passing D2a run 42302838768](https://github.com/infoconex/dotnet-modernization/actions/runs/42302838768)**: GitHub API reported workflow conclusion SUCCESS at exact implementation SHA `c2f6e3bb50ac0e53b56845118092314c7f8d1434`; [Windows job 128184675128](https://github.com/infoconex/dotnet-modernization/actions/runs/42302838768) completed every step SUCCESS, including two actual builds, validation, cleanup and sanitized-only artifact upload.
- Independently downloaded authenticated job logs show fixed output `D2a REAL Windows native PDB 2 positive builds, 5 targeted negatives PASS`, followed by `D2a FIVE original-PDB/compiler/CLR research negatives verified with two real builds.`
- [Sanitized artifact on the run](https://github.com/infoconex/dotnet-modernization/actions/runs/42302838768): `gate-cn-d2a-real-negatives-sanitized`, GitHub artifact ID `13543954740`, retained for 30 days, only fixed identifiers/verdict/categories. No original source paths/bytes, raw symbols/assemblies, Csc diagnostic log or private hashes uploaded. The artifact metadata and successful upload step were independently confirmed; **its ZIP payload was not separately decoded during this review**, so do not claim independent byte-by-byte artifact validation.
- The runner used `windows-2022` with Visual Studio MSBuild/Roslyn; C# 7.3 traditional non-SDK `net48`, `DebugType=pdbonly`, `/t:Rebuild`, single-node `/m:1`; two variants of **the same unchanged tracked source bytes** differing in `DefineConstants`. It required fresh absent bin/obj roots before each compilation, retained private full TaskStarted/structured Sources/successful TaskFinished correlation under full Node/Project/Target/Task context, and verified real PE RSDS ↔ classic PDB Info GUID+age. Output DLL SHA256 for variant A differs from B. Original checked-in generated-source moniker count is **not separately authenticated by this D2a run**; that belongs to previous EXP-044 research scope.

## Observed controls (positive predecessor + exact rejection)

| Test | Real-fact precondition | Introduced mutation | Expected fixed category | CI result |
| --- | --- | --- | --- | --- |
| **D2a-N01** | Real A DLL/native PDB + real completed Csc witness accepted | Omit fresh Csc witness while retaining valid A pair | `MISSING_FRESH_CSC_OUTPUT_ATTESTATION` | PASS |
| **D2a-N02** | A and B are genuinely separately built, distinct option variants and DLL SHA256, same tracked source bytes | Pair B candidate with A observed Csc event + options | `INVOCATION_OPTIONS_OR_OUTPUT_SHA_MISMATCH` | PASS |
| **D2a-N03** | Valid real A and B PE↔PDB pairs and B source/event/sealed output accepted | Substitute complete older A DLL/PDB while keeping current B seal/event | `OUTPUT_INVOCATION_SHA_MISMATCH` | PASS |
| **D2a-N04** | Real B DLL copied and actually loaded by a fresh Windows PowerShell 5.1 **.NET Framework CLR** child; reflected method invoked, actual Assembly.Location + MVID observed | Copy and load real A DLL instead, expecting B candidate byte identity and behavior | `CANDIDATE_TEST_DLL_NOT_ATTESTED` | PASS |
| **D2a-N05** | Valid real B event/output positive; two real builds were fresh-root | Deliberately set independent root-freshness witness false while preserving valid paired B output | `OUTPUT_ROOT_NOT_FRESH` | PASS **assertion-only** |

Each named scenario verifies the unmutated real positive first. Python reads the two real DLL/PDBs from the trusted Windows runner; the PDB/PE reader parses actual MSF7 stream 1 and RSDS records. All five rejected with the exact category specified before execution. **N05 does not involve an actual old-output reuse or demonstrated incremental-build exploit**, only failure of a supplied false freshness assertion. N01 demonstrates missing-witness blocking on a genuine A pair, not a compiler process forgery.

For N04, the CLR child reported **actual** Assembly.Location, reflected method behavior and CLR module MVID. Attempting Get-FileHash inside the loaded CLR process failed (see red history); the successful experiment calculates SHA256 **in the parent after the CLR child exits** from the verified loaded location. This is useful trusted runner-local candidate-byte evidence but **not atomic cryptographic module identity against a hostile filesystem or TOCTOU threat**.

## Transparent prior failed attempts — not negative-test passes

| CI run / executing SHA | Conclusion | Bounded reason | Evidence status |
| --- | --- | --- | --- |
| [42302361493](https://github.com/infoconex/dotnet-modernization/actions/runs/42302361493) `95396d9...` | FAILURE | Original CLR load/check probe could not complete, fixed `REAL_CLR_LOAD_INCONCLUSIVE` | INCONCLUSIVE; cleanup succeeded |
| [42302561088](https://github.com/infoconex/dotnet-modernization/actions/runs/42302561088) `1b1282a...` | FAILURE | CLR probe still inconclusive | INCONCLUSIVE; cleanup succeeded |
| [42302593160](https://github.com/infoconex/dotnet-modernization/actions/runs/42302593160) `756347c...` | FAILURE | Sanitized stage `D2A_CLR_STAGE_SHA256_READ_FAILED`; in-child file re-open/hash issue | INCONCLUSIVE; cleanup succeeded |
| [42302813454](https://github.com/infoconex/dotnet-modernization/actions/runs/42302813454) `5fa0579...` | FAILURE | Child changed to MVID/location output, parent still expected prior in-child SHA contract | INCONCLUSIVE; no evidence used |
| **[42302838768](https://github.com/infoconex/dotnet-modernization/actions/runs/42302838768)** `c2f6e3b...` | **SUCCESS** | Parent follows actual loaded location and hashes it after child exit; five exact checks passed | **D2a research PASS** |

These attempts were legitimate troubleshooting *within the approved same five-control matrix*, not additional experiments or accepted negatives. Failing intermediate runs must not be omitted from traceability or mistaken for deliberate fail-closed controls.

## Actual assurance, unproven authority and stop

**Established at D2a scale:** on one trusted hosted Windows runner, two real traditional net48 compiler builds yield genuine native DLL/PDB pairs and distinct output bytes; the exact sealed candidate and Csc event/options are necessary for the research validator to accept; replacing real paired outputs or using a wrong candidate in a real .NET Framework CLR child is rejected by precise research-only checks.

**Not established:** independently signed/immutable prebuild manifest or source universe; externally tamper-resistant Csc invocation-output causality; runtime atomic module measurement; complete RecordSift suite graph and NuGet package/archive/feed/installation chain; hostile PDB or arbitrary generators/Portable PDB; production toolchain trust; final human approval, independent custodian/retention/revocation; true IDE debugger/source retrieval.

**D2a conclusion:** Targeted five real-fixture controls successfully executed under authorized scope. CV-01..03 **production** evidence gaps remain OPEN. D2b package/CLR extension and enterprise gate implementation need separate authorization, after #77 independent reviewer/governance decisions. No RecordSift/main edit, package publication, merge or Source Link production adoption. Both PR #81 and draft stacked PR #82 remain unmerged.

**Managed Gate C `UNSATISFIED`; native Gate C-N production `NOT_AUTHORIZED`; Source Link production `HOLD`.**
