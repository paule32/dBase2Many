# ---------------------------------------------------------------------------
# File:   dialogs.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from   __future__          import annotations
from   share.common        import *

import share.locales
from   share.locales       import *
from   share.utildef.theme import *

class CollectProgressDialog(QDialog):
    def __init__(self, parent=None, filename: str = ""):
        super().__init__(parent)
        
        self.cancel_requested = False
        self.total_lines      = 0
        self.current_lines    = 0
        self.class_count      = 0
        self.method_count     = 0
        self.start_time       = time.monotonic()
        self._recent_hits: list[str] = []

        self.setWindowTitle(share.locales.tr("Collect-Phase"))
        self.setModal(False)
        self.resize(460, 360)
        share.utildef.theme.apply_theme_global(self)

        layout = QVBoxLayout(self)

        self.lbl_status = QLabel(share.locales.tr("Sammle Informationen ..."))
        self.lbl_file   = QLabel(share.locales.tr("File:")  + filename)
        self.lbl_line   = QLabel(share.locales.tr("Zeile")  + ": 0 / 0")
        self.lbl_class  = QLabel(share.locales.tr("CLASSs") + ": 0")
        self.lbl_method = QLabel(share.locales.tr("METHOD") + ": 0")
        self.lbl_count  = QLabel(share.locales.tr("Lines")  + ": 0")
        self.lbl_time   = QLabel(share.locales.tr("Time")   + ": 0,0 s")
        self.lbl_hit    = QLabel(share.locales.tr("Letzter Treffer: —"))

        layout.addWidget(self.lbl_status)
        layout.addWidget(self.lbl_file)
        layout.addWidget(self.lbl_line)
        layout.addWidget(self.lbl_class)
        layout.addWidget(self.lbl_method)
        layout.addWidget(self.lbl_count)
        layout.addWidget(self.lbl_time)
        layout.addWidget(self.lbl_hit)

        self.progress = QProgressBar(self)
        self.progress.setMinimum(0)
        self.progress.setMaximum(0)
        layout.addWidget(self.progress)

        self.current_text = QPlainTextEdit(self)
        self.current_text.setReadOnly(True)
        self.current_text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.current_text.setPlaceholderText(share.locales.tr("Aktuelle Zeile ..."))
        layout.addWidget(self.current_text, 1)

        self.recent_text = QPlainTextEdit(self)
        self.recent_text.setReadOnly(True)
        self.recent_text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.recent_text.setMaximumHeight(90)
        self.recent_text.setPlaceholderText(share.locales.tr("Letzte erkannte Einträge ..."))
        layout.addWidget(self.recent_text)

        btn_row = QHBoxLayout()
        btn_row.addStretch()

        self.btn_ok = QPushButton(share.locales.tr("OK"), self)
        self.btn_ok.setEnabled(False)
        self.btn_ok.clicked.connect(self.accept)

        self.btn_cancel = QPushButton(share.locales.tr("Cancel"), self)
        self.btn_cancel.clicked.connect(self._on_cancel)

        btn_row.addWidget(self.btn_ok)
        btn_row.addWidget(self.btn_cancel)
        layout.addLayout(btn_row)

    def _pump(self):
        app = QApplication.instance()
        if app is not None:
            app.processEvents()

    def _format_elapsed(self) -> str:
        elapsed = max(0.0, time.monotonic() - self.start_time)
        return f"{elapsed:0.1f}".replace(".", ",")

    def _extract_hit(self, line_text: str) -> str:
        raw = (line_text or "").strip()
        if not raw:
            return ""
        m = re.match(r'^\s*CLASS\s+([A-Za-z_]\w*)', raw, flags=re.IGNORECASE)
        if m:
            return f"CLASS  {m.group(1)}"
        m = re.match(r'^\s*METHOD\s+([A-Za-z_]\w*)', raw, flags=re.IGNORECASE)
        if m:
            return f"METHOD {m.group(1)}"
        m = re.match(r'^\s*#include\s+"([^"]+)"', raw, flags=re.IGNORECASE)
        if m:
            return f'INCLUDE {m.group(1)}'
        return ""

    def _append_hit(self, hit: str):
        hit = (hit or "").strip()
        if not hit:
            return
        if self._recent_hits and self._recent_hits[-1] == hit:
            return
        self._recent_hits.append(hit)
        self._recent_hits = self._recent_hits[-8:]
        self.lbl_hit.setText(f"{share.locales.tr("Letzter Treffer")}: {hit}")
        self.recent_text.setPlainText("\n".join(self._recent_hits))

    def _on_cancel(self):
        self.cancel_requested = True
        self.reject()

    def set_total_lines(self, total: int):
        self.total_lines = max(0, int(total or 0))
        self.progress.setMaximum(max(1, self.total_lines))
        self.progress.setValue(0)
        self.lbl_line.setText(f"{share.locales.tr("Line")}: 0 / {self.total_lines}")
        self.lbl_time.setText(f"{share.locales.tr("Time")}: {self._format_elapsed()} s")
        self._pump()

    def update_progress(self, *,
        line_no     : int        =  0,
        line_text   : str        = "",
        class_count : int | None = None,
        method_count: int | None = None,
        line_count  : int | None = None,
        status      : str | None = None):
        
        if status is not None:
            self.lbl_status.setText(status)
        if line_no:
            self.current_lines = int(line_no)
            self.progress.setValue(min(self.progress.maximum(), max(0, self.current_lines)))
        if class_count is not None:
            self.class_count = int(class_count)
        if method_count is not None:
            self.method_count = int(method_count)
        if line_count is None:
            line_count = self.current_lines
        self.lbl_line  .setText(f"{share.locales.tr("Line"  )}: {self.current_lines} / {self.total_lines}")
        self.lbl_class .setText(f"{share.locales.tr("CLASS" )}: {self.class_count}")
        self.lbl_method.setText(f"{share.locales.tr("METHOD")}: {self.method_count}")
        self.lbl_count .setText(f"{share.locales.tr("Lines" )}: {int(line_count)}")
        self.lbl_time  .setText(f"{share.locales.tr("Time"  )}: {self._format_elapsed()} s")
        self.current_text.setPlainText(line_text or "")
        self._append_hit(self._extract_hit(line_text))
        self._pump()
        return not self.cancel_requested

    def set_ready(self, *,
        class_count: int   = 0,
        method_count: int  = 0,
        line_count: int    = 0):
        self.class_count   = int(class_count)
        self.method_count  = int(method_count)
        self.current_lines = max(self.current_lines, self.total_lines)
        self.progress  .setValue(self.progress.maximum())
        self.lbl_status.setText(share.locales.tr("Collect-Phase abgeschlossen. Mit OK starten oder mit Cancel abbrechen."))
        self.lbl_line  .setText(f"{share.locales.tr("Line"  )}: {self.current_lines} / {self.total_lines}")
        self.lbl_class .setText(f"{share.locales.tr("CLASS" )}: {self.class_count}")
        self.lbl_method.setText(f"{share.locales.tr("METHOD")}: {self.method_count}")
        self.lbl_count .setText(f"{share.locales.tr("Lines" )}: {int(line_count)}")
        self.lbl_time  .setText(f"{share.locales.tr("Time"  )}: {self._format_elapsed()} s")
        self.btn_ok.setEnabled(True)
        self._pump()

