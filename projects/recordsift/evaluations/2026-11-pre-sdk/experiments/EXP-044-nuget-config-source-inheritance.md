# EXP-044 — NuGet.Config source-inheritance and normal restore controls

**Assessment date:** November 9, 2026 (Pacific); Windows execution November 10, 2026 UTC.  
**Tracking:** [dotnet-modernization #87](https://github.com/infoconex/dotnet-modernization/issues/87)  
**Application repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Unchanged application main baseline:** `3627a62260437db0bde83c5c7d3be56caee8af95`  
**Isolated research branch:** [research/nuget-config-inheritance-20261109](https://github.com/infoconex/RecordSift/tree/research/nuget-config-inheritance-20261109)  
**Research-only draft PR:** [#266 — DO NOT MERGE](https://github.com/infoconex/RecordSift/pull/266)  
**Definitive successful run:** [GitHub Actions 42737924517](https://github.com/infoconex/RecordSift/actions/runs/42737924517); [complete execution artifact 13728071750](https://github.com/infoconex/RecordSift/actions/runs/42737924517/artifacts/13728071750). **Research job passed**; four inheritance checks and ordinary restore each passed independently. The same PR commit also passed the existing Windows build/test, documentation, and clean-consumer workflows. An [earlier run 42737739041](https://github.com/infoconex/RecordSift/actions/runs/42737739041) passed A–E but its overall job failed at a subsequent evidence-push race. The workflow was adjusted so PR checks do not push evidence; the definitive run is fully green.

## Purpose and boundaries

Provide executed evidence for the companion NuGet.Config article, not alter RecordSift's source policy or project/package format. Verify:
1. `packageSources` inheritance and `<clear />`.
2. Separate `disabledPackageSources` inheritance and `<clear />`.
3. Ordinary RecordSift `packages.config` restore **without** `-ConfigFile` and with a fresh package directory.

The PowerShell script, workflow, and experimental README live under [research/nuget-config](https://github.com/infoconex/RecordSift/tree/research/nuget-config-inheritance-20261109/research/nuget-config); the workflow lives at [research-nuget-config-inheritance.yml](https://github.com/infoconex/RecordSift/blob/research/nuget-config-inheritance-20261109/.github/workflows/research-nuget-config-inheritance.yml). No production configuration was changed.

## Toolchain

| Item | Observed |
| --- | --- |
| Hosted Windows | `windows-2022`, Microsoft Windows `10.0.20348` |
| PowerShell | `7.6.9` |
| .NET SDK | `10.0.403` |
| NuGet CLI | `NuGet Version: 7.9.0.83` |
| NuGet executable | `C:\ProgramData\Chocolatey\bin\nuget.exe` |
| Source command | `dotnet nuget list source` (**no** `--configfile`) |

The experiment created a disposable parent/child directory outside the checkout. Parent `NuGet.Config` declared a fake `test-feed` and disabled `nuget.org`; child `NuGet.Config` declared `nuget.org` and varied the two `<clear />` settings. No project packages were acquired during A–D.

## Observed result matrix

| Scenario | Actual nuget.org | Actual test-feed | Result |
| --- | --- | --- | --- |
| A — Child clears package and disabled-source collections | Enabled | Absent | **PASS** |
| B — Child omits only `packageSources` clear | Enabled | Present | **PASS** |
| C — Child omits entire `disabledPackageSources` section | Disabled | Absent | **PASS** |
| D — Child restores both clears | Enabled | Absent | **PASS** |

Actual `dotnet nuget list source` output, trimmed only to separate commands:

**A — both cleared**
```text
Registered Sources:
  1.  nuget.org [Enabled]
      https://api.nuget.org/v3/index.json
```

**B — packageSources clear omitted**
```text
Registered Sources:
  1.  nuget.org [Enabled]
      https://api.nuget.org/v3/index.json
  2.  test-feed [Enabled]
      C:\NuGetTestFeed
  3.  Microsoft Visual Studio Offline Packages [Enabled]
      C:\Program Files (x86)\Microsoft SDKs\NuGetPackages\
```

**C — disabledPackageSources section omitted**
```text
Registered Sources:
  1.  nuget.org [Disabled]
      https://api.nuget.org/v3/index.json
```

**D — both clears restored**
```text
Registered Sources:
  1.  nuget.org [Enabled]
      https://api.nuget.org/v3/index.json
```

Scenario B also inherited the hosted runner's machine-installed Visual Studio Offline Packages source, demonstrating why readers' full source lists can differ. The presence and disabled-state assertions were automated. The [read-only evidence snapshot on the research branch](https://github.com/infoconex/RecordSift/blob/research/nuget-config-inheritance-20261109/research/nuget-config/evidence/inheritance-output.txt) retains the stdout and version information.

## Normal restore without explicit config

The script executed from RecordSift repository root:

```powershell
dotnet nuget list source
nuget restore .\RecordSift.sln -NonInteractive -PackagesDirectory <fresh temporary directory> -Verbosity detailed
```

There was **no `-ConfigFile` argument**. Effective source listing showed exactly **`nuget.org [Enabled]`**, and restore exited **0**. The full verbose restore log was preserved in the [workflow artifact](https://github.com/infoconex/RecordSift/actions/runs/42737924517/artifacts/13728071750) under `record-sift-restore.log`. This verifies successful normal restore and effective source configuration **in the tested runner**. It does not separately prove every downloaded package's origin or a security guarantee; caches and tool/version differences remain relevant.

The [normal-restore source listing](https://github.com/infoconex/RecordSift/blob/research/nuget-config-inheritance-20261109/research/nuget-config/evidence/record-sift-effective-sources.txt) is also retained separately.

## Follow-up case-study positive/negative restore evidence

The initial EXP-044 A–D checks used `dotnet nuget list source`, and E successfully restored the original RecordSift configuration without `-ConfigFile`. They did not themselves execute an intentionally disabled-source restore.

A later isolated case-study stage in [RecordSift PR #268](https://github.com/infoconex/RecordSift/pull/268) added that negative control without changing production `main`:

- [Exact stage execution commit `27daf116f23415ea117257ed5789ee9ab9963517`](https://github.com/infoconex/RecordSift/commit/27daf116f23415ea117257ed5789ee9ab9963517)
- [Successful stage workflow #42744343004](https://github.com/infoconex/RecordSift/actions/runs/42744343004) and [artifact #13730207481](https://github.com/infoconex/RecordSift/actions/runs/42744343004/artifacts/13730207481)
- Disposable `packages.config` referencing RecordSift's existing `NUnit 3.14.0`, with a fresh output directory for each restore, `-DirectDownload` and `-NoHttpCache`, and **no** `-ConfigFile` or `-Source` argument

| Control | Actual exit code | Installed | Disposition |
| --- | ---: | --- | --- |
| Inherited `nuget.org` disabled; child omits `disabledPackageSources` clear | 1 | No | Expected failure verified |
| Same source; child includes `disabledPackageSources` clear | 0 | Yes | Expected success verified |

The successful stage run also retained the original positive/negative source-listing controls and successful ordinary RecordSift solution restore. The two restore controls establish actual restore behavior on the observed Windows/NuGet CLI 7.9.0.83 runner. They do **not** prove an enterprise compliance policy, exhaustive package provenance, all tool versions, or audit advisory network contact.

## Interpretation and proposed disposition

- **Verified:** `packageSources` and `disabledPackageSources` are distinct inherited collections, and their `<clear />` elements independently affect effective source behavior.
- **Verified:** ordinary `packages.config` restore succeeded with the existing repository `NuGet.Config` and no explicit config selection.
- **Not verified by this experiment:** runtime audit advisory contact, enforcement of organizational network policy, cache package provenance, general portability to all NuGet versions, source mapping behavior, or complete deterministic builds.
- **Recommendation:** Evaluate adding `<disabledPackageSources><clear /></disabledPackageSources>` to RecordSift's production `NuGet.Config` if the intended policy is to enable explicitly declared nuget.org. Organizational policy must be considered. **Not approved or committed.** Any implementation requires separate owner authorization and its own checks.
- **Article:** Cite A–E, the separate stage restore controls, and tool versions; replace expected-result notes with observed results and differentiate the research job's successful assertions from the historical archival-race failure and the definitive green rerun.

No merges, releases, application source changes or blog publication were performed under this research.
