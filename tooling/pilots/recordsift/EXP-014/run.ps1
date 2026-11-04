# Read-only RecordSift .NET Framework 4.8 metadata pilot.
# Invoked from the modernization repository by validate-recordsift-assembly-pilot.yml.
# Never checks out a writable RecordSift branch, publishes packages, or merges code.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ApplicationRoot,
    [Parameter(Mandatory = $true)][string]$EvidenceRoot,
    [string]$ExpectedCommit = '8358780829458854a4b0356df5ac5e685f0a34c8',
    [string]$ExperimentId = 'EXP-014'
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$expected = $ExpectedCommit
$application = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$evidence = [IO.Path]::GetFullPath($EvidenceRoot)
if ($evidence.StartsWith($application + [IO.Path]::DirectorySeparatorChar,
                         [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Evidence must be outside the application source checkout.'
}
$commit = (& git -C $application rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $commit -cne $expected) {
    throw "Wrong RecordSift commit: $commit; expected $expected"
}
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
$extractor = Join-Path $repoRoot 'tooling/assembly-metadata/src/bin/Release/net10.0/AssemblyMetadata.dll'
if (-not (Test-Path -LiteralPath $extractor)) { throw "Build the approved extractor first: $extractor" }

$components = @('Domain', 'Application', 'Infrastructure.Csv', 'Infrastructure.Reporting', 'Infrastructure.Xlsx')
$names = @($components | ForEach-Object { "RecordSift.$_" })
$assemblies = @($names | ForEach-Object {
    Join-Path $application ("src/{0}/bin/Release/{0}.dll" -f $_)
})
foreach ($path in $assemblies) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing Release assembly: $path" }
}
# Verify application-owned compiled API and XML documentation gates before new extraction.
Push-Location $application
try {
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $application 'scripts/verify_public_api.ps1')
    if ($LASTEXITCODE -ne 0) { throw "Existing RecordSift public API gate failed: $LASTEXITCODE" }
    & (Join-Path $application 'scripts/verify_xml_documentation.ps1')
    if ($LASTEXITCODE -ne 0) { throw "Existing XML documentation gate failed: $LASTEXITCODE" }

    # Frozen source run_tests.ps1 omits XLSX; execute all FIVE NUnit assemblies explicitly.
    $runner = Join-Path $application 'packages/NUnit.ConsoleRunner.3.17.0/tools/nunit3-console.exe'
    if (-not (Test-Path -LiteralPath $runner)) { throw "NUnit console runner missing: $runner" }
    $testNames = @('Domain', 'Application', 'Infrastructure.Csv', 'Infrastructure.Reporting', 'Infrastructure.Xlsx')
    $testResults = @()
    foreach ($name in $testNames) {
        $testAssembly = Join-Path $application ("tests/RecordSift.{0}.Tests/bin/Release/RecordSift.{0}.Tests.dll" -f $name)
        if (-not (Test-Path -LiteralPath $testAssembly)) { throw "Missing NUnit suite: $testAssembly" }
        $label = $name.ToLowerInvariant().Replace('.', '-')
        $path = Join-Path $evidence ("nunit-{0}.xml" -f $label)
        & $runner $testAssembly "--result=$path;format=nunit3" --noheader
        if ($LASTEXITCODE -ne 0) { throw "NUnit failed for $name ($LASTEXITCODE)" }
        [xml]$resultsXml = Get-Content -LiteralPath $path -Raw
        $node = $resultsXml.'test-run'
        $testResults += [ordered]@{
            name = $name
            total = [int]$node.total
            passed = [int]$node.passed
            failed = [int]$node.failed
            skipped = [int]$node.skipped
        }
    }
    # Ordered hashtables are not PSCustomObjects; sum keyed values explicitly.
    $total = 0; $passed = 0; $failed = 0; $skipped = 0
    foreach ($suite in $testResults) {
        $total += [int]$suite['total']
        $passed += [int]$suite['passed']
        $failed += [int]$suite['failed']
        $skipped += [int]$suite['skipped']
    }
    if ($total -ne 419 -or $passed -ne 418 -or $failed -ne 0 -or $skipped -ne 1) {
        throw "Frozen NUnit baseline changed: total=$total passed=$passed failed=$failed skipped=$skipped"
    }
    Write-Host "PASS: five independent NUnit suites total=$total passed=$passed failed=$failed skipped=$skipped"

    # Execute the application-owned LOCAL build/pack and net48 installed-consumer gates.
    # No NuGet package is published or uploaded as an artifact.
    $packageDir = Join-Path $evidence 'local-package'
    & (Join-Path $application 'scripts/build_release_candidate.ps1') -OutputDirectory $packageDir -PackageVersion '0.1.0'
    if ($LASTEXITCODE -ne 0) { throw 'Local RecordSift package build failed.' }
    & (Join-Path $application 'scripts/verify_clean_consumer.ps1') -CandidateDirectory $packageDir -PackageVersion '0.1.0'
    if ($LASTEXITCODE -ne 0) { throw 'Clean installed consumer check failed.' }
    $package = Join-Path $packageDir 'RecordSift.0.1.0.nupkg'
    if (-not (Test-Path -LiteralPath $package)) { throw 'Application-owned package gate did not produce nupkg.' }
}
finally { Pop-Location }

