// ---------------------------------------------------------------------------
// \file print.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

void jit_print_text(const char* s)  { std::cout << s; }
void jit_print_int(int v)           { std::cout << v; }
void jit_print_double(double v)     { std::cout << v; }
void jit_print_newline()            { std::cout << std::endl; }
void jit_print_char(int c)          { std::cout << static_cast<char>(c); }
