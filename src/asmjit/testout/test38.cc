// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-08
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
// -----------------------------------------------------------------------------
# include "runtime/dbase2many.hpp"

using namespace std;
using namespace asmjit;

static const char str_0[] = "O";
static const char str_1[] = "P";
static const char str_2[] = "A";

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
    a.mov(x86::eax, 10);
    a.movsxd(x86::rdx, x86::eax);
    a.mov(x86::r8, 4);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array a
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&jit_dynarray_setlength));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // dynamic array a
    a.mov(x86::eax, 10);
    a.movsxd(x86::rdx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0));
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&jit_dynstring_setlength));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rdx, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::qword_ptr(x86::rdx, 0), x86::rax);
    a.mov(x86::eax, 123);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.mov(x86::eax, 0);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array a
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 456);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.mov(x86::eax, 1);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array a
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::rax, imm((uint64_t)str_0));
    a.movzx(x86::ebx, x86::byte_ptr(x86::rax)); // char value
    a.mov(x86::eax, 1);
    a.sub(x86::eax, 1);
    a.mov(x86::r10d, x86::eax); // zero based string index
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // s
    Label string_not_nil_1 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(string_not_nil_1);
    a.mov(x86::rax, imm((uint64_t)&jit_string_range_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(string_not_nil_1);
    a.mov(x86::r11, x86::rax);
    a.sub(x86::r11, 16);
    a.mov(x86::r11, x86::qword_ptr(x86::r11)); // string length
    Label string_index_ok_2 = a.new_label();
    Label string_index_fail_3 = a.new_label();
    a.cmp(x86::r10d, 0);
    a.jl(string_index_fail_3);
    a.cmp(x86::r10, x86::r11);
    a.jb(string_index_ok_2);
    a.bind(string_index_fail_3);
    a.mov(x86::rax, imm((uint64_t)&jit_string_range_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(string_index_ok_2);
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax);
    a.mov(x86::byte_ptr(x86::r11), x86::bl); // s[index] :=
    a.mov(x86::rax, imm((uint64_t)str_1));
    a.movzx(x86::ebx, x86::byte_ptr(x86::rax)); // char value
    a.mov(x86::eax, 2);
    a.sub(x86::eax, 1);
    a.mov(x86::r10d, x86::eax); // zero based string index
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // s
    Label string_not_nil_4 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(string_not_nil_4);
    a.mov(x86::rax, imm((uint64_t)&jit_string_range_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(string_not_nil_4);
    a.mov(x86::r11, x86::rax);
    a.sub(x86::r11, 16);
    a.mov(x86::r11, x86::qword_ptr(x86::r11)); // string length
    Label string_index_ok_5 = a.new_label();
    Label string_index_fail_6 = a.new_label();
    a.cmp(x86::r10d, 0);
    a.jl(string_index_fail_6);
    a.cmp(x86::r10, x86::r11);
    a.jb(string_index_ok_5);
    a.bind(string_index_fail_6);
    a.mov(x86::rax, imm((uint64_t)&jit_string_range_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(string_index_ok_5);
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax);
    a.mov(x86::byte_ptr(x86::r11), x86::bl); // s[index] :=
    a.mov(x86::rax, imm((uint64_t)str_2));
    a.movzx(x86::ebx, x86::byte_ptr(x86::rax)); // char value
    a.mov(x86::eax, 3);
    a.sub(x86::eax, 1);
    a.mov(x86::r10d, x86::eax); // zero based string index
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // s
    Label string_not_nil_7 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(string_not_nil_7);
    a.mov(x86::rax, imm((uint64_t)&jit_string_range_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(string_not_nil_7);
    a.mov(x86::r11, x86::rax);
    a.sub(x86::r11, 16);
    a.mov(x86::r11, x86::qword_ptr(x86::r11)); // string length
    Label string_index_ok_8 = a.new_label();
    Label string_index_fail_9 = a.new_label();
    a.cmp(x86::r10d, 0);
    a.jl(string_index_fail_9);
    a.cmp(x86::r10, x86::r11);
    a.jb(string_index_ok_8);
    a.bind(string_index_fail_9);
    a.mov(x86::rax, imm((uint64_t)&jit_string_range_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(string_index_ok_8);
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax);
    a.mov(x86::byte_ptr(x86::r11), x86::bl); // s[index] :=
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // s
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 1);
    a.sub(x86::eax, 1);
    a.mov(x86::r10d, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // s
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax);
    a.movzx(x86::eax, x86::byte_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_char));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 0);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array a
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 1);
    a.imul(x86::eax, x86::eax, 4);
    a.mov(x86::r10d, x86::eax); // save dynamic array byte offset
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // dynamic array a
    a.movsxd(x86::r11, x86::r10d);
    a.add(x86::r11, x86::rax); // dynamic array element address
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
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
    
    std::ofstream asm_out("test38.asm");
    std::string asm_text = logger.data();

    replace_all_fun(asm_text);
    
    SymbolMappings symbols;
    symbols.add(std::to_string((uint64_t)&str_0), "_str_0");
    symbols.add(std::to_string((uint64_t)&str_1), "_str_1");
    symbols.add(std::to_string((uint64_t)&str_2), "_str_2");
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
    labels.add("L0", "string_not_nil_1");
    labels.add("L1", "string_index_ok_2");
    labels.add("L2", "string_index_fail_3");
    labels.add("L3", "string_not_nil_4");
    labels.add("L4", "string_index_ok_5");
    labels.add("L5", "string_index_fail_6");
    labels.add("L6", "string_not_nil_7");
    labels.add("L7", "string_index_ok_8");
    labels.add("L8", "string_index_fail_9");
    labels.apply(asm_text);

    replace_all_ptr(asm_text);
    
    
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.print_double_tmp]");
    
    
    
    asm_out << "; -----------------------------------------------------------------------------\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-08\n";
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
    asm_out << "_str_0 db \"O\", 0\n";
    asm_out << "_str_1 db \"P\", 0\n";
    asm_out << "_str_2 db \"A\", 0\n";
    
    asm_out.close();
    
    std::array<int,      1> int_vars{};
    std::array<double,   1> double_vars{};
    std::array<char*,    1> string_vars{};
    std::array<uint8_t,  1> record_vars{};
    std::array<uint8_t,  8> arrays_vars{};
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

