# ---------------------------------------------------------------------------
# File:   c64_disasm_viewer.py
# Author: add-on for dBase2Many
# Purpose: C64/6502 byte viewer + disassembler as MDI sub window
# ---------------------------------------------------------------------------
from __future__   import annotations
from share.common import *
from PyQt5.QtWidgets import QTabWidget

try:
    from capstone import (
        Cs,
        CS_ARCH_M68K,
        CS_ARCH_X86,
        CS_MODE_64,
        CS_MODE_32,
        CS_MODE_16,
        CS_MODE_BIG_ENDIAN,
        CS_MODE_M68K_000,
    )
    CAPSTONE_AVAILABLE    = True
    CAPSTONE_IMPORT_ERROR = None
    
except Exception as exc:
    Cs                      = None
    CS_ARCH_M68K            = None
    CS_ARCH_X86             = None
    
    CS_MODE_64              = 0
    CS_MODE_32              = 0
    CS_MODE_16              = 0
    CS_MODE_BIG_ENDIAN      = 0
    CS_MODE_M68K_000        = 0
    
    CAPSTONE_AVAILABLE      = False
    CAPSTONE_IMPORT_ERROR   = exc


# opcode -> (mnemonic, addressing mode, instruction length)
# 6510 is compatible with the official 6502 instruction set used by the C64.
C64_OPCODES: Dict[int, Tuple[str, str, int]] = {
    0x00: ("BRK", "impl", 1), 0x01: ("ORA", "indx", 2), 0x05: ("ORA", "zp", 2), 0x06: ("ASL", "zp", 2),
    0x08: ("PHP", "impl", 1), 0x09: ("ORA", "imm", 2), 0x0A: ("ASL", "acc", 1), 0x0D: ("ORA", "abs", 3),
    0x0E: ("ASL", "abs", 3), 0x10: ("BPL", "rel", 2), 0x11: ("ORA", "indy", 2), 0x15: ("ORA", "zpx", 2),
    0x16: ("ASL", "zpx", 2), 0x18: ("CLC", "impl", 1), 0x19: ("ORA", "absy", 3), 0x1D: ("ORA", "absx", 3),
    0x1E: ("ASL", "absx", 3), 0x20: ("JSR", "abs", 3), 0x21: ("AND", "indx", 2), 0x24: ("BIT", "zp", 2),
    0x25: ("AND", "zp", 2), 0x26: ("ROL", "zp", 2), 0x28: ("PLP", "impl", 1), 0x29: ("AND", "imm", 2),
    0x2A: ("ROL", "acc", 1), 0x2C: ("BIT", "abs", 3), 0x2D: ("AND", "abs", 3), 0x2E: ("ROL", "abs", 3),
    0x30: ("BMI", "rel", 2), 0x31: ("AND", "indy", 2), 0x35: ("AND", "zpx", 2), 0x36: ("ROL", "zpx", 2),
    0x38: ("SEC", "impl", 1), 0x39: ("AND", "absy", 3), 0x3D: ("AND", "absx", 3), 0x3E: ("ROL", "absx", 3),
    0x40: ("RTI", "impl", 1), 0x41: ("EOR", "indx", 2), 0x45: ("EOR", "zp", 2), 0x46: ("LSR", "zp", 2),
    0x48: ("PHA", "impl", 1), 0x49: ("EOR", "imm", 2), 0x4A: ("LSR", "acc", 1), 0x4C: ("JMP", "abs", 3),
    0x4D: ("EOR", "abs", 3), 0x4E: ("LSR", "abs", 3), 0x50: ("BVC", "rel", 2), 0x51: ("EOR", "indy", 2),
    0x55: ("EOR", "zpx", 2), 0x56: ("LSR", "zpx", 2), 0x58: ("CLI", "impl", 1), 0x59: ("EOR", "absy", 3),
    0x5D: ("EOR", "absx", 3), 0x5E: ("LSR", "absx", 3), 0x60: ("RTS", "impl", 1), 0x61: ("ADC", "indx", 2),
    0x65: ("ADC", "zp", 2), 0x66: ("ROR", "zp", 2), 0x68: ("PLA", "impl", 1), 0x69: ("ADC", "imm", 2),
    0x6A: ("ROR", "acc", 1), 0x6C: ("JMP", "ind", 3), 0x6D: ("ADC", "abs", 3), 0x6E: ("ROR", "abs", 3),
    0x70: ("BVS", "rel", 2), 0x71: ("ADC", "indy", 2), 0x75: ("ADC", "zpx", 2), 0x76: ("ROR", "zpx", 2),
    0x78: ("SEI", "impl", 1), 0x79: ("ADC", "absy", 3), 0x7D: ("ADC", "absx", 3), 0x7E: ("ROR", "absx", 3),
    0x81: ("STA", "indx", 2), 0x84: ("STY", "zp", 2), 0x85: ("STA", "zp", 2), 0x86: ("STX", "zp", 2),
    0x88: ("DEY", "impl", 1), 0x8A: ("TXA", "impl", 1), 0x8C: ("STY", "abs", 3), 0x8D: ("STA", "abs", 3),
    0x8E: ("STX", "abs", 3), 0x90: ("BCC", "rel", 2), 0x91: ("STA", "indy", 2), 0x94: ("STY", "zpx", 2),
    0x95: ("STA", "zpx", 2), 0x96: ("STX", "zpy", 2), 0x98: ("TYA", "impl", 1), 0x99: ("STA", "absy", 3),
    0x9A: ("TXS", "impl", 1), 0x9D: ("STA", "absx", 3), 0xA0: ("LDY", "imm", 2), 0xA1: ("LDA", "indx", 2),
    0xA2: ("LDX", "imm", 2), 0xA4: ("LDY", "zp", 2), 0xA5: ("LDA", "zp", 2), 0xA6: ("LDX", "zp", 2),
    0xA8: ("TAY", "impl", 1), 0xA9: ("LDA", "imm", 2), 0xAA: ("TAX", "impl", 1), 0xAC: ("LDY", "abs", 3),
    0xAD: ("LDA", "abs", 3), 0xAE: ("LDX", "abs", 3), 0xB0: ("BCS", "rel", 2), 0xB1: ("LDA", "indy", 2),
    0xB4: ("LDY", "zpx", 2), 0xB5: ("LDA", "zpx", 2), 0xB6: ("LDX", "zpy", 2), 0xB8: ("CLV", "impl", 1),
    0xB9: ("LDA", "absy", 3), 0xBA: ("TSX", "impl", 1), 0xBC: ("LDY", "absx", 3), 0xBD: ("LDA", "absx", 3),
    0xBE: ("LDX", "absy", 3), 0xC0: ("CPY", "imm", 2), 0xC1: ("CMP", "indx", 2), 0xC4: ("CPY", "zp", 2),
    0xC5: ("CMP", "zp", 2), 0xC6: ("DEC", "zp", 2), 0xC8: ("INY", "impl", 1), 0xC9: ("CMP", "imm", 2),
    0xCA: ("DEX", "impl", 1), 0xCC: ("CPY", "abs", 3), 0xCD: ("CMP", "abs", 3), 0xCE: ("DEC", "abs", 3),
    0xD0: ("BNE", "rel", 2), 0xD1: ("CMP", "indy", 2), 0xD5: ("CMP", "zpx", 2), 0xD6: ("DEC", "zpx", 2),
    0xD8: ("CLD", "impl", 1), 0xD9: ("CMP", "absy", 3), 0xDD: ("CMP", "absx", 3), 0xDE: ("DEC", "absx", 3),
    0xE0: ("CPX", "imm", 2), 0xE1: ("SBC", "indx", 2), 0xE4: ("CPX", "zp", 2), 0xE5: ("SBC", "zp", 2),
    0xE6: ("INC", "zp", 2), 0xE8: ("INX", "impl", 1), 0xE9: ("SBC", "imm", 2), 0xEA: ("NOP", "impl", 1),
    0xEC: ("CPX", "abs", 3), 0xED: ("SBC", "abs", 3), 0xEE: ("INC", "abs", 3), 0xF0: ("BEQ", "rel", 2),
    0xF1: ("SBC", "indy", 2), 0xF5: ("SBC", "zpx", 2), 0xF6: ("INC", "zpx", 2), 0xF8: ("SED", "impl", 1),
    0xF9: ("SBC", "absy", 3), 0xFD: ("SBC", "absx", 3), 0xFE: ("INC", "absx", 3),
}


class BasicLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class BasicNumberedPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = BasicLineNumberArea(self)
        self.basic_line_numbers = [10]

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        max_number = max(self.basic_line_numbers or [10])
        digits = len(str(max_number))
        return 10 + self.fontMetrics().horizontalAdvance("9") * max(3, digits)

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            cursor = self.textCursor()
            block_index = cursor.blockNumber()
            super().keyPressEvent(event)
            self.insert_basic_line_number_after(block_index)
            return

        super().keyPressEvent(event)
        self.sync_line_number_count()

    def insertFromMimeData(self, source):
        old_count = self.blockCount()
        old_block = self.textCursor().blockNumber()
        super().insertFromMimeData(source)
        new_count = self.blockCount()
        added = new_count - old_count
        if added > 0:
            for i in range(added):
                self.insert_basic_line_number_after(old_block + i)
        self.sync_line_number_count()

    def insert_basic_line_number_after(self, block_index):
        self.sync_line_number_count()

        if block_index < 0:
            self.basic_line_numbers.insert(0, 10)
            self.line_number_area.update()
            return

        previous = self.basic_line_numbers[block_index] if block_index < len(self.basic_line_numbers) else 10
        next_index = block_index + 1
        next_number = None
        if next_index < len(self.basic_line_numbers):
            next_number = self.basic_line_numbers[next_index]

        if next_number is None:
            new_number = previous + 10
        else:
            new_number = previous + 1
            if new_number >= next_number:
                self.shift_following_line_numbers(next_index, new_number + 1)

        self.basic_line_numbers.insert(next_index, new_number)
        self.line_number_area.update()

    def shift_following_line_numbers(self, start_index, minimum_value):
        value = minimum_value
        for i in range(start_index, len(self.basic_line_numbers)):
            if self.basic_line_numbers[i] < value:
                self.basic_line_numbers[i] = value
            value = self.basic_line_numbers[i] + 1

    def sync_line_number_count(self):
        count = self.blockCount()

        if count <= 0:
            self.basic_line_numbers = [10]
            return

        if not self.basic_line_numbers:
            self.basic_line_numbers = [10]

        while len(self.basic_line_numbers) < count:
            self.basic_line_numbers.append(self.basic_line_numbers[-1] + 10)

        if len(self.basic_line_numbers) > count:
            self.basic_line_numbers = self.basic_line_numbers[:count]

        self.line_number_area.update()

    def highlight_current_line(self):
        selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#202020"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            selections.append(selection)
        self.setExtraSelections(selections)

    def line_number_area_paint_event(self, event):
        self.sync_line_number_count()

        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#151515"))
        painter.setPen(QColor("#8fc7ff"))
        painter.setFont(self.font())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                if block_number < len(self.basic_line_numbers):
                    number = str(self.basic_line_numbers[block_number])
                else:
                    number = str((block_number + 1) * 10)
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width() - 4,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

class ClickableMnemonic(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, mnemonic: str, text: str, parent=None):
        super().__init__(text, parent)
        
        txt = share.locales.tr("Display Help for: %s")
        
        self.mnemonic = mnemonic
        self.setCursor(Qt.PointingHandCursor)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setToolTip(f"{txt}" % mnemonic)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.mnemonic)
            event.accept()
            return
        super().mousePressEvent(event)


def _word(lo: int, hi: int) -> int:
    return lo | (hi << 8)


def _format_operand(mode: str, operand: bytes, pc: int) -> str:
    b0 = operand[0] if len(operand) > 0 else 0
    b1 = operand[1] if len(operand) > 1 else 0
    if mode == "impl": return ""
    if mode == "acc": return "A"
    if mode == "imm": return "#$%02X" % b0
    if mode == "zp": return "$%02X" % b0
    if mode == "zpx": return "$%02X,X" % b0
    if mode == "zpy": return "$%02X,Y" % b0
    if mode == "abs": return "$%04X" % _word(b0, b1)
    if mode == "absx": return "$%04X,X" % _word(b0, b1)
    if mode == "absy": return "$%04X,Y" % _word(b0, b1)
    if mode == "ind": return "($%04X)" % _word(b0, b1)
    if mode == "indx": return "($%02X,X)" % b0
    if mode == "indy": return "($%02X),Y" % b0
    if mode == "rel":
        signed = b0 - 256 if b0 & 0x80 else b0
        return "$%04X" % ((pc + 2 + signed) & 0xFFFF)
    return ""


def disassemble_one(data: bytes, offset: int) -> Tuple[str, str, int]:
    op = data[offset]
    info = C64_OPCODES.get(op)
    if info is None:
        return ("???", ".BYTE $%02X" % op, 1)
    mnemonic, mode, length = info
    chunk = data[offset + 1:offset + length]
    operand = _format_operand(mode, chunk, offset)
    if operand:
        return (mnemonic, "%s %s" % (mnemonic, operand), length)
    return (mnemonic, mnemonic, length)


def c64_char(byte_value: int) -> str:
    # PETSCII-artige Anzeige: druckbare ASCII-Zeichen direkt, sonst Punkt.
    if 32 <= byte_value <= 126:
        return chr(byte_value)
    return "."


