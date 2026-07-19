// ---------------------------------------------------------------------------
// File:   test39.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test39;

type
    TPoint = record
        X: Integer;
        Y: Integer;
    end;

var
    Points: array of TPoint;

begin
    SetLength(Points, 10);

    Points[0].X := 100;
    Points[0].Y := 200;

    WriteLn(Points[0].X);
    WriteLn(Points[0].Y);
end.
