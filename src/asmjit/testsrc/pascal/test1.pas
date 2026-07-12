// ---------------------------------------------------------------------------
// File:   test1.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

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
