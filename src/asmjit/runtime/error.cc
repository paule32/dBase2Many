// ---------------------------------------------------------------------------
// \file error.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

using namespace std;

JitRuntimeError::JitRuntimeError(
    const std::string& msg):
    std::runtime_error(msg)
    {}

extern "C" void jit_array_bounds_error(
    const char* array_name,
    int index,
    int min_value,
    int max_value) {
    
    throw JitRuntimeError(
        std::string("Array bounds error: ") +
        array_name + "[" +
        std::to_string(index) + "] allowed range " +
        std::to_string(min_value) + ".." +
        std::to_string(max_value)
    );
}

extern "C" void
jit_string_range_error() {
    throw JitRuntimeError("String range check error");
}
