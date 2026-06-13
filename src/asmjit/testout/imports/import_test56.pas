{$mode objfpc}{$H+}
unit import_test56;

interface

const
  DLL_NAME = 'test56.dll';

function Add(a: Integer; b: Integer): Integer; external DLL_NAME name '_ADD$INTEGER$INTEGER';

type
  TFooHandle = Pointer;

function TFoo_Create: TFooHandle; external DLL_NAME name '_TEST56$$_$$_TFOO_$$_CREATE';

function TFoo_Create_AnsiString(S: AnsiString): TFooHandle; external DLL_NAME name '_TEST56$$_$$_TFOO_$$_CREATE$ANSISTRING';

function TFoo_Create_Integer_Integer(I1: Integer; I2: Integer): TFooHandle; external DLL_NAME name '_TEST56$$_$$_TFOO_$$_CREATE$INTEGER$INTEGER';

type
  TFoo = class
  private
    FHandle: TFooHandle;
  public
    constructor Create;
    constructor Create(S: AnsiString);
    constructor Create(I1: Integer; I2: Integer);
  end;

implementation

constructor TFoo.Create;
begin
  inherited Create;
  FHandle := TFoo_Create;
end;

constructor TFoo.Create(S: AnsiString);
begin
  inherited Create;
  FHandle := TFoo_Create_AnsiString(S);
end;

constructor TFoo.Create(I1: Integer; I2: Integer);
begin
  inherited Create;
  FHandle := TFoo_Create_Integer_Integer(I1, I2);
end;

begin
end.
