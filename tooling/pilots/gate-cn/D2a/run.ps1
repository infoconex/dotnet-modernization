# D2a: ONE disposable net48 native-PDB project, exact research checkout,
# two fresh real compiler invocations and five controlled research negatives.
# This is NOT a production gate; private data remains on hosted Windows runner.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ExpectedCommit)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root = (Resolve-Path -LiteralPath $env:GITHUB_WORKSPACE).Path
$fixture = Join-Path $root 'tooling/fixtures/gate-cn/D2a'
$project = Join-Path $fixture 'D2a.Probe.csproj'
$tracked = Join-Path $fixture 'Tracked.cs'
$private = Join-Path $env:RUNNER_TEMP 'gate-cn-d2a-private'
$sanitized = Join-Path $env:RUNNER_TEMP 'gate-cn-d2a-sanitized.json'
$loggerSource = Join-Path $root 'tooling/pilots/gate-cn/D2a/D2aCscWitnessLogger.cs'
$loggerDll = Join-Path $private 'D2aCscWitnessLogger.dll'
$loader = Join-Path $root 'tooling/pilots/gate-cn/D2a/load_in_netfx.ps1'
$verifier = Join-Path $root 'tooling/pilots/gate-cn/D2a/verify_real_controls.py'
$bin = Join-Path $fixture 'bin'
$obj = Join-Path $fixture 'obj'

if ($ExpectedCommit -cnotmatch '^[0-9a-f]{40}$' -or
    (& git -C $root rev-parse HEAD).Trim() -cne $ExpectedCommit -or
    $LASTEXITCODE -ne 0) {
    throw 'D2A_WRONG_IMMUTABLE_RESEARCH_CHECKOUT'
}
foreach ($path in @($private, $sanitized, $bin, $obj)) {
    if (Test-Path -LiteralPath $path) {
        throw 'D2A_DISPOSABLE_OUTPUT_ROOT_NOT_CLEAN'
    }
}

$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
if (-not (Test-Path -LiteralPath $vswhere)) { throw 'D2A_MSBUILD_DISCOVERY_MISSING' }
$msbuild = (& $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' |
    Select-Object -First 1)
if (-not $msbuild) { throw 'D2A_MSBUILD_MISSING' }
$compiler = Join-Path (Split-Path -Parent $msbuild) 'Roslyn/csc.exe'
$framework = Join-Path (Split-Path -Parent $msbuild) 'Microsoft.Build.Framework.dll'
if (-not (Test-Path -LiteralPath $compiler) -or -not (Test-Path -LiteralPath $framework)) {
    throw 'D2A_COMPILER_OR_MSBUILD_FRAMEWORK_MISSING'
}
New-Item -ItemType Directory -Path $private -Force | Out-Null

& $compiler '/nologo' '/target:library' '/langversion:7.3' "/reference:$framework" '/reference:System.Core.dll' "/out:$loggerDll" $loggerSource *> (Join-Path $private 'logger-compilation.log')
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $loggerDll)) {
    throw 'D2A_PRIVATE_CSC_WITNESS_LOGGER_BUILD_FAILED'
}
$sourceSha = (Get-FileHash -LiteralPath $tracked -Algorithm SHA256).Hash

function Build-RealVariant {
    param(
        [Parameter(Mandatory=$true)][string]$Label,
        [Parameter(Mandatory=$true)][string]$Define
    )
    # Require truly empty output directories, not just Rebuild's intended clean.
    if ((Test-Path -LiteralPath $bin) -or (Test-Path -LiteralPath $obj)) {
        throw 'D2A_OUTPUT_ROOT_NOT_FRESH_BEFORE_COMPILATION'
    }
    $variant = Join-Path $private ("variant-" + $Label)
    New-Item -ItemType Directory -Path $variant | Out-Null
    $witness = Join-Path $variant 'csc-witness.tsv'
    $diagnostic = Join-Path $variant 'private-msbuild.log'

    $buildArgs = @(
        $project,
        '/t:Rebuild',
        '/m:1',
        '/nologo',
        '/verbosity:diagnostic',
        '/p:Configuration=Release',
        '/p:Platform=AnyCPU',
        '/p:Deterministic=true',
        '/p:DebugType=pdbonly',
        "/p:DefineConstants=$Define",
        "/logger:D2aCscWitnessLogger,$loggerDll;$witness"
    )
    & $msbuild @buildArgs *> $diagnostic
    if ($LASTEXITCODE -ne 0) { throw 'D2A_REAL_NET48_COMPILATION_FAILED' }
    $dll = Join-Path $fixture 'bin/Release/D2a.Probe.dll'
    $pdb = Join-Path $fixture 'bin/Release/D2a.Probe.pdb'
    if (-not (Test-Path -LiteralPath $dll) -or
        -not (Test-Path -LiteralPath $pdb) -or
        -not (Test-Path -LiteralPath $witness)) {
        throw 'D2A_NATIVE_OUTPUT_OR_CSC_WITNESS_MISSING'
    }
    Copy-Item -LiteralPath $dll -Destination (Join-Path $variant 'D2a.Probe.dll')
    Copy-Item -LiteralPath $pdb -Destination (Join-Path $variant 'D2a.Probe.pdb')
    [IO.File]::WriteAllText((Join-Path $variant 'options.txt'), $Define, [Text.Encoding]::ASCII)
    if ((Get-FileHash -LiteralPath $tracked -Algorithm SHA256).Hash -cne $sourceSha) {
        throw 'D2A_TRACKED_SOURCE_CHANGED_BETWEEN_COMPILATIONS'
    }
    # Every following build starts with no prior project bin/obj state.
    Remove-Item -LiteralPath $bin -Recurse -Force -ErrorAction Stop
    Remove-Item -LiteralPath $obj -Recurse -Force -ErrorAction Stop
}

Build-RealVariant -Label 'a' -Define 'D2A_BASE'
Build-RealVariant -Label 'b' -Define 'D2A_ALT'

# Only actual positive/negative verification against real private compiler
# output pairs and loaded .NET Framework assembly identities.
& python $verifier --private-root $private --loader $loader --sanitized-output $sanitized
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $sanitized)) {
    throw 'D2A_REAL_NEGATIVE_RESEARCH_INCOMPLETE'
}

$report = Get-Content -LiteralPath $sanitized -Raw -Encoding utf8 | ConvertFrom-Json
if ($report.experiment -cne 'D2a' -or
    $report.verdict -cne 'RESEARCH_NEGATIVES_PASSED_REAL_FIXTURE_ONLY' -or
    $report.real_compiler_positives -ne 2 -or
    $report.actual_netfx_clr_load_positives -ne 1 -or
    $report.controls.Count -ne 5 -or
    @($report.controls | Where-Object { $_.status -cne 'PASS' }).Count -ne 0 -or
    $report.gate_c -cne 'UNSATISFIED' -or
    $report.gate_cn_release -cne 'NOT_AUTHORIZED' -or
    $report.production_source_link -cne 'HOLD') {
    throw 'D2A_SANITIZED_REPORT_DID_NOT_PROVE_PREREGISTERED_RESULTS'
}
Write-Host 'D2a FIVE original-PDB/compiler/CLR research negatives verified with two real builds.'
Write-Host 'D2a explicitly not a release gate: Gate C UNSATISFIED; Gate C-N release NOT_AUTHORIZED; Source Link HOLD'
