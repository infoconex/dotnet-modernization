# EXP-023A — Source Link package-version and build-asset audit (no execution)

**Assessment:** November 4, 2026. **Status:** CI evidence pending.
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

**Live evidence:** Pending actual Windows and Ubuntu CI.
