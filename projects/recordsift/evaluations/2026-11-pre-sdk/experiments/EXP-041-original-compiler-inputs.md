# EXP-041 — Original physical compiler-input authentication (frozen CSV PDB)

**Status:** PROPOSED / IMPLEMENTED ON ISOLATED RESEARCH BRANCH; NOT YET VERIFIED BY CI. Existing Gate C **UNSATISFIED**, Source Link production **HOLD**.

Tracking [#66](https://github.com/infoconex/dotnet-modernization/issues/66), parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37), predecessor [EXP-040 draft PR #65](https://github.com/infoconex/dotnet-modernization/pull/65). Research branch stacks on #65, does not modify `main` or frozen RecordSift commit `8358780829458854a4b0356df5ac5e685f0a34c8`. No NuGet publishing, dependency upgrades or policy waiver.

## Evidence inherited, not redone

EXP-040 [verified executing-code CI #42159910996](https://github.com/infoconex/dotnet-modernization/actions/runs/42159910996): seven independent DBI and C13 source identities, seven supported named native source streams with SHA256, eight C13 records all algorithm NONE (one duplicate), four reader-visible/line-referenced documents, three additional independently native-referenced documents without line blocks; **4/7** original physical compiler-input bytes verified. Full original/candidate 425 API, 419 NUnit (418 pass/one skip), five XML, local unpublished package and clean net48 consumer passed. Native source digest by itself does **not** prove independently supplied bytes.

## Isolated hypothesis and test

The frozen CSV traditional csproj declares six source items. Source-item lists in source control alone do not prove inputs consumed in the actual candidate build, and a generated framework-moniker source could also be included. Capture the **actual evaluated `@(Compile)` immediately before `CoreCompile`** and the contemporaneous `$(PathMap)` by importing `CompilerInputSnapshot.targets` only in the disposable temporary CSV csproj during the existing EXP-024 candidate build. The import is opt-in (`-CaptureCompilerSources`) and removed by the existing `finally` restoration. Inline RoslynCodeTaskFactory writes a private, numbered source identity/byte snapshot and SHA256 manifest outside the checkout. A post-`CoreCompile` task compares sources and snapshots byte-for-byte by SHA256, detecting changes during the compile window. This is *not yet* a complete effective-csc-argv capture: the MSBuild Csc source task parameter must be independently compared to the pre-target item list before claiming exact compiler source coverage.

The standalone Python verifier reads only separately captured paths and snapshots, never opens files named by native PDB keys, checks PE/PDB CodeView GUID+age and seven native injected-source records, requires complete normalized identity agreement between named source, DBI File Info and C13 FILECHKSMS source families, maps private captured source identities through the independently captured full prefix PathMap, rejects collisions, and compares the source snapshot's exact BOM/CRLF physical bytes with the native SHA256 digest (or separately supported SHA1). Reports counts and origin evidence categories only. `git ls-files` may independently corroborate a file's checked-in identity; a path under `obj` is only intermediate-location evidence, NOT proof of generator provenance.

**Privacy:** All private paths, map contents, raw originals, manifest, binaries, PDB and native digest bytes remain in ephemeral runner-local storage and are excluded from the artifact. The capture directory is erased in `finally` during independent audit. Diagnostic build logs stay private, never uploaded. Output contains only counts, fixed categories, and explicitly unchanged Gate C and Source Link policy states. Trusted compiler-produced PDB only, not hostile-input safe.

**Potential limitations:** The `BeforeTargets=CoreCompile` item set might differ from the effective Csc `Sources` task argument due to target ordering, dynamic items, compiler-generated inputs or embedded path remapping; that is a required corroboration before calling any result independently complete. A source with `#line` or generator virtual document names may not correspond to a physical compiler input. Missing mapping yields INCOMPLETE or fail-closed rather than invented matches. Full five-production-assembly expansion is conditional on an independently credible CSV result.

## Verification and acceptance protocol

- Ubuntu: synthetic source-path/prefix mapping, same-basename disambiguation, BOM/CRLF, missing bytes, stale content, duplicate IDs, algorithm mismatch, unrelated inputs and DBI/C13 identity negative controls.
- Windows: frozen original and candidate EXP-024 release/consumer gates **retained**. An independent pre-/post-`CoreCompile` physical capture and bounded stdlib native PDB audit runs against the actual candidate CSV PDB, leaving no private data in artifact.
- Review the running workflow and its retained sanitized evidence. If seven original-source inputs and byte digests match, classify their origins only by independently established source identities. If not, preserve missing input and parser findings without relaxing the gate.
- Do not independently declare Gate C satisfied on the basis of the standalone native audit, even if 7/7 bytes eventually match. Managed-reader checksum API exposure remains a separately unsatisfied contract; authentic Visual Studio project package installation and live debugger stepping remain NOT TESTED. Any alternative Gate C evidence pathway, full app scope, merge, or production adoption needs explicit stakeholder approval.

### Execution record

Pending actual EXP-041 CI run. No implementation, test pass, or native 7/7 claim is established by this draft alone.
