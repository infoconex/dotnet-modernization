# EXP-034 — Verify every independently listed owned CSV PDB source URL against immutable Git

**Status:** Research proof pending actual CI. Branch stacked after EXP-033; frozen RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8`, no application commits, research main merge or package publication.

EXP-028 proved one selected C# path. This experiment broadens that provenance test to **every distinct owned source file independently identified in the actual native PDB's LLVM `-modules -files -l` inventory**, rather than assuming all files matching a wildcard were compiled.

1. Build manually Source Link-integrated frozen traditional CSV with unchanged 425 API, 419 NUnit (418 passed/1 skipped), five XML, local package and installed consumer release gates.
2. Verify actual native Windows MSF7 PDB, `sourcelink` named stream, frozen SHA and PE CodeView GUID/age.
3. Parse actual LLVM file-reference lines, map filenames unambiguously to tracked owned `src/RecordSift.Infrastructure.Csv/**/*.cs` files, reject ambiguous or unknown *owned* filenames, require at least four and `CsvStreamImporterAdapter.cs`.
4. For **each independently listed tracked owned source**, apply the PDB Source Link wildcard, require exact HTTPS `raw.githubusercontent.com/infoconex/RecordSift/<frozen SHA>/...` URL, fetch raw content and compare **all bytes** to immutable `git show <SHA>:<relative path>`, not CRLF-transformed local checkout. Require source checkout diff clean.
5. Include six synthetic inventory parser negative/positive controls alongside the earlier nineteen remote-source controls and ten native-PDB reader tests on Windows and Ubuntu. Retain only per-file source-relative paths, SHA256 hashes, byte counts, and report assertions.

**Strict limitation:** This proves all **identified owned CSV source file URLs** in the selected native PDB inventory. It does not certify unknown external/compiler-generated PDB documents, actual native managed document **checksum records**, Visual Studio interactive debugging, conventional NuGet Package Manager installation, or host module-binding behavior outside EXP-032. An LLVM inventory limitation must be reported if sources are not actually listed. No raw source/PDB/packages uploaded.

Evidence: [EXP-028](EXP-028-remote-source-proof.md), [EXP-029](EXP-029-pdb-document-checksums.md), [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).

## Verified Windows CI and independent retained JSON evidence

**[Windows/Ubuntu workflow 41984558557](https://github.com/infoconex/dotnet-modernization/actions/runs/41984558557) passed** at implementation SHA `0e699127067e0f6a000892a05e102cf9fc90b4a8`: Windows original frozen provider-integrated candidate Release/consumer gates, plus cross-platform source inventory, HTTPS provenance, and native PDB structural negative controls. Retained [artifact 13395102732](https://github.com/infoconex/dotnet-modernization/actions/runs/41984558557/artifacts/13395102732) ZIP SHA-256 `548e086e175a3dd00300948f7b59675ec6ea05b9c51f13127be09bb83f15f400`, independently downloaded and inspected.

**Actual independent native PDB source-file inventory selected four distinct owned source documents** (one repeated LLVM entry deduplicated); each embedded Source Link mapping derived exact allowlisted raw GitHub URL for frozen commit `8358780829458854a4b0356df5ac5e685f0a34c8`, and **complete remote source bytes matched immutable `git show` blob bytes**:

| Owned PDB-listed source document | Exact frozen Git file bytes | Result |
| --- | ---: | --- |
| `src/RecordSift.Infrastructure.Csv/CharacterLimitedTextReader.cs` | 1,600 | Exact remote/Git bytes match |
| `src/RecordSift.Infrastructure.Csv/CsvRecordReaderAdapter.cs` | 4,738 | Exact remote/Git bytes match |
| `src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs` | 6,346 | Exact remote/Git bytes match |
| `src/RecordSift.Infrastructure.Csv/MalformedCsvException.cs` | 306 | Exact remote/Git bytes match |

Native PDB MSF7 structure, one Source Link JSON mapping and PE CodeView GUID/age matching PDB were also independently verified. The full original candidate preserved 425 public API entries, 419 NUnit (418 pass / 1 skipped), five XML, unpublished local package and clean net48 consumer, with all five logical compatibility categories matching. All six inventory fixture controls and existing remote URL/identity tests passed on both Windows and Ubuntu.

**Verdict: `VERIFIED_ALL_FOUR_INDEPENDENTLY_LISTED_OWNED_CSV_DOCUMENT_REMOTE_BLOB_BYTES`.** This is stronger than one-file EXP-028 and covers the **four distinct owned source files shown by this LLVM inventory**, not necessarily every native managed PDB document or generated/external file. **Per-document checksums stored in the PDB still NOT VERIFIED**, as EXP-029/033 independently reported no checksum indicators and EXP-031 patched native-reader probe remains security-blocked. Visual Studio interactive source stepping and conventional NuGet Package Manager project installation are also not established. No production push, merge or package publish.
