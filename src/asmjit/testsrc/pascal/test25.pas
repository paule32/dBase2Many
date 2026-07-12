// ---------------------------------------------------------------------------
// File:   test25.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test25;

type
    TMatrix = array[0..9, 0..9] of Integer;

var
    m : TMatrix;

begin
    m[0,0] := 10;
    m[0,1] := 20;
    m[1,0] := 30;
    m[2,3] := 99;

    WriteLn(m[0,0]);
    WriteLn(m[0,1]);
    WriteLn(m[1,0]);
    WriteLn(m[2,3]);
end.
