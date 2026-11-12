# EXP-026 — Source Link reproducibility in two authentic Git worktrees

**Status:** Research queued. Frozen RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8`. Stacked on EXP-025/024, all drafts.

## Hypothesis

Two *different physical source directories* at the exact frozen commit, one a regular checkout and one a genuine `git worktree add --detach` with a `.git` pointer file, should produce byte-identical CSV DLLs under manual Source Link 10.0.403 task imports and `Deterministic=true;ContinuousIntegrationBuild=true`. Native Windows PDB identity is separately observed, not assumed.

The experiment invokes EXP-024 separately in both worktrees: baseline full solution, manual imported CSV rebuild, the original 425 API/419 NUnit/five XML/local package/net48 consumer gates against the candidate, and five logical compatibility categories.

## Verification

- Require each worktree at identical immutable SHA; verify second has a real `.git` file pointer instead of simulating one.
- Run unchanged ESP-024 disposable candidate integration in each physical checkout; ensure no tracked application changes.
- Collect exact SHA-256 of CSV DLL and native Windows PDB from each and preserve their comparison in JSON without uploading binary bytes.
- Require identical DLL bytes for successful cross-worktree deterministic assessment; record PDB differences as observations for further diagnosis.
- Do not equate `git worktree` with a real nested Git submodule; submodules and shallow clone are additional independent controls.
- No RecordSift tracked commits, no application or research main merge, and no NuGet publish.

See [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37). 

## Verified Windows CI result

[EXP-026 run 41967459156](https://github.com/infoconex/dotnet-modernization/actions/runs/41967459156) **passed** on Windows 2022 at research commit `ae59ef86d063f30a670f825df44d08c3c22f3dc0`, after the initial `41967271489` PowerShell Test-Path parenthesization failure was corrected. Evidence artifact [13388605867](https://github.com/infoconex/dotnet-modernization/actions/runs/41967459156/artifacts/13388605867), ZIP digest SHA-256 `aa2b6b0458c75457a0b67b4f1de809bf4c1e8ebecf840aa2d2534c8983de2b3d`, was downloaded and its JSON inspected.

Both authentic, physically independent worktrees at frozen SHA `8358780829458854a4b0356df5ac5e685f0a34c8` passed EXP-024 manual Source Link candidate import/CSV build and original 425 API, 419 NUnit, XML, local package and installed consumer gates. Five logical compatibility categories matched for both. Worktree B used actual `.git` file-pointer layout.

- **CSV DLL SHA-256 both paths:** `b857f93fcb371cfeb74663113c330031ea37d8dd9cf2df6bd3ff6fa291dce3f4` (byte-identical).
- **Windows PDB SHA-256 both paths:** `4d0c4143690885d087d7828ec4978ee125c7260a4c54b188b2306532c8ed41e5` (byte-identical).

**Verdict:** `VERIFIED_SAME_COMMIT_TWO_WORKTREES_DLL_AND_WINDOWS_PDB_BYTE_IDENTITY` on one Windows runner with manual Source Link build-task imports. No claim about nested submodules, shallow clones, other machines, package installation, PDB Source Link JSON validity or actual debugger stepping.
