// ---------------------------------------------------------------------------
// File:   test57.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program test57;

function Sum(const Values: array of Integer): Integer;
var
    I: Integer;
begin
    Result := 0;

    for I := Low(Values) to High(Values) do
        Result := Result + Values[I];
end;

begin
    WriteLn(Sum([1, 2, 3, 5]));
end.
