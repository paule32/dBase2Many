// ---------------------------------------------------------------------------
// File:   test55.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test55;

uses VCL.Windows;

var
    x: Integer;
    z: TZuZu;
    
begin
    x := GetNumber;
    WriteLn('x: ', x);
    TestString('Hola');
    
    z := TZuZu.Create;
    try
    finally
        z.Free;
    end;
end.
