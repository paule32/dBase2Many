# ---------------------------------------------------------------------------
# File:   excepts.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations
from share.common import *

# ---------------------------------------------------------------------------
# Exception classes ...
# ---------------------------------------------------------------------------
class ReturnSignal(Exception):
    def __init__(self, value=None, has_value: bool = False):
        super().__init__(self, value)
        self.value = value
        self.has_value = has_value

# ---------------------------------------------------------------------------
# Stoppt die aktuelle dBase-Abarbeitung kontrolliert und kehrt zur GUI zurück
# ---------------------------------------------------------------------------
class ProgramAbortSignal(Exception):
    pass

class UnterminatedBlockCommentError(Exception):
    def __init__(self, line, column, message="unterminated block comment"):
        super().__init__(f"{line}:{column}: {message}")
        self.line    = line
        self.column  = column
        self.message = message

class KeyError(Exception):
    def __init__(self, name, message="Zuordnungs-Fehler"):
        super().__init__(self, name)
        self.name    = name
        self.message = message

# ---------------------------------------------------------------------------
# Interner Control-Flow für BREAK (nur Schleifen fangen das ab).
# ---------------------------------------------------------------------------
class BreakSignal(Exception):
    pass

class PreprocessorError(Exception):
    pass

# ---------------------------------------------------------------------------
# Interner Control-Flow für RETURN aus einer Methode.
# ---------------------------------------------------------------------------
class RuntimeReturn(Exception):
    def __init__(self, value=None):
        self.value = value

# ---------------------------------------------------------------------------
# Qt5 Application stuff ...
# ---------------------------------------------------------------------------
class showException(QDialog):
    def __init__(self, parent=None, etype: str="Ausnahme", message: str=""):
        super().__init__(parent)
        self.setWindowTitle("Demo: " + etype)
        self.resize(320, 200)
        self.message = message
        
        layout = QVBoxLayout(self)
        
        self.text = QTextEdit(self)
        self.text.setText(self.message)
        
        layout.addWidget(self.text)
        
        self.btn = QPushButton("Schließen", self)
        self.btn.clicked.connect(self.on_button_clicked)
        
        layout.addWidget(self.btn)
        
    def on_button_clicked(self):
        self.close()
