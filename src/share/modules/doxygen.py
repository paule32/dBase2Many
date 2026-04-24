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

HEADER_FORMAT   = "dBase2Many Project File"
HEADER_TOOL     = "doxygen-dialog"
HEADER_KIND     = "doxygen-project"
HEADER_VERSION  = 1

PROJECT_FIELDS  = [
    {"obj": None, "name": "DOXYFILE_ENCODING",        "type": "lineedit"      , "help_key": "doxygen.project.DOXYFILE_ENCODING.help"},
    {"obj": None, "name": "PROJECT_NAME",             "type": "lineedit"      , "help_key": "doxygen.project.PROJECT_NAME.help"},
    {"obj": None, "name": "PROJECT_NUMBER",           "type": "lineedit"      , "help_key": "doxygen.project.PROJECT_NUMBER.help"},
    {"obj": None, "name": "PROJECT_BRIEF",            "type": "lineedit"      , "help_key": "doxygen.project.PROJECT_BRIEF.help"},
    {"obj": None, "name": "PROJECT_LOGO",             "type": "lineedit_btn"  , "help_key": "doxygen.project.PROJECT_LOGO.help"},
    {"obj": None, "name": "_LOGO_LABEL",              "type": "_label"        , "help_key": ""},
    {"obj": None, "name": "_SPACER",                  "type": "_spacer"       , "help_key": ""},
    {"obj": None, "name": "PROJECT_ICON",             "type": "lineedit_btn"  , "help_key": "doxygen.project.PROJECT_ICON.help"},
    {"obj": None, "name": "_LOGO_LABEL",              "type": "_label"        , "help_key": ""},
    {"obj": None, "name": "_SPACER",                  "type": "_spacer"       , "help_key": ""},
    
    {"obj": None, "name": "OUTPUT_DIRECTORY",         "type": "lineedit_btn"  , "help_key": "doxygen.project.OUTPUT_DIRECTORY.help"},
    {"obj": None, "name": "CREATE_SUBDIRS",           "type": "checkbox"      , "help_key": "doxygen.project.CREATE_SUBDIRS.help"},
    {"obj": None, "name": "CREATE_SUBDIRS_LEVEL",     "type": "spinedit"      , "help_key": "doxygen.project.CREATE_SUBDIRS_LEVEL.help"},
    
    {"obj": None, "name": "ALLOW_UNICODE_NAMES",      "type": "checkbox"      , "help_key": "doxygen.project.ALLOW_UNICODE_NAMES.help"},
    {"obj": None, "name": "OUTPUT_LANGUAGE",          "type": "combobox_lang" , "help_key": "doxygen.project.OUTPUT_LANGUAGE.help"},
    
    {"obj": None, "name": "BRIEF_MEMBER_DESC",        "type": "checkbox"      , "help_key": "doxygen.project.BRIEF_MEMBER_DESC.help"},
    {"obj": None, "name": "REPEAT_BRIEF",             "type": "checkbox"      , "help_key": "doxygen.project.REPEAT_BRIEF.help"},
    {"obj": None, "name": "ABBREVIATVE_BRIEF",        "type": "lineedit_btn3" , "help_key": "doxygen.project.ABBREVIATVE_BRIEF.help"},
    {"obj": None, "name": "ABBREVIATVE_BRIEF",        "type": "textedit"      , "help_key": "doxygen.project.ABBREVIATVE.help"},
    
    {"obj": None, "name": "ALWAYS_DETAILED_SEC",      "type": "checkbox"      , "help_key": "doxygen.project.ALWAYS_DETAILED_SEC.help"},
    {"obj": None, "name": "INLINE_INHERITED_MEMB",    "type": "checkbox"      , "help_key": "doxygen.project.INLINE_INHERITED_MEMB.help"},
    {"obj": None, "name": "FULL_PATH_NAMES",          "type": "checkbox"      , "help_key": "doxygen.project.FULL_PATH_NAMES.help"},
    
    {"obj": None, "name": "STRIP_FROM_PATH",          "type": "lineedit_btn4" , "help_key": "doxygen.project.STRIP_FROM_PATH.help"},
    {"obj": None, "name": "STRIP_FROM_PATH",          "type": "textedit"      , "help_key": "doxygen.project.STRIP_FROM_PATH.help"},
    {"obj": None, "name": "STRIP_FROM_INC_PATH",      "type": "lineedit_btn4" , "help_key": "doxygen.project.STRIP_FROM_INC_PATH.help"},
    {"obj": None, "name": "STRIP_FROM_INC_PATH",      "type": "textedit"      , "help_key": "doxygen.project.STRIP_FROM_INC_PATH.help"},
    {"obj": None, "name": "SHORT_NAMES",              "type": "checkbox"      , "help_key": "doxygen.project.SHPRT_NAMES.help"},
    
    {"obj": None, "name": "JAVADOC_AUTOBRIEF",        "type": "checkbox"      , "help_key": "doxygen.project.JAVADOC_AUTOBRIEF.help"},
    {"obj": None, "name": "JAVADOC_BANNER",           "type": "checkbox"      , "help_key": "doxygen.project.JAVADOC_BANNER.help"},
    {"obj": None, "name": "QT_AUTOBRIEF",             "type": "checkbox"      , "help_key": "doxygen.project.QT_AUTOBRIEF.help"},
    
    {"obj": None, "name": "PYTHON_DOCSTRING",         "type": "checkbox"      , "help_key": "doxygen.project.PYTHON_DOCSTRING.help"},
    {"obj": None, "name": "INHERIT_DOCS",             "type": "checkbox"      , "help_key": "doxygen.project.INHERIT_DOCS.help"},
    {"obj": None, "name": "SEPARATE_MEMBER_PAGES",    "type": "checkbox"      , "help_key": "doxygen.project.SEPARATE_MEMBER_PAGES.help"},
    
    {"obj": None, "name": "TAB_SIZE",                 "type": "spinedit"      , "help_key": "doxygen.project.TAB_SIZE.help"},
    
    {"obj": None, "name": "ALIASES",                  "type": "lineedit_btn3" , "help_key": "doxygen.project.ALIASES.help"},
    {"obj": None, "name": "ALIASES",                  "type": "textedit"      , "help_key": "doxygen.project.ALIASES.help"},
    
    {"obj": None, "name": "OPTIMIZE_OUTPUT_FOR_C",    "type": "checkbox"      , "help_key": "doxygen.project.OPTIMIZE_OUTPUT_FOR_C.help"},
    {"obj": None, "name": "OPTIMIZE_OUTPUT_JAVA",     "type": "checkbox"      , "help_key": "doxygen.project.OPTIMIZE_OUTPUT_JAVA.help"},
    {"obj": None, "name": "OPTIMIZE_FOR_FORTRAN",     "type": "checkbox"      , "help_key": "doxygen.project.OPTIMIZE_FOR_FORTRAN.help"},
    {"obj": None, "name": "OPTIMIZE_OUTPUT_VHDL",     "type": "checkbox"      , "help_key": "doxygen.project.OPTIMIZE_OUTPUT_VHDL.help"},
    {"obj": None, "name": "OPTIMIZE_OUTPUT_SLICE",    "type": "checkbox"      , "help_key": "doxygen.project.OPTIMIZE_OUTPUT_SLICE.help"},
    
    {"obj": None, "name": "EXTERNAL_MAPPING",         "type": "lineedit_btn3" , "help_key": "doxygen.project.EXTERNAL_MAPPING.help"},
    {"obj": None, "name": "EXTERNAL_MAPPING",         "type": "textedit"      , "help_key": "doxygen.project.EXTERNAL_MAPPING.help"},
    
    {"obj": None, "name": "MARKDOWN_SUPPORT",         "type": "checkbox"      , "help_key": "doxygen.project.MARKDOWN_SUPPORT.help"},
    {"obj": None, "name": "MARKDOWN_STRICT",          "type": "checkbox"      , "help_key": "doxygen.project.MARKDOWN_STRICT.help"},
    
    {"obj": None, "name": "TOC_INCLUDE_HEADINGS",     "type": "spinedit"      , "help_key": "doxygen.project.TOC_INCLUDE_HEADINGS.help"},
    {"obj": None, "name": "MARKDOWN_ID_STYLE",        "type": "combobox_md"   , "help_key": "doxygen.project.MARKDOWN_ID_STYLE.help"},
    {"obj": None, "name": "AUTOLINK_SUPPORT",         "type": "checkbox"      , "help_key": "doxygen.project.AUTOLINK_SUPPORT.help"},
    {"obj": None, "name": "AUTOLINK_IGNORE_WORDS",    "type": "lineedit_btn3" , "help_key": "doxygen.project.AUTOLINK_IGNORE_WORDS.help"},
    {"obj": None, "name": "AUTOLINK_IGNORE_WORDS",    "type": "textedit"      , "help_key": "doxygen.project.AUTOLINK_IGNORE_WORDS.help"},
    
    {"obj": None, "name": "BUILTiN_STL_SUPPORT",      "type": "checkbox"      , "help_key": "doxygen.project.BUILTiN_STL_SUPPORT.help"},
    {"obj": None, "name": "CPP_CLI_SUPPORT",          "type": "checkbox"      , "help_key": "doxygen.project.CPP_CLI_SUPPORT.help"},
    {"obj": None, "name": "SIP_SUPPORT",              "type": "checkbox"      , "help_key": "doxygen.project.SIP_SUPPORT.help"},
    {"obj": None, "name": "IDL_PROPERTY_SUPPORT",     "type": "checkbox"      , "help_key": "doxygen.project.IDL_PROPERTY_SUPPORT.help"},
    
    {"obj": None, "name": "DISTRIBUTE_GROUP_DOC",     "type": "checkbox"      , "help_key": "doxygen.project.DISTRIBUTE_GROUP_DOC.help"},
    {"obj": None, "name": "GROUP_NESTED_COMPOUNDS",   "type": "checkbox"      , "help_key": "doxygen.project.GROUP_NESTED_COMPOUNDS.help"},
    {"obj": None, "name": "SUBGROUPING",              "type": "checkbox"      , "help_key": "doxygen.project.SUBGROUPING.help"},
    {"obj": None, "name": "INLINE_GROUPED_CLASSES",   "type": "checkbox"      , "help_key": "doxygen.project.INLINE_GROUPED_CLASSES.help"},
    {"obj": None, "name": "INLINE_SIMPLE_STRUCTS",    "type": "checkbox"      , "help_key": "doxygen.project.INLINE_SIMPLE_STRUCTS.help"},
    {"obj": None, "name": "TYPEDEF_HIDE_STRUCT",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
    
    {"obj": None, "name": "LOOKUP_CACHE_SIZE",        "type": "spinedit"      , "help_key": "doxygen.project.LOOKUP_CACHE_SIZE.help"},
    {"obj": None, "name": "NUM_PROC_THREADS",         "type": "spinedit"      , "help_key": "doxygen.project.NUM_PROC_THREADS.help"},
    {"obj": None, "name": "TIMESTAMP",                "type": "combobox_time" , "help_key": "doxygen.project.TIMESTAMP.help"},
    
    {"obj": None, "name": "",                         "type": "panelspacer"   , "help_key": ""},
]

BUILD_FIELDS  = [
    {"obj": None, "name": "EXTRACT_ALL",              "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_ALL.help"},
    {"obj": None, "name": "EXTRACT_PRIVATE",          "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_PRIVATE.help"},
    {"obj": None, "name": "EXTRACT_PRIV_VIRTUAL",     "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_PRIV_VIRTUAL.help"},
    {"obj": None, "name": "EXTRACT_PACKAGE",          "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_PACKAGE.help"},
    {"obj": None, "name": "EXTRACT_STATIC",           "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_STATIC.help"},
    
    {"obj": None, "name": "EXTRACT_LOCAL_CLASSES",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_CLASSES.help"},
    {"obj": None, "name": "EXTRACT_LOCAL_METHODS",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "EXTRACT_ANON_NSPACES",     "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "RESOLVE_UNNAMED_PARAMS",   "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "HIDE_UNDOC_MEMBERS",       "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "HIDE_UNDOC_CLASSES",       "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "HIDE_UNDOC_NAMESPACES",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "HIDE_FRIEND_COMPOUNDS",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "HIDE_IN_BODY_DOCS",        "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "INTERNAL_DOCS",            "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "CASE_SENSE_NAMES",         "type": "combobox_sense", "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "HIDE_UNDOC_MEMBERS",       "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "HIDE_SCOPE_NAMES",         "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "HIDE_COMPOUND_REFERENCE",  "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "SHOW_HEADERFILE",          "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SHOW_INCLUDE_FILES",       "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "FORCE_LOCAL_INCLUDES",     "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "INLINE_INFO",              "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "SORT_MEMBER_DOCS",         "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SORT_BRIEF_DOCS",          "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SORT_MEMBER_CTORS_1ST",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SORT_GROUP_NAMES",         "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SORT_BY_SCOPE_NAME",       "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "STRICT_PROTO_MATCHING",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "GENERATE_TODOLIST",        "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "GENERATE_TESTLIST",        "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "GENERATE_BUGLIST",         "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "GENERATE_DEPRECATEDLIST",  "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "GENERATE_REQUIREMENTS",    "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "REQ_TRACEABILITY_INFO",    "type": "combobox_info" , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "ENABLE_SECTIONS",          "type": "lineedit_btn3" , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "",                         "type": "textedit"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "MAX_INITIALIZER_LINES",    "type": "spinedit"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "SHOW_USED_FILES",          "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SHOW_FILES",               "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "SHOW_NAMESPACES",          "type": "checkbox"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "FILE_VERSION_FILTER",      "type": "lineedit_btn"  , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "LAYOUT_FILE",              "type": "lineedit_btn"  , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "CITE_BIB_FILES",           "type": "lineedit_btn4" , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "",                         "type": "textedit"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    
    {"obj": None, "name": "EXTERNAL_TOOL_PATH",       "type": "lineedit_btn4" , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
    {"obj": None, "name": "",                         "type": "textedit"      , "help_key": "doxygen.project.EXTRACT_LOCAL_METHODS.help"},
]

MESSAGES_FIELDS = [
    {"obj": None, "name": "QUIET",                    "type": "checkbox"      , "help_key": "doxygen.project.QUIET.help"},
    {"obj": None, "name": "WARNINGS",                 "type": "checkbox"      , "help_key": "doxygen.project.WARNINGS.help"},
    {"obj": None, "name": "WARN_IF_UNDOCUMENTED",     "type": "checkbox"      , "help_key": "doxygen.project.WARN_IF_UNDOCUMENTED.help"},
    {"obj": None, "name": "WARN_IF_DOC_ERROR",        "type": "checkbox"      , "help_key": "doxygen.project.WARN_IF_DOC_ERROR.help"},
    {"obj": None, "name": "WARN_IF_INCOMPLETE_DOC",   "type": "checkbox"      , "help_key": "doxygen.project.WARN_IF_INCOMPLETE_DOC.help"},
    {"obj": None, "name": "WARN_NO_PARAMDOC",         "type": "checkbox"      , "help_key": "doxygen.project.WARN_NO_PARAMDOC.help"},
    {"obj": None, "name": "WARN_IF_UNDOC_ENUM_VAL",   "type": "checkbox"      , "help_key": "doxygen.project.WARN_IF_UNDOC_ENUM_VAL.help"},
    {"obj": None, "name": "WARN_LAYOUT_FILE",         "type": "checkbox"      , "help_key": "doxygen.project.WARN_LAYOUT_FILE.help"},
    {"obj": None, "name": "WARN_AS_ERROR",            "type": "combobox_warn" , "help_key": "doxygen.project.WARN_AS_ERROR.help"},
    {"obj": None, "name": "WARN_FORMAT",              "type": "lineedit"      , "help_key": "doxygen.project.WARN_FORMAT.help"},
    {"obj": None, "name": "WARN_LINE_FORMAT",         "type": "lineedit"      , "help_key": "doxygen.project.WARN_LINE_FORMAT.help"},
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]

INPUT_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
SOURCE_BROWSER_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
INDEX_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
HTML_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
LATEX_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
RTF_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
MAN_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
XML_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
DOCBOOK_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
AUTOGEN_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
SQLITE3_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
PERLMOD_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
PREPROCESSOR_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
EXTERNAL_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
]
DOC_FIELDS = [
    {"obj": None, "name": "WARN_LOGFILE",             "type": "lineedit_btn"  , "help_key": "doxygen.project.WARN_LOGFILE.help"},
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


class ComboBoxMarkDown(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
            "DOXYGEN",
            "GITHUB"
        ])
        lay.addWidget(self.combo)


class ComboBoxLanguage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
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
        ])
        lay.addWidget(self.combo)


class ComboBoxTimeStamp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
            share.locales.tr("NO"),
            share.locales.tr("YES"),
            share.locales.tr("DATETIME"),
            share.locales.tr("DATE")
        ])
        lay.addWidget(self.combo)


