# ---------------------------------------------------------------------------
# \file  : app.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from   __future__ import annotations
import os

from   pathlib              import Path
from   typing               import Callable
from   share.locales        import *
from   share.utildef.theme  import *

# -----------------------------------------------------------------------
# we use antlr4 for the lexer + parser generator ...
# -----------------------------------------------------------------------
from antlr4      import (
     InputStream, FileStream, CommonTokenStream, Token, Lexer,
     Parser, DFA, ParserRuleContext, ATNDeserializer,
     PredictionContextCache, ParseTreeListener, ParseTreeVisitor
)
from antlr4.error.ErrorListener import ErrorListener

# -----------------------------------------------------------------------
# Qt Backend Factory + Property Mapping
# -----------------------------------------------------------------------
from PyQt5.QtCore    import (
    QObject, Qt, QSocketNotifier, pyqtSignal, QEvent, QRect, QSize,
    QRegExp, QFileInfo, QPoint, QAbstractProxyModel, QModelIndex,
    QRegularExpression, QRectF, QPointF, qRegisterResourceData, QUrl,
    qUnregisterResourceData, qVersion, QSortFilterProxyModel, QByteArray,
    QTimer, qInstallMessageHandler, QMimeData, QDataStream, QIODevice,
    QBuffer, QSettings
)
from PyQt5.QtGui     import (
    QFont, QPainter, QFontMetrics, QSyntaxHighlighter, QIcon, QPixmap,
    QTextCharFormat, QColor, QStandardItemModel, QStandardItem, QPen,
    QPalette, QFontInfo, QFontDatabase, QRegularExpressionValidator,
    QIntValidator, QPainterPath, QLinearGradient, QRadialGradient,
    QKeySequence, QTextFormat, QBrush, QGuiApplication, QTextOption,
    QTextCursor
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QFrame, QPushButton,
    QVBoxLayout, QTextEdit, QToolBar, QStatusBar, QMessageBox,
    QPlainTextEdit, QAction, QFileDialog, QMenuBar, QMdiArea,
    QMdiSubWindow, QDockWidget, QTreeWidget, QHBoxLayout, QComboBox,
    QTabWidget, QListWidget, QListWidgetItem, QScrollBar, QMenu,
    QFileDialog, QFileIconProvider, QListWidget, QTableWidget,
    QProgressBar, QTableWidgetItem, QHeaderView, QStyledItemDelegate,
    QGroupBox, QLabel, QLineEdit, QCheckBox, QRadioButton, QSpacerItem,
    QGridLayout, QSpinBox, QSizePolicy, QStyleOptionHeader, QStyle,
    QTableView, QAbstractItemView, QStyleOptionComplex, QProxyStyle,
    QToolButton, QInputDialog, QTreeWidgetItem, QTreeView, QSplitter,
    QTabBar, QRubberBand, QTreeWidget, QTreeWidgetItem, QHeaderView,
    QScrollArea, QAbstractButton
)
from PyQt5.QtWebEngineCore import (
    QWebEngineUrlSchemeHandler, QWebEngineUrlRequestJob,
    QWebEngineUrlScheme
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineScript
)
from PyQt5.QtSvg import QSvgRenderer
# -----------------------------------------------------------------------
from share.common         import *
from share.editors.editor import *
# -----------------------------------------------------------------------

from .language_profiles import LanguageProfile, get_language_profile
from . import legacy_api

legacy = legacy_api.module


import inspect

