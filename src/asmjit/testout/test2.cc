#include <asmjit/x86.h>
#include <cstdio>
#include <cstdint>
#include <cstring>

#include <iostream>
#include <fstream>
#include <sstream>

#include <string>
#include <array>

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

int main() {
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

    a.mov(x86::r10, x86::rcx); // ctx
    a.mov(x86::eax, 10);
    a.sub(x86::rsp, 8);
    a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);
    a.mov(x86::rax, imm(double_to_bits(20.214)));
    a.movq(x86::xmm0, x86::rax);
    a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));
    a.add(x86::rsp, 8);
    a.addsd(x86::xmm0, x86::xmm1);
    a.mov(x86::rax, x86::qword_ptr(x86::r10, offsetof(JitContext, double_vars)));
    a.movsd(x86::qword_ptr(x86::rax, 0), x86::xmm0); // x
    a.mov(x86::rax, x86::qword_ptr(x86::r10, offsetof(JitContext, double_vars)));
    a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, 0)); // x
    a.movsd(x86::qword_ptr(x86::r10, offsetof(JitContext, print_double_tmp)), x86::xmm0);
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {
        std::cerr << "AsmJit error: " << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }
    
    std::ofstream asm_out("test2.asm");

    std::string asm_text = logger.data();
    std::istringstream iss(asm_text);
    std::string line;

    asm_out << "public " << main << "\n";
    asm_out << "main" << ":\n";
    
    while (std::getline(iss, line)) {
        std::string s = line;

        // führende Leerzeichen entfernen
        size_t start = s.find_first_not_of(" \t");
        if (start == std::string::npos) {
            asm_out << "\n";
            continue;
        }

        s = s.substr(start);

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

            asm_out << "\t" << mnemonic << "\t" << rest << "\n";
        } else {
            asm_out << "\t" << s << "\n";
        }
    }

    asm_out.close();
   
    std::array<int, 1> int_vars{};
    std::array<double, 1> double_vars{};
    
    JitContext ctx{};
    ctx.int_vars = int_vars.data();
    ctx.double_vars = double_vars.data();
    
    fn(&ctx);

    std::cout << "text";
    std::cout << std::endl;
    std::cout << "x = ";
    std::cout << ctx.print_double_tmp;
    std::cout << std::endl;

    rt.release(fn);
    return 0;
}

