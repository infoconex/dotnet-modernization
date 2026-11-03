# RecordSift — Pre-SDK modernization discovery

**Date:** November 2, 2026  
**Application repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Canonical application branch:** main  
**Canonical baseline commit:** `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Scope:** discovery and isolated experiments; **no SDK-style conversion and no application main-branch changes**.  
**Overall work status:** substantially complete; selected follow-up verification remains.

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

All experiments were isolated to disposable GitHub Actions workspaces and experimental branches in the application repository. **RecordSift main stayed unchanged.** Modernization tasks in the [roadmap](roadmap.md) remain recommendations until separately approved and implemented in RecordSift.

Each future RecordSift evaluation should have its own dated folder and immutable starting SHA.

## Approved methodology-validation pilot scope

**Status:** **Approved November 2, 2026** by the evaluation stakeholder; guided autonomous methodology improvements and targeted isolated investigations may proceed within the documented boundaries. This pilot validates the reusable methodology using the existing pre-SDK RecordSift evidence. Its stakeholder authorization decisions are recorded in [decisions.md](decisions.md), especially P-001–P-009. The original technical evaluation and its frozen baseline remain unchanged.

**Objective and outcome:** Make the methodology usable by an AI assistant with no earlier conversation history. Demonstrate that it can discover a .NET application's context, interview only for missing decisions, obtain explicit scope approval, prioritize and execute appropriately isolated investigations, preserve evidence, track work in GitHub, and deliver justified recommendations without assuming implementation authority.

**Included methodology work:** Review the actual entry-point documentation, intake/interview/authorization workflow, area screening, investigation selection, evidence and compatibility standards, GitHub milestone/issue boundaries, documentation responsibilities and duplication, cross-session continuity, AI instruction entry points and completion criteria. Improve existing methodology documentation and templates on the open documentation PR branch; create new files only where a genuine gap requires them.

**Proposed targeted technical work:** Use existing evidence first, then choose the smallest meaningful unresolved investigation to exercise the method end-to-end. The leading candidate is verifying existing public API, XML documentation, NuGet packaging and clean-consumer gates in the .NET SDK-only Windows environment (currently unexecuted). If useful to validate a separate workflow, evaluate pinned `global.json` with the actual formatter/CI toolchain. Testing the supported .NET Framework 4.8.1 container image is optional and should require a stated benefit. Do not reopen successful experiments merely to generate activity. Create focused issues only for substantial approved work; keep research issues in `dotnet-modernization` and potential implementation issues in RecordSift subject to separate approval.

**Constraints and exclusions:** Preserve RecordSift `main` at the frozen baseline `8358780829458854a4b0356df5ac5e685f0a34c8`; preserve public APIs, assembly/resource identities and observable behavior. Use only authorized isolated branches, disposable workspaces, and controlled tests. Do not implement permanent application changes, convert projects to SDK style, migrate the runtime, change dependencies, merge PRs, publish packages, deploy, perform destructive cleanup or incur unapproved costs. Escalate unexpected work only when it exceeds approved bounds; preserve negative evidence and note checks not executed.

**Verification:** For changes that could affect compatibility, compare restore, Release build of all ten projects, five NUnit suites (historical baseline 419 discovered / 418 passed / 0 failed / 1 intentionally skipped), 425 approved API/packaging metadata entries, assembly/resource/XML contracts, package contents and clean consumers as applicable. Record exact source SHAs, tools/OS/image digests, commands, run links, outcomes and omissions. Existing runs may be cited rather than needlessly repeated. None of these gates is claimed newly executed by this proposal.

**Acceptance:** (1) a consolidated approval is explicitly recorded; (2) necessary methodology improvements are committed to the existing docs PR without merging; (3) at least one meaningful investigation, or a documented no-experiment justification, demonstrates accurate issue/evidence/decision tracking; (4) a separately initiated fresh-context assistant validates the workflow using repository instructions and reports pass/fail against agreed criteria; (5) unresolved gaps and required follow-ups are transparently documented. The fresh-context test is future work, not currently passed.

**Completed targeted investigation:** [Issue #2](https://github.com/infoconex/dotnet-modernization/issues/2) produced [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), a **partially verified** result: 419 NUnit tests, XML, API, NuGet package generation and installation passed in the SDK-only environment, while unchanged packaging/consumer validation scripts did not pass. [Acceptance #3](https://github.com/infoconex/dotnet-modernization/issues/3) tracks the independent fresh-context validation. The reusable first-contact workflow, scope approval, GitHub conventions and continuity rules have been added to [the central methodology](../../../../methodology/evaluation-process.md). These documentation changes are on PR #1, still unmerged.

**Next action:** Conduct the independently tracked fresh-context methodology acceptance test in a separate AI session and use its results to correct any remaining methodology gaps; optionally seek separate approval for RecordSift validation-tool implementation changes. The **independent fresh-context test remains pending**; it cannot be self-certified by this session. Approval does not authorize RecordSift implementation or merging PR #1.
