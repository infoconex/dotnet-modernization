# RecordSift — Pre-SDK modernization discovery

**Date:** November 2, 2026  
**Application repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Canonical application branch:** main  
**Canonical baseline commit:** `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Scope:** discovery and isolated experiments; **no SDK-style conversion and no application main-branch changes**.  
**Overall work status (November 3):** EXP-001–013 assessed; the current consolidated documentation is **draft/unmerged**, with independent implementation and merge approval required.

## Evaluation question

Which low-risk improvements deliver value to an existing Windows-only .NET Framework 4.8 / C# 7.3 application **before** converting its ten traditional projects to SDK-style, and how do we demonstrate preserved behavior?

## Navigation

- [Consolidated research review](review-2026-11-03-consolidated-research.md) — reconciles draft evidence, historical limitations, priority proposals and stakeholder review gates.
- [Original dated discovery report](discovery-report.md) — preserved source document, with A–I assessment, experiment results, sources and article recommendations.
- [Status](status.md) — activity vs. evidence state and specific open work.
- [Baseline](baseline.md) — actual projects, configuration, tests and compatibility contracts.
- [Findings](findings.md) — independently traceable conclusions, including late follow-up experiments.
- [Roadmap and investigation crosswalk](roadmap.md) — implementation priorities, verification gates and disposition of 34 proposed investigations across six workstreams.
- [Risks](risks.md) — what remains unverified.
- [Decisions](decisions.md) — decisions explicitly proposed, not silently approved.
- [Experiments](experiments/README.md) — individually reproducible investigation notes.
- [Evidence manifest](evidence/manifest.md) — GitHub Actions runs, artifact IDs, experiment branches and immutable image digests.
- [EXP-043 retained sanitized reports](evidence/README.md) — RecordSift's five-assembly audit and managed-reader exposure.
- [RecordSift-focused Gate C-N strategy review](reviews/gate-cn-engineering-perspectives-strategy-review-20261106.md) — application modernization recommendation, not production approval.

## Boundary between evaluation and implementation

All experiments were isolated to disposable GitHub Actions workspaces and experimental branches in the application repository. **RecordSift main stayed unchanged.** Modernization tasks in the [roadmap](roadmap.md) remain recommendations until separately approved and implemented in RecordSift.

Each future RecordSift evaluation should have its own dated folder and immutable starting SHA.

## Approved methodology-validation pilot scope

**Status:** **Approved November 2, 2026** by the evaluation stakeholder; guided autonomous methodology improvements and targeted isolated investigations may proceed within the documented boundaries. This pilot validates the reusable methodology using the existing pre-SDK RecordSift evidence. Its stakeholder authorization decisions are recorded in [decisions.md](decisions.md), including scope approval P-010. The original technical evaluation and its frozen baseline remain unchanged.

**Objective and outcome:** Make the methodology usable by an AI assistant with no earlier conversation history. Demonstrate that it can discover a .NET application's context, interview only for missing decisions, obtain explicit scope approval, prioritize and execute appropriately isolated investigations, preserve evidence, track work in GitHub, and deliver justified recommendations without assuming implementation authority.

**Included methodology work (historical pilot scope):** Reviewed entry-point documentation, intake/interview/authorization workflow, area screening, investigation selection, evidence standards, GitHub issue boundaries, cross-session continuity, AI instruction entry points and completion criteria. [Original documentation PR #1](https://github.com/infoconex/dotnet-modernization/pull/1) was **merged November 3**. This completed merge is separate from later research drafts and does not authorize any implementation or research PR merge.

**Targeted technical work and disposition (current):** The first approved targeted investigation, [issue #2](https://github.com/infoconex/dotnet-modernization/issues/2), remains **historically partial** in [EXP-007](experiments/EXP-007-sdk-only-release-gates.md). Later [EXP-009](experiments/EXP-009-sdk-only-release-validation.md) verified the corrected SDK-only positive package/consumer path but not original unmodified scripts or SDK-only negative CS1591. [EXP-008](experiments/EXP-008-pinned-sdk-formatter-build.md) **verified** the actual formatter under SDK pins 10.0.303 and 10.0.403. [EXP-010–013](experiments/README.md) cover WarningLevel, dependency graph, exact-pinned PackageReference and actual CI-coupling controls. The supported Framework SDK 4.8.1 image pull remains **not executed**. No migration or application change is approved.

**Constraints and exclusions:** Preserve RecordSift `main` at the frozen baseline `8358780829458854a4b0356df5ac5e685f0a34c8`; preserve public APIs, assembly/resource identities and observable behavior. Use only authorized isolated branches, disposable workspaces, and controlled tests. Do not implement permanent application changes, convert projects to SDK style, migrate the runtime, change dependencies, merge PRs, publish packages, deploy, perform destructive cleanup or incur unapproved costs. Escalate unexpected work only when it exceeds approved bounds; preserve negative evidence and note checks not executed.

**Verification:** For changes that could affect compatibility, compare restore, Release build of all ten projects, five NUnit suites (baseline 419 discovered / 418 passed / 0 failed / 1 intentionally skipped), 425 approved API/packaging metadata entries, assembly/resource/XML contracts, package contents and clean consumers as applicable. Record exact source SHAs, tools/OS/image digests, commands, run links, outcomes and omissions. Existing runs may be cited rather than needlessly repeated. The [EXP-007 historical partial record](experiments/EXP-007-sdk-only-release-gates.md) and later [EXP-009 corrected positive-path record](experiments/EXP-009-sdk-only-release-validation.md) are **different evidence**; do not equate successful corrected probes with the unchanged release pipeline. PackageReference's 414 compiled API records **do not replace** the 425-entry original API+package-metadata contract without a separately authorized format-aware validator.

**Acceptance disposition:** The methodology, evidence and investigation requirements (1)–(3) and (5) were completed on documentation PR #1. Independent testing (4) produced multiple detailed, repository-grounded responses and exposed a corrected roadmap discrepancy, but **no complete same-session candidate response and independently reviewable source/tool record was retained**; the originally required *strict* AC-01–AC-09 proof is **not established**. In [decision P-011](decisions.md) the stakeholder directed an end to repeated retests and accepted that evidence limitation **for this pilot only**. [Issue #3](https://github.com/infoconex/dotnet-modernization/issues/3) retains the observations and is closed as not planned / accepted limitation; it is **not** a documented strict acceptance pass. The general methodology's independent-evidence standard remains intact.

**Completed targeted investigation:** [Issue #2](https://github.com/infoconex/dotnet-modernization/issues/2) produced [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), a **partially verified** result: 419 NUnit tests, XML, API, NuGet package generation and installation passed in the SDK-only environment, while unchanged packaging/consumer validation scripts did not pass. [Acceptance #3](https://github.com/infoconex/dotnet-modernization/issues/3) preserves the independent fresh-context attempts and their closure by documented exception. The reusable first-contact workflow, scope approval, GitHub conventions and continuity rules have been added to [the central methodology](../../../../methodology/evaluation-process.md). The methodology documentation from [PR #1](https://github.com/infoconex/dotnet-modernization/pull/1) was **merged on November 3, 2026**; later research and this consolidation remain **draft/unmerged**. Historical P-004/P-011 references to prior no-merge authorization preserve the decision at that time; [P-012](decisions.md) is the current research-only boundary.

**Next action:** Review the consolidated research [report](review-2026-11-03-consolidated-research.md) and the **docs-only integration draft**. This branch combines later experiment documents and resolves conflicts for review, **not** permission to merge it into `dotnet-modernization/main`. RecordSift's previous [runner correction PR #258](https://github.com/infoconex/RecordSift/pull/258) is already merged into `release/0.2` but not application `main`; do not duplicate it. The first *new* optional application candidate is minimal conditional `LangVersion=7.3` centralization, subject to **separate implementation approval**.
