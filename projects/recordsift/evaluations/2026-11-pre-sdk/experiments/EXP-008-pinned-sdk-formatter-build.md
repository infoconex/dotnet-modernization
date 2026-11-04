# EXP-008 — Pinned SDK compatibility for the existing Roslyn formatter and traditional net48 build

**Investigation:** Test the previously unexecuted `global.json` formatter/CI compatibility claim.  
**Assessment date:** November 3, 2026.  
**Application repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift).  
**Frozen application source baseline:** `main` / `research/dotnet-modernization` at `8358780829458854a4b0356df5ac5e685f0a34c8`.  
**Experimental application branch:** `research/globaljson-formatter-20261103`. Its final workflow-only HEAD was `0c8cc3d775ccff0534d697e5e3cfe2a5fe80ef13`.  
**Work state:** Complete. **Evidence outcome:** Verified for the bounded checks listed here; adoption value remains a decision, not a verified technical necessity.

## Objective and hypotheses

RecordSift's existing `.github/workflows/windows-net48.yml` runs `dotnet format style RecordSift.sln --no-restore --verify-no-changes --diagnostics IDE1006 --severity error --verbosity normal` but does **not** install or select a specific SDK before invoking the command. Previous [EXP-005](EXP-005-sdk-selection-and-overrides.md) verified `global.json` selection and negative controls, **not** formatter execution.

We investigated whether an exact SDK pin would (1) reliably select its requested SDK, (2) run RecordSift's actual existing IDE1006 formatting check, (3) rebuild all ten non-SDK-style .NET Framework 4.8 projects, and (4) preserve the five-assembly NUnit and public API/XML baselines. A second comparison tests a different installed SDK, rather than merely pinning the same default.

This is **not** an argument that every traditional Framework build must use `global.json`; only the `dotnet`-hosted toolchain is under test.

## Environment and isolation

- **Host:** GitHub-hosted `windows-2022`; normal runner toolchain includes Visual Studio/MSBuild as well as installed .NET SDKs. **This experiment does not demonstrate independence from Visual Studio Build Tools.** See [EXP-004](EXP-004-sdk-only-build.md) for that separate question.
- **Runner SDK inventory:** included 10.0.303 and 10.0.403 (also 10.0.114 and 10.0.204, recorded in run logs).
- **Explicit provisioning:** `actions/setup-dotnet@a98b56852c35b8e3190ac28c8c2271da59106c68` (v6.0.0) with exact `dotnet-version: 10.0.403`. Version 10.0.303 was already installed.
- **Restore:** existing standalone `nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config`, respecting current `packages.config`/sources. No PackageReference conversion.
- **Temporary config:** `global.json` was created inside the disposable runner workspace, with `rollForward: disable` and `allowPrerelease: false`, then removed in a `finally` block. **No `global.json` was committed to RecordSift.**
- **Repository modification:** only `.github/workflows/research-globaljson-sdk.yml` was committed on the disposable experimental branch, never to `main`, `release/0.2` or the research base. No source, build or version-file edits were committed, no package was published.

## Exact test surfaces

The two fixed-version probes used this in-workspace template (with `version` set to `10.0.403` and `10.0.303` in their respective runs):

```json
{
  "sdk": {
    "version": "10.0.403",
    "rollForward": "disable",
    "allowPrerelease": false
  }
}
```

Commands, executed from the checkout root:

```powershell
nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
dotnet --version
dotnet format style RecordSift.sln --no-restore --verify-no-changes --diagnostics IDE1006 --severity error --verbosity normal
dotnet msbuild RecordSift.sln /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
```

