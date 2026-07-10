// ---------------------------------------------------------------------------
// File:   testtypes.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
{$info Compile time: {$__DATE__} at {$__TIME__}}
{$note File: {$__FILE__}, Line: {$__LINE__}}

{$define VERSION 3}
{$if VERSION >= 3}
    {$info Version fits into needs}
{$else}
    {$error Version does not fit into needs}
{$endif}

program testtypes;

uses System.Types;
    
var
    b : Boolean;
    c : Byte;
    w : Word;
    r : Real;
    e : Extended;
begin
    writeln('START: ', {$VERSION});
    b := False;
    c := 255;    writeln('B: OK');
    w := 65535;  writeln('W: OK');
    r := 3.14;   writeln('R: OK');
    e := 2.71;   writeln('E: OK');

    writeLn('b: ', b);
    writeLn('c: ', c);
    writeLn('w: ', w);
    writeLn('r: ', r);
    writeLn('e: ', e);
end.
