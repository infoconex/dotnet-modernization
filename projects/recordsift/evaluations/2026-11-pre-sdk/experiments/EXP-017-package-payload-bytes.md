# EXP-017 — inspect exact NuGet package and compiled payload bytes

**Date:** November 4, 2026. **Status:** Research workflow awaiting independent CI evidence; do not label outcomes verified before the run completes.
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

**Results:** Pending actual CI; record exact run, source and candidate commits/tree SHAs, package digest differences and changed member classification only after verification.
