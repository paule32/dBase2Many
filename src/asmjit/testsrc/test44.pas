// ---------------------------------------------------------------------------
// File:   test44.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test44;

type
    TUser = record
        Active : Boolean;
        Admin  : Boolean;
    end;

var
    U : TUser;

begin
    U.Active := True;
    U.Admin  := False;

    if U.Active and not U.Admin then
        WriteLn('User active');
end.
