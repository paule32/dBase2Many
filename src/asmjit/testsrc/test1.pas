(**!
 * @file test1.pas
 *)
program Test1;
var
  i: Integer;
  d: Double;

begin
  i := 10;        // ok
  d := 10;        // ok
  d := 0.11;      // ok
  i := 0.11;      // error
  i := d;         // error
end.
