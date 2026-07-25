:: ----------------------------------------------------------------------------
:: file: compile.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
@echo off
set PATH=%CD%;%PATH%
set ANTLR_VERSION=4.13.2

:: ----------------------------------------------------------------------------
:: Windows Resource Compiler ...
:: ----------------------------------------------------------------------------
echo create: Lexer + Parser for Windows Resource Compiler
antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/resource   ^
    compiler/grammar/ResourceLexer.g4

antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/resource   ^
    -visitor              ^
    -lib parsers/resource ^
    compiler/grammar/ResourceParser.g4

:: ----------------------------------------------------------------------------
:: Pascal
:: ----------------------------------------------------------------------------
echo create: Lexer + Parser for Pascal
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
echo create: Lexer + Parser for ELAN/EUMEL
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

:: ----------------------------------------------------------------------------
:: LISP
:: ----------------------------------------------------------------------------
echo create: Lexer + Parser for LISP
antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/lisp       ^
    compiler/grammar/LispLexer.g4

antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/lisp       ^
    -visitor              ^
    -lib parsers/lisp     ^
    compiler/grammar/LispParser.g4

:: ----------------------------------------------------------------------------
:: BASIC
:: ----------------------------------------------------------------------------
echo create: Lexer + Parser for BASIC
antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/basic      ^
    compiler/grammar/BasicLexer.g4

antlr4 -v %ANTLR_VERSION% ^
    -Dlanguage=Python3    ^
    -o parsers/basic      ^
    -visitor              ^
    -lib parsers/basic    ^
    compiler/grammar/BasicParser.g4
