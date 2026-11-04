# EXP-022. Add exactly one SourceRoot item only in CI-local, untracked props files.
# Reuse unchanged EXP-021 negative build controls. Never push or publish RecordSift.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ApplicationRoot,
      [Parameter(Mandatory=$true)][string]$EvidenceRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$frozen='8358780829458854a4b0356df5ac5e685f0a34c8'
$original=(Resolve-Path -LiteralPath $ApplicationRoot).Path
$research=(Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$evidence=[IO.Path]::GetFullPath($EvidenceRoot)
if ($evidence.StartsWith($original+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw 'Evidence cannot be inside source.' }
if (Test-Path $evidence) { throw 'Evidence path must not exist.' }
if ((& git -C $original rev-parse HEAD).Trim() -cne $frozen) { throw 'Wrong frozen source commit.' }
$controls=Join-Path $evidence 'negative-controls'
& (Join-Path $research 'tooling/pilots/recordsift/EXP-021/run.ps1') -ApplicationRoot $original -EvidenceRoot $controls | Out-Host
if ($LASTEXITCODE -ne 0) { throw 'EXP-021 negative controls did not execute.' }
$negative=Get-Content (Join-Path $controls 'experiment-report.json') -Raw | ConvertFrom-Json
if ($negative.outcome -cne 'ci_only_build_blocked' -or $negative.frozen_source_sha -cne $frozen -or
    $negative.deterministic_only_control.assembly_names.Count -ne 5) { throw 'Missing verified failed-CI root controls.' }
$other=Join-Path $controls 'deterministic-only-controls/independent-source'
if ((& git -C $other rev-parse HEAD).Trim() -cne $frozen) { throw 'Wrong independent source SHA.' }
$vswhere=Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild=& $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild unavailable.' }
$reader=Join-Path $research 'tooling/pe-provenance/src/bin/Release/net10.0/PeProvenance.dll'
if (-not (Test-Path $reader)) { throw 'Metadata-only PE reader missing.' }
$pilot=Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1'
$components=@('Domain','Application','Infrastructure.Csv','Infrastructure.Reporting','Infrastructure.Xlsx')
$props='<?xml version="1.0" encoding="utf-8"?><Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup><SourceRoot Include="$(MSBuildThisFileDirectory)" /></ItemGroup></Project>'
$inject=@()
foreach ($dir in @($original,$other)) {
    $file=Join-Path $dir 'Directory.Build.props'
    if (Test-Path $file) { throw "Unexpected prior Directory.Build.props at $dir" }
    [IO.File]::WriteAllText($file,$props,[Text.UTF8Encoding]::new($false))
    $tracked=@(& git -C $dir diff --name-only HEAD --)
    if ($LASTEXITCODE -ne 0 -or $tracked.Count -ne 0) { throw 'Root injection modified tracked source.' }
    $inject+=@{source_sha=$frozen;file='Directory.Build.props';sha256=(Get-FileHash $file -Algorithm SHA256).Hash;tracked_source_modified=$false}
}
$cases=@([pscustomobject]@{label='provided-root-original';dir=$original},
         [pscustomobject]@{label='provided-root-other';dir=$other},
         [pscustomobject]@{label='provided-root-samepath-repeat';dir=$original})
$properties=@()
foreach ($case in @($cases | Where-Object {$_.label -cne 'provided-root-samepath-repeat'})) {
    foreach ($component in $components) {
        $proj=Join-Path $case.dir ("src/RecordSift.{0}/RecordSift.{0}.csproj" -f $component)
        $args=@($proj,'/p:Configuration=Release','/p:Platform=AnyCPU','/p:Deterministic=true','/p:ContinuousIntegrationBuild=true','-nologo')
        $roots=@(& $msbuild @args '-getItem:SourceRoot')
        if ($LASTEXITCODE -ne 0 -or (-not (($roots -join ' ') -match 'SourceRoot'))) { throw "No SourceRoot evaluation for $($case.label)/$component" }
        $value=@(& $msbuild @args '-target:_SetPathMapFromSourceRoots' '-getProperty:PathMap')
        if ($LASTEXITCODE -ne 0) { throw "Roslyn path mapping target failed $($case.label)/$component" }
        $mapped=($value -join [Environment]::NewLine).Trim()
        if ([string]::IsNullOrWhiteSpace($mapped) -or -not $mapped.Contains('=')) { throw "No computed compiler path mapping for $($case.label)/$component" }
        $properties+=@{case=$case.label;component=$component;computed_pathmap=$mapped;source_root_present=$true}
    }
}
if ($properties.Count -ne 10) { throw 'Incomplete mapped source roots.' }
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$properties | ConvertTo-Json -Depth 7 | Set-Content (Join-Path $evidence 'computed-pathmaps.json') -Encoding utf8
$accepted=@()
foreach ($case in $cases) {
    $dir=[string]$case.dir;$label=[string]$case.label
    if ((& git -C $dir rev-parse HEAD).Trim() -cne $frozen) { throw "$label invalid source commit." }
    Push-Location $dir
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Out-Host
        if($LASTEXITCODE -ne 0){throw "$label restore failed."}
        & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' '/p:Deterministic=true' '/p:ContinuousIntegrationBuild=true' /verbosity:minimal | Out-Host
        if($LASTEXITCODE -ne 0){throw "$label compilation failed even with SourceRoot."}
    }
    finally{Pop-Location}
    $release=Join-Path $evidence "$label-release-evidence"
    & $pilot -ApplicationRoot $dir -EvidenceRoot $release -ExpectedCommit $frozen -ExperimentId "EXP-022-$label" | Out-Host
    if($LASTEXITCODE -ne 0){throw "$label historical API/NUnit/XML/package/consumer acceptance failed."}
    $changed=@(& git -C $dir diff --name-only HEAD --)
    if($LASTEXITCODE -ne 0 -or $changed.Count -ne 0){throw "$label mutated application tracked source."}
    $metadata=@($reader)
    foreach($comp in $components){
        $assembly="RecordSift.$comp"
        $dll=Join-Path $dir ("src/{0}/bin/Release/{0}.dll" -f $assembly)
        if(-not(Test-Path $dll)){throw "Missing $assembly in $label"}
        $metadata+='--assembly';$metadata+=$dll
    }
    $metadata+='--output';$metadata+=(Join-Path $evidence "$label-pe.json")
    & dotnet @metadata | Out-Host
    if($LASTEXITCODE -ne 0){throw "$label PE metadata reader failed."}
    $accept=Get-Content (Join-Path $release 'pilot-report.json') -Raw | ConvertFrom-Json
    if($accept.source_commit -cne $frozen){throw "$label wrong source attribution."}
    $accepted+=@{name=$label;source=$frozen;build='passed';original_release_gates='passed'}
    Write-Host "PASS: $label manual SourceRoot CI=true compile and all original release gates."
}
$comparisonFile=Join-Path $evidence 'pe-comparison.json'
& python (Join-Path $research 'tooling/validators/pe_variation.py') --original (Join-Path $evidence 'provided-root-original-pe.json') --independent (Join-Path $evidence 'provided-root-other-pe.json') --same-path-rebuild (Join-Path $evidence 'provided-root-samepath-repeat-pe.json') --output $comparisonFile
if($LASTEXITCODE -ne 0){throw 'Missing compiled DLL snapshots.'}
$comparison=Get-Content $comparisonFile -Raw | ConvertFrom-Json
if($comparison.assembly_names.Count -ne 5){throw 'Missing production DLLs in comparison.'}
$logical=@()
foreach($label in @('provided-root-original','provided-root-other','provided-root-samepath-repeat')){
    $out=Join-Path $evidence "$label-logical.json"
    & python (Join-Path $research 'tooling/validators/compatibility.py') compare --baseline (Join-Path $controls 'deterministic-only-controls/baseline-default-release-evidence/baseline.json') --candidate (Join-Path $evidence "$label-release-evidence/baseline.json") --output $out
    $code=$LASTEXITCODE;$res=Get-Content $out -Raw | ConvertFrom-Json
    if($code -ne 0 -or $res.overall -cne 'matched'){throw "$label logical contracts changed."}
    $logical+=@{name=$label;outcome=$res.overall}
}
[ordered]@{
 experiment='EXP-022'
 original_source_commit=$frozen
 change='only untracked Directory.Build.props with one SourceRoot; no Source Link or package migrations'
 prior_ci_without_root=$negative.outcome
 source_root_injection=$inject
 computed_paths=$properties
 total_full_release_gated_builds=7
 candidates=$accepted
 logical_contracts=$logical
 pe_byte_comparison=$comparison
 caveats=@('Not Source Link: no Git URLs are emitted or proven by this experiment.',
            'Identical DLL bytes on one runner do not establish full cross-machine reproducibility.',
            'SourceRoot file is never committed to the application repository.')
} | ConvertTo-Json -Depth 24 | Set-Content (Join-Path $evidence 'experiment-report.json') -Encoding utf8
Write-Host "EXP-022 distinct-worktree DLL byte identity: $($comparison.independent_worktree.identical_binaries) / 5"
Write-Host "EXP-022 same-directory DLL byte identity: $($comparison.same_worktree_rebuild.identical_binaries) / 5"
Write-Host 'PASS: EXP-022 missing SourceRoot resolved with only disposable build metadata, all original gates passed.'
