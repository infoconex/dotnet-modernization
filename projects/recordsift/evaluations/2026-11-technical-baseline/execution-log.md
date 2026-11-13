# RecordSift — Technical discovery execution log

**Source repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Frozen source SHA:** `1809d06c0fade59e4769d16e0f8eaf10fa426004` (GitHub `main` observed 2026-11-12)  
**Runbook:** [Native-first discovery](../../../../methodology/technical-discovery-runbook.md)  
**Schema:** [Discovery execution-log template](../../../../templates/discovery-execution-log.md)  
**Working technical baseline:** [baseline.md](baseline.md)  
**Evidence manifest:** [evidence/manifest.md](evidence/manifest.md)

This is the authoritative operator progress record, separate from the final technical facts in `baseline.md`. **Nothing has been run in a local checkout as part of this new walkthrough.** Initial GitHub source inspection is recorded separately below.

## DISC-001 — Check prerequisites

**Executed by:** Not yet recorded.  
**Date/time:** Not yet recorded.  
**Discovery folder:** Not yet created.

Execute each snippet separately in **Windows PowerShell**. Replace **Not yet executed** with the actual result, including the version or any error.

### Windows — required; Windows host for all RecordSift steps

```powershell
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
```

**Result:** Not yet executed.

- If you're not using Windows, switch to a Windows computer before beginning.
- Record Windows version, build, and architecture.

### PowerShell — required; Windows PowerShell 5.1 or PowerShell 7

```powershell
$PSVersionTable.PSVersion
```

**Result:** Not yet executed.

- If unavailable, use Windows PowerShell or [install PowerShell for Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows).

### Git — required; minimum version 2.23

```powershell
git --version
```

**Result:** Not yet executed.

