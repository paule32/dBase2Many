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
    share.locales.tr("Project"),
    share.locales.tr("Build"),
    share.locales.tr("Messages"),
    share.locales.tr("Input"),
    share.locales.tr("Source Browser"),
    share.locales.tr("Index"),
    share.locales.tr("HTML"),
    share.locales.tr("LaTeX"),
    share.locales.tr("RTF"),
    share.locales.tr("Man"),
    share.locales.tr("XML"),
    share.locales.tr("DocBook"),
    share.locales.tr("AutoGen"),
    share.locales.tr("SQLite3"),
    share.locales.tr("PerlMod"),
    share.locales.tr("Preprocessor"),
    share.locales.tr("External"),
    share.locales.tr("Dot")
]

SUPPORTED_LANGUAGES = [
    share.locales.tr("Afrikans"),
    share.locales.tr("Arabic"),
    share.locales.tr("Armeniam"),
    share.locales.tr("Brazilian"),
    share.locales.tr("Bulgarian"),
    share.locales.tr("Catalan"),
    share.locales.tr("Chinese"),
    share.locales.tr("Chinese Traditional"),
    share.locales.tr("Croatian"),
    share.locales.tr("Czech"),
    share.locales.tr("Danish"),
    share.locales.tr("Dutch"),
    share.locales.tr("English"),
    share.locales.tr("Esperanto"),
    share.locales.tr("Farsil"),
    share.locales.tr("Finnish"),
    share.locales.tr("French"),
    share.locales.tr("German"),
    share.locales.tr("Greek"),
    share.locales.tr("Hindi"),
    share.locales.tr("Hungarian"),
    share.locales.tr("Indonesian"),
    share.locales.tr("Italian"),
    share.locales.tr("Japanese"),
    share.locales.tr("Japanese-en"),
    share.locales.tr("Korean"),
    share.locales.tr("Korean-en"),
    share.locales.tr("Latvian"),
    share.locales.tr("Lithuanian"),
    share.locales.tr("Macedonian"),
    share.locales.tr("Norwegian"),
    share.locales.tr("Persian"),
    share.locales.tr("Polish"),
    share.locales.tr("Portuguese"),
    share.locales.tr("Romanian"),
    share.locales.tr("Russian"),
    share.locales.tr("Serbian"),
    share.locales.tr("Serbian-Cyrillic"),
    share.locales.tr("Slovak"),
    share.locales.tr("Slovene"),
    share.locales.tr("Spanish"),
    share.locales.tr("Swedish"),
    share.locales.tr("Turkish"),
    share.locales.tr("Ukrainian"),
    share.locales.tr("Vietnamese"),
 ]

HEADER_FORMAT   = "dBase2Many Project File"
HEADER_TOOL     = "doxygen-dialog"
HEADER_KIND     = "doxygen-project"
HEADER_VERSION  = 1


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


# ---------------------------------------------------------------------------
# \brief this is a helper class for QHBoxLayout to reduce code space.
# \param parent - QWidget as the parent, default: None.
# ---------------------------------------------------------------------------
class DoxyHBoxLayout(QHBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPushButton to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyButton(QPushButton):
    def __init__(self, help_str:str=""):
        super().__init__(None)
        
        self.setText("...")
        self.setProperty("help", help_str)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyLabel(QLabel):
    def __init__(self, help_str:str="", flag:int=0):
        super().__init__(None)
        
        self.setProperty("help", help_str)
        
        if flag == 0: self.setText(help_str)
        else:         self.setText("")
            
        self.setFont(QFont("Consolas", 10))
        self.setMinimumWidth(164)
        self.setStyleSheet("color: white;")
        self.setProperty("help", help_str)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPlainTextEdit to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyTextEdit(QWidget):
    def __init__(self, help_str:str="", text:list=[]):
        super().__init__(None)
        
        self.layout = DoxyHBoxLayout(self)
        
        self.label  = DoxyLabel(help_str, 1)
        self.edit   = QPlainTextEdit()
        self.edit.setStyleSheet("background-color: #303030;")
        
        for line in text:
            self.edit.appendPlainText(line)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)


