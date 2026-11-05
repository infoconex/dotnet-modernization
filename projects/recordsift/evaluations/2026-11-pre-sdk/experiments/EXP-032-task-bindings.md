# EXP-032 — Observe Source Link task assembly binding inside the real MSBuild process

**Status:** Research-only; Windows CI required before any verification claim. Standalone draft from EXP-030, avoiding blocked EXP-031 security dependency. RecordSift frozen SHA `8358780829458854a4b0356df5ac5e685f0a34c8`.

## Question

Does the manually imported Source Link 10.0.403 toolchain execute and load its task assemblies within the build process, and from which paths, without silently replacing the nine application `packages.config` references or copying tool DLLs into the CSV output?

## Control

The optional `-CaptureLoadedModules` switch in the existing EXP-024 reusable pilot imports a research-only inline RoslynCodeTaskFactory `.targets` file into the **disposable CSV project only**. The diagnostic task executes `AfterTargets=CoreCompile` during the same Release MSBuild invocation as the provider Source Link tasks. It obtains process and AppDomain identifiers and enumerates AppDomain loaded assemblies: Microsoft.Build.Tasks.Git, Microsoft.SourceLink.Common, Microsoft.SourceLink.GitHub, System.Buffers, System.Memory, System.IO.Hashing, System.Numerics.Vectors and Unsafe, including loaded version and raw assembly location. Raw paths are held privately in ephemeral runner temp and **never uploaded**. Evidence JSON contains only assembly name, version and category: `isolated_build_tool_package_tree`, `existing_application_package_tree`, `preinstalled_host_toolchain`, `inside_disposable_application`, or `other_external_location`.

The same pilot still runs the immutable ten-project baseline and 425 public API, 419 NUnit, five XML, local NuGet package and clean net48 consumer gates on the **provider-built** CSV candidate. It asserts zero new task DLLs in Release output and restores original tracked files before acceptance checks.

## Precise boundaries

- In-process `AppDomain.CurrentDomain.GetAssemblies()` shows assemblies in the **diagnostic task's AppDomain** and host process, not every separately spawned MSBuild node or AppDomain. It does not automatically establish every task's executable module binding.
- A known loaded tool DLL path is stronger than inferred `UsingTask` import text, but the experiment must still independently examine NuGet package manager installation semantics if that deployment approach is being considered.
- Do not infer successful Visual Studio debugger stepping, safe production integration, CVE immunity or full PDB source checksum proof from this phase.
- No source commits, production dependency upgrades, merges, artifacts containing module paths, DLL/PDB uploads, or NuGet publish. Keep this PR draft pending review.

Related: [EXP-024](EXP-024-sourcelink-windows-import.md), [EXP-023B](EXP-023B-dependency-preflight.md), [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).
