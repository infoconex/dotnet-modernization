# Independent Gate C-N Review — ONE Canonical Copy-and-Paste Prompt

Conduct an **independent, adversarial, evidence-driven engineering review** of the narrowly proposed **Gate C-N: Native Classic Windows-PDB Original Compiler-Source Provenance** acceptance protocol. You are one of three independently briefed model reviewers (Claude, Gemini, isolated ChatGPT), but you must **not** access or adopt any other reviewer's conclusions. Do not infer approval from successful CI or an existing acceptance summary.

## Repositories and exact immutable revisions

**Research repository:** https://github.com/infoconex/dotnet-modernization

**FROZEN RESEARCH CODE/REVIEW BASELINE SHA:** `719275bb16feed7a8cd2eb7afeb7ae3cb7117991`

**Application repository:** https://github.com/infoconex/RecordSift

**FROZEN APPLICATION SHA:** `8358780829458854a4b0356df5ac5e685f0a34c8`

**Draft research PR (context only; do not merge or use moving head):** https://github.com/infoconex/dotnet-modernization/pull/74

Use the **exact frozen revisions for all files**, rather than either repository's current default branch or the PR's potentially moving branch head. If code access is impossible, report the limitation instead of claiming an inspection. Do not change code or repository settings.

## Required documents at the frozen research SHA

The paths below are all in `infoconex/dotnet-modernization` **at exactly** `719275bb16feed7a8cd2eb7afeb7ae3cb7117991`:

1. `methodology/acceptance-gates/gate-cn-native-pdb-source-provenance.md` — proposed requirements CN-01 through CN-12.
2. `methodology/acceptance-gates/gate-cn-formal-acceptance-review-package-20261106.md` — review claim, evidence classes, limitations and acceptance mapping.
3. `methodology/acceptance-gates/gate-cn-manifest-custody-review-protocol-20261106.md` — prebuild scope, authority separation, custody, replay, and release proposal.
4. `methodology/acceptance-gates/gate-cn-acceptance-readiness-review-20261105.md` — earlier conclusions to **challenge**, not treat as proof.
5. `projects/recordsift/evaluations/2026-11-pre-sdk/gate-cn-recordsift-scope.json` — frozen historical RecordSift count scope, not a signed production manifest.
6. `methodology/acceptance-gates/gate-cn-exp044-evidence-scope.json` — historical different-application count scope, not production authorization.
7. `methodology/acceptance-gates/evidence/exp043-five-pdb-source-audit.json`, `exp043-managed-reader-exposure.json` and `exp044-non-recordsift-sanitized.json` — small sanitized aggregate reports, **not original PDB/source bytes**.

## Required actual implementation, tests, and build harness

In `tooling/validators/`, inspect directly:

- `gate_cn_live_provenance.py`
- `gate_cn_evidence_consistency.py`
- `gate_cn_live_evidence_consistency.py`
- `exp041_compiler_input_audit.py`
- `exp042_source_provenance.py`
- `exp043_five_pdb_audit.py`
- `exp043_managed_reader_exposure.py`
- `native_pdb_document_inventory.py`
- `native_windows_pdb_sourcelink.py`
- `classic_pdb_document_checksums.py`
- Relevant tests under `tooling/validators/tests/`, particularly `test_gate_cn_live_provenance.py`, `test_gate_cn_evidence_consistency.py`, and `test_gate_cn_live_evidence_consistency.py`.

Inspect the actual build/producer and release harness:

- `tooling/pilots/gate-cn/EXP-044/run.ps1`
- `tooling/fixtures/gate-cn/AnotherLibrary.Core/AnotherLibrary.Core.csproj`
- `tooling/pilots/recordsift/EXP-041/CompilerInputSnapshot.targets`
- `tooling/pilots/recordsift/EXP-042/CscParameterLogger.cs`
- `tooling/pilots/recordsift/EXP-042/MonikerProducerProbe.targets`
- `tooling/pilots/recordsift/EXP-043/build-remaining.ps1`
- `tooling/pilots/recordsift/EXP-014/run.ps1`
- `.github/workflows/validate-exp043-five-pdbs.yml`
- `.github/workflows/validate-exp044-non-recordsift-live.yml`
- `.github/workflows/validate-gate-cn-evidence-design.yml`
- `.github/workflows/validate-exp044-retained-evidence.yml`
- `.github/workflows/validate-modernization-tooling.yml`.

At the **frozen RecordSift application SHA**, independently inspect:

- `scripts/build_release_candidate.ps1`
- `scripts/verify_public_api.ps1`
- `scripts/verify_xml_documentation.ps1`
- `scripts/verify_clean_consumer.ps1`
- Relevant original five-project Release configurations and NUnit test outputs/runner definitions.

Trace real cross-file input/output and invocation relationships; do not just review filenames or supplied summaries.

## Actual GitHub Actions execution evidence to authenticate

**EXP-043: original five-assembly RecordSift native-PDB/source-byte and compatibility run**

- https://github.com/infoconex/dotnet-modernization/actions/runs/42173080423
- Expected executing research SHA: `9fb67deeb2aa4c98587727abc01e8a11f01070b4`
- Expected frozen RecordSift SHA: `8358780829458854a4b0356df5ac5e685f0a34c8`
- Reported: **64/64** per-assembly native original compiler-source document records; 59 tracked and 5 independently generated framework-moniker inputs; all five production PDBs. Original/candidate 425 public API baseline entries, 419 NUnit tests (418 pass, one expected skip), five XML documentation outputs, local NuGet pack/install and clean net48 consumer acceptance.
- Historical artifact ID `13482117590`; ZIP SHA256 `5efcc9b1c872f85c926eeef4819135a2325d97668b2abdcdde4e21f4b7e14443`.

