# EXP-010 — Centralizing `WarningLevel` in ten traditional projects

**Date:** November 3, 2026  
**Tracking:** [dotnet-modernization issue #9](https://github.com/infoconex/dotnet-modernization/issues/9)  
**Prior research:** [EXP-002](EXP-002-shared-properties.md) (LangVersion), [EXP-005](EXP-005-sdk-selection-and-overrides.md) (conditional overrides), [EXP-006](EXP-006-msbuild-imports.md) (imports), [unmerged property audit PR #5](https://github.com/infoconex/dotnet-modernization/pull/5).  
**Application:** `infoconex/RecordSift`, frozen `main` and `research/dotnet-modernization` at `8358780829458854a4b0356df5ac5e685f0a34c8`.  
**Disposable experiment branch:** `research/warninglevel-20261103`; final SHA `fd44c1b7bd89c7718117222f5276fbeef0e649af`.  
**Successful Actions run:** [41713886548](https://github.com/infoconex/RecordSift/actions/runs/41713886548); [artifact 13268657551](https://github.com/infoconex/RecordSift/actions/runs/41713886548/artifacts/13268657551).  
**Work state:** Complete. **Evidence outcome:** Verified for Debug and Release builds, evaluated properties, explicit override behavior and tested compatibility gates. A representative nonstandard `Custom` configuration was *evaluated*, not compiled.  
**Authorization boundary:** All 10 `.csproj` edits and `Directory.Build.props` creation existed **only in the GitHub Actions temporary checkout**. The sole committed change in the disposable research branch is its workflow. No RecordSift `main`, `release/0.2`, application release, or package feed changed.

## Question and expectation

A previous full source audit found exactly **20 declarations** of `<WarningLevel>4</WarningLevel>`: two (Debug/Release) in each of five production and five test projects. Unlike `LangVersion=7.3`, these declarations are inside `Configuration|Platform`-conditional project property groups. A root `Directory.Build.props` in RecordSift's **existing traditional imports** is imported late; a conditional value can still be overridden by a project property already set.

Determine whether a shared property preserves original **effective property semantics**, compiler warnings, output compatibility and clean consumers. Do **not** infer equivalence merely from two successful builds. In addition, C# compiler warning level 4 is already the default, reducing the practical urgency of this change.

## Environment and reproducibility

| Item | Observed |
|---|---|
| GitHub host | `windows-2022`, Windows NT `10.0.20348.0` |
| MSBuild | Visual Studio 2022 Enterprise `C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\MSBuild.exe`; `17.14.60.43110` |
| .NET SDK | `10.0.403` |
| PowerShell | PowerShell `7.6.9` for experiment/build/package orchestration; `powershell.exe` (Windows PowerShell) for the 425-entry API reflection script |
| NuGet CLI | `7.9.0.83` |
| NUnit | Existing restored `NUnit.ConsoleRunner` `3.17.0` |
| Target | `.NET Framework 4.8`, C# `7.3`; standard Windows runner with VS Build Tools available, not the SDK-only container |

The complete immutable executable procedure is [the experimental workflow](https://github.com/infoconex/RecordSift/blob/fd44c1b7bd89c7718117222f5276fbeef0e649af/.github/workflows/research-exp010-warninglevel.yml). It checks that the experiment branch differs from the baseline **only** by the workflow; inspects the original evaluated properties; modifies files in the temporary checkout; then restores/packages/runs consumers and the CS1591 negative test. The workflow uploads `TestResults/warninglevel-props.json` and `TestResults/warninglevel-nunit.xml` even if a subsequent gate fails.

## Exact evaluated-property controls

`MSBuild.exe -getProperty:WarningLevel` with `/p:Configuration=Debug` or `Release` and `/p:Platform=AnyCPU` was run against each of all ten `.csproj` files.

| Control | Observed result | Interpretation |
|---|---|---|
| Original projects, Debug and Release | **20/20 evaluated `WarningLevel=4`** | Verified immutable baseline |
| Original representative Application production and test projects under `Custom|AnyCPU` | **Empty** `WarningLevel` value | Baseline does not explicitly set it in this configuration |
| Remove exactly 20 project declarations; create unrestricted shared default `4` | **20/20 Debug/Release still `4`**, but representative `Custom` becomes **explicit `4`** | Functional gate parity is possible; **property semantics broaden** for an undefined configuration |
| Scope shared default to Debug and Release only | **20/20 Debug/Release remain `4`; representative `Custom` becomes empty again** | Preserves tested effective property semantics |
| In scoped shared default, temporarily substitute `WarningLevel=3` | Application and test examples: **Debug=3, Release=3, Custom=empty** | Verified that shared value truly propagates and is not merely masked by the compiler default |
| With scoped default `4`, temporarily set unconditional project-local `WarningLevel=3` in Domain | **Debug=3, Release=3**; after restoring local edit, value returns to 4 | Project override precedence preserved |

**Verified candidate pattern only (not committed to application):**

```xml
<Project>
  <PropertyGroup>
    <WarningLevel Condition="'$(WarningLevel)' == '' and ('$(Configuration)|$(Platform)' == 'Debug|AnyCPU' or '$(Configuration)|$(Platform)' == 'Release|AnyCPU')">4</WarningLevel>
  </PropertyGroup>
</Project>
```

The condition scopes the setting to the two configurations that **actually contained it** in baseline XML and preserves project-local overrides. An unconditional shared value is simpler but changes evaluated `Custom` properties. The representative `Custom` check did not attempt a complete build of that unsupported configuration; it documents a property-level behavioral distinction, not a demonstrated functional regression.

One source-format observation matters for reproducing the experiment: the Reporting project has `<WarningLevel>4</WarningLevel>` **inline with other XML elements**. A line-based removal regex did not match it. The successful temporary transformation matches the XML element itself, counts exactly two per project, and never commits those edits.

## Full compatibility result: successful run 41713886548

| Check | Evidence |
|---|---|
| Restore of pinned `packages.config` dependencies | **PASS** with NuGet CLI 7.9.0.83 |
| All ten project builds, Debug | **PASS** |
| All ten project builds, Release | **PASS** |
| Positive XML docs | **PASS:** five production XML files; documented member counts **179 / 101 / 8 / 2 / 9** |
| Compiled public API and packaging metadata | **PASS:** all **425** baseline entries |
| All five NUnit test DLLs | **PASS:** **419 discovered / 418 passed / 0 failed / 1 skipped** |
| Unpublished local `0.1.0-rc.1` package | **PASS:** metadata, five assemblies, five XML files, notices, README, license and dependencies validated |
| Independent installed-package consumer | **PASS:** compiled/executed; customer CSV/XLSX and all four Getting Started sample files validated |
| Intentional missing-public-documentation control `CS1591` | **PASS:** existing negative check rejected undocumented `ExpectedColumn.Name` |
| Actual permanent application files | **UNMODIFIED** | Experimental checkout and local candidate were discarded when job finished |

**Unpublished experimental package SHA-256:** `7765D2479FFBA0FA4700889E9467B56AF24E516951B334B813C2D82FF6CF9ADD`. The local package's source-commit field points to the experimental workflow commit (while the unchanged packager stamps `branch=main`); **do not publish** that exploratory archive. This is compatibility-test evidence, not an approved publication candidate.

## Failed controls and why they do not discredit the application

| Run | First failure | Classification |
|---|---|---|
| [41713158056](https://github.com/infoconex/RecordSift/actions/runs/41713158056), `03a445c6ef96e25d145bf251426c974f8598d503` | Shallow checkout could not resolve baseline `8358780` during `git diff` verification | Experimental harness; corrected using `fetch-depth: 0` |
| [41713305055](https://github.com/infoconex/RecordSift/actions/runs/41713305055), `4586c8d2a177067e1828beef7f73680e1fc93bdf` | Property probe assumed `Custom` always reports a number, but baseline reports an empty value | Harness parser error; substantive baseline observation retained |
| [41713632786](https://github.com/infoconex/RecordSift/actions/runs/41713632786), `9643e5936a1ef6f3681b738fa5f2bb7690f781b0` | Probe assumed project warning XML elements start on their own line; Reporting contains inline elements | Harness matcher defect, corrected with exact XML element replacement |
| **[41713886548](https://github.com/infoconex/RecordSift/actions/runs/41713886548)**, **`fd44c1b7bd89c7718117222f5276fbeef0e649af`** | No failure; all intended controls and compatibility checks completed | **Verified** |

Run links and uploaded artifact IDs are evidence locators, not permanent archival guarantees; the essential results, exact workflow reference, SHA, environment and caveats are recorded here.

## Assessment, risks and recommendation

**Technical feasibility: verified.** The configuration-scoped and override-aware single shared property preserves the evaluated Debug/Release baseline and passes tests, build, compiled API, XML, NuGet/independent consumer and negative documentation enforcement. `Directory.Build.props` works under these traditional project imports; do not add an early `Microsoft.Common.props` import, which previously caused MSB3107 (EXP-006).

**Practical value: modest.** Centralizing 20 identical declarations provides one deliberate place to change compiler warning policy, retaining local overrides. However, C# compiler warning level **4 is already the default**; the current values are identical and rarely need coordinated change. The condition needed to preserve exactly the old Custom semantics makes this candidate less minimal than the already verified `LangVersion` centralization.

**Preferred decision:** Mark `WarningLevel` centralization **technically verified but optional / lower priority**. If an implementation is later specifically approved, use configuration-scoped defaults and execute complete compatibility gates. Prefer `LangVersion` first. Do not combine `WarningLevel` with `WarningsAsErrors=1591` or broaden the existing production-only documentation policy. Do not introduce a new targets file or rework MSBuild import ordering for this cleanup.

**Unverified outside tested scope:** Other custom configuration/platform combinations, other MSBuild/SDK hosts, and potential future changes to the property/import chain. This experiment does not approve implementation, SDK-style conversion, or modern .NET migration.

Microsoft references: [C# compiler warning levels](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/errors-warnings) (level 4 is default), [Directory.Build.props customization and import order](https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory).

## Review interaction with other draft PRs

[Property audit PR #5](https://github.com/infoconex/dotnet-modernization/pull/5) is intentionally independent and unmerged; it provides **source-only** findings that EXP-010 now supplements with **executed** evidence. Other drafts (including EXP-009 draft PR #8) may update the same index, status and findings. Reconcile those only after stakeholder review. Do not duplicate existing `F-###` IDs between draft branches; the experiment record itself is the stable source of this result.
