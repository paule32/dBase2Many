// ---------------------------------------------------------------------------
// File:   test49.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test50;

var
    S : String;
    
begin
    SetLength(S, 3);

    S[1] := 'X';
    S[2] := 'Y';
    S[3] := 'Z';

    S := 'ABC' + S;
    S := S + S;

    WriteLn(S);
end.
