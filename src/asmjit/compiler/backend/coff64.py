# ---------------------------------------------------------------------------
# File: coff64.py - backend for coff64
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.backend.code     import *

# ---------------------------------------------------------------------------
# Windows 64-Bit PE coff backend ...
# ---------------------------------------------------------------------------
class Coff64Backend(CodeBackend):
    def __init__(self, writer=None):
        super().__init__("nt35")
        
        if writer is None:
            raise Exception(tr("no writer given."))
            
        self.writer              = writer
        self.pending_call_symbol = None

    def emit_ucomisd(self, left, right, comment=""):
        self.writer.emit_ucomisd64(left, right)
    
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_r32(base, offset, src)

    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_r64(base, offset, src)

    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_r8(base, offset, src)

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""):
        self.writer.emit_mov_r8_mem(dst, base, offset)
        
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        self.writer.emit_mov_r32_mem(dst, base, offset)

    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""):
        self.writer.emit_mov_r64_mem(dst, base, offset)

    def emit_mov_ptr_dword(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_r32(base, offset, src)

    def emit_mov_ptr_qword(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_r64(base, offset, src)

    def emit_lea_dword(self, dst, base, offset=0, comment=""):
        self.writer.emit_lea_dword(dst, base, offset)

    def emit_lea_qword(self, dst, base, offset=0, comment=""):
        self.writer.emit_lea_qword(dst, base, offset)

    def emit_new_label_decl(self, name, comment=""):
        return

    def emit_mov_qword(self, dst, base, field, comment=""):
        self.writer.emit_mov_r64_mem(
            dst,
            base,
            JIT_CONTEXT_OFFSETS[field]
        )

    def emit_mov_dword(self, dst, base, field, comment=""):
        self.writer.emit_mov_r32_mem(
            dst,
            base,
            JIT_CONTEXT_OFFSETS[field]
        )

    def emit_mov_byte(self, dst, base, field, comment=""):
        self.writer.emit_mov_r8_mem(
            dst,
            base,
            JIT_CONTEXT_OFFSETS[field]
        )
    
    def emit_lea_qword(self, dst, base, offset, comment=""):
        self.writer.emit_lea_qword(dst, base, offset)

    def emit_lea_dword(self, dst, base, offset, comment=""):
        self.writer.emit_lea_dword(dst, base, offset)

    def emit_lea_byte(self, dst, base, offset, comment=""):
        self.writer.emit_lea_byte(dst, base, offset)

    def emit_bind_label(self, label, comment=""):
        self.writer.bind_label(label)

    def emit_push(self, reg, comment=""):
        self.writer.emit_push_r64(reg)

    def emit_pop(self, reg, comment=""):
        self.writer.emit_pop_r64(reg)

    def emit_ret(self, comment=""):
        self.writer.emit_ret()

    def emit_mov(self, dst, src, comment=""):
        if isinstance(src, str) and src.startswith("str_"):
            self.writer.emit_lea_reg_data_label(dst, src)
        else:
            self.writer.emit_mov(dst, src)

    def emit_mov_imm(self, dst, value, comment=""):
        if isinstance(value, str):
            if value.startswith("&"):
                name = value[1:]

                if name.startswith("_jit_") or name == "ExitProcess":
                    self.pending_call_symbol = name
                    return

                self.writer.emit_lea_reg_data_label(dst, name)
                return

            if (   value.startswith("str_")
                or value.startswith("dbl_")
                or value.startswith("_var_")
            ):
                self.coff.emit_lea_reg_data_label(dst, value)
                return

        self.writer.emit_mov(dst, value)

    def emit_add(self, dst, src, comment=""):
        self.writer.emit_add(dst, src)

    def emit_sub(self, dst, src, comment=""):
        self.writer.emit_sub(dst, src)

    def emit_imul(self, dst, src, value=None, comment=""):
        self.writer.emit_imul(dst, src, value)

    def emit_cmp(self, dst, src, comment=""):
        self.writer.emit_cmp(dst, src)
        
    def emit_test(self, a, b, comment=""):
        self.writer.emit_test(a, b)
        
    def emit_jmp(self, label, comment=""): self.writer.emit_jmp(label)
    def emit_je (self, label, comment=""): self.writer.emit_je (label)
    def emit_jne(self, label, comment=""): self.writer.emit_jne(label)
    def emit_jz (self, label, comment=""): self.writer.emit_jz (label)
    def emit_jnz(self, label, comment=""): self.writer.emit_jnz(label)
    def emit_jl (self, label, comment=""): self.writer.emit_jl (label)
    def emit_jle(self, label, comment=""): self.writer.emit_jle(label)
    def emit_jg (self, label, comment=""): self.writer.emit_jg (label)
    def emit_jge(self, label, comment=""): self.writer.emit_jge(label)

    def emit_call_lbl(self, target, comment=""):
        # internes Label: normaler rel32-call, KEIN Runtime-/Import-call
        if target in self.coff.labels:
            self.writer.emit_call_label(target)
            return
        
        # noch nicht gebundenes internes Label
        if target.startswith("class_") or target.startswith("proc_") or target.startswith("func_"):
            self.writer.emit_call_label(target)
            return
        
        # echte Runtime/Import-Funktion
        self.writer.emit_runtime_call(target)
    
    def emit_call(self, target, comment=""):
        if target == "rax" and self.pending_call_symbol:
            name = self.pending_call_symbol
            self.pending_call_symbol = None
            self.writer.emit_runtime_call(name)
            return
            
        self.writer.emit_call(target)

    def emit_call_reg(self, target, comment=""):
        self.writer.emit_call_reg(target)

    def emit_movzx(self, dst, src, comment=""):
        self.writer.emit_movzx(dst, src)

    def emit_movsxd(self, dst, src, comment=""):
        self.writer.emit_movsxd_r64_r32(dst, src)

    def emit_xor(self, dst, src, comment=""):
        self.writer.emit_xor_r32_r32(dst, src)

    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        # Win64-Visitor ruft qword auf.
        # NT32 speichert Pointer aber als dword.
        self.writer.emit_mov_mem_reg32(
            self.map_reg32(base),
            int(offset),
            self.map_reg32(src)
        )

    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_reg32(
            self.map_reg32(base),
            int(offset),
            self.map_reg32(src)
        )
