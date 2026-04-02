# ---------------------------------------------------------------------------
# \file  : app.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import os
from pathlib import Path
from typing  import Callable

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


class ProfiledIconTab(legacy.IconTab):
    """Sprachspezifischer Wrapper um die bestehende IconTab-Implementierung."""

    def __init__(self, profile: LanguageProfile, *args, **kwargs):
        self.language_profile = profile
        super().__init__(*args, **kwargs)

    def _new_program(self):
        directory = (getattr(self, "base_dir", "") or "").strip()
        if not directory or not os.path.isdir(directory):
            legacy.QMessageBox.information(self, "Neu", "Bitte zuerst ein Verzeichnis auswählen.")
            return

        ext = self.language_profile.default_source_extension
        path = self._unique_name_in_dir(directory, "unbenannt", ext)
        if not path:
            return

        try:
            text = self.language_profile.new_file_template or ""
            with open(path, "w", encoding="utf-8", errors="replace") as handle:
                handle.write(text)
        except Exception as exc:
            legacy.QMessageBox.warning(self, "Neu", f"Konnte Datei nicht erstellen:\n{exc}")
            return

        self._refresh_all_icon_tabs()

        host = self._regiecenter_host()
        if host is not None and hasattr(host, "open_in_code_editor"):
            host.open_in_code_editor(display_name=os.path.basename(path), path=path)

    def _edit_in_editor(self, path: str) -> None:
        try:
            ext = os.path.splitext(path)[1].lower()
            if not (self.language_profile.matches_extension(ext) or ext == ".dbf"):
                return

            display_name = os.path.basename(path)
            host = self.parent()

            if self.language_profile.matches_extension(ext):
                while host is not None and not hasattr(host, "open_in_code_editor"):
                    host = host.parent()
                if host is not None and hasattr(host, "open_in_code_editor"):
                    host.open_in_code_editor(display_name=display_name, path=path)
                else:
                    legacy.QMessageBox.information(self, "Bearbeiten", "Kein CodeEditor-Hook gefunden.")
                return

            if ext == ".dbf":
                while host is not None and not hasattr(host, "open_in_table_editor"):
                    host = host.parent()
                if host is not None and hasattr(host, "open_in_table_editor"):
                    host.open_in_table_editor(display_name=display_name, path=path)
                else:
                    legacy.QMessageBox.information(self, "Bearbeiten", "Kein TabellenEditor-Hook gefunden.")
        except Exception as exc:
            legacy.QMessageBox.warning(self, "Bearbeiten", f"Konnte Editor nicht öffnen:\n{exc}")

    def _run_file(self, path: str):
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".dbf":
                self._edit_in_editor(path)
                return

            if ext == ".prg":
                legacy.parse(path)
                return

            if self.language_profile.matches_extension(ext):
                host = self._regiecenter_host()
                if host is not None and hasattr(host, "run_source_file"):
                    host.run_source_file(path)
                    return
                legacy.QMessageBox.information(
                    self,
                    self.language_profile.display_name,
                    "Für diese Sprache ist der neue Parser/Lexer noch nicht verdrahtet. "
                    "Die Oberfläche funktioniert bereits, die Laufzeitlogik ist noch Platzhalter.",
                )
                return
        except Exception as exc:
            legacy.QMessageBox.warning(self, "Ausführen", f"Konnte Datei nicht starten:\n{exc}")


class ProfiledRegieCenter(legacy.QDialog):
    """RegieCenter mit Sprachprofil statt fest verdrahtetem .prg-Filter."""

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
        ext_alltypes = list(dict.fromkeys(e.lower() for e in ext_alltypes))
        ext_projekte = [".dpr", ".prj", ".proj", ".project"]
        ext_formulare = [".frm", ".form", ".wfm"]
        ext_berichte = [".rep", ".rpt", ".report"]
        ext_tabellen = [".dbf", ".csv", ".xlsx", ".xls"]
        ext_sql = [".sql"]
        ext_grafiken = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"]
        ext_internet = [".htm", ".html", ".css", ".js", ".url"]

        self.lw1 = ProfiledIconTab(profile, ext_alltypes, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw1); self.tabs.addTab(self.lw1, "Alle Typen")
        self.lw2 = ProfiledIconTab(profile, ext_projekte, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw2); self.tabs.addTab(self.lw2, "Projekte")
        self.lw3 = ProfiledIconTab(profile, ext_programme, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw3); self.tabs.addTab(self.lw3, profile.program_tab_title)
        self.lw4 = ProfiledIconTab(profile, ext_formulare, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw4); self.tabs.addTab(self.lw4, "Formulare")
        self.lw5 = ProfiledIconTab(profile, ext_tabellen, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw5); self.tabs.addTab(self.lw5, "Tabellen")
        self.lw6 = ProfiledIconTab(profile, ext_sql, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw6); self.tabs.addTab(self.lw6, "SQL")
        self.lw7 = ProfiledIconTab(profile, ext_berichte, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw7); self.tabs.addTab(self.lw7, "Berichte")
        self.lw8 = ProfiledIconTab(profile, ext_grafiken, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw8); self.tabs.addTab(self.lw8, "Grafiken")
        self.lw9 = ProfiledIconTab(profile, ext_internet, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw9); self.tabs.addTab(self.lw9, "Internet")

        ext_all_known = (
            ext_projekte + ext_formulare + ext_berichte + ext_programme +
            ext_tabellen + ext_sql + ext_grafiken + ext_internet
        )
        self.lwA = ProfiledIconTab(profile, exclude_exts=ext_all_known, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lwA); self.tabs.addTab(self.lwA, "Sonstiges")

        root = legacy.QVBoxLayout(self)
        root.addLayout(top)
        root.addWidget(self.tabs, 1)
        self.resize(980, 640)

    # Reuse legacy methods without duplication.
    open_in_table_editor = legacy.RegieCenter.open_in_table_editor
    open_in_code_editor = legacy.RegieCenter.open_in_code_editor
    pick_directory_non_native = legacy.RegieCenter.pick_directory_non_native
    _add_and_select_dir = legacy.RegieCenter._add_and_select_dir
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
        legacy.MAINAPP.show()
        legacy.center_on_screen(legacy.MAINAPP)
        rc = app.exec_()
        return int(rc)
    finally:
        legacy.RegieCenter = original_regiecenter
