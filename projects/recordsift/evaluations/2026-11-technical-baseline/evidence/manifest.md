# RecordSift technical discovery — Evidence manifest

**Evaluation:** [November 2026 native-first technical baseline](../README.md)  
**Frozen source commit:** `1809d06c0fade59e4769d16e0f8eaf10fa426004`  
**Status:** **Source inspection only**, not local command evidence. No native SDK, MSBuild, NuGet, Git or test command has been manually executed or captured in this new evaluation.

| Evidence ID | Discovery context | Source / trace | Method and provenance | What it establishes / limitations |
|---|---|---|---|---|
| EV-001 | DISC-001 preflight | [Immutable application commit](https://github.com/infoconex/RecordSift/commit/1809d06c0fade59e4769d16e0f8eaf10fa426004) | Source metadata inspected via connected GitHub on 2026-11-12 | Identifies the repository revision selected for this walkthrough. **Does not** establish operator local HEAD, working-tree state, or toolchain. |
| EV-002 | DISC-002, DISC-006, DISC-011 preflight | [Tracked tree at frozen SHA](https://github.com/infoconex/RecordSift/tree/1809d06c0fade59e4769d16e0f8eaf10fa426004) | GitHub tree source-inspected on 2026-11-12 | Records observed solution, project, repository configuration and workflow *paths*. Does not prove effective imports, solution membership, or commands executed. |
| EV-003 | Application identity context | [README at frozen SHA](https://github.com/infoconex/RecordSift/blob/1809d06c0fade59e4769d16e0f8eaf10fa426004/README.md) | Source-inspected product documentation | Documents the application's own Windows/.NET Framework 4.8 description; not independently verified project evaluation or runtime execution. |

## Rules for new evidence

- Link each new artifact/output to `DISC-NNN` and the complete source SHA. For executed operations, capture command, tool version, host/environment, timestamp, **exit code**, output/result and retained artifact location.
- Keep **actual raw output** or a durable faithful excerpt separately from any generated report. Give exact GitHub Actions run/artifact IDs and note expiry; commit small redacted text where useful.
- Use source-inspected, tool-evaluated and executed classifications separately; preserve historical provenance. An earlier evaluation run is not new evidence for this SHA unless its exact scope is verified.
- Do not commit credentials, secret-bearing configuration, generated packages, restored dependencies or large binaries. Report missing/blocked/unexecuted checks explicitly.
- Add links to actual artifacts only when they exist. No placeholder file trees or invented screenshots/logs.
