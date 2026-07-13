# ---------------------------------------------------------------------------
# File:   generator.py - LISP compiler
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import os
import sys
import re
import json

from pathlib     import Path
from dataclasses import dataclass, field

from antlr4      import ParseTreeVisitor, TerminalNode
from antlr4      import *

from parsers.lisp.LispLexer          import LispLexer
from parsers.lisp.LispParser         import LispParser
from parsers.lisp.LispParserVisitor  import LispParserVisitor

from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.constants import *

from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.writer.pe64coff        import *
from compiler.frontend.generatorbase import *

# ---------------------------------------------------------------------------
# generator classes
# ---------------------------------------------------------------------------
class GeneratorClass(CodeGeneratorBase, LispParserVisitor):
    def __init__(self, backend, writer=None):
        CodeGeneratorBase.__init__(self, backend)
        LispParserVisitor.__init__(self)
        
        self.backend  = backend
        self.writer   = writer
        self.coff     = None

        self.entry_function_name  = None

        self.function_definitions = []
        self.top_level_forms      = []
        
        self.handlers = {
            "+"       : self.emit_lisp_add,
            "-"       : self.emit_lisp_sub,
            "*"       : self.emit_lisp_mul,
            "/"       : self.emit_lisp_div,
            
            "="       : self.emit_lisp_eq,
            "=="      : self.emit_lisp_eq,

            "/="      : self.emit_lisp_ne,
            "!="      : self.emit_lisp_ne,
            "<>"      : self.emit_lisp_ne,

            "<"       : self.emit_lisp_lt,
            "<="      : self.emit_lisp_le,
            ">"       : self.emit_lisp_gt,
            ">="      : self.emit_lisp_ge,
    
            "setq"    : self.emit_lisp_setq,
            "if"      : self.emit_lisp_if,
            "while"   : self.emit_lisp_while,
            
            "break"   : self.emit_lisp_break,
            "continue": self.emit_lisp_continue,
            
            "print"   : self.emit_lisp_print,
            "println" : self.emit_lisp_println,
            
            "defun"   : self.emit_lisp_defun,
        }
        
        if writer is None:
            raise RuntimeError("generator writer invalid")

        # EXE-Writer bekommen: echten COFF-Writer herausziehen
        if isinstance(writer, NT32Writer):
            self.coff = writer.coff
            self.writer = writer.coff

        elif isinstance(writer, PE64Writer):
            self.coff = writer.coff
            self.writer = writer.coff

        elif isinstance(writer, (PE32Writer, PE64CoffWriter)):
            self.coff = writer

        else:
            raise RuntimeError(f"unsupported generator writer: {type(writer)}")

    def register_lisp_start(self, ctx, args):
        if len(args) != 1:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="one function name"
            )

        function_name = self.get_symbol_expression(
            args[0]
        )

        if self.entry_function_name is not None:
            raise CompileError(
                ctx,
                "E0002",
                identifier="start"
            )

        self.entry_function_name = function_name

    def infer_lisp_static_type(self, ctx):
        atom_ctx = ctx.atom()

        if atom_ctx is not None:
            if atom_ctx.NUMBER():
                return "integer"

            if atom_ctx.STRING():
                return "string"

            if atom_ctx.SYMBOL():
                name = (
                    atom_ctx
                    .SYMBOL()
                    .getText()
                    .lower()
                )

                if name in (
                    "true",
                    "false",
                    "t"
                ):
                    return "boolean"

                if name == "nil":
                    # NIL wird vorerst als 32-Bit-Nullwert abgelegt.
                    return "integer"

                info = self.find_variable(name)

                if info is not None:
                    return info["type"]

                # In der ersten LISP-Version verwenden wir Integer
                # als Standardtyp für noch unbekannte Symbole.
                return "integer"

        list_ctx = ctx.list_()

        if list_ctx is not None:
            expressions = list_ctx.expression()

            if not expressions:
                return "integer"

            operator_ctx = expressions[0]

            if (
                operator_ctx.atom() is not None
                and operator_ctx.atom().SYMBOL() is not None
            ):
                operator = (
                    operator_ctx
                    .atom()
                    .SYMBOL()
                    .getText()
                    .lower()
                )

                if operator in (
                    "+",
                    "-",
                    "*",
                    "/"
                ):
                    return "integer"

                if operator in (
                    "=",
                    "/=",
                    "!=",
                    "<",
                    "<=",
                    ">",
                    ">="
                ):
                    return "boolean"

                if operator == "if":
                    # Typ des THEN-Ausdrucks verwenden.
                    if len(expressions) >= 3:
                        return self.infer_lisp_static_type(
                            expressions[2]
                        )

                function_info = self.functions.get(
                    operator
                )

                if function_info is not None:
                    return (
                        function_info.get("return_type")
                        or "integer"
                    )

        return "integer"

    def predeclare_lisp_setq(self, ctx, args):
        if len(args) < 2 or len(args) % 2 != 0:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="symbol/value pairs"
            )

        for index in range(0, len(args), 2):
            name_ctx  = args[index]
            value_ctx = args[index + 1]

            name = self.get_symbol_expression(
                name_ctx
            )

            if name in self.variables:
                continue

            var_type = self.infer_lisp_static_type(
                value_ctx
            )

            self.declare_global_variable(
                name,
                var_type
            )

    def visitProgram(self, ctx):
        all_expressions = list(
            ctx.expression()
        )

        self.entry_function_name = None
        self.function_definitions.clear()
        self.top_level_forms.clear()

        # ---------------------------------------------------------
        # Pass 1:
        # Funktionen und Startdirektive registrieren.
        # Top-Level-Ausdrücke sammeln.
        # ---------------------------------------------------------
        for expression_ctx in all_expressions:
            (
                operator,
                list_ctx,
                args
            ) = self.get_expression_list_info(
                expression_ctx
            )

            if operator == "defun":
                self.register_lisp_defun(
                    list_ctx,
                    args
                )
                continue

            if operator == "start":
                self.register_lisp_start(
                    list_ctx,
                    args
                )
                continue

            self.top_level_forms.append(
                expression_ctx
            )

        # ---------------------------------------------------------
        # Pass 2:
        # Globale Variablen vorab deklarieren.
        #
        # Noch keinen Initialisierungscode erzeugen.
        # ---------------------------------------------------------
        for expression_ctx in self.top_level_forms:
            (
                operator,
                list_ctx,
                args
            ) = self.get_expression_list_info(
                expression_ctx
            )

            if operator == "setq":
                self.predeclare_lisp_setq(
                    list_ctx,
                    args
                )

        # ---------------------------------------------------------
        # Explizites Startsymbol prüfen.
        # ---------------------------------------------------------
        if (
            self.entry_function_name is not None
            and self.entry_function_name
            not in self.functions
        ):
            raise RuntimeError(
                "LISP start function not found: "
                + self.entry_function_name
            )

        # ---------------------------------------------------------
        # Pass 3:
        # Funktionen erzeugen.
        #
        # Die globalen Variablen sind jetzt bereits bekannt.
        # ---------------------------------------------------------
        for function_info in self.function_definitions:
            self.emit_registered_lisp_function(
                function_info
            )

        # ---------------------------------------------------------
        # Pass 4:
        # _main und Top-Level-Initialisierungen erzeugen.
        # ---------------------------------------------------------
        return self.emit_lisp_main()

    def visitList(self, ctx):
        expressions = ctx.expression()

        if not expressions:
            return "nil"

        operator = expressions[0].getText().lower()
        args = expressions[1:]

        handler = self.handlers.get(operator)

        if handler is not None:
            return handler(ctx, args)

        return self.emit_lisp_function_call(ctx, operator, args)

    def emit_lisp_compare(self, ctx, args, operator):
        if len(args) != 2:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="2"
            )

        left_type = self.visit(args[0])

        if left_type not in (
            "integer",
            "boolean",
            "char"
        ):
            raise CompileError(
                args[0],
                "E0005",
                got=left_type,
                expected="integer, boolean or char"
            )

        # Linken Operanden sichern.
        self.emit_push("eax")

        right_type = self.visit(args[1])

        if right_type != left_type:
            raise CompileError(
                args[1],
                "E0005",
                got=right_type,
                expected=left_type
            )

        # eax = rechter Operand
        # ecx = linker Operand
        self.emit_pop("ecx")

        # Vergleich: links operator rechts
        self.emit_cmp("ecx", "eax")

        if   operator == "eq": self.emit_sete ("al")
        elif operator == "ne": self.emit_setne("al")
        elif operator == "lt": self.emit_setl ("al")
        elif operator == "le": self.emit_setle("al")
        elif operator == "gt": self.emit_setg ("al")
        elif operator == "ge": self.emit_setge("al")

        else:
            raise RuntimeError(
                f"Unsupported LISP comparison: {operator}"
            )

        # Boolean auf 0 oder 1 erweitern.
        self.emit_movzx("eax", "al")

        return "boolean"

    def emit_lisp_eq(self, ctx, args): return self.emit_lisp_compare(ctx, args, "eq" )
    def emit_lisp_ne(self, ctx, args): return self.emit_lisp_compare(ctx, args, "ne" )
    def emit_lisp_lt(self, ctx, args): return self.emit_lisp_compare(ctx, args, "lt" )
    def emit_lisp_le(self, ctx, args): return self.emit_lisp_compare(ctx, args, "le" )
    def emit_lisp_gt(self, ctx, args): return self.emit_lisp_compare(ctx, args, "gt" )
    def emit_lisp_ge(self, ctx, args): return self.emit_lisp_compare(ctx, args, "ge" )

    def emit_lisp_add(self, ctx, args):
        if len(args) < 2:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="at least 2"
            )

        result_type = self.visit(args[0])

        if result_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="integer"
            )

        for arg in args[1:]:
            self.emit_push("eax")

            arg_type = self.visit(arg)

            if arg_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=arg_type,
                    expected="integer"
                )

            self.emit_pop("ecx")
            self.emit_add("eax", "ecx")

        return "integer"

    def emit_lisp_sub(self, ctx, args):
        if not args:
            raise CompileError(
                ctx,
                "E0005",
                got="0",
                expected="at least 1"
            )

        result_type = self.visit(args[0])

        if result_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="integer"
            )

        # (- x) bedeutet -x
        if len(args) == 1:
            self.emit_neg("eax")
            return "integer"

        for arg in args[1:]:
            # Linken Zwischenwert sichern
            self.emit_push("eax")

            arg_type = self.visit(arg)

            if arg_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=arg_type,
                    expected="integer"
                )

            # eax = rechter Operand
            # ecx = linker Operand
            self.emit_pop("ecx")

            # ecx = ecx - eax
            self.emit_sub("ecx", "eax")

            # Ergebnis wieder nach eax
            self.emit_mov("eax", "ecx")

        return "integer"

    def emit_lisp_mul(self, ctx, args):
        if not args:
            # In Common Lisp ist (*) gleich 1.
            self.emit_mov("eax", 1)
            return "integer"

        result_type = self.visit(args[0])

        if result_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="integer"
            )

        for arg in args[1:]:
            self.emit_push("eax")

            arg_type = self.visit(arg)

            if arg_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=arg_type,
                    expected="integer"
                )

            self.emit_pop("ecx")

            # eax = eax * ecx
            self.emit_imul("eax", "ecx")

        return "integer"

    def emit_lisp_div(self, ctx, args):
        if len(args) < 2:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="at least 2"
            )

        result_type = self.visit(args[0])

        if result_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="integer"
            )

        for arg in args[1:]:
            # Bisherigen linken Wert sichern
            self.emit_push("eax")

            divisor_type = self.visit(arg)

            if divisor_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=divisor_type,
                    expected="integer"
                )

            # ecx = Divisor
            self.emit_mov("ecx", "eax")

            # Division durch Null prüfen
            div_ok = self.new_label("div_ok")

            self.emit_cmp("ecx", 0)
            self.emit_jne(div_ok)
            self.emit_call("_jit_error_divide_by_zero")

            self.emit_bind_label(div_ok)

            # eax = Dividend
            self.emit_pop("eax")

            # edx:eax vorzeichenbehaftet erweitern
            self.emit_cdq()

            # eax = eax / ecx
            self.emit_idiv("ecx")

        return "integer"

    def emit_lisp_setq(self, ctx, args):
        if len(args) < 2 or len(args) % 2 != 0:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="symbol/value pairs"
            )

        result_type = "nil"

        for index in range(0, len(args), 2):
            name_ctx = args[index]
            value_ctx = args[index + 1]

            name = self.get_symbol_expression(name_ctx)

            value_type = self.visit(value_ctx)

            self.emit_store_lisp_variable(
                ctx,
                name,
                value_type
            )

            result_type = value_type

        # SETQ liefert den letzten zugewiesenen Wert.
        # eax enthält diesen bereits.
        return result_type

    def emit_lisp_while(self, ctx, args):
        if len(args) < 1:
            raise CompileError(
                ctx,
                "E0005",
                got="0",
                expected="condition and optional body"
            )

        condition_ctx = args[0]
        body = args[1:]

        condition_label = self.new_label("while_condition")
        end_label = self.new_label("while_end")

        self.break_label_stack.append(end_label)
        self.continue_label_stack.append(condition_label)

        try:
            self.emit_bind_label(condition_label)

            condition_type = self.visit(condition_ctx)

            if condition_type not in (
                "integer",
                "boolean",
                "nil"
            ):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=condition_type,
                    expected="boolean or integer"
                )

            self.emit_cmp("eax", 0)
            self.emit_je(end_label)

            for expression in body:
                self.visit(expression)

            self.emit_jmp(condition_label)

            self.emit_bind_label(end_label)

        finally:
            self.continue_label_stack.pop()
            self.break_label_stack.pop()

        # WHILE liefert NIL.
        self.emit_mov("eax", 0)
        return "nil"

    def emit_lisp_break(self, ctx, args):
        if args:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="0"
            )

        if not self.break_label_stack:
            raise CompileError(
                ctx,
                "E0015",
                got="break outside loop",
                expected="loop"
            )

        self.emit_jmp(self.break_label_stack[-1])
        return "nil"

    def emit_lisp_continue(self, ctx, args):
        if args:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="0"
            )

        if not self.continue_label_stack:
            raise CompileError(
                ctx,
                "E0015",
                got="continue outside loop",
                expected="loop"
            )

        self.emit_jmp(self.continue_label_stack[-1])
        return "nil"

    def emit_lisp_print(self, ctx, args, newline=False):
        if not args:
            if newline:
                self.emit_call("_jit_print_newline")

            self.emit_mov("eax", 0)
            return "nil"

        last_type = "nil"

        for arg in args:
            arg_type = self.visit(arg)
            last_type = arg_type

            if arg_type == "integer":
                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    self.emit_push("eax")
                    self.emit_call("_jit_print_int")
                    self.backend.emit_cleanup_stack(4)
                else:
                    self.emit_mov("rcx", "rax")
                    self.emit_call("_jit_print_int")

            elif arg_type == "boolean":
                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    self.emit_push("eax")
                    self.emit_call("_jit_print_bool")
                    self.backend.emit_cleanup_stack(4)
                else:
                    self.emit_mov("rcx", "rax")
                    self.emit_call("_jit_print_bool")

            elif arg_type == "char":
                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    self.emit_push("eax")
                    self.emit_call("_jit_print_char")
                    self.backend.emit_cleanup_stack(4)
                else:
                    self.emit_mov("rcx", "rax")
                    self.emit_call("_jit_print_char")

            elif arg_type == "string":
                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    self.emit_push("eax")
                    self.emit_call("_jit_print_text")
                    self.backend.emit_cleanup_stack(4)
                else:
                    self.emit_mov("rcx", "rax")
                    self.emit_call("_jit_print_text")

            elif arg_type == "nil":
                label = self.add_string_literal("NIL")

                if CDATA.args_target in (
                    "nt35",
                    "winnt",
                    "win32"
                ):
                    self.backend.writer.emit_push_data_label32(label)
                    self.emit_call("_jit_print_text")
                    self.backend.emit_cleanup_stack(4)
                else:
                    self.emit_mov_imm("rcx", label)
                    self.emit_call("_jit_print_text")

            else:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=arg_type,
                    expected="printable value"
                )

        if newline:
            self.emit_call("_jit_print_newline")

        # PRINT liefert in echtem LISP meist den ausgegebenen Wert.
        # Das Runtime-PRINT kann eax verändert haben, daher hier
        # zunächst NIL zurückgeben.
        self.emit_mov("eax", 0)
        return "nil"

    def emit_lisp_print_form(self, ctx, args):
        return self.emit_lisp_print(
            ctx,
            args,
            newline=False
        )

    def emit_lisp_defun(self, ctx, args):
        if len(args) < 3:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="name, parameter list and body"
            )

        name_ctx = args[0]
        params_ctx = args[1]
        body = args[2:]

        function_name = self.get_symbol_expression(name_ctx)

        if params_ctx.list_() is None:
            raise CompileError(
                params_ctx,
                "E0005",
                got=params_ctx.getText(),
                expected="parameter list"
            )

        parameter_expressions = params_ctx.list_().expression()
        parameter_names = []

        for parameter_ctx in parameter_expressions:
            parameter_name = self.get_symbol_expression(
                parameter_ctx
            )

            if parameter_name in parameter_names:
                raise CompileError(
                    parameter_ctx,
                    "E0002",
                    name=parameter_name
                )

            parameter_names.append(parameter_name)

        if function_name in self.functions:
            raise CompileError(
                ctx,
                "E0002",
                name=function_name
            )

        function_label = f"lisp_func_{function_name}"
        end_label = self.new_label(
            f"defun_{function_name}_skip"
        )

        function_info = {
            "name": function_name,
            "label": function_label,
            "parameters": parameter_names,
            "parameter_types": [
                "integer"
                for _ in parameter_names
            ],
            "return_type": None,
        }

        self.functions[function_name] = function_info

        # Funktionsdefinition darf beim normalen Programmablauf
        # nicht direkt ausgeführt werden.
        self.emit_jmp(end_label)

        self.emit_bind_label(function_label)

        # Prolog
        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        old_function = self.current_func
        self.current_func = function_info

        local_scope = {}

        for index, parameter_name in enumerate(parameter_names):
            local_scope[parameter_name] = {
                "name": parameter_name,
                "type": "integer",
                "kind": "parameter",
                "offset": 8 + index * 4,
            }

        self.local_scopes.append(local_scope)

        try:
            result_type = "nil"

            for expression in body:
                result_type = self.visit(expression)

            function_info["return_type"] = result_type

            # Der letzte Ausdruck hat sein Resultat bereits in eax.

        finally:
            self.local_scopes.pop()
            self.current_func = old_function

        # Epilog
        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()

        self.emit_bind_label(end_label)

        # DEFUN liefert normalerweise das Funktionssymbol.
        # In dieser ersten Version verwenden wir NIL.
        self.emit_mov("eax", 0)
        return "nil"

    def emit_lisp_function_call(self, ctx, name, args):
        name = name.lower()

        function_info = self.functions.get(name)

        if function_info is None:
            raise CompileError(
                ctx,
                "E0001",
                name=name
            )

        parameters = function_info["parameters"]

        if len(args) != len(parameters):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected=str(len(parameters))
            )

        for index in range(len(args) - 1, -1, -1):
            arg_type = self.visit(args[index])

            expected_type = (
                function_info[
                    "parameter_types"
                ][index]
            )

            if arg_type != expected_type:
                raise CompileError(
                    args[index],
                    "E0005",
                    got=arg_type,
                    expected=expected_type
                )

            self.emit_push("eax")

        self.emit_call_lbl(function_info["label"])
        stack_size = len(args) * 4

        if stack_size:
            self.backend.emit_cleanup_stack(
                stack_size
            )

        return (
            function_info["return_type"]
            or "integer"
        )

    def emit_lisp_println(self, ctx, args):
        return self.emit_lisp_print(
            ctx,
            args,
            newline=True
        )

    def emit_lisp_if(self, ctx, args):
        if len(args) not in (2, 3):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="2 or 3"
            )

        condition_ctx = args[0]
        then_ctx = args[1]
        else_ctx = args[2] if len(args) == 3 else None

        else_label = self.new_label("if_else")
        end_label = self.new_label("if_end")

        condition_type = self.visit(condition_ctx)

        if condition_type not in (
            "integer",
            "boolean",
            "nil"
        ):
            raise CompileError(
                ctx,
                "E0005",
                got=condition_type,
                expected="boolean or integer"
            )

        # NIL beziehungsweise 0 ist falsch.
        self.emit_cmp("eax", 0)
        self.emit_je(else_label)

        then_type = self.visit(then_ctx)

        self.emit_jmp(end_label)

        self.emit_bind_label(else_label)

        if else_ctx is not None:
            else_type = self.visit(else_ctx)
        else:
            # Fehlender ELSE-Zweig liefert NIL.
            self.emit_mov("eax", 0)
            else_type = "nil"

        self.emit_bind_label(end_label)

        if then_type == else_type:
            return then_type

        # NIL darf mit einem anderen Rückgabetyp kombiniert werden.
        if then_type == "nil":
            return else_type

        if else_type == "nil":
            return then_type

        raise CompileError(
            ctx,
            "E0005",
            got=else_type,
            expected=then_type
        )

    def new_label(self, prefix):
        self.label_counter += 1
        return f"__lisp_{prefix}_{self.label_counter}"

    def symbol_name(self, ctx):
        return ctx.getText().lower()

    def get_symbol_expression(self, ctx):
        if ctx.atom() is None or ctx.atom().SYMBOL() is None:
            raise CompileError(
                ctx,
                "E0005",
                got=ctx.getText(),
                expected="symbol"
            )
        return ctx.atom().SYMBOL().getText().lower()

    def current_scope(self):
        if self.local_scopes:
            return self.local_scopes[-1]

        return None

    def find_variable(self, name):
        name = name.lower()
        for scope in reversed(self.local_scopes):
            if name in scope:
                return scope[name]
        return self.variables.get(name)

    def declare_global_variable(self, name, var_type="integer"):
        name = name.lower()

        if name in self.variables:
            return self.variables[name]

        label = f"lisp_var_{name}"

        info = {
            "name": name,
            "type": var_type,
            "kind": "global",
            "label": label,
        }

        self.variables[name] = info
        
        if self.writer.find_symbol_index(label) is None:
            if var_type in ("integer", "boolean", "char"):
                self.writer.add_data_i32(label, 0)
            else:
                raise RuntimeError(
                f"Unsupported global LISP variable type: "
                f"{var_type}"
                )

        return info

    def declare_local_variable(self, name, var_type="integer"):
        scope = self.current_scope()

        if scope is None:
            return self.declare_global_variable(name, var_type)

        name = name.lower()

        if name in scope:
            raise RuntimeError(f"Duplicate local variable: {name}")

        # Beispiel: lokale Variablen relativ zu EBP.
        # Eine echte Implementation sollte deinen vorhandenen
        # lokalen Slot-Allocator verwenden.
        offset = -4 * (len(scope) + 1)

        info = {
            "name": name,
            "type": var_type,
            "kind": "local",
            "offset": offset,
        }

        scope[name] = info
        return info

    def emit_load_lisp_variable(self, ctx, name):
        name = name.lower()
        info = self.find_variable(name)

        if info is None:
            raise CompileError(
                ctx,
                "E0001",
                name=name
            )

        kind = info["kind"]

        if kind == "global":
            self.writer.emit_mov_reg_from_data_label32(
                "eax",
                info["label"]
            )

        elif kind in ("local", "parameter"):
            self.writer.emit_mov_reg_mem32(
                "eax",
                "ebp",
                info["offset"]
            )

        else:
            raise RuntimeError(
                f"Unsupported LISP variable kind: {kind}"
            )

        return info["type"]

    def emit_store_lisp_variable(self, ctx, name, value_type):
        name = name.lower()
        info = self.find_variable(name)

        if info is None:
            info = self.declare_global_variable(
                name,
                value_type
            )

        expected_type = info["type"]

        if expected_type != value_type:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=expected_type
            )

        kind = info["kind"]

        if kind == "global":
            self.writer.emit_mov_data_label_r32(
                info["label"],
                "eax"
            )

        elif kind in ("local", "parameter"):
            self.writer.emit_mov_mem_reg32(
                "ebp",
                info["offset"],
                "eax"
            )

        else:
            raise RuntimeError(
                f"Unsupported LISP variable kind: {kind}"
            )

        return value_type

    def visitAtom(self, ctx):
        if ctx.NUMBER():
            value = int(ctx.NUMBER().getText(), 10)
            self.emit_mov("eax", value)
            return "integer"

        if ctx.STRING():
            raw = ctx.STRING().getText()
            value = raw[1:-1]

            label = self.add_string_literal(value)

            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.writer.emit_mov_reg_data_label32("eax", label)
            else:
                self.emit_lea_label("rax", label)

            return "string"

        if ctx.SYMBOL():
            name = ctx.SYMBOL().getText().lower()

            if name in ("nil", "false"):
                self.emit_mov("eax", 0)
                return "nil" if name == "nil" else "boolean"

            if name in ("t", "true"):
                self.emit_mov("eax", 1)
                return "boolean"

            return self.emit_load_lisp_variable(
                ctx,
                name
            )

        raise CompileError(
            ctx,
            "E0015",
            got=ctx.getText(),
            expected="atom"
        )
        
    def visitList(self, ctx):
        expressions = ctx.expression()

        if not expressions:
            self.emit_mov("eax", 0)
            return "nil"

        operator_ctx = expressions[0]

        if (
            operator_ctx.atom() is None
            or operator_ctx.atom().SYMBOL() is None
        ):
            raise CompileError(
                operator_ctx,
                "E0005",
                got=operator_ctx.getText(),
                expected="operator symbol"
            )

        operator = (
            operator_ctx
            .atom()
            .SYMBOL()
            .getText()
            .lower()
        )

        args    = expressions[1:]
        handler = self.handlers.get(operator)

        if handler is not None:
            return handler(ctx, args)

        return self.emit_lisp_function_call(
            ctx,
            operator,
            args
        )

    def get_expression_list_info(self, expression_ctx):
        list_ctx = expression_ctx.list_()

        if list_ctx is None:
            return None, None, []

        expressions = list_ctx.expression()

        if not expressions:
            return None, list_ctx, []

        operator_ctx = expressions[0]

        if (operator_ctx.atom() is None or operator_ctx.atom().SYMBOL() is None):
            return None, list_ctx, expressions[1:]

        operator = (
            operator_ctx
            .atom()
            .SYMBOL()
            .getText()
            .lower()
        )

        return operator, list_ctx, expressions[1:]
        
    def register_lisp_defun(self, ctx, args):
        if len(args) < 3:
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected="name, parameter list and body"
            )

        name_ctx   = args[0]
        params_ctx = args[1]
        body       = args[2:]

        function_name = self.get_symbol_expression(
            name_ctx
        )

        param_list_ctx = params_ctx.list_()

        if param_list_ctx is None:
            raise CompileError(
                params_ctx,
                "E0005",
                got=params_ctx.getText(),
                expected="parameter list"
            )

        parameter_names = []

        for parameter_ctx in param_list_ctx.expression():
            parameter_name = self.get_symbol_expression(
                parameter_ctx
            )

            if parameter_name in parameter_names:
                raise CompileError(
                    parameter_ctx,
                    "E0002",
                    identifier=parameter_name
                )

            parameter_names.append(parameter_name)

        if function_name in self.functions:
            raise CompileError(
                ctx,
                "E0002",
                identifier=function_name
            )

        function_info = {
            "name": function_name,
            "label": f"lisp_func_{function_name}",

            "parameters": parameter_names,

            "parameter_types": [
                "integer"
                for _ in parameter_names
            ],

            "return_type": None,

            # ParseTree-Kontexte für den zweiten Durchlauf
            "ctx": ctx,
            "body": body,

            "emitted": False,
        }

        self.functions[function_name] = function_info
        self.function_definitions.append(function_info)

        return function_info

    def emit_registered_lisp_function(self, function_info):
        if function_info["emitted"]:
            return function_info["return_type"]

        function_info["emitted"] = True

        function_label = function_info["label"]
        parameter_names = function_info["parameters"]
        body = function_info["body"]

        self.emit_bind_label(function_label)

        # NT32-cdecl-Prolog
        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        old_function = self.current_func
        self.current_func = function_info

        local_scope = {}

        for index, parameter_name in enumerate(
            parameter_names
        ):
            local_scope[parameter_name] = {
                "name": parameter_name,
                "type": "integer",
                "kind": "parameter",

                # [ebp+8]  = erster Parameter
                # [ebp+12] = zweiter Parameter
                "offset": 8 + index * 4,
            }

        self.local_scopes.append(local_scope)

        try:
            result_type = "nil"

            for expression in body:
                result_type = self.visit(expression)

            function_info["return_type"] = result_type

            # Der letzte Ausdruck hinterlässt sein Ergebnis in EAX.

        finally:
            self.local_scopes.pop()
            self.current_func = old_function

        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()

        return function_info["return_type"]

    def emit_lisp_main(self):
        if self.main_emitted:
            raise RuntimeError(
                "LISP _main was already emitted"
            )

        self.main_emitted = True
        self.emit_bind_label("_main")

        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        result_type = "nil"

        # Top-Level-Code dient als Initialisierung.
        for expression in self.top_level_forms:
            result_type = self.visit(expression)

        entry_name = self.entry_function_name

        # Ohne explizites (start ...) wird eine vorhandene
        # Funktion namens main automatisch verwendet.
        if entry_name is None and "main" in self.functions:
            entry_name = "main"

        if entry_name is not None:
            function_info = self.functions.get(
                entry_name
            )

            if function_info is None:
                raise CompileError(
                    None,
                    "E0001",
                    identifier=entry_name
                )

            if function_info["parameters"]:
                raise RuntimeError(
                    f"LISP start function '{entry_name}' "
                    "must not have parameters"
                )

            # Internes lokales Funktionslabel aufrufen.
            self.emit_call_lbl(
                function_info["label"]
            )

            result_type = (
                function_info["return_type"]
                or "integer"
            )

        elif not self.top_level_forms:
            # Leeres Programm liefert NIL beziehungsweise 0.
            self.emit_mov("eax", 0)
            result_type = "nil"

        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()

        return result_type
