# Reusable .NET evaluation validators

**Status:** Reusable, tested toolkit under continuing development. These scripts are intentionally **independent of RecordSift**. Their observations do not substitute for application-specific builds, API/resource checks, packaging, consumer or security verification.

## Requirements and scope

- Python **3.9 or newer**, standard library only. Git is recommended to capture and verify the complete source revision. To execute .NET build/test gates, install or provision the actual .NET/MSBuild/NuGet/test tools separately.
- **inventory.py:** reads project XML and package declarations without invoking MSBuild. Detects traditional and SDK-style MSBuild projects, explicit property declarations **with conditions**, imports, direct project/assembly/COM references, PackageReference, packages.config, central PackageVersion declarations, .nuspec dependencies, solution filenames and configuration file presence. Records source Git revision, branch and dirty paths.
- **gates.py:** executes an explicit, reviewed array of argv commands **without a shell**, using the application checkout as its working root. Captures stdout/stderr to separate log files and records each gate's exit code, duration, status, expected-negative controls, and optionally NUnit 3 test counts. Records Git revision and source dirty paths before/after execution. Machine-readable output is **JSON schema version 1**.
- All toolkit scripts use **only Python's standard library**. Unit fixtures do not require Visual Studio or RecordSift; the live MSBuild smoke test runs only when the SDK is installed.

The source-only inventory and gate runner remain separate from evaluated-property, existing-restore-graph and compatibility-snapshot tools. Taken together, these tools still do **not** prove package feed acquisition origins, scan all runtime/native/COM activation, compile projects automatically, reconstruct complete legacy NuGet transitive closure, or independently compare binary/API/resource/consumer contracts. Supply those commands as explicit gates once your application has appropriate trusted checks. Do not call a successful workflow a validated upgrade merely because these tools ran.

## Compatibility snapshots and comparisons

The [compatibility snapshot and comparison guide](COMPATIBILITY.md) documents the new `compatibility.py` command, its five optional evidence categories (API, assembly identities, embedded-resource names, NuGet package metadata/path inventory, and NUnit 3 test results), source SHA controls, and its **scoped-match** semantics. Application-specific tools must generate API/assembly/resource manifests before comparison; the toolkit does **not** independently inspect .NET DLLs or certify consumer/runtime compatibility.

## Toolchain, evaluated MSBuild settings and dependencies

These additional commands emit independent, versioned JSON reports. They **do not change source files, run a build, restore packages, validate consumers, or authorize a modernization change**. All output paths must be outside the application's checkout.

Each new report contains its own Git **source commit**, branch and dirty-path observation. Pass `--expect-commit FULL_40_CHARACTER_GIT_SHA` to **every** collector in a frozen-baseline evaluation; the command exits with an error before probing if the checkout doesn't match. Without that option, Git provenance is informative but not enforced. A matching commit does not guarantee a clean worktree; inspect the recorded dirty paths and use an isolated checkout.

### Host toolchain observations

~~~shell
python tooling/validators/toolchain.py \
  --source /path/to/application \
  --output /path/outside/application/evidence/toolchain.json
~~~

Captures OS/architecture/Python, `dotnet` selected SDK version **from the application's working directory** (so `global.json` matters), enumerated SDKs and runtimes, the SDK's MSBuild version, any stand-alone `msbuild` and `nuget` available on `PATH`, installed .NET targeting packs in probed SDK roots, and conventional Windows .NET Framework reference-assembly folder versions. Missing tools and SDK-selection failures are explicit. **This is not a complete Visual Studio/Build Tools inventory**, does not authenticate binaries or image digests, and does not prove that a package/SDK builds an application.

### MSBuild evaluated-property matrix

Copy and edit [the sample matrix](examples/property-matrix.example.json). Choose the actual project(s), properties and explicit build contexts you need.

~~~shell
python tooling/validators/properties.py \
  --source /path/to/application \
  --project path/inside/application/Library.csproj \
  --matrix tooling/validators/examples/property-matrix.example.json \
  --engine dotnet \
  --output /path/outside/application/evidence/evaluated-properties.json
~~~

