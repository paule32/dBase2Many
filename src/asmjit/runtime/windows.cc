// ---------------------------------------------------------------------------
// \file error.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------

# include "dbase2many.hpp"

DLL_API VOID
_jit_ExitProcess(UINT uExitCode) {
    ExitProcess(uExitCode);
}


