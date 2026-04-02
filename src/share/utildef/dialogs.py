# ---------------------------------------------------------------------------
# File:   dialogs.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations
from share.common import *

class InputValueDialog(QDialog):
    def __init__(self, prompt: str = "", parent=None):
        super().__init__(parent)
        self._value = ""
        self._rc = 0

        self.setWindowTitle("Eingabe")
        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(360, 120)

        layout = QVBoxLayout(self)

        self.lbl_prompt = QLabel(str(prompt or ""), self)
        self.lbl_prompt.setWordWrap(True)
        layout.addWidget(self.lbl_prompt)

        self.edit = QLineEdit(self)
        layout.addWidget(self.edit)

        btn_row = QHBoxLayout()
        btn_row.addStretch(1)

        self.btn_ok = QPushButton("OK", self)
        self.btn_cancel = QPushButton("Cancel", self)

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
