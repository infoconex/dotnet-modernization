# Evidence

[manifest.md](manifest.md) is the navigation and provenance index for the November 2026 RecordSift discovery.

Prefer immutable Git commit SHAs, container digests, exact commands, observed results and GitHub Actions run/artifact IDs. This repository deliberately does not vendor compiled DLLs, NuGet packages or full workflow logs.

**Retention:** GitHub Actions artifacts may expire. A permanent reproduction recipe and the critical observation should survive in the [experiment records](../experiments/README.md) even when an artifact is no longer downloadable. Avoid copying sensitive paths, tokens or authentication headers.

## Retained EXP-043 sanitized reports

- [Five-assembly native-source provenance audit](exp043-five-pdb-source-audit.json)
- [Managed PDB reader exposure report](exp043-managed-reader-exposure.json)

These two reports belong to the frozen RecordSift evaluation (five production assemblies), not to a reusable acceptance-gate standard. Their Git blob identities are unchanged from the initial Gate C-N research archive, and they remain **historical sanitized reports** only. They do not establish production approval or independently reproduce the original private compiler inputs. The cross-application [Gate C-N protocol and other-application research](../../../../../research/native-pdb-provenance/gate-cn/README.md) is maintained separately.
