# ---------------------------------------------------------------------------
# File:   doxygen.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
#
# die Datei erwartet die .mo-Datei standardmäßig unter
# src/data/po/locales/<sprache>/LC_MESSAGES/doxygen.mo
# ---------------------------------------------------------------------------
from   __future__   import annotations

import os
import html
import hashlib

from share.common import *
from PyQt5.QtGui  import QPageLayout, QPageSize
from PyQt5.QtCore import QMarginsF

# -----------------------------------------------------------------------
# c++ documenting interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.cc.CppDocLexer          import CppDocLexer
from parse.cc.CppDocParser         import CppDocParser
from parse.cc.CppDocParserListener import CppDocParserListener
from parse.cc.CppDocParserVisitor  import CppDocParserVisitor

# -----------------------------------------------------------------------
# pascal documenting interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.pascal.PasDocLexer          import PasDocLexer
from parse.pascal.PasDocParser         import PasDocParser
from parse.pascal.PasDocParserListener import PasDocParserListener
from parse.pascal.PasDocParserVisitor  import PasDocParserVisitor

DOXYGEN_PROJECT_PAGES = {}
DOXYGEN_ITEMS         = []
DOXYGEN_WINDOW        = None
DOXYGEN_CONFIG        = []
DOXYGEN_EXPERT_ITEMS  = [
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

SUPPORTED_LANGUAGES = [
    "Afrikans",
    "Arabic",
    "Armeniam",
    "Brazilian",
    "Bulgarian",
    "Catalan",
    "Chinese",
    "Chinese Traditional",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Esperanto",
    "Farsil",
    "Finnish",
    "French",
    "German",
    "Greek",
    "Hindi",
    "Hungarian",
    "Indonesian",
    "Italian",
    "Japanese",
    "Japanese-en",
    "Korean",
    "Korean-en",
    "Latvian",
    "Lithuanian",
    "Macedonian",
    "Norwegian",
    "Persian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Serbian",
    "Serbian-Cyrillic",
    "Slovak",
    "Slovene",
    "Spanish",
    "Swedish",
    "Turkish",
    "Ukrainian",
    "Vietnamese",
 ]

HEADER_FORMAT   = "dBase2Many Project File"
HEADER_TOOL     = "doxygen-dialog"
HEADER_KIND     = "doxygen-project"
HEADER_VERSION  = 1

ALPHA_CHARS     = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ---------------------------------------------------------------------------
# \brief global definition to write the css styles for dark mode html
# ---------------------------------------------------------------------------
def _write_css(output_dir):
    filename = os.path.join(output_dir, "style.css")
    doxy_css = share.locales.tr("doxy_html_css")
    #doxy_css = doxy_css +
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(doxy_css)

def set_tooltip_if_text(widget, text):
    text = (text or "").strip()
    widget.setToolTip(text)

# ---------------------------------------------------------------------------
# \brief get the default documents home directory for the current user login
# ---------------------------------------------------------------------------
def _default_project_dir() -> Path:
    base = Path.home() / "Documents" / "dBase2Many" / "DoxygenProjects"
    base.mkdir(parents=True, exist_ok=True)
    return base

def make_anchor(name, signature=""):
    text = f"{name}:{signature}"
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]

# ---------------------------------------------------------------------------
# \brief C++ Documentation classes used as records ...
# ---------------------------------------------------------------------------
class CppClassInfo:
    def __init__(self, name):
        self.name    = name
        self.kind    = "class"
        self.bases   = []
        self.methods = []
        self.fields  = []

class CppMemberInfo:
    def __init__(self, access, signature):
        self.access    = access
        self.signature = signature

# ---------------------------------------------------------------------------
# \brief Pascal Documentation classes used as records ...
# ---------------------------------------------------------------------------
class PasTypeInfo:
    def __init__(self       ,
        name                ,
        kind                ,
        signature      = "" ,
        brief          = ""):
        
        self.name      = name
        self.kind      = kind
        self.signature = signature
        self.brief     = brief
        self.fields    = []
        
class PasClassInfo:
    def __init__(self, name):
        self.name       = name
        self.kind       = "class"
        self.brief      = ""
        self.bases      = []
        self.methods    = []
        self.fields     = []
        self.properties = []

class PasMemberInfo:
    def __init__(
        self           ,
        access         ,
        signature      ,
        brief   = ""   ,
        params  = None ,
        returns = ""   ,
        notes   = None):
        
        self.access    = access
        self.signature = signature
        self.brief     = brief
        self.params    = params or []
        self.returns   = returns
        self.notes     = notes  or []
        
        self.property_type_brief  = ""
        self.property_read_brief  = ""
        
        self.property_write_brief = ""

class PasConstInfo:
    def __init__(self, name, value, brief=""):
        self.name  = name
        self.value = value
        self.brief = brief

class PasVarInfo:
    def __init__(self, name, vtype, brief=""):
        self.name  = name
        self.vtype = vtype
        self.brief = brief

class PasEnumInfo(PasTypeInfo):
    def __init__(self,
        name,
        signature  = "" ,
        brief      = ""):
        
        super().__init__(name, "enum", signature, brief)
        self.items = []

class PasVarGroupInfo:
    def __init__(self, title="Global Variables"):
        self.title = title
        self.vars  = []

@dataclass
class PasInterfaceInfo:
    name        : str
    bases       : list
    brief       : str
    methods     : list
    properties  : list

class DoxyProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.index_file = ""

        self.setWindowTitle(share.locales.tr("Generate Documentation"))
        self.resize(600, 400)

        layout = QVBoxLayout(self)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        self.log_edit = QPlainTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setFont(QFont("Consolas", 9))

        btn_layout = QHBoxLayout()

        self.btn_open = QPushButton(share.locales.tr("Open HTML Documentation"))
        self.btn_open.setEnabled(False)

        self.btn_close = QPushButton(share.locales.tr("Close"))

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_close)

        layout.addWidget(self.progress)
        layout.addWidget(self.log_edit)
        layout.addLayout(btn_layout)

        self.btn_open.clicked.connect(self.open_html)
        self.btn_close.clicked.connect(self.accept)

    def log(self, text):
        self.log_edit.appendPlainText(str(text))
        self.log_edit.moveCursor(QTextCursor.End)
        QApplication.processEvents()

    def setValue(self, value):
        self.progress.setValue(value)
        QApplication.processEvents()

    def done_generation(self, index_file):
        self.index_file = index_file
        self.setValue(100)
        self.log("DONE")
        self.btn_open.setEnabled(True)

    def open_html(self):
        if self.index_file and os.path.exists(self.index_file):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.index_file))

# ---------------------------------------------------------------------------
# \brief definition to generate the html code (depend on file extension)
# ---------------------------------------------------------------------------
class HtmlToPdf(QObject):
    def __init__(self, html_file, pdf__file, parent=None):
        super().__init__(parent)
        
        self.html_file = os.path.abspath(html_file)
        self.pdf__file = os.path.abspath(pdf__file)
        
        self.owner = parent
        self.view  = QWebEngineView()
        self.view.hide()
        
        self.progress = self.owner.visitor.progress
        
        settings = self.view.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        
        self.view.loadFinished.connect(self.on_load_finished)
        self.view.page().pdfPrintingFinished.connect(self.on_pdf_finished)
        
        self.load_html()
    
    def load_html(self):
        self.progress.log(share.locales.tr("Load HTML") + ": " + self.html_file)

        if not os.path.exists(self.html_file):
            QMessageBox.critical(
                DOXYGEN_WINDOW,
                share.locales.tr("HTML Error"),
                share.locales.tr("HTML does not exists"))
            return

        with open(self.html_file, "r", encoding="utf-8") as f:
            html_code = f.read()

        base_dir = os.path.dirname(self.html_file)
        base_url = QUrl.fromLocalFile(base_dir + os.sep + "test.pdf")

        self.progress.log(share.locales.tr("BASE") + ": " + base_url.toString())
        self.view.setHtml(html_code, base_url)
    
    def on_load_finished(self, ok):
        self.progress.log(share.locales.tr("HTML load Finished") + ": ok")
        if not ok:
            return
        QTimer.singleShot(250, self.print_pdf)
    
    def print_pdf(self):
        self.progress.log(share.locales.tr("PDF") + ": " + self.pdf__file)
        layout = QPageLayout(
            QPageSize(QPageSize.A4),
            QPageLayout.Portrait,
            QMarginsF(0.0, 0.0, 0.0, 0.0),
            QPageLayout.Millimeter
        )
        self.view.page().printToPdf(self.pdf__file, layout)
        
    def on_pdf_finished(self, file_path, success):
        if success: success = share.locales.tr("success")
        else:       success = share.locales.tr("failed")
        self.progress.log(share.locales.tr("PDF created") + ": " + success)

