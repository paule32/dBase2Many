:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
setlocal EnableDelayedExpansion
chcp 1252 >nul
:: ==========================================
:: Deutsche Doku
:: ==========================================
echo Building German documentation...
doxygen Doxyfile_de.dark
if errorlevel 1 exit /b 1

:: ==========================================
:: Englische Doku
:: ==========================================
echo Building English documentation...
doxygen Doxyfile_en.dark
if errorlevel 1 exit /b 1

:: ==========================================
:: Doku Codepage konvertieren
:: ==========================================
::python utf8tocp1252.py

:: ==========================================
:: CHM-Verzeichnis vorbereiten
:: ==========================================
if not exist out\chm mkdir out\chm

copy /Y out\de\html\dBaseHelp_de.chm out\chm\
copy /Y out\en\html\dBaseHelp_en.chm out\chm\

echo Creating timestamped master project...

:: ==========================================
:: Master CHM kompilieren
:: ==========================================
set HHC="C:\Program Files (x86)\HTML Help Workshop\hhc.exe"

%HHC% out\chm\master.hhp

echo ==========================================
echo   Fertig.
echo ==========================================

endlocal
pause
