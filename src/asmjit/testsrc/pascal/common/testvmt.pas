// ---------------------------------------------------------------------------
// File:   testvmt.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
{$link dll_inflate.o}
{$link dll_loader.o}
{$link dll_runtime_bindings.o}
{$link dll_runtime.o}
{$link dll_runtime_thunks_mini.o}
program testvmt;

uses System.Objects, System.Strings;

type
    TFaz = class(TObject)
    public
        constructor Create;
        destructor Destroy; override;
        
        procedure Show; virtual;
    end;
type
    TFoo = class(TFaz)
    private
        FValue: Integer;
        FString: String;
        FDouble: Double;
        FName: String;
    public
        constructor Create(AValue: Integer);
        destructor Destroy; override;
        
        procedure Show; override;
    published
        property OnTest: String read FString write FString;
        property OnTest2: Double read FDouble write FDouble;
        property OnTest3: String read FName write FName;
    end;

procedure PrintLn(S1: String; S2: String);
begin
    WriteLn(S1,s2);
end;

constructor TFaz.Create;
begin
    inherited Create;
    WriteLn('TFaz Create');
end;
procedure TFaz.Show;
begin
    PrintLn('TFaz Show', '');
    PrintLn('  Runtime class: ', ClassName);
    PrintLn('  Method  owner: ', OwnerClassName());
    PrintLn('  Size         : ', IntToStr(InstanceSize));
end;
destructor TFaz.Destroy;
begin
    PrintLn('TFaz Destroy','');
    inherited Destroy;
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
    PrintLn('TFoo Destroy','');
    inherited Destroy;
end;

procedure TFoo.Show;
begin
    PrintLn('TFoo Show','');
    PrintLn('  Runtime class: ', ClassName);
    PrintLn('  Method  owner: ', OwnerClassName );
    PrintLn('  Size         : ', IntToStr(self.InstanceSize));
    inherited Show;
end;

var
    Foo: TFoo;
    
begin
    Foo := TFoo.Create(42);
    try
        Foo.Show;
    finally
        Foo.Free;
    end;
end.
