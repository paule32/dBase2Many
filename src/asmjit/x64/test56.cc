// -----------------------------------------------------------------------------
// AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: 2026-06-16
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
// -----------------------------------------------------------------------------

# include "runtime/dbase2many.hpp"

using namespace std;
using namespace asmjit;

static constexpr int DBASE2MANY_MODULE_KIND = 1;

static const char str_0[] = "TFoo: Create";
static const char str_1[] = "TFoo: Create(S: String)";
static const char str_2[] = "TFoo: Create(I1, I2: Integer)";
static const char str_3[] = "TFoo: Destroy";
static const char str_4[] = "TFoo: String";
static const char str_5[] = "before break";
static const char str_6[] = "after break";

int main() {{
  JitRuntime rt;

   CodeHolder code;
  code.init(rt.environment());

  StringLogger logger;

  logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
  logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);

  code.set_logger(&logger);
  x86::Assembler a(&code);

    Label class_TFoo_SetValue_1 = a.new_label();
    Label class_TFoo_Create_2 = a.new_label();
    Label class_TFoo_Create_3 = a.new_label();
    Label class_TFoo_Create_4 = a.new_label();
    Label class_TFoo_Destroy_5 = a.new_label();
    Label class_TFoo_GetValue_6 = a.new_label();
    Label func_Add_7 = a.new_label();
    Label endfunc_Add_8 = a.new_label();
    a.jmp(endfunc_Add_8);
    a.bind(func_Add_7);
    a.push(x86::rbp);  // epilog
    a.mov(x86::rbp, x86::rsp);  // stack frame
    a.push(x86::rbx);  // preserve non-volatile RBX
    a.push(x86::rcx); // save function param a
    a.push(x86::rdx); // save function param b
    a.sub(x86::rsp, 8);  // align stack in function
    a.sub(x86::rsp, 256);  // local variables
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -16));
    a.push(x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -24));
    a.mov(x86::ebx, x86::eax);
    a.pop(x86::rax);
    a.add(x86::eax, ebx);
    a.mov(x86::rbx, x86::qword_ptr(x86::rbp, -8));
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_Add_8);
    Label skip_class_TFoo_Create_9 = a.new_label();
    a.jmp(skip_class_TFoo_Create_9);
    a.bind(class_TFoo_Create_2);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Create_9);
    Label skip_class_TFoo_Create_10 = a.new_label();
    a.jmp(skip_class_TFoo_Create_10);
    a.bind(class_TFoo_Create_3);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.push(x86::rdx); // save class method param S
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_1));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Create_10);
    Label skip_class_TFoo_Create_11 = a.new_label();
    a.jmp(skip_class_TFoo_Create_11);
    a.bind(class_TFoo_Create_4);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.push(x86::rdx); // save class method param I1
    a.push(x86::r8); // save class method param I2
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_2));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Create_11);
    Label skip_class_TFoo_Destroy_12 = a.new_label();
    a.jmp(skip_class_TFoo_Destroy_12);
    a.bind(class_TFoo_Destroy_5);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_Destroy_12);
    Label skip_class_TFoo_SetValue_13 = a.new_label();
    a.jmp(skip_class_TFoo_SetValue_13);
    a.bind(class_TFoo_SetValue_1);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.push(x86::rdx); // save class method param v
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::eax, x86::dword_ptr(x86::rbp, -16));
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -8)); // Self
    a.mov(x86::dword_ptr(x86::rax, 0), x86::ebx); // Self.FValue :=
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_SetValue_13);
    Label skip_class_TFoo_GetValue_14 = a.new_label();
    a.jmp(skip_class_TFoo_GetValue_14);
    a.bind(class_TFoo_GetValue_6);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.push(x86::rcx); // Self
    a.sub(x86::rsp, 256); // class method locals
    a.mov(x86::rax, x86::qword_ptr(x86::rbp, -8)); // Self
    a.mov(x86::eax, x86::dword_ptr(x86::rax, 0)); // Self.FValue
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(skip_class_TFoo_GetValue_14);
    a.push(x86::r12);
    a.push(x86::rbx);
    a.sub(x86::rsp, 8); // align stack
    a.mov (x86::r12, x86::rcx); // ctx
    a.mov(x86::rax, imm((uint64_t)&str_4));
    a.mov(x86::rcx, x86::rax);
    a.mov(x86::rax, imm((uint64_t)&_jit_dynstring_from_cstr));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.push(x86::rax); // ctor string arg
    a.mov(x86::rcx, 4);
    a.mov(x86::rax, imm((uint64_t)&_jit_new_memory));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, x86::rax);  // self
    a.pop(x86::rdx);  // ctor arg {index + 1}
    a.push(x86::rcx);  // save constructor result object
    a.sub(x86::rsp, 32);
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::class_TFoo_Create_3);
    a.add(x86::rsp, 32);
    a.add(x86::add, 32);
    a.pop(x86::rax);  // constructor result
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // object foo
    a.mov(x86::rcx, imm((uint64_t)str_5));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_debug_break));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, imm((uint64_t)str_6));
    a.mov(x86::rax, imm((uint64_t)&_jit_print_text));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&_jit_print_newline));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::rax, x86::qword_ptr(x86::rax, 0)); // object foo
    Label free_nil_15 = a.new_label();
    Label free_end_16 = a.new_label();
    a.test(x86::rax, x86::rax);
    a.jz(free_nil_15);
    a.push(x86::rax); // save object for dispose
    a.mov(x86::rcx, x86::rax); // Self
    a.sub(x86::rsp, 32);
    a.call(class_TFoo_Destroy_5);
    a.add(x86::rsp, 32);
    a.pop(x86::rcx);
    a.mov(x86::rax, imm((uint64_t)&_jit_dispose_memory));
    a.sub(x86::rsp, 32);  // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.xor_(x86::rax, x86::rax);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, pointr_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // object foo
    a.jmp(free_end_16);
    a.bind(free_nil_15);
    a.bind(free_end_16);
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
  if (err != Error::kOk) {{
      std::cerr << "AsmJit error: " << DebugUtils::error_as_string(err) << std::endl;
      return 1;
  }}

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
    
    _jit_symbols_add(symbols);
  symbols.apply(asm_text);

  LabelMappings labels;
  labels.add("L0", "class_TFoo_SetValue_1");
    labels.add("L1", "class_TFoo_Create_2");
    labels.add("L2", "class_TFoo_Create_3");
    labels.add("L3", "class_TFoo_Create_4");
    labels.add("L4", "class_TFoo_Destroy_5");
    labels.add("L5", "class_TFoo_GetValue_6");
    labels.add("L6", "func_Add_7");
    labels.add("func_Add_7", "_ADD$INTEGER$INTEGER");
    labels.add("L8", "endfunc_Add_8");
    labels.add("L9", "skip_class_TFoo_Create_9");
    labels.add("L10", "skip_class_TFoo_Create_10");
    labels.add("L11", "skip_class_TFoo_Create_11");
    labels.add("L12", "skip_class_TFoo_Destroy_12");
    labels.add("L13", "skip_class_TFoo_SetValue_13");
    labels.add("L14", "skip_class_TFoo_GetValue_14");
    labels.add("L15", "free_nil_15");
    labels.add("L16", "free_end_16");
  labels.apply(asm_text);

  replace_all_ptr(asm_text);
  replace_all(asm_text, "mov r12, rcx", "lea r12, [rel ctx]");

  replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]"        );
replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]"     );
replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.string_vars]"     );
replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.record_vars]"     );
replace_all(asm_text, "[r12+32]",  "[r12 + JitContext.arrays_vars]"     );
replace_all(asm_text, "[r12+40]",  "[r12 + JitContext.pointr_vars]"     );
replace_all(asm_text, "[r12+48]",  "[r12 + JitContext.print_int_tmp]"   );
replace_all(asm_text, "[r12+56]",  "[r12 + JitContext.print_double_tmp]");


  asm_out << std::endl << "; -----------------------------------------------------------------------------"
asm_out << std::endl << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-16"
asm_out << std::endl << "; Copyright (c) 2026 by Jens Kallup - paule32"
asm_out << std::endl << "; all rights reserved."
asm_out << std::endl << "; -----------------------------------------------------------------------------"


  asm_out << "struc JitContext
";
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
asm_out << "extern _jit_debug_break" << std::endl;
asm_out << std::endl;
asm_out << "extern _jit_ExitProcess" << std::endl;


  asm_out << std::endl << "section .data" << std::endl;
asm_out << "ctx:" << std::endl;
asm_out << "    istruc JitContext" << std::endl;
asm_out << "        at JitContext.int_vars,         dq int_vars"    << std::endl;
asm_out << "        at JitContext.double_vars,      dq double_vars" << std::endl;
asm_out << "        at JitContext.string_vars,      dq string_vars" << std::endl;
asm_out << "        at JitContext.record_vars,      dq record_vars" << std::endl;
asm_out << "        at JitContext.arrays_vars,      dq arrays_vars" << std::endl;
asm_out << "        at JitContext.pointr_vars,      dq pointr_vars" << std::endl;
asm_out << "        at JitContext.print_int_tmp,    dd 0" << std::endl;
asm_out << "        at JitContext.print_double_tmp, dq 0" << std::endl;
asm_out << "    iend" << std::endl;
asm_out << std::endl;
asm_out << "int_vars:    times 1 dd 0"  << std::endl;
asm_out << "double_vars: times 1 dq 0" << std::endl;
asm_out << "string_vars: times 1 dq 0" << std::endl;
asm_out << "record_vars: times 1 db 0" << std::endl;
asm_out << "arrays_vars: times 1 db 0" << std::endl;
asm_out << "pointr_vars: times 1 dq 0" << std::endl;
asm_out << std::endl;



    asm_out << std::endl;
    asm_out << "dbase2many_module_kind dq {self.module_kind_value}" << std::endl;
    asm_out << "dbase2many_module_kind_program  equ 1" << std::endl;
    asm_out << "dbase2many_module_kind_unit     equ 2" << std::endl;
    asm_out << "dbase2many_module_kind_library  equ 3" << std::endl << std::endl;

    asm_out << std::endl;
    asm_out << "section .text" << std::endl;
    asm_out << "global " << "_main" << std::endl;
   
    asm_out << "_main" << ":" << std::endl;

    asm_out << asm_text;

    
    asm_out << std::endl << "section .data" << std::endl;
    asm_out << "_str_0 db \"TFoo: Create\", 0" << std::endl;
    asm_out << "_str_1 db \"TFoo: Create(S: String)\", 0" << std::endl;
    asm_out << "_str_2 db \"TFoo: Create(I1, I2: Integer)\", 0" << std::endl;
    asm_out << "_str_3 db \"TFoo: Destroy\", 0" << std::endl;
    asm_out << "_str_4 db \"TFoo: String\", 0" << std::endl;
    asm_out << "_str_5 db \"before break\", 0" << std::endl;
    asm_out << "_str_6 db \"after break\", 0" << std::endl;

    std::string final_asm_text = asm_out.str();

    if (!write_formatted_asm_file(
        final_asm_text.c_str(),
        "T:\GitHub\dBase2Many\src\asmjit\x64\test56.asm")) {
        std::cerr << "Could not write ASM file: T:\GitHub\dBase2Many\src\asmjit\x64\test56.asm" << std::endl;
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