# ---------------------------------------------------------------------------
# \brief construct a QCheckBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxyCheckBox(QWidget):
    def __init__(self, help_str:str=""):
        super().__init__(None)
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(help_str)
        self.check  = QCheckBox("NO")

        self.check.setStyleSheet("color: red;")
        self.check.toggled.connect(self.on_changed)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.check)
        self.layout.addStretch(1)
    
    def on_changed(self, checked):
        if checked:
            self.check.setText("YES")
            self.check.setStyleSheet("color: yellow;")
        else:
            self.check.setText("NO")
            self.check.setStyleSheet("color: red;")


# ---------------------------------------------------------------------------
# \brief construct a QSpinBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxySpinEdit(QWidget):
    def __init__(self ,
        help_str:str =  "",
        v_min : int  =   0,
        v_max : int  = 100,
        v_def : int  =   0):
            
        super().__init__(None)
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(help_str)
        self.spin   = QSpinBox()
        
        self.spin.setMinimum(v_min)
        self.spin.setMaximum(v_max)
        self.spin.setValue  (v_def)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin)
        self.layout.addStretch(1)


# ---------------------------------------------------------------------------
# \brief construct a QLineEdit with a label
# \param parent   - QWidget as the parent
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the input content, default: "".
# ---------------------------------------------------------------------------
class DoxyLineEdit(QWidget):
    def __init__(self, help_str:str="", text_str: str=""):
        super().__init__(None)
        
        self.setProperty("help", help_str)
        self.setProperty("text", text_str)
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(help_str)
        self.input  = QLineEdit()
        
        self.input.setProperty("help", help_str)
        self.input.setFont(QFont("Consolas", 10))
        self.input.setText(text_str)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLineEdit with a Button to reduce code.
# ---------------------------------------------------------------------------
class DoxyLineBtn1(QWidget):
    def __init__(self, help_str:str="", text_str:str=""):
        super().__init__(None)
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(help_str, text_str)
        self.buttn  = DoxyButton  (help_str)
        
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.buttn)

class DoxyLineBtn3(QWidget):
    def __init__(self, help_str:str="", text_str:str=""):
        super().__init__(None)
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(help_str, text_str)
        
        self.butt1  = DoxyButton(help_str)
        self.butt2  = DoxyButton(help_str)
        self.butt3  = DoxyButton(help_str)
        
        self.layout.addWidget(self.input)
        
        self.layout.addWidget(self.butt1)
        self.layout.addWidget(self.butt2)
        self.layout.addWidget(self.butt3)

class DoxyLineBtn4(QWidget):
    def __init__(self, help_str:str="", text_str:str=""):
        super().__init__(None)
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(help_str, text_str)
        
        self.butt1  = DoxyButton(help_str)
        self.butt2  = DoxyButton(help_str)
        self.butt3  = DoxyButton(help_str)
        self.butt4  = DoxyButton(help_str)
        
        self.layout.addWidget(self.input)
        
        self.layout.addWidget(self.butt1)
        self.layout.addWidget(self.butt2)
        self.layout.addWidget(self.butt3)
        self.layout.addWidget(self.butt4)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel with a image to reduce code space.
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyImage(QWidget):
    def __init__(self, help_str:str="", text_str:str=""):
        super().__init__(None)
        
        self.setMinimumHeight(74)
        
        self.layout = DoxyHBoxLayout(self)
        self.label1 = DoxyLabel(help_str, 1)
        self.label2 = QLabel(text_str)
        
        self.label2.setAlignment(Qt.AlignLeft)
        self.label2.setProperty("help", help_str)
        
        self.label2.setFont(QFont("Arial", 9))
        self.label2.setStyleSheet("color:yellow;")
        
        self.layout.addWidget(self.label1, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label2, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLineEdit to reduce code space.
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the input content, default: "".
# ---------------------------------------------------------------------------
class DoxyLineButt(QWidget):
    def __init__(self, help_str:str="", text_str:str=""):
        super().__init__(None)
        
        self.setProperty("help", help_str)
        self.setProperty("text", text_str)
        
        self.layout = DoxyHBoxLayout(self)
        self.setLayout(self.layout)
        
        self.input = DoxyLineEdit(help_str, text_str)
        self.buttn = DoxyButton(help_str)
        
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.buttn)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
class DoxyComboBox(QWidget):
    def __init__(self, help_str:str="", items:list=[]):
        super().__init__(None)
        
        self.setProperty("help", help_str)
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(help_str)
        self.combo  = QComboBox()
        
        self.combo.addItems(items)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addStretch(1)


