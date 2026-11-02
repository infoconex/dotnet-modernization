# Modernization evaluation lifecycle

## 1. Intake

Identify the application, owning repository, supported platforms, target framework(s), project formats, stakeholders, constraints, and objective. Separate **discovery**, **approved implementation**, and **release** scopes.

**Output:** project profile and evaluation overview.

## 2. Establish the baseline

Record branch/commit, source inventory, explicit and implicit build dependencies, restore commands, compilation, full test count, API/resource/assembly identities, packaging and consumer compatibility. Note failed, skipped, and unavailable checks.

**Output:** baseline document with evidence references.

## 3. Reproduce the environment

Inventory OS/build, SDK/runtime/targeting packs, compiler, MSBuild implementation, NuGet, test runner, environment variables, container image and digest where applicable. Label tools as preinstalled or explicitly added.

**Output:** environment record and executable commands.

## 4. Discover opportunities

Identify actual duplication, workflow defects, tool assumptions, modernization tools, and technical constraints. Classify benefits as **immediate**, **future migration**, or **likely redundant**.

**Output:** candidate opportunities, hypotheses, priorities.

## 5. Experiment in isolation

Prefer disposable workspaces or branch-specific workflows. Capture commands, environment, raw results, control comparisons, and limitations. Preserve application compatibility unless the experiment explicitly explores a deviation.

**Output:** one experiment record per meaningful hypothesis.

## 6. Assess and decide

Rank candidates by benefit, risk, effort, independent implementability, tool dependencies, reversibility, SDK preparation value, longevity, and educational value. Distinguish **what was observed** from **what we intend to do**. Record rejected and deferred options.

**Output:** findings, decision records, roadmap.

## 7. Implement only approved changes

Use the **application's own repository**. Create focused, reversible change sets. Run baseline and post-change verification gates; validate on the actual CI platform. Do not infer implementation from a discovery experiment.

**Output:** issues/PRs, compatibility evidence, implementation status.

## 8. Capture reusable learning

Promote broadly applicable lessons into research, linking the exact application experiment that supports each claim. Date findings with tool-version sensitivity. Map publication candidates to evidence, but draft articles separately.

**Output:** cross-project research and article planning links.

## Status model

Track **work state** independently from **verification outcome**:

- Work: not started, in progress, complete, blocked, deferred.
- Evidence: verified, partially verified, unverified, failed hypothesis, not executed.

A successfully completed experiment can have a failed hypothesis; a verified experiment does not imply an implementation was approved.
