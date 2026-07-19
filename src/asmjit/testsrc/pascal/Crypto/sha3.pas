// ---------------------------------------------------------------------------
// File:   sha3.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program sha3;
uses Crypto.sha3;

begin
    WriteLn(sha3('bbc', 3));
end.
