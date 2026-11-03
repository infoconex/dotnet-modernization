# Evidence and compatibility standards

## Required record for each experiment

- Experiment ID, objective, hypothesis, and success criteria.
- Application repository, baseline branch, **full commit SHA**, and whether the checkout was modified.
- Host OS and build; container image and **immutable digest**; process/Hyper-V isolation as applicable.
- Inventory of SDKs, runtimes, framework targeting assemblies, compilers, MSBuild paths/versions, NuGet, test tooling and relevant environment variables.
- Tool provenance: **preinstalled**, **explicitly installed**, or **provided by the base image**.
- Exact commands, arguments, working directories, setup steps and required credentials/feeds (without secrets).
- Baseline and post-change results: restore, build, NUnit counts including skips, API, resources, XML documentation, assembly identities, packages, consumer checks when relevant.
- Workflow run and logs; artifact name/ID; retention or reproducibility notes.
- Outcome, unexpected errors, unexecuted checks, scope of conclusion and follow-up work.

## Evidence classifications

| Label | Definition |
|---|---|
| Verified | Reproduced by actual inspection or executed checks with traceable evidence. |
| Partially verified | Some meaningful checks passed; specifically named gates remain incomplete. |
| Unverified | Hypothesis or recommendation without executed proof. |
| Failed hypothesis | Experiment ran and contradicted its success criteria; preserve diagnostics. |
| Blocked | Environmental or access limitation prevented the intended experiment. |
| Not executed | No run; do not describe as passed. |

**Never equate workflow status = success with every embedded experiment passing.** A deliberately failing negative control can coexist with a successful workflow.

## Failure attribution and probe validity

When an experiment fails, identify **which layer actually failed** before blaming the application:

- **Application behavior:** the intended check executed correctly and demonstrated a contract or behavior change. Report the exact reproduced failure.
- **Environment/toolchain:** the check could not run as intended due to missing SDK, targeting pack, compiler, container daemon, credentials, host runtime, implicit assembly loading, or similar prerequisites. Record as blocked or partially verified and identify which earlier checks passed.
- **Experiment harness:** the diagnostic workflow, wrapper, quoting, parameter binding, error handling, or artifact collection was incorrect. Mark that result **inconclusive**, fix the harness in isolation and rerun without changing the application.

A failed workflow is not necessarily a failed application. A green workflow is not proof that every check ran. Preserve the **first failure encountered**, any independent successful gates and the command's true exit code. Repeat only the narrow control needed to distinguish explanations; do not silently reclassify an environmental or harness failure as a product defect.

**Observed pilot example:** [RecordSift EXP-007](../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-007-sdk-only-release-gates.md) found that build/NUnit/XML/API checks succeeded, a packaging invocation initially lacked an implicitly loaded PowerShell assembly, a later wrapper incorrectly quoted a named parameter, and another attempt encountered an unavailable Docker daemon. These are distinct conclusions with distinct verification statuses.

## Compatibility checklist

Before and after meaningful changes, compare:

1. Complete restore and Release compilation, including all production and test projects.
2. All discovered test suites; compare totals, passes, failures, skips and runtime behavior.
3. Public API signatures, type identity, assembly metadata and dependencies.
4. Embedded resource logical names; localized resources when relevant.
5. XML documentation output and intentional warnings-as-errors policy.
6. Package layout, declarations, dependency versions, local install and consumer verification.
7. Supported platform and any build/toolchain dependencies.

Record any check not run, including why. Do not require byte-identical DLL/package hashes unless the build is explicitly deterministic; compare meaningful contracts.

## Artifact retention

Prefer small checked-in text summaries and exact commands. Reference GitHub Actions runs and artifact IDs, but artifacts can expire. Preserve indispensable diagnostics in a durable text record or repeatable script. Never commit secrets, credentials, or unnecessarily large binary artifacts.
