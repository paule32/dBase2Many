# ---------------------------------------------------------------------------
# \file  : parser.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations

import share.common
from   share.common             import *

from   share.excepts            import *
from   share.locales            import *

from   share.utildef.sysinfo    import *
from   share.utildef.dialogs    import *
from   share.utildef.theme      import *

from   parse.dbase.preprocessor import *

# -----------------------------------------------------------------------
# dbase interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.dbase.dBaseLexer          import dBaseLexer
from parse.dbase.dBaseParser         import dBaseParser
from parse.dbase.dBaseParserVisitor  import dBaseParserVisitor


def _pdf_backend_available() -> bool:
    return bool(getattr(share.common, "_PDF_BACKEND_AVAILABLE", False))


def _pdf_backend_import_error():
    return getattr(share.common, "_PDF_BACKEND_IMPORT_ERROR", None)


def _pdf_pagesize_a4():
    return getattr(share.common, "A4", None)


def _pdf_canvas_module():
    return getattr(share.common, "canvas", None)


def _pdf_colors_module():
    return getattr(share.common, "rl_colors", None)


def _pdf_metrics_module():
    return getattr(share.common, "pdfmetrics", None)


def _resolve_runtime_mainapp():
    seen = set()

    def _iter_candidate(obj):
        cur = obj
        depth = 0
        while cur is not None and depth < 16:
            oid = id(cur)
            if oid in seen:
                break
            seen.add(oid)
            yield cur
            try:
                cur = cur.parent()
            except Exception:
                cur = None
            depth += 1

    base_candidates = []
    try:
        base_candidates.append(getattr(share.common, "MAINAPP", None))
    except Exception:
        pass
    try:
        base_candidates.append(globals().get("MAINAPP"))
    except Exception:
        pass

    try:
        app = QApplication.instance()
    except Exception:
        app = None

    if app is not None:
        try:
            base_candidates.append(app.activeWindow())
        except Exception:
            pass
        try:
            fw = app.focusWidget()
            if fw is not None:
                base_candidates.append(fw)
                try:
                    base_candidates.append(fw.window())
                except Exception:
                    pass
        except Exception:
            pass
        try:
            base_candidates.extend(list(app.topLevelWidgets()))
        except Exception:
            pass

    for base in base_candidates:
        for cand in _iter_candidate(base):
            if hasattr(cand, "append_debug_output"):
                return cand

    return None

# ---------------------------------------------------------------------------
# runtime output routing (WRITE/TEXT -> Debug Console or PDF printer)
# ---------------------------------------------------------------------------
_RUNTIME_CAPTURE_STACK: list[tuple[list[str], bool]] = []
_RUNTIME_OUTPUT_FORMAT = "SCREEN"
_RUNTIME_PRINT_ENABLED = False
_RUNTIME_PRINT_LINES: list[dict[str, Any]] = []
_RUNTIME_PRINT_PDF_PATH: Path | None = None
_RUNTIME_PRINT_STARTED_AT: datetime.datetime | None = None
_RUNTIME_PRINT_SCRIPT_PATH: Path | None = None
_RUNTIME_PRINT_MARGIN_DEFAULTS = {
    "left": 42.0,
    "top": 42.0,
    "right": 42.0,
    "bottom": 42.0,
}
_RUNTIME_PRINT_MARGINS = dict(_RUNTIME_PRINT_MARGIN_DEFAULTS)
_RUNTIME_ESCAPE_ENABLED = False
_RUNTIME_ESCAPE_FILTER = None
_RUNTIME_CONFIRM_ENABLED = False
_RUNTIME_DELETE_ENABLED = False

_VGA_COLOR_TABLE = {
     0: {"name": "Schwarz",     "hex": "#000000"},
     1: {"name": "Blau",        "hex": "#0000AA"},
     2: {"name": "Gruen",       "hex": "#00AA00"},
     3: {"name": "Cyan",        "hex": "#00AAAA"},
     4: {"name": "Rot",         "hex": "#AA0000"},
     5: {"name": "Magenta",     "hex": "#AA00AA"},
     6: {"name": "Braun",       "hex": "#AA5500"},
     7: {"name": "Hellgrau",    "hex": "#AAAAAA"},
     8: {"name": "Dunkelgrau",  "hex": "#555555"},
     9: {"name": "Hellblau",    "hex": "#5555FF"},
    10: {"name": "Hellgruen",   "hex": "#55FF55"},
    11: {"name": "Hellcyan",    "hex": "#55FFFF"},
    12: {"name": "Hellrot",     "hex": "#FF5555"},
    13: {"name": "Hellmagenta", "hex": "#FF55FF"},
    14: {"name": "Gelb",        "hex": "#FFFF55"},
    15: {"name": "Weiss",       "hex": "#FFFFFF"},
}

# ---------------------------------------------------------------------------
# native base classes supported by dBase 2026
# ---------------------------------------------------------------------------
NATIVE_BASES = {
    "FORM"          : QDialog,          # oder QDialog, wenn FORM per default Dialog sein soll
    "DIALOG"        : QDialog,
    "PUSHBUTTON"    : QPushButton,
    "CONTAINER"     : QFrame,
    "ENTRYFIELD"    : QLineEdit,
    "RADIOBUTTON"   : QRadioButton,
    "COMBOBOX"      : QComboBox,
    "EDITOR"        : QPlainTextEdit,
    "CHECKBOX"      : QCheckBox,
    "LISTBOX"       : QListWidget,
    "CHECKLISTBOX"  : QListWidget,
    "IMAGE"         : QLabel,
    "GRID"          : QTableWidget,
    "PROGRESS"      : QProgressBar,
    "PAINTBOX"      : QWidget,
    "VSCROLLBAR"    : QScrollBar,
    "HSCROLLBAR"    : QScrollBar,
    "TEXT"          : QLabel,
    "TREEVIEW"      : QTreeView,
    "SPINBOX"       : QSpinBox,
    "BROWSE"        : QTableView,
}

def _copy_runtime_color_style(style: dict[str, Any] | None) -> dict[str, Any]:
    return dict(style or {})

def _make_default_screen_style() -> dict[str, Any]:
    return {
        "attr": 7,
        "fg_index": 7,
        "bg_index": 0,
        "fg_hex" : _VGA_COLOR_TABLE[7]["hex" ],
        "bg_hex" : _VGA_COLOR_TABLE[0]["hex" ],
        "fg_name": _VGA_COLOR_TABLE[7]["name"],
        "bg_name": _VGA_COLOR_TABLE[0]["name"],
        "transparent_bg": False,
    }

def _make_default_print_style() -> dict[str, Any]:
    return {
        "attr"      : None,
        "fg_index"  : 0,
        "bg_index"  : None,
        "fg_hex"    : "#000000",
        "bg_hex"    : None,
        "fg_name"   : "Schwarz",
        "bg_name"   : "Transparent/Weiss",
        "transparent_bg": True,
    }

class _SilentAntlrErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.messages: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        try:
            self.messages.append(f"line {line}:{column} {msg}")
        except Exception:
            self.messages.append(str(msg))


def _attach_silent_antlr_errors(lexer=None, parser=None):
    listener = _SilentAntlrErrorListener()
    for obj in (lexer, parser):
        if obj is None:
            continue
        try:
            obj.removeErrorListeners()
        except Exception:
            pass
        try:
            obj.addErrorListener(listener)
        except Exception:
            pass
    return listener

def _coerce_runtime_color_attr(value: Any) -> int:
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        iv = int(value)
    else:
        s = ("" if value is None else str(value)).strip()
        if not s:
            raise RuntimeError("SET COLOR TO: Farbwert fehlt")
        m = re.fullmatch(r"[+-]?\d+(?:\.\d+)?", s)
        if not m:
            raise RuntimeError(f"SET COLOR TO: ungueltiger Farbwert: {s}")
        iv = int(float(s))
    if iv < 0 or iv > 255:
        raise RuntimeError(f"SET COLOR TO: Farbwert ausserhalb des Bereichs 0..255: {iv}")
    return iv

def _style_from_vga_attr(value: Any) -> dict[str, Any]:
    attr = _coerce_runtime_color_attr(value)
    fg_index = attr % 16
    bg_index = (attr // 16) % 16
    fg = _VGA_COLOR_TABLE[fg_index]
    bg = _VGA_COLOR_TABLE[bg_index]
    return {
        "attr": attr,
        "fg_index": fg_index,
        "bg_index": bg_index,
        "fg_hex": fg["hex"],
        "bg_hex": bg["hex"],
        "fg_name": fg["name"],
        "bg_name": bg["name"],
        "transparent_bg": False,
    }

_RUNTIME_SCREEN_COLOR_STYLE = _make_default_screen_style()
_RUNTIME_PRINT_COLOR_STYLE  = _make_default_print_style()


def _runtime_output_session_begin(script_filename: str | os.PathLike[str] | None):
    global _RUNTIME_OUTPUT_FORMAT, _RUNTIME_PRINT_ENABLED
    global _RUNTIME_PRINT_LINES, _RUNTIME_PRINT_PDF_PATH
    global _RUNTIME_PRINT_STARTED_AT, _RUNTIME_PRINT_SCRIPT_PATH
    global _RUNTIME_PRINT_MARGINS, _RUNTIME_ESCAPE_ENABLED, _RUNTIME_CONFIRM_ENABLED, _RUNTIME_DELETE_ENABLED
    global _RUNTIME_SCREEN_COLOR_STYLE, _RUNTIME_PRINT_COLOR_STYLE

    _RUNTIME_OUTPUT_FORMAT      = "SCREEN"
    _RUNTIME_PRINT_ENABLED      = False
    _RUNTIME_PRINT_LINES        = []
    _RUNTIME_PRINT_PDF_PATH     = None
    _RUNTIME_PRINT_STARTED_AT   = datetime.datetime.now()
    _RUNTIME_PRINT_MARGINS      = dict(_RUNTIME_PRINT_MARGIN_DEFAULTS)
    _RUNTIME_ESCAPE_ENABLED     = False
    _RUNTIME_CONFIRM_ENABLED    = False
    _RUNTIME_DELETE_ENABLED     = False
    _RUNTIME_SCREEN_COLOR_STYLE = _make_default_screen_style()
    _RUNTIME_PRINT_COLOR_STYLE  = _make_default_print_style()
    try:
        _RUNTIME_PRINT_SCRIPT_PATH = Path(script_filename).resolve() if script_filename else None
    except Exception:
        _RUNTIME_PRINT_SCRIPT_PATH = None

# ---------------------------------------------------------------------------
# Accepts '#RRGGBB', 'red', 'rgb(...)'. Returns None if empty.
# ---------------------------------------------------------------------------
def _qss_color(v: Any) -> Optional[str]:
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    return str(v)

def form_open(inst: share.common.Instance):
    if inst.backend is None:
        return

    backend = inst.backend

    try:
        _ensure_escape_filter_installed()
    except Exception:
        pass

    try:
        if hasattr(backend, "setModal"):
            backend.setModal(False)
    except Exception:
        pass

    try:
        if hasattr(backend, "setWindowModality"):
            backend.setWindowModality(Qt.NonModal)
    except Exception:
        pass

    # ---------------------------------------------------------------------------
    # QDialog/QWidget fuer MDI-Nutzung neutralisieren, damit das Fenster nicht
    # als eigenes Top-Level-Fenster ausserhalb des MDI-Bereichs auftaucht.
    # ---------------------------------------------------------------------------
    try:
        if isinstance(backend, QDialog):
            backend.setWindowFlags(Qt.Widget)
    except Exception:
        pass

    sub = None
    try:
        sub = share.common.MAINAPP.mdi.addSubWindow(backend)
    except Exception:
        sub = None

    if sub is not None:
        #sub.setStyleSheet()
        try:
            sub.setAttribute(Qt.WA_DeleteOnClose, True)
        except Exception:
            pass
        try:
            sub.resize(360, 400)
        except Exception:
            pass
        try:
            backend.setProperty("_DBASE_ESCAPE_TARGET", True)
        except Exception:
            pass
        try:
            sub.setProperty("_DBASE_ESCAPE_TARGET", True)
        except Exception:
            pass
        inst.props["_QT_SUBWINDOW"] = sub
        try:
            share.utildef.theme.apply_theme_global(backend)
            backend.show()
        except Exception:
            pass
        try:
            share.utildef.theme.apply_theme_global(sub)
            sub.show()
        except Exception:
            pass
        return sub

    try:
        backend.setProperty("_DBASE_ESCAPE_TARGET", True)
    except Exception:
        pass
    try:
        share.utildef.theme.apply_theme_global(backend)
        backend.show()
    except Exception:
        pass
    return backend

# ---------------------------------------------------------------------------
# Build QSS for CONTAINER (QFrame) from instance properties.
# ---------------------------------------------------------------------------
def build_container_qss(inst: "share.common.Instance") -> str:
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

def apply_property_to_qt(inst: share.common.Instance, prop: str, value: Any):
    if inst.backend is None:
        return
        
    p = prop.upper()
    s = str(value)
    
    # normalisiere Zahlen (dein Interpreter nutzt evtl. float)
    if isinstance(value, float) and value.is_integer():
        value = int(value)

    # CONTAINER (QFrame) Stylesheet-Properties
    if inst.class_name.upper() == "CONTAINER" and p in (
        "BACKCOLOR",
        "BORDERCOLOR",
        "BORDERWIDTH",
        "RADIUS",
        "STYLE"):
        qss = build_container_qss(inst)
        inst.backend.setStyleSheet(qss)
        return
    
    # ---------------------------------------------------------------------------
    # VALUE/STATE/ITEMS Mappings (Entryfield, Checkbox, Radiobutton, Combobox,
    # Editor, Listbox, Progress, Scrollbar, Spinbox, Image, Text)
    # ---------------------------------------------------------------------------
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
    
    # ---------------------------------------------------------------------------
    # Geometry: Qt braucht Left/Top/Width/Height gemeinsam
    # Besonderheit: Wenn das Widget in einem QMdiSubWindow steckt, müssen wir
    # sowohl das SubWindow (Position/Größe im MDI) als auch das eigentliche
    # Widget anpassen.
    # ---------------------------------------------------------------------------
    if p in ("LEFT", "TOP", "WIDTH", "HEIGHT"):
        # Ausgangswerte aus den gespeicherten Properties
        left   = int(inst.props.get("LEFT",    0)   or 0)
        top    = int(inst.props.get("TOP",     0)   or 0)
        width  = int(inst.props.get("WIDTH", 100)   or 100)
        height = int(inst.props.get("HEIGHT",100)   or 100)

        mdi = share.common.find_mdi_subwindow(inst.backend)

        if mdi is not None:
            # ---------------------------------------------------------------------------
            # Für MDI: wenn der User das SubWindow verschoben hat, sind LEFT/TOP in props
            # evtl. veraltet. Damit WIDTH/HEIGHT nicht auf alte Position zurückspringen,
            # nehmen wir die aktuelle Position aus dem QMdiSubWindow, wenn nur die Größe
            # geändert wird (und umgekehrt).
            # ---------------------------------------------------------------------------
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
        if isinstance(value, share.common.FontValue):
            f = QFont(value.family, int(value.size))
            f.setBold(bool(value.bold))
            f.setItalic(bool(value.italic))
            f.setUnderline(bool(value.underline))
            if hasattr(inst.backend, "setFont"):
                inst.backend.setFont(f)
            return

def set_prop_runtime(inst: share.common.Instance, name: str, value: Any):
    inst.set_prop(name, value)
    apply_property_to_qt(inst, name, value)

def _runtime_output_session_end():
    try:
        if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT" and _RUNTIME_PRINT_PDF_PATH is not None:
            _render_runtime_output_pdf()
    except Exception:
        pass


def _wrap_pdf_text_line(text: str, *,
    font_name: str,
    font_size: int,
    max_width: float) -> list[str]:
    text = ("" if text is None else str(text)).expandtabs(4)
    if text == "":
        return [""]

    parts = re.findall(r'\S+|\s+', text)
    lines: list[str] = []
    cur = ""

    def width_of(s: str) -> float:
        metrics = _pdf_metrics_module()
        if metrics is None:
            return max(0.0, float(len(s)) * float(font_size) * 0.6)
        return metrics.stringWidth(s, font_name, font_size)

    for part in parts:
        trial = cur + part
        if cur == "" or width_of(trial) <= max_width:
            cur = trial
            continue

        if cur:
            lines.append(cur.rstrip())
            cur = ""

        if width_of(part) <= max_width:
            cur = part.lstrip()
            continue

        chunk = ""
        for ch in part:
            trial_chunk = chunk + ch
            if chunk and width_of(trial_chunk) > max_width:
                lines.append(chunk.rstrip())
                chunk = ch.lstrip()
            else:
                chunk = trial_chunk
        cur = chunk

    if cur or not lines:
        lines.append(cur.rstrip())

    return lines


def _notify_pdf_backend_unavailable():
    global _PDF_BACKEND_WARNING_EMITTED, _RUNTIME_OUTPUT_FORMAT, _RUNTIME_PRINT_ENABLED

    _RUNTIME_OUTPUT_FORMAT = "SCREEN"
    _RUNTIME_PRINT_ENABLED = False

    if _PDF_BACKEND_WARNING_EMITTED:
        return False

    _PDF_BACKEND_WARNING_EMITTED = True
    msg = "PDF-Ausgabe nicht verfügbar: Modul 'reportlab' wurde nicht gefunden. Ausgabe erfolgt im Debug-Fenster."
    try:
        pdf_error = _pdf_backend_import_error()
        if pdf_error is not None:
            msg += f" ({pdf_error})"
    except Exception:
        pass

    try:
        mainapp = _resolve_runtime_mainapp()
        if mainapp is not None:
            mainapp.append_debug_output(msg)
            return False
    except Exception:
        pass

    try:
        debug_print(msg)
    except Exception:
        pass
    return False


def _coerce_margin_to_points(value: Any) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, float(value))

    s = ("" if value is None else str(value)).strip()
    if not s:
        raise RuntimeError("SET MARGIN TO: leerer Randwert ist nicht zulässig")

    m = re.fullmatch(r'([+-]?\d+(?:\.\d+)?)\s*(px|cm|pt)?', s, flags=re.IGNORECASE)
    if not m:
        raise RuntimeError(f"SET MARGIN TO: ungültiger Randwert: {s}")

    num = float(m.group(1))
    unit = (m.group(2) or 'pt').lower()

    if unit == 'pt':
        pts = num
    elif unit == 'cm':
        pts = num * 72.0 / 2.54
    elif unit == 'px':
        pts = num * 72.0 / 96.0
    else:
        raise RuntimeError(f"SET MARGIN TO: unbekannte Einheit: {unit}")

    return max(0.0, pts)


