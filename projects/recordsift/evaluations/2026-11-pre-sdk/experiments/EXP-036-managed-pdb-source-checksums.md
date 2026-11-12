# EXP-036 — Independently read managed source checksums from classic Windows PDBs

**Status as of November 5, 2026: CONTROL FIXTURE VERIFIED; FROZEN RECORDSIFT CHECKSUM ACCEPTANCE FAILED CLOSED.**
**Research only:** [Tracking issue #54](https://github.com/infoconex/dotnet-modernization/issues/54), parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37), stage 1 draft PR [#55](https://github.com/infoconex/dotnet-modernization/pull/55), fixture PR [#56](https://github.com/infoconex/dotnet-modernization/pull/56), application-scoped PR [#57](https://github.com/infoconex/dotnet-modernization/pull/57).
**Immutable application:** `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`, traditional C# 7.3/.NET Framework 4.8 with Release `pdbonly`. **No app main commits, research merge, dependency upgrades or publication.**

## Question and original evidence gap

EXP-029/033 LLVM native PDB listing and EXP-035 Visual Studio DIA source-file table found no usable checksum bytes (0/4 selected), but neither pathway directly read the *managed* document model. Roslyn classic-PDB tests show compiler support for document hashes. Could two distinct **fully managed** parser families decode actual checksum algorithm GUIDs and digest bytes, validate controlled physical source bytes, and do the same for frozen RecordSift?

This work separates **source file identity/URL provenance** (already established in EXP-034), **actual source-document checksum metadata authenticity** (this experiment), authentic VS Package Manager installation, and **interactive debugger remote fetch/stepping** (untested).

## Fixed package and tool provenance

Stage 1 [nonexecuting run 42082942825](https://github.com/infoconex/dotnet-modernization/actions/runs/42082942825) succeeded with nine synthetic archive controls and exact official NuGet archive identifiers, assets and SHA256. Relevant pinned material:

| Package | Official archive SHA-256 | Managed DLL SHA-256 |
|---|---|---|
| `dnlib 4.5.0` | `63bc2f9579568204cc8b30fa9f6700a231bcf868a8032e09118887af3eafee58` | `lib/net45/dnlib.dll`: `97ef5328d1d1703924c48d9cd1d45b7227fe3836e116dcded623b6a0dbd52c23` |
| `Mono.Cecil 0.11.6` | `d2a23832aaa948ba9a01acc42b5726e34c5f995958f1b30d45c0e7c70b3a72d5` | `lib/net40/Mono.Cecil.dll`: `c41bdb9ffd3c5f6e17d2382c1012d73703e035e3f1100245fdd4e08c8dc6eb5b`; `lib/net40/Mono.Cecil.Pdb.dll`: `50a1a1a79dc86fcfb8b51249b5325a10dd93d193c52999cf6775d25030a4e606` |

Only those three DLLs are loaded into separate disposable research-only executables: dnlib `PdbReaderOptions.None` chooses managed mode; Cecil `NativePdbReaderProvider` is **managed C#** and vendors Microsoft's CCI parser, not a native COM call. **Cecil and CCI are the same parser family**, but dnlib and Cecil are distinct. Exact binaries come from official pinned NuGet archive bytes, with no package installation or application dependency change.

An indexed third-party report alleges dnlib 4.5.0 malformed-input/resource-exhaustion issues; its full article was not independently retrievable. Security status for hostile files is **NOT established**; this research uses only controlled, locally compiled fixture PDBs or trusted frozen RecordSift build outputs, with process firewall outbound denial, 20-second limit and monitored 256MiB working set. No raw PDB, source, package or compiled reader artifact is retained.

## Phase 2 — known-good classic-PDB fixture: VERIFIED

Successful [Windows run 42085539647](https://github.com/infoconex/dotnet-modernization/actions/runs/42085539647) at research SHA `99316385d242561c6addde44fddd32a2308c4b1a`; independent static preflight [42085540228](https://github.com/infoconex/dotnet-modernization/actions/runs/42085540228) also PASS. Roslyn C# compiler version **4.14.0-3.26424.7** (compiler executable SHA-256 `cf32cb7e8e5691b962e1b6f92b03d87409dd9e7afbed71c5bf77b8203cc56ee1`), `/debug:pdbonly`, explicit independent `/checksumalgorithm:SHA1` and `SHA256`; two C# 7.3 files (UTF-8 BOM and no BOM; CRLF) per fixture.

- Both independent parsers enumerated **2/2** fixture checksum-bearing documents for SHA1 and **2/2** for SHA256.
- For every document the full checksum GUID and digest agreed across readers and matched the **physical compiler-input source bytes**.
- PE CodeView RSDS GUID/age matched MSF7 PDB identity. Wrong PE/PDB and post-compile one-byte source mutations were detected.
- Metadata-only artifact [13441669260](https://github.com/infoconex/dotnet-modernization/actions/runs/42085539647/artifacts/13441669260) ZIP SHA256 `a591b81bb3f15033acd89c28d331fc435466af180703dc433c7ceb20d8fb02c3`; independently inspected. No PDBs/binaries/source uploaded.
- Failed harness runs before final PASS were preserved in Actions history; they were script issues (action-pin syntax, PowerShell parser/strict mode, expected negative-control exit propagation), **not parser-compatibility failures**.

**Conclusion:** A fully managed reader can recover correctly signed SHA1/SHA256 *checksum metadata* from at least these compiler-generated classic Windows PDB fixtures. This does not prove checksum metadata authenticity, availability or completeness in any other build.

## Phase 3 — actual frozen RecordSift Source Link candidate: 0/4 × 2, FAIL CLOSED

**Candidate source:** exact frozen SHA above; disposable Windows 2022 checkout and EXP-024 manual Source Link import simulation (not VS Package Manager project installation). Two actual runs:

- [42086411004](https://github.com/infoconex/dotnet-modernization/actions/runs/42086411004) first exercised the full original candidate, then returned generic `InvalidDataException` from the reader's previously strict missing-checksum behavior. Diagnostic harness was refined; not counted as document validation.
- **[42087528244](https://github.com/infoconex/dotnet-modernization/actions/runs/42087528244)** at exact stage-3 research SHA `e78f388fa3a6086d34c1e703c63112eb65dc7785` reproduced and classified the result. Full original and candidate release/consumer checks passed: original 425 public API entries, 419 NUnit (418 pass/1 expected skipped), five XML docs, local unpublished NuGet 0.1.0 package, clean independently installed net48 consumer, five logical compatibility categories matched. Candidate real native Windows PDB and PE GUID/age matched, Source Link manual integration/build task observations preserved. Same-workflow known-good SHA1/SHA256 fixture controls passed again.

**Actual real-PDB document observations:**

| Reader | Unique source documents discovered | Documents with readable checksum bytes | Selected owned source documents |
|---|---:|---:|---|
| dnlib managed | **4** | **0** | All four `DISCOVERED_WITHOUT_HASH` |
| Cecil managed / CCI | **4** | **0** | All four `DISCOVERED_WITHOUT_HASH` |

Selected files: `CharacterLimitedTextReader.cs`, `CsvRecordReaderAdapter.cs`, `CsvStreamImporterAdapter.cs`, `MalformedCsvException.cs`. Both readers explicitly discovered all four yet returned **empty/missing checksum bytes**, even though the exact same harness and both parsers validated checksum bytes in the trusted fixture.

**Bounded verdict:** This is strong *reproducible, independent managed-reader negative evidence for this one actual traditional net48 CSV candidate*. Neither parser's returned document model supplies cryptographic source-checksum metadata, so the selected 4/4 hash-authenticity assertion cannot be met. Do **not** relabel this as actual hash equality, proof that the PDB has no bytes anywhere in alternate unparsed structures, a universal Windows-PDB/Roslyn limitation, or an application behavior failure. The final workflow was deliberately **FAILED** by this acceptance gate; no sanitized PASS artifact was uploaded. The exact reproducible CI logs and this written evidence persist.

## Next distinct investigation and decision boundary

The remaining useful question is **why** the traditional MSBuild/Roslyn candidate's actual managed documents differ from the command-line known-good fixture. Independently capture **exact candidate Csc executable/tool path and effective compiler arguments** (especially `/debug`, `/checksumalgorithm`, source encoding/normalization and shared compilation) and its loaded symbol writer, then design *one* isolated control that can distinguish compiler configuration from PDB-reader discovery. Do not presume SHA1 defaults or native FILECHKSMS claims settle the actual observed absence. No dependency/migration change is authorized.

**Current acceptance:** EXP-036 fixture **VERIFIED**; frozen CSV managed-checksum Gate C **FAILED CLOSED / INCONCLUSIVE for underlying physical PDB structures**; Source Link **HOLD**. EXP-031's vulnerable native reader remains **SECURITY-BLOCKED**; VS Package Manager project installation and actual Visual Studio source stepping **NOT TESTED**; other ten-project applicability unknown. No research PR merged or RecordSift production state changed.
