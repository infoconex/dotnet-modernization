# Retired RecordSift research-repository workflows

These **31 historical GitHub Actions workflow source files** were formerly under `.github/workflows/` in `infoconex/dotnet-modernization`. They belong with the [dated RecordSift evaluation](../../README.md) and its [experiment reports](../../experiments/README.md), not with generic validation code. They are separate from the [previously retained original RecordSift application workflow snapshots](../README.md).

All 31 YAML files retain their **exact original Git blob identities**, including historical `pull_request` and `workflow_dispatch` declarations, now inert because the files are outside `.github/workflows/`. They are not generic CI templates. Historic runs provide the recorded evidence; archived source has not been rerun here.

| Experiment | Original workflow | Git blob SHA |
| --- | --- | --- |
| EXP-024 | [`validate-exp024-windows-sourcelink-import.yml`](validate-exp024-windows-sourcelink-import.yml) | `731652602910930833605c3e631a3dfc6bd5751b` |
| EXP-025 | [`validate-exp025-native-pdb.yml`](validate-exp025-native-pdb.yml) | `714fdca767b3240885351e834f98353ffe1bf852` |
| EXP-026 | [`validate-exp026-two-source-worktrees.yml`](validate-exp026-two-source-worktrees.yml) | `210889abe8e49a0993dacf3d77e8752b80d912fc` |
| EXP-027 | [`validate-exp027-nuget-closure.yml`](validate-exp027-nuget-closure.yml) | `59cdfa585f77110769a26e38da517e1718596578` |
| EXP-028 | [`validate-exp028-remote-source.yml`](validate-exp028-remote-source.yml) | `ceaf0b1e2e76ca7463d626395ba62690d49b226b` |
| EXP-029 | [`validate-exp029-pdb-document-checksums.yml`](validate-exp029-pdb-document-checksums.yml) | `00a273b11718b4b9a184a45be642308f4ad4824d` |
| EXP-030 | [`validate-exp030-git-topology.yml`](validate-exp030-git-topology.yml) | `50c6e94008c3df3b42f825df0ccc1a5a993c5d6f` |
| EXP-032 | [`validate-exp032-task-module-bindings.yml`](validate-exp032-task-module-bindings.yml) | `6541195314d28aa33f0f7ad8dcc208ce10af8a6d` |
| EXP-033 | [`validate-exp033-native-c13.yml`](validate-exp033-native-c13.yml) | `5773f2eb09a8ed6258f1cb7c415d12c49bffdc30` |
| EXP-034 | [`validate-exp034-all-pdb-owned-sources.yml`](validate-exp034-all-pdb-owned-sources.yml) | `32deb6fd5c3e96cde1297e1fb9a0cc831bae2dcf` |
| EXP-035 | [`validate-exp035-dia-sdk.yml`](validate-exp035-dia-sdk.yml) | `17fbe9e30d3aefa6847e23b354d4e96b2be6051c` |
| EXP-036 | [`validate-exp036-frozen-csv.yml`](validate-exp036-frozen-csv.yml) | `7e272146f9f26968955bbfa5877942ddc78d7c6f` |
| EXP-036 | [`validate-exp036-managed-fixture.yml`](validate-exp036-managed-fixture.yml) | `f285415d7fb7df2764d1a8ffecec21e5f242fcd5` |
| EXP-036 | [`validate-exp036-reader-preflight.yml`](validate-exp036-reader-preflight.yml) | `9a306c94e440a6a9a70d5f1a242ae83c1a3dac50` |
| EXP-037 | [`validate-exp037-compiler-pdb.yml`](validate-exp037-compiler-pdb.yml) | `9367cc48f744cb27034df0ea4d1f619f7137558b` |
| EXP-038 | [`validate-exp038-document-key.yml`](validate-exp038-document-key.yml) | `3ea9a47c7bd57dadc9e912ce837e840224d6fa8a` |
| EXP-039 | [`validate-exp039-reusable-pdb-checksums.yml`](validate-exp039-reusable-pdb-checksums.yml) | `7041a9d2183b7e0cbc2c88ce530380fe482f3a45` |
| EXP-040 | [`validate-exp040-native-document-inventory.yml`](validate-exp040-native-document-inventory.yml) | `e31cfedc72d17a84d136e68aefc9c90e85ea19cf` |
| EXP-041 | [`validate-exp041-original-inputs.yml`](validate-exp041-original-inputs.yml) | `0b8ea701daa1345e38de976411eaf17a86f870a3` |
| EXP-042 | [`validate-exp042-source-provenance.yml`](validate-exp042-source-provenance.yml) | `ebe4757d825732edc4124e925b5729d2579c7926` |
| EXP-043 | [`validate-exp043-five-pdbs.yml`](validate-exp043-five-pdbs.yml) | `bcbfbf69ec34dda9b5d8ed9304af040356eca9ee` |
| EXP-021 | [`validate-recordsift-ci-property-only.yml`](validate-recordsift-ci-property-only.yml) | `9a081812a3cbb67e1bc9719efb16b0e651695dff` |
| EXP-019 | [`validate-recordsift-deterministic-isolation.yml`](validate-recordsift-deterministic-isolation.yml) | `6571edc62525429a9af8b98258aeb245b840fdcd` |
| EXP-015 | [`validate-recordsift-langversion-candidate.yml`](validate-recordsift-langversion-candidate.yml) | `9456f72b7dde82f4a1c308ffee1b7eeff8cdab6c` |
| EXP-022 | [`validate-recordsift-manual-sourceroot.yml`](validate-recordsift-manual-sourceroot.yml) | `9e55fa744b514dc31ce5849dcaa6bce729e68290` |
| EXP-014 | [`validate-recordsift-metadata-pilot.yml`](validate-recordsift-metadata-pilot.yml) | `1d48e803cd1c77b137e78cac9a3cf3e86454f674` |
| EXP-017 | [`validate-recordsift-package-payload.yml`](validate-recordsift-package-payload.yml) | `54533da2cf86d14165195a028b6d2b3821815bd5` |
| EXP-020 | [`validate-recordsift-pathmap-isolation.yml`](validate-recordsift-pathmap-isolation.yml) | `c38203e2cb6553b7917e30737c7474e200c35ec4` |
| EXP-018 | [`validate-recordsift-pe-reproducibility.yml`](validate-recordsift-pe-reproducibility.yml) | `89c3b277db2a83f06f7110478bf6bbdda726cb5b` |
| EXP-016 | [`validate-recordsift-source-api-regression.yml`](validate-recordsift-source-api-regression.yml) | `714bed95aac7a57d7aa79c83a7a03df0e306b2c1` |
| EXP-023B | [`validate-sourcelink-dependency-preflight.yml`](validate-sourcelink-dependency-preflight.yml) | `8b62d3b17bfcb54bc598bbd8c6289b03a939ca7b` |

To run again, obtain approval, copy/adapt the workflow onto a temporary research branch under `.github/workflows/`, validate all tooling/security assumptions and runner versions, and collect new evidence. Keep the archived original unchanged; copying does not establish equivalence with historic runs.
