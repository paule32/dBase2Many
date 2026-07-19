:: ----------------------------------------------------------------------------
:: file: build.bat
:: author: (c) 2026 Jens Kallup - paule32
:: all rights reserved.
:: ----------------------------------------------------------------------------
@echo off   
setlocal EnableDelayedExpansion

python -m compileall cpascal.py
set "compiler=python cpascal.py"

:: ----------------------------------------------------------------------------
:: compile Pascal system files ...
:: ----------------------------------------------------------------------------
echo stage:  [  1 /  4] - System
set "list=System.Types System.Objects"
set /a total=0
for %%A in (%list%) do ( set /a total += 1 )
set /a current=0
for %%A in (%list%) do (
    set /a current+=1
    set "lhs_pad=  !current!"
    set "rhs_pad=  !total!"
    echo compile [!lhs_pad:~-3! / !rhs_pad:~-2!]: runtime/pascal/System/.%%A.pas
)
echo.
:: ----------------------------------------------------------------------------
:: compile crypto files ...
:: ----------------------------------------------------------------------------
echo stage:  [  2 /  4] - Crypto package
set "list=crc16 crc32 crc32c crc64 md5 sha1 sha3 sha224 sha256 sha384 sha512"
set /a total=0
for %%A in (%list%) do ( set /a total += 1 )
set /a current=0
for %%A in (%list%) do (
    set /a current+=1
    set "lhs_pad=  !current!"
    set "rhs_pad=  !total!"
    echo compile [!lhs_pad:~-3! / !rhs_pad:~-2!]: runtime/pascal/Crypto/Crypto.%%A.pas
    python cpascal.py -Twin32 --backend obj --force --verbose ^
        -Fo runtime/pascal/crypto/objects ^
        -Fo x32/pascal/System ^
        -Fo x32/pascal/Crypto -FE x32/pascal/Crypto ^
        runtime/pascal/Crypto/Crypto.%%A.pas
    set "result=%errorlevel%"
    if !result! gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
)
echo.
:: ----------------------------------------------------------------------------
:: test applications ...
:: ----------------------------------------------------------------------------
echo stage:  [  3 /  4] - Test Application's with external DLL
set "list=crc16 crc32 crc32c crc64 md5 sha1 sha3 sha224 sha256 sha384 sha512"
set /a total=0
for %%A in (%list%) do ( set /a total += 1 )
set /a current=0
for %%A in (%list%) do (
    set /a current+=1
    set "lhs_pad=  !current!"
    set "rhs_pad=  !total!"
    echo compile [!lhs_pad:~-3! / !rhs_pad:~-2!]: testsrc/pascal/crypto/%%A.pas
    python cpascal.py -Twin32 --backend exe --force --verbose ^
        -Fo runtime/pascal/crypto/objects ^
        -Fo x32/pascal/System ^
        -Fo x32/pascal/Crypto ^
        -FE x32/pascal/tests/crypto testsrc/pascal/crypto/%%A.pas
    set "result=%errorlevel%"
    if %result% gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
    call :writeRun x32/pascal/tests/crypto/%%A.bat %%A.exe
)
echo.
:: ----------------------------------------------------------------------------
set /a total   = 54
set /a current = 0
for /L %%A in (2,1,%total%) do (
    set /a current+=1
    set "lhs_pad=  !current!"
    set "rhs_pad=  !total!"
    echo compile [!lhs_pad:~-3! / !rhs_pad:~-2!]: testsrc/pascal/common/test%%A.pas
    python cpascal.py -Twin32 --backend exe --force --verbose ^
        -Fo x32/pascal/System ^
        -Fo x32/pascal/Crypto ^
        -FE x32/pascal/tests/common testsrc/pascal/common/test%%A.pas
    set "result=%errorlevel%"
    if %result% gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
    call :writeRun x32/pascal/tests/common/test%%A.bat test%%A.exe
)
echo.
:: ----------------------------------------------------------------------------
echo stage:  [  4 /  4] - Test Application's without external DLL / packed
set "list=testvmt"
set /a total=0
for %%A in (%list%) do ( set /a total += 1 )
set /a current=0
for %%A in (%list%) do (
    set /a current+=1
    set "lhs_pad=  !current!"
    set "rhs_pad=  !total!"
    echo compile [!lhs_pad:~-3! / !rhs_pad:~-2!]: testsrc/pascal/common/%%A.pas
    python cpascal.py -Twin32 --backend exe --force --verbose -Us ^
        -Fo runtime/pascal/crypto/objects ^
        -Fo x32/pascal/System       ^
        -Fo x32/pascal/Crypto       ^
        -Fo testsrc/pascal/objects  ^
        -FE x32/pascal/tests/common testsrc/pascal/common/%%A.pas
    set "result=%errorlevel%"
    if %result% gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
)

goto ok

:: ----------------------------------------------------------------------------
:: goto label as alternative for a sub routine call - write runner batch file
:: call :writeRun <output-file> <exe-file>
:: ----------------------------------------------------------------------------
:writeRun
echo ^:^: ------------------------------------------------------------>%1
echo ^:^: Copyright ^(c^) 2026 by Jens Kallup - paule32>>%1
echo ^:^: all rights reserved.>>%1
echo ^:^: ------------------------------------------------------------>>%1
echo @echo off>>%1
echo set PATH=%CD%\x32;%PATH%>>%1
echo %2>>%1
exit /b 

:done
echo done.
exit 0

--backend exe testsrc/testcrc16.pas
python cpascal.py -Twinnt --backend exe testsrc/testcrc32.pas
python cpascal.py -Twinnt --backend exe testsrc/testcrc32c.pas
python cpascal.py -Twinnt --backend exe testsrc/testcrc64.pas
python cpascal.py -Twinnt --backend exe testsrc/testmd5.pas
python cpascal.py -Twinnt --backend exe testsrc/testsha1.pas
python cpascal.py -Twinnt --backend exe testsrc/testsha3.pas
python cpascal.py -Twinnt --backend exe testsrc/testsha224.pas
python cpascal.py -Twinnt --backend exe testsrc/testsha256.pas
python cpascal.py -Twinnt --backend exe testsrc/testsha384.pas
python cpascal.py -Twinnt --backend exe testsrc/testsha512.pas

python pas2asmjit.py -Twinnt --backend exe testsrc/testdisk.pas

:: ----------------------------------------------------------------------------
exit 0

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
exit /b %result%

:ok
echo Compile ok
:done
exit /b 0
