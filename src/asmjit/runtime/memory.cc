// ---------------------------------------------------------------------------
// \file memory.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "iostream.h"
# include "stddef.h"
# include "string.h"
# include "memory.h"
# include "windows.h"

static malloc_fn    p_malloc    = nullptr;
static realloc_fn   p_realloc   = nullptr;
static free_fn      p_free      = nullptr;

static memcpy_fn    p_memcpy    = nullptr;
static memset_fn    p_memset    = nullptr;
static memcmp_fn    p_memcmp    = nullptr;
static memmove_fn   p_memmove   = nullptr;

static vprintf_fn   p_vprintf   = nullptr;
static printf_fn    p_printf    = nullptr;

//static snprintf_fn  p_snprintf  = nullptr;
static vsnprintf_fn p_vsnprintf = nullptr;

// ---------------------------------------------------------------------------
// msvcrt.dll imports ...
// ---------------------------------------------------------------------------
struct CRTImport {
    const char* name;
    void**      target;
};
CRTImport crt_imports[] = {
    { "malloc",    (void**)&p_malloc     },
    { "realloc",   (void**)&p_realloc    },
    { "free",      (void**)&p_free       },

    { "memcpy",    (void**)&p_memcpy     },
    { "memset",    (void**)&p_memset     },
    { "memcmp",    (void**)&p_memcmp     },
    { "memmove",   (void**)&p_memmove    },

    { "printf",    (void**)&p_printf     },
    { "vprintf",   (void**)&p_vprintf    },
    
    //{ "snprintf",  (void**)&p_snprintf   },
    { "vsnprintf", (void**)&p_vsnprintf  },
};

// ---------------------------------------------------------------------------
// kernel32.dll imports ...
// ---------------------------------------------------------------------------
struct KERNEL32Import {
    const char* name;
    void**      target;
};
KERNEL32Import kernel32_imports[] = {
    { "ExitProcess",            (void**)&p_ExitProcess},
    { "GetDriveTypeA",          (void**)&p_GetDriveTypeA},
    { "GetVolumeInformationA",  (void**)&p_GetVolumeInformationA},
};

// ---------------------------------------------------------------------------
// user32.dll imports ...
// ---------------------------------------------------------------------------
struct USER32Import {
    const char* name;
    void**      target;
};
USER32Import user32_imports[] = {
    { "MessageBoxA",     (void**)&p_MessageBoxA  },
};

// ---------------------------------------------------------------------------
// mpr.dll imports ...
// ---------------------------------------------------------------------------
struct MPRImport {
    const char* name;
    void**      target;
};
MPRImport mpr_imports[] = {
    { "WNetGetConnectionA", (void**)&p_WNetGetConnectionA},
};

