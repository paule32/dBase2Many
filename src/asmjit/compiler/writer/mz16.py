# ---------------------------------------------------------------------------
# File: mz16.py - writer for dos 16 bit
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

# ---------------------------------------------------------------------------
# MS-DOS 16-Bit MZ executable writer ...
# ---------------------------------------------------------------------------
class MZ16Writer:
    def __init__(self):
        self.code   = bytearray()
        self.data   = bytearray()
        
        self.fixups = []
        self.labels = {}
        
        self.dos_for_end_symbol   = "__dos_for_end"
        
        self.dos_heap_pos_symbol  = "__dos_heap_pos"
        self.dos_heap_area_symbol = "__dos_heap_area"
        self.dos_heap_size        = 8192

    def bind_label(self, name):
        self.labels[name] = len(self.code)

        pending = [f for f in self.fixups if f["label"] == name]
        for fix in pending:
            self.patch_rel16(fix["patch_pos"], self.labels[name])

        self.fixups = [f for f in self.fixups if f["label"] != name]

    def emit_jmp(self, label):
        # near jmp rel16: E9 xx xx
        self.code.append(0xE9)

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        if label in self.labels:
            self.patch_rel16(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })

    def patch_rel16(self, patch_pos, target_pos):
        rel = target_pos - (patch_pos + 2)
        self.code[patch_pos:patch_pos + 2] = int(rel).to_bytes(
            2,
            "little",
            signed=True
        )
    
    def emit_mov_dx_label(self, label):
        self.code += b"\xBA"          # mov dx, imm16

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "data16",
            "patch_pos": patch_pos,
            "label": label
        })
    
    def emit_call_label(self, label):
        # near call rel16: E8 xx xx
        self.code.append(0xE8)

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        if label in self.labels:
            self.patch_rel16(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    def emit_print_string_current_dx(self):
        # DOS AH=09h erwartet DS:DX.
        # Unsere DOS-Strings liegen im Programmsegment.
        self.emit_push_cs_pop_ds()

        self.emit_mov_ah_imm8(0x09)
        self.emit_int(0x21)
    
    def emit_print_string(self, offset):
        self.emit_mov_dx_imm16(offset)
        self.emit_mov_ah_imm8(0x09)
        self.emit_int(0x21)
    
    def emit_print_newline(self):
        # CR
        self.emit_mov_dl_imm8(13)
        self.emit_mov_ah_imm8(0x02)
        self.emit_int(0x21)

        # LF
        self.emit_mov_dl_imm8(10)
        self.emit_mov_ah_imm8(0x02)
        self.emit_int(0x21)
        
    def emit_print_char_dl(self):
        self.emit_mov_ah_imm8(0x02)
        self.emit_int(0x21)

    def emit_print_int_ax(self):
        return_label = f"__print_int_done_{len(self.code)}"
        lbl_nonzero  = f"__print_int_nonzero_{len(self.code)}"

        # Spezialfall 0
        self.emit_cmp_reg16_imm16("ax", 0)
        self.emit_jne(lbl_nonzero)

        self.emit_mov_dl_imm8(ord("0"))
        self.emit_print_char_dl()
        self.emit_jmp(return_label)

        self.bind_label(lbl_nonzero)

        # cx = 0 ; digit counter
        self.emit_mov_reg16_imm16("cx", 0)

        # bx = 10
        self.emit_mov_reg16_imm16("bx", 10)

        div_loop   = f"__print_int_div_{len(self.code)}"
        print_loop = f"__print_int_print_{len(self.code)}"

        self.bind_label(div_loop)

        # dx = 0
        self.emit_mov_reg16_imm16("dx", 0)

        # div bx -> ax = ax / 10, dx = rest
        self.emit_div_reg16("bx")

        # Rest nach ASCII wandeln
        self.emit_add_dl_imm8(ord("0"))

        # Digit speichern
        self.emit_push_reg16("dx")

        # cx++
        self.emit_inc_reg16("cx")

        # solange ax != 0
        self.emit_cmp_reg16_imm16("ax", 0)
        self.emit_jne(div_loop)

        self.bind_label(print_loop)

        self.emit_pop_reg16("dx")
        self.emit_print_char_dl()

        self.emit_dec_reg16("cx")
        self.emit_cmp_reg16_imm16("cx", 0)
        self.emit_jne(print_loop)

        self.bind_label(return_label)
        
    def emit_mov_dl_imm8(self, value):
        self.code += b"\xB2"
        self.code.append(value & 0xFF)
    
    def emit_startup(self):
        self.emit_push_cs_pop_ds()
    
    def add_dos_string(self, name, text):
        offset            = len(self.data)
        self.labels[name] = offset
        self.data += text.encode("ascii", errors="replace") + b"$"
        return offset

    def emit_mov_ax_imm16(self, value):
        self.code += b"\xB8"
        self.code += int(value).to_bytes(2, "little")

    def emit_mov_dx_imm16(self, value):
        self.code += b"\xBA"
        self.code += int(value).to_bytes(2, "little")
    
    def emit_mov_ah_imm8(self, value):
        self.code += b"\xB4"
        self.code.append(value & 0xFF)
    
    def emit_int(self, value):
        self.code += b"\xCD"
        self.code.append(value & 0xFF)
    
    def emit_push_cs_pop_ds(self):
        self.code += b"\x0E"  # push cs
        self.code += b"\x1F"  # pop ds
    
    def emit_exit(self, code=0):
        self.emit_mov_ax_imm16(0x4C00 | (code & 0xFF))
        self.emit_int(0x21)
    
    def patch_data_fixups(self):
        data_base = len(self.code)
        
        for fix in self.fixups:
            if fix.get("kind") == "data16_disp":
                label = fix["label"]
                if label not in self.labels:
                    raise RuntimeError(f"{tr('unknown DOS data label')}: {label}")
                
                value = data_base + self.labels[label] + fix.get("disp", 0)
                self.code[fix["patch_pos"]:fix["patch_pos"] + 2] = int(value).to_bytes(
                    2,
                    "little",
                    signed = False
                )
                continue
                
            if fix.get("kind") != "data16":
                continue
            
            label = fix["label"]
            if label not in self.labels:
                raise RuntimeError(f"{tr('unknown DOS data label')}: {label}")
            
            value = data_base + self.labels[label]

            self.code[fix["patch_pos"]:fix["patch_pos"] + 2] = int(value).to_bytes(
                2,
                "little",
                signed=False
            )

    def _reg16_id(self, reg):
        regs = {
            "ax": 0,
            "cx": 1,
            "dx": 2,
            "bx": 3,
            "sp": 4,
            "bp": 5,
            "si": 6,
            "di": 7,
        }

        if reg not in regs:
            raise RuntimeError(f"{tr('unsupported 16-bit register')}: {reg}")

        return regs[reg]
    
    def emit_push_reg16(self, reg):
        op = {
            "ax": 0x50,
            "cx": 0x51,
            "dx": 0x52,
            "bx": 0x53,
            "sp": 0x54,
            "bp": 0x55,
            "si": 0x56,
            "di": 0x57,
        }

        if reg not in op:
            raise RuntimeError(f"{tr('unsupported 16-bit register')}: {reg}")

        self.code.append(op[reg])

    def emit_pop_reg16(self, reg):
        op = {
            "ax": 0x58,
            "cx": 0x59,
            "dx": 0x5A,
            "bx": 0x5B,
            "sp": 0x5C,
            "bp": 0x5D,
            "si": 0x5E,
            "di": 0x5F,
        }

        if reg not in op:
            raise RuntimeError(f"{tr('unsupported 16-bit register')}: {reg}")

        self.code.append(op[reg])

    def emit_mov_reg16_reg16(self, dst, src):
        reg_id = {
            "ax": 0,
            "cx": 1,
            "dx": 2,
            "bx": 3,
            "sp": 4,
            "bp": 5,
            "si": 6,
            "di": 7,
        }

        if dst not in reg_id:
            raise RuntimeError(f"{tr('unsupported dst register')}: {dst}")

        if src not in reg_id:
            raise RuntimeError(f"{tr('unsupported src register')}: {src}")

        # mov r/m16, r16
        self.code.append(0x89)
        self.code.append(0xC0 | (reg_id[src] << 3) | reg_id[dst])

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
            raise RuntimeError(f"{tr('unsupported DOS jcc')}: {cc}")

        self.code += opcodes[cc]

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        if label in self.labels:
            self.patch_rel16(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })

    def emit_je (self, label): self.emit_jcc("je",  label)
    def emit_jne(self, label): self.emit_jcc("jne", label)
    def emit_jz (self, label): self.emit_jcc("je",  label)
    def emit_jnz(self, label): self.emit_jcc("jne", label)

    def emit_jl (self, label): self.emit_jcc("jl",  label)
    def emit_jle(self, label): self.emit_jcc("jle", label)
    def emit_jg (self, label): self.emit_jcc("jg",  label)
    def emit_jge(self, label): self.emit_jcc("jge", label)

    def emit_cwd(self):
        # CWD: sign extend AX -> DX:AX
        self.code.append(0x99)

    def emit_idiv_reg16(self, reg):
        reg_id = self._reg16_id(reg)

        # idiv r/m16
        self.code.append(0xF7)
        self.code.append(0xF8 | reg_id)
    
    def emit_div_reg16(self, reg):
        reg_id = self._reg16_id(reg)

        # div r/m16
        self.code.append(0xF7)
        self.code.append(0xF0 | reg_id)

    def emit_inc_reg16(self, reg):
        reg_id = self._reg16_id(reg)
        self.code.append(0x40 + reg_id)

    def emit_dec_reg16(self, reg):
        reg_id = self._reg16_id(reg)
        self.code.append(0x48 + reg_id)

    def emit_add_dl_imm8(self, value):
        # add dl, imm8
        self.code += b"\x80\xC2"
        self.code.append(value & 0xFF)

    def emit_cmp_reg16_reg16(self, left, right):
        left_id  = self._reg16_id(left)
        right_id = self._reg16_id(right)

        # cmp r/m16, r16
        self.code.append(0x39)
        self.code.append(0xC0 | (right_id << 3) | left_id)
    
    def emit_cmp_reg16_imm16(self, reg, value):
        reg_id = self._reg16_id(reg)
        
        # cmp r/m16, imm16
        self.code.append(0x81)
        self.code.append(0xF8 | reg_id)
        self.code += int(value).to_bytes(2, "little", signed=True)
    
    def emit_sub_sp_imm16(self, value):
        if value <= 0:
            return
        
        self.code += b"\x81\xEC"
        self.code += int(value).to_bytes(2, "little", signed=False)

    def emit_add_sp_imm16(self, value):
        if value <= 0:
            return

        self.code += b"\x81\xC4"
        self.code += int(value).to_bytes(2, "little", signed=False)

    def emit_function_prolog(self, local_size=0):
        self.emit_push_reg16("bp")
        self.emit_mov_reg16_reg16("bp", "sp")

        if local_size:
            self.emit_sub_sp_imm16(local_size)

    def emit_function_epilog(self):
        self.emit_mov_reg16_reg16("sp", "bp")
        self.emit_pop_reg16("bp")
        self.emit_ret()

    def emit_ret(self):
        self.code.append(0xC3)

    def add_word_var(self, name, value=0):
        offset = len(self.data)
        self.labels[name] = offset
        self.data += int(value).to_bytes(2, "little", signed=True)
        return offset

    def emit_mov_reg16_imm16(self, reg, value):
        reg_id = self._reg16_id(reg)

        # mov r16, imm16
        self.code.append(0xB8 + reg_id)
        self.code += int(value).to_bytes(2, "little", signed=True)

    def emit_mov_mem16_reg16(self, label, reg):
        reg_id = self._reg16_id(reg)

        # mov [imm16], r16
        self.code.append(0x89)
        self.code.append(0x06 | (reg_id << 3))

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "data16",
            "patch_pos": patch_pos,
            "label": label
        })

    def emit_mov_reg16_mem16(self, reg, label):
        reg_id = self._reg16_id(reg)

        # mov r16, [imm16]
        self.code.append(0x8B)
        self.code.append(0x06 | (reg_id << 3))

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "data16",
            "patch_pos": patch_pos,
            "label": label
        })
    
    def emit_mov_reg16_mem16_base_disp(self, dst, base, offset):
        dst_id  = self._reg16_id(dst)

        if base == "si":
            rm = 0x04          # [si]
        elif base == "bp":
            rm = 0x06          # [bp + disp]
        else:
            raise RuntimeError(f"{tr('DOS16 memory base not supported yet')}: {base}")

        # mov r16, r/m16
        self.code.append(0x8B)

        # [si] rm = 100
        if offset == 0 and base != "bp":
            self.code.append(0x00 | (dst_id << 3) | rm)

        elif -128 <= offset <= 127:
            self.code.append(0x40 | (dst_id << 3) | rm)
            self.code.append(offset & 0xFF)
        else:
            self.code.append(0x80 | (dst_id << 3) | rm)
            self.code += int(offset).to_bytes(2, "little", signed=True)
    
    def emit_mov_reg16_mem16_disp(self, reg, label, disp):
        if not isinstance(label, str):
            raise RuntimeError(f"{tr('emit_mov_reg16_mem16_disp: label must be str, got')} {label!r}")
            
        reg_id = self._reg16_id(reg)

        # mov r16, [imm16]
        self.code.append(0x8B)
        self.code.append(0x06 | (reg_id << 3))

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "data16_disp",
            "patch_pos": patch_pos,
            "label": label,
            "disp": disp
        })
    
    def emit_imul_reg16_reg16(self, dst, src):
        dst_id = self._reg16_id(dst)
        src_id = self._reg16_id(src)

        # 0F AF /r  => imul r16, r/m16
        self.code += b"\x0F\xAF"
        self.code.append(0xC0 | (dst_id << 3) | src_id)

    def emit_imul_reg16_reg16_imm16(self, dst, src, value):
        dst_id = self._reg16_id(dst)
        src_id = self._reg16_id(src)

        # 69 /r iw => imul r16, r/m16, imm16
        self.code.append(0x69)
        self.code.append(0xC0 | (dst_id << 3) | src_id)
        self.code += int(value).to_bytes(2, "little", signed=True)

    def emit_xor_reg16_reg16(self, dst, src):
        dst_id = self._reg16_id(dst)
        src_id = self._reg16_id(src)

        # xor r/m16, r16
        self.code.append(0x31)
        self.code.append(0xC0 | (src_id << 3) | dst_id)
    
    def emit_add_reg16_imm16(self, reg, value):
        reg_id = self._reg16_id(reg)

        self.code.append(0x81)
        self.code.append(0xC0 | reg_id)
        self.code += int(value).to_bytes(2, "little", signed=True)

    def emit_sub_reg16_imm16(self, reg, value):
        reg_id = self._reg16_id(reg)

        self.code.append(0x81)
        self.code.append(0xE8 | reg_id)
        self.code += int(value).to_bytes(2, "little", signed=True)

    def emit_add_reg16_reg16(self, dst, src):
        dst_id = self._reg16_id(dst)
        src_id = self._reg16_id(src)

        self.code.append(0x01)
        self.code.append(0xC0 | (src_id << 3) | dst_id)

    def emit_sub_reg16_reg16(self, dst, src):
        dst_id = self._reg16_id(dst)
        src_id = self._reg16_id(src)

        self.code.append(0x29)
        self.code.append(0xC0 | (src_id << 3) | dst_id)

    def emit_test_reg16_reg16(self, left, right):
        left_id  = self._reg16_id(left)
        right_id = self._reg16_id(right)

        # test r/m16, r16
        self.code.append(0x85)
        self.code.append(0xC0 | (right_id << 3) | left_id)
    
    def emit_mov_mem16_reg16_disp(self, label, disp, reg):
        if not isinstance(label, str):
            raise RuntimeError(
                f"{tr('emit_mov_mem16_reg16_disp: label must be str, got')} {label!r}"
            )
        reg_id = self._reg16_id(reg)

        # mov [imm16], r16
        self.code.append(0x89)
        self.code.append(0x06 | (reg_id << 3))

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "data16_disp",
            "patch_pos": patch_pos,
            "label": label,
            "disp": disp
        })
    
    def emit_mov_mem16_base_disp_reg16(self, base, offset, src):
        src_id = self._reg16_id(src)

        if base == "si":
            rm = 0x04          # [si]
        elif base == "bp":
            rm = 0x06          # [bp + disp]
        else:
            raise RuntimeError(f"{tr('DOS16 memory base not supported yet')}: {base}")

        self.code.append(0x89) # mov r/m16, r16

        # Achtung:
        # [bp] ohne Displacement wäre im 16-bit Encoding eigentlich [disp16].
        # Darum bei bp und offset == 0 trotzdem disp8=0 verwenden.
        if offset == 0 and base != "bp":
            self.code.append(0x00 | (src_id << 3) | rm)

        elif -128 <= offset <= 127:
            self.code.append(0x40 | (src_id << 3) | rm)
            self.code.append(offset & 0xFF)

        else:
            self.code.append(0x80 | (src_id << 3) | rm)
            self.code += int(offset).to_bytes(2, "little", signed=True)

    def add_bytes_var(self, name, data):
        offset = len(self.data)
        self.labels[name] = offset
        self.data += data
        return offset

    def ensure_dos_heap(self):
        if self.dos_heap_pos_symbol not in self.labels:
            self.add_word_var(self.dos_heap_pos_symbol, 2)

        if self.dos_heap_area_symbol not in self.labels:
            self.add_bytes_var(
                self.dos_heap_area_symbol,
                b"\x00" * self.dos_heap_size
            )

    def emit_mov_ax_data_label(self, label):
        self.code.append(0xB8)

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "data16",
            "patch_pos": patch_pos,
            "label": label
        })
    
    def add_dword_var(self, name, value=0):
        offset = len(self.data)
        self.labels[name] = offset
        self.data += int(value).to_bytes(4, "little", signed=False)
        return offset

    def emit_mov_es_reg16(self, reg):
        reg_id = self._reg16_id(reg)

        # mov Sreg, r/m16
        # ES = 0
        self.code.append(0x8E)
        self.code.append(0xC0 | (0 << 3) | reg_id)

    def emit_mov_bx_imm16(self, value):
        self.emit_mov_reg16_imm16("bx", value)

    def emit_jc(self, label):
        self.emit_jcc_rel16(0x82, label)   # JC/JB/NAE

    def emit_clc(self):
        self.code.append(0xF8)
        
    def emit_jcc_rel16(self, opcode, label):
        self.code += b"\x0F"
        self.code.append(opcode)

        patch_pos = len(self.code)
        self.code += b"\x00\x00"

        self.fixups.append({
            "kind": "rel16",
            "patch_pos": patch_pos,
            "label": label
        })

    def ensure_dos_heap_symbols(self):
        if "__heap_initialized" not in self.labels:
            self.add_word_var("__heap_initialized", 0)
        
        if "__heap_segment" not in self.labels:
            self.add_word_var("__heap_segment", 0)

        if "__heap_size" not in self.labels:
            self.add_word_var("__heap_size", 0)

        if "__heap_free_head_off" not in self.labels:
            self.add_word_var("__heap_free_head_off", 0)

        if "__heap_free_head_seg" not in self.labels:
            self.add_word_var("__heap_free_head_seg", 0)
            
        if "__heap_next" not in self.labels:
            self.add_word_var("__heap_next", 0)

    def emit_ja(self, label):
        self.emit_jcc_rel16(0x87, label)

    def emit_heap_init(self, paragraphs=0x40):
        self.ensure_dos_heap_symbols()

        fail_label = f"__heap_init_fail_{len(self.code)}"
        done_label = f"__heap_init_done_{len(self.code)}"

        already_label = f"__heap_init_already_{len(self.code)}"
        
        self.emit_mov_reg16_mem16("ax", "__heap_initialized")
        self.emit_cmp_reg16_imm16("ax", 1)
        self.emit_je(already_label)
        
        # AH = 48h, BX=Paragraphen
        self.emit_mov_ah_imm8(0x48)
        self.emit_mov_reg16_imm16("bx", paragraphs)
        self.emit_int(0x21)

        # CF gesetzt => Fehler
        self.emit_jc(fail_label)
        
        self.emit_mov_reg16_imm16("bx", 1)
        self.emit_mov_mem16_reg16("__heap_initialized", "bx")

        # AX = Heap-Segment
        self.emit_mov_mem16_reg16("__heap_segment", "ax")
        self.emit_mov_reg16_imm16("bx", paragraphs)
        self.emit_mov_mem16_reg16("__heap_size", "bx")

        # FreeList Head = Offset 0, Segment AX
        self.emit_mov_reg16_imm16("dx", 0)
        self.emit_mov_mem16_reg16("__heap_free_head_off", "dx")
        self.emit_mov_mem16_reg16("__heap_free_head_seg", "ax")

        # erster freier Offset im Heap
        self.emit_mov_reg16_imm16("bx", 0)
        self.emit_mov_mem16_reg16("__heap_next", "bx")

        self.emit_jmp(done_label)
        self.bind_label(fail_label)

        msg_label = "__msg_heap_init_failed"
        self.add_dos_string(msg_label, "HeapInit failed")

        self.emit_mov_dx_label(msg_label)
        self.emit_print_string_current_dx()
        self.emit_print_newline()
        self.emit_exit(1)

        self.bind_label(already_label)
        self.bind_label(done_label)

    # ---------------------------------------------------------------------------
    #  Input:
    #     AX = gewünschte Größe in Bytes
    #
    #  Output:
    #     AX = Offset im Heap
    #     DX = Heap-Segment
    #     AX = 0/DX = 0 bei Fehler
    # ---------------------------------------------------------------------------
    def emit_heap_alloc(self):
        fail_label = f"__heap_alloc_fail_{len(self.code)}"
        done_label = f"__heap_alloc_done_{len(self.code)}"

        # BX = size + header
        self.emit_mov_reg16_reg16("bx", "ax")
        self.emit_add_reg16_imm16("bx", 4)

        # Größe auf gerade Zahl runden
        self.emit_add_reg16_imm16("bx", 1)
        # bx &= 0xFFFE fehlt noch -> einfache Version:
        # vorerst nur WORD-ausgerichtete Größen vom Generator übergeben

        # AX = heap_next
        self.emit_mov_reg16_mem16("ax", "__heap_next")

        # CX = alter heap_next = Rückgabe-Offset
        self.emit_mov_reg16_reg16("cx", "ax")

        # AX = heap_next + size
        self.emit_add_reg16_reg16("ax", "bx")

        # Prüfen gegen Heapgröße in Bytes
        # DX = paragraphs
        self.emit_mov_reg16_mem16("dx", "__heap_size")

        # DX = paragraphs * 16
        self.emit_shl_reg16_imm8("dx", 4)

        # Sicherheitsreserve: 16 Bytes am Ende lassen
        self.emit_sub_reg16_imm16("dx", 16)

        self.emit_cmp_reg16_reg16("ax", "dx")
        self.emit_ja(fail_label)

        # heap_next = AX
        self.emit_mov_mem16_reg16("__heap_next", "ax")

        # Rückgabe:
        # AX = alter Offset
        # DX = Heap-Segment
        self.emit_mov_reg16_reg16("ax", "cx")
        self.emit_add_reg16_imm16("ax", 4)
        self.emit_mov_reg16_mem16("dx", "__heap_segment")

        self.emit_jmp(done_label)

        self.bind_label(fail_label)

        self.emit_mov_reg16_imm16("ax", 0)
        self.emit_mov_reg16_imm16("dx", 0)

        self.bind_label(done_label)

    # ---------------------------------------------------------------------------
    #  Input:
    #    AX = Nutzdaten-Offset
    #    DX = Heap-Segment
    #
    #  Fügt Block vorne in FreeList ein.
    #  BlockHeader liegt bei AX - 4.
    # ---------------------------------------------------------------------------
    def emit_heap_free(self):
        done_label = f"__heap_free_done_{len(self.code)}"

        # nil?
        self.emit_cmp_reg16_imm16("dx", 0)
        self.emit_je(done_label)

        self.emit_cmp_reg16_imm16("ax", 0)
        self.emit_je(done_label)

        # BX = block header offset = AX - 4
        self.emit_mov_reg16_reg16("bx", "ax")
        self.emit_sub_reg16_imm16("bx", 4)

        # ES = Heap-Segment
        self.emit_mov_es_reg16("dx")

        # [ES:BX+2] = __heap_free_head_off
        self.emit_mov_reg16_mem16("cx", "__heap_free_head_off")
        self.emit_mov_mem16_es_bx_disp_reg16(2, "cx")

        # __heap_free_head_off = BX
        self.emit_mov_mem16_reg16("__heap_free_head_off", "bx")

        # __heap_free_head_seg = DX
        self.emit_mov_mem16_reg16("__heap_free_head_seg", "dx")

        self.bind_label(done_label)

    def emit_shl_reg16_imm8(self, reg, value):
        reg_id = self._reg16_id(reg)

        # C1 /4 ib  => shl r/m16, imm8
        self.code.append(0xC1)
        self.code.append(0xE0 | reg_id)
        self.code.append(value & 0xFF)

    def emit_mov_mem16_es_bx_disp_reg16(self, disp, src):
        src_id = self._reg16_id(src)

        # ES override
        self.code.append(0x26)

        # mov [bx+disp], r16
        self.code.append(0x89)

        if disp == 0:
            self.code.append(0x07 | (src_id << 3))  # [bx]
        elif -128 <= disp <= 127:
            self.code.append(0x47 | (src_id << 3))  # [bx+disp8]
            self.code.append(disp & 0xFF)
        else:
            self.code.append(0x87 | (src_id << 3))  # [bx+disp16]
            self.code += int(disp).to_bytes(2, "little", signed=True)

    def emit_mov_reg16_ds(self, reg):
        reg_id = self._reg16_id(reg)

        # mov r/m16, Sreg
        # DS = Segmentregister 3
        self.code.append(0x8C)
        self.code.append(0xC0 | (3 << 3) | reg_id)

    def write(self, filename):
        code_size         =  len(self.code)
        data_size         =  len(self.data)
        
        HEADER_PARAGRAPHS = 4
        HEADER_SIZE       = HEADER_PARAGRAPHS * 16   # 64 Byte
        image_size        = HEADER_SIZE + len(self.code) + len(self.data)
        
        if self.dos_for_end_symbol not in self.labels:
            self.add_word_var(self.dos_for_end_symbol, 0)
        
        #self.ensure_dos_heap()
        self.patch_data_fixups()

        last_page_bytes   =  image_size % 512
        page_count        = (image_size + 511) // 512
        
        if  last_page_bytes == 0:
            last_page_bytes = 512

        header = struct.pack(
            "<14H",
            0x5A4D,               # "MZ"
            last_page_bytes,      # Bytes der letzten Seite
            page_count,           # Seiten im File
            0,                    # e_crlc
            HEADER_PARAGRAPHS,    # header paragraphs (4 * 16 = 64)
            0x1000,               # min alloc
            0x1000,               # max alloc
            0,                    # SS
            0x8000,               # SP
            0,                    # checksum
            0,                    # IP
            0,                    # CS
            0x40,                 # reloc table
            0                     # overlay number
        )

        with open(filename, "wb") as f:
            f.write(header)
            
            if len(header) < HEADER_SIZE:
                f.write(b"\x00" * (HEADER_SIZE - len(header)))
                
            f.write(self.code)
            f.write(self.data)
