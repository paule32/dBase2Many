:: ---------------------------------------------------------------------------
:: File: parser_cc.bat
:: Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
:: All rights reserved
:: ---------------------------------------------------------------------------
:: build C/C++ parser
venv\Scripts\antlr4 -Dlanguage=Python3                            -o parse/pascal gramm/pascal/pascalLexer.g4
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -lib parse/pascal -o parse/pascal gramm/pascal/pascalParser.g4
