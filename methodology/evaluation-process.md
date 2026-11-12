# Modernization evaluation lifecycle

## Start here: first-contact protocol

An assistant with **no prior conversation context** must be able to start from the root README, this procedure, the application repository, and any existing dated evaluation. Do not rely on remembered stakeholder choices, prior chats, or undocumented approvals.

**Order matters for a new evaluation:** inspect repositories and existing evidence → identify missing stakeholder decisions → interview adaptively → present consolidated scope → obtain **explicit approval** → establish/reuse baseline → select investigations → run authorized isolated experiments if justified → assess, document and recommend. Technical discovery from source inspection is allowed before scope approval; **new experiments and investigation issues are not** unless separately authorized.

**Resuming an existing evaluation is different:** inspect the evaluation overview, recorded stakeholder decisions and approval, current status, experiment evidence and relevant GitHub issues **before** asking questions or proposing new work. If the existing approval still covers the requested action, reuse it; do not re-interview, reapprove unchanged scope, recreate work, or treat an already completed investigation as pending. If approval cannot be verified or a materially different goal is requested, present only the missing decision or scope amendment. Validate live repository branches/SHAs separately from the immutable historical baseline. Do not assume an unmerged documentation PR is part of the default branch.

## 1. Inspect, interview, and approve scope

### Inspect before asking

1. Confirm the owning repository, current default branch/full SHA, access level, project inventory, existing CI/build/test commands and requirements/consumer constraints. Follow repository-specific instructions and check relevant existing evaluations.
2. Identify existing authoritative requirements, acceptance scenarios, architecture, test traceability and compatibility evidence where available. Compare material claims with the current source revision; flag missing, conflicting or historical documentation. Answer repository-evidenced questions before interviewing stakeholders.
3. Review the [investigation catalog](investigation-catalog.md) as a relevance screen, **not** a list of mandatory work. Note relevant unknowns and exclusions.
4. Explain the known baseline, available evidence, and unresolved human decisions before starting the interview.

### Adaptive stakeholder interview

Ask **one consequential question at a time** and explain the recommendation, alternatives and implications. Use supported interactive single-choice controls where practical; otherwise provide clearly numbered options. Always allow **Other / custom answer**. Avoid collecting information already verified from repositories or earlier answers. A small evaluation may require few questions; do not force a standard questionnaire.

Resolve only material decisions: objectives and drivers, desired modernization horizon, compatibility invariants, platforms/consumers, critical risk tolerance, AI autonomy, scope exclusions, authorization for isolation/experiments/implementation, evidence expectations, GitHub tracking, and completion/acceptance criteria. Distinguish **discovering** existing constraints from **asking** stakeholders to choose them. Follow up only if an answer changes what is permitted or how success will be measured.

### Explicit consolidated scope approval — mandatory checkpoint

Write a concise scope proposal in the evaluation overview ([template](../templates/evaluation-overview.md)) covering:

- Application owner/repository/branch and frozen baseline SHA; objective, measurable outputs and intended modernization stage.
- Included areas/investigations and explicit exclusions or deferrals, with prioritization and existing evidence to reuse.
- Required compatibility contracts, accepted risk, verification gates and criteria for stopping/escalation.
- Levels of autonomy; exactly which experiments, branches, workflows, documentation updates and issue actions are authorized.
- Explicit **non-authorizations**: permanent source changes, merges, publishing, deployments and costs unless approved.
- Evidence and GitHub tracking conventions; completion criteria and any independent fresh-context acceptance test.

Present the proposal to the stakeholder and request explicit approval or revision **before starting investigations**. A preferred interview answer is not itself final approval; record the approval decision, date, approver and linked scope. A later scope expansion requires a recorded amendment and approval. Continue the already-approved portion of work where safe.

### Approval and escalation rules

- Default without authorization: **read-only discovery and proposal**.
- Guided autonomous (when explicitly selected): after scope approval, investigate and record evidence independently within approved boundaries. Isolated branch/workflow modifications are allowed **only** if covered by experiment authorization.
- Stop the affected work and seek authorization for scope expansion, permanent application changes, backward-compatibility breaks, destructive cleanup, unapproved spending, merge/release or publication. Continue unrelated in-scope work.
- An experiment may demonstrate a regression; **accepting or shipping** it is not authorized. Never interpret a finding or recommendation as approval.

