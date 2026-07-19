// ---------------------------------------------------------------------------
// File:   sha512.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program sha512;
uses Crypto.sha512;

begin
    WriteLn(sha512('bbc', 3));
end.
