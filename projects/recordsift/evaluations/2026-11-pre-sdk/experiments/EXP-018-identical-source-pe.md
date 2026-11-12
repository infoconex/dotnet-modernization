# EXP-018 — identical-source managed PE reproducibility evidence

**Assessment:** November 4, 2026. **Status:** Proposed; independent CI validation pending.
**Frozen application:** infoconex/RecordSift, main SHA 8358780829458854a4b0356df5ac5e685f0a34c8. No application source or branch modification authorized.

## Question

EXP-017 [draft PR #30](https://github.com/infoconex/dotnet-modernization/pull/30) found all five packaged RecordSift DLLs differ in SHA-256 between two independent Release builds of the exact same frozen Git commit. Why? Which *observable* PE and CLR metadata fields differ? Does rebuilding in the **same source directory** also cause differences? Do raw method IL bytes differ?

A binary hash mismatch does not by itself prove an API, functional, security or runtime incompatibility.

## Three actual immutable-source builds

The [EXP-018 Windows runner](../../../../../tooling/pilots/recordsift/EXP-018/run.ps1) and [read-only workflow](../archives/workflows/validate-recordsift-pe-reproducibility.yml) use:

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

## Verified evidence — three real builds with identical Git source

[Successful Windows run 41901750747](https://github.com/infoconex/dotnet-modernization/actions/runs/41901750747), research SHA ade83c20d4942ebb5b34bd34a38e68e5d9b508cf (before documentation and enhanced property-log commits). [Evidence artifact 13359585654](https://github.com/infoconex/dotnet-modernization/actions/runs/41901750747/artifacts/13359585654), SHA-256 d42b59068654f3274a69a2d8580fd1c09f3bbb02e8fc6b9bda1520cd9226dd43, 30-day retention. The real original application Git SHA remained 8358780829458854a4b0356df5ac5e685f0a34c8 in all three builds. No app source files were modified and nothing was pushed or published.

Each complete solution was independently restored and Rebuilt (all 10 traditional projects) using Windows 2022 Visual Studio MSBuild. **Each passed** the original **425-entry** compiled API gate, **419/418/0/1** NUnit tests across five assemblies, five XML docs, locally packaged 0.1.0, separate installed net48 consumer and Getting Started examples. The predecessor EXP-014 same-binary metadata repeats also matched, and the artificial evidence-difference controls detected the intended changes.

Real metadata-only PE comparison of all five production DLLs:

| Comparison against original build | DLL bytes differ | MVID differs | COFF stamp differs | PE debug directory differs | Raw method IL token records differ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Second worktree, **same source SHA** | 5/5 | 5/5 | 5/5 | 5/5 | **0/5** |
| Rebuilt at **exact same original checkout path** | 5/5 | 5/5 | 5/5 | 5/5 | **0/5** |

The C# reader captured each actual PE and the portable Python comparator reported five changed whole-DLL hashes in both comparisons but **zero changed method-body IL token records**. The exact per-assembly SHA-256, version IDs, timestamp values, debug CodeView records, PDB path hashes, raw method IL token hashes, and 80 effective Release MSBuild property observations were retained in the artifact. All 40 project/property values matched across the two distinct source checkout paths. The workflow also inspected the new reader's own compiled DLL as a self-test before inspecting RecordSift.

### Actual evaluated Release settings (no assumption about compiler defaults)

[Follow-up successful run 41902568850](https://github.com/infoconex/dotnet-modernization/actions/runs/41902568850), research commit 7f3d9ad7398ede5e810749389b07012c9900a685, repeated the three full release/consumer gates and emitted each **actual evaluated** MSBuild Release property value to the job log. **All five production projects** independently reported:

| MSBuild property | Observed Release evaluation |
| --- | --- |
| LangVersion | 7.3 |
| Optimize | true |
| DebugType | pdbonly |
| Deterministic | empty |
| DebugSymbols | empty |
| PathMap | empty |
| ContinuousIntegrationBuild | empty |
| PlatformTarget | empty |

Each corresponding property also matched when evaluated from the independent second source checkout. An **empty evaluation** does not distinguish unspecified, inherited empty or explicitly set empty. In particular, it **does not prove** that the actual C# compiler's deterministic behavior was off, nor does it establish every compiler input; investigating the compiler command line and explicit opt-in properties requires a separate experiment.

**Interpretation:** In this specific existing build, the changing whole-DLL bytes correlate with changed MVID/COFF/debug metadata **even with an identical Git source and identical source-directory path**. The compiled raw method IL bytes did not change. This is stronger evidence for build-generated metadata variation than EXP-017 could show, **not proof of which compiler setting or input caused the differences**, nor a guarantee that no other assembly metadata changed. It does not justify asserting an application defect or enabling Deterministic on production RecordSift.

### Preserved interim failures and independent tooling check

- [Windows run 41901490943](https://github.com/infoconex/dotnet-modernization/actions/runs/41901490943) **failed** while compiling the newly introduced PE reader: implementation incorrectly treated an object result as having a statically known assembly property, plus a nullable method-IL warning treated as an error. No three-build evidence was produced.
- [Windows run 41901638985](https://github.com/infoconex/dotnet-modernization/actions/runs/41901638985) **failed** on the remaining nullable IL warning after fixing the first issue. The actual successful run came only after requiring nonnull method IL and correcting the reader.
- [Portable validator run 41901638806](https://github.com/infoconex/dotnet-modernization/actions/runs/41901638806) passed on Ubuntu and Windows. At the successful PE-run research SHA, [tooling run 41901750743](https://github.com/infoconex/dotnet-modernization/actions/runs/41901750743) passed on Ubuntu but initially **failed** on Windows in a pre-existing dotnet-MSBuild smoke test: the returned LangVersion object lacked a value because its underlying query did not return a successful evaluated result. The failed Windows job was [rerun successfully as attempt 2](https://github.com/infoconex/dotnet-modernization/actions/runs/41901750743) (Windows and Ubuntu both passed). This is not the new PE comparator fixture failing. Repeated failures should be recorded/investigated separately; do not misreport the initial Windows job as passing.

**Evidence status:** The **three-build real PE experiment is verified**, with a separate final-branch property logging enhancement awaiting validation. Windows/Ubuntu portable validation passed in rerun 41901750743 attempt 2; later documentation/property logging commits require their own final-head status checks. Draft PR #32 is open, unmerged, and RecordSift remains frozen.

**Recommended next investigation:** Inspect actual evaluated Deterministic/DebugType/PathMap/PDB settings and isolate deliberate compiler determinism or debug-path controls **in disposable workspaces** with the full original API/NUnit/pack/consumer gate. Do not equate matching raw method IL with full binary, binding or behavioral equivalence.

