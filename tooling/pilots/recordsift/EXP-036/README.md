# EXP-036 — managed Windows-PDB checksum feasibility (nonexecuting preflight)

**Status:** Research-only package preflight. **Not a checksum experiment or acceptance gate pass.**
**Issue:** [#54](https://github.com/infoconex/dotnet-modernization/issues/54), follow-up to [#37](https://github.com/infoconex/dotnet-modernization/issues/37) and [EXP-035](../../../../projects/recordsift/evaluations/2026-11-pre-sdk/experiments/EXP-035-dia-sdk-checksum-feasibility.md).
**Unchanged application baseline:** `infoconex/RecordSift@8358780829458854a4b0356df5ac5e685f0a34c8` (.NET Framework 4.8, C# 7.3, Windows `pdbonly`).
**Preflight input:** Official NuGet `dnlib` **4.5.0** and `Mono.Cecil` **0.11.6** archives, downloaded directly from the pinned version endpoints at `api.nuget.org`.

## Why this narrow follow-up exists

EXP-029 and EXP-033 read native LLVM file/checksum views; EXP-035 executed signed Visual Studio DIA **source-file table** inspection and independently verified 0/4 selected managed document checksums. The absence of file-table hashes in those views is **not** evidence that a Roslyn managed Windows PDB lacks `ISymUnmanagedDocument` checksums.

Upstream Roslyn Windows-PDB tests explicitly expect SHA1 source-document hashes. Two different managed source readers can potentially expose the relevant PDB records: dnlib's default managed reader and Mono.Cecil.Pdb's managed `NativePdbReader` (vendored CCI). Cecil and CCI are **one implementation family**, not independent confirmations. No successful RecordSift checksum extraction has been demonstrated yet.

## This phase — only archive metadata, no package execution

`nuget_reader_preflight.py` verifies exact nuspec ID/version, bounded ZIP entry layout and content size, archive/asset SHA-256, the minimum managed reader DLL assets, declared dependency groups, and absence of package install/build scripts. It rejects wrong identity, version, missing assets, unsafe paths, duplicate archive entries, large archives and install scripts; nine synthetic controls run offline before downloading actual packages. It **does not extract packages or load any reader binaries**. It does not claim malware-free packages, complete NuGet resolution, trust of nuspec authors, or vulnerability clearance. Authentic publisher/signature checks and current advisories require separate independent security review before execution.

The workflow downloads only two exact NuGet archives over TLS, runs the static scanner, and uploads only a small JSON metadata report (no package, binary, PDB or source). No actual application build/test suite is needed at this stage, and passing this workflow must not alter Gate C.

## Later work — NOT authorized or implemented by this preflight

After inspecting archive hashes, package assets and security advisories, create an isolated trust-reviewed C# 7.3/net48 Roslyn classic-PDB fixture. Independently check PDB/PE identity and SHA1/SHA256 actual compiler-input bytes, use both readers with managed mode explicitly selected and resource limits, and test source mutation, missing source, wrong PDB, and document coverage. Only a successful trustworthy fixture justifies investigating the existing disposable RecordSift CSV candidate's four selected owned source files. Do not silently reuse a native COM reader or upload symbols.

Keep separate the authentic Visual Studio Package Manager installation and real debugger stepping gates. **EXP-035 stays INCONCLUSIVE; EXP-031 remains SECURITY-BLOCKED; Source Link stays on HOLD.** No RecordSift source/dependency edits, merges, application release, or NuGet publication are part of this branch.
