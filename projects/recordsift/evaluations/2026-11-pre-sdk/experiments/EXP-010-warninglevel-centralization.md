# EXP-010 — Centralize `WarningLevel` in traditional RecordSift projects

**Date:** November 3, 2026  
**Tracking:** [Issue #9](https://github.com/infoconex/dotnet-modernization/issues/9)  
**Application baseline:** `infoconex/RecordSift` `main` / `research/dotnet-modernization` at `8358780829458854a4b0356df5ac5e685f0a34c8` (both frozen and unchanged)  
**Disposable experiment branch:** `research/warninglevel-20261103`; only its `.github/workflows/research-exp010-warninglevel.yml` is committed. All other changes occur in an ephemeral GitHub Actions workspace.  
**Prior evidence:** [EXP-002 shared `LangVersion`](EXP-002-shared-properties.md), [EXP-005 override precedence](EXP-005-sdk-selection-and-overrides.md), [EXP-006 import behavior](EXP-006-msbuild-imports.md), and existing unmerged [property audit PR #5](https://github.com/infoconex/dotnet-modernization/pull/5).  
**Status:** targeted experiment in progress; no permanent application changes approved.

## Research question

The existing audit confirms 20 identical `<WarningLevel>4</WarningLevel>` elements: two in each of ten traditional projects (Debug and Release). Can these be replaced by a shared property without changing evaluated properties, enabled compiler warnings, override behavior, builds, API/assembly identities, NUnit, XML documentation enforcement, or packaging/independent consumers?

This differs from `LangVersion` centralization in EXP-002. The WarningLevel declarations are **configuration-conditional**, so an unconditional shared property can broaden the effective setting to configurations where the baseline did not declare it. C# warning level 4 is also the compiler's established default, lowering the practical benefit of changing the project files.

## Minimal experiment and controls

1. Verify the immutable baseline source SHA and workflow-only commit difference; inspect effective `WarningLevel` values using Visual Studio MSBuild `-getProperty:WarningLevel` across all ten projects in Debug and Release. Probe an otherwise unspecified `Custom` configuration in representative production and test projects.
2. In the disposable checkout, remove exactly twenty XML elements, create a temporary `Directory.Build.props`, and compare all twenty Debug/Release evaluated values. Test an unrestricted shared 4 and a configuration-scoped shared 4 against the Custom baseline.
3. Change the scoped shared value temporarily to 3 and evaluate representative Debug, Release and Custom properties; restore 4. Add an isolated unconditional project-level 3 in `RecordSift.Domain.csproj` and verify that it overrides the shared default; restore its temporary change.
4. Restore/compile in both Debug and Release; run all five NUnit assemblies, 425-entry API and production XML checks, local unpublished NuGet package generation/validation and independent consumer, and the existing negative CS1591 documentation enforcement gate.
5. Record any failure's true layer. Preserve failed harness runs without treating them as application regressions.

The experiment deliberately does **not** change `TargetFrameworkVersion`, `LangVersion`, output paths, identities, embedded resources, `WarningsAsErrors=1591`, package references, or other project configuration.

## Initial execution observations

- [Run 41713158056](https://github.com/infoconex/RecordSift/actions/runs/41713158056) was inconclusive before probes because shallow checkout lacked the frozen baseline commit needed for the branch diff control; a full checkout fixed this **harness issue**.
- [Run 41713305055](https://github.com/infoconex/RecordSift/actions/runs/41713305055) verified baseline Debug/Release property values but stopped when the probe incorrectly treated the **empty** value of `WarningLevel` under an undefined `Custom` configuration as a parse error. This was a meaningful baseline observation; the exception itself was a **harness issue**.
- [Run 41713632786](https://github.com/infoconex/RecordSift/actions/runs/41713632786) verified 20/20 baseline Debug/Release values = 4 and representative Custom values empty, then stopped because the temporary regex assumed standalone XML lines. The Reporting project contains inline `<WarningLevel>4</WarningLevel>` elements. A token-based probe matching the actual XML elements corrected this **harness issue**.
- [Run 41713886548](https://github.com/infoconex/RecordSift/actions/runs/41713886548) is the corrected follow-up; assess actual completed logs before claiming parity or compatibility.

**Do not infer full compatibility from partial run observations.** Final results, relevant artifact ID, effective-property table, verification omissions and recommendation will be added after the corrected run finishes.

## External engineering guidance

Microsoft documents a default C# `WarningLevel` of 4 and identifies settings in `Directory.Build.props` as directory-wide defaults subject to import ordering and later overrides:
- [C# compiler warnings](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/errors-warnings)
- [Customize by directory](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory)

Those are guidance, not substitutes for RecordSift-specific execution evidence.

## Authorization and decision boundary

No permanent RecordSift change is requested or approved. Conditional property design, if safe, is a candidate recommendation only. The existing property audit [draft PR #5](https://github.com/infoconex/dotnet-modernization/pull/5) is separate and remains unmerged. Avoid modifying its historical findings or assuming they are present in documentation main. No application merges, releases or NuGet publication.