**Output:** repository profile, focused stakeholder decisions, **approved or verified existing** evaluation scope, stated authorization boundary and current next action. Preserve concise decisions, not necessarily the whole interview transcript.

## 2. Establish the baseline

Establish **two complementary records for the unchanged application** before modernization experiments:

1. **Source-backed discovery:** At an immutable full Git SHA, inventory the application's identity and versions, Git repository and directory structure, existing configuration files (including modernization-related files that are absent), all relevant `.sln`/`.slnx` and project files, configurations, direct/dependency graph, build inputs, scripts, CI, packaging and runtime requirements.
2. **Executed compatibility verification:** Record the actual host/toolchain and commands, restore/build results, all discovered/passed/failed/skipped tests, relevant public APIs/assembly/resources/XML contracts, package/consumer results, and links to logs/artifacts. State any unexecuted or failing gate explicitly.

**Behavioral discovery before opportunity assessment:** Establish a proportionate understanding of who or what invokes the application, its primary capabilities and application-facing entry points, representative successful workflows, expected failure/boundary behavior, inputs/outputs, component and data paths, business rules and externally observable contracts. Start from existing authoritative specifications and traceability, then trace representative paths through implementation and tests. For undocumented applications, record source-backed observations and unresolved questions rather than treating inferred intent as an approved requirement. Flag contradictory or stale documentation, distinguish inspection from executed verification, and link to the authoritative evidence and material gaps from the evaluation overview. Reuse existing application records rather than reproducing their requirements, scenarios or test matrices. Do not require exhaustive workflow mapping or unrelated runtime experiments merely to complete discovery.

**Use the [application baseline template](../templates/application-baseline.md)** for a substantial application and keep the inventory in a single `baseline.md`. Smaller evaluations can summarize equivalent relevant facts in the [evaluation overview](../templates/evaluation-overview.md). The template owns the detailed field checklist; **do not duplicate it in the methodology or repeat facts across baseline sections**. A baseline should describe what exists, not propose implementation.

**Baseline field-design rule:** Before representing each field, identify its **applicable scope**, **material variations**, **source of truth**, and **verification status**. Check the [baseline variation guide](baseline-variation-guide.md) for possibilities beyond the pilot application's configuration, then document only the facts observed in the evaluated application. Add relevant columns, rows or focused tables when values vary; do not turn the guide into mandatory empty fields or copy its hypothetical examples into the baseline.

**Provenance:** Distinguish source-declared values, actual MSBuild-evaluated values, installed tools, mutable hosting metadata and executed behavior. Absence of an optional file is not a reason to create it. Reuse adequate existing verification from the same exact source revision and relevant environment; a baseline with known failures may still be a valid, documented starting point. Preserve evidence gaps and avoid unnecessary reruns.

**Output:** Source-verified inventory plus traceable reproducible compatibility evidence, with an explicit baseline disposition.

## 3. Reproduce the environment

Inventory OS/build, SDK/runtime/targeting packs, compiler, MSBuild implementation, NuGet, test runner, environment variables, container image and digest where applicable. Label tools as preinstalled or explicitly added.

**Output:** environment record and executable commands.

## 4. Discover opportunities

Identify actual duplication, workflow defects, tool assumptions, modernization tools, and technical constraints. Revisit the [investigation catalog](investigation-catalog.md) as evidence changes the priorities; document applicability, assessment state and deferrals, not merely a list of technologies. Use the [repository configuration and tooling assessment](repository-configuration.md) to consider relevant central .NET configuration mechanisms, including existing files, effective imports, and intentional omissions. Record applicability and assessment state without assuming each mechanism should be introduced. Classify benefits as **immediate**, **future migration**, or **likely redundant**.

**Output:** candidate opportunities, hypotheses, priorities.

## 5. Experiment in isolation

Prefer disposable workspaces or branch-specific workflows. Capture commands, environment, raw results, control comparisons, and limitations. Preserve application compatibility unless the experiment explicitly explores a deviation.

**Output:** one experiment record per meaningful hypothesis.

## 6. Assess and decide

Rank candidates by benefit, risk, effort, independent implementability, tool dependencies, reversibility, SDK preparation value, longevity, and educational value. Distinguish **what was observed** from **what we intend to do**. Record rejected and deferred options.

