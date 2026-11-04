# EXP-022 — manual SourceRoot in traditional net48 before Source Link

**Date:** November 4, 2026. **Status:** Research-only candidate, live Windows CI pending.
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

**Results:** Pending exact Windows run, per-DLL observations and retained artifact.
