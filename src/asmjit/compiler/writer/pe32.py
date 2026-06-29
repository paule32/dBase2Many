# ---------------------------------------------------------------------------
# File: pe32.py - writer for pe32
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.common.constants import *
from compiler.writer.nt32      import *

import struct

def double_to_bits(value):
    return struct.unpack(
        "<Q",
        struct.pack("<d", float(value))
    )[0]

# ---------------------------------------------------------------------------
# Windows NT 3.5 PE COFF object/code writer
# ---------------------------------------------------------------------------
class PE32Writer:
    def __init__(self):
        self.regs = {
            "eax": 0,
            "ecx": 1,
            "edx": 2,
            "ebx": 3,
            "esp": 4,
            "ebp": 5,
            "esi": 6,
            "edi": 7,
        }
        
        self.text = bytearray()
        self.data = bytearray()

        self.labels = {}
        self.fixups = []

        self.symbols = []
        self.text_relocations = []
        self.data_relocations = []

        self.string_table = bytearray()
        self.string_offsets = {}

    def begin_function(self, name, local_size=0, public=True):
        offset = len(self.text)

        self.bind_label(name)

        if self.find_symbol_index(name) is None:
            self.add_symbol(
                name=name,
                value=offset,
                section_number=1
            )

        # Für NT32 erst schlicht:
        # push ebp
        # mov  ebp, esp
        self.emit_push_reg32("ebp")
        self.emit_mov_reg_reg32("ebp", "esp")

        if local_size:
            self.emit_sub_reg_imm32("esp", local_size)

        return offset
    
    def end_function(self):
        self.emit_mov_reg_reg32("esp", "ebp")
        self.emit_pop_reg32("ebp")
        self.emit_ret()

    def _reg_id(self, reg):
        if reg not in self.regs:
            raise RuntimeError(f"{tr('unsupported 32-bit register')}: {reg}")
        return self.regs[reg]

    def bind_label(self, name):
        self.labels[name] = len(self.text)
        
        idx = self.find_symbol_index(name)
        if idx is None:
            self.add_symbol(name, len(self.text), section_number=1)
        else:
            self.symbols[idx]["value"] = len(self.text)
            self.symbols[idx]["section"] = 1

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

    def patch_rel32(self, patch_pos, target_pos):
        rel = target_pos - (patch_pos + 4)
        self.text[patch_pos:patch_pos + 4] = int(rel).to_bytes(
            4,
            "little",
            signed=True
        )

    def emit_push_imm32(self, value):
        self.text.append(0x68)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_push_reg32(self, reg):
        reg_id = self._reg_id(reg)
        self.text.append(0x50 + reg_id)

    def emit_pop_reg32(self, reg):
        reg_id = self._reg_id(reg)
        self.text.append(0x58 + reg_id)

    def emit_mov_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)
        self.text.append(0xB8 + reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_xor_reg_reg(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        self.text.append(0x31)
        self.text.append(0xC0 | (src_id << 3) | dst_id)

    def emit_ret(self):
        self.text.append(0xC3)

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
    
    def emit_jmp(self, label):
        self.text.append(0xE9)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })

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

    def emit_je(self, label):  self.emit_jcc("je",  label)
    def emit_jne(self, label): self.emit_jcc("jne", label)
    def emit_jl(self, label):  self.emit_jcc("jl",  label)
    def emit_jle(self, label): self.emit_jcc("jle", label)
    def emit_jg(self, label):  self.emit_jcc("jg",  label)
    def emit_jge(self, label): self.emit_jcc("jge", label)
    
    def emit_call_external(self, symbol_name):
        if symbol_name in ["rax", "eax", "rbx", "ebx", "rcx", "ecx", "rdx", "edx"]:
            raise RuntimeError(f"{tr('register passed to emit_call_external')}: {symbol_name}")
        
        sym_index = self.find_or_add_external(symbol_name)

        self.text.append(0xE8)          # call rel32
        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_REL32
        })

    def add_symbol(self, name, value, section_number=1):
        self.symbols.append({
            "name": name,
            "value": value,
            "section": section_number,
            "type": 0x20,
            "storage": IMAGE_SYM_CLASS_EXTERNAL,
            "aux": 0
        })

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

    def add_data_string(self, name, text):
        offset = len(self.data)
        self.data += text.encode("ascii", errors="replace") + b"\x00"

        self.add_symbol(
            name=name,
            value=offset,
            section_number=2
        )

        return offset

    def add_data_i32(self, name, value=0):
        return self.add_data_bytes(
            name,
            int(value).to_bytes(4, "little", signed=True),
            alignment=4
        )

    def add_data_zeros(self, name, size, alignment=4):
        return self.add_data_bytes(
            name,
            b"\x00" * size,
            alignment=alignment
        )

    def align_data(self, alignment):
        while len(self.data) % alignment != 0:
            self.data.append(0)

    def add_data_bytes(self, name, data_bytes, alignment=1):
        self.align_data(alignment)

        offset = len(self.data)
        self.data += data_bytes

        self.add_symbol(
            name=name,
            value=offset,
            section_number=2
        )

        return offset
    
    def emit_mov_reg_reg32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # mov r/m32, r32
        self.text.append(0x89)
        self.text.append(0xC0 | (src_id << 3) | dst_id)
    
    def emit_sub_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        # sub r/m32, imm32
        self.text.append(0x81)
        self.text.append(0xE8 | reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_sub_reg_reg32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # sub r/m32, r32
        self.text.append(0x29)
        self.text.append(0xC0 | (src_id << 3) | dst_id)

    def emit_add_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        # add r/m32, imm32
        self.text.append(0x81)
        self.text.append(0xC0 | reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_add_reg_reg32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # add r/m32, r32
        self.text.append(0x01)
        self.text.append(0xC0 | (src_id << 3) | dst_id)

    def find_symbol_index(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index

        return None
    
    def emit_mov_reg_data_label32(self, reg, label):
        reg_id    = self._reg_id(reg)
        sym_index = self.find_or_add_symbol(label)

        # mov r32, imm32
        self.text.append(0xB8 + reg_id)

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })

    def _emit_modrm_mem32(self, reg_id, base_id, offset=0):
        rm = base_id & 7

        needs_sib  = rm == 4          # esp
        needs_disp = rm == 5 and offset == 0  # ebp braucht disp8=0

        if offset == 0 and not needs_disp:
            mod = 0x00
        elif -128 <= offset <= 127:
            mod = 0x40
        else:
            mod = 0x80

        if needs_disp:
            mod = 0x40
            offset = 0

        if needs_sib:
            self.text.append(mod | ((reg_id & 7) << 3) | 0x04)
            self.text.append(0x24)  # scale=0,index=none,base=esp
        else:
            self.text.append(mod | ((reg_id & 7) << 3) | rm)

        if mod == 0x40:
            self.text.append(offset & 0xFF)
        elif mod == 0x80:
            self.text += int(offset).to_bytes(4, "little", signed=True)
    
    def emit_mov_mem_reg32(self, base, offset, src):
        base_id = self._reg_id(base)
        src_id  = self._reg_id(src)

        self.text.append(0x89)  # mov r/m32, r32
        self._emit_modrm_mem32(src_id, base_id, offset)
    
    def emit_mov_mem_reg32(self, base, offset, src):
        base_id = self._reg_id(base)
        src_id  = self._reg_id(src)

        self.text.append(0x89)
        self._emit_modrm_mem32(src_id, base_id, offset)
    
    def emit_mov_reg_mem32(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        self.text.append(0x8B)  # mov r32, r/m32
        self._emit_modrm_mem32(dst_id, base_id, offset)
    
    def emit_mov_data_label_r32(self, label, src):
        src_id    = self._reg_id(src)
        sym_index = self.find_or_add_symbol(label)

        # mov r/m32, r32
        # absoluter Speicherzugriff: [imm32]
        self.text.append(0x89)
        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })
    
    def emit_mov_r32_data_label(self, dst, label):
        return self.emit_mov_reg_data_label32(dst, label)
    
    def emit_imul_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # imul r32, r/m32
        self.text += b"\x0F\xAF"
        self.text.append(0xC0 | (dst_id << 3) | src_id)

    def emit_imul_r32_r32_imm32(self, dst, src, value):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        # imul r32, r/m32, imm32
        self.text.append(0x69)
        self.text.append(0xC0 | (dst_id << 3) | src_id)
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_imul(self, dst, src, value=None):
        if value is None:
            self.emit_imul_r32_r32(dst, src)
        else:
            self.emit_imul_r32_r32_imm32(dst, src, value)
    
    def emit_cdq(self):
        # CDQ: EDX:EAX vorbereiten für IDIV
        self.text.append(0x99)

    def emit_idiv_r32(self, reg):
        reg_id = self._reg_id(reg)

        # idiv r/m32
        self.text.append(0xF7)
        self.text.append(0xF8 | reg_id)
    
    def emit_cmp_reg_reg32(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        # cmp r/m32, r32
        self.text.append(0x39)
        self.text.append(0xC0 | (right_id << 3) | left_id)

    def emit_cmp_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        # cmp r/m32, imm32
        self.text.append(0x81)
        self.text.append(0xF8 | reg_id)
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_setne(self, reg):
        if reg != "al":
            raise RuntimeError(tr("PE32Writer.emit_setne currently supports only al"))

        # setne al
        self.text += b"\x0F\x95\xC0"
    
    def emit_movzx(self, dst, src, comment=""):
        self.writer.emit_movzx_r32_r8(
            self.map_reg32(dst),
            self.map_reg8(src)
        )

    def emit_movzx_r32_r8(self, dst, src):
        dst_id = self._reg_id(dst)

        reg8 = {
            "al": 0,
            "cl": 1,
            "dl": 2,
            "bl": 3,
        }

        if src not in reg8:
            raise RuntimeError(f"{tr('unsupported 8-bit source register')}: {src}")

        # movzx r32, r/m8
        self.text += b"\x0F\xB6"
        self.text.append(0xC0 | (dst_id << 3) | reg8[src])
    
    def emit_mov_r64_data_label(self, dst, label):
        # NT32: r64-Aufruf vom gemeinsamen Generator auf r32 abbilden
        return self.emit_mov_r32_data_label(
            self._map_reg64_to_32(dst),
            label
        )

    def emit_mov_data_label_r64(self, label, src):
        # NT32: Pointer/String/Object-Handles sind 32-bit
        return self.emit_mov_data_label_r32(
            label,
            self._map_reg64_to_32(src)
        )

    def _map_reg64_to_32(self, reg):
        reg_map = {
            "rax": "eax",
            "rbx": "ebx",
            "rcx": "ecx",
            "rdx": "edx",
            "rsi": "esi",
            "rdi": "edi",
            "rbp": "ebp",
            "rsp": "esp",
        }

        return reg_map.get(reg, reg)
    
    def emit_test_reg_reg32(self, reg1, reg2):
        r1 = self._reg_id(reg1)
        r2 = self._reg_id(reg2)

        # test r/m32, r32
        self.text.append(0x85)
        self.text.append(0xC0 | (r2 << 3) | r1)
    
    def emit_call_reg32(self, reg):
        reg_id = self._reg_id(reg)

        # call r/m32
        self.text.append(0xFF)
        self.text.append(0xD0 | reg_id)
    
    def emit_push_data_label32(self, label):
        sym_index = self.find_or_add_symbol(label)

        self.text.append(0x68)  # push imm32

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })
    
    def emit_fstp_qword_ptr_esp(self):
        # fstp qword [esp]
        self.text += b"\xDD\x1C\x24"
    
    def emit_movsd_qword_ptr_esp_xmm0(self):
        # movsd qword [esp], xmm0
        self.text += b"\xF2\x0F\x11\x04\x24"
    
    def add_data_double(self, name, value):
        bits = double_to_bits(value)
        return self.add_data_bytes(
            name,
            int(bits).to_bytes(8, "little", signed=False),
            alignment=8
        )

    def emit_movsd_xmm0_data_label32(self, label):
        sym_index = self.find_or_add_symbol(label)

        # movsd xmm0, qword ptr [imm32]
        self.text += b"\xF2\x0F\x10\x05"

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })
    
    def _xmm_id(self, reg):
        xmm = {
            "xmm0": 0,
            "xmm1": 1,
        }
        if reg not in xmm:
            raise RuntimeError(f"{tr('unsupported NT32 xmm register')}: {reg}")
        return xmm[reg]

    def emit_movsd_store32(self, base, offset, src):
        src_id = self._xmm_id(src)
        self.text += b"\xF2\x0F\x11"
        self._emit_modrm_mem32(src_id, self._reg_id(base), offset)

    def emit_movsd_load32(self, dst, base, offset=0):
        dst_id = self._xmm_id(dst)
        self.text += b"\xF2\x0F\x10"
        self._emit_modrm_mem32(dst_id, self._reg_id(base), offset)
    
    def emit_cvtsi2sd32(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._reg_id(src)

        # cvtsi2sd xmm, r/m32
        self.text += b"\xF2\x0F\x2A"
        self.text.append(0xC0 | (dst_id << 3) | src_id)

    def emit_sse2_xmm_xmm32(self, opcode, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._xmm_id(src)

        # addsd/subsd/mulsd/divsd xmm, xmm
        self.text += b"\xF2\x0F"
        self.text.append(opcode)
        self.text.append(0xC0 | (dst_id << 3) | src_id)

    def emit_mov_reg_from_data_label32(self, reg, label):
        reg_id    = self._reg_id(reg)
        sym_index = self.find_or_add_symbol(label)

        # mov r32, dword ptr [imm32]
        self.text.append(0x8B)
        self.text.append(0x05 | (reg_id << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })

    def emit_lea_reg_data_label(self, reg, label):
        # NT32: Adresse eines Datenlabels in Register laden
        # mov reg, imm32 + DIR32 relocation
        self.emit_mov_reg_data_label32(reg, label)

    def add_data_i32_symbol_ref(self, target_symbol):
        sym_index = self.find_or_add_symbol(target_symbol)
        offset = len(self.data)
        self.data += b"\x00\x00\x00\x00"

        self.data_relocations.append({
            "offset": offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_I386_DIR32
        })

        return offset

    #def has_symbol(self, name):
    #    for sym in self.symbols:
    #        if sym.name == name:
    #            return True
    #    return False
    
    def has_symbol(self, name):
        for sym in self.symbols:
            if isinstance(sym, dict):
                if sym.get("name") == name:
                    return True
            else:
                if getattr(sym, "name", None) == name:
                    return True
        return False

    def add_data_label(self, name):
        self.add_symbol(
            name,
            2, #self.data_section_number,
            len(self.data)
        )

    def ensure_data_symbol_block(self, name, size):
        if not self.has_symbol(name):
            self.add_data_bytes(name, b"\x00" * size, alignment=4)
        
    def add_jit_context32(self, name="ctx"):
        #self.ensure_data_symbol_block("int_vars",    4 * max( 1, self.required_int_slots))
        #self.ensure_data_symbol_block("double_vars", 8 * max( 1, self.required_double_slots))
        #self.ensure_data_symbol_block("string_vars", 4 * max( 1, self.required_string_slots))
        #self.ensure_data_symbol_block("record_vars",     max(16, self.required_record_bytes))
        #self.ensure_data_symbol_block("arrays_vars",     max(16, self.required_array_bytes))
        #self.ensure_data_symbol_block("pointr_vars", 4 * max( 1, self.required_pointer_slots))
        
        self.ensure_data_symbol_block("int_vars", 16)
        self.ensure_data_symbol_block("double_vars", 16)
        self.ensure_data_symbol_block("string_vars", 16)
        self.ensure_data_symbol_block("record_vars", 64)
        self.ensure_data_symbol_block("arrays_vars", 64)
        self.ensure_data_symbol_block("pointr_vars", 16)

        self.align_data(4)
        ctx_offset = len(self.data)

        self.add_symbol(
            name=name,
            value=ctx_offset,
            section_number=2
        )

        self.add_data_i32_symbol_ref("int_vars")
        self.add_data_i32_symbol_ref("double_vars")
        self.add_data_i32_symbol_ref("string_vars")
        self.add_data_i32_symbol_ref("record_vars")
        self.add_data_i32_symbol_ref("arrays_vars")
        self.add_data_i32_symbol_ref("pointr_vars")

        self.data += b"\x00" * 4   # print_int_tmp
        self.data += b"\x00" * 8   # print_double_tmp

        return ctx_offset

    def pointer_slot_size(self):
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                return 4
            return 8

    def write(self, filename):
        NT32Writer(self).write(filename)
