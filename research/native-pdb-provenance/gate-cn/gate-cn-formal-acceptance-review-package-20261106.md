# Gate C-N — formal independent acceptance review packet (DRAFT)

**Prepared:** 2026-11-06 Pacific. **Authority:** stakeholder approved *preparation only* in [issue #73](https://github.com/infoconex/dotnet-modernization/issues/73#issuecomment-6680589160), tracked by [issue #77](https://github.com/infoconex/dotnet-modernization/issues/77). **Implementation:** [draft PR #74](https://github.com/infoconex/dotnet-modernization/pull/74), stacked on completed research PRs. **Review status:** AWAITING INDEPENDENT HUMAN REVIEW; **not** a signed assessment or approved release gate.

**Current disposition:** original managed-reader checksum Gate C **UNSATISFIED**; proposed native original-source Gate C-N **NOT AUTHORIZED FOR RELEASE**; Source Link **HOLD**; genuine Visual Studio NuGet project install, remote source retrieval and live stepping **NOT TESTED**. No research PR merge, no application/main branch edits, no publication.

## 1. Proposed decision and exact claim

Consider, after actual independent review and a **separate consolidated stakeholder decision**, whether to accept a **distinct narrow native-PDB original physical compiler-source provenance criterion** for trusted locally compiled traditional C# 7.3 / .NET Framework 4.8 applications using classic Windows PDBs. Evidence must connect **every externally enumerated required production compilation** to its exact immutable source revision, the actual Csc task-input identities, separately captured original physical bytes (before/after Csc), independently enumerated native PDB named/DBI/C13 document identities and real generated producer execution, with matching PE/PDB GUID+age, plus all existing original release compatibility checks.

This is **not semantically interchangeable with managed `ISymUnmanagedDocument.GetCheckSum`**. Native C13 `NONE` checksums remain noncryptographic, reader checksum exposure is unchanged, and no automatic Source Link/IDE adoption follows. Proving correct *local original compilation source provenance* is narrower than proving that a consumer can retrieve or debug remote source.

**Supported proposal v0.1:** locally produced *trusted* Roslyn classic Windows PDB, one explicitly witnessed `GenerateTargetFrameworkMonikerAttribute` generated input per component, all other compiler inputs Git-tracked and full-input identity matched, supported /SRC/FILES/ digest formats. Additional generators, dynamic/additional Csc tasks, external or untracked inputs, Portable PDBs, nonclassic native formats, ambiguous pathmaps or untrusted/hostile files default **BLOCKED** pending new externally reviewed contract and tests. Even within supported inputs, a live per-build verdict and all separately required release compatibility gates are mandatory.

## 2. Primary evidence (direct execution) and secondary evidence (claims only)

| Evidence class | Immutable primary run / scope | Retained audit / limitation |
| --- | --- | --- |
| EXP-043 real five-assembly RecordSift pilot | [42173080423](https://github.com/infoconex/dotnet-modernization/actions/runs/42173080423), source `8358780829458854a4b0356df5ac5e685f0a34c8`, research executor `9fb67deeb2aa4c98587727abc01e8a11f01070b4`; native documents **64/64** (59 tracked and 5 separately witnessed moniker sources), 46 line docs / 18 no-line docs. Full 425 API, 419 NUnit (418 passed, one expected skipped), five XML, local package, clean installed net48 consumer and candidate compatibility passed. | [Frozen external pilot scope](../../../projects/recordsift/evaluations/2026-11-pre-sdk/gate-cn-recordsift-scope.json), artifact 13482117590 (ZIP SHA256 `5efcc9b1c872f85c926eeef4819135a2325d97668b2abdcdde4e21f4b7e14443`), [native report](evidence/exp043-five-pdb-source-audit.json) and [two-reader report](evidence/exp043-managed-reader-exposure.json). Actual managed checksum bytes **0/46**, Gate C still UNSATISFIED. |
| EXP-044 real *different* traditional net48 fixture | [42182129657](https://github.com/infoconex/dotnet-modernization/actions/runs/42182129657), research executor `3c06d003ac75cc8b649a244be8705e44efa2c4c7`; actual PE/PDB, native named/DBI/C13, Csc physical bytes **2/2**, one tracked source and one genuinely generated moniker. Three pinned source-link package archives authenticated. | [EXP-044 frozen scope](gate-cn-exp044-evidence-scope.json), artifact 13486535447 (ZIP SHA256 `dcb76d42aeccfd2e9524ca347bf24e4678430ab4a52960331450e41f27aa2bf6`), [retained sanitized live report](evidence/exp044-non-recordsift-sanitized.json). Fixture does **not** prove RecordSift release/consumer contracts or arbitrary generators. |
| Research-only secondary checks | [Gate C-N run 42184120843](https://github.com/infoconex/dotnet-modernization/actions/runs/42184120843), 29 controls; 23 synthetic adapter controls. [EXP-044 replay 42184120895](https://github.com/infoconex/dotnet-modernization/actions/runs/42184120895), 12 controls. [Reusable Windows/Linux 42184120847](https://github.com/infoconex/dotnet-modernization/actions/runs/42184120847). | Original GitHub run identity and ZIP digests, allowlisted exact **public aggregate** JSON bytes and raw SHA256 compared to Git copies. Verdict only `AGGREGATES_CONSISTENT_RESEARCH_ONLY`. **No original compiler bytes or PDBs are available in these archives.** |

Historical GitHub workflow artifacts expire in December 2026. Retained public JSON is useful for **audit assertions only**; it is not a reusable proof that can be applied to a future or changed build. Historical failed experiments and their fixes (Windows original path spelling; Python Boolean/count aliasing; reader-exposure count tamper) are documented in [the readiness review](gate-cn-acceptance-readiness-review-20261105.md) and remain available for independent scrutiny.

## 3. Acceptance control matrix for independent reviewers

Each review must examine actual implementation and original workflow evidence. A check mark in an earlier AI-assisted evaluation is **not** a reviewer signoff.

| Control | Required independent review verification | Present evidence / open item |
| --- | --- | --- |
| CN-01 source and executor | Immutable application commit, clean checkout, exact executing workflow/validator/SDK/host identity; externally approved full compilation universe | EXP-043 and EXP-044 history verified; **independently signed, pre-build production manifest missing** |
| CN-02 PE/PDB pair | Actual candidate DLL PE CodeView GUID+age matches its native MSF PDB; fail closed on mismatch | Real pilot/fixture verified; no production acceptance runner |
| CN-03 native complete inventory | Full native named + DBI + C13 keys including line-less docs, record counts and supported algorithms; C13 `NONE` never treated as a digest | Five original RecordSift PDBs and second real fixture verified |
| CN-04 actual Csc invocation | Unique structured `Csc TaskInput Sources` and complete path identities; diagnostic text alone insufficient | Both primary runs verified; multiple/unknown invocations remain blocked |
| CN-05–06 original physical bytes | Snapshot each compiler-time input before Csc, verify unchanged afterward, check exact native SHA1/SHA256 bytes for every required source | RecordSift 64/64 and alternate fixture 2/2 verified; fresh per-build reexecution needed |
| CN-07 generated sources | Real generator target execution, output previously absent, exact physical identity and byte equality | Framework moniker only; external/extra generators blocked |
| CN-08 set equality | Full normalized native named/DBI/C13/Csc/captured-source identity equality, not just matching totals | Primary real verifiers; **archived aggregates cannot reproduce identities** |
| CN-09 managed-reader limitation | Exposed managed docs must be compared against actual native line-document set, including digest exposure as separate claim | 46 matched identities with **0 actual reader checksum values**; original Gate C still unmet |
| CN-10 original release contract | Original/candidate 425 API inventory, NUnit discovered/passed/skipped, five XML, assembly metadata/resources/dependencies, NuGet pack/install and clean net48 consumer, all tested against **candidate** binaries | Historical RecordSift pilot accepted; **each future production run must rerun**, and adapter does not currently enforce full release suite |
| CN-11 security/evidence custody | Pin packages and security advisories, trusted runner, strict parser/path bounds, negative controls, public report allowlist, cleanup, run SHA/artifact digest, independent custody/replay policy | Research privacy checks and ephemeral cleanup verified; **independent custodian/release revocation not selected** |
| CN-12 adoption gates (separate) | Genuine Visual Studio project Package Manager install, remote source delivery/source retrieval/stepping | **NOT TESTED**; cannot be asserted through Gate C-N |

**No acceptance by arithmetic:** `29 + 23 + 12` synthetic or replay tests cannot be counted as 64 live physical-source proofs or a release contract. Approval should require specific artifact and complete job/log references for every asserted control.

## 4. Reviewer packet assignments — all PENDING

Every named, authenticated reviewer must assess this packet and the [proposed normative standard](gate-cn-native-pdb-source-provenance.md) afresh. Their recorded judgment must include identity, organization/role, reviewed **exact Git SHA(s)**, evidence/run links, severity-ranked findings, rationale, residual risks and a signed/attributable final disposition. Authorship of research evidence alone does **not** constitute independent signoff.

| Reviewer capacity | Minimum independent work | Signoff / ownership |
| --- | --- | --- |
| Architecture / application | Review compiler/project universe, supported contracts and portability assumptions, separation of source-provenance from debugger claims | **UNASSIGNED — NOT SIGNED** |
| Build/reproducibility | Reevaluate actual MSBuild task-event capture, original snapshot timing, path identities, PE/PDB pairing, generated producer and pinned toolchain; approve pre-build application manifest | **UNASSIGNED — NOT SIGNED** |
| Security/privacy | Threat model trusted host/PDB, parser/escaping limits, private artifact handling, dependency pins/advisories, sanitizer and secure custody | **UNASSIGNED — NOT SIGNED** |
| Quality/test | Audit positive/negative controls, 425/419/5 and consumer gate coupling, candidate binary identity, false-pass tests | **UNASSIGNED — NOT SIGNED** |
| Release governance | Assign accountable approval authority, decide approved scope, custody/retention/revocation, legacy Gate C disposition and no automatic Source Link deployment | **UNASSIGNED — NOT SIGNED** |

A single person may only fill multiple capacities if the future approving authority **explicitly documents independence and conflict evaluation**; no implicit or fabricated signoff. Any unresolved critical/high finding, required-role vacancy, incomplete manifest/custody, absent original release gate or non-successful live attestation => **NO RELEASE ACCEPTANCE**.

## 5. Required reviewer deliverables and checkable disposition

Reviewers should deliver: (a) exact revision/case inspected; (b) control-by-control findings, evidence and exception inventory; (c) manifest and trust/custody protocol review; (d) independent assessment of release gates and negative-test coverage; (e) explicit `APPROVE_SCOPED_PROTOCOL`, `CONDITIONAL_CHANGES_REQUIRED`, or `REJECT`, with recorded personal identity and authority. `APPROVE_SCOPED_PROTOCOL` means review recommendation, **not** stakeholder gate activation.

All findings and exceptions must be resolved or explicitly accepted by the accountable stakeholder. No role may sign for another without actual authority. **No one has signed this packet yet.**

## 6. Open decisions and next step

1. **Named reviewers / signoff authority** — stakeholder must nominate or authorize independent architecture, build, security, quality, release reviewers.
2. **Evidence custodian** — choose a designated owner and tamper-evident retained public report/run/manifest approval policy, distinct from a mutable CI job; define operational freshness and revocation. See [manifest and custody proposal](gate-cn-manifest-custody-review-protocol-20261106.md).
3. **Exact production candidate scope** — approve which application/build targets and all original release gates are in scope; existing frozen RecordSift pilot is history, not a preauthorized production release execution.
4. **Later consolidated decision** — after reviewer signoffs, explicitly approve or reject a **narrow alternate release acceptance policy**, with separate disposition of managed-reader checksum Gate C. The decision must **not** infer approval of production Source Link or any IDE features.

See [unsigned review and decision record](gate-cn-independent-review-decision-record-20261106.md) for owner slots and future decision wording. **Current required outcome is `REVIEW_PREPARATION_ONLY`; no release activation.**
