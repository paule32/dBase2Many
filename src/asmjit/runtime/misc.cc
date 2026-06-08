// ---------------------------------------------------------------------------
// \file misc.cc
// \note Copyright (c) 2026 by Jens Kallup - paule32
//       all rights reserved.
// ---------------------------------------------------------------------------
# include "dbase2many.hpp"

std::string
format_asm_line(
    const std::string& line) {
    
    std::string s = line;
    
    if (s.empty())
        return s;

    // Labels/Leerzeilen/Kommentare unverändert lassen
    size_t pos = s.find_first_not_of(" \t");
    if (pos == std::string::npos)
        return "";

    if (s[pos] == ';' || s.find(':') != std::string::npos)
        return s.substr(pos);

    s = s.substr(pos);
    
    // erstes Wort = Mnemonic
    size_t mnemonic_end = s.find_first_of(" \t");
    if (mnemonic_end == std::string::npos)
        return "    " + s;

    std::string mnemonic = s.substr(0, mnemonic_end);

    // Operandenteil suchen
    size_t operand_start = s.find_first_not_of(" \t", mnemonic_end);
    if (operand_start == std::string::npos)
        return "    " + mnemonic;

    std::string operands = s.substr(operand_start);

    // Zielspalte für Operanden, z.B. Spalte 8
    const size_t operand_column = 12;

    std::string out = "    " + mnemonic;

    if (out.length() < operand_column)
        out += std::string(operand_column - out.length(), ' ');
    else
        out += "    ";

    out += operands;
    return out;
}

void
replace_all_str(
    std::string&   asm_text,
    std::ofstream& asm_out) {
    
    std::istringstream iss(asm_text);
    std::string line;
    
    while (std::getline(iss, line)) {
        asm_out << format_asm_line(line) << std::endl;
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
