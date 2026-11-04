# .NET assembly metadata extractor

**Scope:** A standalone .NET 10 command-line tool that reads compiled managed assemblies using the platform's System.Reflection.Metadata and PEReader APIs. It does not load assemblies or execute their code, and does not require the inspected assembly's runtime on the host.

## Output

A single invocation emits three deterministic artifacts directly compatible with the existing Python compatibility comparator:

1. **public-api.txt:** sorted, language-neutral ECMA-335 type/member signature records, including public/protected/protected-internal types and members, generic constraints, nested types, overloads, methods, fields, properties, events, and exported type forwarders.
2. **assembly-identities.json:** schema v1 assembly name, version, culture, public-key token, file version and informational version when available.
3. **resources.json:** schema v1 assembly name and manifest-resource logical names.

These are evidence derived from actual compiled files, unlike manually written contracts.

## Build and run

Requires **exact .NET SDK 10.0.403** to build (selected by the included global.json with roll-forward disabled) and .NET 10 runtime to execute. Input assemblies may target .NET Framework, .NET Standard, or modern .NET, because they are inspected as PE metadata rather than loaded.

    dotnet build tooling/assembly-metadata/src/AssemblyMetadata.csproj -c Release

    dotnet tooling/assembly-metadata/src/bin/Release/net10.0/AssemblyMetadata.dll --assembly /path/to/Domain.dll --assembly /path/to/Application.dll --output-dir /external/evidence/assembly

Pass --assembly one to 100 times. Duplicate assembly paths/names, absent or invalid/nonmanaged files and malformed metadata cause nonzero exit. The tool requires a separate output directory from each assembly input directory and limits input file size to 512 MiB.

No application restore, build, source change, loading, dependency resolution, package publication or network access is performed by the extractor.

## Use with the compatibility comparator

Use the existing [compatibility capture and compare guide](../validators/COMPATIBILITY.md) and [spec example](../validators/examples/compatibility-spec.example.json). Generate baseline and candidate artifacts independently after an approved build, then compare all requested contracts including tests and packages. Use the **same extractor version** on both sides. The text format differs from RecordSift's 425-line API-plus-packaging baseline; do not claim that old gate passed because this extractor produced a matching new baseline.

**Integration without modifying the source checkout:** The companion comparator now supports an external evidence directory via its `--artifacts-root` option. Capture provenance comes from the clean application Git checkout while API/assembly/resource evidence comes from the separate, explicitly identified artifacts directory. The collector SHA-256 fingerprints each input; users still must independently prove that the compiled binaries came from the recorded source revision through their build gates.

## Limitations and acceptance scope

The initial API inventory captures literal field/enum values and metadata constant defaults for parameters, but does **not** fully capture: all custom attributes, nullability annotations, tuple names, COM interop behavior, private explicit-interface implementations, InternalsVisibleTo exposure, native/mixed-mode behavior, and every possible signature modifier. Public/protected access is included according to metadata visibility; other accessibility policies require separate tests. Embedded resources are recorded by **name only**, not content. A public key token is not strong-name signature validation.

A matching snapshot is **not** proof of Windows/.NET Framework execution, binary compatibility, resource contents, consumer installation or package safety. Run those independently using the existing application-specific gates. The extractor cannot replace RecordSift's original public API validator without separate migration/approval.

## Integration tests and CI

Run: python -m unittest discover -s tooling/assembly-metadata/tests -v.

The standard-library Python integration test builds a small C# fixture in a temporary directory and checks identity, namespaced/hidden types, generic and nested types, overloads, methods/fields/properties/events, deterministic output, public API drift, malformed files and compatibility with the Python comparison schema.

The dedicated GitHub Actions workflow provisions exact SDK **10.0.403** on Ubuntu 24.04 and Windows Server 2022. The tests must pass on both. The workflow never modifies RecordSift.

A separately authorized proof using **real RecordSift .NET Framework 4.8 release binaries** remains necessary before claiming production-pilot readiness.
