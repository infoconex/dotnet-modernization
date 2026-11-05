# EXP-031 — Native Windows PDB managed document checksum verification

**Status:** Experimental — only declare verified after independent Windows CI. Stacked on EXP-030, not main. Frozen RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8`.

## Objective

Determine whether the classic Windows PDB emitted by a traditional C# 7.3/net48 project contains cryptographic source-file document checksums matching the exact physical Windows source bytes compiled. EXP-029 independently inspected the PDB using LLVM, whose file list displayed “(no checksum)”. That is an observation, not definitive proof of absent managed PDB checksum records.

## Independent reader

An isolated **net10.0-windows** console process uses Microsoft.DiaSymReader and a security-reviewed patched Microsoft.DiaSymReader.Native package. The tool is **not referenced or installed into RecordSift**. Re-run official NuGet audit before use and fail if any unsafe tool dependencies are reported. It enumerates documents through native `ISymUnmanagedReader3`, obtains `ISymUnmanagedDocument` URL, checksum algorithm GUID and checksum bytes, matches known SHA1/SHA256 GUIDs, hashes the source file **as physically compiled** on Windows and requires all records to match. A selected owned CSV importer file must be present. It detects duplicate documents, unsupported URL/path inputs and source escapes.

Seven deterministic positive/negative checksum-matching controls run before actual PDB inspection (correct SHA1/SHA256, algorithm confusion, unknown algorithm, empty digest, altered source bytes and altered checksum). Actual application source must pass original 425 public API, all 419 NUnit (418 pass / 1 skip), five XML, local unpublished package, clean .NET Framework consumer and logical compatibility gates. Native MSF7 PDB, embedded Source Link mapping and PE CodeView GUID+age also verified by EXP-025 independent reader.

## Evidence and boundaries

Preserve only small JSON metadata: per-document relative path, algorithm, digest length, input length and equality; never upload PDBs, assemblies, raw source, passwords, NuGet binaries or binlogs.

**Positive result:** each native document record's SHA1 or SHA256 matches the actual compiler input bytes, and negative controls pass. A green workflow alone is not sufficient; inspect evidence JSON and confirm all expected fields.

**Negative result:** distinguish actual missing checksums, unsupported algorithm, unsupported PDB reader, missing native DLL and harness compilation faults. Never classify a tool error as a product defect. Do not infer that Git LF blob is the compiler input when Windows checkout contains CRLF.

Even a positive checksum result does **not** demonstrate interactive Visual Studio debugger stepping, conventional Visual Studio NuGet project installation, or MSBuild host-module isolation. All are separately tracked in [issue #37](https://github.com/infoconex/dotnet-modernization/issues/37).

References: [EXP-029](EXP-029-pdb-document-checksums.md), [EXP-028](EXP-028-remote-source-proof.md), https://source.dot.net/Microsoft.DiaSymReader/Extensions/SymUnmanagedExtensions.Document.cs.html .

## Actual patched-reader security availability gate

**Reproduced blocked outcome:** [EXP-031 run 41980900376](https://github.com/infoconex/dotnet-modernization/actions/runs/41980900376) at SHA `4ca2904f5dffd17a11de9fd4f39a50fed8ac752b` **failed closed on the security preflight**, before executing a native PDB package. The retained [artifact 13393498140](https://github.com/infoconex/dotnet-modernization/actions/runs/41980900376/artifacts/13393498140), ZIP SHA256 `246affdb9a20217653a7a8ee0a3d3e7ccd06625171cc23379698cc308d1249ab`, independently downloaded and inspected. JSON records `BLOCKED_PENDING_PATCHED_PACKAGE_AVAILABILITY`, required version `Microsoft.DiaSymReader.Native 18.9.0-beta1.26405.2`, `available=false`, and latest public nuget.org version `18.8.4-beta1.26356.2`. The original preflight run [41980647813](https://github.com/infoconex/dotnet-modernization/actions/runs/41980647813) failed NU1102 for the unavailable pinned safe package. No older vulnerable fallback was installed or executed.

**Classification: BLOCKED (security-dependent tool availability), NOT application failure and NOT checksum verification.** The checked-in managed reader remains a **proposal**, not compiled and not verified by CI. It may require compiler/API corrections after the patched package becomes public. The original EXP-029 LLVM observation `(no checksum)` is still the only executed independent document-inventory evidence. Do not recommend production Source Link based on a claim of verified PDB document hashes.

Relevant Microsoft advisories: [CVE-2026-69522](https://github.com/dotnet/runtime/security/advisories/GHSA-2j8r-3c22-8565), [CVE-2026-71328](https://github.com/dotnet/runtime/security/advisories/GHSA-63gh-g2x5-x69v), [CVE-2026-69439](https://github.com/dotnet/runtime/security/advisories/GHSA-527h-q9f6-p7qx). Re-evaluate using an independently patched, verifiable native PDB reader later rather than weakening this gate.
