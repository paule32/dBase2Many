# ---------------------------------------------------------------------------
# File: asmjit.py - backend for AsmJIT
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.backend.code     import *

# ---------------------------------------------------------------------------
# AsmJit backend ...
# ---------------------------------------------------------------------------
class AsmJitBackend(CodeBackend):
    def __init__(self, name="asmjit"):
        super().__init__(name)

    def make_comment(self, comment):
        return f"  // {comment}" if comment else ""

    def emit_new_label_decl(self, name, comment=""):
        self.emit(
            f"Label {name} = a.new_label();{self.make_comment(comment)}"
        )
    
    def collect_array_suffix_exprs(self, suffixes):
        index_exprs = []
        rest_suffixes = []

        in_array_part = True

        for s in suffixes:
            if in_array_part and s.LBRACK():
                index_exprs.extend(list(s.expr()))
                continue

            in_array_part = False
            rest_suffixes.append(s)

        return index_exprs, rest_suffixes
    
    def _imm(self, value):
        s = str(value)
        if s.startswith("imm("):
            return s
        if s.startswith("&"):
            return f"imm((uint64_t){s})"
        if s.startswith("_") or s.startswith("str_") or s.startswith("dbl_"):
            return f"imm((uint64_t)&{s})"
        return s

    def _operand(self, value):
        if isinstance(value, str) and value.isidentifier():
            return f"x86::{value}"
        return str(value)

    def emit_add(self, reg, value, comment=""):
        self.emit(f"a.add(x86::{reg}, {self._operand(value)});{self.make_comment(comment)}")

    def emit_imul(self, dst, src, value=None, comment=""):
        if value is None:
            self.emit(f"a.imul(x86::{dst}, {self._operand(src)});{self.make_comment(comment)}")
        else:
            self.emit(f"a.imul(x86::{dst}, {self._operand(src)}, {value});{self.make_comment(comment)}")

    def emit_cmp(self, dst, value, comment=""):
        if isinstance(value, str) and value.isidentifier():
            self.emit(f"a.cmp(x86::{dst}, x86::{value});{self.make_comment(comment)}")
        else:
            self.emit(f"a.cmp(x86::{dst}, {value});{self.make_comment(comment)}")
    def emit_cmp_dword(self, dst, base, field, comment=""):
        self.emit(f"a.cmp(x86::{dst}, x86::dword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")

    def emit_jl(self, label, comment=""): self.emit(f"a.jl({label});{self.make_comment(comment)}")
    def emit_jg(self, label, comment=""): self.emit(f"a.jg({label});{self.make_comment(comment)}")
    def emit_jz(self, label, comment=""): self.emit(f"a.jz({label});{self.make_comment(comment)}")
    def emit_jb(self, label, comment=""): self.emit(f"a.jb({label});{self.make_comment(comment)}")
    def emit_ja(self, label, comment=""): self.emit(f"a.ja({label});{self.make_comment(comment)}")
    def emit_jae(self, label, comment=""): self.emit(f"a.jae({label});{self.make_comment(comment)}")
    def emit_jbe(self, label, comment=""): self.emit(f"a.jbe({label});{self.make_comment(comment)}")
    def emit_je(self, label, comment=""): self.emit(f"a.je({label});{self.make_comment(comment)}")
    def emit_jle(self, label, comment=""): self.emit(f"a.jle({label});{self.make_comment(comment)}")
    def emit_jge(self, label, comment=""): self.emit(f"a.jge({label});{self.make_comment(comment)}")
    def emit_jne(self, label, comment=""): self.emit(f"a.jne({label});{self.make_comment(comment)}")
    def emit_jnz(self, label, comment=""): self.emit(f"a.jnz({label});{self.make_comment(comment)}")
    def emit_jmp(self, label, comment=""): self.emit(f"a.jmp({label});{self.make_comment(comment)}")

    def emit_lea_byte(self, dst, base, offset, comment=""):
        self.emit(f"a.lea(x86::{dst}, x86::byte_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_lea_dword(self, dst, base, offset, comment=""):
        self.emit(f"a.lea(x86::{dst}, x86::dword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_lea_qword(self, dst, base, offset, comment=""):
        self.emit(f"a.lea(x86::{dst}, x86::qword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")

    def emit_mov_byte(self, dst, base, field, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::byte_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")
    def emit_mov_dword(self, dst, base, field, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::dword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")
    def emit_mov_qword(self, dst, base, field, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::qword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::byte_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::dword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::qword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"a.mov(x86::qword_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"a.mov(x86::dword_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"a.mov(x86::byte_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")

    def emit_mov_reg_byte(self, dst, base, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::byte_ptr(x86::{base}));{self.make_comment(comment)}")
    def emit_mov_reg_dword(self, dst, base, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::dword_ptr(x86::{base}));{self.make_comment(comment)}")
    def emit_mov_reg_qword(self, dst, base, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::qword_ptr(x86::{base}));{self.make_comment(comment)}")

    def emit_mov_imm(self, dst, value, comment=""):
        self.emit(f"a.mov(x86::{dst}, {self._imm(value)});{self.make_comment(comment)}")

    def emit_mov(self, dst, src, comment=""):
        if isinstance(src, int) or (isinstance(src, str) and (src.lstrip('-').isdigit() or src.startswith('&') or src.startswith('imm('))):
            self.emit_mov_imm(dst, src, comment)
        else:
            self.emit(f"a.mov(x86::{dst}, x86::{src});{self.make_comment(comment)}")

    def emit_movzx(self, dst, src, comment=""):
        s = str(src)
        if s.startswith ("byte_ptr(") and s.endswith(")"):
            base = s[len("byte_ptr("):-1]
            self.emit(f"a.movzx(x86::{dst}, x86::byte_ptr(x86::{base}));{self.make_comment(comment)}")
        else:
            self.emit(f"a.movzx(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movsxd(self, dst, src, comment=""):
        self.emit(f"a.movsxd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movq(self, dst, src, comment=""):
        self.emit(f"a.movq(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movsd_load(self, dst, base, offset=0, comment=""):
        self.emit(f"a.movsd(x86::{dst}, x86::qword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_movsd_load_field(self, dst, base, field, comment=""):
        self.emit(f"a.movsd(x86::{dst}, x86::qword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")
    def emit_movsd_store(self, base, offset, src, comment=""):
        self.emit(f"a.movsd(x86::qword_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")
    def emit_ucomisd(self, dst, src, comment=""):
        self.emit(f"a.ucomisd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_cvtsi2sd(self, dst, src, comment=""):
        self.emit(f"a.cvtsi2sd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movapd(self, dst, src, comment=""):
        self.emit(f"a.movapd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_addsd(self, dst, src, comment=""):
        self.emit(f"a.addsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_subsd(self, dst, src, comment=""):
        self.emit(f"a.subsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_mulsd(self, dst, src, comment=""):
        self.emit(f"a.mulsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_divsd(self, dst, src, comment=""):
        self.emit(f"a.divsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_cdq(self, comment=""):
        self.emit(f"a.cdq();{self.make_comment(comment)}")
    def emit_idiv(self, reg, comment=""):
        self.emit(f"a.idiv(x86::{reg});{self.make_comment(comment)}")

    def emit_xor(self, dst, src, comment=""):
        self.emit(f"a.xor_(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_push(self, reg, comment=""):
        self.emit(f"a.push(x86::{reg});{self.make_comment(comment)}")
    def emit_pop(self, reg, comment=""):
        self.emit(f"a.pop(x86::{reg});{self.make_comment(comment)}")
    def emit_sub(self, reg, value, comment=""):
        self.emit(f"a.sub(x86::{reg}, {value});{self.make_comment(comment)}")
    def emit_setne(self, reg, comment=""):
        self.emit(f"a.setne(x86::{reg});{self.make_comment(comment)}")
    def emit_test(self, reg1, reg2, comment=""):
        self.emit(f"a.test(x86::{reg1}, x86::{reg2});{self.make_comment(comment)}")

    def emit_call(self, target, comment=""):
        self.emit_sub("rsp", 32, comment="Windows x64 shadow space")
        self.emit(f"a.call(x86::{target});{self.make_comment(comment)}")
        self.emit_add("rsp", 32)
    def emit_call_reg(self, target, comment=""):
        self.emit_call(target, comment)
    def emit_call_lbl(self, target, comment=""):
        self.emit_sub("rsp", 32, comment="Windows x64 shadow space")
        self.emit(f"a.call({target});{self.make_comment(comment)}")
        self.emit_add("rsp", 32)
    def emit_ret(self, comment=""):
        self.emit(f"a.ret();{self.make_comment(comment)}")
    def emit_bind_label(self, label, comment=""):
        self.emit(f"a.bind({label});{self.make_comment(comment)}")
