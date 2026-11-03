# Evaluation progress and verification status

**As assessed:** November 2, 2026  
**Baseline application SHA:** `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Overall:** discovery substantially complete; no implementation authorized or performed in application main.

**Work state** means an activity was attempted/completed. **Evidence outcome** states what it proved; these are different.

| Activity | Work state | Evidence outcome | Evidence / follow-up |
|---|---|---|---|
| Inventory ten traditional projects and build infrastructure | Complete | Verified | [Baseline](baseline.md) |
| Establish Windows CI restore/build/NUnit/API/package baseline | Complete | Verified | [Baseline run](https://github.com/infoconex/RecordSift/actions/runs/41392848910) |
| Verify independent clean consumer checks | Complete | Verified on existing CI | [Consumer run](https://github.com/infoconex/RecordSift/actions/runs/41392848814) |
| Verify shared Directory.Build.props without changed imports | Complete | Verified | [Experimental run](https://github.com/infoconex/RecordSift/actions/runs/41484769924) |
| Evaluate Directory.Build.targets and early import risks | Complete | Verified mechanism; early import experiment failed | [Import run](https://github.com/infoconex/RecordSift/actions/runs/41484290488) |
| Containerize full build/tests with .NET Framework SDK | Complete | Verified; Build Tools present | [Container run](https://github.com/infoconex/RecordSift/actions/runs/41484891489) |
| Build all ten traditional projects without VS Build Tools | Complete | Verified | [SDK-only run](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| Execute all five NUnit suites without VS Build Tools | Complete | Verified: 419/418/0/1 | [SDK-only run](https://github.com/infoconex/RecordSift/actions/runs/41486238239) |
| Verify global.json version selection and overrides | Complete | Verified selection and missing-SDK negative control | [Follow-up run](https://github.com/infoconex/RecordSift/actions/runs/41486700576) |
| Confirm conditional Directory.Build.props override semantics | Complete | Verified: project override retained when shared default conditional | [Follow-up run](https://github.com/infoconex/RecordSift/actions/runs/41486700576) |
| Run *full* packaging/API/consumer gates inside SDK-only container | Complete | Partially verified: build/419 tests/XML/425 APIs, NuGet pack/install passed; validation scripts failed on notice decoding and XML extraction; standalone consumer not executed | [EXP-007](experiments/EXP-007-sdk-only-release-gates.md), [issue #2](https://github.com/infoconex/dotnet-modernization/issues/2) |
| Test isolated PackageReference conversion while retaining traditional .NET Framework 4.8 (EXP-012) | **Complete, verified for full exact-pins candidate** | 7 projects/17 exact refs; restore/build, 419/418/0/1 NUnit, five XML, compiled API/identity **414/414**, package/consumer, CS1591 negative passed. Unchanged 425-line checker fails due to 11 `packages.config` source-only metadata records; original test runner needs external install. No product implementation. | [EXP-012](experiments/EXP-012-packagereference-isolation.md), [run 41734675914](https://github.com/infoconex/RecordSift/actions/runs/41734675914), [issue #13](https://github.com/infoconex/dotnet-modernization/issues/13) |
| Test pinned SDK with actual formatter validation | Not started | Not executed | `dotnet format style` compatibility and CI SDK provisioning |
| Execute current supported framework SDK 4.8.1 container | Not started | Not executed | Tag manifest exists; no runtime test yet |
| Implement any modernization changes in application repository | Not started | Not applicable | Out of this discovery scope |

**Next research decision:** SDK-only release-gate experiment [EXP-007](experiments/EXP-007-sdk-only-release-gates.md) is complete with a partial outcome. Any permanent validation-script portability changes require separate RecordSift implementation authorization. Independent methodology assessment is **concluded with an explicit evidence exception under P-011**: several repository-grounded candidate responses demonstrated substantive capability, but no complete same-session response and tool trace establishes a formal strict pass. No more retests are requested for this pilot.

**First proposed implementation after approval:** repair local test-script parity and establish a reproducible all-five-suite command; then introduce minimal common shared properties and rerun compatibility gates.

## Methodology-validation pilot (approved November 2, 2026)

| Activity | Work state | Evidence outcome / follow-up |
|---|---|---|
| Adaptive stakeholder interview and explicit scope authorization | Complete | P-001–P-010 recorded in [decisions](decisions.md); approved [scope](README.md) |
| Central methodology process / intake / approval / GitHub rules | Documentation updated on PR #1 | Ready for final PR review with P-011 independent-evidence exception; [process](../../../../methodology/evaluation-process.md) |
| Lightweight agent entry points and authorization-aware template | Documentation updated on PR #1 | [root AGENTS](../../../../AGENTS.md), [Copilot](../../../../.github/copilot-instructions.md), [evaluation template](../../../../templates/evaluation-overview.md) |
| Targeted SDK-only release-gate investigation | Complete — partially verified | [issue #2](https://github.com/infoconex/dotnet-modernization/issues/2), [EXP-007](experiments/EXP-007-sdk-only-release-gates.md) |
| Independent fresh-context acceptance | **Concluded — accepted evidence limitation (P-011)** | Multiple candidate assessments recovered methodology and evidence accurately; isolation/reading evidence was not fully retained **in the same session**, so strict AC-01–AC-09 acceptance cannot be called passed. Stakeholder directed an end to retests; [issue #3](https://github.com/infoconex/dotnet-modernization/issues/3) documents closure by exception. No implementation/merge authorization. |

**Process observation:** Before this pilot, the evaluation lifecycle began with intake but did not instruct an unfamiliar assistant to inspect before interviewing, obtain explicit consolidated approval, or preserve authorization for session handoff. Centralized the new rules in the existing lifecycle rather than duplicating them in AI entry points. Original RecordSift discovery documents remain historical evidence; do not mandate every specialized file for future applications.

**Avoided unnecessary files:** No separate `methodology/start-evaluation.md` was added; the root README, `AGENTS.md` and lightweight Copilot entry point all route to the same authoritative lifecycle. An investigation issue template is deferred until repeated issue creation demonstrates a genuine need; focused issues #2 and #3 already exercise the current conventions without duplicating a process across YAML and Markdown. Specialized status/findings/risks/roadmap documents are retained for this historically extensive evaluation, **not** mandated as empty placeholders for every new application.

**GitHub tracking limitation:** This connection can create issues and edit documentation, but does not expose a GitHub milestone-creation/attachment operation. Issues #2 and #3 are linked to the approved evaluation without a created milestone; do not represent a milestone as created.
