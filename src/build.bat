:: ---------------------------------------------------------------
:: \file build.bat
:: \note (c) 2026 by Jens Kallup - paule32 aka Blacky Cat
::       all rights reserved.
:: ---------------------------------------------------------------
pyrcc5 resources.qrc -o resources_rc.py
python build.py dBaseRunner.py -o start.py
python -m compileall start.py
