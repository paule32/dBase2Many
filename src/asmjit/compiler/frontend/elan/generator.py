# ---------------------------------------------------------------------------
# File:   generator.py - ELAN/EUMEL compiler
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

from antlr4      import ParseTreeVisitor
from antlr4      import *

from compiler.frontend.pascal.preprocessor   import PascalPreprocessor

from parsers.elan.ElanLexer          import ElanLexer
from parsers.elan.ElanParser         import ElanParser
from parsers.elan.ElanParserVisitor  import ElanParserVisitor

from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.constants import *

from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.writer.pe64coff        import *
from compiler.frontend.generatorbase import *

ELAN_TYPES = {
    "INT":    "integer",
    "REAL":   "double",
    "TEXT":   "string",
    "BOOL":   "boolean",
    "CHAR":   "char",
}

# ---------------------------------------------------------------------------
# generator classes
# ---------------------------------------------------------------------------
class GeneratorClass(CodeGeneratorBase, ElanParserVisitor):
    def __init__(self, backend, writer=None):
        CodeGeneratorBase.__init__(self, backend)
        ElanParserVisitor.__init__(self)
        
        self.writer  = writer
        self.coff    = None

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

    def visitExpression              (self, ctx): return self.visit(ctx.logicalOrExpression())
    def visitLogicalOrExpression     (self, ctx): return self.visit(ctx.logicalXorExpression(0))
    def visitLogicalXorExpression    (self, ctx): return self.visit(ctx.logicalAndExpression(0))
    def visitLogicalAndExpression    (self, ctx): return self.visit(ctx.equalityExpression(0))
    def visitEqualityExpression      (self, ctx): return self.visit(ctx.relationalExpression(0))
    def visitRelationalExpression    (self, ctx): return self.visit(ctx.additiveExpression(0))
    def visitMultiplicativeExpression(self, ctx): return self.visit(ctx.unaryExpression(0))

    def visitAdditiveExpression(self, ctx):
        operands = ctx.multiplicativeExpression()

        result_type = self.visit(operands[0])

        if len(operands) == 1:
            return result_type

        if result_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected="integer"
            )

        for index in range(1, len(operands)):
            self.emit_push("eax")

            right_type = self.visit(operands[index])

            if right_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="integer"
                )

            # eax = rechter Wert
            # ecx = linker Wert
            self.emit_pop("ecx")

            operator = ctx.getChild(index * 2 - 1).getText()

            if operator == "+":
                self.emit_add("ecx", "eax")
                self.emit_mov("eax", "ecx")

            elif operator == "-":
                self.emit_sub("ecx", "eax")
                self.emit_mov("eax", "ecx")

            else:
                raise RuntimeError(
                    f"Unsupported additive operator: {operator}"
                )

        return "integer"
    
    def visitUnaryExpression(self, ctx):
        if ctx.postfixExpression() is not None:
            return self.visit(ctx.postfixExpression())

        # später: +, -, NOT
        return self.visit(ctx.unaryExpression())

    def visitPostfixExpression(self, ctx):
        return self.visit(ctx.primaryExpression())

    def visitPrimaryExpression(self, ctx):
        if ctx.literal      () is not None: return self.visit(ctx.literal())
        if ctx.qualifiedName() is not None: return self.visit(ctx.qualifiedName())
        if ctx.expression   () is not None: return self.visit(ctx.expression())
        if ctx.ifExpression () is not None: return self.visit(ctx.ifExpression())

        return self.visitChildren(ctx)
    
    def visitLiteral(self, ctx):
        if ctx.INTEGER_LITERAL() is not None:
            value = int(ctx.INTEGER_LITERAL().getText())

            self.emit_mov_imm("eax", value)

            return "integer"

        if ctx.REAL_LITERAL() is not None:
            value = float(ctx.REAL_LITERAL().getText())

            # später: Double-Literal in XMM0 laden
            raise RuntimeError("REAL literal noch nicht implementiert")

        if ctx.STRING_LITERAL() is not None:
            text = ctx.STRING_LITERAL().getText()[1:-1]

            # später: String-Literal erzeugen
            raise RuntimeError("TEXT literal noch nicht implementiert")

        if ctx.CHAR_LITERAL() is not None:
            text = ctx.CHAR_LITERAL().getText()

            if len(text) < 3:
                raise RuntimeError("Invalid CHAR literal")

            value = ord(text[1])
            self.emit_mov_imm("eax", value)

            return "char"

        if ctx.TRUE() is not None:
            self.emit_mov_imm("eax", 1)
            return "boolean"

        if ctx.FALSE() is not None:
            self.emit_mov_imm("eax", 0)
            return "boolean"

        if ctx.NIL() is not None:
            self.emit_mov_imm("eax", 0)
            return "nil"

        raise RuntimeError(
            f"Unsupported literal: {ctx.getText()}"
        )

    def visitTypeName(self, ctx):
        text = ctx.getText().upper()
        return ELAN_TYPES.get(text, text.lower())
    
    def visitProcedureDeclaration(self, ctx):
        proc_name = ctx.IDENTIFIER(0).getText()

        old_proc_name   = self.current_proc_name
        old_proc_params = self.current_proc_params

        self.current_proc_name   = proc_name
        self.current_proc_params = {}

        label = f"elan_proc_{proc_name.lower()}"

        self.emit_bind_label(label)

        # NT32-Prolog
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            self.emit_push("ebp")
            self.emit_mov("ebp", "esp")

        stack_offset = 8

        params_ctx = ctx.formalParameterList()

        if params_ctx is not None:
            for group in params_ctx.formalParameterGroup():
                param_type = self.visit(group.typeName())

                access = "value"

                if group.parameterAccess() is not None:
                    if group.parameterAccess().VAR() is not None:
                        access = "var"
                    elif group.parameterAccess().CONST() is not None:
                        access = "const"

                for ident in group.identifierList().IDENTIFIER():
                    param_name = ident.getText()
                    key = param_name.lower()

                    if key in self.current_proc_params:
                        raise CompileError(
                            ctx,
                            "E0002",
                            name=param_name
                        )

                    self.current_proc_params[key] = {
                        "name":         param_name,
                        "type":         param_type,
                        "access":       access,
                        "stack_offset": stack_offset
                    }

                    stack_offset += 4

        try:
            self.visit(ctx.procedureBody())

        finally:
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                self.emit_mov("esp", "ebp")
                self.emit_pop("ebp")
                self.emit_ret()

            self.current_proc_name   = old_proc_name
            self.current_proc_params = old_proc_params

        return None
    
    def visitObjectDeclaration(self, ctx):
        var_type = self.visit(ctx.typeName())
        is_const = ctx.objectAccess().CONST() is not None

        if hasattr(ctx, "objectDeclarator"):
            declarators = ctx.objectDeclarator()

        elif hasattr(ctx, "identifierInitList"):
            init_list = ctx.identifierInitList()
            declarators = init_list.identifierInitializer()

        else:
            raise RuntimeError(
                "objectDeclaration: neither objectDeclarator nor identifierInitList found"
            )

        for decl in declarators:
            name = decl.IDENTIFIER().getText()

            info = self.declare_global_var(
                ctx,
                name,
                var_type,
                is_const=is_const
            )

            expr_ctx = decl.expression()

            if expr_ctx is not None:
                expr_type = self.visit(expr_ctx)

                if expr_type != var_type:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got=expr_type,
                        expected=var_type
                    )

                self.emit_store_var(name)
                info["initialized"] = True

        return None
    
    def visitWhileStatement(self, ctx):
        condition_label = self.new_named_label("while_condition")
        end_label       = self.new_named_label("while_end")

        # Für BREAK und CONTINUE
        self.break_label_stack.append(end_label)
        self.continue_label_stack.append(condition_label)

        try:
            # WHILE-Bedingung
            self.emit_bind_label(condition_label)

            condition_type = self.visit(ctx.expression())

            if condition_type not in ("boolean", "integer"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=condition_type,
                    expected="boolean"
                )

            # eax == 0 bedeutet false
            self.emit_cmp("eax", 0)
            self.emit_je(end_label)

            # Schleifenkörper
            self.visit(ctx.paragraph())

            # Zur Bedingung zurück
            self.emit_jmp(condition_label)

            # Schleifenende
            self.emit_bind_label(end_label)

        finally:
            self.continue_label_stack.pop()
            self.break_label_stack.pop()

        return None

    def visitQualifiedName(self, ctx):
        name = ctx.getText()
        key  = name.lower()

        # ---------------------------------------------------------
        # Prozedur- oder Funktionsparameter
        # ---------------------------------------------------------
        if key in self.current_proc_params:
            info = self.current_proc_params[key]
            self.emit_load_parameter(info)
            return info["type"]

        # ---------------------------------------------------------
        # Globale Variable
        # ---------------------------------------------------------
        if key in self.global_vars:
            info = self.global_vars[key]
            self.emit_load_var(name)
            return info["type"]

        raise CompileError(
            ctx,
            "E0001",
            name=name
        )

    def visitRelationalExpression(self, ctx):
        operands = ctx.additiveExpression()

        # Kein Vergleich
        if len(operands) == 1:
            return self.visit(operands[0])

        left_type = self.visit(operands[0])

        if left_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=left_type,
                expected="integer"
            )

        # Linken Wert sichern
        self.emit_push("eax")

        right_type = self.visit(operands[1])

        if right_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=right_type,
                expected="integer"
            )

        # eax = rechter Operand
        # ecx = linker Operand
        self.emit_pop("ecx")

        operator = ctx.getChild(1).getText()

        self.emit_cmp("ecx", "eax")

        if operator == "<":
            self.emit_setl("al")
        elif operator == "<=":
            self.emit_setle("al")
        elif operator == ">":
            self.emit_setg("al")
        elif operator == ">=":
            self.emit_setge("al")
        else:
            raise RuntimeError(
                f"Unsupported relational operator: {operator}"
            )

        #self.backend.writer.emit_movzx_r32_r8("eax", "al")
        self.backend.emit_movzx("eax", "al")

        return "boolean"

    def visitAssignmentStatement(self, ctx):
        name = ctx.assignable().getText()
        key  = name.lower()

        if key not in self.global_vars:
            raise CompileError(
                ctx,
                "E0001",
                name=name
            )

        info = self.global_vars[key]

        if info.get("const", False):
            raise RuntimeError(
                f"Cannot assign to constant: {name}"
            )

        expr_type = self.visit(ctx.expression())

        if expr_type != info["type"]:
            raise CompileError(
                ctx,
                "E0005",
                got=expr_type,
                expected=info["type"]
            )

        self.emit_store_var(name)

        return None
    
    def visitProcedureCallStatement(self, ctx):
        name = ctx.qualifiedName().getText()
        key  = name.lower()

        args_ctx = ctx.actualParameterList()

        if (
            args_ctx is not None
            and args_ctx.expressionList() is not None
        ):
            args = args_ctx.expressionList().expression()
        else:
            args = []

        # ---------------------------------------------------------
        # line / newline
        # ---------------------------------------------------------
        if key in ("line", "newline"):
            if args:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=str(len(args)),
                    expected="0 arguments"
                )

            self.emit_call("_jit_print_newline")
            return None

        # ---------------------------------------------------------
        # put
        # ---------------------------------------------------------
        if key == "put":
            if len(args) != 1:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=str(len(args)),
                    expected="1 argument"
                )

            arg_type = self.visit(args[0])

            if arg_type == "integer":
                self.emit_push("eax")
                self.emit_call("_jit_print_int")

                if CDATA.args_target in ["nt35", "winnt", "win32"]:
                    self.emit_add("esp", 4)

                return None

            raise CompileError(
                ctx,
                "E0005",
                got=arg_type,
                expected="integer"
            )

        raise CompileError(
            ctx,
            "E0001",
            name=name
        )
    
    def visitRefinement(self, ctx):
        name = ctx.refinementName().getText()
        normalized_name = name.lower()

        if normalized_name == "program":
            if self.main_emitted:
                raise RuntimeError("ELAN main refinement already emitted")

            self.main_emitted = True

            self.emit_bind_label("_main")
            self.visit(ctx.paragraph())
            self.emit_ret()

            return None

        label = f"elan_refinement_{normalized_name}"
        self.emit_bind_label(label)
        self.visit(ctx.paragraph())
        self.emit_ret()

        return None
