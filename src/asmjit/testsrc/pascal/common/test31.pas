// ---------------------------------------------------------------------------
// File:   test31.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test31;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    n1, n2, n3 : PNode;
    p          : PNode;

begin
    New(n1);
    New(n2);
    New(n3);

    n1^.Value := 10;
    n2^.Value := 20;
    n3^.Value := 30;

    n1^.Next := n2;
    n2^.Next := n3;
    n3^.Next := nil;

    p := n1;

    while p <> nil do
    begin
        WriteLn(p^.Value);
        p := p^.Next;
    end;

    Dispose(n3);
    Dispose(n2);
    Dispose(n1);
end.
