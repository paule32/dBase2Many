// ---------------------------------------------------------------------------
// File:   test7.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

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
