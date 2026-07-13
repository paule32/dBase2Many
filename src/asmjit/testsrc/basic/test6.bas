REM -------------------------------------------------------------------------
REM File:   test6.bas
REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
REM All rights reserved
REM --------------------------------------------------------------------------
DIM X AS INTEGER

X = 20

IF X < 10 THEN
    PRINT "kleiner als 10"
ELSEIF X = 10 THEN
    PRINT "genau 10"
ELSEIF X < 100 THEN
    PRINT "zwischen 11 und 99"
ELSE
    PRINT "größer oder gleich 100"
END IF
