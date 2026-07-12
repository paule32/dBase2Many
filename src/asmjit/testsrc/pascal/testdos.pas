program testdos;

type
    Tinker = Integer;
    
    PFoo = ^TFoo;
    TFoo = record
        a: Integer;
        b: String;
    end;
    
    TClass = class
    public
        constructor Create;
        constructor Create(S: String);
        
        destructor Destroy;
    end;

var
    i, c: Integer;
    t: Tinker;
    foo: PFoo;
    cls: TClass;

constructor TClass.Create;
begin
    WriteLn('TClass: ctor');
end;

constructor TClass.Create(S: String);
begin
    WriteLn('TClass::String: ctor');
end;

destructor TClass.Destroy;
begin
    WriteLn('TClass: dtor');
end;

function GetString: String;
var
    S: String;
begin
    S := '3.1415';
    result := S;
end;

function GetInteger: Integer;
var
    I: Integer;
begin
    I := 21;
    result := I;
end;

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
    
    try
        New(foo);
        foo^.a := 1234;
        WriteLn('foo: ', foo^.a);
    finally
        WriteLn('Dispose');
        Dispose(foo);
    end;
    
    WriteLn('Class');
    cls := TClass.Create('Klassler');
    try
        WriteLn('str: ', GetString);
        WriteLn('int: ', GetInteger);
    finally
        cls.Free;
    end;
end.
