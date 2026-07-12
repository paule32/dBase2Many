// ---------------------------------------------------------------------------
// File:   test40.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test40;

var
    a: Boolean;
    b: Boolean;

begin
    a := True;
    b := False;

    WriteLn(a and b);
    WriteLn(a or b);
    WriteLn(a xor b);
    WriteLn(not a);
    WriteLn(not b);
end.
