param(
    [Parameter(Mandatory=$true)][string]$ApplicationRoot,
    [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $EvidenceRoot | Out-Null
$vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
if (-not (Test-Path $vswhere)) { throw 'Visual Studio installer locator absent' }
$installation = (& $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath | Select-Object -First 1)
if ($LASTEXITCODE -ne 0 -or -not $installation) { throw 'Required VS C++ tooling unavailable' }
$diaRoot = Join-Path $installation 'DIA SDK'
$diaDll = Join-Path $diaRoot 'bin/amd64/msdia140.dll'
$include = Join-Path $diaRoot 'include'
$lib = Join-Path $diaRoot 'lib/amd64'
$vsDevCmd = Join-Path $installation 'Common7/Tools/VsDevCmd.bat'
foreach ($item in @($diaDll, (Join-Path $include 'dia2.h'),(Join-Path $lib 'diaguids.lib'),$vsDevCmd)) {
    if(-not (Test-Path $item)) { throw 'Required installed DIA SDK component missing' }
}
$signature = Get-AuthenticodeSignature -FilePath $diaDll
if($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Microsoft'){
    throw 'DIA DLL signature cannot be verified as Microsoft-signed'
}
$src = Join-Path $PSScriptRoot 'dia_source_files.cpp'
$exe = Join-Path $EvidenceRoot 'dia_source_files.exe'
$buildCmd = Join-Path $EvidenceRoot 'compile.cmd'
$cmdText = @(
    'call "' + $vsDevCmd + '" -no_logo -arch=x64 -host_arch=x64',
    'cl.exe /nologo /EHsc /std:c++17 /W4 /I"' + $include + '" "' + $src + '" /link /LIBPATH:"' + $lib + '" /OUT:"' + $exe + '"'
) -join "`r`n"
[System.IO.File]::WriteAllText($buildCmd,$cmdText + "`r`n",[System.Text.Encoding]::ASCII)
& cmd.exe /d /c $buildCmd
if ($LASTEXITCODE -ne 0 -or -not (Test-Path $exe)) { throw 'Independent DIA reader compilation failed' }
$pdb = Join-Path $ApplicationRoot 'src/RecordSift.Infrastructure.Csv/bin/Release/RecordSift.Infrastructure.Csv.pdb'
if (-not (Test-Path $pdb)) { throw 'Frozen application PDB absent' }
$diaRaw = Join-Path $EvidenceRoot 'dia-raw.txt'
& $exe $diaDll $pdb | Set-Content -Encoding utf8 -Path $diaRaw
if($LASTEXITCODE -ne 0) { throw 'DIA SDK could not enumerate native PDB source-file table' }
python (Join-Path $PSScriptRoot '../../../validators/dia_source_checksum_assessment.py') --dia-output $diaRaw --source-root $ApplicationRoot --output (Join-Path $EvidenceRoot 'dia-checksum-assessment.json')
if($LASTEXITCODE -ne 0){throw 'Actual DIA source checksum consistency failure'}
$meta = [ordered]@{
    dia_file_version = (Get-Item $diaDll).VersionInfo.FileVersion
    dia_signed_by_microsoft = $true
    dia_file_sha256 = (Get-FileHash $diaDll -Algorithm SHA256).Hash.ToLowerInvariant()
    source_commit = '8358780829458854a4b0356df5ac5e685f0a34c8'
    separate_managed_document_reader_executed = $false
}
$meta | ConvertTo-Json | Set-Content -Encoding utf8 (Join-Path $EvidenceRoot 'dia-tool-provenance.json')
Write-Host 'DIA inventory only; managed ISymUnmanagedDocument checksum gate remains separately open.'
