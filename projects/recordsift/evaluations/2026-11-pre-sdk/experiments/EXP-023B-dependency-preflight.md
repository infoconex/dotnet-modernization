# EXP-023B — Source Link net48 dependency preflight (research-only)

**Status:** Proposed for independent Windows/Ubuntu read-only CI verification. Do not treat this as installed, built, or symbol-verified Source Link.

## Frozen application baseline

Repository: `infoconex/RecordSift`; immutable commit `8358780829458854a4b0356df5ac5e685f0a34c8`; traditional non-SDK `src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj`; `packages.config`; Release `DebugType=pdbonly`.

The original CSV package list has nine entries, including `System.Buffers 4.5.1` and `System.Memory 4.5.5`.

## Preflight design

1. Fetch exact official NuGet archives, pin and verify SHA-256 before inspection. Never import or execute archive targets.
2. Use the repository's existing `tooling/validators/nuget_build_assets.py` to reject malformed archives and record full import/asset inventories.
3. Select only the applicable legacy .NET Framework dependency group (not net8/net10).
4. Compare the metadata dependency closure against the nine original `packages.config` pins. Reject unresolved or ambiguous ranges and any baseline package replacement.
5. Expect a **BLOCKED** metadata-only verdict with precisely two version conflicts: `System.IO.Hashing 10.0.14` requires `System.Buffers >=4.6.1` and `System.Memory >=4.6.3`, whereas RecordSift pins 4.5.1 and 4.5.5 respectively.
6. Record the actual build-task tool files separately from runtime/library assets; the presence of `tools/netframework` files does not prove MSBuild load isolation.
7. Preserve metadata and tests in CI artifacts, with no binaries uploaded and no package publish.

## Evidence already established

EXP-023A read-only package audit: [draft PR #38](https://github.com/infoconex/dotnet-modernization/pull/38), [CI 41934257221](https://github.com/infoconex/dotnet-modernization/actions/runs/41934257221). Original audit passed Windows and Ubuntu with ten pinned official archives; archived asset inventory JSON agrees cross-platform. An independently staged validator passed 24 synthetic tests and replayed retained data locally, but the EXP-023B CI and application integration have not yet run.

Source Link 10.0.403 has packaged `tools/netframework` binaries. Those files are a **hypothesis** for build-time host isolation, not proof. Conventional NuGet installation can still alter compile/runtime references, including via the distinct `System.IO.Hashing lib/net462` asset. Do not install automatically into RecordSift.

## Evidence boundaries

- **Metadata-only preflight pass** means the expected version conflicts were detected accurately. It is **not** a Source Link compatibility pass.
- No RecordSift project, main branch, or NuGet release may be changed. Keep research PR draft and stacked on EXP-023A until stakeholder approval.
- Later work must prove actual legacy install and import semantics, task-module load locations, Windows PDB Source Link JSON and file checksums, exact immutable Git SHA, API baseline 425, 419 NUnit tests (418 pass/1 skipped), five XML docs, package/consumer acceptance, and reproducibility.
- Structural Windows PDB Source Link inspection must not require `srcsrv`; Source Link data and Source Server data are distinct.
- Preserve failed runs and negative controls as evidence, without reclassifying tooling/API failures as application failures.

## Sources

- [Issue #37](https://github.com/infoconex/dotnet-modernization/issues/37) — ongoing design and actual scope.
- [EXP-023A original evidence](EXP-023-source-link-asset-audit.md).
- https://www.nuget.org/packages/Microsoft.SourceLink.GitHub/10.0.403
- https://www.nuget.org/packages/System.IO.Hashing/10.0.14

## Actual GitHub Actions verification — pinned official archive preflight

**CI outcome:** VERIFIED **metadata-only preflight**, not Source Link installation. Exact research commit `fc76bc62ef994bdb53102ec605951ac90fcbf592` passed [Windows 2022 and Ubuntu 24.04 workflow 41964624233](https://github.com/infoconex/dotnet-modernization/actions/runs/41964624233). The [full reusable-tooling workflow 41964624171](https://github.com/infoconex/dotnet-modernization/actions/runs/41964624171) also passed both platforms at the same commit.

| Evidence | Windows 2022 | Ubuntu 24.04 |
| --- | --- | --- |
| Read-only archive integrity and hashes | PASS | PASS |
| 14 synthetic metadata fixtures | PASS | PASS |
| RecordSift immutable SHA and 9 package pins | PASS | PASS |
| Real nuget.org selected net48 graph: 4 package nodes, 6 edges | PASS | PASS |
| Exactly 2 expected `BLOCKED` edges, no unresolved/overlap | PASS | PASS |
| Metadata artifact | [13386099464](https://github.com/infoconex/dotnet-modernization/actions/runs/41964624233/artifacts/13386099464) | [13386976834](https://github.com/infoconex/dotnet-modernization/actions/runs/41964624233/artifacts/13386976834) |
| Artifact ZIP SHA-256 | `66624e9a9d8b3cacc57b6b8297ae9bec842c37c3e1ef24fab5ff52c925bca8dd` | `4d77a0d7d11a3cc9b1e6df27c03f78472e5e8dadd43ebed43ebb33d56168e87b` |

The retained `exp023b-dependency-preflight.json` and `exp023b-package-assets.json` files were downloaded and independently compared: each report is **structurally identical across Windows/Ubuntu**. The real selected dependency edges were:

- GitHub 10.0.403 → Build.Tasks.Git 10.0.403, Common 10.0.403, System.IO.Hashing 10.0.14 (all satisfied).
- Build.Tasks.Git 10.0.403 → System.IO.Hashing 10.0.14 (satisfied).
- System.IO.Hashing 10.0.14 → System.Buffers >=4.6.1 (**RecordSift 4.5.1: conflict**).
- System.IO.Hashing 10.0.14 → System.Memory >=4.6.3 (**RecordSift 4.5.5: conflict**).

There were no unresolved dependency edges, no baseline tool-package overlaps, and no change to the frozen RecordSift source. Archive inputs were verified against the fingerprints retained from EXP-023A. Artifacts are retained for 30 days. No executable package DLL was loaded, no Source Link targets imported, no PDB generated or inspected, no project files changed, no package published, and no full application release/consumer gates executed as part of EXP-023B.

**Next scope (separate research gate):** Determine actual MSBuild task load and isolation using a disposable single-project Windows build (including compared application dependency references, bin outputs, and final .nuspec), then inspect native Windows PDB Source Link JSON, source checksums and exact Git provenance; only afterward perform full historical compatibility gates. The two metadata conflicts do **not** prove that a separately hosted task assembly can never run; bundled tool DLL presence alone does **not** prove safe isolation.
