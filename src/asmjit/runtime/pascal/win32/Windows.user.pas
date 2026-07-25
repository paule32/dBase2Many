// ---------------------------------------------------------------------------
// File:   Windows.User.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit Windows.User;

interface
uses System.Types;

const DLL_FILE = 'libruntime_mini.dll';

function MessageBox(AHwnd: HANDLE; ATitle, AMessage: String; AFlag: DWORD): DWORD; cdecl;
    external DLL_FILE name 'MessageBoxA@16'
    ordinal 75;

implementation

end.
