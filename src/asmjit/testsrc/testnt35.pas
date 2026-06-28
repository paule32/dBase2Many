program testnt35;

type
    TDoubleArray = array of Double;

var
    A : TDoubleArray;

begin
    SetLength(A, 3);

    A[0] := 1.5;
    A[1] := 2.5;
    A[2] := 3.5;

    WriteLn(Low(A));
    WriteLn(High(A));
    WriteLn(Length(A));

    WriteLn(A[0]);
    WriteLn(A[1]);
    WriteLn(A[2]);
end.
