# ---------------------------------------------------------------------------
# File: coff32.py - backend for coff32
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

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

    def pointer_slot_size(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            return 4
        return 8
        
    def emit_new_label_decl(self, name, comment=""):
        # PE32/COFF braucht keine vorherige Label-Deklaration
        return

    def emit_bind_label(self, label, comment=""):
        self.writer.bind_label(label)

    def emit_ret(self, comment=""):
        self.writer.emit_ret()

    def emit_call_lbl(self, label, comment=""):
        if label in ["rax", "eax"]:
            self.writer.emit_call_reg32("eax")
            return

        if label in ["rbx", "ebx"]:
            self.writer.emit_call_reg32("ebx")
            return

        if label in ["rcx", "ecx"]:
            self.writer.emit_call_reg32("ecx")
            return

        if label in ["rdx", "edx"]:
            self.writer.emit_call_reg32("edx")
            return
            
        self.writer.emit_call_label(label)

    def emit_call(self, target, comment=""):
        if target in ["rax", "eax"] and self.pending_call_symbol:
            name = self.pending_call_symbol
            self.pending_call_symbol = None
            self.writer.emit_call_external(name)
            return

        if target in ["rax", "eax"]:
            self.writer.emit_call_reg32("eax")
            return
        
        if target in ["rbx", "ebx"]:
            self.writer.emit_call_reg32("ebx")
            return

        if target in ["rcx", "ecx"]:
            self.writer.emit_call_reg32("ecx")
            return

        if target in ["rdx", "edx"]:
            self.writer.emit_call_reg32("edx")
            return

        self.writer.emit_call_external(target)
    
    def emit_jmp(self, label, comment=""):
        self.writer.emit_jmp(label)

    def emit_je(self, label, comment=""):
        self.writer.emit_je(label)

    def emit_jne(self, label, comment=""):
        self.writer.emit_jne(label)

    def emit_jz(self, label, comment=""):
        self.writer.emit_je(label)

    def emit_jnz(self, label, comment=""):
        self.writer.emit_jne(label)

    def emit_jl(self, label, comment=""):
        self.writer.emit_jl(label)

    def emit_jle(self, label, comment=""):
        self.writer.emit_jle(label)

    def emit_jg(self, label, comment=""):
        self.writer.emit_jg(label)

    def emit_jge(self, label, comment=""):
        self.writer.emit_jge(label)

    def emit_jmp(self, label, comment=""):
        self.writer.emit_jmp(label)

    def emit_je(self, label, comment=""):
        self.writer.emit_je(label)

    def emit_jne(self, label, comment=""):
        self.writer.emit_jne(label)

    def emit_jz(self, label, comment=""):
        self.writer.emit_je(label)

    def emit_jnz(self, label, comment=""):
        self.writer.emit_jne(label)

    def emit_jl(self, label, comment=""):
        self.writer.emit_jl(label)

    def emit_jle(self, label, comment=""):
        self.writer.emit_jle(label)

    def emit_jg(self, label, comment=""):
        self.writer.emit_jg(label)

    def emit_jge(self, label, comment=""):
        self.writer.emit_jge(label)

    def emit_jcc(self, cc, label):
        opcodes = {
            "je":  b"\x0F\x84",
            "jne": b"\x0F\x85",
            "jl":  b"\x0F\x8C",
            "jle": b"\x0F\x8E",
            "jg":  b"\x0F\x8F",
            "jge": b"\x0F\x8D",
        }

        if cc not in opcodes:
            raise RuntimeError(f"{tr('unsupported PE32 condition jump')}: {cc}")

        self.text += opcodes[cc]

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
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

    def emit_push(self, reg, comment=""):
        self.writer.emit_push_reg32(self.map_reg32(reg))

    def emit_pop(self, reg, comment=""):
        self.writer.emit_pop_reg32(self.map_reg32(reg))
        
    def emit_mov(self, dst, src, comment=""):
        dst32 = self.map_reg32(dst)

        if isinstance(src, int):
            self.writer.emit_mov_reg_imm32(dst32, src)
            return

        if isinstance(src, str):
            if src.lstrip("-").isdigit():
                self.writer.emit_mov_reg_imm32(dst32, int(src))
                return

            if src.startswith("str_"):
                self.writer.emit_mov_reg_data_label32(dst32, src)   # Adresse
                return

            if src.startswith("_var_"):
                self.writer.emit_mov_reg_from_data_label32(dst32, src)  # Inhalt
                return

        self.writer.emit_mov_reg_reg32(
            dst32,
            self.map_reg32(src)
        )

    def emit_sub(self, reg, value, comment=""):
        reg32 = self.map_reg32(reg)

        if isinstance(value, int):
            self.writer.emit_sub_reg_imm32(reg32, value)
            return

        if isinstance(value, str):
            if value.lstrip("-").isdigit():
                self.writer.emit_sub_reg_imm32(reg32, int(value))
                return

            self.writer.emit_sub_reg_reg32(
                reg32,
                self.map_reg32(value)
            )
            return

        raise RuntimeError(f"unsupported NT32 sub value: {value}")

    def emit_add(self, reg, value, comment=""):
        reg32 = self.map_reg32(reg)

        if isinstance(value, int):
            self.writer.emit_add_reg_imm32(reg32, value)
            return

        if isinstance(value, str):
            if value.lstrip("-").isdigit():
                self.writer.emit_add_reg_imm32(reg32, int(value))
                return

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
                self.writer.emit_mov_reg_data_label32(dst32, value)         # Adresse
                return
            
            if value.startswith("_var_"):
                self.writer.emit_mov_reg_from_data_label32(dst32, value)     # Inhalt
                return

            # &Runtime / &API
            if value.startswith("&"):
                self.pending_call_symbol = value[1:]
                return

            if value.lstrip("-").isdigit():
                value = int(value)

        self.writer.emit_mov_reg_imm32(dst32, value)
        
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        self.writer.emit_mov_mem_reg32(
            self.map_reg32(base),
            self.resolve_offset32(offset),
            self.map_reg32(src)
        )

    def emit_movsd_load_field(self, dst, base, field, comment=""):
        self.writer.emit_movsd_load32(
            dst,
            self.map_reg32(base),
            self.JIT_CONTEXT_OFFSETS32[field]
        )
    
    def emit_movsd_store_field(self, base, field, src, comment=""):
        self.writer.emit_movsd_store32(
            self.map_reg32(base),
            self.JIT_CONTEXT_OFFSETS32[field],
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
        self.writer.emit_idiv_r32(
            self.map_reg32(reg)
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
    
    def emit_xor(self, dst, src, comment=""):
        self.writer.emit_xor_reg_reg(
            self.map_reg32(dst),
            self.map_reg32(src)
        )
    
    def emit_setne(self, reg, comment=""):
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
        self.writer.emit_test_reg_reg32(
            self.map_reg32(reg1),
            self.map_reg32(reg2)
        )
        
    def emit_call_reg(self, reg, comment=""):
        self.writer.emit_call_reg32(self.map_reg32(reg))
    
    def emit_push_data_label32(self, label):
        self.writer.emit_push_data_label32(label)

    def emit_cleanup_stack(self, size):
        if size:
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

        self.writer.emit_mov_reg_reg32(dst32, src32)

    def emit_mov_reg_dword(self, dst, base, comment=""):
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            0
        )

    def emit_mov_reg_qword(self, dst, base, comment=""):
        # NT32: qword-Load aus gemeinsamem Code bedeutet meistens Pointer-Load.
        # Also dword laden.
        self.writer.emit_mov_reg_mem32(
            self.map_reg32(dst),
            self.map_reg32(base),
            0
        )

    def emit_mov_reg_byte(self, dst, base, comment=""):
        raise NotImplementedError(tr("NT32 byte load is not implemented yet"))
    
    def emit_program_entry(self):
        frame_size = 512

        self.emit_bind_label("_start")

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
    
    def write(self, filename):
        print("12121212121223");
        self.emit_program_entry()
        NTWriter32(self).write(filename)
