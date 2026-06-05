// automaically created per Python 3.14 script on: 2026-06-05
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
# include <vector>
# include <algorithm>

using namespace std;
using namespace asmjit;

struct JitContext {
    int*            int_vars;
    
    double *        double_vars;
    const char **   string_vars;
    uint8_t *       record_vars;
    uint8_t *       arrays_vars;

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



static void
replace_all(
    std::string& s,
    const std::string& from,
    const std::string& to) {
    
    if (from.empty())
        return;

    size_t pos = 0;

    while ((pos = s.find(from, pos)) != std::string::npos) {
        s.replace(pos, from.length(), to);
        pos += std::max<size_t>(to.length(), 1);
    }
}
    
struct LabelMapping
{
    std::string asmjitLabel;
    std::string targetLabel;

    LabelMapping(
        const std::string& asmjit,
        const std::string& target)
        :
        asmjitLabel(asmjit),
        targetLabel(target)
    {
    }
};

struct SymbolMapping
{
    std::string addressText;
    std::string symbolName;

    SymbolMapping(
        const std::string& address,
        const std::string& symbol)
        :
        addressText(address),
        symbolName(symbol)
    {
    }
};

class LabelMappings
{
public:
    void add(
        const std::string& asmjitLabel,
        const std::string& targetLabel)
    {
        mappings.emplace_back(
            asmjitLabel,
            targetLabel);
    }

    void clear()
    {
        mappings.clear();
    }

    void remove(const std::string& asmjitLabel)
    {
        mappings.erase(
            std::remove_if(
                mappings.begin(),
                mappings.end(),
                [&](const LabelMapping& item)
                {
                    return item.asmjitLabel == asmjitLabel;
                }),
            mappings.end());
    }

    void apply(std::string& asm_text)
    {
        for (const auto& item : mappings)
        {
            replace_all(
                asm_text,
                item.asmjitLabel + ":",
                item.targetLabel + ":");

            replace_all(
                asm_text,
                item.asmjitLabel,
                item.targetLabel);
        }
    }

private:
    std::vector<LabelMapping> mappings;
};

class SymbolMappings
{
private:
    std::vector<SymbolMapping> mappings;

public:
    void add(
        const std::string& addressText,
        const std::string& symbolName)
    {
        mappings.emplace_back(addressText, symbolName);
    }

    void apply(std::string& asm_text)
    {
        for (const auto& item : mappings)
        {
            replace_all(
                asm_text,
                item.addressText,
                item.symbolName);
        }
    }
};

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
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.mov(x86::dword_ptr(x86::r11, 0), 1); // init a[0]
    a.mov(x86::dword_ptr(x86::r11, 4), 2); // init a[1]
    a.mov(x86::dword_ptr(x86::r11, 8), 3); // init a[2]
    a.mov(x86::dword_ptr(x86::r11, 12), 4); // init a[3]
    a.mov(x86::dword_ptr(x86::r11, 16), 5); // init a[4]
    a.mov(x86::dword_ptr(x86::r11, 20), 6); // init a[5]
    a.mov(x86::dword_ptr(x86::r11, 24), 7); // init a[6]
    a.mov(x86::dword_ptr(x86::r11, 28), 8); // init a[7]
    a.mov(x86::eax, 2);
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
    a.mov(x86::eax, x86::dword_ptr(x86::r11));
    a.push(x86::rax);
    a.mov(x86::eax, 10);
    a.mov(x86::ebx, x86::eax);
    a.pop(x86::rax);
    a.add(x86::eax, x86::ebx);
    a.mov(x86::ebx, x86::eax);
    a.mov(x86::eax, 0);
    a.imul(x86::eax, x86::eax, 4);
    a.add(x86::eax, 0);
    a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, arrays_vars)));
    a.movsxd(x86::rax, x86::eax);
    a.add(x86::r11, x86::rax);
    a.mov(x86::dword_ptr(x86::r11), x86::ebx);
    a.mov(x86::eax, 0);
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
    a.pop(x86::r12);
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {
        std::cerr << "AsmJit error: " << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }
    
    std::ofstream asm_out("test19.asm");
    std::string asm_text = logger.data();

    replace_all(asm_text, std::to_string((uint64_t)&jit_print_text),    "_jit_print_text");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_int),     "_jit_print_int");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_double),  "_jit_print_double");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    
    SymbolMappings symbols;
    
    symbols.apply(asm_text);
    
    LabelMappings labels;
    
    labels.apply(asm_text);

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
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: 2026-06-05\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\n";
    asm_out << "; all rights reserved.\n";
    asm_out << "; -----------------------------------------------------------------------------\n\n";
    
    
    asm_out << "struc JitContext\n";
    asm_out << "    .int_vars:         resq 1\n";
    asm_out << "    .double_vars:      resq 1\n";
    asm_out << "    .print_int_tmp:    resd 1\n";
    asm_out << "    .print_double_tmp: resq 1\n";
    asm_out << "endstruc\n\n";
    
    
    
    asm_out << "\n";

    std::istringstream iss(asm_text);
    std::string line;

    
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
    
    asm_out.close();
   
    std::array<int,         1> int_vars{};
    std::array<double,      1> double_vars{};
    std::array<const char*, 1> string_vars{};
    std::array<uint8_t,     1> record_vars{};
    std::array<uint8_t,     40> arrays_vars{};
    
    JitContext ctx{};
    ctx.int_vars    = int_vars.data();
    
    ctx.double_vars = double_vars.data();
    ctx.string_vars = string_vars.data();
    ctx.record_vars = record_vars.data();
    ctx.arrays_vars = arrays_vars.data();
    
    fn(&ctx);

    rt.release(fn);
    return 0;
}

