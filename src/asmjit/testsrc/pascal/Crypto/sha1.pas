// ---------------------------------------------------------------------------
// File:   sha1.pas
// Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
program sha1;
uses Crypto.sha1;

begin
    WriteLn(sha1('bbc', 3));
end.
