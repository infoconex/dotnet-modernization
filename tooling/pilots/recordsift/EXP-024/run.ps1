# EXP-024: actual Source Link task-import/build probe, manual import simulation only.
# No edits survive the disposable checkout. No app push, package publish or symbol upload.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ApplicationRoot,
      [Parameter(Mandatory=$true)][string]$EvidenceRoot,
      [switch]$CaptureLoadedModules, [switch]$CaptureCompilerSources)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$frozen = '8358780829458854a4b0356df5ac5e685f0a34c8'
$app = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence = [IO.Path]::GetFullPath($EvidenceRoot)
$research = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
if ($evidence.StartsWith($app + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
    throw 'Evidence must be outside disposable RecordSift checkout.'
}
if (Test-Path -LiteralPath $evidence) { throw 'Evidence destination must be new.' }
if ((& git -C $app rev-parse HEAD).Trim() -cne $frozen -or $LASTEXITCODE -ne 0) {
    throw 'RecordSift source is not the frozen commit.'
}
if (@(& git -C $app status --porcelain).Count -ne 0) { throw 'Initial source checkout must be clean.' }
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$report = [ordered]@{
  experiment = 'EXP-024'; phase='manual_import_simulation'; frozen_commit=$frozen
  baseline='not_executed'; archive_integrity='not_executed'; task_imports='not_executed'
  source_control_initialization='not_executed'; compile='not_executed'
  pdb_format='not_inspected'; application_release_gates='not_executed'
  package_reference_policy='preserve_existing_nine_entries; do_not_resolve_new_nuget_graph'
  source_link_runtime_isolation='not_proven'
  caveat='No Visual Studio NuGet Package Manager install semantics asserted. No debugger validation.'
}
function Write-Report { $report | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $evidence 'experiment-report.json') -Encoding utf8 }
function Assert-Exit([string]$message) { if ($LASTEXITCODE -ne 0) { throw "$message (exit $LASTEXITCODE)" } }
function Check-Frozen([bool]$allowTemporaryProject) {
    if ((& git -C $app rev-parse HEAD).Trim() -cne $frozen) { throw 'Source HEAD changed.' }
    $diff = @(& git -C $app diff --name-only HEAD --)
    Assert-Exit 'Git diff check failed'
    if ($allowTemporaryProject) {
        if (@($diff | Where-Object { $_ -cne 'src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj' }).Count -ne 0) {
            throw "Unexpected tracked changes: $($diff -join ',')"
        }
    } elseif ($diff.Count -gt 0) { throw "Tracked source changed: $($diff -join ',')" }
}
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild was not found.' }
$msbuildVersion = ((& $msbuild -version -nologo) | Select-Object -Last 1).Trim()
$report.msbuild_version = $msbuildVersion
$project = Join-Path $app 'src/RecordSift.Infrastructure.Csv/RecordSift.Infrastructure.Csv.csproj'
$config = Join-Path $app 'src/RecordSift.Infrastructure.Csv/packages.config'
$originalProject = [IO.File]::ReadAllBytes($project)
$originalConfig = [IO.File]::ReadAllBytes($config)
$beforeConfigHash = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash.ToLowerInvariant()
$beforeProjectHash = (Get-FileHash -LiteralPath $project -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedArchives = @(
    @{id='Microsoft.SourceLink.GitHub';version='10.0.403';sha='9c3252f8cbe1547bf8c12b7c65a7bc28985bab2d598ff97c13e0104c22d80cd5'},
    @{id='Microsoft.SourceLink.Common';version='10.0.403';sha='e99d7aea402042d04faa4971709718ebf256406b4c59f700cb1c8a739859c6a2'},
    @{id='Microsoft.Build.Tasks.Git';version='10.0.403';sha='9d21a711e9fce96b34e8c02f10069bc66a381d84a2912e65a14dc9c411135e29'}
)
$baselineFiles = @{}
try {
    Push-Location $app
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config | Out-Host
        Assert-Exit 'Original packages.config NuGet restore failed'
        & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal | Out-Host
        Assert-Exit 'Original solution baseline build failed'
    } finally { Pop-Location }
    $report.baseline='full_solution_compiled'
    Write-Report

    # Strong historical gates, same release baseline and original test/consumer scripts.
    & (Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1') -ApplicationRoot $app -EvidenceRoot (Join-Path $evidence 'baseline-acceptance') -ExpectedCommit $frozen -ExperimentId 'EXP-024-baseline' | Out-Host
    Assert-Exit 'Original frozen release/consumer gates failed'
    $report.baseline='full_solution_425_api_419_tests_5_xml_local_package_clean_consumer_pass'
    $csvBin=Join-Path $app 'src/RecordSift.Infrastructure.Csv/bin/Release'
    $baselineFiles=@{}
    Get-ChildItem -LiteralPath $csvBin -File | ForEach-Object {
        $baselineFiles[$_.Name] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    Check-Frozen $false
    Write-Report

    # Fetch pinned, audited build-task packages. Do not install System.IO.Hashing or
    # upgrade System.Memory/Buffers; their task copies exist under tools/netframework.
    # This is an explicit import simulation, NOT NuGet Package Manager installation.
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $pinnedAssets = @()
    foreach ($p in $expectedArchives) {
        $lower=$p.id.ToLowerInvariant();$version=$p.version
        $archive=Join-Path $evidence ("$lower.$version.nupkg")
        $uri="https://api.nuget.org/v3-flatcontainer/$lower/$version/$lower.$version.nupkg"
        Invoke-WebRequest -Uri $uri -OutFile $archive -TimeoutSec 60 -ErrorAction Stop
        if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant() -cne $p.sha) {
            throw "Official archive hash differs: $($p.id)"
        }
        $destination=Join-Path $app ("packages/$($p.id).$version")
        if (Test-Path -LiteralPath $destination) { throw "Unexpected preexisting package directory: $destination" }
        [IO.Compression.ZipFile]::ExtractToDirectory($archive,$destination)
        $pinnedAssets+=@{id=$p.id;version=$version;sha256=$p.sha;contents='manual_zip_extract_no_NuGet_install'}
    }
    $report.archive_integrity='three_verified_official_archives_extracted_to_disposable_packages_only'
    $report.provider_archives=$pinnedAssets
    if ((Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash.ToLowerInvariant() -cne $beforeConfigHash) {
        throw 'Original packages.config changed.'
    }
    Write-Report

    # The root is exactly ../.. from this project. Preserve the existing references
    # and Release DebugType=pdbonly. Props BEFORE CSharp targets, targets AFTER.
    $projectText=[Text.Encoding]::UTF8.GetString($originalProject)
    $anchor='  <Import Project="$(MSBuildToolsPath)\Microsoft.CSharp.targets" />'
    if (-not $projectText.Contains($anchor)) { throw 'Unexpected traditional project structure.' }
    $props=@();$targets=@()
    foreach ($p in $expectedArchives) {
        $id=$p.id;$version=$p.version
        $relative="..\..\packages\$id.$version\build\$id"
        foreach ($ext in @('props','targets')) {
            $full=Join-Path (Split-Path -Parent $project) "$relative.$ext"
            if (-not (Test-Path -LiteralPath $full)) { throw "Real required package import missing: $full" }
            $entry="  <Import Project=`"$relative.$ext`" />"
            if ($ext -eq 'props') {$props+= $entry} else {$targets+= $entry}
        }
    }
    $replacement=($props -join "`r`n") + "`r`n" + $anchor + "`r`n" + ($targets -join "`r`n")
    $modified=$projectText.Replace($anchor,$replacement)
    if ($CaptureLoadedModules) {
        $probeFile=Join-Path $research 'tooling/pilots/recordsift/EXP-032/ModuleProbe.targets'
        if (-not (Test-Path -LiteralPath $probeFile)) { throw 'Missing independent module capture import.' }
        $escaped=[Security.SecurityElement]::Escape($probeFile)
        $probeImport='  <Import Project="' + $escaped + '" />'
        $rootEnd=$modified.LastIndexOf('</Project>',[StringComparison]::Ordinal)
        if ($rootEnd -lt 0 -or $modified.IndexOf('</Project>',$rootEnd + 1,[StringComparison]::Ordinal) -ge 0) {
            throw 'Cannot safely locate root project closing element.'
        }
        $modified=$modified.Substring(0,$rootEnd) + $probeImport + [Environment]::NewLine + $modified.Substring($rootEnd)
    }

    if ($CaptureCompilerSources) {
        # Imported ONLY into the disposable, temporary CSV project after source-link imports.
        # Captures exact @(Compile) physical bytes immediately before CoreCompile; no PDB
        # path strings are trusted as file paths. Before/after bytes must remain identical.
        $captureTargets=Join-Path $research 'tooling/pilots/recordsift/EXP-041/CompilerInputSnapshot.targets'
        if (-not (Test-Path -LiteralPath $captureTargets)) { throw 'EXP041 source snapshot task missing' }
        $escapedTargets=[Security.SecurityElement]::Escape($captureTargets)
        $captureImport='  <Import Project="' + $escapedTargets + '" />'
        $rootEnd=$modified.LastIndexOf('</Project>',[StringComparison]::Ordinal)
        if ($rootEnd -lt 0) { throw 'EXP041 invalid temporary project root' }
        $modified=$modified.Substring(0,$rootEnd) + $captureImport + [Environment]::NewLine + $modified.Substring($rootEnd)
    }
    [IO.File]::WriteAllText($project,$modified,[Text.UTF8Encoding]::new($false))
    Check-Frozen $true
    $baseArgs=@($project,'/p:Configuration=Release','/p:Platform=AnyCPU','/p:Deterministic=true','/p:ContinuousIntegrationBuild=true','/p:BuildProjectReferences=false','-nologo')
    $pp=Join-Path $evidence 'msbuild-preprocessed.xml'
    & $msbuild @baseArgs "/pp:$pp" | Out-Null
    Assert-Exit 'MSBuild preprocessing failed'
    $preprocessed=[IO.File]::ReadAllText($pp)
    foreach ($p in $expectedArchives) {
        if (-not $preprocessed.Contains("build\$($p.id).targets") -or -not $preprocessed.Contains("build\$($p.id).props")) {
            throw "Missing evaluated import in preprocessor: $($p.id)"
        }
    }
    $report.task_imports='three_provider_props_and_targets_confirmed_in_preprocessor'
    Write-Report

    # Query actual source-control target invocation and effective properties.
    $targetOutput=@(& $msbuild @baseArgs '/t:InitializeSourceControlInformation' '-getProperty:SourceRevisionId' '-getItem:SourceRoot' 2>&1)
    $targetExit=$LASTEXITCODE
    if ($targetExit -ne 0) {throw "InitializeSourceControlInformation target failed ($targetExit): $(($targetOutput|Select-Object -Last 4) -join ' | ')"} 
    $joined=$targetOutput -join [Environment]::NewLine
    $report.source_control_initialization='InitializeSourceControlInformation_target_succeeded'
    $report.source_revision_observed=($joined -match [regex]::Escape($frozen))
    $report.source_root_observed=($joined -match 'SourceRoot')
    Write-Report

    # Run only CSV with project references disabled; the other original projects
    # remain compiled but are not given CI=true (EXP-021 proved that would fail).
    $log=Join-Path $evidence 'msbuild-diagnostic-private.log'
    $compileArgs=@($baseArgs)
    if ($CaptureLoadedModules) {
       $modulePrivate=Join-Path $evidence 'msbuild-task-modules-private.txt'
       $compileArgs+=("/p:SourceLinkProbeOutput=$modulePrivate")
    }

    if ($CaptureCompilerSources) {
        $privateCapture=Join-Path $evidence 'exp041-original-inputs-private'
        if (Test-Path -LiteralPath $privateCapture) { throw 'EXP041 private capture must be new' }
        $compileArgs+=("/p:SourceInputCaptureRoot=$privateCapture")
    }
    & $msbuild @compileArgs '/t:Rebuild' '/verbosity:diagnostic' *> $log
    $exit=$LASTEXITCODE
    if ($exit -ne 0) {
        $report.compile="failed_exit_$exit"
        Write-Report
        Get-Content -LiteralPath $log | Select-Object -Last 35 | Out-Host
        throw 'Provider-integrated CSV compile failed; preserve failure evidence.'
    }

    $report.compile='csv_release_completed'
    if ($CaptureCompilerSources) {
        if (-not (Test-Path -LiteralPath (Join-Path $privateCapture 'input-manifest.tsv'))) {
            throw 'EXP041 pre- and post-CoreCompile private source capture unavailable'
        }
        $report.original_csc_source_capture='physical_inputs_pre_and_post_corecompile_verified_privately'
        $report.original_csc_source_capture_scope='Csc @(Compile) task inputs from disposable frozen CSV project only'
        Write-Report
    }
    if ($CaptureLoadedModules) {
       if (-not (Test-Path -LiteralPath $modulePrivate)) {
          throw 'MSBuild did not execute in-process assembly module capture after CoreCompile.'
       }
       $moduleRows=@(Get-Content -LiteralPath $modulePrivate)
       if ($moduleRows.Count -lt 1 -or $moduleRows[0] -notmatch '^HOST\|\d+\|\d+$') {
          throw 'Missing process/AppDomain identity in captured MSBuild module evidence.'
       }
       $report.task_probe_host_identity_observed=$true
       $summaries=@()
       foreach ($line in ($moduleRows | Select-Object -Skip 1)) {
          $parts=$line.Split('|',3)
          if ($parts.Count -ne 3) {throw 'Malformed assembly module row.'}
          $assembly=$parts[0];$version=$parts[1];$full=$parts[2]
          $category=if ($full.StartsWith((Join-Path $app 'packages') + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) {
            if($full -match '(?i)Microsoft\.(SourceLink|Build\.Tasks\.Git)\.'){'isolated_build_tool_package_tree'}
            else {'existing_application_package_tree'}
          }elseif ($full.StartsWith($app + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){
            'inside_disposable_application'
          }elseif ($full -match '(?i)^[A-Z]:\\Program Files\\') {
            'preinstalled_host_toolchain'
          }else {'other_external_location'}
          $summaries+=@([ordered]@{name=$assembly;version=$version;location_category=$category})
       }
       $report.loaded_module_categories=$summaries
       $report.module_observation_scope='same AppDomain as diagnostic RoslynCodeTaskFactory; not a proof of all other MSBuild nodes'
       # Raw full module paths remain in the ephemeral private text file and are
       # NOT included in upload-artifact paths.
       Write-Report
    }
    $logText=[IO.File]::ReadAllText($log)
    $report.source_link_compiler_argument_observed=($logText -match '/sourcelink:')
    $report.provider_task_assembly_observed=($logText -match 'tools[\\/]netframework[\\/]Microsoft\.Build\.Tasks\.Git\.dll')
    $report.source_revision_observed= $report.source_revision_observed -or ($logText -match [regex]::Escape($frozen))
    $pdb=Join-Path $csvBin 'RecordSift.Infrastructure.Csv.pdb'
    if (-not (Test-Path -LiteralPath $pdb)) { throw 'Missing CSV Release PDB.' }
    $bytes=[IO.File]::ReadAllBytes($pdb)
    $isNativeWindowsPdb=([Text.Encoding]::ASCII.GetString($bytes,0,[Math]::Min(32,$bytes.Length)) -like 'Microsoft C/C++ MSF 7.00*')
    $report.pdb_format=if($isNativeWindowsPdb){'windows_pdb_msf_signature'}else{'not_classic_windows_pdb'}
    if (-not $isNativeWindowsPdb) {throw 'PDB format unexpectedly changed; do not claim Windows PDB success.'}
    # Source Link binary contents remain private for separate structural PDB gate.
    $report.csv_bin_added_files=@(Get-ChildItem -LiteralPath $csvBin -File | Where-Object {-not $baselineFiles.ContainsKey($_.Name)} | Select-Object -ExpandProperty Name)
    $report.csv_bin_changed_files=@(Get-ChildItem -LiteralPath $csvBin -File | Where-Object {
      $baselineFiles.ContainsKey($_.Name) -and (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() -cne $baselineFiles[$_.Name]
    } | Select-Object -ExpandProperty Name)
    $forbidden=@($report.csv_bin_added_files | Where-Object { $_ -match '^(Microsoft\.SourceLink\.|Microsoft\.Build\.Tasks\.Git|System\.IO\.Hashing|System\.Memory|System\.Buffers)' })
    if ($forbidden.Count -gt 0) { throw "New build-task/runtime DLL copied into output: $($forbidden -join ',')" }
    # Keep the exact candidate binaries for the original test and consumer gates.
    # NUnit test projects have copy-local infrastructure dependencies; replace
    # their original CSV copy with the candidate, or they would exercise OLD code.
    $candidateDll=Join-Path $csvBin 'RecordSift.Infrastructure.Csv.dll'
    $candidateDllHash=(Get-FileHash -LiteralPath $candidateDll -Algorithm SHA256).Hash.ToLowerInvariant()
    $injectedCopies=0
    foreach ($suite in @('Domain','Application','Infrastructure.Csv','Infrastructure.Reporting','Infrastructure.Xlsx')) {
        $bin=Join-Path $app ("tests/RecordSift.$suite.Tests/bin/Release")
        $local=Join-Path $bin 'RecordSift.Infrastructure.Csv.dll'
        if (Test-Path -LiteralPath $local) {
            Copy-Item -LiteralPath $candidateDll -Destination $local -Force
            if ((Get-FileHash -LiteralPath $local -Algorithm SHA256).Hash.ToLowerInvariant() -cne $candidateDllHash) {
                throw "Candidate assembly did not reach test execution directory for $suite."
            }
            $injectedCopies++
        }
    }
    if ($injectedCopies -lt 1) { throw 'No candidate CSV binary present in test execution directories.' }
    $report.candidate_test_bin_copies=$injectedCopies
    # Restore tracked csproj BEFORE existing original release gate scripts
    # (their checks must observe a clean source commit), without recompiling CSV.
    [IO.File]::WriteAllBytes($project,$originalProject)
    Check-Frozen $false
    $report.application_release_gates='candidate_started'
    Write-Report
    $candidateEvidence=Join-Path $evidence 'candidate-acceptance'
    & (Join-Path $research 'tooling/pilots/recordsift/EXP-014/run.ps1') -ApplicationRoot $app -EvidenceRoot $candidateEvidence -ExpectedCommit $frozen -ExperimentId 'EXP-024-candidate' | Out-Host
    Assert-Exit 'Original source API/NUnit/XML/package/consumer gate failed with candidate CSV'
    if ((Get-FileHash -LiteralPath $candidateDll -Algorithm SHA256).Hash.ToLowerInvariant() -cne $candidateDllHash) {
        throw 'Candidate CSV bytes changed during original release gates.'
    }
    $comparison=Join-Path $evidence 'candidate-versus-original-compatibility.json'
    & python (Join-Path $research 'tooling/validators/compatibility.py') compare --baseline (Join-Path $evidence 'baseline-acceptance/baseline.json') --candidate (Join-Path $candidateEvidence 'baseline.json') --output $comparison
    Assert-Exit 'Candidate vs original compatibility comparison failed'
    $match=Get-Content -LiteralPath $comparison -Raw | ConvertFrom-Json
    if ($match.overall -cne 'matched') { throw "Candidate contracts changed: $($match.overall)" }
    $report.application_release_gates='candidate_425_api_419_nunit_5_xml_local_package_clean_consumer_passed'
    $report.logical_compatibility='five_categories_matched_original'
    $report.candidate_csv_sha256=$candidateDllHash
    Write-Report
    Write-Host ('EXP-024 scoped result: '+($report | ConvertTo-Json -Depth 6 -Compress))
} catch {
    $report.failure=$_.Exception.Message
    Write-Report
    throw
} finally {
    # Restore tracked csproj bytes even when task initialization/build fails.
    [IO.File]::WriteAllBytes($project,$originalProject)
    if ((Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash.ToLowerInvariant() -cne $beforeConfigHash) {
        throw 'packages.config was changed; restore original frozen checkout manually (disposable only).'
    }
    Check-Frozen $false
}
