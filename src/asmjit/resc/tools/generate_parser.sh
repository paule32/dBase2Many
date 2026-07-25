#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JAR="${ANTLR_JAR:-$ROOT/tools/antlr-4.13.2-complete.jar}"
OUT="$ROOT/rccompiler/generated"

if [[ ! -f "$JAR" ]]; then
    echo "ANTLR jar not found: $JAR" >&2
    echo "Download antlr-4.13.2-complete.jar from https://www.antlr.org/download" >&2
    exit 1
fi

rm -f "$OUT"/ResourceLexer.py "$OUT"/ResourceLexer.tokens "$OUT"/ResourceLexer.interp
rm -f "$OUT"/ResourceParser.py "$OUT"/ResourceParserVisitor.py
rm -f "$OUT"/ResourceParser.tokens "$OUT"/ResourceParser.interp

java -jar "$JAR" \
    -Dlanguage=Python3 \
    -Xexact-output-dir \
    -o "$OUT" \
    "$ROOT/grammar/ResourceLexer.g4"

java -jar "$JAR" \
    -Dlanguage=Python3 \
    -visitor \
    -no-listener \
    -Xexact-output-dir \
    -lib "$OUT" \
    -o "$OUT" \
    "$ROOT/grammar/ResourceParser.g4"

echo "Generated parser in $OUT"
