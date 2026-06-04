// automaically created per Python 3.14 script on: 2026-06-04
//
// DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !
// Copyright (c) 2026 by Jens Kallup - paule32
// all rights reserved.
//
# include <asmjit/x86.h>
# include <cstdio>
# include <cstdint>
# include <cstring>

# include <iostream>
# include <fstream>
# include <sstream>

# include <string>
# include <array>

using namespace std;
using namespace asmjit;

struct JitContext {
    int*            int_vars;
    double*         double_vars;
    const char**    string_vars;

    int             print_int_tmp;
    double          print_double_tmp;
};
typedef void (*JitFunc)(JitContext* ctx);

static uint64_t double_to_bits(double value) {
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(bits));
    return bits;
}

extern "C" void jit_print_text(const char* s) { std::cout << s; }
extern "C" void jit_print_int(int v)          { std::cout << v; }
extern "C" void jit_print_double(double v)    { std::cout << v; }
extern "C" void jit_print_newline()           { std::cout << std::endl; }

static const char str_0[] = "Foo Fuu";
static const char str_1[] = "i : ";
static const char str_2[] = "d : ";
static const char str_3[] = "s : ";
static const char str_4[] = "Pi: ";

int main() {
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

    Label func_PiValue_1 = a.new_label();
    Label endfunc_PiValue_2 = a.new_label();
    a.jmp(endfunc_PiValue_2);
    a.bind(func_PiValue_1);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.sub(x86::rsp, 256); // local variables
    a.mov(x86::rax, imm(double_to_bits(3.1415926)));
    a.movq(x86::xmm0, x86::rax);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_PiValue_2);
    Label func_GetInteger_3 = a.new_label();
    Label endfunc_GetInteger_4 = a.new_label();
    a.jmp(endfunc_GetInteger_4);
    a.bind(func_GetInteger_3);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.sub(x86::rsp, 256); // local variables
    a.mov(x86::eax, 42);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_GetInteger_4);
    Label func_GetDouble_5 = a.new_label();
    Label endfunc_GetDouble_6 = a.new_label();
    a.jmp(endfunc_GetDouble_6);
    a.bind(func_GetDouble_5);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.sub(x86::rsp, 256); // local variables
    a.mov(x86::rax, imm(double_to_bits(12.34)));
    a.movq(x86::xmm0, x86::rax);
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_GetDouble_6);
    Label func_GetString_7 = a.new_label();
    Label endfunc_GetString_8 = a.new_label();
    a.jmp(endfunc_GetString_8);
    a.bind(func_GetString_7);
    a.push(x86::rbp);
    a.mov(x86::rbp, x86::rsp);
    a.sub(x86::rsp, 256); // local variables
    a.mov(x86::rax, imm((uint64_t)str_0));
    a.mov(x86::rsp, x86::rbp);
    a.pop(x86::rbp);
    a.ret();
    a.bind(endfunc_GetString_8);
    a.push(x86::r12);
    a.mov (x86::r12, x86::rcx); // ctx
    a.sub(x86::rsp, 32); // shadow space for parameterless function call
    a.call(func_GetInteger_3);
    a.add(x86::rsp, 32);
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));
    a.mov(x86::dword_ptr(x86::rax, 0), x86::ebx); // i
    a.sub(x86::rsp, 32); // shadow space for parameterless function call
    a.call(func_GetDouble_5);
    a.add(x86::rsp, 32);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));
    a.movsd(x86::qword_ptr(x86::r11, 0), x86::xmm0); // d
    a.sub(x86::rsp, 32); // shadow space for parameterless function call
    a.call(func_GetString_7);
    a.add(x86::rsp, 32);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, string_vars)));
    a.mov(x86::qword_ptr(x86::r11, 0), x86::rax); // s
    a.mov(x86::rcx, imm((uint64_t)str_1));
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));
    a.mov(x86::eax, x86::dword_ptr(x86::rax, 0)); // i
    a.mov(x86::ecx, x86::eax);
    a.mov(x86::rax, imm((uint64_t)&jit_print_int));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, imm((uint64_t)str_2));
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));
    a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, 0)); // d
    a.mov(x86::rax, imm((uint64_t)&jit_print_double));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, imm((uint64_t)str_3));
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
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
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rcx, imm((uint64_t)str_4));
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.sub(x86::rsp, 32); // shadow space for parameterless function call
    a.call(func_PiValue_1);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_double));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.pop(x86::r12);
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {
        std::cerr << "AsmJit error: " << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }
    
    std::ofstream asm_out("test15.asm");
    std::string asm_text = logger.data();
    
    auto replace_all = [](std::string& s, const std::string& from, const std::string& to) {
        if (from.empty())
            return;

        size_t pos = 0;

        while ((pos = s.find(from, pos)) != std::string::npos) {
            s.replace(pos, from.length(), to);
            pos += std::max<size_t>(to.length(), 1);
        }
    };

    replace_all(asm_text, std::to_string((uint64_t)&jit_print_text),    "_jit_print_text");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_int),     "_jit_print_int");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_double),  "_jit_print_double");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    
    replace_all(asm_text, std::to_string((uint64_t)&str_0), "_str_0");
    replace_all(asm_text, std::to_string((uint64_t)&str_1), "_str_1");
    replace_all(asm_text, std::to_string((uint64_t)&str_2), "_str_2");
    replace_all(asm_text, std::to_string((uint64_t)&str_3), "_str_3");
    replace_all(asm_text, std::to_string((uint64_t)&str_4), "_str_4");
    
    replace_all(asm_text, "L0:", "func_PiValue_1:");
    replace_all(asm_text, "L0", "func_PiValue_1");
    replace_all(asm_text, "L1:", "endfunc_PiValue_2:");
    replace_all(asm_text, "L1", "endfunc_PiValue_2");
    replace_all(asm_text, "L2:", "func_GetInteger_3:");
    replace_all(asm_text, "L2", "func_GetInteger_3");
    replace_all(asm_text, "L3:", "endfunc_GetInteger_4:");
    replace_all(asm_text, "L3", "endfunc_GetInteger_4");
    replace_all(asm_text, "L4:", "func_GetDouble_5:");
    replace_all(asm_text, "L4", "func_GetDouble_5");
    replace_all(asm_text, "L5:", "endfunc_GetDouble_6:");
    replace_all(asm_text, "L5", "endfunc_GetDouble_6");
    replace_all(asm_text, "L6:", "func_GetString_7:");
    replace_all(asm_text, "L6", "func_GetString_7");
    replace_all(asm_text, "L7:", "endfunc_GetString_8:");
    replace_all(asm_text, "L7", "endfunc_GetString_8");

    replace_all(asm_text, "byte ptr ",    "byte ");
    replace_all(asm_text, "word ptr ",    "word ");
    replace_all(asm_text, "dword ptr ",   "dword ");
    replace_all(asm_text, "qword ptr ",   "qword ");
    replace_all(asm_text, "xmmword ptr ", "xmmword ");
    
    
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.print_double_tmp]");
    
    
    
    asm_out << "; -----------------------------------------------------------------------------\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-04\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\n";
    asm_out << "; all rights reserved.\n";
    asm_out << "; -----------------------------------------------------------------------------\n\n";
    
    
    asm_out << "struc JitContext\n";
    asm_out << "    .int_vars:         resq 1\n";
    asm_out << "    .double_vars:      resq 1\n";
    asm_out << "    .print_int_tmp:    resd 1\n";
    asm_out << "    .print_double_tmp: resq 1\n";
    asm_out << "endstruc\n\n";
    
    
    replace_all(asm_text, std::to_string(double_to_bits(3.1415926)), "dbl_3_1415926_0");
    replace_all(asm_text, std::to_string(double_to_bits(12.34)), "dbl_12_34_1");
    asm_out << "\n";

    std::istringstream iss(asm_text);
    std::string line;

    asm_out << "dbl_3_1415926_0 equ " << std::to_string(double_to_bits(3.1415926)) << " ; 3.1415926\n";
    asm_out << "dbl_12_34_1 equ " << std::to_string(double_to_bits(12.34)) << " ; 12.34\n";
    asm_out << "extern _jit_print_text\n";
    asm_out << "extern _jit_print_int\n";
    asm_out << "extern _jit_print_double\n";
    asm_out << "extern _jit_print_newline\n";
    
    asm_out << "\n";
    asm_out << "section .text\n";
    asm_out << "global " << "_main" << "\n";
    asm_out << "_main" << ":\n";
    
    while (std::getline(iss, line)) {
        std::string s = line;

        // führende Leerzeichen entfernen
        size_t start = s.find_first_not_of(" \t");
        if (start == std::string::npos) {
            asm_out << "\n";
            continue;
        }

        s = s.substr(start);
        
        // Labels linksbündig ausgeben: L0:
        if (!s.empty() && s.back() == ':') {
            asm_out << s << "\n";
            continue;
        }

        // erstes Leerzeichen nach Mnemonic suchen
        size_t pos = s.find_first_of(" \t");

        if (pos != std::string::npos) {
            std::string mnemonic = s.substr(0, pos);
            std::string rest = s.substr(pos);
            size_t rest_start = rest.find_first_not_of(" \t");

            if (rest_start != std::string::npos)
                rest = rest.substr(rest_start);
            else
                rest.clear();
            
            // short jmp <label>
            if (mnemonic == "short") {
                size_t rest_start = rest.find_first_not_of(" \t");

                if (rest_start != std::string::npos)
                    s = rest.substr(rest_start);
                else
                    s.clear();

                pos = s.find_first_of(" \t");

                if (pos != std::string::npos) {
                    mnemonic = s.substr(0, pos);
                    rest = s.substr(pos);
                } else {
                    mnemonic = s;
                    rest.clear();
                }
            }
            asm_out << "\t" << mnemonic << "\t" << rest << "\n";
        } else {
            asm_out << "\t" << s << "\n";
        }
    }
    
    asm_out << "\nsection .data\n";
    asm_out << "_str_0 db \"Foo Fuu\", 0\n";
    asm_out << "_str_1 db \"i : \", 0\n";
    asm_out << "_str_2 db \"d : \", 0\n";
    asm_out << "_str_3 db \"s : \", 0\n";
    asm_out << "_str_4 db \"Pi: \", 0\n";
    
    asm_out.close();
   
    std::array<int,         1> int_vars{};
    std::array<double,      1> double_vars{};
    std::array<const char*, 1> string_vars{};
    
    JitContext ctx{};
    ctx.int_vars    = int_vars.data();
    ctx.double_vars = double_vars.data();
    ctx.string_vars = string_vars.data();
    
    fn(&ctx);

    rt.release(fn);
    return 0;
}

