// ---------------------------------------------------------------------------
// File:   test26.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test26;

type
    TIntArray = array[0..9] of Integer;
    PInteger  = ^Integer;

var
    a : TIntArray;
    p : PInteger;

begin
    a[0] := 10;

    p  := @a[0];
    p^ := 123;

    WriteLn(a[0]);
    WriteLn(p^);
end.
