program test14;

function GetText: String;
begin
    Result := 'Hallo aus Function';
end;

begin
    WriteLn('Text: ', GetText());
end.
