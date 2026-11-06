# EXP-039 — Reusable native Windows PDB source checksum verifier and document-inventory boundaries

**Status: research implementation submitted; runtime evidence pending. No Gate C approval or production adoption.**

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

## Evidence

**Pending first EXP-039 workflow.** If a test fails, preserve its run ID and exact sanitized failure category; no automatic waivers or invented results.

## Independent review requirements

**Build/release:** capture pinned compiler/reader version, immutable source SHA, full historical release/consumer evidence and distinction between original Csc host and direct fixture. **Quality:** test wrong directory despite identical basename, hash mutation, missing document, reader disagreement, unsupported digest and malformed record lengths; report ambiguous inventories rather than passing. **Security:** only sanitized classification in Actions artifacts and console, no PDB/source/full paths or private URL manifests, strict bounds and firewall, no known vulnerable native reader. **Architecture:** reusable stdlib verifier is research tooling, not a RecordSift runtime/package dependency. **Governance:** no change to Source Link HOLD, real Visual Studio installation and stepping remain NOT TESTED.
