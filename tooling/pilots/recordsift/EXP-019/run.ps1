# EXP-019 — opt-in Deterministic=true by MSBuild command line only.
# Do not modify traditional csproj, commit changes, or push to RecordSift.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ApplicationRoot,
    [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$frozen = '8358780829458854a4b0356df5ac5e685f0a34c8'
$original = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence = [IO.Path]::GetFullPath($EvidenceRoot)
$research = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
if ($evidence.StartsWith($original + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Evidence must remain outside application source.'
}
if (Test-Path -LiteralPath $evidence) { throw 'Evidence destination must be new.' }
$start = (& git -C $original rev-parse --verify HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $start -cne $frozen) { throw 'Wrong frozen RecordSift commit.' }
if (@(& git -C $original status --porcelain --untracked-files=normal).Count -ne 0) {
    throw 'Original application source must start clean.'
}
New-Item -ItemType Directory -Path $evidence | Out-Null
$independent = Join-Path $evidence 'independent-source'
& git -C $original worktree add --detach $independent $frozen
if ($LASTEXITCODE -ne 0) { throw 'Could not create isolated second source worktree.' }
$sourceTree = (& git -C $original rev-parse 'HEAD^{tree}').Trim()
if ($LASTEXITCODE -ne 0 -or $sourceTree -cne (& git -C $independent rev-parse 'HEAD^{tree}').Trim()) {
    throw 'Source tree SHA mismatch between same-commit worktrees.'
}
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild is required.' }
$reader = Join-Path $research 'tooling/pe-provenance/src/bin/Release/net10.0/PeProvenance.dll'
if (-not (Test-Path -LiteralPath $reader)) { throw 'Build metadata-only PE reader first.' }
$pilot = Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1'
$components = @('Domain', 'Application', 'Infrastructure.Csv', 'Infrastructure.Reporting', 'Infrastructure.Xlsx')
$names = @($components | ForEach-Object { "RecordSift.$_" })
$propertyRows = @()
foreach ($mode in @('original-default', 'deterministic-cli')) {
    foreach ($component in $components) {
        $project = Join-Path $original ("src/RecordSift.{0}/RecordSift.{0}.csproj" -f $component)
        $args = @($project, '-getProperty:Deterministic', '/p:Configuration=Release', '/p:Platform=AnyCPU', '-nologo')
        if ($mode -ceq 'deterministic-cli') { $args += '/p:Deterministic=true' }
        $value = ((& $msbuild @args) -join [Environment]::NewLine).Trim()
        if ($LASTEXITCODE -ne 0) { throw "Deterministic evaluation failed for $mode $component" }
        if ($mode -ceq 'deterministic-cli' -and $value -cne 'true') {
            throw "Expected effective Deterministic=true for $component; evaluated '$value'"
        }
        $propertyRows += [ordered]@{ mode=$mode; project="RecordSift.$component"; configuration='Release'; deterministic=$value }
    }
}
$propertyRows | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $evidence 'effective-deterministic-settings.json') -Encoding utf8
[ordered]@{
    frozen_source_sha=$frozen
    frozen_tree_sha=$sourceTree
    windows=[Environment]::OSVersion.VersionString
    dotnet_sdk=(& dotnet --version).Trim()
    msbuild_path=$msbuild
    msbuild_version=((& $msbuild -version -nologo) | Select-Object -Last 1).Trim()
    powershell=$PSVersionTable.PSVersion.ToString()
    compiler_switch='global /p:Deterministic=true for all 10 project rebuilds; command line only'
} | ConvertTo-Json | Set-Content (Join-Path $evidence 'toolchain.json') -Encoding utf8

function Check-FrozenSource([string]$root, [string]$context) {
    $actual = (& git -C $root rev-parse --verify HEAD).Trim()
    $paths = @(& git -C $root diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0 -or $actual -cne $frozen -or $paths.Count -ne 0) {
        throw "$context changed RecordSift tracked source or its Git SHA."
    }
}
function Invoke-BuildAndAcceptance([string]$root, [string]$label, [bool]$deterministic) {
    Check-FrozenSource $root "$label before build"
    Push-Location $root
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
        if ($LASTEXITCODE -ne 0) { throw "$label NuGet restore failed." }
        $args = @('RecordSift.sln', '/m', '/t:Rebuild', '/p:Configuration=Release', '/p:Platform=Any CPU', '/verbosity:minimal')
        if ($deterministic) { $args += '/p:Deterministic=true' }
        & $msbuild @args
        if ($LASTEXITCODE -ne 0) { throw "$label Release rebuild failed." }
    }
    finally { Pop-Location }
    $sideEvidence = Join-Path $evidence "$label-release-evidence"
    & $pilot -ApplicationRoot $root -EvidenceRoot $sideEvidence -ExpectedCommit $frozen -ExperimentId "EXP-019-$label"
    if ($LASTEXITCODE -ne 0) { throw "$label original API/NUnit/XML/package/consumer gates failed." }
    Check-FrozenSource $root "$label after release gates"
    $args = @($reader)
    foreach ($name in $names) {
        $assembly = Join-Path $root ("src/{0}/bin/Release/{0}.dll" -f $name)
        if (-not (Test-Path -LiteralPath $assembly)) { throw "Missing $label $name" }
        $args += '--assembly'; $args += $assembly
    }
    $args += '--output'; $args += (Join-Path $evidence "$label-pe.json")
    & dotnet @args
    if ($LASTEXITCODE -ne 0) { throw "$label metadata-only PE read failed." }
    Write-Host "PASS: $label source=$frozen deterministic_override=$deterministic full release/consumer gates."
}
# Baseline compiled exactly as original historical source, no build overrides.
Invoke-BuildAndAcceptance $original 'baseline-default' $false
# Only compiler-property override: same frozen source, no on-disk project modifications.
Invoke-BuildAndAcceptance $original 'deterministic-first' $true
Invoke-BuildAndAcceptance $independent 'deterministic-other-worktree' $true
Invoke-BuildAndAcceptance $original 'deterministic-samepath-repeat' $true

