// ---------------------------------------------------------------------------
// File:   test11.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test11;

function Add1(a: Integer; b: Integer): Integer;
begin
    Result := a + b;
end;

function Add2(a, b: Integer): Integer;
begin
    Result := a + b;
end;

begin
    WriteLn('Add1 result: ', Add1(10, 20));
    WriteLn('Add2 result: ', Add2(10, 32));
end.
