// ---------------------------------------------------------------------------
// \file print.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "iostream.h"
# include "stddef.h"

DLL_API void _jit_print_text(const char* s)  { std::cout << s; }
DLL_API void _jit_print_int(int v)           { std::cout << v; }
DLL_API void _jit_print_double(double v)     { std::cout << v; }
DLL_API void _jit_print_newline()            { std::cout << std::endl; }
DLL_API void _jit_print_char(int c)          { std::cout << static_cast<char>(c); }

DLL_API int  _jit_snprintf(
    char *buffer,
    size_t size,
    const char *fmt,
    ...)
{
    va_list ap;
    int result;

    va_start(ap, fmt);

    result = _jit_vsnprintf(
        buffer,
        size,
        fmt,
        ap);

    va_end(ap);

    return result;
}

#if 0
DLL_API char *
_jit_dynstring_copy(
    char* src,
    int start,
    int count) {
    
    if (!src)
        return _jit_dynstring_from_cstr("");

    DynStringHeader* h = (DynStringHeader*)(src - sizeof(DynStringHeader));

    if (h->magic != DYNSTRING_MAGIC)
        throw JitRuntimeError("Invalid dynamic string");

    int len = (int)h->length;

    // Pascal: Strings sind 1-basiert
    if (start < 1)
        start = 1;

    if (count < 0)
        count = 0;

    if (start > len)
        return _jit_dynstring_from_cstr("");

    int zero_index = start - 1;

    if (zero_index + count > len)
        count = len - zero_index;

    char* result = (char*)std::malloc(sizeof(DynStringHeader) + count + 1);

    if (!result) {
        throw JitRuntimeError("Out of memory in dynstring_copy");
    }

    DynStringHeader* rh = (DynStringHeader*)result;
    rh->magic    = DYNSTRING_MAGIC;
    rh->reserved = 0;
    rh->length   = count;

    char* data = result + sizeof(DynStringHeader);

    memcpy(data, src + zero_index, count);
    data[count] = 0;

    return data;
}

DLL_API int
_jit_dynstring_pos(
    char* needle,
    char* haystack)
{
    if (!needle || !haystack)
        return 0;

    DynStringHeader* nh = (DynStringHeader*)(needle   - sizeof(DynStringHeader));
    DynStringHeader* hh = (DynStringHeader*)(haystack - sizeof(DynStringHeader));

    if (nh->magic != DYNSTRING_MAGIC)
        throw JitRuntimeError("Invalid search string");

    if (hh->magic != DYNSTRING_MAGIC)
        throw JitRuntimeError("Invalid source string");

    int nlen = (int)nh->length;
    int hlen = (int)hh->length;

    if (nlen <= 0)
        return 0;

    if (nlen > hlen)
        return 0;

    for (int i = 0; i <= hlen - nlen; i++)
    {
        if (memcmp(haystack + i, needle, nlen) == 0)
            return i + 1;   // Pascal: 1-basiert
    }

    return 0;
}
#endif
