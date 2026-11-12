# Archived RecordSift validation workflows — November 2026

**Classification:** Historical, source-preserved, **not generalized or re-executed from this archive**.  
**Application:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Frozen baseline:** `main@8358780829458854a4b0356df5ac5e685f0a34c8`  
**Original result source:** [EXP-001–013](../experiments/README.md) and [evidence manifest](../evidence/manifest.md)

Each YAML file below is a **byte-for-byte preserved UTF-8 file** copied from an immutable original RecordSift workflow commit. The Git blob SHA of each archive was compared with its original immediately after creation. Do **not** edit these historical snapshots; create a distinct reusable implementation with separate tests rather than rewriting original evidence.

| Experiment | Archived workflow | Original workflow at immutable application commit | Original blob SHA | Scope / evidence caveat |
|---|---|---|---|---|
| EXP-004 | [SDK-only traditional build](EXP-004-pre-sdk-sdk-only.yml) | [Original](https://github.com/infoconex/RecordSift/blob/231ae63f8a0435dbc8a1b7a5a4319d4ec8bd0825/.github/workflows/pre-sdk-sdk-only.yml) | `26007bb33a3007cc8739d9c74072182ed5ef8f7e` | Windows SDK-only image/build/test feasibility; VS Build Tools absent; [run 41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239). |
| EXP-007 | [Original SDK-only release-gate probe](EXP-007-pre-sdk-sdk-only-release-gates.yml) | [Original](https://github.com/infoconex/RecordSift/blob/7340c3409a755060cea33265cbcf129d4778832d/.github/workflows/pre-sdk-sdk-only-release-gates.yml) | `c347e87546d9e1286c7c77afd235e00630a2cd6a` | **Partial/negative historical probe**; later attempts used other commits. This is **not** the corrected positive EXP-009 and does not prove unmodified scripts pass. |
| EXP-008 | [Pinned/unpinned SDK and formatter](EXP-008-research-globaljson-sdk.yml) | [Original](https://github.com/infoconex/RecordSift/blob/0c8cc3d775ccff0534d697e5e3cfe2a5fe80ef13/.github/workflows/research-globaljson-sdk.yml) | `c3b0af3d777e0f0cb1b29320f250e05e42724646` | Exact SDK 10.0.303/10.0.403, IDE1006, Release build, NUnit, XML and API; package/consumer parity under both pins not checked. |
| EXP-009 | [Corrected SDK-only package/consumer probes](EXP-009-research-exp009-sdk-only-release.yml) | [Original](https://github.com/infoconex/RecordSift/blob/3cea8e844d5dbb77c10d3908687eae8590899abf/.github/workflows/research-exp009-sdk-only-release.yml) | `c3115aab72f28c160118012f45d7c85e925be04b` | Temporarily adapted scripts verified positive packaging and clean consumers; original untouched scripts still fail and SDK-only negative CS1591 not executed. |
| EXP-010 | [Scoped WarningLevel control](EXP-010-research-exp010-warninglevel.yml) | [Original](https://github.com/infoconex/RecordSift/blob/fd44c1b7bd89c7718117222f5276fbeef0e649af/.github/workflows/research-exp010-warninglevel.yml) | `ff355fb5dd6c9347954d9c7180f771847edfa8d3` | Conditional property propagation and override with full scoped gates; Custom property evaluated, arbitrary Custom build not tested. |
| EXP-011 | [NuGet inventory and restored HintPaths](EXP-011-research-exp011-nuget-graph.yml) | [Original](https://github.com/infoconex/RecordSift/blob/a94381f97843d692265e805aeb899e616c60a7bb/.github/workflows/research-exp011-nuget-graph.yml) | `2bb9a7042a592981bb4c0e9869d310956e30a0af` | 17 declared packages, 13 restored package IDs, 13 real DLL paths and 11 distributable dependencies; historical direct/transitive origin not proved. |
| EXP-012 | [Exact-pinned PackageReference candidate](EXP-012-research-exp012-packagereference.yml) | [Original](https://github.com/infoconex/RecordSift/blob/63eaad20986cdf429fd64f248a5c2a3f9223f857/.github/workflows/research-exp012-packagereference.yml) | `ae04eb501fb18ace7633efa45a4abb5a6d1f6ae8` | Temporary conversion; 414 compiled API/identity pass, original 425-entry raw-metadata gate fails; direct-only candidate downgrades four versions, not consumer-validated. |
| EXP-013 | [Migration CI and architecture controls](EXP-013-research-exp013-migration-ci.yml) | [Original](https://github.com/infoconex/RecordSift/blob/933c74ec916468ce1e4a5c0c0878ca56a360bc36/.github/workflows/research-exp013-migration-ci.yml) | `e4e3dd796d4c437148c05d5923953c3f660eb556` | Format-aware dependency audit/architecture positive and negative controls in disposable workspaces; Visual Studio GUI migrator not executed. |

## Related scripts already versioned in RecordSift

The workflows call application-specific scripts already preserved in the immutable original repository. They are **linked, not duplicated** here:

- [Public API verification](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/verify_public_api.ps1) — mixes compiled API and raw project/package metadata; 425-entry historical baseline.
- [XML documentation verification](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/verify_xml_documentation.ps1).
- [Unpublished release-candidate package](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/build_release_candidate.ps1).
- [Clean package consumer](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/verify_clean_consumer.ps1).
- [Architecture dependency guard](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/validate_architecture_layers.py) — original source format assumes certain raw references; the EXP-013 adaptation was ephemeral.
- [Local test runner](https://github.com/infoconex/RecordSift/blob/8358780829458854a4b0356df5ac5e685f0a34c8/scripts/run_tests.ps1) — **runs four suites only on frozen main**; the five-suite fix exists solely on `release/0.2`.

EXP-001–003 and EXP-005–006 also have recorded experiment commands and evidence but are **not claimed as captured by these eight selected full workflow archives**. Their research reports and the linked historical repository commits remain the provenance for those activities.

## Reproduction limitations

- Workflow trigger branch names, source-integrity guards, test counts, solution paths and tool versions are **RecordSift-specific**.
- GitHub-hosted runner images, registry feeds, container tags, restored packages and available tools can change. The archived files' contents are immutable, but their **environment is not**; compare current behavior against dated reports rather than claiming exact replays.
- Artifacts may have expired. Logs, artifact IDs and observed outcomes are recorded in the dated experiment/evidence files.
- These workflows perform **writes in temporary checkouts** during isolation and may contain intentional failing controls. They do not grant permission to change application source branches or release pipelines.
- Place archived source outside `.github/workflows/` until a *separately authorized* isolated reproduction. Read the [tooling guide](../../../../../tooling/README.md) for a safe adaptation procedure and the plan for reusable validators.

**Archival acceptance:** The eight archived Git blob IDs above are identical to the linked source workflow blobs. **Execution acceptance:** Not performed for these archival copies; no claim of current-run compatibility.
