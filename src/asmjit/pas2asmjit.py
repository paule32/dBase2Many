# ---------------------------------------------------------------------------
# File:   pascal2asmjit.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
import sys
import os
from antlr4 import *

from parsers.pascal.MiniPascalLexer          import MiniPascalLexer
from parsers.pascal.MiniPascalParser         import MiniPascalParser
from parsers.pascal.MiniPascalParserVisitor  import MiniPascalParserVisitor

# ---------------------------------------------------------------------------
# used error code to information text map ...
# ---------------------------------------------------------------------------
ERROR_MAP = {
    "E0001": "Identifier not found: {name}",
    "E0002": "Duplicate identifier: {name}",
    "E0003": "Variable not declared: {name}",
    "E0004": "Unknown type: {name}",
    "E0005": "Incompatible types: got {got}, expected {expected}",
    "E0006": "Illegal assignment",
    "E0007": "Variable identifier expected",
    "E0008": "Unknown type",
    "E0009": "Duplicate variable declaration",
    "E0010": "Constant cannot be assigned",
}

# ---------------------------------------------------------------------------
# Compiler Exception to mark errors in compilation unit ...
# ---------------------------------------------------------------------------
class CompileError(Exception):
    def __init__(self, ctx, code, **params):
        token       = ctx.start if hasattr(ctx, "start") else ctx
        
        self.line   = token.line
        self.column = token.column
        self.code   = code
        self.params = params
        
        super().__init__(code)

