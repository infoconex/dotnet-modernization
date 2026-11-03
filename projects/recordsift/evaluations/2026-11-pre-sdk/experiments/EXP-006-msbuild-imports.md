# EXP-006 — Traditional MSBuild imports, props and targets

**Objective:** Verify actual import order and whether adding early imports is required for repository-wide MSBuild configuration.  
**Application baseline:** infoconex/RecordSift main `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Work state:** Complete  
**Evidence outcome:** Verified imports and a failed early-import experiment

## Controls

The ten projects import `$(MSBuildToolsPath)\Microsoft.CSharp.targets` directly. Their import chain reaches `Microsoft.Common.props` **transitively through targets**, meaning root Directory.Build.props is imported late under the current project layout.

Representative evaluation commands:

    MSBuild.exe src\RecordSift.Domain\RecordSift.Domain.csproj /pp:preprocessed.xml /p:Configuration=Release

    MSBuild.exe src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:LangVersion /p:Configuration=Release

Root Directory.Build.props was read without a new explicit Common.props import. A temporary root Directory.Build.targets with a custom marker target was also imported and executed.

## Failed experiment

Adding a new early `Microsoft.Common.props` import to all ten projects, combined with centralization, produced **MSB3107** project-reference metadata errors. The complete solution did **not** successfully rebuild in that configuration.

The subsequent experiment **without import edits** succeeded completely; see [EXP-002](EXP-002-shared-properties.md).

## Tool host issue

The first experimental API verification was executed in PowerShell 7 and produced spurious .NET Framework reflection differences, including unexpected interfaces. Rerunning under **Windows PowerShell 5.1** restored valid comparison results.

## Evidence

- [Corrected import discovery and unsuccessful early import](https://github.com/infoconex/RecordSift/actions/runs/41484290488).
- [Initial incorrect PowerShell-host experiment](https://github.com/infoconex/RecordSift/actions/runs/41483895096).
- [Working centralization without early import](https://github.com/infoconex/RecordSift/actions/runs/41484769924).

## Conclusion

Do not introduce early imports solely to enable shared props in RecordSift. Directory.Build.targets technically works, but no compelling reusable custom target was found. Avoid creating targets or solution-response files without a demonstrated use case.
