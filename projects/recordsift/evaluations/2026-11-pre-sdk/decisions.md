# Proposed modernization decisions — not implementation authorization

This document keeps **options and recommendations** distinct from decisions already approved for application changes. All entries below are proposals arising from discovery; none should be interpreted as a merged application change.

| ID | Proposed choice | Disposition | Reason / verification |
|---|---|---|---|
| D-001 | Correct the local test runner to include all five NUnit assemblies. | Recommend first | Close a proven safety gap; rerun 419 tests and CI. |
| D-002 | Add minimal root Directory.Build.props with shared LangVersion=7.3 and conditional default where overrides must remain possible. | Recommend after baseline | Isolated POC passed build/tests/API/package checks; no early import required. |
| D-003 | Do **not** add a synthetic Directory.Build.targets. | Not recommended currently | Imports work but no meaningful behavior has been identified to centralize. |
| D-004 | Preserve TargetFrameworkVersion in project files until raw-XML public-API verifier assumptions are removed. | Defer | Avoid false compatibility failures. |
| D-005 | Evaluate a documented SDK-only Windows developer build path. | Optional, proven feasible | Tool independence is real for compilation and NUnit; full release-gate support still unverified. |
| D-006 | Do not convert packages.config to PackageReference or add Directory.Packages.props in pre-SDK discovery. | Defer to SDK migration | Separate dependency and packaging compatibility changes from baseline-preserving configuration work. |
| D-007 | Add global.json only if formatter/CI consistency benefits outweigh SDK provisioning burden. | Optional pending verification | Selection works; actual formatter behavior under a pin remains untested. |
| D-008 | Do not modify MSBuild import ordering just to use shared properties. | Reject based on experiment | Early Common.props import produced MSB3107; minimal props centralization passed without it. |

Decision state should change to **approved** only after explicit authorization, with an issue/PR, responsible owner, date, and evidence links.
