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


## Verified four-layout Windows acceptance results

**Final observed Windows CI**: [41979549061](https://github.com/infoconex/dotnet-modernization/actions/runs/41979549061), research implementation SHA `e1df09b253a52072a05b8473d9f14c6c31780ca5`, **all four independent jobs passed**, each exercising the identical original full release/consumer gates for the manually integrated CSV candidate. The source remains frozen and no application commits/publishes occurred. Earlier [41979011095](https://github.com/infoconex/dotnet-modernization/actions/runs/41979011095) exposed the provider provenance distinction: missing Source Link named stream in **both** no-remote and local-origin submodule despite success of all application compatibility gates. That absence is now independently verified as a **negative control** by `sourcelink_native_absence.py` (valid MSF PDB and matched DLL/PDB GUID+age, zero `sourcelink` named streams). It is not a Source Link integration success for those topologies.

| Authenticated Git configuration | Frozen release/consumer acceptance | PDB Source Link result | Artifact and digest |
| --- | --- | --- | --- |
| Real shallow repository, detached HEAD, GitHub origin | PASS | **Present**, frozen revision + PE/PDB identity verified | [13392898655](https://github.com/infoconex/dotnet-modernization/actions/runs/41979549061/artifacts/13392898655), `sha256:e6da28463a3339cb265075084294bc8b5375feb5953fc8806565ae9baeed5b9c` |
| Fully detached HEAD, zero remotes | PASS | **Absent**, independently verified negative | [13392817863](https://github.com/infoconex/dotnet-modernization/actions/runs/41979549061/artifacts/13392817863), `sha256:b0cd67962baa72d355b547b04bc1317942d7e3f2506183663cebc9a1aac15d0a` |
| Authentic parent gitlink mode `160000` and nested `.git` pointer, local-path origin | PASS | **Absent**, independently verified negative | [13393168132](https://github.com/infoconex/dotnet-modernization/actions/runs/41979549061/artifacts/13393168132), `sha256:b645547853ab098d67ef2422985062a8c298241bed9f21e884b769395244bff7` |
| Authentic parent gitlink and nested `.git` pointer, GitHub origin configured in parent `.gitmodules` and nested repo | PASS | **Present**, frozen revision + PE/PDB identity verified | [13393406701](https://github.com/infoconex/dotnet-modernization/actions/runs/41979549061/artifacts/13393406701), `sha256:bbb56965eb69170a0452b75bd001f15676d293542cede49f95c27341a1e397f9` |

**Scope conclusion:** Traditional net48 Source Link can still compile and pass tests when remote provenance prevents embedding Source Link metadata. CI must **separately enforce valid native Source Link mappings**, not use “build succeeded” as a proxy. Source Link is not universally guaranteed by shallow, detached, or submodule status alone; the effective provider remotes are material. This does not prove interactive debugger stepping or conventional NuGet project installation. All retained evidence contains metadata only, no PDB/binary/source uploads. Keep draft PR #47 unmerged.
