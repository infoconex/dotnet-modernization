# EXP-044: real independent non-RecordSift net48 trusted classic-PDB pilot.
# Runs only inside an ephemeral Windows Actions runner. No RecordSift checkout.
# Private compiler task events, sources, logs, package archives and PDBs stay
# outside uploaded artifacts and are unconditionally destroyed by the workflow.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ExpectedCommit)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$root=(Resolve-Path -LiteralPath $env:GITHUB_WORKSPACE).Path
$private=Join-Path $env:RUNNER_TEMP 'exp044-private'
$project=Join-Path $root 'tooling/fixtures/gate-cn/AnotherLibrary.Core/AnotherLibrary.Core.csproj'
$evidence=Join-Path $private 'capture/independent-core'
$packages=Join-Path $private 'packages'
$manifest=Join-Path $private 'manifest.json'
$sanitized=Join-Path $env:RUNNER_TEMP 'exp044-sanitized.json'
if (-not [regex]::IsMatch($ExpectedCommit,'^[0-9a-f]{40}$') -or
    (& git -C $root rev-parse HEAD).Trim() -cne $ExpectedCommit -or $LASTEXITCODE -ne 0) {
    throw 'EXP044 wrong immutable research commit'
}
if (Test-Path -LiteralPath $private) { throw 'EXP044 private root must start absent' }
if (Test-Path -LiteralPath $sanitized) { throw 'EXP044 sanitized report must start absent' }
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
New-Item -ItemType Directory -Path $packages -Force | Out-Null

$vswhere=Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild=(& $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1)
if (-not $msbuild) { throw 'EXP044 installed Visual Studio MSBuild missing' }
$compiler=Join-Path (Split-Path -Parent $msbuild) 'Roslyn/csc.exe'
$framework=Join-Path (Split-Path -Parent $msbuild) 'Microsoft.Build.Framework.dll'
if (-not (Test-Path -LiteralPath $compiler) -or -not (Test-Path -LiteralPath $framework)) {
    throw 'EXP044 installed compiler or MSBuild Framework missing'
}

# Pins individually audited by EXP-024; no fallback, implicit NuGet graph,
# version selection, or production dependency installation is permitted.
$archives=@(
  @{id='Microsoft.SourceLink.GitHub';sha='9c3252f8cbe1547bf8c12b7c65a7bc28985bab2d598ff97c13e0104c22d80cd5'},
  @{id='Microsoft.SourceLink.Common';sha='e99d7aea402042d04faa4971709718ebf256406b4c59f700cb1c8a739859c6a2'},
  @{id='Microsoft.Build.Tasks.Git';sha='9d21a711e9fce96b34e8c02f10069bc66a381d84a2912e65a14dc9c411135e29'}
)
Add-Type -AssemblyName System.IO.Compression.FileSystem
foreach ($pin in $archives) {
    $lower=$pin.id.ToLowerInvariant()
    $version='10.0.403'
    $archive=Join-Path $private ($lower+'.'+$version+'.nupkg')
    $url="https://api.nuget.org/v3-flatcontainer/$lower/$version/$lower.$version.nupkg"
    Invoke-WebRequest -Uri $url -OutFile $archive -TimeoutSec 60 -ErrorAction Stop
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -cne $pin.sha) {
        throw 'EXP044 pinned official Source Link archive hash mismatch'
    }
    $dest=Join-Path $packages ($pin.id+'.'+$version)
    if (Test-Path -LiteralPath $dest) { throw 'EXP044 package extraction destination exists' }
    [IO.Compression.ZipFile]::ExtractToDirectory($archive,$dest)
    foreach ($extension in @('props','targets')) {
        $asset=Join-Path $dest ('build/'+$pin.id+'.'+$extension)
        if (-not (Test-Path -LiteralPath $asset)) {
            throw 'EXP044 exact pinned Source Link import missing'
        }
    }
}
Write-Host 'EXP044 three independently pinned Source Link archives authenticated; no package publication'

