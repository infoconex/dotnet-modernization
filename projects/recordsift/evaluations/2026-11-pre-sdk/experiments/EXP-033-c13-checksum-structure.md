# EXP-033 — Non-executing independent CodeView C13 checksum-structure probe

**Status:** Read-only research, Windows CI required. Stacked draft after EXP-032; RecordSift frozen at `8358780829458854a4b0356df5ac5e685f0a34c8`.

## Why this experiment exists

EXP-029's LLVM native PDB `dump -modules -files -l` displayed five source-file rows marked `(no checksum)`. EXP-031 proposed using a managed COM wrapper but **cannot safely execute** because the Microsoft advisory's patched NuGet `Microsoft.DiaSymReader.Native 18.9.0-beta1.26405.2` was not publicly available. This phase tries an independent *existing preinstalled LLVM* CodeView C13 raw-chunk inspection without running the vulnerable native NuGet package.

## Verification steps

1. Build the existing disposable Source Link net48 candidate at the frozen commit and rerun 425 API, 419 NUnit, five XML, local NuGet/package-installed consumer and five logical compatibility categories.
2. Independently validate the native MSF7 `sourcelink` stream and DLL/PDB CodeView GUID/age (EXP-025 reader).
3. Use preinstalled `llvm-pdbutil bytes -chunks -split-chunks` to display module C13 CodeView substreams, in addition to the earlier `dump -modules -files -l` view; inspect whether checksum subsections are represented in the independent view.
4. Store **counts and classifications**, not raw LLVM dumps, developer source paths, compiler command line or PDB bytes.
5. **Never claim per-document checksum verification** from a text marker or the lack of one: even C13's `DEBUG_S_FILECHKSMS` format is not automatically identical to managed DiaSymReader document records. A confirmed native documented format and actual digest-to-compiler-input byte comparison remains a separate acceptance gate.

**Technical reference:** LLVM `llvm-pdbutil` command guide documents `bytes -chunks -split-chunks` as raw C13 module subsection inspection: https://llvm.org/docs/CommandGuide/llvm-pdbutil.html.

This is a deliberate bounded investigation, not authorization to install Source Link via conventional Visual Studio NuGet Manager, to publish, to merge or to modify RecordSift.

## Verified Windows CI result

**[EXP-033 Windows run 41984248522](https://github.com/infoconex/dotnet-modernization/actions/runs/41984248522) succeeded** at research SHA `b383eb8341e22b34a022d50f65a08dc572161c10` and retained [artifact 13395746030](https://github.com/infoconex/dotnet-modernization/actions/runs/41984248522/artifacts/13395746030), SHA256 ZIP `c614c3711ded8d1044bf30ae3302de84c76f6650c71e1da933509c1f6fd743f1`, independently downloaded and parsed. Immutable RecordSift source and original provider-integrated Release/consumer gates passed. PDB native Source Link stream/JSON and matched PE CodeView identity passed.

The independent LLVM `dump -modules -files -l` reported **five `(no checksum)` source-file rows**, matching EXP-029. Separately, `bytes -chunks -split-chunks` exited **0**, yielded **119 lines**, with **zero text indicators of C13 file checksum subsections**. These are bounded tool-output observations, NOT an independent cryptographic proof that all managed `ISymUnmanagedDocument` checksum records are absent. As specified, the report retains `per_document_checksum_digest_validation=NOT_VERIFIED` and `source_input_byte_identity=NOT_VERIFIED`. The absence of a textual marker must not be promoted into a universal binary-structure claim.

**Verdict: VERIFIED_INDEPENDENT_LLVM_C13_INVENTORY_WITH_NO_CHECKSUM_INDICATORS; full native managed PDB document checksum gate REMAINS UNVERIFIED.** EXP-031 patched native PDB reader remains security-blocked until its audited patch is available; do not execute a vulnerable fallback. No application changes, merges, binaries/PDB uploads or publication.
