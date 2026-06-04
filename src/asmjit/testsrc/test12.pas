program test12;

function Add(a: Integer; b: Integer): Integer;
    function Add2(a, b: Integer): Integer;
    begin
        Result := a + b;
    end;
begin
    Result := Add2(10, 20) + Add2(a, b);
end;

begin
    WriteLn('Add result: ', Add(10, 20));
end.