# ---------------------------------------------------------------------------
# \brief pascal documentation visitor to generate the pascal html help ...
# ---------------------------------------------------------------------------
class PasDocHtmlVisitor(PasDocParserVisitor):
    def __init__(self,
        output_dir   = "html",
        use_treeview = False ,
        progress     = None):
        
        super().__init__()
        
        self.output_dir      = output_dir
        self.use_treeview    = use_treeview
        self.progress        = progress
        
        self.classes         = []
        
        self.pending_brief   = ""
        self.pending_params  = []
        self.pending_notes   = []
        self.pending_returns = ""
        
        self.constants       = []
        self.global_vars     = []
        self.records         = []
        self.arrays          = []
        self.sets            = []
        self.enums           = []
        
        self.pdf_exports     = []
        self.global_methods  = []
        
        self.interfaces      = []
        self.cross_refs      = {}
        
        self.current_class        = None
        self.current_output_class = None
        
        self.global_var_groups = []
        self.current_var_group = None
        
        self.current_access    = "public"
        
        DOXYGEN_CONFIG.append("# Doxyfile 1.17.3\n")
        
        com_line = ("# " + ('-' * 78))
        com_text = share.locales.tr(" related configuration options")

        self.already_seen = []
        self.already_seen.clear()
        
        if  (DOXYGEN_EXPERT_ITEMS  is not None)\
        and (DOXYGEN_PROJECT_PAGES is not None):
            for res in DOXYGEN_EXPERT_ITEMS:
                txt  = share.locales.tr(res)
                page = DOXYGEN_PROJECT_PAGES.get(txt)
                
                if page is None:
                    continue
                
                DOXYGEN_CONFIG.extend([com_line, f"# {txt}{com_text}", com_line])
                self.doxy_fields(page.area.findChildren(QWidget))
                
            for item in DOXYGEN_CONFIG:
                self.progress.log(f"{item}")
    
    def progress_log(self, text):
        if self.progress:
            self.progress.log(text)

    def progress_value(self, value):
        if self.progress:
            self.progress.setValue(value)
        
    def doxy_fields(self, page_widgets):
        for widget in page_widgets:
            if isinstance(widget, DoxyLineBtn3)\
            or isinstance(widget, DoxyLineBtn4): continue
            
            if isinstance(widget, DoxyTextEdit):
                key = widget.help_str
                if key in self.already_seen:
                    continue
                self.already_seen.append(key)
                lines = widget.edit.toPlainText().splitlines()
                p     = len(lines)
                if p == 1:
                    DOXYGEN_CONFIG.append(f"{key:<32}= \"{lines[0]}\"")
                    continue
                elif p > 1:
                    if lines[0] == "":
                        continue
                    for line in lines:
                        if p == len(lines): DOXYGEN_CONFIG.append(f"{key:<32}= \"{line}\" \\")
                        elif p-1 > 0:       DOXYGEN_CONFIG.append(f"{' ':<32}= \"{line}\" \\")
                        else:               DOXYGEN_CONFIG.append(f"{' ':<34}\"{line}\"")
                        p = p-1
                continue
            if isinstance(widget, DoxySpinEdit):
                DOXYGEN_CONFIG.append(f"{widget.help_str:<32}= {str(widget.spin.value())}")
                continue
            if isinstance(widget, DoxyLineEdit):
                if len(widget.input.text()) > 0:
                    DOXYGEN_CONFIG.append(f"{widget.help_str:<32}= \"{widget.input.text()}\"")
                    continue
                else:
                    DOXYGEN_CONFIG.append(f"{widget.help_str:<32}= ")
                    continue
            if isinstance(widget, DoxyCheckBox):
                if widget.check.isChecked():
                    DOXYGEN_CONFIG.append(f"{widget.help_str:<32}= YES")
                    continue
                else:
                    DOXYGEN_CONFIG.append(f"{widget.help_str:<32}= NO" )
                    continue
            if isinstance(widget, DoxyComboBox):
                DOXYGEN_CONFIG.append(f"{widget.help_str:<32}= {widget.combo.currentText()}")
                continue
    
    def all_pascal_types(self):
        return (
            self.classes +
            self.interfaces +
            self.records +
            self.arrays +
            self.sets +
            self.enums
        )
    
    def normalize_type_name(self, text):
        text = text.strip()
        if "<" in text:
            text = text.split("<", 1)[0].strip()
        return text.lower()
    
    def register_cross_ref(self, type_name, source_kind, source_name, source_link):
        key = self.normalize_type_name(type_name)
        if not key:
            return
        self.cross_refs.setdefault(key, [])
        item = {
            "kind": source_kind,
            "name": source_name,
            "link": source_link
        }
        if item not in self.cross_refs[key]:
            self.cross_refs[key].append(item)
    
    def build_cross_references(self):
        self.cross_refs = {}
        known = {}
        for item in self.all_pascal_types():
            known[self.normalize_type_name(item.name)] = item
        for cls in self.classes + self.interfaces:
            for base in getattr(cls, "bases", []):
                self.register_cross_ref(
                    base,
                    "Inherited by",
                    cls.name,
                    self.safe_filename(cls.name) + ".html"
                )

            members = (
                getattr(cls, "fields", []) +
                getattr(cls, "properties", []) +
                getattr(cls, "methods", [])
            )

            for member in members:
                sig = member.signature

                for key, item in known.items():
                    if key in sig.lower():
                        self.register_cross_ref(
                            item.name,
                            "Used by",
                            cls.name + "." + self.member_display_name(member),
                            self.safe_filename(cls.name) + ".html#" + self.make_member_anchor(cls, member)
                        )
        for v in self.global_vars:
            self.register_cross_ref(
                v.vtype,
                "Global variable",
                v.name,
                "index.html#" + self.make_var_anchor(v.name)
            )
    
    def write_search_index(self):
        out_dir = os.path.join(self.output_dir, "pascal")
        os.makedirs(out_dir, exist_ok=True)

        items = []

        for cls in self.classes:
            items.append({
                "kind": "Class",
                "name": cls.name,
                "text": cls.brief,
                "link": self.safe_filename(cls.name) + ".html"
            })

        for item in self.interfaces:
            items.append({
                "kind": "Interface",
                "name": item.name,
                "text": item.brief,
                "link": self.safe_filename(item.name) + ".html"
            })

        for item in self.records + self.arrays + self.sets + self.enums:
            items.append({
                "kind": item.kind,
                "name": item.name,
                "text": item.brief,
                "link": self.safe_filename(item.name) + ".html"
            })

        for c in self.constants:
            items.append({
                "kind": "Constant",
                "name": c.name,
                "text": c.brief,
                "link": "index.html#const_" + self.safe_filename(c.name)
            })

        for v in self.global_vars:
            items.append({
                "kind": "Variable",
                "name": v.name,
                "text": v.brief,
                "link": "index.html#" + self.make_var_anchor(v.name)
            })

        filename = os.path.join(out_dir, "search_index.js")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("window.PASCAL_SEARCH_INDEX = ")
            f.write(json.dumps(items, ensure_ascii=False, indent=2))
            f.write(";\n")
        
    def parse_doc_comment(self, text):
        self.clear_pending_doc()

        text = text.replace("(**!", "")
        text = text.replace("{**!", "")
        text = text.replace("*)"  , "")
        text = text.replace("*}"  , "")

        lines = text.splitlines()

        current_tag = None
        current_param_index = -1

        for line in lines:
            line = line.strip()
            if line.startswith("*"):
                line = line[1:].strip()
            if not line:
                continue
            if line.startswith("@brief"):
                self.pending_brief = line[len("@brief"):].strip()
                current_tag = "brief"
                current_param_index = -1
            elif line.startswith("@note"):
                self.pending_notes.append(["note", line[len("@note"):].strip()])
                current_tag = "note"
                current_param_index = len(self.pending_notes) - 1
            elif line.startswith("@info"):
                self.pending_notes.append(["info", line[len("@info"):].strip()])
                current_tag = "info"
                current_param_index = len(self.pending_notes) - 1
            elif line.startswith("@warn"):
                self.pending_notes.append(["warn", line[len("@warn"):].strip()])
                current_tag = "warn"
                current_param_index = len(self.pending_notes) - 1
            elif line.startswith("@param"):
                rest = line[len("@param"):].strip()
                parts = rest.split(None, 1)
                if len(parts) == 2:
                    self.pending_params.append([parts[0], parts[1]])
                elif len(parts) == 1:
                    self.pending_params.append([parts[0], ""])
                current_tag = "param"
                current_param_index = len(self.pending_params) - 1
            elif line.startswith("@return"):
                self.pending_returns = line[len("@return"):].strip()
                current_tag = "return"
                current_param_index = -1
            else:
                if current_tag == "brief":
                    self.pending_brief += " " + line
                elif current_tag == "param" and current_param_index >= 0:
                    self.pending_params[current_param_index][1] += " " + line
                elif current_tag == "return":
                    self.pending_returns += " " + line
                    
    def ensure_global_var_group(self):
        if self.current_var_group is None:
            self.current_var_group = PasVarGroupInfo("Global Variables")
            self.global_var_groups.append(self.current_var_group)
        
        return self.current_var_group
        
    def alpha_key(self, name):
        if not name:
            return "#"
        ch = name[0].upper()
        if "A" <= ch <= "Z":
            return ch
        return "#"
    
    def index_items(self):
        items = []
        
        for cls in self.classes    : items.append(("Class"   , cls.name, self.safe_filename(cls.name) + ".html"))
        for rec in self.records    : items.append(("Record"  , rec.name, self.safe_filename(rec.name) + ".html"))
        for arr in self.arrays     : items.append(("Array"   , arr.name, self.safe_filename(arr.name) + ".html"))
        for st  in self.sets       : items.append(("Set"     , st .name, self.safe_filename(st .name) + ".html"))
        
        for c   in self.constants  : items.append(("Constant", c  .name, "index.html#const_" + self.safe_filename(c.name)))
        for v   in self.global_vars: items.append(("Variable", v  .name, "index.html#var_"   + self.safe_filename(v.name)))
        
        for enm in self.enums      : items.append(("Enum"    , enm.name, self.safe_filename(enm.name) + ".html"))
        
        return sorted(items, key=lambda x: x[1].lower())
    
    def extract_brief(self, text):
        text  = text.replace("(**!", "")
        text  = text.replace("{**!", "")
        text  = text.replace("*)"  , "")
        text  = text.replace("*}"  , "")
        
        lines = text.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith("*"):
                line = line[1:].strip()
            if line.startswith("@brief"):
                return line[len("@brief"):].strip()
        return ""
    
    def make_member_anchor(self, cls, member):
        cls_name = getattr(cls, "name", "")
        text     = cls.name + "_" + member.signature
        result   = []
        for ch in text:
            if ch.isalnum():
                result.append(ch.lower())
            else:
                result.append("_")
        anchor = "".join(result)
        while "__" in anchor:
            anchor = anchor.replace("__", "_")
        return anchor.strip("_")
    
    def visitInterfaceDeclaration(self, ctx):
        name  = ctx.IDENT().getText()
        generic_params = self.generic_params_from_ctx(ctx)
        
        name  = name + generic_params
        bases = []
        
        if ctx.interfaceBaseList():
            for t in ctx.interfaceBaseList().typeName():
                bases.append(t.getText())
        
        info = PasInterfaceInfo(
            name        = name,
            bases       = bases,
            brief       = self.pending_brief,
            methods     = [],
            properties  = []
        )
        
        old_class  = self.current_class
        old_access = self.current_access
        
        self.current_class  = info
        self.current_access = "public"
        
        self.interfaces.append(info)
        self.visit( ctx.interfaceBody())
        
        self.current_class  = old_class
        self.current_access = old_access
        
        self.clear_pending_doc()
        return None
    
    def visitEnumDeclaration(self, ctx):
        name  = ctx.IDENT().getText()
        brief = self.pending_brief
        
        if hasattr(ctx, "docComment") and ctx.docComment():
            brief = self.extract_brief(ctx.docComment().getText())

        info = PasEnumInfo(
            name,
            self.clean_pascal_signature(self.text_from_ctx(ctx.enumType())),
            brief
        )

        enum_type = ctx.enumType()
        items     = []

        first_item = enum_type.enumItem()
        items.append({
            "ctx": first_item,
            "brief": ""
        })

        for tail in enum_type.enumItemTail():
            if tail.docComment():
                items[-1]["brief"] = self.extract_brief(tail.docComment().getText())

            items.append({
                "ctx": tail.enumItem(),
                "brief": ""
            })

        for entry in items:
            enum_item  = entry["ctx"]
            item_name  = enum_item.IDENT().getText()
            item_brief = entry["brief"]

            if hasattr(enum_item, "docComment") and enum_item.docComment():
                item_brief = self.extract_brief(enum_item.docComment().getText())

            info.items.append({
                "name": item_name,
                "brief": item_brief
            })

        self.enums.append(info)
        self.clear_pending_doc()
        return None
        
    def visitConstDeclaration(self, ctx):
        item  = ctx.constItem()
        name  = item.IDENT().getText()
        value = self.text_from_ctx(item.constValue())
        brief = ""
        if ctx.docComment():
            brief = self.extract_brief(ctx.docComment().getText())
        else:
            brief = self.pending_brief
        self.constants.append(PasConstInfo(name, value, brief))
        self.pending_brief = ""
        return None
    
    def visitConstItem(self, ctx: PasDocParser.ConstItemContext):
        name  = ctx.IDENT().getText()
        value = self.text_from_ctx(ctx.constValue())
        
        self.constants.append(
            PasConstInfo(
                name,
                value,
                self.pending_brief
            )
        )
        self.pending_brief = ""
        return None
    
    def visitSetDeclaration(self, ctx):
        name  = ctx.IDENT().getText()
        brief = self.pending_brief

        if hasattr(ctx, "docComment") and ctx.docComment():
            brief = self.extract_brief(ctx.docComment().getText())

        self.sets.append(
            PasTypeInfo(
                name,
                "set",
                self.clean_pascal_signature(self.text_from_ctx(ctx.setType())),
                brief
            )
        )

        self.clear_pending_doc()
        return None
    
    def visitArrayDeclaration(self, ctx):
        name  = ctx.IDENT().getText()
        brief = self.pending_brief

        if hasattr(ctx, "docComment") and ctx.docComment():
            brief = self.extract_brief(ctx.docComment().getText())

        self.arrays.append(
            PasTypeInfo(
                name,
                "array",
                self.clean_pascal_signature(self.text_from_ctx(ctx.arrayType())),
                brief
            )
        )

        self.clear_pending_doc()
        return None
    
    def clean_pascal_signature(self, text):
        result = ""
        i = 0
        
        while i < len(text):
            if text.startswith("(**!", i):
                end = text.find("*)", i + 4)
                if end < 0:
                    break
                i = end + 2
                continue
            
            if text.startswith("{**!", i):
                end = text.find("*}", i + 4)
                if end < 0:
                    break
                i = end + 2
                continue
            
            result += text[i]
            i += 1
        
        result = result.strip()
        result = result.rstrip(";").strip()
        return result
        
    def visitRecordDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        generic_params = self.generic_params_from_ctx(ctx)
        name = name + generic_params
        
        info = PasTypeInfo(
            name,
            "record",
            self.clean_pascal_signature(self.text_from_ctx(ctx.recordType())),
            self.pending_brief
        )

        self.pending_brief = ""

        old_class  = self.current_class
        old_access = self.current_access

        self.current_class  = info
        self.current_access = "public"
        self.visit(ctx.recordType().recordBody())
        self.records.append(info)

        self.current_class = old_class
        self.current_access = old_access

        return info
    
    def visitDocComment(self, ctx: PasDocParser.DocCommentContext):
        text = ctx.getText()
        
        self.pending_brief   = ""
        self.pending_params  = []
        self.pending_notes   = []
        self.pending_returns = ""
        
        self.parse_doc_comment(text)
        
        #if self.current_class is None and self.pending_brief:
        #    self.current_var_group = PasVarGroupInfo(self.pending_brief)
        #    self.global_var_groups.append(self.current_var_group)
        
        return None
    
    def visitVarDeclaration(self, ctx):
        if ctx.docComment():
            brief = self.extract_brief(ctx.docComment().getText())
            if brief:
                self.current_var_group = PasVarGroupInfo(brief)
                self.global_var_groups.append(self.current_var_group)
            return None
        return self.visitChildren(ctx)
    
    def visitUnitFile(self, ctx: PasDocParser.UnitFileContext):
        self.progress_log(share.locales.tr("Parse Pascal unit..."))
        self.progress_value(5)
        
        self.visitChildren(ctx)
        os.makedirs(os.path.join(self.output_dir, "pascal"), exist_ok=True)
        
        self.progress_log("BUILD CROSS REFERENCES")
        self.progress_value(8)
        self.build_cross_references()
        
        self.progress_log(share.locales.tr("Delete old PDFs..."))
        self.delete_old_topic_pdfs()
        
        self.progress_log(share.locales.tr("GLOBAL VARS COUNT")       + ": " + str(len(self.global_vars)))
        self.progress_log(share.locales.tr("GLOBAL VAR GROUPS COUNT") + ": " + str(len(self.global_var_groups)))
        
        self.progress_log(share.locales.tr("WRITE INDEX"))
        self.progress_value(10)
        self.write_index()
        
        self.progress_log("WRITE SEARCH INDEX")
        self.progress_value(13)
        self.write_search_index()

        self.progress_log(share.locales.tr("WRITE CLASSES"))
        self.progress_value(15)
        self.write_classes()
        
        self.progress_log(share.locales.tr("WRITE INTERFACES"))
        self.progress_log(share.locales.tr("INTERFACES COUNT") + ": " + str(len(self.interfaces)))
        self.progress_value(20)
        self.write_interfaces()

        self.progress_log(share.locales.tr("WRITE RECORDS"))
        self.progress_value(25)
        self.write_pascal_types(self.records)
        
        self.progress_log(share.locales.tr("WRITE ARRAYS"))
        self.progress_value(30)
        self.write_pascal_types(self.arrays)
        
        self.progress_log(share.locales.tr("WRITE SETS"))
        self.progress_value(35)
        self.write_pascal_types(self.sets)
        
        self.progress_log(share.locales.tr("WRITE ENUMS"))
        self.progress_value(40)
        self.write_pascal_enums()
        
        self.progress_log(share.locales.tr("WRITE PDF DOCUMENT"))
        self.progress_value(45)
        self.write_pascal_pdf_document()
        
        index_file = os.path.abspath(
            os.path.join(self.output_dir, "pascal", "index.html")
        )
        
        self.progress_value(100)
        self.progress.done_generation(index_file)
        
        return self.classes
    
    def visitClassDeclaration(self, ctx: PasDocParser.ClassDeclarationContext):
        class_name = ctx.IDENT().getText()
        generic_params = self.generic_params_from_ctx(ctx)
        
        bases      = []
        
        old_class  = self.current_class
        old_access = self.current_access
        
        info = PasClassInfo(class_name + generic_params)
        info.brief = self.pending_brief
        info.kind  = "class"
        
        self.pending_brief = ""
        
        class_type = ctx.classType()
        
        if class_type.classBaseList():
            for t in class_type.classBaseList().typeName():
                bases.append(self.text_from_ctx(t))
        
        info.bases = bases
        
        self.current_class  = info
        self.current_access = "public"

        self.visit(class_type.classBody())
        self.classes.append(info)
        
        self.current_class  = old_class
        self.current_access = old_access
        
        return info
    
    def visitVisibilitySection(self, ctx: PasDocParser.VisibilitySectionContext):
        self.current_access = ctx.visibility().getText().lower()
        return None
    
    def visitMethodDeclaration(self, ctx: PasDocParser.MethodDeclarationContext):
        if self.current_class is None:
            self.global_methods.append(
                PasMemberInfo(
                    "public",
                    self.text_from_ctx(ctx),
                    self.pending_brief,
                    self.pending_params,
                    self.pending_returns,
                    self.pending_notes
                )
            )
            self.clear_pending_doc()
            return None
        
        signature = self.text_from_ctx(ctx)
        self.current_class.methods.append(
            PasMemberInfo(
                self.current_access,
                signature,
                self.pending_brief,
                self.pending_params,
                self.pending_returns,
                self.pending_notes
            )
        )
        self.clear_pending_doc()
        return None
    
    def visitPropertyDeclaration(self, ctx):
        if self.current_class is None:
            return None

        raw_signature = self.clean_pascal_signature(self.text_from_ctx(ctx))

        member = PasMemberInfo(
            self.current_access,
            raw_signature,
            self.pending_brief
        )

        # Kommentar direkt nach dem Typ:
        # property Name: string (**! @brief Datentyp *)
        if ctx.docComment():
            comments = ctx.docComment()
            if not isinstance(comments, list):
                comments = [comments]

            if comments:
                member.property_type_brief = self.extract_brief(comments[0].getText())

        # Kommentare bei read/write:
        # read FName (**! @brief getter *)
        # write FName (**! @brief setter *)
        if hasattr(ctx, "propertyAccessor"):
            for acc in ctx.propertyAccessor():
                acc_text = acc.getText().lower()

                if acc_text.startswith("read"):
                    if acc.docComment():
                        member.property_read_brief = self.extract_brief(
                            acc.docComment().getText()
                        )

                elif acc_text.startswith("write"):
                    if acc.docComment():
                        member.property_write_brief = self.extract_brief(
                            acc.docComment().getText()
                        )

        self.current_class.properties.append(member)
        self.clear_pending_doc()
        return None
    
    def clear_pending_doc(self):
        self.pending_brief   = ""
        self.pending_params  = []
        self.pending_returns = ""
        self.pending_notes   = []
    
    def add_global_var_from_signature(self, signature, brief=""):
        signature = self.clean_pascal_signature(signature)
        
        if ":" not in signature:
            return
        
        left, right = signature.split(":", 1)
        
        names = [x.strip() for x in left.split(",")]
        vtype = right.strip()
        vtype = vtype.rstrip(";").strip()
        
        group = self.ensure_global_var_group()
        
        for name in names:
            if name:
                item = PasVarInfo(name, vtype, brief)
                
                self.global_vars.append(item)
                group.vars.append(item)
        
        self.clear_pending_doc()
    
    def visitFieldDeclaration(self, ctx: PasDocParser.FieldDeclarationContext):
        signature = self.text_from_ctx(ctx)
        brief     = self.pending_brief
        
        if hasattr(ctx, "docComment") and ctx.docComment():
            brief = self.extract_brief(ctx.docComment().getText())
        
        clean_signature = self.clean_pascal_signature(signature)
        
        if self.current_class is None:
            if brief and self.current_var_group is None:
                self.current_var_group = PasVarGroupInfo(brief)
                self.global_var_groups.append(self.current_var_group)

            self.add_global_var_from_signature(clean_signature, brief)
            return None
            
        self.current_class.fields.append(
            PasMemberInfo(
                self.current_access,
                clean_signature,
                brief,
                self.pending_params,
                self.pending_returns,
                self.pending_notes
            )
        )
        self.clear_pending_doc()
        return None

    def format_pascal_signature_multiline(self, signature):
        text = signature.strip()
        
        pos1 = text.find("(")
        pos2 = text.rfind(")")
        
        if pos1 < 0 or pos2 < 0 or pos2 <= pos1:
            return text
        
        before = text[:pos1 + 1]
        params = text[pos1 + 1:pos2]
        after  = text[pos2:]
        
        parts  = [p.strip() for p in params.split(";")]
        
        if len(parts) <= 1:
            return text
        
        result = before + "\n"
        
        for index, part in enumerate(parts):
            if index > 0:
                result += ";\n"

            result += "    " + part
        
        result += "\n" + after
        
        return result
    
    def text_from_ctx(self, ctx):
        tokens = []
        for child in ctx.getChildren():
            if hasattr(child, "symbol"):
                tokens.append(child.getText())
            else:
                sub_text = self.text_from_ctx(child)
                if sub_text:
                    tokens.extend(sub_text.split(" "))
        return self.join_pascal_tokens(tokens)
    
    def make_var_anchor(self, name):
        return "var_" + self.safe_filename(name).lower()
    
    def write_cross_reference_section(self, f, item):
        key  = self.normalize_type_name(item.name)
        refs = self.cross_refs.get(key, [])
        
        if not refs:
            return
        
        f.write("    <section>\n")
        f.write("      <h2>Cross References</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        
        for ref in refs:
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(ref['kind'])}</td>\n")
            f.write(f"          <td class=\"sig\"><a href=\"{ref['link']}\">{self.html_escape(ref['name'])}</a></td>\n")
            f.write("        </tr>\n")
        
        f.write("      </table>\n")
        f.write("    </section>\n")
    
    def write_doc_header(self, f, title, current_name=None):
        f.write("    <div class=\"doc-header-sticky\">\n")
        f.write("      <div class=\"version\">Pascal Doc</div>\n")
        f.write(f"      <h1>{self.html_escape(title)}</h1>\n")
        f.write("      <div class=\"breadcrumb\">\n")
        if current_name:
            f.write("        <a href=\"index.html\">Overview</a>\n")
            f.write("        <span>›</span>\n")
            f.write(f"        <span>{self.html_escape(current_name)}</span>\n")
        else:
            f.write("        <span>Overview</span>\n")
        f.write("      </div>\n")
        f.write("    </div>\n")
        
        self.write_search_box(f)
    
    def write_global_variable_groups_index_section(self, f):
        if not self.global_var_groups:
            return
        f.write("    <section>\n")
        f.write("      <h2>Global Variables</h2>\n")
        for group in self.global_var_groups:
            if not group.vars:
                continue
            f.write(f"      <h3>{self.html_escape(group.title)}</h3>\n")
            f.write("      <table class=\"func-table\">\n")
            for v in group.vars:
                anchor = self.make_var_anchor(v.name)
                f.write("        <tr>\n")
                f.write(f"          <td class=\"ret\">{self.link_known_types(v.vtype)}</td>\n")
                f.write(
                    f"          <td class=\"sig\" id=\"{anchor}\">"
                    f"<span class=\"func-name\">{self.html_escape(v.name)}</span></td>\n"
                )
                f.write("        </tr>\n")
                if v.brief:
                    f.write("        <tr class=\"member-brief-row\">\n")
                    f.write("          <td class=\"ret\"></td>\n")
                    f.write(f"          <td class=\"sig member-brief\">{self.html_escape(v.brief)}</td>\n")
                    f.write("        </tr>\n")
            
            f.write("      </table>\n")
        f.write("    </section>\n")
    
    def write_pascal_pdf_document(self):
        out_dir = os.path.join(self.output_dir, "pascal")
        os.makedirs(out_dir, exist_ok=True)

        filename = os.path.join(out_dir, "print.html")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write("  <meta charset=\"utf-8\">\n")
            f.write(f"  <title>{share.locales.tr('Pascal Documentation PDF')}</title>\n")
            f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
            f.write("  <script src=\"search_index.js\"></script>\n")
            f.write(f"<style>{share.locales.tr('doxy_html_css_print')}</style>")
            
            f.write("</head>\n<body>\n")
            f.write("<main class=\"page\">\n")
            f.write(f"<h1>{share.locales.tr('Pascal Documentation')}</h1>\n")

            self._write_pdf_constants(f)
            self._write_pdf_global_variables(f)
            self._write_pdf_global_methods(f)

            self._write_pdf_classes(f)
            self._write_pdf_interfaces(f)
            
            self._write_pdf_types(f, share.locales.tr("Records"), self.records)
            self._write_pdf_types(f, share.locales.tr("Arrays" ), self.arrays)
            self._write_pdf_types(f, share.locales.tr("Sets"   ), self.sets)
            
            self._write_pdf_enums(f)

            f.write("</main>\n")
            f.write("</body>\n</html>\n")

        pdf_out = os.path.join(out_dir, share.locales.tr("PascalDocumentation.pdf"))
        self.pdf_exports.append(HtmlToPdf(filename, pdf_out, DOXYGEN_WINDOW))

    def _write_pdf_constants(self, f):
        if not self.constants:
            return
        
        f.write("<section>\n")
        f.write(f"<h2>{share.locales.tr('Constants')}</h2>\n")
        f.write("<table class=\"func-table\">\n")
        
        for c in self.constants:
            f.write("<tr>\n")
            f.write(f"<td class=\"ret\">{self.html_escape(c.value)}</td>\n")
            f.write(f"<td class=\"sig\"><span class=\"func-name\">{self.html_escape(c.name)}</span></td>\n")
            f.write("</tr>\n")
            
            if c.brief:
                f.write("<tr class=\"member-brief-row\"><td></td>")
                f.write(f"<td class=\"sig member-brief\">{self.html_escape(c.brief)}</td></tr>\n")
        
        f.write("</table>\n")
        f.write("</section>\n")

    def _write_pdf_global_variables(self, f):
        if not self.global_vars:
            return

        f.write("<section>\n")
        f.write(f"<h2>{share.locales.tr('Global Variables')}</h2>\n")
        f.write("<table class=\"func-table\">\n")

        for v in self.global_vars:
            f.write("<tr>\n")
            f.write(f"<td class=\"ret\">{self.link_known_types(v.vtype)}</td>\n")
            f.write(f"<td class=\"sig\"><span class=\"func-name\">{self.html_escape(v.name)}</span></td>\n")
            f.write("</tr>\n")

            if v.brief:
                f.write("<tr class=\"member-brief-row\"><td></td>")
                f.write(f"<td class=\"sig member-brief\">{self.html_escape(v.brief)}</td></tr>\n")

        f.write("</table>\n")
        f.write("</section>\n")


    def _write_pdf_global_methods(self, f):
        if not getattr(self, "global_methods", []):
            return
        
        f.write("<section>\n")
        f.write(f"<h2>{share.locales.tr("Global Procedures and Functions")}</h2>\n")
        f.write("<table class=\"func-table\">\n")
        
        for m in self.global_methods:
            left, right = self.split_pascal_signature(m.signature)
            
            f.write("<tr>\n")
            f.write(f"<td class=\"ret\">{self.html_escape(left)}</td>\n")
            f.write(f"<td class=\"sig\">{self.highlight_signature(right)}</td>\n")
            f.write("</tr>\n")
            
            if m.brief:
                f.write("<tr class=\"member-brief-row\"><td></td>")
                f.write(f"<td class=\"sig member-brief\">{self.html_escape(m.brief)}</td></tr>\n")
        
        f.write("</table>\n")
        f.write("</section>\n")
    
    def _write_pdf_classes(self, f):
        if not self.classes:
            return
        
        f.write("<section>\n")
        f.write(f"<h2>{share.locales.tr('Classes')}</h2>\n")
        
        for cls in self.classes:
            f.write(f"<h3>{self.html_escape(cls.name)}</h3>\n")
            
            if cls.brief:
                f.write(f"<p class=\"brief\">{self.html_escape(cls.brief)}</p>\n")
            
            if cls.bases:
                f.write("<p class=\"inherits\">Inherits: ")
                f.write(", ".join(self.html_escape(b) for b in cls.bases))
                f.write("</p>\n")
            
            self.current_output_class = cls
            
            self.write_member_table(f, share.locales.tr("Public Methods"),       cls.methods,    "public")
            self.write_member_table(f, share.locales.tr("Protected Methods"),    cls.methods,    "protected")
            self.write_member_table(f, share.locales.tr("Private Methods"),      cls.methods,    "private")
            self.write_member_table(f, share.locales.tr("Published Methods"),    cls.methods,    "published")
            
            self.write_member_table(f, share.locales.tr("Public Properties"),    cls.properties, "public")
            self.write_member_table(f, share.locales.tr("Protected Properties"), cls.properties, "protected")
            self.write_member_table(f, share.locales.tr("Private Properties"),   cls.properties, "private")
            self.write_member_table(f, share.locales.tr("Published Properties"), cls.properties, "published")
            
            self.write_member_table(f, share.locales.tr("Public Fields"),        cls.fields,     "public")
            self.write_member_table(f, share.locales.tr("Protected Fields"),     cls.fields,     "protected")
            self.write_member_table(f, share.locales.tr("Private Fields"),       cls.fields,     "private")
            self.write_member_table(f, share.locales.tr("Published Fields"),     cls.fields,     "published")
            
            self.write_member_function_docs(f, cls)
            self.write_property_docs(f, cls)
            self.write_field_docs(f, cls)
        
        f.write("</section>\n")

    def _write_pdf_types(self, f, title, items):
        if not items:
            return

        f.write("<section>\n")
        f.write(f"<h2>{self.html_escape(title)}</h2>\n")

        for item in items:
            f.write(f"<h3>{self.html_escape(item.name)}</h3>\n")

            if item.brief:
                f.write(f"<p class=\"brief\">{self.html_escape(item.brief)}</p>\n")

            if item.signature:
                f.write(f"<pre class=\"declaration\">{self.html_escape(item.signature)}</pre>\n")

            self.current_output_class = item

            if item.fields:
                self.write_member_table(f, "Fields", item.fields, "public")

        f.write("</section>\n")
    
    def _write_pdf_enums(self, f):
        if not self.enums:
            return

        f.write("<section>\n")
        f.write("<h2>Enums</h2>\n")

        for item in self.enums:
            f.write(f"<h3>{self.html_escape(item.name)}</h3>\n")

            if item.brief:
                f.write(f"<p class=\"brief\">{self.html_escape(item.brief)}</p>\n")

            if item.signature:
                f.write(f"<pre class=\"declaration\">{self.html_escape(item.signature)}</pre>\n")

            if item.items:
                f.write("<table class=\"func-table\">\n")

                for enum_item in item.items:
                    f.write("<tr>\n")
                    f.write("<td class=\"ret\">enum</td>\n")
                    f.write(f"<td class=\"sig\"><span class=\"func-name\">{self.html_escape(enum_item['name'])}</span></td>\n")
                    f.write("</tr>\n")

                    if enum_item.get("brief"):
                        f.write("<tr class=\"member-brief-row\"><td></td>")
                        f.write(f"<td class=\"sig member-brief\">{self.html_escape(enum_item['brief'])}</td></tr>\n")

                f.write("</table>\n")

        f.write("</section>\n")
    
    def write_global_variables_section(self, f):
        if not self.global_vars:
            return
        
        f.write('<section class="doc-section" id="global_variables">\n')
        f.write('  <h2>Global Variables</h2>\n')
        f.write('  <table class="member-table">\n')
        f.write('    <tr><th>Type</th><th>Name</th><th>Description</th></tr>\n')
        
        for v in self.global_vars:
            name   = v.get("name", "")
            vtype  = v.get("type", "")
            brief  = v.get("brief", "")
            anchor = self.make_var_anchor(name)
            
            f.write(f'    <tr id="{anchor}">\n')
            f.write(f'      <td class="ret">{self.build_type_links(vtype)}</td>\n')
            f.write(f'      <td><a href="#{anchor}">{self.html_escape(name)}</a></td>\n')
            f.write(f'      <td>{self.html_escape(brief)}</td>\n')
            f.write('    </tr>\n')
        
        f.write('  </table>\n')
        f.write('</section>\n')
    
    def build_type_links(self):
        result = {}

        for cls in self.classes: result[cls.name.lower()] = self.safe_filename(cls.name) + ".html"
        for rec in self.records: result[rec.name.lower()] = self.safe_filename(rec.name) + ".html"
        for arr in self.arrays : result[arr.name.lower()] = self.safe_filename(arr.name) + ".html"
        for st  in self.sets   : result[st .name.lower()] = self.safe_filename(st .name) + ".html"

        return result
    
    def link_known_types(self, text):
        result = self.html_escape(text)
        
        known_items = (
            self.classes +
            self.interfaces +
            self.records +
            self.arrays +
            self.sets +
            self.enums
        )
        
        for item in known_items:
            full_name = item.name
            base_name = full_name.split("<", 1)[0]
            
            link = self.safe_filename(full_name) + ".html"
            
            result = result.replace(
                self.html_escape(full_name),
                f"<a class=\"type-link\" href=\"{link}\">{self.html_escape(full_name)}</a>"
            )
            
            result = result.replace(
                self.html_escape(base_name) + "&lt;",
                f"<a class=\"type-link\" href=\"{link}\">{self.html_escape(base_name)}</a>&lt;"
            )
        
        return result
    
    def join_pascal_tokens(self, tokens):
        result = ""
        no_space_before = { ")", "]", ",", ".", ":" }
        no_space_after  = { "(", "[", ".", "^"      }

        for token in tokens:
            if not token:
                continue
            if not result:
                result = token
                continue
            prev = result[-1]
            if token in no_space_before:
                result += token
            elif prev in "([.^":
                result += token
            else:
                result += " " + token
        result = result.strip()
        
        if result.endswith(";"):
            result = result[:-1].strip()
        
        return result
    
    def html_escape(self, text):
        return html.escape(text, quote=True)
    
    def safe_filename(self, name):
        result = []
        for ch in name:
            if ch.isalnum() or ch in "_-":
                result.append(ch)
            else:
                result.append("_")
        return "".join(result)
    
    def format_property_signature(self, signature):
        sig = signature.strip()
        sig = sig.replace(";", "")
        sig = sig.replace(" read ", "\n    read ")
        sig = sig.replace(" write ", "\n    write ")
        sig = self.html_escape(sig)
        
        if sig.startswith("property "):
            sig = sig.replace(
                "property ",
                "<span class=\"kw-property\">property</span> ",
                1
            )
        return sig
    
    def write_alpha_index(self, f):
        items = self.index_items()
        groups = {}
        for kind, name, link in items:
            key = self.alpha_key(name)
            groups.setdefault(key, []).append((kind, name, link))
        f.write("    <section class=\"alpha-index\">\n")
        f.write("      <h2>Index</h2>\n")
        f.write("      <div class=\"alpha-tabs\">\n")
        for ch in ALPHA_CHARS:
            if ch in groups:
                f.write(f"        <a href=\"#idx_{ch}\">{ch}</a>\n")
            else:
                f.write(f"        <span>{ch}</span>\n")
        f.write("      </div>\n")
        for ch in ALPHA_CHARS:
            if ch not in groups:
                continue
            f.write(f"      <h3 id=\"idx_{ch}\">{ch}</h3>\n")
            f.write("      <table class=\"func-table\">\n")
            for kind, name, link in groups[ch]:
                f.write("        <tr>\n")
                f.write(f"          <td class=\"ret\">{self.html_escape(kind)}</td>\n")
                f.write(f"          <td class=\"sig\"><a href=\"{link}\">{self.html_escape(name)}</a></td>\n")
                f.write("        </tr>\n")
            f.write("      </table>\n")
        f.write("    </section>\n")
    
    def write_search_box(self, f):
        f.write("    <section class=\"search-box\">\n")
        f.write("      <h2>Search</h2>\n")
        f.write("      <input id=\"docSearchInput\" type=\"text\" placeholder=\"Search documentation...\" autocomplete=\"off\">\n")
        f.write("      <div id=\"docSearchResults\" class=\"search-results\"></div>\n")
        f.write("    </section>\n")
    
    def write_index(self):
        filename = os.path.join(self.output_dir, "pascal", "index.html")
        with open(filename, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("  <meta charset=\"utf-8\">\n")
            f.write("  <title>Pascal Documentation</title>\n")
            f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
            f.write("  <script src=\"search_index.js\"></script>\n")
            f.write("</head>\n")
            f.write("<body>\n")
            if self.use_treeview:
                f.write("  <div class=\"layout\">\n")
                self.write_sidebar(f, None)
                f.write("    <div id=\"splitter\" class=\"splitter\"></div>\n")
                f.write("    <main class=\"page content-pane\">\n")
            else:
                f.write("  <main class=\"page\">\n")
            
            #f.write("    <div class=\"version\">Pascal Doc</div>\n")
            #f.write("    <h1>Pascal Documentation</h1>\n")
            #f.write("    <div class=\"breadcrumb\">\n")
            #f.write("      <span>Overview</span>\n")
            #f.write("    </div>\n")
            
            self.write_doc_header(
                f,
                "Pascal Documentation",
                None
            )
            #self.write_search_box(f)
            
            ###self.write_alpha_index(f)
            ###self.write_constants_index_section(f)
            
            #f.write("    <section>\n")
            
            self.write_index_section_alpha(
                f,
                share.locales.tr("Classes"),
                [("Class", cls.name, self.safe_filename(cls.name) + ".html") for cls in self.classes]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Interfaces"),
                [("Interface", item.name, self.safe_filename(item.name) + ".html") for item in self.interfaces]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Records"),
                [("Record", rec.name, self.safe_filename(rec.name) + ".html") for rec in self.records]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Arrays"),
                [("Array", arr.name, self.safe_filename(arr.name) + ".html") for arr in self.arrays]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Sets"),
                [("Set", st.name, self.safe_filename(st.name) + ".html") for st in self.sets]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Enums"),
                [("Enum", enm.name, self.safe_filename(enm.name) + ".html") for enm in self.enums]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Constants"),
                [("Constant", c.name, "#const_" + self.safe_filename(c.name)) for c in self.constants]
            )
            self.write_index_section_alpha(
                f,
                share.locales.tr("Global Variables"),
                [("Variable", v.name, "#" + self.make_var_anchor(v.name)) for v in self.global_vars]
            )
            
            self.write_constants_index_section(f)
            self.write_global_variable_groups_index_section(f)
            #self.write_global_variables_index_section(f)
            
            f.write("    <section>\n")
            
            #self.write_type_index_section(f, "Records", self.records)
            #self.write_type_index_section(f, "Arrays",  self.arrays)
            #self.write_type_index_section(f, "Sets",    self.sets)

            f.write(f"      <h2>{share.locales.tr("Classes")}</h2>\n")
            f.write("      <ul class=\"class-list\">\n")
            
            for cls in self.classes:
                html_name = self.safe_filename(cls.name) + ".html"
                f.write(
                    f"        <li><a href=\"{html_name}\">{self.html_escape(cls.name)}</a></li>\n"
                )
            
            f.write("      </ul>\n")
            f.write("    </section>\n")
            f.write("    <footer>\n")
            f.write("      Generated by <span>dBase Lexer + Parser</span> | Pascal Documentation Generator\n")
            f.write("    </footer>\n")
            f.write("    </main>\n")

            if self.use_treeview:
                f.write("  </div>\n")
                self.write_treeview_script(f)
                
            self.write_search_script(f)
            
            f.write("</body>\n")
            f.write("</html>\n")
        
        _write_css(os.path.join(self.output_dir, "pascal"))
    
    def write_global_variables_index_section(self, f):
        if not self.global_vars:
            return
        
        f.write("    <section>\n")
        f.write("      <h2>Global Variables</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        
        for v in self.global_vars:
            anchor = self.make_var_anchor(v.name)
            
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.link_known_types(v.vtype)}</td>\n")
            f.write(
                f"          <td class=\"sig\" id=\"{anchor}\">"
                f"<span class=\"func-name\">{self.html_escape(v.name)}</span></td>\n"
            )
            f.write("        </tr>\n")
            
            if v.brief:
                f.write("        <tr class=\"member-brief-row\">\n")
                f.write("          <td class=\"ret\"></td>\n")
                f.write(f"          <td class=\"sig member-brief\">{self.html_escape(v.brief)}</td>\n")
                f.write("        </tr>\n")
        
        f.write("      </table>\n")
        f.write("    </section>\n")
    
    def write_constants_index_section(self, f):
        if not self.constants:
            return
        f.write("    <section>\n")
        f.write("      <h2>Constants</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        for c in self.constants:
            anchor = "const_" + self.safe_filename(c.name)
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(c.value)}</td>\n")
            f.write(
                f"          <td class=\"sig\" id=\"{anchor}\">"
                f"<span class=\"func-name\">{self.html_escape(c.name)}</span></td>\n"
            )
            f.write("        </tr>\n")
            if c.brief:
                f.write("        <tr class=\"member-brief-row\">\n")
                f.write("          <td class=\"ret\"></td>\n")
                f.write(f"          <td class=\"sig member-brief\">{self.html_escape(c.brief)}</td>\n")
                f.write("        </tr>\n")
        f.write("      </table>\n")
        f.write("    </section>\n")
    
    def write_implemented_by_section(self, f, item):
        implemented_by = self.find_implemented_by(item.name)

        if not implemented_by:
            return

        f.write("    <section>\n")
        f.write("      <h2>Implemented By</h2>\n")
        f.write("      <ul class=\"implemented-by-list\">\n")

        for cls in implemented_by:
            link = self.safe_filename(cls.name) + ".html"
            f.write("        <li>")
            f.write(f"<a class=\"type-link\" href=\"{link}\">{self.html_escape(cls.name)}</a>")
            f.write("</li>\n")

        f.write("      </ul>\n")
        f.write("    </section>\n")
    
    def find_implemented_by(self, interface_name):
        result = []
        iface_key = self.normalize_type_name(interface_name)
        for cls in self.classes:
            for base in getattr(cls, "bases", []):
                if self.normalize_type_name(base) == iface_key:
                    result.append(cls)
        return result
    
    def find_derived_classes(self, class_name):
        result = []
        
        for cls in self.classes:
            for base in getattr(cls, "bases", []):
                if self.normalize_type_name(base) == self.normalize_type_name(class_name):
                    result.append(cls)

        return result
    
    def find_type_dependencies(self, item):
        result = []
        own_key = self.normalize_type_name(item.name)
        known   = {}
        for known_item in self.all_pascal_types():
            key = self.normalize_type_name(known_item.name)
            known[key] = known_item
        texts = []
        for base in getattr(item, "bases", []):
            texts.append(base)
        members = (
            getattr(item, "fields", []) +
            getattr(item, "properties", []) +
            getattr(item, "methods", [])
        )
        for member in members:
            texts.append(getattr(member, "signature", ""))
        if getattr(item, "signature", ""):
            texts.append(item.signature)
        for text in texts:
            text_key = text.lower()
            for key, known_item in known.items():
                if key == own_key:
                    continue
                if key in text_key:
                    if known_item not in result:
                        result.append(known_item)
        return result
    
    def write_derived_classes_section(self, f, cls):
        derived = self.find_derived_classes(cls.name)
        
        if not derived:
            return
        
        f.write("    <section>\n")
        f.write("      <h2>Derived Classes</h2>\n")
        f.write("      <ul class=\"derived-list\">\n")
        
        for item in derived:
            link = self.safe_filename(item.name) + ".html"
            f.write("        <li>")
            f.write(f"<a class=\"type-link\" href=\"{link}\">{self.html_escape(item.name)}</a>")
            f.write("</li>\n")
        
        f.write("      </ul>\n")
        f.write("    </section>\n")
    
    def write_inheritance_diagram(self, f, item):
        if not getattr(item, "bases", []):
            return
        
        f.write("    <section>\n")
        f.write("      <h2>Inheritance Diagram</h2>\n")
        f.write("      <div class=\"inheritance-diagram\">\n")
        
        for base in item.bases:
            f.write("        <div class=\"inheritance-node base-node\">\n")
            f.write(f"          {self.link_known_types(base)}\n")
            f.write("        </div>\n")
            f.write("        <div class=\"inheritance-arrow\">↓</div>\n")
        
        f.write("        <div class=\"inheritance-node current-node\">\n")
        f.write(f"          {self.html_escape(item.name)}\n")
        f.write("        </div>\n")
        
        f.write("      </div>\n")
        f.write("    </section>\n")
    
    def write_dependency_diagram(self, f, item):
        deps = self.find_type_dependencies(item)

        if not deps:
            return

        f.write("    <section>\n")
        f.write("      <h2>Dependency Diagram</h2>\n")
        f.write("      <div class=\"dependency-diagram\">\n")

        f.write("        <div class=\"dependency-node dependency-current\">\n")
        f.write(f"          {self.html_escape(item.name)}\n")
        f.write("        </div>\n")

        for dep in deps:
            link = self.safe_filename(dep.name) + ".html"

            f.write("        <div class=\"dependency-arrow\">↓</div>\n")
            f.write("        <div class=\"dependency-node dependency-target\">\n")
            f.write(f"          <a class=\"type-link\" href=\"{link}\">{self.html_escape(dep.name)}</a>\n")
            f.write("        </div>\n")

        f.write("      </div>\n")
        f.write("    </section>\n")
    
    def write_classes(self):
        os.makedirs(os.path.join(self.output_dir, "pascal" ), exist_ok=True)
        for cls in self.classes:
            self.current_output_class = cls
            filename = os.path.join(
                self.output_dir, "pascal",
                self.safe_filename(cls.name) + ".html")
            print("CLASS:", cls.name, "BASES:", getattr(cls, "bases", []))
            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n")
                f.write("<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(cls.name)} Class</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("  <script src=\"search_index.js\"></script>\n")
                f.write("</head>\n")
                f.write("<body>\n")
                
                if self.use_treeview:
                    f.write("  <div class=\"layout\">\n")
                    self.write_sidebar(f, cls)
                    f.write("    <div id=\"splitter\" class=\"splitter\"></div>\n")
                    f.write("    <main class=\"page content-pane\">\n")
                else:
                    f.write("  <main class=\"page\">\n")
                    
                #f.write("    <div class=\"version\">Pascal Doc</div>\n")
                #f.write(f"    <h1>{self.html_escape(cls.name)} Class</h1>\n")
                
                #f.write("    <div class=\"breadcrumb\">\n")
                #f.write("      <a href=\"index.html\">Overview</a>\n")
                #f.write("      <span>›</span>\n")
                #f.write(f"      <span>{self.html_escape(cls.name)}</span>\n")
                #f.write("    </div>\n")
                
                self.write_doc_header(
                    f,
                    f"{cls.name} Class",
                    cls.name
                )
                
                if cls.bases:
                    f.write("    <p class=\"inherits\">Inherits: ")
                    f.write(", ".join(self.html_escape(b) for b in cls.bases))
                    f.write("</p>\n")
                
                if cls.brief:
                    f.write(f"    <p class=\"brief\">{self.html_escape(cls.brief)}</p>\n")
                    
                self.write_inheritance_diagram(f, cls)
                self.write_derived_classes_section(f, cls)
                self.write_dependency_diagram(f, cls)
                self.write_cross_reference_section(f, cls)
                
                self.current_output_class = cls
                
                self.write_member_table(f, share.locales.tr("Public Methods")         , cls.methods, "public")
                self.write_member_table(f, share.locales.tr("Protected Methods")      , cls.methods, "protected")
                self.write_member_table(f, share.locales.tr("Private Methods")        , cls.methods, "private")
                self.write_member_table(f, share.locales.tr("Published Methods")      , cls.methods, "published")
                
                self.write_member_table(f, share.locales.tr("Public Properties")      , cls.properties, "public")
                self.write_member_table(f, share.locales.tr("Protected Properties")   , cls.properties, "protected")
                self.write_member_table(f, share.locales.tr("Private Properties")     , cls.properties, "private")
                self.write_member_table(f, share.locales.tr("Published Properties")   , cls.properties, "published")
                
                self.write_member_table(f, share.locales.tr("Public Fields")          , cls.fields, "public")
                self.write_member_table(f, share.locales.tr("Protected Fields")       , cls.fields, "protected")
                self.write_member_table(f, share.locales.tr("Private Fields")         , cls.fields, "private")
                self.write_member_table(f, share.locales.tr("Published Fields")       , cls.fields, "published")
                
                f.write("    <section>\n")
                f.write("      <h2>Detailed Description</h2>\n")
                f.write(f"      <p>The <span class=\"linklike\">{self.html_escape(cls.name)}</span> class.</p>\n")
                f.write("    </section>\n")
                
                self.write_member_function_docs(f, cls)
                self.write_property_docs(f, cls)
                self.write_field_docs(f, cls)
                
                f.write("    <footer>\n")
                f.write("      Generated by <span>dBase Lexer + Parser</span> | Pascal Documentation Generator\n")
                f.write("    </footer>\n")
                
                f.write("    </main>\n")
                
                if self.use_treeview:
                    f.write("  </div>\n")
                    self.write_treeview_script(f)
                
                self.write_search_script(f)
                f.write("</body>\n")
                f.write("</html>\n")
            
            #pdf_out = os.path.splitext(filename)[0] + ".pdf"
            #htm_out = filename
            #self.pdf_exports.append(HtmlToPdf(htm_out, pdf_out, DOXYGEN_WINDOW))
    
    def write_sidebar(self, f, current_item=None):
        f.write("    <aside id=\"tocPane\" class=\"toc-pane\">\n")
        f.write("      <div class=\"toc-title\">Table of Contents</div>\n")
        f.write("      <ul class=\"treeview\">\n")

        self.write_tree_group(f, "Classes", self.classes, "book")
        
        self.write_tree_type_group(f, share.locales.tr("Interfaces"), self.interfaces)
        self.write_tree_type_group(f, share.locales.tr("Records")   , self.records)
        self.write_tree_type_group(f, share.locales.tr("Arrays")    , self.arrays )
        self.write_tree_type_group(f, share.locales.tr("Sets")      , self.sets   )
        self.write_tree_type_group(f, share.locales.tr("Enums")     , self.enums  )

        self.write_const_tree_group(f, current_item)
        self.write_var_tree_group(f, current_item)

        f.write("      </ul>\n")
        f.write("    </aside>\n")
    
    def write_var_tree_group(self, f, current_item=None):
        if not self.global_vars:
            return
        
        page_name = "index.html"
        
        f.write("        <li class=\"tree-node\">\n")
        f.write(
            "          <div class=\"tree-row tree-toggle\">"
            "<span class=\"twisty\">▸</span>"
            "<span class=\"icon book-icon\"></span>"
            "<span>Global Variables</span></div>\n"
        )
        f.write("          <ul class=\"collapsed\">\n")
        
        for v in self.global_vars:
            anchor = self.make_var_anchor(v.name)
            f.write("            <li>\n")
            f.write(
                f"              <div class=\"tree-row\">"
                f"<span class=\"twisty empty\"></span>"
                f"<span class=\"icon page-icon\"></span>"
                f"<a href=\"{page_name}#{anchor}\">{self.html_escape(v.name)}</a></div>\n"
            )
            f.write("            </li>\n")
        
        f.write("          </ul>\n")
        f.write("        </li>\n")
    
    def write_tree_type_group(self, f, title, items):
        if not items:
            return
        f.write("        <li class=\"tree-node\">\n")
        f.write(
            f"          <div class=\"tree-row tree-toggle\">"
            f"<span class=\"twisty\">▸</span>"
            f"<span class=\"icon book-icon\"></span>"
            f"<span>{self.html_escape(title)}</span></div>\n")
        f.write("          <ul class=\"collapsed\">\n")
        for item in items:
            f.write("            <li>\n")
            f.write(
                f"              <div class=\"tree-row\">"
                f"<span class=\"twisty empty\"></span>"
                f"<span class=\"icon page-icon\"></span>"
                f"<a href=\"{self.safe_filename(item.name)}.html\">{self.html_escape(item.name)}</a></div>\n")
            f.write("            </li>\n")
        f.write("          </ul>\n")
        f.write("        </li>\n")
    
    def write_index_section_alpha(self, f, title, items):
        if not items:
            return
        groups = {}
        for kind, name, link in items:
            key = self.alpha_key(name)
            groups.setdefault(key, []).append((kind, name, link))
        f.write("    <section>\n")
        f.write(f"      <h2>{self.html_escape(title)}</h2>\n")
        f.write("      <div class=\"alpha-tabs\">\n")
        for ch in ALPHA_CHARS:
            if ch in groups:
                f.write(f"        <a href=\"#{self.safe_filename(title)}_{ch}\">{ch}</a>\n")
            else:
                f.write(f"        <span>{ch}</span>\n")
        f.write("      </div>\n")
        for ch in ALPHA_CHARS:
            if ch not in groups:
                continue
            f.write(f"      <h3 id=\"{self.safe_filename(title)}_{ch}\">{ch}</h3>\n")
            f.write("      <table class=\"func-table\">\n")
            for kind, name, link in groups[ch]:
                f.write("        <tr>\n")
                f.write(f"          <td class=\"ret\">{self.html_escape(kind)}</td>\n")
                f.write(f"          <td class=\"sig\"><a href=\"{link}\">{self.html_escape(name)}</a></td>\n")
                f.write("        </tr>\n")
            f.write("      </table>\n")
        f.write("    </section>\n")
    
    def write_const_tree_group(self, f, current_item=None):
        if not self.constants:
            return
        
        page_name = "index.html"
        
        f.write("        <li class=\"tree-node\">\n")
        f.write(
            "          <div class=\"tree-row tree-toggle\">"
            "<span class=\"twisty\">▸</span>"
            "<span class=\"icon book-icon\"></span>"
            "<span>Constants</span></div>\n"
        )
        f.write("          <ul class=\"collapsed\">\n")
        
        for c in self.constants:
            anchor = "const_" + self.safe_filename(c.name)
            f.write("            <li>\n")
            f.write(
                f"              <div class=\"tree-row\">"
                f"<span class=\"twisty empty\"></span>"
                f"<span class=\"icon page-icon\"></span>"
                f"<a href=\"{page_name}#{anchor}\">{self.html_escape(c.name)}</a></div>\n"
            )
            f.write("            </li>\n")
        
        f.write("          </ul>\n")
        f.write("        </li>\n")
    
    def write_search_script(self, f):
        f.write(share.locales.tr("doxy_html_javascript"))

    def write_treeview_script(self, f):
        f.write(share.locales.tr("doxy_html_treeview_js"))
    
    def write_pascal_enums(self):
        out_dir = os.path.join(self.output_dir, "pascal")
        os.makedirs(out_dir, exist_ok=True)
        
        for item in self.enums:
            filename = os.path.join(out_dir, self.safe_filename(item.name) + ".html")
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(item.name)}</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("  <script src=\"search_index.js\"></script>\n")
                f.write("</head>\n<body>\n")
                
                if self.use_treeview:
                    f.write("  <div class=\"layout\">\n")
                    self.write_sidebar(f, item)
                    f.write("    <div id=\"splitter\" class=\"splitter\"></div>\n")
                    f.write("    <main class=\"page content-pane\">\n")
                else:
                    f.write("  <main class=\"page\">\n")
                
                #f.write("    <div class=\"version\">Pascal Doc</div>\n")
                #f.write(f"    <h1>{self.html_escape(item.name)} enum</h1>\n")
                
                self.write_doc_header(
                    f,
                    f"{item.name} enum",
                    item.name
                )
                
                if item.brief:
                    f.write(f"    <p class=\"brief\">{self.html_escape(item.brief)}</p>\n")
                
                f.write("    <section>\n")
                f.write("      <h2>Declaration</h2>\n")
                f.write(f"      <pre class=\"declaration\">{self.html_escape(item.signature)}</pre>\n")
                f.write("    </section>\n")
                
                if item.items:
                    f.write("    <section>\n")
                    f.write("      <h2>Enum Values</h2>\n")
                    f.write("      <table class=\"func-table\">\n")
                    
                    for enum_item in item.items:
                        f.write("        <tr>\n")
                        f.write("          <td class=\"ret\">enum</td>\n")
                        f.write(
                            f"          <td class=\"sig\"><span class=\"func-name\">"
                            f"{self.html_escape(enum_item['name'])}</span></td>\n"
                        )
                        f.write("        </tr>\n")
                        
                        if enum_item.get("brief"):
                            f.write("        <tr class=\"member-brief-row\">\n")
                            f.write("          <td class=\"ret\"></td>\n")
                            f.write(
                                f"          <td class=\"sig member-brief\">"
                                f"{self.html_escape(enum_item['brief'])}</td>\n"
                            )
                            f.write("        </tr>\n")
                    
                    f.write("      </table>\n")
                    f.write("    </section>\n")
                
                f.write("    </main>\n")
                
                if self.use_treeview:
                    f.write("  </div>\n")
                    self.write_treeview_script(f)
                
                self.write_search_script(f)
                f.write("</body>\n</html>\n")
            
            #pdf_out = os.path.splitext(filename)[0] + ".pdf"
            #htm_out = filename
            #self.pdf_exports.append(HtmlToPdf(htm_out, pdf_out, DOXYGEN_WINDOW))
            
    def write_tree_group(self, f, title, classes, icon):
        if not classes:
            return

        f.write("        <li class=\"tree-node open\">\n")
        f.write("          <div class=\"tree-row tree-toggle\"><span class=\"twisty\">▾</span><span class=\"icon book-icon\"></span><span>Classes</span></div>\n")
        f.write("          <ul>\n")

        for cls in classes:
            f.write("            <li class=\"tree-node open\">\n")
            f.write(
                f"              <div class=\"tree-row tree-toggle\"><span class=\"twisty\">▾</span>"
                f"<span class=\"icon book-icon\"></span>"
                f"<a href=\"{self.safe_filename(cls.name)}.html\">{self.html_escape(cls.name)}</a></div>\n"
            )
            f.write("              <ul>\n")

            self.write_member_tree_group(f, cls, "Fields", cls.fields)
            self.write_member_tree_group(f, cls, "Properties", cls.properties)

            ctors = []
            dtors = []
            funcs = []
            procs = []

            for member in cls.methods:
                sig = member.signature.strip().lower()
                if sig.startswith("constructor "):
                    ctors.append(member)
                elif sig.startswith("destructor "):
                    dtors.append(member)
                elif sig.startswith("function "):
                    funcs.append(member)
                elif sig.startswith("procedure "):
                    procs.append(member)

            self.write_member_tree_group(f, cls, "Constructors", ctors)
            self.write_member_tree_group(f, cls, "Destructors", dtors)
            self.write_member_tree_group(f, cls, "Functions", funcs)
            self.write_member_tree_group(f, cls, "Procedures", procs)

            f.write("              </ul>\n")
            f.write("            </li>\n")
        f.write("          </ul>\n")
        f.write("        </li>\n")
    
    def write_pascal_types(self, items):
        out_dir = os.path.join(self.output_dir, "pascal")
        os.makedirs(out_dir, exist_ok=True)

        for item in items:
            filename = os.path.join(out_dir, self.safe_filename(item.name) + ".html")

            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(item.name)}</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("  <script src=\"search_index.js\"></script>\n")
                f.write("</head>\n<body>\n")
                
                if self.use_treeview:
                    f.write("  <div class=\"layout\">\n")
                    self.write_sidebar(f, item)
                    f.write("    <div id=\"splitter\" class=\"splitter\"></div>\n")
                    f.write("    <main class=\"page content-pane\">\n")
                else:
                    f.write("  <main class=\"page\">\n")
                
                #f.write("    <div class=\"version\">Pascal Doc</div>\n")
                #f.write(f"    <h1>{self.html_escape(item.name)} {self.html_escape(item.kind)}</h1>\n")

                #f.write("    <div class=\"breadcrumb\">\n")
                #f.write("      <a href=\"index.html\">Overview</a>\n")
                #f.write("      <span>›</span>\n")
                #f.write(f"      <span>{self.html_escape(item.name)}</span>\n")
                #f.write("    </div>\n")
                
                self.write_doc_header(
                    f,
                    f"{item.name} {item.kind}",
                    item.name
                )

                if item.brief:
                    f.write(f"    <p class=\"brief\">{self.html_escape(item.brief)}</p>\n")

                f.write("    <section>\n")
                f.write("      <h2>Declaration</h2>\n")
                f.write(f"      <pre class=\"declaration\">{self.html_escape(item.signature)}</pre>\n")
                f.write("    </section>\n")
                
                self.write_cross_reference_section(f, item)
                self.current_output_class = item
                if item.fields:
                    self.write_member_table(f, "Fields", item.fields, "public")
                
                f.write("    </main>\n")
                
                if self.use_treeview:
                    f.write("  </div>\n")
                    self.write_treeview_script(f)
                
                self.write_search_script(f)
                f.write("</body>\n</html>\n")
            
            #pdf_out = os.path.splitext(filename)[0] + ".pdf"
            #htm_out = filename
            #self.pdf_exports.append(HtmlToPdf(htm_out, pdf_out, DOXYGEN_WINDOW))
            
    def write_type_index_section(self, f, title, items):
        if not items:
            return
        f.write(f"      <h2>{self.html_escape(title)}</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        for item in items:
            html_name = self.safe_filename(item.name) + ".html"
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(item.kind)}</td>\n")
            f.write(f"          <td class=\"sig\"><a href=\"{html_name}\">{self.html_escape(item.name)}</a></td>\n")
            f.write("        </tr>\n")
            if item.brief:
                f.write("        <tr class=\"member-brief-row\">\n")
                f.write("          <td class=\"ret\"></td>\n")
                f.write(f"          <td class=\"sig member-brief\">{self.html_escape(item.brief)}</td>\n")
                f.write("        </tr>\n")
        f.write("      </table>\n")
        
    def write_member_table(self, f, title, members, access_filter=None):
        items = []
        
        for member in members:
            if access_filter is None or member.access == access_filter:
                items.append(member)
        
        if not items:
            return
        
        f.write("    <section>\n")
        f.write(f"      <h2>{self.html_escape(title)}</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        
        for member in items:
            left, right = self.split_pascal_signature(member.signature)
            
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(left)}</td>\n")
            
            anchor = self.make_member_anchor(self.current_output_class, member)
            f.write(
                f"          <td class=\"sig\">"
                f"<a class=\"member-link\" href=\"#{anchor}\">"
                f"{self.highlight_signature(right)}"
                f"</a></td>\n"
            )
            
            f.write("        </tr>\n")
            
            if getattr(member, "brief", ""):
                f.write("        <tr class=\"member-brief-row\">\n")
                f.write("          <td class=\"ret\"></td>\n")
                f.write(f"          <td class=\"sig member-brief\">{self.html_escape(member.brief)}</td>\n")
                f.write("        </tr>\n")
                
        f.write("      </table>\n")
        f.write("    </section>\n")

    def write_member_function_docs(self, f, cls):
        ctors_dtors = []
        methods     = []
        for member in cls.methods:
            sig = member.signature.strip().lower()
            if sig.startswith("constructor ") or sig.startswith("destructor "):
                ctors_dtors.append(member)
            else:
                methods.append(member)
        if not ctors_dtors and not methods:
            return
        f.write("    <section class=\"member-docs\">\n")
        if ctors_dtors:
            f.write("      <h2>Constructors and Destructor</h2>\n")
            self.write_member_doc_items(f, cls, ctors_dtors)
        if methods:
            f.write("      <h2>Member Function Documentation</h2>\n")
            self.write_member_doc_items(f, cls, methods)
        f.write("    </section>\n")
    
    def write_member_doc_items(self, f, cls, members):
        for member in members:
            full_signature = self.make_qualified_signature(cls.name, member.signature)
            full_signature = self.format_pascal_signature_multiline(full_signature)
            anchor         = self.make_member_anchor(cls, member)
            
            f.write(f"      <article class=\"member-doc-box\" id=\"{anchor}\">\n")
            f.write("        <div class=\"member-doc-title\">\n")
            f.write(f"          {self.highlight_multiline_signature(full_signature)}\n")
            f.write("        </div>\n")
            f.write("        <div class=\"member-doc-content\">\n")
            if member.brief:
                f.write(f"          <p>{self.html_escape(member.brief)}</p>\n")
            if member.params:
                f.write("          <h4>Parameters</h4>\n")
                f.write("          <table class=\"param-table\">\n")
                for param_name, param_desc in member.params:
                    f.write("            <tr>\n")
                    f.write(f"              <td class=\"param-name\">{self.html_escape(param_name)}</td>\n")
                    f.write(f"              <td>{self.html_escape(param_desc)}</td>\n")
                    f.write("            </tr>\n")
                f.write("          </table>\n")
            if member.returns:
                f.write("          <h4>Returns</h4>\n")
                f.write("          <table class=\"return-table\">\n")
                f.write("            <tr>\n")
                f.write("              <td class=\"return-indent\"></td>\n")
                f.write(f"              <td class=\"return-text\">{self.html_escape(member.returns)}</td>\n")
                f.write("            </tr>\n")
                f.write("          </table>\n")
            self.write_note_blocks(f, member)
            f.write("        </div>\n")
            f.write("      </article>\n")
    
    def is_constructor_or_destructor(self, member):
        sig = member.signature.strip().lower()
        return (
            sig.startswith("constructor ") or
            sig.startswith("destructor ")
        )
    
    def _write_member_function_docs(self, f, cls):
        if not cls.methods:
            return
        
        f.write("    <section class=\"member-docs\">\n")
        f.write("      <h2>Member Function Documentation</h2>\n")
        
        for member in cls.methods:
            full_signature = self.make_qualified_signature(cls.name, member.signature)
            full_signature = self.format_pascal_signature_multiline( full_signature  )
            
            f.write("      <article class=\"member-doc-box\">\n")
            f.write("        <div class=\"member-doc-title\">\n")
            f.write(f"          {self.highlight_multiline_signature(full_signature)}\n")
            f.write("        </div>\n")
            f.write("        <div class=\"member-doc-content\">\n")
            
            if member.brief:
                f.write(f"          <p>{self.html_escape(member.brief)}</p>\n")
            if member.params:
                f.write("          <h4>Parameters</h4>\n")
                f.write("          <table class=\"param-table\">\n")
                for param_name, param_desc in member.params:
                    f.write("            <tr>\n")
                    f.write(f"              <td class=\"param-name\">{self.html_escape(param_name)}</td>\n")
                    f.write(f"              <td>{self.html_escape(param_desc)}</td>\n")
                    f.write("            </tr>\n")
                f.write("          </table>\n")
            if member.returns:
                f.write("          <h4>Returns</h4>\n")
                f.write("          <table class=\"return-table\">\n")
                f.write("            <tr>\n")
                f.write("              <td class=\"return-indent\"></td>\n")
                f.write(f"              <td class=\"return-text\">{self.html_escape(member.returns)}</td>\n")
                f.write("            </tr>\n")
                f.write("          </table>\n")
                
            self.write_note_blocks(f, member)
            
            f.write("        </div>\n")
            f.write("      </article>\n")
        f.write("    </section>\n")
    
    def _write_pdf_interfaces(self, f):
        if not self.interfaces:
            return

        f.write("<section>\n")
        f.write("<h2>Interfaces</h2>\n")

        for item in self.interfaces:
            f.write(f"<h3>{self.html_escape(item.name)}</h3>\n")

            if item.brief:
                f.write(f"<p class=\"brief\">{self.html_escape(item.brief)}</p>\n")

            if item.bases:
                f.write("<p class=\"inherits\">Inherits: ")
                f.write(", ".join(self.html_escape(b) for b in item.bases))
                f.write("</p>\n")

            self.current_output_class = item
            self.write_inheritance_diagram(f, item)

            self.write_member_table(f, "Methods", item.methods, "public")
            self.write_member_table(f, "Properties", item.properties, "public")

            self.write_member_function_docs(f, item)
            self.write_property_docs(f, item)

        f.write("</section>\n")
    
    def write_interfaces(self):
        os.makedirs(os.path.join(self.output_dir, "pascal"), exist_ok=True)

        for item in self.interfaces:
            self.current_output_class = item

            filename = os.path.join(
                self.output_dir,
                "pascal",
                self.safe_filename(item.name) + ".html"
            )

            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n")
                f.write("<html>\n")
                f.write("<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(item.name)} Interface</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("  <script src=\"search_index.js\"></script>\n")
                f.write("</head>\n")
                f.write("<body>\n")

                if self.use_treeview:
                    f.write("  <div class=\"layout\">\n")
                    self.write_sidebar(f, item)
                    f.write("    <div id=\"splitter\" class=\"splitter\"></div>\n")
                    f.write("    <main class=\"page content-pane\">\n")
                else:
                    f.write("  <main class=\"page\">\n")

                self.write_doc_header(
                    f,
                    f"{item.name} Interface",
                    item.name
                )

                if item.bases:
                    f.write("    <p class=\"inherits\">Inherits: ")
                    f.write(", ".join(self.html_escape(b) for b in item.bases))
                    f.write("</p>\n")

                if item.brief:
                    f.write(f"    <p class=\"brief\">{self.html_escape(item.brief)}</p>\n")

                self.current_output_class = item
                
                self.write_inheritance_diagram      (f, item)
                self.write_implemented_by_section   (f, item)
                self.write_dependency_diagram       (f, item)
                self.write_cross_reference_section  (f, item)
                
                self.write_member_table(f, "Methods", item.methods, "public")
                self.write_member_table(f, "Properties", item.properties, "public")

                f.write("    <section>\n")
                f.write("      <h2>Detailed Description</h2>\n")
                f.write(f"      <p>The <span class=\"linklike\">{self.html_escape(item.name)}</span> interface.</p>\n")
                f.write("    </section>\n")

                self.write_member_function_docs(f, item)
                self.write_property_docs(f, item)

                f.write("    <footer>\n")
                f.write("      Generated by <span>dBase Lexer + Parser</span> | Pascal Documentation Generator\n")
                f.write("    </footer>\n")

                f.write("    </main>\n")

                if self.use_treeview:
                    f.write("  </div>\n")
                    self.write_treeview_script(f)

                self.write_search_script(f)
                f.write("</body>\n")
                f.write("</html>\n")
            
    def write_note_blocks(self, f, member):
        for kind, text in getattr(member, "notes", []):
            title = {
                "note": "Note",
                "info": "Info",
                "warn": "Warning"
            }.get(kind, "Note")

            f.write(f"          <div class=\"doc-box doc-box-{kind}\">\n")
            f.write(f"            <div class=\"doc-box-title\">{title}</div>\n")
            f.write(f"            <div class=\"doc-box-text\">{self.html_escape(text)}</div>\n")
            f.write("          </div>\n")
            
    def write_property_docs(self, f, cls):
        if not cls.properties:
            return
        
        f.write("    <section class=\"member-docs\">\n")
        f.write("      <h2>Property Documentation</h2>\n")
        
        msg = share.locales.tr("No documentation for this Property")
        for member in cls.properties:
            anchor = self.make_member_anchor(cls, member)
            
            f.write(f"      <article class=\"member-doc\" id=\"{anchor}\">\n")
            f.write("        <h3>\n")
            f.write("          <pre class=\"property-signature\">\n")
            f.write(f"{self.format_property_signature(member.signature)}\n")
            f.write("          </pre>\n")
            f.write("        </h3>\n")
            f.write("        <div class=\"member-line\"></div>\n")
            
            brief = getattr(member, "brief", "")
            
            type_brief  = getattr(member, "property_type_brief", "")
            read_brief  = getattr(member, "property_read_brief", "")
            write_brief = getattr(member, "property_write_brief", "")

            has_any_doc = bool(brief or type_brief or read_brief or write_brief)

            if has_any_doc:
                if brief:
                    f.write("        <p>\n")
                    f.write(f"          {self.html_escape(brief)}\n")
                    f.write("        </p>\n")
                
                if type_brief:
                    f.write("        <div class=\"property-doc-item\">\n")
                    f.write("          <div class=\"property-doc-label\">Type</div>\n")
                    f.write(f"          <div class=\"property-doc-text\">{self.html_escape(type_brief)}</div>\n")
                    f.write("        </div>\n")
                
                if read_brief:
                    f.write("        <div class=\"property-doc-item\">\n")
                    f.write("          <div class=\"property-doc-label\">Read</div>\n")
                    f.write(f"          <div class=\"property-doc-text\">{self.html_escape(read_brief)}</div>\n")
                    f.write("        </div>\n")
                
                if write_brief:
                    f.write("        <div class=\"property-doc-item\">\n")
                    f.write("          <div class=\"property-doc-label\">Write</div>\n")
                    f.write(f"          <div class=\"property-doc-text\">{self.html_escape(write_brief)}</div>\n")
                    f.write("        </div>\n")
            
            else:
                f.write("        <p>\n")
                f.write(f"          {msg}.\n")
                f.write("        </p>\n")
            
            f.write("      </article>\n")
        
        f.write("    </section>\n")

    def write_field_docs(self, f, cls):
        if not cls.fields:
            return
        f.write("    <section class=\"member-docs\">\n")
        f.write("      <h2>Field Documentation</h2>\n")
        msg = share.locales.tr("No documentation for this Field")
        for member in cls.fields:
            anchor = self.make_member_anchor(cls, member)
            f.write(f"      <article class=\"member-doc\" id=\"{anchor}\">\n")
            f.write(f"        <h3>{self.highlight_signature(member.signature)}</h3>\n")
            f.write("        <div class=\"member-line\"></div>\n")
            brief = getattr(member, "brief", "")
            if brief:
                f.write("        <p>\n")
                f.write(f"       {self.html_escape(brief)}\n")
                f.write("        </p>\n")
            else:
                f.write("        <p>\n")
                f.write(f"          {msg}.\n")
                f.write("        </p>\n")
            f.write("      </article>\n")
        f.write("    </section>\n")
    
    def write_member_tree(self, f, cls):
        ctors = []
        dtors = []
        funcs = []
        procs = []

        for member in cls.methods:
            sig = member.signature.strip()
            low = sig.lower()

            if   low.startswith("constructor "): ctors.append(member)
            elif low.startswith("destructor " ): dtors.append(member)
            elif low.startswith("function "   ): funcs.append(member)
            elif low.startswith("procedure "  ): procs.append(member)

        self.write_member_tree_group(f, cls, "Fields"    , cls.fields)
        self.write_member_tree_group(f, cls, "Properties", cls.properties)
        self.write_member_tree_group(f, cls, "Ctors"     , ctors)
        self.write_member_tree_group(f, cls, "Dtors"     , dtors)
        self.write_member_tree_group(f, cls, "Functions" , funcs)
        self.write_member_tree_group(f, cls, "Procedures", procs)
    
    def write_member_tree_group(self, f, cls, title, members):
        if not members:
            return
        f.write("                <li class=\"tree-node\">\n")
        f.write(
            f"                  <div class=\"tree-row tree-toggle\">"
            f"<span class=\"twisty\">▸</span>"
            f"<span class=\"icon book-icon\"></span>"
            f"<span>{self.html_escape(title)}</span></div>\n"
        )
        f.write("                  <ul class=\"collapsed\">\n")
        for member in members:
            name   = self.member_display_name(member)
            anchor = self.make_member_anchor(cls, member)
            f.write("                    <li>\n")
            f.write(
                f"                      <div class=\"tree-row\">"
                f"<span class=\"twisty empty\"></span>"
                f"<span class=\"icon page-icon\"></span>"
                f"<a href=\"{self.safe_filename(cls.name)}.html#{anchor}\">{self.html_escape(name)}</a></div>\n"
            )
            f.write("                    </li>\n")
        f.write("                  </ul>\n")
        f.write("                </li>\n")
    
    def generic_params_from_ctx(self, ctx):
        if not hasattr(ctx, "genericParams"):
            return ""
        
        gp = ctx.genericParams()
        if not gp:
            return ""
        
        names = []
        
        for ident in gp.IDENT():
            names.append(ident.getText())
        
        return "<" + ", ".join(names) + ">"
        
    def member_display_name(self, member):
        sig = member.signature.strip()
        low = sig.lower()
        for prefix in ["constructor", "destructor", "procedure", "function", "property"]:
            if low.startswith(prefix + " "):
                text = sig[len(prefix):].strip()
                break
        else:
            text = sig
        pos1 = text.find("(")
        pos2 = text.find(":")
        cuts = [p for p in [pos1, pos2] if p >= 0]
        if cuts:
            text = text[:min(cuts)].strip()
        return text
    
    def write_type_tree_section(self, f, title, items):
        if not items:
            return
        f.write("    <details>\n")
        f.write(f"      <summary>{self.html_escape(title)}</summary>\n")
        f.write("      <ul>\n")
        for item in items:
            f.write(
                f"        <li><a href=\"{self.safe_filename(item.name)}.html\">"
                f"{self.html_escape(item.name)}</a></li>\n")
        f.write("      </ul>\n")
        f.write("    </details>\n")
    
    def write_const_tree_section(self, f):
        if not self.constants:
            return
        f.write("    <details>\n")
        f.write("      <summary>Constants</summary>\n")
        f.write("      <ul>\n")
        for c in self.constants:
            f.write(f"        <li>{self.html_escape(c.name)}</li>\n")
        f.write("      </ul>\n")
        f.write("    </details>\n")
    
    def split_pascal_signature(self, signature):
        text = signature.strip()
        if text.lower().startswith("property "):
            body = text[len("property "):].strip()
            return "property", body
        lower_text = text.lower()
        for prefix in ["constructor", "destructor", "procedure", "function"]:
            if lower_text.startswith(prefix + " "):
                body = text[len(prefix):].strip()
                return prefix, body
        if ":" in text:
            left, right = text.split(":", 1)
            return right.strip(), left.strip()
        parts = text.rsplit(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "", text

    def highlight_signature(self, signature):
        text = self.link_known_types(signature)
        text = text.replace("\n", "<br>")
        pos  = text.find("(")
        
        colon_pos = text.find(":")
        end_pos   = -1
        
        if pos >= 0 and colon_pos >= 0:
            end_pos = min(pos, colon_pos)
        elif pos >= 0:
            end_pos = pos
        elif colon_pos >= 0:
            end_pos = colon_pos
            
        if end_pos > 0:
            name = text[:end_pos]
            rest = text[end_pos:]
            return f"<span class=\"func-name\">{name}</span>{rest}"
            
        parts = text.split(" ", 1)
        
        if len(parts) == 2:
            return f"<span class=\"func-name\">{parts[0]}</span> {parts[1]}"
        return f"<span class=\"func-name\">{text}</span>"
    
    def delete_old_topic_pdfs(self):
        out_dir = os.path.join(self.output_dir, "pascal")
        if not os.path.isdir(out_dir):
            return
        keep = { "PascalDocumentation.pdf" }
        for name in os.listdir(out_dir):
            if name.lower().endswith(".pdf") and name not in keep:
                try:
                    os.remove(os.path.join(out_dir, name))
                except Exception as e:
                    QMessageBox.warning(DOXYGEN_WINDOW,
                        share.locales.tr("PDF Error"),
                        share.locales.tr("PDF delete failed") + ": " + name)
                    return
    
    def highlight_multiline_signature(self, signature):
        text     = self.link_known_types(signature)
        keywords = [
            "constructor",
            "destructor",
            "procedure",
            "function"
        ]
        for keyword in keywords:
            if text.lower().startswith(keyword + " "):
                text = (
                    f"<span class=\"func-name\">{text[:len(keyword)]}</span>"
                    + text[len(keyword):]
                )
                break
        lines = text.split("\n")
        for i in range(1, len(lines)):
            lines[i] = (
                "<span class=\"member-args\">"
                + lines[i].replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")
                + "</span>"
            )
        text = "<br>".join(lines)
        return text
        
    def make_qualified_signature(self, class_name, signature):
        text = signature.strip()
        lower_text = text.lower()
        for prefix in ["constructor", "destructor", "procedure", "function"]:
            if lower_text.startswith(prefix + " "):
                body      = text[len(prefix):].strip()
                pos       = body.find("(")
                colon_pos = body.find(":")
                if pos >= 0 and colon_pos >= 0:
                    end_pos = min(pos, colon_pos)
                elif pos >= 0:
                    end_pos = pos
                elif colon_pos >= 0:
                    end_pos = colon_pos
                else:
                    end_pos = len(body)
                name = body[:end_pos].strip()
                rest = body[end_pos:].strip()
                return f"{prefix} {class_name}.{name}{rest}"
        return text

# ---------------------------------------------------------------------------
# \brief c++ documentation visitor to generate the c++ html help ...
# ---------------------------------------------------------------------------
class CppDocHtmlVisitor(CppDocParserVisitor):
    def __init__(self, output_dir="html"):
        super().__init__()
        
        self.output_dir = output_dir
        self.classes = []
        self.current_class = None
        self.current_access = "private"
    
    def visitTranslationUnit(self, ctx: CppDocParser.TranslationUnitContext):
        self.visitChildren(ctx)
        self.write_index()
        self.write_classes()
        return self.classes
    
    def visitClassDeclaration(self, ctx: CppDocParser.ClassDeclarationContext):
        class_name = ctx.IDENT().getText()
        
        old_class  = self.current_class
        old_access = self.current_access
        
        info = CppClassInfo(class_name)
        info.kind = ctx.classKind().getText()

        if info.kind == "struct":
            self.current_access = "public"
        else:
            self.current_access = "private"

        if ctx.inheritance():
            for item in ctx.inheritance().inheritanceItem():
                info.bases.append(self.text_from_ctx(item))

        self.current_class = info
        self.visit(ctx.classBody())
        self.classes.append(info)

        self.current_class  = old_class
        self.current_access = old_access

        return info

    def visitAccessSection(self, ctx: CppDocParser.AccessSectionContext):
        self.current_access = ctx.accessSpecifier().getText()
        return None

    def visitMethodDeclaration(self, ctx: CppDocParser.MethodDeclarationContext):
        if self.current_class is None:
            return None

        signature = self.text_from_ctx(ctx)

        self.current_class.methods.append(
            CppMemberInfo(self.current_access, signature)
        )

        return None

    def visitFieldDeclaration(self, ctx: CppDocParser.FieldDeclarationContext):
        if self.current_class is None:
            return None

        signature = self.text_from_ctx(ctx)

        self.current_class.fields.append(
            CppMemberInfo(self.current_access, signature)
        )

        return None

    def format_signature(self, text):
        text = text.replace(";", "")
        text = text.replace(",", ", ")
        text = text.replace("(", "(")
        text = text.replace(")", ")")
        text = text.replace("*", " *")
        text = text.replace("&", " &")
        return text.strip()
    
    def text_from_ctx(self, ctx):
        tokens = []
        for child in ctx.getChildren():
            if hasattr(child, "symbol"):
                tokens.append(child.getText())
            else:
                sub_text = self.text_from_ctx(child)
                if sub_text:
                    tokens.extend(sub_text.split(" "))
        return self.join_cpp_tokens(tokens)

    def join_cpp_tokens(self, tokens):
        result = ""
        no_space_before = { ")", "]", "}", ";", ",", "::" }
        no_space_after  = { "(", "[", "{", "::", "~"      }
        
        space_around    = { "*", "&", "=", "+", "-", "/", "%", "<", ">" }

        for token in tokens:
            if not token:
                continue
            if not result:
                result = token
                continue
            prev = result[-1]
            if token in no_space_before:
                result += token
            elif prev in "([{~":
                result += token
            elif token in space_around:
                result += " " + token
            elif prev in "*&=+-/%<>":
                result += " " + token
            else:
                result += " " + token
        return result.strip()
    
    def pretty_cpp_text(self, text):
        text = text.strip()
        
        text = text.replace(" *", " *")
        text = text.replace("* ", "* ")
        text = text.replace(" &", " &")
        text = text.replace("& ", "& ")

        text = text.replace(" (", "(")
        text = text.replace("( ", "(")
        text = text.replace(" )", ")")
        text = text.replace(" ,", ",")
        text = text.replace(", ", ", ")

        text = text.replace(" ;", "")

        while "  " in text:
            text = text.replace("  ", " ")

        return text
    
    def safe_filename(self, name):
        result = []

        for ch in name:
            if ch.isalnum() or ch in "_-":
                result.append(ch)
            else:
                result.append("_")

        return "".join(result)

    def html_escape(self, text):
        return html.escape(text, quote=True)

    def write_index(self):
        os.makedirs(os.path.join(self.output_dir, "cpp"), exist_ok=True)
        filename  = os.path.join(self.output_dir, "cpp\\index.html")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("  <meta charset=\"utf-8\">\n")
            f.write("  <title>C++ Documentation</title>\n")
            f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
            f.write("</head>\n")
            f.write("<body>\n")
            f.write("  <h1>C++ Documentation</h1>\n")
            f.write("  <h2>Classes</h2>\n")
            f.write("  <ul>\n")

            for cls in self.classes:
                html_name = self.safe_filename(cls.name) + ".html"
                f.write(
                    f"    <li><a href=\"{html_name}\">{self.html_escape(cls.name)}</a></li>\n"
                )

            f.write("  </ul>\n")
            f.write("</body>\n")
            f.write("</html>\n")

        _write_css(os.path.join(self.output_dir, "cpp"))

    def write_classes(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "cpp" ), exist_ok=True)
        for cls in self.classes:
            filename = os.path.join(
                self.output_dir, "cpp",
                self.safe_filename(cls.name) + ".html")
            with open(filename, "w", encoding="utf-8") as f:
                f.write("<!DOCTYPE html>\n<html>\n<head>\n")
                f.write("  <meta charset=\"utf-8\">\n")
                f.write(f"  <title>{self.html_escape(cls.name)} Class</title>\n")
                f.write("  <link rel=\"stylesheet\" href=\"style.css\">\n")
                f.write("</head>\n<body>\n")

                f.write("  <main class=\"page\">\n")
                f.write(f"    <div class=\"version\">C++ Doc</div>\n")
                f.write(f"    <h1>{self.html_escape(cls.name)} Class</h1>\n")

                f.write("    <div class=\"breadcrumb\">\n")
                f.write("      <a href=\"index.html\">Overview</a>")
                f.write("      <span>›</span>")
                f.write(f"      <span>{self.html_escape(cls.name)}</span>\n")
                f.write("    </div>\n")

                if cls.bases:
                    f.write("    <p class=\"inherits\">Inherits: ")
                    f.write(", ".join(self.html_escape(b) for b in cls.bases))
                    f.write("</p>\n")

                self.write_member_table(f, share.locales.tr("Public Functions")     , cls.methods, "public")
                self.write_member_table(f, share.locales.tr("Protected Functions")  , cls.methods, "protected")
                self.write_member_table(f, share.locales.tr("Private Functions")    , cls.methods, "private")

                self.write_member_table(f, share.locales.tr("Public Fields")        , cls.fields, "public")
                self.write_member_table(f, share.locales.tr("Protected Fields")     , cls.fields, "protected")
                self.write_member_table(f, share.locales.tr("Private Fields")       , cls.fields, "private")
                
                
                f.write("    <section>\n")
                f.write("      <h2>Detailed Description</h2>\n")
                f.write(f"      <p>The <span class=\"linklike\">{self.html_escape(cls.name)}</span> class.</p>\n")
                f.write("    </section>\n")
                
                self.write_member_function_docs(f, cls)
                self.write_property_docs(f, cls)
                self.write_field_docs(f, cls)
                
                f.write("    <footer>\n")
                f.write("      Generated by <span>dBase Lexer + Parser</span> | C++ Documentation Generator\n")
                f.write("    </footer>\n")

                f.write("  </main>\n")
                f.write("</body>\n</html>\n")

    def write_member_function_docs(self, f, cls):
        if not cls.methods:
            return

        f.write("    <section class=\"member-docs\">\n")
        f.write("      <h2>Member Function Documentation</h2>\n")

        msg = share.locales.tr("No documentation for this member")
        for member in cls.methods:
            full_signature = self.make_qualified_signature(cls.name, member.signature)

            f.write("      <article class=\"member-doc\">\n")
            f.write(f"        <h3>{self.highlight_signature(full_signature)}</h3>\n")
            f.write("        <div class=\"member-line\"></div>\n")

            f.write("        <p>\n")
            f.write(f"          {msg}.\n")
            f.write("        </p>\n")

            f.write("      </article>\n")

        f.write("    </section>\n")


    def make_qualified_signature(self, class_name, signature):
        text = signature.strip()

        pos = text.find("(")
        if pos <= 0:
            return text

        before = text[:pos].strip()
        rest = text[pos:].strip()

        parts = before.rsplit(" ", 1)

        if len(parts) == 2:
            left = parts[0]
            name = parts[1]

            if name.startswith("~"):
                return f"{left} {class_name}::{name}{rest}"

            if name == class_name:
                return f"{class_name}::{name}{rest}"

            return f"{left} {class_name}::{name}{rest}"

        name = before

        if name.startswith("~"):
            return f"{class_name}::{name}{rest}"

        return f"{class_name}::{name}{rest}"
    
    def write_member_table(self, f, title, members, access_filter=None):
        items = []
        
        for member in members:
            if access_filter is None or member.access == access_filter:
                items.append(member)
        
        if not items:
            return
        
        f.write("    <section>\n")
        f.write(f"      <h2>{self.html_escape(title)}</h2>\n")
        f.write("      <table class=\"func-table\">\n")
        
        for member in items:
            left, right = self.split_signature(member.signature)
            anchor = self.make_member_anchor(self.current_output_class, member)
            
            f.write("        <tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(left)}</td>\n")
            f.write(
                f"          <td class=\"sig\">"
                f"<a class=\"member-link\" href=\"#{anchor}\">"
                f"{self.highlight_signature(right)}"
                f"</a></td>\n"
            )
            f.write("        </tr>\n")
            f.write(f"          <td class=\"ret\">{self.html_escape(left)}</td>\n")
            f.write(f"          <td class=\"sig\">{self.highlight_signature(right)}</td>\n")
            f.write("        </tr>\n")
        
        f.write("      </table>\n")
        f.write("    </section>\n")

    def split_signature(self, signature):
        text = self.pretty_cpp_text(signature)
        pos  = text.find("(")
        if pos > 0:
            before = text[:pos].strip()
            rest = text[pos:].strip()
            parts = before.rsplit(" ", 1)
            if len(parts) == 2:
                return parts[0], parts[1] + rest
            return "", text
        parts = text.rsplit(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return "", text

    def highlight_signature(self, signature):
        text = self.html_escape(signature)

        pos = text.find("(")
        if pos > 0:
            name = text[:pos]
            rest = text[pos:]
            return f"<span class=\"func-name\">{name}</span>{rest}"

        return f"<span class=\"func-name\">{text}</span>"


class DoxyScrollPage:
    def __init__(self, owner, area, widget, layout):
        self.owner  = owner
        self.area   = area
        self.widget = widget
        self.layout = layout


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
# \brief line number helper class for QPlainTextEdit.
# ---------------------------------------------------------------------------
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return self.editor.lineNumberAreaWidth(), 0
    
    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class DoxyCodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    # Breite des linken Randes berechnen
    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        space = 10 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.lightGray)
                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width() - 4,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor("#333333"))
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPushButton to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyButton(QPushButton):
    def __init__(self,
        owner             = None,
        help_str  : str   =   "",
        icon_norm : QIcon = None,
        icon_hovr : QIcon = None,
        flag      : int   =    0,
        mode      : int   =    0):
        
        super().__init__()
        
        self.help_str   = help_str
        self.owner      = owner
        self.flag       = flag
        self.mode       = mode
        self.filename   = ""
        
        self.config     = False
        
        self.icon_norm  = icon_norm
        self.icon_hovr  = icon_hovr
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
        
        self.setIconSize(QSize(22, 22))
        self.setProperty("help", self.help_str)
        
        self.setMaximumWidth (26)
        self.setMaximumHeight(26)
        
        self.clicked.connect(self.on_click)
        
        if self.icon_norm is not None:
            self.setIcon(self.icon_norm)
    
    def open_dir(self) -> str:
        self.filename = QFileDialog.getExistingDirectory(self,
            share.locales.tr("Select Directory"),
            "",
            QFileDialog.ShowDirsOnly)
        if not self.filename:
            return ""
        return self.filename
    
    def open_file(self) -> str:
        try:
            text = share.locales.tr("All Files")
            self.filename, _ = QFileDialog.getOpenFileName(
                self, share.locales.tr(share.locales.tr("Open File...")),
                "", f"{text} (*.*)")
            if self.filename:
                return self.filename
            return str("")
        except FileNotFoundError as e:
            msg = share.locales.tr("The requested file")
            txt = share.locales.tr("could not be found")
            fxt = share.locales.tr("File not found Error")
            
            dlg = ErrorMessage(ftxt, f"{msg}: {self.filename} {txt}.")
            dlg.exec_()
            return ""
        except PermissionError as e:
            msg = share.locales.tr("You have not enough permissions to open file")
            fxt = share.locales.tr("File Permission Error")
            
            dlg = ErrorMessage(ftxt, f"{msg}:\n{self.filename}.")
            dlg.exec_()
            return ""
        except RuntimeError as e:
            msg = share.locales.tr("Runtime Error")
            fxt = share.locales.tr("The Python Library throws a Runtime Error on opening file")
            
            dlg = ErrorMessage(msg, f"{fxt}:\n{self.filename}.")
            dlg.exec_()
            return ""
        except OSError as e:
            msg = share.locales.tr("Operation System Error")
            fxt = share.locales.tr("The System is not able to open file")
            
            dlg = ErrorMessage(msg, f"{fxt}:\n{self.filename}.")
            dlg.exec_()
            return ""
        except Exception as e:
            msg = share.locales.tr("Common Exception Error")
            fxt = share.locales.tr("Common Exception throwed during open file")
            
            dlg = ErrorMessage(msg, f"{fxt}:\n{self.filename}.")
            dlg.exec_()
            return ""
    
    def delete_current_line(self, edit):
        cursor = edit.textCursor()
        
        # 1-basierte Zeilennummer
        line_no = cursor.blockNumber() + 1
        
        text = edit.toPlainText()
        lines = text.splitlines()
        
        index = line_no - 1
        
        if 0 <= index < len(lines):
            removed_line = lines.pop(index)
            edit.setPlainText("\n".join(lines))
            
            # Cursor auf die neue Position setzen
            cursor = edit.textCursor()
            cursor.movePosition(cursor.Start)
            
            for _ in range(min(index, len(lines) - 1)):
                cursor.movePosition(cursor.Down)
            
            edit.setTextCursor(cursor)
            return line_no, removed_line

        return line_no, ""
    
    def on_click(self, b):
        found = False
        if self.owner is not None:
            if isinstance(self.owner, DoxyLineBtn1):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
            elif isinstance(self.owner, DoxyLineBtnA):
                if self.flag == 1:
                    if self.open_dir():
                        self.owner.input.input.setText(self.filename)
            elif isinstance(self.owner, DoxyLineBtn3):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
                elif self.flag == 2:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            trans = share.locales.tr(res)
                            page  = DOXYGEN_PROJECT_PAGES.get(trans)
                            item1 = page.area.findChild(DoxyTextEdit, self.help_str)
                            item2 = page.area.findChild(DoxyLineBtn3, self.help_str)
                            if (item1 is not None) and (item1.help_str == item2.help_str):
                                item1.edit.appendPlainText(item2.input.input.text())
                                break
                elif self.flag == 3:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            trans = share.locales.tr(res)
                            page  = DOXYGEN_PROJECT_PAGES.get(trans)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help_str)
                                if item is not None:
                                    line, text = self.delete_current_line(item.edit)
                                    self.owner.input.input.setText(text)
                                    break
            elif isinstance(self.owner, DoxyLineBtn4):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
                elif self.flag == 2:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            trans = share.locales.tr(res)
                            page  = DOXYGEN_PROJECT_PAGES.get(trans)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help_str)
                                if item is not None:
                                    text = self.owner.input.input.text().strip()
                                    item.edit.appendPlainText(text)
                                    break
                elif self.flag == 3:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            trans = share.locales.tr(res)
                            page  = DOXYGEN_PROJECT_PAGES.get(trans)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help_str)
                                if item is not None:
                                    line, text = self.delete_current_line(item.edit)
                                    self.owner.input.input.setText(text)
                                    break
                elif self.flag == 4:
                    text = self.owner.input.input.text().strip()
                    print("refresh:", text)
        else:
            QMessageBox.warning(self,
                share.locales.tr("No button binding"),
                share.locales.tr("The button have no binding component."))
    
    def enterEvent(self, event):
        if self.icon_hovr is not None:
            self.setIcon(self.icon_hovr)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if self.icon_norm is not None:
            self.setIcon(self.icon_norm)
        super().leaveEvent(event)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
class LinkLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        
        self.web_url = "https://www.doxygen.nl/manual/config.html#cfg_"
        self.hlp_txt = text.lower()
        self.web_url = f"{self.web_url}{self.hlp_txt}"
        
        self.setFont(QFont("Consolas", 10))
        self.setMinimumWidth(164)
        self.setStyleSheet("color: white;")
        self.setText(text)
        
        self.setCursor(Qt.PointingHandCursor)
        set_tooltip_if_text(self, self.web_url)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            QDesktopServices.openUrl(QUrl(self.web_url))
        super().mousePressEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyLabel(LinkLabel):
    def __init__(self,
        parent         = None,
        help_str : str =  "" ,
        flag     : int =  0 ):
        
        super().__init__(help_str, parent.owner)
        
        self.parent   = parent
        self.owner    = parent.owner
        self.help_str = help_str
        self.flag     = flag
        
        self.config   = False
        
        self.setObjectName(self.help_str)
       
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
        
        self.setProperty("help", self.help_str)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPlainTextEdit to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyTextEdit(QWidget):
    def __init__(self,
        parent          = None,
        help_str : str  =  "" ,
        text     : list =  []):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.edit   = DoxyCodeEditor()
        
        self.label  = DoxyLabel(self.parent, self.help_str)
        self.label.setStyleSheet("color: rgba(0,0,0,0);")
        
        self.edit.setProperty("help", self.help_str)
        self.edit.setProperty("text", self.text_str)
        self.edit.setProperty("link", self.link_str)
        
        self.edit.setStyleSheet("background-color: #303030;")
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        for line in text:
            self.edit.appendPlainText(line)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QCheckBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxyCheckBox(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str =  ""):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = ""
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.help_str, 1)
        self.check  = QCheckBox(share.locales.tr("NO"))
        
        self.label.setProperty("help", self.help_str)
        self.label.setProperty("text", self.help_str)
        self.label.setProperty("link", self.link_str)
        
        self.check.setProperty("help", self.help_str)
        #self.check.setProperty("text", self.text_str)
        self.check.setProperty("link", self.link_str)
            
        self.check.setStyleSheet("color: red;")
        self.check.toggled.connect(self.on_changed)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.check)
        self.layout.addStretch(1)
    
    def on_changed(self, checked):
        if checked:
            self.check.setText(share.locales.tr("YES"))
            self.check.setStyleSheet("color: yellow;")
        else:
            self.check.setText(share.locales.tr("NO"))
            self.check.setStyleSheet("color: red;")
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QSpinBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxySpinEdit(QWidget):
    def __init__(self ,
        parent       = None,
        help_str:str =   "",
        v_min : int  =    0,
        v_max : int  =  100,
        v_def : int  =   0):
            
        super().__init__(None)

        self.help_str = help_str
        self.text_str = ""
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.help_str, 1)
        self.spin   = QSpinBox()
        
        self.spin.setMinimum(v_min)
        self.spin.setMaximum(v_max)
        self.spin.setValue  (v_def)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.spin .setProperty("help", self.help_str)
        self.spin .setProperty("link", self.link_str)
        
        self.label.setProperty("help", self.help_str)
        self.label.setProperty("link", self.link_str)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin)
        self.layout.addStretch(1)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QLineEdit with a label
