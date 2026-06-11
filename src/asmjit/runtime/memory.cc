// ---------------------------------------------------------------------------
// \file memory.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

static bool is_probably_dynstring(const char* data)
{
    if (!data)
        return false;

    const DynStringHeader* h = ((const DynStringHeader*)data) - 1;
    return h->length < 1024 * 1024;
}

static bool is_dynstring(const char* data)
{
    if (!data)
        return false;

    const DynStringHeader* h = ((const DynStringHeader*)data) - 1;
    return h->magic == DYNSTRING_MAGIC;
}

static uint64_t
dynstring_length_strict(
    const char* data) {
    
    if (!data)
        return 0;

    const DynStringHeader* h = ((const DynStringHeader*)data) - 1;

    if (h->magic != DYNSTRING_MAGIC)
        throw JitRuntimeError("Invalid dynamic string");

    return h->length;
}

static uint64_t string_length_mixed(
    const char* data) {
    
    if (!data)
        return 0;

    if (is_dynstring(data)) {
        const DynStringHeader* h = ((const DynStringHeader*)data) - 1;
        return h->length;
    }

    return (uint64_t)std::strlen(data);
}

DLL_API void*
_jit_new_memory(uint64_t size)
{
    void* p = std::malloc(size);

    if (!p) {
        throw JitRuntimeError("Out of memory in New()");
    }

    std::memset(p, 0, size);
    return p;
}

DLL_API void
_jit_dispose_memory(void* p) {
    if (p) {
        std::free(p);
    }
}

DLL_API void *
_jit_setlength_memory(
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
_jit_dynarray_setlength(
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
        throw JitRuntimeError("Out of memory in SetLength(array)");
    }

    new_header->length = length;
    new_header->element_size = element_size;

    return (void*)(new_header + 1);
}

DLL_API void *
_jit_dynstring_setlength(
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
    
    h->magic    = DYNSTRING_MAGIC;
    h->length   = new_length;
    
    char * data = (char*)(h + 1);
    
    // neuen Bereich sauber mit 0 füllen
    if (new_length > old_length) {
        std::memset(data + old_length, 0, new_length - old_length);
    }

    // C-String-Terminator
    data[new_length] = 0;

    return data;
}

DLL_API int
_jit_dynstring_length(const char* data)
{    
    if (!data)
        return 0;

    const DynStringHeader* h = ((const DynStringHeader*)data) - 1;
    return (int)h->length;
}

DLL_API char*
_jit_dynstring_concat(
    const char* left,
    const char* right)
{
    uint64_t len_left  = dynstring_length_strict(left);
    uint64_t len_right = dynstring_length_strict(right);
    uint64_t new_len   = len_left + len_right;

    DynStringHeader* h = (DynStringHeader*)std::malloc(
        sizeof(DynStringHeader) + new_len + 1
    );

    if (!h)
        throw JitRuntimeError("Out of memory in string concat");

    h->magic    = DYNSTRING_MAGIC;
    h->reserved = 0;
    h->length   = new_len;

    char* data = (char*)(h + 1);

    if (left)
        std::memcpy(data, left, len_left);

    if (right)
        std::memcpy(data + len_left, right, len_right);

    data[new_len] = 0;

    return data;
}

DLL_API char*
_jit_dynstring_from_cstr(
    const char* text) {
    
    if (!text)
        text = "";

    uint64_t len = (uint64_t)std::strlen(text);

    DynStringHeader* h =
        (DynStringHeader*)std::malloc(sizeof(DynStringHeader) + len + 1);

    if (!h)
        throw JitRuntimeError("Out of memory in string literal");

    h->magic    = DYNSTRING_MAGIC;
    h->reserved = 0;
    h->length   = len;

    char* data = (char*)(h + 1);

    std::memcpy(data, text, len);
    data[len] = 0;

    return data;
}
