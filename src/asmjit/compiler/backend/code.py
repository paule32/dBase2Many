# ---------------------------------------------------------------------------
# File: code.py - backend abstraction
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.common.types     import *

class CodeBackend:
    def __init__(self, name: str = "asmjit"):
        self.lines = []
        self.name = name
        CDATA.BackEnd.current = name
    
    def emit(self, line):
        self.lines.append("    " + line)
    
    def get_lines(self):
        return self.lines
    
    def emit_new_label_decl(self, name, comment=""): raise NotImplementedError
    
    def emit_mov_byte_ptr_store(
        self,
        base,
        offset,
        src,
        comment=""
    ):
        raise NotImplementedError
    
    def emit_mov_word_ptr_store(
        self,
        base,
        offset,
        src,
        comment=""
    ):
        raise NotImplementedError
    
    def emit_add(self, reg, value, comment=""): raise NotImplementedError
    def emit_imul(self, dst, src, value=None, comment=""): raise NotImplementedError
    def emit_cmp(self, dst, value, comment=""): raise NotImplementedError
    def emit_cmp_dword(self, dst, base, field, comment=""): raise NotImplementedError

    def emit_jl(self, label, comment=""): raise NotImplementedError
    def emut_jl(self, label, comment=""): return self.emit_jl(label, comment)
    def emit_jg(self, label, comment=""): raise NotImplementedError
    def emit_jz(self, label, comment=""): raise NotImplementedError
    def emit_jb(self, label, comment=""): raise NotImplementedError
    def emit_ja(self, label, comment=""): raise NotImplementedError
    def emit_jae(self, label, comment=""): raise NotImplementedError
    def emit_jbe(self, label, comment=""): raise NotImplementedError
    def emit_je(self, label, comment=""): raise NotImplementedError
    def emit_jle(self, label, comment=""): raise NotImplementedError
    def emit_jge(self, label, comment=""): raise NotImplementedError
    def emit_jne(self, label, comment=""): raise NotImplementedError
    def emit_jnz(self, label, comment=""): raise NotImplementedError
    def emit_jmp(self, label, comment=""): raise NotImplementedError

    def emit_lea_byte(self, dst, base, offset, comment=""): raise NotImplementedError
    def emit_lea_dword(self, dst, base, offset, comment=""): raise NotImplementedError
    def emit_lea_qword(self, dst, base, offset, comment=""): raise NotImplementedError

    def emit_mov_byte(self, dst, base, field, comment=""): raise NotImplementedError
    def emit_mov_dword(self, dst, base, field, comment=""): raise NotImplementedError
    def emit_mov_qword(self, dst, base, field, comment=""): raise NotImplementedError

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""): raise NotImplementedError
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""): raise NotImplementedError

    def emit_mov_reg_byte(self, dst, base, comment=""): raise NotImplementedError
    def emit_mov_reg_dword(self, dst, base, comment=""): raise NotImplementedError
    def emit_mov_reg_qword(self, dst, base, comment=""): raise NotImplementedError

    def emit_mov_imm(self, dst, value, comment=""): raise NotImplementedError
    def emit_mov(self, dst, src, comment=""): raise NotImplementedError
    def emit_movzx(self, dst, src, comment=""): raise NotImplementedError
    def emit_movsxd(self, dst, src, comment=""): raise NotImplementedError
    def emit_movq(self, dst, src, comment=""): raise NotImplementedError
    def emit_movsd_load(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_movsd_load_field(self, dst, base, field, comment=""): raise NotImplementedError
    def emit_movsd_store(self, base, offset, src, comment=""): raise NotImplementedError
    def emit_ucomisd(self, dst, src, comment=""): raise NotImplementedError
    def emit_cvtsi2sd(self, dst, src, comment=""): raise NotImplementedError
    def emit_movapd(self, dst, src, comment=""): raise NotImplementedError
    def emit_addsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_subsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_mulsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_divsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_cdq(self, comment=""): raise NotImplementedError
    def emit_idiv(self, reg, comment=""): raise NotImplementedError

    def emit_xor(self, dst, src, comment=""): raise NotImplementedError
    def emit_push(self, reg, comment=""): raise NotImplementedError
    def emit_pop(self, reg, comment=""): raise NotImplementedError
    def emit_sub(self, reg, value, comment=""): raise NotImplementedError
    def emit_setne(self, reg, comment=""): raise NotImplementedError
    def emit_test(self, reg1, reg2, comment=""): raise NotImplementedError

    def emit_call(self, target, comment=""): raise NotImplementedError
    def emit_call_reg(self, target, comment=""): return self.emit_call(target, comment)
    def emit_call_lbl(self, target, comment=""): raise NotImplementedError
    def emit_ret(self, comment=""): raise NotImplementedError
    def emit_bind_label(self, label, comment=""): raise NotImplementedError
