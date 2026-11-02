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
