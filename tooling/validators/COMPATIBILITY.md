# Compatibility snapshots and baseline comparisons

**Scope:** Compare *explicitly collected* behavioral and packaging contracts from a baseline checkout and a candidate checkout. This is a comparison of evidence, **not** a build, release, binary introspection, signing verification, security scan or automatic approval to modernize.

The standard-library `compatibility.py` implementation works independently of RecordSift. Generate trustworthy artifacts for **each** checkout using the application's build/test/API tooling, then capture and compare them. In particular, **API, assembly identity and embedded-resource manifests must come from external trusted tools**; this module does not inspect compiled .NET assemblies or produce those manifests itself.

## Evidence contract

The [specification example](examples/compatibility-spec.example.json) selects only components actually being assessed. All file paths are relative to `--source`; source artifacts must exist under that checkout, and the output must be **outside** it.

| Component | Artifact contract | What is compared |
|---|---|---|
| `api` | UTF-8 text, one stable API/metadata record per line; blank lines and `#` comments ignored | Exact normalized record sets, additions/removals; no inference about compiled APIs from arbitrary text |
| `assemblies` | [JSON identity manifest](examples/assembly-identities.example.json): `schema_version:1`, `assemblies` with unique `name`, required `version`, optional `culture`, `public_key_token`, `file_version`, `informational_version` | Assembly identity properties; omitted properties are not verified |
| `resources` | [JSON resource manifest](examples/resources.example.json): unique assembly names, unique `resources` string array | Embedded-resource *logical names* for each assembly; not resource bytes or localization content |
| `packages` | List of unique `id` + `.nupkg` paths | NuGet `.nuspec` ID/version, dependency groups/version ranges/include/exclude; archive payload **paths only**, excluding known generated OPC/signature metadata |
| `tests` | List of unique `id` + NUnit **3** `<test-run>` XML paths | Complete reported counts (total/passed/failed/skipped/inconclusive), test-case full names, results and labels |

Archive comparison intentionally excludes ZIP timestamps, signature material, per-file hashes and compiled DLL bytes. **The same NuGet payload paths may contain different binaries without detection**; pair this comparison with actual compiled-API, assembly/resource and clean-consumer validation. `.nupkg` inspection does not install packages, verify authenticity, scan vulnerabilities or validate publisher signatures.

The NUnit reader rejects inconsistent totals, duplicate case names, unsupported results, or missing per-test evidence rather than treating them as passed tests. Namespace/assembly scoping is supplied through each test input's unique `id`; use one file per test suite/assembly where necessary. RecordSift's frozen main local test script omits XLSX—do not use its four-suite result as complete evidence.

## Capturing and comparing

Both checkouts should be **separate, reproducible source revisions**. Commit candidate changes before capturing if you want the final comparison to have verified Git provenance. Do not write generated reports inside either checkout.

```sh
python tooling/validators/compatibility.py capture \
  --source /path/to/baseline-checkout \
  --spec /path/to/baseline-spec.json \
  --expect-commit FULL_BASELINE_GIT_SHA \
  --output /external/evidence/baseline.json

python tooling/validators/compatibility.py capture \
  --source /path/to/candidate-checkout \
  --spec /path/to/candidate-spec.json \
  --expect-commit FULL_CANDIDATE_GIT_SHA \
  --output /external/evidence/candidate.json

python tooling/validators/compatibility.py compare \
  --baseline /external/evidence/baseline.json \
  --candidate /external/evidence/candidate.json \
  --output /external/evidence/comparison.json
```

Each captured component records **SHA-256 fingerprints of its exact source input files** (including raw `.nupkg` bytes). The comparison preserves both sides' input hashes separately from the *logical* contract differences: a package's binary bytes can differ even when the selected `.nuspec` fields and payload paths match. Review these fingerprints together with full binary/consumer gates. They are evidence fingerprints, not signatures or an attestation of authenticity.

**Capture exit statuses:** 0 = requested evidence captured; 1 = one or more requested components missing/invalid; 2 = bad configuration or Git SHA mismatch. Capture writes per-component `captured`/`error` and a list of capture errors.

The comparison refuses to overwrite either supplied snapshot file. Its output remains a distinct evidence artifact.

**Comparison exit statuses:** 0 = all requested contracts matched **and both snapshots have full, clean Git commits**; 1 = changed, incomplete, or unverified/dirty; 2 = invalid snapshot or I/O error. The JSON `overall` is:

- `matched`: captured categories match with clean committed provenance. **A scoped match, not a full compatibility certification.**
- `matched_unverified_provenance`: selected evidence matches but one/both Git revisions are missing or dirty.
- `changes_detected`: at least one category differs. Diffs distinguish additions, removals and changed identity/status values; capped at 100 items per category with `diff_truncated`.
- `incomplete`: a requested category is missing or invalid on either side, including scope mismatches.

The comparison contains per-component status and detailed differences. Components omitted from *both* specifications are **not tested** and are never silently auto-generated. If either side requests a component and the other does not, the comparison is incomplete. Review test runner coverage and package contents separately.

## Generating the input manifests

Use an existing approved application validator where possible; for example, RecordSift's frozen `docs/compatibility/public-api-net48.txt` contains a combined API/metadata text baseline, while `scripts/verify_public_api.ps1` already checks compiled assemblies. That historical file mixes **compiled API and raw package metadata**, so a format migration may change its metadata lines without changing compiled API. Preserve that distinction in findings; do **not** delete metadata entries or claim a 425-entry unchanged checker passed unless it actually did.

The new JSON assembly and resource manifests are a deliberately **small interchange format**, not evidence that their values were independently extracted from binaries. Record provenance of the extractor, runtime/PowerShell host, file hashes and exact build inputs as part of the surrounding experiment. A future reusable reflection or ECMA-335 metadata extractor may make those captures automatic, but should be tested on strong-named, mixed-mode, multi-target and framework-dependent assemblies before adoption.

## Reuse and safeguards

- Evidence-producing commands run under the existing [configurable gate runner](README.md) in a separately authorized, isolated build/test environment. The snapshot tool itself never runs those commands or changes applications.
- ZIP archives are read without extraction; unsafe traversal paths, duplicate entries, missing or ambiguous root nuspec and oversized manifests are rejected. Review archives before publication or distribution.
- Keep the source Git SHA guard, actual toolchain fingerprint, restoration provenance and all negative controls in your evaluation record. Existing `project.assets.json` or package caches are not proof of a fresh restore.
- Result JSON may include public signatures, dependency names and test identifiers. Review and control access to evidence before sharing.
- This tool does not claim public API source/binary compatibility, assembly loader behavior, resource content equivalence, consumer install/test success, package reproducibility, or runtime-platform support unless separately validated by those respective gates.

**Validation:** Unit fixtures exercise all five evidence areas, incomplete/malformed and intentionally malicious inputs, provenance enforcement, changed tests/packages/resources/assemblies, and reporting behavior. Hosted Python tests run on both Windows and Ubuntu under the existing toolkit CI workflow.
