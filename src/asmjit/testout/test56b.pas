// ---------------------------------------------------------------------------
// File:   test56b.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test56b;

{$mode objfpc}{$H+}

function Add(a, b: Integer): Integer; external 'test56.dll' name '_ADD$INTEGER$INTEGER';

begin
    WriteLn(Add(10, 20));
end.
