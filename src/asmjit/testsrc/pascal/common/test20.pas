// ---------------------------------------------------------------------------
// File:   test20.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test20;

function Fak(n: Integer): Integer;
begin
    if n <= 1 then
        result := 1
    else
        result := n * Fak(n - 1);
end;

begin
    WriteLn('Fak 5: ', Fak(5));
end.
