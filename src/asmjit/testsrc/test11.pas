program test11;

function Add1(a: Integer; b: Integer): Integer;
begin
    Result := a + b;
end;

function Add2(a, b: Integer): Integer;
begin
    Result := a + b;
end;

begin
    WriteLn('Add1 result: ', Add1(10, 20));
    WriteLn('Add2 result: ', Add2(10, 32));
end.
