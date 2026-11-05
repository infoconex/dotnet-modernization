# EXP-035 — signed Visual Studio DIA SDK native PDB document checksum feasibility

**State:** PROPOSED / PENDING CI. **Research only, no production authorization.** Tracking [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37). Builds a disposable frozen RecordSift checkout at `8358780829458854a4b0356df5ac5e685f0a34c8`.

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

**Do not merge**. Do not modify either repository's main branch, publish packages or claim debugger stepping verified. Record final actual CI run/head/status and artifact hash only after inspecting the run.
