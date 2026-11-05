# EXP-035 — signed Visual Studio DIA SDK native PDB document checksum feasibility

**State:** VERIFIED tool execution and original release compatibility; **INCONCLUSIVE** actual managed source document checksums. **Research only, no production authorization.** Tracking [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37). Builds a disposable frozen RecordSift checkout at `8358780829458854a4b0356df5ac5e685f0a34c8`.

## Research question

Can a Microsoft-signed DIA SDK already included with a supported Windows Visual Studio toolchain enumerate checksum types and bytes from the **actual classic Windows PDB** produced by the existing EXP-024 Source Link candidate, without installing or executing the unavailable patched `Microsoft.DiaSymReader.Native` NuGet package?

Microsoft documents `IDiaSourceFile::get_checksumType` and `IDiaSourceFile::get_checksum` for DIA PDB tables. DIA is **not** necessarily equivalent to `ISymUnmanagedReader.GetDocuments` for managed document records; a positive DIA result is scoped to the DIA-visible file inventory. A zero-checksum record must remain *inconclusive*, not silently accepted as an absent managed checksum.

## Independent acceptance controls

1. Compile a standalone C++ COM client against Visual Studio's own DIA SDK headers and import library. Load the exact Authenticode-verified Microsoft-signed VS DIA DLL by explicit path (not a registered old package); retain version and archive SHA-256 without leaking local paths.
2. Capture only source basenames, algorithm IDs, checksum bytes and bounded metadata, never original Windows absolute paths, raw source, DLL/PDB, or credentials.
3. Compare supported MD5/SHA1/SHA256 digest lengths and hashes to the **physical compiler checkout bytes**, not the LF-only Git blob. Unavailable digest, missing document, unknown algorithm or unsupported DIA source format is INCONCLUSIVE; mismatch, duplicate, malformed checksum or missing inventory terminator is FAILED.
4. Run eight independent synthetic controls on Windows and Ubuntu, including changed physical bytes, wrong algorithm, duplicates, LF/CRLF distinction and missing records.
5. Reuse existing EXP-024 full 425 API/419 NUnit/five XML/local unpublished NuGet/clean net48 consumer compatibility, and existing actual native PE/PDB CodeView identity.
6. Treat DIA-visible coverage as partial even if all four selected sources match. Never promote to complete managed document authenticity without independent `ISymUnmanagedDocument` inventory and negative controls. A signed DLL is not automatically proof of a patched runtime; retain installed VS image identity for later security review.

## Prior blockers and expected result interpretation

EXP-031 remains security-blocked: public NuGet did not offer the patched `Microsoft.DiaSymReader.Native >=18.9.0-beta1.26405.2`, and the vulnerable 18.8.x version must not execute. EXP-029/033 reported five LLVM native source entries with no visible checksum and no C13 checksum markers; neither proves managed documents lack checksums. This DIA comparison tests a genuinely different API and stops if the build tool/SDK cannot be established.

## Executed evidence and outcome — November 5, 2026 UTC

**Actual result: INCONCLUSIVE for managed document checksums; independently verified safe tool execution and original application compatibility.**

- Isolated research branch `research/exp035-dia-sdk-checksum-probe-20261105`, draft [PR #52](https://github.com/infoconex/dotnet-modernization/pull/52), corrected implementation SHA `dee47696abec2541dcf85a636b7a9fc768a78c46`. Base EXP-034 at `4e5f55637d89870335f2815fe1e3af4b9a5a805c`.
- **First run [41988037857](https://github.com/infoconex/dotnet-modernization/actions/runs/41988037857): FAILED** at research SHA `26e119287072cbe138eb6a605dfd577ca355ccd8`. The generated `compile.cmd` inadvertently concatenated `VsDevCmd.bat` and `cl.exe` into one command, yielding invalid arguments. Windows and Ubuntu synthetic controls **8/8 passed each** and original RecordSift release/consumer acceptance and PDB identity **passed before the harness failure**. The harness was corrected by writing two distinct command lines, without any application modifications. First-run metadata artifact `13396817233`, SHA-256 `09312253f4c7517df0fb36961fdcf69ca4c1511c49f6782ba9423509cb1041da`.
- **Corrected run [41988493390](https://github.com/infoconex/dotnet-modernization/actions/runs/41988493390): ALL THREE JOBS PASSED**, at implementation SHA `dee47696abec2541dcf85a636b7a9fc768a78c46`. Eight independently exercised comparator tests passed on **each** Windows 2022 and Ubuntu 24.04. Full original 425 public API, 419 NUnit (418 pass, 1 skip), five XML, locally packaged unpublished NuGet and independent clean net48 consumer, plus native Windows PDB / DLL CodeView identity, passed. C++ DIA reader compiled against the installed Visual Studio 2022 Enterprise DIA SDK and executed with the Microsoft Authenticode-signed installed DLL. The output classification was **`INCONCLUSIVE (0/4 selected documents)`**: no selected managed document checksum was confirmed to match the physical source bytes. This observation **does not prove** that the managed PDB contains no checksums, or that all DIA records are absent; DIA-visible enumeration is not authoritative for `ISymUnmanagedDocument`.
- **Corrected run artifact [13396623969](https://github.com/infoconex/dotnet-modernization/actions/runs/41988493390/artifacts/13396623969)**: 4,125-byte metadata-only ZIP, archived SHA-256 `72149233feba4cedbbf411b9fe0c605eef3e3c0ac7c370605b19e48cd6c83941`, 30-day retention. Contains original release and consumer acceptance summaries, native Source Link/PE identity, signed DIA tool identity/hash and explicit inconclusive per-document assessment. **No PDB, DLL, raw source, or unredacted absolute source file paths uploaded.**
- [Reusable tooling run 41988493694](https://github.com/infoconex/dotnet-modernization/actions/runs/41988493694) passed at the same implementation SHA.

### Independent engineering review

| Perspective | Assessment |
| --- | --- |
| Architecture | Independent research-only C++ reader and Python comparator have no coupling to RecordSift source or distributable packages. DIA-visible sources cannot be equated with managed document inventory. |
| Build / reproducibility | Real frozen native Windows PDB generated by verified manual tool imports, native DLL/PDB identity and all original release gates passed; the new reader was executed rather than guessed from metadata. Zero checksum matches is **inconclusive**, not negative proof. |
| Security | No older vulnerable `Microsoft.DiaSymReader.Native` dependency was installed/executed. Installed DIA SDK DLL passed Microsoft Authenticode check and SHA-256 identity retained, but signature alone is **not** an advisory/patch-level safety certification. Never silently fall back to vulnerable packages or parse untrusted PDBs outside bounded research isolation. |
| Release / quality | Positive and corrupted negative controls passed on both Windows and Ubuntu. Historical 425 API/419 NUnit/five XML/unpublished package/clean consumer remained intact. Synthetic controls validate the comparator, not actual managed PDB document checksums. |

### Decision

**Do not clear native managed PDB checksum acceptance.** EXP-031 remains SECURITY-BLOCKED on an independently audited patched managed reader. Conventional Visual Studio Package Manager Console installation and interactive debugger stepping remain NOT TESTED. EXP-032 host module observation remains PARTIALLY VERIFIED beyond its inspected AppDomain. Source Link adoption stays **research HOLD**. Deterministic/PathMap/SourceRoot preparation remains a separate low-risk candidate to consider after stakeholder review, not authorized for application merge.

**Do not merge**. Do not modify either repository's main branch, publish packages or claim debugger stepping verified. Record final actual CI run/head/status and artifact hash only after inspecting the run.
