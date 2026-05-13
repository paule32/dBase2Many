# ---------------------------------------------------------------------------
# File:   c64_disasm_viewer.py
# Author: add-on for dBase2Many
# Purpose: C64/6502 byte viewer + disassembler as MDI sub window
# ---------------------------------------------------------------------------
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Tuple, Optional
from share.common import *

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
    """
    QPlainTextEdit mit BASIC-artigem Zeilen-Gutter.

    Neue Zeilen am Ende werden in 10er-Schritten nummeriert:
        10, 20, 30, 40, ...

    Neue Zeilen zwischen vorhandenen Zeilen bekommen +1 zur vorherigen Zeile:
        10, 11, 12, 20, 21, 30, ...
    """
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
        self.mnemonic = mnemonic
        self.setCursor(Qt.PointingHandCursor)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        self.setToolTip("Hilfe zu %s anzeigen" % mnemonic)

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


def format_c64_disasm_line(data: bytes, offset: int) -> Tuple[str, str, str, str, int]:
    """
    Erstellt eine synchrone Disassembler-Zeile.

    Die Hex-Bytefolge enthält exakt die Bytes der aktuellen
    Assembler-Instruktion. Dadurch bleiben Hex-Spalte,
    Assembler-Code und Zeichen-Spalte zusammen.

    Rückgabe:
        hex_text, mnemonic, asm_text, char_text, used
    """
    mnemonic, asm_text, used = disassemble_one(data, offset)

    if used <= 0:
        used = 1

    instr_bytes = data[offset:offset + used]
    if not instr_bytes:
        instr_bytes = data[offset:offset + 1]

    used = max(1, len(instr_bytes))

    hex_text = " ".join("%02X" % b for b in instr_bytes)
    char_text = "".join(c64_char(b) for b in instr_bytes)

    return hex_text, mnemonic, asm_text, char_text, used


