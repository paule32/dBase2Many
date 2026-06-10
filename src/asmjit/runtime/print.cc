// ---------------------------------------------------------------------------
// \file print.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

DLL_API void _jit_print_text(const char* s)  { std::cout << s; }
DLL_API void _jit_print_int(int v)           { std::cout << v; }
DLL_API void _jit_print_double(double v)     { std::cout << v; }
DLL_API void _jit_print_newline()            { std::cout << std::endl; }
DLL_API void _jit_print_char(int c)          { std::cout << static_cast<char>(c); }
