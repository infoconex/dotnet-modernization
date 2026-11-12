# Gate C-N — proposed immutable manifest, custody and enforcement protocol

**Version:** C-N governance proposal 0.1 (2026-11-06 Pacific). **State:** DISCUSSION DRAFT / REVIEW PREPARATION ONLY. **Authority:** [stakeholder preparation approval #73](https://github.com/infoconex/dotnet-modernization/issues/73#issuecomment-6680589160); [tracking #77](https://github.com/infoconex/dotnet-modernization/issues/77). **This document does not configure a production gate or appoint a custodian.**

## 1. Two separate artifacts: pre-build authorization versus post-build evidence

### A. Pre-build reviewer-controlled immutable scope manifest

A future production acceptance manifest MUST be created **independently of the candidate DLL/PDB, current build log and audit report**, and approved **before** any acceptance build begins. It must be immutable and pinned by content SHA256/signature or a reviewer-controlled protected revision. Its expected universe must not be silently populated from the output it purports to verify. Reject missing, unknown and extra project/build/source-target records.

**Proposed manifest attributes** (names/shape are prospective; not an implemented or preapproved production schema):

| Field | Expected semantics / reviewer verification |
| --- | --- |
| `protocol_revision`, `policy_stage` | Exact supported C-N policy revision; only review stage until separate release activation. |
| `application_repository`, `application_commit` | Full official repository identity, immutable application commit, clean tracked checkout and branch/ref expectations. |
| `compiled_components[]` | **Entire externally approved production assembly/project/target universe**, each unique case-normalized project identity, configuration/platform/TFM, expected assembly output relative path and associated native PDB path; the approval package enumerates 5 RecordSift assemblies if this application is eventually selected. |
| `expected_compiler_inputs` | Explicit expected compiler-source identity inventory or independently reviewed exact count+provenance origin categories **per component**; for stronger release claims, compare the full original normalized identity set in **private trusted runner memory** with approved private inventory. Never derive expected totals from candidate PDB. |
| `allowed_generator_contracts[]` | Initially only `EXP042_MONIKER_ONE_PER_COMPONENT` with one real independently witnessed moniker source; all other generators/external/untracked inputs fail closed pending independent authorization. |
| `supported_compilation` | Traditional C# 7.3 net48, Release classic Windows PDB / `pdbonly`, trusted local compiler-produced PDBs, independently pinned compiler/SDK/MSBuild/Source Link packages and vulnerability policy. No fallback to unsupported formats. |
| `required_original_release_gates[]` | Explicit baseline SHA, 425 API, 419 NUnit including skip policy, five XML, assembly metadata/resources/dependencies and NuGet installed-consumer acceptance, with exact **candidate** binary identity and failure treatment; current observations are historical, not release exemptions. |
| `review_approval` | Authentic independently attributable reviewer identities, approval of **exact manifest SHA**, scope and revision, dates, finding disposition, security/release approver, expiry/revocation semantics. No self-approval by build job. |
| `custody_policy` | Named custody authority, approved storage identifier, immutable retention, access/revocation incident procedure and replay policy, with no public private-source material. |
| `decision_record` | Pointer to an explicit **later** stakeholder release-policy decision resolving legacy managed checksum Gate C; blank/approval-preparation-only cannot activate. |

**Binding rules:** manifest hash is captured at workflow start **before** loading candidate artifacts. Reviewer approval and hash must come from an identity/branch/path **not writable by the same candidate build**. Attest source SHA and compiler identity, compare actual set and count for **every** approved component, compare expected artifact file locations and actual paired PE CodeView/PDB GUID+age. The actual GUID/age is known only *after* compilation; it is checked from the independently read DLL/PDB pair, not presumed by a pre-build manifest. A change in scope, source revision, generator, toolchain or security advisory baseline invalidates prior approval and requires fresh reviewer signoff.

**Important distinction:** the existing `gate_cn_live_provenance.py` manifest has `authorization: DESIGN_VALIDATION_ONLY` and is consumed **inside** an isolated experimental runner; the fixture's JSON was assembled during the run. The historical `gate-cn-recordsift-scope.json` pins observed counts from already-run research. Neither is an immutable **preapproved production manifest**. Their schema must not be relabeled or trusted as such.

### B. Post-build live attestation / release envelope

The live verifier emits only **allowlisted sanitized public aggregates**, with exact source/workflow/validator/manifest SHA, component verdict, original expected vs observed counts and origin categories, PE/PDB pairing, Csc task/source and generated producer categories, native source-document set equality, candidate compatibility identities/results, original release gates and cleanup status. Full source names/pathmaps/URLs, private Csc command lines, native PDB streams, original physical bytes and per-document digests remain private. An authorized custodian authenticates exact sanitized bytes and records SHA256 and genuine run/job identity, distinct from the build author's self-attestation.

**Release aggregation must never pass on sanitized JSON alone.** It needs current fresh trusted build execution; it must fail closed when any required component is absent/unknown, live Csc/PDB/source origin or release gate incomplete, source/manifest changed since approval, trusted artifact custody unavailable, or the policy decision is not explicitly active. Retained EXP-043/044 public reports provide historical comparison, **not** new live proof.

## 2. Mandatory authority separation / anti-confusion controls

There are at least four independent actors: (1) manifest preparer/technical author; (2) independent technical/security reviewer(s) who authorize the immutable build scope; (3) trusted runner producing live ephemeral evidence; and (4) evidence custodian and release approver evaluating it. A single service identity may not independently sign its own code, approve its own source manifest, manufacture an artifact and declare release acceptance.

**Identity proof:** signoffs must have authenticated identities and date, exact reviewed Git/manifest SHA and findings, recorded in an access-controlled governance system (e.g., branch-protected review with identifiable approvers and audit logs, or organization-approved signature workflow). Whether GitHub protection/signatures are sufficient is a **stakeholder/security choice**, not yet verified.

**Policy states:** `REVIEW_PREPARATION_ONLY` → `HUMAN_REVIEW_PENDING` → `HUMAN_REVIEW_COMPLETE` (signed recommendations only) → **separate stakeholder decision** `RELEASE_ACCEPTED` for explicitly enumerated scope, if approved. Even a `HUMAN_REVIEW_COMPLETE` recommendation cannot activate or merge anything. The existing managed reader checksum Gate C remains `UNSATISFIED` until **explicitly disposed of**, not by reinterpretation of old outputs. Source Link production requires further separate IDE/remote-source acceptance.

**Approval expiry:** revocation, digest mismatch, new vulnerability advisory affecting pinned components, different source SHA, project set, runner/toolchain, unreviewed generated producer or failed compatibility test requires **BLOCKED** until reassessed. Never fall back to “report consistency passed”.

## 3. Trust, threat and privacy boundaries

**Trusted assumptions:** GitHub or explicitly approved source host, authentic compiler-produced classic PDB on trusted isolated Windows build host, trustworthy captured source bytes/task events and pinned toolchain. This is NOT a sandbox for arbitrary crafted PDBs. Native named stream keys must never be used as file paths. Limits apply to memory, raw PDB streams, input count/size, log size and path normalization; physical source bytes compared before and after compilation. Unrecognized format/algorithms, nonunique Csc events, path aliases/collisions, sources outside approved scope, missing generated producer and incomplete cleanup all block.

**Sensitive material prohibited from retained artifacts:** source snapshots, raw compiler task input/events or arguments, raw diagnostic logs, native PDB files/streams, source names/paths/URLs, document keys or per-document digests. This includes free text in error messages and uploaded filenames. Archive only fixed public fields after schema/allowlist privacy review. The current EXP-043/044 provenance ZIP digests and public JSON SHA256 values are specifically approved as *research report contents*, not source attestations for new builds.

## 4. Custody alternatives for stakeholder/security selection

| Alternative | Benefit | Unresolved concern / required owner action | Proposed disposition |
| --- | --- | --- | --- |
| **A. Security/release-owned immutable object archive** (e.g. locked object-versioning/WORM retention with independent access) | Durable tamper-resistant sanitized report/approval envelope beyond CI artifact expiry; explicit custodian and revocation/audit trail | Security and release must provision storage, access/retention policy, reliable object digest validation, backup/incident response. Integration has **NOT** been validated. | **Recommended for a future production acceptance system**, subject to owner approval. |
| **B. Protected governance Git repository/release with independently approved immutable signed revisions** | Easy audit of *small sanitized reports*, manifest approval commits, exact SHA and accessible review history; existing research draft already stores report bytes | Branch protection, immutability, signer/reviewer identities, retention, deletion privilege and independent custody **NOT verified**. Mutable drafts alone are not tamper-evident governance. | Practical research reference; may be acceptable only if security/release verifies controls and responsible custodian. |
| **C. GitHub Actions 30-day artifacts only** | Reuses current evidence test tooling and ZIP SHA256 | Artifacts expire; lack of custody, may not reproduce original private compiler-byte witness, cannot serve durable release proof. | **REJECT as sole release evidence custody.** |

**Retention duration** (e.g., the release record retention period), custodian name, storage account, replication, signature method, offline replay and revocation deadline **NOT SELECTED**. Do not invent commitments. At minimum, retain the public manifest version/hash, approval identities, exact build source/executor SHA and toolchain pins, actual run/job URL, ZIP/report SHA256, sanitized results, negative-control and original release-gate outcomes, reviewer dispositions and custody write/verify acknowledgements for the approved compliance period.

**Replay** has two distinct modes:
1. **Historical audit replay:** independently verify SHA256 and allowlist of archived sanitized report, exact origin run/workflow/repository/commit, immutable manifest approval and provenance; this establishes what an authenticated **past trusted build reported**, not source bytes.
2. **Live acceptance replay:** fresh isolated trusted compiler invocation for the approved application commit/manifest, original physical source snapshot and task input capture, native PDB identity/hash verification, original release/consumer gates and new independently custodial receipt. An expired historical ZIP or copied public report **must not pass** this mode.

**Failure/revocation:** a leaked path/source digest, failed archive checksum, wrong identity, unexpected access, missing cleanup or compromised build host invalidates affected attestations; freeze the current release decision, preserve safe audit metadata, triage incident with security/release custodian, issue explicit revocation and require fresh authorized live run. Do not silently delete evidence or accept old CI status.

## 5. Proposed enforcement and full release compatibility ordering

1. Independently approved immutable **pre-build** scope and named authority; confirm policy `RELEASE_ACCEPTED` **only if** a later explicit stakeholder decision authorizes this application and criteria. For now stop at research-only.
2. Isolate runner/check pinned toolchain, source/manifest executing SHA and read-only inputs. Reject unapproved scope or unsupported compiler/PDB format.
3. Capture compiler-time physical sources, unique structured Csc inputs and observed generated producer. Build fresh candidate. Verify physical bytes unchanged post-Csc.
4. Independently parse paired actual PE/native PDB and complete named/DBI/C13 identities, all digests and pathmap source sets against approved full component universe; fail closed on any missing/extra/mismatched entry.
5. Run **original and candidate** API inventory, NUnit tests (including skip contract), assembly metadata/resources/references, five XML docs, NuGet package pack/install and **clean .NET Framework 4.8 consumer** checks. Confirm test/candidate copy-local DLL and package identity, not baseline DLL by accident.
6. Sanitize allowlisted aggregate evidence; unconditionally destroy raw compiler sources, PDBs, logs and task events. Independent custodian authenticates report ZIP + run/source/manifest SHA and grants a custody receipt.
7. Review all gate verdicts, human signoffs, security exceptions and complete release policy. **Any incomplete/unknown => BLOCKED**. No automatic conversion of `RESEARCH_VALIDATED` or `AGGREGATES_CONSISTENT_RESEARCH_ONLY` into release acceptance.

**Current implementation gap:** EXP-043 did run the full original release contract and real five-PDB evidence, while the external-manifest live adapter from EXP-044 proves only native original-source provenance on a tiny fixture. No consolidated **reusable production release workflow** that runs steps 1–7 on an externally **preauthorized production manifest** has been implemented or accepted. Human review must decide whether and how to commission one; design approval alone does not fill this gap.

## 6. Human decisions explicitly pending

- Appoint real independent architecture/build/security/QA/release reviewers and a named decision authority.
- Choose custodian **A or B** with verified controls (C insufficient), actual retention, integrity and incident ownership.
- Select an in-scope application/release contract for a *future* policy acceptance review, with immutable preapproved component list and generator support.
- Decide whether to commission the **separate production-oriented implementation** needed to enforce the approved manifest and original release gates (not authorized by research completion alone).
- **Later**, only on signed evidence, decide explicitly whether to accept or reject native Gate C-N for the stated scope and disposition of the existing managed checksum Gate C. **Source Link adoption remains separate.**

The [formal review packet](gate-cn-formal-acceptance-review-package-20261106.md) and [unsigned decision record](gate-cn-independent-review-decision-record-20261106.md) are the required review entry points. None of these proposals represent completed organizational actions.
