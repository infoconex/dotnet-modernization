# Source Link in a traditional .NET Framework 4.8 project — independent technical assessment

**Prepared:** November 4, 2026 (America/Los_Angeles). **State: RESEARCH HOLD — NO PRODUCTION CHANGE APPROVED.**

**Repositories:** `infoconex/dotnet-modernization` and frozen `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`. Experiments are disposable Windows runner changes plus standalone research draft PRs; no application main commits, research main merges or NuGet publications.

## Question

Can modern Source Link tooling for GitHub safely produce verifiable source mappings in **traditional non-SDK C# 7.3 / net48** projects while preserving existing application package versions, `DebugType=pdbonly` and historically verified public API/runtime/package compatibility?

**Short answer:** Manual, hash-pinned Source Link **build-tool-only imports have demonstrated technical viability**, preserving the application release contracts in a disposable CSV project. However, this is **not** sufficient evidence to recommend installing the complete Source Link NuGet dependency graph in the existing `packages.config` project. One critical native PDB document checksum gate is presently blocked by a patched-reader availability issue; normal Visual Studio NuGet Package Manager project installation and actual debugger source stepping remain unverified.

## Evidence matrix — do not collapse categories

| Experiment | Actual independently verified scope | Known limitation |
| --- | --- | --- |
| EXP-019 / EXP-020 / EXP-022 | Explicit deterministic / PathMap or SourceRoot bridge can produce identical DLLs across different actual checkout roots, with all original release gates. | Does not provide source retrieval or debug Source Link mapping. |
| EXP-023A / EXP-023B ([PR #38](https://github.com/infoconex/dotnet-modernization/pull/38), [#39](https://github.com/infoconex/dotnet-modernization/pull/39)) | Official pinned NuGet archives, asset inventory, transitive net48 package metadata and Windows/Ubuntu regression gates. | Metadata and tool-asset presence alone do not establish host load path or safe NuGet project install. |
| EXP-024 ([PR #40](https://github.com/infoconex/dotnet-modernization/pull/40)) | Manually imported three hashed Source Link 10.0.403 tool archives into **one** temporary CSV csproj, preserved original nine packages.config entries, `DebugType=pdbonly`, no new Release-output task DLL; historical 425 API, 419 NUnit (418 pass/1 skip), five XML docs, unpublished package and clean net48 consumer passed against candidate. | Not equivalent to Visual Studio NuGet Package Manager installation or full closure. |
| EXP-025 ([PR #41](https://github.com/infoconex/dotnet-modernization/pull/41)) | Native Windows PDB MSF7 `sourcelink` stream (not necessarily `sourcelink$1`), nonempty JSON, exact frozen commit, and matching compiled DLL CodeView GUID+age. | Does not verify per-document recorded checksum bytes or debugger UI behavior. |
| EXP-026 ([PR #42](https://github.com/infoconex/dotnet-modernization/pull/42)) | Real two-worktree frozen candidate builds produce identical CSV DLL and Windows PDB SHA-256 bytes with compatibility gates; authentic `.git` pointer. | Not equivalent to a nested gitlink submodule; separate EXP-030 covers that. |
| EXP-027 ([PR #43](https://github.com/infoconex/dotnet-modernization/pull/43)) | Real `nuget install ... -Framework net48 -DependencyVersion Lowest` toolchain closure **eight package IDs**, **four differing application package pins**. | Acquisition into temp directory, not actual `.csproj` Package Manager install, runtime copy-local or binding proof. |
| EXP-028 ([PR #44](https://github.com/infoconex/dotnet-modernization/pull/44)) | One selected PDB-mapped C# source URL resolves to exact frozen Git blob (6,346 bytes), independently compared; Windows CRLF checkout (6,469 bytes) distinguished; all original candidate gates passed. | One source, not every PDB document record; worktree bytes differ legitimately due to CRLF. |
| EXP-029 ([PR #46](https://github.com/infoconex/dotnet-modernization/pull/46)) | Independent LLVM native PDB source reference inventory on actual candidate PDB, five displayed source-file entries with `(no checksum)`; original release gates passed. | **Managed document checksum authenticity is NOT verified.** LLVM text could omit records. |
| EXP-030 ([PR #47](https://github.com/infoconex/dotnet-modernization/pull/47)) | Four genuine Git layouts, all historical Release/consumer gates: shallow-detached GitHub origin Source Link **present**; no remote **absent**; genuine submodule with local origin **absent**; genuine submodule with GitHub origin **present**. Negative PDB controls additionally verify native DLL/PDB identity. | Source Link absence can occur despite passing build and tests; no blanket positive claim across all Git layouts. |
| EXP-031 ([PR #48](https://github.com/infoconex/dotnet-modernization/pull/48)) | Security gate verifies patched `Microsoft.DiaSymReader.Native >= 18.9.0-beta1.26405.2` unavailable from public NuGet (latest `18.8.4-beta1.26356.2`) on checked date, so native reader execution refused. | **BLOCKED**. C# reader is proposal only, not compiled, checksum gate cannot be cleared by disabling safety. |
| EXP-032 ([PR #49](https://github.com/infoconex/dotnet-modernization/pull/49)) | **Verified actual runtime observation** in Windows CI [41982078891](https://github.com/infoconex/dotnet-modernization/actions/runs/41982078891): SourceLink.GitHub, SourceLink.Common and Build.Tasks.Git loaded from isolated build-tool packages; System.Memory, Buffers, Numerics.Vectors and Unsafe loaded from preinstalled host toolchain; full original candidate API/NUnit/XML/package/consumer gates pass, no new bin DLLs. | Observed diagnostic task's MSBuild AppDomain only, not every node or Package Manager project install; full process-host isolation not universally established. |

### Complete normal NuGet closure conflicts

Real `net48` NuGet CLI resolution at [EXP-027 CI 41968065998](https://github.com/infoconex/dotnet-modernization/actions/runs/41968065998) selected:

| Dependency | Frozen RecordSift pin | Resolved toolchain package |
| --- | --- | --- |
| `System.Buffers` | 4.5.1 | **4.6.1** |
| `System.Memory` | 4.5.5 | **4.6.3** |
| `System.Numerics.Vectors` | 4.5.0 | **4.6.1** |
| `System.Runtime.CompilerServices.Unsafe` | 6.0.0 | **6.1.2** |

Build-task packages may bundle private `tools/netframework` copies while ordinary NuGet closure contains additional `lib/net462` assets. Both observations can be true simultaneously. Never equate `developmentDependency=true` with complete runtime exclusion or recommend overwriting the original nine package entries.

## Reviews from four engineering perspectives

**Application architect:** The unmodified traditional project + temporary tool-only import preserves the application-facing contracts in the tested pilot. This supports keeping Source Link optional and separate from language/MSBuild property modernization. A one-project positive gate cannot be generalized to all ten projects, framework versions or Git providers.

**Build/reproducibility engineer:** EXP-026 verified same SHA, different actual Git worktrees produced byte-identical CSV DLL and PDB, but git provider provenance materially changes whether Source Link is embedded. Enforce a native PDB mapping gate, not just `/sourcelink` compiler args or CI success. Maintain clean frozen SHA, toolchain version and portable SourceRoot/PathMap evidence.

**Security engineer:** The Source Link NuGet toolchain introduces four original dependency-version conflicts in standard resolution. Separate pre-release dependency audit and loader inspection are necessary. A separate native DiaSymReader checksum inspection is **blocked** until the patched native reader becomes available and is independently vetted. Never run a vulnerable fallback merely to make CI green.

**Release/quality engineer:** The original 425-entry API, all 419 NUnit, five XML docs, unpublished package and net48 installed consumer are mandatory for every candidate. EXP-024 observed these and was careful to copy the candidate into test directories before running tests. Do not publish or merge based on only module presence, structural PDB metadata, or unchanged packages.config.

## Recommendation for stakeholder review — no implementation authorization

**HOLD Source Link as an optional research candidate** for traditional net48/`packages.config`. Favor already verified low-risk **deterministic and SourceRoot/PathMap preparation** independently of this Source Link work. Before production guidance, separately resolve:

1. **Full PDB document checksum acceptance:** validate the actual classic Windows managed PDB document records with a securely patched and independently provisioned reader, including algorithm, exact compiled physical source bytes and negative corruption controls. The existing LLVM `(no checksum)` lines do not clear this check.
2. **Visual Studio debugger source-step test:** interactive verification using matching release PDB and symbol/source settings (manual, explicitly unverified until observed).
3. **Conventional NuGet project install:** truly disposable traditional csproj with Visual Studio Package Manager semantics, record every new package, HintPath, import, build output, binding redirect and distributable dependency change. Not equivalent to `nuget install` or manually unzipping three tool packages.
4. **Task host process isolation and security audit:** record actual loaded DLL versions and locations in relevant MSBuild AppDomains, validate no production reference/output/consumer dependency changes; recheck CVEs and reproducible official archive integrity.
5. **Broader source/host permutations:** a real nested GitHub submodule is verified in EXP-030; other providers, missing remote and URL privacy/security require scoped acceptance before generalized templates.

**Decision requested:** Keep draft research PRs intact, do not merge or update RecordSift; review whether documentation should describe Source Link as *optional with explicit prerequisites* or defer until dependency-install and checksum/debugger gates are resolved. No production recommendation is made here.
