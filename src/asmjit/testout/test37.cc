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

static const char str_0[] = "n";
static const char str_1[] = "Nil pointer error: n";
static const char str_2[] = "p";
static const char str_3[] = "Nil pointer error: p";

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
    a.sub(x86::rsp, 512); // local variables
    a.mov(x86::rcx, 12);
    a.mov(x86::rax, imm((uint64_t)&_jit_new_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::qword_ptr(x86::rbp, -24), x86::rax); // local pointer n :=
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -16));
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -24)); // local pointer n
    Label ptr_not_nil_4 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_4);
    a.mov(x86::rcx, imm((uint64_t)str_1));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_4);
    a.mov(x86::dword_ptr(x86::rax), x86::ebx); // n^.Value :=
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::rax, x86::qword_ptr(x86::r11));
    a.push(x86::rax); // save right pointer value
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -24)); // local pointer n
    a.add(x86::rax, 4); // field offset
    a.pop(x86::r11);
    a.mov(x86::qword_ptr(x86::rax), x86::r11); // n^.Next :=
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -24)); // local pointer n
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::qword_ptr(x86::r11), x86::rax);
    a.bind(exitproc_Push_3);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skipproc_Push_2);
    Label proc_InsertAfter_5 = a.new_label();
    Label skipproc_InsertAfter_6 = a.new_label();
    Label exitproc_InsertAfter_7 = a.new_label();
    a.jmp(skipproc_InsertAfter_6);
    a.bind(proc_InsertAfter_5);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // save param Head
    a.push(x86::rdx); // save param AfterValue
    a.push(x86::r8); // save param NewValue
    a.sub(x86::rsp, 8); // align stack after odd param saves
    a.sub(x86::rsp, 512); // local variables
    a.mov(x86::r11, x86::qword_ptr(x86::rbp, -8)); // var param address Head
    a.mov(x86::rax, x86::qword_ptr(x86::r11));
    a.mov(x86::qword_ptr(x86::rbp, -32), x86::rax); // local pointer p :=
    Label while_8 = a.new_label();
    Label endwhile_9 = a.new_label();
    a.bind(while_8);
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -32)); // local pointer p
    a.push(x86::rax); // save left pointer
    a.xor_(x86::rax, x86::rax); // nil
    a.mov(x86::rbx, x86::rax); // right pointer
    a.pop(x86::rax);           // left pointer
    a.cmp(x86::rax, x86::rbx);
    a.je(endwhile_9);
    Label else_10 = a.new_label();
    Label endif_11 = a.new_label();
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -32)); // local pointer p
    Label ptr_not_nil_12 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_12);
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_12);
    a.mov(x86::eax, x86::dword_ptr(x86::rax, 0)); // p.Value
    a.push(x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -16));
    a.mov(x86::ebx, x86::eax);
    a.pop(x86::rax);
    a.cmp(x86::eax, x86::ebx);
    a.jne(else_10);
    a.mov(x86::rcx, 12);
    a.mov(x86::rax, imm((uint64_t)&_jit_new_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::qword_ptr(x86::rbp, -40), x86::rax); // local pointer n :=
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -24));
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -40)); // local pointer n
    Label ptr_not_nil_13 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_13);
    a.mov(x86::rcx, imm((uint64_t)str_1));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_13);
    a.mov(x86::dword_ptr(x86::rax), x86::ebx); // n^.Value :=
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -32)); // local pointer p
    Label ptr_not_nil_14 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_14);
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_14);
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 4)); // p.Next
    a.push(x86::rax); // save right pointer value
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -40)); // local pointer n
    a.add(x86::rax, 4); // field offset
    a.pop(x86::r11);
    a.mov(x86::qword_ptr(x86::rax), x86::r11); // n^.Next :=
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -40)); // local pointer n
    a.push(x86::rax); // save right pointer value
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -32)); // local pointer p
    a.add(x86::rax, 4); // field offset
    a.pop(x86::r11);
    a.mov(x86::qword_ptr(x86::rax), x86::r11); // p^.Next :=
    a.jmp(exitproc_InsertAfter_7); // Exit
    a.bind(else_10);
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -32)); // local pointer p
    Label ptr_not_nil_15 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_15);
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_15);
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 4)); // p.Next
    a.mov(x86::qword_ptr(x86::rbp, -32), x86::rax); // local pointer p :=
    a.jmp(while_8);
    a.bind(endwhile_9);
    a.bind(exitproc_InsertAfter_7);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skipproc_InsertAfter_6);
    a.push(x86::r12);
    a.push(x86::rbx);
    a.sub(x86::rsp, 8); // align stack
    a.mov (x86::r12, x86::rcx); // ctx
    a.xor_(x86::rax, x86::rax); // nil
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // Head
    a.mov(x86::eax, 10);
    a.movsxd(x86::rax, x86::eax);
    a.push(x86::rax); // integer parameter
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.push(x86::rax); // var parameter
    a.pop(x86::rcx); // load parameter 1
    a.pop(x86::rdx); // load parameter 2
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Push_1);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 20);
    a.movsxd(x86::rax, x86::eax);
    a.push(x86::rax); // integer parameter
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.push(x86::rax); // var parameter
    a.pop(x86::rcx); // load parameter 1
    a.pop(x86::rdx); // load parameter 2
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Push_1);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 30);
    a.movsxd(x86::rax, x86::eax);
    a.push(x86::rax); // integer parameter
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.push(x86::rax); // var parameter
    a.pop(x86::rcx); // load parameter 1
    a.pop(x86::rdx); // load parameter 2
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_Push_1);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 25);
    a.movsxd(x86::rax, x86::eax);
    a.push(x86::rax); // integer parameter
    a.mov(x86::eax, 20);
    a.movsxd(x86::rax, x86::eax);
    a.push(x86::rax); // integer parameter
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.add(x86::rax, 0); // @Head
    a.push(x86::rax); // var parameter
    a.pop(x86::rcx); // load parameter 1
    a.pop(x86::rdx); // load parameter 2
    a.pop(x86::r8); // load parameter 3
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(proc_InsertAfter_5);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // Head
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 8), x86::rax); // p
    Label while_16 = a.new_label();
    Label endwhile_17 = a.new_label();
    a.bind(while_16);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 8)); // p
    a.push(x86::rax); // save left pointer
    a.xor_(x86::rax, x86::rax); // nil
    a.mov(x86::rbx, x86::rax); // right pointer
    a.pop(x86::rax);           // left pointer
    a.cmp(x86::rax, x86::rbx);
    a.je(endwhile_17);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 8)); // p
    Label ptr_not_nil_18 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_18);
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_18);
    a.mov(x86::eax, x86::dword_ptr(x86::rax, 0)); // p.Value
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 8)); // p
    Label ptr_not_nil_19 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_19);
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_19);
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 4)); // p.Next
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 8), x86::rax); // p
    a.jmp(while_16);
    a.bind(endwhile_17);
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
    symbols.add(std::to_string((uint64_t)&str_0), "_str_0");
    symbols.add(std::to_string((uint64_t)&str_1), "_str_1");
    symbols.add(std::to_string((uint64_t)&str_2), "_str_2");
    symbols.add(std::to_string((uint64_t)&str_3), "_str_3");
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
    labels.add("L0", "proc_Push_1");
    labels.add("L1", "skipproc_Push_2");
    labels.add("L2", "exitproc_Push_3");
    labels.add("L3", "ptr_not_nil_4");
    labels.add("L4", "proc_InsertAfter_5");
    labels.add("L5", "skipproc_InsertAfter_6");
    labels.add("L6", "exitproc_InsertAfter_7");
    labels.add("L7", "while_8");
    labels.add("L8", "endwhile_9");
    labels.add("L9", "else_10");
    labels.add("L10", "endif_11");
    labels.add("L11", "ptr_not_nil_12");
    labels.add("L12", "ptr_not_nil_13");
    labels.add("L13", "ptr_not_nil_14");
    labels.add("L14", "ptr_not_nil_15");
    labels.add("L15", "while_16");
    labels.add("L16", "endwhile_17");
    labels.add("L17", "ptr_not_nil_18");
    labels.add("L18", "ptr_not_nil_19");
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
    asm_out << "pointr_vars: times 2 dq 0\n";
    
    
    asm_out << std::endl;
    asm_out << "section .text\n";
    asm_out << "global " << "_main" << std::endl;
    asm_out << "_main" << ":" << std::endl;
    
    asm_out << asm_text;
    
    asm_out << "\nsection .data\n";
    asm_out << "_str_0 db \"n\", 0\n";
    asm_out << "_str_1 db \"Nil pointer error: n\", 0\n";
    asm_out << "_str_2 db \"p\", 0\n";
    asm_out << "_str_3 db \"Nil pointer error: p\", 0\n";
    
    std::string final_asm_text = asm_out.str();

    if (!write_formatted_asm_file(
        final_asm_text.c_str(),
        "test37.asm"
    )) {
        std::cerr << "Could not write ASM file: test37.asm" << std::endl;
    }
    
    std::array<int,      1> int_vars{};
    std::array<double,   1> double_vars{};
    std::array<char*,    1> string_vars{};
    std::array<uint8_t,  1> record_vars{};
    std::array<uint8_t,  1> arrays_vars{};
    std::array<uint64_t, 2> pointr_vars{};
    
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

