# EXP-021 — isolate legacy MSBuild ContinuousIntegrationBuild=true without Source Link.
# Never modifies RecordSift, its project files, dependencies or repository branches.
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
    throw 'Evidence must be outside source checkout.'
}
if (Test-Path -LiteralPath $evidence) { throw 'Evidence destination must be new.' }
if ((& git -C $original rev-parse HEAD).Trim() -cne $frozen -or
    @(& git -C $original status --porcelain --untracked-files=normal).Count -ne 0) {
    throw 'Original RecordSift source must match immutable baseline and start clean.'
}
New-Item -ItemType Directory -Path $evidence | Out-Null
# Reuse EXP-019 as an explicit verified negative control, unchanged:
# 4 full historical + deterministic-only Release/consumer builds with immutable
# source, comparing cross-directory and same-directory PE hashes.
$controls = Join-Path $evidence 'deterministic-only-controls'
& (Join-Path $research 'tooling/pilots/recordsift/EXP-019/run.ps1') -ApplicationRoot $original -EvidenceRoot $controls
if ($LASTEXITCODE -ne 0) { throw 'Original EXP-019 controls failed.' }
$control = Get-Content (Join-Path $controls 'experiment-report.json') -Raw | ConvertFrom-Json
if ($control.frozen_source_sha -cne $frozen -or
    $control.deterministic_reproducibility.assembly_names.Count -ne 5 -or
    $control.deterministic_reproducibility.same_worktree_rebuild.identical_binaries -ne 5 -or
    $control.deterministic_reproducibility.independent_worktree.different_binaries -le 0) {
    throw 'Unmodified deterministic-only evidence was incomplete or inconsistent.'
}
$independent = Join-Path $controls 'independent-source'
if ((& git -C $independent rev-parse HEAD).Trim() -cne $frozen) { throw 'Independent worktree must match frozen SHA.' }

$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild not found.' }
$reader = Join-Path $research 'tooling/pe-provenance/src/bin/Release/net10.0/PeProvenance.dll'
if (-not (Test-Path -LiteralPath $reader)) { throw 'Required metadata-only PE reader not built.' }
$pilot = Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1'
$names = @('Domain', 'Application', 'Infrastructure.Csv', 'Infrastructure.Reporting', 'Infrastructure.Xlsx')
$properties = @('Deterministic', 'ContinuousIntegrationBuild', 'DeterministicSourcePaths', 'PathMap')
$evaluations = @()
foreach ($side in @([pscustomobject]@{ label='original'; root=$original },
                    [pscustomobject]@{ label='independent'; root=$independent })) {
    foreach ($component in $names) {
        $project = Join-Path $side.root ("src/RecordSift.{0}/RecordSift.{0}.csproj" -f $component)
        foreach ($mode in @('deterministic-only', 'ci-property-only')) {
            foreach ($prop in $properties) {
                $argv = @($project, "-getProperty:$prop", '/p:Configuration=Release', '/p:Platform=AnyCPU',
                          '/p:Deterministic=true', '-nologo')
                if ($mode -ceq 'ci-property-only') { $argv += '/p:ContinuousIntegrationBuild=true' }
                $value = ((& $msbuild @argv) -join [Environment]::NewLine).Trim()
                if ($LASTEXITCODE -ne 0) { throw "Could not evaluate $($side.label) $component $mode $prop" }
                if ($prop -ceq 'Deterministic' -and $value -cne 'true') { throw 'Deterministic property was not honored.' }
                if ($prop -ceq 'ContinuousIntegrationBuild' -and $mode -ceq 'ci-property-only' -and $value -cne 'true') {
                    throw 'MSBuild did not recognize explicit ContinuousIntegrationBuild global property.'
                }
                $evaluations += [ordered]@{ side=$side.label; project="RecordSift.$component"; mode=$mode; name=$prop; value=$value }
            }
        }
    }
}
if ($evaluations.Count -ne 80) { throw "Missing evaluated property evidence: $($evaluations.Count)/80" }
$evaluations | ConvertTo-Json -Depth 7 | Set-Content (Join-Path $evidence 'effective-properties.json') -Encoding utf8
Write-Host 'EXP-021 compared actual Release MSBuild properties for deterministic-only vs CI=true:'
foreach ($r in @($evaluations | Where-Object { $_.side -eq 'original' -and $_.project -ceq 'RecordSift.Domain' })) {
    Write-Host ("$($r.mode): $($r.name)=$($r.value)")
}
$components = @($names | ForEach-Object { "RecordSift.$_" })
$results = @()

