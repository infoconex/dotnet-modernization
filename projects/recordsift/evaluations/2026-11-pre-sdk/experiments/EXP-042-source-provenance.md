# EXP-042 — Corroborate Csc effective source inputs and generated intermediate producer

**State:** PROPOSED / EXECUTABLE RESEARCH PROTOTYPE; no verified run yet. Tracked in [issue #68](https://github.com/infoconex/dotnet-modernization/issues/68), parent [#37](https://github.com/infoconex/dotnet-modernization/issues/37). Stacked research branch on unmerged EXP-041 PR #67. Frozen RecordSift `8358780829458854a4b0356df5ac5e685f0a34c8` unchanged.

## Inherited (do not redo)

EXP-041 verified Windows/Ubuntu 7/7 physical original byte checksum matches for seven native source records, against private pre-CoreCompile physical snapshots, with all frozen original/candidate 425 API, 419 NUnit (418 passed, one skipped), five XML, local NuGet and clean net48 consumer gates passing. Existing approved Gate C **UNSATISFIED**, Source Link production **HOLD**. EXP-041 repository-wide Windows synthetic test path normalization defect corrected on parent #67 and separate full validator workflow revalidated.

## New independent evidence families

**Csc task invocation:** Check the actual evaluated `CoreCompile` Csc task's `Sources` binding in the private MSBuild preprocessed project and separately inspect the *actual private diagnostic Csc task's* `Task Parameter:Sources` payload. Compare complete Windows-path-normalized source identities to the independently captured original seven `@(Compile)` physical inputs. Do not accept the latter alone as proof of the former. If MSBuild logs do not provide independently parsable task parameters, emit **INCONCLUSIVE**; never imply a match.

**Generated source producer:** A research-only import, restricted to the disposable candidate project, probes `GenerateTargetFrameworkMonikerAttribute`: its output is permitted only inside the project's `obj` tree and must be an AssemblyAttributes.cs file. The probe ensures the output was *absent* before the genuine target, then records its actual emitted output path and physical SHA256 privately after target completion. The independent verifier requires full normalized path identity with exactly one captured compiler input, the exact physical byte SHA256, and execution of a `WriteLinesToFile` task inside the real generation target's private diagnostic span. A stale preexisting source file, a matching filename, or an after-target callback without generator task execution is **not sufficient**.

## Security and regression controls

Only trusted compiler-created sources; PDB contents never treated as paths to open. All private diagnostic logs, source identities and physical bytes, producer records and preprocessed MSBuild XML remain ephemeral, never in public artifacts. Output only bounded categories, counts and Boolean relationships; no source names, digests, private pathmap or source bytes. Pre-/post-source and generator evidence cleaned under `finally`. Add synthetic missing/mismatched/duplicate/ambiguous task source, unsupported preprocessor binding, producer non-execution, stale output, altered bytes and wrong origin controls. Existing frozen original/candidate compatibility and 7/7 native PDB audit repeat as regression gates only; not a rerun of EXP-039 or EXP-040 fixtures.

**No production authority:** no application or main-branch writes; no merge, dependency upgrade, NuGet publication, native vulnerable reader execution or policy waiver. Authentic Visual Studio Package Manager project installation and live debugger stepping remain NOT TESTED. A new Gate C evidence pathway requires explicit stakeholder decision.

## Execution record

Pending run. Findings must be supported by a specific executing commit SHA, successful Windows and Ubuntu jobs and retained sanitized artifact.
