# Consolidated modernization preparation decision matrix — November 5, 2026

**Status: DOCUMENTATION / INDEPENDENT ASSESSMENT ONLY. No application implementation, research merge, package publication, or Source Link approval.**

Application: `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8` (traditional ten-project net48, C# 7.3, `packages.config`). Research base: [EXP-035 draft PR #52](https://github.com/infoconex/dotnet-modernization/pull/52) head `3d4108d34da091bb4b6342792cf564b91a0fb57e`. Research main when independently checked: `484f25b1f894f85cdfddf133446a6ea34ae39af2`. [Tracking issue #37](https://github.com/infoconex/dotnet-modernization/issues/37). This matrix synthesizes observed experiments, not a list of granted permissions.

## Fixed acceptance contract

Full Windows Release builds of ten projects; public API **425 existing entries** including the established package metadata policy; **419 NUnit discovered / 418 passed / 0 failed / 1 expected skipped** across all five test assemblies; five XML-doc checks; assembly/resource identity and all five established logical compatibility components; unpublished local NuGet package, original distributable dependencies, and independently installed clean net48 consumer. No unintended runtime, API, behavior, reference, or dependency changes. A format-aware alternative to the original 425-entry policy needs **separate explicit acceptance**; the 414 compiled-member subset alone does not clear it. The frozen `main` local test script omits XLSX; the fix on `release/0.2` (RecordSift PR #258) is **not** on frozen `main`.

Evidence types are kept separate: source declaration, evaluated property, loaded host assembly, compiler argument, produced binary, PDB structure, remote bytes, project installation, debugger operation, and clean consumer. Successful CI alone never promotes an untested dimension.

## Experiment coverage / evidence crosswalk (EXP-001–035)

Reference the [individual experiment reports](experiments/README.md) and [permanent manifest](evidence/manifest.md) for run identifiers, failed controls, and precise boundaries. “Verified” below is strictly **the reported experiment's scoped claim**, not full modernization acceptance.

| EXP | Scope and strongest supported disposition | Limitation / distinction |
|---|---|---|
| 001 | **Verified** original solution, Windows build and NUnit baseline | Main test script has five-suite discrepancy |
| 002 | **Verified** conditional LangVersion shared property behavior | Not a permanent application change |
| 003 | **Verified** Windows Framework SDK image with Build Tools | Historical image/tag; environment-specific |
| 004 | **Verified** SDK-only Windows build and all five test suites | Full original release scripts not demonstrated |
| 005 | **Partially scoped / verified controls** SDK versions and per-project property overrides | Not a blanket SDK-selection guarantee |
| 006 | **Mixed** import/targets proofs; early Common.props caused MSB3107 | Reject early import pattern |
| 007 | **Partially verified** SDK-only Release/API/XML/pack work | Original validator/consumer issues persisted |
| 008 | **Verified** exact SDK pins for formatter/Release/test/API/XML | SDK provisioning and governance still needed |
| 009 | **Verified** corrected SDK-only positive release/clean-consumer path | Original scripts fail unchanged; negative CS1591 not run |
| 010 | **Verified** scoped WarningLevel controls and Release gates | Unconditional global setting changes Custom behavior |
| 011 | **Verified** NuGet declarations/restore and HintPath inventory | Configured feed is not historical acquisition origin |
| 012 | **Partially verified** exact-pinned PackageReference candidate; compiled API/test pass | Original 425-entry metadata gate fails; direct-only graph drifts |
| 013 | **Partially verified** migration tooling/format-aware guards | Visual Studio GUI migration and full future CI not tested |
| 014 | **Verified** real immutable binary metadata baseline | Same-source baseline is not migration candidate |
| 015 | **Verified** independently built LangVersion candidate compatibility | Not byte-for-byte identity |
| 016 | **Verified** intentional enum-break negative-control detection | Tool proof, not acceptance of breaking change |
| 017 | **Verified** package/member-byte differences, including same-source variation | Not proof source change caused every byte change |
| 018 | **Verified** same-source PE/MVID drift with IL-token parity | Build was not yet hermetic |
| 019 | **Verified** same-root deterministic DLL equality; cross-root unequal | Property value not final Csc argv observation |
| 020 | **Verified** PathMap + deterministic 5/5 cross-root DLL equality and wrong-map negative | Must preserve source/path semantics |
| 021 | **Verified failed control** global ContinuousIntegrationBuild with missing SourceRoot | Do not enable globally without valid roots |
| 022 | **Verified** bounded manual SourceRoot bridge/controls | Does not establish genuine provider/source retrieval |
| 023A/B | **Verified** official Source Link archive/asset metadata and dependency preflight | Not authentic IDE project installation or loader proof |
| 024 | **Verified** manual isolated tool imports, build, original compatibility | Not NuGet project installation |
| 025 | **Verified** actual Windows PDB Source Link JSON/PE identity | No source-step or managed checksum claim |
| 026 | **Verified** byte-identical DLL **and native PDB** from independent worktrees | Bounded to CSV candidate |
| 027 | **Verified** actual NuGet CLI net48 closure: four potential pin conflicts | `nuget install` is not IDE project installation |
| 028 | **Verified** one PDB URL to immutable Git blob; CRLF distinction | Single source only |
| 029 | **Verified** LLVM native file listing; five rows with no visible checksum | Managed document checksum authenticity **inconclusive** |
| 030 | **Verified** real shallow/remote-free/submodule positive/negative controls | Green build does not guarantee Source Link data |
| 031 | **SECURITY-BLOCKED** vulnerable/unavailable patched native reader | No native checksum execution |
| 032 | **Verified scoped** MSBuild AppDomain module loading/isolated tasks | Other nodes and IDE installation unobserved |
| 033 | **Verified** separate LLVM C13 view without text checksum markers | Not proof of complete absence |
| 034 | **Verified** all four independently LLVM-listed owned CSV URL/blob matches | Not full managed document inventory |
| 035 | **Verified** signed VS DIA SDK C++ execution, regression controls, unchanged original release gates; **INCONCLUSIVE** managed checksum (0/4) | DIA source-file table is not `ISymUnmanagedReader.GetDocuments` |

EXP-023A/B is one numbered research family with two distinct stages. EXP-016/017 are tracked through their draft PRs and the permanent evidence manifest even though there are no correspondingly named standalone Markdown pages in the current tree. No additional experiment is represented by this November 5 review.

## Preparation decisions (proposals, **not** implementation approvals)

Risk and complexity are scoped to RecordSift and only the cited controls. “Easy rollback” means restoring a focused application change **after** approval, not permission to do it now. Each row supplies the present configuration, proposal, benefit, dependencies, risks/security, acceptance, effort/reversibility, ordering, and outstanding approval.

| Category / proposed step | Current → proposal and value | Dependencies and required acceptance | Risk / security | Complexity / rollback / sequence | Open question / approval |
|---|---|---|---|---|---|
| **A1 Baseline contracts as a gate** | Five suites, API 425, XML 5, package and clean consumer exist → make all five-suite and full release evidence mandatory for every candidate | EXP-001, 014–016, 024–035; independent baseline/candidate/negative-control comparison | Low; guard must handle missing evidence by failing closed | Medium / easy / **first** | Approve future implementation of a consistent release gate; preserve frozen main |
| **A2 Minimal conditional LangVersion centralization** | Ten projects individually declare C# 7.3 → conditional root `Directory.Build.props` default, preserve project overrides | EXP-002,005,015; all Debug/Release property scopes and entire release gates after approved implementation | Low–medium; inherited value/import timing; no package change | Low / easy / **after A1** | Approve standalone application PR later |
| **A3 Deterministic compiler setting** | Without opt-in same-source DLLs drift → controlled `Deterministic=true` | EXP-018,019,020; multiple physical checkout roots, original API/resource/XML/package/consumer and PDB identity | Low–medium; path disclosure and source-debug semantics if combined with PathMap | Low / easy / **after A1/A2** | Approve only specified build configurations |
| **A4 Canonical PathMap with valid SourceRoot** | Cross-root deterministic alone 0/5 → suitable canonical PathMap gave 5/5, explicit SourceRoot controls | EXP-020–022,026; actual paths/negative map, PDB/source lookup validation, no global `ContinuousIntegrationBuild` without roots | Medium; incorrect paths can break diagnostics/debugger mapping | Medium / easy / **after A3** | Choose canonical path strategy and whether PDB portability is desired |
| **A5 Existing test runner correction** | Main local script misses XLSX → PR #258 corrected only on release/0.2 | Existing approved branch evidence; verify branch reconciliation and complete five-suite gate at implementation time | Low when isolated, but don't duplicate/promote automatically | Low / easy / **before routine local acceptance** | Separate approval for any release-branch promotion |
| **B1 Explicit SDK selection (`global.json`)** | No guaranteed SDK pin across machines → exact pin/roll-forward policy if needed | EXP-005,008; SDK installed on each host, IDE1006/Release/all suites; note direct Visual Studio MSBuild is independent | Medium operational availability and patch cadence | Low file change / easy / **optional after baseline** | Choose SDK maintenance owner and roll-forward policy |
| **B2 SDK-only Windows release CI** | VS-backed flow works; SDK-only alternative succeeded only with script fixes → optional portable Windows host | EXP-003,004,007,009; repaired UTF-8 notices, XML extraction, runner discovery, negative CS1591 and all consumers | Medium platform/runtime and script changes; audit tool provenance | Medium / reversible / **optional after A1** | Is replacing current CI worth maintenance cost? |
| **B3 Scoped warning-level centralization** | WarningLevel 4 duplicated but default already 4 → conditional scoped shared default | EXP-010 all 20 Debug/Release and Custom controls + release gates | Low if conditional; unconditional changes Custom | Low / easy / **optional** | Is consistency benefit worth added configuration? |
| **B4 Source Link build-task-only research** | Traditional CSV `pdbonly`, manual pinned tool import works → **do not adopt yet** | EXP-023–035; authentic Visual Studio package install, approved closure, security-safe managed PDB checksums, real debugger fetch/step, all-app/consumer gates | **High unresolved**: four NuGet version conflicts, native symbol security, provenance and debugging | Medium–high / reversibility depends on package/binding edits / **after separate gates** | Consolidated approval required; current disposition HOLD |
| **B5 packages.config → exact-pinned PackageReference** | Seven packages.config files, 17 declarations/13 packages; optional format migration without SDK conversion | EXP-011–013; full original 425 policy or separately approved format-aware equivalent, restore/guards, bindings and all consumers | Medium–high; direct-only package downgrade and toolchain differences | High / careful restore / **separate optional migration** | Approve separately; forbid version drift; not a Source Link workaround |
| **C1 SDK-style project conversion** | Ten traditional csproj, framework 4.8, C# 7.3 → defer project format change until controlled evaluation | Preserve source item globs, resx/resource names, assembly identity, imports, API, NuGet nuspec/consumer, generated files | High untested change surface if combined with dependency upgrades | High / branch rollback possible / **later dedicated evaluation** | Separate conversion scope and approval |
| **C2 Central Package Management / package lock strategy** | packages.config does not use CPM → only consider after suitable PackageReference adoption | Explicit NuGet/SDK feature and full graph compatibility | Medium drift; feed integrity, transitive version change | Medium / reversible / **after B5 if chosen** | Choose source/lock policy and whether to adopt |
| **C3 Runtime/TFM or C# feature uplift** | net48 and C# 7.3 → preserve through preparation | New framework, platform, API and performance acceptance matrix | High runtime/consumer compatibility exposure | High / staging required / **separate future evaluation** | Business case and consumer compatibility approval |
| **D1 Early Microsoft.Common.props import** | Existing traditional imports → no early forced import | EXP-006 observed MSB3107 | Known failed behavior | No change / n.a. | Reject unless new, independently scoped necessity |
| **D2 Synthetic Directory.Build.targets/.rsp/solution files** | No duplicated targets demonstrated → no new file | EXP-006 / repository configuration audit | Unnecessary complexity and changed build scope | No change / n.a. | Revisit only for a measured problem |
| **D3 Native managed PDB checksum reader** | DIA table 0/4; older native reader vulnerable → **BLOCK** | EXP-029,031,033,035; prove patched installed binary provenance + actual `GetDocuments`/algorithm/digest/physical CRLF bytes, negative controls | **Security-blocked** without independently established patch status | Research only / n.a. | Microsoft advisory-compliant binary and approved secured execution |
| **D4 Authentic VS Package Manager project installation and debugger stepping** | Manual imports/remote byte checks only → **NOT TESTED** | Live VS IDE host, real `Install-Package` or `IVsPackageInstaller`, real debugger breakpoint + cache-independent fetch | Four pin conflicts and UI automation reliability | Manual acceptance procedure until supported interactive host / n.a. | Document actual install/step results before any adoption |
| **D5 Broad MSBuild process/node isolation** | One inspected AppDomain → scoped observation only | EXP-032; add only if threat/rollout requires all-node guarantee | Unmeasured additional host binding risks | Research optional / n.a. | No duplicate experiment until concrete host-specific failure |

**A means a lower-risk candidate supported by relevant experiments, not that full source implementation is approved or every conceivable environment is tested.** B means additional choices or significant acceptance gaps. C means future work is better isolated into a later project-format/runtime evaluation, not a universal sequencing dependency. D captures rejected, genuinely blocked and research-only paths.

## Independent four-perspective synthesis

**Application architect — OBSERVED:** traditional net48/C# 7.3 remains consumable after scoped manual CSV tool integration; current layering contracts are not changed by the experiments. **INTERPRETATION:** property-only preparation can remain independent of Source Link and dependency migrations; do not present one CSV project as whole-application modernization. **RECOMMENDATION:** preserve architecture boundaries and separate dependency/SDK change sets.

**Build and release — OBSERVED:** deterministic alone fails cross-root equality; PathMap enabled 5/5 DLL equality; independent Source Link builds generated identical DLL/PDB; SDK-only adjusted consumer path works with documented original-script failures. **INTERPRETATION:** fully reproducible builds require controlled host, source paths and dependency environment; a green runner is not a debugger acceptance. **RECOMMENDATION:** accept changes by executed gates, host/version and precise source provenance.

**Security — OBSERVED:** official package hashes/Source Link tasks and module path observations exist; ordinary NuGet resolution exposes four original pin conflicts; the patched `Microsoft.DiaSymReader.Native` version was unavailable in EXP-031; DIA code execution did not verify managed checksums. **INTERPRETATION:** neither Authenticode nor original compatibility certifies a patched native managed reader or full install isolation. **RECOMMENDATION:** hold Source Link and forbid vulnerable fallback, unauthorized feeds/updates, source secrets or PDB uploads.

**Quality — OBSERVED:** 425 API, 419 discovered (418/0/1), five XML, local package and clean consumers repeatedly pass on actual experimental candidates; corrupted negative controls independently validate several checker behaviors. **INTERPRETATION:** synthetic checksum tests cannot substitute for physical managed document records; source-only/package-format coupling can create false positives or misses. **RECOMMENDATION:** maintain per-gate results and full original contract, adapt format-sensitive checks only with separately approved equivalence.

## Recommended sequencing for a future approved implementation

**0. No application changes now.** Preserve draft research and frozen baseline. **1.** Decide future acceptance gate ownership, correct/coordinate the already-implemented five-suite local runner from release/0.2. **2.** Consider minimal conditional LangVersion centralization alone; rebuild and compare exact contracts. **3.** Consider `Deterministic=true` alone and then canonical PathMap/SourceRoot with negative controls. **4.** Independently decide SDK pinning, optional SDK-only Windows CI, and warning-level centralization based on measurable operational value. **5.** Keep Source Link, PackageReference and SDK-style conversion as *separate* approval decisions; do not combine their dependency changes. **6.** Revisit runtime migration only in a new evaluation with explicit consumer/platform targets.

## Approval record needed for any implementation

A future explicit stakeholder decision must identify: exact candidate(s), owning application branch, responsible reviewer, accepted risk and rollback, immutable baseline/reference, whether 425-entry metadata policy changes are permitted, supported Debug/Release/SDK/host platforms, package version restrictions, evidence required before merge, and separate merge/publish authorization. **No such implementation authorization is recorded by this review.**

## Remaining Source Link gate feasibility and manual procedure

See [outstanding approval protocol](experiments/remaining-source-link-approval-gates.md) for the exact installation, debugger and checksum gates. On November 5, independent source/documentation review found **no supported headless equivalent** demonstrated for the Visual Studio-hosted Package Manager Console or debugger on the available GitHub-hosted Windows runner; NuGet/VS components installed on the runner do not by themselves create a running IDE/extension service. This is a **documented feasibility limitation**, not an executed negative test. The official NuGet package gallery continued to list the affected 18.8.4 native reader in publicly indexed information; no independently audited 18.9.0 patched downloadable binary was established during this review. Do not record either gate as verified, or claim permanent impossibility. `Microsoft.DiaSymReader` supports a COM-registry fallback through a .NET Framework reader with limited capabilities, but its installed binary patch identity, exact managed records and safety have **not** been verified; it is a narrowly scoped future hypothesis, not authorization to execute it.

**No new experiment, application acceptance run or CI result was created by this documentation-only decision review.** Prior immutable evidence remains cited with exact relevant runs in the permanent manifest.


## November 5 EXP-036 addendum — independently measured managed Windows-PDB checksum distinction

The consolidated matrix above covered EXP-001–035 and predates [EXP-036](experiments/EXP-036-managed-pdb-source-checksums.md). New evidence does **not** grant adoption authorization: in the controlled direct-Roslyn classic-PDB fixture [42085539647](https://github.com/infoconex/dotnet-modernization/actions/runs/42085539647), two independent managed readers passed SHA1/SHA256 document digest equality with physical compiler source bytes. In the actual frozen RecordSift CSV manual Source Link candidate [42087528244](https://github.com/infoconex/dotnet-modernization/actions/runs/42087528244), original full release/consumer gates passed but dnlib and Cecil each discovered four owned documents **without any exposed checksum digest bytes (0/4)**. The checksum gate therefore **fails closed**; physical alternate-stream absence remains unresolved. No source package/runtime modification or API drift was detected. The exact real compiler invocation/writer difference remains a future scoped investigation, and the VS install/debugger gates are still not tested. Preserve Source Link **HOLD** and prior stakeholder approval boundary.


## November 5 EXP-037 addendum — managed checksum extraction versus physically present source digests

**[Verified isolated research run 42115147369](https://github.com/infoconex/dotnet-modernization/actions/runs/42115147369)** (draft [PR #59](https://github.com/infoconex/dotnet-modernization/pull/59), research SHA `d2be221081444892d30a0deff0b56d91efefd0e8`; [experiment](experiments/EXP-037-compiler-pdb-differential.md)) advances the EXP-036 source-checksum negative without altering the application. All frozen original and manual Source Link candidate API/NUnit/XML/local package/clean consumer/five logical-compatibility controls still PASS. Actual Csc diagnostic invocation exposes `/pathmap` and `/deterministic+` but candidate compiler-server and writer identity remain PARTIAL.

**Controlled differential VERIFIED:** direct Roslyn SHA256 checksum metadata is exposed through both dnlib and Cecil with/without explicit checksum flag and with deterministic-only compilation. Adding pathmap to deterministic direct compilation causes both to discover the same document **without exposing its checksum**, even without Source Link. **Independent MSF7 byte scan VERIFIED:** the original exact source SHA256 bytes are **still stored in named `/SRC/FILES/` streams** in every tested direct fixture and for all **four** actual frozen CSV sources (one matching digest per file), despite the actual two managed parsers returning 0/4. Pathmap controls retain digest bytes under mapped source stream names. Upstream pinned reader code constructs named source stream lookup from document name; exact document-to-named-key equality is the narrow next unverified diagnostic. A physical digest hit alone does not prove per-document record authenticity.

| Approval dimension | EXP-037 result | Decision consequence |
|---|---|---|
| Controlled pathmap/managed-checksum interaction | **VERIFIED** (both readers, independent controls) | Target exact document-name to `/SRC/FILES/` key association |
| Real CSV physical input digests in native named source streams | **VERIFIED**, four of four | Do **not** describe actual native PDB as checksum-byte-free |
| Real CSV *managed document-associated* checksum authenticity | **UNSATISFIED** (dnlib 0/4, Cecil 0/4) | Gate C remains fail-closed; no adoption |
| Actual Csc compiler host, native writer binary identities | **PARTIAL** | No version/writer equality claim |
| Authentic VS Package Manager installation / debugger source stepping | **NOT TESTED** | Independent stakeholder approval gates remain open |

**Disposition unchanged:** Source Link **HOLD**. No changes to the existing approval-gate policy, RecordSift, packages or default branches. Reported evidence only; not production modernization authorization.

## November 5 EXP-038 addendum — source checksum key mismatch explained but approval unchanged

**[Successful isolated experiment 42148192785](https://github.com/infoconex/dotnet-modernization/actions/runs/42148192785)**, [full report](experiments/EXP-038-document-to-native-stream-key.md), draft [PR #61](https://github.com/infoconex/dotnet-modernization/pull/61), executing SHA `fea65001d757d824ff1d908dd5baed5844b42db0`. With unchanged frozen RecordSift, old API/NUnit/XML/package/clean net48 consumer and five logical-compatibility categories passed again. Exact packaged managed reader versions were preserved and the native PE/PDB identity checks passed.

The EXP-037 pathmap result is now explained at the precise source-name level: **both** pinned dnlib and Cecil source-doc URLs construct a named source-checksum key that is found by case-insensitive matching in no-pathmap positive controls but **not found** after pathmap; in mapped fixtures **and each of four selected actual CSV source documents**, normalizing slash and backslash separators plus casefold makes the document name and digest-bearing named stream key equal. The actual native source-file record was structurally parsed (algorithm GUID/length/digest) and matched to physical compiler-input SHA256 for all four owned files, not merely found as a free byte substring. A private ephemeral URL manifest was used solely in bounded runner memory/files and deleted before sanitized artifact upload.

| Decision gate | Evidence | Status/decision |
|---|---|---|
| Original frozen app API/behaviors/packaging/consumer | 425 API, 419 NUnit (418 pass/1 skip), five XML, unpublished nupkg, clean net48 consumer, five compatibility categories | **PASS** for bounded manual-import candidate |
| Exact native SHA256 record per selected owned CSV source | Native GUID/length/checksum structured decode + physical source digest match | **VERIFIED 4/4** |
| Actual managed document vs native stream key mapping | Both pinned readers fail case-insensitive key lookup when pathmapped; separator normalization + casefold matches real digest-bearing stream | **ROOT MECHANISM VERIFIED** for selected four and controlled fixtures |
| Managed reader exposure / existing Gate C all-relevant-doc authenticity | Both unmodified readers still return 0/4; unclassified/generated/external document inventory not covered | **UNSATISFIED; FAIL-CLOSED** |
| Authentic IDE NuGet project install and actual Visual Studio debugging | Neither executed | **NOT TESTED** |
| Source Link production adoption | Requires separate stakeholder decision and additional acceptance | **HOLD** |

**Consolidated recommendation:** do not change Roslyn, remove pathmap, migrate PDB format, or add a runtime package based on a **reader lookup mismatch**. Prefer a separately evaluated, bounded, generalizable, independent normalized-key structural verifier as a **proposed** alternative Gate C evidence pathway, with explicit complete-document/negative/security evidence and approval. Do not silently relabel existing Gate C PASSED. Compiler-server and native symbol writer identity remains partially captured but need not be asserted as the cause of this observation.

## November 5 EXP-039 addendum — independent verifier succeeds but complete native source stream inventory remains open

[Successful EXP-039 CI 42152491141](https://github.com/infoconex/dotnet-modernization/actions/runs/42152491141), [experiment](experiments/EXP-039-reusable-windows-pdb-checksum-verifier.md), [draft PR #63](https://github.com/infoconex/dotnet-modernization/pull/63), executing SHA `6597250630998c01da43c5c6527cda478cb9008a`. A reusable Python stdlib research tool with 21 passing synthetic tests reconstructs exact normalized document URL to native `/SRC/FILES/` key, verifies PE/PDB identity and structured checksum records, and cryptographically validates physical compiler-input bytes. It independently verified **one of one** managed-reader-discovered source in each of five compiler-option fixtures and **four of four** actual frozen CSV sources, preserving 425 API / 419 NUnit (418 pass/1 skip) / five XML / original local nupkg / clean net48 consumer and five compatibility-category acceptance.

**Coverage matters more than headline 4/4:** the actual CSV PDB has seven native named source streams but only four independently reader-discovered document identities. The remaining **three** are unclassified; the verifier explicitly says `INCOMPLETE_OR_UNCLASSIFIED_NATIVE_STREAMS`. The test proves authentic SHA256 for four declared compiler inputs but **not** all native PDB document records, not all application assemblies, and not a security-approved replacement reader. A clean full-source checksum Gate C claim is **not** justified.

| Gate | EXP-039 status | Decision |
|---|---|---|
| Original app API/test/XML/package/consumer compatibility | **Verified** in frozen original and manual candidate | Historical compatibility preserved in scoped experiment |
| Independent native structured physical hash (5 fixtures, 4 owned CSV) | **VERIFIED** | Reusable audit candidate, not current Gate C acceptance |
| All native source-stream/document/physical-input coverage | **INCOMPLETE** (three unmatched CSV native source streams) | Require targeted C13/source provenance classification |
| Existing unmodified managed-reader Gate C | **UNSATISFIED** (dnlib and Cecil still 0/4) | No silent policy replacement |
| Authentic VS package-install, debugger source retrieval and stepping | **NOT TESTED** | Retain independent gates |
| Source Link production approval | **HOLD** | Consolidated stakeholder approval still required |

**Research boundary unchanged:** no RecordSift code/pin/target change, no merge or publication. The portable-PDB format option and native vulnerable reader are not used as shortcuts; exact compiler-server/writer identity remains partial.


## November 5 EXP-040 decision update — native document inventory reconciled, physical bytes incomplete

[Experiment](experiments/EXP-040-native-document-provenance.md), [draft research PR #65](https://github.com/infoconex/dotnet-modernization/pull/65), [successful Windows/Ubuntu run 42159594243](https://github.com/infoconex/dotnet-modernization/actions/runs/42159594243). Frozen RecordSift source unchanged; original/candidate API, NUnit, XML, unpublished NuGet/clean consumer and five logical compatibility categories passed.

| Gate | Independent finding | Current decision |
|---|---|---|
| Native CSV document inventory | **Seven** native named streams = seven DBI source identities = seven C13 FILECHKSMS identities across eight records | Three extra streams are **native-referenced source documents**, not unreferenced metadata |
| Extra records' structure | All **three** have supported native SHA256 records; DBI and C13 references; no C13 line references | Do not infer they are irrelevant, generated, repository-owned or physically verified |
| Original compiler-input bytes | SHA256 validated **4/7**; three originals unproven | Require separately trusted source-input manifest and exact-byte comparison |
| Managed-reader Gate C | Both current readers expose **0/4** digest bytes | **UNSATISFIED; no alternate policy authorized** |
| Actual VS Package Manager project install / remote stepping | No authentic execution evidence | **NOT TESTED** as separate gates |
| Source Link adoption | No consolidated release authorization | **HOLD** |

**Five review perspectives:** Build: keep frozen compiler/host and original release acceptance distinct from direct Roslyn fixtures. Security: bounded trusted PDB parser, private manifests destroyed, no native untrusted code or raw PDB/path/hash artifact. Architecture: reusable full normalized source identity and independent DBI/C13/managed/named inventories. Quality: 21 previous and 22 new regression tests passed, preserve two initial parser-harness failures and correction of C13 line block header sizing; no false application fault. Release governance: incomplete 4/7 physical-byte coverage and no stakeholder Gate C approval. Recommended next targeted investigation: authenticate three additional physical compiler inputs; only then evaluate whether an **alternative** Gate C evidence path merits a formal approval request. No app change, merge, NuGet publication or waiver.
