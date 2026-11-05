# EXP-036: compare the actual frozen CSV PDB's selected document hashes.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ApplicationRoot,
      [Parameter(Mandatory=$true)][string]$Experiment24Evidence,
      [Parameter(Mandatory=$true)][string]$OutputPath)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$global:LASTEXITCODE=0
$app=(Resolve-Path $ApplicationRoot).Path
$bin=Join-Path $env:RUNNER_TEMP 'exp036-fixture/bin'
$csv=Join-Path $app 'src/RecordSift.Infrastructure.Csv'
$dll=Join-Path $csv 'bin/Release/RecordSift.Infrastructure.Csv.dll'
$pdb=Join-Path $csv 'bin/Release/RecordSift.Infrastructure.Csv.pdb'
$frozen='8358780829458854a4b0356df5ac5e685f0a34c8'
if((git -C $app rev-parse HEAD).Trim() -cne $frozen){throw 'Unexpected RecordSift source commit'}
$gate=Get-Content -LiteralPath (Join-Path $Experiment24Evidence 'experiment-report.json') -Raw | ConvertFrom-Json
if($gate.application_release_gates -cne 'candidate_425_api_419_nunit_5_xml_local_package_clean_consumer_passed' -or
   $gate.logical_compatibility -cne 'five_categories_matched_original'){throw 'Frozen candidate compatibility not proved'}
python (Join-Path $PSScriptRoot 'verify_identity.py') --dll $dll --pdb $pdb
if($LASTEXITCODE -ne 0){throw 'PE/PDB structural identity mismatch'}

function Run-Reader([string]$exe){
    $rule='EXP036-CSV-OUTBOUND-'+[guid]::NewGuid().ToString('N')
    New-NetFirewallRule -DisplayName $rule -Direction Outbound -Action Block -Profile Any -Program $exe -ErrorAction Stop | Out-Null
    try{
        $start=New-Object Diagnostics.ProcessStartInfo
        $start.FileName=$exe
        $start.Arguments=('"'+$dll+'" "'+$pdb+'"')
        $start.UseShellExecute=$false
        $start.RedirectStandardOutput=$true
        $start.RedirectStandardError=$true
        $start.CreateNoWindow=$true
        $p=[Diagnostics.Process]::Start($start)
        try {
            $deadline=[DateTime]::UtcNow.AddSeconds(20)
            while(-not $p.HasExited -and [DateTime]::UtcNow -lt $deadline){
                $p.Refresh()
                if($p.WorkingSet64 -gt 256MB){throw 'Reader memory cap exceeded'}
                Start-Sleep -Milliseconds 100
            }
            if(-not $p.HasExited){throw 'Reader timeout'}
            $stdout=$p.StandardOutput.ReadToEnd()
            $stderr=$p.StandardError.ReadToEnd()
            if($p.ExitCode -ne 0){throw "Reader failed: exit $($p.ExitCode); category $stderr"}
            return $stdout
        } finally {
            if(-not $p.HasExited){$p.Kill();$p.WaitForExit(3000)|Out-Null}
            $p.Dispose()
        }
    } finally {Remove-NetFirewallRule -DisplayName $rule -ErrorAction Stop}
}

$selected=@('CharacterLimitedTextReader.cs','CsvRecordReaderAdapter.cs',
  'CsvStreamImporterAdapter.cs','MalformedCsvException.cs')
$algorithms=@{'ff1816ec-aa5e-4d10-87f7-6f4963833460'='SHA1';
 '8829d00f-11b8-4213-878b-770e8597ac16'='SHA256'}
$observations=@{}
foreach($reader in @('DNLIB','CECIL')){
    $out=Run-Reader (Join-Path $bin "ReaderProbe-$reader.exe")
    $records=@{}
    foreach($line in ($out -split '\r?\n')){
        if(-not $line.StartsWith('DOC'+[char]9)){continue}
        $fields=$line.Split([char]9)
        if($fields.Count -ne 4){throw 'Invalid document row'}
        $name=$fields[1]
        if($records.ContainsKey($name)){throw 'Duplicate reader document name'}
        if(-not $algorithms.ContainsKey($fields[2])){throw 'Unsupported checksum algorithm GUID'}
        $records[$name]=@{alg=$algorithms[$fields[2]];sha=$fields[3]}
    }
    foreach($name in $selected){
        if(-not $records.ContainsKey($name)){throw "Missing selected document: $name/$reader"}
        $source=Join-Path $csv $name
        $actual=(Get-FileHash -LiteralPath $source -Algorithm $records[$name].alg).Hash.ToLowerInvariant()
        if($actual -cne $records[$name].sha){throw "Physical source checksum mismatch: $name/$reader"}
    }
    $observations[$reader]=$records
    Write-Host "VERIFIED: $reader managed selected CSV checksum bytes $($selected.Count)/$($selected.Count); total docs $($records.Count)"
}
foreach($name in $selected){
    if($observations.DNLIB[$name].alg -cne $observations.CECIL[$name].alg -or
       $observations.DNLIB[$name].sha -cne $observations.CECIL[$name].sha){
       throw "Independent reader disagreement: $name"
    }
}
$namesA=@($observations.DNLIB.Keys | Sort-Object)
$namesB=@($observations.CECIL.Keys | Sort-Object)
if(($namesA -join '|') -cne ($namesB -join '|')){throw 'Reader document sets differ'}
$unclassified=@($namesA | Where-Object {$_ -cnotin $selected})
$report=[ordered]@{
  experiment='EXP-036'; result='VERIFIED_SELECTED_OWNED_CSV_CHECKSUMS'
  frozen_sha=$frozen; native_pdb_pe_identity='matched'
  selected_documents=$selected; selected_match_count=$selected.Count
  dnlib_total_document_count=$namesA.Count; cecil_total_document_count=$namesB.Count
  unclassified_count=$unclassified.Count; unclassified_names=$unclassified
  actual_release_gates='425 API / 419 NUnit (418 pass, 1 skipped) / 5 XML / local package / clean consumer / five compatibility categories'
  limitation='Selected four owned CSV sources only; any additional generated/external PDB documents must be audited separately'
  security='Pinned research DLLs, trusted frozen source, outbound process firewall, 20s and 256MiB monitored'
  source_link_approval='HOLD; VS install and real debugger source stepping NOT TESTED'
}
if(@(git -C $app diff --name-only HEAD --).Count -ne 0){throw 'Tracked RecordSift files changed'}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $OutputPath -Encoding utf8
Write-Host "EXP036 REAL FROZEN CSV $($selected.Count)/$($selected.Count) CHECKSUMS VERIFIED"
$global:LASTEXITCODE=0
