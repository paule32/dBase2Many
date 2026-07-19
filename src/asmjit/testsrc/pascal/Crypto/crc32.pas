// ---------------------------------------------------------------------------
// File:   crc32.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program crc32;
uses Crypto.crc32;

begin
    WriteLn(crypt('bbc', 3));
end.
