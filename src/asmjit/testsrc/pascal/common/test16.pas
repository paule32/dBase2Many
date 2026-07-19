// ---------------------------------------------------------------------------
// File:   test16.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test16;

type
    TInt  = Integer;
    TReal = Double;
    TText = String;

const
    c1 = 123;

var
    i: TInt;
    d: TReal;
    s: TText;

begin
    i := c1;
    s := 'Hallo';

    WriteLn('i: ', i);
    WriteLn('s: ', s);
end.
