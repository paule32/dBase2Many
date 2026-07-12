// ---------------------------------------------------------------------------
// File:   test27.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test27;

type
    PInteger = ^Integer;

var
    p : PInteger;

begin
    New(p);
    p^ := 123;

    WriteLn(p^);

    Dispose(p);
end.
