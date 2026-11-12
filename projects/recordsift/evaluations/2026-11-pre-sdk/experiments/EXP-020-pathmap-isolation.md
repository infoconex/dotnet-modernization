# EXP-020 — isolate normalized source paths for deterministic traditional .NET Framework builds

**Assessment date:** November 4, 2026. **Status:** **Verified for the tested seven-build Windows source-path experiment; research draft PR #34 unmerged.**
**Application:** infoconex/RecordSift, frozen immutable source SHA 8358780829458854a4b0356df5ac5e685f0a34c8.
**Dependency:** Stacked on [EXP-019 draft PR #33](https://github.com/infoconex/dotnet-modernization/pull/33), which itself depends on unmerged EXP-018 PR #32. None of these research PRs have authorization to merge. No RecordSift source or project edits are proposed.

## Why investigate

EXP-019 verified that enabling the existing MSBuild property Deterministic=true for all ten traditional net48 projects yielded five of five **byte-identical DLLs** in a **same-checkout repeated** build but **zero of five** identical DLLs in two separate worktrees built from exactly the same frozen Git commit. All existing API/NUnit/XML/package/installed-consumer gates passed. Changes in MVID, COFF and CodeView/PDB metadata were observed without raw method-IL hash drift.

The C# compiler's deterministic inputs can include full source paths. Microsoft's [Deterministic compiler inputs](https://github.com/dotnet/roslyn/blob/main/docs/compilers/Deterministic%20Inputs.md) and [MSBuild PathMap property](https://learn.microsoft.com/en-us/visualstudio/msbuild/common-msbuild-project-properties) describe path normalization; the C# [compiler advanced options](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/main-compiler-option) document PathMap.

**Question:** Can explicit source-root path mapping make identical-source DLL outputs byte-identical when different checkout locations are used? Can we demonstrate that a deliberately wrong canonical map changes compiled byte evidence, to verify the mapping is not merely an unused MSBuild setting?

## Seven full-gate builds, source never changed

The [Windows runner](../../../../../tooling/pilots/recordsift/EXP-020/run.ps1) and [workflow](../archives/workflows/validate-recordsift-pathmap-isolation.yml) reuse EXP-019 without modifying its accepted controls:

1. Historical source build without deterministic override.
2. Deterministic=true original checkout, no PathMap.
3. Deterministic=true separate checkout, no PathMap.
4. Deterministic=true original checkout **rebuild**, no PathMap.

The original controls must reproduce an observed cross-worktree byte mismatch in at least one DLL and a 5-of-5 identical same-directory repeat. The script then executes:

5. Deterministic=true, original worktree, physical source-root mapping to the common virtual prefix /_recordsift.
6. Deterministic=true, second worktree, its different physical root mapped to the **same** virtual prefix /_recordsift.
7. Deterministic=true, second worktree, deliberately incorrect virtual prefix /_recordsift_intentionally_wrong.

Actual command-line MSBuild property arguments are used, rather than modifying Directory.Build.props or traditional csproj files. All five production projects must evaluate Deterministic to true, and PathMap to the exact requested physical-root-to-virtual-prefix value. The wrong-map build is a **negative control**: at least one compiled DLL must differ from the correctly mapped original build, proving that differently normalized paths have a detectable effect. The correctly mapped cross-directory comparison is an *observation*: neither a match nor mismatch is pre-assumed.

For **every one of the seven builds**, independently run original acceptance checks: 425 compiled API/metadata entries, all five NUnit suites (419 tests, 418 pass, zero fail, one skip), five XML docs, local unpublished NuGet 0.1.0 pack and clean installed net48 consumer including Getting Started examples. Require all five selected logical compatibility components to match historical baseline for each of the mapped and wrong-map builds. Require source commit SHA to remain frozen and tracked source files unchanged. No application commits or package publication.

## Evidence and limits

Reuse the standalone [managed PE metadata reader](../../../../../tooling/pe-provenance/README.md) and [three-snapshot comparator](../../../../../tooling/validators/pe_variation.py) to record exact SHA-256 of each of five binaries, MVID, COFF, debug-directory CodeView data (hashed raw path) and raw method IL byte hashes per metadata token. The unmapped negative control, correctly mapped candidate and intentionally incorrect mapping have distinct reports. All raw compiler paths, package DLLs, PDBs and nupkg bytes stay on the disposable runner; uploaded artifacts contain JSON and selected gate/NUnit results only.

A matching DLL hash across these two checkout locations demonstrates **scoped byte identity**, not build hermeticity, cross-machine reproducibility, supply-chain trust, full binary/ABI compatibility, secure signing, or all-runtime-consumer parity. The experiment does not independently inspect actual C# compiler argv (only the global properties as evaluated by MSBuild). No other compiler/debug/project/framework/package setting is deliberately changed. Do not generalize this canonical source path mapping to paths outside the checkout without separate validation.

If the correctly mapped outputs still differ, report that result rather than weakening the experiment. If the wrong-map negative yields no DLL changes, reject the claim that the path mapping is causally exercised. Do not recommend production RecordSift changes until fully reviewed and explicitly approved.

## Verified Windows results

[Successful Windows Actions run 41905350490](https://github.com/infoconex/dotnet-modernization/actions/runs/41905350490), experiment branch commit 6f8e01ee99031ca353e8e9f56404b117f0846e40. [Artifact 13360690760](https://github.com/infoconex/dotnet-modernization/actions/runs/41905350490/artifacts/13360690760), SHA-256 digest 56be38d563feb66de3b3ac506c7a87ff9efcba17d4fb8c340da9615ba958b59c, 30-day retention. The immutable RecordSift source SHA for **every** one of the seven builds was 8358780829458854a4b0356df5ac5e685f0a34c8; the two distinct worktree sources had identical Git trees. No source or project file modifications were made.

### Byte-level observations

| Experiment control (all same Git source SHA) | Identical DLL byte hashes across different worktrees | Raw method IL token differences |
| --- | ---: | ---: |
| Historical/unmapped deterministic opt-in, two worktrees (EXP-019 repeated control) | **0 of 5** | 0/5 |
| **Identical virtual source root** /_recordsift on both different worktrees, Deterministic=true | **5 of 5** | 0/5 |
| **Intentionally wrong virtual source root** /_recordsift_intentionally_wrong in second worktree, versus correct mapping in first | **0 of 5** | 0/5 |

All five complete compiled DLL binaries (not merely method IL) had matching SHA-256 when the physical checkout roots were mapped to the same canonical virtual source path. The intentionally wrong map changed all five DLLs, proving in this tested environment that the mapping value has an observable compiled-byte effect. The original unmapped controls reproduced the previously verified cross-directory differences.

The experiment required each of the five production projects in all mapped variants to evaluate MSBuild Deterministic=true and the **exact physical-root-to-virtual-root PathMap value**. The JSON artifact records the actual evaluated properties, full PE file SHA-256, MVID, COFF/debug fields and raw method IL hashes for all five managed DLLs from each mapped build.

### Original user-facing acceptance results

**All seven** full solution restores and Release rebuilds independently passed:

- Original **425-entry** compiled public API and package metadata gate.
- Five independent NUnit suites: **419 discovered / 418 passed / 0 failed / 1 skipped**, for **each** build.
- Five XML documentation outputs; unpublished 0.1.0 local NuGet package creation/validation; independent clean installed net48 consumer and all existing Getting Started examples.
- The five selected logical compatibility contract categories **matched** between historical baseline and each correctly/incorrectly mapped candidate.

The source-mutation/commit guard and missing/invalid PE evidence controls remain enforced by the predecessor research harness and readers. Full actual application acceptance is **not** replaced by a hash match.

### Interpretation and remaining limits

For **this exact frozen RecordSift source, Windows runner, pinned SDK 10.0.403 for the metadata reader and tested VS MSBuild toolchain**, the combined compiler-property settings Deterministic=true and physical-root PathMap to a **shared canonical virtual root** produced byte-identical DLL files across two distinct checkout directories. The controlled wrong map produced differing bytes. This is stronger than EXP-019's same-directory deterministic repeat.

This does **not** prove byte-identical NuGet archive ZIPs, PDB files, strong-name signatures, all external dependencies or every generated file. Different toolchain versions, build modes, machines, signing inputs and additional paths outside the normalized source root have not been tested. The source-mapping setting also changes source path information that can affect debugger/PDB interpretation; examine source-debugging/source-link tradeoffs before recommending application adoption. Effective MSBuild properties, not the final C# invocation, were captured.

**Recommendation:** Treat Deterministic plus canonical PathMap as **a candidate for future pre-SDK changes**, subject to independently reviewed MSBuild/compiler behavior, full debug-symbol/source retrieval assessment, CI replay on additional environments, and explicit stakeholder approval. Do not commit these options to RecordSift or merge any research branch based solely on this experiment.

**Approval status:** Research only. Draft PR #34 stacked on unmerged PR #33, which depends on unmerged PR #32. Previous independent PRs #28 and #30 remain unmerged. RecordSift main and modernization main are frozen at their previously approved commits.

