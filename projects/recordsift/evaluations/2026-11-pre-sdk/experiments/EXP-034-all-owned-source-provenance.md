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
