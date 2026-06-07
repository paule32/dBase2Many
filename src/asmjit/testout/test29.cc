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

static const char str_0[] = "m";

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
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 0);
    Label array_bounds_ok_1 = a.new_label();
    Label array_bounds_fail_2 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_2);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_2);
    a.jmp(array_bounds_ok_1);
    a.bind(array_bounds_fail_2);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_1);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 0);
    Label array_bounds_ok_3 = a.new_label();
    Label array_bounds_fail_4 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_4);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_4);
    a.jmp(array_bounds_ok_3);
    a.bind(array_bounds_fail_4);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_3);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 20);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 0);
    Label array_bounds_ok_5 = a.new_label();
    Label array_bounds_fail_6 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_6);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_6);
    a.jmp(array_bounds_ok_5);
    a.bind(array_bounds_fail_6);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_5);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 1);
    Label array_bounds_ok_7 = a.new_label();
    Label array_bounds_fail_8 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_8);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_8);
    a.jmp(array_bounds_ok_7);
    a.bind(array_bounds_fail_8);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_7);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 30);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 1);
    Label array_bounds_ok_9 = a.new_label();
    Label array_bounds_fail_10 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_10);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_10);
    a.jmp(array_bounds_ok_9);
    a.bind(array_bounds_fail_10);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_9);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 0);
    Label array_bounds_ok_11 = a.new_label();
    Label array_bounds_fail_12 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_12);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_12);
    a.jmp(array_bounds_ok_11);
    a.bind(array_bounds_fail_12);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_11);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.mov(x86::eax, 99);
    a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax);
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 2);
    Label array_bounds_ok_13 = a.new_label();
    Label array_bounds_fail_14 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_14);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_14);
    a.jmp(array_bounds_ok_13);
    a.bind(array_bounds_fail_14);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_13);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 3);
    Label array_bounds_ok_15 = a.new_label();
    Label array_bounds_fail_16 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_16);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_16);
    a.jmp(array_bounds_ok_15);
    a.bind(array_bounds_fail_16);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_15);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));
    a.mov(x86::dword_ptr(x86::r11), x86::eax);
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 0);
    Label array_bounds_ok_17 = a.new_label();
    Label array_bounds_fail_18 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_18);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_18);
    a.jmp(array_bounds_ok_17);
    a.bind(array_bounds_fail_18);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_17);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 0);
    Label array_bounds_ok_19 = a.new_label();
    Label array_bounds_fail_20 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_20);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_20);
    a.jmp(array_bounds_ok_19);
    a.bind(array_bounds_fail_20);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_19);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
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
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 0);
    Label array_bounds_ok_21 = a.new_label();
    Label array_bounds_fail_22 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_22);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_22);
    a.jmp(array_bounds_ok_21);
    a.bind(array_bounds_fail_22);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_21);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 1);
    Label array_bounds_ok_23 = a.new_label();
    Label array_bounds_fail_24 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_24);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_24);
    a.jmp(array_bounds_ok_23);
    a.bind(array_bounds_fail_24);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_23);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
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
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 1);
    Label array_bounds_ok_25 = a.new_label();
    Label array_bounds_fail_26 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_26);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_26);
    a.jmp(array_bounds_ok_25);
    a.bind(array_bounds_fail_26);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_25);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 0);
    Label array_bounds_ok_27 = a.new_label();
    Label array_bounds_fail_28 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_28);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_28);
    a.jmp(array_bounds_ok_27);
    a.bind(array_bounds_fail_28);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_27);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
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
    a.xor_(x86::ebx, x86::ebx); // linear array index
    a.mov(x86::eax, 2);
    Label array_bounds_ok_29 = a.new_label();
    Label array_bounds_fail_30 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_30);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_30);
    a.jmp(array_bounds_ok_29);
    a.bind(array_bounds_fail_30);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_29);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.imul(x86::eax, x86::eax, 10);
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, 3);
    Label array_bounds_ok_31 = a.new_label();
    Label array_bounds_fail_32 = a.new_label();
    a.mov(x86::r10d, x86::eax); // save dimension index
    a.cmp(x86::eax, 0);
    a.jl(array_bounds_fail_32);
    a.cmp(x86::eax, 9);
    a.jg(array_bounds_fail_32);
    a.jmp(array_bounds_ok_31);
    a.bind(array_bounds_fail_32);
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::edx, x86::r10d);
    a.mov(x86::r8d, 0);
    a.mov(x86::r9d, 9);
    a.mov(x86::rax, imm((uint64_t)&jit_array_bounds_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(array_bounds_ok_31);
    a.mov(x86::eax, x86::r10d); // restore dimension index
    a.add(x86::ebx, x86::eax);
    a.mov(x86::eax, x86::ebx); // final linear index
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
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
    
    std::ofstream asm_out("test29.asm");
    std::string asm_text = logger.data();

    replace_all_fun(asm_text);
    
    SymbolMappings symbols;
    symbols.add(std::to_string((uint64_t)&str_0), "_str_0");
    symbols.add(std::to_string((uint64_t)&jit_print_text), "_jit_print_text");
    symbols.add(std::to_string((uint64_t)&jit_print_int), "_jit_print_int");
    symbols.add(std::to_string((uint64_t)&jit_print_double), "_jit_print_double");
    symbols.add(std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    symbols.add(std::to_string((uint64_t)&jit_array_bounds_error), "_jit_array_bounds_error");
    symbols.add(std::to_string((uint64_t)&jit_new_memory), "_jit_new_memory");
    symbols.add(std::to_string((uint64_t)&jit_dispose_memory), "_jit_dispose_memory");
    symbols.apply(asm_text);
    
    LabelMappings labels;
    labels.add("L0", "array_bounds_ok_1");
    labels.add("L1", "array_bounds_fail_2");
    labels.add("L2", "array_bounds_ok_3");
    labels.add("L3", "array_bounds_fail_4");
    labels.add("L4", "array_bounds_ok_5");
    labels.add("L5", "array_bounds_fail_6");
    labels.add("L6", "array_bounds_ok_7");
    labels.add("L7", "array_bounds_fail_8");
    labels.add("L8", "array_bounds_ok_9");
    labels.add("L9", "array_bounds_fail_10");
    labels.add("L10", "array_bounds_ok_11");
    labels.add("L11", "array_bounds_fail_12");
    labels.add("L12", "array_bounds_ok_13");
    labels.add("L13", "array_bounds_fail_14");
    labels.add("L14", "array_bounds_ok_15");
    labels.add("L15", "array_bounds_fail_16");
    labels.add("L16", "array_bounds_ok_17");
    labels.add("L17", "array_bounds_fail_18");
    labels.add("L18", "array_bounds_ok_19");
    labels.add("L19", "array_bounds_fail_20");
    labels.add("L20", "array_bounds_ok_21");
    labels.add("L21", "array_bounds_fail_22");
    labels.add("L22", "array_bounds_ok_23");
    labels.add("L23", "array_bounds_fail_24");
    labels.add("L24", "array_bounds_ok_25");
    labels.add("L25", "array_bounds_fail_26");
    labels.add("L26", "array_bounds_ok_27");
    labels.add("L27", "array_bounds_fail_28");
    labels.add("L28", "array_bounds_ok_29");
    labels.add("L29", "array_bounds_fail_30");
    labels.add("L30", "array_bounds_ok_31");
    labels.add("L31", "array_bounds_fail_32");
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
    asm_out << "_str_0 db \"m\", 0\n";
    
    asm_out.close();
    
    std::array<int,         1> int_vars{};
    std::array<double,      1> double_vars{};
    std::array<const char*, 1> string_vars{};
    std::array<uint8_t,     1> record_vars{};
    std::array<uint8_t,     400> arrays_vars{};
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

