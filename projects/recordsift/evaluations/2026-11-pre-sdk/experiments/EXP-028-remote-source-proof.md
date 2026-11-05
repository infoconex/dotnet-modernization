# EXP-028 — Source Link maps to exact frozen Git object bytes

**Date:** November 4, 2026 (Pacific). **Status:** VERIFIED within the bounded scope below; draft/unmerged.
**Frozen RecordSift:** `8358780829458854a4b0356df5ac5e685f0a34c8`.
**Research dependency:** Stacked on draft EXP-027 → EXP-026 → EXP-025 → EXP-024 → EXP-023B; do not merge into either main without consolidated stakeholder review.

## Question and scope

Does the *actual native Windows PDB* emitted by one manually Source Link-integrated traditional net48 CSV project map a selected owned C# document to an HTTPS raw GitHub file whose returned bytes match the **immutable source blob** at the exact frozen Git commit?

The selected tracked source is `src/RecordSift.Infrastructure.Csv/CsvStreamImporterAdapter.cs`. A single document-path mapping (for example `/_/*`) is resolved through the **actual PDB** `sourcelink` named stream to `https://raw.githubusercontent.com/infoconex/RecordSift/<frozen SHA>/<path>`, with strict host/commit/path/query/redirect checks. Source bytes are fetched from that allowlisted URL only. The source file must be tracked, the checkout HEAD must match, and `git diff --quiet HEAD -- <path>` must succeed.

Compare the remote bytes directly to `git show <frozen SHA>:<path>`, not naively to physical Windows checkout bytes, which can differ due to Git CRLF conversion. Verify all bytes, not merely a URL string or content length. Record the physical worktree comparison separately and require that any observed difference is consistent with **only** CRLF conversion. The actual DLL's PE CodeView GUID/age must match its native PDB before the mapping test.

This is **not** a per-document PDB checksum validation, multi-source coverage claim or real Visual Studio debugger stepping test.

## Verified Windows / cross-platform CI

**Primary full-gate run:** [41969360785](https://github.com/infoconex/dotnet-modernization/actions/runs/41969360785) on research SHA `2c0a972bc637bb80986053a52a99ec4a7ef7e05f`, **success**: actual Windows Source Link candidate with historical acceptance and real remote file parity; 19 Source Link URL/blob regression tests **and** ten native PDB reader structural controls passed on **both Windows 2022 and Ubuntu 24.04** (29 tests per OS). The [reusable tooling CI](https://github.com/infoconex/dotnet-modernization/actions/runs/41969360783) is tracked separately.

**Retained evidence artifact:** [13388549095](https://github.com/infoconex/dotnet-modernization/actions/runs/41969360785/artifacts/13388549095), ZIP SHA-256 `dcc20a2729420cfc226abc649f48d56b5331acf92e33956c151dea9bade72c6d`; independently downloaded and JSON inspected. Metadata-only: no raw sources, DLL/PDB, nupkg, credentials or binlogs uploaded.

| Real observed value | Result |
| --- | --- |
| Native PDB | Windows MSF7, Source Link stream count 1; one mapping |
| PE CodeView GUID and age vs PDB | Exact match |
| Source Link immutable URL and frozen SHA | Verified |
| Remote Git raw blob size | **6,346 bytes** |
| SHA-256 of **both remote bytes and frozen Git blob** | `bc861547bdba0b08119db108ddd51348960b7c4ecb61ae5811fc452f0cfab480` |
| Windows physical worktree size | **6,469 bytes** |
| Windows worktree SHA-256 | `5f9ca993ee682897fb55d077fd2a23159f4b72a30582a67a3f6cc9f8cdc85e19` |
| Worktree byte equality with raw blob | **False** |
| Worktree difference explained by CRLF conversion | **True** |
| Unchanged 425 API, 419 NUnit (418 pass/1 skipped), five XML, local nupkg and net48 clean consumer | **Passed using provider-integrated CSV candidate** |
| Five logical compatibility categories | Matched original |
| Changes to RecordSift tracked files, merges or publication | None |

The worktree/Git difference is expected for this Windows checkout and **must not** be mistaken for different committed source content. The correct raw Source Link URL resolves to the committed blob.

## Failed controls retained and corrections

- [41968504611](https://github.com/infoconex/dotnet-modernization/actions/runs/41968504611) inherited the **older PDB reader** in the stacked branch; it rejected a real `sourcelink` stream. Corrected reader and structural tests were explicitly synchronized from EXP-025.
- [41968825551](https://github.com/infoconex/dotnet-modernization/actions/runs/41968825551) surfaced the **physical Windows checkout vs Git raw blob** difference. We changed the proof boundary to immutable `git show` blob bytes and independently recorded CRLF-only worktree transformation.
- [41968966008](https://github.com/infoconex/dotnet-modernization/actions/runs/41968966008) found synthetic test mocks that returned a literal backslash-n sequence rather than valid Git stdout; negative and positive tests were corrected, not suppressed.
- [41969254434](https://github.com/infoconex/dotnet-modernization/actions/runs/41969254434) was invalid workflow YAML caused by a repository file-update string substitution; restored from previous known-good workflow and verified green.
- The final full-gate run `41969360785` passed with strict **schema version 2**, source SHA, 64-character checksum, nonempty file, and approved worktree newline classification assertions. The separate original candidate release controls also passed.

## Interpretation and remaining independent research

**Verdict: `VERIFIED_ONE_OWNED_SOURCE_LINK_URL_MATCHES_IMMUTABLE_GIT_BLOB`.** This experiment proves HTTPS mapping and exact committed-file byte provenance for **one** selected CSV source from the real native Windows PDB. It does not prove every PDB document record, full source checksum table and algorithms, real debugger stepping, authentic nested submodules/shallow clone/missing remotes, conventional Visual Studio NuGet Package Manager installation, or build-host process/module isolation. Those remain explicitly **unverified** separate research questions, not a reason to reclassify this bounded positive result.

No changes are authorized to RecordSift main; preserve draft PRs and the documented findings pending review. Related: [EXP-025](EXP-025-windows-pdb-identity.md), [EXP-024](EXP-024-sourcelink-windows-import.md), [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).
