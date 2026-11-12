# `<Application>` — Technical discovery execution log

**Application and repository:** `<owner/repo>`  
**Evaluation:** `<path to dated evaluation README>`  
**Frozen source ref and full SHA:** `<branch or tag>` / `<40-character SHA>`  
**Discovery dates:** `<YYYY-MM-DD>`  
**Operator and host:** `<person/runner, OS and architecture; omit private user details>`  
**Runbook:** [Native-first technical discovery](../methodology/technical-discovery-runbook.md)  
**Baseline record:** `<path to baseline.md>`  
**Evidence manifest:** `<path to evidence/manifest.md when evidence exists>`

This template is a **working record**, not an executable script. Create a row for each applicable step and a detailed record only when the step is attempted or a material gap needs documenting. The project baseline holds facts; the execution log holds **how they were established**. Link raw evidence instead of duplicating it.

## Execution summary

| Step | Work status | Evidence method | Evidence outcome | Result/evidence link |
|---|---|---|---|---|
| DISC-001 — Source identity | Not started | — | Not executed | — |
| DISC-002 — Solutions/projects | Not started | — | Not executed | — |
| DISC-003 — Declared project configuration | Not started | — | Not executed | — |
| DISC-004 — Toolchain inventory | Not started | — | Not executed | — |
| DISC-005 — Evaluated build settings | Not started | — | Not executed | — |
| DISC-006 — Central configuration | Not started | — | Not executed | — |
| DISC-007 — Dependencies before restore | Not started | — | Not executed | — |
| DISC-008 — Restore | Not started | — | Not executed | — |
| DISC-009 — Build | Not started | — | Not executed | — |
| DISC-010 — Tests | Not started | — | Not executed | — |
| DISC-011 — CI/CD and delivery | Not started | — | Not executed | — |
| DISC-012 — Compatibility evidence | Not started | — | Not executed | — |
| DISC-013 — Reconciliation | Not started | — | Not executed | — |
| DISC-014 — Baseline review | Not started | — | Not executed | — |

**Work status:** not started / in progress / complete / blocked / deferred / not applicable.  
**Evidence method:** source-inspected / tool-evaluated / executed; several may apply but record them as **distinct observations**.  
**Evidence outcome:** verified for stated scope / partially verified / blocked / failed / not executed / unresolved / not applicable. Work completion and verification are independent.

## Detailed step record — copy only when needed

### DISC-`NNN` — `<purpose>`

| Field | Recorded value |
|---|---|
| Work status and date | `<in progress/complete/blocked; date/time and zone>` |
| Operator | `<manual operator / CI workflow / source inspection>` |
| Source identity | `<repository, branch/tag, exact commit SHA, dirty state>` |
| Target scope | `<solution, project, TFM, configuration, platform, host as relevant>` |
| Applicability | `<SDK-style/traditional/mixed; framework family; OS/toolchain; tested vs assumed>` |
| Tool identity | `<name, full version, installed/provided origin>` |
| Working directory | `<path relative to repository root>` |
| Exact command | `<verbatim command or "source inspection only">` |
| Side effects | `<none observed / restored packages / obj/bin generated / other>` |
| Method and provenance | `<source-inspected/tool-evaluated/executed; new vs historical>` |
| Exit code | `<integer / not applicable / not captured>` |
| Observed result | `<actual concise outcome, not predicted behavior>` |
| Evidence path or URL | `<committed relative path, full Git SHA URL, run ID and artifact ID, etc.>` |
| Evidence retention | `<committed text, GitHub Actions expiry, local only, redacted copy>` |
| Evidence status | `<verified for stated scope/partial/blocked/failed/not executed/unresolved>` |
| Limitations and next action | `<what this does not establish; next small step>` |
| Article candidate | `<one useful illustrated lesson, or none>` |

If the command is not run, do **not** invent a command outcome or exit code. If the operation fails, capture the real failure; decide whether it is an application result, tool/environment block, or invalid procedure before rerunning. For changed SHA or toolchain, create another record or explicitly scope the new observation.

## Evidence manifest convention

Store entries as `EV-001`, `EV-002`, etc., linked to `DISC-NNN` and baseline findings. Use the dated evaluation's `evidence/manifest.md` when evidence exists.

| Evidence ID | Discovery step | Evidence source | SHA / execution scope | Retention or limitation |
|---|---|---|---|---|
| `EV-NNN` | `DISC-NNN` | `<source path, recorded output or workflow run>` | `<exact source and tool/host context>` | `<retention/status>` |

Keep original command output separate from any formatted report. Redact credentials and private paths; note redactions. Prefer text evidence stored in the evaluation repository; reference large GitHub Actions artifacts with an expiry warning and durable summary. Do not commit compiled binaries, caches, packages or unnecessary logs.

## Session handoff and article progress

**Last confirmed step:** `<DISC-NNN or none>`  
**Next manual action:** `<one concrete command and prerequisites>`  
**Open gaps/approval gates:** `<not executed steps and conditions>`  
**Blog evidence mapping:** `<section candidate and supporting EV IDs; no unsupported claims>`  

Leave the application repository and its main branch unchanged unless a distinct change is approved.