# -----------------------------------------------------------------------
# Sprachspezifischer Wrapper um die bestehende IconTab-Implementierung.
# -----------------------------------------------------------------------
class ProfiledIconTab(legacy.IconTab):
    def __init__(self, profile: LanguageProfile, *args, **kwargs):
        self.language_profile = profile

        self.tab_name = (kwargs.get("tab_name", "") or "").strip()
        self.special_items = list(kwargs.get("special_items", []) or [])

        try:
            sig = inspect.signature(legacy.IconTab.__init__)
            self._legacy_supports_special_items = "special_items" in sig.parameters
            self._legacy_supports_tab_name = "tab_name" in sig.parameters
        except Exception:
            self._legacy_supports_special_items = False
            self._legacy_supports_tab_name = False

        if not self._legacy_supports_special_items:
            kwargs.pop("special_items", None)
        if not self._legacy_supports_tab_name:
            kwargs.pop("tab_name", None)

        super().__init__(*args, **kwargs)

        # Falls die Legacy-Klasse die neuen Parameter nicht kennt,
        # trotzdem gleich die festen Icons anzeigen.
        if self.special_items and not self._legacy_supports_special_items:
            self.refresh()

    def _special_icon(self, kind: str = "new") -> legacy.QIcon:
        kind = (kind or "new").strip().lower()
        style = self.style()
        mapping = {
            "project"   : legacy.QStyle.SP_DirHomeIcon,
            "program"   : legacy.QStyle.SP_FileIcon,
            "form"      : legacy.QStyle.SP_FileDialogDetailedView,
            "designer"  : legacy.QStyle.SP_DesktopIcon,
            "expert"    : legacy.QStyle.SP_CommandLink,
            "table"     : legacy.QStyle.SP_DriveHDIcon,
            "sql"       : legacy.QStyle.SP_DriveNetIcon,
            "html"      : legacy.QStyle.SP_FileDialogContentsView,
            "css"       : legacy.QStyle.SP_FileDialogListView,
            "js"        : legacy.QStyle.SP_BrowserReload,
            "new"       : legacy.QStyle.SP_FileIcon,
        }
        try:
            return style.standardIcon(mapping.get(kind, legacy.QStyle.SP_FileIcon))
        except Exception:
            return legacy.QIcon()

    def _add_special_items_fallback(self):
        if not self.special_items:
            return
        for idx, spec in enumerate(self.special_items):
            title = str(spec.get("title", "")).strip()
            if not title:
                continue
            icon = self._special_icon(spec.get("icon", "new"))
            item = legacy.QListWidgetItem(icon, title)
            item.setData(legacy.Qt.UserRole, "")
            item.setData(legacy.Qt.UserRole + 1, dict(spec))
            tip = str(spec.get("tooltip", title)).strip()
            item.setToolTip(tip)
            self.insertItem(idx, item)

    def refresh(self):
        super().refresh()
        if not getattr(self, "_legacy_supports_special_items", False):
            self._add_special_items_fallback()

    def _run_selected(self):
        it = self.currentItem()
        if it is not None:
            spec = it.data(legacy.Qt.UserRole + 1)
            if isinstance(spec, dict) and spec.get("action"):
                self._dispatch_special_action(spec)
                return
        return super()._run_selected()

    def _on_item_double_clicked(self, item):
        try:
            spec = item.data(legacy.Qt.UserRole + 1)
            if isinstance(spec, dict) and spec.get("action"):
                self._dispatch_special_action(spec)
                return
        except Exception:
            pass
        return super()._on_item_double_clicked(item)

