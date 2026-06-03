// automaically created per Python 3.14 script on: 2026-06-03
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
    int*    int_vars;
    double* double_vars;

    int     print_int_tmp;
    double  print_double_tmp;
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

static const char str_0[] = "text";
static const char str_1[] = "x = ";

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
    a.mov (x86::r12, x86::rcx); // ctx
    a.mov(x86::rcx, imm((uint64_t)str_0));
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, imm((uint64_t)&jit_print_newline));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::eax, 10);
    a.push(x86::rax);
    a.mov(x86::rax, imm(double_to_bits(20.214))); // dbl_20_214_0
    a.movq(x86::xmm0, x86::rax);
    a.pop(x86::rax);
    a.cvtsi2sd(x86::xmm1, x86::eax);
    a.sub(x86::rsp, 8);
    a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);
    a.mov(x86::rax, imm(double_to_bits(20.214))); // dbl_20_214_1
    a.movq(x86::xmm0, x86::rax);
    a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));
    a.add(x86::rsp, 8);
    a.addsd(x86::xmm0, x86::xmm1);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));
    a.movsd(x86::qword_ptr(x86::r11, 0), x86::xmm0); // x
    a.mov(x86::rcx, imm((uint64_t)str_1));
    a.mov(x86::rax, imm((uint64_t)&jit_print_text));
    a.sub(x86::rsp, 32); // Windows x64 shadow space
    a.call(x86::rax);
    a.add(x86::rsp, 32);
    a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));
    a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, 0)); // x
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
    
    std::ofstream asm_out("test2.asm");
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
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-03\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\n";
    asm_out << "; all rights reserved.\n";
    asm_out << "; -----------------------------------------------------------------------------\n\n";
    
    
    asm_out << "struc JitContext\n";
    asm_out << "    .int_vars:         resq 1\n";
    asm_out << "    .double_vars:      resq 1\n";
    asm_out << "    .print_int_tmp:    resd 1\n";
    asm_out << "    .print_double_tmp: resq 1\n";
    asm_out << "endstruc\n\n";
    
    
    replace_all(asm_text, std::to_string(double_to_bits(20.214)), "dbl_20_214_0");
    replace_all(asm_text, std::to_string(double_to_bits(20.214)), "dbl_20_214_1");
    asm_out << "\n";

    std::istringstream iss(asm_text);
    std::string line;

    asm_out << "dbl_20_214_0 equ " << std::to_string(double_to_bits(20.214)) << " ; 20.214\n";
    asm_out << "dbl_20_214_1 equ " << std::to_string(double_to_bits(20.214)) << " ; 20.214\n";
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
    asm_out << "_str_0 db \"text\", 0\n";
    asm_out << "_str_1 db \"x = \", 0\n";
    
    asm_out.close();
   
    std::array<int,    1> int_vars{};
    std::array<double, 1> double_vars{};
    
    JitContext ctx{};
    ctx.int_vars = int_vars.data();
    ctx.double_vars = double_vars.data();
    
    fn(&ctx);

    rt.release(fn);
    return 0;
}

