// ---------------------------------------------------------------------------
// File:   System.Types.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------


// ---------------------------------------------------------------------------
// File:   test56.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit Registry;
interface

type
    TRegistry = class
    private
        FValueA: Integer;
        FValueB: Integer;
        FValueC: Integer;
        FValueD: Integer;
    protected
        procedure SetValueA(v: Integer);
        procedure SetValueB(v: Integer);
        procedure SetValueC(v: Integer);
        procedure SetValueD(v: Integer);
        
        function  GetValueA: Integer;
        function  GetValueB: Integer;
        function  GetValueC: Integer;
        function  GetValueD: Integer;
    public
        constructor Create;
        constructor Create(S: String);
        constructor Create(I1, I2: Integer);
        
        destructor Destroy;
        
    published
        property ValueA: Integer read GetValueA write SetValueA;
        property ValueB: Integer read GetValueB write FValueB;
        property ValueC: Integer read FValueC   write SetValueC;
        property ValueD: Integer read FValueD   write FValueD;
    end;

implementation

function Add(a, b: Integer): Integer;
begin
    Result := a + b;
end;

constructor TRegistry.Create;
begin
    WriteLn('TFoo: Create');
end;

constructor TRegistry.Create(S: String);
begin
    WriteLn('TFoo: Create(S: String)');
    WriteLn(S);
end;

constructor TRegistry.Create(I1, I2: Integer);
begin
    WriteLn('TFoo: Create(I1, I2: Integer)');
end;

destructor TRegistry.Destroy;
begin
    WriteLn('TFoo: Destroy');
end;

procedure TRegistry.SetValueA(v: Integer); begin FValueA := v; end;
procedure TRegistry.SetValueB(v: Integer); begin FValueB := v; end;
procedure TRegistry.SetValueC(v: Integer); begin FValueC := v; end;
procedure TRegistry.SetValueD(v: Integer); begin FValueD := v; end;

function TRegistry.GetValueA: Integer; begin result := FValueA; end;
function TRegistry.GetValueB: Integer; begin result := FValueB; end;
function TRegistry.GetValueC: Integer; begin result := FValueC; end;
function TRegistry.GetValueD: Integer; begin result := FValueD; end;

begin
end.
