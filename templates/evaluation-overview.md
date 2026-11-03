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

## Baseline

Link to restore/build/full-test/API/resource/package results and environment inventory.

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
