// ---------------------------------------------------------------------------
// File:   test38.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test38;

var
    a: array of Integer;
    s: string;

begin
    writeln('START');
    
    writeln('alloc array');
    SetLength(a, 10);
    writeln('A1 OK');
    
    writeln('alloc string');
    SetLength(s, 10);
    writeln('S1 OK');
    SetLength(s, 16);
    writeln('S2 OK');
    
    a[0] := 123;
    a[1] := 456;
    writeln('A2 OK');
        
    s[1] := 'O';
    s[2] := 'P';
    s[3] := 'A';
    writeln('S3 OK');
    
    WriteLn(s[1]);
    WriteLn(s[2]);
    WriteLn(s[3]);

    WriteLn(a[0]);
    WriteLn(a[1]);
end.
