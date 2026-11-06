# Dedicated child host: Windows PowerShell 5.1 uses the .NET Framework CLR.
# This script returns only to a PRIVATE parent process; it is never logged/uploaded.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$AssemblyPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$loaded = [System.Reflection.Assembly]::LoadFrom($AssemblyPath)
$probe = $loaded.GetType('D2a.Fixture.Probe', $true)
$method = $probe.GetMethod('Identity', [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::Static)
if ($null -eq $method) { throw 'D2A_METHOD_MISSING' }
$value = [int]$method.Invoke($null, @())
$location = [IO.Path]::GetFullPath($loaded.Location)
$hash = (Get-FileHash -LiteralPath $location -Algorithm SHA256).Hash.ToLowerInvariant()

[pscustomobject]@{
    loaded_location = $location
    loaded_sha256 = $hash
    method_value = $value
} | ConvertTo-Json -Compress
