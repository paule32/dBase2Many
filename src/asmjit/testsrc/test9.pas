program test9;

procedure TestInteger(t1: Integer; t2: String; t3, t4: Integer);
begin
    writeln('integer: ', t1);
    writeln('string: ', t2);
    writeln('t3: ', t3);
    writeln('t4: ', t4);
end;

procedure TestProc(t1, t2: string);
begin
    writeln('sub caller: ', t1);
    writeln('more text: ', t2);
    TestInteger(1234, 'Hallo', 42, 74);
end;

procedure Hallo;
begin
    WriteLn('Hallo aus Procedure');
    TestProc('text', 'more text');
end;

begin
    Hallo;
end.
