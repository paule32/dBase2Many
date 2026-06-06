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

void jit_print_text(const char* s);
void jit_print_int(int v);
void jit_print_double(double v);
void jit_print_newline();

void jit_array_bounds_error(
    const char* array_name,
    int index,
    int min_index,
    int max_index);

// ---------------------------------------------------------------------------
// end of C section
// ---------------------------------------------------------------------------
# ifdef __cplusplus
};
# endif

// ---------------------------------------------------------------------------
// asmjit context for various structures ...
// ---------------------------------------------------------------------------
struct JitContext {
    int        *    int_vars;

    double     *    double_vars;
    const char **   string_vars;
    uint8_t    *    record_vars;
    uint8_t    *    arrays_vars;
    uint64_t   *    pointr_vars;

    int             print_int_tmp;
    double          print_double_tmp;
};

typedef void (*JitFunc)(JitContext* ctx);

// ---------------------------------------------------------------------------
// misc. C++ helper members ..
// ---------------------------------------------------------------------------
uint64_t double_to_bits(double value);

void
replace_all(
          std::string& s,
    const std::string& from,
    const std::string& to);

std::string& replace_all_ptr(std::string& asm_text);
std::string& replace_all_fun(std::string& asm_text);
void         replace_all_str(std::string& asm_text , std::ofstream& asm_out);

#endif  // __DBASE2MANY_HPP__
