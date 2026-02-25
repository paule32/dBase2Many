:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
set "STARTDIR=%CD%"
set "CPYTHON=cpython-313"

echo erstelle resources ...
pyrcc5 resources.qrc -o resources_rc.py

antlr4 -Dlanguage=Python3 -visitor -o gen          dBaseLexer.g4
antlr4 -Dlanguage=Python3 -visitor -o gen -lib gen dBaseParser.g4

pushd gen
python -m compileall dBaseLexer.py
python -m compileall dBaseParser.py
python -m compileall dBaseListener.py
python -m compileall dBaseParserVisitor.py

pushd __pycache__
copy /y dBaseLexer.%CPYTHON%.pyc          dBaseLexer.pyc
copy /y dBaseParser.%CPYTHON%.pyc         dBaseParser.pyc
copy /y dBaseParserListener.%CPYTHON%.pyc dBaseParserListener.pyc
copy /y dBaseParserVisitor.%CPYTHON%.pyc  dBaseParserVisitor.pyc

del dBaseParser*.%CPYTHON%.pyc
popd
popd

echo compile dBaseRunner.py ...
copy /y dBaseRunner_patched51.py dBaseRunner.py
python -m compileall dBaseRunner.py
python -m compileall resources_rc.py

pushd __pycache__
copy /y dBaseRunner.%CPYTHON%.pyc dBaseRunner.pyc
copy /y resources_rc.%CPYTHON%.pyc resources_rc.pyc

del *.cpython-313.pyc
popd

echo erstelle \en\LC_MESSAGES\dbase.mo ...
pushd "locales\en\LC_MESSAGES"
del dbase.mo
msgfmt -o dbase.mo dbase.po
popd

echo erstelle \de\LC_MESSAGES\dbase.mo ...
pushd "locales\de\LC_MESSAGES"
del dbase.mo
msgfmt -o dbase.mo dbase.po
popd

echo erstelle locales.zip
pushd locales
del locales.zip
zip -9 -R locales.zip *.mo
popd

:: ---------------------------------------------------------------
:: install application binaries ...
:: ---------------------------------------------------------------
rm -rf dist

mkdir  dist
mkdir  dist\dBaseRunner
mkdir  dist\dBaseRunner\gen
mkdir  dist\dBaseRunner\data

copy __pycache__\dBaseRunner.pyc dist\dBaseRunner\dBaseRunner.pyc
copy __pycache__\resources_rc.pyc dist\dBaseRunner\resources_rc.pyc

copy gen\__pycache__\dBaseLexer.pyc dist\dBaseRunner\gen\dBaseLexer.pyc
copy gen\__pycache__\dBaseParser.pyc dist\dBaseRunner\gen\dBaseParser.pyc
copy gen\__pycache__\dBaseParserListener.pyc dist\dBaseRunner\gen\dBaseParserListener.pyc
copy gen\__pycache__\dBaseParserVisitor.pyc dist\dBaseRunner\gen\dBaseParserVisitor.pyc

copy /y locales\locales.zip dist\dBaseRunner\data\locales.zip

copy /y ..\doc\out\chm\dBaseHelp_de.chm dist\dBaseRunner\data\dBaseHelp_de.chm
copy /y ..\doc\out\chm\dBaseHelp_en.chm dist\dBaseRunner\data\dBaseHelp_en.chm

copy /y install.bat dist\dBaseRunner\install.bat
copy /y start.bat dist\dBaseRunner\start.bat

:: ---------------------------------------------------------------
:: \brief todo: modify the path in install.bat, to start python3.
:: \note  use the Microsoft App Store to install Python3.
:: ---------------------------------------------------------------
echo all files under: .\dist\
echo done.
