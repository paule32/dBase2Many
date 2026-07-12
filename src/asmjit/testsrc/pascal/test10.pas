// ---------------------------------------------------------------------------
// File:   test10.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test10;

function GetValue: Integer;
begin
    Result := 1234;
end;

begin
    WriteLn('Function result: ', GetValue());
end.
