// ---------------------------------------------------------------------------
// File:   crc16.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program crc16;
uses Crypto.crc16;

begin
    WriteLn(crypt('bbc', 3));
end.
