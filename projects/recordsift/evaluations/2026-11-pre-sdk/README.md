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
