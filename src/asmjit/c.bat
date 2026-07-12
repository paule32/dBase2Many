:: ----------------------------------------------------------------------------
:: file: compile.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
@echo off
set PATH=%CD%;%PATH%
set ANTLR_VERSION=4.13.2

echo create: Lexer + Parser

:: ----------------------------------------------------------------------------
:: Pascal
:: ----------------------------------------------------------------------------
antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/pascal     ^
    compiler/grammar/PascalLexer.g4

antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/pascal     ^
    -visitor              ^
    -lib parsers/pascal   ^
    compiler/grammar/PascalParser.g4

:: ----------------------------------------------------------------------------
:: ELAN / EUMEL
:: ----------------------------------------------------------------------------
antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/elan       ^
    compiler/grammar/ElanLexer.g4

antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/elan       ^
    -visitor              ^
    -lib parsers/elan     ^
    compiler/grammar/ElanParser.g4
