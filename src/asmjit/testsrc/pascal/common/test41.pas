// ---------------------------------------------------------------------------
// File:   test41.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test41;

function IsOk: Boolean;
begin
    Result := True;
end;

function IsNotOk: Boolean;
begin
    Result := False;
end;

begin
    WriteLn(IsOk);
    WriteLn(IsNotOk);
    WriteLn(not IsNotOk);
end.
