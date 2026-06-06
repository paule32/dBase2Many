// ---------------------------------------------------------------------------
// \file misc.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

void
replace_all_str(
    std::string&   asm_text,
    std::ofstream& asm_out)
{
    std::istringstream iss(asm_text);
    std::string line;

    while (std::getline(iss, line)) {
        std::string s = line;

        // führende Leerzeichen entfernen
        size_t start = s.find_first_not_of(" \t");
        if (start == std::string::npos) {
            asm_out << std::endl;
            continue;
        }

        s = s.substr(start);
        
        // Labels linksbündig ausgeben: L0:
        if (!s.empty() && s.back() == ':') {
            asm_out << s << std::endl;
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
                }   else {
                    mnemonic = s;
                    rest.clear();
                }
            }
            asm_out << "\t" << mnemonic << "\t" << rest << std::endl;
        }   else {
            asm_out << "\t" << s << std::endl;
        }
    }
}

uint64_t
double_to_bits(double value) {
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(bits));
    return bits;
}

void
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

std::string&
replace_all_ptr(std::string& asm_text)
{
    replace_all(asm_text, "byte ptr ",    "byte ");
    replace_all(asm_text, "word ptr ",    "word ");
    replace_all(asm_text, "dword ptr ",   "dword ");
    replace_all(asm_text, "qword ptr ",   "qword ");
    replace_all(asm_text, "xmmword ptr ", "xmmword ");
    
    return asm_text;
}

std::string&
replace_all_fun(std::string& asm_text)
{
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_text),    "_jit_print_text");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_int),     "_jit_print_int");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_double),  "_jit_print_double");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    
    return asm_text;
}
