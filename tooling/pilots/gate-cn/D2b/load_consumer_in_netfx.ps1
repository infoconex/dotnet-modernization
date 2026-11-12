# .NET Framework 4.8 host: invoke real SDK-style NuGet consumer's method,
# then report the assembly dependency ACTUALLY loaded, not expected path.
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$ConsumerPath)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$stage = 'CONSUMER_LOAD'
try {
    $consumer = [Reflection.Assembly]::LoadFrom($ConsumerPath)
    $stage = 'CONSUMER_METHOD'
    $type = $consumer.GetType('D2b.Consumer.CallPath', $true)
    $method = $type.GetMethod('Run')
    if ($null -eq $method) { throw 'D2B_METHOD_MISSING' }
    $result = [int]$method.Invoke($null, [object[]]@())
    $stage = 'DEPENDENCY_LOOKUP'
    $matches = @([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object {
        $_.GetName().Name -ceq 'D2a.Probe'
    })
    if ($matches.Count -ne 1) { throw 'D2B_LOADED_CANDIDATE_UNIQUE_MISSING' }
    $loaded = $matches[0]
    $stage = 'MODULE_IDENTITY'
    $location = [IO.Path]::GetFullPath($loaded.Location)
    $mvid = $loaded.ManifestModule.ModuleVersionId.ToString('D')
    $stage = 'JSON'
    [pscustomobject]@{
        loaded_location = $location
        module_mvid = $mvid
        method_value = $result
    } | ConvertTo-Json -Compress
}
catch {
    [Console]::Error.WriteLine('D2B_CLR_STAGE_' + $stage + '_FAILED')
    exit 2
}
