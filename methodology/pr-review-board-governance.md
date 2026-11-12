# Pull-request review board and delegated merge policy

**Stakeholder directive:** November 6, 2026 — “For every PR, put together a board of reviewers that are applicable and if you get consensus on approval of the PR then go ahead and merge if it does not require me to also review.” This is a **standing conditional authorization**, not a blanket approval of individual code, release operations or existing PRs with unresolved approval boundaries.

**Scope:** PRs arising from the `dotnet-modernization` research and RecordSift pilot. Repo-specific instructions, GitHub rulesets, CODEOWNERS, required human approvals, existing frozen baselines, release/publishing boundaries and explicit previous conditions still apply. Do not apply automatically to unrelated repositories.

## 1. Assemble a board for each PR

Choose applicable perspectives; do not imply one AI's role-based review is independently staffed:

| Perspective | Required when | Review responsibility |
| --- | --- | --- |
| Architecture and compatibility | Application code, project formats, dependencies, APIs or design | Inward dependencies, contractual parity, impact and minimal scope. |
| Build/toolchain | MSBuild, compiler, CI, release automation, tooling | Evaluated configuration, build behavior, rollback, tool and path selection. |
| Quality/test | Every implementation PR | Positive/negative and regression gates, exact-head runs, limits of test coverage. |
| Security/supply chain | Every dependency, build trust, consumer data, parser, credential, provenance or release change | Pinned inputs, vulnerability scans, trust boundaries, accidental permissions. |
| Release/governance | **Every** PR | Authorization, PR target branch, protections, publication risk, evidence, no bypass. |
| Documentation/usability | Public docs, workflow, developer UX, errors | Coherence, accurate claims, user-facing behavior and maintenance cost. |

Default to at least the directly relevant technical reviewers plus Quality and Release/Governance; include Security on security-sensitive changes. **These are review lenses applied by this assistant, not independent agents or named human reviewers.** If a human or organization requires actual independent approval, request it; an AI perspective cannot satisfy GitHub's human approval rule.

## 2. Decision on each exact candidate commit

The board must inspect the **actual patch**, issue/approval scope, source and relevant build/run logs, exact head SHA and base SHA, all GitHub review requests/submissions, unresolved threads, CI, branch rules/rulesets, and release risks. Record per-role:

- **APPROVE** with concrete evidence and residual risks;
- **CHANGES REQUIRED** with an actionable issue; or
- **ABSTAIN / INSUFFICIENT EVIDENCE** when outside scope or blocked.

**Consensus means every applicable perspective approves, with no unresolved blocking finding or absent required evidence.** It is not the mere absence of objections. Do not fabricate independent persons or votes, or equate a green workflow with a release signoff.

If any reviewer perspective objects or evidence is unavailable, do **not** merge. Gather targeted evidence, fix the change, or escalate the specific blocker. Reevaluate against **the new exact head**.

## 3. Delegated merges: allow only bounded, non-owner-review-required cases

An assistant can recommend and perform a **squash merge** on a previously authorized application integration branch (e.g., RecordSift `release/0.2`) **only** when all of these hold:

1. User's standing delegation applies to this PR and the underlying implementation was in scope.
2. Role-based board consensus is documented with relevant evidence and exact candidate SHA; no required human reviewer/team/code-owner is missing; no unresolved requested changes.
3. GitHub checks, policies, branch protection/rulesets and PR mergeability are satisfied. Do not disable protections, force bypass, or misuse reviewer APIs to self-certify independent approval.
4. Only reviewed changes exist; compare exact full patch to the authorized scope and confirm no unreviewed updates.
5. The operation is a **non-destructive squash merge into the permitted integration branch**, not release promotion, protected main change, tags, package publication or deployment.
6. Reconfirm the target head has not moved unexpectedly, and use GitHub's expected-head-SHA merge guard; verify actual merge result and preserve audit references.

**Escalate to the stakeholder rather than auto-merge:** any PR requiring their review under repo instructions/policy; promotion into application `main` or releases; published packages, deployments; API/runtime/behavior breaks, incompatible dependency changes, security exceptions, lockfile/version surprises, loss of regression coverage, high-risk external effects; architecture changes outside approved scope; unresolved technical disagreement or uncertain authorization. A zero-review-count GitHub setting **alone** does not waive such stakeholder requirements. A documentation PR into research main is subject to its own separate previously recorded authorization/PR scope.

## 4. Board report for audit

Record the exact PR number, base and head SHAs, short change summary, applicable board roles, each conclusion + evidence, CI run IDs and negative controls, unresolved uncertainty, GitHub human review/rule status, merge permission decision, and SHA of resulting squash merge if one occurs.

Do not use GitHub APPROVE events from the author's identity as simulated independent reviews. Prefer a clearly labeled board assessment in an issue/PR comment; retain the fact if no human reviewer participated.

## 5. Specific existing constraints

- RecordSift `main` remains on the accepted frozen baseline pending separately authorized release promotion.
- Research Gate C original `UNSATISFIED`, production native C-N `NOT_AUTHORIZED`, Source Link production `HOLD`. No research-only result silently approves operational use.
- Research PRs previously designated draft/unmerged, including stacked Gate C-N branches, remain unmerged until individually cleared under applicable scope and explicit approval records. Do not bulk-merge historical PRs simply because this policy now exists.
- PRs requiring a true independent human security/release reviewer cannot be cleared by this assistant's single-model board.
