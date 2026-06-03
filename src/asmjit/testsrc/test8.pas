program test8;

var
  x: Integer;

begin
    for x := 0 to 5 do
        WriteLn('x = ', x);

    for x := 5 downto 0 do
        WriteLn('x = ', x);
end.
