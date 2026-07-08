// ---------------------------------------------------------------------------
// File:   test51.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test51;

var
    s : String;
    t : String;
    p : Integer;

begin
    s := 'Hallo Welt';
    
    t := Copy(s, 1, 5);
    WriteLn(t);

    t := Copy(s, 7, 4);
    WriteLn(t);

    p := Pos('Welt', s);
    WriteLn(p);

    p := Pos('abc', s);
    WriteLn(p);
end.
