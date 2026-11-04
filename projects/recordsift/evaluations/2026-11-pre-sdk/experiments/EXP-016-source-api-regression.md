# EXP-016 — detect a real compiled public API regression

**Date:** November 4, 2026. **Status:** **Verified for the selected source-level enum and missing-evidence controls**; [Windows CI run #41884441296](https://github.com/infoconex/dotnet-modernization/actions/runs/41884441296) completed successfully. Research in draft PR #28, unmerged.
**Application baseline:** infoconex/RecordSift at SHA 8358780829458854a4b0356df5ac5e685f0a34c8; RecordSift main and release branches remain untouched.
**Predecessors:** [EXP-014](EXP-014-real-binary-metadata-pilot.md) checked same-binary repeat and altered external evidence; [EXP-015](EXP-015-actual-langversion-candidate.md) compared actual separately built revisions with matched contracts.

## Question and expected evidence

Can both the original 425-entry public API checker and the new metadata-extraction/comparison pipeline detect an **actual compiled source regression** even when ordinary tests pass? Does the comparator fail closed if a required metadata artifact is absent?

The chosen change is intentionally meaningful but buildable: the public CLR enum member RecordSift.Domain.Results.ImportStatus.Canceled has baseline value **3**. Change the **numeric literal to 42** while keeping the name, type, code, packages and project files otherwise intact. Consumers that persist or compare integer enum representations may break; tests comparing enum names may still pass. This is an actual contract change, not fabricated metadata.

## Independently built revisions

The [Windows workflow](../../../../../.github/workflows/validate-recordsift-source-api-regression.yml) calls the [experiment adapter](../../../../../tooling/pilots/recordsift/EXP-016/run.ps1) using the existing application-owned API, XML, package and clean-consumer gates plus shared .NET metadata extractor and compatibility comparator.

1. Check out the immutable baseline with no push credentials; require clean source. Create a detached separate baseline worktree. Restore/build all ten projects in Release and run the EXP-014 complete baseline gate (five NUnit suites, 425 legacy API entries, XML, unpublished NuGet package, clean consumer, metadata and repeated capture with external-evidence negative control).
2. In the distinct initially clean candidate checkout, make exactly one edit in src/RecordSift.Domain/Results/ImportStatus.cs: change implicit Canceled=3 to explicit Canceled=42. Commit locally **only inside CI**. Require exactly one changed file, different Git tree hashes and preserve the actual patch and candidate commit SHA. Never push to RecordSift.
3. Independently restore and rebuild the candidate. Run the original API guard but require it to **fail specifically for old Canceled=3 and current Canceled=42**; arbitrary tool errors are not an acceptable negative control. All remaining NUnit/XML/package/consumer checks must succeed.
4. Extract actual metadata from all five changed Release DLLs; capture separate source-verified evidence. Compare baseline and candidate. Require exit 1, changes_detected, clean_committed provenance, and **exactly two** public API line-set differences: removed enum field default 3 and added enum field default 42. Require assembly identity, resource names, NuGet logical contract and NUnit case outcomes to match.
5. Copy the candidate evidence to a separate incomplete folder and remove only public-api.txt; require capture exit 1 and comparison exit 1 with status incomplete and API missing_evidence.

Expected public API failure is an **intended negative result**, not a claim of unchanged compatibility. The EXP-014 runner defaults remain strict; a clearly named opt-in parameter is provided only for this narrow known Canceled enum mutation.

## Acceptance, retention and limits

All required baseline and candidate steps must run, with complete pass/fail observations and no missing components. The two negative controls must be proven by their exact output, not only exit codes. Retain the source patch, full commit/tree SHAs, host/tool versions, legacy and extracted API evidence, separate NUnit XML, comparator/negative-control JSON and per-side evidence reports for 30 days. Do not upload DLLs, package archives or secrets, and do not publish or merge application code.

This does not measure all runtime contracts, direct binary linking, native/COM, custom attributes, source/compiler compatibility, package bytes, signing or hermetic provenance. Matching package metadata/payload paths does not prove identical packaged binaries. A numeric enum value is one form of public contract regression; source-level method removal and other negative controls may be investigated later if warranted.

**Review lenses:** Modernization architect: relevance and scope of the enum regression. MSBuild/NuGet specialist: independent build roots and source provenance. Software architecture: reuse of existing validators. Test/release engineer: exact expected failures and missing evidence. Security/supply chain: isolation, no push or package publication. Documentation/developer experience: distinguish verified observations from planned controls. These are analytical criteria, not separate human approvals.


## Recorded outcome — verified negative controls on real compiled binaries

**Successful Windows CI:** [run 41884441296](https://github.com/infoconex/dotnet-modernization/actions/runs/41884441296) (research commit a2f6280a74d1ac56632c97dfd19cfd07e9a03149, before final documentation-only commits). Runner: GitHub Actions windows-2022, Visual Studio MSBuild for traditional net48 Release, .NET 10 SDK 10.0.403 for metadata extraction, PowerShell orchestration. Immutable baseline source: 8358780829458854a4b0356df5ac5e685f0a34c8. **Ephemeral CI-local candidate commit:** f8422e5673e85c19c820c4ad8205487d6e89efc8, recorded alongside tree hashes and one-file patch; **not pushed**.

| Check | Baseline | Intentional changed candidate |
| --- | --- | --- |
| Separate NuGet restore + Release rebuild of all ten projects | Passed | Passed |
| Application-owned 425-entry compiled API/package metadata guard | **425/425 passed** | **Expected failure**: exact Canceled numeric literal 3 removed and 42 added |
| Five production XML docs | Passed | Passed |
| Five NUnit suites | **419 discovered / 418 pass / 0 fail / 1 skip** | **419 / 418 / 0 / 1**, unchanged outcome |
| Local unpublished 0.1.0 package and installed net48 consumer | Passed | Passed |
| Four Getting Started sample inputs | Passed | Passed |
| Metadata-only read of five compiled assemblies | 443 API records | 443 API records (different enum value) |
| Same-revision repeated extract and external evidence-diff check | matched / detected | matched / detected |

**True independent source-version comparison:** reusable comparator returned **exit 1 / changes_detected** with clean committed source provenance. Only the **public API** category changed: one removed and one added record for the field default in **RecordSift.Domain** (Canceled 3 → 42). Assembly identity, embedded-resource names, NuGet logical package contracts, and NUnit case results all returned **matched**. The exact record names include the extractor's assembly-qualified prefix.

**Fail-closed missing-evidence control:** intentionally removed candidate public-api.txt from a separate copy of external artifacts. Capture returned **exit 1** with API **error**; subsequent comparison returned **exit 1 / incomplete**, API **missing_evidence**. This was expected and required. Missing evidence was not treated as a match.

**Durable evidence locator:** [CI artifact 13351465669](https://github.com/infoconex/dotnet-modernization/actions/runs/41884441296/artifacts/13351465669), name recordsift-exp016-source-api-regression-evidence, reported SHA-256 **6912916d2cf4ee66803884b26a32f4636a94c8724e9a6e3e0f9f561a837f1872**, 30-day retention. Includes experiment report, source patch, source SHA/tree evidence, comparison and missing-evidence JSON, NUnit, metadata manifests and per-side release-pilot reports; excludes DLL and nupkg bytes.

### Failed orchestration runs (preserved)

The following attempts **failed the workflow**; they do not count as complete experiment success and are not relabeled:

- [41882790894](https://github.com/infoconex/dotnet-modernization/actions/runs/41882790894): legacy checker correctly detected enum 3 → 42; a nonzero native process exit leaked into a successful PowerShell-only XML validation, causing a false harness failure. Corrected by resetting only the verified expected-negative exit state.
- [41883158939](https://github.com/infoconex/dotnet-modernization/actions/runs/41883158939): both compiled revisions built, all NUnit/consumer gates passed and the comparator detected the source regression; assertion incorrectly omitted the extractor's explicit owning-assembly prefix. Corrected to require the exact fully qualified record, without widening acceptance.
- [41883910260](https://github.com/infoconex/dotnet-modernization/actions/runs/41883910260): **all substantive positive and negative checks passed**, including missing-evidence rejection; the final wrapper inherited the expected comparator's exit 1 after the script printed success. Corrected to return process exit 0 **only after** asserting all individual expected failure statuses and generating the report.

The final successful run **41884441296** used these targeted harness corrections. Importantly, the tests and consumers passed on the intentionally incompatible candidate; passing them did **not** negate the detected public-contract regression.

## Review disposition

**Within verified scope:** a real compiled public enum numeric regression and missing mandatory evidence are both caught, with positive gates executing independently on baseline and candidate. This strengthens confidence in the reusable metadata/comparator pipeline and its fail-closed behavior.

**Not established:** arbitrary method removals, source-level consumers compiled against a previous assembly, DLL byte-for-byte equivalence, binding redirects, custom attributes, native/COM dependencies, persisted enum compatibility across all consumers, or supply-chain attestation. The candidate deliberately contains a breaking contract change and **must not be merged** into RecordSift. The research PR remains draft pending stakeholder review/merge approval.