The exact-pin runs then invoked `packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe` against all **five** `tests\*\bin\Release\*.dll` assemblies, parsed the NUnit XML, checked all five production XML documentation outputs with `scripts/verify_xml_documentation.ps1`, and ran the compiled 425-entry public API check using **Windows PowerShell 5.1**:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\verify_public_api.ps1
```

This intentionally avoids the previously demonstrated PowerShell 7 reflection difference.

## Observed results

Two Windows Actions runs:

- [Initial exact-pin execution — #41680085537](https://github.com/infoconex/RecordSift/actions/runs/41680085537), workflow-only branch SHA `8b1a2e745fb01fddf333b854e470f2f86fe71bd6` — **passed**.
- [Completed cross-version comparison — #41681192996](https://github.com/infoconex/RecordSift/actions/runs/41681192996), branch SHA `0c8cc3d775ccff0534d697e5e3cfe2a5fe80ef13` — **passed**.

| Case | SDK reported by `dotnet --version` | IDE1006 `dotnet format style` | `dotnet msbuild` Release | All five NUnit suites | XML docs / API |
|---|---|---|---|---|---|
| No `global.json` | **10.0.403** | Pass | Pass | Not run in unpinned phase | Not run in unpinned phase |
| Exact pin, `rollForward: disable` | **10.0.403** | Pass | Pass | **419 total / 418 pass / 0 fail / 1 skip** | Pass / **425 entries** |
| Exact pin, `rollForward: disable` | **10.0.303** | Pass | Pass | **419 total / 418 pass / 0 fail / 1 skip** | Pass / **425 entries** |

The [cross-version run job log](https://github.com/infoconex/RecordSift/actions/runs/41681192996) explicitly recorded `UNPINNED_SDK=10.0.403`, `PINNED_SDK=10.0.403`, and `OLDER_PINNED_SDK=10.0.303`, alongside the NUnit summaries and `NFR-010-SC01` API acceptance. Its NUnit XML is retained temporarily as [artifact 13253190405](https://github.com/infoconex/RecordSift/actions/runs/41681192996/artifacts/13253190405), subject to a seven-day retention window (through approximately November 10, 2026). The essential conclusions and commands are retained here independently of artifact expiration.

## Interpretation and limitations

**Verified:** Exact `global.json` selection works with RecordSift's current traditional Framework projects. Both tested 10.0 feature bands (10.0.303 and 10.0.403) successfully executed the **actual existing** IDE1006 formatting gate and preserved the bounded Release, five-suite NUnit, XML and public API checks. SDK 10.0.403 was explicitly provisioned with `setup-dotnet` to demonstrate the CI setup path.

**Not verified/claimed:**

- No formatter **negative control** (deliberate IDE1006 violation) was added during EXP-008. Existing CI convention/other verification addresses enforcement separately.
- No new Debug build, other SDK major versions, unsupported/preview SDK, clean-room developer-machine test, whole-package release-candidate packaging, independent installed-package consumer, or full pipeline parity was run under both pins.
- This run used a Windows runner with Visual Studio tooling preinstalled, unlike the separate SDK-only container experiments.
- An exact pin does **not** cause Visual Studio MSBuild invoked directly by `vswhere` to adopt the selected `dotnet` SDK. The current Windows CI build uses a direct Visual Studio `MSBuild.exe`, while its formatter uses `dotnet`.
- The run proves an exact version **can** work; it does not prove `global.json` is required. Both the unpinned baseline and the 10.0.403 pin selected the same SDK on this runner. Multiple versions work for our bounded checks, which weakens the urgency of adopting an exact pin solely to make these checks pass.
- The required SDK must be installed/provisioned on developer machines and CI; `rollForward: disable` intentionally fails when an exact version is unavailable (as separately verified in EXP-005). Different `rollForward` policies have different maintenance/provisioning tradeoffs.

## Research recommendation (not implementation approval)

**Do not adopt `global.json` as an automatic pre-SDK modernization step.** It becomes useful when the team defines a reproducibility requirement for the **`dotnet` CLI / formatter / SDK MSBuild** across CI and developers and commits to provisioning/updating its selected SDK. If such a requirement is established, compare a strict exact pin with a justified `latestPatch` or `latestFeature` policy, explicitly configure CI setup, then verify both local workflows and existing compatibility gates. Do not present `global.json` as changing `TargetFrameworkVersion=v4.8`, pinning a .NET Framework runtime, or controlling separately selected Visual Studio `MSBuild.exe`.

Microsoft reference: [global.json overview](https://learn.microsoft.com/en-us/dotnet/core/tools/global-json); [dotnet format command](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format).

**Governance:** This was disposable, authorized research. All implementation and documentation merges require explicit stakeholder review and separate approval. The experiment branch is not a release branch and may be discarded when its evidence has been accepted.
