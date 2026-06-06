// ---------------------------------------------------------------------------
// \file error.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

using namespace std;

extern "C" void jit_array_bounds_error(
    const char* array_name,
    int index,
    int min_index,
    int max_index)
{
    std::cerr
        << "Runtime error: array index out of bounds: "
        << array_name
        << "["
        << index
        << "] allowed range "
        << min_index
        << ".."
        << max_index
        << std::endl;

    std::exit(1);
}
