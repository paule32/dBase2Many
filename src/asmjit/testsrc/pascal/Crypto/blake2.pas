// ---------------------------------------------------------------------------
// File:   blake2.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program blake2;
uses Crypto.blake2;

begin
    WriteLn(crypt('bbc', 3));
end.
