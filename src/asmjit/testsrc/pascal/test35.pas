// ---------------------------------------------------------------------------
// File:   test35.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test35;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    Head : PNode;
    p    : PNode;

procedure Push(var Head: PNode; Value: Integer);
var
    n : PNode;
begin
    New(n);

    n^.Value := Value;
    n^.Next  := Head;

    Head := n;
end;

procedure Pop(var Head: PNode);
var
    tmp : PNode;
begin
    if Head = nil then
        Exit;

    tmp  := Head;
    Head := Head^.Next;

    Dispose(tmp);
end;

begin
    Head := nil;

    Push(Head, 10);
    Push(Head, 20);
    Push(Head, 30);

    Pop(Head);

    p := Head;

    while p <> nil do
    begin
        WriteLn(p^.Value);
        p := p^.Next;
    end;
end.