# Build and packaging legitimately populate some nontracked directories in the
# disposable build checkout. Verify tracked source was NOT modified, then
# independently attach a clean Git worktree at the exact SAME immutable SHA
# for source attribution. Do not label a dirty build checkout as clean.
$trackedChanges = @(& git -C $application diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0 -or $trackedChanges.Count -gt 0) {
    throw "Tracked RecordSift source changed during pilot: $($trackedChanges -join ' | ')"
}
$buildCheckoutStatus = @(& git -C $application status --porcelain --untracked-files=normal)
Write-Host "Build checkout changed/untracked paths: $($buildCheckoutStatus.Count)"
if ($buildCheckoutStatus.Count -gt 0) {
    $buildCheckoutStatus | ForEach-Object { Write-Host "Build output status: $_" }
}
$sourceProof = Join-Path $evidence 'clean-source-revision'
if (Test-Path -LiteralPath $sourceProof) { throw 'Source proof worktree already exists.' }
& git -C $application worktree add --detach $sourceProof $expected
if ($LASTEXITCODE -ne 0) { throw 'Unable to create exact detached source proof worktree.' }
$sourceProofStatus = @(& git -C $sourceProof status --porcelain --untracked-files=normal)
$proofSha = (& git -C $sourceProof rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $proofSha -cne $expected -or $sourceProofStatus.Count -gt 0) {
    throw "Independent provenance checkout invalid: sha=$proofSha, dirty=$($sourceProofStatus -join ' | ')"
}
Write-Host "PASS: independent clean source attribution worktree at $proofSha"
$first = Join-Path $evidence 'first'
$second = Join-Path $evidence 'repeat'
foreach ($dir in @($first, $second)) {
    if (Test-Path -LiteralPath $dir) { throw "Pilot evidence destination must not already exist: $dir" }
    # The extractor does not load or execute RecordSift code, even on Windows.
    $extractArgs = @($extractor)
    foreach ($assembly in $assemblies) { $extractArgs += '--assembly'; $extractArgs += $assembly }
    $extractArgs += '--output-dir'; $extractArgs += $dir
    & dotnet @extractArgs
    if ($LASTEXITCODE -ne 0) { throw "Metadata extractor failed: $LASTEXITCODE" }
    foreach ($result in Get-ChildItem -LiteralPath $evidence -Filter 'nunit-*.xml' -File) {
        Copy-Item -LiteralPath $result.FullName -Destination $dir
    }
    Copy-Item -LiteralPath $package -Destination (Join-Path $dir 'RecordSift.0.1.0.nupkg')
}
$spec = Join-Path $PSScriptRoot 'compatibility-spec.json'
$comparator = Join-Path $repoRoot 'tooling/validators/compatibility.py'
$baseline = Join-Path $evidence 'baseline.json'
$candidate = Join-Path $evidence 'repeat.json'
$comparison = Join-Path $evidence 'comparison.json'
foreach ($case in @(@{ root = $first; file = $baseline }, @{ root = $second; file = $candidate })) {
    & python $comparator capture --source $sourceProof --artifacts-root $case.root --spec $spec --expect-commit $expected --output $case.file
    if ($LASTEXITCODE -ne 0) { throw "Compatibility capture failed: $LASTEXITCODE" }
}
& python $comparator compare --baseline $baseline --candidate $candidate --output $comparison
$comparisonCode = $LASTEXITCODE
$comparisonData = Get-Content -LiteralPath $comparison -Raw | ConvertFrom-Json
if ($comparisonCode -ne 0) {
    Write-Host "Baseline Git evidence: $($comparisonData.baseline_source | ConvertTo-Json -Compress -Depth 4)"
    Write-Host "Candidate Git evidence: $($comparisonData.candidate_source | ConvertTo-Json -Compress -Depth 4)"
    throw "Independent repeated binary snapshot comparison failed: $comparisonCode; status=$($comparisonData.overall)"
}
if ($comparisonData.overall -cne 'matched') { throw "Expected clean committed repeat match, got $($comparisonData.overall)" }

