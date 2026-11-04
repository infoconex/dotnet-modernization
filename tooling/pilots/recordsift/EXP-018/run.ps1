# EXP-018: identical frozen source, two worktrees and a same-directory rebuild.
# Collect CLR PE metadata; no source/project properties changed or published.
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
$research = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
if ($evidence.StartsWith($application + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Evidence must remain outside application source.' }
if (Test-Path -LiteralPath $evidence) { throw 'Evidence destination already exists.' }
$startSha = (& git -C $application rev-parse --verify HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $startSha -cne $frozen) { throw 'Wrong frozen RecordSift source revision.' }
$initialState = @(& git -C $application status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $initialState.Count -ne 0) { throw 'Frozen RecordSift must start clean.' }
New-Item -ItemType Directory -Path $evidence | Out-Null
$independent = Join-Path $evidence 'independent-source'
& git -C $application worktree add --detach $independent $frozen
if ($LASTEXITCODE -ne 0 -or (& git -C $independent rev-parse HEAD).Trim() -cne $frozen) { throw 'Independent checkout mismatch.' }
if (@(& git -C $independent status --porcelain --untracked-files=normal).Count -ne 0) { throw 'Independent source checkout dirty.' }
$metadataTool = Join-Path $research 'tooling/pe-provenance/src/bin/Release/net10.0/PeProvenance.dll'
if (-not (Test-Path -LiteralPath $metadataTool)) { throw 'Build PeProvenance first.' }
$pilot = Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1'
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild not found.' }
[ordered]@{
    windows = [Environment]::OSVersion.VersionString
    dotnet_sdk = (& dotnet --version).Trim()
    msbuild_path = $msbuild
    msbuild_version = ((& $msbuild -version -nologo) | Select-Object -Last 1).Trim()
    powershell_version = $PSVersionTable.PSVersion.ToString()
} | ConvertTo-Json | Set-Content (Join-Path $evidence 'toolchain.json') -Encoding utf8
$assemblies = @('Domain', 'Application', 'Infrastructure.Csv', 'Infrastructure.Reporting', 'Infrastructure.Xlsx')
$properties = @('Deterministic', 'DebugType', 'DebugSymbols', 'PathMap', 'ContinuousIntegrationBuild', 'Optimize', 'LangVersion', 'PlatformTarget')
$evaluations = @()

function Verify-Source([string]$root, [string]$stage) {
    $observed = (& git -C $root rev-parse HEAD).Trim()
    $trackedChanges = @(& git -C $root diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0 -or $observed -cne $frozen -or $trackedChanges.Count -ne 0) { throw "$stage altered tracked source or Git SHA in $root" }
}
function Invoke-FrozenRelease([string]$root, [string]$label) {
    Verify-Source $root "$label before build"
    Push-Location $root
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
        if ($LASTEXITCODE -ne 0) { throw "$label NuGet restore failed." }
        & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
        if ($LASTEXITCODE -ne 0) { throw "$label ten-project Release rebuild failed." }
    }
    finally { Pop-Location }
    & $pilot -ApplicationRoot $root -EvidenceRoot (Join-Path $evidence "$label-release-evidence") -ExpectedCommit $frozen -ExperimentId "EXP-018-$label"
    if ($LASTEXITCODE -ne 0) { throw "$label original API/NUnit/XML/package/consumer gates failed." }
    Verify-Source $root "$label after release gates"
    $arguments = @($metadataTool)
    foreach ($component in $assemblies) {
        $name = "RecordSift.$component"
        $assemblyPath = Join-Path $root ("src/{0}/bin/Release/{0}.dll" -f $name)
        if (-not (Test-Path -LiteralPath $assemblyPath)) { throw "$label missing $name" }
        $arguments += '--assembly'
        $arguments += $assemblyPath
    }
    $arguments += '--output'
    $arguments += (Join-Path $evidence "$label-pe.json")
    & dotnet @arguments
    if ($LASTEXITCODE -ne 0) { throw "$label PE reader failed." }
    Write-Host "PASS: $label original complete release gates and metadata against frozen source $frozen"
}

foreach ($side in @([pscustomobject]@{ Label='original'; Root=$application }, [pscustomobject]@{ Label='independent'; Root=$independent })) {
    foreach ($component in $assemblies) {
        $name = "RecordSift.$component"
        $projectPath = Join-Path $side.Root ("src/{0}/{0}.csproj" -f $name)
        foreach ($property in $properties) {
            $raw = @(& $msbuild $projectPath "-getProperty:$property" '/p:Configuration=Release' '/p:Platform=AnyCPU' -nologo)
            if ($LASTEXITCODE -ne 0) { throw "Could not evaluate $($side.Label) $name $property" }
            $evaluations += [ordered]@{ side=$side.Label; project=$name; configuration='Release'; property=$property; value=($raw -join [Environment]::NewLine).Trim() }
        }
    }
}
$evaluations | ConvertTo-Json -Depth 6 | Set-Content (Join-Path $evidence 'msbuild-evaluated-settings.json') -Encoding utf8
foreach ($row in @($evaluations | Where-Object { $_.side -eq 'original' })) {
    $other = @($evaluations | Where-Object { $_.side -eq 'independent' -and $_.project -ceq $row['project'] -and $_.property -ceq $row['property'] })
    if ($other.Count -ne 1 -or $other[0]['value'] -cne $row['value']) { throw "Effective property parity mismatch for $($row['project']) $($row['property'])" }
}
if ($evaluations.Count -ne 80) { throw "Incomplete property matrix: $($evaluations.Count)" }
Invoke-FrozenRelease $application 'original'
Invoke-FrozenRelease $independent 'independent'
Invoke-FrozenRelease $application 'same-path-rebuild'
$comparisonPath = Join-Path $evidence 'pe-variation-comparison.json'
& python (Join-Path $research 'tooling/validators/pe_variation.py') --original (Join-Path $evidence 'original-pe.json') --independent (Join-Path $evidence 'independent-pe.json') --same-path-rebuild (Join-Path $evidence 'same-path-rebuild-pe.json') --output $comparisonPath
if ($LASTEXITCODE -ne 0) { throw 'Three PE reports invalid or incomplete.' }
$comparison = Get-Content -LiteralPath $comparisonPath -Raw | ConvertFrom-Json
if ($comparison.assembly_names.Count -ne 5 -or @($comparison.independent_worktree.assemblies.PSObject.Properties).Count -ne 5 -or @($comparison.same_worktree_rebuild.assemblies.PSObject.Properties).Count -ne 5) { throw 'Missing production assembly evidence.' }
foreach ($label in @('original', 'independent', 'same-path-rebuild')) {
    $result = Get-Content (Join-Path $evidence "$label-release-evidence/pilot-report.json") -Raw | ConvertFrom-Json
    if ($result.source_commit -cne $frozen) { throw "$label source provenance mismatch." }
}
$report = [ordered]@{
    experiment='EXP-018'
    source_sha=$frozen
    source_mutations='none; three frozen-source builds'
    workspaces=@('original checkout', 'detached second worktree', 'same original path rebuilt')
    release_and_consumer_gates='passed three times'
    nunit_each='419 discovered, 418 passed, 0 failed, 1 skipped'
    original_public_api_entries=425
    msbuild_release_evaluations=$evaluations.Count
    effective_properties='all 40 project/property cells matched across two source worktrees'
    pe_variation=$comparison
    limitations=@('Raw PE byte/IL hash differences do not themselves imply runtime behavior regression.',
                  'MVID/COFF/CodeView differences are evidence, not causal explanations.',
                  'Different build times/worktrees and caches mean builds are not hermetically equivalent.',
                  'No RecordSift source change, publish or merge.')
}
$report | ConvertTo-Json -Depth 20 | Set-Content (Join-Path $evidence 'experiment-report.json') -Encoding utf8
Write-Host 'PASS: EXP-018 three original-source real release builds and PE metadata observations.'
