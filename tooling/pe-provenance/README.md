# Managed PE provenance reader (evidence-only)

This is a small .NET 10 command-line tool for inspecting **existing managed PE files**. It never calls Reflection Assembly.Load, loads a RecordSift DLL for execution, modifies application code, or invokes a compiler. It uses .NET System.Reflection.Metadata and PEReader to inspect the raw file and associated CLR tables without requiring Visual Studio or net48 at execution time.

## Build and run

Requires a .NET 10 SDK; the EXP-018 Windows workflow pins 10.0.403.

    dotnet build tooling/pe-provenance/src/PeProvenance.csproj -c Release

    dotnet tooling/pe-provenance/src/bin/Release/net10.0/PeProvenance.dll --assembly /path/original/Library.Domain.dll --assembly /path/original/Library.Application.dll --output /outside/source/original-pe.json

One to 100 unique managed assembly inputs are accepted per run. Output must be a new file, not adjacent to an input binary. Fail closed on missing/invalid/unmanaged input, duplicate CLR assembly names, oversized input, invalid method bodies and reused output files. JSON schema v1 records actual input size and SHA-256, CLR assembly/version, MVID, COFF header timestamp, PE format, debug directory values and (when present) CodeView GUID/age, PDB basename and hash of PDB path, and per-method raw IL byte hashes indexed by CLR method definition metadata token. No IL text or PDB path is emitted.

To compare three independent reports:

    python tooling/validators/pe_variation.py --original /evidence/original-pe.json --independent /evidence/other-checkout-pe.json --same-path-rebuild /evidence/rebuild-pe.json --output /evidence/pe-variation-comparison.json

The comparator requires the same assembly-name set across all three reports and reports exact binary SHA-256, MVID, COFF, PDB/debug and raw method IL token differences. Exit 0 indicates **successful evidence comparison**, NOT byte compatibility: actual matches and differences are both valid observations. Malformed or missing evidence exits nonzero. See portable fixture tests in tooling/validators/tests/test_pe_variation.py.

## Interpretation and limitations

- The MVID and PDB records are **evidence of metadata**, not a standalone explanation of why binaries differ; the COFF timestamp is not necessarily a wall-clock timestamp.
- Exact raw method IL hash equality does not cover attributes, metadata tables, signatures, resources, binding, native images, PDB bytes or runtime behavior. IL token values can change across builds, so the comparison is raw-token evidence, not semantic normalization.
- A DLL byte mismatch from two distinct worktrees can reflect paths, compiler inputs, environment, or nondeterminism. A same-path rebuild is a valuable extra control but still does not make builds hermetic.
- The full original PDB source path is hashed but still correlated through its digest; inspect where evidence is shared. Some metadata fields may contain application names and versions.
- Do not use PE inspection as a substitute for frozen-source attribution, MSBuild property evaluation, all unit/acceptance gates, NuGet package comparison, ABI/binary binding analysis or security review.

## Real Windows case study

[RecordSift EXP-018](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-018-identical-source-pe.md) uses an independent adapter and full traditional .NET Framework 4.8 release gates. [Run 41901750747](https://github.com/infoconex/dotnet-modernization/actions/runs/41901750747) found **all five DLL file hashes, MVIDs, COFF stamps and debug-directory records changed** in both a separate-checkout and same-checkout rebuild of the identical frozen source; no raw method IL byte record changed. This is a scoped evidence observation, not proof of semantic equivalence or a recommended RecordSift production change.

The reusable reader is application-agnostic. The 10 project files, 419 test counts, 425 historical API records, CSV/XLSX samples, and immovable RecordSift source revision belong **only** to the RecordSift-specific EXP-018 adapter.
