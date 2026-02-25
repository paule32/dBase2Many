:: ---------------------------------------------------------------
:: \file start.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
set "PYTHON_VENV=venv"

:: ---------------------------------------------------------------
:: \brief before we start the application, we check if the needed
::        packages are installed in ther virtual environment.
:: ---------------------------------------------------------------
echo setup ...
%PYTHON_VENV%\Scripts\python -m pip install --upgrade pip

if not exist "%PYTHON_VENV%\Lib\site-packages\antrl4\" (
%PYTHON_VENV%\Scripts\python -m pip install antlr4-python3-runtime
)
if not exist "%PYTHON_VENV%\Lib\site-packages\polib.py" (
%PYTHON_VENV%\Scripts\python -m pip install polib
)
if not exist "%PYTHON_VENV%\Lib\site-packages\PyQt5\" (
%PYTHON_VENV%\Scripts\python -m pip install PyQt5 PyQtWebEngine
)
:: ---------------------------------------------------------------
:: \brief now, the application should run fine. When you start the
::        application (or this batch script), the start of the
::        runner maybe faster - because the installed files are
::        present in venv directory.
:: ---------------------------------------------------------------
venv\Scripts\python.exe dBaseRunner.pyc
