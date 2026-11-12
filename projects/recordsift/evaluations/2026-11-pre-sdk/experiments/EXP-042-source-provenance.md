# EXP-042 — Corroborate Csc effective source inputs and generated intermediate producer

**State (November 5, 2026): VERIFIED structured Csc source inputs 7/7 and generated intermediate producer. Existing Gate C UNSATISFIED; Source Link HOLD.** Tracked in [issue #68](https://github.com/infoconex/dotnet-modernization/issues/68), parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37). Stacked research branch on unmerged EXP-041 PR #67. Frozen RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8` unchanged.

## Inherited (do not redo)

EXP-041 verified Windows/Ubuntu 7/7 physical original byte checksum matches for seven native source records, against private pre-CoreCompile physical snapshots, with all frozen original/candidate 425 API, 419 NUnit (418 passed, one skipped), five XML, local NuGet and clean net48 consumer gates passing. Existing approved Gate C **UNSATISFIED**, Source Link production **HOLD**. EXP-041 repository-wide Windows synthetic test path normalization defect corrected on parent #67 and separate full validator workflow revalidated.

## New independent evidence families

**Csc task invocation:** Check the actual evaluated `CoreCompile` Csc task's `Sources` binding in the private MSBuild preprocessed project and separately inspect the *actual private diagnostic Csc task's* `Task Parameter:Sources` payload. Compare complete Windows-path-normalized source identities to the independently captured original seven `@(Compile)` physical inputs. Do not accept the latter alone as proof of the former. If MSBuild logs do not provide independently parsable task parameters, emit **INCONCLUSIVE**; never imply a match.

**Generated source producer:** A research-only import, restricted to the disposable candidate project, probes `GenerateTargetFrameworkMonikerAttribute`: its output is permitted only inside the project's `obj` tree and must be an AssemblyAttributes.cs file. The probe ensures the output was *absent* before the genuine target, then records its actual emitted output path and physical SHA256 privately after target completion. The independent verifier requires full normalized path identity with exactly one captured compiler input, the exact physical byte SHA256, and execution of a `WriteLinesToFile` task inside the real generation target's private diagnostic span. A stale preexisting source file, a matching filename, or an after-target callback without generator task execution is **not sufficient**.

## Security and regression controls

Only trusted compiler-created sources; PDB contents never treated as paths to open. All private diagnostic logs, source identities and physical bytes, producer records and preprocessed MSBuild XML remain ephemeral, never in public artifacts. Output only bounded categories, counts and Boolean relationships; no source names, digests, private pathmap or source bytes. Pre-/post-source and generator evidence cleaned under `finally`. Add synthetic missing/mismatched/duplicate/ambiguous task source, unsupported preprocessor binding, producer non-execution, stale output, altered bytes and wrong origin controls. Existing frozen original/candidate compatibility and 7/7 native PDB audit repeat as regression gates only; not a rerun of EXP-039 or EXP-040 fixtures.

**No production authority:** no application or main-branch writes; no merge, dependency upgrade, NuGet publication, native vulnerable reader execution or policy waiver. Authentic Visual Studio Package Manager project installation and live debugger stepping remain NOT TESTED. A new Gate C evidence pathway requires explicit stakeholder decision.

## Execution record

Superseded by the verified execution record below.


## Final independently verified execution — November 5, 2026

**Final executing-code workflow:** https://github.com/infoconex/dotnet-modernization/actions/runs/42164989228
**Executing SHA:** 9c9396e8d78cbd38e498c6df4da94171eda76d10. Both Windows and Ubuntu jobs PASS. Seven new EXP-042 synthetic controls PASS, and the repository-wide reusable validator jobs PASS on Windows and Ubuntu.

**Real Csc Sources verified: 7/7.** The evaluated CoreCompile task declares Csc Sources from Compile items. A research-only custom MSBuild logger compiled against the active installed Microsoft.Build.Framework captured genuine structured TaskParameterEventArgs TaskInput/Sources events, correlated with the Csc task ID. Exactly seven source identities were received. Every normalized full identity matches the seven private, physical, pre-CoreCompile captured inputs; the post-CoreCompile byte-stability control also passes. Independently verified native PE/PDB, DBI/C13, and named structured source records match the exact physical input SHA256 values for all 7 of 7 documents, zero missing. All eight native C13 FILECHKSMS records still use checksum NONE; the cryptographic proof is from independently captured physical bytes and separate native named source digests.

**The earlier six-source observation was an incomplete diagnostic-text extraction**, not a missing Csc task source. Runs 42163547310 and 42163869879 failed closed using parsed diagnostic text; 42164248325 established OBS6_CAP7_OVERLAP6, with the intermediate identity missing from the parsable text task parameter region. Structured task-input events resolved the seven-source set independently. Preserve both evidence families and never upgrade textual ambiguity to a pass.

**Generated intermediate producer verified.** The research probe forced the allowed target-framework AssemblyAttributes output to be absent beforehand in the disposable CSV project, observed actual GenerateTargetFrameworkMonikerAttribute target and WriteLinesToFile task execution, and compared the resulting exact physical bytes and full path with the captured input. They matched. The other six compiler identities were independently corroborated as checked-in files. This supersedes the earlier producer-unknown classification for the frozen CSV candidate without rewriting historical EXP-041 evidence.

**Frozen compatibility retained:** RecordSift commit 8358780829458854a4b0356df5ac5e685f0a34c8, original and manually isolated candidate 425 public API entries, 419 NUnit discovered / 418 passed / one expected skipped, five XML docs, unpublished local package and clean installed net48 consumer, and five logical compatibility categories all PASS. No application code, packages.config, production dependency versions, main branch, NuGet publication, or research policy changed.

**Sanitized retained artifact:** exp042-source-provenance-sanitized, GitHub artifact ID 13478167890, ZIP SHA256 6e392453adb9f8be0d61c2827217bcae632af8d421e01c31ff6fd6a9a13b1eed, 30-day retention. Contains aggregate exp042-native-audit.json and exp042-provenance.json only. Final workflow adds unconditional cleanup of private source/producer manifests, structured Csc event evidence, diagnostic MSBuild log, preprocessed XML and research logger DLL. No raw source names/paths, PDBs, bytes, URLs or full original digests uploaded.

**Five perspectives:** build (active MSBuild structured task inputs and actual target execution); security (private ephemeral inputs and fail-closed controls); architecture (reusable isolated logger/validators and full normalized path association); quality (synthetic positives/negatives and full Windows/Ubuntu validator pass); release governance (all frozen release/consumer contracts intact; approvals unchanged). None establishes compiler-server virtual document internals or hostile-PDB parser safety.

**Approval remains unchanged:** unmodified managed readers expose 0/4 document checksums; existing Gate C UNSATISFIED; Source Link HOLD. Authentic Visual Studio Package Manager project installation, interactive source retrieval/debugger stepping, and other four production PDB physical-source audits remain NOT TESTED. Proposal issue #70 is the possible bounded EXP-043 follow-up; adoption/alternate Gate C evidence must receive explicit stakeholder approval. Leave draft PR #69 unmerged.
