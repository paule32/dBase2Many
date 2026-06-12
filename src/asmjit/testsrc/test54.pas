// ---------------------------------------------------------------------------
// File:   test54.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test54;

type
    TObject = class
        constructor Create;
        destructor Destroy;
    end;

type
    TFoo = class(TObject)
        field : Integer;

        constructor Create;
        constructor Create(S: String; I: Integer);
        
        destructor Destroy;
    end;

var
    foo : TFoo;

constructor TObject.Create;
begin
    WriteLn('TObject: Create');
end;

destructor TObject.Destroy;
begin
    WriteLn('TObject: Destroy');
end;

constructor TFoo.Create;
begin
    WriteLn('TFoo: Create');
end;

constructor TFoo.Create(S: String; I: Integer);
begin
    inherited Create;
    
    WriteLn('str: ', S);
    WriteLn('int: ', I);
end;

destructor TFoo.Destroy;
begin
    WriteLn('TFoo: Destroy');
end;

begin
    foo := TFoo.Create('test', 12);
    try
        foo.field := 42;
        WriteLn('field: ', foo.field);
    finally
        foo.Free;
    end;
end.
