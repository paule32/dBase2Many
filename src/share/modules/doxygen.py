# ---------------------------------------------------------------------------
# File:   doxygen.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
#
# die Datei erwartet die .mo-Datei standardmäßig unter
# src/data/po/locales/<sprache>/LC_MESSAGES/doxygen.mo
# ---------------------------------------------------------------------------
from __future__ import annotations

import share.resrces.images_rc
import share.resrces.locales_de_rc

from   share.common import *

DOXYGEN_PROJECT_PAGES = {}

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


class DoxyScrollPage:
    def __init__(self, owner, area, widget, layout):
        self.owner = owner
        self.area = area
        self.widget = widget
        self.layout = layout
        
def _default_project_dir() -> Path:
    base = Path.home() / "Documents" / "dBase2Many" / "DoxygenProjects"
    base.mkdir(parents=True, exist_ok=True)
    return base

def bind_help(parent, obj, help_key: str, title: str = ""):
    obj.setProperty("help_key", help_key)
    obj.setProperty("help_title", title)
    
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
    def __init__(self,
        owner           = None,
        help_str :str   =   "",
        icon_norm:QIcon = None,
        icon_hovr:QIcon = None, flag:int=0):
        
        super().__init__()
        
        self.owner      = owner
        self.flag       = flag
        self.filename   = ""
        
        self.help       = help_str
        
        self.icon_norm  = icon_norm
        self.icon_hovr  = icon_hovr
        
        self.setIconSize(QSize(22, 22))
        self.setProperty("help", self.help)
        
        self.setMaximumWidth (26)
        self.setMaximumHeight(26)
        
        self.clicked.connect(self.on_click)
        
        if self.icon_norm is not None:
            self.setIcon(self.icon_norm)
    
    def open_file(self) -> str:
        try:
            text = share.locales.tr("All Files")
            self.filename, _ = QFileDialog.getOpenFileName(
                self, share.locales.tr("Open File..."),
                "", f"{text} (*.*)")
            if self.filename:
                return self.filename
            return str("")
        except FileNotFoundError as e:
            dlg = ErrorMessage("File not found Error",
            f"The requested file: {self.filename} could not be found.")
            dlg.exec_()
            return ""
        except PermissionError as e:
            dlg = ErrorMessage("File Permission Error",
            f"You have not enough permissions to open file: {self.filename}.")
            dlg.exec_()
            return ""
        except RuntimeError as e:
            dlg = ErrorMessage("Runtime Error",
            f"The Python Library throws a Runtime Error on opening file: {self.filename}.")
            dlg.exec_()
            return ""
        except OSError as e:
            dlg = ErrorMessage("Operating System Error",
            f"The System is not able to open file: {self.filename}.")
            dlg.exec_()
            return ""
        except Exception as e:
            dlg = ErrorMessage("Common Exception Error",
            f"Common Exception throwed on open file: {self.filename}.")
            dlg.exec_()
            return ""
    
    def on_click(self, text):
        if self.owner is not None:
            if isinstance(self.owner, DoxyLineBtn1):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
            elif isinstance(self.owner, DoxyLineBtn3):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
                elif self.flag == 2:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            page = DOXYGEN_PROJECT_PAGES.get(res)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help)
                                if item is not None:
                                    text = self.owner.input.input.text().strip()
                                    item.edit.appendPlainText(text)
                                    print("ADD text:", text)
                                    break
                elif self.flag == 3:
                    print("deL text")
            elif isinstance(self.owner, DoxyLineBtn4):
                if self.flag == 1:
                    if self.open_file():
                        self.owner.input.input.setText(self.filename)
                elif self.flag == 2:
                    if  (DOXYGEN_EXPERT_ITEMS  is not None)\
                    and (DOXYGEN_PROJECT_PAGES is not None):
                        for res in DOXYGEN_EXPERT_ITEMS:
                            page = DOXYGEN_PROJECT_PAGES.get(res)
                            if page is not None:
                                item = page.area.findChild(DoxyTextEdit, self.help)
                                if item is not None:
                                    text = self.owner.input.input.text().strip()
                                    item.edit.appendPlainText(text)
                                    print("add text:", text)
                                    break
                elif self.flag == 3:
                    print("Del text")
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
# \brief this is a helper class for QLabel to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyLabel(QLabel):
    def __init__(self, parent=None, help_str:str="", flag:int=0):
        super().__init__(parent.owner)
        
        self.setProperty("help", help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        bind_help(self.parent, self, help_str)
        
        if flag == 0: self.setText(help_str)
        else:         self.setText("")
            
        self.setFont(QFont("Consolas", 10))
        self.setMinimumWidth(164)
        self.setStyleSheet("color: white;")
        self.setProperty("help", help_str)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QPlainTextEdit to reduce code space.
# \param help_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyTextEdit(QWidget):
    def __init__(self, parent=None, help_str:str="", text:list=[]):
        super().__init__(parent.owner)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.setObjectName(self.help)
        self.layout = DoxyHBoxLayout(self)
        
        self.label  = DoxyLabel(self.parent, help_str, 1)
        self.edit   = QPlainTextEdit()
        self.edit.setStyleSheet("background-color: #303030;")
        
        for line in text:
            self.edit.appendPlainText(line)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QCheckBox as a helper class to reduce code space.
# ---------------------------------------------------------------------------
class DoxyCheckBox(QWidget):
    def __init__(self, parent=None, help_str:str=""):
        super().__init__(parent.owner)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, help_str)
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
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
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
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, help_str)
        self.spin   = QSpinBox()
        
        self.spin.setMinimum(v_min)
        self.spin.setMaximum(v_max)
        self.spin.setValue  (v_def)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin)
        self.layout.addStretch(1)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief construct a QLineEdit with a label
