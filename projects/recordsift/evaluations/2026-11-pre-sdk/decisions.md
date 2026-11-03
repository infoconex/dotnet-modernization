# RecordSift evaluation decisions

The modernization choices below are **proposals**, not approved application changes. The separately listed pilot stakeholder decisions authorize a bounded evaluation process, not production implementation.

| ID | Proposed choice | Disposition | Reason / verification |
|---|---|---|---|
| D-001 | Correct the local test runner to include all five NUnit assemblies. | Recommend first | Close a proven safety gap; rerun 419 tests and CI. |
| D-002 | Add minimal root Directory.Build.props with shared LangVersion=7.3 and conditional default where overrides must remain possible. | Recommend after baseline | Isolated POC passed build/tests/API/package checks; no early import required. |
| D-003 | Do **not** add a synthetic Directory.Build.targets. | Not recommended currently | Imports work but no meaningful behavior has been identified to centralize. |
| D-004 | Preserve TargetFrameworkVersion in project files until raw-XML public-API verifier assumptions are removed. | Defer | Avoid false compatibility failures. |
| D-005 | Evaluate a documented SDK-only Windows developer build path. | Optional, proven feasible | Tool independence is real for compilation and NUnit; full release-gate support still unverified. |
| D-006 | Do not convert packages.config to PackageReference or add Directory.Packages.props in pre-SDK discovery. | Defer to SDK migration | Separate dependency and packaging compatibility changes from baseline-preserving configuration work. |
| D-007 | Add global.json only if formatter/CI consistency benefits outweigh SDK provisioning burden. | Optional pending verification | Selection works; actual formatter behavior under a pin remains untested. |
| D-008 | Do not modify MSBuild import ordering just to use shared properties. | Reject based on experiment | Early Common.props import produced MSB3107; minimal props centralization passed without it. |

The technical proposals above become **approved for implementation** only with separate explicit authorization, an application-repository issue/PR, an owner, date, and verification evidence.

## Approved pilot stakeholder decisions

**Recorded:** November 2, 2026. **Approver:** evaluation stakeholder (repository owner, via interactive interview). These decisions govern the **RecordSift methodology-validation pilot** and should not be assumed for other applications. This concise record preserves outcomes and authorization boundaries, not the full interview transcript.

| ID | Topic | Approved decision / boundary |
|---|---|---|
| P-001 | AI autonomy | **Guided autonomous:** inspect and interview, agree scope, then independently investigate and document within that scope; request separate authorization for application implementation. |
| P-002 | Pilot scope | **Methodology validation with targeted investigations:** test documentation and workflow; investigate genuine evidence gaps rather than repeat completed experiments. |
| P-003 | Experiments | **Preauthorize isolated experiments** within approved evaluation scope, including temporary application branches/workflows and clean environments. Do not modify or merge into RecordSift `main`, publish artifacts, or treat experimental changes as authorized permanent implementation. Preserve traceable evidence. |
| P-004 | Methodology improvements | **Implement on existing documentation PR branch** `docs/initial-structure-recordsift` and verify; do **not merge PR #1** without separate authorization. Favor improving existing files over unnecessary new documents. |
| P-005 | Acceptance | **Independent fresh-context validation required:** a new assistant should be able to initiate and conduct an evaluation using repository instructions without prior chat history. This test remains to be performed; the present pilot is not by itself final acceptance. |
| P-006 | Compatibility | **Strict backward compatibility:** preserve public APIs, assembly and resource identities, and observable behavior. Potential breaks may be tested in isolation but not accepted or implemented without explicit authorization. |
| P-007 | Unexpected findings | **Investigate autonomously within authorization:** isolate failures, collect evidence, and continue unrelated work. Escalate scope expansion, permanent changes, compatibility regressions, destructive actions, or unapproved costs. |
| P-008 | Decision documentation | **Concise evaluation decision record:** preserve decisions, rationale where relevant, approver/date and boundaries here. Do not require a full interview transcript or an issue for every question; keep stakeholder authorization distinct from technical proposals. |
| P-009 | Scope authorization | **Explicit consolidated scope approval is required** before autonomous technical investigations. After inspection and interview, present objectives, inclusions/exclusions, risk boundaries, selected work, evidence standards and acceptance criteria; record stakeholder approval in this evaluation. Extensions require additional approval. Prior interview decisions do not silently approve the pending consolidated pilot scope. |
| P-010 | Consolidated pilot scope approval | **Approved November 2, 2026 by the evaluation stakeholder** in this conversation: the proposed methodology-validation pilot scope in [README.md](README.md) is authorized for guided autonomous execution. This approval permits bounded methodology updates and targeted isolated investigations; it does **not** authorize application implementation, merging, publishing, or scope expansion. |

**Unchanged boundary:** modernization implementation belongs to `infoconex/RecordSift` and is not preapproved by these pilot decisions. No application production-code changes, merges, release or package publication are authorized.
