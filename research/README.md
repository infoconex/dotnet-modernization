# Reusable modernization research

This area collects generalizable guidance after it has been validated or tied to primary-source documentation. It is **not** a duplicate of a project experiment.

A research note should state the general mechanism, applicable project formats and tool versions, important limitations, verification date, primary-source links, and links to underlying application experiments.

Initial candidates from RecordSift:

- MSBuild import order and conditional shared-property defaults.
- Traditional projects with Directory.Build.props and Directory.Build.targets.
- Building .NET Framework 4.8 with SDK-provided MSBuild on Windows.
- Difference between Visual Studio IDE, Visual Studio Build Tools, targeting packs, runtime, and SDK.
- packages.config versus PackageReference; when Directory.Packages.props becomes applicable.
- Controlling SDK selection with global.json.

Add individual notes only when there is enough reusable content to justify them. See [RecordSift findings](../projects/recordsift/evaluations/2026-11-pre-sdk/findings.md) for the first observed evidence.

## Cross-application research investigations

- [Native classic-PDB source provenance and Gate C-N](native-pdb-provenance/README.md) — scoped, historical research involving RecordSift and an independent .NET Framework compilation. Not an approved production release gate.
- [Historical research and branch records](history/README.md) — preserved inventories and original decision context.

- [Source Link package build-asset research archive](source-link-build-assets/README.md) — one-off read-only NuGet asset audit, now inert.
