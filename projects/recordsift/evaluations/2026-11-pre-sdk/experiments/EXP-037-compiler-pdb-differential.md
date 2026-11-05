# EXP-037 — Traditional MSBuild versus direct Roslyn native-PDB checksum differential

**Status:** INITIAL EXPERIMENT SUBMITTED; NO EXP-037 RESULTS ACCEPTED YET.

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
3. Independently compare exact `/SRC/FILES/` named-stream *counts and sizes*, Source Link named-stream counts, and native PE/PDB identities for original SHA1/SHA256 fixtures and the actual frozen CSV candidate using the existing read-only `named_stream_gap.py` validator. This is **not** a managed checksum parser; stream-count differences cannot alone locate missing digest bytes.
4. Keep final sanitized metadata only, with accurate run ID, research SHA, failure observations and limitations. For a concrete compiler-input difference, follow with a smaller single-variable reproduction. Do not declare a root cause from two correlated changes.

## Acceptance / negative cases

- Compiler log synthetic tests must prove path/reference arguments are stripped, expected switch values remain, and an empty Csc task does not falsely report switches.
- Direct compiled fixture cases must all have actual native MSF7 PDB identity and both managed readers must match compiler-input checksum bytes. A failed variant is a finding, not an application-compatibility failure.
- Existing wrong-DLL/PDB and source-mutation controls remain negative (EXP-036).
- If the private diagnostic transcript does not expose a full compiler invocation, mark exact candidate effective arguments as **PARTIAL**, not verified. Compiler-server identity and loaded writer remain open until direct evidence exists.
- Actual frozen candidate Gate C remains **UNSATISFIED** regardless of synthetic fixture outcomes.
- The investigation must not commit the RecordSift application, upgrade dependencies, merge research PRs or publish artifacts containing source/PDB/binaries/secret paths.

## Results

**Pending the first EXP-037 workflow and inspection of its actual steps and metadata artifact.** Do not interpret this document or a workflow's mere existence as proof of successful execution.

## Independent review rubric

**Build engineering:** distinguish Csc task property values from emitted arguments; distinguish `csc.exe` and `VBCSCompiler.exe` invocation/assembly hashes from simply discovering an installed executable.

**Architecture:** do not modify source code or dependency contracts to make checksum verification easier; reuse existing project-specific acceptance procedures.

**Security:** process only trusted fixtures/frozen PDBs, retain package hashes, isolate parsers, redact private log bytes, prevent artifact leakage.

**Quality:** preserve explicit negative results, require hash bytes not only document count, account for native-stream limitations, and keep independently verified dimensions separate.

**Decision:** Source Link adoption is **HOLD**; stakeholder approval remains required for any gate-policy changes or production modernization.
