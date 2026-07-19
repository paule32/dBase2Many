// ---------------------------------------------------------------------------
// File:   test46.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test46;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    P : PNode;

begin
    P := nil;

    WriteLn('Before nil access');

    P^.Value := 123;

    WriteLn('After nil access');
end.
