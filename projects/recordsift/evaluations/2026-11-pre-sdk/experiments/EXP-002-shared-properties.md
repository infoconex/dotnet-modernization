# EXP-002 — Centralize common language version safely

**Objective:** Determine whether traditional projects can share LangVersion without import rewrites or compatibility differences.  
**Application baseline:** infoconex/RecordSift, main `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Work state:** Complete  
**Evidence outcome:** Verified

## Environment and change

Disposable Windows GitHub Actions workspace with existing VS 2022 MSBuild and .NET Framework 4.8 toolchain. The experimental branch only contained a workflow; these project edits were not committed:

1. Create root `Directory.Build.props` with `LangVersion=7.3`.
2. Remove identical project-local `<LangVersion>7.3</LangVersion>` from all ten projects.
3. Leave all existing imports, target framework, packages, assembly identities and resources unchanged.
4. Query evaluated properties with MSBuild `-getProperty`; rebuild and compare compatibility gates.

Representative evaluation command:

    MSBuild.exe src\RecordSift.Domain\RecordSift.Domain.csproj -getProperty:LangVersion /p:Configuration=Release

## Results

- All ten evaluated to the intended C# language version 7.3.
- Complete Release build succeeded.
- NUnit before and after: **419 discovered, 418 passed, 0 failed, 1 skipped**.
- **425** API/packaging-metadata entries verified.
- Production XML documentation counts and local NuGet package validation checked.
- No original source code or dependency changes required.
- Package binary hashes differed; byte-identical binaries were not claimed or required.

## Follow-up precedence control

A separate run deliberately changed a Domain project to LangVersion 7.2. An **unconditional** shared property evaluated to 7.3; changing the shared property to a **conditional default** honored the project override and evaluated to 7.2.

This demonstrates why property **evaluation order** and **conditional defaults** matter in the current late-import arrangement.

## Evidence

- [Full shared-property parity run](https://github.com/infoconex/RecordSift/actions/runs/41484769924) — evidence artifact ID **13160583419**.
- [Project override follow-up](https://github.com/infoconex/RecordSift/actions/runs/41486700576).

## Limitations and conclusion

The experiment validates common **LangVersion**, not arbitrary property movement. Do **not** centralize TargetFrameworkVersion before addressing the API checker's raw-XML assumption.

Recommended pre-SDK improvement after local test-command parity is repaired and baseline checks are retained.
