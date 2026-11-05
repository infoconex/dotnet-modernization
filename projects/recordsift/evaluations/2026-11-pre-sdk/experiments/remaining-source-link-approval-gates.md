# Traditional net48 Source Link — outstanding approval-gate execution protocol

**Research only, prepared November 4, 2026. No implementation authorization.** Target `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`, C# 7.3, traditional `packages.config`, Release `DebugType=pdbonly`. This is a reusable **future-execution procedure**, not a claim that the open gates have passed. See [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37) and [consolidated assessment](EXP-023-to-032-source-link-assessment.md).

## Universal prerequisites: immutable baseline and privacy

All experiments must use a **new disposable Windows checkout** frozen to the exact RecordSift SHA. Do not change, commit to, or merge main in either repo; do not publish NuGet packages. Preserve byte-level SHA256 snapshots of all nine existing CSV `packages.config` entries, original `.csproj`, distributable `.nuspec`, existing DLL/API surface and exact build/environment versions. Preserve research provenance separately from app changes, redact absolute paths and credentials, never upload untrusted symbols/source/binaries, and retain failed negative controls.

Avoid conflating `nuget install`, `nuget restore`, manually extracted Source Link `.props/.targets`, `developmentDependency=true` and actual **Visual Studio NuGet Package Manager installation**. They have different project-editing and dependency semantics.

## Gate A — Conventional Visual Studio Package Manager project installation (UNVERIFIED)

On Windows with the actual Visual Studio Package Manager Console and correct classic solution loaded, select only the disposable CSV project. The research command to **try, not an approved application modification**, is:

```powershell
Install-Package Microsoft.SourceLink.GitHub -Version 10.0.403 -ProjectName RecordSift.Infrastructure.Csv
```

Record Package Manager and NuGet versions, actual selected feed, console diagnostics, all new/changed `packages.config` entries, `.csproj` `Reference`, `HintPath`, `Private`, imports and install scripts, `msbuild /pp`, compiler arguments, copy-local outputs, app/runtime assembly binding, local nupkg and clean consumer dependencies. EXP-027 actual NuGet CLI acquisition revealed *four* potential net48 application-version conflicts (not only two): `System.Buffers 4.5.1→4.6.1`, `System.Memory 4.5.5→4.6.3`, `System.Numerics.Vectors 4.5.0→4.6.1`, and `System.Runtime.CompilerServices.Unsafe 6.0.0→6.1.2`. Do not upgrade application package pins or assert no effect without separate evidence and approval.

Compare **before vs after** full source byte snapshots, all 425 public API entries, 419 NUnit (418 pass, 1 skip), five XML, exact local unpublished nupkg, installed clean net48 consumer, five logical compatibility categories and actual `Release/bin` dependency manifest. A successful `nuget install` acquisition into a temp folder is **not** a substitute for this Visual Studio project-installation acceptance.

**Acceptance:** original app pins/distributable contract preserved or each approved difference explicitly documented, original tests/API/consumer and local dependency output unchanged, Source Link compiler/PDB gates independently pass. **Block:** unavailable interactive Package Manager extension, any unintended package/reference/runtime changes, unsafe package source, or incomplete consumer proof.

## Gate B — Actual Visual Studio debugging and source retrieval (UNVERIFIED)

Use a disposable net48 consumer, exact native Windows PDB and DLL from frozen Source Link candidate. In a clean Visual Studio debugger profile with source caches cleared, verify loaded symbols match the exact PDB CodeView GUID/age and frozen SHA. Step through a CSV method executed by the consumer; confirm source was **fetched through the mapped HTTPS Source Link URL**, not silently resolved to a local checkout or cache, and that source bytes and line numbers match. Include deliberately wrong PDB and temporarily unavailable raw-source negative controls; do not treat fallback local source opening as a positive.

