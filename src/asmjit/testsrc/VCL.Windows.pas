// ---------------------------------------------------------------------------
// File:   VCL.Windows.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

unit VCL.Windows;

interface

function GetNumber: Integer;

implementation

function GetNumber: Integer;
begin
    Result := 100;
end;

begin
    WriteLn('VCL.Windows init');
end.
