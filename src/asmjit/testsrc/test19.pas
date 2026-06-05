// ---------------------------------------------------------------------------
// File:   test19.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test19;

type
    TIntArray = array[0..9] of Integer = (
        1, 2, 3, 4, 5, 6, 7, 8
    );

var
    a: TIntArray;

begin
    a[0] := a[2] + 10;
    WriteLn(a[0]);
end.
