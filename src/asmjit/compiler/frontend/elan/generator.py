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

from antlr4      import ParseTreeVisitor, TerminalNode
from antlr4      import *

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
class ElanGenerator(CodeGeneratorBase, ElanParserVisitor):
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
    
    def visitMultiplicativeExpression(self, ctx):
        operands = ctx.unaryExpression()

        if not operands:
            raise RuntimeError(
                "multiplicativeExpression contains no operands"
            )

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
            # Linken Zwischenwert sichern.
            self.emit_push("eax")

            right_type = self.visit(operands[index])

            if right_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="integer"
                )

            # Nach dem Besuch:
            #
            # eax = rechter Operand
            # ecx = linker Operand
            self.emit_pop("ecx")

            operator = ctx.getChild(index * 2 - 1).getText().upper()

            if operator == "*":
                # ecx = ecx * eax
                self.emit_imul("ecx", "eax")

                # Ergebnis-Konvention: eax
                self.emit_mov("eax", "ecx")

            elif operator in ("/", "DIV"):
                ok_label = self.new_named_label(
                    "divisor_not_zero"
                )
                
                # Divisor liegt noch in EAX.
                self.emit_cmp("eax", 0)
                self.emit_jne(ok_label)

                self.emit_call("_jit_error_divide_by_zero")
                
                # ecx = Dividend
                # eax = Divisor
                self.emit_bind_label(ok_label)
                self.emit_push("esi")
                self.emit_mov("esi", "eax")

                self.emit_mov("eax", "ecx")
                self.emit_cdq()
                self.emit_idiv("esi")

                # Quotient liegt bereits in EAX.
                self.emit_pop("esi")

            elif operator == "MOD":
                # ecx = Dividend
                # eax = Divisor

                self.emit_push("esi")
                self.emit_mov("esi", "eax")

                self.emit_mov("eax", "ecx")
                self.emit_cdq()
                self.emit_idiv("esi")

                # Bei IDIV:
                #   eax = Quotient
                #   edx = Rest
                self.emit_mov("eax", "edx")

                self.emit_pop("esi")

            else:
                raise RuntimeError(
                    f"Unsupported multiplicative operator: {operator}"
                )

        return "integer"

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

    def emit_load_identifier(self, ctx, name):
        key = name.strip().lower()

        # Parameter
        info = self.current_proc_params.get(key)

        if info is not None:
            self.emit_load_parameter(info)
            return info["type"]

        # Globale Variable
        info = self.global_vars.get(key)

        if info is not None:
            self.emit_load_var(name)
            return info["type"]

        raise CompileError(
            ctx,
            "E0001",
            name=name
        )

    def visitPrimaryExpression(self, ctx):
        # ---------------------------------------------------------
        # Literal
        # ---------------------------------------------------------
        if ctx.literal() is not None:
            return self.visit(ctx.literal())

        # ---------------------------------------------------------
        # qualifiedName
        # ---------------------------------------------------------
        if hasattr(ctx, "qualifiedName"):
            qualified_ctx = ctx.qualifiedName()

            if qualified_ctx is not None:
                name = qualified_ctx.getText()
                return self.emit_load_identifier(ctx, name)

        # ---------------------------------------------------------
        # Direkter IDENTIFIER-Token
        # ---------------------------------------------------------
        if hasattr(ctx, "IDENTIFIER"):
            ident = ctx.IDENTIFIER()

            if ident is not None:
                if isinstance(ident, list):
                    ident = ident[0] if ident else None

                if ident is not None:
                    name = ident.getText()
                    return self.emit_load_identifier(ctx, name)

        # ---------------------------------------------------------
        # Eventuell separate identifier-/variableReference-Regel
        # ---------------------------------------------------------
        for method_name in (
            "identifier",
            "variableReference",
            "objectReference",
            "nameReference",
        ):
            if not hasattr(ctx, method_name):
                continue

            child_ctx = getattr(ctx, method_name)()

            if child_ctx is not None:
                name = child_ctx.getText()
                return self.emit_load_identifier(ctx, name)

        # ---------------------------------------------------------
        # Geklammerter Ausdruck
        # ---------------------------------------------------------
        if ctx.expression() is not None:
            return self.visit(ctx.expression())

        if ctx.ifExpression() is not None:
            return self.visit(ctx.ifExpression())

        raise RuntimeError(
            "Unsupported primary expression: "
            + ctx.getText()
        )
    
    def visitIfStatement(self, ctx):
        end_label  = self.new_named_label("if_end")
        next_label = self.new_named_label("if_next")
        
        # ---------------------------------------------------------
        # Hauptbedingung
        # ---------------------------------------------------------
        condition_type = self.visit(ctx.expression())

        if condition_type not in ("boolean", "integer"):
            raise CompileError(
                ctx,
                "E0005",
                got=condition_type,
                expected="boolean"
            )

        self.emit_cmp("eax", 0)
        self.emit_je(next_label)

        then_paragraph = ctx.paragraph()

        if then_paragraph is None:
            raise RuntimeError(tr("IF statement contains no THEN paragraph"))

        self.visit(then_paragraph)
        
        self.emit_jmp(end_label)
        self.emit_bind_label(next_label)

        # ---------------------------------------------------------
        # ELIF-Zweige
        # ---------------------------------------------------------
        for elif_ctx in ctx.elifPart():
            next_elif_label = self.new_named_label(
                "elif_next"
            )

            elif_type = self.visit(
                elif_ctx.expression()
            )

            if elif_type not in ("boolean", "integer"):
                raise CompileError(
                    elif_ctx,
                    "E0005",
                    got=elif_type,
                    expected="boolean"
                )

            self.emit_cmp("eax", 0)
            self.emit_je(next_elif_label)

            self.visit(
                elif_ctx.paragraph()
            )

            self.emit_jmp(end_label)
            self.emit_bind_label(next_elif_label)

        # ---------------------------------------------------------
        # ELSE
        # ---------------------------------------------------------
        else_ctx = ctx.elsePart()

        if else_ctx is not None:
            self.visit(
                else_ctx.paragraph()
            )

        self.emit_bind_label(end_label)

        return None

    def add_double_literal(self, value):
        value = float(value)
        for label, existing_value in self.double_literals:
            if existing_value == value:
                return label
                
        label = f"real_{len(self.double_literals)}"
        self.double_literals.append((label, value))
        return label

    def visitEqualityExpression(self, ctx):
        operands = ctx.relationalExpression()

        # Kein Gleichheitsvergleich
        if len(operands) == 1:
            return self.visit(operands[0])

        left_type = self.visit(operands[0])

        if left_type not in ("integer", "boolean", "char"):
            raise CompileError(
                ctx,
                "E0005",
                got=left_type,
                expected="integer, boolean or char"
            )

        for index in range(1, len(operands)):
            # linken Wert sichern
            self.emit_push("eax")

            right_type = self.visit(operands[index])

            if right_type != left_type:
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected=left_type
                )

            # eax = rechter Wert
            # ecx = linker Wert
            self.emit_pop("ecx")

            operator = ctx.getChild(index * 2 - 1).getText().upper()

            self.emit_cmp("ecx", "eax")

            if operator in ("=", "=="):
                self.emit_sete("al")

            elif operator in ("<>", "/=", "!="):
                self.emit_setne("al")

            else:
                raise RuntimeError(
                    f"Unsupported equality operator: {operator}"
                )

            self.emit_movzx("eax", "al")

            left_type = "boolean"

        return "boolean"
    
    def visitLiteral(self, ctx):
        if ctx.INTEGER_LITERAL() is not None:
            value = int(ctx.INTEGER_LITERAL().getText())
            self.emit_mov_imm("eax", value)
            return "integer"

        if ctx.REAL_LITERAL() is not None:
            literal_text = ctx.REAL_LITERAL().getText()
            value        = float(literal_text.replace(",", "."))
            label        = f"real_{len(self.double_literals)}"
            self.double_literals.append((label, value))

            if self.writer.find_symbol_index(label) is None:
                self.writer.add_data_double(label, value)

            self.writer.emit_movsd_xmm0_data_label32(label)
            return "double"

        if ctx.STRING_LITERAL() is not None:
            raw_text = ctx.STRING_LITERAL().getText()
            text     = raw_text[1:-1]
            label    = f"str_{len(self.string_literals)}"
            self.string_literals.append((label, text))
            
            # Symbol sofort in .data anlegen
            if self.writer.find_symbol_index(label) is None:
                self.writer.add_data_string(label, text)

            # Adresse des Strings nach EAX laden
            self.emit_mov_imm("eax", label)
            return "string"

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

    def emit_load_parameter(self, info):
        param_type = info["type"]
        access     = info["access"]
        offset     = info["stack_offset"]

        if param_type not in ("integer", "boolean", "char"):
            raise RuntimeError(
                f"Unsupported parameter type: {param_type}"
            )

        if access == "var":
            self.backend.writer.emit_mov_reg_mem32(
                "edx",
                "ebp",
                offset
            )

            self.backend.writer.emit_mov_reg_mem32(
                "eax",
                "edx",
                0
            )
        else:
            self.backend.writer.emit_mov_reg_mem32(
                "eax",
                "ebp",
                offset
            )

    def resolve_identifier_value(self, ctx, name):
        key = name.lower()

        # Parameter der aktuellen Routine
        info = self.current_proc_params.get(key)

        if info is not None:
            self.emit_load_parameter(info)
            return info["type"]

        # Globale Variable
        info = self.global_vars.get(key)

        if info is not None:
            self.emit_load_var(name)
            return info["type"]

        raise CompileError(
            ctx,
            "E0001",
            name=name
        )
    
    def visitTypeName(self, ctx):
        text = ctx.getText().upper()
        return ELAN_TYPES.get(text, text.lower())
    
    def visitProcedureDeclaration(self, ctx):
        proc_name = ctx.IDENTIFIER(0).getText()
        proc_key  = proc_name.lower()
        label     = f"elan_proc_{proc_key}"

        old_proc_name   = self.current_proc_name
        old_proc_params = self.current_proc_params

        parameter_map  = {}
        parameter_list = []
        stack_offset   = 8

        params_ctx = ctx.formalParameterList()

        if params_ctx is not None:
            groups = params_ctx.formalParameterGroup()

            if not isinstance(groups, list):
                groups = [groups]

            for group in groups:
                param_type = self.visit(group.typeName())
                access     = "value"

                access_ctx = group.parameterAccess()

                if access_ctx is not None:
                    if access_ctx.VAR() is not None:
                        access = "var"
                    elif access_ctx.CONST() is not None:
                        access = "const"

                identifiers = group.identifierList().IDENTIFIER()

                if not isinstance(identifiers, list):
                    identifiers = [identifiers]

                for ident in identifiers:
                    param_name = ident.getText()
                    param_key  = param_name.lower()

                    info = {
                        "name":         param_name,
                        "type":         param_type,
                        "access":       access,
                        "stack_offset": stack_offset
                    }

                    parameter_map[param_key] = info
                    parameter_list.append(info)

                    stack_offset += 4

        result_type = "void"

        if ctx.resultType() is not None:
            result_type = self.visit(
                ctx.resultType()
            )

        self.routines[proc_key] = {
            "name":        proc_name,
            "label":       label,
            "result_type": result_type,
            "params":      parameter_list
        }

        self.current_proc_name   = proc_name
        self.current_proc_params = parameter_map

        self.emit_bind_label(label)

        if CDATA.args_target in [
            "nt35",
            "winnt",
            "win32"
        ]:
            self.emit_push("ebp")
            self.emit_mov("ebp", "esp")

        try:
            self.visit(
                ctx.procedureBody()
            )

        finally:
            if CDATA.args_target in [
                "nt35",
                "winnt",
                "win32"
            ]:
                self.emit_mov("esp", "ebp")
                self.emit_pop("ebp")
                self.emit_ret()

            self.current_proc_name   = old_proc_name
            self.current_proc_params = old_proc_params

        return None
    
    def visitPostfixExpression(self, ctx):
        primary = ctx.primaryExpression()

        # Kein Aufruf/Indexer/Memberzugriff.
        postfix_parts = []

        if hasattr(ctx, "postfixPart"):
            postfix_parts = ctx.postfixPart()

        if not postfix_parts:
            return self.visit(primary)

        # Der erste Ausdruck muss hier ein Routinenname sein.
        qualified = primary.qualifiedName()

        if qualified is None:
            raise RuntimeError(
                f"Unsupported postfix expression: {ctx.getText()}"
            )

        routine_name = qualified.getText()
        routine_key  = routine_name.lower()

        if routine_key not in self.routines:
            raise CompileError(
                ctx,
                "E0001",
                name=routine_name
            )

        if len(postfix_parts) != 1:
            raise RuntimeError(
                f"Unsupported postfix chain: {ctx.getText()}"
            )

        part = postfix_parts[0]

        if not hasattr(part, "actualParameterList"):
            raise RuntimeError(
                f"Unsupported postfix operation: {part.getText()}"
            )

        return self.emit_routine_call(
            ctx,
            self.routines[routine_key],
            part.actualParameterList()
        )
    
    def emit_routine_call(self, ctx, routine, args_ctx):
        if (
            args_ctx is not None
            and args_ctx.expressionList() is not None
        ):
            args = list(
                args_ctx.expressionList().expression()
            )
        else:
            args = []

        params = routine["params"]

        if len(args) != len(params):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(args)),
                expected=str(len(params))
            )

        if CDATA.args_target not in ["nt35", "winnt", "win32"]:
            raise RuntimeError(
                "ELAN routine calls are currently implemented only for NT32"
            )

        # cdecl: Argumente von rechts nach links auswerten und pushen.
        for index in range(len(args) - 1, -1, -1):
            arg_ctx = args[index]
            param   = params[index]

            arg_type = self.visit(arg_ctx)

            if arg_type != param["type"]:
                raise CompileError(
                    arg_ctx,
                    "E0005",
                    got=arg_type,
                    expected=param["type"]
                )

            if param["access"] == "var":
                raise RuntimeError(
                    "VAR parameters are not implemented for ELAN calls yet"
                )

            # Integer, BOOL, CHAR und Pointer: jeweils 4 Byte.
            if arg_type in (
                "integer",
                "boolean",
                "char"
            ):
                self.emit_push("eax")
                continue

            raise RuntimeError(
                f"Unsupported ELAN argument type: {arg_type}"
            )

        # Interne Routine, daher kein DLL-/Import-Aufruf.
        self.backend.emit_call_lbl(
            routine["label"]
        )

        stack_bytes = len(args) * 4

        if stack_bytes:
            self.emit_add(
                "esp",
                stack_bytes
            )

        return routine["result_type"]
    
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

    def visitRepeatUntilStatement(self, ctx):
        body_label      = self.new_named_label("repeat_body")
        condition_label = self.new_named_label("repeat_condition")
        end_label       = self.new_named_label("repeat_end")

        # BREAK verlässt die Schleife.
        # CONTINUE springt bei REPEAT zur UNTIL-Bedingung.
        self.break_label_stack.append(end_label)
        self.continue_label_stack.append(condition_label)

        try:
            # ---------------------------------------------------------
            # Schleifenkörper
            #
            # REPEAT/UNTIL wird immer mindestens einmal ausgeführt.
            # ---------------------------------------------------------
            self.emit_bind_label(body_label)

            self.visit(
                ctx.paragraph()
            )

            # ---------------------------------------------------------
            # UNTIL-Bedingung
            # ---------------------------------------------------------
            self.emit_bind_label(condition_label)

            condition_type = self.visit(
                ctx.expression()
            )

            if condition_type not in (
                "boolean",
                "integer"
            ):
                raise CompileError(
                    ctx.expression(),
                    "E0005",
                    got=condition_type,
                    expected="boolean"
                )

            # UNTIL bedeutet:
            #
            # Bedingung TRUE  -> Schleife beenden
            # Bedingung FALSE -> Körper erneut ausführen
            self.emit_cmp("eax", 0)
            self.emit_je(body_label)

            self.emit_bind_label(end_label)

        finally:
            self.continue_label_stack.pop()
            self.break_label_stack.pop()

        return None

    def visitForStatement(self, ctx):
        # Erwartete Grammatik:
        #
        # FOR IDENTIFIER FROM expression
        #     (UPTO | DOWNTO)
        #     expression
        # REP
        #     paragraph
        # ENDREP

        loop_name = ctx.IDENTIFIER().getText()
        loop_key  = loop_name.lower()

        expressions = ctx.expression()

        if expressions is None:
            expressions = []
        elif not isinstance(expressions, list):
            expressions = [expressions]

        if len(expressions) != 2:
            raise RuntimeError(
                "FOR statement requires start and end expression"
            )

        start_expr = expressions[0]
        end_expr   = expressions[1]

        direction = ctx.forDirection().getText().upper()

        if direction not in ("UPTO", "DOWNTO"):
            raise RuntimeError(
                f"Unsupported FOR direction: {direction}"
            )

        # ---------------------------------------------------------
        # Vorhandenes Symbol sichern.
        #
        # Die FOR-Variable ist innerhalb der Schleife sichtbar und
        # überschattet vorübergehend ein gleichnamiges Symbol.
        # ---------------------------------------------------------
        previous_loop_info = self.global_vars.get(loop_key)

        # Eigener Integer-Slot für die Schleifenvariable.
        loop_info = {
            "name":        loop_name,
            "type":        "integer",
            "slot":        self.allocate_slot("integer"),
            "const":       False,
            "initialized": True,
            "for_control": True,
        }

        # Verdeckter Slot für die obere beziehungsweise untere Grenze.
        limit_name = self.new_label_name("__for_limit")
        limit_key  = limit_name.lower()

        limit_info = {
            "name":        limit_name,
            "type":        "integer",
            "slot":        self.allocate_slot("integer"),
            "const":       False,
            "initialized": True,
            "for_limit":   True,
        }

        # Der Grenzwert kann sofort registriert werden. Die sichtbare
        # Schleifenvariable wird erst nach Auswertung der Grenzen gebunden.
        self.global_vars[limit_key] = limit_info

        condition_label = self.new_named_label("for_condition")
        continue_label  = self.new_named_label("for_continue")
        end_label       = self.new_named_label("for_end")

        try:
            # ---------------------------------------------------------
            # Startwert einmal auswerten und vorübergehend sichern.
            # ---------------------------------------------------------
            start_type = self.visit(start_expr)

            if start_type != "integer":
                raise CompileError(
                    start_expr,
                    "E0005",
                    got=start_type,
                    expected="integer"
                )

            self.emit_push("eax")

            # ---------------------------------------------------------
            # Endwert ebenfalls nur einmal auswerten.
            # ---------------------------------------------------------
            end_type = self.visit(end_expr)

            if end_type != "integer":
                raise CompileError(
                    end_expr,
                    "E0005",
                    got=end_type,
                    expected="integer"
                )

            self.emit_store_var(limit_name)

            # Startwert wiederherstellen.
            self.emit_pop("eax")

            # Ab jetzt ist i im Schleifenkörper sichtbar.
            self.global_vars[loop_key] = loop_info
            self.emit_store_var(loop_name)

            # BREAK springt zum Ende.
            # CONTINUE springt zur Inkrement-/Dekrementstelle.
            self.break_label_stack.append(end_label)
            self.continue_label_stack.append(continue_label)

            try:
                # -----------------------------------------------------
                # Schleifenbedingung
                # -----------------------------------------------------
                self.emit_bind_label(condition_label)

                # EAX = aktuelle Schleifenvariable
                self.emit_load_var(loop_name)
                self.emit_push("eax")

                # EAX = Grenze
                self.emit_load_var(limit_name)

                # ECX = Schleifenvariable
                # EAX = Grenze
                self.emit_pop("ecx")
                self.emit_cmp("ecx", "eax")

                if direction == "UPTO":
                    # Ende, sobald i > Grenze.
                    self.emit_jg(end_label)

                else:
                    # Ende, sobald i < Grenze.
                    self.emit_jl(end_label)

                # -----------------------------------------------------
                # Schleifenkörper
                # -----------------------------------------------------
                self.visit(ctx.paragraph())

                # -----------------------------------------------------
                # CONTINUE-Ziel und Schritt
                # -----------------------------------------------------
                self.emit_bind_label(continue_label)

                self.emit_load_var(loop_name)

                if direction == "UPTO":
                    self.emit_add("eax", 1)
                else:
                    self.emit_sub("eax", 1)

                self.emit_store_var(loop_name)

                self.emit_jmp(condition_label)
                self.emit_bind_label(end_label)

            finally:
                self.continue_label_stack.pop()
                self.break_label_stack.pop()

        finally:
            # Verdeckten Grenzwert aus der Compilersymboltabelle entfernen.
            self.global_vars.pop(limit_key, None)

            # Vorherigen Namenskontext wiederherstellen.
            if previous_loop_info is None:
                self.global_vars.pop(loop_key, None)
            else:
                self.global_vars[loop_key] = previous_loop_info

        return None

    def visitQualifiedName(self, ctx):
        name = ctx.getText()
        key  = name.strip().lower()

        info = self.current_proc_params.get(key)

        if info is not None:
            print("LOAD PARAMETER:", key, info)

            self.emit_load_parameter(info)

            return info["type"]

        info = self.global_vars.get(key)

        if info is not None:
            print("LOAD GLOBAL:", key, info)

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

    def visitBuiltinProcedureStatement(self, ctx):
        if (ctx.LINE() is not None or ctx.NEWLINE() is not None):
            self.emit_call("_jit_print_newline")
            return None

        raise RuntimeError(
            "Unsupported builtin procedure: "
            + ctx.getText()
        )

    def visitResultType(self, ctx):
        return self.visit(
            ctx.typeName()
        )

    def visitResultExpression(self, ctx):
        result_type = self.visit(
            ctx.expression()
        )

        routine = self.routines.get(
            self.current_proc_name.lower()
        )

        if routine is None:
            raise RuntimeError(
                "Result expression outside routine"
            )

        expected_type = routine["result_type"]

        if result_type != expected_type:
            raise CompileError(
                ctx,
                "E0005",
                got=result_type,
                expected=expected_type
            )

        # Integer-Ergebnis bleibt in EAX.
        # REAL-Ergebnis bleibt in XMM0.
        return result_type
    
    def visitProcedureCallStatement(self, ctx):
        name = ctx.qualifiedName().getText()
        key  = name.lower()

        args_ctx = ctx.actualParameterList()

        if (args_ctx.expressionList() is not None):
            args = list(args_ctx.expressionList().expression())
        else:
            args = []

        # ---------------------------------------------------------
        # put
        # ---------------------------------------------------------
        if key == "put":
            if not args:
                raise CompileError(
                    ctx,
                    "E0005",
                    got="0",
                    expected="at least 1 argument"
                )

            for arg in args:
                arg_type = self.visit(arg)

                if arg_type == "integer":
                    self.emit_push("eax")
                    self.emit_call("_jit_print_int")
                    self.emit_add("esp", 4)

                elif arg_type == "string":
                    self.emit_push("eax")
                    self.emit_call("_jit_print_text")
                    self.emit_add("esp", 4)

                elif arg_type == "char":
                    self.emit_push("eax")
                    self.emit_call("_jit_print_char")
                    self.emit_add("esp", 4)

                else:
                    raise CompileError(
                        arg,
                        "E0005",
                        got=arg_type,
                        expected="integer, string or char"
                    )

            return None

        # ---------------------------------------------------------
        # Benutzerdefinierte Prozedur
        # ---------------------------------------------------------
        if key in self.routines:
            routine = self.routines[key]

            if routine["result_type"] != "void":
                raise RuntimeError(
                    f"Function {name} used as procedure"
                )

            self.emit_routine_call(
                ctx,
                routine,
                args_ctx
            )

            return None

        raise CompileError(
            ctx,
            "E0001",
            name=name
        )

    def get_terminal_tokens(self, ctx):
        result = []

        if ctx is None:
            return result

        for child in ctx.getChildren():
            if isinstance(child, TerminalNode):
                result.append(child.getSymbol())
            else:
                result.extend(
                    self.get_terminal_tokens(child)
                )

        return result

    def visitProcedureBody(self, ctx):
        items = ctx.declarationOrStatement()

        if items is None:
            items = []
        elif not isinstance(items, list):
            items = [items]

        for item in items:
            self.visit(item)

        result_ctx = ctx.resultExpression()

        if result_ctx is not None:
            return self.visit(result_ctx)

        routine = self.routines.get(
            self.current_proc_name.lower()
        )

        if (
            routine is not None
            and routine["result_type"] != "void"
        ):
            raise RuntimeError(
                f"Function {self.current_proc_name} "
                "has no result expression"
            )

        return None

    def collect_formal_parameters(self, ctx):
        params_ctx = ctx.formalParameterList()

        if params_ctx is None:
            return []

        tokens = self.get_terminal_tokens(params_ctx)

        groups = []
        current = []

        for token in tokens:
            text = token.text

            if text in ("(", ")"):
                continue

            if text == ",":
                if current:
                    groups.append(current)
                    current = []
                continue

            current.append(token)

        if current:
            groups.append(current)

        result = []

        for group_tokens in groups:
            type_name  = None
            access     = "value"
            param_name = None

            for token in group_tokens:
                text  = token.text
                upper = text.upper()

                if upper in ELAN_TYPES:
                    type_name = ELAN_TYPES[upper]
                    continue

                if upper == "CONST":
                    access = "const"
                    continue

                if upper == "VAR":
                    access = "var"
                    continue

                # Alles, was kein Typ und kein Zugriffsmodifikator ist,
                # ist hier der Parametername.
                if upper not in {
                    "INT",
                    "REAL",
                    "TEXT",
                    "BOOL",
                    "CHAR",
                    "CONST",
                    "VAR",
                }:
                    param_name = text

            if type_name is None:
                raise RuntimeError(
                    "Parameter type not found in: "
                    + " ".join(
                        token.text
                        for token in group_tokens
                    )
                )

            if param_name is None:
                raise RuntimeError(
                    "Parameter name not found in: "
                    + " ".join(
                        token.text
                        for token in group_tokens
                    )
                )

            result.append({
                "name":   param_name,
                "type":   type_name,
                "access": access,
            })

        return result
        
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
