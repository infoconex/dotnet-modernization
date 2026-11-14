# Evaluation methodology

A reusable process for assessing .NET applications regardless of whether the proposed modernization concerns project format, dependencies, toolchains, infrastructure, or the runtime.

- [Evaluation process and first-contact protocol](evaluation-process.md#start-here-first-contact-protocol) — inspect, interview, approve scope, investigate, track and complete. **Authoritative** for AI and human workflow rules.
- [Native-first technical discovery runbook](technical-discovery-runbook.md) — manual Git/.NET/MSBuild/NuGet inspection and verification, step IDs, applicability, and evidence capture.
- [Evidence standards](evidence-standards.md) — reproduction metadata, test gates, and outcome terminology.
- [Reusable validation tools](../tooling/validators/README.md) — source inventory, observed toolchains, evaluated MSBuild property matrices, existing NuGet restore graphs and per-gate machine-readable evidence.
- [Baseline variation and applicability guide](baseline-variation-guide.md) — field-by-field alternatives to check before completing a factual baseline.
- [Investigation catalog](investigation-catalog.md) — screen modernization areas for relevance before choosing experiments or changes.
- [Repository configuration and tooling](repository-configuration.md) — how to assess applicable .NET central files without prescribing unnecessary ones.
- [Evaluation overview template](../templates/evaluation-overview.md).
- [Experiment template](../templates/experiment.md).

Avoid treating any RecordSift-specific tool version or conclusion as automatically applicable to another application.

## Organization boundary

Keep reusable evaluation *instructions* here. Put an application's measurements, baselines, and decisions under [`projects/`](../projects/README.md); cross-application technical investigations, evidence, and reviews under [`research/`](../research/README.md). A proposed technical acceptance mechanism is not automatically an approved methodology or production gate.

The [PR review-board governance policy](pr-review-board-governance.md) remains a scoped operating policy for this repository and the RecordSift pilot, not a universal recommendation for other organizations.
