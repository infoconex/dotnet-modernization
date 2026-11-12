# EXP-025 — Native Windows PDB Source Link and PE identity (structural)

**Status:** Candidate research, independent verification pending. Stacked on disposable EXP-024, itself stacked on EXP-023B. No application commits or merges.

## Purpose

EXP-024 demonstrated that correctly pinned Source Link build tasks can be manually imported into the frozen traditional CSV project and reach a compiler `/sourcelink` invocation while preserving `DebugType=pdbonly`. That alone does not prove the compiler embedded valid data into the resulting Windows PDB.

EXP-025 tests the native structures using a **standard-library binary reader, not a raw text grep**:

- Verify the MSF7 superblock, directory block map, individual indexed stream lengths and block numbers.
- Parse PDB Info Stream 1, string table, present/deleted hash bits and named stream index table.
- Retrieve `sourcelink$N` named stream bytes and parse actual UTF-8 Source Link JSON.
- Require nonempty mappings using HTTPS URLs that contain exact immutable RecordSift commit `8358780829458854a4b0356df5ac5e685f0a34c8`.
- Parse the PE/COFF debug directory of the compiled CSV DLL and require one actual `RSDS` CodeView record whose GUID and age match the PDB Info Stream.
- Reject missing metadata, structurally malformed streams, duplicate keys, mismatched DLL/PDB, and wrong SHA. Run synthetic positive/negative fixtures on Windows and Ubuntu.
- Build the candidate in a disposable Windows checkout via EXP-024, then inspect its real PDB; do not upload binary or debug symbols.

**Important boundaries:** This first structural reader does **not** yet decode per-source PDB document/checksum records, prove remote raw source byte identity, validate external/generated source locations, demonstrate debugger step-through, or test detached HEAD/shallow/submodule behavior. All remain required follow-up acceptance controls. A `srcsrv` stream is not an acceptable substitute for native `sourcelink$N` metadata.

The reader implementation follows LLVM's documented MSF superblock, PDB stream and serialized name map formats. This is a limited format implementation: unsupported stream-directory layouts fail closed rather than silently skipping data.

## References

- https://llvm.org/docs/PDB/MsfFile.html
- https://llvm.org/docs/PDB/PdbStream.html
- https://llvm.org/docs/PDB/HashTable.html
- https://github.com/dotnet/symreader-converter
- [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37)
