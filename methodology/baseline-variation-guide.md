# Baseline inventory — variation and applicability guide

Use this **when preparing** an application baseline using the [template](../templates/application-baseline.md). It is **not** part of the copied baseline. The goal is to avoid assuming that another project uses RecordSift's settings; it is **not** to enumerate every possible MSBuild property or impose empty tables.

## Recording rules

1. **Inspect each independently scoped item.** A repository can contain multiple applications, solutions, projects, target frameworks, configurations, platforms and hosts. Do not copy a value from one project into another without source evidence.
2. **Record facts at the level where they differ:** repository, application, solution, project, project × TFM, project × configuration/platform, environment, or dependency declaration. Use one row per actual item; add columns or focused subordinate tables for material variations. A single shared value or `<Configuration>` display pattern is appropriate **only after comparing applicable declarations**.
3. **Keep provenance separate:** declared in tracked source; inherited/imported/centrally set; evaluated by a specified build tool and conditions; resolved/restored; or observed in executed output. Host/registry/feed metadata may change independently of the source SHA. Do not infer an effective value from an omitted XML property.
4. **Use precise non-values:** *not declared* ≠ *not applicable* ≠ *not assessed* ≠ *unresolved* ≠ *verified absent*. A missing source file does not establish that the toolchain has no corresponding defaults.
5. **Record exceptions, not theoretical examples.** If a variation is not present, do not reproduce this guide's examples in the application's baseline. If a property has an additional mechanism or a nonstandard setting not listed here, record it with evidence as **Other**. This reference is deliberately extensible.
6. **Separate consumers and implementations.** A source package reference, a restored NuGet archive, a referenced DLL, a compiled output assembly and a published package dependency are different facts. Relate them without duplicating the same package as unrelated dependencies.
7. **Do not invent validation.** A source inspection alone is not an executed build/test/runtime trace. Missing evidence remains a named gap rather than a claim of absence.

## 1. Application and repository fields

| Field | Variations to check | Record at |
|---|---|---|
| Repository host, identity, type | GitHub, Azure Repos, GitLab, other Git/host; standalone application, monorepo, multiple applications, nested repos/submodules, external shared files | Repository, with source SHA and observed host-metadata date |
| Access and clone | Public/private/internal; HTTPS, SSH, enterprise/custom URLs; remote may use credentials; missing/not applicable clone methods | Repository; never include access tokens |
| Branches and source revision | Default vs evaluation branch vs detached tag; submodule SHAs; moving branch vs immutable commit | Every separately checked source tree |
| Application type and consumers | Library, API, web app, service, worker, console, Windows desktop, mobile, test/tool, cloud-hosted or mixed workloads | Per application or deployable component |
| Runtime/platform/architecture | .NET Framework, modern .NET, .NET Standard (library contract), multiple targets; Windows/Linux/macOS; x86/x64/ARM64; IIS, Windows Service, container, serverless, desktop, library distribution | Per application, artifact, and tested host as needed |
| Identity and versions | Repo/tag/release, application/product, NuGet package, nuspec, assembly/file/informational versions may diverge or be generated/conditioned; multiple artifacts may have different versions | Individual version identifier, with declaration or binary source |
| License / ownership | Repo-wide vs project/package-specific; no license or third-party notices; owners/CODEOWNERS may differ by path | Applicable scope; link to evidence |

## 2. Solution and project fields

| Field | Variations to check | Record at |
|---|---|---|
| Solutions / entry points | None, one, many; `.sln`, `.slnx`, solution filters, build orchestration without a solution | Each solution and standalone project |
| Solution metadata / mapping | Format-specific version or no such field; folders; project GUID/type/path; solution vs project configuration/platform names; project `ActiveCfg` vs `Build.0`, exclusions and dependencies | Each solution × configuration/platform |
| Project kind / file format | SDK-style, traditional .NET Framework, C#/`csproj`, VB/`vbproj`, F#/`fsproj`, Web Application, test, shared project, C++/CLI/native, other | **Each project**, with direct path |
| SDK / MSBuild imports | `Sdk` attribute/elements, explicit/custom `.props`/`.targets`, imported defaults, targets/toolset version, condition and import order | Project + imported configuration; distinguish declared vs evaluated |
| Target framework | `TargetFrameworkVersion` vs `TargetFramework`/`TargetFrameworks`; single, multitarget, conditionally set, inherited, absent or unsupported; framework references/targeting packs | Each project × target framework |
| Language and compiler | Explicit `LangVersion`, `default`/`latest`/version, inherited/SDK default; nullable, implicit usings, compiler, analyzers/generators, VB/F# equivalents | Each applicable project × configuration/TFM |
| Output and project identity | `Library`, `Exe`, `WinExe` or technology-specific output; project GUIDs/IDs, assembly name, root namespace, version, signing, generated assembly info | Each project/artifact |
| Platform and architecture | Solution `Any CPU` vs project `AnyCPU`; x86/x64/ARM64/Mixed, `PlatformTarget`, `Prefer32Bit`, RID; conditional platform mappings, COM/native bitness | Each project × relevant configuration/platform |
| Property values and precedence | Unconditional, Debug/Release/other configurations, per-platform/TFM, inherited/overridden, environment/global properties, absent values; multiple `PropertyGroup` definitions | Project × material condition; declared and **evaluated** separately |
| Compiler/build settings | Optimization, debug symbols/type, defines, warning level / warnings-as-errors, nullable, treatment of warnings, deterministic flag, unsafe/checked, analyzers | Per project; split Debug/Release **columns only when they differ** |
| Output, docs, resources | Output/intermediate paths, globbed vs explicit sources, linked/generated files, XML-doc paths, embedded-resource logical names, satellite resources, signing and copy rules | Per project × relevant configuration/TFM |
| Project relationships | Direct `ProjectReference`, references conditional on config/TFM, shared projects, build order, aliases, cycles, project outside solution | Per referencing project; don't duplicate in external-dependency list |

