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
        
        self.label_id           = 0
        
        self.string_literals    = []
        self.double_literals    = []
        
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
    
    def emit_call_rax(self):
        self.emit("a.sub(x86::rsp, 32); // Windows x64 shadow space")
        self.emit("a.call(x86::rax);")
        self.emit("a.add(x86::rsp, 32);")
    
    def emit_load_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::dword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rax, {slot * 4})); // {name}")

        elif typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, {slot * 8})); // {name}")
    
    def emit_store_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::dword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::dword_ptr(x86::rax, {slot * 4}), x86::eax); // {name}")

        elif typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
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
    
    def render_asm_double_replacements(self):
        out = []
        for name, value in self.double_literals:
            out.append(
                f'replace_all(asm_text, std::to_string(double_to_bits({value})), "{name}");'
            )
        return "\n    ".join(out)
    
    def var_type_of(self, ctx, name):
        return self.var_info(ctx, name)["type"]

    def slot_for(self, ctx, name):
        return self.var_info(ctx, name)["slot"]
    
    def emit(self, line):
        self.lines.append("    " + line)
    
    def new_label_name(self, prefix):
        self.label_id += 1
        return f"{prefix}_{self.label_id}"
    
    def add_string_literal(self, text):
        name = f"str_{len(self.string_literals)}"
        self.string_literals.append((name, text))
        return name
    
    def add_double_literal(self, value):
        safe = value.replace(".", "_").replace("-", "minus_")
        name = f"dbl_{safe}_{len(self.double_literals)}"
        self.double_literals.append((name, value))
        return name
    
    def visitProgramFile(self, ctx):
        self.program_name = ctx.IDENT().getText()
        
        if ctx.varSection():
            self.visit(ctx.varSection())
            
        self.emit("a.push(x86::r12);")
        self.emit("a.mov (x86::r12, x86::rcx); // ctx")
        
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

        if ctx.ifStatement():
            return self.visit(ctx.ifStatement())

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
            label = self.add_double_literal(value)

            self.emit(f"a.mov(x86::rax, imm(double_to_bits({value}))); // {label}")
            self.emit("a.movq(x86::xmm0, x86::rax);")
            return "double"
            
        elif ctx.IDENT():
            name = ctx.IDENT().getText()
            info = self.var_info(ctx, name)

            self.emit_load_var(name, info)
            return info["type"]
            
        else:
            return self.visit(ctx.expr())
    
    def visitIfStatement(self, ctx):
        self.emit_if_statement(ctx)
        return None
    
    def emit_if_statement(self, ctx):
        else_label = self.new_label_name("else")
        end_label  = self.new_label_name("endif")

        self.emit(f"Label {else_label} = a.new_label();")
        self.emit(f"Label {end_label} = a.new_label();")

        self.emit_condition_jump_false(ctx.condition(), else_label)

        self.visit(ctx.statement(0))

        if ctx.ELSE():
            self.emit(f"a.jmp({end_label});")
            self.emit(f"a.bind({else_label});")
            self.visit(ctx.statement(1))
            self.emit(f"a.bind({end_label});")
        else:
            self.emit(f"a.bind({else_label});")
    
    def emit_condition_jump_false(self, ctx, false_label):
        left_ctx  = ctx.expr(0)
        right_ctx = ctx.expr(1)
        op        = ctx.compareOp().getText()

        left_type = self.visit(left_ctx)

        self.emit("a.push(x86::rax);")

        right_type = self.visit(right_ctx)

        self.emit("a.mov(x86::ebx, x86::eax);")
        self.emit("a.pop(x86::rax);")
        self.emit("a.cmp(x86::eax, x86::ebx);")

        jump_map = {
            "=":  "jne",
            "<>": "je",
            "<":  "jge",
            "<=": "jg",
            ">":  "jle",
            ">=": "jl",
        }

        jmp = jump_map[op]
        self.emit(f"a.{jmp}({false_label});")
        
    def visitWriteLnStatement(self, ctx):
        args = ctx.writeArgList()
        
        if args:
            for arg in args.writeArg():
                if arg.STRING():
                    value = arg.STRING().getText()[1:-1]
                    label = self.add_string_literal(value)

                    self.emit(f"a.mov(x86::rcx, imm((uint64_t){label}));")
                    self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_text));")
                    self.emit_call_rax()
                    
                else:
                    expr_type = self.visit(arg.expr())
                    
                    if expr_type == "integer":
                        self.emit("a.mov(x86::ecx, x86::eax);")
                        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_int));")
                        self.emit_call_rax()
                    
                    elif expr_type == "double":
                        # Windows x64: double-Argument liegt in xmm0
                        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_double));")
                        self.emit_call_rax()
        
        self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_newline));")
        self.emit_call_rax()
        
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
    
    def render_string_literals(self):
        out = []

        for name, text in self.string_literals:
            out.append(
                f'static const char {name}[] = "{self.cpp_escape(text)}";'
            )

        return "\n".join(out)
    
    def render_asm_double_symbols(self):
        out = []
        for name, value in self.double_literals:
            out.append(f'asm_out << "{name} equ " << std::to_string(double_to_bits({value})) << " ; {value}\\n";')
        return "\n    ".join(out)
    
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

extern \"C\" void jit_print_text(const char* s) {{ std::cout << s; }}
extern \"C\" void jit_print_int(int v)          {{ std::cout << v; }}
extern \"C\" void jit_print_double(double v)    {{ std::cout << v; }}
extern \"C\" void jit_print_newline()           {{ std::cout << std::endl; }}

{self.render_string_literals()}

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
    a.pop(x86::r12);
    a.ret();

    JitFunc fn = nullptr;
    Error err = rt.add(&fn, &code);
    if (err != Error::kOk) {{
        std::cerr << \"AsmJit error: \" << DebugUtils::error_as_string(err) << std::endl;
        return 1;
    }}
    
    std::ofstream asm_out(\"{self.asm_file}\");
    std::string asm_text = logger.data();
    
    auto replace_all = [](std::string& s, const std::string& from, const std::string& to) {{
        size_t pos = 0;
        while ((pos = s.find(from, pos)) != std::string::npos) {{
            s.replace(pos, from.length(), to);
            pos += to.length();
        }}
    }};

    replace_all(asm_text, std::to_string((uint64_t)&jit_print_text),    "_jit_print_text");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_int),     "_jit_print_int");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_double),  "_jit_print_double");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    
    replace_all(asm_text, std::to_string((uint64_t)&str_0), "_str_0");
    replace_all(asm_text, std::to_string((uint64_t)&str_1), "_str_1");
    replace_all(asm_text, std::to_string((uint64_t)&str_2), "_str_2");
    replace_all(asm_text, std::to_string((uint64_t)&str_3), "_str_3");
    replace_all(asm_text, std::to_string((uint64_t)&str_4), "_str_4");

    {self.render_asm_double_replacements()}

    std::istringstream iss(asm_text);
    std::string line;

    {self.render_asm_double_symbols()}
    
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
   
    std::array<int,    {int_count}> int_vars{{}};
    std::array<double, {double_count}> double_vars{{}};
    
    JitContext ctx{{}};
    ctx.int_vars = int_vars.data();
    ctx.double_vars = double_vars.data();
    
    fn(&ctx);

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
