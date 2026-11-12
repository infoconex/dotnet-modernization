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

## Verified CI execution and observed compatibility

**Verified:** [Windows 2022 workflow 41966519714](https://github.com/infoconex/dotnet-modernization/actions/runs/41966519714) passed at research SHA `8be8bd47621ae40b05ed018ee69d154585eb2a25`, after earlier [failed run 41965940708](https://github.com/infoconex/dotnet-modernization/actions/runs/41965940708) exposed a PowerShell reserved `$IsWindows` variable collision in PDB-check code. The fault was corrected in `9d1bbde6fefe8c9ae121b0936aa9b6ab9616f129` and is **not** a Source Link/compiler compatibility failure.

**Retained artifact** [13388340011](https://github.com/infoconex/dotnet-modernization/actions/runs/41966519714/artifacts/13388340011), ZIP SHA-256 `6457a6de38464aab0d58208bb5777f33116a203ba27bb8446ee76e07a82b1ee1`. The independently downloaded JSON `experiment-report.json` and `candidate-versus-original-compatibility.json` report:

- Original frozen ten-project Release baseline, 425 API, all five NUnit suites (419 total; 418 passed/1 skipped), five XML checks, local 0.1.0 package and clean net48 consumer passed.
- The three manually extracted, hash-pinned tool packages' six props/targets appeared in preprocessed CSV, `InitializeSourceControlInformation` succeeded, the actual compiler diagnostics included `/sourcelink`, and CSV Release rebuilt successfully with `Deterministic=true` + `ContinuousIntegrationBuild=true` while leaving the nine application packages.config entries intact.
- A classic native MSF Windows PDB signature was present. Zero newly introduced CSV Release files; CSV DLL and PDB bytes changed as expected. Tool task DLL import was observed in diagnostic output, but process/module load isolation was **not** directly measured.
- Before candidate release gates, temporary tracked csproj bytes were restored, and the new CSV DLL was copied to **two** NUnit test assembly execution folders. Original candidate API/NUnit/XML/local package/clean consumer gates all passed, with CSV candidate SHA-256 `b857f93fcb371cfeb74663113c330031ea37d8dd9cf2df6bd3ff6fa291dce3f4` unchanged through acceptance. All five logical compatibility categories (api, assemblies, packages, resources, tests) matched the original frozen baseline.

**Precise verdict:** `VERIFIED_MANUAL_CSV_BUILD_AND_RELEASE_COMPATIBILITY` on this Windows runner. Does not establish NuGet Package Manager project installation, transitive dependency safety, actual PDB Source Link stream, URL/checksum, debugger steps, module host isolation or distinct-worktree reproducibility. Keep draft/unmerged.
