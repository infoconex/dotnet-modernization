# Historical RecordSift research source index (November 2026)

**Scope:** This index records historical experiment artifacts preserved in `main` and immutable draft PR heads. It is **not** a claim that earlier experiments have been rerun, nor an approval to enable Source Link, a production release gate, or any application change.

## Historical evidence and source now on research main

- [EXP-016 source-level API regression](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-016-source-api-regression.md) and [EXP-017 package-byte comparison](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-017-package-payload-bytes.md) were preserved from historical research PRs [#28](https://github.com/infoconex/dotnet-modernization/pull/28) and [#30](https://github.com/infoconex/dotnet-modernization/pull/30).
- [EXP-018–043 experiment reports](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/README.md), relevant validators and opt-in research workflows were progressively preserved in original source-specific integration merges through [PR #82](https://github.com/infoconex/dotnet-modernization/pull/82). The reports record exact experiment conditions, including failed, blocked and inconclusive outcomes. Previously merged PR source files, not this index, determine the retained executable code.
- [Gate C-N D2b research controls](https://github.com/infoconex/dotnet-modernization/pull/91) preserve the exact eight file blobs from original draft [#83](https://github.com/infoconex/dotnet-modernization/pull/83), including local NuGet and .NET Framework CLR identity probes.
- [Post-D2b human-review handoff preparation](https://github.com/infoconex/dotnet-modernization/pull/92) preserves two source-identical historical reviews from draft [#84](https://github.com/infoconex/dotnet-modernization/pull/84). **Simulated engineering perspectives are not independent human approvals.**
- [RecordSift Option A outcome and review-governance proposal](https://github.com/infoconex/dotnet-modernization/pull/93) preserve two historical documents from draft [#86](https://github.com/infoconex/dotnet-modernization/pull/86). Earlier references to `release/0.2` describe the original November 6 state; that branch was subsequently removed by the owner.

## Alternate or blocked PDB investigations

Two earlier divergent drafts are preserved separately rather than silently conflated with the later independently validated native-PDB path:

| Draft | Report | Retained source | Evidentiary status |
|---|---|---|---|
| [#45 / EXP-029 alternate](https://github.com/infoconex/dotnet-modernization/pull/45) at `b1ad2927d91f585eede12c9d41cf01df664e53a5` | [C13 checksum research](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-029-c13-document-checksum.md) | [Inactive archive](../../tooling/archives/recordsift/2026-11/alternate-pdb-research.md) | Research draft; its full real-Windows source-checksum assertion is **not** promoted as verified |
| [#48 / EXP-031](https://github.com/infoconex/dotnet-modernization/pull/48) at `36bd8de35543aa1f41420d3f4bb9e25b52068666` | [Managed PDB reader investigation](../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-031-managed-pdb-checksums.md) | [Inactive archive](../../tooling/archives/recordsift/2026-11/alternate-pdb-research.md) | **BLOCKED:** required patched native reader package was unavailable in the recorded execution |

Original YAML from #45 and #48 is placed **outside** `.github/workflows/` and original tools/test code is placed outside live `tooling/validators/` to prevent discovery as active validation. Exact Git blob hashes of archived files match the original draft heads. Reproduction requires separate technical/security review and explicit scope approval.

## Disposition and retention

The [original documentation-only consolidation draft #90](https://github.com/infoconex/dotnet-modernization/pull/90) became obsolete as exact code, workflows and documentation were preserved through focused PRs. **Its differing copies of EXP-024/025/026/029 are not used to overwrite newer files on `main`.** Source in historical draft PRs remains addressable by immutable commit SHA even when old branches are later deleted.

Research conclusions are only as strong as their cited exact-run evidence. **Original managed Gate C: UNSATISFIED. Proposed native Gate C-N production: NOT_AUTHORIZED. Source Link production adoption: HOLD.** No production release, package publishing, or RecordSift branch mutation follows from this archive.
