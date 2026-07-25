$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Root
try {
    $env:PYTHONPATH = $Root
    python -m rccompiler `
        examples\app.rc `
        -o examples\app.res.o `
        -I examples `
        --dump-preprocessed examples\app.preprocessed.rc `
        --dump-records examples\app.records.json `
        -v
} finally {
    Pop-Location
}
