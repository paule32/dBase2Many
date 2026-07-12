// ---------------------------------------------------------------------------
// File:   VCL.Windows.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

unit VCL.Windows;

interface

type
    TZuZu = class
    public
        constructor Create;
        destructor Destroy;
    end;

function GetNumber: Integer;
procedure TestString(S: String);

implementation

constructor TZuZu.Create;
begin
    WriteLn('zuzu: Create');
end;
destructor TZuZu.Destroy;
begin
    WriteLn('zuzu: Destroy');
end;

procedure TestString(S: String);
begin
    WriteLn('Test: ', S);
end;

function GetNumber: Integer;
begin
    Result := 100;
end;

begin
    WriteLn('VCL.Windows init');
end.
