// ---------------------------------------------------------------------------
// File:   test17.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test17;

type
    TColor = (
        clRed   = 2,
        clGreen = 3,
        clBlue  = 4
    );

var
    c: TColor;

begin
    WriteLn(clRed);
    WriteLn(clGreen);
    WriteLn(clBlue);

    c := clGreen;
    writeln('c: ', c);
end.
