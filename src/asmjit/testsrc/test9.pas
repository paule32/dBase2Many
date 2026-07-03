// ---------------------------------------------------------------------------
// File:   test9.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test9;

procedure TestInteger(t1: Integer; t2: String; t3, t4: Integer; t5: String);
begin
    writeln('integer: ', t1);
    writeln('string: ', t2);
    writeln('t3: ', t3);
    writeln('t4: ', t4);
    writeln('Str2:', t5);
end;

procedure TestProc(t1, t2: string);
begin
    writeln('sub caller: ', t1);
    writeln('more text: ', t2);
    TestInteger(1234, 'Hallo', 42, 74, 'Welt');
end;

procedure CountDown(i: integer);
begin
    writeln(i);
    if i > 0 then CountDown(i - 1);
end;

procedure Hallo;
begin
    WriteLn('Hallo aus Procedure');
    TestProc('text', 'more text');
end;

begin
    Hallo;
    CountDown(5);
end.
