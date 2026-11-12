# EXP-043 independent engineering review — proposed native-PDB provenance alternative

**Review:** November 5, 2026. **Status:** review and recommendation only; NOT stakeholder acceptance, production approval, or replacement of managed checksum Gate C.
**Application:** RecordSift frozen at `8358780829458854a4b0356df5ac5e685f0a34c8`.
**Research:** EXP-043 issue #70, draft PR #71, stakeholder issue #72, parent issue #37.
**Executing evidence:** [CI 42170182029](https://github.com/infoconex/dotnet-modernization/actions/runs/42170182029) at `d261572a4f02e94f83897eb94d056681d5cf6d55`; sanitized artifact **13479814833** with ZIP SHA256 `b0b23a78e8b0e1227631a25e9a3f975dbca4dbb8ae97f8b52d6aea463405a7fc`. Both Windows and Ubuntu jobs completed successfully.

## Independent record check

Downloaded the original sanitized ZIP, checked the actual ZIP SHA256, listed all **three** JSON files, inspected all per-assembly counters, inspected the PR source, Windows/Ubuntu job logs and frozen application packaging script. Independently confirmed the following values in the artifact, rather than relying solely on PR prose:

| Production component | Native named/DBI/C13 identities | Physical source matches / Csc identities | Managed identities (both readers) | Exposed checksums |
| --- | ---: | ---: | ---: | ---: |
| Domain | 24 | 24 / 24 | 20 | 0 |
| Application | 23 | 23 / 23 | 16 | 0 |
| Infrastructure.Csv | 7 | 7 / 7 | 4 | 0 |
| Infrastructure.Reporting | 7 | 7 / 7 | 5 | 0 |
| Infrastructure.Xlsx | 3 | 3 / 3 | 1 | 0 |
| **Total** | **64** | **64 / 64** | **46** | **0** |

There are **59** Git-tracked and **five** separately generator-attested framework-moniker inputs, **18** native documents not surfaced by either reader, and **72** C13 checksum records with algorithm `NONE`. These are **per-assembly document identities**, not 64 distinct physical files globally. Native injected SHA256 source records were matched against independently captured compiler-time physical bytes; the `NONE` C13 records cannot themselves authenticate bytes. Diagnostic-text Csc parameter reconstruction is **incomplete** and was not the accepted source set: actual structured TaskInput/Sources events were used.

The Windows log corroborates source/provenance checks and existing release gates, including 425 public API entries, 419 NUnit tests (418 pass, one expected skip), five XML documentation outputs, unpublished NuGet package, clean installed net48 consumer and five compatibility categories. The frozen `scripts/build_release_candidate.ps1` **stages existing Release DLLs/XML**, rather than overwriting candidate DLLs by recompilation. The EXP-043 script copies matching candidate production DLLs to test assembly output directories before running EXP-014. These facts reduce the risk of a false-positive baseline-only test run; none prove authentic Visual Studio host behaviors.

## Review lenses

- **Architecture:** research-only, disposable instrumentation separated from original application and public package; five production assemblies inventoried. No new application dependency or change to the frozen commit. Valid reusable technique, but readers that reduce documents to basenames reject duplicate-basename projects: document this as a portability precondition, not a universal capability.
- **Build and reproducibility:** actual Csc TaskInput source identities, independent compiler-time physical-byte captures, generated producer execution and paired native PE/PDB references provide a strong *build-provenance* argument. The same CI host still participates in several observations: this is independently checked evidence within a trusted host, not an adversarial build-host-compromise proof. No globally deterministic compiled-byte claim.
- **Security:** source/URL/byte/PDB data are private and erased; retained artifact has fixed metadata only, verified by ZIP inspection. Pinned dnlib/Cecil archive and DLL hashes, limited processes and outbound executable firewall rules are favorable. The 256-MiB process check is **polled**, not an OS-enforced hard sandbox; executable firewall rules and a native-module check do not qualify parsers for hostile symbols or a compromised host.
- **Quality:** explicit five-suite compatibility, candidate copy-local checks and ten additional passing controls. Remaining targeted item: **identity equality of managed document sets and native C13 line-reference sets** was not asserted by the original EXP-043 comparison. Equality of counts (46) alone is insufficient to say that the exact 18 missing documents are the ones without lines. An added fail-closed assertion and a same-count/wrong-identity synthetic negative control are committed on draft PR #71. **Do not attribute their execution to the original CI SHA/artifact.** Require a new successful workflow and sanitized result before upgrading this exact-set assertion to VERIFIED.
- **Release governance:** existing managed-reader original-document checksum **Gate C UNSATISFIED**; Source Link production **HOLD**; neither original artifact nor this review approves an alternative gate or merging PRs. NuGet CLI/local-feed installation is not authentic Visual Studio Package Manager project installation. Real Visual Studio debugger source retrieval and stepping have not been exercised.

## Decision options for stakeholder issue #72

| Option | Independent assessment | Consequence |
| --- | --- | --- |
| **A — Preserve existing managed checksum Gate C** | Valid conservative default **until explicitly changed**. | Maintain HOLD; investigation of supported managed-symbol APIs could remain blocked even though native physical-source provenance is strong. |
| **B — Authorize design of a separate, explicitly bounded native provenance gate** | **Recommended for stakeholder consideration**, conditional on targeted identity check and independently approved protocol. | Preserves original behavior contracts while allowing native proof of original compiler-source provenance *as an alternative evidence method*, **not** proof of real IDE functionality or blanket production approval. |
| **C — Orthogonal targeted experiment** | Appropriate only for a concretely identified supported-symbol API, patched reader, authentic VS package/IDE host or other objective independent missing evidence. | More effort and possibly blocked by unavailable/suspect native tooling; do not repeat EXP-039–043 without a specific gap. |
| **D — Stop traditional Windows-PDB Source Link adoption** | Defensible if actual IDE acceptance is infeasible or policy requires the original API criterion. | Preserve the methodology and evidence, consciously retain HOLD. No evidence forces this choice yet. |

### Proposed B protocol, NOT YET APPROVED

1. Distinguish **native original-source provenance acceptance** from any existing *managed reader API* requirement. Record a separately named provisional `Gate C-N` with explicit scope, owner, approval date and threat model; until approval, `Gate C` remains UNSATISFIED.
2. Require immutable application revision, paired PE/native PDB GUID+age, **complete** named/DBI/C13 per-assembly source-identity universe, full matching structured actual Csc Sources set, pre/post compiler-time bytes, cryptographic native named checksums verified against those independent bytes, explicit unknown algorithm/duplicate/pathmap/unsupported input failures and generated producer proof. Do not infer a path from the PDB key.
3. Require **exact key-set identity**, not merely counts, for any claimed correlation between managed readers and native C13 line records. Require negative controls and confirmation on the actual frozen assemblies. Any unexpected native/managed mismatch remains explicit, not silently accepted.
4. Retain original API, NUnit, resources/assembly identity, XML, packaging and clean installed net48 consumer gates. New tests/validation must compare actual candidates and report first failures.
5. Bound to trusted local compiler output; security-review parser input bounds, dependency authenticity and advisories, failure sanitization, artifact upload paths, cleanup on failure and evidence retention. Record that host compromise and malicious PDBs are out of scope unless separately mitigated.
6. Verify Source Link mappings and remote original-source bytes, including any production sources not already covered by previous CSV-only remote provenance experiments, before asserting end-to-end source retrieval. Do **not** infer remote availability from local Git tracking or native record hash alone.
7. Keep **separate, unsatisfied IDE gates** until authentic Visual Studio package-to-project installation and real debugger source retrieval/stepping with positive and negative controls execute. A command-line consumer or simulated package install does not satisfy them.
8. Require an independent security/build/quality/release review, written stakeholder approval of this exact protocol, and a separate later production deployment decision. Preserve draft PRs and HOLD until approvals.

## Disposition

**Recommended stakeholder choice: conditional B, while A remains effective by default.** The evidence supports an independently checkable *provenance* substitute in principle, not an equivalence claim about managed reader APIs or Visual Studio's debugger. Complete the newly identified exact-set control and obtain explicit consent before amending any approved policy. **No option has been selected and no gate has been changed by this document.**

Follow-up: await the new execution/result of the targeted equality guard; evaluate exact native-versus-managed C13 identity sets. Keep other completed EXP-001–043 investigations closed unless new independent evidence requires focused work.
