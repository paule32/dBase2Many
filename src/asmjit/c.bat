:: ----------------------------------------------------------------------------
:: file: compile.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
@echo off
set PATH=%CD%;%PATH%
set ANTLR_VERSION=4.13.2

echo create: Lexer + Parser

antlr4 -v %ANTLR_VERSION% -Dlanguage=Python3 -o parsers/pascal grammar/MiniPascalLexer.g4
antlr4 -v %ANTLR_VERSION% -Dlanguage=Python3 -o parsers/pascal -visitor -lib parsers/pascal grammar/MiniPascalParser.g4
