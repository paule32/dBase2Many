:: ----------------------------------------------------------------------------
:: file: build.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
@echo off
python -m compileall pas2asmjit.py
::python pas2asmjit.py -Twinnt --backend exe testsrc/testnt35.pas

:: ----------------------------------------------------------------------------
:: hash algos
:: ----------------------------------------------------------------------------
python pas2asmjit.py -Twinnt --backend exe testsrc/testcrc16.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testcrc32.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testcrc32c.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testcrc64.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testmd5.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testsha1.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testsha3.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testsha224.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testsha256.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testsha384.pas
python pas2asmjit.py -Twinnt --backend exe testsrc/testsha512.pas

python pas2asmjit.py -Twinnt --backend exe testsrc/testdisk.pas

echo @echo off> x32/testcrc16.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testcrc16.bat
echo testcrc16.exe>> x32/testcrc16.bat

echo @echo off> x32/testcrc32.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testcrc32.bat
echo testcrc32.exe>> x32/testcrc32.bat

echo @echo off> x32/testcrc32c.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testcrc32c.bat
echo testcrc32c.exe>> x32/testcrc32c.bat

echo @echo off> x32/testcrc64.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testcrc64.bat
echo testcrc64.exe>> x32/testcrc64.bat

echo @echo off> x32/testmd5.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testmd5.bat
echo testmd5.exe>> x32/testmd5.bat

echo @echo off> x32/testsha1.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testsha1.bat
echo testsha1.exe>> x32/testsha1.bat

echo @echo off> x32/testsha3.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testsha3.bat
echo testsha3.exe>> x32/testsha3.bat

echo @echo off> x32/testsha224.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testsha224.bat
echo testsha224.exe>> x32/testsha224.bat

echo @echo off> x32/testsha256.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testsha256.bat
echo testsha256.exe>> x32/testsha256.bat

echo @echo off> x32/testsha384.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testsha384.bat
echo testsha384.exe>> x32/testsha384.bat

echo @echo off> x32/testsha512.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testsha512.bat
echo testsha512.exe>> x32/testsha512.bat


echo @echo off> x32/testdisk.bat
echo set PATH=%CD%;..\runtime\win32;S:\msys64\mingw64\bin;S:\GitHub\asmjit\build-dll;..\runtime;%PATH%>> x32/testdisk.bat
echo testdisk.exe>> x32/testdisk.bat

:: ----------------------------------------------------------------------------
exit 0
:: ----------------------------------------------------------------------------
:: first, set the current working directory, if you want to execute the created
:: example Windows files (external). So the executables can find the libasmjit
:: library file (libasmjit.dll)
:: ----------------------------------------------------------------------------
set PATH=%CD%;%PATH%
set ANTLR_VERSION=4.13.2

echo create: Lexer + Parser

::antlr4 -v %ANTLR_VERSION% -Dlanguage=Python3 -o parsers/pascal grammar/MiniPascalLexer.g4
::antlr4 -v %ANTLR_VERSION% -Dlanguage=Python3 -o parsers/pascal -visitor -lib parsers/pascal grammar/MiniPascalParser.g4

:: rm -rf testout
rm debug.log

if not exist testout ( mkdir testout )
python pas2asmjit.py testsrc/test1.pas 1> testout/test1.cc 2>> debug.log
::g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -m64 -mconsole -O2 -L. -o testout/test1.exe testout/test1.cc -lasmjit

echo create: Python + Exe files ...
python -m compileall pas2asmjit.py

::for /L %%N in (2,1,50) do (
for %%N in (56) do (
    echo create: test%%N.exe
    python pas2asmjit.py --backend nasm testsrc/test%%N.pas 1> testout/test%%N.cc 2>> debug.log
    echo done
)
    ::g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -I. -m64 -mconsole -O2 ^
    ::    -LT:/GitHub/asmjit/build-dll -Lruntime ^
    ::    -o  testout/test%%N.exe testout/test%%N.cc -ldbase2many.dll -lasmjit
    ::strip   testout/test%%N.exe
goto ok
echo create: batch files
for /L %%N in (2,1,54) do (
    echo ^:^: ------------------------------------------------------------ > testout/run_test%%N.bat
    echo ^:^: Copyright ^(c^) 2026 by Jens Kallup - paule32 >> testout/run_test%%N.bat
    echo ^:^: all rights reserved. >testout/run_test%%N.bat >> testout/run_test%%N.bat
    echo ^:^: ------------------------------------------------------------ >> testout/run_test%%N.bat
    echo @echo off >> testout/run_test%%N.bat
    echo set PATH=%CD%;T:\msys64\mingw64\bin;T:\GitHub\asmjit\build-dll;..\runtime;%PATH% >> testout/run_test%%N.bat
    echo test%%N.exe >> testout/run_test%%N.bat
    echo nasm -fwin64 -o test%%N.o test%%N.asm >> testout/run_test%%N.bat
    
    echo ^:^: ------------------------------------------------------------ > testout/run_test%%Na.bat
    echo ^:^: Copyright ^(c^) 2026 by Jens Kallup - paule32 >> testout/run_test%%Na.bat
    echo ^:^: all rights reserved. >testout/run_test%%N.bat >> testout/run_test%%Na.bat
    echo ^:^: ------------------------------------------------------------ >> testout/run_test%%Na.bat
    echo @echo off >> testout/run_test%%Na.bat
    echo set PATH=%CD%;T:\msys64\mingw64\bin;T:\GitHub\asmjit\build-dll;..\runtime;%PATH% >> testout/run_test%%Na.bat
    echo.>> testout/run_test%%Na.bat
    echo g++ -IT:/GitHub/asmjit -DASMJIT_STATIC=OFF -I. -m64 -mconsole -O2 -L../runtime ^^>> testout/run_test%%Na.bat
    echo     -nostartfiles ^^>> testout/run_test%%Na.bat
    echo     -o test%%Na.exe test%%N.o -ldbase2many.dll -lkernel32 ^^>> testout/run_test%%Na.bat
    echo     -Wl,-e,_main>> testout/run_test%%Na.bat
    echo.>> testout/run_test%%Na.bat
    echo echo final exe:>> testout/run_test%%Na.bat
    echo strip test%%Na.exe>> testout/run_test%%Na.bat
    echo test%%Na.exe>> testout/run_test%%Na.bat
)
goto ok

:error
echo Error occur.
type debug.log
goto done

:ok
echo Compile ok
:done
