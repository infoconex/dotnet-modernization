# RecordSift pre-SDK modernization — consolidated research review

**Assessment date:** November 3, 2026 (America/Los_Angeles)  
**Type:** Cross-PR, **research-only review** of existing evidence, not a new application experiment, migration implementation, or approval to merge.  
**Tracking:** [Documentation reconciliation issue #17](https://github.com/infoconex/dotnet-modernization/issues/17).  
**Application frozen baseline:** `infoconex/RecordSift` `main` and `research/dotnet-modernization` = `8358780829458854a4b0356df5ac5e685f0a34c8`.  
**Separate application release branch:** `release/0.2` = `338257f84a72a04136801aa93c3c435e28a61dce`.  
**Documentation base:** `infoconex/dotnet-modernization` `main` = `903629088e57ad081c512292c7fab4d9c72e4476`.  
**Source of record:** Existing experiment notes and associated GitHub Actions evidence, plus actual GitHub draft PR/branch comparisons and [evaluation methodology](../../../../methodology/evaluation-process.md), [evidence standards](../../../../methodology/evidence-standards.md), [evaluation decisions](decisions.md), and [roadmap](roadmap.md).

> **Review status:** Prepared for stakeholder disposition. No new application implementation, docs merges, package publication, SDK-style conversion, .NET migration, or integration of temporary experiment code is authorized by this report. The source PRs remain open and draft, and findings are not stakeholder-approved implementation decisions.

## Executive conclusion

**RecordSift can gain useful pre-SDK maintainability improvements without changing framework, project format, architecture or runtime.** The strongest low-risk candidate is consolidating `LangVersion=7.3` into a minimal conditional `Directory.Build.props`, using the existing traditional import chain. This has actual build/test/API/documentation/packaging evidence; no early `Microsoft.Common.props` import is necessary or recommended. The value is a *single authoritative setting across ten currently identical projects* while retaining local overrides. **Nothing is approved for implementation.**

A new `Directory.Build.targets` would have no demonstrated repeated build behavior to centralize. `WarningLevel=4` centralization is possible only when original Debug/Release configuration semantics are preserved; because C# level 4 is already the compiler default, this is **optional, lower priority**. Adding a repository `global.json` is compatible with the verified formatter and builds, but whether pinning is worth the SDK provisioning burden is an **operations decision**, not a must-have modernization step.

**SDK-only Windows build/test and an adapted release/clean-consumer path are technically feasible without Visual Studio Build Tools**, but original Windows PowerShell/NuGet/consumer scripts still have portability assumptions. This evidence **does not justify replacing stable VS-backed release CI** without an operational need and separately approved script changes.

The manually constructed, **exact-pinned** `PackageReference` conversion was proven in the *disposable test workspace* while retaining traditional .NET Framework 4.8 projects. It is **not required before SDK-style conversion**, not equivalent to the Visual Studio migrator wizard, and **not a pre-SDK recommendation to implement immediately**. Removing nine likely-transitive declarations selected **four older dependency versions despite passing all 419 NUnit tests**, so conversion and dependency cleanup must be separate decisions. The existing verification scripts couple to `packages.config`, and the NUnit console path is legacy-format-specific.

**Critical documentation integration defect:** eight unmerged drafts reuse two finding IDs and update the same status/roadmap/evidence/decision files independently. Integrating by simply taking the latest version of each shared file would silently **discard** findings or overwrite historical partial outcomes. See the concrete reconciliation plan below.

## Verified repository and PR state

GitHub state checked November 3, 2026. All eight research PRs are **open and draft**, target `dotnet-modernization/main` at the same original base SHA, and contain **documentation-only** changes. No draft has been merged.

| Draft | Main focus | Review evidence and disposition |
|---|---|---|
| [#4](https://github.com/infoconex/dotnet-modernization/pull/4) | Shared `Directory.Build.targets` source audit; governing P-012 research-only boundary | **Source audit:** 0 custom build targets/tasks and no repeated per-project target behavior across ten projects. **Do not add** targets merely for consistency. PR is also the only reviewed draft that records **P-012**, which must not be lost in integration. |
| [#5](https://github.com/infoconex/dotnet-modernization/pull/5) | 19 unique declared property names; ten `LangVersion`, twenty `WarningLevel` elements | **Source inspection** and prior EXP-002/005/006 execution; propose only minimal conditional `LangVersion` first. D-009's *unverified WarningLevel* label is historical and must be updated with EXP-010 before any consolidation. |
| [#6](https://github.com/infoconex/dotnet-modernization/pull/6) | **EXP-008** pinned `global.json` / actual IDE1006 formatter | [Run 41681192996](https://github.com/infoconex/RecordSift/actions/runs/41681192996): **10.0.403** and **10.0.303** pins, formatter, ten-project build, 419 NUnit, XML/API pass. **Compatible, adoption optional**; packaging/consumer under both pins not tested. |
| [#8](https://github.com/infoconex/dotnet-modernization/pull/8) | **EXP-009** SDK-only Windows release/clean-consumer portability | [Run 41708730067](https://github.com/infoconex/RecordSift/actions/runs/41708730067): modified *temporary copies* of scripts passed UTF-8 notice checks, ZIP XML extraction and SDK Roslyn-compiled/executed installed-package consumers. **Original scripts still fail unmodified**; negative CS1591 in SDK-only host **not executed**. |
| [#10](https://github.com/infoconex/dotnet-modernization/pull/10) | **EXP-010** scoped common `WarningLevel=4` | [Run 41713886548](https://github.com/infoconex/RecordSift/actions/runs/41713886548): 20/20 Debug/Release evaluated values, overrides, Debug/Release builds, 419 tests, 425 API, package/consumer and CS1591 pass. Unconditional property also sets otherwise blank `Custom` configuration; **only scoped default preserves tested property semantics**. Lower priority. |
| [#12](https://github.com/infoconex/dotnet-modernization/pull/12) | **EXP-011** legacy NuGet graph and assets | [Run 41728933974](https://github.com/infoconex/RecordSift/actions/runs/41728933974): 7 `packages.config`, 17 entries, 13 unique/restored package IDs, 11 production `.nuspec` exact dependencies, all 13 restored `HintPath` DLLs. **Inventory verified**, but true migrator classification or PackageReference resolver not yet tested at this stage. |
| [#14](https://github.com/infoconex/dotnet-modernization/pull/14) | **EXP-012** exact-pinned PackageReference then direct-only control | [Run 41735278846](https://github.com/infoconex/RecordSift/actions/runs/41735278846): 17 exact PackageReferences in seven traditional net48 projects, restore/build, 419 NUnit, **414 compiled API+identity** records, XML, unpublished package/consumer and CS1591 pass. The **unchanged 425-entry verifier fails** on 11 removed raw package records; NUnit runner installed separately. Direct-only drops nine refs and **downgrades four versions** despite passing build/tests/API; direct-only consumer **not tested**. |
| [#16](https://github.com/infoconex/dotnet-modernization/pull/16) | **EXP-013** migration tools and existing CI behavior | [Run 41737816926](https://github.com/infoconex/RecordSift/actions/runs/41737816926): **unchanged `nuget restore` and IDE1006 formatter pass** on converted projects; existing package audit fails on removed configs, a temporary exact-pin audit passes 17/17, and a temporary format-aware XLSX architecture guard **passes positive and rejects removal** of `ExcelDataReader`. GUI migrator **not executed**. |

**Earlier experiments still matter:** EXP-001 baseline 419 discovered / 418 pass / 0 fail / 1 skip and 425 API/metadata records; EXP-002 common `LangVersion`; EXP-003 Framework SDK Windows container **contains** VS Build Tools; EXP-004 SDK-only without Build Tools; EXP-005 overrides; EXP-006 import-order failure (MSB3107); EXP-007 historical SDK-only release validation **partial**. The later EXP-009 result is complementary, not a retrospective rewrite of the EXP-007 run.

**Source verification:** RecordSift `release/0.2` is exactly one commit ahead of app `main`. Previously approved and merged **[RecordSift PR #258](https://github.com/infoconex/RecordSift/pull/258)** added the missing XLSX assembly to `scripts/run_tests.ps1` **on that release branch**, alongside a related CI change and `AGENTS.md`. The frozen `main` baseline's local runner still omits XLSX. **Do not implement the same fix twice or assert it is already on main**. This change is separate from all research branches.

## Integrated evidence outcomes, limitations and priorities

Legend: **Verified** means the named checks actually ran or the source was inspected. **Not executed** is never inferred to pass. Priority is a **proposal for stakeholder review**, *not* a permission to implement.

| Subject | Outcome / bounded verification | Proposed value and action | Priority |
|---|---|---|---|
| Historical contract and local all-five-suite runner | Baseline 419/418/0/1; main local runner omitted XLSX. Corrected in separate `release/0.2` PR #258, not main. | **Recognize existing fix** and confirm intended branch promotion separately when appropriate; avoid recreating/merging from research. | **P0 release-branch disposition**, not a new experiment |
| Shared `LangVersion=7.3` in `Directory.Build.props` | **EXP-002/005 verified** no change to tested build/NUnit/API/XML/package and override behavior. Existing traditional import chain adequate. | **Primary low-risk pre-SDK candidate**: one place for ten identical settings, project override permitted. Require explicit implementation approval and current SHA/full gates. | **P1 (if implementation authorized)** |
| `Directory.Build.targets` | Source audit #4 verified no reusable target action; EXP-006 established import mechanism. | **Do not add** without actual shared behavior to enforce. | No change |
| Early `Microsoft.Common.props` import | EXP-006 **MSB3107 regression**. | **Avoid** changing imports just for central defaults. | No change |
| Remaining MSBuild settings | Property audit of 19 names; shared target/output/Debug/Release/compiler/XML settings carry import, identity or verifier risks. | Leave framework, output, identifiers, per-config flags, XML/CS1591 and resources local. | No change |
| Shared `WarningLevel=4` | EXP-010 verifies scoped Debug/Release/property override compatibility; unconditional root setting broadens `Custom` property. | **Optional**, reduced priority versus `LangVersion`; default C# level already 4. | P3 optional |
| `global.json` / SDK selection | EXP-008 actual IDE1006, build, test, XML/API passes under pins 10.0.303 and 10.0.403. | Compatible; **only add if reproducible local/CI tool selection provides operational value**. Explicit SDK installation then required. | P2 conditional |
| Windows SDK-only developer environment | EXP-004 build/test verified without VS Build Tools; ref assemblies, NuGet CLI explicitly required. | Optional documented developer/CI path; preserve Windows/net48 requirements. | P2 conditional |
| SDK-only package/consumer path | EXP-009 **adapted** UTF-8 notice validation, `NUGET_XMLDOC_MODE=none` and SDK Roslyn consumers passed. **Original scripts fail**; SDK-only negative CS1591 not run. | Avoid release pipeline rewrite without need; targeted script portability changes only under approval and then rerun full gates. | P3 optional |
| Legacy NuGet inventory | EXP-011 exact source/nuspec/restored graph and 13 DLL HintPaths verified. | Keep baseline evidence; no automatic package update. | Documented |
| Exact-pinned `PackageReference` on traditional net48 | EXP-012/013 17 exact pins, build, 419 NUnit, 414 compiled API/identity, XML, local package/clean consumer, CS1591 pass; original full 425 gate fails due 11 raw source lines. | **Feasible independent of SDK conversion** but requires validator and test-runner migration; no immediate business need established. | P3 separate future project |
| Direct-only `PackageReference` simplification | EXP-012 drops nine refs: `System.Memory 4.5.5→4.5.0`, `Unsafe 6.0.0→4.5.3`, `System.Buffers 4.5.1→4.4.0`, `System.Numerics.Vectors 4.5.0→4.4.0`, while tests/API still pass. | **Do not combine** dependency cleanup with format conversion; versions need separate review and consumer/binding-redirect checks. | P4 independent risk review |
| Existing CI after PackageReference | EXP-013 **unchanged NuGet CLI restore and `dotnet format` pass**. Raw package audit and API checker fail; NUnit runner depends on `packages/`; architecture validator needs explicit vendor `PackageReference` recognition. Temporary vendor guard positive + negative checks pass. | If migration ever authorized, adapt **only needed** guards and provisioning; do **not** replace working restore/formatter needlessly. | Prerequisites to P3 |
| Documentation Python source validators | EXP-013 both fail on generated `obj/**/*.cs` **even after original-format Windows build**; after cleanup `validate_core_messages.py` passes. XLSX guard still rejects converted source until format-aware fix. | Independent guard robustness improvement if docs/workflows ever run post-build. Current main Ubuntu docs workflow operates separately on clean checkout. Do not label as a PackageReference regression. | P2 conditional |
| SDK-style project conversion / .NET runtime change | **Not executed / not authorized** in this evaluation. | Separate evaluation, baseline, resource/assembly identity analysis, and approval. | Out of current scope |

## Documentation reconciliation defects to resolve before any merge

### Finding-ID collisions — do not overwrite content

**Two current draft branches assign the same IDs to unrelated findings:**

| ID | Existing draft owner | Conflicting draft owner | Proposed canonical disposition |
|---|---|---|---|
| `F-019` | [PR #4](https://github.com/infoconex/dotnet-modernization/pull/4): **targets audit** | [PR #8](https://github.com/infoconex/dotnet-modernization/pull/8): SDK-only notice encoding | Keep **F-019 = targets audit**; reassign SDK-only encoding to **F-022** in eventual integrated findings table. |
| `F-020` | [PR #5](https://github.com/infoconex/dotnet-modernization/pull/5): **19-property inventory** | [PR #8](https://github.com/infoconex/dotnet-modernization/pull/8): SDK-only clean-consumer and VS dependency | Keep **F-020 = property inventory**; reassign SDK-only consumer to **F-023**. |

**Other unique IDs:**
- Keep **F-001–F-018** from the merged historical main record (including EXP-007's partial diagnosis, not silently revised).
- Keep **F-021** from [PR #6](https://github.com/infoconex/dotnet-modernization/pull/6) for global.json/formatter verification.
- **Proposed only** new unique IDs if an integrated findings table is approved: **F-024** scoped WarningLevel, **F-025** pinned legacy dependency inventory, **F-026** exact-pins PackageReference parity with unchanged-checker caveat, **F-027** four transitive-version downgrades, **F-028** unchanged NuGet restore/IDE1006 and changed package audit, **F-029** XLSX architecture guard positive/negative, **F-030** generated-obj validator build-order issue. These are reservation suggestions, **not inserted into the existing draft PRs**.

**ID policy:** do not reuse an assigned finding ID merely because it resides only in an unmerged branch. Reconcile and verify IDs against all reviewed PRs before integrating. Original experiment documents retain their own immutable experiment ID and historical outcomes.

### Other shared-file overlaps and stale statements

All eight drafts share the **same base main SHA** and independently update common files; accepting a branch's latest version may discard rows from the others. The overlapping files include `status.md`, `roadmap.md`, `risks.md`, `experiments/README.md`, `evidence/manifest.md`, and for early PRs `findings.md` / `decisions.md`. This is a **manual content-reconciliation requirement**, not merely a Git line-conflict problem.

| Canonical section | Consolidated correction (proposal, no committed integration) |
|---|---|
| **Stakeholder decisions** | Preserve **P-001–P-011** including P-011's accepted strict-acceptance-evidence limitation, and incorporate **P-012** research-only/branch boundary recorded in PR #4. The latter must not be discarded by PR #5/#6 branches based on an earlier decisions version. Do **not** reinterpret old pilot approvals as modernization implementation approval. |
| **D-001** | Note correction already merged into RecordSift **release/0.2** via PR #258, still absent from app main. Distinguish branch status from recommended action. |
| **D-002 / D-003** | Align with PR #5 conditional LangVersion recommendation and PR #4 no-targets recommendation. No early MSBuild import. |
| **D-005 / R-001** | EXP-009 **corrected positive SDK-only release path verified**; original validators **still fail unchanged**, and SDK-only **negative CS1591** remains untested. Keep historical EXP-007 recorded as *partial* and add new evidence instead of overwriting its outcome. |
| **D-006 / R-008** | The sentence “defer PackageReference **to SDK conversion**” is no longer a technical dependency: EXP-012 executed it separately in traditional net48. Reframe as **optional and unapproved**, with confirmed version-drift hazard, required audit/API/runner/architecture adaptations and consumer gates. Central package management is not needed during legacy `packages.config` use. |
| **D-007 / R-003** | EXP-008 **did execute** the exact current IDE1006 formatter under two pinned SDK versions. Mark **compatibility verified**, **adoption optional**, not “formatter untested”. |
| **D-009 / D-010** | PR #5 proposed a WarningLevel experiment as unverified; **EXP-010 verified** scoped conditional approach but found modest value. Preserve per-project/conditional/identity/resource settings unless independently justified. |
| **R-007 / status** | Historical local-runner defect in frozen app main but correction **already on release/0.2**; avoid double work. |
| **Python source guard risk** | New distinct documented finding: generated `obj` C# causes false positives after both original-format and migrated Windows builds; separately, XLSX source guard requires a format-aware vendor dependency check. Distinguish these two causes. |
| **Evidence manifest** | Retain all previous EXP-001–007 runs, append **EXP-008–013**, evidence artifact IDs, immutable workflow SHAs and negative-control caveats. All run artifacts eventually expire; essential claims and commands belong in durable Markdown. |
| **Roadmap / experiment index / status** | Union all new candidate outcomes; preserve the historical 34 candidate rows and six workstreams. Reclassify “not executed” only when a named experiment has actually tested that exact claim, not by inference. |

### Proposed integration approach — only after stakeholder approval

1. **Review this consolidated evidence and the eight source draft PRs** with the owner. Clarify which findings and recommendations should enter the authoritative methodology/evaluation and which are historical detail. This review is **not** permission to implement RecordSift changes.
2. After separate explicit **documentation integration approval**, create a dedicated short-lived **docs-only integration branch from current `dotnet-modernization/main`**; import each **unique** EXP-008–EXP-013 experiment document. PR #4/#5 source audits live primarily in shared documents; preserve their distinct content during manual reconciliation.
3. Build **one canonical** `findings.md`, `decisions.md`, `status.md`, `risks.md`, `roadmap.md`, `experiments/README.md`, and `evidence/manifest.md`. Resolve F-019/F-020 collisions and P-012 governance, stale D/R outcomes, and link paths **as a single consistent reviewable change**. Do **not** merge eight independent shared-file rewrites in arbitrary order.
4. Run documentation quality checks (internal links, source citations, experiment numbering, 34-row roadmap completeness, unique F/D/P/R IDs, branch/commit/run evidence, no fabricated performed tests, and consistency of 'research complete' vs 'implemented'). No application build is required for a **docs-only** integration, but a new implementation would require a new application baseline and complete gates.
5. Present the eventual integration diff for review **before any merge into docs main**. Close/supersede the eight overlapping drafts only with explicit approval, preserving links to the original experiment submissions and all failed-harness evidence.

**This report does not create the integration branch or modify any existing draft.** It documents the steps and decision boundary for later review.

## Outstanding questions and evidence still not established

- **Actual Visual Studio migration wizard output:** Not executed. Its top-level/transitive classification, backup and conflict report cannot be inferred from our manual full-exact-pins and heuristic direct-only experiments. If desired, approve a separate Visual Studio IDE comparison; do not call that mandatory pre-SDK work.
- **SDK-only Windows CS1591 intentional-negative release check:** Not executed in EXP-009. Successful negative CS1591 under a **VS-backed** runner in other experiments is not the same evidence. The original SDK-only release scripts still fail unmodified.
- **Direct-only dependency graph independent consumer:** Not executed; restoring/building/passing tests/compiled API does **not** approve the four observed downgrades or package publication. Check version/binding redirects and installed consumer only if intentionally pursuing that variant.
- **.NET Framework 4.8.1 supported image pull/runtime:** Previously deferred, not executed. Historical 4.8 SDK tag used in EXP-003 was cached and had VS Build Tools; do not claim a contemporary SDK-only container from that run.
- **More general Debug/custom-configuration and host parity:** Scoped WarningLevel evaluated representative `Custom` properties but did **not** compile arbitrary custom configurations. No claim of Linux support for net48. SDK pin package/consumer gates weren't tested under both versions in EXP-008.
- **Architecture and code coverage:** 419 NUnit cases verify accepted test suites but do not prove exhaustive coverage, production security, performance or dependency upgrade compatibility.
- **Integration permission:** P-012 permits research and review branches, **not** merging docs or app changes, releasing packages, or making migration decisions for the owner.

## Review decisions requested from the stakeholder

The review can be accepted without approving any application changes. Suggested separate decisions, **not yet approved**:

- **Documentation disposition:** approve or revise the proposed unique finding-ID mapping and content reconciliation plan, then separately authorize creation/review of a docs-only integrated PR.
- **Immediate modernization priority:** decide whether the already-proven minimal conditional `LangVersion` consolidation is valuable enough to authorize as a future independent application change. Do **not** assume approval from experiments.
- **Optional toolchain choices:** decide whether `global.json` or SDK-only Windows tool independence solves a real developer/CI problem, or whether to **leave existing verified CI alone**.
- **Deferred migration choices:** decide whether future `PackageReference` conversion or the GUI migrator comparison warrants any immediate work; evidence permits deferring them until a well-scoped SDK-style conversion project.
- **Existing test-runner fix:** explicitly recognize the approved `release/0.2` state; any promotion to application main remains a separate release/source decision.

**Current recommendation:** resolve the documentation record first, choose at most one small application improvement at a time *after explicit approval*, and keep conversion/runtime modernization as separate future evaluations. No new exploratory runs are justified merely to fill a list of configuration files.

---

**Provenance and integrity:** source applications and documentation branches were inspected via connected GitHub, not modified by this review other than this new review-only document/branch. Runs cited are from existing experiment reports, not newly repeated. Artifact retention is limited; supporting reports contain necessary setup/probe details. This document is a synthesis and proposed review plan, not a declaration of accepted implementation or of a merged repository state.
