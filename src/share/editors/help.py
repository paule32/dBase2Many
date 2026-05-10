# ---------------------------------------------------------------------------
# File:   help.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import json
import os
import sys
import uuid

from   dataclasses   import dataclass
from   share.locales import *

ROLE_BLOCK_POS  = Qt.UserRole
ROLE_TOPIC_HTML = Qt.UserRole + 1
ROLE_TOPIC_ID   = Qt.UserRole + 2

@dataclass
class TableSpec:
    rows         : int =   2
    cols         : int =   2
    border       : int =   1
    cell_padding : int =   4
    cell_spacing : int =   0
    width_percent: int = 100

class TableInsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(share.locales.tr("Insert Table"))
        self.resize(360, 220)
        self.setStyleSheet(self._qss())
        
        lay  = QVBoxLayout(self)
        form = QFormLayout()

        self.spin_rows    = QSpinBox(); self.spin_rows   .setRange( 1, 100); self.spin_rows.setValue(2)
        self.spin_cols    = QSpinBox(); self.spin_cols   .setRange( 1,  50); self.spin_cols.setValue(2)
        self.spin_border  = QSpinBox(); self.spin_border .setRange( 0,  20); self.spin_border.setValue(1)
        self.spin_padding = QSpinBox(); self.spin_padding.setRange( 0,  50); self.spin_padding.setValue(4)
        self.spin_spacing = QSpinBox(); self.spin_spacing.setRange( 0,  50); self.spin_spacing.setValue(0)
        self.spin_width   = QSpinBox(); self.spin_width  .setRange(10, 100); self.spin_width.setValue(100)

        form.addRow(share.locales.tr("Lines:"      ), self.spin_rows)
        form.addRow(share.locales.tr("Columns:"    ), self.spin_cols)
        form.addRow(share.locales.tr("Border:"     ), self.spin_border)
        form.addRow(share.locales.tr("Padding:"    ), self.spin_padding)
        form.addRow(share.locales.tr("Cell Pad.:"  ), self.spin_spacing)
        form.addRow(share.locales.tr("Width in % :"), self.spin_width)
        
        lay.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        lay.addWidget(buttons)

    def spec(self) -> TableSpec:
        return TableSpec(
            rows          = self.spin_rows   .value(),
            cols          = self.spin_cols   .value(),
            border        = self.spin_border .value(),
            cell_padding  = self.spin_padding.value(),
            cell_spacing  = self.spin_spacing.value(),
            width_percent = self.spin_width  .value(),
        )

    def _qss(self) -> str:
        return """
        QDialog { background:#131313; color:#ffd84d; }
        QLabel { color:#ffd84d; }
        QSpinBox {
            background:#1d1d1d; color:white; border:1px solid #3a3a3a; min-height:22px;
        }
        QPushButton {
            background:#1a1a1a; color:#ffd84d; border:1px solid #3a3a3a; min-height:24px; padding:4px 10px;
        }
        QPushButton:hover { background:#232323; }
        """

class HtmlSourceDialog(QDialog):
    def __init__(self, html: str, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(share.locales.tr("HTML Source Code"))
        self.resize(900, 700)
        self.setStyleSheet("""
            QDialog { background:#131313; color:#ffd84d; }
            QPlainTextEdit {
                background:#1b1b1b; color:white; border:1px solid #555;
                selection-background-color:#0b57d0;
            }
            QPushButton {
                background:#1a1a1a; color:#ffd84d; border:1px solid #3a3a3a; min-height:24px; padding:4px 10px;
            }
        """)

        lay = QVBoxLayout(self)
        
        self.editor = QPlainTextEdit()
        self.editor.setPlainText(html)
        self.editor.setLineWrapMode(QPlainTextEdit.NoWrap)
        
        lay.addWidget(self.editor)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        lay.addWidget(buttons)

    def html(self) -> str:
        return self.editor.toPlainText()

class ActionComboBox(QComboBox):
    doubleClicked = pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)

class LinkTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(share.locales.tr("Choose Link-Type"))
        self.resize(280, 120)

        lay = QVBoxLayout(self)
        
        self.rb_http = QRadioButton(share.locales.tr("HTTP-Address"))
        self.rb_mail = QRadioButton(share.locales.tr("E-Mail-Address"))
        self.rb_http.setChecked(True)
        
        lay.addWidget(self.rb_http)
        lay.addWidget(self.rb_mail)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        lay.addWidget(buttons)

    def link_type(self):
        return 'mail' if self.rb_mail.isChecked() else 'http'

