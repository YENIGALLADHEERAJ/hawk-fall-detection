param([Parameter(Mandatory=$true)][string]$Video, [string]$Output = 'data/debug-run')
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    & '.venv/Scripts/python.exe' -m vision.run $Video --output $Output --view
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally { Pop-Location }
