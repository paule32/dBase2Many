program testinports;

procedure TestString(S: String); cdecl 'testdll.dll';

begin
    WriteLn('DLL CALL TEST');
    TestString('Hello World');
end.
