# <Application or repository> — Verified application baseline

**Repository:** <owner/repository>  
**Source revision:** <full immutable Git SHA; branch is context, not identity>  
**Source inventory date:** <YYYY-MM-DD>  
**Baseline verification date(s):** <YYYY-MM-DD or not executed>  
**Owner / scope:** <application owner, solution(s), included/excluded components>  
**Inventory state:** <complete / partial with named gaps>  
**Compatibility state:** <verified / partially verified / blocked / not executed>  
**Evidence links:** <workflow runs, logs, artifacts, previously verified baseline>

Use this for substantial application or multi-project evaluations. Follow [the baseline procedure](../methodology/evaluation-process.md#2-establish-the-baseline). For small evaluations, include equivalent information directly in the [evaluation overview](evaluation-overview.md) instead of adding a duplicate file. **Remove empty/non-applicable subsections.** This template is an inventory and verification record, **not a proposed modernization plan or a requirement to add missing configuration files**.

Record the origin and observation status of material claims: **source-declared**, **tool-evaluated**, **executed/verified**, **host-metadata observed**, **not executed** or **unknown**. Pin repository-source links to the baseline SHA; time-stamp mutable GitHub or package registry metadata. Do not infer that a declared version is the actual installed compiler version.

## 1. Repository identity, application and release

| Field | Observed value | Provenance / location |
|---|---|---|
| Git host/provider and repository type | <GitHub/GitLab/etc.; app repo/monorepo/multiple solutions> | <host metadata and date> |
| Repository name, owner, visibility | <values> | <host metadata> |
| Browser URL; HTTPS/SSH clone URLs | <URLs> | <host metadata> |
| Default branch and pinned baseline commit | <branch, full SHA> | <commit/tree link> |
| Source ownership/instructions/license | <team, AGENTS.md/other, SPDX> | <files/host> |
| Submodules, linked worktrees, external/shared sources | <present/absent and paths> | <tree/metadata> |
| Application(s), purpose and consumers | <name, description, library/API/service/web/desktop/CLI> | <README/architecture> |
| Supported OS, runtime, architecture/hosting | <Windows/Linux, runtime, framework, x86/x64/etc.> | <docs/config/build evidence> |
| Published package/release/tag version(s) | <each separate value> | <release/feed metadata; observed date> |
| Source package/manifests version(s) | <each separate value> | <nuspec/csproj/manifests> |
| Assembly, file, informational/product version(s) | <per relevant output> | <AssemblyInfo.cs, project props, compiled metadata> |

**Identity/versions warning:** Solution format, declared VS version, project `ToolsVersion`, SDK version, MSBuild/compiler executable version, target framework, language version, assembly/file version and published package version are separate facts. State inconsistencies rather than silently harmonizing them.

## 2. Directory and solution inventory

Summarize the actual tracked top-level/nested layout. List paths to source, tests, scripts, workflows, requirements, packaging, deployment, configuration and generated/ignored outputs; note any projects outside solutions. A short directory tree or table is sufficient.

| Path | Role and noteworthy content | Source reference |
|---|---|---|
| <directory> | <source/test/config/deployment/etc.> | <pinned Git link> |

Find **every** solution (`.sln`, `.slnx`, filters such as `.slnf`) and standalone project relevant to scope. Do not assume all projects are in one solution.

| Solution/file | Format/version metadata when present | Projects/folders | Configurations/platforms | Mappings/exclusions | Source |
|---|---|---|---|---|---|
| <path or no solution> | <.sln version/VS declaration; .slnx-specific metadata; unknown> | <count and membership> | <Debug/Release/Custom, Any CPU/x64/etc.> | <ActiveCfg, Build.0, explicit dependencies, filters> | <pinned link> |

Record solution project identifiers/GUIDs and paths, solution folders/nested hierarchy, build inclusion per configuration, and any project outside the solution. **Declared** minimum Visual Studio/version metadata is not proof of a working build environment. Solution-level `Any CPU` and project-level `AnyCPU` names can differ.

## 3. Project inventory, settings and references

One row per relevant project (or link to a complete versioned machine-readable inventory for a very large repository). Include project identity and what it actually produces, not just its filename.

| Project path/name | Kind/format/SDK or ToolsVersion | Framework(s)/language | Output, assembly/root namespace/version | Config/platform | Direct project references | Other notable metadata |
|---|---|---|---|---|---|---|
| <.csproj/.vbproj/.fsproj/etc.> | <traditional/SDK-style/test/web/shared> | <TFM(s), C# version> | <Library/Exe/WinExe, identities> | <Debug/Release, AnyCPU/x64> | <paths> | <resources, signing, imports, warnings, generator> |

For each project/condition where relevant, also record:

- Direct `ProjectReference`, `Reference`/`HintPath`, `FrameworkReference`, `PackageReference` or `packages.config`, COM/PInvoke/native or shared-project edges; source dependencies are **not automatically** effective runtime dependencies.
- Explicit or globbed `Compile`, `EmbeddedResource`, linked/generated items, logical resource names, assembly metadata and code generators/analyzers. Preserve compatibility-sensitive outputs through later project-format conversion.
- Conditional `Configuration`/`Platform` groups; `DefineConstants`, optimization, debug/PDB, output/intermediate paths, XML docs and warning policies, signing, pre/post-build events, imports, custom `.props`/`.targets`, packaging/publish settings.
- Declared **versus evaluated** MSBuild properties and imports in the build environment. Note the exact tool/command used to evaluate; don't claim evaluation without executing it.
- Project reference topology including cycles, project-level architecture boundaries and target-framework incompatibilities, when found.

## 4. Existing repository configuration mechanisms

Record relevant files as **present/absent**, source location, current settings/purpose and observation status. *Absent from tracked source* does not rule out imported, machine-wide, environment or generated settings.

| Mechanism | Present / absent / unknown | Path(s), consequential settings and source | Evaluation needed? |
|---|---|---|---|
| `.editorconfig`, `.globalconfig`/rulesets | <state> | <style/analyzer configuration> | <source vs run> |
| `global.json` | <state> | <SDK pin/roll-forward> | <not inferred from dotnet --version> |
| `Directory.Build.props`, `Directory.Build.targets`, `Directory.Build.rsp` | <state> | <imports/defaults/targets> | <evaluate if important> |
| `Directory.Solution.*` | <state> | <solution customization> | <if applicable> |
| `Directory.Packages.props` | <state> | <central package versions> | <if applicable> |
| `NuGet.Config`, `packages.config`, `packages.lock.json` | <state> | <sources, audit, restore style, pins> | <actual restore closure> |
| `.gitignore`, `.gitattributes`, source instructions | <state> | <ignored/generated files, line endings, instructions> | <if relevant> |
| App/host configuration | <state> | <app.config, web.config, appsettings, IIS, Docker, services, IaC, secrets names only> | <if applicable> |

Do not mistake a file's absence for a defect or recommend creating files during source inventory.

## 5. Dependency graph and tooling inventory

| Category | Declared dependency/version | Effective/observed version | Source/evidence | Constraint or known gap |
|---|---|---|---|---|
| Production project references | <paths> | <graph> | <project XML> | <cycles/layers> |
| Test project references and test tools | <NUnit, MSTest, etc.> | <runner version> | <project/CI> | <suite completeness> |
| NuGet/direct and transitive packages | <pins and sources> | <resolved closure> | <restore output/lock/assets> | <license/security/binding redirects> |
| Framework/SDK/targeting packs | <declared TFM> | <installed/ref packs> | <host inventory> | <supported platforms> |
| Build toolchain | <VS/MSBuild/compiler/NuGet> | <actual version/path> | <commands/CI> | <preinstalled vs installed> |
| OS/host/environment | <OS, arch, environment variables> | <version/image digest> | <runner/VM/container inventory> | <external services/feeds> |

Record package **declarations separately from resolved dependencies**, and test/packaging tools separately from distributable production dependencies. Do not record secrets or infer "direct" package intent without evidence.

## 6. Build, test, CI/CD, packaging and runtime entry points

| Operation or workflow | Entry point, exact command/trigger | OS, shell, toolchain and configuration | Inputs/outputs and evidence | Limits |
|---|---|---|---|---|
| Clone and restore | <command> | <environment> | <source/feed> | <secrets names only> |
| Build per solution/configuration | <command> | <Release/Debug, platform> | <DLL/EXE paths> | <unexecuted variants> |
| Full and filtered tests | <command> | <runner, framework> | <counts/results> | <missing suites> |
| API/compatibility checks | <command> | <host> | <snapshot, resources, identities> | <format/tool assumptions> |
| Packaging and consumer check | <command> | <host> | <NuGet/install/consumer> | <unexecuted negatives> |
| CI workflow | <path, triggers, branch filters> | <runner, tool provenance> | <run URL and commit> | <scope of CI gate> |
| Publish/deploy/hosting | <script/workflow, no action taken> | <host> | <artifacts/healthchecks> | <authorization/external dependencies> |

The presence of a workflow/script is **source evidence only**. A passing workflow may contain intentionally failed negative controls or skip tests; describe gate-level execution separately.

## 7. Reproducible compatibility verification

Verification must run on the **unchanged pinned revision** (or cite existing acceptable evidence from that exact revision). Record the actual OS/build environment, immutable container digest if used, tool provenance, command, results and run/artifact links. For absent gates, say **not executed / not applicable** with the reason.

| Compatibility gate | Baseline outcome (verified/partial/failure/unexecuted/N/A) | Exact counts/contracts and evidence |
|---|---|---|
| Restore and complete project build | <status> | <commands/versions/CI SHA> |
| All discovered automated tests | <status> | <discovered/passed/failed/skipped per suite> |
| API/ABI, assembly/file identity, XML docs, resources | <status> | <snapshot/signatures/identities> |
| Package contents, dependency closure and clean consumer | <status> | <artifact/install/consumer logs> |
| Runtime/platform/host/deployment behavior | <status> | <supported workloads and limitations> |
| Application-specific security/integration/performance checks | <status> | <evidence or reason not applicable> |

**Do not require a separate human reviewer.** A reproducible baseline means auditable source inspection and appropriately isolated execution, not perfect application correctness. Test counts are not coverage percentages. Preserve unexpected failures and negative controls.

## 8. Discrepancies, known risks and baseline acceptance

| Observation / missing information | Source vs evaluated vs executed | Impact on comparability | Follow-up (not automatically approved) |
|---|---|---|---|
| <known issue> | <evidence> | <risk> | <candidate or no change> |

**Baseline assessment:** <verified / partial / blocked, with exact rationale>  
**Acceptance constraints:** <what future modernization experiments must preserve>  
**Unexecuted checks:** <list or none>  
**Evidence retention:** <durable notes, links and artifacts; expiration concerns>  
**Reusable baseline?** <yes for exact commit/tool environment, or conditions>

**Boundary:** Completing this document does **not** approve experiments, implementation, merges, release or publication. Link modernization opportunities and decisions from the [evaluation overview](evaluation-overview.md), not by rewriting historical baseline facts.
