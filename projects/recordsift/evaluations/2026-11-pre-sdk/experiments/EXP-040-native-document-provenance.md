# EXP-040 — Native DBI/C13 provenance and unmatched Windows PDB source streams

**Status (November 5, 2026): RESEARCH EXECUTION IN PROGRESS.** This report is not a claim of completed native coverage. Existing Gate C **UNSATISFIED**, Source Link adoption **HOLD**.

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

## Pending evidence

Final EXP-040 execution SHA, workflow outcome, sanitized artifact ID/digest, actual classifications of all three unmatched streams, and completeness disposition must be filled **only from observed CI**. Until then, the result is **NOT YET VERIFIED**. Even if the seven streams are classified, independent original-byte authentication, all-assembly source coverage, authentic VS Package Manager project installation and remote source debugging/stepping require separate evidence or approval. No Gate C redefinition is authorized.
