# EXP-041 — Original physical compiler-input authentication (frozen CSV PDB)

**Status (November 5, 2026): VERIFIED 7/7 ORIGINAL PHYSICAL NATIVE-PDB SOURCE DOCUMENT BYTES FOR FROZEN CSV CANDIDATE; ONE INTERMEDIATE INPUT PRODUCER UNVERIFIED.** Existing Gate C **UNSATISFIED**, Source Link production **HOLD**.

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

### Verified executing-code workflow and evidence

**Final code execution:** [GitHub Actions 42162017966](https://github.com/infoconex/dotnet-modernization/actions/runs/42162017966), SHA `760fa7e87c23a17a79337ca112b3eff23b7167e4`. **Ubuntu and Windows PASS.** Ubuntu **13/13** new controls pass. Frozen Release original and manually isolated candidate **425 public API, 419 NUnit discovered / 418 passed / 0 failed / one expected skipped, five XML documents, unpublished local NuGet package, clean installed net48 consumer and five logical compatibility categories PASS**. The original packages.config and frozen application Git HEAD remain unchanged, and no research/application main merge or publication occurred.

**Sanitized independent artifact:** `exp041-sanitized-original-input-audit`, ID `13477690414`, GitHub artifact ZIP digest `sha256:60ca39e2f5696be5e509edceb0917d663d91002e487c0fe7453a39422e537823` (30-day retention). Source paths, full original bytes, native checksum values, raw PDBs, application binaries, private source identity map, and diagnostic MSBuild logs were excluded. The private source snapshot was deleted in the Windows job's `finally`.

**Authentic source bytes:** The isolated frozen CSV project's seven `@(Compile)` physical input files were captured immediately before `CoreCompile` and successfully byte-hash-compared after compile. The native Windows PDB PE CodeView signature, DBI and C13 named-document sets agreed for all seven. All **7/7** original captured physical compiler-input bytes matched the corresponding native named `/SRC/FILES/` checksums, with **0 missing**. All eight separate C13 checksum entries remain algorithm `NONE`, so only named streams supply digest values; the original snapshots authenticate them independently. The full compiler effective argv/task `Sources` parameter was not separately replayed; this proof is restricted to the seven native document identities matching the captured `@(Compile)` list and not an assertion that no other compiler virtual/document inputs could exist.

**Source-origin evidence:** Six out of seven captured input identities independently matched Git-tracked files. One source appeared in an intermediate directory and is categorized `intermediate_location_producer_unverified`; this is **not yet independent proof of its generator or target execution**. Among the three formerly unmatched native documents independently identified in EXP-040 as lacking C13 line references and managed-reader exposure, the sanitized opaque identity classifications are:

| Opaque EXP-041 identifier | Independently evidenced origin | Exact physical checksum |
|---|---|---|
| `native-no-line-1` | `checked_in` | MATCH |
| `native-no-line-2` | `intermediate_location_producer_unverified` | MATCH |
| `native-no-line-3` | `checked_in` | MATCH |

The opaque order is defined by normalized native identities privately and does not disclose names. This validates all three additional native-referenced documents' original byte digests, while refusing to invent an unproven producer.

**Preserved failure history:** [42161613718](https://github.com/infoconex/dotnet-modernization/actions/runs/42161613718) revealed two synthetic verifier defects (prefix separator duplication and unsupported hash algorithm only checked when bytes present). After both were corrected, [42161953501](https://github.com/infoconex/dotnet-modernization/actions/runs/42161953501) achieved the first **7/7** native byte result but the later opaque origin breakdown was not yet in that executing code. [42162017966](https://github.com/infoconex/dotnet-modernization/actions/runs/42162017966) is the final accepted run including origin categories and all 13 controls. Intermediate Windows failure `INVALID_CAPTURE_PATHMAP` was a parser assumption about leading/trailing MSBuild mapping separators; corrected with fail-closed mapping validation. These were research harness failures, not application regressions.

**Release/governance:** Native source-document byte coverage for this one frozen CSV candidate is now **7/7**. Existing managed-reader checksum disclosure is still **0/4**, and no stakeholder-approved alternate Gate C evidence pathway exists. Therefore **Gate C UNSATISFIED, Source Link HOLD**. No Visual Studio Package Manager **project installation**, source retrieval, or real debugger source stepping was established. Do not claim this workflow validates all five production PDBs or grants production acceptance.

### Residual research and decision boundary

1. Independently corroborate the effective `Csc Sources` task parameter/argv with the private pre-target snapshot; avoid overclaiming complete compiler invocation solely from `@(Compile)`.
2. Attribute the intermediate input to an actual generating target/tool only using separately observed producer evidence. Its byte digest already authenticates; its origin remains unknown.
3. Consider broader all-five-production-assembly native source coverage only after scoped validation justification, a new isolated experiment and preserved original gates.
4. Any alternative standalone native-checksum Gate C pathway, Source Link adoption, merger or publication requires **explicit stakeholder approval**. Keep #66 and draft PR #67 open until review.

