1 REM ------------------------------------------------------------------------
2 REM File:   test21.bas
3 REM Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
4 REM All rights reserved
5 REM ------------------------------------------------------------------------
10 DIM X AS INTEGER
20 X = X + 1
30 PRINT "X = "; X
40 IF X < 5 THEN GOTO 20
50 GOSUB 100
60 STOP

100 PRINT "Programm beendet"
110 RETURN