# -----------------------------------------------------------------------
# RegieCenter mit Sprachprofil statt fest verdrahtetem .prg-Filter.
# -----------------------------------------------------------------------
class ProfiledRegieCenter(legacy.QDialog):
    def __init__(self, profile: LanguageProfile, parent=None):
        super().__init__(parent)
        self.language_profile = profile
        legacy.mark_escape_close(self)

        self.setFont(legacy.QFont("Arial", 10))
        self.setWindowTitle(f"{profile.display_name} RegieCenter")
        self.setModal(False)
        self.setWindowModality(legacy.Qt.NonModal)

        self.icon_provider = legacy.QFileIconProvider()

        self.combo = legacy.QComboBox()
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(legacy.QComboBox.NoInsert)
        self.combo.currentTextChanged.connect(self._on_dir_changed)

        self.btn_pick = legacy.QPushButton("Verzeichnis…")
        self.btn_pick.clicked.connect(self.pick_directory_non_native)

        top = legacy.QHBoxLayout()
        top.addWidget(self.combo, 1)
        top.addWidget(self.btn_pick, 0)

        self.tabs = legacy.QTabWidget()
        self.icon_lists = []

        ext_programme = list(profile.program_extensions)
        ext_alltypes = [
            ".htm", ".html", ".css", ".js", ".url",
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico",
            ".sql",
            ".dbf", ".csv", ".xlsx", ".xls",
            ".rep", ".rpt", ".report",
            ".frm", ".form", ".wfm",
            ".dpr", ".prj", ".proj", ".project",
            ".prg",
            *ext_programme,
        ]
        ext_alltypes  = list(dict.fromkeys(e.lower() for e in ext_alltypes))
        ext_projekte  = [".pro", ".dpr", ".prj", ".proj", ".project"]
        ext_formulare = [".frm", ".form", ".wfm"]
        ext_berichte  = [".rep", ".rpt", ".report"]
        ext_tabellen  = [".dbf", ".csv", ".xlsx", ".xls"]
        ext_sql       = [".sql"]
        ext_grafiken  = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"]
        ext_internet  = [".htm", ".html", ".css", ".js", ".url"]

        self.lw1 = ProfiledIconTab(profile, ext_alltypes, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw1); self.tabs.addTab(self.lw1, "Alle Typen")
        #self.lw2 = ProfiledIconTab(profile, ext_projekte, parent=self, icon_provider=self.icon_provider, special_items=[{'title':'Neues Projekt','action':'new_project','icon':'project','tooltip':'Neues Projekt anlegen'}])
        
        self.lw2 = ProfiledIconTab(
            profile, ext_projekte,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "Projekte",
            special_items = [{
                "title"   : "Neu Projekt",
                "action"  : "new_project",
                "icon"    : "project",
                "tooltip" : "Neues Projekt anlegen",
            }])
        self.tabs.addTab(self.lw2, "Projekte")
        self.icon_lists.append(self.lw2)
        # ---------------------------------------------------
        self.lw3 = ProfiledIconTab(
            profile, ext_programme,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = profile.program_tab_title,
            special_items = [{
                "title"   : "Neu Programm",
                "action"  : "new_program",
                "icon"    : "form",
                "tooltip" : "Neues Programm anlegen",
            }])
        self.tabs.addTab(self.lw3, "Programm")
        self.icon_lists.append(self.lw3)
        # ---------------------------------------------------
        self.lw4 = ProfiledIconTab(
            profile, ext_formulare,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "Formulare",
            special_items = [{
                "title"   : "Neu Designer",
                "action"  : "new_form_designer",
                "icon"    : "form",
                "tooltip" : "Neues Formular im Design-Modus anlegen",
            },{
                "title"   : "Neu Experte",
                "action"  : "new_form_expert",
                "icon"    : "form",
                "tooltip" : "Neues Formular im Experten-Modus anlegen",
            }])
        self.tabs.addTab(self.lw4, "Formular")
        self.icon_lists.append(self.lw4)
        # ---------------------------------------------------
        self.lw5 = ProfiledIconTab(
            profile, ext_tabellen,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "Tabellen",
            special_items = [{
                "title"   : "Neu Designer",
                "action"  : "new_table_designer",
                "icon"    : "form",
                "tooltip" : "Neu Tabelle im Design-Modus anlegen",
            },{
                "title"   : "Neu Experte",
                "action"  : "new_table_expert",
                "icon"    : "form",
                "tooltip" : "Neu Tabelle im Experten-Modus anlegen",
            }])
        self.tabs.addTab(self.lw5, "Tabellen")
        self.icon_lists.append(self.lw5)
        # ---------------------------------------------------
        self.lw6 = ProfiledIconTab(
            profile, ext_sql,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "SQL",
            special_items = [{
                "title"   : "Neu SQL",
                "action"  : "new_sql_designer",
                "icon"    : "form",
                "tooltip" : "Neue Abfrage anlegen",
            }])
        self.tabs.addTab(self.lw6, "SQL")
        self.icon_lists.append(self.lw6)
        # ---------------------------------------------------
        self.lw7 = ProfiledIconTab(
            profile, ext_berichte,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "Berichte",
            special_items = [{
                "title"   : "Neu Bericht",
                "action"  : "new_report",
                "icon"    : "form",
                "tooltip" : "Neuen Bericht anlegen",
            }])
        self.tabs.addTab(self.lw7, "Berichte")
        self.icon_lists.append(self.lw7)
        # ---------------------------------------------------
        self.lw8 = ProfiledIconTab(
            profile, ext_grafiken,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "Grafiken",
            special_items = [{
                "title"   : "Neu Grafik",
                "action"  : "new_graphic",
                "icon"    : "form",
                "tooltip" : "Neue Grafik anlegen",
            }])
        self.tabs.addTab(self.lw8, "Grafiken")
        self.icon_lists.append(self.lw8)
        # ---------------------------------------------------
        self.lw9 = ProfiledIconTab(
            profile, ext_internet,
            parent        = self,
            icon_provider = self.icon_provider,
            tab_name      = "Internet",
            special_items = [{
                "title"   : "Neu HTML",
                "action"  : "new_webdoc_html",
                "icon"    : "form",
                "tooltip" : "Neues HTML-Dokument anlegen",
            },{
                "title"   : "Neu CSS",
                "action"  : "new_webdoc_css",
                "icon"    : "form",
                "tooltip" : "Neues CSS-Dokument anlegen",
            },{
                "title"   : "Neu JavaScript",
                "action"  : "new_webdoc_js",
                "icon"    : "form",
                "tooltip" : "Neues JavaScript-Dokument anlegen",
            }])
        self.tabs.addTab(self.lw9, "Internet")
        self.icon_lists.append(self.lw9)
        # ---------------------------------------------------
        
        ext_all_known = (
            ext_projekte + ext_formulare + ext_berichte + ext_programme +
            ext_tabellen + ext_sql + ext_grafiken + ext_internet
        )
        self.lwA = ProfiledIconTab(profile, exclude_exts=ext_all_known, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lwA); self.tabs.addTab(self.lwA, "Sonstiges")

        root = legacy.QVBoxLayout(self)
        root.addLayout(top)
        root.addWidget(self.tabs, 1)

        try:
            for lw in self.icon_lists:
                lw.refresh()
        except Exception:
            pass

        try:
            self._restore_recent_dirs()
        except Exception:
            pass

        self.resize(980, 640)

    def _save_recent_dirs(self, current_path: str):
        try:
            if 'MAINAPP' not in globals() or not hasattr(MAINAPP, '_settings'):
                return

            current_path = (current_path or "").strip()
            items = []

            if current_path and os.path.isdir(current_path):
                items.append(current_path)

            for i in range(self.combo.count()):
                txt = (self.combo.itemText(i) or "").strip()
                if txt and os.path.isdir(txt) and txt not in items:
                    items.append(txt)

            items = items[:15]

            MAINAPP._settings.setValue("regiecenter/recent_dirs", items)
            MAINAPP._settings.setValue("regiecenter/workdir", current_path)
        except Exception:
            pass
            
    # Reuse legacy methods without duplication.
    open_in_table_editor = legacy.RegieCenter.open_in_table_editor
    open_in_code_editor = legacy.RegieCenter.open_in_code_editor
    pick_directory_non_native = legacy.RegieCenter.pick_directory_non_native
    _add_and_select_dir = legacy.RegieCenter._add_and_select_dir
    _restore_recent_dirs = legacy.RegieCenter._restore_recent_dirs
    _on_dir_changed = legacy.RegieCenter._on_dir_changed
    run_source_file: Callable[[str], None] | None = None


