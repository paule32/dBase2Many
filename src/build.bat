:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
setlocal EnableDelayedExpansion

set "STARTDIR=%CD%"
set "CPYTHON=cpython-313"
set "DIST=dist\dBaseRunner"
set "GEN_DBASE=gen\__pycache__\dBase"
set "CHM_HELP=..\doc\out\chm\dBaseHelp"

:: ---------------------------------------------------------------
:: resources:
:: ---------------------------------------------------------------
echo build resources ...
pyrcc5 resources.qrc -o resources_rc.py

:: ---------------------------------------------------------------
:: build the parser for dbase ...
:: ---------------------------------------------------------------
antlr4 -Dlanguage=Python3 -visitor -o gen          dBaseLexer.g4
antlr4 -Dlanguage=Python3 -visitor -o gen -lib gen dBaseParser.g4

pushd gen
python -m compileall dBaseLexer.py
python -m compileall dBaseParser.py
python -m compileall dBaseListener.py
python -m compileall dBaseParserVisitor.py

:: ---------------------------------------------------------------
:: rename the output files that was created by python3 ...
:: ---------------------------------------------------------------
pushd __pycache__
copy /y dBaseLexer.%CPYTHON%.pyc          dBaseLexer.pyc
copy /y dBaseParser.%CPYTHON%.pyc         dBaseParser.pyc
copy /y dBaseParserListener.%CPYTHON%.pyc dBaseParserListener.pyc
copy /y dBaseParserVisitor.%CPYTHON%.pyc  dBaseParserVisitor.pyc

del dBaseParser*.%CPYTHON%.pyc
popd
popd
:: ---------------------------------------------------------------
:: build the main application (dbase) ...
:: ---------------------------------------------------------------
echo compile dBaseRunner.py ...
copy /y dBaseRunner_patched51.py dBaseRunner.py
python -m compileall dBaseRunner.py
if errorlevel 1 (
echo error building dBaseRunner
exit /b 1
)
python -m compileall resources_rc.py
if errorlevel 1 (
echo error building resources_rc.py
exit /b 1
)
:: ---------------------------------------------------------------
:: perform pre-task for application scripts ...
:: ---------------------------------------------------------------
pushd __pycache__
copy /y dBaseRunner.%CPYTHON%.pyc dBaseRunner.pyc
copy /y resources_rc.%CPYTHON%.pyc resources_rc.pyc

del *.cpython-313.pyc
popd

:: ---------------------------------------------------------------
:: create the locales for supported languages ...
:: ---------------------------------------------------------------
echo build \en\LC_MESSAGES\dbase.mo ...
pushd "locales\en\LC_MESSAGES"
del dbase.mo
msgfmt -o dbase.mo dbase.po
if errorlevel 1 (
echo error creating english dbase.mo
exit /b 1
)
popd
echo build \de\LC_MESSAGES\dbase.mo ...
pushd "locales\de\LC_MESSAGES"
del dbase.mo
msgfmt -o dbase.mo dbase.po
if errorlevel 1 (
echo error creating german dbase.mo
exit /b 1
)
popd
:: ---------------------------------------------------------------
:: pack the locales files into single zip archive ...
:: ---------------------------------------------------------------
echo create locale bundle: locales.zip
pushd locales
del locales.zip
zip -9 -R locales.zip *.mo
if errorlevel 1 (
echo error creating locales.zip
exit /b 1
)
popd
:: ---------------------------------------------------------------
rm -rf dist
mkdir  dist
mkdir  %DIST%
mkdir  %DIST%\gen
mkdir  %DIST%\data
:: ---------------------------------------------------------------
copy /y locales\locales.zip %DIST%\data\locales.zip
if errorlevel 1 (
echo error copy locales.zip
exit /b 1
)
:: ---------------------------------------------------------------
:: install application binaries ...
:: ---------------------------------------------------------------
copy __pycache__\dBaseRunner.pyc %DIST%\dBaseRunner.pyc
copy __pycache__\resources_rc.pyc %DIST%\resources_rc.pyc

:: ---------------------------------------------------------------
:: copy dbase parser files ...
:: ---------------------------------------------------------------
copy %GEN_DBASE%Lexer.pyc %DIST%\gen\dBaseLexer.pyc
copy %GEN_DBASE%Parser.pyc %DIST%\gen\dBaseParser.pyc
copy %GEN_DBASE%ParserListener.pyc %DIST%\gen\dBaseParserListener.pyc
copy %GEN_DBASE%ParserVisitor.pyc %DIST%\gen\dBaseParserVisitor.pyc

:: ---------------------------------------------------------------
:: create documentation:
:: ---------------------------------------------------------------
echo building German documentation ...
pushd ..\doc
cd out
if exist de    ( rm -rf de    )
if exist en    ( rm -rf en    )
if exist dark  ( rm -rf dark  )
if exist ligth ( rm -rf ligth )
:: ---------------------------------------------------------------
mkdir  light
mkdir  dark

cd ..
:: ---------------------------------------------------------------
doxygen.exe Doxyfile_de.dark
if errorlevel 1 (
echo error building dark german documentation.
exit /b 1
)
:: ---------------------------------------------------------------
doxygen.exe Doxyfile_de.light
if errorlevel 1 (
echo error building light german documentation.
exit /b 1
)
:: ---------------------------------------------------------------
echo building English documentation ...
doxygen.exe Doxyfile_en.dark
if errorlevel 1 (
echo error building dark english documentation.
exit /b 1
)
:: ---------------------------------------------------------------
doxygen.exe Doxyfile_en.light
if errorlevel 1 (
echo error building light english documentation.
exit /b 1
)
popd
:: ---------------------------------------------------------------
:: copy documentation files ...
:: ---------------------------------------------------------------
pushd ..\doc
if not exist out\chm (
mkdir out
mkdir out\chm
)
copy /Y out\dark\de\html\dBaseHelp_dark_de.chm out\chm\
copy /Y out\dark\en\html\dBaseHelp_dark_en.chm out\chm\

copy /Y out\light\de\html\dBaseHelp_light_de.chm out\chm\
copy /Y out\light\en\html\dBaseHelp_light_en.chm out\chm\
popd

copy /y %CHM_HELP%_dark_de.chm %DIST%\data\dBaseHelp_dark_de.chm
copy /y %CHM_HELP%_dark_en.chm %DIST%\data\dBaseHelp_dark_en.chm

copy /y %CHM_HELP%_light_de.chm %DIST%\data\dBaseHelp_light_de.chm
copy /y %CHM_HELP%_light_en.chm %DIST%\data\dBaseHelp_light_en.chm

copy /y install.bat %DIST%\install.bat
copy /y start.bat %DIST%\start.bat

:: ---------------------------------------------------------------
:: create zip archive for ftp server upload ...
:: ---------------------------------------------------------------
echo create zip archive ...
pushd dist
::zuo -9 -R packed.zip *.*
popd

:: ---------------------------------------------------------------
:: \brief todo: modify the path in install.bat, to start python3.
:: \note  use the Microsoft App Store to install Python3.
:: ---------------------------------------------------------------
echo all files under: .\dist\
echo done.
endlocal
