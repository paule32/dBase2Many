:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
setlocal EnableDelayedExpansion

set "STARTDIR=%CD%"
set "CPYTHON=cpython-313"
set "PY313=%STARTDIR%\venv\Scripts"

set "DIST=dist\dBaseRunner"
set "GEN_DBASE=gen\__pycache__\dBase"
set "CHM_HELP=..\doc\out\chm\dBaseHelp"

:: ---------------------------------------------------------------
:: resources:
:: ---------------------------------------------------------------
echo build resources ...
pyrcc5 resources.qrc -o resources_rc.py
if errorlevel 1 (
echo error building dBaseLexer
goto have_error
)
:: ---------------------------------------------------------------
:: build the parser for dbase ...
:: ---------------------------------------------------------------
antlr4 -Dlanguage=Python3 -visitor -o gen dBaseLexer.g4
if errorlevel 1 (
echo error building dBaseLexer
goto have_error
)
antlr4 -Dlanguage=Python3 -visitor -o gen -lib gen dBaseParser.g4
if errorlevel 1 (
echo error building dBaseParser
goto have_error
)

pushd gen
%PY313%\python -m compileall dBaseLexer.py
if errorlevel 1 (
echo error building dBaseLexer
goto have_error
)
%PY313%\python -m compileall dBaseParser.py
if errorlevel 1 (
echo error building dBaseParser
goto have_error
)
%PY313%\python -m compileall dBaseParserListener.py
if errorlevel 1 (
echo error building dBaseParserListener
goto have_error
)
%PY313%\python -m compileall dBaseParserVisitor.py
if errorlevel 1 (
echo error building dBaseParserVisitor
goto have_error
)

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
%PY313%\python -m compileall dBaseRunner.py
if errorlevel 1 (
echo error building dBaseRunner
goto have_error
)
%PY313%\python -m compileall resources_rc.py
if errorlevel 1 (
echo error building resources_rc.py
goto have_error
)
:: ---------------------------------------------------------------
:: perform pre-task for application scripts ...
:: ---------------------------------------------------------------
pushd __pycache__
copy /y dBaseRunner.%CPYTHON%.pyc dBaseRunner.pyc
copy /y resources_rc.%CPYTHON%.pyc resources_rc.pyc

del *.cpython-314.pyc
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
goto have_error
)
popd
echo build \de\LC_MESSAGES\dbase.mo ...
pushd "locales\de\LC_MESSAGES"
del dbase.mo
msgfmt -o dbase.mo dbase.po
if errorlevel 1 (
echo error creating german dbase.mo
goto have_error
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
goto have_error
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
goto have_error
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
pushd ..\doc\src
cd ..\out
if exist de    ( rm -rf de    )
if exist en    ( rm -rf en    )
if exist dark  ( rm -rf dark  )
if exist ligth ( rm -rf ligth )
:: ---------------------------------------------------------------
mkdir light
mkdir dark
cd ..\src
:: ---------------------------------------------------------------
doxygen.exe Doxyfile_de.dark
if errorlevel 1 (
echo error building dark german documentation.
goto have_error
)
:: ---------------------------------------------------------------
doxygen.exe Doxyfile_de.light
if errorlevel 1 (
echo error building light german documentation.
goto have_error
)
:: ---------------------------------------------------------------
echo building English documentation ...
doxygen.exe Doxyfile_en.dark
if errorlevel 1 (
echo error building dark english documentation.
goto have_error
)
:: ---------------------------------------------------------------
doxygen.exe Doxyfile_en.light
if errorlevel 1 (
echo error building light english documentation.
goto have_error
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
:: TODO: create zip archive for ftp server upload ...
:: ---------------------------------------------------------------
goto skip
echo create zip archive ...
pushd dist
zip -9 -R packed.zip *.*
if errorlevel 1 (
echo error building dBaseLexer
goto have_error
)
popd
:skip
goto ok

:have_error
echo error on building dBaseRunner
popd
exit /b 1

:: ---------------------------------------------------------------
:: \brief todo: modify the path in install.bat, to start python3.
:: \note  use the Microsoft App Store to install Python3.
:: ---------------------------------------------------------------
:ok
echo all files under: .\dist\
echo done.
endlocal