# ---------------------------------------------------------------------------
# \brief this is the doxygen tool window for help / documenting the source.
# ---------------------------------------------------------------------------
class DoxyGenToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.holder  = self
        
        self.project_dir = _default_project_dir()
        self.propath     = self.project_dir / "doxygen_project.json"
        
        self.current_project_path = ""
        self.project_edits   = {}
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
        self.btn_load   = QPushButton(share.locales.tr("Open"))
        
        btn_row.addWidget(self.btn_save)
        btn_row.addWidget(self.btn_delete)
        btn_row.addWidget(self.btn_load)
        
        left_lay.addLayout(btn_row)

        self.btn_save  .clicked.connect(self._save_project_as)
        self.btn_delete.clicked.connect(self._delete_selected_project)
        self.btn_load  .clicked.connect(self._load_selected_project)

        self.main_splitter.addWidget(self.left_host)

        self.right_host = QWidget()
        right_lay = QVBoxLayout(self.right_host)
        right_lay.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        right_lay.addWidget(self.tabs)
        self.main_splitter.addWidget(self.right_host)
        self.main_splitter.setSizes([260, 940])

        self.tabs.addTab(self._build_wizard_tab(), share.locales.tr("Wizard"))
        self.tabs.addTab(self._build_expert_tab(), share.locales.tr("Expert"))
        self.tabs.addTab(self._build_run_tab   (), share.locales.tr("Run"))

    def _build_wizard_tab(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        txt = QTextEdit()
        txt.setReadOnly(False)
        txt.setHtml("<b>DoxyGen Wizard</b><br><p>Hier kann später der geführte Assistent erweitert werden.</p>")
        lay.addWidget(txt)
        self.wizard_text = txt
        return page

    def _create_scroll_page(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_lay = QVBoxLayout(scroll_widget)
        scroll_lay.setContentsMargins(2, 2, 2, 2)
        scroll_lay.setSpacing(2)

        scroll_area.setWidget(scroll_widget)

        return scroll_area, scroll_widget, scroll_lay
    
    def _build_expert_tab(self):
        page     = QWidget()
        page_lay = QVBoxLayout(page)
        page_lay.setContentsMargins(0, 0, 0, 0)
        
        self.expert_splitter_v = QSplitter(Qt.Vertical)
        page_lay.addWidget(self.expert_splitter_v)
        
        top_host = QWidget()
        top_lay  = QVBoxLayout(top_host)
        top_lay.setContentsMargins(0, 0, 0, 0)
        
        self.expert_splitter_h = QSplitter(Qt.Horizontal)
        top_lay.addWidget(self.expert_splitter_h)
        
        self.list_categories = QListWidget()
        
        for item in DOXYGEN_EXPERT_ITEMS:
            self.list_categories.addItem(item)
        
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)
        
        # -----------------------------------------------------------
        self.expert_pages = QStackedWidget()
        self.expert_splitter_h.addWidget(self.expert_pages)
        
        self.scroll_pages = {}

        for name in DOXYGEN_EXPERT_ITEMS:
            scroll_area, scroll_widget, scroll_lay = self._create_scroll_page()
            self.scroll_pages[str(name)] = {
                "area"  : scroll_area,
                "widget": scroll_widget,
                "layout": scroll_lay,
            }
            self.expert_pages.addWidget(scroll_area)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_lay = QVBoxLayout(self.expert_pages)
        self.scroll_lay.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay.setSpacing(2)
        
        # -------------------------------------------------------------------------
        self.project_items = [
            DoxyLineEdit("DOXYFILE_ENCODING", "UTF-8"),
            
            DoxyLineEdit("PROJECT_NAME", "MyProject"),
            DoxyLineEdit("PROJECT_NUMBER"),
            DoxyLineEdit("PROJECT_BRIEF"),
            DoxyLineButt("PROJECT_LOGO"),
            DoxyImage   ("PROJECT_LOGO", share.locales.tr("No Project Logo selected.")),
            DoxyLineBtn1("PROJECT_ICON"),
            DoxyImage   ("PROJECT_ICON", share.locales.tr("No Project Icon selected.")),
            
            DoxyLineBtn1("OUTPUT_DIRECTORY"),
            DoxyCheckBox("CREATE_SUBDIRS"),
            DoxySpinEdit("CREATE_SUBDIRS_LEVEL", 0, 64, 4),
            
            DoxyCheckBox("ALLOW_UNICODE_NAMES"),
            DoxyComboBox("OUTPUT_LANGUAGE", SUPPORTED_LANGUAGES),
            
            DoxyCheckBox("BRIEF_MEMBER_DESC"),
            DoxyCheckBox("REPEAT_BRIEF"),
            
            DoxyLineBtn3("ABBREVIATVE_BRIEF"),
            DoxyTextEdit("ABBREVIATVE_BRIEF", []),
            
            DoxyCheckBox("ALWAYS_DETAILED_SEC"),
            DoxyCheckBox("INLINE_INHERITED_MEMB"),
            
            DoxyCheckBox("FULL_PATH_NAMES"),
            
            DoxyLineBtn4("STRIP_FROM_PATH"),
            DoxyTextEdit("STRIP_FROM_PATH", []),
            
            DoxyLineBtn4("STRIP_FROM_INC_PATH"),
            DoxyTextEdit("STRIP_FROM_INC_PATH", []),
            
            DoxyCheckBox("SHORT_NAMES"),
            
            DoxyCheckBox("JAVADOC_AUTOBRIEF"),
            DoxyCheckBox("JAVADOC_BANNER"),
            
            DoxyCheckBox("QT_AUTOBRIEF"),
            DoxyCheckBox("PYTHON_DOCSTRING"),
            DoxyCheckBox("INHERIT_DOCS"),
            
            DoxyCheckBox("SEPARATE_MEMBER_PAGES"),
            DoxySpinEdit("TAB_SIZE", 2, 16, 2),
            
            DoxyLineBtn3("ALIASES"),
            DoxyTextEdit("ALIASES", []),
            
            DoxyCheckBox("OPTIMIZE_OUTPUT_C"),
            DoxyCheckBox("OPTIMIZE_OUTPUT_JAVA"),
            DoxyCheckBox("OPTIMIZE_OUTPUT_FORTRAN"),
            DoxyCheckBox("OPTIMIZE_OUTPUT_VHDL"),
            DoxyCheckBox("OPTIMIZE_OUTPUT_SLICE"),
            
            DoxyLineBtn3("EXTERNAL_MAPPING"),
            DoxyTextEdit("EXTERNAL_MAPPING", []),
            
            DoxyCheckBox("MARKDOWN_SUPPORT"),
            DoxyCheckBox("MARKDOWN_STRICT"),
            DoxyComboBox("MARKDOWN_ID_STYLE", ["DOXYGEN", "GITHUB"]),
            
            DoxySpinEdit("TOC_INCLUDE_HEADINGS"),
            
            DoxyCheckBox("AUTOLINK_SUPPORT"),
            DoxyLineBtn3("AUTOLINK_IGNORE_WORDS"),
            DoxyTextEdit("AUTOLINK_IGNORE_WORDS", []),
            
            DoxyCheckBox("BUILTiN_STL_SUPPORT"),
            DoxyCheckBox("CPP_CLI_SUPPORT"),
            DoxyCheckBox("SIP_SUPPORT"),
            DoxyCheckBox("IDL_PROPERTY_SUPPORT"),
            DoxyCheckBox("DISTRIBUTE_GROUP_DOC"),
            DoxyCheckBox("GROUP_NESTED_COMPOUNDS"),
            
            DoxyCheckBox("SUBGROUPING"),
            DoxyCheckBox("INLINE_GROUPED_CLASSES"),
            DoxyCheckBox("INLINE_SIMPLE_STRUCTS"),
            
            DoxyCheckBox("TYPEDEF_HIDE_STRUCT"),
            DoxySpinEdit("LOOKUP_CACHE_SIZE"),
            
            DoxySpinEdit("NUM_PROC_THREADS"),
            DoxyComboBox("TIMESTAMP", ["YES", "NO", "DATETIME", "DATE"]),
        ]
        project_lay = self.scroll_pages["Project"]["layout"]
        for item in self.project_items:
            project_lay.addWidget(item)
        project_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.build_items = [
            DoxyCheckBox("EXTRACT_ALL"),
            DoxyCheckBox("EXTRACT_PRIVATE"),
            DoxyCheckBox("EXTRACT_PRIV_VIRTUAL"),
            DoxyCheckBox("EXTRACT_PACKAGE"),
            DoxyCheckBox("EXTRACT_STATIC"),
            
            DoxyCheckBox("EXTRACT_LOCAL_CLASSES"),
            DoxyCheckBox("EXTRACT_LOCAL_METHODS"),
            
            DoxyCheckBox("EXTRACT_ANON_NSPACES"),
            DoxyCheckBox("RESOLVE_UNNAMED_PARAMS"),
            
            DoxyCheckBox("HIDE_UNDOC_MEMBERS"),
            DoxyCheckBox("HIDE_UNDOC_CLASSES"),
            DoxyCheckBox("HIDE_UNDOC_NAMESPACES"),
            
            DoxyCheckBox("HIDE_FRIEND_COMPOUNDS"),
            DoxyCheckBox("HIDE_IN_BODY_DOCS"),
            
            DoxyCheckBox("INTERNAL_DOCS"),
            DoxyComboBox("CASE_SENSE_NAMES", [
                "SYSTEM",
                "YES",
                "NO"
            ]),
            
            DoxyCheckBox("HIDE_UNDOC_MEMBERS"),
            DoxyCheckBox("HIDE_SCOPE_NAMES"),
            DoxyCheckBox("HIDE_COMPOUND_REFERENCE"),
            
            DoxyCheckBox("SHOW_HEADERFILE"),
            DoxyCheckBox("SHOW_INCLUDE_FILES"),
            
            DoxyCheckBox("FORCE_LOCAL_INCLUDES"),
            DoxyCheckBox("INLINE_INFO"),
            
            DoxyCheckBox("SORT_MEMBER_DOCS"),
            DoxyCheckBox("SORT_BRIEF_DOCS"),
            DoxyCheckBox("SORT_MEMBER_CTORS_1ST"),
            DoxyCheckBox("SORT_GROUP_NAMES"),
            DoxyCheckBox("SORT_BY_SCOPE_NAME"),
            
            DoxyCheckBox("STRICT_PROTO_MATCHING"),
            
            DoxyCheckBox("GENERATE_TODOLIST"),
            DoxyCheckBox("GENERATE_TESTLIST"),
            DoxyCheckBox("GENERATE_BUGLIST"),
            DoxyCheckBox("GENERATE_DEPRECATEDLIST"),
            DoxyCheckBox("GENERATE_REQUIREMENTS"),
            
            DoxyComboBox("REQ_TRACEABILITY_INFO", [
                "YES",
                "NO",
                "UNSATISFIED_ONLY",
                "UNVERIFIED_ONLY"
            ]),
            
            DoxyLineBtn3("ENABLE_SECTIONS"),
            DoxyTextEdit("ENABLE_SECTIONS", []),
            
            DoxySpinEdit("MAX_INITIALIZER_LINES"),
            
            DoxyCheckBox("SHOW_USED_FILES"),
            DoxyCheckBox("SHOW_FILES"),
            DoxyCheckBox("SHOW_NAMESPACES"),
            
            DoxyLineBtn1("FILE_VERSION_FILTER"),
            DoxyLineBtn1("LAYOUT_FILE"),
            DoxyLineBtn4("CITE_BIB_FILES"),
            DoxyTextEdit("CITE_BIB_FILES", []),
            
            DoxyLineBtn4("EXTERNAL_TOOL_PATH"),
            DoxyTextEdit("EXTERNAL_TOOL_PATH", [])
        ]
        build_lay = self.scroll_pages["Build"]["layout"]
        for item in self.build_items:
            build_lay.addWidget(item)
        build_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.messages_items = [
            DoxyCheckBox("QUIET"),
            DoxyCheckBox("WARNINGS"),
            DoxyCheckBox("WARN_IF_UNDOCUMENTED"),
            DoxyCheckBox("WARN_IF_DOC_ERROR"),
            DoxyCheckBox("WARN_IF_INCOMPLETE_DOC"),
            DoxyCheckBox("WARN_NO_PARAMDOC"),
            DoxyCheckBox("WARN_IF_UNDOC_ENUM_VAL"),
            DoxyCheckBox("WARN_LAYOUT_FILE"),
            DoxyComboBox("WARN_AS_ERROR", [
                "NO",
                "YES",
                "FAIL_ON_WARNINGS",
                "FAIL_ON_WARNINGS_PRINT"]),
            DoxyLineEdit("WARN_FORMAT"),
            DoxyLineEdit("WARN_LINE_FORMAT"),
            DoxyLineBtn1("WARN_LOGFILE"),
        ]
        messages_lay = self.scroll_pages["Messages"]["layout"]
        for item in self.messages_items:
            messages_lay.addWidget(item)
        messages_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.input_items = [
            DoxyLineBtn4("INPUT"),
            DoxyTextEdit("INPUT", []),
            DoxyLineEdit("INPUT_ENCODING"),
            DoxyLineBtn3("INPUT_FILE"),
            DoxyTextEdit("INPUT_FILE_ENCODING", []),
            
            DoxyLineBtn3("FILE_PATTERNS"),
            DoxyTextEdit("FILE_PATTERNS", ["*.c", "*.cc"]),
            
            DoxyCheckBox("RECURSIVE"),
            
            DoxyLineBtn4("EXCLUDE"),
            DoxyTextEdit("EXCLUDE", []),
            
            DoxyLineBtn3("EXCLUDE_PATTERNS"),
            DoxyTextEdit("EXCLUDE_PATTERNS", []),
            DoxyLineBtn3("EXCLUDE_SYMBOLS"),
            DoxyTextEdit("EXCLUDE_SYMBOLS", []),
            
            DoxyLineBtn4("EXAMPLE_PATH"),
            DoxyTextEdit("EXAMPLE_PATH", []),
            DoxyLineBtn3("EXAMPLE_PATTERNS"),
            DoxyTextEdit("EXAMPLE_PATTERNS", ["*"]),
            DoxyCheckBox("EXAMPLE_RECURSIVE"),
            
            DoxyLineBtn4("IMAGE_PATH"),
            DoxyTextEdit("IMAGE_PATH", []),
            
            DoxyLineBtn1("INPUT_FILTER"),
            
            DoxyLineBtn3("FILTER_PATTERNS"),
            DoxyTextEdit("FILTER_PATTERNS", []),
            
            DoxyCheckBox("FILTER_SOURCE_FILES"),
            DoxyLineBtn3("FILTER_SOURCE_PATTERNS"),
            DoxyTextEdit("FILTER_SOURCE_PATTERNS", []),
            
            DoxyLineEdit("USE_MDFILE_AS_MAINPAGE"),
            
            DoxyCheckBox("IMPLICIT_DIR_DOCS"),
            DoxySpinEdit("FORTRAN_COMMENT_AFTER", 0, 128, 72)
        ]
        input_lay = self.scroll_pages["Input"]["layout"]
        for item in self.input_items:
            input_lay.addWidget(item)
        input_lay.addStretch()

        # -------------------------------------------------------------------------
        self.browser_items = [
            DoxyCheckBox("SOURCE_BROWSER"),
            DoxyCheckBox("INLINE_SOURCES"),
            DoxyCheckBox("STRIP_CODE_COMMENTS"),
            
            DoxyCheckBox("REFERENCED_BY_RELATION"),
            DoxyCheckBox("REFERENCED_LINK_SOURCE"),
            
            DoxyCheckBox("SOURCE_TOOLTIPS"),
            DoxyCheckBox("USE_HTAGS"),
            DoxyCheckBox("VERBATIM_HEADERS"),
            
            DoxyCheckBox("CLANG_ASSISTED_PARSING"),
            DoxyCheckBox("CLANG_ADD_INC_PATHS"),
            DoxyLineBtn3("CLANG_OPTIONS"),
            DoxyTextEdit("CLANG_OPTIONS", []),
            DoxyLineBtn1("CLANG_DATABASE_PATH")
        ]
        browser_lay = self.scroll_pages["Source Browser"]["layout"]
        for item in self.browser_items:
            browser_lay.addWidget(item)
        browser_lay.addStretch()

        # -------------------------------------------------------------------------
        self.index_items = [
            DoxyCheckBox("ALPHABETICAL_INDEX"),
            DoxyTextEdit("ALPHABETICAL_INDEX", [])
        ]
        index_lay = self.scroll_pages["Index"]["layout"]
        for item in self.index_items:
            index_lay.addWidget(item)
        index_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.html_items = [
            DoxyCheckBox("GENERATE_HTML"),
            DoxyLineBtn1("HTML_OUTPUT"),
            DoxyLineEdit("HTML_FILE_EXTENSION"),
            
            DoxyLineBtn1("HTML_HEADER"),
            DoxyLineBtn1("HTML_FOOTER"),
            
            DoxyLineBtn1("HTML_STYLESHEET"),
            DoxyLineBtn4("HTML_EXTRA_STYLESHEET"),
            DoxyTextEdit("HTML_EXTRA_STYLESHEET"),
            DoxyLineBtn4("HTML_EXTRA_FILES"),
            DoxyTextEdit("HTML_EXTRA_FILES", []),
            
            DoxyComboBox("HTML_COLORSTYLE", [
                "LIGHT",
                "DARK",
                "AUTO_LIGHT",
                "AUTP_DARK",
                "TOGGLE"
            ]),
            
            DoxySpinEdit("COLOR_STYLE_HUE"  , 0, 255, 220),
            DoxySpinEdit("COLOR_STYLE_SAT"  , 0, 255, 100),
            DoxySpinEdit("COLOR_STYLE_GAMMA", 0, 255,  80)
        ]
        html_lay = self.scroll_pages["HTML"]["layout"]
        for item in self.html_items:
            html_lay.addWidget(item)
        html_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.latex_items = [
            DoxyCheckBox("GENERATE_LATEX"),
        ]
        latex_lay = self.scroll_pages["LaTeX"]["layout"]
        for item in self.latex_items:
            latex_lay.addWidget(item)
        latex_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.rtf_items = [
            DoxyCheckBox("BUILD"),
        ]
        rtf_lay = self.scroll_pages["RTF"]["layout"]
        for item in self.rtf_items:
            rtf_lay.addWidget(item)
        rtf_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.man_items = [
            DoxyCheckBox("BUILD"),
        ]
        man_lay = self.scroll_pages["Man"]["layout"]
        for item in self.man_items:
            man_lay.addWidget(item)
        man_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.xml_items = [
            DoxyCheckBox("BUILD"),
        ]
        xml_lay = self.scroll_pages["XML"]["layout"]
        for item in self.xml_items:
            xml_lay.addWidget(item)
        xml_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.docbook_items = [
            DoxyCheckBox("BUILD"),
        ]
        docbook_lay = self.scroll_pages["DocBook"]["layout"]
        for item in self.docbook_items:
            docbook_lay.addWidget(item)
        docbook_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.autogen_items = [
            DoxyCheckBox("BUILD"),
        ]
        autogen_lay = self.scroll_pages["AutoGen"]["layout"]
        for item in self.autogen_items:
            autogen_lay.addWidget(item)
        autogen_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.sqlite3_items = [
            DoxyCheckBox("BUILD"),
        ]
        sqlite3_lay = self.scroll_pages["SQLite3"]["layout"]
        for item in self.sqlite3_items:
            sqlite3_lay.addWidget(item)
        sqlite3_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.perlmod_items = [
            DoxyCheckBox("BUILD"),
        ]
        perlmod_lay = self.scroll_pages["PerlMod"]["layout"]
        for item in self.perlmod_items:
            perlmod_lay.addWidget(item)
        perlmod_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.preproc_items = [
            DoxyCheckBox("BUILD"),
        ]
        preproc_lay = self.scroll_pages["Preprocessor"]["layout"]
        for item in self.preproc_items:
            preproc_lay.addWidget(item)
        preproc_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.external_items = [
            DoxyCheckBox("BUILD"),
        ]
        external_lay = self.scroll_pages["External"]["layout"]
        for item in self.external_items:
            external_lay.addWidget(item)
        external_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.dot_items = [
            DoxyCheckBox("BUILDxxx"),
        ]
        dot_lay = self.scroll_pages["Dot"]["layout"]
        for item in self.dot_items:
            dot_lay.addWidget(item)
        dot_lay.addStretch()
        
        # -----------------------------------------------------------
        self.scroll_area.setWidget(self.expert_pages)
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

        self.list_categories.setCurrentRow(1)
        self.list_categories.setCurrentRow(0)
        return page
        
    def _on_expert_item_changed(self, text):
        if not text:
            return
        page = self.scroll_pages.get(text)
        if page:
            self.expert_pages.setCurrentWidget(page["area"])
    
    def _build_run_tab(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        txt = QTextEdit()
        txt.setReadOnly(False)
        txt.setHtml("<b>DoxyGen Run</b><br><p>Hier können Lauf-Ausgaben und Hinweise stehen.</p>")
        lay.addWidget(txt)
        self.run_text = txt
        return page
                
    def _locales_dir(self) -> Path:
        return Path(__file__).resolve().parents[2] / "data" / "po" / "locales"

    def _load_help_translator(self):
        lang = (locale.getdefaultlocale()[0] or "de") if locale.getdefaultlocale() else "de"
        lang = lang.split("_")[0].lower()
        try:
            return gettext.translation("doxygen",
            localedir = str(self._locales_dir()),
            languages = [lang],
            fallback  = True)
        except Exception:
            return gettext.NullTranslations()

    def _help_html(self, help_key: str, title: str = "") -> str:
        html = self.help_translator.gettext(help_key)
        if html == help_key:
            head = title or help_key
            return f"<b>{head}</b><br><p>Keine Beschreibung in der .mo-Datei gefunden.</p>"
        return html

    def _bind_help(self, obj, help_key: str, title: str = ""):
        obj.setProperty("help_key", help_key)
        obj.setProperty("help_title", title)
        obj.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Enter, QEvent.FocusIn):
            help_key   = obj.property("help_key")
            help_title = obj.property("help_title") or ""
            if help_key:
                self._show_help_for_key(help_key, title=help_title)
        return QWidget.eventFilter(self, obj, event)

    def _show_help_for_key(self, help_key: str, title: str = ""):
        self.html_preview.clear()
        self.html_preview.setHtml(self._help_html(help_key, title=title))


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
            }
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
        path, _ = QFileDialog.getSaveFileName(self,
            share.locales.tr("Save DoxyGen-Project"),
            str(start),
            "JSON (*.json)")
        if not path:
            return
        if not path.lower().endswith(".json"):
            path += ".json"
        self.propath = path
        payload = self._project_payload(path)
        try:
            reply = QMessageBox.question(self,
                share.locales.tr("Save Project As ..."),
                f"{share.locales.tr("Did you realy want to overwrite the file")}:\n\n{Path(path).name}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            
            config = {}
            
            payload["config"] = config
            
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Save"), str(e))

    def _selected_project_path(self):
        item = self.project_list.currentItem()
        if item is None:
            return ""
        return item.data(Qt.UserRole) or ""

    def _load_selected_project(self):
        path = self._selected_project_path()
        if not path:
            path, _ = QFileDialog.getOpenFileName(self,
                share.locales.tr("Load DoxyGen-Project"),
                str(self.project_dir), "JSON (*.json)")
            if not path:
                return
        try:
            self.propath = path
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ok, err = self._validate_payload(data)
            if not ok:
                QMessageBox.critical(self, "Ungültige Projektdatei", err)
                return
            state = data.get("state", {})
            self.tabs.setCurrentIndex(int(state.get("current_tab", 0)))
            self.list_categories.setCurrentRow(int(state.get("expert_item", 0)))
        except RuntimeError as e:
            QMessageBox.critical(self, share.locales.tr("bOpen"), str(e))
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("aOpen"), str(e))

    
    def _delete_selected_project(self):
        path = self._selected_project_path()
        if not path:
            return
        reply = QMessageBox.question(
            self,
            "Projekt löschen",
            f"{share.locales.tr("Would you realy delte the Project ?")}\n\n{Path(path).name}",
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
            QMessageBox.critical(self, share.locales.tr("Delete"), str(e))
