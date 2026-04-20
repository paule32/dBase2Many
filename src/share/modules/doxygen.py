# ---------------------------------------------------------------------------
# File:   doxygen.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
#
# die Datei erwartet die .mo-Datei standardmäßig unter
# src/data/po/locales/<sprache>/LC_MESSAGES/doxygen.mo
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

HEADER_FORMAT   = "dBase2Many Project File"
HEADER_TOOL     = "doxygen-dialog"
HEADER_KIND     = "doxygen-project"
HEADER_VERSION  = 1

PROJECT_FIELDS  = [
    {"name": "DOXYFILE_ENCODING",        "type": "lineedit"      , "help_key": "doxygen.project.DOXYFILE_ENCODING.help"},
    {"name": "PROJECT_NAME",             "type": "lineedit"      , "help_key": "doxygen.project.PROJECT_NAME.help"},
    {"name": "PROJECT_NUMBER",           "type": "lineedit"      , "help_key": "doxygen.project.PROJECT_NUMBER.help"},
    {"name": "PROJECT_BRIEF",            "type": "lineedit"      , "help_key": "doxygen.project.PROJECT_BRIEF.help"},
    {"name": "PROJECT_LOGO",             "type": "lineedit_btn"  , "help_key": "doxygen.project.PROJECT_LOGO.help"},
    {"name": "_LOGO_LABEL",              "type": "_label"        , "help_key": ""},
    {"name": "_SPACER",                  "type": "_spacer"       , "help_key": ""},
    {"name": "PROJECT_ICON",             "type": "lineedit_btn"  , "help_key": "doxygen.project.PROJECT_ICON.help"},
    {"name": "_LOGO_LABEL",              "type": "_label"        , "help_key": ""},
    {"name": "_SPACER",                  "type": "_spacer"       , "help_key": ""},
    {"name": "OUTPUT_DIRECTORY",         "type": "lineedit_btn"  , "help_key": "doxygen.project.OUTPUT_DIRECTORY.help"},
    {"name": "CREATE_SUBDIRS",           "type": "checkbox"      , "help_key": "doxygen.project.CREATE_SUBDIRS.help"},
    {"name": "CREATE_SUBDIRS_LEVEL",     "type": "spinedit"      , "help_key": "doxygen.project.CREATE_SUBDIRS_LEVEL.help"},
    {"name": "ALLOW_UNICODE_NAMES",      "type": "checkbox"      , "help_key": "doxygen.project.ALLOW_UNICODE_NAMES.help"},
    {"name": "OUTPUT_LANGUAGE",          "type": "combobox_lang" , "help_key": "doxygen.project.OUTPUT_LANGUAGE.help"},
    {"name": "BRIEF_MEMBER_DESC",        "type": "checkbox"      , "help_key": "doxygen.project.BRIEF_MEMBER_DESC.help"},
    {"name": "REPEAT_BRIEF",             "type": "checkbox"      , "help_key": "doxygen.project.REPEAT_BRIEF.help"},
    {"name": "ABBREVIATVE_BRIEF",        "type": "lineedit_btn3" , "help_key": "doxygen.project.ABBREVIATVE_BRIEF.help"},
    {"name": "ABBREVIATVE",              "type": "textedit"      , "help_key": "doxygen.project.ABBREVIATVE.help"},
    {"name": "ALWAYS_DETAILED_SEC",      "type": "checkbox"      , "help_key": "doxygen.project.ALWAYS_DETAILED_SEC.help"},
    {"name": "INLINE_INHERITED_MEMB",    "type": "checkbox"      , "help_key": "doxygen.project.INLINE_INHERITED_MEMB.help"},
    {"name": "FULL_PATH_NAMES",          "type": "checkbox"      , "help_key": "doxygen.project.FULL_PATH_NAMES.help"},
    {"name": "STRIP_FROM_PATH",          "type": "lineedit_btn4" , "help_key": "doxygen.project.STRIP_FROM_PATH.help"},
    {"name": "STRIP_FROM_PATH_EDIT",     "type": "textedit"      , "help_key": "doxygen.project.STRIP_FROM_PATH.help"},
    {"name": "STRIP_FROM_INC_PATH",      "type": "lineedit_btn4" , "help_key": "doxygen.project.STRIP_FROM_INC_PATH.help"},
    {"name": "STRIP_FROM_INC_PATH_EDIT", "type": "textedit"      , "help_key": "doxygen.project.STRIP_FROM_INC_PATH_EDIT.help"},
    {"name": "SHORT_NAMES",              "type": "checkbox"      , "help_key": "doxygen.project.SHPRT_NAMES.help"},
    {"name": "JAVADOC_AUTOBRIEF",        "type": "checkbox"      , "help_key": "doxygen.project.JAVADOC_AUTOBRIEF.help"},
    
    {"name": "AUTOLINK_IGNORE_WORDS",    "type": "lineedit_btn3" , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    {"name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    
    {"name": "LOOKUP_CACHE_SIZE",        "type": "spinedit"      , "help_key": "doxygen.project.LOOKUP_CACHE_SIZE.help"},
    {"name": "NUM_PROC_THREADS",         "type": "spinedit"      , "help_key": "doxygen.project.NUM_PROC_THREADS.help"},
    {"name": "TIMESTAMP",                "type": "combobox"      , "help_key": "doxygen.project.TIMESTAMP.help"},
]


def _default_project_dir() -> Path:
    base = Path.home() / "Documents" / "dBase2Many" / "DoxygenProjects"
    base.mkdir(parents=True, exist_ok=True)
    return base


class LineEditButton(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(2,2,2,2)
        
        self.parent = parent
        
        self.edit = QLineEdit()
        self.edit.setContentsMargins(2, 2, 2, 2)
        self.btn = QPushButton("...")
        self.btn.clicked.connect(self._open_dialog)
        
        lay.addWidget(self.edit)
        lay.addWidget(self.btn)
    
    def _open_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self,
            share.locales.tr("Load DoxyGen Project"),
            "", "Alle (*.*)")
        if not path:
            self.edit.setText("")
            return
        self.edit.setText(path)


class ComboBoxLanguage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
            "English",
            "German",
            "French",
            "Italian",
            "Polsky"
        ])
        lay.addWidget(self.combo)


