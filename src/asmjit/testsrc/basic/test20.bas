REM -------------------------------------------------------------------------
REM File:   test20.bas
REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
REM All rights reserved
REM --------------------------------------------------------------------------
SUB INCREMENT(BYREF VALUE AS INTEGER)
    VALUE = VALUE + 1
END SUB

DIM X AS INTEGER

X = 10

CALL INCREMENT(X)
PRINT X
