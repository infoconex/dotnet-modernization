# RecordSift November 2026 evidence manifest

**Application:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Canonical unchanged main SHA:** `8358780829458854a4b0356df5ac5e685f0a34c8`

## Workflow evidence

| Purpose | GitHub Actions run | Outcome | Artifact / notes |
|---|---|---|---|
| Windows baseline build and five NUnit suites | [41392848910](https://github.com/infoconex/RecordSift/actions/runs/41392848910) | Passed | 419/418/0/1; 425 API/metadata entries |
| Clean package consumers | [41392848814](https://github.com/infoconex/RecordSift/actions/runs/41392848814) | Passed | Main's existing workflow |
| Documentation | [41392848879](https://github.com/infoconex/RecordSift/actions/runs/41392848879) | Passed | Main's existing workflow |
| First import/API-host probe | [41483895096](https://github.com/infoconex/RecordSift/actions/runs/41483895096) | Failed | PowerShell 7 reflection differences, corrected later |
| Import and early Common.props probe | [41484290488](https://github.com/infoconex/RecordSift/actions/runs/41484290488) | Mixed | Directory.Build props/targets work; forced early import caused MSB3107 |
| Windows container feasibility | [41484601947](https://github.com/infoconex/RecordSift/actions/runs/41484601947) | Passed | Cached historical Framework SDK image |
| Full property-centralization parity | [41484769924](https://github.com/infoconex/RecordSift/actions/runs/41484769924) | Passed | **Artifact 13160583419** |
| Framework SDK container full build/NUnit | [41484891489](https://github.com/infoconex/RecordSift/actions/runs/41484891489) | Passed | 419/418/0/1; Build Tools installed |
| SDK-only container (no Build Tools) | [41486238239](https://github.com/infoconex/RecordSift/actions/runs/41486238239) | Passed | **Artifact 13162920363**, 419/418/0/1 |
| First SDK selection negative control | [41486570113](https://github.com/infoconex/RecordSift/actions/runs/41486570113) | Workflow failed | Missing SDK correctly detected, but negative control was not handled |
| Corrected SDK selection and override controls | [41486700576](https://github.com/infoconex/RecordSift/actions/runs/41486700576) | Passed | Fixed 10.0.403; latestFeature 10.0.403; override 7.2 |
| SDK-only full release-gates probe | [41575562993](https://github.com/infoconex/RecordSift/actions/runs/41575562993) | Partial; XML and API passed, package/consumer failed on ZipFile type | **Artifact 13203417992**; workflow SHA `7340c3409a755060cea33265cbcf129d4778832d`; [EXP-007](../experiments/EXP-007-sdk-only-release-gates.md) |
| SDK-only assembly-loading control | [41576091787](https://github.com/infoconex/RecordSift/actions/runs/41576091787) | Inconclusive for package: harness incorrectly quoted PowerShell parameter | **Artifact 13202929618**; workflow SHA `5775fb98c7d30866ae24d0aaee721548bc71c591` |
| Corrected SDK-only assembly-loading control | [41576608287](https://github.com/infoconex/RecordSift/actions/runs/41576608287) | Attempt 1 blocked by runner Docker daemon; attempt 2 executed: 419 tests, XML and API pass; NuGet pack/install succeeded, existing validators failed on notice text comparison and missing extracted XML. Partial outcome; no clean consumer execution | **Artifact 13204365812**, workflow SHA `7df8be3374e292c6957ab22dcd9966dc30138b19`, [EXP-007](../experiments/EXP-007-sdk-only-release-gates.md) |

| SDK-only EXP-009 first follow-up | [41707695201](https://github.com/infoconex/RecordSift/actions/runs/41707695201) | Partial: 419/418/0/1, XML/API passed; Windows PowerShell default vs explicit UTF-8 mismatch confirmed; new ZIP probe hit missing assembly load | **Artifact 13266705727**; workflow `abfce77d277c0854d478152808a2591801afbc08`; [EXP-009](../experiments/EXP-009-sdk-only-release-validation.md) |
| SDK-only EXP-009 corrected compression probe | [41707884452](https://github.com/infoconex/RecordSift/actions/runs/41707884452) | ZIP text equals explicit UTF-8; next script-copy control blocked by .NET/PowerShell working-directory mismatch in harness | **Artifact 13267920768**; workflow `290634e3d5ef12cc870af5ea4fa2761eba3c9032`; [EXP-009](../experiments/EXP-009-sdk-only-release-validation.md) |
| **SDK-only EXP-009 final positive validation** | **[41708730067](https://github.com/infoconex/RecordSift/actions/runs/41708730067)** | **PASS corrected path:** build, all 419 tests (418/0/1), positive XML, 425 APIs, unpublished NuGet packaging validation with explicit UTF-8, clean NuGet install, both independent C# 7.3/net48 consumers compiled/executed with SDK Roslyn, all four Getting Started samples. **Original scripts still fail:** default notice decoding, `NUGET_XMLDOC_MODE=skip` extraction and VS `vswhere`; optional CS1591 negative not run. | **Artifact 13268111524**; workflow SHA `3cea8e844d5dbb77c10d3908687eae8590899abf`; [EXP-009](../experiments/EXP-009-sdk-only-release-validation.md) |

## Container identities

**Framework SDK container:** historical, cached tag `mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2022`; immutable digest `sha256:460dedaed73224f73ff10dc3ad754d0ed250aa57bcdf6c5052a811b4b7e29345`. Visual Studio Build Tools included; not a currently supported tag for new instructions.

**SDK-only container:** `mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022`; immutable digest `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25`. .NET SDK 10.0.403, SDK MSBuild 18.9.15.52412, no VS Build Tools, NuGet 6.14.0.116 and net48 ref-pack 1.0.3 added during experiment. Windows Server Core 2022 and compatible Windows container host.

**Artifact limitation:** Run links and artifact IDs are locators, not permanent preservation guarantees. Core evidence is summarized in checked-in experiment notes and the original [discovery report](../discovery-report.md).

## Experimental repository branches (not main)

- `discovery/pre-sdk-20261102` — import/property/validation workflows.
- `discovery/pre-sdk-container-20261102` — Framework SDK container workflows.
- `discovery/sdk-only-20261102` — SDK-only container proof.
- `discovery/props-sdk-selection-20261102` — SDK selection and property override controls.
- `discovery/sdk-only-release-gates-20261102` — EXP-007 compatibility-gate controls; not merged.
- `research/sdk-only-release-followup-20261103` — EXP-009 follow-up workflow from untouched main SHA; not merged.

Branches may be deleted after evidence is durably archived. No application pull request was merged and no application release/publishing action occurred.
