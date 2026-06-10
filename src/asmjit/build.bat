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
set ANTLR_VERSION=4.13.2

echo create: Lexer + Parser

antlr4 -v %ANTLR_VERSION% -Dlanguage=Python3 -o parsers/pascal grammar/MiniPascalLexer.g4
antlr4 -v %ANTLR_VERSION% -Dlanguage=Python3 -o parsers/pascal -visitor -lib parsers/pascal grammar/MiniPascalParser.g4

:: rm -rf testout
rm debug.log

if not exist testout ( mkdir testout )
python pas2asmjit.py testsrc/test1.pas 1> testout/test1.cc 2>> debug.log
::g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -m64 -mconsole -O2 -L. -o testout/test1.exe testout/test1.cc -lasmjit

echo create: Python + Exe files ...
python -m compileall pas2asmjit.py

::for /L %%N in (2,1,48) do (
for %%N in (48) do (
    echo create: test%%N.exe
    python pas2asmjit.py testsrc/test%%N.pas 1> testout/test%%N.cc 2>> debug.log
    g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -I. -m64 -mconsole -O2 ^
        -LT:/GitHub/asmjit/build-dll -Lruntime ^
        -o  testout/test%%N.exe testout/test%%N.cc -ldbase2many.dll -lasmjit
    strip   testout/test%%N.exe
)
echo create: batch files
for /L %%N in (2,1,48) do (
    echo ^:^: ------------------------------------------------------------ > testout/run_test%%N.bat
    echo ^:^: Copyright ^(c^) 2026 by Jens Kallup - paule32 >> testout/run_test%%N.bat
    echo ^:^: all rights reserved. >testout/run_test%%N.bat >> testout/run_test%%N.bat
    echo ^:^: ------------------------------------------------------------ >> testout/run_test%%N.bat
    echo @echo off >> testout/run_test%%N.bat
    echo set PATH=%CD%;T:\msys64\mingw64\bin;T:\GitHub\asmjit\build-dll;..\runtime;%PATH% >> testout/run_test%%N.bat
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
