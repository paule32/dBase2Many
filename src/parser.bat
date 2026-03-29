:: ---------------------------------------------------------------------------
:: File:   parser.bat
:: Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
:: All rights reserved
:: ---------------------------------------------------------------------------
:: build dBase parser
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -o gen          dBaseLexer.g4
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -o gen -lib gen dBaseParser.g4
