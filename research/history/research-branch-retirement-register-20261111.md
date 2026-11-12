# Research branch retirement register — November 11, 2026

**Repository:** [infoconex/dotnet-modernization](https://github.com/infoconex/dotnet-modernization)  
**Verified main at audit:** `77484d7aba11f081f043e09d659144d58e6311ed`  
**Audit:** 44 non-`main` branches; 0 open pull requests.

## Interpretation

This is an inventory of exact branch tips *before branch deletion*, not permission to delete branches automatically. All branch trees were checked against the preserved research `main` tree after PRs #91–94. No research branch has an otherwise unpreserved source **path**, apart from six original executable paths from alternate EXP-029/EXP-031 drafts, whose **identical Git blob content** is preserved in the [inert archive](../../projects/recordsift/evaluations/2026-11-pre-sdk/archives/alternate-pdb-research.md). Many historical branches contain **older revisions** of files with the same paths. Those older revisions remain associated with their commits, not as identical copies on `main`.

Original historical research PR references and run evidence remain the provenance for original experiments. Deleting a branch removes its convenient ref; this register records its exact commit SHA, but **does not guarantee permanent reachability of an otherwise unreferenced commit**. Review external links referring to branch names and preserve any additional necessary commit/tree evidence before deleting a branch. Original CI runs are not rerun by this audit.

## Branches

| Branch | Audited exact tip SHA | Note |
| --- | --- | --- |
| `integration/archive-alternate-pdb-research-20261111` | [`fcbc31672ce01da5ef3b0867478386536452834f`](https://github.com/infoconex/dotnet-modernization/commit/fcbc31672ce01da5ef3b0867478386536452834f) | Superseded integration branch; associated PR merged |
| `integration/preserve-gate-cn-d2b-20261111` | [`807cfc9c96f458338ac408840e4fd04b1a240c9a`](https://github.com/infoconex/dotnet-modernization/commit/807cfc9c96f458338ac408840e4fd04b1a240c9a) | Superseded integration branch; associated PR merged |
| `integration/preserve-gate-cn-handoff-20261111` | [`a6012041e9b3014015f97f544762a1a025871832`](https://github.com/infoconex/dotnet-modernization/commit/a6012041e9b3014015f97f544762a1a025871832) | Superseded integration branch; associated PR merged |
| `integration/preserve-option-a-governance-20261111` | [`6fa8319b16293a698fee93d8f559f14decb7932b`](https://github.com/infoconex/dotnet-modernization/commit/6fa8319b16293a698fee93d8f559f14decb7932b) | Superseded integration branch; associated PR merged |
| `research/acceptance-gate-decision-review-20261105` | [`c0dcd7e93b8466ff7a0c7f88b5d0ad5a2ea3a1fc`](https://github.com/infoconex/dotnet-modernization/commit/c0dcd7e93b8466ff7a0c7f88b5d0ad5a2ea3a1fc) | Historical research branch |
| `research/consolidate-verified-findings-20261111` | [`f08ad074b3dda5ae119a2b4974578eb6d2bbe6d1`](https://github.com/infoconex/dotnet-modernization/commit/f08ad074b3dda5ae119a2b4974578eb6d2bbe6d1) | Historical research branch |
| `research/exp016-source-api-regression-20261104` | [`6f14cfeeba4e11d9a3c6020d64b2c21876985c11`](https://github.com/infoconex/dotnet-modernization/commit/6f14cfeeba4e11d9a3c6020d64b2c21876985c11) | Historical research branch |
| `research/exp017-package-payload-bytes-20261104` | [`83eb8c7b6c5ac5458b0ad3a6c1048702a35038c3`](https://github.com/infoconex/dotnet-modernization/commit/83eb8c7b6c5ac5458b0ad3a6c1048702a35038c3) | Historical research branch |
| `research/exp018-assembly-reproducibility-20261104` | [`1a960e83561b190afbfc2548536f3d44dca7a088`](https://github.com/infoconex/dotnet-modernization/commit/1a960e83561b190afbfc2548536f3d44dca7a088) | Historical research branch |
| `research/exp019-deterministic-msbuild-20261104` | [`6b529f8375e6e9f13d320760ccd9a15da7906ca2`](https://github.com/infoconex/dotnet-modernization/commit/6b529f8375e6e9f13d320760ccd9a15da7906ca2) | Historical research branch |
| `research/exp020-pathmap-isolation-20261104` | [`65306b2ebd19e4f72367690e97020b52ecfbda33`](https://github.com/infoconex/dotnet-modernization/commit/65306b2ebd19e4f72367690e97020b52ecfbda33) | Historical research branch |
| `research/exp021-ci-property-only-20261104` | [`9a8037e802009d52d52273326507fc2d23275e39`](https://github.com/infoconex/dotnet-modernization/commit/9a8037e802009d52d52273326507fc2d23275e39) | Historical research branch |
| `research/exp022-manual-sourceroot-20261104` | [`3e661b10998f273509a28e5682f088191b5f9b6f`](https://github.com/infoconex/dotnet-modernization/commit/3e661b10998f273509a28e5682f088191b5f9b6f) | Historical research branch |
| `research/exp023-sourcelink-package-audit-20261104` | [`616c5833378a77703bd5afd8e226bc5346b5a271`](https://github.com/infoconex/dotnet-modernization/commit/616c5833378a77703bd5afd8e226bc5346b5a271) | Historical research branch |
| `research/exp023b-dependency-preflight-20261104` | [`876e890b750dd747a326a242fb7403076c0fcee6`](https://github.com/infoconex/dotnet-modernization/commit/876e890b750dd747a326a242fb7403076c0fcee6) | Historical research branch |
| `research/exp024-sourcelink-windows-imports-20261104` | [`d2c84377b98be29bb1ad9c6f2ba65b28f88daef2`](https://github.com/infoconex/dotnet-modernization/commit/d2c84377b98be29bb1ad9c6f2ba65b28f88daef2) | Historical research branch |
| `research/exp025-native-windows-pdb-20261104` | [`a2ee6122c5a29282fb2d27f3049af4aed5f0eccd`](https://github.com/infoconex/dotnet-modernization/commit/a2ee6122c5a29282fb2d27f3049af4aed5f0eccd) | Historical research branch |
| `research/exp026-sourcelink-two-worktrees-20261104` | [`99a70ba270b0e744a1de5e1aaada344aee8fc497`](https://github.com/infoconex/dotnet-modernization/commit/99a70ba270b0e744a1de5e1aaada344aee8fc497) | Historical research branch |
| `research/exp027-nuget-closure-isolation-20261104` | [`928567178daba11d6403ba6a0dfa0b797fdca0e2`](https://github.com/infoconex/dotnet-modernization/commit/928567178daba11d6403ba6a0dfa0b797fdca0e2) | Historical research branch |
| `research/exp028-source-remote-byte-validation-20261104` | [`8fc900f11455999b92be5336463b4bc13644edf8`](https://github.com/infoconex/dotnet-modernization/commit/8fc900f11455999b92be5336463b4bc13644edf8) | Historical research branch |
| `research/exp029-pdb-document-checksum-20261104` | [`b1ad2927d91f585eede12c9d41cf01df664e53a5`](https://github.com/infoconex/dotnet-modernization/commit/b1ad2927d91f585eede12c9d41cf01df664e53a5) | Alternate historical source; original executable blobs also in inert archive |
| `research/exp029-pdb-source-checksums-20261104` | [`22c7413518f0284748af0f3f73fc63e3a6c79fb3`](https://github.com/infoconex/dotnet-modernization/commit/22c7413518f0284748af0f3f73fc63e3a6c79fb3) | Historical research branch |
| `research/exp030-git-topology-controls-20261104` | [`1dbc00300e33269ece967611e9d86405dd80e4ff`](https://github.com/infoconex/dotnet-modernization/commit/1dbc00300e33269ece967611e9d86405dd80e4ff) | Historical research branch |
| `research/exp031-managed-pdb-document-hashes-20261104` | [`36bd8de35543aa1f41420d3f4bb9e25b52068666`](https://github.com/infoconex/dotnet-modernization/commit/36bd8de35543aa1f41420d3f4bb9e25b52068666) | Alternate historical source; original executable blobs also in inert archive |
| `research/exp032-sourcelink-task-module-bindings-20261104` | [`b73d355a0b03f5f042800a40003a3398ccaeb7b8`](https://github.com/infoconex/dotnet-modernization/commit/b73d355a0b03f5f042800a40003a3398ccaeb7b8) | Historical research branch |
| `research/exp033-native-c13-checksum-structure-20261104` | [`312c721929796fa8d7c24287fece332371fbbcd1`](https://github.com/infoconex/dotnet-modernization/commit/312c721929796fa8d7c24287fece332371fbbcd1) | Historical research branch |
| `research/exp034-all-csv-source-provenance-20261104` | [`b4cb1600778275764b924c3318b0bd85d3b35bc2`](https://github.com/infoconex/dotnet-modernization/commit/b4cb1600778275764b924c3318b0bd85d3b35bc2) | Historical research branch |
| `research/exp035-dia-sdk-checksum-probe-20261105` | [`eb931a2d048d1bf4b35dabecd522d7a2e908f69c`](https://github.com/infoconex/dotnet-modernization/commit/eb931a2d048d1bf4b35dabecd522d7a2e908f69c) | Historical research branch |
| `research/exp036-fixture-managed-pdb-20261105` | [`d90aff52cd254a011422486d2feddb41a1dd94f1`](https://github.com/infoconex/dotnet-modernization/commit/d90aff52cd254a011422486d2feddb41a1dd94f1) | Historical research branch |
| `research/exp036-frozen-csv-managed-checksums-20261105` | [`feb6bd3d9e1b8f62f4154ca53551dbbedca89655`](https://github.com/infoconex/dotnet-modernization/commit/feb6bd3d9e1b8f62f4154ca53551dbbedca89655) | Historical research branch |
| `research/exp036-managed-pdb-fixture-preflight-20261105` | [`6b4e5d41bb695e45d2346fb89a746efb0871c10a`](https://github.com/infoconex/dotnet-modernization/commit/6b4e5d41bb695e45d2346fb89a746efb0871c10a) | Historical research branch |
| `research/exp037-compiler-pdb-differential-20261105` | [`e65b5789757e91b8fc3be22b9dbf1dc16e1b51c3`](https://github.com/infoconex/dotnet-modernization/commit/e65b5789757e91b8fc3be22b9dbf1dc16e1b51c3) | Historical research branch |
| `research/exp038-pdb-document-stream-key-association-20261105` | [`70793a4e6e016b6c20dcee56d3d847e7d242c5fb`](https://github.com/infoconex/dotnet-modernization/commit/70793a4e6e016b6c20dcee56d3d847e7d242c5fb) | Historical research branch |
| `research/exp039-reusable-native-pdb-verifier-20261105` | [`157f75139bb437328b9ca29632a152b6375b932b`](https://github.com/infoconex/dotnet-modernization/commit/157f75139bb437328b9ca29632a152b6375b932b) | Historical research branch |
| `research/exp040-native-document-provenance-20261105` | [`1c7f9896d23efb446a6bbc3e09aab31ceb76c22a`](https://github.com/infoconex/dotnet-modernization/commit/1c7f9896d23efb446a6bbc3e09aab31ceb76c22a) | Historical research branch |
| `research/exp041-original-compiler-inputs-20261105` | [`33e472cd514494c04376b78ed53d12f88a988ab2`](https://github.com/infoconex/dotnet-modernization/commit/33e472cd514494c04376b78ed53d12f88a988ab2) | Historical research branch |
| `research/exp042-csc-producer-provenance-20261105` | [`623da3486baf449a345421f854c8694c19dd3703`](https://github.com/infoconex/dotnet-modernization/commit/623da3486baf449a345421f854c8694c19dd3703) | Historical research branch |
| `research/exp043-five-production-pdbs-20261105` | [`d68a5be05b95007db20bbdb88d55773d7dfcbfdd`](https://github.com/infoconex/dotnet-modernization/commit/d68a5be05b95007db20bbdb88d55773d7dfcbfdd) | Historical research branch |
| `research/gate-cn-d1-synthetic-negatives-20261106` | [`627251e67832a7dc1c37a660e047d65db6455f86`](https://github.com/infoconex/dotnet-modernization/commit/627251e67832a7dc1c37a660e047d65db6455f86) | Historical research branch |
| `research/gate-cn-d2a-live-compiler-negatives-20261106` | [`9896a0450cc1f9b2e871e0370a0d7d04c14e46d0`](https://github.com/infoconex/dotnet-modernization/commit/9896a0450cc1f9b2e871e0370a0d7d04c14e46d0) | Historical research branch |
| `research/gate-cn-d2b-local-nuget-identity-20261106` | [`1b16327a10b7474b959054e1270a01924fc1dbfc`](https://github.com/infoconex/dotnet-modernization/commit/1b16327a10b7474b959054e1270a01924fc1dbfc) | Historical research branch |
| `research/gate-cn-design-validation-20261105` | [`ff503e0a42c46707206c03587f22f26604e983dd`](https://github.com/infoconex/dotnet-modernization/commit/ff503e0a42c46707206c03587f22f26604e983dd) | Historical research branch |
| `research/gate-cn-post-d2b-human-review-handoff-20261106` | [`8a663b60acd883235b5ec2eacd73f8bdddc18559`](https://github.com/infoconex/dotnet-modernization/commit/8a663b60acd883235b5ec2eacd73f8bdddc18559) | Historical research branch |
| `research/recordsift-option-a-first-modernization-proposal-20261106` | [`faa1fd91b07e6053b61799aba1067355bb8de022`](https://github.com/infoconex/dotnet-modernization/commit/faa1fd91b07e6053b61799aba1067355bb8de022) | Historical research branch |

## Retirement checklist

1. Verify [no open PRs](https://github.com/infoconex/dotnet-modernization/pulls) reference the candidate branch and confirm its exact head has not changed since this register.
2. Review documentation links (especially historical `tree/research/...` or `blob/research/...` URLs). Convert any links that must keep working to immutable commit SHAs. Do not silently rewrite the content or conclusions of historical reports.
3. Confirm the branch contains no additional required content missing from `main`, the inactive archive, or a stable external repository; retain this tip registry.
4. Delete retired branches through [GitHub Branches](https://github.com/infoconex/dotnet-modernization/branches) with owner authorization. **Do not delete `main`**. Verify after deletion.

The research state remains: **managed Gate C UNSATISFIED; native Gate C-N production NOT_AUTHORIZED; production Source Link HOLD**. The register does not authorize production release or modernization changes.
