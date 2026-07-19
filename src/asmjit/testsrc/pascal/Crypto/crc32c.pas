// ---------------------------------------------------------------------------
// File:   crc32cpas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program crc32c;
uses Crypto.crc32c;

begin
    WriteLn(crc32c('bbc', 3));
end.
