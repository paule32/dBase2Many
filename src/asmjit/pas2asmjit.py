# ---------------------------------------------------------------------------
# File:   pascal2asmjit.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
import sys
import os

from datetime import datetime
from antlr4   import *

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

COMMENT_REPL = ('-' * 77)

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
        
        self.procedures          = {}
        self.current_proc_params = {}
        
        self.asm_file               = asm_file
        self.asm_label_replacements = []
        self.emit_local_string_data = True
    
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
    
    def collect_formal_params(self, ctx):
        params = []
        if not ctx.formalParamList():
            return params
        for p in ctx.formalParamList().formalParam():
            typ = p.typeName().getText().lower()
            for ident in p.identList().IDENT():
                params.append({
                    "name": ident.getText(),
                    "type": typ
                })
        return params
    
    def emit_call_rax(self):
        self.emit("a.sub(x86::rsp, 32); // Windows x64 shadow space")
        self.emit("a.call(x86::rax);")
        self.emit("a.add(x86::rsp, 32);")
    
    def emit_load_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rax, {slot * 4})); // {name}")

        elif typ == "double":
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::xmm0, x86::qword_ptr(x86::rax, {slot * 8})); // {name}")
    
    def emit_store_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]
        
        if typ == "integer":
            self.emit("a.mov(x86::ebx, x86::eax);")
            self.emit("a.mov(x86::rax, x86::qword_ptr(x86::r12, offsetof(JitContext, int_vars)));")
            self.emit(f"a.mov(x86::dword_ptr(x86::rax, {slot * 4}), x86::ebx); // {name}")

        elif typ == "double":
            self.emit("a.mov(x86::r11, x86::qword_ptr(x86::r12, offsetof(JitContext, double_vars)));")
            self.emit(f"a.movsd(x86::qword_ptr(x86::r11, {slot * 8}), x86::xmm0); // {name}")
    
    def emit_if_statement(self, ctx):
        else_name = self.new_named_label("else")
        end_name  = self.new_named_label("endif")

        self.emit_condition_jump_false(ctx.condition(), else_name)

        self.visit(ctx.statement(0))

        if ctx.ELSE():
            self.emit(f"a.jmp({end_name});")
            self.emit(f"a.bind({else_name});")
            self.visit(ctx.statement(1))
            self.emit(f"a.bind({end_name});")
        else:
            self.emit(f"a.bind({else_name});")
        
    def emit_int_to_double(self):
        self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
    
    def emit_condition_jump_false(self, ctx, false_label):
        left_ctx  = ctx.expr(0)
        right_ctx = ctx.expr(1)
        op        = ctx.compareOp().getText()

        left_type  = self.visit(left_ctx)

        # Linken Wert sichern
        if left_type == "double":
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")
        elif left_type == "integer":
            self.emit("a.push(x86::rax);")
        else:
            raise CompileError(ctx, "E0005", got=left_type, expected="integer/double")

        right_type = self.visit(right_ctx)

        # Double-Vergleich, sobald eine Seite Double ist
        if left_type == "double" or right_type == "double":
            if right_type == "integer":
                self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            elif right_type != "double":
                raise CompileError(ctx, "E0005", got=right_type, expected="integer/double")

            self.emit("a.movapd(x86::xmm1, x86::xmm0);")

            if left_type == "integer":
                self.emit("a.pop(x86::rax);")
                self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")
            else:
                self.emit("a.movsd(x86::xmm0, x86::qword_ptr(x86::rsp));")
                self.emit("a.add(x86::rsp, 8);")

            # Vergleich: left xmm0 gegen right xmm1
            self.emit("a.ucomisd(x86::xmm0, x86::xmm1);")

            jump_map = {
                "=":  "jne",
                "<>": "je",
                "<":  "jae",
                "<=": "ja",
                ">":  "jbe",
                ">=": "jb",
            }

            self.emit(f"a.{jump_map[op]}({false_label});")
            return

        # Integer-Vergleich
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

        self.emit(f"a.{jump_map[op]}({false_label});")
    
    def emit_expr_as_double(self, ctx):
        expr_type = self.visit(ctx)

        if expr_type == "integer":
            self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")

        elif expr_type != "double":
            raise CompileError(ctx, "E0005", got=expr_type, expected="double")

        return "double"

    def emit_while_statement(self, ctx):
        start_name = self.new_named_label("while")
        end_name   = self.new_named_label("endwhile")

        self.emit(f"a.bind({start_name});")
        self.emit_condition_jump_false(ctx.condition(), end_name)

        self.visit(ctx.statement())

        self.emit(f"a.jmp({start_name});")
        self.emit(f"a.bind({end_name});")
    
    def emit_repeat_statement(self, ctx):
        start_label = self.new_label_name("repeat")
        end_label   = self.new_label_name("endrepeat")

        self.emit_label(start_label)

        # Body
        for stmt in ctx.statement():
            self.visit(stmt)

        # Bedingung am Ende auswerten
        # Wichtig: Springe zurück, wenn Bedingung FALSE ist
        self.emit_condition_jump_false(ctx.condition(), start_label)
        self.emit_label(end_label)
    
    def require_var(self, ctx, name):
        key = name.lower()
        
        if key not in self.vars:
            raise CompileError(ctx, "E0003", name=key)  # Variable not declared
        
        return self.vars[key]
    
    def emit_repeat_statement(self, ctx):
        start_name = self.new_named_label("repeat")
        end_name   = self.new_named_label("endrepeat")

        self.emit(f"a.bind({start_name});")

        for stmt in ctx.statementList().statement():
            self.visit(stmt)

        self.emit_condition_jump_false(ctx.condition(), start_name)

        self.emit(f"a.bind({end_name});")
    
    def emit_for_statement(self, ctx):
        var_name = ctx.IDENT().getText()
        info = self.var_info(ctx, var_name)

        if info["type"] != "integer":
            raise CompileError(ctx, "E0005", got=info["type"], expected="integer")

        start_name = self.new_named_label("for")
        end_name   = self.new_named_label("endfor")

        # Startwert auswerten
        start_type = self.visit(ctx.expr(0))

        if start_type != "integer":
            raise CompileError(ctx, "E0005", got=start_type, expected="integer")

        self.emit_store_var(var_name, info)

        # Endwert auswerten und in r10d sichern
        end_type = self.visit(ctx.expr(1))

        if end_type != "integer":
            raise CompileError(ctx, "E0005", got=end_type, expected="integer")

        self.emit("a.mov(x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)), x86::eax); // for end value")

        self.emit(f"a.bind({start_name});")

        # Laufvariable laden
        self.emit_load_var(var_name, info)

        direction = ctx.getChild(4).getText().lower()

        if direction == "to":
            self.emit("a.cmp(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_int_tmp)));")
            self.emit(f"a.jg({end_name});")
        else:
            self.emit("a.cmp(x86::eax, x86::dword_ptr(x86::r12, offsetof(JitContext, print_double_tmp)));")
            self.emit(f"a.jl({end_name});")

        self.visit(ctx.statement())

        # Laufvariable erneut laden, ändern, speichern
        self.emit_load_var(var_name, info)

        if direction == "to":
            self.emit("a.add(x86::eax, 1);")
        else:
            self.emit("a.sub(x86::eax, 1);")

        self.emit_store_var(var_name, info)

        self.emit(f"a.jmp({start_name});")
        self.emit(f"a.bind({end_name});")
    
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
        
        for proc in ctx.procedureDeclaration():
            self.visit(proc)
    
        self.visit(ctx.block())
        return self.render_cpp()
    
    def visitBlock(self, ctx):
        return self.visit(ctx.statementList())
    
    def visitStatementList(self, ctx):
        for st in ctx.statement():
            self.visit(st)
    
    def visitStatement(self, ctx):
        if ctx.procedureCallStatement():
            return self.visit(ctx.procedureCallStatement())
    
        if ctx.assignment():
            return self.visit(ctx.assignment())
        
        if ctx.writeLnStatement():
            return self.visit(ctx.writeLnStatement())
        
        if ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        
        if ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        
        if ctx.repeatStatement():
            return self.visit(ctx.repeatStatement())
        
        if ctx.forStatement():
            return self.visit(ctx.forStatement())
        
        if ctx.compoundStatement():
            return self.visit(ctx.compoundStatement())
        
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

            if result_type == "integer":
                self.emit("a.push(x86::rax);")

                right_type = self.visit(ctx.term(i))

                if right_type == "integer":
                    self.emit("a.mov(x86::ebx, x86::eax);")
                    self.emit("a.pop(x86::rax);")

                    if op == "+":
                        self.emit("a.add(x86::eax, x86::ebx);")
                    elif op == "-":
                        self.emit("a.sub(x86::eax, x86::ebx);")

                    result_type = "integer"
                    continue

                self.emit("a.pop(x86::rax);")
                self.emit("a.cvtsi2sd(x86::xmm1, x86::eax);")
                result_type = "double"

            # Double-Fallback
            self.emit("a.sub(x86::rsp, 8);")
            self.emit("a.movsd(x86::qword_ptr(x86::rsp), x86::xmm0);")

            right_type = self.visit(ctx.term(i))

            if right_type == "integer":
                self.emit("a.cvtsi2sd(x86::xmm0, x86::eax);")

            self.emit("a.movsd(x86::xmm1, x86::qword_ptr(x86::rsp));")
            self.emit("a.add(x86::rsp, 8);")

            if op == "+":
                self.emit("a.addsd(x86::xmm0, x86::xmm1);")
            elif op == "-":
                self.emit("a.movapd(x86::xmm2, x86::xmm0);")
                self.emit("a.movapd(x86::xmm0, x86::xmm1);")
                self.emit("a.subsd(x86::xmm0, x86::xmm2);")

            result_type = "double"

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
    
    def visitProcedureDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()

        label     = self.new_named_label("proc_" + name)
        end_label = self.new_named_label("endproc_" + name)

        params = self.collect_formal_params(ctx)

        self.procedures[key] = {
            "name": name,
            "label": label,
            "params": params
        }

        param_regs = ["rcx", "rdx", "r8", "r9"]

        if len(params) > len(param_regs):
            raise CompileError(ctx,
                "E0005",
                got="too many params",
                expected="max 4 params")

        self.emit(f"a.jmp({end_label});")
        self.emit(f"a.bind({label});")
        
        self.emit("a.push(x86::rbp);")
        self.emit("a.mov(x86::rbp, x86::rsp);")

        old_params = self.current_proc_params
        self.current_proc_params = {}

        for index, p in enumerate(params):
            reg = param_regs[index]
            pname = p["name"]
            self.emit(f"a.push(x86::{reg}); // save param {pname}")
            
            self.current_proc_params[p["name"].lower()] = {
                "type": p["type"],
                "reg": param_regs[index],
                "stack_offset": -8 * (index + 1)
            }
            
        self.visit(ctx.block())
        
        self.current_proc_params = old_params
        
        self.emit("a.mov(x86::rsp, x86::rbp);")
        self.emit("a.pop(x86::rbp);")
        self.emit("a.ret();")
        
        self.emit(f"a.bind({end_label});")
        return None
    
    def visitProcedureCallStatement(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()
        param_regs = ["rcx", "rdx", "r8", "r9"]
        
        if key not in self.procedures:
            raise CompileError(ctx, "E0001", name=name)

        proc = self.procedures[key]
        params = proc["params"]

        actuals = []
        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != len(params):
            raise CompileError(ctx,
                "E0005",
                got=str(len(actuals)),
                expected=str(len(params)))

        for index, arg in enumerate(actuals):
            formal = params[index]

            if formal["type"] == "integer":
                expr_type = self.visit(arg.expr())

                if expr_type != "integer":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

                int_regs = ["ecx", "edx", "r8d", "r9d"]
                reg = int_regs[index]
                self.emit(f"a.mov(x86::{reg}, x86::eax);")

            elif formal["type"] == "string":
                if not arg.STRING():
                    raise CompileError(ctx, "E0005", got="expr", expected="string")

                value = arg.STRING().getText()[1:-1]
                label = self.add_string_literal(value)

                reg = param_regs[index]
                self.emit(f"a.mov(x86::{reg}, imm((uint64_t){label}));")

            else:
                raise CompileError(ctx, "E0005", got=formal["type"], expected="string/integer")

        self.emit("a.sub(x86::rsp, 32); // shadow space for procedure call")
        self.emit(f"a.call({proc['label']});")
        self.emit("a.add(x86::rsp, 32);")
        return None
    
    def visitIfStatement(self, ctx):
        self.emit_if_statement(ctx)
        return None
    
    def visitCompoundStatement(self, ctx):
        return self.visit(ctx.statementList())
    
    def visitWhileStatement(self, ctx):
        self.emit_while_statement(ctx)
        return None
    
    def visitRepeatStatement(self, ctx):
        return self.emit_repeat_statement(ctx)
    
    def visitForStatement(self, ctx):
        return self.emit_for_statement(ctx)
    
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
                    if arg.expr() and arg.expr().getText().lower() in self.current_proc_params:
                        pname = arg.expr().getText().lower()
                        pinfo = self.current_proc_params[pname]
                        
                        if pinfo["type"] == "integer":
                            offset = pinfo["stack_offset"]
                            offset = pinfo["stack_offset"]
                            self.emit(f"a.mov(x86::eax, x86::dword_ptr(x86::rbp, {offset})); // load integer parameter")
                            self.emit("a.mov(x86::ecx, x86::eax);")
                            self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_int));")
                            self.emit_call_rax()
                            continue
                            
                        if pinfo["type"] == "string":
                            offset = pinfo["stack_offset"]
                            self.emit(f"a.mov(x86::rcx, x86::qword_ptr(x86::rbp, {offset})); // load string parameter")
                            self.emit("a.mov(x86::rax, imm((uint64_t)&jit_print_text));")
                            self.emit_call_rax()
                            continue
                    
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
    
    def new_named_label(self, prefix):
        name = self.new_label_name(prefix)
        asmjit_l = f"L{len(self.asm_label_replacements)}"

        self.emit(f"Label {name} = a.new_label();")
        self.asm_label_replacements.append((asmjit_l, name))

        return name
    
    def render_asm_double_replacements(self):
        out = []
        for name, value in self.double_literals:
            out.append(
                f'replace_all(asm_text, std::to_string(double_to_bits({value})), "{name}");'
            )
        return "\n    ".join(out)
        
    def render_asm_string_replacements(self):
        out = []
        for name, text in self.string_literals:
            out.append(
                f'replace_all(asm_text, std::to_string((uint64_t)&{name}), "_{name}");'
            )
        return "\n    ".join(out)
    
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
    
    def render_asm_nasm_header(self):
        return f"""
    asm_out << "; {COMMENT_REPL}\\n";
    asm_out << "; GENERATED WITH PYTHON 3.14 ON: {datetime.now().strftime("%Y-%m-%d")}\\n";
    asm_out << "; Copyright (c) 2026 by Jens Kallup - paule32\\n";
    asm_out << "; all rights reserved.\\n";
    asm_out << "; {COMMENT_REPL}\\n\\n";
    """
    
    def render_asm_nasm_structs(self):
        return r"""
    asm_out << "struc JitContext\n";
    asm_out << "    .int_vars:         resq 1\n";
    asm_out << "    .double_vars:      resq 1\n";
    asm_out << "    .print_int_tmp:    resd 1\n";
    asm_out << "    .print_double_tmp: resq 1\n";
    asm_out << "endstruc\n\n";
    """

    def render_asm_context_replacements(self):
        return r"""
    replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]");
    replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]");
    replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.print_int_tmp]");
    replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.print_double_tmp]");
    """
    
    def render_asm_extern_symbols(self):
        out = []

        if not self.emit_local_string_data:
            for name, text in self.string_literals:
                out.append(f'asm_out << "extern _{name}\\n";')

            if self.string_literals:
                out.append('asm_out << "\\n";')

        out.append('asm_out << "extern _jit_print_text\\n";')
        out.append('asm_out << "extern _jit_print_int\\n";')
        out.append('asm_out << "extern _jit_print_double\\n";')
        out.append('asm_out << "extern _jit_print_newline\\n";')

        return "\n    ".join(out)
    
    def render_asm_string_data(self):
        if not self.emit_local_string_data:
            return ""

        out = []
        out.append('asm_out << "\\nsection .data\\n";')

        for name, text in self.string_literals:
            escaped = self.cpp_escape(text)
            out.append(f'asm_out << "_{name} db \\"{escaped}\\", 0\\n";')

        return "\n    ".join(out)
    
    def render_asm_label_replacements(self):
        out = []

        for old_name, new_name in self.asm_label_replacements:
            out.append(f'replace_all(asm_text, "{old_name}:", "{new_name}:");')
            out.append(f'replace_all(asm_text, "{old_name}", "{new_name}");')

        return "\n    ".join(out)
    
    def render_cpp(self):
        body         = "\n".join(self.lines)
        
        var_count    = max(257, self.next_slot)
        int_count    = max(  1, self.next_int_slot)
        double_count = max(  1, self.next_double_slot)
        
        # todo !!!
        self.func_name = "main"
        self.date_str  = datetime.now().strftime("%Y-%m-%d")
        
        return f'''// automaically created per Python 3.14 script on: {self.date_str}
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
        if (from.empty())
            return;

        size_t pos = 0;

        while ((pos = s.find(from, pos)) != std::string::npos) {{
            s.replace(pos, from.length(), to);
            pos += std::max<size_t>(to.length(), 1);
        }}
    }};

    replace_all(asm_text, std::to_string((uint64_t)&jit_print_text),    "_jit_print_text");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_int),     "_jit_print_int");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_double),  "_jit_print_double");
    replace_all(asm_text, std::to_string((uint64_t)&jit_print_newline), "_jit_print_newline");
    
    {self.render_asm_string_replacements()}
    
    {self.render_asm_label_replacements ()}

    replace_all(asm_text, "byte ptr ",    "byte ");
    replace_all(asm_text, "word ptr ",    "word ");
    replace_all(asm_text, "dword ptr ",   "dword ");
    replace_all(asm_text, "qword ptr ",   "qword ");
    replace_all(asm_text, "xmmword ptr ", "xmmword ");
    
    {self.render_asm_context_replacements()}
    
    {self.render_asm_nasm_header()}
    {self.render_asm_nasm_structs()}
    
    {self.render_asm_double_replacements()}
    asm_out << "\\n";

    std::istringstream iss(asm_text);
    std::string line;

    {self.render_asm_double_symbols()}
    {self.render_asm_extern_symbols()}
    
    asm_out << "\\n";
    asm_out << "section .text\\n";
    asm_out << \"global \" << \"_{self.func_name}\" << \"\\n\";
    asm_out << \"_{self.func_name}\" << \":\\n\";
    
    while (std::getline(iss, line)) {{
        std::string s = line;

        // führende Leerzeichen entfernen
        size_t start = s.find_first_not_of(\" \\t\");
        if (start == std::string::npos) {{
            asm_out << \"\\n\";
            continue;
        }}

        s = s.substr(start);
        
        // Labels linksbündig ausgeben: L0:
        if (!s.empty() && s.back() == \':\') {{
            asm_out << s << \"\\n\";
            continue;
        }}

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
            
            // short jmp <label>
            if (mnemonic == "short") {{
                size_t rest_start = rest.find_first_not_of(" \\t");

                if (rest_start != std::string::npos)
                    s = rest.substr(rest_start);
                else
                    s.clear();

                pos = s.find_first_of(" \\t");

                if (pos != std::string::npos) {{
                    mnemonic = s.substr(0, pos);
                    rest = s.substr(pos);
                }} else {{
                    mnemonic = s;
                    rest.clear();
                }}
            }}
            asm_out << \"\\t\" << mnemonic << \"\\t\" << rest << \"\\n\";
        }} else {{
            asm_out << \"\\t\" << s << \"\\n\";
        }}
    }}
    
    {self.render_asm_string_data()}
    
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
