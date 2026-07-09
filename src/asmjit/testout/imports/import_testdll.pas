{$mode objfpc}{$H+}
unit import_testdll;

interface

const
  DLL_NAME = 'testdll.dll';

function Add(A: Integer; B: Integer): Integer; external DLL_NAME name '_ADD$INTEGER$INTEGER';

procedure TestString(S: AnsiString); external DLL_NAME name '_TESTSTRING$ANSISTRING';

implementation

begin
end.
