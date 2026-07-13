REM -------------------------------------------------------------------------
REM File:   test22.bas
REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
REM All rights reserved
REM --------------------------------------------------------------------------
DIM X AS INTEGER
DIM ENABLED AS BOOLEAN

X = 42
ENABLED = TRUE

IF ENABLED AND X > 10 THEN
    PRINT "aktiv"
END IF

IF NOT ENABLED OR X = 0 THEN
    PRINT "inaktiv"
END IF
