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
:: goto test0
set "list=System.Types System.Objects"
set /a total=0
for %%A in (%list%) do ( set /a total += 1 )
set /a current=0
for %%A in (%list%) do (
    set /a current+=1
    set "lhs_pad=  !current!"
    set "rhs_pad=  !total!"
    echo compile [!lhs_pad:~-3! / !rhs_pad:~-2!]: runtime/pascal/System/%%A.pas
    python cpascal.py -Twin32 --backend obj --force --verbose -Us ^
        -Fo runtime/pascal/crypto/objects ^
        -Fo x32/pascal/System ^
        -Fo x32/pascal/Crypto -FE x32/pascal/System ^
        runtime/pascal/System/%%A.pas
    set "result=%errorlevel%"
    if !result! gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
)
echo.
:: goto test2
:test0
:: goto test2
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
        -Fo x32/pascal/System ^
        -Fo x32/pascal/Crypto ^
        -FE x32/pascal/tests/crypto testsrc/pascal/crypto/%%A.pas
    set "result=%errorlevel%"
    if %result% gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
)
echo.
:: ----------------------------------------------------------------------------
:test1
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
        -FE x32/pascal/tests/common/with_dll testsrc/pascal/common/test%%A.pas
    set "result=%errorlevel%"
    if %result% gtr 0 (
        echo Python Error Code: %result%
        goto error
    )
)
echo.
:: ----------------------------------------------------------------------------
:test2
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
    python cpascal.py -Twin32 --backend exe --force -Us ^
        -Fo x32/pascal/System       ^
        -Fo runtime/win32           ^
        -FE x32/pascal/tests/common/free_dll testsrc/pascal/common/%%A.pas
    set "result=%errorlevel%"
    if !result! gtr 1 (
        echo Python Error Code: %result%
        goto error
    )
)

goto ok

:done
goto ok

:error
echo Error occur.
exit /b %result%

:ok
echo Compile ok
exit /b
