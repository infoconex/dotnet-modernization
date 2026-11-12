# Explore whether actual managed classic Windows PDB contains CodeView C13 checksum
# subsections. Never infer validity from printed raw chunk bytes or from stream text.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ApplicationRoot,
      [Parameter(Mandatory=$true)][string]$EvidenceRoot)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$app=(Resolve-Path -LiteralPath $ApplicationRoot).Path
$expected='8358780829458854a4b0356df5ac5e685f0a34c8'
if((& git -C $app rev-parse HEAD).Trim() -cne $expected){throw 'Wrong immutable source SHA'}
$evidence=[IO.Path]::GetFullPath($EvidenceRoot)
if(Test-Path -LiteralPath $evidence){throw 'Evidence directory already exists'}
New-Item -ItemType Directory -Path $evidence -Force|Out-Null
$llvm=Get-Command llvm-pdbutil.exe -ErrorAction Stop
$pdb=Join-Path $app 'src/RecordSift.Infrastructure.Csv/bin/Release/RecordSift.Infrastructure.Csv.pdb'
$dll=Join-Path $app 'src/RecordSift.Infrastructure.Csv/bin/Release/RecordSift.Infrastructure.Csv.dll'
if(-not (Test-Path -LiteralPath $pdb)){throw 'Native PDB was not built'}
& python tooling/validators/native_windows_pdb_sourcelink.py --pdb $pdb --dll $dll --output (Join-Path $evidence 'native-identity.json')
if($LASTEXITCODE -ne 0){throw 'PDB-DLL identity prerequisite failed'}
$files=@(& $llvm.Source dump -modules -files -l $pdb 2>&1)
$filesExit=$LASTEXITCODE
if($filesExit -ne 0){throw 'Cannot inventory native PDB module files'}
$chunks=@(& $llvm.Source bytes -chunks -split-chunks $pdb 2>&1)
$chunkExit=$LASTEXITCODE
$signatures=@($chunks|Where-Object {$_ -match '(?i)(FileChecksum|FileChksum|DEBUG_S_FILECHKSMS|0x000000f4|0xF4)'})
$noChecksum=@($files|Where-Object {$_ -match '\(no checksum\)'})
$out=[ordered]@{
  experiment='EXP-033';source_commit=$expected
  llvm_pdbutil_version=((& $llvm.Source --version 2>&1)|Select-Object -First 1)
  independent_file_listing_exit_code=$filesExit
  native_pdb_displayed_no_checksum_rows=$noChecksum.Count
  native_c13_byte_dump_exit_code=$chunkExit
  native_c13_byte_dump_line_count=@($chunks).Count
  c13_checksum_subsection_indicators=$signatures.Count
  c13_structural_inference=if($chunkExit -ne 0){'UNAVAILABLE'}elseif($signatures.Count -eq 0){'NO_CHECKSUM_SUBSECTION_TOKEN_IN_LLVM_OUTPUT'}else{'CHECKSUM_TOKEN_FOUND_NEEDS_BINARY_VALIDATION'}
  per_document_checksum_digest_validation='NOT_VERIFIED'
  source_input_byte_identity='NOT_VERIFIED'
  disclaimer='C13 CodeView chunks are distinct from managed DiaSymReader document records. Absence of an LLVM text marker is not proof all PDB managed checksums are missing.'
}
$out|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $evidence 'exp033-c13-evidence.json') -Encoding utf8
Write-Host "EXP-033 C13 dump exit=$chunkExit, checksum-token-lines=$($signatures.Count), file listing no-checksum rows=$($noChecksum.Count)"
if($chunkExit -ne 0){throw 'LLVM C13 byte view unsupported; record as inconclusive'}
if($noChecksum.Count -lt 1){throw 'Expected EXP-029 no-checksum independent control is absent; requires investigation'}
