// ---------------------------------------------------------------------------
// File:   Windows.kernel.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit Windows.kernel;

interface
uses System;

const DLL_FILE = 'libruntime_mini.dll';

procedure ExitProcess(AValue: DWord); cdecl;
    external DLL_FILE name '_jit_ExitProcess'
    ordinal 75;

implementation

end.
