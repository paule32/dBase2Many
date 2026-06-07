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

    Label proc_Push_1 = a.new_label();
    Label skipproc_Push_2 = a.new_label();
    Label exitproc_Push_3 = a.new_label();
    a.jmp(skipproc_Push_2);
    a.bind(proc_Push_1);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // save param Head
    a.push(x86::rdx); // save param Value
    a.mov(x86::rcx, 12);
    a.mov(x86::rax, imm((uint64_t)&jit_new_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 16), x86::rax); // n
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -16));
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 16)); // n
    a.mov(x86::dword_ptr(x86::rax), x86::ebx); // n^.Value :=
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::rax, x86::qword_ptr(x86::r11));
    a.push(x86::rax); // save right pointer value
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 16)); // n
    a.add(x86::rax, 4); // field offset
    a.pop(x86::r11);
    a.mov(x86::qword_ptr(x86::rax), x86::r11); // n^.Next :=
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 16)); // n
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::qword_ptr(x86::r11), x86::rax);
    a.bind(exitproc_Push_3);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skipproc_Push_2);
    Label proc_Pop_4 = a.new_label();
    Label skipproc_Pop_5 = a.new_label();
    Label exitproc_Pop_6 = a.new_label();
    a.jmp(skipproc_Pop_5);
    a.bind(proc_Pop_4);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // save param Head
    Label else_7 = a.new_label();
    Label endif_8 = a.new_label();
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::rax, x86::qword_ptr(x86::r11));
    a.push(x86::rax); // save left pointer
    a.xor_(x86::rax, x86::rax); // nil
    a.mov(x86::r11, x86::rax); // right pointer
    a.pop(x86::rax); // left pointer
    a.cmp(x86::rax, x86::r11);
    a.jne(else_7);
    a.jmp(exitproc_Pop_6); // Exit
    a.bind(else_7);
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::rax, x86::qword_ptr(x86::r11));
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 24), x86::rax); // tmp
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // Head
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 4)); // Head.Next
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::qword_ptr(x86::r11), x86::rax);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 24)); // tmp
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&jit_dispose_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.xor_(x86::rax, x86::rax);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 24), x86::rax); // tmp
    a.bind(exitproc_Pop_6);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skipproc_Pop_5);
    a.push(x86::r12);
    a.push(x86::rbx);
    a.sub(x86::rsp, 8); // align stack
    a.mov (x86::r12, x86::rcx); // ctx
    a.xor_(x86::rax, x86::rax); // nil
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // Head
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.mov(x86::rcx, x86::rax); // var parameter
    a.mov(x86::eax, 10);
    a.mov(x86::edx, x86::eax);
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Push_1);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.mov(x86::rcx, x86::rax); // var parameter
    a.mov(x86::eax, 20);
    a.mov(x86::edx, x86::eax);
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Push_1);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.mov(x86::rcx, x86::rax); // var parameter
    a.mov(x86::eax, 30);
    a.mov(x86::edx, x86::eax);
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Push_1);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.mov(x86::rcx, x86::rax); // var parameter
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Pop_4);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // Head
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 8), x86::rax); // p
    Label while_9 = a.new_label();
    Label endwhile_10 = a.new_label();
    a.bind(while_9);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 8)); // p
    a.push(x86::rax); // save left pointer
    a.xor_(x86::rax, x86::rax); // nil
    a.mov(x86::r11, x86::rax); // right pointer
    a.pop(x86::rax); // left pointer
    a.cmp(x86::rax, x86::r11);
    a.je(endwhile_10);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 8)); // p
    a.mov(x86::eax, x86::dword_ptr(x86::rax, 0)); // p.Value
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
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 8)); // p
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 4)); // p.Next
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 8), x86::rax); // p
    a.jmp(while_9);
    a.bind(endwhile_10);
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
    
    std::ofstream asm_out("test35.asm");
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
    labels.add("L0", "proc_Push_1");
    labels.add("L1", "skipproc_Push_2");
    labels.add("L2", "exitproc_Push_3");
    labels.add("L3", "proc_Pop_4");
    labels.add("L4", "skipproc_Pop_5");
    labels.add("L5", "exitproc_Pop_6");
    labels.add("L6", "else_7");
    labels.add("L7", "endif_8");
    labels.add("L8", "while_9");
    labels.add("L9", "endwhile_10");
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
    std::array<uint64_t,    4> pointr_vars{};
    
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

