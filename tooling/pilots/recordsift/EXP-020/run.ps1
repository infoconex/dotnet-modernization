# EXP-020 — PathMap isolation after verified EXP-019 deterministic-only controls.
# Only command-line properties are applied in disposable worktrees. No source edits.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ApplicationRoot,
    [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$frozen = '8358780829458854a4b0356df5ac5e685f0a34c8'
$application = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence = [IO.Path]::GetFullPath($EvidenceRoot)
$repo = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
if ($evidence.StartsWith($application + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Evidence must remain outside the application checkout.' }
if (Test-Path -LiteralPath $evidence) { throw 'Evidence root must not preexist.' }
$startSha = (& git -C $application rev-parse --verify HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $startSha -cne $frozen) { throw 'Wrong immutable RecordSift source revision.' }
$startDirty = @(& git -C $application status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $startDirty.Count -ne 0) { throw 'Original source checkout must begin clean.' }
New-Item -ItemType Directory -Path $evidence | Out-Null

# Full negative control: the predecessor executes historical default, two
# deterministic-only independent paths and a same-directory repeat. It validates
# the FULL application release/consumer gates for all four builds.
$controls = Join-Path $evidence 'unmapped-deterministic-control'
& (Join-Path $repo 'tooling/pilots/recordsift/EXP-019/run.ps1') -ApplicationRoot $application -EvidenceRoot $controls
if ($LASTEXITCODE -ne 0) { throw 'EXP-019 unmapped deterministic negative control was not accepted.' }
$controlReport = Get-Content (Join-Path $controls 'experiment-report.json') -Raw | ConvertFrom-Json
if ($controlReport.frozen_source_sha -cne $frozen -or $controlReport.deterministic_reproducibility.independent_worktree.different_binaries -le 0 -or
    $controlReport.deterministic_reproducibility.same_worktree_rebuild.identical_binaries -ne 5) {
    throw 'Unmapped deterministic controls did not preserve expected verified behavior.'
}
$independent = Join-Path $controls 'independent-source'
if ((& git -C $independent rev-parse HEAD).Trim() -cne $frozen) { throw 'Second source worktree SHA changed.' }
$reader = Join-Path $repo 'tooling/pe-provenance/src/bin/Release/net10.0/PeProvenance.dll'
if (-not (Test-Path $reader)) { throw 'Required metadata-only PE reader missing.' }
$pilot = Join-Path $repo 'tooling/pilots/recordsift/EXP-014/run.ps1'
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Required Visual Studio MSBuild not found.' }
$components = @('Domain', 'Application', 'Infrastructure.Csv', 'Infrastructure.Reporting', 'Infrastructure.Xlsx')
$parameters = @(
    [pscustomobject]@{ label='mapped-original'; root=$application; canonical='/_recordsift' },
    [pscustomobject]@{ label='mapped-independent'; root=$independent; canonical='/_recordsift' },
    [pscustomobject]@{ label='wrong-map-independent'; root=$independent; canonical='/_recordsift_intentionally_wrong' }
)
$observations = @()

function Verify-Immutable([string]$root, [string]$phase) {
    $sha = (& git -C $root rev-parse --verify HEAD).Trim()
    $changed = @(& git -C $root diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0 -or $sha -cne $frozen -or $changed.Count -ne 0) { throw "$phase changed frozen source or tracked files." }
}
foreach ($case in $parameters) {
    $root = [string]$case.root
    $label = [string]$case.label
    $canonical = [string]$case.canonical
    Verify-Immutable $root "$label before build"
    $value = "$root=$canonical"
    $evaluations = @()
    foreach ($component in $components) {
        $project = Join-Path $root ("src/RecordSift.{0}/RecordSift.{0}.csproj" -f $component)
        foreach ($property in @('Deterministic', 'PathMap')) {
            $args = @($project, "-getProperty:$property", '/p:Configuration=Release', '/p:Platform=AnyCPU', '/p:Deterministic=true', "/p:PathMap=$value", '-nologo')
            $effective = ((& $msbuild @args) -join [Environment]::NewLine).Trim()
            if ($LASTEXITCODE -ne 0) { throw "$label property $property evaluation failed." }
            if (($property -ceq 'PathMap' -and $effective -cne $value) -or
                ($property -ceq 'Deterministic' -and $effective -cne 'true')) {
                throw "$label $component effective $property mismatch. Expected mapping or deterministic true."
            }
            $evaluations += [ordered]@{ assembly="RecordSift.$component"; property=$property; value=$effective }
        }
    }
    $observations += [ordered]@{ label=$label; source_sha=$frozen; requested_mapping=$value; effective_properties=$evaluations }
    Push-Location $root
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
        if ($LASTEXITCODE -ne 0) { throw "$label restore failed." }
        & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' '/p:Deterministic=true' "/p:PathMap=$value" /verbosity:minimal
        if ($LASTEXITCODE -ne 0) { throw "$label mapped Release rebuild failed." }
    }
    finally { Pop-Location }
    $sideEvidence = Join-Path $evidence "$label-release-evidence"
    & $pilot -ApplicationRoot $root -EvidenceRoot $sideEvidence -ExpectedCommit $frozen -ExperimentId "EXP-020-$label"
    if ($LASTEXITCODE -ne 0) { throw "$label original 425 API/419 NUnit/XML/package/consumer gates failed." }
    Verify-Immutable $root "$label after build and acceptance"
    $readerArgs = @($reader)
    foreach ($component in $components) {
        $name = "RecordSift.$component"
        $binary = Join-Path $root ("src/{0}/bin/Release/{0}.dll" -f $name)
        if (-not (Test-Path $binary)) { throw "$label missing $name compiled DLL." }
        $readerArgs += '--assembly'; $readerArgs += $binary
    }
    $readerArgs += '--output'; $readerArgs += (Join-Path $evidence "$label-pe.json")
    & dotnet @readerArgs
    if ($LASTEXITCODE -ne 0) { throw "$label PE read failed." }
    Write-Host "PASS: $label original acceptance gates, deterministic=true, PathMap=$canonical (source rooted separately)."
}
$observations | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $evidence 'evaluated-pathmap-properties.json') -Encoding utf8
$comparator = Join-Path $repo 'tooling/validators/pe_variation.py'
$mappedReport = Join-Path $evidence 'mapped-cross-worktree.json'
$wrongReport = Join-Path $evidence 'intentionally-wrong-map.json'
& python $comparator --original (Join-Path $evidence 'mapped-original-pe.json') --independent (Join-Path $evidence 'mapped-independent-pe.json') --same-path-rebuild (Join-Path $evidence 'mapped-original-pe.json') --output $mappedReport
if ($LASTEXITCODE -ne 0) { throw 'Correctly mapped PE comparison was incomplete.' }
& python $comparator --original (Join-Path $evidence 'mapped-original-pe.json') --independent (Join-Path $evidence 'wrong-map-independent-pe.json') --same-path-rebuild (Join-Path $evidence 'mapped-original-pe.json') --output $wrongReport
if ($LASTEXITCODE -ne 0) { throw 'Wrong-map negative control comparison incomplete.' }
$correct = Get-Content -LiteralPath $mappedReport -Raw | ConvertFrom-Json
$wrong = Get-Content -LiteralPath $wrongReport -Raw | ConvertFrom-Json
if ($correct.assembly_names.Count -ne 5 -or $wrong.assembly_names.Count -ne 5) { throw 'Comparison omitted a production assembly.' }
# The negative mapping must materially affect at least one compiled DLL.
if ($wrong.independent_worktree.different_binaries -le 0) {
    throw 'Deliberately different mapped source roots had no detectable PE effect; PathMap behavior remains unverified.'
}
$compat = Join-Path $repo 'tooling/validators/compatibility.py'
$baseSnapshot = Join-Path $controls 'baseline-default-release-evidence/baseline.json'
$logical = @()
foreach ($case in $parameters) {
    $label = $case.label
    $dest = Join-Path $evidence "logical-$label.json"
    & python $compat compare --baseline $baseSnapshot --candidate (Join-Path $evidence "$label-release-evidence/baseline.json") --output $dest
    $exitCode = $LASTEXITCODE
    $data = Get-Content $dest -Raw | ConvertFrom-Json
    if ($exitCode -ne 0 -or $data.overall -cne 'matched') {
        throw "$label changed selected logical contract: $($data.overall) (exit=$exitCode)"
    }
    $logical += [ordered]@{ variant=$label; logical_result=$data.overall; source_sha=$frozen }
    $pilotReport = Get-Content (Join-Path $evidence "$label-release-evidence/pilot-report.json") -Raw | ConvertFrom-Json
    if ($pilotReport.source_commit -cne $frozen) { throw "$label pilot attribution does not match frozen source." }
}
$report = [ordered]@{
    experiment='EXP-020'
    frozen_git_sha=$frozen
    frozen_tree_sha=$controlReport.frozen_source_tree
    predecessor_controls='EXP-019 four full release-gated builds passed: no PathMap, same worktree deterministic equality and different-worktree inequality.'
    total_full_release_gated_builds=7
    change_scope='Only MSBuild global Deterministic=true and PathMap mappings; no source/project changes'
    evaluated_pathmap_settings=$observations
    without_pathmap=$controlReport.deterministic_reproducibility
    with_identical_canonical_pathmap=$correct
    intentionally_different_canonical_pathmap=$wrong
    original_logical_contracts=$logical
    negative_control='wrong canonical mapping must change at least one DLL; all builds must still meet logical contracts'
    limitations=@('A matching DLL hash is narrow byte identity, not security or general runtime equivalence.',
                  'Even matching mapped builds on one runner are not cross-machine hermetic attestation.',
                  'Unchanged source SHA is not evidence of identical external dependencies absent independent restore proof.',
                  'Package ZIP container byte hashes and PDB file bytes are not compared in this experiment.',
                  'C# compiler complete argv was not independently captured; MSBuild effective properties were captured.')
}
$report | ConvertTo-Json -Depth 23 | Set-Content (Join-Path $evidence 'experiment-report.json') -Encoding utf8
Write-Host "EXP-020 mapped different-worktree identical DLLs: $($correct.independent_worktree.identical_binaries) / 5"
Write-Host "EXP-020 unmapped different-worktree identical DLLs: $($controlReport.deterministic_reproducibility.independent_worktree.identical_binaries) / 5"
Write-Host "EXP-020 wrong-map negative changed DLLs: $($wrong.independent_worktree.different_binaries) / 5"
Write-Host 'PASS: EXP-020 seven real Release-gated builds and source-path mapping controls; exact byte outcomes captured.'
