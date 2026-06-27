program testnt35;

type
    TIntArray = array[0..9] of Integer;
    PInteger  = ^Integer;

var
    A : TIntArray;
    P1,P2 : PInteger;

begin
    A[0] := 1234;

    P1 := @A[0];
    P2 := P1;

    WriteLn(P1^);
    WriteLn(P2^);
end.