class InputValueDialog(QDialog):
    def __init__(self, prompt: str = "", parent=None):
        super().__init__(parent)
        self._value = ""
        self._rc = 0

        self.setWindowTitle(share.locales.tr("Input"))
        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(360, 120)
        share.utildef.theme.apply_theme_global(self)

        layout = QVBoxLayout(self)

        self.lbl_prompt = QLabel(str(prompt or ""), self)
        self.lbl_prompt.setWordWrap(True)
        layout.addWidget(self.lbl_prompt)

        self.edit = QLineEdit(self)
        layout.addWidget(self.edit)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        self.btn_ok     = QPushButton(share.locales.tr("OK"),     self)
        self.btn_cancel = QPushButton(share.locales.tr("Cancel"), self)

        self.btn_ok.clicked.connect(self._on_ok)
        self.btn_cancel.clicked.connect(self._on_cancel)
        self.edit.returnPressed.connect(self._on_ok)

        btn_row.addWidget(self.btn_ok)
        btn_row.addWidget(self.btn_cancel)
        layout.addLayout(btn_row)

        self.edit.setFocus()

    def _on_ok(self):
        self._value = self.edit.text()
        self._rc = 1
        self.accept()

    def _on_cancel(self):
        self._value = ""
        self._rc = 0
        self.reject()

    def get_result(self):
        return self._value, self._rc

    @staticmethod
    def get_value(prompt: str = "", parent=None):
        dlg = InputValueDialog(prompt=prompt, parent=parent)
        dlg.exec_()
        return dlg.get_result()
