// ---------------------------------------------------------------------------
// File:   test14.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test14;

function GetText: String;
begin
    Result := 'Hallo aus Function';
end;

begin
    WriteLn('Text: ', GetText());
end.
