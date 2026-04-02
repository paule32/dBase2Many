# ---------------------------------------------------------------------------
# \file  : highlight.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations
from share.common import *

class ccHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # --- Formate ---
        self.fmt_keyword = QTextCharFormat()
        self.fmt_keyword.setFontWeight(QFont.Bold)
        self.fmt_keyword.setForeground(QColor(200, 200, 0))  # schwarz

        self.fmt_comment = QTextCharFormat()
        self.fmt_comment.setForeground(QColor(0, 148, 0))  # grün

        # --- Keywords (nach Bedarf erweitern) ---
        keywords = [
            "FOR", "ENDFOR", "CLASS", "ENDCLASS", "METHOD", "ENDMETHOD",
            "IF", "ENDIF", "ELSE", "DO", "CASE", "ENDCASE", "OTHERWISE",
            "WHILE", "ENDDO", "RETURN", "LOCAL", "PARAMETER", "WITH",
            "ENDWITH", "NEW", "OF", "OBJECT", "THIS", "SUPER",
            "TRUE", "FALSE", "TEXT", "ENDTEXT", "ERASE",
            "FORMAT", "PRINT", "SCREEN", "ON", "OFF", "MARGIN", "ESCAPE"
        ]

        self.rules = []
        for kw in keywords:
            # \bKW\b = ganzes Wort, case-insensitive
            rx = QRegExp(rf"\b{kw}\b", Qt.CaseInsensitive)
            self.rules.append((rx, self.fmt_keyword))

        # --- Line comments: NOTE, //, **, && bis Zeilenende ---
        self.rules.append((QRegExp(r"\bNOTE\b[^\n]*", Qt.CaseInsensitive), self.fmt_comment))
        self.rules.append((QRegExp(r"//[^\n]*"), self.fmt_comment))
        self.rules.append((QRegExp(r"\*\*[^\n]*"), self.fmt_comment))
        self.rules.append((QRegExp(r"&&[^\n]*"), self.fmt_comment))

        # --- Block comments: /* ... */ (mehrzeilig) ---
        self.block_start = QRegExp(r"/\*")
        self.block_end   = QRegExp(r"\*/")

    def highlightBlock(self, text: str):
        # 1) normale Regeln (Keywords + Single-line comments)
        for rx, fmt in self.rules:
            i = rx.indexIn(text, 0)
            while i >= 0:
                length = rx.matchedLength()
                self.setFormat(i, length, fmt)
                i = rx.indexIn(text, i + length)

        # 2) Block comments mehrzeilig
        self.setCurrentBlockState(0)

        start = 0
        if self.previousBlockState() != 1:
            start = self.block_start.indexIn(text, 0)
        else:
            start = 0

        while start >= 0:
            end = self.block_end.indexIn(text, start)
            if end == -1:
                # Kommentar geht in nächste Zeile weiter
                self.setCurrentBlockState(1)
                length = len(text) - start
            else:
                length = (end - start) + self.block_end.matchedLength()

            self.setFormat(start, length, self.fmt_comment)

            if end == -1:
                break
            start = self.block_start.indexIn(text, start + length)
