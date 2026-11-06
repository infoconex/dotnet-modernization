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


## Tool-specific acceptance semantics (November 2026 clarification)

When a proposed modernization depends on an IDE, debugger, package extension, COM registration, GUI wizard, generator, native symbol reader or runtime host, **presence of the installed component is not proof of operation**. Record separately: (1) installed package/IDE version and cryptographic provenance, (2) active host/service and invoked API, (3) tool operation and actual changed project/package/assembly/PDB/runtime artifacts, (4) all release/consumer contracts, (5) explicit positive and negative controls. A NuGet CLI `install` or `restore` result does not establish Visual Studio Package Manager **project installation** semantics; a Csc `/sourcelink` argument or native PDB mapping does not establish actual Visual Studio debugger stepping or managed document checksum authenticity. Distinguish standalone PowerShell commands from Visual Studio-hosted Package Manager Console commands.

For security-sensitive native readers, check the **specific binary actually loaded** (version, original source, signed publisher/hash, applicable advisories and update level), rather than assuming an OS/IDE signature certifies patched status. If reader safety or document coverage cannot be established, stop the affected gate as **BLOCKED** or **INCONCLUSIVE** and continue other independent work. A planned manual procedure is **NOT TESTED** until executed; a documentation-only review cannot invent a new workflow/artifact. This reusable standard applies to any legacy application with COM/native/external host dependencies, not only RecordSift. See [RecordSift acceptance gate protocol](../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/remaining-source-link-approval-gates.md).

## Native PDB source-document completeness (research evidence pattern)

When evaluating classic Windows PDB source integrity, separately inventory the following **non-equivalent** structures: (1) managed symbol-reader documents, (2) native named `/SRC/FILES/` source records, (3) the DBI module File Info source list, (4) C13 `FILECHKSMS` entries and references, and (5) C13 line-block source references. Do not infer a full relevant-document universe from only one or two implementations, especially if both share a discovery limitation. A source may have a checksum and a DBI/C13 file reference without any executable line information.

Join identities using complete normalized document paths, not basenames or untrusted PDB source paths opened as files. Check native stream ID bounds and uniqueness; DBI module source-file counts/offsets; the C13 `/names` offset, checksum algorithm/length and aligned record boundaries; C13 line-block sizes **including the block header**; each line-block reference to its module checksum-record offset; repeated document identities across modules; and PE/PDB CodeView GUID+age. Retain malformed/unsupported cases as fail-closed findings. Validate checksums against **separately trusted, exact original physical compiler-input bytes**; a native digest, a matching cross-reference, or a Git blob alone is not sufficient. Require evidence for generated or external inputs and for source-path mapping differences.

Use source files and PDBs from a **trusted, locally controlled build** only. Raw PDBs, DLLs, private paths, private reader URL inventories, source bytes, and full hash values must not appear in published logs/artifacts. Sanitized evidence may contain counts, Boolean relationships, algorithm categories, and opaque identifiers; delete private manifests under `finally`. A bounded custom parser is not a hostile-input security audit. Preserve failed harness runs separately from genuine application regressions.

Maintain separate dispositions for document-inventory coverage, native checksum structural agreement, original-source-byte authentication, original/candidate release compatibility, managed-reader API exposure, authentic Visual Studio project installation and live debugger source stepping. **A passing native audit does not automatically replace a previously approved checksum acceptance gate.** Any alternative evidence pathway or adoption decision needs explicit stakeholder approval. Pilot: [EXP-040 RecordSift native provenance](../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-040-native-document-provenance.md).