class LineEditButton3(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.edit = QLineEdit()
        self.edit.setContentsMargins(2, 2, 2, 2)
        
        self.btn1 = QPushButton("...")
        self.btn1.clicked.connect(self._open_dialog)
        
        self.btn2 = QPushButton("...")
        self.btn2.clicked.connect(self._open_dialog)
        
        self.btn3 = QPushButton("...")
        self.btn3.clicked.connect(self._open_dialog)
        
        lay.addWidget(self.edit)
        
        lay.addWidget(self.btn1)
        lay.addWidget(self.btn2)
        lay.addWidget(self.btn3)
    
    def _open_dialog(self):
        pass


class DoxySpinEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.spin = QSpinBox()
        self.spin.setValue(8)
        
        lay.addWidget(self.spin)
    
    
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


class DoxyGenToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_dir = _default_project_dir()
        self.current_project_path = ""
        self.project_edits = {}
        self.help_translator = self._load_help_translator()
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
        self.btn_save   = QPushButton(share.locales.tr("Save"))
        self.btn_delete = QPushButton(share.locales.tr("Delete"))
        self.btn_load   = QPushButton(share.locales.tr("Load"))
        
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_delete)
        btn_row.addWidget(self.btn_load)
        
        left_lay.addLayout(btn_row)

        self.btn_save   .clicked.connect(self._save_project_as)
        self.btn_delete .clicked.connect(self._delete_selected_project)
        self.btn_load   .clicked.connect(self._load_selected_project)

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
            "QLineEdit#doxyEdit { border:none; padding:4px; background:#1b1b1b; color:white; }"
            "QLineEdit#doxyEdit:hover, QLineEdit#doxyEdit:focus { background:#262626; }"
            "QFrame { border:none; }"
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
        self.scroll_lay = QVBoxLayout(self.scroll_widget)
        self.scroll_lay.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay.setSpacing(2)
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
        self._populate_option_panel("Project")
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
        self._populate_option_panel(text)
        self._show_help_for_key(f"doxygen.section.{text}.help", title=text)

    def _locales_dir(self) -> Path:
        return Path(__file__).resolve().parents[2] / "data" / "po" / "locales"

    def _load_help_translator(self):
        lang = (locale.getdefaultlocale()[0] or "de") if locale.getdefaultlocale() else "de"
        lang = lang.split("_")[0].lower()
        try:
            return gettext.translation("doxygen", localedir=str(self._locales_dir()), languages=[lang], fallback=True)
        except Exception:
            return gettext.NullTranslations()

    def _help_html(self, help_key: str, title: str = "") -> str:
        html = self.help_translator.gettext(help_key)
        if html == help_key:
            head = title or help_key
            return f"<b>{head}</b><br><p>Keine Beschreibung in der .mo-Datei gefunden.</p>"
        return html

    def _clear_scroll_area(self):
        while self.scroll_lay.count():
            item = self.scroll_lay.takeAt(0)
            widget = item.widget()
            child_lay = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_lay is not None:
                while child_lay.count():
                    citem = child_lay.takeAt(0)
                    cwidget = citem.widget()
                    if cwidget is not None:
                        cwidget.deleteLater()

    def _bind_help(self, obj, help_key: str, title: str = ""):
        obj.setProperty("help_key", help_key)
        obj.setProperty("help_title", title)
        obj.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Enter, QEvent.FocusIn):
            help_key = obj.property("help_key")
            help_title = obj.property("help_title") or ""
            if help_key:
                self._show_help_for_key(help_key, title=help_title)
        return QWidget.eventFilter(self, obj, event)

    def _show_help_for_key(self, help_key: str, title: str = ""):
        self.html_preview.clear()
        self.html_preview.setHtml(self._help_html(help_key, title=title))

    def _populate_option_panel(self, section_name: str):
        self._clear_scroll_area()
        if section_name == "Project":
            form_host = QWidget()
            form = QFormLayout(form_host)
            form.setContentsMargins(2, 2, 2, 2)
            form.setHorizontalSpacing(6)
            form.setVerticalSpacing(2)
            form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
            form.setFormAlignment(Qt.AlignTop | Qt.AlignLeft)

            label_font = QFont("Consolas", 10)
            metrics = QFontMetrics(label_font)
            max_label_width = max(metrics.horizontalAdvance(field["name"]) for field in PROJECT_FIELDS) + 8
            self.project_edits = {}

            for field in PROJECT_FIELDS:
                label = QLabel(field["name"])
                label.setFont(label_font)
                label.setFixedWidth(max_label_width)
                label.setContentsMargins(2, 2, 2, 2)
                self._bind_help(label, field["help_key"], field["name"])

                if field["type"] == "lineedit":
                    edit = QLineEdit()
                    edit.setObjectName("doxyEdit")
                    edit.setContentsMargins(2, 2, 2, 2)
                    self._bind_help(edit, field["help_key"], field["name"])
                    self.project_edits[field["name"]] = edit
                    form.addRow(label, edit)
                elif field["type"] == "lineedit_btn":
                    edit = LineEditButton(self)
                    edit.setObjectName("doxyEditButton")
                    self._bind_help(edit, field["help_key"], field["name"])
                    self.project_edits[field["name"]] = edit
                    form.addRow(label, edit)
                elif field["type"] == "checkbox":
                    check = QCheckBox()
                    check.setObjectName("doxyCheck")
                    self._bind_help(check, field["help_key"], field["name"])
                    form.addRow(label, check)
                elif field["type"] == "combobox_lang":
                    combo = ComboBoxLanguage(self)
                    combo.setObjectName("doxyComboBoxLangauge")
                    self._bind_help(combo, field["help_key"], field["name"])
                    form.addRow(label, combo)
                elif field["type"] == "lineedit_btn3":
                    edit = LineEditButton3(self)
                    edit.setObjectName("doxyLineEditButton3")
                    self._bind_help(edit, field["help_key"], field["name"])
                    form.addRow(label, edit)
                elif field["type"] == "spinedit":
                    spin = DoxySpinEdit(self)
                    spin.setObjectName("doxySpinEdit")
                    self._bind_help(spin, field["help_key"], field["name"])
                    form.addRow(label, spin)
            
            self.scroll_lay.addWidget(form_host)
            self.scroll_lay.addStretch(1)
        else:
            label = QLabel(section_name)
            label.setFont(QFont("Consolas", 10))
            label.setContentsMargins(2, 2, 2, 2)
            self._bind_help(label, f"doxygen.section.{section_name}.help", section_name)
            self.scroll_lay.addWidget(label)
            self.scroll_lay.addStretch(1)

    def _collect_project_values(self):
        return {name: edit.text() for name, edit in self.project_edits.items()}

    def _apply_project_values(self, values: dict):
        if not isinstance(values, dict):
            return
        for name, value in values.items():
            edit = self.project_edits.get(name)
            if edit is not None:
                edit.setText(str(value))

    def _project_payload(self, path: str) -> dict:
        now = dt.datetime.now()
        p = Path(path)
        return {
            "header": {
                "format"        : HEADER_FORMAT,
                "tool"          : HEADER_TOOL,
                "kind"          : HEADER_KIND,
                "version"       : HEADER_VERSION,
            },
            "meta": {
                "date"          : now.strftime("%Y-%m-%d"),
                "time"          : now.strftime("%H:%M:%S"),
                "filename"      : p.name,
                "filepath"      : str(p),
            },
            "state": {
                "current_tab"   : self.tabs.currentIndex(),
                "expert_item"   : self.list_categories.currentRow(),
                "wizard_html"   : self.wizard_text.toHtml(),
                "expert_html"   : self.html_preview.toHtml(),
                "run_html"      : self.run_text.toHtml(),
                "project_values": self._collect_project_values(),
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
            dt_text = dt.datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            item = QListWidgetItem(self.project_list)
            item.setData(Qt.UserRole, str(path))
            item.setSizeHint(QSize(220, 42))
            widget = ProjectListItemWidget(path.name, dt_text)
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
            reply = QMessageBox.question(
                self,
                share.locales.tr("Save Project As ..."),
                f"{share.locales.tr("Did you realy want to overwrite the file:\n\n")}{Path(path).name}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.NO:
                return
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
            self._apply_project_values(state.get("project_values", {}))
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
