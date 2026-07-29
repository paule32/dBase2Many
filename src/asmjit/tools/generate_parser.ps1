$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Jar = if ($env:ANTLR_JAR) {
    $env:ANTLR_JAR
} else {
    Join-Path $Root "tools\antlr-4.13.2-complete.jar"
}
$Out = Join-Path $Root "rccompiler\generated"

if (-not (Test-Path $Jar -PathType Leaf)) {
    throw "ANTLR jar not found: $Jar"
}

java -jar $Jar `
    -Dlanguage=Python3 `
    -Xexact-output-dir `
    -o $Out `
    (Join-Path $Root "grammar\ResourceLexer.g4")

java -jar $Jar `
    -Dlanguage=Python3 `
    -visitor `
    -no-listener `
    -Xexact-output-dir `
    -lib $Out `
    -o $Out `
    (Join-Path $Root "grammar\ResourceParser.g4")

Write-Host "Generated parser in $Out"
