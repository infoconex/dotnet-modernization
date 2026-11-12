# Native-first .NET technical discovery runbook

This is the **reusable how-to** for collecting an evidence-backed technical baseline. Use it with the [application baseline template](../templates/application-baseline.md), [discovery execution log](../templates/discovery-execution-log.md), and [baseline variation guide](baseline-variation-guide.md). It supplements the [evaluation lifecycle](evaluation-process.md); it does **not** authorize new experiments, application changes, modernization assessment, or publication.

**Operating rule:** run an applicable built-in Git, .NET SDK, MSBuild, NuGet, test-runner, or CI command **manually first**. Inspect the original output, record the command's true outcome, and only later decide whether a portable reporting script would help. A source-inspection-only pass is valid when commands cannot safely run.

## Before starting

1. Review existing documentation/evaluations and the [evaluation lifecycle's scope gate](evaluation-process.md#start-here-first-contact-protocol). For a new evaluation, agree and record the scope before new experiments; read-only source inspection can precede approval. Do not assume that a previous pilot authorized a new evaluation or a publishing action.
2. Freeze the **exact source commit SHA**; record checkout branch/tag, working-tree modifications, local or external inputs, discovery date, and who performs each command. A branch name is not immutable.
3. Identify application roles and the actual available toolchains before choosing commands. A .NET Framework project, SDK-style project, SDK-installed host, and Visual Studio installation are not interchangeable.
4. Record each step in the [execution log template](../templates/discovery-execution-log.md). Store the summarized technical facts **once** in the [application baseline](../templates/application-baseline.md); link its findings to durable evidence via the evaluation's evidence manifest.
5. Do not include credentials, tokens, private feed URLs containing secrets, user profile paths, personally identifiable data, or raw environment dumps in committed records. Redact sensitive content **in a copy**, noting the redaction. Preserve raw material securely only where permitted.

### Two independent classifications

**Evidence method:** **source-inspected** (file/definition at a known revision), **tool-evaluated** (resolved configuration/graph under stated inputs), or **executed** (an operation actually ran, with outcome). A failed operation is still executed evidence of that failure. An evaluated setting is not proof of a successful build. Separately record **provenance** (collected now vs historical and its original scope).

**Applicability:** describe separately the *project system* (SDK-style / traditional MSBuild / mixed / unknown), *target framework(s)* (.NET Framework, modern .NET, .NET Standard library contract, etc.), *host/toolchain* (Windows/other OS, Visual Studio MSBuild, `dotnet msbuild`, NuGet CLI), and *tool versions*. Do not label a procedure "all .NET" based on one RecordSift run. Use "tested on", "documented to support but not tested here", "not applicable", or "not established" explicitly.

### Command safety and records

| Activity | Default behavior | Permission |
|---|---|---|
| Git identity/status, tracked-file listing, read-only project/CI inspection, tool version queries | No repository modification expected | Suitable for source discovery |
| MSBuild `-getProperty` / `-getItem` queries (on compatible MSBuild) | Evaluation rather than compilation; imports/tasks may still load and some custom project evaluation may have side effects | Inspect inputs before use |
| NuGet restore, `dotnet restore`, or lock-mode restore | Writes package caches, `obj`/assets/lock-related files and possibly repository files depending on configuration | Require explicit execution scope and record side effects |
| MSBuild build/rebuild, `dotnet build`, `dotnet test`, runners, packaging, CI triggers | Can create/remove outputs or run custom build/test actions | Execute only within approved environment/scope |
| Package publish, release, deployment, migrations, source edit, `dotnet new` | Alters applications or external state | **Not part of discovery**; separate approval required |

Run commands individually. Capture the **exact command**, working directory, full output or durable excerpt, exit code, date, tool version, environment, and source SHA. A green workflow does not establish that every expected check ran. Never replace a failed command with a different one and report the original as successful.

## DISC-001 — Acquire and identify the exact source

**Purpose:** obtain a trustworthy source checkout, then record the exact revision and working-tree state. **For a reproducible case study, prefer a fresh clone into a new, dedicated folder** rather than resetting or cleaning an existing workspace. Reusing an existing checkout is still valid when its state is inspected and documented.

### A. Confirm Git and select a safe location

Run in PowerShell:

```powershell
git --version
```

Choose an existing parent directory where creating a new checkout is permitted. Verify that your intended destination folder does **not** exist before cloning. **Do not delete, overwrite, reset, or clean an existing directory** just to make a discovery look reproducible.

### B. Choose one acquisition path

**Preferred for a new baseline walkthrough — fresh isolated clone:**

The following is an example. Replace the parent path, Git remote and frozen source SHA with the application's actual values. The example paths are placeholders, not assumptions about the operator's machine.

```powershell
Set-Location "C:\path\to\parent-directory"
Test-Path .\REPOSITORY-discovery
git clone --no-checkout https://github.com/OWNER/REPOSITORY.git REPOSITORY-discovery
Set-Location .\REPOSITORY-discovery
git switch --detach FULL_COMMIT_SHA
```

**Stop if `Test-Path` returns `True`; choose a different unused folder name.** Run commands individually and check errors before continuing. `git clone --no-checkout` creates a new local repository without checking out the changing default branch; `git switch --detach` then populates its working tree at the **frozen immutable commit**. The detached HEAD is intentional for a baseline snapshot. `git switch` requires Git 2.23+; on older installations, evaluate an appropriate documented alternative rather than silently changing the instructions.

**Side effects:** clone downloads Git objects and writes the new destination folder; switching to the frozen commit writes its tracked files. These commands do not change the remote repository or an existing checkout. Private/enterprise repositories may require an approved authenticated remote. Never embed credentials in recorded clone URLs.

**Existing checkout path — if you deliberately choose to reuse it:**

```powershell
Set-Location "C:\path\to\existing-checkout"
```

Do not clone again into the same folder. Inspect the existing checkout **before** any operation that changes its branch or files. Reusing it is not evidence of a clean environment; record its status and any ignored/generated files that could affect the investigation.

**Do not assume the default-branch HEAD equals the frozen baseline SHA**, even immediately after cloning. Avoid automatically running `git pull`, `git reset`, `git clean`, or branch switches in an existing workspace.

### C. Verify the local source state

Inside the chosen checkout, run these native Git commands individually:

```powershell
git rev-parse --show-toplevel
git rev-parse HEAD
git branch --show-current
git status --porcelain=v1 --untracked-files=all
git remote get-url origin
```

For the preferred fresh-detached clone, the expected observations are: **HEAD equals the recorded SHA**, `git branch --show-current` prints no branch name, and `git status --porcelain` prints nothing. These are *expected*, not proof until the operator shares actual output. For a reused checkout, record any divergence. Check optional submodules or external source dependencies separately when relevant.

**Applicability:** Git operations are independent of .NET Framework, current .NET, SDK-style or traditional project formats. Applications not stored in Git need a different source-identity mechanism.

**Evidence:** method of acquisition (fresh clone / existing), sanitized remote, Git version, approximate execution time, full source SHA, checkout/ref state, clean/dirty status and relevant external inputs. Redact personal paths, credentials and secrets before committing or sharing.

**Limit:** a pristine Git working tree does **not** establish a pristine build environment. Installed SDKs, targeting packs, MSBuild, user-level NuGet configuration, global package caches, environment variables and network feeds can still affect subsequent commands. Record those in DISC-004 onward.

**Stop/check:** if HEAD differs from the intended SHA, the checkout is unexpectedly dirty, the commit cannot be checked out, or the clone fails, preserve the actual diagnostic and resolve the mismatch before continuing. Do not erase evidence by cleaning or resetting files.

## DISC-002 — Inventory solutions and projects

**Purpose:** identify every solution and project, not merely the projects reachable from the first solution.

```powershell
git ls-files "*.sln" "*.slnx" "*.slnf" "*.csproj" "*.fsproj" "*.vbproj"
dotnet --version
dotnet sln .\RecordSift.sln list
```

The `RecordSift.sln` path above is **illustrative and project-specific**; substitute an actual discovered solution, or omit `dotnet sln` if the repository has none. `dotnet sln ... list` requires a compatible .NET SDK; if unavailable, inspect the solution file directly. Capture standalone projects, multi-solution overlaps, solution filters, project roles and project references. A solution filter is a subset view, not a new project graph.

**Applicability:** Git listing is generic; `dotnet sln` applies only where an SDK supports the solution format. **Evidence:** tracked paths are source-inspected; CLI solution listing is tool-interpreted, not a build.

## DISC-003 — Identify project formats and declared targets

Inspect a representative project file and each materially different project. Record `<Project Sdk=...>` / imported SDK indicators, traditional imports, `TargetFramework`, `TargetFrameworks`, `TargetFrameworkVersion`, project role, language, output type, configurations, project references and conditional declarations.

**Applicability:** SDK-style and traditional projects can both target .NET Framework; target framework alone does not identify project format. Multi-targeting and conditional values must be scoped per project/target/configuration.

**Evidence:** file path and relevant source lines at the frozen SHA. Do not infer evaluated defaults from omitted XML declarations.

## DISC-004 — Check toolchain availability and versions

Run the commands supported **on the actual host**, recording "not installed" rather than forcing substitutions:

```powershell
dotnet --info
dotnet --list-sdks
dotnet --list-runtimes
msbuild -version -nologo
nuget help
```

`msbuild` requires a suitable MSBuild installation on PATH, often a Visual Studio Developer PowerShell on Windows; `nuget` requires a standalone NuGet CLI. Their absence is not evidence that the application cannot build. `dotnet --info` does **not** establish that .NET Framework targeting packs or Visual Studio Build Tools are installed.

**Capture:** OS/architecture, SDK/runtime list, actual MSBuild implementation/version, NuGet CLI version, Visual Studio/Build Tools and .NET Framework targeting-pack prerequisites where applicable. Record tools as preinstalled versus explicitly supplied. Avoid dumping all environment variables.

## DISC-005 — Inspect imported and evaluated build settings

First inspect declared project and repository configuration, including `Directory.Build.props`, `Directory.Build.targets`, imported `.props`/`.targets`, `global.json`, conditional settings, compiler properties and custom targets.

For MSBuild **17.8+**, on a compatible project and host, try property queries *without building*:

```powershell
msbuild .\path\to\project.csproj -getProperty:TargetFramework -getProperty:TargetFrameworkVersion -p:Configuration=Release
```

The path is a placeholder, not a RecordSift command. On some supported toolchains, `dotnet msbuild` can perform the same property query; **do not assume** it can evaluate every traditional project. Record command, MSBuild version, configuration/platform, framework and environment. For multi-targeting, repeat under explicitly selected target frameworks and configurations when applicable.

**Capture separately:** source declarations, evaluated output, and any conflicts. MSBuild evaluation may differ from values after target execution; **no successful build is established**. If `-getProperty` is unsupported, record "not evaluated" and retain source inspection without installing or upgrading tools solely to fill a row.

## DISC-006 — Inventory central configuration

Use `git ls-files` or direct source inspection to locate relevant `global.json`, `Directory.Build.props`, `Directory.Build.targets`, `Directory.Packages.props`, `nuget.config`/`NuGet.Config`, `.editorconfig`, `.globalconfig`, local tool manifests, response files and project-specific imports.

For each relevant mechanism, record its location, applicability, declared settings and (where verified) actual import/precedence. Configuration can be nested or supplied by a user, machine, SDK, environment or command line. **A missing file is an observation, not a recommendation to add it.**

## DISC-007 — Inventory dependencies without restoring

Inspect `ProjectReference`, `Reference`, `HintPath`, `packages.config`, `PackageReference`, central package versions, NuGet source configuration, native/COM/local DLL dependencies and documented external services.

```powershell
dotnet nuget list source
```

This **lists configured NuGet sources** on hosts with the applicable SDK; it does not prove which feed a restore uses or which packages resolve. Review feed URLs before sharing. The separate NuGet CLI has its own source-inspection commands where installed. Record declaration scope, source location and relevant versions; don't conflate package declarations, restored packages, a produced assembly, and a published package's consumer dependencies.

**Do not restore yet.** Package graphs from existing assets/lock files may be inspected as artifacts, but their existence alone does not prove a current successful restore or locked-mode enforcement.

## DISC-008 — Reproduce dependency restore (approved execution only)

Choose **the application's documented working restore command** and confirm the tool/format match. For example, an application using `packages.config` may require standalone `nuget restore <solution>` and an explicit packages directory; applicable SDK-style/`PackageReference` projects often use `dotnet restore <solution>`. Neither should be substituted automatically for the other.

Record the exact command, feed/configuration scope, package cache and generated-file side effects, tool version, source SHA, outcome, and any produced assets or lock-file behavior. A successful restore verifies **that restore invocation**; graph completeness, feed provenance and locked-mode enforcement require their own supporting evidence.

If the environment is missing packages, credentials or feeds, record "blocked"; do not create new credentials, change package versions, or bypass feed restrictions.

## DISC-009 — Perform build verification (approved execution only)

Find existing documented commands in scripts, workflows or developer instructions **before selecting an invocation**. Identify intended solution/projects, configuration, platform, framework, host/toolchain and any restore prerequisite.

For a compatible SDK-style project, `dotnet build <solution> --configuration Release` is a *candidate*, not a universal command. Traditional Windows projects may require `MSBuild.exe <solution> /t:Build /p:Configuration=Release` with a particular platform, build tools and targeting packs. `Rebuild` removes existing build outputs; do not substitute it without accounting for that side effect.

Record exit code, warnings/errors, products, environment and exact scope. A build of one project or Debug configuration does not verify all solution projects or a Release package.

## DISC-010 — Inventory and execute tests (approved execution only)

Identify every test project/assembly, framework, runner, filtering rules and the established local/CI commands. Use `dotnet test` **only where the project and runner support it**. Other applications may use standalone NUnit, VSTest, or application-specific runners.

Capture tests discovered, executed, passed, failed, skipped, configuration, platform, target framework, complete assembly coverage, runner version, and any result/coverage artifacts. "All tests passed" is unsupported if an expected test assembly was omitted. An execution result does not establish comprehensive functional coverage.

## DISC-011 — Inspect CI/CD, packaging and deployment

Read repository workflow definitions and existing run evidence without triggering new releases or deployments. Identify triggers, runner images, toolchains, source SHAs, restore/build/test commands, retention, artifacts, secrets *names only*, packaging and distribution.

Record definition (source-inspected) separately from completed run logs (historical executed evidence). Review runtime/hosting prerequisites appropriate to libraries, services, desktop or web applications. A package manifest or workflow definition does not prove a released artifact exists.

## DISC-012 — Identify existing compatibility evidence

Find existing checks for public API and assembly identities, resources, XML documentation, serialization contracts, package consumers, native dependencies and other relevant contracts. Link to existing snapshots and scripts.

Record whether each check was merely defined, previously executed for a different revision, or actually run for the selected baseline. Do not rerun or add gates without a justified scope; functional scenarios remain in their established documentation.

## DISC-013 — Reconcile and close evidence gaps

Compare **like scopes only**: the same source SHA, project, target framework, configuration, platform, toolchain and relevant environment. Distinguish failed application behavior, missing environment prerequisites and faulty harness/command setup.

Mark each significant finding with evidence type, provenance and status: verified for stated scope, partially verified, blocked, failed, not executed, not applicable or unresolved. Preserve negative results and exact failure diagnostics. Never copy old test counts into a fresh verification column.

## DISC-014 — Produce and review the baseline

Populate [`templates/application-baseline.md`](../templates/application-baseline.md) with **observed** applicable fields, not speculative examples. Link evidence through the execution log and manifest; avoid duplicating raw logs in the baseline.

Check that a second engineer can identify the exact source, reproduce applicable inspection and verification commands, find outputs, understand gaps and separate **discovery facts** from later modernization decisions. Date/freeze the baseline; a later source SHA requires a separate snapshot or clearly scoped follow-up.

## When should a reusable script be created?

**Not during the initial native-command walkthrough by default.** After manual execution, evaluate whether automation materially reduces repetition, reliably normalizes complex results or improves traceability.

A proposed collector must have:
- A defined **input contract** (repository, solution/project paths, framework, configuration, platform, command/tool versions, output location). No hardcoded RecordSift paths.
- A **supported-applicability matrix**, including SDK-style/traditional, target framework families, operating systems/toolchains; distinguish *tested*, *documented but untested*, *unsupported* and *unknown*. One successful RecordSift run verifies only that tested combination.
- A reviewable **side-effect contract**: read-only wherever practical; explicit approval for restore/build/modified files; no publishing, source changes, credentials, or hidden network activity.
- Raw output preserved with true exit codes and immutable source identifiers; report summaries cite the raw evidence and never hide skipped/failed operations.
- Formatting/reporting separated from command execution where practical. Test both expected output and failure handling, with fixtures from genuinely different environments before claiming portability.

Record the proposed benefit and validation results before adding any script to the reusable tooling tree. A project-specific helper belongs with its project unless or until its broader applicability is demonstrated.

## Documentation ownership

- **Reusable instructions:** `methodology/technical-discovery-runbook.md`.
- **Reusable recording schema:** `templates/discovery-execution-log.md` plus the existing `templates/application-baseline.md`.
- **Application-specific records, results and evidence:** `projects/<app>/evaluations/<dated-scope>/` in this repository. Retain historical evaluations as separate immutable evidence.
- **Application code and existing CI:** the application repository; do not alter them for a read-only discovery.
- **Publication drafts and images:** `infoconex/coding-blog`. The article selectively demonstrates findings and links to the canonical technical records; it is not an authoritative evidence store.
