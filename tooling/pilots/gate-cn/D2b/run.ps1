# D2b: two original (public dummy only) traditional net48 compiled candidates
# used to test actual LOCAL NuGet restore/CopyLocal and real .NET Framework CLR.
# This is research, not a NuGet publisher, production gate or app modification.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ExpectedCommit)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root = (Resolve-Path -LiteralPath $env:GITHUB_WORKSPACE).Path
$fixture = Join-Path $root 'tooling/fixtures/gate-cn/D2a'
$tracked = Join-Path $fixture 'Tracked.cs'
$project = Join-Path $fixture 'D2a.Probe.csproj'
$private = Join-Path $env:RUNNER_TEMP 'gate-cn-d2b-private'
$output = Join-Path $env:RUNNER_TEMP 'gate-cn-d2b-sanitized.json'
$template = Join-Path $root 'tooling/fixtures/gate-cn/D2b/Consumer'
$loader = Join-Path $root 'tooling/pilots/gate-cn/D2b/load_consumer_in_netfx.ps1'
$verifier = Join-Path $root 'tooling/pilots/gate-cn/D2b/verify_nuget_chain.py'
$bin = Join-Path $fixture 'bin'
$obj = Join-Path $fixture 'obj'

if ($ExpectedCommit -cnotmatch '^[0-9a-f]{40}$' -or
    (& git -C $root rev-parse HEAD).Trim() -cne $ExpectedCommit -or
    $LASTEXITCODE -ne 0) {
    throw 'D2B_WRONG_IMMUTABLE_RESEARCH_CHECKOUT'
}
foreach ($path in @($private, $output, $bin, $obj)) {
    if (Test-Path -LiteralPath $path) {
        throw 'D2B_DISPOSABLE_ROOT_NOT_CLEAN'
    }
}
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
if (-not (Test-Path -LiteralPath $vswhere)) { throw 'D2B_MSBUILD_DISCOVERY_MISSING' }
$msbuild = (& $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' |
    Select-Object -First 1)
if (-not $msbuild) { throw 'D2B_MSBUILD_MISSING' }
& dotnet --version *> $null
if ($LASTEXITCODE -ne 0) { throw 'D2B_DOTNET_RESTORE_SDK_MISSING' }
New-Item -ItemType Directory -Path $private -Force | Out-Null
$sourceSha = (Get-FileHash -LiteralPath $tracked -Algorithm SHA256).Hash

function Build-DisposableCandidate {
    param([string]$Label, [string]$Define)
    if ((Test-Path -LiteralPath $bin) -or (Test-Path -LiteralPath $obj)) {
        throw 'D2B_CANDIDATE_BUILD_ROOT_NOT_FRESH'
    }
    $variant = Join-Path $private ('variant-' + $Label)
    New-Item -ItemType Directory -Path $variant -Force | Out-Null
    $args = @(
        $project, '/t:Rebuild', '/m:1', '/nologo', '/verbosity:minimal',
        '/p:Configuration=Release', '/p:Platform=AnyCPU',
        '/p:Deterministic=true', '/p:DebugType=pdbonly',
        "/p:DefineConstants=$Define"
    )
    & $msbuild @args *> (Join-Path $variant 'private-build.log')
    if ($LASTEXITCODE -ne 0) { throw 'D2B_TRADITIONAL_NET48_BUILD_FAILED' }
    $dll = Join-Path $fixture 'bin/Release/D2a.Probe.dll'
    $pdb = Join-Path $fixture 'bin/Release/D2a.Probe.pdb'
    if (-not (Test-Path -LiteralPath $dll) -or -not (Test-Path -LiteralPath $pdb)) {
        throw 'D2B_REAL_NATIVE_PDB_OR_DLL_MISSING'
    }
    Copy-Item -LiteralPath $dll -Destination (Join-Path $variant 'D2a.Probe.dll')
    Copy-Item -LiteralPath $pdb -Destination (Join-Path $variant 'D2a.Probe.pdb')
    if ((Get-FileHash -LiteralPath $tracked -Algorithm SHA256).Hash -cne $sourceSha) {
        throw 'D2B_SOURCE_BYTES_CHANGED'
    }
    Remove-Item -LiteralPath $bin -Recurse -Force -ErrorAction Stop
    Remove-Item -LiteralPath $obj -Recurse -Force -ErrorAction Stop
}
Build-DisposableCandidate -Label 'a' -Define 'D2A_BASE'
Build-DisposableCandidate -Label 'b' -Define 'D2A_ALT'

# Python uses only locally constructed OPC NuGet archives and isolated
# private NuGet.Config with packageSources CLEAR. It invokes REAL dotnet
# restore and build from local feeds; no nuget.org or package publication.
& python $verifier --private-root $private --consumer-template $template --netfx-loader $loader --output $output
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $output)) {
    throw 'D2B_LOCAL_NUGET_AND_CLR_NEGATIVES_INCOMPLETE'
}
$report = Get-Content -LiteralPath $output -Raw -Encoding utf8 | ConvertFrom-Json
if ($report.experiment -cne 'D2b' -or
    $report.verdict -cne 'LOCAL_REAL_NUGET_AND_CLR_RESEARCH_VERIFIED_ONLY' -or
    $report.two_real_compiler_variants -cne 'VERIFIED_DISTINCT' -or
    $report.two_actual_local_feed_restores -cne 'VERIFIED_ISOLATED' -or
    $report.two_real_netfx_consumer_loads -cne 'VERIFIED' -or
    $report.negative_controls.Count -ne 5 -or
    @($report.negative_controls | Where-Object { $_.status -cne 'PASS' }).Count -ne 0 -or
    $report.original_gate_c -cne 'UNSATISFIED' -or
    $report.native_gate_cn_release -cne 'NOT_AUTHORIZED' -or
    $report.source_link_production -cne 'HOLD') {
    throw 'D2B_NEGATIVE_CONTROL_REPORT_NOT_ACCEPTABLE'
}
Write-Host 'D2b REAL local NuGet restore/consumer CLR, two feeds, five candidate identity negatives PASS'
Write-Host 'D2b research only; Gate C UNSATISFIED; C-N release NOT_AUTHORIZED; Source Link HOLD'
