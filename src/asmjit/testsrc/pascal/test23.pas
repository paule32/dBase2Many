// ---------------------------------------------------------------------------
// File:   test23.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test23;

type
    TPoint = record
        X: Integer;
        Y: Integer;
    end;

    PPoint = ^TPoint;

var
    p : TPoint;
    pp: PPoint;

begin
    pp := @p;
    pp^.X := 10;
    pp^.Y := 20;

    WriteLn(pp^.X);
    WriteLn(pp^.Y);
 end.