Repeat `--project` for multiple projects. `--engine msbuild` selects stand-alone `MSBuild.exe` where it is discoverable on `PATH`; the default is `dotnet msbuild`. This feature requires an MSBuild version supporting `-getProperty` (MSBuild 17.8+). Values are obtained **one property at a time**, in each requested `Configuration`, `Platform`, `TargetFramework` or `RuntimeIdentifier` context. The tool records actual evaluated values, explicit empty-or-undefined outcomes and blocked/failed/timeout statuses. An ordinary failed query makes the command return a nonzero status. No `-target:Build` invocation or automatic restore is performed.

**Important:** MSBuild evaluates imported project code and SDK resolvers. Use trusted, isolated checkouts and verify that an experiment cannot invoke unwanted custom behavior. Source-declared settings from `inventory.py` and effective settings from `properties.py` are *different evidence*. An empty result does not distinguish an omitted property from one deliberately set to empty. The CLI restricts property names and context values and does not capture verbose MSBuild error text, but sensitive values can still be present in property results: review plans and generated evidence before sharing.

### Existing NuGet restore graph

~~~shell
python tooling/validators/dependencies.py \
  --source /path/to/application \
  --output /path/outside/application/evidence/dependencies.json
~~~

For **PackageReference** projects with an existing `obj/project.assets.json`, captures the *previous restore's* target-framework/RID-specific package and project library graph, resolved versions and dependency edges, direct declarations when supported by restore metadata, and counts of available compile/runtime/native assets. If no direct-classification metadata exists it reports **unknown**, not transitive. Graph edges can be explicitly unresolved or ambiguous.

For **legacy `packages.config`**, captures exact source-declared versions and target frameworks, with optional folder-presence evidence using `--packages-dir /path/to/restored/packages`. **This is not a complete transitive dependency graph** for legacy projects; directories are not proof of an authentic restore. Reports explicitly distinguish `assets_available`, `legacy_metadata_only`, `no_restore_evidence`, and `partial` (parse failures). The command **never executes NuGet restore**. Stale `obj` data and restore sources must be independently checked. A complete security/dependency provenance review needs additional controls.

**Example evidence order:** capture the immutable source SHA, run source inventory and toolchain inventory, perform an authorized normal restore through the application-provided gate runner, then collect the resolved graph and evaluated settings. Use an isolated workspace and compare *before* and *after* modernization candidates; preserve all logs and note missing gates.

## Source inventory

Run from the methodology repository, pointing at the unmodified application checkout:

~~~shell
python tooling/validators/inventory.py \
  --source /path/to/application \
  --output /path/outside/application/evidence/inventory.json \
  --expect-commit FULL_40_CHARACTER_GIT_SHA
~~~

The output must be **outside the application checkout**; the inventory command rejects an in-checkout path to avoid changing the starting state. The output is a **source-declarations report**, not an evaluated MSBuild property graph or an execution success. Conditional declarations remain distinct. An invalid XML file produces a partial report with an **error exit code 2**; a revision mismatch also returns **2**. Evidence status needs to reflect either condition.

NuGet declarations are recorded as seen, without guessing historical direct/transitive roles. Package source acquisition, compiled DLL ownership and actual runtime dependencies need separate verification. Configuration files are inventoried by presence/path only. Common sensitive property/metadata names are redacted, but **redaction is best effort**: review evidence before sharing or uploading it; do not use source files containing actual secrets.

## Configurable validation gates

Copy and adapt [the example JSON plan](examples/plan.example.json). This example only checks tool availability, **not** an application's compatibility.

~~~shell
python tooling/validators/gates.py \
  --source /path/to/disposable/application-checkout \
  --plan tooling/validators/examples/plan.example.json \
  --evidence-dir /path/outside/application/gates
~~~

A plan has a required `schema_version: 1`, an optional application name, an optional immutable `expected_commit` (40 hex characters) and a nonempty `gates` array. A gate looks like:

