# ---------------------------------------------------------------------------
# File: pe32coff.py - PE 32-bit coff writer
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.common.locale    import *
from compiler.common.constants import *

# ---------------------------------------------------------------------------
# Windows 64-Bit PE coff writer ...
# ---------------------------------------------------------------------------
class PE64CoffWriter:
    def __init__(self):
        self.regs = {
            "al"  :  0, "cl"  :  1, "dl"  :  2, "bl"  :  3,
            "spl" :  4, "bpl" :  5, "sil" :  6, "dil" :  7,
            "r8b" :  8, "r9b" :  9, "r10b": 10, "r11b": 11,
            "r12b": 12, "r13b": 13, "r14b": 14, "r15b": 15,

            "rax" :  0, "rcx" :  1, "rdx" :  2, "rbx" :  3,
            "rsp" :  4, "rbp" :  5, "rsi" :  6, "rdi" :  7,
            "r8"  :  8, "r9"  :  9, "r10" : 10, "r11" : 11,
            "r12" : 12, "r13" : 13, "r14" : 14, "r15" : 15,
            
            "eax" :  0, "ecx" :  1, "edx" :  2, "ebx" :  3,
            "esp" :  4, "ebp" :  5, "esi" :  6, "edi" :  7,
            "r8d" :  8, "r9d" :  9, "r10d": 10, "r11d": 11,
            "r12d": 12, "r13d": 13, "r14d": 14, "r15d": 15,
        }
        
        self.text               = bytearray()
        self.data               = bytearray()
        
        self.text_relocations   = []
        self.data_relocations   = []

        self.symbols            = []
        self.labels             = {}
        self.fixups             = []
        
        self.string_table       = bytearray()
        self.string_offsets     = {}

    def pointer_slot_size(self):
        if CDATA.args_target in ["nt35", "winnt", "win32"]:
            return 4
        return 8
    
    def begin_function(self, name, local_size=0, public=True):
        offset = len(self.text)
        self.bind_label(name)
        self.add_symbol(
            name            = name,
            value           = offset,
            section_number  = 1
        )
        self.emit_function_prolog(local_size)
        return offset

    def end_function(self):
        self.emit_function_epilog()
        
    def align_data(self, alignment):
        while len(self.data) % alignment != 0:
            self.data.append(0)

    def add_data_i32(self, name, value=0):
        return self.add_data_bytes(name,
            int(value).to_bytes(4, "little", signed=True),
            alignment = 4
        )

    def add_data_qword(self, name, value=0):
        return self.add_data_bytes(name,
            int(value).to_bytes(8, "little", signed=False),
            alignment = 8
        )

    def add_data_double(self, name, value=0.0):
        bits = double_to_bits(value)
        return self.add_data_bytes(name,
            int(bits).to_bytes(8, "little", signed=False),
            alignment = 8
        )

    def add_data_bytes(self, name, data_bytes, alignment=1):
        self.align_data(alignment)

        offset = len(self.data)
        self.data += data_bytes

        self.add_symbol(
            name=name,
            value=offset,
            section_number = 2
        )
        return offset

    def add_data_zeros(self, name, size, alignment=8):
        return self.add_data_bytes(name,
            b"\x00" * size,
            alignment
        )
    
    def add_data_qword_symbol_ref(self, target_symbol):
        sym_index   = self.find_or_add_symbol(target_symbol)
        offset      = len(self.data)
        self.data  += b"\x00" * 8

        self.data_relocations.append({
            "offset": offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_ADDR64
        })
        return offset
        
    def add_data_i32_array   (self, name, count): return self.add_data_zeros(name, count * 4, alignment=4)
    def add_data_qword_array (self, name, count): return self.add_data_zeros(name, count * 8, alignment=8)
    def add_data_double_array(self, name, count): return self.add_data_zeros(name, count * 8, alignment=8)
    
    def add_jit_context( self,
        name          = "ctx",
        int_count     =   256,
        double_count  =   256,
        string_count  =   256,
        record_bytes  =  4096,
        arrays_bytes  =  4096,
        pointer_count =   256):
        
        self.add_data_i32_array     ("int_vars"   , int_count)
        self.add_data_double_array  ("double_vars", double_count)
        self.add_data_qword_array   ("string_vars", string_count)
        self.add_data_zeros         ("record_vars", record_bytes, alignment = 8)
        self.add_data_zeros         ("arrays_vars", arrays_bytes, alignment = 8)
        self.add_data_qword_array   ("pointr_vars", pointer_count)

        self.align_data(8)
        ctx_offset = len(self.data)

        self.add_symbol(
            name           = name,
            value          = ctx_offset,
            section_number = 2
        )

        self.add_data_qword_symbol_ref("int_vars")
        self.add_data_qword_symbol_ref("double_vars")
        self.add_data_qword_symbol_ref("string_vars")
        self.add_data_qword_symbol_ref("record_vars")
        self.add_data_qword_symbol_ref("arrays_vars")
        self.add_data_qword_symbol_ref("pointr_vars")

        self.data += b"\x00" * 4   # print_int_tmp
        self.data += b"\x00" * 4   # padding
        self.data += b"\x00" * 8   # print_double_tmp

        return ctx_offset
    
    def add_data_i32(self, name, value = 0):
        return self.add_data_bytes(name,
            int(value).to_bytes(4, "little", signed = True),
            alignment=4
        )

    def add_data_qword(self, name, value = 0):
        return self.add_data_bytes(name,
            int(value).to_bytes(8, "little", signed = False),
            alignment=8
        )
    
    def _is_ext_reg(self, reg): return self._reg_id(reg) >= 8
    def _reg_low3  (self, reg): return self._reg_id(reg)  & 7
    
    def _reg_id(self, reg):
        if reg not in self.regs:
            raise RuntimeError(f"{tr('unsupported register')}: {reg}")
        return self.regs[reg]
    
    def _xmm_id(self, reg):
        if not isinstance(reg, str):
            raise RuntimeError(f"{tr('unsupported xmm register')}: {reg}")

        reg = reg.lower()

        if not reg.startswith("xmm"):
            raise RuntimeError(f"{tr('unsupported xmm register')}: {reg}")
        try:
            n = int(reg[3:])
        except ValueError:
            raise RuntimeError(f"{tr('unsupported xmm register')}: {reg}")

        if n < 0 or n > 15:
            raise RuntimeError(f"{tr('unsupported xmm register')}: {reg}")

        return n
    
    def _emit_rex_xmm_mem(self, xmm_id, base):
        base_id = self._reg_id(base)

        rex = 0x48
        if xmm_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        self.text.append(rex)

    def emit_mov_r32_data_label(self, dst, label):
        dst_id    = self._reg_id(dst)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text.append(0x8B)  # mov r32, r/m32

        # RIP-relative: mod=00, reg=dst, rm=101
        self.text.append(0x05 | ((dst_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset"        : reloc_offset,
            "symbol_index"  : sym_index,
            "type"          : IMAGE_REL_AMD64_REL32
        })

    def emit_mov_data_label_r32(self, label, src):
        src_id    = self._reg_id(src)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x40
        if src_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text.append(0x89)  # mov r/m32, r32

        # RIP-relative: mod=00, reg=src, rm=101
        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset"        : reloc_offset,
            "symbol_index"  : sym_index,
            "type"          : IMAGE_REL_AMD64_REL32
        })

    def emit_mov_r64_data_label(self, dst, label):
        dst_id = self._reg_id(dst)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x48
        if dst_id >= 8:
            rex |= 0x04

        self.text.append(rex)
        self.text.append(0x8B)

        self.text.append(0x05 | ((dst_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })

    def emit_mov_data_label_r64(self, label, src):
        src_id = self._reg_id(src)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x48
        if src_id >= 8:
            rex |= 0x04

        self.text.append(rex)
        self.text.append(0x89)

        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })
    
    def emit_movsd_data_label(self, dst, label):
        dst_id = self._xmm_id(dst)
        sym_index = self.find_or_add_symbol(label)

        self.text += b"\xF2"

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text += b"\x0F\x10"
        self.text.append(0x05 | ((dst_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })

    def emit_movsd_data_label_store(self, label, src):
        src_id = self._xmm_id(src)
        sym_index = self.find_or_add_symbol(label)

        self.text += b"\xF2"

        rex = 0x40
        if src_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text += b"\x0F\x11"
        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })
    
    ##
    def emit_movsd_load(self, dst, base, offset=0):
        dst_id = self._xmm_id(dst)

        self.text += b"\xF2"
        self._emit_rex_xmm_mem(dst_id, base)
        self.text += b"\x0F\x10"

        self._emit_modrm_mem(dst_id, base, offset)

    def emit_movsd_store(self, base, offset, src):
        src_id = self._xmm_id(src)

        self.text += b"\xF2"
        self._emit_rex_xmm_mem(src_id, base)
        self.text += b"\x0F\x11"

        self._emit_modrm_mem(src_id, base, offset)
    
    def _emit_modrm_mem(self, reg_id, base, offset=0):
        base_id = self._reg_id(base)

        reg = reg_id  & 7
        rm  = base_id & 7

        needs_sib  = rm == 4          # rsp / r12
        needs_disp = base in ("rbp", "r13") and offset == 0

        if offset == 0 and not needs_disp: mod = 0x00
        elif -128 <= offset <= 127:        mod = 0x40
        else:                              mod = 0x80

        if needs_disp:
            mod = 0x40
            offset = 0

        if needs_sib:
            self.text.append(mod | (reg << 3) | 0x04)

            # SIB: scale=0, index=none(4), base=rm
            self.text.append(0x20 | rm)
        else:
            self.text.append(mod | (reg << 3) | rm)

        if mod == 0x40:
            self.text.append(offset & 0xFF)
        elif mod == 0x80:
            self.text += int(offset).to_bytes(4, "little", signed=True)

    def _emit_xmm_xmm(self, prefix, opcode, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._xmm_id(src)

        if prefix is not None:
            self.text.append(prefix)

        rex = 0x40
        if dst_id >= 8:
            rex |= 0x04
        if src_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text += b"\x0F"
        self.text.append(opcode)
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_addsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x58, dst, src)
    def emit_subsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x5C, dst, src)
    def emit_mulsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x59, dst, src)
    def emit_divsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x5E, dst, src)

    def emit_ucomisd(self, left, right):
        self._emit_xmm_xmm(0x66, 0x2E, left, right)

    def emit_cvtsi2sd(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._reg_id(src)
        
        self.text += b"\xF2"
        
        rex = 0x48
        if dst_id >= 8: rex |= 0x04
        if src_id >= 8: rex |= 0x01
        
        self.text.append(rex)
        self.text += b"\x0F\x2A"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_sub_r64_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x48
        if reg_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x81)
        self.text.append(0xE8 | (reg_id & 7))  # /5 SUB
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_add_r64_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x48
        if reg_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x81)
        self.text.append(0xC0 | (reg_id & 7))  # /0 ADD
        self.text += int(value).to_bytes(4, "little", signed=True)
        
    # --------------------------------
    # Label definieren
    # --------------------------------
    def bind_label(self, name):
        self.labels[name] = len(self.text)

        pending = [
            f for f in self.fixups
            if f["label"] == name
        ]

        for fix in pending:
            self.patch_rel32(
                fix["patch_pos"],
                self.labels[name]
            )

        self.fixups = [
            f for f in self.fixups
            if f["label"] != name
        ]
    
    # --------------------------------
    # add r32, r32
    # --------------------------------
    def emit_add_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40

        if src_id >= 8:
            rex |= 0x04  # REX.R

        if dst_id >= 8:
            rex |= 0x01  # REX.B

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x01)  # add r/m32, r32
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # and r32, r32
    # --------------------------------
    def emit_and_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        if src_id >= 8 or dst_id >= 8:
            rex = 0x40
            if src_id >= 8:
                rex |= 0x04
            if dst_id >= 8:
                rex |= 0x01
            self.text.append(rex)

        self.text.append(0x21)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    def emit_add_r32_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x40
        if reg_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x81)
        self.text.append(0xC0 | (reg_id & 7))  # /0 ADD
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_sub_r32_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x40
        if reg_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x81)
        self.text.append(0xE8 | (reg_id & 7))  # /5 SUB
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_add_r32_imm(self, reg, value): self.emit_add_r32_imm32(reg, value)
    def emit_sub_r32_imm(self, reg, value): self.emit_sub_r32_imm32(reg, value)
    
    def emit_add_r64_r64(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x48
        if src_id >= 8:
            rex |= 0x04
        if dst_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x01)  # add r/m64, r64
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))

    def emit_sub_r64_r64(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x48
        if src_id >= 8:
            rex |= 0x04
        if dst_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x29)  # sub r/m64, r64
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # or r32, r32
    # --------------------------------
    def emit_or_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        if src_id >= 8 or dst_id >= 8:
            rex = 0x40
            if src_id >= 8:
                rex |= 0x04
            if dst_id >= 8:
                rex |= 0x01
            self.text.append(rex)

        self.text.append(0x09)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # xor r32, r32
    # --------------------------------
    def emit_xor_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        if src_id >= 8 or dst_id >= 8:
            rex = 0x40
            if src_id >= 8:
                rex |= 0x04
            if dst_id >= 8:
                rex |= 0x01
            self.text.append(rex)

        self.text.append(0x31)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
        
    # --------------------------------
    # sub r32, r32
    # --------------------------------
    def emit_sub_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40

        if src_id >= 8:
            rex |= 0x04

        if dst_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x29)  # sub r/m32, r32
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # imul r32, r32
    # --------------------------------
    def emit_imul_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40

        if dst_id >= 8:
            rex |= 0x04  # REX.R

        if src_id >= 8:
            rex |= 0x01  # REX.B

        if rex != 0x40:
            self.text.append(rex)

        self.text += b"\x0F\xAF"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))
    
    def emit_imul_r32_r32_imm32(self, dst, src, value):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if src_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x69)  # imul r32, r/m32, imm32
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_imul(self, dst, src, value=None):
        if value is None:
            self.emit_imul_r32_r32(dst, src)
        else:
            self.emit_imul_r32_r32_imm32(dst, src, value)
    
    def emit_external_call(self, symbol_name):
        self.emit_call_rel32(symbol_name)

    def emit_runtime_call(self, symbol_name, arg_regs=None):
        if arg_regs is None:
            arg_regs = []

        # Windows x64:
        # 32 Byte Shadow Space + 8 Byte Alignment-Ausgleich
        self.emit_sub_rsp_imm8(40)
        self.emit_external_call(symbol_name)
        self.emit_add_rsp_imm8(40)
    
    def emit_call_rel32(self, symbol_name):
        sym_index = self.find_or_add_external(symbol_name)
        self.text.append(0xE8)

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset"        : reloc_offset,
            "symbol_index"  : sym_index,
            "type"          : IMAGE_REL_AMD64_REL32
        })
    
    def emit_call_r64(self, reg):
        reg_id = self._reg_id(reg)

        rex = 0x40
        if reg_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0xFF)
        self.text.append(0xD0 | (reg_id & 7))  # /2 call r64
    
    def emit_call(self, target):
        if target in self.labels or target.startswith(("class_", "proc_", "func_")):
            self.emit_call_label(target)
            return

        if target.startswith("_"):
            self.emit_runtime_call(target)
            return

        self.emit_sub_rsp_imm8(40)
        self.emit_call_r64(target)
        self.emit_add_rsp_imm8(40)
    
    def emit_call_lbl(self, target):
        self.emit_runtime_call(target)

    def emit_call_reg(self, target):
        self.emit_sub_rsp_imm8(40)
        self.emit_call_r64(target)
        self.emit_add_rsp_imm8(40)

    def emit_call_label(self, label):
        self.text.append(0xE8)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    def emit_cdq(self):
        self.text.append(0x99)
    
    # --------------------------------
    # idiv r32
    # --------------------------------
    def emit_idiv_r32(self, reg):
        reg_id = self._reg_id(reg)

        if reg_id >= 8:
            self.text.append(0x41)

        self.text.append(0xF7)
        self.text.append(0xF8 | (reg_id & 7))  # /7 idiv
    
    # --------------------------------
    # Vergleichsoperator abbilden
    # --------------------------------
    def emit_compare_result_eax_ebx(self, op):
        self.emit_cmp_r32_r32("eax", "ebx")

        set_map = {
            "=":  "sete",
            "<>": "setne",
            "<":  "setl",
            "<=": "setle",
            ">":  "setg",
            ">=": "setge",
        }

        if op not in set_map:
            raise RuntimeError(f"{tr('unsupported compare operator')}: {op}")

        self.emit_setcc_al(set_map[op])
        self.emit_movzx_eax_al()
    
    # --------------------------------
    # Sprung auf Label
    # --------------------------------
    def emit_jmp_label(self, label):
        patch_pos = self.emit_jmp_placeholder()

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    # --------------------------------
    # Bedingter Sprung auf Label
    # --------------------------------
    def emit_jcc_label(self, cc, label):
        patch_pos = self.emit_jcc_placeholder(cc)

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    # --------------------------------
    # Am Ende prüfen
    # --------------------------------
    def check_unresolved_labels(self):
        if self.fixups:
            names = ", ".join(f["label"] for f in self.fixups)
            raise RuntimeError(f"{tr('Unresolved labels')}: {names}")
    
    def emit_cmp(self, left, right):
        if isinstance(right, int):
            if left.startswith("r") and not left.endswith("d"):
                self.emit_cmp_r64_imm32(left, right)
            else:
                self.emit_cmp_r32_imm32(left, right)
            return

        if left.startswith("r") and not left.endswith("d") and right.startswith("r") and not right.endswith("d"):
            self.emit_cmp_r64_r64(left, right)
        else:
            self.emit_cmp_r32_r32(left, right)

    def emit_test(self, left, right):
        if left.startswith("r") and not left.endswith("d") and right.startswith("r") and not right.endswith("d"):
            self.emit_test_r64_r64(left, right)
        else:
            self.emit_test_r32_r32(left, right)

    def emit_jmp(self, label): self.emit_jmp_label(label)
    def emit_je (self, label): self.emit_jcc_label("je" , label)
    def emit_jne(self, label): self.emit_jcc_label("jne", label)
    def emit_jz (self, label): self.emit_jcc_label("je" , label)
    def emit_jnz(self, label): self.emit_jcc_label("jne", label)
    def emit_jl (self, label): self.emit_jcc_label("jl" , label)
    def emit_jle(self, label): self.emit_jcc_label("jle", label)
    def emit_jg (self, label): self.emit_jcc_label("jg" , label)
    def emit_jge(self, label): self.emit_jcc_label("jge", label)
    
    # --------------------------------
    # cmp r32, imm32
    # --------------------------------
    def emit_cmp_r32_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        if reg_id >= 8:
            self.text.append(0x41)  # REX.B für r8d-r15d

        self.text.append(0x81)

        # /7 = CMP
        modrm = 0xF8 | (reg_id & 7)
        self.text.append(modrm)

        self.text += int(value).to_bytes(4, "little", signed=True)
    
    # --------------------------------
    # cmp r32, r32
    # --------------------------------
    def emit_cmp_r32_r32(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x40

        if right_id >= 8:
            rex |= 0x04  # REX.R

        if left_id >= 8:
            rex |= 0x01  # REX.B

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x39)  # cmp r/m32, r32

        modrm = 0xC0 | ((right_id & 7) << 3) | (left_id & 7)
        self.text.append(modrm)
    
    # --------------------------------
    # cmp r64, r64
    # --------------------------------
    def emit_cmp_r64_r64(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x48

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x39)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    def emit_cmp_r64_imm32(self, reg, value):
        reg_id = self._reg_id(reg)
        
        rex = 0x48
        
        if reg_id >= 8:
            rex |= 0x01
        
        self.text.append(rex)
        self.text.append(0x81)
        
        # /7 = cmp
        self.text.append(0xF8 | (reg_id & 7))
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_cmp_r64_r64(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x48

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x39)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    def emit_nil_check_rax(self, ok_label, fail_label):
        self.emit_test_r64_r64("rax", "rax")
        self.emit_jcc_label("jne", ok_label)
        self.emit_jmp_label(fail_label)
    
    # --------------------------------
    # Relativer Sprung mit Patch-Liste
    # --------------------------------
    def emit_jcc_placeholder(self, cc):
        opcodes = {
            "je":  b"\x0F\x84",
            "jne": b"\x0F\x85",
            "jl":  b"\x0F\x8C",
            "jle": b"\x0F\x8E",
            "jg":  b"\x0F\x8F",
            "jge": b"\x0F\x8D",
        }

        if cc not in opcodes:
            raise RuntimeError(f"{tr('unsupported condition jump')}: {cc}")

        self.text += opcodes[cc]

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        return patch_pos
    
    # --------------------------------
    # Operator jump
    # --------------------------------
    def emit_jump_by_op(self, op, label):
        jump_map = {
            "=":  "je",
            "<>": "jne",
            "<":  "jl",
            "<=": "jle",
            ">":  "jg",
            ">=": "jge",
        }

        if op not in jump_map:
            raise RuntimeError(f"{tr('unsupported jump op')}: {op}")

        self.emit_jcc_label(jump_map[op], label)
    
    # --------------------------------
    # Unbedingter Sprung
    # --------------------------------
    def emit_jmp_placeholder(self):
        self.text.append(0xE9)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        return patch_pos
    
    # --------------------------------
    # Sprung patcher
    # --------------------------------
    def patch_rel32(self, patch_pos, target_pos):
        # rel32 ist relativ zum nächsten Befehl,
        # also patch_pos + 4
        rel = target_pos - (patch_pos + 4)

        self.text[patch_pos:patch_pos + 4] = int(rel).to_bytes(
            4,
            "little",
            signed=True
        )
    
    def emit_lea_rcx_data_label(self, label):
        self.emit_lea_reg_data_label("rcx", label)
        
    def emit_lea_r64_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x48

        if dst_id >= 8:
            rex |= 0x04

        if base_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x8D)  # LEA r64, m

        self._emit_modrm_mem(dst_id, base, offset)
    
    def emit_lea_byte (self, dst, base, offset): self.emit_lea_r64_mem(dst, base, offset)
    def emit_lea_dword(self, dst, base, offset): self.emit_lea_r64_mem(dst, base, offset)
    def emit_lea_qword(self, dst, base, offset): self.emit_lea_r64_mem(dst, base, offset)

    # --------------------------------
    # lea reg, [rel data_label]
    # --------------------------------
    def emit_lea_reg_data_label(self, reg, label):
        reg_id = self._reg_id(reg)

        rex = 0x48
        if reg_id >= 8:
            rex |= 0x04

        sym_index = self.find_or_add_symbol(label)

        self.text.append(rex)
        self.text += b"\x8D"

        # RIP-relative: mod=00, r/m=101
        self.text.append(0x05 | ((reg_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })

    def emit_mov_eax_imm32(self, value):
        self.text.append(0xB8)
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_rax_imm64(self, value):
        self.text += b"\x48\xB8"
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    def emit_mov_ecx_imm32(self, value):
        self.text.append(0xB9)  # mov ecx, imm32
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)
        
        if reg_id >= 8:
            self.text.append(0x41)
        
        self.text.append(0xB8 + (reg_id & 7))
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_r8_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x40
        if dst_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x8A)  # mov r8, r/m8
        self._emit_modrm_mem(dst_id, base, offset)

    def emit_mov_mem_r8(self, base, offset, src):
        src_id  = self._reg_id(src)
        base_id = self._reg_id(base)

        rex = 0x40
        if src_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x88)  # mov r/m8, r8
        self._emit_modrm_mem(src_id, base, offset)
    
    def emit_mov_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40
        if src_id >= 8: rex |= 0x04
        if dst_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x89)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    def emit_movsxd_r64_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x48
        if dst_id >= 8:
            rex |= 0x04
        if src_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x63)
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))
    
    def emit_mov_eax_ebx   (self): self.emit_mov_r32_r32   ("eax", "ebx")
    def emit_mov_ebx_eax   (self): self.emit_mov_r32_r32   ("ebx", "eax")
    
    def emit_movsxd_rax_eax(self): self.emit_movsxd_r64_r32("rax", "eax")
    
    # --------------------------------
    # mov r64, imm64
    # --------------------------------
    def emit_mov_reg_imm64(self, reg, value):
        reg_id = self._reg_id(reg)
        rex    = 0x48
        
        if reg_id >= 8:
            rex |= 0x01
            
        self.text.append(rex)
        self.text.append(0xB8 + (reg_id & 7))
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    # --------------------------------
    # mov eax, dword [rax + 8]
    # --------------------------------
    def emit_mov_r32_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x40
        if dst_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x8B)
        self._emit_modrm_mem(dst_id, base, offset)
    
    # --------------------------------
    # mov r64, [base + offset]
    # --------------------------------
    def emit_mov_r64_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x48

        if dst_id >= 8:
            rex |= 0x04  # REX.R

        if base_id >= 8:
            rex |= 0x01  # REX.B

        self.text.append(rex)
        self.text.append(0x8B)  # mov r64, r/m64

        self._emit_modrm_mem(dst_id, base, offset)
    
    # --------------------------------
    # mov dword [base + offset], r32
    # --------------------------------
    def emit_mov_mem_r32(self, base, offset, src):
        src_id  = self._reg_id(src)
        base_id = self._reg_id(base)

        rex = 0x40
        if src_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x89)
        self._emit_modrm_mem(src_id, base, offset)
    
    # --------------------------------
    # mov [base + offset], r64
    # --------------------------------
    def emit_mov_mem_r64(self, base, offset, src):
        src_id  = self._reg_id(src)
        base_id = self._reg_id(base)

        rex = 0x48

        if src_id >= 8:
            rex |= 0x04  # REX.R

        if base_id >= 8:
            rex |= 0x01  # REX.B

        self.text.append(rex)
        self.text.append(0x89)  # mov r/m64, r64

        self._emit_modrm_mem(src_id, base, offset)
    
    def emit_mov_r8d_imm32(self, value):
        self.text += b"\x41\xB8"
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_r9d_imm32(self, value):
        self.text += b"\x41\xB9"
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_r8_imm64(self, value):
        self.text += b"\x49\xB8"
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    def emit_mov_r9_imm64(self, value):
        self.text += b"\x49\xB9"
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    # --------------------------------
    # mov r64, r64
    # --------------------------------
    def emit_mov_r64_r64(self, dst, src):
        ##
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)
        
        rex = 0x48
        
        if src_id >= 8:
            rex |= 0x04   # REX.R
        
        if dst_id >= 8:
            rex |= 0x01   # REX.B
        
        self.text.append(rex)
        self.text.append(0x89)
        
        modrm = 0xC0 | ((src_id & 7) << 3) | (dst_id & 7)
        self.text.append(modrm)
    
    # --------------------------------
    # movzx eax, al
    # --------------------------------
    def emit_movzx_eax_al(self):
        self.text += b"\x0F\xB6\xC0"
    
    def emit_movq_xmm_r64(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._reg_id(src)

        self.text += b"\x66"

        rex = 0x48
        if dst_id >= 8:
            rex |= 0x04
        if src_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text += b"\x0F\x6E"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_movzx_r32_r8(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if src_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text += b"\x0F\xB6"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_movq_r64_xmm(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._xmm_id(src)

        self.text += b"\x66"

        rex = 0x48
        if src_id >= 8: rex |= 0x04
        if dst_id >= 8: rex |= 0x01

        self.text.append(rex)
        self.text += b"\x0F\x7E"
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))

    def emit_mov_xmm_imm64_double_bits(self, xmm, bits):
        self.emit_mov_reg_imm64("rax", bits)
        self.emit_movq_xmm_r64(xmm, "rax")

    def emit_movzx(self, dst, src):
        if dst == "eax" and src == "al":
            self.emit_movzx_eax_al()
            return

        self.emit_movzx_r32_r8(dst, src)
    
    def emit_mov(self, dst, src):
        if isinstance(src, int):
            if dst.startswith("r") and not dst.endswith("d"):
                self.emit_mov_reg_imm64(dst, src)
            else:
                self.emit_mov_reg_imm32(dst, src)
            return

        if dst.startswith("xmm"):
            raise RuntimeError(tr("use XMM-specific mov methods"))

        if dst.startswith("r") and not dst.endswith("d") and src.startswith("r") and not src.endswith("d"):
            self.emit_mov_r64_r64(dst, src)
        else:
            self.emit_mov_r32_r32(dst, src)

    def emit_add(self, dst, src):
        if isinstance(src, int):
            if dst.startswith("r") and not dst.endswith("d"):
                self.emit_add_r64_imm32(dst, src)
            else:
                self.emit_add_r32_imm32(dst, src)
            return

        if dst.startswith("r") and not dst.endswith("d") and src.startswith("r") and not src.endswith("d"):
            self.emit_add_r64_r64(dst, src)
        else:
            self.emit_add_r32_r32(dst, src)

    def emit_setne(self, reg):
        if reg != "al":
            raise RuntimeError(tr("currently only setne al supported"))
        self.emit_setcc_al("setne")

    def emit_sub(self, dst, src):
        if isinstance(src, int):
            if dst.startswith("r") and not dst.endswith("d"):
                self.emit_sub_r64_imm32(dst, src)
            else:
                self.emit_sub_r32_imm32(dst, src)
            return

        if dst.startswith("r") and not dst.endswith("d") and src.startswith("r") and not src.endswith("d"):
            self.emit_sub_r64_r64(dst, src)
        else:
            self.emit_sub_r32_r32(dst, src)
    
    def emit_push_r64(self, reg):
        ##
        reg_id = self._reg_id(reg)
        
        if reg_id >= 8:
            self.text.append(0x41)
        
        self.text.append(0x50 + (reg_id & 7))
    
    def emit_pop_r64(self, reg):
        ##
        reg_id = self._reg_id(reg)
        
        if reg_id >= 8:
            self.text.append(0x41)
        
        self.text.append(0x58 + (reg_id & 7))
        
    def emit_ret(self):
        self.text.append(0xC3)
    
    def emit_setcc_al(self, cc):
        opcodes = {
            "sete":  b"\x0F\x94",
            "setne": b"\x0F\x95",
            "setl":  b"\x0F\x9C",
            "setle": b"\x0F\x9E",
            "setg":  b"\x0F\x9F",
            "setge": b"\x0F\x9D",
        }

        if cc not in opcodes:
            raise RuntimeError(f"{tr('unsupported setcc')}: {cc}")

        self.text += opcodes[cc]
        self.text.append(0xC0)  # al
    
    def emit_sub_rsp_imm8(self, value):
        self.text += b"\x48\x83\xEC"
        self.text.append(value & 0xFF)

    def emit_add_rsp_imm8(self, value):
        self.text += b"\x48\x83\xC4"
        self.text.append(value & 0xFF)

    # --------------------------------
    # test r32, r32
    # --------------------------------
    def emit_test_r32_r32(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x40

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x85)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    # --------------------------------
    # test r64, r64
    # --------------------------------
    def emit_test_r64_r64(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x48

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x85)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    def emit_function_prolog(self, local_size=256):
        self.emit_push_r64("rbp")
        self.emit_mov_r64_r64("rbp", "rsp")

        if local_size:
            self.emit_sub_r64_imm32("rsp", local_size)

    def emit_function_epilog(self):
        self.emit_mov_r64_r64("rsp", "rbp")
        self.emit_pop_r64("rbp")
        self.emit_ret()
    
    def add_data_string(self, name, text):
        offset = len(self.data)
        self.data += text.encode("utf-8") + b"\x00"
        self.add_symbol(
            name            = name,
            value           = offset,
            section_number  = 2
        )
        return offset
    
    def add_symbol(self, name, value, section_number=1):
        self.symbols.append({
            "name"      : name,
            "value"     : value,
            "section"   : section_number,
            "type"      : IMAGE_SYM_DTYPE_FUNCTION,
            "storage"   : IMAGE_SYM_CLASS_EXTERNAL,
            "aux"       : 0
        })
    
    # boolean
    def emit_normalize_bool_eax(self):
        self.emit_test_r32_r32("eax", "eax")
        self.emit_setcc_al("setne")
        self.emit_movzx_eax_al()
        
    def emit_bool_not_eax(self):
        self.emit_test_r32_r32("eax", "eax")
        self.emit_setcc_al("sete")
        self.emit_movzx_eax_al()
        
    def write_symbol(self, sym):
        name = sym["name"].encode("ascii")
        
        if len(name) <= 8:
            name_field = name.ljust(8, b"\x00")
        else:
            offset = self.get_string_offset(sym["name"])
            
            # Long name:
            # first 4 bytes = 0
            # next  4 bytes = offset into string table
            name_field = struct.pack("<II", 0, offset)
        
        return (
            name_field +
            struct.pack(
                "<IhHBB",
                sym["value"],
                sym["section"],
                sym["type"],
                sym["storage"],
                sym["aux"]
            )
        )
    
    def add_external_symbol(self, name):
        index = len(self.symbols)
        self.symbols.append({
            "name": name,
            "value": 0,
            "section": 0,
            "type": 0,
            "storage": IMAGE_SYM_CLASS_EXTERNAL,
            "aux": 0
        })
        return index

    def get_string_offset(self, name):
        if name in self.string_offsets:
            return self.string_offsets[name]

        # Offset zählt ab Anfang der String Table.
        # Die ersten 4 Bytes sind später die Größenangabe.
        offset = 4 + len(self.string_table)

        self.string_table += name.encode("ascii") + b"\x00"
        self.string_offsets[name] = offset

        return offset

    def find_symbol_index(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index
        return None

    def find_or_add_symbol(self, name):
        index = self.find_symbol_index(name)

        if index is None:
            raise RuntimeError(f"{tr('Symbol not defined')}: {name}")

        return index
    
    def find_or_add_external(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index
        
        return self.add_external_symbol(name)
    
    def write(self, filename):
        number_of_sections  = 2

        coff_header_size    = 20
        section_header_size = 40

        header_size = coff_header_size + number_of_sections * section_header_size
        
        text_size = len(self.text)
        data_size = len(self.data)
        
        text_ptr  = header_size
        data_ptr  = text_ptr + text_size
        
        text_reloc_ptr   = data_ptr + data_size
        text_reloc_count = len(self.text_relocations)
        text_reloc_size  = text_reloc_count * 10
        
        text_reloc_data  = bytearray()
        for reloc in self.text_relocations:
            text_reloc_data += struct.pack(
                "<IIH",
                reloc["offset"],
                reloc["symbol_index"],
                reloc["type"]
            )
        
        data_reloc_ptr   = text_reloc_ptr + text_reloc_size
        data_reloc_count = len(self.data_relocations)
        data_reloc_size  = data_reloc_count * 10
        
        data_reloc_data  = bytearray()
        for reloc in self.data_relocations:
            data_reloc_data += struct.pack(
                "<IIH",
                reloc["offset"],
                reloc["symbol_index"],
                reloc["type"]
            )
        
        symbol_table_ptr  = data_reloc_ptr + data_reloc_size
        number_of_symbols = len(self.symbols)

        coff_header = struct.pack(
            "<HHIIIHH",
            IMAGE_FILE_MACHINE_AMD64,
            number_of_sections,
            int(time.time()),
            symbol_table_ptr,
            number_of_symbols,
            0,
            0
        )
        
        text_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".text\x00\x00\x00",
            0,
            0,
            text_size,
            text_ptr,
            text_reloc_ptr if text_reloc_count else 0,
            0,
            text_reloc_count,
            0,
            IMAGE_SCN_CNT_CODE | IMAGE_SCN_MEM_EXECUTE | IMAGE_SCN_MEM_READ
        )

        data_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".data\x00\x00\x00",
            0,
            0,
            data_size,
            data_ptr if data_size else 0,
            data_reloc_ptr if data_reloc_count else 0,
            0,
            data_reloc_count,
            0,
            IMAGE_SCN_CNT_INITIALIZED_DATA | IMAGE_SCN_MEM_READ | IMAGE_SCN_MEM_WRITE
        )

        symbol_data = bytearray()
        for sym in self.symbols:
            symbol_data += self.write_symbol(sym)

        string_table = (
            struct.pack("<I", 4 + len(self.string_table)) +
            self.string_table
        )

        print("text_relocations:", self.text_relocations)
        print("text_reloc_count:", text_reloc_count)
        print("text_reloc_ptr:"  , text_reloc_ptr)
        
        self.check_unresolved_labels()
        
        with open(filename, "wb") as f:
            f.write(coff_header)
            f.write(text_section_header)
            f.write(data_section_header)
            
            f.write(self.text)
            f.write(self.data)
            
            f.write(text_reloc_data)
            f.write(data_reloc_data)
            
            f.write(symbol_data)
            f.write(string_table)
