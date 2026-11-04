# EXP-014 — Read-only RecordSift .NET Framework 4.8 compiled-metadata pilot

**Status: Verified on the frozen .NET Framework 4.8 release baseline (November 4, 2026).** [Successful Windows CI run #41858448425](https://github.com/infoconex/dotnet-modernization/actions/runs/41858448425). The research is in **draft PR #26**, stacked on **draft PR #25** (unmerged extractor); neither is approved to merge. RecordSift's frozen source commit and main branch remain unchanged.

## Question

Can the generic metadata extractor read **actual** RecordSift 0.1 .NET Framework 4.8 Release assemblies, generate three compatibility formats, and produce reproducible evidence alongside existing RecordSift release gates—without modernizing or modifying the application?

## Fixed inputs and validation

- Repository: `infoconex/RecordSift`, exact source commit `8358780829458854a4b0356df5ac5e685f0a34c8`; public repository checked out to the **Windows 2022 GitHub Actions runner**, no push/write credentials.
- Analyzer: `tooling/assembly-metadata` on the currently **draft** metadata-extractor branch from PR #25, built using pinned **.NET SDK 10.0.403**.
- Restores the traditional solution's `packages.config` dependencies with `NuGet.Config`, then builds all 10 projects in Release using the Visual Studio installation's MSBuild.
- Verifies application-owned `scripts/verify_public_api.ps1` against the established combined 425-record API/package baseline and `scripts/verify_xml_documentation.ps1` against all five assemblies.
- Runs **five separate NUnit 3 test assemblies**, not the frozen `scripts/run_tests.ps1` which omits XLSX; requires 419 discovered / 418 passed / 0 failed / 1 skipped, and records suite-level XML.
- Uses the application-owned, **unpublished** `build_release_candidate.ps1` with package version 0.1.0 and `verify_clean_consumer.ps1` on an independent installed net48 consumer.
- Invokes the new extractor twice on the *same* five immutable-built Release assemblies, collecting identity, public API, resource name manifests and SHA-256 of compiled DLLs.
- Uses the generic `compatibility.py capture --artifacts-root ... --expect-commit ...` for both independent evidence roots (five test XMLs, local NuGet package and three metadata manifests); requires a scoped `matched` result with clean source Git status.
- Performs an **expected failure** control by appending a fabricated API record **to copied external evidence only** and verifying `changes_detected` with comparison exit code 1.

## Recorded outcome — verified real assemblies

**Exact source:** `8358780829458854a4b0356df5ac5e685f0a34c8`. **Platform:** GitHub Actions Windows Server 2022; traditional Visual Studio MSBuild for RecordSift .NET Framework 4.8; extractor SDK pinned to `10.0.403`. **Run:** [#41858448425](https://github.com/infoconex/dotnet-modernization/actions/runs/41858448425), conclusion `success`.

| Gate | Observed result |
| --- | --- |
| Frozen 10-project solution NuGet restore and Release MSBuild | Passed |
| Existing RecordSift NFR-010 compiled API + package metadata guard | **425/425 records verified** |
| Existing XML documentation checks for all production assemblies | Passed |
| Domain NUnit | 123 total / 123 passed / 0 skipped |
| Application NUnit | 62 total / 62 passed / 0 skipped |
| Infrastructure.Csv NUnit | 132 total / 131 passed / 1 skipped |
| Infrastructure.Reporting NUnit | 54 total / 54 passed / 0 skipped |
| Infrastructure.Xlsx NUnit | 48 total / 48 passed / 0 skipped |
| Total NUnit | **419 discovered, 418 passed, 0 failed, 1 skipped** |
| Unpublished local RecordSift 0.1.0 package | Passed; SHA-256 `e01e8615a177ed7aae8cc10956a71e500325c2cbce75dd8438ec0b73fe9f70cc` |
| Installed independent .NET Framework 4.8 consumer and four Getting Started examples | Passed |
| New metadata-only extractor on five real Release DLLs | **443 API records**; identity and resource-name manifests generated |
| Two independently extracted snapshots of the **same binaries** | `matched` with full five-category evidence (API, assembly identities, resources, package, NUnit) |
| Intentional addition to **copied external** API evidence | `changes_detected` as required, exit code 1 |
| Source revisions and modification checks | Build and clean proof worktree at same pinned commit; no tracked source changes |

**Provenance observation:** The disposable build checkout contained ten untracked diagnostic files: five `InternalTrace.*.log` and five `nunit-agent_*.log`, produced by the tool/test environment. It was correctly marked dirty. A separate **clean detached worktree** at the same SHA supplied source identity to the comparator, while compiled DLL SHA-256 values and the build checkout's dirty paths were captured in `pilot-report.json`. This preserves the difference between *clean source revision evidence* and a generated-output build workspace; it does not erase or reinterpret the latter.

**Evidence retention:** [CI artifact `recordsift-exp014-research-evidence` (ID 13339046592)](https://github.com/infoconex/dotnet-modernization/actions/runs/41858448425/artifacts/13339046592), archived November 4, 2026 with 30-day retention. It contains snapshot JSON, comparison and negative-control JSON, representative metadata manifests, NUnit XML and per-DLL hashes in the pilot report. The local `.nupkg` and DLLs were **not uploaded**. The archive's reported SHA-256 digest is `c351e039e9631f0fa69931bafc2c6a3b74e1e686df48f7399b00fd6adba3f4ba`.

**Interpretation:** The observed **443** records do not represent an expansion/regression from the existing **425** baseline: the legacy script includes package/project metadata and uses a different public signature grammar, while the new extractor reports metadata records according to its own schema and visibility rules. They cannot be directly subtracted, equated or substituted for one another. The original 425-record guard **ran and passed separately**.

**Troubleshooting history:** Earlier CI runs [#41856355214](https://github.com/infoconex/dotnet-modernization/actions/runs/41856355214) and [#41857286861](https://github.com/infoconex/dotnet-modernization/actions/runs/41857286861) failed on experiment orchestration (hashtable aggregation and an honest dirty-worktree provenance status), **not** on RecordSift's API/tests or the extractor's ability to read five DLLs. The final successful run corrected the aggregation and applied separate-worktree provenance without relaxing the comparator's clean-source requirements.

## Meaning of the results

A successful execution supports a **real .NET Framework 4.8 compiled-assembly inspection**, integration with the approved application-owned validations, and consistency of repeat extraction. Because both valid snapshots read the *same binaries*, it does **not** show baseline-to-modernized-candidate parity or target-framework migration success.

The old 425-record combined baseline is enforced by the existing application script. The extractor's metadata-only format is not interchangeable with that baseline; no counts should be compared or converted as though formatting and packaging differences were binary API changes.

The disposable **build checkout** may contain generated/untracked build, restore and test outputs. The pilot checks that no **tracked application source** changed, records that checkout's dirty/untracked paths, and creates a **separate clean detached Git worktree at the same immutable SHA** for the comparator's Git provenance. This does not pretend that the build checkout is clean: attribution of compiled DLLs to that SHA rests on the controlled checkout/build CI steps and recorded per-DLL SHA-256 hashes. A matching clean proof worktree is necessary but is not a cryptographic attestation of the binary build inputs.

## Execution safety and evidence

The workflow `.github/workflows/validate-recordsift-metadata-pilot.yml` runs only on proposed research changes or explicit dispatch, with `contents: read` permissions. The source checkout is public and pinned, package output stays on the runner, and no NuGet publishing, Git pushes, tags or application merges occur. Only reports, metadata text/JSON and NUnit XML are retained as ephemeral CI artifacts for **30 days**. Archives and NuGet packages are *not uploaded*. Outputs live outside the RecordSift checkout.

**Acceptance requires** the Windows CI job to finish successfully, each original gate's success to be verified from the run, actual source/toolchain SHA and package evidence, full 419-test suite, a repeated scoped match and a real negative-control detection. If any prerequisite fails, record **blocked/failed** findings rather than claiming the extractor is validated.

## Related documentation

- [Assembly metadata extractor (draft PR #25)](../../../../../tooling/assembly-metadata/README.md)
- [Compatibility evidence guide](../../../../../tooling/validators/COMPATIBILITY.md)
- [Experiment scripts](../../../../../tooling/pilots/recordsift/EXP-014/run.ps1)

**Not authorized:** merging PR #25 or this stacked pilot PR to main, making changes to RecordSift, changing framework/SDK project style, or treating a clean repeat comparison as full compatibility certification.
