# Modernization evaluation lifecycle

## Start here: first-contact protocol

An assistant with **no prior conversation context** must be able to start from the root README, this procedure, the application repository, and any existing dated evaluation. Do not rely on remembered stakeholder choices, prior chats, or undocumented approvals.

**Order matters for a new evaluation:** inspect repositories and existing evidence → identify missing stakeholder decisions → interview adaptively → present consolidated scope → obtain **explicit approval** → establish/reuse baseline → select investigations → run authorized isolated experiments if justified → assess, document and recommend. Technical discovery from source inspection is allowed before scope approval; **new experiments and investigation issues are not** unless separately authorized.

**Resuming an existing evaluation is different:** inspect the evaluation overview, recorded stakeholder decisions and approval, current status, experiment evidence and relevant GitHub issues **before** asking questions or proposing new work. If the existing approval still covers the requested action, reuse it; do not re-interview, reapprove unchanged scope, recreate work, or treat an already completed investigation as pending. If approval cannot be verified or a materially different goal is requested, present only the missing decision or scope amendment. Validate live repository branches/SHAs separately from the immutable historical baseline. Do not assume an unmerged documentation PR is part of the default branch.

## 1. Inspect, interview, and approve scope

### Inspect before asking

1. Confirm the owning repository, current default branch/full SHA, access level, project inventory, existing CI/build/test commands and requirements/consumer constraints. Follow repository-specific instructions and check relevant existing evaluations.
2. Identify which questions can be answered from code, documentation, recorded decisions or previous evidence. Do not ask these again.
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

The baseline has **two required complementary parts**, not just a successful build. Begin with **read-only, source-verified repository/application/solution discovery**, then capture **executed, reproducible compatibility verification** on the unchanged baseline. Record the exact source revision and distinguish *declared configuration*, *evaluated configuration*, *observed execution* and *unverified assumptions*. A known failing application may still have a useful baseline: do not silently turn gaps or pre-existing failures into a green result.

### A. Discover repository, application, solution and project state

Inspect the actual repository at a **full pinned commit SHA**, not a default-branch URL that may move. Adapt this inventory to the application type; collect relevant fields or mark them **not applicable / unavailable / not verified** rather than inventing values.

1. **Repository identity and topology:** Git host/provider and repository type (single application, monorepo, multi-solution, library, service or other), owner/name, visibility where accessible, browser/HTTPS clone/SSH clone URLs, default branch, full baseline SHA, license, relevant ownership and existing instructions. Differentiate current host metadata from the historical immutable source snapshot. Record meaningful nested repositories, submodules, shared projects or external source references.
2. **Application and release identity:** purpose and consumers, workload type (library, API, web, desktop, service, CLI, etc.), runtime/OS/architecture constraints, application/assembly/file/informational/product/package versions and their **individual source locations**; published releases are not assumed to match the tracked packaging source. Identify distinct apps in a multi-app repository.
3. **Directory/source structure:** top-level and relevant nested source, test, documentation, packaging, deployment and tooling directories. Inventory repository-contained solutions, projects and projects not included in any solution. Inspect tracked scripts, manifests and generated/ignored file conventions; distinguish source items from generated build output.
4. **Solution inventory (`.sln`/`.slnx` and other supported solution formats):** every solution path, declared format/Visual Studio versions or format-specific metadata where available, projects and project type/GUID/path mapping, solution folders/nesting, solution configurations/platforms and **project ActiveCfg/Build mapping**. Presence of a solution does not imply every repository project is included or built. Do not presume `.slnx` has the same serialized fields as `.sln`.
5. **Project inventory (`.csproj`, `.vbproj`, `.fsproj`, shared/other project kinds):** path/name, project system (traditional vs SDK-style; SDK identifiers and imports), project/output type, project GUID/identity where applicable, `ToolsVersion` where declared, target framework(s), language/version, platform target and build configurations, assembly/root namespace/output paths and version metadata. Capture evaluated build-critical values where raw XML is conditional, imported or overridden, and compare declared solution configuration to project configuration.
6. **Project graph, dependencies and build contracts:** declared project references, shared projects, explicit assembly references/HintPaths, NuGet declarations/sources/lockfiles, effective dependency versions, external tools/feeds/services and target framework support. Identify direct vs transitive dependency information only when independently established. Preserve source/resource globs, linked/generated files, embedded-resource logical names, assembly attributes, analyzer/generator inputs, compiler defines, XML docs, warning policies, pre/post-build events and custom imports/targets **when present**. Watch for dependency cycles, cross-layer/vendor coupling and source-format-dependent validation scripts.
7. **Existing repository/configuration mechanisms:** record relevant files as **present or absent**, including location, purpose and noteworthy settings: `.editorconfig`, `global.json`, `NuGet.Config`, `packages.config`, `Directory.Build.props/targets/rsp`, `Directory.Packages.props`, `Directory.Solution.*`, `packages.lock.json`, `.globalconfig`/`.ruleset`, `.gitattributes`/`.gitignore`, and repository-specific instructions. Also inspect applicable `web.config`, `app.config`, `appsettings*.json`, container/IIS/service/deployment manifests or other host configuration. **Absence is a fact, not a recommendation to create a file.** Machine-wide/imported settings may still exist.
8. **Build, tests, CI/CD, packaging and execution entry points:** documented restore/build/test/package/publish commands; local scripts; relevant workflow files, triggers, branch filters, agent OS, tool installation/provenance, PowerShell/shell assumptions, required feeds/secrets **by name only**, deployment/hosting and artifact identities. Inspect whether all tests/projects are actually executed and if packaging/consumer gates depend on raw file formats, specific paths or compilers.

Keep the inventory **navigable and proportional**: summarize source-backed values in one baseline and link to immutable file paths, detailed inventories or existing evidence. Do not copy entire project XML, private credentials or bulky reports. If the application has no solution file, record that explicitly and inventory standalone projects/entry points instead. Do not rely on one technology's version field to infer another (solution format vs Visual Studio vs MSBuild `ToolsVersion` vs installed compiler vs SDK vs target framework vs C# vs assembly vs NuGet).

### B. Verify unchanged behavior and compatibility

On the same pinned application source, record the actual OS/toolchain, restore and compilation commands, full discovered/passed/failed/skipped tests, API/resource/assembly identities, packaging, clean consumers, supported hosting and other application-specific contracts. Include a documented **independent** run/consumer where feasible, but no separate external reviewer is inherently required. Capture workflow/commit/artifact links and classify each gate as verified, partially verified, failed, blocked, not executed or not applicable. A green build alone is insufficient; executed test counts do **not** measure complete code coverage.

**Reuse rule:** Reuse an adequately verified existing baseline at the **same immutable commit** and compatible relevant environment. Do not rerun successful checks merely to populate an inventory; do not use another commit's green CI result as evidence for the current source without explaining its scope. New experiments compare against the established reference gates.

**Output:** a traceable, readable application **baseline record** containing both source-inventory and verification evidence, with explicit missing fields/limitations. Use the [application baseline template](../templates/application-baseline.md) as the recommended format for substantial evaluations and record the result in one `baseline.md`, or capture the applicable information in the evaluation overview for small ones; do not create mandatory empty secondary files. The [evidence standards](evidence-standards.md) govern actual run provenance. Baseline **facts** belong here; proposed modernization changes belong in later findings/opportunities/experiments.

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
