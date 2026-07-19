// ---------------------------------------------------------------------------
// File:   Crypto.crc32c.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
{$L crc32c.o}
unit Crypto.crc32c;
interface
uses System.Types;

function crypt(S: String; Len: Integer): String; cdecl;

implementation

function _jit_crc32c(S: String; Len: Integer): String; cdecl; external;
function crypt(S: String; Len: Integer): String; cdecl;
begin
    result := _jit_crc32c(S, Len);
end;

end.
