// ---------------------------------------------------------------------------
// File:   test53.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test53;

var
    i : Integer;

begin
    i := 2;

    case i of
        1:
            WriteLn('one');
        2:
            WriteLn('two');
        3, 4:
            WriteLn('three or four');
    else
        WriteLn('other');
    end;
end.