def ansi_char(byte_value: int) -> str:
    if 32 <= byte_value <= 126:
        return chr(byte_value)
    return "."


def display_char(byte_value: int, arch_name: str) -> str:
    if arch_name == DISASM_ARCH_C64:
        return c64_char(byte_value)
    return ansi_char(byte_value)


def format_c64_disasm_line(data: bytes, offset: int) -> Tuple[str, str, str, str, str, int]:
    mnemonic, asm_text, used = disassemble_one(data, offset)

    if used <= 0:
        used = 1

    instr_bytes = data[offset:offset + used]
    if not instr_bytes:
        instr_bytes = data[offset:offset + 1]

    used = max(1, len(instr_bytes))

    address_text = "%04X:" % (offset & 0xFFFF)
    hex_text     = " ".join("%02X" % b  for b in instr_bytes)
    char_text    = "" .join(c64_char(b) for b in instr_bytes)

    return address_text, hex_text, mnemonic, asm_text, char_text, used


DISASM_ARCH_C64     = "c64"
DISASM_ARCH_AMIGA   = "amiga"

DISASM_ARCH_INTEL16 = "intel16"
DISASM_ARCH_INTEL32 = "intel32"
DISASM_ARCH_INTEL64 = "intel64"

DISASM_ARCH_LABELS = {
    DISASM_ARCH_C64:     "C64 / 6502",
    DISASM_ARCH_AMIGA:   "Amiga / Motorola 68000",
    
    DISASM_ARCH_INTEL16: "Intel x86  16-Bit DOS",
    DISASM_ARCH_INTEL32: "Intel x86  32-Bit Windows",
    DISASM_ARCH_INTEL64: "Intel ia64 64-Bit Windows",
}


def guess_architecture_from_path(file_path: str) -> str:
    ext = os.path.splitext(file_path or "")[1].lower()

    if ext in (".prg", ".c64"):
        return DISASM_ARCH_C64
    
    if ext in (".adf", ".hunk"):
        return DISASM_ARCH_AMIGA
    
    if ext in (".exe", ".dll", ".obj", ".com"):
        return DISASM_ARCH_INTEL32
    
    if ext in (".rom", ".bin"):
        return DISASM_ARCH_C64
    
    return DISASM_ARCH_C64


def _capstone_config(arch_name: str):
    if arch_name == DISASM_ARCH_AMIGA:
        return CS_ARCH_M68K, CS_MODE_BIG_ENDIAN | CS_MODE_M68K_000, 0x00000000, 8
    
    if arch_name == DISASM_ARCH_INTEL64:
        return CS_ARCH_X86, CS_MODE_64, 0x0000000000000000, 16
    
    if arch_name == DISASM_ARCH_INTEL32:
        return CS_ARCH_X86, CS_MODE_32, 0x00400000, 8
    
    if arch_name == DISASM_ARCH_INTEL16:
        return CS_ARCH_X86, CS_MODE_16, 0x0100, 4
        
    return None


def format_capstone_disasm_line(data: bytes, offset: int, arch_name: str) -> Tuple[str, str, str, str, str, int]:
    cfg = _capstone_config(arch_name)

    if cfg is None:
        return format_c64_disasm_line(data, offset)

    if not CAPSTONE_AVAILABLE:
        b = data[offset] if offset < len(data) else 0
        address_width = 8
        address_text = ("%%0%dX:" % address_width) % offset
        hex_text = "%02X" % b
        mnemonic = "???"
        asm_text = ".BYTE $%02X    ; Capstone fehlt: pip install capstone" % b
        char_text = c64_char(b)
        return address_text, hex_text, mnemonic, asm_text, char_text, 1

    cap_arch, cap_mode, base_address, address_width = cfg
    md = Cs(cap_arch, cap_mode)
    md.detail = False

    chunk = data[offset:]
    absolute_address = base_address + offset

    try:
        insn = next(md.disasm(chunk, absolute_address, count=1), None)
    except Exception:
        insn = None

    if insn is None or not getattr(insn, "bytes", None):
        b = data[offset] if offset < len(data) else 0
        instr_bytes = bytes([b])
        mnemonic = "???"
        asm_text = ".BYTE $%02X" % b
        used = 1
    else:
        instr_bytes = bytes(insn.bytes)
        mnemonic = (insn.mnemonic or "???").upper()
        op_str = (insn.op_str or "").strip()
        if op_str:
            asm_text = "%s %s" % (mnemonic, op_str.upper())
        else:
            asm_text = mnemonic
        used = max(1, len(instr_bytes))

    if arch_name == DISASM_ARCH_INTEL16:
        address_text = "%04X:%04X" % (0, absolute_address & 0xFFFF)
    else:
        address_text = ("%%0%dX:" % address_width) % (absolute_address & ((1 << (address_width * 4)) - 1))
    hex_text = " ".join("%02X" % b for b in instr_bytes)
    char_text = "".join(c64_char(b) for b in instr_bytes)

    return address_text, hex_text, mnemonic, asm_text, char_text, used


def format_disasm_line(data: bytes, offset: int, arch_name: str) -> Tuple[str, str, str, str, str, int]:
    if arch_name == DISASM_ARCH_C64:
        return format_c64_disasm_line(data, offset)
    return format_capstone_disasm_line(data, offset, arch_name)


class C64DisasmTableModel(QAbstractTableModel):
    COL_ADDRESS = 0
    COL_BYTES   = 1
    COL_ASM     = 2
    COL_CHARS   = 3

    HEADERS = [
        share.locales.tr("Address"   ),
        share.locales.tr("Bytes"     ),
        share.locales.tr("Assembler" ),
        share.locales.tr("Characters")]

    def __init__(self, c64_font_family="Courier New", parent=None):
        super().__init__(parent)
        self._rows = []
        self._arch_name = DISASM_ARCH_C64
        self._mono_font = QFont("Consolas", 10)
        self._mono_font.setStyleHint(QFont.Monospace)
        self._c64_font = QFont(c64_font_family, 10)
        self._c64_font.setStyleHint(QFont.Monospace)

    def set_architecture(self, arch_name):
        self._arch_name = arch_name or DISASM_ARCH_C64
        if self._rows:
            top_left = self.index(0, 0)
            bottom_right = self.index(len(self._rows) - 1, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.FontRole])

    def clear(self):
        self.beginResetModel()
        self._rows = []
        self.endResetModel()

    def set_rows(self, rows):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 4

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and 0 <= section < len(self.HEADERS):
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._rows):
            return None

        address_text, hex_text, mnemonic, asm_text, char_text, used = self._rows[row]

        if role in (Qt.DisplayRole, Qt.EditRole):
            if col == self.COL_ADDRESS:
                return address_text
            if col == self.COL_BYTES:
                return hex_text
            if col == self.COL_ASM:
                return asm_text
            if col == self.COL_CHARS:
                return char_text
            return ""

        if role == Qt.UserRole:
            return mnemonic

        if role == Qt.FontRole:
            if self._arch_name == DISASM_ARCH_C64:
                return self._c64_font
            return self._mono_font

        if role == Qt.ForegroundRole:
            if col == self.COL_ADDRESS:
                return QColor("#8fc7ff")
            if col == self.COL_BYTES:
                return QColor("#dcdcdc")
            if col == self.COL_ASM:
                return QColor("#ffd866")
            if col == self.COL_CHARS:
                return QColor("#ffffff")

        if role == Qt.TextAlignmentRole:
            if col == self.COL_ADDRESS:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        if role == Qt.ToolTipRole and col == self.COL_ASM:
            return "Hilfe zu %s anzeigen" % mnemonic

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def mnemonic_for_row(self, row):
        if 0 <= row < len(self._rows):
            return self._rows[row][2]
        return ""


