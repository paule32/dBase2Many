// ---------------------------------------------------------------------------
// File:   testdisk.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program testdisk;

begin
    WriteLn('Free D: ', DiskFree  ('D'));
    WriteLn('Label : ', DiskLabel ('D'));
    WriteLn('Serial: ', DiskSerial('D'));
    WriteLn('Type  : ', DiskType  ('D'));
end.
