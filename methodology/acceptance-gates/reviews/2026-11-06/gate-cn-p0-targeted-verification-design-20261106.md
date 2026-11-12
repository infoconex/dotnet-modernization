# Gate C-N — P0 targeted source verification and negative-control design

**Prepared:** 2026-11-06 Pacific. **Disposition:** SOURCE-REVIEWED DESIGN ONLY; NO NEW EXPERIMENT EXECUTED; NO HUMAN SIGNOFF.  
**Parent:** [issue #80](https://github.com/infoconex/dotnet-modernization/issues/80); [review consolidation](gate-cn-preliminary-cross-model-consolidation.md); [governance #77](https://github.com/infoconex/dotnet-modernization/issues/77).  
**Immutable source reviewed:** research code at 719275bb16feed7a8cd2eb7afeb7ae3cb7117991; RecordSift at 8358780829458854a4b0356df5ac5e685f0a34c8. The current document is a later research-branch addition; **do not silently change the reviewed-code baseline**.

## 0. Scope, authority and status

Stakeholder Option B in [#72](https://github.com/infoconex/dotnet-modernization/issues/72) authorizes design/research validation of a *separate* Gate C-N, and the preparation decision in [#73](https://github.com/infoconex/dotnet-modernization/issues/73#issuecomment-6680589160) authorizes human review preparation. [#80](https://github.com/infoconex/dotnet-modernization/issues/80) explicitly does **not** authorize running new negatives or producing a release-capable verifier. This document defines requirements, source-backed current behavior, proposed interfaces, **unexecuted** targeted controls, and a bounded future decision.

Existing managed-reader Gate C **UNSATISFIED**; Gate C-N production **NOT_AUTHORIZED**; Source Link production **HOLD**. Frozen historical EXP-043 64/64 and EXP-044 2/2 physical source provenance remain valid within their documented trusted-Windows/native-PDB scope. Neither is a complete production release identity/authority chain. No RecordSift/source/main edits, workflow execution, PR merge, package publication, human signature, custody appointment or gate activation are authorized by this design.

Use these classifications: **OBSERVED CODE** = source independently read at immutable SHA; **REPORTED RUN** = authenticated CI metadata but private source/PDB not replayed; **UNTESTED HYPOTHESIS** = proposed failure scenario not observed; **FUTURE REQUIREMENT** = release acceptance obligation only after explicit governance decision.

## 1. P0-1 — Independent and complete prebuild compilation manifest (CV-01)

### Source-backed boundary

- **OBSERVED CODE:** [live adapter, lines 25–37 and 76–119](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/validators/gate_cn_live_provenance.py#L25-L119) has a strict but caller-supplied research-only manifest: component/project/evidence paths, assembly name, counts and one moniker producer. It requires authorization = DESIGN_VALIDATION_ONLY. It has no independent signature, approval lookup, exact tracked-source identity inventory, configuration/platform/TFM/output contract, or full source/project graph approval.
- **OBSERVED CODE:** [EXP-044 runner lines 90–108](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/pilots/gate-cn/EXP-044/run.ps1#L90-L108) writes the research manifest during the pilot. It **does not** represent independently approved scope.
- **OBSERVED CODE:** [existing manifest/custody proposal](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/methodology/acceptance-gates/gate-cn-manifest-custody-review-protocol-20261106.md) already requires prebuild independent approval and prevents runtime authorization by historical sanitized JSON. This design refines the missing executable acceptance contract, not an already implemented feature.

### Proposed domain contract (FUTURE REQUIREMENT, not active schema)

**M-01 — Authority:** A separately controlled, immutable approval binds exact canonical manifest bytes SHA256, approval policy revision, repository and pinned source commit, author and *independent* reviewer identities, approval timestamp, expiry, revocation/incident registry identity, and intended build purpose. The build job cannot write, grant or self-approve this authority. Verify authentic signature or independently protected review/identity service and active approval **before compilation**. Recompute digest; reject TOCTOU scope changes, signature mismatch and replayed/revoked approvals.

**M-02 — Whole production graph:** Approval lists the exact finite compilation universe, not just components discovered from PDB/build/validator: each unique repository-relative project, assembly identity, target framework net48, configuration Release, platform, target/compile invocation identity, deterministic/debug/native-PDB settings, expected DLL/PDB output location, compiler/toolchain policy, and declared project dependencies. Require a complete independently reviewed assembly/target graph with no unknown, absent, duplicate, case-folded alias or out-of-scope production component. A production graph baseline must come from independent source review/approved inventory, not from postbuild PDB or validator output.

**M-03 — Compiler inputs:** For each component, approve the **full normalized tracked input identity set** (repository-relative path + pinned Git tree/blob identity or SHA256) and the exact supported generated-source identity/origin contract. Each nontracked, external or unrecognized compiler input blocks. The currently supported moniker source can be approved via a single exact generated path/origin/producer contract when its actual bytes are created during compilation, then authenticated by the existing producer/physical-byte chain. A count is an independent *cross-check*, **not a substitute for the full source identity set**.

**M-04 — Approval and expected vs actual:** Verify a canonical, versioned manifest with collision-resistant path normalization, stable component ordering, duplicate-key rejection, explicit no-extra-input rules, and protected digest. Compare complete *actual* project/target/source/invocation sets from the trusted runner with those approved. Distinguish inputs loaded from approved manifest from observed build and PDB evidence; never allow observed sets to populate approved fields.

**M-05 — Original compatibility policy:** Bind the approved application release contract to exact baseline IDs and acceptance expectations (425 API entries, five XML outputs, five test suites with 419 discovered/418 pass/1 approved skip, assembly metadata/resources/references, unpublished package and clean net48 installed consumer for this frozen pilot). Historical aggregates are not acceptance for a new candidate.

### Minimal proposed, unexecuted negative controls

| ID | Controlled alteration | Expected fail-closed assertion | Evidence |
| --- | --- | --- | --- |
| M-N01 | Omit one approved production component from a caller-supplied run manifest while preserving self-consistent counts | Externally approved whole-set comparison rejects missing component; self-supplied design-only manifest is **not** authoritative | Approved manifest SHA; observed approved/actual counts; fixed error category |
| M-N02 | Add an unexpected assembly/project or a tracked compiler input without approval | Reject extra project/input, including when PDB and Csc agree with one another | Sanitized unexpected-count category |
| M-N03 | Rewrite approval digest/authorization/signer or use revoked/expired approval | Block before compiler invocation; no self-authorization or fallback | Approval registry response category; manifest/approval SHA, no private input names |
| M-N04 | Supply source-set cardinality equal to approved count, with one approved path replaced | Exact source-identity set mismatch must block; counts alone insufficient | Aggregate missing/extra counts only |
| M-N05 | Case/relative/alias duplicate component or unauthorized generated/external source | Reject collision/out-of-scope producer | Fixed category; no raw paths |

**Claim threshold:** Passing these negatives against a future prototype would not constitute a production-approved manifest: approval identities, protected controls, completeness review, custody and separate stakeholder acceptance still required.

## 2. P0-2 — Candidate binary identity to tests, package and runtime (CV-02)

### Observed code, not an observed release failure

- [EXP-043 candidate staging lines 119–140](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/pilots/recordsift/EXP-043/build-remaining.ps1#L119-L140) copies each candidate production DLL into every test output **only if a destination already exists**, then SHA256-compares copied file to candidate. It does not reject missing *mandatory* copy-local destinations. Preserve these successful hash comparisons; add an externally approved mandatory dependency matrix.
- [EXP-014 runner lines 29–86](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/pilots/recordsift/EXP-014/run.ps1#L29-L86) validates five test suites, public API, XML and runs the local package/consumer scripts. Running all suites is **observed**; runtime DLL provenance is not.
- [RecordSift package script lines 15–31 and 70–125](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/build_release_candidate.ps1#L15-L125) copies source output DLL/XML into staging, checks assembly/file version and package entry presence, but does not compare each entry's SHA256 to the previously PDB-authenticated candidate DLL.
- [RecordSift consumer lines 21–38, 57–98, 101–146](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/verify_clean_consumer.ps1#L21-L146) allows a local feed **and** nuget.org for dependency resolution, validates package ID/version and executes standalone consumers after copying installed DLLs. The local-feed path does not hash-join the chosen package or loaded candidate assemblies to the authenticated build. Do not claim that NuGet actually selected the wrong package.

### Frozen *source-reference* production test-dependency closure

Independently extracted from the ten frozen [RecordSift project files at 8358780…](https://github.com/infoconex/RecordSift/tree/8358780829458854a4b0356df5ac5e685f0a34c8). These are direct/transitive **project reference** closures, **not yet independently certified effective runtime probe/copy-local inventories**; approval must reconcile MSBuild ReferencePath/CopyLocal outputs and actual runtime binding.

| NUnit suite | Production assembly project-reference closure |
| --- | --- |
| Domain.Tests | Domain |
| Application.Tests | Application, Domain |
| Infrastructure.Csv.Tests | Infrastructure.Csv, Application, Domain |
| Infrastructure.Reporting.Tests | Infrastructure.Reporting, Infrastructure.Csv, Application, Domain |
| Infrastructure.Xlsx.Tests | Infrastructure.Xlsx, Application, Domain |

The Csv suite also directly references the Application.Tests test support project; this does not add a sixth production assembly. Mark a required DLL missing from its approved per-suite closure as **BLOCKED**, not "not applicable"; extra unexpected candidate production DLLs require explicit classification and approved policy.

### Required immutable candidate chain

For each compiled component, bind **compilation envelope ID → output DLL SHA256 / native PDB SHA256 → PE RSDS GUID+age/PDB pairing → staged candidate DLL SHA256 → every mandatory test copy-local SHA256 → packaged lib/net48 DLL entry SHA256 → actual selected nupkg SHA256 → installed nupkg SHA256 and extracted DLL SHA256 → consumer bin DLL SHA256 → actual loaded CLR assembly identity, MVID, path/load context and file SHA256**. Record assembly FullName/version as supplemental checks only; same version does not imply same bytes. A matching MVID alone is not a unique binary or source attestation. Require all five across the package regardless of test-suite-specific closure.

Treat package selection and assembly resolution as *events to attest*, not inferences from filenames or exit code: isolate the local package feed from public dependency resolution; verify the exact selected archive hash; reject ambiguous duplicate candidate versions; log the runtime binding in an independently controlled harness, with load context, process identity, path, SHA256 and MVID. Account for .NET Framework GAC/probing/shadow-copy behavior; prohibit unapproved resolver redirects. Protect staging/installation paths against swap between hashing and load; verify after load in same trusted execution context.

### Minimal proposed, unexecuted negatives

| ID | Alteration | Mandatory assertion |
| --- | --- | --- |
| B-N01 | Delete a required production copy-local DLL before one specific suite | The suite candidate-binding prerequisite fails, even if NUnit could otherwise load via alternate probing |
| B-N02 | Replace one suite's candidate DLL with version-equal but different bytes | Candidate-to-suite SHA256 mismatch fails before an apparently passing NUnit result |
| B-N03 | Use identical original source input bytes but a **binary-different** DLL produced with deliberately changed options | Per-candidate output SHA identity join rejects substitution; source equality alone does not allow the replacement. Confirm a real binary difference before treating the negative as valid |
| B-N04 | Supply two packages with same ID/version via different feeds or a substituted local .nupkg | Installed package SHA256 must equal selected approved package; reject ambiguity/wrong choice, not just wrong ID/version |
| B-N05 | Introduce an unapproved CLR assembly probing/GAC/load-context resolution that executes another same-named/version assembly | Actual loaded assembly path/context/SHA256 identity differs from expected and blocks; do not rely solely on on-disk staged hashes |
| B-N06 | Swap packaged lib/net48 DLL after copy, retaining valid metadata/version | ZIP entry digest must equal attested candidate DLL; block package acceptance |

For each B-negative, preserve the original positive control and prevent unrelated failures from masking the intended assertion. These tests are **designed, NOT EXECUTED**.

## 3. P0-3 — Specific Csc invocation, output, freshness and replay (CV-03)

### Source-backed fact boundary

- [CscParameterLogger.cs lines 14–75](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/pilots/recordsift/EXP-042/CscParameterLogger.cs#L14-L75) observes TaskStarted and structured TaskInput Sources; it joins task events with integer TaskId, expects one event, and writes only the input names/count in a private file. It does **not** bind a unique full BuildEventContext, Csc parameters/options, task completion, output path/hash or invocation identifier into the emitted file. The multicore collision scenario is **UNTESTED**, not an observed historical defect.
- [exp042_source_provenance.py lines 164–230](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/validators/exp042_source_provenance.py#L164-L230) parses and compares that event's source names with physical capture. This establishes source **task input identity**, not unique emitted output.
- [exp043_five_pdb_audit.py lines 26–41](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/validators/exp043_five_pdb_audit.py#L26-L41) independently compares PE CodeView RSDS GUID+age with native PDB Info Stream GUID+age: strong local **pairing**, not invocation freshness.
- [gate_cn_live_provenance.py lines 175–245](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/validators/gate_cn_live_provenance.py#L175-L245) checks the DLL/PDB, source snapshots, actual physical-file bytes, Csc sources and moniker producer separately. The resulting claim deliberately remains **research-only**.
- [EXP-043 Rebuild lines 80–92](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/pilots/recordsift/EXP-043/build-remaining.ps1#L80-L92) and [EXP-044 Rebuild lines 70–83](https://github.com/infoconex/dotnet-modernization/blob/719275bb16feed7a8cd2eb7afeb7ae3cb7117991/tooling/pilots/gate-cn/EXP-044/run.ps1#L70-L83) mitigate stale outputs historically; no stale-binary false pass has been demonstrated.

### Required invocation/output attestation (FUTURE REQUIREMENT)

**I-01 — Freshness boundary:** Before each candidate compiler invocation, trusted runner creates a unique nonreused, confined output root; records absence of DLL/PDB and source/manifest/toolchain SHA, task/build-run nonce and monotonic event ordering. Clean/rebuild is required but alone is not proof of non-replay. Assert outputs newly created after the authorized task started and before attestation; prevent mutable shared paths and incremental reuse.

**I-02 — Unique task identity:** Correlate all Csc TaskStarted/TaskInput/TaskFinished events by full MSBuild BuildEventContext (node/project-context/target/task/submission as available), unique build-run nonce, canonical project/target/configuration, observed source inputs, output assembly/PDB paths and relevant compiler command parameters. For v0.1 a strictly serialized single-Csc invocation and fail-closed reject on multiple/unattributed events is a reasonable **proposed** scope; do not assume TaskId global uniqueness across nodes.

**I-03 — Invocation settings:** Capture independently approved option/response-file material and SHA256 (including deterministic, debug format, optimize, defines, pathmap, warning/language level, reference identities, compiler version and significant environment). Full command line/paths remain private; allowlist sanitized option categories/digests. Pin exact toolchain in P1 CV-04.

**I-04 — Concrete outputs:** After verified Csc task completion, hash DLL and PDB *bytes* in the protected fresh root; record exact output paths/lengths/SHA256 and parse pair identity (PE CodeView GUID+age == PDB Info GUID+age). Independently inventory PE MVID and assembly identity as extra diagnostics; MVID and GUID+age do **not** substitute for SHA256 or fresh invocation evidence. Bind emitted hashes into a single tamper-evident invocation envelope before stage/test/package operations.

**I-05 — Enforcement and limit:** Require precise one-to-one relation between approved invocation, actual event, source-byte snapshot and produced DLL/PDB; reject orphan task/events, undeclared outputs, preexisting output, mismatched flags, stale/replayed pair, untrusted tool or changed stage bytes. These controls hold **only under explicitly trusted runner/toolchain and custody assumptions**; logs from a hostile or self-authorizing build cannot cryptographically prove causation.

### Minimal proposed, unexecuted negatives

| ID | Controlled scenario | Expected proof/decision |
| --- | --- | --- |
| I-N01 | Supply a previously valid, internally matching PE/PDB pair without executing the current Csc task | No fresh Csc completion/unique output-creation attestation → BLOCKED (pairing alone would not suffice) |
| I-N02 | Recompile identical source bytes with different explicit compiler flags, then substitute a pair from the other invocation | Approved flags and execution envelope must bind each exact DLL/PDB SHA; reject cross-invocation replay |
| I-N03 | Preserve event/source identities but substitute a different paired DLL/PDB | Pair may remain internally valid, but output hash/invocation identity join must fail |
| I-N04 | Inject second concurrent Csc task or duplicate short TaskId with distinct node context | Reject ambiguity under serialized v0.1 policy; full BuildEventContext correlation is a separately authorized extension |
| I-N05 | Reuse nonempty output directory or pre-existing DLL/PDB with a skipped/no-op Csc | Reject before accepting freshness claim |
| I-N06 | Change PDB only or DLL only | Reject SHA256 and/or PE/PDB pairing mismatch; controlled mismatch must exercise intended stage |

All are **UNTESTED HYPOTHESES** until authorized disposable controls produce immutable run SHA, exact expected error stage, sanitized result and a valid positive control.

## 4. Reusable architecture and traceability design

Prefer independent domain contracts rather than modifying app scripts. Suggested components are *design names, not existing modules*:

| Domain-defined contract | Adapter responsibilities | Main invariant |
| --- | --- | --- |
| ApprovedCompilationScope / IApprovalAuthority | Immutable manifest/approval registry adapter; canonical hashing and authentic signer/revocation checks | Expected scope exists **before** build and cannot authorize itself |
| ICompilationGraphObserver | Trusted MSBuild graph and project/target/source inventory adapter | Exact approved vs actual set equality |
| ICscInvocationObserver | Full BuildEventContext structured recorder, producer evidence, option/toolchain digest; private capture | Unique task + settings + completion |
| ICompilerOutputAttestor | Isolated output freshness, PE/PDB parser, SHA256/MVID adapter | Exact output bytes match one attested invocation |
| ICandidateIdentityVerifier | Test dependency matrix, package ZIP, isolated NuGet feed, runtime CLR module witness adapters | End-to-end same candidate DLL SHA256 for every required edge |
| IEvidenceCustodian | Allowlisted sanitized report, protected approval/run association, expiry/revocation | Independent receipt, not self-attestation |
| IReleaseDecisionPolicy | Combines approval + P0 + existing original release gates + human decision | **BLOCKED** on missing/unknown; never promotes research verdict |

Use immutable value objects for ComponentIdentity, SourceIdentity, InvocationIdentity, BinaryDigest, PackageIdentity and RuntimeAssemblyIdentity; typed failure reasons rather than free-text private paths. Contract tests should use in-memory fakes independent of Python PDB libraries, MSBuild or NuGet. Thin adapters may be Python/PowerShell/C# where unavoidable; retain inward dependencies, Microsoft C# conventions, no generic "Helper" abstraction and no changes to RecordSift.

**Mandatory evidence fields:** policy/manifest schema + exact SHA + approved authority identity/expiry status; frozen app SHA; exact research validator/workflow/toolchain SHA; build run/job identity; approved/actual component and source origin counts; per-component output DLL/PDB hashes kept in protected private execution envelope (public report only allowlisted non-sensitive digests by policy); PE/PDB match; invocation event association; per-suite copy-local identity verdict; package candidate ZIP SHA; installed and runtime witness verdicts; 425/419/5 original compatibility verdicts; cleaning/custody status; release decision marker. Public artifact/privacy allowlist requires security review. Historical sanitized aggregate reports cannot satisfy fresh build obligations.

## 5. Smallest next investigations; expected evidence and stopping rule

**Stage D0 (already authorized: this document):** static source review + explicit contracts/negative-control specifications + governance decision. No build, mutation, production verifier or branch merge. Status **COMPLETED AS DESIGN**, not evidence-gap closed.

**Stage D1 (separate approval needed):** isolated, disposable *synthetic-only* contract/adapter negative controls M-N01..05, B-N01..02/B-N04 (mock package selection), I-N01/I-N03/I-N05 with explicit expected failure stages. Run under unprivileged CI with no private PDB/RecordSift changes, no production release path; require clean fixture deletion and allowlisted reports. A green synthetic result supports only the tested assertions.

**Stage D2 (separate explicit live-build approval needed):** *one* non-RecordSift traditional net48 single-project Windows native-PDB fixture, targeted I-N01/I-N02/I-N03 and B-N03/B-N05 as practical. Use new unique issue/experiment ID and workflow at an immutable research SHA; retain positive controls, one deliberate mutation per scenario, absence/pairing/source/flags/sha checks, privacy-safe report and cleanup. No rerun of 64-document EXP-043 unless a specific new RecordSift-only gap is demonstrated. No Portable PDB or arbitrary generators.

**Stage D3 (future separate approval):** build/review production-capable enforcement integrating all original release gates and whole approved scope, independently reviewed by named humans and custodian. **DO NOT INITIATE** from this design. This stage cannot automatically accept C-N or waive Gate C.

**Stop here for stakeholder decision:** request either **Option A (recommended): authorize D1 design-scoped disposable synthetic negatives only, with protections above**; **Option B: authorize D1 plus explicitly bounded D2 after D1 passes and a separate preregistered fixture/CI evidence plan is reviewed**; or **Option C: preserve design only/no new execution**. None authorizes D3. If interpretation of existing Option B covers a synthetic edit, issue #80's explicit non-execution language still requires clarification/approval before execution.

## 6. P1 preserved, not inadvertently expanded

CV-04 toolchain, CV-05 real native-PDB mutation, CV-06 SHA256-only vs explicitly approved native SHA1, CV-07 logs/retention/revocation, and CV-08 full parallel-node context are separate future work, not prerequisites to publishing this design. Prefer SHA256-only as a prospective release policy pending security review, **not** as a retroactive claim that old experiments failed. The trusted local Windows classic-PDB and single moniker origin boundary remains. Independent human reviewer assignments and evidence custody remain unresolved in #77.

**Final disposition:** CV-01 and CV-02 are **source-observed missing release controls**; CV-03 is a **source-observed absence of invocation/output binding with an untested replay failure hypothesis**. No new negative control has been executed, so none is a demonstrated runtime false-pass. Production release **BLOCKED**; legacy Gate C **UNSATISFIED**; Gate C-N release **NOT_AUTHORIZED**; production Source Link **HOLD**.