class ProfiledMainWindow(legacy.MainWindow):
    def __init__(self, profile: LanguageProfile):
        self.language_profile = profile
        super().__init__()
        self._apply_language_profile()

    def _apply_language_profile(self) -> None:
        try:
            self.setWindowTitle(self.language_profile.app_title)
        except Exception:
            pass

        try:
            regie = getattr(self, "regie_center", None)
            if regie is not None:
                regie.setWindowTitle(f"{self.language_profile.display_name} RegieCenter")
                # Laufroutine als Hook für ProfiledIconTab.
                regie.run_source_file = self.run_source_file
        except Exception:
            pass

    def run_source_file(self, path: str) -> None:
        ext = Path(path).suffix.lower()
        if ext == ".prg":
            legacy.parse(path)
            return

        legacy.QMessageBox.information(
            self,
            self.language_profile.display_name,
            f"Die Datei {os.path.basename(path)} wurde erkannt.\n\n"
            f"Die Oberfläche ist bereits auf {self.language_profile.display_name} umgestellt, "
            f"aber der Parser/Lexer für {self.language_profile.program_extensions_label} "
            "ist noch nicht angebunden.",
        )

    def on_action_file_open(self):
        dlg = legacy.QFileDialog(self, legacy._tr("Open File..."))
        dlg.setFileMode(legacy.QFileDialog.ExistingFile)
        filters = [self.language_profile.program_name_filter, "Alle Dateien (*.*)"]
        dlg.setNameFilters(filters)
        dlg.setDefaultSuffix(self.language_profile.default_source_extension.lstrip("."))
        dlg.setOption(legacy.QFileDialog.DontUseNativeDialog, True)
        if not dlg.exec_():
            return
        files = dlg.selectedFiles()
        if not files:
            return
        path = files[0]

        sub = self.mdi.activeSubWindow()
        win = sub.widget() if sub else None

        if isinstance(win, legacy.FileEditorWindow):
            win.open_path_in_tab(path)
            win.raise_()
            win.activateWindow()
            return

        try:
            new_win = legacy.FileEditorWindow(parent=self, initial_path="", initial_text="")
            subw = self.mdi.addSubWindow(new_win)
            legacy.mark_escape_close(subw)
            new_win.resize(700, 500)
            new_win.show()
            new_win.open_path_in_tab(path)
            self.mdi.setActiveSubWindow(subw)
        except Exception as exc:
            legacy.QMessageBox.critical(self, "Fehler", f"Konnte Editor nicht öffnen:\n{exc}")


def _bootstrap_qt_app(profile: LanguageProfile):
    legacy.APPINST = legacy.ensure_qt_app()
    if legacy.APPINST is None:
        raise RuntimeError("QApplication konnte nicht initialisiert werden.")

    try:
        legacy.APPINST.setApplicationName(profile.display_name)
    except Exception:
        pass

    try:
        legacy.APPINST.setStyle(legacy.ArrowFontProxyStyle(legacy.APPINST.style()))
    except Exception:
        pass

    return legacy.APPINST


def run_language_app(profile_key: str) -> int:
    profile = get_language_profile(profile_key)
    app = _bootstrap_qt_app(profile)

    original_regiecenter = legacy.RegieCenter

    try:
        def _factory(parent=None):
            return ProfiledRegieCenter(profile, parent=parent)

        legacy.RegieCenter = _factory
        legacy.MAINAPP = ProfiledMainWindow(profile)
        share.utildef.theme.apply_theme_global(legacy.MAINAPP)
        legacy.MAINAPP.show()
        legacy.center_on_screen(legacy.MAINAPP)
        rc = app.exec_()
        return int(rc)
    finally:
        legacy.RegieCenter = original_regiecenter
