$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    $env:PYTHONPATH = $Root
    python -m unittest discover -s tests -v
} finally {
    Pop-Location
}
