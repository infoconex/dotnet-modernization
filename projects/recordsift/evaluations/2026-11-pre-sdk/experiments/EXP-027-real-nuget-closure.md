# EXP-027 — Real NuGet dependency acquisition, separate from project installation

**Status:** Draft and awaiting Windows CI. Stacked research branch, no application or research main merge.

**Objective:** Confirm actual official NuGet package acquisition resolves Source Link 10.0.403 dependency closure and contrast each selected version with the frozen CSV `packages.config` nine pins.

## Boundaries and procedure

- Checkout `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8` clean.
- Use Windows runner's NuGet CLI `nuget install Microsoft.SourceLink.GitHub -Version 10.0.403 -DependencyVersion Lowest` with **a runner-temp output directory**, not the RecordSift checkout. This runs the NuGet resolver but does **not** mean Visual Studio Package Manager changed any .csproj imports or packages.config entries.
- Read resulting nuspec identities, package versions and archive SHA-256. Compare overlaps with the original CSV packages.config versions. Expect the `System.Buffers` and `System.Memory` toolchain dependencies to exceed frozen application pins.
- Preserve source Git HEAD and tracked working tree; store only package-version/hash JSON, not NuGet archives or executable binaries.
- If versions conflict, **do not upgrade the application** or declare this an installable recommendation. Use EXP-024's manual import simulation as separate proof only.

This does not prove actual Visual Studio NuGet Package Manager installation behavior, MSBuild task dependency binding, final NuGet distributable dependencies or application runtime isolation. Those require further evidence.

Related: [EXP-023B](EXP-023B-dependency-preflight.md), [EXP-024](EXP-024-sourcelink-windows-import.md), [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).

## Verified real NuGet CLI resolution on Windows

**Verified:** [run 41968065998](https://github.com/infoconex/dotnet-modernization/actions/runs/41968065998) passed at SHA `383fcedc9a079bd803f8a40f8b5ff707cd60404b` with real `nuget install ... -Framework net48 -DependencyVersion Lowest` into temporary runner directory. Prior [run 41967645444](https://github.com/infoconex/dotnet-modernization/actions/runs/41967645444) failed a mistaken assumption that an extracted `.nuspec` always exists at the package root. Reader now inspects the **embedded** `.nuspec` inside each downloaded `.nupkg`; failed-run cause is tooling, not NuGet resolution.

Retained JSON from [successful run 41967938409](https://github.com/infoconex/dotnet-modernization/actions/runs/41967938409), [artifact 13387719624](https://github.com/infoconex/dotnet-modernization/actions/runs/41967938409/artifacts/13387719624), digest SHA-256 `a3154d72e9233ef832a430480bb1dd9a7851e697b048a4f1675b691e4ce49a48`, independently downloaded and inspected. Exactly **eight resolved package identities**:

- Microsoft.SourceLink.GitHub 10.0.403
- Microsoft.SourceLink.Common 10.0.403
- Microsoft.Build.Tasks.Git 10.0.403
- System.IO.Hashing 10.0.14
- System.Buffers **4.6.1** (RecordSift **4.5.1**)
- System.Memory **4.6.3** (RecordSift **4.5.5**)
- System.Numerics.Vectors **4.6.1** (RecordSift **4.5.0**)
- System.Runtime.CompilerServices.Unsafe **6.1.2** (RecordSift **6.0.0**)

Follow-up workflow assertion at SHA `383fcedc9a079bd803f8a40f8b5ff707cd60404b` now explicitly expects **8 packages and four version overlaps**; verified green. The first EXP-023B selected package subset exposed only the first two conflicts. This is not equivalent to actual Visual Studio Package Manager project-install semantics. No RecordSift tracked file modified; no package publish or binary uploaded. Separate manual build-tool-only integration EXP-024 proved compatibility without those version upgrades, but does not erase the conventional closure conflict.
