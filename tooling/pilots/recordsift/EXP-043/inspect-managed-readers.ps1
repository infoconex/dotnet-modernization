# EXP-043: two independently pinned fully managed readers on trusted
# five local candidate PDBs. NO fixture repeat, native COM, network access
# during reader execution or source/PDB log upload.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ApplicationRoot,
      [Parameter(Mandatory=$true)][string]$EvidenceRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$global:LASTEXITCODE=0
$app=(Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence=[IO.Path]::GetFullPath($EvidenceRoot)
$research=(Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$frozen='8358780829458854a4b0356df5ac5e685f0a34c8'
if ((& git -C $app rev-parse HEAD).Trim() -cne $frozen -or $LASTEXITCODE -ne 0) {
  throw 'EXP043 managed reader frozen revision mismatch'
}
if (Test-Path -LiteralPath $evidence) {throw 'EXP043 managed reader evidence must be new'}
New-Item -ItemType Directory -Path $evidence | Out-Null
$archiveSpecs=@(
  @{Name='dnlib.4.5.0.nupkg';Id='dnlib';Version='4.5.0';Hash='63bc2f9579568204cc8b30fa9f6700a231bcf868a8032e09118887af3eafee58'},
  @{Name='mono.cecil.0.11.6.nupkg';Id='mono.cecil';Version='0.11.6';Hash='d2a23832aaa948ba9a01acc42b5726e34c5f995958f1b30d45c0e7c70b3a72d5'}
)
# Verify pinned archive SHA256 against previous EXP-036/040 independent
# preflight. Never use floating versions or unsafe native symbol readers.
foreach ($item in $archiveSpecs) {
  $archive=Join-Path $evidence $item.Name
  $lower=$item.Id
  $url="https://api.nuget.org/v3-flatcontainer/$lower/$($item.Version)/$lower.$($item.Version).nupkg"
  curl.exe --fail --location --retry 3 --silent --show-error --proto '=https' --proto-redir '=https' --max-filesize 31457280 $url --output $archive
  if ($LASTEXITCODE -ne 0 -or (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -cne $item.Hash) {
    throw 'EXP043 pinned managed reader archive authentication failed'
  }
}
$extractions=@(
  @{Archive='dnlib.4.5.0.nupkg';Entry='lib/net45/dnlib.dll';Out='dnlib.dll';Hash='97ef5328d1d1703924c48d9cd1d45b7227fe3836e116dcded623b6a0dbd52c23'},
  @{Archive='mono.cecil.0.11.6.nupkg';Entry='lib/net40/Mono.Cecil.dll';Out='Mono.Cecil.dll';Hash='c41bdb9ffd3c5f6e17d2382c1012d73703e035e3f1100245fdd4e08c8dc6eb5b'},
  @{Archive='mono.cecil.0.11.6.nupkg';Entry='lib/net40/Mono.Cecil.Pdb.dll';Out='Mono.Cecil.Pdb.dll';Hash='50a1a1a79dc86fcfb8b51249b5325a10dd93d193c52999cf6775d25030a4e606'}
)
Add-Type -AssemblyName System.IO.Compression
$bin=Join-Path $evidence 'bin'
New-Item -ItemType Directory -Path $bin | Out-Null
foreach ($item in $extractions) {
  $zip=[IO.Compression.ZipFile]::OpenRead((Join-Path $evidence $item.Archive))
  try {
    $entries=@($zip.Entries | Where-Object { $_.FullName -ceq $item.Entry })
    if ($entries.Count -ne 1 -or $entries[0].Length -gt 2MB) {throw 'EXP043 pinned reader entry missing or oversized'}
    $input=$entries[0].Open()
    $output=Join-Path $bin $item.Out
    $dest=[IO.File]::Create($output)
    try {$input.CopyTo($dest)} finally {$dest.Dispose();$input.Dispose()}
    if ((Get-FileHash -LiteralPath $output -Algorithm SHA256).Hash.ToLowerInvariant() -cne $item.Hash) {
      throw 'EXP043 pinned reader DLL authentication failed'
    }
  } finally {$zip.Dispose()}
}
$pf=[Environment]::GetFolderPath('ProgramFilesX86')
$vswhere=Join-Path $pf 'Microsoft Visual Studio\Installer\vswhere.exe'
$vsroot=(& $vswhere -latest -products '*' -property installationPath | Select-Object -First 1)
if (-not $vsroot) {throw 'EXP043 supported VS Csc host unavailable'}
$csc=Join-Path $vsroot 'MSBuild\Current\Bin\Roslyn\csc.exe'
$refs=Join-Path $pf 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8'
if (-not (Test-Path -LiteralPath $csc) -or -not (Test-Path -LiteralPath (Join-Path $refs 'mscorlib.dll'))) {
  throw 'EXP043 net48 managed reader compiler reference files unavailable'
}
$source=Join-Path $research 'tooling/pilots/recordsift/EXP-036/ReaderProbe.cs'
foreach ($reader in @('DNLIB','CECIL')) {
  $exe=Join-Path $bin ("ReaderProbe-$reader.exe")
  $references=@("/reference:$(Join-Path $refs 'mscorlib.dll')",
    "/reference:$(Join-Path $refs 'System.dll')",
    "/reference:$(Join-Path $refs 'System.Core.dll')")
  if ($reader -ceq 'DNLIB') {
    $references+=("/reference:$(Join-Path $bin 'dnlib.dll')")
  } else {
    $references+=("/reference:$(Join-Path $bin 'Mono.Cecil.dll')",
      "/reference:$(Join-Path $bin 'Mono.Cecil.Pdb.dll')")
  }
  & $csc /nologo /noconfig /langversion:7.3 /target:exe /debug- /optimize+ "/define:$reader" "/out:$exe" @references $source *> (Join-Path $evidence ("compile-$reader-private.log"))
  if ($LASTEXITCODE -ne 0) {throw 'EXP043 isolated managed reader compilation failed'}
}
function RunBounded([string]$program,[string]$dll,[string]$pdb,[string]$privateUrls,[string]$stdoutPath) {
  # One true Windows firewall rule per executable invocation, removed in finally.
  $rule='EXP043-MANAGED-ONLY-'+[guid]::NewGuid().ToString('N')
  $protected=$false
  $proc=$null
  try {
    New-NetFirewallRule -DisplayName $rule -Direction Outbound -Action Block -Program $program -Profile Any -ErrorAction Stop | Out-Null
    $protected=$true
    $start=New-Object System.Diagnostics.ProcessStartInfo
    $start.FileName=$program
    $start.Arguments=('"'+$dll+'" "'+$pdb+'" "'+$privateUrls+'"')
    $start.UseShellExecute=$false
    $start.RedirectStandardOutput=$true
    $start.RedirectStandardError=$true
    $start.CreateNoWindow=$true
    $proc=[Diagnostics.Process]::Start($start)
    $deadline=[DateTime]::UtcNow.AddSeconds(20)
    while (-not $proc.HasExited -and [DateTime]::UtcNow -lt $deadline) {
      $proc.Refresh()
      if ($proc.WorkingSet64 -gt 256MB) {throw 'EXP043 managed reader memory bound exceeded'}
      Start-Sleep -Milliseconds 100
    }
    if (-not $proc.HasExited) {throw 'EXP043 managed reader execution timeout'}
    $out=$proc.StandardOutput.ReadToEnd()
    $err=$proc.StandardError.ReadToEnd()
    if ($proc.ExitCode -ne 0) {throw 'EXP043 managed reader returned nonzero; private error suppressed'}
    if ($out.Length -gt 128KB) {throw 'EXP043 managed reader output oversized'}
    [IO.File]::WriteAllText($stdoutPath,$out,[Text.UTF8Encoding]::new($false))
  } finally {
    if ($null -ne $proc) {
      if (-not $proc.HasExited) {$proc.Kill();$proc.WaitForExit(3000)|Out-Null}
      $proc.Dispose()
    }
    if ($protected) {Remove-NetFirewallRule -DisplayName $rule -ErrorAction Stop}
  }
}
$components=@('Domain','Application','Infrastructure.Csv','Infrastructure.Reporting','Infrastructure.Xlsx')
foreach ($component in $components) {
  $name='RecordSift.'+$component
  $dll=Join-Path $app ("src/$name/bin/Release/$name.dll")
  $pdb=Join-Path $app ("src/$name/bin/Release/$name.pdb")
  foreach ($reader in @('DNLIB','CECIL')) {
    $prefix=Join-Path $evidence ($component+'-'+$reader)
    RunBounded (Join-Path $bin ("ReaderProbe-$reader.exe")) $dll $pdb ($prefix+'-urls.private') ($prefix+'-stdout.private')
  }
  Write-Host "EXP043 managed reader pair executed for $component without native COM (private document output withheld)"
}
