# EXP-030 — Actual Git topology controls under traditional Source Link

**Status:** research only, requires actual Windows CI evidence; stack on EXP-029/028. Frozen RecordSift: `8358780829458854a4b0356df5ac5e685f0a34c8`. No tracked RecordSift edits/push, no package release or main merge.

## Authentic scenarios

Three isolated Windows 2022 jobs create different real Git layouts without faking .git metadata:

1. **Shallow detached HEAD**: initialize temp Git directory, fetch **one immutable commit** from actual GitHub remote with `--depth 1`, checkout detached, assert `--is-shallow-repository=true` and exactly one origin.
2. **No remote**: local exact-sha clone, detach HEAD, remove `origin`, assert zero remotes and non-shallow checkout.
3. **Genuine nested submodule**: initialize temporary parent repo, add RecordSift using `git -c protocol.file.allow=always submodule add`, commit `.gitmodules` and gitlink, assert mode `160000`, pinned nested SHA and an actual `.git` pointer file (not a hand-written fake).

In each fixture, attempt the **same** EXP-024 isolated Source Link build-task imports, original 425 API, 419 NUnit (418 passed / 1 skipped), five XML, NuGet pack, installed net48 consumer gates and logical compatibility checks, then run EXP-025 native Windows PDB parser against the result. A failed candidate is **not** automatically called an expected negative/pass. Preserve partial stage evidence; failed Git/provider hypotheses remain failures for review. The worktree submodule parent is disposable and never pushed.

A genuine no-remote result can reveal missing Source Link mappings, but no success criterion assumes it must fail; discover the actual behavior. The tests do not verify debugger stepping or PDB document-checksum digests. Source root/provider URL content in nested submodules may require separate byte validation.

This is a distinct positive/negative Git-topology experiment, not a substitute for the conventional Visual Studio NuGet Package Manager installation and MSBuild task host process isolation gates.

Related: [EXP-024](EXP-024-sourcelink-windows-import.md), [EXP-025](EXP-025-windows-pdb-identity.md), [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).
