# EXP-043 — Five-production-assembly native Windows PDB provenance

**State (November 5, 2026): VERIFIED five-production native source-byte provenance 64/64 and two-reader exposure limitation (46 of 64 documents, 0 of 46 checksums). Gate C UNSATISFIED; Source Link HOLD.** Issue [#70](https://github.com/infoconex/dotnet-modernization/issues/70), parent #37. Stacked on EXP-042 draft PR #69; no application or main branch changes.

## Evidence inherited without repeating completed investigations

EXP-041 established seven of seven CSV named-native PDB source checksums against captured original physical inputs. EXP-042 established actual Csc structured TaskInput/Sources identity agreement seven of seven and independent target-framework moniker generator execution/byte provenance, while preserving 425 public APIs, 419 NUnit (418 pass/one skip), five XML outputs, local unpublished NuGet and installed net48 consumer gates. Source Link adoption remains HOLD; approved managed-reader checksum Gate C is UNSATISFIED.

## Isolated work

1. Execute inherited frozen EXP-024 baseline and CSV candidate full acceptance with private original source snapshot, target producer, actual structured Csc logger. The EXP-024 candidate CSV PDB and original PDBs for the other four projects are inventoried read-only in `exp043-initial-native-inventory.json`, with counts and algorithms only (this is a *mixed-stage* inventory, not five original PDBs).
2. Independently compile **four other** traditional .NET Framework projects in disposable checkout, preserving their existing targets/references and original project files, importing the same three pinned official provider target/props modules and opt-in EXP-041/042 private instrumentation. Original files restored byte-identically after each compile. Source manifests, actual TaskInput parameters, preprocessed XML and compiler diagnostic records are isolated per component in the ephemeral runner directory. The CSV candidate is reused, not recompiled.
3. Replace any existing copy-local production DLL test-runner copies with their matching candidate assemblies. Run existing **full five-assembly** EXP-014 release/API/NUnit/XML/unpublished NuGet and clean installed net48 consumer contract gates, then compare five frozen release categories with the original baseline. Do not confuse package structure with genuine IDE project-package install.
4. Verify each paired candidate PE/PDB GUID+age, named native source records, DBI/C13 source identities, exact source-document hashes over independently captured original physical bytes, actual Csc structured TaskInput set, and real framework-moniker generator target execution/output bytes. Native record keys are never used as physical filesystem paths. `exp043-five-pdb-source-audit.json` is all five required or marked incomplete. Failure records include fixed error categories only, not private source names.
5. Automatically erase all private compiler, PDB-derived, generator, original source, log, preprocessed, logger DLL and shell evidence in workflow `if: always()`. Upload only aggregate sanitized JSON. Ubuntu controls test complete five-component universe, native inventory disagreement, missing input, incomplete source coverage, privacy and error classification.

## Research governance

No RecordSift or `main` branch changes; no unapproved source changes, merge, upgrades, package publishing, native vulnerable COM symbol reader, authentic Visual Studio Package Manager project-install or debugger stepping claim. Gate C UNSATISFIED; Source Link production HOLD, even if all native source bytes are independently verified. EXP-043 audits trusted locally generated PDBs only; it does not certify hostile PDB parsing safety or a policy replacement. Specific release checks and executing SHAs must be recorded after CI.

## Run record

**Completed at executing research SHA `d261572a4f02e94f83897eb94d056681d5cf6d55`: Windows and Ubuntu PASS; original and candidate contracts preserved, native 64/64 source inputs matched, two managed readers independently exposed 46 matching documents with 0/46 available checksums.** Details below.


## Final verified execution — November 5, 2026

**[CI run 42170182029](https://github.com/infoconex/dotnet-modernization/actions/runs/42170182029)**, actual executing code SHA `d261572a4f02e94f83897eb94d056681d5cf6d55`, both Windows and Ubuntu PASS; 10 new synthetic EXP-043 controls PASS. The repository-wide reusable tooling and all inherited EXP-041/042 infrastructure gates remained available. Frozen RecordSift SHA `8358780829458854a4b0356df5ac5e685f0a34c8` unchanged. Final native PDB and managed-reader results are independently derived from the retained, sanitized artifact.

| Production assembly | Named/DBI/C13 native source identities | Original physical bytes match | Actual Csc TaskInput Sources match | dnlib documents | Cecil documents | Managed checksums exposed |
|---|---:|---:|---:|---:|---:|---:|
| Domain | 24 | 24 | 24 | 20 | 20 | 0 |
| Application | 23 | 23 | 23 | 16 | 16 | 0 |
| Infrastructure.Csv | 7 | 7 | 7 | 4 | 4 | 0 |
| Infrastructure.Reporting | 7 | 7 | 7 | 5 | 5 | 0 |
| Infrastructure.Xlsx | 3 | 3 | 3 | 1 | 1 | 0 |
| **Total** | **64** | **64** | **64** | **46** | **46** | **0/46** |

All 64 source-document references are distinct **within their production assembly**. They are not asserted to represent 64 globally unique physical files across separate compilations. Source-input identities came from the actual structured MSBuild Csc TaskInput/Sources events, independently of the evaluated Compile items and privately snapshotted, unchanged pre/post-CoreCompile physical source bytes. Each paired PE and native PDB GUID+age matched, and all native named SHA256 source records, DBI and C13 source universes agreed. All input source hashes were compared to independently captured **physical compiler-time bytes**, not merely Git source or a PDB record. **Zero native input bytes missing**, zero observed native source family disagreements. The diagnostic-text-only Csc parameter extraction remains incomplete/ambiguous across these PDBs and is NOT accepted as the authoritative source set.

**Generated input provenance:** each assembly has one physical input under its intermediate object location. The separately probed real `GenerateTargetFrameworkMonikerAttribute` target executed its `WriteLinesToFile` task only after its allowed generated output had been removed in the disposable build. The exact emitted output bytes and path matched one of the actual Csc inputs for each assembly. The other **59** inputs were associated with tracked frozen application sources. These 59/5 categories are based on source path location plus independent producer execution; the location-only reused EXP-041 validator intentionally still labels the five intermediates `intermediate_location_producer_unverified` until the separate producer evidence is joined. The aggregate verifier records the join in `generated_source_producer=VERIFIED_TARGET_EXECUTION_AND_BYTES`.

**Two independently pinned managed readers:** the previously authenticated `dnlib 4.5.0` and `Mono.Cecil 0.11.6` managed Windows PDB readers were run as separate bounded processes with outbound Windows firewall rule, 20-second deadline, 256-MiB memory limit, and checks rejecting native DiaSymReader module loads. Both readers produced identical full document identity sets per assembly, exactly **46** documents total (20+16+4+5+1), all independently confirmed to be subsets of the 64 native source identities. Neither reader exposed checksum bytes for any of those **46** documents: **0/46**. The **18** native documents not exposed by either reader match the **18** documents without native C13 line references, providing an independently observed explanation for missing managed-reader source coverage; this is a bounded finding for frozen trusted PDBs, not proof of general framework behavior. Reader private names, full URLs, hash values, stdout and binaries were NOT published.

**C13 checksum distinction:** across five PDBs there are **72** C13 FILECHKSMS entries, every one `NONE` (no digest). There are **64** distinct C13 document identities, **46** identities with C13 line references, and **18** without. The independent native injected source streams carry supported SHA256 values, but only original-byte matching from the separate physical snapshots authenticates them. Neither native named checksums, C13 source references nor preprocessed project configuration alone establishes original-source integrity.

**Full frozen release/consumer acceptance:** original net48 and isolated CSV candidate via existing EXP-024; all four other candidates compiled without overwriting permanent application source/project files; candidate production DLL copies injected into actual test binary directories before execution. Verified all **425** public API entries, all **419** NUnit tests (418 pass, one expected skip, zero failures), five XML outputs, local **unpublished** NuGet package and installed clean net48 consumer, and all five logical compatibility categories matched original. All original tracked .csproj bytes were restored in finally, no tracked source changes, no dependency upgrade, no RecordSift commits or merges.

**Final sanitized metadata artifact:** `exp043-five-production-pdb-provenance-sanitized` GitHub Actions artifact ID **13479814833**, ZIP SHA256 **b0b23a78e8b0e1227631a25e9a3f975dbca4dbb8ae97f8b52d6aea463405a7fc**, 30-day retention. It contains exactly `exp043-initial-native-inventory.json` (mixed-phase CSV candidate plus four original PDBs), `exp043-five-pdb-source-audit.json` (all five candidates) and `exp043-managed-reader-exposure.json` (both actual pinned managed readers). Only aggregate counts and fixed labels are published. Workflow unconditionally removes the entire private evidence tree after the checks, including original compiler inputs, target producer evidence, native PDB logs, reader archives/DLLs/stdout/private URLs, PDB/private symbols and preprocessed projects. The candidate application checkout itself is ephemeral; no original application or main branch was pushed.

### Failure and negative-control history

- First isolated [run 42168811699](https://github.com/infoconex/dotnet-modernization/actions/runs/42168811699) successfully inventoried all five native PDBs but failed on an overly strict clean-working-tree check after the legitimate inherited build produced ignored artifacts. Corrected to enforce no tracked frozen source changes.
- [Run 42169134368](https://github.com/infoconex/dotnet-modernization/actions/runs/42169134368), executing SHA `e5353231747d1ed32260d4ef3593212913e2ac26`, first passed full **64/64** native and five-assembly release compatibility with both Ubuntu/Windows jobs. Retained sanitized artifact ID 13480785089, ZIP digest cf084bcf105a5c1f7f8727390a12f968522eb06bc94467934d516d6a9365debf.
- Initial managed-reader extension failed on a transcription mistake in the pinned dnlib archive digest, prior to any managed-reader execution. The pin was corrected to the **exact already verified EXP-036 archive SHA256**, never bypassed. Final run 42170182029 passed both managed readers. These were research-harness errors, not observed RecordSift regressions.
- Ten new EXP-043 offline controls and earlier EXP-041/042 controls cover incomplete five-assembly sets, source mismatches, missing/corrupted inputs, malformed reader identity, digest exposure/missing counts, wrong native universes and redaction. No completed EXP-039/040 fixture experiment was restarted merely to establish this result.

### Independent perspectives and remaining policy gap

**Build/reproducibility:** original source pinned; actual Csc task structured events and independent pre/post physical bytes all match, per-project isolated imports, exact paired PE/PDB native metadata. This is not proof of compiler-server internal virtual document behavior.

**Security:** only trusted locally produced PDBs, bounded native parser, full-path identity joins and fail-closed malformed input; authenticated pinned managed libraries and outbound-blocked bounded processes; original bytes, paths and logs remain ephemeral. This is NOT a hostile-PDB security certification.

**Architecture/reusability:** isolated source capture targets, structured Csc logger, native DBI/C13 and named source verifier, producer attestation, per-assembly reusable validator and two-reader exposure comparison. No new RecordSift production dependency or application architectural change.

**Quality/release:** compatibility gates include all five actual assemblies/test suites, copied candidate DLLs and local package/consumer checks, independent negative controls and sanitized retained evidence. No authentic Visual Studio Package Manager project-install or real debugger source stepping was executed.

**Governance:** Native PDB original physical input source provenance **VERIFIED 64/64** for frozen five-assembly candidate; two original managed reader implementations expose **0/46** checksums despite identical 46-document subsets; earlier approved managed checksum **Gate C UNSATISFIED**, Source Link production **HOLD**, not waived. This is evidence for a *future stakeholder decision* on a potential alternate gate, not implicit authorization to change the gate. Retain PR #71 **DRAFT/UNMERGED**; do not merge/publish or modify either main branch without explicit approval.
