// ---------------------------------------------------------------------------
// File:   test21.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test21;

type
    PInteger = ^Integer;

var
    x: Integer;
    p: PInteger;

begin
    x := 10;
    p := @x;
    p^ := 20;

    WriteLn(x);
end.
