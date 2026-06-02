program test6;

var
    x : Integer;

begin
    x := 0;

    while x < 5 do
    begin
        WriteLn('x = ', x);
        x := x + 1;
    end;

    WriteLn('ende');
end.
