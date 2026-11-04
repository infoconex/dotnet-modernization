# EXP-023A — Source Link package-version and build-asset audit (no execution)

**Assessment:** November 4, 2026. **Status:** Verified read-only NuGet archive and MSBuild asset metadata on Windows 2022 and Ubuntu 24.04. Source Link integration/building remains untested.
**Application:** infoconex/RecordSift at immutable source 8358780829458854a4b0356df5ac5e685f0a34c8.
**Review boundary:** Research draft stacked on unmerged EXP-022 PR #36 (and EXP-021/020/019/018). No application or research main merges authorized.

## Motivation

EXP-021 verified that in traditional net48 projects, ContinuousIntegrationBuild=true activates DeterministicSourcePaths=true, but without SourceRoot the legacy build fails. EXP-022 then supplied only an untracked top-level SourceRoot and verified full original release/consumer acceptance and 5/5 byte-identical DLLs across different physical worktrees **without Source Link**.

Thus Source Link is **not required for deterministic compilation or Roslyn path normalization** in the tested project. Source Link remains independently valuable for Git commit URLs, source checksums, PDB content and debugging. A recommendation to use Microsoft.SourceLink.GitHub 1.1.1 because it dates to the traditional-project era is a hypothesis, not compatibility evidence.

## Exact pinned package candidates and safety

The [read-only CI workflow](../../../../../.github/workflows/validate-sourcelink-package-audit.yml) retrieves archives from the official nuget.org v3 flat-container API without installing packages, importing MSBuild targets or executing task DLLs.

| Versions | Archive inventory | Execution policy |
| --- | --- | --- |
| GitHub, Common and Build.Tasks.Git **1.1.1** | Historical packages from 2021 | Metadata only |
| GitHub, Common and Build.Tasks.Git **8.0.0** | Compare older documented build/import structure | **Never execute**: Microsoft.Build.Tasks.Git 8.0.0 is affected by 2026 CVE-2026-62900 |
| GitHub, Common and Build.Tasks.Git **10.0.403** | Current stable comparison, with net472 dependency group in provider | Metadata only until full import/security review |
| System.IO.Hashing **10.0.14** | Provider-declared dependency in 10.0.403 | Metadata only |

Sources: https://github.com/dotnet/sourcelink ; https://www.nuget.org/packages/Microsoft.SourceLink.GitHub/1.1.1 ; https://www.nuget.org/packages/Microsoft.SourceLink.GitHub/10.0.403 ; https://github.com/advisories/GHSA-23fw-v26w-5fgq

The [reusable stdlib auditor](../../../../../tooling/validators/nuget_build_assets.py) validates actual archive SHA-256, expected ID/version, single embedded nuspec, ZIP path and size bounds, declared dependency names/version ranges, build/buildTransitive props/targets, and tools/lib/runtimes asset names. [Negative fixtures](../../../../../tooling/validators/tests/test_nuget_build_assets.py) reject malformed XML, unsafe paths, symlinks and duplicate archive members. Windows and Ubuntu use the same fixture suite and real package inputs. Upload versioned JSON metadata only, not NuGet package bytes. Keep 30-day research artifact.

## Interpretation and strict constraints

- A props/targets file inside a package does **not** prove the traditional packages.config installer adds its imports or loads dependent task assemblies. A distinct disposable project installation test must validate actual imports and target execution.
- A declared dependency group does **not** prove complete NuGet restore closure or safety; inspect chosen versions and advisories again before execution.
- A package with no lib assets does **not** prove it has zero effects on runtime output, consumer package, or debuggability.
- Microsoft's official README supports classic .NET Framework and Windows PDBs, but Gemini's specific srcsrv stream implementation claim requires direct Windows PDB inspection. Do not alter current Release DebugType=pdbonly in this phase.
- No Source Link PDB URL, source checksum, debugger step-through, detached HEAD, shallow Git or full package archive reproducibility is established by inspecting package ZIPs.
- Different physical source paths, nested submodules and external source files are distinct scenarios requiring separate controls.
- No RecordSift tracked edits, no NuGet publishes, no research main merges.

## Next decision

Select a specific pinned provider build **only after** reviewing actual archive import targets, dependencies and vulnerability advisories. Then implement EXP-023B in disposable Windows source worktrees with authentic packages.config NuGet installation, inspected evaluated import graph, Git-commit mapping, unchanged Windows PDB, and full existing API/NUnit/XML/pack/consumer gates.

## Actual pinned package evidence and cross-platform verification