def _set_runtime_print_margin(*args):
    global _RUNTIME_PRINT_MARGINS

    if len(args) == 0:
        _RUNTIME_PRINT_MARGINS = dict(_RUNTIME_PRINT_MARGIN_DEFAULTS)
        if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT" and _RUNTIME_PRINT_PDF_PATH is not None:
            _render_runtime_output_pdf()
        return 0

    if len(args) not in (2, 4):
        raise RuntimeError("SET MARGIN TO erwartet 0, 2 oder 4 Werte")

    if len(args) == 2:
        left, top = (_coerce_margin_to_points(args[0]), _coerce_margin_to_points(args[1]))
        _RUNTIME_PRINT_MARGINS = {
            "left": left,
            "top": top,
            "right": float(_RUNTIME_PRINT_MARGIN_DEFAULTS["right"]),
            "bottom": float(_RUNTIME_PRINT_MARGIN_DEFAULTS["bottom"]),
        }
    else:
        left, top, right, bottom = (_coerce_margin_to_points(v) for v in args[:4])
        _RUNTIME_PRINT_MARGINS = {
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
        }

    if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT" and _RUNTIME_PRINT_PDF_PATH is not None:
        _render_runtime_output_pdf()
    return 0

def _get_runtime_current_color_style() -> dict[str, Any]:
    if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT":
        return _copy_runtime_color_style(_RUNTIME_PRINT_COLOR_STYLE)
    return _copy_runtime_color_style(_RUNTIME_SCREEN_COLOR_STYLE)

def _set_runtime_color(*args):
    global _RUNTIME_SCREEN_COLOR_STYLE, _RUNTIME_PRINT_COLOR_STYLE

    if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT":
        if len(args) == 0:
            _RUNTIME_PRINT_COLOR_STYLE = _make_default_print_style()
        else:
            _RUNTIME_PRINT_COLOR_STYLE = _style_from_vga_attr(args[0])
        return 0

    if len(args) == 0:
        _RUNTIME_SCREEN_COLOR_STYLE = _make_default_screen_style()
    else:
        _RUNTIME_SCREEN_COLOR_STYLE = _style_from_vga_attr(args[0])
    return 0


def _render_runtime_output_pdf():
    global _RUNTIME_PRINT_PDF_PATH

    if not _pdf_backend_available():
        _notify_pdf_backend_unavailable()
        return None

    if _RUNTIME_PRINT_PDF_PATH is None:
        return None

    pdf_path = Path(_RUNTIME_PRINT_PDF_PATH)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    pagesize = _pdf_pagesize_a4()
    pdf_canvas = _pdf_canvas_module()
    pdf_colors = _pdf_colors_module()
    if pagesize is None or pdf_canvas is None or pdf_colors is None:
        _notify_pdf_backend_unavailable()
        return None

    page_w, page_h = pagesize
    margin_left = float(_RUNTIME_PRINT_MARGINS.get("left", _RUNTIME_PRINT_MARGIN_DEFAULTS["left"]))
    margin_right = float(_RUNTIME_PRINT_MARGINS.get("right", _RUNTIME_PRINT_MARGIN_DEFAULTS["right"]))
    margin_top = float(_RUNTIME_PRINT_MARGINS.get("top", _RUNTIME_PRINT_MARGIN_DEFAULTS["top"]))
    margin_bottom = float(_RUNTIME_PRINT_MARGINS.get("bottom", _RUNTIME_PRINT_MARGIN_DEFAULTS["bottom"]))
    font_name = "Courier"
    font_size = 10
    line_height = 13
    max_width = max(20.0, page_w - margin_left - margin_right)

    c = pdf_canvas.Canvas(str(pdf_path), pagesize=pagesize)
    c.setTitle(pdf_path.stem)
    c.setAuthor("dBaseRunner")
    c.setSubject("SET FORMAT TO PRINT")

    y = page_h - margin_top

    def new_page():
        nonlocal y
        c.showPage()
        c.setFont(font_name, font_size)
        y = page_h - margin_top

    c.setFont(font_name, font_size)

    entries = _RUNTIME_PRINT_LINES[:] if _RUNTIME_PRINT_LINES else [{"text": "", "style": _copy_runtime_color_style(_RUNTIME_PRINT_COLOR_STYLE)}]
    for entry in entries:
        if isinstance(entry, dict):
            raw = entry.get("text", "")
            style = _copy_runtime_color_style(entry.get("style"))
        else:
            raw = str(entry)
            style = _copy_runtime_color_style(_RUNTIME_PRINT_COLOR_STYLE)

        fg_hex = style.get("fg_hex") or "#000000"
        bg_hex = style.get("bg_hex")
        wrapped = _wrap_pdf_text_line(raw, font_name=font_name, font_size=font_size, max_width=max_width)
        for line in wrapped:
            if y < margin_bottom:
                new_page()

            if bg_hex:
                try:
                    c.setFillColor(pdf_colors.HexColor(bg_hex))
                    c.rect(margin_left, y - 2, max_width, line_height, stroke=0, fill=1)
                except Exception:
                    pass

            try:
                c.setFillColor(pdf_colors.HexColor(fg_hex))
            except Exception:
                c.setFillColorRGB(0, 0, 0)

            c.drawString(margin_left, y, line)
            y -= line_height

    c.save()
    return pdf_path


def _ensure_runtime_print_pdf_path() -> Path:
    global _RUNTIME_PRINT_PDF_PATH

    if _RUNTIME_PRINT_PDF_PATH is not None:
        return Path(_RUNTIME_PRINT_PDF_PATH)

    base_path = _RUNTIME_PRINT_SCRIPT_PATH or (Path.cwd() / "script.prg")
    started = _RUNTIME_PRINT_STARTED_AT or datetime.datetime.now()
    stamp_date = started.strftime("%Y-%m-%d")
    stamp_time = started.strftime("%H-%M-%S")
    pdf_name = f"protokoll_{stamp_date}_{stamp_time}.pdf"
    proto_dir = base_path.resolve().parent / "proto"
    _RUNTIME_PRINT_PDF_PATH = proto_dir / pdf_name
    return Path(_RUNTIME_PRINT_PDF_PATH)


def _set_runtime_output_format(mode: str):
    global _RUNTIME_OUTPUT_FORMAT, _RUNTIME_PRINT_ENABLED

    mode = (mode or "SCREEN").strip().upper()
    if mode not in ("SCREEN", "PRINT"):
        raise RuntimeError(f"SET FORMAT TO {mode} ist nicht unterstützt")

    if mode == "PRINT" and not _pdf_backend_available():
        _notify_pdf_backend_unavailable()
        return 0

    _RUNTIME_OUTPUT_FORMAT = mode
    if mode == "PRINT":
        _RUNTIME_PRINT_ENABLED = True
        _ensure_runtime_print_pdf_path()
        _render_runtime_output_pdf()
    else:
        _RUNTIME_PRINT_ENABLED = False

    return 0


def _set_runtime_print_enabled(enabled: bool):
    global _RUNTIME_OUTPUT_FORMAT, _RUNTIME_PRINT_ENABLED

    enabled = bool(enabled)
    if enabled:
        if not _pdf_backend_available():
            _notify_pdf_backend_unavailable()
            return 0
        _RUNTIME_OUTPUT_FORMAT = "PRINT"
        _RUNTIME_PRINT_ENABLED = True
        _ensure_runtime_print_pdf_path()
        _render_runtime_output_pdf()
    else:
        _RUNTIME_PRINT_ENABLED = False
        if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT":
            _RUNTIME_OUTPUT_FORMAT = "SCREEN"

    return 0



def _set_runtime_escape_enabled(enabled: bool):
    global _RUNTIME_ESCAPE_ENABLED
    _RUNTIME_ESCAPE_ENABLED = bool(enabled)
    return 0


def _set_runtime_confirm_enabled(enabled: bool):
    global _RUNTIME_CONFIRM_ENABLED
    _RUNTIME_CONFIRM_ENABLED = bool(enabled)
    return 0


def _set_runtime_delete_enabled(enabled: bool):
    global _RUNTIME_DELETE_ENABLED
    _RUNTIME_DELETE_ENABLED = bool(enabled)
    return 0


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
class MyQtEventFilter(QObject):
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