# \param parent   - QWidget as the parent
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the input content, default: "".
# ---------------------------------------------------------------------------
class DoxyLineEdit(QWidget):
    def __init__(self,
        parent=None,
        help_str : str = "",
        text_str : str = "",
        flag     : int = 0):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = flag
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.link_str)
        self.input  = QLineEdit()
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.input.setProperty("help", self.help_str)
        self.input.setProperty("text", self.text_str)
        self.input.setProperty("link", self.link_str)
        
        self.input.setFont(QFont("Consolas", 10))
        #self.input.setText(self.text_str)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLineEdit with a Button to reduce code.
# ---------------------------------------------------------------------------
class DoxyLineBtnA(QWidget):
    def __init__(self,
        parent   = None,
        help_str : str = "",
        text_str : str = "",
        flag     : int =  0):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.flag     = flag
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, self.help_str, self.text_str)
        
        self.input.setProperty("help", self.help_str)
        self.input.setProperty("text", self.text_str)
        self.input.setProperty("link", self.link_str)
        
        self.button = DoxyButton(
            self,
            self.help_str,
            QIcon(":/icons/doc.ico"),
            QIcon(":/icons/doc_hov.ico"), 1, 1)
        
        self.button.setProperty  ("help", self.help_str)
        self.button.setProperty  ("text", self.text_str)
        self.button.setProperty  ("link", self.link_str)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)