**EXP-044: genuinely different traditional .NET Framework 4.8 project, actual live native PDB**

- https://github.com/infoconex/dotnet-modernization/actions/runs/42182129657
- Expected executing research SHA: `3c06d003ac75cc8b649a244be8705e44efa2c4c7`
- Reported **2/2** original physical compiler inputs: one tracked C# source, one framework-moniker source with observed producer execution.
- Historical artifact ID `13486535447`; ZIP SHA256 `dcb76d42aeccfd2e9524ca347bf24e4678430ab4a52960331450e41f27aa2bf6`.

**Secondary research checks executed at the frozen review SHA `719275bb16feed7a8cd2eb7afeb7ae3cb7117991`:**

- Gate C-N sanitized consistency and synthetic portability: https://github.com/infoconex/dotnet-modernization/actions/runs/42188740514
- EXP-044 historical artifact replay: https://github.com/infoconex/dotnet-modernization/actions/runs/42188740497
- Reusable tooling on Windows and Ubuntu: https://github.com/infoconex/dotnet-modernization/actions/runs/42188740504

All three were reported SUCCESS. **Verify independently where accessible.** Historical artifacts expire; saved public JSON and archive/checksum verification can authenticate what an earlier trusted job reported, **not reconstruct the private original physical source bytes, full identity keys or original PDBs**. Report if original runs/jobs are inaccessible.

## Core question and five deliberately adversarial review perspectives

**Under which exact threat/compilation/release scope, if any, could native original-source-byte proof be a defensible distinct production release acceptance criterion? Find evidence-supported reasons to block it.**

Perform five distinct reviews:

1. **Architecture and reusability:** clean/hexagonal architecture and SOLID principles; contract boundaries; portability beyond RecordSift; coupling; explicit supported and unsupported source generators, compiler formats and source origins.
2. **Build/compiler correctness:** actual MSBuild/Roslyn Csc TaskInput `Sources`; compiler execution identity; independently captured original physical bytes before/after Csc; pathmaps and normalized source identity; native PE/PDB GUID+age; MSF/DBI/C13 named/checksum/line and non-line-referenced documents; generated framework-moniker producer; multi-project/parallel builds; deterministic and source-identical stale binary risks.
3. **Security and privacy:** trust boundaries, manifest tampering, incomplete or self-authorized scope, forged or stale evidence, path escape/collisions, untrusted PDB parser safety vs trusted-local PDB scope, dependencies/advisories, unexpected exception privacy leaks, private source/URL/path/digest disclosure, runner cleanup, custody, retention, replay and revocation.
4. **Quality/test reliability:** meaningful negatives and mutation tests; actual vs mocked provenance; potential false-pass scenarios in which CI stays green; full externally enumerated PDB/source document universe; original vs candidate API/NUnit/XML/assembly/resource/package/installed consumer gates; **proof that test runners and packaged consumers loaded the PDB-attested candidate DLLs**.
5. **Release governance:** independent preapproved immutable production manifest, authorized reviewers and custodian, evidence authenticity and expiry, separation of approval to *review* versus approval to *activate*, exact CN-01..CN-12 mapping, no implicit waiver of the legacy gate.

**Do not conflate:** (a) real original compiler-source bytes; (b) native PDB /SRC/FILES digests; (c) native C13 `NONE` checksum records; (d) managed `ISymUnmanagedDocument` checksum exposure; (e) Source Link URLs/remote retrieval; (f) actual Visual Studio project package installation and debugger stepping; (g) release gate authorization. These are separate observable claims.

**Frozen policy disposition:** existing managed-reader checksum Gate C `UNSATISFIED` (0 actual checksum bytes exposed for 46 managed-reader documents); proposed native Gate C-N release `NOT_AUTHORIZED`; Source Link production `HOLD`; authentic Visual Studio package-project installation and remote debugger retrieval/stepping `NOT TESTED`.

## Evidence requirements and report format

Do not invent a finding. For each, give:

- Severity `BLOCKER`, `HIGH`, `MEDIUM`, or `LOW`.
- **Exact file and line number** (at a frozen commit), or verified job/run evidence.
- Observed defect versus explicit hypothesis/unknown, with reasoning and false-positive risk.
- Reproduction / negative-control / independent experiment specifically able to resolve it.
- Proposed correction and affected CN-01..CN-12 criteria.
- Whether needed *before human independent review* or only *before future production release acceptance*.

Submit a complete **Markdown** report containing: model/provider/version/date; exact code SHA(s), files and runs actually inspected; independent findings for each of five perspectives; consolidated ranked findings; CN-01..CN-12 status matrix; evidence gaps and unavailable sources; security/privacy findings; corrections required for each acceptance stage; no unnecessary repetition of already completed experiments; unaddressed stakeholder decisions; and one or more explicitly scoped verdicts chosen from `RESEARCH_ACCEPTABLE_WITH_GAPS`, `CHANGES_REQUIRED_BEFORE_REVIEW`, `BLOCKED_FOR_RELEASE`, `INSUFFICIENT_EVIDENCE`.

**Do not access other AI reviewers' reports or the author-context review** until your report is final. The normative/review-design documents are legitimate target artifacts to challenge; prior conclusions are **not proof**. If public GitHub/file/CI access fails, name each unavailable source and distinguish inspection from assumption. A green synthetic test and public aggregate replay are not independent original-source-byte proof. Multiple AI opinions are not independent named human approvals.

**Prohibited:** merging PRs; modifying RecordSift or either repository's `main`; publishing packages; activating/substituting/waiving release Gate C or Gate C-N; authorizing Source Link adoption; invoking hostile native COM; repeating completed expensive experiments without an identified evidence gap; claiming human review/signoff. **Review only; no repository edits.**
