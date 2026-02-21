# ---------------------------------------------------------------------------
# File:   dBaseRunner.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from antlr4      import (
     InputStream, FileStream, CommonTokenStream, Token, Lexer, Parser, DFA,
     ParserRuleContext, ATNDeserializer, PredictionContextCache,
     ParseTreeListener, ParseTreeVisitor
)
from dataclasses import dataclass, field
from typing      import Dict, List, Optional, Union, Any, TextIO
from pathlib     import Path
from copy        import deepcopy

#from gen.dBaseLexer         import dBaseLexer
#from gen.dBaseParser        import dBaseParser
#from gen.dBaseParserVisitor import dBaseParserVisitor

import traceback
import sys
import os
import re
import pprint

# ---------------------------------------------------------------------------
# Qt Backend Factory + Property Mapping
# ---------------------------------------------------------------------------
from PyQt5.QtCore    import (
    QObject, Qt, QSocketNotifier, pyqtSignal, QEvent, QRect, QSize, QRegExp,
    QFileInfo, QPoint, QAbstractProxyModel, QModelIndex, QRegularExpression,
    QRectF, QPointF, qRegisterResourceData, qUnregisterResourceData, qVersion
)
from PyQt5.QtGui     import (
    QFont, QPainter, QFontMetrics, QSyntaxHighlighter, QTextCharFormat,
    QColor, QStandardItemModel, QStandardItem, QIcon, QFontInfo,
    QFontDatabase, QRegularExpressionValidator, QIntValidator, QPainterPath,
    QLinearGradient, QRadialGradient, QPen, QKeySequence, QPalette,
    QTextFormat
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QPushButton, QVBoxLayout,
    QTextEdit, QToolBar, QStatusBar, QMessageBox, QPlainTextEdit, QAction,
    QFileDialog, QMenuBar, QMdiArea, QMdiSubWindow, QTreeView, QSplitter,
    QHBoxLayout, QComboBox, QTabWidget, QListWidget, QListWidgetItem,
    QMenu, QFileDialog, QFileIconProvider, QListWidget, QTableWidget,
    QTableWidgetItem, QHeaderView, QStyledItemDelegate, QGroupBox, QLabel,
    QLineEdit, QCheckBox, QRadioButton, QSpacerItem, QGridLayout, QSpinBox,
    QSizePolicy, QStyleOptionHeader, QStyle, QTableView, QAbstractItemView,
    QStyleOptionComplex, QProxyStyle
)

TYPE_VALUES = [
    "Character",
    "Numeric",
    "Float",
    "Integer",
    "Date",
    "DateTime",
    "Logical",
    "Memo",
]

NATIVE_BASES = {
    "FORM": QDialog,          # oder QDialog, wenn FORM per default Dialog sein soll
    "DIALOG": QDialog,
    "PUSHBUTTON": QPushButton,
}

# ---------------------------------------------------------------------------
# Scrollbars (global)
# ---------------------------------------------------------------------------
APP_DARK_QSS = r"""/*VERTICAL*/
QScrollBar:vertical {background:#081a33;/*navy*/width:16px;/*Breite*/margin:16px 0 16px 0;/*Platz für Buttons oben/unten*/border:1px solid #0f2a4a;}
QScrollBar::handle:vertical {background:#2b6cb0;/*normales Blau*/border:1px solid #163a66;border-radius:6px;min-height:26px;/*nie kleiner*/max-height:26px;/*nie größer (fix 26px)*/}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{background:#061226;/*etwas dunkler*/height:16px;/*Button-Höhe*/border:1px solid #0f2a4a;}
QScrollBar::sub-line:vertical{/*oben*/subcontrol-origin:margin;subcontrol-position:top;}
QScrollBar::add-line:vertical{/*unten*/subcontrol-origin:margin;subcontrol-position:bottom;}
/*Pfeile (ohne Bilder): simple “Chevron”-Optik über Farben*/
QScrollBar::up-arrow:vertical,QScrollBar::down-arrow:vertical{width:8px;height:8px;background:#c9b458;/*gelb – gut sichtbar*/border-radius:2px;}
QScrollBar::up-arrow:vertical{margin-top:3px;}
QScrollBar::down-arrow:vertical{margin-bottom:3px;}
/*Track-Bereiche*/
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical{background: transparent;}
/*HORIZONTAL*/
QScrollBar:horizontal {background:#081a33;/*navy*/height:16px;/*Höhe*/margin:0 16px 0 16px;/*Platz für Buttons links/rechts*/border:1px solid #0f2a4a;}
QScrollBar::handle:horizontal{background:#2b6cb0;border:1px solid #163a66;border-radius:6px;min-width:26px;max-width:26px;/*fix 26px breit*/}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{background:#061226;width:16px;/*Button-Breite*/border:1px solid #0f2a4a;}
QScrollBar::sub-line:horizontal{/*links*/subcontrol-origin:margin;subcontrol-position:left;}
QScrollBar::add-line:horizontal{/*rechts*/subcontrol-origin:margin;subcontrol-position:right;}
QScrollBar::left-arrow:horizontal,QScrollBar::right-arrow:horizontal{width:8px;height:8px;background:#c9b458;border-radius:2px;}
QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal{background:transparent;}
/* Toolbar */
QToolBar{background:#1e1f22;/*dunkelgrau*/border:1px solid #2b2d31;spacing:6px;padding:4px;}
QToolBar::separator{background:#2b2d31;width:1px;margin:6px 4px;}
/* ToolButtons (Icons/Buttons in der Toolbar) */
QToolButton{background: transparent;color:#c9b458;/*gelb*/border:1px solid transparent;padding:4px 6px;border-radius:6px;}
QToolButton:hover{background:#2b2d31;border-color:#3a3d45;}
QToolButton:pressed{background:#343740;}
/* Statusbar */
QStatusBar{background:#1e1f22;border-top:1px solid #2b2d31;}
QStatusBar QLabel{color:#c9b458;padding:0 6px;}
QStatusBar::item{border: none;/*keine extra Boxen*/}"""

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
    props: Dict[str, object] = field(default_factory=dict)
    children: Dict[str, "Instance"] = field(default_factory=dict)
    
    def get_prop(self, name: str) -> Any:
        return self.props.get(name.upper())

    def set_prop(self, name: str, value: Any):
        self.props[name.upper()] = value
        
@dataclass
class Delegate:
    target: "Instance"
    method_name: str
    runner: Optional[object] = None

    def __call__(self, *args):
        if self.runner is None:
            raise RuntimeError("Delegate hat keinen runner")
        return self.runner.invoke_method(self.target, self.method_name, list(args), None)

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
#    obj: object
#    method: MethodDef
#    runner: object  # z.B. dein Visitor/Runner, der Blöcke ausführt
#
#    def __call__(self, *args):
#        # self/this vorne dran, wenn du OOP so modellierst:
#        return self.runner.call_method(self.obj, self.method, list(args))

# ---- Exceptions -------------------------------------------------------------
class ReturnSignal(Exception):
    def __init__(self, value=None, has_value: bool = False):
        super().__init__(self, value)
        self.value = value
        self.has_value = has_value

class UnterminatedBlockCommentError(Exception):
    def __init__(self, line, column, message="unterminated block comment"):
        super().__init__(f"{line}:{column}: {message}")
        self.line    = line
        self.column  = column
        self.message = message

class KeyError(Exception):
    def __init__(self, name, message="Zuordnungs-Fehler"):
        super().__init__(self, name)
        self.name    = name
        self.message = message

class BreakSignal(Exception):
    """Interner Control-Flow für BREAK (nur Schleifen fangen das ab)."""
    pass

class PreprocessorError(Exception):
    pass

# Interner Control-Flow für RETURN aus einer Methode.
class RuntimeReturn(Exception):
    def __init__(self, value=None):
        self.value = value

# ---- Resources (icons, ...) -------------------------------------------------
# -*- coding: utf-8 -*-

# Resource object code
#
# Created by: The Resource Compiler for PyQt5 (Qt v5.15.2)
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore

qt_resource_data = b"\
\x00\x00\x05\x29\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x31\x00\x00\x00\x3a\x08\x06\x00\x00\x00\x19\x5b\xb1\xdf\
\x00\x00\x01\x85\x69\x43\x43\x50\x49\x43\x43\x20\x70\x72\x6f\x66\
\x69\x6c\x65\x00\x00\x28\x91\x7d\x91\xbd\x4b\xc3\x50\x14\xc5\x4f\
\x53\x8b\x22\x55\x41\x3b\x88\x88\x64\xa8\x4e\x76\x51\x11\xc7\x52\
\xc5\x22\x58\x28\x6d\x85\x56\x1d\x4c\x5e\xfa\x05\x4d\x1a\x92\x14\
\x17\x47\xc1\xb5\xe0\xe0\xc7\x62\xd5\xc1\xc5\x59\x57\x07\x57\x41\
\x10\xfc\x00\xf1\x0f\x10\x27\x45\x17\x29\xf1\xbe\xa4\xd0\x22\xc6\
\x0b\x8f\xf7\xe3\xbc\x7b\x0e\xef\xdd\x07\x08\x8d\x0a\x53\xcd\xae\
\x28\xa0\x6a\x96\x91\x8a\xc7\xc4\x6c\x6e\x55\xec\x7e\x85\x0f\x83\
\xe8\x47\x00\x63\x12\x33\xf5\x44\x7a\x31\x03\xcf\xfa\xba\xa7\x6e\
\xaa\xbb\x08\xcf\xf2\xee\xfb\xb3\xfa\x94\xbc\xc9\x00\x9f\x48\x1c\
\x65\xba\x61\x11\x6f\x10\xcf\x6e\x5a\x3a\xe7\x7d\xe2\x10\x2b\x49\
\x0a\xf1\x39\xf1\xa4\x41\x17\x24\x7e\xe4\xba\xec\xf2\x1b\xe7\xa2\
\xc3\x02\xcf\x0c\x19\x99\xd4\x3c\x71\x88\x58\x2c\x76\xb0\xdc\xc1\
\xac\x64\xa8\xc4\x33\xc4\x61\x45\xd5\x28\x5f\xc8\xba\xac\x70\xde\
\xe2\xac\x56\x6a\xac\x75\x4f\xfe\xc2\x60\x5e\x5b\x49\x73\x9d\xd6\
\x28\xe2\x58\x42\x02\x49\x88\x90\x51\x43\x19\x15\x58\x88\xd0\xae\
\x91\x62\x22\x45\xe7\x31\x0f\xff\x88\xe3\x4f\x92\x4b\x26\x57\x19\
\x8c\x1c\x0b\xa8\x42\x85\xe4\xf8\xc1\xff\xe0\xf7\x6c\xcd\xc2\xf4\
\x94\x9b\x14\x8c\x01\x81\x17\xdb\xfe\x18\x07\xba\x77\x81\x66\xdd\
\xb6\xbf\x8f\x6d\xbb\x79\x02\xf8\x9f\x81\x2b\xad\xed\xaf\x36\x80\
\xb9\x4f\xd2\xeb\x6d\x2d\x7c\x04\x0c\x6c\x03\x17\xd7\x6d\x4d\xde\
\x03\x2e\x77\x80\xe1\x27\x5d\x32\x24\x47\xf2\xd3\x12\x0a\x05\xe0\
\xfd\x8c\xbe\x29\x07\x0c\xdd\x02\xbd\x6b\xee\xdc\x5a\xe7\x38\x7d\
\x00\x32\x34\xab\xe5\x1b\xe0\xe0\x10\x98\x28\x52\xf6\xba\xc7\xbb\
\x7b\x3a\xe7\xf6\x6f\x4f\x6b\x7e\x3f\x6c\xb4\x72\xa4\x74\x35\xf5\
\x28\x00\x00\x00\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff\xa0\
\xbd\xa7\x93\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x2e\x23\x00\
\x00\x2e\x23\x01\x78\xa5\x3f\x76\x00\x00\x03\x38\x49\x44\x41\x54\
\x68\xde\xed\x5a\xcd\x4e\x14\x41\x18\xac\xee\x99\x45\x8d\x28\xe0\
\x4a\xc8\x92\x28\x5c\x4c\x44\x24\xde\x3d\x68\xf4\xea\xab\xf8\x22\
\x3e\x81\x6f\xe1\xd5\x83\xf1\xa0\x57\x8d\x22\x11\x31\xc1\x88\x62\
\xb2\x04\x05\xf6\x82\x71\x23\x4c\x97\x87\x65\x75\xd5\xee\x99\xfe\
\xf9\x06\xc1\x6c\x27\x9b\x4d\x66\xa6\x67\xaa\xfa\xab\xfa\xbe\xee\
\x9e\x51\x00\x88\x63\xde\x34\xfe\x83\x36\x24\x31\x24\x21\xd8\x72\
\xdb\xc1\x7b\x0f\x96\xb1\xdb\xdd\x3b\x54\x20\xb7\x17\x5a\xb8\xb5\
\x30\x25\x47\xa2\x30\x06\x77\xef\x5c\xc6\xd9\x53\x8d\x5f\x07\x23\
\x73\x58\x55\x37\xa5\x80\x47\x8b\x6d\x3c\x5e\xda\xc0\xd3\xe5\x4d\
\xdc\x98\x9f\x92\x21\x01\x00\x23\xb9\xc6\x48\xae\xed\x80\x18\x07\
\xd8\x76\x9d\x56\x40\xa6\x35\x9a\xa3\x27\xf0\xf2\xfd\x4e\x14\x91\
\xbc\xf4\x61\xfc\x1b\x18\x03\x51\x57\x5e\xa2\x7a\x7f\x57\x66\xc6\
\x71\xe6\x64\x03\xcf\xdf\x6d\x05\x13\xa9\x24\x61\x42\x40\x32\x9c\
\x90\x3e\x38\x98\x6b\x8d\xab\xb3\x13\x20\x80\x17\x81\x44\x4a\x49\
\x98\x03\x22\x31\x96\xa0\x07\x31\x0e\x9c\x26\x7a\xb2\x9a\xbf\x38\
\x01\x1a\x62\x71\xcd\x5f\x5a\xe5\x24\xfa\x72\xa2\x8c\xfe\xad\x07\
\x39\x20\x5d\x02\x59\xa6\x31\x37\x73\x0e\x06\xc0\xd2\x87\x1d\x3c\
\x59\xde\xc4\xcd\x0a\x22\x79\x15\x00\xc3\x30\xf4\x0c\x24\x46\xcb\
\xb3\x1a\x99\xc6\xdc\x85\x9e\xb4\x5e\x7f\xac\x8e\x48\xb5\xb1\x5d\
\x51\x60\x42\x24\x2c\xe7\x9f\xad\x7e\xc1\x9b\xf5\xce\x6f\xe7\xba\
\x7b\x05\xbe\x76\xf7\xd1\xd9\xfd\x5c\x4a\xc4\x8b\x04\x85\xf4\xef\
\x6a\xd7\xe7\x26\xb1\x30\x3b\xee\x3c\xff\x6a\xad\x83\xf5\x8d\xad\
\x78\x4f\x0c\xca\x89\xe2\xc6\x26\xbe\xed\x01\x3a\xcb\x31\x36\x6a\
\x87\x32\x92\x29\x8c\x9d\xde\xc5\xf6\xf6\x3e\xda\xed\x36\xa6\xa7\
\xa7\xc3\xb3\x93\xa1\xeb\xf1\x81\xd9\xca\xd1\xa1\x20\x50\x94\xf4\
\xcb\x34\xd3\xb2\x13\x49\xeb\x88\xa6\xae\xa2\x18\x9b\x05\xa4\x8c\
\xcd\x44\x26\x0c\xbc\xc0\xe7\x31\x95\x29\x96\xbe\x37\x8d\xac\x25\
\x4c\x0f\x84\xc7\xb4\x83\xe9\x23\xcb\x84\x68\x31\x55\x4e\x86\xe1\
\xd3\x0e\x0a\xca\x44\x4c\x4e\x26\x12\x00\x23\x10\x32\x20\xab\x45\
\xd7\x89\x43\x19\xd9\x08\xf9\x05\x65\x27\xdf\xcc\x92\xe2\x01\xf1\
\x48\x48\x19\x3b\xba\xda\x4b\x65\x27\x52\x68\x64\xff\x95\xb1\x0d\
\x06\x56\x76\xd2\xe6\xf6\xac\x2b\xe9\x72\x82\xac\xb1\x63\xa4\x27\
\x5a\x27\x7c\x47\x57\xd2\xd4\xa2\xbb\x1d\x21\x39\x5f\xaa\x86\xf4\
\x17\x5e\x06\x35\x64\x27\x6f\x43\x52\x28\x1a\x94\x30\x36\x0f\xc7\
\xc0\x4e\x63\x8b\x6d\x9e\x79\x16\x3c\x06\x0e\x3d\x85\x22\x1a\x3e\
\xed\x70\x00\x50\x51\x95\xfa\xcf\x9b\xa9\x9a\x8c\xcd\x72\x00\x64\
\x9f\x80\x8a\x5f\xc4\xfe\xcc\x6a\xb4\x4c\x40\x55\x22\x09\x00\xa6\
\x22\x9e\xb4\x00\x90\x7a\x09\x48\x89\x48\x18\xd2\xcb\xd8\xde\xc6\
\x8d\xb9\x97\x44\xc5\x66\x02\x00\x5f\x30\x65\x9b\x71\x94\xdc\x28\
\x88\x05\xe1\x6d\xf0\x3a\x49\x18\xe3\x53\x59\x99\x24\xb5\x54\x0f\
\x55\x7a\xc2\x67\xee\x24\x32\x5b\xad\x73\x8d\x4d\x4b\x15\xf7\x6e\
\xc6\x3f\x3a\x2c\xa9\x55\xe9\xc5\xce\x88\xe0\xac\x1c\x61\xe5\x20\
\x23\xb3\xef\xe4\x09\xc0\x44\x90\xe0\x41\x1d\x53\x06\x50\x36\xd9\
\x29\x09\x4f\x38\xc0\x99\x81\x19\x82\x0b\x40\x1f\x84\x8f\x5f\x58\
\x02\xb8\xde\x1d\x40\x0f\x00\x21\xda\x77\x4e\x47\x58\x83\xb1\x83\
\xb2\x08\x91\xf4\xbe\x4f\x24\x12\x85\xe9\xfd\x04\x13\x51\xb0\x6f\
\x4c\x5d\x9e\xa8\x4b\x3a\xd6\x0e\x26\x91\x44\x9e\x29\xe4\xa4\x18\
\xea\xd2\x4b\x94\xbd\x83\x56\x09\x53\xf1\xee\xf7\x02\xd7\x26\x8f\
\xc2\x97\x44\x06\x9f\xda\x0c\x27\xd1\xc8\x34\xee\x3f\x7c\x7b\xa4\
\xbe\x0e\xbc\x74\xde\x3d\xa0\xce\x55\xe5\xca\xca\x0a\x8a\xa2\xc0\
\x51\x6a\xcd\x66\x13\xad\x56\xcb\x9f\xc4\x71\x6a\xc3\x6f\x00\x87\
\x24\x04\xdb\x0f\x4e\xc7\x07\x72\xb0\x27\x8e\x29\x00\x00\x00\x00\
\x49\x45\x4e\x44\xae\x42\x60\x82\
\x00\x00\x0a\x71\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x36\x00\x00\x00\x2c\x08\x06\x00\x00\x00\x2e\x08\x4b\x20\
\x00\x00\x01\x85\x69\x43\x43\x50\x49\x43\x43\x20\x70\x72\x6f\x66\
\x69\x6c\x65\x00\x00\x28\x91\x7d\x91\xbd\x4b\xc3\x50\x14\xc5\x4f\
\x53\x8b\x22\x55\x41\x3b\x88\x88\x64\xa8\x4e\x76\x51\x11\xc7\x52\
\xc5\x22\x58\x28\x6d\x85\x56\x1d\x4c\x5e\xfa\x05\x4d\x1a\x92\x14\
\x17\x47\xc1\xb5\xe0\xe0\xc7\x62\xd5\xc1\xc5\x59\x57\x07\x57\x41\
\x10\xfc\x00\xf1\x0f\x10\x27\x45\x17\x29\xf1\xbe\xa4\xd0\x22\xc6\
\x0b\x8f\xf7\xe3\xbc\x7b\x0e\xef\xdd\x07\x08\x8d\x0a\x53\xcd\xae\
\x28\xa0\x6a\x96\x91\x8a\xc7\xc4\x6c\x6e\x55\xec\x7e\x85\x0f\x83\
\xe8\x47\x00\x63\x12\x33\xf5\x44\x7a\x31\x03\xcf\xfa\xba\xa7\x6e\
\xaa\xbb\x08\xcf\xf2\xee\xfb\xb3\xfa\x94\xbc\xc9\x00\x9f\x48\x1c\
\x65\xba\x61\x11\x6f\x10\xcf\x6e\x5a\x3a\xe7\x7d\xe2\x10\x2b\x49\
\x0a\xf1\x39\xf1\xa4\x41\x17\x24\x7e\xe4\xba\xec\xf2\x1b\xe7\xa2\
\xc3\x02\xcf\x0c\x19\x99\xd4\x3c\x71\x88\x58\x2c\x76\xb0\xdc\xc1\
\xac\x64\xa8\xc4\x33\xc4\x61\x45\xd5\x28\x5f\xc8\xba\xac\x70\xde\
\xe2\xac\x56\x6a\xac\x75\x4f\xfe\xc2\x60\x5e\x5b\x49\x73\x9d\xd6\
\x28\xe2\x58\x42\x02\x49\x88\x90\x51\x43\x19\x15\x58\x88\xd0\xae\
\x91\x62\x22\x45\xe7\x31\x0f\xff\x88\xe3\x4f\x92\x4b\x26\x57\x19\
\x8c\x1c\x0b\xa8\x42\x85\xe4\xf8\xc1\xff\xe0\xf7\x6c\xcd\xc2\xf4\
\x94\x9b\x14\x8c\x01\x81\x17\xdb\xfe\x18\x07\xba\x77\x81\x66\xdd\
\xb6\xbf\x8f\x6d\xbb\x79\x02\xf8\x9f\x81\x2b\xad\xed\xaf\x36\x80\
\xb9\x4f\xd2\xeb\x6d\x2d\x7c\x04\x0c\x6c\x03\x17\xd7\x6d\x4d\xde\
\x03\x2e\x77\x80\xe1\x27\x5d\x32\x24\x47\xf2\xd3\x12\x0a\x05\xe0\
\xfd\x8c\xbe\x29\x07\x0c\xdd\x02\xbd\x6b\xee\xdc\x5a\xe7\x38\x7d\
\x00\x32\x34\xab\xe5\x1b\xe0\xe0\x10\x98\x28\x52\xf6\xba\xc7\xbb\
\x7b\x3a\xe7\xf6\x6f\x4f\x6b\x7e\x3f\x6c\xb4\x72\xa4\x74\x35\xf5\
\x28\x00\x00\x00\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff\xa0\
\xbd\xa7\x93\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x2e\x23\x00\
\x00\x2e\x23\x01\x78\xa5\x3f\x76\x00\x00\x08\x80\x49\x44\x41\x54\
\x68\xde\xed\x9a\x5b\x6f\xdc\xc6\x19\x86\x9f\x99\x21\xf7\xc0\x5d\
\x69\xe5\xd5\xc1\xb6\x64\x59\x96\xad\xc4\xb5\x61\x07\x71\xec\xda\
\x41\x82\xa2\x88\x7b\x00\x52\x14\x3d\x5d\x34\x70\x5b\xb4\x40\x83\
\xe6\x3f\xe4\xbe\xff\xa0\x37\xbd\x28\x7a\x51\xa0\xff\xa1\x68\x90\
\xab\xb4\x45\x90\xa2\x69\xe3\xa6\xa8\xe3\xc6\x8e\xe2\x93\x2c\xeb\
\x64\xad\xf6\x48\x72\xe6\xeb\x05\xa9\x5d\xee\x4a\x56\x24\xc5\x45\
\x9d\x20\x04\x08\x2e\xc8\x19\xce\xbc\x7c\xbf\xef\x9d\xf7\x23\x57\
\x01\xc2\xe7\x70\xd3\x7c\x4e\xb7\x2f\x80\x7d\xd6\x36\x6f\xf0\x44\
\x7c\xfb\x0f\x44\x57\x7f\x87\xf1\x05\xd4\xee\x6e\xe2\x42\x87\x3b\
\xf7\x3a\xc1\xe4\xb3\x4f\x2e\xb0\xe8\xbd\x5f\x63\x4e\x5f\x41\x0d\
\xcd\xf6\x08\xb5\x2e\xbd\x6a\x53\xad\x71\x60\xd3\x23\x82\x8e\x1f\
\xd0\x79\xef\x57\xd4\x6e\xbf\xc3\xf0\xf4\xc5\x27\x13\x98\xea\x2c\
\xa2\xab\xa7\xa0\x38\x95\x80\xb0\x02\x62\x37\xf9\xec\x1d\x05\xc4\
\x26\x40\x95\x8c\x91\x3f\xad\x68\xff\xeb\x37\xd4\x6e\xfe\x99\xe1\
\xe3\x2f\x3e\x81\xc0\x14\xa0\x3c\x88\x5b\x03\x00\x32\xc0\x6c\x7a\
\x94\x4d\x06\x2d\xa6\x7c\x94\xc2\xc9\x97\xb0\x37\x7f\x4f\xe7\xcd\
\x57\x51\xe6\xd3\xa7\xaf\xc4\x82\x1d\x9a\xc5\x3b\xfe\x1d\x72\xe3\
\x67\x3f\x1d\xb0\xde\x4d\x1b\x29\x63\x16\x64\x33\xec\xd2\xdd\xc6\
\xe9\x39\xdb\x17\xa2\xa6\x78\x10\x3d\xfb\x02\x88\xa0\x4c\x00\xca\
\xec\x1f\x95\x0b\xc1\x36\xd1\x4b\x57\x51\xab\x57\x3f\x3d\x63\xdd\
\xcd\x36\x20\xb6\x19\x00\x19\x70\x76\x9b\xf3\x92\x3c\x04\xe5\x1f\
\x48\x68\x57\x06\x50\xe0\x1c\x88\xcb\xf4\x4f\xfd\x80\x73\x99\x07\
\x26\xbd\x5d\x04\x9c\x43\xb0\xa8\xa0\x8a\xd2\x39\xe8\x6c\x3c\x46\
\x60\x71\x13\xa2\x28\x63\x4c\x32\x20\x5c\xba\x6f\x02\x15\x01\x67\
\xc1\x6d\x4e\x34\xee\xf5\xb3\x16\x19\x64\x1c\xd9\xe6\x1e\xae\xd7\
\x5f\xd2\x73\xfe\x51\xd0\x6a\x5f\x8b\xd2\xce\xc0\x5c\x9c\x0e\xfe\
\x88\xfc\xea\xe6\x18\x88\x8d\xd3\x9f\x36\x03\x80\xad\xec\xba\xf4\
\x28\x6e\x80\x75\xc1\x89\x43\x90\x64\x0c\x67\xd1\x36\x42\x69\x50\
\x4a\x3d\x46\x60\x9d\x46\x32\x71\x67\x33\x83\x3f\x06\x00\x22\x38\
\xfa\x01\xf4\x85\x7f\x73\x11\xd5\xa9\x25\x7d\x6a\x1f\x22\xd1\x06\
\x4e\xdf\x20\x7a\xfb\xf5\xed\xb5\xc0\x0a\x94\xa7\x31\xc7\xbe\x89\
\xa9\x3c\xb5\x0b\xf1\x88\x52\xc6\x1e\x07\x80\x38\xce\x2c\x19\x09\
\xfb\x42\x1a\x7a\x22\x60\x43\x68\x2c\x81\xb2\xe8\xea\x49\x4c\xf9\
\x68\xa2\xcc\xbb\x12\x99\x98\x78\xed\x63\xec\x47\x6f\xee\x36\x14\
\x1b\x20\x71\x6f\xa2\x9b\x92\x2f\x11\xf6\xfe\x55\x34\x61\xe2\x4c\
\x24\x93\xf8\x49\x83\xec\xe3\x41\x6d\xe6\x93\x6c\x73\x7e\x73\x6e\
\x51\x84\x1a\x3a\x86\x3e\x78\x0a\x55\x99\x05\xbf\x0a\x4a\x27\xfd\
\x6c\x07\xfc\x32\xe4\x46\x7a\x0f\x57\xe8\x8e\xa9\x08\x91\xd6\x2a\
\x6e\xfd\xce\x6e\x55\xb1\x9d\x48\xee\x26\x5b\xce\xe1\xe2\x10\x59\
\xbb\x8e\x1a\x3b\x83\x2a\x1e\x40\xa9\xc7\x63\x35\x55\xdc\x41\x15\
\x46\x51\xa5\xd1\x04\x4c\x7b\xad\x2b\x4a\x12\x35\x20\x5f\x45\x99\
\x62\x46\x39\x53\x80\xca\x62\x57\xaf\x11\x37\x1a\x78\xd3\x5f\x03\
\x7e\xf9\xc9\xc0\x9c\x6b\x25\xc0\xe2\xb8\x7b\x23\xb7\x7e\x13\x3d\
\x34\x83\x99\xbe\x04\xde\x81\x81\x4a\xce\xf5\x64\xbc\x8f\xbd\xf4\
\xb7\x0c\xfc\x96\x5e\x1b\x2d\x11\xc4\x1d\x08\x5b\x69\x64\x64\x96\
\x07\xd7\x01\x17\x25\xd1\x23\x92\x59\x3a\x00\xed\xb0\xb5\xbb\xa8\
\xc8\x51\x3a\xfe\xd2\xee\x18\x73\x71\xa3\x07\x2c\x95\x7b\x69\x2d\
\xa0\x4f\x7e\x2f\x59\xa3\xa2\x7a\x2f\x3c\xb3\xaa\xe9\x6c\xdf\xa4\
\x7b\xb9\x97\x99\x90\xa4\x52\x2f\xf4\xa9\x62\xaf\x6d\xd2\x46\xc4\
\x41\x1c\x82\x17\x25\xf9\x2e\xae\xc7\x96\x06\x69\x2f\x13\x39\x8d\
\x8c\x9f\xdb\xcb\x02\xdd\x4c\xe2\x3b\x4e\x07\x6e\xaf\xa2\x82\xc3\
\x90\x0f\x52\x16\xa5\x1f\x84\xd8\x0c\x2b\x2e\x93\x4e\x2e\x35\xd1\
\x83\x0b\xb1\xeb\xb5\x17\x49\x40\x6c\xb9\xee\x12\xb6\x36\xf7\xec\
\x22\x8e\xc2\x3e\x9c\x87\xc8\x22\x33\x5f\xde\xe3\x3a\xd6\x05\x06\
\x52\x5b\xc0\xcc\x7d\x1f\xe5\x4c\x12\x36\xce\xf5\x83\x70\xd9\xe3\
\x6e\x40\x38\x3e\x58\x5d\x64\x29\x0c\x29\xfa\x39\x7c\x27\x94\x3c\
\x45\xc1\x28\x2a\x7e\x9e\xb2\x9f\x4b\xf3\x2c\x4c\xc2\xd0\x45\xfd\
\xc2\x24\x9a\xc8\xfa\x48\xe1\x10\xd5\x89\xa3\x7b\x01\xd6\x4a\x04\
\x24\xb6\x89\x34\x23\xe8\x03\xc7\x20\x8e\x12\xc6\x9c\x1d\x70\x24\
\xf4\x1c\x45\x0a\x46\xfa\x18\xcc\x84\x61\xca\x8e\x72\x21\x0b\x1b\
\x6b\x14\x2a\xd3\x8c\x0d\x4d\xd2\x8c\xea\xac\xd7\xef\x60\xe2\x25\
\x8e\x14\x03\x8e\x14\x03\x4a\x46\x40\x22\x94\x8b\x7a\x63\x18\x0f\
\x69\x2d\x22\x2a\x87\x3e\x7c\x71\xaf\xce\x23\x04\xdb\x42\x62\x0b\
\xad\x75\xf4\xe8\x19\x94\xf1\x93\x04\x77\x2e\x5d\xe3\x52\xd1\x70\
\x59\xc9\x4f\x26\x2d\x92\x51\xaf\x4d\x9b\x24\xfd\x0f\xe2\xe9\xca\
\x08\x81\xd6\xdc\xc5\x50\x1a\x1a\xc7\x78\x33\xd4\xfd\x02\x0f\xd6\
\x6f\xb0\xdc\x5e\x63\xbe\xbd\xc6\xf1\x9c\xcf\x8c\x5f\xa1\x80\xed\
\x89\x8e\x6f\xb0\x0f\xe7\x31\x6d\x4d\xf9\xf0\xd9\x3d\xba\xfb\x4e\
\x2b\x2d\x5d\x1c\x34\x37\x50\xa7\x2f\x40\x14\x42\xd4\xee\x79\xb9\
\x14\x8c\xb8\x4c\x48\xca\x80\x78\x6c\xb6\x13\xc9\x18\xe2\x5e\x0e\
\x1e\x29\xe6\x90\xc6\x32\x1f\xdf\x7f\x87\xc2\xd8\x29\xaa\xd5\x83\
\xe8\xbc\x70\xef\xe1\x0d\xde\xaf\xdd\x66\x7e\x75\x83\xf3\x14\x38\
\x9d\xaf\x52\xf6\x0a\xa0\x0c\xd2\x5e\x23\x0c\x63\x08\x9e\xda\x8f\
\x57\x6c\x27\x7b\xd4\x81\x60\x0c\x86\xc6\x90\x66\x2d\xc9\xbb\x9d\
\x40\x74\x15\x4f\x32\xcb\xc0\xd6\x30\xcc\xe6\xcb\x91\x20\x8f\x6b\
\xd6\xb8\xfe\xe0\x3d\x54\x75\x16\xad\x15\x79\xbf\x48\x50\x2a\x73\
\xaf\xbd\xc2\xca\xe2\xbf\xd9\xc0\x70\x61\x7c\x8e\x4a\x79\x0c\xbb\
\x7a\x0b\x11\x0f\xff\xe8\x57\xf6\x53\xb6\x84\x60\x3b\xd8\x7a\x13\
\xff\xf4\x65\x8c\xd2\x88\x6d\x65\x6c\x16\x3d\x06\xba\x73\xcc\xda\
\x2b\xb6\xe6\x57\x62\x75\x13\x9b\x95\x8d\x0e\x67\x99\xca\xfb\xb4\
\x36\xd6\xb8\xb9\x22\x30\x3c\x81\x51\x0a\x0f\xc8\xe7\x0d\xf7\x9a\
\x8b\xfc\xf1\xee\x5f\xc9\x29\xcd\xf3\x41\x85\x38\x06\x9d\x1b\xa7\
\x34\x32\xb9\x1f\xc6\x42\x68\x87\x88\x80\x39\xf8\x0c\x34\xd6\x93\
\xfc\x12\xd7\xef\x1d\xbb\xee\x7f\xb7\x20\xe2\x54\x54\xb2\x0f\xd1\
\x82\x73\xcc\x15\xf2\xac\x6e\x3c\xe0\x9e\x16\xbc\x20\x48\xab\x15\
\x85\xf1\x15\x77\x9b\x0b\xfc\x65\xf9\x7d\x0e\x19\xc5\xa1\xdc\x38\
\x66\xe2\xfc\xde\xdd\xbd\xa4\x0b\x73\xab\xd1\x26\x98\x9a\x43\xe5\
\x4b\x48\x63\x3e\x51\xc9\x47\x80\x00\x49\x81\xec\x0e\xc4\xd6\xfe\
\x49\xd8\x4e\xf9\xc2\x6a\x67\x9d\x75\x2d\x89\x11\x50\x06\xb4\x46\
\xb4\xe5\x5a\xed\x63\xfe\xb6\xb6\xc0\xcb\x27\xbe\x4d\x75\xea\xd9\
\x7d\x94\x2d\xae\x0e\x51\x44\x23\x74\x94\xa7\x5e\x84\x76\x3d\x59\
\xb0\x33\xaf\x02\x06\x99\xc0\xb9\x5e\x3d\xd5\x65\x3d\xde\xea\x3a\
\xfa\x2c\x98\xdb\x92\x87\x53\x85\x1c\x37\xd7\xea\xdc\x17\x50\xe5\
\x1c\xda\xf3\xba\x85\x66\xdd\xd6\xb9\x11\x97\x58\xf2\x87\xf7\x5b\
\x8f\x75\x88\x9c\x10\x54\x86\xd0\x23\xb3\xb8\xd6\xfd\x64\xa1\xcc\
\x94\xf5\x56\x06\x26\xdb\x07\x62\x4b\x5c\x67\xda\x6e\x77\xdd\x66\
\x42\x5b\xf0\xa5\x89\x27\x39\x50\x05\x8c\xf1\x30\x68\x14\x0a\xa7\
\x2d\xb7\x82\x12\x1f\x15\xab\xfb\x2f\x34\x63\xa5\x28\x4d\x9f\x45\
\xe5\xf3\xc4\x0f\xd7\x13\x31\x79\xdc\x20\x52\x20\x7d\x25\x8d\xb5\
\x98\x38\x02\x3f\xc6\x21\x78\xca\x23\xa7\xf2\xe8\x94\xb6\xa6\x8b\
\xa8\x4b\x67\xff\xc0\xca\x81\x8f\x9a\xbc\x84\xab\x2d\x40\xd8\x4e\
\x2d\xcd\x5e\x41\xc4\xfd\xac\x3a\xd9\x1a\x92\xb1\xcd\xd8\xb3\xe4\
\x5a\xce\x3a\x6c\xb3\x49\x58\x28\xe2\x69\x1f\xcf\xf4\xa6\xd9\xb1\
\x6d\xea\x9d\xda\xfe\x80\x49\x6b\x19\xe7\x0d\xa3\x8b\x87\x70\x2b\
\xff\x48\x0b\xce\xff\x0d\x88\x3b\x9d\x90\x95\x38\x06\x25\x28\x95\
\x38\x96\x1b\x61\x87\x0d\x3f\xc0\x8f\x15\xc6\x80\xa7\x74\xaf\xf6\
\x73\x21\x77\xd7\xae\xf3\xd6\x87\x6f\x10\xe4\x87\x50\x80\x13\x61\
\xac\x34\xc1\xb1\xd1\x13\x3b\x03\xb3\xf3\x6f\xa0\x8e\x5c\x40\x87\
\x75\x5c\xd8\x80\x2d\xd4\xef\x06\x44\x3c\x60\xb5\xb6\x17\x8e\x7f\
\x36\x6a\xfc\xe9\x61\x8d\x38\x3f\x44\x69\xe8\x20\x56\xa0\xad\x7d\
\xc6\x4b\x43\x04\x79\x9f\xd0\xb5\xd1\x5e\x0e\xcf\xf3\x21\x02\x31\
\x11\xef\x2e\xbc\xc5\x07\xcb\xd7\x19\x29\x8d\x52\x6f\xd5\x11\x67\
\xf8\xee\xd9\x57\x3e\x99\x31\xbd\xf0\x77\xf4\x99\x5f\xe0\x6a\x37\
\xd2\x10\x8c\x76\x06\x11\xc5\xfd\x85\xe4\x4e\x0f\x61\xa0\x00\x7d\
\xb9\x3a\xcc\x29\xa3\xb9\xef\x4d\x52\x39\x76\x99\xc2\xf0\x04\x6b\
\xe1\x32\x8b\xed\x7b\xac\xd4\xef\xd1\x0c\x05\xa5\x75\x37\x1c\x1d\
\x82\xe7\x75\x98\x19\x1b\xe5\xe4\xd8\x73\xdc\x5f\x5f\xe2\x58\xf5\
\x2c\x3f\x38\xf7\xe3\x9d\x81\x49\xfa\x91\x45\xea\xb7\x71\xad\xbb\
\x28\x19\x08\xbb\x30\x1a\x78\x7f\xb1\x83\x30\x3c\xda\xd6\xf4\xb5\
\x9b\x0d\x80\xda\x87\xdc\xba\x5e\xc3\x9f\xbc\x80\xae\x4c\xf4\x8b\
\x89\x05\x0f\x93\xcc\x0b\x28\xf8\x01\x4a\x29\xee\x3c\x5c\x60\x76\
\xf4\x19\x7e\x78\xfe\x67\x9f\x9c\x63\x32\x7c\x0a\xad\x22\x58\xbf\
\xc5\xb6\x2f\xa8\x95\xb7\xc3\xe7\x25\x7f\xdf\xef\x3d\xe6\x46\x2a\
\xe4\x5a\x31\xd7\x96\xfe\x43\x5b\x1c\x2e\xf0\x50\xa8\xee\x58\x46\
\x69\x3c\xa5\x11\xa5\x19\xc9\x8d\x23\x71\xc0\xec\xc4\x33\x5c\x39\
\xff\xf3\xdd\x89\x47\xf1\x1b\xbf\xfd\xbf\x7e\x25\xb9\xbd\x72\x9b\
\x77\xef\xbc\xcd\x6a\x6b\x1e\xd1\x0a\x65\x40\x22\x41\x6b\x85\x31\
\x86\xbc\x2e\xa3\x5d\x89\x33\x87\x5f\x7c\x24\xa8\x27\xf2\x8b\xe6\
\xf4\xe8\x34\xcf\x1d\x79\x9e\xb2\x7f\x98\x66\x2b\xc6\x39\xc1\x62\
\x89\x5c\x84\x16\x0f\xc3\x30\x2f\xcc\x7c\x8b\x2b\x17\x5e\xfd\xec\
\x7d\xaa\x9d\x1e\x9d\xe6\xab\x73\x97\x99\x29\x9f\x26\xea\x78\x88\
\x03\xad\x0c\x79\x3d\xc6\xe5\x13\xaf\xf0\xa3\x4b\xaf\x7d\x76\xbf\
\x41\x4f\x54\x26\x39\x75\xe0\x3c\x4f\x4f\x5c\x22\xec\x18\x08\xcb\
\x7c\x7d\xee\x0a\x3f\xdd\x05\xa8\x9d\xcb\x96\x27\x60\xfb\xd2\xf1\
\x33\x5c\xbb\xf9\x3e\x8d\xb0\x89\x6f\x7c\x7e\x72\xf1\xb5\x5d\xf7\
\x55\x7c\xf1\x07\x96\x2f\x80\x3d\x11\xdb\x7f\x01\x5e\x5a\x7f\xe8\
\x56\xce\xcf\x19\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
\
\x00\x00\x0a\x86\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x32\x00\x00\x00\x38\x08\x06\x00\x00\x00\xbf\xa4\xab\xd7\
\x00\x00\x01\x85\x69\x43\x43\x50\x49\x43\x43\x20\x70\x72\x6f\x66\
\x69\x6c\x65\x00\x00\x28\x91\x7d\x91\xbd\x4b\xc3\x50\x14\xc5\x4f\
\x53\x8b\x22\x55\x41\x3b\x88\x88\x64\xa8\x4e\x76\x51\x11\xc7\x52\
\xc5\x22\x58\x28\x6d\x85\x56\x1d\x4c\x5e\xfa\x05\x4d\x1a\x92\x14\
\x17\x47\xc1\xb5\xe0\xe0\xc7\x62\xd5\xc1\xc5\x59\x57\x07\x57\x41\
\x10\xfc\x00\xf1\x0f\x10\x27\x45\x17\x29\xf1\xbe\xa4\xd0\x22\xc6\
\x0b\x8f\xf7\xe3\xbc\x7b\x0e\xef\xdd\x07\x08\x8d\x0a\x53\xcd\xae\
\x28\xa0\x6a\x96\x91\x8a\xc7\xc4\x6c\x6e\x55\xec\x7e\x85\x0f\x83\
\xe8\x47\x00\x63\x12\x33\xf5\x44\x7a\x31\x03\xcf\xfa\xba\xa7\x6e\
\xaa\xbb\x08\xcf\xf2\xee\xfb\xb3\xfa\x94\xbc\xc9\x00\x9f\x48\x1c\
\x65\xba\x61\x11\x6f\x10\xcf\x6e\x5a\x3a\xe7\x7d\xe2\x10\x2b\x49\
\x0a\xf1\x39\xf1\xa4\x41\x17\x24\x7e\xe4\xba\xec\xf2\x1b\xe7\xa2\
\xc3\x02\xcf\x0c\x19\x99\xd4\x3c\x71\x88\x58\x2c\x76\xb0\xdc\xc1\
\xac\x64\xa8\xc4\x33\xc4\x61\x45\xd5\x28\x5f\xc8\xba\xac\x70\xde\
\xe2\xac\x56\x6a\xac\x75\x4f\xfe\xc2\x60\x5e\x5b\x49\x73\x9d\xd6\
\x28\xe2\x58\x42\x02\x49\x88\x90\x51\x43\x19\x15\x58\x88\xd0\xae\
\x91\x62\x22\x45\xe7\x31\x0f\xff\x88\xe3\x4f\x92\x4b\x26\x57\x19\
\x8c\x1c\x0b\xa8\x42\x85\xe4\xf8\xc1\xff\xe0\xf7\x6c\xcd\xc2\xf4\
\x94\x9b\x14\x8c\x01\x81\x17\xdb\xfe\x18\x07\xba\x77\x81\x66\xdd\
\xb6\xbf\x8f\x6d\xbb\x79\x02\xf8\x9f\x81\x2b\xad\xed\xaf\x36\x80\
\xb9\x4f\xd2\xeb\x6d\x2d\x7c\x04\x0c\x6c\x03\x17\xd7\x6d\x4d\xde\
\x03\x2e\x77\x80\xe1\x27\x5d\x32\x24\x47\xf2\xd3\x12\x0a\x05\xe0\
\xfd\x8c\xbe\x29\x07\x0c\xdd\x02\xbd\x6b\xee\xdc\x5a\xe7\x38\x7d\
\x00\x32\x34\xab\xe5\x1b\xe0\xe0\x10\x98\x28\x52\xf6\xba\xc7\xbb\
\x7b\x3a\xe7\xf6\x6f\x4f\x6b\x7e\x3f\x6c\xb4\x72\xa4\x74\x35\xf5\
\x28\x00\x00\x00\x06\x62\x4b\x47\x44\x00\x16\x00\x16\x00\x73\xc7\
\x44\x26\x19\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x2e\x23\x00\
\x00\x2e\x23\x01\x78\xa5\x3f\x76\x00\x00\x00\x07\x74\x49\x4d\x45\
\x07\xea\x02\x09\x0f\x15\x38\x68\x28\x97\x19\x00\x00\x00\x19\x74\
\x45\x58\x74\x43\x6f\x6d\x6d\x65\x6e\x74\x00\x43\x72\x65\x61\x74\
\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x57\x81\x0e\x17\
\x00\x00\x08\x5d\x49\x44\x41\x54\x68\xde\xed\x9a\x59\x8c\x1c\x57\
\x15\x86\xbf\x7b\xab\xaa\xb7\xea\x65\x16\xcf\x78\x9b\x2c\x1e\x4f\
\xc6\x71\x1c\x27\x52\xec\x10\x11\x05\x5e\x82\x04\x84\x24\x82\x28\
\xaf\xbc\x20\x9e\x50\x9e\xe0\x01\xc5\x3c\x21\xa1\x08\x45\x88\x40\
\x14\x82\x14\x21\x04\x6f\x48\x80\x08\x21\xb2\x14\x45\x04\x5e\x40\
\x62\xcb\xea\x25\xb6\xc7\x71\x4c\x66\x3c\x33\x3d\x5b\x4f\x6f\xd3\
\x5d\x75\xef\x3d\x3c\x74\xcf\xc4\x76\x66\xed\x59\x62\xa2\x1c\xe9\
\xa8\xa5\xaa\x56\xdd\xfb\xdf\xf3\xff\xe7\x9e\x3a\xb7\x94\x88\x08\
\x9f\x00\xd3\x7c\x42\xec\x53\x20\x37\x9a\xf9\xd7\x5f\xf8\xd9\xc9\
\x73\x8c\xcf\x35\x76\x74\x12\x61\xca\xe3\x3b\x5f\x3d\x4c\xc2\xf3\
\x3a\x7e\x86\xba\x5e\xec\x3f\x7d\xf9\x5d\x1e\x39\x3e\xc0\xfe\xde\
\xcc\x8e\x80\x98\xaf\x47\x3c\xf3\xc7\xb3\xe4\x33\x01\x4f\x3e\x7e\
\xe7\xd6\x52\x2b\xf0\x35\xc9\x60\x79\x0f\x3c\xf0\xb5\x6c\x89\x07\
\x1e\x24\x7d\x8d\xd6\x8a\xdd\xf9\x34\x4f\xfd\xee\xd4\xd6\x6b\xc4\
\x39\x87\xb5\xf6\x23\xbe\x91\x6c\x2d\x80\x59\xcd\xdb\xcf\x4a\x06\
\x1e\x8f\x7e\x76\x80\x3d\xf9\x34\x4f\xfd\xf6\x14\x9d\xec\x08\xab\
\x8a\xdd\xae\x35\x91\x35\xdc\xae\x97\xdf\x0a\xb2\x19\x9f\x47\xef\
\x1f\x60\x4f\x21\xcd\x0f\x7f\x7f\x9a\xd8\xba\xad\x01\x62\xdb\x2b\
\xba\x19\x13\x01\x6b\x57\xf7\x25\x06\x58\x48\x07\x3e\x0f\xdf\x37\
\xc0\xee\x7c\x9a\x67\x5e\x7a\x97\x66\x6c\xb7\x2e\xfd\x3a\xb7\xf6\
\x64\x56\x73\x91\x55\xfc\x2a\x0e\x2e\xb2\x29\x4c\xf9\x7c\xe5\x33\
\x03\xf4\x67\x53\x3c\x77\xf2\x3c\xf5\xa6\xd9\x64\x44\xda\x13\x71\
\x6e\x8d\xc9\xac\xe2\x9d\x5a\x36\xed\xf3\xa5\xe3\xfb\xe8\x0d\x93\
\xbc\xf0\xca\x08\x95\x85\x78\xe3\xfb\xc8\xf5\xd4\xe8\x98\x56\x80\
\x5b\xe7\x2a\x2e\x44\x96\x17\x5e\xb9\xf0\x91\xfb\xe5\x7a\x44\x23\
\xb2\xfc\xe2\xd5\x11\xbe\xf1\x85\x21\x0a\x99\xa0\x33\x20\x6e\x93\
\x3a\x91\x75\xdc\xcf\xa6\x03\xbe\xf5\xd0\xf0\xaa\xff\xfb\xd5\x9f\
\x2f\x32\x72\xf1\x3d\x8e\x1e\x3a\x40\x22\x91\xd8\x18\x10\xbb\x8e\
\x15\xdd\x4c\x12\x70\xae\x35\x46\xd5\x0a\xb9\x4c\x6a\xc5\xff\xe6\
\x53\x1a\xcf\xd3\x34\x1a\x0d\x9c\x73\x9d\x45\x64\x25\xf1\x6f\x45\
\xe1\xbf\xf8\x0c\xb3\xc6\xc3\xd6\x3b\x94\xbf\xaa\xd8\xdd\xd6\xea\
\x66\x47\x8b\xc6\xad\x14\xbb\xdc\x08\x40\xdc\x16\x68\xe4\x86\x00\
\xb2\x9d\x2b\xda\x12\xbb\xec\x1c\xb5\x56\x16\xfb\xca\x93\x88\x63\
\xc7\x5c\xa9\xc1\xd4\x6c\x95\x72\x35\xc2\x46\x0e\xed\x29\x52\x69\
\x9f\xde\xae\x0c\x7d\xbd\x21\x99\x8c\xbf\xe5\x5a\x5b\x99\x5a\x4e\
\xb0\x56\xd6\xad\x9d\x28\x72\x5c\x7c\x7f\x96\x8b\x97\x67\x48\x25\
\x7c\x72\xb9\x04\xe9\x74\x80\x17\xea\x76\x84\x85\xe9\xd9\x3a\xe3\
\x13\x15\xd2\x61\x82\x03\x37\xf7\x90\x0b\xfd\x65\xd3\xfe\xd6\x52\
\x6b\x03\x65\x46\xa5\x1a\x71\xe6\x5c\x91\xd1\xf1\x79\xfa\x77\x85\
\xdc\xb4\xbf\x40\xbe\x90\x24\x91\x08\xc0\xd3\x58\x2b\x18\xe7\x88\
\x1a\x86\x6a\xa5\xc9\xfc\x7c\x83\x33\x67\x27\xb8\xe5\x96\x6e\xfa\
\xfb\xc2\x55\xe9\x2c\x3b\x25\xf6\x4a\x35\xe2\xd4\x99\x09\x8a\x33\
\x55\x86\x6f\xeb\x65\xf0\x96\x6e\x92\xa9\xa0\xb5\xa1\xba\x56\x0a\
\x17\xad\x50\x4a\x93\x0e\x7d\x12\xe9\x24\x99\x5c\x8a\xd9\x99\x1a\
\xa3\x63\xf3\x08\xd0\x77\x15\x98\x6d\x11\xfb\x5a\x40\xa2\xc8\x71\
\xf6\x42\x91\xc9\xe9\x2a\x87\x0f\xf5\x31\x3c\xd8\x43\xc2\xd7\x58\
\x01\x71\x60\x10\x16\xd9\x29\xce\xd1\x34\x60\x05\x74\x10\xd0\xd5\
\x57\x60\x5e\x55\xb9\x30\x32\x4d\x2a\x93\x24\x0c\xfd\x9d\x15\xfb\
\xd5\xe1\x9f\x98\xaa\x32\x33\x53\xe7\xe6\x81\x3c\xc3\x83\xbd\x64\
\x12\x1a\xaf\xfd\xa6\xd4\x74\x42\x1c\x09\xb1\x05\x63\x5b\xbf\xcd\
\x58\x88\x1d\x58\x23\x18\x51\xd8\x20\xa4\xa9\xea\x9c\x1f\x99\xe6\
\xee\xa3\x7b\xb6\x39\x22\x6e\x79\x20\x51\xec\xf8\x60\xac\x44\x2a\
\xed\x33\x74\x60\x17\x99\xa4\x47\x52\x83\x56\x60\x1c\xc4\x56\xa8\
\x2e\x38\x2a\x91\x10\xd9\xd6\xb5\x28\x76\xc4\xa2\x71\x46\x68\x1a\
\x8b\x71\x90\xec\x2e\x30\x39\x3e\x4d\xbd\x6a\x48\x65\xfc\x8e\x37\
\x23\xbd\x5a\x9a\x75\x0e\x9c\x7c\xc8\x75\xd3\xfe\x75\x0e\x4a\x73\
\x0b\x34\xea\x11\xbb\x7a\x52\x14\xf2\x29\x94\xb4\x40\x38\x81\x85\
\x58\x98\xad\x39\x4a\x75\xa1\x16\x41\xdd\x42\xc3\x0a\x4d\xa3\x30\
\x16\x62\x51\xad\x04\x20\x96\xc8\xf9\x24\xc2\x14\xe3\x13\xe5\x25\
\x5d\xba\x0e\x36\x64\xbd\x56\x85\xea\x84\x65\x07\x28\xcd\x2f\x10\
\xf8\x9a\x5d\x3d\x19\xb4\x47\x2b\x2b\x59\xa8\xc7\xc2\x4c\xdd\x32\
\x57\x77\x44\xae\xfd\x2a\x20\x60\xad\xc2\xa1\xb0\x02\xc6\x2a\x10\
\x1f\x17\x0b\x0b\xb1\x23\x95\x4d\x33\x3e\x31\x7f\x4d\x92\xd9\x28\
\x90\x8e\xb3\x56\xbd\x11\xa3\xb5\x22\x95\x0c\x30\x56\x58\x30\x0e\
\xa5\xa0\x61\x84\x52\x43\x68\xda\x0f\x3b\x25\xd6\xb4\x26\x6f\x05\
\x8c\x01\xb1\x82\xc5\x22\xc6\x23\x12\x8b\x84\x49\x66\xcb\x8d\x65\
\xc7\x94\xed\xce\x5a\xb1\x71\xa0\x40\x2b\x4d\x23\x72\x94\x9b\x0e\
\xa3\x84\xd8\x40\x23\x96\x25\x10\xce\x48\xab\x92\x16\xf5\x21\x08\
\x31\x18\xeb\x30\x68\x8c\x01\x63\x84\x46\xe4\x36\x55\xdb\x75\x1c\
\x11\xa5\x15\xce\x41\x64\x1d\xc6\x42\xad\x9d\x5a\x63\x2b\x18\xb7\
\x1c\x08\x8b\x58\x8d\x15\x8b\xb1\x16\x63\xc0\x2e\xae\xb7\x51\x04\
\xde\xe6\xf6\x91\x8e\x9b\xd8\xa9\x94\x8f\x13\xa1\xd6\x30\x44\x0e\
\x62\x0b\x62\x04\x67\xaf\x07\xa1\xb1\x4b\x91\xb0\x18\x6b\x30\x46\
\x30\x6d\xdd\x88\x08\x2e\x8e\xc8\xe5\x93\xab\xb6\x8b\xb6\x0d\x48\
\xae\x90\xa1\x11\x0b\x93\xd3\x0b\x44\x4d\x87\x35\x42\xe4\xc0\x5e\
\x0d\x02\xdd\xca\x76\x96\xb6\xc8\x0d\x62\xc0\xe2\x01\x82\x31\x06\
\xad\x34\xf1\x42\x9d\xfe\x3d\x5d\xc4\x31\x1f\xf1\xcd\xb7\x4c\xd7\
\xe8\x57\x65\xb3\x69\x94\xe7\x31\x39\x55\xa5\x5a\x8d\x70\x40\xd3\
\x3a\xe2\xab\x41\x48\x2b\x65\x8b\x48\x1b\x84\xc2\xe2\x21\xa2\x5a\
\x3d\x2f\xa7\x08\x34\x94\x4b\xf3\xf4\xf5\x17\xb6\x87\x5a\xc6\xb0\
\xec\x0a\x2d\xba\xa7\x3d\xf6\xee\x2d\x60\x62\x43\x71\x7c\x0e\xe5\
\x04\x67\xa5\x9d\x9d\x54\x4b\xcc\x6d\x4a\x39\x71\x6d\x10\xba\x4d\
\x29\x43\xd4\x04\xe5\x84\xd2\xd8\x18\x57\x46\xde\x20\x9d\x0c\x3e\
\x1e\x8d\x00\xf4\xf5\xe5\xc9\xe7\x43\x8a\xe3\x15\x66\xa7\x2b\x68\
\xad\x5a\x8d\x6b\x63\xb0\xb1\x41\xac\x6d\xe9\xc2\x99\x36\xb5\xda\
\x20\x22\x45\xe0\x69\x74\x54\x67\xf2\xc2\x79\xe6\x27\xfe\xb9\xf3\
\x2f\x56\xd7\x1e\x3f\x78\x0c\x0e\xf6\x13\x35\x2d\x1f\xbc\x57\x64\
\x8f\xb1\xa4\x0b\x21\x4a\x69\x94\x86\xd8\xc6\xc4\x16\x5c\xbb\xc6\
\xc2\x09\x4e\x3c\x12\xda\xe1\x35\xe6\xb9\x7c\xee\x34\x7b\x7a\x1a\
\x94\x5c\x17\x2e\x8e\xd1\x41\xf0\xf1\x44\x04\x20\x9b\x4d\x72\xfb\
\xe1\xbd\x74\x77\x65\x98\xb8\x3c\x45\x65\x72\x0e\x53\x6f\x20\xc6\
\xb5\xfa\x50\x4e\x50\xaa\x95\xcb\x3d\x25\x04\xa6\x49\x5c\x2a\xf2\
\xde\xeb\x7f\xe5\xbf\x6f\xbd\x8a\x6e\x5c\xe6\xb6\x03\xb7\x32\x35\
\x7a\x89\xa8\x32\x8d\x69\xd4\x10\x91\x25\xdf\x91\x88\x2c\x5a\x18\
\x26\x38\x72\x64\x3f\xc5\xe2\x3c\x57\x46\x67\xa8\xce\x55\x49\x17\
\xb2\x48\x7b\xaf\xf1\xb4\x26\x50\x3e\xbe\x18\xe2\x5a\x8d\x6a\xf1\
\x0a\xa9\xa0\xc8\xc1\xe1\x5e\x2a\x4d\x87\x9e\x9a\xa4\x2b\x7e\x91\
\x42\x5f\x37\x7e\xb6\x9f\xa0\xab\x9f\xfa\xee\x63\xa0\x34\x22\xfe\
\x66\x77\xf6\xf5\xaf\x88\x38\xc1\xf7\x15\xfb\xf6\x75\xb1\xab\x2f\
\x47\xa9\xd2\x60\x66\xae\x4a\x79\xa6\x42\xad\x5c\x27\x48\x27\x29\
\x74\x67\xc9\x77\x87\x74\xdf\xda\xcd\x3d\xc7\x0f\x00\xf7\x03\x86\
\x85\x5a\x83\xbf\xfc\xe6\x59\x8e\x99\xd7\x08\xc3\xfd\xd0\x74\xc4\
\x17\xe7\x68\xde\x7d\x82\xc6\xde\xfb\x80\xe4\x66\x1b\x74\x6e\xc3\
\x87\x2d\x00\x3a\xf0\x28\xf4\x84\x14\x7a\x42\x38\xb8\x7b\xf9\xf2\
\xa6\x55\x1b\x00\x01\x7e\xc6\xe7\xc1\xc7\xbe\xc9\xd4\xf3\x7f\xa2\
\xe7\x6b\x0f\x40\x97\x22\x7a\xe7\x5f\xf4\xfe\xfd\x04\x33\xf7\x3d\
\x05\x03\x9f\x5b\x57\xc5\xb5\x22\x10\xb3\x34\xe0\xf6\x9a\x88\x60\
\x6a\x35\x9c\x68\xec\x54\x11\x2f\x71\x13\xb9\xbb\xee\xa5\x02\xec\
\xfa\xc7\x09\x9a\xbb\x9f\x06\x93\x05\xbc\xed\x15\xfb\x66\x4d\x69\
\x4d\xd0\xd3\x4b\x39\xb7\x9f\xf9\x77\xde\xc4\x8e\x8d\x41\x2d\x41\
\xee\xae\x7b\xf1\x8f\x1e\x62\xea\xa5\xef\xd2\x5d\xfa\x0f\x9e\xc4\
\x37\x36\x10\x00\x97\xcc\x52\x7c\xf0\xfb\x5c\x38\x1b\x51\x3e\x75\
\x0a\x3b\x36\x0a\xd5\x45\x30\xc3\x7c\xb1\xf2\x4b\x72\xa5\x33\x60\
\xe3\x9d\x01\x22\x1d\xba\xf6\x3c\x6e\xba\xe3\x76\xc6\x1f\x7e\x9a\
\x73\xe7\x6a\x94\xdf\x79\xbd\x0d\x26\x58\x8a\x4c\xe6\xed\x9f\x63\
\x3e\xf8\x37\x2e\x6e\x6e\xf0\x0d\x71\x39\x5f\xe3\xa8\xcd\x0a\x34\
\xe9\xcc\x63\xad\xd9\x77\x78\x98\xf1\x2f\xff\x88\x73\x6f\xd7\x29\
\x9f\x3e\xdd\xa2\x59\x35\x20\x77\xe7\x71\x82\xa3\x87\x98\x7a\xf9\
\x04\xb5\x91\xbf\x2d\x0b\x66\x45\xb1\x47\xed\x01\xae\x4d\x65\xd2\
\x79\x2b\x70\x3d\x7a\x41\x31\x30\x34\xc4\xe8\x63\xcf\xc1\xc9\x6f\
\x33\xcc\x1b\x14\x00\xaf\x6f\x3f\xd9\x23\xc7\xa8\x02\xd3\x27\xbf\
\x07\x0f\xfd\x80\x70\xe8\x01\x74\x90\x5c\x07\xb5\x62\x81\xe6\x75\
\x6e\x77\x20\x8b\x01\xfb\x0f\x0e\x72\xe5\xa1\x1f\x73\x7e\x31\x32\
\x53\x63\x50\x82\xec\x91\x63\x04\x47\x0f\x51\xfc\xc3\x93\xd4\xde\
\x7f\xf3\x9a\x13\xac\x15\x81\x04\x9e\x22\xf1\x31\x38\x6d\x1f\x18\
\x3e\xc8\xf8\xe3\xcf\x31\x3a\x52\x69\x83\x29\x42\x3d\x41\xf6\x8e\
\x7b\x28\xd7\x52\x9c\x79\xf3\x34\xd5\x72\x79\x75\x6a\x35\x63\xcb\
\x70\x6f\x72\xcd\xdc\xbd\xed\x36\x70\x88\x77\x77\xff\x84\x0b\xcf\
\x3f\xc1\x90\x7b\x83\x9c\xd1\xa8\x84\x8f\xd8\x24\x41\x36\x8f\xf6\
\xfd\x95\x81\x04\x9e\xe2\xd7\xaf\x8d\xec\xec\x29\xcd\x1a\x36\x3b\
\xf8\x04\x8f\x9c\x79\x96\xfc\x5b\x2f\x82\x52\xe8\xcf\x7f\x9d\x74\
\xdf\xc0\xb5\xfa\xba\xfe\x33\xa7\xd9\xd9\x59\x26\x27\x27\x89\xe3\
\x98\x1b\xc9\x2e\x5d\xba\xc4\x3e\x35\x87\xca\x0f\x10\x14\x7a\x19\
\x1a\x1e\x26\x0c\xc3\x95\x81\xfc\xbf\xda\xa7\xdf\x34\xde\x68\xf6\
\x3f\x3a\x85\xad\xf2\x55\x15\xc7\x4f\x00\x00\x00\x00\x49\x45\x4e\
\x44\xae\x42\x60\x82\
\x00\x00\x0b\x9d\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x34\x00\x00\x00\x34\x08\x06\x00\x00\x00\xc5\x78\x1b\xeb\
\x00\x00\x01\x85\x69\x43\x43\x50\x49\x43\x43\x20\x70\x72\x6f\x66\
\x69\x6c\x65\x00\x00\x28\x91\x7d\x91\xbd\x4b\xc3\x50\x14\xc5\x4f\
\x53\x8b\x22\x55\x41\x3b\x88\x88\x64\xa8\x4e\x76\x51\x11\xc7\x52\
\xc5\x22\x58\x28\x6d\x85\x56\x1d\x4c\x5e\xfa\x05\x4d\x1a\x92\x14\
\x17\x47\xc1\xb5\xe0\xe0\xc7\x62\xd5\xc1\xc5\x59\x57\x07\x57\x41\
\x10\xfc\x00\xf1\x0f\x10\x27\x45\x17\x29\xf1\xbe\xa4\xd0\x22\xc6\
\x0b\x8f\xf7\xe3\xbc\x7b\x0e\xef\xdd\x07\x08\x8d\x0a\x53\xcd\xae\
\x28\xa0\x6a\x96\x91\x8a\xc7\xc4\x6c\x6e\x55\xec\x7e\x85\x0f\x83\
\xe8\x47\x00\x63\x12\x33\xf5\x44\x7a\x31\x03\xcf\xfa\xba\xa7\x6e\
\xaa\xbb\x08\xcf\xf2\xee\xfb\xb3\xfa\x94\xbc\xc9\x00\x9f\x48\x1c\
\x65\xba\x61\x11\x6f\x10\xcf\x6e\x5a\x3a\xe7\x7d\xe2\x10\x2b\x49\
\x0a\xf1\x39\xf1\xa4\x41\x17\x24\x7e\xe4\xba\xec\xf2\x1b\xe7\xa2\
\xc3\x02\xcf\x0c\x19\x99\xd4\x3c\x71\x88\x58\x2c\x76\xb0\xdc\xc1\
\xac\x64\xa8\xc4\x33\xc4\x61\x45\xd5\x28\x5f\xc8\xba\xac\x70\xde\
\xe2\xac\x56\x6a\xac\x75\x4f\xfe\xc2\x60\x5e\x5b\x49\x73\x9d\xd6\
\x28\xe2\x58\x42\x02\x49\x88\x90\x51\x43\x19\x15\x58\x88\xd0\xae\
\x91\x62\x22\x45\xe7\x31\x0f\xff\x88\xe3\x4f\x92\x4b\x26\x57\x19\
\x8c\x1c\x0b\xa8\x42\x85\xe4\xf8\xc1\xff\xe0\xf7\x6c\xcd\xc2\xf4\
\x94\x9b\x14\x8c\x01\x81\x17\xdb\xfe\x18\x07\xba\x77\x81\x66\xdd\
\xb6\xbf\x8f\x6d\xbb\x79\x02\xf8\x9f\x81\x2b\xad\xed\xaf\x36\x80\
\xb9\x4f\xd2\xeb\x6d\x2d\x7c\x04\x0c\x6c\x03\x17\xd7\x6d\x4d\xde\
\x03\x2e\x77\x80\xe1\x27\x5d\x32\x24\x47\xf2\xd3\x12\x0a\x05\xe0\
\xfd\x8c\xbe\x29\x07\x0c\xdd\x02\xbd\x6b\xee\xdc\x5a\xe7\x38\x7d\
\x00\x32\x34\xab\xe5\x1b\xe0\xe0\x10\x98\x28\x52\xf6\xba\xc7\xbb\
\x7b\x3a\xe7\xf6\x6f\x4f\x6b\x7e\x3f\x6c\xb4\x72\xa4\x74\x35\xf5\
\x28\x00\x00\x00\x06\x62\x4b\x47\x44\x00\xff\x00\xff\x00\xff\xa0\
\xbd\xa7\x93\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x2e\x23\x00\
\x00\x2e\x23\x01\x78\xa5\x3f\x76\x00\x00\x09\xac\x49\x44\x41\x54\
\x68\xde\xed\x9a\x4b\xac\x5d\x55\x19\xc7\x7f\x7b\x9f\x73\xcf\x39\
\xf7\xb6\xbd\xf4\x11\xd2\x27\x28\x94\x56\xb0\x4a\xc5\xd2\x52\xa3\
\x80\xc6\x18\xc3\x44\x07\x0e\x34\x4e\x4c\x34\x1a\x26\x26\x24\x26\
\xc6\x88\x06\x06\x6a\x62\x18\xe8\xc0\x10\x8d\x03\x27\x80\x1d\x19\
\x22\x10\xc3\x80\x18\x83\x0a\xa2\x36\x48\x09\x08\x81\x96\x96\xb4\
\xf4\x7d\xdf\xf7\x9e\xbd\xd6\xf7\x70\xb0\xf6\x3e\x8f\xfb\xea\x39\
\xa4\x2d\x86\xb0\x6e\x76\xee\xbe\xfb\x9c\xb3\xcf\xfe\xaf\xef\xff\
\xfd\xbf\xff\xb7\xd6\xcd\x00\xe7\x7d\x34\x72\xde\x67\xe3\x03\x40\
\xff\xef\xa3\xbe\xf8\xc2\x0b\x47\xa7\x78\xe0\xd0\x1b\x4c\xce\xc5\
\x25\x6f\xbe\x6d\xfd\x3b\x6c\x18\x59\x58\x72\xfd\x33\xfb\x6f\x66\
\xcf\xae\x1d\x97\xed\xa1\xa6\xe7\x95\x6f\xff\xf6\xf8\x92\xeb\x3f\
\xf9\xfa\x6e\x3e\xbf\x67\xe3\x70\x80\x1e\x38\xf4\x06\xf7\x7d\x65\
\x37\xeb\xd7\x36\x96\xbc\xf9\xa1\x87\x8f\xf2\xf7\xb7\xce\x93\xe7\
\xdd\x8f\x4d\xcd\x9c\x65\xe7\x8d\xd7\xf3\x85\x83\x9b\x2e\x1b\xa0\
\x56\x6d\x8e\x73\xff\x7e\x9a\x0d\xfb\xef\xe6\x57\xf7\x7e\x0a\x80\
\xdf\x3c\xf6\x1c\x3f\x78\xe8\x11\x1e\xfc\xd3\x5b\x7c\x92\x63\x7c\
\xe9\x9e\xcf\x0d\x06\x68\x66\x41\x58\x3b\x5a\xe7\x82\xd7\x09\x8b\
\xf4\x6f\x4e\x9c\x20\x4e\x9e\x77\x5f\x68\x07\xc5\xcc\xa9\xe5\xfd\
\xec\x55\x55\x54\xb5\x3c\x87\x42\x14\x41\x40\x41\xc5\x88\x16\xf1\
\x60\x04\x0f\x78\x80\x80\xe3\x1e\x08\xc1\x99\x9a\x99\x06\x29\x70\
\x9c\x23\x13\x06\xc0\xee\x83\xb7\x70\x76\x6e\x86\xc7\x0f\x3d\x81\
\x7d\xf9\x6e\x4e\x9c\xb9\xc8\xf5\x9b\x37\x5e\x1a\x50\x35\xa2\x43\
\xb4\xfe\x6b\xb6\xca\xac\xaa\xa6\xa3\xfc\x0b\x77\x29\xcf\x40\x1c\
\xcc\x1c\xc5\xc0\x8c\xc3\x47\x8e\xf2\xd3\x5f\x3f\x0d\xee\xa9\x66\
\x38\x38\xce\xb6\xcd\xeb\xf9\xdd\xcf\xbf\xc9\xf3\x2f\x5e\x48\xb7\
\x71\x98\x9a\x6f\xa7\x07\x6d\x8c\x70\xf0\xb3\xb7\xf3\x5c\x08\x3c\
\xf9\xc7\xbf\x90\xf9\x9d\xbc\x33\x51\xb0\x75\x43\xf3\xca\x88\x82\
\xbb\xe2\x1e\xca\x43\x7b\x90\x82\x54\xd1\x31\x30\x71\x66\x43\xe4\
\xf4\xc4\x1c\x67\x02\x9c\x0d\x70\x36\xc2\xb9\x98\x31\x21\x19\x8d\
\x91\x11\x42\xd1\x7b\x5f\xc7\xdd\x99\x2d\x9c\x98\x37\xd8\x73\xe7\
\x1d\x6c\xda\xbe\x9d\x27\x9f\xfa\x1b\x7f\x78\xf9\x22\xdf\xf8\xd6\
\x77\xae\x94\xca\x79\xdf\xa1\x40\xa1\x20\xd2\x8d\x00\x0e\xee\x3d\
\x95\x3c\xcf\x17\x1d\xb5\x12\x44\xf7\x8e\xb3\x45\x02\xa3\x0e\x5a\
\x04\x1a\xb5\x9c\x8f\xee\xdf\xcb\xc6\x2d\x5b\x79\xe4\xd1\x27\xb9\
\xff\x81\x9f\x0d\x46\xb9\x61\x87\x08\x84\xb0\xe8\x1a\x8a\x94\xd4\
\x4b\xd1\xb1\x14\xa9\x21\x86\x3a\x78\x00\x3c\x10\xdd\x70\x60\xa4\
\xd6\xa2\xd1\x6c\x32\x39\x39\x85\x88\x5c\x21\x40\x08\x85\xc7\x45\
\x31\x4b\x3f\x18\x58\x34\xa2\x47\xdc\x1c\xe2\x10\x71\x0f\x81\x68\
\xe0\xc1\xa8\x98\xe8\x96\x26\xcf\x9d\xc1\x45\xe1\xdd\x10\xce\x16\
\xcb\x86\xa6\xc3\xbc\x0b\xc6\xa2\x75\xa3\x36\xc0\x4d\x83\x19\x45\
\x28\x23\x0c\x84\x92\x06\x66\xbe\xac\x0b\xbd\x6c\x80\x10\x20\xf4\
\xa3\x51\xd7\x44\x19\xbc\x03\x26\x7a\xc4\x57\xd5\xcb\xfe\x49\x2a\
\x02\x98\xf5\x02\xb1\xce\x6b\x03\xd5\xa1\x77\x3b\xd4\x85\x60\x61\
\x29\xe1\x2c\x81\xed\x8d\xd2\xe0\x69\xe4\xb4\xdb\xfd\x40\x62\x2c\
\xa9\xe6\x57\x18\x90\xab\x63\x61\xf1\xcc\x2b\xe6\x8a\x94\x51\x52\
\x73\x44\x40\x6c\x35\xf9\x77\x42\xec\x26\x59\x07\x48\x28\x69\x6d\
\x5c\x9e\x08\x89\x48\x9a\xdd\x95\x5e\x77\x5d\x14\xa1\xfe\x28\x99\
\xa4\xc0\x98\x19\x76\x89\x10\x55\x20\xa0\xab\x9c\xd5\x25\x21\xe2\
\xd1\x89\x21\xe0\xcb\xa8\x42\x7d\x20\x20\xee\x98\x95\x8a\xb5\x5a\
\x84\x7a\xac\x85\x95\x9a\x50\x4d\xa7\x9b\x61\x24\x9b\x24\x3a\x78\
\x4f\x59\x01\x89\x65\xd4\x0c\x45\x14\xd4\x6c\xf0\x08\x2d\x90\x94\
\x35\x8a\x60\xaa\xcb\xca\xe3\x92\x1c\x32\x88\xda\x6f\x93\xbc\x07\
\x96\x99\xa3\x6a\xb8\xc3\xcd\x37\x6e\xe3\x97\x3f\xfc\x2a\x59\xbd\
\xff\xeb\xc7\x5a\x8d\x25\xaa\xd0\x01\xa2\x8a\x74\xd4\x74\x08\xb7\
\x5d\x09\x96\x8a\xa0\xa2\xcb\x44\xac\x20\xcb\xba\xd4\x6a\x8c\x34\
\x78\xe1\xa5\x63\x5c\xb7\x69\x8c\xcd\xd7\x8e\xf7\xcd\xac\x6a\xf7\
\xeb\xdd\xab\xd9\x36\xc6\x5a\x19\xd7\x6e\x58\xdf\x97\x37\x55\x81\
\x3c\xf2\xdf\xa3\xbc\x7a\xec\x74\x27\x4f\x42\xd7\x20\xa2\xa5\x28\
\xf4\xba\x89\x81\x29\xe7\x6a\x7d\x37\x32\x81\x1d\x1f\xda\xc6\xd9\
\x13\xa7\x98\x9d\x9c\xee\xf3\x4e\xff\x3c\x7c\x94\x0b\x67\x2e\xb2\
\x71\xfd\xda\xee\xe7\x0d\x96\x4f\x39\xc7\x5d\xe9\x63\x8c\x83\x5a\
\xe5\xcc\x9d\x93\xe7\x26\x97\x05\x51\x99\x60\x2f\xd3\x60\x68\x51\
\x10\xc0\x25\x3d\x98\x18\xec\xfa\xd8\xcd\xac\x5b\x37\xce\xdc\xcc\
\x6c\x47\x20\x82\x3a\x15\xf6\x19\xab\x92\x5e\xcb\x08\x75\x93\x5c\
\x35\xd9\x16\xf5\xf2\xc6\xb5\x34\xcb\xa2\x0e\x99\x40\x5e\xaa\x79\
\x1d\xd8\xbe\x9d\xad\x5b\x72\xb2\xf1\x71\x62\xec\xde\xc7\x45\x50\
\x77\x5c\x15\x89\x3e\x9c\x53\x50\x40\x05\x44\x4b\xba\x00\x6b\xc6\
\xc7\xb9\x61\xcf\x5a\xcc\x2c\xc9\xab\x42\x21\x8e\x49\x9a\x61\x73\
\x43\xc4\x91\x32\x57\x44\x0c\x55\xc5\xdc\x89\x62\x98\xa6\xc9\x71\
\x75\x54\x04\xa3\xca\x3b\xed\x80\xed\x58\x33\x2d\x9f\x41\xbb\x79\
\x84\x6a\x47\x68\x44\x97\x97\xee\x95\x01\x95\x60\xd4\x93\x38\x54\
\x4d\x5b\x05\xc4\xdc\x89\x01\xa2\x29\xa6\x9e\x1e\xde\x0d\xb3\x04\
\xc4\xcc\x10\x49\x87\x55\xfd\x52\x34\x1c\x43\xdc\x93\xd8\x94\x20\
\x3a\x11\xe8\x39\xaf\x72\xca\xdd\x3b\x8d\x62\xf7\xd9\x64\x38\x51\
\xa8\x66\xa0\x88\x92\xbe\x74\x55\x20\x8a\xba\x97\xd4\x30\xa0\x07\
\x88\xa5\x19\x37\x4b\x00\xa3\x25\x40\xe6\xa4\x68\xf5\x82\x28\xa9\
\xa4\x2b\x80\xe8\x75\xd5\x2a\x92\x72\x81\x21\xea\x50\x50\x41\x56\
\x00\xe2\xea\x04\x29\xa9\x14\x15\x55\x5f\x14\x99\x74\xee\x18\x52\
\xe6\x95\x63\xdd\x68\x54\x80\x7a\x40\xf4\x02\x5a\x11\x44\xd9\xa7\
\x24\xe7\x23\x43\xc8\x76\xd9\x65\x16\xe2\x98\x3b\x21\x28\x31\x3a\
\x6f\x1f\x3f\xcd\xec\xfc\x1c\x86\x77\xf2\xa1\x9a\xfd\x4a\xaa\xcd\
\x4a\x85\x33\xc3\x16\xf9\xef\x5e\x4a\xb1\x02\x88\x25\xd4\x12\x68\
\xae\x5d\xdb\x77\xcd\x57\xd1\xed\xfa\x4a\xf9\x53\x14\xd0\x6e\x4b\
\xe2\x7b\x50\x8e\x1f\x3f\xcd\x99\x53\xa7\xd8\xba\x65\x03\x6b\xd7\
\x8d\x95\xc5\xd3\x30\x5d\x6a\xe3\xad\x22\x43\x09\x8e\x01\x0a\xe2\
\x4a\x16\xe8\x1f\x2f\xbf\x81\x4f\x16\xd4\xd7\x8e\x93\x91\x75\xa2\
\x26\xcb\x33\x6e\x65\xca\xcd\x17\xd2\x01\x24\x41\x39\x76\xfc\x24\
\xb7\xee\xde\xcc\x27\xf6\xee\xa6\x35\xda\xc4\xdd\x29\x4c\x11\x71\
\x54\xd2\x4a\x8e\xb8\x25\xc7\x20\xa9\x8f\x31\x35\x3c\xa6\x45\x12\
\x11\x4f\x74\x1d\x02\x98\x99\x33\xb2\x69\x8a\xf6\xf1\x13\xb4\x5a\
\x63\x64\x64\x78\x0f\xf5\x18\xc6\xcb\x15\x2a\xcc\x15\x52\x5a\x96\
\x94\x4b\x3b\x77\xee\x60\xa4\xd5\x62\x72\xb6\x8d\x99\x31\x1f\x9d\
\xa8\xa9\xf0\xb5\xdb\x91\x42\x95\x42\xa0\xdd\x86\x42\x04\x11\x49\
\xd1\xd6\x32\xda\x31\x52\x76\x13\x03\x8f\x35\xa3\x5b\x98\xab\x9f\
\x2a\x73\x27\x2b\xf5\xbc\x2a\x66\xc3\x88\x42\xa1\xb4\xdb\xdd\x8a\
\xec\x0e\x13\x53\x6d\x34\x9f\x67\xa1\x08\xb8\x38\x6d\x71\x62\x29\
\x06\x21\x08\xd1\x8c\x50\xae\x2d\x14\xa2\x88\x44\x5c\x53\xad\x91\
\x98\x6a\xd2\xd0\x5b\x1d\xb5\x1c\xea\x23\xb8\x28\x59\x96\x01\x11\
\x17\x52\x81\x1d\x46\xb6\x8b\x42\x69\x47\xa1\xb3\xc6\xe1\xb0\x21\
\x37\xae\x1b\x35\xb4\x55\x03\x49\x13\x65\xa5\x71\x34\xcb\x53\xbd\
\xb1\xa4\x60\x62\x86\x6a\xa3\xb3\xd0\x11\x75\xf8\x1e\x2b\x03\xbc\
\x5e\xe7\xd1\xe3\x89\x62\x2b\xcb\xc7\x80\x80\x0a\x11\x5c\x3c\xad\
\x0b\x98\x71\xd7\xce\x35\x1c\xfc\xc8\xe5\x5b\xf2\x1d\xa8\x13\x36\
\xe7\xf7\x4f\x90\x1a\x45\x62\xa7\x27\x59\xa9\x95\x59\x16\x90\x01\
\x41\x84\x58\x78\xb2\x2a\xd2\x6f\x34\x4f\x9d\x3e\x4d\xbb\x28\xa8\
\xe7\x75\x44\x85\x28\x31\xf5\x43\x55\xdf\xe3\x5e\xca\xb9\xe2\xe6\
\x68\xf9\xb7\x97\xbf\x07\xda\x45\xa8\xd7\x38\xb0\xef\xb6\x9e\x52\
\x92\xec\x8f\x57\xa1\xd6\x21\xdb\x87\xc2\x1c\x29\x8c\x68\xde\xa9\
\xe8\xd5\x38\x7f\xe1\x02\x53\xb3\xb3\x34\x6b\x0d\xda\xa1\x60\xa1\
\x58\xc0\x82\x96\x74\x33\xd4\x94\xa8\x86\xc6\x88\xa9\x12\xcd\x50\
\xad\x04\x66\x30\x49\x68\x34\x1a\x7d\x80\x3a\x40\xca\x35\x30\x37\
\x1d\x4e\xb6\x43\x61\x14\x21\x22\x65\xf2\x59\x0f\xa2\x5b\xf7\xec\
\x79\x0f\x76\x7e\x62\xb7\xd1\x72\x27\xcf\x22\x96\x0d\xa1\x72\x31\
\x0a\xb1\x97\x22\x3d\x80\xce\x9e\x3f\x4f\x08\x81\x5a\x5e\x43\x54\
\x11\x15\x5c\x93\x9d\x77\x4f\xd4\x4a\x36\xdf\x70\xb7\x74\x6e\xd5\
\xfa\xc2\x60\x94\xab\xd5\x6a\x7c\x7c\xcf\x2d\x4b\x7a\x71\x2f\x17\
\x19\x46\xa2\x2f\xd9\x1d\x59\x15\x50\x65\x69\x24\x46\x5c\xb5\xef\
\x41\xde\x3e\x79\x92\xa9\x99\x19\x9a\xf5\x26\xed\xa2\xcd\x7c\x7b\
\xbe\x43\xb9\xb4\x8d\x62\x44\x55\x24\x06\x4c\x12\xe5\xa4\xa4\x9c\
\xc8\x60\x94\x6b\x36\x1b\x7d\x80\xbc\xb3\x7e\xd5\xf1\x28\x43\xba\
\xed\x18\x89\xed\x76\xca\x9f\x18\xfb\x3a\xc4\x7d\x7b\xf7\xbe\x47\
\x1b\x8e\xd5\x22\xa3\x10\x89\xc3\x15\x56\xf3\x94\xd4\x55\x0e\xf5\
\x7e\x74\x62\x72\x92\x10\x23\xb5\xbc\x86\x96\x94\xeb\xec\x2c\x94\
\xdb\x1f\xe6\x89\x5e\x9d\xf3\x9e\x63\x90\x91\xe7\x39\xbb\x76\xde\
\xd0\x07\xc6\x89\x70\x09\xca\xae\x9c\x43\x21\x12\x7b\xad\x71\xcf\
\x83\xbc\xfe\xe6\x9b\x4c\x4e\x4f\xd3\xaa\xb7\x58\x68\x2f\x30\xd7\
\x9e\x43\x83\x96\x9b\x5e\x69\xe7\x2e\xa8\xa2\x21\x74\xce\x45\xb4\
\x6c\x2d\x06\x5b\xa9\x6f\xb5\x9a\x7c\xef\xbb\xf7\xf6\xac\x51\x14\
\xc9\x9d\xf7\x51\x6f\x88\x3a\x24\x73\xe7\x89\x13\x13\xe0\x4e\x6d\
\xec\x9a\xae\x6d\x06\xee\xd8\xb7\xef\xaa\x93\xcd\x43\xc0\xc2\x6c\
\x37\x82\xf5\x51\xc8\xf2\xc1\x00\x05\x60\xea\xc8\x53\x5c\x38\x75\
\x1e\x77\xd8\x74\xeb\x17\xa1\xb5\xae\xbb\x0f\x3b\x3b\x8b\x88\x90\
\x67\x39\x5a\x15\x50\xaf\xd6\x9c\x93\x9a\x59\x79\x21\xd1\xac\xa4\
\x22\x43\x50\x2e\xcb\xd9\xb1\x7d\x6b\xff\x73\x5d\x7c\x95\x66\x6b\
\x34\x79\xba\x35\x37\x41\xad\x31\xdc\xaa\xcf\xd4\xdc\x35\x88\xd5\
\x19\x6f\xd7\xa8\xf7\x7c\xf6\xa5\x57\x5e\xe1\xe2\xe4\x24\xa3\xf5\
\x51\xe6\xdb\xf3\xcc\x2e\xcc\x62\xa1\x5c\xd1\x94\x44\xb9\x42\x15\
\x2d\x0a\x54\x85\x42\x0d\x11\xc1\x4c\x91\x28\x03\x53\xee\x47\xdf\
\xbf\xaf\x9f\xf2\x0e\x7b\x6e\xbf\x9b\xf1\xd1\x06\x2f\xfe\xe7\x0c\
\x6d\xd7\xc1\x01\x65\x8d\x35\xd4\xc7\x02\x99\xd6\xd0\x9a\x52\xc3\
\x98\x9e\x2b\x88\xa2\x7c\xfa\xc0\x81\xab\x43\x33\x87\x8b\xd3\x73\
\x49\x90\x8a\x40\x96\x37\xd8\xba\x73\x17\x07\xb6\x8d\xf0\xda\x6b\
\x17\x68\xb7\x87\x00\x34\x76\xd3\xdd\x6c\xdf\x38\x4b\xef\x5a\xff\
\xa1\x67\x0e\x33\x56\x57\x3e\xbc\x65\xe3\x55\x01\x24\x62\x3c\xfc\
\xf8\xb3\x58\x4c\x12\xdd\x1c\xdf\xcd\x33\x8f\xff\x99\x67\x92\x39\
\x82\xe6\x00\x39\x74\xcd\x58\x9d\xb9\xf9\x98\xcc\x64\xa8\xda\xeb\
\x40\x36\x52\xe7\xaf\x87\x4f\xf0\xec\xf3\xaf\x5f\x62\x8b\x8a\x65\
\x95\xf1\xd2\x1f\xf1\x4b\x87\xab\xf7\x77\x3e\xa0\xca\x3d\xf8\xb5\
\x5d\xfc\xf8\xb1\xd7\x99\x3c\x37\x0d\x3d\xdb\x23\x1e\x94\xbc\xb5\
\x06\xcf\x1b\x2b\xd6\x82\xb4\x12\xa3\x7d\xeb\xb6\xbe\x9a\x33\x30\
\xd2\x3f\x44\xe0\x5c\x72\xe3\x35\xcb\xba\xd6\xc7\x9d\x6c\x5d\x93\
\x66\xb3\x4e\x9e\x67\xab\x03\xda\x7f\xc3\x38\xff\x3a\x36\xcd\xfd\
\xbf\x78\x91\xf3\x13\xb3\xcb\x98\xac\xf2\x58\x59\x9f\xba\xa7\x23\
\x39\x30\x72\xc5\x28\x79\xcf\x5d\xbb\x19\x5b\x44\xbb\x8c\x0f\xfe\
\x01\xf0\x03\x40\x57\x75\xfc\x0f\xa7\x55\x3a\xf4\x35\xfb\x29\xff\
\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
\x00\x00\x11\xaf\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x3a\x00\x00\x00\x37\x08\x06\x00\x00\x00\x5d\x25\x59\xf6\
\x00\x00\x01\x85\x69\x43\x43\x50\x49\x43\x43\x20\x70\x72\x6f\x66\
\x69\x6c\x65\x00\x00\x28\x91\x7d\x91\xbd\x4b\xc3\x50\x14\xc5\x4f\
\x53\x8b\x22\x55\x41\x3b\x88\x88\x64\xa8\x4e\x76\x51\x11\xc7\x52\
\xc5\x22\x58\x28\x6d\x85\x56\x1d\x4c\x5e\xfa\x05\x4d\x1a\x92\x14\
\x17\x47\xc1\xb5\xe0\xe0\xc7\x62\xd5\xc1\xc5\x59\x57\x07\x57\x41\
\x10\xfc\x00\xf1\x0f\x10\x27\x45\x17\x29\xf1\xbe\xa4\xd0\x22\xc6\
\x0b\x8f\xf7\xe3\xbc\x7b\x0e\xef\xdd\x07\x08\x8d\x0a\x53\xcd\xae\
\x28\xa0\x6a\x96\x91\x8a\xc7\xc4\x6c\x6e\x55\xec\x7e\x85\x0f\x83\
\xe8\x47\x00\x63\x12\x33\xf5\x44\x7a\x31\x03\xcf\xfa\xba\xa7\x6e\
\xaa\xbb\x08\xcf\xf2\xee\xfb\xb3\xfa\x94\xbc\xc9\x00\x9f\x48\x1c\
\x65\xba\x61\x11\x6f\x10\xcf\x6e\x5a\x3a\xe7\x7d\xe2\x10\x2b\x49\
\x0a\xf1\x39\xf1\xa4\x41\x17\x24\x7e\xe4\xba\xec\xf2\x1b\xe7\xa2\
\xc3\x02\xcf\x0c\x19\x99\xd4\x3c\x71\x88\x58\x2c\x76\xb0\xdc\xc1\
\xac\x64\xa8\xc4\x33\xc4\x61\x45\xd5\x28\x5f\xc8\xba\xac\x70\xde\
\xe2\xac\x56\x6a\xac\x75\x4f\xfe\xc2\x60\x5e\x5b\x49\x73\x9d\xd6\
\x28\xe2\x58\x42\x02\x49\x88\x90\x51\x43\x19\x15\x58\x88\xd0\xae\
\x91\x62\x22\x45\xe7\x31\x0f\xff\x88\xe3\x4f\x92\x4b\x26\x57\x19\
\x8c\x1c\x0b\xa8\x42\x85\xe4\xf8\xc1\xff\xe0\xf7\x6c\xcd\xc2\xf4\
\x94\x9b\x14\x8c\x01\x81\x17\xdb\xfe\x18\x07\xba\x77\x81\x66\xdd\
\xb6\xbf\x8f\x6d\xbb\x79\x02\xf8\x9f\x81\x2b\xad\xed\xaf\x36\x80\
\xb9\x4f\xd2\xeb\x6d\x2d\x7c\x04\x0c\x6c\x03\x17\xd7\x6d\x4d\xde\
\x03\x2e\x77\x80\xe1\x27\x5d\x32\x24\x47\xf2\xd3\x12\x0a\x05\xe0\
\xfd\x8c\xbe\x29\x07\x0c\xdd\x02\xbd\x6b\xee\xdc\x5a\xe7\x38\x7d\
\x00\x32\x34\xab\xe5\x1b\xe0\xe0\x10\x98\x28\x52\xf6\xba\xc7\xbb\
\x7b\x3a\xe7\xf6\x6f\x4f\x6b\x7e\x3f\x6c\xb4\x72\xa4\x74\x35\xf5\
\x28\x00\x00\x00\x06\x62\x4b\x47\x44\x00\x16\x00\x16\x00\x73\xc7\
\x44\x26\x19\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x2e\x23\x00\
\x00\x2e\x23\x01\x78\xa5\x3f\x76\x00\x00\x00\x07\x74\x49\x4d\x45\
\x07\xea\x02\x09\x0f\x14\x06\xb0\x52\xbb\xf3\x00\x00\x00\x19\x74\
\x45\x58\x74\x43\x6f\x6d\x6d\x65\x6e\x74\x00\x43\x72\x65\x61\x74\
\x65\x64\x20\x77\x69\x74\x68\x20\x47\x49\x4d\x50\x57\x81\x0e\x17\
\x00\x00\x0f\x86\x49\x44\x41\x54\x68\xde\xed\x9a\xf9\x6f\x5c\xd7\
\x75\xc7\x3f\xf7\xad\xb3\xcf\x70\x86\xc3\x5d\x24\x45\x6a\xb5\x64\
\x59\x56\xe2\x2d\x4a\x62\xcb\x8e\xed\x3a\x75\x8c\xa0\x2d\x8a\xb6\
\x28\xfa\x53\xff\x96\xfe\xd0\xbf\x21\x6e\x81\xfe\xd0\x02\x4d\x82\
\x14\x68\x62\xc0\x71\xd2\xa4\xae\xd3\x54\x56\xec\x48\x5e\xb4\x50\
\x14\x49\x51\xdc\x67\xe1\xcc\x70\xd6\xf7\xde\xbd\xb7\x3f\x0c\x97\
\x21\x35\xa4\x28\x59\x0e\x5a\x24\x17\x38\x7c\x98\xc7\x99\xf7\xee\
\xf7\x9e\x73\xcf\xf9\x9e\x73\xae\xd0\x5a\x6b\x7e\x0f\x86\xc1\xef\
\xc9\xf8\xbd\x01\x6a\x7d\x59\x0f\x5e\xaf\x34\xb9\x79\xbb\xc0\xed\
\xf9\x12\x33\xf7\x4a\xac\xae\x6d\x90\x2b\x54\x69\x79\x72\xfb\x3b\
\xc9\xb8\x4b\x6f\x26\xc6\xc8\x50\x82\xc9\xe1\x14\xa7\x8f\x67\x18\
\x1b\x4e\x12\x0e\x3d\xfe\x69\x89\xc7\xb9\x47\x9b\x4d\x9f\x6b\xd7\
\x73\xfc\xf4\xfd\x69\x6e\xcc\x56\x70\x2c\xe8\x1b\x4d\xd0\x37\x98\
\x22\x99\x0c\xd3\x93\x89\x63\x87\xad\x6d\x3b\xd2\xad\x80\xf2\x7a\
\x93\xb5\xa5\x12\xb9\x85\x22\xf9\x42\x1d\xc7\x32\x78\xe6\xdc\x10\
\x2f\x3d\x3f\xc6\xe8\x70\x02\xdb\x36\xff\xef\x00\x6d\x36\x7d\x7e\
\xf1\xe1\x22\xef\xfc\xe2\x36\x8d\xba\xc7\x91\xe3\x83\x1c\x39\x91\
\x26\x33\x94\x24\x1a\xb3\xb1\x2c\x81\x10\x02\xc3\x10\x20\x3a\x7e\
\xa8\x41\x6b\x8d\xa1\x34\x42\x69\x6a\x35\x9f\xd5\xb9\x75\xee\xde\
\xcc\xb1\xba\x5c\x61\x74\x24\xc9\xeb\x2f\x1e\xe5\xf4\x44\xfa\x0b\
\x03\xfe\xc2\x40\x3f\xf8\xf0\x2e\x3f\x7c\x77\x8a\xba\x27\x39\x7e\
\x76\x84\xa3\x4f\x0e\x12\xc9\xb8\x98\xb6\x81\x6b\x18\x98\xe2\x70\
\xfb\xc7\x04\xb4\x06\x25\x15\x32\x50\x94\x0b\x75\x6e\x7d\xb2\xc4\
\xdc\xed\x3c\xa7\xc6\xd2\x7c\xfb\xe5\x49\xc6\x46\x92\xbf\x7b\xa0\
\xc5\x72\x93\xb7\xff\xf9\x63\x6e\xcc\x16\x99\x38\x33\xc8\xc9\xaf\
\x8c\x12\xcb\x86\xb1\x5c\x13\x61\xb4\xd1\x39\xfa\xf0\xde\x6e\x6b\
\x3d\xcc\x2d\xd0\x4a\xd3\xa8\x4b\xf2\xab\x65\x6e\x5d\x5b\xa4\x9c\
\xaf\xf3\xea\xd7\xc6\x78\xf1\xd9\xd1\x47\xd2\xee\x23\x01\xbd\x31\
\x5d\xe4\xed\xef\x5f\x25\xd0\x8a\xd3\x17\x8f\x31\x74\xac\x87\x50\
\xd4\xd9\x06\xb8\x35\x1e\x06\xe8\x5e\xc0\x6c\x69\x58\x29\xea\xe5\
\x26\xb3\xd7\x57\x99\xbb\xbe\xca\x85\x13\x7d\xbc\x71\x69\x92\x44\
\xc2\xfd\x72\x81\x5e\xb9\xba\xcc\x3f\xfe\xf0\x13\x7a\x8f\x24\x38\
\xf9\xc2\x24\xe9\x4c\x74\xdf\x15\x6e\xd4\x3d\x1a\x85\x2a\xca\x93\
\xd4\x2b\x75\x7c\x2f\x00\x1f\x82\x96\x8f\x52\x0a\xcb\xb2\x71\x63\
\x0e\x86\x65\x62\x87\x2d\xa2\x71\x97\x48\xc2\xc5\x09\xbb\x98\xa6\
\xd9\x01\x58\xe3\xb7\x24\x2b\x73\x05\x6e\x7f\xb2\xc4\x68\x36\xca\
\x1b\x97\x26\x19\xec\x8b\x7e\x39\x40\xaf\x5c\x5d\xe6\x1f\x7e\x70\
\x8d\x78\x7f\x82\xf3\xaf\x9c\x20\x9e\x8e\xb6\x1d\x0c\xe0\x95\x6a\
\x54\xf3\x4d\x2a\xf9\x2a\xcd\x4a\x03\x2d\x15\xe9\x98\x4d\x22\x6a\
\x11\x8f\xb9\x24\x93\x61\x22\x61\x0b\xc7\x32\x49\x44\x1c\x1c\xdb\
\xa0\xd5\x54\x54\x3d\x9f\x40\x2b\x6a\xb5\x80\x8d\x0d\x8f\x72\xb9\
\x4e\x4b\x41\x28\x1d\x25\xd1\x9f\xc0\x09\x3b\xdb\xef\x97\xbe\x64\
\x69\xb6\xc0\xa7\x57\xee\x32\x36\x10\xe5\x4f\xfe\xe8\x24\x7d\xe9\
\xe8\xe3\x05\xfa\x9b\x6b\xcb\xbc\xfd\xfd\x4f\x88\xf7\xc5\x79\xea\
\xe5\xe3\x24\x7a\x63\x08\x43\xb0\x3e\xbb\xce\xd2\xd4\x12\xa9\x88\
\x4d\x4f\x2a\x4a\x36\x6c\x33\xd0\x1b\x25\x99\x74\x71\x1d\x03\xcb\
\x34\x30\x4d\x03\xd3\x32\x30\x8d\xb6\xf7\xb5\xcc\xf6\x55\x29\x8d\
\x54\x1a\x8d\x46\x49\x4d\x10\x28\x02\xa9\xc8\x97\x9a\xdc\x5b\xae\
\x50\xdc\xf0\xb0\x7a\x22\xc4\xfb\xe2\xd8\x8e\x0d\x40\xe0\x4b\x16\
\x67\xf2\xdc\xbe\xb6\xc8\xc9\x91\x24\x6f\xbe\x72\xec\x50\x66\x7c\
\x28\xa0\xab\xab\x55\xfe\xfe\x7b\x97\x31\xe3\x61\x4e\x5f\x3a\x4e\
\x22\x1b\xdb\xde\x8f\xb9\x9b\x4b\xa4\xaa\x1e\xcf\x9e\x1b\x20\x95\
\x08\xe3\x58\x06\x8e\x6d\x62\x59\x06\x42\x3c\x9a\x87\xf4\x03\x45\
\xb3\x15\x50\x28\x36\xb8\xbd\x50\xa6\xa4\x04\xb1\x81\x04\xe1\x98\
\x8b\x09\x04\x9e\x64\xe1\xce\x1a\x33\x9f\x2d\x72\xfe\x78\x96\x6f\
\xbf\x7c\xec\x81\x0e\xca\x3a\x4c\x8c\xfc\xde\xbf\x5e\xa5\xda\x52\
\x3c\xf7\xe6\x31\xe2\xd9\x18\x18\x02\xe5\xfb\xa0\x35\x4a\x4b\x22\
\x11\x87\xde\x54\x84\x78\xcc\x79\x2c\xc1\xdd\xb6\x0c\x6c\xcb\x21\
\xec\x5a\x44\x23\x36\x9f\xcf\xac\x53\x58\xab\x60\x98\x49\xec\x88\
\x03\xae\x49\x76\x3c\xcd\x46\xa9\xc6\x67\xb7\xf3\xf4\x65\x63\xbc\
\x70\x61\xf8\x8b\x71\xdd\x9f\xfe\xea\x2e\x37\x66\x8a\x3c\xf1\xe2\
\x31\xdc\x54\x14\x3f\x00\xed\xf9\x20\x25\xbe\x32\xd1\x9e\x80\x2f\
\x29\xff\xb1\x2c\x83\x4c\x4f\x98\xb3\x93\x69\x7a\x4d\xa8\xaf\x55\
\x08\x7c\x89\x02\xac\xb0\xc3\x91\x53\x03\xb8\xa9\x30\x9f\xdc\x5c\
\x25\xb7\x5e\x7b\x74\xa0\xa5\x8d\x26\xff\xfe\xde\x2d\x46\xcf\x0c\
\x90\x1a\x4d\x80\x90\x28\xe5\xe3\x2b\x89\x0f\x28\x24\xbe\xd6\x7c\
\x99\x89\x9e\x61\x08\xd2\xa9\x10\x83\xbd\x61\x0c\xcf\xa7\x59\xae\
\x83\x94\x20\x04\xa1\x78\x88\xc1\xb1\x34\xf9\x8a\xc7\xff\x7c\xb4\
\xf8\xe8\xa6\xfb\xee\x7f\xce\x50\x53\x8a\xaf\x3c\x3d\x8e\x12\x06\
\x9e\x27\xb1\x01\x65\x0b\x74\xa0\x11\x96\x42\x1d\x62\xb2\x2b\xf9\
\x2a\x53\x73\x45\x0a\xc5\x06\x32\x50\x24\x63\x21\x86\x06\x63\x8c\
\x0d\x27\x89\x45\x9c\x43\x81\x1d\xec\x8b\xb3\x56\xf6\x58\xa9\xb5\
\x70\xe3\x0e\x86\x94\xa0\x34\x3d\xfd\x71\x72\x2b\x1b\xcc\xdc\x2d\
\x31\xbf\x58\x61\x74\x38\xf1\x70\x1a\x2d\x6f\xb4\x78\xf7\xfd\x3b\
\x9c\x78\xf2\x08\x76\xcc\x46\x29\x50\x0a\x7c\x05\x9e\xaf\xf1\x65\
\xfb\xfa\x20\x6d\x56\xeb\x1e\x1f\x7e\xb6\xc2\xad\x5c\x9d\x42\xd8\
\xa5\x94\x8a\x71\x4f\xc1\xc7\xb7\x8b\x5c\xbd\xbe\x4a\xb9\xd2\x3c\
\x94\x66\xa3\x11\x87\x44\xc8\x42\xf8\x9a\x20\xd0\xf8\x4a\x21\xb5\
\xc6\x70\x4d\xfa\x46\x52\x34\xa4\xe0\xe3\xcf\x96\x1f\x5e\xa3\xef\
\x5f\xb9\x47\xbd\x05\xc3\x67\x47\xf0\x05\xd8\x9b\xf7\xd5\xf6\x9f\
\xcd\xeb\x03\x80\xe6\x8a\x0d\x0a\x35\x09\x3d\x51\xdc\x74\x04\x61\
\x18\x28\x3f\x20\xd8\x68\x32\xbd\x5a\xa3\x37\x15\x21\x1a\x71\xb0\
\x2c\xe3\x81\x5a\x35\x85\xc0\xf3\x7c\x54\xc3\x23\x1c\x76\xd0\x9b\
\x8e\x36\x9a\x89\x62\x27\x43\xcc\x2f\x57\x28\x94\xea\x64\x52\x91\
\xc3\x03\xfd\xaf\xcb\xf3\x0c\x4c\x64\x90\x61\x13\x79\xc0\x04\x1e\
\xb4\x3d\x0b\x85\x5a\xdb\x79\x84\x6c\x84\x61\x20\x81\x86\xb0\xf0\
\x5c\x97\x5c\xb1\xc0\xd0\x72\x85\x91\x81\x18\xb1\xd8\x83\x63\x61\
\xb1\xd2\xe4\xfa\x62\x05\x25\x4d\xdc\x70\x9b\x5f\x5a\x86\xc0\xb5\
\xa0\x64\x99\xa8\x72\x8b\xa9\x99\x22\x2f\x5c\xd8\x0d\x54\x6b\xdd\
\x1d\x68\xa1\x50\x67\x76\x7e\x9d\xe7\xff\xec\x29\x9a\x81\xe6\xa0\
\x80\xe8\xfb\xa0\x0f\xd8\x66\x1b\x8d\x80\x9a\x30\x68\xf9\x0a\xaf\
\xe2\xe3\x6b\x68\x29\xf0\xa5\x22\x57\x6a\x91\xdf\x68\xe2\x4b\x75\
\x28\xf3\xcd\x97\x1a\xcc\xe7\x1b\x18\xc9\x04\x86\x6c\xb5\x35\x2d\
\xc0\x32\x41\x22\x90\x0d\xc9\xed\xb9\x75\x5e\xb8\x30\x72\x38\x8d\
\xde\x9c\xce\x21\x35\xc4\xb2\x71\x6a\x4a\x74\xd5\x9a\xb5\x49\xc0\
\x95\x84\xd9\x7b\xeb\xfc\xa4\xd6\xc0\xee\x30\x3f\xa9\xa0\x5e\xf7\
\xb9\x35\xb7\x4e\x73\xac\x17\x42\x61\x7c\x82\x36\x51\xdf\xb4\x84\
\xfa\x86\x8f\x52\x20\x8c\x07\x53\xff\x6a\xdd\x27\xbf\xde\xa4\xe9\
\x29\xc2\x1a\xa4\x1f\xb4\x17\x1a\x68\x00\x42\x98\x78\x86\x60\x65\
\xad\x4a\xb5\xea\x11\xeb\x88\xe9\x42\x88\xee\x40\x6f\xcc\x16\xe8\
\x1b\x4e\x21\xb1\x08\x02\x1f\xd3\xb2\xf7\x35\x5f\xab\x37\x46\xdd\
\x35\xb8\xab\x14\x42\x41\x2b\x08\xd8\x08\x34\x4d\x0f\x9a\x4d\x68\
\xc6\x13\xb8\x4e\x08\x1d\x28\x74\x87\x8f\x96\xf5\x00\x2b\x08\xc8\
\x26\x43\x44\x42\xf6\x03\x81\x2e\xac\x6c\xb0\x50\x6c\x22\x6d\x9b\
\x40\xc3\xd6\x84\xf4\xa6\xab\x30\x6d\x13\x22\x0e\xe5\xba\xc7\x5a\
\xa1\xbe\x0b\xa8\x52\xfb\x98\xee\xbd\x95\x1a\xbd\x23\x69\xea\xad\
\x80\x40\xab\xfb\x3c\xab\xb5\xf3\x1e\xcc\xb0\x89\x19\xef\x41\x4b\
\x49\xa5\xa9\xa9\xfa\x1e\x75\xa9\x08\x64\x3b\xcd\xb2\x37\x27\xa2\
\x50\xe8\x2d\xdb\x90\x50\xbb\x97\xe3\x64\xc6\x65\x7c\x28\x81\x63\
\x1f\xac\xd1\x96\x27\xb9\x71\x27\xcf\xfc\x86\x87\xd1\xdf\xb3\x6b\
\xd1\x95\x6a\x87\x55\x69\x08\x0c\xc7\xc5\xf7\x7c\x56\x8b\x75\x26\
\xc6\x52\xbb\xea\x57\x5d\x81\x2e\xae\x56\x39\x79\xbc\x9f\xba\x92\
\x58\x42\x20\xa5\x3c\x70\x22\x95\x96\xa6\x11\xf8\x54\x5b\x0a\x5f\
\xef\x06\xd4\xb9\x4a\x12\xd0\x81\xc4\x5f\xd9\xa0\xa7\xd6\xe0\x1b\
\x17\xc7\x18\x19\x4c\x3c\x50\x9b\xd7\xa7\x72\x5c\xbe\xbe\x46\xd9\
\xb6\x31\xc2\x2e\x3a\xd8\x0d\x74\x0b\xac\x6b\x59\xb4\x10\xac\x15\
\x76\xb3\xa4\xd5\x7c\xbd\x3b\xd0\x7c\xb1\xca\xb9\x44\x88\xaa\x6c\
\xef\x4f\xb1\x4d\xc9\x76\x26\x0c\xd0\x0a\xa0\x1a\x04\x6c\xd4\x35\
\xbe\x92\x68\x74\x1b\xcc\x2e\x64\x3b\xcf\xf5\xaa\x1e\xad\xa5\x75\
\x06\x94\xcf\x6b\x17\x86\xf8\xea\xd9\x01\xa2\x91\x83\xcd\x76\x66\
\x7e\x9d\x77\x7f\x3d\xc7\x54\x55\xa2\x46\x32\x68\x0c\x08\x76\x9b\
\xed\x56\xac\x93\x86\xa6\xa9\x35\xf5\x66\xb0\x5b\x11\x55\xaf\x3b\
\x50\xdf\x93\x60\x99\x04\x7e\xbb\xac\xd1\x99\xf1\x6f\x39\xe0\x5a\
\x10\x50\x69\x69\x6a\xbe\x44\x49\xbd\x0d\xa8\x6b\x68\x95\xe0\x17\
\xca\xa8\x95\x0a\x27\xa2\x16\x97\x9e\x19\xe1\x85\xf3\x43\xf4\x24\
\x43\xfb\x02\x94\x52\x71\x7d\x2a\xc7\x3b\x1f\xcc\xf1\xf1\x6a\x83\
\x56\x36\x8d\x19\xb6\xd1\x04\xbb\x42\x9b\x52\x3b\xc1\xdd\x52\xdd\
\x99\x9a\x27\xd5\xc1\x14\x30\xd8\x33\xe9\x60\x53\x95\xf5\x56\x40\
\x25\x08\x68\x06\xf7\x33\x23\x29\x77\x59\x2b\xba\xda\x20\xc8\x55\
\x49\xb5\x1a\x5c\x18\x8b\xf3\xf5\xa7\x87\x38\x35\xd9\x4b\x24\xbc\
\xbf\x26\x8b\xa5\x06\xd7\x6e\xac\xf2\xde\x95\x45\x3e\x2f\xb7\xf0\
\x7a\x13\x88\xa8\x4b\x10\x04\x7b\x74\xd8\x09\xb4\xed\xe9\xbb\x0d\
\x75\x98\x34\x2d\xd8\xeb\xe6\x5b\x01\xe5\x5a\x80\xaf\x74\xd7\xb0\
\xd3\x09\x54\x37\x3c\x82\xd9\x35\xce\xf4\x38\x3c\xff\xe4\x30\x5f\
\x7b\x7a\x90\x6c\x66\xa7\x2a\x71\x9f\xd3\xf1\x25\x53\xb3\x45\x3e\
\xbc\xb6\xcc\xe5\xe9\x22\x0b\xd2\x40\x0f\xa4\xd1\x61\x07\xa5\x14\
\x7b\xd5\xa5\xd8\x7d\x4b\x1d\x90\xb9\x74\x05\x9a\x8c\xbb\xd0\x92\
\x48\xa5\x76\x81\x69\x48\x28\xd4\x02\xfc\x03\x38\x6e\xa7\xe9\x6a\
\x2d\x09\x8a\x15\xbe\xf5\xad\x27\xf9\xe6\xb3\xa3\xb8\x8e\xb5\x2f\
\xc0\xf9\x85\x32\x9f\x4d\x17\xb8\x3c\x95\xe7\xfa\x5a\x93\x7a\x34\
\x8c\x91\x8d\x20\x1c\x8b\x2e\x18\xdb\xcf\xdf\x74\x44\x3b\x55\x04\
\x81\x65\xde\xef\xc1\x1d\xd3\xe8\x0e\xb4\xaf\x37\x46\x50\x6b\x12\
\x84\x42\xe8\x4d\x8f\xdb\xf0\xa0\xec\x6b\x3c\x7f\xef\x3e\xdc\xed\
\x71\x64\xc7\x47\xed\x18\x60\x0a\xd2\xa9\xf0\xbe\x20\xe7\x97\x2a\
\x5c\xbb\x95\xe3\xa3\xa9\x02\x9f\xae\xd4\x28\x3b\x16\x7a\xb0\x07\
\x42\x0e\xd2\xd8\xf1\xac\xba\x0b\x52\xb5\x07\x28\x81\x26\x2c\x04\
\x91\x3d\x2d\x8d\x44\xcc\xe9\x0e\xb4\x37\x13\xa5\x94\xaf\xe0\x8c\
\xc7\xa8\x4b\x89\xe7\x41\xb1\x11\xe0\xe9\xdd\x5e\x17\xc9\xa6\x73\
\xd0\xbb\x6c\x5d\xe9\x8e\x3b\x0f\x20\xc3\xbf\xfa\x68\x81\x1f\xfd\
\x66\x85\xa2\xed\xa2\x32\x49\x54\xd8\x01\xc3\x68\xff\x6e\xf3\x45\
\x4a\xee\x01\xd4\x8d\xb8\x98\x02\x9a\x12\x5b\x29\x7a\x53\xbb\x9d\
\x5c\x7f\x6f\xa4\x7b\x9a\x36\x71\x24\xc5\xe2\x4c\x9e\x94\x6b\xe0\
\x29\x28\x36\x34\x0d\xad\x09\x50\x04\x28\x34\x7e\x5b\x02\x1f\x7c\
\xdd\xe6\x61\x5b\xa2\x77\xe6\x18\x1c\x82\xf4\xcf\x2f\x96\x28\xba\
\x0e\x7a\xa4\x07\x15\x0d\x21\x95\x41\xe0\xb3\x4b\xd4\x21\xa8\xb0\
\x6b\x1b\x38\x28\x4c\x25\x49\xef\x01\xda\x93\x08\x75\x07\x7a\xf2\
\x68\x9a\x72\xae\x4e\xd8\x52\x34\x5a\xd0\xd4\x6d\x3e\x24\xb0\x11\
\xd8\x3b\x4d\x04\xd3\xdc\x29\xad\x9b\x3b\x01\xb7\xcb\xad\x07\x37\
\x2f\x8d\xcd\xc7\x59\x9b\xd7\x0e\x39\x4c\x91\xcd\xd6\x0a\x5b\x7a\
\xc4\xc2\x16\xfd\xd9\xd8\x7d\x29\x5e\x57\xd3\x3d\x7e\xb4\x07\xd7\
\x36\xa9\x2c\xac\xe3\xc9\x30\xc6\x1e\xcd\x6c\x47\x25\x0b\x34\x62\
\xe7\xbf\xdb\x2a\x54\x98\x9b\xf6\x7b\xb8\xbc\x64\x67\x98\x5b\x2b\
\xd4\xf9\xbe\x2e\xa6\xab\xf4\xce\xbe\x15\x02\x8c\x56\x8b\xa8\x1f\
\x30\x34\x9a\x26\x9d\x0c\x1f\x2e\x4d\x4b\xc4\x5c\xce\x1e\x4b\x33\
\x37\xb5\x46\xec\xcc\x38\x7e\x7d\xb7\x97\xdd\xed\x7e\xac\x1d\x30\
\xd6\xd6\xb6\x0c\x20\xd8\xda\xa8\x82\xd5\x7c\x9d\xb9\xc5\xca\x4e\
\xb5\x20\x6c\x61\x6f\xf2\x5b\xdf\x97\x18\xb4\x19\x98\xde\xc7\xd4\
\x0d\xb3\x2d\x74\xe1\xb8\x00\xae\x25\xb0\x2a\x1e\x49\x60\xe2\x48\
\xcf\xc3\x55\x18\x5e\xbe\x38\xce\xdf\xbd\x7d\x85\xd3\xe7\x27\xd8\
\x30\x25\x7e\x47\x40\x35\xef\x27\x3e\x7b\x26\x68\xed\x3c\x39\xe2\
\xf2\xcb\x4f\x56\xf9\xed\x7c\x65\x4b\xd9\x64\x53\x0e\xd1\x50\xfb\
\x29\x0b\xeb\x4d\xcc\x68\x1c\x21\x04\x52\xeb\x03\x2d\xa0\x73\x21\
\x0c\xa3\x2d\x00\x51\x43\xe3\x34\x3d\xd2\x11\x8b\x53\x93\xe9\xfb\
\x8b\xd7\xfb\xa5\x69\x00\xe7\xcf\x0c\x90\x89\xda\x04\xcb\xeb\xa4\
\x06\xd3\xac\x57\x83\xfb\xdd\xf9\x3e\xc0\x77\x69\x63\x38\xc3\xcd\
\x4a\x0d\x2f\x97\x47\xf9\xc1\xa6\xd3\x0a\xd0\x86\x40\x44\x5c\x0c\
\xd7\xc6\x48\xc4\x10\x96\x85\x29\xe5\x81\xcf\x52\x80\xd4\x7a\x17\
\xf5\xb2\x2d\x03\xa7\xde\x20\xd2\x6c\x71\xf4\xd4\x20\x7d\x99\xc8\
\xc3\x69\xd4\x75\x6d\x5e\xff\xe6\x24\x3f\xf8\xd9\x1d\x8e\x1d\x49\
\xd3\x0c\x99\xf8\x81\x64\xb3\x6e\xbd\xff\x64\xf6\x2c\x84\x88\x46\
\x30\x6b\x2d\xd2\x8e\x4f\x36\x16\xc2\x35\x05\x4a\x29\x8a\x81\x20\
\x67\x5a\x04\xe9\x04\x3a\xe6\xa2\xb7\x3c\xcf\x01\xda\x14\x80\x29\
\xe5\x76\x6c\x17\x40\xd2\x36\xb1\x5b\x1e\x03\x31\x87\xf3\xa7\xfb\
\x1f\xad\xdc\xf9\xfa\x8b\x13\xfc\xec\x83\x59\xd6\x3f\xbd\x47\xe2\
\xec\x51\xd6\xa5\xc2\xb6\x0f\x0e\x18\x9d\x0b\xa1\x9a\x3e\xe2\x5e\
\x8e\x13\x11\xb8\xf4\x8d\xa3\x3c\x7f\x61\x98\x64\xc2\xc5\xf7\x25\
\x9f\x4d\x17\xf8\x8f\xff\x9e\xe3\xe3\xd5\x22\x55\x61\x60\x26\x0e\
\x6e\x16\x6d\xd3\xbd\x8e\x05\x71\x04\x88\x52\x05\xab\xb0\xc1\xd9\
\xa7\x06\x38\xde\x91\x83\x3e\x54\x01\x3b\x15\x0f\xf1\x9d\x57\x4f\
\x92\x9f\xcd\x93\xf6\x5a\x44\x5c\x13\x53\x6c\x47\x83\xae\x62\xdb\
\xe0\x38\x6d\xd1\x6b\x45\x46\x1d\xc9\xdf\x7c\xe7\x14\xaf\x7e\x73\
\x9c\xe4\x66\x33\xc8\xb6\x4d\x9e\x3e\xdd\xc7\x5f\x7f\xf7\x09\xce\
\x64\x22\x98\x1b\x4d\x84\x52\xdb\xfb\xae\x9b\x58\x06\x38\x1d\x12\
\xb2\x04\x09\x2d\xb1\xf3\x15\xc6\x12\x36\xcf\x3d\x35\x74\x60\xff\
\xe5\x81\xc5\x9a\xd7\x2e\x8e\x71\x7c\x38\xc9\xdc\x07\x53\x64\x2d\
\x41\x3c\x64\xe1\x18\x06\xf6\x3e\x62\x1a\x46\x9b\xb4\x6b\x8d\xb1\
\xbe\xc1\x1b\x5f\x1b\x65\x7c\xb4\x07\xa3\x4b\x5d\xa8\x3f\x13\xe3\
\x99\x33\x7d\xf4\x09\x1f\xab\xd9\x20\xe4\x80\xeb\xec\x2c\xd4\x7e\
\x12\x0a\x09\x52\xae\x80\x7c\x99\x70\xb3\xc5\x73\xe7\x47\x98\x1c\
\x4f\x7f\xb1\xde\x4b\x28\x64\xf3\xb7\x7f\x71\x0e\x47\x05\xac\x7f\
\x74\x97\x6c\xd4\x21\x14\x71\x31\x1d\x07\xa3\x8b\x38\x8e\x83\xe3\
\x98\x08\xdf\x27\x61\x9b\x8c\x0f\xa6\x0e\xac\x09\x0d\xf7\xc7\x49\
\x0a\x30\x3c\xd9\xb1\x50\xfb\x8b\x69\x18\x44\x4d\x81\xb1\x56\xc6\
\x58\x2d\xf1\xdc\xd9\xfe\xae\x55\xbf\x87\x06\x0a\x30\x79\x24\xcd\
\x9f\xbf\x79\x96\xea\x52\x81\xc6\xf4\x0a\x29\x02\x62\xb6\xc0\x35\
\xda\xfb\x64\x5b\x68\x8b\x89\x85\x90\x06\xe1\x90\x8d\x61\x1d\x4c\
\x6b\xc2\x61\x0b\xdb\x35\x31\x6c\x0b\xc3\x71\xb0\x1d\x07\x77\x1f\
\x09\xbb\x2e\x09\xd7\xc2\xca\x95\x69\xde\x59\xe6\xe4\x60\x94\x97\
\x9e\x1f\x3b\x54\x7f\xf4\xd0\x27\x97\x5e\xbb\x38\x46\xa1\x50\xe5\
\xc7\x3f\xbf\xcd\x10\x90\x3d\x31\x40\x51\x1b\x34\x83\x8e\xe2\x99\
\xdf\xa6\x42\x36\xa0\x43\x06\xd5\x5a\x8b\x7a\xdd\x47\x29\xbd\x6f\
\x0e\x9a\x2f\x34\x68\x04\x02\x3b\x66\xe1\x1e\xb0\x26\x42\x08\x1c\
\x53\xa0\x96\xcb\x14\x6f\x2c\x31\xd1\x1f\xe3\x8f\xbf\x75\x82\xf1\
\x23\x87\x3b\xa9\xf2\x50\x47\xb4\xfe\xf2\xad\x33\x68\xe0\xc7\x3f\
\x9f\x02\xdf\x27\x7b\x76\x88\x8a\x6d\xd1\x92\xed\x8e\x35\xb6\xe8\
\x08\x4f\x51\x96\x84\xcd\xa7\xb7\x73\x8c\x0c\xc6\xc9\xa4\x22\xf7\
\x71\xd6\x5a\xdd\xe3\xea\xad\x35\x2a\x42\x13\xe9\x71\x71\xba\x20\
\x15\x42\x60\x0a\xb0\xa4\xa6\x75\x2f\x4f\xf9\xe6\x02\x23\x29\x97\
\x37\x2f\x4d\x72\xe6\x58\xe6\xf0\x2d\xc8\x87\x6d\xe3\xfd\xd5\x5b\
\x67\x40\x6b\xde\x7d\x7f\x86\x72\xae\xc6\xc9\x97\x4e\xd1\x8c\x39\
\x34\x1a\x01\x41\xa0\x50\x1d\xd1\x27\x75\x7a\x80\x9f\xfd\x76\x81\
\x74\x32\xcc\xb3\xe7\x06\x89\x47\x1d\x0c\xa3\xdd\xd2\x6f\x79\x92\
\x77\x7e\x79\x87\x5f\x7f\xbe\x8a\x71\x62\x18\x37\x11\xbe\x7f\x5f\
\x09\xb0\x0c\x83\x98\xd6\x94\xa6\x17\x59\xbd\xbe\xc8\x57\x4f\xf6\
\xf1\xa7\x6f\x9c\x3e\xb4\x26\x1f\xf9\x54\xca\xd6\xf8\xf0\xb7\xcb\
\xfc\xcb\x4f\x3e\x67\xb9\xec\xf3\xc4\xd7\x27\xc8\x4c\x64\x29\x69\
\x41\x23\x68\x03\xd9\x02\x5c\xbc\xbe\xc8\xc6\xd4\x12\xe7\x8e\xf6\
\x70\xfe\x74\x86\x58\xc4\xa6\x52\xf6\xb8\x76\x2b\xcf\xf5\xf9\x75\
\xc2\x93\x03\xa4\x8e\x0f\x62\x86\x9c\x0e\x80\x02\x94\x22\x62\x48\
\xe4\x5a\x99\xf9\x6b\x0b\xb4\x0a\x55\x2e\x3d\x37\xc2\x5b\xaf\x1c\
\x27\x9b\x8e\x3e\xf4\x7c\xbf\xd0\xc9\xb1\x62\xb9\xc1\x3f\xfd\xe8\
\x73\xae\x5c\x5d\xc0\x49\x44\x39\xf6\xec\x18\x3d\xe3\xbd\xb4\x2c\
\x41\x3d\x00\xa9\xdb\x64\xbd\x9a\xab\x52\x9a\x59\xa6\xbe\x56\x41\
\x06\x6d\xea\x94\x1a\x48\x92\x1e\xef\xc3\xc9\xc4\x10\xce\x56\x42\
\xa7\x31\x02\x45\xcc\x32\xf0\xd6\x6b\xcc\x7e\x7c\x8f\xfc\xcc\x1a\
\x13\x83\x31\xbe\xfb\xda\x09\x9e\x39\x37\xf4\xc8\x47\xe5\x1e\xcb\
\x59\xc0\xe9\xf9\x22\xff\xf6\xde\x34\x1f\x5d\x5b\x24\x94\x8a\x32\
\x74\x76\x98\x91\x13\xfd\x98\x51\x17\xdf\x10\x78\x41\x80\x46\x6d\
\xb2\x26\xb1\x5d\x3a\xb5\x2d\x8d\x10\x60\x99\x26\xb6\x30\x90\x35\
\x8f\xdc\x74\x8e\xc5\x9b\x2b\x54\xd6\xca\xf4\x26\x5d\x5e\xb9\x38\
\xce\x8b\xcf\x1d\x21\xdb\x13\xfd\x42\x73\x7c\xac\xa7\x3b\xa7\xe7\
\x8b\xbc\x7f\x79\x9e\xcb\xd7\x96\x59\xcb\x55\x49\x66\x93\xf4\x4f\
\xf6\x11\xe9\x8d\x12\x4d\xb8\x58\x96\x41\x2a\x1b\xc5\xb4\x60\xa3\
\xd8\xc4\x6b\x49\x36\x0a\x0d\x4a\x2b\x65\x0a\xcb\x65\x2a\x6b\x15\
\xa2\x8e\xc1\xa9\x63\x59\x5e\xb9\x38\xce\xb9\x53\xd9\x43\xf5\x65\
\x7e\xe7\x40\x3b\xc7\x9d\x7b\x45\x3e\x9d\x2a\x32\x33\x57\x62\x79\
\xa5\xcc\xdd\xa5\x12\x8d\x66\x70\xdf\xf7\x86\x06\x93\x0c\x66\xe3\
\x4c\x8c\xc4\x39\x77\x22\xcb\xb1\xa3\x99\x5d\x0d\xa2\xc7\x35\xc4\
\x1f\xce\xd4\xff\x01\xe8\xff\xcf\xf1\xbf\x67\x1f\x6d\xa3\x03\x34\
\x58\xae\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82\
"

qt_resource_name = b"\
\x00\x05\
\x00\x6f\xa6\x53\
\x00\x69\
\x00\x63\x00\x6f\x00\x6e\x00\x73\
\x00\x07\
\x04\xca\x57\xa7\
\x00\x6e\
\x00\x65\x00\x77\x00\x2e\x00\x70\x00\x6e\x00\x67\
\x00\x08\
\x06\xc1\x59\x87\
\x00\x6f\
\x00\x70\x00\x65\x00\x6e\x00\x2e\x00\x70\x00\x6e\x00\x67\
\x00\x0a\
\x08\x94\x60\x47\
\x00\x73\
\x00\x65\x00\x61\x00\x72\x00\x63\x00\x68\x00\x2e\x00\x70\x00\x6e\x00\x67\
\x00\x08\
\x08\xc8\x58\x67\
\x00\x73\
\x00\x61\x00\x76\x00\x65\x00\x2e\x00\x70\x00\x6e\x00\x67\
\x00\x08\
\x0c\x33\x5a\x87\
\x00\x68\
\x00\x65\x00\x6c\x00\x70\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct_v1 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x02\
\x00\x00\x00\x10\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x00\x24\x00\x00\x00\x00\x00\x01\x00\x00\x05\x2d\
\x00\x00\x00\x3a\x00\x00\x00\x00\x00\x01\x00\x00\x0f\xa2\
\x00\x00\x00\x54\x00\x00\x00\x00\x00\x01\x00\x00\x1a\x2c\
\x00\x00\x00\x6a\x00\x00\x00\x00\x00\x01\x00\x00\x25\xcd\
"

qt_resource_struct_v2 = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x05\x00\x00\x00\x02\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x10\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x9c\x47\xc0\x07\x76\
\x00\x00\x00\x24\x00\x00\x00\x00\x00\x01\x00\x00\x05\x2d\
\x00\x00\x01\x9c\x47\xbf\x79\xa0\
\x00\x00\x00\x3a\x00\x00\x00\x00\x00\x01\x00\x00\x0f\xa2\
\x00\x00\x01\x9c\x42\xfe\xba\x75\
\x00\x00\x00\x54\x00\x00\x00\x00\x00\x01\x00\x00\x1a\x2c\
\x00\x00\x01\x9c\x47\xbf\xb7\xef\
\x00\x00\x00\x6a\x00\x00\x00\x00\x00\x01\x00\x00\x25\xcd\
\x00\x00\x01\x9c\x42\xfd\x10\x31\
"

qt_version = [int(v) for v in qVersion().split('.')]
if qt_version < [5, 8, 0]:
    rcc_version = 1
    qt_resource_struct = qt_resource_struct_v1
else:
    rcc_version = 2
    qt_resource_struct = qt_resource_struct_v2

def qInitResources():
    qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

# ---- Parser/Lexer -----------------------------------------------------------
# Generated from dBaseLexer.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,69,540,6,-1,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,
        7,5,2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,
        2,13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,
        7,19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,
        2,26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,
        7,32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,
        2,39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,
        7,45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,
        2,52,7,52,2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,
        7,58,2,59,7,59,2,60,7,60,2,61,7,61,2,62,7,62,2,63,7,63,2,64,7,64,
        2,65,7,65,2,66,7,66,2,67,7,67,2,68,7,68,2,69,7,69,2,70,7,70,2,71,
        7,71,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,7,1,7,
        1,7,1,7,1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,
        1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,
        1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,14,1,14,1,14,1,14,1,15,
        1,15,1,15,1,15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,16,1,17,
        1,17,1,17,1,17,1,17,1,17,1,18,1,18,1,18,1,18,1,18,1,18,1,18,1,18,
        1,18,1,19,1,19,1,19,1,20,1,20,1,20,1,20,1,20,1,21,1,21,1,21,1,21,
        1,21,1,21,1,21,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,22,
        1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,23,1,24,1,24,1,24,1,24,
        1,24,1,24,1,24,1,25,1,25,1,25,1,25,1,25,1,26,1,26,1,26,1,27,1,27,
        1,27,1,27,1,27,1,28,1,28,1,28,1,28,1,28,1,28,1,29,1,29,1,29,1,29,
        1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,31,1,31,1,32,1,32,1,33,4,33,
        339,8,33,11,33,12,33,340,1,33,1,33,4,33,345,8,33,11,33,12,33,346,
        1,34,4,34,350,8,34,11,34,12,34,351,1,35,1,35,3,35,356,8,35,1,36,
        1,36,1,36,5,36,361,8,36,10,36,12,36,364,9,36,1,36,1,36,1,37,1,37,
        1,37,5,37,371,8,37,10,37,12,37,374,9,37,1,37,1,37,1,38,1,38,1,38,
        1,39,1,39,1,39,1,40,1,40,1,40,1,41,1,41,1,41,1,42,1,42,1,42,1,43,
        1,43,1,44,1,44,1,45,1,45,1,45,1,46,1,46,1,47,1,47,1,48,1,48,1,49,
        1,49,1,50,1,50,1,51,1,51,1,52,1,52,1,53,1,53,1,54,1,54,1,55,1,55,
        1,56,1,56,1,57,1,57,1,57,1,57,5,57,426,8,57,10,57,12,57,429,9,57,
        1,57,1,57,1,58,1,58,1,58,1,58,1,58,1,58,3,58,439,8,58,1,59,1,59,
        1,59,1,59,1,59,1,59,3,59,447,8,59,1,60,1,60,1,60,1,60,1,60,1,60,
        1,61,1,61,1,61,1,61,1,61,1,62,1,62,1,62,1,62,1,62,1,62,1,63,1,63,
        5,63,468,8,63,10,63,12,63,471,9,63,1,64,4,64,474,8,64,11,64,12,64,
        475,1,64,1,64,1,65,1,65,1,65,1,65,5,65,484,8,65,10,65,12,65,487,
        9,65,1,65,1,65,1,66,1,66,1,66,1,66,5,66,495,8,66,10,66,12,66,498,
        9,66,1,66,1,66,1,67,1,67,1,67,1,67,5,67,506,8,67,10,67,12,67,509,
        9,67,1,67,1,67,1,68,1,68,1,68,1,68,1,68,1,68,1,68,1,68,1,69,1,69,
        1,69,1,69,1,69,1,69,1,69,1,69,1,70,1,70,1,70,1,70,1,70,1,70,1,70,
        1,70,1,71,1,71,1,71,1,71,0,0,72,2,1,4,2,6,3,8,4,10,5,12,6,14,7,16,
        8,18,9,20,10,22,11,24,12,26,13,28,14,30,15,32,16,34,17,36,18,38,
        19,40,20,42,21,44,22,46,23,48,24,50,25,52,26,54,27,56,28,58,29,60,
        30,62,31,64,32,66,33,68,34,70,35,72,36,74,0,76,0,78,0,80,37,82,38,
        84,39,86,40,88,41,90,42,92,43,94,44,96,45,98,46,100,47,102,48,104,
        49,106,50,108,51,110,52,112,53,114,54,116,55,118,56,120,57,122,58,
        124,59,126,60,128,61,130,62,132,63,134,64,136,65,138,66,140,67,142,
        68,144,69,2,0,1,29,2,0,80,80,112,112,2,0,65,65,97,97,2,0,82,82,114,
        114,2,0,77,77,109,109,2,0,69,69,101,101,2,0,84,84,116,116,2,0,87,
        87,119,119,2,0,73,73,105,105,2,0,72,72,104,104,2,0,78,78,110,110,
        2,0,68,68,100,100,2,0,79,79,111,111,2,0,71,71,103,103,2,0,85,85,
        117,117,2,0,70,70,102,102,2,0,83,83,115,115,2,0,66,66,98,98,2,0,
        75,75,107,107,2,0,76,76,108,108,2,0,67,67,99,99,2,0,89,89,121,121,
        1,0,48,57,4,0,10,10,13,13,34,34,92,92,4,0,10,10,13,13,39,39,92,92,
        1,0,93,93,3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,97,122,3,
        0,9,10,13,13,32,32,2,0,10,10,13,13,552,0,2,1,0,0,0,0,4,1,0,0,0,0,
        6,1,0,0,0,0,8,1,0,0,0,0,10,1,0,0,0,0,12,1,0,0,0,0,14,1,0,0,0,0,16,
        1,0,0,0,0,18,1,0,0,0,0,20,1,0,0,0,0,22,1,0,0,0,0,24,1,0,0,0,0,26,
        1,0,0,0,0,28,1,0,0,0,0,30,1,0,0,0,0,32,1,0,0,0,0,34,1,0,0,0,0,36,
        1,0,0,0,0,38,1,0,0,0,0,40,1,0,0,0,0,42,1,0,0,0,0,44,1,0,0,0,0,46,
        1,0,0,0,0,48,1,0,0,0,0,50,1,0,0,0,0,52,1,0,0,0,0,54,1,0,0,0,0,56,
        1,0,0,0,0,58,1,0,0,0,0,60,1,0,0,0,0,62,1,0,0,0,0,64,1,0,0,0,0,66,
        1,0,0,0,0,68,1,0,0,0,0,70,1,0,0,0,0,72,1,0,0,0,0,80,1,0,0,0,0,82,
        1,0,0,0,0,84,1,0,0,0,0,86,1,0,0,0,0,88,1,0,0,0,0,90,1,0,0,0,0,92,
        1,0,0,0,0,94,1,0,0,0,0,96,1,0,0,0,0,98,1,0,0,0,0,100,1,0,0,0,0,102,
        1,0,0,0,0,104,1,0,0,0,0,106,1,0,0,0,0,108,1,0,0,0,0,110,1,0,0,0,
        0,112,1,0,0,0,0,114,1,0,0,0,0,116,1,0,0,0,0,118,1,0,0,0,0,120,1,
        0,0,0,0,122,1,0,0,0,0,124,1,0,0,0,0,126,1,0,0,0,0,128,1,0,0,0,0,
        130,1,0,0,0,0,132,1,0,0,0,0,134,1,0,0,0,0,136,1,0,0,0,0,138,1,0,
        0,0,1,140,1,0,0,0,1,142,1,0,0,0,1,144,1,0,0,0,2,146,1,0,0,0,4,156,
        1,0,0,0,6,161,1,0,0,0,8,169,1,0,0,0,10,177,1,0,0,0,12,184,1,0,0,
        0,14,188,1,0,0,0,16,191,1,0,0,0,18,198,1,0,0,0,20,203,1,0,0,0,22,
        209,1,0,0,0,24,212,1,0,0,0,26,218,1,0,0,0,28,224,1,0,0,0,30,230,
        1,0,0,0,32,234,1,0,0,0,34,241,1,0,0,0,36,247,1,0,0,0,38,253,1,0,
        0,0,40,262,1,0,0,0,42,265,1,0,0,0,44,270,1,0,0,0,46,277,1,0,0,0,
        48,287,1,0,0,0,50,296,1,0,0,0,52,303,1,0,0,0,54,308,1,0,0,0,56,311,
        1,0,0,0,58,316,1,0,0,0,60,322,1,0,0,0,62,328,1,0,0,0,64,333,1,0,
        0,0,66,335,1,0,0,0,68,338,1,0,0,0,70,349,1,0,0,0,72,355,1,0,0,0,
        74,357,1,0,0,0,76,367,1,0,0,0,78,377,1,0,0,0,80,380,1,0,0,0,82,383,
        1,0,0,0,84,386,1,0,0,0,86,389,1,0,0,0,88,392,1,0,0,0,90,394,1,0,
        0,0,92,396,1,0,0,0,94,399,1,0,0,0,96,401,1,0,0,0,98,403,1,0,0,0,
        100,405,1,0,0,0,102,407,1,0,0,0,104,409,1,0,0,0,106,411,1,0,0,0,
        108,413,1,0,0,0,110,415,1,0,0,0,112,417,1,0,0,0,114,419,1,0,0,0,
        116,421,1,0,0,0,118,438,1,0,0,0,120,446,1,0,0,0,122,448,1,0,0,0,
        124,454,1,0,0,0,126,459,1,0,0,0,128,465,1,0,0,0,130,473,1,0,0,0,
        132,479,1,0,0,0,134,490,1,0,0,0,136,501,1,0,0,0,138,512,1,0,0,0,
        140,520,1,0,0,0,142,528,1,0,0,0,144,536,1,0,0,0,146,147,7,0,0,0,
        147,148,7,1,0,0,148,149,7,2,0,0,149,150,7,1,0,0,150,151,7,3,0,0,
        151,152,7,4,0,0,152,153,7,5,0,0,153,154,7,4,0,0,154,155,7,2,0,0,
        155,3,1,0,0,0,156,157,7,6,0,0,157,158,7,7,0,0,158,159,7,5,0,0,159,
        160,7,8,0,0,160,5,1,0,0,0,161,162,7,4,0,0,162,163,7,9,0,0,163,164,
        7,10,0,0,164,165,7,6,0,0,165,166,7,7,0,0,166,167,7,5,0,0,167,168,
        7,8,0,0,168,7,1,0,0,0,169,170,7,0,0,0,170,171,7,2,0,0,171,172,7,
        11,0,0,172,173,7,12,0,0,173,174,7,2,0,0,174,175,7,1,0,0,175,176,
        7,3,0,0,176,9,1,0,0,0,177,178,7,2,0,0,178,179,7,4,0,0,179,180,7,
        5,0,0,180,181,7,13,0,0,181,182,7,2,0,0,182,183,7,9,0,0,183,11,1,
        0,0,0,184,185,7,14,0,0,185,186,7,11,0,0,186,187,7,2,0,0,187,13,1,
        0,0,0,188,189,7,5,0,0,189,190,7,11,0,0,190,15,1,0,0,0,191,192,7,
        4,0,0,192,193,7,9,0,0,193,194,7,10,0,0,194,195,7,14,0,0,195,196,
        7,11,0,0,196,197,7,2,0,0,197,17,1,0,0,0,198,199,7,15,0,0,199,200,
        7,5,0,0,200,201,7,4,0,0,201,202,7,0,0,0,202,19,1,0,0,0,203,204,7,
        16,0,0,204,205,7,2,0,0,205,206,7,4,0,0,206,207,7,1,0,0,207,208,7,
        17,0,0,208,21,1,0,0,0,209,210,7,10,0,0,210,211,7,11,0,0,211,23,1,
        0,0,0,212,213,7,6,0,0,213,214,7,8,0,0,214,215,7,7,0,0,215,216,7,
        18,0,0,216,217,7,4,0,0,217,25,1,0,0,0,218,219,7,4,0,0,219,220,7,
        9,0,0,220,221,7,10,0,0,221,222,7,10,0,0,222,223,7,11,0,0,223,27,
        1,0,0,0,224,225,7,18,0,0,225,226,7,11,0,0,226,227,7,19,0,0,227,228,
        7,1,0,0,228,229,7,18,0,0,229,29,1,0,0,0,230,231,7,9,0,0,231,232,
        7,4,0,0,232,233,7,6,0,0,233,31,1,0,0,0,234,235,7,10,0,0,235,236,
        7,4,0,0,236,237,7,18,0,0,237,238,7,4,0,0,238,239,7,5,0,0,239,240,
        7,4,0,0,240,33,1,0,0,0,241,242,7,15,0,0,242,243,7,13,0,0,243,244,
        7,0,0,0,244,245,7,4,0,0,245,246,7,2,0,0,246,35,1,0,0,0,247,248,7,
        19,0,0,248,249,7,18,0,0,249,250,7,1,0,0,250,251,7,15,0,0,251,252,
        7,15,0,0,252,37,1,0,0,0,253,254,7,4,0,0,254,255,7,9,0,0,255,256,
        7,10,0,0,256,257,7,19,0,0,257,258,7,18,0,0,258,259,7,1,0,0,259,260,
        7,15,0,0,260,261,7,15,0,0,261,39,1,0,0,0,262,263,7,11,0,0,263,264,
        7,14,0,0,264,41,1,0,0,0,265,266,7,5,0,0,266,267,7,8,0,0,267,268,
        7,7,0,0,268,269,7,15,0,0,269,43,1,0,0,0,270,271,7,3,0,0,271,272,
        7,4,0,0,272,273,7,5,0,0,273,274,7,8,0,0,274,275,7,11,0,0,275,276,
        7,10,0,0,276,45,1,0,0,0,277,278,7,4,0,0,278,279,7,9,0,0,279,280,
        7,10,0,0,280,281,7,3,0,0,281,282,7,4,0,0,282,283,7,5,0,0,283,284,
        7,8,0,0,284,285,7,11,0,0,285,286,7,10,0,0,286,47,1,0,0,0,287,288,
        7,0,0,0,288,289,7,2,0,0,289,290,7,11,0,0,290,291,7,0,0,0,291,292,
        7,4,0,0,292,293,7,2,0,0,293,294,7,5,0,0,294,295,7,20,0,0,295,49,
        1,0,0,0,296,297,7,19,0,0,297,298,7,2,0,0,298,299,7,4,0,0,299,300,
        7,1,0,0,300,301,7,5,0,0,301,302,7,4,0,0,302,51,1,0,0,0,303,304,7,
        14,0,0,304,305,7,7,0,0,305,306,7,18,0,0,306,307,7,4,0,0,307,53,1,
        0,0,0,308,309,7,7,0,0,309,310,7,14,0,0,310,55,1,0,0,0,311,312,7,
        4,0,0,312,313,7,18,0,0,313,314,7,15,0,0,314,315,7,4,0,0,315,57,1,
        0,0,0,316,317,7,4,0,0,317,318,7,9,0,0,318,319,7,10,0,0,319,320,7,
        7,0,0,320,321,7,14,0,0,321,59,1,0,0,0,322,323,7,6,0,0,323,324,7,
        2,0,0,324,325,7,7,0,0,325,326,7,5,0,0,326,327,7,4,0,0,327,61,1,0,
        0,0,328,329,7,19,0,0,329,330,7,1,0,0,330,331,7,18,0,0,331,332,7,
        18,0,0,332,63,1,0,0,0,333,334,5,44,0,0,334,65,1,0,0,0,335,336,5,
        46,0,0,336,67,1,0,0,0,337,339,7,21,0,0,338,337,1,0,0,0,339,340,1,
        0,0,0,340,338,1,0,0,0,340,341,1,0,0,0,341,342,1,0,0,0,342,344,5,
        46,0,0,343,345,7,21,0,0,344,343,1,0,0,0,345,346,1,0,0,0,346,344,
        1,0,0,0,346,347,1,0,0,0,347,69,1,0,0,0,348,350,7,21,0,0,349,348,
        1,0,0,0,350,351,1,0,0,0,351,349,1,0,0,0,351,352,1,0,0,0,352,71,1,
        0,0,0,353,356,3,74,36,0,354,356,3,76,37,0,355,353,1,0,0,0,355,354,
        1,0,0,0,356,73,1,0,0,0,357,362,5,34,0,0,358,361,3,78,38,0,359,361,
        8,22,0,0,360,358,1,0,0,0,360,359,1,0,0,0,361,364,1,0,0,0,362,360,
        1,0,0,0,362,363,1,0,0,0,363,365,1,0,0,0,364,362,1,0,0,0,365,366,
        5,34,0,0,366,75,1,0,0,0,367,372,5,39,0,0,368,371,3,78,38,0,369,371,
        8,23,0,0,370,368,1,0,0,0,370,369,1,0,0,0,371,374,1,0,0,0,372,370,
        1,0,0,0,372,373,1,0,0,0,373,375,1,0,0,0,374,372,1,0,0,0,375,376,
        5,39,0,0,376,77,1,0,0,0,377,378,5,92,0,0,378,379,9,0,0,0,379,79,
        1,0,0,0,380,381,5,60,0,0,381,382,5,61,0,0,382,81,1,0,0,0,383,384,
        5,62,0,0,384,385,5,61,0,0,385,83,1,0,0,0,386,387,5,33,0,0,387,388,
        5,61,0,0,388,85,1,0,0,0,389,390,5,61,0,0,390,391,5,61,0,0,391,87,
        1,0,0,0,392,393,5,60,0,0,393,89,1,0,0,0,394,395,5,62,0,0,395,91,
        1,0,0,0,396,397,5,58,0,0,397,398,5,58,0,0,398,93,1,0,0,0,399,400,
        5,58,0,0,400,95,1,0,0,0,401,402,5,61,0,0,402,97,1,0,0,0,403,404,
        5,40,0,0,404,99,1,0,0,0,405,406,5,41,0,0,406,101,1,0,0,0,407,408,
        5,43,0,0,408,103,1,0,0,0,409,410,5,45,0,0,410,105,1,0,0,0,411,412,
        5,42,0,0,412,107,1,0,0,0,413,414,5,47,0,0,414,109,1,0,0,0,415,416,
        5,123,0,0,416,111,1,0,0,0,417,418,5,125,0,0,418,113,1,0,0,0,419,
        420,5,59,0,0,420,115,1,0,0,0,421,427,5,91,0,0,422,423,5,93,0,0,423,
        426,5,93,0,0,424,426,8,24,0,0,425,422,1,0,0,0,425,424,1,0,0,0,426,
        429,1,0,0,0,427,425,1,0,0,0,427,428,1,0,0,0,428,430,1,0,0,0,429,
        427,1,0,0,0,430,431,5,93,0,0,431,117,1,0,0,0,432,433,5,46,0,0,433,
        434,5,84,0,0,434,439,5,46,0,0,435,436,5,46,0,0,436,437,5,116,0,0,
        437,439,5,46,0,0,438,432,1,0,0,0,438,435,1,0,0,0,439,119,1,0,0,0,
        440,441,5,46,0,0,441,442,5,70,0,0,442,447,5,46,0,0,443,444,5,46,
        0,0,444,445,5,102,0,0,445,447,5,46,0,0,446,440,1,0,0,0,446,443,1,
        0,0,0,447,121,1,0,0,0,448,449,5,46,0,0,449,450,7,1,0,0,450,451,7,
        9,0,0,451,452,7,10,0,0,452,453,5,46,0,0,453,123,1,0,0,0,454,455,
        5,46,0,0,455,456,7,11,0,0,456,457,7,2,0,0,457,458,5,46,0,0,458,125,
        1,0,0,0,459,460,5,46,0,0,460,461,7,9,0,0,461,462,7,11,0,0,462,463,
        7,5,0,0,463,464,5,46,0,0,464,127,1,0,0,0,465,469,7,25,0,0,466,468,
        7,26,0,0,467,466,1,0,0,0,468,471,1,0,0,0,469,467,1,0,0,0,469,470,
        1,0,0,0,470,129,1,0,0,0,471,469,1,0,0,0,472,474,7,27,0,0,473,472,
        1,0,0,0,474,475,1,0,0,0,475,473,1,0,0,0,475,476,1,0,0,0,476,477,
        1,0,0,0,477,478,6,64,0,0,478,131,1,0,0,0,479,480,5,42,0,0,480,481,
        5,42,0,0,481,485,1,0,0,0,482,484,8,28,0,0,483,482,1,0,0,0,484,487,
        1,0,0,0,485,483,1,0,0,0,485,486,1,0,0,0,486,488,1,0,0,0,487,485,
        1,0,0,0,488,489,6,65,0,0,489,133,1,0,0,0,490,491,5,38,0,0,491,492,
        5,38,0,0,492,496,1,0,0,0,493,495,8,28,0,0,494,493,1,0,0,0,495,498,
        1,0,0,0,496,494,1,0,0,0,496,497,1,0,0,0,497,499,1,0,0,0,498,496,
        1,0,0,0,499,500,6,66,0,0,500,135,1,0,0,0,501,502,5,47,0,0,502,503,
        5,47,0,0,503,507,1,0,0,0,504,506,8,28,0,0,505,504,1,0,0,0,506,509,
        1,0,0,0,507,505,1,0,0,0,507,508,1,0,0,0,508,510,1,0,0,0,509,507,
        1,0,0,0,510,511,6,67,0,0,511,137,1,0,0,0,512,513,5,47,0,0,513,514,
        5,42,0,0,514,515,1,0,0,0,515,516,6,68,1,0,516,517,1,0,0,0,517,518,
        6,68,2,0,518,519,6,68,0,0,519,139,1,0,0,0,520,521,5,47,0,0,521,522,
        5,42,0,0,522,523,1,0,0,0,523,524,6,69,3,0,524,525,1,0,0,0,525,526,
        6,69,2,0,526,527,6,69,0,0,527,141,1,0,0,0,528,529,5,42,0,0,529,530,
        5,47,0,0,530,531,1,0,0,0,531,532,6,70,4,0,532,533,1,0,0,0,533,534,
        6,70,5,0,534,535,6,70,0,0,535,143,1,0,0,0,536,537,9,0,0,0,537,538,
        1,0,0,0,538,539,6,71,0,0,539,145,1,0,0,0,19,0,1,340,346,351,355,
        360,362,370,372,425,427,438,446,469,475,485,496,507,6,6,0,0,1,68,
        0,5,1,0,1,69,1,1,70,2,4,0,0
    ]

class dBaseLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    COMMENT = 1

    PARAMETER = 1
    WITH = 2
    ENDWITH = 3
    PROGRAM = 4
    RETURN = 5
    FOR = 6
    TO = 7
    ENDFOR = 8
    STEP = 9
    BREAK = 10
    DO = 11
    WHILE = 12
    ENDDO = 13
    LOCAL = 14
    NEW = 15
    DELETE = 16
    SUPER = 17
    CLASS = 18
    ENDCLASS = 19
    OF = 20
    THIS = 21
    METHOD = 22
    ENDMETHOD = 23
    PROPERTY = 24
    CREATE = 25
    FILE = 26
    IF = 27
    ELSE = 28
    ENDIF = 29
    WRITE = 30
    CALL = 31
    COMMA = 32
    DOT = 33
    FLOAT = 34
    NUMBER = 35
    STRING = 36
    LE = 37
    GE = 38
    NE = 39
    EQ = 40
    LT = 41
    GT = 42
    DCOLON = 43
    COLON = 44
    ASSIGN = 45
    LPAREN = 46
    RPAREN = 47
    PLUS = 48
    MINUS = 49
    STAR = 50
    SLASH = 51
    LBRACE = 52
    RBRACE = 53
    SEMI = 54
    BRACKET_STRING = 55
    TRUE = 56
    FALSE = 57
    AND = 58
    OR = 59
    NOT = 60
    IDENT = 61
    WS = 62
    LINECOMMENT_DBA = 63
    LINECOMMENT_DBB = 64
    LINECOMMENT_CPP = 65
    BLOCKCOMMENT_START = 66
    COMMENT_NEST_START = 67
    COMMENT_END = 68
    COMMENT_ANY = 69

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE", "COMMENT" ]

    literalNames = [ "<INVALID>",
            "','", "'.'", "'<='", "'>='", "'!='", "'=='", "'<'", "'>'", 
            "'::'", "':'", "'='", "'('", "')'", "'+'", "'-'", "'*'", "'/'", 
            "'{'", "'}'", "';'" ]

    symbolicNames = [ "<INVALID>",
            "PARAMETER", "WITH", "ENDWITH", "PROGRAM", "RETURN", "FOR", 
            "TO", "ENDFOR", "STEP", "BREAK", "DO", "WHILE", "ENDDO", "LOCAL", 
            "NEW", "DELETE", "SUPER", "CLASS", "ENDCLASS", "OF", "THIS", 
            "METHOD", "ENDMETHOD", "PROPERTY", "CREATE", "FILE", "IF", "ELSE", 
            "ENDIF", "WRITE", "CALL", "COMMA", "DOT", "FLOAT", "NUMBER", 
            "STRING", "LE", "GE", "NE", "EQ", "LT", "GT", "DCOLON", "COLON", 
            "ASSIGN", "LPAREN", "RPAREN", "PLUS", "MINUS", "STAR", "SLASH", 
            "LBRACE", "RBRACE", "SEMI", "BRACKET_STRING", "TRUE", "FALSE", 
            "AND", "OR", "NOT", "IDENT", "WS", "LINECOMMENT_DBA", "LINECOMMENT_DBB", 
            "LINECOMMENT_CPP", "BLOCKCOMMENT_START", "COMMENT_NEST_START", 
            "COMMENT_END", "COMMENT_ANY" ]

    ruleNames = [ "PARAMETER", "WITH", "ENDWITH", "PROGRAM", "RETURN", "FOR", 
                  "TO", "ENDFOR", "STEP", "BREAK", "DO", "WHILE", "ENDDO", 
                  "LOCAL", "NEW", "DELETE", "SUPER", "CLASS", "ENDCLASS", 
                  "OF", "THIS", "METHOD", "ENDMETHOD", "PROPERTY", "CREATE", 
                  "FILE", "IF", "ELSE", "ENDIF", "WRITE", "CALL", "COMMA", 
                  "DOT", "FLOAT", "NUMBER", "STRING", "DQ_STRING", "SQ_STRING", 
                  "ESC", "LE", "GE", "NE", "EQ", "LT", "GT", "DCOLON", "COLON", 
                  "ASSIGN", "LPAREN", "RPAREN", "PLUS", "MINUS", "STAR", 
                  "SLASH", "LBRACE", "RBRACE", "SEMI", "BRACKET_STRING", 
                  "TRUE", "FALSE", "AND", "OR", "NOT", "IDENT", "WS", "LINECOMMENT_DBA", 
                  "LINECOMMENT_DBB", "LINECOMMENT_CPP", "BLOCKCOMMENT_START", 
                  "COMMENT_NEST_START", "COMMENT_END", "COMMENT_ANY" ]

    grammarFileName = "dBaseLexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[68] = self.BLOCKCOMMENT_START_action 
            actions[69] = self.COMMENT_NEST_START_action 
            actions[70] = self.COMMENT_END_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def BLOCKCOMMENT_START_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:
             self._cmtDepth = getattr(self, "_cmtDepth", 0) + 1 
     

    def COMMENT_NEST_START_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
             self._cmtDepth += 1 
     

    def COMMENT_END_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
             self._cmtDepth -= 1 
     



def serializedATN():
    return [
        4,1,69,517,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,45,2,46,
        7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,52,7,52,
        2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,1,0,5,0,118,8,
        0,10,0,12,0,121,9,0,1,0,1,0,1,1,1,1,1,1,3,1,128,8,1,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,147,
        8,2,1,3,1,3,1,3,3,3,152,8,3,1,4,1,4,1,4,1,4,5,4,158,8,4,10,4,12,
        4,161,9,4,1,4,1,4,1,5,1,5,1,6,1,6,3,6,169,8,6,1,7,1,7,1,7,1,7,3,
        7,175,8,7,1,8,1,8,3,8,179,8,8,1,9,1,9,1,9,3,9,184,8,9,1,9,1,9,3,
        9,188,8,9,1,10,1,10,1,10,1,11,1,11,1,11,5,11,196,8,11,10,11,12,11,
        199,9,11,1,12,1,12,1,12,5,12,204,8,12,10,12,12,12,207,9,12,1,12,
        1,12,3,12,211,8,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,14,
        1,14,1,15,1,15,1,15,5,15,226,8,15,10,15,12,15,229,9,15,1,16,1,16,
        1,16,5,16,234,8,16,10,16,12,16,237,9,16,1,17,1,17,1,17,3,17,242,
        8,17,1,18,1,18,1,18,1,18,3,18,248,8,18,1,19,1,19,1,20,1,20,1,20,
        1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,22,1,23,1,23,1,23,1,23,1,23,
        1,23,1,23,1,23,3,23,271,8,23,1,23,1,23,1,23,1,24,1,24,1,25,1,25,
        1,25,1,25,1,26,1,26,3,26,284,8,26,1,27,1,27,1,27,4,27,289,8,27,11,
        27,12,27,290,1,27,1,27,1,27,5,27,296,8,27,10,27,12,27,299,9,27,3,
        27,301,8,27,1,28,1,28,1,29,1,29,1,29,1,29,1,29,3,29,310,8,29,1,29,
        1,29,1,30,5,30,315,8,30,10,30,12,30,318,9,30,1,31,1,31,1,31,1,31,
        5,31,324,8,31,10,31,12,31,327,9,31,1,32,1,32,1,32,3,32,332,8,32,
        1,33,1,33,1,33,1,33,3,33,338,8,33,1,33,1,33,1,33,1,34,1,34,5,34,
        345,8,34,10,34,12,34,348,9,34,1,35,1,35,1,35,1,35,3,35,354,8,35,
        1,36,1,36,1,36,1,36,1,36,1,36,1,36,1,37,1,37,1,37,1,37,3,37,367,
        8,37,1,38,1,38,1,38,5,38,372,8,38,10,38,12,38,375,9,38,1,39,1,39,
        1,39,1,39,1,40,1,40,1,40,5,40,384,8,40,10,40,12,40,387,9,40,1,41,
        1,41,1,41,1,41,3,41,393,8,41,1,42,1,42,1,42,1,42,3,42,399,8,42,1,
        42,1,42,1,42,1,42,1,43,1,43,1,43,5,43,408,8,43,10,43,12,43,411,9,
        43,1,44,1,44,1,44,1,45,1,45,3,45,418,8,45,1,45,1,45,1,45,3,45,423,
        8,45,1,45,1,45,1,46,1,46,1,46,3,46,430,8,46,1,47,1,47,1,47,5,47,
        435,8,47,10,47,12,47,438,9,47,1,48,1,48,1,49,1,49,1,50,1,50,1,50,
        5,50,447,8,50,10,50,12,50,450,9,50,1,51,1,51,1,51,5,51,455,8,51,
        10,51,12,51,458,9,51,1,52,1,52,1,52,3,52,463,8,52,1,52,1,52,1,52,
        5,52,468,8,52,10,52,12,52,471,9,52,1,53,1,53,1,53,1,53,3,53,477,
        8,53,1,53,3,53,480,8,53,1,54,1,54,1,54,1,54,3,54,486,8,54,1,54,1,
        54,1,55,1,55,1,55,5,55,493,8,55,10,55,12,55,496,9,55,1,56,1,56,1,
        57,1,57,1,57,1,57,1,57,1,57,1,57,1,57,1,57,1,57,1,57,1,57,1,57,1,
        57,1,57,3,57,515,8,57,1,57,0,0,58,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,
        68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100,102,104,106,
        108,110,112,114,0,6,1,0,37,42,1,0,48,49,1,0,50,51,2,0,33,33,43,43,
        2,0,21,21,61,61,2,0,35,36,56,57,541,0,119,1,0,0,0,2,127,1,0,0,0,
        4,146,1,0,0,0,6,148,1,0,0,0,8,153,1,0,0,0,10,164,1,0,0,0,12,166,
        1,0,0,0,14,170,1,0,0,0,16,178,1,0,0,0,18,187,1,0,0,0,20,189,1,0,
        0,0,22,192,1,0,0,0,24,200,1,0,0,0,26,214,1,0,0,0,28,220,1,0,0,0,
        30,222,1,0,0,0,32,230,1,0,0,0,34,241,1,0,0,0,36,243,1,0,0,0,38,249,
        1,0,0,0,40,251,1,0,0,0,42,254,1,0,0,0,44,259,1,0,0,0,46,262,1,0,
        0,0,48,275,1,0,0,0,50,277,1,0,0,0,52,283,1,0,0,0,54,300,1,0,0,0,
        56,302,1,0,0,0,58,304,1,0,0,0,60,316,1,0,0,0,62,319,1,0,0,0,64,331,
        1,0,0,0,66,333,1,0,0,0,68,346,1,0,0,0,70,353,1,0,0,0,72,355,1,0,
        0,0,74,366,1,0,0,0,76,373,1,0,0,0,78,376,1,0,0,0,80,380,1,0,0,0,
        82,388,1,0,0,0,84,394,1,0,0,0,86,404,1,0,0,0,88,412,1,0,0,0,90,417,
        1,0,0,0,92,426,1,0,0,0,94,431,1,0,0,0,96,439,1,0,0,0,98,441,1,0,
        0,0,100,443,1,0,0,0,102,451,1,0,0,0,104,459,1,0,0,0,106,479,1,0,
        0,0,108,481,1,0,0,0,110,489,1,0,0,0,112,497,1,0,0,0,114,514,1,0,
        0,0,116,118,3,2,1,0,117,116,1,0,0,0,118,121,1,0,0,0,119,117,1,0,
        0,0,119,120,1,0,0,0,120,122,1,0,0,0,121,119,1,0,0,0,122,123,5,0,
        0,1,123,1,1,0,0,0,124,128,3,66,33,0,125,128,3,84,42,0,126,128,3,
        4,2,0,127,124,1,0,0,0,127,125,1,0,0,0,127,126,1,0,0,0,128,3,1,0,
        0,0,129,147,3,58,29,0,130,147,3,14,7,0,131,147,3,10,5,0,132,147,
        3,20,10,0,133,147,3,62,31,0,134,147,3,50,25,0,135,147,3,6,3,0,136,
        147,3,56,28,0,137,147,3,42,21,0,138,147,3,40,20,0,139,147,3,88,44,
        0,140,147,3,66,33,0,141,147,3,46,23,0,142,147,3,26,13,0,143,147,
        3,44,22,0,144,147,3,12,6,0,145,147,3,72,36,0,146,129,1,0,0,0,146,
        130,1,0,0,0,146,131,1,0,0,0,146,132,1,0,0,0,146,133,1,0,0,0,146,
        134,1,0,0,0,146,135,1,0,0,0,146,136,1,0,0,0,146,137,1,0,0,0,146,
        138,1,0,0,0,146,139,1,0,0,0,146,140,1,0,0,0,146,141,1,0,0,0,146,
        142,1,0,0,0,146,143,1,0,0,0,146,144,1,0,0,0,146,145,1,0,0,0,147,
        5,1,0,0,0,148,149,5,25,0,0,149,151,5,26,0,0,150,152,3,98,49,0,151,
        150,1,0,0,0,151,152,1,0,0,0,152,7,1,0,0,0,153,154,5,52,0,0,154,159,
        3,98,49,0,155,156,5,54,0,0,156,158,3,98,49,0,157,155,1,0,0,0,158,
        161,1,0,0,0,159,157,1,0,0,0,159,160,1,0,0,0,160,162,1,0,0,0,161,
        159,1,0,0,0,162,163,5,53,0,0,163,9,1,0,0,0,164,165,5,10,0,0,165,
        11,1,0,0,0,166,168,5,5,0,0,167,169,3,98,49,0,168,167,1,0,0,0,168,
        169,1,0,0,0,169,13,1,0,0,0,170,171,5,11,0,0,171,174,3,16,8,0,172,
        173,5,2,0,0,173,175,3,94,47,0,174,172,1,0,0,0,174,175,1,0,0,0,175,
        15,1,0,0,0,176,179,3,18,9,0,177,179,5,61,0,0,178,176,1,0,0,0,178,
        177,1,0,0,0,179,17,1,0,0,0,180,183,5,61,0,0,181,182,5,33,0,0,182,
        184,5,61,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,188,1,0,0,0,185,
        186,5,4,0,0,186,188,5,61,0,0,187,180,1,0,0,0,187,185,1,0,0,0,188,
        19,1,0,0,0,189,190,5,1,0,0,190,191,3,22,11,0,191,21,1,0,0,0,192,
        197,5,61,0,0,193,194,5,32,0,0,194,196,5,61,0,0,195,193,1,0,0,0,196,
        199,1,0,0,0,197,195,1,0,0,0,197,198,1,0,0,0,198,23,1,0,0,0,199,197,
        1,0,0,0,200,205,3,114,57,0,201,202,5,33,0,0,202,204,5,61,0,0,203,
        201,1,0,0,0,204,207,1,0,0,0,205,203,1,0,0,0,205,206,1,0,0,0,206,
        208,1,0,0,0,207,205,1,0,0,0,208,210,5,46,0,0,209,211,3,94,47,0,210,
        209,1,0,0,0,210,211,1,0,0,0,211,212,1,0,0,0,212,213,5,47,0,0,213,
        25,1,0,0,0,214,215,5,11,0,0,215,216,5,12,0,0,216,217,3,28,14,0,217,
        218,3,60,30,0,218,219,5,13,0,0,219,27,1,0,0,0,220,221,3,30,15,0,
        221,29,1,0,0,0,222,227,3,32,16,0,223,224,5,59,0,0,224,226,3,32,16,
        0,225,223,1,0,0,0,226,229,1,0,0,0,227,225,1,0,0,0,227,228,1,0,0,
        0,228,31,1,0,0,0,229,227,1,0,0,0,230,235,3,34,17,0,231,232,5,58,
        0,0,232,234,3,34,17,0,233,231,1,0,0,0,234,237,1,0,0,0,235,233,1,
        0,0,0,235,236,1,0,0,0,236,33,1,0,0,0,237,235,1,0,0,0,238,239,5,60,
        0,0,239,242,3,34,17,0,240,242,3,36,18,0,241,238,1,0,0,0,241,240,
        1,0,0,0,242,35,1,0,0,0,243,247,3,100,50,0,244,245,3,38,19,0,245,
        246,3,100,50,0,246,248,1,0,0,0,247,244,1,0,0,0,247,248,1,0,0,0,248,
        37,1,0,0,0,249,250,7,0,0,0,250,39,1,0,0,0,251,252,5,14,0,0,252,253,
        5,61,0,0,253,41,1,0,0,0,254,255,5,14,0,0,255,256,5,61,0,0,256,257,
        5,45,0,0,257,258,3,98,49,0,258,43,1,0,0,0,259,260,5,16,0,0,260,261,
        5,61,0,0,261,45,1,0,0,0,262,263,5,6,0,0,263,264,5,61,0,0,264,265,
        5,45,0,0,265,266,3,48,24,0,266,267,5,7,0,0,267,270,3,48,24,0,268,
        269,5,9,0,0,269,271,3,48,24,0,270,268,1,0,0,0,270,271,1,0,0,0,271,
        272,1,0,0,0,272,273,3,60,30,0,273,274,5,8,0,0,274,47,1,0,0,0,275,
        276,5,35,0,0,276,49,1,0,0,0,277,278,3,52,26,0,278,279,5,45,0,0,279,
        280,3,98,49,0,280,51,1,0,0,0,281,284,3,104,52,0,282,284,3,54,27,
        0,283,281,1,0,0,0,283,282,1,0,0,0,284,53,1,0,0,0,285,288,5,21,0,
        0,286,287,5,33,0,0,287,289,5,61,0,0,288,286,1,0,0,0,289,290,1,0,
        0,0,290,288,1,0,0,0,290,291,1,0,0,0,291,301,1,0,0,0,292,297,5,61,
        0,0,293,294,5,33,0,0,294,296,5,61,0,0,295,293,1,0,0,0,296,299,1,
        0,0,0,297,295,1,0,0,0,297,298,1,0,0,0,298,301,1,0,0,0,299,297,1,
        0,0,0,300,285,1,0,0,0,300,292,1,0,0,0,301,55,1,0,0,0,302,303,3,104,
        52,0,303,57,1,0,0,0,304,305,5,27,0,0,305,306,3,98,49,0,306,309,3,
        60,30,0,307,308,5,28,0,0,308,310,3,60,30,0,309,307,1,0,0,0,309,310,
        1,0,0,0,310,311,1,0,0,0,311,312,5,29,0,0,312,59,1,0,0,0,313,315,
        3,4,2,0,314,313,1,0,0,0,315,318,1,0,0,0,316,314,1,0,0,0,316,317,
        1,0,0,0,317,61,1,0,0,0,318,316,1,0,0,0,319,320,5,30,0,0,320,325,
        3,64,32,0,321,322,5,48,0,0,322,324,3,64,32,0,323,321,1,0,0,0,324,
        327,1,0,0,0,325,323,1,0,0,0,325,326,1,0,0,0,326,63,1,0,0,0,327,325,
        1,0,0,0,328,332,5,36,0,0,329,332,3,54,27,0,330,332,3,98,49,0,331,
        328,1,0,0,0,331,329,1,0,0,0,331,330,1,0,0,0,332,65,1,0,0,0,333,334,
        5,18,0,0,334,337,5,61,0,0,335,336,5,20,0,0,336,338,5,61,0,0,337,
        335,1,0,0,0,337,338,1,0,0,0,338,339,1,0,0,0,339,340,3,68,34,0,340,
        341,5,19,0,0,341,67,1,0,0,0,342,345,3,70,35,0,343,345,3,4,2,0,344,
        342,1,0,0,0,344,343,1,0,0,0,345,348,1,0,0,0,346,344,1,0,0,0,346,
        347,1,0,0,0,347,69,1,0,0,0,348,346,1,0,0,0,349,354,3,84,42,0,350,
        354,3,82,41,0,351,354,3,50,25,0,352,354,3,72,36,0,353,349,1,0,0,
        0,353,350,1,0,0,0,353,351,1,0,0,0,353,352,1,0,0,0,354,71,1,0,0,0,
        355,356,5,2,0,0,356,357,5,46,0,0,357,358,3,74,37,0,358,359,5,47,
        0,0,359,360,3,76,38,0,360,361,5,3,0,0,361,73,1,0,0,0,362,367,5,21,
        0,0,363,367,3,54,27,0,364,367,5,61,0,0,365,367,3,104,52,0,366,362,
        1,0,0,0,366,363,1,0,0,0,366,364,1,0,0,0,366,365,1,0,0,0,367,75,1,
        0,0,0,368,372,3,78,39,0,369,372,3,72,36,0,370,372,3,4,2,0,371,368,
        1,0,0,0,371,369,1,0,0,0,371,370,1,0,0,0,372,375,1,0,0,0,373,371,
        1,0,0,0,373,374,1,0,0,0,374,77,1,0,0,0,375,373,1,0,0,0,376,377,3,
        80,40,0,377,378,5,45,0,0,378,379,3,98,49,0,379,79,1,0,0,0,380,385,
        5,61,0,0,381,382,5,33,0,0,382,384,5,61,0,0,383,381,1,0,0,0,384,387,
        1,0,0,0,385,383,1,0,0,0,385,386,1,0,0,0,386,81,1,0,0,0,387,385,1,
        0,0,0,388,389,5,24,0,0,389,392,5,61,0,0,390,391,5,45,0,0,391,393,
        3,98,49,0,392,390,1,0,0,0,392,393,1,0,0,0,393,83,1,0,0,0,394,395,
        5,22,0,0,395,396,5,61,0,0,396,398,5,46,0,0,397,399,3,86,43,0,398,
        397,1,0,0,0,398,399,1,0,0,0,399,400,1,0,0,0,400,401,5,47,0,0,401,
        402,3,60,30,0,402,403,5,23,0,0,403,85,1,0,0,0,404,409,5,61,0,0,405,
        406,5,32,0,0,406,408,5,61,0,0,407,405,1,0,0,0,408,411,1,0,0,0,409,
        407,1,0,0,0,409,410,1,0,0,0,410,87,1,0,0,0,411,409,1,0,0,0,412,413,
        5,31,0,0,413,414,3,90,45,0,414,89,1,0,0,0,415,416,5,17,0,0,416,418,
        5,43,0,0,417,415,1,0,0,0,417,418,1,0,0,0,418,419,1,0,0,0,419,420,
        5,61,0,0,420,422,5,46,0,0,421,423,3,94,47,0,422,421,1,0,0,0,422,
        423,1,0,0,0,423,424,1,0,0,0,424,425,5,47,0,0,425,91,1,0,0,0,426,
        429,3,96,48,0,427,428,5,33,0,0,428,430,3,96,48,0,429,427,1,0,0,0,
        429,430,1,0,0,0,430,93,1,0,0,0,431,436,3,98,49,0,432,433,5,32,0,
        0,433,435,3,98,49,0,434,432,1,0,0,0,435,438,1,0,0,0,436,434,1,0,
        0,0,436,437,1,0,0,0,437,95,1,0,0,0,438,436,1,0,0,0,439,440,5,61,
        0,0,440,97,1,0,0,0,441,442,3,30,15,0,442,99,1,0,0,0,443,448,3,102,
        51,0,444,445,7,1,0,0,445,447,3,102,51,0,446,444,1,0,0,0,447,450,
        1,0,0,0,448,446,1,0,0,0,448,449,1,0,0,0,449,101,1,0,0,0,450,448,
        1,0,0,0,451,456,3,104,52,0,452,453,7,2,0,0,453,455,3,104,52,0,454,
        452,1,0,0,0,455,458,1,0,0,0,456,454,1,0,0,0,456,457,1,0,0,0,457,
        103,1,0,0,0,458,456,1,0,0,0,459,469,3,114,57,0,460,462,5,46,0,0,
        461,463,3,94,47,0,462,461,1,0,0,0,462,463,1,0,0,0,463,464,1,0,0,
        0,464,468,5,47,0,0,465,466,7,3,0,0,466,468,5,61,0,0,467,460,1,0,
        0,0,467,465,1,0,0,0,468,471,1,0,0,0,469,467,1,0,0,0,469,470,1,0,
        0,0,470,105,1,0,0,0,471,469,1,0,0,0,472,473,5,33,0,0,473,480,5,61,
        0,0,474,476,5,46,0,0,475,477,3,94,47,0,476,475,1,0,0,0,476,477,1,
        0,0,0,477,478,1,0,0,0,478,480,5,47,0,0,479,472,1,0,0,0,479,474,1,
        0,0,0,480,107,1,0,0,0,481,482,5,15,0,0,482,483,5,61,0,0,483,485,
        5,46,0,0,484,486,3,94,47,0,485,484,1,0,0,0,485,486,1,0,0,0,486,487,
        1,0,0,0,487,488,5,47,0,0,488,109,1,0,0,0,489,494,7,4,0,0,490,491,
        7,3,0,0,491,493,5,61,0,0,492,490,1,0,0,0,493,496,1,0,0,0,494,492,
        1,0,0,0,494,495,1,0,0,0,495,111,1,0,0,0,496,494,1,0,0,0,497,498,
        7,5,0,0,498,113,1,0,0,0,499,515,3,8,4,0,500,515,3,108,54,0,501,515,
        3,110,55,0,502,515,3,112,56,0,503,515,5,21,0,0,504,515,5,17,0,0,
        505,515,5,34,0,0,506,515,5,35,0,0,507,515,5,61,0,0,508,515,5,36,
        0,0,509,515,5,55,0,0,510,511,5,46,0,0,511,512,3,98,49,0,512,513,
        5,47,0,0,513,515,1,0,0,0,514,499,1,0,0,0,514,500,1,0,0,0,514,501,
        1,0,0,0,514,502,1,0,0,0,514,503,1,0,0,0,514,504,1,0,0,0,514,505,
        1,0,0,0,514,506,1,0,0,0,514,507,1,0,0,0,514,508,1,0,0,0,514,509,
        1,0,0,0,514,510,1,0,0,0,515,115,1,0,0,0,51,119,127,146,151,159,168,
        174,178,183,187,197,205,210,227,235,241,247,270,283,290,297,300,
        309,316,325,331,337,344,346,353,366,371,373,385,392,398,409,417,
        422,429,436,448,456,462,467,469,476,479,485,494,514
    ]

class dBaseParser ( Parser ):

    grammarFileName = "dBaseParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "','", "'.'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'<='", "'>='", "'!='", "'=='", "'<'", "'>'", "'::'", 
                     "':'", "'='", "'('", "')'", "'+'", "'-'", "'*'", "'/'", 
                     "'{'", "'}'", "';'" ]

    symbolicNames = [ "<INVALID>", "PARAMETER", "WITH", "ENDWITH", "PROGRAM", 
                      "RETURN", "FOR", "TO", "ENDFOR", "STEP", "BREAK", 
                      "DO", "WHILE", "ENDDO", "LOCAL", "NEW", "DELETE", 
                      "SUPER", "CLASS", "ENDCLASS", "OF", "THIS", "METHOD", 
                      "ENDMETHOD", "PROPERTY", "CREATE", "FILE", "IF", "ELSE", 
                      "ENDIF", "WRITE", "CALL", "COMMA", "DOT", "FLOAT", 
                      "NUMBER", "STRING", "LE", "GE", "NE", "EQ", "LT", 
                      "GT", "DCOLON", "COLON", "ASSIGN", "LPAREN", "RPAREN", 
                      "PLUS", "MINUS", "STAR", "SLASH", "LBRACE", "RBRACE", 
                      "SEMI", "BRACKET_STRING", "TRUE", "FALSE", "AND", 
                      "OR", "NOT", "IDENT", "WS", "LINECOMMENT_DBA", "LINECOMMENT_DBB", 
                      "LINECOMMENT_CPP", "BLOCKCOMMENT_START", "COMMENT_NEST_START", 
                      "COMMENT_END", "COMMENT_ANY" ]

    RULE_input = 0
    RULE_item = 1
    RULE_statement = 2
    RULE_createFileStmt = 3
    RULE_handlerList = 4
    RULE_breakStmt = 5
    RULE_returnStmt = 6
    RULE_doStmt = 7
    RULE_doTarget = 8
    RULE_programRef = 9
    RULE_parameterStmt = 10
    RULE_paramNames = 11
    RULE_callExpr = 12
    RULE_doWhileStatement = 13
    RULE_condition = 14
    RULE_logicalOr = 15
    RULE_logicalAnd = 16
    RULE_logicalNot = 17
    RULE_comparison = 18
    RULE_compareOp = 19
    RULE_localDeclStmt = 20
    RULE_localAssignStmt = 21
    RULE_deleteStmt = 22
    RULE_forStmt = 23
    RULE_numberExpr = 24
    RULE_assignStmt = 25
    RULE_lvalue = 26
    RULE_dottedRef = 27
    RULE_exprStmt = 28
    RULE_ifStmt = 29
    RULE_block = 30
    RULE_writeStmt = 31
    RULE_writeArg = 32
    RULE_classDecl = 33
    RULE_classBody = 34
    RULE_classMember = 35
    RULE_withStmt = 36
    RULE_withTarget = 37
    RULE_withBody = 38
    RULE_withAssignStmt = 39
    RULE_withLvalue = 40
    RULE_propertyDecl = 41
    RULE_methodDecl = 42
    RULE_paramList = 43
    RULE_callStmt = 44
    RULE_callTarget = 45
    RULE_qualifiedName = 46
    RULE_argList = 47
    RULE_identifier = 48
    RULE_expr = 49
    RULE_additiveExpr = 50
    RULE_multiplicativeExpr = 51
    RULE_postfixExpr = 52
    RULE_postfixSuffix = 53
    RULE_newExpr = 54
    RULE_memberExpr = 55
    RULE_literal = 56
    RULE_primary = 57

    ruleNames =  [ "input", "item", "statement", "createFileStmt", "handlerList", 
                   "breakStmt", "returnStmt", "doStmt", "doTarget", "programRef", 
                   "parameterStmt", "paramNames", "callExpr", "doWhileStatement", 
                   "condition", "logicalOr", "logicalAnd", "logicalNot", 
                   "comparison", "compareOp", "localDeclStmt", "localAssignStmt", 
                   "deleteStmt", "forStmt", "numberExpr", "assignStmt", 
                   "lvalue", "dottedRef", "exprStmt", "ifStmt", "block", 
                   "writeStmt", "writeArg", "classDecl", "classBody", "classMember", 
                   "withStmt", "withTarget", "withBody", "withAssignStmt", 
                   "withLvalue", "propertyDecl", "methodDecl", "paramList", 
                   "callStmt", "callTarget", "qualifiedName", "argList", 
                   "identifier", "expr", "additiveExpr", "multiplicativeExpr", 
                   "postfixExpr", "postfixSuffix", "newExpr", "memberExpr", 
                   "literal", "primary" ]

    EOF = Token.EOF
    PARAMETER=1
    WITH=2
    ENDWITH=3
    PROGRAM=4
    RETURN=5
    FOR=6
    TO=7
    ENDFOR=8
    STEP=9
    BREAK=10
    DO=11
    WHILE=12
    ENDDO=13
    LOCAL=14
    NEW=15
    DELETE=16
    SUPER=17
    CLASS=18
    ENDCLASS=19
    OF=20
    THIS=21
    METHOD=22
    ENDMETHOD=23
    PROPERTY=24
    CREATE=25
    FILE=26
    IF=27
    ELSE=28
    ENDIF=29
    WRITE=30
    CALL=31
    COMMA=32
    DOT=33
    FLOAT=34
    NUMBER=35
    STRING=36
    LE=37
    GE=38
    NE=39
    EQ=40
    LT=41
    GT=42
    DCOLON=43
    COLON=44
    ASSIGN=45
    LPAREN=46
    RPAREN=47
    PLUS=48
    MINUS=49
    STAR=50
    SLASH=51
    LBRACE=52
    RBRACE=53
    SEMI=54
    BRACKET_STRING=55
    TRUE=56
    FALSE=57
    AND=58
    OR=59
    NOT=60
    IDENT=61
    WS=62
    LINECOMMENT_DBA=63
    LINECOMMENT_DBB=64
    LINECOMMENT_CPP=65
    BLOCKCOMMENT_START=66
    COMMENT_NEST_START=67
    COMMENT_END=68
    COMMENT_ANY=69

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class InputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(dBaseParser.EOF, 0)

        def item(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.ItemContext)
            else:
                return self.getTypedRuleContext(dBaseParser.ItemContext,i)


        def getRuleIndex(self):
            return dBaseParser.RULE_input

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInput" ):
                listener.enterInput(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInput" ):
                listener.exitInput(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInput" ):
                return visitor.visitInput(self)
            else:
                return visitor.visitChildren(self)




    def input_(self):

        localctx = dBaseParser.InputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2562618680372874342) != 0):
                self.state = 116
                self.item()
                self.state = 121
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 122
            self.match(dBaseParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classDecl(self):
            return self.getTypedRuleContext(dBaseParser.ClassDeclContext,0)


        def methodDecl(self):
            return self.getTypedRuleContext(dBaseParser.MethodDeclContext,0)


        def statement(self):
            return self.getTypedRuleContext(dBaseParser.StatementContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_item

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterItem" ):
                listener.enterItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitItem" ):
                listener.exitItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitItem" ):
                return visitor.visitItem(self)
            else:
                return visitor.visitChildren(self)




    def item(self):

        localctx = dBaseParser.ItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_item)
        try:
            self.state = 127
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                self.classDecl()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 125
                self.methodDecl()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 126
                self.statement()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ifStmt(self):
            return self.getTypedRuleContext(dBaseParser.IfStmtContext,0)


        def doStmt(self):
            return self.getTypedRuleContext(dBaseParser.DoStmtContext,0)


        def breakStmt(self):
            return self.getTypedRuleContext(dBaseParser.BreakStmtContext,0)


        def parameterStmt(self):
            return self.getTypedRuleContext(dBaseParser.ParameterStmtContext,0)


        def writeStmt(self):
            return self.getTypedRuleContext(dBaseParser.WriteStmtContext,0)


        def assignStmt(self):
            return self.getTypedRuleContext(dBaseParser.AssignStmtContext,0)


        def createFileStmt(self):
            return self.getTypedRuleContext(dBaseParser.CreateFileStmtContext,0)


        def exprStmt(self):
            return self.getTypedRuleContext(dBaseParser.ExprStmtContext,0)


        def localAssignStmt(self):
            return self.getTypedRuleContext(dBaseParser.LocalAssignStmtContext,0)


        def localDeclStmt(self):
            return self.getTypedRuleContext(dBaseParser.LocalDeclStmtContext,0)


        def callStmt(self):
            return self.getTypedRuleContext(dBaseParser.CallStmtContext,0)


        def classDecl(self):
            return self.getTypedRuleContext(dBaseParser.ClassDeclContext,0)


        def forStmt(self):
            return self.getTypedRuleContext(dBaseParser.ForStmtContext,0)


        def doWhileStatement(self):
            return self.getTypedRuleContext(dBaseParser.DoWhileStatementContext,0)


        def deleteStmt(self):
            return self.getTypedRuleContext(dBaseParser.DeleteStmtContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(dBaseParser.ReturnStmtContext,0)


        def withStmt(self):
            return self.getTypedRuleContext(dBaseParser.WithStmtContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = dBaseParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_statement)
        try:
            self.state = 146
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 129
                self.ifStmt()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 130
                self.doStmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 131
                self.breakStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 132
                self.parameterStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 133
                self.writeStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 134
                self.assignStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 135
                self.createFileStmt()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 136
                self.exprStmt()
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 137
                self.localAssignStmt()
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 138
                self.localDeclStmt()
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 139
                self.callStmt()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 140
                self.classDecl()
                pass

            elif la_ == 13:
                self.enterOuterAlt(localctx, 13)
                self.state = 141
                self.forStmt()
                pass

            elif la_ == 14:
                self.enterOuterAlt(localctx, 14)
                self.state = 142
                self.doWhileStatement()
                pass

            elif la_ == 15:
                self.enterOuterAlt(localctx, 15)
                self.state = 143
                self.deleteStmt()
                pass

            elif la_ == 16:
                self.enterOuterAlt(localctx, 16)
                self.state = 144
                self.returnStmt()
                pass

            elif la_ == 17:
                self.enterOuterAlt(localctx, 17)
                self.state = 145
                self.withStmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CreateFileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CREATE(self):
            return self.getToken(dBaseParser.CREATE, 0)

        def FILE(self):
            return self.getToken(dBaseParser.FILE, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_createFileStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCreateFileStmt" ):
                listener.enterCreateFileStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCreateFileStmt" ):
                listener.exitCreateFileStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCreateFileStmt" ):
                return visitor.visitCreateFileStmt(self)
            else:
                return visitor.visitChildren(self)




    def createFileStmt(self):

        localctx = dBaseParser.CreateFileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_createFileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.match(dBaseParser.CREATE)
            self.state = 149
            self.match(dBaseParser.FILE)
            self.state = 151
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 150
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HandlerListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(dBaseParser.LBRACE, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.ExprContext)
            else:
                return self.getTypedRuleContext(dBaseParser.ExprContext,i)


        def RBRACE(self):
            return self.getToken(dBaseParser.RBRACE, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.SEMI)
            else:
                return self.getToken(dBaseParser.SEMI, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_handlerList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHandlerList" ):
                listener.enterHandlerList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHandlerList" ):
                listener.exitHandlerList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHandlerList" ):
                return visitor.visitHandlerList(self)
            else:
                return visitor.visitChildren(self)




    def handlerList(self):

        localctx = dBaseParser.HandlerListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_handlerList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 153
            self.match(dBaseParser.LBRACE)
            self.state = 154
            self.expr()
            self.state = 159
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==54:
                self.state = 155
                self.match(dBaseParser.SEMI)
                self.state = 156
                self.expr()
                self.state = 161
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 162
            self.match(dBaseParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BREAK(self):
            return self.getToken(dBaseParser.BREAK, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_breakStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStmt" ):
                listener.enterBreakStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStmt" ):
                listener.exitBreakStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStmt" ):
                return visitor.visitBreakStmt(self)
            else:
                return visitor.visitChildren(self)




    def breakStmt(self):

        localctx = dBaseParser.BreakStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_breakStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 164
            self.match(dBaseParser.BREAK)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(dBaseParser.RETURN, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStmt" ):
                return visitor.visitReturnStmt(self)
            else:
                return visitor.visitChildren(self)




    def returnStmt(self):

        localctx = dBaseParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 166
            self.match(dBaseParser.RETURN)
            self.state = 168
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 167
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DO(self):
            return self.getToken(dBaseParser.DO, 0)

        def doTarget(self):
            return self.getTypedRuleContext(dBaseParser.DoTargetContext,0)


        def WITH(self):
            return self.getToken(dBaseParser.WITH, 0)

        def argList(self):
            return self.getTypedRuleContext(dBaseParser.ArgListContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_doStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoStmt" ):
                listener.enterDoStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoStmt" ):
                listener.exitDoStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoStmt" ):
                return visitor.visitDoStmt(self)
            else:
                return visitor.visitChildren(self)




    def doStmt(self):

        localctx = dBaseParser.DoStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_doStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.match(dBaseParser.DO)
            self.state = 171
            self.doTarget()
            self.state = 174
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 172
                self.match(dBaseParser.WITH)
                self.state = 173
                self.argList()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoTargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def programRef(self):
            return self.getTypedRuleContext(dBaseParser.ProgramRefContext,0)


        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_doTarget

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoTarget" ):
                listener.enterDoTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoTarget" ):
                listener.exitDoTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoTarget" ):
                return visitor.visitDoTarget(self)
            else:
                return visitor.visitChildren(self)




    def doTarget(self):

        localctx = dBaseParser.DoTargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_doTarget)
        try:
            self.state = 178
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 176
                self.programRef()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 177
                self.match(dBaseParser.IDENT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def DOT(self):
            return self.getToken(dBaseParser.DOT, 0)

        def PROGRAM(self):
            return self.getToken(dBaseParser.PROGRAM, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_programRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgramRef" ):
                listener.enterProgramRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgramRef" ):
                listener.exitProgramRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgramRef" ):
                return visitor.visitProgramRef(self)
            else:
                return visitor.visitChildren(self)




    def programRef(self):

        localctx = dBaseParser.ProgramRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_programRef)
        self._la = 0 # Token type
        try:
            self.state = 187
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [61]:
                self.enterOuterAlt(localctx, 1)
                self.state = 180
                self.match(dBaseParser.IDENT)
                self.state = 183
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==33:
                    self.state = 181
                    self.match(dBaseParser.DOT)
                    self.state = 182
                    self.match(dBaseParser.IDENT)


                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 185
                self.match(dBaseParser.PROGRAM)
                self.state = 186
                self.match(dBaseParser.IDENT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PARAMETER(self):
            return self.getToken(dBaseParser.PARAMETER, 0)

        def paramNames(self):
            return self.getTypedRuleContext(dBaseParser.ParamNamesContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_parameterStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameterStmt" ):
                listener.enterParameterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameterStmt" ):
                listener.exitParameterStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameterStmt" ):
                return visitor.visitParameterStmt(self)
            else:
                return visitor.visitChildren(self)




    def parameterStmt(self):

        localctx = dBaseParser.ParameterStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_parameterStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 189
            self.match(dBaseParser.PARAMETER)
            self.state = 190
            self.paramNames()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamNamesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.COMMA)
            else:
                return self.getToken(dBaseParser.COMMA, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_paramNames

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamNames" ):
                listener.enterParamNames(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamNames" ):
                listener.exitParamNames(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamNames" ):
                return visitor.visitParamNames(self)
            else:
                return visitor.visitChildren(self)




    def paramNames(self):

        localctx = dBaseParser.ParamNamesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_paramNames)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
            self.match(dBaseParser.IDENT)
            self.state = 197
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 193
                self.match(dBaseParser.COMMA)
                self.state = 194
                self.match(dBaseParser.IDENT)
                self.state = 199
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(dBaseParser.PrimaryContext,0)


        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DOT)
            else:
                return self.getToken(dBaseParser.DOT, i)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def argList(self):
            return self.getTypedRuleContext(dBaseParser.ArgListContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_callExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallExpr" ):
                listener.enterCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallExpr" ):
                listener.exitCallExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallExpr" ):
                return visitor.visitCallExpr(self)
            else:
                return visitor.visitChildren(self)




    def callExpr(self):

        localctx = dBaseParser.CallExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_callExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self.primary()
            self.state = 205
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 201
                self.match(dBaseParser.DOT)
                self.state = 202
                self.match(dBaseParser.IDENT)
                self.state = 207
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 208
            self.match(dBaseParser.LPAREN)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3715540181586182144) != 0):
                self.state = 209
                self.argList()


            self.state = 212
            self.match(dBaseParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DoWhileStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DO(self):
            return self.getToken(dBaseParser.DO, 0)

        def WHILE(self):
            return self.getToken(dBaseParser.WHILE, 0)

        def condition(self):
            return self.getTypedRuleContext(dBaseParser.ConditionContext,0)


        def block(self):
            return self.getTypedRuleContext(dBaseParser.BlockContext,0)


        def ENDDO(self):
            return self.getToken(dBaseParser.ENDDO, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_doWhileStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoWhileStatement" ):
                listener.enterDoWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoWhileStatement" ):
                listener.exitDoWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoWhileStatement" ):
                return visitor.visitDoWhileStatement(self)
            else:
                return visitor.visitChildren(self)




    def doWhileStatement(self):

        localctx = dBaseParser.DoWhileStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_doWhileStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 214
            self.match(dBaseParser.DO)
            self.state = 215
            self.match(dBaseParser.WHILE)
            self.state = 216
            self.condition()
            self.state = 217
            self.block()
            self.state = 218
            self.match(dBaseParser.ENDDO)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOr(self):
            return self.getTypedRuleContext(dBaseParser.LogicalOrContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = dBaseParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_condition)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 220
            self.logicalOr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalOrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalAnd(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.LogicalAndContext)
            else:
                return self.getTypedRuleContext(dBaseParser.LogicalAndContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.OR)
            else:
                return self.getToken(dBaseParser.OR, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_logicalOr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalOr" ):
                listener.enterLogicalOr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalOr" ):
                listener.exitLogicalOr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalOr" ):
                return visitor.visitLogicalOr(self)
            else:
                return visitor.visitChildren(self)




    def logicalOr(self):

        localctx = dBaseParser.LogicalOrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_logicalOr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            self.logicalAnd()
            self.state = 227
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==59:
                self.state = 223
                self.match(dBaseParser.OR)
                self.state = 224
                self.logicalAnd()
                self.state = 229
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalAndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalNot(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.LogicalNotContext)
            else:
                return self.getTypedRuleContext(dBaseParser.LogicalNotContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.AND)
            else:
                return self.getToken(dBaseParser.AND, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_logicalAnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalAnd" ):
                listener.enterLogicalAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalAnd" ):
                listener.exitLogicalAnd(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalAnd" ):
                return visitor.visitLogicalAnd(self)
            else:
                return visitor.visitChildren(self)




    def logicalAnd(self):

        localctx = dBaseParser.LogicalAndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_logicalAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            self.logicalNot()
            self.state = 235
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==58:
                self.state = 231
                self.match(dBaseParser.AND)
                self.state = 232
                self.logicalNot()
                self.state = 237
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalNotContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(dBaseParser.NOT, 0)

        def logicalNot(self):
            return self.getTypedRuleContext(dBaseParser.LogicalNotContext,0)


        def comparison(self):
            return self.getTypedRuleContext(dBaseParser.ComparisonContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_logicalNot

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalNot" ):
                listener.enterLogicalNot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalNot" ):
                listener.exitLogicalNot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalNot" ):
                return visitor.visitLogicalNot(self)
            else:
                return visitor.visitChildren(self)




    def logicalNot(self):

        localctx = dBaseParser.LogicalNotContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_logicalNot)
        try:
            self.state = 241
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [60]:
                self.enterOuterAlt(localctx, 1)
                self.state = 238
                self.match(dBaseParser.NOT)
                self.state = 239
                self.logicalNot()
                pass
            elif token in [15, 17, 21, 34, 35, 36, 46, 52, 55, 56, 57, 61]:
                self.enterOuterAlt(localctx, 2)
                self.state = 240
                self.comparison()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additiveExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.AdditiveExprContext)
            else:
                return self.getTypedRuleContext(dBaseParser.AdditiveExprContext,i)


        def compareOp(self):
            return self.getTypedRuleContext(dBaseParser.CompareOpContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_comparison

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = dBaseParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 243
            self.additiveExpr()
            self.state = 247
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8658654068736) != 0):
                self.state = 244
                self.compareOp()
                self.state = 245
                self.additiveExpr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CompareOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LT(self):
            return self.getToken(dBaseParser.LT, 0)

        def LE(self):
            return self.getToken(dBaseParser.LE, 0)

        def GT(self):
            return self.getToken(dBaseParser.GT, 0)

        def GE(self):
            return self.getToken(dBaseParser.GE, 0)

        def EQ(self):
            return self.getToken(dBaseParser.EQ, 0)

        def NE(self):
            return self.getToken(dBaseParser.NE, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_compareOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompareOp" ):
                listener.enterCompareOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompareOp" ):
                listener.exitCompareOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompareOp" ):
                return visitor.visitCompareOp(self)
            else:
                return visitor.visitChildren(self)




    def compareOp(self):

        localctx = dBaseParser.CompareOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_compareOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 249
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 8658654068736) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocalDeclStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def LOCAL(self):
            return self.getToken(dBaseParser.LOCAL, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_localDeclStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLocalDeclStmt" ):
                listener.enterLocalDeclStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLocalDeclStmt" ):
                listener.exitLocalDeclStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLocalDeclStmt" ):
                return visitor.visitLocalDeclStmt(self)
            else:
                return visitor.visitChildren(self)




    def localDeclStmt(self):

        localctx = dBaseParser.LocalDeclStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_localDeclStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 251
            self.match(dBaseParser.LOCAL)
            self.state = 252
            localctx.name = self.match(dBaseParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LocalAssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def LOCAL(self):
            return self.getToken(dBaseParser.LOCAL, 0)

        def ASSIGN(self):
            return self.getToken(dBaseParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_localAssignStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLocalAssignStmt" ):
                listener.enterLocalAssignStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLocalAssignStmt" ):
                listener.exitLocalAssignStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLocalAssignStmt" ):
                return visitor.visitLocalAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def localAssignStmt(self):

        localctx = dBaseParser.LocalAssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_localAssignStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 254
            self.match(dBaseParser.LOCAL)
            self.state = 255
            localctx.name = self.match(dBaseParser.IDENT)
            self.state = 256
            self.match(dBaseParser.ASSIGN)
            self.state = 257
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeleteStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DELETE(self):
            return self.getToken(dBaseParser.DELETE, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_deleteStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeleteStmt" ):
                listener.enterDeleteStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeleteStmt" ):
                listener.exitDeleteStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeleteStmt" ):
                return visitor.visitDeleteStmt(self)
            else:
                return visitor.visitChildren(self)




    def deleteStmt(self):

        localctx = dBaseParser.DeleteStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_deleteStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 259
            self.match(dBaseParser.DELETE)
            self.state = 260
            self.match(dBaseParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(dBaseParser.FOR, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def ASSIGN(self):
            return self.getToken(dBaseParser.ASSIGN, 0)

        def numberExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.NumberExprContext)
            else:
                return self.getTypedRuleContext(dBaseParser.NumberExprContext,i)


        def TO(self):
            return self.getToken(dBaseParser.TO, 0)

        def block(self):
            return self.getTypedRuleContext(dBaseParser.BlockContext,0)


        def ENDFOR(self):
            return self.getToken(dBaseParser.ENDFOR, 0)

        def STEP(self):
            return self.getToken(dBaseParser.STEP, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStmt" ):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)




    def forStmt(self):

        localctx = dBaseParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_forStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self.match(dBaseParser.FOR)
            self.state = 263
            self.match(dBaseParser.IDENT)
            self.state = 264
            self.match(dBaseParser.ASSIGN)
            self.state = 265
            self.numberExpr()
            self.state = 266
            self.match(dBaseParser.TO)
            self.state = 267
            self.numberExpr()
            self.state = 270
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9:
                self.state = 268
                self.match(dBaseParser.STEP)
                self.state = 269
                self.numberExpr()


            self.state = 272
            self.block()
            self.state = 273
            self.match(dBaseParser.ENDFOR)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(dBaseParser.NUMBER, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_numberExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberExpr" ):
                listener.enterNumberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberExpr" ):
                listener.exitNumberExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberExpr" ):
                return visitor.visitNumberExpr(self)
            else:
                return visitor.visitChildren(self)




    def numberExpr(self):

        localctx = dBaseParser.NumberExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_numberExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 275
            self.match(dBaseParser.NUMBER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lvalue(self):
            return self.getTypedRuleContext(dBaseParser.LvalueContext,0)


        def ASSIGN(self):
            return self.getToken(dBaseParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_assignStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStmt" ):
                listener.enterAssignStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStmt" ):
                listener.exitAssignStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStmt" ):
                return visitor.visitAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def assignStmt(self):

        localctx = dBaseParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_assignStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 277
            self.lvalue()
            self.state = 278
            self.match(dBaseParser.ASSIGN)
            self.state = 279
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LvalueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def postfixExpr(self):
            return self.getTypedRuleContext(dBaseParser.PostfixExprContext,0)


        def dottedRef(self):
            return self.getTypedRuleContext(dBaseParser.DottedRefContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_lvalue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLvalue" ):
                listener.enterLvalue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLvalue" ):
                listener.exitLvalue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLvalue" ):
                return visitor.visitLvalue(self)
            else:
                return visitor.visitChildren(self)




    def lvalue(self):

        localctx = dBaseParser.LvalueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_lvalue)
        try:
            self.state = 283
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 281
                self.postfixExpr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 282
                self.dottedRef()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DottedRefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def THIS(self):
            return self.getToken(dBaseParser.THIS, 0)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DOT)
            else:
                return self.getToken(dBaseParser.DOT, i)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_dottedRef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDottedRef" ):
                listener.enterDottedRef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDottedRef" ):
                listener.exitDottedRef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDottedRef" ):
                return visitor.visitDottedRef(self)
            else:
                return visitor.visitChildren(self)




    def dottedRef(self):

        localctx = dBaseParser.DottedRefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_dottedRef)
        self._la = 0 # Token type
        try:
            self.state = 300
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [21]:
                self.enterOuterAlt(localctx, 1)
                self.state = 285
                self.match(dBaseParser.THIS)
                self.state = 288 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 286
                    self.match(dBaseParser.DOT)
                    self.state = 287
                    self.match(dBaseParser.IDENT)
                    self.state = 290 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==33):
                        break

                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 2)
                self.state = 292
                self.match(dBaseParser.IDENT)
                self.state = 297
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==33:
                    self.state = 293
                    self.match(dBaseParser.DOT)
                    self.state = 294
                    self.match(dBaseParser.IDENT)
                    self.state = 299
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def postfixExpr(self):
            return self.getTypedRuleContext(dBaseParser.PostfixExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_exprStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprStmt" ):
                listener.enterExprStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprStmt" ):
                listener.exitExprStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprStmt" ):
                return visitor.visitExprStmt(self)
            else:
                return visitor.visitChildren(self)




    def exprStmt(self):

        localctx = dBaseParser.ExprStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_exprStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 302
            self.postfixExpr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(dBaseParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.BlockContext)
            else:
                return self.getTypedRuleContext(dBaseParser.BlockContext,i)


        def ENDIF(self):
            return self.getToken(dBaseParser.ENDIF, 0)

        def ELSE(self):
            return self.getToken(dBaseParser.ELSE, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = dBaseParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 304
            self.match(dBaseParser.IF)
            self.state = 305
            self.expr()
            self.state = 306
            self.block()
            self.state = 309
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==28:
                self.state = 307
                self.match(dBaseParser.ELSE)
                self.state = 308
                self.block()


            self.state = 311
            self.match(dBaseParser.ENDIF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.StatementContext)
            else:
                return self.getTypedRuleContext(dBaseParser.StatementContext,i)


        def getRuleIndex(self):
            return dBaseParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = dBaseParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 316
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2562618680368680038) != 0):
                self.state = 313
                self.statement()
                self.state = 318
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WriteStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WRITE(self):
            return self.getToken(dBaseParser.WRITE, 0)

        def writeArg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.WriteArgContext)
            else:
                return self.getTypedRuleContext(dBaseParser.WriteArgContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.PLUS)
            else:
                return self.getToken(dBaseParser.PLUS, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_writeStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWriteStmt" ):
                listener.enterWriteStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWriteStmt" ):
                listener.exitWriteStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWriteStmt" ):
                return visitor.visitWriteStmt(self)
            else:
                return visitor.visitChildren(self)




    def writeStmt(self):

        localctx = dBaseParser.WriteStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_writeStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 319
            self.match(dBaseParser.WRITE)
            self.state = 320
            self.writeArg()
            self.state = 325
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==48:
                self.state = 321
                self.match(dBaseParser.PLUS)
                self.state = 322
                self.writeArg()
                self.state = 327
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WriteArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(dBaseParser.STRING, 0)

        def dottedRef(self):
            return self.getTypedRuleContext(dBaseParser.DottedRefContext,0)


        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_writeArg

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWriteArg" ):
                listener.enterWriteArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWriteArg" ):
                listener.exitWriteArg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWriteArg" ):
                return visitor.visitWriteArg(self)
            else:
                return visitor.visitChildren(self)




    def writeArg(self):

        localctx = dBaseParser.WriteArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_writeArg)
        try:
            self.state = 331
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,25,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 328
                self.match(dBaseParser.STRING)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 329
                self.dottedRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 330
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token
            self.parent = None # Token

        def CLASS(self):
            return self.getToken(dBaseParser.CLASS, 0)

        def classBody(self):
            return self.getTypedRuleContext(dBaseParser.ClassBodyContext,0)


        def ENDCLASS(self):
            return self.getToken(dBaseParser.ENDCLASS, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def OF(self):
            return self.getToken(dBaseParser.OF, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_classDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassDecl" ):
                listener.enterClassDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassDecl" ):
                listener.exitClassDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassDecl" ):
                return visitor.visitClassDecl(self)
            else:
                return visitor.visitChildren(self)




    def classDecl(self):

        localctx = dBaseParser.ClassDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_classDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 333
            self.match(dBaseParser.CLASS)
            self.state = 334
            localctx.name = self.match(dBaseParser.IDENT)
            self.state = 337
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 335
                self.match(dBaseParser.OF)
                self.state = 336
                localctx.parent = self.match(dBaseParser.IDENT)


            self.state = 339
            self.classBody()
            self.state = 340
            self.match(dBaseParser.ENDCLASS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def classMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.ClassMemberContext)
            else:
                return self.getTypedRuleContext(dBaseParser.ClassMemberContext,i)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.StatementContext)
            else:
                return self.getTypedRuleContext(dBaseParser.StatementContext,i)


        def getRuleIndex(self):
            return dBaseParser.RULE_classBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassBody" ):
                listener.enterClassBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassBody" ):
                listener.exitClassBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassBody" ):
                return visitor.visitClassBody(self)
            else:
                return visitor.visitChildren(self)




    def classBody(self):

        localctx = dBaseParser.ClassBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_classBody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 346
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2562618680389651558) != 0):
                self.state = 344
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,27,self._ctx)
                if la_ == 1:
                    self.state = 342
                    self.classMember()
                    pass

                elif la_ == 2:
                    self.state = 343
                    self.statement()
                    pass


                self.state = 348
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ClassMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def methodDecl(self):
            return self.getTypedRuleContext(dBaseParser.MethodDeclContext,0)


        def propertyDecl(self):
            return self.getTypedRuleContext(dBaseParser.PropertyDeclContext,0)


        def assignStmt(self):
            return self.getTypedRuleContext(dBaseParser.AssignStmtContext,0)


        def withStmt(self):
            return self.getTypedRuleContext(dBaseParser.WithStmtContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_classMember

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterClassMember" ):
                listener.enterClassMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitClassMember" ):
                listener.exitClassMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitClassMember" ):
                return visitor.visitClassMember(self)
            else:
                return visitor.visitChildren(self)




    def classMember(self):

        localctx = dBaseParser.ClassMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_classMember)
        try:
            self.state = 353
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [22]:
                self.enterOuterAlt(localctx, 1)
                self.state = 349
                self.methodDecl()
                pass
            elif token in [24]:
                self.enterOuterAlt(localctx, 2)
                self.state = 350
                self.propertyDecl()
                pass
            elif token in [15, 17, 21, 34, 35, 36, 46, 52, 55, 56, 57, 61]:
                self.enterOuterAlt(localctx, 3)
                self.state = 351
                self.assignStmt()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 4)
                self.state = 352
                self.withStmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WithStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WITH(self):
            return self.getToken(dBaseParser.WITH, 0)

        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def withTarget(self):
            return self.getTypedRuleContext(dBaseParser.WithTargetContext,0)


        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def withBody(self):
            return self.getTypedRuleContext(dBaseParser.WithBodyContext,0)


        def ENDWITH(self):
            return self.getToken(dBaseParser.ENDWITH, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_withStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithStmt" ):
                listener.enterWithStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithStmt" ):
                listener.exitWithStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWithStmt" ):
                return visitor.visitWithStmt(self)
            else:
                return visitor.visitChildren(self)




    def withStmt(self):

        localctx = dBaseParser.WithStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_withStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 355
            self.match(dBaseParser.WITH)
            self.state = 356
            self.match(dBaseParser.LPAREN)
            self.state = 357
            self.withTarget()
            self.state = 358
            self.match(dBaseParser.RPAREN)
            self.state = 359
            self.withBody()
            self.state = 360
            self.match(dBaseParser.ENDWITH)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WithTargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def THIS(self):
            return self.getToken(dBaseParser.THIS, 0)

        def dottedRef(self):
            return self.getTypedRuleContext(dBaseParser.DottedRefContext,0)


        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def postfixExpr(self):
            return self.getTypedRuleContext(dBaseParser.PostfixExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_withTarget

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithTarget" ):
                listener.enterWithTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithTarget" ):
                listener.exitWithTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWithTarget" ):
                return visitor.visitWithTarget(self)
            else:
                return visitor.visitChildren(self)




    def withTarget(self):

        localctx = dBaseParser.WithTargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_withTarget)
        try:
            self.state = 366
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,30,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 362
                self.match(dBaseParser.THIS)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 363
                self.dottedRef()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 364
                self.match(dBaseParser.IDENT)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 365
                self.postfixExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WithBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def withAssignStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.WithAssignStmtContext)
            else:
                return self.getTypedRuleContext(dBaseParser.WithAssignStmtContext,i)


        def withStmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.WithStmtContext)
            else:
                return self.getTypedRuleContext(dBaseParser.WithStmtContext,i)


        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.StatementContext)
            else:
                return self.getTypedRuleContext(dBaseParser.StatementContext,i)


        def getRuleIndex(self):
            return dBaseParser.RULE_withBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithBody" ):
                listener.enterWithBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithBody" ):
                listener.exitWithBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWithBody" ):
                return visitor.visitWithBody(self)
            else:
                return visitor.visitChildren(self)




    def withBody(self):

        localctx = dBaseParser.WithBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_withBody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 373
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 2562618680368680038) != 0):
                self.state = 371
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,31,self._ctx)
                if la_ == 1:
                    self.state = 368
                    self.withAssignStmt()
                    pass

                elif la_ == 2:
                    self.state = 369
                    self.withStmt()
                    pass

                elif la_ == 3:
                    self.state = 370
                    self.statement()
                    pass


                self.state = 375
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WithAssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def withLvalue(self):
            return self.getTypedRuleContext(dBaseParser.WithLvalueContext,0)


        def ASSIGN(self):
            return self.getToken(dBaseParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_withAssignStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithAssignStmt" ):
                listener.enterWithAssignStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithAssignStmt" ):
                listener.exitWithAssignStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWithAssignStmt" ):
                return visitor.visitWithAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def withAssignStmt(self):

        localctx = dBaseParser.WithAssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_withAssignStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 376
            self.withLvalue()
            self.state = 377
            self.match(dBaseParser.ASSIGN)
            self.state = 378
            self.expr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WithLvalueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DOT)
            else:
                return self.getToken(dBaseParser.DOT, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_withLvalue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWithLvalue" ):
                listener.enterWithLvalue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWithLvalue" ):
                listener.exitWithLvalue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWithLvalue" ):
                return visitor.visitWithLvalue(self)
            else:
                return visitor.visitChildren(self)




    def withLvalue(self):

        localctx = dBaseParser.WithLvalueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_withLvalue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 380
            self.match(dBaseParser.IDENT)
            self.state = 385
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==33:
                self.state = 381
                self.match(dBaseParser.DOT)
                self.state = 382
                self.match(dBaseParser.IDENT)
                self.state = 387
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PROPERTY(self):
            return self.getToken(dBaseParser.PROPERTY, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def ASSIGN(self):
            return self.getToken(dBaseParser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_propertyDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyDecl" ):
                listener.enterPropertyDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyDecl" ):
                listener.exitPropertyDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertyDecl" ):
                return visitor.visitPropertyDecl(self)
            else:
                return visitor.visitChildren(self)




    def propertyDecl(self):

        localctx = dBaseParser.PropertyDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 82, self.RULE_propertyDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 388
            self.match(dBaseParser.PROPERTY)
            self.state = 389
            self.match(dBaseParser.IDENT)
            self.state = 392
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==45:
                self.state = 390
                self.match(dBaseParser.ASSIGN)
                self.state = 391
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MethodDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def METHOD(self):
            return self.getToken(dBaseParser.METHOD, 0)

        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(dBaseParser.BlockContext,0)


        def ENDMETHOD(self):
            return self.getToken(dBaseParser.ENDMETHOD, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def paramList(self):
            return self.getTypedRuleContext(dBaseParser.ParamListContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_methodDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMethodDecl" ):
                listener.enterMethodDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMethodDecl" ):
                listener.exitMethodDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMethodDecl" ):
                return visitor.visitMethodDecl(self)
            else:
                return visitor.visitChildren(self)




    def methodDecl(self):

        localctx = dBaseParser.MethodDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 84, self.RULE_methodDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 394
            self.match(dBaseParser.METHOD)
            self.state = 395
            localctx.name = self.match(dBaseParser.IDENT)
            self.state = 396
            self.match(dBaseParser.LPAREN)
            self.state = 398
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==61:
                self.state = 397
                self.paramList()


            self.state = 400
            self.match(dBaseParser.RPAREN)
            self.state = 401
            self.block()
            self.state = 402
            self.match(dBaseParser.ENDMETHOD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.COMMA)
            else:
                return self.getToken(dBaseParser.COMMA, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = dBaseParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 86, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 404
            self.match(dBaseParser.IDENT)
            self.state = 409
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 405
                self.match(dBaseParser.COMMA)
                self.state = 406
                self.match(dBaseParser.IDENT)
                self.state = 411
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CALL(self):
            return self.getToken(dBaseParser.CALL, 0)

        def callTarget(self):
            return self.getTypedRuleContext(dBaseParser.CallTargetContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_callStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallStmt" ):
                listener.enterCallStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallStmt" ):
                listener.exitCallStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallStmt" ):
                return visitor.visitCallStmt(self)
            else:
                return visitor.visitChildren(self)




    def callStmt(self):

        localctx = dBaseParser.CallStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 88, self.RULE_callStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 412
            self.match(dBaseParser.CALL)
            self.state = 413
            self.callTarget()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CallTargetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def SUPER(self):
            return self.getToken(dBaseParser.SUPER, 0)

        def DCOLON(self):
            return self.getToken(dBaseParser.DCOLON, 0)

        def argList(self):
            return self.getTypedRuleContext(dBaseParser.ArgListContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_callTarget

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCallTarget" ):
                listener.enterCallTarget(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCallTarget" ):
                listener.exitCallTarget(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallTarget" ):
                return visitor.visitCallTarget(self)
            else:
                return visitor.visitChildren(self)




    def callTarget(self):

        localctx = dBaseParser.CallTargetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 90, self.RULE_callTarget)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 417
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==17:
                self.state = 415
                self.match(dBaseParser.SUPER)
                self.state = 416
                self.match(dBaseParser.DCOLON)


            self.state = 419
            self.match(dBaseParser.IDENT)
            self.state = 420
            self.match(dBaseParser.LPAREN)
            self.state = 422
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3715540181586182144) != 0):
                self.state = 421
                self.argList()


            self.state = 424
            self.match(dBaseParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifiedNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def identifier(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.IdentifierContext)
            else:
                return self.getTypedRuleContext(dBaseParser.IdentifierContext,i)


        def DOT(self):
            return self.getToken(dBaseParser.DOT, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_qualifiedName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedName" ):
                listener.enterQualifiedName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedName" ):
                listener.exitQualifiedName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQualifiedName" ):
                return visitor.visitQualifiedName(self)
            else:
                return visitor.visitChildren(self)




    def qualifiedName(self):

        localctx = dBaseParser.QualifiedNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 92, self.RULE_qualifiedName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 426
            self.identifier()
            self.state = 429
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==33:
                self.state = 427
                self.match(dBaseParser.DOT)
                self.state = 428
                self.identifier()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.ExprContext)
            else:
                return self.getTypedRuleContext(dBaseParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.COMMA)
            else:
                return self.getToken(dBaseParser.COMMA, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_argList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgList" ):
                listener.enterArgList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgList" ):
                listener.exitArgList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgList" ):
                return visitor.visitArgList(self)
            else:
                return visitor.visitChildren(self)




    def argList(self):

        localctx = dBaseParser.ArgListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 94, self.RULE_argList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 431
            self.expr()
            self.state = 436
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32:
                self.state = 432
                self.match(dBaseParser.COMMA)
                self.state = 433
                self.expr()
                self.state = 438
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdentifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentifier" ):
                listener.enterIdentifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentifier" ):
                listener.exitIdentifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentifier" ):
                return visitor.visitIdentifier(self)
            else:
                return visitor.visitChildren(self)




    def identifier(self):

        localctx = dBaseParser.IdentifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 96, self.RULE_identifier)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 439
            self.match(dBaseParser.IDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logicalOr(self):
            return self.getTypedRuleContext(dBaseParser.LogicalOrContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = dBaseParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 98, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 441
            self.logicalOr()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.MultiplicativeExprContext)
            else:
                return self.getTypedRuleContext(dBaseParser.MultiplicativeExprContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.PLUS)
            else:
                return self.getToken(dBaseParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.MINUS)
            else:
                return self.getToken(dBaseParser.MINUS, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_additiveExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpr" ):
                listener.enterAdditiveExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpr" ):
                listener.exitAdditiveExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)




    def additiveExpr(self):

        localctx = dBaseParser.AdditiveExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 100, self.RULE_additiveExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 443
            self.multiplicativeExpr()
            self.state = 448
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,41,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 444
                    _la = self._input.LA(1)
                    if not(_la==48 or _la==49):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 445
                    self.multiplicativeExpr() 
                self.state = 450
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,41,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def postfixExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.PostfixExprContext)
            else:
                return self.getTypedRuleContext(dBaseParser.PostfixExprContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.STAR)
            else:
                return self.getToken(dBaseParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.SLASH)
            else:
                return self.getToken(dBaseParser.SLASH, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_multiplicativeExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpr" ):
                listener.enterMultiplicativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpr" ):
                listener.exitMultiplicativeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)




    def multiplicativeExpr(self):

        localctx = dBaseParser.MultiplicativeExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 102, self.RULE_multiplicativeExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 451
            self.postfixExpr()
            self.state = 456
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==50 or _la==51:
                self.state = 452
                _la = self._input.LA(1)
                if not(_la==50 or _la==51):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 453
                self.postfixExpr()
                self.state = 458
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def primary(self):
            return self.getTypedRuleContext(dBaseParser.PrimaryContext,0)


        def LPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.LPAREN)
            else:
                return self.getToken(dBaseParser.LPAREN, i)

        def RPAREN(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.RPAREN)
            else:
                return self.getToken(dBaseParser.RPAREN, i)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DOT)
            else:
                return self.getToken(dBaseParser.DOT, i)

        def DCOLON(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DCOLON)
            else:
                return self.getToken(dBaseParser.DCOLON, i)

        def argList(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(dBaseParser.ArgListContext)
            else:
                return self.getTypedRuleContext(dBaseParser.ArgListContext,i)


        def getRuleIndex(self):
            return dBaseParser.RULE_postfixExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixExpr" ):
                listener.enterPostfixExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixExpr" ):
                listener.exitPostfixExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixExpr" ):
                return visitor.visitPostfixExpr(self)
            else:
                return visitor.visitChildren(self)




    def postfixExpr(self):

        localctx = dBaseParser.PostfixExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 104, self.RULE_postfixExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 459
            self.primary()
            self.state = 469
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,45,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 467
                    self._errHandler.sync(self)
                    token = self._input.LA(1)
                    if token in [46]:
                        self.state = 460
                        self.match(dBaseParser.LPAREN)
                        self.state = 462
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3715540181586182144) != 0):
                            self.state = 461
                            self.argList()


                        self.state = 464
                        self.match(dBaseParser.RPAREN)
                        pass
                    elif token in [33, 43]:
                        self.state = 465
                        _la = self._input.LA(1)
                        if not(_la==33 or _la==43):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 466
                        self.match(dBaseParser.IDENT)
                        pass
                    else:
                        raise NoViableAltException(self)
             
                self.state = 471
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,45,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PostfixSuffixContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOT(self):
            return self.getToken(dBaseParser.DOT, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def argList(self):
            return self.getTypedRuleContext(dBaseParser.ArgListContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_postfixSuffix

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixSuffix" ):
                listener.enterPostfixSuffix(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixSuffix" ):
                listener.exitPostfixSuffix(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixSuffix" ):
                return visitor.visitPostfixSuffix(self)
            else:
                return visitor.visitChildren(self)




    def postfixSuffix(self):

        localctx = dBaseParser.PostfixSuffixContext(self, self._ctx, self.state)
        self.enterRule(localctx, 106, self.RULE_postfixSuffix)
        self._la = 0 # Token type
        try:
            self.state = 479
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 472
                self.match(dBaseParser.DOT)
                self.state = 473
                self.match(dBaseParser.IDENT)
                pass
            elif token in [46]:
                self.enterOuterAlt(localctx, 2)
                self.state = 474
                self.match(dBaseParser.LPAREN)
                self.state = 476
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3715540181586182144) != 0):
                    self.state = 475
                    self.argList()


                self.state = 478
                self.match(dBaseParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NewExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEW(self):
            return self.getToken(dBaseParser.NEW, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def argList(self):
            return self.getTypedRuleContext(dBaseParser.ArgListContext,0)


        def getRuleIndex(self):
            return dBaseParser.RULE_newExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNewExpr" ):
                listener.enterNewExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNewExpr" ):
                listener.exitNewExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNewExpr" ):
                return visitor.visitNewExpr(self)
            else:
                return visitor.visitChildren(self)




    def newExpr(self):

        localctx = dBaseParser.NewExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 108, self.RULE_newExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 481
            self.match(dBaseParser.NEW)
            self.state = 482
            self.match(dBaseParser.IDENT)
            self.state = 483
            self.match(dBaseParser.LPAREN)
            self.state = 485
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 3715540181586182144) != 0):
                self.state = 484
                self.argList()


            self.state = 487
            self.match(dBaseParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MemberExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def THIS(self):
            return self.getToken(dBaseParser.THIS, 0)

        def IDENT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.IDENT)
            else:
                return self.getToken(dBaseParser.IDENT, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DOT)
            else:
                return self.getToken(dBaseParser.DOT, i)

        def DCOLON(self, i:int=None):
            if i is None:
                return self.getTokens(dBaseParser.DCOLON)
            else:
                return self.getToken(dBaseParser.DCOLON, i)

        def getRuleIndex(self):
            return dBaseParser.RULE_memberExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberExpr" ):
                listener.enterMemberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberExpr" ):
                listener.exitMemberExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberExpr" ):
                return visitor.visitMemberExpr(self)
            else:
                return visitor.visitChildren(self)




    def memberExpr(self):

        localctx = dBaseParser.MemberExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 110, self.RULE_memberExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 489
            _la = self._input.LA(1)
            if not(_la==21 or _la==61):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 494
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,49,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 490
                    _la = self._input.LA(1)
                    if not(_la==33 or _la==43):
                        self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 491
                    self.match(dBaseParser.IDENT) 
                self.state = 496
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,49,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(dBaseParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(dBaseParser.STRING, 0)

        def TRUE(self):
            return self.getToken(dBaseParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(dBaseParser.FALSE, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = dBaseParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 112, self.RULE_literal)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 497
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 216172885192998912) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def handlerList(self):
            return self.getTypedRuleContext(dBaseParser.HandlerListContext,0)


        def newExpr(self):
            return self.getTypedRuleContext(dBaseParser.NewExprContext,0)


        def memberExpr(self):
            return self.getTypedRuleContext(dBaseParser.MemberExprContext,0)


        def literal(self):
            return self.getTypedRuleContext(dBaseParser.LiteralContext,0)


        def THIS(self):
            return self.getToken(dBaseParser.THIS, 0)

        def SUPER(self):
            return self.getToken(dBaseParser.SUPER, 0)

        def FLOAT(self):
            return self.getToken(dBaseParser.FLOAT, 0)

        def NUMBER(self):
            return self.getToken(dBaseParser.NUMBER, 0)

        def IDENT(self):
            return self.getToken(dBaseParser.IDENT, 0)

        def STRING(self):
            return self.getToken(dBaseParser.STRING, 0)

        def BRACKET_STRING(self):
            return self.getToken(dBaseParser.BRACKET_STRING, 0)

        def LPAREN(self):
            return self.getToken(dBaseParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(dBaseParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(dBaseParser.RPAREN, 0)

        def getRuleIndex(self):
            return dBaseParser.RULE_primary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrimary" ):
                listener.enterPrimary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrimary" ):
                listener.exitPrimary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrimary" ):
                return visitor.visitPrimary(self)
            else:
                return visitor.visitChildren(self)




    def primary(self):

        localctx = dBaseParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 114, self.RULE_primary)
        try:
            self.state = 514
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,50,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 499
                self.handlerList()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 500
                self.newExpr()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 501
                self.memberExpr()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 502
                self.literal()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 503
                self.match(dBaseParser.THIS)
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 504
                self.match(dBaseParser.SUPER)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 505
                self.match(dBaseParser.FLOAT)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 506
                self.match(dBaseParser.NUMBER)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 507
                self.match(dBaseParser.IDENT)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 508
                self.match(dBaseParser.STRING)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 509
                self.match(dBaseParser.BRACKET_STRING)
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 510
                self.match(dBaseParser.LPAREN)
                self.state = 511
                self.expr()
                self.state = 512
                self.match(dBaseParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






# This class defines a complete listener for a parse tree produced by dBaseParser.
class dBaseParserListener(ParseTreeListener):

    # Enter a parse tree produced by dBaseParser#input.
    def enterInput(self, ctx:dBaseParser.InputContext):
        pass

    # Exit a parse tree produced by dBaseParser#input.
    def exitInput(self, ctx:dBaseParser.InputContext):
        pass


    # Enter a parse tree produced by dBaseParser#item.
    def enterItem(self, ctx:dBaseParser.ItemContext):
        pass

    # Exit a parse tree produced by dBaseParser#item.
    def exitItem(self, ctx:dBaseParser.ItemContext):
        pass


    # Enter a parse tree produced by dBaseParser#statement.
    def enterStatement(self, ctx:dBaseParser.StatementContext):
        pass

    # Exit a parse tree produced by dBaseParser#statement.
    def exitStatement(self, ctx:dBaseParser.StatementContext):
        pass


    # Enter a parse tree produced by dBaseParser#createFileStmt.
    def enterCreateFileStmt(self, ctx:dBaseParser.CreateFileStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#createFileStmt.
    def exitCreateFileStmt(self, ctx:dBaseParser.CreateFileStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#handlerList.
    def enterHandlerList(self, ctx:dBaseParser.HandlerListContext):
        pass

    # Exit a parse tree produced by dBaseParser#handlerList.
    def exitHandlerList(self, ctx:dBaseParser.HandlerListContext):
        pass


    # Enter a parse tree produced by dBaseParser#breakStmt.
    def enterBreakStmt(self, ctx:dBaseParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#breakStmt.
    def exitBreakStmt(self, ctx:dBaseParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#returnStmt.
    def enterReturnStmt(self, ctx:dBaseParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#returnStmt.
    def exitReturnStmt(self, ctx:dBaseParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#doStmt.
    def enterDoStmt(self, ctx:dBaseParser.DoStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#doStmt.
    def exitDoStmt(self, ctx:dBaseParser.DoStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#doTarget.
    def enterDoTarget(self, ctx:dBaseParser.DoTargetContext):
        pass

    # Exit a parse tree produced by dBaseParser#doTarget.
    def exitDoTarget(self, ctx:dBaseParser.DoTargetContext):
        pass


    # Enter a parse tree produced by dBaseParser#programRef.
    def enterProgramRef(self, ctx:dBaseParser.ProgramRefContext):
        pass

    # Exit a parse tree produced by dBaseParser#programRef.
    def exitProgramRef(self, ctx:dBaseParser.ProgramRefContext):
        pass


    # Enter a parse tree produced by dBaseParser#parameterStmt.
    def enterParameterStmt(self, ctx:dBaseParser.ParameterStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#parameterStmt.
    def exitParameterStmt(self, ctx:dBaseParser.ParameterStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#paramNames.
    def enterParamNames(self, ctx:dBaseParser.ParamNamesContext):
        pass

    # Exit a parse tree produced by dBaseParser#paramNames.
    def exitParamNames(self, ctx:dBaseParser.ParamNamesContext):
        pass


    # Enter a parse tree produced by dBaseParser#callExpr.
    def enterCallExpr(self, ctx:dBaseParser.CallExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#callExpr.
    def exitCallExpr(self, ctx:dBaseParser.CallExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:dBaseParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by dBaseParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:dBaseParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by dBaseParser#condition.
    def enterCondition(self, ctx:dBaseParser.ConditionContext):
        pass

    # Exit a parse tree produced by dBaseParser#condition.
    def exitCondition(self, ctx:dBaseParser.ConditionContext):
        pass


    # Enter a parse tree produced by dBaseParser#logicalOr.
    def enterLogicalOr(self, ctx:dBaseParser.LogicalOrContext):
        pass

    # Exit a parse tree produced by dBaseParser#logicalOr.
    def exitLogicalOr(self, ctx:dBaseParser.LogicalOrContext):
        pass


    # Enter a parse tree produced by dBaseParser#logicalAnd.
    def enterLogicalAnd(self, ctx:dBaseParser.LogicalAndContext):
        pass

    # Exit a parse tree produced by dBaseParser#logicalAnd.
    def exitLogicalAnd(self, ctx:dBaseParser.LogicalAndContext):
        pass


    # Enter a parse tree produced by dBaseParser#logicalNot.
    def enterLogicalNot(self, ctx:dBaseParser.LogicalNotContext):
        pass

    # Exit a parse tree produced by dBaseParser#logicalNot.
    def exitLogicalNot(self, ctx:dBaseParser.LogicalNotContext):
        pass


    # Enter a parse tree produced by dBaseParser#comparison.
    def enterComparison(self, ctx:dBaseParser.ComparisonContext):
        pass

    # Exit a parse tree produced by dBaseParser#comparison.
    def exitComparison(self, ctx:dBaseParser.ComparisonContext):
        pass


    # Enter a parse tree produced by dBaseParser#compareOp.
    def enterCompareOp(self, ctx:dBaseParser.CompareOpContext):
        pass

    # Exit a parse tree produced by dBaseParser#compareOp.
    def exitCompareOp(self, ctx:dBaseParser.CompareOpContext):
        pass


    # Enter a parse tree produced by dBaseParser#localDeclStmt.
    def enterLocalDeclStmt(self, ctx:dBaseParser.LocalDeclStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#localDeclStmt.
    def exitLocalDeclStmt(self, ctx:dBaseParser.LocalDeclStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#localAssignStmt.
    def enterLocalAssignStmt(self, ctx:dBaseParser.LocalAssignStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#localAssignStmt.
    def exitLocalAssignStmt(self, ctx:dBaseParser.LocalAssignStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#deleteStmt.
    def enterDeleteStmt(self, ctx:dBaseParser.DeleteStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#deleteStmt.
    def exitDeleteStmt(self, ctx:dBaseParser.DeleteStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#forStmt.
    def enterForStmt(self, ctx:dBaseParser.ForStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#forStmt.
    def exitForStmt(self, ctx:dBaseParser.ForStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#numberExpr.
    def enterNumberExpr(self, ctx:dBaseParser.NumberExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#numberExpr.
    def exitNumberExpr(self, ctx:dBaseParser.NumberExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#assignStmt.
    def enterAssignStmt(self, ctx:dBaseParser.AssignStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#assignStmt.
    def exitAssignStmt(self, ctx:dBaseParser.AssignStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#lvalue.
    def enterLvalue(self, ctx:dBaseParser.LvalueContext):
        pass

    # Exit a parse tree produced by dBaseParser#lvalue.
    def exitLvalue(self, ctx:dBaseParser.LvalueContext):
        pass


    # Enter a parse tree produced by dBaseParser#dottedRef.
    def enterDottedRef(self, ctx:dBaseParser.DottedRefContext):
        pass

    # Exit a parse tree produced by dBaseParser#dottedRef.
    def exitDottedRef(self, ctx:dBaseParser.DottedRefContext):
        pass


    # Enter a parse tree produced by dBaseParser#exprStmt.
    def enterExprStmt(self, ctx:dBaseParser.ExprStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#exprStmt.
    def exitExprStmt(self, ctx:dBaseParser.ExprStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#ifStmt.
    def enterIfStmt(self, ctx:dBaseParser.IfStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#ifStmt.
    def exitIfStmt(self, ctx:dBaseParser.IfStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#block.
    def enterBlock(self, ctx:dBaseParser.BlockContext):
        pass

    # Exit a parse tree produced by dBaseParser#block.
    def exitBlock(self, ctx:dBaseParser.BlockContext):
        pass


    # Enter a parse tree produced by dBaseParser#writeStmt.
    def enterWriteStmt(self, ctx:dBaseParser.WriteStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#writeStmt.
    def exitWriteStmt(self, ctx:dBaseParser.WriteStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#writeArg.
    def enterWriteArg(self, ctx:dBaseParser.WriteArgContext):
        pass

    # Exit a parse tree produced by dBaseParser#writeArg.
    def exitWriteArg(self, ctx:dBaseParser.WriteArgContext):
        pass


    # Enter a parse tree produced by dBaseParser#classDecl.
    def enterClassDecl(self, ctx:dBaseParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by dBaseParser#classDecl.
    def exitClassDecl(self, ctx:dBaseParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by dBaseParser#classBody.
    def enterClassBody(self, ctx:dBaseParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by dBaseParser#classBody.
    def exitClassBody(self, ctx:dBaseParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by dBaseParser#classMember.
    def enterClassMember(self, ctx:dBaseParser.ClassMemberContext):
        pass

    # Exit a parse tree produced by dBaseParser#classMember.
    def exitClassMember(self, ctx:dBaseParser.ClassMemberContext):
        pass


    # Enter a parse tree produced by dBaseParser#withStmt.
    def enterWithStmt(self, ctx:dBaseParser.WithStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#withStmt.
    def exitWithStmt(self, ctx:dBaseParser.WithStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#withTarget.
    def enterWithTarget(self, ctx:dBaseParser.WithTargetContext):
        pass

    # Exit a parse tree produced by dBaseParser#withTarget.
    def exitWithTarget(self, ctx:dBaseParser.WithTargetContext):
        pass


    # Enter a parse tree produced by dBaseParser#withBody.
    def enterWithBody(self, ctx:dBaseParser.WithBodyContext):
        pass

    # Exit a parse tree produced by dBaseParser#withBody.
    def exitWithBody(self, ctx:dBaseParser.WithBodyContext):
        pass


    # Enter a parse tree produced by dBaseParser#withAssignStmt.
    def enterWithAssignStmt(self, ctx:dBaseParser.WithAssignStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#withAssignStmt.
    def exitWithAssignStmt(self, ctx:dBaseParser.WithAssignStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#withLvalue.
    def enterWithLvalue(self, ctx:dBaseParser.WithLvalueContext):
        pass

    # Exit a parse tree produced by dBaseParser#withLvalue.
    def exitWithLvalue(self, ctx:dBaseParser.WithLvalueContext):
        pass


    # Enter a parse tree produced by dBaseParser#propertyDecl.
    def enterPropertyDecl(self, ctx:dBaseParser.PropertyDeclContext):
        pass

    # Exit a parse tree produced by dBaseParser#propertyDecl.
    def exitPropertyDecl(self, ctx:dBaseParser.PropertyDeclContext):
        pass


    # Enter a parse tree produced by dBaseParser#methodDecl.
    def enterMethodDecl(self, ctx:dBaseParser.MethodDeclContext):
        pass

    # Exit a parse tree produced by dBaseParser#methodDecl.
    def exitMethodDecl(self, ctx:dBaseParser.MethodDeclContext):
        pass


    # Enter a parse tree produced by dBaseParser#paramList.
    def enterParamList(self, ctx:dBaseParser.ParamListContext):
        pass

    # Exit a parse tree produced by dBaseParser#paramList.
    def exitParamList(self, ctx:dBaseParser.ParamListContext):
        pass


    # Enter a parse tree produced by dBaseParser#callStmt.
    def enterCallStmt(self, ctx:dBaseParser.CallStmtContext):
        pass

    # Exit a parse tree produced by dBaseParser#callStmt.
    def exitCallStmt(self, ctx:dBaseParser.CallStmtContext):
        pass


    # Enter a parse tree produced by dBaseParser#callTarget.
    def enterCallTarget(self, ctx:dBaseParser.CallTargetContext):
        pass

    # Exit a parse tree produced by dBaseParser#callTarget.
    def exitCallTarget(self, ctx:dBaseParser.CallTargetContext):
        pass


    # Enter a parse tree produced by dBaseParser#qualifiedName.
    def enterQualifiedName(self, ctx:dBaseParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by dBaseParser#qualifiedName.
    def exitQualifiedName(self, ctx:dBaseParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by dBaseParser#argList.
    def enterArgList(self, ctx:dBaseParser.ArgListContext):
        pass

    # Exit a parse tree produced by dBaseParser#argList.
    def exitArgList(self, ctx:dBaseParser.ArgListContext):
        pass


    # Enter a parse tree produced by dBaseParser#identifier.
    def enterIdentifier(self, ctx:dBaseParser.IdentifierContext):
        pass

    # Exit a parse tree produced by dBaseParser#identifier.
    def exitIdentifier(self, ctx:dBaseParser.IdentifierContext):
        pass


    # Enter a parse tree produced by dBaseParser#expr.
    def enterExpr(self, ctx:dBaseParser.ExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#expr.
    def exitExpr(self, ctx:dBaseParser.ExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:dBaseParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:dBaseParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#multiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:dBaseParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#multiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:dBaseParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#postfixExpr.
    def enterPostfixExpr(self, ctx:dBaseParser.PostfixExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#postfixExpr.
    def exitPostfixExpr(self, ctx:dBaseParser.PostfixExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#postfixSuffix.
    def enterPostfixSuffix(self, ctx:dBaseParser.PostfixSuffixContext):
        pass

    # Exit a parse tree produced by dBaseParser#postfixSuffix.
    def exitPostfixSuffix(self, ctx:dBaseParser.PostfixSuffixContext):
        pass


    # Enter a parse tree produced by dBaseParser#newExpr.
    def enterNewExpr(self, ctx:dBaseParser.NewExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#newExpr.
    def exitNewExpr(self, ctx:dBaseParser.NewExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#memberExpr.
    def enterMemberExpr(self, ctx:dBaseParser.MemberExprContext):
        pass

    # Exit a parse tree produced by dBaseParser#memberExpr.
    def exitMemberExpr(self, ctx:dBaseParser.MemberExprContext):
        pass


    # Enter a parse tree produced by dBaseParser#literal.
    def enterLiteral(self, ctx:dBaseParser.LiteralContext):
        pass

    # Exit a parse tree produced by dBaseParser#literal.
    def exitLiteral(self, ctx:dBaseParser.LiteralContext):
        pass


    # Enter a parse tree produced by dBaseParser#primary.
    def enterPrimary(self, ctx:dBaseParser.PrimaryContext):
        pass

    # Exit a parse tree produced by dBaseParser#primary.
    def exitPrimary(self, ctx:dBaseParser.PrimaryContext):
        pass



# This class defines a complete generic visitor for a parse tree produced by dBaseParser.

class dBaseParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by dBaseParser#input.
    def visitInput(self, ctx:dBaseParser.InputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#item.
    def visitItem(self, ctx:dBaseParser.ItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#statement.
    def visitStatement(self, ctx:dBaseParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#createFileStmt.
    def visitCreateFileStmt(self, ctx:dBaseParser.CreateFileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#handlerList.
    def visitHandlerList(self, ctx:dBaseParser.HandlerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#breakStmt.
    def visitBreakStmt(self, ctx:dBaseParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#returnStmt.
    def visitReturnStmt(self, ctx:dBaseParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#doStmt.
    def visitDoStmt(self, ctx:dBaseParser.DoStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#doTarget.
    def visitDoTarget(self, ctx:dBaseParser.DoTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#programRef.
    def visitProgramRef(self, ctx:dBaseParser.ProgramRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#parameterStmt.
    def visitParameterStmt(self, ctx:dBaseParser.ParameterStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#paramNames.
    def visitParamNames(self, ctx:dBaseParser.ParamNamesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#callExpr.
    def visitCallExpr(self, ctx:dBaseParser.CallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:dBaseParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#condition.
    def visitCondition(self, ctx:dBaseParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#logicalOr.
    def visitLogicalOr(self, ctx:dBaseParser.LogicalOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#logicalAnd.
    def visitLogicalAnd(self, ctx:dBaseParser.LogicalAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#logicalNot.
    def visitLogicalNot(self, ctx:dBaseParser.LogicalNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#comparison.
    def visitComparison(self, ctx:dBaseParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#compareOp.
    def visitCompareOp(self, ctx:dBaseParser.CompareOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#localDeclStmt.
    def visitLocalDeclStmt(self, ctx:dBaseParser.LocalDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#localAssignStmt.
    def visitLocalAssignStmt(self, ctx:dBaseParser.LocalAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#deleteStmt.
    def visitDeleteStmt(self, ctx:dBaseParser.DeleteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#forStmt.
    def visitForStmt(self, ctx:dBaseParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#numberExpr.
    def visitNumberExpr(self, ctx:dBaseParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#assignStmt.
    def visitAssignStmt(self, ctx:dBaseParser.AssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#lvalue.
    def visitLvalue(self, ctx:dBaseParser.LvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#dottedRef.
    def visitDottedRef(self, ctx:dBaseParser.DottedRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#exprStmt.
    def visitExprStmt(self, ctx:dBaseParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#ifStmt.
    def visitIfStmt(self, ctx:dBaseParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#block.
    def visitBlock(self, ctx:dBaseParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#writeStmt.
    def visitWriteStmt(self, ctx:dBaseParser.WriteStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#writeArg.
    def visitWriteArg(self, ctx:dBaseParser.WriteArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#classDecl.
    def visitClassDecl(self, ctx:dBaseParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#classBody.
    def visitClassBody(self, ctx:dBaseParser.ClassBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#classMember.
    def visitClassMember(self, ctx:dBaseParser.ClassMemberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#withStmt.
    def visitWithStmt(self, ctx:dBaseParser.WithStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#withTarget.
    def visitWithTarget(self, ctx:dBaseParser.WithTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#withBody.
    def visitWithBody(self, ctx:dBaseParser.WithBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#withAssignStmt.
    def visitWithAssignStmt(self, ctx:dBaseParser.WithAssignStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#withLvalue.
    def visitWithLvalue(self, ctx:dBaseParser.WithLvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#propertyDecl.
    def visitPropertyDecl(self, ctx:dBaseParser.PropertyDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#methodDecl.
    def visitMethodDecl(self, ctx:dBaseParser.MethodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#paramList.
    def visitParamList(self, ctx:dBaseParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#callStmt.
    def visitCallStmt(self, ctx:dBaseParser.CallStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#callTarget.
    def visitCallTarget(self, ctx:dBaseParser.CallTargetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#qualifiedName.
    def visitQualifiedName(self, ctx:dBaseParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#argList.
    def visitArgList(self, ctx:dBaseParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#identifier.
    def visitIdentifier(self, ctx:dBaseParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#expr.
    def visitExpr(self, ctx:dBaseParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:dBaseParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#multiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:dBaseParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#postfixExpr.
    def visitPostfixExpr(self, ctx:dBaseParser.PostfixExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#postfixSuffix.
    def visitPostfixSuffix(self, ctx:dBaseParser.PostfixSuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#newExpr.
    def visitNewExpr(self, ctx:dBaseParser.NewExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#memberExpr.
    def visitMemberExpr(self, ctx:dBaseParser.MemberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#literal.
    def visitLiteral(self, ctx:dBaseParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dBaseParser#primary.
    def visitPrimary(self, ctx:dBaseParser.PrimaryContext):
        return self.visitChildren(ctx)



del dBaseParser

# -----------------------------------------------------------------------------
def create_backend_for_base(base_name: str, parent_backend=None):
    QtClass = NATIVE_BASES.get(base_name.upper())
    if QtClass is None:
        raise RuntimeError(f"Unbekannte native Basisklasse: {base_name}")
    return QtClass(parent_backend) if parent_backend is not None else QtClass()

def apply_property_to_qt(inst: Instance, prop: str, value: Any):
    if inst.backend is None:
        return
        
    p = prop.upper()
    s = str(value)
    
    # normalisiere Zahlen (dein Interpreter nutzt evtl. float)
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    
    # Geometry: Qt braucht Left/Top/Width/Height gemeinsam
    if p in ("LEFT", "TOP", "WIDTH", "HEIGHT"):
        left   = int(inst.props.get("LEFT",    0) or   0)
        top    = int(inst.props.get("TOP",     0) or   0)
        width  = int(inst.props.get("WIDTH", 100) or 100)
        height = int(inst.props.get("HEIGHT",100) or 100)

        # update den einen Wert
        if p == "LEFT":   left   = int(value)
        if p == "TOP":    top    = int(value)
        if p == "WIDTH":  width  = int(value)
        if p == "HEIGHT": height = int(value)

        inst.props["LEFT"] = left
        inst.props["TOP"] = top
        inst.props["WIDTH"] = width
        inst.props["HEIGHT"] = height

        inst.backend.setGeometry(left, top, width, height)
        return
    
    # Text / Caption für Buttons
    if p in ("TEXT", "CAPTION"):
        if hasattr(inst.backend, "setText"):
            inst.backend.setText(s)
            return
        # Fenster/Dialog Titel
        if hasattr(inst.backend, "setWindowTitle"):
            inst.backend.setWindowTitle(s)
            return
    
    # optional: TITLE explizit
    if p == "TITLE":
        if hasattr(inst.backend, "setWindowTitle"):
            inst.backend.setWindowTitle(s)
        return
    
    # Font setzen
    if p == "FONT":
        if isinstance(value, FontValue):
            f = QFont(value.family, int(value.size))
            f.setBold(bool(value.bold))
            f.setItalic(bool(value.italic))
            f.setUnderline(bool(value.underline))
            if hasattr(inst.backend, "setFont"):
                inst.backend.setFont(f)
            return

def set_prop_runtime(inst: Instance, name: str, value: Any):
    inst.set_prop(name, value)
    apply_property_to_qt(inst, name, value)

def form_open(inst: Instance):
    if inst.backend is None:
        return
    modal = bool(inst.props.get("modal", False))

    # QDialog
    if hasattr(inst.backend, "show"):
        if modal:
            if hasattr(inst.backend, "show"):
                inst.backend.setModal(False)
                inst.backend.setWindowModality(Qt.NonModal) 
                sub = MAINAPP.mdi.addSubWindow(inst.backend)
                sub.resize(360,400)
                sub.show()
            else:
                inst.backend.setModal(False)
                inst.backend.setWindowModality(Qt.NonModal) 
                sub = MAINAPP.mdi.addSubWindow(inst.backend)
                sub.resize(360,400)
                sub.show()
        else:
            # todo: remove 2 lines below
            if hasattr(inst.backend, "show"):
                inst.backend.setModal(False)
                inst.backend.setWindowModality(Qt.NonModal) 
                sub = MAINAPP.mdi.addSubWindow(inst.backend)
                sub.resize(360,400)
                sub.show()
                
            #inst.backend.show()
        return

    # QWidget
    # todo: remove 2 lines below
    if hasattr(inst.backend, "show"):
        inst.backend.setModal(False)
        sub = MAINAPP.mdi.addSubWindow(inst.backend)
        sub.resize(360,400)
        sub.show()
        
    #inst.backend.show()

class Preprocessor:
    include_re = re.compile(r'^\s*#include\s+"([^"]+)"\s*$')
    define_re  = re.compile(r'^\s*#define\s+([A-Za-z_]\w*)(.*)\s*$')
    ifdef_re   = re.compile(r'^\s*#ifdef\s+([A-Za-z_]\w*)\s*$')
    ifndef_re  = re.compile(r'^\s*#ifndef\s+([A-Za-z_]\w*)\s*$')
    else_re    = re.compile(r'^\s*#else\s*$')
    endif_re   = re.compile(r'^\s*#endif\s*$')

    def __init__(self, *, include_paths: list[Path] | None = None):
        self.include_paths = include_paths or []
        self.macros: dict[str, Macro] = {}
        self.defined: set[str] = set()
        self._include_stack: list[Path] = []

    def _split_args(self, s: str) -> list[str]:
        # s ist Inhalt zwischen den äußeren (...) eines Calls
        args = []
        cur = []
        depth = 0
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == "(":
                depth += 1
                cur.append(ch)
            elif ch == ")":
                depth -= 1
                cur.append(ch)
            elif ch == "," and depth == 0:
                args.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
            i += 1
        if cur or s.strip() == "":
            args.append("".join(cur).strip())
        return args

    def _stringize(self, arg_text: str) -> str:
        # Whitespace normalisieren wie C-ish
        norm = " ".join(arg_text.split())
        norm = norm.replace("\\", "\\\\").replace('"', '\\"')
        return f"\"{norm}\""

    def _expand_function_macro(self, macro: Macro, call_args: list[str]) -> str:
        if macro.params is None:
            raise PreprocessorError("internal: not a function macro")

        if len(call_args) != len(macro.params):
            raise PreprocessorError(
                f"macro {macro.name} expects {len(macro.params)} args, got {len(call_args)}"
            )

        argmap = dict(zip(macro.params, call_args))

        # body als Arbeitsstring
        body = macro.body

        # 1) stringize: #param  (nur wenn param direkt folgt)
        #    Beispiel: #x
        for p in macro.params:
            body = re.sub(rf'#\s*{re.escape(p)}\b',
                          lambda m, p=p: self._stringize(argmap[p]),
                          body)

        # 2) token paste: a ## b  (pragmatisch: Strings zusammenkleben)
        #    Wir machen das iterativ, solange es '##' gibt.
        #    Dabei erlauben wir links/rechts: param oder direktes Wort/Token
        while "##" in body:
            m = re.search(r'(\S+)\s*##\s*(\S+)', body)
            if not m:
                break
            left = m.group(1)
            right = m.group(2)

            # param ersetzen, falls es param ist
            left_val = argmap.get(left, left)
            right_val = argmap.get(right, right)

            # Wenn left_val ein Stringliteral ist ("..."), quotes entfernen und concat
            if left_val.startswith('"') and left_val.endswith('"'):
                left_inner = left_val[1:-1]
                # right_val: wenn auch string, ohne quotes
                if right_val.startswith('"') and right_val.endswith('"'):
                    right_part = right_val[1:-1]
                else:
                    right_part = right_val
                glued = f"\"{left_inner}{right_part}\""
            else:
                glued = f"{left_val}{right_val}"

            body = body[:m.start()] + glued + body[m.end():]

        # 3) normale param substitution (für verbleibende params im body)
        for p in macro.params:
            body = re.sub(rf'\b{re.escape(p)}\b', argmap[p], body)

        return body

    def _expand_macros_in_line(self, line: str) -> str:
        # Sehr einfache, iterative Expansion (mit Limit gegen Endlosschleifen)
        out = line
        for _ in range(50):
            changed = False

            # 1) function-like macros: NAME(...)
            #    Suche NAME( ... ) und expandiere
            for name, macro in list(self.macros.items()):
                if macro.params is None:
                    continue

                # finde "name(" in der Zeile
                idx = out.find(name + "(")
                while idx != -1:
                    # parse bis passendes ')'
                    j = idx + len(name) + 1
                    depth = 1
                    while j < len(out) and depth > 0:
                        if out[j] == "(":
                            depth += 1
                        elif out[j] == ")":
                            depth -= 1
                        j += 1
                    if depth != 0:
                        # unbalanciert -> abbrechen
                        break

                    inside = out[idx + len(name) + 1 : j - 1]
                    args = self._split_args(inside)
                    repl = self._expand_function_macro(macro, args)

                    out = out[:idx] + repl + out[j:]
                    changed = True

                    idx = out.find(name + "(", idx + len(repl))
                # next macro

            # 2) object-like macros: \bNAME\b
            for name, macro in list(self.macros.items()):
                if macro.params is not None:
                    continue
                # ganzes Wort ersetzen
                new_out = re.sub(rf'\b{re.escape(name)}\b', macro.body, out)
                if new_out != out:
                    out = new_out
                    changed = True

            if not changed:
                break

        return out

    def process(self, filename: str | Path) -> str:
        #data = Path(filename).read_text(encoding="utf-8")
        #data = re.sub(r'(?i)\bNEW(?=[A-Za-z_])', 'NEW ', data)
        #data = re.sub(r'(?i)\bCALL(?=[A-Za-z_])', 'CALL ', data)
        #with open(filename,"w",encoding="utf-8") as f:
        #    f.write(data)
        #    f.close()
            
        entry = Path(filename).resolve()
        return self._process_file(entry)

    def _resolve_include(self, current_file: Path, name: str) -> Path:
        # 1) relativ zum aktuellen file
        cand = (current_file.parent / name).resolve()
        if cand.exists():
            return cand

        # 2) include_paths
        for base in self.include_paths:
            cand2 = (base / name).resolve()
            if cand2.exists():
                return cand2

        raise PreprocessorError(f'include file not found: "{name}" (from {current_file})')
        
    # Schneidet trailing Kommentare ab: &&, **, //, /* ...
    # (Nur bis Zeilenende; Blockkommentar-Mehrzeiligkeit ist für Direktiven egal,
    # weil nach der Direktive sowieso nichts mehr ausgewertet werden soll.)
    def _strip_trailing_comment(self, s: str) -> str:
        markers = ["&&", "**", "//", "/*"]
        cut = None
        for m in markers:
            pos = s.find(m)
            if pos != -1 and (cut is None or pos < cut):
                cut = pos
        return s if cut is None else s[:cut]
        
    def _process_file(self, path: Path) -> str:
        if path in self._include_stack:
            chain = " -> ".join(str(p) for p in self._include_stack + [path])
            raise PreprocessorError(f"circular include detected: {chain}")

        self._include_stack.append(path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            out_lines: list[str] = []
            frames: list[PPFrame] = [PPFrame(parent_active=True, this_active=True)]

            def active() -> bool:
                return frames[-1].parent_active and frames[-1].this_active

            lines = text.splitlines(keepends=True)
            for i, line in enumerate(lines, start=1):
                # Direktiven erkennen (immer), aber nur ausführen wenn "active"
                raw_line = line
                line = self._strip_trailing_comment(line).rstrip("\r\n")
                m = self.include_re.match(line)
                if m:
                    if active():
                        inc_name = m.group(1)
                        inc_path = self._resolve_include(path, inc_name)
                        out_lines.append(f'**line 1 "{inc_path}"*/\n')
                        out_lines.append(self._process_file(inc_path))
                        out_lines.append(f'**line {i+1} "{path}"*/\n')
                    continue
                    
                m = self.define_re.match(line)
                if m:
                    if active():
                        name = m.group(1)
                        tail = (m.group(2) or "").strip()

                        # function-like: direkt nach Name "("
                        if tail.startswith("("):
                            close = tail.find(")")
                            if close == -1:
                                raise PreprocessorError(f"{path}:{i}: malformed function-like #define")
                            params_part = tail[1:close].strip()
                            body = tail[close+1:].lstrip()

                            params = [p.strip() for p in params_part.split(",")] if params_part else []
                            self.macros[name] = Macro(name=name, params=params, body=body)
                        else:
                            self.macros[name] = Macro(name=name, params=None, body=tail)

                        self.defined.add(name)
                    continue
                
                m = self.ifdef_re.match(line)
                if m:
                    name = m.group(1)
                    parent = active()
                    cond = name in self.defined
                    frames.append(PPFrame(
                        parent_active=parent,
                        this_active=cond,
                        start_file=path,
                        start_line=i,
                        kind="#ifdef",
                        name=name
                    ))
                    continue

                m = self.ifndef_re.match(line)
                if m:
                    name = m.group(1)
                    parent = active()
                    cond = name not in self.defined
                    frames.append(PPFrame(
                        parent_active=parent,
                        this_active=cond,
                        start_file=path,
                        start_line=i,
                        kind="#ifndef",
                        name=name
                    ))
                    continue

                if self.else_re.match(line):
                    if len(frames) == 1:
                        raise PreprocessorError(f"{path}:{i}: #else without #if")
                    top = frames[-1]
                    if top.saw_else:
                        raise PreprocessorError(f"{path}:{i}: multiple #else")
                    top.saw_else = True
                    # else invertiert nur die "this_active" Ebene, parent bleibt gleich
                    top.this_active = not top.this_active
                    continue

                if self.endif_re.match(line):
                    if len(frames) == 1:
                        raise PreprocessorError(f"{path}:{i}: #endif without #if")
                    frames.pop()
                    continue

                # Normale Zeile: nur ausgeben wenn aktiv
                if active():
                     out_lines.append(self._expand_macros_in_line(raw_line))

            if len(frames) != 1:
                top = frames[-1]
                raise PreprocessorError(
                    f"{path}: EOF: missing #endif for {top.kind} {top.name} "
                    f"(opened at {top.start_file}:{top.start_line})"
                )
                
            return "".join(out_lines)
        finally:
            self._include_stack.pop()
            
class Symbols:
    def __init__(self) -> None:
        self.classes: Dict[str, object] = {}

    def has_class(self, name: str) -> bool:
        # dBase ist oft case-insensitive -> normalisieren:
        return name.upper() in self.classes

    def add_class(self, name: str, node: object) -> None:
        self.classes[name.upper()] = node

class SemanticVisitor(dBaseParserVisitor):
    def __init__(self):
        super().__init__()
        self.symbols = Symbols()
        self.classes = self.symbols.classes   # <- Alias
        self.errors: List[CompileError] = []
        self._current_class = None

    def error(self, ctx, msg: str):
        tok = ctx.start
        self.errors.append(CompileError(tok.line, tok.column, msg))
    
    def visitClassBody(self, ctx):
        # NUR member besuchen
        for m in ctx.classMember():
            self.visit(m)
        return None

def analyze(tree, parser):
    sema = SemanticVisitor()
    sema.visit(tree)

    if sema.errors:
        for e in sema.errors:
            print(f"{e.line}:{e.column}: error: {e.message}")
        raise SystemExit(1)

    return sema

class ScopeStack:
    def __init__(self):
        self._scopes = [{}]  # global scope

    def push(self):
        self._scopes.append({})

    def pop(self):
        if len(self._scopes) == 1:
            raise RuntimeError("Cannot pop global scope")
        self._scopes.pop()

    def set(self, name: str, value):
        self._scopes[-1][name] = value

    def get(self, name: str):
        for scope in reversed(self._scopes):
            if name in scope:
                return scope[name]
        raise KeyError(name)

    def has(self, name: str) -> bool:
        for scope in reversed(self._scopes):
            if name in scope:
                return True
        return False

# ---------------------------------------------------------------------------
# Ein EventFilter pro Widget-Instance.
# Ruft Wrapper-Funktionen auf, die du in inst.props hinterlegst.
# ---------------------------------------------------------------------------
class _QtEventFilter(QObject):
    def __init__(self, runner, inst):
        super().__init__()
        self.runner = runner
        self.inst = inst

    def eventFilter(self, obj, event):
        t = event.type()

        if t == QEvent.FocusIn:
            cb = self.inst.props.get("_ONFOCUSIN_WRAPPER")
            if cb:
                cb(event)

        elif t == QEvent.FocusOut:
            cb = self.inst.props.get("_ONFOCUSOUT_WRAPPER")
            if cb:
                cb(event)

        elif t == QEvent.MouseMove:
            cb = self.inst.props.get("_ONMOUSEMOVE_WRAPPER")
            if cb:
                cb(event)

        elif t == QEvent.MouseButtonPress:
            cb = self.inst.props.get("_ONMOUSEDOWN_WRAPPER")
            if cb:
                cb(event)

        elif t == QEvent.MouseButtonRelease:
            cb = self.inst.props.get("_ONMOUSEUP_WRAPPER")
            if cb:
                cb(event)

            # Rechts/Links-Button Events
            try:
                if event.button() == Qt.LeftButton:
                    cb = self.inst.props.get("_ONMOUSELBUTTON_WRAPPER")
                    if cb:
                        cb(event)

                    # Click-Fallback NUR links (und nur wenn nicht via Qt.clicked)
                    if not self.inst.props.get("_ONCLICK_VIA_SIGNAL"):
                        cb = self.inst.props.get("_ONCLICK_WRAPPER")
                        if cb:
                            cb(event)

                elif event.button() == Qt.RightButton:
                    # onClick darf hier NICHT laufen!
                    cb = self.inst.props.get("_ONMOUSERBUTTON_WRAPPER")
                    if cb:
                        cb(event)

            except Exception:
                pass
        
        elif t == QEvent.KeyPress:
            cb = self.inst.props.get("_ONKEYDOWN_WRAPPER")
            if cb:
                cb(event)

        elif t == QEvent.KeyRelease:
            cb = self.inst.props.get("_ONKEYUP_WRAPPER")
            if cb:
                cb(event)

        elif t == QEvent.MouseButtonDblClick:
            cb = self.inst.props.get("_ONDBLCLICK_WRAPPER")
            if cb:
                cb(event)

        return False

class RowMarkerProxy(QAbstractProxyModel):
    def __init__(self, source_model, parent=None):
        super().__init__(parent)
        self.setSourceModel(source_model)
        self._row = -1
        self._marker = "\u25BA"
        self._font = QFont("Arial", 12)

    # --- Pflicht-Forwarder ---
    def mapToSource(self, proxyIndex):
        return self.sourceModel().index(proxyIndex.row(), proxyIndex.column(), proxyIndex.parent())

    def mapFromSource(self, sourceIndex):
        return self.index(sourceIndex.row(), sourceIndex.column(), sourceIndex.parent())

    def index(self, row, column, parent=QModelIndex()):
        if self.hasIndex(row, column, parent):
            return self.createIndex(row, column)
        return QModelIndex()

    def parent(self, child):
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return self.sourceModel().rowCount(parent)

    def columnCount(self, parent=QModelIndex()):
        return self.sourceModel().columnCount(parent)

    def data(self, index, role=Qt.DisplayRole):
        return self.sourceModel().data(self.mapToSource(index), role)

    def setData(self, index, value, role=Qt.EditRole):
        return self.sourceModel().setData(self.mapToSource(index), value, role)

    def flags(self, index):
        return self.sourceModel().flags(self.mapToSource(index))

    # --- Hier passiert die Magie: Header links ---
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return "\u25BA" if section == self._row else ""
        return self.sourceModel().headerData(section, orientation, role)

    def setCurrentRow(self, row: int):
        if row == self._row:
            return
        old = self._row
        self._row = row
        # Nur alte + neue Zeile im Header neu zeichnen lassen
        if old >= 0:
            self.headerDataChanged.emit(Qt.Vertical, old, old)
        if row >= 0:
            self.headerDataChanged.emit(Qt.Vertical, row, row)

class GlossyPillButtonGreen(QPushButton):
    def __init__(self, text="Success", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self._hover = False
        self._pressed = False

        # Größe/Font
        f = self.font()
        f.setPointSize(10)
        f.setBold(True)
        self.setFont(f)
        
        self.setMinimumHeight(34)
        self.setMaximumHeight(34)
        self.setMinimumWidth(200)

        self.setAttribute(Qt.WA_Hover, True)

    # --- states ---
    def enterEvent(self, e):
        self._hover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover = False
        self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        sh = super().sizeHint()
        sh.setHeight(max(sh.height(), 56))
        sh.setWidth(max(sh.width() + 40, 220))
        return sh

    # --- painting ---
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        r = QRectF(self.rect()).adjusted(3, 3, -3, -3)

        # Pressed: "rein"
        y_offset = 2 if self._pressed else 0
        r = r.adjusted(0, y_offset, 0, y_offset)

        radius = r.height() / 2.0

        # Farb-Setup je nach State
        if self._pressed:
            base_mid  = QColor("#0f7a25")
            base_lit  = QColor("#1fb64a")
            base_dark = QColor("#084814")
            glow = 0.55
            depth = 1
        elif self._hover:
            base_mid  = QColor("#1bbb45")
            base_lit  = QColor("#7bff9a")
            base_dark = QColor("#0b5d1e")
            glow = 0.75
            depth = 3
        else:
            base_mid  = QColor("#16a83b")
            base_lit  = QColor("#67f38a")
            base_dark = QColor("#0b5d1e")
            glow = 0.70
            depth = 3

        # Schatten (unter dem Button)
        if not self._pressed:
            shadow_r = QRectF(r).translated(0, 4)   # statt QRect
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(shadow_r, radius, radius)
            p.fillPath(shadow_path, QColor(0, 0, 0, 60))

        # Button-Form
        path = QPainterPath()
        path.addRoundedRect(r, radius, radius)

        # Hauptverlauf horizontal: links/rechts "shine"
        grad = QLinearGradient(r.left(), r.center().y(), r.right(), r.center().y())
        grad.setColorAt(0.00, base_lit)
        grad.setColorAt(0.08, base_mid.lighter(115))
        grad.setColorAt(0.50, base_mid)
        grad.setColorAt(0.92, base_mid.lighter(115))
        grad.setColorAt(1.00, base_lit)

        p.fillPath(path, grad)

        # Innenkante / 3D-Rand
        pen = QPen(base_dark.darker(120))
        pen.setWidth(2)
        p.setPen(pen)
        p.drawPath(path)

        # “Depth lip” unten (dicke Unterkante)
        if depth > 0:
            lip_r = QRectF(r)
            lip_r.setTop(lip_r.top() + r.height() * 0.55)
            lip_path = QPainterPath()
            lip_path.addRoundedRect(lip_r, radius, radius)
            p.fillPath(lip_path, QColor(base_dark.red(), base_dark.green(), base_dark.blue(), 90))

        # Gloss oben (vertikaler Glanz)
        gloss_r = QRectF(r)
        gloss_r.setHeight(r.height() * 0.55)

        gloss_path = QPainterPath()
        gloss_path.addRoundedRect(gloss_r, radius, radius)

        gloss_grad = QLinearGradient(gloss_r.left(), gloss_r.top(), gloss_r.left(), gloss_r.bottom())
        gloss_grad.setColorAt(0.0, QColor(255, 255, 255, int(180 * glow)))
        gloss_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(gloss_path, gloss_grad)

        # Side highlights (radial “spots” links/rechts)
        spot_alpha = 120 if (self._hover and not self._pressed) else 90
        if self._pressed:
            spot_alpha = 60

        # Links
        left_center = QPointF(r.left() + r.height() * 0.40, r.top() + r.height() * 0.28)
        left_spot = QRadialGradient(left_center, r.height() * 0.55)
        left_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        left_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, left_spot)

        # Rechts
        right_center = QPointF(r.right() - r.height() * 0.40, r.top() + r.height() * 0.28)
        right_spot = QRadialGradient(right_center, r.height() * 0.55)
        right_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        right_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, right_spot)

        # Text (mit leichter Schattenkante)
        text_rect = r.toRect()
        p.setPen(QColor(0, 0, 0, 110))
        p.drawText(text_rect.translated(0, 1), Qt.AlignCenter, self.text())

        p.setPen(QColor(255, 255, 255))
        p.drawText(text_rect, Qt.AlignCenter, self.text())

class GlossyPillButtonBlue(QPushButton):
    def __init__(self, text="Success", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self._hover = False
        self._pressed = False

        # Größe/Font
        f = self.font()
        f.setPointSize(10)
        f.setBold(True)
        self.setFont(f)
        self.setMinimumHeight(34)
        self.setMaximumHeight(34)
        self.setMinimumWidth(220)

        self.setAttribute(Qt.WA_Hover, True)

    # --- states ---
    def enterEvent(self, e):
        self._hover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover = False
        self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        sh = super().sizeHint()
        sh.setHeight(max(sh.height(), 56))
        sh.setWidth(max(sh.width() + 40, 220))
        return sh

    # --- painting ---
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        r = QRectF(self.rect()).adjusted(3, 3, -3, -3)

        # Pressed: "rein"
        y_offset = 2 if self._pressed else 0
        r = r.adjusted(0, y_offset, 0, y_offset)

        radius = r.height() / 2.0

        # Farb-Setup je nach State
        if self._pressed:
            base_mid  = QColor("#0b4fb3")  # deep blue
            base_lit  = QColor("#2f74ff")  # bright
            base_dark = QColor("#07306b")  # shadow
            glow = 0.55
            depth = 1
        elif self._hover:
            base_mid  = QColor("#1b66ff")
            base_lit  = QColor("#7fb0ff")
            base_dark = QColor("#0a3a8c")
            glow = 0.75
            depth = 3
        else:
            base_mid  = QColor("#155ee6")
            base_lit  = QColor("#5fa0ff")
            base_dark = QColor("#0a3a8c")
            glow = 0.70
            depth = 3

        # Schatten (unter dem Button)
        if not self._pressed:
            shadow_r = QRectF(r).translated(0, 4)   # statt QRect
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(shadow_r, radius, radius)
            p.fillPath(shadow_path, QColor(0, 0, 0, 60))

        # Button-Form
        path = QPainterPath()
        path.addRoundedRect(r, radius, radius)

        # Hauptverlauf horizontal: links/rechts "shine"
        grad = QLinearGradient(r.left(), r.center().y(), r.right(), r.center().y())
        grad.setColorAt(0.00, base_lit)
        grad.setColorAt(0.08, base_mid.lighter(115))
        grad.setColorAt(0.50, base_mid)
        grad.setColorAt(0.92, base_mid.lighter(115))
        grad.setColorAt(1.00, base_lit)

        p.fillPath(path, grad)

        # Innenkante / 3D-Rand
        pen = QPen(base_dark.darker(120))
        pen.setWidth(2)
        p.setPen(pen)
        p.drawPath(path)

        # “Depth lip” unten (dicke Unterkante)
        if depth > 0:
            lip_r = QRectF(r)
            lip_r.setTop(lip_r.top() + r.height() * 0.55)
            lip_path = QPainterPath()
            lip_path.addRoundedRect(lip_r, radius, radius)
            p.fillPath(lip_path, QColor(base_dark.red(), base_dark.green(), base_dark.blue(), 90))

        # Gloss oben (vertikaler Glanz)
        gloss_r = QRectF(r)
        gloss_r.setHeight(r.height() * 0.55)

        gloss_path = QPainterPath()
        gloss_path.addRoundedRect(gloss_r, radius, radius)

        gloss_grad = QLinearGradient(gloss_r.left(), gloss_r.top(), gloss_r.left(), gloss_r.bottom())
        gloss_grad.setColorAt(0.0, QColor(255, 255, 255, int(180 * glow)))
        gloss_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(gloss_path, gloss_grad)

        # Side highlights (radial “spots” links/rechts)
        spot_alpha = 120 if (self._hover and not self._pressed) else 90
        if self._pressed:
            spot_alpha = 60

        # Links
        left_center = QPointF(r.left() + r.height() * 0.40, r.top() + r.height() * 0.28)
        left_spot = QRadialGradient(left_center, r.height() * 0.55)
        left_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        left_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, left_spot)

        # Rechts
        right_center = QPointF(r.right() - r.height() * 0.40, r.top() + r.height() * 0.28)
        right_spot = QRadialGradient(right_center, r.height() * 0.55)
        right_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        right_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, right_spot)

        # Text (mit leichter Schattenkante)
        text_rect = r.toRect()
        p.setPen(QColor(0, 0, 0, 110))
        p.drawText(text_rect.translated(0, 1), Qt.AlignCenter, self.text())

        p.setPen(QColor(255, 255, 255))
        p.drawText(text_rect, Qt.AlignCenter, self.text())

class GlossyPillButtonGold(QPushButton):
    def __init__(self, text="Success", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self._hover = False
        self._pressed = False

        # Größe/Font
        f = self.font()
        f.setPointSize(10)
        f.setBold(True)
        self.setFont(f)
        self.setMinimumHeight(34)
        self.setMaximumHeight(34)
        self.setMinimumWidth(220)

        self.setAttribute(Qt.WA_Hover, True)

    # --- states ---
    def enterEvent(self, e):
        self._hover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hover = False
        self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(e)

    def sizeHint(self):
        sh = super().sizeHint()
        sh.setHeight(max(sh.height(), 56))
        sh.setWidth(max(sh.width() + 40, 220))
        return sh

    # --- painting ---
    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        r = QRectF(self.rect()).adjusted(3, 3, -3, -3)

        # Pressed: "rein"
        y_offset = 2 if self._pressed else 0
        r = r.adjusted(0, y_offset, 0, y_offset)

        radius = r.height() / 2.0

        # Farb-Setup je nach State
        if self._pressed:
            base_mid  = QColor("#b8860b")   # dark gold
            base_lit  = QColor("#ffd24d")   # warm highlight
            base_dark = QColor("#7a5a00")   # deep shadow
            glow = 0.50
            depth = 1

        elif self._hover:
            base_mid  = QColor("#e6b422")   # rich gold
            base_lit  = QColor("#fff1a8")   # glossy shine
            base_dark = QColor("#9c7400")
            glow = 0.80
            depth = 3

        else:
            base_mid  = QColor("#d4a017")   # classic gold
            base_lit  = QColor("#ffe08a")   # soft gloss
            base_dark = QColor("#8a6a00")
            glow = 0.70
            depth = 3

        # Schatten (unter dem Button)
        if not self._pressed:
            shadow_r = QRectF(r).translated(0, 4)   # statt QRect
            shadow_path = QPainterPath()
            shadow_path.addRoundedRect(shadow_r, radius, radius)
            p.fillPath(shadow_path, QColor(0, 0, 0, 60))

        # Button-Form
        path = QPainterPath()
        path.addRoundedRect(r, radius, radius)

        # Hauptverlauf horizontal: links/rechts "shine"
        grad = QLinearGradient(r.left(), r.center().y(), r.right(), r.center().y())
        grad.setColorAt(0.00, base_lit)
        grad.setColorAt(0.08, base_mid.lighter(115))
        grad.setColorAt(0.50, base_mid)
        grad.setColorAt(0.92, base_mid.lighter(115))
        grad.setColorAt(1.00, base_lit)

        p.fillPath(path, grad)

        # Innenkante / 3D-Rand
        pen = QPen(base_dark.darker(120))
        pen.setWidth(2)
        p.setPen(pen)
        p.drawPath(path)

        # “Depth lip” unten (dicke Unterkante)
        if depth > 0:
            lip_r = QRectF(r)
            lip_r.setTop(lip_r.top() + r.height() * 0.55)
            lip_path = QPainterPath()
            lip_path.addRoundedRect(lip_r, radius, radius)
            p.fillPath(lip_path, QColor(base_dark.red(), base_dark.green(), base_dark.blue(), 90))

        # Gloss oben (vertikaler Glanz)
        gloss_r = QRectF(r)
        gloss_r.setHeight(r.height() * 0.55)

        gloss_path = QPainterPath()
        gloss_path.addRoundedRect(gloss_r, radius, radius)

        gloss_grad = QLinearGradient(gloss_r.left(), gloss_r.top(), gloss_r.left(), gloss_r.bottom())
        gloss_grad.setColorAt(0.0, QColor(255, 255, 255, int(180 * glow)))
        gloss_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(gloss_path, gloss_grad)

        # Side highlights (radial “spots” links/rechts)
        spot_alpha = 120 if (self._hover and not self._pressed) else 90
        if self._pressed:
            spot_alpha = 60

        # Links
        left_center = QPointF(r.left() + r.height() * 0.40, r.top() + r.height() * 0.28)
        left_spot = QRadialGradient(left_center, r.height() * 0.55)
        left_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        left_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, left_spot)

        # Rechts
        right_center = QPointF(r.right() - r.height() * 0.40, r.top() + r.height() * 0.28)
        right_spot = QRadialGradient(right_center, r.height() * 0.55)
        right_spot.setColorAt(0.0, QColor(255, 255, 255, spot_alpha))
        right_spot.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.fillPath(path, right_spot)

        # Text (mit leichter Schattenkante)
        text_rect = r.toRect()
        p.setPen(QColor(0, 0, 0, 110))
        p.drawText(text_rect.translated(0, 1), Qt.AlignCenter, self.text())

        p.setPen(QColor(245, 245, 245))
        p.drawText(text_rect, Qt.AlignCenter, self.text())

class PyEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("    " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class PasEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("  " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class CppEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("  " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class JavaEmitter:
    def __init__(self):
        self.lines = []
        self.level = 0

    def emit(self, line=""):
        self.lines.append(("  " * self.level) + line)

    def indent(self): self.level += 1
    def dedent(self): self.level = max(0, self.level - 1)

    def text(self):
        return "\n".join(self.lines) + "\n"

class DBaseToJava:
    def __init__(self, parser, classes=None, class_name="GenProg", package=None):
        self.p = parser
        self.out = JavaEmitter()
        self.classes = classes or {}
        self.class_name = class_name
        self.package = package
        self._tmp_i = 0

    def new_temp(self):
        self._tmp_i += 1
        return f"t{self._tmp_i}"

    def jstr(self, s: str) -> str:
        s = s.replace("\\", "\\\\").replace('"', '\\"')
        return f"\"{s}\""

    def jstr_list(self, items):
        # java.util.List.of("A","B")
        inner = ", ".join(self.jstr(x) for x in items)
        return f"java.util.List.of({inner})"

    def jval_list(self, exprs):
        # java.util.List.of(a, b, c)
        inner = ", ".join(exprs)
        return f"java.util.List.of({inner})"

    def generate(self, tree, out_path: str):
        o = self.out
        if self.package:
            o.emit(f"package {self.package};")
            o.emit("")
        o.emit("import java.util.*;")
        o.emit("")
        o.emit("public class " + self.class_name + " {")
        o.indent()
        o.emit("public static void main(String[] args) {")
        o.indent()
        o.emit("TRT rt = new TRT();")
        o.emit("try {")
        o.indent()

        self.gen_input(tree)

        o.dedent()
        o.emit("} catch (Exception e) {")
        o.indent()
        o.emit('System.err.println("ERROR: " + e.getMessage());')
        o.emit("e.printStackTrace();")
        o.dedent()
        o.emit("}")
        o.dedent()
        o.emit("}")
        o.dedent()
        o.emit("}")
        Path(out_path).write_text(o.text(), encoding="utf-8")

    # input : item* EOF
    def gen_input(self, ctx):
        for it in ctx.item():
            self.gen_item(it)

    # item : classDecl | methodDecl | statement
    def gen_item(self, it):
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            self.out.emit("// TODO classDecl not implemented in Java backend")
            return
        if it.methodDecl():
            self.out.emit("// TODO methodDecl not implemented in Java backend")
            return
        self.out.emit("// TODO unhandled item")

    # statement dispatcher (erweitern wie bei Python/Pascal)
    def gen_stmt(self, st):
        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())
        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        if st.exprStmt():          return self.gen_expr_stmt(st.exprStmt())

        self.out.emit("// TODO unhandled statement: " + type(st.getChild(0)).__name__)

    # writeStmt : WRITE writeArg (PLUS writeArg)* ;
    def gen_write(self, ctx):
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]
        if not parts:
            self.out.emit("rt.WRITE(TRT.Null());")
            return

        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, \"+\", {p})"
        self.out.emit(f"rt.WRITE({expr});")

    # writeArg : STRING | dottedRef | expr ;
    def gen_write_arg(self, actx):
        if actx.STRING():
            # actx.STRING().getText() liefert schon Anführungszeichen aus dem Lexer
            return f"TRT.V({actx.STRING().getText()})"
        if actx.dottedRef():
            base, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET('{base.upper()}', {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return "TRT.Null()"

    def gen_local_decl(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        self.out.emit(f"rt.SET_NAME({self.jstr(name)}, TRT.Null());")

    def gen_local_assign(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME({self.jstr(name)}, {rhs});")

    # lvalue : postfixExpr | dottedRef ;
    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        if lv.dottedRef():
            base, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)

            if len(chain) == 1:
                self.out.emit(f"rt.SET_NAME({self.jstr(chain[0])}, {rhs});")
                return

            head = chain[0]
            if head.upper() == "THIS":
                base = "rt.GET_THIS()"
                path = self.jstr_list(chain[1:])
            else:
                base = f"rt.GET_NAME({self.jstr(head)})"
                path = self.jstr_list(chain[1:])

            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        self.out.emit("// TODO unsupported lvalue: " + lv.getText())

    # ifStmt : IF expr block (ELSE block)? ENDIF ;
    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if (rt.TRUE({cond})) {{")
        self.out.indent()

        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()
        self.out.emit("}")

        if ctx.ELSE():
            self.out.emit("else {")
            self.out.indent()
            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)
            self.out.dedent()
            self.out.emit("}")

    # forStmt : FOR IDENT ASSIGN numberExpr TO numberExpr (STEP numberExpr)? block ENDFOR ;
    def gen_for(self, ctx):
        var = ctx.IDENT().getText()
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"

        self.out.emit(f"rt.SET_NAME({self.jstr(var)}, TRT.V({start}));")
        self.out.emit(f"while (rt.TRUE(rt.FOR_COND(rt.GET_NAME({self.jstr(var)}), TRT.V({end}), TRT.V({step})))) {{")
        self.out.indent()

        for st in ctx.block().statement():
            self.gen_stmt(st)

        self.out.emit(f"rt.SET_NAME({self.jstr(var)}, rt.BINOP(rt.GET_NAME({self.jstr(var)}), \"+\", TRT.V({step})));")
        self.out.dedent()
        self.out.emit("}")

    def gen_break(self, ctx):
        self.out.emit("break;")

    def gen_return(self, ctx):
        # Top-level main: delegiere an Runtime (z.B. Exception oder Flag)
        if ctx.expr():
            self.out.emit(f"rt.RETURN({self.gen_expr(ctx.expr())});")
        else:
            self.out.emit("rt.RETURN(TRT.Null());")

    # parameterStmt : PARAMETER paramNames ;  paramNames : IDENT (',' IDENT)* ;
    def gen_parameter(self, ctx):
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({self.jstr_list(names)});")

    # exprStmt : postfixExpr ;
    def gen_expr_stmt(self, ctx):
        e = self.gen_postfix(ctx.postfixExpr())
        self.out.emit(e + ";")

    # WITH
    def gen_with(self, ctx):
        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()
        self.out.emit(f"Object {tmp} = {base};")
        self.out.emit(f"rt.PUSH_WITH({tmp});")

        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            t = type(ch).__name__
            if t.endswith("WithAssignStmtContext"):
                self.gen_with_assign(ch)
            elif t.endswith("WithStmtContext"):
                self.gen_with(ch)
            elif t.endswith("StatementContext"):
                self.gen_stmt(ch)

        self.out.emit("rt.POP_WITH();")

    def gen_with_target(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.dottedRef():
            base, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET(\"{base.upper()}\", {path})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.jstr(ctx.IDENT().getText())})"
        if ctx.postfixExpr():
            return self.gen_postfix(ctx.postfixExpr())
        return "TRT.Null()"

    def gen_with_assign(self, ctx):
        path = [t.getText() for t in ctx.withLvalue().IDENT()]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({self.jstr_list(path)}, {rhs});")

    # ----- expr/postfix/primary (runtime-backed) -----
    def gen_expr(self, ctx):
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"OR\", {rhs})"
        return out

    def gen_logical_and(self, ctx):
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"AND\", {rhs})"
        return out

    def gen_logical_not(self, ctx):
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP(\"NOT\", {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, {self.jstr(op)}, {right})"
        return left

    def gen_additive(self, ctx):
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.jstr(op)}, {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.jstr(op)}, {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        cur = self.gen_primary(ctx.primary())
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()
            if t == "(":
                args = []
                if kids[k+1].getText() != ")":
                    argctx = kids[k+1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1
                cur = f"rt.CALL_ANY({cur}, {self.jval_list(args)})"
                k += 2
                continue
            if t in (".", "::"):
                name = kids[k+1].getText()
                cur = f"rt.GET_ATTR({cur}, {self.jstr(name)})"
                k += 2
                continue
            k += 1
        return cur

    def gen_primary(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.STRING():
            return f"TRT.V({ctx.STRING().getText()})"
        if ctx.NUMBER():
            return f"TRT.V({ctx.NUMBER().getText()})"
        if ctx.FLOAT():
            return f"TRT.V({ctx.FLOAT().getText()})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.jstr(ctx.IDENT().getText())})"
        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())
        if ctx.expr():
            return "(" + self.gen_expr(ctx.expr()) + ")"
        return "TRT.Null()"

    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            args = [self.gen_expr(e) for e in ctx.argList().expr()]
        return f"rt.NEW({self.jstr(class_name)}, {self.jval_list(args)})"

    def gen_dotted_ref_parts(self, dctx):
        parts = [t.getText() for t in dctx.IDENT()]
        head = parts[0]
        if head.upper() == "THIS":
            base = "rt.GET_THIS()"
            path = self.jstr_list(parts[1:])
        else:
            base = f"rt.GET_NAME({self.jstr(head)})"
            path = self.jstr_list(parts[1:])
        return base, path

    def lvalue_chain_from_postfix(self, pe):
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()
            if ch == ".":
                chain.append(pe.getChild(i+1).getText())
                i += 2
                continue
            if ch == "(":
                raise RuntimeError(f"LVALUE darf keinen Call enthalten: {pe.getText()}")
            i += 1
        return chain

class DBaseToCSharp:
    def __init__(self, parser, class_name="GenProg", namespace=None, package=None):
        self.parser = parser
        self.class_name = class_name
        # Alias: falls du aus Gewohnheit package übergibst
        self.namespace = namespace if namespace is not None else package

        self.out = []
        self.indent = 0

    # ---------- public API ----------
    def generate(self, tree, outfile):
        self.out = []
        self.indent = 0

        # Header
        self.emit("using System;")
        self.emit()

        if self.namespace:
            self.emit(f"namespace {self.namespace} {{")
            self.indent += 1

        # Wenn tree eine Liste von items ist: iterieren, sonst direkt verarbeiten
        if hasattr(tree, "item"):
            # z.B. input: tree.item() -> liste
            for it in tree.item():
                self.gen_item(it)
        else:
            # fallback
            self.gen_any(tree)

        if self.namespace:
            self.indent -= 1
            self.emit("}")

        code = self.get_code()
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(code)

    # ---------- basics ----------
    def emit(self, s=""):
        self.out.append("    " * self.indent + s)

    def get_code(self):
        return "\n".join(self.out)

    # ---------- generic fallback ----------
    def gen_any(self, node):
        # versuche typische top-level struktur
        if hasattr(node, "classDecl") and node.classDecl():
            return self.gen_class(node.classDecl())
        if hasattr(node, "children"):
            for ch in node.children or []:
                self.gen_any(ch)
        else:
            self.emit(f"// TODO top node: {type(node).__name__}")

    # ---------- dispatcher: item ----------
    def gen_item(self, it):
        if hasattr(it, "classDecl") and it.classDecl():
            return self.gen_class(it.classDecl())
        self.emit(f"// TODO item: {type(it).__name__}")

    # ---------- class ----------
    def gen_class(self, ctx):
        # Wenn du class_name erzwingen willst (z.B. immer "GenProg"), dann:
        # class_name = self.class_name
        class_name = ctx.name.text if hasattr(ctx, "name") else self.class_name
        parent = ctx.parent.text if getattr(ctx, "parent", None) else None

        self.emit(f"public class {class_name}" + (f" : {parent}" if parent else "") + " {")
        self.indent += 1

        body = ctx.classBody() if hasattr(ctx, "classBody") else None
        children = list(getattr(body, "children", []) or []) if body else []

        for ch in children:
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self.gen_property(ch.propertyDecl())
            elif hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())
            elif hasattr(ch, "initDecl") and ch.initDecl():
                self.gen_init(ch.initDecl(), class_name)
            else:
                self.emit(f"// TODO class body child: {type(ch).__name__}")

        self.indent -= 1
        self.emit("}")
        self.emit()

    # ---------- property ----------
    def gen_property(self, ctx):
        name = ctx.IDENT().getText()
        self.emit(f"public object {name};")

    # ---------- method ----------
    def gen_method(self, ctx):
        name = ctx.IDENT().getText()

        params = []
        if hasattr(ctx, "paramList") and ctx.paramList():
            for p in ctx.paramList().IDENT():
                params.append(f"object {p.getText()}")

        self.emit(f"public object {name}(" + ", ".join(params) + ") {{")
        self.indent += 1

        block = ctx.block()
        for st in self.iter_block_statements(block):
            self._emit_stmt_multiline(self.gen_stmt(st))

        self.emit("return null;")
        self.indent -= 1
        self.emit("}")
        self.emit()

    def get_write_exprs(self, wctx):
        """
        Gibt eine Liste von Expr-Contexts zurück, die WRITE ausgeben soll.
        Funktioniert auch, wenn es kein wctx.expr() gibt.
        """
        if wctx is None:
            return []

        # 1) expr(i) / expr() (ANTLR: expr() kann Liste zurückgeben ODER expr(i) existiert)
        if hasattr(wctx, "expr"):
            expr_attr = getattr(wctx, "expr")
            if callable(expr_attr):
                try:
                    res = expr_attr()  # manche Grammatiken liefern direkt Liste
                    if res is not None:
                        return res if isinstance(res, list) else [res]
                except TypeError:
                    # wahrscheinlich expr(i) Variante
                    pass

            # expr(i) Variante
            try:
                out = []
                i = 0
                while True:
                    out.append(expr_attr(i))
                    i += 1
            except Exception:
                if out:
                    return out

        # 2) exprList().expr()
        if hasattr(wctx, "exprList") and wctx.exprList():
            el = wctx.exprList()
            if hasattr(el, "expr") and callable(el.expr):
                res = el.expr()
                if res is not None:
                    return res if isinstance(res, list) else [res]

        # 3) primary() (WRITE primary)
        if hasattr(wctx, "primary") and wctx.primary():
            p = wctx.primary()
            return p if isinstance(p, list) else [p]

        # 4) Fallback: children nach “Expr/Primary”-ähnlichen Nodes filtern
        kids = list(getattr(wctx, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "expr" in t or "primary" in t:
                out.append(ch)
        return out
        
    def gen_init(self, ctx, class_name):
        self.emit(f"public {class_name}() {{")
        self.indent += 1
        for st in ctx.block().stmt():
            self._emit_stmt_multiline(self.gen_stmt(st))
        self.indent -= 1
        self.emit("}")
        self.emit()

    def _emit_stmt_multiline(self, s):
        for line in s.split("\n"):
            self.emit(line)

    def get_assign_lhs(self, actx):
        """
        Liefert den linken Teil einer Zuweisung als Context zurück.
        Unterstützt viele Grammatik-Varianten: lhs(), lvalue(), target(), ref(), dottedRef(), primary(), IDENT()
        """
        if actx is None:
            return None

        for name in ("lhs", "lvalue", "target", "left", "ref"):
            fn = getattr(actx, name, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is not None:
                        return res
                except TypeError:
                    pass

        # oft ist LHS ein dottedRef
        if hasattr(actx, "dottedRef") and actx.dottedRef():
            return actx.dottedRef()

        # manchmal ist LHS einfach IDENT
        if hasattr(actx, "IDENT") and actx.IDENT():
            return actx.IDENT()

        # fallback: erstes child nehmen, das wie lvalue/ref aussieht
        kids = list(getattr(actx, "children", []) or [])
        for ch in kids:
            t = type(ch).__name__.lower()
            if "dottedref" in t or "lvalue" in t or "ref" in t or "primary" in t:
                return ch
        return None

    def get_assign_rhs(self, actx):
        """
        Liefert den rechten Teil einer Zuweisung als Expr-Context zurück.
        Häufig: expr() oder expr(i) (meist der letzte expr im AssignStmt)
        """
        if actx is None:
            return None

        if hasattr(actx, "expr") and callable(actx.expr):
            # Fall A: expr() gibt Liste oder einzelnes Element
            try:
                res = actx.expr()
                if isinstance(res, list):
                    return res[-1] if res else None
                if res is not None:
                    return res
            except TypeError:
                # Fall B: expr(i)
                i = 0
                last = None
                while True:
                    try:
                        last = actx.expr(i)
                        i += 1
                    except Exception:
                        break
                return last

        # fallback: letztes child, das wie expr aussieht
        kids = list(getattr(actx, "children", []) or [])
        for ch in reversed(kids):
            if "expr" in type(ch).__name__.lower() or hasattr(ch, "primary"):
                return ch
        return None
    
    def get_for_parts(self, fctx):
        """
        Liefert (var_name, start_expr_ctx, end_expr_ctx, step_expr_ctx, block_ctx)
        ohne vorauszusetzen, dass fctx.expr(i) existiert.
        """
        if fctx is None:
            return (None, None, None, None, None)

        # ---- var ----
        var = None
        if hasattr(fctx, "IDENT") and fctx.IDENT():
            var = fctx.IDENT().getText()

        # ---- block ----
        blk = None
        for bn in ("block", "stmtBlock", "forBlock"):
            fn = getattr(fctx, bn, None)
            if callable(fn):
                try:
                    blk = fn()
                    if blk is not None:
                        break
                except TypeError:
                    pass

        # ---- start/end/step: typische Namen ----
        start = end = step = None
        for sn in ("start", "startExpr", "fromExpr", "exprFrom"):
            fn = getattr(fctx, sn, None)
            if callable(fn):
                try:
                    start = fn()
                    if start is not None:
                        break
                except TypeError:
                    pass

        for en in ("end", "endExpr", "toExpr", "exprTo"):
            fn = getattr(fctx, en, None)
            if callable(fn):
                try:
                    end = fn()
                    if end is not None:
                        break
                except TypeError:
                    pass

        for pn in ("step", "stepExpr", "byExpr"):
            fn = getattr(fctx, pn, None)
            if callable(fn):
                try:
                    step = fn()
                    if step is not None:
                        break
                except TypeError:
                    pass

        # ---- falls FOR intern ein assignStmt hat: FOR i = <start> TO <end> ----
        if start is None:
            if hasattr(fctx, "assignStmt") and fctx.assignStmt():
                a = fctx.assignStmt()
                start = self.get_assign_rhs(a)  # aus deinem Assign-Helper von vorhin
                # var ggf. aus assign lhs
                if var is None:
                    lhs = get_assign_lhs(a)
                    # simplest: wenn lhs IDENT hat
                    if lhs is not None and hasattr(lhs, "IDENT") and lhs.IDENT():
                        var = lhs.IDENT().getText()

        # ---- letzter Fallback: children nach expr/primary durchsuchen ----
        if start is None or end is None:
            kids = list(getattr(fctx, "children", []) or [])
            expr_like = []
            for ch in kids:
                t = type(ch).__name__.lower()
                if "expr" in t or "primary" in t:
                    expr_like.append(ch)
            # Heuristik: erste = start, zweite = end, dritte = step
            if start is None and len(expr_like) >= 1:
                start = expr_like[0]
            if end is None and len(expr_like) >= 2:
                end = expr_like[1]
            if step is None and len(expr_like) >= 3:
                step = expr_like[2]

        return (var, start, end, step, blk)
        
    # ---------- statements ----------
    def gen_stmt(self, st):
        if hasattr(st, "writeStmt") and st.writeStmt():
            w = st.writeStmt()
            exprs = self.get_write_exprs(w)

            # wenn WRITE mehrere Werte erlaubt: jede Zeile einzeln ausgeben
            if not exprs:
                return "Console.WriteLine();"

            lines = []
            for ex in exprs:
                lines.append(f"Console.WriteLine({self.gen_expr(ex)});")
            return "\n".join(lines)

        if hasattr(st, "assignStmt") and st.assignStmt():
            a = st.assignStmt()
            
            lhs_ctx = self.get_assign_lhs(a)
            rhs_ctx = self.get_assign_rhs(a)

            lhs = self.gen_expr(lhs_ctx) if lhs_ctx is not None else "/* TODO lhs */"
            rhs = self.gen_expr(rhs_ctx) if rhs_ctx is not None else "/* TODO rhs */"
            
            return f"{lhs} = {rhs};"

        if hasattr(st, "returnStmt") and st.returnStmt():
            r = st.returnStmt()
            if hasattr(r, "expr") and r.expr():
                return f"return {self.gen_expr(r.expr())};"
            return "return null;"

        if hasattr(st, "breakStmt") and st.breakStmt():
            return "break;"

        if hasattr(st, "ifStmt") and st.ifStmt():
            return self.gen_if(st.ifStmt())

        if hasattr(st, "forStmt") and st.forStmt():
            return self.gen_for(st.forStmt())

        if hasattr(st, "expr") and st.expr():
            return self.gen_expr(st.expr()) + ";"

        return f"/* TODO stmt: {type(st).__name__} */;"

    def iter_block_statements(self, block):
        if block is None:
            return []

        for attr in ("stmt", "statement", "stat", "statementList", "stmtList", "stmts"):
            fn = getattr(block, attr, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is None:
                        continue
                    return res if isinstance(res, list) else [res]
                except TypeError:
                    pass

        kids = list(getattr(block, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "stmt" in t or "statement" in t or "stat" in t:
                out.append(ch)
        return out
        
    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())

        lines = [f"if ({cond}) {{"]

        # then block
        then_blk = ctx.thenBlock() if hasattr(ctx, "thenBlock") else (ctx.block(0) if hasattr(ctx, "block") else None)
        self.indent += 1
        for st in self.iter_block_statements(then_blk):
            lines.append("    " * self.indent + self.gen_stmt(st))
        self.indent -= 1
        lines.append("    " * self.indent + "}")

        # else block (optional)
        else_blk = None
        if hasattr(ctx, "elseBlock") and ctx.elseBlock():
            else_blk = ctx.elseBlock()
        elif hasattr(ctx, "block") and len(ctx.block()) > 1:
            else_blk = ctx.block(1)

        if else_blk is not None:
            lines.append("    " * self.indent + "else {")
            self.indent += 1
            for st in self.iter_block_statements(else_blk):
                lines.append("    " * self.indent + self.gen_stmt(st))
            self.indent -= 1
            lines.append("    " * self.indent + "}")

        return "\n".join(lines)

    def gen_for(self, ctx):
        var, start_ctx, end_ctx, step_ctx, blk = self.get_for_parts(ctx)

        var = var or "i"
        start = self.gen_expr(start_ctx) if start_ctx is not None else "0"
        end   = self.gen_expr(end_ctx)   if end_ctx   is not None else "0"
        step  = self.gen_expr(step_ctx)  if step_ctx  is not None else "1"

        cmp_op = "<="
        inc = f"{var} += {step}"
        if isinstance(step, str) and step.strip().startswith("-"):
            cmp_op = ">="
            inc = f"{var} += {step}"

        lines = [f"for (int {var} = {start}; {var} {cmp_op} {end}; {inc}) {{"]

        if blk is not None:
            self.indent += 1
            for st in self.iter_block_statements(blk):  # aus deinem Block-Fix
                lines.append("    " * self.indent + self.gen_stmt(st))
            self.indent -= 1
        else:
            lines.append("    " * (self.indent + 1) + "/* TODO for-block */")

        lines.append("    " * self.indent + "}")
        return "\n".join(lines)

    # ---------- expressions ----------
    def gen_expr(self, e):
        if hasattr(e, "primary") and e.primary():
            return self.gen_primary(e.primary())

        # falls du binOps als left/right/op hast:
        if hasattr(e, "left") and hasattr(e, "right") and hasattr(e, "op"):
            a = self.gen_expr(e.left)
            b = self.gen_expr(e.right)
            op = e.op.text
            op_map = {"AND": "&&", "OR": "||", "=": "==", "<>": "!="}
            op2 = op_map.get(op.upper(), op)
            return f"({a} {op2} {b})"

        if hasattr(e, "getText"):
            return e.getText()

        return f"/* TODO expr: {type(e).__name__} */null"

    def gen_primary(self, ctx):
        if hasattr(ctx, "newExpr") and ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        if hasattr(ctx, "NUMBER") and ctx.NUMBER():
            return ctx.NUMBER().getText()

        if hasattr(ctx, "STRING") and ctx.STRING():
            return ctx.STRING().getText()

        if hasattr(ctx, "IDENT") and ctx.IDENT():
            name = ctx.IDENT().getText()
            if name.upper() == "THIS":
                return "this"
            if name.upper() == "NIL":
                return "null"
            return name

        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            return self.gen_dotted_ref(ctx.dottedRef())

        if hasattr(ctx, "callExpr") and ctx.callExpr():
            return self.gen_call(ctx.callExpr())

        return f"/* TODO primary: {type(ctx).__name__} */null"

    def gen_dotted_ref(self, ctx):
        parts = [t.getText() for t in ctx.IDENT()]
        if parts and parts[0].upper() == "THIS":
            parts[0] = "this"
        return ".".join(parts)

    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))
        return f"new {class_name}(" + ", ".join(args) + ")"

    def gen_call(self, ctx):
        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            callee = self.gen_dotted_ref(ctx.dottedRef())
        elif hasattr(ctx, "IDENT") and ctx.IDENT():
            callee = ctx.IDENT().getText()
        else:
            callee = "/* TODO callee */"

        if callee.upper() == "WRITE":
            callee = "Console.WriteLine"

        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))

        return f"{callee}(" + ", ".join(args) + ")"
        
class DBaseToCpp:
    def __init__(self, parser, classes=None, prog_name="genprog"):
        self.p = parser
        self.out = CppEmitter()
        self.classes = classes or {}
        self.prog_name = prog_name
        self._tmp_i = 0

    def new_temp(self):
        self._tmp_i += 1
        return f"t{self._tmp_i}"

    # ---------- helpers ----------
    def cpp_str(self, s: str) -> str:
        return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

    def cpp_str_vec(self, items):
        # {"A","B"}
        inner = ", ".join(self.cpp_str(x) for x in items)
        return "{ " + inner + " }"

    def cpp_val_vec(self, exprs):
        # { a, b, c }
        inner = ", ".join(exprs)
        return "{ " + inner + " }"

    def norm_local(self, name: str) -> str:
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name).lower()

    # ---------- entry ----------
    def generate(self, tree, out_path: str):
        o = self.out
        o.emit("// generated dBase -> GNU C++ (runtime-backed)")
        o.emit("#include <iostream>")
        o.emit("#include <vector>")
        o.emit("#include <string>")
        o.emit("#include \"dBaseRT.hpp\"")
        o.emit("")
        o.emit("int main() {")
        o.indent()
        o.emit("TRT rt;")
        o.emit("try {")
        o.indent()

        self.gen_input(tree)

        o.dedent()
        o.emit("} catch (const std::exception& e) {")
        o.indent()
        o.emit('std::cerr << "ERROR: " << e.what() << std::endl;')
        o.emit("return 1;")
        o.dedent()
        o.emit("}")
        o.emit("return 0;")
        o.dedent()
        o.emit("}")
        Path(out_path).write_text(o.text(), encoding="utf-8")

    # ---------- root ----------
    def gen_input(self, ctx):
        for it in ctx.item():
            self.gen_item(it)

    def gen_item(self, it):
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            self.out.emit("// TODO classDecl not implemented in C++ backend")
            return
        if it.methodDecl():
            self.out.emit("// TODO methodDecl not implemented in C++ backend")
            return
        self.out.emit("// TODO unhandled item")

    # ---------- statements ----------
    def gen_stmt(self, st):
        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())
        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        if st.exprStmt():          return self.gen_expr_stmt(st.exprStmt())

        self.out.emit("// TODO unhandled statement: " + type(st.getChild(0)).__name__)

    def gen_write(self, ctx):
        # writeStmt : WRITE writeArg (PLUS writeArg)* ;
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]
        if not parts:
            self.out.emit("rt.WRITE(TRT::Null());")
            return

        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, \"+\", {p})"

        self.out.emit(f"rt.WRITE({expr});")

    def gen_write_arg(self, actx):
        if actx.STRING():
            return f"TRT::V({actx.STRING().getText()})"  # String-Literal inkl. Quotes kommt aus Lexer
        if actx.dottedRef():
            base, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET({base}, {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return "TRT::Null()"

    def gen_local_decl(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        self.out.emit(f"rt.SET_NAME({self.cpp_str(name)}, TRT::Null());")

    def gen_local_assign(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME({self.cpp_str(name)}, {rhs});")

    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        if lv.dottedRef():
            base, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)

            if len(chain) == 1:
                self.out.emit(f"rt.SET_NAME({self.cpp_str(chain[0])}, {rhs});")
                return

            head = chain[0]
            if head.upper() == "THIS":
                base = "rt.GET_THIS()"
                path = self.cpp_str_vec(chain[1:])
            else:
                base = f"rt.GET_NAME({self.cpp_str(head)})"
                path = self.cpp_str_vec(chain[1:])

            self.out.emit(f"rt.SET({base}, {path}, {rhs});")
            return

        self.out.emit("// TODO unsupported lvalue: " + lv.getText())

    def gen_if(self, ctx):
        # ifStmt : IF expr block (ELSE block)? ENDIF ;
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if (rt.TRUE({cond})) {{")
        self.out.indent()

        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()
        self.out.emit("}")

        if ctx.ELSE():
            self.out.emit("else {")
            self.out.indent()
            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)
            self.out.dedent()
            self.out.emit("}")

    def gen_for(self, ctx):
        # forStmt : FOR IDENT ASSIGN numberExpr TO numberExpr (STEP numberExpr)? block ENDFOR ;
        var = ctx.IDENT().getText()
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"

        # Wir halten "i" als Runtime-Variable, damit Semantik identisch bleibt
        self.out.emit(f"rt.SET_NAME({self.cpp_str(var)}, TRT::V({start}));")
        self.out.emit(f"while (rt.TRUE(rt.FOR_COND(rt.GET_NAME({self.cpp_str(var)}), TRT::V({end}), TRT::V({step})))) {{")
        self.out.indent()

        for st in ctx.block().statement():
            self.gen_stmt(st)

        self.out.emit(f"rt.SET_NAME({self.cpp_str(var)}, rt.BINOP(rt.GET_NAME({self.cpp_str(var)}), \"+\", TRT::V({step})));")
        self.out.dedent()
        self.out.emit("}")

    def gen_break(self, ctx):
        self.out.emit("break;")

    def gen_return(self, ctx):
        # Top-level main(): wir delegieren an runtime (oder du kannst return 0/1 machen)
        if ctx.expr():
            self.out.emit(f"rt.RETURN({self.gen_expr(ctx.expr())});")
        else:
            self.out.emit("rt.RETURN(TRT::Null());")

    def gen_parameter(self, ctx):
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({self.cpp_str_vec(names)});")

    def gen_expr_stmt(self, ctx):
        # exprStmt : postfixExpr ;
        e = self.gen_postfix(ctx.postfixExpr())
        self.out.emit(f"(void){e};")

    # ---------- WITH ----------
    def gen_with(self, ctx):
        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()
        self.out.emit(f"auto {tmp} = {base};")
        self.out.emit(f"rt.PUSH_WITH({tmp});")

        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            t = type(ch).__name__
            if t.endswith("WithAssignStmtContext"):
                self.gen_with_assign(ch)
            elif t.endswith("WithStmtContext"):
                self.gen_with(ch)
            elif t.endswith("StatementContext"):
                self.gen_stmt(ch)

        self.out.emit("rt.POP_WITH();")

    def gen_with_target(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.dottedRef():
            base, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET('{base.upper()}', {path})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.cpp_str(ctx.IDENT().getText())})"
        if ctx.postfixExpr():
            return self.gen_postfix(ctx.postfixExpr())
        return "TRT::Null()"

    def gen_with_assign(self, ctx):
        path = [t.getText() for t in ctx.withLvalue().IDENT()]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({self.cpp_str_vec(path)}, {rhs});")

    # ---------- expr / postfix / primary ----------
    # Hier kannst du (fast) genau deine Python-Version übernehmen, nur dass
    # du C++-Strings und TRT::V(...) nutzt. Ich mach’s minimal:

    def gen_expr(self, ctx):
        # expr : logicalOr ;
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"OR\", {rhs})"
        return out

    def gen_logical_and(self, ctx):
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, \"AND\", {rhs})"
        return out

    def gen_logical_not(self, ctx):
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP(\"NOT\", {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, {self.cpp_str(op)}, {right})"
        return left

    def gen_additive(self, ctx):
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.cpp_str(op)}, {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, {self.cpp_str(op)}, {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        cur = self.gen_primary(ctx.primary())
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()
            if t == "(":
                args = []
                if kids[k+1].getText() != ")":
                    argctx = kids[k+1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1
                cur = f"rt.CALL_ANY({cur}, {self.cpp_val_vec(args)})"
                k += 2
                continue
            if t in (".", "::"):
                name = kids[k+1].getText()
                cur = f"rt.GET_ATTR({cur}, {self.cpp_str(name)})"
                k += 2
                continue
            k += 1
        return cur

    def gen_primary(self, ctx):
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.STRING():
            return f"TRT::V({ctx.STRING().getText()})"
        if ctx.NUMBER():
            return f"TRT::V({ctx.NUMBER().getText()})"
        if ctx.FLOAT():
            return f"TRT::V({ctx.FLOAT().getText()})"
        if ctx.IDENT():
            return f"rt.GET_NAME({self.cpp_str(ctx.IDENT().getText())})"
        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())
        if ctx.expr():
            return "(" + self.gen_expr(ctx.expr()) + ")"
        return "TRT::Null()"

    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            args = [self.gen_expr(e) for e in ctx.argList().expr()]
        return f"rt.NEW({self.cpp_str(class_name)}, {self.cpp_val_vec(args)})"

    def gen_dotted_ref_parts(self, dctx):
        parts = [t.getText() for t in dctx.IDENT()]
        head = parts[0]
        if head.upper() == "THIS":
            base = "rt.GET_THIS()"
            path = self.cpp_str_vec(parts[1:])
        else:
            base = f"rt.GET_NAME({self.cpp_str(head)})"
            path = self.cpp_str_vec(parts[1:])
        return base, path

    def lvalue_chain_from_postfix(self, pe):
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()
            if ch == ".":
                chain.append(pe.getChild(i+1).getText())
                i += 2
                continue
            if ch == "(":
                raise RuntimeError(f"LVALUE darf keinen Call enthalten: {pe.getText()}")
            i += 1
        return chain
        
class DBaseToPascal:
    def __init__(self, parser, classes=None, unit_name="GenProg"):
        self.p = parser
        self.out = PasEmitter()
        self.classes = classes or {}
        self.unit_name = unit_name
        self._tmp_i = 0

    def new_temp(self):
        self._tmp_i += 1
        return f"t{self._tmp_i}"

    # ----------------- ENTRY -----------------
    def generate(self, tree, out_path: str):
        o = self.out

        # Minimal-Programm. Du kannst auch "unit" generieren, wenn du willst.
        o.emit(f"program {self.unit_name};")
        o.emit("")
        o.emit("{$mode objfpc}{$H+}")
        o.emit("")
        o.emit("uses")
        o.indent()
        o.emit("SysUtils, Variants, dBaseRT;")
        o.dedent()
        o.emit(";")
        o.emit("")
        o.emit("var")
        o.indent()
        o.emit("rt: TRT;")
        o.dedent()
        o.emit("")
        o.emit("begin")
        o.indent()
        o.emit("rt := TRT.Create;")
        o.emit("try")
        o.indent()

        self.gen_input(tree)

        o.dedent()
        o.emit("finally")
        o.indent()
        o.emit("rt.Free;")
        o.dedent()
        o.emit("end;")
        o.dedent()
        o.emit("end.")
        Path(out_path).write_text(o.text(), encoding="utf-8")

    # ----------------- ROOT -----------------
    def gen_input(self, ctx):
        # input : item* EOF
        for it in ctx.item():
            self.gen_item(it)

    def gen_item(self, it):
        # item : classDecl | methodDecl | statement
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            return self.gen_class(it.classDecl())   # optional später
        if it.methodDecl():
            return self.gen_method(it.methodDecl()) # optional später
        self.out.emit("{ TODO unhandled item }")

    # ----------------- STATEMENTS -----------------
    def gen_stmt(self, st):
        # Passe das an die Stmt-Alternativen an, die du schon in Python eingebaut hast.
        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())
        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        # … Schritt für Schritt erweitern …
        self.out.emit("{ TODO unhandled statement: " + type(st.getChild(0)).__name__ + " }")

    def gen_write(self, ctx):
        # writeStmt : WRITE writeArg (PLUS writeArg)* ;
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]
        if not parts:
            self.out.emit("rt.WRITE('');")
            return

        # dBase-Plus soll runtime-semantisch bleiben -> BINOP kaskadieren
        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, '+', {p})"

        self.out.emit(f"rt.WRITE({expr});")

    def gen_write_arg(self, actx):
        # writeArg : STRING | dottedRef | expr ;
        if actx.STRING():
            return actx.STRING().getText()
        if actx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return f"Null"

    def gen_local_decl(self, ctx):
        # LOCAL IDENT
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        self.out.emit(f"rt.SET_NAME('{name}', Null);")

    def gen_local_assign(self, ctx):
        name = ctx.name.text if hasattr(ctx, "name") else ctx.IDENT().getText()
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME('{name}', {rhs});")

    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        # lvalue : postfixExpr | dottedRef ;
        if lv.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET_({base_expr}, {path}, {rhs});")
            return

        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)  # ["Y"] oder ["THIS","X","Y"]

            if len(chain) == 1:
                self.out.emit(f"rt.SET_NAME('{chain[0]}', {rhs});")
                return

            head = chain[0]
            if head.upper() == "THIS":
                base_expr = "rt.GET_THIS()"
                path = chain[1:]
            else:
                base_expr = f"rt.GET_NAME('{head}')"
                path = chain[1:]

            self.out.emit(f"rt.SET_({base_expr}, {self.pas_str_array(path)}, {rhs});")
            return

        self.out.emit("{ TODO unsupported lvalue }")

    def gen_if(self, ctx):
        # ifStmt : IF expr block (ELSE block)? ENDIF ;
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if rt.TRUE_({cond}) then")
        self.out.emit("begin")
        self.out.indent()

        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()
        self.out.emit("end")

        if ctx.ELSE():
            self.out.emit("else")
            self.out.emit("begin")
            self.out.indent()

            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)

            self.out.dedent()
            self.out.emit("end;")
        else:
            self.out.emit(";")

    def gen_for(self, ctx):
        # forStmt : FOR IDENT ASSIGN numberExpr TO numberExpr (STEP numberExpr)? block ENDFOR ;
        varname = self.norm_local(ctx.IDENT().getText())
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"

        # STEP != 1 -> while-Schleife (FPC for kann keinen Step)
        if step == "1":
            self.out.emit(f"rt.SET_NAME('{varname}', {start});")
            self.out.emit(f"while rt.TRUE_(rt.BINOP(rt.GET_NAME('{varname}'), '<=', {end})) do")
            self.out.emit("begin")
            self.out.indent()
            # Body
            for st in ctx.block().statement():
                self.gen_stmt(st)
            # Increment
            self.out.emit(f"rt.SET_NAME('{varname}', rt.BINOP(rt.GET_NAME('{varname}'), '+', {step}));")
            self.out.dedent()
            self.out.emit("end;")
        else:
            # allgemein: i := start; while cond: body; i += step
            self.out.emit(f"rt.SET_NAME('{varname}', {start});")
            self.out.emit(f"while rt.TRUE_(rt.FOR_COND(rt.GET_NAME('{varname}'), {end}, {step})) do")
            self.out.emit("begin")
            self.out.indent()
            for st in ctx.block().statement():
                self.gen_stmt(st)
            self.out.emit(f"rt.SET_NAME('{varname}', rt.BINOP(rt.GET_NAME('{varname}'), '+', {step}));")
            self.out.dedent()
            self.out.emit("end;")

    def gen_break(self, ctx):
        # in Pascal: break;
        self.out.emit("break;")

    def gen_return(self, ctx):
        # Im Program-Level gibt es kein "return". In Methoden später: Exit(value).
        # Hier delegieren wir:
        if ctx.expr():
            self.out.emit(f"rt.RETURN_({self.gen_expr(ctx.expr())});")
        else:
            self.out.emit("rt.RETURN_(Null);")

    def gen_parameter(self, ctx):
        # parameterStmt : PARAMETER paramNames ;
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({self.pas_str_array(names)});")

    # ----------------- WITH -----------------
    def gen_with(self, ctx):
        # withStmt : WITH '(' withTarget ')' withBody ENDWITH ;
        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()
        self.out.emit(f"var {tmp}: Variant; {tmp} := {base};")  # simpel, du kannst var-block auch global machen
        self.out.emit(f"rt.PUSH_WITH({tmp});")
        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            t = type(ch).__name__
            if t.endswith("WithAssignStmtContext"):
                self.gen_with_assign(ch)
            elif t.endswith("WithStmtContext"):
                self.gen_with(ch)
            elif t.endswith("StatementContext"):
                self.gen_stmt(ch)
        self.out.emit("rt.POP_WITH();")

    def gen_with_target(self, ctx):
        # withTarget : THIS | dottedRef | IDENT | postfixExpr ;
        if ctx.THIS():
            return "rt.GET_THIS()"
        if ctx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"
        if ctx.IDENT():
            name = ctx.IDENT().getText()
            return f"rt.GET_NAME('{name}')"
        if ctx.postfixExpr():
            return self.gen_postfix(ctx.postfixExpr())
        return "Null"

    def gen_with_assign(self, ctx):
        # withAssignStmt : withLvalue ASSIGN expr ;
        path = [t.getText() for t in ctx.withLvalue().IDENT()]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({self.pas_str_array(path)}, {rhs});")

    # ----------------- EXPRESSIONS -----------------
    # Hier: nutze deine bereits angepassten gen_expr/gen_postfix/gen_primary-Methoden,
    # aber gib Pascal-Ausdrücke zurück, die auf rt.* basieren.

    def gen_expr(self, ctx):
        # expr : logicalOr ;
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'OR', {rhs})"
        return out

    def gen_logical_and(self, ctx):
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'AND', {rhs})"
        return out

    def gen_logical_not(self, ctx):
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP('NOT', {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, '{op}', {right})"
        return left

    def gen_additive(self, ctx):
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, '{op}', {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        kids = list(ctx.getChildren())
        i = 1
        while i < len(kids):
            op = kids[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, '{op}', {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        # postfixExpr : primary ( '(' argList? ')' | ('.'|'::') IDENT )* ;
        cur = self.gen_primary(ctx.primary())
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()
            if t == "(":
                args = []
                if kids[k+1].getText() != ")":
                    argctx = kids[k+1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1
                cur = f"rt.CALL_ANY({cur}, {self.pas_expr_array(args)})"
                k += 2
                continue
            if t in (".", "::"):
                name = kids[k+1].getText()
                cur = f"rt.GET_ATTR({cur}, '{name}')"
                k += 2
                continue
            k += 1
        return cur
    
    def gen_new(self, ctx):
        # newExpr : NEW IDENT LPAREN argList? RPAREN ;
        class_name = ctx.IDENT().getText()
        args = []
        if ctx.argList():
            args = [self.gen_expr(e) for e in ctx.argList().expr()]
        
        # Pascal: array of Variant -> wir geben einen Pascal-Array-Ausdruck zurück
        return f"rt.NEW('{class_name}', {self.pas_expr_array(args)})"
    
    def gen_class(self, ctx):
        self.out.emit("{ TODO gen_class: " + ctx.name.text + " }")

    def gen_method(self, ctx):
        self.out.emit("{ TODO gen_method: " + ctx.IDENT().getText() + " }")
        
    def gen_primary(self, ctx):
        if ctx.THIS():    return "rt.GET_THIS()"
        if ctx.STRING():  return ctx.STRING().getText()
        if ctx.NUMBER():  return ctx.NUMBER().getText()
        if ctx.FLOAT():   return ctx.FLOAT().getText()
        if ctx.IDENT():
            name = ctx.IDENT().getText()
            return f"rt.GET_NAME('{name}')"
        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())
        if ctx.expr():
            return f"({self.gen_expr(ctx.expr())})"
        return "Null"

    # ----------------- dottedRef / lvalue helpers -----------------
    def gen_dotted_ref_parts(self, dctx):
        parts = [t.getText() for t in dctx.IDENT()]
        head = parts[0]
        if head.upper() == "THIS":
            base = "rt.GET_THIS()"
            path = parts[1:]
        else:
            base = f"rt.GET_NAME('{head}')"
            path = parts[1:]
        return base, self.pas_str_array(path)

    def lvalue_chain_from_postfix(self, pe):
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()
            if ch == ".":
                chain.append(pe.getChild(i+1).getText())
                i += 2
                continue
            if ch == "(":
                raise RuntimeError(f"LVALUE darf keinen Call enthalten: {pe.getText()}")
            i += 1
        return chain

    # ----------------- small utils -----------------
    def pas_str_array(self, items):
        # ["A","B"] -> ['A','B']
        inner = ", ".join("'" + s.replace("'", "''") + "'" for s in items)
        return f"[{inner}]"

    def pas_expr_array(self, exprs):
        # ["rt.GET_NAME('X')", "5"] -> [rt.GET_NAME('X'), 5]
        inner = ", ".join(exprs)
        return f"[{inner}]"

    def norm_local(self, name: str) -> str:
        # optional (wenn du Namen in Pascal-Var-IDs brauchst)
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name).lower()

class DBaseToJavaScript:
    def __init__(self, parser, class_name="GenProg", module_name=None):
        self.parser = parser
        self.class_name = class_name
        self.module_name = module_name  # optional
        self.out = []
        self.indent = 0

    # ---------- robuste Helfer (wie zuvor) ----------
    def iter_block_statements(self, block):
        if block is None:
            return []
        for attr in ("stmt", "statement", "stat", "statementList", "stmtList", "stmts"):
            fn = getattr(block, attr, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is None:
                        continue
                    return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
        kids = list(getattr(block, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "stmt" in t or "statement" in t or "stat" in t:
                out.append(ch)
        return out

    def get_write_exprs(self, wctx):
        if wctx is None:
            return []
        if hasattr(wctx, "expr"):
            expr_attr = getattr(wctx, "expr")
            if callable(expr_attr):
                try:
                    res = expr_attr()
                    if res is not None:
                        return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
            try:
                out = []
                i = 0
                while True:
                    out.append(expr_attr(i))
                    i += 1
            except Exception:
                if out:
                    return out
        if hasattr(wctx, "exprList") and wctx.exprList():
            el = wctx.exprList()
            if hasattr(el, "expr") and callable(el.expr):
                res = el.expr()
                if res is not None:
                    return res if isinstance(res, list) else [res]
        if hasattr(wctx, "primary") and wctx.primary():
            p = wctx.primary()
            return p if isinstance(p, list) else [p]
        kids = list(getattr(wctx, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "expr" in t or "primary" in t:
                out.append(ch)
        return out
        
    def get_assign_lhs(self, actx):
        if actx is None:
            return None
        for name in ("lhs", "lvalue", "target", "left", "ref"):
            fn = getattr(actx, name, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is not None:
                        return res
                except TypeError:
                    pass
        if hasattr(actx, "dottedRef") and actx.dottedRef():
            return actx.dottedRef()
        if hasattr(actx, "IDENT") and actx.IDENT():
            return actx.IDENT()
        kids = list(getattr(actx, "children", []) or [])
        for ch in kids:
            t = type(ch).__name__.lower()
            if "dottedref" in t or "lvalue" in t or "ref" in t or "primary" in t:
                return ch
        return None

    def get_assign_rhs(self, actx):
        if actx is None:
            return None
        if hasattr(actx, "expr") and callable(actx.expr):
            try:
                res = actx.expr()
                if isinstance(res, list):
                    return res[-1] if res else None
                if res is not None:
                    return res
            except TypeError:
                i = 0
                last = None
                while True:
                    try:
                        last = actx.expr(i)
                        i += 1
                    except Exception:
                        break
                return last
        kids = list(getattr(actx, "children", []) or [])
        for ch in reversed(kids):
            if "expr" in type(ch).__name__.lower() or hasattr(ch, "primary"):
                return ch
        return None

    # --- API wie bei dir ---
    def generate(self, tree, outfile):
        self.out, self.indent = [], 0

        # Header: ES Modules, Runtime import
        self.emit('import { WRITE, NEWOBJ, ParentForm } from "./rt.js";')
        self.emit()

        # Tree abarbeiten
        if hasattr(tree, "item"):
            for it in tree.item():
                self.gen_item(it)
        else:
            self.gen_any(tree)

        # optional: Auto-Start / Main
        self.emit()
        self.emit(f"// --- optional quick test ---")
        self.emit(f"// const app = new {self.class_name}();")
        self.emit(f"// if (app.Init) app.Init();")

        with open(outfile, "w", encoding="utf-8") as f:
            f.write(self.get_code())

    # --- basics ---
    def emit(self, s=""):
        self.out.append("  " * self.indent + s)

    def get_code(self):
        return "\n".join(self.out)

    # --- tree fallback ---
    def gen_any(self, node):
        if hasattr(node, "classDecl") and node.classDecl():
            return self.gen_class(node.classDecl())
        if hasattr(node, "children"):
            for ch in (node.children or []):
                self.gen_any(ch)

    # --- old schema entrypoints ---
    def gen_item(self, it):
        if hasattr(it, "classDecl") and it.classDecl():
            return self.gen_class(it.classDecl())
        self.emit(f"// TODO item: {type(it).__name__}")

    def gen_class(self, ctx):
        # Du kannst wahlweise ctx.name.text nehmen, oder immer class_name erzwingen
        cls = self.class_name

        parent = "ParentForm"
        if getattr(ctx, "parent", None):
            parent = ctx.parent.text

        self.emit(f"export class {cls} extends {parent} " + "{")
        self.indent += 1

        body = ctx.classBody()
        children = list(getattr(body, "children", []) or [])

        # Properties -> in JS im ctor initialisieren
        props = []
        for ch in children:
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                props.append(ch.propertyDecl().IDENT().getText())

        self.emit("constructor() {")
        self.indent += 1
        self.emit("super();")
        for p in props:
            self.emit(f"this.{p} = null;")
        self.indent -= 1
        self.emit("}")
        self.emit()

        # Methods
        for ch in children:
            if hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())

        self.indent -= 1
        self.emit("}")
        self.emit()

    def gen_method(self, ctx):
        name = ctx.IDENT().getText()

        params = []
        if hasattr(ctx, "paramList") and ctx.paramList():
            for p in ctx.paramList().IDENT():
                params.append(p.getText())

        self.emit(f"{name}(" + ", ".join(params) + ") {")
        self.indent += 1

        block = ctx.block()
        for st in self.iter_block_statements(block):
            self._emit_stmt_multiline(self.gen_stmt(st))

        self.indent -= 1
        self.emit("}")
        self.emit()

    def _emit_stmt_multiline(self, s):
        for line in s.split("\n"):
            self.emit(line)

    # --- statements ---
    def gen_stmt(self, st):
        # WRITE -> WRITE(...)
        if hasattr(st, "writeStmt") and st.writeStmt():
            w = st.writeStmt()
            exprs = self.get_write_exprs(w)
            args = ", ".join(self.gen_expr(ex) for ex in exprs)
            return f"WRITE({args});" if args else "WRITE();"

        # ASSIGN
        if hasattr(st, "assignStmt") and st.assignStmt():
            a = st.assignStmt()
            lhs_ctx = self.get_assign_lhs(a)
            rhs_ctx = self.get_assign_rhs(a)
            lhs = self.gen_expr(lhs_ctx) if lhs_ctx is not None else "/* TODO lhs */"
            rhs = self.gen_expr(rhs_ctx) if rhs_ctx is not None else "/* TODO rhs */"
            return f"{lhs} = {rhs};"

        # RETURN
        if hasattr(st, "returnStmt") and st.returnStmt():
            r = st.returnStmt()
            if hasattr(r, "expr") and r.expr():
                return f"return {self.gen_expr(r.expr())};"
            return "return;"

        # BREAK
        if hasattr(st, "breakStmt") and st.breakStmt():
            return "break;"

        # IF
        if hasattr(st, "ifStmt") and st.ifStmt():
            return self.gen_if(st.ifStmt())

        # FOR
        if hasattr(st, "forStmt") and st.forStmt():
            return self.gen_for(st.forStmt())

        # expr stmt
        if hasattr(st, "expr") and st.expr():
            return self.gen_expr(st.expr()) + ";"

        return f"// TODO stmt: {type(st).__name__}"

    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())
        lines = [f"if ({cond}) {{"]

        then_blk = ctx.thenBlock() if hasattr(ctx, "thenBlock") else (ctx.block(0) if hasattr(ctx, "block") else None)
        self.indent += 1
        for st in self.iter_block_statements(then_blk):
            lines.append("  " * self.indent + self.gen_stmt(st))
        self.indent -= 1
        lines.append("  " * self.indent + "}")

        # else optional
        else_blk = None
        if hasattr(ctx, "elseBlock") and ctx.elseBlock():
            else_blk = ctx.elseBlock()
        elif hasattr(ctx, "block") and len(ctx.block()) > 1:
            else_blk = ctx.block(1)

        if else_blk is not None:
            lines.append("  " * self.indent + "else {")
            self.indent += 1
            for st in self.iter_block_statements(else_blk):
                lines.append("  " * self.indent + self.gen_stmt(st))
            self.indent -= 1
            lines.append("  " * self.indent + "}")

        return "\n".join(lines)

    def gen_for(self, ctx):
        # Da dein ForStmtContext kein expr() hat, wieder heuristisch
        var = ctx.IDENT().getText() if hasattr(ctx, "IDENT") and ctx.IDENT() else "i"

        start_ctx = end_ctx = step_ctx = None
        for nm in ("startExpr", "fromExpr", "start"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    start_ctx = fn()
                    if start_ctx is not None:
                        break
                except TypeError:
                    pass
        for nm in ("endExpr", "toExpr", "end"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    end_ctx = fn()
                    if end_ctx is not None:
                        break
                except TypeError:
                    pass
        for nm in ("stepExpr", "byExpr", "step"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    step_ctx = fn()
                    if step_ctx is not None:
                        break
                except TypeError:
                    pass

        start = self.gen_expr(start_ctx) if start_ctx is not None else "0"
        end   = self.gen_expr(end_ctx)   if end_ctx   is not None else "0"
        step  = self.gen_expr(step_ctx)  if step_ctx  is not None else "1"

        lines = [f"for (let {var} = {start}; {var} <= {end}; {var} += {step}) {{"]

        blk = ctx.block() if hasattr(ctx, "block") else None
        self.indent += 1
        for st in self.iter_block_statements(blk):
            lines.append("  " * self.indent + self.gen_stmt(st))
        self.indent -= 1

        lines.append("  " * self.indent + "}")
        return "\n".join(lines)

    # --- expressions ---
    def gen_expr(self, e):
        if e is None:
            return "null"

        if hasattr(e, "primary") and e.primary():
            return self.gen_primary(e.primary())

        if hasattr(e, "left") and hasattr(e, "right") and hasattr(e, "op"):
            a = self.gen_expr(e.left)
            b = self.gen_expr(e.right)
            op = e.op.text
            op_map = {"AND": "&&", "OR": "||", "=": "==", "<>": "!="}
            op2 = op_map.get(op.upper(), op)
            return f"({a} {op2} {b})"

        if hasattr(e, "getText"):
            return e.getText()

        return "null"

    def gen_primary(self, ctx):
        # NEW
        if hasattr(ctx, "newExpr") and ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        if hasattr(ctx, "NUMBER") and ctx.NUMBER():
            return ctx.NUMBER().getText()

        if hasattr(ctx, "STRING") and ctx.STRING():
            return ctx.STRING().getText()

        if hasattr(ctx, "IDENT") and ctx.IDENT():
            name = ctx.IDENT().getText()
            if name.upper() == "THIS":
                return "this"
            if name.upper() == "NIL":
                return "null"
            return name

        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            return self.gen_dotted_ref(ctx.dottedRef())

        if hasattr(ctx, "callExpr") and ctx.callExpr():
            return self.gen_call(ctx.callExpr())

        return "null"

    def gen_dotted_ref(self, ctx):
        parts = [t.getText() for t in ctx.IDENT()]
        if parts and parts[0].upper() == "THIS":
            parts[0] = "this"
        return ".".join(parts)

    def gen_new(self, ctx):
        # JS: entweder direkt new ClassName(...) ODER Runtime NEWOBJ
        # Da du Klassen evtl. nicht immer als JS-Klasse hast: robust über NEWOBJ("Class", args)
        class_name = ctx.IDENT().getText()
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))
        return f'NEWOBJ("{class_name}", ' + ", ".join(args) + ")" if args else f'NEWOBJ("{class_name}")'

    def gen_call(self, ctx):
        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            callee = self.gen_dotted_ref(ctx.dottedRef())
        elif hasattr(ctx, "IDENT") and ctx.IDENT():
            callee = ctx.IDENT().getText()
        else:
            callee = "/*callee*/"

        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))

        # WRITE als Funktion
        if callee.upper() == "WRITE":
            callee = "WRITE"

        return callee + "(" + ", ".join(args) + ")"
        
class DBaseToVBAAccess:
    """
    Generiert:
      - <module_name>.bas  (Standardmodul mit Public Sub Main oder Hilfsprocs)
      - <class_name>.cls   (Class Module)
      - RT.bas, PushButton.cls (Runtime)
    """
    def __init__(self, parser, class_name="GenProg", module_name="GenProg"):
        self.parser = parser
        self.class_name = class_name
        self.module_name = module_name

        self.out = []
        self.indent = 0
        self._cur_func = None  # für RETURN in VBA

    # --- Reuse von deinen robusten Helfern (Block/WRITE/ASSIGN/FOR) ---
    def iter_block_statements(self, block):
        if block is None:
            return []
        for attr in ("stmt", "statement", "stat", "statementList", "stmtList", "stmts"):
            fn = getattr(block, attr, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is None:
                        continue
                    return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
        kids = list(getattr(block, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "stmt" in t or "statement" in t or "stat" in t:
                out.append(ch)
        return out

    def get_write_exprs(self, wctx):
        if wctx is None:
            return []
        if hasattr(wctx, "expr"):
            expr_attr = getattr(wctx, "expr")
            if callable(expr_attr):
                try:
                    res = expr_attr()
                    if res is not None:
                        return res if isinstance(res, list) else [res]
                except TypeError:
                    pass
            try:
                out = []
                i = 0
                while True:
                    out.append(expr_attr(i))
                    i += 1
            except Exception:
                if out:
                    return out
        if hasattr(wctx, "exprList") and wctx.exprList():
            el = wctx.exprList()
            if hasattr(el, "expr") and callable(el.expr):
                res = el.expr()
                if res is not None:
                    return res if isinstance(res, list) else [res]
        if hasattr(wctx, "primary") and wctx.primary():
            p = wctx.primary()
            return p if isinstance(p, list) else [p]
        kids = list(getattr(wctx, "children", []) or [])
        out = []
        for ch in kids:
            t = type(ch).__name__.lower()
            if "expr" in t or "primary" in t:
                out.append(ch)
        return out

    def get_assign_lhs(self, actx):
        if actx is None:
            return None
        for name in ("lhs", "lvalue", "target", "left", "ref"):
            fn = getattr(actx, name, None)
            if callable(fn):
                try:
                    res = fn()
                    if res is not None:
                        return res
                except TypeError:
                    pass
        if hasattr(actx, "dottedRef") and actx.dottedRef():
            return actx.dottedRef()
        if hasattr(actx, "IDENT") and actx.IDENT():
            return actx.IDENT()
        kids = list(getattr(actx, "children", []) or [])
        for ch in kids:
            t = type(ch).__name__.lower()
            if "dottedref" in t or "lvalue" in t or "ref" in t or "primary" in t:
                return ch
        return None

    def get_assign_rhs(self, actx):
        if actx is None:
            return None
        if hasattr(actx, "expr") and callable(actx.expr):
            try:
                res = actx.expr()
                if isinstance(res, list):
                    return res[-1] if res else None
                if res is not None:
                    return res
            except TypeError:
                i = 0
                last = None
                while True:
                    try:
                        last = actx.expr(i)
                        i += 1
                    except Exception:
                        break
                return last
        kids = list(getattr(actx, "children", []) or [])
        for ch in reversed(kids):
            if "expr" in type(ch).__name__.lower() or hasattr(ch, "primary"):
                return ch
        return None

    # ---------- file writing ----------
    def generate(self, tree, filename):
        # 2) Klasse generieren
        self.out, self.indent = [], 0
        self._emit_class_header()
        self._gen_tree(tree)
        cls_code = self.get_code()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(cls_code)

    # ---------- emit helpers ----------
    def emit(self, s=""):
        self.out.append("    " * self.indent + s)

    def get_code(self):
        return "\n".join(self.out)

    def _emit_class_header(self):
        # Access .cls Textformat braucht keinen speziellen Header, nur Option/Explicit ist gut.
        self.emit("Option Compare Database")
        self.emit("Option Explicit")
        self.emit()

    # ---------- tree driving ----------
    def _gen_tree(self, tree):
        # je nach deinem parse-tree:
        if hasattr(tree, "item"):
            for it in tree.item():
                self.gen_item(it)
        else:
            self.gen_any(tree)

    def gen_any(self, node):
        if hasattr(node, "classDecl") and node.classDecl():
            return self.gen_class(node.classDecl())
        if hasattr(node, "children"):
            for ch in (node.children or []):
                self.gen_any(ch)

    # ---------- old schema entrypoints ----------
    def gen_item(self, it):
        if hasattr(it, "classDecl") and it.classDecl():
            return self.gen_class(it.classDecl())
        # sonst ignorieren
        return None

    def gen_class(self, ctx):
        # VBA: wir generieren i.d.R. genau eine Klasse als Ziel (class_name),
        # aber du kannst auch ctx.name.text nehmen – je nachdem was du willst.
        cls = self.class_name

        body = ctx.classBody()
        children = list(getattr(body, "children", []) or [])

        # Properties
        for ch in children:
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self.gen_property(ch.propertyDecl())

        # Methods
        for ch in children:
            if hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())

    def gen_property(self, ctx):
        name = ctx.IDENT().getText()
        # VBA: als Public Variant (dynamisch)
        self.emit(f"Public {name} As Variant")

    def gen_method(self, ctx):
        name = ctx.IDENT().getText()
        self._cur_func = name

        params = []
        if hasattr(ctx, "paramList") and ctx.paramList():
            for p in ctx.paramList().IDENT():
                params.append(f"ByVal {p.getText()} As Variant")

        self.emit()
        self.emit(f"Public Function {name}(" + ", ".join(params) + ") As Variant")
        self.indent += 1

        block = ctx.block()
        for st in self.iter_block_statements(block):
            self._emit_stmt_multiline(self.gen_stmt(st))

        # Default return
        self.emit(f"{name} = Null")
        self.indent -= 1
        self.emit("End Function")

        self._cur_func = None

    def _emit_stmt_multiline(self, s):
        for line in s.split("\n"):
            self.emit(line)

    # ---------- statements ----------
    def gen_stmt(self, st):
        # WRITE
        if hasattr(st, "writeStmt") and st.writeStmt():
            w = st.writeStmt()
            exprs = self.get_write_exprs(w)
            if not exprs:
                return "Debug.Print"
            args = ", ".join(self.gen_expr(ex) for ex in exprs)
            # wir nutzen RT.WRITE, damit multi-args sauber sind
            return f"WRITE {args}"

        # ASSIGN
        if hasattr(st, "assignStmt") and st.assignStmt():
            a = st.assignStmt()
            lhs_ctx = self.get_assign_lhs(a)
            rhs_ctx = self.get_assign_rhs(a)
            lhs = self.gen_expr(lhs_ctx) if lhs_ctx is not None else "/*lhs*/"
            rhs = self.gen_expr(rhs_ctx) if rhs_ctx is not None else "/*rhs*/"

            # VBA braucht Set bei Objektzuweisung. Heuristik: rhs beginnt mit NEWOBJ(...) oder New ...
            rhs_trim = rhs.lstrip()
            if rhs_trim.upper().startswith("NEWOBJ(") or rhs_trim.upper().startswith("NEW "):
                return f"Set {lhs} = {rhs}"
            return f"{lhs} = {rhs}"

        # RETURN
        if hasattr(st, "returnStmt") and st.returnStmt():
            r = st.returnStmt()
            if hasattr(r, "expr") and r.expr():
                val = self.gen_expr(r.expr())
                fn = self._cur_func or "/*func*/"
                return f"{fn} = {val}\nExit Function"
            return "Exit Function"

        # BREAK
        if hasattr(st, "breakStmt") and st.breakStmt():
            return "Exit For"

        # IF
        if hasattr(st, "ifStmt") and st.ifStmt():
            return self.gen_if(st.ifStmt())

        # FOR
        if hasattr(st, "forStmt") and st.forStmt():
            return self.gen_for(st.forStmt())

        # expr stmt
        if hasattr(st, "expr") and st.expr():
            return self.gen_expr(st.expr())

        return f"' TODO stmt: {type(st).__name__}"

    def gen_if(self, ctx):
        cond = self.gen_expr(ctx.expr())
        lines = [f"If {cond} Then"]

        then_blk = ctx.thenBlock() if hasattr(ctx, "thenBlock") else (ctx.block(0) if hasattr(ctx, "block") else None)
        self.indent += 1
        for st in self.iter_block_statements(then_blk):
            lines.append("    " * self.indent + self.gen_stmt(st))
        self.indent -= 1

        # else optional
        else_blk = None
        if hasattr(ctx, "elseBlock") and ctx.elseBlock():
            else_blk = ctx.elseBlock()
        elif hasattr(ctx, "block") and len(ctx.block()) > 1:
            else_blk = ctx.block(1)

        if else_blk is not None:
            lines.append("Else")
            self.indent += 1
            for st in self.iter_block_statements(else_blk):
                lines.append("    " * self.indent + self.gen_stmt(st))
            self.indent -= 1

        lines.append("End If")
        return "\n".join(lines)

    def gen_for(self, ctx):
        # Da deine ForStmtContext kein expr() hat, bleibt es heuristisch:
        var = ctx.IDENT().getText() if hasattr(ctx, "IDENT") and ctx.IDENT() else "i"

        start_ctx = None
        end_ctx = None
        step_ctx = None

        # häufig: startExpr/toExpr/stepExpr etc.
        for nm in ("startExpr", "fromExpr", "start"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    start_ctx = fn()
                    if start_ctx is not None:
                        break
                except TypeError:
                    pass

        for nm in ("endExpr", "toExpr", "end"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    end_ctx = fn()
                    if end_ctx is not None:
                        break
                except TypeError:
                    pass

        for nm in ("stepExpr", "byExpr", "step"):
            fn = getattr(ctx, nm, None)
            if callable(fn):
                try:
                    step_ctx = fn()
                    if step_ctx is not None:
                        break
                except TypeError:
                    pass

        start = self.gen_expr(start_ctx) if start_ctx is not None else "0"
        end = self.gen_expr(end_ctx) if end_ctx is not None else "0"
        step = self.gen_expr(step_ctx) if step_ctx is not None else "1"

        lines = [f"Dim {var} As Long", f"For {var} = {start} To {end} Step {step}"]

        blk = ctx.block() if hasattr(ctx, "block") else None
        self.indent += 1
        for st in self.iter_block_statements(blk):
            lines.append("    " * self.indent + self.gen_stmt(st))
        self.indent -= 1

        lines.append("Next")
        return "\n".join(lines)

    # ---------- expressions ----------
    def gen_expr(self, e):
        if e is None:
            return "Null"

        if hasattr(e, "primary") and e.primary():
            return self.gen_primary(e.primary())

        # binary op (wenn dein AST so liefert)
        if hasattr(e, "left") and hasattr(e, "right") and hasattr(e, "op"):
            a = self.gen_expr(e.left)
            b = self.gen_expr(e.right)
            op = e.op.text
            op_map = {"AND": "And", "OR": "Or", "=": "=", "<>": "<>"}
            op2 = op_map.get(op.upper(), op)
            return f"({a} {op2} {b})"

        if hasattr(e, "getText"):
            return e.getText()

        return "Null"

    def gen_primary(self, ctx):
        if hasattr(ctx, "newExpr") and ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        if hasattr(ctx, "NUMBER") and ctx.NUMBER():
            return ctx.NUMBER().getText()

        if hasattr(ctx, "STRING") and ctx.STRING():
            return ctx.STRING().getText()

        if hasattr(ctx, "IDENT") and ctx.IDENT():
            name = ctx.IDENT().getText()
            if name.upper() == "THIS":
                return "Me"
            if name.upper() == "NIL":
                return "Nothing"
            return name

        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            return self.gen_dotted_ref(ctx.dottedRef())

        if hasattr(ctx, "callExpr") and ctx.callExpr():
            return self.gen_call(ctx.callExpr())

        return "Null"

    def gen_dotted_ref(self, ctx):
        parts = [t.getText() for t in ctx.IDENT()]
        if parts and parts[0].upper() == "THIS":
            parts[0] = "Me"
        return ".".join(parts)

    def gen_new(self, ctx):
        # VBA kann New <Class> nicht mit Args. Daher: RT.NEWOBJ("Class", args...)
        class_name = ctx.IDENT().getText()
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))
        if args:
            return f'NEWOBJ("{class_name}", ' + ", ".join(args) + ")"
        return f'NEWOBJ("{class_name}")'

    def gen_call(self, ctx):
        # callee
        if hasattr(ctx, "dottedRef") and ctx.dottedRef():
            callee = self.gen_dotted_ref(ctx.dottedRef())
        elif hasattr(ctx, "IDENT") and ctx.IDENT():
            callee = ctx.IDENT().getText()
        else:
            callee = "/*callee*/"

        # args
        args = []
        if hasattr(ctx, "argList") and ctx.argList():
            for a in ctx.argList().expr():
                args.append(self.gen_expr(a))

        return callee + "(" + ", ".join(args) + ")"
        
class DBaseToPython:
    """
    ParseTree -> Python source (calls into your runtime 'rt').
    - No direct attribute access; all member ops go through rt.GET/rt.SET/rt.CALL
    - Keeps dBase semantics in runtime, not in generated python.
    """

    def __init__(self, parser, classes=None):
        self.p = parser
        self.out = PyEmitter()
        self.classes = classes or {}  # optional: your collected ClassDefs, if you want structure

    # ---------- public ----------
    def generate(self, tree, out_path: str):
        self.out.emit("# generated by dBaseToPython (runtime-backed)")
        self.out.emit("from dBaseRuntimeFacade import RT")
        self.out.emit("")
        self.out.emit("rt = RT()")
        self.out.emit("")
        self.out.emit("def main():")
        self.out.indent()

        self.gen_input(tree)  # adapt name to your root rule

        self.out.dedent()
        self.out.emit("")
        self.out.emit("if __name__ == '__main__':")
        self.out.indent()
        self.out.emit("main()")
        self.out.dedent()

        Path(out_path).write_text(self.out.text(), encoding="utf-8")

    # ---------- root / statements ----------
    def gen_input(self, ctx):
        # input : item* EOF
        for it in ctx.item():
            self.gen_item(it)

    def gen_item(self, it):
        # Dispatch by available child rule; adapt to your grammar structure
        # item : classDecl | methodDecl | statement
        if it.statement():
            return self.gen_stmt(it.statement())
        if it.classDecl():
            return self.gen_class(it.classDecl())
        if it.methodDecl():
            return self.gen_method(it.methodDecl())

        # fallback:
        self.out.emit(f"# TODO unhandled stmt: {type(it).__name__}")

    def gen_stmt(self, st):
        if st.ifStmt():            return self.gen_if(st.ifStmt())
        if st.forStmt():           return self.gen_for(st.forStmt())
        if st.doWhileStatement():  return self.gen_do_while(st.doWhileStatement())

        if st.writeStmt():         return self.gen_write(st.writeStmt())
        if st.assignStmt():        return self.gen_assign(st.assignStmt())
        if st.localDeclStmt():     return self.gen_local_decl(st.localDeclStmt())
        if st.localAssignStmt():   return self.gen_local_assign(st.localAssignStmt())

        if st.callStmt():          return self.gen_call_stmt(st.callStmt())
        if st.exprStmt():          return self.gen_expr_stmt(st.exprStmt())

        if st.parameterStmt():     return self.gen_parameter(st.parameterStmt())
        if st.createFileStmt():    return self.gen_create_file(st.createFileStmt())
        if st.deleteStmt():        return self.gen_delete(st.deleteStmt())

        if st.withStmt():          return self.gen_with(st.withStmt())
        if st.doStmt():            return self.gen_do(st.doStmt())

        if st.returnStmt():        return self.gen_return(st.returnStmt())
        if st.breakStmt():         return self.gen_break(st.breakStmt())

        if st.classDecl():         return self.gen_class(st.classDecl())

        # bessere Debug-Ausgabe: zeig, was wirklich drinsteckt
        child0 = st.getChild(0)
        self.out.emit(f"# TODO unhandled statement: {type(child0).__name__}  text={st.getText()!r}")
    
    def gen_local_decl(self, ctx):
        # localDeclStmt : LOCAL name=IDENT ;
        name = ctx.name.text
        self.out.emit(f"rt.SET_NAME({name!r}, None)")

    def gen_local_assign(self, ctx):
        # localAssignStmt : LOCAL name=IDENT ASSIGN expr ;
        name = ctx.name.text
        rhs  = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.SET_NAME({name!r}, {rhs})")

    def gen_expr_stmt(self, ctx):
        # exprStmt : postfixExpr ;
        e = self.gen_postfix(ctx.postfixExpr())
        self.out.emit(e)

    def gen_call_stmt(self, ctx):
        # callStmt : CALL callTarget ;
        # callTarget : (SUPER DCOLON)? IDENT LPAREN argList? RPAREN ;
        # simplest: delegiere als "exprStmt" (Call ist Effekt)
        txt = ctx.callTarget().getText()
        self.out.emit(f"rt.CALL_STMT({txt!r})  # TODO: map callTarget sauber")

    def gen_do_while(self, ctx):
        # doWhileStatement : DO WHILE condition block ENDDO ;
        cond = self.gen_logical_or(ctx.condition().logicalOr())
        self.out.emit(f"while rt.TRUE({cond}):")
        self.out.indent()
        for st in ctx.block().statement():
            self.gen_stmt(st)
        self.out.dedent()

    def gen_delete(self, ctx):
        # deleteStmt : DELETE IDENT ;
        self.out.emit(f"rt.DELETE_NAME({ctx.IDENT().getText()!r})")

    def gen_create_file(self, ctx):
        # createFileStmt : CREATE FILE (expr)? ;
        arg = self.gen_expr(ctx.expr()) if ctx.expr() else "None"
        self.out.emit(f"rt.CREATE_FILE({arg})")
        
    def gen_break(self, ctx):
        self.out.emit("break")
        
    def gen_parameter(self, ctx):
        p = ctx.paramNames()
        names = [t.getText() for t in p.IDENT()]
        self.out.emit(f"rt.PARAMETER({names!r})")
    
    def new_temp(self):
        n = getattr(self, "_tmp_i", 0) + 1
        self._tmp_i = n
        return f"_t{n}"

    def gen_with(self, ctx):
        # withStmt : WITH LPAREN withTarget RPAREN withBody ENDWITH ;

        base = self.gen_with_target(ctx.withTarget())
        tmp = self.new_temp()

        # base einmal auswerten (wichtig, falls es ein Call/Expr ist)
        self.out.emit(f"{tmp} = {base}")
        self.out.emit(f"rt.PUSH_WITH({tmp})")

        # body: (withAssignStmt | withStmt | statement)*
        body = ctx.withBody()
        for ch in list(getattr(body, "children", []) or []):
            # ANTLR liefert "TerminalNode" auch als children, die ignorieren wir
            if hasattr(ch, "withAssignStmt") and ch.withAssignStmt():
                self.gen_with_assign(ch.withAssignStmt())
            elif hasattr(ch, "withStmt") and ch.withStmt():
                self.gen_with(ch.withStmt())
            elif hasattr(ch, "statement") and ch.statement():
                self.gen_stmt(ch.statement())
            else:
                # manchmal ist ch direkt der Context-Typ
                t = type(ch).__name__
                if t.endswith("WithAssignStmtContext"):
                    self.gen_with_assign(ch)
                elif t.endswith("WithStmtContext"):
                    self.gen_with(ch)
                elif t.endswith("StatementContext"):
                    self.gen_stmt(ch)
                else:
                    pass

        self.out.emit("rt.POP_WITH()")


    def gen_with_target(self, ctx):
        # withTarget : THIS | dottedRef | IDENT | postfixExpr ;
        if ctx.THIS():
            return "this"

        if ctx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(ctx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"

        if ctx.IDENT():
            # Variablenzugriff: runtime-semantisch (Scoping/WITH)
            name = ctx.IDENT().getText()
            return f"rt.GET_NAME({name!r})"

        if ctx.postfixExpr():
            # postfix kann call/member enthalten -> dein gen_postfix liefert runtime-Ausdruck
            return self.gen_postfix(ctx.postfixExpr())

        return f"rt.PRIMARY({ctx.getText()!r})"


    def gen_with_assign(self, ctx):
        # withAssignStmt : withLvalue ASSIGN expr ;
        path = [t.getText() for t in ctx.withLvalue().IDENT()]  # z.B. ["top"] oder ["pushbutton1","width"]
        rhs = self.gen_expr(ctx.expr())
        self.out.emit(f"rt.WITH_SET({path!r}, {rhs})")
    # ---------- WRITE ----------
    def gen_write_arg(self, actx):
        # writeArg : STRING | dottedRef | expr ;
        if actx.STRING():
            return actx.STRING().getText()
        if actx.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(actx.dottedRef())
            return f"rt.GET('{base_expr.upper()}', {path})"
        if actx.expr():
            return self.gen_expr(actx.expr())
        return f"rt.PRIMARY({actx.getText()!r})"
        
    def gen_write(self, ctx):
        # writeStmt : WRITE writeArg (PLUS writeArg)* ;
        parts = [self.gen_write_arg(a) for a in ctx.writeArg()]

        if not parts:
            self.out.emit("rt.WRITE('')")   # sollte praktisch nie passieren
            return

        # WRITE a + b + c  -> runtime-konforme Verkettung
        expr = parts[0]
        for p in parts[1:]:
            expr = f"rt.BINOP({expr}, '+', {p})"

        self.out.emit(f"rt.WRITE({expr})")

    # ---------- assignment ----------
    def lvalue_chain_from_postfix(self, pe):
        # postfixExpr : primary ( '(' ... ')' | ('.'|'::') IDENT )*
        chain = [pe.primary().getText()]
        i = 1
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()

            if ch == '.':
                chain.append(pe.getChild(i + 1).getText())
                i += 2
                continue

            if ch == '(':
                raise Exception(f"LVALUE darf keinen Call enthalten: {pe.getText()}")

            i += 1
        return chain
        
    def gen_assign(self, ctx):
        rhs = self.gen_expr(ctx.expr())
        lv = ctx.lvalue()

        # 1) dottedRef direkt (THIS.X.Y ...)
        if lv.dottedRef():
            base_expr, path = self.gen_dotted_ref_parts(lv.dottedRef())
            self.out.emit(f"rt.SET({base_expr}, {path}, {rhs})")
            return

        # 2) postfixExpr als LHS: kann "Y" oder "THIS.X.Y" sein
        pe = lv.postfixExpr()
        if pe:
            chain = self.lvalue_chain_from_postfix(pe)   # z.B. ["Y"] oder ["THIS","PushButton1","Text"]

            if len(chain) == 1:
                # wichtig: über Runtime setzen, damit WITH/Scopes wie im Interpreter funktionieren
                self.out.emit(f"rt.SET_NAME({chain[0]!r}, {rhs})")
                return

            # Kette: base + path
            head = chain[0]
            if head.upper() == "THIS":
                base_expr = "this"
                path = chain[1:]
            else:
                base_expr = self.norm_local(head)
                path = chain[1:]

            self.out.emit(f"rt.SET({base_expr}, {path!r}, {rhs})")
            return

        self.out.emit(f"# TODO unsupported lvalue: {lv.getText()}")

    # ---------- IF ----------
    def gen_if(self, ctx):
        # ifStmt : IF expr block (ELSE block)? ENDIF ;
        cond = self.gen_expr(ctx.expr())
        self.out.emit(f"if rt.TRUE({cond}):")
        self.out.indent()

        # then-block
        then_block = ctx.block(0)
        for st in then_block.statement():
            self.gen_stmt(st)

        self.out.dedent()

        # else-block (optional)
        if ctx.ELSE():
            self.out.emit("else:")
            self.out.indent()

            else_block = ctx.block(1)
            for st in else_block.statement():
                self.gen_stmt(st)

            self.out.dedent()

    # ---------- FOR ----------
    def gen_for(self, ctx):
        # forStmt : FOR IDENT ASSIGN expr TO expr (STEP expr)? block ENDFOR ;
        
        var = self.norm_local(ctx.IDENT().getText())
        
        start = ctx.numberExpr(0).getText()
        end   = ctx.numberExpr(1).getText()
        step  = ctx.numberExpr(2).getText() if ctx.STEP() else "1"
        
        # dBase TO ist inklusiv -> Runtime-Helper
        self.out.emit(f"for {var} in rt.RANGE_INCL({start}, {end}, {step}):")
        self.out.indent()
        for st in ctx.block().statement():
            self.gen_stmt(st)
        self.out.dedent()

    # ---------- RETURN ----------
    def gen_return(self, ctx):
        if ctx.expr():
            self.out.emit(f"return {self.gen_expr(ctx.expr())}")
        else:
            self.out.emit("return")

    # ---------- CLASS / METHOD ----------
    def gen_class(self, ctx):
        cname = ctx.name.text  # adapt
        parent = ctx.parent.text if ctx.parent else "OBJECT"

        self.out.emit(f"class {self.norm_class(cname)}({self.norm_class(parent)}):")
        self.out.indent()
        self.out.emit("def __init__(self, *args):")
        self.out.indent()
        self.out.emit("super().__init__()")
        self.out.emit("self._instance = rt.MAKE_INSTANCE(self, args)")  # or however you represent instances
        self.out.dedent()
        self.out.emit("")

        # properties/methods in body: adapt to your classBody structure
        body = ctx.classBody()
        for ch in list(getattr(body, "children", []) or []):
            if hasattr(ch, "methodDecl") and ch.methodDecl():
                self.gen_method(ch.methodDecl())
            else:
                # propertyDecl / init statements -> put into __init__ or Init method
                pass

        self.out.dedent()
        self.out.emit("")

    def gen_method(self, mctx):
        mname = mctx.IDENT().getText()
        params = [p.getText() for p in mctx.paramList().IDENT()] if mctx.paramList() else []
        pyparams = ", ".join(["self"] + [self.norm_local(p) for p in params])

        self.out.emit(f"def {self.norm_method(mname)}({pyparams}):")
        self.out.indent()
        # inside methods, dBase THIS maps to `self` (or `this`)
        self.out.emit("this = self")
        # method statements:
        for st in mctx.block().statement():
            self.gen_stmt(st)
        self.out.dedent()
        self.out.emit("")


    def gen_new(self, ctx):
        class_name = ctx.IDENT().getText()
        args = [self.gen_expr(e) for e in ctx.argList().expr()] if ctx.argList() else []
        return f"rt.NEW({class_name!r}, {', '.join(args)})"

    def gen_call(self, ctx):
        # something like dottedRef '(' args ')'
        base_expr, path = self.gen_dotted_ref_parts(ctx.dottedRef())
        args = [self.gen_expr(e) for e in ctx.argList().expr()] if ctx.argList() else []
        return f"rt.CALL({base_expr}, {path}, [{', '.join(args)}])"

    def gen_dotted_ref_parts(self, dctx):
        # e.g. THIS.PushButton1.Text -> base=this, path=["PushButton1","Text"]
        parts = [t.getText() for t in dctx.IDENT()]

        head = parts[0]
        if head.upper() == "THIS":
            base = "this"
            path = parts[1:]
        else:
            base = self.norm_local(head)
            path = parts[1:]

        return base, repr(path)

    # ---------- naming ----------
    def norm_local(self, name: str) -> str:
        # conservative: keep letters/digits/_ and lower it
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name).lower()

    def norm_class(self, name: str) -> str:
        # keep it simple; you can make PascalCase if you like
        return "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name)

    def norm_method(self, name: str) -> str:
        return self.norm_local(name)
        
        
    def gen_expr(self, ctx):
        # expr : logicalOr ;
        return self.gen_logical_or(ctx.logicalOr())

    def gen_logical_or(self, ctx):
        # logicalOr : logicalAnd (OR logicalAnd)* ;
        parts = [self.gen_logical_and(x) for x in ctx.logicalAnd()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'OR', {rhs})"
        return out

    def gen_logical_and(self, ctx):
        # logicalAnd : logicalNot (AND logicalNot)* ;
        parts = [self.gen_logical_not(x) for x in ctx.logicalNot()]
        out = parts[0]
        for rhs in parts[1:]:
            out = f"rt.BINOP({out}, 'AND', {rhs})"
        return out

    def gen_logical_not(self, ctx):
        # logicalNot : NOT logicalNot | comparison ;
        if ctx.NOT():
            inner = self.gen_logical_not(ctx.logicalNot())
            return f"rt.UNOP('NOT', {inner})"
        return self.gen_comparison(ctx.comparison())

    def gen_comparison(self, ctx):
        # comparison : additiveExpr (compareOp additiveExpr)? ;
        left = self.gen_additive(ctx.additiveExpr(0))
        if ctx.compareOp():
            op = ctx.compareOp().getText()
            right = self.gen_additive(ctx.additiveExpr(1))
            return f"rt.BINOP({left}, {op!r}, {right})"
        return left

    def gen_additive(self, ctx):
        # additiveExpr : multiplicativeExpr ((PLUS|MINUS) multiplicativeExpr)* ;
        terms = [self.gen_multiplicative(x) for x in ctx.multiplicativeExpr()]
        out = terms[0]
        # Operatoren stehen als Token zwischen den Termen -> über getChildren laufen
        # Einfacher: Text-basiert paaren (robust genug für Start)
        # Wir bauen anhand der Kindersequenz: term (op term)*.
        children = list(ctx.getChildren())
        i = 1
        while i < len(children):
            op = children[i].getText()
            rhs = terms[(i + 1) // 2]
            out = f"rt.BINOP({out}, {op!r}, {rhs})"
            i += 2
        return out

    def gen_multiplicative(self, ctx):
        # multiplicativeExpr : postfixExpr ((STAR|SLASH) postfixExpr)* ;
        factors = [self.gen_postfix(x) for x in ctx.postfixExpr()]
        out = factors[0]
        children = list(ctx.getChildren())
        i = 1
        while i < len(children):
            op = children[i].getText()
            rhs = factors[(i + 1) // 2]
            out = f"rt.BINOP({out}, {op!r}, {rhs})"
            i += 2
        return out

    def gen_postfix(self, ctx):
        # postfixExpr : primary ( LPAREN argList? RPAREN | (DOT|DCOLON) IDENT )* ;
        cur = self.gen_primary(ctx.primary())

        # Wir laufen über die restlichen Kinder und erkennen Muster:
        # ( ... )  oder . IDENT / :: IDENT
        kids = list(ctx.getChildren())
        k = 1
        while k < len(kids):
            t = kids[k].getText()

            if t == "(":
                # call: ( argList? )
                # argList ist optional und sitzt zwischen '(' und ')'
                args = []
                # wenn nächstes Kind nicht ')', ist es argList
                if kids[k + 1].getText() != ")":
                    # kids[k+1] ist der argList-Context
                    argctx = kids[k + 1]
                    args = [self.gen_expr(e) for e in argctx.expr()]
                    k += 1  # argList "verbraucht"
                cur = f"rt.CALL_ANY({cur}, [{', '.join(args)}])"
                k += 2  # überspringe ')'
                continue

            if t in (".", "::"):
                name = kids[k + 1].getText()
                cur = f"rt.GET_ATTR({cur}, {name!r})"
                k += 2
                continue

            # fallback (sollte selten passieren)
            k += 1

        return cur

    def gen_primary(self, ctx):
        # primary:
        # handlerList | newExpr | memberExpr | literal | THIS | SUPER | FLOAT | NUMBER
        # | IDENT | STRING | BRACKET_STRING | '(' expr ')'
        if ctx.THIS():
            return "this"

        if ctx.SUPER():
            return "super_obj"  # falls du es nutzt; sonst an runtime delegieren

        if ctx.STRING():
            return ctx.STRING().getText()

        if ctx.BRACKET_STRING():
            return ctx.BRACKET_STRING().getText()

        if ctx.NUMBER():
            return ctx.NUMBER().getText()

        if ctx.FLOAT():
            return ctx.FLOAT().getText()

        if ctx.IDENT():
            return self.norm_local(ctx.IDENT().getText())

        if ctx.literal():
            return ctx.literal().getText()

        if ctx.newExpr():
            return self.gen_new(ctx.newExpr())

        # ( expr )
        if ctx.expr():
            return self.gen_expr(ctx.expr())

        # memberExpr/handlerList erstmal roh:
        return f"rt.PRIMARY({ctx.getText()!r})"
        
# ---------------------------------------------------------------------------
# Qt application stuff: Editor ...
# ---------------------------------------------------------------------------
class DBaseHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # --- Formate ---
        self.fmt_keyword = QTextCharFormat()
        self.fmt_keyword.setFontWeight(QFont.Bold)
        self.fmt_keyword.setForeground(QColor(200, 200, 0))  # schwarz

        self.fmt_comment = QTextCharFormat()
        self.fmt_comment.setForeground(QColor(0, 148, 0))  # grün

        # --- Keywords (nach Bedarf erweitern) ---
        keywords = [
            "FOR", "ENDFOR", "CLASS", "ENDCLASS", "METHOD", "ENDMETHOD",
            "IF", "ENDIF", "ELSE", "DO", "WHILE", "ENDDO",
            "RETURN", "LOCAL", "PARAMETER", "WITH", "ENDWITH",
            "NEW", "OF", "OBJECT", "THIS", "SUPER", "TRUE", "FALSE"
        ]

        self.rules = []
        for kw in keywords:
            # \bKW\b = ganzes Wort, case-insensitive
            rx = QRegExp(rf"\b{kw}\b", Qt.CaseInsensitive)
            self.rules.append((rx, self.fmt_keyword))

        # --- Line comments: //, **, && bis Zeilenende ---
        self.rules.append((QRegExp(r"//[^\n]*"), self.fmt_comment))
        self.rules.append((QRegExp(r"\*\*[^\n]*"), self.fmt_comment))
        self.rules.append((QRegExp(r"&&[^\n]*"), self.fmt_comment))

        # --- Block comments: /* ... */ (mehrzeilig) ---
        self.block_start = QRegExp(r"/\*")
        self.block_end   = QRegExp(r"\*/")

    def highlightBlock(self, text: str):
        # 1) normale Regeln (Keywords + Single-line comments)
        for rx, fmt in self.rules:
            i = rx.indexIn(text, 0)
            while i >= 0:
                length = rx.matchedLength()
                self.setFormat(i, length, fmt)
                i = rx.indexIn(text, i + length)

        # 2) Block comments mehrzeilig
        self.setCurrentBlockState(0)

        start = 0
        if self.previousBlockState() != 1:
            start = self.block_start.indexIn(text, 0)
        else:
            start = 0

        while start >= 0:
            end = self.block_end.indexIn(text, start)
            if end == -1:
                # Kommentar geht in nächste Zeile weiter
                self.setCurrentBlockState(1)
                length = len(text) - start
            else:
                length = (end - start) + self.block_end.matchedLength()

            self.setFormat(start, length, self.fmt_comment)

            if end == -1:
                break
            start = self.block_start.indexIn(text, start + length)

class BreakpointArea(QWidget):
    def __init__(self, editor: "CodeEditor"):
        super().__init__(editor)
        self.editor = editor
        self.setCursor(Qt.PointingHandCursor)

    def sizeHint(self):
        return QSize(self.editor.breakpoint_area_width(), 0)

    def paintEvent(self, event):
        self.editor.paint_breakpoint_area(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.editor.toggle_breakpoint_at_y(event.pos().y())
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

class LineNumberArea(QWidget):
    def __init__(self, editor: "CodeEditor"):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.paint_line_number_area(event)

class TitleBar(QWidget):
    def __init__(self, parent_dialog: QDialog, title: str, icon: QIcon = None):
        super().__init__(parent_dialog)
        self.dlg = parent_dialog
        self._drag_pos = None
        self.setFixedHeight(34)

        # --- left icon + title ---
        self.iconLabel = QLabel()
        self.iconLabel.setFixedSize(22, 22)
        if icon is not None:
            self.iconLabel.setPixmap(icon.pixmap(18, 18))
        self.iconLabel.setCursor(Qt.PointingHandCursor)

        self.titleLabel = QLabel(title)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # --- window buttons ---
        self.btnMin   = QToolButton()
        self.btnMax   = QToolButton()
        self.btnClose = QToolButton()

        # Standard-Icons (plattformabhängig, aber okay). Alternativ eigene SVGs setzen.
        style = self.style()
        self.btnMin.setIcon  (style.standardIcon(style.SP_TitleBarMinButton))
        self.btnMax.setIcon  (style.standardIcon(style.SP_TitleBarMaxButton))
        self.btnClose.setIcon(style.standardIcon(style.SP_TitleBarCloseButton))

        self.btnMin  .clicked.connect(self.dlg.showMinimized)
        self.btnMax  .clicked.connect(self._toggle_max_restore)
        self.btnClose.clicked.connect(self.dlg.close)

        # Layout
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 0, 8, 0)
        lay.setSpacing(8)
        lay.addWidget(self.iconLabel)
        lay.addWidget(self.titleLabel)
        lay.addWidget(self.btnMin)
        lay.addWidget(self.btnMax)
        lay.addWidget(self.btnClose)

        # Styling: Verlauf blau->weiß + dunkler Rahmen
        self.setStyleSheet(r"""
TitleBar {
    border: 1px solid #3a3a3a;
    border-bottom: 1px solid #2a2a2a;
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #1a4fa3,
        stop:1 #f2f6ff
    );
}
QLabel {
    color: #0b0f18;
    font-weight: 600;
}
QToolButton {
    border: 0px;
    padding: 6px;
    border-radius: 6px;
    background: transparent;
}
QToolButton:hover {
    background: rgba(0,0,0,0.10);
}
QToolButton:pressed {
    background: rgba(0,0,0,0.18);
}
""")

    def _toggle_max_restore(self):
        if self.dlg.isMaximized():
            self.dlg.showNormal()
        else:
            self.dlg.showMaximized()

    # --- close on double click icon ---
    def mouseDoubleClickEvent(self, event):
        # optional: Doppelklick auf TitleBar toggelt maximieren
        if event.button() == Qt.LeftButton:
            self._toggle_max_restore()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def eventFilter(self, obj, event):
        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Drag starten (global Position merken)
            self._drag_pos = event.globalPos() - self.dlg.frameGeometry().topLeft()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and (event.buttons() & Qt.LeftButton):
            if not self.dlg.isMaximized():
                self.dlg.move(event.globalPos() - self._drag_pos)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def _icon_double_clicked(self):
        self.dlg.close()

    def showEvent(self, event):
        # Doppelklick auf IconLabel => schließen
        self.iconLabel.mouseDoubleClickEvent = lambda e: (self.dlg.close(), e.accept())
        super().showEvent(event)

class IconScrollBarStyle(QProxyStyle):
    def __init__(self, base_style=None):
        super().__init__(base_style)
        self.track      = QColor("#081a33")  # navy
        self.btn_bg     = QColor("#061246")  # dunkler
        self.thumb      = QColor("#2b6cb0")  # blau
        self.border     = QColor("#0f2a4a")
        self.icon_color = QColor("#c9b458")  # gelb

        # Optional: eine Icon-Font laden (z.B. FontAwesome/Material)
        # Wenn du eine ttf in Resources hast: ":/fonts/YourIconFont.ttf"
        self.icon_font = QFont()
        self.icon_font.setPointSize(10)
        self.icon_font.setBold(True)

        # Fallback-Glyphs (funktionieren ohne Extra-Font)
        self.g_up = "▲"
        self.g_down = "▼"
        self.g_left = "◀"
        self.g_right = "▶"

        # Wenn du FontAwesome nutzt, setze z.B.:
        # self.g_up = "\uf077"   # chevron-up
        # self.g_down = "\uf078"
        # self.g_left = "\uf053"
        # self.g_right = "\uf054"

    # --- Größen: 16px dick, Thumb immer 26px ---
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QStyle.PM_ScrollBarExtent:
            return 21
        if metric == QStyle.PM_ScrollBarSliderMin:
            return 32  # min thumb length
        return super().pixelMetric(metric, option, widget)

    def drawComplexControl(self, control, option: QStyleOptionComplex, painter: QPainter, widget=None):
        if control != QStyle.CC_ScrollBar:
            return super().drawComplexControl(control, option, painter, widget)

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Subcontrol-Rects holen
        sub_line = self.subControlRect(control, option, QStyle.SC_ScrollBarSubLine, widget)
        add_line = self.subControlRect(control, option, QStyle.SC_ScrollBarAddLine, widget)
        groove   = self.subControlRect(control, option, QStyle.SC_ScrollBarGroove, widget)
        slider   = self.subControlRect(control, option, QStyle.SC_ScrollBarSlider, widget)

        # Track/Groove
        painter.fillRect(option.rect, self.track)
        painter.fillRect(groove, self.track)

        # Buttons
        painter.fillRect(sub_line, self.btn_bg)
        painter.fillRect(add_line, self.btn_bg)

        painter.setPen(self.border)
        painter.drawRect(sub_line.adjusted(0, 0, -1, -1))
        painter.drawRect(add_line.adjusted(0, 0, -1, -1))
        painter.drawRect(option.rect.adjusted(0, 0, -1, -1))

        # Thumb (fix 26px wird über Metrics erzwungen; Qt berechnet slider-Rect)
        painter.setPen(self.border)
        painter.setBrush(self.thumb)
        r = slider.adjusted(2, 2, -2, -2)
        painter.drawRoundedRect(r, 6, 6)

        # Pfeil-Glyphs zeichnen
        painter.setPen(self.icon_color)
        painter.setFont(self.icon_font)

        if option.state & QStyle.State_Horizontal:
            painter.drawText(sub_line, Qt.AlignCenter, self.g_left)
            painter.drawText(add_line, Qt.AlignCenter, self.g_right)
        else:
            painter.drawText(sub_line, Qt.AlignCenter, self.g_up)
            painter.drawText(add_line, Qt.AlignCenter, self.g_down)

        painter.restore()

    # Optional: wenn du willst, dass der Thumb wirklich NIE > 26 wird:
    # Qt kann bei wenig Inhalt größere Slider zeichnen; dafür “max” müssen wir tricksen.
    # Am stabilsten: SliderRect kürzen:
    def subControlRect(self, control, option, subControl, widget=None):
        rect = super().subControlRect(control, option, subControl, widget)
        if control == QStyle.CC_ScrollBar and subControl == QStyle.SC_ScrollBarSlider:
            # Slider auf exakt 26 px kürzen (zentriert in seiner berechneten Position)
            if option.state & QStyle.State_Horizontal:
                w = 42
                cx = rect.center().x()
                rect.setLeft(cx - w // 2)
                rect.setRight(rect.left() + w - 1)
            else:
                h = 42
                cy = rect.center().y()
                rect.setTop(cy - h // 2)
                rect.setBottom(rect.top() + h - 1)
        return rect
        
class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self._line_number_area = LineNumberArea(self)

        self._breakpoints = set()  # speichert blockNumber() (0-basiert)
        
        # --- Editor-Farben: Navy Hintergrund + dunkleres Gelb für Text ---
        pal = self.palette()
        pal.setColor(QPalette.Base, QColor("#081a33"))        # Hintergrund (navy)
        pal.setColor(QPalette.Text, QColor("#c9b458"))        # Text (dunkleres Gelb)
        pal.setColor(QPalette.Highlight, QColor("#274b8a"))   # Selection Hintergrund
        pal.setColor(QPalette.HighlightedText, QColor("#f0e6b0"))
        self.setPalette(pal)

        # optional: Cursor + Selection im QSS sauberer kontrollieren
        self.setStyleSheet("""
        QPlainTextEdit {
            background: #081a33;
            color: #c9b458;
            selection-background-color: #274b8a;
            selection-color: #f0e6b0;
        }
        """)
        self.setStyleSheet(self.styleSheet() + "\n" + APP_DARK_QSS)
        
        self.breakpointArea = BreakpointArea(self)
        self.lineNumberArea = LineNumberArea(self)
        
        self.blockCountChanged.connect(self._update_gutter_widths)
        self.updateRequest.connect(self._update_gutters_on_scroll)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_gutter_widths()
        self._highlight_current_line()

    # ---------- API / State ----------
    def breakpoints(self):
        """Gibt Breakpoints als 1-basierte Zeilennummern zurück."""
        return sorted(b + 1 for b in self._breakpoints)

    # ---------- Layout: zwei Gutters ----------
    def breakpoint_area_width(self) -> int:
        return 14  # schmaler Gutter für roten Punkt

    def line_number_area_width(self) -> int:
        digits = len(str(max(1, self.blockCount())))
        fm = QFontMetrics(self.font())
        # etwas Padding
        return 6 + fm.horizontalAdvance("9") * digits + 8

    def _update_gutter_widths(self):
        left = self.breakpoint_area_width() + self.line_number_area_width()
        self.setViewportMargins(left, 0, 0, 0)
        self._reposition_gutters()
        self.viewport().update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._reposition_gutters()

    def _reposition_gutters(self):
        cr = self.contentsRect()
        bpw = self.breakpoint_area_width()
        lnw = self.line_number_area_width()

        self.breakpointArea.setGeometry(QRect(cr.left(), cr.top(), bpw, cr.height()))
        self.lineNumberArea.setGeometry(QRect(cr.left() + bpw, cr.top(), lnw, cr.height()))

    def _update_gutters_on_scroll(self, rect, dy):
        if dy:
            self.breakpointArea.scroll(0, dy)
            self.lineNumberArea.scroll(0, dy)
        else:
            self.breakpointArea.update(0, rect.y(), self.breakpointArea.width(), rect.height())
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self._update_gutter_widths()

    # ---------- Painting ----------
    def paint_breakpoint_area(self, event):
        painter = QPainter(self.breakpointArea)
        painter.fillRect(event.rect(), QColor("#1b1b1b"))  # Hintergrund

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        # rote Punkte
        dot_color = QColor("#d32f2f")

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                if block_number in self._breakpoints:
                    # Kreis zentriert im Breakpoint-Gutter
                    w = self.breakpointArea.width()
                    h = int(self.blockBoundingRect(block).height())
                    diameter = min(10, w - 2, h - 4)
                    x = (w - diameter) // 2
                    y = top + (h - diameter) // 2

                    painter.setPen(Qt.NoPen)
                    painter.setBrush(dot_color)
                    painter.setRenderHint(QPainter.Antialiasing, True)
                    painter.drawEllipse(x, y, diameter, diameter)

            block = block.next()
            block_number += 1
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())

    def paint_line_number_area(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#202020"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        painter.setPen(QColor("#9e9e9e"))

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number_text = str(block_number + 1)
                painter.drawText(
                    0, top,
                    self.lineNumberArea.width() - 4, int(self.blockBoundingRect(block).height()),
                    Qt.AlignRight | Qt.AlignVCenter,
                    number_text
                )
            block = block.next()
            block_number += 1
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())

    # ---------- Toggle per Doppelklick ----------
    def toggle_breakpoint_at_y(self, y_in_area: int):
        """Ermittelt Block unter y (Viewport-Koordinate) und toggelt Breakpoint."""
        # y aus BreakpointArea -> y in Viewport
        y_view = y_in_area
        block = self.firstVisibleBlock()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid():
            if top <= y_view < bottom and block.isVisible():
                bn = block.blockNumber()
                if bn in self._breakpoints:
                    self._breakpoints.remove(bn)
                else:
                    self._breakpoints.add(bn)
                self.breakpointArea.update()
                return

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())

    # ---------- Optional: current line highlight ----------
    def _highlight_current_line(self):
        selections = []

        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()  # <-- statt QPlainTextEdit.ExtraSelection

            sel.format.setBackground(QColor("#0b2a52"))  # dunkleres Blau
            sel.format.setForeground(QColor("#c9b458"))  # Gelb
            sel.format.setProperty(QTextFormat.FullWidthSelection, True)

            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            selections.append(sel)

        self.setExtraSelections(selections)

class FileEditorWindow(QDialog):
    def __init__(self, parent, initial_path: str = "", initial_text: str = ""):
        super().__init__(parent)
        self.parent = parent
        
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        
        self.setWindowTitle("CodeEditor")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        # Optional: eigenes Icon setzen
        icon = self.windowIcon()  # oder QIcon("dein_icon.png")

        self.titlebar = TitleBar(self, "CodeEditor", icon)

        # Content Frame (Rahmen + Hintergrund)
        self.frame = QFrame()
        self.frame.setObjectName("WindowFrame")

        content_layout = QVBoxLayout(self.frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        
        # Splitter: links Tree, rechts Editor
        self.splitter = QSplitter(Qt.Horizontal, self)
        
        # --- TreeView links ---
        self.tree = QTreeView(self.splitter)
        
        # Dummy Model (später kannst du hier Klassen/Methoden/etc. einfüllen)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Struktur"])
        
        root = model.invisibleRootItem()
        
        root.appendRow(QStandardItem("CLASS ParentForm"))
        root.appendRow(QStandardItem("METHOD Init"))
        
        self.tree.setModel(model)
        self.tree.expandAll()
        
        vlayout = QVBoxLayout(self)

        self.ed = self._create_editor()
        self.ed.setFont(QFont("Consolas", 10))

        if initial_path:
            try:
                with open(initial_path, "r", encoding="utf-8") as f:
                    initial_text = f.read()
                    f.close()
            except Exception as e:
                raise Exception(e)
                
        self.highlighter = DBaseHighlighter(self.ed.document())
        
        # Splitter-Verhältnisse
        self.splitter.setStretchFactor(0, 0)  # Tree
        self.splitter.setStretchFactor(1, 1)  # Editor
        self.splitter.setSizes([220, 800])
        
        self._path = initial_path or ""
        self._set_text(initial_text or "")
        self._update_title()
        
        self._create_actions()
        
        self.mb = self._create_menus()
        self.tb = self._create_toolbar()
        self.sb = self._create_statusbar()
        
        vlayout.addWidget(self.titlebar)
        vlayout.addWidget(self.fname)
        
        vlayout.addWidget(self.mb)
        vlayout.addWidget(self.tb)
        vlayout.addWidget(self.splitter)
        vlayout.addWidget(self.sb)

        vlayout.setContentsMargins(0, 0, 0, 0)
        
        content_layout.addLayout(vlayout)
        self.setLayout(vlayout)
        
        self.ed.cursorPositionChanged.connect(self._update_cursor_status)
        self.ed.document().modificationChanged.connect(lambda _: self._update_title())
        self._update_cursor_status()

    # ---------- UI building ----------
    def _create_editor(self):
        editor = CodeEditor(self.splitter)
        return editor
        
    def _create_actions(self):
        # File
        self.act_new = QAction("Neu", self)
        self.act_new.setShortcut("Ctrl+N")
        self.act_new.triggered.connect(self.file_new)

        self.act_save = QAction("Speichern", self)
        self.act_save.setShortcut("Ctrl+S")
        self.act_save.triggered.connect(self.file_save)

        self.act_save_as = QAction("Speichern unter…", self)
        self.act_save_as.setShortcut("Ctrl+Shift+S")
        self.act_save_as.triggered.connect(self.file_save_as)

        self.act_exit = QAction("Beenden", self)
        self.act_exit.setShortcut("Alt+F4")
        self.act_exit.triggered.connect(self.close)

        # Edit
        self.act_undo = QAction("Undo", self)
        self.act_undo.setShortcut("Ctrl+Z")
        self.act_undo.triggered.connect(self.ed.undo)

        self.act_redo = QAction("Redo", self)
        self.act_redo.setShortcut("Ctrl+Y")
        self.act_redo.triggered.connect(self.ed.redo)

        self.act_cut = QAction("Cut", self)
        self.act_cut.setShortcut("Ctrl+X")
        self.act_cut.triggered.connect(self.ed.cut)

        self.act_copy = QAction("Copy", self)
        self.act_copy.setShortcut("Ctrl+C")
        self.act_copy.triggered.connect(self.ed.copy)

        self.act_paste = QAction("Paste", self)
        self.act_paste.setShortcut("Ctrl+V")
        self.act_paste.triggered.connect(self.ed.paste)

        self.act_select_all = QAction("Select All", self)
        self.act_select_all.setShortcut("Ctrl+A")
        self.act_select_all.triggered.connect(self.ed.selectAll)

        # Help
        self.act_about = QAction("Über", self)
        self.act_about.triggered.connect(self.help_about)

    def _create_menus(self):
        mb = QMenuBar(self)

        m_file = mb.addMenu("Datei")
        m_file.addAction(self.act_new)
        m_file.addSeparator()
        m_file.addAction(self.act_save)
        m_file.addAction(self.act_save_as)
        m_file.addSeparator()
        m_file.addAction(self.act_exit)

        m_edit = mb.addMenu("Bearbeiten")
        m_edit.addAction(self.act_undo)
        m_edit.addAction(self.act_redo)
        m_edit.addSeparator()
        m_edit.addAction(self.act_cut)
        m_edit.addAction(self.act_copy)
        m_edit.addAction(self.act_paste)
        m_edit.addSeparator()
        m_edit.addAction(self.act_select_all)

        m_help = mb.addMenu("Hilfe")
        m_help.addAction(self.act_about)
        
        return mb

    def _create_toolbar(self):
        tb = QToolBar("Datei", self)
        tb.setMovable(False)
        tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        tb.addAction(self.act_new)
        tb.addAction(self.act_save)
        tb.addAction(self.act_save_as)
        
        return tb

    def _create_statusbar(self):
        sb = QStatusBar(self)
        sb.showMessage("Bereit")
        return sb

    # ---------- File operations ----------
    def maybe_save(self) -> bool:
        if not self.ed.document().isModified():
            return True
        res = QMessageBox.question(
            self,
            "Ungespeicherte Änderungen",
            "Du hast ungespeicherte Änderungen. Speichern?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if res == QMessageBox.Yes:
            return self.file_save()
        if res == QMessageBox.No:
            return True
        return False

    def file_new(self):
        if not self.maybe_save():
            return
        self._path = ""
        self._set_text("")
        self.ed.document().setModified(False)
        self._update_title()

    def file_save(self) -> bool:
        if not self._path:
            return self.file_save_as()
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                f.write(self.ed.toPlainText())
            self.ed.document().setModified(False)
            self.sb.showMessage(f"Gespeichert: {self._path}", 3000)
            self._update_title()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte nicht speichern:\n{e}")
            return False

    def file_save_as(self) -> bool:
        path, _ = QFileDialog.getSaveFileName(self, "Speichern unter", self._path or "", "Alle Dateien (*.*)")
        if not path:
            return False
        self._path = path
        return self.file_save()

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    # ---------- Helpers ----------
    def _set_text(self, text: str):
        self.ed.setPlainText(text)

    def _update_title(self):
        name = self._path if self._path else "Unbenannt"
        star = " *" if self.ed.document().isModified() else ""
        self.setWindowTitle(f"{name}{star} - Editor")

    def _update_cursor_status(self):
        tc = self.ed.textCursor()
        line = tc.blockNumber() + 1
        col = tc.positionInBlock() + 1
        self.sb.showMessage(f"Zeile {line}, Spalte {col}")

    def help_about(self):
        QMessageBox.information(self, "Über", "Einfacher QPlainTextEdit-Editor mit Zeilennummern.\n(Generiert im dBaseRunner)")
        
# ---------------------------------------------------------------------------
# ExecVisitor - Interpreter for dBase DSL ...
# ---------------------------------------------------------------------------
class ExecVisitor(dBaseParserVisitor):
    def __init__(self):
        super().__init__()
        self.output  = []  # sammelt Ausgaben (statt direkt printen)
        self._mode = ""
        
        self.vars: Dict[str, object] = {}   # normale Variablen
        self.this_obj: object | None = None # aktuelles "this"
        
        self.globals = {}
        self._scopes = [{}]        # stack of dicts
        
        self.env = ScopeStack()
        self.classes = {}          # className -> {"parent": str, "methods": {methodName: MethodDef}}
        
        self.classes["OBJECT"] = ClassDef(
            parent     = None,
            name       = "OBJECT",
            methods    = {"POPS": ""}
        )
        
        self.classes["PUSHBUTTON"] = ClassDef(
            parent     = "OBJECT",
            name       = "PUSHBUTTON",
            methods    = {"MOPS": ""},
            default_props = {       # <-- neu
                "path": "",
                "handle": None,
                "isopen": False,
                "mode": "",
                "eof": False,
                "pos": 0,
            }
        )
        
        self.frames: list[Frame] = [Frame(name="<global>")]  # globaler Frame
        self._current_class = None
        
        self.this_stack = []
        self.with_stack      : list[object] = []
        self.with_stack_owner: list[object] = []

    @property
    def current_frame(self) -> Frame:
        return self.frames[-1]
    
    @property
    def current_with_base(self):
        return self.with_stack[-1] if self.with_stack else None

    def push_frame(self, name: str, args: list[Any] | None = None) -> None:
        self.frames.append(Frame(name=name, args=list(args or [])))

    def pop_frame(self) -> Frame:
        if len(self.frames) <= 1:
            raise RuntimeError("Cannot pop global frame")
        return self.frames.pop()
    
    def push_this(self, inst: Instance):
        self.this_stack.append(inst)

    def pop_this(self):
        self.this_stack.pop()

    def cur_this(self) -> Instance:
        if not self.this_stack:
            raise RuntimeError("THIS ist nicht gesetzt")
        return self.this_stack[-1]

    def bind_child(self, owner: Instance, name: str, child: Instance):
        key = name.upper()
        
        # wenn Parent eine Font hat und Kind noch nicht: übernehmen
        if "FONT" in owner.props and "FONT" not in child.props:
            self.set_prop(child, "FONT", owner.props["FONT"], None)
            
        owner.children[key] = child
        owner.props[key] = child   # THIS.PushButton1 soll wie Property funktionieren

    def assign_name(self, name: str, value: Any):
        target = self.cur_with_target() or self.cur_this()
        set_prop_runtime(target, name, value)
    
    def cur_with_target(self) -> Optional[Instance]:
        return self.with_stack[-1] if self.with_stack else None
        
    def resolve_dotted(self, parts: list[str], ctx):
        if not parts:
            return None

        if parts[0].upper() == "THIS":
            obj = self.get_var("THIS", ctx)
        else:
            obj = self.get_var(parts[0], ctx)

        for member in parts[1:]:
            obj = self.get_member(obj, member, ctx)

        return obj
    
    def _need_value(self, v, ctx, what="Ausdruck"):
        if v is None:
            raise Exception(f"{ctx.start.line}:{ctx.start.column}: {what} ist None")
        return v

    def visitAdditiveExpr(self, ctx):
        # multiplicativeExpr ( (PLUS|MINUS) multiplicativeExpr )*
        res = self._need_value(self.visit(ctx.multiplicativeExpr(0)), ctx, "additiveExpr")
        n = len(ctx.multiplicativeExpr())
        for i in range(1, n):
            op = ctx.getChild(2*i - 1).getText()          # '+' oder '-'
            rhs = self._need_value(self.visit(ctx.multiplicativeExpr(i)), ctx, "additiveExpr rhs")
            if op == '+':
                res = res + rhs
            else:
                res = res - rhs
        return res

    def visitMultiplicativeExpr(self, ctx):
        # postfixExpr ( (STAR|SLASH) postfixExpr )*
        res = self._need_value(self.visit(ctx.postfixExpr(0)), ctx, "multiplicativeExpr")
        n = len(ctx.postfixExpr())
        for i in range(1, n):
            op = ctx.getChild(2*i - 1).getText()          # '*' oder '/'
            rhs = self._need_value(self.visit(ctx.postfixExpr(i)), ctx, "multiplicativeExpr rhs")
            if op == '*':
                res = res * rhs
            else:
                res = res / rhs
        return res

    def visitComparison(self, ctx):
        left = self._need_value(self.visit(ctx.additiveExpr(0)), ctx, "comparison left")
        if ctx.additiveExpr(1) is None:
            return left

        right = self._need_value(self.visit(ctx.additiveExpr(1)), ctx, "comparison right")
        op = ctx.compareOp().getText()

        if op == "<":  return left < right
        if op == "<=": return left <= right
        if op == ">":  return left > right
        if op == ">=": return left >= right
        if op == "==": return left == right
        if op == "!=": return left != right
        raise Exception(f"{ctx.start.line}:{ctx.start.column}: unbekannter Vergleichs-Operator {op}")

    def visitLogicalNot(self, ctx):
        # NOT logicalNot | comparison
        if ctx.NOT():
            return not bool(self._need_value(self.visit(ctx.logicalNot()), ctx, "logicalNot"))
        return self.visit(ctx.comparison())

    def visitLogicalAnd(self, ctx):
        result = self.visit(ctx.logicalNot(0))
        for i in range(1, len(ctx.logicalNot())):
            if not bool(result):      # short-circuit
                return result         # <-- NICHT False
            result = self.visit(ctx.logicalNot(i))
        return result

    def visitLogicalOr(self, ctx):
        result = self.visit(ctx.logicalAnd(0))
        for i in range(1, len(ctx.logicalAnd())):
            if bool(result):          # short-circuit
                return result         # <-- NICHT True
            result = self.visit(ctx.logicalAnd(i))
        return result

    def visitBreakStmt(self, ctx):
        raise BreakSignal()
    
    def visitExpr(self, ctx):
        # expr : logicalOr ;
        return self.visit(ctx.logicalOr())
    
    def visitWithBody(self, ctx):
        for ch in (ctx.children or []):
            if isinstance(ch, ParserRuleContext):
                self.visit(ch)
        return None
    
    def visitWithAssignStmt(self, ctx):
        value = self.visit(ctx.expr())
        parts = [t.getText() for t in ctx.withLvalue().IDENT()]

        target = self.with_stack[-1]
        owner  = self.with_stack_owner[-1]  # None oder Instance (z.B. Sender)

        # 1) Einfach: bold = .T.   oder   Text = "x"
        if len(parts) == 1:
            name = parts[0]

            if isinstance(target, Instance):
                self.set_prop(target, name.upper(), value, ctx)
                return None

            # z.B. WITH(Font) bold = .T.
            self.set_member(target, name, value, ctx)

            # wenn WITH(Font): neu anwenden
            if owner is not None and isinstance(target, FontValue):
                self.set_prop(owner, "FONT", target, ctx)

            return None

        # 2) Kette: Font.bold = .T.   innerhalb WITH(Sender)
        cur = target
        for seg in parts[:-1]:
            cur = self.get_member(cur, seg, ctx)

        self.set_member(cur, parts[-1], value, ctx)

        # wenn innerhalb WITH(Sender): Font.* geändert -> auf Sender neu setzen
        if isinstance(target, Instance) and parts and parts[0].upper() == "FONT":
            fv = target.props.get("FONT")
            if isinstance(fv, FontValue):
                self.set_prop(target, "FONT", fv, ctx)

        # wenn wir in WITH(Font) sind: owner neu setzen
        if owner is not None and isinstance(target, FontValue):
            self.set_prop(owner, "FONT", target, ctx)

        return None

    def set_property(self, obj, prop_name: str, value, ctx=None):
        key = prop_name.upper()

        # Wenn obj ein Qt-Widget ist:
        if hasattr(obj, "setFont") and key == "FONT":
            if isinstance(value, QFont):
                obj.setFont(value)
                return value
                
    def set_property_path(self, base_obj, path, value, ctx):
        obj = base
        for seg in path[:-1]:
            obj = self.get_member(obj, seg, ctx)

        last = path[-1]

        # Wir brauchen den "container" des letzten Members:
        container = base
        for seg in path[:-2]:
            container = self.get_member(container, seg, ctx)
            
        # obj ist jetzt das Zielobjekt (z.B. QFont), last ist "bold"
        self.set_member(obj, last, value, ctx)
        
        # -----------------------------------------
        # Wenn wir gerade Font.* geändert haben,
        # Font erneut ans Widget binden
        # -----------------------------------------
        if len(path) >= 2 and path[-2].upper() == "FONT":
            # -----------------------------------------------------
            # container ist dann das Objekt, das die Font-Property
            # besitzt falls das ein Qt-Widget ist:
            # -----------------------------------------------------
            qt_obj = getattr(container, "qt_obj", None)
            if qt_obj is not None and hasattr(qt_obj, "setFont"):
                qt_obj.setFont(obj)
            elif hasattr(container, "setFont"):
                container.setFont(obj)
                
        return value
        
    def push_scope(self):
        if not hasattr(self, "_scopes"):
            self._scopes = []
        self._scopes.append({})

    def pop_scope(self):
        self._scopes.pop()
    
    def visitStatement(self, ctx):
        if self._mode == "collect":
            # im Sammelpass Statements ignorieren
            return None
        return self.visitChildren(ctx)
    
    def ctx_text_token(ctx, token_name: str) -> str | None:
        fn = getattr(ctx, token_name, None)
        if callable(fn):
            t = fn()
            return t.getText() if t else None
        return None
        
    def eval_expr(self, ctx):
        text = ctx.getText()
        
        if getattr(ctx, "BRACKET_STRING", None) and ctx.BRACKET_STRING():
            tok = ctx.BRACKET_STRING().getSymbol()
            return self._unescape_bracket_string(tok.text)
            
        if self.is_simple_reference(text):
            return self.eval_reference_text(text)
        # Fallback: normale Expr-Auswertung über Visitor
        return self.visit(ctx)
    
    def is_simple_reference(self, s: str) -> bool:
        # erlaubt: X, this.width, a.b.c
        # (ohne Klammern/Operatoren)
        import re
        return re.fullmatch(r'(this|[A-Za-z_]\w*)(\.[A-Za-z_]\w*)*', s, re.IGNORECASE) is not None

    def eval_reference_text(self, s: str):
        parts = s.split('.')
        head = parts[0].upper()

        if head == "this":
            obj = self.this_object
            idx = 1
        else:
            obj = self._get_name(parts[0])
            idx = 1

        for name in parts[idx:]:
            obj = self.get_member(obj, name)
        return obj
        
    def visitBooleanLiteral(self, ctx):
        if ctx.TRUE():
            return True
        return False
        
    def eval_primary(self, ctx):
        if ctx.getText().upper() == "THIS":
            return self.this_object
        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())
        if ctx.STRING():
            return self._unquote(ctx.STRING().getText())
        if ctx.identifier():
            name = ctx.identifier().getText()
            return self._get_name(name)   # <-- HIER
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False
        if ctx.expr():
            return self.visit(ctx.expr())
            
        raise NotImplementedError(type(ctx).__name__)
    
    def has_method(self, obj, name: str) -> bool:
        # an dein Objektmodell anpassen:
        try:
            return name.upper() in obj.klass.methods
        except Exception:
            return False

    def resolve_method(self, start_class: str, method_name: str, ctx):
        c = start_class.upper()
        m = method_name.upper()

        while c is not None:
            cdef = self.classes.get(c)
            if cdef is None:
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: Klasse '{c}' ist nicht definiert")

            # ClassDef statt dict
            if m in cdef.methods:
                return c, cdef.methods[m]

            c = cdef.parent.upper() if cdef.parent else None

        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Methode '{m}' nicht gefunden (ab '{start_class}')")


    def resolve_method_silent(self, class_name: str, method_name: str):
        c = class_name
        m = method_name.upper()

        while c:
            cdef = self.classes.get(c)
            if not cdef:
                return None

            hit = cdef.methods.get(m)
            if hit:
                return hit

            c = cdef.parent.upper() if cdef.parent else None

        return None

    def in_local_scope(self) -> bool:
        return bool(self._scopes)

    def visitLocalDeclStmt(self, ctx):
        var_name = ctx.name.text  # IDENT token text
        # Deklaration ohne Wert -> None
        self.set_var(var_name, None)
        return None
        
    def visitLocalAssignStmt(self, ctx):
        var_name = ctx.name.text
        value = self.visit(ctx.expr())
        self.set_var(var_name, value)
        return value
    
    def _resolve_root(self, name: str, ctx):
        n = name.upper()
        if n == "THIS":
            # ist THIS irgendwo gesetzt?
            try:
                return self.get_var("THIS", ctx)
            except Exception:
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: 'this' ist nur innerhalb einer Instanzmethode gültig")
        return self.get_var(n, ctx)

    def loc(self, ctx):
        if ctx is not None and hasattr(ctx, "start") and ctx.start is not None:
            return f"{ctx.start.line}:{ctx.start.column}"
        return "<unknown>"

    def _normalize_handlers(self, value, ctx, event_name: str):
        # erlaubt: einzelner Delegate oder Liste/Tuple davon
        if value is None:
            return []
        if isinstance(value, (list, tuple)):
            handlers = list(value)
        else:
            handlers = [value]

        out = []
        for h in handlers:
            if not isinstance(h, Delegate):
                raise RuntimeError(
                    f"{self.loc(ctx)}: {event_name} erwartet Methode(n) (Delegate), bekam {type(h).__name__}"
                )
            out.append(h)
        return out

    def _bind_event(self, inst, prop_key: str, value, ctx=None):
        key = prop_key.upper()

        # welche Events gibt's?
        # (pass_event = ob Qt-event als 2s-Arg an Handler geht)
        EVENT_MAP = {
            "ONCLICK"       : ("_ONCLICK_WRAPPER",     "_ONCLICK_HANDLERS",     False),
            "ONDBLCLICK"    : ("_ONDBLCLICK_WRAPPER",  "_ONDBLCLICK_HANDLERS",  False),
            
            "ONMOUSEDOWN"   : ("_ONMOUSEDOWN_WRAPPER", "_ONMOUSEDOWN_HANDLERS", True),
            "ONMOUSEUP"     : ("_ONMOUSEUP_WRAPPER",   "_ONMOUSEUP_HANDLERS",   True),
            "ONMOUSEMOVE"   : ("_ONMOUSEMOVE_WRAPPER", "_ONMOUSEMOVE_HANDLERS", True),
            
            "ONMOUSELBUTTON": ("_ONMOUSELBUTTON_WRAPPER", "_ONMOUSELBUTTON_HANDLERS", True),
            "ONMOUSERBUTTON": ("_ONMOUSERBUTTON_WRAPPER", "_ONMOUSERBUTTON_HANDLERS", True),

            "ONKEYDOWN"     : ("_ONKEYDOWN_WRAPPER", "_ONKEYDOWN_HANDLERS", True),
            "ONKEYUP"       : ("_ONKEYUP_WRAPPER",   "_ONKEYUP_HANDLERS",   True),
        }

        if key not in EVENT_MAP:
            return False

        wrapper_prop, handlers_prop, pass_event = EVENT_MAP[key]
        handlers = self._normalize_handlers(value, ctx, key)

        # "löschen" erlauben: onX = NIL -> entfernt Handler
        if not handlers:
            inst.props.pop(wrapper_prop, None)
            inst.props.pop(handlers_prop, None)

            # bei Click auch Signal trennen
            if key == "ONCLICK" and hasattr(inst.backend, "clicked"):
                old = inst.props.get("_ONCLICK_WRAPPER")
                if old is not None:
                    try:
                        inst.backend.clicked.disconnect(old)
                    except Exception:
                        pass
            return True

        wrapper = self._make_multi_wrapper(inst, handlers, pass_event)
        inst.props[wrapper_prop] = wrapper
        inst.props[handlers_prop] = handlers

        # Click: lieber Qt-Signal (wie du’s schon hast)
        if key == "ONCLICK" and hasattr(inst.backend, "clicked"):
            old = inst.props.get("_ONCLICK_WRAPPER")
            if old is not None:
                try:
                    inst.backend.clicked.disconnect(old)
                except Exception:
                    pass

            inst.props["_ONCLICK_VIA_SIGNAL"] = True
            inst.backend.clicked.connect(wrapper)
            return True

        # Rest: EventFilter sicherstellen
        self._ensure_event_filter(inst, ctx)
        return True

    def _make_multi_wrapper(self, inst, handlers, pass_event: bool):
        def wrapper(ev=None):
            for h in handlers:
                try:
                    # dBase-Semantik: Sender ist inst
                    args = [inst]
                    if pass_event:
                        args.append(ev)
                    self.invoke_method(h.target, h.method_name, args, None)
                except ReturnSignal:
                    # RETURN in Handler -> nur diesen Handler beenden, nächste weiter
                    continue
            return None
        return wrapper
    
    def get_member(self, obj, prop: str, ctx=None):
        key = prop.upper()
        
        # --- QFont support ---
        if isinstance(obj, FontValue):
            if key == "BOLD":
                return bool(obj.bold)
            if key == "ITALIC":
                return bool(obj.italic)
            if key == "UNDERLINE":
                return bool(obj.underline)
            if key == "NAME":
                return str(obj.family)
            if key == "SIZE":
                return int(obj.size)
            
        if isinstance(obj, Instance):
            # 1) Property?
            if key in obj.props:
                return obj.props[key]
            
            if key == "FONT" and getattr(obj, "backend", None) is not None and hasattr(obj.backend, "font"):
                qf = obj.backend.font()  # QFont vom Widget
                fv = FontValue(
                    family      = qf.family(),
                    size        = qf.pointSize(),
                    bold        = qf.bold(),
                    italic      = qf.italic(),
                    underline   = qf.underline(),
                    obj         = qf,     # wichtig: gleicher QFont
                )
                obj.props["FONT"] = fv
                return fv

            cls_name = getattr(obj, "class_name", None)

            # 2) DSL-Methode? -> als Delegate zurückgeben
            if cls_name:
                cls_def = self.classes.get(cls_name.upper())
                if cls_def and key in cls_def.methods:
                    return Delegate(target=obj, method_name=key, runner=self)

            # ✅ 3) Native Methode: OPEN (für FORM und alles was davon erbt)
            if key == "OPEN" and cls_name and self.is_descendant_of(cls_name.upper(), "FORM"):
                return Delegate(target=obj, method_name="OPEN", runner=self)

            raise RuntimeError(f"{self.loc(ctx)}: Member '{prop}' in {cls_name} nicht gefunden")

    def set_member(self, obj, prop: str, value, ctx):
        key = prop.upper()
        
        # --- QFont support ---
        if isinstance(obj, FontValue):
            if key == "BOLD":
                obj.bold = bool(value)
                obj.obj.setBold(obj.bold)
                return value
            if key == "ITALIC":
                obj.italic = bool(value)
                obj.obj.setItalic(obj.italic)
                return value
            if key == "UNDERLINE":
                obj.underline = bool(value)
                obj.obj.setUnderline(obj.underline)
                return value
            if key == "NAME":
                obj.family = str(value)
                obj.obj.setFamily(obj.family)
                return value
            if key == "SIZE":
                obj.size = int(value)
                obj.obj.setPointSize(obj.size)
                return value

        if not isinstance(obj, Instance):
            raise RuntimeError(f"{self.loc(ctx)}: '{prop}' setzen auf Nicht-Objekt")
        
        # Hauptspeicher: props
        self.set_prop(obj, key, value, ctx)
        return value

    def class_chain_base_to_derived(self, class_name: str) -> list[str]:
        chain = []
        c = class_name.upper()
        while c:
            if c not in self.classes:
                break
            chain.append(c)
            parent = self.classes[c].parent
            c = parent.upper() if parent else None
        return list(reversed(chain))  # base zuerst
        
    def eval_member(self, obj, name: str, ctx):
        key = name.upper()

        # Nur Beispiel: anpassen an deine Instance-Struktur!
        if isinstance(obj, Instance):
            # 1) Field/Property?
            # falls du z.B. obj.fields als dict hast:
            if hasattr(obj, "props") and key in obj.props:
                return obj.props[key]

            # 2) Methode?
            res = self.resolve_method_silent(obj.class_name.upper(), key)
            if res is not None:
                # Delegate ist bei dir offenbar genau das, was CallExpr ausführen kann
                return Delegate(target=obj, method_name=key, runner=self)

            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Member '{name}' nicht gefunden")

        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Memberzugriff auf Nicht-Objekt: {type(obj).__name__}")
    
    def call_delegate(self, d: Delegate, args: list, ctx):
        # d.target ist deine Instance, d.method_name z.B. "INIT"
        return self.invoke_method(d.target, d.method_name, args, ctx)
        
    def visitCallExpr(self, ctx):
        callee = self.visit(ctx.expr())  # oder ctx.callee o.ä.
        args = []
        if ctx.argList() is not None:
            args = [self.visit(a) for a in ctx.argList().expr()]

        # ✅ Delegate direkt ausführen
        if isinstance(callee, Delegate):
            return self.call_delegate(callee, args, ctx)

        # normale Python-callables
        if not callable(callee):
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}")

        return callee(*args)
    
    def try_get_var(self, name, ctx):
        try:
            return self.get_var(name, ctx)
        except Exception:
            return None
        
    def get_chain(self, parts: list[str], ctx):
        parts = [p.upper() for p in parts]
        
        # --- SUPER::Method(...) ---
        if parts and parts[0] == "SUPER":
            if len(parts) < 2:
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: SUPER ohne Methodenname")
            
            this_obj = self.get_var("THIS", ctx)          # THIS muss gesetzt sein
            if not isinstance(this_obj, Instance):
                raise RuntimeError(f"{self.loc(ctx)}: SUPER nur innerhalb einer Instanzmethode gültig")
            
            cur_class = this_obj.class_name.upper()
            cdef = self.classes.get(cur_class)
            parent = cdef.parent.upper() if (cdef and cdef.parent) else None
            
            if not parent:
                raise RuntimeError(f"{self.loc(ctx)}: SUPER nicht möglich (keine Parent-Klasse)")
            
            mname = parts[1].upper()
            
            # Existiert die Methode irgendwo im Parent-Chain?
            if self.resolve_method_silent(parent, mname) is None:
                raise RuntimeError(f"{self.loc(ctx)}: SUPER-Methode '{mname}' nicht gefunden ab '{parent}'")
            
            # Delegate zurückgeben -> visitPostfixExpr ruft das dann auf
            return Delegate(target=this_obj, method_name=mname, runner=self)
            
        if parts[0].upper() == "THIS":
            cur = self.get_var("THIS", ctx)
        else:
            cur = self.get_var(parts[0], ctx)
        
        if cur is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist None")
        
        for name in parts[1:]:
            key = name.upper()

            if isinstance(cur, Instance):
                if hasattr(cur, "props") and key in cur.props:
                    cur = cur.props[key]
                    continue

                if self.resolve_method_silent(cur.class_name.upper(), key) is not None:
                    cur = Delegate(target=cur, method_name=key, runner=self)
                    continue
                    
                # 1) Property/Child?
                val = cur.props.get(name.upper())
                if val is not None:
                    cur = val
                    continue

                # 2) Methode?
                mctx = self.resolve_method_silent(cur.class_name.upper(), name.upper())
                if mctx is not None:
                    return Delegate(target=cur, method_name=name.upper(), runner=self)

                # 3) Fallback: zentrale Member-Logik benutzen (inkl. native OPEN)
                try:
                    cur = self.get_member(cur, name, ctx)   # <-- name ist "Open" im Original
                    continue
                except RuntimeError:
                    pass
                    
                # 4) sonst Fehler
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Member '{name}' nicht gefunden")

            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist kein Objekt (ist {type(cur).__name__})")

        return cur

    def set_chain(self, dotted_ctx, value):
        parts = [t.getText() for t in dotted_ctx.IDENT()]  # z.B. ["THIS", "PushButton1"]
        if not parts:
            raise RuntimeError(f"{dotted_ctx.start.line}:{dotted_ctx.start.column}: leere dottedRef")

        # Startobjekt bestimmen
        head = parts[0].upper()
        if head == "THIS":
            cur = self.this_obj
            if cur is None:
                cur = self.get_var(parts[0], dotted_ctx)
                #raise RuntimeError(f"{dotted_ctx.start.line}:{dotted_ctx.start.column}: THIS ist nicht gesetzt")
        else:
            # z.B. A.B = ...
            cur = self.get_var(parts[0], dotted_ctx)

        # bis zum vorletzten Member entlanglaufen
        for name in parts[1:-1]:
            cur = self.get_member(cur, name, dotted_ctx)  # muss Instance zurückgeben, wenn weiter gekettet wird
        
        # letztes Member setzen
        last = parts[-1].upper()
        if isinstance(cur, Instance):
            self.set_prop(cur, last, value, dotted_ctx)
            #cur.props[last] = value
            #cur.fields[last] = value
            return

        raise RuntimeError(f"{dotted_ctx.start.line}:{dotted_ctx.start.column}: Ziel ist kein Objekt für Member-Set")
        
    def new_instance(self, class_name: str, args: list[Any]):
        cn = class_name.upper()
        
        # 1) FONT ist builtin -> zuerst abfangen
        if cn == "FONT":
            family    = str(args[0]) if len(args) > 0 else "Arial"
            size      = int(args[1]) if len(args) > 1 else 10
            
            bold      = bool(args[2]) if len(args) > 2 else False
            italic    = bool(args[3]) if len(args) > 3 else False
            underline = bool(args[4]) if len(args) > 4 else False
            
            font_obj = QFont(family, size)
            font_obj.setBold(bold)
            font_obj.setItalic(italic)
            font_obj.setUnderline(underline)
            
            return FontValue(
                obj         = font_obj,
                family      = family,
                size        = size,
                bold        = bold,
                italic      = italic,
                underline   = underline)

        # 2) native Qt-Klassen (FORM, PUSHBUTTON, ...)
        if cn in NATIVE_BASES:
            parent_inst = args[0] if args else None
            parent_backend = parent_inst.backend if isinstance(parent_inst, Instance) else None

            inst = Instance(class_name=cn)
            inst.backend = create_backend_for_base(cn, parent_backend)
            return inst

        # 3) user-defined Klassen
        cdef = self.classes.get(cn)
        if cdef is None:
            known = ", ".join(sorted(self.classes.keys()))
            raise RuntimeError(
                f"{self.loc(None)}: Klasse '{cn}' ist nicht definiert. "
                f"Bekannte Klassen: {known}"
            )
        
        classdef = cdef
        inst = Instance(class_name=classdef.name)
        
        # base backend (FORM etc.)
        if classdef.parent:
            inst.backend = create_backend_for_base(classdef.parent, None)
        
        # defaults apply
        #for k,v in getattr(classdef, "default_props", {}).items():
        #    set_prop_runtime(inst, k, v)
        for k, v in classdef.default_props.items():
            self.set_prop(inst, k, v)
        
        # execute class body with THIS = inst
        self.push_this(inst)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = inst
            self._scopes[-1]["SELF"] = inst
            self.exec_class_body(classdef)
        finally:
            self.pop_scope()
            self.pop_this()
        
        if "INIT" in classdef.methods:
            self.invoke_method(inst, "INIT", args, None)
        
        return inst

    def set_prop(self, inst: Instance, name: str, value: Any, ctx=None):
        key = name.upper()
        
        # 1) normal speichern
        inst.props[key] = value
        
        # 2) MouseMove/Focus (Events => EventFilter)
        # MouseMove nur zuverlässig mit MouseTracking
        if hasattr(inst.backend, "setMouseTracking"):
            inst.backend.setMouseTracking(True)
            
        # 2) Event hooks
        if key == "ONGOTFOCUS":
            self._bind_ongotfocus(inst, value, ctx)
            return
        if key == "ONLOSTFOCUS":
            self._bind_onlostfocus(inst, value, ctx)
            return
        
        # Event-Properties?
        if self._bind_event(inst, key, value, ctx):
            return
            
        # 3) normale Qt properties
        apply_property_to_qt(inst, key, value)
    
    def _ensure_event_filter(self, inst: Instance, ctx=None):
        if inst.backend is None:
            return

        # Focus möglich machen
        try:
            inst.backend.setFocusPolicy(Qt.StrongFocus)
        except Exception:
            pass

        # MouseMove auch ohne gedrückte Taste
        try:
            inst.backend.setMouseTracking(True)
        except Exception:
            pass

        if not inst.props.get("_QT_EVENT_FILTER"):
            f = _QtEventFilter(self, inst)
            inst.props["_QT_EVENT_FILTER"] = f
            inst.backend.installEventFilter(f)

    def _bind_onkeydown(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onKeyDown erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                return None

        inst.props["_ONKEYDOWN_WRAPPER"] = wrapper

    def _bind_onkeyup(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onKeyUp erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                return None

        inst.props["_ONKEYUP_WRAPPER"] = wrapper

    def _bind_ondblclick(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onDblClick erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                return None

        inst.props["_ONDBLCLICK_WRAPPER"] = wrapper
        
    def _bind_onclick(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # NEU: Liste/Tuple erlauben
        handlers = handler
        if isinstance(handler, (list, tuple)):
            handlers = list(handler)
        else:
            handlers = [handler]
        
        # Alle müssen Delegate sein
        for h in handlers:
            if not isinstance(h, Delegate):
                raise RuntimeError(
                    f"{self.loc(ctx)}: onClick erwartet Methode(n) (Delegate), bekam {type(h).__name__}"
                )
        
        def wrapper(*qt_args):
            try:
                # nacheinander ausführen
                for h in handlers:
                    try:
                        self.invoke_method(h.target, h.method_name, [inst], None)
                    except ReturnSignal:
                        # Return aus Handler ignorieren -> weiter zum nächsten
                        pass
            except ReturnSignal:
                return None
                
        # nur für Buttons (erstmal)
        if hasattr(inst.backend, "clicked"):
            old = inst.props.get("_ONCLICK_WRAPPER")
            try:
                if old is not None:
                    inst.backend.clicked.disconnect(old)
            except Exception:
                pass
            #raise RuntimeError(f"{self.loc(ctx)}: onClick nicht unterstützt für {inst.class_name}")
            #return
            
            inst.props["_ONCLICK_WRAPPER"   ] = wrapper
            inst.props["_ONCLICK_VIA_SIGNAL"] = True
            
            inst.backend.clicked.connect(wrapper)
            return
            
        inst.props["_ONCLICK_VIA_SIGNAL"] = False
        
        # Alles andere (z.B. FORM/QDialog): EventFilter via MouseRelease
        self._ensure_event_filter(inst, ctx)
        inst.props["_ONCLICK_WRAPPER"] = wrapper
        
    def _bind_onmousedown(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # nur für Buttons (erstmal)
        if not hasattr(inst.backend, "pressed"):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseDown nicht unterstützt für {inst.class_name}")
        
        # Handler muss Delegate sein (oder notfalls BoundMethod)
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseDown erwartet eine Methode (Delegate), bekam {type(handler).__name__}")
        
        # alten wrapper ggf. disconnecten
        old = inst.props.get("_ONMOUSEDOWN_WRAPPER")
        try:
            if old is not None:
                inst.backend.pressed.disconnect(old)
        except Exception:
            pass
        
        def wrapper(*qt_args):
            # Sender: inst (dBase-Instance)
            try:
                # Wenn dein Handler Sender erwartet:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                # click-handler ignoriert return meistens
                return None
        
        inst.props["_ONMOUSEDOWN_WRAPPER"] = wrapper
        inst.backend.pressed.connect(wrapper)
    
    def _bind_onmouseup(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # nur für Buttons (erstmal)
        if not hasattr(inst.backend, "released"):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseUp nicht unterstützt für {inst.class_name}")
        
        # Handler muss Delegate sein (oder notfalls BoundMethod)
        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseUp erwartet eine Methode (Delegate), bekam {type(handler).__name__}")
        
        # alten wrapper ggf. disconnecten
        old = inst.props.get("_ONMOUSEUP_WRAPPER")
        try:
            if old is not None:
                inst.backend.released.disconnect(old)
        except Exception:
            pass
        
        def wrapper(*qt_args):
            # Sender: inst (dBase-Instance)
            try:
                # Wenn dein Handler Sender erwartet:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                # click-handler ignoriert return meistens
                return None
        
        inst.props["_ONMOUSEUP_WRAPPER"] = wrapper
        inst.backend.released.connect(wrapper)

    def _bind_onmousemove(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, Delegate):
            raise RuntimeError(
                f"{self.loc(ctx)}: onMouseMove erwartet eine Methode (Delegate), bekam {type(handler).__name__}"
            )

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                # Minimal: nur Sender
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                return None

        inst.props["_ONMOUSEMOVE_WRAPPER"] = wrapper

    def _bind_ongotfocus(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onGotFocus erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                return None

        inst.props["_ONFOCUSIN_WRAPPER"] = wrapper

    def _bind_onlostfocus(self, inst: Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onLostFocus erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except ReturnSignal:
                return None

        inst.props["_ONFOCUSOUT_WRAPPER"] = wrapper
    
    def exec_class_body(self, cdef: ClassDef):
        """
        Führt die Init-Statements aus, die beim Collect-Pass gesammelt wurden.
        Das sind z.B. WITH(...), THIS.PushButton1 = NEW ..., WRITE ..., usw.
        """
        # Primär: gesammelt in cdef.inits
        if getattr(cdef, "inits", None):
            for st in cdef.inits:
                self.visit(st)
            return

        # Fallback: alter Weg über body_ctx (falls du den später setzt)
        body = getattr(cdef, "body_ctx", None)
        if body is None:
            return

        for item in body.classBodyItem():
            if item.propertyDecl() is not None:
                continue
            if item.methodDecl() is not None:
                continue
            st = item.statement()
            if st is not None:
                self.visit(st)
            
    def collect_default_props(self, class_name: str) -> dict:
        cname = class_name.upper()

        # Klassenkette sammeln: derived -> base
        chain = []
        c = cname
        while c:
            cdef = self.classes.get(c)
            if not cdef:
                break
            chain.append(cdef)
            c = cdef.parent.upper() if cdef.parent else None

        # base -> derived mergen (Kind überschreibt)
        out = {}
        for cdef in reversed(chain):
            for k, v in (cdef.default_props or {}).items():
                out[k.upper()] = deepcopy(v)
        return out
        
    # Wert für PROPERTY ... = <expr> auswerten.
    # Läuft in einem frischen Scope und setzt THIS/SELF auf die neue Instanz.
    def _eval_property_default(self, expr_ctx, this_obj: Instance):
        local = {"THIS": this_obj, "SELF": this_obj}
        self._scopes.append(local)
        try:
            return self.visit(expr_ctx)
        finally:
            self._scopes.pop()
    
    def _norm(self, name: str) -> str:
        return name.upper()

    def _ensure_classdef(self, class_name: str) -> dict:
        k = self._norm(class_name.upper())
        if k not in self.classes:
            self.classes[k] = {
                "props": set(),
                "methods": {},
                "inits": [],
                # optional: "base": None,
            }
        else:
            # falls Klasse schon existiert, aber alt aufgebaut ist:
            self.classes[k].setdefault("props", set())
            self.classes[k].setdefault("methods", {})
            self.classes[k].setdefault("inits", [])
        return self.classes[k]
        
    def _vkey(self, name: str) -> str:
        return name.upper()

    def has_var(self, name: str) -> bool:
        key = self._vkey(name)
        return any(key in s for s in reversed(self._scopes))

    def get_var(self, name: str, ctx=None):
        key = self._vkey(name)
        for s in reversed(self._scopes):
            if key in s:
                return s[key]
        if ctx:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Variable '{key}' ist nicht definiert")
        raise RuntimeError(f"Variable '{key}' ist nicht definiert")

    def set_var(self, name: str, value):
        key = self._vkey(name)

        # wenn vorhanden: im nächstliegenden Scope updaten
        for s in reversed(self._scopes):
            if key in s:
                s[key] = value
                return

        # sonst: neu im aktuellen Scope anlegen
        self._scopes[-1][key] = value
    
    # ---------- Statements ----------
    def visitInput(self, ctx):
        # Pass 1: Klassen registrieren
        if self._mode == "collect":
            for it in ctx.item():
                if it.classDecl():
                    self.visit(it.classDecl())
            return None

        # Pass 2: Statements ausführen
        for it in ctx.item():
            if it.statement():
                self.visit(it.statement())

        return None
    
    def visitCallStmt(self, ctx):
        # callee irgendwie holen – z.B.:
        callee = self.visit(ctx.memberExpr())   # je nach Grammar: memberExpr/MemberExpr/etc.

        args = []
        if hasattr(ctx, "argList") and ctx.argList() is not None:
            args = [self.visit(e) for e in ctx.argList().expr()]

        # Delegate kann man "aufrufen", indem man die Methode im DSL ausführt
        if isinstance(callee, Delegate):
            return self.invoke_method(callee.target, callee.method_name, args, ctx)

        # normale Python-Funktionen
        if not callable(callee):
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}")

        return callee(*args)
            
    def visitDoWhileStatement(self, ctx):
        #print("DEBUG: enter DO WHILE")
        guard = 0
        while True:
            cond = self.visit(ctx.condition())
            #print("DEBUG: condition =", cond)
            
            if not cond:
                #print("DEBUG: leave DO WHILE (cond false)")
                break
            
            try:
                self.visit(ctx.block())
            except BreakSignal:
                break   # beendet Schleife
                
            guard += 1
            if guard > 1_000_000:
                raise RuntimeError("DO WHILE: Endlosschleife?")
            
    def visitNewExpr(self, ctx):
        class_name = ctx.IDENT().getText().upper()

        args = []
        if ctx.argList() is not None:
            args = [self.visit(e) for e in ctx.argList().expr()]

        # WICHTIG: benutze die robuste Instanz-Erzeugung
        return self.new_instance(class_name.upper(), args)
    
    def visitDeleteStmt(self, ctx):
        name = ctx.IDENT().getText().upper()

        # zuerst in lokalen Scopes suchen (innerstes zuerst)
        for scope in reversed(self._scopes):
            if name in scope:
                obj = scope[name]
                self._maybe_destroy(obj, ctx)
                del scope[name]
                return None

        # dann globals
        if name in self.globals:
            obj = self.globals[name]
            self._maybe_destroy(obj, ctx)
            del self.globals[name]
            return None

        raise Exception(f"{ctx.start.line}:{ctx.start.column}: DELETE: Variable '{name}' existiert nicht")


    def _maybe_destroy(self, obj, ctx):
        if not isinstance(obj, Instance):
            return
        # falls du sowas willst:
        try:
            owner_class, mctx = self.resolve_method(obj.class_name.upper(), "DESTROY", ctx)
        except Exception:
            return
        self.execute_method(owner_class, mctx, [], this_obj=obj)
    
    def execute_method(self, owner_class_name: str, method_ctx, arg_values, this_obj):
        prev_this = self.this_obj
        self.this_obj = this_obj
        self.push_scope()
        try:
            self.set_var("THIS", this_obj)
            params = self._get_method_params(method_ctx)
            for i, pname in enumerate(params):
                self.set_var(pname.upper(), arg_values[i] if i < len(arg_values) else None)
            return self.visit(method_ctx.block())
        finally:
            self.pop_scope()
            self.this_obj = prev_this
    
    def visitVarRef(self, ctx):
        name = ctx.IDENT().getSymbol().text
        return self._get_name(name)
    
    def _get_class_members(self, ctx):
        # probiere typische Namen in Reihenfolge
        for name in ("classBody", "classMembers", "classItems", "classItem", "classStmt", "classStatement", "member"):
            if hasattr(ctx, name):
                node = getattr(ctx, name)()
                if node is None:
                    continue
                # wenn node selbst die Liste hat:
                for list_name in ("classMember", "member", "classItem", "statement", "stmt"):
                    if hasattr(node, list_name):
                        return getattr(node, list_name)()
                # manchmal ist node schon eine Liste
                if isinstance(node, list):
                    return node
        return []
    
    def visitPropertyDecl(self, ctx):
        # PROPERTY <ident> = <expr>
        # zur Laufzeit: in THIS.props schreiben
        this_obj = self.get_var("THIS", ctx)

        if not isinstance(this_obj, Instance):
            raise RuntimeError(f"{self.loc(ctx)}: PROPERTY nur innerhalb einer Instanz gültig")

        pname = ctx.IDENT().getText().upper()
        pval  = self.visit(ctx.expr()) if ctx.expr() else None

        this_obj.props[pname] = pval
        return None
    
    def _handle_property_decl(self, pctx, cdef: ClassDef):
        # pctx ist propertyDeclContext
        pname = pctx.IDENT().getText().upper()
        pval  = self.visit(pctx.expr())   # Expression auswerten
        cdef.default_props[pname] = pval
        
    def visitClassDecl(self, ctx):
        if getattr(self, "_mode", "") != "collect":
            return None
        
        class_name  = ctx.name.text.upper()
        parent_name = ctx.parent.text.upper() if ctx.parent else None
        
        cdef = ClassDef(name=class_name.upper(), parent=parent_name)
        body = ctx.classBody()
        
        # WICHTIG: alles in Original-Reihenfolge einsammeln
        for ch in list(getattr(body, "children", []) or []):
            tname = type(ch).__name__

            # PROPERTY
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self._handle_property_decl(ch.propertyDecl(), cdef)
                # optional: auch in inits aufnehmen, wenn du propertyDecl zur Laufzeit ausführen willst
                # cdef.inits.append(ch)

            # METHOD
            elif hasattr(ch, "methodDecl") and ch.methodDecl():
                mctx = ch.methodDecl()
                mname = mctx.IDENT().getText().upper()
                cdef.methods[mname] = mctx

            # direkte Init-Statements (Assign / WITH / normale Statements)
            elif hasattr(ch, "assignStmt") and ch.assignStmt():
                cdef.inits.append(ch.assignStmt())
            elif hasattr(ch, "withStmt") and ch.withStmt():
                cdef.inits.append(ch.withStmt())
            elif tname.endswith("StatementContext"):
                cdef.inits.append(ch)

        self.classes[class_name] = cdef
        return None

    # Basisklasse -> Kind-Reihenfolge, damit Kind überschreiben könnte (später).
    def collect_props(self, class_name: str) -> list[str]:
        out = []
        seen = set()

        c = class_name.upper()
        chain = []

        while c:
            if c not in self.classes:
                break
            chain.append(c)
            parent = self.classes[c].parent
            c = parent.upper() if parent else None

        for cname in reversed(chain):  # base zuerst
            for p in self.classes[cname].get("props", set()):
                if p not in seen:
                    seen.add(p)
                    out.append(p)

        return out
 
    def _method_name(self, ctx):
        # Label: name=IDENT
        if hasattr(ctx, "name") and ctx.name is not None:
            return ctx.name.text

        # Token getter: IDENT() oder ID()
        for tok in ("IDENT", "ID"):
            fn = getattr(ctx, tok, None)
            if callable(fn):
                t = fn()
                if t:
                    return t.getText()

        # Rule getter: identifier()
        fn = getattr(ctx, "identifier", None)
        if callable(fn):
            sub = fn()
            if sub:
                return sub.getText()

        # Fallback
        return ctx.getText()

    def visitMethodDecl(self, ctx):
        method_name = ctx.name.text.upper()

        params = []
        pl = ctx.paramList()
        if pl is not None:
            params = [t.getText().upper() for t in pl.IDENT()]

        # block besuchen / speichern / was auch immer du tust
        body = ctx.block()

        # Beispiel: speichern
        self.methods[method_name] = {
            "params": params,
            "ctx": body,
        }

        return None

    def visitMemberExpr(self, ctx):
        idents = [t.getText() for t in ctx.IDENT()]

        # THIS vorkommt
        if ctx.THIS() is not None:
            parts = ["THIS"] + idents
        else:
            parts = idents

        # Sonderfall: einzelner Name (z.B. "Font" oder "Sender")
        # -> MUSS über _get_name laufen, damit WITH-Context/Props funktionieren
        if len(parts) == 1 and parts[0].upper() != "THIS":
            return self._get_name(parts[0])

        # Sonderfall: nur "THIS"
        if parts == ["THIS"]:
            if self.this_stack:
                return self.cur_this()
            return self.get_var("THIS", ctx)

        # Optional: schneller Pfad THIS.Method => Delegate
        if len(parts) == 2 and parts[0].upper() == "THIS":
            this_obj = self.get_var("THIS", ctx)
            if isinstance(this_obj, Instance):
                key = parts[1].upper()
                if self.resolve_method_silent(this_obj.class_name.upper(), key) is not None:
                    return Delegate(target=this_obj, method_name=key, runner=self)

        return self.get_chain(parts, ctx)

    
    def visitPostfixExpr(self, ctx):
        # Basis auswerten
        cur = self.visit(ctx.primary())
        expr_list = []
        #print("===> ", cur)
        # Alle argLists einsammeln (für jeden '(' ... ')'-Call)
        arglists = ctx.argList() or []
        if not isinstance(arglists, list):
            arglists = [arglists]
        call_i = 0
        #print("--> ", ctx.argList())
        
        pending_member = None  # merkt sich den Namen nach '.'

        i = 1  # child(0) ist primary
        while i < ctx.getChildCount():
            t = ctx.getChild(i).getText()

            # Member-Start: ".Name"
            if t == '.':
                pending_member = ctx.getChild(i + 1).getText()
                i += 2
                continue

            # Call: "( ... )"
            if t == '(':
                # Argumente zur passenden argList
                if call_i < len(arglists):
                    al = arglists[call_i]

                    exprs = al.expr()
                    if exprs is None:
                        expr_list = []
                    elif isinstance(exprs, list):
                        expr_list = exprs
                    else:
                        # WICHTIG: einzelner ExprContext ist iterierbar -> sonst "Child-Liste"
                        expr_list = [exprs]
                        
                args = [self.visit(e) for e in expr_list]

                call_i += 1

                # Call ausführen
                if pending_member is None:
                    # direkter Call: Foo(...)
                    # dBase-Methoden-Objekte auch aufrufbar machen
                    if isinstance(cur, Delegate):
                        cur = self.invoke_method(cur.target, cur.method_name, args, ctx)
                    elif isinstance(cur, BoundMethod):
                        cur = self.invoke_method(cur.target, cur.name, args, ctx)
                    elif callable(cur):
                        cur = cur(*args)
                    else:
                        raise Exception(
                            f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}"
                        )
                else:
                    # Methoden-/Membercall: obj.Member(...)
                    name = pending_member
                    pending_member = None

                    if isinstance(cur, Instance):
                        # resolve_method NICHT separat aufrufen (Altlast / falscher Zugriff bei ClassDef)
                        cur = self.invoke_method(cur, name, args, ctx)
                    else:
                        fn = self.get_member(cur, name, ctx)
                        if callable(fn):
                            cur = fn(*args)
                        else:
                            raise Exception(
                                f"{ctx.start.line}:{ctx.start.column}: Member '{name}' ist nicht aufrufbar"
                            )

                i += 1
                continue

            # Falls noch ein Member "steht" und kein '(' folgt: obj.Member
            if pending_member is not None:
                cur = self.get_member(cur, pending_member, ctx)
                pending_member = None
                continue

            i += 1

        # falls am Ende noch ".X"
        if pending_member is not None:
            cur = self.get_member(cur, pending_member, ctx)

        return cur

    def visitLvalue(self, ctx):
        pe = ctx.postfixExpr()

        # Basis (primary) als Text
        base = pe.primary().getText()

        # Suffixe iterieren: children enthalten '.' IDENT oder '(' ... ')'
        parts = [base]
        i = 1  # child 0 ist primary
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()

            if ch == '.':
                ident = pe.getChild(i + 1).getText()
                parts.append(ident)
                i += 2
                continue

            if ch == '(':
                # Call in LHS ist nicht erlaubt
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: LVALUE darf keinen Call enthalten: {pe.getText()}")

            i += 1

        # z.B. "THIS.width" -> ["THIS","width"]
        return parts
    
    def _lvalue_chain_from_postfix(self, pe, ctx):
        # pe ist postfixExpr-Context
        chain = [pe.primary().getText()]

        i = 1  # child 0 ist primary
        while i < pe.getChildCount():
            ch = pe.getChild(i).getText()

            if ch == '.':
                chain.append(pe.getChild(i + 1).getText())
                i += 2
                continue

            if ch == '(':
                raise Exception(
                    f"{ctx.start.line}:{ctx.start.column}: "
                    f"Assignment-Ziel darf keinen Call enthalten: {pe.getText()}"
                )

            i += 1

        return [s.upper() for s in chain]
    
    def set_chain_on_object(self, base_obj, chain: list[str], value, ctx):
        if base_obj is None:
            raise RuntimeError("WITH base object is None")

        if not chain:
            raise RuntimeError("empty chain in assignment")

        obj = base_obj
        # bis vor die letzte Property laufen
        for name in chain[:-1]:
            # hier brauchst du irgendeine Art get_member (oder du nutzt fields direkt)
            obj = self.get_member(obj, name, ctx)  # <- falls du das hast
            if obj is None:
                raise RuntimeError(f"WITH chain member '{name}' is None")

        return self.set_member(obj, chain[-1], value, ctx)
    
    def visitAssignment(self, ctx):
        value = self.visit(ctx.expr())
        self.set_chain(ctx.dottedRef(), value)
        return value
        
    def _set_chain_parts(self, parts, value, ctx):
        head = parts[0].upper()

        if head == "THIS":
            cur = self.get_var("THIS", ctx)
            if cur is None:
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: THIS ist nicht gesetzt")
        else:
            cur = self.get_var(parts[0], ctx)  # z.B. Sender, obj, etc.

        if cur is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist nicht definiert")

        # Merker: wenn wir gerade Font.* ändern, brauchen wir den "Besitzer" (z.B. Sender)
        font_container = None

        # bis zum vorletzten auflösen
        for name in parts[1:-1]:
            # Wenn das nächste Segment "Font" ist und cur ein Instance ist,
            # dann ist cur der Container (z.B. Sender), dessen Font wir später neu anwenden müssen.
            if name.upper() == "FONT" and isinstance(cur, Instance):
                font_container = cur

            cur = self.get_member(cur, name, ctx)

        last = parts[-1]  # NICHT uppern, set_member macht eh upper intern (oder du machst's dort)

        # 1) normales Instance-Property setzen (Sender.Text = ..., Sender.Font = NEW FONT(...))
        if isinstance(cur, Instance):
            self.set_prop(cur, last.upper(), value, ctx)  # aktualisiert props + Qt (setText etc.)
            return

        # 2) Unter-Property auf "value object" setzen (z.B. Sender.Font.bold = .T.)
        #    -> cur ist dann z.B. FontValue
        self.set_member(cur, last, value, ctx)

        # Wenn wir Font.* geändert haben: Font erneut auf den Container anwenden,
        # damit Qt das wirklich übernimmt.
        if font_container is not None:
            try:
                fv = self.get_member(font_container, "FONT", ctx)  # liefert FontValue
            except Exception:
                fv = font_container.props.get("FONT")

            if fv is not None:
                # set_prop sorgt bei dir dafür, dass Qt aktualisiert wird
                self.set_prop(font_container, "FONT", fv, ctx)

        return
        
    def assign_lvalue(self, lctx, value, ctx):
        # häufig: lvalue : IDENT ('.' IDENT)* ;
        if hasattr(lctx, "IDENT") and lctx.IDENT():
            toks = lctx.IDENT()
            parts = [t.getText() for t in (toks if isinstance(toks, list) else [toks])]

            # nur X = ...
            if len(parts) == 1:
                self._set_name(parts[0], value, ctx)   # WITH-aware: setzt Var oder Property
                return

            # THIS.PushButton1 = ...
            self._set_chain_parts(parts, value, ctx)
            return
        
        # fallback: Text parsen (quick&dirty, aber funktioniert)
        text = lctx.getText()  # z.B. THIS.PushButton1
        parts = text.split(".")
        if len(parts) == 1:
            self._set_name(parts[0], value, ctx)
        else:
            self._set_chain_parts(parts, value, ctx)
            
    def visitAssignStmt(self, ctx):
        value = self.visit(ctx.expr())
        pe = ctx.lvalue().postfixExpr()
        idents_u = self._lvalue_chain_from_postfix(pe, ctx)

        # ✅ WITH zuerst behandeln, bevor du returnst
        base = self.current_with_base
        if base is not None:
            # relative Zuweisung im WITH: "watch = 123" oder "a.b = 1"
            if len(idents_u) >= 1 and idents_u[0] != "THIS":
                return self.set_chain_on_object(base, idents_u, value, ctx)

        # danach normaler Assign
        if ctx.lvalue():
            self.assign_lvalue(ctx.lvalue(), value, ctx)
            return None
    
    def visitForStmt(self, ctx):
        var_name = ctx.IDENT().getText()
        start = float(ctx.numberExpr(0).getText())
        end = float(ctx.numberExpr(1).getText())

        # klassisch inklusiv (wie in vielen Basics/xBase)
        step = 1.0
        i = start
        
        # STEP optional
        if ctx.STEP() is not None:
            step = float(self.visit(ctx.numberExpr(2)))
            if step == 0:
                raise RuntimeError(f"{self.loc(ctx)}: STEP darf nicht 0 sein")
        else:
            # sinnvoller Default: Richtung automatisch
            step = 1.0 if end >= start else -1.0

        def cond(x):
            return x <= end if step > 0 else x >= end

        while cond(i):
            self.set_var(var_name.upper(), i)

            try:
                # block ausführen: statement*
                for st in ctx.block().statement():
                    self.visit(st)
            except BreakSignal:
                break

            i += step

        return None
        
    def visitWriteStmt(self, ctx):
        #print("DEBUG writeStmt text:", ctx.getText())
        #print("DEBUG writeArg count:", len(ctx.writeArg()))
        #for i, a in enumerate(ctx.writeArg()):
            #print(f"DEBUG arg[{i}] text:", a.getText(),
            #      "STRING?", a.STRING() is not None,
            #      "dottedRef?", a.dottedRef() is not None,
            #      "expr?", a.expr() is not None)

        parts = [self.eval_writeArg(a) for a in ctx.writeArg()]
        print("".join(parts))
        return None
    
    def eval_writeArg(self, arg_ctx):
        if arg_ctx.STRING():
            s = arg_ctx.STRING().getText()
            return s[1:-1]

        if arg_ctx.dottedRef():
            val = self.visit(arg_ctx.dottedRef())
            return "" if val is None else str(val)

        if arg_ctx.expr():
            val = self.visit(arg_ctx.expr())
            return "" if val is None else str(val)

        raise RuntimeError("writeArg enthält weder STRING noch dottedRef noch expr")

    def visitDottedRef(self, ctx):
        # dottedRef : (THIS | IDENT) (DOT IDENT)+ ;
        idents = [t.getText() for t in ctx.IDENT()]

        if ctx.THIS() is not None:
            head = "THIS"
        else:
            head = idents[0]  # erster IDENT ist der Kopf

        # ✅ Startobjekt über _get_name holen (kennt WITH + Variablen)
        if head.upper() == "THIS":
            cur = self.get_var("THIS", ctx)
            tail = idents
        else:
            cur = self._get_name(head)      # <-- wichtig!
            tail = idents[1:]               # Rest nach dem Kopf

        # Restliche Member auflösen
        for name in tail:
            cur = self.get_member(cur, name, ctx)

        return cur

        
    def _format_value(self, val):
        # optional hübscher: 3.0 -> "3"
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        return str(val)

    def visitIfStmt(self, ctx):
        cond_val = self.visit(ctx.expr())
        cond_true = (cond_val != 0)

        blocks = ctx.block()
        then_block = blocks[0]
        else_block = blocks[1] if len(blocks) > 1 else None

        if cond_true:
            self.visit(then_block)
        elif else_block is not None:
            self.visit(else_block)

        return None

    def visitBlock(self, ctx):
        for st in ctx.statement():
            self.visit(st)
        return None

    # ---------- Expression Evaluation ----------
    def visitAddExpr(self, ctx):
        value = self.visit(ctx.mulExpr(0))
        for i in range(1, len(ctx.mulExpr())):
            op = ctx.getChild(2*i-1).getText()
            rhs = self.visit(ctx.mulExpr(i))
            value = value + rhs if op == '+' else value - rhs
        return value

    def visitMulExpr(self, ctx):
        value = self.visit(ctx.unaryExpr(0))
        for i in range(1, len(ctx.unaryExpr())):
            op = ctx.getChild(2*i-1).getText()
            rhs = self.visit(ctx.unaryExpr(i))
            value = value * rhs if op == '*' else value / rhs
        return value

    def visitUnaryExpr(self, ctx):
        if ctx.getChildCount() == 2:
            op = ctx.getChild(0).getText()
            val = self.visit(ctx.unaryExpr(0))
            return +val if op == '+' else -val
        return self.visit(ctx.primary())

    def visitLiteral(self, ctx):
        if ctx.TRUE():
            return True
        if ctx.FALSE():
            return False
        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())
        if ctx.STRING():
            s = ctx.STRING().getText()
            return s[1:-1] if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'") else s
        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Unbekanntes literal")

    def visitPrimary(self, ctx):
        if hasattr(ctx, "handlerList") and ctx.handlerList():
            return self.visit(ctx.handlerList())
            
        if ctx.literal():
            return self.visit(ctx.literal())
            
        if ctx.newExpr():
            return self.visit(ctx.newExpr())

        if ctx.memberExpr():
            return self.visit(ctx.memberExpr())
        
        if ctx.THIS():
            return self.get_var("THIS", ctx)
        
        if ctx.SUPER():
            return "SUPER"
            
        if ctx.FLOAT():
            return float(ctx.FLOAT().getText())

        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())

        if ctx.STRING():
            s = ctx.STRING().getText()
            return s[1:-1] if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'") else s

        if ctx.IDENT():
            name = ctx.IDENT().getSymbol().text  # Token-Text
            return self._get_name(name)       # <-- HIER ist der Lookup!
        
        if getattr(ctx, "BRACKET_STRING", None) and ctx.BRACKET_STRING():
            return self._unescape_bracket_string(ctx.BRACKET_STRING().getText())
            
        # ( expr )
        if ctx.expr():
            return self.visit(ctx.expr())
        
        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Unbekanntes primary")
    
    def visitExprStmt(self, ctx):
        # expr ausführen, Ergebnis ignorieren
        self.visit(ctx.postfixExpr())
        return None

    def _get_name(self, name: str):
        key = name.upper()

        # 1) normale Variablen (aus _scopes!)
        try:
            return self.get_var(key, None)
        except Exception:
            pass

        # 2) WITH-Kontext: als Property des aktuellen WITH-Objekts behandeln
        if self.with_stack:
            base = self.with_stack[-1]
            if isinstance(base, Instance):
                if key in base.props:
                    return base.props[key]
                try:
                    return self.get_member(base, key, None)
                except Exception:
                    raise RuntimeError(f"Unbekanntes WITH-Property '{name}'")
            if isinstance(base, dict):
                # case-insensitive
                for k, v in base.items():
                    if k.upper() == key:
                        return v
                raise RuntimeError(f"Unbekanntes WITH-Property '{name}'")

        # 3) nicht gefunden
        raise RuntimeError(f"Unbekannter Name '{name}'")


    def _set_name(self, name: str, value, ctx=None):
        key = name.upper()

        # 1) wenn Variable irgendwo existiert -> updaten (in _scopes)
        for s in reversed(self._scopes):
            if key in s:
                s[key] = value
                return

        # 2) WITH aktiv? -> Property setzen
        if self.with_stack:
            base = self.with_stack[-1]
            if isinstance(base, Instance):
                base.props[key] = value
                self.set_prop(base, key, value, ctx)
                return
            if isinstance(base, dict):
                # vorhandenen key (case-insensitiv) treffen oder neu anlegen
                for k in list(base.keys()):
                    if k.upper() == key:
                        base[k] = value
                        return
                base[name] = value
                return

        # 3) sonst: neue Variable im aktuellen Scope anlegen
        self._scopes[-1][key] = value

    def visitWithStmt(self, ctx):
        # WITH ( withTarget ) withBody ENDWITH
        obj = self.visit(ctx.withTarget())
        
        if obj is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: WITH target ist None")
        
        owner = None
        if isinstance(obj, FontValue) and self.with_stack and isinstance(self.with_stack[-1], Instance):
            owner = self.with_stack[-1]
        
        self.with_stack.append(obj)
        self.with_stack_owner.append(owner)
        try:
            self.visit(ctx.withBody())
        finally:
            self.with_stack_owner.pop()
            self.with_stack.pop()
        
        return None

    def set_child(self, owner: Instance, name: str, child: Instance):
        owner.children[name.upper()] = child
        owner.props[name.upper()] = child  # damit THIS.PushButton1 als Property funktioniert

    def visitWithTarget(self, ctx):
        # withTarget
        #   : THIS
        #   | dottedRef
        #   | IDENT
        #   | postfixExpr
        #   ;

        if ctx.THIS():
            if ctx.THIS():
                return self.get_var("THIS", ctx)   # oder self.cur_this() wenn du das nutzt

        if ctx.dottedRef():
            return self.visit(ctx.dottedRef())

        if ctx.IDENT():
            # Variable/Objektname (case-insensitiv handled by _get_name)
            return self._get_name(ctx.IDENT().getText())

        if ctx.postfixExpr():
            return self.visit(ctx.postfixExpr())

        return None

    def visitCompareExpr(self, ctx):
        left = self.visit(ctx.addExpr(0))

        # kein Vergleich, nur Zahl -> direkt zurück
        if ctx.getChildCount() == 1:
            return left

        op = ctx.getChild(1).getText()
        right = self.visit(ctx.addExpr(1))

        if op == "==": return 1 if left == right else 0
        if op == "!=": return 1 if left != right else 0
        if op == "<":  return 1 if left <  right else 0
        if op == "<=": return 1 if left <= right else 0
        if op == ">":  return 1 if left >  right else 0
        if op == ">=": return 1 if left >= right else 0

        raise ValueError(f"Unknown comparison operator: {op}")

    # ---------- Helpers ----------
    def _unescape_string(self, raw: str) -> str:
        quote = raw[0]
        s     = raw[1:-1]  # äußere Quotes weg
        out   = []
        i     = 0
        while i < len(s):
            if s[i] == '\\' and i + 1 < len(s):
                c = s[i+1]
                if c == 'n':
                    out.append('\n')
                elif c == 't':
                    out.append('\t')
                elif c == '\\':
                    out.append('\\')
                elif c == '"':
                    out.append('"')
                elif c == "'":
                    out.append("'")
                else:
                    out.append(c)
                i += 2
            else:
                out.append(s[i])
                i += 1
        return ''.join(out)
        
    def _unescape_bracket_string(self, tok_text: str) -> str:
        # tok_text enthält inklusive [ ... ]
        s = tok_text[1:-1]           # äußere Klammern weg
        s = s.replace("]]", "]")     # Escape wieder zurück
        return s
        
    def visitClassBody(self, ctx):
        # NUR member besuchen
        for m in ctx.classMember():
            self.visit(m)
        return None

    def _methoddef_from_methoddecl(self, decl_ctx):
        # 1) Parameterliste finden
        params = []

        # Häufig: decl_ctx.paramList() -> hat IDENT()
        if hasattr(decl_ctx, "paramList") and decl_ctx.paramList() is not None:
            pl = decl_ctx.paramList()
            if hasattr(pl, "IDENT"):
                params = [t.getText() for t in pl.IDENT()]

        # Alternativ: decl_ctx.IDENT() enthält [methodName, p1, p2, ...]
        if not params and hasattr(decl_ctx, "IDENT"):
            idents = [t.getText() for t in decl_ctx.IDENT()]
            if len(idents) >= 2:
                params = idents[1:]  # erstes ist meist der Methodenname

        # 2) Block/Body finden (je nach Grammar-Namen)
        block_ctx = None
        for cand in ("block", "stmtBlock", "compoundStmt", "methodBlock"):
            if hasattr(decl_ctx, cand):
                fn = getattr(decl_ctx, cand)
                try:
                    tmp = fn()
                except TypeError:
                    tmp = None
                if tmp is not None:
                    block_ctx = tmp
                    break

        # Wenn nix gefunden: nimm notfalls den decl_ctx selbst (und visit() muss damit klarkommen)
        if block_ctx is None:
            block_ctx = decl_ctx

        return MethodDef(params=params, block_ctx=block_ctx)

    def _get_method_params(self, method_ctx):
        # method_ctx ist MethodDeclContext
        pl = method_ctx.paramList()
        if not pl:
            return []

        # Häufige Fälle:
        # 1) paramList : IDENT (',' IDENT)* ;
        if hasattr(pl, "IDENT"):
            toks = pl.IDENT()
            if toks:
                if isinstance(toks, list):
                    return [t.getText() for t in toks]
                return [toks.getText()]

        # 2) paramList : identifier (',' identifier)* ;
        if hasattr(pl, "identifier"):
            ids = pl.identifier()
            if ids:
                if isinstance(ids, list):
                    return [x.getText() for x in ids]
                return [ids.getText()]

        # Fallback (zur Not): Text parsen
        txt = pl.getText()  # z.B. "a,c" oder "a,c,d"
        return [p.strip() for p in txt.split(",") if p.strip()]
        
    def invoke_method(self, target, method_name: str, args: list, ctx):
        mname = method_name.upper()

        # Native OPEN
        if mname == "OPEN" and self.is_descendant_of(target.class_name.upper(), "FORM"):
            return form_open(target)

        # resolve_method liefert (owner_class, method_ctx)
        owner_class, mctx = self.resolve_method(target.class_name, mname, ctx)

        self.push_this(target)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = target
            self._scopes[-1]["SELF"] = target

            # ✅ Parameter binden (DAS fehlt!)
            params = self._get_method_params(mctx)
            for i, pname in enumerate(params):
                self.set_var(pname, args[i] if i < len(args) else None)

            try:
                self.visit(mctx.block())
                return None
            except ReturnSignal as rs:
                return rs.value

        finally:
            self.pop_scope()
            self.pop_this()
        
    # für Events ... -> FireClick(button)
    def invoke_delegate(self, d: Delegate, args: list, ctx):
        res = self.resolve_method(d.target.class_name.upper(), d.method_name, ctx)
        owner_class, method_ctx = res
        return self.execute_method(owner_class, method_ctx, args, this_obj=d.target)

    def visitCondition(self, ctx):
        return self.visit(ctx.logicalOr())

    def visitDoStmt(self, ctx):
        target = ctx.doTarget().getText()
        args = []
        if ctx.argList():
            for e in ctx.argList().expr():
                args.append(self.eval_expr(e))

        # 1) Program?
        if self.looks_like_program(target):   # z.B. enthält '.' oder endet auf .PRG
            self.run_program(target, args)
        else:
            self.call_procedure(target, args)

    def visitParameterStmt(self, ctx):
        names = [t.getText() for t in ctx.paramNames().IDENT()]
        incoming = self.current_frame.args if self.current_frame.args else []

        for i, name in enumerate(names):
            self.current_frame.vars[name.upper()] = incoming[i] if i < len(incoming) else None
    
    def visitReturnStmt(self, ctx):
        val = self.visit(ctx.expr()) if ctx.expr() else None
        raise ReturnSignal(val)

    def visitHandlerList(self, ctx):
        # ctx.expr() ist eine Liste: erstes expr + alle (SEMI expr)*
        items = []
        for e in ctx.expr():
            items.append(self.eval_expr(e))
        return items
        
    def is_descendant_of(self, class_name: str, base_name: str) -> bool:
        cn = class_name.upper()
        base = base_name.upper()
        while True:
            if cn == base:
                return True
            cdef = self.classes.get(cn)
            if not cdef or not cdef.parent:
                return False
            cn = cdef.parent.upper()

    def _bool_arg(self, args, idx, default=False):
        if idx >= len(args):
            return default
        v = args[idx]
        # robust: akzeptiere auch 0/1, "true"/"false"
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.strip().upper() in ("TRUE", "T", ".T.", "1", "YES", "Y")
        return default

    def fire_event(self, inst, event_name: str, qt_event=None):
        # event_name z.B. "ONMOUSEDOWN"
        handler = inst.props.get(event_name)
        if handler is None:
            return False

        # 1) Delegate-Fall (dein System)
        #    z.B. Delegate(target=thisObj, method_name="PUSHBUTTON1_ONMOUSEDOWN", runner=self)
        if isinstance(handler, Delegate):
            # Signatur: METHOD ... (Sender)   oder (Sender, Event)
            try:
                return handler.call([inst])  # minimal: Sender
            except TypeError:
                return handler.call([inst, qt_event])  # optional: Qt-Event durchreichen

        # 2) Wenn du Handler als MethodDef / Callable speicherst:
        if callable(handler):
            return handler(inst, qt_event)

        return False

    def attach_events_to_widget(self, inst):
        w = inst.backend
        if w is None:
            return

        # MouseMove kommt nur, wenn MouseTracking an ist
        if hasattr(w, "setMouseTracking"):
            w.setMouseTracking(True)

        # Focus events kommen nur, wenn das Widget Fokus bekommen darf
        # PushButton kann das, aber sicher ist sicher:
        try:
            from PyQt5.QtCore import Qt
            w.setFocusPolicy(Qt.StrongFocus)
        except Exception:
            pass

        filt = WidgetEventFilter(self, inst)
        inst._qt_event_filter = filt      # <-- Referenz halten!
        w.installEventFilter(filt)

    def call_method(self, inst: Instance, name: str, args):
        name = name.upper()

        # native OPEN
        if name == "OPEN" and self.is_descendant_of(inst.class_name.upper(), "FORM"):
            return form_open(inst)

        cdef = self.classes.get(inst.class_name.upper())
        if not cdef or name not in cdef.methods:
            raise RuntimeError(f"Methode {name} nicht gefunden")

        mctx = cdef.methods[name]

        self.push_this(inst)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = inst
            self._scopes[-1]["SELF"] = inst

            params = self._get_method_params(mctx)
            for i, pname in enumerate(params):
                self.set_var(pname, args[i] if i < len(args) else None)

            self.visit(mctx.block())
        finally:
            self.pop_scope()
            self.pop_this()

    def visitCreateFileStmt(self, ctx):
        # Beispiel: CREATE FILE oder CREATE FILE <expr>
        path = ""
        if hasattr(ctx, "expr") and ctx.expr():
            path = str(self.eval_expr(ctx.expr()))
        
        self.open_file_editor(path=path, text="")
        return None
        
    def open_file_editor(self, path: str = "", text: str = ""):
        text = ""
        # wenn path gesetzt ist und text leer: Datei laden
        if path and text == "":
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
            except FileNotFoundError:
                print("file not found.")
                pass
        try:
            win = FileEditorWindow(parent=MAINAPP, initial_path=path, initial_text=text)
            sub = MAINAPP.mdi.addSubWindow(win)
            win.resize(500, 450)
            
            # 1) immer sichtbar + Vordergrund
            win.show()
            win.raise_()
            win.activateWindow()

            # 2) falls minimiert: wieder herstellen
            win.setWindowState(win.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

            # 3) optional: "Always on top"
            win.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            win.show()  # nach setWindowFlag nochmal show()!
            win.raise_()
            win.activateWindow()
    
            # Referenz halten (gegen GC)
            self._open_windows = getattr(self, "_open_windows", [])
            self._open_windows.append(win)
        except Exception as e:
            print(e)

# ---------------------------------------------------------------------------
# parser stuff ...
# ---------------------------------------------------------------------------        
def parse(filename: str):
    # 0 pre-procession
    pp = Preprocessor(include_paths=[Path("includes")])
    pre = pp.process(filename)
    
    #source = FileStream(filename, encoding="utf-8")
    source = InputStream(pre)
    lexer  = dBaseLexer(source)
    tokens = CommonTokenStream(lexer)
    tokens.fill();
    parser = dBaseParser(tokens)

    tree   = parser.input_()
    sema   = analyze(tree, parser)
    
    # 1. lexer check
    while True:
        tok = lexer.nextToken()   # HIER wird dein Override aufgerufen
        if tok.type == Token.EOF:
            depth = getattr(lexer, "_cmtDepth", 0)
            if depth > 0:
                line = lexer.line
                col  = lexer.column
                raise UnterminatedBlockCommentError(line, col)
            break
    
    global VISITOR
    VISITOR = ExecVisitor()
    
    # PASS 1: Klassen sammeln
    VISITOR._mode = "collect"
    VISITOR.visit(tree)

    # PASS 2: Statements ausführen
    VISITOR._mode = "exec"
    VISITOR.visit(tree)
    
    for line in VISITOR.output:
        print(line)
    
    #print("Tree  :", tree.toStringTree(recog=parser))
    return tree

# ---------------------------------------------------------------------------
# Qt5 Application stuff ...
# ---------------------------------------------------------------------------
class showException(QDialog):
    def __init__(self, parent=None, etype: str="Ausnahme", message: str=""):
        super().__init__(parent)
        self.setWindowTitle("Demo: " + etype)
        self.resize(320, 200)
        self.message = message
        
        layout = QVBoxLayout(self)
        
        self.text = QTextEdit(self)
        self.text.setText(self.message)
        
        layout.addWidget(self.text)
        
        self.btn = QPushButton("Schließen", self)
        self.btn.clicked.connect(self.on_button_clicked)
        
        layout.addWidget(self.btn)
        
    def on_button_clicked(self):
        self.close()

class SourceAliasesTab(QWidget):
    """
    Tab 'Quell-Aliases' wie Screenshot, inkl. Add/Remove/Edit + nicht-nativer Folder-Dialog.
    model: dict[str, str]  (alias -> path)
    """
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)

        self._model = dict(initial or {})
        self._updating_ui = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---- Oben: Liste ----
        gb_list = QGroupBox("Definierte Quell-Aliases", self)
        v_list = QVBoxLayout(gb_list)

        self.lst = QListWidget()
        self.lst.setMinimumHeight(210)
        v_list.addWidget(self.lst)

        # ---- Unten: Editor ----
        gb_edit = QGroupBox("Quell-Alias bearbeiten", self)
        e = QGridLayout(gb_edit)
        e.setHorizontalSpacing(10)
        e.setVerticalSpacing(8)

        e.addWidget(QLabel("Alias:"), 0, 0)
        self.ed_alias = QLineEdit()
        self.ed_alias.setMinimumWidth(220)
        e.addWidget(self.ed_alias, 0, 1)

        self.btn_add = QPushButton("Hinzufügen")
        self.btn_remove = QPushButton("Entfernen")
        self.btn_add.setFixedWidth(95)
        self.btn_remove.setFixedWidth(95)
        e.addWidget(self.btn_add, 0, 2)
        e.addWidget(self.btn_remove, 0, 3)

        e.addWidget(QLabel("Pfad:"), 1, 0)
        self.ed_path = QLineEdit()
        e.addWidget(self.ed_path, 1, 1, 1, 2)

        self.btn_browse = QPushButton("…")
        self.btn_browse.setFixedWidth(30)
        e.addWidget(self.btn_browse, 1, 3, alignment=Qt.AlignLeft)

        root.addWidget(gb_list)
        root.addWidget(gb_edit)
        root.addStretch(1)

        # Demo / initial
        if not self._model:
            self._model.update({
                "CoreShared": r"T:\Programme\dBASE\dBASE2019\Bin\dBLCore\Shared",
                "dBStartup": r"T:\Programme\dBASE\dBASE2019\Bin\dBStartup",
                "Examples": r"T:\Programme\dBASE\dBASE2019\Examples",
                "Forms": r"T:\Programme\dBASE\dBASE2019\Forms",
                "Images": r"T:\Programme\dBASE\dBASE2019\Images",
            })

        self._reload_list(select_first=True)

        # Signals
        self.lst.currentItemChanged.connect(self._on_list_changed)
        self.btn_add.clicked.connect(self._on_add)
        self.btn_remove.clicked.connect(self._on_remove)
        self.btn_browse.clicked.connect(self._on_browse)

        # optional: Live-Update ins Modell, wenn man Felder verlässt
        self.ed_alias.editingFinished.connect(self._on_edit_finished)
        self.ed_path.editingFinished.connect(self._on_edit_finished)

    # ---------- Public ----------
    def model(self) -> dict:
        """Gibt eine Kopie des Modells zurück."""
        return dict(self._model)

    # ---------- Intern ----------
    def _reload_list(self, select_first=False, select_alias=None):
        self._updating_ui = True
        try:
            self.lst.clear()
            for alias in sorted(self._model.keys(), key=lambda s: s.lower()):
                self.lst.addItem(QListWidgetItem(alias))

            if select_alias:
                items = self.lst.findItems(select_alias, Qt.MatchFixedString)
                if items:
                    self.lst.setCurrentItem(items[0])
            elif select_first and self.lst.count() > 0:
                self.lst.setCurrentRow(0)
        finally:
            self._updating_ui = False

        # falls leer
        self._sync_editor_enabled()

    def _sync_editor_enabled(self):
        has = self.lst.currentItem() is not None
        self.btn_remove.setEnabled(has)

    def _on_list_changed(self, cur, prev):
        if self._updating_ui:
            return
        self._sync_editor_enabled()

        if not cur:
            self.ed_alias.setText("")
            self.ed_path.setText("")
            return

        alias = cur.text()
        path = self._model.get(alias, "")

        self._updating_ui = True
        try:
            self.ed_alias.setText(alias)
            self.ed_path.setText(path)
        finally:
            self._updating_ui = False

    def _normalized_alias(self, s: str) -> str:
        return (s or "").strip()

    def _on_add(self):
        alias = self._normalized_alias(self.ed_alias.text())
        path = (self.ed_path.text() or "").strip()

        if not alias:
            QMessageBox.warning(self, "Fehler", "Bitte einen Alias-Namen eingeben.")
            self.ed_alias.setFocus()
            return

        if not path:
            QMessageBox.warning(self, "Fehler", "Bitte einen Pfad eingeben oder auswählen.")
            self.ed_path.setFocus()
            return

        if alias in self._model:
            r = QMessageBox.question(
                self,
                "Alias existiert bereits",
                f"Der Alias '{alias}' existiert schon.\nSoll der Pfad überschrieben werden?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if r != QMessageBox.Yes:
                return

        self._model[alias] = path
        self._reload_list(select_alias=alias)

    def _on_remove(self):
        cur = self.lst.currentItem()
        if not cur:
            return

        alias = cur.text()
        r = QMessageBox.question(
            self,
            "Entfernen",
            f"Alias '{alias}' wirklich entfernen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if r != QMessageBox.Yes:
            return

        self._model.pop(alias, None)
        self._reload_list(select_first=True)

    def _on_browse(self):
        start_dir = (self.ed_path.text() or "").strip() or ""
        dlg = QFileDialog(self, "Pfad auswählen", start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # <- NICHT NATIV

        if dlg.exec_():
            dirs = dlg.selectedFiles()
            if dirs:
                self.ed_path.setText(dirs[0])

    def _on_edit_finished(self):
        """
        Optional: wenn ein bestehender Alias ausgewählt ist,
        sollen Änderungen an Pfad/Alias (vorsichtig) ins Modell übernommen werden.
        """
        if self._updating_ui:
            return

        cur = self.lst.currentItem()
        if not cur:
            return

        old_alias = cur.text()
        new_alias = self._normalized_alias(self.ed_alias.text())
        new_path = (self.ed_path.text() or "").strip()

        # Nur Pfad geändert?
        if new_alias == old_alias:
            if new_path and self._model.get(old_alias) != new_path:
                self._model[old_alias] = new_path
            return

        # Alias umbenennen (mit Kollisionscheck)
        if not new_alias:
            # revert
            self._updating_ui = True
            try:
                self.ed_alias.setText(old_alias)
            finally:
                self._updating_ui = False
            return

        if new_alias in self._model:
            QMessageBox.warning(self, "Fehler", f"Alias '{new_alias}' existiert bereits.")
            self._updating_ui = True
            try:
                self.ed_alias.setText(old_alias)
            finally:
                self._updating_ui = False
            return

        # rename im model
        old_path = self._model.pop(old_alias, "")
        self._model[new_alias] = new_path or old_path
        self._reload_list(select_alias=new_alias)

class UpperNoSpaceDelegate(QStyledItemDelegate):
    """Editor erzwingt: keine Leerzeichen + (optional) Großbuchstaben."""

    def __init__(self, parent=None, force_upper=True):
        super().__init__(parent)
        self.force_upper = force_upper
        # ^\S*$  => 0..n Nicht-Leerzeichen, keine Spaces/Tabs
        self._validator = QRegularExpressionValidator(QRegularExpression(r"^\S*$"))

    def createEditor(self, parent, option, index):
        ed = QLineEdit(parent)
        ed.setValidator(self._validator)

        if self.force_upper:
            ed.textEdited.connect(lambda t: ed.setText(t.upper()))
        return ed

    def setEditorData(self, editor, index):
        txt = (index.data(Qt.EditRole) or index.data(Qt.DisplayRole) or "")
        editor.setText(txt.upper() if self.force_upper else txt)

    def setModelData(self, editor, model, index):
        txt = editor.text()
        txt = txt.upper() if self.force_upper else txt
        model.setData(index, txt, Qt.EditRole)

class IntOnlyDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, min_value=0, max_value=999999):
        super().__init__(parent)
        self._validator = QIntValidator(min_value, max_value)

    def createEditor(self, parent, option, index):
        ed = QLineEdit(parent)
        ed.setValidator(self._validator)  # verhindert Nicht-Zahlen + Leerzeichen
        return ed

    def setEditorData(self, editor, index):
        editor.setText(str(index.data(Qt.EditRole) or index.data(Qt.DisplayRole) or ""))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)
        
class TypeComboDelegate(QStyledItemDelegate):
    """ComboBox-Editor nur für die Type-Spalte."""

    def __init__(self, type_column: int, parent=None):
        super().__init__(parent)
        self.type_column = type_column

    def createEditor(self, parent, option, index):
        if index.column() != self.type_column:
            return super().createEditor(parent, option, index)

        cb = QComboBox(parent)
        cb.addItems(TYPE_VALUES)
        cb.setEditable(False)
        return cb

    def setEditorData(self, editor, index):
        if index.column() != self.type_column or not isinstance(editor, QComboBox):
            return super().setEditorData(editor, index)

        current = (index.data(Qt.DisplayRole) or "").strip()
        i = editor.findText(current, Qt.MatchFixedString)
        editor.setCurrentIndex(i if i >= 0 else 0)

    def setModelData(self, editor, model, index):
        if index.column() != self.type_column or not isinstance(editor, QComboBox):
            return super().setModelData(editor, model, index)

        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class TableDesignerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Phonebook.dbf - Table Designer")
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)

        layout = QVBoxLayout(self)
        
        self.table = QTableView(self)
        self.model = QStandardItemModel(0, 6, self.table)
        self.proxy = RowMarkerProxy(self.model, self.table)
        self.table.setModel(self.proxy)
        
        #self.table.setColumnCount(6)
        self.model.setHorizontalHeaderLabels(["Field", "Name", "Type", "Width", "Decimal", "Index"])

        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.SelectedClicked |
            QAbstractItemView.EditKeyPressed
        )

        # Delegate auf Spalten
        self.table.setItemDelegateForColumn(4, IntOnlyDelegate     (self.table, min_value=0, max_value=512))
        self.table.setItemDelegateForColumn(3, IntOnlyDelegate     (self.table, min_value=0, max_value=512))
        self.table.setItemDelegateForColumn(2, TypeComboDelegate(2, self.table))
        self.table.setItemDelegateForColumn(1, UpperNoSpaceDelegate(self.table, force_upper=True))

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode    (QAbstractItemView.SingleSelection)
        
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setFixedWidth(24)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        vm = self.table.verticalHeader()
        vm.setFont(QFont("Arial", 14))

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)

        self.table.setColumnWidth(0, 55)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 120)

        layout.addWidget(self.table)
        self.resize(520, 320)

        self._fill_demo_data()

        self.table.selectionModel().currentChanged.connect(self.on_current_changed)
        self.table.selectRow(0)
        
        self.proxy.setCurrentRow(0)
        self.table.selectRow(0)
        
    # Bei Reihenwechsel Marker mitwandern lassen
    def on_current_changed(self, current, previous):
        self.proxy.setCurrentRow(current.row())
        
    def _fill_demo_data(self):
        rows = [
            (1,  "First_Name",    "Character", 25, 0, "None"),
            (2,  "Last_Name",     "Character", 35, 0, "None"),
            (3,  "Sex",           "Character",  1, 0, "None"),
            (4,  "Address",       "Character", 40, 0, "None"),
            (5,  "City",          "Character", 25, 0, "None"),
            (6,  "State_Prov",    "Character", 17, 0, "None"),
            (7,  "Zip_Code",      "Character",  7, 0, "Ascend"),
            (8,  "Long_Distance", "Logical",    1, 0, "None"),
            (9,  "Phone",         "Character", 10, 0, "None"),
            (10, "Fax",           "Character", 10, 0, "None"),
            (11, "Email",         "Character", 40, 0, "None"),
            (12, "Notes",         "Memo",      10, 0, ""),
        ]

        for r, rowdata in enumerate(rows):
            self.model.insertRow(r)
            for c, value in enumerate(rowdata):
                text = str(value)
                
                # 1. Feld (Spalte 0) in Großbuchstaben
                if c == 1:
                    text = text.upper()
                
                self.model.setItem(r, c, QStandardItem(text))

class DBaseParser:
    def __init__(self, filename):
        # 0 pre-procession
        self.pp = Preprocessor(include_paths=[Path("includes")])
        self.pre = self.pp.process(filename)
        
        #source = FileStream(filename, encoding="utf-8")
        self.source  = InputStream       (self.pre)
        self.lexer   = dBaseLexer        (self.source)
        self.tokens  = CommonTokenStream (self.lexer)
        self.tokens.fill();
        self.parser  = dBaseParser       (self.tokens)
        self.tree    = self.parser.input_()
        
class EditorWidget(QDialog):
    def __init__(self, text="abcdef"):
        super().__init__()
        self.setWindowTitle("Demo: dBase 2026")
        self.resize(450, 250)
        
        self.filename = "dbase.prg"

        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        
        # Splitter: links Tree, rechts Editor
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setStyleSheet(
        "QSplitter::handle { background: rgb(200,200,0); }" +
        "QSplitter::handle:hover { background: rgb(200,200,200); }")
        
        self.setStyleSheet("""QDialog { background: #1e1f22; }""")
        
        # --- TreeView links ---
        self.tree = QTreeView(self.splitter)
        self.tree.setStyleSheet("""
QTreeView {
    background: #061226;              /* etwas dunkler als Editor */
    color: #c9b458;                   /* warmes, dunkleres Gelb */
    border: 1px solid #0f2a4a;
    alternate-background-color: #071a33;
    outline: 0;
}
QTreeView::item {
    padding: 4px 6px;
}
QTreeView::item:hover {
    background: #0b2a52;
}
QTreeView::item:selected {
    background: #274b8a;
    color: #f0e6b0;
}
QTreeView::branch {
    background: transparent;
}
/* Header */
QHeaderView::section {
    background: #07162c;
    color: #c9b458;
    padding: 4px 6px;
    border: 0px;
    border-right: 1px solid #0f2a4a;
    border-bottom: 1px solid #0f2a4a;
}
/* Scrollbar (optional, aber sieht sonst schnell “fremd” aus) */
QScrollBar:vertical {
    background: #061226;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #0f2a4a;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
    background: #163a66;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}
""")
        
        # Dummy Model (später kannst du hier Klassen/Methoden/etc. einfüllen)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Struktur"])
        
        root = model.invisibleRootItem()
        
        root.appendRow(QStandardItem("CLASS ParentForm"))
        root.appendRow(QStandardItem("METHOD Init"))
        
        self.tree.setModel(model)
        self.tree.expandAll()
        
        vlayout = QVBoxLayout()

        # Mehrzeiliges Eingabefeld
        self.text = CodeEditor(self.splitter)
        self.text.setPlaceholderText("Schreib hier was rein…")
        self.text.setLineWrapMode(self.text.NoWrap)
        self.text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.text.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.text.setLineWrapMode(self.text.NoWrap)
        self.text.setFont(QFont("Consolas", 10))
        
        self.highlighter = DBaseHighlighter(self.text.document())
        
        # Splitter-Verhältnisse
        self.splitter.setStretchFactor(0, 0)  # Tree
        self.splitter.setStretchFactor(1, 1)  # Editor
        self.splitter.setSizes([220, 800])
        
        vlayout.addWidget(self.splitter)

        # Button
        self.btn_run = GlossyPillButtonGreen("Ausführen" , self)
        self.btn_run.clicked.connect(self.on_button_run_clicked)
        
        vlayout.addWidget(self.btn_run)
        
        h1layout = QHBoxLayout()
        self.btn_gen_python = GlossyPillButtonBlue("Gen. Python Code" , self)
        self.btn_gen_pascal = GlossyPillButtonBlue("Gen. Pascal Code" , self)
        self.btn_gen_javout = GlossyPillButtonBlue("Gen. Jave Code"   , self)
        self.btn_gen_gnucpp = GlossyPillButtonBlue("Gen. GNU C++ Code", self)
        self.btn_gen_csharp = GlossyPillButtonBlue("Gen. C-Sharp Code", self)
        
        self.btn_gen_python.clicked.connect(self.on_button_gen_python_clicked)
        self.btn_gen_pascal.clicked.connect(self.on_button_gen_pascal_clicked)
        self.btn_gen_javout.clicked.connect(self.on_button_gen_javout_clicked)
        self.btn_gen_gnucpp.clicked.connect(self.on_button_gen_gnucpp_clicked)
        self.btn_gen_csharp.clicked.connect(self.on_button_gen_csharp_clicked)
        
        h1layout.addWidget(self.btn_gen_python)
        h1layout.addWidget(self.btn_gen_pascal)
        h1layout.addWidget(self.btn_gen_javout)
        h1layout.addWidget(self.btn_gen_gnucpp)
        h1layout.addWidget(self.btn_gen_csharp)
        
        h2layout = QHBoxLayout()
        self.btn_gen_vbaout = GlossyPillButtonGold("Gen. Visual-Basic Access Code", self)
        self.btn_gen_javscr = GlossyPillButtonGold("Gen. Java Script Code", self)
        
        self.btn_gen_vbaout.clicked.connect(self.on_button_gen_vbaout_clicked)
        self.btn_gen_javscr.clicked.connect(self.on_button_gen_javscr_clicked)
        
        h2layout = QHBoxLayout()
        h2layout.addWidget(self.btn_gen_vbaout)
        h2layout.addWidget(self.btn_gen_javscr)
        
        vlayout.addLayout(h1layout)
        vlayout.addLayout(h2layout)
        
        layout = QVBoxLayout(self)
        layout.addLayout(vlayout)
        
        with open(self.filename, "r", encoding="utf-8") as f:
            content = f.read()
            f.close()
            
        self.text.setPlainText(content)
        
    def close_tracked_windows(self):
        for w in getattr(self, "_open_windows", []):
            if w:
                w.close()
        self._open_windows = []
    
    def closeEvent(self, event):
        self.close_tracked_windows()

    def on_button_gen_vbaout_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToVBAAccess(parser, class_name="GenProg", module_name="GenProg")
        codegen.generate(parser.tree, "dbase.cls")
        print("gen vba ok.")
        
    def on_button_gen_javscr_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToJavaScript(parser, class_name="GenProg", module_name=None)
        codegen.generate(parser.tree, "dbase.js")
        print("gen js ok.")
        
    def on_button_gen_csharp_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToCSharp(parser, class_name="GenProg", namespace=None)
        codegen.generate(parser.tree, "dbase.cs")
        print("gen c-sharp ok.")
        
    def on_button_gen_javout_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToJava(parser, class_name="GenProg", package=None)
        codegen.generate(parser.tree, "dbase.java")
        print("gen java ok.")

    def on_button_gen_python_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToPython(parser.parser)
        codegen.generate(parser.tree, "dbase.py")
        print("gen py ok.")
    
    def on_button_gen_gnucpp_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToCpp(parser, prog_name="genprog")
        codegen.generate(parser.tree, "dbase.cc")
        print("gen c++ ok.")
    
    def on_button_gen_pascal_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToPascal(parser, unit_name="GenProg")
        codegen.generate(parser.tree, "dbase.pas")
        print("gen pas ok.")
    
    def on_button_run_clicked(self):
        # Das ist die Funktion, die beim Klick ausgeführt wird
        content = self.text.toPlainText().strip()
        if not content:
            QMessageBox.information(self, "Info", "Bitte erst Text eingeben.")
            return
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(content)
                f.close()
            res = parse(self.filename)
        except UnterminatedBlockCommentError as e:
            tb_str = (f"error: {e.line}:{e.column}: {e.message}\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))

            dlg = showException(self,
            "Kommentar-Fehler" + type(e).__name__, tb_str)
            dlg.exec_()
        except KeyError as e:
            tb_str = (f"error: {e.name}: {e.message}\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Internal-Fehler" + type(e).__name__, tb_str)
            dlg.exec_()
        except PermissionError as e:
            tb_str = (f"error: Zugriff verweigert\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Zugriff-Fehler" + type(e).__name__, tb_str)
            dlg.exec_()
        except FileNotFoundError as e:
            tb_str = (f"error: Datei nicht gefunden.\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Datei-Fehler" + type(e).__name__, tb_str)
            dlg.exec_()
        except NameError as e:
            msg = str(e)
            m = re.search(r"name '([^']+)' is not defined", msg)
            missing = m.group(1) if m else "<?>"
            message = "Internal Error (Python NameError)\n"
            message = message + f"{missing}: {msg}"
            
            tb_str = (f"Fehler: {message}\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Fehler: " + type(e).__name__, tb_str)
            dlg.exec_()
        except AttributeError as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Attribut-Fehler: " + type(e).__name__, tb_str)
            dlg.exec_()
        except RuntimeError as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Laufzeit-Fehler" + type(e).__name__, tb_str)
            dlg.exec_()
        except SyntaxError as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            "Syntax-Fehler: " + type(e).__name__, tb_str)
            dlg.exec_()
        except Exception as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            traceback.print_exc()
            dlg = showException(self,
            "Allgemeiner Fehler: " + type(e).__name__, tb_str)
            dlg.exec_()

class IconTab(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setWrapping(True)
        self.setWordWrap(True)
        self.setTextElideMode(Qt.ElideRight)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

    def _is_binary_file(self, path: str) -> bool:
        # simple + schnell: NUL-Byte oder sehr viele "komische" bytes
        try:
            with open(path, "rb") as f:
                data = f.read(2048)
            if b"\x00" in data:
                return True
            # Heuristik: Anteil nicht-printbarer Bytes
            # (tab/newline/CR zulassen)
            allowed = set(b"\t\r\n") | set(range(32, 127))
            non = sum(1 for b in data if b not in allowed)
            return len(data) > 0 and (non / max(1, len(data))) > 0.30
        except Exception:
            # wenn wir nicht lesen können → lieber "binär/unknown"
            return True

    def _file_policy(self, path: str):
        # gibt (full_menu: bool) zurück
        ext = os.path.splitext(path)[1].lower()
        if ext in (".txt", ".prg"):
            return True
        # unbekannt oder binär => nur Info
        return False

    def _on_context_menu(self, pos: QPoint):
        item = self.itemAt(pos)
        if not item:
            return

        path = item.data(Qt.UserRole) or ""
        name = item.text()  # Name unter dem Icon

        full_menu = self._file_policy(path)

        menu = QMenu(self)

        act_run   = menu.addAction("Starten / Ausführen")
        act_edit  = menu.addAction("Editieren")
        menu.addSeparator()
        act_ren   = menu.addAction("Umbenennen")
        act_copy  = menu.addAction("Kopieren")
        act_del   = menu.addAction("Löschen")
        menu.addSeparator()
        act_info  = menu.addAction("Dateiinfo")

        # Aktivierung je nach Policy
        act_run.setEnabled(full_menu)
        act_edit.setEnabled(full_menu)
        act_ren.setEnabled(full_menu)
        act_copy.setEnabled(full_menu)
        act_del.setEnabled(full_menu)
        act_info.setEnabled(True)

        chosen = menu.exec_(self.mapToGlobal(pos))
        if not chosen:
            return

        # Aktionen dispatchen:
        if chosen is act_info:
            self._show_file_info(path)
        elif chosen is act_run:
            self._run_file(path)
        elif chosen is act_edit:
            self._edit_file(name, path)
        elif chosen is act_ren:
            self._rename_item(item, path)
        elif chosen is act_copy:
            self._copy_file(path)
        elif chosen is act_del:
            self._delete_file(item, path)

    def _show_file_info(self, path: str):
        try:
            st = os.stat(path)
            QMessageBox.information(
                self,
                "Dateiinfo",
                f"{path}\n\n"
                f"Größe: {st.st_size} Bytes\n"
                f"Ext: {os.path.splitext(path)[1]}\n"
            )
        except Exception as e:
            QMessageBox.warning(self, "Dateiinfo", f"Konnte Info nicht lesen:\n{e}")

    def _run_file(self, path: str):
        # Windows: os.startfile, sonst xdg-open/open
        try:
            if os.name == "nt":
                os.startfile(path)  # noqa
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            QMessageBox.warning(self, "Ausführen", f"Konnte Datei nicht starten:\n{e}")

    def _edit_file(self, name: str, path: str):
        # hier: "name unter icon verwenden" -> name = item.text()
        # real öffnest du aber natürlich über den Pfad.
        # Übergabe an Parent (DirectoryIconDialog), der den CodeEditor öffnen kann:
        
        #dlg = self.window()  # Top-Level window (dein DirectoryIconDialog oder MDI Container)
        #dlg.mdi_open_editor(name, path)
        
        win = FileEditorWindow(parent=MAINAPP, initial_path=path, initial_text="")
        sub = MAINAPP.mdi.addSubWindow(win)
        win.resize(500, 450)
        
        # 1) immer sichtbar + Vordergrund
        win.show()
        win.raise_()
        win.activateWindow()

        # 2) falls minimiert: wieder herstellen
        win.setWindowState(win.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)

        # 3) optional: "Always on top"
        win.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        win.show()  # nach setWindowFlag nochmal show()!
        win.raise_()
        win.activateWindow()

        # Referenz halten (gegen GC)
        self._open_windows = getattr(self, "_open_windows", [])
        self._open_windows.append(win)
        #if hasattr(dlg, "open_in_code_editor"):
        #   dlg.open_in_code_editor(name, path)
        #else:
        #    QMessageBox.warning(self, "Editieren", "open_in_code_editor(...) ist nicht implementiert.")

    def _rename_item(self, item, path: str):
        # minimal: du kannst hier später eine Eingabebox bauen
        QMessageBox.information(self, "Umbenennen", "TODO: Umbenennen implementieren")

    def _copy_file(self, path: str):
        QMessageBox.information(self, "Kopieren", "TODO: Kopieren implementieren")

    def _delete_file(self, item, path: str):
        res = QMessageBox.question(self, "Löschen?", f"Wirklich löschen?\n{path}")
        if res != QMessageBox.Yes:
            return
        try:
            os.remove(path)
            row = self.row(item)
            self.takeItem(row)
        except Exception as e:
            QMessageBox.warning(self, "Löschen", f"Konnte nicht löschen:\n{e}")
            
class DirectoryIconDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFont(QFont("Arial", 10))

        self.setWindowTitle("Directory Icon Browser")
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)

        self.icon_provider = QFileIconProvider()

        # --- Top controls ---
        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.combo.currentTextChanged.connect(self._on_dir_changed)

        self.btn_pick = QPushButton("Verzeichnis…")
        self.btn_pick.clicked.connect(self.pick_directory_non_native)

        top = QHBoxLayout()
        top.addWidget(self.combo, 1)
        top.addWidget(self.btn_pick, 0)

        # --- Tabs ---
        self.tabs = QTabWidget()
        self.icon_lists = []

        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Alle Typen")
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Projekte"  )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Formulare" )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Berichte"  )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Programme" )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Tabellen"  )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "SQL"       )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Grafiken"  )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Internet"  )
        lw = IconTab(); self.icon_lists.append(lw); self.tabs.addTab(lw, "Sonstiges" )

        # --- Layout ---
        root = QVBoxLayout(self)
        root.addLayout(top)
        root.addWidget(self.tabs, 1)

        self.resize(980, 640)

    def open_in_code_editor(self, display_name: str, path: str):
        # display_name ist der Text unter dem Icon (z.B. "foo.prg")
        # path ist der volle Pfad -> den solltest du wirklich öffnen
        # Beispiel: MDI-Variante
        if hasattr(self, "mdi_open_editor"):
            self.mdi_open_editor(title=display_name, text=open(path, "r", encoding="utf-8", errors="replace").read())
            return

        # oder normale Fenster-Variante:
        if hasattr(self, "open_file_editor"):
            self.open_file_editor(path=path, text="")
            return
            
    def pick_directory_non_native(self):
        dlg = QFileDialog(self, "Verzeichnis auswählen")
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)

        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                path = selected[0]
                self._add_and_select_dir(path)

    def _add_and_select_dir(self, path: str):
        path = os.path.normpath(path)

        # Wenn schon drin -> nur markieren
        idx = self.combo.findText(path, Qt.MatchExactly)
        if idx < 0:
            self.combo.addItem(path)
            idx = self.combo.findText(path, Qt.MatchExactly)

        self.combo.setCurrentIndex(idx)  # markiert/selektiert
        # _on_dir_changed() wird automatisch ausgelöst

    def _on_dir_changed(self, path: str):
        path = path.strip()
        if not path or not os.path.isdir(path):
            # Tabs ggf. leeren
            for lw in self.icon_lists:
                lw.clear()
            return
        
        self._fill_all_tabs(path)

    def _fill_all_tabs(self, directory: str):
        # gleiche Anzeige in allen 7 Tabs (kannst du später tab-spezifisch filtern)
        entries = []
        try:
            for name in os.listdir(directory):
                full = os.path.join(directory, name)
                entries.append((name, full))
        except Exception:
            entries = []
        
        for lw in self.icon_lists:
            lw.setUpdatesEnabled(False)
            lw.clear()
            
            for name, full in entries:
                info = QFileInfo(full)
                icon = self.icon_provider.icon(info)
                item = QListWidgetItem(icon, name)
                item.setToolTip(full)
                item.setData(Qt.UserRole, full)
                lw.addItem(item)
            
            lw.setUpdatesEnabled(True)
            
class UserBdeAliasesTab(QWidget):
    """
    Tab 'Benutzer BDE Aliases' wie Screenshot, inkl. Add/Remove/Edit + nicht-native Dialoge.
    Model: dict[str, dict]  alias -> {"driver": str, "options": str}
    """
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)

        self._model = dict(initial or {})
        self._updating_ui = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # -------- Oben: Liste --------
        gb_list = QGroupBox("Definiert ein BDE Anschluss aller", self)
        v_list = QVBoxLayout(gb_list)

        self.lst = QListWidget()
        self.lst.setMinimumHeight(220)
        v_list.addWidget(self.lst)

        # -------- Unten: Editor --------
        gb_edit = QGroupBox("Benutzer BDE Alias bearbeiten", self)
        e = QGridLayout(gb_edit)
        e.setHorizontalSpacing(10)
        e.setVerticalSpacing(8)

        e.addWidget(QLabel("Alias:"), 0, 0)
        self.ed_alias = QLineEdit()
        self.ed_alias.setMinimumWidth(230)
        e.addWidget(self.ed_alias, 0, 1)

        self.btn_add = QPushButton("Hinzufügen")
        self.btn_remove = QPushButton("Entfernen")
        self.btn_add.setFixedWidth(95)
        self.btn_remove.setFixedWidth(95)
        e.addWidget(self.btn_add, 0, 2)
        e.addWidget(self.btn_remove, 0, 3)

        e.addWidget(QLabel("Driver:"), 1, 0)
        self.cb_driver = QComboBox()
        self.cb_driver.setMinimumWidth(260)
        self.cb_driver.addItems([
            "dBASE", "PARADOX", "DB2", "ORACLE", "ODBC", "SQL", "FIREBIRD"
        ])
        e.addWidget(self.cb_driver, 1, 1, 1, 3)

        e.addWidget(QLabel("Options:"), 2, 0)
        self.ed_options = QLineEdit()
        e.addWidget(self.ed_options, 2, 1, 1, 2)

        self.btn_options = QPushButton("…")
        self.btn_options.setFixedWidth(30)
        e.addWidget(self.btn_options, 2, 3, alignment=Qt.AlignLeft)

        root.addWidget(gb_list)
        root.addWidget(gb_edit)
        root.addStretch(1)

        # Demo / initial
        if not self._model:
            self._model.update({
                "dBASEContax": {
                    "driver": "dBASE",
                    "options": r"PATH:C:\Users\Jens Kallup\Documents\Programme\dBASE\dBA..."
                },
                "dBASESamples": {
                    "driver": "dBASE",
                    "options": r"PATH:C:\dBASE\Samples"
                },
                "dBASESignup": {
                    "driver": "dBASE",
                    "options": r"PATH:C:\dBASE\Signup"
                },
                "dBASETemp": {
                    "driver": "dBASE",
                    "options": r"PATH:C:\Temp"
                },
                "DmdDesnTemp": {
                    "driver": "dBASE",
                    "options": r"PATH:C:\Temp\Dmd"
                },
            })

        self._reload_list(select_first=True)

        # Signals
        self.lst.currentItemChanged.connect(self._on_list_changed)
        self.btn_add.clicked.connect(self._on_add)
        self.btn_remove.clicked.connect(self._on_remove)
        self.btn_options.clicked.connect(self._on_options_browse)

        # optional: live update bei editingFinished
        self.ed_alias.editingFinished.connect(self._on_edit_finished)
        self.ed_options.editingFinished.connect(self._on_edit_finished)
        self.cb_driver.currentIndexChanged.connect(lambda *_: self._on_edit_finished())

    # ---------- Public ----------
    def model(self) -> dict:
        return {k: dict(v) for k, v in self._model.items()}

    # ---------- Intern ----------
    def _reload_list(self, select_first=False, select_alias=None):
        self._updating_ui = True
        try:
            self.lst.clear()
            for alias in sorted(self._model.keys(), key=lambda s: s.lower()):
                self.lst.addItem(QListWidgetItem(alias))

            if select_alias:
                items = self.lst.findItems(select_alias, Qt.MatchFixedString)
                if items:
                    self.lst.setCurrentItem(items[0])
            elif select_first and self.lst.count() > 0:
                self.lst.setCurrentRow(0)
        finally:
            self._updating_ui = False

        self._sync_editor_enabled()

    def _sync_editor_enabled(self):
        has = self.lst.currentItem() is not None
        self.btn_remove.setEnabled(has)

    def _on_list_changed(self, cur, prev):
        if self._updating_ui:
            return
        self._sync_editor_enabled()

        if not cur:
            self._updating_ui = True
            try:
                self.ed_alias.setText("")
                self.cb_driver.setCurrentIndex(0)
                self.ed_options.setText("")
            finally:
                self._updating_ui = False
            return

        alias = cur.text()
        rec = self._model.get(alias, {"driver": "dBASE", "options": ""})

        self._updating_ui = True
        try:
            self.ed_alias.setText(alias)
            # Driver setzen
            i = self.cb_driver.findText(rec.get("driver", "dBASE"), Qt.MatchFixedString)
            self.cb_driver.setCurrentIndex(i if i >= 0 else 0)
            self.ed_options.setText(rec.get("options", ""))
        finally:
            self._updating_ui = False

    def _norm(self, s: str) -> str:
        return (s or "").strip()

    def _on_add(self):
        alias = self._norm(self.ed_alias.text())
        driver = self.cb_driver.currentText()
        options = self._norm(self.ed_options.text())

        if not alias:
            QMessageBox.warning(self, "Fehler", "Bitte einen Alias-Namen eingeben.")
            self.ed_alias.setFocus()
            return

        if alias in self._model:
            r = QMessageBox.question(
                self,
                "Alias existiert bereits",
                f"Der Alias '{alias}' existiert schon.\nSoll er überschrieben werden?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if r != QMessageBox.Yes:
                return

        self._model[alias] = {"driver": driver, "options": options}
        self._reload_list(select_alias=alias)

    def _on_remove(self):
        cur = self.lst.currentItem()
        if not cur:
            return
        alias = cur.text()

        r = QMessageBox.question(
            self,
            "Entfernen",
            f"Alias '{alias}' wirklich entfernen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if r != QMessageBox.Yes:
            return

        self._model.pop(alias, None)
        self._reload_list(select_first=True)

    def _on_options_browse(self):
        """
        Im Screenshot ist 'Options' meist PATH:... -> sinnvoll ist ein Directory Picker.
        Wir setzen dann automatisch 'PATH:<dir>'.
        """
        current = self._norm(self.ed_options.text())
        start_dir = ""
        if current.upper().startswith("PATH:"):
            start_dir = current[5:].strip()

        dlg = QFileDialog(self, "Verzeichnis auswählen", start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # <- NICHT NATIV

        if dlg.exec_():
            dirs = dlg.selectedFiles()
            if dirs:
                self.ed_options.setText(f"PATH:{dirs[0]}")

    def _on_edit_finished(self):
        """
        Änderungen am aktuell selektierten Alias ins Model übernehmen.
        Alias-Umbenennung mit Kollisionscheck.
        """
        if self._updating_ui:
            return
        cur = self.lst.currentItem()
        if not cur:
            return

        old_alias = cur.text()
        new_alias = self._norm(self.ed_alias.text())
        driver = self.cb_driver.currentText()
        options = self._norm(self.ed_options.text())

        # nur Werte aktualisieren
        if new_alias == old_alias:
            self._model[old_alias] = {"driver": driver, "options": options}
            return

        if not new_alias:
            # revert
            self._updating_ui = True
            try:
                self.ed_alias.setText(old_alias)
            finally:
                self._updating_ui = False
            return

        if new_alias in self._model:
            QMessageBox.warning(self, "Fehler", f"Alias '{new_alias}' existiert bereits.")
            self._updating_ui = True
            try:
                self.ed_alias.setText(old_alias)
            finally:
                self._updating_ui = False
            return

        # rename
        self._model.pop(old_alias, None)
        self._model[new_alias] = {"driver": driver, "options": options}
        self._reload_list(select_alias=new_alias)

class SourceAliasesTab(QWidget):
    """
    Tab 'Quell-Aliases' wie Screenshot, inkl. Add/Remove/Edit + nicht-nativer Folder-Dialog.
    model: dict[str, str]  (alias -> path)
    """
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)

        self._model = dict(initial or {})
        self._updating_ui = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---- Oben: Liste ----
        gb_list = QGroupBox("Definierte Quell-Aliases", self)
        v_list = QVBoxLayout(gb_list)

        self.lst = QListWidget()
        self.lst.setMinimumHeight(210)
        v_list.addWidget(self.lst)

        # ---- Unten: Editor ----
        gb_edit = QGroupBox("Quell-Alias bearbeiten", self)
        e = QGridLayout(gb_edit)
        e.setHorizontalSpacing(10)
        e.setVerticalSpacing(8)

        e.addWidget(QLabel("Alias:"), 0, 0)
        self.ed_alias = QLineEdit()
        self.ed_alias.setMinimumWidth(220)
        e.addWidget(self.ed_alias, 0, 1)

        self.btn_add = QPushButton("Hinzufügen")
        self.btn_remove = QPushButton("Entfernen")
        self.btn_add.setFixedWidth(95)
        self.btn_remove.setFixedWidth(95)
        e.addWidget(self.btn_add, 0, 2)
        e.addWidget(self.btn_remove, 0, 3)

        e.addWidget(QLabel("Pfad:"), 1, 0)
        self.ed_path = QLineEdit()
        e.addWidget(self.ed_path, 1, 1, 1, 2)

        self.btn_browse = QPushButton("…")
        self.btn_browse.setFixedWidth(30)
        e.addWidget(self.btn_browse, 1, 3, alignment=Qt.AlignLeft)

        root.addWidget(gb_list)
        root.addWidget(gb_edit)
        root.addStretch(1)

        # Demo / initial
        if not self._model:
            self._model.update({
                "CoreShared": r"T:\Programme\dBASE\dBASE2019\Bin\dBLCore\Shared",
                "dBStartup": r"T:\Programme\dBASE\dBASE2019\Bin\dBStartup",
                "Examples": r"T:\Programme\dBASE\dBASE2019\Examples",
                "Forms": r"T:\Programme\dBASE\dBASE2019\Forms",
                "Images": r"T:\Programme\dBASE\dBASE2019\Images",
            })

        self._reload_list(select_first=True)

        # Signals
        self.lst.currentItemChanged.connect(self._on_list_changed)
        self.btn_add.clicked.connect(self._on_add)
        self.btn_remove.clicked.connect(self._on_remove)
        self.btn_browse.clicked.connect(self._on_browse)

        # optional: Live-Update ins Modell, wenn man Felder verlässt
        self.ed_alias.editingFinished.connect(self._on_edit_finished)
        self.ed_path.editingFinished.connect(self._on_edit_finished)

    # ---------- Public ----------
    def model(self) -> dict:
        """Gibt eine Kopie des Modells zurück."""
        return dict(self._model)

    # ---------- Intern ----------
    def _reload_list(self, select_first=False, select_alias=None):
        self._updating_ui = True
        try:
            self.lst.clear()
            for alias in sorted(self._model.keys(), key=lambda s: s.lower()):
                self.lst.addItem(QListWidgetItem(alias))

            if select_alias:
                items = self.lst.findItems(select_alias, Qt.MatchFixedString)
                if items:
                    self.lst.setCurrentItem(items[0])
            elif select_first and self.lst.count() > 0:
                self.lst.setCurrentRow(0)
        finally:
            self._updating_ui = False

        # falls leer
        self._sync_editor_enabled()

    def _sync_editor_enabled(self):
        has = self.lst.currentItem() is not None
        self.btn_remove.setEnabled(has)

    def _on_list_changed(self, cur, prev):
        if self._updating_ui:
            return
        self._sync_editor_enabled()

        if not cur:
            self.ed_alias.setText("")
            self.ed_path.setText("")
            return

        alias = cur.text()
        path = self._model.get(alias, "")

        self._updating_ui = True
        try:
            self.ed_alias.setText(alias)
            self.ed_path.setText(path)
        finally:
            self._updating_ui = False

    def _normalized_alias(self, s: str) -> str:
        return (s or "").strip()

    def _on_add(self):
        alias = self._normalized_alias(self.ed_alias.text())
        path = (self.ed_path.text() or "").strip()

        if not alias:
            QMessageBox.warning(self, "Fehler", "Bitte einen Alias-Namen eingeben.")
            self.ed_alias.setFocus()
            return

        if not path:
            QMessageBox.warning(self, "Fehler", "Bitte einen Pfad eingeben oder auswählen.")
            self.ed_path.setFocus()
            return

        if alias in self._model:
            r = QMessageBox.question(
                self,
                "Alias existiert bereits",
                f"Der Alias '{alias}' existiert schon.\nSoll der Pfad überschrieben werden?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if r != QMessageBox.Yes:
                return

        self._model[alias] = path
        self._reload_list(select_alias=alias)

    def _on_remove(self):
        cur = self.lst.currentItem()
        if not cur:
            return

        alias = cur.text()
        r = QMessageBox.question(
            self,
            "Entfernen",
            f"Alias '{alias}' wirklich entfernen?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if r != QMessageBox.Yes:
            return

        self._model.pop(alias, None)
        self._reload_list(select_first=True)

    def _on_browse(self):
        start_dir = (self.ed_path.text() or "").strip() or ""
        dlg = QFileDialog(self, "Pfad auswählen", start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # <- NICHT NATIV

        if dlg.exec_():
            dirs = dlg.selectedFiles()
            if dirs:
                self.ed_path.setText(dirs[0])

    def _on_edit_finished(self):
        """
        Optional: wenn ein bestehender Alias ausgewählt ist,
        sollen Änderungen an Pfad/Alias (vorsichtig) ins Modell übernommen werden.
        """
        if self._updating_ui:
            return

        cur = self.lst.currentItem()
        if not cur:
            return

        old_alias = cur.text()
        new_alias = self._normalized_alias(self.ed_alias.text())
        new_path = (self.ed_path.text() or "").strip()

        # Nur Pfad geändert?
        if new_alias == old_alias:
            if new_path and self._model.get(old_alias) != new_path:
                self._model[old_alias] = new_path
            return

        # Alias umbenennen (mit Kollisionscheck)
        if not new_alias:
            # revert
            self._updating_ui = True
            try:
                self.ed_alias.setText(old_alias)
            finally:
                self._updating_ui = False
            return

        if new_alias in self._model:
            QMessageBox.warning(self, "Fehler", f"Alias '{new_alias}' existiert bereits.")
            self._updating_ui = True
            try:
                self.ed_alias.setText(old_alias)
            finally:
                self._updating_ui = False
            return

        # rename im model
        old_path = self._model.pop(old_alias, "")
        self._model[new_alias] = new_path or old_path
        self._reload_list(select_alias=new_alias)
        
class DesktopPropertiesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setWindowTitle("Desktop Properties")
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)

        root = QVBoxLayout(self)

        # Tabs
        self.tabs = QTabWidget(self)
        root.addWidget(self.tabs)

        # Platzhalter-Tabs (wie im Bild)
        self.tabs.addTab(self._build_tab_country (), "Country")
        self.tabs.addTab(self._build_tab_table   (), "Table")
        self.tabs.addTab(self._build_tab_data    (), "Data Entry")
        self.tabs.addTab(self._build_tab_files   (), "Files")
        self.tabs.addTab(self._build_tab_app     (), "Application")
        self.tabs.addTab(self._build_tab_prog    (), "Programming")
        self.tabs.addTab(self._build_tab_aliase  (), "Source Aliases")
        self.tabs.addTab(self._build_tab_usrbde  (), "User-BDE-Aliases")
        
        # Bottom buttons: OK / Abbrechen / Hilfe / Übernehmen
        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.btn_ok     = QPushButton("OK")
        self.btn_cancel = QPushButton("Abbrechen")
        self.btn_help   = QPushButton("Hilfe")
        self.btn_apply  = QPushButton("Übernehmen")

        for b in (self.btn_ok, self.btn_cancel, self.btn_help, self.btn_apply):
            b.setFixedWidth(95)

        self.btn_ok    .clicked.connect(self.onbtn_accept)
        self.btn_cancel.clicked.connect(self.onbtn_cancel)
        self.btn_help  .clicked.connect(lambda: None)   # später füllen
        self.btn_apply .clicked.connect(lambda: None)  # später füllen

        btn_row.addWidget(self.btn_ok)
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_help)
        btn_row.addWidget(self.btn_apply)

        root.addLayout(btn_row)

        self.resize(520, 360)
    
    def onbtn_accept(self):
        self.accept()
        self.mdi.close()
        
    def onbtn_cancel(self):
        self.reject()
        self.mdi.close()

    def _build_tab_aliase(self) -> QWidget:
        tab = QWidget()
        SourceAliasesTab(tab)
        return tab
    
    def _build_tab_usrbde(self) -> QWidget:
        tab = QWidget()
        UserBdeAliasesTab(tab)
        return tab

    def _build_tab_country(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        # --- Zahlenwerte ---
        gb_num = QGroupBox("Zahlenwerte", tab)
        num = QGridLayout(gb_num)
        num.setHorizontalSpacing(10)
        num.setVerticalSpacing(8)

        num.addWidget(QLabel("Trennzeichen:"), 0, 0)
        self.ed_thousand = QLineEdit(".")
        self.ed_thousand.setFixedWidth(34)
        num.addWidget(self.ed_thousand, 0, 1, alignment=Qt.AlignLeft)

        num.addWidget(QLabel("Dezimalzeichen:"), 1, 0)
        self.ed_decimal = QLineEdit(",")
        self.ed_decimal.setFixedWidth(34)
        num.addWidget(self.ed_decimal, 1, 1, alignment=Qt.AlignLeft)

        num.addWidget(QLabel("Muster:"), 2, 0)
        num.addWidget(QLabel("1.000.000,00"), 2, 1, 1, 2)

        # --- Währungssymbol ---
        gb_cur = QGroupBox("Währungssymbol", tab)
        cur = QGridLayout(gb_cur)
        cur.setHorizontalSpacing(10)
        cur.setVerticalSpacing(8)

        cur.addWidget(QLabel("Position:"), 0, 0)
        self.rb_left = QRadioButton("Links")
        self.rb_right = QRadioButton("Rechts")
        self.rb_right.setChecked(True)
        cur.addWidget(self.rb_left, 0, 1)
        cur.addWidget(self.rb_right, 1, 1)

        cur.addWidget(QLabel("Symbol:"), 2, 0)
        self.ed_currency = QLineEdit("€")
        self.ed_currency.setFixedWidth(50)
        cur.addWidget(self.ed_currency, 2, 1, alignment=Qt.AlignLeft)

        cur.addWidget(QLabel("Muster:"), 3, 0)
        cur.addWidget(QLabel("129,99 €"), 3, 1, 1, 2)

        # --- Datum ---
        gb_date = QGroupBox("Datum", tab)
        date = QGridLayout(gb_date)
        date.setHorizontalSpacing(10)
        date.setVerticalSpacing(8)

        date.addWidget(QLabel("Datumsformat:"), 0, 0)
        self.cb_datefmt = QComboBox()
        self.cb_datefmt.addItems(["DMY", "MDY", "YMD", "ISO"])
        self.cb_datefmt.setCurrentText("DMY")
        self.cb_datefmt.setFixedWidth(120)
        date.addWidget(self.cb_datefmt, 0, 1, alignment=Qt.AlignLeft)

        date.addWidget(QLabel("Datumszeichen:"), 1, 0)
        self.ed_datesep = QLineEdit(".")
        self.ed_datesep.setFixedWidth(34)
        date.addWidget(self.ed_datesep, 1, 1, alignment=Qt.AlignLeft)

        self.chk_century = QCheckBox("Jahrhundert")
        self.chk_century.setChecked(True)
        date.addWidget(self.chk_century, 2, 0, 1, 2)

        date.addWidget(QLabel("Muster:"), 3, 0)
        date.addWidget(QLabel("08.02.2026"), 3, 1, 1, 2)

        # --- Umgebungssprache ---
        gb_ui = QGroupBox("Umgebungssprache", tab)
        ui = QGridLayout(gb_ui)
        self.cb_lang = QComboBox()
        self.cb_lang.addItems(["DE - Deutsch", "EN - English", "FR - Français"])
        self.cb_lang.setCurrentText("DE - Deutsch")
        self.cb_lang.setFixedWidth(160)
        ui.addWidget(self.cb_lang, 0, 0)

        # --- Sprachtreiber ---
        gb_drv = QGroupBox("Sprachtreiber", tab)
        drv = QGridLayout(gb_drv)
        self.chk_mismatch = QCheckBox("Warnung bei Konflikten")
        drv.addWidget(self.chk_mismatch, 0, 0)

        # Positionierung wie Screenshot
        g.addWidget(gb_num, 0, 0)
        g.addWidget(gb_date, 0, 1)
        g.addWidget(gb_cur, 1, 0)
        g.addWidget(gb_ui, 1, 1)
        g.addWidget(gb_drv, 2, 1)

        g.setRowStretch(3, 1)
        return tab
    
    def _build_tab_table(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        # --- Mehrplatz (links oben) ---
        gb_multi = QGroupBox("Mehrplatz", tab)
        l_multi = QGridLayout(gb_multi)
        l_multi.setHorizontalSpacing(10)
        l_multi.setVerticalSpacing(8)

        self.chk_lock = QCheckBox("Sperren")
        self.chk_exclusive = QCheckBox("Exklusiv")

        l_multi.addWidget(self.chk_lock, 0, 0, 1, 2)
        l_multi.addWidget(self.chk_exclusive, 1, 0, 1, 2)

        l_multi.addWidget(QLabel("Aktualisieren:"), 2, 0)
        self.spin_refresh = QSpinBox()
        self.spin_refresh.setRange(0, 9999)
        self.spin_refresh.setFixedWidth(70)
        l_multi.addWidget(self.spin_refresh, 2, 1, alignment=Qt.AlignLeft)

        l_multi.addWidget(QLabel("Wiederholen:"), 3, 0)
        self.spin_retry = QSpinBox()
        self.spin_retry.setRange(0, 9999)
        self.spin_retry.setFixedWidth(70)
        l_multi.addWidget(self.spin_retry, 3, 1, alignment=Qt.AlignLeft)

        # default wie Screenshot
        self.chk_lock.setChecked(True)

        # --- Standardtabellentyp (links mitte) ---
        gb_default = QGroupBox("Standardtabellentyp", tab)
        l_def = QVBoxLayout(gb_default)
        
        self.rb_dbase   = QRadioButton("dBASE")
        self.rb_paradox = QRadioButton("Paradox")
        self.rb_sqlite3 = QRadioButton("SQLite 3")
        self.rb_mysql   = QRadioButton("MySQL")
        
        self.rb_dbase.setChecked(True)
        
        l_def.addWidget(self.rb_dbase)
        l_def.addWidget(self.rb_paradox)
        l_def.addWidget(self.rb_sqlite3)
        l_def.addWidget(self.rb_mysql)

        # --- Systemtabellen (links unten) ---
        gb_system = QGroupBox("Systemtabellen", tab)
        l_sys = QVBoxLayout(gb_system)
        self.chk_system_show = QCheckBox("Anzeigen")
        l_sys.addWidget(self.chk_system_show)

        # --- Blockgrößen (rechts oben) ---
        gb_blocks = QGroupBox("Blockgrößen", tab)
        l_blocks = QGridLayout(gb_blocks)
        l_blocks.setHorizontalSpacing(10)
        l_blocks.setVerticalSpacing(8)

        l_blocks.addWidget(QLabel("Indexblock:"), 0, 0)
        self.spin_indexblock = QSpinBox()
        self.spin_indexblock.setRange(1, 9999)
        self.spin_indexblock.setFixedWidth(80)
        self.spin_indexblock.setValue(1)
        l_blocks.addWidget(self.spin_indexblock, 0, 1, alignment=Qt.AlignLeft)

        l_blocks.addWidget(QLabel("Memoblock:"), 1, 0)
        self.spin_memoblock = QSpinBox()
        self.spin_memoblock.setRange(1, 9999)
        self.spin_memoblock.setFixedWidth(80)
        self.spin_memoblock.setValue(8)
        l_blocks.addWidget(self.spin_memoblock, 1, 1, alignment=Qt.AlignLeft)

        # --- Andere (rechts mitte) ---
        gb_other = QGroupBox("Andere", tab)
        l_other = QGridLayout(gb_other)
        l_other.setHorizontalSpacing(10)
        l_other.setVerticalSpacing(6)

        self.chk_autosave = QCheckBox("Automatische Speicherung")
        self.chk_deleted = QCheckBox("Löschmarken")
        self.chk_encrypt = QCheckBox("Verschlüsselung")
        self.chk_ident = QCheckBox("Identisch")
        self.chk_approx = QCheckBox("Annähernd")
        self.chk_autonull = QCheckBox("AutoNullFields")

        # wie Screenshot: Löschmarken + Verschlüsselung + AutoNullFields aktiv
        self.chk_deleted.setChecked(True)
        self.chk_encrypt.setChecked(True)
        self.chk_autonull.setChecked(True)

        l_other.addWidget(self.chk_autosave, 0, 0, 1, 2)
        l_other.addWidget(self.chk_deleted, 1, 0, 1, 2)
        l_other.addWidget(self.chk_encrypt, 2, 0, 1, 2)
        l_other.addWidget(self.chk_ident, 3, 0)
        l_other.addWidget(self.chk_approx, 4, 0)
        l_other.addWidget(self.chk_autonull, 3, 1)

        self.btn_components = QPushButton("Komponententypen zuordnen...")
        self.btn_components.setFixedWidth(220)
        l_other.addWidget(self.btn_components, 5, 0, 1, 2, alignment=Qt.AlignLeft)

        # Positionen im Grid wie im Bild
        g.addWidget(gb_multi,   0, 0)
        g.addWidget(gb_blocks,  0, 1)
        g.addWidget(gb_default, 1, 0)
        g.addWidget(gb_other,   1, 1)
        g.addWidget(gb_system,  2, 0)

        # etwas Luft nach unten/rechts
        g.setRowStretch(3, 1)
        g.setColumnStretch(2, 1)
        
        return tab
    
    def _build_tab_app(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        # --- Experten anzeigen (links oben) ---
        gb_exp = QGroupBox("Experten anzeigen", tab)
        exp = QVBoxLayout(gb_exp)
        exp.setSpacing(6)

        chk_form = QCheckBox("Formular")
        chk_report = QCheckBox("Report")
        chk_labels = QCheckBox("Etiketten")
        chk_datamodule = QCheckBox("Datenmodul")
        chk_table = QCheckBox("Tabelle")

        # wie Screenshot: alle an
        for c in (chk_form, chk_report, chk_labels, chk_datamodule, chk_table):
            c.setChecked(True)
            exp.addWidget(c)

        # --- Dateimenü (links unten) ---
        gb_file = QGroupBox("Dateimenü", tab)
        fm = QGridLayout(gb_file)
        fm.setHorizontalSpacing(10)
        fm.setVerticalSpacing(8)

        fm.addWidget(QLabel("Anzahl Dateien:"), 0, 0)
        sp_files = QSpinBox()
        sp_files.setRange(0, 99)
        sp_files.setValue(5)
        sp_files.setFixedWidth(80)
        fm.addWidget(sp_files, 0, 1, alignment=Qt.AlignLeft)

        fm.addWidget(QLabel("Anzahl Projekte:"), 1, 0)
        sp_projects = QSpinBox()
        sp_projects.setRange(0, 99)
        sp_projects.setValue(5)
        sp_projects.setFixedWidth(80)
        fm.addWidget(sp_projects, 1, 1, alignment=Qt.AlignLeft)

        # --- Datenbank (rechts oben) ---
        gb_db = QGroupBox("Datenbank", tab)
        db = QVBoxLayout(gb_db)
        db.setSpacing(6)

        chk_login = QCheckBox("Anmeldungen sichern")
        chk_sqltrace = QCheckBox("SQL-Ablaufverfolgung")
        chk_login.setChecked(True)
        db.addWidget(chk_login)
        db.addWidget(chk_sqltrace)

        # --- Fenster (rechts mitte) ---
        gb_win = QGroupBox("Fenster", tab)
        win = QVBoxLayout(gb_win)
        win.setSpacing(6)

        chk_fit = QCheckBox("Fenstergröße an Inhalt anpassen")
        chk_anim = QCheckBox("Animationen endlos abspielen")
        chk_ole = QCheckBox("Objekte als OLE 2.0 speichern")

        # wie Screenshot: alle 3 an
        chk_fit.setChecked(True)
        chk_anim.setChecked(True)
        chk_ole.setChecked(True)

        win.addWidget(chk_fit)
        win.addWidget(chk_anim)
        win.addWidget(chk_ole)

        # --- Andere (rechts unten) ---
        gb_other = QGroupBox("Andere", tab)
        other = QVBoxLayout(gb_other)
        other.setSpacing(6)

        chk_splash = QCheckBox("Startbildschirm")
        chk_splash.setChecked(True)
        other.addWidget(chk_splash)

        # Layout wie im Screenshot:
        # links: Experten anzeigen + Dateimenü
        # rechts: Datenbank + Fenster + Andere
        g.addWidget(gb_exp,   0, 0)
        g.addWidget(gb_db,    0, 1)
        g.addWidget(gb_file,  1, 0)
        g.addWidget(gb_win,   1, 1)
        g.addWidget(gb_other, 2, 1)

        g.setRowStretch(3, 1)
        return tab
    
    def _build_tab_files(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        # ---------- Pfad (links oben) ----------
        gb_path = QGroupBox("Pfad", tab)
        path = QGridLayout(gb_path)
        path.setHorizontalSpacing(10)
        path.setVerticalSpacing(8)

        path.addWidget(QLabel("Aktuelles Verzeichnis:"), 0, 0, 1, 2)

        # Zeile: Combo/Text + Folder Button
        self_cur_dir = QLineEdit(r"F:\Heinz\ext\irgl\...")
        self_cur_dir.setMinimumWidth(240)
        btn_cur_browse = QPushButton("📁")
        btn_cur_browse.setFixedWidth(30)

        path.addWidget(self_cur_dir, 1, 0)
        path.addWidget(btn_cur_browse, 1, 1, alignment=Qt.AlignLeft)

        path.addWidget(QLabel("Suchpfad:"), 2, 0, 1, 2)

        self_search_path = QLineEdit("")
        btn_search_browse = QPushButton("📁")
        btn_search_browse.setFixedWidth(30)

        path.addWidget(self_search_path, 3, 0)
        path.addWidget(btn_search_browse, 3, 1, alignment=Qt.AlignLeft)

        # ---------- Ausgabeprotokoll (links unten) ----------
        gb_log = QGroupBox("Ausgabeprotokoll", tab)
        log = QGridLayout(gb_log)
        log.setHorizontalSpacing(10)
        log.setVerticalSpacing(8)

        chk_enable_log = QCheckBox("Protokoll anlegen")
        log.addWidget(chk_enable_log, 0, 0, 1, 2)

        log.addWidget(QLabel("Name der Protokolldatei:"), 1, 0, 1, 2)

        ed_logfile = QLineEdit("")
        ed_logfile.setEnabled(False)
        btn_logfile = QPushButton("✎")
        btn_logfile.setFixedWidth(30)
        btn_logfile.setEnabled(False)

        log.addWidget(ed_logfile, 2, 0)
        log.addWidget(btn_logfile, 2, 1, alignment=Qt.AlignLeft)

        rb_overwrite = QRadioButton("Überschreiben")
        rb_append = QRadioButton("Anhängen")
        rb_overwrite.setEnabled(False)
        rb_append.setEnabled(False)
        rb_overwrite.setChecked(True)

        log.addWidget(rb_overwrite, 3, 0, 1, 2)
        log.addWidget(rb_append, 4, 0, 1, 2)

        # Enable/Disable abhängig von Checkbox
        def _toggle_log(on: bool):
            ed_logfile.setEnabled(on)
            btn_logfile.setEnabled(on)
            rb_overwrite.setEnabled(on)
            rb_append.setEnabled(on)

        chk_enable_log.toggled.connect(_toggle_log)

        # ---------- Editor (rechts oben) ----------
        gb_editor = QGroupBox("Editor", tab)
        ed = QGridLayout(gb_editor)
        ed.setHorizontalSpacing(10)
        ed.setVerticalSpacing(8)

        ed.addWidget(QLabel("Externer Quelltext-Editor:"), 0, 0, 1, 2)

        ed_editor = QLineEdit("")
        btn_editor = QPushButton("✎")
        btn_editor.setFixedWidth(30)

        ed.addWidget(ed_editor, 1, 0)
        ed.addWidget(btn_editor, 1, 1, alignment=Qt.AlignLeft)

        # ---------- Andere (rechts mitte) ----------
        gb_other = QGroupBox("Andere", tab)
        other = QVBoxLayout(gb_other)
        other.setSpacing(6)

        chk_backup = QCheckBox("Sicherungsdateien")
        chk_sessions = QCheckBox("Arbeitssitzungen")
        other.addWidget(chk_backup)
        other.addWidget(chk_sessions)

        # Layout wie Screenshot
        g.addWidget(gb_path,   0, 0)
        g.addWidget(gb_editor, 0, 1)
        g.addWidget(gb_log,    1, 0)
        g.addWidget(gb_other,  1, 1)

        g.setRowStretch(2, 1)
        return tab
    
    def _build_tab_data(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        # ---------- Tastatur (links oben) ----------
        gb_kbd = QGroupBox("Tastatur", tab)
        kbd = QGridLayout(gb_kbd)
        kbd.setHorizontalSpacing(10)
        kbd.setVerticalSpacing(8)

        chk_confirm = QCheckBox("Bestätigung")
        chk_cua = QCheckBox("CUA-Eingabe")
        chk_esc = QCheckBox("Escape")

        # wie Screenshot: alle 3 an
        chk_confirm.setChecked(True)
        chk_cua.setChecked(True)
        chk_esc.setChecked(True)

        kbd.addWidget(chk_confirm, 0, 0, 1, 2)
        kbd.addWidget(chk_cua,     1, 0, 1, 2)
        kbd.addWidget(chk_esc,     2, 0, 1, 2)

        kbd.addWidget(QLabel("Tastaturpuffer:"), 3, 0)
        sp_buf = QSpinBox()
        sp_buf.setRange(0, 9999)
        sp_buf.setValue(49)
        sp_buf.setFixedWidth(90)
        kbd.addWidget(sp_buf, 3, 1, alignment=Qt.AlignLeft)

        # ---------- Andere (links unten) ----------
        gb_other = QGroupBox("Andere", tab)
        other = QGridLayout(gb_other)
        other.setHorizontalSpacing(10)
        other.setVerticalSpacing(8)

        other.addWidget(QLabel("Epoche:"), 0, 0)
        sp_epoch = QSpinBox()
        sp_epoch.setRange(0, 9999)
        sp_epoch.setValue(1950)
        sp_epoch.setFixedWidth(90)
        other.addWidget(sp_epoch, 0, 1, alignment=Qt.AlignLeft)

        # ---------- Signalton (rechts) ----------
        gb_beep = QGroupBox("Signalton", tab)
        beep = QGridLayout(gb_beep)
        beep.setHorizontalSpacing(10)
        beep.setVerticalSpacing(8)

        chk_beep = QCheckBox("Einschalten")
        chk_beep.setChecked(True)
        beep.addWidget(chk_beep, 0, 0, 1, 2)

        beep.addWidget(QLabel("Frequenz:"), 1, 0)
        sp_freq = QSpinBox()
        sp_freq.setRange(0, 20000)
        sp_freq.setValue(512)
        sp_freq.setFixedWidth(90)
        beep.addWidget(sp_freq, 1, 1, alignment=Qt.AlignLeft)

        beep.addWidget(QLabel("Dauer:"), 2, 0)
        sp_dur = QSpinBox()
        sp_dur.setRange(0, 10000)
        sp_dur.setValue(50)
        sp_dur.setFixedWidth(90)
        beep.addWidget(sp_dur, 2, 1, alignment=Qt.AlignLeft)

        btn_test = QPushButton("Prüfen")
        btn_test.setFixedWidth(95)
        beep.addWidget(btn_test, 3, 0, 1, 2, alignment=Qt.AlignLeft)

        # Aktivieren/Deaktivieren je nach Einschalten
        def _toggle_beep(on: bool):
            sp_freq.setEnabled(on)
            sp_dur.setEnabled(on)
            btn_test.setEnabled(on)

        chk_beep.toggled.connect(_toggle_beep)
        _toggle_beep(True)

        # Optional: wirklich piepen
        def _do_beep():
            # QApplication.beep() ist plattformabhängig, reicht aber als "Test"
            from PyQt5.QtWidgets import QApplication
            QApplication.beep()

        btn_test.clicked.connect(_do_beep)

        # Layout wie Screenshot
        g.addWidget(gb_kbd,   0, 0)
        g.addWidget(gb_beep,  0, 1, 2, 1)
        g.addWidget(gb_other, 1, 0)

        g.setRowStretch(2, 1)
        return tab
    
    def _build_tab_prog(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        # --- Befehlsausgabe (links oben) ---
        gb_out = QGroupBox("Befehlsausgabe", tab)
        out = QGridLayout(gb_out)
        out.setHorizontalSpacing(10)
        out.setVerticalSpacing(8)

        out.addWidget(QLabel("Dezimalstellen:"), 0, 0)
        sp_dec = QSpinBox()
        sp_dec.setRange(0, 20)
        sp_dec.setValue(2)
        sp_dec.setFixedWidth(80)
        out.addWidget(sp_dec, 0, 1, alignment=Qt.AlignLeft)

        out.addWidget(QLabel("Genauigkeit:"), 1, 0)
        sp_prec = QSpinBox()
        sp_prec.setRange(0, 20)
        sp_prec.setValue(10)
        sp_prec.setFixedWidth(80)
        out.addWidget(sp_prec, 1, 1, alignment=Qt.AlignLeft)

        out.addWidget(QLabel("Rand:"), 2, 0)
        sp_margin = QSpinBox()
        sp_margin.setRange(0, 999)
        sp_margin.setValue(0)
        sp_margin.setFixedWidth(80)
        out.addWidget(sp_margin, 2, 1, alignment=Qt.AlignLeft)

        chk_blank = QCheckBox("Leerzeichen")
        chk_trace = QCheckBox("Ablaufverfolgung")
        chk_fieldnames = QCheckBox("Feldnamen")

        # wie Screenshot: Leerzeichen + Feldnamen an
        chk_blank.setChecked(True)
        chk_fieldnames.setChecked(True)

        out.addWidget(chk_blank, 3, 0, 1, 2)
        out.addWidget(chk_trace, 4, 0, 1, 2)
        out.addWidget(chk_fieldnames, 5, 0, 1, 2)

        # --- Programmentwicklung (rechts oben) ---
        gb_dev = QGroupBox("Programmentwicklung", tab)
        dev = QGridLayout(gb_dev)
        dev.setHorizontalSpacing(10)
        dev.setVerticalSpacing(8)

        chk_fulltest = QCheckBox("Volltest")
        chk_buildtime = QCheckBox("Erstellungszeit")
        chk_buildtime.setChecked(True)

        dev.addWidget(chk_fulltest, 0, 0, 1, 2)
        dev.addWidget(chk_buildtime, 1, 0, 1, 2)

        # --- Andere (rechts mitte) ---
        gb_other = QGroupBox("Andere", tab)
        other = QGridLayout(gb_other)
        other.setHorizontalSpacing(10)
        other.setVerticalSpacing(8)

        chk_design = QCheckBox("Design")
        chk_hiprec = QCheckBox("High Precision")
        chk_protect = QCheckBox("Änderungsschutz")
        chk_fullpath = QCheckBox("Vollständige Pfadangabe")

        # wie Screenshot: Design + Änderungsschutz an
        chk_design.setChecked(True)
        chk_protect.setChecked(True)

        other.addWidget(chk_design, 0, 0)
        other.addWidget(chk_hiprec, 0, 1)
        other.addWidget(chk_protect, 1, 0, 1, 2)
        other.addWidget(chk_fullpath, 2, 0, 1, 2)

        # --- Error Handling (unten, über beide Spalten) ---
        gb_err = QGroupBox("Error Handling", tab)
        err = QGridLayout(gb_err)
        err.setHorizontalSpacing(10)
        err.setVerticalSpacing(8)

        err.addWidget(QLabel("Error Action:"), 0, 0)
        cb_action = QComboBox()
        cb_action.addItems([
            "0 - Ignore",
            "1 - Message",
            "2 - Log",
            "3 - Abort",
            "4 - Show Error Dialog",
        ])
        cb_action.setCurrentText("4 - Show Error Dialog")
        cb_action.setMinimumWidth(260)
        err.addWidget(cb_action, 0, 1, 1, 2)

        # Error Log File + browse button
        err.addWidget(QLabel("Error Log File:"), 1, 0)
        ed_log = QLineEdit("PLUSerr.log")
        err.addWidget(ed_log, 1, 1)
        btn_log = QPushButton("...")
        btn_log.setFixedWidth(28)
        err.addWidget(btn_log, 1, 2, alignment=Qt.AlignLeft)

        # Maximum Size + unit label
        err.addWidget(QLabel("Maximum Size:"), 2, 0)
        sp_max = QSpinBox()
        sp_max.setRange(0, 999999)
        sp_max.setValue(100)
        sp_max.setFixedWidth(90)
        err.addWidget(sp_max, 2, 1, alignment=Qt.AlignLeft)
        err.addWidget(QLabel("Kilobytes"), 2, 2, alignment=Qt.AlignLeft)

        # HTML Error Template + browse button
        err.addWidget(QLabel("HTML Error Template:"), 3, 0)
        ed_tpl = QLineEdit("error.htm")
        err.addWidget(ed_tpl, 3, 1)
        btn_tpl = QPushButton("...")
        btn_tpl.setFixedWidth(28)
        err.addWidget(btn_tpl, 3, 2, alignment=Qt.AlignLeft)

        # Layout wie Screenshot
        g.addWidget(gb_out,   0, 0)
        g.addWidget(gb_dev,   0, 1)
        g.addWidget(gb_other, 1, 1)
        g.addWidget(gb_err,   2, 0, 1, 2)

        g.setRowStretch(3, 1)
        return tab

    def _help(self):
        QMessageBox.information(self, "Help", "Hier könnte deine Hilfe stehen :)")

    # Damit Esc auch sauber schließt
    def reject(self):
        super().reject()
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.mdi = QMdiArea(self)
        self.setCentralWidget(self.mdi)

        # Beispiel-Menü "Fenster"
        # Menü: Eigenschaften -> Arbeitsplatz
        f1 = QFont("Verdana", 11); f1.setBold(True)
        f2 = QFont("Verdana", 10); f2.setBold(False)
        
        menubar = self.menuBar()
        menubar.setFont(f1)
        menubar.font().setBold(True)
        
        menu_file       = menubar.addMenu("Datei")
        menu_file.setFont(f2)
        
        menu_edit       = menubar.addMenu("Editieren")
        menu_display    = menubar.addMenu("Anzeige")
        menu_properties = menubar.addMenu("Eigenschaften")
        menu_windows    = menubar.addMenu("Fenster")
        menu_help       = menubar.addMenu("Hilfe")
        
        menu_file_new               = menu_file.addMenu("Neu")
        menu_file_new.setFont(f2)
        
        action_file_open            = QAction("Öffnen", self)
        action_file_close           = QAction("Schließen", self)
        
        action_file_open .setShortcut(QKeySequence("Ctrl+O"))
        action_file_close.setShortcut(QKeySequence("Ctrl+F4"))
        
        action_file_open .triggered.connect(self.on_action_file_open)
        action_file_close.triggered.connect(self.on_action_file_close)
        
        action_file_new_project     = QAction("Neues Projekt", self)
        action_file_open_project    = QAction("Projekt öffnen", self)
        action_file_print           = QAction("Drucken", self)

        action_file_print.setShortcut(QKeySequence("Ctrl+P"))
        
        action_file_new_project .triggered.connect(self.on_action_file_new_project)
        action_file_open_project.triggered.connect(self.on_action_file_open_project)
        
        action_file_print_preview   = QAction("Durckvorschau", self)
        action_file_window_app      = QAction("Ein-klick Anwendung", self)
        action_file_web_wizard      = QAction("Web Wizard", self)
        action_file_database        = QAction("Datenbank-Verwaltung", self)
        action_file_exit            = QAction("Beenden", self)
        
        action_file_print        .triggered.connect(self.on_action_file_print)
        action_file_print_preview.triggered.connect(self.on_action_file_print_preview)
        action_file_window_app   .triggered.connect(self.on_action_file_window_app)
        action_file_web_wizard   .triggered.connect(self.on_action_file_web_wizard)
        action_file_database     .triggered.connect(self.on_action_file_database)
        action_file_exit         .triggered.connect(self.on_action_file_exit)
        
        action_file_new_form        = QAction("Formular", self)
        action_file_new_menu        = QAction("Menu", self)
        action_file_new_popupmenu   = QAction("Popup-Menu", self)
        action_file_new_report      = QAction("Bericht", self)
        action_file_new_labels      = QAction("Ettiketten", self)
        action_file_new_program     = QAction("Programm", self)
        action_file_new_table       = QAction("Tabelle", self)
        action_file_new_sql         = QAction("SQL", self)
        
        menu_file_new.addAction(action_file_new_form)
        menu_file_new.addAction(action_file_new_menu)
        menu_file_new.addAction(action_file_new_popupmenu)
        menu_file_new.addSeparator()
        menu_file_new.addAction(action_file_new_report)
        menu_file_new.addAction(action_file_new_labels)
        menu_file_new.addSeparator()
        menu_file_new.addAction(action_file_new_program)
        menu_file_new.addSeparator()
        menu_file_new.addAction(action_file_new_table)
        menu_file_new.addAction(action_file_new_sql)
        
        menu_file.addAction(action_file_open)
        menu_file.addAction(action_file_close)
        menu_file.addSeparator()
        menu_file.addAction(action_file_new_project)
        menu_file.addAction(action_file_open_project)
        menu_file.addSeparator()
        menu_file.addAction(action_file_print)
        menu_file.addAction(action_file_print_preview)
        menu_file.addSeparator()
        menu_file.addAction(action_file_window_app)
        menu_file.addAction(action_file_web_wizard)
        menu_file.addSeparator()
        menu_file.addAction(action_file_database)
        menu_file.addAction(action_file_exit)
        
        action_workplace = QAction("Arbeitsplatz", self)
        action_workplace.triggered.connect(self.open_workplace_properties)
        
        menu_properties.addAction(action_workplace)
        
        action_cascade = QAction("Kaskadieren",   self, triggered = self.mdi.cascadeSubWindows)
        action_tile    = QAction("Nebeneinander", self, triggered = self.mdi.tileSubWindows)
        
        menu_windows.addAction(action_cascade)
        menu_windows.addAction(action_tile)

        self._dlg_workplace = None  # Dialog-Instanz merken (nicht jedes Mal neu)
        
        self._create_toolbar()
        self._create_statusbar()
        
        dlg = DirectoryIconDialog()
        sub = self.mdi.addSubWindow(dlg)
        sub.show()
        
        self.mdi_open_editor()
        self.mdi_open_table_designer()

    def on_action_file_close(self):
        print("file close")
    def on_action_file_database(self):
        print("file data base")
    def on_action_file_exit(self):
        print("file exit")
        self.close()
    def on_action_file_new_project(self):
        print("file new project")
    def on_action_file_open(self):
        print("file open")
    def on_action_file_open_project(self):
        print("file open project")
    def on_action_file_print(self):
        print("file print")
    def on_action_file_print_preview(self):
        print("file print preview")
    def on_action_file_web_wizard(self):
        print("file web wizard")
    def on_action_file_window_app(self):
        print("file window app")
        
    def on_new(self):
        self.status_left.setText("Neu angelegt")

    def on_open(self):
        self.status_left.setText("Öffnen...")

    def on_save(self):
        self.status_left.setText("Gespeichert")
        
    def _create_toolbar(self):
        toolbar = QToolBar("Haupt-Toolbar", self)
        toolbar.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        act_new  = QAction(QIcon(":/icons/new.png" ), "Neu"      , self)
        act_open = QAction(QIcon(":/icons/open.png"), "Öffnen"   , self)
        act_save = QAction(QIcon(":/icons/save.png"), "Speichern", self)

        act_new .triggered.connect(self.on_new)
        act_open.triggered.connect(self.on_open)
        act_save.triggered.connect(self.on_save)

        toolbar.addAction(act_new)
        toolbar.addAction(act_open)
        toolbar.addAction(act_save)

        toolbar.addSeparator()
        
    def _create_statusbar(self):
        status = QStatusBar(self)
        self.setStatusBar(status)

        # Panel 1 – linker Bereich (dehnbar)
        self.status_left = QLabel("Bereit")
        self.status_left.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Panel 2 – Mitte
        self.status_mid = QLabel("MDI: 0 Fenster")
        self.status_mid.setAlignment(Qt.AlignCenter)

        # Panel 3 – rechts
        self.status_right = QLabel("Ln 1, Col 1")
        self.status_right.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        status.addWidget(self.status_left, 1)        # Stretch
        status.addPermanentWidget(self.status_mid, 0)
        status.addPermanentWidget(self.status_right, 0)
        
    def mdi_open_editor(self, title="Unbenannt", text=""):
        w = EditorWidget(text)
        sub = self.mdi.addSubWindow(w)     # Qt erzeugt ein QMdiSubWindow
        sub.setWindowTitle(title)
        sub.resize(900, 650)
        w.show()
        sub.show()
        
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy  (Qt.ScrollBarAsNeeded)
        
        self.mdi.setActiveSubWindow(sub)
        return sub

    def mdi_open_table_designer(self):
        dlg = TableDesignerDialog()
        sub = self.mdi.addSubWindow(dlg)
        sub.show()
    
    def open_workplace_properties(self):
        if self._dlg_workplace is None:
            self._dlg_workplace = DesktopPropertiesDialog(self)
            sub = MAINAPP.mdi.addSubWindow(self._dlg_workplace)
            # Wenn Benutzer das Fenster schließt, Instanz wieder freigeben
            self._dlg_workplace.mdi = sub
            self._dlg_workplace.finished.connect(lambda _=0: setattr(self, "_dlg_workplace", None))

        self._dlg_workplace.show()
        self._dlg_workplace.raise_()
        self._dlg_workplace.activateWindow()
        
def main():
    app = ensure_qt_app()
    if app is not None:
        global MAINAPP
        MAINAPP = MainWindow()
        MAINAPP.setStyleSheet(APP_DARK_QSS)
        MAINAPP.show()
        sys.exit(app.exec_())
    else:
        print("Qt5 kann nicht gestartet werden.")
        sys.exit(1)

if __name__ == "__main__":
    main()
