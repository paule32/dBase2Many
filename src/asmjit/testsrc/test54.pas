// ---------------------------------------------------------------------------
// File:   test54.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test54;

type
    TFoo = class
        field : Integer;

        constructor Create;
        constructor Create(S: String);
        
        destructor Destroy;
    end;

var
    foo : TFoo;

constructor TFoo.Create;
begin
    WriteLn('create');
end;

constructor TFoo.Create(S: String);
begin
    WriteLn('str: ', S);
end;

destructor TFoo.Destroy;
begin
    WriteLn('destroy');
end;

begin
    foo := TFoo.Create('test');
    foo.field := 42;
    WriteLn('field: ', foo.field);
    foo.Free;
end.
