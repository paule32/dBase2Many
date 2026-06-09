// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-09
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

    Label proc_Test_1 = a.new_label();
    Label skipproc_Test_2 = a.new_label();
    Label exitproc_Test_3 = a.new_label();
    a.jmp(skipproc_Test_2);
    a.bind(proc_Test_1);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // save param b
    a.sub(x86::rsp, 8); // align stack after odd param saves
    a.sub(x86::rsp, 512); // local variables
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -8)); // load integer parameter
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(exitproc_Test_3);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skipproc_Test_2);
    Label func_IsValid_4 = a.new_label();
    Label endfunc_IsValid_5 = a.new_label();
    a.jmp(endfunc_IsValid_5);
    a.bind(func_IsValid_4);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rbx); // preserve non-volatile RBX
    a.sub(x86::rsp, 8); // align stack in function
    a.sub(x86::rsp, 256); // local variables
    a.mov(x86::eax, 1);
    a.mov(x86::rbx, x86::qword_ptr(x86::rbp, -8));
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_IsValid_5);
    a.push(x86::r12);
    a.push(x86::rbx);
    a.sub(x86::rsp, 8); // align stack
    a.mov (x86::r12, x86::rcx); // ctx
    a.sub(x86::rsp, 32); // shadow space for parameterless function call
    a.call(func_IsValid_4);
    a.add(x86::rsp, 32);
    a.mov(x86::ecx, x86::eax);
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Test_1);
    a.add(x86::rsp, 32);
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
    
    std::ostringstream asm_out;
    std::string asm_text = logger.data();
    asm_out << asm_text;

    std::string final_asm_text = asm_out.str();
    replace_all_fun(final_asm_text);
    
    SymbolMappings symbols;
    symbols.add(std::to_string((uint64_t)&jit_print_text), "_jit_print_text");
    symbols.add(std::to_string((uint64_t)&jit_print_int), "_jit_print_int");
    symbols.add(std::to_string((uint64_t)&jit_print_double), "_jit_print_double");
    symbols.add(std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    symbols.add(std::to_string((uint64_t)&jit_dynarray_setlength), "_jit_dynarray_setlength");
    symbols.add(std::to_string((uint64_t)&jit_dynstring_setlength), "_jit_dynstring_setlength");
    symbols.add(std::to_string((uint64_t)&jit_array_bounds_error), "_jit_array_bounds_error");
    symbols.add(std::to_string((uint64_t)&jit_string_range_error), "_jit_string_range_error");
    symbols.add(std::to_string((uint64_t)&jit_new_memory), "_jit_new_memory");
    symbols.add(std::to_string((uint64_t)&jit_dispose_memory), "_jit_dispose_memory");
    symbols.apply(asm_text);
    
    LabelMappings labels;
    labels.add("L0", "proc_Test_1");
    labels.add("L1", "skipproc_Test_2");
    labels.add("L2", "exitproc_Test_3");
    labels.add("L3", "func_IsValid_4");
    labels.add("L4", "endfunc_IsValid_5");
    labels.apply(asm_text);

    replace_all_ptr(asm_text);
    
    
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.print_double_tmp]");
    
    
    
    asm_out << "; -----------------------------------------------------------------------------\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-09\n";
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
    
    asm_out << "extern _jit_array_bounds_error"  << std::endl;
    asm_out << "extern _jit_string_range_error"  << std::endl;
    asm_out << "extern _jit_dynarray_setlength"  << std::endl;
    asm_out << "extern _jit_dynstring_setlength" << std::endl;
    asm_out << std::endl;
    
    
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
    
    asm_out << "\nsection .data\n";
    
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