class C64DisasmTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(False)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.setSortingEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet(r"""
        QTableView{color:#ffffff;background:#101010;alternate-background-color:#141414;border:none;
        selection-background-color:#315a90;selection-color:#ffffff;}
        QHeaderView::section{color:#ffffff;background:#202020;border:0px;border-right:1px solid #303030;
        padding: 3px 6px;}""")

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy_selection_to_clipboard()
            event.accept()
            return
        super().keyPressEvent(event)

    def copy_selection_to_clipboard(self):
        indexes = self.selectedIndexes()
        if not indexes:
            return

        indexes = sorted(indexes, key=lambda idx: (idx.row(), idx.column()))
        rows = {}
        for index in indexes:
            rows.setdefault(index.row(), {})[index.column()] = str(index.data() or "")

        lines = []
        for row in sorted(rows):
            cols = rows[row]
            line = "\t".join(cols.get(col, "") for col in sorted(cols))
            lines.append(line)

        QApplication.clipboard().setText("\n".join(lines))


def format_hex_viewer_rows(data: bytes, arch_name: str):
    rows = []
    pos = 0

    if arch_name in (DISASM_ARCH_INTEL32, DISASM_ARCH_INTEL64):
        left_count  = 8
        right_count = 8
    else:
        left_count  = 4
        right_count = 4

    row_count = left_count + right_count

    while pos < len(data):
        row_bytes = data[pos:pos + row_count]
        left_bytes = row_bytes[:left_count]
        right_bytes = row_bytes[left_count:row_count]

        left_text = " ".join("%02X" % b for b in left_bytes)
        right_text = " ".join("%02X" % b for b in right_bytes)

        if len(left_bytes) < left_count:
            left_text = left_text + ("   " * (left_count - len(left_bytes)))
        if len(right_bytes) < right_count:
            right_text = right_text + ("   " * (right_count - len(right_bytes)))

        hex_text = "%s | %s" % (left_text, right_text)
        char_text = "".join(display_char(b, arch_name) for b in row_bytes)
        rows.append((hex_text, char_text))
        pos += row_count

    return rows


class C64HexViewerTableModel(QAbstractTableModel):
    COL_HEX   = 0
    COL_CHARS = 1

    HEADERS = [
        share.locales.tr("Hex"     ),
        share.locales.tr("PETSCII" )]

    def __init__(self, c64_font_family="Courier New", parent=None):
        super().__init__(parent)
        self._rows = []
        self._arch_name = DISASM_ARCH_C64
        self._mono_font = QFont("Consolas", 10)
        self._mono_font.setStyleHint(QFont.Monospace)
        self._c64_font = QFont(c64_font_family, 10)
        self._c64_font.setStyleHint(QFont.Monospace)

    def set_architecture(self, arch_name):
        self._arch_name = arch_name or DISASM_ARCH_C64
        if self._rows:
            top_left = self.index(0, 0)
            bottom_right = self.index(len(self._rows) - 1, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.FontRole, Qt.DisplayRole])
            self.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount() - 1)

    def clear(self):
        self.beginResetModel()
        self._rows = []
        self.endResetModel()

    def set_rows(self, rows):
        self.beginResetModel()
        self._rows = rows
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return 2

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and 0 <= section < len(self.HEADERS):
            if section == self.COL_CHARS and self._arch_name != DISASM_ARCH_C64:
                return "ANSI/Unicode"
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()
        if row < 0 or row >= len(self._rows):
            return None

        hex_text, char_text = self._rows[row]

        if role in (Qt.DisplayRole, Qt.EditRole):
            if col == self.COL_HEX:
                return hex_text
            if col == self.COL_CHARS:
                return char_text
            return ""

        if role == Qt.FontRole:
            if col == self.COL_CHARS and self._arch_name == DISASM_ARCH_C64:
                return self._c64_font
            return self._mono_font

        if role == Qt.ForegroundRole:
            if col == self.COL_HEX:
                return QColor("#dcdcdc")
            if col == self.COL_CHARS:
                return QColor("#ffffff")

        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignVCenter

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


class C64HexViewerTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(False)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.setSortingEnabled(False)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.setStyleSheet(r"""
        QTableView{color:#ffffff;background:#101010;alternate-background-color:#141414;border:none;
        selection-background-color:#315a90;selection-color:#ffffff;}
        QHeaderView::section{color:#ffffff;background:#202020;border:0px;border-right:1px solid #303030;
        padding: 3px 6px;}""")

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy_selection_to_clipboard()
            event.accept()
            return
        super().keyPressEvent(event)

    def copy_selection_to_clipboard(self):
        indexes = self.selectedIndexes()
        if not indexes:
            return

        indexes = sorted(indexes, key=lambda idx: (idx.row(), idx.column()))
        rows = {}
        for index in indexes:
            rows.setdefault(index.row(), {})[index.column()] = str(index.data() or "")

        lines = []
        for row in sorted(rows):
            cols = rows[row]
            line = "\t".join(cols.get(col, "") for col in sorted(cols))
            lines.append(line)

        QApplication.clipboard().setText("\n".join(lines))


