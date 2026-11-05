# EXP-037 — Traditional MSBuild versus direct Roslyn native-PDB checksum differential

**Status (November 5, 2026): VERIFIED CONTROLLED PATHMAP DIFFERENTIAL AND PHYSICAL PDB DIGEST PRESENCE; REAL MANAGED CHECKSUM GATE STILL UNSATISFIED.**

Research scope: [issue #58](https://github.com/infoconex/dotnet-modernization/issues/58), [EXP-036 results](EXP-036-managed-pdb-source-checksums.md). Frozen application: `RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`. Source Link production adoption remains **HOLD**.

## Research question and competing explanations

EXP-036 directly verified full SHA1 and SHA256 source-byte hashes in two independent managed parsers on known-good Roslyn native PDB fixtures, but found 4/4 real RecordSift documents with **no managed checksum bytes** through either parser. The gate fails closed; neither physical absence nor root cause is established.

- H1: the direct fixture's explicit `/checksumalgorithm` flag is essential; the legacy candidate may omit it.
- H2: deterministic compilation, `/pathmap`, or `/sourcelink` alters classic-PDB checksum emission or the managed reader's interpretation.
- H3: the compiler server/MSBuild Csc task uses different executable or symbol-writer implementations than direct `csc.exe`.
- H4: the physical PDB stream layout differs even where documents are enumerated, independently of managed reader presentation.

## Preconditions and controls

Use **only** disposable Windows 2022 checkout at exact frozen RecordSift SHA. Reuse EXP-024 unchanged full baseline and manually integrated candidate acceptance (425 original API, 419 NUnit/418 pass/one skip, five XML, original unpublished local NuGet package, clean .NET Framework 4.8 consumer and five logical compatibility categories). No Visual Studio Package Manager installation equivalence is claimed.

Retrieve only exact pinned official archives `dnlib 4.5.0` and `Mono.Cecil 0.11.6`, rerun existing bounded archive preflight and fixture code. Each managed reader runs as an isolated process with outbound firewall denial, 20-second execution timeout, monitored 256 MiB working set and no native COM reader opt-in. Do not load arbitrary or adversarial PDBs. Verify actual MSF7 and PE/PDB identity.

## Experimental method

1. Run EXP-024 on a fresh frozen checkout and examine its **private** diagnostic log from the real CSV Csc task. Reusable `tooling/pilots/recordsift/EXP-037/compiler_capture.py` records only observed, allowlisted switch categories, and whether the Csc invocation itself was discoverable. Unknown switches remain **UNKNOWN**, never inferred absent. It never uploads physical paths, command-line transcripts or source.
2. Preserve EXP-036 SHA1/SHA256 explicit-flag fixtures as positive controls. Compile five additional C# 7.3/net48 native-PDB controls from **identical compiler-input source path and bytes** using the same direct VS Roslyn executable: **explicit SHA256**, **no checksum switch**, **explicit SHA256 + deterministic**, **explicit SHA256 + deterministic/pathmap**, and **explicit SHA256 + deterministic/pathmap/SourceLink**. Adjacent comparisons differ by one option; the explicit SHA256 control is reused when assessing the deterministic difference. Use a synthetic Source Link URL and explicitly do not claim Git provenance from the fixture. Require both independent parsers to agree and match the physical input file hash.
3. Independently compare `/SRC/FILES/` named-stream counts, Source Link stream counts, and native PE/PDB identities with the existing read-only `named_stream_gap.py`; then use `EXP-037/pdb_digest_scan.py` to locate exact physical SHA1/SHA256 digests and classify whether their host stream is an MSF7 named `/SRC/FILES/` stream. Print **only** stream roles, source basenames, occurrence counts and Boolean classification against known physical/controlled mapped source paths. None of these binary checks proves correct managed-document association.
4. Keep final sanitized metadata only, with accurate run ID, research SHA, failure observations and limitations. For a concrete compiler-input difference, follow with a smaller single-variable reproduction. Do not declare a root cause from two correlated changes.

## Acceptance / negative cases

- Compiler log synthetic tests must prove path/reference arguments are stripped, expected switch values remain, and an empty Csc task does not falsely report switches.
- Each fixture case must have native MSF7 PDB identity. Each parser must independently identify the same document and either report a matching physical source-byte digest or explicitly classify `DISCOVERED_WITHOUT_HASH`. Unexpected/missing documents, conflicting reader classification, mismatched present hashes, or bad PDB identity still fail the diagnostic harness. Missing hashes are preserved as negative observations and **do not** pass Gate C.
- Existing wrong-DLL/PDB and source-mutation controls remain negative (EXP-036).
- If the private diagnostic transcript does not expose a full compiler invocation, mark exact candidate effective arguments as **PARTIAL**, not verified. Compiler-server identity and loaded writer remain open until direct evidence exists.
- Actual frozen candidate Gate C remains **UNSATISFIED** regardless of synthetic fixture outcomes.
- The investigation must not commit the RecordSift application, upgrade dependencies, merge research PRs or publish artifacts containing source/PDB/binaries/secret paths.

## Results

### Verified primary execution

**Final diagnostic [Windows run 42115147369](https://github.com/infoconex/dotnet-modernization/actions/runs/42115147369)** at research SHA `d2be221081444892d30a0deff0b56d91efefd0e8`: **PASS**, including the unchanged frozen baseline and manually integrated candidate release/consumer acceptance (425 API, 419 tests with 418 pass and one expected skipped, five XML, original unpublished local package, clean consumer, five logical compatibility categories). Correct source commit `8358780829458854a4b0356df5ac5e685f0a34c8`; no application changes or research merges. All native DLL/PDB CodeView GUID/age identities passed, official reader archive preflight passed, and EXP-036 independent SHA1/SHA256 controls, wrong-PDB and source-mutation negatives passed.

Exact artifact: [metadata-only artifact 13456185828](https://github.com/infoconex/dotnet-modernization/actions/runs/42115147369/artifacts/13456185828), GitHub-reported ZIP digest `sha256:00b62d1e10e56399922b25d3e832d16e92c61ea09cc3255d034f0d07199e02bb` (30-day retention). Contains **sanitized JSON only**, never source, DLL, PDB, raw compiler logs, URL keys, package archives or private absolute paths. An earlier [successful differential and raw-byte control 42114250192](https://github.com/infoconex/dotnet-modernization/actions/runs/42114250192) at SHA `d6e97ab487b8dcda0dc6c2521db47a2d9bc0a54c` first confirmed raw SHA256 bytes in all six candidate categories; artifact 13454359338, digest `sha256:c334dc5caae51dd009f942f43dd029f462d94023df9b9eba01ce0770f6812c8d`. Initial harness failures [42112584150](https://github.com/infoconex/dotnet-modernization/actions/runs/42112584150) and [42112968117](https://github.com/infoconex/dotnet-modernization/actions/runs/42112968117) are retained: they correctly identified negative fixture outcomes but aborted before classifying all variants. The corrected protocol records negative outcomes without conflating diagnostic CI success with checksum acceptance.

### Actual effective compiler configuration (partial capture)

Actual frozen candidate diagnostic transcript contained one `Csc` task and one compiler-command evidence line. Sanitized observations: `/debug:pdbonly`, `/deterministic+`, `/pathmap`, `/sourcelink`, `/langversion:7.3`, `/optimize+`, `/nostdlib` and expected output/reference switches. No explicit `/checksumalgorithm` was **observed**; its actual effective value remains unproven by that absence alone. The trusted **direct-csc** fixture executable was Roslyn 4.14.0-3.26424.7, SHA256 `cf32cb7e8e5691b962e1b6f92b03d87409dd9e7afbed71c5bf77b8203cc56ee1`. The actual Csc task's executable/assembly SHA256, server invocation identity and native symbol writer are **not** independently established; they must not be inferred from the fixture compiler's location.

### Single-variable direct-Roslyn controls — the pathmap distinction

All five controls use **the same physical compiler-input path and bytes**, `/debug:pdbonly`, C# 7.3/net48 and `/optimize-`:

| Controlled configuration | dnlib 4.5.0 | Cecil 0.11.6 | Physical source SHA256 digest in native PDB |
|---|---|---|---|
| Explicit SHA256 / nondeterministic | matched exact bytes | matched exact bytes | 1, in named `/SRC/FILES/` stream |
| No explicit checksum switch / nondeterministic | matched SHA256 exact bytes | matched SHA256 exact bytes | 1, in named `/SRC/FILES/` stream |
| Explicit SHA256 / deterministic only | matched exact bytes | matched exact bytes | 1, in named `/SRC/FILES/` stream |
| Deterministic + pathmap | **document found; digest absent** | **document found; digest absent** | **1, in mapped-name `/SRC/FILES/` stream** |
| Deterministic + pathmap + synthetic Source Link | **document found; digest absent** | **document found; digest absent** | **1, in mapped-name `/SRC/FILES/` stream** |

Adding `/pathmap` to this deterministic direct-compiler fixture is **sufficient to reproduce** the managed-parser checksum-extraction discrepancy; deterministic compilation alone and Source Link are not necessary to reproduce it. The physically stored digest bytes *do not disappear*; stream names in the mapped controls resolve to the controlled mapped source path rather than the original input path.

### Actual frozen RecordSift — physical evidence narrows the explanation

For all four selected owned CSV files, each *physical compiler-input SHA256 digest* occurs **exactly once in a native named `/SRC/FILES/` stream** in the actual candidate PDB, with matched PE/PDB CodeView identity. The actual CSV PDB contains **seven nonempty `/SRC/FILES/` named streams** and one Source Link stream. These source stream names are not equal to the physical source path; the mapped fixture's synthetic `/_/` prefix is not a valid comparison for the real candidate's mapping, so its exact mapping remains unclassified. The separate EXP-036 managed-document observation remains **4 discovered, 0 with exposed hashes in each reader**.

This **disproves the narrow hypothesis that the SHA256 input-byte digests are physically absent from these tested PDBs**. It does **not** independently prove that a digest-bearing source stream is properly associated with the corresponding C13/managed document, nor that the native writer or parsers are incorrect.

### Pinned upstream implementation evidence and remaining gap

Independently fetched exact published-tag source:
- [dnlib v4.5.0 `PdbReader.GetDocument`](https://github.com/0xd4d/dnlib/blob/v4.5.0/src/DotNet/Pdb/Managed/PdbReader.cs) constructs the lookup `$"/src/files/{name}"`, reading its digest-bearing content only if that named stream resolves.
- [Cecil 0.11.6 vendored CCI `ReadSourceFileInfo`](https://github.com/jbevain/cecil/blob/0.11.6/symbols/pdb/Microsoft.Cci.Pdb/PdbFile.cs) constructs `"/SRC/FILES/" + name.ToUpperInvariant()` and loads checksum GUID and bytes from that stream if found. Cecil and Microsoft CCI are **one parser family**, not two independent readers.

**Supported interpretation:** both managed parsers discover actual source documents, while checksum-bearing named source streams demonstrably exist; changing `/pathmap` reproduces that mismatch in a controlled fixture. The leading *mechanism hypothesis* is inconsistency between **the exact document-name string used for lookup and the exact named-stream key** (possibly path encoding/separator/canonicalization). This **specific equality mismatch has not yet been proved**, because no raw document URLs/stream keys were retained or correlated. Do not call it a verified reader bug or a missing PDB checksum record.

**Smallest next justified experiment:** within the isolated trusted runner, compare each C13/managed document's exact lookup key against the native PDB named-stream key **in memory**, record only per-file Boolean exact-match/canonicalized-match categories, and verify the digest contents using the pinned bounded readers or independent structured stream parsing. Never upload the keys. Do this before speculative writer-version changes or switching PDB format. Candidate compiler server identity remains a distinct secondary gap.

**Disposition:** EXP-037 controlled pathmap/raw-stream distinction **VERIFIED**; actual managed Gate C **UNSATISFIED / FAIL-CLOSED**; compiler host/writer identity **PARTIAL**, authentic VS project-install/debugger gates **NOT TESTED**, Source Link adoption **HOLD**.

## Independent review rubric

**Build engineering:** distinguish Csc task property values from emitted arguments; distinguish `csc.exe` and `VBCSCompiler.exe` invocation/assembly hashes from simply discovering an installed executable.

**Architecture:** do not modify source code or dependency contracts to make checksum verification easier; reuse existing project-specific acceptance procedures.

**Security:** process only trusted fixtures/frozen PDBs, retain package hashes, isolate parsers, redact private log bytes, prevent artifact leakage.

**Quality:** preserve explicit negative results, require hash bytes not only document count, account for native-stream limitations, and keep independently verified dimensions separate.

**Decision:** Source Link adoption is **HOLD**; stakeholder approval remains required for any gate-policy changes or production modernization.
