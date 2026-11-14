# Optional operator-local experiment for legacy net48 packages.config solutions.
# Does not restore or download packages. Requires cached exact package versions.
# Execute from a clean, frozen RecordSift checkout in PowerShell 7 on Windows.
[CmdletBinding()]
param(
    [string]$SourceRoot = (Get-Location).Path,
    [string]$ReferenceAssembliesVersion = '1.0.3',
    [string]$Configuration = 'Release'
)
$ErrorActionPreference = 'Stop'
if (-not $IsWindows) { throw 'This procedure requires Windows to execute net48 NUnit tests.' }
$source = (Resolve-Path -LiteralPath $SourceRoot).Path
$solution = Join-Path $source 'RecordSift.sln'
if (-not (Test-Path -LiteralPath $solution -PathType Leaf)) { throw "Missing RecordSift.sln: $source" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required for checkout verification.' }
$before = @(& git -C $source status --porcelain=v1)
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect source Git status.' }
if ($before.Count -gt 0) { throw 'Source checkout must be clean before experiment; no cleanup is automatic.' }
$sha = (& git -C $source rev-parse HEAD).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Cannot resolve source SHA.' }
$workspace = Join-Path ([IO.Path]::GetTempPath()) ("RecordSift-sdk-only-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $workspace | Out-Null
$pkgRoot = Join-Path $workspace 'packages'
New-Item -ItemType Directory -Path $pkgRoot | Out-Null
foreach ($name in @('src','tests')) {
    Copy-Item -LiteralPath (Join-Path $source $name) -Destination $workspace -Recurse
}
Copy-Item -LiteralPath $solution -Destination $workspace
$pkgConfigs = @(Get-ChildItem -LiteralPath $workspace -Filter 'packages.config' -Recurse -File)
$specs = foreach ($cfg in $pkgConfigs) {
    [xml]$xml = Get-Content -LiteralPath $cfg.FullName -Raw
    foreach ($item in $xml.packages.package) {
        [pscustomobject]@{ Id = [string]$item.id; Version = [string]$item.version }
    }
}
$specs = @($specs | Sort-Object Id,Version -Unique)
foreach ($spec in $specs) {
    $from = Join-Path $HOME ('.nuget\packages\' + $spec.Id.ToLowerInvariant() + '\' + $spec.Version)
    $to = Join-Path $pkgRoot ($spec.Id + '.' + $spec.Version)
    if (-not (Test-Path -LiteralPath $from -PathType Container)) {
        throw "Missing cached package: $($spec.Id) $($spec.Version); no automatic restore performed."
    }
    Copy-Item -LiteralPath $from -Destination $to -Recurse
}
$refRoot = Join-Path $HOME ('.nuget\packages\microsoft.netframework.referenceassemblies.net48\' + $ReferenceAssembliesVersion + '\build')
if (-not (Test-Path -LiteralPath (Join-Path $refRoot '.NETFramework\v4.8\mscorlib.dll') -PathType Leaf)) {
    throw "Missing cached net48 reference assemblies $ReferenceAssembliesVersion under $refRoot"
}
$results = Join-Path $workspace 'TestResults'
New-Item -ItemType Directory -Path $results | Out-Null
$runner = Join-Path $pkgRoot 'NUnit.ConsoleRunner.3.17.0\tools\nunit3-console.exe'
if (-not (Test-Path -LiteralPath $runner -PathType Leaf)) { throw "Missing NUnit runner: $runner" }
$exit = 0
try {
    Push-Location -LiteralPath $workspace
    try {
        & dotnet msbuild (Join-Path $workspace 'RecordSift.sln') -target:Build "-property:Configuration=$Configuration" "-property:TargetFrameworkRootPath=$refRoot" -verbosity:minimal
        if ($LASTEXITCODE -ne 0) { throw "Solution build failed with exit code $LASTEXITCODE" }
        $names = @(
            'RecordSift.Domain.Tests',
            'RecordSift.Application.Tests',
            'RecordSift.Infrastructure.Csv.Tests',
            'RecordSift.Infrastructure.Reporting.Tests',
            'RecordSift.Infrastructure.Xlsx.Tests'
        )
        foreach ($name in $names) {
            $dll = Join-Path $workspace ("tests\$name\bin\$Configuration\$name.dll")
            if (-not (Test-Path -LiteralPath $dll -PathType Leaf)) { throw "Missing compiled test assembly $dll" }
            $xml = Join-Path $results "$name.xml"
            & $runner $dll "--work=$results" "--result=$xml;format=nunit3" --noheader
            if ($LASTEXITCODE -ne 0) { throw "NUnit suite $name failed with exit code $LASTEXITCODE" }
        }
    }
    finally { Pop-Location }
}
finally {
    $after = @(& git -C $source status --porcelain=v1)
    if ($LASTEXITCODE -ne 0) { Write-Warning 'Could not inspect source checkout status after experiment.' }
    elseif ($after.Count -gt 0) { Write-Warning "Source checkout has changes after experiment: $($after -join ', ')" }
    Write-Host "Source revision: $sha"
    Write-Host "Isolated workspace and XML results: $workspace"
    Write-Host 'The experiment workspace is retained for inspection; cleanup is manual.'
}