# ---------------------------------------------------------------------------
# ExecVisitor - Interpreter for dBase DSL ...
# ---------------------------------------------------------------------------
class ExecVisitor(dBaseParserVisitor):
    def __init__(self):
        super().__init__()
        self.output  = []  # legacy buffer (WRITE wird direkt ins Debug-Fenster geroutet)
        self._mode = ""
        self._class_line_ranges = None
        
        self.vars: Dict[str, object] = {}   # normale Variablen
        self.this_obj: object | None = None # aktuelles "this"
        
        self.globals = {}
        self._scopes = [{}]        # stack of dicts
        
        self.env = ScopeStack()
        self.classes = {}          # className -> {"parent": str, "methods": {methodName: MethodDef}}
        
        self.classes["OBJECT"] = share.common.ClassDef(
            parent     = None,
            name       = "OBJECT",
            methods    = {"POPS": ""}
        )
        
        self.classes["PUSHBUTTON"] = share.common.ClassDef(
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
        
        self.methods = {}          # top-level METHOD name -> MethodDef / MethodDeclContext
        self._current_filename = ""

        self.frames: list[share.common.Frame] = [share.common.Frame(name="<global>")]  # globaler Frame
        self._current_class = None
        
        self.this_stack = []
        self.with_stack      : list[object] = []
        self.with_stack_owner: list[object] = []
        
        # --- DBF exclusive locks (USE ... EXCLUSIVE) ---
        # maps absolute dbf_path -> lockfile path
        self._dbf_exclusive_locks: dict[str, str] = {}
        
        # Builtins
        self.set_var("USE", self._builtin_USE)
        self.set_var("INPUT", self._builtin_INPUT)
        # interne Builtins aus der Vorverarbeitung
        self.set_var("__DBASE_USE__"            , self._builtin_USE)
        self.set_var("__DBASE_ERASE__"          , self._builtin_ERASE)
        self.set_var("__DBASE_SET_FORMAT__"     , self._builtin_SET_FORMAT)
        self.set_var("__DBASE_SET_PRINT__"      , self._builtin_SET_PRINT)
        self.set_var("__DBASE_SET_MARGIN__"     , self._builtin_SET_MARGIN)
        self.set_var("__DBASE_SET_COLOR__"      , self._builtin_SET_COLOR)
        self.set_var("__DBASE_SET_ESCAPE__"     , self._builtin_SET_ESCAPE)
        self.set_var("__DBASE_SET_CONFIRM__"    , self._builtin_SET_CONFIRM)
        self.set_var("__DBASE_SET_DELETE__"     , self._builtin_SET_DELETE)
        self.set_var("__DBASE_STORE__"          , self._builtin_STORE)
        self.set_var("__DBASE_SAVE__"           , self._builtin_SAVE)
        self.set_var("__DBASE_RESTORE__"        , self._builtin_RESTORE)
        self.set_var("__DBASE_RELEASE__"        , self._builtin_RELEASE)
        self.set_var("__DBASE_SELECT__"         , self._builtin_SELECT)
        self.set_var("__DBASE_RENAME__"         , self._builtin_RENAME)
        self.set_var("__DBASE_CLEAR_ALL__"      , self._builtin_CLEAR_ALL)
        self.set_var("__DBASE_SKIP__"           , self._builtin_SKIP)
        self.set_var("__DBASE_GOTO__"           , self._builtin_GOTO)
        self.set_var("__DBASE_DELETE_RECORD__"  , self._builtin_DELETE_RECORD)
        self.set_var("__DBASE_PACK__"           , self._builtin_PACK)
        self.set_var("__DBASE_ZAP__"            , self._builtin_ZAP)
        self.set_var("__DBASE_COUNT__"          , self._builtin_COUNT)

        # -----------------------------------------------------------------------
        # DBF-Arbeitsbereiche immer sofort initialisieren, damit SELECT/USE
        # bereits im ersten Script-Lauf sicher funktionieren.
        # -----------------------------------------------------------------------
        self._init_workareas()
    
    def _builtin_ERASE(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        _clear_runtime_output()
        return 0

    def _builtin_SET_FORMAT(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0

        norm_args = []
        for raw in args:
            if isinstance(raw, str):
                s = raw.strip()
                if not s:
                    continue
                norm_args.append(s)
            elif raw is not None:
                norm_args.append(str(raw))

        mode = "SCREEN"
        if norm_args:
            upper_args = [s.upper() for s in norm_args]
            if len(upper_args) >= 2 and upper_args[0] == "TO" and upper_args[1] in ("SCREEN", "PRINT"):
                mode = upper_args[1]
            elif upper_args[-1] in ("SCREEN", "PRINT"):
                mode = upper_args[-1]
            else:
                mode = upper_args[0]

        return _set_runtime_output_format(mode)

    def _builtin_SET_PRINT(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        enabled = False
        if args:
            raw = args[0]
            if isinstance(raw, str):
                enabled = raw.strip().upper() in ("1", "ON", "TRUE", ".T.", "T", "Y", ".Y.")
            else:
                enabled = bool(raw)
        return _set_runtime_print_enabled(enabled)

    def _builtin_SET_MARGIN(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        return _set_runtime_print_margin(*args)

    def _builtin_SET_COLOR(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        return _set_runtime_color(*args)

    def _builtin_SET_ESCAPE(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        enabled = False
        if args:
            raw = args[0]
            if isinstance(raw, str):
                enabled = raw.strip().upper() in ("1", "ON", "TRUE", ".T.", "T", "Y", ".Y.")
            else:
                enabled = bool(raw)
        return _set_runtime_escape_enabled(enabled)

    def _builtin_SET_DELETE(self, *args):
        pass
        
    def _builtin_SET_CONFIRM(self, *args):
        if getattr(self, "_mode", "exec") != "exec":
            return 0
        enabled = False
        if args:
            raw = args[0]
            if isinstance(raw, str):
                enabled = raw.strip().upper() in ("1", "ON", "TRUE", ".T.", "T", "Y", ".Y.")
            else:
                enabled = bool(raw)
        return _set_runtime_confirm_enabled(enabled)

    def _decode_builtin_text_arg(self, value, default: str = "") -> str:
        if value is None:
            return default
        s = str(value).strip()
        if not s:
            return default
        if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
            return self._unescape_string(s)
        if len(s) >= 2 and s[0] == '[' and s[-1] == ']':
            return self._unescape_bracket_string(s)
        return s

    def _is_reserved_memvar(self, name: str, value=None) -> bool:
        key = (name or '').upper()
        if key in ('THIS', 'SELF'):
            return True
        if key.startswith('__DBASE_'):
            return True
        if callable(value):
            return True
        return False

    def _match_mem_mask(self, name: str, mask: str) -> bool:
        import fnmatch
        return fnmatch.fnmatchcase((name or '').upper(), (mask or '').upper())

    def _flatten_memory_vars(self) -> dict[str, object]:
        merged: dict[str, object] = {}
        for scope in self._scopes:
            for key, value in scope.items():
                merged[key.upper()] = value
        return {k: v for k, v in merged.items() if not self._is_reserved_memvar(k, v)}

    def _select_memory_vars(self, mode: str = 'ALL', mask: str = '') -> dict[str, object]:
        mode = (mode or 'ALL').upper()
        mask = (mask or '').strip()
        items = self._flatten_memory_vars()
        if mode == 'ALL' or not mask:
            return dict(items)
        if mode == 'LIKE':
            return {k: v for k, v in items.items() if self._match_mem_mask(k, mask)}
        if mode == 'EXCEPT':
            return {k: v for k, v in items.items() if not self._match_mem_mask(k, mask)}
        raise RuntimeError(f"SAVE/RELEASE: unbekannter Auswahlmodus '{mode}'")

    def _jsonify_mem_value(self, value, var_name: str = ''):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, Path):
            return str(value)
        if isinstance(value, (list, tuple)):
            return [self._jsonify_mem_value(v, var_name) for v in value]
        if isinstance(value, dict):
            return {str(k): self._jsonify_mem_value(v, var_name) for k, v in value.items()}
        raise RuntimeError(f"SAVE: Variable '{var_name}' ist nicht JSON-serialisierbar ({type(value).__name__})")

    def _resolve_memfile_path(self, filename: str = '', drive: str = '') -> Path:
        name = self._decode_builtin_text_arg(filename, 'memory.mem').strip()
        if not name:
            name = 'memory.mem'
        if not Path(name).suffix:
            name += '.mem'

        drv = self._decode_builtin_text_arg(drive, '').strip().rstrip(':')
        if drv:
            base = Path(f"{drv.upper()}:\\")
            path = base / name
        else:
            path = Path(name)
            if not path.is_absolute():
                cur = getattr(self, '_current_filename', '') or ''
                base_dir = Path(cur).resolve().parent if cur else Path.cwd()
                path = base_dir / path
        return Path(os.path.abspath(str(path)))

    def _confirm_memfile_overwrite(self, path: Path) -> None:
        if not path.exists() or not _RUNTIME_CONFIRM_ENABLED:
            return

        parent = share.common.MAINAPP if 'MAINAPP' in globals() else None
        answer = QMessageBox.question(
            parent,
            'Datei überschreiben?',
            f'Die Datei existiert bereits und wird überschrieben:\n\n{path}\n\nSoll die Datei überschrieben werden?',
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        if answer != QMessageBox.Ok:
            raise share.common.ProgramAbortSignal()

        backup_path = path.with_name(path.name + '.bak')
        shutil.copy2(str(path), str(backup_path))

    def _clear_memory_variables(self):
        for scope in self._scopes:
            for key in list(scope.keys()):
                value = scope.get(key)
                if self._is_reserved_memvar(key, value):
                    continue
                scope.pop(key, None)

    def _delete_memory_variable(self, name: str):
        key = (name or '').strip().upper()
        if not key:
            return
        for scope in self._scopes:
            scope.pop(key, None)


    def _workarea_empty(self) -> dict[str, object]:
        return {
            "dbf_path"  : "",
            "indexes"   : [],
            "fields"    : [],
            "records"   : [],
            "pointer"   : 1,
            "eof"       : True,
            "version"   : 0x03,
        }

    def _workarea_state_file_path(self) -> Path:
        return Path(tempfile.gettempdir()) / ".dbase_workareas.json"

    def _mark_hidden_path(self, path: Path) -> None:
        try:
            if SystemInfo.is_windows():
                ctypes.windll.kernel32.SetFileAttributesW(str(path), 0x02)
        except Exception:
            pass

    def _init_workareas(self):
        self._selected_workarea = 0
        self._workareas = {i: self._workarea_empty() for i in range(65)}
        self._workarea_state_path = self._workarea_state_file_path()
        self._sync_workareas_state()

    def _sync_workareas_state(self):
        try:
            payload = {
                "selected": int(getattr(self, "_selected_workarea", 0)),
                "workareas": {},
            }
            for idx, ws in getattr(self, "_workareas", {}).items():
                recs = ws.get("records", []) or []
                payload["workareas"][str(idx)] = {
                    "dbf_path": ws.get("dbf_path", ""),
                    "indexes": list(ws.get("indexes", []) or []),
                    "pointer": int(ws.get("pointer", 1) or 1),
                    "eof": bool(ws.get("eof", True)),
                    "record_count": len(recs),
                    "deleted_count": sum(1 for r in recs if r.get("__deleted__")),
                }
            self._workarea_state_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            self._mark_hidden_path(self._workarea_state_path)
        except Exception:
            pass

    def _current_workarea(self) -> dict[str, object]:
        if not hasattr(self, "_workareas") or not hasattr(self, "_selected_workarea"):
            self._init_workareas()
        idx = int(getattr(self, "_selected_workarea", 0) or 0)
        if idx < 0 or idx > 64:
            idx = 0
            self._selected_workarea = 0
        if idx not in self._workareas:
            self._workareas[idx] = self._workarea_empty()
        return self._workareas[idx]

    def _resolve_db_path(self, filename: str = "", default_ext: str = ".dbf") -> Path:
        name = self._decode_builtin_text_arg(filename, "").strip()
        if not name:
            return Path("")
        p = Path(name)
        if not p.suffix and default_ext:
            p = Path(str(p) + default_ext)
        if not p.is_absolute():
            cur = getattr(self, "_current_filename", "") or ""
            base_dir = Path(cur).resolve().parent if cur else Path.cwd()
            p = base_dir / p
        return Path(os.path.abspath(str(p)))

    def _resolve_index_paths(self, index_text: str = "", dbf_path: Path | None = None) -> list[str]:
        raw = self._decode_builtin_text_arg(index_text, "").strip()
        if not raw:
            return []
        base_dir = dbf_path.parent if isinstance(dbf_path, Path) and str(dbf_path) else (Path(getattr(self, "_current_filename", "")).resolve().parent if getattr(self, "_current_filename", "") else Path.cwd())
        parts = [p.strip() for p in self._split_args(raw) if p.strip()]
        resolved = []
        for part in parts:
            val = self._decode_builtin_text_arg(part, part).strip()
            if not val:
                continue
            p = Path(val)
            if not p.suffix:
                p = Path(str(p) + ".ndx")
            if not p.is_absolute():
                p = base_dir / p
            resolved.append(str(Path(os.path.abspath(str(p)))))
        return resolved

    def _dbf_read_header_runtime(self, path: str):
        with open(path, "rb") as f:
            hdr = f.read(32)
            if len(hdr) < 32:
                raise ValueError("DBF header too short")
            version = hdr[0]
            num_records = int.from_bytes(hdr[4:8], "little")
            header_len = int.from_bytes(hdr[8:10], "little")
            record_len = int.from_bytes(hdr[10:12], "little")

            f.seek(32)
            desc = f.read(max(0, header_len - 32))
            end = desc.find(b"\x0D")
            if end == -1:
                end = len(desc)
            desc = desc[:end]

            def _parse_standard_32(desc_bytes: bytes):
                parsed: list[DbfFieldSpec] = []
                offset = 1
                for i in range(0, len(desc_bytes), 32):
                    ch = desc_bytes[i:i+32]
                    if len(ch) < 32:
                        break
                    name_raw = ch[0:11].split(b"\x00", 1)[0]
                    name = name_raw.decode("ascii", errors="ignore").strip()
                    if not name:
                        continue
                    ftype = chr(ch[11]).upper()
                    flen = int(ch[16])
                    fdec = int(ch[17])
                    parsed.append(DbfFieldSpec(name=name, ftype=ftype, length=flen, decimals=fdec, offset=offset))
                    offset += flen
                return parsed

            def _parse_extended_48(desc_bytes: bytes):
                # Fallback für zuvor erzeugte DBF-Dateien mit 48-Byte-Deskriptoren
                # (32 Byte Feldname, Typ an Offset 32, Länge an 33, Dezimalen an 34).
                parsed: list[DbfFieldSpec] = []
                offset = 1
                for i in range(0, len(desc_bytes), 48):
                    ch = desc_bytes[i:i+48]
                    if len(ch) < 35:
                        break
                    name_raw = ch[0:32].split(b"\x00", 1)[0]
                    name = name_raw.decode("ascii", errors="ignore").strip()
                    if not name:
                        continue
                    try:
                        ftype = chr(ch[32]).upper()
                    except Exception:
                        continue
                    flen = int(ch[33]) if len(ch) > 33 else 0
                    fdec = int(ch[34]) if len(ch) > 34 else 0
                    if flen <= 0:
                        continue
                    parsed.append(DbfFieldSpec(name=name, ftype=ftype, length=flen, decimals=fdec, offset=offset))
                    offset += flen
                return parsed

            fields: list[DbfFieldSpec] = _parse_standard_32(desc)
            if not fields:
                fields = _parse_extended_48(desc)
            return version, header_len, record_len, num_records, fields

    def _dbf_decode_field_runtime(self, spec: DbfFieldSpec, raw: bytes):
        s = raw.decode("cp1252", errors="ignore")
        if spec.ftype in ("C", "M"):
            return s.rstrip()
        if spec.ftype in ("N", "F", "I"):
            txt = s.strip()
            if not txt:
                return 0
            try:
                if spec.decimals:
                    return float(txt.replace(",", "."))
                return int(float(txt.replace(",", ".")))
            except Exception:
                return txt
        if spec.ftype == "L":
            v = s.strip().upper()
            return True if v in ("T", "Y", "1") else False
        if spec.ftype == "D":
            return s.strip()
        return s.rstrip()

    def _dbf_encode_field_runtime(self, spec: DbfFieldSpec, value) -> bytes:
        if spec.ftype in ("C", "M"):
            txt = str(value or "")
            b = txt.encode("cp1252", errors="replace")[:spec.length]
            return b.ljust(spec.length, b" ")
        if spec.ftype in ("N", "F", "I"):
            if value is None or value == "":
                txt = ""
            elif isinstance(value, float) and spec.decimals:
                txt = f"{value:.{spec.decimals}f}"
            else:
                txt = str(value).strip().replace(",", ".")
            b = txt.encode("ascii", errors="ignore")[:spec.length]
            return b.rjust(spec.length, b" ")
        if spec.ftype == "L":
            ch = b"T" if bool(value) else b"F"
            return ch.ljust(spec.length, b" ")
        if spec.ftype == "D":
            txt = str(value or "").strip()
            b = txt.encode("ascii", errors="ignore")[:spec.length]
            return b.ljust(spec.length, b" ")
        txt = str(value or "")
        b = txt.encode("cp1252", errors="replace")[:spec.length]
        return b.ljust(spec.length, b" ")

    def _load_dbf_workarea(self, path: Path) -> dict[str, object]:
        version, header_len, record_len, num_records, fields = self._dbf_read_header_runtime(str(path))
        records = []
        with open(path, "rb") as f:
            f.seek(header_len)
            for recno in range(1, num_records + 1):
                rec = f.read(record_len)
                if len(rec) < record_len:
                    break
                deleted = rec[:1] == b"*"
                row = {"__deleted__": bool(deleted), "__recno__": recno}
                for spec in fields:
                    raw = rec[spec.offset:spec.offset + spec.length]
                    row[spec.name.upper()] = self._dbf_decode_field_runtime(spec, raw)
                records.append(row)
        ws = self._workarea_empty()
        ws.update({
            "dbf_path": str(path),
            "indexes": [],
            "fields": fields,
            "records": records,
            "pointer": 1,
            "eof": len(records) == 0,
            "version": version or 0x03,
        })
        return ws

    def _save_dbf_workarea(self, ws: dict[str, object]) -> None:
        path = Path(ws.get("dbf_path", ""))
        fields: list[DbfFieldSpec] = list(ws.get("fields", []) or [])
        records = list(ws.get("records", []) or [])
        if not path:
            return
        nfields = len(fields)
        header_len = 32 + 32 * nfields + 1
        record_len = 1 + sum(f.length for f in fields)
        today = datetime.date.today()

        hdr        = bytearray(32)
        hdr[0]     = int(ws.get("version", 0x03) or 0x03)
        hdr[1]     = today.year - 1900
        hdr[2]     = today.month
        hdr[3]     = today.day
        hdr[4:8]   = int(len(records)).to_bytes(4, "little", signed=False)
        hdr[8:10]  = int(header_len).to_bytes(2, "little", signed=False)
        hdr[10:12] = int(record_len).to_bytes(2, "little", signed=False)

        out = bytearray()
        out += hdr
        for spec in fields:
            desc = bytearray(32)
            nb = spec.name.encode("ascii", errors="ignore")[:11]
            desc[0:len(nb)] = nb
            desc[11] = ord(spec.ftype[:1])
            desc[16] = int(spec.length) & 0xFF
            desc[17] = int(spec.decimals) & 0xFF
            out += desc
        out += b"\x0D"

        for row in records:
            rec = bytearray()
            rec += b"*" if row.get("__deleted__") else b" "
            for spec in fields:
                rec += self._dbf_encode_field_runtime(spec, row.get(spec.name.upper()))
            out += rec

        out += b"\x1A"
        path.write_bytes(bytes(out))

    def _set_workarea_pointer(self, ws: dict[str, object], pointer: int) -> int:
        records = list(ws.get("records", []) or [])
        count = len(records)
        if count <= 0:
            ws["pointer"] = 1
            ws["eof"] = True
            return 1
        pointer = int(pointer or 1)
        if pointer < 1:
            pointer = 1
        if pointer > count:
            ws["pointer"] = count + 1
            ws["eof"] = True
            return ws["pointer"]
        ws["pointer"] = pointer
        ws["eof"] = False
        return pointer

    def _current_record(self) -> dict[str, object] | None:
        ws = self._current_workarea()
        records = list(ws.get("records", []) or [])
        ptr = int(ws.get("pointer", 1) or 1)
        if ptr < 1 or ptr > len(records):
            return None
        return records[ptr - 1]

    def _confirm_runtime_action(self, title: str, text: str) -> None:
        if not _RUNTIME_CONFIRM_ENABLED:
            return
        parent = share.common.MAINAPP if 'MAINAPP' in globals() else None
        answer = QMessageBox.question(
            parent,
            title,
            text,
            QMessageBox.Ok | QMessageBox.Cancel,
            QMessageBox.Cancel
        )
        if answer != QMessageBox.Ok:
            raise share.common.ProgramAbortSignal()

    def _record_visible_for_runtime(self, rec: dict[str, object] | None) -> bool:
        if rec is None:
            return False
        if _RUNTIME_DELETE_ENABLED and bool(rec.get('__deleted__')):
            return False
        return True

    def _count_records_runtime(self, range_part: str = '', mode: str = '', cond_expr: str = '') -> int:
        ws = self._current_workarea()
        records = list(ws.get('records', []) or [])
        old_ptr = int(ws.get('pointer', 1) or 1)
        old_eof = bool(ws.get('eof', True))
        total = 0

        # Bereich derzeit reserviert; standardmäßig werden alle Datensätze geprüft.
        start_idx = 1
        end_idx = len(records)

        mode_up = (mode or '').strip().upper()
        cond_expr = (cond_expr or '').strip()

        try:
            for recno in range(start_idx, end_idx + 1):
                self._set_workarea_pointer(ws, recno)
                rec = self._current_record()
                if rec is None:
                    break

                visible = self._record_visible_for_runtime(rec)
                cond_ok = True
                if cond_expr:
                    cond_ok = bool(self._eval_expr_text_from_source(cond_expr))

                if mode_up == 'WHILE':
                    if not cond_ok:
                        break
                    if visible:
                        total += 1
                elif mode_up == 'FOR':
                    if visible and cond_ok:
                        total += 1
                else:
                    if visible:
                        total += 1
        finally:
            ws['pointer'] = old_ptr
            ws['eof'] = old_eof

        return total

    def _builtin_SELECT(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        area = 0
        if args:
            try:
                area = int(float(args[0]))
            except Exception:
                area = 0
        if area < 0 or area > 64:
            parent = share.common.MAINAPP if 'MAINAPP' in globals() else None
            try:
                QMessageBox.warning(parent, 'Arbeitsbereich', 'Arbeitsbereich außerhalb des gültigen Bereichs 0..64. Es wird auf Arbeitsbereich 0 gewechselt.')
            except Exception:
                pass
            area = 0
        self._selected_workarea = area
        self._sync_workareas_state()
        return area

    def _builtin_RENAME(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        if len(args) < 2:
            raise RuntimeError('RENAME erwartet alten und neuen Dateinamen')
        old_path = self._resolve_db_path(args[0], '.dbf')
        new_name_raw = self._decode_builtin_text_arg(args[1], '').strip()
        if not old_path or not str(old_path):
            raise RuntimeError('RENAME: alter Dateiname fehlt')
        if not old_path.exists():
            raise RuntimeError(f'RENAME: Datei wurde nicht gefunden: {old_path}')
        if not new_name_raw:
            raise RuntimeError('RENAME: neuer Dateiname fehlt')
        new_path = Path(new_name_raw)
        if not new_path.suffix:
            new_path = Path(str(new_path) + (old_path.suffix or '.dbf'))
        if not new_path.is_absolute():
            new_path = old_path.parent / new_path

        self._confirm_runtime_action('Datei umbenennen?', f'Soll die Datei umbenannt werden?\n\n{old_path}\n→\n{new_path}')
        os.replace(str(old_path), str(new_path))

        old_abs = str(old_path.resolve())
        new_abs = str(new_path.resolve())
        for idx, ws in self._workareas.items():
            if ws.get('dbf_path', '') and str(Path(ws['dbf_path']).resolve()) == old_abs:
                reloaded = self._load_dbf_workarea(Path(new_abs))
                reloaded['indexes'] = list(ws.get('indexes', []) or [])
                self._set_workarea_pointer(reloaded, 1)
                self._workareas[idx] = reloaded

        self._sync_workareas_state()
        return 1

    def _builtin_CLEAR_ALL(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        self._clear_memory_variables()
        self._init_workareas()
        return 1

    def _builtin_SKIP(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        count = 1
        if args:
            try:
                count = int(float(args[0]))
            except Exception:
                count = 1
        ws = self._current_workarea()
        self._set_workarea_pointer(ws, int(ws.get('pointer', 1) or 1) + count)
        self._sync_workareas_state()
        return int(ws.get('pointer', 1) or 1)

    def _builtin_GOTO(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        records = list(ws.get('records', []) or [])
        count = len(records)
        target = args[0] if args else 'TOP'
        if isinstance(target, str):
            up = target.strip().upper()
            if up == 'TOP':
                self._set_workarea_pointer(ws, 1)
                self._sync_workareas_state()
                return 1
            if up == 'BOTTOM':
                self._set_workarea_pointer(ws, count if count > 0 else 1)
                self._sync_workareas_state()
                return int(ws.get('pointer', 1) or 1)
        try:
            recno = int(float(target))
        except Exception:
            recno = 1

        if recno < 1 or recno > max(1, count):
            parent = share.common.MAINAPP if 'MAINAPP' in globals() else None
            try:
                QMessageBox.warning(parent, 'Datensatzzeiger', 'Ungültige Datensatznummer. Es wird auf Datensatz 1 gewechselt.')
            except Exception:
                pass
            recno = 1
        self._set_workarea_pointer(ws, recno)
        self._sync_workareas_state()
        return int(ws.get('pointer', 1) or 1)

    def _builtin_DELETE_RECORD(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        rec = self._current_record()
        if rec is None:
            return 0
        rec['__deleted__'] = True
        self._save_dbf_workarea(ws)
        self._sync_workareas_state()
        return 1

    def _builtin_PACK(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        if not ws.get('dbf_path'):
            return 0
        self._confirm_runtime_action('PACK', 'Sollen die löschmarkierten Datensätze endgültig entfernt werden?')
        records = [r for r in list(ws.get('records', []) or []) if not r.get('__deleted__')]
        ws['records'] = records
        self._save_dbf_workarea(ws)
        self._set_workarea_pointer(ws, 1)
        self._sync_workareas_state()
        return len(records)

    def _builtin_ZAP(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        ws = self._current_workarea()
        if not ws.get('dbf_path'):
            return 0
        self._confirm_runtime_action('ZAP', 'Sollen alle Datensätze endgültig gelöscht werden?')
        ws['records'] = []
        self._save_dbf_workarea(ws)
        self._set_workarea_pointer(ws, 1)
        self._sync_workareas_state()
        return 0

    def _builtin_COUNT(self, *args):
        pass
        
    def _builtin_STORE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        if len(args) < 2:
            raise RuntimeError('STORE erwartet einen Ausdruck und eine Zielvariable')
        value = args[0]
        target_name = self._decode_builtin_text_arg(args[1], '').strip()
        if not target_name:
            raise RuntimeError('STORE: Zielvariable fehlt')
        self._assign_input_target(target_name, value)
        return value

    def _builtin_SAVE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        filename = args[0] if len(args) > 0 else ''
        mode = self._decode_builtin_text_arg(args[1] if len(args) > 1 else 'ALL', 'ALL').upper()
        mask = self._decode_builtin_text_arg(args[2] if len(args) > 2 else '', '')
        drive = args[3] if len(args) > 3 else ''

        path = self._resolve_memfile_path(filename, drive)
        selected = self._select_memory_vars(mode, mask)
        payload_vars = {key: self._jsonify_mem_value(value, key) for key, value in selected.items()}

        path.parent.mkdir(parents=True, exist_ok=True)
        self._confirm_memfile_overwrite(path)
        payload = {
            'format': 'dbase.mem.json',
            'saved_at': datetime.datetime.now().isoformat(timespec='seconds'),
            'variables': payload_vars,
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
        return 1

    def _builtin_RESTORE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        filename = args[0] if len(args) > 0 else ''
        additive = bool(args[1]) if len(args) > 1 else False
        drive = args[2] if len(args) > 2 else ''
        path = self._resolve_memfile_path(filename, drive)
        if not path.exists():
            raise RuntimeError(f'RESTORE: Datei wurde nicht gefunden: {path}')

        data = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data, dict) and isinstance(data.get('variables'), dict):
            variables = data['variables']
        elif isinstance(data, dict):
            variables = data
        else:
            raise RuntimeError('RESTORE: ungültiges Speicherformat')

        if not additive:
            self._clear_memory_variables()

        for key, value in variables.items():
            self._set_name(str(key), value, None)
        return len(variables)

    def _builtin_RELEASE(self, *args):
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0
        names_text = self._decode_builtin_text_arg(args[0] if len(args) > 0 else '', '')
        mode = self._decode_builtin_text_arg(args[1] if len(args) > 1 else 'LIST', 'LIST').upper()
        mask = self._decode_builtin_text_arg(args[2] if len(args) > 2 else '', '')

        if mode == 'ALL':
            self._clear_memory_variables()
            return 0
        if mode in ('LIKE', 'EXCEPT'):
            selected = self._select_memory_vars(mode, mask)
            for key in list(selected.keys()):
                self._delete_memory_variable(key)
            return len(selected)

        names = [part.strip() for part in names_text.split(',') if part.strip()]
        for name in names:
            self._delete_memory_variable(name)
        return len(names)

    def _builtin_USE(self, *args):
        """
        USE <table> [INDEX idx1, idx2, ...]
        Ohne Parameter wird der aktive Arbeitsbereich geschlossen.
        """
        if getattr(self, '_mode', 'exec') != 'exec':
            return 0

        filename = args[0] if len(args) > 0 else ''
        index_text = args[1] if len(args) > 1 else ''
        _exclusive = bool(args[2]) if len(args) > 2 else False

        raw_name = self._decode_builtin_text_arg(filename, '').strip()
        ws = self._current_workarea()

        if not raw_name:
            self._workareas[self._selected_workarea] = self._workarea_empty()
            self._sync_workareas_state()
            return 0

        path = self._resolve_db_path(raw_name, '.dbf')
        if not path.exists():
            raise RuntimeError(f"USE: Datei wurde nicht gefunden: {path}")

        loaded = self._load_dbf_workarea(path)
        loaded['indexes'] = self._resolve_index_paths(index_text, path)
        self._set_workarea_pointer(loaded, 1)
        self._workareas[self._selected_workarea] = loaded
        self._sync_workareas_state()
        return 1
        
    @property
    def current_frame(self) -> share.common.Frame:
        return self.frames[-1]
    
    @property
    def current_with_base(self):
        return self.with_stack[-1] if self.with_stack else None

    def push_frame(self, name: str, args: list[Any] | None = None) -> None:
        self.frames.append(share.common.Frame(name=name, args=list(args or [])))

    def pop_frame(self) -> share.common.Frame:
        if len(self.frames) <= 1:
            raise RuntimeError("Cannot pop global frame")
        return self.frames.pop()
    
    def push_this(self, inst: share.common.Instance):
        self.this_stack.append(inst)

    def pop_this(self):
        self.this_stack.pop()

    def cur_this(self) -> share.common.Instance:
        if not self.this_stack:
            raise RuntimeError("THIS ist nicht gesetzt")
        return self.this_stack[-1]

    
    def _acquire_dbf_exclusive_lock(self, dbf_path: str) -> None:
        lock_path = dbf_path + ".lck"
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8", errors="ignore") as f:
                f.write(str(os.getpid()))
        except FileExistsError:
            raise RuntimeError(f"DBF ist bereits exklusiv gesperrt: {dbf_path}")
        self._dbf_exclusive_locks[dbf_path] = lock_path
    
    # ----------------- MENU / POPUPMENU helpers -----------------
    def _detach_menu(self, inst: share.common.Instance) -> None:
        """Entfernt ein bereits angehängtes Menü aus MenuBar oder Parent-Menu (wenn möglich)."""
        try:
            container = inst.props.get("_QT_MENU_CONTAINER")  # QMenuBar oder QMenu
            action = inst.props.get("_QT_MENU_ACTION")        # QAction
            if container is not None and action is not None and hasattr(container, "removeAction"):
                container.removeAction(action)
        except Exception:
            pass
        inst.props["_QT_MENU_CONTAINER"] = None
        inst.props["_QT_MENU_ACTION"] = None

    def _attach_menu(self, inst: share.common.Instance, parent_inst: Any) -> None:
        """Hängt MENU/POPUPMENU an parent_inst (MENU => Submenu; MainWindow => Menübar)."""
        if inst is None or inst.backend is None:
            return
        if inst.class_name.upper() not in ("MENU", "POPUPMENU"):
            return

        self._detach_menu(inst)

        # Parent kann None sein (dann nur "lose" QMenu-Instanz)
        if not isinstance(parent_inst, share.common.Instance) or parent_inst.backend is None:
            return

        pb = parent_inst.backend

        # 1) Parent ist MENU/POPUPMENU => submenu
        if parent_inst.class_name.upper() in ("MENU", "POPUPMENU") and hasattr(pb, "addMenu"):
            act = pb.addMenu(inst.backend)  # returns QAction
            inst.props["_QT_MENU_CONTAINER"] = pb
            inst.props["_QT_MENU_ACTION"] = act
            inst.parent = parent_inst
            return

        # 2) Parent ist ein Qt-MainWindow (oder kompatibel) => MenuBar
        if hasattr(pb, "menuBar"):
            mb = pb.menuBar()
            if mb is not None and hasattr(mb, "addMenu"):
                act = mb.addMenu(inst.backend)  # returns QAction
                inst.props["_QT_MENU_CONTAINER"] = mb
                inst.props["_QT_MENU_ACTION"] = act
                inst.parent = parent_inst
                return

        # 3) Fallback: wenn Parent selbst eine MenuBar ist
        if hasattr(pb, "addMenu"):
            act = pb.addMenu(inst.backend)
            inst.props["_QT_MENU_CONTAINER"] = pb
            inst.props["_QT_MENU_ACTION"] = act
            inst.parent = parent_inst
            return

    def reparent_instance(self, child: share.common.Instance, new_parent: Optional[share.common.Instance]) -> None:
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

    def bind_child(self, owner: share.common.Instance, name: str, child: share.common.Instance):
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
    
    def cur_with_target(self) -> Optional[share.common.Instance]:
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

            if isinstance(target, share.common.Instance):
                self.set_prop(target, name.upper(), value, ctx)
                return None

            # z.B. WITH(Font) bold = .T.
            self.set_member(target, name, value, ctx)

            # wenn WITH(Font): neu anwenden
            if owner is not None and isinstance(target, share.common.FontValue):
                self.set_prop(owner, "FONT", target, ctx)

            return None

        # 2) Kette: Font.bold = .T.   innerhalb WITH(Sender)
        cur = target
        for seg in parts[:-1]:
            cur = self.get_member(cur, seg, ctx)

        self.set_member(cur, parts[-1], value, ctx)

        # wenn innerhalb WITH(Sender): Font.* geändert -> auf Sender neu setzen
        if isinstance(target, share.common.Instance) and parts and parts[0].upper() == "FONT":
            fv = target.props.get("FONT")
            if isinstance(fv, share.common.FontValue):
                self.set_prop(target, "FONT", fv, ctx)

        # wenn wir in WITH(Font) sind: owner neu setzen
        if owner is not None and isinstance(target, share.common.FontValue):
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

        # classDecl darf im Exec-Pass nie als normales Statement herunterlaufen.
        # In der Grammar ist classDecl sowohl als item als auch als statement erlaubt.
        # Falls der Parse-Tree hier dennoch eine Klassendeklaration liefert,
        # würden sonst Header-Tokens wie "ParentForm" als exprStmt/memberExpr
        # fehlinterpretiert werden.
        try:
            if hasattr(ctx, "classDecl") and ctx.classDecl() is not None:
                return None
        except Exception:
            pass

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
            self._ensure_class_methods_loaded(c)
            cdef = self.classes.get(c)
            if cdef is None:
                raise Exception(f"{ctx.start.line}:{ctx.start.column}: Klasse '{c}' ist nicht definiert")

            # ClassDef statt dict
            if m in cdef.methods:
                return c, cdef.methods[m]

            found = self._find_method_decl_in_tree(c, m)
            if found is None:
                found = self._find_method_decl_in_source(c, m)
            if found is not None:
                cdef.methods[m] = found
                self.classes[c] = cdef
                return c, found

            c = cdef.parent.upper() if cdef.parent else None

        raise Exception(f"{ctx.start.line}:{ctx.start.column}: Methode '{m}' nicht gefunden (ab '{start_class}')")


    def resolve_method_silent(self, class_name: str, method_name: str):
        c = class_name.upper() if class_name else None
        m = method_name.upper()

        while c:
            self._ensure_class_methods_loaded(c)
            cdef = self.classes.get(c)
            if cdef is None:
                return None

            methods = getattr(cdef, "methods", {}) or {}
            if m in methods:
                return methods[m]

            found = self._find_method_decl_in_tree(c, m)
            if found is None:
                found = self._find_method_decl_in_source(c, m)
            if found is not None:
                cdef.methods[m] = found
                self.classes[c] = cdef
                return found

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
            if not isinstance(h, share.common.Delegate):
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
                except (ReturnSignal, share.common.ProgramAbortSignal):
                    # RETURN in Handler -> nur diesen Handler beenden, nächste weiter
                    continue
            return None
        return wrapper
    
    def get_member(self, obj, prop: str, ctx=None):
        key = prop.upper()
        
        # --- QFont support ---
        if isinstance(obj, share.common.FontValue):
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
            
        if isinstance(obj, share.common.Instance):
            # 0) Parent chain
            if key == "PARENT":
                return obj.parent

            # 1) zuerst direkt in props, dann robust in children
            if key in obj.props:
                return obj.props[key]
            if key in obj.children:
                child = obj.children[key]
                # props/cache nachziehen, damit zukünftige Lookups konsistent sind
                obj.props[key] = child
                return child
            
            if key == "FONT" and getattr(obj, "backend", None) is not None and hasattr(obj.backend, "font"):
                qf = obj.backend.font()  # QFont vom Widget
                fv = share.common.FontValue(
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
                        mdi = share.common.find_mdi_subwindow(b)
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
                if self.resolve_method_silent(cls_name.upper(), key) is not None:
                    return share.common.Delegate(target=obj, method_name=key, runner=self)

            # ✅ 3) Native Methode: OPEN (für FORM und alles was davon erbt)
            if key == "OPEN" and cls_name and self.is_descendant_of(cls_name.upper(), "FORM"):
                return share.common.Delegate(target=obj, method_name="OPEN", runner=self)

            raise RuntimeError(f"{self.loc(ctx)}: Member '{prop}' in {cls_name} nicht gefunden")

    def set_member(self, obj, prop: str, value, ctx):
        key = prop.upper()
        
        # --- QFont support ---
        if isinstance(obj, share.common.FontValue):
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

        if not isinstance(obj, share.common.Instance):
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
        if isinstance(obj, share.common.Instance):
            # 1) Field/Property?
            # falls du z.B. obj.fields als dict hast:
            if hasattr(obj, "props") and key in obj.props:
                return obj.props[key]

            # 2) Methode?
            res = self.resolve_method_silent(obj.class_name.upper(), key)
            if res is not None:
                # Delegate ist bei dir offenbar genau das, was CallExpr ausführen kann
                return share.common.Delegate(target=obj, method_name=key, runner=self)

            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Member '{name}' nicht gefunden")

        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Memberzugriff auf Nicht-Objekt: {type(obj).__name__}")
    
    def call_delegate(self, d: share.common.Delegate, args: list, ctx):
        # d.target ist deine Instance, d.method_name z.B. "INIT"
        return self.invoke_method(d.target, d.method_name, args, ctx)
        
    def visitCallExpr(self, ctx):
        callee = self.visit(ctx.expr())  # oder ctx.callee o.ä.
        args = []
        if ctx.argList() is not None:
            args = [self.visit(a) for a in ctx.argList().expr()]

        # ✅ Delegate direkt ausführen
        if isinstance(callee, share.common.Delegate):
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
            if not isinstance(this_obj, share.common.Instance):
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
            return share.common.Delegate(target=this_obj, method_name=mname, runner=self)

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


            if isinstance(cur, share.common.Instance):
                if hasattr(cur, "props") and key in cur.props:
                    cur = cur.props[key]
                    if cur is None and name != parts[-1]:
                        raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: '{prev_path}' ist None (z.B. Parent nicht gesetzt)")
                    continue

                if self.resolve_method_silent(cur.class_name.upper(), key) is not None:
                    cur = share.common.Delegate(target=cur, method_name=key, runner=self)
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
                    return share.common.Delegate(target=cur, method_name=name.upper(), runner=self)

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
        if isinstance(cur, share.common.Instance):
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
            
            return share.common.FontValue(
                obj         = font_obj,
                family      = family,
                size        = size,
                bold        = bold,
                italic      = italic,
                underline   = underline)


        # 1b) MENU / POPUPMENU (Qt: QMenu)
        # dBase-Semantik: NEW MENU(THIS) => Menu an Parent (MainWindow-Menubar oder Parent-Menu) anhängen.
        if cn in ("MENU", "POPUPMENU"):
            parent_inst = args[0] if args else None
            parent_backend = parent_inst.backend if isinstance(parent_inst, share.common.Instance) else None

            inst = share.common.Instance(class_name=cn)
            if isinstance(parent_inst, share.common.Instance):
                inst.parent = parent_inst

            # Backend ist immer ein QMenu
            inst.backend = QMenu(parent_backend) if parent_backend is not None else QMenu()

            # Anhängen (wenn Parent mitgegeben)
            try:
                self._attach_menu(inst, parent_inst)
            except Exception:
                # absichtlich leise: Parent kann später per Property gesetzt werden
                pass

            return inst

        # 2) native Qt-Klassen (FORM, PUSHBUTTON, ...)
        if cn in NATIVE_BASES:
            parent_inst = args[0] if args else None
            parent_backend = parent_inst.backend if isinstance(parent_inst, share.common.Instance) else None

            inst = share.common.Instance(class_name=cn)
            if isinstance(parent_inst, share.common.Instance):
                inst.parent = parent_inst
            inst.backend = create_backend_for_base(cn, parent_backend)
            return inst

        # 3) user-defined Klassen
        self._hydrate_class_from_source(cn)
        cdef = self.classes.get(cn)
        if cdef is None:
            known = ", ".join(sorted(self.classes.keys()))
            raise RuntimeError(
                f"{self.loc(None)}: Klasse '{cn}' ist nicht definiert. "
                f"Bekannte Klassen: {known}"
            )
        
        share.common.classdef = cdef
        inst = share.common.Instance(class_name = share.common.classdef.name)
        parent_inst = args[0] if args else None
        if isinstance(parent_inst, share.common.Instance):
            inst.parent = parent_inst
        parent_backend = parent_inst.backend if isinstance(parent_inst, share.common.Instance) else None
        
        # base backend (FORM etc.)
        if share.common.classdef.parent:
            inst.backend = create_backend_for_base(share.common.classdef.parent, parent_backend)
        
        # defaults apply
        #for k,v in getattr(share.common.classdef, "default_props", {}).items():
        #    set_prop_runtime(inst, k, v)
        for k, v in share.common.classdef.default_props.items():
            self.set_prop(inst, k, v)
        
        # execute class body with THIS = inst
        self.push_this(inst)
        self.push_scope()
        try:
            self._scopes[-1]["THIS"] = inst
            self._scopes[-1]["SELF"] = inst
            self.exec_class_body(share.common.classdef)
            self._ensure_declared_children_from_source(inst)
        finally:
            self.pop_scope()
            self.pop_this()
        
        if self.resolve_method_silent(share.common.classdef.name, "INIT") is not None:
            self.invoke_method(inst, "INIT", args, None)
        
        return inst

    def set_prop(self, inst: share.common.Instance, name: str, value: Any, ctx=None):
        key = name.upper()
        
        # 1) normal speichern
        inst.props[key] = value

        # 1a) Objekt-Kinder automatisch binden, damit THIS.PushButton1,
        #     THIS.Container1.PushButton1 usw. sowohl über props als auch
        #     über children zuverlässig auflösbar bleiben.
        if isinstance(value, share.common.Instance) and key != "PARENT":
            try:
                self.bind_child(inst, key, value)
            except Exception:
                # Fallback: wenigstens Runtime-Referenz sichern
                inst.children[key] = value

        # MENU/POPUPMENU: Text => Menü-Titel
        if inst.class_name.upper() in ("MENU", "POPUPMENU") and key in ("TEXT", "CAPTION", "TITLE"):
            try:
                if hasattr(inst.backend, "setTitle"):
                    inst.backend.setTitle(str(value))
                elif hasattr(inst.backend, "setWindowTitle"):
                    inst.backend.setWindowTitle(str(value))
            except Exception:
                pass
            return

        # MENU/POPUPMENU: SubMenu anhängen (THIS.MenuDatei.SubMenu = NEW MENU(...))
        if inst.class_name.upper() in ("MENU", "POPUPMENU") and key == "SUBMENU":
            if isinstance(value, share.common.Instance) and value.backend is not None:
                # Falls der SubMenu noch keinen Parent hat: automatisch hier einhängen
                try:
                    self._attach_menu(value, inst)
                except Exception:
                    try:
                        if hasattr(inst.backend, "addMenu"):
                            inst.backend.addMenu(value.backend)
                    except Exception:
                        pass
            return


        # 1b) Reparenting: `obj.parent = otherObj` (or `obj.parent = null`)

        if key == "PARENT":
            new_parent = value if isinstance(value, share.common.Instance) else None

            # MENU/POPUPMENU: nicht QWidget-reparenting, sondern im Menübaum umhängen
            if inst.class_name.upper() in ("MENU", "POPUPMENU"):
                inst.parent = new_parent
                inst.props[key] = new_parent
                try:
                    self._attach_menu(inst, new_parent)
                except Exception:
                    pass
                return

            # normale Widgets
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
    
    def _ensure_event_filter(self, inst: share.common.Instance, ctx=None):
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
            f = MyQtEventFilter(self, inst)
            inst.props["_QT_EVENT_FILTER"] = f
            inst.backend.installEventFilter(f)

    def _bind_onkeydown(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, share.common.Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onKeyDown erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, share.common.ProgramAbortSignal):
                return None

        inst.props["_ONKEYDOWN_WRAPPER"] = wrapper

    def _bind_onkeyup(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, share.common.Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onKeyUp erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, share.common.ProgramAbortSignal):
                return None

        inst.props["_ONKEYUP_WRAPPER"] = wrapper

    def _bind_ondblclick(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        if not isinstance(handler, share.common.Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onDblClick erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, share.common.ProgramAbortSignal):
                return None

        inst.props["_ONDBLCLICK_WRAPPER"] = wrapper
        
    def _bind_onclick(self, inst: share.common.Instance, handler: Any, ctx=None):
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
            if not isinstance(h, share.common.Delegate):
                raise RuntimeError(
                    f"{self.loc(ctx)}: onClick erwartet Methode(n) (Delegate), bekam {type(h).__name__}"
                )
        
        def wrapper(*qt_args):
            try:
                # nacheinander ausführen
                for h in handlers:
                    try:
                        self.invoke_method(h.target, h.method_name, [inst], None)
                    except (ReturnSignal, share.common.ProgramAbortSignal):
                        # Return aus Handler ignorieren -> weiter zum nächsten
                        pass
            except (ReturnSignal, share.common.ProgramAbortSignal):
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
        
    def _bind_onmousedown(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # nur für Buttons (erstmal)
        if not hasattr(inst.backend, "pressed"):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseDown nicht unterstützt für {inst.class_name}")
        
        # Handler muss Delegate sein (oder notfalls BoundMethod)
        if not isinstance(handler, share.common.Delegate):
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
            except (ReturnSignal, share.common.ProgramAbortSignal):
                # click-handler ignoriert return meistens
                return None
        
        inst.props["_ONMOUSEDOWN_WRAPPER"] = wrapper
        inst.backend.pressed.connect(wrapper)
    
    def _bind_onmouseup(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return
        
        # nur für Buttons (erstmal)
        if not hasattr(inst.backend, "released"):
            raise RuntimeError(f"{self.loc(ctx)}: onMouseUp nicht unterstützt für {inst.class_name}")
        
        # Handler muss Delegate sein (oder notfalls BoundMethod)
        if not isinstance(handler, share.common.Delegate):
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
            except (ReturnSignal, share.common.ProgramAbortSignal):
                # click-handler ignoriert return meistens
                return None
        
        inst.props["_ONMOUSEUP_WRAPPER"] = wrapper
        inst.backend.released.connect(wrapper)

    def _bind_onmousemove(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, share.common.Delegate):
            raise RuntimeError(
                f"{self.loc(ctx)}: onMouseMove erwartet eine Methode (Delegate), bekam {type(handler).__name__}"
            )

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                # Minimal: nur Sender
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, share.common.ProgramAbortSignal):
                return None

        inst.props["_ONMOUSEMOVE_WRAPPER"] = wrapper

    def _bind_ongotfocus(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, share.common.Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onGotFocus erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, share.common.ProgramAbortSignal):
                return None

        inst.props["_ONFOCUSIN_WRAPPER"] = wrapper

    def _bind_onlostfocus(self, inst: share.common.Instance, handler: Any, ctx=None):
        if inst.backend is None:
            return

        if not isinstance(handler, share.common.Delegate):
            raise RuntimeError(f"{self.loc(ctx)}: onLostFocus erwartet eine Methode (Delegate), bekam {type(handler).__name__}")

        self._ensure_event_filter(inst, ctx)

        def wrapper(qt_event=None):
            try:
                return self.invoke_method(handler.target, handler.method_name, [inst], None)
            except (ReturnSignal, share.common.ProgramAbortSignal):
                return None

        inst.props["_ONFOCUSOUT_WRAPPER"] = wrapper
    
    def exec_class_body(self, cdef: share.common.ClassDef):
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
    def _eval_property_default(self, expr_ctx, this_obj: share.common.Instance):
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
    
    def _eval_input_text(self, raw_text: str):
        text = (raw_text or "").strip()
        if text == "":
            return ""

        upper = text.upper()
        if upper in ("T", ".T.", "Y", ".Y."):
            return True
        if upper in ("F", ".F.", "N", ".N."):
            return False

        source   = InputStream(text)
        lexer    = dBaseLexer(source)
        tokens   = CommonTokenStream(lexer)
        tokens.fill()
        parser   = dBaseParser(tokens)
        listener = _attach_silent_antlr_errors(lexer, parser)
        tree     = parser.expr()

        if parser.getNumberOfSyntaxErrors() > 0:
            msg = listener.messages[0] if listener.messages else "Ungültiger Ausdruck"
            raise RuntimeError(msg)
        if tokens.LA(1) != Token.EOF:
            raise RuntimeError("Ungültiger Ausdruck")

        return self.visit(tree)

    def _assign_input_target(self, target_name: str, value):
        target_name = str(target_name or "").strip()
        if not target_name:
            raise RuntimeError("INPUT: Missing target variable name")

        parts = [p.strip() for p in target_name.split('.') if p.strip()]
        if not parts:
            raise RuntimeError("INPUT: Missing target variable name")

        if len(parts) == 1:
            self._set_name(parts[0], value, None)
            return

        self._set_chain_parts(parts, value, None)

    def _builtin_INPUT(self, prompt_expr="", target_name=""):
        prompt_text = "" if prompt_expr is None else str(prompt_expr)
        target_name = str(target_name or "").strip()
        if not target_name:
            raise RuntimeError("INPUT: Missing target variable name")

        parent = share.common.MAINAPP if "MAINAPP" in globals() else None

        while True:
            raw_text, rc = InputValueDialog.get_value(prompt=prompt_text, parent=parent)
            self.set_var("INPUT_RC", int(rc))
            self.set_var("_INPUT_RC", int(rc))

            if int(rc) == 0:
                self._assign_input_target(target_name, "")
                return 0

            try:
                value = self._eval_input_text(raw_text)
            except Exception as e:
                QMessageBox.warning(
                    parent,
                    "Ungültige Eingabe",
                    str(e)
                )
                continue

            self._assign_input_target(target_name, value)
            return 1

    # ---------- Statements ----------
    def _precollect_classes_from_source(self):
        text = getattr(self, "_pre_source", "") or ""
        if not text:
            return

        rx = re.compile(r'^\s*CLASS\s+(?P<name>[A-Za-z_]\w*)(?:\s+OF\s+(?P<parent>[A-Za-z_]\w*))?\b', re.IGNORECASE | re.MULTILINE)
        for m in rx.finditer(text):
            cname = m.group('name').upper()
            parent = m.group('parent').upper() if m.group('parent') else None
            cdef = self.classes.get(cname)
            if cdef is None or not isinstance(cdef, share.common.ClassDef):
                self.classes[cname] = share.common.ClassDef(name=cname, parent=parent)
            else:
                if parent and not cdef.parent:
                    cdef.parent = parent

    def _get_class_line_ranges(self):
        if self._class_line_ranges is not None:
            return self._class_line_ranges

        text = getattr(self, "_pre_source", "") or ""
        ranges = []
        stack = []

        for lineno, raw in enumerate(text.splitlines(), start=1):
            line = raw.strip()
            if re.match(r"^CLASS\b", line, re.IGNORECASE):
                stack.append(lineno)
                continue
            if re.match(r"^ENDCLASS\b", line, re.IGNORECASE):
                if stack:
                    start = stack.pop()
                    ranges.append((start, lineno))

        self._class_line_ranges = ranges
        return ranges


    def _eval_expr_text_from_source(self, expr_text: str):
        txt = (expr_text or "").strip()
        if not txt:
            return None
        try:
            sub_source = InputStream(txt)
            sub_lexer = dBaseLexer(sub_source)
            sub_tokens = CommonTokenStream(sub_lexer)
            sub_tokens.fill()
            sub_parser = dBaseParser(sub_tokens)
            _attach_silent_antlr_errors(sub_lexer, sub_parser)
            if hasattr(sub_parser, "expr"):
                ectx = sub_parser.expr()
                return self.visit(ectx)
        except Exception:
            pass

        u = txt.upper()
        if u in (".T.", "TRUE"):
            return True
        if u in (".F.", "FALSE"):
            return False
        if (txt.startswith('"') and txt.endswith('"')) or (txt.startswith("'") and txt.endswith("'")):
            try:
                return self._unescape_string(txt)
            except Exception:
                return txt[1:-1]
        try:
            if "." in txt:
                return float(txt)
            return int(txt)
        except Exception:
            return txt

    def _parse_statements_from_source(self, source_text: str):
        txt = source_text or ""
        if not txt.strip():
            return []
        try:
            if not txt.endswith("\n"):
                txt += "\n"
            sub_source = InputStream(txt)
            sub_lexer = dBaseLexer(sub_source)
            sub_tokens = CommonTokenStream(sub_lexer)
            sub_tokens.fill()
            sub_parser = dBaseParser(sub_tokens)
            _attach_silent_antlr_errors(sub_lexer, sub_parser)
            sub_tree = sub_parser.input_()
            out = []
            items = []
            try:
                items = sub_tree.item() or []
            except Exception:
                items = []
            if not isinstance(items, list):
                items = [items]
            for it in items:
                if it is None:
                    continue
                try:
                    st = it.statement()
                except Exception:
                    st = None
                if st is not None:
                    out.append(st)
            return out
        except Exception:
            return []

    def _hydrate_class_from_source(self, class_name: str):
        source = getattr(self, "_pre_source", "") or ""
        cname = (class_name or "").strip().upper()
        if not source or not cname:
            return

        class_pat = re.compile(
            rf'(?ims)^\s*CLASS\s+{re.escape(cname)}\b(?:\s+OF\s+(?P<parent>[A-Za-z_]\w*))?(?P<body>.*?)^\s*ENDCLASS\b'
        )
        m_class = class_pat.search(source)
        if not m_class:
            return

        parent_name = m_class.group('parent').upper() if m_class.group('parent') else None
        class_body = m_class.group('body') or ''

        cdef = self.classes.get(cname)
        if cdef is None or not isinstance(cdef, share.common.ClassDef):
            cdef = share.common.ClassDef(name=cname, parent=parent_name)
            self.classes[cname] = cdef
        else:
            cdef.name = cname
            cdef.parent = parent_name

        cdef.methods = {}
        cdef.default_props = {}
        cdef.inits = []

        pre_method = re.split(r'(?im)^\s*METHOD\b', class_body, maxsplit=1)[0]

        prop_rx = re.compile(r'(?im)^\s*PROPERTY\s+(?P<name>[A-Za-z_]\w*)\s*=\s*(?P<expr>.+?)\s*$')
        for pm in prop_rx.finditer(pre_method):
            pname = pm.group('name').upper()
            pexpr = pm.group('expr')
            cdef.default_props[pname] = self._eval_expr_text_from_source(pexpr)

        init_stmts = self._parse_statements_from_source(pre_method)
        if init_stmts:
            cdef.inits.extend(init_stmts)

        method_rx = re.compile(
            r'(?ims)^\s*METHOD\s+(?P<name>[A-Za-z_]\w*)\b\s*\((?P<params>.*?)\)\s*(?P<body>.*?)^\s*ENDMETHOD\b'
        )
        for mm in method_rx.finditer(class_body):
            mname = mm.group('name').upper()
            snippet = mm.group(0)
            try:
                if not snippet.endswith("\n"):
                    snippet += "\n"
                sub_source = InputStream(snippet)
                sub_lexer = dBaseLexer(sub_source)
                sub_tokens = CommonTokenStream(sub_lexer)
                sub_tokens.fill()
                sub_parser = dBaseParser(sub_tokens)
                _attach_silent_antlr_errors(sub_lexer, sub_parser)
                if hasattr(sub_parser, 'methodDecl'):
                    mctx = sub_parser.methodDecl()
                    if mctx is not None:
                        cdef.methods[mname] = mctx
                        continue
            except Exception:
                pass
            found = self._find_method_decl_in_source(cname, mname)
            if found is not None:
                cdef.methods[mname] = found

        self.classes[cname] = cdef

    def _hydrate_all_classes_from_source(self):
        text = getattr(self, "_pre_source", "") or ""
        if not text:
            return
        rx = re.compile(r'^\s*CLASS\s+(?P<name>[A-Za-z_]\w*)\b', re.IGNORECASE | re.MULTILINE)
        seen = set()
        for m in rx.finditer(text):
            cname = m.group('name').upper()
            if cname in seen:
                continue
            seen.add(cname)
            self._hydrate_class_from_source(cname)

    def _is_line_inside_class_block(self, lineno: int) -> bool:
        if not lineno:
            return False
        for start, stop in self._get_class_line_ranges():
            if start <= lineno <= stop:
                return True
        return False

    def _collect_all_classdecls(self, node, seen=None):
        if node is None:
            return
        if seen is None:
            seen = set()
        try:
            nid = id(node)
            if nid in seen:
                return
            seen.add(nid)
        except Exception:
            pass

        tname = type(node).__name__
        if tname.endswith("ClassDeclContext"):
            self.visitClassDecl(node)
            return

        if hasattr(node, "classDecl"):
            try:
                cd = node.classDecl()
            except TypeError:
                cd = None
            if cd is not None:
                if isinstance(cd, list):
                    for it in cd:
                        if it is not None:
                            self.visitClassDecl(it)
                else:
                    self.visitClassDecl(cd)

        children = getattr(node, "children", None)
        if children:
            for ch in children:
                self._collect_all_classdecls(ch, seen)

    def visitInput(self, ctx):
        # Pass 1: Klassen + top-level Methoden registrieren
        if self._mode == "collect":
            self._precollect_classes_from_source()
            self._collect_all_classdecls(ctx)
            self._hydrate_all_classes_from_source()
            for it in ctx.item():
                try:
                    mctx = it.methodDecl()
                except Exception:
                    mctx = None
                if mctx is not None:
                    self.visit(mctx)
            return None

        # Pass 2: nur echte Top-Level-Statements ausführen.
        # Parser-Recovery kann Anweisungen aus CLASS...ENDCLASS-Blöcken als
        # scheinbare Top-Level-Statements durchreichen; die dürfen hier nicht
        # laufen, weil z.B. WITH(THIS) nur beim Instanziieren gültig ist.
        for it in ctx.item():
            if it.statement():
                st = it.statement()
                if hasattr(st, "classDecl") and st.classDecl() is not None:
                    continue
                try:
                    st_line = getattr(getattr(st, "start", None), "line", 0) or 0
                except Exception:
                    st_line = 0
                if self._is_line_inside_class_block(st_line):
                    continue
                self.visit(st)

        return None

    def visitCallStmt(self, ctx):
        # callee irgendwie holen – z.B.:
        callee = self.visit(ctx.memberExpr())   # je nach Grammar: memberExpr/MemberExpr/etc.

        args = []
        if hasattr(ctx, "argList") and ctx.argList() is not None:
            args = [self.visit(e) for e in ctx.argList().expr()]

        # Delegate kann man "aufrufen", indem man die Methode im DSL ausführt
        if isinstance(callee, share.common.Delegate):
            return self.invoke_method(callee.target, callee.method_name, args, ctx)

        # normale Python-Funktionen
        if not callable(callee):
            raise RuntimeError(f"{ctx.start.line}:{ctx.start.column}: Ausdruck ist nicht aufrufbar: {ctx.getText()}")

        return callee(*args)
            
    def visitDoWhileStatement(self, ctx):
        #_debug_print("DEBUG: enter DO WHILE")
        guard = 0
        while True:
            cond = self.visit(ctx.condition())
            #_debug_print("DEBUG: condition =", cond)
            
            if not cond:
                #_debug_print("DEBUG: leave DO WHILE (cond false)")
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
        if not isinstance(obj, share.common.Instance):
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

        if not isinstance(this_obj, share.common.Instance):
            raise RuntimeError(f"{self.loc(ctx)}: PROPERTY nur innerhalb einer Instanz gültig")

        pname = ctx.IDENT().getText().upper()
        pval  = self.visit(ctx.expr()) if ctx.expr() else None

        this_obj.props[pname] = pval
        return None
    
    def _handle_property_decl(self, pctx, cdef: share.common.ClassDef):
        # pctx ist propertyDeclContext
        pname = pctx.IDENT().getText().upper()
        pval  = self.visit(pctx.expr())   # Expression auswerten
        cdef.default_props[pname] = pval

    def _walk_tree_nodes(self, node, seen=None):
        if node is None:
            return
        if seen is None:
            seen = set()
        try:
            nid = id(node)
            if nid in seen:
                return
            seen.add(nid)
        except Exception:
            pass
        yield node
        children = getattr(node, 'children', None)
        if children:
            for ch in children:
                yield from self._walk_tree_nodes(ch, seen)

    def _collect_methods_from_node(self, node, cdef: share.common.ClassDef):
        changed = False
        for sub in self._walk_tree_nodes(node):
            tname = type(sub).__name__
            mctx = None
            if tname.endswith('MethodDeclContext'):
                mctx = sub
            elif hasattr(sub, 'methodDecl'):
                try:
                    tmp = sub.methodDecl()
                except TypeError:
                    tmp = None
                if isinstance(tmp, list):
                    for one in tmp:
                        if one is None:
                            continue
                        mname = self._method_name(one).upper()
                        cdef.methods[mname] = one
                        changed = True
                    continue
                mctx = tmp
            if mctx is not None:
                mname = self._method_name(mctx).upper()
                cdef.methods[mname] = mctx
                changed = True
        return changed

    def _find_method_decl_in_tree(self, class_name: str, method_name: str):
        tree = getattr(self, '_parse_tree', None)
        if tree is None:
            return None

        cname = (class_name or '').upper()
        mname = (method_name or '').upper()

        for node in self._walk_tree_nodes(tree):
            if not type(node).__name__.endswith('ClassDeclContext'):
                continue
            try:
                node_cname = node.name.text.upper()
            except Exception:
                continue
            if node_cname != cname:
                continue

            for sub in self._walk_tree_nodes(node):
                if not type(sub).__name__.endswith('MethodDeclContext'):
                    continue
                try:
                    if self._method_name(sub).upper() == mname:
                        return sub
                except Exception:
                    pass
        return None

    def _find_method_decl_in_source(self, class_name: str, method_name: str):
        source = getattr(self, '_pre_source', None)
        if not source:
            return None

        cname = (class_name or '').strip()
        mname = (method_name or '').strip()
        if not cname or not mname:
            return None

        try:
            class_pat = re.compile(
                rf'(?is)\bCLASS\s+{re.escape(cname)}\b(?:\s+OF\s+[A-Za-z_]\w*)?(?P<body>.*?)\bENDCLASS\b'
            )
            m_class = class_pat.search(source)
            if not m_class:
                return None

            class_body = m_class.group('body') or ''
            method_pat = re.compile(
                rf'(?is)\bMETHOD\s+{re.escape(mname)}\b\s*\((?P<params>.*?)\)\s*(?P<body>.*?)\bENDMETHOD\b'
            )
            m_method = method_pat.search(class_body)
            if not m_method:
                return None

            params = (m_method.group('params') or '').strip()
            body = (m_method.group('body') or '').strip()
            snippet = f"METHOD {mname}({params})\n{body}\nENDMETHOD\n"

            sub_source = InputStream(snippet)
            sub_lexer = dBaseLexer(sub_source)
            sub_tokens = CommonTokenStream(sub_lexer)
            sub_parser = dBaseParser(sub_tokens)

            if hasattr(sub_parser, 'methodDecl'):
                mctx = sub_parser.methodDecl()
                return mctx
        except Exception:
            return None

        return None

    def _ensure_declared_children_from_source(self, inst: share.common.Instance):
        source = getattr(self, "_pre_source", None)
        if not source or not isinstance(inst, share.common.Instance):
            return

        cname = (getattr(inst, "class_name", "") or "").strip()
        if not cname:
            return

        try:
            class_pat = re.compile(
                rf'(?is)\bCLASS\s+{re.escape(cname)}\b(?:\s+OF\s+[A-Za-z_]\w*)?(?P<body>.*?)\bENDCLASS\b'
            )
            m_class = class_pat.search(source)
            if not m_class:
                return

            class_body = m_class.group('body') or ''
            pre_method = re.split(r'(?im)^\s*METHOD\b', class_body, maxsplit=1)[0]

            # 1) direkte Kinder: THIS.PushButton1 = NEW PUSHBUTTON(THIS)
            rx_direct = re.compile(
                r'(?im)^\s*THIS\.(?P<name>[A-Za-z_]\w*)\s*=\s*NEW\s+(?P<klass>[A-Za-z_]\w*)\s*\(\s*THIS\s*\)\s*$'
            )
            for m in rx_direct.finditer(pre_method):
                key = m.group('name').upper()
                if key in inst.props or key in inst.children:
                    continue
                child_class = m.group('klass').upper()
                try:
                    child = self.new_instance(child_class, [inst])
                    self.bind_child(inst, key, child)
                except Exception:
                    pass

            # 2) ein Level verschachtelt: THIS.Container1.PushButton1 = NEW PUSHBUTTON(THIS.Container1)
            rx_nested = re.compile(
                r'(?im)^\s*THIS\.(?P<owner>[A-Za-z_]\w*)\.(?P<name>[A-Za-z_]\w*)\s*=\s*NEW\s+(?P<klass>[A-Za-z_]\w*)\s*\(\s*THIS\.(?P=owner)\s*\)\s*$'
            )
            for m in rx_nested.finditer(pre_method):
                owner_key = m.group('owner').upper()
                child_key = m.group('name').upper()
                owner_obj = inst.props.get(owner_key) or inst.children.get(owner_key)
                if not isinstance(owner_obj, share.common.Instance):
                    continue
                if child_key in owner_obj.props or child_key in owner_obj.children:
                    continue
                child_class = m.group('klass').upper()
                try:
                    child = self.new_instance(child_class, [owner_obj])
                    self.bind_child(owner_obj, child_key, child)
                except Exception:
                    pass
        except Exception:
            return

    def _ensure_class_methods_loaded(self, class_name: str):
        c = (class_name or '').upper()
        cdef = self.classes.get(c)
        if not isinstance(cdef, share.common.ClassDef):
            return

        # Nicht nur bei komplett leeren Methodenlisten laden.
        # In einigen Tree-Formen werden einzelne Methoden (z.B. INIT)
        # beim ersten Collect übersehen, obwohl andere Methoden schon
        # vorhanden sind. Deshalb immer noch einmal robust über body/decl
        # nachladen; das Dict verhindert Dubletten automatisch.
        body = getattr(cdef, 'body_ctx', None)
        decl = getattr(cdef, 'decl_ctx', None)
        if body is not None:
            self._collect_methods_from_node(body, cdef)
        if decl is not None:
            self._collect_methods_from_node(decl, cdef)
        self.classes[c] = cdef
        
    def visitClassDecl(self, ctx):
        if getattr(self, "_mode", "") != "collect":
            return None
        
        class_name  = ctx.name.text.upper()
        parent_name = ctx.parent.text.upper() if ctx.parent else None
        
        cdef = self.classes.get(class_name)
        if cdef is None or not isinstance(cdef, share.common.ClassDef):
            cdef = share.common.ClassDef(name=class_name.upper(), parent=parent_name)
            self.classes[class_name] = cdef
        else:
            cdef.name = class_name.upper()
            cdef.parent = parent_name
            # beim erneuten Collect nicht anhäufen
            cdef.methods = {}
            cdef.default_props = {}
            cdef.inits = []

        body = ctx.classBody()
        cdef.body_ctx = body
        cdef.decl_ctx = ctx

        # 1) echte classMember zuverlässig einsammeln
        members = []
        try:
            members = body.classMember() or []
        except Exception:
            members = []
        if not isinstance(members, list):
            members = [members]

        for ch in members:
            if ch is None:
                continue
            if hasattr(ch, "propertyDecl") and ch.propertyDecl() is not None:
                self._handle_property_decl(ch.propertyDecl(), cdef)
                continue
            if hasattr(ch, "methodDecl") and ch.methodDecl() is not None:
                mctx = ch.methodDecl()
                mname = self._method_name(mctx).upper()
                cdef.methods[mname] = mctx
                continue
            if hasattr(ch, "assignStmt") and ch.assignStmt() is not None:
                cdef.inits.append(ch.assignStmt())
                continue
            if hasattr(ch, "withStmt") and ch.withStmt() is not None:
                cdef.inits.append(ch.withStmt())
                continue

        # 2) zusätzliche normale statements im Klassenrumpf (z.B. WRITE ...)
        stmts = []
        try:
            stmts = body.statement() or []
        except Exception:
            stmts = []
        if not isinstance(stmts, list):
            stmts = [stmts]
        for st in stmts:
            if st is not None:
                cdef.inits.append(st)

        # 3) Zusätzlicher robuster Scan des gesamten Klassenknotens.
        #    Wichtig: methodDecl kann je nach Tree-Form nicht immer sauber in
        #    body.classMember() auftauchen. Darum Methoden immer zusätzlich
        #    rekursiv einsammeln; Properties/Inits nur ergänzend.
        self._collect_methods_from_node(body, cdef)

        seen_init_ids = {id(x) for x in cdef.inits}
        for ch in list(getattr(body, "children", []) or []):
            tname = type(ch).__name__
            if hasattr(ch, "propertyDecl") and ch.propertyDecl():
                self._handle_property_decl(ch.propertyDecl(), cdef)
            elif hasattr(ch, "assignStmt") and ch.assignStmt():
                sub = ch.assignStmt()
                if id(sub) not in seen_init_ids:
                    cdef.inits.append(sub)
                    seen_init_ids.add(id(sub))
            elif hasattr(ch, "withStmt") and ch.withStmt():
                sub = ch.withStmt()
                if id(sub) not in seen_init_ids:
                    cdef.inits.append(sub)
                    seen_init_ids.add(id(sub))
            elif tname.endswith("StatementContext"):
                if id(ch) not in seen_init_ids:
                    cdef.inits.append(ch)
                    seen_init_ids.add(id(ch))

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

        body = ctx.block()
        self.methods[method_name] = share.common.MethodDef(params=params, block_ctx=body)
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
            if isinstance(this_obj, share.common.Instance):
                key = parts[1].upper()
                if self.resolve_method_silent(this_obj.class_name.upper(), key) is not None:
                    return share.common.Delegate(target=this_obj, method_name=key, runner=self)

        return self.get_chain(parts, ctx)

    
    def visitPostfixExpr(self, ctx):
        # Basis auswerten
        cur = self.visit(ctx.primary())
        expr_list = []
        #_debug_print("===> ", cur)
        # Alle argLists einsammeln (für jeden '(' ... ')'-Call)
        arglists = ctx.argList() or []
        if not isinstance(arglists, list):
            arglists = [arglists]
        call_i = 0
        #_debug_print("--> ", ctx.argList())
        
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
                    if isinstance(cur, share.common.Delegate):
                        cur = self.invoke_method(cur.target, cur.method_name, args, ctx)
                    elif isinstance(cur, share.common.BoundMethod):
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

                    if isinstance(cur, share.common.Instance):
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
            if name.upper() == "FONT" and isinstance(cur, share.common.Instance):
                font_container = cur

            cur = self.get_member(cur, name, ctx)

        last = parts[-1]  # NICHT uppern, set_member macht eh upper intern (oder du machst's dort)

        # 1) normales Instance-Property setzen (Sender.Text = ..., Sender.Font = NEW FONT(...))
        if isinstance(cur, share.common.Instance):
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
        # Im Collect-Pass nichts ausführen/ausgeben, sonst doppelte Ausgabe
        if getattr(self, "_mode", "exec") != "exec":
            return None

        parts = [self.eval_writeArg(a) for a in ctx.writeArg()]
        _emit_runtime_output_line("".join(parts))
        return None

    def eval_writeArg(self, arg_ctx):
        if arg_ctx.STRING():
            s = arg_ctx.STRING().getText()
            return s[1:-1]

        if arg_ctx.dottedRef():
            val = self.visit(arg_ctx.dottedRef())
            return "" if val is None else self._format_value(val)

        if arg_ctx.expr():
            val = self.visit(arg_ctx.expr())
            return "" if val is None else self._format_value(val)

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
        if isinstance(val, share.common.Instance):
            return repr(val)
        if isinstance(val, share.common.Delegate):
            return repr(val)
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
        # Parser-Recovery kann Teile eines CLASS-Headers als nackte exprStmt liefern
        # (z.B. "ParentForm" oder native Basen wie "FORM"). Diese sollen im
        # Exec-Pass keine Laufzeitwirkung haben.
        try:
            pe = ctx.postfixExpr()
            txt = pe.getText() if pe is not None else ""
            up = txt.upper()
            if up in self.classes or up in NATIVE_BASES:
                return None
        except Exception:
            pass

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
            if isinstance(base, share.common.Instance):
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

        # 3) Aktiver Arbeitsbereich: EOF / Feldnamen
        try:
            ws = self._current_workarea()
            if key == 'EOF':
                return bool(ws.get('eof', True))
            if key == 'RECNO':
                return int(ws.get('pointer', 1) or 1)

            rec = self._current_record()
            if rec is not None:
                if key == 'DELETED':
                    return bool(rec.get('__deleted__'))
                if key in rec:
                    return rec[key]

            # Feldnamen auch dann erkennen, wenn aktuell kein gültiger Datensatz
            # im Zugriff ist (z.B. EOF/leer/pointer außerhalb). In diesem Fall
            # liefern wir einen leeren Wert statt "Unbekannter Name".
            fields = list(ws.get('fields', []) or [])
            for spec in fields:
                try:
                    if str(getattr(spec, 'name', '') or '').upper() == key:
                        return '' if rec is None else rec.get(key, '')
                except Exception:
                    continue
        except Exception:
            pass

        # 4) Klassenname oder native Basisklasse als Symbol tolerieren.
        # Das verhindert, dass versehentlich im Exec-Pass ankommende Teile eines
        # CLASS-Headers (z.B. "ParentForm" oder "FORM") als unbekannter
        # Variablenname abstürzen. Für NEW <Class>(...) wird dieser Pfad nicht
        # benutzt, daher ist das hier nur ein harmloser Fallback.
        if key in self.classes:
            return key
        if key in NATIVE_BASES:
            return key

        # 4) nicht gefunden
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
            if isinstance(base, share.common.Instance):
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
        if isinstance(obj, share.common.FontValue) and self.with_stack and isinstance(self.with_stack[-1], share.common.Instance):
            owner = self.with_stack[-1]
        
        self.with_stack.append(obj)
        self.with_stack_owner.append(owner)
        try:
            self.visit(ctx.withBody())
        finally:
            self.with_stack_owner.pop()
            self.with_stack.pop()
        
        return None

    def set_child(self, owner: share.common.Instance, name: str, child: share.common.Instance):
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

        return share.common.MethodDef(params=params, block_ctx=block_ctx)

    def _get_method_params(self, method_ctx):
        if isinstance(method_ctx, share.common.MethodDef):
            return list(method_ctx.params or [])

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
                block_ctx = mctx.block_ctx if isinstance(mctx, share.common.MethodDef) else mctx.block()
                self.visit(block_ctx)
                return None
            except ReturnSignal as rs:
                return rs.value

        finally:
            self.pop_scope()
            self.pop_this()
        
    # für Events ... -> FireClick(button)
    def invoke_delegate(self, d: share.common.Delegate, args: list, ctx):
        res = self.resolve_method(d.target.class_name.upper(), d.method_name, ctx)
        owner_class, method_ctx = res
        return self.execute_method(owner_class, method_ctx, args, this_obj=d.target)

    def visitCondition(self, ctx):
        return self.visit(ctx.logicalOr())

    def _strip_program_target(self, target: str) -> str:
        s = (target or "").strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()

    def _do_program_extensions(self) -> list[str]:
        return [".prg", ".wfm", ".frm"]

    def _iter_program_candidates(self, target: str):
        s = self._strip_program_target(target)
        if not s:
            return []
        if s.upper().startswith("PROGRAM "):
            s = s.split(None, 1)[1].strip()

        root, ext = os.path.splitext(s)
        names = [s] if ext else [s + ex for ex in self._do_program_extensions()]

        candidates = []
        cur = getattr(self, "_current_filename", "") or ""
        if cur:
            base_dir = os.path.dirname(os.path.abspath(cur))
            for name in names:
                candidates.append(os.path.join(base_dir, name))
        for name in names:
            candidates.append(os.path.abspath(name))
            candidates.append(os.path.join(os.getcwd(), name))

        seen = set()
        ordered = []
        for cand in candidates:
            full = os.path.abspath(cand)
            if full in seen:
                continue
            seen.add(full)
            ordered.append(full)
        return ordered

    def looks_like_program(self, target: str) -> bool:
        s = self._strip_program_target(target)
        if not s:
            return False
        if s.upper().startswith("PROGRAM "):
            return True
        _root, ext = os.path.splitext(s)
        if ext:
            return ext.lower() in tuple(self._do_program_extensions())
        # DO test: Datei zuerst versuchen
        for cand in self._iter_program_candidates(target):
            if os.path.exists(cand):
                return True
        # expliziter Pfad/quoted path ohne Extension -> ebenfalls dateiartig behandeln
        return any(sep in s for sep in ("/", "\\"))

    def try_resolve_program_path(self, target: str) -> str | None:
        for cand in self._iter_program_candidates(target):
            if os.path.exists(cand):
                return cand
        return None

    def resolve_program_path(self, target: str, ctx=None) -> str:
        path = self.try_resolve_program_path(target)
        if path:
            return path
        s = self._strip_program_target(target)
        if s.upper().startswith("PROGRAM "):
            s = s.split(None, 1)[1].strip()
        where = self.loc(ctx) if ctx is not None else "<unknown>"
        raise RuntimeError(f"{where}: DO-Datei '{s}' wurde nicht gefunden")

    def _parse_external_program(self, filename: str):
        pp = Preprocessor(include_paths=[Path("includes")])
        pre = pp.process(filename)
        if pre and not pre.endswith("\n"):
            pre += "\n"
        parser_input = _build_parser_input(pre)
        if parser_input and not parser_input.endswith("\n"):
            parser_input += "\n"
        source = InputStream(parser_input)
        lexer = dBaseLexer(source)
        tokens = CommonTokenStream(lexer)
        tokens.fill()
        parser = dBaseParser(tokens)
        listener = _attach_silent_antlr_errors(lexer, parser)
        tree = parser.input_()
        if parser.getNumberOfSyntaxErrors() > 0:
            msg = listener.messages[0] if listener.messages else "Syntaxfehler im Quelltext"
            raise RuntimeError(msg)
        return tree, pre

    def run_program(self, target: str, args: list[Any] | None = None):
        path = self.resolve_program_path(target)
        tree, pre = self._parse_external_program(path)

        old_mode = self._mode
        old_pre_source = getattr(self, "_pre_source", "")
        old_ranges = self._class_line_ranges
        old_file = getattr(self, "_current_filename", "")

        self.push_frame(os.path.basename(path), list(args or []))
        try:
            self._current_filename = path
            self._pre_source = pre
            self._class_line_ranges = None

            self._mode = "collect"
            self.visit(tree)

            self._mode = "exec"
            for it in tree.item():
                st = it.statement() if hasattr(it, "statement") else None
                if st is None:
                    continue
                if hasattr(st, "classDecl") and st.classDecl() is not None:
                    continue
                try:
                    st_line = getattr(getattr(st, "start", None), "line", 0) or 0
                except Exception:
                    st_line = 0
                if self._is_line_inside_class_block(st_line):
                    continue
                self.visit(st)
        finally:
            self.pop_frame()
            self._mode = old_mode
            self._pre_source = old_pre_source
            self._class_line_ranges = old_ranges
            self._current_filename = old_file

    def has_procedure(self, target: str) -> bool:
        name = self._strip_program_target(target).upper()
        return name in self.methods

    def call_procedure(self, target: str, args: list[Any] | None = None):
        name = self._strip_program_target(target).upper()
        mdef = self.methods.get(name)
        if mdef is None:
            raise RuntimeError(f"{self.loc(None)}: Prozedur/Methode '{name}' ist nicht definiert")

        self.push_frame(name, list(args or []))
        self.push_scope()
        try:
            params = self._get_method_params(mdef)
            for i, pname in enumerate(params):
                self.set_var(pname, args[i] if args and i < len(args) else None)
            try:
                block_ctx = mdef.block_ctx if isinstance(mdef, share.common.MethodDef) else mdef.block()
                self.visit(block_ctx)
                return None
            except ReturnSignal as rs:
                return rs.value
        finally:
            self.pop_scope()
            self.pop_frame()

    def _call_do_target_as_method(self, target: str, args: list[Any] | None, ctx=None):
        raw = self._strip_program_target(target)
        if not raw:
            return False, None

        expr = raw.strip()
        if expr.endswith('()'):
            expr = expr[:-2].strip()
        expr = re.sub(r'\s*::\s*', '.', expr)
        expr = re.sub(r'\s*\.\s*', '.', expr)
        parts = [p for p in expr.split('.') if p]
        if not parts:
            return False, None

        # Expliziter Methodenaufruf auf Objekt: THIS.testProcer / obj.method
        if len(parts) >= 2:
            try:
                owner = self.get_chain(parts[:-1], ctx)
            except Exception:
                owner = None
            if isinstance(owner, share.common.Instance):
                return True, self.invoke_method(owner, parts[-1], list(args or []), ctx)

        # Impliziter Methodenaufruf auf THIS: DO testProcer
        this_obj = None
        try:
            this_obj = self.this_obj or self.get_var("THIS", ctx)
        except Exception:
            this_obj = self.this_obj
        if isinstance(this_obj, share.common.Instance):
            mname = parts[-1].upper()
            if self.resolve_method_silent(this_obj.class_name.upper(), mname) is not None:
                return True, self.invoke_method(this_obj, mname, list(args or []), ctx)

        return False, None

    def visitDoStmt(self, ctx):
        target = ctx.doTarget().getText()
        args = []
        if ctx.argList():
            for e in ctx.argList().expr():
                args.append(self.eval_expr(e))

        # 1) Datei im Quellverzeichnis / Pfad / CWD suchen (.prg, .wfm, .frm)
        path = self.try_resolve_program_path(target)
        if path is not None:
            self.run_program(path, args)
            return None

        # 2) Objekt-/Instanzmethode: DO THIS.testProcer() / DO obj.method()
        handled, method_result = self._call_do_target_as_method(target, args, ctx)
        if handled:
            return method_result

        # 3) Falls keine Datei existiert: lokale/top-level METHOD aufrufen
        if self.has_procedure(target):
            return self.call_procedure(target, args)

        # 4) Explizite Dateiangabe mit Extension/Pfad soll einen klaren Fehler liefern
        if self.looks_like_program(target):
            self.run_program(target, args)
            return None

        # 5) Letzter Versuch: implizite Methode auf THIS auch dann noch probieren,
        #    wenn der Methodenaufruf keinen Rückgabewert liefert (None).
        handled, tried = self._call_do_target_as_method(target, args, ctx)
        if handled:
            return tried

        # 6) Sonst wie klassische Prozedur behandeln -> Fehlermeldung aus call_procedure
        return self.call_procedure(target, args)

    def visitDoCaseStmt(self, ctx):
        branches = ctx.doCaseBranch() or []
        if not isinstance(branches, list):
            branches = [branches]

        for br in branches:
            try:
                cond = self.visit(br.expr())
            except Exception:
                cond = False
            if bool(cond):
                self.visit(br.block())
                return None

        ob = ctx.doOtherwiseBranch()
        if ob is not None:
            self.visit(ob.block())
        return None

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
        if isinstance(handler, share.common.Delegate):
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

    def call_method(self, inst: share.common.Instance, name: str, args):
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

            block_ctx = mctx.block_ctx if isinstance(mctx, share.common.MethodDef) else mctx.block()
            self.visit(block_ctx)
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
                debug_print(share.locales.tr("file not found."))
                pass
        try:
            win = FileEditorWindow(parent = share.common.MAINAPP,
                initial_path = path,
                initial_text = text)
            win.resize(600, 500)
            sub = share.common.MAINAPP.mdi.addSubWindow(win)
            
            # 1) immer sichtbar + Vordergrund
            share.utildef.theme.apply_theme_global(win)
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
            debug_print(e)

def _emit_runtime_output_line(text: str):
    text  = "" if text is None else str(text)
    style = _get_runtime_current_color_style()

    # optional in-memory capture (used by one-liner console)
    try:
        if _RUNTIME_CAPTURE_STACK:
            bucket, forward = _RUNTIME_CAPTURE_STACK[-1]
            bucket.append(text)
            if not forward:
                return
    except Exception:
        pass

    # printer / PDF routing
    try:
        if _RUNTIME_OUTPUT_FORMAT.upper() == "PRINT" and bool(_RUNTIME_PRINT_ENABLED):
            _ensure_runtime_print_pdf_path()
            _RUNTIME_PRINT_LINES.append({
                "text": text,
                "style": _copy_runtime_color_style(style),
            })
            _render_runtime_output_pdf()
            return
    except Exception:
        pass

    # preferred sink: Debug Console in the main window
    try:
        mainapp = _resolve_runtime_mainapp()
        if mainapp is not None:
            mainapp.append_debug_output(text,
                fg_hex=style.get("fg_hex"),
                bg_hex=style.get("bg_hex"))
            return
    except Exception:
        pass

    # fallback when no UI is available
    try:
        debug_print(text)
    except Exception:
        pass


def _clear_runtime_output():
    try:
        mainapp = _resolve_runtime_mainapp()
        if mainapp is not None and hasattr(mainapp, "clear_debug_output"):
            mainapp.clear_debug_output()
            return
    except Exception:
        pass

@contextlib.contextmanager
def capture_runtime_output(forward: bool = False):
    bucket: list[str] = []
    entry = (bucket, bool(forward))
    _RUNTIME_CAPTURE_STACK.append(entry)
    try:
        yield bucket
    finally:
        try:
            if _RUNTIME_CAPTURE_STACK and _RUNTIME_CAPTURE_STACK[-1] is entry:
                _RUNTIME_CAPTURE_STACK.pop()
            else:
                _RUNTIME_CAPTURE_STACK.remove(entry)
        except Exception:
            pass

def _write_preprocessed_dump(filename: str, pre: str) -> Path:
    src_path = Path(filename).resolve()
    candidates = [
        src_path.with_name(src_path.stem + "_parse_input_dump.prg"),
        Path(app_dir()) / "parse_input_dump.prg",
        Path("parse_input_dump.prg").resolve(),
    ]
    txt = pre if pre.endswith("\n") else pre + "\n"
    for dump_path in candidates:
        try:
            dump_path.write_text(txt, encoding="utf-8")
            return dump_path
        except Exception:
            continue
    return candidates[-1]



def _write_parser_input_dump(filename: str, parser_input: str) -> Path:
    src_path = Path(filename).resolve()
    candidates = [
        src_path.with_name(src_path.stem + "_parser_input_dump.prg"),
        Path(app_dir()) / "parser_input_dump.prg",
        Path("parser_input_dump.prg").resolve(),
    ]
    txt = parser_input if parser_input.endswith("\n") else parser_input + "\n"
    for dump_path in candidates:
        try:
            dump_path.write_text(txt, encoding="utf-8")
            return dump_path
        except Exception:
            continue
    return candidates[-1]
def _split_line_ending(raw: str) -> tuple[str, str]:
    if raw.endswith("\r\n"):
        return raw[:-2], "\r\n"
    if raw.endswith("\n"):
        return raw[:-1], "\n"
    return raw, ""


def _blank_like_line(raw: str) -> str:
    _body, nl = _split_line_ending(raw)
    return nl


def _rewrite_do_this_for_parser(raw: str) -> str:
    body, nl = _split_line_ending(raw)
    m = re.match(
        r'^(?P<indent>\s*)DO\s+(?P<target>THIS(?:\s*(?:\.|::)\s*[A-Za-z_]\w*)+)(?P<call>\s*\((?P<args>.*)\))?\s*$',
        body,
        flags=re.IGNORECASE,
    )
    if not m:
        return raw
    indent = m.group('indent') or ''
    target = re.sub(r'\s*::\s*', '.', m.group('target') or '', flags=re.IGNORECASE)
    target = re.sub(r'\s*\.\s*', '.', target)
    call = m.group('call')
    if call:
        return f"{indent}{target}{call}{nl}"
    return f"{indent}{target}(){nl}"


def _build_parser_input(pre: str) -> str:
    lines = pre.splitlines(keepends=True)
    out: list[str] = []
    class_depth = 0

    for raw in lines:
        if class_depth > 0:
            if re.match(r'^\s*CLASS\b', raw, re.IGNORECASE):
                class_depth += 1
            if re.match(r'^\s*ENDCLASS\b', raw, re.IGNORECASE):
                class_depth = max(0, class_depth - 1)
            out.append(_blank_like_line(raw))
            continue

        if re.match(r'^\s*CLASS\b', raw, re.IGNORECASE):
            class_depth = 1
            out.append(_blank_like_line(raw))
            continue

        out.append(_rewrite_do_this_for_parser(raw))

    return ''.join(out)


def _format_parse_error_with_context(messages: list[str], pre: str, dump_path: Path) -> str:
    lines = pre.splitlines()
    out   = []
    msgs  = messages[:10] if messages else ["Syntaxfehler im Quelltext"]
    line_numbers = []

    for msg in msgs:
        out.append(msg)
        m = re.search(r'line\s+(\d+):(\d+)', msg)
        if m:
            try:
                line_numbers.append((int(m.group(1)), int(m.group(2))))
            except Exception:
                pass

    seen = set()
    for line_no, col in line_numbers[:3]:
        start = max(1, line_no - 2)
        end   = min(len(lines), line_no + 2)
        key   = (start, end)
        if key in seen:
            continue
        seen.add(key)

        out.append("")
        out.append(f"Kontext um Zeile {line_no}:{col}")
        for idx in range(start, end + 1):
            prefix = ">>" if idx == line_no else "  "
            txt = lines[idx - 1] if 0 <= idx - 1 < len(lines) else ""
            out.append(f"{prefix} {idx:4d}: {txt}")

    out.append("")
    out.append(f"Vorverarbeitete Quelle: {dump_path}")
    return "\n".join(out)


def _count_collect_entities(visitor: "ExecVisitor") -> tuple[int, int]:
    native = set(NATIVE_BASES.keys()) | {"OBJECT", "PUSHBUTTON"}

    class_count  = 0
    method_count = 0

    for cname, cdef in (getattr(visitor, "classes", {}) or {}).items():
        if str(cname).upper() in native:
            continue
        if isinstance(cdef, share.common.ClassDef):
            class_count += 1
            for _, mdef in (cdef.methods or {}).items():
                if isinstance(mdef, str):
                    continue
                method_count += 1

    for _, mdef in (getattr(visitor, "methods", {}) or {}).items():
        if isinstance(mdef, str):
            continue
        method_count += 1

    return class_count, method_count

def parse(filename: str, show_collect_dialog: bool = True):
    collect_dlg = None
    _runtime_output_session_begin(filename)

    # 0 pre-procession
    pp  = Preprocessor(include_paths=[Path("includes")])
    pre = pp.process(filename)
    if pre and not pre.endswith("\n"):
        pre += "\n"
    dump_path    = _write_preprocessed_dump(filename, pre)
    parser_input = _build_parser_input(pre)
    if parser_input and not parser_input.endswith("\n"):
        parser_input += "\n"
    parser_dump_path = _write_parser_input_dump(filename, parser_input)

    if show_collect_dialog and QApplication.instance() is not None:
        try:
            collect_dlg  = share.utildef.dialogs.CollectProgressDialog(
                parent   = share.common.MAINAPP if "MAINAPP" in globals() else None,
                filename = os.path.abspath(filename))
            share.utildef.theme.apply_theme_global(collect_dlg)
            collect_dlg.show()
            lines        = pre.splitlines()
            total_lines  = len(lines)
            collect_dlg.set_total_lines(total_lines)

            class_rx     = re.compile(r'^\s*CLASS\b' , re.IGNORECASE)
            method_rx    = re.compile(r'^\s*METHOD\b', re.IGNORECASE)
            class_count  = 0
            method_count = 0

            for idx, raw in enumerate(lines, start=1):
                if class_rx.search(raw):
                    class_count  += 1
                if method_rx.search(raw):
                    method_count += 1
                if not collect_dlg.update_progress(
                    line_no      = idx,
                    line_text    = raw,
                    class_count  = class_count,
                    method_count = method_count,
                    line_count   = idx,
                    status       = "Collect-Phase: Quelltext wird durchsucht …"
                ):
                    _runtime_output_session_end()
                    return None
        except Exception:
            collect_dlg = None

    source   = InputStream(parser_input)
    lexer    = dBaseLexer(source)
    tokens   = CommonTokenStream(lexer)
    tokens.fill()
    parser   = dBaseParser(tokens)
    listener = _attach_silent_antlr_errors(lexer, parser)

    tree = parser.input_()
    if parser.getNumberOfSyntaxErrors() > 0:
        if collect_dlg is not None:
            try:
                collect_dlg.close()
            except Exception:
                pass
        msg = _format_parse_error_with_context(
            getattr(listener, "messages", []) if listener is not None else [],
            parser_input,
            dump_path
        ) + f"\n\nParser-Eingabe: {parser_dump_path}"
        dlg = share.excepts.ErrorMessage(
            title    = share.locales.tr("Parser Error"),
            log_path = share.common.LOG,
            message  = msg,
            parent   = share.common.MAINAPP
        )
        dlg.exec_()
        _runtime_output_session_end()
        return None

    try:
        while True:
            tok = lexer.nextToken()
            if tok.type == Token.EOF:
                depth = getattr(lexer, "_cmtDepth", 0)
                if depth > 0:
                    line = lexer.line
                    col  = lexer.column
                    raise UnterminatedBlockCommentError(line, col)
                break
    except Exception as e:
        if collect_dlg is not None:
            try:
                collect_dlg.close()
            except Exception:
                pass
        dlg = share.excepts.ErrorMessage(
            title    = share.locales.tr("Lexer Error"),
            log_path = share.common.LOG,
            message  = f"{e}",
            parent   = share.common.MAINAPP
        )
        dlg.exec_()
        _runtime_output_session_end()
        return None

    global VISITOR
    VISITOR = ExecVisitor()
    VISITOR._current_filename  = os.path.abspath(filename)
    VISITOR._pre_source        = pre
    VISITOR._class_line_ranges = None
    VISITOR._parse_tree        = tree

    if collect_dlg is not None:
        collect_dlg.update_progress(
            line_no   =  0,
            line_text = "",
            status    = share.locales.tr("Collect-Phase: Klassen und Methoden werden eingesammelt …")
        )

    VISITOR._mode = "collect"
    VISITOR.visit(tree)

    if collect_dlg is not None:
        class_count, method_count = _count_collect_entities(VISITOR)
        collect_dlg.set_ready(
            class_count  = class_count,
            method_count = method_count,
            line_count   = len(pre.splitlines())
        )
        res = collect_dlg.exec_()
        if res != QDialog.Accepted or collect_dlg.cancel_requested:
            _runtime_output_session_end()
            return None

    VISITOR._mode = "exec"
    try:
        VISITOR.visit(tree)
    except share.common.ProgramAbortSignal:
        _runtime_output_session_end()
        return None

    _runtime_output_session_end()
    return tree
