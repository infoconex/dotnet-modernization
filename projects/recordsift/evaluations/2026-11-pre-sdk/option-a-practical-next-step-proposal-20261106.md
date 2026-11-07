# RecordSift Option A — practical modernization restart and first change proposal

**Prepared:** November 6, 2026 Pacific. **State:** DOCUMENTATION / PROPOSED APPLICATION CHANGE ONLY; no implementation permission. **Stakeholder decision:** [issue #85](https://github.com/infoconex/dotnet-modernization/issues/85) records the user's explicit **YES** to Option A — preserve bounded Gate C-N research and return to the practical modernization roadmap.

## 1. Executive decision, without specialized compiler knowledge

**Objective:** improve the safety, repeatability and maintainability of the existing RecordSift .NET Framework 4.8 solution before any project-format/runtime migration. The practical test of success is **same externally observable library behavior, APIs, dependencies and consumer installation after each small, reviewable change**.

**Decision already made:** stop new speculative Gate C-N/native-PDB experiments by default and do not build it into a production release gate. Retain all prior evidence and unmerged research drafts. Original managed Gate C **UNSATISFIED**, native Gate C-N production **NOT_AUTHORIZED**, Source Link production **HOLD**. These are unchanged disposition statements for that specialized research; they are **not** an instruction to block ordinary independently approved modernization preparation forever.

**Decision not made:** nothing in Option A authorizes touching RecordSift branches, committing candidate code, merging pull requests, changing release policy, publishing NuGet packages, or weakening the current release acceptance contract. The *next* application change is a separate stakeholder decision.

## 2. Fresh exact GitHub state, independently inspected

| Object | Verified state | Consequence |
| --- | --- | --- |
| [RecordSift main](https://github.com/infoconex/RecordSift/tree/8358780829458854a4b0356df5ac5e685f0a34c8) | Exact main branch SHA `8358780829458854a4b0356df5ac5e685f0a34c8` | Historical application baseline remains frozen; **do not change it**. |
| [RecordSift release/0.2](https://github.com/infoconex/RecordSift/tree/338257f84a72a04136801aa93c3c435e28a61dce) | Exact branch SHA `338257f84a72a04136801aa93c3c435e28a61dce` | Current integration target if later approved; **not** main. |
| [RecordSift PR #258](https://github.com/infoconex/RecordSift/pull/258) / [issue #257](https://github.com/infoconex/RecordSift/issues/257) | PR **MERGED** into `release/0.2`, squash commit `338257f84a72a04136801aa93c3c435e28a61dce`; issue **CLOSED** | The earlier four-versus-five local NUnit script fix is **already complete on release/0.2**. Do not duplicate it or assume main changed. |
| [PR #258 Windows run 41587324609](https://github.com/infoconex/RecordSift/actions/runs/41587324609) | Exact original PR head `582458e184afc7b6da007ef63289b57afd286215`, successful Windows CI: five suites; **419 discovered, 418 passed, 0 failed, 1 expected skip**; combined metadata filter and no-match negative verified | Existing acceptance evidence; **not a new run against a proposed modernization candidate**. |
| [Release/0.2 windows-net48.yml](https://github.com/infoconex/RecordSift/blob/338257f84a72a04136801aa93c3c435e28a61dce/.github/workflows/windows-net48.yml) | Existing restore/build, five-suite CI AND local runner, API comparison with altered-baseline negative, five XML files, IDE1006, NFR checks, local unpublished pack and CS1591 negative | Preserve and reuse. Do **not** build another parallel acceptance framework without an observed deficit. |
| [verify-rc-consumer.yml](https://github.com/infoconex/RecordSift/blob/338257f84a72a04136801aa93c3c435e28a61dce/.github/workflows/verify-rc-consumer.yml) | Independent Windows clean consumer validates local prerelease and stable package candidates without publication | Retain in the future candidate acceptance checklist. |
| Project inventory | All **ten** actual `src/` and `tests/` traditional csproj files at release/0.2 individually inspected: each has exactly one `<LangVersion>7.3</LangVersion>`, `<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>`, and `Microsoft.CSharp.targets` import. Tracked repository tree has **no Directory.Build.props or Directory.Build.targets**. | A narrow shared language version change is possible; the baseline is not secretly already centralized. |

**Important evidence limitation:** this preparation checked actual source, merge status, historical CI metadata and documented EXP-002/005. It did **not** execute any new build, NUnit, restore, package or consumer; those must be rerun on the **future changed candidate** after separate authorization.

## 3. Phase 1: use our existing safeguards before touching the application

**Recommendation: A1 is largely existing infrastructure, not a new bespoke tool.** Before any new source change, declare these non-negotiable gates in the application's review checklist; point to exact *new candidate* workflow run results. Evaluate only genuinely missing evidence instead of modifying already-working CI.

| Check | Minimum future candidate acceptance | Current observed baseline |
| --- | --- | --- |
| Solution | Fresh Windows restore + Release build of **10** traditional net48/C#7.3 projects | Existing Windows CI; EXP-001 |
| Tests | All **five** NUnit suites, **419 discovered / 418 passed / 0 failed / 1 approved skip**; fail on missing suite, new skips or empty selection | Existing Windows CI and merged runner PR #258; must rerun on changed candidate |
| Public compatibility | Exactly **425** original public API + package metadata baseline entries (not only 414 compiled members), unless different format-aware gate is approved separately | `scripts/verify_public_api.ps1`; existing known negative |
| XML | Each of **five** production XML documentation files present and valid, preserve CS1591 negative | `scripts/verify_xml_documentation.ps1`; existing negative |
| Identity/dependencies | Preserve assembly/file versions, public API, resources, project references, approved NuGet dependency versions and metadata | Existing baseline/CI plus targeted comparison; don't assume green tests alone certify full graph |
| Packaging | Build and inspect **unpublished** local NuGet candidate; ensure contents/metadata expected | Existing `scripts/build_release_candidate.ps1`, CI |
| Actual consumer | Fresh net48 package install/clean consumer on candidate, including prerelease/stable local scenarios where required | Existing `verify-rc-consumer.yml`; never publish |
| Reproducibility/traceability | Exact candidate SHA, original baseline SHA, updated workflows/job IDs and clear comparison without relying on old green CI | Existing research evidence model; no Gate C-N production substitution |

**Stop conditions:** any failing build, a test count changing without approved explicit baseline, an unexplained API change, dependency/resource/assembly identity drift, missing XML or failed consumer => no implementation approval/merge. Do not hide skips or auto-update golden baselines. Existing CS1591 and public-API negatives must remain effective.

## 4. First proposed *new* change after that evidence review — D-002 conditional shared C# language version

**Business explanation:** Ten different project files repeat the same compiler-language setting. Put the default in one place, but **do not change C# 7.3 itself** or any application behavior.

**Why this and not SDK conversion first?** Lowest-risk preparation with isolated rollback, documented real disposable proof in [EXP-002](experiments/EXP-002-shared-properties.md) and [EXP-005](experiments/EXP-005-sdk-selection-and-overrides.md). Those two experiments already checked ten-project evaluation, override precedence and historical Release/test/API/XML/packaging behavior; **do not repeat identical experiments just for research**. An authorized, *real persisted candidate* will nevertheless need its own ordinary CI.

**Potential future edit footprint (only after separate approval):**
1. Add root `Directory.Build.props` containing **only** a conditional default `LangVersion=7.3` where `LangVersion` is empty. No other properties, SDK pins, analyzers, targets, package changes or broad imports.
2. Remove the redundant explicit `<LangVersion>7.3</LangVersion>` line from each of the **ten** project files, retaining every other project declaration exactly.
3. Do **not** add early `Microsoft.Common.props` imports or rewrite existing `Microsoft.CSharp.targets`; early import produced an error in EXP-006. Document the observed **late-import** behavior of these traditional projects.
4. Preserve a future project-specific value when a project deliberately overrides the default. Verify through evaluated MSBuild properties rather than source text alone.

**Required later validation:** exact diff of only these **11** intended files, original/current baseline SHAs, Debug and Release `LangVersion` evaluated for all ten projects (all 7.3), known project override honored in a *disposable test scenario* with no tracked drift, all A1 compatibility gates above on real candidate, and Windows CI with exact head. If an unapproved behavior, version/dependency/resource change or missing evidence appears, stop, revert candidate; no merging.

**Rollback:** revert the one props file and restore ten original project-local `LangVersion` declarations. No NuGet publication or primary branch merge is needed to test or reverse it. **Do not guarantee byte-identical DLL/PDB output**; earlier proof correctly checked behavioral and interface compatibility, not universal byte identity.

**Cost/benefit:** modest maintainability gain (one shared default), low feature risk, but 11-file mechanical scope means this must be easy to review and isolated from unrelated proposals. No claim that shared properties are an essential modernization requirement for every legacy .NET project.

**Future stakeholder decision wording:** “Approve an **isolated application candidate only** on a dedicated branch from currently verified `release/0.2`, with the 11-file change above, existing full acceptance and rollback. Do not merge, publish, promote to main, change C# version or framework, or add other build properties without another approval.” **This approval has NOT been given.**

## 5. Five simulated engineering perspectives (not five human signoffs)

- **Architecture:** Separate baseline contract from implementation; do not mix shared compiler defaults with SDK-style conversion or project layering changes.
- **Build:** Record actual property evaluation for both configurations; verify conditional override and import order, not merely project XML text.
- **Security:** No new source network endpoints, packages, unpinned build dependencies or Source Link activation. Preserve existing dependency audit.
- **Quality:** A candidate must rerun the complete 419/425/5/package/consumer checks; old experimental PASS is feasibility, not candidate acceptance.
- **Release governance:** Research-only choice cannot be interpreted as application merge authorization. Keep distinct roles for candidate implementation and final release promotion.

**Consensus of these simulated perspectives:** Review Phase 1 existing acceptance evidence, then recommend the smallest reversible shared-language-version candidate as first new code change, **subject to a separate approval**. No independent human/team consensus claimed.

## 6. Boundaries and next checkpoint

- RecordSift **main** remains frozen. Existing **release/0.2** runner fix remains as already merged; no further application commit is part of this proposal.
- No new experimental CI or duplicate PDB tests; no Source Link, Gate C-N release, SDK conversion, package format migration, dependency upgrades, analyzer policy or runtime/framework uplift.
- Keep research outputs in a **draft** PR unmerged. Summarize this proposal to the stakeholder in plain English and seek explicit implementation permission **only when ready** to undertake this specific change.
- Existing C-N #77/#80 release blockers stay unresolved **for C-N production use**, but do not obstruct documenting ordinary modernization plans.

**Current disposition:** Option A prioritization **APPROVED**; Phase 1 proposal **PREPARED**; first new RecordSift application implementation **NOT_AUTHORIZED**; no merge/publication/production changes.