class C64DisasmViewer(QWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.file_path: Optional[str] = None
        self.bytes_per_row = 8
        self.c64_font_family = self._load_c64_font()
        self._build_ui()

    def load_file(self, file_path: str):
        self.file_path = file_path

        with open(file_path, "rb") as f:
            data = f.read()

        progress = QProgressDialog(
            "Datei wird disassembliert...",
            "Abbrechen",
            0,
            len(data),
            self
        )
        progress.setWindowTitle("C64 Disassembler")
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)

        self.render_bytes(data, progress)

        progress.close()
        self.info_label.setText("%s  -  %d Bytes" % (file_path, len(data)))

    def render_bytes(self, data: bytes, progress=None):
        self.clear_rows()
        pos = 0

        while pos < len(data):
            if progress is not None:
                progress.setValue(pos)

                if progress.wasCanceled():
                    break

                QApplication.processEvents()

            address_text, hex_text, mnemonic, asm_text, char_text, used = format_c64_disasm_line(data, pos)

            self.rows.insertWidget(
                self.rows.count() - 1,
                self._make_row(
                    pos,
                    address_text,
                    hex_text,
                    mnemonic,
                    asm_text,
                    char_text
                )
            )

            pos += used

        if progress is not None:
            progress.setValue(len(data))

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

        self.info_label = QLabel("Keine Datei geladen", self.left_panel)
        self.info_label.setStyleSheet("color: #d7d7d7;")
        self.left_layout.addWidget(self.info_label)

        self.left_vertical_splitter = QSplitter(Qt.Vertical, self.left_panel)
        self.left_vertical_splitter.setChildrenCollapsible(False)
        self.left_layout.addWidget(self.left_vertical_splitter, 1)

        self.listing_panel = QWidget(self.left_vertical_splitter)
        self.listing_layout = QVBoxLayout(self.listing_panel)
        self.listing_layout.setContentsMargins(0, 0, 0, 0)
        self.listing_layout.setSpacing(0)

        self.scroll = QScrollArea(self.listing_panel)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.content = QWidget()
        self.rows = QVBoxLayout(self.content)
        self.rows.setContentsMargins(2, 2, 2, 2)
        self.rows.setSpacing(1)
        self.rows.addStretch(1)

        self.scroll.setWidget(self.content)
        self.listing_layout.addWidget(self.scroll, 1)

        self.bottom_splitter = QSplitter(Qt.Horizontal, self.left_vertical_splitter)
        self.bottom_splitter.setChildrenCollapsible(False)

        self.left_plain_edit = BasicNumberedPlainTextEdit(self.bottom_splitter)
        self.left_plain_edit.setPlaceholderText("BASIC / Labels / Kommentare ...")

        self.right_plain_edit = QPlainTextEdit(self.bottom_splitter)
        self.right_plain_edit.setPlaceholderText("VICE / Monitor / Ausgabe ...")
        self.right_plain_edit.setLineWrapMode(QPlainTextEdit.NoWrap)

        edit_font = QFont("Consolas", 10)
        edit_font.setStyleHint(QFont.Monospace)
        self.left_plain_edit.setFont(edit_font)
        self.right_plain_edit.setFont(edit_font)

        self.bottom_splitter.addWidget(self.left_plain_edit)
        self.bottom_splitter.addWidget(self.right_plain_edit)
        self.bottom_splitter.setStretchFactor(0, 1)
        self.bottom_splitter.setStretchFactor(1, 1)
        self.bottom_splitter.setSizes([330, 330])

        self.left_vertical_splitter.addWidget(self.listing_panel)
        self.left_vertical_splitter.addWidget(self.bottom_splitter)
        self.left_vertical_splitter.setStretchFactor(0, 3)
        self.left_vertical_splitter.setStretchFactor(1, 1)
        self.left_vertical_splitter.setSizes([430, 160])

        self.vice_host = QWidget(self.right_panel)
        self.vice_host.setMinimumWidth(360)
        self.vice_host.setStyleSheet("""
            QWidget {
                background: #000000;
                border: 1px solid #444444;
            }
        """)
        self.right_layout.addWidget(self.vice_host, 1)

        self._toolbar_actions = []
        self._toolbar = None

        self.setStyleSheet("""
            C64DisasmViewer { background: #101010; }
            QScrollArea { background: #101010; }
            QLabel { color: #e6e6e6; }
            QPlainTextEdit {
                color: #ffffff;
                background: #181818;
                border: 1px solid #333333;
                selection-background-color: #315a90;
            }
            QLineEdit {
                color: #ffffff;
                background: #181818;
                border: 1px solid #333333;
                padding: 1px 4px;
                selection-background-color: #315a90;
            }
            QSplitter::handle {
                background: #303030;
            }
            QSplitter::handle:hover {
                background: #505050;
            }
        """)

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
        self.action_vice_start.setToolTip("VICE starten / einbetten")
        self.action_vice_start.triggered.connect(self.on_vice_start_clicked)

        self.action_vice_stop = QAction(
            style.standardIcon(QStyle.SP_MediaStop),
            "VICE beenden",
            self
        )
        self.action_vice_stop.setObjectName("actionC64ViceStop")
        self.action_vice_stop.setToolTip("VICE beenden")
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

    def on_vice_start_clicked(self):
        QMessageBox.information(
            self,
            "VICE",
            "VICE-Start ist vorbereitet. Hier kann später QProcess + Window-Embedding angeschlossen werden."
        )

    def on_vice_stop_clicked(self):
        QMessageBox.information(
            self,
            "VICE",
            "VICE-Stopp ist vorbereitet."
        )

    def closeEvent(self, event):
        self.remove_toolbar_actions()
        super().closeEvent(event)

    """def load_file(self, file_path: str):
        self.file_path = file_path
        with open(file_path, "rb") as f:
            data = f.read()
        self.render_bytes(data)
        self.info_label.setText("%s  -  %d Bytes" % (file_path, len(data)))"""

    def clear_rows(self):
        while self.rows.count() > 0:
            item = self.rows.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        self.rows.addStretch(1)

    """def render_bytes(self, data: bytes):
        self.clear_rows()
        pos = 0
        while pos < len(data):
            hex_text, mnemonic, asm_text, char_text, used = format_c64_disasm_line(data, pos)
            self.rows.insertWidget(
                self.rows.count() - 1,
                self._make_row(pos, hex_text, mnemonic, asm_text, char_text)
            )
            pos += used"""

    def _make_row(self, offset: int, hex_text: str, mnemonic: str, asm_text: str, char_text: str) -> QWidget:
        row = QFrame(self.content)
        row.setObjectName("c64DisasmRow")
        row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        row.setStyleSheet("""
            QFrame#c64DisasmRow { background: #101010; border-bottom: 1px solid #202020; }
            QFrame#c64DisasmRow:hover { background: #181818; }
        """)

        lay = QHBoxLayout(row)
        lay.setContentsMargins(4, 1, 4, 1)
        lay.setSpacing(8)

        mono = QFont("Consolas", 10)
        mono.setStyleHint(QFont.Monospace)
        c64_font = QFont(self.c64_font_family, 10)
        c64_font.setStyleHint(QFont.Monospace)

        off = QLabel("%04X:" % (offset & 0xFFFF), row)
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
        edit.setToolTip("Dieser Byte-Code-String kann markiert und kopiert werden.")
        lay.addWidget(edit, 1)

        return row

    def open_opcode_help(self, mnemonic: str):
        if not mnemonic or mnemonic == "???":
            QMessageBox.information(self, "C64 Assembler", "Kein offizieller Opcode für dieses Byte.")
            return

        topic_id = "c64_asm_%s" % mnemonic.lower()
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
        dlg = QFileDialog(main_window, "Open File...")
        dlg.setFileMode(QFileDialog.ExistingFile)

        filters = []
        language_profile = getattr(main_window, "language_profile", None)
        program_filter = getattr(language_profile, "program_name_filter", "")
        if program_filter:
            filters.append(program_filter)

        filters.extend([
            "C64/PRG/BIN (*.prg *.bin *.c64 *.rom)",
            "Assembler Files (*.asm *.s *.inc)",
            "Disk Images (*.d64 *.d71 *.d81)",
            "Tape Images (*.tap *.t64)",
            "Cartridge Images (*.crt)",
            "All Files (*.*)",
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
    viewer.load_file(path)
    viewer.install_toolbar_actions()

    title = "C64 Disassembler - %s" % os.path.basename(path)

    if hasattr(main_window, "add_mdi_widget"):
        return main_window.add_mdi_widget(viewer, title, 780, 420)

    mdi = getattr(main_window, "mdi", None)
    if mdi is not None:
        sub = mdi.addSubWindow(viewer)
        sub.setAttribute(Qt.WA_DeleteOnClose, True)
        sub.setWindowTitle(title)
        sub.resize(780, 420)
        try:
            sub.destroyed.connect(viewer.remove_toolbar_actions)
        except Exception:
            pass
        sub.show()
        return sub

    viewer.setWindowTitle(title)
    viewer.resize(780, 420)
    viewer.show()
    return viewer


def install_c64_disasm_menu_action(main_window, file_menu=None):
    action = QAction("C64 Datei laden...", main_window)
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
