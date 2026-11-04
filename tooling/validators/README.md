# Reusable .NET evaluation validators (draft)

**Status:** First toolkit increment, tested locally with Python's standard-library unit tests. These scripts are intentionally **independent of RecordSift**. They are not a substitute for application-specific build, API, resource, packaging and consumer checks.

## Requirements and scope

- Python **3.9 or newer**, standard library only. Git is recommended to capture and verify the complete source revision. To execute .NET build/test gates, install or provision the actual .NET/MSBuild/NuGet/test tools separately.
- **inventory.py:** reads project XML and package declarations without invoking MSBuild. Detects traditional and SDK-style MSBuild projects, explicit property declarations **with conditions**, imports, direct project/assembly/COM references, PackageReference, packages.config, central PackageVersion declarations, .nuspec dependencies, solution filenames and configuration file presence. Records source Git revision, branch and dirty paths.
- **gates.py:** executes an explicit, reviewed array of argv commands **without a shell**, using the application checkout as its working root. Captures stdout/stderr to separate log files and records each gate's exit code, duration, status, expected-negative controls, and optionally NUnit 3 test counts. Records Git revision and source dirty paths before/after execution. Machine-readable output is **JSON schema version 1**.
- Both scripts use **only Python's standard library**. Their own tests do not require .NET, Visual Studio or RecordSift.

They intentionally do **not** evaluate inherited MSBuild properties, prove package feed acquisition origins, scan runtime/native/COM activation, compile projects automatically, resolve NuGet transitive closure, or independently compare binary/API/resource/consumer contracts. Supply those commands as explicit gates once your application has appropriate trusted checks. Do not call a successful workflow a validated upgrade merely because these tools ran.

## Source inventory

Run from the methodology repository, pointing at the unmodified application checkout:

~~~shell
python tooling/validators/inventory.py \
  --source /path/to/application \
  --output /path/outside/application/evidence/inventory.json \
  --expect-commit FULL_40_CHARACTER_GIT_SHA
~~~

The output is a **source-declarations report**, not an evaluated MSBuild property graph or an execution success. Conditional declarations remain distinct. An invalid XML file produces a partial report with an **error exit code 2**; a revision mismatch also returns **2**. Evidence status needs to reflect either condition.

NuGet declarations are recorded as seen, without guessing historical direct/transitive roles. Package source acquisition, compiled DLL ownership and actual runtime dependencies need separate verification. Configuration files are inventoried by presence/path only. Common sensitive property/metadata names are redacted, but **redaction is best effort**: review evidence before sharing or uploading it; do not use source files containing actual secrets.

## Configurable validation gates

Copy and adapt [the example JSON plan](examples/plan.example.json). This example only checks tool availability, **not** an application's compatibility.

~~~shell
python tooling/validators/gates.py \
  --source /path/to/disposable/application-checkout \
  --plan tooling/validators/examples/plan.example.json \
  --evidence-dir /path/outside/application/gates
~~~

A plan has a required \`schema_version: 1\`, an optional application name, an optional immutable \`expected_commit\` (40 hex characters) and a nonempty \`gates\` array. A gate looks like:

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

This is **illustrative**, not a promise that a particular NUnit runner accepts those arguments. Configure the actual command and result-file path for the application. To verify multiple NUnit assemblies, use multiple gates or a trusted aggregate check. NUnit validation accepts the NUnit 3 \`<test-run>\` XML root and compares every configured count; a changed skip is a failing compatibility check.

**Intentional negative control:**

~~~json
{"id": "reject-invalid-input", "kind": "negative",
 "command": ["your-validator", "--invalid-input"],
 "expected_exit_codes": [1], "timeout_seconds": 60}
~~~

A negative control reports \`expected_negative\` **only if the command exits with one of the configured nonzero codes**. Exit code 0 makes the negative control fail. This prevents deliberate failures from being incorrectly treated as application regressions or a green workflow from concealing an unchecked negative control.

The result directory is required **outside the source checkout** to avoid contaminating the observed source status. Each gate creates \`<gate-id>.log\`; \`results.json\` contains per-gate status: \`passed\`, \`expected_negative\`, \`failed\`, \`blocked\`, \`timed_out\`, \`not_executed\`. The overall result is \`passed\` only if **every** gate succeeded or produced its intended negative; otherwise it is \`incomplete_or_failed\`. Use \`--fail-fast\` to skip later checks explicitly, never silently. Exit codes: **0** all accepted; **1** a gate failed/blocked/incomplete; **2** invalid plan, wrong SHA or configuration failure.

## Safety and trustworthy evidence

- **Only run plans you have inspected and authorized**: the gate runner executes the plan's commands; a no-shell invocation does not make arbitrary commands inherently safe. Use disposable, least-privilege environments. Do not run production publishing, deployment or migration by accident.
- **Do not put secrets in command arguments, output filenames or source files**. The runner records complete argument arrays and command output; logs and inventories may be confidential. Control access and retention for evidence.
- Source SHA guards check the **commit**, not the workspace's cleanliness. Every report includes dirty state; review it and use an isolated clean checkout for meaningful baselines. Temporary migration branches can be deliberately dirty; **do not** treat that as a production approval.
- Git not installed/unavailable is reported as a missing source commit; pass \`expected_commit\` in your plans to **require** a matching Git checkout, otherwise explicitly label provenance as insufficient.
- Original RecordSift test runner on frozen \`main\` omits XLSX. Do not reuse it as a five-suite acceptance check without the correct workflow/branch. The verified baseline is **419 discovered, 418 passed, 0 failed, 1 skipped**, but these are **not default values** in the new tools.
- Reuse the [modernization evidence standard](../../methodology/evidence-standards.md). Application-specific API/metadata, resource, XML, NuGet and consumer scripts remain application-owned until separated and tested.

## Tests

~~~shell
python -m unittest discover -s tooling/validators/tests -v
~~~

The tests exercise both legacy and SDK-style project XML, conditional property declarations, central package version declarations, COM and DLL references, partial malformed XML, SHA mismatch, redaction, negative controls, missing executables, fail-fast, NUnit counts, invalid paths, timeouts, and output isolation.

**Verified locally:** 13/13 tests passed on Python 3.13.5 (Linux). Source/test files on this draft branch have Git blob IDs matching the tested local files. A separate pull-request CI workflow runs the suite on Ubuntu and Windows; its result is **not claimed passed until GitHub reports it**.

## Next increments

After stakeholder review, consider a separate source-controlled module for toolchain fingerprinting (MSBuild executable/tool provenance, SDKs/targeting packs, container digests), evaluated-property matrices with controlled configuration/TFM/platform, NuGet restore-resolution closure, explicit API/assembly/resource/package diff checks, and a common report summary/JSON schema contract. Each needs focused tests on **legacy and SDK-style fixtures** before it is generalized. Keep the [historical RecordSift archive in draft PR #21](https://github.com/infoconex/dotnet-modernization/pull/21) unchanged; use it as evidence and regression input rather than treating it as automatically portable.
