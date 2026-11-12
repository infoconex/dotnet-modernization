# Gate C-N D2b — real isolated NuGet package-to-CLR identity verification

**Date:** 2026-11-06 Pacific · **Disposition:** D2b LOCAL RESEARCH COMPLETE / FIVE TARGETED NEGATIVES PASSED / PRODUCTION RELEASE STILL BLOCKED.

**Authorization:** [stakeholder delegated strictly bounded next research and five simulated engineering-role consensus, issue #80](https://github.com/infoconex/dotnet-modernization/issues/80#issuecomment-6697745793). No independent human reviewers met or signed; #77 remains open. **Preregistered before execution:** [D2b local protocol, commit `0169c6b43194f7300bb7d46c8b954483139edcbb`](https://github.com/infoconex/dotnet-modernization/blob/0169c6b43194f7300bb7d46c8b954483139edcbb/methodology/acceptance-gates/reviews/2026-11-06/gate-cn-d2b-preregistered-local-nuget-protocol-20261106.md).

## Primary CI evidence independently retrieved from GitHub

**[Run 42308071696 — SUCCESS](https://github.com/infoconex/dotnet-modernization/actions/runs/42308071696)**; executing research SHA `1e5c0afa69dd32c3059a4f110b0f6b6ab6c83b0e`, job `128202376201`, `windows-2022` hosted runner. All steps completed SUCCESS, including exact-SHA checkout attestation, actual two-restore/five-negative research execution, cleanup and sanitized-only upload. Independently fetched GitHub job log states `D2b research: two real local NuGet installs, two real CLR consumers, 5/5 candidate identity negatives PASS`. Retained [sanitized research workflow artifact](https://github.com/infoconex/dotnet-modernization/actions/runs/42308071696): ID `13547480963`, name `gate-cn-d2b-sanitized-research-only`, expiration policy 30 days, no original source/path/PE/PDB/hash uploads. **The artifact payload ZIP has not been separately opened/decoded in this review; the report's observations derive from trusted source at exact SHA, independently fetched workflow/job/log metadata and artifact listing.**

**Research code implementing actual probes, execution SHA:**
- [Orchestration, two traditional builds](https://github.com/infoconex/dotnet-modernization/blob/1e5c0afa69dd32c3059a4f110b0f6b6ab6c83b0e/tooling/pilots/gate-cn/D2b/run.ps1)
- [Actual package, real restore, installed/copy/loaded candidate verifier](https://github.com/infoconex/dotnet-modernization/blob/1e5c0afa69dd32c3059a4f110b0f6b6ab6c83b0e/tooling/pilots/gate-cn/D2b/verify_nuget_chain.py)
- [Genuine SDK net48 consumer PackageReference](https://github.com/infoconex/dotnet-modernization/blob/1e5c0afa69dd32c3059a4f110b0f6b6ab6c83b0e/tooling/fixtures/gate-cn/D2b/Consumer/D2b.Consumer.csproj)
- [Actual Windows PowerShell 5.1 .NET Framework consumer method/dependency-load observer](https://github.com/infoconex/dotnet-modernization/blob/1e5c0afa69dd32c3059a4f110b0f6b6ab6c83b0e/tooling/pilots/gate-cn/D2b/load_consumer_in_netfx.ps1)
- [Research-only Windows workflow](https://github.com/infoconex/dotnet-modernization/blob/1e5c0afa69dd32c3059a4f110b0f6b6ab6c83b0e/.github/workflows/validate-gate-cn-d2b-local-nuget.yml)

## Actual chain and five intended rejection controls

**Prerequisite genuine positives:** same checked-in original public C# tracked source in the traditional non-SDK net48 fixture, two separate deterministic Windows `/t:Rebuild` outputs with different `DefineConstants`, real different DLL SHA256, each actual PE CodeView RSDS GUID/age matches corresponding classic PDB Info. A and B are separately assembled **standards-format OPC ZIP + nuspec NuGet packages**, each containing real `lib/net48/D2a.Probe.dll`, same package ID `D2b.Disposable` and version `0.1.0` but different bytes; packages are assembled via Python stdlib, **not by a NuGet pack command**. `dotnet restore` genuinely resolves these archives via two isolated `NuGet.Config` files with `packageSources/clear`, single local feed and fresh per-case global-packages directories, with no nuget.org fallback; actual project.assets contains the expected ID/version. Both SDK net48 consumers compile after real restore and copy appropriate package DLL. New Windows PowerShell .NET Framework CLR child invokes the actual consumer method calling the package library, observes loaded candidate Assembly.Location/MVID/method return, and trusted parent hashes actual loaded location after the child exits. Positive A method returns 101 and B returns 202.

| Case | Deliberate negative | Contract rejection required; asserted by running code | Observed primary CI result |
| --- | --- | --- | --- |
| **D2b-N01** | Construct genuine alternate ZIP package member containing real B DLL while expected DLL was A | `D2B_PACKAGE_DLL_HASH_MISMATCH` at package ZIP member check | **PASS**, after real A package-member positive; mixed package **was not restored** |
| **D2b-N02** | Actually restore a different same-ID/version package B from a different isolated local feed with fresh cache; compare against approved A archive digest | `D2B_PACKAGE_ARCHIVE_SHA_MISMATCH` | **PASS**, after two actual local NuGet restores and independent A/B archive positives |
| **D2b-N03** | Substitute real B DLL bytes for A installed NuGet global-cache DLL after actual restore | `D2B_RESTORED_DLL_HASH_MISMATCH` | **PASS**, then restores original A bytes before consumer build |
| **D2b-N04** | Substitute real B DLL bytes for A consumer CopyLocal after actual NuGet restore and C# consumer build | `D2B_CONSUMER_COPY_HASH_MISMATCH` | **PASS**, then restores A before positive CLR execution |
| **D2b-N05** | Actual new .NET Framework child loads the consumer B and real B dependency; compare actual observed SHA, method identity to approved A | `D2B_CLR_LOADED_DLL_HASH_MISMATCH` | **PASS**, after both A and B actual runtime load positives |

A negative counts only if the *specific expected typed category* is returned, not when a NuGet, compiler or CLR process errors. Implementation's `negative()` function checks that exact failure code; unrelated setup failures are `INCONCLUSIVE`. No new real control is counted from historical D1/D2a results.

## Evidence limitations; no release promotion

- **Independent production manifest NOT ESTABLISHED.** The experiment gets expected candidate hash from trusted in-memory runner-local A output before packaging; there is **no independently approved/custodied exact source/target/assembly list** or human signature. Self-consistency is not authoritative release scope.
- **Compiler provenance NOT CRYPTOGRAPHIC.** This D2b experiment intentionally reuses only the public fixture and actual paired output as a positive prerequisite, not the D2a Csc instrumentation or original 64-source RecordSift proof. It does not establish independent Csc invocation→DLL custody or official release dependency graph.
- **Runtime module SHA NOT ATOMIC.** The .NET Framework child reports real assembly location, MVID and invoked method. Trusted parent SHA256 of the loaded location occurs after the child exits, so a hostile filesystem or TOCTOU adversary is outside this runner-local evidence boundary.
- **Package trust not generalized.** Real packages are standards-format OPC ZIPs assembled by Python, not `nuget pack`; actual NuGet restore/build authenticates local consumer compatibility. This does not assert a package signed/published from RecordSift or validate its five-component dependency graph, source-server behavior, IDE install or production NuGet dependencies.
- **Security:** no user data/real RecordSift build, package publication, external feed, raw source/PDB/package uploads, secrets, release gate or branch merge. Hosted Windows teardown step succeeded. Sanitized artifact retention is temporary; it is not an independent immutable production archive.

**Disposition:** Bounded D2b research objective COMPLETE under its precise threat and compiler scope; CV-01/02/03 **production blockers remain open**, especially independent approved manifests, compiler/output custody and a complete real application test/package/loaded-module dependency graph. The next high-value milestone should be an **independent human review/custody and formal acceptance boundary decision in #77**, not reflexive additional live builds. Future full application or release-gate integration requires explicit stakeholder and human technical/security approval. Keep stacked draft PRs #74/#81/#82/#83 unmerged.

**Original managed Gate C `UNSATISFIED`; proposed native Gate C-N production `NOT_AUTHORIZED`; Source Link production `HOLD`.**
