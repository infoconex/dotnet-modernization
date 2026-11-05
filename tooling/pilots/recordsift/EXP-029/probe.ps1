# EXP-029: independent native Windows PDB checksum inventory, read-only.
# This phase intentionally does NOT assert source checksum correctness from a text match.
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$ApplicationRoot,
  [Parameter(Mandatory=$true)][string]$EvidenceRoot
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$app=(Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence=[IO.Path]::GetFullPath($EvidenceRoot)
$expected='8358780829458854a4b0356df5ac5e685f0a34c8'
if((git -C $app rev-parse HEAD).Trim() -cne $expected){ throw 'Not frozen RecordSift HEAD.' }
$gitDifferences=@(& git -C $app diff --name-only HEAD)
if($LASTEXITCODE -ne 0 -or $gitDifferences.Count -ne 0){ throw 'Tracked source modifications found or git diff failed.' }
if(Test-Path -LiteralPath $evidence){throw 'Evidence destination exists, refuse overwrite.'}
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$root=Join-Path $app 'src/RecordSift.Infrastructure.Csv/bin/Release'
$pdb=Join-Path $root 'RecordSift.Infrastructure.Csv.pdb'
$dll=Join-Path $root 'RecordSift.Infrastructure.Csv.dll'
$identity=Join-Path $evidence 'exp029-native-identity.json'
& python tooling/validators/native_windows_pdb_sourcelink.py --pdb $pdb --dll $dll --output $identity
if($LASTEXITCODE -ne 0){throw 'Source Link identity prerequisite failed.'}
$llvm=Get-Command llvm-pdbutil.exe -ErrorAction SilentlyContinue
if(-not $llvm){throw 'llvm-pdbutil is not preinstalled/available in PATH. No checksum claim.'}
$versionLines=@(& $llvm.Source --version 2>&1)
$versionLine=($versionLines|Select-Object -First 1)
# -files dumps the module source-file references; -l prints line data,
# but may not expose cryptographic checksums. Do not assert digests by guessing.
$dumpLines=@(& $llvm.Source dump -modules -files -l $pdb 2>&1)
$rc=$LASTEXITCODE
if($rc -ne 0){throw "llvm-pdbutil dump returned $rc; checksum inventory not established."}
$lines=@($dumpLines|ForEach-Object { [string]$_ })
$sourceName='CsvStreamImporterAdapter.cs'
$sourceHits=@($lines|Where-Object {$_ -match [regex]::Escape($sourceName)})
$algoTokens=@($lines|Where-Object {$_ -match '(?i)(?:SHA[-_ ]?(?:1|256)|MD5|checksum|hash)'})
# Redact any absolute paths and limit the diagnostic excerpt. Persist no actual host
# source paths, compiled content, PDB bytes or raw tool logs.
$preview=@($algoTokens|Select-Object -First 12|ForEach-Object {
  $redacted=[regex]::Replace($_, '(?i)[A-Z]:[\\/][^\s,;()\[\]]+', '<LOCAL_PATH>')
  $redacted=[regex]::Replace($redacted, '/(?:home|tmp|runner)/[^\s,;()\[\]]+', '<LOCAL_PATH>')
  if($redacted.Length -gt 200){$redacted.Substring(0,200)}else{$redacted}
})
$out=[ordered]@{
 experiment='EXP-029'
 frozen_commit=$expected
 native_identity='verified_by_existing_exp025_reader'
 independently_observed_tool='llvm-pdbutil'
 llvm_version_line=($versionLine -replace '([A-Z]:[\\/][^\s]+)','<LOCAL_PATH>')
 invocation='llvm-pdbutil dump -modules -files -l <native Windows PDB>'
 exit_code=$rc
 output_line_count=$lines.Count
 selected_source_file_present_in_dump=($sourceHits.Count -gt 0)
 selected_source_hit_count=$sourceHits.Count
 checksum_related_line_count=$algoTokens.Count
 sanitized_checksum_lines=$preview
 document_record_digest_status='NOT_VERIFIED_UNTIL_CHECKSUM_FORMAT_AND_HASH_INPUT_CONFIRMED'
 warnings=@(
  'This inventory does not match all native PDB checksum records to immutable Git bytes.',
  'Do not classify SHA checksum verified without algorithm, record length and raw document inputs.',
  'No Source Link debugger stepping, NuGet project installation or module-load isolation tested.'
 )
}
$out|ConvertTo-Json -Depth 10|Set-Content (Join-Path $evidence 'exp029-document-inventory.json') -Encoding utf8
Write-Host ("EXP-029 inventory: file_found=$($out.selected_source_file_present_in_dump); checksum_tokens=$($out.checksum_related_line_count); lines=$($lines.Count)")
if(-not $out.selected_source_file_present_in_dump){throw 'Independent PDB reader did not list selected compiled source file.'}
