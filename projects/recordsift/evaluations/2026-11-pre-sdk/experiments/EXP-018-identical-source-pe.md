# EXP-018 — identical-source managed PE reproducibility evidence

**Assessment:** November 4, 2026. **Status:** Proposed; independent CI validation pending.
**Frozen application:** infoconex/RecordSift, main SHA 8358780829458854a4b0356df5ac5e685f0a34c8. No application source or branch modification authorized.

## Question

EXP-017 [draft PR #30](https://github.com/infoconex/dotnet-modernization/pull/30) found all five packaged RecordSift DLLs differ in SHA-256 between two independent Release builds of the exact same frozen Git commit. Why? Which *observable* PE and CLR metadata fields differ? Does rebuilding in the **same source directory** also cause differences? Do raw method IL bytes differ?

A binary hash mismatch does not by itself prove an API, functional, security or runtime incompatibility.

## Three actual immutable-source builds

The [EXP-018 Windows runner](../../../../../tooling/pilots/recordsift/EXP-018/run.ps1) and [read-only workflow](../../../../../.github/workflows/validate-recordsift-pe-reproducibility.yml) use:

1. **Original checkout:** frozen RecordSift source, NuGet restore and Release rebuild of all ten traditional projects.
2. **Independent detached worktree:** exactly the same Git source SHA, separate filesystem checkout, independent restore and rebuild.
3. **Same-path rebuild:** another restore and Rebuild in the original checkout path, after the first PE evidence has already been saved.

For **all three** builds, require the original compiled 425-entry public API baseline, five NUnit suites (419 tests, 418 passed, zero failed, one skipped), five XML docs, unpublished 0.1.0 local package, independent installed net48 consumer and Getting Started examples. Verify each Git revision and unchanged tracked source. No commits or pushes to RecordSift.

Before building, evaluate *actual* Release MSBuild properties across five production projects and the two independent checkout paths: Deterministic, DebugType, DebugSymbols, PathMap, ContinuousIntegrationBuild, Optimize, LangVersion, PlatformTarget. Require 80 recorded values and parity across worktrees; do not assume these are the complete effective compiler command line.

## Reusable reader and comparator

[PeProvenance.cs](../../../../../tooling/pe-provenance/src/Program.cs) is a .NET 10 metadata-only PE reader using System.Reflection.Metadata, without loading or executing application code. Per managed DLL it captures exact file SHA-256/size, assembly identity, MVID, COFF timestamp, PE format, debug directory (including CodeView GUID/age), PDB basename and *hash of full PDB path* (never an unhashed absolute path), and byte SHA-256 per raw method IL body indexed by metadata token.

[pe_variation.py](../../../../../tooling/validators/pe_variation.py) compares the three snapshots. It separately reports binary hash changes, MVID/COFF/debug differences and changed raw IL byte tokens in distinct-path and same-path rebuilds. Different or matching hashes are legitimate observations; missing or malformed evidence must fail closed. [Fixture tests](../../../../../tooling/validators/tests/test_pe_variation.py) cover no-change, MVID/COFF, debug and IL changes plus missing/ambiguous evidence.

The application-specific runner owns the RecordSift SHA, five component names, NuGet/MSBuild/NUnit invocation and legacy acceptance gates. It does not make these universal defaults for unrelated .NET projects.

## Acceptance and interpretation

Actual Windows CI must build both .NET metadata tools with pinned SDK 10.0.403, pass Python fixture tests, verify all three separately accepted Release builds and output versioned per-assembly reports. Reusable Python tests must pass in both Linux and Windows environments. Retain the full source SHA, MSBuild settings, JSON/PE hashes and NUnit/consumer results in a 30-day research artifact; **never upload compiled DLL, PDB or nupkg bytes**. Keep PR draft/unmerged until review.

PE/MVID/PDB and raw IL hashes are *not* by themselves a causal explanation. Even identical raw IL does not prove that runtime semantics, custom attributes, resources, assembly binding or packaging bytes match. The repeated builds are not hermetic; worktrees, output locations, clocks, compiler toolchain, environment and NuGet caches can vary. A COFF field may be a reproducible-build stamp rather than a wall-clock time.

**Next decision only after evidence:** whether to study explicit deterministic compiler settings and PathMap/PDB controls in disposable source workspaces. No production build change is requested here.

**Review lenses:** .NET architecture, MSBuild/compiler, QA/release, reusable tooling design, security/supply-chain and developer documentation. These are analytical perspectives, not external human reviews.

**Results:** Pending verified Actions run and artifact.
