# ---------------------------------------------------------------------------
# File:   uiRunner.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import sys
import os
import builtins
import re
import json
from datetime import datetime
import tempfile

from   share.common                 import *
from   share.excepts                import *
from   share.locales                import *
from   share.editors.editor         import *

import share.utildef
from   share.utildef.sysinfo        import SystemInfo
from   share.utildef.helpwin        import *
from   share.utildef.theme          import *
from   share.widgets.button.glossy  import *

from   parse.dbase.parser           import *
import parse.dbase.parser as _dbase_parser_runtime

# ---------------------------------------------------------------------------
# perform Windows 10/11 specifiec stuff ...
# ---------------------------------------------------------------------------
if SystemInfo.is_windows():
    import ctypes
    debug_print(share.locales.tr("Windows detected"))
elif SystemInfo.is_linux():
    debug_print(share.locales.tr("Linux detected"))
else:
    debug_print(share.locales.tr("could not detect operating system,"))
    sys.exit(1)

if "_PDF_BACKEND_AVAILABLE" not in globals():
    _PDF_BACKEND_AVAILABLE = False
if "_PDF_BACKEND_IMPORT_ERROR" not in globals():
    _PDF_BACKEND_IMPORT_ERROR = None
_PDF_BACKEND_WARNING_EMITTED = False


faulthandler.enable(open(share.common.LOG, "a", buffering=1), all_threads=True)


def load_qss(rel_path: str) -> str:
    p = app_dir() / rel_path
    return p.read_text(encoding="utf-8")

_RUNNER_LANGUAGE = (os.environ.get("DBASERUNNER_LANGUAGE") or "dbase").strip().lower()

def _runner_window_title() -> str:
    author = f"Runner 2026 - (c) Jens Kallup - paule32"
    titles = {
        "dbase" : f"dBase  {author}",
        "pascal": f"Pascal {author}",
        "cc"    : f"C/C++  {author}",
        "lisp"  : f"LISP   {author}",
    }
    return titles.get(_RUNNER_LANGUAGE, titles["dbase"])

# ---------------------------------------------------------------------------
# ensure_qt_app (safe early stub)
# Some crashes can happen during module import before Qt widgets are loaded.
# This stub allows the excepthook to avoid NameError and fail gracefully.
# ---------------------------------------------------------------------------
def ensure_qt_app():
    try:
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        return app
    except Exception:
        return False, None

def excepthook(etype, value, tb):
    content = ""
    
    with open(share.common.LOG, "w", buffering=1) as f:
        f.write(share.locales.tr("\n--- PYTHON UNCAUGHT EXCEPTION ---\n"))
        traceback.print_exception(etype, value, tb, file=f)
        f.close()
        
    app = ensure_qt_app()

    # If Qt isn't available yet (e.g. crash during import), just log and fall back.
    if app is not None:
        try:
            with open(share.common.LOG, "r") as f:
                content = f.read()

            dlg = share.excepts.ErrorMessage(
                title    = share.locales.tr("Laufzeitfehler"),
                message  = content,
                log_path = share.common.LOG,
                parent   = None
            )
            dlg.exec_()
        except Exception:
            # Never let the excepthook crash the program.
            pass

    sys.__excepthook__(etype, value, tb)

sys.excepthook = excepthook
debug_print(share.locales.tr("hook installed."))

APPINST = ensure_qt_app()
if APPINST is None:
    if SystemInfo.is_windows():
        ctypes.windll.user32.MessageBoxW(0,
            share.locales.tr("Application could not be initialized."),
            share.locales.tr("Internal Error:"),
            0)
        sys.exit(1)
    else:
        debug_print(share.locales.tr("internal error"))
        sys.exit(1)

base = Path(sys.argv[0]).resolve().parent
cand = list(base.rglob("QtWebEngineProcess.exe"))
try:
    with open(share.common.LOG, "a", buffering=1) as f:
        f.write(f"base={base}\nQtWebEngineProcess={cand}\n")
except Exception:
    pass
    
try:
    def qt_msg_handler(mode, context, message):
        with open(share.common.LOG, "a", buffering=1) as f:
            f.write(f"[QT] {message}\n")
    qInstallMessageHandler(qt_msg_handler)
except Exception as e:
    if SystemInfo.is_windows():
        ctypes.windll.user32.MessageBoxW(0,
            share.locales.tr("Could not install Qt5 Message Handler."),
            share.locales.tr("Error:"),0)
        sys.exit(1)
    else:
        debug_print(e)
        pass


def _runtime_escape_enabled_live() -> bool:
    try:
        return bool(getattr(_dbase_parser_runtime, "_RUNTIME_ESCAPE_ENABLED", False))
    except Exception:
        return False

def _is_runtime_escape_target(candidate: Any = None, fallback_sub: Any = None) -> bool:
    try:
        w = candidate if isinstance(candidate, QWidget) else QApplication.focusWidget()
    except Exception:
        w = None

    while w is not None:
        try:
            if bool(w.property("_DBASE_ESCAPE_TARGET")):
                return True
        except Exception:
            pass
        try:
            w = w.parentWidget()
        except Exception:
            try:
                w = w.parent()
            except Exception:
                w = None

    try:
        sub = fallback_sub if fallback_sub is not None else find_mdi_subwindow_robust(candidate)
    except Exception:
        sub = None

    if sub is not None:
        try:
            inner = sub.widget()
        except Exception:
            inner = None
        for probe in (sub, inner):
            try:
                if probe is not None and bool(probe.property("_DBASE_ESCAPE_TARGET")):
                    return True
            except Exception:
                pass

    return False

class _GlobalEscapeCloseFilter(QObject):
    def _candidate_widget(self, obj):
        try:
            if isinstance(obj, QWidget):
                return obj
        except Exception:
            pass
        try:
            fw = QApplication.focusWidget()
            if fw is not None:
                return fw
        except Exception:
            pass
        return None

    def eventFilter(self, obj, event):
        try:
            et = event.type()
            if et not in (QEvent.ShortcutOverride, QEvent.KeyPress) or event.key() != Qt.Key_Escape:
                return False
        except Exception:
            return False

        candidate = self._candidate_widget(obj)

        blocked_widget, blocked_sub = share.common.resolve_escape_block_target(candidate)
        if blocked_widget is not None or blocked_sub is not None:
            try:
                event.accept()
            except Exception:
                pass
            return True

        close_widget, close_sub = share.common.resolve_escape_close_target(candidate)
        if close_widget is not None or close_sub is not None:
            try:
                event.accept()
            except Exception:
                pass
            # Wichtig: Auch bei ShortcutOverride bereits schliessen.
            # Wenn wir das Event hier konsumieren, kommt oft kein KeyPress mehr an.
            if not close_escape_target(close_widget, close_sub):
                try:
                    fallback_sub = find_mdi_subwindow_robust(candidate)
                except Exception:
                    fallback_sub = None
                if fallback_sub is not None:
                    close_escape_target(candidate, fallback_sub)
            return True

        target_widget, sub = share.common.resolve_escape_target(candidate)
        if target_widget is not None or sub is not None:
            try:
                event.accept()
            except Exception:
                pass
            if _runtime_escape_enabled_live():
                if not close_escape_target(target_widget, sub):
                    try:
                        fallback_sub = find_mdi_subwindow_robust(candidate)
                    except Exception:
                        fallback_sub = None
                    if fallback_sub is not None:
                        close_escape_target(candidate, fallback_sub)
            return True

        # Robuster Fallback: Wenn der Fokus in einem MDI-Unterfenster liegt,
        # ESC soll nur dann schliessen, wenn es sich nicht um ein dBase-Laufzeitfenster
        # handelt oder SET ESCAPE ON aktiv ist. Bei SET ESCAPE OFF blockieren wir ESC,
        # damit QDialog nicht per Default-Reject ausserhalb unserer Laufzeitlogik schliesst.
        try:
            fallback_sub = find_mdi_subwindow_robust(candidate)
        except Exception:
            fallback_sub = None

        if fallback_sub is not None:
            try:
                event.accept()
            except Exception:
                pass

            is_dbase_runtime_target = _is_runtime_escape_target(candidate, fallback_sub)

            if is_dbase_runtime_target:
                if _runtime_escape_enabled_live():
                    close_escape_target(candidate, fallback_sub)
                return True

            close_escape_target(candidate, fallback_sub)
            return True

        return False


def _ensure_escape_filter_installed():
    global _RUNTIME_ESCAPE_FILTER
    #if _RUNTIME_ESCAPE_FILTER is not None:
    #    return _RUNTIME_ESCAPE_FILTER
    try:
        app = QApplication.instance()
        if app is None:
            return None
        _RUNTIME_ESCAPE_FILTER = _GlobalEscapeCloseFilter(app)
        app.installEventFilter(_RUNTIME_ESCAPE_FILTER)
        return _RUNTIME_ESCAPE_FILTER
    except Exception:
        return None

# ---------------------------------------------------------------------------
# Qt message handleer (for WebEngine) ...
# ---------------------------------------------------------------------------
def qt_msg_handler(mode, context, message):
    with open(share.common.LOG, "a", buffering=1) as f:
        f.write(f"[QT] {message}\n")

qInstallMessageHandler(qt_msg_handler)

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

SVG_SQL = r"""
<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <rect x="6" y="4" width="26" height="36" rx="4" fill="#e5e7eb" stroke="#334155" stroke-width="2"/>
  <path d="M26 4v8h8" fill="#cbd5e1"/>
  <rect x="10" y="18" width="28" height="18" rx="6" fill="#2563eb" stroke="#1e40af" stroke-width="2"/>
  <text x="24" y="31" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#ffffff">SQL</text>
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


def delete_last_line(edit):
    doc = edit.document()
    if doc.blockCount() == 0:
        return

    c = edit.textCursor()
    c.beginEditBlock()

    c.movePosition(QTextCursor.End)
    c.select(QTextCursor.BlockUnderCursor)   # letzte Zeile (Block)
    c.removeSelectedText()

    # falls am Ende noch ein Zeilenumbruch übrig bleibt: den auch weg
    if doc.blockCount() > 1 and doc.lastBlock().text() == "":
        c.deletePreviousChar()

    c.endEditBlock()

# ---------------------------------------------------------------------------
# dBase field types ...
# ---------------------------------------------------------------------------
TYPE_VALUES = [
    share.locales.tr("Character"),
    share.locales.tr("Numeric"),
    share.locales.tr("Float"),
    share.locales.tr("Integer"),
    share.locales.tr("Date"),
    share.locales.tr("DateTime"),
    share.locales.tr("Logical"),
    share.locales.tr("Memo"),
]

def _guess_mime(path: str) -> bytes:
    mt, _ = mimetypes.guess_type(path)
    if not mt:
        # sinnvolle Defaults
        if path.lower().endswith(".html") or path.lower().endswith(".htm"):
            mt = "text/html"
        elif path.lower().endswith(".css"):
            mt = "text/css"
        elif path.lower().endswith(".js"):
            mt = "application/javascript"
        else:
            mt = "application/octet-stream"
    return mt.encode("ascii")

class FontTriangleArrowsStyle(QProxyStyle):
    def __init__(self, base_style=None, color="#d7b300", font_family=None):
        super().__init__(base_style)
        self.col = QColor(color)
        self.font_family = "Arial" #font_family  # z.B. "Segoe UI Symbol" (Windows), sonst None

    def _draw_triangle(self, painter: QPainter, rect, direction: Qt.ArrowType):
        glyph = {
            Qt.UpArrow   : "▲",
            Qt.DownArrow : "▼",
            Qt.LeftArrow : "◀",
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
        

def open_helpwindow(mdi_area, mw: 'QMainWindow'):
    # wichtig: nicht als eigenes Top-Level laufen
    mw.setWindowFlags(Qt.Widget)
    mw.setParent(mdi_area)
    
    mode = "dark" if share.common.AppMode.dark else "light"
    lang = "de"   if share.common.AppMode.lang else "en"
    
    # mw.open_from_args(f"./dBaseHelp_{mode}_{lang}.chm", "index.html")
    mw.open_from_args("hlp/help.chm", None)

    sub = QMdiSubWindow()
    sub.setWidget(mw)
    sub.setAttribute(Qt.WA_DeleteOnClose, True)

    mdi_area.addSubWindow(sub)
    sub.resize(mw.sizeHint())
    sub.show()
    return sub

def _global_shortcut_focus_widget(obj: Any):
    try:
        if isinstance(obj, QWidget):
            return obj
    except Exception:
        pass
    try:
        return QApplication.focusWidget()
    except Exception:
        return None


def _find_host_by_class_name(widget: Any, class_names: set[str]):
    w = widget
    while w is not None:
        try:
            if w.__class__.__name__ in class_names:
                return w
        except Exception:
            pass
        try:
            w = w.parentWidget()
        except Exception:
            try:
                w = w.parent()
            except Exception:
                w = None
    return None


def _resolve_global_shortcut_host(obj: Any):
    focus = _global_shortcut_focus_widget(obj)
    return _find_host_by_class_name(
        focus,
        {
            "FileEditorWindow",
            "TableDesignerDialog",
            "TableRecordEditorDialog",
            "SqlBuilderWindow",
            "RegieCenter",
            "MainWindow",
        },
    )


def _dispatch_global_open(obj: Any) -> bool:
    host = _resolve_global_shortcut_host(obj)
    if host is None:
        return False
    name = host.__class__.__name__
    try:
        if name == "FileEditorWindow" and hasattr(host, "file_open"):
            host.file_open()
            return True
        if name == "TableDesignerDialog" and hasattr(host, "_action_open"):
            host._action_open()
            return True
        if name == "SqlBuilderWindow" and hasattr(host, "load_builder"):
            host.load_builder()
            return True
        if name in ("RegieCenter", "MainWindow"):
            mw = globals().get("MAINAPP", None)
            if mw is not None and hasattr(mw, "on_action_file_open"):
                mw.on_action_file_open()
                return True
    except Exception:
        return False
    return False


def _dispatch_global_save(obj: Any) -> bool:
    host = _resolve_global_shortcut_host(obj)
    if host is None:
        return False
    name = host.__class__.__name__
    try:
        if name == "FileEditorWindow" and hasattr(host, "file_save"):
            host.file_save()
            return True
        if name == "TableDesignerDialog" and hasattr(host, "_action_save"):
            host._action_save()
            return True
        if name == "TableRecordEditorDialog" and hasattr(host, "_action_save"):
            host._action_save()
            return True
        if name == "SqlBuilderWindow" and hasattr(host, "save_builder"):
            host.save_builder()
            return True
    except Exception:
        return False
    return False


class F1Filter(QObject):
    def __init__(self, mdi_area, create_help_mw, parent=None):
        super().__init__(parent)
        self.mdi_area       = mdi_area
        self.create_help_mw = create_help_mw
        self._help_sub      = None  # optional: merken, damit wir nicht 100 Fenster öffnen

    def eventFilter(self, obj, event):
        try:
            et = event.type()
        except Exception:
            return super().eventFilter(obj, event)

        # Ctrl+O / Ctrl+S global und kontextabhaengig
        try:
            if et in (QEvent.ShortcutOverride, QEvent.KeyPress):
                mods = event.modifiers()
                ctrl_only = bool(mods & Qt.ControlModifier) and not bool(mods & (Qt.AltModifier | Qt.MetaModifier))
                if ctrl_only and event.key() in (Qt.Key_O, Qt.Key_S):
                    handled = False
                    if event.key() == Qt.Key_O:
                        handled = _dispatch_global_open(obj)
                    elif event.key() == Qt.Key_S:
                        handled = _dispatch_global_save(obj)
                    if handled:
                        try:
                            event.accept()
                        except Exception:
                            pass
                        return True
        except Exception:
            pass

        if et == QEvent.KeyPress and event.key() == Qt.Key_F1:
            debug_print("F1 global abgefangen")
            # optional: wenn schon offen, nur nach vorne holen
            if self._help_sub is not None and not self._help_sub.isHidden():
                self.mdi_area.setActiveSubWindow(self._help_sub)
                self._help_sub.showNormal()
                self._help_sub.raise_()
                return True

            help_mw = self.create_help_mw()   # erzeugt ein QMainWindow (oder QWidget im QMainWindow)
            self._help_sub = open_helpwindow(self.mdi_area, help_mw)
            self._help_sub.dark_mode = True

            # wenn User schließt: Referenz leeren
            self._help_sub.destroyed.connect(lambda *_: setattr(self, "_help_sub", None))
            return True

        if et == QEvent.KeyPress and event.key() == Qt.Key_F2:
            pass

        return super().eventFilter(obj, event)


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

# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# parser stuff ...
# ---------------------------------------------------------------------------
# Tab 'Quell-Aliases' wie Screenshot, inkl. Add/Remove/Edit + nicht-nativer
# Folder-Dialog.
# model: dict[str, str]  (alias -> path)
# ---------------------------------------------------------------------------        
class SourceAliasesTab(QWidget):
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)

        self._model = dict(initial or {})
        self._updating_ui = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---- Oben: Liste ----
        gb_list = QGroupBox(share.locales.tr("Definierte Quell-Aliases"), self)
        v_list = QVBoxLayout(gb_list)

        self.lst = QListWidget()
        self.lst.setMinimumHeight(210)
        v_list.addWidget(self.lst)

        # ---- Unten: Editor ----
        gb_edit = QGroupBox(share.locales.tr("Quell-Alias bearbeiten"), self)
        e = QGridLayout(gb_edit)
        e.setHorizontalSpacing(10)
        e.setVerticalSpacing(8)

        e.addWidget(QLabel(share.locales.tr("Alias:")), 0, 0)
        self.ed_alias = QLineEdit()
        self.ed_alias.setMinimumWidth(220)
        e.addWidget(self.ed_alias, 0, 1)

        self.btn_add = QPushButton(share.locales.tr("Hinzufügen"))
        self.btn_remove = QPushButton(share.locales.tr("Entfernen"))
        self.btn_add.setFixedWidth(95)
        self.btn_remove.setFixedWidth(95)
        e.addWidget(self.btn_add, 0, 2)
        e.addWidget(self.btn_remove, 0, 3)

        e.addWidget(QLabel(share.locales.tr("Pfad:")), 1, 0)
        self.ed_path = QLineEdit()
        e.addWidget(self.ed_path, 1, 1, 1, 2)

        self.btn_browse = QPushButton("...")
        self.btn_browse.setFixedWidth(30)
        e.addWidget(self.btn_browse, 1, 3, alignment=Qt.AlignLeft)

        root.addWidget(gb_list)
        root.addWidget(gb_edit)
        root.addStretch(1)

        # Demo / initial
        if not self._model:
            self._model.update({
                "CoreShared": r"T:\Programme\dBASE\dBASE2019\Bin\dBLCore\Shared",
                "dBStartup" : r"T:\Programme\dBASE\dBASE2019\Bin\dBStartup",
                "Examples"  : r"T:\Programme\dBASE\dBASE2019\Examples",
                "Forms"     : r"T:\Programme\dBASE\dBASE2019\Forms",
                "Images"    : r"T:\Programme\dBASE\dBASE2019\Images",
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
    # ---------------------------------------------------------------------------
    # Gibt eine Kopie des Modells zurück.
    # ---------------------------------------------------------------------------
    def model(self) -> dict:
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
            QMessageBox.warning(self,
                share.locales.tr("Fehler"),
                share.locales.tr("Bitte einen Alias-Namen eingeben."))
            self.ed_alias.setFocus()
            return

        if not path:
            QMessageBox.warning(self,
                share.locales.tr("Fehler"),
                share.locales.tr("Bitte einen Pfad eingeben oder auswählen."))
            self.ed_path.setFocus()
            return

        if alias in self._model:
            r = QMessageBox.question(
                self,
                share.locales.tr("alias already exists"),
                f"{share.locales.tr('The alias')} '{alias}' {share.locales.tr('already exists')}.\n{share.locales.tr(alias_overwrite)}",
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
            share.locales.tr("Remove"),
                f"Alias '{alias}' {share.locales.tr('are you sure, to delete?')}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if r != QMessageBox.Yes:
            return

        self._model.pop(alias, None)
        self._reload_list(select_first=True)

    def _on_browse(self):
        start_dir = (self.ed_path.text() or "").strip() or ""
        dlg = QFileDialog(self, share.locales.tr("Choose path"), start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # <- NICHT NATIV

        if dlg.exec_():
            dirs = dlg.selectedFiles()
            if dirs:
                self.ed_path.setText(dirs[0])

    # ---------------------------------------------------------------------------
    # Optional: wenn ein bestehender Alias ausgewählt ist,
    # sollen Änderungen an Pfad/Alias (vorsichtig) ins Modell übernommen werden.
    # ---------------------------------------------------------------------------
    def _on_edit_finished(self):
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
            QMessageBox.warning(self, share.locales.tr("Error"), f"Alias '{new_alias}' " + share.locales.tr("already exists."))
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
    def __init__(self, type_column: int, parent=None):
        super().__init__(parent)
        self.type_column = type_column

    def createEditor(self, parent, option, index):
        if index.column() != self.type_column:
            return super().createEditor(parent, option, index)

        cb = QComboBox(parent)
        # Requested: force font
        try:
            cb.setFont(QFont("Arial", 10))
        except Exception:
            pass
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

class IndexComboDelegate(QStyledItemDelegate):
    VALUES = [  share.locales.tr("kein"),
                share.locales.tr("aufsteigend"),
                share.locales.tr("absteigend")]

    def __init__(self, index_column: int, parent=None):
        super().__init__(parent)
        self.index_column = index_column

    def createEditor(self, parent, option, index):
        if index.column() != self.index_column:
            return super().createEditor(parent, option, index)
        cb = QComboBox(parent)
        try:
            cb.setFont(QFont("Arial", 10))
        except Exception:
            pass
        cb.addItems(self.VALUES)
        cb.setEditable(False)
        return cb

    def setEditorData(self, editor, index):
        if index.column() != self.index_column or not isinstance(editor, QComboBox):
            return super().setEditorData(editor, index)
        current = (index.data(Qt.DisplayRole) or "").strip()
        i = editor.findText(current, Qt.MatchFixedString)
        editor.setCurrentIndex(i if i >= 0 else 0)

    def setModelData(self, editor, model, index):
        if index.column() != self.index_column or not isinstance(editor, QComboBox):
            return super().setModelData(editor, model, index)
        model.setData(index, editor.currentText(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class ReorderableStandardItemModel(QStandardItemModel):
    _MIME = "application/x-dbase-td-rows"

    def flags(self, index):
        f = super().flags(index)
        # ganze Row bewegen: Drag/Drop auf jedes Item erlauben
        if index.isValid():
            f |= Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
        else:
            f |= Qt.ItemIsDropEnabled
        return f

    def supportedDropActions(self):
        return Qt.MoveAction

    def mimeTypes(self):
        return [self._MIME]

    def mimeData(self, indexes):
        md = QMimeData()
        rows = sorted({i.row() for i in indexes if i.isValid()})
        if not rows:
            return md
        # wir unterstützen 1 Row Move (sonst wird's unübersichtlich)
        row = rows[0]
        ba = QByteArray()
        ds = QDataStream(ba, QIODevice.WriteOnly)
        ds.writeInt32(row)
        md.setData(self._MIME, ba)
        return md

    def dropMimeData(self, data, action, row, column, parent):
        if action != Qt.MoveAction:
            return False
        if not data or not data.hasFormat(self._MIME):
            return False

        ba = data.data(self._MIME)
        ds = QDataStream(ba, QIODevice.ReadOnly)
        src_row = ds.readInt32()
        if src_row < 0 or src_row >= self.rowCount():
            return False

        # Zielrow bestimmen
        if row < 0:
            row = parent.row() if parent.isValid() else self.rowCount()
        row = max(0, min(row, self.rowCount()))

        if row == src_row or row == src_row + 1:
            return False

        take = self.takeRow(src_row)
        if row > src_row:
            row -= 1
        self.insertRow(row, take)
        return True

# ---------------------------------------------------------------------------
# Markiert Widget/Subwindow dafuer, dass ESC das gesamte Fenster schliesst.
# ---------------------------------------------------------------------------
def mark_escape_close(obj: Any) -> Any:
    try:
        if obj is not None and hasattr(obj, "setProperty"):
            try:
                obj.setProperty("ESCAPE_BLOCKED", False)
            except Exception:
                pass
            obj.setProperty("ESCAPE_CLOSE", True)
    except Exception:
        pass
    return obj
    
class TableRecordEditorDialog(QDialog):
    def __init__(self, main_window: "MainWindow", dbf_path: str, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        mark_escape_close(self)
        self.current_path = dbf_path or ""
        self._modified = False
        self._updating = False
        self._subwindow = None

        self.setModal(False)
        self.setWindowModality(Qt.NonModal)

        lay = QVBoxLayout(self)

        # Sidebar + table
        self.table = QTableView(self)
        self.model = QStandardItemModel(0, 0, self.table)

        # Row indicator (►) in the vertical header, like in TableDesigner
        self.proxy = RowMarkerProxy(self.model, self.table)
        self.table.setModel(self.proxy)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setFixedWidth(24)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        try:
            self.table.verticalHeader().setFont(QFont("Arial", 14))
        except Exception:
            pass

        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.SelectedClicked |
            QAbstractItemView.EditKeyPressed
        )

        # keep indicator in sync with selection
        try:
            self.table.selectionModel().currentChanged.connect(self._on_current_changed)
        except Exception:
            pass

        # Robust fallback for the top-left corner (styles sometimes keep it white)
        self._ensure_corner_overlay()

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)


        self.side_bar = QWidget(self)
        self.side_bar.setObjectName("TableRecordEditorSideBar")
        sb_lay = QVBoxLayout(self.side_bar)
        sb_lay.setContentsMargins(1, 1, 1, 1)
        sb_lay.setSpacing(6)

        def _mk(std_icon, tip):
            b = QToolButton(self.side_bar)
            try:
                b.setIcon(self.style().standardIcon(std_icon))
            except Exception:
                pass
            b.setToolTip(tip)
            b.setAutoRaise(True)
            b.setIconSize (QSize(36, 36))
            b.setFixedSize(QSize(42, 42))
            return b

        self.btn_new  = _mk(QStyle.SP_FileIcon, "Neuer Record")
        self.btn_del  = _mk(QStyle.SP_DialogDiscardButton, "Record löschen")
        self.btn_save = _mk(QStyle.SP_DialogSaveButton, "Speichern")

        self.btn_new.clicked.connect(self._action_new_record)
        self.btn_del.clicked.connect(self._action_delete_record)
        self.btn_save.clicked.connect(self._action_save)

        sb_lay.addWidget(self.btn_new)
        sb_lay.addWidget(self.btn_del)
        sb_lay.addSpacing(8)
        sb_lay.addWidget(self.btn_save)
        sb_lay.addStretch(1)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        row.addWidget(self.side_bar, 0, Qt.AlignTop)
        row.addWidget(self.table, 1)
        lay.addLayout(row)

        self.resize(780, 460)

        self.fields: List[DbfFieldSpec] = []
        self.header_len = 0
        self.record_len = 0
        self.version = 0x03
        self._load_dbf(self.current_path)

        # track modifications
        try:
            self.model.dataChanged.connect(self._on_model_changed)
            self.model.rowsInserted.connect(self._on_model_changed)
            self.model.rowsRemoved.connect(self._on_model_changed)
        except Exception:
            pass

    def closeEvent(self, event):
        if not self._maybe_save_changes():
            event.ignore()
            return
        event.accept()

    def _on_model_changed(self, *_):
        if self._updating:
            return
        self._modified = True
        self._update_title()

    def _update_title(self):
        base = os.path.basename(self.current_path) if self.current_path else "Unbenannt.dbf"
        star = " *" if self._modified else ""
        self.setWindowTitle(f"{base}{star} - Bearbeiten")

    # --- row indicator helpers ---
    def _on_current_changed(self, current, previous):
        try:
            if current.isValid():
                self.proxy.setCurrentRow(current.row())
            else:
                self.proxy.setCurrentRow(-1)
        except Exception:
            pass

    def _select_row(self, row: int):
        if row < 0 or row >= self.model.rowCount():
            try:
                self.proxy.setCurrentRow(-1)
            except Exception:
                pass
            return
        try:
            pidx = self.proxy.index(row, 0)
            self.table.setCurrentIndex(pidx)
            self.table.selectRow(row)
            self.proxy.setCurrentRow(row)
        except Exception:
            try:
                self.table.selectRow(row)
            except Exception:
                pass

    # ---------------------------------------------------------------------------
    # Make sure an open editor widget commits its value into the model before saving.
    # ---------------------------------------------------------------------------
    def _commit_pending_edit(self):
        try:
            # clear focus from an editor widget -> triggers commitData/closeEditor
            self.table.clearFocus()
            self.table.setFocus(Qt.OtherFocusReason)
        except Exception:
            pass

    # ---------------------------------------------------------------------------
    # Robust fallback to paint the top-left header corner black (some styles
    # ignore QTableCornerButton::section).
    # ---------------------------------------------------------------------------
    def _ensure_corner_overlay(self):
        if getattr(self, "_corner_overlay", None) is not None:
            return
        self._corner_overlay = QLabel(self.table)
        self._corner_overlay.setObjectName("TableCornerOverlay")
        self._corner_overlay.setText("")
        self._corner_overlay.setStyleSheet("""
QLabel#TableCornerOverlay{
	background:#000000;
	color: white;
	border-right:1px solid #333333;
	border-bottom:1px solid #333333;
}""")
        self._corner_overlay.hide()
        self._corner_overlay.raise_()

        def _reposition():
            try:
                w = self.table.verticalHeader().width()
                h = self.table.horizontalHeader().height()
                if w <= 0 or h <= 0:
                    self._corner_overlay.hide()
                    return
                self._corner_overlay.setGeometry(QRect(0, 0, w, h))
                self._corner_overlay.show()
                self._corner_overlay.raise_()
            except Exception:
                pass

        QTimer.singleShot(0, _reposition)
        try:
            self.table.horizontalHeader().geometriesChanged.connect(_reposition)
            self.table.verticalHeader().geometriesChanged.connect(_reposition)
        except Exception:
            pass

    # ---------------- DBF I/O ----------------
    def _read_dbf_header(self, path: str):
        with open(path, "rb") as f:
            hdr = f.read(32)
            if len(hdr) < 32:
                raise ValueError(share.locales.tr("DBF header too short"))
            self.version = hdr[0]
            num_records = int.from_bytes(hdr[4:8], "little")
            self.header_len = int.from_bytes(hdr[8:10], "little")
            self.record_len = int.from_bytes(hdr[10:12], "little")

            # field descriptors
            f.seek(32)
            desc = f.read(max(0, self.header_len - 32))
            end = desc.find(b"\x0D")
            if end == -1:
                end = len(desc)
            desc = desc[:end]

            fields: List[DbfFieldSpec] = []
            offset = 1  # deletion flag
            for i in range(0, len(desc), 32):
                ch = desc[i:i+32]
                if len(ch) < 32:
                    break
                name_raw = ch[0:11].split(b"\x00", 1)[0]
                name = name_raw.decode("ascii", errors="ignore").strip()
                if not name:
                    continue
                ftype = chr(ch[11]).upper()
                flen = int(ch[16])
                fdec = int(ch[17])
                fields.append(DbfFieldSpec(name=name, ftype=ftype, length=flen, decimals=fdec, offset=offset))
                offset += flen

            return num_records, fields

    def _decode_field(self, spec: DbfFieldSpec, raw: bytes) -> Any:
        s = raw.decode("cp1252", errors="ignore")
        if spec.ftype in ("C", "M"):
            return s.rstrip()
        if spec.ftype in ("N", "F", "I"):
            return s.strip()
        if spec.ftype == "L":
            v = s.strip().upper()
            return True if v in ("T", "Y", "1") else False
        if spec.ftype == "D":
            v = s.strip()
            return v
        if spec.ftype == "T":
            return s.strip()
        return s.rstrip()

    def _encode_field(self, spec: DbfFieldSpec, value: Any) -> bytes:
        # returns exactly spec.length bytes
        if spec.ftype in ("C", "M"):
            txt = str(value or "")
            b = txt.encode("cp1252", errors="replace")[:spec.length]
            return b.ljust(spec.length, b" ")
        if spec.ftype in ("N", "F", "I"):
            txt = str(value or "").strip().replace(",", ".")
            # right-justify numeric
            b = txt.encode("ascii", errors="ignore")[:spec.length]
            return b.rjust(spec.length, b" ")
        if spec.ftype == "L":
            v = value
            if isinstance(v, str):
                vv = v.strip().upper()
                v = True if vv in ("1", "T", "Y", "TRUE") else False
            ch = b"T" if bool(v) else b"F"
            return ch.ljust(spec.length, b" ")
        if spec.ftype == "D":
            txt = str(value or "").strip()
            # expect YYYYMMDD
            b = txt.encode("ascii", errors="ignore")[:spec.length]
            return b.ljust(spec.length, b" ")
        # fallback
        txt = str(value or "")
        b = txt.encode("cp1252", errors="replace")[:spec.length]
        return b.ljust(spec.length, b" ")

    def _load_dbf(self, path: str):
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Fehler", "Keine DBF-Datei zum Bearbeiten vorhanden.")
            return

        try:
            num_records, fields = self._read_dbf_header(path)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"DBF konnte nicht gelesen werden:\n{e}")
            return

        self.fields = fields
        self._updating = True
        try:
            self.model.clear()
            self.model.setColumnCount(len(fields))
            self.model.setHorizontalHeaderLabels([f.name for f in fields])

            # set delegates per column
            for c, spec in enumerate(fields):
                if spec.ftype == "L":
                    self.table.setItemDelegateForColumn(c, LogicalCheckDelegate(self.table))
                elif spec.ftype in ("N", "F", "I"):
                    self.table.setItemDelegateForColumn(c, NumericLenDelegate(spec.length, spec.decimals, self.table))
                else:
                    self.table.setItemDelegateForColumn(c, FixedLenTextDelegate(spec.length, self.table))

            # read records
            with open(path, "rb") as f:
                f.seek(self.header_len)
                for r in range(num_records):
                    rec = f.read(self.record_len)
                    if len(rec) < self.record_len:
                        break
                    if rec[:1] == b"*":
                        continue  # deleted
                    items: List[QStandardItem] = []
                    for spec in fields:
                        raw = rec[spec.offset:spec.offset + spec.length]
                        val = self._decode_field(spec, raw)
                        it = QStandardItem()
                        if spec.ftype == "L":
                            it.setData(bool(val), Qt.EditRole)
                            it.setData("1" if bool(val) else "0", Qt.DisplayRole)
                        else:
                            it.setData(str(val), Qt.EditRole)
                            it.setData(str(val), Qt.DisplayRole)
                        items.append(it)
                    self.model.appendRow(items)

            self._modified = False
            self._update_title()
            if self.model.rowCount() > 0:
                self._select_row(0)
        finally:
            self._updating = False

    def _save_dbf(self, path: str) -> bool:
        self._last_save_error = ""
        try:
            # Build header
            nfields = len(self.fields)
            header_len = 32 + 32 * nfields + 1
            record_len = 1 + sum(f.length for f in self.fields)

            today = datetime.date.today()
            num_records = self.model.rowCount()

            hdr = bytearray(32)
            hdr[0] = self.version if self.version else 0x03
            hdr[1] = today.year - 1900
            hdr[2] = today.month
            hdr[3] = today.day
            hdr[4:8] = int(num_records).to_bytes(4, "little", signed=False)
            hdr[8:10] = int(header_len).to_bytes(2, "little", signed=False)
            hdr[10:12] = int(record_len).to_bytes(2, "little", signed=False)

            out = bytearray()
            out += hdr

            # field descriptors
            for spec in self.fields:
                desc = bytearray(32)
                nb = spec.name.encode("ascii", errors="ignore")[:11]
                desc[0:len(nb)] = nb
                desc[11] = ord(spec.ftype[:1])
                desc[16] = int(spec.length) & 0xFF
                desc[17] = int(spec.decimals) & 0xFF
                out += desc
            out += b"\x0D"

            # records
            for r in range(self.model.rowCount()):
                rec = bytearray()
                rec += b" "  # not deleted
                for c, spec in enumerate(self.fields):
                    v = self.model.item(r, c)
                    if v is None:
                        val = ""
                    else:
                        # Logical: prefer EditRole boolean
                        val = v.data(Qt.EditRole)
                    rec += self._encode_field(spec, val)
                # enforce record length
                if len(rec) < record_len:
                    rec += b" " * (record_len - len(rec))
                out += rec[:record_len]

            out += b"\x1A"

            # Write atomically: temp file -> replace
            folder = os.path.dirname(path) or "."
            fd, tmp_path = tempfile.mkstemp(prefix="dbf_save_", suffix=".tmp", dir=folder)
            try:
                with os.fdopen(fd, "wb") as f:
                    f.write(out)
                os.replace(tmp_path, path)
            finally:
                try:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except Exception:
                    pass
            return True
        except Exception as e:
            try:
                self._last_save_error = traceback.format_exc()
            except Exception:
                self._last_save_error = str(e)
            return False

    # ---------------- actions ----------------
    def _maybe_save_changes(self) -> bool:
        if not self._modified:
            return True
        r = QMessageBox.question(
            self,
            "Änderungen speichern?",
            "Es gibt ungespeicherte Änderungen.\nSollen diese gespeichert werden?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes,
        )
        if r == QMessageBox.Cancel:
            return False
        if r == QMessageBox.Yes:
            self._action_save()
            return not self._modified
        return True

    def _open_help(self):
        try:
            if hasattr(self.main_window, "mdi") and hasattr(self.main_window, "help_mainwindow"):
                open_helpwindow(self.main_window.mdi, self.main_window.help_mainwindow)
                return
        except Exception:
            pass
        QMessageBox.information(self, "Hilfe", "Keine Hilfe verfügbar.")

    def _action_new_record(self):
        items = []
        for spec in self.fields:
            it = QStandardItem()
            if spec.ftype == "L":
                it.setData(False, Qt.EditRole)
                it.setData("0", Qt.DisplayRole)
            else:
                it.setData("", Qt.EditRole)
                it.setData("", Qt.DisplayRole)
            items.append(it)
        self.model.appendRow(items)
        r = self.model.rowCount() - 1
        if r >= 0:
            self._select_row(r)
        self._modified = True
        self._update_title()

    def _action_delete_record(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return
        r = idx.row()
        self.model.removeRow(r)
        self._modified = True
        self._update_title()
        if self.model.rowCount() > 0:
            self._select_row(min(r, self.model.rowCount() - 1))

    def _action_copy_record(self):
        idx = self.table.currentIndex()
        if not idx.isValid():
            return
        r = idx.row()
        vals = []
        for c, spec in enumerate(self.fields):
            it = self.model.item(r, c)
            if spec.ftype == "L":
                vals.append("1" if bool(it.data(Qt.EditRole)) else "0")
            else:
                vals.append(str(it.data(Qt.EditRole) or ""))
        QApplication.clipboard().setText("\t".join(vals))

    def _action_paste_record(self):
        txt = QApplication.clipboard().text() or ""
        parts = txt.split("\t")
        if not parts or not self.fields:
            return
        # insert after current row
        idx = self.table.currentIndex()
        insert_at = idx.row() + 1 if idx.isValid() else self.model.rowCount()
        self.model.insertRow(insert_at)
        for c, spec in enumerate(self.fields):
            it = self.model.item(insert_at, c)
            if it is None:
                it = QStandardItem()
                self.model.setItem(insert_at, c, it)
            v = parts[c] if c < len(parts) else ""
            if spec.ftype == "L":
                vv = str(v).strip().upper()
                b = True if vv in ("1", "T", "Y", "TRUE") else False
                it.setData(b, Qt.EditRole)
                it.setData("1" if b else "0", Qt.DisplayRole)
            else:
                it.setData(v, Qt.EditRole)
                it.setData(v, Qt.DisplayRole)
        self._select_row(insert_at)
        self._modified = True
        self._update_title()

    def _action_cut_record(self):
        self._action_copy_record()
        self._action_delete_record()

    def _action_save(self):
        self._commit_pending_edit()
        if not self.current_path:
            return self._action_save_as()
        if os.path.exists(self.current_path):
            r = QMessageBox.question(
                self,
                "Überschreiben?",
                f"Datei existiert bereits:\n{self.current_path}\n\nÜberschreiben?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if r != QMessageBox.Yes:
                return
        if self._save_dbf(self.current_path):
            self._modified = False
            self._update_title()
        else:
            msg = "Konnte die DBF-Datei nicht speichern."
            if getattr(self, "_last_save_error", ""):
                msg += "\n\nDetails:\n" + self._last_save_error
            QMessageBox.critical(self, "Fehler", msg)

    def _action_save_as(self):
        self._commit_pending_edit()
        dlg = QFileDialog(self, "Speichern unter")
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDefaultSuffix("dbf")
        dlg.setNameFilters(["dBase Tabellen (*.dbf)", "Alle Dateien (*.*)"])
        if self.current_path:
            try:
                dlg.selectFile(self.current_path)
            except Exception:
                pass
        if not dlg.exec_():
            return
        files = dlg.selectedFiles()
        if not files:
            return
        path = files[0]
        if os.path.exists(path):
            r = QMessageBox.question(
                self,
                "Überschreiben?",
                f"Datei existiert bereits:\n{path}\n\nÜberschreiben?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if r != QMessageBox.Yes:
                return
        if self._save_dbf(path):
            self.current_path = path
            self._modified = False
            self._update_title()
        else:
            QMessageBox.critical(self, "Fehler", "Konnte die DBF-Datei nicht speichern.")

    def _action_design_mode(self):
        # open TableDesigner and close this dialog
        try:
            designer = TableDesignerDialog(self.main_window)
            # load schema
            designer._clear_rows()
            if designer._load_dbf_schema(self.current_path):
                designer.current_path = self.current_path
                designer._set_modified(False)
            sub = self.main_window.mdi.addSubWindow(designer)
            designer.setSubWindow(sub)
            sub.setWindowTitle(f"Table Designer - {os.path.basename(self.current_path)}")
            sub.resize(640, 340)
            sub.move(240, 60)
            designer.show()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Design-Modus nicht öffnen:\n{e}")
            return
        try:
            if self._subwindow is not None:
                self._subwindow.close()
        except Exception:
            pass
        try:
            self.close()
        except Exception:
            pass

    # ---------------- context menu ----------------
    def _show_context_menu(self, pos):
        menu = QMenu(self)

        act_help = QAction(share.locales.tr("Hilfe\tF1"), self)
        act_help.setShortcut(QKeySequence("F1"))
        menu.addAction(act_help)

        menu.addSeparator()

        act_new = QAction(share.locales.tr("Neuer Record"), self)
        menu.addAction(act_new)

        edit_menu = menu.addMenu(share.locales.tr("Edit"))
        act_copy  = QAction(share.locales.tr("Record Kopieren"), self)
        act_paste = QAction(share.locales.tr("Record Einfügen"), self)
        act_cut   = QAction(share.locales.tr("Ausschneiden"   ), self)
        
        edit_menu.addAction(act_copy)
        edit_menu.addAction(act_paste)
        edit_menu.addAction(act_cut)

        act_del = QAction(share.locales.tr("Record löschen"), self)
        menu.addAction(act_del)

        menu.addSeparator()

        act_save    = QAction(share.locales.tr("Speichern"), self)
        act_save_as = QAction(share.locales.tr("Speichern unter..."), self)
        menu.addAction(act_save)
        menu.addAction(act_save_as)

        menu.addSeparator()

        act_design = QAction(share.locales.tr("Design Modus"), self)
        act_close  = QAction(share.locales.tr("Schließen"   ), self)
        menu.addAction(act_design)
        menu.addAction(act_close)

        has_row = self.model.rowCount() > 0 and self.table.currentIndex().isValid()
        act_copy.setEnabled(has_row)
        act_cut.setEnabled(has_row)
        act_del.setEnabled(has_row)

        chosen = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if chosen is None:
            return
        if chosen is act_help:
            self._open_help()
        elif chosen is act_new:
            self._action_new_record()
        elif chosen is act_copy:
            self._action_copy_record()
        elif chosen is act_paste:
            self._action_paste_record()
        elif chosen is act_cut:
            self._action_cut_record()
        elif chosen is act_del:
            self._action_delete_record()
        elif chosen is act_save:
            self._action_save()
        elif chosen is act_save_as:
            self._action_save_as()
        elif chosen is act_design:
            self._action_design_mode()
        elif chosen is act_close:
            self.close()

class FixedLenTextDelegate(QStyledItemDelegate):
    def __init__(self, max_len: int, parent=None):
        super().__init__(parent)
        self.max_len = max(1, int(max_len or 1))

    def createEditor(self, parent, option, index):
        ed = QLineEdit(parent)
        ed.setMaxLength(self.max_len)
        return ed

class NumericLenDelegate(QStyledItemDelegate):
    def __init__(self, max_len: int, decimals: int = 0, parent=None):
        super().__init__(parent)
        self.max_len = max(1, int(max_len or 1))
        self.decimals = max(0, int(decimals or 0))

        # allow: optional sign, digits, optional decimal part
        # keep it permissive; hard truncation is done on save.
        if self.decimals > 0:
            pat = r"^[+-]?[0-9]*([\\.,][0-9]{0,%d})?$" % self.decimals
        else:
            pat = r"^[+-]?[0-9]*$"
        try:
            self._re = QRegularExpression(pat)
            self._val = QRegularExpressionValidator(self._re)
        except Exception:
            self._val = None

    def createEditor(self, parent, option, index):
        ed = QLineEdit(parent)
        ed.setMaxLength(self.max_len)
        if self._val is not None:
            ed.setValidator(self._val)
        return ed

# ---------------------------------------------------------------------------
# Displays/edits logical field as checkbox.
# ---------------------------------------------------------------------------
class LogicalCheckDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        cb = QCheckBox(parent)
        cb.setTristate(False)
        return cb

    def setEditorData(self, editor, index):
        if isinstance(editor, QCheckBox):
            v = index.data(Qt.EditRole)
            # accept 0/1, True/False, 'T'/'F', 'Y'/'N'
            s = str(v).strip().upper()
            checked = False
            if v is True or s in ("1", "T", "Y", "TRUE"):
                checked = True
            editor.setChecked(checked)
            return
        super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QCheckBox):
            model.setData(index, bool(editor.isChecked()), Qt.EditRole)
            # display as 1/0 like many dBase tools
            model.setData(index, "1" if editor.isChecked() else "0", Qt.DisplayRole)
            return
        super().setModelData(editor, model, index)

class TableDesignerDialog(QDialog):
    def __init__(self, main_window: "MainWindow", parent=None):
        super().__init__(parent)
        self.main_window = main_window
        mark_escape_close(self)
        self.parent      = parent
        self.subwindow   = None

        # current file path (may be empty)
        self.current_path = ""
        self._modified = False
        self._updating = False  # guard while loading

        self.setModal(False)
        self.setWindowModality(Qt.NonModal)

        layout = QVBoxLayout(self)

        self.table = QTableView(self)
        # Use a model that supports InternalMove (drag&drop row reorder) if possible
        try:
            self.model = ReorderableStandardItemModel(0, 6, self.table)
        except Exception:
            self.model = QStandardItemModel(0, 6, self.table)

        self.proxy = RowMarkerProxy(self.model, self.table)
        self.table.setModel(self.proxy)

        self.model.setHorizontalHeaderLabels(["Field", "Name", "Type", "Width", "Decimal", "Index"])

        self.table.setEditTriggers(
            QAbstractItemView.DoubleClicked |
            QAbstractItemView.SelectedClicked |
            QAbstractItemView.EditKeyPressed
        )

        # Delegate auf Spalten
        self.table.setItemDelegateForColumn(4, IntOnlyDelegate(self.table, min_value=0, max_value=512))
        self.table.setItemDelegateForColumn(3, IntOnlyDelegate(self.table, min_value=0, max_value=512))
        self.table.setItemDelegateForColumn(2, TypeComboDelegate(2, self.table))
        self.table.setItemDelegateForColumn(5, IndexComboDelegate(5, self.table))
        self.table.setItemDelegateForColumn(1, UpperNoSpaceDelegate(self.table, force_upper=True))

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setFixedWidth(24)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

        try:
            vm = self.table.verticalHeader()
            vm.setFont(QFont("Arial", 14))
        except Exception:
            pass

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)

        self.table.setColumnWidth(0, 55)
        self.table.setColumnWidth(1, 160)
        self.table.setColumnWidth(2, 130)
        self.table.setColumnWidth(3, 70)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 120)

        self.overlay = QLabel(self.table)
        self.overlay.setText("")
        self.overlay.move(0,0)
        self.overlay.resize(42,42)
        self.overlay.setStyleSheet(f"""
            QLabel {{
                background: #000000;
                color: #ffff00;
                border-right: 1px solid #000000;
                border-bottom: 1px solid #000000;
            }}
        """)
        self.overlay.raise_()
        def reposition():
            w = self.table.verticalHeader  ().width ()
            h = self.table.horizontalHeader().height()
            if w <= 0 or h <= 0:
                self.overlay.hide()
                return
            self.overlay.setGeometry(QRect(0, 0, w, h))
            self.overlay.show()
            self.overlay.raise_()
        
        # Erst nach Layout positionieren
        QTimer.singleShot(0, reposition)
        
        # Enable row drag&drop reordering (best effort; Up/Down actions are the fallback)
        try:
            self.table.setDragEnabled(True)
            self.table.setAcceptDrops(True)
            self.table.setDropIndicatorShown(True)
            self.table.setDragDropMode(QAbstractItemView.InternalMove)
            self.table.setDefaultDropAction(Qt.MoveAction)
        except Exception:
            pass

        # Context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)

        
        # --- Left icon toolbar (row operations) ---
        self.side_bar = QWidget(self)
        self.side_bar.setObjectName("TableDesignerSideBar")
        side_layout = QVBoxLayout(self.side_bar)
        side_layout.setContentsMargins(1, 1, 1, 1)
        side_layout.setSpacing(6)

        def _mk_tool_btn(std_icon, tooltip):
            b = QToolButton(self.side_bar)
            try:
                b.setIcon(self.style().standardIcon(std_icon))
            except Exception:
                pass
            b.setToolTip(tooltip)
            b.setAutoRaise(True)
            b.setIconSize (QSize(36, 36))
            b.setFixedSize(QSize(42, 42))
            return b

        self.btn_move_up   = _mk_tool_btn(QStyle.SP_ArrowUp,             share.locales.tr("Move up"))
        self.btn_move_down = _mk_tool_btn(QStyle.SP_ArrowDown,           share.locales.tr("Move down"))
        self.btn_new_row   = _mk_tool_btn(QStyle.SP_FileIcon,            share.locales.tr("Neu (Zeile hinzufügen)"))
        self.btn_delete    = _mk_tool_btn(QStyle.SP_DialogDiscardButton, share.locales.tr("Löschen"))
        self.btn_save      = _mk_tool_btn(QStyle.SP_DialogSaveButton,    share.locales.tr("Speichern"))

        self.btn_move_up   . clicked.connect(lambda: self._action_move_row(-1))
        self.btn_move_down . clicked.connect(lambda: self._action_move_row(+1))
        self.btn_new_row   . clicked.connect(self._action_add_row)
        self.btn_delete    . clicked.connect(self._action_delete_row)
        self.btn_save      . clicked.connect(self._action_save)

        side_layout.addWidget(self.btn_move_up)
        side_layout.addWidget(self.btn_move_down)
        side_layout.addSpacing(8)
        side_layout.addWidget(self.btn_new_row)
        side_layout.addWidget(self.btn_delete)
        side_layout.addSpacing(8)
        side_layout.addWidget(self.btn_save)
        side_layout.addStretch(1)

        # Put side bar + table into a single horizontal row
        main_row = QHBoxLayout()
        main_row.setContentsMargins(0, 0, 0, 0)
        main_row.setSpacing(6)
        main_row.addWidget(self.side_bar, 0, Qt.AlignTop)
        main_row.addWidget(self.table, 1)

        layout.addLayout(main_row)

        self.resize(620, 320)

        # Demo / start state
        self._fill_demo_data()

        self.table.selectionModel().currentChanged.connect(self.on_current_changed)
        self.table.selectRow(0)
        self.proxy.setCurrentRow(0)

        # Modified tracking
        try:
            self.model.itemChanged.connect(self._on_item_changed)
        except Exception:
            pass
        # Some edits come through setData via the proxy/delegates; ensure we still mark modified.
        try:
            self.model.dataChanged.connect(self._on_any_model_change)
        except Exception:
            pass
        for sig in ("rowsInserted", "rowsRemoved", "rowsMoved", "columnsInserted", "columnsRemoved", "columnsMoved"):
            try:
                getattr(self.model, sig).connect(self._on_any_model_change)
            except Exception:
                pass

        self._update_window_title()
    
    def setSubWindow(self, parent):
        self.subwindow = parent

    def closeEvent(self, event):
        # ask to save changes before closing
        if not self._maybe_save_changes():
            event.ignore()
            return
        try:
            if self.subwindow is not None:
                self.subwindow.close()
        except Exception:
            pass
        try:
            if self.parent is not None:
                self.parent.close()
        except Exception:
            pass
        event.accept()

    # --------------------------
    # UI helpers
    # --------------------------
    def _update_window_title(self):
        base = os.path.basename(self.current_path) if self.current_path else "Unbenannt.dbf"
        star = " *" if self._modified else ""
        self.setWindowTitle(f"{base}{star} - Table Designer")

    def _set_modified(self, flag: bool):
        self._modified = bool(flag)
        self._update_window_title()

    def _on_item_changed(self, *_):
        if self._updating:
            return
        self._set_modified(True)

    def _on_any_model_change(self, *_):
        # catches dataChanged/rowsMoved/etc. (including updates via proxy/delegates)
        if self._updating:
            return
        self._set_modified(True)

    # ---------------------------------------------------------------------------
    # Enable/disable sidebar buttons based on current row and model state.
    # ---------------------------------------------------------------------------
    def _update_side_buttons(self):
        try:
            row = self._current_source_row()
            rc = self.model.rowCount()
            has_row = (rc > 0) and (row >= 0)
            self.btn_delete    . setEnabled(has_row)
            self.btn_move_up   . setEnabled(has_row and row > 0)
            self.btn_move_down . setEnabled(has_row and row < rc - 1)
            # Save is always allowed (will fall back to Save As if needed)
            self.btn_save.setEnabled(True)
        except Exception:
            pass

    # ---------------------------------------------------------------------------
    # Try to commit an active editor (e.g. ComboBox) so modifications are detected.
    # ---------------------------------------------------------------------------
    def _commit_pending_edit(self):
        try:
            if self.table.state() == QAbstractItemView.EditingState:
                fw = QApplication.focusWidget()
                try:
                    self.table.closeEditor(fw, QAbstractItemDelegate.SubmitModelCache)
                except Exception:
                    # fallback: toggling focus usually commits
                    self.table.clearFocus()
                    self.table.setFocus()
                QApplication.processEvents()
        except Exception:
            pass

    # Bei Reihenwechsel Marker mitwandern lassen
    def on_current_changed(self, current, previous):
        try:
            self.proxy.setCurrentRow(current.row())
        except Exception:
            pass

    def _current_source_row(self) -> int:
        idx = self.table.currentIndex()
        if not idx.isValid():
            return -1
        try:
            return self.proxy.mapToSource(idx).row()
        except Exception:
            return idx.row()

    def _select_source_row(self, row: int):
        if row < 0 or row >= self.model.rowCount():
            return
        try:
            pidx = self.proxy.mapFromSource(self.model.index(row, 0))
            self.table.setCurrentIndex(pidx)
            self.table.selectRow(pidx.row())
            self.proxy.setCurrentRow(pidx.row())
        except Exception:
            self.table.selectRow(row)
            self.proxy.setCurrentRow(row)

    # --------------------------
    # Context menu
    # --------------------------
    def _show_context_menu(self, pos):
        menu = QMenu(self)

        act_help = QAction(share.locales.tr("Hilfe\tF1"), self)
        act_help.setShortcut(QKeySequence("F1"))
        menu.addAction(act_help)

        act_edit = QAction(share.locales.tr("Bearbeiten"), self)
        menu.addAction(act_edit)

        # requested: separator after help, then Neu/Open
        menu.addSeparator()

        act_new  = QAction(share.locales.tr("Neu"), self)
        act_open = QAction(share.locales.tr("Öffnen..."), self)
        menu.addAction(act_new)
        menu.addAction(act_open)

        menu.addSeparator()

        act_add = QAction(share.locales.tr("Hinzufügen"), self)
        act_del = QAction(share.locales.tr("Löschen"   ), self)
        menu.addAction(act_add)
        menu.addAction(act_del)

        menu.addSeparator()

        act_save    = QAction(share.locales.tr("Speichern"), self)
        act_save_as = QAction(share.locales.tr("Speichern unter..."), self)
        menu.addAction(act_save)
        menu.addAction(act_save_as)

        menu.addSeparator()

        act_up   = QAction(share.locales.tr("Nach oben verschieben" ), self)
        act_down = QAction(share.locales.tr("Nach unten verschieben"), self)
        menu.addAction(act_up)
        menu.addAction(act_down)

        menu.addSeparator()

        act_close = QAction(share.locales.tr("Schließen"), self)
        menu.addAction(act_close)

        # enable/disable
        has_row = self.model.rowCount() > 0 and self._current_source_row() >= 0
        act_del .setEnabled(has_row)
        act_up  .setEnabled(has_row and self._current_source_row() > 0)
        act_down.setEnabled(has_row and self._current_source_row() < self.model.rowCount() - 1)
        act_save.setEnabled(bool(self.current_path))

        chosen = menu.exec_(self.table.viewport().mapToGlobal(pos))
        if chosen is None:
            return

        if chosen is act_help:
            self._open_help()
        elif chosen is act_edit:
            self._action_edit_records()
        elif chosen is act_new:
            self._action_new()
        elif chosen is act_open:
            self._action_open()
        elif chosen is act_add:
            self._action_add_row()
        elif chosen is act_del:
            self._action_delete_row()
        elif chosen is act_save:
            self._action_save()
        elif chosen is act_save_as:
            self._action_save_as()
        elif chosen is act_up:
            self._action_move_row(-1)
        elif chosen is act_down:
            self._action_move_row(+1)
        elif chosen is act_close:
            self.close()

    def _open_help(self):
        # Use existing help window API from this project
        try:
            # Many parts of this project use open_helpwindow(mdi_area, mw)
            if hasattr(self.main_window, "mdiArea") and hasattr(self.main_window, "help_mainwindow"):
                open_helpwindow(self.main_window.mdiArea(), self.main_window.help_mainwindow)
                return
        except Exception:
            pass
        try:
            # fallback: some projects have a method
            if hasattr(self.main_window, "open_help"):
                self.main_window.open_help()
                return
        except Exception:
            pass
        QMessageBox.information(self, "Hilfe", "Keine Hilfe verfügbar.")

    # --------------------------
    # Actions
    # --------------------------
    def _action_new(self):
        # "Neu" clears the designer visually, but keeps the current file path.
        # If there are unsaved changes, ask the user first.
        if not self._maybe_save_changes():
            return

        self._clear_rows()
        # user expectation: start with exactly one empty row
        self._insert_default_row(0)
        self._select_source_row(0)
        try:
            self.proxy.setCurrentRow(0)
        except Exception:
            pass
        self._set_modified(False)
        self._update_side_buttons()

    def _action_open(self):

        # Visual clear + load from file; ask to save changes first
        if not self._maybe_save_changes():
            return

        dlg = QFileDialog(self, "DBF öffnen")
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["dBase Tabellen (*.dbf)", "Alle Dateien (*.*)"])
        if self.current_path:
            try:
                dlg.selectFile(self.current_path)
            except Exception:
                pass
        if not dlg.exec_():
            return
        files = dlg.selectedFiles()
        if not files:
            return
        path = files[0]
        # Ensure the view is really empty before re-populating
        self._clear_rows()
        ok = self._load_dbf_schema(path)
        if ok:
            self.current_path = path
            self._set_modified(False)
            self._update_side_buttons()
        else:
            QMessageBox.warning(self, "Fehler", "Die DBF-Datei konnte nicht gelesen werden.")

    # ---------------------------------------------------------------------------
    # Switch to record-edit mode for the current DBF file.
    # ---------------------------------------------------------------------------
    def _action_edit_records(self):
        # Need a file on disk.
        if not self.current_path:
            # Ask user to save schema first
            r = QMessageBox.question(
                self,
                "Datei speichern?",
                "Zum Bearbeiten der Records muss eine DBF-Datei existieren.\n"
                "Soll die Tabelle zuerst gespeichert werden?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes,
            )
            if r != QMessageBox.Yes:
                return
            self._action_save_as()
            if not self.current_path:
                return

        # If schema modified, offer to save.
        if not self._maybe_save_changes():
            return

        try:
            dlg = TableRecordEditorDialog(self.main_window, self.current_path)
            sub = None
            try:
                sub = self.main_window.mdi.addSubWindow(dlg)
                mark_escape_close(sub)
            except Exception:
                sub = None
            if sub is not None:
                dlg._subwindow = sub
                sub.setWindowTitle(f"Bearbeiten - {os.path.basename(self.current_path)}")
                sub.resize(760, 460)
                sub.move(240, 60)
                dlg.show()
            else:
                dlg.show()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Bearbeiten-Modus nicht öffnen:\n{e}")
            return

        # Close designer window (only the designer, not the whole app)
        try:
            if self.subwindow is not None:
                self.subwindow.close()
        except Exception:
            pass
        try:
            self.close()
        except Exception:
            pass

    def _action_add_row(self):
        row = self._current_source_row()
        insert_at = (row + 1) if row >= 0 else self.model.rowCount()
        self._insert_default_row(insert_at)
        self._select_source_row(insert_at)
        self._set_modified(True)
        self._update_side_buttons()

    def _action_delete_row(self):
        row = self._current_source_row()
        if row < 0:
            return
        self.model.removeRow(row)
        # renumber Field column
        self._renumber_field_column()
        self._set_modified(True)
        self._select_source_row(min(row, self.model.rowCount() - 1))
        self._update_side_buttons()

    def _action_move_row(self, delta: int):
        row = self._current_source_row()
        if row < 0:
            return
        new_row = row + delta
        if new_row < 0 or new_row >= self.model.rowCount():
            return

        # move row in source model
        items = self.model.takeRow(row)
        self.model.insertRow(new_row, items)
        self._renumber_field_column()
        self._set_modified(True)
        self._select_source_row(new_row)
        self._update_side_buttons()

    def _action_save(self):
        if not self.current_path:
            return self._action_save_as()

        # overwrite confirmation
        if os.path.exists(self.current_path):
            r = QMessageBox.question(
                self,
                "Überschreiben?",
                f"Datei existiert bereits:\n{self.current_path}\n\nÜberschreiben?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if r != QMessageBox.Yes:
                return

        if self._save_dbf_schema(self.current_path):
            self._set_modified(False)
        else:
            QMessageBox.critical(self, "Fehler", "Konnte die DBF-Datei nicht speichern.")

    def _action_save_as(self):
        dlg = QFileDialog(self, "Speichern unter")
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDefaultSuffix("dbf")
        dlg.setNameFilters(["dBase Tabellen (*.dbf)", "Alle Dateien (*.*)"])
        if self.current_path:
            try:
                dlg.selectFile(self.current_path)
            except Exception:
                pass
        if not dlg.exec_():
            return
        files = dlg.selectedFiles()
        if not files:
            return
        path = files[0]

        # overwrite confirmation
        if os.path.exists(path):
            r = QMessageBox.question(
                self,
                "Überschreiben?",
                f"Datei existiert bereits:\n{path}\n\nÜberschreiben?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if r != QMessageBox.Yes:
                return

        if self._save_dbf_schema(path):
            self.current_path = path
            self._set_modified(False)
        else:
            QMessageBox.critical(self, "Fehler", "Konnte die DBF-Datei nicht speichern.")

    # --------------------------
    # Save / Load / Clear helpers
    # --------------------------
    def _clear_rows(self):
        self._updating = True
        try:
            # hard reset so proxy/view reliably refresh
            try:
                self.model.beginResetModel()
            except Exception:
                pass
            try:
                self.model.removeRows(0, self.model.rowCount())
            finally:
                try:
                    self.model.endResetModel()
                except Exception:
                    pass
            # reset row marker
            try:
                self.proxy.setCurrentRow(-1)
            except Exception:
                pass
        finally:
            self._updating = False

    def _insert_default_row(self, row: int):
        self._updating = True
        try:
            self.model.insertRow(row)
            # Field number
            self.model.setItem(row, 0, QStandardItem(str(row + 1)))
            self.model.setItem(row, 1, QStandardItem("FIELD"))
            self.model.setItem(row, 2, QStandardItem(share.locales.tr("Character")))
            self.model.setItem(row, 3, QStandardItem("10"))
            self.model.setItem(row, 4, QStandardItem("0"))
            self.model.setItem(row, 5, QStandardItem(share.locales.tr("kein")))
        finally:
            self._updating = False

    def _renumber_field_column(self):
        self._updating = True
        try:
            for r in range(self.model.rowCount()):
                it = self.model.item(r, 0)
                if it is None:
                    it = QStandardItem()
                    self.model.setItem(r, 0, it)
                it.setText(str(r + 1))
        finally:
            self._updating = False

    def _maybe_save_changes(self) -> bool:
        # commit current editor (e.g. Type ComboBox) so changes are detected
        self._commit_pending_edit()
        if not self._modified:
            return True
        r = QMessageBox.question(
            self,
            "Änderungen speichern?",
            "Es gibt ungespeicherte Änderungen.\nSollen diese gespeichert werden?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes
        )
        if r == QMessageBox.Cancel:
            return False
        if r == QMessageBox.Yes:
            # if no current_path -> Save As
            if self.current_path:
                self._action_save()
            else:
                self._action_save_as()
            # if still modified, assume save cancelled/failed
            return not self._modified
        return True

    def _type_char_to_label(self, t: str) -> str:
        t = (t or "").upper()[:1]
        mapping = {
            "C": share.locales.tr("Character"),
            "N": share.locales.tr("Numeric"),
            "F": share.locales.tr("Float"),
            "I": share.locales.tr("Integer"),
            "D": share.locales.tr("Date"),
            "T": share.locales.tr("DateTime"),
            "L": share.locales.tr("Logical"),
            "M": share.locales.tr("Memo"),
        }
        return mapping.get(t, share.locales.tr("Character"))

    def _type_label_to_char(self, label: str) -> str:
        # label is translated; match by TYPE_VALUES content
        lab = (label or "").strip()
        if lab == share.locales.tr("Character"):
            return "C"
        if lab == share.locales.tr("Numeric"):
            return "N"
        if lab == share.locales.tr("Float"):
            return "F"
        if lab == share.locales.tr("Integer"):
            return "I"
        if lab == share.locales.tr("Date"):
            return "D"
        if lab == share.locales.tr("DateTime"):
            return "T"
        if lab == share.locales.tr("Logical"):
            return "L"
        if lab == share.locales.tr("Memo"):
            return "M"
        return "C"

    def _load_dbf_schema(self, path: str) -> bool:
        try:
            with open(path, "rb") as f:
                hdr = f.read(32)
                if len(hdr) < 32:
                    return False
                # header length at bytes 8-9 (little endian)
                header_len = int.from_bytes(hdr[8:10], "little")
                if header_len < 33:
                    return False
                # field descriptors follow
                f.seek(32)
                desc_bytes = f.read(max(0, header_len - 32))
                # descriptors end with 0x0D
                end = desc_bytes.find(b"\x0D")
                if end == -1:
                    end = len(desc_bytes)
                desc_bytes = desc_bytes[:end]

            fields = []
            for i in range(0, len(desc_bytes), 32):
                chunk = desc_bytes[i:i+32]
                if len(chunk) < 32:
                    break
                name_raw = chunk[0:11].split(b"\x00", 1)[0]
                name = name_raw.decode("ascii", errors="ignore").strip()
                if not name:
                    continue
                ftype = chr(chunk[11])
                flen = chunk[16]
                fdec = chunk[17]
                fields.append((name, ftype, flen, fdec))

            # full reset so view/proxy always reflects new schema
            self._updating = True
            try:
                try:
                    self.model.beginResetModel()
                except Exception:
                    pass
                try:
                    self.model.removeRows(0, self.model.rowCount())
                    for r, (name, ftype, flen, fdec) in enumerate(fields):
                        self.model.insertRow(r)
                        self.model.setItem(r, 0, QStandardItem(str(r + 1)))
                        self.model.setItem(r, 1, QStandardItem(name))
                        self.model.setItem(r, 2, QStandardItem(self._type_char_to_label(ftype)))
                        self.model.setItem(r, 3, QStandardItem(str(int(flen))))
                        self.model.setItem(r, 4, QStandardItem(str(int(fdec))))
                        self.model.setItem(r, 5, QStandardItem(share.locales.tr("kein")))
                finally:
                    try:
                        self.model.endResetModel()
                    except Exception:
                        pass
            finally:
                self._updating = False

            if self.model.rowCount() > 0:
                self._select_source_row(0)
                try:
                    self.proxy.setCurrentRow(0)
                except Exception:
                    pass
            return True
        except Exception:
            return False

    def _save_dbf_schema(self, path: str) -> bool:
        # write schema-only DBF (0 records), dBase 5 compatible header
        try:
            # collect fields
            fields = []
            for r in range(self.model.rowCount()):
                name = (self.model.item(r, 1).text() if self.model.item(r, 1) else "").strip()
                if not name:
                    continue
                name = name[:11]  # dbf limit
                tlabel = (self.model.item(r, 2).text() if self.model.item(r, 2) else share.locales.tr("Character"))
                ftype = self._type_label_to_char(tlabel)
                flen = int((self.model.item(r, 3).text() if self.model.item(r, 3) else "0") or "0")
                fdec = int((self.model.item(r, 4).text() if self.model.item(r, 4) else "0") or "0")
                flen = 1 if flen <= 0 else min(255, flen)
                fdec = 0 if fdec < 0 else min(255, fdec)
                fields.append((name, ftype, flen, fdec))

            n = len(fields)
            header_len = 32 + 32 * n + 1
            record_len = 1 + sum(f[2] for f in fields)  # deletion flag + field widths

            today = datetime.date.today()
            ver = 0x03  # dBASE III+ style, widely accepted as "dBase 5 compatible" for schema
            num_records = 0

            hdr = bytearray(32)
            hdr[0] = ver
            hdr[1] = today.year - 1900
            hdr[2] = today.month
            hdr[3] = today.day
            hdr[4:8] = int(num_records).to_bytes(4, "little", signed=False)
            hdr[8:10] = int(header_len).to_bytes(2, "little", signed=False)
            hdr[10:12] = int(record_len).to_bytes(2, "little", signed=False)
            # rest stays 0

            out = bytearray()
            out += hdr

            # field descriptors
            for name, ftype, flen, fdec in fields:
                desc = bytearray(32)
                nb = name.encode("ascii", errors="ignore")[:11]
                desc[0:len(nb)] = nb
                desc[11] = ord(ftype)
                # desc[12:16] data address = 0
                desc[16] = int(flen) & 0xFF
                desc[17] = int(fdec) & 0xFF
                out += desc

            out += b"\x0D"  # field descriptor terminator
            out += b"\x1A"  # EOF marker (optional but common)

            with open(path, "wb") as f:
                f.write(out)
            return True
        except Exception:
            return False

    # --------------------------
    # Demo data (kept for convenience)
    # --------------------------
    def _fill_demo_data(self):
        rows = [
            (1,  "First_Name",    share.locales.tr("Character"), 25, 0, "None"),
            (2,  "Last_Name",     share.locales.tr("Character"), 35, 0, "None"),
            (3,  "Sex",           share.locales.tr("Character"),  1, 0, "None"),
            (4,  "Address",       share.locales.tr("Character"), 40, 0, "None"),
            (5,  "City",          share.locales.tr("Character"), 25, 0, "None"),
            (6,  "State_Prov",    share.locales.tr("Character"), 17, 0, "None"),
            (7,  "Zip",           share.locales.tr("Character"), 10, 0, "None"),
        ]

        self._updating = True
        try:
            self.model.removeRows(0, self.model.rowCount())
            for r, (no, name, typ, width, dec, idx) in enumerate(rows):
                self.model.insertRow(r)
                self.model.setItem(r, 0, QStandardItem(str(no)))
                self.model.setItem(r, 1, QStandardItem(name))
                self.model.setItem(r, 2, QStandardItem(typ))
                self.model.setItem(r, 3, QStandardItem(str(width)))
                self.model.setItem(r, 4, QStandardItem(str(dec)))
                self.model.setItem(r, 5, QStandardItem(share.locales.tr("kein") if (idx or "").strip().lower() in ("none", "") else idx))
        finally:
            self._updating = False

        self._set_modified(False)

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
#        self.splitter.setStyleSheet(share.locales.css("EditorWindow_Splitter"))
#        self.setStyleSheet(share.locales.css("EditorWindow_Dialog"))
        
        # --- TreeView links ---
        self.tree = QTreeView(self.splitter)

#        self.tree.setStyleSheet(share.locales.css("EditoWidget"))
        
        # Dummy Model (später kannst du hier Klassen/Methoden/etc. einfüllen)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels([share.locales.tr("Structure")])
        
        root = model.invisibleRootItem()
        
        root.appendRow(QStandardItem("CLASS ParentForm"))
        root.appendRow(QStandardItem("METHOD Init"))
        
        self.tree.setModel(model)
        self.tree.expandAll()
        
        vlayout = QVBoxLayout()

        # Mehrzeiliges Eingabefeld
        self.text = CodeEditor(self.splitter)
        self.text.setPlaceholderText(share.locales.tr("Please enter text"))
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
        self.btn_run = share.widgets.button.glossy.GlossyPillButtonGreen(share.locales.tr("Ausführen"), self)
        self.btn_run.clicked.connect(self.on_button_run_clicked)

        # Run per F2 (auch ohne Kontextmenü)
        self.text.runRequested.connect(self.on_button_run_clicked)
        self.act_run_f2 = QAction(share.locales.tr("Run"), self)
        self.act_run_f2.setShortcut(QKeySequence(Qt.Key_F2))
        self.act_run_f2.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.act_run_f2.triggered.connect(self.on_button_run_clicked)
        self.addAction(self.act_run_f2)
        
        vlayout.addWidget(self.btn_run)
        
        h1layout = QHBoxLayout()
        self.btn_gen_python = share.widgets.button.glossy.GlossyPillButtonBlue(share.locales.tr("Gen. Python Code" ), self)
        self.btn_gen_pascal = share.widgets.button.glossy.GlossyPillButtonBlue(share.locales.tr("Gen. Pascal Code" ), self)
        self.btn_gen_javout = share.widgets.button.glossy.GlossyPillButtonBlue(share.locales.tr("Gen. Jave Code"   ), self)
        self.btn_gen_gnucpp = share.widgets.button.glossy.GlossyPillButtonBlue(share.locales.tr("Gen. GNU C++ Code"), self)
        self.btn_gen_csharp = share.widgets.button.glossy.GlossyPillButtonBlue(share.locales.tr("Gen. C-Sharp Code"), self)
        
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
        self.btn_gen_vbaout = share.widgets.button.glossy.GlossyPillButtonGold(share.locales.tr("Gen. Visual-Basic Access Code"), self)
        self.btn_gen_javscr = share.widgets.button.glossy.GlossyPillButtonGold(share.locales.tr("Gen. Java Script Code"), self)
        
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
        debug_print("gen vba ok.")
        
    def on_button_gen_javscr_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToJavaScript(parser, class_name="GenProg", module_name=None)
        codegen.generate(parser.tree, "dbase.js")
        debug_print("gen js ok.")
        
    def on_button_gen_csharp_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToCSharp(parser, class_name="GenProg", namespace=None)
        codegen.generate(parser.tree, "dbase.cs")
        debug_print("gen c-sharp ok.")
        
    def on_button_gen_javout_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToJava(parser, class_name="GenProg", package=None)
        codegen.generate(parser.tree, "dbase.java")
        debug_print("gen java ok.")

    def on_button_gen_python_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToPython(parser.parser)
        codegen.generate(parser.tree, "dbase.py")
        debug_print("gen py ok.")
    
    def on_button_gen_gnucpp_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToCpp(parser, prog_name="genprog")
        codegen.generate(parser.tree, "dbase.cc")
        debug_print("gen c++ ok.")
    
    def on_button_gen_pascal_clicked(self):
        parser  = DBaseParser(self.filename)
        codegen = DBaseToPascal(parser, unit_name="GenProg")
        codegen.generate(parser.tree, "dbase.pas")
        debug_print("gen pas ok.")
    
    def on_button_hlp_clicked(self):
        debug_print("hhhhh")
        
    def on_button_run_clicked(self):
        # Das ist die Funktion, die beim Klick ausgeführt wird
        content = self.text.toPlainText().strip()
        if not content:
            QMessageBox.information(self, "Info", share.locales.tr("Please enter text"))
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
            share.locales.tr("Comment Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except KeyError as e:
            tb_str = (f"error: {e.name}: {e.message}\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            share.locales.tr("Internal Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except PermissionError as e:
            tb_str = (f"error: Zugriff verweigert\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            share.locales.tr("Access Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except FileNotFoundError as e:
            tb_str = (f"error: Datei nicht gefunden.\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,
            share.locales.tr("File Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except NameError as e:
            msg = str(e)
            m = re.search(r"name '([^']+)' is not defined", msg)
            missing = m.group(1) if m else "<?>"
            message = share.locales.tr("Internal Error (Python NameError)") + "\n"
            message = message + f"{missing}: {msg}"
            
            tb_str = (f"Fehler: {message}\n")
            tb_str = (tb_str + "".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,share.locales.tr("Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except AttributeError as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,share.locales.tr("Attribut Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except RuntimeError as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,share.locales.tr("Runtime Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except SyntaxError as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            dlg = showException(self,share.locales.tr("Syntax Error: ") + type(e).__name__, tb_str)
            dlg.exec_()
        except Exception as e:
            tb_str = ("".join(traceback.TracebackException.from_exception(e).format()))
            
            traceback.print_exc()
            dlg = showException(self,share.locales.tr("Common Exception: ") + type(e).__name__, tb_str)
            dlg.exec_()

# ---------------------------------------------------------------------------
# IconView je Tab. Zeigt je nach Filter andere Dateiarten.
# Meta-Info pro Item:
#   - Qt.UserRole: voller Pfad
# Meta-Info am Widget:
#   - self.base_dir (und Qt Property 'directory')
# ---------------------------------------------------------------------------
class IconTab(QListWidget):
    def __init__(self, include_exts=None, exclude_exts=None, parent=None, icon_provider=None):
        super().__init__(parent)

        self.include_exts = [e.lower() for e in (include_exts or [])]
        self.exclude_exts = [e.lower() for e in (exclude_exts or [])]
        self.base_dir = ""
        self.icon_provider = icon_provider or QFileIconProvider()

        # IconView-Layout
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setWrapping(True)
        self.setWordWrap(True)
        self.setTextElideMode(Qt.ElideRight)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setIconSize(QSize(48, 48))
        self.setGridSize(QSize(120, 92))
        self.setSpacing(8)

        # Kontextmenü
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

        # F2 = Ausführen
        self._act_run = QAction(share.locales.tr("Run - F2"), self)
        self._act_run.setShortcut(QKeySequence(Qt.Key_F2))
        self._act_run.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._act_run.triggered.connect(self._run_selected)
        self.addAction(self._act_run)

        # Doppelklick: Standardaktion fuer unterstuetzte Dateien ausfuehren
        self.setFocusPolicy(Qt.StrongFocus)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)

    def set_directory(self, directory: str):
        directory = (directory or "").strip()
        self.base_dir = directory
        self.setProperty("directory", directory)
        self.refresh()

    def _suffix_match(self, lower_name: str, ext: str) -> bool:
        lower_name = (lower_name or "").lower()
        ext = (ext or "").lower().strip()
        if not ext:
            return False
        if lower_name.endswith(ext):
            return True
        try:
            suffixes = ''.join(Path(lower_name).suffixes)
            if suffixes.endswith(ext):
                return True
        except Exception:
            pass
        if ext == '.sqlb.json':
            return lower_name.endswith('.json') and '.sqlb.' in lower_name
        return False

    def _matches_include(self, name: str) -> bool:
        lower = (name or "").lower()
        if not self.include_exts:
            return True
        for ext in self.include_exts:
            if self._suffix_match(lower, ext):
                return True
        return False

    def _matches_exclude(self, name: str) -> bool:
        lower = (name or "").lower()
        if not self.exclude_exts:
            return False
        for ext in self.exclude_exts:
            if self._suffix_match(lower, ext):
                return True
        return False

    def refresh(self):
        self.setUpdatesEnabled(False)
        try:
            self.clear()
            if not self.base_dir or not os.path.isdir(self.base_dir):
                return

            entries = []
            try:
                for name in os.listdir(self.base_dir):
                    full = os.path.join(self.base_dir, name)
                    if os.path.isfile(full):
                        entries.append((name, full))
            except Exception:
                entries = []

            entries.sort(key=lambda t: t[0].lower())

            for name, full in entries:
                if not self._matches_include(name):
                    continue
                if self._matches_exclude(name):
                    continue

                info = QFileInfo(full)
                lower_name = name.lower()
                is_sql_file = self._suffix_match(lower_name, '.sql') or self._suffix_match(lower_name, '.sqlb.json')
                if is_sql_file:
                    try:
                        icon = icon_from_svg(SVG_SQL, 48)
                    except Exception:
                        try:
                            icon = icon_from_svg(SVG_PAGE, 48)
                        except Exception:
                            icon = self.icon_provider.icon(info)
                else:
                    icon = self.icon_provider.icon(info)
                item = QListWidgetItem(icon, name)
                item.setToolTip(full)
                item.setData(Qt.UserRole, full)
                self.addItem(item)
        finally:
            self.setUpdatesEnabled(True)

    def _selected_path(self) -> str:
        it = self.currentItem()
        if not it:
            return ""
        path = it.data(Qt.UserRole) or ""
        if not path:
            try:
                tip = (it.toolTip() or "").strip()
                if tip and os.path.isfile(tip):
                    path = tip
            except Exception:
                path = ""
        if not path:
            try:
                candidate = os.path.join(self.base_dir or "", it.text())
                if os.path.isfile(candidate):
                    path = candidate
            except Exception:
                path = ""
        return path

    def _run_selected(self):
        path = self._selected_path()
        if path:
            self._run_file(path)

    # ---------------------------------------------------------------------------
    # Bei Doppelklick auf unterstuetzte Dateien -> passende Standardaktion.
    # ---------------------------------------------------------------------------
    def _on_item_double_clicked(self, item: QListWidgetItem):
        try:
            path = item.data(Qt.UserRole) or ""
            if not path:
                try:
                    tip = (item.toolTip() or "").strip()
                    if tip and os.path.isfile(tip):
                        path = tip
                except Exception:
                    path = ""
            if not path:
                try:
                    candidate = os.path.join(self.base_dir or "", item.text())
                    if os.path.isfile(candidate):
                        path = candidate
                except Exception:
                    path = ""
            if not path:
                return
            lower = path.lower()
            if lower.endswith(".prg") or lower.endswith(".dbf") or lower.endswith(".sqlb.json") or lower.endswith(".po") or lower.endswith(".pro"):
                self._run_file(path)
        except Exception:
            # keine harte Fehlermeldung bei UI-Events
            pass

    
    def _on_context_menu(self, pos: QPoint):
        # Kontextmenü für die IconView (auch bei Rechtsklick auf leere Fläche).
        item = self.itemAt(pos)
        if item:
            self.setCurrentItem(item)
            path = item.data(Qt.UserRole) or ""
            if not path:
                try:
                    tip = (item.toolTip() or "").strip()
                    if tip and os.path.isfile(tip):
                        path = tip
                except Exception:
                    path = ""
            if not path:
                try:
                    candidate = os.path.join(self.base_dir or "", item.text())
                    if os.path.isfile(candidate):
                        path = candidate
                except Exception:
                    path = ""
        else:
            path = ""

        menu = QMenu(self)

        # --- Neu Submenu (immer vorhanden) ---
        m_new = menu.addMenu(share.locales.tr("Neu"))
        act_new_prg = QAction(share.locales.tr("Programm"), self)
        act_new_prg.triggered.connect(self._new_program)
        m_new.addAction(act_new_prg)

        act_new_table = QAction(share.locales.tr("Tabelle"), self)
        act_new_table.triggered.connect(self._new_table)
        m_new.addAction(act_new_table)

        act_new_sql = QAction(share.locales.tr("SQL Query"), self)
        act_new_sql.triggered.connect(self._new_sql_query)
        m_new.addAction(act_new_sql)

        act_new_localize = QAction(share.locales.tr("Localize"), self)
        act_new_localize.triggered.connect(self._new_localize)
        m_new.addAction(act_new_localize)

        menu.addSeparator()

        # --- Datei-Aktionen (nur wenn Item selektiert) ---
        if path:
            ext = os.path.splitext(path)[1].lower()

            act_run = QAction(share.locales.tr("Run - F2"), self)
            act_run.triggered.connect(lambda: self._run_file(path))
            menu.addAction(act_run)

            act_edit = QAction(share.locales.tr("Edit"), self)
            act_edit.triggered.connect(lambda: self._edit_in_editor(path))
            
            menu.addAction(act_edit)
            menu.addSeparator()
            
            m_compile    = menu.addMenu(share.locales.tr("Compile"))
            act_c_py     = QAction("Python",     self)
            act_c_pascal = QAction("Pascal",     self)
            act_c_cpp    = QAction("C++",        self)
            act_c_csharp = QAction("C Sharp",    self)
            act_c_java   = QAction("Java",       self)
            act_c_javscr = QAction("JavaScript", self)
            
            act_c_py    .setEnabled(ext == ".prg")
            act_c_pascal.setEnabled(ext == ".prg")
            act_c_cpp   .setEnabled(ext == ".prg")
            act_c_csharp.setEnabled(ext == ".prg")
            act_c_java  .setEnabled(ext == ".prg")
            act_c_javscr.setEnabled(ext == ".prg")
            
            act_c_py    .triggered.connect(lambda: self._compile_to_python(path))
            act_c_pascal.triggered.connect(lambda: self._compile_to_pascal(path))
            act_c_cpp   .triggered.connect(lambda: self._compile_to_cpp   (path))
            act_c_csharp.triggered.connect(lambda: self._compile_to_csharp(path))
            act_c_java  .triggered.connect(lambda: self._compile_to_java  (path))
            act_c_javscr.triggered.connect(lambda: self._compile_to_javscr(path))
            
            m_compile.addAction(act_c_py    )
            m_compile.addAction(act_c_pascal)
            m_compile.addAction(act_c_cpp   )
            m_compile.addAction(act_c_csharp)
            m_compile.addAction(act_c_java  )
            m_compile.addAction(act_c_javscr)

            menu.addSeparator()

            act_copy = QAction(share.locales.tr("Copy"), self)
            act_copy.triggered.connect(lambda: self._copy_path(path))
            menu.addAction(act_copy)

            act_ren = QAction(share.locales.tr("Rename"), self)
            act_ren.triggered.connect(lambda: self._rename_file(item, path))
            menu.addAction(act_ren)

            act_del = QAction(share.locales.tr("Delete"), self)
            act_del.triggered.connect(lambda: self._delete_file(item, path))
            menu.addAction(act_del)

        menu.exec_(self.viewport().mapToGlobal(pos))

    # ------------------------------------------------------------------
    # Neu Aktionen (RegieCenter IconView)
    # ------------------------------------------------------------------
    def _regiecenter_host(self):
        host = self.parent()
        while host is not None and host.__class__.__name__ != "RegieCenter":
            host = host.parent()
        return host

    def _refresh_all_icon_tabs(self):
        host = self._regiecenter_host()
        if host is None:
            return
        try:
            cur_dir = host.combo.currentText()
            host._on_dir_changed(cur_dir)
        except Exception:
            try:
                self.refresh()
            except Exception:
                pass

    def _unique_name_in_dir(self, directory: str, base: str, ext: str) -> str:
        directory = os.path.normpath(directory or "")
        if not directory:
            return ""
        candidate = os.path.join(directory, f"{base}{ext}")
        if not os.path.exists(candidate):
            return candidate
        i = 1
        while True:
            candidate = os.path.join(directory, f"{base}{i}{ext}")
            if not os.path.exists(candidate):
                return candidate
            i += 1

    def _new_program(self):
        host = self._regiecenter_host()
        directory = (getattr(self, "base_dir", "") or "").strip()
        if not directory or not os.path.isdir(directory):
            QMessageBox.information(self, "Neu", "Bitte zuerst ein Verzeichnis auswählen.")
            return

        path = self._unique_name_in_dir(directory, "unbenannt", ".prg")
        if not path:
            return

        try:
            tpl = "* unbenannt.prg\n\n"
            with open(path, "w", encoding="utf-8", errors="replace") as f:
                f.write(tpl)
        except Exception as e:
            QMessageBox.warning(self, "Neu", f"Konnte Datei nicht erstellen:\n{e}")
            return

        self._refresh_all_icon_tabs()

        if host is not None and hasattr(host, "open_in_code_editor"):
            host.open_in_code_editor(display_name=os.path.basename(path), path=path)

    def _new_table(self):
        # neues Tabellen-Designer Fenster (ohne Records)
        try:
            if "MAINAPP" in globals() and hasattr(MAINAPP, "mdi_open_table_designer"):
                MAINAPP.mdi_open_table_designer()
                return
        except Exception:
            pass
        QMessageBox.information(self, "Neu", "Konnte Table-Designer nicht öffnen (Hook fehlt).")

    def _new_sql_query(self):
        # SQL Builder öffnen
        try:
            if "MAINAPP" in globals():
                if hasattr(MAINAPP, "mdi_open_sql_builder"):
                    MAINAPP.mdi_open_sql_builder()
                    return
                if hasattr(MAINAPP, "on_action_view_sql_builder"):
                    MAINAPP.on_action_view_sql_builder()
                    return
        except Exception:
            pass
        QMessageBox.information(self, "Neu", "Konnte SQL Builder nicht öffnen (Hook fehlt).")

    def _new_localize(self):
        # Localize-Dialog öffnen
        try:
            if "MAINAPP" in globals() and hasattr(MAINAPP, "ensure_localize_tool"):
                try:
                    MAINAPP.ensure_localize_tool(focus=True, po_path="")
                except TypeError:
                    MAINAPP.ensure_localize_tool(focus=True)
                return
        except Exception:
            pass
        QMessageBox.information(self, "Neu", "Konnte Localize nicht öffnen (Hook fehlt).")

    def _close_regiecenter(self):
        host = self._regiecenter_host()
        try:
            if host is not None:
                host.close()
                return
        except Exception:
            pass

    def _edit_in_editor(self, path: str) -> None:
        try:
            lower = path.lower()
            is_prg = lower.endswith('.prg')
            is_dbf = lower.endswith('.dbf')
            is_sql_builder = lower.endswith('.sqlb.json')
            is_po = lower.endswith('.po')
            if not (is_prg or is_dbf or is_sql_builder or is_po):
                return

            display_name = os.path.basename(path)

            # Host/RegieCenter finden (parent-chain)
            host = self.parent()

            if is_prg:
                while host is not None and not hasattr(host, "open_in_code_editor"):
                    host = host.parent()
                if host is not None and hasattr(host, "open_in_code_editor"):
                    host.open_in_code_editor(display_name=display_name, path=path)
                else:
                    QMessageBox.information(self, "Bearbeiten", "Kein CodeEditor-Hook gefunden.")
            elif is_dbf:
                while host is not None and not hasattr(host, "open_in_table_editor"):
                    host = host.parent()
                if host is not None and hasattr(host, "open_in_table_editor"):
                    global MDIHOST
                    MDIHOST = host
                    MDIHOST.open_in_table_editor(display_name=display_name, path=path)
                else:
                    QMessageBox.information(self, "Bearbeiten", "Kein TabellenEditor-Hook gefunden.")
            elif is_sql_builder:
                while host is not None and not hasattr(host, "open_in_sql_builder"):
                    host = host.parent()
                if host is not None and hasattr(host, "open_in_sql_builder"):
                    host.open_in_sql_builder(display_name=display_name, path=path)
                else:
                    QMessageBox.information(self, "Bearbeiten", "Kein SQL-Builder-Hook gefunden.")
            elif is_po:
                while host is not None and not hasattr(host, "open_in_localize"):
                    host = host.parent()
                if host is not None and hasattr(host, "open_in_localize"):
                    host.open_in_localize(display_name=display_name, path=path)
                else:
                    QMessageBox.information(self, "Bearbeiten", "Kein Localize-Hook gefunden.")
        except Exception as e:
            QMessageBox.warning(self, "Bearbeiten", f"Konnte Editor nicht öffnen:\n{e}")

    def _copy_path(self, path: str) -> None:
        try:
            QApplication.clipboard().setText(path)
        except Exception as e:
            QMessageBox.warning(self, "Kopieren", f"Konnte Pfad nicht kopieren:\n{e}")

    def _run_file(self, path: str):
        try:
            lower = path.lower()
            if lower.endswith(".prg"):
                parse(path)
                return
            if lower.endswith(".dbf"):
                self._edit_in_editor(path)
                return
            if lower.endswith(".sqlb.json"):
                self._edit_in_editor(path)
                return
            if lower.endswith(".po"):
                self._edit_in_editor(path)
                return
            if lower.endswith(".pro"):
                try:
                    mw = MAINAPP
                except Exception:
                    mw = None
                if mw is not None and hasattr(mw, "open_project_file"):
                    mw.open_project_file(path)
                return

            #if os.name == "nt":
            #    os.startfile(path)  # noqa
            #elif sys.platform == "darwin":
            #    subprocess.Popen(["open", path])
            #else:
            #    subprocess.Popen(["xdg-open", path])
        except Exception as e:
            QMessageBox.warning(self, "Ausführen", f"Konnte Datei nicht starten:\n{e}")
    
    def _compile_output_path(self, src_path: str, lang_folder: str, ext: str) -> str:
        src_path = os.path.abspath(src_path)
        src_dir  = os.path.dirname(src_path)
        src_name = os.path.splitext(os.path.basename(src_path))[0]

        out_dir = os.path.join(src_dir, "build", lang_folder)
        os.makedirs(out_dir, exist_ok=True)

        return os.path.join(out_dir, src_name + ext)

    def _compile_to_vba(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "vba", ".cls")
        codegen  = DBaseToVBAAccess(parser, class_name="GenProg", module_name="GenProg")
        codegen.generate(parser.tree, out_file)
        debug_print("gen vba ok:", out_file)
        
    def _compile_to_javscr(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "javascript", ".js")
        codegen  = DBaseToJavaScript(parser, class_name="GenProg", module_name=None)
        codegen.generate(parser.tree, out_file)
        debug_print("gen js ok:", out_file)
        
    def _compile_to_csharp(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "csharp", ".cs")
        codegen  = DBaseToCSharp(parser, class_name="GenProg", namespace=None)
        codegen.generate(parser.tree, out_file)
        debug_print("gen c-sharp ok:", out_file)
        
    def _compile_to_java(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "java", ".java")
        codegen  = DBaseToJava(parser, class_name="GenProg", package=None)
        codegen.generate(parser.tree, out_file)
        debug_print("gen java ok:", out_file)
    
    def _compile_to_python(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "python", ".py")
        codegen  = DBaseToPython(parser.parser)
        codegen.generate(parser.tree, out_file)
        debug_print("gen py ok:", out_file)
        
    def _compile_to_cpp(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "cpp", ".cc")
        codegen  = DBaseToCpp(parser, prog_name="genprog")
        codegen.generate(parser.tree, out_file)
        debug_print("gen c++ ok:", out_file)
    
    def _compile_to_pascal(self, path: str):
        parser   = DBaseParser(path)
        out_file = self._compile_output_path(path, "pascal", ".pas")
        codegen  = DBaseToPascal(parser, unit_name="GenProg")
        codegen.generate(parser.tree, out_file)
        debug_print("gen pas ok:", out_file)

class RegieCenter(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        mark_escape_close(self)
        
        self.setFont(QFont("Arial", 10))

        self.setWindowTitle(share.locales.tr("Regierzentrum"))
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)

        self.icon_provider = QFileIconProvider()

        # --- Top controls ---
        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setInsertPolicy(QComboBox.NoInsert)
        self.combo.currentTextChanged.connect(self._on_dir_changed)

        self.btn_pick = QPushButton(share.locales.tr("Verzeichnis…"))
        self.btn_pick.clicked.connect(self.pick_directory_non_native)

        top = QHBoxLayout()
        top.addWidget(self.combo, 1)
        top.addWidget(self.btn_pick, 0)

                # --- Tabs ---
        self.tabs = QTabWidget()
        self.icon_lists = []

        # Dateityp-Filter pro Tab (kannst du jederzeit anpassen)
        ext_alltypes  = [
            '.htm', '.html', '.css'   , '.js', '.url',
            '.png', '.jpg' , '.jpeg'  , '.gif', '.bmp', '.svg', '.webp', '.ico',
            '.sql', '.sqlb.json',
            '.dbf', '.csv' , '.xlsx'  , '.xls',
            '.rep', '.rpt' , '.report',
            '.frm', '.form', ".wfm"   ,
            '.dpr', '.prj' , '.proj'  , '.project',
            ".prg"
        ]
        ext_programme = ['.prg']
        ext_projekte  = ['.dpr', '.prj', '.proj', '.project']
        ext_formulare = ['.frm', '.form', '.wfm']
        ext_berichte  = ['.rep', '.rpt', '.report']
        ext_tabellen  = ['.dbf', '.csv', '.xlsx', '.xls']
        ext_sql       = ['.sql', '.sqlb.json']
        ext_grafiken  = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico']
        ext_internet  = ['.htm', '.html', '.css', '.js', '.url']

        self.lw1 = IconTab(ext_alltypes,  parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw1); self.tabs.addTab(self.lw1, 'Alle Typen')
        self.lw2 = IconTab(ext_projekte,  parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw2); self.tabs.addTab(self.lw2, 'Projekte')
        self.lw3 = IconTab(ext_programme, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw3); self.tabs.addTab(self.lw3, 'Programme')
        self.lw4 = IconTab(ext_formulare, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw4); self.tabs.addTab(self.lw4, 'Formulare')        
        self.lw5 = IconTab(ext_tabellen,  parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw5); self.tabs.addTab(self.lw5, 'Tabellen')
        self.lw6 = IconTab(ext_sql,       parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw6); self.tabs.addTab(self.lw6, 'SQL')
        self.lw7 = IconTab(ext_berichte,  parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw7); self.tabs.addTab(self.lw7, 'Berichte')
        self.lw8 = IconTab(ext_grafiken,  parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw8); self.tabs.addTab(self.lw8, 'Grafiken')
        self.lw9 = IconTab(ext_internet,  parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lw9); self.tabs.addTab(self.lw9, 'Internet')

        # Sonstiges = alles, was in keinem der anderen Filter steckt
        ext_all_known = (ext_projekte + ext_formulare + ext_berichte + ext_programme +
                        ext_tabellen + ext_sql + ext_grafiken + ext_internet)
        self.lwA = IconTab(exclude_exts=ext_all_known, parent=self, icon_provider=self.icon_provider)
        self.icon_lists.append(self.lwA); self.tabs.addTab(self.lwA, 'Sonstiges')
        # --- Layout ---
        root = QVBoxLayout(self)
        root.addLayout(top)
        root.addWidget(self.tabs, 1)

        self.resize(980, 640)

        try:
            self._restore_recent_dirs()
        except Exception:
            pass
    
    def open_in_table_editor(self, display_name: str, path: str):
        try:
            debug_print("table")
            path = os.path.normpath(path)
            # erst versuchen: aktives Editor-Fenster wiederverwenden
            sub = None
            win = None
            try:
                sub = MAINAPP.mdi.activeSubWindow() if hasattr(MAINAPP, "mdi") else None
                win = sub.widget() if sub else None
            except Exception:
                sub = None
                win = None

            if isinstance(win, FileEditorWindow):
                win.open_path_in_tab(path)
                win.raise_()
                try:
                    win.activateWindow()
                except Exception:
                    pass
                return
            
            try:
                dlg = TableRecordEditorDialog(MAINAPP, path)
                sub = None
                try:
                    sub = MAINAPP.mdi.addSubWindow(dlg)
                    mark_escape_close(sub)
                except Exception:
                    sub = None
                if sub is not None:
                    dlg._subwindow = sub
                    sub.setWindowTitle(f"Bearbeiten - {os.path.basename(path)}")
                    sub.resize(760, 460)
                    sub.move(240, 60)
                    dlg.show()
                else:
                    dlg.show()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", f"Konnte Bearbeiten-Modus nicht öffnen:\n{e}")
                return
                
        except Exception as e:
            QMessageBox.warning(self, "Bearbeiten", f"Konnte Tabellen-Editor nicht öffnen:\n{e}")
            
    # -----------------------------------------------------------
    # Öffnet *path* im FileEditorWindow (CodeEditor) als Tab.
    # -----------------------------------------------------------
    def open_in_code_editor(self, display_name: str, path: str):
        try:
            debug_print("editor")
            path = os.path.normpath(path)
            # erst versuchen: aktives Editor-Fenster wiederverwenden
            sub = None
            win = None
            try:
                sub = MAINAPP.mdi.activeSubWindow() if hasattr(MAINAPP, "mdi") else None
                win = sub.widget() if sub else None
            except Exception:
                sub = None
                win = None

            if isinstance(win, FileEditorWindow):
                win.open_path_in_tab(path)
                win.raise_()
                try:
                    win.activateWindow()
                except Exception:
                    pass
                return

            # sonst: neues Editor-Fenster im MDI anlegen
            text = ""
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except Exception:
                text = ""

            win = FileEditorWindow(parent=MAINAPP, initial_path=path, initial_text=text)
            win.resize(900, 650)
            if hasattr(MAINAPP, "mdi"):
                sub = MAINAPP.mdi.addSubWindow(win)
                mark_escape_close(sub)
                try:
                    sub.setWindowTitle(display_name or os.path.basename(path))
                except Exception:
                    pass
            win.show()
            win.raise_()
            try:
                win.activateWindow()
            except Exception:
                pass
        except Exception as e:
            QMessageBox.warning(self, "Bearbeiten", f"Konnte Editor nicht öffnen:\n{e}")

    def open_in_sql_builder(self, display_name: str, path: str):
        try:
            debug_print("sqlbuilder")
            path = os.path.normpath(path)
            if "MAINAPP" in globals() and hasattr(MAINAPP, "mdi_open_sql_builder"):
                MAINAPP.mdi_open_sql_builder(path)
                return
        except Exception as e:
            QMessageBox.warning(self, "Bearbeiten", f"Konnte SQL-Builder nicht öffnen:\n{e}")
            return
        QMessageBox.information(self, "Bearbeiten", "Kein SQL-Builder-Hook gefunden.")


    def open_in_localize(self, display_name: str, path: str):
        try:
            debug_print("localize")
            path = os.path.normpath(path)
            if "MAINAPP" in globals() and hasattr(MAINAPP, "ensure_localize_tool"):
                try:
                    MAINAPP.ensure_localize_tool(focus=True, po_path=path)
                except TypeError:
                    widget = MAINAPP.ensure_localize_tool(focus=True)
                    if widget is not None and path:
                        try:
                            if hasattr(widget, "ed_po_path"):
                                widget.ed_po_path.setText(path)
                        except Exception:
                            pass
                        try:
                            if hasattr(widget, "_open_po"):
                                widget._open_po(path)
                        except Exception:
                            pass
                return
        except Exception as e:
            QMessageBox.warning(self, "Bearbeiten", f"Konnte Localize nicht öffnen:\n{e}")
            return
        QMessageBox.information(self, "Bearbeiten", "Kein Localize-Hook gefunden.")

    def _save_recent_dirs(self, current_path: str):
        try:
            if 'MAINAPP' not in globals() or not hasattr(MAINAPP, '_settings'):
                return

            current_path = (current_path or '').strip()
            items = []

            if current_path and os.path.isdir(current_path):
                items.append(current_path)

            for i in range(self.combo.count()):
                txt = (self.combo.itemText(i) or '').strip()
                if txt and os.path.isdir(txt) and txt not in items:
                    items.append(txt)

            items = items[:15]
            MAINAPP._settings.setValue('regiecenter/recent_dirs', items)
            MAINAPP._settings.setValue('regiecenter/workdir', current_path)
        except Exception:
            pass

    def _restore_recent_dirs(self):
        try:
            if 'MAINAPP' not in globals() or not hasattr(MAINAPP, '_settings'):
                return

            recent_dirs = MAINAPP._settings.value('regiecenter/recent_dirs', [], type=list) or []
            workdir = (MAINAPP._settings.value('regiecenter/workdir', '', type=str) or '').strip()

            for entry in recent_dirs:
                entry = (entry or '').strip()
                if entry and os.path.isdir(entry):
                    if self.combo.findText(entry, Qt.MatchExactly) < 0:
                        self.combo.addItem(entry)

            if workdir and os.path.isdir(workdir):
                if self.combo.findText(workdir, Qt.MatchExactly) < 0:
                    self.combo.insertItem(0, workdir)
                self.combo.setCurrentText(workdir)
            elif self.combo.count() > 0:
                self.combo.setCurrentIndex(0)
        except Exception:
            pass

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
        try:
            self._save_recent_dirs(path)
        except Exception:
            pass
        # _on_dir_changed() wird automatisch ausgelöst

    def _on_dir_changed(self, path: str):
        path = (path or "").strip()
        if not path or not os.path.isdir(path):
            for lw in self.icon_lists:
                lw.set_directory("")
                lw.clear()
            return

        # Jede IconView rendert ihren eigenen Filter
        for lw in self.icon_lists:
            lw.set_directory(path)

        # INI: Arbeitsverzeichnis merken
        try:
            if 'MAINAPP' in globals() and hasattr(MAINAPP, '_settings'):
                MAINAPP._settings.setValue('regiecenter/workdir', path)
        except Exception:
            pass

        try:
            self._save_recent_dirs(path)
        except Exception:
            pass

# ---------------------------------------------------------------------------
# Tab 'Benutzer BDE Aliases' wie Screenshot, inkl. Add/Remove/Edit + nicht
# native Dialoge.
# Model: dict[str, dict]  alias -> {"driver": str, "options": str}
# ---------------------------------------------------------------------------
class UserBdeAliasesTab(QWidget):
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)

        self._model = dict(initial or {})
        self._updating_ui = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # -------- Oben: Liste --------
        gb_list  = QGroupBox(share.locales.tr("Definiert ein BDE Anschluss aller"), self)
        v_list   = QVBoxLayout(gb_list)

        self.lst = QListWidget()
        self.lst.setMinimumHeight(220)
        v_list.addWidget(self.lst)

        # -------- Unten: Editor --------
        gb_edit = QGroupBox(share.locales.tr("Benutzer BDE Alias bearbeiten"), self)
        e = QGridLayout(gb_edit)
        e.setHorizontalSpacing(10)
        e.setVerticalSpacing(8)

        e.addWidget(QLabel("Alias:"), 0, 0)
        self.ed_alias = QLineEdit()
        self.ed_alias.setMinimumWidth(230)
        e.addWidget(self.ed_alias, 0, 1)

        self.btn_add    = QPushButton(share.locales.tr("Hinzufügen"))
        self.btn_remove = QPushButton(share.locales.tr("Entfernen"))
        self.btn_add.setFixedWidth(95)
        self.btn_remove.setFixedWidth(95)
        e.addWidget(self.btn_add, 0, 2)
        e.addWidget(self.btn_remove, 0, 3)

        e.addWidget(QLabel(share.locales.tr("Driver:")), 1, 0)
        self.cb_driver = QComboBox()
        self.cb_driver.setMinimumWidth(260)
        self.cb_driver.addItems([
            "dBASE", "PARADOX", "DB2", "ORACLE", "ODBC", "SQL", "FIREBIRD"
        ])
        e.addWidget(self.cb_driver, 1, 1, 1, 3)

        e.addWidget(QLabel(share.locales.tr("Options:")), 2, 0)
        self.ed_options = QLineEdit()
        e.addWidget(self.ed_options, 2, 1, 1, 2)

        self.btn_options = QPushButton("...")
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

    # ---------------------------------------------------------------------------
    # Im Screenshot ist 'Options' meist PATH:... -> sinnvoll ist ein Directory Picker.
    # Wir setzen dann automatisch 'PATH:<dir>'.
    # ---------------------------------------------------------------------------
    def _on_options_browse(self):
        current = self._norm(self.ed_options.text())
        start_dir = ""
        if current.upper().startswith("PATH:"):
            start_dir = current[5:].strip()

        dlg = QFileDialog(self, share.locales.tr("Verzeichnis auswählen"), start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)  # <- NICHT NATIV

        if dlg.exec_():
            dirs = dlg.selectedFiles()
            if dirs:
                self.ed_options.setText(f"PATH:{dirs[0]}")

    # ---------------------------------------------------------------------------
    # Änderungen am aktuell selektierten Alias ins Model übernehmen.
    # Alias-Umbenennung mit Kollisionscheck.
    # ---------------------------------------------------------------------------
    def _on_edit_finished(self):
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

# ---------------------------------------------------------------------------
# Tab 'Quell-Aliases' wie Screenshot, inkl. Add/Remove/Edit + nicht-nativer
# Folder-Dialog.
# model: dict[str, str]  (alias -> path)
# ---------------------------------------------------------------------------
class SourceAliasesTab(QWidget):
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)

        self._model = dict(initial or {})
        self._updating_ui = False

        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)

        # ---- Oben: Liste ----
        gb_list = QGroupBox(share.locales.tr("Definierte Quell-Aliases"), self)
        v_list = QVBoxLayout(gb_list)

        self.lst = QListWidget()
        self.lst.setMinimumHeight(210)
        v_list.addWidget(self.lst)

        # ---- Unten: Editor ----
        gb_edit = QGroupBox(share.locales.tr("Quell-Alias bearbeiten"), self)
        e = QGridLayout(gb_edit)
        e.setHorizontalSpacing(10)
        e.setVerticalSpacing(8)

        e.addWidget(QLabel("Alias:"), 0, 0)
        self.ed_alias = QLineEdit()
        self.ed_alias.setMinimumWidth(220)
        e.addWidget(self.ed_alias, 0, 1)

        self.btn_add    = QPushButton(share.locales.tr("Hinzufügen"))
        self.btn_remove = QPushButton(share.locales.tr("Entfernen"))
        self.btn_add.setFixedWidth(95)
        self.btn_remove.setFixedWidth(95)
        e.addWidget(self.btn_add, 0, 2)
        e.addWidget(self.btn_remove, 0, 3)

        e.addWidget(QLabel(share.locales.tr("Pfad:")), 1, 0)
        self.ed_path = QLineEdit()
        e.addWidget(self.ed_path, 1, 1, 1, 2)

        self.btn_browse = QPushButton("...")
        self.btn_browse.setFixedWidth(30)
        e.addWidget(self.btn_browse, 1, 3, alignment=Qt.AlignLeft)

        root.addWidget(gb_list)
        root.addWidget(gb_edit)
        root.addStretch(1)

        # Demo / initial
        if not self._model:
            self._model.update({
                "CoreShared": r"T:\Programme\dBASE\dBASE2019\Bin\dBLCore\Shared",
                "dBStartup" : r"T:\Programme\dBASE\dBASE2019\Bin\dBStartup",
                "Examples"  : r"T:\Programme\dBASE\dBASE2019\Examples",
                "Forms"     : r"T:\Programme\dBASE\dBASE2019\Forms",
                "Images"    : r"T:\Programme\dBASE\dBASE2019\Images",
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
    # ---------------------------------------------------------------------------
    # Gibt eine Kopie des Modells zurück.
    # ---------------------------------------------------------------------------
    def model(self) -> dict:
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

    # ---------------------------------------------------------------------------
    # Optional: wenn ein bestehender Alias ausgewählt ist,
    # sollen Änderungen an Pfad/Alias (vorsichtig) ins Modell übernommen werden.
    # ---------------------------------------------------------------------------
    def _on_edit_finished(self):
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

        self.setWindowTitle(share.locales.tr("Desktop Properties"))
        self.setModal(False)
        self.setWindowModality(Qt.NonModal)
        self.setFont(QFont("Arial", 10))

        root = QVBoxLayout(self)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("desktop_properties_scroll_area")
        root.addWidget(self.scroll_area, 1)

        self.scroll_widget = QWidget(self.scroll_area)
        self.scroll_widget.setObjectName("desktop_properties_scroll_widget")
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget(self.scroll_widget)
        self.scroll_layout.addWidget(self.tabs, 1)
        self.scroll_area.setWidget(self.scroll_widget)

        self.tabs.addTab(self._build_tab_country(), share.locales.tr("Country"))
        self.tabs.addTab(self._build_tab_table(), share.locales.tr("Table"))
        self.tabs.addTab(self._build_tab_data(), share.locales.tr("Data Entry"))
        self.tabs.addTab(self._build_tab_files(), share.locales.tr("Files"))
        self.tabs.addTab(self._build_tab_app(), share.locales.tr("Application"))
        self.tabs.addTab(self._build_tab_prog(), share.locales.tr("Programming"))
        self.tabs.addTab(self._build_tab_aliase(), share.locales.tr("Source Aliases"))
        self.tabs.addTab(self._build_tab_usrbde(), share.locales.tr("User-BDE-Aliases"))

        btn_row = QHBoxLayout()
        btn_row.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.btn_ok = QPushButton(share.locales.tr("OK"))
        self.btn_cancel = QPushButton(share.locales.tr("Cancel"))
        self.btn_help = QPushButton(share.locales.tr("Help"))
        self.btn_apply = QPushButton(share.locales.tr("Apply"))

        for b in (self.btn_ok, self.btn_cancel, self.btn_help, self.btn_apply):
            b.setFixedWidth(95)

        self.btn_ok.clicked.connect(self.onbtn_accept)
        self.btn_cancel.clicked.connect(self.onbtn_cancel)
        self.btn_help.clicked.connect(self._help)
        self.btn_apply.clicked.connect(self._apply_desktop_properties)

        btn_row.addWidget(self.btn_ok)
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_help)
        btn_row.addWidget(self.btn_apply)
        root.addLayout(btn_row)

        self._country_syncing = False
        self._load_desktop_properties()
        self.resize(620, 520)

    def onbtn_accept(self):
        self._apply_desktop_properties()
        self.accept()
        try:
            self.mdi.close()
        except Exception:
            pass

    def onbtn_cancel(self):
        self.reject()
        try:
            self.mdi.close()
        except Exception:
            pass

    def _desktop_settings(self):
        try:
            if self.parent is not None and hasattr(self.parent, '_settings'):
                return self.parent._settings
        except Exception:
            pass
        try:
            if 'MAINAPP' in globals() and hasattr(MAINAPP, '_settings'):
                return MAINAPP._settings
        except Exception:
            pass
        return None

    def _country_defaults(self) -> dict:
        return {
            'thousand_sep': '.',
            'decimal_sep': ',',
            'currency_position': 'right',
            'currency_display': 'EUR  €',
            'currency_symbol': '€',
            'currency_code': 'EUR',
            'currency_format_short': False,
            'date_format': 'DMY',
            'date_sep': '.',
            'century': True,
            'ui_lang': 'DE - Deutsch',
            'warn_mismatch': False,
        }

    def _allowed_country_separators(self):
        return {'.', ',', "'"}

    def _allowed_date_separators(self):
        return {'.', '/', '-', ':'}

    def _currency_choices(self):
        return [
            ('EUR', '€'), ('USD', '$'), ('GBP', '£'), ('JPY', '¥'), ('CHF', 'CHF'),
            ('SEK', 'kr'), ('NOK', 'kr'), ('DKK', 'kr'), ('PLN', 'zł'), ('CZK', 'Kč'),
            ('HUF', 'Ft'), ('TRY', '₺'), ('RUB', '₽'), ('INR', '₹'), ('CNY', '¥'),
            ('KRW', '₩'), ('UAH', '₴'),
        ]

    def _extract_currency_symbol(self, text: str) -> str:
        txt = (text or '').strip()
        if not txt:
            return self._country_defaults()['currency_symbol']
        parts = txt.split()
        return parts[-1] if len(parts) >= 2 else txt

    def _extract_currency_code(self, text: str) -> str:
        txt = (text or '').strip()
        if not txt:
            return self._country_defaults()['currency_code']
        parts = txt.split()
        return parts[0] if len(parts) >= 2 else txt

    def _update_country_currency_format_checkbox(self):
        try:
            self.chk_currency_format.setText('kurz' if self.chk_currency_format.isChecked() else 'lang')
        except Exception:
            pass

    def _set_currency_combo_text(self, text: str):
        txt = (text or '').strip() or self._country_defaults()['currency_display']
        idx = self.cb_currency.findText(txt, Qt.MatchExactly)
        if idx >= 0:
            self.cb_currency.setCurrentIndex(idx)
        else:
            self.cb_currency.setEditText(txt)

    def _set_currency_combo_from_symbol(self, symbol: str):
        sym = (symbol or '').strip() or self._country_defaults()['currency_symbol']
        for code, item_symbol in self._currency_choices():
            if item_symbol == sym:
                self._set_currency_combo_text(f'{code}  {item_symbol}')
                return
        self.cb_currency.setEditText(sym)

    def _update_country_number_preview(self):
        thousand = (self.ed_thousand.text() or '').strip() or self._country_defaults()['thousand_sep']
        decimal = (self.ed_decimal.text() or '').strip() or self._country_defaults()['decimal_sep']
        self.lbl_num_pattern.setText(f'1{thousand}000{thousand}000{decimal}00')
        self._update_country_currency_preview()

    def _update_country_date_preview(self):
        try:
            today = datetime.date.today()
        except Exception:
            today = None

        if today is None:
            yyyy, yy, mm, dd = '2026', '26', '04', '12'
        else:
            yyyy = f"{today.year:04d}"
            yy = f"{today.year % 100:02d}"
            mm = f"{today.month:02d}"
            dd = f"{today.day:02d}"

        sep = (self.ed_datesep.text() or '').strip() or self._country_defaults()['date_sep']
        fmt = (self.cb_datefmt.currentText() or self._country_defaults()['date_format']).strip().upper()
        year_text = yyyy if self.chk_century.isChecked() else yy

        if fmt == 'MDY':
            pattern = f"{mm}{sep}{dd}{sep}{year_text}"
        elif fmt in ('YMD', 'ISO'):
            pattern = f"{year_text}{sep}{mm}{sep}{dd}"
        else:
            pattern = f"{dd}{sep}{mm}{sep}{year_text}"

        try:
            self.lbl_date_pattern.setText(pattern)
        except Exception:
            pass

    def _update_country_currency_preview(self):
        self._update_country_currency_format_checkbox()
        symbol = self._extract_currency_symbol(self.cb_currency.currentText())
        code = self._extract_currency_code(self.cb_currency.currentText())
        marker = symbol if self.chk_currency_format.isChecked() else code
        number = self.lbl_num_pattern.text().strip() or '129,99'
        number = number.replace('1.000.000,00', '129,99')
        number = number.replace('1,000,000.00', '129.99')
        number = number.replace("1'000'000,00", '129,99')
        number = number.replace("1'000'000.00", '129.99')
        self.lbl_currency_pattern.setText(f'{marker} {number}' if self.rb_left.isChecked() else f'{number} {marker}')

    def _normalize_separator_edit(self, which: str):
        if self._country_syncing:
            return
        defaults = self._country_defaults()
        edit = self.ed_thousand if which == 'thousand' else self.ed_decimal
        default_value = defaults['thousand_sep'] if which == 'thousand' else defaults['decimal_sep']
        value = (edit.text() or '').strip()
        if value == '':
            self._country_syncing = True
            try:
                edit.setText(default_value)
            finally:
                self._country_syncing = False
        elif value not in self._allowed_country_separators():
            QApplication.beep()
            self._country_syncing = True
            try:
                edit.setText(default_value)
            finally:
                self._country_syncing = False
        self._update_country_number_preview()

    def _normalize_date_separator_edit(self):
        if self._country_syncing:
            return
        defaults = self._country_defaults()
        default_value = defaults['date_sep']
        value = (self.ed_datesep.text() or '').strip()
        if value == '':
            self._country_syncing = True
            try:
                self.ed_datesep.setText(default_value)
            finally:
                self._country_syncing = False
        elif value not in self._allowed_date_separators():
            QApplication.beep()
            self._country_syncing = True
            try:
                self.ed_datesep.setText(default_value)
            finally:
                self._country_syncing = False
        self._update_country_date_preview()

    def _sync_country_currency_from_combo(self):
        if not self._country_syncing:
            self._update_country_currency_preview()

    def _table_defaults(self) -> dict:
        return {
            'lock': True,
            'exclusive': False,
            'refresh': 0,
            'retry': 0,
            'default_type': 'dbase',
            'indexblock': 1,
            'memoblock': 8,
            'autosave': False,
            'deleted': True,
            'encrypt': True,
            'ident': False,
            'approx': False,
            'autonull': True,
            'system_show': False,
        }

    def _data_entry_defaults(self) -> dict:
        return {
            'confirm': True,
            'cua': True,
            'escape': True,
            'keyboard_buffer': 49,
            'epoch': 1950,
            'beep_enabled': True,
            'frequency': 512,
            'duration': 50,
        }

    def _files_defaults(self) -> dict:
        workdir = ''
        try:
            settings = self._desktop_settings()
            if settings is not None:
                workdir = (settings.value('regiecenter/workdir', '', type=str) or '').strip()
        except Exception:
            workdir = ''
        if not workdir:
            try:
                workdir = os.getcwd()
            except Exception:
                workdir = ''
        return {
            'current_dir': workdir,
            'search_path': '',
            'log_enabled': False,
            'logfile': '',
            'log_mode': 'overwrite',
            'external_editor': '',
            'backup': False,
            'sessions': False,
        }

    def _app_defaults(self) -> dict:
        return {
            'show_form': True,
            'show_report': True,
            'show_labels': True,
            'show_datamodule': True,
            'show_table': True,
            'file_menu_files': 5,
            'file_menu_projects': 5,
            'db_save_logins': True,
            'db_sql_trace': False,
            'win_fit_to_content': True,
            'win_loop_animations': True,
            'win_save_as_ole2': True,
            'show_splash': True,
        }

    def _programming_defaults(self) -> dict:
        return {
            'decimals': 2,
            'precision': 10,
            'margin': 0,
            'blank': True,
            'trace': False,
            'fieldnames': True,
            'fulltest': False,
            'buildtime': True,
            'design': True,
            'high_precision': False,
            'protect': True,
            'fullpath': False,
            'error_action': '4 - Show Error Dialog',
            'error_log_file': 'PLUSerr.log',
            'max_size_kb': 100,
            'html_template': 'error.htm',
        }

    def _load_desktop_properties(self):
        settings = self._desktop_settings()
        defaults = self._country_defaults()
        if settings is None:
            self._update_country_number_preview()
            self._update_country_date_preview()
            self._update_country_currency_preview()
            self._toggle_data_entry_beep_controls(self.chk_beep.isChecked())
            self._toggle_files_log_controls(self.chk_enable_log.isChecked())
            return
        self._country_syncing = True
        try:
            thousand = (settings.value('desktop/country/thousand_sep', defaults['thousand_sep'], type=str) or defaults['thousand_sep']).strip()
            decimal = (settings.value('desktop/country/decimal_sep', defaults['decimal_sep'], type=str) or defaults['decimal_sep']).strip()
            if thousand not in self._allowed_country_separators():
                thousand = defaults['thousand_sep']
            if decimal not in self._allowed_country_separators():
                decimal = defaults['decimal_sep']
            self.ed_thousand.setText(thousand)
            self.ed_decimal.setText(decimal)
            pos = (settings.value('desktop/country/currency_position', defaults['currency_position'], type=str) or defaults['currency_position']).strip().lower()
            self.rb_left.setChecked(pos == 'left')
            self.rb_right.setChecked(pos != 'left')
            currency_display = (settings.value('desktop/country/currency_display', defaults['currency_display'], type=str) or defaults['currency_display']).strip()
            currency_symbol = (settings.value('desktop/country/currency_symbol', defaults['currency_symbol'], type=str) or defaults['currency_symbol']).strip()
            currency_code = (settings.value('desktop/country/currency_code', defaults['currency_code'], type=str) or defaults['currency_code']).strip()
            currency_format_short = bool(settings.value('desktop/country/currency_format_short', defaults['currency_format_short'], type=bool))
            self.chk_currency_format.setChecked(currency_format_short)
            if currency_display:
                self._set_currency_combo_text(currency_display)
            elif currency_code and currency_symbol:
                self._set_currency_combo_text(f'{currency_code}  {currency_symbol}')
            else:
                self._set_currency_combo_from_symbol(currency_symbol)
            date_format = (settings.value('desktop/country/date_format', defaults['date_format'], type=str) or defaults['date_format']).strip().upper()
            if date_format not in ('DMY', 'MDY', 'YMD', 'ISO'):
                date_format = defaults['date_format']
            self.cb_datefmt.setCurrentText(date_format)
            date_sep = (settings.value('desktop/country/date_sep', defaults['date_sep'], type=str) or defaults['date_sep']).strip()[:1] or defaults['date_sep']
            if date_sep not in self._allowed_date_separators():
                date_sep = defaults['date_sep']
            self.ed_datesep.setText(date_sep)
            self.chk_century.setChecked(bool(settings.value('desktop/country/century', defaults['century'], type=bool)))
            ui_lang = (settings.value('desktop/country/ui_lang', defaults['ui_lang'], type=str) or defaults['ui_lang']).strip()
            idx = self.cb_lang.findText(ui_lang, Qt.MatchExactly)
            if idx >= 0:
                self.cb_lang.setCurrentIndex(idx)
            self.chk_mismatch.setChecked(bool(settings.value('desktop/country/warn_mismatch', defaults['warn_mismatch'], type=bool)))
        finally:
            self._country_syncing = False
        self._update_country_number_preview()
        self._update_country_date_preview()
        self._update_country_currency_preview()
        self._load_table_properties()
        self._load_data_entry_properties()
        self._load_files_properties()
        self._load_app_properties()
        self._load_programming_properties()

    def _save_desktop_properties(self):
        settings = self._desktop_settings()
        if settings is None:
            return
        self._normalize_separator_edit('thousand')
        self._normalize_separator_edit('decimal')
        currency_display = (self.cb_currency.currentText() or '').strip()
        currency_symbol = self._extract_currency_symbol(currency_display)
        currency_code = self._extract_currency_code(currency_display)
        settings.setValue('desktop/country/thousand_sep', (self.ed_thousand.text() or '').strip() or self._country_defaults()['thousand_sep'])
        settings.setValue('desktop/country/decimal_sep', (self.ed_decimal.text() or '').strip() or self._country_defaults()['decimal_sep'])
        settings.setValue('desktop/country/currency_position', 'left' if self.rb_left.isChecked() else 'right')
        settings.setValue('desktop/country/currency_display', currency_display)
        settings.setValue('desktop/country/currency_symbol', currency_symbol)
        settings.setValue('desktop/country/currency_code', currency_code)
        settings.setValue('desktop/country/currency_format_short', bool(self.chk_currency_format.isChecked()))
        self._normalize_date_separator_edit()
        settings.setValue('desktop/country/date_format', self.cb_datefmt.currentText().strip())
        settings.setValue('desktop/country/date_sep', (self.ed_datesep.text() or '').strip()[:1] or self._country_defaults()['date_sep'])
        settings.setValue('desktop/country/century', bool(self.chk_century.isChecked()))
        settings.setValue('desktop/country/ui_lang', self.cb_lang.currentText().strip())
        settings.setValue('desktop/country/warn_mismatch', bool(self.chk_mismatch.isChecked()))
        self._save_table_properties()
        self._save_data_entry_properties()
        self._save_files_properties()
        self._save_app_properties()
        self._save_programming_properties()
        try:
            settings.sync()
        except Exception:
            pass

    def _load_table_properties(self):
        defaults = self._table_defaults()
        settings = self._desktop_settings()
        if settings is None:
            return
        try:
            self.chk_lock.setChecked(bool(settings.value('desktop/table/lock', defaults['lock'], type=bool)))
            self.chk_exclusive.setChecked(bool(settings.value('desktop/table/exclusive', defaults['exclusive'], type=bool)))
            self.spin_refresh.setValue(int(settings.value('desktop/table/refresh', defaults['refresh'], type=int)))
            self.spin_retry.setValue(int(settings.value('desktop/table/retry', defaults['retry'], type=int)))
            default_type = (settings.value('desktop/table/default_type', defaults['default_type'], type=str) or defaults['default_type']).strip().lower()
            self.rb_dbase.setChecked(default_type == 'dbase')
            self.rb_paradox.setChecked(default_type == 'paradox')
            self.rb_sqlite3.setChecked(default_type == 'sqlite3')
            self.rb_mysql.setChecked(default_type == 'mysql')
            if not any((self.rb_dbase.isChecked(), self.rb_paradox.isChecked(), self.rb_sqlite3.isChecked(), self.rb_mysql.isChecked())):
                self.rb_dbase.setChecked(True)
            self.spin_indexblock.setValue(int(settings.value('desktop/table/indexblock', defaults['indexblock'], type=int)))
            self.spin_memoblock.setValue(int(settings.value('desktop/table/memoblock', defaults['memoblock'], type=int)))
            self.chk_autosave.setChecked(bool(settings.value('desktop/table/autosave', defaults['autosave'], type=bool)))
            self.chk_deleted.setChecked(bool(settings.value('desktop/table/deleted', defaults['deleted'], type=bool)))
            self.chk_encrypt.setChecked(bool(settings.value('desktop/table/encrypt', defaults['encrypt'], type=bool)))
            self.chk_ident.setChecked(bool(settings.value('desktop/table/ident', defaults['ident'], type=bool)))
            self.chk_approx.setChecked(bool(settings.value('desktop/table/approx', defaults['approx'], type=bool)))
            self.chk_autonull.setChecked(bool(settings.value('desktop/table/autonull', defaults['autonull'], type=bool)))
            self.chk_system_show.setChecked(bool(settings.value('desktop/table/system_show', defaults['system_show'], type=bool)))
        except Exception:
            pass

    def _save_table_properties(self):
        settings = self._desktop_settings()
        if settings is None:
            return
        default_type = 'dbase'
        if self.rb_paradox.isChecked():
            default_type = 'paradox'
        elif self.rb_sqlite3.isChecked():
            default_type = 'sqlite3'
        elif self.rb_mysql.isChecked():
            default_type = 'mysql'
        settings.setValue('desktop/table/lock', bool(self.chk_lock.isChecked()))
        settings.setValue('desktop/table/exclusive', bool(self.chk_exclusive.isChecked()))
        settings.setValue('desktop/table/refresh', int(self.spin_refresh.value()))
        settings.setValue('desktop/table/retry', int(self.spin_retry.value()))
        settings.setValue('desktop/table/default_type', default_type)
        settings.setValue('desktop/table/indexblock', int(self.spin_indexblock.value()))
        settings.setValue('desktop/table/memoblock', int(self.spin_memoblock.value()))
        settings.setValue('desktop/table/autosave', bool(self.chk_autosave.isChecked()))
        settings.setValue('desktop/table/deleted', bool(self.chk_deleted.isChecked()))
        settings.setValue('desktop/table/encrypt', bool(self.chk_encrypt.isChecked()))
        settings.setValue('desktop/table/ident', bool(self.chk_ident.isChecked()))
        settings.setValue('desktop/table/approx', bool(self.chk_approx.isChecked()))
        settings.setValue('desktop/table/autonull', bool(self.chk_autonull.isChecked()))
        settings.setValue('desktop/table/system_show', bool(self.chk_system_show.isChecked()))

    def _toggle_data_entry_beep_controls(self, on: bool):
        try:
            self.sp_freq.setEnabled(bool(on))
            self.sp_dur.setEnabled(bool(on))
            self.btn_test_beep.setEnabled(bool(on))
        except Exception:
            pass

    def _load_data_entry_properties(self):
        defaults = self._data_entry_defaults()
        settings = self._desktop_settings()
        if settings is None:
            self._toggle_data_entry_beep_controls(self.chk_beep.isChecked())
            return
        try:
            self.chk_confirm.setChecked(bool(settings.value('desktop/data_entry/confirm', defaults['confirm'], type=bool)))
            self.chk_cua.setChecked(bool(settings.value('desktop/data_entry/cua', defaults['cua'], type=bool)))
            self.chk_esc.setChecked(bool(settings.value('desktop/data_entry/escape', defaults['escape'], type=bool)))
            self.sp_buf.setValue(int(settings.value('desktop/data_entry/keyboard_buffer', defaults['keyboard_buffer'], type=int)))
            self.sp_epoch.setValue(int(settings.value('desktop/data_entry/epoch', defaults['epoch'], type=int)))
            self.chk_beep.setChecked(bool(settings.value('desktop/data_entry/beep_enabled', defaults['beep_enabled'], type=bool)))
            self.sp_freq.setValue(int(settings.value('desktop/data_entry/frequency', defaults['frequency'], type=int)))
            self.sp_dur.setValue(int(settings.value('desktop/data_entry/duration', defaults['duration'], type=int)))
        except Exception:
            pass
        self._toggle_data_entry_beep_controls(self.chk_beep.isChecked())

    def _save_data_entry_properties(self):
        settings = self._desktop_settings()
        if settings is None:
            return
        settings.setValue('desktop/data_entry/confirm', bool(self.chk_confirm.isChecked()))
        settings.setValue('desktop/data_entry/cua', bool(self.chk_cua.isChecked()))
        settings.setValue('desktop/data_entry/escape', bool(self.chk_esc.isChecked()))
        settings.setValue('desktop/data_entry/keyboard_buffer', int(self.sp_buf.value()))
        settings.setValue('desktop/data_entry/epoch', int(self.sp_epoch.value()))
        settings.setValue('desktop/data_entry/beep_enabled', bool(self.chk_beep.isChecked()))
        settings.setValue('desktop/data_entry/frequency', int(self.sp_freq.value()))
        settings.setValue('desktop/data_entry/duration', int(self.sp_dur.value()))

    def _quote_path_if_needed(self, value: str) -> str:
        txt = (value or '').strip()
        if not txt:
            return ''
        if len(txt) >= 2 and txt.startswith('"') and txt.endswith('"'):
            return txt
        return f'"{txt}"' if any(ch.isspace() for ch in txt) else txt

    def _toggle_files_log_controls(self, on: bool):
        enabled = bool(on)
        try:
            self.ed_logfile.setEnabled(enabled)
            self.btn_logfile.setEnabled(enabled)
            self.rb_log_overwrite.setEnabled(enabled)
            self.rb_log_append.setEnabled(enabled)
        except Exception:
            pass

    def _browse_files_current_dir(self):
        start_dir = (self.ed_files_current_dir.text() or '').strip() or os.getcwd()
        dlg = QFileDialog(self, share.locales.tr('Verzeichnis auswählen'), start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                self.ed_files_current_dir.setText(os.path.normpath(selected[0]))

    def _append_search_path_entry(self, entry: str):
        value = self._quote_path_if_needed(os.path.normpath(entry or ''))
        if not value:
            return
        current = (self.ed_files_search_path.text() or '').strip()
        if not current:
            self.ed_files_search_path.setText(value)
            return
        parts = [p.strip() for p in current.split(';') if p.strip()]
        if value in parts:
            return
        self.ed_files_search_path.setText(current + ';' + value)

    def _browse_files_search_path(self):
        current = (self.ed_files_search_path.text() or '').strip()
        start_dir = (self.ed_files_current_dir.text() or '').strip() or os.getcwd()
        if current:
            last = current.split(';')[-1].strip()
            if len(last) >= 2 and last.startswith('"') and last.endswith('"'):
                last = last[1:-1]
            if last:
                start_dir = last
        dlg = QFileDialog(self, share.locales.tr('Verzeichnis auswählen'), start_dir)
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                self._append_search_path_entry(selected[0])

    def _browse_external_editor(self):
        start_file = (self.ed_external_editor.text() or '').strip()
        if len(start_file) >= 2 and start_file.startswith('"') and start_file.endswith('"'):
            start_file = start_file[1:-1]
        dlg = QFileDialog(self, share.locales.tr('Editor auswählen'), start_file or os.getcwd())
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(['Programme (*.exe *.bat *.cmd *.com)', 'Alle Dateien (*.*)'])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                self.ed_external_editor.setText(self._quote_path_if_needed(os.path.normpath(selected[0])))

    def _browse_log_file(self):
        start_file = (self.ed_logfile.text() or '').strip()
        dlg = QFileDialog(self, share.locales.tr('Protokolldatei auswählen'), start_file or os.getcwd())
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDefaultSuffix('log')
        dlg.setNameFilters(['Log-Dateien (*.log *.txt)', 'Alle Dateien (*.*)'])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                self.ed_logfile.setText(os.path.normpath(selected[0]))

    def _load_files_properties(self):
        defaults = self._files_defaults()
        settings = self._desktop_settings()
        if settings is None:
            self._toggle_files_log_controls(self.chk_enable_log.isChecked())
            return
        try:
            self.ed_files_current_dir.setText((settings.value('desktop/files/current_dir', defaults['current_dir'], type=str) or defaults['current_dir']).strip())
            self.ed_files_search_path.setText((settings.value('desktop/files/search_path', defaults['search_path'], type=str) or defaults['search_path']).strip())
            self.chk_enable_log.setChecked(bool(settings.value('desktop/files/log_enabled', defaults['log_enabled'], type=bool)))
            self.ed_logfile.setText((settings.value('desktop/files/logfile', defaults['logfile'], type=str) or defaults['logfile']).strip())
            log_mode = (settings.value('desktop/files/log_mode', defaults['log_mode'], type=str) or defaults['log_mode']).strip().lower()
            self.rb_log_append.setChecked(log_mode == 'append')
            self.rb_log_overwrite.setChecked(log_mode != 'append')
            self.ed_external_editor.setText((settings.value('desktop/files/external_editor', defaults['external_editor'], type=str) or defaults['external_editor']).strip())
            self.chk_backup.setChecked(bool(settings.value('desktop/files/backup', defaults['backup'], type=bool)))
            self.chk_sessions.setChecked(bool(settings.value('desktop/files/sessions', defaults['sessions'], type=bool)))
        except Exception:
            pass
        self._toggle_files_log_controls(self.chk_enable_log.isChecked())

    def _save_files_properties(self):
        settings = self._desktop_settings()
        if settings is None:
            return
        current_dir = (self.ed_files_current_dir.text() or '').strip()
        search_path = (self.ed_files_search_path.text() or '').strip()
        external_editor = (self.ed_external_editor.text() or '').strip()
        logfile = (self.ed_logfile.text() or '').strip()
        settings.setValue('desktop/files/current_dir', current_dir)
        settings.setValue('desktop/files/search_path', search_path)
        settings.setValue('desktop/files/log_enabled', bool(self.chk_enable_log.isChecked()))
        settings.setValue('desktop/files/logfile', logfile)
        settings.setValue('desktop/files/log_mode', 'append' if self.rb_log_append.isChecked() else 'overwrite')
        settings.setValue('desktop/files/external_editor', external_editor)
        settings.setValue('desktop/files/backup', bool(self.chk_backup.isChecked()))
        settings.setValue('desktop/files/sessions', bool(self.chk_sessions.isChecked()))
        try:
            if current_dir:
                settings.setValue('regiecenter/workdir', current_dir)
        except Exception:
            pass

    def _load_app_properties(self):
        defaults = self._app_defaults()
        settings = self._desktop_settings()
        if settings is None:
            return
        try:
            self.chk_app_form.setChecked(bool(settings.value('desktop/application/show_form', defaults['show_form'], type=bool)))
            self.chk_app_report.setChecked(bool(settings.value('desktop/application/show_report', defaults['show_report'], type=bool)))
            self.chk_app_labels.setChecked(bool(settings.value('desktop/application/show_labels', defaults['show_labels'], type=bool)))
            self.chk_app_datamodule.setChecked(bool(settings.value('desktop/application/show_datamodule', defaults['show_datamodule'], type=bool)))
            self.chk_app_table.setChecked(bool(settings.value('desktop/application/show_table', defaults['show_table'], type=bool)))
            self.sp_app_files.setValue(int(settings.value('desktop/application/file_menu_files', defaults['file_menu_files'], type=int)))
            self.sp_app_projects.setValue(int(settings.value('desktop/application/file_menu_projects', defaults['file_menu_projects'], type=int)))
            self.chk_app_save_logins.setChecked(bool(settings.value('desktop/application/db_save_logins', defaults['db_save_logins'], type=bool)))
            self.chk_app_sql_trace.setChecked(bool(settings.value('desktop/application/db_sql_trace', defaults['db_sql_trace'], type=bool)))
            self.chk_app_fit.setChecked(bool(settings.value('desktop/application/win_fit_to_content', defaults['win_fit_to_content'], type=bool)))
            self.chk_app_anim.setChecked(bool(settings.value('desktop/application/win_loop_animations', defaults['win_loop_animations'], type=bool)))
            self.chk_app_ole.setChecked(bool(settings.value('desktop/application/win_save_as_ole2', defaults['win_save_as_ole2'], type=bool)))
            self.chk_app_splash.setChecked(bool(settings.value('desktop/application/show_splash', defaults['show_splash'], type=bool)))
        except Exception:
            pass

    def _save_app_properties(self):
        settings = self._desktop_settings()
        if settings is None:
            return
        settings.setValue('desktop/application/show_form', bool(self.chk_app_form.isChecked()))
        settings.setValue('desktop/application/show_report', bool(self.chk_app_report.isChecked()))
        settings.setValue('desktop/application/show_labels', bool(self.chk_app_labels.isChecked()))
        settings.setValue('desktop/application/show_datamodule', bool(self.chk_app_datamodule.isChecked()))
        settings.setValue('desktop/application/show_table', bool(self.chk_app_table.isChecked()))
        settings.setValue('desktop/application/file_menu_files', int(self.sp_app_files.value()))
        settings.setValue('desktop/application/file_menu_projects', int(self.sp_app_projects.value()))
        settings.setValue('desktop/application/db_save_logins', bool(self.chk_app_save_logins.isChecked()))
        settings.setValue('desktop/application/db_sql_trace', bool(self.chk_app_sql_trace.isChecked()))
        settings.setValue('desktop/application/win_fit_to_content', bool(self.chk_app_fit.isChecked()))
        settings.setValue('desktop/application/win_loop_animations', bool(self.chk_app_anim.isChecked()))
        settings.setValue('desktop/application/win_save_as_ole2', bool(self.chk_app_ole.isChecked()))
        settings.setValue('desktop/application/show_splash', bool(self.chk_app_splash.isChecked()))

    def _browse_programming_error_log(self):
        start_file = (self.ed_prog_error_log.text() or '').strip()
        dlg = QFileDialog(self, share.locales.tr('Error Log File auswählen'), start_file or os.getcwd())
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDefaultSuffix('log')
        dlg.setNameFilters(['Log-Dateien (*.log *.txt)', 'Alle Dateien (*.*)'])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                self.ed_prog_error_log.setText(os.path.normpath(selected[0]))

    def _browse_programming_html_template(self):
        start_file = (self.ed_prog_html_template.text() or '').strip()
        dlg = QFileDialog(self, share.locales.tr('HTML Error Template auswählen'), start_file or os.getcwd())
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(['HTML-Dateien (*.htm *.html)', 'Alle Dateien (*.*)'])
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        if dlg.exec_():
            selected = dlg.selectedFiles()
            if selected:
                self.ed_prog_html_template.setText(os.path.normpath(selected[0]))

    def _load_programming_properties(self):
        defaults = self._programming_defaults()
        settings = self._desktop_settings()
        if settings is None:
            return
        try:
            self.sp_prog_decimals.setValue(int(settings.value('desktop/programming/decimals', defaults['decimals'], type=int)))
            self.sp_prog_precision.setValue(int(settings.value('desktop/programming/precision', defaults['precision'], type=int)))
            self.sp_prog_margin.setValue(int(settings.value('desktop/programming/margin', defaults['margin'], type=int)))
            self.chk_prog_blank.setChecked(bool(settings.value('desktop/programming/blank', defaults['blank'], type=bool)))
            self.chk_prog_trace.setChecked(bool(settings.value('desktop/programming/trace', defaults['trace'], type=bool)))
            self.chk_prog_fieldnames.setChecked(bool(settings.value('desktop/programming/fieldnames', defaults['fieldnames'], type=bool)))
            self.chk_prog_fulltest.setChecked(bool(settings.value('desktop/programming/fulltest', defaults['fulltest'], type=bool)))
            self.chk_prog_buildtime.setChecked(bool(settings.value('desktop/programming/buildtime', defaults['buildtime'], type=bool)))
            self.chk_prog_design.setChecked(bool(settings.value('desktop/programming/design', defaults['design'], type=bool)))
            self.chk_prog_high_precision.setChecked(bool(settings.value('desktop/programming/high_precision', defaults['high_precision'], type=bool)))
            self.chk_prog_protect.setChecked(bool(settings.value('desktop/programming/protect', defaults['protect'], type=bool)))
            self.chk_prog_fullpath.setChecked(bool(settings.value('desktop/programming/fullpath', defaults['fullpath'], type=bool)))
            action = (settings.value('desktop/programming/error_action', defaults['error_action'], type=str) or defaults['error_action']).strip()
            idx = self.cb_prog_error_action.findText(action, Qt.MatchExactly)
            if idx >= 0:
                self.cb_prog_error_action.setCurrentIndex(idx)
            else:
                self.cb_prog_error_action.setCurrentText(defaults['error_action'])
            self.ed_prog_error_log.setText((settings.value('desktop/programming/error_log_file', defaults['error_log_file'], type=str) or defaults['error_log_file']).strip())
            self.sp_prog_max_size.setValue(int(settings.value('desktop/programming/max_size_kb', defaults['max_size_kb'], type=int)))
            self.ed_prog_html_template.setText((settings.value('desktop/programming/html_template', defaults['html_template'], type=str) or defaults['html_template']).strip())
        except Exception:
            pass

    def _save_programming_properties(self):
        settings = self._desktop_settings()
        if settings is None:
            return
        settings.setValue('desktop/programming/decimals', int(self.sp_prog_decimals.value()))
        settings.setValue('desktop/programming/precision', int(self.sp_prog_precision.value()))
        settings.setValue('desktop/programming/margin', int(self.sp_prog_margin.value()))
        settings.setValue('desktop/programming/blank', bool(self.chk_prog_blank.isChecked()))
        settings.setValue('desktop/programming/trace', bool(self.chk_prog_trace.isChecked()))
        settings.setValue('desktop/programming/fieldnames', bool(self.chk_prog_fieldnames.isChecked()))
        settings.setValue('desktop/programming/fulltest', bool(self.chk_prog_fulltest.isChecked()))
        settings.setValue('desktop/programming/buildtime', bool(self.chk_prog_buildtime.isChecked()))
        settings.setValue('desktop/programming/design', bool(self.chk_prog_design.isChecked()))
        settings.setValue('desktop/programming/high_precision', bool(self.chk_prog_high_precision.isChecked()))
        settings.setValue('desktop/programming/protect', bool(self.chk_prog_protect.isChecked()))
        settings.setValue('desktop/programming/fullpath', bool(self.chk_prog_fullpath.isChecked()))
        settings.setValue('desktop/programming/error_action', self.cb_prog_error_action.currentText().strip())
        settings.setValue('desktop/programming/error_log_file', (self.ed_prog_error_log.text() or '').strip())
        settings.setValue('desktop/programming/max_size_kb', int(self.sp_prog_max_size.value()))
        settings.setValue('desktop/programming/html_template', (self.ed_prog_html_template.text() or '').strip())

    def _apply_desktop_properties(self):
        self._save_desktop_properties()
        self._update_country_number_preview()
        self._update_country_date_preview()
        self._update_country_currency_preview()
        self._toggle_data_entry_beep_controls(self.chk_beep.isChecked())
        self._toggle_files_log_controls(self.chk_enable_log.isChecked())

    def _build_tab_aliase(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(SourceAliasesTab(tab))
        return tab

    def _build_tab_usrbde(self) -> QWidget:
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(UserBdeAliasesTab(tab))
        return tab

    def _build_tab_country(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        gb_num = QGroupBox(share.locales.tr('Zahlenwerte'), tab)
        num = QGridLayout(gb_num)
        num.setHorizontalSpacing(10)
        num.setVerticalSpacing(8)
        num.addWidget(QLabel(share.locales.tr('Trennzeichen:')), 0, 0)
        self.ed_thousand = QLineEdit('.')
        self.ed_thousand.setFixedWidth(34)
        self.ed_thousand.setMaxLength(1)
        num.addWidget(self.ed_thousand, 0, 1, alignment=Qt.AlignLeft)
        num.addWidget(QLabel(share.locales.tr('Dezimalzeichen:')), 1, 0)
        self.ed_decimal = QLineEdit(',')
        self.ed_decimal.setFixedWidth(34)
        self.ed_decimal.setMaxLength(1)
        num.addWidget(self.ed_decimal, 1, 1, alignment=Qt.AlignLeft)
        num.addWidget(QLabel(share.locales.tr('Muster:')), 2, 0)
        self.lbl_num_pattern = QLabel('1.000.000,00')
        num.addWidget(self.lbl_num_pattern, 2, 1, 1, 2)

        gb_cur = QGroupBox(share.locales.tr('Währungssymbol'), tab)
        cur = QGridLayout(gb_cur)
        cur.setHorizontalSpacing(10)
        cur.setVerticalSpacing(8)
        cur.addWidget(QLabel(share.locales.tr('Position:')), 0, 0)
        self.rb_left = QRadioButton(share.locales.tr('Links'))
        self.rb_right = QRadioButton(share.locales.tr('Rechts'))
        self.rb_right.setChecked(True)
        cur.addWidget(self.rb_left, 0, 1)
        cur.addWidget(self.rb_right, 1, 1)
        cur.addWidget(QLabel(share.locales.tr('Format:')), 2, 0)
        self.chk_currency_format = QCheckBox('lang')
        self.chk_currency_format.setChecked(False)
        cur.addWidget(self.chk_currency_format, 2, 1, alignment=Qt.AlignLeft)
        cur.addWidget(QLabel(share.locales.tr('Symbol:')), 3, 0)
        self.cb_currency = QComboBox()
        self.cb_currency.setEditable(True)
        self.cb_currency.setInsertPolicy(QComboBox.NoInsert)
        self.cb_currency.setMinimumWidth(170)
        try:
            self.cb_currency.setFont(QFont('Consolas', 10))
            if self.cb_currency.lineEdit() is not None:
                self.cb_currency.lineEdit().setFont(QFont('Consolas', 10))
        except Exception:
            pass
        for code, symbol in self._currency_choices():
            self.cb_currency.addItem(f'{code}  {symbol}')
            try:
                self.cb_currency.setItemData(self.cb_currency.count() - 1, QFont('Consolas', 10), Qt.FontRole)
            except Exception:
                pass
        self._set_currency_combo_from_symbol('€')
        cur.addWidget(self.cb_currency, 3, 1, alignment=Qt.AlignLeft)
        cur.addWidget(QLabel(share.locales.tr('Muster:')), 4, 0)
        self.lbl_currency_pattern = QLabel('129,99 EUR')
        cur.addWidget(self.lbl_currency_pattern, 4, 1, 1, 2)

        gb_date = QGroupBox(share.locales.tr('Datum'), tab)
        date = QGridLayout(gb_date)
        date.setHorizontalSpacing(10)
        date.setVerticalSpacing(8)
        date.addWidget(QLabel(share.locales.tr('Datumsformat:')), 0, 0)
        self.cb_datefmt = QComboBox()
        self.cb_datefmt.addItems(['DMY', 'MDY', 'YMD', 'ISO'])
        self.cb_datefmt.setCurrentText('DMY')
        self.cb_datefmt.setFixedWidth(120)
        date.addWidget(self.cb_datefmt, 0, 1, alignment=Qt.AlignLeft)
        date.addWidget(QLabel(share.locales.tr('Datumszeichen:')), 1, 0)
        self.ed_datesep = QLineEdit('.')
        self.ed_datesep.setFixedWidth(34)
        self.ed_datesep.setMaxLength(1)
        date.addWidget(self.ed_datesep, 1, 1, alignment=Qt.AlignLeft)
        self.chk_century = QCheckBox(share.locales.tr('Jahrhundert'))
        self.chk_century.setChecked(True)
        date.addWidget(self.chk_century, 2, 0, 1, 2)
        date.addWidget(QLabel(share.locales.tr('Muster:')), 3, 0)
        self.lbl_date_pattern = QLabel('12.04.2026')
        date.addWidget(self.lbl_date_pattern, 3, 1, 1, 2)

        gb_ui = QGroupBox(share.locales.tr('Umgebungssprache'), tab)
        ui = QGridLayout(gb_ui)
        self.cb_lang = QComboBox()
        self.cb_lang.addItems(['DE - Deutsch', 'EN - English', 'FR - Français'])
        self.cb_lang.setCurrentText('DE - Deutsch')
        self.cb_lang.setFixedWidth(160)
        ui.addWidget(self.cb_lang, 0, 0)

        gb_drv = QGroupBox(share.locales.tr('Sprachtreiber'), tab)
        drv = QGridLayout(gb_drv)
        self.chk_mismatch = QCheckBox(share.locales.tr('Warnung bei Konflikten'))
        drv.addWidget(self.chk_mismatch, 0, 0)

        self.ed_thousand.textChanged.connect(lambda _=None: self._normalize_separator_edit('thousand'))
        self.ed_decimal.textChanged.connect(lambda _=None: self._normalize_separator_edit('decimal'))
        self.ed_thousand.editingFinished.connect(lambda: self._normalize_separator_edit('thousand'))
        self.ed_decimal.editingFinished.connect(lambda: self._normalize_separator_edit('decimal'))
        self.cb_currency.currentTextChanged.connect(lambda _=None: self._sync_country_currency_from_combo())
        self.chk_currency_format.toggled.connect(lambda _=None: self._update_country_currency_preview())
        self.rb_left.toggled.connect(lambda _=None: self._update_country_currency_preview())
        self.rb_right.toggled.connect(lambda _=None: self._update_country_currency_preview())
        self.cb_datefmt.currentTextChanged.connect(lambda _=None: self._update_country_date_preview())
        self.ed_datesep.textChanged.connect(lambda _=None: self._normalize_date_separator_edit())
        self.ed_datesep.editingFinished.connect(self._normalize_date_separator_edit)
        self.chk_century.toggled.connect(lambda _=None: self._update_country_date_preview())

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

        gb_multi = QGroupBox(share.locales.tr('Mehrplatz'), tab)
        l_multi = QGridLayout(gb_multi)
        l_multi.setHorizontalSpacing(10)
        l_multi.setVerticalSpacing(8)
        self.chk_lock = QCheckBox(share.locales.tr('Lock'))
        self.chk_exclusive = QCheckBox(share.locales.tr('Exklusiv'))
        l_multi.addWidget(self.chk_lock, 0, 0, 1, 2)
        l_multi.addWidget(self.chk_exclusive, 1, 0, 1, 2)
        l_multi.addWidget(QLabel(share.locales.tr('Refresh:')), 2, 0)
        self.spin_refresh = QSpinBox()
        self.spin_refresh.setRange(0, 9999)
        self.spin_refresh.setFixedWidth(70)
        l_multi.addWidget(self.spin_refresh, 2, 1, alignment=Qt.AlignLeft)
        l_multi.addWidget(QLabel(share.locales.tr('Replay:')), 3, 0)
        self.spin_retry = QSpinBox()
        self.spin_retry.setRange(0, 9999)
        self.spin_retry.setFixedWidth(70)
        l_multi.addWidget(self.spin_retry, 3, 1, alignment=Qt.AlignLeft)
        self.chk_lock.setChecked(True)

        gb_default = QGroupBox(share.locales.tr('Standardtabellentyp'), tab)
        l_def = QVBoxLayout(gb_default)
        self.rb_dbase = QRadioButton('dBASE')
        self.rb_paradox = QRadioButton('Paradox')
        self.rb_sqlite3 = QRadioButton('SQLite 3')
        self.rb_mysql = QRadioButton('MySQL')
        self.rb_dbase.setChecked(True)
        l_def.addWidget(self.rb_dbase)
        l_def.addWidget(self.rb_paradox)
        l_def.addWidget(self.rb_sqlite3)
        l_def.addWidget(self.rb_mysql)

        gb_system = QGroupBox(share.locales.tr('Systemtabellen'), tab)
        l_sys = QVBoxLayout(gb_system)
        self.chk_system_show = QCheckBox(share.locales.tr('Anzeigen'))
        l_sys.addWidget(self.chk_system_show)

        gb_blocks = QGroupBox(share.locales.tr('Blockgrößen'), tab)
        l_blocks = QGridLayout(gb_blocks)
        l_blocks.setHorizontalSpacing(10)
        l_blocks.setVerticalSpacing(8)
        l_blocks.addWidget(QLabel(share.locales.tr('Indexblock:')), 0, 0)
        self.spin_indexblock = QSpinBox()
        self.spin_indexblock.setRange(1, 9999)
        self.spin_indexblock.setFixedWidth(80)
        self.spin_indexblock.setValue(1)
        l_blocks.addWidget(self.spin_indexblock, 0, 1, alignment=Qt.AlignLeft)
        l_blocks.addWidget(QLabel(share.locales.tr('Memoblock:')), 1, 0)
        self.spin_memoblock = QSpinBox()
        self.spin_memoblock.setRange(1, 9999)
        self.spin_memoblock.setFixedWidth(80)
        self.spin_memoblock.setValue(8)
        l_blocks.addWidget(self.spin_memoblock, 1, 1, alignment=Qt.AlignLeft)

        gb_other = QGroupBox(share.locales.tr('Andere'), tab)
        l_other = QGridLayout(gb_other)
        l_other.setHorizontalSpacing(10)
        l_other.setVerticalSpacing(6)
        self.chk_autosave = QCheckBox(share.locales.tr('Automatische Speicherung'))
        self.chk_deleted = QCheckBox(share.locales.tr('Löschmarken'))
        self.chk_encrypt = QCheckBox(share.locales.tr('Verschlüsselung'))
        self.chk_ident = QCheckBox(share.locales.tr('Identisch'))
        self.chk_approx = QCheckBox(share.locales.tr('Annähernd'))
        self.chk_autonull = QCheckBox(share.locales.tr('AutoNullFields'))
        self.chk_deleted.setChecked(True)
        self.chk_encrypt.setChecked(True)
        self.chk_autonull.setChecked(True)
        l_other.addWidget(self.chk_autosave, 0, 0, 1, 2)
        l_other.addWidget(self.chk_deleted, 1, 0, 1, 2)
        l_other.addWidget(self.chk_encrypt, 2, 0, 1, 2)
        l_other.addWidget(self.chk_ident, 3, 0)
        l_other.addWidget(self.chk_approx, 4, 0)
        l_other.addWidget(self.chk_autonull, 3, 1)
        self.btn_components = QPushButton(share.locales.tr('Komponententypen zuordnen...'))
        self.btn_components.setFixedWidth(220)
        l_other.addWidget(self.btn_components, 5, 0, 1, 2, alignment=Qt.AlignLeft)

        g.addWidget(gb_multi, 0, 0)
        g.addWidget(gb_blocks, 0, 1)
        g.addWidget(gb_default, 1, 0)
        g.addWidget(gb_other, 1, 1)
        g.addWidget(gb_system, 2, 0)
        g.setRowStretch(3, 1)
        g.setColumnStretch(2, 1)
        return tab

    def _build_tab_data(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        gb_kbd = QGroupBox(share.locales.tr('Tastatur'), tab)
        kbd = QGridLayout(gb_kbd)
        kbd.setHorizontalSpacing(10)
        kbd.setVerticalSpacing(8)
        self.chk_confirm = QCheckBox(share.locales.tr('Bestätigung'))
        self.chk_cua = QCheckBox(share.locales.tr('CUA-Eingabe'))
        self.chk_esc = QCheckBox(share.locales.tr('Escape'))
        self.chk_confirm.setChecked(True)
        self.chk_cua.setChecked(True)
        self.chk_esc.setChecked(True)
        kbd.addWidget(self.chk_confirm, 0, 0, 1, 2)
        kbd.addWidget(self.chk_cua, 1, 0, 1, 2)
        kbd.addWidget(self.chk_esc, 2, 0, 1, 2)
        kbd.addWidget(QLabel(share.locales.tr('Tastaturpuffer:')), 3, 0)
        self.sp_buf = QSpinBox()
        self.sp_buf.setRange(0, 9999)
        self.sp_buf.setValue(49)
        self.sp_buf.setFixedWidth(90)
        kbd.addWidget(self.sp_buf, 3, 1, alignment=Qt.AlignLeft)

        gb_other = QGroupBox(share.locales.tr('Andere'), tab)
        other = QGridLayout(gb_other)
        other.setHorizontalSpacing(10)
        other.setVerticalSpacing(8)
        other.addWidget(QLabel(share.locales.tr('Epoche:')), 0, 0)
        self.sp_epoch = QSpinBox()
        self.sp_epoch.setRange(0, 9999)
        self.sp_epoch.setValue(1950)
        self.sp_epoch.setFixedWidth(90)
        other.addWidget(self.sp_epoch, 0, 1, alignment=Qt.AlignLeft)

        gb_beep = QGroupBox(share.locales.tr('Signalton'), tab)
        beep = QGridLayout(gb_beep)
        beep.setHorizontalSpacing(10)
        beep.setVerticalSpacing(8)
        self.chk_beep = QCheckBox(share.locales.tr('Einschalten'))
        self.chk_beep.setChecked(True)
        beep.addWidget(self.chk_beep, 0, 0, 1, 2)
        beep.addWidget(QLabel(share.locales.tr('Frequenz:')), 1, 0)
        self.sp_freq = QSpinBox()
        self.sp_freq.setRange(0, 20000)
        self.sp_freq.setValue(512)
        self.sp_freq.setFixedWidth(90)
        beep.addWidget(self.sp_freq, 1, 1, alignment=Qt.AlignLeft)
        beep.addWidget(QLabel(share.locales.tr('Dauer:')), 2, 0)
        self.sp_dur = QSpinBox()
        self.sp_dur.setRange(0, 10000)
        self.sp_dur.setValue(50)
        self.sp_dur.setFixedWidth(90)
        beep.addWidget(self.sp_dur, 2, 1, alignment=Qt.AlignLeft)
        self.btn_test_beep = QPushButton(share.locales.tr('Prüfen'))
        self.btn_test_beep.setFixedWidth(95)
        beep.addWidget(self.btn_test_beep, 3, 0, 1, 2, alignment=Qt.AlignLeft)
        self.chk_beep.toggled.connect(self._toggle_data_entry_beep_controls)
        self.btn_test_beep.clicked.connect(lambda: QApplication.beep())
        self._toggle_data_entry_beep_controls(True)

        g.addWidget(gb_kbd, 0, 0)
        g.addWidget(gb_beep, 0, 1, 2, 1)
        g.addWidget(gb_other, 1, 0)
        g.setRowStretch(2, 1)
        return tab

    def _build_tab_files(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        gb_path = QGroupBox('Pfad', tab)
        path = QGridLayout(gb_path)
        path.setHorizontalSpacing(10)
        path.setVerticalSpacing(8)
        path.addWidget(QLabel(share.locales.tr('Aktuelles Verzeichnis:')), 0, 0, 1, 2)
        self.ed_files_current_dir = QLineEdit('')
        self.ed_files_current_dir.setMinimumWidth(240)
        self.btn_files_current_dir = QPushButton('...')
        self.btn_files_current_dir.setFixedWidth(30)
        path.addWidget(self.ed_files_current_dir, 1, 0)
        path.addWidget(self.btn_files_current_dir, 1, 1, alignment=Qt.AlignLeft)
        path.addWidget(QLabel(share.locales.tr('Suchpfad:')), 2, 0, 1, 2)
        self.ed_files_search_path = QLineEdit('')
        self.btn_files_search_path = QPushButton('...')
        self.btn_files_search_path.setFixedWidth(30)
        path.addWidget(self.ed_files_search_path, 3, 0)
        path.addWidget(self.btn_files_search_path, 3, 1, alignment=Qt.AlignLeft)

        gb_log = QGroupBox(share.locales.tr('Ausgabeprotokoll'), tab)
        log = QGridLayout(gb_log)
        log.setHorizontalSpacing(10)
        log.setVerticalSpacing(8)
        self.chk_enable_log = QCheckBox(share.locales.tr('Protokoll anlegen'))
        log.addWidget(self.chk_enable_log, 0, 0, 1, 2)
        log.addWidget(QLabel(share.locales.tr('Name der Protokolldatei:')), 1, 0, 1, 2)
        self.ed_logfile = QLineEdit('')
        self.btn_logfile = QPushButton('...')
        self.btn_logfile.setFixedWidth(30)
        log.addWidget(self.ed_logfile, 2, 0)
        log.addWidget(self.btn_logfile, 2, 1, alignment=Qt.AlignLeft)
        self.rb_log_overwrite = QRadioButton(share.locales.tr('Überschreiben'))
        self.rb_log_append = QRadioButton(share.locales.tr('Anhängen'))
        self.rb_log_overwrite.setChecked(True)
        log.addWidget(self.rb_log_overwrite, 3, 0, 1, 2)
        log.addWidget(self.rb_log_append, 4, 0, 1, 2)
        self.chk_enable_log.toggled.connect(self._toggle_files_log_controls)
        self.btn_logfile.clicked.connect(self._browse_log_file)

        gb_editor = QGroupBox(share.locales.tr('Editor'), tab)
        ed = QGridLayout(gb_editor)
        ed.setHorizontalSpacing(10)
        ed.setVerticalSpacing(8)
        ed.addWidget(QLabel(share.locales.tr('Externer Quelltext-Editor:')), 0, 0, 1, 2)
        self.ed_external_editor = QLineEdit('')
        self.btn_external_editor = QPushButton('...')
        self.btn_external_editor.setFixedWidth(30)
        ed.addWidget(self.ed_external_editor, 1, 0)
        ed.addWidget(self.btn_external_editor, 1, 1, alignment=Qt.AlignLeft)

        gb_other = QGroupBox(share.locales.tr('Andere'), tab)
        other = QVBoxLayout(gb_other)
        other.setSpacing(6)
        self.chk_backup = QCheckBox(share.locales.tr('Sicherungsdateien'))
        self.chk_sessions = QCheckBox(share.locales.tr('Arbeitssitzungen'))
        other.addWidget(self.chk_backup)
        other.addWidget(self.chk_sessions)

        self.btn_files_current_dir.clicked.connect(self._browse_files_current_dir)
        self.btn_files_search_path.clicked.connect(self._browse_files_search_path)
        self.btn_external_editor.clicked.connect(self._browse_external_editor)
        self._toggle_files_log_controls(False)

        g.addWidget(gb_path, 0, 0)
        g.addWidget(gb_editor, 0, 1)
        g.addWidget(gb_log, 1, 0)
        g.addWidget(gb_other, 1, 1)
        g.setRowStretch(2, 1)
        return tab

    def _build_tab_app(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        gb_exp = QGroupBox(share.locales.tr('Experten anzeigen'), tab)
        exp = QVBoxLayout(gb_exp)
        exp.setSpacing(6)
        self.chk_app_form = QCheckBox(share.locales.tr('Formular'))
        self.chk_app_report = QCheckBox(share.locales.tr('Report'))
        self.chk_app_labels = QCheckBox(share.locales.tr('Etiketten'))
        self.chk_app_datamodule = QCheckBox(share.locales.tr('Datenmodul'))
        self.chk_app_table = QCheckBox(share.locales.tr('Tabelle'))
        for c in (self.chk_app_form, self.chk_app_report, self.chk_app_labels, self.chk_app_datamodule, self.chk_app_table):
            c.setChecked(True)
            exp.addWidget(c)

        gb_file = QGroupBox(share.locales.tr('Dateimenü'), tab)
        fm = QGridLayout(gb_file)
        fm.setHorizontalSpacing(10)
        fm.setVerticalSpacing(8)
        fm.addWidget(QLabel(share.locales.tr('Anzahl Dateien:')), 0, 0)
        self.sp_app_files = QSpinBox()
        self.sp_app_files.setRange(0, 99)
        self.sp_app_files.setValue(5)
        self.sp_app_files.setFixedWidth(80)
        fm.addWidget(self.sp_app_files, 0, 1, alignment=Qt.AlignLeft)
        fm.addWidget(QLabel(share.locales.tr('Anzahl Projekte:')), 1, 0)
        self.sp_app_projects = QSpinBox()
        self.sp_app_projects.setRange(0, 99)
        self.sp_app_projects.setValue(5)
        self.sp_app_projects.setFixedWidth(80)
        fm.addWidget(self.sp_app_projects, 1, 1, alignment=Qt.AlignLeft)

        gb_db = QGroupBox(share.locales.tr('Datenbank'), tab)
        db = QVBoxLayout(gb_db)
        db.setSpacing(6)
        self.chk_app_save_logins = QCheckBox(share.locales.tr('Anmeldungen sichern'))
        self.chk_app_sql_trace = QCheckBox(share.locales.tr('SQL-Ablaufverfolgung'))
        self.chk_app_save_logins.setChecked(True)
        db.addWidget(self.chk_app_save_logins)
        db.addWidget(self.chk_app_sql_trace)

        gb_win = QGroupBox(share.locales.tr('Fenster'), tab)
        win = QVBoxLayout(gb_win)
        win.setSpacing(6)
        self.chk_app_fit = QCheckBox(share.locales.tr('Fenstergröße an Inhalt anpassen'))
        self.chk_app_anim = QCheckBox(share.locales.tr('Animationen endlos abspielen'))
        self.chk_app_ole = QCheckBox(share.locales.tr('Objekte als OLE 2.0 speichern'))
        self.chk_app_fit.setChecked(True)
        self.chk_app_anim.setChecked(True)
        self.chk_app_ole.setChecked(True)
        win.addWidget(self.chk_app_fit)
        win.addWidget(self.chk_app_anim)
        win.addWidget(self.chk_app_ole)

        gb_other = QGroupBox(share.locales.tr('Andere'), tab)
        other = QVBoxLayout(gb_other)
        other.setSpacing(6)
        self.chk_app_splash = QCheckBox(share.locales.tr('Startbildschirm'))
        self.chk_app_splash.setChecked(True)
        other.addWidget(self.chk_app_splash)

        g.addWidget(gb_exp, 0, 0)
        g.addWidget(gb_db, 0, 1)
        g.addWidget(gb_file, 1, 0)
        g.addWidget(gb_win, 1, 1)
        g.addWidget(gb_other, 2, 1)
        g.setRowStretch(3, 1)
        return tab

    def _build_tab_prog(self) -> QWidget:
        tab = QWidget()
        g = QGridLayout(tab)
        g.setContentsMargins(12, 12, 12, 12)
        g.setHorizontalSpacing(18)
        g.setVerticalSpacing(12)

        gb_out = QGroupBox(share.locales.tr('Befehlsausgabe'), tab)
        out = QGridLayout(gb_out)
        out.setHorizontalSpacing(10)
        out.setVerticalSpacing(8)
        out.addWidget(QLabel(share.locales.tr('Dezimalstellen:')), 0, 0)
        self.sp_prog_decimals = QSpinBox()
        self.sp_prog_decimals.setRange(0, 20)
        self.sp_prog_decimals.setValue(2)
        self.sp_prog_decimals.setFixedWidth(80)
        out.addWidget(self.sp_prog_decimals, 0, 1, alignment=Qt.AlignLeft)
        out.addWidget(QLabel(share.locales.tr('Genauigkeit:')), 1, 0)
        self.sp_prog_precision = QSpinBox()
        self.sp_prog_precision.setRange(0, 20)
        self.sp_prog_precision.setValue(10)
        self.sp_prog_precision.setFixedWidth(80)
        out.addWidget(self.sp_prog_precision, 1, 1, alignment=Qt.AlignLeft)
        out.addWidget(QLabel(share.locales.tr('Rand:')), 2, 0)
        self.sp_prog_margin = QSpinBox()
        self.sp_prog_margin.setRange(0, 999)
        self.sp_prog_margin.setValue(0)
        self.sp_prog_margin.setFixedWidth(80)
        out.addWidget(self.sp_prog_margin, 2, 1, alignment=Qt.AlignLeft)
        self.chk_prog_blank = QCheckBox(share.locales.tr('Leerzeichen'))
        self.chk_prog_trace = QCheckBox(share.locales.tr('Ablaufverfolgung'))
        self.chk_prog_fieldnames = QCheckBox(share.locales.tr('Feldnamen'))
        self.chk_prog_blank.setChecked(True)
        self.chk_prog_fieldnames.setChecked(True)
        out.addWidget(self.chk_prog_blank, 3, 0, 1, 2)
        out.addWidget(self.chk_prog_trace, 4, 0, 1, 2)
        out.addWidget(self.chk_prog_fieldnames, 5, 0, 1, 2)

        gb_dev = QGroupBox(share.locales.tr('Programmentwicklung'), tab)
        dev = QGridLayout(gb_dev)
        dev.setHorizontalSpacing(10)
        dev.setVerticalSpacing(8)
        self.chk_prog_fulltest = QCheckBox(share.locales.tr('Volltest'))
        self.chk_prog_buildtime = QCheckBox(share.locales.tr('Erstellungszeit'))
        self.chk_prog_buildtime.setChecked(True)
        dev.addWidget(self.chk_prog_fulltest, 0, 0, 1, 2)
        dev.addWidget(self.chk_prog_buildtime, 1, 0, 1, 2)

        gb_other = QGroupBox(share.locales.tr('Andere'), tab)
        other = QGridLayout(gb_other)
        other.setHorizontalSpacing(10)
        other.setVerticalSpacing(8)
        self.chk_prog_design = QCheckBox(share.locales.tr('Design'))
        self.chk_prog_high_precision = QCheckBox(share.locales.tr('High Precision'))
        self.chk_prog_protect = QCheckBox(share.locales.tr('Änderungsschutz'))
        self.chk_prog_fullpath = QCheckBox(share.locales.tr('Vollständige Pfadangabe'))
        self.chk_prog_design.setChecked(True)
        self.chk_prog_protect.setChecked(True)
        other.addWidget(self.chk_prog_design, 0, 0)
        other.addWidget(self.chk_prog_high_precision, 0, 1)
        other.addWidget(self.chk_prog_protect, 1, 0, 1, 2)
        other.addWidget(self.chk_prog_fullpath, 2, 0, 1, 2)

        gb_err = QGroupBox(share.locales.tr('Error Handling'), tab)
        err = QGridLayout(gb_err)
        err.setHorizontalSpacing(10)
        err.setVerticalSpacing(8)
        err.addWidget(QLabel(share.locales.tr('Error Action:')), 0, 0)
        self.cb_prog_error_action = QComboBox()
        self.cb_prog_error_action.addItems(['0 - Ignore', '1 - Message', '2 - Log', '3 - Abort', '4 - Show Error Dialog'])
        self.cb_prog_error_action.setCurrentText('4 - Show Error Dialog')
        self.cb_prog_error_action.setMinimumWidth(260)
        err.addWidget(self.cb_prog_error_action, 0, 1, 1, 2)
        err.addWidget(QLabel(share.locales.tr('Error Log File:')), 1, 0)
        self.ed_prog_error_log = QLineEdit('PLUSerr.log')
        err.addWidget(self.ed_prog_error_log, 1, 1)
        self.btn_prog_error_log = QPushButton('...')
        self.btn_prog_error_log.setFixedWidth(28)
        err.addWidget(self.btn_prog_error_log, 1, 2, alignment=Qt.AlignLeft)
        err.addWidget(QLabel(share.locales.tr('Maximum Size:')), 2, 0)
        self.sp_prog_max_size = QSpinBox()
        self.sp_prog_max_size.setRange(0, 999999)
        self.sp_prog_max_size.setValue(100)
        self.sp_prog_max_size.setFixedWidth(90)
        err.addWidget(self.sp_prog_max_size, 2, 1, alignment=Qt.AlignLeft)
        err.addWidget(QLabel(share.locales.tr('Kilobytes')), 2, 2, alignment=Qt.AlignLeft)
        err.addWidget(QLabel(share.locales.tr('HTML Error Template:')), 3, 0)
        self.ed_prog_html_template = QLineEdit('error.htm')
        err.addWidget(self.ed_prog_html_template, 3, 1)
        self.btn_prog_html_template = QPushButton('...')
        self.btn_prog_html_template.setFixedWidth(28)
        err.addWidget(self.btn_prog_html_template, 3, 2, alignment=Qt.AlignLeft)
        self.btn_prog_error_log.clicked.connect(self._browse_programming_error_log)
        self.btn_prog_html_template.clicked.connect(self._browse_programming_html_template)

        g.addWidget(gb_out, 0, 0)
        g.addWidget(gb_dev, 0, 1)
        g.addWidget(gb_other, 1, 1)
        g.addWidget(gb_err, 2, 0, 1, 2)
        g.setRowStretch(3, 1)
        return tab

    def _help(self):
        QMessageBox.information(self, share.locales.tr('Help'), 'Hier könnte deine Hilfe stehen :)')

    def reject(self):
        super().reject()


# ---------------------------------------------------------------------------
# Formular-Designer Dock (Objektinspector + Werkzeugpalette)

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Ein einfacher Key-Value Editor (2 Spalten).
# ---------------------------------------------------------------------------
class _KeyValueTree(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHeaderLabels(["Name", "Wert"])
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        self.setRootIsDecorated(True)

# ---------------------------------------------------------------------------
# Werkzeug-Palette (links unten):
# - 3 Tabs (Standard/Datenzugriff/Individuell)
# - pro Tab ein IconView (QListWidget)
# - bei Auswahl wird toolSelected(tool_name) emittiert
# ---------------------------------------------------------------------------
class _ToolPalette(QTabWidget):
    toolSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabPosition(QTabWidget.North)

        self.std = self._make_icon_view()
        self.data = self._make_icon_view()
        self.custom = self._make_icon_view()

        self.addTab(self.std,    share.locales.tr("Standard"))
        self.addTab(self.data,   share.locales.tr("Datenzugriff"))
        self.addTab(self.custom, share.locales.tr("Individuell"))

        self._fill_defaults()

        # Click -> Werkzeug setzen
        for view in (self.std, self.data, self.custom):
            view.itemClicked.connect(self._on_item_clicked)

        self._current_tool = ""

    def current_tool(self) -> str:
        return self._current_tool or ""

    def clear_selection(self) -> None:
        for view in (self.std, self.data, self.custom):
            view.clearSelection()
        self._current_tool = ""
        self.toolSelected.emit("")

    def _on_item_clicked(self, item: QListWidgetItem):
        name = (item.text() or "").strip()
        self._current_tool = name
        self.toolSelected.emit(name)

    def _make_icon_view(self) -> QListWidget:
        lw = QListWidget(self)
        lw.setViewMode(QListWidget.IconMode)
        lw.setResizeMode(QListWidget.Adjust)
        lw.setMovement(QListWidget.Static)
        lw.setWrapping(True)
        lw.setWordWrap(True)
        lw.setSelectionMode(QListWidget.SingleSelection)
        lw.setIconSize(QSize(32, 32))
        lw.setGridSize(QSize(110, 70))
        lw.setSpacing(8)
        return lw

    def _add(self, lw: QListWidget, text: str, icon: QIcon | None = None):
        it = QListWidgetItem(text)
        if icon is not None and not icon.isNull():
            it.setIcon(icon)
        lw.addItem(it)

    def _fill_defaults(self):
        ip = QFileIconProvider()

        # Standard Controls
        self._add(self.std, "Label",     ip.icon(QFileIconProvider.File))
        self._add(self.std, "Button",    ip.icon(QFileIconProvider.File))
        self._add(self.std, "LineEdit",  ip.icon(QFileIconProvider.File))
        self._add(self.std, "TextEdit",  ip.icon(QFileIconProvider.File))
        self._add(self.std, "CheckBox",  ip.icon(QFileIconProvider.File))
        self._add(self.std, "ComboBox",  ip.icon(QFileIconProvider.File))
        self._add(self.std, "ListBox",   ip.icon(QFileIconProvider.File))
        self._add(self.std, "GroupBox",  ip.icon(QFileIconProvider.File))
        self._add(self.std, "TabWidget", ip.icon(QFileIconProvider.File))

        # Datenzugriff (Platzhalter/Start)
        self._add(self.data, "TableView",  ip.icon(QFileIconProvider.File))
        self._add(self.data, "TreeView",   ip.icon(QFileIconProvider.File))
        self._add(self.data, "DataSource", ip.icon(QFileIconProvider.File))

        # Individuell (Platzhalter)
        self._add(self.custom, "CustomControl", ip.icon(QFileIconProvider.File))

class DockTitleBar(QWidget):
    def __init__(self, dock: QDockWidget, title: str = "", parent=None):
        super().__init__(parent)
        self.dock = dock

        lay = QHBoxLayout(self)
        lay.setContentsMargins(8, 2, 6, 2)
        lay.setSpacing(6)

        self.lbl = QLabel(title or dock.windowTitle(), self)
        self.lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Float (andocken/abdocken)
        self.btnFloat = QToolButton(self)
        self.btnFloat.setAutoRaise(True)
        self.btnFloat.clicked.connect(self._toggle_floating)

        # Close
        self.btnClose = QToolButton(self)
        self.btnClose.setAutoRaise(True)
        self.btnClose.clicked.connect(dock.close)

        lay.addWidget(self.lbl)
        lay.addWidget(self.btnFloat)
        lay.addWidget(self.btnClose)

        # initial
        self._sync_icons()

        # Wenn der Dock-Zustand wechselt, Icon anpassen
        dock.topLevelChanged.connect(lambda _: self._sync_icons())

        # Styling direkt hier (oder per globalem QSS, s.u.)
        self.setStyleSheet("""
            DockTitleBar {
                background: #1e1e1e;
            }
            QLabel {
                color: #ffd866;           /* GELB */
                font-weight: 600;
            }
            QToolButton {
                color: #ffffff;           /* WEISS (falls Text/Icon-Font) */
                background: transparent;
                border: none;
                padding: 2px;
            }
            QToolButton:hover {
                background: rgba(255,255,255,0.10);
                border-radius: 3px;
            }
        """)

    def setTitle(self, text: str):
        self.lbl.setText(text)

    def _toggle_floating(self):
        self.dock.setFloating(not self.dock.isFloating())
        self._sync_icons()

    def _sync_icons(self):
        # NIMM HIER DEINE WEISSEN PNG/SVG ICONS (empfohlen)
        # Beispiel: Ressourcenpfade anpassen:
        if self.dock.isFloating():
            self.btnFloat.setIcon(QIcon(":/icons/dock_white.png"))   # andocken
        else:
            self.btnFloat.setIcon(QIcon(":/icons/undock_white.png")) # abdocken
        self.btnClose.setIcon(QIcon(":/icons/close_white.png"))

def apply_custom_dock_titlebar(dock: QDockWidget):
    tb = DockTitleBar(dock)
    dock.setTitleBarWidget(tb)

    # Optional: damit dein Titel immer sync bleibt
    dock.windowTitleChanged.connect(tb.setTitle)

# ---------------------------------------------------------------------------
# Dock: Objekt-Inspector (oben links).
# ---------------------------------------------------------------------------
class ObjectInspectorDock(QDockWidget):
    def __init__(self, main_window: "MainWindow", parent=None):
        super().__init__(share.locales.tr("Object Inspector"), parent)
        self.main_window = main_window
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.setStyleSheet("color: #ffff00;")

        inspector = ObjectInspectorPanel(main_window)
        main_window.object_inspector = inspector
        self.setWidget(inspector)

# ---------------------------------------------------------------------------
# Dock: Objektpalette (unten links).
# ---------------------------------------------------------------------------
class ObjectPaletteDock(QDockWidget):
    def __init__(self, main_window: "MainWindow", parent=None):
        super().__init__(share.locales.tr("Object Palette"), parent)
        self.main_window = main_window
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.setStyleSheet("color: #ffff00;")

        # Reuse vorhandene _ToolPalette, sonst minimaler Stub
        try:
            palette = _ToolPalette(self)
            try:
                palette.toolSelected.connect(self.main_window.set_designer_tool)
            except Exception:
                pass
        except Exception:
            palette = QWidget(self)
            lay = QVBoxLayout(palette)
            lay.addWidget(QLabel(share.locales.tr("ToolPalette nicht verfügbar"), palette))

        self.setWidget(palette)

# ---------------------------------------------------------------------------
# Design-Time Wrapper:
# - enthält ein echtes Qt-Control (inner)
# - zeichnet Auswahlrahmen + 8 Resize-Handles (außen am Rand)
# - Move + Resize mit Grid-Snap
# - inner ist mouse-transparent, damit Klicks immer den Wrapper selektieren
# ---------------------------------------------------------------------------

def _find_form_designer_host(widget):
    cur = widget
    while cur is not None:
        if hasattr(cur, "_action_load_form") and hasattr(cur, "_action_save_form") and hasattr(cur, "_action_save_form_as"):
            return cur
        try:
            cur = cur.parent()
        except Exception:
            cur = None
    return None



class DesignerControl(QWidget):
    HANDLE_SIZE = 7
    MARGIN = HANDLE_SIZE  # Platz für "außenliegende" Handles

    def __init__(self, tool_name: str, parent_canvas: "PixelGridCanvas", rect: QRect):
        super().__init__(parent_canvas)
        self.tool_name = (tool_name or "").strip() or "Control"

        self.instance_name = ''  # z.B. Label1
        self._selected = False

        self.setMouseTracking(True)
        # Opaque Hintergrund, damit überlappende Controls das darunterliegende NICHT durchscheinen lassen:
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background: rgb(55,55,55);")

        # echtes Control als Kind
        self.inner = self._create_inner(self.tool_name)
        self.inner.setParent(self)
        # Proxy: inner bekommt keine Mouse-Events, der Wrapper fängt alles ab
        self.inner.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # initiale Geometrie:
        # rect ist die "Content"-Geometrie (das sichtbare Control), Wrapper wird um MARGIN erweitert.
        m = int(self.MARGIN)
        outer = QRect(rect.x() - m, rect.y() - m, rect.width() + 2 * m, rect.height() + 2 * m).normalized()
        if outer.x() < 0:
            outer.moveLeft(0)
        if outer.y() < 0:
            outer.moveTop(0)
        self.setGeometry(outer)

        self._content_w = max(16, rect.width())
        self._content_h = max(16, rect.height())
        self._sync_inner()

        # Drag state
        self._drag_mode = ""     # "", "move", "resize"
        self._resize_handle = -1
        self._press_pos = QPoint()
        self._press_global = QPoint()
        self._start_outer = QRect()
        self._start_content_global = QRect()

    def _snap(self, v: int) -> int:
        try:
            g = int(getattr(self.parent(), "grid", 8))
        except Exception:
            g = 8
        g = max(2, g)
        return int(round(v / g) * g)
        
    def _content_rect(self) -> QRect:
        m = int(self.MARGIN)
        return QRect(m, m, int(self._content_w), int(self._content_h))

    def _content_rect_global(self) -> QRect:
        g = self.geometry()
        m = int(self.MARGIN)
        return QRect(g.x() + m, g.y() + m, int(self._content_w), int(self._content_h))

    def _sync_inner(self):
        r = self._content_rect()
        self.inner.setGeometry(r)

    def set_selected(self, sel: bool):
        self._selected = bool(sel)
        self.update()

    def _create_inner(self, name: str) -> QWidget:
        n = (name or "").strip().lower()
        if n in ("button", "pushbutton"):
            w = QPushButton("Button")
        elif n in ("label",):
            w = QLabel("Label")
            w.setAlignment(Qt.AlignCenter)
        elif n in ("lineedit", "edit", "textbox"):
            w = QLineEdit("")
        elif n in ("checkbox",):
            w = QCheckBox("CheckBox")
        elif n in ("combobox",):
            w = QComboBox()
            w.addItems(["Item 1", "Item 2"])
        elif n in ("listbox", "listwidget"):
            w = QListWidget()
            w.addItem("Item")
        else:
            w = QLabel(name or "Control")
            w.setAlignment(Qt.AlignCenter)

        # Inner selbst soll nicht transparent sein (sonst schimmert es):
        try:
            w.setStyleSheet("background: rgb(75,75,75);")
        except Exception:
            pass
        return w

    def _snap(self, v: int) -> int:
        try:
            g = int(getattr(self.parent(), "grid", 8))
        except Exception:
            g = 8
        g = max(2, g)
        return int(round(v / g) * g)

    def _handle_rects(self):
        s = int(self.HANDLE_SIZE)
        half = s // 2
        r = self._content_rect()
        cx = r.center().x()
        cy = r.center().y()
        # 0..7: TL, T, TR, R, BR, B, BL, L (Uhrzeigersinn)
        return [
            QRect(r.left() - half,  r.top() - half, s, s),
            QRect(cx - half,        r.top() - half, s, s),
            QRect(r.right() - half, r.top() - half, s, s),
            QRect(r.right() - half, cy - half, s, s),
            QRect(r.right() - half, r.bottom() - half, s, s),
            QRect(cx - half,        r.bottom() - half, s, s),
            QRect(r.left() - half,  r.bottom() - half, s, s),
            QRect(r.left() - half,  cy - half, s, s),
        ]

    def _hit_handle(self, pos: QPoint) -> int:
        for i, hr in enumerate(self._handle_rects()):
            if hr.contains(pos):
                return i
        return -1

    def _cursor_for_handle(self, h: int):
        # TL/BR -> diag1, TR/BL -> diag2, T/B -> vert, L/R -> horiz
        if h in (0, 4):
            return Qt.SizeFDiagCursor
        if h in (2, 6):
            return Qt.SizeBDiagCursor
        if h in (1, 5):
            return Qt.SizeVerCursor
        if h in (3, 7):
            return Qt.SizeHorCursor
        return Qt.ArrowCursor

    def paintEvent(self, ev):
        # Opaque Hintergrund (überdeckt darunterliegende Controls bei Überlappung)
        p = QPainter(self)
        p.fillRect(self.rect(), QColor(55, 55, 55))
        p.end()

        super().paintEvent(ev)
        self._draw_instance_name()

        if not self._selected:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False)

        cr = self._content_rect()

        # Auswahlrahmen (um das Content-Rect)
        pen = QPen(QColor(255, 216, 102))
        pen.setStyle(Qt.DashLine)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(cr.adjusted(0, 0, -1, -1))

        # Handles (außen am Rand)
        p.setPen(QPen(QColor(255, 216, 102)))
        for hr in self._handle_rects():
            p.fillRect(hr, QColor(255, 216, 102))
            p.drawRect(hr.adjusted(0, 0, -1, -1))

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            # aktivieren
            try:
                self.parent().set_active(self)
            except Exception:
                pass

            self._press_pos = ev.pos()
            self._press_global = ev.globalPos()
            self._start_outer = self.geometry()
            self._start_content_global = self._content_rect_global()

            h = self._hit_handle(ev.pos())
            if h >= 0 and self._selected:
                self._drag_mode = "resize"
                self._resize_handle = h
            else:
                # Click im Content => Move
                if self._content_rect().contains(ev.pos()):
                    self._drag_mode = "move"
                else:
                    self._drag_mode = ""
                self._resize_handle = -1

            ev.accept()
            return
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        # Hover-Cursor (wenn nicht drag)
        if not self._drag_mode:
            if self._selected:
                h = self._hit_handle(ev.pos())
                if h >= 0:
                    self.setCursor(self._cursor_for_handle(h))
                elif self._content_rect().contains(ev.pos()):
                    self.setCursor(Qt.SizeAllCursor)
                else:
                    self.unsetCursor()
            else:
                self.unsetCursor()
            super().mouseMoveEvent(ev)
            return

        delta = ev.globalPos() - self._press_global

        # Move (snap am Content-Rect)
        if self._drag_mode == "move":
            cg = QRect(self._start_content_global)
            nx = cg.x() + delta.x()
            ny = cg.y() + delta.y()
            m = int(self.MARGIN)
            self.setGeometry(nx - m, ny - m, self.width(), self.height())
            self.update()
            ev.accept()
            return

        # Resize (snap an Content-Rect)
        if self._drag_mode == "resize":
            minw, minh = 16, 16
            g = QRect(self._start_content_global)

            x, y, w, h = g.x(), g.y(), g.width(), g.height()
            dx, dy = delta.x(), delta.y()

            # TL
            if self._resize_handle == 0:
                x = g.x() + dx
                y = g.y() + dy
                w = g.right() - x + 1
                h = g.bottom() - y + 1
            # T
            elif self._resize_handle == 1:
                y = g.y() + dy
                h = g.bottom() - y + 1
            # TR
            elif self._resize_handle == 2:
                y = g.y() + dy
                w = g.width() + dx
                h = g.bottom() - y + 1
            # R
            elif self._resize_handle == 3:
                w = g.width() + dx
            # BR
            elif self._resize_handle == 4:
                w = g.width() + dx
                h = g.height() + dy
            # B
            elif self._resize_handle == 5:
                h = g.height() + dy
            # BL
            elif self._resize_handle == 6:
                x = g.x() + dx
                w = g.right() - x + 1
                h = g.height() + dy
            # L
            elif self._resize_handle == 7:
                x = g.x() + dx
                w = g.right() - x + 1

            w = max(minw, int(w))
            h = max(minh, int(h))

            m = int(self.MARGIN)
            self._content_w = w
            self._content_h = h
            self.setGeometry(int(x) - m, int(y) - m, w + 2 * m, h + 2 * m)
            self._sync_inner()
            self.update()
            ev.accept()
            return

        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton and self._drag_mode:
            # Sanfter Drag: erst beim Loslassen auf Grid snappen
            try:
                cg = self._content_rect_global()
                sx = self._snap(cg.x())
                sy = self._snap(cg.y())
                sw = max(16, self._snap(cg.width()))
                sh = max(16, self._snap(cg.height()))
                m = int(self.MARGIN)
                self._content_w = sw
                self._content_h = sh
                self.setGeometry(int(sx) - m, int(sy) - m, int(sw) + 2*m, int(sh) + 2*m)
                self._sync_inner()
                self.update()
                # Canvas + Objektinspektor aktualisieren
                try:
                    if hasattr(self.parent(), 'update_canvas_size'):
                        self.parent().update_canvas_size()
                except Exception:
                    pass
                try:
                    mw = getattr(self.parent(), 'main_window', None) or self.window()
                    oi = getattr(mw, 'object_inspector', None) if mw is not None else None
                    if oi is not None and getattr(oi, '_current_ctrl', None) is self:
                        oi._refresh_properties()
                except Exception:
                    pass
            except Exception:
                pass
            self._drag_mode = ""
            self._resize_handle = -1
            self.unsetCursor()
            ev.accept()
            return
        super().mouseReleaseEvent(ev)



    def _draw_instance_name(self):
        name = getattr(self, "instance_name", "")
        if not name:
            return
        try:
            p = QPainter(self)
            p.setPen(QPen(QColor(230, 230, 230)))
            p.drawText(self._content_rect(), Qt.AlignCenter, name)
        except Exception:
            pass



    def contextMenuEvent(self, ev):
        # Komponenten-Kontextmenü
        try:
            self.parent().set_active(self)
        except Exception:
            pass

        menu = QMenu(self)

        act_help = QAction(share.locales.tr("Hilfe\tF1"), self)
        act_help.setShortcut("F1")
        act_help.triggered.connect(lambda: QMessageBox.information(self,
            share.locales.tr("Hilfe"), f"{share.locales.tr("Komponente")}: {self.tool_name}"))
        menu.addAction(act_help)

        menu.addSeparator()

        host = _find_form_designer_host(self)

        act_load_form = QAction(share.locales.tr("Laden"), self)
        act_load_form.triggered.connect(lambda: getattr(host, "_action_load_form", lambda: None)())
        menu.addAction(act_load_form)

        act_save_form = QAction(share.locales.tr("Speichern"), self)
        act_save_form.triggered.connect(lambda: getattr(host, "_action_save_form", lambda: None)())
        menu.addAction(act_save_form)

        act_save_form_as = QAction(share.locales.tr("Speichern unter..."), self)
        act_save_form_as.triggered.connect(lambda: getattr(host, "_action_save_form_as", lambda: None)())
        menu.addAction(act_save_form_as)

        menu.addSeparator()

        act_edit = QAction(share.locales.tr("Bearbeiten"), self)
        act_edit.triggered.connect(self._action_edit)
        menu.addAction(act_edit)

        act_rename = QAction(share.locales.tr("Umbenennen"), self)
        act_rename.triggered.connect(self._action_rename)
        menu.addAction(act_rename)

        menu.addSeparator()

        act_copy = QAction(share.locales.tr("Kopieren"), self)
        act_copy.triggered.connect(lambda: self._clipboard_copy(cut=False))
        menu.addAction(act_copy)

        act_cut = QAction(share.locales.tr("Ausschneiden"), self)
        act_cut.triggered.connect(lambda: self._clipboard_copy(cut=True))
        menu.addAction(act_cut)

        act_del = QAction(share.locales.tr("Entfernen/Löschen"), self)
        act_del.triggered.connect(self._action_delete)
        menu.addAction(act_del)

        menu.addSeparator()

        act_paste = QAction(share.locales.tr("Einfügen"), self)
        act_paste.setEnabled(bool(getattr(self.parent(), "_designer_clip", None)))
        act_paste.triggered.connect(lambda: self.parent().paste_from_clipboard(ev.globalPos()))
        menu.addAction(act_paste)

        menu.exec_(ev.globalPos())



    def _action_edit(self):
        # Öffnet den CodeEditor + springt zur Komponente/Handler-Stelle (best-effort)
        try:
            mw = getattr(self.parent(), "main_window", None) or self.window()
            w = None

            # MainWindow-API: bevorzugt ensure_code_editor_window (öffnet FileEditorWindow)
            if hasattr(mw, "ensure_code_editor_window"):
                w = mw.ensure_code_editor_window(focus=True)
            # ältere/alternative Helper
            if w is None and hasattr(mw, "_get_or_create_file_editor_window"):
                w = mw._get_or_create_file_editor_window()
            # Fallbacks (falls noch irgendwo vorhanden)
            if w is None and hasattr(mw, "mdi_open_code_editor"):
                w = mw.mdi_open_code_editor()
            if w is None and hasattr(mw, "mdi_open_editor"):
                w = mw.mdi_open_editor()
            if w is not None and hasattr(mw, "jump_to_symbol"):
                mw.jump_to_symbol(self.instance_name or self.tool_name)
        except Exception as e:
            QMessageBox.warning(self, "Bearbeiten", str(e))

    def _action_rename(self):
        base = (self.tool_name or "Control").strip() or "Control"
        new_name, ok = QInputDialog.getText(self,
            share.locales.tr("Umbenennen"),
            share.locales.tr("Neuer Name:"),
            text=(self.instance_name or base))
        if not ok:
            return
        new_name = (new_name or "").strip()
        if not new_name:
            return
        try:
            if hasattr(self.parent(), "is_name_used") and self.parent().is_name_used(new_name, except_ctrl=self):
                QMessageBox.warning(self,
                    share.locales.tr("Umbenennen"),
                    share.locales.tr("Name wird bereits verwendet."))
                return
        except Exception:
            pass
        self.instance_name = new_name
        self.update()


    def _action_delete(self):
        try:
            self.parent().delete_control(self)
        except Exception:
            self.deleteLater()


    def _clipboard_copy(self, cut: bool = False):
        try:
            self.parent().copy_to_clipboard(self, cut=cut)
        except Exception as e:
            QMessageBox.warning(self, share.locales.tr("Clipboard"), str(e))

# ---------------------------------------------------------------------------
# Designer-Fläche mit Pixelgrid + Platzieren von DesignerControl.
#
# Workflow:
# - In der Palette ein Tool anklicken (z.B. 'Button')
# - Im Canvas: LMB drücken/ziehen -> Rahmen (RubberBand)
# - LMB loslassen -> Control wird erzeugt
# - Control: klicken = aktiv, ziehen = verschieben, Handles = resize
# ---------------------------------------------------------------------------
class PixelGridCanvas(QWidget):
    def __init__(self, main_window: "MainWindow", parent=None):
        super().__init__(parent)
        # Referenz auf MainWindow (für Objektinspektor-Sync)
        self.main_window = getattr(parent, "main_window", None) if 'parent' in locals() else None
        if self.main_window is None:
            try:
                self.main_window = self.window()
            except Exception:
                self.main_window = None
        self.main_window = main_window

        self.grid = 8
        self.show_origin = True
        self.setMinimumSize(2400, 2300)
        self.setAutoFillBackground(True)
        self.setMouseTracking(True)

        self.setFocusPolicy(Qt.StrongFocus)
        self._tool_counters = {}
        self._controls = []
        self._active = None
        self._designer_clip = None
        self._base_design_size = QSize(2048, 2048)
        self._scroll_area = None

        self._rubber = QRubberBand(QRubberBand.Rectangle, self)
        self._rubber.hide()
        self._drag_start = QPoint()

        self._active: DesignerControl | None = None

    def set_active(self, ctrl: 'DesignerControl | None') -> None:
        if self._active is ctrl:
            return

        if self._active is not None:
            try:
                self._active.set_selected(False)
            except Exception:
                pass

        self._active = ctrl

        if ctrl is not None:
            try:
                ctrl.set_selected(True)
                ctrl.raise_()
                ctrl.setFocus()
            except Exception:
                pass

        # Objektinspektor synchronisieren
        try:
            mw = getattr(self, "main_window", None) or self.window()
            if mw is not None and hasattr(mw, "on_designer_selection_changed"):
                mw.on_designer_selection_changed(ctrl)
        except Exception:
            pass

        self.update()

    def on_designer_selection_changed(self, ctrl):
        try:
            oi = getattr(self, "object_inspector", None)
            if oi is not None:
                oi.set_current(ctrl)
        except Exception:
            pass


    def on_designer_controls_changed(self, controls):
        try:
            self.designer_controls = list(controls or [])
        except Exception:
            self.designer_controls = []
        try:
            oi = getattr(self, "object_inspector", None)
            if oi is not None:
                oi.set_controls_list(self.designer_controls)
        except Exception:
            pass

    def _snap(self, v: int) -> int:
        try:
            g = int(getattr(self.parent(), "grid", 8))
        except Exception:
            g = 8
        g = max(2, g)
        return int(round(v / g) * g)

    def _snap_point(self, p: QPoint) -> QPoint:
        g = max(2, int(self.grid))
        x = int(round(p.x() / g) * g)
        y = int(round(p.y() / g) * g)
        return QPoint(x, y)

    def _snap_rect(self, r: QRect) -> QRect:
        tl = self._snap_point(r.topLeft())
        br = self._snap_point(r.bottomRight())
        rr = QRect(tl, br).normalized()
        # Mindestgröße
        if rr.width() < 16:
            rr.setWidth(16)
        if rr.height() < 16:
            rr.setHeight(16)
        return rr

    def _current_tool(self) -> str:
        try:
            return (getattr(self.main_window, "designer_current_tool", "") or "").strip()
        except Exception:
            return ""

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            # Klick auf bestehendes Control? (dann macht das Control selbst Selection)
            if self.childAt(ev.pos()) is not None:
                super().mousePressEvent(ev)
                return

            tool = self._current_tool()
            if tool:
                self._drag_start = self._snap_point(ev.pos())
                self._rubber.setGeometry(QRect(self._drag_start, QSize()))
                self._rubber.show()
                ev.accept()
                return

            # kein Tool: Klick in freie Fläche -> deselect
            self.set_active(None)
            ev.accept()
            return

        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._rubber.isVisible():
            cur = self._snap_point(ev.pos())
            self._rubber.setGeometry(QRect(self._drag_start, cur).normalized())
            ev.accept()
            return
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton and self._rubber.isVisible():
            self._rubber.hide()
            r = self._snap_rect(self._rubber.geometry())

            tool = self._current_tool()
            if tool and r.width() >= 16 and r.height() >= 16:
                ctrl = DesignerControl(tool, self, r)
                ctrl.show()
                if ctrl not in self._controls:
                    self._controls.append(ctrl)
                try:
                    mw = getattr(self, "main_window", None) or self.window()
                    if mw is not None and hasattr(mw, "on_designer_controls_changed"):
                        mw.on_designer_controls_changed(self._controls)
                except Exception:
                    pass
                self.set_active(ctrl)
                self.update_canvas_size()
                self.ensure_visible_control(ctrl)
            ev.accept()
            return
        super().mouseReleaseEvent(ev)

    def paintEvent(self, ev):
        super().paintEvent(ev)
        p = QPainter(self)
        r = self.rect()

        # Hintergrund (Palette Window)
        bg = self.palette().color(QPalette.Window)
        p.fillRect(r, bg)

        # Grid
        pen = QPen(QColor(55, 55, 55))
        pen.setWidth(1)
        p.setPen(pen)

        g = max(2, int(self.grid))
        left, top, right, bottom = r.left(), r.top(), r.right(), r.bottom()

        x = left - (left % g)
        while x <= right:
            p.drawLine(x, top, x, bottom)
            x += g

        y = top - (top % g)
        while y <= bottom:
            p.drawLine(left, y, right, y)
            y += g

        # Origin Crosshair
        if self.show_origin:
            pen2 = QPen(QColor(90, 90, 90))
            pen2.setWidth(1)
            p.setPen(pen2)
            p.drawLine(0, 0, min(60, right), 0)
            p.drawLine(0, 0, 0, min(60, bottom))

    def set_scroll_area(self, scroll_area):
        self._scroll_area = scroll_area

    def delete_control(self, ctrl):
        if ctrl is None:
            return
        try:
            if ctrl in self._controls:
                self._controls.remove(ctrl)
        except Exception:
            pass
        if self._active is ctrl:
            self._active = None
        ctrl.deleteLater()
        self.update()
        self.update_canvas_size()
        try:
            mw = getattr(self, "main_window", None) or self.window()
            if mw is not None and hasattr(mw, "on_designer_controls_changed"):
                mw.on_designer_controls_changed(self._controls)
            if mw is not None and hasattr(mw, "on_designer_selection_changed"):
                mw.on_designer_selection_changed(None)
        except Exception:
            pass

    def is_name_used(self, name: str, except_ctrl=None) -> bool:
        name = (name or "").strip()
        if not name:
            return False
        for c in self._controls:
            if c is except_ctrl:
                continue
            if getattr(c, "instance_name", "") == name:
                return True
        return False



    def copy_to_clipboard(self, ctrl, cut: bool = False):
        if ctrl is None:
            return
        cr = ctrl._content_rect_global()
        self._designer_clip = {
            "tool": getattr(ctrl, "tool_name", "Control"),
            "w": int(cr.width()),
            "h": int(cr.height()),
            "name": getattr(ctrl, "instance_name", ""),
        }
        if cut:
            self.delete_control(ctrl)



    def paste_from_clipboard(self, global_pos=None):
        clip = self._designer_clip
        if not clip:
            return
        tool = clip.get("tool", "Control")
        w = int(clip.get("w", 80))
        h = int(clip.get("h", 28))

        if global_pos is not None:
            p = self.mapFromGlobal(global_pos)
            x, y = p.x(), p.y()
        else:
            x, y = 20, 20

        x = self._snap(x)
        y = self._snap(y)

        rect = QRect(x, y, max(16, w), max(16, h))
        ctrl = DesignerControl(tool, self, rect)

        key = (tool or "Control").strip() or "Control"
        self._tool_counters[key] = self._tool_counters.get(key, 0) + 1
        ctrl.instance_name = f"{key}{self._tool_counters[key]}"

        ctrl.show()
        self._controls.append(ctrl)
        try:
            mw = getattr(self, "main_window", None) or self.window()
            if mw is not None and hasattr(mw, "on_designer_controls_changed"):
                mw.on_designer_controls_changed(self._controls)
        except Exception:
            pass
        try:
            mw = getattr(self, 'main_window', None) or self.window()
            if mw is not None and hasattr(mw, 'object_inspector') and mw.object_inspector is not None:
                mw.object_inspector.set_controls_list(self._controls)
        except Exception:
            pass
        self.set_active(ctrl)
        self.update_canvas_size()
        self.ensure_visible_control(ctrl)

    def ensure_visible_control(self, ctrl):
        sa = self._scroll_area
        if sa is not None and ctrl is not None:
            try:
                sa.ensureWidgetVisible(ctrl, 40, 40)
            except Exception:
                pass

    def update_canvas_size(self):
        w = int(self._base_design_size.width())
        h = int(self._base_design_size.height())
        margin = 80
        for c in list(self._controls):
            try:
                g = c.geometry()
                w = max(w, g.right() + margin)
                h = max(h, g.bottom() + margin)
            except Exception:
                pass
        self.setMinimumSize(QSize(w, h))

    def keyPressEvent(self, ev):
        if ev.key() in (Qt.Key_Delete, Qt.Key_Backspace):
            if self._active is not None:
                self.delete_control(self._active)
                ev.accept()
                return
        super().keyPressEvent(ev)



    def contextMenuEvent(self, ev):
        # Rechtsklick auf leere Fläche: Einfügen anbieten
        if self.childAt(ev.pos()) is not None:
            super().contextMenuEvent(ev)
            return

        menu = QMenu(self)
        act_paste = QAction(share.locales.tr("Einfügen"), self)
        act_paste.setEnabled(bool(self._designer_clip))
        act_paste.triggered.connect(lambda: self.paste_from_clipboard(ev.globalPos()))
        menu.addAction(act_paste)

        menu.addSeparator()
        host = _find_form_designer_host(self)

        act_load = QAction(share.locales.tr("Laden"), self)
        act_load.triggered.connect(lambda: getattr(host, "_action_load_form", lambda: None)())
        menu.addAction(act_load)

        act_save = QAction(share.locales.tr("Speichern"), self)
        act_save.triggered.connect(lambda: getattr(host, "_action_save_form", lambda: None)())
        menu.addAction(act_save)

        act_save_as = QAction(share.locales.tr("Speichern unter..."), self)
        act_save_as.triggered.connect(lambda: getattr(host, "_action_save_form_as", lambda: None)())
        menu.addAction(act_save_as)

        menu.exec_(ev.globalPos())
        
# ---------------------------------------------------------------------------
# Extra Fenster (MDI SubWindow) für den Formular-Designer mit Pixelgrid.
# ---------------------------------------------------------------------------

class FormDesignerWindow(QWidget):
    def __init__(self, main_window: "MainWindow", parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.current_form_path = ""
        self.form_class_name = "ParentForm"
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)

        self.canvas = PixelGridCanvas(self.main_window, self)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setWidget(self.canvas)
        self.canvas.set_scroll_area(self.scroll_area)

        lay.addWidget(self.scroll_area, 1)

    def _designer_host_widget(self):
        try:
            host = self.parentWidget()
            if host is not None:
                return host
        except Exception:
            pass
        try:
            return self.window()
        except Exception:
            return None

    def _form_geometry_for_save(self):
        host = self._designer_host_widget()
        if host is None:
            return 700, 520, 40, 220
        try:
            g = host.geometry()
            return int(g.width()), int(g.height()), int(g.y()), int(g.x())
        except Exception:
            return 700, 520, 40, 220

    def _serialize_form_text(self) -> str:
        width, height, top, left = self._form_geometry_for_save()
        form_name = (self.form_class_name or "ParentForm").strip() or "ParentForm"
        host = self._designer_host_widget()

        generated_on = datetime.now().strftime("%d.%m.%Y")
        header_lines = [
            "** END HEADER -- do not remove this line",
            f"// Generated on {generated_on}",
            "//",
            "PARAMETER bmodal",
            "LOCAL B",
            "B = NEW ParentForm(51,4)",
            "IF (bmodal)",
            "    B.mdi = false",
            "    B.ReadModal()",
            "else",
            "    B.Init(121,2)",
            "    B.Open()",
            "endif",
            "",
        ]

        class_lines = [
            f"CLASS {form_name} OF FORM",
            f"    PROPERTY width = {float(width):.2f}",
            f"    PROPERTY top   = {int(top)}",
            "",
            "    WITH (THIS)",
            f"        onClick = THIS.{form_name}_onClick",
            f"        Width = {int(width)}",
            f"        Height = {int(height)}",
            f"        Top = {int(top)}",
            f"        Left = {int(left)}",
            "    ENDWITH",
        ]

        method_lines = [
            "",
            f"    METHOD {form_name}_onClick(Sender)",
            "    ENDMETHOD",
        ]

        for ctrl in list(getattr(self.canvas, "_controls", [])):
            try:
                r = ctrl._content_rect_global()
                name = getattr(ctrl, "instance_name", "") or getattr(ctrl, "tool_name", "Control")
                tool = (getattr(ctrl, "tool_name", "Control") or "Control").upper()
                text_value = ""
                try:
                    inner = getattr(ctrl, "inner", None)
                    if inner is not None:
                        if hasattr(inner, "text"):
                            text_value = inner.text() or ""
                        elif hasattr(inner, "windowTitle"):
                            text_value = inner.windowTitle() or ""
                except Exception:
                    text_value = ""

                class_lines.extend([
                    f"    THIS.{name} = NEW {tool}(THIS)",
                    f"    WITH (THIS.{name})",
                    f"        onClick = THIS.{name}_onClick",
                ])

                if tool == "PUSHBUTTON":
                    class_lines.extend([
                        '        Font = NEW FONT("Arial",12, .T., .T., .T.)',
                        "        Font.bold = .F.",
                    ])

                class_lines.extend([
                    f"        Left = {int(r.x())}",
                    f"        Top = {int(r.y())}",
                    f"        Width = {int(r.width())}",
                ])

                if int(r.height()) > 0:
                    class_lines.append(f"        Height = {int(r.height())}")

                if text_value:
                    class_lines.append(f"        Text = {json.dumps(text_value, ensure_ascii=False)}")

                class_lines.extend([
                    "    ENDWITH",
                    "",
                ])

                method_lines.extend([
                    "",
                    f"    METHOD {name}_onClick(Sender)",
                    "    ENDMETHOD",
                ])
            except Exception:
                pass

        lines = header_lines + class_lines + method_lines + ["ENDCLASS", ""]
        return "\n".join(lines)

    def _write_form_file(self, file_path: str):
        with open(file_path, "w", encoding="utf-8") as fh:
            fh.write(self._serialize_form_text())
        self.current_form_path = file_path

    def _clear_designer_controls(self):
        for ctrl in list(getattr(self.canvas, "_controls", [])):
            try:
                ctrl.deleteLater()
            except Exception:
                pass
        self.canvas._controls = []
        self.canvas.set_active(None)
        try:
            self.canvas.update_canvas_size()
        except Exception:
            pass
        try:
            mw = getattr(self, "main_window", None)
            if mw is not None and hasattr(mw, "on_designer_controls_changed"):
                mw.on_designer_controls_changed(self.canvas._controls)
        except Exception:
            pass

    def _load_from_form_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read()

        class_match = re.search(
            r"CLASS\s+([A-Za-z_][A-Za-z0-9_]*)\s+OF\s+FORM.*?WITH\s*\(THIS\)(.*?)ENDWITH",
            content,
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        if class_match:
            self.form_class_name = class_match.group(1)
            form_block = class_match.group(2) or ""

            def _read_num(block, key, default=0):
                m = re.search(rf"\b{key}\s*=\s*(-?\d+(?:\.\d+)?)", block, re.IGNORECASE)
                if not m:
                    return default
                try:
                    return int(float(m.group(1)))
                except Exception:
                    return default

            def _read_str(block, key, default=""):
                m = re.search(rf"\b{key}\s*=\s*(.+)", block, re.IGNORECASE)
                if not m:
                    return default
                raw = (m.group(1) or "").strip()
                try:
                    return json.loads(raw)
                except Exception:
                    return raw.strip('"')

            width = _read_num(form_block, "Width", 700)
            height = _read_num(form_block, "Height", 520)
            top = _read_num(form_block, "Top", 40)
            left = _read_num(form_block, "Left", 220)
            title = _read_str(form_block, "Title", "")

            host = self._designer_host_widget()
            if host is not None:
                try:
                    host.setGeometry(left, top, width, height)
                except Exception:
                    pass
                try:
                    if title:
                        host.setWindowTitle(title)
                except Exception:
                    pass

        self._clear_designer_controls()

        tool_map = {
            "PUSHBUTTON": "PushButton",
            "LABEL": "Label",
            "CHECKBOX": "CheckBox",
            "RADIOBUTTON": "RadioButton",
            "LINEEDIT": "LineEdit",
            "TEXTEDIT": "TextEdit",
            "COMBOBOX": "ComboBox",
            "LISTWIDGET": "ListWidget",
            "TABLEWIDGET": "TableWidget",
            "FRAME": "Frame",
            "GROUPBOX": "GroupBox",
        }

        component_pattern = re.compile(
            r"THIS\.([A-Za-z_][A-Za-z0-9_]*)\s*=\s*NEW\s+([A-Za-z_][A-Za-z0-9_]*)\(THIS\)\s+WITH\s*\(THIS\.\1\)(.*?)ENDWITH",
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )

        for m in component_pattern.finditer(content):
            name = m.group(1)
            tool_raw = (m.group(2) or "").upper()
            block = m.group(3) or ""
            tool = tool_map.get(tool_raw, m.group(2).title())

            def _read_num(block, key, default=0):
                mx = re.search(rf"\b{key}\s*=\s*(-?\d+(?:\.\d+)?)", block, re.IGNORECASE)
                if not mx:
                    return default
                try:
                    return int(float(mx.group(1)))
                except Exception:
                    return default

            def _read_str(block, key, default=""):
                mx = re.search(rf"\b{key}\s*=\s*(.+)", block, re.IGNORECASE)
                if not mx:
                    return default
                raw = (mx.group(1) or "").strip()
                try:
                    return json.loads(raw)
                except Exception:
                    return raw.strip('"')

            left = _read_num(block, "Left", 0)
            top = _read_num(block, "Top", 0)
            width = _read_num(block, "Width", 100)
            height = _read_num(block, "Height", 32)
            text_value = _read_str(block, "Text", "")

            rect = QRect(left, top, max(16, width), max(16, height))
            ctrl = DesignerControl(tool, self.canvas, rect)
            ctrl.instance_name = name

            try:
                inner = getattr(ctrl, "inner", None)
                if inner is not None:
                    if hasattr(inner, "setText"):
                        inner.setText(text_value)
                    elif hasattr(inner, "setWindowTitle"):
                        inner.setWindowTitle(text_value)
            except Exception:
                pass

            ctrl.show()
            self.canvas._controls.append(ctrl)

        self.current_form_path = file_path
        try:
            self.canvas.update_canvas_size()
        except Exception:
            pass
        try:
            mw = getattr(self, "main_window", None)
            if mw is not None and hasattr(mw, "on_designer_controls_changed"):
                mw.on_designer_controls_changed(self.canvas._controls)
            if mw is not None and hasattr(mw, "on_designer_selection_changed"):
                mw.on_designer_selection_changed(None)
        except Exception:
            pass

    def _action_save_form_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            share.locales.tr("Formular speichern unter"),
            self.current_form_path or f"{self.form_class_name}.wfm",
            "Formulare (*.wfm *.frm);;WFM (*.wfm);;FRM (*.frm);;Alle Dateien (*.*)",
        )
        if not file_path:
            return
        if not file_path.lower().endswith((".wfm", ".frm")):
            file_path += ".wfm"
        self._write_form_file(file_path)

    def _action_save_form(self):
        if not self.current_form_path:
            self._action_save_form_as()
            return
        self._write_form_file(self.current_form_path)

    def _action_load_form(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            share.locales.tr("Formular laden"),
            "",
            "Formulare (*.wfm *.frm);;Alle Dateien (*.*)",
        )
        if not file_path:
            return
        self._load_from_form_file(file_path)

    def closeEvent(self, ev):
        mw = getattr(self, 'main_window', None)
        try:
            oi = getattr(mw, 'object_inspector', None) if mw is not None else None
            if oi is not None:
                try:
                    oi._current_ctrl = None
                except Exception:
                    pass
                try:
                    oi.set_controls_list([])
                except Exception:
                    pass
        except Exception:
            pass

        try:
            dock = getattr(mw, 'obj_inspector_dock', None) if mw is not None else None
            if dock is not None:
                dock.hide()
        except Exception:
            pass

        try:
            dock = getattr(mw, 'obj_palette_dock', None) if mw is not None else None
            if dock is not None:
                dock.hide()
        except Exception:
            pass

        try:
            panel = getattr(mw, '_designer_panel_splitter', None) if mw is not None else None
            host = getattr(mw, '_designer_host_splitter', None) if mw is not None else None
            if panel is not None:
                panel.hide()
            if host is not None:
                try:
                    host.setSizes([0, max(1, host.sizes()[-1] if host.sizes() else 1000)])
                except Exception:
                    pass
        except Exception:
            pass

        try:
            if mw is not None:
                if getattr(mw, 'form_designer_window', None) is self:
                    mw.form_designer_window = None
                try:
                    mw.designer_canvas = None
                except Exception:
                    pass
        except Exception:
            pass

        super().closeEvent(ev)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        try:
            if hasattr(self.canvas, "update_canvas_size"):
                self.canvas.update_canvas_size()
        except Exception:
            pass
        try:
            mw = getattr(self, "main_window", None)
            oi = getattr(mw, "object_inspector", None) if mw is not None else None
            if oi is not None:
                oi._refresh_properties()
        except Exception:
            pass

class _InspectorTreeDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = QFont("Arial", 10)

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        try:
            if isinstance(editor, QLineEdit):
                editor.setFont(self._font)
                editor.setTextMargins(1, 0, 1, 0)
                editor.setStyleSheet("QLineEdit { padding-left: 1px; padding-right: 1px; padding-top: 0px; padding-bottom: 0px; }")
            elif isinstance(editor, QComboBox):
                editor.setFont(self._font)
                editor.setStyleSheet("QComboBox { padding-left: 1px; padding-right: 1px; padding-top: 0px; padding-bottom: 0px; }")
            elif hasattr(editor, "setFont"):
                editor.setFont(self._font)
        except Exception:
            pass
        return editor


class _EventCodeHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self._rules = []

        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor("#ffd866"))
        kw_fmt.setFontWeight(QFont.Bold)

        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("#a6e22e"))

        com_fmt = QTextCharFormat()
        com_fmt.setForeground(QColor("#7f848e"))
        com_fmt.setFontItalic(True)

        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#66d9ef"))

        keywords = [
            "METHOD", "FUNCTION", "PROCEDURE", "RETURN", "IF", "ELSE", "ENDIF",
            "DO", "CASE", "ENDCASE", "WHILE", "ENDDO", "FOR", "NEXT", "LOCAL",
            "PRIVATE", "PUBLIC", "CLASS", "ENDCLASS", "THIS", "SET", "WRITE",
            "PRINT", "ON", "OFF", "TO", "SCREEN", "SQL", "FORM", "TABLE"
        ]
        for kw in keywords:
            self._rules.append((re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE), kw_fmt))

        self._rules.append((re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"'), str_fmt))
        self._rules.append((re.compile(r"'[^'\\]*(?:\\.[^'\\]*)*'"), str_fmt))
        self._rules.append((re.compile(r"\b\d+(?:\.\d+)?\b"), num_fmt))
        self._rules.append((re.compile(r"(?:&&|//|\*\*).*$"), com_fmt))

    def highlightBlock(self, text):
        for rx, fmt in self._rules:
            for m in rx.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


class _EventCodeLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self):
        return QSize(self._editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._editor.line_number_area_paint_event(event)


class _EventCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._line_number_area = _EventCodeLineNumberArea(self)
        self._highlighter = _EventCodeHighlighter(self.document())

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setTabStopDistance(QFontMetrics(self.font()).horizontalAdvance(" ") * 4)
        self.setStyleSheet(
            "QPlainTextEdit {"
            " background: #1e1e1e; color: #e6e6e6; border: 1px solid #444;"
            " selection-background-color: #264f78; padding-left: 4px; }"
        )

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = max(2, len(str(max(1, self.blockCount()))))
        return 10 + self.fontMetrics().horizontalAdvance("9") * digits

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self._line_number_area)
        painter.fillRect(event.rect(), QColor("#252526"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#8a8a8a"))
                painter.drawText(
                    0, top,
                    self._line_number_area.width() - 4,
                    self.fontMetrics().height(),
                    Qt.AlignRight,
                    str(block_number + 1)
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        extra = []
        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()
            sel.format.setBackground(QColor("#2d2d30"))
            sel.format.setProperty(QTextFormat.FullWidthSelection, True)
            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            extra.append(sel)
        self.setExtraSelections(extra)


class EventEditorWindow(QWidget):
    def __init__(self, main_window, control, event_name: str, item: QTreeWidgetItem | None = None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.control = control
        self.item = item
        self._subwindow = None

        mark_escape_close(self)
        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self._object_name = self._sanitize_object_name(
            getattr(control, "instance_name", "") or "Form"
        )
        self._initial_event_name = (event_name or "").strip() or "OnClick"

        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(6)

        top = QHBoxLayout()
        top.addWidget(QLabel("Event Name:", self), 0)

        self.ed_event_name = QLineEdit(self._initial_event_name, self)
        self.ed_event_name.setFont(QFont("Arial", 10))
        self.ed_event_name.setTextMargins(1, 0, 1, 0)
        top.addWidget(self.ed_event_name, 1)

        root.addLayout(top)

        self.editor = _EventCodeEditor(self)
        self.editor.setFont(QFont("Consolas", 10))
        root.addWidget(self.editor, 1)

        btns = QHBoxLayout()
        btns.addStretch(1)

        self.btn_apply = QPushButton("Apply", self)
        self.btn_help = QPushButton("Help", self)
        self.btn_cancel = QPushButton("Cancel", self)

        btns.addWidget(self.btn_apply)
        btns.addWidget(self.btn_help)
        btns.addWidget(self.btn_cancel)
        root.addLayout(btns)

        self.btn_apply.clicked.connect(self._apply)
        self.btn_help.clicked.connect(self._help)
        self.btn_cancel.clicked.connect(self.close)

        self._load_existing_code()

    def set_subwindow(self, sub):
        self._subwindow = sub

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            event.accept()
            return
        super().keyPressEvent(event)

    def _sanitize_object_name(self, name: str) -> str:
        name = re.sub(r"\W+", "_", (name or "").strip())
        return name or "Form"

    def _current_method_name(self) -> str:
        ev = re.sub(r"\W+", "_", (self.ed_event_name.text() or self._initial_event_name).strip())
        ev = ev or "OnClick"
        return f"{self._object_name}_{ev}"

    def _resolve_editor_widget(self):
        mw = self.main_window
        if mw is None or not hasattr(mw, "ensure_code_editor_window"):
            return None

        win = mw.ensure_code_editor_window(focus=True)
        if win is None:
            return None

        for attr in ("current_editor", "editor", "code_editor", "text_edit"):
            if hasattr(win, attr):
                try:
                    ed = getattr(win, attr)()
                except TypeError:
                    ed = getattr(win, attr)
                if ed is not None:
                    return ed
        return None

    def _method_regex(self, method_name: str):
        return re.compile(
            rf"(?ims)^\s*METHOD\s+{re.escape(method_name)}\b.*?(?=^\s*METHOD\b|\Z)"
        )

    def _load_existing_code(self):
        ed = self._resolve_editor_widget()
        if ed is None:
            return

        try:
            text = ed.document().toPlainText()
        except Exception:
            return

        method_name = self._current_method_name()
        m = self._method_regex(method_name).search(text)
        if not m:
            self.editor.setPlainText("")
            return

        block = m.group(0)
        lines = block.splitlines()
        body = []
        for line in lines[1:]:
            if line.strip().upper() == "RETURN":
                continue
            body.append(line)

        self.editor.setPlainText("\n".join(body).rstrip())

    def _apply(self):
        method_name = self._current_method_name()
        code = (self.editor.toPlainText() or "").rstrip()

        snippet_lines = [f"METHOD {method_name}"]
        if code:
            snippet_lines.append(code)
        snippet_lines.append("RETURN")
        snippet = "\n".join(snippet_lines) + "\n"

        ed = self._resolve_editor_widget()
        if ed is None:
            QMessageBox.warning(self, "Apply", "Kein Editor-Fenster verfügbar.")
            return

        try:
            doc_text = ed.document().toPlainText()
            rx = self._method_regex(method_name)

            if rx.search(doc_text):
                new_text = rx.sub(snippet.rstrip(), doc_text, count=1)
            else:
                sep = "" if doc_text.endswith("\n") or not doc_text else "\n\n"
                new_text = doc_text + sep + snippet

            ed.setPlainText(new_text)
        except Exception as exc:
            QMessageBox.warning(self, "Apply", str(exc))
            return

        if self.item is not None:
            try:
                self.item.setText(1, method_name)
            except Exception:
                pass

        try:
            if hasattr(self.main_window, "jump_to_symbol"):
                self.main_window.jump_to_symbol(method_name)
        except Exception:
            pass

        self.close()

    def _help(self):
        try:
            if hasattr(self.main_window, "mdi") and hasattr(self.main_window, "help_mainwindow"):
                open_helpwindow(self.main_window.mdi, self.main_window.help_mainwindow)
                return
        except Exception:
            pass
        QMessageBox.information(self, "Help", "Keine Hilfe verfügbar.")

class ObjectInspectorPanel(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self._current_ctrl = None
        self._event_buttons = []
        self._tree_delegate = _InspectorTreeDelegate(self)
        self._ui_font = QFont("Arial", 10)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(6)

        self.obj_combo = QComboBox(self)
        self.obj_combo.setEditable(False)
        self.obj_combo.setFont(self._ui_font)
        self.obj_combo.setStyleSheet("QComboBox { padding-left: 1px; padding-right: 1px; padding-top: 0px; padding-bottom: 0px; }")
        self.obj_combo.currentIndexChanged.connect(self._on_combo_changed)
        lay.addWidget(self.obj_combo)

        self.tabs = QTabWidget(self)
        self.tabs.setFont(self._ui_font)
        lay.addWidget(self.tabs, 1)

        self.tree_props = QTreeWidget(self)
        self.tree_props.setFont(self._ui_font)
        self.tree_props.setIndentation(20)
        self.tree_props.setRootIsDecorated(True)
        self.tree_props.setItemDelegate(self._tree_delegate)
        self.tree_props.header().setFont(self._ui_font)
        self.tree_props.setColumnCount(2)
        self.tree_props.setHeaderLabels(["Key", "Value"])
        self.tree_props.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree_props.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tree_props.itemChanged.connect(self._on_prop_changed)
        self.tabs.addTab(self.tree_props, share.locales.tr("Properties"))

        self.tree_events = QTreeWidget(self)
        self.tree_events.setFont(self._ui_font)
        self.tree_events.setIndentation(20)
        self.tree_events.setRootIsDecorated(True)
        self.tree_events.setItemDelegate(self._tree_delegate)
        self.tree_events.header().setFont(self._ui_font)
        self.tree_events.setColumnCount(3)
        self.tree_events.setHeaderLabels(["Event", "Handler", ""])
        self.tree_events.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree_events.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tree_events.header().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tree_events.header().resizeSection(2, 34)
        self.tree_events.itemDoubleClicked.connect(self._on_event_double_clicked)
        self.tabs.addTab(self.tree_events, "Events")

        self.tree_methods = QTreeWidget(self)
        self.tree_methods.setFont(self._ui_font)
        self.tree_methods.setIndentation(20)
        self.tree_methods.setRootIsDecorated(True)
        self.tree_methods.setItemDelegate(self._tree_delegate)
        self.tree_methods.header().setFont(self._ui_font)
        self.tree_methods.setColumnCount(2)
        self.tree_methods.setHeaderLabels(["Methode", "Override"])
        self.tree_methods.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tree_methods.header().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tree_methods.itemDoubleClicked.connect(self._on_method_double_clicked)
        self.tabs.addTab(self.tree_methods, "Methoden")

        self._fill_static_events_methods()

    def _clear_event_buttons(self):
        self._event_buttons = []
        try:
            for i in range(self.tree_events.topLevelItemCount()):
                item = self.tree_events.topLevelItem(i)
                if item is not None:
                    self.tree_events.removeItemWidget(item, 2)
        except Exception:
            pass

    def _make_event_button(self, item):
        host = QWidget(self.tree_events)
        host_layout = QHBoxLayout(host)
        host_layout.setContentsMargins(0, 0, 0, 0)
        host_layout.setSpacing(0)
        host_layout.addStretch(1)

        btn = QPushButton("E", host)
        btn.setFixedSize(20, 18)
        btn.setFont(QFont("Arial", 8, QFont.Bold))
        btn.setStyleSheet(
            "QPushButton { color: #ffff00; background: #303030; border: 1px solid #666666; padding: 0px; }"
            "QPushButton:hover { background: #404040; }"
        )
        btn.clicked.connect(lambda _=False, it=item: self._open_event_editor_for_item(it))
        host_layout.addWidget(btn, 0, Qt.AlignRight)
        self._event_buttons.append(btn)
        return host

    def _fill_static_events_methods(self):
        self._clear_event_buttons()

        self.tree_events.clear()
        for ev in ["OnClick", "OnDblClick", "OnKeyDown", "OnKeyUp", "OnCreate", "OnDestroy"]:
            it = QTreeWidgetItem([ev, "", ""])
            it.setFlags(it.flags() | Qt.ItemIsEditable)
            it.setFont(0, self._ui_font)
            it.setFont(1, self._ui_font)
            self.tree_events.addTopLevelItem(it)
            self.tree_events.setItemWidget(it, 2, self._make_event_button(it))

        self.tree_methods.clear()
        for m in ["Init", "Show", "Hide", "Enable", "Disable", "Resize", "Move"]:
            it = QTreeWidgetItem([m, ""])
            it.setFlags(it.flags() | Qt.ItemIsEditable)
            it.setFont(0, self._ui_font)
            it.setFont(1, self._ui_font)
            self.tree_methods.addTopLevelItem(it)

    def set_controls_list(self, controls):
        self.obj_combo.blockSignals(True)
        current_text = self.obj_combo.currentText()
        self.obj_combo.clear()
        form_name = "Form"
        try:
            fw = getattr(self.main_window, "form_designer_window", None)
            if fw is not None:
                form_name = (getattr(fw, "form_class_name", "") or "Form").strip() or "Form"
        except Exception:
            pass
        self.obj_combo.addItem(form_name, None)
        for c in controls or []:
            name = getattr(c, "instance_name", "") or getattr(c, "tool_name", "Control")
            self.obj_combo.addItem(name, c)
        self.obj_combo.blockSignals(False)
        idx = self.obj_combo.findText(current_text)
        if idx >= 0:
            self.obj_combo.setCurrentIndex(idx)

    def set_current(self, ctrl):
        self._current_ctrl = ctrl
        if ctrl is None:
            if self.obj_combo.count() > 0:
                self.obj_combo.setCurrentIndex(0)
        else:
            name = getattr(ctrl, "instance_name", "")
            idx = self.obj_combo.findText(name)
            if idx >= 0:
                self.obj_combo.setCurrentIndex(idx)
        self._refresh_properties()

    def _get_ctrl_text(self, c) -> str:
        try:
            w = getattr(c, "inner", None)
            if w is None:
                return ""
            if hasattr(w, "text"):
                t = w.text()
                return "" if t is None else str(t)
            if hasattr(w, "windowTitle"):
                t = w.windowTitle()
                return "" if t is None else str(t)
        except Exception:
            pass
        return ""

    def _refresh_properties(self):
        self.tree_props.blockSignals(True)
        self.tree_props.setUpdatesEnabled(False)
        try:
            self.tree_props.clear()
            c = self._current_ctrl
            if c is None:
                fw = getattr(self.main_window, "form_designer_window", None)
                host = None
                try:
                    host = fw.parentWidget() if fw is not None else None
                except Exception:
                    host = None
                if host is None and fw is not None:
                    try:
                        host = fw.window()
                    except Exception:
                        host = None
                width = 700
                height = 520
                top = 0
                left = 0
                title = ""
                form_name = "Form"
                try:
                    if host is not None:
                        g = host.geometry()
                        width = int(g.width())
                        height = int(g.height())
                        top = int(g.y())
                        left = int(g.x())
                        title = host.windowTitle() or ""
                except Exception:
                    pass
                try:
                    if fw is not None:
                        form_name = (getattr(fw, "form_class_name", "") or "Form").strip() or "Form"
                except Exception:
                    pass

                groups = {
                    "Form": [
                        ("Name", form_name),
                        ("Width", str(width)),
                        ("Height", str(height)),
                        ("Top", str(top)),
                        ("Left", str(left)),
                        ("Title", title),
                    ],
                }
            else:
                cr = c._content_rect_global()
                groups = {
                    "Name": [
                        ("Name", getattr(c, "instance_name", "")),
                        ("Type", getattr(c, "tool_name", "")),
                    ],
                    "Anzeige": [
                        ("Left", str(cr.x())),
                        ("Top", str(cr.y())),
                        ("Width", str(cr.width())),
                        ("Height", str(cr.height())),
                    ],
                    "Beschriftung": [
                        ("Text", self._get_ctrl_text(c)),
                    ],
                }

            self.tree_props.setRootIsDecorated(True)
            for gname, rows in groups.items():
                top_item = QTreeWidgetItem([gname, ""])
                top_item.setFirstColumnSpanned(True)
                top_item.setFlags(top_item.flags() & ~Qt.ItemIsEditable)
                top_item.setFont(0, self._ui_font)
                self.tree_props.addTopLevelItem(top_item)

                for k, v in rows:
                    it = QTreeWidgetItem([k, str(v)])
                    it.setFlags(it.flags() | Qt.ItemIsEditable)
                    it.setFont(0, self._ui_font)
                    it.setFont(1, self._ui_font)
                    top_item.addChild(it)
                top_item.setExpanded(True)
        except Exception:
            pass
        finally:
            self.tree_props.setUpdatesEnabled(True)
            self.tree_props.blockSignals(False)

    def _on_prop_changed(self, item: QTreeWidgetItem, col: int):
        if col != 1:
            return
        c = self._current_ctrl

        try:
            if item.parent() is None and item.childCount() > 0:
                return
        except Exception:
            pass

        key = (item.text(0) or "").strip()
        val = item.text(1)

        if c is None:
            fw = getattr(self.main_window, "form_designer_window", None)
            host = None
            try:
                host = fw.parentWidget() if fw is not None else None
            except Exception:
                host = None
            if host is None and fw is not None:
                try:
                    host = fw.window()
                except Exception:
                    host = None
            try:
                if key.lower() == "name" and fw is not None:
                    fw.form_class_name = val.strip() or "Form"
                    self.obj_combo.setItemText(0, fw.form_class_name)
                    self.obj_combo.setCurrentIndex(0)
                    return
                if key.lower() in ("left", "top", "width", "height") and host is not None:
                    n = int(float(val))
                    g = host.geometry()
                    if key.lower() == "left":
                        g.moveLeft(n)
                    elif key.lower() == "top":
                        g.moveTop(n)
                    elif key.lower() == "width":
                        g.setWidth(max(1, n))
                    elif key.lower() == "height":
                        g.setHeight(max(1, n))
                    host.setGeometry(g)
                    self._refresh_properties()
                    return
                if key.lower() == "title" and host is not None:
                    host.setWindowTitle(val)
                    self._refresh_properties()
                    return
            except Exception:
                pass
            return

        try:
            if key.lower() == "name":
                c.instance_name = val.strip()
                try:
                    c.update()
                except Exception:
                    pass
                try:
                    self.set_controls_list(
                        getattr(self.main_window, "designer_controls", [])
                        or getattr(getattr(self.main_window, "designer_canvas", None), "_controls", [])
                    )
                    self.set_current(c)
                except Exception:
                    pass
                return

            if key.lower() in ("left", "top", "width", "height"):
                try:
                    n = int(float(val))
                except Exception:
                    return
                g = c.geometry()
                if key.lower() == "left":
                    g.moveLeft(n)
                elif key.lower() == "top":
                    g.moveTop(n)
                elif key.lower() == "width":
                    g.setWidth(max(1, n))
                elif key.lower() == "height":
                    g.setHeight(max(1, n))
                c.setGeometry(g)
                try:
                    if hasattr(c, "_sync_inner"):
                        c._sync_inner()
                except Exception:
                    pass
                try:
                    if hasattr(c.parent(), "update_canvas_size"):
                        c.parent().update_canvas_size()
                except Exception:
                    pass
                try:
                    c.update()
                except Exception:
                    pass
                try:
                    self._refresh_properties()
                except Exception:
                    pass
                return

            if key.lower() in ("text", "caption", "title"):
                w = getattr(c, "inner", None)
                if w is not None:
                    if hasattr(w, "setText"):
                        w.setText(val)
                    elif hasattr(w, "setWindowTitle"):
                        w.setWindowTitle(val)
                    c.update()
                return
        except Exception:
            pass

    def _on_combo_changed(self, idx):
        ctrl = self.obj_combo.itemData(idx)
        try:
            canvas = getattr(self.main_window, "designer_canvas", None)
            if canvas is not None:
                canvas.set_active(ctrl)
        except Exception:
            pass
        self._current_ctrl = ctrl
        self._refresh_properties()

    def _open_event_editor_for_item(self, item):
        if item is None:
            return

        ev_name = (item.text(0) or "").strip() or "OnClick"
        try:
            mw = self.main_window
            editor_win = EventEditorWindow(mw, self._current_ctrl, ev_name, item=item)
            if hasattr(mw, "mdi") and mw.mdi is not None:
                sub = mw.mdi.addSubWindow(editor_win)
                mark_escape_close(sub)
                editor_win.set_subwindow(sub)
                sub.setWindowTitle(f"Event Editor - {ev_name}")
                sub.resize(640, 420)
                sub.show()
                mw.mdi.setActiveSubWindow(sub)
            else:
                editor_win.show()
        except Exception as exc:
            QMessageBox.warning(self, "Events", str(exc))

    def _on_event_double_clicked(self, item, col):
        if item is None:
            return

        if col == 2:
            self._open_event_editor_for_item(item)
            return

        handler = (item.text(1) or "").strip()
        if not handler:
            base = getattr(self._current_ctrl, "instance_name", "Control") or "Control"
            handler = f"{base}_{item.text(0)}"
            item.setText(1, handler)

        try:
            self.main_window.ensure_code_editor_window(focus=True)
            self.main_window.jump_to_symbol(handler)
        except Exception:
            pass

    def _on_method_double_clicked(self, item, col):
        if col != 1:
            return

        name = (item.text(1) or "").strip()
        if not name:
            base = getattr(self._current_ctrl, "instance_name", "Control") or "Control"
            name = f"{base}_{item.text(0)}"
            item.setText(1, name)

        try:
            self.main_window.ensure_code_editor_window(focus=True)
            self.main_window.jump_to_symbol(name)
        except Exception:
            pass

class ArrowFontProxyStyle(QProxyStyle):
    def __init__(self, base=None, font_family="Segoe UI Symbol"):
        super().__init__(base)
        self.font_family = font_family

    def drawPrimitive(self, elem, opt, painter, widget=None):
        # ComboBox Pfeil
        if elem == QStyle.PE_IndicatorArrowDown:
            self._draw_glyph(painter, opt.rect, "▼")
            return
        if elem == QStyle.PE_IndicatorArrowUp:
            self._draw_glyph(painter, opt.rect, "▲")
            return
        if elem == QStyle.PE_IndicatorArrowLeft:
            self._draw_glyph(painter, opt.rect, "◀")
            return
        if elem == QStyle.PE_IndicatorArrowRight:
            self._draw_glyph(painter, opt.rect, "▶")
            return
        super().drawPrimitive(elem, opt, painter, widget)

    def _draw_glyph(self, painter: QPainter, rect, glyph: str):
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(QPen(QColor(255, 220, 0)))
        f = QFont(self.font_family)
        f.setBold(True)
        # Größe an Rect koppeln
        f.setPixelSize(max(10, min(rect.width(), rect.height()) - 2))
        painter.setFont(f)
        painter.drawText(rect, Qt.AlignCenter, glyph)
        painter.restore()
        

# ---------------------------------------------------------------------------
# Debug Console (split view: output + one-liner input with history)
# Single-line-ish input with history (Up/Down) and Enter-to-submit.
# ---------------------------------------------------------------------------
class _CommandInputEdit(QPlainTextEdit):
    commandEntered = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._history = []
        self._hist_idx = -1
        self.setMaximumBlockCount(2000)
        self.setTabChangesFocus(False)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        try:
            self.setFont(QFont("Consolas", 10))
        except Exception:
            pass

    def set_history(self, items):
        self._history = list(items or [])
        self._hist_idx = len(self._history)

    def history(self):
        return list(self._history)

    def _set_text_all(self, s: str):
        self.blockSignals(True)
        try:
            self.setPlainText(s)
            cur = self.textCursor()
            cur.movePosition(QTextCursor.End)
            self.setTextCursor(cur)
        finally:
            self.blockSignals(False)

    def keyPressEvent(self, ev):
        key = ev.key()
        mods = ev.modifiers()

        # Enter => submit current line(s)
        if key in (Qt.Key_Return, Qt.Key_Enter) and mods == Qt.NoModifier:
            cmd = self.toPlainText().strip()
            if cmd:
                # add to history (dedupe last)
                if not self._history or self._history[-1] != cmd:
                    self._history.append(cmd)
                self._hist_idx = len(self._history)
                self._set_text_all("")
                self.commandEntered.emit(cmd)
            ev.accept()
            return

        # Up/Down => history navigation (only when cursor at start/end-ish)
        if key == Qt.Key_Up and mods == Qt.NoModifier:
            if self._history:
                self._hist_idx = max(0, self._hist_idx - 1)
                self._set_text_all(self._history[self._hist_idx])
            ev.accept()
            return

        if key == Qt.Key_Down and mods == Qt.NoModifier:
            if self._history:
                self._hist_idx = min(len(self._history), self._hist_idx + 1)
                if self._hist_idx >= len(self._history):
                    self._set_text_all("")
                else:
                    self._set_text_all(self._history[self._hist_idx])
            ev.accept()
            return

        super().keyPressEvent(ev)

# ---------------------------------------------------------------------------
# MDI widget: output on top (read-only), input below.
# ---------------------------------------------------------------------------
class DebugConsoleWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        mark_escape_protected(self)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        self.splitter = QSplitter(Qt.Vertical, self)

        self.out = QTextEdit(self)
        self.out.setReadOnly(True)
        try:
            self.out.document().setMaximumBlockCount(10000)
        except Exception:
            pass
        self.out.setLineWrapMode(QTextEdit.NoWrap)
        try:
            self.out.setFont(QFont("Consolas", 10))
        except Exception:
            pass

        self.inp = _CommandInputEdit(self)
        self.inp.setMinimumHeight(100)
        self.inp.commandEntered.connect(self._on_command)

        self.splitter.addWidget(self.out)
        self.splitter.addWidget(self.inp)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([400, 90])

        lay.addWidget(self.splitter, 1)

    def append_output(self, text: str, fg_hex: str | None = None, bg_hex: str | None = None):
        text = "" if text is None else str(text)
        cursor = self.out.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.out.setTextCursor(cursor)

        fmt = QTextCharFormat()
        if fg_hex:
            try:
                fmt.setForeground(QColor(fg_hex))
            except Exception:
                pass
        if bg_hex:
            try:
                fmt.setBackground(QColor(bg_hex))
            except Exception:
                pass

        cursor.insertText(text, fmt)
        cursor.insertBlock()
        self.out.setTextCursor(cursor)
        try:
            self.out.ensureCursorVisible()
        except Exception:
            pass

    def clear_output(self):
        try:
            self.out.clear()
            cur = self.out.textCursor()
            cur.movePosition(QTextCursor.Start)
            self.out.setTextCursor(cur)
        except Exception:
            pass

    def _on_command(self, cmd: str):
        #self.append_output(f">>> {cmd}")
        try:
            out = self.main_window._execute_one_liner(cmd)
            if out:
                self.append_output(out.rstrip())
                delete_last_line(self.out)
        except Exception as e:
            tb = traceback.format_exc()
            self.append_output(tb)



class SidebarActionLabel(QLabel):
    def __init__(self, text: str, callback=None, parent=None):
        super().__init__(text, parent)
        self._callback = callback
        self.setCursor(Qt.PointingHandCursor)
        self.setMargin(8)
        self.setStyleSheet("""
            QLabel {
                color: #ffd866;
                background: transparent;
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 6px 8px;
            }
            QLabel:hover {
                background: #2a2a2a;
                border: 1px solid #555555;
            }
        """)

    def mousePressEvent(self, event):
        try:
            if callable(self._callback):
                self._callback()
        finally:
            super().mousePressEvent(event)


class SidebarPopupWidget(QFrame):
    def __init__(self, parent=None, title: str = ""):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.setObjectName("SidebarPopupWidget")
        self.setFrameShape(QFrame.NoFrame)
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self.setStyleSheet("""
            QFrame#SidebarPopupWidget {
                background: #1f1f1f;
                color: #ffd866;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            QLabel {
                color: #ffd866;
            }
        """)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setSpacing(4)

        if title:
            lbl = QLabel(title, self)
            f = QFont("Arial", 10)
            f.setBold(True)
            lbl.setFont(f)
            lay.addWidget(lbl)

        self._items_layout = QVBoxLayout()
        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(2)
        lay.addLayout(self._items_layout)

    def add_action(self, text: str, callback):
        lbl = SidebarActionLabel(text, callback=callback, parent=self)
        self._items_layout.addWidget(lbl)
        return lbl

    def popup_next_to(self, anchor: QWidget, x_offset: int = 8):
        if anchor is None:
            self.show()
            return
        self.adjustSize()
        gp = anchor.mapToGlobal(QPoint(anchor.width() + x_offset, 0))
        self.move(gp)
        self.show()
        self.raise_()
        self.activateWindow()


class SidebarIconButton(QToolButton):
    def __init__(self, text: str, icon: QIcon = None, parent=None):
        super().__init__(parent)
        self.setText(text)
        if icon is not None:
            self.setIcon(icon)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(32, 32))
        self.setFixedWidth(88)
        self.setMinimumHeight(76)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QToolButton {
                color: #ffd866;
                background: #1f1f1f;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 6px 4px;
            }
            QToolButton:hover {
                background: #2a2a2a;
                border: 1px solid #666666;
            }
            QToolButton:pressed {
                background: #111111;
            }
        """)



class FormDesignerDock(QDockWidget):
    def __init__(self, main_window, parent=None):
        super().__init__("", parent)
        self.main_window = main_window
        self._actions_popup = None
        self._projects_popup = None
        self._convert_popup = None
        self._tools_popup = None

        self.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setFloating(False)
        self.setTitleBarWidget(QWidget(self))
        self.setMinimumWidth(100)
        self.setMaximumWidth(100)

        host = QWidget(self)
        host.setMinimumWidth(100)
        host.setMaximumWidth(100)

        outer = QVBoxLayout(host)
        outer.setContentsMargins(6, 6, 6, 6)
        outer.setSpacing(6)

        self.btn_up = QPushButton("▲\nOben", host)
        self.btn_down = QPushButton("▼\nUnten", host)
        for b in (self.btn_up, self.btn_down):
            b.setFixedHeight(52)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    color: #ffd866;
                    background: #1f1f1f;
                    border: 1px solid #555555;
                    border-radius: 6px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #2a2a2a;
                }
                QPushButton:pressed {
                    background: #111111;
                }
            """)

        self.scroll = QScrollArea(host)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)

        inner = QWidget(self.scroll)
        inner.setMinimumWidth(90)
        inner.setMaximumWidth(90)
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        st = self.style()
        self.btn_actions = SidebarIconButton(
            "Actions",
            st.standardIcon(QStyle.SP_FileDialogDetailedView),
            inner,
        )
        self.btn_projects = SidebarIconButton(
            "Projects",
            st.standardIcon(QStyle.SP_DirOpenIcon),
            inner,
        )
        self.btn_help = SidebarIconButton(
            "Hilfe",
            st.standardIcon(QStyle.SP_MessageBoxInformation),
            inner,
        )
        self.btn_convert = SidebarIconButton(
            "Convert",
            st.standardIcon(QStyle.SP_BrowserReload),
            inner,
        )
        self.btn_settings = SidebarIconButton(
            "Einstellungen",
            st.standardIcon(QStyle.SP_FileDialogContentsView),
            inner,
        )
        self.btn_tools = SidebarIconButton(
            "Tools",
            st.standardIcon(QStyle.SP_ComputerIcon),
            inner,
        )

        lay.addWidget(self.btn_actions, 0, Qt.AlignTop | Qt.AlignHCenter)
        lay.addWidget(self.btn_projects, 0, Qt.AlignTop | Qt.AlignHCenter)
        lay.addWidget(self.btn_help, 0, Qt.AlignTop | Qt.AlignHCenter)
        lay.addWidget(self.btn_convert, 0, Qt.AlignTop | Qt.AlignHCenter)
        lay.addWidget(self.btn_settings, 0, Qt.AlignTop | Qt.AlignHCenter)
        lay.addWidget(self.btn_tools, 0, Qt.AlignTop | Qt.AlignHCenter)
        lay.addStretch(1)

        self.scroll.setWidget(inner)

        outer.addWidget(self.btn_up, 0)
        outer.addWidget(self.scroll, 1)
        outer.addWidget(self.btn_down, 0)

        self.setWidget(host)

        self.btn_up.clicked.connect(self._scroll_up)
        self.btn_down.clicked.connect(self._scroll_down)
        self.btn_actions.clicked.connect(self._toggle_actions_popup)
        self.btn_projects.clicked.connect(self._toggle_projects_popup)
        self.btn_help.clicked.connect(self._show_help)
        self.btn_convert.clicked.connect(self._toggle_convert_popup)
        self.btn_settings.clicked.connect(self._open_settings)
        self.btn_tools.clicked.connect(self._toggle_tools_popup)

    def _scroll_up(self):
        try:
            bar = self.scroll.verticalScrollBar()
            bar.setValue(bar.value() - 80)
        except Exception:
            pass

    def _scroll_down(self):
        try:
            bar = self.scroll.verticalScrollBar()
            bar.setValue(bar.value() + 80)
        except Exception:
            pass

    def _close_other_popups(self, keep=None):
        for popup in (self._actions_popup, self._projects_popup, self._convert_popup, self._tools_popup):
            try:
                if popup is not None and popup is not keep and popup.isVisible():
                    popup.hide()
            except Exception:
                pass

    def _placeholder_message(self, title: str, text: str):
        QMessageBox.information(self.main_window, title, text)

    def _ensure_actions_popup(self):
        if self._actions_popup is not None:
            return self._actions_popup
        p = SidebarPopupWidget(self, title="Actions")
        p.add_action("Neu Tabelle", lambda: self._run_and_close(p, self.main_window.mdi_open_table_designer))
        p.add_action("Neu Formular", lambda: self._run_and_close(p, lambda: self.main_window.ensure_designer(focus=True)))
        p.add_action("Neu Programm", lambda: self._run_and_close(p, lambda: self.main_window.ensure_code_editor_window(focus=True)))
        p.add_action("Neu Bericht", lambda: self._run_and_close(p, lambda: self._placeholder_message("Bericht", "Platzhalter: Neuer Bericht")))
        p.add_action("Neu SQL", lambda: self._run_and_close(p, self.main_window.mdi_open_sql_builder))
        p.add_action("Neu Internet-Dokument", lambda: self._run_and_close(p, lambda: self.main_window.ensure_code_editor_window(focus=True)))
        self._actions_popup = p
        return p

    def _ensure_projects_popup(self):
        p = self._projects_popup
        if p is None:
            p = SidebarPopupWidget(self, title="Projects")
            self._projects_popup = p
        while p._items_layout.count():
            item = p._items_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        entries = []
        try:
            entries = list(self.main_window.recent_project_directories(limit=5))
        except Exception:
            entries = []
        if not entries:
            p.add_action("Keine Projekte", lambda: p.hide())
            return p
        for directory in entries:
            title = os.path.basename(directory.rstrip('/\\')) or directory
            p.add_action(title, lambda d=directory: self._run_and_close(p, lambda: self.main_window.open_project_directory(d)))
        return p

    def _ensure_convert_popup(self):
        if self._convert_popup is not None:
            return self._convert_popup
        p = SidebarPopupWidget(self, title="Convert")
        p.add_action("Convert to Python", lambda: self._run_and_close(p, lambda: self._placeholder_message("Convert", "Platzhalter: Convert to Python")))
        p.add_action("Convert to Pascal", lambda: self._run_and_close(p, lambda: self._placeholder_message("Convert", "Platzhalter: Convert to Pascal")))
        p.add_action("Convert to JavaScript", lambda: self._run_and_close(p, lambda: self._placeholder_message("Convert", "Platzhalter: Convert to JavaScript")))
        p.add_action("Convert to Java", lambda: self._run_and_close(p, lambda: self._placeholder_message("Convert", "Platzhalter: Convert to Java")))
        p.add_action("Convert to C/C++", lambda: self._run_and_close(p, lambda: self._placeholder_message("Convert", "Platzhalter: Convert to C/C++")))
        p.add_action("Convert to Visual Basic", lambda: self._run_and_close(p, lambda: self._placeholder_message("Convert", "Platzhalter: Convert to Visual Basic")))
        self._convert_popup = p
        return p

    def _ensure_tools_popup(self):
        p = self._tools_popup
        if p is None:
            p = SidebarPopupWidget(self, title="Tools")
            self._tools_popup = p
        while p._items_layout.count():
            item = p._items_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
        p.add_action("Localize", lambda: self._run_and_close(p, lambda: self.main_window.ensure_localize_tool(focus=True)))
        return p

    def _toggle_tools_popup(self):
        popup = self._ensure_tools_popup()
        self._close_other_popups(keep=popup)
        if popup.isVisible():
            popup.hide()
        else:
            popup.popup_next_to(self.btn_tools)

    def _run_and_close(self, popup, callback):
        try:
            if callable(callback):
                callback()
        finally:
            try:
                popup.hide()
            except Exception:
                pass

    def _toggle_actions_popup(self):
        popup = self._ensure_actions_popup()
        self._close_other_popups(keep=popup)
        if popup.isVisible():
            popup.hide()
        else:
            popup.popup_next_to(self.btn_actions)

    def _toggle_projects_popup(self):
        popup = self._ensure_projects_popup()
        self._close_other_popups(keep=popup)
        if popup.isVisible():
            popup.hide()
        else:
            popup.popup_next_to(self.btn_projects)

    def _toggle_convert_popup(self):
        popup = self._ensure_convert_popup()
        self._close_other_popups(keep=popup)
        if popup.isVisible():
            popup.hide()
        else:
            popup.popup_next_to(self.btn_convert)

    def _show_help(self):
        try:
            if hasattr(self.main_window, 'status_left'):
                self.main_window.status_left.setText('Hilfe wird geladen...')
                QApplication.processEvents()
            help_mw = share.utildef.helpwin.HelpMainWindow()
            open_helpwindow(self.main_window.mdi, help_mw)
        except Exception:
            self._placeholder_message("Hilfe", "Keine Hilfe verfügbar.")
        finally:
            try:
                if hasattr(self.main_window, 'status_left'):
                    self.main_window.status_left.setText('Ready')
            except Exception:
                pass

    def _open_settings(self):
        try:
            self.main_window.open_workplace_properties()
            return
        except Exception:
            pass
        self._placeholder_message("Einstellungen", "Platzhalter: Einstellungen")

# ---------------------------------------------------------------------------
# Kompatibilitäts-Alias für den festen Sidebar-Bereich.
#
# MainWindow verwendet in diesem Stand bereits `FixedSidebarWidget(...)`,
# während die konkrete Implementierung oben noch `FormDesignerDock` heißt.
# Damit der bestehende Code unverändert weiterlaufen kann, bleibt beides gültig.
# ---------------------------------------------------------------------------
class FixedSidebarWidget(FormDesignerDock):
    pass



class SearchDialogWidget(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        root = QHBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)
        left = QVBoxLayout()
        left.setSpacing(6)
        left.addWidget(QLabel("Search Text:", self))
        self.ed_text = QLineEdit(self)
        left.addWidget(self.ed_text)
        left.addWidget(QLabel("RegEx:", self))
        self.ed_regex = QLineEdit(self)
        left.addWidget(self.ed_regex)
        self.chk_regex = QCheckBox("Use RegEx", self)
        left.addWidget(self.chk_regex)
        self.lbl_result = QLabel("Ready", self)
        left.addWidget(self.lbl_result)
        gb = QGroupBox("Fortführung", self)
        gb_l = QVBoxLayout(gb)
        self.rb_forward = QRadioButton("Suche vorwärts vom Anfang fortführen", gb)
        self.rb_backward = QRadioButton("Suche rückwärts vom Ende fortführen", gb)
        self.rb_forward.setChecked(True)
        gb_l.addWidget(self.rb_forward)
        gb_l.addWidget(self.rb_backward)
        left.addWidget(gb)
        left.addStretch(1)
        right = QVBoxLayout()
        right.setSpacing(6)
        self.btn_search = QPushButton("Search", self)
        self.btn_next = QPushButton("Next", self)
        self.btn_cancel = QPushButton("Cancel", self)
        right.addWidget(self.btn_search)
        right.addWidget(self.btn_next)
        right.addWidget(self.btn_cancel)
        right.addStretch(1)
        root.addLayout(left, 1)
        root.addLayout(right, 0)
        self.btn_search.clicked.connect(lambda: self._do_search(restart=True))
        self.btn_next.clicked.connect(lambda: self._do_search(restart=False))
        self.btn_cancel.clicked.connect(self.close)
        self.ed_text.returnPressed.connect(lambda: self._do_search(restart=True))
        self.ed_regex.returnPressed.connect(lambda: self._do_search(restart=True))

    def _pattern(self):
        if self.chk_regex.isChecked():
            return (self.ed_regex.text() or self.ed_text.text() or '').strip(), True
        return (self.ed_text.text() or '').strip(), False

    def _do_search(self, restart: bool):
        pattern, use_regex = self._pattern()
        if not pattern:
            self.lbl_result.setText("Text was not found")
            return
        backward = self.rb_backward.isChecked()
        ok = False
        try:
            ok = bool(self.main_window.find_in_active_editor(pattern, use_regex=use_regex, restart=restart, backward=backward))
        except Exception:
            ok = False
        self.lbl_result.setText("Text was found" if ok else "Text was not found")


class ReplaceDialogWidget(QWidget):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(6)
        root.addWidget(QLabel("Search Text:", self))
        self.ed_search = QLineEdit(self)
        root.addWidget(self.ed_search)
        root.addWidget(QLabel("Replace With:", self))
        self.ed_replace = QLineEdit(self)
        root.addWidget(self.ed_replace)
        self.chk_regex = QCheckBox("Use RegEx", self)
        root.addWidget(self.chk_regex)
        self.lbl_result = QLabel("Ready", self)
        root.addWidget(self.lbl_result)
        btns = QHBoxLayout()
        btns.addStretch(1)
        self.btn_apply = QPushButton("Replace", self)
        self.btn_cancel = QPushButton("Cancel", self)
        btns.addWidget(self.btn_apply)
        btns.addWidget(self.btn_cancel)
        root.addLayout(btns)
        self.btn_apply.clicked.connect(self._do_replace)
        self.btn_cancel.clicked.connect(self.close)

    def _do_replace(self):
        pattern = (self.ed_search.text() or '').strip()
        repl = self.ed_replace.text() or ''
        if not pattern:
            self.lbl_result.setText("Text was not found")
            return
        ok = False
        try:
            ok = bool(self.main_window.replace_in_active_editor(pattern, repl, use_regex=self.chk_regex.isChecked()))
        except Exception:
            ok = False
        self.lbl_result.setText("Text was found" if ok else "Text was not found")

class _LocalizeLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code_editor.lineNumberAreaPaintEvent(event)


class LocalizeCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._line_number_area = _LocalizeLineNumberArea(self)
        try:
            self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
            self.updateRequest.connect(self.updateLineNumberArea)
            self.cursorPositionChanged.connect(self.highlightCurrentLine)
        except Exception:
            pass
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        self.setFont(QFont("Arial", 10))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

    def lineNumberAreaWidth(self):
        digits = 1
        maximum = max(1, self.blockCount())
        while maximum >= 10:
            maximum //= 10
            digits += 1
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self._line_number_area)
        painter.fillRect(event.rect(), QColor(28, 28, 28))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(170, 170, 170))
                painter.drawText(0, top, self._line_number_area.width() - 4, self.fontMetrics().height(), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlightCurrentLine(self):
        extra = []
        if not self.isReadOnly():
            sel = QTextEdit.ExtraSelection()
            line_color = QColor(255, 216, 102, 28)
            sel.format.setBackground(line_color)
            sel.format.setProperty(QTextFormat.FullWidthSelection, True)
            sel.cursor = self.textCursor()
            sel.cursor.clearSelection()
            extra.append(sel)
        self.setExtraSelections(extra)


class LocalizeToolWindow(QWidget):
    LANGUAGE_CODES = [
        ("ENU", "English (USA)"),
        ("ENG", "English"),
        ("DEU", "Deutsch"),
        ("FRE", "Français"),
        ("ESP", "Español"),
        ("ITA", "Italiano"),
        ("NLD", "Nederlands"),
        ("PTB", "Português"),
        ("PLK", "Polski"),
        ("RUS", "Русский"),
    ]

    HEADER_FIELDS = [
        "Project-Id-Version",
        "Report-Msgid-Bugs-To",
        "POT-Creation-Date",
        "PO-Revision-Date",
        "Last-Translator",
        "Language-Team",
        "Language",
        "MIME-Version",
        "Content-Type",
        "Content-Transfer-Encoding",
    ]

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.entries = []
        self._current_index = -1
        self._block_lang_sync = False
        self.setFont(QFont("Arial", 10))
        self.setAttribute(Qt.WA_DeleteOnClose, False)
        self._build_ui()
        self._load_state()
        self._apply_default_headers()
        try:
            if hasattr(self, "_sync_language_buttons"):
                self._sync_language_buttons()
        except Exception:
            pass
        self._refresh_msgid_list()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
        root.setSpacing(8)

        self.tabs = QTabWidget(self)
        root.addWidget(self.tabs, 1)

        self.tabs.addTab(self._build_entries_tab(), "Entries")
        self.tabs.addTab(self._build_settings_tab(), "Settings")

        btn_row = QHBoxLayout()
        self.btn_create = QPushButton("Create", self)
        self.btn_help   = QPushButton("Help", self)
        self.btn_cancel = QPushButton("Cancel", self)
        for b in (self.btn_create, self.btn_help, self.btn_cancel):
            b.setMinimumWidth(95)
            btn_row.addWidget(b)
        root.addLayout(btn_row)

        self.btn_create.clicked.connect(self._create_mo_file)
        self.btn_help  .clicked.connect(self._show_help)
        self.btn_cancel.clicked.connect(self._close_self)

    def _build_entries_tab(self):
        content = QWidget()
        outer = QHBoxLayout(content)
        outer.setContentsMargins(10, 10, 10, 10)
        outer.setSpacing(12)

        left_col = QVBoxLayout()
        left_col.setSpacing(10)
        lang_row = QHBoxLayout()
        lang_row.setSpacing(8)

        self.gb_source  = QGroupBox("Source", content)
        self.gb_dest    = QGroupBox("Destination", content)
        self.src_group  = QButtonGroup(self)
        self.dst_group  = QButtonGroup(self)
        self.src_radios = {}
        self.dst_radios = {}

        src_lay = QVBoxLayout(self.gb_source)
        dst_lay = QVBoxLayout(self.gb_dest)
        src_lay.setSpacing(4)
        dst_lay.setSpacing(4)
        for code, title in self.LANGUAGE_CODES:
            rb_src = QRadioButton(code, self.gb_source)
            rb_src.setToolTip(title)
            self.src_group.addButton(rb_src)
            self.src_radios[code] = rb_src
            src_lay.addWidget(rb_src)
            rb_dst = QRadioButton(code, self.gb_dest)
            rb_dst.setToolTip(title)
            self.dst_group.addButton(rb_dst)
            self.dst_radios[code] = rb_dst
            dst_lay.addWidget(rb_dst)
        lang_row.addWidget(self.gb_source)
        lang_row.addWidget(self.gb_dest)
        left_col.addLayout(lang_row)

        self.msgid_list = QListWidget(content)
        self.msgid_list.setMinimumWidth(240)
        left_col.addWidget(self.msgid_list, 1)

        editor_col = QVBoxLayout()
        editor_col.setSpacing(6)
        editor_col.addWidget(QLabel("MSGID:", content))
        self.ed_msgid = QLineEdit(content)
        self.ed_msgid.setFont(QFont("Arial", 10))
        editor_col.addWidget(self.ed_msgid)
        editor_col.addWidget(QLabel("MSGSTR:", content))
        self.text_msgstr = LocalizeCodeEditor(content)
        self.text_msgstr.setMinimumSize(420, 340)
        editor_col.addWidget(self.text_msgstr, 1)

        btn_col = QVBoxLayout()
        btn_col.setSpacing(6)
        
        self.btn_insert       = QPushButton(share.locales.tr("Insert")        , content)
        self.btn_apply        = QPushButton(share.locales.tr("Apply")         , content)
        self.btn_delete_msgid = QPushButton(share.locales.tr("Delete MSGID")  , content)
        #
        self.btn_open_po      = QPushButton(share.locales.tr("Open")          , content)
        #
        self.btn_save_po      = QPushButton(share.locales.tr("Save")          , content)
        self.btn_save_as_po   = QPushButton(share.locales.tr("Save As ...")   , content)
        #
        self.btn_paste        = QPushButton(share.locales.tr("Paste")         , content)
        self.btn_cut          = QPushButton(share.locales.tr("Cut")           , content)
        self.btn_delete_text  = QPushButton(share.locales.tr("Delete")        , content)

        for b in (
            self.btn_insert,
            self.btn_apply,
            self.btn_delete_msgid,
            #
            self.btn_open_po,
            #
            self.btn_save_po,
            self.btn_save_as_po,
            #
            self.btn_paste,
            self.btn_cut,
            self.btn_delete_text,
        ):
            b.setMinimumWidth(110)
        
        btn_col.addWidget(self.btn_insert)
        btn_col.addWidget(self.btn_apply)
        btn_col.addWidget(self.btn_delete_msgid)
        btn_col.addSpacing(2)
        
        btn_col.addWidget(self.btn_open_po)
        btn_col.addWidget(self.btn_save_po)
        btn_col.addWidget(self.btn_save_as_po)
        btn_col.addSpacing(2)
        
        btn_col.addWidget(self.btn_paste)
        btn_col.addWidget(self.btn_cut)
        btn_col.addWidget(self.btn_delete_text)
        btn_col.addSpacing(2)

        btn_col.addStretch(1)

        outer.addLayout(btn_col, 0)
        outer.addLayout(editor_col, 1)
        outer.addLayout(left_col, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(content)
        
        self.msgid_list         .currentRowChanged.connect(self._on_msgid_selection_changed)
        
        self.src_group          .buttonClicked.connect(self._sync_language_buttons)
        self.dst_group          .buttonClicked.connect(self._sync_language_buttons)
        
        self.btn_save_po        .clicked.connect(self._save_po)
        self.btn_save_as_po     .clicked.connect(self._save_po_as)
        
        self.btn_open_po.clicked.connect(self._choose_and_open_po)
        self.btn_paste.clicked  .connect(self._paste_into_focused)
        self.btn_cut.clicked    .connect(self._cut_from_focused)
        
        self.btn_delete_text    .clicked.connect(self._delete_in_focused)
        self.btn_delete_msgid   .clicked.connect(self._delete_selected_entry)
        
        self.btn_insert.clicked .connect(self._insert_entry)
        self.btn_apply.clicked  .connect(self._apply_entry)
        
        return scroll

    def _build_settings_tab(self):
        content = QWidget()
        lay = QGridLayout(content)
        lay.setContentsMargins(10, 10, 10, 10)
        lay.setHorizontalSpacing(8)
        lay.setVerticalSpacing(8)

        row = 0
        lay.addWidget(QLabel("Input file (*.po):", content), row, 0)
        self.ed_po_path = QLineEdit(content)
        self.ed_po_path.setFont(QFont("Arial", 10))
        lay.addWidget(self.ed_po_path, row, 1)
        self.btn_load_po_path = QPushButton("Load", content)
        lay.addWidget(self.btn_load_po_path, row, 2)
        row += 1

        lay.addWidget(QLabel("Output file (*.mo):", content), row, 0)
        self.ed_mo_path = QLineEdit(content)
        self.ed_mo_path.setFont(QFont("Arial", 10))
        lay.addWidget(self.ed_mo_path, row, 1)
        self.btn_load_mo_path = QPushButton("Load", content)
        lay.addWidget(self.btn_load_mo_path, row, 2)
        row += 1

        self.header_edits = {}
        for header in self.HEADER_FIELDS:
            lay.addWidget(QLabel(header + ":", content), row, 0)
            ed = QLineEdit(content)
            ed.setFont(QFont("Arial", 10))
            self.header_edits[header] = ed
            lay.addWidget(ed, row, 1, 1, 2)
            row += 1

        lay.setColumnStretch(1, 1)
        lay.setRowStretch(row, 1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(content)

        self.btn_load_po_path.clicked.connect(self._choose_and_open_po)
        self.btn_load_mo_path.clicked.connect(self._choose_mo_path)
        try:
            self.header_edits['Language'].editingFinished.connect(self._apply_language_from_header)
        except Exception:
            pass
        return scroll

    def _focused_text_widget(self):
        fw = QApplication.focusWidget()
        if isinstance(fw, (QLineEdit, QTextEdit, QPlainTextEdit)):
            return fw
        return self.text_msgstr

    def _paste_into_focused(self):
        w = self._focused_text_widget()
        try:
            w.paste()
        except Exception:
            pass

    def _cut_from_focused(self):
        w = self._focused_text_widget()
        try:
            w.cut()
        except Exception:
            pass

    def _delete_in_focused(self):
        w = self._focused_text_widget()
        try:
            if isinstance(w, QLineEdit):
                if w.hasSelectedText():
                    txt = w.text()
                    a = w.selectionStart()
                    b = a + len(w.selectedText())
                    w.setText(txt[:a] + txt[b:])
                    w.setCursorPosition(a)
                else:
                    w.clear()
            else:
                tc = w.textCursor()
                if tc.hasSelection():
                    tc.removeSelectedText()
                    w.setTextCursor(tc)
                else:
                    tc.select(QTextCursor.LineUnderCursor)
                    tc.removeSelectedText()
                    w.setTextCursor(tc)
        except Exception:
            pass

    def _normalize_text(self, text):
        return (text or "").replace("\r\n", "\n").replace("\r", "\n")

    def _escape_po_text(self, text):
        return (text or "").replace('\\', '\\\\').replace('"', '\\"').replace('\t', '\\t')

    def _serialize_po_lines(self, text):
        text = self._normalize_text(text)
        parts = text.split('\n')
        if parts == ['']:
            return ['""']
        out = []
        for idx, part in enumerate(parts):
            suffix = '\\n' if idx < len(parts) - 1 else ''
            out.append(f'"{self._escape_po_text(part)}{suffix}"')
        return out or ['""']

    def _language_schema_value(self):
        return f"{self._current_source_code()}:{self._current_destination_code()}"

    def _parse_language_schema(self, value):
        text = (value or '').strip().upper()
        if ':' not in text:
            return 'ENU', 'DEU'
        src, dst = [part.strip() for part in text.split(':', 1)]
        if src not in self.src_radios or dst not in self.dst_radios or src == dst:
            return 'ENU', 'DEU'
        return src, dst

    def _set_language_pair(self, src, dst):
        src, dst = self._parse_language_schema(f"{src}:{dst}")
        self._block_lang_sync = True
        try:
            if src in self.src_radios:
                self.src_radios[src].setChecked(True)
            else:
                self.src_radios['ENU'].setChecked(True)
            if dst in self.dst_radios:
                self.dst_radios[dst].setChecked(True)
            else:
                self.dst_radios['DEU'].setChecked(True)
        finally:
            self._block_lang_sync = False
        self._sync_language_buttons()

    def _apply_language_from_header(self):
        value = self.header_edits.get('Language', QLineEdit()).text().strip()
        src, dst = self._parse_language_schema(value)
        self._set_language_pair(src, dst)

    def _metadata(self):
        data = {}
        for key, ed in self.header_edits.items():
            data[key] = (ed.text() or "").strip()
        data["Language"] = self._language_schema_value()
        return data

    def _serialize_po_content(self):
        meta = self._metadata()
        lines = []
        lines.append('msgid ""')
        lines.append('msgstr ""')
        for key in self.HEADER_FIELDS:
            value = meta.get(key, "")
            value = f"{key}: {value}" if value else f"{key}:"
            lines.append(f'"{self._escape_po_text(value)}\\n"')
        lines.append("")
        for entry in self.entries:
            msgid = self._normalize_text(entry.get('msgid', ''))
            msgstr = self._normalize_text(entry.get('msgstr', ''))
            lines.append('msgid ""')
            lines.extend(self._serialize_po_lines(msgid))
            lines.append('msgstr ""')
            lines.extend(self._serialize_po_lines(msgstr))
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    def _find_entry_index(self, msgid):
        msgid = self._normalize_text(msgid)
        for idx, entry in enumerate(self.entries):
            if self._normalize_text(entry.get('msgid', '')) == msgid:
                return idx
        return -1

    def _duplicate_msgids(self):
        counts = {}
        for entry in self.entries:
            msgid = self._normalize_text(entry.get('msgid', ''))
            counts[msgid] = counts.get(msgid, 0) + 1
        return {msgid for msgid, count in counts.items() if msgid and count > 1}

    def _refresh_msgid_list(self, select_index=None):
        self.msgid_list.blockSignals(True)
        self.msgid_list.clear()
        duplicate_ids = self._duplicate_msgids()
        for entry in self.entries:
            raw_msgid = self._normalize_text(entry.get('msgid', ''))
            title = raw_msgid.replace('\n', ' ⏎ ')
            item = QListWidgetItem(title)
            if raw_msgid in duplicate_ids:
                item.setBackground(QColor('#b00000'))
                item.setForeground(QColor('#ffffff'))
            self.msgid_list.addItem(item)
        self.msgid_list.blockSignals(False)
        if self.entries:
            if select_index is None:
                select_index = 0 if self._current_index < 0 else min(self._current_index, len(self.entries) - 1)
            self.msgid_list.setCurrentRow(max(0, min(select_index, len(self.entries) - 1)))
        else:
            self._current_index = -1
            self.ed_msgid.clear()
            self.text_msgstr.clear()

    def _on_msgid_selection_changed(self, row):
        if row < 0 or row >= len(self.entries):
            self._current_index = -1
            return
        self._current_index = row
        entry = self.entries[row]
        self.ed_msgid.setText(self._normalize_text(entry.get('msgid', '')))
        self.text_msgstr.setPlainText(self._normalize_text(entry.get('msgstr', '')))

    def _insert_entry(self):
        msgid = self._normalize_text(self.ed_msgid.text())
        msgstr = self._normalize_text(self.text_msgstr.toPlainText())
        if not msgid:
            QMessageBox.warning(self, 'Localize', 'Bitte zuerst eine MSGID eingeben.')
            self.ed_msgid.setFocus()
            return
        idx = self._find_entry_index(msgid)
        if idx >= 0:
            self.entries[idx]['msgstr'] = msgstr
            self._current_index = idx
        else:
            self.entries.append({'msgid': msgid, 'msgstr': msgstr})
            self._current_index = len(self.entries) - 1
        self._refresh_msgid_list(select_index=self._current_index)

    def _apply_entry(self):
        if self._current_index < 0 or self._current_index >= len(self.entries):
            self._insert_entry()
            return
        msgid = self._normalize_text(self.ed_msgid.text())
        msgstr = self._normalize_text(self.text_msgstr.toPlainText())
        if not msgid:
            QMessageBox.warning(self, 'Localize', 'Bitte zuerst eine MSGID eingeben.')
            return
        old_msgid = self._normalize_text(self.entries[self._current_index].get('msgid', ''))
        other = self._find_entry_index(msgid)
        if other >= 0 and other != self._current_index and msgid != old_msgid:
            QMessageBox.warning(self, 'Localize', 'Die MSGID existiert bereits.')
            return
        self.entries[self._current_index] = {'msgid': msgid, 'msgstr': msgstr}
        self._refresh_msgid_list(select_index=self._current_index)

    def _delete_selected_entry(self):
        row = self.msgid_list.currentRow()
        if row < 0 or row >= len(self.entries):
            return
        del self.entries[row]
        self._current_index = -1
        self._refresh_msgid_list(select_index=min(row, len(self.entries) - 1))

    def _choose_and_open_po(self):
        start = self.ed_po_path.text().strip() or os.getcwd()
        path, _ = QFileDialog.getOpenFileName(self, 'PO-Datei öffnen', start, 'PO Dateien (*.po);;Alle Dateien (*.*)')
        path = (path or '').strip()
        if not path:
            return
        self.ed_po_path.setText(path)
        self._open_po(path)

    def _choose_mo_path(self):
        start = self.ed_mo_path.text().strip() or os.getcwd()
        path, _ = QFileDialog.getSaveFileName(self, 'MO-Datei auswählen', start, 'MO Dateien (*.mo);;Alle Dateien (*.*)')
        path = (path or '').strip()
        if not path:
            return
        self.ed_mo_path.setText(path)

    def _open_po(self, path):
        path = os.path.normpath((path or '').strip())
        if not path:
            return
        try:
            import polib
        except Exception as e:
            QMessageBox.warning(self, 'Localize', f'polib konnte nicht geladen werden:\n{e}')
            return
        try:
            po = polib.pofile(path)
            self.entries = []
            for entry in po:
                if getattr(entry, 'obsolete', False):
                    continue
                self.entries.append({'msgid': self._normalize_text(entry.msgid), 'msgstr': self._normalize_text(entry.msgstr)})
            for key in self.HEADER_FIELDS:
                self.header_edits[key].setText(po.metadata.get(key, ''))
            schema = (self.header_edits.get('Language', QLineEdit()).text() or '').strip()
            src, dst = self._parse_language_schema(schema)
            self._set_language_pair(src, dst)
            self.header_edits['Language'].setText(self._language_schema_value())
            self._refresh_msgid_list(select_index=0)
            self._save_state()
        except Exception as e:
            QMessageBox.warning(self, 'Localize', f'PO-Datei konnte nicht geladen werden:\n{e}')

    def _sort_entries_by_msgid(self):
        current_msgid = self._normalize_text(self.ed_msgid.text())
        self.entries.sort(key=lambda entry: self._normalize_text(entry.get('msgid', '')))
        select_index = None
        if current_msgid:
            idx = self._find_entry_index(current_msgid)
            if idx >= 0:
                select_index = idx
        self._refresh_msgid_list(select_index=select_index)

    def _write_po_file(self, path):
        path = os.path.normpath((path or '').strip())
        if not path:
            raise ValueError('Kein Dateiname für die Eingabedatei (*.po) angegeben.')
        self._sort_entries_by_msgid()
        folder = os.path.dirname(path) or os.getcwd()
        os.makedirs(folder, exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self._serialize_po_content())
        self.ed_po_path.setText(path)
        self._save_state()

    def _save_po(self):
        path = self.ed_po_path.text().strip()
        if not path:
            return self._save_po_as()
        try:
            self._write_po_file(path)
            QMessageBox.information(self, 'Localize', 'PO-Datei wurde gespeichert.')
        except Exception as e:
            QMessageBox.warning(self, 'Localize', f'PO-Datei konnte nicht gespeichert werden:\n{e}')

    def _save_po_as(self):
        start = self.ed_po_path.text().strip() or os.path.join(os.getcwd(), 'messages.po')
        path, _ = QFileDialog.getSaveFileName(self, 'PO-Datei speichern', start, 'PO Dateien (*.po);;Alle Dateien (*.*)')
        path = (path or '').strip()
        if not path:
            return
        try:
            self._write_po_file(path)
            QMessageBox.information(self, 'Localize', 'PO-Datei wurde gespeichert.')
        except Exception as e:
            QMessageBox.warning(self, 'Localize', f'PO-Datei konnte nicht gespeichert werden:\n{e}')

    def _ensure_output_writable(self, path):
        folder = os.path.dirname(path) or os.getcwd()
        os.makedirs(folder, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(prefix='localize_', suffix='.tmp', dir=folder)
        os.close(fd)
        os.remove(tmp_path)

    def _create_mo_file(self):
        po_path = self.ed_po_path.text().strip()
        mo_path = self.ed_mo_path.text().strip()
        if not po_path:
            QMessageBox.warning(self, 'Localize', 'Bitte zuerst eine Eingabedatei (*.po) angeben.')
            self.tabs.setCurrentIndex(1)
            self.ed_po_path.setFocus()
            return
        if not mo_path:
            QMessageBox.warning(self, 'Localize', 'Bitte zuerst eine Ausgabedatei (*.mo) angeben.')
            self.tabs.setCurrentIndex(1)
            self.ed_mo_path.setFocus()
            return
        try:
            self._write_po_file(po_path)
            self._ensure_output_writable(mo_path)
            import polib
            po = polib.pofile(po_path)
            po.save_as_mofile(mo_path)
            QMessageBox.information(self, 'Localize', 'MO-Datei wurde erzeugt.')
        except Exception as e:
            QMessageBox.warning(self, 'Localize', f'MO-Datei konnte nicht erzeugt werden:\n{e}')

    def _show_help(self):
        try:
            help_mw = share.utildef.helpwin.HelpMainWindow()
            open_helpwindow(self.main_window.mdi, help_mw)
        except Exception:
            QMessageBox.information(self, 'Help', 'Keine Hilfe verfügbar.')

    def _close_self(self):
        try:
            self._save_state()
        except Exception:
            pass
        try:
            host = self.parent()
            if isinstance(host, QMdiSubWindow):
                host.close()
                return
        except Exception:
            pass
        try:
            self.close()
        except Exception:
            pass

    def closeEvent(self, event):
        try:
            self._save_state()
        except Exception:
            pass
        super().closeEvent(event)

    def _current_source_code(self):
        for code, rb in self.src_radios.items():
            if rb.isChecked():
                return code
        return 'ENU'

    def _current_destination_code(self):
        for code, rb in self.dst_radios.items():
            if rb.isChecked():
                return code
        return 'DEU'

    def _sync_language_buttons(self):
        if self._block_lang_sync:
            return
        self._block_lang_sync = True
        try:
            src = self._current_source_code()
            dst = self._current_destination_code()
            for code, rb in self.src_radios.items():
                rb.setEnabled(code != dst)
            for code, rb in self.dst_radios.items():
                rb.setEnabled(code != src)
            if src == dst:
                src, dst = self._parse_language_schema('ENU:DEU')
                if src in self.src_radios:
                    self.src_radios[src].setChecked(True)
                if dst in self.dst_radios:
                    self.dst_radios[dst].setChecked(True)
                for code, rb in self.src_radios.items():
                    rb.setEnabled(code != dst)
                for code, rb in self.dst_radios.items():
                    rb.setEnabled(code != src)
            self.header_edits.get('Language', QLineEdit()).setText(self._language_schema_value())
        finally:
            self._block_lang_sync = False

    def _apply_default_headers(self):
        now = QDateTime.currentDateTime().toString('yyyy-MM-dd HH:mmZ')
        defaults = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': '',
            'POT-Creation-Date': now,
            'PO-Revision-Date': now,
            'Last-Translator': '',
            'Language-Team': '',
            'Language': self._language_schema_value(),
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=UTF-8',
            'Content-Transfer-Encoding': '8bit',
        }
        for key, value in defaults.items():
            if not self.header_edits[key].text().strip():
                self.header_edits[key].setText(value)

    def _load_state(self):
        try:
            schema = (self.main_window._settings.value('localize/header/Language', '', type=str) or '').strip()
            if not schema:
                src_saved = (self.main_window._settings.value('localize/source_lang', 'ENU', type=str) or 'ENU').strip()
                dst_saved = (self.main_window._settings.value('localize/dest_lang', 'DEU', type=str) or 'DEU').strip()
                schema = f"{src_saved}:{dst_saved}"
            src, dst = self._parse_language_schema(schema)
            self._set_language_pair(src, dst)
            self.ed_po_path.setText((self.main_window._settings.value('localize/po_path', '', type=str) or '').strip())
            self.ed_mo_path.setText((self.main_window._settings.value('localize/mo_path', '', type=str) or '').strip())
            for key in self.HEADER_FIELDS:
                self.header_edits[key].setText((self.main_window._settings.value(f'localize/header/{key}', '', type=str) or '').strip())
            self.header_edits['Language'].setText(self._language_schema_value())
        except Exception:
            try:
                self._set_language_pair('ENU', 'DEU')
                self.header_edits['Language'].setText(self._language_schema_value())
            except Exception:
                pass

    def _save_state(self):
        try:
            self.header_edits['Language'].setText(self._language_schema_value())
            self.main_window._settings.setValue('localize/source_lang'  , self._current_source_code())
            self.main_window._settings.setValue('localize/dest_lang'    , self._current_destination_code())
            self.main_window._settings.setValue('localize/po_path'      , self.ed_po_path.text().strip())
            self.main_window._settings.setValue('localize/mo_path'      , self.ed_mo_path.text().strip())
            for key in self.HEADER_FIELDS:
                self.main_window._settings.setValue(f'localize/header/{key}', self.header_edits[key].text().strip())
        except Exception:
            pass


class ProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(share.locales.tr("Project"))
        self.resize(760, 440)
        self._project_file_path = ""

        root_layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)

        # ------------------------------------------------------------------
        # Tab 1: Allgemein
        # ------------------------------------------------------------------
        self.tab_general = QWidget(self)
        self.tab_general.setObjectName("project_tab_general")
        general_layout = QVBoxLayout(self.tab_general)

        self.ed_path = QLineEdit(self.tab_general)
        self.ed_path.setObjectName("project_path_edit")
        general_layout.addWidget(self.ed_path, 0)

        self.split_vertical = QSplitter(Qt.Vertical, self.tab_general)
        self.split_vertical.setObjectName("project_splitter_vertical")

        self.split_horizontal = QSplitter(Qt.Horizontal, self.split_vertical)
        self.split_horizontal.setObjectName("project_splitter_horizontal")

        self.tree_project = QTreeWidget(self.split_horizontal)
        self.tree_project.setObjectName("project_tree")
        self.tree_project.setHeaderHidden(True)
        self.tree_project.setColumnCount(1)
        self.tree_project.setMinimumWidth(220)

        self.project_roots = {}
        for key, caption in [
            ("forms", share.locales.tr("Formulare")),
            ("programs", share.locales.tr("Programme")),
            ("reports", share.locales.tr("Berichte")),
            ("queries", share.locales.tr("Abfragen")),
            ("internet", share.locales.tr("Internet")),
            ("localize", share.locales.tr("Localize")),
            ("graphics", share.locales.tr("Grafiken")),
            ("misc", share.locales.tr("Sonstiges")),
        ]:
            item = QTreeWidgetItem([caption])
            item.setData(0, Qt.UserRole, {"kind": "root", "root_key": key})
            self.tree_project.addTopLevelItem(item)
            self.project_roots[key] = item

        self._project_clipboard = None
        self.tree_project.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_project.customContextMenuRequested.connect(self._on_project_tree_context_menu)

        right_side = QWidget(self.split_horizontal)
        right_side.setObjectName("project_right_side")
        right_side_layout = QHBoxLayout(right_side)
        right_side_layout.setContentsMargins(0, 0, 0, 0)
        right_side_layout.setSpacing(6)

        scroll_host = QWidget(right_side)
        scroll_host.setObjectName("project_scroll_host")
        scroll_host.setMinimumWidth(330)
        scroll_host_layout = QVBoxLayout(scroll_host)
        scroll_host_layout.setContentsMargins(0, 0, 0, 0)
        scroll_host_layout.setSpacing(0)

        self.scroll_area = QScrollArea(scroll_host)
        self.scroll_area.setObjectName("project_scroll_area")
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget(self.scroll_area)
        self.scroll_widget.setObjectName("project_scroll_widget")
        self.scroll_form_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_form_layout.setContentsMargins(6, 6, 6, 6)
        self.scroll_form_layout.setSpacing(8)

        manifest_form = QFormLayout()
        self.ed_manifest_version = QLineEdit(self.scroll_widget)
        self.ed_manifest_version.setObjectName("project_manifest_version")
        manifest_form.addRow(share.locales.tr("Manifest-Version"), self.ed_manifest_version)
        self.scroll_form_layout.addLayout(manifest_form)

        self.gb_identity = QGroupBox(share.locales.tr("Identity"), self.scroll_widget)
        identity_form = QFormLayout(self.gb_identity)
        self.ed_identity_type = QLineEdit(self.gb_identity)
        self.ed_identity_name = QLineEdit(self.gb_identity)
        self.ed_identity_language = QLineEdit(self.gb_identity)
        self.ed_identity_arch = QLineEdit(self.gb_identity)
        self.ed_identity_version = QLineEdit(self.gb_identity)
        self.ed_identity_public_key = QLineEdit(self.gb_identity)
        identity_form.addRow(share.locales.tr("Art"), self.ed_identity_type)
        identity_form.addRow(share.locales.tr("Name"), self.ed_identity_name)
        identity_form.addRow(share.locales.tr("Sprache"), self.ed_identity_language)
        identity_form.addRow(share.locales.tr("Prozessor-Architektur"), self.ed_identity_arch)
        identity_form.addRow(share.locales.tr("Version"), self.ed_identity_version)
        identity_form.addRow(share.locales.tr("publicKeyToken"), self.ed_identity_public_key)
        self.scroll_form_layout.addWidget(self.gb_identity)

        self.gb_compat = QGroupBox(share.locales.tr("Kompatibilität"), self.scroll_widget)
        compat_layout = QVBoxLayout(self.gb_compat)

        self.gb_application = QGroupBox(share.locales.tr("Anwendung"), self.gb_compat)
        application_layout = QVBoxLayout(self.gb_application)

        self.gb_supported_os = QGroupBox(share.locales.tr("Unterstützte OS"), self.gb_application)
        os_layout = QVBoxLayout(self.gb_supported_os)
        self.chk_os_xp = QCheckBox("Windows XP", self.gb_supported_os)
        self.chk_os_vista = QCheckBox("Windows Vista", self.gb_supported_os)
        self.chk_os_7 = QCheckBox("Windows 7", self.gb_supported_os)
        self.chk_os_8 = QCheckBox("Windows 8", self.gb_supported_os)
        self.chk_os_81 = QCheckBox("Windows 8.1", self.gb_supported_os)
        self.chk_os_10 = QCheckBox("Windows 10", self.gb_supported_os)
        self.chk_os_11 = QCheckBox("Windows 11", self.gb_supported_os)
        for chk in [
            self.chk_os_xp,
            self.chk_os_vista,
            self.chk_os_7,
            self.chk_os_8,
            self.chk_os_81,
            self.chk_os_10,
            self.chk_os_11,
        ]:
            os_layout.addWidget(chk)
        application_layout.addWidget(self.gb_supported_os)

        app_form = QFormLayout()
        self.ed_active_codepage = QLineEdit(self.gb_application)
        self.cb_supported_arch = QComboBox(self.gb_application)
        self.cb_supported_arch.addItems([
            "",
            "x86",
            "x64",
            "arm64",
            "x86,x64",
            "x86,x64,arm64",
        ])
        app_form.addRow(share.locales.tr("Aktive CodePage"), self.ed_active_codepage)
        app_form.addRow(share.locales.tr("supported Architectures"), self.cb_supported_arch)
        application_layout.addLayout(app_form)

        self.gb_console_policies = QGroupBox("consolePolicies", self.gb_application)
        console_layout = QVBoxLayout(self.gb_console_policies)
        self.chk_console_v2 = QCheckBox("V2", self.gb_console_policies)
        self.chk_console_force_v1 = QCheckBox("ForceV1", self.gb_console_policies)
        self.chk_console_terminal = QCheckBox("TerminalLevelAware", self.gb_console_policies)
        self.chk_console_wrap = QCheckBox("WrapTextAtEOL", self.gb_console_policies)
        for chk in [
            self.chk_console_v2,
            self.chk_console_force_v1,
            self.chk_console_terminal,
            self.chk_console_wrap,
        ]:
            console_layout.addWidget(chk)
        application_layout.addWidget(self.gb_console_policies)

        compat_layout.addWidget(self.gb_application)
        self.scroll_form_layout.addWidget(self.gb_compat)
        self.scroll_form_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_widget)
        scroll_host_layout.addWidget(self.scroll_area, 1)

        self.button_panel = QWidget(right_side)
        self.button_panel.setObjectName("project_button_panel")
        button_layout = QVBoxLayout(self.button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(6)

        self.btn_load = QPushButton(share.locales.tr("Laden"), self.button_panel)
        self.btn_save = QPushButton(share.locales.tr("Speichern"), self.button_panel)
        self.btn_save_as = QPushButton(share.locales.tr("Speichern unter"), self.button_panel)
        self.btn_cancel = QPushButton(share.locales.tr("Cancel"), self.button_panel)

        self.btn_load.setObjectName("project_btn_load")
        self.btn_save.setObjectName("project_btn_save")
        self.btn_save_as.setObjectName("project_btn_save_as")
        self.btn_cancel.setObjectName("project_btn_cancel")

        button_layout.addWidget(self.btn_load)
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_save_as)
        button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch(1)

        right_side_layout.addWidget(scroll_host, 1)
        right_side_layout.addWidget(self.button_panel, 0)

        self.split_horizontal.setChildrenCollapsible(False)
        self.split_horizontal.setStretchFactor(0, 1)
        self.split_horizontal.setStretchFactor(1, 2)

        self.editor_notes = QPlainTextEdit(self.split_vertical)
        self.editor_notes.setObjectName("project_editor")

        self.split_vertical.setStretchFactor(0, 3)
        self.split_vertical.setStretchFactor(1, 2)

        general_layout.addWidget(self.split_vertical, 1)
        self.tabs.addTab(self.tab_general, share.locales.tr("Allgemein"))

        # ------------------------------------------------------------------
        # Tab 2: GitHub
        # ------------------------------------------------------------------
        self.tab_github = QWidget(self)
        self.tab_github.setObjectName("project_tab_github")
        github_layout = QVBoxLayout(self.tab_github)

        self.gb_github_repo = QGroupBox("GitHub", self.tab_github)
        gh_form = QFormLayout(self.gb_github_repo)
        self.ed_gh_owner = QLineEdit(self.gb_github_repo)
        self.ed_gh_repo = QLineEdit(self.gb_github_repo)
        self.ed_gh_branch = QLineEdit(self.gb_github_repo)
        self.ed_gh_token = QLineEdit(self.gb_github_repo)
        self.ed_gh_token.setEchoMode(QLineEdit.Password)
        gh_form.addRow(share.locales.tr("Owner"), self.ed_gh_owner)
        gh_form.addRow(share.locales.tr("Repository"), self.ed_gh_repo)
        gh_form.addRow(share.locales.tr("Branch"), self.ed_gh_branch)
        gh_form.addRow(share.locales.tr("Token"), self.ed_gh_token)
        github_layout.addWidget(self.gb_github_repo)

        gh_button_row = QHBoxLayout()
        self.btn_gh_init = QPushButton(share.locales.tr("Einrichten"), self.tab_github)
        self.btn_gh_upload = QPushButton(share.locales.tr("Hochladen"), self.tab_github)
        self.btn_gh_download = QPushButton(share.locales.tr("Herunterladen"), self.tab_github)
        gh_button_row.addWidget(self.btn_gh_init)
        gh_button_row.addWidget(self.btn_gh_upload)
        gh_button_row.addWidget(self.btn_gh_download)
        gh_button_row.addStretch(1)
        github_layout.addLayout(gh_button_row)

        self.memo_github = QPlainTextEdit(self.tab_github)
        self.memo_github.setObjectName("project_github_log")
        github_layout.addWidget(self.memo_github, 1)

        self.tabs.addTab(self.tab_github, "GitHub")
        root_layout.addWidget(self.tabs, 1)

        self.btn_cancel.clicked.connect(self.close)
        self.btn_load.clicked.connect(self._on_load_project)
        self.btn_save.clicked.connect(self._on_save_project)
        self.btn_save_as.clicked.connect(self._on_save_project_as)

        try:
            self.split_horizontal.setSizes([240, 480])
        except Exception:
            pass
        try:
            self.split_vertical.setSizes([300, 110])
        except Exception:
            pass
        try:
            self.tree_project.expandAll()
        except Exception:
            pass

    def _project_root(self, key: str):
        return self.project_roots.get(key)

    def _tree_item_payload(self, item):
        try:
            data = item.data(0, Qt.UserRole)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _clear_project_children(self):
        for root in self.project_roots.values():
            while root.childCount():
                root.removeChild(root.child(0))

    def _collect_tree_data(self):
        data = {}
        for key, root in self.project_roots.items():
            files = []
            for i in range(root.childCount()):
                child = root.child(i)
                payload = self._tree_item_payload(child)
                files.append({
                    "text": child.text(0),
                    "path": payload.get("path", ""),
                })
            data[key] = files
        return data

    def _metadata_to_dict(self):
        return {
            "manifest_version": self.ed_manifest_version.text(),
            "identity": {
                "type": self.ed_identity_type.text(),
                "name": self.ed_identity_name.text(),
                "language": self.ed_identity_language.text(),
                "processor_architecture": self.ed_identity_arch.text(),
                "version": self.ed_identity_version.text(),
                "publicKeyToken": self.ed_identity_public_key.text(),
            },
            "application": {
                "supported_os": {
                    "xp": self.chk_os_xp.isChecked(),
                    "vista": self.chk_os_vista.isChecked(),
                    "win7": self.chk_os_7.isChecked(),
                    "win8": self.chk_os_8.isChecked(),
                    "win81": self.chk_os_81.isChecked(),
                    "win10": self.chk_os_10.isChecked(),
                    "win11": self.chk_os_11.isChecked(),
                },
                "active_codepage": self.ed_active_codepage.text(),
                "supported_architectures": self.cb_supported_arch.currentText(),
                "consolePolicies": {
                    "v2": self.chk_console_v2.isChecked(),
                    "force_v1": self.chk_console_force_v1.isChecked(),
                    "terminal_level_aware": self.chk_console_terminal.isChecked(),
                    "wrap_text_at_eol": self.chk_console_wrap.isChecked(),
                },
            },
            "github": {
                "owner": self.ed_gh_owner.text(),
                "repository": self.ed_gh_repo.text(),
                "branch": self.ed_gh_branch.text(),
                "token": self.ed_gh_token.text(),
                "log": self.memo_github.toPlainText(),
            },
            "notes": self.editor_notes.toPlainText(),
            "path_hint": self.ed_path.text(),
        }

    def _apply_metadata(self, meta: dict):
        meta = meta or {}
        identity = meta.get("identity") or {}
        application = meta.get("application") or {}
        supported_os = application.get("supported_os") or {}
        console = application.get("consolePolicies") or {}
        github = meta.get("github") or {}

        self.ed_manifest_version.setText(meta.get("manifest_version", ""))
        self.ed_identity_type.setText(identity.get("type", ""))
        self.ed_identity_name.setText(identity.get("name", ""))
        self.ed_identity_language.setText(identity.get("language", ""))
        self.ed_identity_arch.setText(identity.get("processor_architecture", ""))
        self.ed_identity_version.setText(identity.get("version", ""))
        self.ed_identity_public_key.setText(identity.get("publicKeyToken", ""))

        self.chk_os_xp.setChecked(bool(supported_os.get("xp")))
        self.chk_os_vista.setChecked(bool(supported_os.get("vista")))
        self.chk_os_7.setChecked(bool(supported_os.get("win7")))
        self.chk_os_8.setChecked(bool(supported_os.get("win8")))
        self.chk_os_81.setChecked(bool(supported_os.get("win81")))
        self.chk_os_10.setChecked(bool(supported_os.get("win10")))
        self.chk_os_11.setChecked(bool(supported_os.get("win11")))

        self.ed_active_codepage.setText(application.get("active_codepage", ""))
        idx = self.cb_supported_arch.findText(application.get("supported_architectures", ""))
        self.cb_supported_arch.setCurrentIndex(idx if idx >= 0 else 0)

        self.chk_console_v2.setChecked(bool(console.get("v2")))
        self.chk_console_force_v1.setChecked(bool(console.get("force_v1")))
        self.chk_console_terminal.setChecked(bool(console.get("terminal_level_aware")))
        self.chk_console_wrap.setChecked(bool(console.get("wrap_text_at_eol")))

        self.ed_gh_owner.setText(github.get("owner", ""))
        self.ed_gh_repo.setText(github.get("repository", ""))
        self.ed_gh_branch.setText(github.get("branch", ""))
        self.ed_gh_token.setText(github.get("token", ""))
        self.memo_github.setPlainText(github.get("log", ""))

        self.editor_notes.setPlainText(meta.get("notes", ""))
        self.ed_path.setText(meta.get("path_hint", ""))

    def _project_to_dict(self):
        return {
            "project_file": self._project_file_path,
            "tree": self._collect_tree_data(),
            "meta": self._metadata_to_dict(),
        }

    def _apply_project_dict(self, data: dict):
        self._clear_project_children()

        tree = (data or {}).get("tree") or {}
        for key, items in tree.items():
            root = self._project_root(key)
            if root is None:
                continue
            for entry in items or []:
                file_path = entry.get("path", "")
                text = entry.get("text") or (os.path.basename(file_path) if file_path else "")
                node = QTreeWidgetItem([text])
                node.setData(0, Qt.UserRole, {
                    "kind": "file",
                    "root_key": key,
                    "path": file_path,
                })
                root.addChild(node)
            root.setExpanded(True)

        self._apply_metadata((data or {}).get("meta") or {})
        try:
            self.tree_project.expandAll()
        except Exception:
            pass

    def _save_project_to_file(self, file_path: str):
        data = self._project_to_dict()
        with open(file_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        self._project_file_path = file_path
        self.ed_path.setText(file_path)

    def _load_project_from_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        self._project_file_path = file_path
        self.ed_path.setText(file_path)
        self._apply_project_dict(data)

    def _on_save_project_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            share.locales.tr("Projekt speichern unter"),
            self._project_file_path or "projekt.pro",
            "Projektdateien (*.pro);;Alle Dateien (*.*)",
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".pro"):
            file_path += ".pro"
        self._save_project_to_file(file_path)

    def _on_save_project(self):
        if not self._project_file_path:
            self._on_save_project_as()
            return
        self._save_project_to_file(self._project_file_path)

    def _on_load_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            share.locales.tr("Projekt laden"),
            "",
            "Projektdateien (*.pro);;Alle Dateien (*.*)",
        )
        if not file_path:
            return
        self._load_project_from_file(file_path)

    def _add_files_to_root(self, root_key: str, title: str, file_filter: str):
        root_item = self._project_root(root_key)
        if root_item is None:
            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            share.locales.tr(title),
            "",
            file_filter,
        )
        if not files:
            return

        existing = set()
        for i in range(root_item.childCount()):
            child = root_item.child(i)
            payload = self._tree_item_payload(child)
            path = payload.get("path") or ""
            if path:
                existing.add(os.path.normcase(os.path.normpath(path)))

        for file_path in files:
            norm = os.path.normcase(os.path.normpath(file_path))
            if norm in existing:
                continue
            node = QTreeWidgetItem([os.path.basename(file_path)])
            node.setData(0, Qt.UserRole, {
                "kind": "file",
                "root_key": root_key,
                "path": file_path,
            })
            root_item.addChild(node)
            existing.add(norm)

        root_item.setExpanded(True)

    def _copy_selected_tree_item(self):
        item = self.tree_project.currentItem()
        if item is None:
            return
        payload = self._tree_item_payload(item)
        if payload.get("kind") != "file":
            return
        self._project_clipboard = {
            "text": item.text(0),
            "payload": dict(payload),
        }

    def _paste_tree_item(self):
        clip = self._project_clipboard
        if not isinstance(clip, dict):
            return

        item = self.tree_project.currentItem()
        target_root = None
        if item is not None:
            payload = self._tree_item_payload(item)
            if payload.get("kind") == "root":
                target_root = item
            elif item.parent() is not None:
                target_root = item.parent()

        if target_root is None:
            target_root = self._project_root(clip.get("payload", {}).get("root_key", ""))

        if target_root is None:
            return

        new_payload = dict(clip.get("payload") or {})
        node = QTreeWidgetItem([clip.get("text") or ""])
        node.setData(0, Qt.UserRole, new_payload)
        target_root.addChild(node)
        target_root.setExpanded(True)

    def _delete_selected_tree_item(self):
        item = self.tree_project.currentItem()
        if item is None:
            return
        payload = self._tree_item_payload(item)
        if payload.get("kind") == "root":
            return
        parent = item.parent()
        if parent is None:
            return
        parent.removeChild(item)

    def _on_project_tree_context_menu(self, pos):
        menu = QMenu(self.tree_project)

        m_add = menu.addMenu(share.locales.tr("Hinzufügen"))

        act_add_program = QAction(share.locales.tr("Programm"), self.tree_project)
        act_add_program.triggered.connect(
            lambda: self._add_files_to_root(
                "programs",
                "Datei laden",
                "Programme (*.prg);;Alle Dateien (*.*)"
            )
        )
        m_add.addAction(act_add_program)

        act_add_form = QAction(share.locales.tr("Formular"), self.tree_project)
        act_add_form.triggered.connect(
            lambda: self._add_files_to_root(
                "forms",
                "Datei laden",
                "Formulare (*.wfm *.frm);;Alle Dateien (*.*)"
            )
        )
        m_add.addAction(act_add_form)

        act_add_report = QAction(share.locales.tr("Bericht"), self.tree_project)
        act_add_report.triggered.connect(
            lambda: self._add_files_to_root(
                "reports",
                "Datei laden",
                "Berichte (*.rep *.rpt *.frx *.rtm);;Alle Dateien (*.*)"
            )
        )
        m_add.addAction(act_add_report)

        act_add_sql = QAction(share.locales.tr("SQL"), self.tree_project)
        act_add_sql.triggered.connect(
            lambda: self._add_files_to_root(
                "queries",
                "Datei laden",
                "SQL Dateien (*.sql *.sqlb.json);;Alle Dateien (*.*)"
            )
        )
        m_add.addAction(act_add_sql)

        act_add_graphic = QAction(share.locales.tr("Grafik"), self.tree_project)
        act_add_graphic.triggered.connect(
            lambda: self._add_files_to_root(
                "graphics",
                "Datei laden",
                "Grafiken (*.png *.jpg *.jpeg *.bmp *.gif *.svg *.ico *.webp);;Alle Dateien (*.*)"
            )
        )
        m_add.addAction(act_add_graphic)

        act_add_misc = QAction(share.locales.tr("Sonstiges"), self.tree_project)
        act_add_misc.triggered.connect(
            lambda: self._add_files_to_root(
                "misc",
                "Datei laden",
                "Alle Dateien (*.*)"
            )
        )
        m_add.addAction(act_add_misc)

        menu.addSeparator()

        current_item = self.tree_project.itemAt(pos)
        if current_item is not None:
            self.tree_project.setCurrentItem(current_item)
        payload = self._tree_item_payload(self.tree_project.currentItem()) if self.tree_project.currentItem() else {}

        act_copy = menu.addAction(share.locales.tr("Kopieren"))
        act_copy.setEnabled(payload.get("kind") == "file")
        act_copy.triggered.connect(self._copy_selected_tree_item)

        act_paste = menu.addAction(share.locales.tr("Einfügen"))
        act_paste.setEnabled(isinstance(self._project_clipboard, dict))
        act_paste.triggered.connect(self._paste_tree_item)

        act_delete = menu.addAction(share.locales.tr("Löschen"))
        act_delete.setEnabled(payload.get("kind") == "file")
        act_delete.triggered.connect(self._delete_selected_tree_item)

        menu.exec_(self.tree_project.viewport().mapToGlobal(pos))



class MainWindow(QMainWindow):
    # --- i18n ---------------------------------------------------------------
    # ---------------------------------------------------------------------------
    # Loads <lang>/LC_MESSAGES/dbase.mo from locales.zip and refreshes menu texts.
    # ---------------------------------------------------------------------------
    def _set_language(self, lang: str):
        try:
            share.locales.I18N.load_mo("po/locales/" + lang)
        except Exception:
            pass
        self._retranslate_ui()

    # ---------------------------------------------------------------------------
    # Best-effort retranslate for main menu + window title.
    # ---------------------------------------------------------------------------
    def _retranslate_ui(self):
        try:
            self.setWindowTitle(share.locales.tr(_runner_window_title()))
        except Exception:
            pass

        # Menüs (nur wenn vorhanden)
        try:
            if hasattr(self, "menu_file"):       self.menu_file      .setTitle(share.locales.tr("File"))
            if hasattr(self, "menu_edit"):       self.menu_edit      .setTitle(share.locales.tr("Edit"))
            if hasattr(self, "menu_display"):    self.menu_display   .setTitle(share.locales.tr("View"))
            if hasattr(self, "menu_properties") and self.menu_properties is not None: self.menu_properties.setTitle(share.locales.tr("Properties"))
            if hasattr(self, "menu_windows"):    self.menu_windows   .setTitle(share.locales.tr("Window"))
            if hasattr(self, "menu_help"):       self.menu_help      .setTitle(share.locales.tr("Help"))
            if hasattr(self, "menu_language"):   self.menu_language  .setTitle(share.locales.tr("Language"))
            if hasattr(self, "action_workplace"): self.action_workplace.setText(share.locales.tr("Eigenschaften"))
        except Exception:
            pass

        # Beispiele: ein paar Actions umhängen, wenn sie als Attribute existieren
        try:
            for name, msgid in [
                ("action_file_open", "Open"),
                ("action_file_close", "Close"),
                ("action_file_exit", "Exit"),
                ("act_view_debug_window", "Debug Window"),
                ("act_view_regie", "Control Center"),
                ("act_view_designer", "Designer"),
                ("act_view_editor", "Editor"),
                ("act_view_table", "Table Designer"),
                ("act_view_sql", "SQL Builder"),
                ("act_edit_minimap", "Mini-Map"),
                ("action_help_contents", "Contents"),
                ("action_help_whatis", "What is ... ?"),
                ("action_help_about", "About ..."),
            ]:
                act = getattr(self, name, None)
                if act is not None:
                    act.setText(share.locales.tr(msgid))
            if hasattr(self, 'menu_language'):
                try:
                    self.act_lang_en.setText(share.locales.tr("English"))
                    self.act_lang_de.setText(share.locales.tr("German"))
                except Exception:
                    pass
            if hasattr(self, '_debug_console') and self._debug_console is not None:
                try:
                    for sub in self.mdi.subWindowList():
                        if sub.widget() is self._debug_console:
                            sub.setWindowTitle(share.locales.tr("Debug Window"))
                            break
                except Exception:
                    pass
            if hasattr(self, 'obj_inspector_dock') and self.obj_inspector_dock is not None:
                try:
                    self.obj_inspector_dock.setWindowTitle(share.locales.tr("Object Inspector"))
                except Exception:
                    pass
            if hasattr(self, 'obj_palette_dock') and self.obj_palette_dock is not None:
                try:
                    self.obj_palette_dock.setWindowTitle(share.locales.tr("Object Palette"))
                except Exception:
                    pass
            try:
                for sub in self.mdi.subWindowList():
                    w = sub.widget()
                    if w is getattr(self, 'form_designer_window', None):
                        sub.setWindowTitle(share.locales.tr("Form Designer"))
            except Exception:
                pass
        except Exception:
            pass

    # ---------------------------------------------------------------------------
    # Aktuelles Werkzeug aus der Objektpalette setzen (z.B. 'Button', 'Label', ...).
    # ---------------------------------------------------------------------------
    def set_designer_tool(self, tool_name: str) -> None:
        self.designer_current_tool = (tool_name or "").strip()
        # optional: Statusbar
        try:
            if self.designer_current_tool:
                self.statusBar().showMessage(f"Designer-Tool: {self.designer_current_tool}")
            else:
                self.statusBar().clearMessage()
        except Exception:
            pass


    # --- Designer -> Objektinspektor Sync ---------------------------------
    # ---------------------------------------------------------------------------
    # Wird vom PixelGridCanvas gerufen, wenn sich die Auswahl ändert.
    # ---------------------------------------------------------------------------
    def on_designer_selection_changed(self, ctrl):
        try:
            oi = getattr(self, "object_inspector", None)
            if oi is not None:
                oi.set_current(ctrl)
        except Exception:
            pass

    # ---------------------------------------------------------------------------
    # Wird vom PixelGridCanvas gerufen, wenn Controls hinzugefügt/entfernt werden.
    # ---------------------------------------------------------------------------
    def on_designer_controls_changed(self, controls):
        try:
            oi = getattr(self, "object_inspector", None)
            if oi is not None:
                oi.set_controls_list(controls)
        except Exception:
            pass


    def _create_help_mainwindow(self):
        mw = share.utildef.helpwin.HelpMainWindow()
        try:
            mw.setWindowTitle(share.locales.tr("Help"))
        except Exception:
            pass
        return mw

    def _open_help_topic(self, topic=None):
        try:
            help_widget = self._create_help_mainwindow()
            open_helpwindow(self.mdi, help_widget, topic)
            return True
        except Exception:
            QMessageBox.information(self, share.locales.tr("Help"), share.locales.tr("Keine Hilfe verfügbar."))
            return False

    def set_whatis_mode(self, enabled: bool):
        self._whatis_help_mode = bool(enabled)
        act = getattr(self, "action_help_whatis", None)
        if act is not None and act.isChecked() != self._whatis_help_mode:
            block = act.blockSignals(True)
            act.setChecked(self._whatis_help_mode)
            act.blockSignals(block)
        try:
            if self._whatis_help_mode:
                self.statusBar().showMessage(share.locales.tr("What is ... ? aktiv: Bitte eine Komponente mit der linken Maustaste anklicken."))
            else:
                self.statusBar().clearMessage()
        except Exception:
            pass

    def on_action_help_whatis(self, checked=False):
        self.set_whatis_mode(bool(checked))

    def handle_whatis_click(self, widget):
        if not bool(getattr(self, "_whatis_help_mode", False)):
            return False
        if bool(getattr(self, "_whatis_help_busy", False)):
            return True

        meta = resolve_widget_help(widget)
        if not meta:
            self.set_whatis_mode(False)
            return False

        title = meta.get("title") or _widget_display_name(widget)
        help_id = meta.get("help_id") or f"qt.widgets.{meta.get('class_name') or widget.__class__.__name__}"
        topic = meta.get("topic") or None
        text = meta.get("text") or share.locales.tr("Für dieses Objekt sind noch keine speziellen Hilfetexte hinterlegt.")
        class_name = meta.get("class_name") or widget.__class__.__name__
        object_name = ""
        try:
            object_name = widget.objectName() or ""
        except Exception:
            object_name = ""

        self._whatis_help_busy = True
        self.set_whatis_mode(False)
        try:
            box = QMessageBox(self)
            box.setIcon(QMessageBox.Information)
            box.setWindowTitle(share.locales.tr("What is ... ?"))
            box.setText(f"{title}\n\n{text}")
            details = [
                f"Class: {class_name}",
                f"Help-ID: {help_id}",
            ]
            if object_name:
                details.append(f"ObjectName: {object_name}")
            if topic:
                details.append(f"Topic: {topic}")
            extra = meta.get("extra")
            if extra:
                details.append(f"Meta: {extra}")
            box.setDetailedText("\n".join(details))
            box.setInformativeText(share.locales.tr("Mit 'In Hilfe öffnen' wird die CHM-Hilfe geöffnet. Ohne konkrete Topic-Zuordnung wird die Hauptseite angezeigt."))
            btn_open = box.addButton(share.locales.tr("In Hilfe öffnen"), QMessageBox.AcceptRole)
            box.addButton(QMessageBox.Close)
            box.exec_()
            if box.clickedButton() is btn_open:
                self._open_help_topic(topic)
        finally:
            self._whatis_help_busy = False
        return True

    def on_action_help_contents(self):
        self._open_help_topic(None)

    def on_action_help_about(self):
        title = share.locales.tr("About ...")
        app_name = _runner_window_title()
        text = (
            f"{app_name}\n\n"
            f"(c) 2024, 2025, 2026 Jens Kallup - paule32\n"
            f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
            f"Qt / PyQt5\n\n"
            f"{share.locales.tr('Anwendung zum Bearbeiten und Ausführen von dBase-Projekten.')}"
        )
        QMessageBox.about(self, title, text)

    def eventFilter(self, obj, event):
        try:
            if bool(getattr(self, "_whatis_help_mode", False)) and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                if isinstance(obj, QWidget):
                    if self.handle_whatis_click(obj):
                        try:
                            event.accept()
                        except Exception:
                            pass
                        return True
        except Exception:
            pass
        return super().eventFilter(obj, event)


    def __init__(self):
        super().__init__()

        global MAINAPP
        try:
            MAINAPP = self
            share.common.MAINAPP = self
        except Exception:
            pass

        # INI Settings
        self._settings = QSettings(self._ini_path(), QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

        self._whatis_help_mode = False
        self._whatis_help_busy = False
        self.help_mainwindow = None

        self.mdi = QMdiArea(self)
        
        pal = self.mdi.palette()
        pal.setColor(QPalette.Window, QColor(18, 18, 18))
        self.mdi.setPalette(pal)
        self.mdi.setAutoFillBackground(True)
        
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy  (Qt.ScrollBarAsNeeded)
        
        self.setWindowTitle(_runner_window_title())

        self._central_host = QWidget(self)
        self._central_host_layout = QHBoxLayout(self._central_host)
        self._central_host_layout.setContentsMargins(0, 0, 0, 0)
        self._central_host_layout.setSpacing(0)

        self.sidebar_widget = FixedSidebarWidget(self, self._central_host)
        self.sidebar_widget.setMinimumWidth(100)
        self.sidebar_widget.setMaximumWidth(100)

        self._central_host_layout.addWidget(self.sidebar_widget, 0)
        self._central_host_layout.addWidget(self.mdi, 1)

        self.setCentralWidget(self._central_host)
        
        # Factory: wie dein Help-Fenster erzeugt wird
        def create_help():
            # Beispiel: irgendein HelpMainWindow / HelpWidget
            mw = share.utildef.helpwin.HelpMainWindow()
            mw.setWindowTitle(share.locales.tr("Hilfe"))
            #mw.setCentralWidget(QLabel("Hier kommt die Hilfe rein"))
            return mw

        self.f1filter = F1Filter(self.mdi, create_help, self)
        QApplication.instance().installEventFilter(self.f1filter)
        try:
            QApplication.instance().installEventFilter(self)
        except Exception:
            pass
        try:
            _ensure_escape_filter_installed()
        except Exception:
            pass
                
        # Designer (Form-Designer + Docks) wird erst bei 'Ansicht -> Designer' on-demand erstellt
        self.dark_mode = True

        # Beispiel-Menü "Fenster"
        # Menü: Eigenschaften -> Arbeitsplatz
        f1 = QFont("Verdana", 11); f1.setBold(True)
        f2 = QFont("Verdana", 10); f2.setBold(False)
        
        menubar = self.menuBar()

        # --- i18n: load translations from locales.zip next to this script ---
        try:
            self._locales_zip = Path(__file__).parent / 'data' / 'locales.zip'
            share.locales.I18N.set_zip(self._locales_zip)
            # Default: Deutsch (passt zum aktuellen UI-Stand)
            share.locales.I18N.load_mo("de")
        except Exception:
            self._locales_zip = None

        menubar.setFont(f1)
        menubar.font().setBold(True)

        # Build custom chrome (TitleBar + MenuBar) at the very top
        try:
            top = QWidget()
            top_lay = QVBoxLayout(top)
            top_lay.setContentsMargins(0, 0, 0, 0)
            top_lay.setSpacing(0)
            top_lay.addWidget(menubar)
            self.setMenuWidget(top)
        except Exception:
            self._main_titlebar = None

        # Keep "MDI child buttons" in sync with the active subwindow (maximize/restore)
        try:
            self.mdi.subWindowActivated.connect(self._on_mdi_subwindow_activated)
        except Exception:
            pass

        self.menu_file       = menubar.addMenu(share.locales.tr("File"))
        self.menu_file.setFont(f2)

        self.menu_edit       = menubar.addMenu(share.locales.tr("Edit"))
        self.menu_edit.setFont(f2)

        self.menu_display    = menubar.addMenu(share.locales.tr("View"))
        self.menu_display.setFont(f2)

        self.menu_properties = QMenu(share.locales.tr("Properties"), self)
        self.menu_windows    = menubar.addMenu(share.locales.tr("Window"))
        self.menu_help       = menubar.addMenu(share.locales.tr("Help"))
        self.menu_help.setFont(f2)

        self.action_help_contents = QAction(share.locales.tr("Contents"), self)
        self.action_help_contents.setShortcut(QKeySequence("F1"))
        self.action_help_contents.triggered.connect(self.on_action_help_contents)
        self.menu_help.addAction(self.action_help_contents)

        self.action_help_whatis = QAction(share.locales.tr("What is ... ?"), self)
        self.action_help_whatis.setCheckable(True)
        self.action_help_whatis.toggled.connect(self.on_action_help_whatis)
        self.menu_help.addAction(self.action_help_whatis)

        self.menu_help.addSeparator()
        self.action_help_about = QAction(share.locales.tr("About ..."), self)
        self.action_help_about.triggered.connect(self.on_action_help_about)
        self.menu_help.addAction(self.action_help_about)

        self.action_workplace = QAction(share.locales.tr("Eigenschaften"), self)
        self.action_workplace.triggered.connect(self.open_workplace_properties)
        self.menu_display.addAction(self.action_workplace)
        self.menu_display.addSeparator()

        self.act_view_debug_window = QAction(share.locales.tr("Debug Window"), self)
        self.act_view_regie        = QAction(share.locales.tr("Control Center"), self)
        self.act_view_designer     = QAction(share.locales.tr("Designer"), self)
        self.act_view_editor       = QAction(share.locales.tr("Editor"), self)
        self.act_view_table        = QAction(share.locales.tr("Table Designer"), self)
        self.act_view_sql          = QAction(share.locales.tr("SQL Builder"), self)
        self.act_edit_minimap      = QAction(share.locales.tr("Mini-Map"), self, checkable=True, checked=True)
        self.act_edit_minimap.toggled.connect(self.on_action_edit_minimap)
        self.act_view_debug_window.triggered.connect(self.on_action_view_debug_window)
        self.act_view_regie.triggered.connect(self.on_action_view_regiecenter)
        self.act_view_designer.triggered.connect(self.on_action_view_designer)
        self.act_view_editor.triggered.connect(self.on_action_view_editor)
        self.act_view_table.triggered.connect(self.on_action_view_table_designer)
        self.act_view_sql.triggered.connect(self.on_action_view_sql_builder)
        self.menu_display.addAction(self.act_view_debug_window)
        self.menu_display.addSeparator()
        self.menu_display.addAction(self.act_view_regie)
        self.menu_display.addAction(self.act_view_designer)
        self.menu_display.addAction(self.act_view_editor)
        self.menu_display.addSeparator()
        self.menu_display.addAction(self.act_view_table)
        self.menu_display.addSeparator()
        self.menu_display.addAction(self.act_view_sql)
        self.menu_display.addSeparator()
        self.menu_display.addAction(self.act_edit_minimap)

        self.menu_language = self.menu_display.addMenu(share.locales.tr("Language"))
        try:
            from PyQt5.QtWidgets import QActionGroup
        except Exception:
            QActionGroup = None
        self.act_lang_en = QAction("English", self)
        self.act_lang_de = QAction("Deutsch", self)
        self.act_lang_en.setCheckable(True)
        self.act_lang_de.setCheckable(True)
        if QActionGroup is not None:
            grp = QActionGroup(self)
            grp.setExclusive(True)
            grp.addAction(self.act_lang_en)
            grp.addAction(self.act_lang_de)
        if (share.locales.I18N.lang or '').lower().startswith('de'):
            self.act_lang_de.setChecked(True)
        else:
            self.act_lang_en.setChecked(True)
        self._set_language('de')
        self.act_lang_en.triggered.connect(lambda: self._set_language('en'))
        self.act_lang_de.triggered.connect(lambda: self._set_language('de'))
        self.menu_language.addAction(self.act_lang_en)
        self.menu_language.addAction(self.act_lang_de)

        self.act_edit_undo = QAction('Undo', self, shortcut=QKeySequence('Ctrl+Z'))
        self.act_edit_redo = QAction('Redo', self, shortcut=QKeySequence('Ctrl+Y'))
        self.act_edit_paste = QAction('Paste', self, shortcut=QKeySequence('Ctrl+V'))
        self.act_edit_copy = QAction('Copy', self, shortcut=QKeySequence('Ctrl+C'))
        self.act_edit_cut = QAction('Cut', self, shortcut=QKeySequence('Ctrl+X'))
        self.act_edit_replace = QAction('Replace', self, shortcut=QKeySequence('Ctrl+H'))
        self.act_edit_search = QAction('Search', self, shortcut=QKeySequence('Ctrl+F'))
        self.act_edit_undo.triggered.connect(self.on_action_edit_undo)
        self.act_edit_redo.triggered.connect(self.on_action_edit_redo)
        self.act_edit_paste.triggered.connect(self.on_action_edit_paste)
        self.act_edit_copy.triggered.connect(self.on_action_edit_copy)
        self.act_edit_cut.triggered.connect(self.on_action_edit_cut)
        self.act_edit_replace.triggered.connect(self.on_action_edit_replace)
        self.act_edit_search.triggered.connect(self.on_action_edit_search)
        self.menu_edit.addAction(self.act_edit_undo)
        self.menu_edit.addAction(self.act_edit_redo)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.act_edit_paste)
        self.menu_edit.addAction(self.act_edit_copy)
        self.menu_edit.addAction(self.act_edit_cut)
        self.menu_edit.addSeparator()
        self.menu_edit.addAction(self.act_edit_replace)
        self.menu_edit.addAction(self.act_edit_search)

        menu_file_new = self.menu_file.addMenu(share.locales.tr("New"))
        menu_file_new.setFont(f2)
        self.action_file_open = QAction(share.locales.tr("Open"), self)
        self.action_file_close = QAction(share.locales.tr("Close"), self)
        self.action_file_open.setShortcut(QKeySequence("Ctrl+O"))
        self.action_file_close.setShortcut(QKeySequence("Ctrl+F4"))
        self.action_file_open.triggered.connect(self.on_action_file_open)
        self.action_file_close.triggered.connect(self.on_action_file_close)
        action_file_new_project = QAction(share.locales.tr("New Project"), self)
        action_file_open_project = QAction(share.locales.tr("Open Project"), self)
        action_file_print = QAction(share.locales.tr("Print"), self)
        action_file_print.setShortcut(QKeySequence("Ctrl+P"))
        action_file_new_project.triggered.connect(self.on_action_file_new_project)
        action_file_open_project.triggered.connect(self.on_action_file_open_project)
        action_file_print_preview = QAction(share.locales.tr("Print Preview"), self)
        action_file_window_app = QAction(share.locales.tr("One-Click Application"), self)
        action_file_web_wizard = QAction(share.locales.tr("Web Wizard"), self)
        action_file_database = QAction(share.locales.tr("Database Manager"), self)
        action_file_exit = QAction(share.locales.tr("Exit"), self)
        action_file_print.triggered.connect(self.on_action_file_print)
        action_file_print_preview.triggered.connect(self.on_action_file_print_preview)
        action_file_window_app.triggered.connect(self.on_action_file_window_app)
        action_file_web_wizard.triggered.connect(self.on_action_file_web_wizard)
        action_file_database.triggered.connect(self.on_action_file_database)
        action_file_exit.triggered.connect(self.on_action_file_exit)
        action_file_new_form = QAction(share.locales.tr("Forms"), self)
        action_file_new_menu = QAction(share.locales.tr("Menue"), self)
        action_file_new_popupmenu = QAction(share.locales.tr("Popup-Menu"), self)
        action_file_new_report = QAction(share.locales.tr("Reports"), self)
        action_file_new_labels = QAction(share.locales.tr("Labels"), self)
        action_file_new_program = QAction(share.locales.tr("Programs"), self)
        action_file_new_table = QAction(share.locales.tr("Tables"), self)
        action_file_new_sql = QAction(share.locales.tr("Queries"), self)
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
        self.menu_file.addAction(self.action_file_open)
        self.menu_file.addAction(self.action_file_close)
        self.menu_file.addSeparator()
        self.menu_file.addAction(action_file_new_project)
        self.menu_file.addAction(action_file_open_project)
        self.menu_file.addSeparator()
        self.menu_file.addAction(action_file_print)
        self.menu_file.addAction(action_file_print_preview)
        self.menu_file.addSeparator()
        self.menu_file.addAction(action_file_window_app)
        self.menu_file.addAction(action_file_web_wizard)
        self.menu_file.addSeparator()
        self.menu_file.addAction(action_file_database)
        self.menu_file.addAction(action_file_exit)

        self.action_window_cascade = QAction('Cascade', self, triggered=self.mdi.cascadeSubWindows)
        self.action_window_tile = QAction('Tiled', self, triggered=self.mdi.tileSubWindows)
        self.action_window_close_all = QAction('Alle schließen', self, triggered=self.close_all_mdi_subwindows)
        try:
            self.menu_windows.aboutToShow.connect(self.rebuild_windows_menu)
            self.mdi.subWindowActivated.connect(lambda _=None: self.rebuild_windows_menu())
        except Exception:
            pass

        self._dlg_workplace = None  # Dialog-Instanz merken (nicht jedes Mal neu)

        
        self._create_toolbar()
        self._create_statusbar()
        
        self.dark_mode = True
        self.apply_theme()

        try:
            self._init_form_designer_dock()
        except Exception:
            pass
        
        dlg = RegieCenter()
        self.regie_center = dlg
        sub = self.mdi.addSubWindow(dlg)
        mark_escape_close(sub)
        sub.resize(520,300)
        sub.move(30,30)
        sub.setWindowTitle(share.locales.tr("Regiecenter"))
        dlg.show()
        sub.show()

        # RegieCenter: zuletzt verwendetes Arbeitsverzeichnis (INI)
        try:
            last_dir = (self._settings.value("regiecenter/workdir", "", type=str) or "").strip()
            if last_dir:
                if dlg.combo.findText(last_dir, Qt.MatchExactly) < 0:
                    dlg.combo.addItem(last_dir)
                dlg.combo.setCurrentText(last_dir)  # triggert refresh
        except Exception:
            pass
        # CommandWindow (Debug Console) beim Start immer anzeigen
        try:
            self.ensure_debug_console(focus=False)
        except Exception:
            pass


    # Debug Console als weiteres Sub-MDI (Split: Output/Input)
    # -------- INI / State --------
    # ---------------------------------------------------------------------------
    # INI file path (portable: next to script/exe).
    # ---------------------------------------------------------------------------
    def _ini_path(self) -> str:
        try:
            base = os.path.dirname(os.path.abspath(sys.argv[0]))
        except Exception:
            base = os.getcwd()
        return os.path.join(base, "dBaseRunner.ini")

    # ---------------------------------------------------------------------------
    # Creates (or focuses) the debug console MDI subwindow.
    # ---------------------------------------------------------------------------
    def ensure_debug_console(self, focus: bool = True):
        try:
            existing = getattr(self, "_debug_console", None)
            if existing is not None:
                for sub in self.mdi.subWindowList():
                    if sub.widget() is existing:
                        existing.show()
                        existing.raise_()
                        if focus:
                            self.mdi.setActiveSubWindow(sub)
                        return existing
        except Exception:
            pass

        w = DebugConsoleWidget(self)
        self._debug_console = w
        sub = self.mdi.addSubWindow(w)
        mark_escape_protected(sub)
        sub.setWindowTitle(share.locales.tr("Debug Window"))
        sub.resize(780, 420)
        sub.move(580, 30)
        w.show()
        sub.show()
        if focus:
            self.mdi.setActiveSubWindow(sub)

        # restore splitter + history
        try:
            sizes = self._settings.value("console/split_sizes", None)
            if isinstance(sizes, (list, tuple)) and len(sizes) == 2:
                w.splitter.setSizes([int(sizes[0]), int(sizes[1])])
        except Exception:
            pass
        try:
            hist = self._settings.value("console/history", [], type=list)
            w.inp.set_history(hist)
        except Exception:
            pass
        return w

    def on_action_view_debug_window(self):
        try:
            self.ensure_debug_console(focus=True)
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Error"), f"{share.locales.tr('Debug Window')}\n\n{e}")

    def append_debug_output(self, text: str, fg_hex: str | None = None, bg_hex: str | None = None):
        text = "" if text is None else str(text)
        try:
            console = self.ensure_debug_console(focus=False)
            if console is not None:
                console.append_output(text, fg_hex=fg_hex, bg_hex=bg_hex)
                return
        except Exception:
            pass
        try:
            debug_print(text)
        except Exception:
            pass

    def clear_debug_output(self):
        try:
            console = self.ensure_debug_console(focus=False)
            if console is not None:
                console.clear_output()
                return
        except Exception:
            pass

    # ---------------------------------------------------------------------------
    # Führt eine einzelne dBase-One-Liner-Eingabe aus und gibt die Ausgabe
    # (stdout) zurück.
    #
    #  - Statements wie: WRITE "test"
    #  - Expressions wie: 2 + 3 * 4  -> werden automatisch zu: WRITE (2 + 3 * 4)
    #  - '?' wird als Kurzform für WRITE behandelt: ? "hi"
    # ---------------------------------------------------------------------------
    def _execute_one_liner(self, code_line: str) -> str:
        code_line = (code_line or "").strip()
        if not code_line:
            return ""

        # '?' als Kurzform
        if code_line.startswith("?"):
            code_line = "WRITE " + code_line[1:].lstrip()

        # Wenn es wie eine Expression aussieht (oder kein bekanntes Statement ist),
        # automatisch in WRITE einbetten, damit der Benutzer ein Ergebnis sieht.
        first_tok = (code_line.split(None, 1)[0] if code_line.split() else "").upper()

        stmt_keywords = {
            "WRITE", "USE", "SELECT", "SET", "IF", "ELSE", "ENDIF",
            "FOR", "ENDFOR", "BREAK", "RETURN", "WITH", "ENDWITH",
            "PARAMETER", "LOCAL", "CREATE", "OPEN", "CLOSE", "CLEAR",
            "DO", "CALL", "INPUT", "QUIT", "ERASE",
            "FORMAT", "PRINT", "SCREEN", "ON", "OFF", "MARGIN", "ESCAPE"
        }

        looks_like_expr = (
            first_tok not in stmt_keywords
            and (
                code_line[:1] in "\"'("  # String / Klammer
                or any(op in code_line for op in ("+", "-", "*", "/", "(", ")", "%"))
                or re.match(r"^[0-9\s\.\+\-\*/\(\)%]+$", code_line) is not None
            )
        )

        if looks_like_expr:
            code_line = f"WRITE ({code_line})"

        tmp_path = os.path.join(tempfile.gettempdir(), "dbase_one_liner.prg")
        with open(tmp_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(code_line + "\n")

        try:
            with capture_runtime_output(forward=False) as captured:
                parse(tmp_path, show_collect_dialog=False)
            return "\n".join(captured)
        except Exception as e:
            dlg = share.excepts.ErrorMessage(
                title    = share.locales.tr("Parser Error"),
                log_path = share.common.LOG,
                message  = f"{e}",
                parent   = MAINAPP
            )
            dlg.exec_()

    def on_action_edit_minimap(self, visible: bool):
        debug_print(visible)
        MINIMAP.minimap.setVisible(visible)
        
    def closeEvent(self, event):
        # Ask user
        reply = QMessageBox.question(
            self,
            share.locales.tr("Close Application"),
            share.locales.tr("Would you realy close the Application?"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            event.ignore()
            return

        # ---- persist INI ----
        try:
            # RegieCenter workdir
            rc = getattr(self, "regie_center", None)
            if rc is not None and hasattr(rc, "combo"):
                wd = (rc.combo.currentText() or "").strip()
                self._settings.setValue("regiecenter/workdir", wd)
        except Exception:
            pass

        # Debug Console state
        try:
            c = getattr(self, "_debug_console", None)
            if c is not None:
                self._settings.setValue("console/split_sizes", c.splitter.sizes())
                self._settings.setValue("console/history", c.inp.history())
        except Exception:
            pass

        # Designer dock layout (only if created)
        try:
            if hasattr(self, "obj_inspector_dock") and hasattr(self, "obj_palette_dock"):
                self._settings.setValue("designer/main_state", self.saveState())
                self._settings.setValue("designer/main_geom", self.saveGeometry())
        except Exception:
            pass

        try:
            self._settings.sync()
        except Exception:
            pass

        event.accept()

    # ---------------------------------------------------------------------------
    # Stellt sicher, dass ein FileEditorWindow existiert (im MDI) und setzt Fokus.
    #
    #   Hintergrund: im Projekt existieren mehrere Editor-Typen (EditorWidget vs.
    #   FileEditorWindow). Für "Ansicht -> Editor" und "Bearbeiten"
    #   wollen wir IMMER den FileEditorWindow (Tabs).
    # ---------------------------------------------------------------------------
    def ensure_code_editor_window(self, focus: bool = True):
        # 1) aktives SubWindow
        try:
            sub = self.mdi.activeSubWindow() if hasattr(self, "mdi") else None
            w = sub.widget() if sub else None
            if isinstance(w, FileEditorWindow):
                if focus and hasattr(self, "mdi"):
                    self.mdi.setActiveSubWindow(sub)
                    try:
                        w.setFocus()
                    except Exception:
                        pass
                return w
        except Exception:
            pass

        # 2) irgendein vorhandenes FileEditorWindow wiederverwenden
        try:
            if hasattr(self, "mdi"):
                for sub in self.mdi.subWindowList():
                    w = sub.widget()
                    if isinstance(w, FileEditorWindow):
                        if focus:
                            self.mdi.setActiveSubWindow(sub)
                            try:
                                w.setFocus()
                            except Exception:
                                pass
                        w.raise_()
                        try:
                            w.activateWindow()
                        except Exception:
                            pass
                        return w
        except Exception:
            pass

        # 3) Fallback: vorhandenen Helper benutzen, falls vorhanden
        try:
            if hasattr(self, "_get_or_create_file_editor_window"):
                w = self._get_or_create_file_editor_window()
                if focus and hasattr(self, "mdi"):
                    try:
                        # _get_or_create_file_editor_window liefert Widget; aktives Subwindow setzen
                        for sub in self.mdi.subWindowList():
                            if sub.widget() is w:
                                self.mdi.setActiveSubWindow(sub)
                                break
                    except Exception:
                        pass
                    try:
                        w.setFocus()
                    except Exception:
                        pass
                return w
        except Exception:
            pass

        # 4) Notnagel: neu erzeugen
        try:
            w = FileEditorWindow(parent=self, initial_path="", initial_text="")
            if hasattr(self, "mdi"):
                sub = self.mdi.addSubWindow(w)
                try:
                    sub.setWindowTitle("Editor")
                except Exception:
                    pass
                if focus:
                    self.mdi.setActiveSubWindow(sub)
            w.show()
            w.raise_()
            try:
                w.activateWindow()
            except Exception:
                pass
            return w
        except Exception:
            return None
        return None
    
    # ---------------------------------------------------------------------------
    # Best-effort: springt im aktiven Editor zu 'symbol' (oder legt Marker an).
    # ---------------------------------------------------------------------------
    def jump_to_symbol(self, symbol: str):
        symbol = (symbol or "").strip()
        if not symbol:
            return
        w = self.ensure_code_editor_window(focus=True)
        if w is None:
            return
        
        ed = None
        for attr in ("current_editor", "editor", "code_editor", "text_edit"):
            if hasattr(w, attr):
                try:
                    ed = getattr(w, attr)()
                except TypeError:
                    ed = getattr(w, attr)
                if ed is not None:
                    break
        if ed is None:
            return
        
        try:
            txt = ed.document().toPlainText()
            idx = txt.lower().find(symbol.lower())
            cur = ed.textCursor()
            if idx >= 0:
                cur.setPosition(idx)
                cur.movePosition(cur.EndOfLine, cur.KeepAnchor)
                ed.setTextCursor(cur)
                ed.setFocus()
                return

            cur.movePosition(cur.End)
            cur.insertText(f"\n\n* --- designer jump: {symbol} ---\n")
            ed.setTextCursor(cur)
            ed.setFocus()
        except Exception:
            pass

    def ensure_regie_center(self, focus: bool = True):
        # vorhandenes RegieCenter suchen
        try:
            for sub in self.mdi.subWindowList():
                w = sub.widget()
                if w and w.__class__.__name__ == "RegieCenter":
                    self.regie_center = w
                    if focus:
                        self.mdi.setActiveSubWindow(sub)
                        w.show()
                        w.raise_()
                    return w
        except Exception:
            pass

        try:
            dlg = RegieCenter()
            self.regie_center = dlg
            sub = self.mdi.addSubWindow(dlg)
            mark_escape_close(sub)
            sub.resize(520, 300)
            sub.move(30, 30)
            sub.setWindowTitle(share.locales.tr("Regiecenter"))
            dlg.show()
            if focus:
                self.mdi.setActiveSubWindow(sub)
            return dlg
        except Exception:
            return None

    

    def ensure_designer(self, focus: bool = True):
        try:
            need_init = (
                not hasattr(self, 'obj_inspector_dock') or self.obj_inspector_dock is None or
                not hasattr(self, 'obj_palette_dock') or self.obj_palette_dock is None or
                not hasattr(self, '_designer_panel_splitter') or self._designer_panel_splitter is None
            )

            if need_init:
                host = getattr(self, "_central_host", None)
                layout = getattr(self, "_central_host_layout", None)
                if host is None or layout is None:
                    raise RuntimeError("Designer-Host/Layout nicht verfügbar")

                panel_splitter = QSplitter(Qt.Vertical, host)
                panel_splitter.setObjectName("designer_panel_splitter")
                panel_splitter.setChildrenCollapsible(False)
                panel_splitter.setMinimumWidth(280)

                self.obj_inspector_dock = ObjectInspectorDock(self, panel_splitter)
                self.obj_palette_dock = ObjectPaletteDock(self, panel_splitter)

                try:
                    apply_custom_dock_titlebar(self.obj_inspector_dock)
                except Exception:
                    pass
                try:
                    apply_custom_dock_titlebar(self.obj_palette_dock)
                except Exception:
                    pass

                panel_splitter.addWidget(self.obj_inspector_dock)
                panel_splitter.addWidget(self.obj_palette_dock)
                try:
                    panel_splitter.setSizes([260, 220])
                except Exception:
                    pass

                panel_splitter.hide()
                self.obj_inspector_dock.hide()
                self.obj_palette_dock.hide()

                try:
                    layout.insertWidget(1, panel_splitter, 0)
                except Exception:
                    layout.addWidget(panel_splitter, 0)

                self._designer_panel_splitter = panel_splitter
                self._designer_host_splitter = None

            if hasattr(self, 'sidebar_widget') and self.sidebar_widget is not None:
                self.sidebar_widget.show()

            if hasattr(self, '_designer_panel_splitter') and self._designer_panel_splitter is not None:
                self._designer_panel_splitter.setMinimumWidth(280)
                self._designer_panel_splitter.show()
                try:
                    self._designer_panel_splitter.setSizes([260, 220])
                except Exception:
                    pass

            if hasattr(self, 'obj_inspector_dock') and self.obj_inspector_dock is not None:
                self.obj_inspector_dock.show()
            if hasattr(self, 'obj_palette_dock') and self.obj_palette_dock is not None:
                self.obj_palette_dock.show()
        except Exception as e:
            QMessageBox.warning(self, "Designer", f"Designer-Docks konnten nicht erstellt werden:\n{e}")

        try:
            fw = getattr(self, "form_designer_window", None)
            if fw is not None:
                for sub in self.mdi.subWindowList():
                    if sub.widget() is fw:
                        fw.show()
                        fw.raise_()
                        if focus:
                            self.mdi.setActiveSubWindow(sub)
                        return fw

            fw = FormDesignerWindow(self)
            self.form_designer_window = fw
            try:
                self.designer_canvas = fw.canvas
            except Exception:
                pass

            sub = self.mdi.addSubWindow(fw)
            sub.resize(720, 560)
            sub.setWindowTitle(share.locales.tr("Form Designer"))
            fw.show()
            if focus:
                self.mdi.setActiveSubWindow(sub)
            return fw
        except Exception as e:
            QMessageBox.warning(self, "Designer", f"Formular-Designer konnte nicht geöffnet werden:\n{e}")
            return None

    def on_action_view_regiecenter(self):
        self.ensure_regie_center(focus=True)

    def on_action_view_designer(self):
        self.ensure_designer(focus=True)

    def on_action_view_editor(self):
        self.ensure_code_editor_window(focus=True)

    def on_action_view_table_designer(self):
        self.mdi_open_table_designer()


    def _active_text_editor_widget(self):
        try:
            sub = self.mdi.activeSubWindow()
            w = sub.widget() if sub else None
        except Exception:
            w = None

        candidates = []
        if w is not None:
            candidates.append(w)
            for attr in ("current_editor", "editor", "code_editor", "text_edit", "text"):
                if hasattr(w, attr):
                    try:
                        obj = getattr(w, attr)()
                    except TypeError:
                        obj = getattr(w, attr)
                    except Exception:
                        obj = None
                    if obj is not None:
                        candidates.append(obj)

        fw = QApplication.focusWidget()
        if fw is not None:
            candidates.append(fw)

        for cand in candidates:
            try:
                if isinstance(cand, (QPlainTextEdit, QTextEdit, QLineEdit)):
                    return cand
            except Exception:
                pass
        return None

    def _editor_action(self, name: str):
        ed = self._active_text_editor_widget()
        if ed is None:
            return
        fn = getattr(ed, name, None)
        if callable(fn):
            try:
                fn()
            except Exception:
                pass

    def on_action_edit_undo(self): self._editor_action("undo")
    def on_action_edit_redo(self): self._editor_action("redo")
    def on_action_edit_copy(self): self._editor_action("copy")
    def on_action_edit_cut(self): self._editor_action("cut")
    def on_action_edit_paste(self): self._editor_action("paste")

    def _open_mdi_tool_widget(self, widget: QWidget, title: str, size: QSize = QSize(460, 220)):
        sub = self.mdi.addSubWindow(widget)
        mark_escape_close(sub)
        sub.setWindowTitle(title)
        sub.resize(size)
        widget.show()
        sub.show()
        self.mdi.setActiveSubWindow(sub)
        return sub, widget

    def on_action_edit_search(self):
        widget = SearchDialogWidget(self)
        self._open_mdi_tool_widget(widget, "Search", QSize(520, 240))

    def on_action_edit_replace(self):
        widget = ReplaceDialogWidget(self)
        self._open_mdi_tool_widget(widget, "Replace", QSize(520, 200))

    def find_in_active_editor(self, pattern: str, use_regex: bool = False, restart: bool = False, backward: bool = False) -> bool:
        ed = self._active_text_editor_widget()
        if ed is None:
            return False

        try:
            full_text = ed.toPlainText() if hasattr(ed, "toPlainText") else ed.text()
        except Exception:
            return False

        cursor = ed.textCursor() if hasattr(ed, "textCursor") else None
        if cursor is None:
            return False

        if restart:
            start_pos = len(full_text) if backward else 0
        else:
            start_pos = cursor.selectionStart() if backward else cursor.selectionEnd()

        match_start = -1
        match_end = -1

        try:
            if use_regex:
                rx = re.compile(pattern, re.MULTILINE)
                if backward:
                    matches = list(rx.finditer(full_text[:start_pos]))
                    if matches:
                        m = matches[-1]
                        match_start, match_end = m.start(), m.end()
                else:
                    m = rx.search(full_text, max(0, start_pos))
                    if m:
                        match_start, match_end = m.start(), m.end()
            else:
                if backward:
                    match_start = full_text.rfind(pattern, 0, max(0, start_pos))
                else:
                    match_start = full_text.find(pattern, max(0, start_pos))
                if match_start >= 0:
                    match_end = match_start + len(pattern)
        except re.error:
            return False

        if match_start < 0 or match_end < 0:
            return False

        try:
            tc = ed.textCursor()
            tc.setPosition(match_start)
            tc.setPosition(match_end, QTextCursor.KeepAnchor)
            ed.setTextCursor(tc)
            if hasattr(ed, "centerCursor"):
                ed.centerCursor()
            ed.setFocus()
        except Exception:
            return False
        return True

    def replace_in_active_editor(self, pattern: str, replacement: str, use_regex: bool = False) -> bool:
        ed = self._active_text_editor_widget()
        if ed is None:
            return False

        try:
            tc = ed.textCursor()
            selected = tc.selectedText()
        except Exception:
            return False

        if not pattern:
            return False

        replaced = False
        try:
            if use_regex:
                if selected:
                    new_text, count = re.subn(pattern, replacement, selected, count=1)
                    if count:
                        tc.insertText(new_text)
                        replaced = True
                if not replaced:
                    if self.find_in_active_editor(pattern, use_regex=True, restart=False, backward=False):
                        return self.replace_in_active_editor(pattern, replacement, use_regex=True)
            else:
                if selected == pattern:
                    tc.insertText(replacement)
                    replaced = True
                if not replaced:
                    if self.find_in_active_editor(pattern, use_regex=False, restart=False, backward=False):
                        return self.replace_in_active_editor(pattern, replacement, use_regex=False)
        except re.error:
            return False
        return replaced

    def rebuild_windows_menu(self):
        self.menu_windows.clear()
        windows = []
        try:
            windows = self.mdi.subWindowList()
        except Exception:
            windows = []

        active = None
        try:
            active = self.mdi.activeSubWindow()
        except Exception:
            active = None

        for idx, sub in enumerate(windows, 1):
            title = sub.windowTitle() or f"Window {idx}"
            act = QAction(title, self, checkable=True)
            act.setChecked(sub is active)
            act.triggered.connect(lambda checked=False, s=sub: self._activate_mdi_subwindow(s))
            self.menu_windows.addAction(act)

        if windows:
            self.menu_windows.addSeparator()

        self.menu_windows.addAction(self.action_window_cascade)
        self.menu_windows.addAction(self.action_window_tile)
        self.menu_windows.addSeparator()
        self.menu_windows.addAction(self.action_window_close_all)

    def _activate_mdi_subwindow(self, sub):
        try:
            if sub is not None:
                self.mdi.setActiveSubWindow(sub)
                sub.showNormal()
                sub.raise_()
        except Exception:
            pass

    def close_all_mdi_subwindows(self):
        try:
            self.mdi.closeAllSubWindows()
        except Exception:
            pass

    def open_project_directory(self, directory: str):
        directory = (directory or "").strip()
        if not directory or not os.path.isdir(directory):
            return
        try:
            self.record_project_directory(directory)
        except Exception:
            pass
        rc = self.ensure_regie_center(focus=True)
        if rc is None:
            return
        try:
            rc._add_and_select_dir(directory)
        except Exception:
            try:
                if rc.combo.findText(directory, Qt.MatchExactly) < 0:
                    rc.combo.addItem(directory)
                rc.combo.setCurrentText(directory)
            except Exception:
                pass



    def record_project_directory(self, directory: str):
        directory = (directory or '').strip()
        if not directory or not os.path.isdir(directory):
            return
        try:
            items = self._settings.value('projects/recent_dirs', [], type=list) or []
        except Exception:
            items = []
        items = [d for d in items if d and os.path.isdir(d) and os.path.normpath(d) != os.path.normpath(directory)]
        items.insert(0, os.path.normpath(directory))
        items = items[:5]
        try:
            self._settings.setValue('projects/recent_dirs', items)
        except Exception:
            pass

    def recent_project_directories(self, limit: int = 5):
        try:
            items = self._settings.value('projects/recent_dirs', [], type=list) or []
        except Exception:
            items = []
        out = []
        for d in items:
            d = (d or '').strip()
            if d and os.path.isdir(d) and d not in out:
                out.append(d)
            if len(out) >= max(1, int(limit or 5)):
                break
        return out

    def on_action_view_sql_builder(self):
        self.mdi_open_sql_builder()

    def on_action_file_open_project(self):
        self.open_project_directory(QFileDialog.getExistingDirectory(self, "Projektordner öffnen", os.getcwd()))
        
    def on_action_file_print(self):
        pass
    def on_action_file_print_preview(self):
        pass
    def on_action_file_window_app(self):
        pass
    def on_action_file_web_wizard(self):
        pass
    def ensure_localize_tool(self, focus: bool = True, po_path: str = ""):
        po_path = os.path.normpath((po_path or '').strip()) if po_path else ''
        try:
            existing = getattr(self, '_localize_tool_window', None)
            if existing is not None:
                for sub in self.mdi.subWindowList():
                    if sub.widget() is existing:
                        if po_path:
                            try:
                                if hasattr(existing, 'ed_po_path'):
                                    existing.ed_po_path.setText(po_path)
                            except Exception:
                                pass
                            try:
                                if hasattr(existing, '_open_po'):
                                    existing._open_po(po_path)
                            except Exception:
                                pass
                        existing.show()
                        existing.raise_()
                        if focus:
                            self.mdi.setActiveSubWindow(sub)
                        return existing
        except Exception:
            pass
        try:
            widget = LocalizeToolWindow(self)
            self._localize_tool_window = widget
            sub = self.mdi.addSubWindow(widget)
            mark_escape_close(sub)
            sub.setWindowTitle('Localize')
            sub.resize(856, 580)
            if po_path:
                try:
                    if hasattr(widget, 'ed_po_path'):
                        widget.ed_po_path.setText(po_path)
                except Exception:
                    pass
                try:
                    if hasattr(widget, '_open_po'):
                        widget._open_po(po_path)
                except Exception:
                    pass
            widget.show()
            sub.show()
            if focus:
                self.mdi.setActiveSubWindow(sub)
            try:
                widget.destroyed.connect(lambda *_: setattr(self, '_localize_tool_window', None))
            except Exception:
                pass
            return widget
        except Exception as e:
            QMessageBox.warning(self, 'Localize', f'Localize konnte nicht geöffnet werden:\n{e}')
            return None

    def open_workplace_properties(self):
        pass
    def _create_toolbar(self):
        pass
    def _create_statusbar(self):
        pass
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

    # ---------------------------------------------------------------------------
    # Datei -> Öffnen: Quellcode-Datei(en) im FileEditorWindow als Tab öffnen.
    # ---------------------------------------------------------------------------
    def on_action_file_open(self):
        try:
            dlg = QFileDialog(self, share.locales.tr("Open File..."))
            dlg.setFileMode(QFileDialog.ExistingFiles)
            dlg.setNameFilters([ share.locales.tr("dBaseSourcecodeFiles"), share.locales.tr("allFiles")])
            dlg.selectNameFilter(share.locales.tr("dBaseSourcecodeFiles"))
            try:
                dlg.setDefaultSuffix("prg")
            except Exception:
                pass

            if not dlg.exec_():
                return

            paths = dlg.selectedFiles() or []
            if not paths:
                return

            # Ziel-Editor-Fenster bestimmen: aktives FileEditorWindow oder erstes vorhandenes
            target_win = None
            sub = self.mdi.activeSubWindow() if hasattr(self, "mdi") else None
            if sub:
                w = sub.widget()
                if isinstance(w, FileEditorWindow):
                    target_win = w

            if target_win is None and hasattr(self, "mdi"):
                for sw in self.mdi.subWindowList():
                    w = sw.widget()
                    if isinstance(w, FileEditorWindow):
                        target_win = w
                        break

            # Wenn keins da: neu erstellen
            if target_win is None:
                first = paths[0]
                text = ""
                try:
                    with open(first, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                except Exception:
                    text = ""
                target_win = FileEditorWindow(parent=self, initial_path=first, initial_text=text)
                target_win.resize(900, 650)
                if hasattr(self, "mdi"):
                    sw = self.mdi.addSubWindow(target_win)
                    try:
                        sw.setWindowTitle(os.path.basename(first))
                    except Exception:
                        pass
                target_win.show()

                # restliche Dateien als Tabs
                for fp in paths[1:]:
                    try:
                        target_win.open_path_in_tab(os.path.normpath(fp))
                    except Exception:
                        pass
            else:
                # alle gewählten Dateien als Tabs öffnen
                for fp in paths:
                    try:
                        target_win.open_path_in_tab(os.path.normpath(fp))
                    except Exception:
                        pass

            target_win.raise_()
            try:
                target_win.activateWindow()
            except Exception:
                pass
        except Exception as e:
            QMessageBox.warning(self,
                share.locales.tr("Open File..."),
                f"{share.locales.tr('could not open file')}:\n{e}"
            )

    def on_action_file_database(self):
        debug_print("file data base")
    
    def on_action_file_exit(self):
        debug_print("file exit")
        try:
            os.remove(share.common.LOG)
            p = Path(share.common.LOG)
            if p.exists():
                p.unlink()
        except FileNotFoundError:
            dlg = share.excepts.ErrorMessage(
                title    = share.locales.tr("Runtime Error"),
                log_path = share.common.LOG,
                message  = f"{share.locales.tr('file not found')}: '{share.common.LOG}'.",
                parent   = MAINAPP
            )
            dlg.exec_()
        except PermissionError:
            txt = share.locales.tr("file is in use")
            dlg = share.excepts.ErrorMessage(
                title    = share.locales.tr("Runtime Error"),
                log_path = share.common.LOG,
                message  = (f"{txt}: '{share.common.LOG}'.\n" +
                share.locales.tr("you have to remove it your self")),
                parent   = MAINAPP
            )
            dlg.exec_()
        self.close()
        
    def on_action_file_new_project(self):
        debug_print("file new project")
        try:
            dlg = ProjectDialog(self)
            sub = self.mdi.addSubWindow(dlg)
            mark_escape_close(sub)
            sub.setWindowTitle(share.locales.tr("Project"))
            sub.setMinimumSize(800, 500)
            sub.setMaximumSize(800, 500)
            sub.resize(800, 500)
            dlg.show()
            sub.show()
            try:
                self.mdi.setActiveSubWindow(sub)
            except Exception:
                pass
        except Exception as e:
            QMessageBox.warning(self, share.locales.tr("Project"), f"{share.locales.tr('Projekt-Fenster konnte nicht geöffnet werden.')}\n{e}")

    def open_project_file(self, project_path: str):
        project_path = (project_path or "").strip()
        if not project_path:
            return
        if not os.path.isfile(project_path):
            QMessageBox.warning(self, share.locales.tr("Project"), f"{share.locales.tr('Datei nicht gefunden')}:\n{project_path}")
            return
        try:
            dlg = ProjectDialog(self)
            try:
                dlg._load_project_from_file(project_path)
            except Exception as e:
                QMessageBox.warning(self, share.locales.tr("Project"), f"{share.locales.tr('Projektdatei konnte nicht geladen werden.')}\n{e}")
                try:
                    dlg.deleteLater()
                except Exception:
                    pass
                return

            sub = self.mdi.addSubWindow(dlg)
            mark_escape_close(sub)
            base = os.path.basename(project_path)
            sub.setWindowTitle(f"{share.locales.tr('Project')}: {base}")
            sub.setMinimumSize(800, 500)
            sub.setMaximumSize(800, 500)
            sub.resize(800, 500)
            dlg.show()
            sub.show()
            try:
                self.mdi.setActiveSubWindow(sub)
            except Exception:
                pass
        except Exception as e:
            QMessageBox.warning(self, share.locales.tr("Project"), f"{share.locales.tr('Projekt-Fenster konnte nicht geöffnet werden.')}\n{e}")

    def _init_form_designer_dock(self):
        # Die feste Sidebar ist bereits Teil des zentralen Layouts.
        # Hier kein zusätzliches Dock-Fenster mehr erzeugen.
        try:
            self.form_designer_dock = getattr(self, 'sidebar_widget', None)
        except Exception:
            self.form_designer_dock = None

    def _active_file_editor_window(self):
        try:
            sub = self.mdi.activeSubWindow()
            w = sub.widget() if sub else None
            if isinstance(w, FileEditorWindow):
                return w
        except Exception:
            pass
        return None

    def _get_or_create_file_editor_window(self) -> "FileEditorWindow":
        win = self._active_file_editor_window()
        if win is not None:
            return win

        # wenn es einen FileEditorWindow irgendwo im MDI gibt: wiederverwenden
        try:
            for sub in self.mdi.subWindowList():
                w = sub.widget()
                if isinstance(w, FileEditorWindow):
                    sub.setFocus()
                    w.raise_()
                    return w
        except Exception:
            pass

        # sonst: neuen leeren Editor erzeugen
        win = FileEditorWindow(parent=self, initial_path="", initial_text="")
        sub = self.mdi.addSubWindow(win)
        sub.setWindowTitle("Editor")
        win.show()
        return win

    # ---------------------------------------------------------------------------
    # Erzeugt (falls nicht vorhanden) einen Eventhandler als Code.
    # ---------------------------------------------------------------------------
    def insert_event_handler(self, handler_name: str):
        handler_name = (handler_name or "").strip()
        if not handler_name:
            return

        win = self._get_or_create_file_editor_window()
        ed = win.current_editor()
        txt = ed.toPlainText()

        needle = f"PROCEDURE {handler_name}".lower()
        if needle in txt.lower():
            return

        stub = f"\n\nPROCEDURE {handler_name}\n    * TODO: Handler Code\nRETURN\n"
        ed.appendPlainText(stub)


    def insert_override_method(self, method_name: str):
        """Erzeugt einen überschreibbaren Methoden-Stub."""
        method_name = (method_name or "").strip()
        if not method_name:
            return

        win = self._get_or_create_file_editor_window()
        ed = win.current_editor()
        txt = ed.toPlainText()

        needle = f"PROCEDURE {method_name}".lower()
        if needle in txt.lower():
            return

        stub = f"\n\nPROCEDURE {method_name}\n    * TODO: Override\nRETURN\n"
        ed.appendPlainText(stub)

    def on_action_file_open(self):
        # Datei -> Öffnen: in CodeEditor-Tabs öffnen
        dlg = QFileDialog(self, share.locales.tr("Open File..."))
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
            mark_escape_close(subw)
            new_win.resize(700, 500)
            new_win.show()
            new_win.open_path_in_tab(path)
            self.mdi.setActiveSubWindow(subw)
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Editor nicht öffnen:\n{e}")

    # ---------------------------------------------------------------------------
    # Projekt/Ordner öffnen und im RegieCenter (Programme) als aktuelles
    # Verzeichnis setzen.
    # ---------------------------------------------------------------------------
    def on_action_file_open_project(self):
        directory = QFileDialog.getExistingDirectory(self, "Projektordner öffnen", os.getcwd())
        if not directory:
            return
        self.open_project_directory(directory)
    def on_action_file_print(self):
        debug_print("file print")
    def on_action_file_print_preview(self):
        debug_print("file print preview")
    def on_action_file_web_wizard(self):
        debug_print("file web wizard")
    def on_action_file_window_app(self):
        debug_print("file window app")
        
    def on_new(self):
        self.status_left.setText(share.locales.tr("Neu angelegt"))

    def on_open(self):
        self.status_left.setText(share.locales.tr("Öffnen..."))

    def on_save(self):
        self.status_left.setText(share.locales.tr("Gespeichert"))
        
    def _create_toolbar(self):
        toolbar = QToolBar("Haupt-Toolbar", self)
        toolbar.setIconSize(QSize(40, 40))
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        act_new  = QAction(QIcon(":/icons/new.png" ), share.locales.tr("Neu")      , self)
        act_open = QAction(QIcon(":/icons/open.png"), share.locales.tr("Öffnen")   , self)
        act_save = QAction(QIcon(":/icons/save.png"), share.locales.tr("Speichern"), self)

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
        self.status_left = QLabel("Ready")
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
    
    # ---------------------------------------------------------------------------
    # Update main titlebar when active MDI subwindow changes/maximizes.
    # ---------------------------------------------------------------------------
    def _on_mdi_subwindow_activated(self, sub: 'QMdiSubWindow') -> None:
        tb = getattr(self, "_main_titlebar", None)
        if tb is None:
            return
        try:
            active = self.mdi.activeSubWindow()
        except Exception:
            active = None

        if active is None:
            tb.set_child_controls_visible(False)
            tb.set_child_restore_state(False)
            return

        try:
            maximized = active.isMaximized()
        except Exception:
            maximized = False

        tb.set_child_controls_visible(maximized)
        tb.set_child_restore_state(maximized)

        # Keep main window title informative when a child is maximized
        try:
            if maximized:
                self.setWindowTitle(f"{active.windowTitle()} - dBase Runner")
            else:
                self.setWindowTitle("dBase Runner")
        except Exception:
            pass

        try:
            self.status_mid.setText(f"MDI: {len(self.mdi.subWindowList())} Fenster")
        except Exception:
            pass

        
    def mdi_open_editor(self, title="Unbenannt", text=""):
        w = EditorWidget(text)
        sub = self.mdi.addSubWindow(w)     # Qt erzeugt ein QMdiSubWindow
        mark_escape_close(sub)
        sub.setWindowTitle(title)
        sub.resize(900, 650)
        w.show()
        sub.show()
        
        self.mdi.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi.setVerticalScrollBarPolicy  (Qt.ScrollBarAsNeeded)
        
        self.mdi.setActiveSubWindow(sub)
        return sub

    def mdi_open_table_designer(self):
        dlg = TableDesignerDialog(self)
        sub = self.mdi.addSubWindow(dlg)
        mark_escape_close(sub)
        dlg.setSubWindow(sub)
        sub.resize(600,250)
        sub.move(56,320)
        sub.show()


    def mdi_open_sql_builder(self, project_path: str = ""):
        dlg = SqlBuilderWindow(self)
        if project_path:
            try:
                dlg._load_builder_project(project_path)
            except Exception as e:
                QMessageBox.warning(self, "SQL Builder", f"Konnte Projekt nicht laden:\n{e}")
        sub = self.mdi.addSubWindow(dlg)
        mark_escape_close(sub)
        sub.resize(900, 520)
        sub.move(40, 60)
        try:
            if project_path:
                sub.setWindowTitle(os.path.basename(project_path))
        except Exception:
            pass
        sub.show()
    
    def open_workplace_properties(self):
        if self._dlg_workplace is None:
            self._dlg_workplace = DesktopPropertiesDialog(self)
            sub = MAINAPP.mdi.addSubWindow(self._dlg_workplace)
            sub.resize(650, 500)
            # Wenn Benutzer das Fenster schließt, Instanz wieder freigeben
            self._dlg_workplace.mdi = sub
            self._dlg_workplace.finished.connect(lambda _=0: setattr(self, "_dlg_workplace", None))

        self._dlg_workplace.show()
        self._dlg_workplace.raise_()
        self._dlg_workplace.activateWindow()
        
    def apply_theme(self):
        share.utildef.theme.apply_theme_global(self)
        self.mdi.setBackground(QBrush(QColor("#373737")))

# ---------------------------------------------------------------------------
# Fixup: globale Helper als MainWindow-Methoden (falls sie durch Einrückung global gelandet sind)
# ---------------------------------------------------------------------------
try:
    if not hasattr(MainWindow, "insert_event_handler") and "insert_event_handler" in globals():
        MainWindow.insert_event_handler = globals()["insert_event_handler"]
    if not hasattr(MainWindow, "insert_override_method") and "insert_override_method" in globals():
        MainWindow.insert_override_method = globals()["insert_override_method"]
    if not hasattr(MainWindow, "_active_file_editor_window") and "_active_file_editor_window" in globals():
        MainWindow._active_file_editor_window = globals()["_active_file_editor_window"]
    if not hasattr(MainWindow, "_get_or_create_file_editor_window") and "_get_or_create_file_editor_window" in globals():
        MainWindow._get_or_create_file_editor_window = globals()["_get_or_create_file_editor_window"]
except Exception:
    pass

# ---------------------------------------------------------------------------
# SQL Builder (Canvas + Table)
# ---------------------------------------------------------------------------
# Read field names from a DBF header (dBASE III/IV style).
# Best-effort: returns [] on errors.
# ---------------------------------------------------------------------------
def _read_dbf_fields(dbf_path: str) -> List[str]:
    try:
        with open(dbf_path, "rb") as f:
            hdr = f.read(32)
            if len(hdr) < 32:
                return []
            header_len = int.from_bytes(hdr[8:10], "little", signed=False)
            f.seek(32)
            fields = []
            # field descriptors until 0x0D
            while True:
                b = f.read(1)
                if not b:
                    break
                if b == b"\x0d":
                    break
                rest = f.read(31)
                if len(rest) < 31:
                    break
                desc = b + rest
                name_raw = desc[0:11]
                name = name_raw.split(b"\x00", 1)[0].decode("ascii", errors="ignore").strip()
                if name:
                    fields.append(name)
            return fields
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Return (table_name, [fields]) for a SQLite database file.
# If multiple tables exist, asks user to pick later (handled by caller).
# ---------------------------------------------------------------------------
def _read_sqlite_fields(db_path: str) -> (str, List[str]):
    # This helper only returns all tables; caller selects.
    con = sqlite3.connect(db_path)
    try:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        tables = [r[0] for r in cur.fetchall()]
        return ("", tables)
    finally:
        con.close()


class SqlConnection:
    __slots__ = ("src_proxy", "src_field", "dst_proxy", "dst_field")

    def __init__(self, src_proxy, src_field: str, dst_proxy, dst_field: str):
        self.src_proxy = src_proxy
        self.src_field = src_field
        self.dst_proxy = dst_proxy
        self.dst_field = dst_field

# ---------------------------------------------------------------------------
# A draggable proxy widget representing a table (DBF or SQLite table).
# ---------------------------------------------------------------------------
class SqlTableProxy(QFrame):
    request_delete = pyqtSignal(object)             # self
    request_connection = pyqtSignal(object, str, object, str)  # src_proxy, src_field, dst_proxy, dst_field

    def __init__(self, canvas, table_name: str, fields: List[str], source_path: str = "", source_kind: str = "dbf"):
        super().__init__(canvas)
        self.canvas = canvas
        self.table_name = table_name
        self.source_path = source_path
        self.source_kind = source_kind  # 'dbf' | 'sqlite'
        self._dragging = False
        self._drag_off = QPoint(0, 0)

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("""
            SqlTableProxy { background: #2a2a2a; border: 1px solid rgba(0,0,0,140); }
            QLabel { color: #ffd800; }
            QCheckBox { color: #eaeaea; }
            QListWidget { background: #1f1f1f; color: #eaeaea; border: 1px solid rgba(0,0,0,120); }
        """)
        self.setFixedSize(230, 240)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(6)

        hdr = QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)

        self.lbl_title = QLabel(table_name)
        self.lbl_title.setStyleSheet("font-weight: bold; color: #ffd800;")
        hdr.addWidget(self.lbl_title, 1)

        self.btn_close = QToolButton()
        self.btn_close.setText("×")
        self.btn_close.setAutoRaise(True)
        self.btn_close.setToolTip("Tabelle entfernen")
        self.btn_close.clicked.connect(lambda: self.request_delete.emit(self))
        hdr.addWidget(self.btn_close, 0)

        lay.addLayout(hdr)

        self.chk_all = QCheckBox(share.locales.tr("Alle wählen"))
        self.chk_all.stateChanged.connect(self._on_all_changed)
        lay.addWidget(self.chk_all)

        self.listw = QListWidget()
        self.listw.setSelectionMode(QListWidget.SingleSelection)
        self.listw.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listw.customContextMenuRequested.connect(self._on_list_context_menu)
        lay.addWidget(self.listw, 1)

        for fn in fields:
            # Ensure list shows ONLY the field name (no table prefix, no type hints)
            fn_clean = str(fn).strip()
            if not fn_clean:
                continue
            # drop possible "table.field"
            if "." in fn_clean:
                fn_clean = fn_clean.split(".")[-1].strip()
            # drop possible "FIELD (type)" or "FIELD type"
            if "(" in fn_clean:
                fn_clean = fn_clean.split("(", 1)[0].strip()
            if " " in fn_clean:
                fn_clean = fn_clean.split(" ", 1)[0].strip()

            it = QListWidgetItem(fn_clean)
            it.setFlags(it.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            it.setCheckState(Qt.Unchecked)
            self.listw.addItem(it)

        # Drag to connect
        self.listw.viewport().installEventFilter(self)

    def _on_all_changed(self, _state: int):
        checked = self.chk_all.isChecked()
        for i in range(self.listw.count()):
            it = self.listw.item(i)
            it.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def checked_fields(self) -> List[str]:
        res = []
        for i in range(self.listw.count()):
            it = self.listw.item(i)
            if it.checkState() == Qt.Checked:
                res.append(it.text())
        return res

    def _on_list_context_menu(self, pos):
        m = QMenu(self)
        act_all = m.addAction(share.locales.tr("Alle wählen") if not self.chk_all.isChecked() else share.locales.tr("Alle abwählen"))
        act_all.triggered.connect(lambda: self.chk_all.setChecked(not self.chk_all.isChecked()))
        m.addSeparator()
        act_del = m.addAction(share.locales.tr("Tabelle löschen"))
        act_del.triggered.connect(lambda: self.request_delete.emit(self))
        m.exec_(self.listw.mapToGlobal(pos))

    def contextMenuEvent(self, ev):
        m = QMenu(self)
        act_del = m.addAction(share.locales.tr("Tabelle löschen"))
        act_del.triggered.connect(lambda: self.request_delete.emit(self))
        m.exec_(ev.globalPos())

    # --- drag proxy itself (move) ---
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_off = ev.pos()
            ev.accept()
            return
        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev):
        if self._dragging and (ev.buttons() & Qt.LeftButton):
            new_pos = self.mapToParent(ev.pos() - self._drag_off)
            self.move(new_pos)
            self.canvas.update()
            self.canvas.proxy_moved_or_resized()
            ev.accept()
            return
        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._dragging = False
            self.canvas.update()
            self.canvas.proxy_moved_or_resized()
        super().mouseReleaseEvent(ev)

    # --- drag connections from list item to list item ---
    def eventFilter(self, obj, ev):
        if obj is self.listw.viewport():
            if ev.type() == QEvent.MouseButtonPress and ev.button() == Qt.LeftButton:
                it = self.listw.itemAt(ev.pos())
                if it is not None:
                    self.canvas._drag_src_proxy = self
                    self.canvas._drag_src_field = it.text()
                    self.canvas._dragging_link = True
                    self.canvas._drag_pos = self.listw.viewport().mapToGlobal(ev.pos())
                return False
            if ev.type() == QEvent.MouseMove and self.canvas._dragging_link and (ev.buttons() & Qt.LeftButton):
                self.canvas._drag_pos = self.listw.viewport().mapToGlobal(ev.pos())
                self.canvas.update()
                return False
            if ev.type() == QEvent.MouseButtonRelease and self.canvas._dragging_link and ev.button() == Qt.LeftButton:
                # drop target
                gpos = self.listw.viewport().mapToGlobal(ev.pos())
                w = QApplication.widgetAt(gpos)
                target_proxy = None
                target_field = None
                if w is not None:
                    # walk up to find a SqlTableProxy
                    p = w
                    while p is not None and not isinstance(p, SqlTableProxy):
                        p = p.parentWidget()
                    if isinstance(p, SqlTableProxy):
                        target_proxy = p
                        # if released on list viewport, determine field
                        vp = None
                        try:
                            vp = target_proxy.listw.viewport()
                        except Exception:
                            vp = None
                        if vp is not None and (w is vp or vp.isAncestorOf(w)):
                            local = vp.mapFromGlobal(gpos)
                            it = target_proxy.listw.itemAt(local)
                            if it is not None:
                                target_field = it.text()

                if target_proxy is not None and target_field is not None and target_proxy is not self:
                    self.request_connection.emit(self, self.canvas._drag_src_field, target_proxy, target_field)

                self.canvas._dragging_link = False
                self.canvas._drag_src_proxy = None
                self.canvas._drag_src_field = None
                self.canvas.update()
                return False
        return super().eventFilter(obj, ev)

# ---------------------------------------------------------------------------
# A scrollable canvas that hosts SqlTableProxy widgets and draws connections.
# ---------------------------------------------------------------------------
class SqlCanvas(QFrame):
    selection_changed = pyqtSignal(object)  # reserved (future)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setMinimumSize(1400, 900)
        self.setStyleSheet("SqlCanvas { background: #1b1b1b; }")
        self.proxies: List[SqlTableProxy] = []
        self.connections: List[SqlConnection] = []

        # drag-link state
        self._dragging_link = False
        self._drag_src_proxy = None
        self._drag_src_field = None
        self._drag_pos = None

        self.setContextMenuPolicy(Qt.DefaultContextMenu)

    def proxy_moved_or_resized(self):
        # expand canvas if needed (simple: ensure all proxies fit)
        try:
            max_r = 0
            max_b = 0
            for p in self.proxies:
                g = p.geometry()
                max_r = max(max_r, g.right() + 80)
                max_b = max(max_b, g.bottom() + 80)
            self.setMinimumSize(max(1200, max_r), max(800, max_b))
        except Exception:
            pass

    def add_table_proxy(self, table_name: str, fields: List[str], source_path: str = "", source_kind: str = "dbf", pos: QPoint = None):
        pr = SqlTableProxy(self, table_name, fields, source_path=source_path, source_kind=source_kind)
        pr.request_delete.connect(self.remove_proxy)
        pr.request_connection.connect(self.add_connection)
        self.proxies.append(pr)
        if pos is None:
            pos = QPoint(40 + 40*len(self.proxies), 40 + 30*len(self.proxies))
        pr.move(pos)
        pr.show()
        self.proxy_moved_or_resized()
        self.update()
        return pr

    def remove_proxy(self, proxy: SqlTableProxy):
        # remove connections
        self.connections = [c for c in self.connections if c.src_proxy is not proxy and c.dst_proxy is not proxy]
        try:
            self.proxies.remove(proxy)
        except Exception:
            pass
        proxy.setParent(None)
        proxy.deleteLater()
        self.proxy_moved_or_resized()
        self.update()

    def add_connection(self, src_proxy, src_field: str, dst_proxy, dst_field: str):
        # avoid duplicates
        for c in self.connections:
            if c.src_proxy is src_proxy and c.dst_proxy is dst_proxy and c.src_field == src_field and c.dst_field == dst_field:
                return
            if c.src_proxy is dst_proxy and c.dst_proxy is src_proxy and c.src_field == dst_field and c.dst_field == src_field:
                return
        self.connections.append(SqlConnection(src_proxy, src_field, dst_proxy, dst_field))
        self.update()

    def _connection_segments(self, c: SqlConnection):
        # compute polyline segments in canvas coordinates
        sp = c.src_proxy
        dp = c.dst_proxy
        sg = sp.geometry()
        dg = dp.geometry()
        sy = sg.top() + 58 + self._field_index_y(sp, c.src_field)
        dy = dg.top() + 58 + self._field_index_y(dp, c.dst_field)

        # decide which side (left/right) based on relative x
        if sg.center().x() <= dg.center().x():
            sx_edge = sg.right()
            dx_edge = dg.left()
            dir_out = +1
        else:
            sx_edge = sg.left()
            dx_edge = dg.right()
            dir_out = -1

        sx = sx_edge
        dx = dx_edge

        s0 = QPoint(sx, sy)
        s1 = QPoint(sx + dir_out*12, sy)
        e1 = QPoint(dx - dir_out*12, dy)
        e0 = QPoint(dx, dy)

        midx = int((s1.x() + e1.x())/2)
        p2 = QPoint(midx, s1.y())
        p3 = QPoint(midx, e1.y())

        pts = [s0, s1, p2, p3, e1, e0]
        return pts

    def _field_index_y(self, proxy: SqlTableProxy, field: str) -> int:
        # return y offset inside list widget item, best-effort
        try:
            for i in range(proxy.listw.count()):
                it = proxy.listw.item(i)
                if it.text() == field:
                    r = proxy.listw.visualItemRect(it)
                    return r.center().y()
        except Exception:
            pass
        return 10

    def _hit_test_connection(self, pos: QPoint, tol: int = 6):
        # simple distance to polyline segments
        def dist_point_to_seg(p, a, b):
            ax, ay = a.x(), a.y()
            bx, by = b.x(), b.y()
            px, py = p.x(), p.y()
            vx, vy = bx-ax, by-ay
            wx, wy = px-ax, py-ay
            vv = vx*vx + vy*vy
            if vv == 0:
                return ((px-ax)**2 + (py-ay)**2) ** 0.5
            t = (wx*vx + wy*vy)/vv
            t = 0 if t < 0 else 1 if t > 1 else t
            cx, cy = ax + t*vx, ay + t*vy
            return ((px-cx)**2 + (py-cy)**2) ** 0.5

        for c in self.connections:
            pts = self._connection_segments(c)
            for a, b in zip(pts, pts[1:]):
                if dist_point_to_seg(pos, a, b) <= tol:
                    return c
        return None

    # ---------------------------------------------------------------------------
    # Walk up the parent chain to find the SqlBuilderWindow (or wrapper) that
    # owns this canvas.
    # ---------------------------------------------------------------------------
    def _find_builder_host(self):
        w = self
        # parentWidget() is more reliable than window() here because the canvas lives inside a QScrollArea viewport
        while w is not None:
            if hasattr(w, "add_table_dialog") and hasattr(w, "preview_sql"):
                return w
            try:
                w = w.parentWidget()
            except Exception:
                break
        # fallback: try window(), then its parents (covers QMdiSubWindow cases)
        try:
            w = self._find_builder_host()
        except Exception:
            w = None
        while w is not None:
            if hasattr(w, "add_table_dialog") and hasattr(w, "preview_sql"):
                return w
            try:
                w = w.parentWidget()
            except Exception:
                break
        return None

    def contextMenuEvent(self, ev):
        # if right-click on a connection -> connection menu
        c = self._hit_test_connection(ev.pos())
        if c is not None:
            m = QMenu(self)
            act_help = m.addAction(share.locales.tr("Hilfe"))
            act_help.setShortcut(QKeySequence("F1"))
            act_preview = m.addAction(share.locales.tr("Vorschau"))
            m.addSeparator()
            act_save    = m.addAction(share.locales.tr("Speichern"))
            act_save_as = m.addAction(share.locales.tr("Speichern unter..."))
            m.addSeparator()
            act_del     = m.addAction(share.locales.tr("Löschen"))

            chosen = m.exec_(ev.globalPos())
            if chosen is act_del:
                try:
                    self.connections.remove(c)
                except Exception:
                    pass
                self.update()
            elif chosen is act_help:
                self._show_help()
            elif chosen is act_preview:
                # bubble to window if possible
                w = self._find_builder_host()
                if hasattr(w, "preview_sql"):
                    w.preview_sql()
            return

        # canvas menu
        m = QMenu(self)
        act_new  = m.addAction(share.locales.tr("Neu"))
        act_load = m.addAction(share.locales.tr("Laden"))
        m.addSeparator()
        act_add  = m.addAction(share.locales.tr("Hinzufügen"))
        m.addSeparator()
        act_save = m.addAction(share.locales.tr("Speichern"))
        act_save_as = m.addAction(share.locales.tr("Speichern unter..."))
        m.addSeparator()
        act_help = m.addAction(share.locales.tr("Hilfe"))
        act_help.setShortcut(QKeySequence("F1"))
        act_preview = m.addAction(share.locales.tr("Vorschau"))

        chosen = m.exec_(ev.globalPos())
        w = self._find_builder_host()
        if chosen is act_add and hasattr(w, "add_table_dialog"):
            w.add_table_dialog(ev.globalPos())
        elif chosen is act_new and hasattr(w, "new_builder"):
            w.new_builder()
        elif chosen is act_load and hasattr(w, "load_builder"):
            w.load_builder()
        elif chosen is act_save and hasattr(w, "save_builder"):
            w.save_builder()
        elif chosen is act_save_as and hasattr(w, "save_builder_as"):
            w.save_builder_as()
        elif chosen is act_help:
            self._show_help()
        elif chosen is act_preview and hasattr(w, "preview_sql"):
            w.preview_sql()

    def _show_help(self):
        QMessageBox.information(self, "SQL Builder – Hilfe",
            """Drag & Drop:\n"
            "- Feld in einer Liste anklicken, linke Maustaste halten und auf ein Feld in einer anderen Tabelle ziehen.\n"
            "- Es wird eine Verbindung (Join) gezeichnet.\n\n"
            "Auswahl:\n"
            "- 'Alle wählen' selektiert/entfernt alle Felder.\n"
            "- Sonst werden nur angehakte Felder im SELECT verwendet.\n\n"
            "Kontextmenü:\n"
            "- Rechtsklick auf Canvas: Neu/Laden/Speichern/Hinzufügen/Vorschau.\n"
            "- Rechtsklick auf Linie: Löschen.\n""")

    def paintEvent(self, ev):
        super().paintEvent(ev)

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        # draw connections
        pen = QPen(QColor(255, 216, 0, 210))
        pen.setWidth(2)
        p.setPen(pen)

        for c in self.connections:
            pts = self._connection_segments(c)
            for a, b in zip(pts, pts[1:]):
                p.drawLine(a, b)

        # draw currently dragging preview line
        if self._dragging_link and self._drag_src_proxy is not None and self._drag_pos is not None:
            sp = self._drag_src_proxy
            sg = sp.geometry()
            sy = sg.top() + 70
            if self._drag_src_field:
                sy = sg.top() + 58 + self._field_index_y(sp, self._drag_src_field)

            gpos = self._drag_pos
            end = self.mapFromGlobal(gpos)
            if sg.center().x() <= end.x():
                sx = sg.right()
                dir_out = +1
            else:
                sx = sg.left()
                dir_out = -1
            s0 = QPoint(sx, sy)
            s1 = QPoint(sx + dir_out*12, sy)
            e1 = QPoint(end.x() - dir_out*12, end.y())
            e0 = QPoint(end.x(), end.y())
            midx = int((s1.x()+e1.x())/2)
            pts = [s0, s1, QPoint(midx, s1.y()), QPoint(midx, e1.y()), e1, e0]
            for a,b in zip(pts, pts[1:]):
                p.drawLine(a,b)

# ---------------------------------------------------------------------------
# SQL Builder window: scrollable canvas on top, QTableWidget below.
# ---------------------------------------------------------------------------
class SqlBuilderWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._project_path = None
        mark_escape_close(self)

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(6)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.canvas = SqlCanvas()
        self.scroll.setWidget(self.canvas)

        root.addWidget(self.scroll, 3)

        self.sql_editor = LocalizeCodeEditor(self)
        self.sql_editor.setObjectName("SqlBuilderPreviewEditor")
        self.sql_editor.setPlaceholderText("SELECT * FROM ...")
        self.sql_editor.setReadOnly(False)
        try:
            self.sql_editor.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        except Exception:
            pass
        root.addWidget(self.sql_editor, 2)

        # F1 help
        act_help = QAction(self)
        act_help.setShortcut(QKeySequence("F1"))
        act_help.triggered.connect(lambda: self.canvas._show_help())
        self.addAction(act_help)
        self.setFocusPolicy(Qt.StrongFocus)

    # ---- canvas menu actions ----
    def new_builder(self):
        # clear canvas
        for pxy in list(self.canvas.proxies):
            self.canvas.remove_proxy(pxy)
        self.canvas.connections.clear()
        self.canvas.update()
        self._project_path = None
        self._set_table_preview("")

    def add_table_dialog(self, _global_pos=None):
        # choose DBF or SQLite file
        fn, _ = QFileDialog.getOpenFileName(self, "Tabelle hinzufügen", "", "DBF Dateien (*.dbf);;SQLite DB (*.db *.sqlite *.sqlite3);;Alle Dateien (*.*)")
        if not fn:
            return
        path = fn
        lower = fn.lower()

        if lower.endswith(".dbf"):
            fields = _read_dbf_fields(path)
            table_name = Path(path).stem
            self.canvas.add_table_proxy(table_name, fields, source_path=path, source_kind="dbf")
            return

        # sqlite
        try:
            _dummy, tables = _read_sqlite_fields(path)
        except Exception as e:
            QMessageBox.warning(self, "SQLite", f"Konnte DB nicht öffnen:\n{e}")
            return
        if not tables:
            QMessageBox.information(self, "SQLite", "Keine Tabellen gefunden.")
            return
        if len(tables) == 1:
            table = tables[0]
        else:
            table, ok = QInputDialog.getItem(self, "Tabelle wählen", "SQLite Tabelle:", tables, 0, False)
            if not ok or not table:
                return
        # read fields
        try:
            con = sqlite3.connect(path)
            cur = con.cursor()
            cur.execute(f"PRAGMA table_info('{table}')")
            fields = [r[1] for r in cur.fetchall()]
        except Exception as e:
            QMessageBox.warning(self, "SQLite", f"Konnte Felder nicht lesen:\n{e}")
            return
        finally:
            try:
                con.close()
            except Exception:
                pass
        self.canvas.add_table_proxy(table, fields, source_path=path, source_kind="sqlite")

    def save_builder(self):
        if not self._project_path:
            return self.save_builder_as()
        self._save_to_path(self._project_path)

    def save_builder_as(self):
        fn, _ = QFileDialog.getSaveFileName(self, "SQL Builder speichern", "", "SQL Builder Projekt (*.sqlb.json);;Alle Dateien (*.*)")
        if not fn:
            return
        if not fn.lower().endswith(".json"):
            fn = fn + ".sqlb.json"
        self._project_path = fn
        self._save_to_path(fn)

    def load_builder(self):
        fn, _ = QFileDialog.getOpenFileName(self, "SQL Builder laden", "", "SQL Builder Projekt (*.sqlb.json *.json);;Alle Dateien (*.*)")
        if not fn:
            return
        self._load_builder_project(fn)

    def load_builder_from_path(self, fn: str):
        self._load_builder_project(fn)

    def _load_builder_project(self, fn: str):
        try:
            data = json.loads(Path(fn).read_text(encoding="utf-8"))
        except Exception as e:
            QMessageBox.warning(self, "Laden", f"Konnte Projekt nicht laden:\n{e}")
            return False

        self.new_builder()
        self._project_path = fn

        # proxies
        idmap = {}
        for rec in data.get("tables", []):
            name = rec.get("name", "")
            fields = rec.get("fields", [])
            spath = rec.get("source_path", "")
            skind = rec.get("source_kind", "dbf")
            pos = QPoint(int(rec.get("x", 40)), int(rec.get("y", 40)))
            pr = self.canvas.add_table_proxy(name, fields, source_path=spath, source_kind=skind, pos=pos)
            try:
                pr.chk_all.setChecked(bool(rec.get("all", False)))
            except Exception:
                pass
            checks = set(rec.get("checked", []))
            for i in range(pr.listw.count()):
                it = pr.listw.item(i)
                if it.text() in checks:
                    it.setCheckState(Qt.Checked)
            idmap[rec.get("id")] = pr

        # connections
        for c in data.get("connections", []):
            sp = idmap.get(c.get("src_id"))
            dp = idmap.get(c.get("dst_id"))
            if sp and dp:
                self.canvas.add_connection(sp, c.get("src_field", ""), dp, c.get("dst_field", ""))

        self.canvas.proxy_moved_or_resized()
        self.canvas.update()
        return True

    def _save_to_path(self, fn: str):
        try:
            tables = []
            # stable ids
            ids = {p: f"t{idx}" for idx, p in enumerate(self.canvas.proxies)}
            for pxy in self.canvas.proxies:
                g = pxy.geometry()
                tables.append({
                    "id": ids[pxy],
                    "name": pxy.table_name,
                    "source_path": pxy.source_path,
                    "source_kind": pxy.source_kind,
                    "x": g.x(),
                    "y": g.y(),
                    "fields": [pxy.listw.item(i).text() for i in range(pxy.listw.count())],
                    "all": bool(pxy.chk_all.isChecked()),
                    "checked": pxy.checked_fields(),
                })
            conns = []
            for c in self.canvas.connections:
                conns.append({
                    "src_id": ids.get(c.src_proxy),
                    "src_field": c.src_field,
                    "dst_id": ids.get(c.dst_proxy),
                    "dst_field": c.dst_field,
                })
            data = {"tables": tables, "connections": conns}
            Path(fn).write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception as e:
            QMessageBox.warning(self, "Speichern", f"Konnte Projekt nicht speichern:\n{e}")

    # ---- preview SQL ----
    def preview_sql(self):
        sql = self.build_sql()
        self._set_table_preview(sql)

    def _set_table_preview(self, sql: str):
        try:
            self.sql_editor.blockSignals(True)
            self.sql_editor.setPlainText(sql or "")
        finally:
            try:
                self.sql_editor.blockSignals(False)
            except Exception:
                pass

    def build_sql(self) -> str:
        if not self.canvas.proxies:
            return ""

        proxies = self.canvas.proxies
        conns = self.canvas.connections

        # field list
        selected = []
        any_checked = False
        for pxy in proxies:
            if pxy.chk_all.isChecked():
                fs = [pxy.listw.item(i).text() for i in range(pxy.listw.count())]
                any_checked = True
                for f in fs:
                    selected.append(f"{pxy.table_name}.{f}")
            else:
                fs = pxy.checked_fields()
                if fs:
                    any_checked = True
                    for f in fs:
                        selected.append(f"{pxy.table_name}.{f}")

        if not any_checked:
            select_part = "*"
        else:
            # if only one table, de-qualify for nicer output
            if len(proxies) == 1:
                select_part = ", ".join([s.split(".", 1)[1] for s in selected]) if selected else "*"
            else:
                select_part = ", ".join(selected) if selected else "*"

        base = proxies[0].table_name
        sql = f"SELECT {select_part} FROM {base}"

        # naive joins from connections
        used_tables = {base}
        pending = True
        # Build adjacency for easier chaining
        edges = []
        for c in conns:
            edges.append((c.src_proxy.table_name, c.src_field, c.dst_proxy.table_name, c.dst_field))
            edges.append((c.dst_proxy.table_name, c.dst_field, c.src_proxy.table_name, c.src_field))

        # keep joining until no progress
        while pending:
            pending = False
            for a, af, b, bf in edges:
                if a in used_tables and b not in used_tables:
                    sql += f" JOIN {b} ON {a}.{af} = {b}.{bf}"
                    used_tables.add(b)
                    pending = True

        return sql


def center_on_screen(widget):
    widget.adjustSize()
    screen = QApplication.primaryScreen()
    ag = screen.availableGeometry()  # ohne Taskbar
    fg = widget.frameGeometry()
    fg.moveCenter(ag.center())
    widget.move(fg.topLeft())

def main():
    # Remote DevTools (hilft zu sehen, ob der Renderer überhaupt hochkommt)
    #os.environ.setdefault("QTWEBENGINE_REMOTE_DEBUGGING", "9222")
    
    # Häufige Workarounds für Frozen/Windows-Umgebungen:
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-gpu --disable-gpu-compositing")
    # wenn es *immer noch* crasht, testweise:
    # os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] += " --no-sandbox"

    global APPINST
    APPINST = ensure_qt_app()
    if APPINST is not None:
        #register_chm_scheme()
        #chm_path = 
        
        #profile = QWebEngineProfile.defaultProfile()
        #handler = ChmOnDemandSchemeHandler(chm_path, profile)
        #profile.installUrlSchemeHandler(b"chm", handler)
        
        #f1filter = F1Filter()
        #app.installEventFilter(f1filter)
        #app.setStyle(FontTriangleArrowsStyle(app.style(), color="#d7b300", font_family="Segoe UI Symbol"))
        
        #APPINST.setStyle(ArrowFontProxyStyle(APPINST.style()))
        global MAINAPP
        try:
            MAINAPP = MainWindow()
            try:
                share.common.MAINAPP = MAINAPP
            except Exception:
                pass
            MAINAPP.show()
            center_on_screen(MAINAPP)
        except Exception:
            import traceback as _tb
            try:
                with open(share.common.LOG, "a", encoding="utf-8", buffering=1) as _f:
                    _f.write("[Startup Exception]")
                    _f.write(_tb.format_exc())
                    _f.write("")
            except Exception:
                pass
            try:
                QMessageBox.critical(
                    None,
                    share.locales.tr("Startfehler"),
                    share.locales.tr("Beim Start ist ein Fehler aufgetreten.") + "\n" +
                    share.locales.tr("Details stehen in: webengine_crash.log"))
            except Exception:
                pass
            return

        rc = APPINST.exec_()
        
        #handler.close()
        sys.exit(rc)
    else:
        if SystemInfo.is_windows():
            ctypes.windll.user32.MessageBoxW(0,
                share.locales.tr("Qt5 could not be started"),
                share.locales.tr("Qt5 Framework Error:"), 0
            )
            sys.exit(1)
        else:
            debug_print(share.locales.tr("Qt5 kann nicht gestartet werden."))
            sys.exit(1)

if __name__ == "__main__":
    main()
