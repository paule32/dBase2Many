:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
setlocal EnableDelayedExpansion
python build.py ^
    --sources "..\dark\de\html|Deutsch" "..\dark\en\html|English" ^
    --out ".\\merged_build" ^
    --project-name "MergedHelp" ^
    --default-topic "..\dark\de\html\index.html" ^
    --compile ^
    --hhc "C:\Program Files (x86)\HTML Help Workshop\hhc.exe" ^
    --clean
endlocal
:: ---------------------------------------------------------------
:: E O F  -  End Of File
:: ---------------------------------------------------------------
