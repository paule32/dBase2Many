// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-11
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
// -----------------------------------------------------------------------------
# include "runtime/dbase2many.hpp"

using namespace std;
using namespace asmjit;



int main() {
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

    a.push(x86::r12);
    a.push(x86::rbx);
    a.sub(x86::rsp, 8); // align stack
    a.mov (x86::r12, x86::rcx); // ctx
    a.mov(x86::eax, 4);
    a.movsxd(x86::rdx, x86::eax);
    a.mov(x86::r8, 4);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&_jit_dynarray_setlength));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // dynamic array flags
    a.mov(x86::eax, 1);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.mov(x86::eax, 0);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 0);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.mov(x86::eax, 1);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 1);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.cmp(x86::eax, 0);
    a.setne(x86::al);
    a.movzx(x86::eax, x86::al);
    a.xor_(x86::eax, 1); // not
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.mov(x86::eax, 2);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 0);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.cmp(x86::eax, 0);
    a.setne(x86::al);
    a.movzx(x86::eax, x86::al);
    a.push(x86::rax);
    a.mov(x86::eax, 2);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.cmp(x86::eax, 0);
    a.setne(x86::al);
    a.movzx(x86::eax, x86::al);
    a.pop(x86::rbx);
    a.and_(x86::eax, x86::ebx);
    a.cmp(x86::eax, 0);
    a.setne(x86::al);
    a.movzx(x86::eax, x86::al);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.mov(x86::eax, 3);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 0);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 1);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 2);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 3);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array flags
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.add(x86::rsp, 8); // undo alignment
    a.pop(x86::rbx);
    a.pop(x86::r12);
    
    a.xor_(x86::ecx, x86::ecx);
    a.sub(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_ExitProcess));
    a.call(x86::rax);
    a.ret();        // never reach

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {
        std::cerr << "AsmJit error: " << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }
    
    std::ostringstream asm_out;
    std::string asm_text = logger.data();

    replace_all_fun(asm_text);
    
    SymbolMappings symbols;
    symbols.add(std::to_string((uint64_t)&_jit_print_text), "_jit_print_text");
    symbols.add(std::to_string((uint64_t)&_jit_print_int), "_jit_print_int");
    symbols.add(std::to_string((uint64_t)&_jit_print_double), "_jit_print_double");
    symbols.add(std::to_string((uint64_t)&_jit_print_newline), "_jit_print_newline");
    
    symbols.add(std::to_string((uint64_t)&_jit_new_memory), "_jit_new_memory");
    symbols.add(std::to_string((uint64_t)&_jit_dispose_memory), "_jit_dispose_memory");
    
    symbols.add(std::to_string((uint64_t)&_jit_dynarray_setlength), "_jit_dynarray_setlength");
    
    symbols.add(std::to_string((uint64_t)&_jit_dynstring_from_cstr), "_jit_dynstring_from_cstr");
    symbols.add(std::to_string((uint64_t)&_jit_dynstring_setlength), "_jit_dynstring_setlength");
    symbols.add(std::to_string((uint64_t)&_jit_dynstring_length), "_jit_dynstring_length");
    symbols.add(std::to_string((uint64_t)&_jit_dynstring_concat), "_jit_dynstring_concat");
    
    symbols.add(std::to_string((uint64_t)&_jit_set_exception), "_jit_set_exception");
    symbols.add(std::to_string((uint64_t)&_jit_runtime_error), "_jit_runtime_error");
    
    symbols.add(std::to_string((uint64_t)&_jit_array_bounds_error), "_jit_array_bounds_error");
    symbols.add(std::to_string((uint64_t)&_jit_string_range_error), "_jit_string_range_error");
    symbols.add(std::to_string((uint64_t)&_jit_nil_pointer_error), "_jit_nil_pointer_error");
    symbols.add(std::to_string((uint64_t)&_jit_out_of_memory_error), "_jit_out_of_memory_error");
    
    symbols.add(std::to_string((uint64_t)&_jit_ExitProcess), "_jit_ExitProcess");
    symbols.apply(asm_text);
    
    LabelMappings labels;
    
    labels.apply(asm_text);

    replace_all_ptr(asm_text);
    replace_all(asm_text, "mov r12, rcx", "lea r12, [rel ctx]");
    
    
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.string_vars]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.record_vars]");
    replace_all(asm_text, "[r12+32]",  "[r12 + JitContext.arrays_vars]");
    replace_all(asm_text, "[r12+40]",  "[r12 + JitContext.pointr_vars]");
    replace_all(asm_text, "[r12+48]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+56]",  "[r12 + JitContext.print_double_tmp]");
    
    
    
    asm_out << "; -----------------------------------------------------------------------------\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-11\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\n";
    asm_out << "; all rights reserved.\n";
    asm_out << "; -----------------------------------------------------------------------------\n\n";
    
    
        asm_out << "struc JitContext\n";
        asm_out << "    .int_vars:         resq 1" << std::endl;
        asm_out << "    .double_vars:      resq 1" << std::endl;
        asm_out << "    .string_vars:      resq 1" << std::endl;
        asm_out << "    .record_vars:      resq 1" << std::endl;
        asm_out << "    .arrays_vars:      resq 1" << std::endl;
        asm_out << "    .pointr_vars:      resq 1" << std::endl;
        asm_out << "    .print_int_tmp:    resd 1" << std::endl;
        asm_out << "    .print_double_tmp: resq 1" << std::endl;
        asm_out << "endstruc" << std::endl << std::endl;
        
    
    
    asm_out << std::endl;
    asm_out << std::endl;
    
    
    asm_out << "extern _jit_print_text" << std::endl;
    asm_out << "extern _jit_print_int" << std::endl;
    asm_out << "extern _jit_print_double" << std::endl;
    asm_out << "extern _jit_print_newline" << std::endl;
    asm_out << std::endl;
    asm_out << "extern _jit_new_memory" << std::endl;
    asm_out << "extern _jit_dispose_memory" << std::endl;
    asm_out << std::endl;
    asm_out << "extern _jit_dynarray_setlength" << std::endl;
    asm_out << std::endl;
    asm_out << "extern _jit_dynstring_from_cstr" << std::endl;
    asm_out << "extern _jit_dynstring_setlength" << std::endl;
    asm_out << "extern _jit_dynstring_length" << std::endl;
    asm_out << "extern _jit_dynstring_concat" << std::endl;
    asm_out << std::endl;
    asm_out << "extern _jit_set_exception" << std::endl;
    asm_out << "extern _jit_runtime_error" << std::endl;
    asm_out << std::endl;
    asm_out << "extern _jit_nil_pointer_error" << std::endl;
    asm_out << "extern _jit_out_of_memory_error" << std::endl;
    asm_out << "extern _jit_array_bounds_error" << std::endl;
    asm_out << "extern _jit_string_range_error" << std::endl;
    asm_out << std::endl;
    asm_out << "extern _jit_ExitProcess" << std::endl;
    
    
    asm_out << "\nsection .data\n";
    asm_out << "ctx:\n";
    asm_out << "    istruc JitContext\n";
    asm_out << "        at JitContext.int_vars,         dq int_vars\n";
    asm_out << "        at JitContext.double_vars,      dq double_vars\n";
    asm_out << "        at JitContext.string_vars,      dq string_vars\n";
    asm_out << "        at JitContext.record_vars,      dq record_vars\n";
    asm_out << "        at JitContext.arrays_vars,      dq arrays_vars\n";
    asm_out << "        at JitContext.pointr_vars,      dq pointr_vars\n";
    asm_out << "        at JitContext.print_int_tmp,    dd 0\n";
    asm_out << "        at JitContext.print_double_tmp, dq 0\n";
    asm_out << "    iend\n\n";

    asm_out << "int_vars:    times 1 dd 0\n";
    asm_out << "double_vars: times 1 dq 0\n";
    asm_out << "string_vars: times 1 dq 0\n";
    asm_out << "record_vars: times 1 db 0\n";
    asm_out << "arrays_vars: times 1 db 0\n";
    asm_out << "pointr_vars: times 1 dq 0\n";
    
    
    asm_out << std::endl;
    asm_out << "section .text\n";
    asm_out << "global " << "_main" << std::endl;
    asm_out << "_main" << ":" << std::endl;
    
    asm_out << asm_text;
    
    asm_out << "\nsection .data\n";
    
    std::string final_asm_text = asm_out.str();

    if (!write_formatted_asm_file(
        final_asm_text.c_str(),
        "test42.asm"
    )) {
        std::cerr << "Could not write ASM file: test42.asm" << std::endl;
    }
    
    std::array<int,      1> int_vars{};
    std::array<double,   1> double_vars{};
    std::array<char*,    1> string_vars{};
    std::array<uint8_t,  1> record_vars{};
    std::array<uint8_t,  1> arrays_vars{};
    std::array<uint64_t, 1> pointr_vars{};
    
    JitContext ctx{};
    ctx.int_vars    = int_vars.data();
    
    ctx.double_vars = double_vars.data();
    ctx.string_vars = string_vars.data();
    ctx.record_vars = record_vars.data();
    ctx.arrays_vars = arrays_vars.data();
    ctx.pointr_vars = pointr_vars.data();
    
    try {
        fn(&ctx);
    }
    catch (const JitRuntimeError& e) {
        std::cerr << "JIT runtime error: " << e.what() << std::endl;
        rt.release(fn);
        return 2;
    }
    catch (const std::exception& e) {
        std::cerr << "C++ exception: " << e.what() << std::endl;
        rt.release(fn);
        return 3;
    }
    catch (...) {
        std::cerr << "Unknown JIT exception" << std::endl;
        rt.release(fn);
        return 4;
    }

    rt.release(fn);
    return 0;
}

