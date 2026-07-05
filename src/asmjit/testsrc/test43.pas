// ---------------------------------------------------------------------------
// File:   test43.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test43;

type
    TFlags = array[0..3] of Boolean;

var
    flags: TFlags;

begin
    WriteLn('START');
    
    flags[0] := True;
    WriteLn('OK 1');
    
    flags[1] := False;
    WriteLn('OK 2');
    
    flags[2] := not flags[1];
    WriteLn('OK 3');
    
    flags[3] := flags[0] xor flags[2];
    WriteLn('OK 4');

    WriteLn(flags[0]); WriteLn('OK A');
    WriteLn(flags[1]); WriteLn('OK B');
    WriteLn(flags[2]); WriteLn('OK C');
    WriteLn(flags[3]); WriteLn('OK D');
end.