# ---------------------------------------------------------------------------
# the transpiler generator for Pascal->Assembly
# ---------------------------------------------------------------------------
class AsmJitGenerator(MiniPascalParserVisitor):
    def __init__(self, asm_file = None):
        self.vars               = {}
        self.next_slot          = 0
        self.lines              = []
        self.program_name       = "Program"
        self.var_types          = {}
        self.cpp_print_lines    = []
        
        self.vars               = {}
        self.var_types          = {}

        self.int_slots          = {}
        self.double_slots       = {}

        self.next_int_slot      = 0
        self.next_double_slot   = 0
        
        self.asm_file           = asm_file
    
    def format_error(self, filename, err):
        template = ERROR_MAP.get(err.code, err.code)
        message  = template.format(**err.params)
        
        return f"{err.code}: {os.path.basename(filename)} {err.line}:{err.column} {message}"
    
    def is_double(self, typ):
        return typ.lower() == "double"

    def is_integer(self, typ):
        return typ.lower() == "integer"
        
    def declare_var(self, ctx, name, vtype):
        key = name.lower()
        typ = vtype.lower()

        if key in self.vars:
            raise CompileError(ctx, "E0002", name=name)

        if typ == "integer":
            slot = self.next_int_slot
            self.next_int_slot += 1
        elif typ == "double":
            slot = self.next_double_slot
            self.next_double_slot += 1
        else:
            raise CompileError(ctx, "E0004", name=vtype)

        self.vars[key] = {
            "name": name,
            "type": typ,
            "slot": slot,
        }

        self.var_types[key] = typ
    
    def emit_load_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r10, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rax, {slot * 4})); // {name}")

        elif typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r10, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, {slot * 8})); // {name}")
    
    def emit_store_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r10, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::dword_ptr(x86::rax, {slot * 4}), x86::eax); // {name}")

        elif typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r10, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::qword_ptr(x86::rax, {slot * 8}), x86::xmm0); // {name}")
    
    def emit_int_to_double(self):
        self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
    
    def require_var(self, ctx, name):
        key = name.lower()
        
        if key not in self.vars:
            raise CompileError(ctx, "E0003", name=key)  # Variable not declared
        
        return self.vars[key]
    
    # typen überprüfung ...
    def var_info(self, ctx, name):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        return self.vars[key]

    def var_type_of(self, ctx, name):
        return self.var_info(ctx, name)["type"]

    def slot_for(self, ctx, name):
        return self.var_info(ctx, name)["slot"]
    
    
    def emit(self, line):
        self.lines.append("    " + line)
    
    def visitProgramFile(self, ctx):
        self.program_name = ctx.IDENT().getText()
        
        if ctx.varSection():
            self.visit(ctx.varSection())
            
        self.emit("a.mov(x86::r10, x86::rcx); // ctx")
        
        self.visit(ctx.block())
        return self.render_cpp()
    
    def visitBlock(self, ctx):
        return self.visit(ctx.statementList())
    
    def visitStatementList(self, ctx):
        for st in ctx.statement():
            self.visit(st)
    
    def visitStatement(self, ctx):
        if ctx.assignment():
            return self.visit(ctx.assignment())

        if ctx.writeLnStatement():
            return self.visit(ctx.writeLnStatement())

        return None

    def visitVarSection(self, ctx):
        for decl in ctx.varDeclaration():
            self.visit(decl)
        return None

    def visitVarDeclaration(self, ctx):
        vtype = ctx.typeName().getText()

        for ident in ctx.identList().IDENT():
            self.declare_var(ident.symbol, ident.getText(), vtype)
            
        return None
    
    def visitAssignment(self, ctx):
        name = ctx.IDENT().getText()
        info = self.var_info(ctx, name)

        target_type = info["type"]
        expr_type = self.visit(ctx.expr())

        if target_type == "integer" and expr_type == "double":
            raise CompileError(ctx, "E0005", got=expr_type, expected=target_type)

        if target_type == "double" and expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")

        self.emit_store_var(name, info)
        return None
    
    def visitExpr(self, ctx):
        result_type = self.visit(ctx.term(0))

        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()

            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

            right_type = self.visit(ctx.term(i))

            self.emit("a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")

            if op == "+":
                self.emit("a.addsd(x86::xmm0, x86::xmm1);")
            elif op == "-":
                self.emit("a.movapd(x86::xmm2, x86::xmm0);")
                self.emit("a.movapd(x86::xmm0, x86::xmm1);")
                self.emit("a.subsd(x86::xmm0, x86::xmm2);")

            if result_type == "double" or right_type == "double":
                result_type = "double"
            else:
                result_type = "integer"

        return result_type
    
    def visitTerm(self, ctx):
        result_type = self.visit(ctx.factor(0))

        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()

            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

            right_type = self.visit(ctx.factor(i))

            self.emit("a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")

            if op == "*":
                self.emit("a.mulsd(x86::xmm0, x86::xmm1);")
            elif op == "/":
                self.emit("a.movapd(x86::xmm2, x86::xmm0);")
                self.emit("a.movapd(x86::xmm0, x86::xmm1);")
                self.emit("a.divsd(x86::xmm0, x86::xmm2);")

            if op == "/" or result_type == "double" or right_type == "double":
                result_type = "double"
            else:
                result_type = "integer"

        return result_type
    
    def visitFactor(self, ctx):
        if ctx.NUMBER():
            value = ctx.NUMBER().getText()
            
            self.emit(f"a.mov(x86::eax, {value});")
            return "integer"

        elif ctx.HEXNUMBER():
            text  = ctx.HEXNUMBER().getText()
            value = int(text[1:], 16)
            
            self.emit(f"a.mov(x86::eax, {value}); // {text}")
            return "integer"

        elif ctx.FLOATNUMBER():
            value = ctx.FLOATNUMBER().getText()
            
            self.emit(f"a.mov(x86::rax, imm(double_to_bits({value})));")
            self.emit("a.movq(x86::xmm0, x86::rax);")
            return "double"
            
        elif ctx.IDENT():
            name = ctx.IDENT().getText()
            info = self.var_info(ctx, name)

            self.emit_load_var(name, info)
            return info["type"]
            
        else:
            return self.visit(ctx.expr())
    
    def visitWriteLnStatement(self, ctx):
        args = ctx.writeArgList()

        if args:
            for arg in args.writeArg():
                text = arg.getText()

                if arg.STRING():
                    value = text[1:-1]
                    self.cpp_print_lines.append(
                        f'    std::cout << "{self.cpp_escape(value)}";'
                    )
                else:
                    expr_type = self.visit(arg.expr())
                    if expr_type == "integer":
                        self.emit(
                            "a.mov(x86::dword_ptr(x86::r10, "
                            "offsetof(JitContext, print_int_tmp)), x86::eax);"
                        )
                        self.cpp_print_lines.append(
                            "    std::cout << ctx.print_int_tmp;"
                        )
                    elif expr_type == "double":
                        self.emit(
                            "a.movsd(x86::qword_ptr(x86::r10, "
                            "offsetof(JitContext, print_double_tmp)), x86::xmm0);"
                        )
                        self.cpp_print_lines.append(
                            "    std::cout << ctx.print_double_tmp;"
                        )

        self.cpp_print_lines.append("    std::cout << std::endl;")
        return None
    
    def cpp_escape(self, text):
        return (
            text
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
    
    def render_batch(self):
        with open("testout/run_test2.bat", "w", encoding="utf-8") as f:
            f.write("set PATH=T:\\msys64\\mingw64\\bin;%CD%;%PATH%\n")
            f.write("test2.exe")
            f.close()
        
    def render_cpp(self):
        body         = "\n".join(self.lines)
        
        var_count    = max(257, self.next_slot)
        int_count    = max(  1, self.next_int_slot)
        double_count = max(  1, self.next_double_slot)
        
        # todo !!!
        self.func_name = "main"
        
        self.render_batch()
        return f'''#include <asmjit/x86.h>
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

struct JitContext {{
    int*    int_vars;
    double* double_vars;

    int     print_int_tmp;
    double  print_double_tmp;
}};
typedef void (*JitFunc)(JitContext* ctx);

static uint64_t double_to_bits(double value) {{
    uint64_t bits;
    std::memcpy(&bits, &value, sizeof(bits));
    return bits;
}}

int main() {{
    JitRuntime rt;

    CodeHolder code;
    code.init(rt.environment());
    
    StringLogger logger;
    
    logger.options().set_indentation(FormatIndentationGroup::kCode, 1);
    logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);
    
    code.set_logger(&logger);
    x86::Assembler a(&code);

{body}
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {{
        std::cerr << \"AsmJit error: \" << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }}
    
    std::ofstream asm_out(\"{self.asm_file}\");

    std::string asm_text = logger.data();
    std::istringstream iss(asm_text);
    std::string line;

    asm_out << \"public \" << {self.func_name} << \"\\n\";
    asm_out << \"{self.func_name}\" << \":\\n\";
    
    while (std::getline(iss, line)) {{
        std::string s = line;

        // führende Leerzeichen entfernen
        size_t start = s.find_first_not_of(\" \\t\");
        if (start == std::string::npos) {{
            asm_out << \"\\n\";
            continue;
        }}

        s = s.substr(start);

        // erstes Leerzeichen nach Mnemonic suchen
        size_t pos = s.find_first_of(\" \\t\");

        if (pos != std::string::npos) {{
            std::string mnemonic = s.substr(0, pos);
            std::string rest = s.substr(pos);
            size_t rest_start = rest.find_first_not_of(\" \\t\");

            if (rest_start != std::string::npos)
                rest = rest.substr(rest_start);
            else
                rest.clear();

            asm_out << \"\\t\" << mnemonic << \"\\t\" << rest << \"\\n\";
        }} else {{
            asm_out << \"\\t\" << s << \"\\n\";
        }}
    }}

    asm_out.close();
   
    std::array<int, {int_count}> int_vars{{}};
    std::array<double, {double_count}> double_vars{{}};
    
    JitContext ctx{{}};
    ctx.int_vars = int_vars.data();
    ctx.double_vars = double_vars.data();
    
    fn(&ctx);

{self.render_print_output()}

    rt.release(fn);
    return 0;
}}
'''

    def render_variable_output(self):
        out = []

        for key, info in sorted(self.vars.items(), key=lambda x: x[1]["slot"]):
            name = info["name"]
            typ  = info["type"]
            slot = info["slot"]

            if typ == "integer":
                out.append(
                    f'    std::cout << "{name} = " << int_vars[{slot}] << std::endl;'
                )
            elif typ == "double":
                out.append(
                    f'    std::cout << "{name} = " << double_vars[{slot}] << std::endl;'
                )

        return "\\n".join(out)
        
    def render_print_output(self):
        return "\n".join(self.cpp_print_lines)

def main():
    if len(sys.argv) != 2:
        print("Usage: python pascal_to_asmjit.py file.pas", file=sys.stderr)
        return 1
    
    generator   = None
    source_file = ""
    
    try:
        source_file = sys.argv[1]
        base_name   = os.path.basename(source_file)
        asm_file    = os.path.splitext(base_name)[0] + ".asm"
        
        stream = FileStream(sys.argv[1], encoding="utf-8")
        lexer  = MiniPascalLexer(stream)
        tokens = CommonTokenStream(lexer)
        parser = MiniPascalParser(tokens)
        
        tree = parser.programFile()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            return 1
        
        generator = AsmJitGenerator(asm_file)
        cpp = generator.visit(tree)
        print(cpp)
        return 0
        
    except CompileError as e:
        if generator is not None:
            print(generator.format_error(source_file, e), file = sys.stderr)
            return 2
        else:
            print(e, file = sys.stderr)
            return 2
            
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
