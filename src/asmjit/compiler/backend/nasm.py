# ---------------------------------------------------------------------------
# File: nasm.py - backend for AsmJIT
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.backend.code     import *

# ---------------------------------------------------------------------------
# NASM backend ...
# ---------------------------------------------------------------------------
class NasmBackend(CodeBackend):
    def __init__(self, name: str = "nasm"):
        super().__init__(name)

    def make_comment(self, comment):
        return f"  ; {comment}" if comment else ""

    def emit_new_label_decl(self, name, comment=""):
        # NASM braucht keine vorherige Label-Deklaration
        return
    
    def _mem(self, base, offset=0):
        if offset in (None, "", 0, "0"):
            return f"[{base}]"
        off = str(offset)
        if off.startswith("-"):
            return f"[{base} - {off[1:]}]"
        return f"[{base} + {off}]"

    def _symbol(self, value):
        s = str(value)
        if s.startswith("&"):
            return s[1:]
        if s.startswith ("imm((uint64_t)&") and s.endswith(")"):
            return s[len("imm((uint64_t)&"):-1]
        return s

    def emit_add(self, reg, value, comment=""):
        self.emit(f"add {reg}, {value}{self.make_comment(comment)}")
    def emit_imul(self, dst, src, value=None, comment=""):
        if value is None:
            self.emit(f"imul {dst}, {src}{self.make_comment(comment)}")
        else:
            self.emit(f"imul {dst}, {src}, {value}{self.make_comment(comment)}")
    def emit_cmp(self, dst, value, comment=""):
        self.emit(f"cmp {dst}, {value}{self.make_comment(comment)}")
    def emit_cmp_dword(self, dst, base, field, comment=""):
        self.emit(f"cmp {dst}, dword [{base} + JitContext.{field}]{self.make_comment(comment)}")

    def emit_jl (self, label, comment=""): self.emit(f"jl  {label}{self.make_comment(comment)}")
    def emit_jg (self, label, comment=""): self.emit(f"jg  {label}{self.make_comment(comment)}")
    def emit_jz (self, label, comment=""): self.emit(f"jz  {label}{self.make_comment(comment)}")
    def emit_jb (self, label, comment=""): self.emit(f"jb  {label}{self.make_comment(comment)}")
    def emit_ja (self, label, comment=""): self.emit(f"ja  {label}{self.make_comment(comment)}")
    def emit_jae(self, label, comment=""): self.emit(f"jae {label}{self.make_comment(comment)}")
    def emit_jbe(self, label, comment=""): self.emit(f"jbe {label}{self.make_comment(comment)}")
    def emit_je (self, label, comment=""): self.emit(f"je  {label}{self.make_comment(comment)}")
    def emit_jle(self, label, comment=""): self.emit(f"jle {label}{self.make_comment(comment)}")
    def emit_jge(self, label, comment=""): self.emit(f"jge {label}{self.make_comment(comment)}")
    def emit_jne(self, label, comment=""): self.emit(f"jne {label}{self.make_comment(comment)}")
    def emit_jnz(self, label, comment=""): self.emit(f"jnz {label}{self.make_comment(comment)}")
    def emit_jmp(self, label, comment=""): self.emit(f"jmp {label}{self.make_comment(comment)}")

    def emit_lea_byte(self, dst, base, offset, comment=""):
        self.emit(f"lea {dst}, {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_lea_dword(self, dst, base, offset, comment=""):
        self.emit(f"lea {dst}, {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_lea_qword(self, dst, base, offset, comment=""):
        self.emit(f"lea {dst}, {self._mem(base, offset)}{self.make_comment(comment)}")

    def emit_mov_byte(self, dst, base, field, comment=""):
        self.emit(f"mov {dst}, byte [{base} + JitContext.{field}]{self.make_comment(comment)}")
    def emit_mov_dword(self, dst, base, field, comment=""):
        self.emit(f"mov {dst}, dword [{base} + JitContext.{field}]{self.make_comment(comment)}")
    def emit_mov_qword(self, dst, base, field, comment=""):
        self.emit(f"mov {dst}, qword [{base} + JitContext.{field}]{self.make_comment(comment)}")

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"mov {dst}, byte {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"mov {dst}, dword {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"mov {dst}, qword {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"mov qword {self._mem(base, offset)}, {src}{self.make_comment(comment)}")
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"mov dword {self._mem(base, offset)}, {src}{self.make_comment(comment)}")
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"mov byte {self._mem(base, offset)}, {src}{self.make_comment(comment)}")

    def emit_mov_reg_byte(self, dst, base, comment=""):
        self.emit(f"mov {dst}, byte [{base}]{self.make_comment(comment)}")
    def emit_mov_reg_dword(self, dst, base, comment=""):
        self.emit(f"mov {dst}, dword [{base}]{self.make_comment(comment)}")
    def emit_mov_reg_qword(self, dst, base, comment=""):
        self.emit(f"mov {dst}, qword [{base}]{self.make_comment(comment)}")

    def emit_mov(self, dst, src, comment=""):
        self.emit(f"mov {dst}, {src}{self.make_comment(comment)}")
    def emit_mov_imm(self, dst, value, comment=""):
        self.emit(f"mov {dst}, {self._symbol(value)}{self.make_comment(comment)}")
    def emit_movzx(self, dst, src, comment=""):
        s = str(src)
        if s.startswith ("byte_ptr(") and s.endswith(")"):
            base = s[len("byte_ptr("):-1]
            self.emit(f"movzx {dst}, byte [{base}]{self.make_comment(comment)}")
        else:
            self.emit(f"movzx {dst}, {src}{self.make_comment(comment)}")
    def emit_movsxd(self, dst, src, comment=""):
        self.emit(f"movsxd {dst}, {src}{self.make_comment(comment)}")
    def emit_movq(self, dst, src, comment=""):
        self.emit(f"movq {dst}, {src}{self.make_comment(comment)}")
    def emit_movsd_load(self, dst, base, offset=0, comment=""):
        self.emit(f"movsd {dst}, qword {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_movsd_load_field(self, dst, base, field, comment=""):
        self.emit(f"movsd {dst}, qword [{base} + JitContext.{field}]{self.make_comment(comment)}")
    def emit_movsd_store(self, base, offset, src, comment=""):
        self.emit(f"movsd qword {self._mem(base, offset)}, {src}{self.make_comment(comment)}")
    def emit_ucomisd(self, dst, src, comment=""):
        self.emit(f"ucomisd {dst}, {src}{self.make_comment(comment)}")
    def emit_cvtsi2sd(self, dst, src, comment=""):
        self.emit(f"cvtsi2sd {dst}, {src}{self.make_comment(comment)}")
    def emit_movapd(self, dst, src, comment=""):
        self.emit(f"movapd {dst}, {src}{self.make_comment(comment)}")
    def emit_addsd(self, dst, src, comment=""):
        self.emit(f"addsd {dst}, {src}{self.make_comment(comment)}")
    def emit_subsd(self, dst, src, comment=""):
        self.emit(f"subsd {dst}, {src}{self.make_comment(comment)}")
    def emit_mulsd(self, dst, src, comment=""):
        self.emit(f"mulsd {dst}, {src}{self.make_comment(comment)}")
    def emit_divsd(self, dst, src, comment=""):
        self.emit(f"divsd {dst}, {src}{self.make_comment(comment)}")
    def emit_cdq(self, comment=""):
        self.emit(f"cdq{self.make_comment(comment)}")
    def emit_idiv(self, reg, comment=""):
        self.emit(f"idiv {reg}{self.make_comment(comment)}")

    def emit_xor(self, dst, src, comment=""):
        self.emit(f"xor {dst}, {src}{self.make_comment(comment)}")
    def emit_push(self, reg, comment=""):
        self.emit(f"push {reg}{self.make_comment(comment)}")
    def emit_pop(self, reg, comment=""):
        self.emit(f"pop {reg}{self.make_comment(comment)}")
    def emit_sub(self, reg, value, comment=""):
        self.emit(f"sub {reg}, {value}{self.make_comment(comment)}")
    def emit_setne(self, reg, comment=""):
        self.emit(f"setne {reg}{self.make_comment(comment)}")
    def emit_test(self, reg1, reg2, comment=""):
        self.emit(f"test {reg1}, {reg2}{self.make_comment(comment)}")

    def emit_call(self, target, comment=""):
        self.emit_sub("rsp", 32, comment="Windows x64 shadow space")
        self.emit(f"call {target}{self.make_comment(comment)}")
        self.emit_add("rsp", 32)
    def emit_call_reg(self, target, comment=""):
        self.emit_call(target, comment)
    def emit_call_lbl(self, target, comment=""):
        self.emit_call(target, comment)
    def emit_ret(self, comment=""):
        self.emit(f"ret{self.make_comment(comment)}")
    def emit_bind_label(self, label, comment=""):
        self.lines.append(f"{label}:{self.make_comment(comment)}")
