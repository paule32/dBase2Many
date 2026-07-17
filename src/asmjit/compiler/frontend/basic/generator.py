# ---------------------------------------------------------------------------
# File:   clisp.py - LISP compiler
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import sys
import os
import re
import io
import argparse
import struct
import time

# ---------------------------------------------------------------------------
# i18n / gettext (mo inside zip: <lang>/LC_MESSAGES/dbase.mo)
# ---------------------------------------------------------------------------
import locale
import gettext
import polib

# ---------------------------------------------------------------------------
from os          import linesep   as NL
from datetime    import datetime  as dt
from dataclasses import dataclass, field
from pathlib     import PureWindowsPath, Path
from typing      import Union

from compiler.common.config    import *
from compiler.common.types     import *
from compiler.common.constants import *
from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.locale    import *

from compiler.backend.code     import *
from compiler.backend.coff32   import Coff32Backend
from compiler.backend.coff64   import Coff64Backend
from compiler.backend.dos16    import *

from compiler.backend.asmjit   import *
from compiler.backend.nasm     import *

from compiler.frontend.generatorbase    import CodeGeneratorBase
from compiler.frontend.basic.generator  import *

from compiler.writer.pe64coff    import *

from compiler.writer.mz16 import *
from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.cli import *

from antlr4 import CommonTokenStream
from antlr4 import FileStream
from antlr4 import InputStream
from antlr4 import ParserRuleContext

from antlr4.tree.Tree import TerminalNode

from parsers.basic.BasicLexer          import BasicLexer
from parsers.basic.BasicParser         import BasicParser
from parsers.basic.BasicParserVisitor  import BasicParserVisitor

class NoSourceException(Exception):          pass
class NoCompilerModeException(Exception):    pass
class NoEntryRefinementException(Exception): pass

@dataclass
class BasicVariable:
    name: str
    type_name: str
    stack_offset: int

class BasicLayoutCollector(BasicParserVisitor):
    def __init__(self):
        super().__init__()
        
        self.variables = {}
        self.for_count = 0

    def visitVariableDecl(self, ctx):
        name = ctx.IDENT().getText().lower()

        if name not in self.variables:
            explicit_type = None

            if ctx.typeName():
                explicit_type = ctx.typeName().getText().lower()

            self.variables[name] = explicit_type

        return self.visitChildren(ctx)

    def visitForStatement(self, ctx):
        self.for_count += 1
        return self.visitChildren(ctx)

    def visitSubDeclaration(self, ctx):
        # Lokale Variablen von SUBs gehören nicht zum Hauptprogramm.
        return None

    def visitFunctionDeclaration(self, ctx):
        return None


