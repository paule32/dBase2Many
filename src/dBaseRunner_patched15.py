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
from html.parser import HTMLParser

from gen.dBaseLexer         import dBaseLexer
from gen.dBaseParser        import dBaseParser
from gen.dBaseParserVisitor import dBaseParserVisitor

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
    QRectF, QPointF, qRegisterResourceData, qUnregisterResourceData, qVersion,
    QSortFilterProxyModel, QByteArray, QUrl, QTimer
)
from PyQt5.QtGui     import (
    QFont, QPainter, QFontMetrics, QSyntaxHighlighter, QTextCharFormat, QColor,
    QStandardItemModel, QStandardItem, QIcon, QPixmap, QFontInfo, QPalette,
    QFontDatabase, QRegularExpressionValidator, QIntValidator, QPainterPath,
    QLinearGradient, QRadialGradient, QPen, QKeySequence, QTextFormat,
    QGuiApplication
)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QFrame, QPushButton, QVBoxLayout,
    QTextEdit, QToolBar, QStatusBar, QMessageBox, QPlainTextEdit, QAction,
    QFileDialog, QMenuBar, QMdiArea, QMdiSubWindow, QTreeView, QSplitter, QTabBar,
    QHBoxLayout, QComboBox, QTabWidget, QListWidget, QListWidgetItem, QScrollBar,
    QMenu, QFileDialog, QFileIconProvider, QListWidget, QTableWidget, QProgressBar,
    QTableWidgetItem, QHeaderView, QStyledItemDelegate, QGroupBox, QLabel,
    QLineEdit, QCheckBox, QRadioButton, QSpacerItem, QGridLayout, QSpinBox,
    QSizePolicy, QStyleOptionHeader, QStyle, QTableView, QAbstractItemView,
    QStyleOptionComplex, QProxyStyle, QToolButton
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineScript
)
from PyQt5.QtSvg import QSvgRenderer

# ---------------------------------------------------------------------------
# resources suff like icons, ...
# ---------------------------------------------------------------------------
import resources_rc

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
    "CONTAINER": QFrame,
    "ENTRYFIELD": QLineEdit,
    "RADIOBUTTON": QRadioButton,
    "COMBOBOX": QComboBox,
    "EDITOR": QPlainTextEdit,
    "CHECKBOX": QCheckBox,
    "LISTBOX": QListWidget,
    "CHECKLISTBOX": QListWidget,
    "IMAGE": QLabel,
    "GRID": QTableWidget,
    "PROGRESS": QProgressBar,
    "PAINTBOX": QWidget,
    "VSCROLLBAR": QScrollBar,
    "HSCROLLBAR": QScrollBar,
    "TEXT": QLabel,
    "TREEVIEW": QTreeView,
    "SPINBOX": QSpinBox,
    "BROWSE": QTableView,
}

SVG_BOOK = r"""
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">
  <rect x="2" y="2" width="11" height="12" rx="2" fill="#3b82f6"/>
  <rect x="4" y="3" width="1.5" height="10" fill="#1e3a8a" opacity="0.7"/>
  <rect x="6" y="4" width="6" height="1" fill="#ffffff" opacity="0.92"/>
  <rect x="6" y="6" width="6" height="1" fill="#ffffff" opacity="0.92"/>
  <rect x="6" y="8" width="5" height="1" fill="#ffffff" opacity="0.92"/>
</svg>
"""

SVG_PAGE = r"""
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">
  <path d="M4 2h6l2 2v10H4z" fill="#e5e7eb"/>
  <path d="M10 2v2h2" fill="#cbd5e1"/>
  <rect x="5" y="6" width="7" height="1" fill="#64748b"/>
  <rect x="5" y="8" width="6" height="1" fill="#64748b"/>
  <rect x="5" y="10" width="5" height="1" fill="#64748b"/>
</svg>
"""

def icon_from_svg(svg: str, size: int = 16) -> QIcon:
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    renderer.render(p)
    p.end()
    return QIcon(pix)

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

class FontTriangleArrowsStyle(QProxyStyle):
    def __init__(self, base_style=None, color="#d7b300", font_family=None):
        super().__init__(base_style)
        self.col = QColor(color)
        self.font_family = "Arial" #font_family  # z.B. "Segoe UI Symbol" (Windows), sonst None

    def _draw_triangle(self, painter: QPainter, rect, direction: Qt.ArrowType):
        glyph = {
            Qt.UpArrow: "▲",
            Qt.DownArrow: "▼",
            Qt.LeftArrow: "◀",
            Qt.RightArrow: "▶",
        }[direction]

        painter.save()
        painter.setRenderHint(QPainter.TextAntialiasing, True)
        painter.setPen(self.col)

        size = max(8, min(rect.width(), rect.height()) - 2)
        f = QFont()
        if self.font_family:
            f.setFamily(self.font_family)
        f.setPixelSize(size)
        f.setBold(True)
        painter.setFont(f)

        painter.drawText(rect, Qt.AlignCenter, glyph)
        painter.restore()

    def drawComplexControl(self, cc, option, painter, widget=None):
        # erst normal zeichnen (Track, Handle, Rahmen etc.)
        super().drawComplexControl(cc, option, painter, widget)

        # danach unsere Pfeile "drüber" malen
        if cc == QStyle.CC_ScrollBar:
            # sub-line (oben/links) und add-line (unten/rechts)
            sub_rect = self.subControlRect(cc, option, QStyle.SC_ScrollBarSubLine, widget)
            add_rect = self.subControlRect(cc, option, QStyle.SC_ScrollBarAddLine, widget)

            if option.orientation == Qt.Vertical:
                if sub_rect.isValid() and not sub_rect.isEmpty():
                    self._draw_triangle(painter, sub_rect, Qt.UpArrow)
                if add_rect.isValid() and not add_rect.isEmpty():
                    self._draw_triangle(painter, add_rect, Qt.DownArrow)
            else:
                if sub_rect.isValid() and not sub_rect.isEmpty():
                    self._draw_triangle(painter, sub_rect, Qt.LeftArrow)
                if add_rect.isValid() and not add_rect.isEmpty():
                    self._draw_triangle(painter, add_rect, Qt.RightArrow)

        elif cc == QStyle.CC_ComboBox:
            arrow_rect = self.subControlRect(cc, option, QStyle.SC_ComboBoxArrow, widget)
            if arrow_rect.isValid() and not arrow_rect.isEmpty():
                self._draw_triangle(painter, arrow_rect, Qt.DownArrow)
        
class HtmlHelpParser(HTMLParser):
    """
    Parser für htmlhelp .hhc (Contents) und .hhk (Index).
    Beide nutzen:
      <OBJECT type="text/sitemap">
         <param name="Name" value="...">
         <param name="Local" value="...">
      </OBJECT>
      <UL> ... </UL> (optional)
    """
    def __init__(self):
        super().__init__()
        self.root = TocNode("ROOT")
        self._stack: List[TocNode] = [self.root]

        self._in_object = False
        self._cur_name: Optional[str] = None
        self._cur_local: Optional[str] = None

        self._last_created: Optional[TocNode] = None
        self._pending_push_on_ul = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = {k.lower(): v for k, v in attrs}

        if tag == "object":
            t = (attrs.get("type") or "").lower()
            if "text/sitemap" in t:
                self._in_object = True
                self._cur_name = None
                self._cur_local = None

        elif tag == "param" and self._in_object:
            name = (attrs.get("name") or "").lower()
            value = (attrs.get("value") or "").strip()
            if name == "name":
                self._cur_name = value
            elif name == "local":
                self._cur_local = value

        elif tag == "ul":
            if self._pending_push_on_ul and self._last_created is not None:
                self._stack.append(self._last_created)
                self._pending_push_on_ul = False

    def handle_endtag(self, tag):
        tag = tag.lower()

        if tag == "object" and self._in_object:
            self._in_object = False
            title = (self._cur_name or "Untitled").strip()
            local = (self._cur_local or "").strip() or None

            node = TocNode(title=title, local=local)
            self._stack[-1].children.append(node)

            self._last_created = node
            self._pending_push_on_ul = True

        elif tag == "ul":
            if len(self._stack) > 1:
                self._stack.pop()

    def unknown_decl(self, data):
        pass


def _read_text_fallback(path: str) -> str:
    for enc in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            with open(path, "r", encoding=enc, errors="strict") as f:
                return f.read()
        except Exception:
            pass
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_hh_file(path: str) -> TocNode:
    raw = _read_text_fallback(path)
    p = HtmlHelpParser()
    p.feed(raw)
    return p.root


