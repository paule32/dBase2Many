:: ---------------------------------------------------------------
:: \file install.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
setlocal EnableDelayedExpansion
:: ---------------------------------------------------------------
echo %PATH%
set "STARTDIR=%CD%"

echo [1 / 7] create virtual environment
python.exe -m venv venv

:: ---------------------------------------------------------------
:: KEEP THE FOLLOWING LINES UNTOUCHED
:: ---------------------------------------------------------------
set PATH=%STARTDIR%\venv\Scripts;%PATH%
set PYTHON_VENV=%STARTDIR%\venv\Scripts
:: ---------------------------------------------------------------
:: %PYTHON_VENV%\Scripts\activate.bat
echo [2 / 7] pip update
%PYTHON_VENV%\python -m     ensurepip --upgrade
%PYTHON_VENV%\python -m pip install   --upgrade pip

echo [3 / 7] install antlr4 tool
%PYTHON_VENV%\python -m pip install antlr4-tools
if errorlevel 1 (
    echo error installing antrl4 tools
    goto have_error
)
echo [4 / 7] install antlr4 runtime
%PYTHON_VENV%\python -m pip install antlr4-python3-runtime
if errorlevel 1 (
    echo error installing antrl4 runtime
    goto have_error
)
echo [5 / 7] install polib
if not exist "%PYTHON_VENV%\Lib\site-packages\polib.py" (
%PYTHON_VENV%\python -m pip install polib
    if errorlevel 1 (
        echo error installing polib
        goto have_error
    )
)
echo [6 / 7] install Qt5
if not exist "%PYTHON_VENV%\Lib\site-packages\PyQt5\" (
%PYTHON_VENV%\python -m pip install PyQt5
    if errorlevel 1 (
        echo error installing PyQt5
        goto have_error
    )
)
echo [7 / 7] install QtWebEngine
%PYTHON_VENV%\python -m pip install PyQtWebEngine
if errorlevel 1 (
    echo error installing PyQtWebEngine
    goto have_error
)
%PYTHON_VENV%\python.exe -m pip install reportlab
goto no_error
:: ---------------------------------------------------------------
:have_error
echo "install aborted."
exit /b 1
:: ---------------------------------------------------------------
:no_error
echo done.
pause

endlocal
:: ---------------------------------------------------------------
:: E O F  -  End Of File
:: ---------------------------------------------------------------
