// ---------------------------------------------------------------------------
// \file print.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "iostream.h"
# include "stddef.h"
# include "memory.h"
# include "string.h"
# include "exception.h"
# include "windows.h"

extern "C" {
//DLL_API void _jit_print_text(const char* s)  { std::cout << s; }
//DLL_API void _jit_print_int(int v)           { std::cout << v; }
//DLL_API void _jit_print_double(double v)     { std::cout << v; }
DLL_API void _jit_print_newline()            { _jit_print_text("\n"); }
//DLL_API void _jit_print_char(int c)          { std::cout << static_cast<char>(c); }

unsigned int utoa10(unsigned int value, char *buffer)
{
    char tmp[16];
    unsigned int len = 0;

    do {
        tmp[len++] = '0' + (value % 10);
        value /= 10;
    }   while (value);

    for (unsigned int i = 0; i < len; i++)
    buffer[i  ] = tmp[len - i - 1];
    buffer[len] = 0;

    return len;
}

unsigned int itoa10(int value, char *buffer)
{
    unsigned int pos = 0;

    if (value < 0) {
        buffer[pos++] = '-';
        value = -value;
    }

    return pos + utoa10((unsigned int)value, buffer + pos);
}

DLL_API VOID _jit_print_char(int ch)
{
    DWORD  written;
    HANDLE h = p_GetStdHandle(STD_OUTPUT_HANDLE);
    p_WriteFile(h, &ch, 1, &written, 0);
}

DLL_API VOID _jit_print_double(double value)
{
    if (value < 0.0) {
        _jit_print_text("-");
        value = -value;
    }

    int integer = (int)value;
    double frac = value - integer;
    HANDLE    h = p_GetStdHandle(STD_OUTPUT_HANDLE);

    _jit_print_int(integer);
    _jit_print_text(".");

    for (int i = 0; i < 6; i++) {
        frac     *= 10.0;
        int digit = (int)frac;
        char c    = '0' + digit;

        DWORD written;
        p_WriteFile(h, &c, 1, &written, nullptr);
        frac -= digit;
    }
}

DLL_API VOID _jit_print_int(int value)
{
    char buffer[16];
    DWORD written;

    unsigned int len = itoa10(value, buffer);
    HANDLE   h = p_GetStdHandle(STD_OUTPUT_HANDLE);

    p_WriteFile(h, buffer, len, &written, 0);
    //ExitProcess(1);
}

DLL_API char *
_jit_dynstring_copy(
    char* src,
    int start,
    int count) {
    
    //if (!src)
    //    return _jit_dynstring_from_cstr("");

    DynStringHeader* h = (DynStringHeader*)(src - sizeof(DynStringHeader));

    if (h->magic != DYNSTRING_MAGIC)
        _jit_raise(
            JIT_RUNTIME_ERROR,
            "Invalid dynamic string"
        );

    int len = (int)h->length;

    // Pascal: Strings sind 1-basiert
    if (start < 1)
        start = 1;

    if (count < 0)
        count = 0;

    //if (start > len)
    //    return _jit_dynstring_from_cstr("");

    int zero_index = start - 1;

    if (zero_index + count > len)
        count = len - zero_index;

    char* result = (char*)_jit_malloc(sizeof(DynStringHeader) + count + 1);

    if (!result) {
        _jit_raise(
            JIT_RUNTIME_ERROR,
            "Out of memory in dynstring_copy"
        );
    }

    DynStringHeader* rh = (DynStringHeader*)result;
    rh->magic    = DYNSTRING_MAGIC;
    rh->reserved = 0;
    rh->length   = count;

    char* data = result + sizeof(DynStringHeader);

    _jit_memcpy(data, src + zero_index, count);
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
        _jit_raise(
            JIT_RUNTIME_ERROR,
            "Invalid search string"
        );

    if (hh->magic != DYNSTRING_MAGIC)
        _jit_raise(
            JIT_RUNTIME_ERROR,
            "Invalid source string"
        );

    int nlen = (int)nh->length;
    int hlen = (int)hh->length;

    if (nlen <= 0)
        return 0;

    if (nlen > hlen)
        return 0;

    for (int i = 0; i <= hlen - nlen; i++)
    {
        if (_jit_memcmp(haystack + i, needle, nlen) == 0)
            return i + 1;   // Pascal: 1-basiert
    }

    return 0;
}

};
