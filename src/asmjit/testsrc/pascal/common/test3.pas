// ---------------------------------------------------------------------------
// File:   test3.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program Test3;

var
    x: Integer;
    d: Double;

begin
    x := 20;
    d := 10.5;
    
    WriteLn('start');

    if x > 10 then
        WriteLn('x ist groesser als 10')
    else
        WriteLn('x ist kleiner oder gleich 10');

    if d < 20.0 then
        WriteLn('d ist kleiner als 20');

    WriteLn('ende');
end.
