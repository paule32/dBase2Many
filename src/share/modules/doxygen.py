# ---------------------------------------------------------------------------
# File:   doxygen.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations
from share.common import *

DOXYGEN_EXPERT_ITEMS = [
    "Project",
    "Build",
    "Messages",
    "Input",
    "Source Browser",
    "Index",
    "HTML",
    "LaTeX",
    "RTF",
    "Man",
    "XML",
    "DocBook",
    "AutoGen",
    "SQLite3",
    "PerlMod",
    "Preprocessor",
    "External",
    "Dot"
]

class DoxyGenToolWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs)

        self.tab_wizard = self._build_wizard_tab()
        self.tab_expert = self._build_expert_tab()
        self.tab_run = self._build_run_tab()

        self.tabs.addTab(self.tab_wizard, "Wizard")
        self.tabs.addTab(self.tab_expert, "Expert")
        self.tabs.addTab(self.tab_run, "Run")

    def _build_wizard_tab(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        info = QTextEdit()
        info.setReadOnly(True)
        info.setHtml(
            "<h3>DoxyGen Wizard</h3>"
            "<p>Hier kann später ein geführter Assistent für die Doxygen-Konfiguration eingebettet werden.</p>"
        )
        lay.addWidget(info)
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
        self.list_categories.setMinimumWidth(180)
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.StyledPanel)
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area_layout.setContentsMargins(8, 8, 8, 8)
        self.scroll_area_layout.setSpacing(6)

        self.lbl_expert_title = QLabel("<b>Project</b>")
        self.lbl_expert_title.setTextFormat(Qt.RichText)
        self.scroll_area_layout.addWidget(self.lbl_expert_title)

        self.lbl_expert_desc = QLabel(
            "Hier können später die Experten-Optionen des ausgewählten Doxygen-Bereichs angezeigt werden."
        )
        self.lbl_expert_desc.setWordWrap(True)
        self.scroll_area_layout.addWidget(self.lbl_expert_desc)

        for idx in range(6):
            row = QFrame()
            row.setFrameShape(QFrame.StyledPanel)
            row_lay = QHBoxLayout(row)
            row_lay.setContentsMargins(8, 6, 8, 6)
            row_lay.addWidget(QLabel(f"Option {idx + 1}"))
            row_lay.addStretch(1)
            row_lay.addWidget(QPushButton("Bearbeiten"))
            self.scroll_area_layout.addWidget(row)

        self.scroll_area_layout.addStretch(1)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.expert_splitter_h.addWidget(self.scroll_area)
        self.expert_splitter_h.setSizes([220, 700])

        self.html_preview = QTextEdit()
        self.html_preview.setAcceptRichText(True)
        self.html_preview.setReadOnly(False)
        self.html_preview.setHtml(
            "<b>Project</b><br>"
            "<p>Hier erscheinen einfache HTML-formatierte Texte. "
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
        info = QTextEdit()
        info.setReadOnly(True)
        info.setHtml(
            "<h3>DoxyGen Run</h3>"
            "<p>Hier kann später die Ausführung von Doxygen, Konsolen-Ausgabe und Log-Informationen erscheinen.</p>"
        )
        lay.addWidget(info)
        return page

    def _on_expert_item_changed(self, text):
        if not text:
            return
        self.lbl_expert_title.setText(f"<b>{text}</b>")
        self.lbl_expert_desc.setText(
            f"Dies ist der Platzhalterbereich für die Doxygen-Experteneinstellungen von <b>{text}</b>."
        )
        self.html_preview.setHtml(
            f"<b>{text}</b><br>"
            f"<p>Hier können HTML-formatierte Hinweise für <b>{text}</b> angezeigt werden.</p>"
        )


class DoxyGenToolWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DoxyGen")
        self.resize(1100, 720)
        self.setCentralWidget(DoxyGenToolWidget(self))

    @staticmethod
    def open_in_mdi(main_window):
        widget = DoxyGenToolWindow(parent=main_window)
        sub = main_window.mdi.addSubWindow(widget)
        sub.setWindowTitle("DoxyGen")
        sub.resize(1100, 720)
        widget.show()
        sub.show()
        try:
            main_window.mdi.setActiveSubWindow(sub)
        except Exception:
            pass
        return sub
