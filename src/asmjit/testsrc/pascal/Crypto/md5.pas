// ---------------------------------------------------------------------------
// File:   md5.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program md5;
uses Crypto.md5;

begin
    WriteLn(md5('bbc', 3));
end.
