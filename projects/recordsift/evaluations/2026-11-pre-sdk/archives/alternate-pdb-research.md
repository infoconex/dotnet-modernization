# Inactive alternate native-PDB research (EXP-029 and EXP-031)

These original source blobs were preserved from historical stacked draft heads without executing them. Source paths below are **inert archives**, not GitHub Actions workflows or part of the active validation toolkit.

## EXP-029 alternative C13 checksum parser — PR #45

Original research head: [b1ad2927d91f585eede12c9d41cf01df664e53a5](https://github.com/infoconex/dotnet-modernization/commit/b1ad2927d91f585eede12c9d41cf01df664e53a5).

| Archive file | Original path | Git blob SHA |
|---|---|---|
| [Original workflow](EXP-029/validate-exp029-pdb-checksum.yml) | `.github/workflows/validate-exp029-pdb-checksum.yml` | `de2bf4006ce9798aee27cc47f8746ba7b7cd99d7` |
| [Parser source](EXP-029/windows_pdb_document_checksums.py) | `tooling/validators/windows_pdb_document_checksums.py` | `fd7675193b12a384c282424aad34ddfb32e62f02` |
| [Parser tests](EXP-029/test_windows_pdb_document_checksums.py) | `tooling/validators/tests/test_windows_pdb_document_checksums.py` | `c2c73873462e13dbe496472dd482177cac2efe2f` |

[Original report](../experiments/EXP-029-c13-document-checksum.md) is historical and does not establish a successful new replay.

## EXP-031 patched managed PDB reader — PR #48

Original research head: [36bd8de35543aa1f41420d3f4bb9e25b52068666](https://github.com/infoconex/dotnet-modernization/commit/36bd8de35543aa1f41420d3f4bb9e25b52068666).

| Archive file | Original path | Git blob SHA |
|---|---|---|
| [Original workflow](EXP-031/validate-exp031-managed-pdb-checksums.yml) | `.github/workflows/validate-exp031-managed-pdb-checksums.yml` | `0214a9db0ac026db0e255043033f3aca6fe6a831` |
| [Project file](EXP-031/PdbDocumentHashes.csproj) | `tooling/validators/pdb-document-hashes/PdbDocumentHashes.csproj` | `93f5a8a6ba84f5b78bb14bcd3ad4176050b89010` |
| [Reader source](EXP-031/Program.cs) | `tooling/validators/pdb-document-hashes/Program.cs` | `c633f8b1bb2d1f2c44ed45ad69181c59bbe2a58e` |

[Original report](../experiments/EXP-031-managed-pdb-checksums.md) explicitly records a **BLOCKED** security preflight: the required patched `Microsoft.DiaSymReader.Native` package was not publicly available at the time. Never install a known-vulnerable fallback to make the experiment pass.

## Reuse rule

The archived YAML may contain original `pull_request` triggers, but no file here is under the active `.github/workflows/` directory. Original test scripts are not automatically discovered. Reproduction requires copying/adapting dependencies and paths into a disposable checkout, validating current package security and authorization, and separately verifying new run evidence. Preserve original blob contents and research conclusions unchanged.
