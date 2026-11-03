# EXP-009 — SDK-only Windows packaging and clean-consumer compatibility

**Investigation date:** November 3, 2026  
**Tracking issue:** [dotnet-modernization #7](https://github.com/infoconex/dotnet-modernization/issues/7)  
**Historical predecessor:** [EXP-007](EXP-007-sdk-only-release-gates.md) (preserved unchanged)  
**Application baseline:** `infoconex/RecordSift` `main` = `8358780829458854a4b0356df5ac5e685f0a34c8`  
**Disposable research branch:** `research/sdk-only-release-followup-20261103`, forked from the exact application baseline  
**Final workflow commit:** `3cea8e844d5dbb77c10d3908687eae8590899abf`  
**Work state:** Complete. **Evidence outcome:** Verified for the **temporarily corrected positive release path**; original scripts do **not** pass unmodified in this SDK-only environment. Optional CS1591 negative gate not executed.  
**Authorization:** Research and documentation only. No production application code, application `main`, `release/0.2`, or release artifact was changed, merged or published.

## Question and hypotheses

Can existing traditional net48 projects complete restore, build, all tests, public API and XML checks, NuGet packaging/validation, local installation and *independent compiled/executed consumers* in a Windows .NET SDK environment with no Visual Studio IDE or Build Tools?

Following [EXP-007](EXP-007-sdk-only-release-gates.md), test three separate explanations, not a generic application failure:

1. Windows PowerShell 5.1's default handling of BOM-less UTF-8 notices differs from the ZIP-entry UTF-8 reader.
2. The container's `NUGET_XMLDOC_MODE=skip` prevents expected documentation extraction from an otherwise valid archive.
3. Independent consumer compilation is blocked by a validation-script assumption about Visual Studio `vswhere` / `Roslyn\csc.exe`, not by RecordSift's .NET Framework 4.8 binaries.

Only the disposable workflow was committed. The experiment generates **untracked, temporary copies** of the two affected scripts in its ephemeral checkout, changes their text decoding/compiler invocation, runs them, and discards the workspace. The original scripts run separately as negative controls.

## Execution environment and prerequisites

| Requirement | Actual observed environment |
|---|---|
| Host / container | GitHub Actions `windows-2022`; Windows Server Core 2022, NT `10.0.20348.0`, Docker process isolation |
| Image | `mcr.microsoft.com/dotnet/sdk:10.0.403-windowsservercore-ltsc2022` |
| Pulled immutable image digest | `sha256:2b4600777bcef9209c18ae1c284bbdbf92edfbfba64728887ccf8eb61051bc25` |
| .NET SDK and MSBuild | SDK `10.0.403`; `dotnet msbuild` `18.9.15.52412`, provided by image |
| SDK Roslyn | `C:\Program Files\dotnet\sdk\10.0.403\Roslyn\bincore\csc.dll`, provided by SDK |
| .NET Framework | Windows framework **runtime** present; net48 **reference assemblies** absent before explicit provisioning |
| Additional targeting pack | `Microsoft.NETFramework.ReferenceAssemblies.net48` `1.0.3` provisioned into `C:\sdktools\packages` |
| NuGet CLI | `nuget.exe` `6.14.0.116`, separately downloaded (not bundled with the SDK) |
| PowerShell | Windows PowerShell `5.1.20348.5773` |
| NUnit runner | `NUnit.ConsoleRunner` `3.17.0` restored with existing packages |
| Excluded | No Visual Studio IDE, Build Tools, or standalone Visual Studio `MSBuild.exe` |

The targeting pack supplies **compile-time** reference assemblies; the existing Windows .NET Framework runtime is required for the NUnit and net48 consumer executables. Neither requirement is satisfied merely by having a .NET SDK.

The inherited container environment had `NUGET_XMLDOC_MODE=skip`. The positive consumer controls explicitly set it to `none`.

## Runs and controls

| Run | Workflow SHA | Observations and validity |
|---|---|---|
| [41707695201](https://github.com/infoconex/RecordSift/actions/runs/41707695201) | `abfce77d277c0854d478152808a2591801afbc08` | Baseline build, 419 NUnit, XML, API passed. Confirmed default notice decoding differs from explicit UTF-8. A new ZIP probe lacked `System.IO.Compression.FileSystem`, so its entry comparison was **inconclusive (harness defect)**. [Artifact 13266705727](https://github.com/infoconex/RecordSift/actions/runs/41707695201/artifacts/13266705727). |
| [41707884452](https://github.com/infoconex/RecordSift/actions/runs/41707884452) | `290634e3d5ef12cc870af5ea4fa2761eba3c9032` | ZIP entry text matched explicit UTF-8 source, not default-decoded source. The temporary script-copy step failed because .NET file APIs used a different current directory than PowerShell's provider location; corrected without touching product code. **Packaging/consumer positive controls not executed (harness defect).** [Artifact 13267920768](https://github.com/infoconex/RecordSift/actions/runs/41707884452/artifacts/13267920768). |
| **[41708730067](https://github.com/infoconex/RecordSift/actions/runs/41708730067)** | **`3cea8e844d5dbb77c10d3908687eae8590899abf`** | **Completed successfully:** repeated original negative controls, verified UTF-8 correction, validated local package and installed it, tested `NUGET_XMLDOC_MODE=none`, and compiled/executed both independent consumers with SDK Roslyn. Full step logs and [artifact 13268111524](https://github.com/infoconex/RecordSift/actions/runs/41708730067/artifacts/13268111524). |

The corrected workflow reconciled .NET's process current directory with the PowerShell working directory before creating temporary script copies; this was a diagnostic-harness fix, not an application change.

### Exact gate results — final run

| Gate | Actual result | Meaning |
|---|---|---|
| No net48 reference assemblies (negative control) | **Expected failure, MSB3644** | A .NET SDK alone does not provide the net48 targeting pack. |
| Explicit reference assemblies + NuGet restore + ten-project Release build | **PASS** | Traditional project compilation needs no VS Build Tools in the tested environment. |
| Five NUnit assemblies | **PASS:** 419 discovered, 418 passed, 0 failed, 1 skipped | Full known automated baseline retained. |
| XML docs positive validation | **PASS:** 179 / 101 / 8 / 2 / 9 documented members | Five compiled XML outputs present. |
| Public API and metadata | **PASS:** 425 baseline entries | No observed API/identity regression. |
| Original package validator | **FAIL:** notice text mismatch | Expected negative control; package archive exists. |
| Byte/text comparison | **PASS:** 2,655-byte notices; ZIP text equals explicit UTF-8 and `.NET Encoding.UTF8`, not default Windows PowerShell 5.1 text | Pinpoints encoding mismatch in validator, not package corruption. |
| **Temporary explicit-UTF8 package validator** | **PASS** | Unpublished `RecordSift.0.1.0-rc.1.nupkg` validates DLL/XML layout, package metadata, README, MIT license and notices. |
| Original installed-package consumer under `NUGET_XMLDOC_MODE=skip` | **FAIL:** extracted XML missing | Expected environment negative control; archive itself includes XML docs. |
| Original consumer under `NUGET_XMLDOC_MODE=none` | **FAIL:** cannot execute `vswhere.exe` | Installed XML missing-file failure is eliminated; the next genuine dependency is the Visual Studio tool-discovery path. |
| **Temporary SDK-Roslyn consumer under `none`** | **PASS** | Clean NuGet install, both C# 7.3/net48 executables compiled and ran against installed DLLs, not repository-built DLLs. |
| Getting Started source examples | **PASS** | Both `customers` and `customers-invalid` CSV/XLSX sample pairs validated and compared. |
| CS1591 **negative** XML-documentation compiler test | **NOT EXECUTED** | `verify_xml_documentation.ps1 -Negative` still explicitly discovers VS MSBuild. No claim of full negative-gate independence. |

The validated, **unpublished** local archive SHA-256 is `8244C4BD83A2C91D443D0FCE86D5AA6E522289D1B94BD98E468689A53BC4F43F`. Its package source-commit metadata necessarily names the **experimental workflow SHA**, while the existing packaging script writes `branch=main`; that metadata combination is an isolated research artifact only, **not** a candidate for publication. For the tested code, the application projects match the frozen `8358780` baseline; only the added workflow differs.

## Reproducible commands and modifications

The exact [workflow file](https://github.com/infoconex/RecordSift/blob/3cea8e844d5dbb77c10d3908687eae8590899abf/.github/workflows/research-exp009-sdk-only-release.yml) supplies path provisioning, all process arguments, container volumes and artifact collection.

Core build/test commands (inside `C:\repo`, after installing NuGet CLI and net48 reference pack):

```powershell
nuget restore RecordSift.sln -NonInteractive -PackagesDirectory C:\repo\packages -ConfigFile NuGet.Config
dotnet msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' "/p:TargetFrameworkRootPath=$frameworkRoot" "/p:FrameworkPathOverride=$($refs.DirectoryName)" /v:minimal
& C:\repo\packages\NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe @assemblies '--result=C:\repo\TestResults\sdk-only-nunit.xml;format=nunit3' --noheader
```

The workflow invokes the existing positive XML and API check scripts under Windows PowerShell 5.1, preloading `System.IO.Compression.FileSystem` in each independent child process. The **temporary** package validation copy changes only the reviewed notice-source reading expression to:

```powershell
$source = Get-Content -LiteralPath (Join-Path $root $file) -Raw -Encoding UTF8
```

The **temporary** consumer validation copy removes the hard-coded `vswhere`/Visual Studio compiler path and invokes SDK Roslyn with `dotnet exec $csc /nologo /noconfig /nostdlib+ @frameworkReferences /target:exe /langversion:7.3 ...`, with explicit net48 references for `mscorlib`, `System`, `System.Core`, `System.Xml`, `System.Data`, and `Microsoft.CSharp`. The scripts installed the unpublished candidate and pinned third-party dependencies into a freshly created temporary directory, then executed `Program.cs` and `GettingStartedSamples.cs`.

All detailed commands and failures are in the workflow job output, `TestResults/sdk-only-release-gates.json` and per-gate logs in artifact **13268111524**. The success of the workflow is not treated as passing the intentionally unsuccessful original-script controls.

## Findings, risks and recommended disposition

**What caused EXP-007's remaining failures:** (1) a Windows PowerShell 5.1 decoding assumption in the notice validator, (2) container-specific NuGet XML extraction suppression, and (3) the consumer script's hard-coded Visual Studio compiler lookup. The failures were in the release-validation toolchain/environment, not observed RecordSift package data or public API behavior. The first two EXP-009 reruns additionally exposed temporary *experiment harness* defects; their logs are preserved, not counted as product regressions.

**Alternatives:** Specify UTF-8 explicitly when comparing notice text, or validate exact bytes if the desired contract is byte identity. Scope `NUGET_XMLDOC_MODE=none` to the consumer verification process. For compilation, either use the SDK-provided Roslyn compiler with explicit framework references (**verified**) or consider a small independent net48 consumer project built through `dotnet msbuild` (**not experimentally verified**), to avoid brittle SDK-internal compiler paths and hand-maintained references.

**Risk:** Compiler paths and SDK versions change; explicit raw compiler invocation may be more fragile than project-based builds. PowerShell and NuGet defaults vary by host. The SDK-only Windows runtime and targeting-pack prerequisites must be documented explicitly. This experiment covers **Windows Server Core 2022 with SDK 10.0.403**, not all Windows images, PowerShell 7, or standalone machines. Existing CI passes with VS tooling; changing it gains little unless VS Build Tools independence is a real operating requirement. The optional CS1591 negative compiler-control path is still VS-dependent and unverified under SDK-only.

**Recommendation:** Treat SDK-only **development build/test** and **positive release-validation feasibility** as verified. Retain the existing verified VS-backed release pipeline unless an explicit operational constraint justifies changing it. If portability is later desired, approve focused validation-script changes separately and rerun every release gate including the negative CS1591 control. Avoid introducing a complex new build abstraction merely for the experiment. No SDK-style conversion, modern .NET migration, package publication or production changes are authorized.

**Additional research justified?** Not for the core feasibility question: it now has direct positive consumer evidence. Research of the optional CS1591 negative test, project-based consumer compilation, or broader image portability is warranted only if an actual release-tooling-independence requirement emerges.

## Primary references

- [EXP-009 successful Actions run, workflow logs and artifacts](https://github.com/infoconex/RecordSift/actions/runs/41708730067)
- [Artifact 13268111524](https://github.com/infoconex/RecordSift/actions/runs/41708730067/artifacts/13268111524)
- [PowerShell character encoding](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_character_encoding) — Windows PowerShell default encoding behavior.
- [NuGet CLI environment variables](https://learn.microsoft.com/en-us/nuget/reference/cli-reference/cli-ref-environment-variables) — `NUGET_XMLDOC_MODE`.
