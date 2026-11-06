# Classic Windows PDB document-checksum research validator (EXP-039)

**Status: reusable research tool only.** Do not use its output to approve a Source Link migration or relax Gate C without stakeholder review. [Experiment](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-039-reusable-windows-pdb-checksum-verifier.md) and [issue #62](https://github.com/infoconex/dotnet-modernization/issues/62).

## What the tool proves

`classic_pdb_document_checksums.py` reads a trusted, compiler-generated classic MSF7 Windows PDB and the matching managed PE/DLL without executing the DLL, PDB or native COM parser. It uses the existing bounded `native_windows_pdb_sourcelink.py` MSF and CodeView identity parser; two *independent managed reader* original-URL inventories; and independently declared physical compiler-input files. It validates exact normalized full document keys in native `/SRC/FILES/` streams (slash/backslash and case normalization only), parses the injected record's checksum algorithm GUID, lengths and digest, and compares SHA1/SHA256 digest to the original source file bytes.

It **never** equates same filenames from unrelated directories or substitutes Git remote files for compiler-input bytes. It rejects conflicting reader inventories, missing/ambiguous document-to-native keys, a malformed or unsupported source checksum record, a wrong hash, a missing required source, and basename collisions between explicitly provided physical source files. Native named source streams that neither independent managed reader enumerates are **counted as unexplained**, not silently accepted or rejected as irrelevant. No complete independent native C13 document inventory is currently proven.

## Invocation

Run the library-free synthetic controls on a supported Python 3 environment:

```console
python -m unittest discover -s tooling/validators/tests -p test_classic_pdb_document_checksums.py -v
```

In a private Windows runner with a trusted matched native-PDB pair, run the two pinned readers **inside the established firewall/timeout/memory harness**, writing their exact document-URL inventories privately and erasing those files in a finally block. Pass the private manifests to:

```console
python tooling/validators/classic_pdb_document_checksums.py --dll <compiled.dll> --pdb <compiled.pdb> --dnlib-urls <dnlib-private-manifest> --cecil-urls <cecil-private-manifest> --source-file <physical-source-A.cs> --source-file <physical-source-B.cs> --require-source-name <A.cs> --require-source-name <B.cs> --output <sanitized.json>
```

Each `--source-file` points to the **exact original compiler-input bytes**. For apps with colliding basenames, this first prototype deliberately **fails closed** rather than trying to infer the correct source; a future version must add explicit full-identity source mapping, not loosen path matching. For generated/external sources, obtain the original bytes from a independently trusted source and declare them explicitly, or mark coverage incomplete. No unknown raw metadata may be uploaded.

## Research-only pilot

The dedicated `validate-exp039-reusable-pdb-checksums.yml` workflow:
- Checks out immutable `RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8`.
- Repeats both original and experimental manual Source Link candidate 425 API / 419 NUnit / five XML / original unpublished local NuGet package / clean consumer / five logical compatibility categories.
- Reuses the exact pinned official managed dnlib and Cecil archive preflight, and the existing native PDB identity, SHA1/SHA256 fixture, wrong-PDB, mutation, and pathmap negative controls.
- Tests each of five controlled direct Roslyn fixture variants and all four selected frozen CSV source files using the reusable validator against **private reader URL inventories**.
- Writes only sanitized JSON with counts, classifications, algorithm labels and fixed known source basenames; private full document URLs are removed in `finally`.

## Output interpretation

`source_hashes_matched` counts distinct cryptographically validated declared physical compiler-input files. `managed_document_count` is the independently agreed **managed reader discovery count**, not a proved all-C13-document inventory. `native_named_source_stream_count` counts all native named `/SRC/FILES/` streams; `unmatched_native_source_streams` records those not connected to either reader's managed document URL, and must be investigated before declaring comprehensive coverage. `reader_documents_without_supplied_physical_source` counts missing compiler inputs. The `inventory_completeness` field means only the named-stream and managed-reader-discovered-document inventories are internally reconciled: it does **not** prove that unrelated native document records or other assemblies are absent.

Even when all declared physical source checksums pass, `gate_c` remains `NOT_EVALUATED_FOR_POLICY_REPLACEMENT`. The unmodified managed readers may still expose no hashes; the current Gate C cannot be silently replaced with this native structural verification. Real Visual Studio Package Manager project installation, Visual Studio Source Link source retrieval/breakpoint stepping, full all-assembly PDB document coverage and general hostile-input safety remain outside this pilot.

## Extension checklist for a future application

Use an immutable source commit, record exact compiler/build host and DLL/PDB formats, enumerate the independent managed document inventory, provide **the exact full compiler source inputs**, make explicit source-identity mappings if basename collisions exist, verify per-document native structured source hashes and all extra streams, include negative controls, validate full original API/tests/XML/package/consumer behavior, and obtain stakeholder approval separately for *any* change of acceptance methodology.
