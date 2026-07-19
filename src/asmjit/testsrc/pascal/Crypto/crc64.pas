// ---------------------------------------------------------------------------
// File:   crc64.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program crc64;
uses Crypto.crc64;

begin
    WriteLn(crc64('bbc', 3));
end.
