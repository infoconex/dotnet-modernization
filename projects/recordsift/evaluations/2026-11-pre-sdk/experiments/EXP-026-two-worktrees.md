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
