# EXP-039 — Reusable native Windows PDB source checksum verifier and document-inventory boundaries

**Status (November 5, 2026): CONTROLLED VALIDATOR VERIFIED; ACTUAL FROZEN CSV 4/4 MANAGED-DISCOVERED SOURCES VERIFIED; THREE UNMATCHED NATIVE SOURCE STREAMS UNRESOLVED; GATE C UNSATISFIED.**

**Research issue:** [#62](https://github.com/infoconex/dotnet-modernization/issues/62); predecessor [EXP-038](EXP-038-document-to-native-stream-key.md) ([#60](https://github.com/infoconex/dotnet-modernization/issues/60)); parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37). Experimental RecordSift commit is frozen at `8358780829458854a4b0356df5ac5e685f0a34c8`. Draft research only; do not merge, modify the application, upgrade its dependencies, change the PDB format, waive Gate C or publish a package.

## Proven EXP-038 starting point

Original and manual Source Link candidate release/consumer compatibility gates pass (425 API, 419 NUnit / 418 pass / 1 skip, five XML docs, locally built 0.1.0 NuGet package, installed clean net48 consumer and five logical compatibility categories). Both official pinned dnlib 4.5.0 and Cecil 0.11.6 managed parsers enumerate the four selected CSV documents but expose zero hashes after `/pathmap`. The real PDB nonetheless contains one structurally decoded checksum record with SHA256 of the physical compiler-input file for each of the four. The exact reader document URL-derived source key does **not** equal the native source stream key case-insensitively; separator normalization + casefold resolves the key in both controlled mapped fixtures and actual four CSV documents. [Evidence run 42148192785](https://github.com/infoconex/dotnet-modernization/actions/runs/42148192785) and successful final [PR head run 42148785734](https://github.com/infoconex/dotnet-modernization/actions/runs/42148785734).

## Research question

Can a reusable, standalone, bounded, standard-library Windows PDB validator independently check the SHA1/SHA256 **structured native** source checksum against physical compiler-input source bytes for *every document discovered by both independent readers* (not just a manually selected four), use exact normalized full paths rather than basename-only matching, and explicitly classify named native source streams that cannot be linked to those documents?

**A positive selected-source result is not by itself proof of the complete native document inventory**: dnlib/Cecil might share discovery gaps, named source streams might be unrelated to document records, and generated/external compiler inputs may not be available. Any such uncertainty must remain visible.

## Reusable verifier design

`tooling/validators/classic_pdb_document_checksums.py` is standard library only. It imports the existing bounded `native_windows_pdb_sourcelink.py` MSF7 and PE/CodeView identity parsers. It takes the exact matched DLL/PDB, two private reader-inventory files with full document URLs, and explicitly declared physical compiler-input files.

- Reader URLs are obtained from isolated, verified, managed-only dnlib/Cecil readers under outbound firewall, 20-second timeout and monitored 256 MiB process memory limit. Full paths/URLs exist only in temporary local private manifests, deleted in `finally` even on diagnostic failure. No source URL or native stream key is included in logs or artifacts.
- The checker compares **the complete normalized `/src/files/` + document URL** to named native streams; slash/backslash and case normalize, but directory components **must not** be dropped. It verifies both readers describe the same normalized document set, rejects duplicate/colliding document identities, and requires every enumerated document to resolve to a supported injected-source record. It **never** guesses physical inputs from untrusted PDB paths.
- Each verified record is independently parsed as four GUIDs, two bounded signed lengths, supported SHA1/SHA256 algorithm and exact checksum bytes; physical source bytes from an explicit trusted path are hashed and compared. A missing/incorrect checksum for a supplied file is a hard failure.
- Native source named-stream entries not linked to a managed reader URL are **counted, not silently counted as verified or assumed relevant**. A source URL without an explicitly supplied physical input is separately counted as unresolved. Require all named sources before using an all-inventory claim.
- Synthetic negative/positive controls are stored under `tooling/validators/tests/test_classic_pdb_document_checksums.py` and executed without third-party libraries on Ubuntu. Full original frozen application compatibility and existing all-fixture checksum tests rerun on Windows using the dedicated `validate-exp039-reusable-pdb-checksums.yml` workflow.

## Explicit limitations and decision table

| Area | Proposed EXP-039 test | Acceptance boundary |
|---|---|---|
| Known physical compiler inputs | Full SHA1/SHA256 structured PDB record matches exact bytes | Passes *selected-input native checksum evidence*, not existing managed reader Gate C |
| Full managed document inventory (reader view) | Both independent readers enumerate equal normalized complete URL sets, with no unsupported named lookup | Does not prove completeness of independent C13 document inventory |
| Extra native named source streams | Count, parse-classify and mark unmatched | Must not silently waive or assert they are required managed documents |
| Generated/external source | Requires explicitly trusted physical file; unresolved if absent | Prevents all-document proof |
| Legacy key mapping | Full path separator/case normalized, no basename shortcut | Caller must validate this policy for alternate platforms and PDB versions |
| Security | Only trusted frozen/locally compiled bounded PDBs | No hostile-input parser safety or OS-wide sandbox claim |
| Scope | Frozen CSV and direct csc fixtures | No all-assembly/other-application guarantee |
| Adoption | No production change or Gate C replacement | **HOLD** until stakeholder chooses policy and tests missing IDE/debugger gates |

## Verified execution and evidence

**[Successful Windows + Ubuntu workflow 42152491141](https://github.com/infoconex/dotnet-modernization/actions/runs/42152491141)**, executing verifier fix at research SHA `6597250630998c01da43c5c6527cda478cb9008a`: **both jobs PASS**. The Ubuntu stdlib-only regression suite passed **21/21** synthetic tests; Windows completed the frozen original + manual candidate EXP-024 release gates, pinned official reader preflight, all original EXP-036 SHA1/SHA256 source mutation/wrong PDB controls, EXP-037 five compiler variants and EXP-038 exact URL/key association; then independently validated each physical input through the new reusable verifier. [Metadata-only artifact 13473675850](https://github.com/infoconex/dotnet-modernization/actions/runs/42152491141/artifacts/13473675850), GitHub-reported ZIP digest `sha256:7fb63772a6e968263d806440006ea9b06e7d490f15c59cd3b042a13552b68aa6`, 30-day retention. **No source files, private URL manifests, raw PDBs/DLLs, package archives, full hashes, or diagnostic command lines** uploaded.

| Input under test | Reusable verifier's valid managed-document-associated native SHA256 | Unmatched native `/SRC/FILES/` streams | Inventory classification |
|---|---:|---:|---|
| Direct Roslyn explicit-SHA256 fixture | 1 / 1 | 0 | Reconciled named streams and managed-discovered document |
| Direct Roslyn implicit-checksum fixture | 1 / 1 | 0 | Reconciled named streams and managed-discovered document |
| Direct Roslyn deterministic-only fixture | 1 / 1 | 0 | Reconciled named streams and managed-discovered document |
| Direct Roslyn deterministic + `/pathmap` fixture | 1 / 1 | 0 | Reconciled named streams and managed-discovered document |
| Direct Roslyn deterministic + `/pathmap` + Source Link fixture | 1 / 1 | 0 | Reconciled named streams and managed-discovered document |
| Real frozen RecordSift CSV manual Source Link candidate | **4 / 4** | **3** | **INCOMPLETE_OR_UNCLASSIFIED_NATIVE_STREAMS** |

Every managed-reader-discovered source document in this frozen CSV candidate was matched to exactly one native named source checksum record, with algorithm GUID, bounds and physical source-byte SHA256 verified. The independent readers agreed on the four-document identity set, despite their original APIs exposing **zero** checksum bytes after path mapping. The new verifier **does not** require such managed-reader-exposed checksum fields to read and validate the native record; it therefore provides an independent research evidence pathway. **The seven native named source streams versus four managed-reader-discovered documents remain a coverage discrepancy.** Three streams have not been established to correspond to additional actual managed documents, nor established to be irrelevant. Their status must not be inferred from a 4/4 selected-source result.

**Original RecordSift unchanged:** source SHA `8358780829458854a4b0356df5ac5e685f0a34c8`, original and manual candidate each passed 425 API, 419 NUnit tests (418 pass, 1 skip, 0 fail), five XML docs, unpublished local nupkg, clean installed net48 consumer, five logical compatibility categories. The isolated validation did not change application code, packages, target framework, SDK project structure, original public API, or either main branch.

### Failure history retained

Initial [run 42152397808](https://github.com/infoconex/dotnet-modernization/actions/runs/42152397808) **FAILED**: the new verifier compared required source names case-sensitively against normalized inventory identifiers, causing nine of 21 unit tests to fail and the Windows prototype to fail closed at `REQUIRED_SELECTED_DOCUMENT_NOT_DISCOVERED`. The defect was corrected in source [commit 6597250630998c01da43c5c6527cda478cb9008a](https://github.com/infoconex/dotnet-modernization/commit/6597250630998c01da43c5c6527cda478cb9008a), and both new jobs then passed. This is a verifier implementation defect and correction, **not** a RecordSift source change or proof of new application drift.

### Independent technical review, five perspectives

**Build/release:** frozen original and manual Source Link candidate have independent repeated full API, NUnit, XML, package and installed-consumer evidence. The tests do not establish authentic Visual Studio Package Manager installation, native writer module identity, or a Microsoft-approved production checksum API.

**Quality:** independent reader document-set agreement, exact normalized full paths, native GUID/length/checksum decode, physical source bytes, wrong-directory same-basename, bad checksum, missing key, unsupported hash, malformed record, colliding physical basename, private manifest corruption and truncated/invalid stream tests all have focused synthetic coverage. Missing *native* source-stream provenance remains deliberately incomplete.

**Security:** PDB parsing is stdlib with explicit MSF and source-length bounds, trusted build-produced inputs, private manifests erased by `finally`; no vulnerable native COM library invoked. Nonetheless, **not a security-reviewed hostile-PDB parser**; process isolation, arbitrary-data rejection, dependency provenance and parser stress testing are not complete.

**Architecture/reuse:** tool is application-independent and records input/coverage limitations instead of depending on RecordSift runtime or package references. The first pilot intentionally rejects applications with duplicate source basenames; a future source identity mapping needs full-path keys and its own controls, not a basename shortcut.

**Governance:** the tool proves physical source hashes for managed-reader-discovered documents in the tested scope, not all independently existing native/PDB document records or all five RecordSift production assemblies. The established **Gate C remains UNSATISFIED** and may only be changed by explicit stakeholder approval. No PDB format migration, release adoption or application merge. The authentic Visual Studio project-package installation and remote Source Link breakpoint/step gate are **NOT TESTED**.

**Narrow next evidence gap:** privately classify the **three unmatched native named source streams** (structured checksum record vs unrecognized, whether they are referenced by native source-file/C13 record indices, and original physical-source availability) without leaking source paths or assuming they are relevant; then independently reconcile native document discovery with two managed inventories. Consider broadening the generic checker to explicit full-source-ID mappings and another frozen application only after that. Source Link **HOLD**.


## Independent review requirements

**Build/release:** capture pinned compiler/reader version, immutable source SHA, full historical release/consumer evidence and distinction between original Csc host and direct fixture. **Quality:** test wrong directory despite identical basename, hash mutation, missing document, reader disagreement, unsupported digest and malformed record lengths; report ambiguous inventories rather than passing. **Security:** only sanitized classification in Actions artifacts and console, no PDB/source/full paths or private URL manifests, strict bounds and firewall, no known vulnerable native reader. **Architecture:** reusable stdlib verifier is research tooling, not a RecordSift runtime/package dependency. **Governance:** no change to Source Link HOLD, real Visual Studio installation and stepping remain NOT TESTED.
