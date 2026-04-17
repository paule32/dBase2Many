# ---------------------------------------------------------------------------
# \file  : editor.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from   __future__ import annotations

import share.common
from   share.common                  import *

from   share.editors.dbase.highlight import *
from   share.parsers.dbase.parser    import *

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

class CodeEditor(QPlainTextEdit):
    runRequested = pyqtSignal()
    hlpRequested = pyqtSignal()
    
    def __init__(self, main_window: "MainWindow", parent=None):
        super().__init__(parent)
        self.main_window = main_window
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

        self.setFocusPolicy(Qt.StrongFocus)
        self.setCenterOnScroll(False)
        self.viewport().installEventFilter(self)
        self._tab_spaces = "    "
        self._apply_tab_settings()

        # --- Run (F2) ---
        self.act_run = QAction("Run2", self)
        self.act_run.setShortcut(QKeySequence(Qt.Key_F2))
        self.act_run.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.act_run.triggered.connect(self._emit_run_requested)
        self.addAction(self.act_run)
    
    def focusInEvent(self, e):
        share.common.debug_print("FileEditorWindow Fokus IN")
        super().focusInEvent(e)

    def _apply_tab_settings(self):
        try:
            fm = QFontMetrics(self.font())
            try:
                tabw = fm.horizontalAdvance(self._tab_spaces)
            except AttributeError:
                tabw = fm.width(self._tab_spaces)
            self.setTabStopDistance(max(1, tabw))
        except Exception:
            pass

    def setFont(self, font):
        super().setFont(font)
        self._apply_tab_settings()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab and not (event.modifiers() & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)):
            cursor = self.textCursor()
            if cursor.hasSelection():
                self._indent_selection_with_spaces()
            else:
                cursor.insertText(self._tab_spaces)
            return

        if event.key() == Qt.Key_Backtab and not (event.modifiers() & (Qt.ControlModifier | Qt.AltModifier | Qt.MetaModifier)):
            self._unindent_selection_spaces()
            return

        super().keyPressEvent(event)

    def _indent_selection_with_spaces(self):
        cursor = self.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()
        cursor.setPosition(start)
        first_block = self.document().findBlock(start).blockNumber()
        last_block = self.document().findBlock(max(start, end - 1)).blockNumber()

        for block_no in range(first_block, last_block + 1):
            block = self.document().findBlockByNumber(block_no)
            if not block.isValid():
                continue
            c = QTextCursor(block)
            c.movePosition(QTextCursor.StartOfBlock)
            c.insertText(self._tab_spaces)

        cursor.endEditBlock()

    def _unindent_selection_spaces(self):
        cursor = self.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.beginEditBlock()
        first_block = self.document().findBlock(start).blockNumber()
        last_block = self.document().findBlock(max(start, end - 1)).blockNumber()

        for block_no in range(first_block, last_block + 1):
            block = self.document().findBlockByNumber(block_no)
            if not block.isValid():
                continue
            text = block.text()
            remove_count = 0
            for ch in text[:4]:
                if ch == ' ':
                    remove_count += 1
                else:
                    break
            if remove_count > 0:
                c = QTextCursor(block)
                c.movePosition(QTextCursor.StartOfBlock)
                for _ in range(remove_count):
                    c.deleteChar()

        cursor.endEditBlock()

    def eventFilter(self, obj, event):
        if obj is self.viewport() and event.type() == QEvent.Wheel:
            if self._handle_vertical_wheel(event):
                event.accept()
                return True
        return super().eventFilter(obj, event)

    def wheelEvent(self, event):
        if self._handle_vertical_wheel(event):
            event.accept()
            return
        super().wheelEvent(event)
        event.accept()

    def _handle_vertical_wheel(self, event) -> bool:
        sb = self.verticalScrollBar()
        if sb is None:
            return False

        pixel_delta_y = event.pixelDelta().y()
        angle_delta_y = event.angleDelta().y()
        angle_delta_x = event.angleDelta().x()

        if angle_delta_y == 0 and pixel_delta_y == 0:
            return False if angle_delta_x else True

        single_step = max(1, sb.singleStep())
        page_step = max(single_step, sb.pageStep())

        if pixel_delta_y:
            steps = float(pixel_delta_y) / 40.0
        else:
            steps = float(angle_delta_y) / 120.0

        mods = event.modifiers()
        factor = 3.0
        if mods & Qt.ShiftModifier:
            factor = 0.5
        elif mods & Qt.ControlModifier:
            factor = float(page_step) / float(single_step)

        delta = int(round(steps * single_step * factor))
        if delta == 0:
            delta = 1 if steps > 0 else -1

        target = sb.value() - delta
        sb.setValue(max(sb.minimum(), min(sb.maximum(), target)))

        # Wichtig: NICHT ensureCursorVisible() aufrufen.
        # Sonst springt der sichtbare Bereich sofort wieder zur aktuellen
        # Cursor-Zeile zurück und das Scrollen per Mausrad wirkt so, als
        # würde der Editor gar nicht scrollen.
        self.viewport().update()

        mm = getattr(self, "_minimap", None)
        if mm is not None:
            mm.viewport().update()
        return True
        
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

