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

DLL_API void
jit_array_bounds_error(
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

DLL_API void
jit_string_range_error() {
    throw JitRuntimeError("String range check error");
}

DLL_API void
jit_nil_pointer_error(const char* name)
{
    throw JitRuntimeError(
        std::string("Nil pointer error: ") +
        (name ? name : "<unknown>")
    );
}

DLL_API void
jit_out_of_memory_error(const char* what)
{
    throw JitRuntimeError(
        std::string("Out of memory: ") +
        (what ? what : "<unknown>")
    );
}

DLL_API void
_jit_set_exception(
    JitContext* ctx,
    const char* message
)
{
    if (!ctx)
        return;

    ctx->exception_active  = 1;
    ctx->exception_message = message;
}

DLL_API void
jit_runtime_error(const char* message)
{
    throw JitRuntimeError(
        message ? message : "Runtime error"
    );
}
