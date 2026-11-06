# Windows PowerShell 5.1 child host: loads real net48 candidate in .NET Framework CLR.
# Private stdout is parsed only by the research parent; no file paths published.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$AssemblyPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$stage = 'ASSEMBLY_LOAD'

try {
    $loaded = [System.Reflection.Assembly]::LoadFrom($AssemblyPath)
    $stage = 'TYPE_LOOKUP'
    $probe = $loaded.GetType('D2a.Fixture.Probe', $true)
    $method = $probe.GetMethod('Identity')
    if ($null -eq $method) { throw 'D2A_METHOD_MISSING' }

    $stage = 'METHOD_INVOKE'
    $value = [int]$method.Invoke($null, [object[]]@())
    $stage = 'ASSEMBLY_LOCATION'
    $location = [IO.Path]::GetFullPath($loaded.Location)
    $stage = 'SHA256_READ'
    $hash = (Get-FileHash -LiteralPath $location -Algorithm SHA256).Hash.ToLowerInvariant()

    $stage = 'REPORT_JSON'
    [pscustomobject]@{
        loaded_location = $location
        loaded_sha256 = $hash
        method_value = $value
    } | ConvertTo-Json -Compress
}
catch {
    # Fixed category ONLY: no internal paths, exception payload or stack trace.
    [Console]::Error.WriteLine("D2A_CLR_STAGE_" + $stage + "_FAILED")
    exit 2
}
