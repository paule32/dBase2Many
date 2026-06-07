// ---------------------------------------------------------------------------
// File:   test38.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test38;

var
    a: array of Integer;

begin
    SetLength(a, 10);

    a[0] := 123;
    a[1] := 456;

    WriteLn(a[0]);
    WriteLn(a[1]);
end.