class HelpAuthoringEditor(QMainWindow):
    contentChanged = pyqtSignal()

    def __init__(self, parent=None, initial_html: str = "", file_path: str = ""):
        super().__init__(parent)
        self.current_path = file_path or ""

        self._is_dirty           = False
        self._loading_topic_html = False
        self._loading_toc_model  = False
        self._last_tab_index     = -1

        self.setWindowTitle(share.locales.tr("Help Authoring"))
        self.resize(1000, 520)

        self.toc_model = QStandardItemModel()
        self.toc_model.setHorizontalHeaderLabels([share.locales.tr("TOC")])
        self.toc_model.itemChanged.connect(self._on_toc_item_changed)
        
        self.toc_view = QTreeView()
        self.toc_view.setModel(self.toc_model)
        self.toc_view.setMinimumWidth(180)
        self.toc_view.setHeaderHidden(False)
        self.toc_view.clicked.connect(self._on_toc_clicked)
        self.toc_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toc_view.customContextMenuRequested.connect(self._on_toc_context_menu)
        self.toc_view.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

        self.editor = None
        self._add_editor_tab(initial_html or self._default_document_html(), file_path)

        self.format_tabs = QTabWidget()
        self.format_tabs.setMinimumHeight(210)
        
        self._build_format_tab()
        self._build_links_tab()
        self._build_table_tab()

        self.right_splitter = QSplitter(Qt.Vertical)
        self.right_splitter.addWidget(self.format_tabs)
        self.right_splitter.addWidget(self.tab_widget)
        self.right_splitter.setStretchFactor(0, 0)
        self.right_splitter.setStretchFactor(1, 1)
        self.right_splitter.setSizes([240, 480])

        self.main_splitter = QSplitter(Qt.Horizontal)
        self.main_splitter.addWidget(self.toc_view)
        self.main_splitter.addWidget(self.right_splitter)
        self.main_splitter.setStretchFactor(0, 0)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setSizes([240, 760])
        self.setCentralWidget(self.main_splitter)

        self._build_toolbar()
        #self._apply_dark_qss()
        #self._seed_toc()
        
        self._settings = QSettings(self._ini_path(), QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)
        
        if initial_html:
            roots = [self._new_topic_item(share.locales.tr("New Topic"), initial_html)]
            self._add_editor_tab('', file_path, roots)
        else:
            self.file_new()
        
        self._restore_window_state()

    def _ini_path(self) -> str:
        try:
            base = os.path.dirname(os.path.abspath(sys.argv[0]))
        except Exception:
            base = os.getcwd()
        return os.path.join(base, 'dBaseRunner.ini')

    def _build_format_tab(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(6)

        row = QHBoxLayout()
        self.btn_bold = QPushButton("F")
        self.btn_italic = QPushButton("K")
        self.btn_underline = QPushButton("U")
        self.btn_strike = QPushButton("S")
        for btn in (self.btn_bold, self.btn_italic, self.btn_underline, self.btn_strike):
            btn.setCheckable(True)
            btn.setMinimumWidth(42)
            row.addWidget(btn)
        row.addStretch(1)
        lay.addLayout(row)

        row = QHBoxLayout()
        self.dock_font_combo = QFontComboBox()
        self.dock_font_combo.setCurrentFont(QFont("Arial"))
        self.dock_size_combo = QComboBox()
        self.dock_size_combo.setEditable(True)
        for size in (8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72):
            self.dock_size_combo.addItem(str(size))
        self.dock_size_combo.setCurrentText("11")
        row.addWidget(self.dock_font_combo, 1)
        row.addWidget(self.dock_size_combo, 0)
        lay.addLayout(row)

        row = QHBoxLayout()
        self.btn_text_color = QPushButton("Text Color")
        self.btn_bg_color = QPushButton("BG Color")
        row.addWidget(self.btn_text_color)
        row.addWidget(self.btn_bg_color)
        row.addStretch(1)
        lay.addLayout(row)

        self.align_combo = QComboBox()
        self.align_combo.addItems(["Left", "Center", "Right", "Block"])
        lay.addWidget(self.align_combo)

        row = QHBoxLayout()
        self.bullet_combo = QComboBox()
        self.bullet_combo.addItems(["List Disc", "List Circle", "List Square"])
        self.number_combo = QComboBox()
        self.number_combo.addItems([
            "Number: decimal",
            "Number: lower alpha",
            "Number: upper alpha",
            "Number: lower roman",
            "Number: upper roman",
        ])
        row.addWidget(self.bullet_combo)
        row.addWidget(self.number_combo)
        lay.addLayout(row)
        lay.addStretch(1)

        self.btn_bold.toggled.connect(self._dock_toggle_bold)
        self.btn_italic.toggled.connect(self._dock_toggle_italic)
        self.btn_underline.toggled.connect(self._dock_toggle_underline)
        self.btn_strike.toggled.connect(self._dock_toggle_strike)
        self.dock_font_combo.currentFontChanged.connect(self.set_font_family)
        self.dock_size_combo.currentTextChanged.connect(self.set_font_size_from_text)
        self.btn_text_color.clicked.connect(self.set_text_color)
        self.btn_bg_color.clicked.connect(self.set_background_color)
        self.align_combo.activated.connect(self._on_align_combo_activated)
        self.bullet_combo.activated.connect(self._on_bullet_combo_activated)
        self.number_combo.activated.connect(self._on_number_combo_activated)

        self.format_tabs.addTab(tab, "Format")

    def _build_links_tab(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(6)

        row = QHBoxLayout()
        self.link_edit = QLineEdit()
        self.link_edit.setPlaceholderText("Resource path, URL, e-Mail or Anchor ...")
        self.btn_pick_resource = QPushButton("...")
        self.btn_pick_resource.setMaximumWidth(40)
        row.addWidget(self.link_edit, 1)
        row.addWidget(self.btn_pick_resource)
        lay.addLayout(row)

        row = QHBoxLayout()
        self.btn_insert_link = QPushButton("Link")
        self.btn_insert_mail = QPushButton("e-Mail")
        self.btn_insert_image = QPushButton("Image")
        self.btn_insert_anchor = QPushButton("Anchor")
        row.addWidget(self.btn_insert_link)
        row.addWidget(self.btn_insert_mail)
        row.addWidget(self.btn_insert_image)
        row.addWidget(self.btn_insert_anchor)
        row.addStretch(1)
        lay.addLayout(row)
        lay.addStretch(1)

        self.btn_pick_resource.clicked.connect(self.pick_resource_path)
        self.btn_insert_link.clicked.connect(self.insert_link_from_tab)
        self.btn_insert_mail.clicked.connect(self.insert_mail_from_tab)
        self.btn_insert_image.clicked.connect(self.insert_image_from_tab)
        self.btn_insert_anchor.clicked.connect(self.insert_anchor_from_tab)

        self.format_tabs.addTab(tab, "Links / Anchors")

    def _build_table_tab(self):
        tab = QWidget()
        lay = QVBoxLayout(tab)
        lay.setContentsMargins(6, 6, 6, 6)
        lay.setSpacing(6)

        row = QHBoxLayout()
        self.btn_insert_table = QPushButton("Table")
        self.table_ops_combo = QComboBox()
        self.table_ops_combo.addItems(["+ Line", "+ Column", "- Line", "- Column", "Concatenate"])
        self.btn_table_cell_color = QPushButton("Cell Color")
        row.addWidget(self.btn_insert_table)
        row.addWidget(self.table_ops_combo, 1)
        row.addWidget(self.btn_table_cell_color)
        lay.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Border"))
        self.edit_margin_left = QLineEdit(); self.edit_margin_left.setPlaceholderText("Left")
        self.edit_margin_top = QLineEdit(); self.edit_margin_top.setPlaceholderText("Top")
        self.edit_margin_right = QLineEdit(); self.edit_margin_right.setPlaceholderText("Right")
        self.edit_margin_bottom = QLineEdit(); self.edit_margin_bottom.setPlaceholderText("Bottom")
        self.spin_border_radius = QSpinBox(); self.spin_border_radius.setRange(0, 100)
        row.addWidget(self.edit_margin_left)
        row.addWidget(self.edit_margin_top)
        row.addWidget(self.edit_margin_right)
        row.addWidget(self.edit_margin_bottom)
        row.addWidget(QLabel("Radius"))
        row.addWidget(self.spin_border_radius)
        lay.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Cell Size"))
        self.edit_cell_width = QLineEdit(); self.edit_cell_width.setPlaceholderText("Width")
        self.edit_cell_height = QLineEdit(); self.edit_cell_height.setPlaceholderText("Height")
        self.edit_cell_colspan = QLineEdit(); self.edit_cell_colspan.setPlaceholderText("ColSpan")
        self.edit_cell_rowspan = QLineEdit(); self.edit_cell_rowspan.setPlaceholderText("RowSpan")
        row.addWidget(self.edit_cell_width)
        row.addWidget(self.edit_cell_height)
        row.addWidget(self.edit_cell_colspan)
        row.addWidget(self.edit_cell_rowspan)
        lay.addLayout(row)
        lay.addStretch(1)

        self.btn_insert_table.clicked.connect(self.insert_table)
        self.table_ops_combo.activated.connect(self._on_table_ops_combo_activated)
        self.btn_table_cell_color.clicked.connect(self.table_set_cell_background)

        self.format_tabs.addTab(tab, "Table")

    def _build_toolbar(self):
        tb = self.addToolBar("File")
        tb.setIconSize(QSize(16, 16))
        act_source = QAction("HTML", self)
        act_source.triggered.connect(self.show_html_debug)
        tb.addAction(act_source)

    def edit_html_source(self):
        editor = self._current_editor()
        if editor is None:
            return
        dlg = HtmlSourceDialog(editor.toHtml(), self)
        if dlg.exec_() != QDialog.Accepted:
            return
        editor.setHtml(dlg.html())
        item = self._toc_current_item()
        if item is not None:
            item.setData(editor.toHtml(), ROLE_TOPIC_HTML)
            self._save_toc_to_current_editor()

    def _restore_window_state(self):
        try:
            geom = self._settings.value('help_authoring/main_geom')
            if geom is not None:
                self.restoreGeometry(geom)
        except Exception:
            pass
        try:
            state = self._settings.value('help_authoring/main_state')
            if state is not None:
                self.restoreState(state)
        except Exception:
            pass
        try:
            if hasattr(self, 'format_dock') and self.format_dock is not None:
                self.format_dock.setFloating(False)
                self.format_dock.show()
                self.format_dock.setVisible(True)
        except Exception:
            pass
        try:
            sizes = self._settings.value('help_authoring/splitter_sizes')
            if sizes is not None:
                self.splitter.setSizes([int(x) for x in sizes])
        except Exception:
            pass

    def _save_window_state(self):
        try:
            parent = self.parentWidget()
            if parent is not None and parent.__class__.__name__ == 'QMdiSubWindow':
                self._settings.setValue('help_authoring/sub_geom', parent.saveGeometry())
        except Exception:
            pass
        try:
            self._settings.setValue('help_authoring/main_geom'    , self.saveGeometry())
            self._settings.setValue('help_authoring/main_state'   , self.saveState())
            self._settings.setValue('help_authoring/splitter_sizes', self.splitter.sizes())
            self._settings.sync()
        except Exception:
            pass

    def _apply_dark_qss(self):
        self.setStyleSheet("""
            QMainWindow, QWidget { background:#131313; color:#ffffff; font:9pt Arial; }
            QTreeView, QTextEdit { background:#1b1b1b; color:#ffffff; border:1px solid #3a3a3a; }
            QTabWidget::pane { border:1px solid #3a3a3a; }
            QTabBar::tab { background:#1a1a1a; color:#ffd84d; padding:5px 10px; border:1px solid #333; }
            QTabBar::tab:selected { background:#252525; }
            QPushButton { background:#1a1a1a; color:#ffd84d; border:1px solid #3a3a3a; padding:4px 8px; min-height:22px; }
            QPushButton:checked { background:#2f2f2f; }
            QComboBox, QLineEdit, QFontComboBox, QSpinBox { background:#1b1b1b; color:#ffffff; border:1px solid #3a3a3a; min-height:24px; }
            QLabel { color:#ffd84d; }
        """)

    def _sync_current_editor_ref(self):
        self.editor = self._current_editor()
        self.current_path = getattr(self.editor, '_path', '') if self.editor is not None else ''

    def _set_editor_dirty(self, editor, state: bool):
        if editor is None:
            self._loading_toc_model = False
            return
        editor._dirty = bool(state)
        idx = self.tab_widget.indexOf(editor)
        if idx >= 0:
            title = self._title_from_path(getattr(editor, '_path', ''))
            if getattr(editor, '_dirty', False):
                title += ' *'
            self.tab_widget.setTabText(idx, title)

    def _update_window_title(self):
        editor = self._current_editor()
        if editor is None:
            self.setWindowTitle(share.locales.tr('Help Authoring'))
            return
        name = self._title_from_path(getattr(editor, '_path', ''))
        star = ' *' if getattr(editor, '_dirty', False) else ''
        self.current_path = getattr(editor, '_path', '')
        self.setWindowTitle(f'Help Authoring - {name}{star}')

    def _on_tab_close_requested(self, idx: int):
        editor = self._editor_at(idx)
        if editor is None:
            return
        if editor is self._current_editor():
            self._capture_current_project_to_editor(editor)
        if not self.maybe_save(editor):
            return
        self.tab_widget.removeTab(idx)
        editor.deleteLater()
        if self.tab_widget.count() == 0:
            self.file_new()
        else:
            self._sync_current_editor_ref()
            self._sync_toolbar_state()
            self._update_status()
            self._update_window_title()
            self._load_toc_from_current_editor()

    def _clone_item_deep(self, item):
        new_item = QStandardItem(item.text())
        new_item.setData(item.data(ROLE_BLOCK_POS ), ROLE_BLOCK_POS )
        new_item.setData(item.data(ROLE_TOPIC_HTML), ROLE_TOPIC_HTML)
        new_item.setData(item.data(ROLE_TOPIC_ID  ), ROLE_TOPIC_ID  )
        for row in range(item.rowCount()):
            child = item.child(row)
            if child is not None:
                new_item.appendRow(self._clone_item_deep(child))
        return new_item

    def _capture_current_project_to_editor(self, editor=None):
        if editor is None:
            editor = self._current_editor()
        if editor is None:
            return
        if editor is not self._current_editor():
            return
        item = self._toc_current_item()
        if item is not None:
            item.setData(editor.toHtml(), ROLE_TOPIC_HTML)
            editor._current_topic_id = item.data(ROLE_TOPIC_ID)
        self._save_toc_to_current_editor()

    def file_new(self):
        roots = [self._new_topic_item('New Topic', self._default_document_html())]
        editor = self._add_editor_tab('', '', roots)
        self._set_editor_dirty(editor, False)
        self._sync_current_editor_ref()
        self._update_window_title()
        self._update_status()
        self._load_toc_from_current_editor()

    def maybe_save(self, editor=None) -> bool:
        if isinstance(editor, bool):
            editor = None
        if editor is None:
            editor = self._current_editor()
        if editor is None:
            return True
        if not getattr(editor, '_dirty', False):
            return True
        title = self._title_from_path(getattr(editor, '_path', ''))
        ret = QMessageBox.question(self,
            'Änderungen speichern?',
            f'Das Dokument "{title}" wurde geändert.\nSoll es gespeichert werden?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes)
        if ret == QMessageBox.Cancel:
            return False
        if ret == QMessageBox.Yes:
            return self.file_save(editor)
        return True

    def _load_toc_from_current_editor(self):
        editor = self._current_editor()
        self._loading_toc_model = True
        self.toc_model.clear()
        self.toc_model.setHorizontalHeaderLabels(['TOC'])
        if editor is None:
            self._loading_toc_model = False
            return
        roots = getattr(editor, '_toc_snapshot', None)
        if roots:
            for item in roots:
                self.toc_model.appendRow(self._clone_item_deep(item))
            self.toc_view.expandAll()
            target = self._find_item_by_topic_id(getattr(editor, '_current_topic_id', None))
            if target is None and self.toc_model.rowCount() > 0:
                target = self.toc_model.item(0)
            if target is not None:
                idx = self.toc_model.indexFromItem(target)
                self.toc_view.setCurrentIndex(idx)
                self._load_topic_into_editor(target)
        self._loading_toc_model = False

    def _on_tab_changed(self, idx: int):
        self._sync_current_editor_ref()
        self._update_status()
        self._update_window_title()
        self._last_tab_index = idx

    def _toc_new_topic(self):
        item = self._toc_current_item()
        new_item = self._new_topic_item(share.locales.tr('New Topic'), self._default_document_html())
        if item is None:
            self.toc_model.appendRow(new_item)
        else:
            parent = item.parent() or self.toc_model.invisibleRootItem()
            parent.insertRow(item.row() + 1, new_item)
        self._save_toc_to_current_editor()
        self._toc_select_item(new_item)
        self.toc_view.edit(self.toc_model.indexFromItem(new_item))

    def _toc_add_sub_topic(self):
        item = self._toc_current_item()
        new_item = self._new_topic_item(share.locales.tr('Child Topic'), self._default_document_html())
        if item is None:
            self.toc_model.appendRow(new_item)
        else:
            item.appendRow(new_item)
            self.toc_view.expand(self.toc_model.indexFromItem(item))
        self._save_toc_to_current_editor()
        self._toc_select_item(new_item)
        self.toc_view.edit(self.toc_model.indexFromItem(new_item))

    def _toc_select_item(self, item):
        if item is None:
            return
        idx = self.toc_model.indexFromItem(item)
        if idx.isValid():
            self.toc_view.setCurrentIndex(idx)
            self.toc_view.scrollTo(idx)
            self._load_topic_into_editor(item)

    def _save_toc_to_current_editor(self):
        editor = self._current_editor()
        if editor is None:
            return
        roots = []
        for row in range(self.toc_model.rowCount()):
            item = self.toc_model.item(row)
            if item is not None:
                roots.append(self._clone_item_deep(item))
        editor._toc_snapshot = roots

    def _new_topic_item(self, title='New Topic', html=''):
        item = QStandardItem(title)
        item.setData(None, Qt.UserRole)
        item.setData(html or self._default_document_html(), ROLE_TOPIC_HTML)
        item.setData(str(uuid.uuid4()), ROLE_TOPIC_ID)
        return item

    def _toc_current_item(self):
        idx = self.toc_view.currentIndex()
        if not idx.isValid():
            return None
        return self.toc_model.itemFromIndex(idx)

    def _toc_delete(self):
        item = self._toc_current_item()
        if item is None:
            return
        parent = item.parent() or self.toc_model.invisibleRootItem()
        parent.removeRow(item.row())
        self._save_toc_to_current_editor()
        if self.toc_model.rowCount() > 0:
            self._toc_select_item(self.toc_model.item(0))

    def _toc_cut(self):
        item = self._toc_current_item()
        if item is None:
            return
        self._toc_clipboard_item = self._clone_item_deep(item)
        parent = item.parent() or self.toc_model.invisibleRootItem()
        parent.removeRow(item.row())
        self._save_toc_to_current_editor()
        if self.toc_model.rowCount() > 0:
            self._toc_select_item(self.toc_model.item(0))

    def _toc_paste(self):
        if self._toc_clipboard_item is None:
            return
        item = self._toc_current_item()
        new_item = self._clone_item_deep(self._toc_clipboard_item)
        if item is None:
            self.toc_model.appendRow(new_item)
        else:
            parent = item.parent() or self.toc_model.invisibleRootItem()
            parent.insertRow(item.row() + 1, new_item)
        self._save_toc_to_current_editor()
        self._toc_select_item(new_item)

    def _toc_move_up(self):
        item = self._toc_current_item()
        if item is None:
            return
        parent = item.parent() or self.toc_model.invisibleRootItem()
        row = item.row()
        if row <= 0:
            return
        data = parent.takeRow(row)
        parent.insertRow(row - 1, data)
        self._save_toc_to_current_editor()
        self._toc_select_item(data[0])

    def _toc_move_down(self):
        item = self._toc_current_item()
        if item is None:
            return
        parent = item.parent() or self.toc_model.invisibleRootItem()
        row = item.row()
        if row >= parent.rowCount() - 1:
            return
        data = parent.takeRow(row)
        parent.insertRow(row + 1, data)
        self._save_toc_to_current_editor()
        self._toc_select_item(data[0])

    def _toc_move_left(self):
        item = self._toc_current_item()
        if item is None:
            return
        parent_item = item.parent()
        if parent_item is None:
            return
        grand_parent = parent_item.parent() or self.toc_model.invisibleRootItem()
        parent_row = parent_item.row()
        data = parent_item.takeRow(item.row())
        grand_parent.insertRow(parent_row + 1, data)
        self._save_toc_to_current_editor()
        self._toc_select_item(data[0])

    def _toc_move_right(self):
        item = self._toc_current_item()
        if item is None:
            return
        parent = item.parent() or self.toc_model.invisibleRootItem()
        row = item.row()
        if row <= 0:
            return
        prev_sibling = parent.child(row - 1)
        if prev_sibling is None:
            return
        data = parent.takeRow(row)
        prev_sibling.appendRow(data)
        self.toc_view.expand(self.toc_model.indexFromItem(prev_sibling))
        self._save_toc_to_current_editor()
        self._toc_select_item(data[0])

    def _load_topic_into_editor(self, item):
        editor = self._current_editor()
        if editor is None or item is None:
            return
        self._loading_topic_html = True
        try:
            editor._current_topic_id = item.data(ROLE_TOPIC_ID)
            editor.setHtml(item.data(ROLE_TOPIC_HTML) or self._default_document_html())
        finally:
            self._loading_topic_html = False
        self._update_status()
        self._sync_toolbar_state()

    def _title_from_path(self, path: str) -> str:
        return os.path.basename(path) if path else share.locales.tr('Unamed')

    def _current_tab_index(self) -> int:
        return self.tab_widget.currentIndex()

    def _editor_at(self, idx: int):
        if idx < 0 or idx >= self.tab_widget.count():
            return None
        w = self.tab_widget.widget(idx)
        return w if isinstance(w, QTextEdit) else None

    def _current_editor(self):
        return self._editor_at(self._current_tab_index())

    def _build_toc_from_headings(self, editor=None):
        if editor is None:
            editor = self._current_editor()
        self._loading_toc_model = True
        self.toc_model.clear()
        self.toc_model.setHorizontalHeaderLabels(['TOC'])
        if editor is None:
            self._loading_toc_model = False
            return

        root_items = [None, None, None, None, None]
        block = editor.document().firstBlock()
        found = False
        while block.isValid():
            txt = block.text().strip()
            if txt:
                level = self._toc_level_from_block(block)
                if level > 0:
                    item = self._new_topic_item(txt, self._default_document_html())
                    item.setData(block.position(), ROLE_BLOCK_POS)
                    if level <= 1 or root_items[level - 1] is None:
                        self.toc_model.appendRow(item)
                    else:
                        parent = root_items[level - 1]
                        parent.appendRow(item)
                    root_items[level] = item
                    for i in range(level + 1, len(root_items)):
                        root_items[i] = None
                    found = True
            block = block.next()

        if not found:
            self.toc_model.appendRow(self._new_topic_item('New Topic', editor.toHtml()))

        self.toc_view.expandAll()
        self._save_toc_to_current_editor()
        if self.toc_model.rowCount() > 0:
            item = self.toc_model.item(0)
            self.toc_view.setCurrentIndex(self.toc_model.indexFromItem(item))
            self._load_topic_into_editor(item)
        self._loading_toc_model = False

    def _toc_level_from_block(self, block):
        it = block.begin()
        while not it.atEnd():
            fragment = it.fragment()
            if fragment.isValid():
                fmt = fragment.charFormat()
                size = fmt.fontPointSize() or 0
                weight = fmt.fontWeight()
                if size >= 22:
                    return 1
                if size >= 18:
                    return 2
                if size >= 15:
                    return 3
                if size >= 13 and weight >= QFont.Bold:
                    return 4
            it += 1
        return 0

    def _add_editor_tab(self, html: str, file_path: str = '', toc_roots=None):
        editor = QTextEdit()
        editor.setAcceptRichText(True)
        editor.setHtml(html or self._default_document_html())
        editor._path = file_path or ''
        editor._dirty = False
        editor._toc_snapshot = toc_roots or []
        editor._current_topic_id = None
        editor.textChanged.connect(lambda ed=editor: self._on_editor_text_changed(ed))
        editor.cursorPositionChanged.connect(self._sync_toolbar_state)

        idx = self.tab_widget.addTab(editor, self._title_from_path(file_path))
        self.tab_widget.setCurrentIndex(idx)
        self._sync_current_editor_ref()
        if editor._toc_snapshot:
            self._load_toc_from_current_editor()
        else:
            self._build_toc_from_headings(editor)
        self._last_tab_index = self.tab_widget.currentIndex()
        return editor

    def _on_editor_text_changed(self, editor):
        if self._loading_topic_html:
            if editor is self._current_editor():
                self._sync_current_editor_ref()
                self._update_status()
            return
        self._set_editor_dirty(editor, True)
        if editor is self._current_editor():
            item = self._toc_current_item()
            if item is not None:
                item.setData(editor.toHtml(), ROLE_TOPIC_HTML)
                editor._current_topic_id = item.data(ROLE_TOPIC_ID)
                self._save_toc_to_current_editor()
            self._sync_current_editor_ref()
            self._update_window_title()
            self._update_status()
        self.contentChanged.emit()

    def _find_item_by_topic_id(self, topic_id, parent=None):
        if not topic_id:
            return None
        if parent is None:
            for row in range(self.toc_model.rowCount()):
                item = self.toc_model.item(row)
                res = self._find_item_by_topic_id(topic_id, item)
                if res is not None:
                    return res
            return None
        if parent.data(ROLE_TOPIC_ID) == topic_id:
            return parent
        for row in range(parent.rowCount()):
            res = self._find_item_by_topic_id(topic_id, parent.child(row))
            if res is not None:
                return res
        return None

    def _sync_toolbar_state(self):
        pass

    def _update_status(self):
        return

    def _on_toc_clicked(self, index):
        item = self.toc_model.itemFromIndex(index)
        if item is None:
            return
        self._load_topic_into_editor(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F2 and self.toc_view.hasFocus():
            idx = self.toc_view.currentIndex()
            if idx.isValid():
                self.toc_view.edit(idx)
                event.accept()
                return
        super().keyPressEvent(event)

    def _on_toc_item_changed(self, item):
        if self._loading_toc_model:
            return
        editor = self._current_editor()
        if editor is None:
            return
        self._set_editor_dirty(editor, True)
        self._save_toc_to_current_editor()
        self._update_window_title()

    def _on_toc_context_menu(self, pos):
        menu = QMenu(self)
        sub = menu.addMenu(share.locales.tr('New'))
        act_add_sub = sub.addAction(share.locales.tr('Add Sub Topic'))
        act_new_top = sub.addAction(share.locales.tr('New Topic'))
        sub.addSeparator()
        act_up    = sub.addAction(share.locales.tr('Move Up'))
        act_down  = sub.addAction(share.locales.tr('Move Down'))
        act_left  = sub.addAction(share.locales.tr('Move Left'))
        act_right = sub.addAction(share.locales.tr('Move Right'))

        menu.addSeparator()
        act_cut    = menu.addAction(share.locales.tr('Cut'))
        act_paste  = menu.addAction(share.locales.tr('Paste'))
        act_delete = menu.addAction(share.locales.tr('Delete'))
        menu.addSeparator()
        act_html   = menu.addAction(share.locales.tr("HTML"))

        act = menu.exec_(self.toc_view.viewport().mapToGlobal(pos))
        if act == act_add_sub:
            self._toc_add_sub_topic()
        elif act == act_new_top:
            self._toc_new_topic()
        elif act == act_up:
            self._toc_move_up()
        elif act == act_down:
            self._toc_move_down()
        elif act == act_left:
            self._toc_move_left()
        elif act == act_right:
            self._toc_move_right()
        elif act == act_cut:
            self._toc_cut()
        elif act == act_paste:
            self._toc_paste()
        elif act == act_delete:
            self._toc_delete()
        elif act == act_html:
            self.edit_html_source()

    def _seed_toc(self):
        item = self._new_topic_item("New Topic", self._default_document_html())
        self.toc_model.appendRow(item)
        self.toc_view.setCurrentIndex(self.toc_model.indexFromItem(item))

    def _mark_dirty(self):
        self._is_dirty = True
        self.contentChanged.emit()

    def _merge_char_format(self, fmt):
        cursor = (self._current_editor() or self.editor).textCursor()
        if not cursor.hasSelection():
            (self._current_editor() or self.editor).mergeCurrentCharFormat(fmt)
        else:
            cursor.mergeCharFormat(fmt)
            (self._current_editor() or self.editor).mergeCurrentCharFormat(fmt)
        (self._current_editor() or self.editor).setFocus()

    def _dock_toggle_bold(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if checked else QFont.Normal)
        self._merge_char_format(fmt)

    def _dock_toggle_italic(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self._merge_char_format(fmt)

    def _dock_toggle_underline(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self._merge_char_format(fmt)

    def _dock_toggle_strike(self, checked):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(checked)
        self._merge_char_format(fmt)

    def set_font_family(self, font):
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self._merge_char_format(fmt)

    def set_font_size_from_text(self, text):
        try:
            size = float(text.replace(",", "."))
        except Exception:
            return
        if size <= 0:
            return
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self._merge_char_format(fmt)

    def set_text_color(self):
        color = QColorDialog.getColor(QColor("#ffffff"), self, "Text Color")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self._merge_char_format(fmt)

    def set_background_color(self):
        color = QColorDialog.getColor(QColor("#000000"), self, "BG Color")
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self._merge_char_format(fmt)

    def _on_align_combo_activated(self, idx):
        mapping = {
            0: Qt.AlignLeft,
            1: Qt.AlignHCenter,
            2: Qt.AlignRight,
            3: Qt.AlignJustify,
        }
        self._apply_alignment(mapping.get(idx, Qt.AlignLeft))

    def _apply_alignment(self, align):
        cursor = (self._current_editor() or self.editor).textCursor()
        block_fmt = cursor.blockFormat()
        block_fmt.setAlignment(align)
        cursor.mergeBlockFormat(block_fmt)
        (self._current_editor() or self.editor).setTextCursor(cursor)
        (self._current_editor() or self.editor).setFocus()

    def _on_bullet_combo_activated(self, idx):
        mapping = {
            0: QTextListFormat.ListDisc,
            1: QTextListFormat.ListCircle,
            2: QTextListFormat.ListSquare,
        }
        (self._current_editor() or self.editor).textCursor().insertList(mapping.get(idx, QTextListFormat.ListDisc))

    def _on_number_combo_activated(self, idx):
        mapping = {
            0: QTextListFormat.ListDecimal,
            1: QTextListFormat.ListLowerAlpha,
            2: QTextListFormat.ListUpperAlpha,
            3: QTextListFormat.ListLowerRoman,
            4: QTextListFormat.ListUpperRoman,
        }
        (self._current_editor() or self.editor).textCursor().insertList(mapping.get(idx, QTextListFormat.ListDecimal))

    def pick_resource_path(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Resource", "", "All Files (*.*)")
        if path:
            self.link_edit.setText(path)

    def insert_link_from_tab(self):
        raw = self.link_edit.text().strip()
        if not raw:
            return
        href = raw if "://" in raw else "file:///" + raw.replace("\\", "/")
        cursor = (self._current_editor() or self.editor).textCursor()
        text = cursor.selectedText() or raw
        cursor.insertHtml(f'<a href="{href}">{text}</a>')

    def insert_mail_from_tab(self):
        raw = self.link_edit.text().strip()
        if not raw:
            return
        href = raw if raw.lower().startswith("mailto:") else "mailto:" + raw
        cursor = (self._current_editor() or self.editor).textCursor()
        text = cursor.selectedText() or raw
        cursor.insertHtml(f'<a href="{href}">{text}</a>')

    def insert_image_from_tab(self):
        raw = self.link_edit.text().strip()
        if not raw:
            return
        src = raw.replace("\\", "/")
        (self._current_editor() or self.editor).textCursor().insertHtml(f'<img src="{src}" alt="" />')

    def insert_anchor_from_tab(self):
        raw = self.link_edit.text().strip()
        if not raw:
            return
        anchor = raw.replace(" ", "_")
        (self._current_editor() or self.editor).textCursor().insertHtml(f'<a id="{anchor}" name="{anchor}"></a>')

    def insert_table(self):
        editor = self._current_editor()
        dlg = TableInsertDialog(self)
        if editor is None:
            return
        if dlg.exec_() != QDialog.Accepted:
            return
        values  = dlg.spec()
        rows    = values.rows
        cols    = values.cols
        border  = values.border
        padding = values.cell_padding
        html    = [f'<table border="{border}" cellpadding="{padding}" cellspacing="0" style="border-collapse:collapse; width:100%;">']
        for _ in range(rows):
            html.append("<tr>")
            for _ in range(cols):
                html.append("<td>&nbsp;</td>")
            html.append("</tr>")
        html.append("</table>")
        (self._current_editor() or self.editor).textCursor().insertHtml("".join(html))

    def _on_table_ops_combo_activated(self, idx):
        handlers = {
            0: self.table_add_row,
            1: self.table_add_column,
            2: self.table_remove_row,
            3: self.table_remove_column,
            4: self.table_merge_cells,
        }
        handler = handlers.get(idx)
        if handler:
            handler()

    def _current_table(self):
        cursor = (self._current_editor() or self.editor).textCursor()
        return cursor.currentTable()

    def table_add_row(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt((self._current_editor() or self.editor).textCursor())
        table.insertRows(cell.row() + 1, 1)

    def table_add_column(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt((self._current_editor() or self.editor).textCursor())
        table.insertColumns(cell.column() + 1, 1)

    def table_remove_row(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt((self._current_editor() or self.editor).textCursor())
        table.removeRows(cell.row(), 1)

    def table_remove_column(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt((self._current_editor() or self.editor).textCursor())
        table.removeColumns(cell.column(), 1)

    def table_merge_cells(self):
        table = self._current_table()
        if table is None:
            return
        cursor = (self._current_editor() or self.editor).textCursor()
        try:
            table.mergeCells(cursor)
        except Exception:
            cell = table.cellAt(cursor)
            row_span = max(1, self._safe_int(self.edit_cell_rowspan, 1))
            col_span = max(1, self._safe_int(self.edit_cell_colspan, 1))
            table.mergeCells(cell.row(), cell.column(), row_span, col_span)

    def table_set_cell_background(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt((self._current_editor() or self.editor).textCursor())
        if not cell.isValid():
            return
        color = QColorDialog.getColor(QColor("#ffffff"), self, "Cell Color")
        if not color.isValid():
            return
        fmt = cell.format()
        fmt.setBackground(color)
        cell.setFormat(fmt)

    def _safe_int(self, edit, default=0):
        try:
            return int(float((edit.text() or "").replace(",", ".")))
        except Exception:
            return default

    def show_html_debug(self):
        QMessageBox.information(self, "HTML", (self._current_editor() or self.editor).toHtml()[:4000])

    def _default_document_html(self):
        return """<!DOCTYPE html>
<html>
<head>
<meta charset=\"utf-8\">
<title>Help Authoring</title>
</head>
<body>
<h1>Neue Hilfe-Seite</h1>
<p>Hier kann dein Hilfetext bearbeitet werden.</p>
</body>
</html>"""


def run_standalone():
    app = QApplication(sys.argv)
    w = HelpAuthoringEditor()
    w.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(run_standalone())
