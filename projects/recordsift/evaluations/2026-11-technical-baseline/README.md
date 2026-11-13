# RecordSift — Native-first technical baseline discovery

**Status:** Draft, manual discovery preparation; no local commands or builds performed as part of this new exercise.  
**Application:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Selected source ref:** `main`, observed 2026-11-12  
**Frozen source commit:** [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004)  
**Discovery opened:** 2026-11-12  
**Required evaluation host:** **Windows** (RecordSift is Windows-only; host version/build and architecture not yet verified)  
**Runbook:** [Technical discovery](../../../../methodology/technical-discovery-runbook.md)  
**Reusable template:** [Full discovery report](../../../../templates/application-baseline.md)  
**Verification approach:** User executes supported native commands one at a time; assistant records facts, limitations, results and article-relevant findings.

## Purpose and boundaries

**Objective:** validate that a portable, documented discovery method can produce a traceable technical baseline using RecordSift as the worked example. This is **not** a new modernization assessment or application implementation.

**Platform boundary:** perform the entire RecordSift discovery on Windows, starting with DISC-001 tool/OS preflight. Do not substitute Linux, macOS or WSL as equivalent verification. Cross-platform exploration would be a separate explicitly scoped assessment.

**Proposed scope for owner-led manual execution:** source identity; solution/project and MSBuild configuration; central settings; NuGet dependencies; toolchain inventory; existing build/test entry points; approved manual restore/build/test verification; CI, runtime, package, and compatibility evidence; synthesis of a dated baseline.

**Authorized preparation:** documentation drafting and read-only inspection of publicly available repository contents. The user requested a hands-on, native-command-first walkthrough and will operate local commands. **Before state-changing execution** (restore/build/test, CI triggers, package operations), confirm the specific environment, side effects and current step with the operator. No new experiment, workflow, application edit, release, deployment, branch merge or publication is authorized by this document.

**Existing evidence:** The [2026-11 pre-SDK evaluation](../2026-11-pre-sdk/README.md) covers an earlier immutable RecordSift commit and a different modernization question. It may guide discovery, but old test/build outcomes cannot be relabeled as results from this frozen source revision.

## Working documents

- [Discovery report](baseline.md) — the single record of actual tool versions, commands, collected findings, and results; currently limited to source-inspected preflight.
- [Evidence manifest](evidence/manifest.md) — immutable GitHub source links now; local/CI outputs to be added **only when collected**.
- [Reusable runbook](../../../../methodology/technical-discovery-runbook.md) — exact portable procedures and their applicability/side-effect conditions.
- [Article evidence map](../../../../articles/recordsift-technical-discovery-outline.md) — candidate narrative, not proof or publication-ready copy.

## Initial source-only preflight — 2026-11-12

The application repository's `main` HEAD was inspected through GitHub at the frozen SHA. The tracked tree contains `RecordSift.sln`, **ten project files** (five under `src/` and five under `tests/`), a root `NuGet.Config`, root `.editorconfig`, seven tracked `packages.config` files, and eight `.github/workflows/` definitions. These are **source-inspection findings**; they do not establish a local checkout state, tool versions, successful restore, MSBuild-evaluated properties, or current test outcomes. Detailed paths appear in [the baseline](baseline.md); [EV-001 and EV-002](evidence/manifest.md) identify provenance.

This is not a claim that missing repository-wide files have no equivalents in parent directories, user-level configuration, installed tools or SDK defaults.

## Approval and progress

**Stakeholder instruction (2026-11-12):** develop detailed reusable discovery documentation; operator manually executes native SDK, NuGet, MSBuild and other commands; capture artifacts and write a worked article as evidence accumulates; consider reporting scripts only after understanding manual outputs.

**Research/implementation separation:** no change to RecordSift source, project files or its application main branch. This documentation remains on its own review PR until approved.

**Next action:** operator follows **DISC-001** in the [step-by-step guide](../../../../methodology/technical-discovery-runbook.md): verify Windows/tool versions, then create a dated, clean RecordSift checkout at commit `1809d06c0fade59e4769d16e0f8eaf10fa426004`. **No local commands have been executed or verified.** The assistant fills in the [discovery report](baseline.md) from the actual output before moving to DISC-002.
