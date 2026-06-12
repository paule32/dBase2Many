// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-12
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
// -----------------------------------------------------------------------------
# include "runtime/dbase2many.hpp"

using namespace std;
using namespace asmjit;

static const char str_0[] = "TObject: Create";
static const char str_1[] = "TObject: Destroy";
static const char str_2[] = "TFoo: Create";
static const char str_3[] = "str: ";
static const char str_4[] = "int: ";
static const char str_5[] = "TFoo: Destroy";
static const char str_6[] = "test";
static const char str_7[] = "foo";
static const char str_8[] = "Nil pointer error: foo";
static const char str_9[] = "field: ";

int main() {
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

    Label class_TObject_Create_1 = a.new_label();
    Label class_TObject_Destroy_2 = a.new_label();
    Label class_TFoo_Create_3 = a.new_label();
    Label class_TFoo_Create_4 = a.new_label();
    Label class_TFoo_Destroy_5 = a.new_label();
    Label skip_class_TObject_Create_6 = a.new_label();
    a.jmp(skip_class_TObject_Create_6);
    a.bind(class_TObject_Create_1);
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
    a.bind(skip_class_TObject_Create_6);
    Label skip_class_TObject_Destroy_7 = a.new_label();
    a.jmp(skip_class_TObject_Destroy_7);
    a.bind(class_TObject_Destroy_2);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
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
    a.bind(skip_class_TObject_Destroy_7);
    Label skip_class_TFoo_Create_8 = a.new_label();
    a.jmp(skip_class_TFoo_Create_8);
    a.bind(class_TFoo_Create_3);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
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
    a.bind(skip_class_TFoo_Create_8);
    Label skip_class_TFoo_Create_9 = a.new_label();
    a.jmp(skip_class_TFoo_Create_9);
    a.bind(class_TFoo_Create_4);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.push(x86::rdx); // save class method param S
    a.push(x86::r8); // save class method param I
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, x86::qword_ptr(x86::rbp, -16)); // load string parameter
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, imm((uint64_t)str_4));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -24)); // load integer parameter
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_int));
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
    a.bind(class_TFoo_Destroy_5);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_5));
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
    a.mov(x86::eax, 12);
    a.movsxd(x86::rax, x86::eax);
    a.push(x86::rax); // ctor integer arg
    a.mov(x86::rax, imm((uint64_t)str_6));
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&_jit_dynstring_from_cstr));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.push(x86::rax); // ctor string arg
    a.mov(x86::rcx, 4);
    a.mov(x86::rax, imm((uint64_t)&_jit_new_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, x86::rax); // Self
    a.pop(x86::rdx); // ctor arg 1
    a.pop(x86::r8); // ctor arg 2
    a.push(x86::rcx); // save constructor result object
    a.sub(x86::rsp, 32);
    a.call(class_TFoo_Create_4);
    a.add(x86::rsp, 32);
    a.pop(x86::rax); // constructor result
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // object foo
    a.mov(x86::eax, 42);
    a.mov(x86::ebx, x86::eax); // save class field value
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // object foo
    Label ptr_not_nil_11 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_11);
    a.mov(x86::rcx, imm((uint64_t)str_8));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_11);
    a.mov(x86::dword_ptr(x86::rax, 0), x86::ebx); // foo.field :=
    a.mov(x86::rcx, imm((uint64_t)str_9));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // object foo
    Label ptr_not_nil_12 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jnz(ptr_not_nil_12);
    a.mov(x86::rcx, imm((uint64_t)str_8));
    a.mov(x86::rax, imm((uint64_t)&_jit_runtime_error));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.bind(ptr_not_nil_12);
    a.mov(x86::eax, x86::dword_ptr(x86::rax, 0)); // foo.field
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
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // object foo
    Label free_nil_13 = a.new_label();
    Label free_end_14 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jz(free_nil_13);
    a.push(x86::rax); // save object for dispose
    a.mov(x86::rcx, x86::rax); // Self
    a.sub(x86::rsp, 32);
    a.call(class_TFoo_Destroy_5);
    a.add(x86::rsp, 32);
    a.pop(x86::rcx);
    a.mov(x86::rax, imm((uint64_t)&_jit_dispose_memory));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.xor_(x86::rax, x86::rax);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // object foo
    a.jmp(free_end_14);
    a.bind(free_nil_13);
    a.bind(free_end_14);
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
    symbols.add(std::to_string((uint64_t)&str_4), "_str_4");
    symbols.add(std::to_string((uint64_t)&str_5), "_str_5");
    symbols.add(std::to_string((uint64_t)&str_6), "_str_6");
    symbols.add(std::to_string((uint64_t)&str_7), "_str_7");
    symbols.add(std::to_string((uint64_t)&str_8), "_str_8");
    symbols.add(std::to_string((uint64_t)&str_9), "_str_9");
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
    symbols.add(std::to_string((uint64_t)&_jit_dynstring_copy), "_jit_dynstring_copy");
    symbols.add(std::to_string((uint64_t)&_jit_dynstring_pos), "_jit_dynstring_pos");
    
    symbols.add(std::to_string((uint64_t)&_jit_set_exception), "_jit_set_exception");
    symbols.add(std::to_string((uint64_t)&_jit_runtime_error), "_jit_runtime_error");
    
    symbols.add(std::to_string((uint64_t)&_jit_array_bounds_error), "_jit_array_bounds_error");
    symbols.add(std::to_string((uint64_t)&_jit_string_range_error), "_jit_string_range_error");
    symbols.add(std::to_string((uint64_t)&_jit_nil_pointer_error), "_jit_nil_pointer_error");
    symbols.add(std::to_string((uint64_t)&_jit_out_of_memory_error), "_jit_out_of_memory_error");
    
    symbols.add(std::to_string((uint64_t)&_jit_ExitProcess), "_jit_ExitProcess");
    symbols.apply(asm_text);
    
    LabelMappings labels;
    labels.add("L0", "class_TObject_Create_1");
    labels.add("L1", "class_TObject_Destroy_2");
    labels.add("L2", "class_TFoo_Create_3");
    labels.add("L3", "class_TFoo_Create_4");
    labels.add("L4", "class_TFoo_Destroy_5");
    labels.add("L5", "skip_class_TObject_Create_6");
    labels.add("L6", "skip_class_TObject_Destroy_7");
    labels.add("L7", "skip_class_TFoo_Create_8");
    labels.add("L8", "skip_class_TFoo_Create_9");
    labels.add("L9", "skip_class_TFoo_Destroy_10");
    labels.add("L10", "ptr_not_nil_11");
    labels.add("L11", "ptr_not_nil_12");
    labels.add("L12", "free_nil_13");
    labels.add("L13", "free_end_14");
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
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-12\n";
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
    asm_out << "section .text\n";
    asm_out << "global " << "_main" << std::endl;
    asm_out << "_main" << ":" << std::endl;
    
    asm_out << asm_text;
    
    asm_out << "\nsection .data\n";
    asm_out << "_str_0 db \"TObject: Create\", 0\n";
    asm_out << "_str_1 db \"TObject: Destroy\", 0\n";
    asm_out << "_str_2 db \"TFoo: Create\", 0\n";
    asm_out << "_str_3 db \"str: \", 0\n";
    asm_out << "_str_4 db \"int: \", 0\n";
    asm_out << "_str_5 db \"TFoo: Destroy\", 0\n";
    asm_out << "_str_6 db \"test\", 0\n";
    asm_out << "_str_7 db \"foo\", 0\n";
    asm_out << "_str_8 db \"Nil pointer error: foo\", 0\n";
    asm_out << "_str_9 db \"field: \", 0\n";
    
    std::string final_asm_text = asm_out.str();

    if (!write_formatted_asm_file(
        final_asm_text.c_str(),
        "test54.asm"
    )) {
        std::cerr << "Could not write ASM file: test54.asm" << std::endl;
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

