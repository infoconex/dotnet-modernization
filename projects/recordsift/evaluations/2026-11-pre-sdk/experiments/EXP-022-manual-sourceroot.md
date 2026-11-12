# EXP-022 — manual SourceRoot in traditional net48 before Source Link

**Date:** November 4, 2026. **Status:** Verified scoped positive result on Windows 2022 with original release gates; draft/unmerged.
**Frozen application:** infoconex/RecordSift, SHA 8358780829458854a4b0356df5ac5e685f0a34c8.

**Dependency:** This is a draft stacked on unmerged EXP-021 PR #35, which inherits EXP-020/019/018. Neither this research branch nor RecordSift main may be merged without stakeholder approval.

## Why

EXP-021 conclusively observed that, on actual traditional non-SDK RecordSift net48 projects, setting global Deterministic=true + ContinuousIntegrationBuild=true makes DeterministicSourcePaths evaluate to true, and the build **fails** before compilation with missing top-level SourceRoot items. The original deterministic-only release controls pass. This disproves a blanket claim that old projects do not react to ContinuousIntegrationBuild, but does not show a complete working CI source mapping.

Roslyn's managed C# targets implement InitializeSourceRootMappedPaths and _SetPathMapFromSourceRoots, validating SourceRoot and creating PathMap. Roslyn engineers document a minimal top-level SourceRoot element that need not have a Source Link provider installed. This experiment tests that narrow mechanism before installing NuGet packages.

## Seven actual full-gate builds

First invoke the unchanged EXP-021 runner as **negative controls**: four full original/deterministic-only builds and two deliberately failing CI-property-only builds. Require actual result ci_only_build_blocked, not an invented compatibility pass.

Then create a single **untracked, CI-local** Directory.Build.props file *inside each of two disposable source worktrees*, containing only a top-level SourceRoot item:

    <Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
      <ItemGroup>
        <SourceRoot Include="$(MSBuildThisFileDirectory)" />
      </ItemGroup>
    </Project>

The file remains uncommitted and is not a proposed application change. Traditional MSBuild's normal Directory.Build.props import must pick it up in all five production projects. Invoke the same global Deterministic=true and ContinuousIntegrationBuild=true flags as the EXP-021 failure, **without** installing Source Link or changing DebugType. Query actual SourceRoot items and execute Roslyn _SetPathMapFromSourceRoots to inspect effective PathMap for five projects in both worktrees. Missing root or empty PathMap fails the experiment.

Compile three actual build candidates:
1. Original frozen Git source directory with untracked root provider.
2. Identical frozen Git SHA in a physically different worktree with the same source-root provider.
3. Rebuild the original checkout with the same provider.

Each successful build must pass all ten Release projects, original **425-entry** compiled API gate, **419 NUnit (418 pass, zero fail, one skipped)** across five independent suites, five XML documentation gates, local unpublished NuGet 0.1.0 packaging, installed clean net48 consumer and Getting Started samples. Capture PE SHA-256/MVID/COFF/CodeView/raw IL for all five DLLs in each build. Require all five logical compatibility components to match the historical original baseline. Source revision and tracked source must remain unchanged. Analyze exact byte results as observations: **do not predeclare that source-root injection must produce byte identity**.

## Interpretive limits and approval

Even if source-root mapping causes byte-identical DLLs across directories, **it is not equivalent to Source Link**. No Git URL, source checksum resolution, debugger stepping, Windows PDB Source Link data, NuGet package build asset, private dependency, or source package publishing is tested. This only isolates one missing dependency from EXP-021.

All added props are temporary runner files and are not pushed to RecordSift. Retain source/path map and JSON/gates/NUnit evidence, not DLL/PDB/nupkg bytes. Repository main remains unchanged.

## Verified experimental result

[Successful Windows 2022 run 41916205685](https://github.com/infoconex/dotnet-modernization/actions/runs/41916205685) on research SHA `91b7a8185c1451b16f7857d84fb0ebcab08a8494`, with [artifact 13365900022](https://github.com/infoconex/dotnet-modernization/actions/runs/41916205685/artifacts/13365900022), digest SHA-256 `004265de1972a9ade335ac900cc2c27d82c56e44b9e081d9537d1d73fb95cd50`, 30-day retention.

The script first reproduced the **EXP-021 CI-only compilation failure** caused by missing `SourceRoot` while the four original full-gate deterministic controls passed. It then supplied the one-item, temporary `Directory.Build.props` root, evaluated **ten** actual project/worktree computed path mappings (five production projects, two distinct worktrees), and compiled **three** real Release solution variants from the same frozen Git SHA. Every candidate passed the unchanged 425-entry API gate; five NUnit suites (419 discovered, 418 passed, zero failed, 1 skipped); five XML documentation checks; unpublished local NuGet 0.1.0 package; clean installed net48 consumer and Getting Started samples; and five matched logical compatibility categories. No tracked RecordSift source was modified.

| Real compiled PE comparison | Exact DLL byte-identical hashes | Changed raw method IL records |
| --- | ---: | ---: |
| Two identical frozen Git source worktrees with different physical directory paths, same manually provided SourceRoot root | **5/5** | 0/5 |
| Repeat build from same physical source directory | **5/5** | 0/5 |

The original negative-control tests remain evidence of what **does not** work: `Deterministic=true + ContinuousIntegrationBuild=true` without a top-level SourceRoot **fails**. With the one SourceRoot item, existing Roslyn/MSBuild targets compute an effective `PathMap` and both different-checkout and same-checkout builds produce byte-identical DLLs for these concrete inputs.

**Precise conclusion:** The Source Link *provider package* is **not a prerequisite for the Roslyn deterministic source-path mapping mechanism** on this traditional net48 baseline. A manually provided SourceRoot is sufficient for the tested workflow. This does not demonstrate Source Link URL mapping, Windows PDB Source Link records, debugger step-into, tracked-source checksums, cross-machine hermeticity or archive-byte reproducibility. A reusable central props file may be a future configuration candidate, but no production adoption is authorized.

**Next:** [issue #37 — Source Link provider and Windows PDB study](https://github.com/infoconex/dotnet-modernization/issues/37). Inspect actual pinned packages.config build assets and SourceRoot/source URL metadata, separately verify Windows PDBs and consumers, and do not conflate symbol packaging with Source Link.

