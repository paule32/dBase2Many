// ---------------------------------------------------------------------------
// File:   test15.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test15;

var
    i: Integer;
    d: Double;
    s: String;

const st = 'Ein String';
const i2 = 102, i3 = 103, s3 = 'Texter', d4 = 2.134;

function PiValue: Double;
begin
    Result := 3.1415926;
end;

function GetInteger: Integer;
begin
    result := 42;
end;

function GetDouble: Double;
begin
    result := 12.34;
end;

function GetString: String;
const s1 = 'Foo Fuu';
begin
    result := s1;
end;

begin
    i := GetInteger;
    d := GetDouble;
    s := GetString;

    WriteLn('i : ', i);
    WriteLn('d : ', d);
    WriteLn('s : ', s);
    WriteLn;
    WriteLn('Pi: ', PiValue);
end.
