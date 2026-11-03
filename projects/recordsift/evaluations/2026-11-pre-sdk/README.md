# RecordSift — Pre-SDK modernization discovery

**Date:** November 2, 2026  
**Application repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Canonical application branch:** main  
**Canonical baseline commit:** `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Scope:** discovery and isolated experiments; **no SDK-style conversion and no application main-branch changes**.  
**Overall work status:** original pre-SDK discovery substantially complete; targeted source-only build-target audit now completed; remaining recommendations under research review.

## Evaluation question

Which low-risk improvements deliver value to an existing Windows-only .NET Framework 4.8 / C# 7.3 application **before** converting its ten traditional projects to SDK-style, and how do we demonstrate preserved behavior?

## Navigation

- [Original dated discovery report](discovery-report.md) — preserved source document, with A–I assessment, experiment results, sources and article recommendations.
- [Status](status.md) — activity vs. evidence state and specific open work.
- [Baseline](baseline.md) — actual projects, configuration, tests and compatibility contracts.
- [Findings](findings.md) — independently traceable conclusions, including late follow-up experiments.
- [Roadmap and investigation crosswalk](roadmap.md) — implementation priorities, verification gates and disposition of 34 proposed investigations across six workstreams.
- [Risks](risks.md) — what remains unverified.
- [Decisions](decisions.md) — decisions explicitly proposed, not silently approved.
- [Experiments](experiments/README.md) — individually reproducible investigation notes.
- [Evidence manifest](evidence/manifest.md) — GitHub Actions runs, artifact IDs, experiment branches and immutable image digests.

## Boundary between evaluation and implementation

All experiments were isolated to disposable GitHub Actions workspaces and experimental branches in the application repository. **RecordSift main stayed unchanged.** A dedicated, disposable investigation base, `RecordSift/research/dotnet-modernization`, points to `main` SHA `8358780829458854a4b0356df5ac5e685f0a34c8`. The separately authorized local-test-runner correction was squash-merged only into `release/0.2` ([PR #258](https://github.com/infoconex/RecordSift/pull/258)), not the research baseline or `main`. **Current stakeholder boundary [P-012](decisions.md): research and documentation only; no application implementation, release promotion, or documentation merge to `main` until findings and recommendations are reviewed and separately approved.**

Each future RecordSift evaluation should have its own dated folder and immutable starting SHA.

## Approved methodology-validation pilot scope

**Status:** **Approved November 2, 2026** by the evaluation stakeholder; guided autonomous methodology improvements and targeted isolated investigations may proceed within the documented boundaries. This pilot validates the reusable methodology using the existing pre-SDK RecordSift evidence. Its stakeholder authorization decisions are recorded in [decisions.md](decisions.md), including scope approval P-010. The original technical evaluation and its frozen baseline remain unchanged.

**Objective and outcome:** Make the methodology usable by an AI assistant with no earlier conversation history. Demonstrate that it can discover a .NET application's context, interview only for missing decisions, obtain explicit scope approval, prioritize and execute appropriately isolated investigations, preserve evidence, track work in GitHub, and deliver justified recommendations without assuming implementation authority.

**Included methodology work:** Review the actual entry-point documentation, intake/interview/authorization workflow, area screening, investigation selection, evidence and compatibility standards, GitHub milestone/issue boundaries, documentation responsibilities and duplication, cross-session continuity, AI instruction entry points and completion criteria. Improve existing methodology documentation and templates on the open documentation PR branch; create new files only where a genuine gap requires them.

**Targeted technical work and disposition:** Reuse existing evidence and choose only a real gap. The first approved investigation, [issue #2](https://github.com/infoconex/dotnet-modernization/issues/2), evaluated SDK-only Windows public API, XML documentation, NuGet package generation and clean-consumer gates in [EXP-007](experiments/EXP-007-sdk-only-release-gates.md). It is **complete, partially verified**: build/test/API/XML/package generation and installation passed; the unchanged package-validation and clean-consumer scripts did not. Further technical work (e.g., pinned `global.json` formatter or supported 4.8.1 Framework SDK image) remains **not executed** and is optional only if demonstrably necessary to validate the method. Any permanent application implementation requires separate approval. Create focused issues only for justified in-scope work; keep research issues in `dotnet-modernization`.

**Constraints and exclusions:** Preserve RecordSift `main` at the frozen baseline `8358780829458854a4b0356df5ac5e685f0a34c8`; preserve public APIs, assembly/resource identities and observable behavior. Use only authorized isolated branches, disposable workspaces, and controlled tests. Do not implement permanent application changes, convert projects to SDK style, migrate the runtime, change dependencies, merge PRs, publish packages, deploy, perform destructive cleanup or incur unapproved costs. Escalate unexpected work only when it exceeds approved bounds; preserve negative evidence and note checks not executed.

**Verification:** For changes that could affect compatibility, compare restore, Release build of all ten projects, five NUnit suites (baseline 419 discovered / 418 passed / 0 failed / 1 intentionally skipped), 425 approved API/packaging metadata entries, assembly/resource/XML contracts, package contents and clean consumers as applicable. Record exact source SHAs, tools/OS/image digests, commands, run links, outcomes and omissions. Existing runs may be cited rather than needlessly repeated. The new EXP-007 results and their limitations are in the [experiment record](experiments/EXP-007-sdk-only-release-gates.md); do not infer full release validation from the passed subset.

**Acceptance disposition:** The methodology, evidence and investigation requirements (1)–(3) and (5) were completed on documentation PR #1. Independent testing (4) produced multiple detailed, repository-grounded responses and exposed a corrected roadmap discrepancy, but **no complete same-session candidate response and independently reviewable source/tool record was retained**; the originally required *strict* AC-01–AC-09 proof is **not established**. In [decision P-011](decisions.md) the stakeholder directed an end to repeated retests and accepted that evidence limitation **for this pilot only**. [Issue #3](https://github.com/infoconex/dotnet-modernization/issues/3) retains the observations and is closed as not planned / accepted limitation; it is **not** a documented strict acceptance pass. The general methodology's independent-evidence standard remains intact.

**Completed targeted investigation:** [Issue #2](https://github.com/infoconex/dotnet-modernization/issues/2) produced [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), a **partially verified** result: 419 NUnit tests, XML, API, NuGet package generation and installation passed in the SDK-only environment, while unchanged packaging/consumer validation scripts did not pass. [Acceptance #3](https://github.com/infoconex/dotnet-modernization/issues/3) preserves the independent fresh-context attempts and their closure by documented exception. The reusable first-contact workflow, scope approval, GitHub conventions and continuity rules have been added to [the central methodology](../../../../methodology/evaluation-process.md). Those methodology changes were merged via [PR #1](https://github.com/infoconex/dotnet-modernization/pull/1) into documentation `main` (`903629088e57ad081c512292c7fab4d9c72e4476`).

**Next action (research only):** consolidate documented pre-SDK findings and prepare stakeholder recommendations. The [F-019 project-file audit](findings.md) confirmed no duplicated custom build actions that warrant `Directory.Build.targets`; compiler-property centralization remains a separate [proven research candidate](experiments/EXP-002-shared-properties.md). Keep new findings on a documentation **review branch**, not `main`, until explicit review and approval; do not merge experimental application work.
