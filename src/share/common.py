# ---------------------------------------------------------------------------
# \file  : common.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import os
import re

try:
    # -----------------------------------------------------------------------
    # import some internal used modules ...
    # -----------------------------------------------------------------------
    from dataclasses import dataclass, field
    from typing      import Dict, List, Optional, Union, Any, TextIO
    from pathlib     import Path
    from copy        import deepcopy
    
    # -----------------------------------------------------------------------
    # import modules to handle html files ...
    # -----------------------------------------------------------------------
    from html        import unescape
    from html.parser import HTMLParser
    
    # -----------------------------------------------------------------------
    # we use antlr4 for the lexer + parser generator ...
    # -----------------------------------------------------------------------
    from antlr4      import (
         InputStream, FileStream, CommonTokenStream, Token, Lexer,
         Parser, DFA, ParserRuleContext, ATNDeserializer,
         PredictionContextCache, ParseTreeListener, ParseTreeVisitor
    )
    from antlr4.error.ErrorListener import ErrorListener

    import share.utildef.sysinfo
    #from   share.utildef.sysinfo    import SystemInfo
    
    import mimetypes
    import ctypes

    import traceback
    import re
    import sys
    import pprint
    import datetime
    import time

    # -----------------------------------------------------------------------
    # i18n / gettext (mo inside zip: <lang>/LC_MESSAGES/dbase.mo)
    # -----------------------------------------------------------------------
    import io
    import zipfile
    import gettext
    import polib

    # -----------------------------------------------------------------------
    # needed module imports for chm help viewer ...
    # -----------------------------------------------------------------------
    import shutil
    import tempfile
    import subprocess

    import tempfile
    import contextlib

    # -----------------------------------------------------------------------
    # database module imports ....
    # -----------------------------------------------------------------------
    import json
    import sqlite3

    # -----------------------------------------------------------------------
    # Qt Backend Factory + Property Mapping
    # -----------------------------------------------------------------------
    from PyQt5.QtCore    import (
        QObject, Qt, QSocketNotifier, pyqtSignal, QEvent, QRect, QSize,
        QRegExp, QFileInfo, QPoint, QAbstractProxyModel, QModelIndex,
        QRegularExpression, QRectF, QPointF, qRegisterResourceData, QUrl,
        qUnregisterResourceData, qVersion, QSortFilterProxyModel, QByteArray,
        QTimer, qInstallMessageHandler, QMimeData, QDataStream, QIODevice,
        QBuffer, QSettings, QDateTime
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
        QScrollArea, QAbstractButton, QButtonGroup
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
    # -----------------------------------------------------------------------
    from share.excepts        import *
    from share.editors.editor import *

    # -----------------------------------------------------------------------
    # resources suff like icons, ...
    # -----------------------------------------------------------------------
    import resources_rc
    
    # -----------------------------------------------------------------------
    # debug log file beyond the exe application ...
    # -----------------------------------------------------------------------
    import faulthandler

    # -----------------------------------------------------------------------
    # PDF printer output for SET FORMAT / SET PRINT
    # reportlab is optional. If it is missing, we fall back to SCREEN output.
    # -----------------------------------------------------------------------
    _PDF_BACKEND_AVAILABLE = True
    _PDF_BACKEND_IMPORT_ERROR = None
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors as rl_colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfgen import canvas
    except ImportError as _pdf_import_error:
        A4 = None
        rl_colors = None
        pdfmetrics = None
        canvas = None
        _PDF_BACKEND_AVAILABLE = False
        _PDF_BACKEND_IMPORT_ERROR = _pdf_import_error

except ImportError as e:
    if SystemInfo.is_windows():
        ctypes.windll.user32.MessageBoxW(0, str(e), "Import Error:", 0)
        sys.exit(1)

except ModuleNotFoundError as e:
    name = f"Module could not be found: {e.name}."
    if SystemInfo.is_windows():
        ctypes.windll.user32.MessageBoxW(0, name, "Module Error:", 0)
        sys.exit()

except Exception as e:
    if SystemInfo.is_windows():
        ctypes.windll.user32.MessageBoxW(0, "A common Exception occur",
        "Exception", 0)
        print(e)
        sys.exit(1)


VERBOSE_CONSOLE = os.environ.get("DBASERUNNER_VERBOSE", "0") == "1"

ESCAPE_CLOSE_WINDOW_CLASSES   = set()
ESCAPE_BLOCKED_WINDOW_CLASSES = {
    "DebugConsoleWidget",
}
# Interne Alias-Namen fuer die Escape-Hilfsfunktionen.
# Die Resolver unten verwenden die underscored-Varianten.
_ESCAPE_CLOSE_WINDOW_CLASSES   = ESCAPE_CLOSE_WINDOW_CLASSES
_ESCAPE_BLOCKED_WINDOW_CLASSES = ESCAPE_BLOCKED_WINDOW_CLASSES

BASE = Path(getattr(sys, "_MEIPASS", Path(sys.argv[0]).resolve().parent))
LOG  = BASE / "webengine_crash.log"

MAINAPP = None

# ---------------------------------------------------------------------------
# DBF schema helpers
# ---------------------------------------------------------------------------
@dataclass
class DbfFieldSpec:
    name: str
    ftype: str
    length: int
    decimals: int
    offset: int = 0

@dataclass
class TocNode:
    title: str
    local: Optional[str] = None
    children: List["TocNode"] = field(default_factory=list)

@dataclass
class FontValue:
    obj      : QFont
    family   : str  = "Arial"
    size     : int  = 10
    bold     : bool = False
    italic   : bool = False
    underline: bool = False
    
def ensure_qt_app():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        app.setStyle(IconScrollBarStyle(app.style()))
    return app

# ---------------------------------------------------------------------------
# Runtime Datenstrukturen
# ---------------------------------------------------------------------------
@dataclass
class CompileError:
    line: int
    column: int
    message: str

@dataclass
class MethodDef:
    params: list[str]
    block_ctx: object   # BlockContext

@dataclass
class PPFrame:
    parent_active: bool
    this_active: bool
    saw_else: bool = False
    start_file: Path | None = None
    start_line: int | None = None
    kind: str | None = None
    name: str | None = None

@dataclass
class Frame:
    name: str = "<anon>"
    vars: dict[str, Any] = field(default_factory=dict)
    args: list[Any] = field(default_factory=list)     # DO ... WITH Argumente

@dataclass
class Macro:
    name: str
    params: list[str] | None  # None => object-like
    body: str

@dataclass
class Instance:
    class_name: str
    backend: Any = None   # Qt Object
    parent: Optional["Instance"] = None
    props: Dict[str, object] = field(default_factory=dict)
    children: Dict[str, "Instance"] = field(default_factory=dict)
    
    def get_prop(self, name: str) -> Any:
        return self.props.get(name.upper())

    def set_prop(self, name: str, value: Any):
        self.props[name.upper()] = value

    def __repr__(self) -> str:
        label = self.props.get("NAME") or self.props.get("TEXT") or self.class_name
        try:
            child_count = len(self.children or {})
        except Exception:
            child_count = 0
        return f"<Instance {self.class_name} {label!r} children={child_count}>"

    __str__ = __repr__
        
@dataclass
class Delegate:
    target: "Instance"
    method_name: str
    runner: Optional[object] = None

    def __call__(self, *args):
        if self.runner is None:
            raise RuntimeError("Delegate hat keinen runner")
        try:
            return self.runner.invoke_method(self.target, self.method_name, list(args), None)
        except ProgramAbortSignal:
            return None

    def __repr__(self) -> str:
        target_name = getattr(self.target, "class_name", "<unknown>")
        return f"<Delegate {target_name}.{self.method_name}>"

    __str__ = __repr__

@dataclass
class ClassDef:
    name: str
    parent: str | None = None
    methods: dict[str, object] = field(default_factory = dict)        # methodname -> MethodDeclContext
    default_props: dict[str, object] = field(default_factory = dict)  # defaults
    inits: list[object] = field(default_factory = list)
    
@dataclass
class BoundMethod:
    target: "Instance"
    name: str

# ---------------------------------------------------------------------------
# application states for global usage ...
# ---------------------------------------------------------------------------
class AppMode_State:
    dark   = True
    lang   = "de"
    domain = "dbase"
# ---------------------------------------------------------------------------
AppMode = AppMode_State()

def debug_print(*args, **kwargs):
    if not VERBOSE_CONSOLE:
        return
    try:
        builtins.print(*args, **kwargs)
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Walk up parent widgets to find a QMdiSubWindow wrapper (if any).
# ---------------------------------------------------------------------------
def find_mdi_subwindow(widget: Any):
    try:
        w = widget
        while w is not None:
            if isinstance(w, QMdiSubWindow):
                return w
            # QWidget has parentWidget(); fallback to QObject.parent()
            if hasattr(w, "parentWidget"):
                w = w.parentWidget()
            else:
                w = w.parent()
        return None
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Robuster Fallback fuer eingebettete QDialog/QWidget-Faelle im MDI.
# ---------------------------------------------------------------------------
def find_mdi_subwindow_robust(widget: Any):
    sub = find_mdi_subwindow(widget)
    if sub is not None:
        return sub

    try:
        if isinstance(widget, QWidget):
            w = widget.window()
            sub = find_mdi_subwindow(w)
            if sub is not None:
                return sub
    except Exception:
        pass

    try:
        aw = QApplication.activeWindow()
        sub = find_mdi_subwindow(aw)
        if sub is not None:
            return sub
    except Exception:
        pass

    try:
        if 'MAINAPP' in globals() and getattr(MAINAPP, 'mdi', None) is not None:
            sub = MAINAPP.mdi.activeSubWindow()
            if sub is not None:
                return sub
    except Exception:
        pass

    return None

# Rueckwaertskompatibler Alias fuer aeltere Aufrufe.
_find_mdi_subwindow_robust = find_mdi_subwindow_robust


def mark_escape_protected(obj: Any) -> Any:
    try:
        if obj is not None and hasattr(obj, "setProperty"):
            obj.setProperty("ESCAPE_BLOCKED", True)
    except Exception:
        pass
    return obj


def resolve_escape_block_target(widget: Any):
    try:
        w = widget if isinstance(widget, QWidget) else QApplication.focusWidget()
    except Exception:
        w = None

    while w is not None:
        try:
            if bool(w.property("ESCAPE_BLOCKED")) or w.__class__.__name__ in _ESCAPE_BLOCKED_WINDOW_CLASSES:
                sub = find_mdi_subwindow_robust(w)
                return w, sub
        except Exception:
            pass
        try:
            w = w.parentWidget()
        except Exception:
            try:
                w = w.parent()
            except Exception:
                w = None

    return None, None

def resolve_escape_close_target(widget: Any):
    try:
        w = widget if isinstance(widget, QWidget) else QApplication.focusWidget()
    except Exception:
        w = None

    while w is not None:
        try:
            if bool(w.property("ESCAPE_CLOSE")) or w.__class__.__name__ in _ESCAPE_CLOSE_WINDOW_CLASSES:
                sub = find_mdi_subwindow_robust(w)
                return w, sub
        except Exception:
            pass
        try:
            w = w.parentWidget()
        except Exception:
            try:
                w = w.parent()
            except Exception:
                w = None

    return None, None


def resolve_escape_target(widget: Any):
    try:
        w = widget if isinstance(widget, QWidget) else QApplication.focusWidget()
    except Exception:
        w = None

    while w is not None:
        try:
            if bool(w.property("_DBASE_ESCAPE_TARGET")):
                sub = find_mdi_subwindow_robust(w)
                return w, sub
        except Exception:
            pass
        try:
            w = w.parentWidget()
        except Exception:
            try:
                w = w.parent()
            except Exception:
                w = None

    return None, None

# ---------------------------------------------------------------------------
# Schliesst robust ein komplettes MDI-Unterfenster inklusive eingebettetem
# Widget.
# ---------------------------------------------------------------------------
def close_escape_target(widget: Any, sub: Any = None) -> bool:
    try:
        if sub is None:
            sub = find_mdi_subwindow_robust(widget)
    except Exception:
        sub = None

    try:
        host_sub = sub
        if host_sub is not None:
            try:
                inner = host_sub.widget()
            except Exception:
                inner = None
            try:
                host_sub.setAttribute(Qt.WA_DeleteOnClose, True)
            except Exception:
                pass
            try:
                if inner is not None:
                    inner.setAttribute(Qt.WA_DeleteOnClose, True)
            except Exception:
                pass

            try:
                host_sub.close()
            except Exception:
                try:
                    host_sub.hide()
                except Exception:
                    pass
            try:
                host_sub.deleteLater()
            except Exception:
                pass
            return True

        if widget is not None:
            try:
                widget.setAttribute(Qt.WA_DeleteOnClose, True)
            except Exception:
                pass
            try:
                widget.close()
            except Exception:
                try:
                    widget.hide()
                except Exception:
                    pass
            try:
                widget.deleteLater()
            except Exception:
                pass
            return True
    except Exception:
        return False

    return False
