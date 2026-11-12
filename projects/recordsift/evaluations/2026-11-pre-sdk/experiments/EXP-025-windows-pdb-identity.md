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

## Verified native Windows PDB experiment

[Run 41967860715](https://github.com/infoconex/dotnet-modernization/actions/runs/41967860715) **passed** real Windows PDB identity/mapping and ten binary-parser regression tests on Windows and Ubuntu at `ad73035d20f609f031ccee11e4879c9101a32611`. Retained ZIP [13388915075](https://github.com/infoconex/dotnet-modernization/actions/runs/41967860715/artifacts/13388915075) SHA-256 `25db7ee11b9a72e2296fc71745afccce3bee45279e780be12203c587248d22c1`; downloaded JSON independently inspected:
`format=windows-msf7`, `pe_codeview_pdb_identity=matched`, `source_link_stream_count=1`, `document_mapping_count=1`, `native_source_link_json=structurally_parsed`, exact source SHA `8358780829458854a4b0356df5ac5e685f0a34c8`. Generated intermediate `RecordSift.Infrastructure.Csv.sourcelink.json` SHA-256 `2aef090374c88c11372b945ee11f0e672910394dd2bd7b612477b00296aa105e` also contained one mapping and the frozen SHA.

**Important failed controls:** The original reader expected only `sourcelink$N`, yielding [run 41966879747 failure](https://github.com/infoconex/dotnet-modernization/actions/runs/41966879747) despite working compilation. A subsequent read of **actual PDB named streams** found exact `sourcelink` (without suffix); reader was corrected to accept both exact `sourcelink` and numbered variants, and the synthetic fixture updated. Earlier failure is a *reader assumption error*, not proof of absent Source Link. No native PDB or application binaries uploaded. Independent `llvm-pdbutil` was available on the Windows runner, but not used as a second structural assertion in this phase.

**Verified narrow verdict:** Native Windows PDB contains correctly parsed Source Link JSON mapping with exact frozen revision and its GUID/age matches compiled DLL. Still missing: per-document PDB checksums, HTTP resolution of exact source bytes, actual debugger stepping and negative Git layout controls. Those must remain separate follow-ups.
