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
