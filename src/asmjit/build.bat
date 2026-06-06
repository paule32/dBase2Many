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

echo create Lexer + Parser

@antlr4 -Dlanguage=Python3 -o parsers/pascal grammar/MiniPascalLexer.g4
@antlr4 -Dlanguage=Python3 -o parsers/pascal -visitor -lib parsers/pascal grammar/MiniPascalParser.g4

:: rm -rf testout
rm debug.log

if not exist testout ( mkdir testout )
python pas2asmjit.py testsrc/test1.pas 1> testout/test1.cc 2>> debug.log
::g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -m64 -mconsole -O2 -L. -o testout/test1.exe testout/test1.cc -lasmjit

echo create Python + Exe files ...
python -m compileall pas2asmjit.py

::for %%N in (2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21) do (
for %%N in (21) do (
    echo create: test%%N
    python pas2asmjit.py testsrc/test%%N.pas 1> testout/test%%N.cc 2>> debug.log
    g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -I. -m64 -mconsole -O2 -L. -Lruntime ^
        -o  testout/test%%N.exe testout/test%%N.cc runtime/obj/*.o -lasmjit
    strip   testout/test%%N.exe
    echo @echo off > testout/run_test%%N.bat
    echo set PATH=T:\msys64\mingw64\bin;%CD%;%PATH% >> testout/run_test%%N.bat
    echo test%%N.exe >> testout/run_test%%N.bat
    echo nasm -fwin64 -o test%%N.o test%%N.asm >> testout/run_test%%N.bat
)
goto ok

:error
echo Error occur.
type debug.log
goto done

:ok
echo Compile ok
:done
