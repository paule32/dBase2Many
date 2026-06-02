program Test4;

var
    x, y: Integer;
    d, e: Double;

begin
    x := 20;
    d := 10.5;
    y := 42;
    e := 3.1415;

    if d < 20.0 then
        WriteLn('d ist kleiner als 20')
    else
        WriteLn('d ist nicht kleiner als 20');

    if e = 3.141 then
        WriteLn('PI ist PI: ', e);

    if x < d then
        WriteLn('x ist kleiner als d')
    else
        WriteLn('x ist nicht kleiner als d');

end.