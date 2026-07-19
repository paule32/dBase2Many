// ---------------------------------------------------------------------------
// File:   sha384.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program sha384;
uses Crypto.sha384;

begin
    WriteLn(sha384('bbc', 3));
end.