function Check-Frozen([string]$root, [string]$phase) {
    $commit = (& git -C $root rev-parse HEAD).Trim()
    $tracked = @(& git -C $root diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0 -or $commit -cne $frozen -or $tracked.Count -ne 0) { throw "$phase modified frozen source." }
}
function Run-CiCandidate([string]$root, [string]$label) {
    Check-Frozen $root "$label before build"
    Push-Location $root
    $output = @()
    $exit = 2
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Out-Host
        if ($LASTEXITCODE -ne 0) { throw "$label NuGet restore failed." }
        $output = @(& $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' '/p:Deterministic=true' '/p:ContinuousIntegrationBuild=true' /verbosity:minimal 2>&1)
        $exit = $LASTEXITCODE
    }
    finally { Pop-Location }
    $codeText = ($output | ForEach-Object { $_.ToString() }) -join [Environment]::NewLine
    $buildErrors = @([regex]::Matches($codeText, '\b(?:MSB|CS)\d{4}\b') | ForEach-Object { $_.Value } | Sort-Object -Unique)
    if ($exit -ne 0) {
        # An unsuccessful candidate is valid negative evidence, but is NOT a
        # passed API/test/pack/consumer gate. Never hide the unavailable gates.
        $limited = @($output | ForEach-Object { $_.ToString() } | Where-Object { $_ -match ':\s*error\s|\berror (?:MSB|CS)\d{4}\b' } | Select-Object -First 15)
        Write-Host "OBSERVED: $label CI-only candidate does not compile (exit $exit); error codes: $($buildErrors -join ',')"
        $limited | ForEach-Object { Write-Host ("Compiler diagnostic: " + $_) }
        Check-Frozen $root "$label failed build"
        return [ordered]@{ label=$label; build='failed'; build_exit=$exit; error_codes=$buildErrors; full_release_gates='not_run'; pe='not_available'; source_sha=$frozen }
    }
    $releaseDir = Join-Path $evidence "$label-release-evidence"
    & $pilot -ApplicationRoot $root -EvidenceRoot $releaseDir -ExpectedCommit $frozen -ExperimentId "EXP-021-$label" | Out-Host
    if ($LASTEXITCODE -ne 0) { throw "$label compiled but historical API/NUnit/XML/NuGet/consumer release acceptance FAILED." }
    Check-Frozen $root "$label after release acceptance"
    $args = @($reader)
    foreach ($name in $components) {
        $path = Join-Path $root ("src/{0}/bin/Release/{0}.dll" -f $name)
        if (-not (Test-Path $path)) { throw "$label missing compiled $name." }
        $args += '--assembly'; $args += $path
    }
    $args += '--output'; $args += (Join-Path $evidence "$label-pe.json")
    & dotnet @args
    if ($LASTEXITCODE -ne 0) { throw "$label metadata-only PE inspection failed." }
    Write-Host "PASS: $label actual CI=true compile and all historical release/consumer gates."
    return [ordered]@{ label=$label; build='passed'; build_exit=0; error_codes=@(); full_release_gates='passed'; pe='captured'; source_sha=$frozen }
}
$results += Run-CiCandidate $original 'ci-original'
$results += Run-CiCandidate $independent 'ci-independent'
if ($results.Count -ne 2) { throw 'Missing required distinct-worktree build attempts.' }

$report = [ordered]@{
    experiment='EXP-021'
    target='traditional non-SDK net48 without Source Link package, all five production projects'
    frozen_source_sha=$frozen
    frozen_tree_sha=$control.frozen_source_tree
    mutation='none: only global /p:Deterministic=true /p:ContinuousIntegrationBuild=true, compared with unchanged EXP-019'
    evaluated_property_count=$evaluations.Count
    ci_attempts=$results
    deterministic_only_control=$control.deterministic_reproducibility
    outcome='pending'
    claim_limitations=@(
        'Property evaluation and successful/failed builds do not alone prove an actual /pathmap compiler argument.',
        'An unsuccessful CI build is a negative outcome and has not passed the historical acceptance gates.',
        'Two identical source SHA worktrees do not constitute hermetically identical environments.',
        'Do not attribute missing CI path normalization to Source Link: this experiment intentionally has no Source Link package.')
}
if (@($results | Where-Object { $_['build'] -eq 'failed' }).Count -gt 0) {
    # Both builds are attempted and captured: classify as blocked, not equivalent.
    $report.outcome='ci_only_build_blocked'
    Write-Host 'OBSERVED: CI property alone could not pass the existing build; no compatibility/reproducibility claim.'
}
else {
    $results += Run-CiCandidate $original 'ci-samepath-repeat'
    if ($results[-1]['build'] -ne 'passed') { throw 'Same-path CI candidate repeat failed; no valid reproducibility comparison.' }
    $report.ci_attempts=$results
    $comparison = Join-Path $research 'tooling/validators/pe_variation.py'
    $ciOutput = Join-Path $evidence 'ci-property-pe-variation.json'
    & python $comparison --original (Join-Path $evidence 'ci-original-pe.json') --independent (Join-Path $evidence 'ci-independent-pe.json') --same-path-rebuild (Join-Path $evidence 'ci-samepath-repeat-pe.json') --output $ciOutput
    if ($LASTEXITCODE -ne 0) { throw 'CI-only actual PE snapshots missing or malformed.' }
    $pe = Get-Content $ciOutput -Raw | ConvertFrom-Json
    if ($pe.assembly_names.Count -ne 5) { throw 'Five compiled production DLLs required.' }
    $report.pe_variation=$pe
    $compat = Join-Path $research 'tooling/validators/compatibility.py'
    $logical=@()
    foreach ($label in @('ci-original', 'ci-independent', 'ci-samepath-repeat')) {
        $out = Join-Path $evidence "$label-logical.json"
        & python $compat compare --baseline (Join-Path $controls 'baseline-default-release-evidence/baseline.json') --candidate (Join-Path $evidence "$label-release-evidence/baseline.json") --output $out
        $exitCode = $LASTEXITCODE
        $result = Get-Content $out -Raw | ConvertFrom-Json
        if ($exitCode -ne 0 -or $result.overall -cne 'matched') { throw "$label selected logical contracts changed or missing: $($result.overall)" }
        $logical += [ordered]@{ label=$label; status=$result.overall }
    }
    $report.logical_compatibility=$logical
    $report.outcome='ci_only_builds_accepted_with_metadata_observations'
    Write-Host ("EXP-021 CI=true independent worktree identical compiled DLLs: " + $pe.independent_worktree.identical_binaries + " / 5")
    Write-Host ("EXP-021 deterministic-only independent worktree identical DLLs: " + $control.deterministic_reproducibility.independent_worktree.identical_binaries + " / 5")
}
$report | ConvertTo-Json -Depth 22 | Set-Content (Join-Path $evidence 'experiment-report.json') -Encoding utf8
Write-Host "EXP-021 research completed: $($report.outcome). Preserve different outcomes honestly."
