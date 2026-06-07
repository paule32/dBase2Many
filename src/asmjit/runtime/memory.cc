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

extern "C" void *
jit_setlength_memory(
    void *   old_ptr,
    uint64_t new_size)
{
    void* p = realloc(old_ptr, new_size);

    if (!p) {
        return nullptr;
    }

    return p;
}

extern "C" void *
jit_dynarray_setlength(
    void *   data,
    uint64_t length,
    uint64_t element_size) {
    
    DynArrayHeader* old_header = nullptr;

    if (data) {
        old_header = ((DynArrayHeader*)data) - 1;
    }

    uint64_t total_size =
        sizeof(DynArrayHeader) + length * element_size;

    DynArrayHeader* new_header =
        (DynArrayHeader*)realloc(old_header, total_size);

    if (!new_header) {
        return nullptr;
    }

    new_header->length = length;
    new_header->element_size = element_size;

    return (void*)(new_header + 1);
}