class DoxyLineBtn1(QWidget):
    def __init__(self,
        parent   = None,
        help_str : str = "",
        text_str : str = "",
        flag     : int =  0):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.flag     = flag
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, self.help_str, self.text_str)
        
        self.input.setProperty("help", self.help_str)
        self.input.setProperty("text", self.text_str)
        self.input.setProperty("link", self.link_str)
        
        self.button = DoxyButton(
            self,
            self.help_str,
            QIcon(":/icons/doc.ico"),
            QIcon(":/icons/doc_hov.ico"), 1, 1)
        
        self.button.setProperty  ("help", self.help_str)
        self.button.setProperty  ("text", self.text_str)
        self.button.setProperty  ("link", self.link_str)
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
            
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)

class DoxyLineBtn3(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str =  "" ,
        text_str : str =  ""):
            
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)

        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, self.help_str, self.text_str)
        
        self.layout.addWidget(self.input)
        
        self.butt1  = DoxyButton(self, self.help_str, QIcon(":/icons/add.ico"), QIcon(":/icons/add_hov.ico"), 2)
        self.butt2  = DoxyButton(self, self.help_str, QIcon(":/icons/sub.ico"), QIcon(":/icons/sub_hov.ico"), 3)
        self.butt3  = DoxyButton(self, self.help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        for item in [self.butt1, self.butt2, self.butt3]:
            item.setProperty("help", self.help_str)
            item.setProperty("text", self.text_str)
            item.setProperty("link", self.link_str)
            self.layout.addWidget(item)
            
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


class DoxyLineBtn4(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str = "",
        text_str : str = "",
        flag     : int = 0):
        
        super().__init__(None)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = flag
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(parent, self.help_str, self.text_str, 1)
        
        self.layout.addWidget(self.input)
        
        self.butt1  = DoxyButton(self, self.help_str, QIcon(":/icons/add.ico"), QIcon(":/icons/add_hov.ico"), 2)
        self.butt2  = DoxyButton(self, self.help_str, QIcon(":/icons/sub.ico"), QIcon(":/icons/sub_hov.ico"), 3)
        self.butt3  = DoxyButton(self, self.help_str, QIcon(":/icons/frs.ico"), QIcon(":/icons/frs_hov.ico"), 4)
        self.butt4  = DoxyButton(self, self.help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        for item in [self.butt1, self.butt2, self.butt3, self.butt3]:
            item.setProperty("help", self.help_str)
            item.setProperty("text", self.text_str)
            item.setProperty("link", self.link_str)
            self.layout.addWidget(item)
            
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel with a image to reduce code space.
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyImage(QWidget):
    def __init__(self,
        parent         = None,
        help_str : str =  "" ,
        text_str : str =  ""):
        
        super().__init__(parent.owner)
        
        self.setMinimumHeight(74)
        
        self.help_str = help_str
        self.text_str = text_str
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label2 = QLabel(self.text_str)
        
        self.label1 = DoxyLabel(self, self.help_str, 1)
        self.label1.setStyleSheet("color: rgba(0,0,0,0);")
        self.label2.setAlignment(Qt.AlignLeft)
        
        self.label2.setProperty("help", self.help_str)
        self.label2.setProperty("text", self.text_str)
        self.label2.setProperty("link", self.link_str)
        
        self.label2.setFont(QFont("Arial", 9))
        self.label2.setStyleSheet("color:yellow;")
        
        self.layout.addWidget(self.label1, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label2, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
class DoxyComboBox(QWidget):
    def __init__(self,
        parent          = None,
        help_str : str  =   "",
        items    : list =  []):
        
        super().__init__(parent.owner)
        
        self.help_str = help_str
        self.text_str = ""
        self.link_str = help_str
        
        self.config   = False
        
        self.setProperty("help", self.help_str)
        self.setProperty("text", self.text_str)
        self.setProperty("link", self.link_str)
        
        self.setObjectName(self.help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.flag   = 0
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, self.help_str)
        self.combo  = QComboBox()
        
        if help_str not in DOXYGEN_ITEMS:
            DOXYGEN_ITEMS.append(self)
        
        for item in items:
            self.combo.addItem(share.locales.tr(item))
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addStretch(1)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help_str)
        super().enterEvent(event)


class WizardSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.pages = [
            share.locales.tr("Project"),
            share.locales.tr("Mode"),
            share.locales.tr("Output"),
            share.locales.tr("Diagrams")
        ]
        
        self.list_view = QListView(self)
        self.model     = QStringListModel(self.pages, self)
        self.list_view.setModel(self.model)
        
        self.stack = QStackedWidget(self)
        
        self.stack.addWidget(self.create_page_project ("Project Page"))
        self.stack.addWidget(self.create_page_mode    ("Mode Page"))
        self.stack.addWidget(self.create_page_output  ("Output Page"))
        self.stack.addWidget(self.create_page_diagrams("Diagrams Page"))
        
        splitter = QSplitter(Qt.Horizontal, self)
        splitter.addWidget(self.list_view)
        splitter.addWidget(self.stack)
        splitter.setSizes([160, 500])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        
        self.list_view.clicked.connect(self.on_page_selected)
        self.list_view.setCurrentIndex(self.model.index(0, 0))
        self.stack.setCurrentIndex(0)
    
    def create_page_project(self, title):
        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)

        label = QLabel(share.locales.tr(
            "Provide some information about "
            "the project you are documenting"),
            page)
        content_layout.addWidget(label)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project name:"))
        label.setStyleSheet("color:white;weight:normal;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        content_layout.addLayout(hlay)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project synopsis:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        content_layout.addLayout(hlay)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project version or id:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        content_layout.addLayout(hlay)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Project logo:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        lbbtn = QPushButton(share.locales.tr("Select..."))
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        hlay.addWidget(lbbtn)
        content_layout.addLayout(hlay)
        
        skipper = QLabel("")
        skipper.resize(120, 22)
        content_layout.addWidget(skipper)
        
        label = QLabel(share.locales.tr("Specify the directory to scan for source code"))
        content_layout.addWidget(label)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Source code directory:"))
        label.setStyleSheet("color:white;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        lbbtn = QPushButton(share.locales.tr("Select..."))
        self.on_button_clicked(lbbtn, lined, 1)
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        hlay.addWidget(lbbtn)
        content_layout.addLayout(hlay)
        
        skipper = QWidget()
        skipper.resize(120, 22)
        content_layout.addWidget(skipper)
        
        hlay  = QHBoxLayout()
        label = QLabel(share.locales.tr("Destination directory:"))
        label.setStyleSheet("color:white;weight:normal;")
        label.setFont(QFont("Arial", 9))
        label.font().setBold(False)
        label.setMinimumWidth(130)
        lined = QLineEdit()
        lbbtn = QPushButton(share.locales.tr("Select..."))
        self.on_button_clicked(lbbtn, lined, 2)
        
        hlay.addWidget(label)
        hlay.addWidget(lined)
        hlay.addWidget(lbbtn)
        content_layout.addLayout(hlay)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        return page
        
    def on_button_clicked(self, btn, edit, mode=0):
        if mode == 1:
            self.button_src  = btn
            self.button_edit = edit
            btn.clicked.connect(self.on_button_clicked_src)
        elif mode == 2:
            self.button_dst  = btn
            self.button_edit = edit
            btn.clicked.connect(self.on_button_clicked_dst)
    
    def on_button_clicked_src(self):
        print("src")
        
    def on_button_clicked_dst(self):
        print("dst")
        
    def create_page_mode(self, title):
        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)

        group1 = QGroupBox(share.locales.tr("Select the desired extraction mode"), content)
        group2 = QGroupBox(share.locales.tr("Select programming language to optimize the result for"), content)
        
        group1_layout = QVBoxLayout(group1)
        group2_layout = QVBoxLayout(group2)
        
        group1_layout.setContentsMargins(4,4,4,4)
        group2_layout.setContentsMargins(4,4,4,4)
        
        group1_layout.setSpacing(4)
        group2_layout.setSpacing(4)
        
        g1rbt1 = QRadioButton(share.locales.tr("Documented entities only"))
        g1rbt2 = QRadioButton(share.locales.tr("All Entities"))
        g1chk1 = QCheckBox   (share.locales.tr("Include cross-referenced source code"))
        
        group1_layout.addWidget(g1rbt1)
        group1_layout.addWidget(g1rbt2)
        group1_layout.addWidget(g1chk1)
        
        txt1   = share.locales.tr("Optimize for")
        txt2   = share.locales.tr("output")
        
        font   = QFont("Consolas", 10)
        self.setStyleSheet("""
        QRadioButton {
            font-family: "Consolas";
            font-size: 10pt;
        }
        """)
        g2rbt1 = QRadioButton(f"{txt1} C++        {txt2}")
        g2rbt2 = QRadioButton(f"{txt1} C++ CLI    {txt2}")
        g2rbt3 = QRadioButton(f"{txt1} Java or C# {txt2}")
        g2rbt4 = QRadioButton(f"{txt1} C or PHP   {txt2}")
        g2rbt5 = QRadioButton(f"{txt1} Fortan     {txt2}")
        g2rbt6 = QRadioButton(f"{txt1} VHDL       {txt2}")
        g2rbt7 = QRadioButton(f"{txt1} SLICE      {txt2}")
        
        for item in [g2rbt1, g2rbt2, g2rbt3, g2rbt4, g2rbt5, g2rbt6, g2rbt7]:
            item.setFont(QFont("Consolas", 1))
            group2_layout.addWidget(item)
        
        content_layout.addWidget(group1)
        content_layout.addWidget(group2)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        
        return page
    
    def create_page_output(self, title):
        page = QWidget(self)
        page.setFont(QFont("Arial", 10))
        
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setFont(QFont("Arial", 10))
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content.setFont(QFont("Arial", 10))
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)

        label = QLabel(share.locales.tr("Select the output format(s) to generate"), page)
        content_layout.addWidget(label)
        
        group1 = QGroupBox(share.locales.tr("HTML" ), content)
        group2 = QGroupBox(share.locales.tr("LaTeX"), content)
        
        group1.setCheckable(True)
        group1.setChecked(True)
        
        group2.setCheckable(True)
        group2.setChecked(True)
        
        group1.toggled.connect(lambda checked: self.set_group_content_enabled(group1, checked))
        group2.toggled.connect(lambda checked: self.set_group_content_enabled(group2, checked))
        
        group1_layout = QVBoxLayout(group1)
        group2_layout = QVBoxLayout(group2)
        
        group1_layout.setContentsMargins(4,4,4,4)
        group2_layout.setContentsMargins(4,4,4,4)
        
        group1_layout.setSpacing(4)
        group2_layout.setSpacing(4)
        
        g1btn1 = QRadioButton(share.locales.tr("plain HTML"))
        g1btn2 = QRadioButton(share.locales.tr("with navigation panel"))
        g1btn3 = QRadioButton(share.locales.tr("prepare for compressed HTML (.chm)"))
        chkbox = QCheckBox   (share.locales.tr("with search function"))
        
        for item in [g1btn1, g1btn1, g1btn2, g1btn3, chkbox]:
            group1_layout.addWidget(item)
            
        txtmsg = share.locales.tr("as intermediate format")
        g2btn1 = QRadioButton(f"{txtmsg} hyperlinked PDF")
        g2btn2 = QRadioButton(f"{txtmsg} PDF")
        g2btn3 = QRadioButton(f"{txtmsg} PostSctipt")
        
        group2_layout.addWidget(g2btn1)
        group2_layout.addWidget(g2btn2)
        group2_layout.addWidget(g2btn3)
        
        content_layout.addWidget(group1)
        content_layout.addWidget(group2)
        
        chk1 = QCheckBox(share.locales.tr("Man page"))
        chk2 = QCheckBox(share.locales.tr("Richt Text Format (RTF)"))
        chk3 = QCheckBox(share.locales.tr("XML"))
        chk4 = QCheckBox(share.locales.tr("Docbook"))
        
        for item in [chk1, chk2, chk3, chk4]:
            content_layout.addWidget(item)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        
        return page
    
    def create_page_diagrams(self, title):
        page = QWidget(self)
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0,0,0,0)
        
        scroll = QScrollArea(page)
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4,4,4,4)
        content_layout.setSpacing(4)
        
        group1 = QGroupBox(share.locales.tr("Diagrams to generate" ), content)
        group2 = QGroupBox(share.locales.tr("Dot graphs to generate"), content)

        group1_layout = QVBoxLayout(group1)
        group2_layout = QVBoxLayout(group2)
        
        group1_layout.setContentsMargins(4,4,4,4)
        group2_layout.setContentsMargins(4,4,4,4)
        
        group1_layout.setSpacing(4)
        group2_layout.setSpacing(4)
        
        radio1 = QRadioButton(share.locales.tr("No diagrams"))
        radio2 = QRadioButton(share.locales.tr("Text only"))
        radio3 = QRadioButton(share.locales.tr("Use built-in class diagram generator"))
        radio4 = QRadioButton(share.locales.tr("Use dot tool from the GraphWiz package"))
        
        for item in [radio1, radio2, radio3, radio4]:
            group1_layout.addWidget(item)
        
        check1 = QCheckBox(share.locales.tr("Class graphs"))
        check2 = QCheckBox(share.locales.tr("Collaboration Class Hierarchy"))
        check3 = QCheckBox(share.locales.tr("Overall Class Hierarchy"))
        check4 = QCheckBox(share.locales.tr("Include dependency graphs"))
        check5 = QCheckBox(share.locales.tr("Included by dependency graphs"))
        check6 = QCheckBox(share.locales.tr("Call Graphs"))
        check7 = QCheckBox(share.locales.tr("Called by graphs"))
        
        for item in [check1, check2, check3, check4, check5, check6, check7]:
            group2_layout.addWidget(item)
        
        content_layout.addWidget(group1)
        content_layout.addWidget(group2)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        page_layout.addWidget(scroll)
        
        lbl_layout = QHBoxLayout()
        btn_prev   = QPushButton(share.locales.tr("Prev"))
        btn_next   = QPushButton(share.locales.tr("Next"))
        
        lbl_layout.addWidget(btn_prev)
        lbl_layout.addStretch()
        lbl_layout.addWidget(btn_next)
        
        page_layout.addLayout(lbl_layout)
        
        return page

    def on_page_selected(self, index):
        self.stack.setCurrentIndex(index.row())
    
    def set_group_content_enabled(self, group, checked):
        for child in group.findChildren(QWidget):
            child.setEnabled(checked)