**Output:** findings, decision records, roadmap.

## 7. Implement only approved changes

Use the **application's own repository**. Create focused, reversible change sets. Run baseline and post-change verification gates; validate on the actual CI platform. Do not infer implementation from a discovery experiment.

**Output:** issues/PRs, compatibility evidence, implementation status.

## 8. Capture reusable learning

Promote broadly applicable lessons into research, linking the exact application experiment that supports each claim. Date findings with tool-version sensitivity. Map publication candidates to evidence, but draft articles separately.

**Output:** cross-project research and article planning links.

## Status model

Track **work state** independently from **verification outcome**:

- Work: not started, in progress, complete, blocked, deferred.
- Evidence: verified, partially verified, unverified, failed hypothesis, not executed.

A successfully completed experiment can have a failed hypothesis; a verified experiment does not imply an implementation was approved.


## GitHub work tracking and ownership

A **milestone** represents **one application and one agreed modernization goal**, e.g. `RecordSift — Pre-SDK Modernization Evaluation`. Create only approved goals, not a milestone for every investigation. Where tooling cannot create/attach milestones, record that limitation and keep the issue linked to the evaluation; never claim a milestone was created.

Meaningful investigations are tracked as focused issues in the **methodology/evaluation repository** (in this project, `infoconex/dotnet-modernization`), not automatically in the application repository. An issue specifies objective, motivating evidence gap, relevant application/evaluation and files, hypotheses/dependencies, authorized experiment boundary, expected verification, findings/disposition and permanent documentation links. Do not create an issue for every catalog row or interview answer. Use sub-issues only for substantial decomposition. Keep the issue updated as evidence emerges; issue closure reflects a supported disposition, **not** an automatic code change.

**Application implementation issues and PRs belong in the application repository**, linked to investigation findings and created only under explicit implementation authorization. Discovery experiments may use preauthorized temporary application branches, but do not merge or publish them. Record exact baseline and experiment SHAs.

## Lean documentation ownership

Each evaluation requires only a navigable **overview** with approved scope, current status/next step, baseline/evidence links, decisions/approvals and a traceable outcome. Add specialized documents **when they earn a distinct responsibility**, not as empty placeholders:

- `baseline.md` for substantial immutable source/environment/compatibility records.
- `experiments/` and `evidence/` for multiple reproducible experiments or sizeable retained diagnostics.
- `findings.md` for many evidence-backed observations; `decisions.md` when authorization/technical dispositions need a durable audit trail.
- `status.md` only for active multi-workstream tracking; `risks.md` for nontrivial unresolved risks; `roadmap.md` for a meaningful sequence of independent recommended changes.
- A preserved historical discovery report is an archival source, **not** an additional live status authority.

Use **one authoritative home** for each fact or procedure; link instead of repeating detailed status, findings or rules across files. Prefer a short overview for simple evaluations and retain older evidence rather than overwriting history.

## Pilot self-audit and cross-session continuation

During an evaluation note actual process failures: unclear entry point, missed/duplicated interview question, ambiguity in approval, unexecuted verification, conflicting documents, unsupported GitHub operation, or a task that depends on hidden chat history. Improve the **central procedure** when possible; AI entry points should link here rather than restate it.

At session boundaries update the overview with the repository/branch/full SHA, approved scope and approvals, issue IDs, experiment artifacts/outcomes, unresolved gates, and **one concrete next action**. A later assistant should verify live repository state first and avoid repeating completed experiments. Never infer success from a workflow's overall color. If the *next action is the independent acceptance run itself*, the evaluating assistant should complete the blind response and let the reviewer record its result, rather than recommend starting the same test again.

## Evaluation completion and independent acceptance

An evaluation may close when the agreed questions have evidence-backed dispositions (including justified deferrals/no-change), compatibility or environment checks are clearly marked pass/fail/not executed, and recommendations are prioritized with implementation authorization separate. Record outstanding risks and owner decisions. **Completing evaluation does not require performing an upgrade.**

When the stakeholder requires **fresh-context acceptance**, an independent AI session must start solely from repository instructions and the application reference, then demonstrate correct inspection, adaptive interview, explicit scope approval, investigation/evidence tracking and escalation boundaries. Log the test procedure, observed passes/failures and correction loop. **This live pilot cannot mark its own fresh-context validation as passed.**
