// ---------------------------------------------------------------------------
// \file memory.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

extern "C" void*
jit_new_memory(uint64_t size)
{
    void* p = std::malloc(size);
    if (p) {
        std::memset(p, 0, size);
    }
    return p;
}

extern "C" void
jit_dispose_memory(void* p) {
    if (p) {
        std::free(p);
    }
}
