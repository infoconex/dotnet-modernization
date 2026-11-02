# Recommended implementation roadmap

These are **discovery-supported recommendations**, not applied RecordSift changes.

## Priority matrix

| Candidate | Immediate value | Risk | Effort | SDK preparation | Recommendation |
|---|---|---|---|---|---|
| Fix four-versus-five local test coverage | High | Low | Low | High | Before SDK, first |
| Capture reproducible compatibility gates | High | Low | Medium | High | Before SDK |
| Centralize identical LangVersion with Directory.Build.props | High | Low–medium | Low | High | Before SDK; already POC verified |
| Standardize local tool and PowerShell assumptions | High | Low–medium | Medium | Medium | Before SDK or independently |
| SDK-only Windows build/test workflow | High | Low–medium | Medium | Medium | Optional before SDK; feasible |
| Condition-based shared warning levels | Medium | Low | Low | Medium | Optional |
| global.json pin/roll-forward | Medium | Low–medium | Low | Medium | Optional after formatter test |
| Directory.Build.targets with no actual reusable build behavior | Low | Medium | Medium | Low | Not recommended |
| Additional .rsp / Directory.Solution.* files without requirements | Low | Medium | Low | Low | Not recommended |
| Early Microsoft.Common.props import | Low | High, observed failure | Medium | Low | Not recommended |
| packages.config to PackageReference / Directory.Packages.props | Migration value | Medium–high | Medium | High | During SDK conversion |

## Dependency-aware sequence

1. **Agree on acceptance baseline.** Use [baseline](baseline.md), preserve five NUnit suites, 425 approved API/metadata entries, XML docs, resource and assembly identity, local package and consumer checks. Document skipped or unavailable gates.
2. **Repair local testing parity.** Modify `scripts/run_tests.ps1` *in RecordSift only after approval* to include XLSX. Confirm 419/418/0/1 and normal CI.
3. **Create minimal shared compiler defaults.** Move identical LangVersion=7.3 from all ten projects into root Directory.Build.props, without adding an early import. Use conditional assignment where project-specific override must remain possible. Compare evaluated properties; execute the complete gate.
4. **Consider other duplication one setting at a time.** WarningLevel may qualify. Keep output directories, documentation files, resource names, assembly metadata and TargetFrameworkVersion project-specific for now.
5. **Document a fully inventoried clean Windows environment.** Favor an immutable .NET SDK-only image for educational build/test independence; separately qualify complete API/packaging/consumer scripts. Do not claim release equivalence prematurely.
6. **Consider SDK selection after actual formatter/CI test.** Make any global.json choice deliberate and documented.
7. **Only then evaluate SDK-style conversion.** Preserve current framework and C# while converting project format; defer PackageReference/central package management to a separately verified stage if appropriate.

## Verification for substantive application changes

Restoration → Release build of all ten → NUnit 419 discovered / 418 pass / 0 fail / 1 expected skip → public API 425 entries → assembly versions and logical resources → five XML docs → .nuspec/package contents, dependencies and clean consumer verification → Windows CI.

A change can be implemented independently when its only dependency is the baseline; the shared-properties change benefits from fixing the local test runner first. Do not change application main, merge or publish based solely on this roadmap.
