// ---------------------------------------------------------------------------
// File:   test28.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test28;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    n1 : PNode;
    n2 : PNode;

begin
    New(n1);
    New(n2);

    n1^.Value := 10;
    n2^.Value := 20;

    n1^.Next := n2;
    n2^.Next := 0;

    WriteLn(n1^.Value);
    WriteLn(n1^.Next^.Value);

    Dispose(n2);
    Dispose(n1);
end.
