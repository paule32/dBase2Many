:: ---------------------------------------------------------------------------
:: File: parser_cc.bat
:: Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
:: All rights reserved
:: ---------------------------------------------------------------------------
:: build C/C++ parser
venv\Scripts\antlr4 -Dlanguage=Python3                        -o parse/cc gramm/cc/ccLexer.g4
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -lib parse/cc -o parse/cc gramm/cc/ccParser.g4

venv\Scripts\antlr4 -Dlanguage=Python3                        -o parse/cc gramm/cc/CppDocLexer.g4
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -lib parse/cc -o parse/cc gramm/cc/CppDocParser.g4