**[GitHub Actions run 41934257221](https://github.com/infoconex/dotnet-modernization/actions/runs/41934257221)** completed successfully at research SHA `3ecab947caeac5c3c1aeb2bfc0084f63d8e3d751` for **both Windows 2022 and Ubuntu 24.04**. The complete reusable-toolkit fixture suite also passed on both platforms in [run 41934257233](https://github.com/infoconex/dotnet-modernization/actions/runs/41934257233).

The run retrieved and **read, never loaded/executed**, ten actual NuGet package archives from the official v3 service. Exact archive metadata, SHA-256, declared dependency ranges, NuGet build/buildTransitive import candidates, and tools/lib/runtimes file inventory were retained as 30-day JSON evidence:

- [Windows artifact 13372349230](https://github.com/infoconex/dotnet-modernization/actions/runs/41934257221/artifacts/13372349230): archive digest `d348d91d99286dab8d015079b21d7854585b3cbab2337986829747d13d27ed5f`.
- [Ubuntu artifact 13372358247](https://github.com/infoconex/dotnet-modernization/actions/runs/41934257221/artifacts/13372358247): archive digest `26dfc4fa606305a2f4c361538d4b05eac313a95c807049979f27ab80a87998ab`.

The same downloaded package identities had **identical NuGet archive SHA-256 values on Windows and Ubuntu**. Important per-package observations from the real CI logs:

| Package | Version | MSBuild props/targets candidates in archive | Direct nuspec dependency declarations |
| --- | --- | ---: | ---: |
| Microsoft.SourceLink.GitHub | 1.1.1 | 4 | 2 |
| Microsoft.SourceLink.GitHub | 8.0.0 | 4 | 2 |
| Microsoft.SourceLink.GitHub | 10.0.403 | 4 | **6** |
| Microsoft.SourceLink.Common | 1.1.1 / 8.0.0 / 10.0.403 | 5 / 5 / 7 | 0 / 0 / 0 |
| Microsoft.Build.Tasks.Git | 1.1.1 / 8.0.0 / 10.0.403 | 4 / 4 / 6 | 0 / 0 / **2** |
| System.IO.Hashing | 10.0.14 | 2 | **4** |

Those counts reflect **nuspec dependency declarations across target-framework groups**, not necessarily six distinct required package identities. This phase does not choose target framework assets or resolve a complete NuGet closure.

Actual NuGet SHA-256 examples: Microsoft.SourceLink.GitHub 1.1.1 = `de173dca6e5178e369d34aee08a8a8fca6b58185e8fe30e5507b5f2b5c193e25`, Microsoft.SourceLink.GitHub 10.0.403 = `9c3252f8cbe1547bf8c12b7c65a7bc28985bab2d598ff97c13e0104c22d80cd5`, and Microsoft.Build.Tasks.Git 8.0.0 = `bd7ebf90f8a3f2f340bbc7fbaebbc71e13eb369876d0872e7e6ac1819371a500`. The 8.0.0 version was **never imported or executed**, consistent with the cited 2026 vulnerability advisory.

### Preserved negative controls and runner issue

- [Initial run 41934081986](https://github.com/infoconex/dotnet-modernization/actions/runs/41934081986): Ubuntu passed; Windows **failed** a synthetic raw-backslash ZIP safety fixture because Python ZIP handling normalizes separators on Windows. The initial test did not construct the intended unsafe raw bytes on Windows.
- [Intermediate run 41934222130](https://github.com/infoconex/dotnet-modernization/actions/runs/41934222130): Windows test still failed because the fixture had not yet been corrected. The auditor was enhanced to validate raw ZIP central-directory filename bytes, rather than trusting platform-normalized member paths.
- [Successful run 41934257221](https://github.com/infoconex/dotnet-modernization/actions/runs/41934257221): the fixture now patches raw ZIP path bytes directly, so both runner platforms reject them and pass all 11 targeted tests. The complete reusable-toolkit CI subsequently passed on both platforms.

### Interpretation / acceptance boundary

**Verified:** Pinned versions and exact archive bytes, names of available NuGet targets/import candidates, declared dependency ranges, basic archive safety, and cross-platform reuse of the generic auditor.

**Not verified:** Actual packages.config NuGet install/import behavior in RecordSift, MSBuild target execution, source-root initialization, C# /sourcelink compiler options, Windows PDB payload, source URL/checksum correctness, debugger stepping, complete dependency-closure safety, ABI compatibility, or any app build/consumer gate. This evidence does **not** authorize choosing either 1.1.1 or 10.0.403 for production. Next is the separately authorized, disposable integration phase of [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).

**No RecordSift source modification or merge, no package publication or executable Source Link package load.**
