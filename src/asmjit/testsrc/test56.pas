// ---------------------------------------------------------------------------
// File:   test56.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

library test56;

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

exports
    Add(Integer, Integer),
    TFoo.Create(),
    TFoo.Create(String),
    TFoo.Create(Integer, Integer)
    ;

begin
end.