$comparator = Join-Path $research 'tooling/validators/pe_variation.py'
& python $comparator --original (Join-Path $evidence 'deterministic-first-pe.json') --independent (Join-Path $evidence 'deterministic-other-worktree-pe.json') --same-path-rebuild (Join-Path $evidence 'deterministic-samepath-repeat-pe.json') --output (Join-Path $evidence 'deterministic-reproducibility.json')
if ($LASTEXITCODE -ne 0) { throw 'Deterministic build PE report incomplete.' }
& python $comparator --original (Join-Path $evidence 'baseline-default-pe.json') --independent (Join-Path $evidence 'deterministic-first-pe.json') --same-path-rebuild (Join-Path $evidence 'deterministic-first-pe.json') --output (Join-Path $evidence 'baseline-versus-opt-in.json')
if ($LASTEXITCODE -ne 0) { throw 'Baseline vs opt-in PE report incomplete.' }
$det = Get-Content -LiteralPath (Join-Path $evidence 'deterministic-reproducibility.json') -Raw | ConvertFrom-Json
$base = Get-Content -LiteralPath (Join-Path $evidence 'baseline-versus-opt-in.json') -Raw | ConvertFrom-Json
if ($det.assembly_names.Count -ne 5 -or $base.assembly_names.Count -ne 5) { throw 'Missing one or more production PE observations.' }
# The new compiler setting must not alter the selected logical compatibility evidence.
$compatibility = Join-Path $research 'tooling/validators/compatibility.py'
$relations = @()
foreach ($side in @('deterministic-first', 'deterministic-other-worktree', 'deterministic-samepath-repeat')) {
    $out = Join-Path $evidence ("logical-compatibility-" + $side + ".json")
    & python $compatibility compare --baseline (Join-Path $evidence 'baseline-default-release-evidence/baseline.json') --candidate (Join-Path $evidence "$side-release-evidence/baseline.json") --output $out
    $code = $LASTEXITCODE
    $result = Get-Content $out -Raw | ConvertFrom-Json
    if ($code -ne 0 -or $result.overall -cne 'matched') {
        throw "Unexpected $side logical compatibility changes: $($result.overall) exit=$code"
    }
    $relations += [ordered]@{ side=$side; status=$result.overall; categories=@($result.components.PSObject.Properties.Name) }
}
foreach ($side in @('baseline-default', 'deterministic-first', 'deterministic-other-worktree', 'deterministic-samepath-repeat')) {
    $report = Get-Content -LiteralPath (Join-Path $evidence "$side-release-evidence/pilot-report.json") -Raw | ConvertFrom-Json
    if ($report.source_commit -cne $frozen) { throw "Unexpected $side source provenance." }
}
$summary = [ordered]@{
    experiment='EXP-019'
    frozen_source_sha=$frozen
    frozen_source_tree=$sourceTree
    candidate_source_mutation='none: only MSBuild global /p:Deterministic=true'
    builds=@('historical default', 'deterministic same checkout A', 'deterministic distinct checkout B', 'deterministic same checkout A rebuild')
    effective_settings=$propertyRows
    acceptance='All four ten-project Release builds; 425-entry API, 419 NUnit 418 pass 1 skip, XML/package/clean installed consumers accepted individually.'
    selected_logical_contracts=$relations
    deterministic_reproducibility=$det
    baseline_vs_explicit=$base
    observed_not_assumed='Same and differing bytes are evidence; deterministic compiler property alone does not guarantee byte identity across all paths/environments.'
    no_application_commit_or_package_publication=$true
}
$summary | ConvertTo-Json -Depth 22 | Set-Content (Join-Path $evidence 'experiment-report.json') -Encoding utf8
Write-Host "PASS: EXP-019 three opt-in deterministic builds + historical baseline; all full acceptance gates and logical contract matches."
