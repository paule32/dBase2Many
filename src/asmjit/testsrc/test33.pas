// ---------------------------------------------------------------------------
// File:   test33.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test33;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    Head : PNode;
    p    : PNode;

procedure Push(var ListHead: PNode; Value: Integer);
var
    n : PNode;
begin
    New(n);

    n^.Value := Value;
    n^.Next  := ListHead;

    ListHead := n;
end;

begin
    Head := nil;

    Push(Head, 10);
    Push(Head, 20);
    Push(Head, 30);

    p := Head;

    while p <> nil do
    begin
        WriteLn(p^.Value);
        p := p^.Next;
    end;
end.