$loggerSource=Join-Path $root 'tooling/pilots/recordsift/EXP-042/CscParameterLogger.cs'
$loggerDll=Join-Path $private 'EXP042.CscParameterLogger.dll'
& $compiler /nologo /target:library /langversion:7.3 "/reference:$framework" '/reference:System.Core.dll' "/out:$loggerDll" $loggerSource *> (Join-Path $private 'logger-build-private.log')
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $loggerDll)) {
    throw 'EXP044 private structured task-event logger compilation failed'
}
$base=@($project,'/p:Configuration=Release','/p:Platform=AnyCPU',
        '/p:Deterministic=true','/p:ContinuousIntegrationBuild=true',
        "/p:GateCNResearchRoot=$root","/p:GateCNPackageRoot=$packages",'-nologo')
$preprocessed=Join-Path $evidence 'msbuild-preprocessed.xml'
& $msbuild @base "/pp:$preprocessed" *> (Join-Path $evidence 'preprocess-private.log')
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $preprocessed)) {
    throw 'EXP044 original Csc declaration not available'
}
$capture=Join-Path $evidence 'source-inputs-private'
$events=Join-Path $evidence 'exp042-csc-parameters-private.tsv'
$log=Join-Path $evidence 'msbuild-diagnostic-private.log'
& $msbuild @base "/p:SourceInputCaptureRoot=$capture" "/logger:RecordSiftResearchCscParameterLogger,$loggerDll;$events" '/t:Rebuild' '/verbosity:diagnostic' *> $log
if ($LASTEXITCODE -ne 0) { throw 'EXP044 disposable net48 compiler build failed' }
if (-not (Test-Path -LiteralPath (Join-Path $capture 'input-manifest.tsv')) -or
    -not (Test-Path -LiteralPath ($capture+'-producer/producer-after.tsv')) -or
    -not (Test-Path -LiteralPath $events)) {
    throw 'EXP044 original compiler/Csc/generated provenance records missing'
}
Write-Host 'EXP044 standalone traditional net48 compiler and actual producer executed; private logs withheld'

$external=@{
  schema='gate-cn-live-manifest-v1'
  authorization='DESIGN_VALIDATION_ONLY'
  application_repository='infoconex/dotnet-modernization'
  application_commit=$ExpectedCommit
  components=@(@{
      component='AnotherLibrary.Core'
      project_dir='tooling/fixtures/gate-cn/AnotherLibrary.Core'
      assembly_name='AnotherLibrary.Core'
      evidence_dir='capture/independent-core'
      capture_dir='source-inputs-private'
      expected_native_documents=2
      expected_tracked_inputs=1
      expected_generated_inputs=1
      producer_contract='EXP042_MONIKER_ONE_PER_COMPONENT'
  })
}
$external | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $manifest -Encoding utf8
python (Join-Path $root 'tooling/validators/gate_cn_live_provenance.py') --manifest $manifest --app-root $root --evidence-root $private --output $sanitized
if ($LASTEXITCODE -ne 0) { throw 'EXP044 original physical bytes or native PDB identity not authenticated' }
$result=Get-Content -LiteralPath $sanitized -Raw -Encoding utf8 | ConvertFrom-Json
if ($result.application_repository -cne 'infoconex/dotnet-modernization' -or
    $result.application_commit -cne $ExpectedCommit -or
    $result.results[0].native_pe_pdb_identity_matched -ne $true -or
    $result.verdict -cne 'SCOPED_LIVE_PROVENANCE_RESEARCH_VERIFIED' -or
    $result.required_components -ne 1 -or
    $result.results[0].status -cne 'RESEARCH_VERIFIED' -or
    $result.results[0].original_bytes_verified -ne 2 -or
    $result.results[0].generated_inputs_verified -ne 1 -or
    $result.gate_cn_release_acceptance -cne 'NOT_AUTHORIZED' -or
    $result.legacy_gate_c -cne 'UNSATISFIED' -or
    $result.source_link_adoption -cne 'HOLD') {
    throw 'EXP044 reported observed live provenance or governance incomplete'
}
Write-Host 'EXP044 real non-RecordSift PE/PDB, Csc and original bytes 2/2 research verified; NO release gate or IDE acceptance'