## 3. Repository configuration fields

| Field | Variations to check | Record at |
|---|---|---|
| Directory organization | Conventional/nonstandard source/test/tool/deployment folders, nested solutions and generated folders, submodules, shared files outside checkout | Directory purpose, not file counts |
| Shared MSBuild files | `Directory.Build.props`/`.targets`/`.rsp`, `Directory.Solution.*`, nested files with nearest-file import behavior, custom imports; file present vs evaluated impact | Relevant directory scope, then project-specific exceptions |
| SDK and style | `global.json` SDK pin/roll-forward or inherited absence; `.editorconfig` nested severity/naming and analyzer settings; generated sources | Scope/path and effective evaluation where executed |
| NuGet configuration | Zero/one/multiple `NuGet.Config` layers, machine/user config, `clear`, local/private/public sources, `auditSources`, package-source mapping, fallback folders, credentials (names only) | Config scope and observed restore environment |
| Package management | `packages.config`, `PackageReference`, Central Package Management, package-version override, lockfile, dependency constraints, non-NuGet packages | Per project / package |
| Runtime/deployment configuration | `app.config`, `web.config`, `appsettings`, binding redirects, IIS/Windows-service settings, container/IaC, per-environment files, connection strings | Per application/host; no secrets |
| Repository policy/automation | `.gitignore`, `.gitattributes`, LFS, CODEOWNERS, CI config, Dependabot, AGENTS/AI instructions, generated or user-local files | Applicable repository/path |

## 4. External dependency fields

| Field | Variations to check | Record at |
|---|---|---|
| NuGet declaration | `packages.config` installed list vs `PackageReference` (inline or central version), explicit/direct vs inferred transitive, exact/range/floating version, conditional package/TFM/configuration, test/build tooling | **Each project/package declaration** + source file |
| NuGet source/provenance | Multiple eligible feeds, source mapping, explicit source overrides, local folder, cache/offline restore; configured feed ≠ verified downloaded origin | Per package when different; otherwise common config plus named evidence gap |
| Dependency closure | Declared vs resolved version, runtime/build/analyzer/native assets, target framework group, binding redirects, copied files; installed package can contain multiple assemblies | Package graph / per project/target; only label verified closure as such |
| Managed assembly reference | Framework/reference assembly, GAC candidate, NuGet-owned DLL `HintPath`, non-NuGet relative/absolute `HintPath`, assembly alias, `Private`/copy-local; file may be tracked, generated, installed or missing | Each non-NuGet reference; link package-owned references to NuGet row instead of duplicating |
| COM / interop | `COMReference`, `COMFileReference`, generated or checked-in interop assembly, registration/ProgID/CLSID/type-library GUID/version, 32/64-bit or per-user registration, runtime COM activation | Each component and consuming project/host; state discovery limits |
| Native dependencies | P/Invoke/`DllImport`, `LibraryImport`, dynamic native loading, C++/CLI, `.lib`/DLL, native NuGet assets, x86/x64/ARM64 and runtime search paths | Each native binary/consumer where discovered |
| Runtime external systems | HTTP/gRPC/API, DB, queue, shared storage, OS registry/certificates, Windows service, installed drivers, external process; optional vs required, environment-specific | Application × runtime environment; source inspection vs runtime evidence |
| Build/test external tools | MSBuild tasks, code generators, Java/Python/Node tooling, VS Build Tools, test runner and coverage tools, web browsers, installers | Build/test workflow and host, version/provenance |
| Distributable contract | Application NuGet package vs project packages, `.nuspec` dependencies, assets/targets/README/docs, runtime copies and clean consumer | Published/packaged artifact separately from developer restore |

## 5. Build, verification and gaps

| Field | Variations to check | Record at |
|---|---|---|
| Host and toolchain | Local developer, VM, hosted/self-hosted runner, Windows/Linux/macOS, architecture/container digest; installed/preinstalled SDK(s), targeting packs, MSBuild variant/compiler, NuGet/tool version | Each executed environment, not inferred from solution metadata |
| Restore/build matrix | Project/solution entry point, configuration, platform, target framework, RID, clean vs cached restore, network availability, secrets/feed requirements | Each executed combination or named unexecuted gap |
| CI/CD pipelines | Multiple workflows, branch/PR/tag triggers, paths, build matrix, permissions, publishing/deployment, scripts/runner provenance; presence ≠ executed success | Per significant workflow/gate |
| Tests | Unit/integration/acceptance/UI, frameworks/runners, discovered/passed/failed/skipped, category filters, OS/runtime constraints, intentionally skipped tests | Suite or gate × executed environment |
| Compatibility gates | API/ABI, assembly identity, resource logical names, XML docs, package metadata/layout, dependencies/security, native/COM registration, clean consumer and runtime behavior | One independently checked fact per row, with outcome and evidence |
| Verification status | Passed, failed, partial, blocked, not executed, not applicable; deliberate negative control vs harness failure | **Per gate**, not whole workflow shorthand |
| Issues and omissions | Known stale docs/scripts, unsupported targets, unavailable sources, missing files/tools, conditional cases or OS/architecture not tested | One evidence-backed gap per row |

**Use this guide to ask what *could differ*. Write only what *actually differs or is observed* in the baseline.** It is valid to say a source scan found no `COMReference` while leaving runtime COM activation **not assessed**. Changes and recommendations belong in the evaluation's experiments/findings/roadmap, not in the immutable factual baseline.
