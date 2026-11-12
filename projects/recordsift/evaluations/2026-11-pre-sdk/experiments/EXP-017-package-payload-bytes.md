# EXP-017 — inspect exact NuGet package and compiled payload bytes

**Date:** November 4, 2026. **Status:** **Verified for the tested source and package-byte observations, positive/negative controls and same-source rebuild comparison**; review remains in draft PR #30.
**Source:** infoconex/RecordSift immutable main SHA 8358780829458854a4b0356df5ac5e685f0a34c8.
**Predecessors:** [EXP-015](EXP-015-actual-langversion-candidate.md) demonstrated unchanged selected *logical contracts* under conditional LangVersion centralization. [EXP-016, draft PR #28](https://github.com/infoconex/dotnet-modernization/pull/28) verified genuine compiled enum regression detection while full tests and package consumers passed.

## Question

Which exact NuGet package members change when the identical RecordSift release workflow independently builds the original source and the previously tested conditional LangVersion centralization candidate? How can reusable tooling distinguish:

- An identical ZIP archive and its members.
- ZIP-container differences (timestamps, compression, ordering or metadata) while all *uncompressed* member bytes match.
- A difference in one or more packaged members (including DLL, XML, nuspec, and OPC metadata), or additions/removals.
- Missing, unsafe or malformed ZIP evidence, which must never yield success.

This is complementary to the existing reusable compatibility comparator: its NuGet package contract deliberately compares logical manifest/dependency values and member *paths* but does not compare actual member byte hashes.

## Tools and experiment structure

Reusable [package_payload.py](../../../../../tooling/validators/package_payload.py) uses Python's standard-library ZIP reader, no extraction or assembly loading. It records full package SHA-256, archive size, named member SHA-256 and uncompressed size. Rejects missing root .nuspec, unsafe/ambiguous member names, symlinks, encrypted entries and oversized archives/members; fails closed on absent/corrupt data. Output is JSON with a documented version and distinct results: identical_archive_and_entries, different_container_same_entries, different_entries, incomplete, error. It never calls a result semantic compatibility or build reproducibility. The companion [fixture tests](../../../../../tooling/validators/tests/test_package_payload.py) cover real bytes, constant logical manifests, ZIP metadata-only changes, added/removed members, missing/corrupt packages, limits, duplicate names and traversal.

The [EXP-017 Windows CI](../../../../../.github/workflows/validate-recordsift-package-payload.yml) first executes **the unchanged EXP-015 script** against two independent worktrees, each with NuGet restore, Release rebuild of all ten projects, legacy API check, five NUnit suites, five XML docs, unpublished package and clean installed consumer, and five-component metadata comparison. No source is modified in RecordSift's branches or pushed.

The Windows research workflow additionally builds a **third independent Release checkout at the identical frozen source commit** through [same-source-repeat.ps1](../../../../../tooling/pilots/recordsift/EXP-017/same-source-repeat.ps1). It restores packages, rebuilds all ten traditional projects, and reexecutes the complete original API, NUnit, XML, unpublished packaging and clean consumer checks. Its package is compared to the first frozen-source build, separately from the altered LangVersion candidate. Distinct checkout directories and build times are not a hermetically equal environment, so this control does not prove the specific cause of differences.

The [RecordSift-specific adapter](../../../../../tooling/pilots/recordsift/EXP-017/controls.py) then reads both real locally produced RecordSift 0.1.0 archives:

1. Record actual package and member byte hashes and exact added/removed/changed paths. **Any real result is an observation; do not force a match or diff.** Different ZIP bytes, changed DLL bytes and changed nuspec bytes are different claims.
2. Check whether each package's embedded git commit matches the corresponding frozen or ephemeral candidate source commit, and preserve branch and URL attributes as *observations*. A hardcoded branch=main on a detached candidate is separately tracked by [investigation #29](https://github.com/infoconex/dotnet-modernization/issues/29); do not silently reinterpret the metadata or declare the published artifact defective.
3. Same-package positive control: byte inspector must return identical_archive_and_entries.
4. Real archive-byte negative control: create a **disposable package copy** (not an application binary/source change) with precisely one flipped byte in lib/net48/RecordSift.Domain.dll and identical member path set. Require the new byte comparator to detect exactly this changed member. Require the *existing logical contract* comparator to match, proving this is a real coverage gap rather than a claim that the older comparator malfunctioned.
5. Missing-package control: require incomplete, not a match.

Do not publish packages or upload DLLs/nupkg files. Preserve source tree hashes, patch, toolchain, package/member digest report, and selected original acceptance gate results. GitHub artifact retention is 30 days; checked-in findings must be summarized separately.

## Acceptance, risk, and scope

- Workflow and both platforms' shared Python validator tests must pass.
- Actual package hashes and member differences must come from the separately built artifacts, not invented fixtures. Preserve their results independently of the previously matched five logical contracts.
- All three controls must produce the specified statuses, and no missing/malformed evidence may count as verified.
- Byte identities are narrower than semantic identities: an exact hash match is evidence of byte identity, not safety/security proof; hash mismatch is not automatically proof of a behavioral regression.
- NuGet package ZIP-level metadata can differ while payload bytes match. Different assemblies can be compiler-generated provenance paths/attributes or actual IL changes; root cause requires targeted investigation.
- No signing, binding, native/COM, true deterministic build attestation, external NuGet-feed acquisition provenance, or security scanning is established by this experiment.
- RecordSift main SHA is immutable, and experimental candidate commits exist **only** in disposable CI. This is research/documentation only.

## Review criteria

Modernization architecture: source-to-compiled-byte provenance and no overclaiming. MSBuild and NuGet: independent build and correct separation of ZIP vs member bytes. Software maintainability: reusable generic comparator separate from RecordSift adapter. QA: positive, negative, and fail-closed controls in Windows and stdlib fixture CI. Security: bounded untrusted archives, no extraction and no uploads of compiled DLL/package bytes. Documentation: explicit source hashes, CI/artifact locators, precise observations and limitations. These are review lenses, not external human signoffs.

## Recorded Windows CI results — real packages and same-source control

**Fully successful run:** [GitHub Actions 41893283946](https://github.com/infoconex/dotnet-modernization/actions/runs/41893283946), research workflow source SHA `b448c1f9a226851be77293c3f243d6ce6d31eda3`. [Artifact 13355435536](https://github.com/infoconex/dotnet-modernization/actions/runs/41893283946/artifacts/13355435536), SHA-256 `985fec126d97f7e74c02ba7fc5f3a897e2fd5d01756ba3c5ac0625d50e5dcfc2`, 30-day retention. It contains JSON with exact full package and member SHA-256 values, the original source patch/tree fingerprints, and per-build acceptance reports. No compiled DLL or nupkg bytes were uploaded. Its disposable candidate Git commit was `254ba273ac5dc11495dd05c93601e0f16740b771`; the baseline and repeated frozen builds both used source SHA `8358780829458854a4b0356df5ac5e685f0a34c8`.

All **three** independently restored/rebuilt ten-project Release revisions passed the application-owned **425-entry** compiled public API gate, five NUnit suites (**419 discovered / 418 pass / 0 fail / 1 skipped**), five XML documentation checks, unpublished local NuGet packaging, and independent installed net48 consumer plus four Getting Started examples. The EXP-015 baseline-versus-candidate metadata comparator reported all five selected components **matched** (443 extracted metadata records per side).

| Comparison | Observed exact bytes | Interpretation |
| --- | --- | --- |
| Frozen source build A vs LangVersion candidate | `different_entries`: **6 changed package members** — `RecordSift.nuspec` and **all five** `lib/net48/RecordSift.*.dll` | Package commit stamp differs by correct source SHA; DLL byte differences cannot be assigned to source configuration without a repeat control |
| Frozen source build A vs independent build B **of the same source commit** | `different_entries`: **all five DLL members changed; the nuspec member matched** | In these separate Windows worktrees, identical Git source SHA is **not sufficient for byte-identical compiled DLLs**. Source and public metadata/tests match; host path, time and compiler/build inputs are not isolated |
| Same packaged archive vs itself | `identical_archive_and_entries` | Positive control passed |
| Baseline package vs a disposable archive copy with precisely one flipped byte of `RecordSift.Domain.dll` | `different_entries`, **exactly one changed DLL member**, unchanged package member paths | Byte-level detector finds drift that the separately checked legacy logical NuGet comparator intentionally ignores |
| Baseline vs nonexistent candidate package | `incomplete` | Required missing evidence fails closed |

**Package source metadata:** Both actual revision packages and the same-source repeat had repository URL `https://github.com/infoconex/RecordSift.git` and embedded a commit matching the actual source revision. All recorded `branch=main`, including the locally committed disposable LangVersion candidate; the interpretation is tracked in [issue #29](https://github.com/infoconex/dotnet-modernization/issues/29). This does not establish a defect in the published release.

**Portable tool tests:** the [reusable tooling workflow 41892475052](https://github.com/infoconex/dotnet-modernization/actions/runs/41892475052) passed its complete test suite on Windows 2022 and Ubuntu 24.04 at initial PR head; [workflow 41893283952](https://github.com/infoconex/dotnet-modernization/actions/runs/41893283952) also passed on the same head as the three-source experiment. The earlier [successful 41892475150](https://github.com/infoconex/dotnet-modernization/actions/runs/41892475150) independently confirmed the first six changed members and the three controls, *before* adding the same-source repeat. The repeat was an important additional control, not a correction of a failed experiment.

**Interpretation:** **Do not claim that LangVersion centralization changed application behavior because the DLL hashes differ.** The five DLL members already differ under independent builds from identical frozen source. This does not prove the specific mechanism (MVID, PE timestamp, PDB path/compiler flags, generated source or any other input) or full deterministic-build behavior. A separate targeted reproducibility investigation is justified before recommending changes to signing/build properties. No application source or package has been pushed or published.


**Follow-up research:** [issue #31](https://github.com/infoconex/dotnet-modernization/issues/31) tracks targeted CLR module/version-ID, PE/PDB and MSBuild property investigations to determine why separate builds of the same source produce differing DLL bytes. Do not assume any specific cause or recommend application changes from this first byte-level observation.

**Preserved intermediary harness failure:** [run 41893233396](https://github.com/infoconex/dotnet-modernization/actions/runs/41893233396) **failed** after the adapter began requiring a third repeated-frozen package but before the workflow had been updated to construct that third checkout. Its baseline/candidate build and gate checks succeeded, but the final comparison correctly rejected missing required repeat evidence. The subsequent [run 41893283946](https://github.com/infoconex/dotnet-modernization/actions/runs/41893283946) included the missing independent checkout, passed all three full release-pilot gates, and satisfied the expanded experiment acceptance criteria. The failed attempt is not counted as a successful same-source experiment.
