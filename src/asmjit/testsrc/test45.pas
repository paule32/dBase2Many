// ---------------------------------------------------------------------------
// File:   test45.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test45;

procedure Test(b: Boolean);
begin
    WriteLn(b);
end;

function IsValid: Boolean;
begin
    Result := True;
end;

begin
    Test(IsValid);
end.
