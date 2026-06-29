# ---------------------------------------------------------------------------
# File: dos16.py - backend for dos16
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.backend.code     import *

# ---------------------------------------------------------------------------
# MS-DOS 16-Bit backend ...
# ---------------------------------------------------------------------------
class DOS16Backend(CodeBackend):
    def __init__(self, writer=None):
        super().__init__(CDATA.args_backend)

        self.REG_MAP = {
            "rax": "ax", "eax": "ax", "ax": "ax",
            "rbx": "bx", "ebx": "bx", "bx": "bx",
            "rcx": "cx", "ecx": "cx", "cx": "cx",
            "rdx": "dx", "edx": "dx", "dx": "dx",

            "rbp": "bp", "ebp": "bp", "bp": "bp",
            "rsp": "sp", "esp": "sp", "sp": "sp",

            "rsi": "si", "esi": "si", "si": "si",
            "rdi": "di", "edi": "di", "di": "di",
        }
        
        self.pending_call = None
        self.writer       = writer
        self.lines        = ""
    
    def emit_add(self, dst, value, comment=""):
        dst16 = self.map_reg(dst)

        if isinstance(value, str) and value.lstrip("-").isdigit():
            value = int(value)

        if isinstance(value, int):
            self.writer.emit_add_reg16_imm16(dst16, value)
            return

        self.writer.emit_add_reg16_reg16(dst16, self.map_reg(value))

    def emit_sub(self, dst, value, comment=""):
        dst16 = self.map_reg(dst)

        if isinstance(value, str) and value.lstrip("-").isdigit():
            value = int(value)

        if isinstance(value, int):
            self.writer.emit_sub_reg16_imm16(dst16, value)
            return

        self.writer.emit_sub_reg16_reg16(dst16, self.map_reg(value))
    
    def emit_new_label_decl(self, name, comment=""):
        # DOS/MZ braucht keine Vorab-Label-Deklaration
        return

    def emit_bind_label(self, label, comment=""):
        self.writer.bind_label(label)

    def emit_jmp(self, label, comment=""):
        self.writer.emit_jmp(label)

    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        # Win64: mov eax, dword [rax + offset]
        # DOS16: mov si, ax / mov ax, word [si + offset]

        dst16  = self.map_reg(dst)
        base16 = self.map_reg(base)

        if base16 != "si":
            self.writer.emit_mov_reg16_reg16("si", base16)
            base16 = "si"

        self.writer.emit_mov_reg16_mem16_base_disp(
            dst16,
            base16,
            int(offset)
        )

    def emit_mov_imm(self, dst, value, comment=""):
        if isinstance(value, str) and value == "&_jit_runtime_error":
            self.pending_call = "_dos_runtime_error"
            return
            
        if isinstance(value, str) and value == "&_jit_print_int":
            self.pending_call = "_dos_print_int"
            return
            
        if isinstance(value, str) and value == "&_jit_print_text":
            self.pending_call = "_dos_print_text"
            return

        if isinstance(value, str) and value == "&_jit_print_newline":
            self.pending_call = "_dos_print_newline"
            return

        if dst in ("rcx", "ecx", "cx") and isinstance(value, str):
            self.writer.emit_mov_dx_label(value)
            return

        if isinstance(value, str) and value.lstrip("-").isdigit():
            value = int(value)

        if dst in ("rax", "eax", "ax") and isinstance(value, int):
            self.writer.emit_mov_ax_imm16(value)
            return

        raise NotImplementedError(f"{tr('DOS emit_mov_imm')} {dst}, {value}")

    def emit_store_word_var(self, name, src="ax"):
        self.writer.emit_mov_mem16_reg16(name, self.map_reg(src))

    def emit_load_word_var(self, dst, name):
        self.writer.emit_mov_reg16_mem16(self.map_reg(dst), name)

    def emit_call_lbl(self, target, comment=""):
        self.writer.emit_call_label(target)
    
    def emit_call(self, target, comment=""):
        if target in ("rax", "eax", "ax"):
            if self.pending_call == "_dos_print_text":
                self.pending_call = None
                self.writer.emit_print_string_current_dx()
                return
                
            if self.pending_call == "_dos_print_int":
                self.pending_call = None
                self.writer.emit_print_int_ax()
                return
                
            if self.pending_call == "_dos_print_newline":
                self.pending_call = None
                self.writer.emit_print_newline()
                return
                
            if self.pending_call == "_dos_runtime_error":
                self.pending_call = None
                self.writer.emit_print_string_current_dx()
                self.writer.emit_print_newline()
                self.writer.emit_exit(1)
                return

        # interne Pascal-Prozeduren/Funktionen
        if isinstance(target, str) and (
            target in self.writer.labels
            or target.startswith("proc_")
            or target.startswith("func_")
            or target.startswith("class_")
        ):
            self.writer.emit_call_label(target)
            return
        
        raise NotImplementedError(f"{tr('DOS call not supported yet')}: {target}")

    def emit_cmp(self, dst, value, comment=""):
        dst = self.map_reg(dst)

        if isinstance(value, int):
            self.writer.emit_cmp_reg16_imm16(dst, value)
            return

        value = self.map_reg(value)
        self.writer.emit_cmp_reg16_reg16(dst, value)

    def emit_je (self, label, comment=""): self.writer.emit_je (label)
    def emit_jne(self, label, comment=""): self.writer.emit_jne(label)
    def emit_jz (self, label, comment=""): self.writer.emit_jz (label)
    def emit_jnz(self, label, comment=""): self.writer.emit_jnz(label)
    def emit_jl (self, label, comment=""): self.writer.emit_jl (label)
    def emit_jle(self, label, comment=""): self.writer.emit_jle(label)
    def emit_jg (self, label, comment=""): self.writer.emit_jg (label)
    def emit_jge(self, label, comment=""): self.writer.emit_jge(label)

    def map_reg(self, reg):
        if reg not in self.REG_MAP:
            raise NotImplementedError(f"{tr('DOS unsupported register')}: {reg}")
        return self.REG_MAP[reg]

    def emit_setne(self, reg, comment=""):
        # DOS16 Ersatz für: setne al
        # Nach cmp ax,0:
        # ax = 1 wenn != 0, sonst 0

        true_label = f"__setne_true_{len(self.writer.code)}"
        done_label = f"__setne_done_{len(self.writer.code)}"

        self.writer.emit_jne(true_label)

        self.writer.emit_mov_reg16_imm16("ax", 0)
        self.writer.emit_jmp(done_label)

        self.writer.bind_label(true_label)
        self.writer.emit_mov_reg16_imm16("ax", 1)

        self.writer.bind_label(done_label)

    def emit_push(self, reg, comment=""):
        self.writer.emit_push_reg16(self.map_reg(reg))

    def emit_pop(self, reg, comment=""):
        self.writer.emit_pop_reg16(self.map_reg(reg))

    def emit_mov(self, dst, src, comment=""):
        dst16 = self.map_reg(dst)

        if isinstance(src, str) and src.lstrip("-").isdigit():
            src = int(src)

        if isinstance(src, int):
            self.writer.emit_mov_reg16_imm16(dst16, src)
            return

        self.writer.emit_mov_reg16_reg16(
            dst16,
            self.map_reg(src)
        )

    def emit_cdq(self, comment=""):
        # Win64/32 Visitor ruft CDQ auf.
        # DOS16 braucht CWD: AX -> DX:AX
        self.writer.emit_cwd()

    def emit_idiv(self, reg, comment=""):
        self.writer.emit_idiv_reg16(self.map_reg(reg))

    def emit_proc_enter(self, local_size=0):
        self.writer.emit_function_prolog(local_size)

    def emit_proc_leave(self):
        self.writer.emit_function_epilog()

    def emit_ret(self, comment=""):
        self.writer.emit_ret()
        
    def emit_imul(self, dst, src, value=None, comment=""):
        dst16 = self.map_reg(dst)
        src16 = self.map_reg(src)
        
        if value is None:
            self.writer.emit_imul_reg16_reg16(dst16, src16)
            return
        
        self.writer.emit_imul_reg16_reg16_imm16(dst16, src16, value)
    
    def emit_xor(self, dst, src, comment=""):
        self.writer.emit_xor_reg16_reg16(
            self.map_reg(dst),
            self.map_reg(src)
        )
    
    def emit_movzx(self, dst, src, comment=""):
        dst16 = self.map_reg(dst)

        # Nach emit_setne() ist AX bereits 0 oder 1.
        # movzx eax, al ist im DOS16-Backend daher ein No-Op.
        if dst16 == "ax" and src == "al":
            return

        raise NotImplementedError(f"{tr('DOS emit_movzx')} {dst}, {src}")
    
    def emit_store_for_end_ax(self):
        self.writer.emit_mov_mem16_reg16(
            self.writer.dos_for_end_symbol,
            "ax"
        )

    def emit_load_for_end_bx(self):
        self.writer.emit_mov_reg16_mem16(
            "bx",
            self.writer.dos_for_end_symbol
        )
    
    def emit_test(self, reg1, reg2, comment=""):
        self.writer.emit_test_reg16_reg16(
            self.map_reg(reg1),
            self.map_reg(reg2)
        )
    
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        # Win64: mov dword [rax + offset], ebx
        # DOS16: mov si, ax / mov word [si + offset], bx

        base16 = self.map_reg(base)
        src16  = self.map_reg(src)

        if base16 != "si":
            self.writer.emit_mov_reg16_reg16("si", base16)
            base16 = "si"

        self.writer.emit_mov_mem16_base_disp_reg16(
            base16,
            int(offset),
            src16
        )

    def emit_new_pointer(self, ptr_symbol, size):
        # bx = heap_pos
        self.writer.emit_mov_reg16_mem16("bx", self.writer.dos_heap_pos_symbol)

        # ax = heap_pos + size
        self.writer.emit_mov_reg16_reg16("ax", "bx")
        self.writer.emit_add_reg16_imm16("ax", size)

        # heap_pos = ax
        self.writer.emit_mov_mem16_reg16(
            self.writer.dos_heap_pos_symbol,
            "ax"
        )

        # ax = address(__dos_heap_area) + old heap_pos
        self.writer.emit_mov_ax_data_label(self.writer.dos_heap_area_symbol)
        self.writer.emit_add_reg16_reg16("ax", "bx")

        # p := ax
        self.writer.emit_mov_mem16_reg16(ptr_symbol, "ax")

    def emit_dispose_pointer(self, ptr_symbol):
        # einfache erste Version: p := nil
        self.writer.emit_mov_reg16_imm16("ax", 0)
        self.writer.emit_mov_mem16_reg16(ptr_symbol, "ax")
    
    def emit_store_far_pointer_var(self, symbol):
        # Erwartung:
        #   AX = Offset
        #   DX = Segment
        self.writer.emit_mov_mem16_reg16_disp(symbol, 0, "ax")
        self.writer.emit_mov_mem16_reg16_disp(symbol, 2, "dx")

    def emit_load_far_pointer_var(self, symbol):
        # Ergebnis:
        #   AX = Offset
        #   DX = Segment
        self.writer.emit_mov_reg16_mem16_disp("ax", symbol, 0)
        self.writer.emit_mov_reg16_mem16_disp("dx", symbol, 2)
    
    def emit_new_pointer_far(self, ptr_symbol, size):
        fail_label = f"__new_fail_{len(self.writer.code)}"
        done_label = f"__new_done_{len(self.writer.code)}"

        self.writer.emit_mov_reg16_imm16("ax", size)
        self.writer.emit_heap_alloc()

        # DX = 0 => Fehler
        self.writer.emit_cmp_reg16_imm16("dx", 0)
        self.writer.emit_je(fail_label)

        # Pointer speichern:
        # AX = Offset
        # DX = Segment
        self.emit_store_far_pointer_var(ptr_symbol)

        self.writer.emit_jmp(done_label)

        self.writer.bind_label(fail_label)

        msg_label = "__msg_out_of_memory"
        self.writer.add_dos_string(msg_label, tr("Out of memory"))

        self.writer.emit_mov_dx_label(msg_label)
        self.writer.emit_print_string_current_dx()
        self.writer.emit_print_newline()
        self.writer.emit_exit(1)

        self.writer.bind_label(done_label)
    
    def emit_dispose_pointer_far(self, ptr_symbol):
        # neuer Heap: NICHT int 21h / AH=49h aufrufen!
        # Dispose/Free setzt den Pointer erstmal nur auf NIL.

        self.writer.emit_mov_reg16_imm16("ax", 0)

        self.writer.emit_mov_mem16_reg16_disp(ptr_symbol, 0, "ax")  # Offset
        self.writer.emit_mov_mem16_reg16_disp(ptr_symbol, 2, "ax")  # Segment
    
    def emit_heap_init(self, paragraphs=0x40):
        self.writer.emit_heap_init(paragraphs)
        
    def emit_heap_alloc(self, size):
        self.writer.emit_mov_reg16_imm16("ax", size)
        self.writer.emit_heap_alloc()
