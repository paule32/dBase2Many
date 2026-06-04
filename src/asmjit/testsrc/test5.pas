// ---------------------------------------------------------------------------
// File:   test5.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program Test5;

var
    x : Integer;
    d : Double;

begin
    x := 20;
    d := 10.5;

    if x > 10 then
    begin
        WriteLn('x > 10');

        if d < 20.0 then
        begin
            WriteLn('d < 20');
        end else
        begin
            WriteLn('d >= 20');
        end;
    end else
    begin
        WriteLn('x <= 10');
    end;

    WriteLn('ende');
end.
