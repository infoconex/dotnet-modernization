# Application evaluations

Organize by **application**, then by **dated, independently reproducible evaluation**. An application may have many evaluations as its baseline evolves.

## Current applications

| Application | Evaluation | Phase | Next action |
|---|---|---|---|
| [RecordSift](recordsift/README.md) | [November 2026 pre-SDK discovery and methodology pilot](recordsift/evaluations/2026-11-pre-sdk/README.md) | Original technical discovery substantially complete; approved methodology pilot active | [SDK-only release-gate issue #2](https://github.com/infoconex/dotnet-modernization/issues/2); [independent acceptance #3](https://github.com/infoconex/dotnet-modernization/issues/3). |
| [RecordSift](recordsift/README.md) | [November 2026 native-first technical baseline walkthrough](recordsift/evaluations/2026-11-technical-baseline/README.md) | Draft/source preflight only; local execution not begun | Owner runs [DISC-001](../methodology/technical-discovery-runbook.md#disc-001--check-tools-and-get-a-clean-copy-of-the-source) and shares outputs for evidence capture. |

## Naming conventions

Use lower-case application directories and evaluation directories in the form YYYY-MM-short-purpose. Each evaluation records a frozen application baseline SHA. Do not overwrite an older result when the application advances; create a new evaluation or explicitly document a follow-up at a new SHA.

Create directories only when documents exist; avoid placeholder files for future evaluations.