# ---------------------------------------------------------------------------
# \brief this is the doxygen tool window for help / documenting the source.
# ---------------------------------------------------------------------------
class DoxyGenToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        global DOXYGEN_WINDOW
        DOXYGEN_WINDOW   = self
        
        self.owner       = self
        self.config      = {}
        self.state       = {}
        
        self.project_dir = _default_project_dir()
        self.propath     = self.project_dir / "doxygen_project.json"
        self.visitor     = None
        
        self.current_project_path = ""

        #self.lang = share.locales.get_default_lang().split("_")[0].lower()
        #self.trmo = share.locales.load_mo_from_resource(f":/locales/{self.lang}/doxygen.mo")
            
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
        
        self.btn_save  .clicked.connect(self.save_project_as)
        self.btn_delete.clicked.connect(self._delete_selected_project)
        self.btn_load  .clicked.connect(self._load_selected_project)
        
        self.main_splitter.addWidget(self.left_host)
        
        self.right_host = QWidget()
        right_lay = QVBoxLayout(self.right_host)
        right_lay.setContentsMargins(0, 0, 0, 0)
        
        hlay = QHBoxLayout()
        self.lineCWD = QLineEdit()
        self.btn_CWD = QPushButton(share.locales.tr("Select"))
        self.txt_CWD = QLabel(share.locales.tr("Specify the working directory from which doxygen will run"))
        
        self.lineCWD.setFont(QFont("Consolas", 9))
        self.lineCWD.setText(str(_default_project_dir()))
        
        self.btn_CWD.clicked.connect(self.on_cwd_click)
        
        hlay.addWidget(self.lineCWD)
        hlay.addWidget(self.btn_CWD)
        
        right_lay.addWidget(self.txt_CWD)
        right_lay.addLayout(hlay)
        
        self.tabs = QTabWidget()
        right_lay.addWidget(self.tabs)
        
        self.main_splitter.addWidget(self.right_host)
        self.main_splitter.setSizes([260, 940])
        
        
        self.tabs.addTab(self._build_wizard_tab(), share.locales.tr("Wizard"))
        self.tabs.addTab(self._build_expert_tab(), share.locales.tr("Expert"))
        self.tabs.addTab(self._build_run_tab   (), share.locales.tr("Run"))

    def generate_html(self, source_file, output_dir="html"):
        name, ext = os.path.splitext(source_file)
        ext       = ext[1:].lower()
        try:
            if ext in ["pas", "pp"]:
                self.progress = DoxyProgressDialog(self)
                self.progress.show()
                self.progress.log(share.locales.tr("Start documentation generation..."))
                self.progress.setValue(1)
                
                self.input_stream = FileStream(source_file, encoding="utf-8")
                self.lexer   = PasDocLexer      (self.input_stream)
                self.tokens  = CommonTokenStream(self.lexer)
            
                self.parser  = PasDocParser(self.tokens)
                self.tree    = self.parser.unitFile()
            
                self.visitor = PasDocHtmlVisitor(
                    output_dir,
                    use_treeview = True,
                    progress     = self.progress
                )
                self.visitor.visit(self.tree)
                
            elif ext in ["c", "c++", "cc", "cpp"]:
                output_dir.join("/cpp")
                
                self.input_stream = FileStream(source_file, encoding="utf-8")
                self.lexer   = CppDocLexer(self.input_stream)
                self.tokens  = CommonTokenStream(self.lexer)
            
                self.parser  = CppDocParser(self.tokens)
                self.tree    = parser.translationUnit()
            
                self.visitor = CppDocHtmlVisitor(output_dir)
                self.visitor.visit(tree)
                
        except Exception as e:
            traceback.print_exc()
            return
        
        self.progress.log(share.locales.tr("HTML created in") + ": " + output_dir)

    def on_cwd_click(self):
        file_name = share.drives.open_share_file_dialog(self)
        print(file_name)
        self.generate_html(file_name, "html")
        
    def _build_wizard_tab(self):
        page = WizardSettings()
        return page

    def _create_scroll_page(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_owner  = self
        scroll_widget = QWidget()
        
        scroll_lay    = QVBoxLayout(scroll_widget)
        scroll_lay.setContentsMargins(2, 2, 2, 2)
        scroll_lay.setSpacing(2)

        scroll_area.setWidget(scroll_widget)

        return scroll_owner, scroll_area, scroll_widget, scroll_lay
    
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
            self.list_categories.addItem(share.locales.tr(item))
        
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)
        
        # -----------------------------------------------------------
        self.expert_pages = QStackedWidget()
        self.expert_splitter_h.addWidget(self.expert_pages)
        
        for name in DOXYGEN_EXPERT_ITEMS:
            scroll_owner, scroll_area, scroll_widget, scroll_lay = self._create_scroll_page()
            DOXYGEN_PROJECT_PAGES[share.locales.tr(str(name))] = DoxyScrollPage(
                scroll_owner,
                scroll_area,
                scroll_widget,
                scroll_lay
            )
            self.expert_pages.addWidget(scroll_area)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_lay = QVBoxLayout(self.expert_pages)
        self.scroll_lay.setContentsMargins(2, 2, 2, 2)
        self.scroll_lay.setSpacing(2)
        
        # -------------------------------------------------------------------------
        self.par1 = DOXYGEN_PROJECT_PAGES[share.locales.tr("Project")]
        self.project_items = [
            DoxyLineEdit (self.par1, "DOXYFILE_ENCODING", "UTF-8"),
            
            DoxyLineEdit(self.par1, "PROJECT_NAME", share.locales.tr("MyProject")),
            DoxyLineEdit(self.par1, "PROJECT_NUMBER"),
            DoxyLineEdit(self.par1, "PROJECT_BRIEF", [
                "\"The $name class\"",
                "\"The $name widget\"",
                "\"The $name file\"",
                "is",
                "provides",
                "specifies",
                "contains",
                "represents",
                "a",
                "an",
                "the",
            ]),
            DoxyLineBtn1(self.par1, "PROJECT_LOGO", "", 0),
            DoxyImage   (self.par1, "PROJECT_LOGO", share.locales.tr("No Project Logo selected.")),
            DoxyLineBtn1(self.par1, "PROJECT_ICON", "", 0),
            DoxyImage   (self.par1, "PROJECT_ICON", share.locales.tr("No Project Icon selected.")),
            
            DoxyLineBtnA(self.par1, "OUTPUT_DIRECTORY", "", 1),
            DoxyCheckBox(self.par1, "CREATE_SUBDIRS"),
            DoxySpinEdit(self.par1, "CREATE_SUBDIRS_LEVEL", 0, 64, 4),
            
            DoxyCheckBox(self.par1, "ALLOW_UNICODE_NAMES"),
            DoxyComboBox(self.par1, "OUTPUT_LANGUAGE", SUPPORTED_LANGUAGES),
            
            DoxyCheckBox(self.par1, "BRIEF_MEMBER_DESC"),
            DoxyCheckBox(self.par1, "REPEAT_BRIEF"),
            
            DoxyLineBtn3(self.par1, "ABBREVIATE_BRIEF"),
            DoxyTextEdit(self.par1, "ABBREVIATE_BRIEF", []),
            
            DoxyCheckBox(self.par1, "ALWAYS_DETAILED_SEC"),
            DoxyCheckBox(self.par1, "INLINE_INHERITED_MEMB"),
            
            DoxyCheckBox(self.par1, "FULL_PATH_NAMES"),
            
            DoxyLineBtn4(self.par1, "STRIP_FROM_PATH"),
            DoxyTextEdit(self.par1, "STRIP_FROM_PATH", []),
            
            DoxyLineBtn4(self.par1, "STRIP_FROM_INC_PATH"),
            DoxyTextEdit(self.par1, "STRIP_FROM_INC_PATH", []),
            
            DoxyCheckBox(self.par1, "SHORT_NAMES"),
            
            DoxyCheckBox(self.par1, "JAVADOC_AUTOBRIEF"),
            DoxyCheckBox(self.par1, "JAVADOC_BANNER"),
            
            DoxyCheckBox(self.par1, "QT_AUTOBRIEF"),
            DoxyCheckBox(self.par1, "PYTHON_DOCSTRING"),
            DoxyCheckBox(self.par1, "INHERIT_DOCS"),
            
            DoxyCheckBox(self.par1, "SEPARATE_MEMBER_PAGES"),
            DoxySpinEdit(self.par1, "TAB_SIZE", 2, 16, 2),
            
            DoxyLineBtn3(self.par1, "ALIASES"),
            DoxyTextEdit(self.par1, "ALIASES", []),
            
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_C"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_JAVA"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_FORTRAN"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_VHDL"),
            DoxyCheckBox(self.par1, "OPTIMIZE_OUTPUT_SLICE"),
            
            DoxyLineBtn3(self.par1, "EXTENSION_MAPPING"),
            DoxyTextEdit(self.par1, "EXTENSION_MAPPING", []),
            
            DoxyCheckBox(self.par1, "MARKDOWN_SUPPORT"),
            DoxyCheckBox(self.par1, "MARKDOWN_STRICT"),
            DoxyComboBox(self.par1, "MARKDOWN_ID_STYLE", ["DOXYGEN", "GITHUB"]),
            
            DoxySpinEdit(self.par1, "TOC_INCLUDE_HEADINGS"),
            
            DoxyCheckBox(self.par1, "AUTOLINK_SUPPORT"),
            DoxyLineBtn3(self.par1, "AUTOLINK_IGNORE_WORDS"),
            DoxyTextEdit(self.par1, "AUTOLINK_IGNORE_WORDS", []),
            
            DoxyCheckBox(self.par1, "BUILTIN_STL_SUPPORT"),
            DoxyCheckBox(self.par1, "CPP_CLI_SUPPORT"),
            DoxyCheckBox(self.par1, "SIP_SUPPORT"),
            DoxyCheckBox(self.par1, "IDL_PROPERTY_SUPPORT"),
            DoxyCheckBox(self.par1, "DISTRIBUTE_GROUP_DOC"),
            DoxyCheckBox(self.par1, "GROUP_NESTED_COMPOUNDS"),
            
            DoxyCheckBox(self.par1, "SUBGROUPING"),
            DoxyCheckBox(self.par1, "INLINE_GROUPED_CLASSES"),
            DoxyCheckBox(self.par1, "INLINE_SIMPLE_STRUCTS"),
            
            DoxyCheckBox(self.par1, "TYPEDEF_HIDES_STRUCT"),
            DoxySpinEdit(self.par1, "LOOKUP_CACHE_SIZE"),
            
            DoxySpinEdit(self.par1, "NUM_PROC_THREADS"),
            DoxyComboBox(self.par1, "TIMESTAMP", ["YES", "NO", "DATETIME", "DATE"]),
        ]
        project_lay = DOXYGEN_PROJECT_PAGES[share.locales.tr("Project")].layout
        for item in self.project_items:
            project_lay.addWidget(item)
        project_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par2 = DOXYGEN_PROJECT_PAGES["Build"]
        self.build_items = [
            DoxyCheckBox(self.par2, "EXTRACT_ALL"),
            DoxyCheckBox(self.par2, "EXTRACT_PRIVATE"),
            DoxyCheckBox(self.par2, "EXTRACT_PRIV_VIRTUAL"),
            DoxyCheckBox(self.par2, "EXTRACT_PACKAGE"),
            DoxyCheckBox(self.par2, "EXTRACT_STATIC"),
            
            DoxyCheckBox(self.par2, "EXTRACT_LOCAL_CLASSES"),
            DoxyCheckBox(self.par2, "EXTRACT_LOCAL_METHODS"),
            
            DoxyCheckBox(self.par2, "EXTRACT_ANON_NSPACES"),
            DoxyCheckBox(self.par2, "RESOLVE_UNNAMED_PARAMS"),
            
            DoxyCheckBox(self.par2, "HIDE_UNDOC_MEMBERS"),
            DoxyCheckBox(self.par2, "HIDE_UNDOC_CLASSES"),
            DoxyCheckBox(self.par2, "HIDE_UNDOC_NAMESPACES"),
            
            DoxyCheckBox(self.par2, "HIDE_FRIEND_COMPOUNDS"),
            DoxyCheckBox(self.par2, "HIDE_IN_BODY_DOCS"),
            
            DoxyCheckBox(self.par2, "INTERNAL_DOCS"),
            DoxyComboBox(self.par2, "CASE_SENSE_NAMES", [
                "SYSTEM",
                "YES",
                "NO"
            ]),
            
            DoxyCheckBox(self.par2, "HIDE_UNDOC_MEMBERS"),
            DoxyCheckBox(self.par2, "HIDE_SCOPE_NAMES"),
            DoxyCheckBox(self.par2, "HIDE_COMPOUND_REFERENCE"),
            
            DoxyCheckBox(self.par2, "SHOW_HEADERFILE"),
            DoxyCheckBox(self.par2, "SHOW_INCLUDE_FILES"),
            
            DoxyCheckBox(self.par2, "FORCE_LOCAL_INCLUDES"),
            DoxyCheckBox(self.par2, "INLINE_INFO"),
            
            DoxyCheckBox(self.par2, "SORT_MEMBER_DOCS"),
            DoxyCheckBox(self.par2, "SORT_BRIEF_DOCS"),
            DoxyCheckBox(self.par2, "SORT_MEMBER_CTORS_1ST"),
            DoxyCheckBox(self.par2, "SORT_GROUP_NAMES"),
            DoxyCheckBox(self.par2, "SORT_BY_SCOPE_NAME"),
            
            DoxyCheckBox(self.par2, "STRICT_PROTO_MATCHING"),
            
            DoxyCheckBox(self.par2, "GENERATE_TODOLIST"),
            DoxyCheckBox(self.par2, "GENERATE_TESTLIST"),
            DoxyCheckBox(self.par2, "GENERATE_BUGLIST"),
            DoxyCheckBox(self.par2, "GENERATE_DEPRECATEDLIST"),
            DoxyCheckBox(self.par2, "GENERATE_REQUIREMENTS"),
            
            DoxyComboBox(self.par2, "REQ_TRACEABILITY_INFO", [
                "YES",
                "NO",
                "UNSATISFIED_ONLY",
                "UNVERIFIED_ONLY"
            ]),
            
            DoxyLineBtn3(self.par2, "ENABLED_SECTIONS"),
            DoxyTextEdit(self.par2, "ENABLED_SECTIONS", []),
            
            DoxySpinEdit(self.par2, "MAX_INITIALIZER_LINES"),
            
            DoxyCheckBox(self.par2, "SHOW_USED_FILES"),
            DoxyCheckBox(self.par2, "SHOW_FILES"),
            DoxyCheckBox(self.par2, "SHOW_NAMESPACES"),
            
            DoxyLineBtn1(self.par2, "FILE_VERSION_FILTER"),
            DoxyLineBtn1(self.par2, "LAYOUT_FILE"),
            DoxyLineBtn4(self.par2, "CITE_BIB_FILES"),
            DoxyTextEdit(self.par2, "CITE_BIB_FILES", []),
            
            DoxyLineBtn4(self.par2, "EXTERNAL_TOOL_PATH"),
            DoxyTextEdit(self.par2, "EXTERNAL_TOOL_PATH", [])
        ]
        build_lay = DOXYGEN_PROJECT_PAGES["Build"].layout
        for item in self.build_items:
            build_lay.addWidget(item)
        build_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par3 = DOXYGEN_PROJECT_PAGES["Messages"]
        #self.par3 = self.par3.owner
        self.messages_items = [
            DoxyCheckBox(self.par3, "QUIET"),
            DoxyCheckBox(self.par3, "WARNINGS"),
            DoxyCheckBox(self.par3, "WARN_IF_UNDOCUMENTED"),
            DoxyCheckBox(self.par3, "WARN_IF_DOC_ERROR"),
            DoxyCheckBox(self.par3, "WARN_IF_INCOMPLETE_DOC"),
            DoxyCheckBox(self.par3, "WARN_NO_PARAMDOC"),
            DoxyCheckBox(self.par3, "WARN_IF_UNDOC_ENUM_VAL"),
            DoxyCheckBox(self.par3, "WARN_LAYOUT_FILE"),
            DoxyComboBox(self.par3, "WARN_AS_ERROR", [
                "NO",
                "YES",
                "FAIL_ON_WARNINGS",
                "FAIL_ON_WARNINGS_PRINT"]),
            DoxyLineEdit(self.par3, "WARN_FORMAT", ["$file:$line: $text"]),
            DoxyLineEdit(self.par3, "WARN_LINE_FORMAT", ["at line $line of file $file"]),
            DoxyLineBtn1(self.par3, "WARN_LOGFILE"),
        ]
        messages_lay = DOXYGEN_PROJECT_PAGES["Messages"].layout
        for item in self.messages_items:
            messages_lay.addWidget(item)
        messages_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par4 = DOXYGEN_PROJECT_PAGES["Input"]
        #self.par4.owner
        self.input_items = [
            DoxyLineBtn4(self.par4, "INPUT"),
            DoxyTextEdit(self.par4, "INPUT", []),
            DoxyLineEdit(self.par4, "INPUT_ENCODING", "UTF-8"),
            DoxyLineBtn3(self.par4, "INPUT_FILE_ENCODING"),
            DoxyTextEdit(self.par4, "INPUT_FILE_ENCODING", []),
            
            DoxyLineBtn3(self.par4, "FILE_PATTERNS"),
            DoxyTextEdit(self.par4, "FILE_PATTERNS", [
                "*.c",
                "*.cc",
                "*.cxx",
                "*.cxxm",
                "*.cpp",
                "*.cppm",
                "*.ccm",
                "*.c++",
                "*.c++m",
                "*.java",
                "*.ii",
                "*.ixx",
                "*.ipp",
                "*.i++",
                "*.inl",
                "*.idl",
                "*.ddl",
                "*.odl",
                "*.h",
                "*.hh",
                "*.hxx",
                "*.hpp",
                "*.h++",
                "*.l",
                "*.cs",
                "*.d",
                "*.php",
                "*.php4",
                "*.php5",
                "*.phtml",
                "*.inc",
                "*.m",
                "*.markdown",
                "*.md",
                "*.mm",
                "*.dox",
                "*.py",
                "*.pyw",
                "*.f90",
                "*.f95",
                "*.f03",
                "*.f08",
                "*.f18",
                "*.f",
                "*.for",
                "*.vhd",
                "*.vhdl",
                "*.ucf",
                "*.qsf",
                "*.ice",
            ]),
            
            DoxyCheckBox(self.par4, "RECURSIVE"),
            
            DoxyLineBtn4(self.par4, "EXCLUDE"),
            DoxyTextEdit(self.par4, "EXCLUDE", []),
            
            DoxyLineBtn3(self.par4, "EXCLUDE_PATTERNS"),
            DoxyTextEdit(self.par4, "EXCLUDE_PATTERNS", []),
            DoxyLineBtn3(self.par4, "EXCLUDE_SYMBOLS"),
            DoxyTextEdit(self.par4, "EXCLUDE_SYMBOLS", []),
            
            DoxyLineBtn4(self.par4, "EXAMPLE_PATH"),
            DoxyTextEdit(self.par4, "EXAMPLE_PATH", []),
            DoxyLineBtn3(self.par4, "EXAMPLE_PATTERNS"),
            DoxyTextEdit(self.par4, "EXAMPLE_PATTERNS", ["*"]),
            DoxyCheckBox(self.par4, "EXAMPLE_RECURSIVE"),
            
            DoxyLineBtn4(self.par4, "IMAGE_PATH"),
            DoxyTextEdit(self.par4, "IMAGE_PATH", []),
            
            DoxyLineBtn1(self.par4, "INPUT_FILTER"),
            
            DoxyLineBtn3(self.par4, "FILTER_PATTERNS"),
            DoxyTextEdit(self.par4, "FILTER_PATTERNS", []),
            
            DoxyCheckBox(self.par4, "FILTER_SOURCE_FILES"),
            DoxyLineBtn3(self.par4, "FILTER_SOURCE_PATTERNS"),
            DoxyTextEdit(self.par4, "FILTER_SOURCE_PATTERNS", []),
            
            DoxyLineEdit(self.par4, "USE_MDFILE_AS_MAINPAGE"),
            
            DoxyCheckBox(self.par4, "IMPLICIT_DIR_DOCS"),
            DoxySpinEdit(self.par4, "FORTRAN_COMMENT_AFTER", 0, 128, 72)
        ]
        input_lay = DOXYGEN_PROJECT_PAGES["Input"].layout
        for item in self.input_items:
            input_lay.addWidget(item)
        input_lay.addStretch()

        # -------------------------------------------------------------------------
        self.par5 = DOXYGEN_PROJECT_PAGES["Source Browser"]
        self.browser_items = [
            DoxyCheckBox(self.par5, "SOURCE_BROWSER"),
            DoxyCheckBox(self.par5, "INLINE_SOURCES"),
            DoxyCheckBox(self.par5, "STRIP_CODE_COMMENTS"),
            
            DoxyCheckBox(self.par5, "REFERENCED_BY_RELATION"),
            DoxyCheckBox(self.par5, "REFERENCES_RELATION"),
            DoxyCheckBox(self.par5, "REFERENCES_LINK_SOURCE"),
            
            DoxyCheckBox(self.par5, "SOURCE_TOOLTIPS"),
            DoxyCheckBox(self.par5, "USE_HTAGS"),
            DoxyCheckBox(self.par5, "VERBATIM_HEADERS"),
            
            DoxyCheckBox(self.par5, "CLANG_ASSISTED_PARSING"),
            DoxyCheckBox(self.par5, "CLANG_ADD_INC_PATHS"),
            DoxyLineBtn3(self.par5, "CLANG_OPTIONS"),
            DoxyTextEdit(self.par5, "CLANG_OPTIONS", []),
            DoxyLineBtn1(self.par5, "CLANG_DATABASE_PATH")
        ]
        browser_lay = DOXYGEN_PROJECT_PAGES["Source Browser"].layout
        for item in self.browser_items:
            browser_lay.addWidget(item)
        browser_lay.addStretch()

        # -------------------------------------------------------------------------
        self.par6 = DOXYGEN_PROJECT_PAGES["Index"]
        self.index_items = [
            DoxyCheckBox(self.par6, "ALPHABETICAL_INDEX"),
            DoxyLineBtn3(self.par6, "IGNORE_PREFIX"),
            DoxyTextEdit(self.par6, "IGNORE_PREFIX", [])
        ]
        index_lay = DOXYGEN_PROJECT_PAGES["Index"].layout
        for item in self.index_items:
            index_lay.addWidget(item)
        index_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par7 = DOXYGEN_PROJECT_PAGES["HTML"]
        self.html_items = [
            DoxyCheckBox(self.par7, "GENERATE_HTML"),
            DoxyLineBtnA(self.par7, "HTML_OUTPUT", "", 1),
            DoxyLineEdit(self.par7, "HTML_FILE_EXTENSION"),
            
            DoxyLineBtn1(self.par7, "HTML_HEADER"),
            DoxyLineBtn1(self.par7, "HTML_FOOTER"),
            
            DoxyLineBtn1(self.par7, "HTML_STYLESHEET"),
            DoxyLineBtn4(self.par7, "HTML_EXTRA_STYLESHEET"),
            DoxyTextEdit(self.par7, "HTML_EXTRA_STYLESHEET", []),
            DoxyLineBtn4(self.par7, "HTML_EXTRA_FILES"),
            DoxyTextEdit(self.par7, "HTML_EXTRA_FILES", []),
            
            DoxyComboBox(self.par7, "HTML_COLORSTYLE", [
                "LIGHT",
                "DARK",
                "AUTO_LIGHT",
                "AUTP_DARK",
                "TOGGLE"
            ]),
            
            DoxySpinEdit(self.par7, "HTML_COLOR_STYLE_HUE"  , 0, 255, 220),
            DoxySpinEdit(self.par7, "HTML_COLOR_STYLE_SAT"  , 0, 255, 100),
            DoxySpinEdit(self.par7, "HTML_COLOR_STYLE_GAMMA", 0, 255,  80),
            
            DoxyCheckBox(self.par7, "HTML_DYNAMIC_MENUS"),
            DoxyCheckBox(self.par7, "HTML_DYNAMIC_SECTIONS"),
            
            DoxyCheckBox(self.par7, "HTML_CODE_FOLDING"),
            DoxyCheckBox(self.par7, "HTML_COPY_CLIPBOARD"),
            DoxyLineEdit(self.par7, "HTML_PROJECT_COOKIE"),
            DoxySpinEdit(self.par7, "HTML_INDEX_NUM_ENTRIES", 0, 255, 100),
            
            DoxyCheckBox(self.par7, "GENERATE_DOCSET"),
            DoxyLineEdit(self.par7, "DOCSET_FEEDNAME"),
            DoxyLineEdit(self.par7, "DOCSET_FEEDURL"),
            DoxyLineEdit(self.par7, "DOCSET_BUNDLE_ID"),
            DoxyLineEdit(self.par7, "DOCSET_PUBLISHER_ID"),
            DoxyLineEdit(self.par7, "DOCSET_PUBLISHER_NAME"),
            
            DoxyCheckBox(self.par7, "GENERATE_HTMLHELP"),
            DoxyLineBtn1(self.par7, "CHM_FILE"),
            DoxyLineBtnA(self.par7, "HHC_LOCATION", "", 1),
            
            DoxyCheckBox(self.par7, "GENERATE_CHI"),
            DoxyLineEdit(self.par7, "CHM_INDEX_ENCODING"),
            DoxyCheckBox(self.par7, "BINARY_TOC"),
            DoxyCheckBox(self.par7, "TOC_EXPAND"),
            DoxyLineEdit(self.par7, "SITEMAP_URL"),
            
            DoxyCheckBox(self.par7, "GENERATE_QHP"),
            DoxyLineBtn1(self.par7, "QCH_FILE"),
            
            DoxyLineEdit(self.par7, "QHP_NAMESPACE"),
            DoxyLineEdit(self.par7, "QHP_VIRTUAL_FOLDER"),
            DoxyLineEdit(self.par7, "QHP_CUST_FILTER_NAME"),
            DoxyLineEdit(self.par7, "QHP_CUST_FILTER_ATTRS"),
            DoxyLineEdit(self.par7, "QHP_SECT_FILTER_ATTRS"),
            
            DoxyLineBtnA(self.par7, "QHG_LOCATION", "", 1),
            
            DoxyCheckBox(self.par7, "GENERATE_ECLIPSE_HELP"),
            DoxyLineEdit(self.par7, "ECLIPSE_DOC_ID"),
            DoxyCheckBox(self.par7, "DISABLE_INDEX"),
            
            DoxyCheckBox(self.par7, "GENERATE_TREEVIEW"),
            DoxyCheckBox(self.par7, "PAGE_OUTLINE_PANEL"),
            DoxyCheckBox(self.par7, "FULL_SIDEBAR"),
            
            DoxySpinEdit(self.par7, "ENUM_VALUES_PER_LINE", 1, 200, 4),
            DoxyCheckBox(self.par7, "SHOW_ENUM_VALUES"),
            
            DoxySpinEdit(self.par7, "TREEVIEW_WIDTH", 50, 800, 250),
            
            DoxyCheckBox(self.par7, "EXT_LINKS_IN_WINDOW"),
            DoxyCheckBox(self.par7, "OBFUSCATE_EMAILS"),
            
            DoxyComboBox(self.par7, "HTML_FORMULA_FORMAT", ["png", "svg"]),
            
            DoxySpinEdit(self.par7, "FORMULA_FONTSIZE", 9, 74, 10),
            DoxyLineBtn1(self.par7, "FORMULA_MACROFILE"),
            
            DoxyCheckBox(self.par7, "USE_MATHJAX"),
            
            DoxyComboBox(self.par7, "MATHJAX_VERSION", ["MathJax2", "MathJax3", "MathJax4"]),
            DoxyComboBox(self.par7, "MATHJAX_FORMAT", ["HTML-CSS", "NativeHtml", "chtml", "SVG"]),
            DoxyLineEdit(self.par7, "MATHJAX_RELPATH"),
            DoxyLineBtn3(self.par7, "MATHJAX_EXTENSIONS"),
            DoxyTextEdit(self.par7, "MATHJAX_EXTENSIONS", []),
            DoxyLineEdit(self.par7, "MATHJAX_CODEFILE"),
            
            DoxyCheckBox(self.par7, "SEARCHENGINE"),
            DoxyCheckBox(self.par7, "SERVER_BASED_SEARCH"),
            DoxyCheckBox(self.par7, "EXTERNAL_SEARCH"),
            DoxyLineEdit(self.par7, "SEARCHENGINE_URL"),
            DoxyLineBtn1(self.par7, "SEARCHDATA_FILE"),
            DoxyLineEdit(self.par7, "EXTERNAL_SEARCH_ID"),
            DoxyLineBtn3(self.par7, "EXTRA_SEARCH_MAPPINGS"),
            DoxyTextEdit(self.par7, "EXTRA_SEARCH_MAPPINGS", []),
        ]
        html_lay = DOXYGEN_PROJECT_PAGES["HTML"].layout
        for item in self.html_items:
            html_lay.addWidget(item)
        html_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par8 = DOXYGEN_PROJECT_PAGES["LaTeX"]
        self.latex_items = [
            DoxyCheckBox(self.par8, "GENERATE_LATEX"),
            DoxyLineBtnA(self.par8, "LATEX_OUTPUT", "", 1),
            DoxyLineBtn1(self.par8, "LATEX_CMD_NAME"),
            DoxyLineBtn1(self.par8, "MAKEINDEX_CMD_NAME"),
            DoxyLineEdit(self.par8, "LATEX_MAKEINDEX_CMD"),
            DoxyCheckBox(self.par8, "COMPACT_LATEX"),
            DoxyComboBox(self.par8, "PAPER_TYPE", ["a4", "letter", "legal", "executive"]),
            DoxyLineBtn3(self.par8, "EXTRA_PACKAGES"),
            DoxyTextEdit(self.par8, "EXTRA_PACKAGES", []),
            DoxyLineBtn1(self.par8, "LATEX_HEADER"),
            DoxyLineBtn1(self.par8, "LATEX_FOOTER"),
            DoxyLineBtn4(self.par8, "LATEX_EXTRA_STYLESHEET"),
            DoxyTextEdit(self.par8, "LATEX_EXTRA_STYLESHEET", []),
            DoxyLineBtn4(self.par8, "LATEX_EXTRA_FILES"),
            DoxyTextEdit(self.par8, "LATEX_EXTRA_FILES", []),
            DoxyCheckBox(self.par8, "PDF_HYPERLINKS"),
            DoxyCheckBox(self.par8, "USE_PDFLATEX"),
            DoxyComboBox(self.par8, "LATEX_BATCHMODE", [
                "NO",
                "YES",
                "BATCH",
                "NON_STOP",
                "SCROLL",
                "ERROR_STOP"
                ]),
            DoxyCheckBox(self.par8, "LATEX_HIDE_INDICES"),
            DoxyLineEdit(self.par8, "LATEX_BIB_STYLE"),
            DoxyLineBtnA(self.par8, "LATEX_EMOJI_DIRECTORY", "", 1)
        ]
        latex_lay = DOXYGEN_PROJECT_PAGES["LaTeX"].layout
        for item in self.latex_items:
            latex_lay.addWidget(item)
        latex_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par9 = DOXYGEN_PROJECT_PAGES["RTF"]
        self.rtf_items = [
            DoxyCheckBox(self.par9, "GENERATE_RTF"),
            DoxyLineBtnA(self.par9, "RTF_OUTPUT", "", 1),
            DoxyCheckBox(self.par9, "COMPACT_RTF"),
            DoxyCheckBox(self.par9, "RTF_HYPERLINKS"),
            DoxyLineBtn1(self.par9, "RTF_STYLESHEET_FILE"),
            DoxyLineBtn1(self.par9, "RTF_EXTENSIONS_FILE"),
            DoxyLineBtn4(self.par9, "RTF_EXTRA_FILES")
        ]
        rtf_lay = DOXYGEN_PROJECT_PAGES["RTF"].layout
        for item in self.rtf_items:
            rtf_lay.addWidget(item)
        rtf_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par10 = DOXYGEN_PROJECT_PAGES["Man"]
        self.man_items = [
            DoxyCheckBox(self.par10, "GENERATE_MAN"),
            DoxyLineBtnA(self.par10, "MAN_OUTPUT", "", 1),
            DoxyLineEdit(self.par10, "MAN_EXTENSION"),
            DoxyLineEdit(self.par10, "MAN_SUBDIR"),
            DoxyCheckBox(self.par10, "MAN_LINKS")
        ]
        man_lay = DOXYGEN_PROJECT_PAGES["Man"].layout
        for item in self.man_items:
            man_lay.addWidget(item)
        man_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par11 = DOXYGEN_PROJECT_PAGES["XML"]
        self.xml_items = [
            DoxyCheckBox(self.par11, "GENERATE_XML"),
            DoxyLineBtnA(self.par11, "XML_OUTPUT", "", 1),
            DoxyCheckBox(self.par11, "XML_PROGRAMLISTING"),
            DoxyCheckBox(self.par11, "XML_NS_MEMB_FILE_SCOPE")
        ]
        xml_lay = DOXYGEN_PROJECT_PAGES["XML"].layout
        for item in self.xml_items:
            xml_lay.addWidget(item)
        xml_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par12 = DOXYGEN_PROJECT_PAGES["DocBook"]
        self.docbook_items = [
            DoxyCheckBox(self.par12, "GENERATE_DOCBOOK"),
            DoxyLineBtnA(self.par12, "DOCBOOK_OUTPUT", "", 1)
        ]
        docbook_lay = DOXYGEN_PROJECT_PAGES["DocBook"].layout
        for item in self.docbook_items:
            docbook_lay.addWidget(item)
        docbook_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par13 = DOXYGEN_PROJECT_PAGES["AutoGen"]
        self.autogen_items = [
            DoxyCheckBox(self.par13, "GENERATE_AUTOGEN_DEF"),
        ]
        autogen_lay = DOXYGEN_PROJECT_PAGES["AutoGen"].layout
        for item in self.autogen_items:
            autogen_lay.addWidget(item)
        autogen_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par14 = DOXYGEN_PROJECT_PAGES["SQLite3"]
        self.sqlite3_items = [
            DoxyCheckBox(self.par14, "GENERATE_SQLITE3"),
            DoxyLineBtnA(self.par14, "SQLITE3_OUTPUT", "", 1),
            DoxyCheckBox(self.par14, "SQLITE3_RECREATE_DB")
        ]
        sqlite3_lay = DOXYGEN_PROJECT_PAGES["SQLite3"].layout
        for item in self.sqlite3_items:
            sqlite3_lay.addWidget(item)
        sqlite3_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par15 = DOXYGEN_PROJECT_PAGES["PerlMod"]
        self.perlmod_items = [
            DoxyCheckBox(self.par15, "GENERATE_PERLMOD"),
            DoxyCheckBox(self.par15, "PERLMOD_LATEX"),
            DoxyCheckBox(self.par15, "PERLMOD_PRETTY"),
            DoxyLineEdit(self.par15, "PERLMOD_MAKEVAR_PREFIX")
        ]
        perlmod_lay = DOXYGEN_PROJECT_PAGES["PerlMod"].layout
        for item in self.perlmod_items:
            perlmod_lay.addWidget(item)
        perlmod_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par16 = DOXYGEN_PROJECT_PAGES["Preprocessor"]
        self.preproc_items = [
            DoxyCheckBox(self.par16, "ENABLE_PREPROCESSING"),
            DoxyCheckBox(self.par16, "MACRO_EXPANSION"),
            DoxyCheckBox(self.par16, "EXPAND_ONLY_PREDEF"),
            DoxyCheckBox(self.par16, "SEARCH_INCLUDES"),
            DoxyLineBtn4(self.par16, "INCLUDE_PATH"),
            DoxyTextEdit(self.par16, "INCLUDE_PATH", []),
            DoxyLineBtn3(self.par16, "INCLUDE_FILE_PATTERNS"),
            DoxyTextEdit(self.par16, "INCLUDE_FILE_PATTERNS"),
            DoxyLineBtn3(self.par16, "PREDEFINED"),
            DoxyTextEdit(self.par16, "PREDEFINED", []),
            DoxyLineBtn3(self.par16, "EXPAND_AS_DEFINED"),
            DoxyTextEdit(self.par16, "EXPAND_AS_DEFINED", []),
            DoxyCheckBox(self.par16, "SKIP_FUNCTION_MACROS")
        ]
        preproc_lay = DOXYGEN_PROJECT_PAGES["Preprocessor"].layout
        for item in self.preproc_items:
            preproc_lay.addWidget(item)
        preproc_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par17 = DOXYGEN_PROJECT_PAGES["External"]
        self.external_items = [
            DoxyLineBtn4(self.par17, "TAGFILES"),
            DoxyTextEdit(self.par17, "TAGFILES", []),
            DoxyLineBtn1(self.par17, "GENERATE_TAGFILE"),
            DoxyCheckBox(self.par17, "ALLEXTERNALS"),
            DoxyCheckBox(self.par17, "EXTERNAL_GROUPS"),
            DoxyCheckBox(self.par17, "EXTERNAL_PAGES")
        ]
        external_lay = DOXYGEN_PROJECT_PAGES["External"].layout
        for item in self.external_items:
            external_lay.addWidget(item)
        external_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par18 = DOXYGEN_PROJECT_PAGES["Dot"]
        self.dot_items = [
            DoxyCheckBox(self.par18, "HIDE_UNDOC_RELATIONS"),
            DoxyCheckBox(self.par18, "HAVE_DOT"),
            DoxySpinEdit(self.par18, "DOT_NUM_THREADS", 0,  64,  0),
            DoxySpinEdit(self.par18, "DOT_BATCH_SIZE", 0, 100, 50),
            DoxyLineEdit(self.par18, "DOT_COMMON_ATTR"),
            DoxyLineEdit(self.par18, "DOT_EDGE_ATTR"),
            DoxyLineEdit(self.par18, "DOT_NODE_ATTR"),
            DoxyLineBtnA(self.par18, "DOT_FONTPATH", "", 1),
            DoxyComboBox(self.par18, "CLASS_GRAPH", [
                "YES",
                "NO",
                "TEXT",
                "GRAPH",
                "BUILTIN"]),
            DoxyCheckBox(self.par18, "COLLABORATION_GRAPH"),
            DoxyCheckBox(self.par18, "GROUP_PATHS"),
            DoxyCheckBox(self.par18, "UML_LOOK"),
            DoxySpinEdit(self.par18, "UML_LIMIT_NUM_FIELDS", 0, 100, 10),
            DoxySpinEdit(self.par18, "UML_MAX_EDGE_LABELS" , 0, 100, 10),
            DoxyComboBox(self.par18, "DOT_UML_DETAILS", ["NO", "YES", "NONE"]),
            DoxySpinEdit(self.par18, "DOT_WRAP_THRESHOLD", 0, 100, 17),
            DoxyCheckBox(self.par18, "TEMPLATE_RELATIONS"),
            DoxyCheckBox(self.par18, "INCLUDE_GRAPH"),
            DoxyCheckBox(self.par18, "INCLUDEED_BY_GRAPH"),
            DoxyCheckBox(self.par18, "CALL_GRAPH"),
            DoxyCheckBox(self.par18, "CALLER_GRAPH"),
            DoxyCheckBox(self.par18, "GRAPHICAL_HIEARCHY"),
            DoxyCheckBox(self.par18, "DIRECTORY_GRAPH"),
            DoxySpinEdit(self.par18, "DIR_GRAPH_MAX_DEPTH", 1, 100, 1),
            DoxyComboBox(self.par18, "DOT_IMAGE_FORMAT", [
                "png",
                "jpg",
                "gif",
                "svg",
                
                "png:cairo",
                "png:cairo:cairo",
                "png:cairo:gd",
                "png:cairo:gdiplus",
                
                "png:gd",
                "png:gd:gd",
                
                "png:gdiplus",
                "png:gdiplus:gdiplus",
                
                "svg:cairo",
                "svg:cairo:cairo",
                
                "svg:svg",
                "svg:svg:core",
                
                "gif:cairo",
                "gif:cairo:gd",
                "gif:cairo:gdiplus",
                
                "gif:gd",
                "gif:gd:gd",
                
                "gif:gdiplus",
                "gif:gdiplus:gdiplus",
                
                "jpg:cairo",
                "jpg:cairo:gd",
                "jpg:cairo:gdiplus",
                
                "jpg:gd",
                "jpg:gd:gd",
                
                "jpg:gdiplus",
                "jpg:gdiplus:gdiplus"]),
            DoxyCheckBox(self.par18, "INTERACTIVE_SVG"),
            DoxyLineBtn1(self.par18, "DOT_PATH"),
            DoxyLineBtn4(self.par18, "DOTFILE_DIRS"),
            DoxyTextEdit(self.par18, "DORFILE_DIRS", []),
            DoxyLineBtn1(self.par18, "DIA_PATH"),
            DoxyLineBtn4(self.par18, "DIAFILE_DIRS"),
            DoxyTextEdit(self.par18, "DIAFILE_DIRS", []),
            DoxyLineBtn1(self.par18, "PLANTUM_JAR_PATH"),
            DoxyLineBtn1(self.par18, "PLANTIM_CFG_FILE"),
            DoxyLineBtn4(self.par18, "PLANTUM_INCLUDE_PATH"),
            DoxyTextEdit(self.par18, "PLANTUM_INCLUDE_PATH", []),
            DoxyLineBtn4(self.par18, "PLANTUMFILE_DIRS"),
            DoxyTextEdit(self.par18, "PLANTUMFILE_DIRS", []),
            DoxyLineBtn1(self.par18, "MERMAID_PATH"),
            DoxyLineBtn1(self.par18, "MERMAID_CONFIG_FILE"),
            DoxyComboBox(self.par18, "MERMAID_RENDER_MODE", [
                "AUTO",
                "CLI",
                "CLIENT_SIDE"
            ]),
            DoxyLineEdit(self.par18, "MERMAID_JS_URL",
                "https://cdn.jsdelivr.net/npm/mermaid@11/"
                "dist/mermaid.esm.min.mjs"
            ),
            DoxyLineBtn4(self.par18, "MERMAIDFILE_DIRS"),
            DoxyTextEdit(self.par18, "MERMAIDFILE_DIRS", []),
            DoxySpinEdit(self.par18, "DOT_GRAPH_MAX_NODES", 0, 100, 50),
            DoxySpinEdit(self.par18, "MAX_DOT_GRAPH_DEPTH", 0, 100,  0),
            DoxyCheckBox(self.par18, "GENERATE_LEGEND"),
            DoxyCheckBox(self.par18, "DOT_CLEANUP"),
            DoxyLineBtn1(self.par18, "MSCGEN_TOOL"),
            DoxyLineBtn4(self.par18, "MSCFILE_DIRS"),
            DoxyTextEdit(self.par18, "MSCFILE_DIRS", [])
        ]
        dot_lay = DOXYGEN_PROJECT_PAGES["Dot"].layout
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
        page = DOXYGEN_PROJECT_PAGES.get(text)
        if page:
            self.expert_pages.setCurrentWidget(page.area)
    
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
    
    def show_help_for_key(self, help_key: str, title: str = ""):
        translated = share.locales.tr(help_key)
        self.html_preview.clear()
        self.html_preview.setHtml(translated)
    
    def _project_payload(self, path: str) -> dict:
        now = datetime.now()
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
        }

    def _validate_payload(self, data: dict):
        if not isinstance(data, dict):
            return False, share.locales.tr("The JSON-File is not a valid project file.")
        header = data.get("header")
        if not isinstance(header, dict):
            return False, share.locales.tr("missing Header-Information's.")
        if header.get("format") != HEADER_FORMAT:
            return False, share.locales.tr("project format is invalid.")
        if header.get("tool") != HEADER_TOOL:
            return False, share.locales.tr(f"the JSON-File does not cover the DoxyGen-Dialog: {header.get('tool', 'unknown')}).")
        if header.get("kind") != HEADER_KIND:
            return False, share.locales.tr("invalid project type.")
        return True, ""

    def _reload_project_list(self):
        self.project_list.clear()
        files = sorted(self.project_dir.glob("*.json"), key=lambda p: p.stat().st_mtime)
        for path in files:
            dt_text = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            item = QListWidgetItem(self.project_list)
            item.setData(Qt.UserRole, str(path))
            item.setSizeHint(QSize(220, 42))
            widget = ProjectListItemWidget(path.name, dt_text)
            self.project_list.addItem(item)
            self.project_list.setItemWidget(item, widget)

    def save_project_as(self):
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
            msg = share.locales.tr("Save Project As ...")
            fxt = share.locales.tr("Did you realy want to overwrite the file")
            
            reply = QMessageBox.question(self, msg, f"{fxt}:\n\n{Path(path).name}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                return
            
            self.state  = {
                "current_tab": self.tabs.currentIndex(),
                "expert_item": self.list_categories.currentRow()
            }
            
            for page in [
                self.project_items,
                self.build_items,
                self.messages_items,
                self.input_items,
                self.browser_items,
                self.index_items,
                self.html_items,
                self.latex_items,
                self.rtf_items,
                self.man_items,
                self.xml_items,
                self.docbook_items,
                self.autogen_items,
                self.sqlite3_items,
                self.perlmod_items,
                self.preproc_items,
                self.external_items,
                self.dot_items]:
                self.save_items(page)
            
            payload["state" ] = self.state
            payload["config"] = self.config
            
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
                QMessageBox.critical(self,
                    share.locales.tr("Invalide project file"),
                    err)
                return
            
            self.state = data.get("state", {})
            self.tabs.setCurrentIndex(int(self.state.get("current_tab", 0)))
            self.list_categories.setCurrentRow(int(self.state.get("expert_item", 0)))
            
            # ------------------------
            # set new item values ...
            # ------------------------
            self.config = data.get("config",{})
            
            for page in [
                self.project_items,
                self.build_items,
                self.messages_items,
                self.input_items,
                self.browser_items,
                self.index_items,
                self.html_items,
                self.latex_items,
                self.rtf_items,
                self.man_items,
                self.xml_items,
                self.docbook_items,
                self.autogen_items,
                self.sqlite3_items,
                self.perlmod_items,
                self.preproc_items,
                self.external_items,
                self.dot_items]:
                self.load_items(page)
            
        except RuntimeError as e:
            QMessageBox.critical(self, share.locales.tr("Open"), str(e))
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Open"), str(e))
    
    def save_items(self, items):
        for item in items:
            if isinstance(item, DoxyLineEdit):
                if not item.flag:
                    text = item.input.text()
                    self.config[item.help_str] = text
                    
            elif isinstance(item, DoxyLineBtn1):
                text = item.input.input.text()
                self.config[item.help_str] = text
                
            elif isinstance(item, DoxyLineBtnA):
                text = item.input.input.text()
                self.config[item.help_str] = text
                
            elif isinstance(item, DoxyLineBtn3):
                text = item.input.input.text()
                self.config[item.help_str] = text
                
            elif isinstance(item, DoxyLineBtn4):
                text = item.input.input.text()
                self.config[item.help_str] = text
                
            elif isinstance(item, DoxySpinEdit):
                value = item.spin.value()
                self.config[item.help_str] = value
                
            elif isinstance(item, DoxyCheckBox):
                if item.check.isChecked():
                    self.config[item.help_str] = 1
                else:
                    self.config[item.help_str] = 0
                    
            elif isinstance(item, DoxyTextEdit):
                text = item.edit.toPlainText()
                self.config[item.help_str] = text
                
            elif isinstance(item, DoxyComboBox):
                text = item.combo.currentText()
                self.config[item.help_str] = text
    
    def _to_int(self, value, default=0):
        try:
            if value is None:
                return default
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    return default
            return int(value)
        except Exception:
            return default
    
    def load_items(self, items):
        for item in items:
            if   isinstance(item, DoxyLineEdit): item.input.      setText(str(self.config.get(item.help_str, "")))
            
            elif isinstance(item, DoxyLineBtn1): item.input.input.setText(str(self.config.get(item.help_str, "")))
            elif isinstance(item, DoxyLineBtnA): item.input.input.setText(str(self.config.get(item.help_str, "")))
            
            elif isinstance(item, DoxyLineBtn3): item.input.input.setText("")
            elif isinstance(item, DoxyLineBtn4): item.input.input.setText("")
            
            elif isinstance(item, DoxyCheckBox):
                check = self._to_int(self.config.get(item.help_str, 0), 0)
                if check:
                    item.check.setChecked(True)
                else:
                    item.check.setChecked(False)
            elif isinstance(item, DoxyTextEdit):
                item.edit.clear()
                item.edit.appendPlainText(str(self.config.get(item.help_str, "")))
            
            elif isinstance(item, DoxySpinEdit): item.spin.setValue(self._to_int(self.config.get(item.help_str, 0), 0))
            elif isinstance(item, DoxyComboBox):
                index = item.combo.findText(str(self.config.get(item.help_str, "English")))
                if index >= 0:
                    item.combo.setCurrentIndex(index)
    
    def _delete_selected_project(self):
        path = self._selected_project_path()
        if not path:
            return
        msg = share.locales.tr("Would you realy delte the Project?")
        fxt = share.locales.tr("Delete Project")
        
        reply = QMessageBox.question(self, fxt, f"{msg}\n\n{Path(path).name}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  )
        if reply != QMessageBox.Yes:
            return
        try:
            os.remove(path)
            if self.current_project_path == path:
                self.current_project_path = ""
            self._reload_project_list()
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Delete"), str(e))
