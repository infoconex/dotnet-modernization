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

| SDK-only full release-gates probe | [41575562993](https://github.com/infoconex/RecordSift/actions/runs/41575562993) | Pending execution results | Experimental workflow commit `7340c3409a755060cea33265cbcf129d4778832d`, [EXP-007](../experiments/EXP-007-sdk-only-release-gates.md) |

## Container identities

**Framework SDK container:** historical, cached tag `mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2022`; immutable digest `sha256:460dedaed73224f73ff10dc3ad754d0ed250aa57bcdf6c5052a811b4b7e29345`. Visual Studio Build Tools included; not a currently supported tag for new instructions.

**SDK-only container:** `mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022`; immutable digest `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25`. .NET SDK 10.0.403, SDK MSBuild 18.9.15.52412, no VS Build Tools, NuGet 6.14.0.116 and net48 ref-pack 1.0.3 added during experiment. Windows Server Core 2022 and compatible Windows container host.

**Artifact limitation:** Run links and artifact IDs are locators, not permanent preservation guarantees. Core evidence is summarized in checked-in experiment notes and the original [discovery report](../discovery-report.md).

## Experimental repository branches (not main)

- `discovery/pre-sdk-20261102` — import/property/validation workflows.
- `discovery/pre-sdk-container-20261102` — Framework SDK container workflows.
- `discovery/sdk-only-20261102` — SDK-only container proof.
- `discovery/props-sdk-selection-20261102` — SDK selection and property override controls.

Branches may be deleted after evidence is durably archived. No application pull request was merged and no application release/publishing action occurred.
