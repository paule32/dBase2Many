program testdos;

type
    Tinker = Integer;
    
    PFoo = ^TFoo;
    TFoo = record
        a: Integer;
        b: String;
    end;
    
var
    i, c: Integer;
    t: Tinker;
    foo: PFoo;

(*function GetDouble: double;
var
    d: Double;
begin
    d := 3.1415;
    result := d;
end;*)

begin
    i := 42;
    WriteLn('Hallo aus DOS: ', (i * 2), ' -> ', (i / 2), ' <-');
    
    if i = 42 then
    begin
        WriteLn('ok');
        for c := 1 to 5 do
        begin
            WriteLn('Count: ', c);
        end;
    end;
    
    t := 32;
    WriteLn('t: ', t);
    
    case i of
        1:
            WriteLn('one');
        2:
            WriteLn('two');
        3, 4:
            WriteLn('three or four');
    else
        WriteLn('other');
    end;

    i := 1;
    while i < 5 do
    begin
        WriteLn('while: ', i);
        i := i + 1;
    end;
    
    i := 1;
    repeat
        WriteLn('repeat: ', i);
        i := i + 1;
    until i = 3;
    
    New(foo);
    foo^.a := 1234;
    WriteLn('foo: ', foo^.a);
    Dispose(foo);
end.
