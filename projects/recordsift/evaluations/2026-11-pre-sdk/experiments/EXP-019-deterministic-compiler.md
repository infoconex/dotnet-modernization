# EXP-019 — explicit deterministic compiler property on traditional net48

**Date:** November 4, 2026. **Status:** Verified for the tested Windows Release builds and scoped compatibility contracts; draft research PR #33 unmerged.
**Frozen application:** infoconex/RecordSift at immutable main commit 8358780829458854a4b0356df5ac5e685f0a34c8.
**Dependency:** [EXP-018 draft PR #32](https://github.com/infoconex/dotnet-modernization/pull/32). This experiment is stacked on the **unmerged EXP-018 research branch** to reuse its managed PE reader. The research dependency does not authorize either merge or a production application change.

## Background and question

[EXP-017](https://github.com/infoconex/dotnet-modernization/pull/30) discovered that all five DLLs have different bytes across independently built copies of the **same frozen source**. EXP-018 established differences in MVID, COFF timestamp and debug-directory/PDB metadata while raw method-body IL hashes remained unchanged, including a repeat built in the **same source directory**. The five production traditional net48 Release projects evaluated DebugType=pdbonly and Optimize=true, but Deterministic and PathMap properties were empty; empty does not establish the compiler's actual defaults.

**Question:** Does setting an explicit global MSBuild Deterministic=true property make the five production DLL files byte-identical across independent builds in different directories and repeats in the same directory? What impact, if any, appears in the original selected compatibility contracts?

## Controls and independent source verification

The [Windows research script](../../../../../tooling/pilots/recordsift/EXP-019/run.ps1) and [workflow](../../../../../.github/workflows/validate-recordsift-deterministic-isolation.yml) perform **four** fully validated, real ten-project Release builds without modifying any source/project files:

1. **Historical baseline** — original source checkout, no compiler property override.
2. **Opt-in A** — same checkout, command-line MSBuild global property /p:Deterministic=true.
3. **Opt-in B** — independent detached worktree at **exactly the same frozen Git SHA/tree**, with the identical property override.
4. **Opt-in A repeat** — rebuild again under the original directory with the identical property override.

Each build must independently pass RecordSift's original **425-entry compiled API** gate, **419 NUnit tests (418 pass, 0 failed, 1 skipped)**, all five XML documentation checks, unpublished local NuGet package validation and independent net48 installed consumer and examples. All five selected logical compatibility categories must match between the historical baseline and each opted-in build. Git SHA and unchanged tracked source are independently checked before and after.

The runner records effective evaluated Release Deterministic settings for all five projects, both baseline and overridden. Explicit values must evaluate to true; the original source's unassigned value is recorded, not invented. These MSBuild properties are not independent final compiler invocation evidence.

## Actual compiled evidence

Reuse [EXP-018's generic metadata-only reader](../../../../../tooling/pe-provenance/README.md) and [generic three-snapshot comparator](../../../../../tooling/validators/pe_variation.py). Capture SHA-256 of whole DLL bytes, MVID, COFF stamp, CodeView debug records (full PDB paths hashed), and per-method raw IL bytes indexed by metadata token. Compare the first opt-in build against both the different-directory and same-directory opted-in builds. Separately compare historical-default against the first opted-in build, and preserve the exact observed difference rather than assuming it must match.

Both byte matches and mismatches are valid experimental observations. Reject missing/invalid evidence, missing assemblies, incomplete source provenance, failed original gates, or unexpected logical compatibility differences. Do not upload DLLs, PDBs or NuGet archives. Emit only JSON and original NUnit evidence with 30-day retention.

## Limits and review

Only the deterministic property is explicitly altered, **not** PathMap, DebugType, target framework, packages.config, project style or NuGet dependencies. A match is not proof of security, behavioral or environmental hermeticity; a mismatch is not automatically a regression. Tool version, compiler arguments, timestamps, source path, build environment and PDB factors may affect exact bytes; a separate scoped investigation will be needed for path mapping or actual C# command-line capture. Do not recommend a production change until the actual Windows test and all release gates pass.

Review through architecture/source provenance, C#/MSBuild compilation, NUnit/consumer compatibility, supply-chain, reusable tooling and technical documentation perspectives. These are internal analytical lenses, not outside independent signoff.

## Verified Windows results — scoped compiler-property experiment

**[GitHub Actions run 41903901066](https://github.com/infoconex/dotnet-modernization/actions/runs/41903901066) passed** on research head 692a1d5e67fb213cb4816622e3640f4e2023d381. [Retained evidence artifact 13359826842](https://github.com/infoconex/dotnet-modernization/actions/runs/41903901066/artifacts/13359826842), SHA-256 digest ec3fe5324f235872c465b5a0b1929d368b75bb78a26dae25b031e9bd27c6d57f, 30-day retention. The evidence includes source SHA/tree and actual per-assembly PE SHA-256, MVID, COFF/debug and method IL hashes (not assembly/package bytes). The frozen RecordSift Git source in all four builds was 8358780829458854a4b0356df5ac5e685f0a34c8. No source/project file was changed.

| Exact PE comparison (all same Git source SHA) | Identical DLL byte hashes | MVID/COFF/debug differences | Raw method IL token changes |
| --- | ---: | ---: | ---: |
| Historical unmodified baseline vs first explicitly deterministic build | **0/5** | 5/5 changed | 0/5 |
| First explicit deterministic build vs another worktree's identical-source explicit deterministic build | **0/5** | 5/5 changed | 0/5 |
| First explicit deterministic build vs **same-directory** explicit deterministic rebuild | **5/5** | **0/5 changed** | 0/5 |

The original/opted-in MSBuild Release Deterministic setting was evaluated for five production projects in each mode: the original setting was observed separately, and each explicit override evaluated to **true**. The experiment did **not** capture the complete C# compiler command line; distinguish effective MSBuild property evaluation from an independently validated compiler switch.

For each of the four separately restored and rebuilt ten-project Release solutions, original application gates were **passed**: **425 compiled public API/metadata baseline entries**, **419 NUnit test discoveries (418 passed, 0 failed, 1 skipped)**, five XML documentation outputs, unpublished NuGet 0.1.0 packaging, and separately installed net48 clean consumer plus examples. The five selected logical compatibility components **matched** between default baseline and *each* opted-in build. The independently read 5 actual compiled DLLs per build provide the byte evidence; no binary or NuGet package file was uploaded or published.

**What this establishes:** For this source, build tools and runner, an explicit global Deterministic=true property **yielded exact repeat DLL bytes when rebuilding in the same source path**. It did **not** yield identical DLL bytes when the same source was compiled at another filesystem path. The observed raw method-body IL hashes remained equal throughout. This is not an application defect or a reason to merge a compiler setting into RecordSift.

**What it does not establish:** This experiment did not prove hermetic compilation, compiler argv, cross-run repeatability, portable-source paths, stable package archive bytes, signed artifact identities, unexamined PE metadata equivalence or runtime compatibility outside tested consumers. Source-path differences are a plausible input but **not yet proven as the cause**. Do not silently add PathMap or alternate PDB settings to this one-property research result.

**Recommendation:** A separately scoped subsequent experiment should test a conditional, explicitly normalized C# source PathMap with Deterministic=true on two disposable worktrees, plus negative controls (without mapping and intentionally wrong mapping). Validate all original application gates again; retain toolchain/source-path observations without exposing secrets. This recommendation is for **further research only**, not production adoption.

**Review status:** Complete scoped experiment evidence. The draft PR is stacked on still-unmerged EXP-018 PR #32; no merge to modernization main or RecordSift is authorized.

