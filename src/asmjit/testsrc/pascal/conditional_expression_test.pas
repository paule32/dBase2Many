// ---------------------------------------------------------------------------
// Test: inferred variables with conditional expressions
// ---------------------------------------------------------------------------
program conditional_expression_test;

function Limit: Integer;
begin
    Result := 7;
end;

procedure TestLocal;
var
    LocalValue := if 10 > 3 else 0;
begin
    // Expected: 3
    WriteLn('LocalValue = ', LocalValue);
end;

var
    FirstValue  := if 5 <= 3 else 1;
    SecondValue := if 5 <= Limit else 2;

begin
    // Expected: 1
    WriteLn('FirstValue = ', FirstValue);

    // Expected: 7
    WriteLn('SecondValue = ', SecondValue);

    TestLocal;
end.
