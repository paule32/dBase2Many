// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-13
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
// -----------------------------------------------------------------------------
# include "runtime/dbase2many.hpp"

using namespace std;
using namespace asmjit;

static constexpr int DBASE2MANY_MODULE_KIND = 3;

static const char str_0[] = "TFoo: Create";
static const char str_1[] = "TFoo: Create(S: String)";
static const char str_2[] = "TFoo: Create(I1, I2: Integer)";
static const char str_3[] = "TFoo: Destroy";

int main() {
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

    Label class_TFoo_Create_1 = a.new_label();
    Label class_TFoo_Create_2 = a.new_label();
    Label class_TFoo_Create_3 = a.new_label();
    Label class_TFoo_Destroy_4 = a.new_label();
    Label func_Add_5 = a.new_label();
    Label endfunc_Add_6 = a.new_label();
    a.jmp(endfunc_Add_6);
    a.bind(func_Add_5);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rbx); // preserve non-volatile RBX
    a.push(x86::rcx); // save function param a
    a.push(x86::rdx); // save function param b
    a.sub(x86::rsp, 8); // align stack in function
    a.sub(x86::rsp, 256); // local variables
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -16));
    a.push(x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -24));
    a.mov(x86::ebx, x86::eax);
    a.pop(x86::rax);
    a.add(x86::eax, x86::ebx);
    a.mov(x86::rbx, x86::qword_ptr(x86::rbp, -8));
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_Add_6);
    Label skip_class_TFoo_Create_7 = a.new_label();
    a.jmp(skip_class_TFoo_Create_7);
    a.bind(class_TFoo_Create_1);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Create_7);
    Label skip_class_TFoo_Create_8 = a.new_label();
    a.jmp(skip_class_TFoo_Create_8);
    a.bind(class_TFoo_Create_2);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.push(x86::rdx); // save class method param S
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_1));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Create_8);
    Label skip_class_TFoo_Create_9 = a.new_label();
    a.jmp(skip_class_TFoo_Create_9);
    a.bind(class_TFoo_Create_3);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.push(x86::rdx); // save class method param I1
    a.push(x86::r8); // save class method param I2
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_2));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Create_9);
    Label skip_class_TFoo_Destroy_10 = a.new_label();
    a.jmp(skip_class_TFoo_Destroy_10);
    a.bind(class_TFoo_Destroy_4);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Destroy_10);
    a.push(x86::r12);
    a.push(x86::rbx);
    a.sub(x86::rsp, 8); // align stack
    a.mov (x86::r12, x86::rcx); // ctx
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
    
    _jit_symbols_add(symbols);
    symbols.apply(asm_text);
    
    LabelMappings labels;
    labels.add("L0", "class_TFoo_Create_1");
    labels.add("L1", "class_TFoo_Create_2");
    labels.add("L2", "class_TFoo_Create_3");
    labels.add("L3", "class_TFoo_Destroy_4");
    labels.add("L4", "func_Add_5");
    labels.add("func_Add_5", "_ADD$INTEGER$INTEGER");
    labels.add("L6", "endfunc_Add_6");
    labels.add("L7", "skip_class_TFoo_Create_7");
    labels.add("L8", "skip_class_TFoo_Create_8");
    labels.add("L9", "skip_class_TFoo_Create_9");
    labels.add("L10", "skip_class_TFoo_Destroy_10");
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
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-13\n";
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
    asm_out << "extern _jit_dynstring_copy" << std::endl;
    asm_out << "extern _jit_dynstring_pos" << std::endl;
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
    asm_out << "dbase2many_module_kind dq 3\n";
    asm_out << "dbase2many_module_kind_program equ 1\n";
    asm_out << "dbase2many_module_kind_unit equ 2\n";
    asm_out << "dbase2many_module_kind_library equ 3\n\n";

    asm_out << std::endl;
    asm_out << "section .text\n";
    asm_out << "global " << "_main" << std::endl;
    asm_out << "global _ADD$INTEGER$INTEGER\n";
    asm_out << "global _TEST56$$_$$_TFOO_$$_CREATE\n";
    asm_out << "global _TEST56$$_$$_TFOO_$$_CREATE$ANSISTRING\n";
    asm_out << "global _TEST56$$_$$_TFOO_$$_CREATE$INTEGER$INTEGER\n";
    asm_out << "\n";
    asm_out << "_main" << ":" << std::endl;
    
    asm_out << asm_text;
    
    asm_out << "\nsection .data\n";
    asm_out << "_str_0 db \"TFoo: Create\", 0\n";
    asm_out << "_str_1 db \"TFoo: Create(S: String)\", 0\n";
    asm_out << "_str_2 db \"TFoo: Create(I1, I2: Integer)\", 0\n";
    asm_out << "_str_3 db \"TFoo: Destroy\", 0\n";
    
    std::string final_asm_text = asm_out.str();

    if (!write_formatted_asm_file(
        final_asm_text.c_str(),
        "test56.asm"
    )) {
        std::cerr << "Could not write ASM file: test56.asm" << std::endl;
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

