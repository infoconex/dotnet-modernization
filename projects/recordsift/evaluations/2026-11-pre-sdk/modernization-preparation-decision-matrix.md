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
