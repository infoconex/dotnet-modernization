# EXP-043 disposable-only extension of the already verified EXP-024 candidate.
# Starts ONLY after EXP-024 baseline + CSV complete. Frozen source checkout
# temporarily modified per project with restored original project bytes in finally.
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$ApplicationRoot,
  [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$frozen='8358780829458854a4b0356df5ac5e685f0a34c8'
$app=(Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence=[IO.Path]::GetFullPath($EvidenceRoot)
$research=(Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
if ($evidence.StartsWith($app + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
  throw 'EXP043 private evidence must be outside disposable checkout'
}
if ((& git -C $app rev-parse HEAD).Trim() -cne $frozen -or $LASTEXITCODE -ne 0) {
  throw 'EXP043 wrong frozen commit'
}
# EXP-024 legitimately creates ignored packages, binaries and temporary files.
# Only tracked frozen source mutations or staged changes violate the boundary.
$trackedDiff=@(& git -C $app diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0 -or $trackedDiff.Count -ne 0) {
  throw 'EXP043 tracked frozen source must be unchanged after EXP024'
}
$parent=Join-Path $evidence 'exp024'
if (-not (Test-Path -LiteralPath (Join-Path $parent 'candidate-versus-original-compatibility.json'))) {
  throw 'EXP043 independently verified EXP024 baseline/candidate prerequisite missing'
}
if (Test-Path -LiteralPath (Join-Path $evidence 'remaining')) { throw 'EXP043 remaining evidence already exists' }
$root=Join-Path $evidence 'remaining'
New-Item -ItemType Directory -Path $root | Out-Null
$vswhere=Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild=(& $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1)
if (-not $msbuild) { throw 'EXP043 MSBuild host not available' }
$loggerDll=Join-Path $parent 'EXP042.CscParameterLogger.dll'
if (-not (Test-Path -LiteralPath $loggerDll)) { throw 'EXP043 requires prior verified EXP042 private structured logger binary' }
$packages=@('Microsoft.SourceLink.GitHub','Microsoft.SourceLink.Common','Microsoft.Build.Tasks.Git')
foreach ($package in $packages) {
  if (-not (Test-Path -LiteralPath (Join-Path $app ("packages/$package.10.0.403/build/$package.targets")))) {
    throw 'EXP043 inherited official pinned provider targets unavailable'
  }
}
$components=[ordered]@{
  Domain='domain'
  Application='application'
  'Infrastructure.Reporting'='reporting'
  'Infrastructure.Xlsx'='xlsx'
}
$sourceCapture=Join-Path $research 'tooling/pilots/recordsift/EXP-041/CompilerInputSnapshot.targets'
$producerCapture=Join-Path $research 'tooling/pilots/recordsift/EXP-042/MonikerProducerProbe.targets'
$nativePdbs=@()
foreach ($component in $components.Keys) {
  $slug=$components[$component]
  $name="RecordSift.$component"
  $project=Join-Path $app ("src/$name/$name.csproj")
  $original=[IO.File]::ReadAllBytes($project)
  $private=Join-Path $root $slug
  New-Item -ItemType Directory -Path $private | Out-Null
  try {
    $text=[Text.Encoding]::UTF8.GetString($original)
    $anchor='  <Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" />'
    if (-not $text.Contains($anchor)) { throw 'EXP043 unsupported frozen project layout' }
    $props=@();$targets=@()
    foreach ($package in $packages) {
      $relative="..\..\packages\$package.10.0.403\build\$package"
      $props+=('  <Import Project="' + $relative + '.props" />')
      $targets+=('  <Import Project="' + $relative + '.targets" />')
    }
    $text=$text.Replace($anchor,($props -join "`r`n") + "`r`n" + $anchor + "`r`n" + ($targets -join "`r`n"))
    foreach ($target in @($sourceCapture,$producerCapture)) {
      $escaped=[Security.SecurityElement]::Escape($target)
      $pos=$text.LastIndexOf('</Project>',[StringComparison]::Ordinal)
      if ($pos -lt 0) {throw 'EXP043 malformed disposable project'}
      $text=$text.Substring(0,$pos) + ('  <Import Project="' + $escaped + '" />') +
        [Environment]::NewLine + $text.Substring($pos)
    }
    [IO.File]::WriteAllText($project,$text,[Text.UTF8Encoding]::new($false))
    $baseArgs=@($project,'/p:Configuration=Release','/p:Platform=AnyCPU',
      '/p:Deterministic=true','/p:ContinuousIntegrationBuild=true',
      '/p:BuildProjectReferences=false','-nologo')
    $pp=Join-Path $private 'msbuild-preprocessed.xml'
    & $msbuild @baseArgs "/pp:$pp" *> (Join-Path $private 'preprocess-private.log')
    if ($LASTEXITCODE -ne 0) {throw 'EXP043 private preprocessing failed'}
    $capture=Join-Path $private 'source-inputs-private'
    $structured=Join-Path $private 'exp042-csc-parameters-private.tsv'
    $log=Join-Path $private 'msbuild-diagnostic-private.log'
    $compileArgs=@($baseArgs,("/p:SourceInputCaptureRoot=$capture"),
      ("/logger:RecordSiftResearchCscParameterLogger,$loggerDll;$structured"),
      '/t:Rebuild','/verbosity:diagnostic')
    & $msbuild @compileArgs *> $log
    if ($LASTEXITCODE -ne 0) { throw 'EXP043 isolated candidate compile failed; raw logs withheld' }
    if (-not (Test-Path -LiteralPath (Join-Path $capture 'input-manifest.tsv')) -or
        -not (Test-Path -LiteralPath (Join-Path ($capture+'-producer') 'producer-after.tsv')) -or
        -not (Test-Path -LiteralPath $structured)) {
      throw 'EXP043 independent source/producer/event evidence missing'
    }
    $pdb=Join-Path $app ("src/$name/bin/Release/$name.pdb")
    $dll=Join-Path $app ("src/$name/bin/Release/$name.dll")
    if (-not (Test-Path -LiteralPath $pdb) -or -not (Test-Path -LiteralPath $dll)) {
      throw 'EXP043 production assembly or PDB absent'
    }
    $header=[Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($pdb),0,32)
    if (-not $header.StartsWith('Microsoft C/C++ MSF 7.00',[StringComparison]::Ordinal)) {
      throw 'EXP043 unexpected nonclassic production PDB'
    }
    $nativePdbs+=$component
    Write-Host "EXP043 isolated $component native PDB candidate built (private bytes/log withheld)"
  } finally {
    [IO.File]::WriteAllBytes($project,$original)
  }
}
if ($nativePdbs.Count -ne 4) {throw 'EXP043 all four candidate PDBs required'}
$changed=@(& git -C $app diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0 -or $changed.Count -ne 0) {
  throw 'EXP043 tracked frozen project files did not restore byte-identically'
}
# The existing five test runners use already-compiled copy-local production
# DLLs. Replace only their candidate production DLL copies; otherwise tests
# would exercise baseline binaries and produce false-positive compatibility.
$names=@('Domain','Application','Infrastructure.Csv','Infrastructure.Reporting','Infrastructure.Xlsx')
foreach ($component in $names) {
  $name="RecordSift.$component"
  $dll=Join-Path $app ("src/$name/bin/Release/$name.dll")
  foreach ($suite in $names) {
    $testDir=Join-Path $app ("tests/RecordSift.$suite.Tests/bin/Release")
    $local=Join-Path $testDir ($name+'.dll')
    if (Test-Path -LiteralPath $local) {
      Copy-Item -LiteralPath $dll -Destination $local -Force
      if ((Get-FileHash -LiteralPath $local -Algorithm SHA256).Hash -cne
          (Get-FileHash -LiteralPath $dll -Algorithm SHA256).Hash) {
        throw 'EXP043 test copy-local candidate mismatch'
      }
    }
  }
}
$both=Join-Path $evidence 'all-five-candidate-acceptance'
& (Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1') -ApplicationRoot $app -EvidenceRoot $both -ExpectedCommit $frozen -ExperimentId 'EXP-043-candidate' | Out-Host
if ($LASTEXITCODE -ne 0) { throw 'EXP043 five-assembly release acceptance failed' }
$comparison=Join-Path $evidence 'all-five-versus-original-compatibility.json'
& python (Join-Path $research 'tooling/validators/compatibility.py') compare --baseline (Join-Path $parent 'baseline-acceptance/baseline.json') --candidate (Join-Path $both 'baseline.json') --output $comparison
if ($LASTEXITCODE -ne 0) { throw 'EXP043 compatibility regression' }
$compare=Get-Content -LiteralPath $comparison -Raw | ConvertFrom-Json
if ($compare.overall -cne 'matched') { throw 'EXP043 full frozen contract comparison diverged' }
Write-Host 'EXP043 all-five candidate full 425 API / 419 NUnit / five XML / unpublished package / clean net48 consumer contracts matched original'
