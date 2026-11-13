# Article evidence map — Performing .NET technical discovery with RecordSift

**Status:** Working outline only; **not** a publication-ready article or execution proof.  
**Target site:** [coding.infoconex.com](https://coding.infoconex.com/)  
**Series:** Staying Current with .NET  
**Preceding methodology article (draft PR #42):** [How to Establish a Technical Baseline for a .NET Application](https://github.com/infoconex/coding-blog/blob/draft/dotnet-modernization-introduction/post/2026/11/12/how-to-establish-a-technical-baseline-for-a-dotnet-application/index.md)  
**Runbook:** [Native-first discovery](../methodology/technical-discovery-runbook.md)  
**Worked application evidence:** [RecordSift November 2026 evaluation](../projects/recordsift/evaluations/2026-11-technical-baseline/README.md)

## Intended article promise

Show a real .NET application's technical discovery **as it happened**: the native commands chosen, why they apply, captured output, mistakes/limitations, and the resulting technical baseline. Keep the article engaging and readable; the full instructions, filled-in baseline (once discovery has been performed), and supporting evidence remain in `dotnet-modernization`.

**Suggested working title:** "Documenting a .NET Application: A Step-by-Step Technical Discovery of RecordSift"

## Proposed narrative and proof requirements

| Article section | Discovery steps | Required actual evidence before writing conclusions |
|---|---|---|
| Why start with source identity? | DISC-001 | Exact user-run Git commands/outputs, revision and dirty-state disposition |
| What projects and solution exist? | DISC-002–003 | Actual paths, solution listing and declared format/frameworks; distinguish source from CLI inspection |
| What configuration is really in effect? | DISC-004–006 | Tool/host version inventory, applicable MSBuild evaluated properties (if supported), imported/config files and gaps |
| What are the dependency and restore requirements? | DISC-007–008 | Real dependency declarations, native NuGet/SDK output and documented side effects; no fabricated success |
| Can we build and test the current code? | DISC-009–010 | Real command scope, results, exit codes, test assembly inclusion, pass/fail/skip counts |
| How does the application ship and prove compatibility? | DISC-011–012 | CI definitions vs exact executed runs, packaging and compatibility evidence |
| What did the baseline establish? | DISC-013–014 | Links to completed baseline, manifest, gaps and reproducibility instructions |

## Editorial rules

1. **Start writing progressively, but do not publish an outcome before it is observed.** An article may describe the intended command as a planned next step; observed outputs, counts and findings require execution evidence.
2. Use **selected** native command/output excerpts; link long logs and multi-project tables to the canonical evaluation documents. Do not duplicate the entire 14-step runbook.
3. State toolchain and project-format limitations alongside a command; do not imply that a Windows/traditional-net48 result applies to all .NET projects.
4. Explain failed or blocked commands and why they matter. Do not silently replace a failed invocation or infer modernized compatibility from a passing build.
5. Link the frozen RecordSift SHA and individual `EV-NNN` items. Distinguish historical research from the current walkthrough.
6. Keep modernization recommendations out of the discovery narrative; they belong to a later assessment article.
7. The public article draft, hero image and SEO metadata belong in `infoconex/coding-blog` on a separate draft PR. This file is an **evidence-to-article map**, not a second publication copy.

## Writing progress

- **Current:** source-only preflight and runbook authored. No new manual command transcripts yet. The draft methodology article already explains why a baseline matters; the companion should focus on what was actually done.
- **Next:** capture owner-run DISC-001, cite verified output, then draft the first real walkthrough section.
- **Publication status:** not authorized; do not create or merge a production article based on a planned result.
