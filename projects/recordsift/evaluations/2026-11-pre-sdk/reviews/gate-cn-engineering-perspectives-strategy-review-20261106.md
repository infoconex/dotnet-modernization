# Gate C-N engineering-perspective full review — practical modernization decision

**Date:** 2026-11-06 Pacific. **Status:** DOCUMENTATION/RESEARCH-ONLY, not governance approval, implementation authority, release-policy amendment, or independent human signoff.
**Author:** GPT-6 in the established author-context conversation. Five separate **simulated** engineering perspectives are applied; they are **one model's analyses, not independent experts**, actual human appointments or five peer votes. External reviews retained in issue #78: isolated GPT-6 complete but non-human, Gemini revised with evidence gaps, Claude access-limited and INCOMPLETE. This does not finish the genuine human review in issue #77.

## 1. What business/engineering question did we investigate?

The **primary goal** is a repeatable, evidence-driven modernization method for traditional .NET Framework applications without changing behavior or accidentally regressing releases. RecordSift is the controlled first case: **ten traditional C# 7.3 / net48 projects**, five production assemblies and five NUnit suites at frozen application SHA `8358780829458854a4b0356df5ac5e685f0a34c8`.

The primary legacy compatibility benchmark is **425 public-API entries, 419 discovered NUnit tests (418 pass, 0 fail, 1 expected skip), five XML documentation outputs, assembly/dependency/resource checks, local package and clean .NET Framework 4.8 consumer**. The research preparation [decision matrix](../modernization-preparation-decision-matrix.md) ranks baseline enforcement, five-suite local runner reconciliation, conditional LangVersion centralization and controlled deterministic builds before optional Source Link, PackageReference, SDK conversion or framework uplift. Its implementation proposals are NOT preapproved application changes.

**Gate C-N is a later, specialized question**: can locally produced classic Windows PDB native document/digest records plus physical source/compiler evidence support a *distinct* candidate source-provenance acceptance criterion? This is related to traceability and Source Link experiments, but **not a universal prerequisite to safely planning or validating SDK-style modernization**. Microsoft .NET SDK and porting documentation explains SDK-style migration separately; Source Link targets source debugging and attribution. Our historically introduced managed-reader checksum requirement **Gate C remains UNSATISFIED** and has NOT been waived. C-N has never been authorized to substitute for it.

**Key choice:** whether Gate C-N should be developed as an **operational production release gate** at all. No demonstrated near-term RecordSift release or modernization objective currently requires this bespoke production mechanism. Its value as a bounded research method is real; its production necessity is **not established**. This is a prioritization judgment, not a proof that no organization could benefit from advanced provenance checks.

## 2. Current-state verification — scoped evidence, not promoted claims

Research/code reviewed at frozen Gate C-N baseline `719275bb16feed7a8cd2eb7afeb7ae3cb7117991`, followed by D1 PR #81 `ac347e0ff845d3db02652d76b8d72e78b8cae0d1`, D2a PR #82 `cc9ffa8063cb10ae17b4542867684eb7e99a5ad5`, D2b PR #83 `a7d61bf1a1afca0a0ea3e9efbe92310aa1dd04b6`, and source/CI review PR #84 `1f003ae8879df9d3ffd93e7857ede9537f4b2d2d`.

