# Gate C-N — narrowly scoped live-adapter portability research

**Authority:** Stakeholder Option B (#72), design and isolated validation only. **Not an approved release gate.**
**Implementation:** `tooling/validators/gate_cn_live_provenance.py`. It does not replace the verified EXP-043 code or execute RecordSift.
**Original managed-reader checksum Gate C: UNSATISFIED. Gate C-N release acceptance: NOT AUTHORIZED. Source Link: HOLD.**

## Independent finding and bounded hypothesis

The verified EXP-043 verifier enumerates five hard-coded RecordSift components and directory layouts. More importantly, EXP-042's actual generated-source producer observation proves **exactly one** framework-moniker source per component, produced by the traditional MSBuild `GenerateTargetFrameworkMonikerAttribute` target and `WriteLinesToFile`. It does **not** prove arbitrary Roslyn generators, other intermediate files, external/untracked C# inputs or different Csc invocation patterns. A future generic gate must fail closed rather than silently treating those as authenticated by the moniker evidence.

**Hypothesis under research:** The already-executed original-source, native-DBI/C13, physical-byte, structured-Csc and generator verifiers can be driven using an externally supplied, reviewed component and trusted private evidence layout **without hard-coding RecordSift**, while rejecting unsupported inputs. This does not prove a live non-RecordSift PDB build works.

## Strict v1 research interface

The caller supplies `--manifest`, `--app-root`, `--evidence-root` and `--output`. The externally controlled JSON manifest requires exactly:

- `schema: gate-cn-live-manifest-v1`; `authorization: DESIGN_VALIDATION_ONLY`; exact GitHub `owner/repo`; 40-digit immutable application commit.
- Nonempty distinct component array (at most 32); each component has safe public `component`, `assembly_name`, relative `project_dir`, isolated relative `evidence_dir`, allowed `capture_dir`, externally expected native/checked-in/generated input counts, and `producer_contract: EXP042_MONIKER_ONE_PER_COMPONENT`.
- Exactly **one** generated compiler input per component, all other inputs Git-tracked; no unidentified, external or untracked inputs. That restriction is intentional, not a universal property of native PDBs. Counts and component universe must be approved independently before the build; do not derive them from the PDB.
- Real separate `bin/Release/<assembly>.dll/.pdb`, captured private physical input snapshots with exact path mapping, MSBuild preprocessed XML, real structured Csc task-event file, diagnostic task log and private producer attestation. All are read under approved confined roots.
- Git HEAD and tracked worktree must match immutable manifest commit; Git origin must be exactly the declared GitHub repository. Evidence directory must be separate from the source tree. No credentials/paths are emitted.

The adapter reuses verified primitive implementations from EXP-041/042/043, **not an independently written source checksum reader**. It compares full native named/DBI/C13 keys, digest bytes against privately snapped original compiler sources, full observed Csc source identities, a separately witnessed original producer execution and unchanged post-Csc physical bytes. The adapter additionally blocks extra generated inputs, unknown origins, mismatched externally declared source counts, malformed/traversing/duplicate paths, missing/oversize local binary/logs, and nonmatching Git roots.

Every component fails closed on any unrecognized error. The sanitized result is either `SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED` or `INCOMPLETE_RESEARCH_ONLY`; it always marks `gate_cn_release_acceptance=NOT_AUTHORIZED`, existing checksum Gate C `UNSATISFIED`, and Source Link production `HOLD`. It **does not** run the full API, test, package or consumer compatibility gates, audit a hostile PDB, or independently evaluate managed reader checksum support.

## Synthetic non-RecordSift controls and evidence ceiling

Isolated fixture uses public fictitious assembly `AnotherLibrary.Core`, 1 tracked source and 1 generated `obj` file, real private captured source bytes, original SHA256 comparisons, real Csc task event parsing and producer-output checks. **The fixture mocks `source_pdb_inventory` and origin classification**; its PE/PDB files are dummy placeholders. This demonstrates adapter wiring and fail-closed policy, **not PE/PDB parsing or live non-RecordSift Windows compilation**.

Target negative controls: changed post-Csc physical byte; wrong injected source digest; native DBI identity mismatch; altered structured Csc input; missing producer execution; generated-byte mismatch; external source; absent captured snapshot; missing binary; wrong generator contract; extra/no generated inputs; untrusted relative paths, symlink escapes, duplicate projects or evidence roots; invalid JSON and unauthorized policy promotion. Dedicated GitHub Actions research job runs these without recompiling EXP-041–043.

**Future live acceptance requires separate execution** on an independently approved non-RecordSift or otherwise genuinely different fixture, with the real native parser (not mocks), controlled source capture/producer execution, original/candidate compatibility requirements and a second independent reviewer. Unrecognized generators, multiple generated files, nonstandard Csc, alternate PDB layouts, external inputs and hostile PDBs must remain **BLOCKED** pending explicitly scoped independent work.

## Retention and independent replay decision

Existing authentic EXP-043 artifact **13482117590**, ZIP SHA256 `5efcc9b1c872f85c926eeef4819135a2325d97668b2abdcdde4e21f4b7e14443`, expires **2026-12-06 UTC**. Once expired, an artifact-dependent replay of original report bytes cannot claim success. An externally signed or separately reviewer-approved durable bundle of **only independently allowlisted sanitized aggregate reports**, manifest/schema, toolchain pins, workflow identity and ZIP digest is a feasible approach, but it has **not been created or authenticated as a durable replay archive**. The existing original GitHub execution record will remain an historical citation, not an independently downloadable source-byte witness after expiration.

Before accepting ongoing release enforcement, choose and implement a controlled archival custodian and independent review of sanitized bytes and their SHA256, plus a documented fresh-build re-execution procedure. Do not upload source files, private URLs, full document keys/hashes, PDBs or raw Csc events to make archival easier. A durable *sanitized* bundle cannot independently regenerate original physical-source proof without rerunning the trusted original compilation.

## Decision boundary

This adapter is **research instrumentation**, not a second live application case study or general release gate. Its schema is deliberately narrow. Research CI success can establish fixture controls and contract correctness only. Gate C-N production/release acceptance, retirement/replacement of original checksum Gate C, package publication, genuine Visual Studio NuGet project install and debugger/source retrieval all require independent explicit decisions. No merge or application/main modification is authorized here.