class C64DisasmViewer(QWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.file_path: Optional[str] = None
        self._data = b""
        self.current_arch = DISASM_ARCH_C64
        self.bytes_per_row = 8
        self.vice_process = None
        self.vice_hwnd = None
        self._vice_embed_attempts = 0
        self.c64_font_family = self._load_c64_font()
        self._build_ui()

    def load_file(self, file_path: str, progress=None):
        self.file_path = file_path
        self.current_arch = guess_architecture_from_path(file_path)

        with open(file_path, "rb") as f:
            self._data = f.read()

        self._set_arch_combo_value(self.current_arch)
        self.render_bytes(self._data, progress)

        label = DISASM_ARCH_LABELS.get(self.current_arch, self.current_arch)
        txt1  = share.locales.tr("Bytes")
        self.info_label.setText(f"%s  -  %d {txt1}  -  %s" % (file_path, len(self._data), label))

    def _set_arch_combo_value(self, arch_name: str):
        combo = getattr(self, "arch_combo", None)
        if combo is None:
            return
        index = combo.findData(arch_name)
        if index >= 0 and combo.currentIndex() != index:
            blocked = combo.blockSignals(True)
            combo.setCurrentIndex(index)
            combo.blockSignals(blocked)

    def on_architecture_changed(self, index: int):
        arch_name = self.arch_combo.itemData(index) or DISASM_ARCH_C64
        self.current_arch = arch_name
        
        txt1 = share.locales.tr("To Disassemble Amiga- and Intel, Capstone is needed")
        txt2 = share.locales.tr("Disassembler")
        txt3 = share.locales.tr("Installing")
        txt4 = share.locales.tr("Bytes")
        txt5 = share.locales.tr("Disassemble File...")
        txt6 = share.locales.tr("Cancel")
        
        if arch_name != DISASM_ARCH_C64 and not CAPSTONE_AVAILABLE:
            QMessageBox.warning(self, txt2, f"{txt1}.\n\n{txt3}:\npip install capstone")

        if self._data:
            progress = QProgressDialog(
                txt5, txt6,   0,
                len(self._data),
                self
            )
            progress.setWindowTitle(txt2)
            progress.setWindowModality(Qt.WindowModal)
            progress.setMinimumDuration(0)
            self.render_bytes(self._data, progress)
            progress.close()

        if self.file_path:
            label = DISASM_ARCH_LABELS.get(self.current_arch, self.current_arch)
            self.info_label.setText(f"%s  -  %d {txt4}  -  %s" % (self.file_path, len(self._data), label))

    def render_bytes(self, data: bytes, progress=None):
        rows = []
        pos = 0
        step_counter = 0

        while pos < len(data):
            if progress is not None and (step_counter % 128 == 0):
                progress.setValue(pos)

                if progress.wasCanceled():
                    break

                QApplication.processEvents()

            address_text, hex_text, mnemonic, asm_text, char_text, used = format_disasm_line(data, pos, self.current_arch)
            rows.append((address_text, hex_text, mnemonic, asm_text, char_text, used))

            pos += max(1, used)
            step_counter += 1

        self.disasm_model.set_architecture(self.current_arch)
        self.disasm_model.set_rows(rows)
        if hasattr(self, "hex_model"):
            self.hex_model.set_architecture(self.current_arch)
            self.hex_model.set_rows(format_hex_viewer_rows(data, self.current_arch))

        if progress is not None:
            progress.setValue(len(data))
            QApplication.processEvents()

    def _load_c64_font(self) -> str:
        candidates = [
            Path(__file__).resolve().parents[2] / "data" / "fonts" / "C64_Pro_Mono-STYLE.ttf",
            Path(__file__).resolve().parents[1] / "data" / "fonts" / "C64_Pro_Mono-STYLE.ttf",
            
            Path.cwd() / "data" / "fonts" / "C64_Pro_Mono-STYLE.ttf",
            Path.cwd() / "C64_Pro_Mono-STYLE.ttf",
        ]
        for font_path in candidates:
            if font_path.exists():
                font_id = QFontDatabase.addApplicationFont(str(font_path))
                if font_id >= 0:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    if families:
                        return families[0]
        return "Courier New"

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)
        
        self.splitter = QSplitter(Qt.Horizontal, self)
        
        self.left_panel = QWidget(self)
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 4, 0)
        self.left_layout.setSpacing(6)
        
        self.right_panel = QWidget(self)
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(4, 0, 0, 0)
        self.right_layout.setSpacing(6)
        
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([680, 360])
        
        root.addWidget(self.splitter, 1)
        
        self.info_label = QLabel(share.locales.tr("No File loaded."), self.left_panel)
        self.info_label.setStyleSheet("color: #d7d7d7;")
        self.left_layout.addWidget(self.info_label)
        
        self.arch_bar = QWidget(self.left_panel)
        self.arch_layout = QHBoxLayout(self.arch_bar)
        self.arch_layout.setContentsMargins(0, 0, 0, 0)
        self.arch_layout.setSpacing(6)

        self.arch_label = QLabel(share.locales.tr("Assembler:"), self.arch_bar)
        self.arch_combo = QComboBox(self.arch_bar)
        self.arch_combo.setFont(QFont("Consolas", 10))
        
        self.arch_combo.addItem(DISASM_ARCH_LABELS[DISASM_ARCH_C64    ], DISASM_ARCH_C64)
        self.arch_combo.addItem(DISASM_ARCH_LABELS[DISASM_ARCH_AMIGA  ], DISASM_ARCH_AMIGA)
        
        self.arch_combo.addItem(DISASM_ARCH_LABELS[DISASM_ARCH_INTEL16], DISASM_ARCH_INTEL16)
        self.arch_combo.addItem(DISASM_ARCH_LABELS[DISASM_ARCH_INTEL32], DISASM_ARCH_INTEL32)
        self.arch_combo.addItem(DISASM_ARCH_LABELS[DISASM_ARCH_INTEL64], DISASM_ARCH_INTEL64)
        
        self.arch_combo.currentIndexChanged.connect(self.on_architecture_changed)

        self.arch_layout.addWidget(self.arch_label)
        self.arch_layout.addWidget(self.arch_combo, 1)
        self.left_layout.addWidget(self.arch_bar)

        self.left_vertical_splitter = QSplitter(Qt.Vertical, self.left_panel)
        self.left_vertical_splitter.setChildrenCollapsible(False)
        self.left_layout.addWidget(self.left_vertical_splitter, 1)

        self.listing_panel = QWidget(self.left_vertical_splitter)
        self.listing_layout = QVBoxLayout(self.listing_panel)
        self.listing_layout.setContentsMargins(0, 0, 0, 0)
        self.listing_layout.setSpacing(0)

        self.listing_tabs = QTabWidget(self.listing_panel)
        self.listing_tabs.setObjectName("listingDisasmTabs")

        self.disasm_model = C64DisasmTableModel(self.c64_font_family, self)
        self.disasm_table = C64DisasmTableView(self.listing_tabs)
        self.disasm_table.setModel(self.disasm_model)
        self.disasm_table.clicked.connect(self.on_disasm_table_clicked)
        self.disasm_table.doubleClicked.connect(self.on_disasm_table_double_clicked)
        self.disasm_table.setColumnWidth(C64DisasmTableModel.COL_ADDRESS, 105)
        self.disasm_table.setColumnWidth(C64DisasmTableModel.COL_BYTES, 140)
        self.disasm_table.setColumnWidth(C64DisasmTableModel.COL_ASM, 190)
        self.disasm_table.setColumnWidth(C64DisasmTableModel.COL_CHARS, 260)

        self.hex_model = C64HexViewerTableModel(self.c64_font_family, self)
        self.hex_table = C64HexViewerTableView(self.listing_tabs)
        self.hex_table.setModel(self.hex_model)
        self.hex_table.setColumnWidth(C64HexViewerTableModel.COL_HEX, 360)
        self.hex_table.setColumnWidth(C64HexViewerTableModel.COL_CHARS, 140)

        self.listing_tabs.addTab(self.disasm_table, share.locales.tr("Assembler"))
        self.listing_tabs.addTab(self.hex_table, share.locales.tr("Hexviewer"))
        self.listing_layout.addWidget(self.listing_tabs, 1)

        self.left_vertical_splitter.addWidget(self.listing_panel)
        self.left_vertical_splitter.setStretchFactor(0, 1)
        self.left_vertical_splitter.setSizes([590])

        self.right_tabs = QTabWidget(self.right_panel)
        self.right_tabs.setObjectName("rightDisasmTabs")
        self.right_layout.addWidget(self.right_tabs, 1)

        self.vice_tab = QWidget(self.right_tabs)
        self.vice_tab_layout = QVBoxLayout(self.vice_tab)
        self.vice_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.vice_tab_layout.setSpacing(6)

        self.vice_host = QWidget(self.vice_tab)
        self.vice_host.setMinimumWidth(360)
        self.vice_host.setStyleSheet("""
            QWidget {
                background: #000000;
                border: 1px solid #444444;
            }
        """)
        self.vice_tab_layout.addWidget(self.vice_host, 1)

        self.vice_status_label = QLabel(
            share.locales.tr("VICE not started"),
            self.vice_tab
        )
        self.vice_status_label.setStyleSheet("color: #d7d7d7;")
        self.vice_tab_layout.addWidget(self.vice_status_label)

        self.left_plain_edit = BasicNumberedPlainTextEdit(self.right_tabs)
        self.left_plain_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        #self.left_plain_edit.setPlaceholderText("BASIC / Labels / Kommentare ...")

        self.right_plain_edit = BasicNumberedPlainTextEdit(self.right_tabs)
        self.right_plain_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        #self.right_plain_edit.setPlaceholderText("VICE / Monitor / Ausgabe ...")

        edit_font = QFont("Consolas", 10)
        edit_font.setStyleHint(QFont.Monospace)
        self.left_plain_edit.setFont(edit_font)
        self.right_plain_edit.setFont(edit_font)

        self.right_tabs.addTab(self.vice_tab, share.locales.tr("Vice View"))
        self.right_tabs.addTab(self.left_plain_edit, share.locales.tr("Left Editor"))
        self.right_tabs.addTab(self.right_plain_edit, share.locales.tr("Right Editor"))

        self._toolbar_actions = []
        self._toolbar = None

        self.setStyleSheet(r"""
        C64DisasmViewer{background:#101010;}
        QScrollArea{background:#101010;}
        QLabel{color:#e6e6e6;}
        QPlainTextEdit{color:#ffffff;background:#181818;border:1px solid #333333;
        selection-background-color:#315a90;}
        QLineEdit{color:#ffffff;background:#181818;border:1px solid #333333;
        padding:1px 4px;selection-background-color:#315a90;}
        QComboBox{color:#ffffff;background:#181818;border:1px solid #444444;padding:2px 6px;}
        QTabWidget::pane{border:1px solid #333333;background:#101010;}
        QTabBar::tab{color:#ffffff;background:#202020;border:1px solid #333333;padding: 4px 10px;}
        QTabBar::tab:selected{background:#303030;color:#ffd866;}
        QSplitter::handle{background:#303030;}
        QSplitter::handle:hover{background:#505050;}""")

    def _find_main_toolbar(self):
        if self.main_window is None:
            return None

        toolbars = []
        try:
            toolbars = self.main_window.findChildren(QToolBar)
        except Exception:
            toolbars = []

        if toolbars:
            return toolbars[0]

        toolbar = getattr(self.main_window, "toolBar", None)
        if isinstance(toolbar, QToolBar):
            return toolbar

        toolbar = getattr(self.main_window, "toolbar", None)
        if isinstance(toolbar, QToolBar):
            return toolbar

        return None

    def install_toolbar_actions(self):
        if self._toolbar_actions:
            return

        toolbar = self._find_main_toolbar()
        if toolbar is None:
            return

        self._toolbar = toolbar
        style = QApplication.style()

        self.action_vice_start = QAction(
            style.standardIcon(QStyle.SP_MediaPlay),
            "VICE starten",
            self
        )
        self.action_vice_start.setObjectName("actionC64ViceStart")
        self.action_vice_start.setToolTip(share.locales.tr("Start VICE"))
        self.action_vice_start.triggered.connect(self.on_vice_start_clicked)

        self.action_vice_stop = QAction(
            style.standardIcon(QStyle.SP_MediaStop),
            "VICE beenden",
            self
        )
        self.action_vice_stop.setObjectName("actionC64ViceStop")
        self.action_vice_stop.setToolTip(share.locales.tr("Stop VICE"))
        self.action_vice_stop.triggered.connect(self.on_vice_stop_clicked)

        toolbar.addAction(self.action_vice_start)
        toolbar.addAction(self.action_vice_stop)
        self._toolbar_actions = [self.action_vice_start, self.action_vice_stop]

    def remove_toolbar_actions(self):
        toolbar = self._toolbar
        if toolbar is not None:
            for action in list(self._toolbar_actions):
                try:
                    toolbar.removeAction(action)
                except Exception:
                    pass

        for action in list(self._toolbar_actions):
            try:
                action.deleteLater()
            except Exception:
                pass

        self._toolbar_actions = []
        self._toolbar = None

    def _resolve_vice_executable(self):
        candidates = []
        configured = getattr(self.main_window, "vice_executable", "") if self.main_window is not None else ""
        
        if configured:
            candidates.append(configured)
        
        for env_name in ("VICE_EXE", "VICE_X64SC"):
            value = os.environ.get(env_name, "")
            if value:
                candidates.append(value)
        
        candidates.extend([
            r"T:\C-64\bin\x64sc.exe",
            r"C:\Program Files\VICE\x64sc.exe",
            r"C:\Program Files\VICE\x64.exe",
            r"C:\Program Files (x86)\VICE\x64sc.exe",
            r"C:\Program Files (x86)\VICE\x64.exe",
            "x64sc.exe",
            "x64.exe",
        ])

        for candidate in candidates:
            if not candidate:
                continue
            if os.path.isabs(candidate):
                if os.path.exists(candidate):
                    return candidate
            else:
                return candidate

        txt1 = share.locales.tr("Select VICE Emulator")
        txt2 = share.locales.tr("Programs")
        txt3 = share.locales.tr("All Files")
        
        path, _ = QFileDialog.getOpenFileName(
            self,
            txt1,
            "",
            f"VICE Emulator (x64sc.exe x64.exe);;{txt2} (*.exe);;{txt3} (*.*)",
        )
        return path or None

    def on_vice_start_clicked(self):
        if sys.platform != "win32":
            QMessageBox.warning(
                self,
                "VICE",
                share.locales.tr("TODO: embedd VICE-Window"))
            return

        if self.vice_process is not None and self.vice_process.state() != QProcess.NotRunning:
            self._embed_vice_window_later()
            return

        vice_exe = self._resolve_vice_executable()
        if not vice_exe:
            return

        self.vice_process = QProcess(self)
        self.vice_process.setProgram(vice_exe)
        self.vice_process.setArguments([])
        self.vice_process.finished.connect(self._on_vice_finished)
        self.vice_process.start()

        if not self.vice_process.waitForStarted(3000):
            msg = share.locales.tr("VICE could not be started")
            QMessageBox.warning(
                self,
                "VICE",
                f"{msg}:\n%s" % self.vice_process.errorString()
            )
            self.vice_process = None
            return

        self.vice_status_label.setText(
        share.locales.tr("VICE started - Embedd Window ..."))
        self._embed_vice_window_later()

    def _embed_vice_window_later(self):
        self._vice_embed_attempts = 0
        QTimer.singleShot(300, self._try_embed_vice_window)

    def _try_embed_vice_window(self):
        self._vice_embed_attempts += 1

        hwnd = self._find_vice_window_handle()
        if hwnd:
            self._embed_window_handle(hwnd)
            return

        if self._vice_embed_attempts < 30:
            QTimer.singleShot(250, self._try_embed_vice_window)
            return

        self.vice_status_label.setText(
        share.locales.tr("VICE runs external - Window not found."))

    def _find_vice_window_handle(self):
        if self.vice_process is None:
            return None

        pid = int(self.vice_process.processId())
        if pid <= 0:
            return None

        user32  = ctypes.windll.user32
        found   = []

        EnumWindows              = user32.EnumWindows
        EnumWindowsProc          = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        IsWindowVisible          = user32.IsWindowVisible
        GetWindowThreadProcessId = user32.GetWindowThreadProcessId

        def callback(hwnd, lparam):
            proc_id = ctypes.c_ulong()
            GetWindowThreadProcessId(hwnd, ctypes.byref(proc_id))
            if proc_id.value == pid and IsWindowVisible(hwnd):
                found.append(hwnd)
                return False
            return True

        EnumWindows(EnumWindowsProc(callback), 0)
        return found[0] if found else None

    def _embed_window_handle(self, hwnd):
        self.vice_hwnd = hwnd

        user32          = ctypes.windll.user32
        GWL_STYLE       = -16
        WS_CHILD        = 0x40000000
        WS_POPUP        = 0x80000000
        WS_CAPTION      = 0x00C00000
        WS_THICKFRAME   = 0x00040000
        WS_MINIMIZEBOX  = 0x00020000
        WS_MAXIMIZEBOX  = 0x00010000
        WS_SYSMENU      = 0x00080000

        if ctypes.sizeof(ctypes.c_void_p) == 8:
            get_window_long = user32.GetWindowLongPtrW
            set_window_long = user32.SetWindowLongPtrW
        else:
            get_window_long = user32.GetWindowLongW
            set_window_long = user32.SetWindowLongW

        host_hwnd = int(self.vice_host.winId())
        user32.SetParent(hwnd, host_hwnd)

        style = get_window_long(hwnd, GWL_STYLE)
        
        style = style & ~WS_POPUP
        style = style & ~WS_CAPTION
        style = style & ~WS_THICKFRAME
        style = style & ~WS_MINIMIZEBOX
        style = style & ~WS_MAXIMIZEBOX
        style = style & ~WS_SYSMENU
        style = style |  WS_CHILD
        
        set_window_long(hwnd, GWL_STYLE, style)

        self._resize_embedded_vice()
        self.vice_status_label.setText("VICE eingebettet")

    def _resize_embedded_vice(self):
        if not self.vice_hwnd or sys.platform != "win32":
            return
        rect = self.vice_host.rect()
        ctypes.windll.user32.MoveWindow(
            self.vice_hwnd,
            0,
            0,
            max(1, rect.width()),
            max(1, rect.height()),
            True,
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_embedded_vice()

    def on_vice_stop_clicked(self):
        if self.vice_process is not None:
            try:
                self.vice_process.terminate()
                if not self.vice_process.waitForFinished(1500):
                    self.vice_process.kill()
            except Exception:
                pass
        self.vice_process = None
        self.vice_hwnd = None
        self.vice_status_label.setText(
        share.locales.tr("VICE not started."))

    def _on_vice_finished(self, *_):
        self.vice_process = None
        self.vice_hwnd = None
        self.vice_status_label.setText(
        share.locales.tr("VICE not running."))

    def closeEvent(self, event):
        self.remove_toolbar_actions()
        self.on_vice_stop_clicked()
        super().closeEvent(event)

    def clear_rows(self):
        if hasattr(self, "disasm_model"):
            self.disasm_model.clear()
        if hasattr(self, "hex_model"):
            self.hex_model.clear()

    def _make_row(self,
        offset      : int,
        address_text: str,
        hex_text    : str,
        mnemonic    : str,
        asm_text    : str,
        char_text   : str) -> QWidget:
        
        row = QFrame(self.content)
        row.setObjectName("c64DisasmRow")
        row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row.setStyleSheet(r"""
        QFrame#c64DisasmRow{background:#101010;border-bottom: 1px solid #202020;}
        QFrame#c64DisasmRow:hover{background:#181818;}""")

        lay = QHBoxLayout(row)
        lay.setContentsMargins(4, 1, 4, 1)
        lay.setSpacing(8)

        mono = QFont("Consolas", 10)
        mono.setStyleHint(QFont.Monospace)
        c64_font = QFont(self.c64_font_family, 10)
        c64_font.setStyleHint(QFont.Monospace)

        off = QLabel(address_text, row)
        off.setFont(mono)
        off.setMinimumWidth(70)
        off.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        off.setStyleSheet("color: #8fc7ff;")
        lay.addWidget(off)

        hex_label = QLabel(hex_text, row)
        hex_label.setFont(mono)
        hex_label.setMinimumWidth(130)
        hex_label.setStyleSheet("color: #dcdcdc;")
        lay.addWidget(hex_label)

        sep1 = QLabel("|", row)
        sep1.setStyleSheet("color: #666666;")
        lay.addWidget(sep1)

        asm = ClickableMnemonic(mnemonic, asm_text, row)
        asm.setFont(mono)
        asm.setMinimumWidth(185)
        asm.setStyleSheet("color: #ffd866; font-weight: bold;")
        asm.clicked.connect(self.open_opcode_help)
        lay.addWidget(asm)

        sep2 = QLabel("|", row)
        sep2.setStyleSheet("color: #666666;")
        lay.addWidget(sep2)

        edit = QLineEdit(char_text, row)
        edit.setReadOnly(True)
        edit.setFont(c64_font)
        edit.setMinimumWidth(260)
        edit.setCursorPosition(0)
        edit.setToolTip(share.locales.tr("This Byte-Code-String can not be mark and copy."))
        lay.addWidget(edit, 1)

        return row

    def on_disasm_table_clicked(self, index):
        if not index.isValid():
            return
        if index.column() == C64DisasmTableModel.COL_ASM:
            mnemonic = self.disasm_model.mnemonic_for_row(index.row())
            self.open_opcode_help(mnemonic)

    def on_disasm_table_double_clicked(self, index):
        if not index.isValid():
            return
        mnemonic = self.disasm_model.mnemonic_for_row(index.row())
        if mnemonic:
            self.open_opcode_help(mnemonic)

    def get_help_topic_id(self, mnemonic: str) -> str:
        m = (mnemonic or "").lower()

        if self.current_arch == DISASM_ARCH_C64:
            return "c64_asm_%s" % m

        if self.current_arch == DISASM_ARCH_AMIGA:
            return "amiga_asm_%s" % m

        if self.current_arch == DISASM_ARCH_INTEL32:
            return "intel32_asm_%s" % m

        if self.current_arch == DISASM_ARCH_INTEL64:
            return "intel64_asm_%s" % m

        return "asm_%s" % m

    def open_opcode_help(self, mnemonic: str):
        if not mnemonic or mnemonic == "???":
            QMessageBox.information(self,
            share.locales.tr("C64 Assembler"),
            share.locales.tr("No offical OpCode."))
            return

        topic_id = self.get_help_topic_id(mnemonic)
        target = self.main_window or self.window()

        for method_name in (
            "open_context_help",
            "open_help_topic",
            "show_help_topic",
            "open_help_keyword",
            "show_help_keyword",
        ):
            method = getattr(target, method_name, None)
            if callable(method):
                try:
                    method(topic_id)
                    return
                except TypeError:
                    try:
                        method(mnemonic)
                        return
                    except Exception:
                        pass
                except Exception:
                    pass

        QMessageBox.information(
            self,
            "C64 Assembler Hilfe",
            "Hilfe-Thema: %s\nMnemonic: %s" % (topic_id, mnemonic),
        )
        

def open_c64_disasm_viewer_from_menu(main_window, path: Optional[str] = None):
    if not path:
        txt = share.locales.tr("Open File...")
        dlg = QFileDialog(main_window, txt)
        dlg.setFileMode(QFileDialog.ExistingFile)

        filters = []
        language_profile = getattr(main_window, "language_profile", None)
        program_filter = getattr(language_profile, "program_name_filter", "")
        if program_filter:
            filters.append(program_filter)

        txt1 = share.locales.tr("All Files")
        txt2 = share.locales.tr("Files")
        txt3 = share.locales.tr("Images")
        
        filters.extend([
            f"C64/PRG/BIN (*.prg *.bin *.c64 *.rom)",
            f"Amiga {txt2} (*.adf *.hunk *.bin *.rom *.exe)",
            f"Intel 32-Bit {txt2} (*.exe *.dll *.obj *.com *.bin)",
            f"Assembler {txt2} (*.asm *.s *.inc)",
            f"Disk {txt3} (*.d64 *.d71 *.d81)",
            f"Tape {txt3} (*.tap *.t64)",
            f"Cartridge {txt3} (*.crt)",
            f"Amiga {txt2} (*.adf *.hunk *.exe *.bin *.rom)",
            f"Intel {txt2} (*.exe *.dll *.obj *.bin *.com)",
            f"{txt1} (*.*)",
        ])
        dlg.setNameFilters(filters)

        default_ext = getattr(language_profile, "default_source_extension", "")
        if default_ext:
            dlg.setDefaultSuffix(default_ext.lstrip("."))

        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if not dlg.exec_():
            return None
        files = dlg.selectedFiles()
        if not files:
            return None
        path = files[0]
        if not path:
            return None

    viewer = C64DisasmViewer(main_window=main_window)

    file_size = 0
    try:
        file_size = os.path.getsize(path)
    except Exception:
        pass

    txt1 = share.locales.tr("Disassemble File...")
    txt2 = share.locales.tr("Disassembler")
    txt3 = share.locales.tr("Cancel")
    
    progress = QProgressDialog(
        txt1, txt3,     0,
        max(1, file_size),
        main_window
    )
    progress.setWindowTitle(txt2)
    progress.setWindowModality(Qt.WindowModal)
    progress.setMinimumDuration(0)
    progress.show()
    QApplication.processEvents()

    viewer.load_file(path, progress)
    viewer.install_toolbar_actions()

    title  = f"{txt2} - %s" % os.path.basename(path)
    result = None

    if hasattr(main_window, "add_mdi_widget"):
        result = main_window.add_mdi_widget(viewer, title, 880, 420)
    else:
        mdi = getattr(main_window, "mdi", None)
        if mdi is not None:
            sub = mdi.addSubWindow(viewer)
            sub.setAttribute(Qt.WA_DeleteOnClose, True)
            sub.setWindowTitle(title)
            sub.resize(880, 420)
            try:
                sub.destroyed.connect(viewer.remove_toolbar_actions)
            except Exception:
                pass
            sub.show()
            result = sub
        else:
            viewer.setWindowTitle(title)
            viewer.resize(880, 420)
            viewer.show()
            result = viewer

    QApplication.processEvents()
    progress.close()
    return result


def install_c64_disasm_menu_action(main_window, file_menu=None):
    action = QAction("Disassembler Datei laden...", main_window)
    action.setObjectName("actionLoadC64DisasmViewer")
    action.triggered.connect(lambda: open_c64_disasm_viewer_from_menu(main_window))

    if file_menu is not None:
        file_menu.addAction(action)
    else:
        menu_bar = main_window.menuBar()
        menu = None
        for a in menu_bar.actions():
            if a.text().replace("&", "").lower() in ("datei", "file"):
                menu = a.menu()
                break
        if menu is None:
            menu = menu_bar.addMenu("Datei")
        menu.addAction(action)

    return action