class MiniMap(QPlainTextEdit):
    """
    Read-only minimap view for a main QPlainTextEdit.
    Shows viewport overlay + optional cursor line marker.
    Dragging overlay scrolls main editor.
    """
    def __init__(self, main_editor: QPlainTextEdit, parent=None):
        super().__init__(parent)
        self.main = main_editor

        self.setReadOnly(True)
        self.setUndoRedoEnabled(False)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setFocusPolicy(Qt.NoFocus)
        self.setCenterOnScroll(False)
        self.setMouseTracking(True)
        self.viewport().installEventFilter(self)
        self._sync_guard = 0

        # Tiny font
        f = QFont(self.main.font())
        f.setPointSize(max(6, f.pointSize() - 4))
        self.setFont(f)

        # Make it look like a minimap
        self.setFrameShape(QFrame.NoFrame)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Overlay behavior
        self._dragging = False
        self._drag_offset_y = 0

        # Keep text + basic settings in sync
        self._sync_all()

        # Signals: main -> minimap
        self.main.textChanged.connect(self._sync_text)
        self.main.verticalScrollBar().valueChanged.connect(self._sync_scroll_from_main)
        self.main.cursorPositionChanged.connect(self._update_overlay)
        self.main.updateRequest.connect(lambda *_: self._update_overlay())

        # Signals: minimap -> main (scrollbar sync)
        self.verticalScrollBar().valueChanged.connect(self._sync_scroll_to_main)

        # Keep document layout similar
        self.document().setDocumentMargin(self.main.document().documentMargin())

        # Initial overlay
        QTimer.singleShot(0, self._update_overlay)

    # ---------- sync helpers ----------
    def _sync_all(self):
        self._sync_text()
        self._sync_scroll_from_main()
        self._update_overlay()

    def _sync_text(self):
        # Avoid cursor jumps: preserve minimap scrollbar ratio
        sb = self.verticalScrollBar()
        ratio = 0.0
        if sb.maximum() > 0:
            ratio = sb.value() / sb.maximum()

        self.setPlainText(self.main.toPlainText())

        # Restore approximate scroll ratio after text update
        QTimer.singleShot(0, lambda: self._restore_ratio(ratio))

    def _restore_ratio(self, ratio: float):
        sb = self.verticalScrollBar()
        if sb.maximum() > 0:
            self._sync_guard += 1
            try:
                was_blocked = sb.blockSignals(True)
                sb.setValue(int(ratio * sb.maximum()))
                sb.blockSignals(was_blocked)
            finally:
                self._sync_guard = max(0, self._sync_guard - 1)
        self._update_overlay()

    def _sync_scroll_from_main(self):
        if self._dragging:
            return
        m = self.main.verticalScrollBar()
        s = self.verticalScrollBar()
        self._sync_guard += 1
        try:
            self._map_scrollbars(m, s)
        finally:
            self._sync_guard = max(0, self._sync_guard - 1)
        self._update_overlay()

    def _sync_scroll_to_main(self, _value: int):
        if self._dragging or self._sync_guard:
            # during drag we drive main directly
            # or while main -> minimap sync is active
            return
        m = self.main.verticalScrollBar()
        s = self.verticalScrollBar()
        self._map_scrollbars(s, m)
        self._update_overlay()

    @staticmethod
    def _map_scrollbars(src: QScrollBar, dst: QScrollBar):
        # Map src.value in [0..src.max] to dst.value in [0..dst.max]
        if dst is None:
            return
        if src.maximum() <= 0 or dst.maximum() <= 0:
            was_blocked = dst.blockSignals(True)
            try:
                dst.setValue(0)
            finally:
                dst.blockSignals(was_blocked)
            return
        ratio = src.value() / src.maximum()
        was_blocked = dst.blockSignals(True)
        try:
            dst.setValue(int(ratio * dst.maximum()))
        finally:
            dst.blockSignals(was_blocked)

    # ---------- overlay drawing ----------
    def _visible_block_range_in_main(self):
        # Which blocks (lines) are visible in main editor?
        main = self.main
        vb = main.firstVisibleBlock()
        if not vb.isValid():
            return 0, 0

        start_block = vb.blockNumber()

        # Estimate how many blocks fit in main viewport
        bh = main.blockBoundingRect(vb).height()
        if bh <= 0:
            bh = QFontMetrics(main.font()).height()

        blocks_visible = int(main.viewport().height() / bh) + 2
        end_block = start_block + blocks_visible
        return start_block, end_block

    def _block_y_in_minimap(self, block_number: int) -> int:
        # Convert block number to y coordinate in minimap viewport using its own geometry
        doc = self.document()
        block = doc.findBlockByNumber(block_number)
        if not block.isValid():
            return 0
        r = self.blockBoundingGeometry(block).translated(self.contentOffset())
        return int(r.top())

    def _update_overlay(self):
        self.viewport().update()

    def paintEvent(self, e: QPaintEvent):
        super().paintEvent(e)

        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.Antialiasing, False)

        # Draw viewport overlay (visible region of main)
        start_b, end_b = self._visible_block_range_in_main()
        y1 = self._block_y_in_minimap(start_b)
        y2 = self._block_y_in_minimap(end_b)
        if y2 <= y1:
            y2 = y1 + 20

        overlay_rect = QRect(0, y1, self.viewport().width(), y2 - y1)

        # translucent overlay
        overlay_color = QColor(255, 215, 0, 40)  # gold-ish, transparent
        border_color  = QColor(255, 215, 0, 160)

        painter.fillRect(overlay_rect, overlay_color)
        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRect(overlay_rect.adjusted(0, 0, -1, -1))

        # Optional: cursor line marker (thin)
        cursor_block = self.main.textCursor().blockNumber()
        cy = self._block_y_in_minimap(cursor_block)
        cpen = QPen(QColor(255, 215, 0, 200))
        cpen.setWidth(1)
        painter.setPen(cpen)
        painter.drawLine(0, cy, self.viewport().width(), cy)

        painter.end()

    # ---------- mouse interaction (drag overlay to scroll main) ----------
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset_y = event.pos().y()
            self._scroll_main_to_minimap_y(event.pos().y())
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging:
            self._scroll_main_to_minimap_y(event.pos().y())
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self._dragging:
            self._dragging = False
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def eventFilter(self, obj, event):
        if obj is self.viewport() and event.type() == QEvent.Wheel:
            if hasattr(self.main, "_handle_vertical_wheel") and self.main._handle_vertical_wheel(event):
                event.accept()
                return True
        return super().eventFilter(obj, event)

    def wheelEvent(self, event):
        # MiniMap-Rad scrollt den Haupteditor und konsumiert das Event,
        # damit der MDI-Bereich es nicht übernimmt.
        if hasattr(self.main, "_handle_vertical_wheel") and self.main._handle_vertical_wheel(event):
            event.accept()
            return
        self.main.wheelEvent(event)
        event.accept()

    def _scroll_main_to_minimap_y(self, y: int):
        # Map minimap y position to a block number, then scroll main to that block.
        # We compute which block is under y and set main scrollbar ratio accordingly.
        doc = self.document()
        # Convert y to document coordinate
        y_doc = y - self.contentOffset().y()

        # Find approximate block by scanning from first visible block in minimap
        first = self.firstVisibleBlock()
        if not first.isValid():
            return

        block = first
        while block.isValid():
            rect = self.blockBoundingGeometry(block)
            top = rect.top()
            bottom = rect.bottom()
            if top <= y_doc <= bottom:
                target_block = block.blockNumber()
                self._scroll_main_to_block(target_block)
                return
            if top > y_doc:
                # y is above current block -> use current
                target_block = block.blockNumber()
                self._scroll_main_to_block(target_block)
                return
            block = block.next()

        # If beyond end, go to bottom
        self.main.verticalScrollBar().setValue(self.main.verticalScrollBar().maximum())

    def _scroll_main_to_block(self, block_number: int):
        m = self.main.verticalScrollBar()
        doc = self.main.document()
        last_block = max(1, doc.blockCount() - 1)
        ratio = max(0.0, min(1.0, block_number / last_block))
        m.setValue(int(ratio * m.maximum()))
        self._update_overlay()

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
    