| Evidence | What is established | What is not established |
| --- | --- | --- |
| EXP-043 / EXP-044 earlier live source investigations | Real trusted Windows classic-PDB original-source proof: RecordSift 64/64 per-assembly source-document records; separate fixture 2/2. | Universal PDB/runtime support, independently retained original source bytes, production gate or IDE stepping. |
| D1 final GitHub Actions [42294445275](https://github.com/infoconex/dotnet-modernization/actions/runs/42294445275) | 11 synthetic test cases, with correctly scoped positive/negative controls; exact head tree reconciled against GitHub PR merge tree. | Real signature authority, compilation, PDB, restore, CLR or release execution. |
| D2a final [42303167674](https://github.com/infoconex/dotnet-modernization/actions/runs/42303167674) | Real disposable traditional net48 builds/PDBs, two distinct outputs, five targeted intentional failures and CLR load witness. | Independent cryptographic compiler/output attestation; actual stale incremental compilation bypass; complete multi-Csc source/output envelope. |
| D2b final [42308376741](https://github.com/infoconex/dotnet-modernization/actions/runs/42308376741) | Two real isolated local NuGet restores, two distinct same-ID/version packages, installed/CopyLocal and loaded CLR candidate identity, five fail-closed controls. | Complete five-assembly RecordSift test/package/runtime dependency closure, official production NuGet pack/publication, atomic module hash in adversarial host. |
| Post-D2b source inspection in PR #84 | Real CI logs/HEAD checks; code-bounded evaluation of CN-01..CN-12, remaining P0 and two low-priority reuse issues. | New independently signed human assessment, original PDB bytes replay, approved release manifest, evidence custody. |

The D2a/D2b sanitized research artifacts have a 30-day expiry (approximately December 6, 2026). GitHub job upload digests and matching source/run metadata were independently read; ZIP payload bytes were **not** separately downloaded and decoded in the source review. Retained Git report text and exact hashes are historical audit metadata, not an independent raw-byte reconstruction.

All draft PRs **#74, #81, #82, #83, #84** remain unmerged; issues #77/#80 remain open with **no named independent human reviewers, manifest owner/custodian, approved production scope or policy**.

## 3. Five simulated adversarial roles, separate challenges

### A. Software architecture — RECOMMEND REFOCUS
**What works:** The research separates synthetic source/candidate/compiler contracts; evidence is pinned to immutable project snapshots and documented nonclaims. The initial modernization matrix deliberately separates low-risk property/build changes from package/framework changes.

**Challenge:** The experimental native-PDB source protocol is narrowly tailored to classic Windows PDB, traditional C# 7.3 net48, known generator behavior and controlled one-node builds. Making it a mandatory prerequisite for **general** .NET modernization would add platform-specific coupling and significant complexity without a demonstrated requirement.

**Finding:** The real goal is safe modernization. Preserve C-N as a **specialized optional acceptance design** rather than expanding it into a universal architectural gate. **Dissent condition:** if an actual customer, regulatory policy or operational threat requires source-to-release attestation, independently scope that separate work.

### B. Build/compiler — RECOMMEND STOP NEW EXPERIMENTS FOR NOW
**What works:** EXP-043/044 demonstrate physical-source/native-symbol pairing in the trusted research scope; D2a strengthens evidence with real paired PDBs and contextual Csc event witness; D2b covers a real local NuGet-to-CLR path.

**Challenge:** Current D2a logger emits unique completed task context and source count, not full compiler options/source identity-to-output authentication. Local same-run seals are not independently approved. D2a N05 is a **freshness-assertion negative**, not an actual demonstrated stale incremental compiler pass. Those are release-hardening obligations only if adopting C-N.

**Finding:** These gaps should **remain documented, not ignored**, but are not blockers to planning A1/A2/A3 modernization work under their own fixed acceptance contract. No new D3 is justified by current purpose.

### C. Security/privacy — RECOMMEND KEEP HOLD, AVOID UNNECESSARY EXPOSURE
**What works:** Trusted hosted disposable Windows runners, controlled synthetic sources, read-only GitHub permission, pinned major GitHub Actions, category-only logs and unconditional private cleanup for D2a/D2b.

**Challenge:** No independent prebuild approval/signing; no separately owned archive, retained immutable original source witness or release revocation; private raw material intentionally ephemeral. Host compromise, malicious PDBs, adversarial filesystem and unrelated generators are out of verified scope. D1 declared origin allowlist is not enforced for mutually matching approved/observed synthetic origin data; D2a/D2b include some bare `assert` positives rather than unconditional fail-closed requirements. Do not carry these into an enforced production gate.

**Finding:** Block C-N deployment. For **research-only reports**, a permanent Markdown/commit/run reference and existing provenance notes are sufficient as research documentation; do not demand production-grade WORM custody if no production release is relying on them. If future deployment is chosen, security-owned separate approval and evidence custody become mandatory.

### D. Quality/test — RECOMMEND PRIORITIZE THE EXISTING RELEASE CONTRACT
**What works:** Real five-suite baseline and contract established. D1/D2a/D2b use paired positives and intention-specific rejection codes, with genuine compiler/CLR/NuGet controls at their respective stages.

**Challenge:** Real-world modernization risk is breaking behavior, public API, dependencies or packaging, even while an elaborate PDB provenance check succeeds. D2b only exercises one dummy library; historical RecordSift five-suite CopyLocal logic is conditional and does not certify a full actual loaded production dependency map.

**Finding:** First ensure that **every planned change** passes 425-entry API, all 419 NUnit tests/skip accounting, five XML, resource/dependency/assembly, unpublished package/install and clean consumer acceptance. Inspect the existing runner correction in RecordSift PR #258 rather than duplicating changes. Isolate changes and negative-test the baseline gate before further project-format or package conversion.

### E. Release governance — RECOMMEND RESEARCH-ONLY WITH EXPLICIT FUTURE GATE DECISION
**What works:** Release HOLD has been preserved; user delegated bounded research but never authorized a production gate, Source Link adoption, application/main edits or PR merges. The original managed checksum gate remains openly unsatisfied rather than silently relabeled.

**Challenge:** No named human independent signoffs, protected release authority, manifest approver, durable custodian or approved policy disposing of managed Gate C. Five simulated personas cannot solve that organizational requirement.

**Finding:** Appoint named security/release/technical humans **only if there is a real proposed operational release use**, at which point the separate release-acceptance procedure in #77 controls. Without such use, seeking appointments now would be bureaucratic overhead rather than reduction of an imminent release risk.

**Combined simulated role disposition:** 5/5 **recommend Option A below**. This is not five independent human votes and is not production acceptance. No simulated perspective recommends another immediate PDB experiment or activating Gate C-N.

## 4. Ranked outcomes

| Priority | Finding | Consequence |
| --- | --- | --- |
| P0 production only | No independently approved entire source/component/target manifest (CV-01) | Production C-N BLOCKED; research milestone valid. |
| P0 production only | No independently accepted full RecordSift candidate test/package/runtime identity chain (CV-02) | Production C-N BLOCKED; release-contract tests must remain primary for modernization. |
| P0 production only | No independently protected end-to-end Csc-to-output custody (CV-03) | Production C-N BLOCKED; D2a research result remains useful. |
| P1 optional | Native corruption/source/DBI/C13 negatives, hashing policy, toolchain pinning and custody remain future scope decisions | Do not spend without a concrete operational need. |
| P1 prototype quality | D1 origin allowlist not actually enforced; D2a/D2b bare Python `assert` for some positives | Repair **if reusing** experimental verifier, not evidence of failed current CI. |
| High strategic priority | Lower-risk modernization acceptance preparation is already well researched but unimplemented in the frozen application | Refocus separate future proposal on stable baseline/test/run/package contracts and small reversible changes. |

## 5. Decision: explain what the stakeholder actually has to decide

### Recommended Option A — RESEARCH-ONLY C-N; REFOCUS (recommended)
Freeze new C-N experiments and production-gate implementation. Preserve pinned draft PRs, reports, exact runs and nonclaim disposition; do not merge, publish or silently change original Gate C. No production-grade signing/immutable evidence archive needs to be commissioned yet **because no real release relies on this research**. Resume **documentation-only planning** of lower-risk RecordSift modernization from the existing decision matrix:
1. A1: ensure complete original application release compatibility evidence is required for future candidates; explicitly account for corrected five-suite runner already present on release/0.2 PR #258.
2. Then consider A2 conditional LangVersion centralization and A3 deterministic settings **one at a time** with whole contract revalidation.
3. Only later separately propose SDK-style csproj conversion, packages.config/PackageReference and/or a new runtime TFM. Retain exact frozen application commit, C# 7.3 and net48 baseline until separately authorized.
4. Preserve Source Link production **HOLD** and original managed Gate C **UNSATISFIED** without using it as an unstated requirement for unrelated preparatory research. If a future approved release policy independently requires it, bring the issue back for specific decision.

**Requires stakeholder affirmation of prioritization before any actual RecordSift application implementation**. No research notes should imply that this automatically authorizes changing RecordSift, either main, merging PRs or publishing.

### Option B — COMMISSION AN OPERATIONAL C-N RELEASE GATE (only if genuine demand)
Would require actual named independent architect/build/security/QA/release reviewers, separate immutable pre-build manifest approval authority, real application component/source universe, trusted compiler/toolchain/candidate closure, independent custodian/retention/revocation and new fresh release-gate CI. Requires explicit decision about existing managed checksum Gate C and separate Source Link/IDE adoption gates. **Significantly more complexity** and no demonstrated immediate modernization dependency. Do not start from delegated research alone.

### Option C — ABANDON ALL C-N RECORDS (not recommended)
Discouraged; destroys useful retained evidence and reversible future options. Preserve the research even if no production use is selected.

## 6. Stakeholder one-step, nontechnical decision framing

**Step 1 (only decision now):** “Are we pursuing an operational release-security gate for a specific real application because we need it now, or are we learning how to modernize legacy applications safely?” Given the stated project purpose, recommendation = **the latter** (Option A). No need to choose hash algorithms, PDB formats, signing keys, 30-day/7-year retention or reviewer names.

**Step 2 (after Option A, later and separately):** Present a focused first **RecordSift improvement proposal** with exact files, review scope, expected behavioral invariants (425 API/419 tests/5 XML/package/consumer), CI controls, rollback and decision needed before application edits. Owner explicitly approves the scope; no automatic app modification.

**Step 3 (only if Option B chosen later):** Explain actual use case and risk being prevented; then recommend named reviewers, custody and policy. Real human signatures cannot be manufactured by the model.

## 7. Governance disposition

**Original managed Gate C: UNSATISFIED. Native Gate C-N production: NOT_AUTHORIZED. Source Link production: HOLD.**
**No merge, RecordSift changes, research-main edits, package publication, live D3, production gate, human appointment or release-policy waiver.**
All findings are available for genuine independent human review if Option B is later chosen. Claude remains incomplete and should not receive peer-review reports while its blind review is pending.