**Acceptance:** matching symbols loaded; correct remote file, breakpoint/step behavior and independent negative controls demonstrated, with redacted evidence. **Blocked:** cannot operate interactive VS debugger, only local/cache resolution observed, or PDB checksum policy prevents stepping. This gate cannot be claimed solely from compiler `/sourcelink`, native PDB JSON or remote Git byte parity.

## Gate C — Native managed Windows PDB document checksum authenticity (SECURITY-BLOCKED)

EXP-029 and EXP-033 separately used preinstalled LLVM and reported five native PDB file rows displaying `(no checksum)`; EXP-033 saw no C13 checksum token in its separate raw-chunk view. **Neither text view establishes complete cryptographic validity or universal absence of all managed `ISymUnmanagedDocument` digests.** EXP-031's proposed native reader is **not compiled and not executed** because `Microsoft.DiaSymReader.Native 18.9.0-beta1.26405.2` (patched per advisories) was unavailable on the official NuGet feed as checked. **Never use the earlier potentially vulnerable native package as a shortcut.**

When a verifiably patched and independently audited reader becomes available, first compile/test the research reader in isolation, with NuGet audit and malicious-PDB input controls. Confirm every PDB managed document URL/path, algorithm GUID and digest length; compare each digest with **physical compiler input bytes** (Windows CRLF matters), and explicitly include generated/external source entries or record exclusions. Negative controls: wrong DLL/PDB GUID, incorrect algorithm, corrupt source, corrupt recorded digest, missing source, duplicate document, malformed PDB and a source file with immutable Git LF bytes that differ from compiler CRLF bytes.

**Acceptance:** each actual document has a supported checksum with exact compiler-input byte match, negative controls fail closed, no vulnerable components executed. **Block:** patched native reader unavailable, no checksum records, insufficient document coverage or corrupted/unsafe symbol inputs.

**EXP-035 update (November 5 UTC):** A Microsoft Authenticode-signed Visual Studio DIA SDK C++ source-file table reader was compiled and executed in frozen Windows CI [41988493390](https://github.com/infoconex/dotnet-modernization/actions/runs/41988493390); 0/4 selected managed document checksums were verified (`INCONCLUSIVE`). Real candidate 425 API/419 NUnit/five XML/local unpublished package/clean consumer and PDB identity passed; independent synthetic checksum corruption controls passed on Windows and Ubuntu. DIA's native table does **not** establish full managed `ISymUnmanagedDocument` records or their absence. The original patched managed-reader requirement remains **SECURITY-BLOCKED**. See [EXP-035](EXP-035-dia-sdk-checksum-feasibility.md).\n\n## Gate D — Full build-host module isolation (PARTIALLY VERIFIED)

EXP-032 directly observed task assemblies `Microsoft.Build.Tasks.Git`, `Microsoft.SourceLink.Common` and `Microsoft.SourceLink.GitHub` loaded from isolated build-tool directories in one MSBuild AppDomain; key `System.*` assemblies came from the preinstalled host, and candidate app release/API/test/consumer gates passed. This is real runtime evidence but does not prove every MSBuild process, out-of-process node, task AppDomain or conventional Package Manager installation. If broader host isolation is required, enumerate each process/AppDomain and fail on undesired runtime references or distributable dependencies; retain only redacted module classification. Do not equate imported targets with executed and correctly isolated assemblies.

## Decision boundary and approvals

Research has verified optional **manual build-task-only** Source Link integration, native PDB URL mapping, exact immutable Git source bytes for the **four independently listed owned CSV source files**, same SHA byte-identical DLL/PDB across two physical worktrees, real Git shallow/remote/submodule positive and negative cases, scoped task assembly loading and preserved historical compatibility. The above gates remain **unverified / partially verified / security-blocked** as specified. RecordSift is a ten-project solution: one CSV project does not establish suitability for all five production assemblies or all CI/consumer platforms.

Recommendation: keep Source Link **optional research only**, do not merge or ship. Treat verified deterministic compilation and explicit SourceRoot/PathMap preparation as independent low-risk modernization candidates, still subject to stakeholder review. Stop before any production adoption or application dependency change without consolidated approval.