class FileEditorWindow(QDialog):
    def __init__(self, parent, initial_path: str = "", initial_text: str = ""):
        super().__init__(parent)
        self.parent = parent
        mark_escape_close(self)

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
            self.new_tab(title="unbenannt.prg", path="", text=initial_text or "")

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

        # Einzeilige Kommentare: NOTE, //, &&, **
        def repl_line(m):
            return " " * (m.end() - m.start())

        text = re.sub(r"(?im)\bNOTE\b.*?$", repl_line, text)
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
            dlg = share.common.showException(self, "Run-Fehler " + type(e).__name__, tb_str)
            dlg.exec_()

    def _create_editor(self):
        self.editor = CodeEditor(self)
        self.editor.setPlaceholderText("Schreib hier was rein…")
        self.editor.setLineWrapMode(self.editor.NoWrap)
        self.editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.editor.setFont(QFont("Consolas", 10))

        self.minimap = MiniMap(self.editor)
        self.minimap.setVisible(True)          # oder False als Default
        self.minimap.setMinimumWidth(140)      # damit sie nicht auf 0 kollabiert

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.minimap)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 0)
        splitter.setSizes([900, 180])

        self.container = QWidget()
        self.container._editor = self.editor

        lay = QHBoxLayout(self.container)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(splitter)

        # wichtig: Referenzen speichern (pro Editor!)
        self.editor._minimap = self.minimap
        self.editor._minimap_container = self.container

        # Strg+S / Strg+O direkt im Editor
        self.editor.act_save_file = QAction("Speichern", self.editor)
        self.editor.act_save_file.setShortcut(QKeySequence("Ctrl+S"))
        self.editor.act_save_file.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.editor.act_save_file.triggered.connect(lambda ed=self.editor: self.file_save(self._tab_index_for_editor(ed)))
        self.editor.addAction(self.editor.act_save_file)

        self.editor.act_open_file = QAction("Öffnen", self.editor)
        self.editor.act_open_file.setShortcut(QKeySequence("Ctrl+O"))
        self.editor.act_open_file.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self.editor.act_open_file.triggered.connect(self.file_open)
        self.editor.addAction(self.editor.act_open_file)

        share.common.debug_print("1111")
        self.highlighter = DBaseHighlighter(self.editor.document())
        share.common.debug_print("2222")
        return self.editor

    def set_minimap_visible(self, visible: bool):
        ed = self.current_editor()
        mm = self.minimap
        if mm is not None:
            share.common.debug_print("set visible: ", visible)
            mm.setVisible(visible)
        
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
    def _editor_from_tab_widget(self, w):
        if w is None:
            return None
        if isinstance(w, (QPlainTextEdit, QTextEdit)):
            return w
        ed = getattr(w, "_editor", None)
        if ed is not None:
            return ed
        try:
            ed = w.findChild(QPlainTextEdit)
            if ed is not None:
                return ed
            ed = w.findChild(QTextEdit)
            if ed is not None:
                return ed
        except Exception:
            pass
        return None

    def current_editor(self) -> CodeEditor:
        w = self.editor_tabs.currentWidget()
        if w is None:
            return None
        return self._editor_from_tab_widget(w)

    def current_tab_index(self) -> int:
        return int(self.editor_tabs.currentIndex())

    def _normalize_meta_path(self, path: str) -> str:
        if not path:
            return ""
        try:
            return os.path.normcase(os.path.abspath(os.path.normpath(path)))
        except Exception:
            return os.path.normcase(os.path.normpath(path))

    def _tab_index_for_editor(self, editor) -> int:
        if editor is None:
            return self.current_tab_index()
        for i in range(self.editor_tabs.count()):
            ed = self._editor_from_tab_widget(self.editor_tabs.widget(i))
            if ed is editor:
                return i
        return self.current_tab_index()

    def _find_open_tab_by_path(self, path: str) -> int:
        needle = self._normalize_meta_path(path)
        if not needle:
            return -1
        for i in range(self.editor_tabs.count()):
            cur = self._normalize_meta_path(self.tab_path(i))
            if cur and cur == needle:
                return i
        return -1

    def tab_path(self, idx: int) -> str:
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
        return getattr(ed, "_path", "") if ed is not None else ""

    def set_tab_path(self, idx: int, path: str) -> None:
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
        if ed is not None:
            setattr(ed, "_path", path)

    def tab_display_name(self, path: str, idx: Optional[int] = None) -> str:
        if path:
            return os.path.basename(path)
        if idx is not None:
            ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
            if ed is not None:
                disp = getattr(ed, "_display_name", "") or ""
                if disp:
                    return disp
        return "unbenannt.prg"

    def _update_tab_visuals(self, idx: int) -> None:
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
        if ed is None:
            return
        modified = bool(ed.document().isModified())
        # TabText: nur Dateiname (ohne Pfad)
        title = self.tab_display_name(getattr(ed, "_path", ""), idx)
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

    def new_tab(
        self,
        title: str = "unbenannt.prg",
        path: str = "",
        text: str = "",
        default_suffix: str = "",
        name_filters=None,
    ) -> int:
        ed = self._create_editor()
        ed.setFont(QFont("Consolas", 10))
        ed.setLineWrapMode(ed.NoWrap)
        ed.setPlainText(text or "")
        
        ed.document().setModified(False)
        ed.runRequested.connect(self.run_current_text)
        ed.cursorPositionChanged.connect(self._update_cursor_status)
        
        setattr(ed, "_path", path or "")
        setattr(ed, "_display_name", title or "unbenannt.prg")

        ds = (default_suffix or "").strip().lstrip(".")
        if not ds:
            ds = os.path.splitext(title or "")[1].lstrip(".")
        if not ds:
            ds = "prg"
        setattr(ed, "_default_suffix", ds)

        nf = list(name_filters or [])
        setattr(ed, "_name_filters", nf)
        
        # Syntax Highlighter pro Editor
        try:
            share.common.debug_print("oooooo")
            self._highlighter = DBaseHighlighter(ed.document())
            share.common.debug_print("999999")
        except Exception as e:
            share.common.debug_print(e)

        #idx = self.editor_tabs.addTab(ed, title)
        idx = self.editor_tabs.addTab(ed._minimap_container, title)
        self.editor_tabs.setCurrentIndex(idx)
        share.common.debug_print("----->>>>")
        # Modified Tracking
        ed.document().contentsChanged.connect(self._schedule_tree_refresh)
        ed.document().modificationChanged.connect(lambda _m, i=idx: self._update_tab_visuals(i))
        share.common.debug_print("AAAAA")
        self._update_tab_visuals(idx)
        share.common.debug_print("iuiuiui")
        return idx

    def open_path_in_tab(self, path: str, warn_if_open: bool = False) -> int:
        path = self._normalize_meta_path(path)
        existing = self._find_open_tab_by_path(path)
        if existing >= 0:
            if warn_if_open:
                QMessageBox.warning(
                    self,
                    "Datei bereits geöffnet",
                    f"Die Datei ist bereits geöffnet:\n{path}",
                    QMessageBox.Ok
                )
            self.editor_tabs.setCurrentIndex(existing)
            ed = self.current_editor()
            if ed is not None:
                ed.setFocus()
            return existing
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                txt = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Datei nicht öffnen:\n{e}")
            return -1
        idx = self.new_tab(title=self.tab_display_name(path), path=path, text=txt)
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
        if ed is not None:
            ed.setFocus()
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
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
        if ed is None:
            return True
        if not ed.document().isModified():
            return True
        title = self.tab_display_name(getattr(ed, "_path", ""), idx)
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
        self.new_tab(title="unbenannt.prg", path="", text="")

    def file_open(self) -> bool:
        dlg = QFileDialog(self, "Öffnen")
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilters(["dBase Quellcode (*.prg)", "Alle Dateien (*.*)"])
        if not dlg.exec_():
            return False
        files = dlg.selectedFiles()
        if not files:
            return False
        idx = self.open_path_in_tab(files[0], warn_if_open=True)
        return idx >= 0

    def file_save(self, idx: Optional[int] = None) -> bool:
        if idx is None:
            idx = self.current_tab_index()
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
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
        ed = self._editor_from_tab_widget(self.editor_tabs.widget(idx))
        if ed is None:
            return False
        
        default_suffix = (getattr(ed, "_default_suffix", "") or "").strip().lstrip(".")
        display_name   = (getattr(ed, "_display_name", "") or "").strip()
        name_filters   = list(getattr(ed, "_name_filters", []) or [])

        if not default_suffix:
            default_suffix = os.path.splitext(display_name)[1].lstrip(".") if display_name else ""
        if not default_suffix:
            default_suffix = "prg"

        if not name_filters:
            ext = default_suffix.lower()
            if ext in ("html", "htm"):
                name_filters = ["HTML Dokument (*.html *.htm)", "Alle Dateien (*.*)"]
            elif ext == "css":
                name_filters = ["CSS Stylesheet (*.css)", "Alle Dateien (*.*)"]
            elif ext == "js":
                name_filters = ["JavaScript (*.js)", "Alle Dateien (*.*)"]
            else:
                name_filters = ["dBase Quellcode (*.prg)", "Alle Dateien (*.*)"]

        dlg = QFileDialog(self, "Speichern unter")
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setDefaultSuffix(default_suffix)
        dlg.setNameFilters(name_filters)
        dlg.setOption(QFileDialog.DontConfirmOverwrite, True)

        if cur_path:
            dlg.selectFile(cur_path)
        else:
            dlg.selectFile(display_name or f"unbenannt.{default_suffix}")
        
        if not dlg.exec_():
            return False
        files = dlg.selectedFiles()
        if not files:
            return False
            
        path = files[0]
        if os.path.exists(path):
            res = QMessageBox.question(
                self,
                "Datei überschreiben?",
                f"Die Datei existiert bereits und soll überschrieben werden:\n{path}",
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Cancel
            )
            if res != QMessageBox.Ok:
                return False
        
        setattr(ed, "_path", path)
        setattr(ed, "_display_name", os.path.basename(path))
        
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
            ed = self.current_editor()
            if ed is None:
                return
            
            name = self.tab_display_name(getattr(ed, "_path", ""), idx)
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
