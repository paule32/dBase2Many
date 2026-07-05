// ---------------------------------------------------------------------------
// File:   test50.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test50;

var
    S : String;
    
begin
    SetLength(S, 3);
    writeln('ALLOC OK');

    S[1] := 'X';  writeln('S1: OK');
    S[2] := 'Y';  writeln('S2: OK');
    S[3] := 'Z';  writeln('S3: OK');
     
    S := 'ABC' + S;  writeln('C1: OK');
    S := S + S;      writeln('C2: OK');

    WriteLn(S);
end.
