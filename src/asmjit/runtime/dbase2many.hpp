// ---------------------------------------------------------------------------
// \file dbase2many.hpp
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
#ifndef __DBASE2MANY_HPP__
#define __DBASE2MANY_HPP__

#pragma once

// ---------------------------------------------------------------------------
// standard C++ header stuff ...
// ---------------------------------------------------------------------------
# include <cstdio>
# include <cstdint>
# include <cstring>

# include <iostream>
# include <fstream>
# include <sstream>

# include <stdexcept>
# include <string>
# include <array>
# include <vector>
# include <algorithm>

// ---------------------------------------------------------------------------
// custom C++ header stuff ...
// ---------------------------------------------------------------------------
# include <asmjit/x86.h>
# include "mapping.hpp"

// ---------------------------------------------------------------------------
// dll export/import members for use DLL ...
// ---------------------------------------------------------------------------
# ifdef DLL_EXPORT
# define DLL_API __declspec(dllexport)
# else
# define DLL_API __declspec(dllimport)
# endif

# define CALL __cdecl

// ---------------------------------------------------------------------------
// all members in this section are marked as C members - no mangled ...
// ---------------------------------------------------------------------------
# ifdef __cplusplus
extern "C"
{
# endif

DLL_API void  jit_print_text(const char* s);
DLL_API void  jit_print_int(int v);
DLL_API void  jit_print_double(double v);
DLL_API void  jit_print_newline();

DLL_API void* jit_setlength_memory(void* old_ptr,uint64_t new_size);

DLL_API void* jit_new_memory(uint64_t size);
DLL_API void  jit_dispose_memory(void* p);
DLL_API void  jit_print_char(int c);

DLL_API void  jit_string_range_error();
DLL_API void
jit_array_bounds_error(
    const char* array_name,
    int index,
    int min_value,
    int max_value);

DLL_API bool
write_formatted_asm_file(
    const char* asm_text,
    const char* file_name);
DLL_API bool
replace_all_str_c(
    const char* asm_text,
    const char* file_name);
// ---------------------------------------------------------------------------
// end of C section
// ---------------------------------------------------------------------------
# ifdef __cplusplus
};
# endif

// ---------------------------------------------------------------------------
// exception handling for our jit framework
// ---------------------------------------------------------------------------
class JitRuntimeError: public std::runtime_error {
public:
    explicit JitRuntimeError(const std::string& msg);
};

// ---------------------------------------------------------------------------
// asmjit context for various structures ...
// ---------------------------------------------------------------------------
struct JitContext {
    int        *    int_vars;

    double     *    double_vars;
    char       **   string_vars;
    uint8_t    *    record_vars;
    uint8_t    *    arrays_vars;
    uint64_t   *    pointr_vars;

    int             print_int_tmp;
    double          print_double_tmp;
};

typedef void (*JitFunc)(JitContext* ctx);

// ---------------------------------------------------------------------------
// dynamic array - SetLength ...
// ---------------------------------------------------------------------------
struct DynArrayHeader {
    uint64_t length;
    uint64_t element_size;
};

DLL_API void *
jit_dynarray_setlength(
    void *   data,
    uint64_t length,
    uint64_t element_size);

// ---------------------------------------------------------------------------
// dynamic string - SetLength ...
// ---------------------------------------------------------------------------
struct DynStringHeader {
    uint64_t length;
    uint64_t capacity;
};

DLL_API void *
jit_dynstring_setlength(
    void *   data,
    uint64_t length);
    
// ---------------------------------------------------------------------------
// misc. C++ helper members ..
// ---------------------------------------------------------------------------
uint64_t double_to_bits(double value);

DLL_API void
replace_all(
          std::string& s,
    const std::string& from,
    const std::string& to);

DLL_API std::string& replace_all_ptr(std::string& asm_text);
DLL_API std::string& replace_all_fun(std::string& asm_text);
DLL_API void         replace_all_str(std::string& asm_text , std::ofstream& asm_out);

#endif  // __DBASE2MANY_HPP__
