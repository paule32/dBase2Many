// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-07
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
    a.mov(x86::rcx, 4);
    a.mov(x86::rax, imm((uint64_t)&jit_new_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // p
    a.mov(x86::eax, 123);
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // p
    a.mov(x86::dword_ptr(x86::rax), x86::ebx); // p^ :=
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // p
    a.mov(x86::eax, x86::dword_ptr(x86::rax)); // p^
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // p
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&jit_dispose_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.xor_(x86::rax, x86::rax);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // p
    a.add(x86::rsp, 8); // undo alignment
    a.pop(x86::rbx);
    a.pop(x86::r12);
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {
        std::cerr << "AsmJit error: " << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }
    
    std::ofstream asm_out("test27.asm");
    std::string asm_text = logger.data();

    replace_all_fun(asm_text);
    
    SymbolMappings symbols;
    symbols.add(std::to_string((uint64_t)&jit_print_text), "_jit_print_text");
    symbols.add(std::to_string((uint64_t)&jit_print_int), "_jit_print_int");
    symbols.add(std::to_string((uint64_t)&jit_print_double), "_jit_print_double");
    symbols.add(std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    symbols.add(std::to_string((uint64_t)&jit_array_bounds_error), "_jit_array_bounds_error");
    symbols.add(std::to_string((uint64_t)&jit_new_memory), "_jit_new_memory");
    symbols.add(std::to_string((uint64_t)&jit_dispose_memory), "_jit_dispose_memory");
    symbols.apply(asm_text);
    
    LabelMappings labels;
    
    labels.apply(asm_text);

    replace_all_ptr(asm_text);
    
    
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.print_double_tmp]");
    
    
    
    asm_out << "; -----------------------------------------------------------------------------\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-07\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\n";
    asm_out << "; all rights reserved.\n";
    asm_out << "; -----------------------------------------------------------------------------\n\n";
    
    
    asm_out << "struc JitContext\n";
    asm_out << "    .int_vars:         resq 1\n";
    asm_out << "    .double_vars:      resq 1\n";
    asm_out << "    .print_int_tmp:    resd 1\n";
    asm_out << "    .print_double_tmp: resq 1\n";
    asm_out << "endstruc\n\n";
    
    
    
    asm_out << std::endl;
    asm_out << std::endl;
    
    asm_out << "extern _jit_array_bounds_error" << std::endl;
    asm_out << std::endl;
    
    std::istringstream iss(asm_text);
    std::string line;

    
    asm_out << "extern _jit_print_text\n";
    asm_out << "extern _jit_print_int\n";
    asm_out << "extern _jit_print_double\n";
    asm_out << "extern _jit_print_newline\n";
    asm_out << "extern _jit_new_memory\n";
    asm_out << "extern _jit_dispose_memory\n";
    
    asm_out << std::endl;
    asm_out << "section .text\n";
    asm_out << "global " << "_main" << std::endl;
    asm_out << "_main" << ":" << std::endl;
    
    replace_all_str(asm_text, asm_out);
    
    asm_out << "\nsection .data\n";
    
    asm_out.close();
    
    std::array<int,         1> int_vars{};
    std::array<double,      1> double_vars{};
    std::array<const char*, 1> string_vars{};
    std::array<uint8_t,     1> record_vars{};
    std::array<uint8_t,     1> arrays_vars{};
    std::array<uint64_t,    1> pointr_vars{};
    
    JitContext ctx{};
    ctx.int_vars    = int_vars.data();
    
    ctx.double_vars = double_vars.data();
    ctx.string_vars = string_vars.data();
    ctx.record_vars = record_vars.data();
    ctx.arrays_vars = arrays_vars.data();
    ctx.pointr_vars = pointr_vars.data();
    
    fn(&ctx);

    rt.release(fn);
    return 0;
}

