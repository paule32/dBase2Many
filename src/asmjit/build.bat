:: ----------------------------------------------------------------------------
:: file: build.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
@echo off
:: first, set the current working directory, if you want to execute the created
:: example Windows files (external). So the executables can find the libasmjit
:: library file (libasmjit.dll)
:: ----------------------------------------------------------------------------
set PATH=%CD%;%PATH%

antlr4 -Dlanguage=Python3                              -o parsers/pascal grammar/MiniPascalLexer.g4
antlr4 -Dlanguage=Python3 -visitor -lib parsers/pascal -o parsers/pascal grammar/MiniPascalParser.g4

rm -rf testout
rm debug.log

mkdir testout
python pas2asmjit.py testsrc/test1.pas 1> testout/test1.cc 2>> debug.log
python pas2asmjit.py testsrc/test2.pas 1> testout/test2.cc 2>> debug.log

g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -m64 -mconsole -O2 -L. -o testout/test1.exe testout/test1.cc -lasmjit
g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -m64 -mconsole -O2 -L. -o testout/test2.exe testout/test2.cc -lasmjit

::strip testout/test2.exe
goto ok

:error
echo Error occur.
type debug.log
goto done

:ok
echo Compile ok
:done
