# RecordSift — Discovery report

This report contains the **answers collected so far**, not instructions or blank form fields. The matching numbers in the [step-by-step guide](../../../../methodology/technical-discovery-runbook.md) explain how to collect more information.

**Record status:** Initial GitHub source inspection only. No Windows commands have been run or reported for this discovery. Fields 1 and 2 reflect the **example values supplied for this report format**; they do not establish that any local discovery was executed.

## Discovery information

**1. Recorder:** Jim Scott

**2. Recorded Date:** 2026-11-12

**12. Source branch:** `main` — observed through GitHub on November 12, 2026.

**13. Selected source commit:** [`1809d06c0fade59e4769d16e0f8eaf10fa426004`](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004). The local checkout has not been verified.

**16. Discovery status:** Partial — source files inspected via GitHub; local prerequisite checks, clone, restore, build, and tests have not been performed.

## Application information

**17. Application:** RecordSift

**18. Description:** CSV/XLSX import, validation and reporting library, described as Windows/.NET Framework 4.8 in its [README at the selected commit](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md). This describes the application's documented requirements; the project files and build have not yet been evaluated.

**19. Repository visibility:** Public GitHub repository.

**20. HTTPS clone URL:** `https://github.com/infoconex/RecordSift.git`

**22. Default branch:** `main` when inspected on November 12, 2026.

**24. Supported operating system:** Windows, as documented in the source README.

## Source inventory

**31. Solution path:** `RecordSift.sln` — found in the tracked tree. Solution membership has not yet been checked.

**38. Project paths:** Ten tracked C# project files were identified:

- `src/RecordSift.Domain/RecordSift.Domain.csproj`
- `src/RecordSift.Application/RecordSift.Application.csproj`
- `src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj`
- `src/RecordSift.Infrastructure.Xlsx/RecordSift.Infrastructure.Xlsx.csproj`
- `src/RecordSift.Infrastructure.Reporting/RecordSift.Infrastructure.Reporting.csproj`
- `tests/RecordSift.Domain.Tests/RecordSift.Domain.Tests.csproj`
- `tests/RecordSift.Application.Tests/RecordSift.Application.Tests.csproj`
- `tests/RecordSift.Infrastructure.Csv.Tests/RecordSift.Infrastructure.Csv.Tests.csproj`
- `tests/RecordSift.Infrastructure.Xlsx.Tests/RecordSift.Infrastructure.Xlsx.Tests.csproj`
- `tests/RecordSift.Infrastructure.Reporting.Tests/RecordSift.Infrastructure.Reporting.Tests.csproj`

**39. Project roles:** Five project paths under `src/` and five under `tests/`. These are directory-based roles, not proof of project configuration or test execution.

**64. Repository directories:** `src/` holds the production project paths; `tests/` holds the test project paths.

**66. Configuration files found:** Root `.editorconfig`, root `NuGet.Config`, seven tracked `packages.config` files (two under `src/` and five under `tests/`), and eight GitHub Actions workflow definitions under `.github/workflows/`.

**67. Configuration files not found at the tracked repository root:** `global.json`, `Directory.Build.props`, `Directory.Build.targets`, and `Directory.Packages.props`. This is **not** proof that equivalents, inherited configuration, or machine defaults do not apply.

These facts come from [EV-001–EV-003](evidence/manifest.md) and are limited to source inspection at the selected commit.

## What remains to be collected

**3–11. Discovery folder and prerequisite versions:** Not yet collected from the Windows machine.

**14. Local checkout status:** Not yet checked; fresh clone and exact SHA verification are pending.

**41. Declared target frameworks:** Not yet verified from the project files.

**82–111. Restore, build, tests, CI outcomes and compatibility checks:** No local execution results from this walkthrough. CI workflow paths are known, but actual CI runs at this revision have not been checked.

**116. Open gaps:** The host and tool versions, full project configuration, dependency details, source checkout status, and executed verification are still unknown.

**119–121. Discovery steps:** DISC-002, DISC-006 and DISC-011 have limited GitHub source-path findings. All operator-run steps remain pending.

**122. Report disposition:** In progress — further checks needed.

**124. Next action:** Follow DISC-001 in the [step-by-step guide](../../../../methodology/technical-discovery-runbook.md), collect the Windows prerequisite results, and verify a fresh checkout at the selected source commit. Add each verified answer to this report using its numbered field.

## Source evidence

- [EV-001–EV-003: RecordSift evidence manifest](evidence/manifest.md)
- [Previous pre-SDK evaluation](../2026-11-pre-sdk/README.md) — historical background at a different source revision, not evidence of local execution for this report
