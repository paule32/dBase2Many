REM -------------------------------------------------------------------------
REM File:   test26.bas
REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
REM All rights reserved
REM --------------------------------------------------------------------------
DIM VALUE AS INTEGER

VALUE = 25

IF VALUE < 10 THEN
    PRINT "klein"
ELSEIF VALUE < 100 THEN
    PRINT "mittel"
ELSE
    PRINT "groß"
END IF
