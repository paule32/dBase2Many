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
    SetLength(a, 10);
    SetLength(s, 10);

    a[0] := 123;
    a[1] := 456;
    
    s[1] := 'O';
    s[2] := 'P';
    s[3] := 'A';
    
    WriteLn(s[0]);
    WriteLn(s[1]);

    WriteLn(a[0]);
    WriteLn(a[1]);
end.
