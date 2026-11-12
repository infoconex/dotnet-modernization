# EXP-017 control: independently rebuild a SECOND unmodified checkout of
# the exact frozen SHA to measure same-source package-byte variability.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ApplicationRoot,
    [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$frozen = '8358780829458854a4b0356df5ac5e685f0a34c8'
$application = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence = (Resolve-Path -LiteralPath $EvidenceRoot).Path
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$sourceSha = (& git -C $application rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Could not resolve original source SHA.' }
# EXP-015 has already made this disposable checkout into a local candidate.
# Require that frozen source SHA is a parent of the candidate, but never modify it.
$parentSha = (& git -C $application rev-parse 'HEAD^').Trim()
if ($LASTEXITCODE -ne 0 -or $parentSha -cne $frozen -or $sourceSha -cne
    (Get-Content (Join-Path $evidence 'candidate-report.json') -Raw | ConvertFrom-Json).ephemeral_candidate_sha) {
    throw 'Expected complete EXP-015 disposable candidate before same-source repeat.'
}
$repeatRoot = Join-Path $evidence 'same-source-repeat'
if (Test-Path -LiteralPath $repeatRoot) { throw 'Repeat checkout already exists.' }
& git -C $application worktree add --detach $repeatRoot $frozen
if ($LASTEXITCODE -ne 0) { throw 'Could not create repeat frozen worktree.' }
if ((& git -C $repeatRoot rev-parse HEAD).Trim() -cne $frozen) { throw 'Repeat SHA differs.' }
if (@(& git -C $repeatRoot status --porcelain --untracked-files=normal).Count -ne 0) { throw 'Repeat checkout dirty.' }
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Missing Visual Studio MSBuild.' }
Push-Location $repeatRoot
try {
    & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
    if ($LASTEXITCODE -ne 0) { throw 'Repeat NuGet restore failed.' }
    & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
    if ($LASTEXITCODE -ne 0) { throw 'Repeat ten-project rebuild failed.' }
}
finally { Pop-Location }
$pilot = Join-Path $repoRoot 'tooling/pilots/recordsift/EXP-014/run.ps1'
$repeatEvidence = Join-Path $evidence 'repeat-evidence'
& $pilot -ApplicationRoot $repeatRoot -EvidenceRoot $repeatEvidence -ExpectedCommit $frozen -ExperimentId 'EXP-017-identical-source-rebuild'
if ($LASTEXITCODE -ne 0) { throw 'Repeated frozen revision failed original full compatibility gates.' }
$repeatReport = Get-Content (Join-Path $repeatEvidence 'pilot-report.json') -Raw | ConvertFrom-Json
if ($repeatReport.source_commit -cne $frozen) { throw 'Repeat pilot provenance mismatch.' }
Write-Host "PASS: EXP-017 fully validated second independent Release build of identical frozen SHA $frozen."
