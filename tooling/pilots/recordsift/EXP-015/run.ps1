# EXP-015 — independent builds of baseline and a disposable LangVersion candidate.
# The candidate commit is local to CI. Never push to RecordSift or publish packages.
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$ApplicationRoot,
    [Parameter(Mandatory = $true)][string]$EvidenceRoot
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$baselineSha = '8358780829458854a4b0356df5ac5e685f0a34c8'
$candidate = (Resolve-Path -LiteralPath $ApplicationRoot).Path
$evidence = [IO.Path]::GetFullPath($EvidenceRoot)
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
if ($evidence.StartsWith($candidate + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Evidence must remain outside RecordSift.'
}
$initial = (& git -C $candidate rev-parse --verify HEAD).Trim()
if ($LASTEXITCODE -ne 0 -or $initial -cne $baselineSha) { throw "Unexpected RecordSift SHA $initial" }
$dirty = @(& git -C $candidate status --porcelain --untracked-files=normal)
if ($LASTEXITCODE -ne 0 -or $dirty.Count -ne 0) { throw 'Initial candidate checkout is dirty.' }
if (Test-Path -LiteralPath $evidence) { throw 'Evidence root must not preexist.' }
New-Item -ItemType Directory -Path $evidence | Out-Null
$baseline = Join-Path $evidence 'baseline-checkout'
& git -C $candidate worktree add --detach $baseline $baselineSha
if ($LASTEXITCODE -ne 0) { throw 'Independent frozen worktree creation failed.' }

$projects = @(Get-ChildItem (Join-Path $candidate 'src') -Filter '*.csproj' -File -Recurse) +
            @(Get-ChildItem (Join-Path $candidate 'tests') -Filter '*.csproj' -File -Recurse)
if ($projects.Count -ne 10) { throw "Expected exactly 10 csproj files, found $($projects.Count)" }
$utf8NoBom = [Text.UTF8Encoding]::new($false)
foreach ($project in $projects) {
    $before = [IO.File]::ReadAllText($project.FullName)
    if ([regex]::Matches($before, '<LangVersion>7\.3</LangVersion>').Count -ne 1) {
        throw "Expected exactly one identical LangVersion in $($project.FullName)"
    }
    $after = $before.Replace('<LangVersion>7.3</LangVersion>', '')
    [IO.File]::WriteAllText($project.FullName, $after, $utf8NoBom)
}
$propsPath = Join-Path $candidate 'Directory.Build.props'
if (Test-Path -LiteralPath $propsPath) { throw 'Candidate already contains Directory.Build.props.' }
$props = @'
<Project>
  <PropertyGroup>
    <LangVersion Condition="'$(LangVersion)' == ''">7.3</LangVersion>
  </PropertyGroup>
</Project>
'@
[IO.File]::WriteAllText($propsPath, $props + [Environment]::NewLine, $utf8NoBom)
& git -C $candidate add -- Directory.Build.props src tests
if ($LASTEXITCODE -ne 0) { throw 'Could not stage candidate changes.' }
& git -C $candidate -c 'user.name=Modernization research' -c 'user.email=research@example.invalid' commit -m 'EXP-015 disposable LangVersion candidate'
if ($LASTEXITCODE -ne 0) { throw 'Could not create ephemeral candidate commit.' }
$candidateSha = (& git -C $candidate rev-parse HEAD).Trim()
$changed = @(& git -C $candidate diff --name-only $baselineSha $candidateSha)
$expectedPaths = @('Directory.Build.props') + @($projects | ForEach-Object {
    [IO.Path]::GetRelativePath($candidate, $_.FullName).Replace('\', '/')
})
if ($changed.Count -ne 11 -or (Compare-Object ($changed | Sort-Object) ($expectedPaths | Sort-Object))) {
    throw "Unexpected change scope: $($changed -join ', ')"
}
$patch = @(& git -C $candidate diff --no-ext-diff $baselineSha $candidateSha -- Directory.Build.props src tests)
if ($LASTEXITCODE -ne 0) { throw 'Could not retain candidate patch.' }
$patch | Set-Content (Join-Path $evidence 'candidate.patch') -Encoding utf8
if (@(& git -C $candidate status --porcelain --untracked-files=normal).Count -ne 0) {
    throw 'Committed candidate is not clean.'
}
$vswhere = Join-Path ([Environment]::GetFolderPath('ProgramFilesX86')) 'Microsoft Visual Studio\Installer\vswhere.exe'
$msbuild = & $vswhere -latest -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe' | Select-Object -First 1
if (-not $msbuild) { throw 'Visual Studio MSBuild was not installed.' }
$hostReport = [ordered]@{
    windows = [Environment]::OSVersion.VersionString
    dotnet_sdk = (& dotnet --version).Trim()
    msbuild_path = $msbuild
    msbuild_version = ((& $msbuild -version -nologo) | Select-Object -Last 1).Trim()
    pwsh_version = $PSVersionTable.PSVersion.ToString()
}
$hostReport | ConvertTo-Json | Set-Content (Join-Path $evidence 'toolchain.json') -Encoding utf8
$propertyRows = @()
$pilot = Join-Path $repoRoot 'tooling/pilots/recordsift/EXP-014/run.ps1'
foreach ($side in @(
    [pscustomobject]@{ Name = 'baseline'; Root = $baseline; Sha = $baselineSha },
    [pscustomobject]@{ Name = 'candidate'; Root = $candidate; Sha = $candidateSha }
)) {
    $sourceSha = (& git -C $side.Root rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or $sourceSha -cne $side.Sha) { throw "Wrong $($side.Name) SHA" }
    foreach ($project in $projects) {
        $relative = [IO.Path]::GetRelativePath($candidate, $project.FullName)
        foreach ($configuration in @('Debug', 'Release')) {
            $projectPath = Join-Path $side.Root $relative
            $effective = (& $msbuild $projectPath '-getProperty:LangVersion' "/p:Configuration=$configuration" '/p:Platform=AnyCPU' -nologo).Trim()
            if ($LASTEXITCODE -ne 0 -or $effective -cne '7.3') {
                throw "$($side.Name) $configuration LangVersion mismatch for $relative : $effective"
            }
            $propertyRows += [ordered]@{ side=$side.Name; project=$relative; configuration=$configuration; langversion=$effective }
        }
    }
    Push-Location $side.Root
    try {
        & nuget restore RecordSift.sln -NonInteractive -PackagesDirectory packages -ConfigFile NuGet.Config
        if ($LASTEXITCODE -ne 0) { throw "$($side.Name) restore failed." }
        & $msbuild RecordSift.sln /m /t:Rebuild /p:Configuration=Release '/p:Platform=Any CPU' /verbosity:minimal
        if ($LASTEXITCODE -ne 0) { throw "$($side.Name) rebuild failed." }
    }
    finally { Pop-Location }
    & $pilot -ApplicationRoot $side.Root -EvidenceRoot (Join-Path $evidence "$($side.Name)-evidence") -ExpectedCommit $side.Sha -ExperimentId "EXP-015-$($side.Name)"
    if ($LASTEXITCODE -ne 0) { throw "$($side.Name) original acceptance gates failed." }
}
$propertyRows | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $evidence 'property-matrix.json') -Encoding utf8
$comparisonFile = Join-Path $evidence 'baseline-versus-candidate.json'
& python (Join-Path $repoRoot 'tooling/validators/compatibility.py') compare --baseline (Join-Path $evidence 'baseline-evidence/baseline.json') --candidate (Join-Path $evidence 'candidate-evidence/baseline.json') --output $comparisonFile
$exit = $LASTEXITCODE
$comparison = Get-Content -LiteralPath $comparisonFile -Raw | ConvertFrom-Json
$report = [ordered]@{
    experiment = 'EXP-015'
    baseline_source_sha = $baselineSha
    ephemeral_candidate_sha = $candidateSha
    candidate_push = 'none; ephemeral commit only'
    changed_files = @($changed)
    comparison_result = $comparison.overall
    comparison_exit = $exit
    comparison_components = $comparison.components
    gates = 'Independent Release rebuilds, 40 evaluated Debug/Release property cells, 425-entry original API check, five XML documentation checks, 419 NUnit tests per checkout, package and clean consumer per checkout, and compiled assembly metadata.'
    scope_limitations = @('Debug property values checked but Debug binaries not built.', 'Native, COM, assembly binding and all external consumers not proved.', 'Candidate SHA is CI-local; replay from retained patch and source transformation.')
}
$report | ConvertTo-Json -Depth 12 | Set-Content (Join-Path $evidence 'candidate-report.json') -Encoding utf8
if ($exit -ne 0 -or $comparison.overall -cne 'matched') {
    throw "Independent candidate compatibility check did not match: $($comparison.overall)"
}
Write-Host "PASS: EXP-015 frozen $baselineSha vs disposable $candidateSha — selected contracts match."
