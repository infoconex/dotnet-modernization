# EXP-016 — detect a real compiled public API regression

**Date:** November 4, 2026. **Status:** Proposed; Windows CI evidence pending.
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
