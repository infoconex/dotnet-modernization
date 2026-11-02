# Modernization investigation catalog

Use this catalog to **discover worthwhile modernization opportunities**, not prescribe a fixed upgrade sequence or create mandatory files. The [evaluation process](evaluation-process.md) describes how to work; [evidence standards](evidence-standards.md) define verification. This catalog lists what to consider.

During intake, screen areas for relevance to the application's purpose, platforms, consumers and constraints. Record **applicability** (applicable / not applicable / undetermined) separately from **assessment state** (evaluated / deferred / not yet assessed), **evidence outcome**, **decision**, and **implementation**. An evaluated area may conclude *no change warranted*.

A proposal should identify the specific problem, benefits, affected files, baseline SHA, hypotheses, risks and verification gates. Work can occur before, during or after SDK conversion **when appropriate**; these are not universal dependencies. See the detailed [repository configuration and tooling assessment](repository-configuration.md) for `global.json`, `.editorconfig`, MSBuild/NuGet central files and test settings.

## Areas to consider

| Area | Investigation questions | Risks / verification |
|---|---|---|
| **1. Baseline and compatibility** | Inventory frameworks, configurations, full test suites, public APIs, assembly/resource identities, packaging and consumers. | Compare recorded baseline commits, build/test counts, APIs, resources and consumer gates; distinguish unexecuted checks. |
| **2. MSBuild and project configuration** | Evaluate shared properties, imports, overrides, duplication and conditional settings in traditional/SDK projects. | Inspect evaluated properties and imports; preserve build outputs and project-specific behavior. |
| **3. Toolchains and environments** | Inventory SDK, MSBuild, compiler, targeting packs, NuGet, runners, Visual Studio/Build Tools and clean hosts/containers. | Record tool provenance, image digests and exact commands; verify complete gates rather than build success alone. |
| **4. Dependencies and NuGet packaging** | Inspect direct/transitive packages, security, sources, PackageReference, central management and lock files. | Compare effective restore graph, .nuspec/package metadata and clean consumers; isolate upgrades from format migration. |
| **5. Code style, analyzers and C#** | Review .editorconfig, warnings, analyzer enforcement, language versions and nullable adoption. | Test the compiler/analyzer toolchain, CI checks and compatibility; C# upgrades need not wait for SDK conversion. |
| **6. SDK-style project conversion** | Compare conversion tools, project formats, source/resource globs, assembly metadata and generated files. | Retain existing framework/language initially where useful; compare compiled output, API/resource/package contracts. |
| **7. Runtime and platform migration** | Evaluate supported .NET targets, API compatibility, Windows-specific behavior and multitargeting needs. | Run representative compatibility, integration, serialization and consumer tests on the target platforms. |
| **8. Testing and verification** | Inspect all local/CI test assemblies, test frameworks, fixtures, test determinism and coverage gaps. | Track discover/pass/fail/skip; running every suite does not establish complete code coverage. |
| **9. CI/CD and releases** | Assess build/test/audit gates, caching, artifact provenance, publishing, signing and rollback. | Verify each step, not only workflow status; preserve package and release contracts, keep publish authorization separate. |
| **10. Architecture and modularity** | Identify coupling, layering, legacy dependencies, integration boundaries and incremental refactoring opportunities. | Preserve behavior and interface contracts; prefer focused, reversible changes over simultaneous rewrites. |
| **11. Security and supply chain** | Review unsupported/vulnerable dependencies, auth, secrets, transports, input handling and CI permissions. | Use threat-informed checks and scanners; assess remediation separately from unrelated format changes. |
| **12. Performance and efficiency** | Identify measured execution, memory, I/O, concurrency, build or test bottlenecks. | Use repeatable workload benchmarks; compare correctness, resources and cost before/after. |
| **13. Deployment and hosting** | Examine IIS, services, containers, cloud assumptions, configuration and portability. | Test host/runtime compatibility, deployment and rollback; mark not applicable to libraries where appropriate. |
| **14. Observability and reliability** | Review logging, tracing, metrics, health checks, failure handling and runbooks. | Verify useful signals without exposing sensitive data; tailor scope to application type. |
| **15. Developer workflows** | Evaluate onboarding, local verification, tool discovery, scripts and duplicated automation. | Reproduce on clean environments; avoid wrapper files without demonstrated benefits. |
| **16. Data and external contracts** | Inspect persistence schemas, serialization, interop, protocols and external service consumers. | Use representative data, schema/contract tests, migration and rollback checks when applicable. |

## Decision discipline

1. **Scope first.** Summarize relevant areas, explicit exclusions and deferred work; a pre-SDK assessment need not complete runtime, architecture or deployment research.
2. **Rank value, not novelty.** Compare benefit, risk, effort, compatibility impact, dependencies, reversibility, and independent implementability.
3. **Experiment independently.** Record actual commands, environment, success and failure, negative controls where useful, and unexecuted gates. Do not equate a green workflow with a passed experiment.
4. **Preserve boundaries.** Findings are not approved decisions; successful experiments are not implemented changes. Application changes belong in the application's own repository.
5. **Keep records lean.** Use the [evaluation overview template](../templates/evaluation-overview.md); create dedicated experiments, research notes or GitHub issues only when justified. Historical evaluations retain their baseline SHA and scope.

## First application example

The [RecordSift November 2026 pre-SDK evaluation](../projects/recordsift/evaluations/2026-11-pre-sdk/README.md) deliberately covers only a subset of these areas. Its [roadmap](../projects/recordsift/evaluations/2026-11-pre-sdk/roadmap.md) reconciles the prior **34 application-specific investigation candidates across six workstreams** with verified evidence, open work and future evaluation boundaries. Those 34 candidates are **not** mandatory catalog steps for other applications.
