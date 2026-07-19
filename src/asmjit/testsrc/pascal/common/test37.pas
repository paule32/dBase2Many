// ---------------------------------------------------------------------------
// File:   test37.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test37;

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

procedure InsertAfter(var Head: PNode; AfterValue: Integer; NewValue: Integer);
var
    p : PNode;
    n : PNode;
begin
    p := Head;

    while p <> nil do
    begin
        if p^.Value = AfterValue then
        begin
            New(n);

            n^.Value := NewValue;
            n^.Next  := p^.Next;
            p^.Next  := n;

            Exit;
        end;

        p := p^.Next;
    end;
end;

begin
    Head := nil;

    Push(Head, 10);
    Push(Head, 20);
    Push(Head, 30);

    InsertAfter(Head, 20, 25);

    p := Head;

    while p <> nil do
    begin
        WriteLn(p^.Value);
        p := p^.Next;
    end;
end.
