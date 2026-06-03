program test7;

var
  x: Integer;

begin
  x := 0;

  repeat
      WriteLn('x = ', x);
      x := x + 1;
  until x >= 5;
end.
