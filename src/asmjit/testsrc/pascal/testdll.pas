library testdll;

function Add(A, B: Integer): Integer;
begin
    Result := A + B;
end;

procedure TestString(S: String);
begin
    WriteLn('IN DLL PART');
    WriteLn('S: ', S);
end;

exports
    Add,
    TestString;
    
begin
end.
