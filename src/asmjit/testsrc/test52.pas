// ---------------------------------------------------------------------------
// File:   test52.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------

program test52;

type
    PNode = ^TNode;

    TNode = record
        Value : Integer;
        Next  : PNode;
    end;

var
    p : PNode;

begin
    p := nil;

    if Assigned(p) and (p^.Value = 10) then
        WriteLn('Fehler')
    else
        WriteLn('OK');
end.
