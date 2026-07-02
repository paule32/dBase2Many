// ---------------------------------------------------------------------------
// File: memory.h
// Note: Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
#ifndef __DBASE2MANY_MEMORY_H__
#define __DBASE2MANY_MEMORY_H__

# pragma once
# include "stddef.h"
# include "exception.h"

extern "C" {

typedef void * (JIT_CDECL *malloc_fn)(size_t size);
typedef void * (JIT_CDECL *realloc_fn)(void *ptr, size_t size);
typedef void   (JIT_CDECL *free_fn)(JitJumpBuffer *ptr);

typedef void * (JIT_CDECL *memcpy_fn )(void* dest, const void* src, size_t count);
typedef void * (JIT_CDECL *memset_fn )(void* dest, int value, size_t count);
typedef int    (JIT_CDECL *memcmp_fn )(void* buf1, void* buf2, size_t count);
typedef void * (JIT_CDECL *memmove_fn)(void* dest, const void* src, size_t count);

DLL_API void * _jit_malloc(unsigned int size);
DLL_API void * _jit_realloc(void *ptr, unsigned int new_size);
DLL_API void   _jit_free(void *ptr);

DLL_API void * _jit_memcpy (void* dest, const void *src, size_t count);
DLL_API void * _jit_memset (void* dest, int value, size_t count);
DLL_API int    _jit_memcmp (void* buf1, void* buf2, size_t count);
DLL_API void * _jit_memmove(void* dest, const void* src, size_t count);

DLL_API int  __jit_setjmp (JitJumpBuffer *env) ;
DLL_API int   _jit_setjmp (JitJumpBuffer *env) ;

DLL_API VOID  _jit_longjmp(JitJumpBuffer *env, int value);
DLL_API VOID __jit_longjmp(JitJumpBuffer *env, int value);

};

# endif
