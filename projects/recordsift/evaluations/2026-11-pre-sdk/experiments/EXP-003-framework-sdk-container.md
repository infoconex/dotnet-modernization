# EXP-003 — Windows .NET Framework SDK container feasibility

**Objective:** Verify Windows containers can reproduce existing restore, compilation and NUnit behavior.  
**Baseline:** infoconex/RecordSift main at `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Work state:** Complete  
**Evidence outcome:** Verified for the tested historical image

## Environment

A GitHub-hosted Windows Server 2022 runner with Windows Docker Engine used **process isolation** and mounted the repository checkout into:

    mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2022

Immutable digest used:

    sha256:460dedaed73224f73ff10dc3ad754d0ed250aa57bcdf6c5052a811b4b7e29345

**Important:** This was a previously cached, historical tag, not a currently recommended Microsoft-supported tag. The supported 4.8.1 Server Core 2022 manifest was inspected but the image was not pulled/tested.

Inventory inside the container:
- Windows Server Core 2022.
- Visual Studio **Build Tools** 2022 present; full Visual Studio IDE absent.
- MSBuild `17.14.23.42201`.
- NuGet CLI `6.14.0.116`.
- .NET SDK `9.0.305`.
- .NET Framework 4.8 reference assemblies present.

## Procedure and observations

- Start Windows container with process isolation on a compatible Windows Server 2022 host.
- Mount checkout.
- Restore with NuGet CLI using existing NuGet.Config/packages.config.
- Compile all ten projects in Release.
- Run all five NUnit assemblies inside the container.

**Result:** Full solution compiled; NUnit **419 discovered, 418 passed, 0 failed, 1 skipped**.

## Evidence

[Full Windows container test run](https://github.com/infoconex/RecordSift/actions/runs/41484891489). Earlier [feasibility and inventory run](https://github.com/infoconex/RecordSift/actions/runs/41484601947).

## Conclusion and limitations

Windows container feasibility and conventional .NET Framework SDK-image reproduction are verified. **This experiment did not remove Visual Studio Build Tools.** EXP-004 separately tested that question.

Do not publish steps using the historical tag as if it is still supported; pull and validate the currently supported image/digest first.
