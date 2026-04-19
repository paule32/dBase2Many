import json
import os
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QTabWidget, QTextEdit, QScrollArea, QFrame,
    QFileDialog, QMessageBox
)


DOXYGEN_EXPERT_ITEMS = [
    "Project", "Build", "Messages", "Input", "Source Browser", "Index",
    "HTML", "LaTeX", "RTF", "Man", "XML", "DocBook", "AutoGen",
    "SQLite3", "PerlMod", "Preprocessor", "External", "Dot"
]

HEADER_FORMAT = "dBase2Many Project File"
HEADER_TOOL = "doxygen-dialog"
HEADER_KIND = "doxygen-project"
HEADER_VERSION = 1


def _default_project_dir() -> Path:
    base = Path.home() / "Documents" / "dBase2Many" / "DoxygenProjects"
    base.mkdir(parents=True, exist_ok=True)
    return base


class ProjectListItemWidget(QWidget):
    def __init__(self, filename: str, dt_text: str, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(6, 4, 6, 4)
        lay.setSpacing(0)

        self.lbl_name = QLabel(filename)
        self.lbl_name.setStyleSheet("QLabel { font: 10pt Arial; color: white; }")
        lay.addWidget(self.lbl_name)

        self.lbl_dt = QLabel(dt_text)
        self.lbl_dt.setStyleSheet("QLabel { font: 8pt Arial; color: #c0c0c0; }")
        lay.addWidget(self.lbl_dt)


class MeineKlasse(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_dir = _default_project_dir()
        self.current_project_path = ""
        self._build_ui()
        self._reload_project_list()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)

        self.main_splitter = QSplitter(Qt.Horizontal)
        root.addWidget(self.main_splitter)

        self.left_host = QWidget()
        left_lay = QVBoxLayout(self.left_host)
        left_lay.setContentsMargins(0, 0, 0, 0)

        self.project_list = QListWidget()
        self.project_list.itemDoubleClicked.connect(self._load_selected_project)
        left_lay.addWidget(self.project_list, 1)

        btn_row = QHBoxLayout()
        self.btn_save = QPushButton("Speichern")
        self.btn_delete = QPushButton("Löschen")
        self.btn_load = QPushButton("Laden")
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_delete)
        btn_row.addWidget(self.btn_load)
        left_lay.addLayout(btn_row)

        self.btn_save.clicked.connect(self._save_project_as)
        self.btn_delete.clicked.connect(self._delete_selected_project)
        self.btn_load.clicked.connect(self._load_selected_project)

        self.main_splitter.addWidget(self.left_host)

        self.right_host = QWidget()
        right_lay = QVBoxLayout(self.right_host)
        right_lay.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        right_lay.addWidget(self.tabs)
        self.main_splitter.addWidget(self.right_host)
        self.main_splitter.setSizes([260, 940])

        self.tabs.addTab(self._build_wizard_tab(), "Wizard")
        self.tabs.addTab(self._build_expert_tab(), "Expert")
        self.tabs.addTab(self._build_run_tab(), "Run")

        self.setStyleSheet(
            "QWidget { background:#131313; color:white; }"
            "QListWidget { background:#171717; border:1px solid #333333; }"
            "QPushButton { background:#1a1a1a; color:#ffd84d; border:1px solid #3a3a3a; padding:5px 10px; font: 9pt Arial; }"
            "QPushButton:hover { background:#242424; }"
            "QTabWidget::pane { border:1px solid #333333; }"
            "QTabBar::tab { background:#1b1b1b; color:#ffd84d; padding:6px 10px; }"
            "QTextEdit { background:#1b1b1b; color:white; border:1px solid #333333; font: 10pt Arial; }"
        )

    def _build_wizard_tab(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        txt = QTextEdit()
        txt.setReadOnly(False)
        txt.setHtml("<b>DoxyGen Wizard</b><br><p>Hier kann später der geführte Assistent erweitert werden.</p>")
        lay.addWidget(txt)
        self.wizard_text = txt
        return page

    def _build_expert_tab(self):
        page = QWidget()
        page_lay = QVBoxLayout(page)
        page_lay.setContentsMargins(0, 0, 0, 0)

        self.expert_splitter_v = QSplitter(Qt.Vertical)
        page_lay.addWidget(self.expert_splitter_v)

        top_host = QWidget()
        top_lay = QVBoxLayout(top_host)
        top_lay.setContentsMargins(0, 0, 0, 0)

        self.expert_splitter_h = QSplitter(Qt.Horizontal)
        top_lay.addWidget(self.expert_splitter_h)

        self.list_categories = QListWidget()
        self.list_categories.addItems(DOXYGEN_EXPERT_ITEMS)
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        scroll_lay = QVBoxLayout(self.scroll_widget)
        scroll_lay.setContentsMargins(8, 8, 8, 8)

        self.lbl_expert_title = QLabel("<b>Project</b>")
        self.lbl_expert_title.setTextFormat(Qt.RichText)
        scroll_lay.addWidget(self.lbl_expert_title)

        self.lbl_expert_info = QLabel("Hier können projektspezifische Doxygen-Einstellungen eingeblendet werden.")
        self.lbl_expert_info.setWordWrap(True)
        scroll_lay.addWidget(self.lbl_expert_info)

        for idx in range(6):
            row = QFrame()
            row.setFrameShape(QFrame.StyledPanel)
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(8, 6, 8, 6)
            row_lay.addWidget(QLabel(f"Option {idx + 1}"))
            row_lay.addStretch(1)
            row_lay.addWidget(QPushButton("Bearbeiten"))
            scroll_lay.addWidget(row)

        scroll_lay.addStretch(1)
        self.scroll_area.setWidget(self.scroll_widget)
        self.expert_splitter_h.addWidget(self.scroll_area)
        self.expert_splitter_h.setSizes([220, 700])

        self.html_preview = QTextEdit()
        self.html_preview.setAcceptRichText(True)
        self.html_preview.setHtml(
            "<b>Project</b><br><p>Hier erscheinen einfache HTML-formatierte Texte. "
            "Zum Beispiel ist <b>foo</b> fett.</p>"
        )
        self.expert_splitter_v.addWidget(top_host)
        self.expert_splitter_v.addWidget(self.html_preview)
        self.expert_splitter_v.setSizes([420, 180])

        self.list_categories.setCurrentRow(0)
        return page

    def _build_run_tab(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        txt = QTextEdit()
        txt.setReadOnly(False)
        txt.setHtml("<b>DoxyGen Run</b><br><p>Hier können Lauf-Ausgaben und Hinweise stehen.</p>")
        lay.addWidget(txt)
        self.run_text = txt
        return page

    def _on_expert_item_changed(self, text):
        if not text:
            return
        self.lbl_expert_title.setText(f"<b>{text}</b>")
        self.lbl_expert_info.setText(f"Dies ist der Platzhalterbereich für <b>{text}</b>.")
        self.html_preview.setHtml(
            f"<b>{text}</b><br><p>Hier können HTML-formatierte Hinweise für <b>{text}</b> angezeigt werden.</p>"
        )

    def _project_payload(self, path: str) -> dict:
        now = datetime.now()
        p = Path(path)
        return {
            "header": {
                "format": HEADER_FORMAT,
                "tool": HEADER_TOOL,
                "kind": HEADER_KIND,
                "version": HEADER_VERSION,
            },
            "meta": {
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "filename": p.name,
                "filepath": str(p),
            },
            "state": {
                "current_tab": self.tabs.currentIndex(),
                "expert_item": self.list_categories.currentRow(),
                "wizard_html": self.wizard_text.toHtml(),
                "expert_html": self.html_preview.toHtml(),
                "run_html": self.run_text.toHtml(),
            },
        }

    def _validate_payload(self, data: dict):
        if not isinstance(data, dict):
            return False, "Die JSON-Datei enthält kein gültiges Projektobjekt."
        header = data.get("header")
        if not isinstance(header, dict):
            return False, "Die Header-Informationen fehlen."
        if header.get("format") != HEADER_FORMAT:
            return False, "Ungültiges dBase2Many-Projektformat."
        if header.get("tool") != HEADER_TOOL:
            return False, f"Die JSON-Datei gehört nicht zum DoxyGen Dialog (gefunden: {header.get('tool', 'unbekannt')})."
        if header.get("kind") != HEADER_KIND:
            return False, "Ungültiger Projekttyp für den DoxyGen Dialog."
        return True, ""

    def _reload_project_list(self):
        self.project_list.clear()
        files = sorted(self.project_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        for path in files:
            dt = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            item = QListWidgetItem(self.project_list)
            item.setData(Qt.UserRole, str(path))
            item.setSizeHint(QSize(220, 42))
            widget = ProjectListItemWidget(path.name, dt)
            self.project_list.addItem(item)
            self.project_list.setItemWidget(item, widget)

    def _save_project_as(self):
        start = self.project_dir / "doxygen_project.json"
        path, _ = QFileDialog.getSaveFileName(self, "DoxyGen-Projekt speichern", str(start), "JSON (*.json)")
        if not path:
            return
        if not path.lower().endswith(".json"):
            path += ".json"
        payload = self._project_payload(path)
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            self.current_project_path = path
            self._reload_project_list()
        except Exception as e:
            QMessageBox.critical(self, "Speichern", str(e))

    def _selected_project_path(self):
        item = self.project_list.currentItem()
        if item is None:
            return ""
        return item.data(Qt.UserRole) or ""

    def _load_selected_project(self):
        path = self._selected_project_path()
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "DoxyGen-Projekt laden", str(self.project_dir), "JSON (*.json)")
            if not path:
                return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ok, err = self._validate_payload(data)
            if not ok:
                QMessageBox.critical(self, "Ungültige Projektdatei", err)
                return
            state = data.get("state", {})
            self.tabs.setCurrentIndex(int(state.get("current_tab", 0)))
            self.list_categories.setCurrentRow(int(state.get("expert_item", 0)))
            self.wizard_text.setHtml(state.get("wizard_html", ""))
            self.html_preview.setHtml(state.get("expert_html", ""))
            self.run_text.setHtml(state.get("run_html", ""))
            self.current_project_path = path
            self._reload_project_list()
        except Exception as e:
            QMessageBox.critical(self, "Laden", str(e))

    def _delete_selected_project(self):
        path = self._selected_project_path()
        if not path:
            return
        reply = QMessageBox.question(
            self,
            "Projekt löschen",
            f"Soll das Projekt wirklich gelöscht werden?\n\n{Path(path).name}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        try:
            os.remove(path)
            if self.current_project_path == path:
                self.current_project_path = ""
            self._reload_project_list()
        except Exception as e:
            QMessageBox.critical(self, "Löschen", str(e))


DoxygenToolWidget = MeineKlasse
