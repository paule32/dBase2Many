// ---------------------------------------------------------------------------
// File:   sha224.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program sha224;
uses Crypto.sha224;

begin
    WriteLn(sha224('bbc', 3));
end.
