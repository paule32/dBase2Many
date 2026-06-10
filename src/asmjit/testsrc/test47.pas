// ---------------------------------------------------------------------------
// File:   test47.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test47;

begin
    WriteLn('start');

    try
        WriteLn('inside try');
    finally
        WriteLn('inside finally');
    end;

    WriteLn('done');
end.
