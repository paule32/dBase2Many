// ---------------------------------------------------------------------------
// File:   test18.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test18;

type
    TPoint = record
        X: Integer;
        Y: Integer;
    end;

    TRecord = record
      R1: TPoint;
      R2: TPoint;
    end;

    TRect = record
        TopLeft    : TRecord;
        BottomRight: TRecord;
    end;

var
    p: TPoint;
    r: TRect;

begin
    p.X := 10;

    r.TopLeft.R1.X := 10;
    r.TopLeft.R1.Y := 20;

    WriteLn(p.X);

    WriteLn('rX: ', r.TopLeft.R1.X);
    WriteLn('rY: ', r.TopLeft.R1.Y);
end.
