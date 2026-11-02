# EXP-005 — SDK selection and conditional shared-property defaults

**Objective:** Test global.json SDK resolution independently of target framework, and verify a project can override a shared property in RecordSift's traditional import chain.  
**Baseline:** infoconex/RecordSift main `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Experimental branch:** `discovery/props-sdk-selection-20261102`  
**Work state:** Complete  
**Evidence outcome:** Verified for SDK selection and property precedence; formatter compatibility not executed

## Environment

GitHub-hosted Windows Server 2022 with installed .NET SDKs, including `10.0.303` and `10.0.403`. Temporary `global.json`, `Directory.Build.props`, and a project-level LangVersion change were created **in the disposable runner workspace only**, not committed to the application.

## SDK selection controls

| Case | Actual selection |
|---|---|
| No global.json | 10.0.403 |
| Exact version 10.0.403, `rollForward: disable` | 10.0.403 |
| Version 10.0.303, `rollForward: latestFeature` | 10.0.403 |
| Missing exact version 10.0.999, roll-forward disabled | SDK selection failed as expected |

Example:

    {"sdk":{"version":"10.0.303","rollForward":"latestFeature"}}

`global.json` influences the **.NET SDK selected by dotnet tooling**; it does not retarget the RecordSift projects from .NET Framework 4.8.

## Shared-property precedence controls

Temporarily set Domain project's language version to **7.2**, while root Directory.Build.props provided **7.3**.

- Unconditional shared LangVersion=7.3: evaluated **7.3**, overriding the project value.
- Conditional default only when LangVersion is empty: evaluated **7.2**, preserving the project value.

This reflects the current **late import timing** of Directory.Build.props in traditional RecordSift projects. It is not a universal guarantee about all MSBuild project types.

## Evidence and caveat

- [Successful controls](https://github.com/infoconex/RecordSift/actions/runs/41486700576).
- A first version of the negative control deliberately hit an unhandled missing SDK failure and marked its [workflow](https://github.com/infoconex/RecordSift/actions/runs/41486570113) failed; the later workflow explicitly treated that diagnostic as **expected**, and passed.

**Unexecuted:** a full `dotnet format style` check under a pinned global.json, and a pinned-SDK full build. Do not recommend mandatory pinning from selection behavior alone.
