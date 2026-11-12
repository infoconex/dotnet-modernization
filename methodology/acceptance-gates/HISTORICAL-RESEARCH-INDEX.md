# Historical research consolidation — RecordSift (November 2026)

> **Historical evidence archive, not a production approval or a current modernization readiness assessment.** The documents below preserve claims and links from draft research. They have not been rerun or independently reproduced by this consolidation.

## Scope and provenance

- EXP-016 source-level API regression: [original draft PR #28](https://github.com/infoconex/dotnet-modernization/pull/28).
- EXP-017 NuGet package payload byte comparison: [original draft PR #30](https://github.com/infoconex/dotnet-modernization/pull/30).
- EXP-018–043: historical stacked research, starting at [PR #32](https://github.com/infoconex/dotnet-modernization/pull/32), culminating in [EXP-043 PR #71](https://github.com/infoconex/dotnet-modernization/pull/71). See the [experiment directory](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/README.md) for original context.
- Alternate EXP-029 and EXP-031 investigations: [PR #45](https://github.com/infoconex/dotnet-modernization/pull/45) and [PR #48](https://github.com/infoconex/dotnet-modernization/pull/48); retained as distinct reports, not silently conflated with the later approaches.
- Gate C-N research design, synthetic controls, Windows compiler tests, local NuGet tests, and AI-assisted handoff: [PR #74](https://github.com/infoconex/dotnet-modernization/pull/74), [#81](https://github.com/infoconex/dotnet-modernization/pull/81), [#82](https://github.com/infoconex/dotnet-modernization/pull/82), [#83](https://github.com/infoconex/dotnet-modernization/pull/83), [#84](https://github.com/infoconex/dotnet-modernization/pull/84).

## Evidence classification

**Reported verified** means an original experiment report cites a particular execution and controls. It does **not** mean the present archive reran it. **Qualified** means the report records important environmental, witness, or scope limitations. **Not verified** includes proposals, simulated review perspectives, and any claim not established by a primary execution artifact. Consult individual reports for exact hashes, run links, controls and limits.

The Gate C-N handoff explicitly states that simulated reviewer roles are not independent human signoffs and that release remains blocked. This consolidation makes no release, Source Link enablement, package publication, or application-change decision.

## Excluded executable material and link caveat

This PR intentionally does **not** import historical GitHub Actions workflows or experimental tooling into active repository locations. Some preserved reports therefore contain **relative links to scripts, validators, and workflows that do not exist on this branch**. Their original source remains accessible in the historical PR commit trees; for example [EXP-016 source](https://github.com/infoconex/dotnet-modernization/tree/research/exp016-source-api-regression-20261104), [EXP-017 source](https://github.com/infoconex/dotnet-modernization/tree/research/exp017-package-payload-bytes-20261104), and [Gate C-N source](https://github.com/infoconex/dotnet-modernization/tree/research/gate-cn-post-d2b-human-review-handoff-20261106). **Do not delete those original branches until executable source provenance is archived by immutable commit SHA or the links are repaired.**

## Before merge / branch retirement

1. Audit and repair broken relative links, or preserve referenced tooling in a clearly labeled inert archive.
2. Validate JSON content, provenance, and whether any evidence requires redaction.
3. Reconcile original draft PRs and preserve final source commit SHAs in a branch-retirement register.
4. Separately decide whether reusable validators deserve maintained tooling with tests and CI; archival is not adoption.

No original draft PR should be closed merely because this index exists.
