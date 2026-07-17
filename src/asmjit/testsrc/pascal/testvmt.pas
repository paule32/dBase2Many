// ---------------------------------------------------------------------------
// File:   testvmt.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
{$link dll_inflate.o}
{$link dll_loader.o}
{$link dll_runtime_bindings.o}
{$link dll_runtime_thunks.o}
{$link dll_runtime.o}
program testvmt;

uses System.Objects;

type
    TFoo = class(TObject)
    private
        FValue: Integer;
        FString: String;
        FDouble: Double;
        FName: String;
    public
        constructor Create(AValue: Integer);
        destructor Destroy; override;
        
        procedure Show; virtual;
    published
        property OnTest: String read FString write FString;
        property OnTest2: Double read FDouble write FDouble;
        property OnTest3: String read FName write FName;
    end;

constructor TFoo.Create(AValue: Integer);
begin
    inherited Create;
    FValue := AValue;
    
    FString := 'Hello';
    FDouble := 3.21;
    FName   := 'World !';
end;

destructor TFoo.Destroy;
begin
    WriteLn('TFoo Destroy');
    inherited Destroy;
end;

procedure TFoo.Show;
begin
    WriteLn('Value: ', FValue, ', ', FString, ', ', FDouble, ', ', FName);
end;

var
    Foo: TFoo;
    
begin
    Foo := TFoo.Create(42);
    try
        Foo.Show;
        WriteLn('Instance size: ', Foo.InstanceSize);
    finally
        Foo.Free;
    end;
end.
