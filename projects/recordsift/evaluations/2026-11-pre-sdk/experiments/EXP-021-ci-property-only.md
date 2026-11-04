# EXP-021 — Does ContinuousIntegrationBuild alone normalize paths in traditional net48 projects?

**Assessment:** November 4, 2026. **Status:** Pending actual Windows CI evidence.
**Application:** infoconex/RecordSift, immutable SHA 8358780829458854a4b0356df5ac5e685f0a34c8.
**Research branch dependency:** Stacked on unmerged EXP-020 draft PR #34, and ultimately unmerged EXP-019 PR #33 / EXP-018 PR #32. The other research PRs #28 and #30 remain independent and unmerged. None authorize application or research main merges.

## Why this experiment is necessary

EXP-019 established that explicitly setting global MSBuild Deterministic=true yielded five of five byte-identical DLLs rebuilt in the **same** source directory, but zero of five when identical Git source was compiled at separate filesystem paths.

EXP-020 then verified five of five byte-identical DLLs across separate source-root paths **when both paths were explicitly mapped to the same virtual root**, with five of five DLLs changing in a deliberately mismatched mapping control. Every variant retained the historical RecordSift API, NUnit, XML, local package and clean-consumer gates.

A separate suggested configuration enables ContinuousIntegrationBuild=true and assumes the modern Roslyn/MSBuild target graph generates an effective PathMap. This hypothesis is **not** established simply by recognizing the property or by looking at SDK-style documentation. The traditional projects import Microsoft.CSharp.targets and have no Source Link package installed. This experiment tests *only the CI property* with no new NuGet or source imports.

## Controls and candidate designs

The [EXP-021 runner](../../../../../tooling/pilots/recordsift/EXP-021/run.ps1) and [read-only workflow](../../../../../.github/workflows/validate-recordsift-ci-property-only.yml) first run **the unchanged EXP-019 control**:

1. Historical frozen-source Release build, with no opt-in determinism.
2. Frozen-source deterministic build in original checkout, only /p:Deterministic=true.
3. Identical-source deterministic build in detached different-path worktree, no PathMap.
4. Repeat deterministic build in original path.

Each must pass the original compiled API (425 entries), all five NUnit suites (419 total/418 pass/0 fail/1 skipped), XML docs, local NuGet 0.1.0 and separate installed net48 consumer. Original controls must reproduce the expected same-worktree identity and different-worktree byte mismatch.

Without changing source/project files, then evaluate effective actual Release MSBuild values for Deterministic, ContinuousIntegrationBuild, DeterministicSourcePaths and PathMap **in each of five production projects, for two source worktrees, under both property modes**: 80 property cells. Record empty values rather than inventing defaults. Explicit CI mode must evaluate ContinuousIntegrationBuild=true and Deterministic=true.

Candidate builds:

5. Original source worktree, /p:Deterministic=true /p:ContinuousIntegrationBuild=true, no explicit PathMap or Source Link package.
6. Independent identical-Git-SHA worktree, same two properties, no Source Link package.
7. If both candidate builds pass, repeat same source-path candidate build, both properties.

If either candidate fails to build (for example, if a source-root target rejects missing SourceRoot metadata), record the actual compiler/MSBuild diagnostics and source state and classify **ci_only_build_blocked**. The CI research job can succeed in capturing a genuine non-usable setting without ever mislabeling the missing acceptance tests or binary results as passed.

If candidates compile, require the complete original 425 API, 419 NUnit, XML, NuGet package and independent clean consumer verification **for every candidate**. Capture all five actual compiled DLL hashes, MVID, COFF, CodeView metadata and raw method IL hashes per build using the inherited read-only PE metadata tool, and compare independent-worktree versus same-path repeat. Compare the five selected logical compatibility categories with original frozen-source baseline. If any gate fails, **the experiment fails**, rather than classifying a change as accepted.

## Interpretation and guardrails

The following outcomes have distinct meanings:

- CI property recognized, no effective deterministic source-path mapping, DLLs still vary: **CI flag alone did not establish cross-path reproducibility** in this traditional project.
- CI property activates source-root mapping but build fails because source-control SourceRoot items are absent: **the flag alone is not a deployable configuration**; the missing SourceRoot integration is a prerequisite to investigate separately.
- Both candidate builds pass and produce matching DLL bytes: promising scoped evidence, **not** proof that Source Link itself works, PDB source retrieval works, all compiler inputs are hermetic, or files match on a different runner.
- Any logical API/test/package/consumer mismatch or missing evidence: failed candidate, not acceptable compatibility.

This experimental branch changes **no RecordSift tracked files**, targets, reference layouts, Source Link packages, PDB format, dependencies, or NuGet packaging scripts. No DLL/PDB/nupkg bytes or raw binlog with sensitive paths are uploaded. GitHub artifacts contain only JSON settings/PE summaries and selected original NUnit/release evidence, retained 30 days.

## Why Source Link is a separate next experiment

Microsoft Roslyn targets define the relationship between Deterministic and ContinuousIntegrationBuild and a DeteministicSourcePaths source-root mapping target. Whether those targets are imported and provided with SourceRoot for this traditional project must be established, not guessed. **Only after this control** should a separate research branch select/pin a verified Source Link package version and attempt conventional packages.config integration, preserving the current Windows Release PDB format first.

Suggested review lenses: MSBuild import/target behavior, compiler inputs and PDB metadata, package restore and dependencies, original release compatibility, source provenance, security and documentation quality. External independent human reviews are not claimed.

**Actual result:** Pending Windows CI and 30-day research artifact. No merges authorized.