class ComboBoxWarning(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
            share.locales.tr("NO"),
            share.locales.tr("YES"),
            share.locales.tr("FAIL_ON_WARNINGS"),
            share.locales.tr("FAIL_ON_WARNINGS_PRINT")
        ])
        lay.addWidget(self.combo)


class ComboBoxInfo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
            share.locales.tr("YES"),
            share.locales.tr("NO"),
            share.locales.tr("UNSATISFIED_ONLY"),
            share.locales.tr("UNVERIFIED_ONLY")
        ])
        lay.addWidget(self.combo)


class ComboBoxSense(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.combo = QComboBox()
        self.combo.addItems([
            share.locales.tr("SYSTEM"),
            share.locales.tr("NO"),
            share.locales.tr("YES")
        ])
        lay.addWidget(self.combo)


class DoxyCheckBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        
        self.check = QCheckBox("NO")
        self.check.setStyleSheet("color: red;")
        self.check.toggled.connect(self._on_changed)
        
        lay.addWidget(self.check)
    
    def _on_changed(self, checked):
        if checked:
            self.check.setText("YES")
            self.check.setStyleSheet("color: yellow;")
        else:
            self.check.setText("NO")
            self.check.setStyleSheet("color: red;")

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


class LineEditButton4(QWidget):
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
        
        self.btn4 = QPushButton("...")
        self.btn4.clicked.connect(self._open_dialog)
        
        lay.addWidget(self.edit)
        
        lay.addWidget(self.btn1)
        lay.addWidget(self.btn2)
        lay.addWidget(self.btn3)
        lay.addWidget(self.btn4)
    
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


class DoxyTextEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0,0,0,0)
        
        self.parent = parent
        self.edit = QPlainTextEdit()
        self.edit.setStyleSheet("background-color: #303030;")
        
        lay.addWidget(self.edit)

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
        
        self.doxy_Counter_LineEdit          = 1
        self.doxy_Counter_EditButton        = 1
        self.doxy_Counter_CheckBox          = 1
        self.doxy_Counter_ComboBox_MarkDown = 1
        self.doxy_Counter_ComboBox_Time     = 1
        self.doxy_Counter_ComboBox_Warn     = 1
        self.doxy_Counter_ComboBox_Sense    = 1
        self.doxy_Counter_ComboBox_Info     = 1
        self.doxy_Counter_ComboBox_Language = 1
        self.doxy_Counter_LineEdit_Button   = 1
        self.doxy_Counter_SpinEdit          = 1
        self.doxy_Counter_TextEdit          = 1
        self.doxy_Counter_PanelSpacer       = 1
        
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
        self.list_categories.addItems(DOXYGEN_EXPERT_ITEMS)
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        
        str_text = "_text"
        str_help = "_help"
        str_type = "_type"
        
        # -----------------------------------------------------------
        self.scroll_lay_project = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_project.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_project.setSpacing(2)
        
        self.lineEdit_DOXYFILE_ENCODING = QLineEdit()
        self.lineEdit_DOXYFILE_ENCODING.setProperty(str_help, "DOXYFILE_ENCODING")
        self.lineEdit_DOXYFILE_ENCODING.setProperty(str_type, "text")
        self.lineEdit_DOXYFILE_ENCODING.setProperty(str_text, "")
        
        self.lineEdit_PROJECT_NAME = QLineEdit()
        self.lineEdit_PROJECT_NAME.setProperty(str_help, "PROJECT_NAME")
        self.lineEdit_PROJECT_NAME.setProperty(str_type, "text")
        self.lineEdit_PROJECT_NAME.setProperty(str_text, "")
        
        self.lineEdit_PROJECT_NUMBER = QLineEdit()
        self.lineEdit_PROJECT_NUMBER.setProperty(str_help, "PROJECT_NUMBER")
        self.lineEdit_PROJECT_NUMBER.setProperty(str_type, "text")
        self.lineEdit_PROJECT_NUMBER.setProperty(str_text, "")
        
        self.lineEdit_PROJECT_BRIEF = QLineEdit()
        self.lineEdit_PROJECT_BRIEF.setProperty(str_help, "PROJECT_BRIEF")
        self.lineEdit_PROJECT_BRIEF.setProperty(str_type, "text")
        self.lineEdit_PROJECT_BRIEF.setProperty(str_text, "")
        
        self.lineButt_PROJECT_LOGO = QLineEdit()
        self.lineButt_PROJECT_LOGO.setProperty(str_help, "PROJECT_LOGO")
        self.lineButt_PROJECT_LOGO.setProperty(str_type, "text")
        self.lineButt_PROJECT_LOGO.setProperty(str_text, "")
        self.lineButt_PROJECT_LOGO_BTN = QPushButton("...")
        self.lineButt_PROJECT_LOGO_BTN.setProperty(str_help, "PROJECT_LOGO")
        self.lineButt_PROJECT_LOGO_BTN.setProperty(str_type, "button")
        
        self.lineLabl_LOGO_LABEL = QLabel("Logo")
        
        self.spacerLn_SPACER = QWidget()",                  "type": "_spacer"       , "help_key": ""},
        self.spacerLn_SPACER.setProperty(str_help, "")
        self.spacerLn_SPACER.setProperty(str_type, "spacer"

        self.lineBtn1_PROJECT_ICON = QLineEdit()
        self.lineBtn1_PROJECT_ICON_BTN1 = QPushButton("...")
        self.lineBtn1_PROJECT_ICON_BTN1.setProperty(str_help, "PROJECT_ICON")
        self.lineBtn1_PROJECT_ICON_BTN1.setProperty(str_type, "button")
        
        self.lineLabl_LOGO_LABEL = QLabel("")",              "type": "_label"        , "help_key": ""},
        self.spacerLn_SPACER = QWidget()",                  "type": "_spacer"       , "help_key": ""},
        
        self.lineBtn1_OUTPUT_DIRECTORY = QLineEdit()
        self.lineBtn1_OUTPUT_DIRECTORY.setProperty(str_help, "OUTPUT_DIRECTORY")
        self.lineBtn1_OUTPUT_DIRECTORY.setProperty(str_type, "text")
        self.lineBtn1_OUTPUT_DIRECTORY_BTN1 = QPushButton("...")
        self.lineBtn1_OUTPUT_DIRECTORY_BTN1.setProperty(str_help, "OUTPUT_DIRECTORY")
        self.lineBtn1_OUTPUT_DIRECTORY_BTN1.setProperty(str_type, "button")
        
        self.checkBox_CREATE_SUBDIRS = QCheckBox("NO")",           "type": "checkbox"      , "help_key": "doxygen.project.CREATE_SUBDIRS.help"},
        self.spinEdit_CREATE_SUBDIRS_LEVEL = QSpinEdit()",     "type": "spinedit"      , "help_key": "doxygen.project.CREATE_SUBDIRS_LEVEL.help"},
        
        self.checkBox_ALLOW_UNICODE_NAMES = QCheckBox("NO")",      "type": "checkbox"      , "help_key": "doxygen.project.ALLOW_UNICODE_NAMES.help"},
        self.comboBox_OUTPUT_LANGUAGE = QComboBox",          "type": "combobox_lang" , "help_key": "doxygen.project.OUTPUT_LANGUAGE.help"},
        
        self.checkBox_BRIEF_MEMBER_DESC = QCheckBox("NO")",        "type": "checkbox"      , "help_key": "doxygen.project.BRIEF_MEMBER_DESC.help"},
        
        self.checkBox_REPEAT_BRIEF = QCheckBox("NO"),             "type": "checkbox"      , "help_key": "doxygen.project.REPEAT_BRIEF.help"},
        self.checkBox_REPEAT_BRIEF.setProperty(str_help, "REPEAT_BRIEF"
        self.checkBox_REPEAT_BRIEF.setProperty(str_help, "checkbox")
        
        self.lineBtn3_ABBREVIATVE_BRIEF = QLineEdit()",        "type": "lineedit_btn3" , "help_key": "doxygen.project.ABBREVIATVE_BRIEF.help"},
        self.lineBTN3_ABBREVIATVE_BRIEF_BTN1 = QPushButton("...")
        self.lineBTN3_ABBREVIATVE_BRIEF_BTN2 = QPushButton("...")
        self.lineBTN3_ABBREVIATVE_BRIEF_BTN3 = QPushButton("...")
        #
        self.lineBTN3_ABBREVIATVE_BRIEF     .setProperty(str_help, "ABBREVIATVE_BRIEF")
        self.lineBTN3_ABBREVIATVE_BRIEF_btn1.setProperty(str_help, "ABBREVIATVE_BRIEF")
        self.lineBTN3_ABBREVIATVE_BRIEF_btn2.setProperty(str_help, "ABBREVIATVE_BRIEF")
        self.lineBTN3_ABBREVIATVE_BRIEF_btn3.setProperty(str_help, "ABBREVIATVE_BRIEF")
        #
        self.lineBTN3_ABBREVIATVE_BRIEF     .setProperty(str_type, "text")
        self.lineBTN3_ABBREVIATVE_BRIEF_BTN1.setProperty(str_type, "button")
        self.lineBTN3_ABBREVIATVE_BRIEF_BTN2.setProperty(str_type, "button")
        self.lineBTN3_ABBREVIATVE_BRIEF_BTN3.setProperty(str_type, "button")
        #
        self.textEdit_ABBREVIATVE_BRIEF = QPlainTextEdit()",        "type": "textedit"      , "help_key": "doxygen.project.ABBREVIATVE.help"},
        
        self.checkBox_ALWAYS_DETAILED_SEC = QCheckBox("NO")",      "type": "checkbox"      , "help_key": "doxygen.project.ALWAYS_DETAILED_SEC.help"},
        self.checkBox_INLINE_INHERITED_MEMB = QCheckBox("NO")",    "type": "checkbox"      , "help_key": "doxygen.project.INLINE_INHERITED_MEMB.help"},
        self.checkBox_FULL_PATH_NAMES = QCheckBox("NO")",          "type": "checkbox"      , "help_key": "doxygen.project.FULL_PATH_NAMES.help"},
        
        self.lineBtn4_STRIP_FROM_PATH = QLineEdit()",          "type": "lineedit_btn4" , "help_key": "doxygen.project.STRIP_FROM_PATH.help"},
        self.textEdit_STRIP_FROM_PATH = QPlainTextEdit()",          "type": "textedit"      , "help_key": "doxygen.project.STRIP_FROM_PATH.help"},
        self.lineBtn4_STRIP_FROM_INC_PATH = QLineEdit()",      "type": "lineedit_btn4" , "help_key": "doxygen.project.STRIP_FROM_INC_PATH.help"},
        self.textEdit_STRIP_FROM_INC_PATH = QPlainTextEdit()",      "type": "textedit"      , "help_key": "doxygen.project.STRIP_FROM_INC_PATH.help"},
        self.checkBox_SHORT_NAMES = QCheckBox("NO")",              "type": "checkbox"      , "help_key": "doxygen.project.SHPRT_NAMES.help"},
        
        self.checkBox_JAVADOC_AUTOBRIEF = QCheckBox("NO")",        "type": "checkbox"      , "help_key": "doxygen.project.JAVADOC_AUTOBRIEF.help"},
        self.checkBox_JAVADOC_BANNER = QCheckBox("NO")",           "type": "checkbox"      , "help_key": "doxygen.project.JAVADOC_BANNER.help"},
        self.checkBox_QT_AUTOBRIEF = QCheckBox("NO")",             "type": "checkbox"      , "help_key": "doxygen.project.QT_AUTOBRIEF.help"},
        
        self.checkBox_PYTHON_DOCSTRING = QCheckBox("NO")",         "type": "checkbox"      , "help_key": "doxygen.project.PYTHON_DOCSTRING.help"},
        self.checkBox_INHERIT_DOCS = QCheckBox("NO")",             "type": "checkbox"      , "help_key": "doxygen.project.INHERIT_DOCS.help"},
        self.checkBox_SEPARATE_MEMBER_PAGES = QCheckBox("NO")",    "type": "checkbox"      , "help_key": "doxygen.project.SEPARATE_MEMBER_PAGES.help"},
        
        self.spinEdit_TAB_SIZE = QSpinEdit()",                 "type": "spinedit"      , "help_key": "doxygen.project.TAB_SIZE.help"},
        
        self.lineBtn3_ALIASES = QLineEdit()",                  "type": "lineedit_btn3" , "help_key": "doxygen.project.ALIASES.help"},
        self.textEdit_ALIASES = QPlainTextEdit()",                  "type": "textedit"      , "help_key": "doxygen.project.ALIASES.help"},
        
        self_checkBox_OPTIMIZE_OUTPUT_FOR_C = QCheckBox("NO")
        self_checkBox_OPTIMIZE_OUTPUT_FOR_C.setProperty(str_help, "OPTIMIZE_OUTPUT_FOR_C")
        self_checkBox_OPTIMIZE_OUTPUT_FOR_C.setProperty(str_type, "checkbox")
    
        self.checkBox_OPTIMIZE_OUTPUT_JAVA = QCheckBox("NO")
        self.checkBox_OPTIMIZE_OUTPUT_JAVA.setProperty(str_help, "OPTIMIZE_OUTPUT_JAVA")
        self.checkBox_OPTIMIZE_OUTPUT_JAVA.setProperty(str_type, "checkbox")

        self.checkBox_OPTIMIZE_FOR_FORTRAN = QCheckBox("NO")
        self.checkBox_OPTIMIZE_FOR_FORTRAN.setProperty(str_help, "OPTIMIZE_FOR_FORTRAN")
        self.checkBox_OPTIMIZE_FOR_FORTRAN.setProperty(str_type, "checkbox")
    
        self.checkBox_OPTIMIZE_OUTPUT_VHDL = QCheckBox("NO")
        self.checkBox_OPTIMIZE_OUTPUT_VHDL.setProperty(str_help, "OPTIMIZE_OUTPUT_VHDL")
        self.checkBox_OPTIMIZE_OUTPUT_VHDL.setProperty(str_type, "checkbox")
        
        self.checkBox_OPTIMIZE_OUTPUT_SLICE = QCheckBox("NO")
        self.checkBox_OPTIMIZE_OUTPUT_SLICE.serProperty(str_help, "OPTIMIZE_OUTPUT_SLICE")
        self.checkBox_OPTIMIZE_OUTPUT_SLICE.setProperty(str_type, "checkbox")
        
        self.lineBtn3_EXTERNAL_MAPPING = QLineEdit()",         "type": "lineedit_btn3" , "help_key": "doxygen.project.EXTERNAL_MAPPING.help"},
        self.textEdit_EXTERNAL_MAPPING = QPlainTextEdit()",         "type": "textedit"      , "help_key": "doxygen.project.EXTERNAL_MAPPING.help"},
        
        self.checkBox_MARKDOWN_SUPPORT = QCheckBox("NO"),         "type": "checkbox"      , "help_key": "doxygen.project.MARKDOWN_SUPPORT.help"},
        self.checkBox_MARKDOWN_STRICT = QCheckBox("NO")",          "type": "checkbox"      , "help_key": "doxygen.project.MARKDOWN_STRICT.help"},
        
        self.spinEdit_TOC_INCLUDE_HEADINGS = QSpinEdit()",     "type": "spinedit"      , "help_key": "doxygen.project.TOC_INCLUDE_HEADINGS.help"},
        self.comboBox_MARKDOWN_ID_STYLE = QComboBox()",        "type": "combobox_md"   , "help_key": "doxygen.project.MARKDOWN_ID_STYLE.help"},
        self.checkBox_AUTOLINK_SUPPORT  = QCheckBox("NO")",         "type": "checkbox"      , "help_key": "doxygen.project.AUTOLINK_SUPPORT.help"},
        self.lineBtn3_AUTOLINK_IGNORE_WORDS = QLineEdit() ",    "type": "lineedit_btn3" , "help_key": "doxygen.project.AUTOLINK_IGNORE_WORDS.help"},
        self.textEdit_AUTOLINK_IGNORE_WORDS = QPlainTextEdit()",    "type": "textedit"      , "help_key": "doxygen.project.AUTOLINK_IGNORE_WORDS.help"},
        
        self.checkBox_BUILTiN_STL_SUPPORT = QCheckBox("NO")",      "type": "checkbox"      , "help_key": "doxygen.project.BUILTiN_STL_SUPPORT.help"},
        self.checkBox_CPP_CLI_SUPPORT  = QCheckBox("NO")",          "type": "checkbox"      , "help_key": "doxygen.project.CPP_CLI_SUPPORT.help"},
        self.checkBox_SIP_SUPPORT  = QCheckBox("NO")",              "type": "checkbox"      , "help_key": "doxygen.project.SIP_SUPPORT.help"},
        self.checkBox_IDL_PROPERTY_SUPPORT  = QCheckBox("NO")",     "type": "checkbox"      , "help_key": "doxygen.project.IDL_PROPERTY_SUPPORT.help"},
        
        self.checkBox_DISTRIBUTE_GROUP_DOC = QCheckBox("NO")",     "type": "checkbox"      , "help_key": "doxygen.project.DISTRIBUTE_GROUP_DOC.help"},
        self.checkBox_GROUP_NESTED_COMPOUNDS  = QCheckBox("NO")",   "type": "checkbox"      , "help_key": "doxygen.project.GROUP_NESTED_COMPOUNDS.help"},
        self.checkBox_SUBGROUPING  = QCheckBox("NO")",              "type": "checkbox"      , "help_key": "doxygen.project.SUBGROUPING.help"},
        self.checkBox_INLINE_GROUPED_CLASSES  = QCheckBox("NO")",   "type": "checkbox"      , "help_key": "doxygen.project.INLINE_GROUPED_CLASSES.help"},
        self.checkBox_INLINE_SIMPLE_STRUCTS  = QCheckBox("NO")",    "type": "checkbox"      , "help_key": "doxygen.project.INLINE_SIMPLE_STRUCTS.help"},
        self.checkBox_TYPEDEF_HIDE_STRUCT  = QCheckBox("NO")",      "type": "checkbox"      , "help_key": "doxygen.project.TYPEDEF_HIDE_STRUCT.help"},
        
        self.spinEdit_LOOKUP_CACHE_SIZE = QSpinEdit()",        "type": "spinedit"      , "help_key": "doxygen.project.LOOKUP_CACHE_SIZE.help"},
        self.spinEdit_NUM_PROC_THREADS = QSpinEdit()",         "type": "spinedit"      , "help_key": "doxygen.project.NUM_PROC_THREADS.help"},
        self.comboBox_TIMESTAMP = QomboBox()",                "type": "combobox_time" , "help_key": "doxygen.project.TIMESTAMP.help"},
        
        
        # -----------------------------------------------------------
        self.scroll_lay_build = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_build.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_build.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_messages = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_messages.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_messages.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_input = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_input.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_input.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_browser = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_browser.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_browser.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_index = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_index.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_index.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_html = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_html.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_html.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_latex = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_latex.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_latex.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_rtf = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_rtf.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_rtf.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_man = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_man.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_man.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_xml = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_xml.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_xml.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_docbook = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_docbook.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_docbook.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_autogen = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_autogen.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_autogen.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_sqlite3 = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_sqlite3.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_sqlitr3.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_perlmod = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_perlmod.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_perlmod.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_preproc = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_preproc.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_preproc.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_external = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_external.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_external.setSpacing(2)
        # -----------------------------------------------------------
        self.scroll_lay_dot = QVBoxLayout(self.scroll_widget)
        self.scroll_lay_dot.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay_dot.setSpacing(2)
        # -----------------------------------------------------------
        
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

        for pan in DOXYGEN_EXPERT_ITEMS:
            self._populate_option_panel(pan)
        
        self.list_categories.setCurrentRow(1)
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
        self._populate_option_panel(text)
        self._show_help_for_key(f"doxygen.section.{text}.help", title=text)
        
        with open(self.propath, "r", encoding="utf-8") as f:
            data = json.load(f)
        ok, err = self._validate_payload(data)
        if not ok:
            QMessageBox.critical(self, "Ungültige Projektdatei", err)
            return
        
        # --------------------------------------------------------------
        # get config values ...
        # --------------------------------------------------------------
        state = data.get("config", {})
        count = 1
        
        # --------------------------------------------------------------
        """for field in PROJECT_FIELDS:
            try:
                obj = field["obj"]
                if obj is not None:
                    if isinstance(obj, DoxyCheckBox):
                        value = state.get(obj.objectName(), 0)
                        if value:
                            obj.check.setChecked(True)
                        else:
                            obj.check.setChecked(False)
            except RuntimeError as e:
                if share.locales.tr("has been deleted") in str(e):
                    pass
                else:
                    raise
            except Exception as e:
                raise
        # --------------------------------------------------------------
        for field in BUILD_FIELDS:
            try:
                obj = field["obj"]
                if obj is not None:
                    if isinstance(obj, DoxyCheckBox):
                        value = state.get(obj.objectName(), 0)
                        if value:
                            obj.check.setChecked(True)
                        else:
                            obj.check.setChecked(False)
            except RuntimeError as e:
                if share.locales.tr("has been deleted") in str(e):
                    pass
                else:
                    raise
            except Exception as e:
                raise
        # --------------------------------------------------------------
        for field in PROJECT_FIELDS:
            try:
                obj = field["obj"]
                if obj is not None:
                    if isinstance(obj, QLineEdit):
                        value = state.get(obj.objectName(), "")
                        obj.setText(value)
            except RuntimeError as e:
                if share.locales.tr("has been deleted") in str(e):
                    pass
                else:
                    raise
            except Exception as e:
                raise"""
        # --------------------------------------------------------------

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

    def _populate_option_panel(self, section_name: str):
        return
        self._clear_scroll_area()
        se = [
            share.locales.tr("Project"),
            share.locales.tr("Build"),
            share.locales.tr("Messages"),
            share.locales.tr("Dot"),
            share.locales.tr("External"),
            share.locales.tr("Preprocessor"),
            share.locales.tr("Perlmod"),
            share.locales.tr("SQLite3"),
            share.locales.tr("AutoGen"),
            share.locales.tr("DocBook"),
            share.locales.tr("XML"),
            share.locales.tr("Man"),
            share.locales.tr("RTF"),
            share.locales.tr("LaTeX"),
            share.locales.tr("HTML"),
            share.locales.tr("Index"),
            share.locales.tr("Source Browser"),
            share.locales.tr("Input"),
            share.locales.tr("Messages"),
            share.locales.tr("Build"),
            share.locales.tr("Project"),
        ]
        if section_name in se:
            form_host = QWidget()
            form = QFormLayout(form_host)
            form.setContentsMargins(2, 2, 2, 2)
            form.setHorizontalSpacing(6)
            form.setVerticalSpacing(2)
            form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
            form.setFormAlignment (Qt.AlignTop   | Qt.AlignLeft)

            label_font         = QFont("Consolas", 10)
            metrics            = QFontMetrics(label_font)
            max_label_width    = max(metrics.horizontalAdvance(
                field["name"]) for field in PROJECT_FIELDS) + 20
            
            self.project_edits = {}
            
            lf = []
            if   section_name == share.locales.tr("Project"):        lf = PROJECT_FIELDS
            elif section_name == share.locales.tr("Build"):          lf = BUILD_FIELDS
            elif section_name == share.locales.tr("Messages"):       lf = MESSAGES_FIELDS
            elif section_name == share.locales.tr("Input"):          lf = INPUT_FIELDS
            elif section_name == share.locales.tr("Source Browser"): lf = SOURCE_BROWSER_FIELDS
            elif section_name == share.locales.tr("Index"):          lf = INDEX_FIELDS
            elif section_name == share.locales.tr("HTML"):           lf = HTML_FIELDS
            elif section_name == share.locales.tr("LaTeX"):          lf = LATEX_FIELDS
            elif section_name == share.locales.tr("RTF"):            lf = RTF_FIELDS
            elif section_name == share.locales.tr("Man"):            lf = MAN_FIELDS
            elif section_name == share.locales.tr("XML"):            lf = XML_FIELDS
            elif section_name == share.locales.tr("DocBook"):        lf = DOCBOOK_FIELDS
            elif section_name == share.locales.tr("AutoGen"):        lf = AUTOGEN_FIELDS
            elif section_name == share.locales.tr("SQLite3"):        lf = SQLITE3_FIELDS
            elif section_name == share.locales.tr("PerlMod"):        lf = PERLMOD_FIELDS
            elif section_name == share.locales.tr("Preprocessor"):   lf = PREPROCESSOR_FIELDS
            elif section_name == share.locales.tr("External"):       lf = EXTERNAL_FIELDS
            elif section_name == share.locales.tr("Doc"):            lf = DOC_FIELDS
            
            try:
                for field in lf:
                    label = QLabel(field["name"])
                    label.setFont(label_font)
                    label.setFixedWidth(max_label_width)
                    label.setContentsMargins(2, 2, 2, 2)
                    
                    self._bind_help(label,
                        field["help_key"],
                        field["name"])
                    
                    if field["type"] == "lineedit":
                        edit = QLineEdit()
                        edit.setObjectName(f"doxy_LineEdit_{self.doxy_Counter_LineEdit}")
                        self.doxy_Counter_LineEdit += 1
                        field["obj"] = edit
                        edit.setContentsMargins(2, 2, 2, 2)
                        self._bind_help(edit, field["help_key"], field["name"])
                        self.project_edits[field["name"]] = edit
                        form.addRow(label, edit)
                    elif field["type"] == "lineedit_btn":
                        edit = LineEditButton(self)
                        edit.setObjectName(f"doxy_EditButton_{self.doxy_Counter_EditButton}")
                        self.doxy_Counter_EditButton += 1
                        field["obj"] = edit
                        self._bind_help(edit, field["help_key"], field["name"])
                        self.project_edits[field["name"]] = edit
                        form.addRow(label, edit)
                    elif field["type"] == "checkbox":
                        check = DoxyCheckBox(self.holder)
                        check.setObjectName(f"doxy_CheckBox_{self.doxy_Counter_CheckBox}")
                        self.doxy_Counter_CheckBox += 1
                        field["obj"] = check
                        self._bind_help(check, field["help_key"], field["name"])
                        form.addRow(label, check)
                    elif field["type"] == "combobox_md":
                        combo = ComboBoxMarkDown(self)
                        combo.setObjectName(f"doxy_ComboBox_MarkDown_{self.doxy_Counter_ComboBox_MarkDown}")
                        self.doxy_Counter_ComboBox_MarkDown += 1
                        field["obj"] = combo
                        self._bind_help(combo, field["help_key"], field["name"])
                        form.addRow(label, combo)
                    elif field["type"] == "combobox_time":
                        combo = ComboBoxTimeStamp(self)
                        combo.setObjectName(f"doxy_ComboBox_Time_{self.doxy_Counter_ComboBox_Time}")
                        self.doxy_Counter_ComboBox_Time += 1
                        field["obj"] = combo
                        self._bind_help(combo, field["help_key"], field["name"])
                        form.addRow(label, combo)
                    elif field["type"] == "combobox_warn":
                        combo = ComboBoxWarning(self)
                        combo.setObjectName(f"doxy_ComboBox_Warning_{self.doxy_Counter_ComboBox_Warn}")
                        self.doxy_Counter_ComboBox_Warn += 1
                        field["obj"] = combo
                        self._bind_help(combo, field["help_key"], field["name"])
                        form.addRow(label, combo)
                    elif field["type"] == "combobox_sense":
                        combo = ComboBoxSense(self)
                        combo.setObjectName(f"doxy_ComboBox_Sense_{self.doxy_Counter_ComboBox_Sense}")
                        self.doxy_Counter_ComboBox_Sense += 1
                        field["obj"] = combo
                        self._bind_help(combo, field["help_key"], field["name"])
                        form.addRow(label, combo)
                    elif field["type"] == "combobox_info":
                        combo = ComboBoxInfo(self)
                        combo.setObjectName(f"doxyComboBoxInfo_{self.doxy_Counter_ComboBox_Info}")
                        self.doxy_Counter_ComboBox_Info += 1
                        field["obj"] = combo
                        self._bind_help(combo, field["help_key"], field["name"])
                        form.addRow(label, combo)
                    elif field["type"] == "combobox_lang":
                        combo = ComboBoxLanguage(self)
                        combo.setObjectName(f"doxy_ComboBox_Langauge_{self.doxy_Counter_ComboBox_Language}")
                        self.doxy_Counter_ComboBox_Language += 1
                        field["obj"] = combo
                        self._bind_help(combo, field["help_key"], field["name"])
                        form.addRow(label, combo)
                    elif field["type"] == "lineedit_btn3":
                        edit = LineEditButton3(self)
                        edit.setObjectName(f"doxy_LineEdit_Button_{self.doxy_Counter_LineEdit_Button}")
                        self.doxy_Counter_LineEdit_Button += 1
                        field["obj"] = edit
                        self._bind_help(edit, field["help_key"], field["name"])
                        form.addRow(label, edit)
                    elif field["type"] == "lineedit_btn4":
                        edit = LineEditButton4(self)
                        edit.setObjectName(f"doxy_LineEdit_Button_{self.doxy_Counter_LineEdit_Button}")
                        self.doxy_Counter_LineEdit_Button += 1
                        field["obj"] = edit
                        self._bind_help(edit, field["help_key"], field["name"])
                        form.addRow(label, edit)
                    elif field["type"] == "spinedit":
                        spin = DoxySpinEdit(self)
                        spin.setObjectName(f"doxy_SpinEdit_{self.doxy_Counter_SpinEdit}")
                        self.doxy_Counter_SpinEdit += 1
                        field["obj"] = spin
                        self._bind_help(spin, field["help_key"], field["name"])
                        form.addRow(label, spin)
                    elif field["type"] == "textedit":
                        label.setText("")
                        edit = DoxyTextEdit(self)
                        edit.setObjectName(f"doxy_TextEdit_{self.doxy_Counter_TextEdit}")
                        self.doxy_Counter_TextEdit += 1
                        field["obj"] = edit
                        self._bind_help(edit, field["help_key"], field["name"])
                        form.addRow(label, edit)
                    elif field["type"] == "panelspacer":
                        panel = QWidget(self)
                        panel.setObjectName(f"doxy_PanelSpacer_{self.doxy_Counter_PanelSpacer}")
                        self.doxy_Counter_PanelSpacer += 1
                        field["obj"] = panel
                        panel.setMinimumHeight(100)
                        form.addRow(label, panel)
                        
            except Exception as e:
                QMessageBox.critical(self, share.locales.tr("11internal build error"), str(e))
                return False
            
            self.scroll_lay.addWidget(form_host)
            self.scroll_lay.addStretch(1)
            
            return True
        else:
            label = QLabel(section_name)
            label.setFont(QFont("Consolas", 10))
            label.setContentsMargins(2, 2, 2, 2)
            self._bind_help(label, f"doxygen.section.{section_name}.help", section_name)
            self.scroll_lay.addWidget(label)
            self.scroll_lay.addStretch(1)

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
