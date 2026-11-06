# EXP-038 — Exact document URL to native PDB source-checksum stream association

**Status: EXECUTION SUBMITTED; NO EXP-038 RESULT ACCEPTED UNTIL COMPLETE CI EVIDENCE IS INSPECTED.**

Parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37), [EXP-037 issue #58](https://github.com/infoconex/dotnet-modernization/issues/58), [EXP-038 issue #60](https://github.com/infoconex/dotnet-modernization/issues/60). Research branch `research/exp038-pdb-document-stream-key-association-20261105` stacked on draft EXP-037 [PR #59](https://github.com/infoconex/dotnet-modernization/pull/59). Frozen application `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`. No application modification, production package changes, merge, or publication authorized.

## Proven baseline

[EXP-037](EXP-037-compiler-pdb-differential.md) in successful [CI 42115147369](https://github.com/infoconex/dotnet-modernization/actions/runs/42115147369) verified five C# 7.3/net48 direct Roslyn native-PDB fixtures. The same two independently implemented managed readers expose actual SHA256 on the explicit, implicit and deterministic-only controls, yet discover documents **without hashes** when `/pathmap` is added. Read-only MSF7 inspection finds the full physical SHA256 bytes in exactly one native named `/SRC/FILES/` stream in every control, and separately in the actual frozen CSV for **each of four selected source files**. Existing actual managed-document Gate C remains **UNSATISFIED 0/4**; source stream ownership/managed document key equality is the unresolved question.

## Specific hypothesis

Pinned [dnlib 4.5.0](https://github.com/0xd4d/dnlib/blob/v4.5.0/src/DotNet/Pdb/Managed/PdbReader.cs) performs an ordinal-ignore-case named-stream lookup based on `"/src/files/" + managed-document-name`. Pinned [Cecil 0.11.6 vendored CCI](https://github.com/jbevain/cecil/blob/0.11.6/symbols/pdb/Microsoft.Cci.Pdb/PdbFile.cs) constructs `"/SRC/FILES/" + managed-document-name.ToUpperInvariant()`. Both succeed only if the actual PDB named stream lookup resolves. A discrepancy between actual document URL and stream key, potentially due to path mapping, separators or canonicalization, could explain missing reader-exposed digests even when their bytes are physically present.

This is a **hypothesis** until identical managed-document URL values and native named-stream keys are compared within the same bounded execution.

## Experiment and controls

1. Reuse the **actual frozen original + manually Source Link-integrated candidate** EXP-024 validation (425 original public API, 419 NUnit/418 pass/one skip, five XML docs, unpublished local NuGet 0.1.0, independently installed clean net48 consumer and five logical compatibility categories). The application branch, package versions and source bytes are not modified or committed.
2. Retrieve and statically verify exact official, pinned dnlib 4.5.0 and Mono.Cecil 0.11.6 archive and DLL hashes; run existing SHA1/SHA256 source mutation, wrong PDB/PE identity and pathmap differential fixture checks. Managed processes retain explicit outbound firewall block, 20-second timeout and monitored 256 MiB working-set limit.
3. The original EXP-036 reader code includes a **strictly opt-in third argument** to write full document URLs encoded into *ephemeral private files*, never stdout or logs. The EXP-038 orchestrator captures each reader for the same five controlled fixtures and actual frozen CSV and **deletes every private URL manifest in a finally block**, including failed controls.
4. A new, read-only Python audit decodes actual native MSF7 named stream keys (from validated PDB identity) and the structured injected-source stream payload: four GUIDs, two bounded lengths, and exact checksum bytes. The physical owned source is independently SHA1/SHA256 hashed; each must match **exactly one structured source checksum record**. Do not confuse a free-floating byte pattern with a structured record.
5. For each selected document and reader, form the exact version-specific `/src/files/` lookup key from the private original document URL. Compare privately against the source-digest-bearing native named-stream key as **exact, case-insensitive, and separator-normalized**. Record only Boolean classifications, known source basenames, counts, checksum algorithm classes and whether the lookup exists in the complete native name table.
6. Synthetic checks independently exercise exact-positive, case-only, separator-only, mapped-path-different, wrong-document and malformed/truncated structured stream controls. Unexpected duplicates or unmatched physical digest records fail closed. All private full paths/URLs and complete checksum bytes are prohibited from published evidence. No raw PDB, compiled assembly, package archive or binary upload.

## Acceptance and limits

- A fixture/CSV comparison can **verify or falsify** a document-name mismatch hypothesis for those observed owned documents only. A checksum present in a native source stream is not automatically proof that the corresponding managed-reader document exposes it.
- If the source-name lookup is verified **different**, the physical stream/key distinction is measured; the actual native managed-document checksum acceptance is **still UNSATISFIED** until a supported reader or separate approved acceptance mechanism cryptographically associates the bytes with the exact managed document.
- If the lookup is verified **equal** while the reader reports no bytes, pursue another narrowly scoped parser/stream interpretation explanation; never force success.
- This is a fixed four-owned-document audit, not a transitive guarantee for generated/third-party sources or other project assemblies.
- Authentic Visual Studio package installation and debugger source retrieval/stepping **NOT TESTED**. Full compiler server / native writer provenance remains **PARTIAL**. EXP-031's potentially vulnerable native reader remains **SECURITY-BLOCKED**. Source Link adoption **HOLD**, stakeholder approval required for policy change.

## Result

**Pending execution of the new isolated EXP-038 workflow.** Do not use a queued CI run or draft PR as a completed measurement.