class RecursiveFilterProxy(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self._text = ""
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        if hasattr(self, "setRecursiveFilteringEnabled"):
            self.setRecursiveFilteringEnabled(True)

    def setFilterText(self, text: str):
        self._text = (text or "").strip()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if not self._text:
            return True

        model = self.sourceModel()
        idx = model.index(source_row, 0, source_parent)
        if not idx.isValid():
            return False

        title = model.data(idx, Qt.DisplayRole) or ""
        if self._text.lower() in title.lower():
            return True

        for r in range(model.rowCount(idx)):
            if self.filterAcceptsRow(r, idx):
                return True
        return False


def decompile_chm_windows(chm_path: str, out_dir: str) -> bool:
    """
    Windows-only: uses hh.exe -decompile OUTDIR file.chm
    """
    hh = shutil.which("hh.exe") or shutil.which("hh")
    if not hh:
        return False
    try:
        subprocess.run(
            [hh, "-decompile", out_dir, chm_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except Exception:
        return False

class F1Filter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F1:
            print("F1 global abgefangen")
            return True  # Event stoppt hier
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_F2:
            pass
            #if EDIT_OBJECT
        return False

class HelpTitleBar(QWidget):
    def __init__(self, window: QMainWindow):
        super().__init__(window)
        self.window = window
        self.setObjectName("TitleBar")

        self._drag_pos: Optional[QPoint] = None
        self._dragging = False
        self._was_maximized = False
        self._press_offset_ratio = 0.5  # Position innerhalb der Titlebar beim Restore aus Maximized

        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 6, 10, 6)
        lay.setSpacing(8)

        self.title_label = QLabel(window.windowTitle())
        self.title_label.setObjectName("TitleLabel")
        lay.addWidget(self.title_label, 1)

        self.btn_min = QPushButton("–")
        self.btn_min.setObjectName("TitleBtnMin")
        self.btn_min.setFixedSize(36, 28)
        self.btn_min.clicked.connect(self.window.showMinimized)

        self.btn_max = QPushButton("▢")
        self.btn_max.setObjectName("TitleBtnMax")
        self.btn_max.setFixedSize(36, 28)
        self.btn_max.clicked.connect(self.toggle_max_restore)

        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("TitleBtnClose")
        self.btn_close.setFixedSize(36, 28)
        self.btn_close.clicked.connect(self.window.close)

        lay.addWidget(self.btn_min)
        lay.addWidget(self.btn_max)
        lay.addWidget(self.btn_close)

        self.window.windowTitleChanged.connect(self.title_label.setText)

    def toggle_max_restore(self):
        if self.window.isMaximized():
            self.window.showNormal()
        else:
            self.window.showMaximized()

    def _is_on_buttons(self, pos) -> bool:
        child = self.childAt(pos)
        return child in (self.btn_min, self.btn_max, self.btn_close)

    def _snap_geometry(self, gp: QPoint):
        """
        Returns QRect or None. gp = global mouse pos on release.
        """
        screen = QGuiApplication.screenAt(gp)
        if not screen:
            return None

        area = screen.availableGeometry()  # ohne Taskbar
        margin = 10  # "Snap-Zone" in px

        x, y = gp.x(), gp.y()

        left = x <= area.left() + margin
        right = x >= area.right() - margin
        top = y <= area.top() + margin

        # Optional: Viertel bei Ecken
        if top and left:
            return QRect(area.left(), area.top(), area.width() // 2, area.height() // 2)
        if top and right:
            return QRect(area.left() + area.width() // 2, area.top(), area.width() // 2, area.height() // 2)

        # Halber Screen links/rechts
        if left:
            return QRect(area.left(), area.top(), area.width() // 2, area.height())
        if right:
            return QRect(area.left() + area.width() // 2, area.top(), area.width() // 2, area.height())

        # Maximieren oben
        if top:
            return area

        return None
    
    def show_help(self):
        print("hhh")
        hlp = HelpMainWindow()
        hlp.open_from_args("dBaseHelp_de.chm","index.html")
        hlp.show()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self._is_on_buttons(event.pos()):
            self._dragging = True
            self._was_maximized = self.window.isMaximized()

            # Merken, wo innerhalb der Titlebar geklickt wurde (für Restore aus Maximized)
            if self.width() > 0:
                self._press_offset_ratio = max(0.05, min(0.95, event.pos().x() / self.width()))

            self._drag_pos = event.globalPos() - self.window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._dragging and self._drag_pos is not None:
            # Wenn maximiert und man zieht, erst restore (wie Windows)
            if self._was_maximized and self.window.isMaximized():
                self.window.showNormal()

                # Fenster so positionieren, dass die Maus "am selben relativen Punkt" bleibt
                gp = event.globalPos()
                w = self.window.width()
                new_x = gp.x() - int(w * self._press_offset_ratio)
                new_y = gp.y() - 12  # kleiner Offset nach oben
                self.window.move(new_x, new_y)

                self._drag_pos = gp - self.window.frameGeometry().topLeft()

            # Normales Dragging
            if not self.window.isMaximized():
                self.window.move(event.globalPos() - self._drag_pos)

            event.accept()

    def mouseReleaseEvent(self, event):
        if self._dragging and event.button() == Qt.LeftButton:
            self._dragging = False

            snap = self._snap_geometry(event.globalPos())
            if snap is not None:
                # area == maximize
                screen = QGuiApplication.screenAt(event.globalPos())
                area = screen.availableGeometry() if screen else None
                if area is not None and snap == area:
                    self.window.showMaximized()
                else:
                    self.window.showNormal()
                    self.window.setGeometry(snap)

            self._drag_pos = None
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton and not self._is_on_buttons(event.pos()):
            self.toggle_max_restore()
            event.accept()

class HelpMainWindow(QMainWindow):
    ROLE_LOCAL = Qt.UserRole + 1
    ROLE_BREAD = Qt.UserRole + 2

    def __init__(self):
        super().__init__()
        
        self._pending_page: Optional[str] = None
        
        self._resize_margin = 8  # Pixel "Griffbreite" am Rand
        self._resizing      = False
        self._resize_edge   = None
        self._drag_pos      = None
        self._start_geom    = None
        
        self.setWindowTitle("CHM-Viewer - (c) 2026 Dimitri Haesch & Co.")
        self.resize(800, 600)
        
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        
        self.titlebar = HelpTitleBar(self)
        
        top = QWidget()
        top.setObjectName("TopContainer")
        top_lay = QVBoxLayout(top)
        top_lay.setContentsMargins(0, 0, 0, 0)
        top_lay.setSpacing(0)
        top_lay.addWidget(self.titlebar)

        # Optional: dünne Trennlinie unter der Titelleiste
        sep = QWidget()
        sep.setObjectName("TitleSeparator")
        sep.setFixedHeight(1)
        top_lay.addWidget(sep)

        self.setMenuWidget(top)
        
        
        self.base_dir: Optional[str] = None
        self.dark_mode = False

        # Icons
        try:
            self.icon_book = icon_from_svg(SVG_BOOK, 16)
            self.icon_page = icon_from_svg(SVG_PAGE, 16)
        except Exception:
            self.icon_book = self.style().standardIcon(QStyle.SP_DirIcon)
            self.icon_page = self.style().standardIcon(QStyle.SP_FileIcon)

        # Web
        self.web = QWebEngineView()
        self.web.urlChanged.connect(self._on_url_changed)

        # Tabs left
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.tabBar().setUsesScrollButtons(True)

        # Contents model/view
        self.contents_model = QStandardItemModel()
        self.contents_model.setHorizontalHeaderLabels(["Contents"])
        self.contents_proxy = RecursiveFilterProxy()
        self.contents_proxy.setSourceModel(self.contents_model)

        self.contents_filter = QLineEdit()
        self.contents_filter.setPlaceholderText("Filter (Contents)…")
        self.contents_filter.textChanged.connect(self.contents_proxy.setFilterText)

        self.contents_tree = QTreeView()
        self.contents_tree.setModel(self.contents_proxy)
        self.contents_tree.setUniformRowHeights(True)
        self.contents_tree.clicked.connect(self.on_contents_clicked)

        tab_contents = QWidget()
        vc = QVBoxLayout(tab_contents)
        vc.setContentsMargins(8, 8, 8, 8)
        vc.setSpacing(8)
        vc.addWidget(self.contents_filter)
        vc.addWidget(self.contents_tree)
        self.tabs.addTab(tab_contents, "Contents")

        # Index model/view
        self.index_model = QStandardItemModel()
        self.index_model.setHorizontalHeaderLabels(["Index"])
        self.index_proxy = RecursiveFilterProxy()
        self.index_proxy.setSourceModel(self.index_model)

        self.index_filter = QLineEdit()
        self.index_filter.setPlaceholderText("Filter (Index)…")
        self.index_filter.textChanged.connect(self.index_proxy.setFilterText)

        self.index_view = QTreeView()
        self.index_view.setModel(self.index_proxy)
        self.index_view.setUniformRowHeights(True)
        self.index_view.clicked.connect(self.on_index_clicked)

        tab_index = QWidget()
        vi = QVBoxLayout(tab_index)
        vi.setContentsMargins(8, 8, 8, 8)
        vi.setSpacing(8)
        vi.addWidget(self.index_filter)
        vi.addWidget(self.index_view)
        self.tabs.addTab(tab_index, "Index")

        # Search tab (Sphinx search.html)
        tab_search = QWidget()
        vs = QVBoxLayout(tab_search)
        vs.setContentsMargins(8, 8, 8, 8)
        vs.setSpacing(8)

        row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search (Sphinx)…")
        self.search_edit.returnPressed.connect(self.open_sphinx_search)
        btn = QPushButton("Search")
        btn.clicked.connect(self.open_sphinx_search)
        row.addWidget(self.search_edit, 1)
        row.addWidget(btn, 0)

        hint = QLabel("Sucht in Sphinx über search.html – Ergebnisse erscheinen rechts.")
        hint.setWordWrap(True)
        hint.setStyleSheet("opacity: 0.8;")

        vs.addLayout(row)
        vs.addWidget(hint)
        vs.addStretch(1)
        self.tabs.addTab(tab_search, "Search")

        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.web)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([380, 820])

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self.status.showMessage("Ready", 2000)
        
        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(splitter)
        self.setCentralWidget(central)

        self._make_toolbar()
        self._apply_theme()

    # -------- Toolbar --------
    def _make_toolbar(self):
        tb = QToolBar("Main")
        tb.setMovable(False)
        self.addToolBar(tb)

        act_open = QAction(self.style().standardIcon(QStyle.SP_DialogOpenButton), "Open…", self)
        act_open.triggered.connect(self.open_chm_single_dialog)
        tb.addAction(act_open)

        tb.addSeparator()

        act_home = QAction(self.style().standardIcon(QStyle.SP_ArrowUp), "Home", self)
        act_home.triggered.connect(self.go_home)
        tb.addAction(act_home)

        act_back = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "Back", self)
        act_back.triggered.connect(self.web.back)
        tb.addAction(act_back)

        act_fwd = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "Forward", self)
        act_fwd.triggered.connect(self.web.forward)
        tb.addAction(act_fwd)

        act_reload = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "Reload", self)
        act_reload.triggered.connect(self.web.reload)
        tb.addAction(act_reload)

        tb.addSeparator()

        self.breadcrumb = QLabel("—")
        self.breadcrumb.setTextInteractionFlags(Qt.TextSelectableByMouse)
        tb.addWidget(self.breadcrumb)

        tb.addSeparator()

        self.act_theme = QAction("🌙 Dark", self)
        self.act_theme.triggered.connect(self.toggle_theme)
        tb.addAction(self.act_theme)

    # -------- Open (single dialog) --------
    def open_chm_single_dialog(self):
        chm_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open CHM",
            "",
            "CHM Help (*.chm);;All Files (*)"
        )
        if not chm_path:
            return

        self.load_from_chm_path(chm_path)

    # -------- Load from CHM path --------
    def load_from_chm_path(self, chm_path: str):
        """
        1) Try: side-by-side .hhc/.hhk in same folder as CHM
        2) Else: Windows hh.exe -decompile to temp -> load .hhc/.hhk from there
        """
        folder = os.path.dirname(chm_path)
        stem = os.path.splitext(os.path.basename(chm_path))[0]

        hhc = os.path.join(folder, f"{stem}.hhc")
        hhk = os.path.join(folder, f"{stem}.hhk")

        if os.path.exists(hhc):
            self.base_dir = folder
            self.load_contents(hhc)
            if os.path.exists(hhk):
                self.load_index(hhk)
            else:
                self.index_model.removeRows(0, self.index_model.rowCount())
            self.open_start_page()
            return

        # fallback: decompile CHM
        tmp = tempfile.mkdtemp(prefix="chm_decompile_")
        ok = decompile_chm_windows(chm_path, tmp)
        if not ok:
            QMessageBox.warning(
                self,
                "TOC nicht verfügbar",
                "Keine passende .hhc neben der CHM gefunden und CHM konnte nicht dekompiliert werden.\n\n"
                "Windows: stelle sicher, dass 'hh.exe' verfügbar ist.\n"
                "Alternative: CHM manuell dekompilieren und dann die entpackten Dateien anzeigen."
            )
            return

        # pick first .hhc/.hhk in temp
        hhc_found = self._find_first(tmp, (".hhc",))
        hhk_found = self._find_first(tmp, (".hhk",))

        if not hhc_found:
            QMessageBox.warning(self, "Keine .hhc gefunden", "Nach Dekomplilierung wurde keine .hhc gefunden.")
            return

        self.base_dir = tmp
        self.load_contents(hhc_found)
        if hhk_found:
            self.load_index(hhk_found)
        else:
            self.index_model.removeRows(0, self.index_model.rowCount())

        self.open_start_page()
        
    def open_from_args(self, chm_path: Optional[str], page: Optional[str]):
        """
        Wird einmal beim Start aufgerufen.
        - chm_path: Pfad zur .chm
        - page: relative Seite, z.B. "index.html" oder "api/mod.html#func"
        """
        if page:
            self._pending_page = page

        if chm_path:
            self.load_from_chm_path(chm_path)

            # nach dem Laden ggf. die Seite öffnen
            if self._pending_page:
                self.open_local(self._pending_page)
                self._pending_page = None
                
    def open_start_page(self):
        if not self.base_dir:
            return
        index_html = os.path.join(self.base_dir, "index.html")
        if os.path.exists(index_html):
            self.web.setUrl(QUrl.fromLocalFile(index_html))
        else:
            first = self._first_local_item(self.contents_model)
            if first:
                self.open_local(first)

    # -------- Contents / Index load --------

    def load_contents(self, hhc_path: str):
        self.contents_model.removeRows(0, self.contents_model.rowCount())
        toc_root = parse_hh_file(hhc_path)
        for child in toc_root.children:
            self.contents_model.appendRow(self._node_to_item(child, parent_path=[]))
        self.contents_tree.expandToDepth(1)

    def load_index(self, hhk_path: str):
        self.index_model.removeRows(0, self.index_model.rowCount())
        idx_root = parse_hh_file(hhk_path)

        # flatten index entries
        items: List[Tuple[str, str]] = []

        def walk(n: TocNode):
            if n.local:
                items.append((n.title.strip(), n.local.strip()))
            for c in n.children:
                walk(c)

        for c in idx_root.children:
            walk(c)

        # Dedup:
        # 1) bevorzugt nach Local (Ziel) deduplizieren
        # 2) falls Local leer/komisch wäre: nach (title, local)
        seen_local = set()
        seen_pair = set()
        deduped: List[Tuple[str, str]] = []

        for title, local in items:
            key_local = (local or "").lower()
            key_pair = (title.lower(), key_local)

            if key_local:
                if key_local in seen_local:
                    continue
                seen_local.add(key_local)
            else:
                if key_pair in seen_pair:
                    continue
                seen_pair.add(key_pair)

            deduped.append((title, local))

        # sort by title
        deduped.sort(key=lambda x: x[0].lower())

        for title, local in deduped:
            it = QStandardItem(title)
            it.setEditable(False)
            it.setIcon(self.icon_page)
            it.setData(local, self.ROLE_LOCAL)
            it.setData(title, self.ROLE_BREAD)
            self.index_model.appendRow(it)


    def _node_to_item(self, node: TocNode, parent_path: List[str]) -> QStandardItem:
        item = QStandardItem(node.title)
        item.setEditable(False)
        item.setIcon(self.icon_book if node.children else self.icon_page)

        bread = " › ".join(parent_path + [node.title])
        item.setData(node.local or "", self.ROLE_LOCAL)
        item.setData(bread, self.ROLE_BREAD)

        for c in node.children:
            item.appendRow(self._node_to_item(c, parent_path + [node.title]))
        return item

    def _find_first(self, folder: str, exts: Tuple[str, ...]) -> Optional[str]:
        for fn in os.listdir(folder):
            if fn.lower().endswith(exts):
                return os.path.join(folder, fn)
        return None

    def _first_local_item(self, model: QStandardItemModel) -> Optional[str]:
        def walk(it: QStandardItem) -> Optional[str]:
            loc = it.data(self.ROLE_LOCAL)
            if loc:
                return loc
            for r in range(it.rowCount()):
                v = walk(it.child(r))
                if v:
                    return v
            return None

        for r in range(model.rowCount()):
            v = walk(model.item(r))
            if v:
                return v
        return None

    # -------- Click handlers --------
    def on_contents_clicked(self, proxy_idx: QModelIndex):
        src_idx = self.contents_proxy.mapToSource(proxy_idx)
        item = self.contents_model.itemFromIndex(src_idx)
        if item:
            self._open_item(item)

    def on_index_clicked(self, proxy_idx: QModelIndex):
        src_idx = self.index_proxy.mapToSource(proxy_idx)
        item = self.index_model.itemFromIndex(src_idx)
        if item:
            self._open_item(item)

    def _open_item(self, item: QStandardItem):
        local = (item.data(self.ROLE_LOCAL) or "").strip()
        bread = (item.data(self.ROLE_BREAD) or "—").strip()
        self.breadcrumb.setText(bread)
        if local:
            self.open_local(local)

    def _hit_test_edge(self, pos):
        """
        Ermittelt, ob Maus in Resize-Zone ist.
        Rückgabe: string aus {L,R,T,B,LT,RT,LB,RB} oder None
        """
        m = self._resize_margin
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        left = x <= m
        right = x >= w - m
        top = y <= m
        bottom = y >= h - m

        if top and left:
            return "LT"
        if top and right:
            return "RT"
        if bottom and left:
            return "LB"
        if bottom and right:
            return "RB"
        if left:
            return "L"
        if right:
            return "R"
        if top:
            return "T"
        if bottom:
            return "B"
        return None


    def _set_cursor_for_edge(self, edge):
        pass
        #"""if edge in ("L", "R"):
        #    self.setCursor(Qt.SizeHorCursor)
        #elif edge in ("T", "B"):
        #    self.setCursor(Qt.SizeVerCursor)
        #elif edge in ("LT", "RB"):
        #    self.setCursor(Qt.SizeFDiagCursor)
        #elif edge in ("RT", "LB"):
        #    self.setCursor(Qt.SizeBDiagCursor)
        #else:
        #    self.setCursor(Qt.ArrowCursor)"""


    def mouseMoveEvent(self, event):
        if self.isMaximized():
            self._set_cursor_for_edge(None)
            return super().mouseMoveEvent(event)

        if self._resizing and self._resize_edge and self._start_geom and self._drag_pos:
            delta = event.globalPos() - self._drag_pos
            g = QRect(self._start_geom)

            min_w, min_h = 400, 300  # Mindestgröße, anpassen wenn du willst

            if "L" in self._resize_edge:
                new_left = g.left() + delta.x()
                if g.right() - new_left + 1 >= min_w:
                    g.setLeft(new_left)
            if "R" in self._resize_edge:
                new_right = g.right() + delta.x()
                if new_right - g.left() + 1 >= min_w:
                    g.setRight(new_right)
            if "T" in self._resize_edge:
                new_top = g.top() + delta.y()
                if g.bottom() - new_top + 1 >= min_h:
                    g.setTop(new_top)
            if "B" in self._resize_edge:
                new_bottom = g.bottom() + delta.y()
                if new_bottom - g.top() + 1 >= min_h:
                    g.setBottom(new_bottom)

            self.setGeometry(g)
            return

        # nicht resizing: nur Cursor setzen
        edge = self._hit_test_edge(event.pos())
        self._set_cursor_for_edge(edge)
        super().mouseMoveEvent(event)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isMaximized():
            edge = self._hit_test_edge(event.pos())
            if edge:
                self._resizing = True
                self._resize_edge = edge
                self._drag_pos = event.globalPos()
                self._start_geom = self.geometry()
                event.accept()
                return
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_edge = None
        self._drag_pos = None
        self._start_geom = None
        super().mouseReleaseEvent(event)

    # -------- Robust open_local --------
    def open_local(self, local: str):
        if not self.base_dir:
            return

        local = unescape((local or "").strip())
        if not local:
            return

        # already URL?
        if re.match(r"^[a-zA-Z]+://", local):
            self.web.setUrl(QUrl(local))
            return

        # split fragment
        path_part, frag = (local.split("#", 1) + [""])[:2]
        path_part = path_part.replace("\\", "/").lstrip("/")

        abs_path = os.path.normpath(os.path.join(self.base_dir, path_part))

        # safety: stay inside base_dir
        base_norm = os.path.normpath(self.base_dir)
        if not os.path.normpath(abs_path).startswith(base_norm):
            QMessageBox.warning(self, "Ungültiger Pfad", f"Pfad außerhalb Basisordner:\n{abs_path}")
            return

        if not os.path.exists(abs_path):
            QMessageBox.warning(self, "Nicht gefunden", f"Datei nicht gefunden:\n{abs_path}")
            return

        url = QUrl.fromLocalFile(abs_path)
        if frag:
            url.setFragment(frag)
        self.web.setUrl(url)

    # -------- Search (Sphinx) --------
    def open_sphinx_search(self):
        if not self.base_dir:
            return
        q = (self.search_edit.text() or "").strip()
        if not q:
            return

        search_html = os.path.join(self.base_dir, "search.html")
        if not os.path.exists(search_html):
            QMessageBox.warning(self, "search.html fehlt", "Im htmlhelp-Ordner gibt es keine search.html.")
            return

        url = QUrl.fromLocalFile(search_html)
        q_enc = re.sub(r"\s+", "+", q)
        url.setQuery(f"q={q_enc}")
        self.web.setUrl(url)

    # -------- Navigation --------
    def go_home(self):
        if not self.base_dir:
            return
        home = os.path.join(self.base_dir, "index.html")
        if os.path.exists(home):
            self.web.setUrl(QUrl.fromLocalFile(home))

    # -------- Theme --------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.act_theme.setText("☀️ Light" if self.dark_mode else "🌙 Dark")
        self._apply_theme()
        self._inject_web_css()
    
    from PyQt5.QtWebEngineWidgets import QWebEngineScript  # oder PyQt6 entsprechend

    def _apply_webview_theme(self):
        """
        Injiziert CSS + toggelt .dark auf <html>.
        Call bei Theme-Wechsel UND idealerweise nach jeder Navigation.
        """
        view = self.web  # <- passe an deinen Namen an (QWebEngineView)
        css = self._webview_scrollbar_css()

        # Wichtig: CSS in JS sicher einbetten
        css_js = css.replace("\\", "\\\\").replace("`", "\\`")

        js = f"""
(function() {{
  const STYLE_ID = "win95-scrollbars-style";

  // dark togglen auf <html>
  const root = document.documentElement;
  root.classList.toggle("dark", {str(bool(self.dark_mode)).lower()});

  // Style-Tag erstellen/ersetzen
  let tag = document.getElementById(STYLE_ID);
  if (!tag) {{
    tag = document.createElement("style");
    tag.id = STYLE_ID;
    document.head.appendChild(tag);
  }}
  tag.textContent = `{css_js}`;
}})();"""

        # 1) sofort auf aktueller Seite anwenden
        view.page().runJavaScript(js)

        # 2) zusätzlich als QWebEngineScript setzen, damit es bei Navigation automatisch wirkt
        script = QWebEngineScript()
        script.setName("win95-scrollbars")
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setRunsOnSubFrames(True)  # auch iframes
        script.setSourceCode(js)

        # vorhandenes Script gleichen Namens entfernen (sonst stapelt es)
        scripts = view.page().scripts()
        for s in scripts.toList():
            if s.name() == "win95-scrollbars":
                scripts.remove(s)
                break
        scripts.insert(script)

    def _apply_theme(self):
        app = QApplication.instance()
        pal = QPalette()
        
        if self.dark_mode:
            pal.setColor(QPalette.Window, QColor(30, 30, 30))
            pal.setColor(QPalette.WindowText, Qt.white)
            pal.setColor(QPalette.Base, QColor(24, 24, 24))
            pal.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
            pal.setColor(QPalette.Text, Qt.white)
            pal.setColor(QPalette.Button, QColor(45, 45, 45))
            pal.setColor(QPalette.ButtonText, Qt.white)
            pal.setColor(QPalette.Highlight, QColor(80, 120, 200))
            pal.setColor(QPalette.HighlightedText, Qt.white)
        else:
            pal = app.style().standardPalette()
        
        app.setPalette(pal)
        
        if self.dark_mode:
            header_bg               = "#222222"
            header_fg               = "#ffd866"
            tree_bg                 = "#181818"
            tree_fg                 = "#ffffff"
            sel_bg                  = "#2b4c7e"
            sel_fg                  = "#ffffff"
            border                  = "#333333"
            
            tab_bg                  = "#1c1c1c"
            tab_bar_bg              = "#161616"
            tab_fg                  = "#eaeaea"
            tab_fg_active           = "#ffd866"
            tab_sel_bg              = "#242424"
            tab_hover_bg            = "#202020"
            
            toolbar_bg              = "#1a1a1a"
            toolbtn_bg              = "#222222"
            toolbtn_fg              = "#ffd866"
            toolbtn_hover           = "#2a2a2a"
            toolbtn_pressed         = "#303030"
            
            title_bg                = "#121212"  # Hintergrund Titelleiste
            title_fg                = "#ffd866"  # Text/Farbe Buttons (oder "#ffffff")
            title_btn_bg            = "#1f1f1f"  # Buttons normal
            title_btn_hover         = "#2a2a2a"  # Buttons hover
            title_btn_close_hover   = "#8a1f1f"  # Close hover
            
            status_bg               = "#121212"
            status_fg               = "#ffd866"  # oder "#ffffff"
            status_border           = "#333333"
            
            # Scrollbar dark-blue
            scroll_track            = "#141414"
            scroll_handle           = "#0b2a4a"
            scroll_handle_hover     = "#0f3a66"
        else:
            header_bg               = "#f0f0f0"
            header_fg               = "#000000"
            tree_bg                 = "#ffffff"
            tree_fg                 = "#000000"
            sel_bg                  = "#cfe3ff"
            sel_fg                  = "#000000"
            border                  = "#d0d0d0"
            
            tab_bg                  = "#f4f4f4"
            tab_bar_bg              = "#ededed"
            tab_fg                  = "#000000"
            tab_fg_active           = "#000000"
            tab_sel_bg              = "#ffffff"
            tab_hover_bg            = "#f9f9f9"
            
            toolbar_bg              = "#f2f2f2"
            toolbtn_bg              = "#e9e9e9"
            toolbtn_fg              = "#000000"
            toolbtn_hover           = "#dedede"
            toolbtn_pressed         = "#d2d2d2"
            
            title_bg                = "#eaeaea"
            title_fg                = "#000000"
            title_btn_bg            = "#f3f3f3"
            title_btn_hover         = "#dedede"
            title_btn_close_hover   = "#e06c75"
            
            status_bg               = "#ededed"
            status_fg               = "#000000"
            status_border           = "#d0d0d0"
            
            # Scrollbar light-gray
            scroll_track            = "#f2f2f2"
            scroll_handle           = "#c8c8c8"
            scroll_handle_hover     = "#b0b0b0"
        
        self.setStyleSheet(f"""
QToolBar {{spacing: 8px;background: {toolbar_bg};border: none;}}
QToolBar::separator {{background: {border};width: 1px;margin: 6px 8px;}}
QLineEdit {{padding: 6px 10px;border-radius: 10px;border: 1px solid {border};background: {tab_bg};color: {tab_fg};}}
QLabel {{color: {tab_fg};}}
QToolButton {{background: {toolbtn_bg};color: {toolbtn_fg};border: 1px solid {border};border-radius: 10px;padding: 6px 10px;}}
QToolButton:hover {{background: {toolbtn_hover};}}
QToolButton:pressed {{background: {toolbtn_pressed};}}
QTabWidget::pane {{border: 1px solid {border};top: -1px;background: {tab_bg};}}
QTabBar {{background: {tab_bar_bg};}}
QTabBar::tab {{background: {tab_bar_bg};color: {tab_fg};border: 1px solid {border};border-bottom: none;padding: 7px 14px;margin-right: 6px;border-top-left-radius: 12px;border-top-right-radius: 12px;min-width: 90px;}}
QTabBar::tab:hover {{background: {tab_hover_bg};}}
QTabBar::tab:selected {{background: {tab_sel_bg};color: {tab_fg_active};}}
QTreeView {{border: none;background: {tree_bg};color: {tree_fg};}}
QTreeView::item:selected {{background: {sel_bg};color: {sel_fg};}}
QHeaderView::section {{background: {header_bg};color: {header_fg};padding: 6px;border: none;border-bottom: 1px solid {border};}}
QPushButton {{background: {toolbtn_bg};color: {toolbtn_fg};border: 1px solid {border};border-radius: 10px;padding: 7px 12px;}}
QPushButton:hover {{background: {toolbtn_hover};}}
QPushButton:pressed {{background: {toolbtn_pressed};}}
/* Scrollbars (TreeView etc.) */
QScrollBar:vertical {{background: {scroll_track};width: 12px;margin: 0px;border: none;border-radius: 6px;}}
QScrollBar::handle:vertical {{background: {scroll_handle};min-height: 28px;border-radius: 6px;}}
QScrollBar::handle:vertical:hover {{background: {scroll_handle_hover};}}
QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {{height: 0px;}}
QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical {{background: transparent;}}
QScrollBar:horizontal {{background: {scroll_track};height: 12px;margin: 0px;border: none;border-radius: 6px;}}
QScrollBar::handle:horizontal {{background: {scroll_handle};min-width: 28px;border-radius: 6px;}}
QScrollBar::handle:horizontal:hover {{background: {scroll_handle_hover};}}
QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal {{width: 0px;}}
QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal {{background: transparent;}}
/* Custom Title Bar */
#TopContainer {{ background: transparent; }}
#TitleBar {{background: {title_bg};}}
#TitleLabel {{color: {title_fg};font-weight: 600;}}
#TitleSeparator {{background: {border};}}
QPushButton#TitleBtnMin,QPushButton#TitleBtnMax,QPushButton#TitleBtnClose {{background: {title_btn_bg};color: {title_fg};border: 1px solid {border};border-radius: 10px;}}
QPushButton#TitleBtnMin:hover,QPushButton#TitleBtnMax:hover {{background: {title_btn_hover};}}
QPushButton#TitleBtnClose:hover {{background: {title_btn_close_hover};}}
QStatusBar {{background: {status_bg};color: {status_fg};border-top: 1px solid {status_border};}}
QStatusBar QLabel {{color: {status_fg};}}
/* Tab scrollers (left/right arrows) */
QTabBar::scroller {{width: 22px;height: 22px;background: {tab_bar_bg};border: 1px solid {border};border-radius: 10px;margin: 2px;}}
QTabBar::scroller:hover {{background: {tab_hover_bg};}}
/* Arrow icons color via "color" + qproperty (works in many styles) */
QTabBar QToolButton {{background: {tab_bar_bg};border: 1px solid {border};border-radius: 10px;padding: 2px;color: {tab_fg_active};}}
QTabBar QToolButton:hover {{background: {tab_hover_bg};}}
QTabBar QToolButton:pressed {{background: {tab_sel_bg};}}
QSplitter {{background: {tree_bg};}}
QSplitter::handle {{background: {border};}}
QWebEngineView {{background: {tree_bg};}}""")

        if self.dark_mode:
            self.web.setStyleSheet("background: #000000;")
        else:
            self.web.setStyleSheet("background: white;")
            
        self._apply_webview_theme()

    def _webview_scrollbar_css(self) -> str:
        # Wir toggeln im HTML einfach "dark" auf <html> (document.documentElement)
        return r"""
/* === Win95 Scrollbars nur im rechten WebView-Dokument === */

/* Default (Light) */
:root {
  --sb-size: 16px;

  --sb-face:  #c0c0c0;
  --sb-track: #e6e6e6;
  --sb-thumb: #c0c0c0;
  --sb-hi:    #ffffff;
  --sb-mid:   #808080;
  --sb-dark:  #000000;
}

/* Dark Mode: Win95-Stil, aber navy (Balken) */
:root.dark {
  --sb-face:  #001f4d;   /* navy */
  --sb-track: #001a40;   /* etwas dunkler */
  --sb-thumb: #002b66;   /* thumb leicht heller */
  --sb-hi:    #2d5aa0;   /* “highlight” blau */
  --sb-mid:   #000b1a;   /* tiefer schatten */
  --sb-dark:  #000000;
}

/* Grundform */
::-webkit-scrollbar {
  width: var(--sb-size);
  height: var(--sb-size);
  background: var(--sb-face);
}

::-webkit-scrollbar-track {
  background: var(--sb-track);
  box-shadow:
    inset 1px 1px 0 var(--sb-mid),
    inset -1px -1px 0 var(--sb-hi);
  border: 1px solid var(--sb-dark);
}

::-webkit-scrollbar-thumb {
  background: var(--sb-thumb);
  border-top: 1px solid var(--sb-hi);
  border-left: 1px solid var(--sb-hi);
  border-right: 1px solid var(--sb-mid);
  border-bottom: 1px solid var(--sb-mid);
  outline: 1px solid var(--sb-dark);
}

/* Ecke */
::-webkit-scrollbar-corner {
  background: var(--sb-face);
  border-top: 1px solid var(--sb-mid);
  border-left: 1px solid var(--sb-mid);
}

/* Buttons */
::-webkit-scrollbar-button {
  width: var(--sb-size);
  height: var(--sb-size);
  background: var(--sb-face);
  border-top: 1px solid var(--sb-hi);
  border-left: 1px solid var(--sb-hi);
  border-right: 1px solid var(--sb-mid);
  border-bottom: 1px solid var(--sb-mid);
  outline: 1px solid var(--sb-dark);

  background-repeat: no-repeat;
  background-position: center;
  background-size: 10px 10px;
}

::-webkit-scrollbar-button:active {
  border-top: 1px solid var(--sb-mid);
  border-left: 1px solid var(--sb-mid);
  border-right: 1px solid var(--sb-hi);
  border-bottom: 1px solid var(--sb-hi);
}

/* ===== Pfeile LIGHT: schwarz ===== */
html:not(.dark) ::-webkit-scrollbar-button:single-button:vertical:decrement { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M5 2 L9 7 H1 Z'/></svg>") !important;}
html:not(.dark) ::-webkit-scrollbar-button:single-button:vertical:increment { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M1 3 H9 L5 8 Z'/></svg>") !important;}
html:not(.dark) ::-webkit-scrollbar-button:single-button:horizontal:decrement {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M2 5 L7 1 V9 Z'/></svg>") !important;}
html:not(.dark) ::-webkit-scrollbar-button:single-button:horizontal:increment {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23000' d='M8 5 L3 1 V9 Z'/></svg>") !important;}

/* ===== Pfeile DARK: gelb ===== */
html.dark ::-webkit-scrollbar-button:single-button:vertical:decrement { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M5 2 L9 7 H1 Z'/></svg>") !important;}
html.dark ::-webkit-scrollbar-button:single-button:vertical:increment { background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M1 3 H9 L5 8 Z'/></svg>") !important;}
html.dark ::-webkit-scrollbar-button:single-button:horizontal:decrement {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M2 5 L7 1 V9 Z'/></svg>") !important;}
html.dark ::-webkit-scrollbar-button:single-button:horizontal:increment {background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10' viewBox='0 0 10 10'><path fill='%23FFD400' d='M8 5 L3 1 V9 Z'/></svg>") !important;}
"""

    def _inject_web_css(self):
        if self.dark_mode:
            js = """
(function(){const id='__qt_dark_css__';let s=document.getElementById(id);if(!s){s=document.createElement('style');
s.id=id;s.innerHTML=`html, body { background-color:#040404 !important;color:#eaeaea !important;}
a { color:#8ab4ff !important;}pre, code { background:#1e1e1e !important;}
`;document.head.appendChild(s);}})();"""
        else:
            js = """(function(){const s=document.getElementById('__qt_dark_css__');if(s) s.remove();})();"""
        self.web.page().runJavaScript(js)

    def _on_url_changed(self, url: QUrl):
        self._inject_web_css()
        
    def _style_theme_button(self):
        # sorgt dafür, dass der Button im Dark Mode wirklich "dark" aussieht
        # (QAction selbst ist kein Widget, aber wir können die Toolbar/Button-Styles über QSS steuern)
        pass

# ---- Resources (icons, ...) -------------------------------------------------
#[:: resources_rc.py ::]
# ---- Parser/Lexer -----------------------------------------------------------
#[:: gen/dBaseLexer.py ::]
#[:: gen/dBaseParser.py ::]
#[:: gen/dBaseParserListener.py ::]
#[:: gen/dBaseParserVisitor.py ::]
# -----------------------------------------------------------------------------
def create_backend_for_base(base_name: str, parent_backend=None):
    QtClass = NATIVE_BASES.get(base_name.upper())
    if QtClass is None:
        raise RuntimeError(f"Unbekannte native Basisklasse: {base_name}")
    bn = base_name.upper()
    # Spezialfälle: Scrollbars brauchen Orientation
    if bn == "VSCROLLBAR":
        return QScrollBar(Qt.Vertical, parent_backend) if parent_backend is not None else QScrollBar(Qt.Vertical)
    if bn == "HSCROLLBAR":
        return QScrollBar(Qt.Horizontal, parent_backend) if parent_backend is not None else QScrollBar(Qt.Horizontal)

    return QtClass(parent_backend) if parent_backend is not None else QtClass()


def _find_mdi_subwindow(widget: Any):
    """Walk up parent widgets to find a QMdiSubWindow wrapper (if any)."""
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


def _qss_color(v: Any) -> Optional[str]:
    """Accepts '#RRGGBB', 'red', 'rgb(...)'. Returns None if empty."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return str(v)

def build_container_qss(inst: "Instance") -> str:
    """Build QSS for CONTAINER (QFrame) from instance properties."""
    props = inst.props
    bg = _qss_color(props.get("BACKCOLOR"))
    bc = _qss_color(props.get("BORDERCOLOR"))
    bw = props.get("BORDERWIDTH")
    radius = props.get("RADIUS")
    extra = props.get("STYLE")

    rules: List[str] = []

    if bg is not None:
        rules.append(f"background-color: {bg};")

    if bc is not None or bw is not None:
        if bw is None:
            bw = 1
        try:
            bw_i = int(bw)
        except Exception:
            bw_i = 1
        if bc is None:
            bc = "#404040"
        rules.append(f"border: {bw_i}px solid {bc};")

    if radius is not None:
        try:
            r_i = int(radius)
        except Exception:
            r_i = 0
        if r_i > 0:
            rules.append(f"border-radius: {r_i}px;")

    if isinstance(extra, str) and extra.strip():
        rules.append(extra.strip().rstrip(";") + ";")

    if not rules:
        return ""
    return "QFrame { " + " ".join(rules) + " }"


def apply_property_to_qt(inst: Instance, prop: str, value: Any):
    if inst.backend is None:
        return
        
    p = prop.upper()
    s = str(value)
    
    # normalisiere Zahlen (dein Interpreter nutzt evtl. float)
    if isinstance(value, float) and value.is_integer():
        value = int(value)

    # CONTAINER (QFrame) Stylesheet-Properties
    if inst.class_name.upper() == "CONTAINER" and p in ("BACKCOLOR", "BORDERCOLOR", "BORDERWIDTH", "RADIUS", "STYLE"):
        qss = build_container_qss(inst)
        inst.backend.setStyleSheet(qss)
        return

    # VALUE/STATE/ITEMS Mappings (Entryfield, Checkbox, Radiobutton, Combobox, Editor, Listbox, Progress, Scrollbar, Spinbox, Image, Text)
    if p in ("VALUE", "CHECKED"):
        b = inst.backend
        # QLineEdit
        if isinstance(b, QLineEdit):
            if p == "VALUE":
                b.setText(str(value))
            return
        # QPlainTextEdit (EDITOR)
        if isinstance(b, QPlainTextEdit):
            if p == "VALUE":
                b.setPlainText(str(value))
            return
        # QCheckBox / QRadioButton
        if isinstance(b, (QCheckBox, QRadioButton)):
            if p in ("VALUE", "CHECKED"):
                b.setChecked(bool(value))
            return
        # QComboBox
        if isinstance(b, QComboBox):
            if p == "VALUE":
                # akzeptiert Index (int) oder Text
                if isinstance(value, (int, float)) and float(value).is_integer():
                    idx = int(value)
                    if 0 <= idx < b.count():
                        b.setCurrentIndex(idx)
                else:
                    txt = str(value)
                    i = b.findText(txt)
                    if i >= 0:
                        b.setCurrentIndex(i)
            return
        # QListWidget (LISTBOX/CHECKLISTBOX)
        if isinstance(b, QListWidget):
            if p == "VALUE":
                # setzt Auswahl nach Index oder Text
                if isinstance(value, (int, float)) and float(value).is_integer():
                    idx = int(value)
                    if 0 <= idx < b.count():
                        b.setCurrentRow(idx)
                else:
                    txt = str(value)
                    for i in range(b.count()):
                        it = b.item(i)
                        if it and it.text() == txt:
                            b.setCurrentRow(i)
                            break
            return
        # QProgressBar / QScrollBar / QSpinBox
        if isinstance(b, (QProgressBar, QScrollBar, QSpinBox)):
            if p == "VALUE":
                try:
                    b.setValue(int(value))
                except Exception:
                    pass
            return
        # QLabel as TEXT
        if isinstance(b, QLabel) and p == "VALUE":
            # VALUE synonym zu TEXT
            b.setText(str(value))
            return

    # ITEMS: füllt ComboBox/ListBox/CheckListBox
    if p in ("ITEMS", "LIST"):
        b = inst.backend
        # value kann list/tuple oder string "a,b,c" sein
        items = None
        if isinstance(value, (list, tuple)):
            items = [str(x) for x in value]
        else:
            sitems = str(value)
            # split an ',' or ';'
            if "," in sitems:
                items = [x.strip() for x in sitems.split(",") if x.strip() != ""]
            elif ";" in sitems:
                items = [x.strip() for x in sitems.split(";") if x.strip() != ""]
            else:
                items = [sitems] if sitems.strip() else []
        if isinstance(b, QComboBox):
            b.clear()
            b.addItems(items)
            return
        if isinstance(b, QListWidget):
            b.clear()
            for t in items:
                it = QListWidgetItem(t)
                # CHECKLISTBOX: Items checkable
                if inst.class_name.upper() == "CHECKLISTBOX":
                    it.setFlags(it.flags() | Qt.ItemIsUserCheckable)
                    it.setCheckState(Qt.Unchecked)
                b.addItem(it)
            return

    # IMAGE: lädt Bilddatei in QLabel
    if p in ("PICTURE", "IMAGEFILE", "FILENAME") and isinstance(inst.backend, QLabel):
        try:
            pm = QPixmap(str(value))
            if not pm.isNull():
                inst.backend.setPixmap(pm)
        except Exception:
            pass
        return
    # Geometry: Qt braucht Left/Top/Width/Height gemeinsam
    # Besonderheit: Wenn das Widget in einem QMdiSubWindow steckt, müssen wir
    # sowohl das SubWindow (Position/Größe im MDI) als auch das eigentliche Widget anpassen.
    if p in ("LEFT", "TOP", "WIDTH", "HEIGHT"):
        # Ausgangswerte aus den gespeicherten Properties
        left   = int(inst.props.get("LEFT",    0)   or 0)
        top    = int(inst.props.get("TOP",     0)   or 0)
        width  = int(inst.props.get("WIDTH", 100)   or 100)
        height = int(inst.props.get("HEIGHT",100)   or 100)

        mdi = _find_mdi_subwindow(inst.backend)

        if mdi is not None:
            # Für MDI: wenn der User das SubWindow verschoben hat, sind LEFT/TOP in props evtl. veraltet.
            # Damit WIDTH/HEIGHT nicht auf alte Position zurückspringen, nehmen wir die aktuelle Position
            # aus dem QMdiSubWindow, wenn nur die Größe geändert wird (und umgekehrt).
            try:
                g = mdi.geometry()
                cur_left, cur_top, cur_w, cur_h = g.x(), g.y(), g.width(), g.height()
            except Exception:
                cur_left, cur_top, cur_w, cur_h = left, top, width, height

            if p in ("WIDTH", "HEIGHT"):
                left, top = cur_left, cur_top
            if p in ("LEFT", "TOP"):
                width, height = cur_w, cur_h

        # jetzt den einen Wert aktualisieren
        if p == "LEFT":   left   = int(value)
        if p == "TOP":    top    = int(value)
        if p == "WIDTH":  width  = int(value)
        if p == "HEIGHT": height = int(value)

        # Properties spiegeln
        inst.props["LEFT"]   = left
        inst.props["TOP"]    = top
        inst.props["WIDTH"]  = width
        inst.props["HEIGHT"] = height

        if mdi is not None:
            # SubWindow anpassen
            try:
                if p in ("LEFT", "TOP"):
                    mdi.move(left, top)
                elif p in ("WIDTH", "HEIGHT"):
                    mdi.resize(width, height)
                else:
                    mdi.setGeometry(left, top, width, height)
            except Exception:
                try:
                    mdi.setGeometry(left, top, width, height)
                except Exception:
                    pass

            # Client-Widget im SubWindow auf die gleiche Größe bringen
            try:
                if hasattr(inst.backend, "move"):
                    inst.backend.move(0, 0)
                if hasattr(inst.backend, "resize"):
                    inst.backend.resize(width, height)
            except Exception:
                pass
        else:
            # Normale Widgets/Fenster
            try:
                inst.backend.setGeometry(left, top, width, height)
            except Exception:
                try:
                    if hasattr(inst.backend, "move"):
                        inst.backend.move(left, top)
                    if hasattr(inst.backend, "resize"):
                        inst.backend.resize(width, height)
                except Exception:
                    pass
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
    runRequested = pyqtSignal()
    hlpRequested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._line_number_area = LineNumberArea(self)

        self._breakpoints = set()  # speichert blockNumber() (0-basiert)
        
        # --- Editor-Farben: Navy Hintergrund + dunkleres Gelb für Text ---
        pal = self.palette()
        pal.setColor(QPalette.Base, QColor("#081a33"))        # Hintergrund (navy)
        pal.setColor(QPalette.Text, QColor("#c9b458"))        # Text (dunkleres Gelb)
        pal.setColor(QPalette.Highlight, QColor("#274b8a"))   # Selection Hintergrund
        pal.setColor(QPalette.HighlightedText, QColor("#f0e6b0"))
        self.setPalette(pal)

        self.breakpointArea = BreakpointArea(self)
        self.lineNumberArea = LineNumberArea(self)
        
        self.blockCountChanged.connect(self._update_gutter_widths)
        self.updateRequest.connect(self._update_gutters_on_scroll)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_gutter_widths()
        self._highlight_current_line()

        # --- Run (F2) ---
        self.act_run = QAction("Run2", self)
        self.act_run.setShortcut(QKeySequence(Qt.Key_F2))
        self.act_run.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.act_run.triggered.connect(self._emit_run_requested)
        self.addAction(self.act_run)
    
    def focusInEvent(self, e):
        print("FileEditorWindow Fokus IN")
        super().focusInEvent(e)
        
    def _emit_run_requested(self):
        self.runRequested.emit()
    
    def contextMenuEvent(self, event):
        std_menu = QPlainTextEdit.createStandardContextMenu(self, event.pos())
        menu = QMenu(self)
        menu.addAction(self.act_run)
        menu.addSeparator()
        for act in std_menu.actions():
            menu.addAction(act)
        menu.exec_(event.globalPos())

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



class ModifiedTabBar(QTabBar):
    """TabBar, der bei 'modified' (tabData == True) eine 2px Linie unter dem Tab-Text zeichnet."""
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        try:
            # Farbe: gleiche wie Scrollbar-Handle (wir nehmen die Highlight-Farbe als sinnvollen Default)
            pen = QPen(self.palette().highlight().color())
            pen.setWidth(2)
            painter.setPen(pen)
            for i in range(self.count()):
                if bool(self.tabData(i)):
                    r = self.tabRect(i)
                    # 2px Linie unten im Tab
                    y = r.bottom() - 1
                    painter.drawLine(r.left()+6, y, r.right()-6, y)
        finally:
            painter.end()

class FileEditorWindow(QDialog):
    def __init__(self, parent, initial_path: str = "", initial_text: str = ""):
        super().__init__(parent)
        self.parent = parent

        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)

        self.setWindowTitle("CodeEditor")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        
        self.CLASS_START_RE = re.compile(r"(?im)^\s*CLASS\s+([A-Za-z_][A-Za-z0-9_]*)\b")
        self.ENDCLASS_RE    = re.compile(r"(?im)^\s*ENDCLASS\b")
        self.METHOD_RE      = re.compile(r"(?im)^\s*METHOD\s+([A-Za-z_][A-Za-z0-9_]*)\b")

        # Optional: eigenes Icon setzen
        icon = self.windowIcon()  # oder QIcon("dein_icon.png")

        # --- Custom TitleBar (frameless window) ---
        #self.titlebar = TitleBar(self, "CodeEditor", icon)

        # Content Frame (Rahmen + Hintergrund)
        self.frame = QFrame(self)
        self.frame.setObjectName("WindowFrame")

        # ---- Outer layout: TitleBar + Frame ----
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        #outer.addWidget(self.titlebar)
        outer.addWidget(self.frame, 1)

        # ---- Inside frame ----
        content_layout = QVBoxLayout(self.frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(8)

        # Filename / path display (optional)
        self.fname = QLabel("")
        self.fname.setObjectName("FileNameLabel")
        self.fname.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.fname.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        content_layout.addWidget(self.fname)

        # Menubar / Toolbar / Statusbar are normal widgets in this QDialog
        self._create_actions()
        self.mb = self._create_menus()
        self.tb = self._create_toolbar()
        self.sb = self._create_statusbar()

        content_layout.addWidget(self.mb)
        content_layout.addWidget(self.tb)

        # Splitter: links Tree, rechts Editor
        self.splitter = QSplitter(Qt.Horizontal, self.frame)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # --- TreeView links ---
        self.tree = QTreeView(self.splitter)
        self.tree.clicked.connect(self._on_tree_clicked)

        # Dummy Model (später kannst du hier Klassen/Methoden/etc. einfüllen)
        self.tree_model = QStandardItemModel()
        self.tree_model.setHorizontalHeaderLabels(["Struktur"])
        
        root = self.tree_model.invisibleRootItem()
        
        self.node_classes = QStandardItem("CLASSES")
        self.node_methods = QStandardItem("METHODS")
        
        root.appendRow(self.node_classes)
        root.appendRow(self.node_methods)
        
        self.tree.setModel(self.tree_model)
        self.tree.expandAll()
        
        self._parse_timer = QTimer(self)
        self._parse_timer.setSingleShot(True)
        self._parse_timer.timeout.connect(self._refresh_structure_tree)

        # --- Editor Tabs (jede Datei ein Tab) ---
        self.editor_tabs = QTabWidget(self.splitter)
        self.editor_tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.editor_tabs.setTabBar(ModifiedTabBar())
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.tabCloseRequested.connect(self._on_tab_close_requested)
        self.editor_tabs.currentChanged.connect(self._on_current_tab_changed)

        # Splitter-Verhältnisse
        self.splitter.setStretchFactor(0, 0)  # Tree
        self.splitter.setStretchFactor(1, 1)  # Editor
        self.splitter.setSizes([220, 800])

        # Splitter soll beim Resize wachsen
        content_layout.addWidget(self.splitter, 1)
        content_layout.addWidget(self.sb)

        # Default: ein neuer Tab (oder initial_path laden)
        if initial_path:
            self.open_path_in_tab(initial_path)
        else:
            self.new_tab(title="(neu)", path="", text=initial_text or "")

        self._update_cursor_status()

    def _schedule_tree_refresh(self):
        # 180ms nach letzter Änderung neu parsen
        self._parse_timer.start(180)
        
    def _refresh_structure_tree(self):
        ed = self.current_editor()
        if ed is None:
            return
        
        text = self._strip_comments_preserve_positions(ed.toPlainText())
        doc  = ed.document()

        # CLASSES-Node leeren
        self.node_classes.removeRows(0, self.node_classes.rowCount())

        # Alle CLASS-Starts finden
        starts = list(self.CLASS_START_RE.finditer(text))
        if not starts:
            self.tree.expand(self.tree_model.indexFromItem(self.node_classes))
            return

        # Für jede CLASS den passenden ENDCLASS suchen (von Start an)
        for i, m in enumerate(starts):
            cls_name = m.group(1)
            cls_start = m.start()

            end_m = self.ENDCLASS_RE.search(text, pos=m.end())
            if not end_m:
                cls_end = len(text)  # unvollständig: bis EOF
            else:
                cls_end = end_m.end()

            # Klassen-Item + Position (für Sprung)
            block = doc.findBlock(cls_start)
            if not block.isValid():
                continue
            cls_line = block.blockNumber()
            cls_col  = cls_start - block.position()

            cls_item = QStandardItem(cls_name)
            cls_item.setData(cls_line, Qt.UserRole)
            cls_item.setData(cls_col,  Qt.UserRole + 1)

            # Unterknoten "METHODS" für diese Klasse
            methods_node = QStandardItem("METHODS")
            cls_item.appendRow(methods_node)

            # Methoden nur im Klassenbereich sammeln
            seen = set()
            for mm in self.METHOD_RE.finditer(text, cls_start, cls_end):
                meth = mm.group(1)
                key = meth.lower()
                if key in seen:
                    continue
                seen.add(key)

                mpos = mm.start()
                mblock = doc.findBlock(mpos)
                if not mblock.isValid():
                    continue
                line = mblock.blockNumber()
                col  = mpos - mblock.position()

                it = QStandardItem(meth)
                it.setData(line, Qt.UserRole)
                it.setData(col,  Qt.UserRole + 1)
                methods_node.appendRow(it)

            self.node_classes.appendRow(cls_item)

        self.tree.expand(self.tree_model.indexFromItem(self.node_classes))

    def _on_tree_clicked(self, index):
        item = self.tree_model.itemFromIndex(index)
        if not item:
            return
            
        if item in (self.node_classes, self.node_methods) or item.text() == "METHODS":
            return

        line = item.data(Qt.UserRole)
        col  = item.data(Qt.UserRole + 1) or 0
        if not isinstance(line, int):
            return

        ed = self.current_editor()
        if ed is None:
            return

        block = ed.document().findBlockByNumber(line)
        if not block.isValid():
            return

        pos = block.position() + int(col)

        cursor = ed.textCursor()
        cursor.setPosition(pos)
        ed.setTextCursor(cursor)
        ed.setFocus()
        ed.centerCursor()
    
    def _strip_comments_preserve_positions(self, text: str) -> str:
        # Block-Kommentare /* ... */
        def repl_block(m):
            return " " * (m.end() - m.start())

        text = re.sub(r"/\*.*?\*/", repl_block, text, flags=re.S)

        # Einzeilige Kommentare: //, &&, **
        def repl_line(m):
            return " " * (m.end() - m.start())

        text = re.sub(r"//.*?$", repl_line, text, flags=re.M)
        text = re.sub(r"&&.*?$", repl_line, text, flags=re.M)
        text = re.sub(r"\*\*.*?$", repl_line, text, flags=re.M)

        return text
    
    def run_current_text(self):
        """Führt den aktuellen Tab-Text aus (Run / F2)."""
        ed = self.current_editor()
        content = ed.toPlainText() if ed is not None else ""
        if not content.strip():
            QMessageBox.information(self, "Info", "Bitte erst Text eingeben.")
            return
        path = getattr(ed, "_path", "") or ""
        if not path:
            # temp file
            path = os.path.join(os.getcwd(), "dbase_run.prg")
            setattr(ed, "_path", path)
            self._update_tab_visuals(self.current_tab_index())
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            parse(path)
        except Exception as e:
            tb_str = traceback.format_exc()
            dlg = showException(self, "Run-Fehler " + type(e).__name__, tb_str)
            dlg.exec_()

    def _create_editor(self):
        # Parent bewusst None: QTabWidget übernimmt Ownership und Resize korrekt
        editor = CodeEditor(None)
        editor.setPlaceholderText("Schreib hier was rein…")
        editor.setLineWrapMode(editor.NoWrap)
        editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        editor.setLineWrapMode(editor.NoWrap)
        editor.setFont(QFont("Consolas", 10))
        
        self.highlighter = DBaseHighlighter(editor.document())
        return editor
        
    def _create_actions(self):
        pass

    def _create_menus(self):
        pass

    def _create_toolbar(self):
        pass

    def _create_statusbar(self):
        sb = QStatusBar(self)
        sb.showMessage("Bereit")
        return sb

    # ---------- File operations ----------
    # ---------- Tab / Editor Helpers ----------
    def current_editor(self) -> CodeEditor:
        w = self.editor_tabs.currentWidget()
        return w  # type: ignore

    def current_tab_index(self) -> int:
        return int(self.editor_tabs.currentIndex())

    def tab_path(self, idx: int) -> str:
        ed = self.editor_tabs.widget(idx)
        return getattr(ed, "_path", "") if ed is not None else ""

    def set_tab_path(self, idx: int, path: str) -> None:
        ed = self.editor_tabs.widget(idx)
        if ed is not None:
            setattr(ed, "_path", path)

    def tab_display_name(self, path: str) -> str:
        return os.path.basename(path) if path else "Unbenannt"

    def _update_tab_visuals(self, idx: int) -> None:
        ed = self.editor_tabs.widget(idx)
        if ed is None:
            return
        modified = bool(ed.document().isModified())
        # TabText: nur Dateiname (ohne Pfad)
        title = self.tab_display_name(getattr(ed, "_path", ""))
        self.editor_tabs.setTabText(idx, title)
        # 2px Linie via TabBar.tabData
        self.editor_tabs.tabBar().setTabData(idx, modified)
        self._update_title()

    def _on_current_tab_changed(self, idx: int) -> None:
        self._update_title()
        # Cursor-Status neu
        try:
            self._update_cursor_status()
        except Exception:
            pass

    def new_tab(self, title: str = "Unbenannt", path: str = "", text: str = "") -> int:
        ed = self._create_editor()
        ed.setFont(QFont("Consolas", 10))
        ed.setLineWrapMode(ed.NoWrap)
        ed.setPlainText(text or "")
        
        ed.document().setModified(False)
        ed.runRequested.connect(self.run_current_text)
        ed.cursorPositionChanged.connect(self._update_cursor_status)
        setattr(ed, "_path", path or "")

        # Syntax Highlighter pro Editor
        try:
            self._highlighter = DBaseHighlighter(ed.document())
        except Exception as e:
            print(e)

        idx = self.editor_tabs.addTab(ed, title)
        self.editor_tabs.setCurrentIndex(idx)

        # Modified Tracking
        ed.document().contentsChanged.connect(self._schedule_tree_refresh)
        ed.document().modificationChanged.connect(lambda _m, i=idx: self._update_tab_visuals(i))

        self._update_tab_visuals(idx)
        return idx

    def open_path_in_tab(self, path: str) -> int:
        path = os.path.normpath(path)
        # bereits offen?
        for i in range(self.editor_tabs.count()):
            if os.path.normpath(self.tab_path(i)) == path:
                self.editor_tabs.setCurrentIndex(i)
                return i
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Datei nicht öffnen:\n{e}")
            txt = ""
        idx = self.new_tab(title=self.tab_display_name(path), path=path, text=txt)
        return idx

    def _on_tab_close_requested(self, idx: int) -> None:
        if not self.maybe_save(idx):
            return
        w = self.editor_tabs.widget(idx)
        self.editor_tabs.removeTab(idx)
        if w is not None:
            w.deleteLater()
        if self.editor_tabs.count() == 0:
            self.close()


    def maybe_save(self, idx: Optional[int] = None) -> bool:
        if idx is None:
            idx = self.current_tab_index()
        ed = self.editor_tabs.widget(idx)
        if ed is None:
            return True
        if not ed.document().isModified():
            return True
        title = self.tab_display_name(getattr(ed, "_path", ""))
        res = QMessageBox.question(
            self,
            "Ungespeicherte Änderungen",
            f"'{title}' hat ungespeicherte Änderungen. Speichern?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        if res == QMessageBox.Yes:
            return self.file_save(idx)
        if res == QMessageBox.No:
            return True
        return False

    def file_new(self):
        self.new_tab(title="Unbenannt", path="", text="")

    def file_save(self, idx: Optional[int] = None) -> bool:
        if idx is None:
            idx = self.current_tab_index()
        ed = self.editor_tabs.widget(idx)
        if ed is None:
            return False
        path = getattr(ed, "_path", "") or ""
        if not path:
            return self.file_save_as(idx)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(ed.toPlainText())
            ed.document().setModified(False)
            try:
                self.sb.showMessage(f"Gespeichert: {path}", 3000)
            except Exception:
                pass
            self._update_tab_visuals(idx)
            return True
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte nicht speichern:\n{e}")
            return False

    def file_save_as(self, idx: Optional[int] = None) -> bool:
        if idx is None:
            idx = self.current_tab_index()
        ed = self.editor_tabs.widget(idx)
        if ed is None:
            return False
        cur_path = getattr(ed, "_path", "") or ""
        dlg = QFileDialog(self, "Speichern unter")
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDefaultSuffix("prg")
        dlg.setNameFilters(["dBase Quellcode (*.prg)", "Alle Dateien (*.*)"])
        if cur_path:
            dlg.selectFile(cur_path)
        if not dlg.exec_():
            return False
        files = dlg.selectedFiles()
        if not files:
            return False
        path = files[0]
        setattr(ed, "_path", path)
        self._update_tab_visuals(idx)
        return self.file_save(idx)

    def closeEvent(self, event):
        for i in range(self.editor_tabs.count()):
            if not self.maybe_save(i):
                event.ignore()
                return
        event.accept()

    def _set_text(self, text: str):
        # legacy helper: set current editor text
        ed = self.current_editor()
        ed.setPlainText(text)
        ed.document().setModified(False)
        self._update_tab_visuals(self.current_tab_index())

    def _update_title(self):
        idx = self.current_tab_index() if hasattr(self, "editor_tabs") else -1
        name = "Unbenannt"
        star = ""
        if idx >= 0:
            ed = self.editor_tabs.widget(idx)
            if ed is not None:
                name = getattr(ed, "_path", "") or "Unbenannt"
                star = " *" if ed.document().isModified() else ""

        if hasattr(self, "fname"):
            self.fname.setText(name)
        self.setWindowTitle(f"{name}{star} - Editor")

    def _update_cursor_status(self):
        ed = self.current_editor()
        if ed is None:
            return
        tc = ed.textCursor()
        line = tc.blockNumber() + 1
        col = tc.positionInBlock() + 1
        try:
            self.sb.showMessage(f"Zeile {line}, Spalte {col}")
        except Exception:
            pass

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

    
    def reparent_instance(self, child: Instance, new_parent: Optional[Instance]) -> None:
        """Re-parent a runtime instance (and its Qt backend) to a new parent instance.

        This makes `child.parent`, `child.parent.parent`, ... work and also updates Qt parenting,
        so property updates (like this.parent.text=...) hit the correct widget tree.
        """
        old_parent = child.parent
        if old_parent is new_parent:
            return

        # 1) detach from old parent's child map (best-effort)
        if old_parent is not None:
            try:
                # remove any aliases pointing to this child
                for k, v in list(old_parent.children.items()):
                    if v is child:
                        old_parent.children.pop(k, None)
                for k, v in list(old_parent.props.items()):
                    if v is child:
                        old_parent.props.pop(k, None)
            except Exception:
                pass

        # 2) update runtime parent
        child.parent = new_parent

        # 3) update Qt backend parent (best-effort; not every backend supports parenting)
        try:
            cb = getattr(child, "backend", None)
            pb = getattr(new_parent, "backend", None) if new_parent is not None else None
            if cb is not None and hasattr(cb, "setParent"):
                cb.setParent(pb)
        except Exception:
            # ignore backend parenting issues; runtime parenting still works
            pass

    def bind_child(self, owner: Instance, name: str, child: Instance):
        key = name.upper()
        
        # wenn Parent eine Font hat und Kind noch nicht: übernehmen
        if "FONT" in owner.props and "FONT" not in child.props:
            self.set_prop(child, "FONT", owner.props["FONT"], None)
            

        # runtime parenting + Qt parenting
        self.reparent_instance(child, owner)

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
            # 0) Parent chain
            if key == "PARENT":
                return obj.parent

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



            # 1b) Fallback: Geometry-Eigenschaften direkt vom Backend lesen,
            #     falls sie nicht im props-Dict liegen (damit Ausdrücke wie THIS.WIDTH = THIS.WIDTH + 10 gehen).
            if key in ("LEFT", "TOP", "WIDTH", "HEIGHT"):
                b = getattr(obj, "backend", None)
                if b is not None:
                    try:
                        # In MDI-Kontext beziehen wir uns auf das QMdiSubWindow (falls vorhanden),
                        # weil LEFT/TOP dort die Position im MDI-Bereich bedeutet.
                        mdi = _find_mdi_subwindow(b)
                        gb = mdi.geometry() if mdi is not None else b.geometry()
                        if key == "LEFT":
                            return int(gb.x())
                        if key == "TOP":
                            return int(gb.y())
                        if key == "WIDTH":
                            return int(gb.width())
                        if key == "HEIGHT":
                            return int(gb.height())
                    except Exception:
                        pass
                # Default, wenn kein Backend vorhanden
                return int(obj.props.get(key, 0) or 0)

            # 1b) Fallback: gängige Text-Eigenschaften direkt vom Backend lesen,
            #     falls sie nicht im props-Dict liegen (z.B. initialer Fenstertitel/Button-Text).
            if key in ("TEXT", "CAPTION", "TITLE"):
                b = getattr(obj, "backend", None)
                if b is not None:
                    # Form/Dialog
                    if hasattr(b, "windowTitle") and callable(getattr(b, "windowTitle")):
                        try:
                            return b.windowTitle()
                        except Exception:
                            pass
                    # Buttons/Labels etc.
                    if hasattr(b, "text") and callable(getattr(b, "text")):
                        try:
                            return b.text()
                        except Exception:
                            pass
                # Kein Backend oder nicht lesbar
                return ""

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

        head = parts[0].upper()
        if head == "THIS":
            # bevorzugt this_obj (sicher in Methoden), fallback auf Variable THIS
            cur = self.this_obj
            if cur is None:
                cur = self.get_var("THIS", ctx)
        else:
            cur = self.get_var(parts[0], ctx)

        if cur is None:
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{parts[0]}' ist None")
        
        prev_path = parts[0].upper()

        for name in parts[1:]:
            # Wenn ein Zwischenergebnis None ist (z.B. Parent nicht gesetzt), sauber abbrechen
            if cur is None:
                raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
            key = name.upper()
            prev_path = prev_path + "." + key


            if isinstance(cur, Instance):
                if hasattr(cur, "props") and key in cur.props:
                    cur = cur.props[key]
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
                    continue

                if self.resolve_method_silent(cur.class_name.upper(), key) is not None:
                    cur = Delegate(target=cur, method_name=key, runner=self)
                    continue
                    
                # 1) Property/Child?
                val = cur.props.get(name.upper())
                if val is not None:
                    cur = val
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
                    continue

                # 2) Methode?
                mctx = self.resolve_method_silent(cur.class_name.upper(), name.upper())
                if mctx is not None:
                    return Delegate(target=cur, method_name=name.upper(), runner=self)

                # 3) Fallback: zentrale Member-Logik benutzen (inkl. native OPEN)
                try:
                    cur = self.get_member(cur, name, ctx)   # <-- name ist "Open" im Original
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
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
            if isinstance(parent_inst, Instance):
                inst.parent = parent_inst
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
        parent_inst = args[0] if args else None
        if isinstance(parent_inst, Instance):
            inst.parent = parent_inst
        parent_backend = parent_inst.backend if isinstance(parent_inst, Instance) else None
        
        # base backend (FORM etc.)
        if classdef.parent:
            inst.backend = create_backend_for_base(classdef.parent, parent_backend)
        
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

        # 1b) Reparenting: `obj.parent = otherObj` (or `obj.parent = null`)
        if key == "PARENT":
            new_parent = value if isinstance(value, Instance) else None
            self.reparent_instance(inst, new_parent)
            # keep the property value as-is for scripts that inspect it
            inst.props[key] = new_parent
            return
        
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
            win.resize(600, 500)
            sub = MAINAPP.mdi.addSubWindow(win)
            
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
        self.resize(620, 320)

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

        # Run per F2 (auch ohne Kontextmenü)
        self.text.runRequested.connect(self.on_button_run_clicked)
        self.act_run_f2 = QAction("Run1", self)
        self.act_run_f2.setShortcut(QKeySequence(Qt.Key_F2))
        self.act_run_f2.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.act_run_f2.triggered.connect(self.on_button_run_clicked)
        self.addAction(self.act_run_f2)
        
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
    
    def on_button_hlp_clicked(self):
        print("hhhhh")
        
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

class RegieCenter(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFont(QFont("Arial", 10))

        self.setWindowTitle("Regierzentrum")
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

        self.lw1 = IconTab(); self.icon_lists.append(self.lw1); self.tabs.addTab(self.lw1, "Alle Typen")
        self.lw2 = IconTab(); self.icon_lists.append(self.lw2); self.tabs.addTab(self.lw2, "Projekte"  )
        self.lw3 = IconTab(); self.icon_lists.append(self.lw3); self.tabs.addTab(self.lw3, "Formulare" )
        self.lw4 = IconTab(); self.icon_lists.append(self.lw4); self.tabs.addTab(self.lw4, "Berichte"  )
        self.lw5 = IconTab(); self.icon_lists.append(self.lw5); self.tabs.addTab(self.lw5, "Programme" )
        self.lw6 = IconTab(); self.icon_lists.append(self.lw6); self.tabs.addTab(self.lw6, "Tabellen"  )
        self.lw7 = IconTab(); self.icon_lists.append(self.lw7); self.tabs.addTab(self.lw7, "SQL"       )
        self.lw8 = IconTab(); self.icon_lists.append(self.lw8); self.tabs.addTab(self.lw8, "Grafiken"  )
        self.lw9 = IconTab(); self.icon_lists.append(self.lw9); self.tabs.addTab(self.lw9, "Internet"  )
        self.lwA = IconTab(); self.icon_lists.append(self.lwA); self.tabs.addTab(self.lwA, "Sonstiges" )

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
        
        self.dark_mode = True

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
        
        self._apply_theme()
        
        dlg = RegieCenter()
        sub = self.mdi.addSubWindow(dlg)
        sub.resize(520,300)
        sub.move(30,30)
        sub.show()
        
        #self.mdi_open_editor()
        self.mdi_open_table_designer()

    def on_action_file_close(self):
        # Datei -> Schließen: Tab schließen (wenn Editor aktiv), sonst SubWindow schließen
        sub = self.mdi.activeSubWindow()
        if not sub:
            return
        w = sub.widget()
        if isinstance(w, FileEditorWindow):
            idx = w.current_tab_index()
            w._on_tab_close_requested(idx)
            return
        sub.close()

    def on_action_file_database(self):
        print("file data base")
    def on_action_file_exit(self):
        print("file exit")
        self.close()
    def on_action_file_new_project(self):
        print("file new project")
    def on_action_file_open(self):
        # Datei -> Öffnen: in CodeEditor-Tabs öffnen
        dlg = QFileDialog(self, "Datei öffnen")
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["dBase Quellcode (*.prg)", "Alle Dateien (*.*)"])
        dlg.setDefaultSuffix("prg")
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if not dlg.exec_():
            return
        files = dlg.selectedFiles()
        if not files:
            return
        path = files[0]

        # aktives SubWindow prüfen
        sub = self.mdi.activeSubWindow()
        win = sub.widget() if sub else None

        if isinstance(win, FileEditorWindow):
            win.open_path_in_tab(path)
            win.raise_()
            win.activateWindow()
            return

        # sonst: neues Editor-Fenster öffnen und Tab hinzufügen
        try:
            new_win = FileEditorWindow(parent=self, initial_path="", initial_text="")
            subw = self.mdi.addSubWindow(new_win)
            new_win.resize(700, 500)
            new_win.show()
            new_win.open_path_in_tab(path)
            self.mdi.setActiveSubWindow(subw)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Editor nicht öffnen:\n{e}")

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
        sub.resize(600,250)
        sub.move(56,320)
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

    def _apply_theme(self):
        app = QApplication.instance()
        pal = QPalette()
        
        if self.dark_mode:
            pal.setColor(QPalette.Window, QColor(40, 40, 40))
            pal.setColor(QPalette.WindowText, Qt.black)
            pal.setColor(QPalette.Base, QColor(34, 34, 34))
            pal.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
            pal.setColor(QPalette.Text, Qt.white)
            pal.setColor(QPalette.Button, QColor(45, 45, 45))
            pal.setColor(QPalette.ButtonText, Qt.white)
            pal.setColor(QPalette.Highlight, QColor(80, 120, 200))
            pal.setColor(QPalette.HighlightedText, Qt.white)
        else:
            pal = app.style().standardPalette()
        
        app.setPalette(pal)
        
        if self.dark_mode:
            header_bg               = "#222222"
            header_fg               = "#ffd866"
            tree_bg                 = "#181818"
            tree_fg                 = "#ffffff"
            sel_bg                  = "#2b4c7e"
            sel_fg                  = "#ffffff"
            border                  = "#333333"
            
            tab_bg                  = "#1c1c1c"
            tab_bar_bg              = "#161616"
            tab_fg                  = "#eaeaea"
            tab_fg_active           = "#ffd866"
            tab_sel_bg              = "#242424"
            tab_hover_bg            = "#202020"
            
            toolbar_bg              = "#1a1a1a"
            toolbtn_bg              = "#222222"
            toolbtn_fg              = "#ffd866"
            toolbtn_hover           = "#2a2a2a"
            toolbtn_pressed         = "#303030"
            
            title_bg                = "#121212"  # Hintergrund Titelleiste
            title_fg                = "#1fd816"  # Text/Farbe Buttons (oder "#ffffff")
            title_btn_bg            = "#1f1f1f"  # Buttons normal
            title_btn_hover         = "#2a2a2a"  # Buttons hover
            title_btn_close_hover   = "#8a1f1f"  # Close hover
            
            status_bg               = "#121212"
            status_fg               = "#ffd866"  # oder "#ffffff"
            status_border           = "#333333"
            
            # Scrollbar dark-blue
            sb_face  = "#001f4d"   # navy
            sb_track = "#001a40"
            sb_thumb = "#002b66"
            sb_hi    = "#2d5aa0"
            sb_mid   = "#000b1a"
            sb_dark  = "#000000"
            arrow    = "#FFD400"

        else:
            header_bg               = "#f0f0f0"
            header_fg               = "#000000"
            tree_bg                 = "#ffffff"
            tree_fg                 = "#000000"
            sel_bg                  = "#cfe3ff"
            sel_fg                  = "#000000"
            border                  = "#d0d0d0"
            
            tab_bg                  = "#f4f4f4"
            tab_bar_bg              = "#ededed"
            tab_fg                  = "#000000"
            tab_fg_active           = "#000000"
            tab_sel_bg              = "#ffffff"
            tab_hover_bg            = "#f9f9f9"
            
            toolbar_bg              = "#f2f2f2"
            toolbtn_bg              = "#e9e9e9"
            toolbtn_fg              = "#000000"
            toolbtn_hover           = "#dedede"
            toolbtn_pressed         = "#d2d2d2"
            
            title_bg                = "#eaeaea"
            title_fg                = "#000000"
            title_btn_bg            = "#f3f3f3"
            title_btn_hover         = "#dedede"
            title_btn_close_hover   = "#e06c75"
            
            status_bg               = "#ededed"
            status_fg               = "#000000"
            status_border           = "#d0d0d0"
            
            # Scrollbar light-gray
            sb_face  = "#c0c0c0"
            sb_track = "#e6e6e6"
            sb_thumb = "#c0c0c0"
            sb_hi    = "#ffffff"
            sb_mid   = "#808080"
            sb_dark  = "#000000"
            arrow    = "#000000"
        
        size = 21  # Win95 vibe
        self.setStyleSheet(f"""
QMenuBar {{ background: #1a1a1a; color: #ffd866; }}
QMenuBar::item {{ background: transparent; padding: 6px 10px; }}
QMenuBar::item:selected {{ background: #2a2a2a; }}
QMenu {{ background: #141414; color: #ffffff; border: 1px solid #333333; }}
QMenu::separator {{
    height: 2px;
    margin: 6px 10px;
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #2a2a2a,
        stop:1 #555555
    );
}}
QMenu::item:selected {{ background: #2b4c7e; color: #ffffff; }}
QMdiArea {{
    background: #2e2e2e;           /* noch dunkler */
    border: 2px solid #333333;
}}
QMdiArea::viewport {{
    background: #2b2b2b;           /* viewport ist oft entscheidend */
}}
/* optional: Subwindows im Dark Mode passend */
QMdiSubWindow {{
    background: #343434;
    border: 2px solid #333333;
}}
QMdiSubWindow:title {{
    background: #0;
    color: #ffffff;
}}
QComboBox {{
    background: #2a2a2a;          /* Feld grau */
    color: #ffffff;
    border: 1px solid #333333;
    padding: 6px 10px;
    padding-right: 28px;          /* Platz für den Pfeil */
}}

QComboBox:hover {{
    background: #303030;
}}

QComboBox:disabled {{
    background: #202020;
    color: #777777;
}}

/* Drop-down Button rechts */
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    border-left: 1px solid #333333;
    background: #222222;
}}

QComboBox::drop-down:hover {{
    background: #2a2a2a;
}}

/* Pfeil */
QComboBox::down-arrow {{
    width: 10px;
    height: 10px;
    background: #ffd866;          /* oder #000000 im Light Mode */
}}

/* Popup-Liste */
QComboBox QAbstractItemView {{
    background: #1c1c1c;
    color: #ffffff;
    border: 1px solid #333333;
    selection-background-color: #2b4c7e;
    selection-color: #ffffff;
    outline: 1px;
}}
QTableView, QTableWidget {{
    background: #0b0b0b;
    color: #ffffff;
    gridline-color: #333333;
    border: 1px solid #333333;
    selection-background-color: #2b4c7e;
    selection-color: #ffffff;
}}

/* WICHTIG: leere Fläche kommt oft vom viewport */
QTableView::viewport, QTableWidget::viewport {{
    background: #0b0b0b;
}}

/* Header oben/links */
QHeaderView::section {{
    background: #222222;
    color: #ffd866;
    padding: 6px;
    border: none;
    border-right: 1px solid #333333;
    border-bottom: 1px solid #333333;
}}

/* Der “Eck-Button” oben links (häufig DER weiße Fleck) */
QTableCornerButton::section {{
    background: #222222;
    border-right: 1px solid #333333;
    border-bottom: 1px solid #333333;
}}

QMessageBox {{
    background-color: #2b2b2b;
    color: #e8e8e8;
    font-size: 10pt;
}}
QMessageBox QLabel {{
    color: #e8e8e8;
}}
QMessageBox QLabel#qt_msgbox_label {{
    color: #e8e8e8;
}}
QMessageBox QLabel#qt_msgboxex_icon_label {{
    /* Icon-Label */
    padding-right: 10px;
}}
QMessageBox QTextEdit {{
    background-color: #232323;
    color: #e8e8e8;
    border: 1px solid #3a3a3a;
    border-radius: 8px;
}}
QMessageBox QAbstractButton, QMessageBox QPushButton {{
    background-color: #3a3a3a;
    color: #f0f0f0;
    border: 1px solid #555;
    border-radius: 8px;
    padding: 6px 12px;
    min-width: 90px;
}}
QMessageBox QPushButton:hover {{
    background-color: #444;
    border-color: #777;
}}
QMessageBox QPushButton:pressed {{
    background-color: #2f2f2f;
}}
QMessageBox QPushButton:default {{
    border: 1px solid #a33;   /* dezenter roter Akzent */
}}
QMessageBox QPushButton:focus {{
    outline: none;
    border: 1px solid #888;
}}

/* Optional: falls Qt dort eine Ecke der ScrollArea malt */
QAbstractScrollArea::corner {{
    background: #222222;
    border: 1px solid #333333;
}}
QToolBar {{spacing: 8px;background: {toolbar_bg};border: none;}}
QToolBar::separator {{background: {border};width: 1px;margin: 6px 8px;}}
QLineEdit {{padding: 6px 10px;border: 1px solid {border};background: {tab_bg};color: {tab_fg};}}
QLabel {{color: {tab_fg};}}
QToolButton {{background: {toolbtn_bg};color: {toolbtn_fg};border: 1px solid {border};padding: 6px 10px;}}
QToolButton:hover {{background: {toolbtn_hover};}}
QToolButton:pressed {{background: {toolbtn_pressed};}}
QTabWidget::pane {{border: 1px solid {border};top: -1px;background: {tab_bg};}}
QTabBar {{background: {tab_bar_bg};}}
QTabBar::tab {{background: {tab_bar_bg};color: {tab_fg};border: 1px solid {border};border-bottom: none;padding: 7px 14px;margin-right: 6px;min-width: 90px;}}
QTabBar::tab:hover {{background: {tab_hover_bg};}}
QTabBar::tab:selected {{background: {tab_sel_bg};color: {tab_fg_active};}}
QTreeView {{border: none;background: {tree_bg};color: {tree_fg};}}
QTreeView::item:selected {{background: {sel_bg};color: {sel_fg};}}
QHeaderView::section {{background: {header_bg};color: {header_fg};padding: 6px;border: none;border-bottom: 1px solid {border};}}
QPushButton {{background: {toolbtn_bg};color: {toolbtn_fg};border: 1px solid {border};border-radius: 10px;padding: 7px 12px;}}
QPushButton:hover {{background: {toolbtn_hover};}}
QPushButton:pressed {{background: {toolbtn_pressed};}}
TopContainer {{ background: transparent; }}
TitleBar {{background: {title_bg};}}
TitleLabel {{color: {title_fg};font-weight: 600;}}
TitleSeparator {{background: {border};}}
QPushButton#TitleBtnMin,QPushButton#TitleBtnMax,QPushButton#TitleBtnClose {{background: {title_btn_bg};color: {title_fg};border: 1px solid {border};border-radius: 10px;}}
QPushButton#TitleBtnMin:hover,QPushButton#TitleBtnMax:hover {{background: {title_btn_hover};}}
QPushButton#TitleBtnClose:hover {{background: {title_btn_close_hover};}}
QStatusBar {{background: {status_bg};color: {status_fg};border-top: 1px solid {status_border};}}
QStatusBar QLabel {{color: {status_fg};}}
QTabBar::scroller {{width: 22px;height: 22px;background: {tab_bar_bg};border: 1px solid {border};border-radius: 10px;margin: 2px;}}
QTabBar::scroller:hover {{background: {tab_hover_bg};}}
QTabBar QToolButton {{background: {tab_bar_bg};border: 1px solid {border};border-radius: 10px;padding: 2px;color: {tab_fg_active};}}
QTabBar QToolButton:hover {{background: {tab_hover_bg};}}
QTabBar QToolButton:pressed {{background: {tab_sel_bg};}}
QSplitter {{background: {tree_bg};}}
QSplitter::handle {{background: {border};}}
QWebEngineView {{background: {tree_bg};}}
QScrollBar:vertical {{background: {sb_face};width: {size}px;margin: 0px;border: 1px solid {sb_dark};}}
QScrollBar:horizontal {{background: {sb_face};height: {size}px;margin: 0px;border: 1px solid {sb_dark};}}
QScrollBar::track:vertical, QScrollBar::track:horizontal {{background: {sb_track};}}
QScrollBar::handle:vertical {{background: {sb_thumb};min-height: 28px;border-top: 1px solid {sb_hi};border-left: 1px solid {sb_hi};border-right: 1px solid {sb_mid};border-bottom: 1px solid {sb_mid};}}
QScrollBar::handle:horizontal {{background: {sb_thumb};min-width: 28px;border-top: 1px solid {sb_hi};border-left: 1px solid {sb_hi};border-right: 1px solid {sb_mid};border-bottom: 1px solid {sb_mid};}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{background: transparent;}}
QScrollBar::sub-line:vertical {{background: {sb_face};height: {size}px;border-top: 1px solid {sb_hi};border-left: 1px solid {sb_hi};border-right: 1px solid {sb_mid};border-bottom: 1px solid {sb_mid};}}
QScrollBar::add-line:vertical {{background: {sb_face};height: {size}px;border-top: 1px solid {sb_hi};border-left: 1px solid {sb_hi};border-right: 1px solid {sb_mid};border-bottom: 1px solid {sb_mid};}}
QScrollBar::sub-line:horizontal {{background: {sb_face};width: {size}px;border-top: 1px solid {sb_hi};border-left: 1px solid {sb_hi};border-right: 1px solid {sb_mid};border-bottom: 1px solid {sb_mid};}}
QScrollBar::add-line:horizontal {{background: {sb_face};width: {size}px;border-top: 1px solid {sb_hi};border-left: 1px solid {sb_hi};border-right: 1px solid {sb_mid};border-bottom: 1px solid {sb_mid};}}
QScrollBar::sub-line:vertical:pressed, QScrollBar::add-line:vertical:pressed,
QScrollBar::sub-line:horizontal:pressed, QScrollBar::add-line:horizontal:pressed {{border-top: 1px solid {sb_mid};border-left: 1px solid {sb_mid};border-right: 1px solid {sb_hi};border-bottom: 1px solid {sb_hi};}}
QScrollBar::up-arrow:vertical {{width: 8px; height: 8px;background: {arrow};}}
QScrollBar::down-arrow:vertical {{width: 8px; height: 8px;background: {arrow};}}
QScrollBar::left-arrow:horizontal {{width: 8px; height: 8px;background: {arrow};}}
QScrollBar::right-arrow:horizontal {{width: 8px; height: 8px;background: {arrow};}}
QScrollBar::sub-line:vertical {{ subcontrol-position: top;    subcontrol-origin: margin; }}
QScrollBar::add-line:vertical {{ subcontrol-position: bottom; subcontrol-origin: margin; }}
QScrollBar::sub-line:horizontal {{ subcontrol-position: left;  subcontrol-origin: margin; }}
QScrollBar::add-line:horizontal {{ subcontrol-position: right; subcontrol-origin: margin; }}
""")

def center_on_screen(widget):
    widget.adjustSize()
    screen = QApplication.primaryScreen()
    ag = screen.availableGeometry()  # ohne Taskbar
    fg = widget.frameGeometry()
    fg.moveCenter(ag.center())
    widget.move(fg.topLeft())

def main():
    app = ensure_qt_app()
    if app is not None:
        f1filter = F1Filter()
        app.installEventFilter(f1filter)
        app.setStyle(FontTriangleArrowsStyle(app.style(), color="#d7b300", font_family="Segoe UI Symbol"))
        global MAINAPP
        MAINAPP = MainWindow()
        MAINAPP.show()
        center_on_screen(MAINAPP)
        sys.exit(app.exec_())
    else:
        print("Qt5 kann nicht gestartet werden.")
        sys.exit(1)

if __name__ == "__main__":
    main()
