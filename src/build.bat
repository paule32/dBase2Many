:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
@echo off
set "STARTDIR=%CD%"

echo erstelle resources ...
pyrcc5 resources.qrc -o resources_rc.py
::python build.py dBaseRunner.py -o start.py

echo compile dBaseRunner.py ...
python -m compileall dBaseRunner.py

echo erstelle \en\LC_MESSAGES\dbase.mo ...
pushd "locales\en\LC_MESSAGES"
msgfmt -o dbase.mo dbase.po
popd

echo erstelle \de\LC_MESSAGES\dbase.mo ...
pushd "locales\de\LC_MESSAGES"
msgfmt -o dbase.mo dbase.po
popd

echo erstelle locales.zip
pushd locales
zip -9 -R locales.zip *.*
copy /Y locales.zip ..\locales.zip
popd

echo fertig.
