# EXP-038 — Exact document URL to native PDB source-checksum stream association

**Status (November 5, 2026): VERIFIED FOR FIVE CONTROLLED FIXTURES AND FOUR FROZEN CSV OWNED DOCUMENTS; NO ADOPTION OR GATE POLICY CHANGE.**

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

## Verified execution and evidence

**[Successful Windows 2022 run 42148192785](https://github.com/infoconex/dotnet-modernization/actions/runs/42148192785)** on isolated draft PR #61 at research SHA `fea65001d757d824ff1d908dd5baed5844b42db0` (workflow completed SUCCESS). [Metadata-only artifact 13471336047](https://github.com/infoconex/dotnet-modernization/actions/runs/42148192785/artifacts/13471336047), GitHub-reported archive digest `sha256:723e444ff56fa29c47d1843e5dedce673b6e2c5dafdd99fbabe6c58dab904c54` (30-day retention). The artifact contains only bounded JSON, source basenames, match categories, counts and approved compiler option metadata. No raw full document URL, named key, compiler transcript, physical source, DLL, PDB, archive or private manifest uploaded.

- **Prerequisites PASS:** exact pinned official dnlib 4.5.0 and Cecil 0.11.6 archive preflight, independently compiled managed-only reader fixture, real MSF7 native PDB and DLL/PE CodeView GUID+age identities, original EXP-036 SHA1 and SHA256 source hash fixtures, wrong PE/PDB and source-mutation negative controls, EXP-037 five compiler-switch variants, and the EXP-024 frozen application original + candidate release gates: **425 public API entries, 419 NUnit (418 pass, zero fail, one expected skip), five XML docs, unpublished local NuGet 0.1.0, clean net48 consumer, five logical compatibility categories matched**. No application source change or package upgrade.
- **Structured native evidence PASS:** each known compiler-input source SHA256 matches exactly one *parsed source-checksum record* with algorithm GUID and bounded checksum bytes inside a native `/SRC/FILES/` named stream. This is stronger than EXP-037's raw-byte occurrence; it uses the real injected source metadata structure. All four selected frozen CSV records matched their actual physical compiler-input bytes; there are seven total nonempty native named source streams in the CSV PDB. Other owned, generated or external records are not automatically accepted.
- **Managed reader URL inventory:** the same bounded and official pinned dnlib/Cecil reader processes captured exact source URLs in private ephemeral files only. Read-only structural analysis compared the precise reader-derived lookup key with the native PDB named key for the physically verified source. **All private full URL manifests were erased by the `finally` block before artifact upload.**

### Exact key comparison results

Both independent reader families (dnlib 4.5.0 managed, Cecil 0.11.6 managed/CCI) produced identical classifications:

| Build/control | Exact case-sensitive key | Case-insensitive key | Separator normalized + casefold | Reader exposes hash |
|---|---|---|---|---|
| Explicit SHA256, nondeterministic | False | **True** | **True** | **Yes** |
| Implicit checksum, nondeterministic | False | **True** | **True** | **Yes** |
| Deterministic-only, explicit SHA256 | False | **True** | **True** | **Yes** |
| Deterministic + `/pathmap` | False | **False** | **True** | **No** |
| Deterministic + `/pathmap` + synthetic Source Link | False | **False** | **True** | **No** |
| Frozen CSV `CharacterLimitedTextReader.cs` | False | **False** | **True** | **No** |
| Frozen CSV `CsvRecordReaderAdapter.cs` | False | **False** | **True** | **No** |
| Frozen CSV `CsvStreamImporterAdapter.cs` | False | **False** | **True** | **No** |
| Frozen CSV `MalformedCsvException.cs` | False | **False** | **True** | **No** |

The exact (case-sensitive) strings also differ in the *working unmapped* controls, so **case-sensitive equality is not the reader's real acceptance criterion**. Both pinned upstream implementations construct keys from the returned managed document URL and compare them against native PDB named stream names using case-insensitive/uppercase semantics, but without the separator-normalization needed in the mapped cases.

**Verified bounded mechanism:** the mapped controls and all four frozen CSV sources have a source-document lookup that fails case-insensitive key matching yet succeeds **once `\\` and `/` separators are normalized and the result casefolded**. The native named checksum stream remains present and contains the correct cryptographic source-byte digest. This accounts for the exact observed managed `DISCOVERED_WITHOUT_HASH` behavior in the tested cases. It is not a claim that the whole PDB has incorrect metadata or that Roslyn omitted source hashes, and does not generalize to all Roslyn/PDB/version combinations.

### Independent adversarial assessment and remaining constraints

**Build engineering:** the controlled five-case experiment holds source input path/bytes, compiler executable and optimization fixed. The actual CSV traditional MSBuild invocation contains `/pathmap` and `/sourcelink`; exact host compiler-server/writer identity is still **PARTIAL**, but it is not needed to demonstrate this reproduced path/key mismatch.

**Quality:** synthetic tests cover exact-match, case-only, slash-only, same-basename/wrong-directory, different filename, correctly shaped SHA256 record, truncated/malformed-size record and missing stream; wrong identity/source mutation controls are inherited and passed. The parser checks GUID, lengths, uniquely matching physical digest and exact source key relation, not substring occurrence alone. The result does *not* silently accept same-basename matching as equivalent to exact path.

**Security:** trusted locally compiled input PDBs only; pinned managed readers under firewall, time and memory guard, no native vulnerable reader, private URL manifests erased even upon failure; only sanitized classifications uploaded. The tool is **not** approved for hostile arbitrary PDBs; full process sandboxing and third-party malformed-input robustness remain unverified.

**Architecture:** no frozen application source, API, target framework, package graph or build contract changed. All historical compatibility gates passed against the original and isolated manually integrated candidate. Conventional Visual Studio package installation was not simulated or asserted.

**Decision governance:** this experiment verifies *native cryptographic source digest and a path-key association explanation for the selected four owned CSV files*. It does **not** change the existing Gate C wording requiring actual **managed-document checksum authenticity across the relevant document inventory**, and it does **not** establish that the unmodified third-party managed readers can expose those hashes. An optional **independent normalized-path, structured native source-record verifier** could be proposed as an alternative evidence pathway, but such a change of acceptance criteria or implementation must be explicitly approved, with missing/generated/external document coverage and hard negative controls.

**Final disposition:** EXP-038 **VERIFIED** on the bounded source/document set; EXP-036 managed reader exposure remains **0/4**, Gate C **UNSATISFIED / FAIL-CLOSED**, actual Visual Studio Package Manager installation and remote-source debugger stepping **NOT TESTED**, EXP-031 vulnerable native reader still **SECURITY-BLOCKED**, Source Link production adoption **HOLD**. All research PRs remain draft, with no merge or NuGet publication.

