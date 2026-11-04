# Evaluation validation tooling

This directory distinguishes **preserved experiment code** from **portable, tested tools**. The source experiments for RecordSift were substantial GitHub Actions workflows with embedded PowerShell, rather than a general-purpose command-line framework. Their source can expire from an active branch even while reports remain, so this repository keeps immutable, reviewable snapshots.

## Available source artifacts

[RecordSift November 2026 validation workflow archive](archives/recordsift/2026-11/README.md) preserves eight complete workflow YAML files from tested historical commits. Archives are **not installed, automatically executed, generalized, or approved for production release validation**. They live outside `.github/workflows/` to prevent GitHub Actions from discovering them in this repository.

The [original RecordSift source validation scripts](https://github.com/infoconex/RecordSift/tree/8358780829458854a4b0356df5ac5e685f0a34c8/scripts) remain owned by the application repository, not silently copied into shared tooling. Notably, the frozen `main` version of `scripts/run_tests.ps1` omits the XLSX suite; the approved fix exists on RecordSift `release/0.2` only. Do not use the original script as evidence of a full five-suite run.

For the evidence behind each workflow, see the [dated RecordSift experiment index](../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/README.md) and [run manifest](../projects/recordsift/evaluations/2026-11-pre-sdk/evidence/manifest.md).

## Assembly metadata tooling

The [metadata-only assembly extractor](assembly-metadata/README.md) provides compiled public API/assembly identity/resource-name manifests for the compatibility comparator. It reads ECMA-335 PE metadata without loading application dependencies and requires separate runtime and clean-consumer verification.

## Application-specific proof-of-method pilots

The [RecordSift EXP-014 pilot](pilots/recordsift/EXP-014/run.ps1) exercises the reusable metadata extractor and compatibility comparator against **unchanged** .NET Framework 4.8 release binaries. The [EXP-015 pilot](pilots/recordsift/EXP-015/run.ps1) takes the next step: independently builds the frozen baseline and a **disposable CI-local committed** conditional LangVersion candidate, executes the application's existing release/consumer gates on both, and compares their actual compiled contract evidence. Both are Windows-hosted research workflows under [the dated evaluation](../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/README.md).

**Reuse boundary:** Do not copy the RecordSift-specific project names, expected 419 tests, pinned SHA, DLL layout or packaging scripts into the generic validators. For another application, supply its own fixture/adapter and compatibility specification while reusing the shared inventory, property, evidence, metadata and comparison tools. Capture baseline/candidate revisions separately; the EXP-014 same-binary repeat is not an application migration gate. Neither pilot publishes packages or changes application main.

**Exact package-byte inventory (EXP-017):** [package_payload.py](validators/package_payload.py) is a reusable Python stdlib command-line comparator for two local NuGet archives. It separately hashes the ZIP container and each uncompressed named ZIP member (including packaged DLL and XML bytes), rejects missing, unsafe, ambiguous and oversized input, and reports distinct identical, container-only and member-level changes. It does **not** replace the logical NuGet contract validation in [compatibility.py](validators/compatibility.py), a security scan, or semantic CLR equivalence. [Fixture tests](validators/tests/test_package_payload.py) run on Linux and Windows; the [RecordSift-specific EXP-017 adapter](pilots/recordsift/EXP-017/controls.py) reuses EXP-015 independently built package artifacts and tests a one-member byte mutation. Validated on Windows and Ubuntu in [run 41893283952](https://github.com/infoconex/dotnet-modernization/actions/runs/41893283952), and against actual separate frozen/candidate and repeated frozen-source packages in [run 41893283946](https://github.com/infoconex/dotnet-modernization/actions/runs/41893283946). Rebuilt identical-source assemblies differed in bytes, so a byte mismatch must not be equated with a modernization regression. No application package is published.

## Reusable validators

The [reusable validation toolkit](validators/README.md) now includes source-only inventory, a configurable gate runner, host toolchain observations, evaluated MSBuild properties and available NuGet restore-graph analysis. This is an **incremental toolkit**, not an automated modernization certificate. The historical experiment workflows below remain separately archived and unchanged.

## What to extract into reusable tools

Develop reusable **functions and thin workflow callers** only after a separate design, test and review. In priority order:

1. **Host fingerprint and integrity:** exact source/checkout SHA, allowed experiment-only changes, OS/image digest, MSBuild/SDK/compiler/targeting packs, NuGet/test runner, preinstalled versus provisioned dependencies.
2. **Compatibility-gate runner and machine-readable results:** restore, build, all-test-suite discovery and counts, public API/assembly and resource identity, XML output, package contents/dependencies, clean consumer; record each gate as passed, failed, expected negative, not executed, blocked, or inconclusive. Do not infer gate success from workflow success.
3. **Dependency inventory:** per-project declarations and resolved graph, NuGet source versus acquisition origin, package-versus-direct-assembly ownership, framework/GAC/COM/native/runtime dependencies, and non-NuGet reference scanning with explicit source-inspection limitations.
4. **Controlled MSBuild/property experiments:** source-only property inventory, evaluated properties by configuration/platform/TFM, import order, project override controls, compilation/test parity and rollback in disposable workspaces.
5. **Isolated migration probes:** optional SDK-only build, `global.json` pinning, `packages.config` to exact-pinned `PackageReference`, version-drift detection, format-aware existing validators, consumer compatibility and intentional negative controls.

**Design principle:** parameterize application root, immutable SHA, projects/solutions, configurations, target frameworks, expected tests/skips and API/packaging contracts. Do not encode RecordSift's **419/418/0/1**, 425 entries, `.nuspec`, Windows-only requirements, or its package versions as universal defaults. Keep app-specific adapters separate from common code, and test both original and altered configurations. Version the result schema and test the wrapper on a small fixture before recommending reuse.

## Safe reproduction of a historical workflow

1. Read the [archive provenance and caveats](archives/recordsift/2026-11/README.md) and the corresponding experiment. Select the **exact original application commit** and workflow file. For a *historical* check, distinguish its original evidence/result from later corrected workflows; do not replace a known failing control with a success claim.
2. Use a **new isolated branch/checkout** of the application at the chosen baseline. Review workflow branch-trigger filters, source-diff guards, hard-coded working directories, expected counts, credentials, package feeds and platform prerequisites. A historical file copied unchanged into a new branch is **not guaranteed to trigger or pass**.
3. Inspect the current action and container image provenance and runner capabilities, including Windows Docker availability. Tags and hosted runners are mutable; original image digests, installed tools and signed/pinned actions need independent verification before rerun. Never assume an archived workflow is safe or supported indefinitely.
4. Copy or adapt the workflow in the **application's temporary branch**, under `.github/workflows/`, only with explicit authorization for that experiment. Validate syntax and no unintended release/publish/deploy steps; preserve permissions and isolation. Do not run these archives from the methodology repository or commit temporary project conversions.
5. Run the baseline controls and the selected experiment, collect per-gate results/commands/tool versions, retain test XML and package/consumer metadata, and record current workflow SHA, run/artifact identifiers and deviations from historical setup. Preserve negative results and note unavailable/expired old artifacts.
6. **Do not merge, publish or implement** application changes based on an archived experiment. Any proposed production configuration, format migration, tool migration or SDK conversion needs separate approval and acceptance verification.

This archive is a reproducibility asset and design input, **not an assertion that a reusable execution library has been implemented or revalidated on current runners**.
