# ---------------------------------------------------------------------------
# File:   generatorbase.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations
from antlr4      import ParseTreeVisitor

import os
import sys

from compiler.common.constants import *
from compiler.common.error     import *
from compiler.common.types     import *

class CodeGeneratorBase:
    def __init__(self, backend):
        self.backend = backend
        
        self.writer  = None
        self.coff    = None

        # Symboltabellen
        self.global_vars = {}
        self.local_vars  = {}
        
        self.routines      = {}
        self.label_counter = 0
        
        self.break_label_stack    = []
        self.continue_label_stack = []
        
        self.current_proc_params  = {}
        self.current_func_params  = {}
        
        self.current_proc_name    = None
        self.current_func         = None
        
        self.variables = {}
        self.functions = {}

        # Slotverwaltung
        self.next_int_slot      = 0
        self.next_double_slot   = 0
        self.next_string_slot   = 0
        self.next_bool_slot     = 0
        self.next_pointer_slot  = 0
        
        self.label_id           = 0

        # Scopes
        self.scope_stack  = []
        self.local_scopes = []
        
        self.lines              = self.backend.lines
        self.asm_label_mappings = []
        
        self.subrange_types     = {}
        self.vars               = {}
        self.next_slot          = 0
        self.program_name       = "Program"
        self.var_types          = {}
        
        self.source_file        = None
        self.source_dir         = None
        
        self.string_literals    = []
        self.double_literals    = []
        
        self.main_emitted       = False
        
        self.pending_open_array_actual  = None
        self.next_open_array_literal_id = 0

    def allocate_slot(self, var_type):
        # Integer, Boolean und Char werden als 32-Bit-Werte
        # gemeinsam in int_vars gespeichert.
        if var_type in (
            "integer",
            "boolean",
            "char"
        ):
            slot = self.next_int_slot
            self.next_int_slot += 1
            return slot

        if var_type == "double":
            slot = self.next_double_slot
            self.next_double_slot += 1
            return slot

        if var_type == "string":
            slot = self.next_string_slot
            self.next_string_slot += 1
            return slot

        if var_type.startswith("^"):
            slot = self.next_pointer_slot
            self.next_pointer_slot += 1
            return slot

        raise RuntimeError(
            f"Unsupported type: {var_type}"
        )

    def is_nt32(self):
        return CDATA.args_target in ["nt35", "winnt", "win32"]
    
    # ------------------------------------------------------------
    # Bereits vorhandenes identisches Literal wiederverwenden
    # ------------------------------------------------------------
    def add_string_literal(self, text):
        for label, old_text in self.string_literals:
            if old_text == text:
                return label

        label = f"str_{len(self.string_literals)}"
        self.string_literals.append((label, text))

        target = CDATA.args_target.lower()

        # ------------------------------------------------------------
        # DOS
        # ------------------------------------------------------------
        if target in ["dos", "dos16"]:
            if self.writer is None:
                raise RuntimeError(
                    "DOS writer not installed"
                )

            self.writer.add_dos_string(
                label,
                text
            )

            return label

        # ------------------------------------------------------------
        # Windows COFF32 / COFF64
        #
        # Gilt sowohl für:
        #   - reine .o/.obj-Dateien
        #   - spätere EXE-/DLL-Erzeugung
        # ------------------------------------------------------------
        if target in ["nt35", "winnt", "win32", "win64"]:
            coff = getattr(self, "coff", None)

            if coff is None:
                raise RuntimeError(
                    "COFF writer not installed"
                )

            if coff.find_symbol_index(label) is None:
                coff.add_data_string(
                    label,
                    text
                )

            return label

        raise RuntimeError(
            f"string literal target not supported: {target}"
        )
        
    def declare_global_var(self, ctx, name, var_type, is_const=False):
        key = name.lower()

        if key in self.global_vars:
            raise CompileError(
                ctx,
                "E0002",
                identifier=name
            )

        slot = self.allocate_slot(var_type)

        info = {
            "name": name,
            "type": var_type,
            "slot": slot,
            "const": is_const,
            "initialized": False,
        }

        self.global_vars[key] = info

        return info

    def format_error(self, filename, err):
        template = ERROR_MAP.get(
            err.code,
            err.code
        )

        params = dict(err.params)

        # Kompatibilität für ältere Fehleraufrufe.
        if ("name"       not in params and "identifier" in params): params["name"]       = params["identifier"]
        if ("identifier" not in params and "name"       in params): params["identifier"] = params["name"]

        try:
            message = template.format(**params)

        except KeyError as exc:
            missing = str(exc).strip("'")

            message = (
                f"{template} "
                f"[missing error parameter: {missing}; "
                f"params={params}]"
            )

        return (
            f"{err.code}: "
            f"{os.path.basename(filename)} "
            f"{err.line}:{err.column} "
            f"{message}"
        )

    def add_asm_label_mapping(self, asmjit_label, target_label):
        self.asm_label_mappings.append({
            "asmjit": asmjit_label,
            "target": target_label
        })
    
    def new_named_label(self, prefix):
        name = self.new_label_name(prefix)
        asmjit_label = f"L{len(self.asm_label_mappings)}"

        self.emit_new_label_decl(name)

        self.add_asm_label_mapping(
            asmjit_label,
            name
        )

        return name
    
    def emit_store_var(self, name, var_type=None):
        key = name.lower()

        if key not in self.global_vars:
            raise RuntimeError(
                f"Unknown variable: {name}"
            )

        info = self.global_vars[key]

        if var_type is None:
            var_type = info["type"]

        slot = info["slot"]

        # ---------------------------------------------------------
        # Integer / Boolean / Char
        # ---------------------------------------------------------
        if var_type in (
            "integer",
            "boolean",
            "char"
        ):
            if not self.is_nt32():
                raise RuntimeError(
                    f"emit_store_var({var_type}): "
                    "target not implemented"
                )

            # Boolean sicher auf 0 oder 1 normalisieren.
            if var_type == "boolean":
                self.emit_cmp("eax", 0)
                self.emit_setne("al")
                self.emit_movzx("eax", "al")

            # edx = ctx->int_vars
            self.backend.writer.emit_mov_reg_mem32(
                "edx",
                "ebx",
                JIT_CONTEXT_OFFSETS["int_vars"]
            )

            # int_vars[slot] = eax
            self.backend.writer.emit_mov_mem_reg32(
                "edx",
                slot * 4,
                "eax"
            )

            return

        # ---------------------------------------------------------
        # Double
        # ---------------------------------------------------------
        if var_type == "double":
            if not self.is_nt32():
                raise RuntimeError(
                    "emit_store_var(double): "
                    "target not implemented"
                )

            # edx = ctx->double_vars
            self.backend.writer.emit_mov_reg_mem32(
                "edx",
                "ebx",
                JIT_CONTEXT_OFFSETS["double_vars"]
            )

            # double_vars[slot] = xmm0
            self.backend.writer.emit_movsd_store32(
                "edx",
                slot * 8,
                "xmm0"
            )

            return

        raise RuntimeError(
            f"emit_store_var: unsupported type: {var_type}"
        )

    def write_string_literals_to_coff(self):
        for label, text in self.string_literals:
            if self.writer.find_symbol_index(label) is None:
                self.writer.add_data_string(label, text)

    def write_double_literals_to_coff(self):
        for name, value in self.double_literals:
            self.writer.add_data_double(name, float(value))

    def emit(self, line):
        self.backend.emit(line)
    
    def emit_add(self, reg, value, comment=""):
        self.backend.emit_add(reg, value, comment)

    def emit_imul(self, dst, src, value=None, comment=""):
        self.backend.emit_imul(dst, src, value, comment)
    
    def emit_bind_label(self, label, comment=""):
        self.backend.emit_bind_label(label, comment)

    def emit_new_label_decl(self, name, comment=""):
        self.backend.emit_new_label_decl(name, comment)
    
    def emit_call(self, dst, comment=""):
        self.backend.emit_call(dst, comment)

    def emit_cmp(self, reg, value, comment=""):
        self.backend.emit_cmp(reg, value, comment)

    def emit_cmp_dword(self, reg, base, field, comment=""):
        self.backend.emit_cmp_dword(reg, base, field, comment)

    def emit_dec(self, reg, comment=""): self.backend.emit_dec(reg, comment)

    def emit_jg(self, label, comment=""): self.backend.emit_jg(label, comment)
    def emit_jl(self, label, comment=""): self.backend.emit_jl(label, comment)
    def emit_jz(self, label, comment=""): self.backend.emit_jz(label, comment)
    def emit_jb(self, label, comment=""): self.backend.emit_jb(label, comment)
    def emit_ja(self, label, comment=""): self.backend.emit_ja(label, comment)
    def emit_jae(self, label, comment=""): self.backend.emit_jae(label, comment)
    def emit_jbe(self, label, comment=""): self.backend.emit_jbe(label, comment)
    def emit_je(self, label, comment=""): self.backend.emit_je(label, comment)
    def emit_jle(self, label, comment=""): self.backend.emit_jle(label, comment)
    def emit_jge(self, label, comment=""): self.backend.emit_jge(label, comment)
    def emit_jne(self, label, comment=""): self.backend.emit_jne(label, comment)
    def emit_jnz(self, label, comment=""): self.backend.emit_jnz(label, comment)

    def emit_jmp(self, target, comment=""):
        self.backend.emit_jmp(target, comment)
    
    def emit_lea_byte (self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_byte(reg1, reg2, offset, comment)
        
    def emit_lea_dword(self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_dword(reg1, reg2, offset, comment)
        
    def emit_lea_qword(self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_qword(reg1, reg2, offset, comment)
    
    def emit_mov_byte (self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_byte(reg1, reg2, vars, comment)
    
    def emit_mov_dword(self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_dword(reg1, reg2, vars, comment)
        
    def emit_mov_qword(self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_qword(reg1, reg2, vars, comment)
    
    def emit_new_label_decl(self, name, comment=""):
        self.backend.emit_new_label_decl(name, comment)

    def emit_ucomisd(self, left, right, comment=""): self.backend.emit_ucomisd(left, right, comment)
    
    def emit_jb(self, label, comment=""): self.backend.emit_jb(label, comment)
    def emit_jbe(self, label, comment=""): self.backend.emit_jbe(label, comment)
    def emit_ja(self, label, comment=""): self.backend.emit_ja(label, comment)
    def emit_jae(self, label, comment=""): self.backend.emit_jae(label, comment)

    def emit_mov    (self, dst, src, comment=""): self.backend.emit_mov    (dst, src, comment)
    def emit_mov_imm(self, dst, src, comment=""): self.backend.emit_mov_imm(dst, src, comment)
    def emit_movzx  (self, dst, src, comment=""): self.backend.emit_movzx  (dst, src, comment)
    def emit_movsxd (self, dst, src, comment=""): self.backend.emit_movsxd (dst, src, comment)
    def emit_movq(self, dst, src, comment=""): self.backend.emit_movq(dst, src, comment)
    def emit_movsd_load(self, dst, base, offset=0, comment=""): self.backend.emit_movsd_load(dst, base, offset, comment)
    def emit_movsd_load_field(self, dst, base, field, comment=""): self.backend.emit_movsd_load_field(dst, base, field, comment)
    def emit_movsd_store(self, base, offset, src, comment=""): self.backend.emit_movsd_store(base, offset, src, comment)
    def emit_ucomisd(self, dst, src, comment=""): self.backend.emit_ucomisd(dst, src, comment)
    def emit_cvtsi2sd(self, dst, src, comment=""): self.backend.emit_cvtsi2sd(dst, src, comment)
    def emit_movapd(self, dst, src, comment=""): self.backend.emit_movapd(dst, src, comment)
    def emit_addsd(self, dst, src, comment=""): self.backend.emit_addsd(dst, src, comment)
    def emit_subsd(self, dst, src, comment=""): self.backend.emit_subsd(dst, src, comment)
    def emit_mulsd(self, dst, src, comment=""): self.backend.emit_mulsd(dst, src, comment)
    def emit_divsd(self, dst, src, comment=""): self.backend.emit_divsd(dst, src, comment)
    def emit_cdq(self, comment=""): self.backend.emit_cdq(comment)
    def emit_idiv(self, reg, comment=""): self.backend.emit_idiv(reg, comment)
    def emit_mov_byte_ptr (self, dst, base, offset=0, comment=""): self.backend.emit_mov_byte_ptr (dst, base, offset, comment)
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""): self.backend.emit_mov_dword_ptr(dst, base, offset, comment)
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""): self.backend.emit_mov_qword_ptr(dst, base, offset, comment)
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_qword_ptr_store(base, offset, src, comment)
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_dword_ptr_store(base, offset, src, comment)
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_byte_ptr_store(base, offset, src, comment)
    def emit_mov_reg_byte (self, dst, base, comment=""): self.backend.emit_mov_reg_byte (dst, base, comment)
    def emit_mov_reg_dword(self, dst, base, comment=""): self.backend.emit_mov_reg_dword(dst, base, comment)
    def emit_mov_reg_qword(self, dst, base, comment=""): self.backend.emit_mov_reg_qword(dst, base, comment)
    def emit_test(self, reg1, reg2, comment=""): self.backend.emit_test(reg1, reg2, comment)
    def emit_call_reg(self, target, comment=""): self.backend.emit_call_reg(target, comment)
    def emit_call_lbl(self, target, comment=""): self.backend.emit_call_lbl(target, comment)
    
    def emit_and(self, dst, src, comment=""):
        self.backend.emit_and(dst, src, comment)
        
    def emit_xor(self, dst, src, comment=""):
        self.backend.emit_xor(dst, src, comment)
    
    def emit_push(self, reg, comment=""): self.backend.emit_push(reg, comment)
    def emit_pop (self, reg, comment=""): self.backend.emit_pop (reg, comment)
    
    def emit_sub (self, reg, value, comment=""):
        self.backend.emit_sub(reg, value, comment)
    
    def emit_ret(self, comment=""):
        self.backend.emit_ret(comment)
    
    def emit_backend_jmp(self, label):
        self.backend.emit_jmp(label)
    
    def emit_backend_label(self, label):
        self.backend.emit_bind_label(label)
    
    def emit_load_integer_const(self, value):
        self.backend.emit_mov_imm("eax", value)
        return "integer"

    def emit_load_var(self, name):
        key = name.lower()

        if key not in self.global_vars:
            raise RuntimeError(
                f"Unknown variable: {name}"
            )

        info     = self.global_vars[key]
        var_type = info["type"]
        slot     = info["slot"]

        # ---------------------------------------------------------
        # Integer / Boolean / Char
        # ---------------------------------------------------------
        if var_type in (
            "integer",
            "boolean",
            "char"
        ):
            if not self.is_nt32():
                raise RuntimeError(
                    f"emit_load_var({var_type}): "
                    "target not implemented"
                )

            # edx = ctx->int_vars
            self.backend.writer.emit_mov_reg_mem32(
                "edx",
                "ebx",
                JIT_CONTEXT_OFFSETS["int_vars"]
            )

            # eax = int_vars[slot]
            self.backend.writer.emit_mov_reg_mem32(
                "eax",
                "edx",
                slot * 4
            )

            # Bei Boolean vorsichtshalber normalisieren.
            if var_type == "boolean":
                self.emit_cmp("eax", 0)
                self.emit_setne("al")
                self.emit_movzx("eax", "al")

            return

        # ---------------------------------------------------------
        # Double
        # ---------------------------------------------------------
        if var_type == "double":
            if not self.is_nt32():
                raise RuntimeError(
                    "emit_load_var(double): "
                    "target not implemented"
                )

            self.backend.writer.emit_mov_reg_mem32(
                "edx",
                "ebx",
                JIT_CONTEXT_OFFSETS["double_vars"]
            )

            self.backend.writer.emit_movsd_load32(
                "xmm0",
                "edx",
                slot * 8
            )

            return

        raise RuntimeError(
            f"emit_load_var: unsupported type: {var_type}"
        )
    
    def emit_load_parameter(self, info):
        param_type = info["type"]
        access     = info["access"]
        offset     = info["stack_offset"]

        if CDATA.args_target not in ["nt35", "winnt", "win32"]:
            raise RuntimeError(
                "emit_load_parameter: target noch nicht implementiert"
            )

        if param_type in ("integer", "boolean", "char"):
            if access == "var":
                # VAR-Parameter enthält eine Adresse.
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
                # Wert- oder CONST-Parameter.
                self.backend.writer.emit_mov_reg_mem32(
                    "eax",
                    "ebp",
                    offset
                )

            return

        raise RuntimeError(
            f"emit_load_parameter: unsupported type {param_type}"
        )

    def new_label_name(self, prefix):
        self.label_id += 1
        return f"{prefix}_{self.label_id}"

    def emit_sete (self, reg, comment=""): self.backend.emit_sete (reg, comment)
    def emit_setne(self, reg, comment=""): self.backend.emit_setne(reg, comment)
    def emit_setl (self, reg, comment=""): self.backend.emit_setl (reg, comment)
    def emit_setle(self, reg, comment=""): self.backend.emit_setle(reg, comment)
    def emit_setg (self, reg, comment=""): self.backend.emit_setg (reg, comment)
    def emit_setge(self, reg, comment=""): self.backend.emit_setge(reg, comment)
    