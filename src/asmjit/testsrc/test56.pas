// ---------------------------------------------------------------------------
// File:   test56.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
{$define DLL_API2}

{$ifdef DLL_API}
library test56;
{$else}
program test56;
{$endif}

type
    TFoo = class
        constructor Create;
        constructor Create(S: String);
        constructor Create(I1, I2: Integer);
        
        destructor Destroy;
    end;

function Add(a, b: Integer): Integer;
begin
    Result := a + b;
end;

constructor TFoo.Create;
begin
    WriteLn('TFoo: Create');
end;

constructor TFoo.Create(S: String);
begin
    WriteLn('TFoo: Create(S: String)');
end;

constructor TFoo.Create(I1, I2: Integer);
begin
    WriteLn('TFoo: Create(I1, I2: Integer)');
end;

destructor TFoo.Destroy;
begin
    WriteLn('TFoo: Destroy');
end;

{$ifdef DLL_API}
exports
    Add(Integer, Integer),
    TFoo.Create(),
    TFoo.Create(String),
    TFoo.Create(Integer, Integer)
    ;
{$endif}

{$ifndef DLL_API}
var
    foo: TFoo;
{$endif}

begin

{$ifndef DLL_API}
    try
        foo := TFoo.Create('TFoo: String');
        WriteLn('before break');
        {$break}
        WriteLn('after break');
    finally
        foo.Free;
    end;
{$endif}

end.
