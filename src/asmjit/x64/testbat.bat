@echo off

testnt35.exe

if errorlevel 100 goto err100
if errorlevel  99 goto err99
if errorlevel   5 goto err5
if errorlevel   1 goto err1
if errorlevel   0 goto noerror

echo query end
goto noerror

:err100
echo Error is 100
goto error

:err99
echo Error is 99
goto error

:err5
echo Error is 5
goto error

:err1
echo Error is 1
goto error

:noerror
echo test success, no error
goto ok

:error
echo test fail
goto ok

:ok
