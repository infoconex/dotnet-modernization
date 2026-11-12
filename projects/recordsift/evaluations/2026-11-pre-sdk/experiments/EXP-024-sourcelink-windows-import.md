# EXP-024 — Disposable traditional net48 Source Link import, Git information and Windows PDB format

**Scope:** Research-only execution on Windows 2022. Frozen application: `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`. Stacked on draft EXP-023B PR #39; no application commits, production merges, or package publication.

## Question

Can three current, SHA-pinned Source Link build-task packages be imported **manually** into the **single** traditional `src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj` without changing its nine-entry `packages.config`, upgrading existing runtime references, or changing Release `DebugType=pdbonly`?

The EXP-023B metadata-only gate detected two dependency conflicts with conventional NuGet install. A build-task-only manual simulation is a strictly different hypothesis. It does **not** establish that Visual Studio NuGet Package Manager can install an equivalent set safely.

## Design

1. Checkout immutable RecordSift with full Git history and no persisted credentials. Verify exact SHA and clean worktree.
2. Restore original dependencies, rebuild original ten-project solution, and run unchanged EXP-014 release acceptance: 425 API, all 419 NUnit (418/1), five XML docs, local nupkg, net48 clean consumer.
3. Download exactly three NuGet packages (GitHub, Common, Build.Tasks.Git 10.0.403), check actual archive SHA-256 against EXP-023A, extract into the disposable `packages/` folder. **Do not install System.IO.Hashing** or change application package declarations.
4. Preserve existing csproj and packages.config bytes. Insert only temporary, explicit props-before-`Microsoft.CSharp.targets` and targets-after-`Microsoft.CSharp.targets`, using the real project-relative `..\\..\\packages` root. Fail on absent imports. Check `/pp`.
5. Attempt real `InitializeSourceControlInformation` target and CSV-only Release rebuild with `Deterministic=true`, `ContinuousIntegrationBuild=true`, `BuildProjectReferences=false` (to avoid unrelated original projects' missing SourceRoot blocker). Record whether compiler used `/sourcelink`, tool DLLs appeared in diagnostic task evidence, and PDB has native Windows MSF signature. Source Link JSON/URL checks remain a separate structural validation stage.
6. Compare added or changed CSV output files against the original baseline; fail if build-task/runtime DLLs unexpectedly newly appear. Restore the original tracked project bytes even on failure and verify Git clean. Keep detailed diagnostics local; retain JSON only. Do not upload binlogs, assemblies, PDBs, raw compilation paths, packages or nupkg.

## Interpretation

**Only a successful Windows CI execution** proves the scoped observed outcomes. A failed build is an important result and must be preserved. A green workflow does **not** prove actual `packages.config` installation, runtime isolation, Source Link URL/checksum/PDB correctness, deterministic byte identity, clean consumer compatibility *after* provider integration, or true submodule handling. Those require separate acceptance.

Use [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37) for provenance and future stages. Review [NuGet import semantics](https://learn.microsoft.com/en-us/nuget/concepts/msbuild-props-and-targets), [Source Link implementation](https://github.com/dotnet/sourcelink) and [Roslyn compiler SourceLink switch](https://github.com/dotnet/roslyn/blob/main/docs/compilers/CSharp/CommandLine.md).
