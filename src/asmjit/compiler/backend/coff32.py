# ---------------------------------------------------------------------------
# File: coff32.py - backend for coff32
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.common.locale    import *
from compiler.backend.code     import *

# ---------------------------------------------------------------------------
# Windows 32-Bit PE coff backend ...
# ---------------------------------------------------------------------------
class Coff32Backend(CodeBackend):
    def __init__(self, writer):
        super().__init__("nt32")
        self.writer = writer
        self.pending_call_symbol = None
        
        self.JIT_CONTEXT_OFFSETS32 = {
            "int_vars": 0,
            "double_vars": 4,
            "string_vars": 8,
            "record_vars": 12,
            "arrays_vars": 16,
            "pointr_vars": 20,
            "print_int_tmp": 24,
            "print_double_tmp": 28,
        }
        self.asm_lines = []

    def emit_shift_left (self, dst, count, comment=""): self.emit(f"shl {dst}, {count}")
    def emit_shift_right(self, dst, count, comment=""): self.emit(f"shr {dst}, {count}")

    def emit_jb(self, label, comment=""):
        self.asm_lines.append(f"jb {label}")
        self.writer.emit_jb(label)

    def emit_jbe(self, label, comment=""):
        self.asm_lines.append(f"jbe {label}")
        self.writer.emit_jbe(label)

    def emit_ja(self, label, comment=""):
        self.asm_lines.append(f"ja {label}")
        self.writer.emit_ja(label)

    def emit_jae(self, label, comment=""):
        self.asm_lines.append(f"jae {label}")
        self.writer.emit_jae(label)
    
    def emit_ucomisd(self, left, right, comment=""):
        self.writer.emit_ucomisd32(left, right)
    
    def emit_movapd(self, dst, src, comment=""):
        self.writer.emit_movapd32(dst, src)
    
    def emit_addsd(self, dst, src, comment=""):
        self.writer.emit_addsd32(dst, src)

    def emit_subsd(self, dst, src, comment=""):
        self.writer.emit_subsd32(dst, src)

    def emit_mulsd(self, dst, src, comment=""):
        self.writer.emit_mulsd32(dst, src)

    def emit_divsd(self, dst, src, comment=""):
        self.writer.emit_divsd32(dst, src)

    def pointer_slot_size(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            return 4
        return 8
    
    def _format_memory_operand(
        self,
        base,
        offset
    ):
        if offset == 0:
            return f"[{base}]"

        if offset > 0:
            return f"[{base}+{offset}]"

        return f"[{base}{offset}]"

    def emit_lea_dword(
        self,
        dst,
        base,
        offset,
        comment=""
    ):
        dst = self.map_reg32(
            dst
        )

        base = self.map_reg32(
            base
        )

        operand = self._format_memory_operand(
            base,
            int(offset)
        )

        line = f"lea {dst}, {operand}"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(
            line
        )

        self.writer.emit_lea_reg_mem32(
            dst,
            base,
            int(offset)
        )

    def emit_lea_byte(
        self,
        dst,
        base,
        offset,
        comment=""
    ):
        # LEA berechnet ausschließlich eine Adresse.
        # Die Größe des adressierten Objekts ist dabei egal.
        return self.emit_lea_dword(
            dst,
            base,
            offset,
            comment
        )

    def emit_lea_qword(
        self,
        dst,
        base,
        offset,
        comment=""
    ):
        # Unter NT32 sind auch Adressen von QWord-Objekten 32 Bit breit.
        return self.emit_lea_dword(
            dst,
            base,
            offset,
            comment
        )
    
    def emit_shl_reg_cl(
        self,
        reg,
        comment=""
    ):
        reg32 = self.map_reg32(
            reg
        )

        line = f"shl {reg32}, cl"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(
            line
        )

        self.writer.emit_shl_reg_cl(
            reg32
        )


    def emit_shr_reg_cl(
        self,
        reg,
        comment=""
    ):
        reg32 = self.map_reg32(
            reg
        )

        line = f"shr {reg32}, cl"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(
            line
        )

        self.writer.emit_shr_reg_cl(
            reg32
        )
    
    def emit_mov_byte_ptr_store(
        self,
        base,
        offset,
        src,
        comment=""
    ):
        base32 = self.map_reg32(
            base
        )

        src8 = self.map_reg8(
            src
        )

        off = self.resolve_offset32(
            offset
        )

        if off == 0:
            line = (
                f"mov byte [{base32}], "
                f"{src8}"
            )

        elif off > 0:
            line = (
                f"mov byte [{base32}+{off}], "
                f"{src8}"
            )

        else:
            line = (
                f"mov byte [{base32}{off}], "
                f"{src8}"
            )

        if comment:
            line += (
                f" ; {comment}"
            )

        self.asm_lines.append(
            line
        )

        self.writer.emit_mov_byte_ptr_reg8(
            base32,
            off,
            src8
        )

    def emit_mov_word_ptr_store(
        self,
        base,
        offset,
        src,
        comment=""
    ):
        base32 = self.map_reg32(
            base
        )

        src16 = self.map_reg16(
            src
        )

        off = self.resolve_offset32(
            offset
        )

        if off == 0:
            line = (
                f"mov word [{base32}], "
                f"{src16}"
            )

        elif off > 0:
            line = (
                f"mov word [{base32}+{off}], "
                f"{src16}"
            )

        else:
            line = (
                f"mov word [{base32}{off}], "
                f"{src16}"
            )

        if comment:
            line += (
                f" ; {comment}"
            )

        self.asm_lines.append(
            line
        )

        self.writer.emit_mov_word_ptr_reg16(
            base32,
            off,
            src16
        )
    
    def emit_seta(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"seta {reg}")
        self.writer.emit_seta(reg)

    def emit_setae(self, reg, comment=""):
        reg = self.map_reg8(reg)

        self.asm_lines.append(f"setae {reg}")
        self.writer.emit_setae(reg)

    def emit_setb(self, reg, comment=""):
        reg = self.map_reg8(reg)

        self.asm_lines.append(f"setb {reg}")
        self.writer.emit_setb(reg)

    def emit_setbe(self, reg, comment=""):
        reg = self.map_reg8(reg)

        self.asm_lines.append(f"setbe {reg}")
        self.writer.emit_setbe(reg)
        
    def emit_new_label_decl(self, name, comment=""):
        # PE32/COFF braucht keine vorherige Label-Deklaration
        return

    def emit_bind_label(self, label, comment=""):
        self.writer.bind_label(label)

    def emit_ret(self, comment=""):
        self.asm_lines.append(f"ret")
        self.writer.emit_ret()

    def emit_call_lbl(self, label, comment=""):
        if label in ["rax", "eax"]:
            self.asm_lines.append(f"call {label}")
            self.writer.emit_call_reg32("eax")
            return

        if label in ["rbx", "ebx"]:
            self.asm_lines.append("call ebx")
            self.writer.emit_call_reg32("ebx")
            return

        if label in ["rcx", "ecx"]:
            self.asm_lines.append("call ecx")
            self.writer.emit_call_reg32("ecx")
            return

        if label in ["rdx", "edx"]:
            self.asm_lines.append("call edx")
            self.writer.emit_call_reg32("edx")
            return
        
        self.asm_lines.append(f"call {label}")
        self.writer.emit_call_label(label)

    def emit_call(self, target, comment=""):
        if target in ["rax", "eax"] and self.pending_call_symbol:
            name = self.pending_call_symbol
            self.pending_call_symbol = None
            
            self.asm_lines.append(f"call {name}")
            self.writer.emit_call_external(name)
            return

        if target in ["rax", "eax"]:
            self.asm_lines.append(f"call eax")
            self.writer.emit_call_reg32("eax")
            return
        
        if target in ["rbx", "ebx"]:
            self.asm_lines.append(f"call ebx")
            self.writer.emit_call_reg32("ebx")
            return

        if target in ["rcx", "ecx"]:
            self.asm_lines.append(f"call ecx")
            self.writer.emit_call_reg32("ecx")
            return

        if target in ["rdx", "edx"]:
            self.asm_lines.append(f"call edx")
            self.writer.emit_call_reg32("edx")
            return
        
        self.asm_lines.append(f"call {target}")
        self.writer.emit_call_external(target)

    def emit_dec(self, reg, comment=""):
        reg = self.map_reg32(reg)

        line = f"dec {reg}"
        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(line)
        self.emit(line)
        
    def emit_jmp(self, label, comment=""):
        self.asm_lines.append(f"jmp {label}")
        self.writer.emit_jmp(label)

    def emit_je(self, label, comment=""):
        self.asm_lines.append(f"je {label}")
        self.writer.emit_je(label)

    def emit_jne(self, label, comment=""):
        self.asm_lines.append(f"jne {label}")
        self.writer.emit_jne(label)

    def emit_jz(self, label, comment=""):
        self.asm_lines.append(f"je {label}")
        self.writer.emit_je(label)

    def emit_jnz(self, label, comment=""):
        self.asm_lines.append(f"jne {label}")
        self.writer.emit_jne(label)

    def emit_jl(self, label, comment=""):
        self.asm_lines.append(f"jl {label}")
        self.writer.emit_jl(label)

    def emit_jle(self, label, comment=""):
        self.asm_lines.append(f"jle {label}")
        self.writer.emit_jle(label)

    def emit_jg(self, label, comment=""):
        self.asm_lines.append(f"jg {label}")
        self.writer.emit_jg(label)

    def emit_jge(self, label, comment=""):
        self.asm_lines.append(f"jge {label}")
        self.writer.emit_jge(label)

    def emit_jmp(self, label, comment=""):
        self.asm_lines.append(f"jmp {label}")
        self.writer.emit_jmp(label)

    def map_reg16(
        self,
        reg
    ):
        reg_map = {
            "ax": "ax",
            "cx": "cx",
            "dx": "dx",
            "bx": "bx",
            "sp": "sp",
            "bp": "bp",
            "si": "si",
            "di": "di",

            # Bequeme Abbildung von 32/64 Bit auf 16 Bit
            "eax": "ax",
            "ecx": "cx",
            "edx": "dx",
            "ebx": "bx",
            "esp": "sp",
            "ebp": "bp",
            "esi": "si",
            "edi": "di",

            "rax": "ax",
            "rcx": "cx",
            "rdx": "dx",
            "rbx": "bx",
            "rsp": "sp",
            "rbp": "bp",
            "rsi": "si",
            "rdi": "di",
        }

        if reg not in reg_map:
            raise RuntimeError(
                f"unsupported NT32 16-bit register: {reg}"
            )

        return reg_map[
            reg
        ]

    def map_reg32(self, reg):
        reg_map = {
            "rax" : "eax", "eax": "eax",
            "rbx" : "ebx", "ebx": "ebx",
            "rcx" : "ecx", "ecx": "ecx",
            "rdx" : "edx", "edx": "edx",
            "rbp" : "ebp", "ebp": "ebp",
            "rsp" : "esp", "esp": "esp",
            "rsi" : "esi", "esi": "esi",
            "rdi" : "edi", "edi": "edi",
            
            "r8"  : "ecx",
            "r8d" : "ecx",
            "r9"  : "edx",
            "r9d" : "edx",

            "r10" : "edi",
            "r10d": "edi",
            "r11" : "ebx",
            "r11d": "ebx",
            
            "r12" : "esi",
        }
        
        if reg not in reg_map:
            raise RuntimeError(f"{tr('unsupported NT32 register')}: {reg}")
        
        return reg_map[reg]
    
    def map_xmm(self, reg):
        reg = reg.lower()

        mapping = {
            "xmm0": "xmm0",
            "xmm1": "xmm1",
            "xmm2": "xmm2",
            "xmm3": "xmm3",
            "xmm4": "xmm4",
            "xmm5": "xmm5",
            "xmm6": "xmm6",
            "xmm7": "xmm7",
        }

        if reg not in mapping:
            raise ValueError(f"Unknown XMM register: {reg}")

        return mapping[reg]

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""):
        dst = self.map_reg8(dst)
        base = self.map_reg32(base)

        if offset == 0:
            line = f"mov {dst}, byte ptr [{base}]"
        elif offset > 0:
            line = f"mov {dst}, byte ptr [{base}+{offset}]"
        else:
            line = f"mov {dst}, byte ptr [{base}{offset}]"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(line)
        self.emit(line)

    def emit_push(self, reg, comment=""):
        self.asm_lines.append(f"push {reg}")
        self.writer.emit_push_reg32(self.map_reg32(reg))

    def emit_pop(self, reg, comment=""):
        self.asm_lines.append(f"pop {reg}")
        self.writer.emit_pop_reg32(self.map_reg32(reg))
        
    def emit_mov(self, dst, src, comment=""):
        dst32 = self.map_reg32(dst)

        if isinstance(src, int):
            self.asm_lines.append(f"mov {dst32}, {src}")
            self.writer.emit_mov_reg_imm32(dst32, src)
            return

        if isinstance(src, str):
            if src.lstrip("-").isdigit():
                self.asm_lines.append(f"mov {dst32}, {inc(src)}")
                self.writer.emit_mov_reg_imm32(dst32, int(src))
                return

            if src.startswith("str_"):
                self.asm_lines.append(f"mov {dst32}, {src}")
                self.writer.emit_mov_reg_data_label32(dst32, src)   # Adresse
                return

            if src.startswith("_var_"):
                self.asm_lines.append(f"mov {dst32}, {src}")
                self.writer.emit_mov_reg_from_data_label32(dst32, src)  # Inhalt
                return

        self.asm_lines.append(f"mov {dst32}, {self.map_reg32(src)}")
        self.writer.emit_mov_reg_reg32(
            dst32,
            self.map_reg32(src)
        )

    def emit_sub(self, reg, value, comment=""):
        reg32 = self.map_reg32(reg)

        if isinstance(value, int):
            self.asm_lines.append(f"sub {reg32}, {value}")
            self.writer.emit_sub_reg_imm32(reg32, value)
            return

        if isinstance(value, str):
            if value.lstrip("-").isdigit():
                self.asm_lines.append(f"sub {reg32}, {inc(value)}")
                self.writer.emit_sub_reg_imm32(reg32, int(value))
                return

            self.asm_lines.append(f"sub {reg32}, {self.map_reg32(value)}")
            self.writer.emit_sub_reg_reg32(
                reg32,
                self.map_reg32(value)
            )
            return

        raise RuntimeError(f"unsupported NT32 sub value: {value}")

    def emit_add(self, reg, value, comment=""):
        reg32 = self.map_reg32(reg)

        if isinstance(value, int):
            self.asm_lines.append(f"add {reg32}, {value}")
            self.writer.emit_add_reg_imm32(reg32, value)
            return

        if isinstance(value, str):
            if value.lstrip("-").isdigit():
                self.asm_lines.append(f"add {reg32}, {inc(value)}")
                self.writer.emit_add_reg_imm32(reg32, int(value))
                return

            self.asm_lines.append(f"add {reg32}, {self.map_reg32(value)}")
            self.writer.emit_add_reg_reg32(
                reg32,
                self.map_reg32(value)
            )
            return

        raise RuntimeError(f"{tr('unsupported NT32 add value')}: {value}")
        
    def emit_mov_imm(self, dst, value, comment=""):
        dst32 = self.map_reg32(dst)

        if isinstance(value, str):
            # String-/Datenlabel
            if value.startswith("str_"):
                self.asm_lines.append(f"mov {dst32}, {value}")
                self.writer.emit_mov_reg_data_label32(dst32, value)         # Adresse
                return
            
            if value.startswith("_var_"):
                self.asm_lines.append(f"mov {dst32}, {value}")
                self.writer.emit_mov_reg_from_data_label32(dst32, value)     # Inhalt
                return

            # &Runtime / &API
            if value.startswith("&"):
                self.asm_lines.append(f"call &{value[1:]}")
                self.pending_call_symbol = value[1:]
                return

            if value.lstrip("-").isdigit():
                value = int(value)

        self.asm_lines.append(f"mov {dst32}, {value}")
        self.writer.emit_mov_reg_imm32(dst32, value)
        
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        base = self.map_reg32(base)
        src  = self.map_reg32(src)
        off  = self.resolve_offset32(offset)

        if off == 0:
            self.asm_lines.append(f"mov dword [{base}], {src}")
        elif off > 0:
            self.asm_lines.append(f"mov dword [{base}+{off}], {src}")
        else:
            self.asm_lines.append(f"mov dword [{base}{off}], {src}")
            
        self.writer.emit_mov_mem_reg32(base, off, src)

    def emit_movsd_load_field(self, dst, base, field, comment=""):
        self.asm_lines.append(f"movsd {dst}, qword [{self.map_reg32(base)} + {self.JIT_CONTEXT_OFFSETS32[field]}]")
        self.writer.emit_movsd_load32(
            dst,
            self.map_reg32(base),
            self.JIT_CONTEXT_OFFSETS32[field]
        )
    
    def emit_movsd_store_field(self, base, offset, src, comment=""):
        base = self.map_reg32(base)
        src  = self.map_xmm(src)
        off  = self.resolve_offset32(offset)
        
        if off == 0:
            addr = f"[{base}]"
        elif off > 0:
            addr = f"[{base}+{off}]"
        else:
            addr = f"[{base}-{abs(off)}]"

        self.asm_lines.append(f"movsd {addr}, {src}")        
        self.writer.emit_movsd_store32(base ,
            self.JIT_CONTEXT_OFFSETS32[offset],
            src
        )

    def resolve_offset32(self, offset):
        if isinstance(offset, int):
            return offset

        if isinstance(offset, str):
            if offset.lstrip("-").isdigit():
                return int(offset)

            if offset.startswith  ("offsetof(JitContext, ") and offset.endswith(")"):
                field = offset[len("offsetof(JitContext, "):-1]
                return self.JIT_CONTEXT_OFFSETS32[field]

        raise RuntimeError(f"{tr('unsupported NT32 offset')}: {offset}")

    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_reg32(
            self.map_reg32(base),
            self.resolve_offset32(offset),
            self.map_reg32(src)
        )

    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""):
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            self.resolve_offset32(offset)
        )

    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            self.resolve_offset32(offset)
        )
        
    def emit_imul(self, dst, src, value=None, comment=""):
        self.writer.emit_imul(
            self.map_reg32(dst),
            self.map_reg32(src),
            value
        )

    def emit_cdq(self, comment=""):
        self.writer.emit_cdq()

    def emit_idiv(self, reg, comment=""):
        reg32 = self.map_reg32(reg)
        line  = f"idiv {reg32}"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(line)
        self.writer.emit_idiv_r32(
            reg32
        )
        
    def emit_cmp(self, dst, value, comment=""):
        dst32 = self.map_reg32(dst)

        if isinstance(value, str):
            if value.lstrip("-").isdigit():
                value = int(value)
            else:
                self.writer.emit_cmp_reg_reg32(
                    dst32,
                    self.map_reg32(value)
                )
                return

        self.writer.emit_cmp_reg_imm32(dst32, value)
    
    def emit_and(self, dst, src, comment=""):
        dst = self.map_reg32(dst)

        if isinstance(src, int) or str(src).isdigit():
            line = f"and {dst}, {src}"
        else:
            src = self.map_reg32(src)
            line = f"and {dst}, {src}"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(line)
        self.emit(line)

    def emit_or(self, dst, src, comment=""):
        dst = self.map_reg32(dst)

        if isinstance(src, int) or str(src).isdigit():
            line = f"or {dst}, {src}"
        else:
            src = self.map_reg32(src)
            line = f"or {dst}, {src}"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(line)
        self.emit(line)
    
    #def emit_xor(self, dst, src, comment=""):
    #    self.writer.emit_xor_reg_reg(
    #        self.map_reg32(dst),
    #        self.map_reg32(src)
    #    )
    
    def emit_xor(self, dst, src, comment=""):
        dst = self.map_reg32(dst)

        if isinstance(src, int):
            line = f"xor {dst}, {src}"
        else:
            src = self.map_reg32(src)
            line = f"xor {dst}, {src}"

        if comment:
            line += f" ; {comment}"

        self.asm_lines.append(line)
        self.emit(line)
    
    def emit_setne(self, reg, comment=""):
        self.asm_lines.append(f"setne {self.map_reg8(reg)}")
        self.writer.emit_setne(
            self.map_reg8(reg)
        )

    def map_reg8(self, reg):
        reg_map = {
            "al": "al",
            "cl": "cl",
            "dl": "dl",
            "bl": "bl",
        }

        if reg not in reg_map:
            raise RuntimeError(f"{tr('unsupported NT32 8-bit register')}: {reg}")

        return reg_map[reg]
    
    def emit_movzx(self, dst, src, comment=""):
        self.writer.emit_movzx_r32_r8(
            self.map_reg32(dst),
            self.map_reg8(src)
        )

    def emit_test(self, reg1, reg2, comment=""):
        self.asm_lines.append(f"test {reg1}. {reg2}")
        self.writer.emit_test_reg_reg32(
            self.map_reg32(reg1),
            self.map_reg32(reg2)
        )
        
    def emit_call_reg(self, reg, comment=""):
        seöf.asm_lines.append(f"call {self.map_reg32(reg)}")
        self.writer.emit_call_reg32(self.map_reg32(reg))
    
    def emit_push_data_label32(self, label):
        self.asm_lines.append(f"push {label}")
        self.writer.emit_push_data_label32(label)

    def emit_cleanup_stack(self, size):
        if size:
            self.asm_lines.append(f"add esp, {size}")
            self.writer.emit_add_reg_imm32("esp", size)
    
    def emit_movsd_store(self, base, offset, src, comment=""):
        self.writer.emit_movsd_store32(
            self.map_reg32(base),
            self.resolve_offset32(offset),
            src
        )

    def emit_movsd_load(self, dst, base, offset=0, comment=""):
        self.writer.emit_movsd_load32(
            dst,
            self.map_reg32(base),
            self.resolve_offset32(offset)
        )
    
    def emit_cvtsi2sd(self, dst, src, comment=""):
        self.writer.emit_cvtsi2sd32(dst, self.map_reg32(src))
    
    def emit_addsd(self, dst, src, comment=""): self.writer.emit_sse2_xmm_xmm32(0x58, dst, src)
    def emit_subsd(self, dst, src, comment=""): self.writer.emit_sse2_xmm_xmm32(0x5C, dst, src)
    def emit_mulsd(self, dst, src, comment=""): self.writer.emit_sse2_xmm_xmm32(0x59, dst, src)
    def emit_divsd(self, dst, src, comment=""): self.writer.emit_sse2_xmm_xmm32(0x5E, dst, src)
    
    def emit_mov_qword(self, dst, base, field, comment=""):
        # NT32: qword aus gemeinsamem Generator bedeutet hier Pointer-Feld,
        # aber im 32-bit Backend laden wir dword.
        dst  = self.map_reg32(dst)
        base = self.map_reg32(base)
        off  = self.JIT_CONTEXT_OFFSETS32[field]

        if off == 0:
            addr = f"[{base}]"
        elif off > 0:
            addr = f"[{base}+{off}]"
        else:
            addr = f"[{base}-{abs(off)}]"

        self.asm_lines.append(f"mov {dst}, dword {addr}")
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            self.JIT_CONTEXT_OFFSETS32[field]
        )

    def emit_mov_dword(self, dst, base, field, comment=""):
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            self.JIT_CONTEXT_OFFSETS32[field]
        )
    
    def emit_movsxd(self, dst, src, comment=""):
        # NT32:
        # Der gemeinsame 64-Bit-Code ruft z.B. movsxd rax,eax auf.
        # In 32 Bit ist das ein No-Op, weil eax bereits 32 Bit ist.
        dst32 = self.map_reg32(dst)
        src32 = self.map_reg32(src)

        if dst32 == src32:
            return

        self.asm_lines.append(f"mov {dst32}, {src32}")
        self.writer.emit_mov_reg_reg32(dst32, src32)

    def emit_mov_reg_dword(self, dst, base, comment=""):
        self.asm_lines.append(f"mov {self.map_reg32(dst)}, {self.map_reg32(base)}")
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            0
        )

    def emit_mov_reg_qword(self, dst, base, comment=""):
        # NT32: qword-Load aus gemeinsamem Code bedeutet meistens Pointer-Load.
        # Also dword laden.
        self.asm_lines.append(f"mov {self.map_reg32(dst)}, [{self.map_reg32(base)}]")
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            0
        )

    def emit_mov_reg_byte(self, dst, base, comment=""):
        raise NotImplementedError(tr("NT32 byte load is not implemented yet"))

    def emit_sete(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"sete {reg}")
        self.writer.emit_sete(reg)

    def emit_setne(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"setne {reg}")
        self.writer.emit_setne(reg)

    def emit_setl(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"setl {reg}")
        self.writer.emit_setl(reg)

    def emit_setle(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"setle {reg}")
        self.writer.emit_setle(reg)

    def emit_setg(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"setg {reg}")
        self.writer.emit_setg(reg)

    def emit_setge(self, reg, comment=""):
        reg = self.map_reg8(reg)
        self.asm_lines.append(f"setge {reg}")
        self.writer.emit_setge(reg)
    
    def emit_program_entry_old(self):
        frame_size = 512

        self.emit_bind_label("_start")
        self.asm_lines.append("_start:")

        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")
        
        self.emit_sub("esp", frame_size, comment="top exception frame")
        self.emit_mov("ebx", "esp", comment="frame ptr")

        self.emit_push("ebx")
        self.emit_call("_jit_exception_push")
        self.emit_cleanup_stack(4)

        self.emit_push("ebx")
        self.emit_call("_jit_setjmp")
        self.emit_cleanup_stack(4)

        except_label = "__top_except"
        exit_label   = "__top_exit"

        self.emit_cmp("eax", 0)
        self.emit_jne(except_label)

        self.emit_call("_main")

        self.emit_push("ebx")
        self.emit_call("_jit_exception_pop")
        self.emit_cleanup_stack(4)

        self.emit_mov("eax", 0)
        self.emit_jmp(exit_label)

        self.emit_bind_label(except_label)

        self.emit_push("ebx")
        self.emit_call("_jit_exception_pop")
        self.emit_cleanup_stack(4)

        self.emit_mov("eax", 1)

        self.emit_bind_label(exit_label)

        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()
    
    def emit_program_entry(self):
        frame_size = 512
        packed_runtime = bool(
            getattr(CDATA, "packed_runtime", False)
        )

        runtime_ready_label = "__packed_runtime_ready"
        except_label = "__top_except"
        exit_label = "__top_exit"
        return_label = "__entry_return"

        self.emit_bind_label("_start")
        self.asm_lines.append("_start:")

        self.emit_push("ebp")
        self.emit_mov("ebp", "esp")

        # The normal Windows loader resolves the EXE import table before
        # AddressOfEntryPoint is entered.  In packed mode the embedded
        # runtime therefore has to be loaded before the first _jit_* call.
        if packed_runtime:
            self.emit_call("_packed_runtime_init")
            self.emit_test("eax", "eax")
            self.emit_jne(runtime_ready_label)

            self.emit_mov("eax", 1)
            self.emit_jmp(return_label)

            self.emit_bind_label(runtime_ready_label)

        # ---------------------------------------------------------
        # Exception-Frame in EDI
        # ---------------------------------------------------------
        self.emit_sub(
            "esp",
            frame_size,
            comment="top exception frame"
        )

        self.emit_mov(
            "edi",
            "esp",
            comment="exception frame"
        )

        self.emit_push("edi")
        self.emit_call("_jit_exception_push")
        self.emit_cleanup_stack(4)

        self.emit_push("edi")
        self.emit_call("_jit_setjmp")
        self.emit_cleanup_stack(4)

        self.emit_cmp("eax", 0)
        self.emit_jne(except_label)

        # ---------------------------------------------------------
        # EBX = Adresse des JitContext
        # ---------------------------------------------------------
        self.writer.emit_mov_reg_data_label32(
            "ebx",
            "ctx"
        )

        self.asm_lines.append("mov ebx, ctx")

        self.emit_call("_main")

        self.emit_push("edi")
        self.emit_call("_jit_exception_pop")
        self.emit_cleanup_stack(4)

        self.emit_mov("eax", 0)
        self.emit_jmp(exit_label)

        self.emit_bind_label(except_label)

        self.emit_push("edi")
        self.emit_call("_jit_exception_pop")
        self.emit_cleanup_stack(4)

        self.emit_mov("eax", 1)

        self.emit_bind_label(exit_label)

        if packed_runtime:
            # Preserve the Pascal process result while the loader releases
            # the temporary runtime module.
            self.emit_push("eax")
            self.emit_call("_packed_runtime_shutdown")
            self.emit_pop("eax")

        self.emit_bind_label(return_label)

        self.emit_mov("esp", "ebp")
        self.emit_pop("ebp")
        self.emit_ret()


    def write(self, filename):
        self.emit_program_entry()
        NTWriter32(self).write(filename)
        