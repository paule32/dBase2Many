// ---------------------------------------------------------------------------
// File:   test42.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test42;

var
    flags: array of Boolean;

begin
    SetLength(flags, 4);

    flags[0] := True;
    flags[1] := False;
    flags[2] := not flags[1];
    flags[3] := flags[0] and flags[2];

    WriteLn(flags[0]);
    WriteLn(flags[1]);
    WriteLn(flags[2]);
    WriteLn(flags[3]);
end.
