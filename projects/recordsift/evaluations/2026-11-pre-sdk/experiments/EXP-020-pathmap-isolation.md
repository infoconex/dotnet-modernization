# EXP-020 — isolate normalized source paths for deterministic traditional .NET Framework builds

**Assessment date:** November 4, 2026. **Status:** Pending actual Windows CI.
**Application:** infoconex/RecordSift, frozen immutable source SHA 8358780829458854a4b0356df5ac5e685f0a34c8.
**Dependency:** Stacked on [EXP-019 draft PR #33](https://github.com/infoconex/dotnet-modernization/pull/33), which itself depends on unmerged EXP-018 PR #32. None of these research PRs have authorization to merge. No RecordSift source or project edits are proposed.

## Why investigate

EXP-019 verified that enabling the existing MSBuild property Deterministic=true for all ten traditional net48 projects yielded five of five **byte-identical DLLs** in a **same-checkout repeated** build but **zero of five** identical DLLs in two separate worktrees built from exactly the same frozen Git commit. All existing API/NUnit/XML/package/installed-consumer gates passed. Changes in MVID, COFF and CodeView/PDB metadata were observed without raw method-IL hash drift.

The C# compiler's deterministic inputs can include full source paths. Microsoft's [Deterministic compiler inputs](https://github.com/dotnet/roslyn/blob/main/docs/compilers/Deterministic%20Inputs.md) and [MSBuild PathMap property](https://learn.microsoft.com/en-us/visualstudio/msbuild/common-msbuild-project-properties) describe path normalization; the C# [compiler advanced options](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/main-compiler-option) document PathMap.

**Question:** Can explicit source-root path mapping make identical-source DLL outputs byte-identical when different checkout locations are used? Can we demonstrate that a deliberately wrong canonical map changes compiled byte evidence, to verify the mapping is not merely an unused MSBuild setting?

## Seven full-gate builds, source never changed

The [Windows runner](../../../../../tooling/pilots/recordsift/EXP-020/run.ps1) and [workflow](../../../../../.github/workflows/validate-recordsift-pathmap-isolation.yml) reuse EXP-019 without modifying its accepted controls:

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

**Results:** Pending actual Windows CI, artifact checksum, and unchanged source provenance. Research only, no merges.
