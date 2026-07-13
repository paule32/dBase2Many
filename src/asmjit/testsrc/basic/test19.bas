REM -------------------------------------------------------------------------
REM File:   test19.bas
REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
REM All rights reserved
REM --------------------------------------------------------------------------
FUNCTION SQUARE(N AS INTEGER) AS INTEGER
    RETURN N * N
END FUNCTION
    
SUB SHOWVALUE(V AS INTEGER)
    PRINT "Wert: "; V
END SUB

DIM X AS INTEGER

X = SQUARE(7)

CALL SHOWVALUE(X)
