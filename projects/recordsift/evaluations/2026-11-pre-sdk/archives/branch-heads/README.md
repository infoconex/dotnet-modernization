# RecordSift temporary discovery branch-head workflows (2026-11-11)

These four YAML files are **source archives**, copied verbatim from the named RecordSift branch heads. They are stored outside `.github/workflows/` to prevent accidental execution. Do not interpret them as generalized, current, or automatically reproducible workflows.

| RecordSift branch | Head commit | Archived file | Original Git blob SHA |
|---|---|---|---|
| [`discovery/pre-sdk-20261102`](https://github.com/infoconex/RecordSift/tree/0708839ada521c0ee606c70541201a8b28ed6a25) | `0708839ada521c0ee606c70541201a8b28ed6a25` | [`EXP-001-pre-sdk-discovery-branch-head.yml`](EXP-001-pre-sdk-discovery-branch-head.yml) | `394f9fe885fa00ae0ae676edcfc4cea4f8b55877` |
| [`discovery/pre-sdk-container-20261102`](https://github.com/infoconex/RecordSift/tree/ea443d3e61de7ac8bc60d33e5d5c6abfb20f229c) | `ea443d3e61de7ac8bc60d33e5d5c6abfb20f229c` | [`EXP-003-container-feasibility-branch-head.yml`](EXP-003-container-feasibility-branch-head.yml) | `a87c46fb52eb369ea967afb7e0ca49d7849b57dc` |
| [`discovery/props-sdk-selection-20261102`](https://github.com/infoconex/RecordSift/tree/c0abeb9e9533bf6b85d419a5c8d6a63a4fca4900) | `c0abeb9e9533bf6b85d419a5c8d6a63a4fca4900` | [`EXP-005-sdk-selection-branch-head.yml`](EXP-005-sdk-selection-branch-head.yml) | `45f329cfc06ca694d032156e23cdc5743c2d0fcd` |
| [`discovery/sdk-only-release-gates-20261102`](https://github.com/infoconex/RecordSift/tree/7df8be3374e292c6957ab22dcd9966dc30138b19) | `7df8be3374e292c6957ab22dcd9966dc30138b19` | [`EXP-007-sdk-only-release-gates-branch-head.yml`](EXP-007-sdk-only-release-gates-branch-head.yml) | `d5995eec1b18e688e96b77355fc109fc7dd0aa12` |

## Evidence and limits

- The [evidence manifest](../../evidence/manifest.md) and [experiment index](../../experiments/README.md) retain outcomes, workflow runs, failures and qualifications. These archived sources alone are not proof that all checks passed.
- The existing [historical workflow archive](../README.md) contains additional snapshots, including an earlier EXP-007 revision. Preserve both versions: the branch-head archive is **not** a replacement for the earlier original.
- Source contents were fetched from GitHub by branch and their original blob SHA recorded above. Do not claim a newly executed test or long-term GitHub Actions artifact retention.
- Original branch heads and original commit history remain separately addressable by immutable commit SHA as long as GitHub retains the objects. This archive safeguards the four workflow source files independently of branch deletion, not all branch commit metadata.
- No RecordSift application, build, CI, release, or production configuration files were changed during archival.
