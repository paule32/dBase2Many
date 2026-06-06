// ---------------------------------------------------------------------------
// File:   test24.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test24;

type
    TPoint = record
        X: Integer;
        Y: Integer;
    end;

    TPointArray = array[0..9] of TPoint;

var
    points: TPointArray;

begin
    points[0].X := 10;
    points[0].Y := 20;

    WriteLn(points[0].X);
    WriteLn(points[0].Y);
end.
