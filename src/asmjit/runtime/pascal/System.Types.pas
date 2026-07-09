// ---------------------------------------------------------------------------
// File:   System.Types.pas
// Author: (c) 2026 Jens Kallup - paule32
// All rights reserved
// ---------------------------------------------------------------------------
unit System.Types;

interface

type
    Boolean = 0..1;
    Byte    = 0..255;
    Word    = 0..65535;
    DWord   = 0..4294967295;
    
    ShortInt = -128..127;
    SmallInt = -32768..32767;
    Int32    = -2147483648..2147483647;
    
    UInt32   = DWord;
    LongInt  = Int32;
    
    Real     = Double;  // todo !!
    Extended = Double;  // todo !!

implementation

begin
end.
