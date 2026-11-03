# EXP-001 — Establish full RecordSift compatibility baseline

**Objective:** Establish a known-good starting point before modifying legacy project configuration.  
**Application:** infoconex/RecordSift, main at `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Date:** November 2, 2026  
**Work state:** Complete  
**Evidence outcome:** Verified

## Environment

GitHub-hosted `windows-2022` runner, Visual Studio 2022 Enterprise MSBuild, .NET Framework 4.8 targeting/runtime tooling, standalone NuGet CLI, NUnit.ConsoleRunner 3.17.0.

Host inventory from related experiments: Windows Server 2022 Datacenter 10.0.20348; MSBuild `17.14.60.43110` at `C:\Program Files\Microsoft Visual Studio\2022\Enterprise\MSBuild\Current\Bin\MSBuild.exe`; NuGet CLI `7.9.0.83`; SDK selection `10.0.403`. These tools were preinstalled on the Windows runner, not evidence of minimal dependency requirements.

## Procedure

The existing workflow:
1. Restored `packages.config` dependencies using the repository NuGet.Config.
2. Compiled the complete Release solution using Visual Studio MSBuild.
3. Ran all **five** NUnit 3 test assemblies.
4. Verified public API and packaging metadata baseline, XML docs, dependencies, package structure, audit and focused checks.
5. Separately validated installed local NuGet consumer behavior and engineering documentation in their own existing workflows.

Representative restore command:

    nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config

## Results

- Domain: 123/123 passed.
- Application: 62/62 passed.
- CSV: 131/132 passed; one deliberate skip.
- Reporting: 54/54 passed.
- XLSX: 48/48 passed.
- **Total: 419 discovered, 418 passed, 0 failed, 1 skipped.**
- API/metadata verifier: **425 accepted entries**.
- Package/docs and clean consumer workflows: passed.

## Evidence

- [Windows build and NUnit](https://github.com/infoconex/RecordSift/actions/runs/41392848910).
- [Local package consumer validation](https://github.com/infoconex/RecordSift/actions/runs/41392848814).
- [Engineering documentation validation](https://github.com/infoconex/RecordSift/actions/runs/41392848879).

## Limitations and conclusion

Existing CI was already configured with Visual Studio and targeting packs, so this is **not** evidence that Build Tools are strictly necessary.

Verified baseline established. See [baseline.md](../baseline.md) for precise configurations and compatibility expectations.
