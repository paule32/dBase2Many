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

extern "C" void *
jit_dynstring_setlength(
    void *   data,
    uint64_t length) {

    size_t total = sizeof(DynStringHeader) + length + 1;

    DynStringHeader* header = nullptr;

    if (data) {
        header = ((DynStringHeader*)data) - 1;
    }

    DynStringHeader* h = (DynStringHeader*)realloc(header, total);
    if (!h) return nullptr;

    h->length     = length;
    h->capacity   = length;

    char*  _data  = (char*)(h + 1);
    _data[length] = 0;

    return _data;
}