# Negative control: a deliberately altered **external evidence file** must cause a detectable difference.
$negativeDir = Join-Path $evidence 'negative'
Copy-Item -LiteralPath $first -Destination $negativeDir -Recurse
$negativeApi = Join-Path $negativeDir 'public-api.txt'
Add-Content -LiteralPath $negativeApi -Value 'assembly RecordSift.Domain :: deliberately-unapproved-contract' -Encoding utf8
$negativeSnapshot = Join-Path $evidence 'negative.json'
$negativeComparison = Join-Path $evidence 'negative-comparison.json'
& python $comparator capture --source $sourceProof --artifacts-root $negativeDir --spec $spec --expect-commit $expected --output $negativeSnapshot
if ($LASTEXITCODE -ne 0) { throw 'Negative evidence capture failed unexpectedly.' }
& python $comparator compare --baseline $baseline --candidate $negativeSnapshot --output $negativeComparison
$negativeCode = $LASTEXITCODE
$negativeData = Get-Content -LiteralPath $negativeComparison -Raw | ConvertFrom-Json
if ($negativeCode -ne 1 -or $negativeData.overall -cne 'changes_detected' -or
    $negativeData.components.api.status -cne 'changed') {
    throw "Comparator negative control invalid: exit=$negativeCode, overall=$($negativeData.overall)"
}
$assemblyHashes = @($assemblies | ForEach-Object {
    [ordered]@{ name = [IO.Path]::GetFileName($_); sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash.ToLowerInvariant() }
})
$report = [ordered]@{
    experiment = $ExperimentId
    source_repository = 'infoconex/RecordSift'
    source_commit = $expected
    provenance_worktree = 'separate clean detached worktree at same exact SHA'
    build_checkout_status = $buildCheckoutStatus
    extractor_repository = 'infoconex/dotnet-modernization'
    extractor_commit = (& git -C $repoRoot rev-parse HEAD).Trim()
    runtime = 'Windows Server 2022 / .NET 10 metadata reader with .NET Framework 4.8 release binaries'
    checks = [ordered]@{
        existing_api_gate = 'passed'
        xml_documentation_gate = 'passed'
        nunit_baseline = '418 passed; 1 skipped; 0 failed / 419 total (five suites)'
        package_build = 'passed'
        clean_net48_consumer = 'passed'
        repeat_snapshot_comparison = $comparisonData.overall
        intentionally_modified_api_evidence = $negativeData.overall
        no_application_source_commit = 'enforced'
    }
    assembly_sha256 = $assemblyHashes
    nunit_suites = $testResults
}
$report | ConvertTo-Json -Depth 9 | Set-Content -LiteralPath (Join-Path $evidence 'pilot-report.json') -Encoding utf8
$finalTrackedChanges = @(& git -C $application diff --name-only HEAD --)
if ($LASTEXITCODE -ne 0 -or $finalTrackedChanges.Count -ne 0) {
    throw "Tracked RecordSift source checkout was modified: $($finalTrackedChanges -join ' | ')"
}
$cleanProofStatus = @(& git -C $sourceProof status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $cleanProofStatus.Count -ne 0) {
    throw "Source attribution worktree is dirty: $($cleanProofStatus -join ' | ')"
}
Write-Host "PASS: Real RecordSift .NET Framework 4.8 pilot, source SHA $expected; all five assemblies and suite gates passed."
Write-Host 'This validates an unchanged-source REPEAT, NOT a migration candidate or a change in target framework.'
