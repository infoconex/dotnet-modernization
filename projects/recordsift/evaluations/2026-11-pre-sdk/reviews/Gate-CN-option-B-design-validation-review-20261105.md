# Gate C-N — independent cross-discipline review (2026-11-05 PT)

**Authority:** [Option B approved for design and validation only (#72)](https://github.com/infoconex/dotnet-modernization/issues/72). Tracking [#73](https://github.com/infoconex/dotnet-modernization/issues/73); [draft PR #74](https://github.com/infoconex/dotnet-modernization/pull/74) stacked on EXP-043 draft PR #71. This document is an assessment, **not a gate change or release approval**.

## Evidence independently checked

Primary native original physical compiler-source authentication is the earlier EXP-043 [CI 42173080423](https://github.com/infoconex/dotnet-modernization/actions/runs/42173080423) at `9fb67deeb2aa4c98587727abc01e8a11f01070b4`, artifact **13482117590**, ZIP SHA256 `5efcc9b1c872f85c926eeef4819135a2325d97668b2abdcdde4e21f4b7e14443`. Scope: frozen RecordSift SHA `8358780829458854a4b0356df5ac5e685f0a34c8`, 64/64 original physical inputs matching actual Csc structured TaskInput and native PDB source-key universes; 59 tracked + 5 generator-attested inputs; managed dnlib/Cecil identical 46 native line keys, 0/46 checksums exposed; 425 API, 419 NUnit (418 pass/one expected skip), five XML, local NuGet and clean consumer PASS. **Not re-executed** for Gate C-N.

New C-N work includes an externally reviewed fixed five-component scope, proposed normative specification, a **secondary metadata-only consistency checker** and synthetic controls. Initial [CI 42174806851](https://github.com/infoconex/dotnet-modernization/actions/runs/42174806851) passed 23 synthetic controls and verified the historical ZIP digest, run ID/head SHA and exactly three allowlisted metadata reports. The scope was then strengthened to pin per-assembly line and C13 record counts. Intermediate CI runs on `41f77473ac8c87c61dcaba36db6ab353f081d312` and `6aefe1d07ad83a67e4b7cf4917b687f81de136a6` **failed during synchronized schema/test edits**. This is research-harness/schema mismatch, **not** evidence of an application regression. Corrected execution `3dad98297bfbebbd278eecbee8d839070066cce9`: [Gate C-N CI 42175004526](https://github.com/infoconex/dotnet-modernization/actions/runs/42175004526) and [reusable tooling 42175004405](https://github.com/infoconex/dotnet-modernization/actions/runs/42175004405) both passed; **25/25 synthetic checks** pass; original authenticated sanitized reports internally consistent.

## Independent reviewer perspectives

| Lens | Findings and disposition |
| --- | --- |
| **Architecture** | Clear separation between original application, live compiler/PDB verifier, external scope manifest, secondary report checker, release contract and IDE gates. Existing live implementation has a frozen RecordSift/Windows net48 assumption; **generic application portability is not proven**. Conditional support for a scoped pilot protocol. |
| **Build and reproducibility** | Strong inherited EXP-041–043 original source-byte/Csc/PE-PDB provenance. The new report checker **cannot recompute physical bytes or per-document keys**, only corroborate aggregate assertions. Require actual live provenance execution for any future release gate. |
| **Security** | Trusted locally compiler-produced PDBs only; native parser not certified for hostile inputs. GitHub token only used for metadata and initial redirect; blob downloaded without token; redirect host validated; private signed redirect URL and temporary reports erased by an unconditional step. Polled process memory limit and firewall are not general hostile-PDB isolation. Artifact retention is short. |
| **Quality** | Twenty-five synthetic positive/negative controls including missing/duplicate components, changed original/Csc counts, wrong generated attribution, false full-key match, impossible C13 counts, tampered line counts, policy promotion, unexpected private metadata and duplicate JSON properties. They validate aggregate consistency, **not independent original-file provenance**. |
| **Release governance** | C-N proposal/secondary checks may advance to *research reviewed*, but cannot pass existing managed checksum Gate C, authorize NuGet VS project install, remote retrieval, debugger stepping, package publication, merge or production adoption. **No automatic acceptance gate substitution**. |

## Fresh-context independent review and corrective controls (2026-11-05 PT)

Actual GitHub Actions job steps and logs at `da35a4a125042623a0de95701facd84a23bbebde` confirm all **25/25** initial synthetic tests executed and the archived EXP-043 metadata check yielded `AGGREGATES_CONSISTENT_RESEARCH_ONLY`. This is not live PDB/source revalidation.

**Finding CN-R01 — medium, report false-positive:** original secondary checker accepted a coordinated tamper changing *both* readers from 0 exposed managed-document checksums to 1 exposed (and decrementing missing by 1) for a component. Counts still agreed, despite contradiction with the frozen original 0/46 observation. Corrective change: the external scope now pins `expected_managed_checksum_exposed: 0` for each of five components, the checker enforces it, and a coordinated-tamper negative test is added. This does **not** prove a checksum API works and does **not** satisfy legacy Gate C.

**Finding CN-R02 — medium, report privacy:** schema key allowlists alone allowed arbitrary strings in privacy/limitation/nonclaim fields and diagnostic status; a future faulty sanitizer could silently include path or source metadata in those fields. Corrective change: enforce actual original fixed public text and fixed-category diagnostic token patterns; add negative controls. These checks do not create a hostile-input security sandbox or replace auditing output bytes before upload.

**Finding CN-R03 — low/medium, external evidence identity:** previous workflow checked the archived artifact's embedded workflow-run metadata, but not a separately retrieved historical workflow run record. Corrective change: independently query GitHub's run endpoint and assert run ID, workflow ID, successful conclusion, actual SHA, event and repository; the artifact's recorded run and ZIP remain separately checked. GitHub and its trusted runner remain inside the trust boundary; run metadata alone does not prove every gate executed.

**Finding CN-R04 — low, test nomenclature:** prior aggregate tests labeled line-*count* changes as different source-*identity* cases. Names and comments now distinguish those; same-count/different-native-key integrity is independently tested only in the live EXP-043 implementation.

**Release-readiness blockers unchanged:** no independently signed immutable external manifest, no portable cross-application live verifier, no plan for 30-day-artifact expiration, no external reviewer signoff and no Visual Studio package/debugger tests. Future live C-N enforcement would require these review decisions and actual compiler/PDB verification, not just amended metadata.

**Evidence for fixes:** the new SHA and CI outcome must be appended after the changed branch is successfully executed. Neither the historical successful run nor this review alone proves the new controls passed.

## Remaining evidence limitations

1. A generally reusable **live** C-N verifier requires validated adaptation beyond RecordSift, including generated/external source origins, pathmaps, nonclassic PDB or unsupported readers, Csc task variants and third-party/COM compilation inputs; fail closed on unknowns rather than generalize the frozen result.
2. The secondary report checker cannot cryptographically authenticate original physical bytes or a compromised runner. Its success verdict is only `AGGREGATES_CONSISTENT_RESEARCH_ONLY`. Workflow separately confirms archived GitHub artifact/run/head/hash metadata, still within trusted GitHub threat boundary.
3. GitHub artifact **13482117590** has limited retention. Future automated replay must fail closed when expired; a separate archival or narrowly reproduced evidence decision would be needed. Durable manifests and evidence reports are linked in the research repository.
4. Complete Source Link remote-source integrity, authentic Visual Studio package-to-project installation and live debugger retrieval/stepping remain independent outstanding acceptance gates.
5. A **second explicit consolidated stakeholder decision** is required for actual Gate C-N release acceptance and disposition of existing managed Gate C; a further separate production authorization is required to deploy Source Link.

**Disposition:** Gate C-N **DESIGN / SECONDARY RESEARCH VALIDATION VERIFIED for frozen pilot**; release acceptance **NOT APPROVED**. Managed Gate C **UNSATISFIED**, production Source Link **HOLD**, PR #74 and parents **DRAFT/UNMERGED**, both main branches and RecordSift unchanged.
