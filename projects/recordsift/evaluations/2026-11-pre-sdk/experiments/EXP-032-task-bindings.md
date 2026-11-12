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

## Verified Windows CI module binding evidence

**Verified:** [Windows run 41982078891](https://github.com/infoconex/dotnet-modernization/actions/runs/41982078891) at corrected research SHA `17a0e47bb2c86db78130fe994ea26bdfe46726b7` passed the in-process MSBuild probe and all historical release gates. Retained [artifact 13394262726](https://github.com/infoconex/dotnet-modernization/actions/runs/41982078891/artifacts/13394262726), ZIP SHA256 `b850807e0fe575db56b04a2602f0dc05212e55028721a42ad42c0b30e10dbf74`, independently downloaded and examined. `experiment-report.json` confirms compiler `/sourcelink`, `InitializeSourceControlInformation`, all six provider props/targets imported, and the candidate 425 API/419 NUnit (418 passed, one skipped)/five XML/unpublished package/clean net48 consumer gates with all five logical categories matched; **no additional CSV output DLLs**. Source remains frozen and tracked files restored.

**Actual in-process loaded assemblies observed after CoreCompile** (assembly versions, **not NuGet package versions**):

| Loaded assembly identity | Assembly version | Observed location classification |
| --- | --- | --- |
| Microsoft.Build.Tasks.Git | 10.0.15.2412 | `isolated_build_tool_package_tree` |
| Microsoft.SourceLink.Common | 10.0.15.2412 | `isolated_build_tool_package_tree` |
| Microsoft.SourceLink.GitHub | 10.0.15.2412 | `isolated_build_tool_package_tree` |
| System.Memory | 4.0.5.0 | `preinstalled_host_toolchain` |
| System.Buffers | 4.0.5.0 | `preinstalled_host_toolchain` |
| System.Numerics.Vectors | 4.1.6.0 | `preinstalled_host_toolchain` |
| System.Runtime.CompilerServices.Unsafe | 6.0.3.0 | `preinstalled_host_toolchain` |

System.IO.Hashing did not appear among the selected loaded assemblies in this captured AppDomain. **Absence from this AppDomain is not proof the DLL was not loaded in another MSBuild node or AppDomain**. Private full host paths were not uploaded. The synthetic diagnostic task executes within the same MSBuild host process and captures the selected assemblies in its own AppDomain. This is direct runtime observation rather than an import or packages.config inference.

**Prior failed harness controls:** initial [41981294556](https://github.com/infoconex/dotnet-modernization/actions/runs/41981294556) incorrectly inserted an XML import at every `</Project>`, corrupting original `ProjectReference` GUID metadata (MSB3107); corrected to target *only root Project's final closing tag*. Follow-up [41981707967](https://github.com/infoconex/dotnet-modernization/actions/runs/41981707967) failed RoslynCodeTaskFactory's unnecessary `System.Core` reference; removed and rerun. The **unchanged baseline EXP-024 workflows passed on both failed-probe revisions**, confirming the underlying application candidate was not at fault. Both failures remain retained harness observations, not application compatibility defects.

**Narrow verdict:** `VERIFIED_SELECTED_SOURCE_LINK_TASK_DLLS_LOADED_FROM_ISOLATED_BUILD_TOOL_PACKAGE_TREE`, with the host-provided System.Memory/Buffers/Vectors/Unsafe assemblies observed separately and original application compatibility passed. **Still not verified:** every MSBuild task node/AppDomain, real Visual Studio Package Manager project-install semantics, native PDB document checksums, interactive debugger stepping. Keep PR draft and no production adoption.