- If missing or older than 2.23, [install Git for Windows](https://git-scm.com/install/win), reopen PowerShell, and try again.
- Record the reported version. Stop before cloning if this check fails.

### .NET SDK — optional for checkout; no universal minimum

```powershell
dotnet --info
```

**Result:** Not yet executed.

- If missing and required for a later step, [install a compatible .NET SDK](https://dotnet.microsoft.com/en-us/download).
- Record installed SDKs and runtimes or the command error.

### MSBuild — required for RecordSift build; version to confirm

```powershell
msbuild -version -nologo
```

**Result:** Not yet executed.

- If missing, try Visual Studio Developer PowerShell first. If not installed, [install Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) with the .NET Framework build components.
- Record the version. The optional `-getProperty` query later requires **MSBuild 17.8+**.

### NuGet CLI — required for RecordSift restore; minimum not yet established

```powershell
nuget help
```

**Result:** Not yet executed.

- If missing, [install the standalone NuGet CLI](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-nuget-cli).
- Record the version shown. Use the application's documented `nuget restore` command at DISC-008, not during this check.

### .NET Framework 4.8 targeting pack — required for RecordSift build

```powershell
Test-Path "${env:ProgramFiles(x86)}\Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8"
```

**Result:** Not yet executed.

- If `False`, check Visual Studio components or [install the .NET Framework 4.8 Developer Pack](https://dotnet.microsoft.com/en-us/download/dotnet-framework/net48).
- Record `True` or `False`. This checks the directory, not build success.

**Test runner:** Check its command and version at DISC-010 after identifying the actual runner.

- **To clone:** Windows, PowerShell, Git, internet access, and a writable folder must be available.
- **Before restore/build/tests:** confirm the remaining prerequisites and record any missing versions. Do not install anything automatically.
- Don't include secrets or personal paths in shared results.

## Step progress

| Step | Work state | Evidence outcome | Current note |
|---|---|---|---|
| DISC-001 — Source identity | Awaiting owner | Partial source-only preflight | GitHub HEAD verified, **local HEAD/status unknown** |
| DISC-002 — Solutions/projects | Not started | Source-tree paths only | No local solution listing executed |
| DISC-003 — Declared project configuration | Not started | Not verified | Project files not examined in detail |
| DISC-004 — Toolchain inventory | Not started | Not executed | No host facts assumed |
| DISC-005 — Evaluated build settings | Not started | Not executed | No MSBuild evaluation performed |
| DISC-006 — Central configuration | Not started | Tracked-file preflight only | Precedence and effective values unknown |
| DISC-007 — Dependencies before restore | Not started | Tracked-file preflight only | No package graph verified |
| DISC-008 — Restore | Not started | Not executed | Requires operator review of writes |
| DISC-009 — Build | Not started | Not executed | Requires operator review of writes |
| DISC-010 — Tests | Not started | Not executed | Runner/coverage unknown in this evaluation |
| DISC-011 — CI/CD and delivery | Not started | Tracked workflow paths only | No workflow outcome reused |
| DISC-012 — Compatibility evidence | Not started | Not executed | Historical checks separate |
| DISC-013 — Evidence reconciliation | Not started | Not executed | Pending collected results |
| DISC-014 — Final baseline review | Not started | Not executed | Pending collected results |

## Source-only preflight — GitHub, 2026-11-12

**Method:** GitHub repository metadata and tracked-tree inspection at `1809d06c0fade59e4769d16e0f8eaf10fa426004`. **Operator:** assistant using connected GitHub repository access, not local Git/MSBuild execution. **Evidence:** [EV-001–003](evidence/manifest.md). **Result:** identified one `.sln`, ten `.csproj` paths, central-file locations and CI workflow paths. **Limitation:** no local dirty-state check, evaluation, compilation, testing or restore performed. This cannot complete DISC-001 or the later steps.

## Next operator step — DISC-001: tool preflight and dated checkout

**Objective:** **require a Windows host**, then verify tools and upcoming prerequisites; obtain a **new** RecordSift source checkout named `RecordSift-discovery-YYYY-MM-DD-HHmmss` at the frozen SHA. No local command has yet been reported as executed for this evaluation. Run the commands individually rather than as a custom discovery script.

### 1. Check the tools above

- Execute each tool's command separately and fill in its **Result**.
- **Stop before cloning** if the Windows or Git prerequisite cannot be met.
- If `dotnet`, `msbuild` or `nuget` is unavailable, note the result; we'll decide what is required before build and restore.

### 2. Create a timestamped discovery directory

Use the prescribed **home-directory-based parent**, unless an alternative writable location is required. The timestamp is generated using the operator's local clock, so it is not a hardcoded date.

```powershell
$discoveryRoot = Join-Path (Join-Path $HOME 'source') 'discoveries'
New-Item -ItemType Directory -Path $discoveryRoot -Force
$discoveryFolder = "RecordSift-discovery-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
$destination = Join-Path $discoveryRoot $discoveryFolder
Test-Path -LiteralPath $destination
```

**Only continue when `Test-Path` reports `False`**. If the name already exists, create a new timestamped destination and check again; never delete, reset or overwrite an old directory. The `New-Item` command creates a parent directory if absent and has no effect on an existing folder's contents.

### 3. Clone and check out the immutable revision

```powershell
git clone --no-checkout https://github.com/infoconex/RecordSift.git $destination
Set-Location -LiteralPath $destination
git switch --detach 1809d06c0fade59e4769d16e0f8eaf10fa426004
```

Run each command separately and stop on failures. This downloads source, creates the new checkout and populates tracked files at our frozen SHA. It does **not** modify the remote repository. Detached HEAD is expected for this documentation snapshot. It does **not** ensure a clean SDK/MSBuild/NuGet environment, which will be examined later.

### 4. Verify before documenting success

```powershell
git rev-parse --show-toplevel
git rev-parse HEAD
git branch --show-current
git status --porcelain=v1 --untracked-files=all
git remote get-url origin
```

**Expected, not yet observed:** Windows host verified; HEAD equals `1809d06c0fade59e4769d16e0f8eaf10fa426004`; current branch output is empty (detached HEAD); status output is empty (clean tracked/untracked working tree).

**Capture:** the verified Windows OS/version/build/architecture, PowerShell/Git versions, availability or gaps for `dotnet`/`msbuild`/`nuget`, date and actual discovery directory name, sanitized clone/checkout commands, full HEAD SHA and status, actual command errors and any unexpected conditions. Do not share private paths or credential-bearing remote URLs.

**Assistant's next action:** verify actual operator results, update EV-001 or add separately sourced execution evidence, complete DISC-001 as applicable, then prepare DISC-002. Do not record expected results as observed or trigger restore/build/test without reviewing prerequisites and side effects.

## Article progress

**Candidate lesson:** start with immutable source identity and distinguish inspected repository files from actually executed checks. **Evidence:** currently source-only; defer walkthrough execution claims until actual operator output is available.