# \param parent   - QWidget as the parent
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the input content, default: "".
# ---------------------------------------------------------------------------
class DoxyLineEdit(QWidget):
    def __init__(self, parent=None, help_str:str="", text_str: str=""):
        super().__init__(parent.owner)
        
        self.setProperty("help", help_str)
        self.setProperty("text", text_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, help_str)
        self.input  = QLineEdit()
        
        self.input.setProperty("help", help_str)
        self.input.setFont(QFont("Consolas", 10))
        self.input.setText(text_str)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLineEdit with a Button to reduce code.
# ---------------------------------------------------------------------------
class DoxyLineBtn1(QWidget):
    def __init__(self, parent=None, help_str:str="", text_str:str="", item=None):
        super().__init__(parent.owner)
        
        self.setProperty("help", help_str)
        self.setProperty("text", text_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, help_str, text_str)
        self.buttn  = DoxyButton  (self, help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.buttn)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


class DoxyLineBtn3(QWidget):
    def __init__(self, parent=None, help_str:str="", text_str:str=""):
        super().__init__(parent.owner)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(self, help_str, text_str)
        
        self.butt1  = DoxyButton(self, help_str, QIcon(":/icons/add.ico"), QIcon(":/icons/add_hov.ico"), 2)
        self.butt2  = DoxyButton(self, help_str, QIcon(":/icons/sub.ico"), QIcon(":/icons/sub_hov.ico"), 3)
        self.butt3  = DoxyButton(self, help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        self.layout.addWidget(self.input)
        
        self.layout.addWidget(self.butt1)
        self.layout.addWidget(self.butt2)
        self.layout.addWidget(self.butt3)
    
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


class DoxyLineBtn4(QWidget):
    def __init__(self, parent=None, help_str:str="", text_str:str=""):
        super().__init__(None)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.setProperty("help", help_str)
        self.setProperty("text", text_str)
        
        self.layout = DoxyHBoxLayout(self)
        self.input  = DoxyLineEdit(parent, help_str, text_str)
        
        self.butt1  = DoxyButton(self, help_str, QIcon(":/icons/add.ico"), QIcon(":/icons/add_hov.ico"), 2)
        self.butt2  = DoxyButton(self, help_str, QIcon(":/icons/sub.ico"), QIcon(":/icons/sub_hov.ico"), 3)
        self.butt3  = DoxyButton(self, help_str, QIcon(":/icons/frs.ico"), QIcon(":/icons/frs_hov.ico"), 4)
        self.butt4  = DoxyButton(self, help_str, QIcon(":/icons/doc.ico"), QIcon(":/icons/doc_hov.ico"), 1)
        
        self.layout.addWidget(self.input)
        
        self.layout.addWidget(self.butt1)
        self.layout.addWidget(self.butt2)
        self.layout.addWidget(self.butt3)
        self.layout.addWidget(self.butt4)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is a helper class for QLabel with a image to reduce code space.
# \param help_str - string for the label and help id, default: "".
# \param text_str - string for the label and help id, default: "".
# ---------------------------------------------------------------------------
class DoxyImage(QWidget):
    def __init__(self, parent=None, help_str:str="", text_str:str=""):
        super().__init__(parent.owner)
        
        self.setMinimumHeight(74)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.label1 = DoxyLabel(self, help_str, 1)
        self.label2 = QLabel(text_str)
        
        self.label2.setAlignment(Qt.AlignLeft)
        self.label2.setProperty("help", help_str)
        
        self.label2.setFont(QFont("Arial", 9))
        self.label2.setStyleSheet("color:yellow;")
        
        self.layout.addWidget(self.label1, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.label2, alignment=Qt.AlignLeft)
        self.layout.addStretch(1)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
class DoxyComboBox(QWidget):
    def __init__(self, parent=None, help_str:str="", items:list=[]):
        super().__init__(parent.owner)
        
        self.setProperty("help", help_str)
        
        self.parent = parent
        self.owner  = parent.owner
        self.help   = help_str
        
        self.layout = DoxyHBoxLayout(self)
        self.label  = DoxyLabel(self, help_str)
        self.combo  = QComboBox()
        
        self.combo.addItems(items)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addStretch(1)
        
    def enterEvent(self, event):
        self.owner.show_help_for_key(self.help)
        super().enterEvent(event)


# ---------------------------------------------------------------------------
# \brief this is the doxygen tool window for help / documenting the source.
# ---------------------------------------------------------------------------
class DoxyGenToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.owner       = self
        
        self.project_dir = _default_project_dir()
        self.propath     = self.project_dir / "doxygen_project.json"
        
        self.current_project_path = ""

        self.lang = self._get_default_lang().split("_")[0].lower()
        self.trmo = self._load_mo_from_resource(f":/locales/{self.lang}/doxygen.mo")
            
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
            self.list_categories.addItem(item)
        
        self.list_categories.currentTextChanged.connect(self._on_expert_item_changed)
        self.expert_splitter_h.addWidget(self.list_categories)
        
        # -----------------------------------------------------------
        self.expert_pages = QStackedWidget()
        self.expert_splitter_h.addWidget(self.expert_pages)
        
        for name in DOXYGEN_EXPERT_ITEMS:
            scroll_owner, scroll_area, scroll_widget, scroll_lay = self._create_scroll_page()
            DOXYGEN_PROJECT_PAGES[str(name)] = DoxyScrollPage(
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
        self.par1 = DOXYGEN_PROJECT_PAGES["Project"]
        #self.par1 = self.par1.owner
        self.project_items = [
            DoxyLineEdit(self.par1, "DOXYFILE_ENCODING", "UTF-8"),
            
            DoxyLineEdit (self.par1, "PROJECT_NAME", "MyProject"),
            DoxyLineEdit (self.par1, "PROJECT_NUMBER"),
            DoxyLineEdit (self.par1, "PROJECT_BRIEF"),
            DoxyLineBtn1 (self.par1, "PROJECT_LOGO", "",
                DoxyImage(self.par1, "", share.locales.tr("No Project Logo selected."))),
            DoxyLineBtn1 (self.par1, "PROJECT_ICON", "",
                DoxyImage(self.par1, "", share.locales.tr("No Project Icon selected."))),
            
            DoxyLineBtn1(self.par1, "OUTPUT_DIRECTORY"),
            DoxyCheckBox(self.par1, "CREATE_SUBDIRS"),
            DoxySpinEdit(self.par1, "CREATE_SUBDIRS_LEVEL", 0, 64, 4),
            
            DoxyCheckBox(self.par1, "ALLOW_UNICODE_NAMES"),
            DoxyComboBox(self.par1, "OUTPUT_LANGUAGE", SUPPORTED_LANGUAGES),
            
            DoxyCheckBox(self.par1, "BRIEF_MEMBER_DESC"),
            DoxyCheckBox(self.par1, "REPEAT_BRIEF"),
            
            DoxyLineBtn3(self.par1, "ABBREVIATVE_BRIEF"),
            DoxyTextEdit(self.par1, "ABBREVIATVE_BRIEF", []),
            
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
            
            DoxyLineBtn3(self.par1, "EXTERNAL_MAPPING"),
            DoxyTextEdit(self.par1, "EXTERNAL_MAPPING", []),
            
            DoxyCheckBox(self.par1, "MARKDOWN_SUPPORT"),
            DoxyCheckBox(self.par1, "MARKDOWN_STRICT"),
            DoxyComboBox(self.par1, "MARKDOWN_ID_STYLE", ["DOXYGEN", "GITHUB"]),
            
            DoxySpinEdit(self.par1, "TOC_INCLUDE_HEADINGS"),
            
            DoxyCheckBox(self.par1, "AUTOLINK_SUPPORT"),
            DoxyLineBtn3(self.par1, "AUTOLINK_IGNORE_WORDS"),
            DoxyTextEdit(self.par1, "AUTOLINK_IGNORE_WORDS", []),
            
            DoxyCheckBox(self.par1, "BUILTiN_STL_SUPPORT"),
            DoxyCheckBox(self.par1, "CPP_CLI_SUPPORT"),
            DoxyCheckBox(self.par1, "SIP_SUPPORT"),
            DoxyCheckBox(self.par1, "IDL_PROPERTY_SUPPORT"),
            DoxyCheckBox(self.par1, "DISTRIBUTE_GROUP_DOC"),
            DoxyCheckBox(self.par1, "GROUP_NESTED_COMPOUNDS"),
            
            DoxyCheckBox(self.par1, "SUBGROUPING"),
            DoxyCheckBox(self.par1, "INLINE_GROUPED_CLASSES"),
            DoxyCheckBox(self.par1, "INLINE_SIMPLE_STRUCTS"),
            
            DoxyCheckBox(self.par1, "TYPEDEF_HIDE_STRUCT"),
            DoxySpinEdit(self.par1, "LOOKUP_CACHE_SIZE"),
            
            DoxySpinEdit(self.par1, "NUM_PROC_THREADS"),
            DoxyComboBox(self.par1, "TIMESTAMP", ["YES", "NO", "DATETIME", "DATE"]),
        ]
        project_lay = DOXYGEN_PROJECT_PAGES["Project"].layout
        for item in self.project_items:
            project_lay.addWidget(item)
        project_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par2 = DOXYGEN_PROJECT_PAGES["Build"]
        #self.par2 = self.par2.owner
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
            
            DoxyLineBtn3(self.par2, "ENABLE_SECTIONS"),
            DoxyTextEdit(self.par2, "ENABLE_SECTIONS", []),
            
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
            DoxyLineEdit(self.par3, "WARN_FORMAT"),
            DoxyLineEdit(self.par3, "WARN_LINE_FORMAT"),
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
            DoxyLineEdit(self.par4, "INPUT_ENCODING"),
            DoxyLineBtn3(self.par4, "INPUT_FILE"),
            DoxyTextEdit(self.par4, "INPUT_FILE_ENCODING", []),
            
            DoxyLineBtn3(self.par4, "FILE_PATTERNS"),
            DoxyTextEdit(self.par4, "FILE_PATTERNS", ["*.c", "*.cc"]),
            
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
        #self.par5 = self.par5.owner
        self.browser_items = [
            DoxyCheckBox(self.par5, "SOURCE_BROWSER"),
            DoxyCheckBox(self.par5, "INLINE_SOURCES"),
            DoxyCheckBox(self.par5, "STRIP_CODE_COMMENTS"),
            
            DoxyCheckBox(self.par5, "REFERENCED_BY_RELATION"),
            DoxyCheckBox(self.par5, "REFERENCED_LINK_SOURCE"),
            
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
        #self.par6 = self.par6.owner
        self.index_items = [
            DoxyCheckBox(self.par6, "ALPHABETICAL_INDEX"),
            DoxyTextEdit(self.par6, "ALPHABETICAL_INDEX", [])
        ]
        index_lay = DOXYGEN_PROJECT_PAGES["Index"].layout
        for item in self.index_items:
            index_lay.addWidget(item)
        index_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par7 = DOXYGEN_PROJECT_PAGES["HTML"]
        #self.par7 = self.par7.owner
        self.html_items = [
            DoxyCheckBox(self.par7, "GENERATE_HTML"),
            DoxyLineBtn1(self.par7, "HTML_OUTPUT"),
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
            
            DoxySpinEdit(self.par7, "COLOR_STYLE_HUE"  , 0, 255, 220),
            DoxySpinEdit(self.par7, "COLOR_STYLE_SAT"  , 0, 255, 100),
            DoxySpinEdit(self.par7, "COLOR_STYLE_GAMMA", 0, 255,  80),
            
            DoxyCheckBox(self.par7, "HTML_DYNAMIC_MENUS"),
            DoxyCheckBox(self.par7, "HTML_DYNAMIC_SECTIONS"),
            
            DoxyCheckBox(self.par7, "HTML_CODE_FOLDING"),
            DoxyCheckBox(self.par7, "HTML_COPY_CLIPBOARD"),
            DoxyLineEdit(self.par7, "HTML_PROJECT_COOKIE"),
            DoxySpinEdit(self.par7, "HTML_INDEX_NUM_ENTRIES", 0, 255, 100),
            DoxyLineEdit(self.par7, "HTML_SITEMAP_URL"),
            
            DoxyCheckBox(self.par7, "GENERATE_HTMLHELP"),
            DoxyLineBtn1(self.par7, "HHC_LOCATION"),
            DoxyLineBtn1(self.par7, "CHM_FILE"),
            DoxyLineEdit(self.par7, "CHM_INDEX_ENCODING"),
            DoxyCheckBox(self.par7, "CHM_BINARY_TOC"),
            
            DoxyCheckBox(self.par7, "GENERATE_CHI"),
            
            DoxyCheckBox(self.par7, "GENERATE_DOCSET"),
            DoxyLineEdit(self.par7, "DOCSET_FEEDNAME"),
            DoxyLineEdit(self.par7, "DOCSET_FEEDURL"),
            DoxyLineEdit(self.par7, "DOCSET_BUNDLE_ID"),
            DoxyLineEdit(self.par7, "DOCSET_PUBLISER_ID"),
            DoxyLineEdit(self.par7, "DOCSET_PUBLISER_NAME"),
            
            DoxyCheckBox(self.par7, "GENERATE_QHP"),
            DoxyLineBtn1(self.par7, "QCH_FILE"),
            
            DoxyLineEdit(self.par7, "QHP_NAMESPACE"),
            DoxyLineEdit(self.par7, "QHP_VIRTUAL_FOLDER"),
            DoxyLineEdit(self.par7, "QHP_CUST_FILTER_NAME"),
            DoxyLineEdit(self.par7, "QHP_CUST_FILTER_ATTRS"),
            DoxyLineEdit(self.par7, "QHP_SECT_FILTER_ATTRS"),
            
            DoxyLineBtn1(self.par7, "QHG_LOCATION"),
            
            DoxyCheckBox(self.par7, "GENERATE_ECLIPSE_HELP"),
            DoxyLineEdit(self.par7, "ECLIPSE_DOC_ID"),
            
            DoxyCheckBox(self.par7, "GENERATE_TREEVIEW"),
            DoxySpinEdit(self.par7, "TREEVIEW_WIDTH", 50, 800, 100)
        ]
        html_lay = DOXYGEN_PROJECT_PAGES["HTML"].layout
        for item in self.html_items:
            html_lay.addWidget(item)
        html_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par8 = DOXYGEN_PROJECT_PAGES["LaTeX"]
        #self.par8 = self.par8.owner
        self.latex_items = [
            DoxyCheckBox(self.par8, "GENERATE_LATEX"),
        ]
        latex_lay = DOXYGEN_PROJECT_PAGES["LaTeX"].layout
        for item in self.latex_items:
            latex_lay.addWidget(item)
        latex_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par9 = DOXYGEN_PROJECT_PAGES["RTF"]
        #self.par9 = self.par9.owner
        self.rtf_items = [
            DoxyCheckBox(self.par9, "BUILD"),
        ]
        rtf_lay = DOXYGEN_PROJECT_PAGES["RTF"].layout
        for item in self.rtf_items:
            rtf_lay.addWidget(item)
        rtf_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par10 = DOXYGEN_PROJECT_PAGES["Man"]
        #self.par10 = self.par10.owner
        self.man_items = [
            DoxyCheckBox(self.par10, "BUILD"),
        ]
        man_lay = DOXYGEN_PROJECT_PAGES["Man"].layout
        for item in self.man_items:
            man_lay.addWidget(item)
        man_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par11 = DOXYGEN_PROJECT_PAGES["XML"]
        #self.par11 = self.par11.owner
        self.xml_items = [
            DoxyCheckBox(self.par11, "BUILD"),
        ]
        xml_lay = DOXYGEN_PROJECT_PAGES["XML"].layout
        for item in self.xml_items:
            xml_lay.addWidget(item)
        xml_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par12 = DOXYGEN_PROJECT_PAGES["DocBook"]
        #self.par12 = self.par12.owner
        self.docbook_items = [
            DoxyCheckBox(self.par12, "BUILD"),
        ]
        docbook_lay = DOXYGEN_PROJECT_PAGES["DocBook"].layout
        for item in self.docbook_items:
            docbook_lay.addWidget(item)
        docbook_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par13 = DOXYGEN_PROJECT_PAGES["AutoGen"]
        #self.par13 = self.par13.owner
        self.autogen_items = [
            DoxyCheckBox(self.par13, "BUILD"),
        ]
        autogen_lay = DOXYGEN_PROJECT_PAGES["AutoGen"].layout
        for item in self.autogen_items:
            autogen_lay.addWidget(item)
        autogen_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par14 = DOXYGEN_PROJECT_PAGES["SQLite3"]
        #self.par14 = self.par14.owner
        self.sqlite3_items = [
            DoxyCheckBox(self.par14, "BUILD"),
        ]
        sqlite3_lay = DOXYGEN_PROJECT_PAGES["SQLite3"].layout
        for item in self.sqlite3_items:
            sqlite3_lay.addWidget(item)
        sqlite3_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par15 = DOXYGEN_PROJECT_PAGES["PerlMod"]
        #self.par15 = self.par15.owner
        self.perlmod_items = [
            DoxyCheckBox(self.par15, "BUILD"),
        ]
        perlmod_lay = DOXYGEN_PROJECT_PAGES["PerlMod"].layout
        for item in self.perlmod_items:
            perlmod_lay.addWidget(item)
        perlmod_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par16 = DOXYGEN_PROJECT_PAGES["Preprocessor"]
        #self.par16 = self.par16.owner
        self.preproc_items = [
            DoxyCheckBox(self.par16, "BUILD"),
        ]
        preproc_lay = DOXYGEN_PROJECT_PAGES["Preprocessor"].layout
        for item in self.preproc_items:
            preproc_lay.addWidget(item)
        preproc_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par17 = DOXYGEN_PROJECT_PAGES["External"]
        #self.par17 = self.par17.owner
        self.external_items = [
            DoxyCheckBox(self.par17, "BUILD"),
        ]
        external_lay = DOXYGEN_PROJECT_PAGES["External"].layout
        for item in self.external_items:
            external_lay.addWidget(item)
        external_lay.addStretch()
        
        # -------------------------------------------------------------------------
        self.par18 = DOXYGEN_PROJECT_PAGES["Dot"]
        #self.par18 = self.par18.owner
        self.dot_items = [
            DoxyCheckBox(self.par18, "BUILDxxx"),
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

    def _get_default_lang(self):
        loc = locale.getdefaultlocale()
        
        if loc is None:
            return "en"
        
        lang = loc[0]
        if not lang:
            return "en"
        
        return lang
    
    def _load_mo_from_resource(self, resource_path: str):
        f = QFile(resource_path)
        if not f.open(QFile.ReadOnly):
            raise FileNotFoundError(resource_path)
        data = bytes(f.readAll())
        f.close()
        return gettext.GNUTranslations(BytesIO(data))
    
    def show_help_for_key(self, help_key: str, title: str = ""):
        translated = self.trmo.gettext(help_key)
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
            dt_text = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
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
