// ---------------------------------------------------------------------------
// File:   test32.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test32;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    Head : PNode;
    p    : PNode;

procedure Push(Value: Integer);
var
    n : PNode;
begin
    New(n);

    n^.Value := Value;
    n^.Next  := Head;

    Head := n;
end;

begin
    Head := nil;

    Push(10);
    Push(20);
    Push(30);

    p := Head;

    while p <> nil do
    begin
        WriteLn(p^.Value);
        p := p^.Next;
    end;
end.
