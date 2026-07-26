// ---------------------------------------------------------------------------
// File:   testvmt.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
{ $ l ink dll_inflate.o}
{ $ l ink dll_loader.o}
{ $ l ink dll_runtime_bindings.o}
{ $ l ink dll_runtime.o}
{ $ l ink dll_runtime_thunks_mini.o}
{$linklib lib_runtime.a}
{$link    dll_runtime_mini.o}
program testvmt;

uses System, Windows;

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
    Application: TApplication;
begin
    Foo := TFoo.Create(42);
    try
        Foo.Show;
    finally
        Foo.Free;
    end;
    
    Application := TApplication.Create;
    Application.Free;
    
    ExitProcess(0)
end.
