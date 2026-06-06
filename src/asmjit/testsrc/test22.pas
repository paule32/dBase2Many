// ---------------------------------------------------------------------------
// File:   test22.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test22;

type
    TIntArray = array[0..9] of Integer;

var
    a: TIntArray;

begin
    a[10] := 123;	// error
end.
