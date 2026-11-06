# EXP-040 — Native DBI/C13 provenance and unmatched Windows PDB source streams

**Status (November 5, 2026): VERIFIED NATIVE DOCUMENT PROVENANCE; SEVEN NATIVE-REFERENCED DOCUMENTS, FOUR WITH PROVEN PHYSICAL INPUT BYTES; GATE C UNSATISFIED.** Source Link adoption **HOLD**.

## Scope and immutable controls

Tracking [issue #64](https://github.com/infoconex/dotnet-modernization/issues/64), parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37), stacked draft [EXP-040 PR #65](https://github.com/infoconex/dotnet-modernization/pull/65) on unmerged [EXP-039 PR #63](https://github.com/infoconex/dotnet-modernization/pull/63). Frozen RecordSift SHA: `8358780829458854a4b0356df5ac5e685f0a34c8`. Application unchanged, no dependency upgrades, no research merge, no publication and no gate/policy changes.

EXP-039 successfully audited 4/4 separately validated physical original CSV compiler inputs but counted **seven** native named `/SRC/FILES/` streams, leaving **three** unmatched against the two independently agreed four-document managed-reader inventories. The unmatched streams are not automatically extra managed documents or irrelevant metadata.

## Questions and separate evidence families

1. Does each native named source stream contain a structurally supported injected checksum record or an unknown payload? This identifies record format, **not** whether a source document exists.
2. Does the native DBI File Info substream link a module to each source name? DBI module file references represent a source universe independent of the reader inventories.
3. Do the module C13 `FILECHKSMS` subsections contain checksums associated with source names in the native `/names` table? Do C13 line records refer to specific FILECHKSMS record offsets?
4. Do the resulting **full normalized keys** associate with the reader documents and the seven named source streams without basename-only comparison, duplicate identities or unsupported structures?
5. Are exact original compiler-input bytes independently present for every additional relevant source? The four previously verified inputs must not be generalized to other documents.

`tooling/validators/native_pdb_document_inventory.py` uses the Python standard library and existing bounded MSF7/PE CodeView parsers. It privately reads the same two pinned-reader original-URL manifests captured by EXP-038/039 and inventories DBI module source records, C13 checksum associations and C13 line blocks. It emits only aggregate counts, fixed status categories and opaque ordered identifiers (`unmatched-1`, etc.); source paths, stream keys, digest hex, raw PDBs and source input bytes are not published. Malformed or unexpected structures cause fail-closed termination. Unrecognized native stream payloads remain unclassified instead of silently accepted.

**Evidence limitation:** DBI File Info, C13 `FILECHKSMS` and C13 line records are not necessarily equal sets. Absence of one family cannot prove that a native named stream is irrelevant, and a structurally valid orphan checksum alone cannot prove it is a managed source document. This diagnostic does not currently independently authenticate original bytes for any newly discovered source. The parser is restricted to trusted build-produced symbols; hostile PDB safety has not been established.

## Execution design

- **Offline:** `python3 -m unittest discover -s tooling/validators/tests -p 'test_native_pdb_document_inventory.py' -v`. Positive and negative controls cover the joined DBI/C13/line reference, unmatched referenced or unreferenced streams, unknown payload, duplicate native keys and stream IDs, unsupported C13 hashes, malformed offsets/lengths, absent checksums, wrong module stream, independent reader disagreement and missing DBI. Existing 21 EXP-039 checksum verifier controls rerun independently.
- **Windows:** `.github/workflows/validate-exp040-native-document-inventory.yml` reruns pinned reader preflight, five direct-Roslyn differential fixtures and actual frozen CSV, full original and manual candidate EXP-024 acceptance, then validates native provenance *before the two reader manifests are deleted in finally*.
- **Retention:** Only sanitized `exp040-summary.json` and previous EXP-037/038/039 metadata are eligible for the 30-day GitHub Actions artifact. Never include actual PDB, DLL, source or private reader URL manifests.

## Provisional interpretation

| Condition | Interpretation |
|---|---|
| Unmatched named stream has DBI or C13 reference | Additional native-referenced source candidate; exact original bytes and source identity need verification. |
| Unmatched named stream has no parsed DBI or C13 reference | Still unclassified; absence from the parsed families is not proof of irrelevance. |
| No DBI or C13 structures observed | No independent native document completeness proof from those structures. |
| Unsupported C13 algorithm, conflicting identity or malformed structure | Fail closed, preserve negative outcome and isolate tool/harness errors. |
| 4/4 original reader-discovered physical sources still match | Existing EXP-039 scoped checksum result preserved; does not satisfy Gate C. |

### Reviewer perspectives and release governance

**Build engineering:** distinguish direct csc fixture output from actual frozen RecordSift candidate; do not infer compiler identity from the fixture. **Security:** only bounded, trusted, locally produced PDB inputs; never execute untrusted native symbol COM parsers; no private data or raw symbols in logs/artifacts. **Architecture:** generic parser, exact full normalized keys, no RecordSift-specific path assumptions or external dependencies. **Quality:** test both match and mismatch/ambiguity, retain failures. **Release governance:** full original/candidate 425 API, 419 NUnit (418 pass/1 skip), five XML, unpublished package, clean consumer and five logical compatibility categories required; no green workflow alone proves the native document universe or policy acceptance.

## Verified execution and independent provenance result

**Latest passing code execution: [GitHub Actions 42159910996](https://github.com/infoconex/dotnet-modernization/actions/runs/42159910996)**, executing research SHA `fdfad1ee176fa72eded4cd9c2e73ed669dbca6ad`, both Windows and Ubuntu jobs **PASS**. The Ubuntu self-tests passed **21/21 EXP-039 checksum controls plus 23/23 EXP-040 native provenance controls = 44/44**. Windows passed frozen original/candidate EXP-024 API **425**, NUnit **419 discovered / 418 passed / 0 failed / 1 expected skipped**, **five** XML documentation files, locally unpublished NuGet package, installed clean net48 consumer, and five logical compatibility categories. Five Roslyn options still validated **1/1** physical source bytes, and the actual frozen RecordSift CSV passed **4/4** independently supplied physical compiler-input SHA256. This repeated full release acceptance is about unchanged application contracts, not complete native source coverage.

**Final sanitized artifact:** `exp040-native-source-provenance-sanitized-metadata`, **ID 13476346930**, GitHub-reported ZIP digest `sha256:75e49fde5a2af9c3ec658d7ee219251d991cd83e115ac493e8a07d6f59589bc7`, 30-day retention. Private PDBs, DLLs, complete source paths, managed reader URL manifests, original source files and digest bytes were never uploaded.

### Frozen RecordSift CSV: native source universe

| Evidence family | Verified counts and classification |
|---|---|
| Independently agreed managed-reader document URLs | 4 unique documents; both readers still expose **0/4** checksums |
| Native named `/SRC/FILES/` keys | **7** unique SHA256-bearing source records; four identified in managed inventory |
| DBI File Info source identities | **7** distinct source documents |
| C13 `FILECHKSMS` source identities | **7** distinct source documents, **8** record occurrences |
| C13 checksum algorithm | **NONE in all 8 entries** (no C13 digest bytes to compare) |
| Repeated C13 identity | 1 additional occurrence, with matching NONE record structure (no conflicting checksum) |
| C13 line-block referenced document identities | **4**; the three unmatched streams have none |
| Three unmatched named-stream keys | Each holds supported native **SHA256**, is independently referenced by DBI and C13, and is absent from both managed reader inventories |
| Original physical compiler-input bytes | **4/7 verified** using exact independently supplied bytes; **3/7 unavailable/unverified in this experiment** |

**Verified conclusion:** the three additional streams are **not unreferenced metadata**. Each is an additional structurally valid **native-referenced source document**. C13 NONE identifies the document but cannot authenticate its bytes. The separate `/SRC/FILES/` SHA256 payload establishes a native digest value but no original compiler-input-byte proof until an independently trusted physical source is supplied. Missing line-block references suggest no code contribution recorded in the parsed C13 line data; they do **not** prove source generation, compiler injection, absence of other roles, or safe irrelevance. Exactly which of the seven are user-owned, generated, external or compiler metadata remains **UNCLASSIFIED BY ORIGIN**. The distinction must be maintained when reusing this method.

### Failure history and correction — preserved

- **[42158428256](https://github.com/infoconex/dotnet-modernization/actions/runs/42158428256)**: first synthetic job passed; frozen original/candidate release checks passed; Windows EXP-040 failed closed without granular diagnostic.
- **[42158692466](https://github.com/infoconex/dotnet-modernization/actions/runs/42158692466)**: diagnostic showed `INVALID_C13_LINE_BLOCK` on the first controlled fixture. The experiment parser incorrectly interpreted CodeView line-block `BlockSize` as excluding the fragment header. LLVM's [DebugLinesSubsection.cpp](https://www.llvm.org/docs/doxygen/DebugLinesSubsection_8cpp_source.html) independently confirms `BlockSize` **includes** the header. Parser and negative regression control were corrected; these were **research harness defects, not RecordSift regressions**.
- **[42159097881](https://github.com/infoconex/dotnet-modernization/actions/runs/42159097881)**: both jobs pass, native 7/7 DBI and C13 source identity association and 3/3 orphan categories verified. Metadata-only artifact **13475977260**, ZIP digest `sha256:2ffa8b41a4098f7a91c8c454b163a17e9fa4c1cc36e4ad9b30eeff8d806f2e64`.
- **[42159594243](https://github.com/infoconex/dotnet-modernization/actions/runs/42159594243)**: both jobs pass after adding C13 digest/reference consistency and duplicate/conflicting-document controls. Metadata-only artifact **13476371301**, ZIP digest `sha256:b32a9f2934f30a7283539a25d46599ba92c9dd56b3827b3f8d0161ea44b2e17c`. All seven C13 document records were not directly comparable with named-stream SHA256.
- **[42159910996](https://github.com/infoconex/dotnet-modernization/actions/runs/42159910996)**: both jobs pass after reporting categorical C13 algorithms; **eight NONE / seven distinct** establishes why C13 was not digest-comparable. The final physical-source coverage result remains **4/7**.

### Five-perspective independent engineering review

**Build:** confirmed frozen commit, existing original and manually isolated candidate release validation, verified direct compiler fixtures separately, and distinguished native PE/PDB pairing from unproven compiler-server/writer provenance and original inputs for three records.

**Security:** trusted compiler-created PDB scope, bounded MSF/DBI/C13 parsing, name/index/length limits, missing reference and malformed format negative controls, no vulnerable native COM reader or hostile input, private original document URLs erased in `finally`, metadata-only output. A custom parser is **not** approved for hostile PDB ingestion.

**Architecture/reuse:** independent native DBI File Info, C13 checksums, C13 line relationships, normalized full-path named streams, and independent managed-reader inventories; no application-specific source paths hardcoded in generic parser; no third-party dependency added. Do not conflate a C13 NONE record with a native SHA256 checksum.

**Quality:** 44 offline controls across both suites, wrong/duplicate source identity and stream ID, unsupported C13 algorithm, truncation, incorrect checksums, malformed module references, C13 line-size mismatch, repeated matching and conflicting records, missing DBI and reader disagreement. Original harness failures retained and corrected with regression controls. Important remaining negative test: physical bytes of the three extra input documents cannot be verified without a trusted source acquisition pathway.

**Release/governance:** application contracts preserved; 4/7 original source-byte proof and 0/4 existing managed API digest exposure still insufficient for existing Gate C. **Gate C UNSATISFIED, Source Link HOLD**, and authentic Visual Studio Package Manager project installation, Source Link source retrieval and interactive debugger stepping **NOT TESTED**. No production adoption, research or application merge, application package/pin changes, or publication.

## Next narrowly scoped investigation and approval boundary

Capture the actual compiler input identities separately (e.g., an ephemeral trusted `Csc` task item manifest) for the frozen candidate; independently classify each of the three native-referenced records as checked-in, generated, external or unavailable without recording names publicly. Bind **complete compiler input identity** (including path-map normalization) to the existing native stream keys, not solely basename or raw checksum matching. Verify SHA256 only against the exact original compiler-input physical byte contents; document unavailable generation outputs as **UNVERIFIED**, not omitted. Preserve C13 NONE provenance and all negative controls, then evaluate the full five-production-assembly scope if the source audit is credible.

An alternative standalone native-checksum audit could only be **proposed** as a Gate C evidence pathway after full source-universe and byte proof. **Adoption of that alternate gate, Source Link production use, and any merge/publish remain separate explicit stakeholder approval decisions.**
