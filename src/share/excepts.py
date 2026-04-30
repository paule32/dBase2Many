# ---------------------------------------------------------------------------
# File:   excepts.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__    import annotations
from share.common  import *
#from share.locales import tr
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

class ErrorMessage(QDialog):
    def __init__(self, title="Error", message="", log_path=None, parent=None):
        super().__init__(parent)
        
        self.log_path = log_path  # Pfad zur Logdatei (oder None)
        
        self.setWindowTitle(self.tr(title))
        self.resize(750, 420)
        
        layout = QVBoxLayout(self)
        
        # Textbereich
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(message)
        self.text_edit.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        self.text_edit.setFont(font)
        
        layout.addWidget(self.text_edit)
        
        # Button-Leiste
        btn_row = QHBoxLayout()
        
        self.btn_delete_log = QPushButton(self.tr("Delete LOG"))
        self.btn_delete_log.clicked.connect(self._on_delete_log_clicked)
        self.btn_delete_log.setEnabled(bool(self.log_path))  # nur aktiv, wenn Pfad vorhanden
        
        btn_style = """QPushButton {
        background-color: #2f2f2f;
        color: white;
        border: 1px solid black;
        }"""
        self.btn_delete_log.setStyleSheet(btn_style)
        
        btn_row.addWidget(self.btn_delete_log)
        btn_row.addStretch()
        
        self.btn_close = QPushButton(self.tr("Close"))
        self.btn_close.clicked.connect(self.accept)
        self.btn_close.setStyleSheet(btn_style)
        
        btn_row.addWidget(self.btn_close)
        layout.addLayout(btn_row)

    def _on_delete_log_clicked(self):
        if not self.log_path:
            return
        if not os.path.exists(self.log_path):
            QMessageBox.information(
                self,
                "LOG nicht gefunden",
                "Die LOG-Datei existiert nicht (mehr)."
            )
            return
        err = tr("remove LOG file?")
        answer = QMessageBox.question(
            self,
            tr("delete LOG file?"),
            f"{err}\n\n{self.log_path}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if answer != QMessageBox.Yes:
            return
        try:
            with open(LOG, "w", encoding="utf-8"):
                pass
            os.remove(self.log_path)
        except Exception as e:
            err = tr("LOG file could not remove")
            QMessageBox.critical(
                self,
                tr("remove file diened."),
                f"{err}:\n{e}"
            )
            return
        QMessageBox.information(
            self,
            tr("removed"),
            tr("LOG file have been removed")
        )
        # Optional: Button deaktivieren, weil Datei weg ist
        self.btn_delete_log.setEnabled(False)

def exception_info(e):
    last = traceback.extract_tb(e.__traceback__)[-1]
    return {
        "file": last.filename,
        "line": last.lineno,
        "function": last.name,
        "code": last.line,
        "error": str(e),
    }