~~~json
{
  "id": "unit-tests",
  "command": ["your-nunit-runner", "YourTests.dll", "--result=TestResults/unit.xml"],
  "timeout_seconds": 600,
  "nunit_xml": {
    "path": "TestResults/unit.xml",
    "expected": {"total": 15, "passed": 14, "failed": 0, "skipped": 1}
  }
}
~~~

This is **illustrative**, not a promise that a particular NUnit runner accepts those arguments. Configure the actual command and result-file path for the application. To verify multiple NUnit assemblies, use multiple gates or a trusted aggregate check. NUnit validation accepts the NUnit 3 `<test-run>` XML root and compares every configured count; a changed skip is a failing compatibility check.

**Intentional negative control:**

~~~json
{"id": "reject-invalid-input", "kind": "negative",
 "command": ["your-validator", "--invalid-input"],
 "expected_exit_codes": [1], "timeout_seconds": 60}
~~~

A negative control reports `expected_negative` **only if the command exits with one of the configured nonzero codes**. Exit code 0 makes the negative control fail. This prevents deliberate failures from being incorrectly treated as application regressions or a green workflow from concealing an unchecked negative control.

The result directory is required **outside the source checkout** to avoid contaminating the observed source status. Each gate creates `<gate-id>.log`; `results.json` contains per-gate status: `passed`, `expected_negative`, `failed`, `blocked`, `timed_out`, `not_executed`. The overall result is `passed` only if **every** gate succeeded or produced its intended negative; otherwise it is `incomplete_or_failed`. Use `--fail-fast` to skip later checks explicitly, never silently. Exit codes: **0** all accepted; **1** a gate failed/blocked/incomplete; **2** invalid plan, wrong SHA or configuration failure.

## Safety and trustworthy evidence

- **Only run plans you have inspected and authorized**: the gate runner executes the plan's commands; a no-shell invocation does not make arbitrary commands inherently safe. Use disposable, least-privilege environments. Do not run production publishing, deployment or migration by accident.
- **Do not put secrets in command arguments, output filenames or source files**. The runner records complete argument arrays and command output; logs and inventories may be confidential. Control access and retention for evidence.
- Source SHA guards check the **commit**, not the workspace's cleanliness. Every report includes dirty state; review it and use an isolated clean checkout for meaningful baselines. Temporary migration branches can be deliberately dirty; **do not** treat that as a production approval.
- Git not installed/unavailable is reported as a missing source commit; pass `expected_commit` in your plans to **require** a matching Git checkout, otherwise explicitly label provenance as insufficient.
- Original RecordSift test runner on frozen `main` omits XLSX. Do not reuse it as a five-suite acceptance check without the correct workflow/branch. The verified baseline is **419 discovered, 418 passed, 0 failed, 1 skipped**, but these are **not default values** in the new tools.
- Reuse the [modernization evidence standard](../../methodology/evidence-standards.md). Application-specific API/metadata, resource, XML, NuGet and consumer scripts remain application-owned until separated and tested.

## Tests

~~~shell
python -m unittest discover -s tooling/validators/tests -v
~~~

The tests exercise legacy/SDK-style XML, NuGet restore graph fixtures, declared/direct ambiguity, tool availability, conditional and evaluated MSBuild settings, basic MSBuild execution when installed, negative controls, NUnit counts, malformed files, timeouts, and evidence isolation.

**Verification for this increment:** Locally, 29 tests passed (Python 3.13.5 on Linux, including one live MSBuild smoke test skipped because no SDK is installed). The existing GitHub Actions test workflow checks the full suite on Windows and Ubuntu; consult the current PR checks for hosted outcomes rather than assuming they passed.

## Next increments

After stakeholder review, consider deeper tool provenance (Visual Studio/Build Tools and pinned image digests), effective imported-property origins, legacy NuGet transitive resolution, explicit API/assembly/resource/package diff checks, and a common result schema and summary. The new modules provide **observational foundations**, not those comprehensive compatibility proofs. Each needs focused tests on **legacy and SDK-style fixtures** before it is generalized. Keep the [merged historical RecordSift archive (PR #21)](https://github.com/infoconex/dotnet-modernization/pull/21) unchanged; use it as evidence and regression input rather than treating it as automatically portable.
