# EXP-029 — Independent native Windows PDB document/checksum audit

**Scope:** Research-only; isolated Windows source build from immutable RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8`. Stacked draft on EXP-028, no application changes or merges.

## Research question

Does the actual Windows PDB encode source-document identities and checksum records that can be independently matched to exact source bytes and their hashing algorithms, rather than merely containing correct Source Link JSON?

## Planned phases and proof levels

1. Build the EXP-024 Source Link candidate and run all existing original API (425 entries), NUnit (419 with 1 skipped), XML (five), package/consumer and logical compatibility gates.
2. Reuse EXP-025 to require native Windows MSF7 and matched PE/PDB CodeView identity.
3. Use **independent preinstalled LLVM `llvm-pdbutil dump -modules -files -l`** to inspect source-file references and whether checksum-related record information is exposed. Record only sanitized bounded summary JSON. This is an **exploratory inventory** and must not be reported as checksum verification.
4. If the independent tool exposes exact algorithm, document filename, and recorded digest, implement a separate fail-closed byte-level comparison against the **compiler input bytes**. The Windows checkout may contain CRLF, while immutable Git blob has LF (EXP-028), so do not assume which bytes the PDB records were generated from.
5. Add positive and deliberately corrupted checksum negative controls and independently verify file-to-record matching; otherwise preserve an explicit `NOT_VERIFIED` finding.

**Research limitation:** Even a verified C13 source file checksum is not a Visual Studio debugger source-stepping test. Real submodules/shallow remotes, NuGet install and MSBuild host task DLL loading remain separate work.

Sources:
- https://www.llvm.org/docs/CommandGuide/llvm-pdbutil.html (documented `-files`, `-l`, `-modules`).
- [EXP-028](EXP-028-remote-source-proof.md)
- [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37)


## Verified inventory result

**Successful execution:** [Windows 2022 run 41978667142](https://github.com/infoconex/dotnet-modernization/actions/runs/41978667142), research code SHA `598043642babd4a4c1737aa46907eace376dc7ee`. Original baseline and provider-integrated candidate passed 425 public API records, all 419 NUnit tests (418 pass/1 skip), five XML documentation checks, unpublished local NuGet package, clean installed net48 consumer and all five logical compatibility categories. Independent reader `llvm-pdbutil dump -modules -files -l` exited 0; selected C# source was present in the actual native PDB inventory, and existing EXP-025 independently verified PE/PDB identity and Source Link JSON.

**Retained metadata:** artifact [13392598479](https://github.com/infoconex/dotnet-modernization/actions/runs/41978667142/artifacts/13392598479), ZIP SHA-256 `cde5fefe3930bd22c8f7ff89b1bf62b6c708540ffa2a6b9f4dff34f83c384cde`, 30-day retention. Downloaded and inspected `exp029-document-inventory.json`: 116 output lines, **five file-reference lines containing '(no checksum)'**, selected `CsvStreamImporterAdapter.cs` present twice. Distinct displayed filenames included `CsvRecordReaderAdapter.cs`, `CsvStreamImporterAdapter.cs`, `CharacterLimitedTextReader.cs` and `MalformedCsvException.cs`. The duplicate record-reader entry means **five reported entries, not five unique files**.

**Precise conclusion:** LLVM reports no checksum **in the file metadata it can decode** from this managed classic Windows PDB. This is an **unverified PDB document-checksum acceptance gate**; do not claim that all PDB checksum records are absent or that a debugger cannot work. A second reader using the managed Windows PDB document interfaces must inspect `GetCheckSumAlgorithmId` and `GetCheckSum`, correlate exact compiler input bytes (Windows CRLF vs immutable Git LF), and include deliberately corrupted checksum negative controls before closing the gate.

**Earlier failed run:** [41978366739](https://github.com/infoconex/dotnet-modernization/actions/runs/41978366739) was a PowerShell empty Git-diff array harness defect. This was corrected without touching RecordSift. Do not classify a harness error as a product failure.

**Security gate for a future independent DiaSymReader experiment:** Do not execute older vulnerable `Microsoft.DiaSymReader.Native` packages; consult September 2026 Microsoft advisories [CVE-2026-69522](https://github.com/advisories/GHSA-2j8r-3c22-8565) and [CVE-2026-71328](https://github.com/advisories/GHSA-63gh-g2x5-x69v). Any separately provisioned reader must be assessed and patched (or use a verified updated Windows component) before running PDB parsing.
