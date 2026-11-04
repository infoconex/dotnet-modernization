# .NET Modernization

Evidence-driven investigation and modernization of existing .NET applications. This repository holds the **methodology, evidence, decisions, and roadmaps** used to evaluate technical changes before they are implemented.

An evaluation is not an upgrade: a successful experiment proves a narrowly defined result under a documented environment. Changes to application source, production pipelines, and releases remain in the application repository and require their own approval and verification.

## Navigate

- [Methodology](methodology/README.md) — how to assess applications and grade evidence consistently.
- [Projects](projects/README.md) — individual applications, each with independent, dated evaluations.
- [Research](research/README.md) — generalizable modernization knowledge, linked to original evidence.
- [Validation tooling archive](tooling/README.md) — preserved experiment workflows, provenance and a safe route to future reusable validators.
- [Articles](articles/README.md) — mapping technical evidence to future articles, without mixing publication drafts into research.
- [Templates](templates/) — lightweight starting points for future assessments and experiments.

## Start an evaluation (human or AI)

Begin at [the evaluation process](methodology/evaluation-process.md#start-here-first-contact-protocol). Inspect the application and existing evaluations **before** interviewing. **For a new evaluation**, record stakeholder choices and obtain explicit approval of a consolidated scope before running investigations. **To resume an existing evaluation**, first verify its recorded scope, approval, progress and outstanding issues; reuse authorization that still applies rather than repeating the interview. The linked methodology is authoritative for issue tracking, experiment safeguards, documentation and completion. Repository-specific AI entry points are pointers, not separate copies of these rules.

## First evaluation

[RecordSift — November 2026 pre-SDK modernization discovery](projects/recordsift/evaluations/2026-11-pre-sdk/README.md)

The RecordSift evaluation examines low-risk improvements to ten traditional .NET Framework 4.8 projects before SDK-style conversion. The original application repository is [infoconex/RecordSift](https://github.com/infoconex/RecordSift).

## Operating principles

1. Record the **application repository, branch, and complete commit SHA** for each baseline and experiment.
2. Separate **general research** from **project-specific observations**.
3. Distinguish **finding** (what was observed), **decision** (what to do), and **implementation** (what was changed).
4. Record negative results and unexecuted checks as carefully as successes.
5. Prefer reproducible commands and immutable tool/image identifiers; keep historical baselines immutable.
6. Run full compatibility gates when configuration changes could affect behavior.
7. Do not publish artifacts, change an application's main branch, or claim a recommendation was implemented because it was experimentally feasible.

Use [the evaluation lifecycle](methodology/evaluation-process.md) to start another project.
