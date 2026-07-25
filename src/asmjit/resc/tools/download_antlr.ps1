$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Target = Join-Path $Root "tools\antlr-4.13.2-complete.jar"
Invoke-WebRequest `
    -Uri "https://www.antlr.org/download/antlr-4.13.2-complete.jar" `
    -OutFile $Target
Write-Host "Downloaded: $Target"
