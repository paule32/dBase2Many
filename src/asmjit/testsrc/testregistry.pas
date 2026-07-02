program testregistry;

uses Registry;

var
    R: TRegistry;

procedure dummy;
begin
    WriteLn('dummy call');
end;

begin
    R := TRegistry.Create;
    try
        WriteLn('Registry test');
        R.ValueA := 123;
        R.ValueB := 456;
        R.ValueC := 789;
        
        WriteLn('ValueA: ', R.ValueA);
        WriteLn('ValueB: ', R.ValueB);
        WriteLn('ValueC: ', R.ValueC);
    finally
        R.Free;
    end;
end.
