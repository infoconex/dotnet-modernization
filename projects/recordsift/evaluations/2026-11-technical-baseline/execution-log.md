# RecordSift — Technical discovery execution log

**Source repository:** [infoconex/RecordSift](https://github.com/infoconex/RecordSift)  
**Frozen source SHA:** `1809d06c0fade59e4769d16e0f8eaf10fa426004` (GitHub `main` observed 2026-11-12)  
**Runbook:** [Native-first discovery](../../../../methodology/technical-discovery-runbook.md)  
**Schema:** [Discovery execution-log template](../../../../templates/discovery-execution-log.md)  
**Working technical baseline:** [baseline.md](baseline.md)  
**Evidence manifest:** [evidence/manifest.md](evidence/manifest.md)

This is the authoritative operator progress record, separate from the final technical facts in `baseline.md`. **Nothing has been run in a local checkout as part of this new walkthrough.** Initial GitHub source inspection is recorded separately below.

## Local execution and prerequisite versions

**Executed by:** Not yet recorded — awaiting your Windows PowerShell results.  
**Execution date/time:** Not yet recorded.  
**Discovery folder:** Not yet created or verified.

| Prerequisite | When needed | Version / details recorded from your computer | Status |
|---|---|---|---|
| Windows OS and architecture | All RecordSift steps | Not yet recorded | Not checked |
| PowerShell | Discovery commands | Not yet recorded | Not checked |
| Git | Clone and source checks | Not yet recorded | Not checked |
| .NET SDK / `dotnet` | Applicable later commands | Not yet recorded | Not checked |
| MSBuild / Visual Studio Build Tools | Build evaluation and compilation | Not yet recorded | Not checked |
| .NET Framework 4.8 targeting pack | Traditional net48 build | Not yet recorded | Not checked |
| Standalone NuGet CLI | Existing `packages.config` restore | Not yet recorded | Not checked |
| Test runner | Test execution | Not yet recorded | Not checked |

- Fill this table from your **actual command results**. Record unavailable tools as *not found on PATH* or *not installed*, as supported by the check; don't guess versions.
- DISC-001 captures Windows, PowerShell, Git, and command availability. DISC-004 records the complete SDK, MSBuild, NuGet, targeting-pack, and test-runner versions before those tools are used.
- For each completed discovery step, record **who ran it, when, the commands/results, and where the output is saved**. Use the detailed fields in the [execution-log template](../../../../templates/discovery-execution-log.md).
- Keep expected outputs separate from observed results. No local execution has been verified yet.

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

### 1. Confirm the discovery prerequisites (before cloning)

In **PowerShell on Windows** (Windows PowerShell 5.1 or PowerShell 7; record which is used), run these commands individually:

```powershell
[System.Runtime.InteropServices.RuntimeInformation]::IsOSPlatform([System.Runtime.InteropServices.OSPlatform]::Windows)
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, OSArchitecture
$PSVersionTable.PSVersion
Get-Command git -ErrorAction SilentlyContinue
git --version
Get-Command dotnet -ErrorAction SilentlyContinue
Get-Command msbuild -ErrorAction SilentlyContinue
Get-Command nuget -ErrorAction SilentlyContinue
```

**Windows is a hard prerequisite for the RecordSift walkthrough, beginning with DISC-001.** The first command must return `True`. If it returns `False`, stop: do not use Linux, macOS or WSL as a substitute for this Windows-only case study. Record the actual Windows version/build and architecture. **For DISC-001:** PowerShell on Windows and Git are required; Git 2.23+ supports the pinned-commit `git switch --detach` step. Record a Git-not-found error and stop rather than proceeding.

**For later RecordSift execution:** the application is a Windows-only .NET Framework 4.8 library using traditional project files and tracked `packages.config` files. We will need a **Windows-compatible build/test environment**, a suitable MSBuild installation, .NET Framework 4.8 targeting assemblies, and a standalone NuGet CLI for the documented restore path. Test runners and any SDK-dependent optional commands will be verified before use. `dotnet` is **not** automatically required for the source checkout or all traditional project builds. `Get-Command` searches PATH only; `msbuild`/`nuget` not found on PATH is a readiness question, not proof the tool is not installed. No software installation is authorized by this preflight.

**Pause at the preflight** if required tools are unavailable or the environment is uncertain; report the results before proceeding with a build/test later. For source-only discovery, non-Git tooling gaps can be recorded and resolved before their steps.

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
