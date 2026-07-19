// ---------------------------------------------------------------------------
// File:   test58.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program test58;
uses System.Types;

procedure PrintValues(
    const Prefix: String;
    const Values: array of const);
var
    I: Integer;
begin
    WriteLn(Prefix);

    for I := Low(Values) to High(Values) do
        WriteLn(Values[I]);
end;

var
    I: Integer;
    D: Double;
    S: String;
    B: Boolean;

begin
    I := 42;
    D := 12.5;
    S := 'Hallo';
    B := True;

    // Projekt-Erweiterung: skalarer Wert wird automatisch
    // als Variant-Array mit einem Element übergeben.
    PrintValues('Integer:', I);
    PrintValues('Double:',  D);
    PrintValues('String:',  S);
    PrintValues('Boolean:', B);

    // Standardnahe explizite Schreibweise mit gemischten Typen.
    PrintValues(
        'Gemischt:',
        [I, D, S, B, 'X']
    );
end.
