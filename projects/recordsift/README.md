# RecordSift

Application repository: [infoconex/RecordSift](https://github.com/infoconex/RecordSift)

RecordSift is a Windows-only CSV and Excel import library, used both as an application and as a realistic modernization case study.

At the first evaluation baseline it contains five production libraries and five NUnit 3 test projects targeting .NET Framework 4.8 with C# 7.3 and traditional, non-SDK project files.

## Evaluations

- [2026-11: Pre-SDK modernization discovery](evaluations/2026-11-pre-sdk/README.md) — what can safely be improved before SDK-style conversion.

Future evaluations (such as SDK conversion or runtime migration) should use their **own** dates, baseline SHAs, evidence and verification gates. This repository stores assessment and learning, not the application source code.

## Related cross-application research

The [Gate C-N native-PDB provenance investigation](../../research/native-pdb-provenance/README.md) references RecordSift as its primary case study, with a separate non-RecordSift portability fixture. RecordSift's own [experiment results and preserved sanitized reports](evaluations/2026-11-pre-sdk/evidence/README.md), together with its application-focused [strategy review](evaluations/2026-11-pre-sdk/reviews/gate-cn-engineering-perspectives-strategy-review-20261106.md), remain in its dated evaluation.

The [historical source index](evaluations/2026-11-pre-sdk/history/HISTORICAL-RESEARCH-INDEX.md) and [inert workflow archives](evaluations/2026-11-pre-sdk/archives/README.md) are maintained with that evaluation, not with reusable toolkit code.