static int init_msvcrt(void)
{
    HMODULE h1, h2, h3, h4;
    bool ok = true;

    if (p_malloc && p_free) {
        return 1;
    }
    
    // msvcrt.dll
    ok = true;
    h1 = p_LoadLibraryA("msvcrt.dll");
    if (!h1) {
        p_MessageBoxA(0,
            "Error",
            "Error: msvcrt.dll could not load.",
            0);
        return 0;
    }
    
    for (int i = 0; i < sizeof(crt_imports) / sizeof(crt_imports[0]); ++i) {
        *crt_imports[i].target = (void*)p_GetProcAddress(h1, crt_imports[i].name);
        
        if (!*crt_imports[i].target) {
            std::cout << crt_imports[i].name << " ";
            ok = false;
        }
    }
    
    // kernel32t.dll
    ok = true;
    h2 = LoadLibraryA("kernel32.dll");
    if (!h2) {
        MessageBoxA(0,
            "Error",
            "Error: kernel32.dll could not load.",
            0);
        return 0;
    }
    
    for (int i = 0; i < sizeof(kernel32_imports) / sizeof(kernel32_imports[0]); ++i) {
        *kernel32_imports[i].target = (void*)GetProcAddress(h2, kernel32_imports[i].name);
        
        if (!*kernel32_imports[i].target) {
            std::cout << kernel32_imports[i].name << " ";
            ok = false;
        }
    }
    if (!ok) {
        std::cout << "== null" << std::endl;
        return 0;
    }
    
    // user32.dll
    ok = true;
    h3 = LoadLibraryA("user32.dll");
    if (!h3) {
        MessageBoxA(0,
            "Error",
            "Error: user32.dll could not load.",
            0);
        return 0;
    }
    
    for (int i = 0; i < sizeof(user32_imports) / sizeof(user32_imports[0]); ++i) {
        *user32_imports[i].target = (void*)GetProcAddress(h3, user32_imports[i].name);
        
        if (!*user32_imports[i].target) {
            std::cout << user32_imports[i].name << " ";
            ok = false;
        }
    }
    
    // user32.dll
    ok = true;
    h4 = LoadLibraryA("mpr.dll");
    if (!h4) {
        MessageBoxA(0,
            "Error",
            "Error: mpr.dll could not load.",
            0);
        return 0;
    }
    
    for (int i = 0; i < sizeof(mpr_imports) / sizeof(mpr_imports[0]); ++i) {
        *mpr_imports[i].target = (void*)GetProcAddress(h4, mpr_imports[i].name);
        
        if (!*mpr_imports[i].target) {
            std::cout << mpr_imports[i].name << " ";
            ok = false;
        }
    }
    if (!ok) {
        std::cout << "== null" << std::endl;
        return 0;
    }   return 1;
}

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

    if (h->magic != DYNSTRING_MAGIC) {
        _jit_raise(
            JIT_INVALIDE,
            "Invalid dynamic string"
        );
    }

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

    return (uint64_t)_jit_strlen(data);
}
extern "C" {
    
/*
DLL_API void*
_jit_new_memory(uint32_t size)
{
    void* p = _jit_malloc(size);

    if (!p) {
        _jit_raise(
            JIT_OUT_OF_MEMORY,
            "Out of memory in New()"
        );
    }

    p_memset(p, 0, size);
    return p;
}*/

DLL_API void *
_jit_new_memory(uint32_t size)
{
    void *p = _jit_malloc(size);

    if (!p) {
        _jit_error_out_of_memory("Out of memory in New()");
        return 0;
    }

    _jit_memset(p, 0, size);
    return p;
}

DLL_API void
_jit_dispose_memory(void* p)
{
    if (!p) return;
    if (!p_free)  {
        if (!init_msvcrt())
            return;
    }

    p_free((JitJumpBuffer*)p);
}

DLL_API void *
_jit_setlength_memory(
    void *   old_ptr,
    uint64_t new_size)
{
    void* p = p_realloc(old_ptr, new_size);

    if (!p) {
        return nullptr;
    }

    return p;
}

DLL_API void *
_jit_dynarray_setlength(
    void *   data,
    uint32_t length,
    uint32_t element_size) {
    
    DynArrayHeader* old_header = nullptr;

    if (data) {
        old_header = ((DynArrayHeader*)data) - 1;
    }

    uint32_t total_size =
        sizeof(DynArrayHeader) + length * element_size;

    DynArrayHeader* new_header =
        //(DynArrayHeader*)p_realloc(old_header, total_size);
        (DynArrayHeader*)_jit_malloc(total_size);

    if (!new_header) {
        _jit_raise(
            JIT_OUT_OF_MEMORY,
            "Out of memory in SetLength(array)"
        );
    }

    new_header->length = length;
    new_header->element_size = element_size;

    return (void*)(new_header + 1);
}

DLL_API void *
_jit_dynstring_setlength(
    void *   old_data,
    uint32_t new_length) {

    if (!new_length) {
        _jit_raise(
            JIT_RUNTIME_ERROR,
            "negative index value not allowed for dynstring."
        );
    }

    DynStringHeader* old_header = nullptr;
    DynStringHeader* new_header = nullptr;

    if (old_data) {
        old_header = ((DynStringHeader*)old_data);
        new_header =  (DynStringHeader*)_jit_malloc(sizeof(DynStringHeader));
        new_header->magic = DYNSTRING_MAGIC;
        
        if (new_length > old_header->length) {
            new_header->data   = (char*)_jit_realloc(old_header->data, new_length);
            if (!new_header->data)
                _jit_raise(
                JIT_RUNTIME_ERROR,
                "dynstring header memory error."
                );
            new_header->length = new_length;
            
            _jit_memset(new_header->data, 0, new_length - 1);
            _jit_memcpy(new_header->data, old_header->data, old_header->length);
        }
        else if (new_length < old_header->length) {
            new_header->data   = (char*)_jit_realloc(old_header->data, new_length);
            if (!new_header->data)
                _jit_raise(
                JIT_RUNTIME_ERROR,
                "dynstring header memory error."
                );
            new_header->length = new_length;
            
            _jit_memset(new_header->data, 0, new_length - 1);
            _jit_memcpy(new_header->data, old_header->data, new_length);
        }
    }
    else {
        old_header = ((DynStringHeader*)old_data);
        new_header = (DynStringHeader*)_jit_malloc(sizeof(DynStringHeader));
        new_header->magic  = DYNSTRING_MAGIC;
        
        new_header->data   = (char*)_jit_malloc(new_length);
        new_header->length = new_length;
        
        _jit_memset(new_header, 0, new_length - 1);
    }
    
    old_data = ((DynStringHeader*)new_header);

    return ((DynStringHeader*)new_header);
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

    DynStringHeader* h = (DynStringHeader*)_jit_malloc(
        sizeof(DynStringHeader) + new_len + 1
    );

    if (!h) {
        _jit_raise(
            JIT_OUT_OF_MEMORY,
            "Out of memory in string concat"
        );
    }

    h->magic    = DYNSTRING_MAGIC;
    h->reserved = 0;
    h->length   = new_len;

    char* data = (char*)(h + 1);

    if (left)
        _jit_memcpy(data, left, len_left);

    if (right)
        _jit_memcpy(data + len_left, right, len_right);

    data[new_len] = 0;

    return data;
}

DLL_API char*
_jit_dynstring_from_cstr(
    const char* text) {
    
    if (!text)
        text = "";

    uint64_t len = (uint64_t)_jit_strlen(text);

    DynStringHeader* h =
        (DynStringHeader*)_jit_malloc(sizeof(DynStringHeader) + len + 1);

    if (!h) {
        _jit_raise(
            JIT_OUT_OF_MEMORY,
            "Out of memory in string literal"
        );
    }

    h->magic    = DYNSTRING_MAGIC;
    h->reserved = 0;
    h->length   = len;

    char* data = (char*)(h + 1);

    _jit_memcpy(data, text, len);
    data[len] = 0;

    return data;
}

DLL_API void *
_jit_malloc(uint32_t size)
{
    if (!init_msvcrt()) {
        std::cout << "heap error" << std::endl;
        return nullptr;
    }

    return p_malloc(size);
}

DLL_API void *
_jit_realloc(void *ptr, unsigned int new_size) {
    return p_realloc(ptr, (size_t)new_size);
}

DLL_API void
_jit_free(void *ptr) {
    if (!ptr)
        return;

    if (!init_msvcrt())
        return;

    _jit_free(ptr);
}

DLL_API size_t
_jit_strlen(const char *s) {
    const char *p = s;

    if (!s) return 0;

    while (*p) ++p;
    return (size_t)(p - s);
}

DLL_API char *
_jit_strdup(const char *s) {
    char *p;
    unsigned int len;

    if (!s)
        s = "";

    if (!p_malloc || !p_memcpy) {
        if (!init_msvcrt())
            return nullptr;
    }
    
    len = (unsigned int)_jit_strlen(s);

    p = (char *)_jit_malloc(len + 1);
    if (!p)
        return nullptr;

    _jit_memcpy(p, s, len + 1);
    return p;
}

DLL_API void * _jit_memcpy (void* dest, const void *src, size_t count) { return p_memcpy (dest, src  , count); }
DLL_API void * _jit_memset (void* dest, int value, size_t count)       { return p_memset (dest, value, count); }
DLL_API void *      memset (void* dest, int value, size_t count)       { return p_memset (dest, value, count); }
DLL_API int    _jit_memcmp (void* buf1, void* buf2, size_t count)      { return p_memcmp (buf1, buf2 , count); }
DLL_API void * _jit_memmove(void* dest, const void* src, size_t count) { return p_memmove(dest, src  , count); }

DLL_API int  _jit_setjmp (JitJumpBuffer *env)            { return __jit_setjmp(env);         }
DLL_API VOID _jit_longjmp(JitJumpBuffer *env, int value) {        __jit_longjmp(env, value); }

DLL_API int  JIT_CDECL _jit_vprintf(const char *format, va_list args) {
    return p_vprintf(format, args);
}
DLL_API int  JIT_CDECL _jit_printf(const char *format, ...) {
    va_list args;
    int result;

    va_start(args, format);
    result = _jit_vprintf(format, args);
    va_end(args);

    return result;
}

DLL_API int JIT_CDECL _jit_vsnprintf(char *buffer, size_t size, const char *fmt, va_list arg) {
    return p_vsnprintf(buffer, size, fmt, arg);
}
DLL_API int JIT_CDECL _jit_snprintf (char *buffer, size_t size, const char *fmt, ...) {
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

DLL_API int  JIT_CDECL _jit_read_int()    { return 9; }
DLL_API int  JIT_CDECL _jit_read_string() { return 0; }
DLL_API void JIT_CDECL _jit_debug_break() { }
};
