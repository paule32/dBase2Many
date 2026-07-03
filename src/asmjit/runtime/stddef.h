// ---------------------------------------------------------------------------
// File: stddef.h
// Note: Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
#ifndef __DBASE2MANY_STDDEF_HH__
#define __DBASE2MANY_STDDEF_HH__

# pragma once

// ---------------------------------------------------------------------------
// mingw32 alternative to MS Visual C++ Studio ...
// ---------------------------------------------------------------------------
# ifdef _MSC_VER
# define JIT_CDECL    __cdecl
# define JIT_STDCALL  __stdcall
# define JIT_FASTCALL __fastcall
# elif defined(__GNUC__)
#   if defined(__i386__)
#      define JIT_CDECL    __attribute__((cdecl))
#      define JIT_STDCALL  __attribute__((stdcall))
#      define JIT_FASTCALL __attribute__((fastcall))
#   else
#      define JIT_CDECL
#      define JIT_STDCALL
#      define JIT_FASTCALL
#   endif
# else
# define JIT_CDECL
# define JIT_STDCALL
# define JIT_FASTCALL
# endif

// ---------------------------------------------------------------------------
// dll export/import members for use DLL ...
// ---------------------------------------------------------------------------
# ifdef DLL_BUILD
# define DLL_API __declspec(dllexport)
# else
# define DLL_API __declspec(dllimport)
# endif

// ---------------------------------------------------------------------------
// atomic constant's ...
// ---------------------------------------------------------------------------
constexpr int TRUE  = 1;
constexpr int FALSE = 0;

// ---------------------------------------------------------------------------
// platform independent type definition's ...
// ---------------------------------------------------------------------------
typedef unsigned char        uint8_t;
typedef signed char           int8_t;

typedef unsigned short      uint16_t;
typedef short                int16_t;

typedef unsigned int        uint32_t;
typedef   signed int         int32_t;

typedef unsigned long long  uint64_t;
typedef signed   long long   int64_t;

typedef uint32_t size_t;

// ---------------------------------------------------------------------------
// widely used Windows 32-bit used type definition's ...
// ---------------------------------------------------------------------------
typedef int                 BOOL;
typedef void                VOID;
typedef void *              PVOID;
typedef PVOID               LPVOID;
typedef long                LONG;
typedef LONG       *        PLONG;
typedef LONG       *        LPLONG;
typedef int                 BOOL;
typedef unsigned char       BYTE;
typedef unsigned short      WORD;
typedef unsigned long       DWORD;
typedef unsigned long long  ULONGLONG;
typedef unsigned int        UINT;
typedef DWORD      *        LPDWORD;
typedef PVOID               HMODULE;
typedef PVOID               HANDLE;
typedef       char *        LPSTR;
typedef const char *        LPCSTR;
typedef void       *        HINSTANCE;

typedef VOID (*FARPROC)(VOID);

// ---------------------------------------------------------------------------
// asmjit context for various structures ...
// ---------------------------------------------------------------------------
struct JitContext {
    int         *  int_vars;

    double      *  double_vars;
    char        ** string_vars;
    uint8_t     *  record_vars;
    uint8_t     *  arrays_vars;
    uint64_t    *  pointr_vars;

    int            print_int_tmp;
    double         print_double_tmp;

    int            exception_active;
    const char  *  exception_message;
};

typedef void (*JitFunc)(JitContext* ctx);

// ---------------------------------------------------------------------------
// build 64-bit arith for 32-bit systems through two long types ...
// ---------------------------------------------------------------------------
typedef union _ULARGE_INTEGER {
    struct {
        DWORD LowPart;
        DWORD HighPart;
    };
    ULONGLONG QuadPart;
}   ULARGE_INTEGER, *PULARGE_INTEGER;

#endif
