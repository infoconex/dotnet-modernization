# EXP-016: a compiled public-enum contract regression from isolated source, not edited evidence.
# Source changes are committed in CI only and never pushed to RecordSift.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ApplicationRoot,
    [Parameter(Mandatory = $true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$baselineSha = '8358780829458854a4b0356df5ac5e685f0a34c8'
$application = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$evidence = [IO.Path]::GetFullPath($EvidenceRoot)
if ($evidence.StartsWith($application + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Evidence must be outside RecordSift.'
}
$sourceSha = (& git -C $application rev-parse --verify HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $sourceSha -cne $baselineSha) { throw "Unexpected RecordSift SHA $sourceSha" }
$initial = @(& git -C $application status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $initial.Count -ne 0) { throw 'Initial candidate checkout is dirty.' }
if (Test-Path -LiteralPath $evidence) { throw 'Evidence destination must not preexist.' }
New-Item -ItemType Directory -Path $evidence | Out-Null

$baseline = Join-Path $evidence 'baseline-source'
& git -C $application worktree add --detach $baseline $baselineSha
if ($LASTEXITCODE -ne 0) { throw 'Separate baseline worktree creation failed.' }
$pilot = Join-Path $repoRoot 'tooling/pilots/recordsift/EXP-014/run.ps1'
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild not found.' }
[ordered]@{
    windows = [Environment]::OSVersion.VersionString
    dotnet_sdk = (& dotnet --version).Trim()
    msbuild_path = $msbuild
    msbuild_version = ((& $msbuild -version -nologo) | Select-Object -Last 1).Trim()
    pwsh = $PSVersionTable.PSVersion.ToString()
} | ConvertTo-Json | Set-Content (Join-Path $evidence 'toolchain.json') -Encoding utf8

function Invoke-ReleaseBuild([string]$root) {
    Push-Location $root
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
        if ($LASTEXITCODE -ne 0) { throw "NuGet restore failed in $root" }
        & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
        if ($LASTEXITCODE -ne 0) { throw "Ten-project Release rebuild failed in $root" }
    }
    finally { Pop-Location }
}

Invoke-ReleaseBuild $baseline
$baseEvidence = Join-Path $evidence 'baseline-evidence'
& $pilot -ApplicationRoot $baseline -EvidenceRoot $baseEvidence -ExpectedCommit $baselineSha -ExperimentId 'EXP-016-frozen-baseline'
if ($LASTEXITCODE -ne 0) { throw 'Original full compatibility baseline failed.' }
$initialAgain = @(& git -C $application status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $initialAgain.Count -ne 0) { throw 'Baseline unexpectedly modified candidate.' }

# Preserve symbol name and uses, alter only the compiled numeric value.
$relative = 'src/RecordSift.Domain/Results/ImportStatus.cs'
$path = Join-Path $application $relative
$before = [IO.File]::ReadAllText($path)
$pattern = '(?m)^        Canceled(?=\r?$)'
if ([regex]::Matches($before, $pattern).Count -ne 1) { throw 'Expected one implicit Canceled enum literal.' }
[IO.File]::WriteAllText($path, [regex]::Replace($before, $pattern, '        Canceled = 42'), [Text.UTF8Encoding]::new($false))
& git -C $application add -- $relative
if ($LASTEXITCODE -ne 0) { throw 'Could not stage source regression.' }
& git -C $application -c 'user.name=Modernization research' -c 'user.email=research@example.invalid' commit -m 'EXP-016 ephemeral incompatible enum literal'
if ($LASTEXITCODE -ne 0) { throw 'Could not commit ephemeral source regression.' }
$candidateSha = (& git -C $application rev-parse --verify HEAD).Trim()
$changed = @(& git -C $application diff --name-only $baselineSha $candidateSha)
if ($LASTEXITCODE -ne 0 -or $changed.Count -ne 1 -or $changed[0] -cne $relative) {
    throw "Unexpected source mutation: $($changed -join ', ')"
}
$baselineTree = (& git -C $baseline rev-parse 'HEAD^{tree}').Trim()
$candidateTree = (& git -C $application rev-parse 'HEAD^{tree}').Trim()
if ($LASTEXITCODE -ne 0 -or $baselineTree -ceq $candidateTree) { throw 'Candidate source tree unchanged or invalid.' }
$patch = @(& git -C $application diff --no-ext-diff $baselineSha $candidateSha -- $relative)
if ($LASTEXITCODE -ne 0) { throw 'Could not save source patch.' }
$patch | Set-Content (Join-Path $evidence 'candidate.patch') -Encoding utf8
$clean = @(& git -C $application status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $clean.Count -ne 0) { throw 'Committed source revision must be clean.' }

Invoke-ReleaseBuild $application
$candidateEvidence = Join-Path $evidence 'candidate-evidence'
& $pilot -ApplicationRoot $application -EvidenceRoot $candidateEvidence -ExpectedCommit $candidateSha -ExperimentId 'EXP-016-source-api-regression' -ExpectCanceledEnumRegression
if ($LASTEXITCODE -ne 0) { throw 'Candidate expected-negative API gate or other positive gates failed.' }

$comparator = Join-Path $repoRoot 'tooling/validators/compatibility.py'
$baseSnapshot = Join-Path $baseEvidence 'baseline.json'
$candidateSnapshot = Join-Path $candidateEvidence 'baseline.json'
$comparisonFile = Join-Path $evidence 'source-api-regression-comparison.json'
& python $comparator compare --baseline $baseSnapshot --candidate $candidateSnapshot --output $comparisonFile
$comparisonExit = $LASTEXITCODE
$comparison = Get-Content -LiteralPath $comparisonFile -Raw | ConvertFrom-Json
if ($comparisonExit -ne 1 -or $comparison.overall -cne 'changes_detected' -or
    $comparison.provenance -cne 'clean_committed' -or $comparison.components.api.status -cne 'changed') {
    throw "Expected compiled API regression was missed: exit=$comparisonExit overall=$($comparison.overall)"
}
foreach ($category in @('assemblies', 'resources', 'packages', 'tests')) {
    if ($comparison.components.$category.status -cne 'matched') {
        throw "Unexpected $category mismatch: $($comparison.components.$category.status)"
    }
}
if ($comparison.components.api.diff_truncated) { throw 'API diff unexpectedly truncated.' }
$diffs = @($comparison.components.api.differences)
$old = 'field RecordSift.Domain.Results.ImportStatus.Canceled public const type=RecordSift.Domain.Results.ImportStatus value=3'
$new = 'field RecordSift.Domain.Results.ImportStatus.Canceled public const type=RecordSift.Domain.Results.ImportStatus value=42'
if ($diffs.Count -ne 2 -or
    @($diffs | Where-Object { $_.change -ceq 'removed' -and $_.baseline -ceq $old }).Count -ne 1 -or
    @($diffs | Where-Object { $_.change -ceq 'added' -and $_.candidate -ceq $new }).Count -ne 1) {
    throw "Unexpected metadata differences: $($diffs | ConvertTo-Json -Depth 5)"
}
Write-Host 'EXPECTED NEGATIVE: compiled enum literal 3 -> 42 detected; four other contracts matched.'

# Explicit missing-evidence control: a required missing API file yields incomplete, never matched.
$missingRoot = Join-Path $evidence 'missing-api-evidence'
Copy-Item -LiteralPath (Join-Path $candidateEvidence 'first') -Destination $missingRoot -Recurse
Remove-Item -LiteralPath (Join-Path $missingRoot 'public-api.txt') -ErrorAction Stop
$missingSnapshot = Join-Path $evidence 'missing-api-snapshot.json'
$missingComparison = Join-Path $evidence 'missing-api-comparison.json'
$spec = Join-Path $repoRoot 'tooling/pilots/recordsift/EXP-014/compatibility-spec.json'
$proof = Join-Path $candidateEvidence 'clean-source-revision'
& python $comparator capture --source $proof --artifacts-root $missingRoot --spec $spec --expect-commit $candidateSha --output $missingSnapshot
$missingCaptureExit = $LASTEXITCODE
& python $comparator compare --baseline $baseSnapshot --candidate $missingSnapshot --output $missingComparison
$missingCompareExit = $LASTEXITCODE
$missing = Get-Content -LiteralPath $missingComparison -Raw | ConvertFrom-Json
if ($missingCaptureExit -ne 1 -or $missingCompareExit -ne 1 -or
    $missing.overall -cne 'incomplete' -or $missing.components.api.status -cne 'missing_evidence') {
    throw "Missing evidence must fail closed: capture=$missingCaptureExit compare=$missingCompareExit status=$($missing.overall)"
}
$summary = [ordered]@{
    experiment = 'EXP-016'
    frozen_source_sha = $baselineSha
    frozen_tree_sha = $baselineTree
    ephemeral_candidate_sha = $candidateSha
    ephemeral_candidate_tree = $candidateTree
    changed_path = $relative
    source_change = 'RecordSift.Domain.Results.ImportStatus.Canceled: 3 -> 42'
    original_425_entry_checker = 'expected_enum_regression_detected'
    compiled_metadata_comparison = $comparison.overall
    api_differences = $diffs
    matched_categories = @('assemblies', 'resources', 'packages', 'tests')
    missing_api_evidence = $missing.overall
    candidate_commit = 'ephemeral CI-only; never pushed to RecordSift'
    limitations = @(
        'A changed public enum value is a binary/serialized-integer contract regression, not a method removal.',
        'Passing tests and clean consumers do not prove numeric enum compatibility.',
        'NuGet package comparison covers logical metadata and file paths, not binary payload bytes.'
    )
}
$summary | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $evidence 'experiment-report.json') -Encoding utf8
Write-Host "PASS: EXP-016 two real compiled revisions and strict positive/negative gates; ephemeral SHA $candidateSha"
