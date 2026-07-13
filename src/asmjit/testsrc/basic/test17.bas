REM -------------------------------------------------------------------------
REM File:   test17.bas
REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
REM All rights reserved
REM --------------------------------------------------------------------------
DIM VALUES(4) AS INTEGER
DIM I AS INTEGER

FOR I = 0 TO 4
    VALUES(I) = I * I
NEXT I

FOR I = 0 TO 4
    PRINT "VALUES("; I; ") = "; VALUES(I)
NEXT I
