// ---------------------------------------------------------------------------
// \file memory.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

DLL_API void*
jit_new_memory(uint64_t size)
{
    void* p = std::malloc(size);
    if (p) {
        std::memset(p, 0, size);
    }
    return p;
}

DLL_API void
jit_dispose_memory(void* p) {
    if (p) {
        std::free(p);
    }
}

DLL_API void *
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

DLL_API void *
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

DLL_API void *
jit_dynstring_setlength(
    void *   old_data,
    uint64_t new_length) {

    uint64_t old_length = 0;
    
    DynStringHeader* old_header = nullptr;
    
    if (old_data) {
        old_header = ((DynStringHeader*)old_data) - 1;
        old_length = old_header->length;
    }
    
    size_t total = sizeof(DynStringHeader) + new_length + 1;
    
    DynStringHeader* h = (DynStringHeader*)realloc(old_header, total);
    if (!h) {
        throw JitRuntimeError("Out of memory in SetLength(string)");
    }
    
    h->length   = new_length;
    h->capacity = new_length;
    
    char*  data = (char*)(h + 1);
    
    // neuen Bereich sauber mit 0 füllen
    if (new_length > old_length) {
        std::memset(data + old_length, 0, new_length - old_length);
    }

    // C-String-Terminator
    data[new_length] = 0;

    return data;
}
