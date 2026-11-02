# EXP-<NNN> — <Title>

**Evaluation:** <relative link>  
**Application repository:** <owner/repository>  
**Baseline branch/SHA:** <branch> / <full SHA>  
**Experiment branch/SHA:** <branch> / <full SHA or no repository changes>  
**Date:** <YYYY-MM-DD>  
**Work state:** <not started/in progress/complete/blocked/deferred>  
**Evidence outcome:** <verified/partially verified/unverified/failed hypothesis/blocked/not executed>

## Objective and hypothesis

A specific, testable question and the expected observable result.

## Environment and dependencies

OS/build, image tag and immutable digest, isolation mode, SDK/runtime, MSBuild path/version, framework references, NuGet/compiler/NUnit, tool provenance and relevant environment variables.

## Baseline and success criteria

Exact behavior and compatibility contracts to preserve.

## Reproduction

Commands to provision the environment, restore dependencies, execute experiment, test and collect artifacts. Specify any intentionally failing negative controls.

## Observed results

Separate each attempted step (passed, failed, skipped, not executed). Include actual counts and error identifiers; do not infer results from the parent workflow status.

## Evidence

Workflow URL, run ID, artifact ID/name, retained log excerpts, source SHA.

## Risks and limitations

What this experiment does **not** establish.

## Conclusion and follow-up

Supported finding, recommended decision (if any), and verification required before implementation.
