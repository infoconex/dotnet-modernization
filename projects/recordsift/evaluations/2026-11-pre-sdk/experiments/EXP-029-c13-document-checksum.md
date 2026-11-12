# EXP-029 — Native Windows PDB C13 document cryptographic checksums

**Status:** Research draft; real Windows CI evidence required before claim.

## Purpose

Existing EXP-025 verified one actual native Windows PDB `sourcelink` stream, JSON mapping, exact frozen Git SHA and DLL/PDB CodeView identity. EXP-028 tests remote source URL and file byte parity. Neither proves a document checksum was embedded in the PDB.

EXP-029 parses actual native Windows PDB **DBI stream index 3**, variable-length ModInfo records, module symbol streams, bounded C13 debug subsections, `DEBUG_S_STRINGTABLE` (0xF3) and `DEBUG_S_FILECHKSMS` (0xF4). It validates the checksum algorithm (MD5, SHA-1 or SHA-256), digest length, relative normalized owned document path, and digest bytes against the exact original tracked `src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs` at SHA `8358780829458854a4b0356df5ac5e685f0a34c8`.

- 11 bounded synthetic positive/negative tests run on Windows and Ubuntu.
- Full original and manually integrated CSV candidate release/consumer checks run on disposable Windows checkout before PDB parsing.
- Unsupported C13 debug records, missing string table, or unexpected paths fail closed; absence is an investigative finding, not automatic proof that compiler didn't write checksum information.
- Never execute or upload native PDBs, source files or binary assemblies. Persist only aggregate JSON.
- A passing selected document does **not** establish checksums for *all* owned/external/generated documents, nor actual interactive Visual Studio debugger stepping. Those are separate acceptance controls.

Standards: https://llvm.org/docs/PDB/DbiStream.html ; https://llvm.org/docs/PDB/ModiStream.html ; CodeView C13 FileChecksums subsection. See [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37). Draft stacked under EXP-028; no RecordSift main edits, no merges, no NuGet publish.
