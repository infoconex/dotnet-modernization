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