class BasicGenerator(CodeGeneratorBase, BasicParserVisitor):
    def __init__(self, backend, writer):
        CodeGeneratorBase .__init__(self, backend)
        BasicParserVisitor.__init__(self)

        self.backend   = backend
        self.writer    = backend.writer
        self.coff      = backend.writer

        self.variables = {}
        self.constants = {}

        self.frame_size = 0
        self.next_stack_offset = 4
        self.next_double_literal_id = 0

        self.for_temp_offsets = []
        self.next_for_index = 0

        self.break_label_stack = []
        self.continue_label_stack = []

        self.main_exit_label = None
        
        if not hasattr(self.coff, "emit_push_data_label32"):
            raise RuntimeError(
                "BASIC generator requires a COFF code writer, "
                f"got: {type(self.coff).__name__}"
            )

    # ------------------------------------------------------------------
    # Allgemeine Hilfsfunktionen
    # ------------------------------------------------------------------
    @staticmethod
    def align(value, alignment):
        return (
            value + alignment - 1
        ) & ~(alignment - 1)

    @staticmethod
    def decode_string(text):
        if len(text) >= 2:
            text = text[1:-1]

        return text.replace('""', '"')

    @staticmethod
    def canonical_name(name):
        return name.lower()

    def infer_variable_type(self, name, explicit_type=None):
        if explicit_type:
            value = explicit_type.lower()

            mapping = {
                "integer": "integer",
                "long":    "integer",
                "boolean": "boolean",
                "string":  "string",

                # Erste Implementierung:
                # SINGLE und DOUBLE werden intern beide als IEEE-754 Double
                # in einem 64-Bit-Slot gespeichert.
                "single":  "double",
                "double":  "double",
            }

            if value not in mapping:
                raise RuntimeError(
                    f"Unsupported BASIC type: {explicit_type}"
                )

            return mapping[value]

        if name.endswith("$"):
            return "string"

        if name.endswith("%"):
            return "integer"

        if name.endswith("!"):
            return "double"

        if name.endswith("#"):
            return "double"

        return "integer"

    def is_integer_type(self, type_name):
        return type_name in (
            "integer",
            "boolean"
        )

    def is_numeric_type(self, type_name):
        return type_name in (
            "integer",
            "boolean",
            "double"
        )

    def save_expression_value(self, value_type):
        if value_type == "double":
            self.emit_sub(
                "esp",
                8,
                comment="save double expression"
            )

            self.backend.emit_movsd_store(
                "esp",
                0,
                "xmm0"
            )

            return

        if self.is_integer_type(value_type):
            self.emit_push(
                "eax",
                comment="save integer expression"
            )

            return

        raise RuntimeError(
            f"Cannot save expression type: {value_type}"
        )

    def restore_left_expression_value(self, value_type):
        if value_type == "double":
            self.backend.emit_movsd_load(
                "xmm1",
                "esp",
                0
            )

            self.emit_add(
                "esp",
                8,
                comment="restore double expression"
            )

            return

        if self.is_integer_type(value_type):
            self.emit_pop(
                "ecx",
                comment="restore integer expression"
            )

            return

        raise RuntimeError(
            f"Cannot restore expression type: {value_type}"
        )

    def get_variable(self, ctx, name):
        key = self.canonical_name(name)

        variable = self.variables.get(key)

        if variable is None:
            raise CompileError(
                ctx,
                "E0001",
                name=name
            )

        return variable

    def allocate_variable(self, name, type_name):
        key = self.canonical_name(name)

        if key in self.variables:
            return self.variables[key]

        variable = BasicVariable(
            name=key,
            type_name=type_name,
            stack_offset=self.next_stack_offset
        )

        self.variables[key] = variable

        # Zunächst für alle BASIC-Variablen 8 Byte reservieren.
        # Integer verwendet nur die unteren 4 Byte.
        self.next_stack_offset += 8

        return variable

    def allocate_temporary(self):
        offset = self.next_stack_offset
        self.next_stack_offset += 8
        return offset
    
    def emit_load_stack32(self, target, offset):
        self.coff.emit_mov_reg_mem32(
            self.backend.map_reg32(target),
            "ebp",
            -offset
        )

    def emit_store_stack32(self, offset, source):
        self.coff.emit_mov_mem_reg32(
            "ebp",
            -offset,
            self.backend.map_reg32(source)
        )

    def emit_load_variable(self, ctx, name):
        variable = self.get_variable(ctx, name)

        if variable.type_name == "double":
            self.backend.emit_movsd_load(
                "xmm0",
                "ebp",
                -variable.stack_offset
            )
            return "double"

        self.emit_load_stack32("eax", variable.stack_offset)
        return variable.type_name

    def emit_store_variable(
        self,
        ctx,
        name,
        value_type
    ):
        variable = self.get_variable(
            ctx,
            name
        )

        target_type = variable.type_name

        # ------------------------------------------------------------
        # Ziel ist DOUBLE
        # ------------------------------------------------------------
        if target_type == "double":
            if value_type in (
                "integer",
                "boolean"
            ):
                # eax -> xmm0
                self.backend.emit_cvtsi2sd(
                    "xmm0",
                    "eax"
                )

            elif value_type != "double":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="double"
                )

            self.backend.emit_movsd_store(
                "ebp",
                -variable.stack_offset,
                "xmm0"
            )

            return

        # ------------------------------------------------------------
        # Ziel ist INTEGER / BOOLEAN
        # ------------------------------------------------------------
        if value_type == "double":
            raise CompileError(
                ctx,
                "E0005",
                got="double",
                expected=target_type
            )

        compatible = (
            target_type == value_type
            or (
                target_type == "integer"
                and value_type == "boolean"
            )
            or (
                target_type == "boolean"
                and value_type == "integer"
            )
        )

        if not compatible:
            raise CompileError(
                ctx,
                "E0005",
                got=value_type,
                expected=target_type
            )

        self.emit_store_stack32(
            variable.stack_offset,
            "eax"
        )

    def emit_boolean_normalize(self):
        self.emit_cmp("eax", 0)
        self.emit_setne("al")
        self.emit_movzx("eax", "al")

    def emit_string_address(self, value):
        label = self.add_string_literal(value)

        # PE32Writer kennt bereits Relocations für:
        # push data_label
        #self.writer.emit_push_data_label32(label)
        self.coff.emit_push_data_label32(label)
        self.emit_pop("eax")

        return "string"

    def emit_print_text_literal(self, value):
        label = self.add_string_literal(value)

        self.writer.emit_push_data_label32(label)

        self.emit_nt32_call_cdecl(
            "_jit_print_text",
            4
        )

    def emit_print_value(self, value_type):
        if value_type == "string":
            self.emit_push("eax")

            self.emit_nt32_call_cdecl(
                "_jit_print_text",
                4
            )

            return

        if value_type in (
            "integer",
            "boolean"
        ):
            self.emit_push("eax")

            self.emit_nt32_call_cdecl(
                "_jit_print_int",
                4
            )

            return

        if value_type == "double":
            # cdecl:
            # Double als 8-Byte-Wert auf den Stack kopieren.
            self.coff.emit_sub_reg_imm32(
                "esp",
                8
            )

            self.coff.emit_movsd_qword_ptr_esp_xmm0()

            self.emit_nt32_call_cdecl(
                "_jit_print_double",
                8
            )

            return

        raise RuntimeError(
            f"PRINT does not support {value_type}"
        )

    def prepare_double_operands(
        self,
        ctx,
        left_type,
        right_type
    ):
        if not self.is_numeric_type(left_type):
            raise CompileError(
                ctx,
                "E0005",
                got=left_type,
                expected="numeric"
            )

        if not self.is_numeric_type(right_type):
            raise CompileError(
                ctx,
                "E0005",
                got=right_type,
                expected="numeric"
            )

        # Linker Wert liegt bei Integer in ecx.
        if left_type != "double":
            self.backend.emit_cvtsi2sd(
                "xmm1",
                "ecx"
            )

        # Rechter Wert liegt bei Integer in eax.
        if right_type != "double":
            self.backend.emit_cvtsi2sd(
                "xmm0",
                "eax"
            )

    # ------------------------------------------------------------------
    # Programmaufbau
    # ------------------------------------------------------------------
    def prepare_main_layout(self, ctx):
        collector = BasicLayoutCollector()
        collector.visit(ctx)

        for name, explicit_type in collector.variables.items():
            variable_type = self.infer_variable_type(
                name,
                explicit_type
            )

            self.allocate_variable(
                name,
                variable_type
            )

        # FOR benötigt:
        #   Endwert
        #   Schrittweite
        for _ in range(collector.for_count):
            end_offset = self.allocate_temporary()
            step_offset = self.allocate_temporary()

            self.for_temp_offsets.append(
                (end_offset, step_offset)
            )

        self.frame_size = self.align(
            max(self.next_stack_offset + 16, 32),
            16
        )

    def emit_main_prologue(self):
        self.emit_bind_label("_main")

        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        if self.frame_size:
            self.emit_sub(
                "esp",
                self.frame_size,
                comment="BASIC main frame"
            )

        self.emit_mov(
            "eax",
            0
        )

        # xmm0 = 0.0
        self.backend.emit_cvtsi2sd(
            "xmm0",
            "eax"
        )

        for variable in self.variables.values():
            if variable.type_name == "double":
                self.backend.emit_movsd_store(
                    "ebp",
                    -variable.stack_offset,
                    "xmm0"
                )
            else:
                self.emit_store_stack32(
                    variable.stack_offset,
                    "eax"
                )

    def emit_main_epilogue(self):
        self.emit_bind_label(
            self.main_exit_label
        )

        # Kein RET beim PE-Programmeinstieg.
        #
        # ExitProcess ist stdcall/noreturn und beendet den Prozess
        # unmittelbar.
        self.coff.emit_push_imm32(0)

        self.coff.emit_call_external(
            "ExitProcess"
        )

        # Markiert nur das Ende der COFF-Funktion.
        self.coff.end_function()

    def visitProgram(self, ctx):
        self.prepare_main_layout(ctx)

        self.main_exit_label = self.new_named_label(
            "basic_main_exit"
        )

        self.emit_main_prologue()

        for item in ctx.topLevelItem():
            # SUB und FUNCTION werden später separat emittiert.
            if item.statement():
                self.visit(item.statement())

        self.emit_main_epilogue()

        # Prozeduren hinter _main ausgeben.
        for item in ctx.topLevelItem():
            if item.subDeclaration():
                self.visit(item.subDeclaration())

            elif item.functionDeclaration():
                self.visit(item.functionDeclaration())

        return None

    # ------------------------------------------------------------------
    # Statements
    # ------------------------------------------------------------------

    def visitStatement(self, ctx):
        if ctx.lineNumber():
            line_number = ctx.lineNumber().getText()

            self.emit_bind_label(
                f"basic_line_{line_number}"
            )

        return self.visit(ctx.statementCore())

    def visitStatementCore(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitInlineStatement(self, ctx):
        return self.visit(ctx.getChild(0))

    def visitStatementBlock(self, ctx):
        for statement in ctx.statement():
            self.visit(statement)

        return None

    # ------------------------------------------------------------------
    # DIM
    # ------------------------------------------------------------------

    def visitDimStatement(self, ctx):
        for declaration in ctx.variableDecl():
            if declaration.expression():
                value_type = self.visit(
                    declaration.expression()
                )

                name = declaration.IDENT().getText()

                self.emit_store_variable(
                    declaration,
                    name,
                    value_type
                )

        return None

    # ------------------------------------------------------------------
    # Zuweisungen
    # ------------------------------------------------------------------

    def visitAssignmentStatement(self, ctx):
        target = ctx.lvalue()

        if target.argumentList():
            raise CompileError(
                ctx,
                "E0015",
                text="array assignment is not implemented yet"
            )

        name = target.IDENT().getText()

        value_type = self.visit(
            ctx.expression()
        )

        self.emit_store_variable(
            ctx,
            name,
            value_type
        )

        return None

    # ------------------------------------------------------------------
    # PRINT
    # ------------------------------------------------------------------

    def visitPrintStatement(self, ctx):
        print_list = ctx.printList()

        if print_list is None:
            self.emit_nt32_call_cdecl(
                "_jit_print_newline",
                0
            )

            return None

        trailing_separator = False

        for child in print_list.children:
            if isinstance(child, TerminalNode):
                if child.symbol.type == BasicParser.COMMA:
                    self.emit_print_text_literal(" ")
                    trailing_separator = True

                elif child.symbol.type == BasicParser.SEMI:
                    trailing_separator = True

                continue

            trailing_separator = False

            value_type = self.visit(child)
            self.emit_print_value(value_type)

        if not trailing_separator:
            self.emit_nt32_call_cdecl(
                "_jit_print_newline",
                0
            )

        return None

    # ------------------------------------------------------------------
    # IF
    # ------------------------------------------------------------------

    def visitInlineIf(self, ctx):
        else_label = self.new_named_label(
            "basic_if_else"
        )

        end_label = self.new_named_label(
            "basic_if_end"
        )

        condition_type = self.visit(
            ctx.expression()
        )

        if condition_type not in ("integer", "boolean"):
            raise CompileError(
                ctx,
                "E0005",
                got=condition_type,
                expected="boolean"
            )

        self.emit_cmp("eax", 0)
        self.emit_je(else_label)

        statements = ctx.inlineStatement()

        self.visit(statements[0])
        self.emit_jmp(end_label)

        self.emit_bind_label(else_label)

        if len(statements) > 1:
            self.visit(statements[1])

        self.emit_bind_label(end_label)

        return None

    def visitBlockIf(self, ctx):
        conditions = ctx.expression()
        blocks = ctx.statementBlock()

        end_label = self.new_named_label(
            "basic_if_end"
        )

        has_else = ctx.ELSE() is not None

        condition_count = len(conditions)

        for index in range(condition_count):
            next_label = self.new_named_label(
                "basic_if_next"
            )

            condition_type = self.visit(
                conditions[index]
            )

            if condition_type not in ("integer", "boolean"):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=condition_type,
                    expected="boolean"
                )

            self.emit_cmp("eax", 0)
            self.emit_je(next_label)

            self.visit(blocks[index])
            self.emit_jmp(end_label)

            self.emit_bind_label(next_label)

        if has_else:
            self.visit(blocks[-1])

        self.emit_bind_label(end_label)

        return None

    # ------------------------------------------------------------------
    # WHILE
    # ------------------------------------------------------------------

    def visitWhileStatement(self, ctx):
        start_label = self.new_named_label(
            "basic_while_start"
        )

        end_label = self.new_named_label(
            "basic_while_end"
        )

        self.break_label_stack.append(end_label)
        self.continue_label_stack.append(start_label)

        self.emit_bind_label(start_label)

        condition_type = self.visit(
            ctx.expression()
        )

        if condition_type not in ("integer", "boolean"):
            raise CompileError(
                ctx,
                "E0005",
                got=condition_type,
                expected="boolean"
            )

        self.emit_cmp("eax", 0)
        self.emit_je(end_label)

        self.visit(ctx.statementBlock())

        self.emit_jmp(start_label)
        self.emit_bind_label(end_label)

        self.continue_label_stack.pop()
        self.break_label_stack.pop()

        return None

    # ------------------------------------------------------------------
    # FOR / NEXT
    # ------------------------------------------------------------------

    def visitForStatement(self, ctx):
        target = ctx.lvalue()

        if target.argumentList():
            raise CompileError(
                ctx,
                "E0015",
                text="array FOR variable is not supported"
            )

        name = target.IDENT().getText()

        variable = self.get_variable(
            ctx,
            name
        )

        if variable.type_name != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=variable.type_name,
                expected="integer"
            )

        end_offset, step_offset = (
            self.for_temp_offsets[self.next_for_index]
        )

        self.next_for_index += 1

        expressions = ctx.expression()

        # Startwert
        start_type = self.visit(expressions[0])

        if start_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=start_type,
                expected="integer"
            )

        self.emit_store_stack32(
            variable.stack_offset,
            "eax"
        )

        # Endwert nur einmal auswerten
        end_type = self.visit(expressions[1])

        if end_type != "integer":
            raise CompileError(
                ctx,
                "E0005",
                got=end_type,
                expected="integer"
            )

        self.emit_store_stack32(
            end_offset,
            "eax"
        )

        # Schrittweite
        if len(expressions) >= 3:
            step_type = self.visit(expressions[2])

            if step_type != "integer":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=step_type,
                    expected="integer"
                )
        else:
            default_step = (
                -1
                if ctx.DOWNTO()
                else 1
            )

            self.emit_mov(
                "eax",
                default_step
            )

        self.emit_store_stack32(
            step_offset,
            "eax"
        )

        condition_label = self.new_named_label(
            "basic_for_condition"
        )

        continue_label = self.new_named_label(
            "basic_for_continue"
        )

        end_label = self.new_named_label(
            "basic_for_end"
        )

        self.break_label_stack.append(end_label)
        self.continue_label_stack.append(continue_label)

        self.emit_bind_label(condition_label)

        self.emit_load_stack32(
            "eax",
            variable.stack_offset
        )

        self.emit_load_stack32(
            "ecx",
            end_offset
        )

        self.emit_cmp("eax", "ecx")

        if ctx.DOWNTO():
            self.emit_jl(end_label)
        else:
            self.emit_jg(end_label)

        self.visit(ctx.statementBlock())

        self.emit_bind_label(continue_label)

        self.emit_load_stack32(
            "eax",
            variable.stack_offset
        )

        self.emit_load_stack32(
            "ecx",
            step_offset
        )

        self.emit_add("eax", "ecx")

        self.emit_store_stack32(
            variable.stack_offset,
            "eax"
        )

        self.emit_jmp(condition_label)

        self.emit_bind_label(end_label)

        self.continue_label_stack.pop()
        self.break_label_stack.pop()

        return None

    # ------------------------------------------------------------------
    # DO / LOOP
    # ------------------------------------------------------------------

    def emit_do_loop(
        self,
        body,
        condition,
        test_mode,
        test_position
    ):
        start_label = self.new_named_label(
            "basic_do_start"
        )

        condition_label = self.new_named_label(
            "basic_do_condition"
        )

        end_label = self.new_named_label(
            "basic_do_end"
        )

        self.break_label_stack.append(end_label)
        self.continue_label_stack.append(condition_label)

        self.emit_bind_label(start_label)

        if test_position == "pre":
            condition_type = self.visit(condition)

            if condition_type not in ("integer", "boolean"):
                raise CompileError(
                    condition,
                    "E0005",
                    got=condition_type,
                    expected="boolean"
                )

            self.emit_cmp("eax", 0)

            if test_mode == "while":
                self.emit_je(end_label)
            else:
                self.emit_jne(end_label)

        self.visit(body)

        self.emit_bind_label(condition_label)

        if test_position == "post":
            condition_type = self.visit(condition)

            if condition_type not in ("integer", "boolean"):
                raise CompileError(
                    condition,
                    "E0005",
                    got=condition_type,
                    expected="boolean"
                )

            self.emit_cmp("eax", 0)

            if test_mode == "while":
                self.emit_jne(start_label)
            else:
                self.emit_je(start_label)
        else:
            self.emit_jmp(start_label)

        self.emit_bind_label(end_label)

        self.continue_label_stack.pop()
        self.break_label_stack.pop()

    def visitDoWhilePre(self, ctx):
        self.emit_do_loop(
            ctx.statementBlock(),
            ctx.expression(),
            "while",
            "pre"
        )

    def visitDoUntilPre(self, ctx):
        self.emit_do_loop(
            ctx.statementBlock(),
            ctx.expression(),
            "until",
            "pre"
        )

    def visitDoWhilePost(self, ctx):
        self.emit_do_loop(
            ctx.statementBlock(),
            ctx.expression(),
            "while",
            "post"
        )

    def visitDoUntilPost(self, ctx):
        self.emit_do_loop(
            ctx.statementBlock(),
            ctx.expression(),
            "until",
            "post"
        )

    def visitDoForever(self, ctx):
        self.emit_do_loop(
            ctx.statementBlock(),
            None,
            None,
            None
        )

    # ------------------------------------------------------------------
    # EXIT und STOP
    # ------------------------------------------------------------------

    def visitExitStatement(self, ctx):
        if not self.break_label_stack:
            raise CompileError(
                ctx,
                "E0015",
                text="EXIT outside a loop"
            )

        self.emit_jmp(
            self.break_label_stack[-1]
        )

        return None

    def visitStopStatement(self, ctx):
        self.emit_jmp(self.main_exit_label)
        return None

    # ------------------------------------------------------------------
    # GOTO und Zeilennummern
    # ------------------------------------------------------------------

    def visitGotoStatement(self, ctx):
        target = ctx.jumpTarget()

        if target.INTEGER_LITERAL():
            label = (
                "basic_line_"
                + target.INTEGER_LITERAL().getText()
            )
        else:
            label = (
                "basic_label_"
                + target.IDENT().getText().lower()
            )

        self.emit_jmp(label)

        return None

    def visitLabelStatement(self, ctx):
        name = ctx.IDENT().getText().lower()

        self.emit_bind_label(
            f"basic_label_{name}"
        )

        return None

    # ------------------------------------------------------------------
    # Ausdrücke
    # ------------------------------------------------------------------

    def visitExpression(self, ctx):
        return self.visit(ctx.orExpression())

    def visitOrExpression(self, ctx):
        return self.emit_binary_chain(ctx)

    def visitXorExpression(self, ctx):
        return self.emit_binary_chain(ctx)

    def visitAndExpression(self, ctx):
        return self.emit_binary_chain(ctx)

    def visitComparisonExpression(self, ctx):
        return self.emit_binary_chain(ctx)

    def visitAdditiveExpression(self, ctx):
        return self.emit_binary_chain(ctx)

    def visitMultiplicativeExpression(self, ctx):
        return self.emit_binary_chain(ctx)

    def emit_binary_chain(self, ctx):
        left_type = self.visit(
            ctx.getChild(0)
        )

        child_index = 1

        while child_index < ctx.getChildCount():
            operator = ctx.getChild(
                child_index
            ).getText().upper()

            # Linken Ausdruck sichern.
            self.save_expression_value(
                left_type
            )

            # Rechter Ausdruck landet in eax oder xmm0.
            right_type = self.visit(
                ctx.getChild(child_index + 1)
            )

            # Linken Ausdruck nach ecx oder xmm1 laden.
            self.restore_left_expression_value(
                left_type
            )

            left_type = self.emit_binary_operator(
                ctx,
                operator,
                left_type,
                right_type
            )

            child_index += 2

        return left_type

    def emit_comparison_operator(
        self,
        ctx,
        operator,
        left_type,
        right_type
    ):
        if not self.is_numeric_type(left_type):
            raise CompileError(
                ctx,
                "E0005",
                got=left_type,
                expected="numeric"
            )

        if not self.is_numeric_type(right_type):
            raise CompileError(
                ctx,
                "E0005",
                got=right_type,
                expected="numeric"
            )

        # ------------------------------------------------------------
        # Doublevergleich
        # ------------------------------------------------------------

        if (
            left_type == "double"
            or right_type == "double"
        ):
            self.prepare_double_operands(
                ctx,
                left_type,
                right_type
            )

            # Vergleicht:
            #
            #     xmm1 mit xmm0
            #
            self.backend.emit_ucomisd(
                "xmm1",
                "xmm0"
            )

            if operator == "=":
                self.emit_sete("al")

            elif operator in (
                "<>",
                "!="
            ):
                self.emit_setne("al")

            elif operator == "<":
                self.emit_setb("al")

            elif operator == "<=":
                self.emit_setbe("al")

            elif operator == ">":
                self.emit_seta("al")

            elif operator == ">=":
                self.emit_setae("al")

            self.emit_movzx(
                "eax",
                "al"
            )

            return "boolean"

        # ------------------------------------------------------------
        # Integervergleich
        # ------------------------------------------------------------

        self.emit_cmp(
            "ecx",
            "eax"
        )

        if operator == "=":
            self.emit_sete("al")

        elif operator in (
            "<>",
            "!="
        ):
            self.emit_setne("al")

        elif operator == "<":
            self.emit_setl("al")

        elif operator == "<=":
            self.emit_setle("al")

        elif operator == ">":
            self.emit_setg("al")

        elif operator == ">=":
            self.emit_setge("al")

        self.emit_movzx(
            "eax",
            "al"
        )

        return "boolean"

    def emit_binary_operator(
        self,
        ctx,
        operator,
        left_type,
        right_type
    ):
        # ------------------------------------------------------------
        # Addition, Subtraktion und Multiplikation
        # ------------------------------------------------------------

        if operator in (
            "+",
            "-",
            "*"
        ):
            if not self.is_numeric_type(left_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=left_type,
                    expected="numeric"
                )

            if not self.is_numeric_type(right_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="numeric"
                )

            # Mindestens ein Operand ist Double.
            if (
                left_type == "double"
                or right_type == "double"
            ):
                self.prepare_double_operands(
                    ctx,
                    left_type,
                    right_type
                )

                if operator == "+":
                    self.backend.emit_addsd(
                        "xmm1",
                        "xmm0"
                    )

                elif operator == "-":
                    self.backend.emit_subsd(
                        "xmm1",
                        "xmm0"
                    )

                else:
                    self.backend.emit_mulsd(
                        "xmm1",
                        "xmm0"
                    )

                # Ausdrucksergebnis immer in xmm0.
                self.backend.emit_movapd(
                    "xmm0",
                    "xmm1"
                )

                return "double"

            # Reine Integeroperation.
            if operator == "+":
                self.emit_add(
                    "ecx",
                    "eax"
                )

            elif operator == "-":
                self.emit_sub(
                    "ecx",
                    "eax"
                )

            else:
                self.emit_imul(
                    "ecx",
                    "eax"
                )

            self.emit_mov(
                "eax",
                "ecx"
            )

            return "integer"

        # ------------------------------------------------------------
        # BASIC-Fließkommadivision /
        #
        # In BASIC ist:
        #
        #     /   Fließkommadivision
        #     \   Ganzzahldivision
        # ------------------------------------------------------------

        if operator == "/":
            self.prepare_double_operands(
                ctx,
                left_type,
                right_type
            )

            self.backend.emit_divsd(
                "xmm1",
                "xmm0"
            )

            self.backend.emit_movapd(
                "xmm0",
                "xmm1"
            )

            return "double"

        # ------------------------------------------------------------
        # Ganzzahldivision und MOD
        # ------------------------------------------------------------

        if operator in (
            "\\",
            "MOD"
        ):
            if not self.is_integer_type(left_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=left_type,
                    expected="integer"
                )

            if not self.is_integer_type(right_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="integer"
                )

            # ecx = linker Operand
            # eax = rechter Operand

            self.emit_mov(
                "ebx",
                "eax",
                comment="divisor"
            )

            self.emit_mov(
                "eax",
                "ecx",
                comment="dividend"
            )

            self.emit_cdq()
            self.emit_idiv("ebx")

            if operator == "MOD":
                self.emit_mov(
                    "eax",
                    "edx"
                )

            return "integer"

        # ------------------------------------------------------------
        # Vergleiche
        # ------------------------------------------------------------

        if operator in (
            "=",
            "<>",
            "!=",
            "<",
            "<=",
            ">",
            ">="
        ):
            return self.emit_comparison_operator(
                ctx,
                operator,
                left_type,
                right_type
            )

        # ------------------------------------------------------------
        # Logische Operatoren
        # ------------------------------------------------------------

        if operator in (
            "AND",
            "OR",
            "XOR"
        ):
            if not self.is_integer_type(left_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=left_type,
                    expected="integer or boolean"
                )

            if not self.is_integer_type(right_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected="integer or boolean"
                )

            if operator == "AND":
                self.emit_and(
                    "ecx",
                    "eax"
                )

            elif operator == "OR":
                self.emit_or(
                    "ecx",
                    "eax"
                )

            else:
                self.emit_xor(
                    "ecx",
                    "eax"
                )

            self.emit_mov(
                "eax",
                "ecx"
            )

            self.emit_boolean_normalize()

            return "boolean"

        # ------------------------------------------------------------
        # Stringverkettung
        # ------------------------------------------------------------

        if operator == "&":
            raise CompileError(
                ctx,
                "E0015",
                text="string concatenation is not implemented yet"
            )

        raise RuntimeError(
            f"Unsupported BASIC operator: {operator}"
        )

    def visitNotExpression(self, ctx):
        if ctx.NOT():
            value_type = self.visit(
                ctx.notExpression()
            )

            if not self.is_integer_type(value_type):
                raise CompileError(
                    ctx,
                    "E0005",
                    got=value_type,
                    expected="boolean or integer"
                )

            self.emit_cmp(
                "eax",
                0
            )

            self.emit_sete("al")

            self.emit_movzx(
                "eax",
                "al"
            )

            return "boolean"

        return self.visit(
            ctx.comparisonExpression()
        )
    
    def visitPowerExpression(self, ctx):
        left_type = self.visit(
            ctx.unaryExpression()
        )

        if not ctx.powerExpression():
            return left_type

        self.save_expression_value(left_type); right_type = \
        self.visit(ctx.powerExpression())
        self.restore_left_expression_value(left_type)

        if not self.is_numeric_type(left_type):
            raise CompileError(
                ctx,
                "E0005",
                got=left_type,
                expected="numeric"
            )

        if not self.is_numeric_type(right_type):
            raise CompileError(
                ctx,
                "E0005",
                got=right_type,
                expected="numeric"
            )

        raise CompileError(
            ctx,
            "E0015",
            text="power operator is not implemented yet"
        )

    def visitUnaryExpression(self, ctx):
        if ctx.primaryExpression():
            return self.visit(
                ctx.primaryExpression()
            )

        operator = ctx.getChild(0).getText()

        value_type = self.visit(
            ctx.unaryExpression()
        )

        if operator == "+":
            return value_type

        if operator == "-":
            if value_type == "integer":
                self.emit_neg("eax")
                return "integer"

            if value_type == "double":
                # xmm1 = 0.0
                self.emit_mov(
                    "eax",
                    0
                )

                self.backend.emit_cvtsi2sd(
                    "xmm1",
                    "eax"
                )

                # xmm1 = 0.0 - xmm0
                self.backend.emit_subsd(
                    "xmm1",
                    "xmm0"
                )

                self.backend.emit_movapd(
                    "xmm0",
                    "xmm1"
                )

                return "double"

        raise CompileError(
            ctx,
            "E0005",
            got=value_type,
            expected="numeric"
        )

    def visitPrimaryExpression(self, ctx):
        if ctx.literal():
            return self.visit(ctx.literal())

        if ctx.expression():
            return self.visit(ctx.expression())

        name = ctx.IDENT().getText()

        if ctx.LPAREN():
            raise CompileError(
                ctx,
                "E0015",
                text=(
                    "function calls and array accesses "
                    "are not implemented yet"
                )
            )

        return self.emit_load_variable(
            ctx,
            name
        )

    def visitLiteral(self, ctx):
        if ctx.INTEGER_LITERAL():
            value = int(
                ctx.INTEGER_LITERAL().getText()
            )

            self.emit_mov("eax", value)
            return "integer"

        if ctx.HEX_LITERAL():
            text = ctx.HEX_LITERAL().getText()
            value = int(text[2:], 16)

            self.emit_mov("eax", value)
            return "integer"

        if ctx.BINARY_LITERAL():
            text = ctx.BINARY_LITERAL().getText()
            value = int(text[2:], 2)

            self.emit_mov("eax", value)
            return "integer"

        if ctx.TRUE():
            self.emit_mov("eax", 1)
            return "boolean"

        if ctx.FALSE():
            self.emit_mov("eax", 0)
            return "boolean"

        if ctx.STRING_LITERAL():
            value = self.decode_string(
                ctx.STRING_LITERAL().getText()
            )

            return self.emit_string_address(value)

        if ctx.FLOAT_LITERAL():
            text  = ctx.FLOAT_LITERAL().getText()
            value = float(text)

            label = (
                f"basic_double_"
                f"{self.next_double_literal_id}"
            )

            self.next_double_literal_id += 1

            # Fügt 8 Byte IEEE-754-Double in die COFF-Datensektion ein.
            self.coff.add_data_double(
                label,
                value
            )

            # movsd xmm0, qword ptr [label]
            self.coff.emit_movsd_xmm0_data_label32(
                label
            )

            return "double"

        raise RuntimeError(
            f"Unsupported literal: {ctx.getText()}"
        )

    # ------------------------------------------------------------------
    # SUB / FUNCTION
    # ------------------------------------------------------------------

    def visitSubDeclaration(self, ctx):
        name = ctx.IDENT().getText().lower()

        label = f"basic_sub_{name}"

        self.emit_bind_label(label)

        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        # Separate lokale Symboltabelle und Parameterbehandlung
        # kommen im nächsten Ausbau.

        self.visit(ctx.statementBlock())

        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()

        return None

    def visitFunctionDeclaration(self, ctx):
        name = ctx.IDENT().getText().lower()

        label = f"basic_function_{name}"

        self.emit_bind_label(label)

        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        self.visit(ctx.statementBlock())

        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()

        return None
