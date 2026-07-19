// ---------------------------------------------------------------------------
// File:   sha256.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program sha256;
uses Crypto.sha256;

begin
    WriteLn(sha256('bbc', 3));
end.
