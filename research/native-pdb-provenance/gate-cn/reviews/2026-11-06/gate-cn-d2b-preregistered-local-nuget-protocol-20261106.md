# Gate C-N D2b — delegated bounded research decision and preregistered plan

**Date:** 2026-11-06 Pacific. **Status:** Authorized by stakeholder delegation for *bounded disposable research only*; preregistered before D2b execution. **No production authorization.**

**Stakeholder instruction:** "You and the group should make a recommendation as to what is next and unless you need me to specifically weight in just keep going. Let me know if we should start a new chat." Treat this as delegated discretion for the **next bounded nonproduction research experiment**, not an instruction to waive independent human decisions, prior approval safeguards, or production release authority.

**Role synthesis (NOT five independent reviewers):** software architect — keep complete candidate identity chain explicit and dependency boundaries inward; build engineer — use real NuGet restore and controlled local sources; security — isolate packages, prevent fallback/caching and upload only sanitized categories; quality — single-change negatives and genuine CLR witness; release governance — new disposable research draft only, preserve legacy and C-N HOLD. Each of the five simulated roles recommends this narrow D2b scope. This single-model synthesis **is not human consensus, actual peer signoff or approval of issue #77**.

## Why D2b follows D2a without repeating it

D1 paired synthetic positives/negatives passed [run 42294445275](https://github.com/infoconex/dotnet-modernization/actions/runs/42294445275). D2a passed [real Windows run 42303167674](https://github.com/infoconex/dotnet-modernization/actions/runs/42303167674) on one disposable traditional C# 7.3 net48 fixture, five targeted real paired/compiler/CLR research controls. **Neither validated actual NuGet package creation, a clean isolated NuGet dependency resolution, local source selection, package extraction, or package-to-runtime loaded-module identity.** This is the new evidence gap, not a rerun of EXP-043/044 or D2a negative matrix.

## Exact bounded experiment

- Create a new *stacked draft* research PR based on D2a draft PR #82. Do not merge any PR or modify either `main` or `infoconex/RecordSift`.
- Reuse only the single public disposable traditional C#7.3 net48 **D2a.Probe** fixture source as a positive build input; compile two source-identical variants with different explicit defines, preserving output SHA/CodeView↔PDB pairing. This reuse is an experiment prerequisite, **not** a repetition of D2a fault-injection tests.
- Build two valid local `D2b.Disposable.0.1.0.nupkg` NuGet ZIP packages, identical ID/version but different real underlying DLL/PDB bytes (variant A approved, B substituted), one package per isolated local feed. Package creation must include a standards-compatible nuspec and `lib/net48` candidate DLL; log no private paths/bytes.
- Restore a single small non-published SDK-style **net48 consumer** from the explicitly selected local feed, with a fresh separate global-package cache / lock file for each case, **no** nuget.org source and no fallback. The SDK-style consumer is only the disposable *consumer harness*, not modernization of the traditional production fixture.
- Verify (i) complete candidate output DLL SHA256, (ii) exact nupkg archive SHA256, (iii) exact nupkg `lib/net48` DLL byte hash, (iv) NuGet *actual installed cache* DLL byte hash and the package archive cache identity, (v) actual compiled consumer DLL's **CopyLocal** candidate and (vi) the actual .NET Framework CLR Assembly.Location/MVID/method output with SHA256 measured in trusted parent after child exits. Preserve source feed identity and package SHA as independent expected values, **not derived after selecting the package**.
- Use fresh separate restore roots to avoid caching cross-contamination; verify one resolver result and exact physical source bytes. Preserve SHA only in ephemeral private witness, public report categories/count only. No private PDB/package/source dump.

## Preregistered negative controls and exact failure categories

| Control | Positive | Single mutation | Expected explicit rejection |
| --- | --- | --- | --- |
| **D2b-N01 package entry mismatch** | Real A package contains A DLL SHA, NuGet extracts same DLL | Substitute complete genuine B `lib/net48` DLL while retaining approved A candidate output identity | `D2B_PACKAGE_DLL_HASH_MISMATCH` |
| **D2b-N02 alternate feed / same ID-version** | Clean restore from only approved local feed A, installed nupkg and DLL bytes match A approval | Select alternate isolated feed containing valid **same ID/version** B package | `D2B_PACKAGE_ARCHIVE_SHA_MISMATCH` |
| **D2b-N03 restored cache DLL substitution** | Package A was restored into clean isolated cache and installed DLL hash matches A | Overwrite one installed DLL with genuine B bytes after NuGet restore, before consumer copy | `D2B_RESTORED_DLL_HASH_MISMATCH` |
| **D2b-N04 wrong copied test candidate** | Compile consumer and copy/load A; private CLR witness matches installed package A | Replace consumer output CopyLocal DLL with B while package cache and approved A remain valid | `D2B_CONSUMER_COPY_HASH_MISMATCH` |
| **D2b-N05 runtime loaded candidate** | New .NET Framework CLR child actually loads A from isolated consumer output; location and method result verified | Load B from another private local path while pretending its identity is approved A | `D2B_CLR_LOADED_DLL_HASH_MISMATCH` |

Each negative must be blocked by **the intended exact layer**, not an unrelated broken project/restoration/error. Every negative must have an actually successful positive predecessor. Validate A and B native PE/PDB pairs, distinct DLL bytes, and actual A vs B method values before injection. If any baseline cannot be verified, report `INCONCLUSIVE` and stop. The N05 host-path measurement is runner-local post-exit, **not atomic in-process loaded-module attestation**.

## Safety and boundary

**Authorized:** only the five listed D2b research controls, one dummy traditional project + disposable SDK net48 consumer, Windows-hosted CI, local isolated feeds and restore roots, fixed-category sanitized report, cleanup (including failure). No external package download, publishing, actual RecordSift release candidate, Source Link IDE production adoption or prod gate activation. Tools may use installed Visual Studio and .NET SDK.

**Not authorized:** new global release authority/certificates, approval of complete RecordSift test suite/package dependency closure, full enterprise manifest, actual production migration or merge, production gate, Source Link rollout, or pretending persona synthesis meets real human security review. The owner must separately designate named independent human reviewers and evidence custodian/retention policy in [issue #77](https://github.com/infoconex/dotnet-modernization/issues/77), and approve any production rollout.

**Stop condition:** report exact runtime/packaging evidence and residuals; do not silently expand the experiment or run D2c/production from D2b outcome. **Original Gate C UNSATISFIED; native Gate C-N release NOT_AUTHORIZED; Source Link production HOLD.**
