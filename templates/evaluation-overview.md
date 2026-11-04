# <Application> — <Evaluation title>

**Application repository:** <owner/repository>  
**Baseline branch:** <branch>  
**Baseline commit:** <full SHA>  
**Date opened:** <YYYY-MM-DD>  
**Phase:** <intake/discovery/decision/implementation/closed>  
**Owner:** <owner>  

## Objective

What questions must this evaluation answer? Distinguish discovery from approved changes.

## Scope and constraints

Describe supported frameworks/platforms, consumers, included areas, excluded migrations, compatibility invariants, risk tolerance and relevant existing evidence. **Do not start new technical investigations merely because this template exists.**

## Stakeholder decisions and scope authorization

**Scope state:** proposed / approved / amendment pending  
**Approval:** approver, date and approval reference, or **not yet approved**  
**AI autonomy:** supervised / guided autonomous / other  
**Experiment authorization:** permitted isolated environments, temporary branches and workflow changes; prohibited actions  
**Implementation / merge / release authorization:** explicitly authorized or **not authorized**

Record concise decisions and rationale or link to a dedicated decision record *only when needed*. An interview preference is not approval of this consolidated scope. For complete procedure see [the evaluation process](../methodology/evaluation-process.md#1-inspect-interview-and-approve-scope).

## Approved investigation boundary

List the few prioritized investigation objectives, rationale, expected evidence/verification, dependencies, exclusions and conditions requiring scope amendment. Distinguish **already verified** from proposed experiments. Do not create empty issue or experiment files.

## Verified, reproducible application baseline

**Baseline source:** <repository owner/name and immutable full commit SHA>  
**Inventory checked:** <date and source reference>  
**Compatibility evidence:** <run URLs/commit/artifact identifiers, or explicitly not executed>  
**Recorded in:** <link to baseline.md or inline section; no empty documents>  
**Baseline status:** <source inventory complete/partial; behavior verified/partial/blocked/not executed>

Follow [establish the baseline](../methodology/evaluation-process.md#2-establish-the-baseline). Complete both **source-backed discovery** and **executed verification** before relying on this baseline for modernization decisions. For a small application, concise tables/links in this overview may be sufficient; for a larger one, link to an application-specific `baseline.md`.

### A. Repository, application, solution and configuration inventory

Record these categories from the **unchanged source**. Include the source location and explicitly mark unavailable/irrelevant data; do **not** turn optional mechanisms into mandatory adoption recommendations.

| Inventory subject | Required information where applicable | Source reference / verification gap |
|---|---|---|
| Repository identity | Git provider, host type, owner/name, public/private scope, browser URL, HTTPS and SSH clone URLs, default branch, exact baseline SHA, license | <source or observed host metadata/date> |
| Application identity | Name, purpose, workload type, consumers, runtime/OS/architecture, published/application/package/assembly/file versions **separately** | <README/manifests/version sources> |
| Directory structure | Actual project/source/test/docs/script/packaging/CI/deployment layout, generated/ignored directories, submodules | <pinned Git tree/paths> |
| Solution(s) | Count and paths of `.sln`/`.slnx` (or none); format and version metadata where applicable, project membership/type/GUID, folders, configurations/platforms and project build mappings; projects outside solutions | <pinned solution files> |
| Project(s) | Path/name, SDK-style or traditional, target framework(s), language/version, output/project type, `ToolsVersion` if relevant, platform/configurations, assembly/root namespace/identity/version and output paths | <pinned project files; evaluated settings if available> |
| Dependency graph | Direct project references, explicit assembly/HintPath, NuGet declarations and **effective** versions, lockfiles, external tool/feeds/services, architecture edges | <projects, restores and inventory evidence> |
| Build-sensitive metadata | Imported `.props`/`.targets`, compiler defines/warnings/optimization, linked/globbed/embedded/generated resources, output/assembly attributes, pre/post-build steps and packaging contracts | <project files, source/verification> |
| Existing config files | **Present/absent**, locations and consequential values for relevant `Directory.Build.*`, `Directory.Solution.*`, `Directory.Packages.props`, `global.json`, `.editorconfig`, `NuGet.Config`, `packages.config`, `packages.lock.json`, `.globalconfig`, Git/config and application/host-specific files | <pinned repository tree; distinguish inherited/host settings> |
| CI, build and release entry points | Restore/build/test/package/publish commands; scripts/workflows, triggers, OS/agent, tools/shells, package consumers, deployment/hosting and external prerequisites | <specific scripts/workflows> |

For multi-project repositories, include a **project inventory table or a referenced machine-readable inventory** showing each relevant project's output type, framework(s), SDK/project format, version identity and direct references. Record inconsistencies without modifying the source. Avoid duplicating raw project XML or dumping unnecessary metadata.

### B. Reproducible compatibility checks

| Gate | Exact command / environment | Evidence and outcome |
|---|---|---|
| Restore and complete solution/project build | <OS, SDK/MSBuild, package sources and command> | <run/commit, verified/partial/failed/not executed> |
| Automated tests | <all assemblies/test frameworks/filters> | <discovered, passed, failed, skipped; run> |
| Public contracts | <API signatures, assembly/version/resources/serialization and docs as applicable> | <comparison evidence or not applicable> |
| Packaging and external consumers | <NuGet/app artifacts, dependencies, clean consumer or deployment> | <run/known limitation> |
| App-specific behavior | <runtime/platform, integration, security, performance or operational gate when relevant> | <evidence or gap> |

**Provenance rule:** Keep **declared project/solution versions**, **evaluated MSBuild/compiler settings**, **actual runtime/tool versions** and **executed evidence** distinct. Record missing tests/uncertainty honestly. Do not require an independent human reviewer; independent execution means evidence from unchanged source in a reproducible environment. Reuse verified existing evidence at the same source revision without rerunning sufficient checks.

**Baseline disposition:** <accepted verified reference / accepted with named gaps / additional evidence needed>.

## Modernization area screening

Use the [investigation catalog](../methodology/investigation-catalog.md) to identify relevant opportunities and explicit exclusions. This is a *screening*, not a requirement to evaluate all catalog areas. Add only meaningful rows; keep applicability, assessment state, evidence, decision and implementation distinct.

| Area | Applicability | Assessment state | Reason / current evidence / follow-up |
|---|---|---|---|
| <relevant area> | Applicable / Not applicable / Undetermined | Evaluated / Deferred / Not yet assessed | <why; link to evidence or next investigation> |

## Repository configuration and tooling

Use the [repository configuration assessment](../methodology/repository-configuration.md) to identify *relevant* central files and tool settings. Record only meaningful existing configurations, opportunities or omissions; do not create placeholder entries for every possible file. Keep applicability and assessment state distinct from verification outcomes.

| File or mechanism | Applicability | Assessment state | Observation or open question | Evidence / proposed action |
|---|---|---|---|---|
| <relevant mechanism> | Applicable / Not applicable / Undetermined | Evaluated / Deferred / Not yet assessed | <observed behavior or question> | <finding, evidence link, or no change> |

## Opportunities

Summarize candidate improvements, benefit, effort, risk and migration relevance.

## Experiments and evidence

| ID | Hypothesis | Evidence outcome | Run/artifact |
|---|---|---|---|
| EXP-001 | <hypothesis> | Not executed | <reference> |

## Findings and decisions

Keep observed findings separate from accepted/rejected/deferred decisions.

## Risks and unanswered questions

List explicit gaps and assumptions.

## Recommended implementation sequence

For every proposed change: prerequisite, verification gates, rollback plan.

## Pilot and process observations

Record only demonstrated workflow friction, missing instructions, conflicting authority or handoff gaps; link to methodology improvements instead of repeating whole procedures.

## Completion and fresh-context acceptance

Specify stakeholder-approved completion criteria. If an independent new-session validation is required, record its procedure, status and actual evidence; do not claim completion from the same context that created the methodology.

## Next action

One specific highest-value activity, with link to the issue or experiment. If scope is pending, the next action is **obtain explicit stakeholder approval**, not start the investigation.
