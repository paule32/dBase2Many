// ---------------------------------------------------------------------------
// File:   test48.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test48;

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

    WriteLn('start');

    try
        WriteLn('before nil access');
        P^.Value := 123;
        WriteLn('after nil access');
    except
        WriteLn('except block');
    end;

    WriteLn('done');
end.
