program test13;


function Add(a, b: Integer): Integer;
var
    c: Integer;

    function Add2(a, b: Integer): Integer;
    begin
        c := a + b;
        Result := c;
    end;

var
    d: Integer;

begin
    c := Add2(a, b);
    d := c + 10;

    Result := d;
end;

begin
    WriteLn('Add result: ', Add(10, 20));
end.
