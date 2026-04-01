:: ---------------------------------------------------------------------------
:: File: parser_lisp.bat
:: Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
:: All rights reserved
:: ---------------------------------------------------------------------------
:: build LISP parser
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -o parse            lispLexer.g4
venv\Scripts\antlr4 -Dlanguage=Python3 -visitor -o parse -lib parse lispParser.g4
