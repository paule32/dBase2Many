// ---------------------------------------------------------------------------
// File:   test59.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program test59;

var
    I: Integer;

begin
    WriteLn('Kommandozeile: ', CommandLine);
    WriteLn('Parameter: ', ParamCount);

    for I := 0 to ParamCount do
    WriteLn( 'ParamStr(', I, ') = [', ParamStr(I), ']');
end.
