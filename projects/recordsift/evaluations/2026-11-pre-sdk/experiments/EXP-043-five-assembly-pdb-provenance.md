# EXP-043 — Five-production-assembly native Windows PDB provenance

**State: UNVERIFIED RESEARCH IMPLEMENTATION — no full-five provenance claims until specific Windows and Ubuntu CI passes.** Issue [#70](https://github.com/infoconex/dotnet-modernization/issues/70), parent #37. Stacked on EXP-042 draft PR #69; no application or main branch changes.

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

Pending first isolated execution. Count every PDB separately; if any assembly is BLOCKED or source evidence unavailable, report **PARTIAL / INCOMPLETE**, not 5/5 VERIFIED.
