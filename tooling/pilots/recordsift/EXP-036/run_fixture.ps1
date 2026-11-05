# EXP-036 isolated classic Windows-PDB fixture. No application checkout/build.
# This run is restricted to compiler-produced, trusted local inputs; never fuzz a parser.
param([Parameter(Mandatory=$true)][string]$ArchiveRoot, [switch]$Experiment37Variants)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$global:LASTEXITCODE=0 # strict-mode compatible initial state before the first native subprocess
$root=(Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$temp=Join-Path $env:RUNNER_TEMP 'exp036-fixture'
New-Item -Path $temp -ItemType Directory -Force | Out-Null
$pkgInfo=@(
    @{ Id='dnlib'; Archive='dnlib.4.5.0.nupkg'; Hash='63bc2f9579568204cc8b30fa9f6700a231bcf868a8032e09118887af3eafee58' },
    @{ Id='Mono.Cecil'; Archive='mono.cecil.0.11.6.nupkg'; Hash='d2a23832aaa948ba9a01acc42b5726e34c5f995958f1b30d45c0e7c70b3a72d5' }
)
foreach($p in $pkgInfo){
    $archive=Join-Path $ArchiveRoot $p.Archive
    if((Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant() -ne $p.Hash){
        throw "Pinned $($p.Id) archive SHA256 mismatch"
    }
}
$managedLibs=@(
    @{ Archive='dnlib.4.5.0.nupkg'; Entry='lib/net45/dnlib.dll'; Out='dnlib.dll'; Hash='97ef5328d1d1703924c48d9cd1d45b7227fe3836e116dcded623b6a0dbd52c23' },
    @{ Archive='mono.cecil.0.11.6.nupkg'; Entry='lib/net40/Mono.Cecil.dll'; Out='Mono.Cecil.dll'; Hash='c41bdb9ffd3c5f6e17d2382c1012d73703e035e3f1100245fdd4e08c8dc6eb5b' },
    @{ Archive='mono.cecil.0.11.6.nupkg'; Entry='lib/net40/Mono.Cecil.Pdb.dll'; Out='Mono.Cecil.Pdb.dll'; Hash='50a1a1a79dc86fcfb8b51249b5325a10dd93d193c52999cf6775d25030a4e606' }
)
Add-Type -AssemblyName System.IO.Compression
$bin=Join-Path $temp 'bin'
New-Item $bin -ItemType Directory -Force | Out-Null
foreach($item in $managedLibs){
    $file=Join-Path $ArchiveRoot $item.Archive
    $zip=[System.IO.Compression.ZipFile]::OpenRead($file)
    try{
        $entries=@($zip.Entries | Where-Object { $_.FullName -ceq $item.Entry })
        if($entries.Count -ne 1){throw "Missing exact pinned managed DLL entry"}
        $entry=$entries[0]
        if($entry.Length -gt 2MB){throw "Reader DLL outside bounded size"}
        $output=Join-Path $bin $item.Out
        $s=$entry.Open();$dest=[System.IO.File]::Create($output)
        try{$s.CopyTo($dest)}finally{$dest.Dispose();$s.Dispose()}
        if((Get-FileHash $output -Algorithm SHA256).Hash.ToLowerInvariant() -ne $item.Hash){
            throw "Pinned reader binary SHA256 mismatch"
        }
    }finally{$zip.Dispose()}
}

$pf=[Environment]::GetFolderPath('ProgramFilesX86')
$vswhere=Join-Path $pf 'Microsoft Visual Studio\Installer\vswhere.exe'
if(-not (Test-Path $vswhere)){throw 'VS installation discovery unavailable'}
$vsroot=(& $vswhere -latest -products '*' -property installationPath | Select-Object -First 1)
if($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($vsroot)){throw 'VS installation missing'}
$csc=Join-Path $vsroot 'MSBuild\Current\Bin\Roslyn\csc.exe'
if(-not (Test-Path $csc)){throw 'Full Framework Roslyn csc.exe missing'}
$refs=Join-Path $pf 'Reference Assemblies\Microsoft\Framework\.NETFramework\v4.8'
if(-not (Test-Path (Join-Path $refs 'mscorlib.dll'))){throw 'net48 reference assembly unavailable'}
Write-Host "Using Roslyn compiler at VS installation; exact compiler binary SHA256: $((Get-FileHash $csc -Algorithm SHA256).Hash)"
& $csc /help | Select-Object -First 1 | Out-Host

function Compile([string[]]$parts) {
    & $csc @parts | Out-Host
    if($LASTEXITCODE -ne 0){throw 'Compiler fixture/harness build failed'}
}
# Compiled research validators are two different executables. No restore, install or MSBuild import.
$readerSrc=Join-Path $PSScriptRoot 'ReaderProbe.cs'
foreach($reader in @('DNLIB','CECIL')){
    $exe=Join-Path $bin ("ReaderProbe-{0}.exe" -f $reader)
    $refsArg=@("/reference:$(Join-Path $refs 'mscorlib.dll')","/reference:$(Join-Path $refs 'System.dll')","/reference:$(Join-Path $refs 'System.Core.dll')")
    if($reader -eq 'DNLIB'){
        $refsArg+=("/reference:$(Join-Path $bin 'dnlib.dll')")
    }else{
        $refsArg+=("/reference:$(Join-Path $bin 'Mono.Cecil.dll')","/reference:$(Join-Path $bin 'Mono.Cecil.Pdb.dll')")
    }
    $argsList=@('/nologo','/noconfig','/langversion:7.3','/target:exe','/debug-','/optimize+',
        "/define:$reader","/out:$exe") + $refsArg + @($readerSrc)
    Compile $argsList
}

# Produce physical source bytes with controlled CRLF, including UTF-8 BOM/no-BOM.
$cases=@()
foreach($alg in @('SHA1','SHA256')){
    $directory=Join-Path $temp $alg
    New-Item $directory -ItemType Directory -Force | Out-Null
    $alpha=Join-Path $directory 'FixtureAlpha.cs'
    $beta=Join-Path $directory 'FixtureBeta.cs'
    $bom=[Text.UTF8Encoding]::new($true)
    $nobom=[Text.UTF8Encoding]::new($false)
    [IO.File]::WriteAllText($alpha, "public static class FixtureAlpha {`r`n    public static int Add(int left, int right) {`r`n        return left + right;`r`n    }`r`n}`r`n", $bom)
    [IO.File]::WriteAllText($beta, "public static class FixtureBeta {`r`n    public static int Multiply(int left, int right) {`r`n        return left * right;`r`n    }`r`n}`r`n", $nobom)
    $dll=Join-Path $directory "Fixture-$alg.dll"
    $pdb=Join-Path $directory "Fixture-$alg.pdb"
    $cscArgs=@('/nologo','/noconfig','/langversion:7.3','/target:library','/debug:pdbonly',
        '/deterministic-','/optimize-',"/checksumalgorithm:$alg",
        "/reference:$(Join-Path $refs 'mscorlib.dll')","/out:$dll","/pdb:$pdb",$alpha,$beta)
    Compile $cscArgs
    python (Join-Path $PSScriptRoot 'verify_identity.py') --dll $dll --pdb $pdb
    if($LASTEXITCODE -ne 0){throw 'Independent PE/PDB identity gate failed'}
    $expected=@{}
    foreach($src in @($alpha,$beta)){
        $hash=(Get-FileHash $src -Algorithm $alg).Hash.ToLowerInvariant()
        $expected[[IO.Path]::GetFileName($src)]=$hash
    }
    $cases+=@{Alg=$alg;Dir=$directory;Dll=$dll;Pdb=$pdb;Expected=$expected;Alpha=$alpha}
}

function RunBounded([string]$program,[string]$dll,[string]$pdb) {
    $rule="EXP036-BLOCK-NET-" + [guid]::NewGuid().ToString('N')
    $ruleApplied=$false
    try{
        New-NetFirewallRule -DisplayName $rule -Direction Outbound -Action Block -Program $program -Profile Any -ErrorAction Stop | Out-Null
        $ruleApplied=$true
        $start=New-Object System.Diagnostics.ProcessStartInfo
        $start.FileName=$program
        $start.Arguments=('"'+$dll+'" "'+$pdb+'"')
        $start.UseShellExecute=$false
        $start.RedirectStandardOutput=$true
        $start.RedirectStandardError=$true
        $start.CreateNoWindow=$true
        $process=[System.Diagnostics.Process]::Start($start)
        try{
            $deadline=[DateTime]::UtcNow.AddSeconds(20)
            while(-not $process.HasExited -and [DateTime]::UtcNow -lt $deadline){
                $process.Refresh()
                if($process.WorkingSet64 -gt 256MB){throw 'Managed reader exceeded 256MiB working set cap'}
                Start-Sleep -Milliseconds 100
            }
            if(-not $process.HasExited){throw 'Managed reader exceeded 20-second limit'}
            $stdout=$process.StandardOutput.ReadToEnd()
            $stderr=$process.StandardError.ReadToEnd()
            if($process.ExitCode -ne 0){throw "Managed reader returned $($process.ExitCode); error category: $stderr"}
            return $stdout
        }finally{
            if(-not $process.HasExited){$process.Kill();$process.WaitForExit(3000)|Out-Null}
            $process.Dispose()
        }
    }finally{
        if($ruleApplied){Remove-NetFirewallRule -DisplayName $rule -ErrorAction Stop}
    }
}

$result=@()
$shaGuids=@{SHA1='ff1816ec-aa5e-4d10-87f7-6f4963833460';SHA256='8829d00f-11b8-4213-878b-770e8597ac16'}
foreach($case in $cases){
    $all=@{}
    foreach($reader in @('DNLIB','CECIL')){
        $out=RunBounded (Join-Path $bin "ReaderProbe-$reader.exe") $case.Dll $case.Pdb
        $docs=@{}
        $rows=@($out -split "\r?\n" | Where-Object {$_ -like 'DOC*'})
        foreach($line in $rows){
            $fields=$line -split "`t"
            if($fields.Count -ne 4 -or $fields[0] -cne 'DOC'){throw "Invalid reader record"}
            $name=$fields[1]
            if($docs.ContainsKey($name)){throw 'Duplicate source basename in reader'}
            if(-not $case.Expected.ContainsKey($name)){throw 'Unexpected fixture document'}
            if($fields[2] -cne $shaGuids[$case.Alg]){throw "Wrong source checksum GUID for $reader/$($case.Alg)"}
            if($fields[3] -cne $case.Expected[$name]){throw "Source checksum mismatch for $reader/$($case.Alg)"}
            $docs[$name]=$fields[3]
        }
        if($docs.Count -ne $case.Expected.Count){throw "Incomplete source checksum inventory for $reader/$($case.Alg)"}
        $all[$reader]=$docs
        Write-Host "Verified: $reader/$($case.Alg): $($docs.Count) full physical source-byte digests"
    }
    foreach($name in $case.Expected.Keys){
        if($all.DNLIB[$name] -cne $all.CECIL[$name]){throw 'Independent managed reader disagreement'}
    }
    $before=$case.Expected['FixtureAlpha.cs']
    [IO.File]::AppendAllText($case.Alpha,"// MUTATED AFTER COMPILATION`r`n")
    $after=(Get-FileHash $case.Alpha -Algorithm $case.Alg).Hash.ToLowerInvariant()
    if($before -ceq $after){throw 'Mutation negative control did not change physical byte digest'}
    if($all.DNLIB['FixtureAlpha.cs'] -ceq $after){throw 'Mutation negative control should mismatch'}
    Write-Host "Verified: $($case.Alg) post-compilation physical source-byte mutation detected"
    $result+=@{algorithm=$case.Alg;document_count=$all.DNLIB.Count;
        dnlib='matched compiler physical input bytes';cecil='matched compiler physical input bytes';
        mutation_negative='detected';pe_pdb_identity='matched'}
}
# Independent wrong DLL/PDB combination must fail structural identity.
python (Join-Path $PSScriptRoot 'verify_identity.py') --dll $cases[0].Dll --pdb $cases[1].Pdb 2>&1 | Out-Null
if($LASTEXITCODE -eq 0){throw 'Wrong DLL/PDB identity negative control unexpectedly accepted'}
Write-Host 'Verified: wrong DLL/PDB identity rejected'
$summary=@{experiment='EXP-036';evidence='trusted locally generated managed Windows PDB fixture only';
    result='PASS_FIXTURE_ONLY';reader_isolation='separate processes; blocked outbound firewall rule; 20s and 256MiB monitored';
    negative_wrong_pdb='rejected';cases=$result;scope='NO RECORDSIFT PDB INSPECTED; NO SOURCE LINK ACCEPTANCE'}
$summary | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $temp 'fixture-result.json') -Encoding utf8
Write-Host 'EXP036 fixture validation passed, with separate PDB and application gates still open.'


# EXP-037 opt-in: single-source classic PDB differential, no application changes.
# Uses exact same pinned managed readers, compiler, isolated process and controls.
if ($Experiment37Variants) {
    $extra = @()
    # Exact same physical compiler-input source path/bytes across all five variants.
    $sourceRoot37 = Join-Path $temp 'EXP037-source'
    New-Item -ItemType Directory -Force -Path $sourceRoot37 | Out-Null
    $source37 = Join-Path $sourceRoot37 'DifferentialSource.cs'
    [IO.File]::WriteAllText($source37,
        "public static class DifferentialSource {`r`n public static int Identity(int value) { return value; }`r`n}`r`n",
        [Text.UTF8Encoding]::new($false))
    $cases37 = @(
        @{ Name='explicit-sha256'; Deterministic=$false; Map=$false; SourceLink=$false; ExplicitAlgorithm='SHA256' },
        @{ Name='implicit-checksum'; Deterministic=$false; Map=$false; SourceLink=$false; ExplicitAlgorithm=$null },
        @{ Name='deterministic-only'; Deterministic=$true; Map=$false; SourceLink=$false; ExplicitAlgorithm='SHA256' },
        @{ Name='deterministic-pathmap'; Deterministic=$true; Map=$true; SourceLink=$false; ExplicitAlgorithm='SHA256' },
        @{ Name='deterministic-pathmap-sourcelink'; Deterministic=$true; Map=$true; SourceLink=$true; ExplicitAlgorithm='SHA256' }
    )
    foreach ($case37 in $cases37) {
        $caseRoot = Join-Path $temp ('EXP037-' + $case37.Name)
        New-Item -ItemType Directory -Force -Path $caseRoot | Out-Null
        $source = $source37
        $dll = Join-Path $caseRoot 'Differential.dll'
        $pdb = Join-Path $caseRoot 'Differential.pdb'
        $args37 = @('/nologo','/noconfig','/langversion:7.3','/target:library',
            '/debug:pdbonly',"/out:$dll","/pdb:$pdb",
            "/reference:$(Join-Path $refs 'mscorlib.dll')")
        if ($case37.Deterministic) { $args37 += '/deterministic+' }
        else { $args37 += '/deterministic-' }
        $args37 += '/optimize-'
        if ($case37.Map) { $args37 += "/pathmap:$sourceRoot37=/_/" }
        if ($case37.ExplicitAlgorithm) { $args37 += "/checksumalgorithm:$($case37.ExplicitAlgorithm)" }
        if ($case37.SourceLink) {
            $mapping = Join-Path $caseRoot 'sourcelink.json'
            # Synthetic, never fetched. Only the compiler's native symbol-writer behavior is under test.
            [IO.File]::WriteAllText($mapping, '{"documents":{"*":"https://invalid.example.test/synthetic/*"}}',
                [Text.UTF8Encoding]::new($false))
            $args37 += "/sourcelink:$mapping"
        }
        $args37 += $source
        Compile $args37
        python (Join-Path $PSScriptRoot 'verify_identity.py') --dll $dll --pdb $pdb
        if ($LASTEXITCODE -ne 0) { throw 'EXP037 differential PE/PDB identity failed' }
        $views = @{}
        foreach ($reader37 in @('DNLIB','CECIL')) {
            $observed = RunBounded (Join-Path $bin "ReaderProbe-$reader37.exe") $dll $pdb
            $rows37 = @($observed -split '\r?\n' | Where-Object { $_.StartsWith('DOC' + [char]9) })
            $missing37 = @($observed -split '\r?\n' | Where-Object { $_.StartsWith('MISSING' + [char]9) })
            if ($rows37.Count -ne 1 -or $missing37.Count -ne 0) {
                throw "EXP037 $($case37.Name) $reader37 document count or checksum absent"
            }
            $tokens37 = $rows37[0].Split([char]9)
            if ($tokens37.Count -ne 4 -or $tokens37[1] -cne 'DifferentialSource.cs') {
                throw 'EXP037 unexpected managed document identity'
            }
            $algorithm37 = @{'ff1816ec-aa5e-4d10-87f7-6f4963833460'='SHA1';
                '8829d00f-11b8-4213-878b-770e8597ac16'='SHA256'}[$tokens37[2]]
            if (-not $algorithm37) { throw 'EXP037 unexpected algorithm GUID' }
            if ($case37.ExplicitAlgorithm -and $algorithm37 -cne $case37.ExplicitAlgorithm) {
                throw 'EXP037 explicit checksum algorithm ignored'
            }
            $physical37 = (Get-FileHash $source -Algorithm $algorithm37).Hash.ToLowerInvariant()
            if ($tokens37[3] -cne $physical37) {
                throw 'EXP037 physical compiler-input checksum mismatch'
            }
            $views[$reader37] = @{ Algorithm=$algorithm37; Digest=$tokens37[3] }
            Write-Host "EXP037 $($case37.Name) $reader37 verified one physical source digest ($algorithm37)"
        }
        if ($views['DNLIB'].Algorithm -cne $views['CECIL'].Algorithm -or
            $views['DNLIB'].Digest -cne $views['CECIL'].Digest) {
            throw 'EXP037 independent managed readers disagree'
        }
        $extra += [ordered]@{
            name=$case37.Name; checksum_switch=($case37.ExplicitAlgorithm ?? 'OMITTED')
            deterministic=$case37.Deterministic; pathmap=$case37.Map; sourcelink=$case37.SourceLink
            two_independent_readers='MATCHED_PHYSICAL_SOURCE_BYTES'
            checksum_algorithm=$views['DNLIB'].Algorithm; source_documents=1
            native_pdb_identity='MATCHED'
        }
    }
    [ordered]@{
        experiment='EXP-037'; phase='direct_compiler_differential'; result='PASS_FOR_FIVE_SINGLE_VARIABLE_CONTROLLED_FIXTURES'
        compiler_executable_sha256=(Get-FileHash $csc -Algorithm SHA256).Hash.ToLowerInvariant()
        variants=$extra
        limitation='Synthetic direct-csc fixtures only. Cannot assert RecordSift compiler inputs or candidate checksum gate.'
    } | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $temp 'exp037-variants.json') -Encoding utf8
}

# An intentionally failing wrong-PDB native check leaves LASTEXITCODE nonzero.
# Reset it only after all assertions and the summary succeeded.
$global:LASTEXITCODE=0
