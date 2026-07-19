// ---------------------------------------------------------------------------
// File:   test29.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test29;

type
    TIntArray = array[0..9] of Integer;
    TMatrix   = array[0..9] of TIntArray;

var
    m: TMatrix;

begin
    m[0, 0] := 10;
    m[0, 1] := 20;
    m[1, 0] := 30;
    m[2, 3] := 99;

    WriteLn(m[0, 0]);
    WriteLn(m[0, 1]);
    WriteLn(m[1, 0]);
    WriteLn(m[2, 3]);
end.
