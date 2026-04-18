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

from   dataclasses  import dataclass
from   share.common import *

ROLE_BLOCK_POS  = Qt.UserRole
ROLE_TOPIC_HTML = Qt.UserRole + 1
ROLE_TOPIC_ID   = Qt.UserRole + 2

@dataclass
class TableSpec:
    rows: int = 2
    cols: int = 2
    border: int = 1
    cell_padding: int = 4
    cell_spacing: int = 0
    width_percent: int = 100

class TableInsertDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Tabelle einfügen')
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

        form.addRow('Zeilen:'       , self.spin_rows)
        form.addRow('Spalten:'      , self.spin_cols)
        form.addRow('Rahmen:'       , self.spin_border)
        form.addRow('Innenabstand:' , self.spin_padding)
        form.addRow('Zellenabstand:', self.spin_spacing)
        form.addRow('Breite %:'     , self.spin_width)
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
        self.setWindowTitle('HTML-Quelltext')
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
        self.setWindowTitle('Link-Typ wählen')
        self.resize(280, 120)

        lay = QVBoxLayout(self)
        self.rb_http = QRadioButton('HTTP-Adresse')
        self.rb_mail = QRadioButton('E-Mail-Adresse')
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

    def __init__(self, parent=None, initial_html: str = '', file_path: str = ''):
        super().__init__(parent)
        self.current_path = file_path or ''
        self._is_dirty = False
        self._loading_topic_html = False
        self._loading_toc_model  = False
        self._last_tab_index     = -1
        self.setWindowTitle('Help Authoring')
        self.resize(800, 620)

        self.editor = None
        self.toc_model = QStandardItemModel()
        self.toc_model.setHorizontalHeaderLabels(['TOC'])
        self.toc_model.itemChanged.connect(self._on_toc_item_changed)
        self.toc_view = QTreeView()
        self.toc_view.setModel(self.toc_model)
        self.toc_view.setHeaderHidden(False)
        self.toc_view.clicked.connect(self._on_toc_clicked)
        self.toc_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.toc_view.customContextMenuRequested.connect(self._on_toc_context_menu)
        self.toc_view.setEditTriggers(QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked | QAbstractItemView.DoubleClicked)
        toc_font = self.toc_view.font()
        toc_font.setPointSize(10)
        self.toc_view.setFont(toc_font)
        self.toc_view.setStyleSheet(
            'QTreeView { font-size: 10pt; } '
            'QTreeView::item { padding: 0px; margin: 0px; } '
            'QTreeView QLineEdit { padding: 1px; margin: 0px; font-size: 10pt; }'
        )
        self._toc_clipboard_item = None

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.tab_widget.tabCloseRequested.connect(self._on_tab_close_requested)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.toc_view)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([760, 240])

        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.splitter)
        self.setCentralWidget(central)

        self._build_format_dock()
        self._build_toolbar()
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.lbl_status = QLabel('Bereit')
        sb.addPermanentWidget(self.lbl_status)

        self._settings = QSettings(self._ini_path(), QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

        if initial_html:
            roots = [self._new_topic_item('New Topic', initial_html)]
            self._add_editor_tab('', file_path, roots)
        else:
            self.file_new()

        self._sync_toolbar_state()
        self._update_window_title()
        self._update_status()
        self._restore_window_state()

    def _build_format_dock(self):
        self.format_dock = QDockWidget('Format-Hilfe', self)
        self.format_dock.setObjectName('HelpFormatDock')
        self.format_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        dock_host = QWidget()
        dock_lay = QVBoxLayout(dock_host)
        dock_lay.setContentsMargins(4, 4, 4, 4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        form = QVBoxLayout(scroll_content)
        form.setContentsMargins(4, 4, 4, 4)
        form.setSpacing(6)

        row1 = QHBoxLayout()
        self.btn_bold = QPushButton('F'); self.btn_bold.setCheckable(True)
        self.btn_italic = QPushButton('K'); self.btn_italic.setCheckable(True)
        self.btn_underline = QPushButton('U'); self.btn_underline.setCheckable(True)
        self.btn_strike = QPushButton('S'); self.btn_strike.setCheckable(True)
        for btn in [self.btn_bold, self.btn_italic, self.btn_underline, self.btn_strike]:
            btn.setMinimumWidth(36)
            row1.addWidget(btn)
        form.addLayout(row1)

        row2 = QHBoxLayout()
        self.dock_font_combo = QFontComboBox()
        self.dock_size_combo = QComboBox()
        for s in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]:
            self.dock_size_combo.addItem(str(s))
        self.dock_size_combo.setEditable(True)
        self.dock_size_combo.setCurrentText('11')
        row2.addWidget(self.dock_font_combo, 1)
        row2.addWidget(self.dock_size_combo, 0)
        form.addLayout(row2)

        row3 = QHBoxLayout()
        self.btn_text_color = QPushButton('Textfarbe')
        self.btn_bg_color = QPushButton('HG-Farbe')
        row3.addWidget(self.btn_text_color)
        row3.addWidget(self.btn_bg_color)
        form.addLayout(row3)

        self.align_combo = QComboBox()
        self.align_combo.addItems(['Links', 'Zentriert', 'Rechts', 'Blocksatz'])
        form.addWidget(self.align_combo)

        row5 = QHBoxLayout()
        self.bullet_combo = QComboBox()
        self.bullet_combo.addItems(['Liste: Disc', 'Liste: Circle', 'Liste: Square'])
        self.number_combo = QComboBox()
        self.number_combo.addItems(['Nummeriert: Decimal', 'Nummeriert: lower-alpha', 'Nummeriert: upper-alpha', 'Nummeriert: lower-roman', 'Nummeriert: upper-roman'])
        row5.addWidget(self.bullet_combo)
        row5.addWidget(self.number_combo)
        form.addLayout(row5)

        row6 = QHBoxLayout()
        self.link_edit = QLineEdit()
        self.link_edit.setPlaceholderText('Link oder E-Mail eingeben ...')
        self.btn_link_mode = QPushButton('...')
        self.btn_link_mode.setMaximumWidth(36)
        self.btn_insert_image = QPushButton('Bild')
        row6.addWidget(self.link_edit, 1)
        row6.addWidget(self.btn_link_mode, 0)
        row6.addWidget(self.btn_insert_image, 0)
        form.addLayout(row6)

        row7 = QHBoxLayout()
        self.btn_insert_table = QPushButton('Tabelle')
        self.table_ops_combo = ActionComboBox()
        self.table_ops_combo.addItems(['+ Zeile', '+ Spalte', '- Zeile', '- Spalte', 'Verbinden', 'Teilen'])
        row7.addWidget(self.btn_insert_table)
        row7.addWidget(self.table_ops_combo, 1)
        form.addLayout(row7)

        self.btn_table_cell_color = QPushButton('Zellfarbe')
        form.addWidget(self.btn_table_cell_color)

        row8 = QHBoxLayout()
        self.btn_table_margins = QPushButton('Tabellenrand')
        self.edit_margin_left = QLineEdit(); self.edit_margin_left.setPlaceholderText('Left')
        self.edit_margin_top = QLineEdit(); self.edit_margin_top.setPlaceholderText('Top')
        self.edit_margin_right = QLineEdit(); self.edit_margin_right.setPlaceholderText('Right')
        self.edit_margin_bottom = QLineEdit(); self.edit_margin_bottom.setPlaceholderText('Bottom')
        row8.addWidget(self.btn_table_margins)
        row8.addWidget(self.edit_margin_left)
        row8.addWidget(self.edit_margin_top)
        row8.addWidget(self.edit_margin_right)
        row8.addWidget(self.edit_margin_bottom)
        form.addLayout(row8)

        row9 = QHBoxLayout()
        self.btn_table_cell_size = QPushButton('Zellgröße')
        self.edit_cell_width = QLineEdit(); self.edit_cell_width.setPlaceholderText('Breite')
        self.edit_cell_height = QLineEdit(); self.edit_cell_height.setPlaceholderText('Höhe')
        self.edit_cell_colspan = QLineEdit(); self.edit_cell_colspan.setPlaceholderText('ColSpan')
        self.edit_cell_rowspan = QLineEdit(); self.edit_cell_rowspan.setPlaceholderText('RowSpan')
        row9.addWidget(self.btn_table_cell_size)
        row9.addWidget(self.edit_cell_width)
        row9.addWidget(self.edit_cell_height)
        row9.addWidget(self.edit_cell_colspan)
        row9.addWidget(self.edit_cell_rowspan)
        form.addLayout(row9)

        form.addStretch(1)
        scroll.setWidget(scroll_content)
        dock_lay.addWidget(scroll)
        self.format_dock.setWidget(dock_host)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.format_dock)

        self.btn_bold.toggled.connect(self._dock_toggle_bold)
        self.btn_italic.toggled.connect(self._dock_toggle_italic)
        self.btn_underline.toggled.connect(self._dock_toggle_underline)
        self.btn_strike.toggled.connect(self._dock_toggle_strike)
        self.dock_font_combo.currentFontChanged.connect(self.set_font_family)
        self.dock_size_combo.currentTextChanged.connect(self.set_font_size_from_text)
        self.btn_text_color.clicked.connect(self.set_text_color)
        self.btn_bg_color.clicked.connect(self.set_background_color)
        self.align_combo.currentTextChanged.connect(self._on_align_combo_changed)
        self.bullet_combo.activated.connect(self._on_bullet_combo_activated)
        self.number_combo.activated.connect(self._on_number_combo_activated)
        self.btn_link_mode.clicked.connect(self._insert_link_from_dock)
        self.btn_insert_image.clicked.connect(self.insert_image)
        self.btn_insert_table.clicked.connect(self.insert_table)
        self.table_ops_combo.doubleClicked.connect(self._on_table_ops_combo_double_clicked)
        self.btn_table_cell_color.clicked.connect(self.table_set_cell_background)
        self.btn_table_margins.clicked.connect(self._apply_table_margins_from_dock)
        self.btn_table_cell_size.clicked.connect(self._apply_table_cell_size_from_dock)

        self.format_dock.setStyleSheet("""
            QDockWidget { color:#ffd84d; font: 9pt Arial; }
            QDockWidget::title { text-align:left; background:#1a1a1a; color:#ffd84d; padding:4px; font: 9pt Arial; }
            QWidget { background:#131313; color:white; }
            QPushButton { background:#1a1a1a; color:#ffd84d; border:1px solid #3a3a3a; padding:4px 8px; font: 9pt Arial; }
            QPushButton:checked { background:#2a2a2a; }
            QComboBox, QLineEdit, QFontComboBox {
                background:#1b1b1b; color:white; border:1px solid #3a3a3a; min-height:24px; font: 9pt Arial;
            }
            QScrollArea { border:none; }
        """)

    def _build_toolbar(self):
        self.tb_file = QToolBar('Datei', self)
        self.tb_file.setObjectName('FileToolBar')
        self.tb_file.setIconSize(QSize(16, 16))
        self.addToolBar(self.tb_file)

        act_new     = QAction('Neu'               , self); act_new    .triggered.connect(self.file_new)
        act_open    = QAction('Öffnen'            , self); act_open   .triggered.connect(self.file_open)
        act_save    = QAction('Speichern'         , self); act_save   .triggered.connect(lambda _=False: self.file_save())
        act_save_as = QAction('Speichern unter...', self); act_save_as.triggered.connect(lambda _=False: self.file_save_as())
        act_source  = QAction('HTML'              , self); act_source .triggered.connect(self.edit_html_source)

        self.tb_file.addAction(act_new)
        self.tb_file.addAction(act_open)
        self.tb_file.addAction(act_save)
        self.tb_file.addAction(act_save_as)
        self.tb_file.addSeparator()
        self.tb_file.addAction(act_source)

        self.tb_fmt = QToolBar('Format', self)
        self.tb_fmt.setObjectName('FormatToolBar')
        self.addToolBar(self.tb_fmt)

        self.act_bold      = QAction('F', self); self.act_bold     .setCheckable(True); self.act_bold     .triggered.connect(self.toggle_bold)
        self.act_italic    = QAction('K', self); self.act_italic   .setCheckable(True); self.act_italic   .triggered.connect(self.toggle_italic)
        self.act_underline = QAction('U', self); self.act_underline.setCheckable(True); self.act_underline.triggered.connect(self.toggle_underline)
        self.act_strike    = QAction('S', self); self.act_strike   .setCheckable(True); self.act_strike   .triggered.connect(self.toggle_strike)

        self.tb_fmt.addAction(self.act_bold)
        self.tb_fmt.addAction(self.act_italic)
        self.tb_fmt.addAction(self.act_underline)
        self.tb_fmt.addAction(self.act_strike)
        self.tb_fmt.addSeparator()

        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.set_font_family)
        self.tb_fmt.addWidget(self.font_combo)

        self.size_combo = QComboBox()
        for s in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]:
            self.size_combo.addItem(str(s))
            
        self.size_combo.setEditable(True)
        self.size_combo.setCurrentText('11')
        self.size_combo.currentTextChanged.connect(self.set_font_size_from_text)
        self.tb_fmt.addWidget(self.size_combo)

        self.heading_combo = QComboBox()
        self.heading_combo.addItems(['Normal', 'H1', 'H2', 'H3', 'H4', 'Code'])
        self.heading_combo.currentTextChanged.connect(self.apply_heading_style)
        self.tb_fmt.addWidget(self.heading_combo)

        act_fg = QAction('Textfarbe', self); act_fg.triggered.connect(self.set_text_color)
        act_bg = QAction('Marker', self); act_bg.triggered.connect(self.set_background_color)
        self.tb_fmt.addAction(act_fg)
        self.tb_fmt.addAction(act_bg)

        self.tb_para = QToolBar('Absatz', self)
        self.tb_para.setObjectName('ParagraphToolBar')
        self.addToolBar(self.tb_para)
        for title, align in [('Links', Qt.AlignLeft), ('Zentriert', Qt.AlignHCenter), ('Rechts', Qt.AlignRight), ('Blocksatz', Qt.AlignJustify)]:
            act = QAction(title, self)
            act.triggered.connect(lambda _=False, a=align: self._apply_alignment(a))
            self.tb_para.addAction(act)

        act_bullets = QAction('Liste'         , self); act_bullets.triggered.connect(self.insert_bullet_list)
        act_numbers = QAction('Nummeriert'    , self); act_numbers.triggered.connect(self.insert_numbered_list)
        act_link    = QAction('Link'          , self); act_link   .triggered.connect(self.insert_link)
        act_unlink  = QAction('Link entfernen', self); act_unlink .triggered.connect(self.remove_link)
        act_image   = QAction('Bild'          , self); act_image  .triggered.connect(self.insert_image)

        self.tb_para.addSeparator()
        self.tb_para.addAction(act_bullets)
        self.tb_para.addAction(act_numbers)
        self.tb_para.addSeparator()
        self.tb_para.addAction(act_link)
        self.tb_para.addAction(act_unlink)
        self.tb_para.addAction(act_image)

        self.tb_table = QToolBar('Tabelle', self)
        self.tb_table.setObjectName('TableToolBar')
        self.addToolBar(self.tb_table)
        entries = [
            ('Tabelle', self.insert_table),
            ('+ Zeile', self.table_add_row),
            ('+ Spalte', self.table_add_column),
            ('- Zeile', self.table_remove_row),
            ('- Spalte', self.table_remove_column),
            ('Verbinden', self.table_merge_cells),
            ('Teilen', self.table_split_cell),
            ('Zellfarbe', self.table_set_cell_background),
        ]
        for title, fn in entries:
            act = QAction(title, self); act.triggered.connect(fn); self.tb_table.addAction(act)

        self.setStyleSheet(self.styleSheet() + """
            QToolBar QToolButton {
                color: #ffd84d;
                font-size: 10pt;
                font-weight: normal;
            }
            QToolBar#FileToolBar QToolButton {
                color: #ffd84d;
                font-size: 10pt;
                font-weight: bold;
            }
        """)

        self.tb_fmt.hide()
        self.tb_para.hide()
        self.tb_table.hide()

    def _dock_toggle_bold(self, checked):
        self.act_bold.setChecked(checked)
        self.toggle_bold()

    def _dock_toggle_italic(self, checked):
        self.act_italic.setChecked(checked)
        self.toggle_italic()

    def _dock_toggle_underline(self, checked):
        self.act_underline.setChecked(checked)
        self.toggle_underline()

    def _dock_toggle_strike(self, checked):
        self.act_strike.setChecked(checked)
        self.toggle_strike()

    def _on_align_combo_changed(self, text):
        mapping = {
            'Links': Qt.AlignLeft,
            'Zentriert': Qt.AlignHCenter,
            'Rechts': Qt.AlignRight,
            'Blocksatz': Qt.AlignJustify,
        }
        if text in mapping:
            self._apply_alignment(mapping[text])

    def _on_bullet_combo_activated(self, idx):
        mapping = {
            0: QTextListFormat.ListDisc,
            1: QTextListFormat.ListCircle,
            2: QTextListFormat.ListSquare,
        }
        editor = self._current_editor()
        if editor is not None:
            editor.textCursor().insertList(mapping.get(idx, QTextListFormat.ListDisc))

    def _on_number_combo_activated(self, idx):
        mapping = {
            0: QTextListFormat.ListDecimal,
            1: QTextListFormat.ListLowerAlpha,
            2: QTextListFormat.ListUpperAlpha,
            3: QTextListFormat.ListLowerRoman,
            4: QTextListFormat.ListUpperRoman,
        }
        editor = self._current_editor()
        if editor is not None:
            editor.textCursor().insertList(mapping.get(idx, QTextListFormat.ListDecimal))

    def _insert_link_from_dock(self):
        editor = self._current_editor()
        if editor is None:
            return
        raw = self.link_edit.text().strip()
        if not raw:
            QMessageBox.information(self, 'Link', 'Bitte zuerst einen Link oder eine E-Mail-Adresse eingeben.')
            return
        dlg = LinkTypeDialog(self)
        if dlg.exec_() != QDialog.Accepted:
            return
        link_type = dlg.link_type()
        href = raw
        if link_type == 'mail':
            if not href.lower().startswith('mailto:'):
                href = 'mailto:' + href
        else:
            if '://' not in href:
                href = 'https://' + href
        cursor = editor.textCursor()
        selected_text = cursor.selectedText() or raw
        cursor.insertHtml(f'<a href="{href}">{selected_text}</a>')

    def _on_table_ops_combo_double_clicked(self):
        txt = self.table_ops_combo.currentText()
        if txt == '+ Zeile':
            self.table_add_row()
        elif txt == '+ Spalte':
            self.table_add_column()
        elif txt == '- Zeile':
            self.table_remove_row()
        elif txt == '- Spalte':
            self.table_remove_column()
        elif txt == 'Verbinden':
            self.table_merge_cells()
        elif txt == 'Teilen':
            self.table_split_cell()

    def _safe_float(self, edit, default=0.0):
        try:
            return float((edit.text() or '').replace(',', '.'))
        except Exception:
            return default

    def _safe_int(self, edit, default=0):
        try:
            return int(float((edit.text() or '').replace(',', '.')))
        except Exception:
            return default

    def _apply_table_margins_from_dock(self):
        table = self._current_table()
        if table is None:
            return
        fmt = table.format()
        fmt.setLeftMargin(self._safe_float(self.edit_margin_left, fmt.leftMargin()))
        fmt.setTopMargin(self._safe_float(self.edit_margin_top, fmt.topMargin()))
        fmt.setRightMargin(self._safe_float(self.edit_margin_right, fmt.rightMargin()))
        fmt.setBottomMargin(self._safe_float(self.edit_margin_bottom, fmt.bottomMargin()))
        table.setFormat(fmt)

    def _apply_table_cell_size_from_dock(self):
        editor = self._current_editor()
        table = self._current_table()
        if editor is None or table is None:
            return
        cell = table.cellAt(editor.textCursor())
        if not cell.isValid():
            return
        col_w = self._safe_int(self.edit_cell_width, 0)
        row_h = self._safe_int(self.edit_cell_height, 0)
        col_span = max(1, self._safe_int(self.edit_cell_colspan, 1))
        row_span = max(1, self._safe_int(self.edit_cell_rowspan, 1))

        if col_w > 0:
            fmt = table.format()
            constraints = list(fmt.columnWidthConstraints())
            while len(constraints) < table.columns():
                constraints.append(QTextLength(QTextLength.PercentageLength, 100.0 / max(1, table.columns())))
            constraints[cell.column()] = QTextLength(QTextLength.FixedLength, col_w)
            fmt.setColumnWidthConstraints(constraints)
            table.setFormat(fmt)

        if row_h > 0:
            cursor = editor.textCursor()
            block_fmt = QTextBlockFormat()
            block_fmt.setLineHeight(row_h, QTextBlockFormat.FixedHeight)
            cursor.mergeBlockFormat(block_fmt)

        if col_span > 1 or row_span > 1:
            try:
                table.mergeCells(cell.row(), cell.column(), row_span, col_span)
            except Exception:
                pass

    def _ini_path(self) -> str:
        try:
            base = os.path.dirname(os.path.abspath(sys.argv[0]))
        except Exception:
            base = os.getcwd()
        return os.path.join(base, 'dBaseRunner.ini')

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

    def _default_document_html(self) -> str:
        return '''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Help Authoring</title>
<style>
body { font-family: Arial, sans-serif; font-size: 11pt; }
table { border-collapse: collapse; width: 100%; }
td, th { border: 1px solid #666; padding: 4px; }
</style>
</head>
<body>
<h1>Neue Hilfe-Seite</h1>
<p>Hier kann dein Hilfetext bearbeitet werden.</p>
</body>
</html>'''

    def _title_from_path(self, path: str) -> str:
        return os.path.basename(path) if path else 'Unbenannt'

    def _current_tab_index(self) -> int:
        return self.tab_widget.currentIndex()

    def _editor_at(self, idx: int):
        if idx < 0 or idx >= self.tab_widget.count():
            return None
        w = self.tab_widget.widget(idx)
        return w if isinstance(w, QTextEdit) else None

    def _current_editor(self):
        return self._editor_at(self._current_tab_index())

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

    def _new_topic_item(self, title='New Topic', html=''):
        item = QStandardItem(title)
        item.setData(None, Qt.UserRole)
        item.setData(html or self._default_document_html(), ROLE_TOPIC_HTML)
        item.setData(str(uuid.uuid4()), ROLE_TOPIC_ID)
        return item

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

    def _on_toc_item_changed(self, item):
        if self._loading_toc_model:
            return
        editor = self._current_editor()
        if editor is None:
            return
        self._set_editor_dirty(editor, True)
        self._save_toc_to_current_editor()
        self._update_window_title()

    def _serialize_item(self, item):
        data = {
            'title'    : item.text(),
            'topic_id' : item.data(ROLE_TOPIC_ID),
            'html'     : item.data(ROLE_TOPIC_HTML) or '',
            'children' : [],
        }
        for row in range(item.rowCount()):
            child = item.child(row)
            if child is not None:
                data['children'].append(self._serialize_item(child))
        return data

    def _deserialize_item(self, data):
        item = QStandardItem(data.get('title', 'Topic'))
        item.setData(None, Qt.UserRole)
        item.setData(data.get('html', self._default_document_html()), ROLE_TOPIC_HTML)
        item.setData(data.get('topic_id', str(uuid.uuid4())), ROLE_TOPIC_ID)
        for child in data.get('children', []):
            item.appendRow(self._deserialize_item(child))
        return item

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

    def _on_tab_changed(self, idx: int):
        old_editor = self._editor_at(self._last_tab_index)
        if old_editor is not None and old_editor is self.editor:
            self._capture_current_project_to_editor(old_editor)
        self._sync_current_editor_ref()
        self._sync_toolbar_state()
        self._update_status()
        self._update_window_title()
        self._load_toc_from_current_editor()
        self._last_tab_index = idx

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

    def _apply_alignment(self, align):
        if self.editor is None:
            return
        self.editor.setAlignment(align)

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

    def _toc_current_item(self):
        idx = self.toc_view.currentIndex()
        if not idx.isValid():
            return None
        return self.toc_model.itemFromIndex(idx)

    def _toc_select_item(self, item):
        if item is None:
            return
        idx = self.toc_model.indexFromItem(item)
        if idx.isValid():
            self.toc_view.setCurrentIndex(idx)
            self.toc_view.scrollTo(idx)
            self._load_topic_into_editor(item)

    def _toc_new_topic(self):
        item = self._toc_current_item()
        new_item = self._new_topic_item('New Topic', self._default_document_html())
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
        new_item = self._new_topic_item('Child Topic', self._default_document_html())
        if item is None:
            self.toc_model.appendRow(new_item)
        else:
            item.appendRow(new_item)
            self.toc_view.expand(self.toc_model.indexFromItem(item))
        self._save_toc_to_current_editor()
        self._toc_select_item(new_item)
        self.toc_view.edit(self.toc_model.indexFromItem(new_item))

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

    def _on_toc_context_menu(self, pos):
        menu = QMenu(self)
        sub = menu.addMenu('New')
        act_add_sub = sub.addAction('Add Sub Topic')
        act_new_top = sub.addAction('New Topic')
        sub.addSeparator()
        act_up = sub.addAction('Move Up')
        act_down = sub.addAction('Move Down')
        act_left = sub.addAction('Move Left')
        act_right = sub.addAction('Move Right')

        menu.addSeparator()
        act_cut = menu.addAction('Cut')
        act_paste = menu.addAction('Paste')
        act_delete = menu.addAction('Delete')

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

    def _on_toc_clicked(self, index):
        item = self.toc_model.itemFromIndex(index)
        if item is None:
            return
        self._load_topic_into_editor(item)

    def _update_window_title(self):
        editor = self._current_editor()
        if editor is None:
            self.setWindowTitle('Help Authoring')
            return
        name = self._title_from_path(getattr(editor, '_path', ''))
        star = ' *' if getattr(editor, '_dirty', False) else ''
        self.current_path = getattr(editor, '_path', '')
        self.setWindowTitle(f'Help Authoring - {name}{star}')

    def _update_status(self):
        editor = self._current_editor()
        if editor is None:
            self.lbl_status.setText('Bereit')
            return
        plain = editor.toPlainText()
        words = len([w for w in plain.split() if w.strip()])
        chars = len(plain)
        self.lbl_status.setText(f'Wörter: {words} | Zeichen: {chars}')

    def _sync_toolbar_state(self):
        editor = self._current_editor()
        if editor is None:
            return

        fmt = editor.currentCharFormat()
        self.act_bold.setChecked(fmt.fontWeight() >= QFont.Bold)
        self.act_italic.setChecked(fmt.fontItalic())
        self.act_underline.setChecked(fmt.fontUnderline())
        self.act_strike.setChecked(fmt.fontStrikeOut())

        font = fmt.font()
        if font.family():
            self.font_combo.blockSignals(True)
            self.font_combo.setCurrentFont(font)
            self.font_combo.blockSignals(False)

        size = int(fmt.fontPointSize() or 11)
        self.size_combo.blockSignals(True)
        self.size_combo.setCurrentText(str(size))
        self.size_combo.blockSignals(False)

        if hasattr(self, 'btn_bold'):
            self.btn_bold.blockSignals(True); self.btn_bold.setChecked(self.act_bold.isChecked()); self.btn_bold.blockSignals(False)
            self.btn_italic.blockSignals(True); self.btn_italic.setChecked(self.act_italic.isChecked()); self.btn_italic.blockSignals(False)
            self.btn_underline.blockSignals(True); self.btn_underline.setChecked(self.act_underline.isChecked()); self.btn_underline.blockSignals(False)
            self.btn_strike.blockSignals(True); self.btn_strike.setChecked(self.act_strike.isChecked()); self.btn_strike.blockSignals(False)
            self.dock_font_combo.blockSignals(True); self.dock_font_combo.setCurrentFont(font); self.dock_font_combo.blockSignals(False)
            self.dock_size_combo.blockSignals(True); self.dock_size_combo.setCurrentText(str(size)); self.dock_size_combo.blockSignals(False)

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

    def file_new(self):
        roots = [self._new_topic_item('New Topic', self._default_document_html())]
        editor = self._add_editor_tab('', '', roots)
        self._set_editor_dirty(editor, False)
        self._sync_current_editor_ref()
        self._update_window_title()
        self._update_status()
        self._load_toc_from_current_editor()

    def file_open(self):
        paths, _ = QFileDialog.getOpenFileNames(self,
            'Datei öffnen', '',
            'Help Authoring (*.json);;HTML Dateien (*.html *.htm);;Alle Dateien (*.*)')
        if not paths:
            return
        for path in paths:
            try:
                ext = os.path.splitext(path)[1].lower()
                if ext == '.json':
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        data = json.load(f)
                    topics = data.get('topics', [])
                    roots = [self._deserialize_item(item) for item in topics]
                    editor = self._add_editor_tab('', path, roots)
                else:
                    with open(path, 'r', encoding='utf-8', errors='replace') as f:
                        html = f.read()
                    roots = [self._new_topic_item(os.path.splitext(os.path.basename(path))[0], html)]
                    editor = self._add_editor_tab('', path, roots)
                self._set_editor_dirty(editor, False)
            except Exception as e:
                QMessageBox.warning(self,
                    'Öffnen',
                    f'Datei konnte nicht gelesen werden:\n{e}')
        self._sync_current_editor_ref()
        self._update_window_title()
        self._update_status()
        self._load_toc_from_current_editor()

    def file_save(self, editor=None) -> bool:
        if isinstance(editor, bool):
            editor = None
        if editor is None:
            editor = self._current_editor()
        if editor is None:
            return False
        if not getattr(editor, '_path', ''):
            return self.file_save_as(editor)
        try:
            if editor is self._current_editor():
                self._capture_current_project_to_editor(editor)
            topics = []
            for item in getattr(editor, '_toc_snapshot', []) or []:
                topics.append(self._serialize_item(item))
            payload = {
                'meta': {
                    'format'          : 'dBase2Many Help Authoring',
                    'version'         : 1,
                    'current_topic_id': getattr(editor, '_current_topic_id', None),
                },
                'topics': topics,
            }
            with open(editor._path, 'w', encoding='utf-8', errors='replace') as f:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            self._set_editor_dirty(editor, False)
            if editor is self._current_editor():
                self._update_window_title()
            return True
        except Exception as e:
            QMessageBox.warning(self,
                'Speichern',
                f'Datei konnte nicht gespeichert werden:\n{e}')
            return False

    def file_save_as(self, editor=None) -> bool:
        if isinstance(editor, bool):
            editor = None
        if editor is None:
            editor = self._current_editor()
        if editor is None:
            return False
        suggested = getattr(editor, '_path', '') or 'help_project.json'
        path, _ = QFileDialog.getSaveFileName(self,
            'Datei speichern',
            suggested,
            'Help Authoring (*.json);;Alle Dateien (*.*)')
        if not path:
            return False
        editor._path = path
        self._set_editor_dirty(editor, getattr(editor, '_dirty', False))
        if editor is self._current_editor():
            self.current_path = path
            self._update_window_title()
        return self.file_save(editor)

    def closeEvent(self, event):
        self._capture_current_project_to_editor(self._current_editor())
        for idx in range(self.tab_widget.count()):
            editor = self._editor_at(idx)
            if editor is not None and not self.maybe_save(editor):
                event.ignore()
                return
        try:
            if hasattr(self, 'format_dock') and self.format_dock is not None:
                self.removeDockWidget(self.format_dock)
                self.format_dock.setParent(None)
                self.format_dock.close()
        except Exception:
            pass
        self._save_window_state()
        event.accept()

    def merge_format_on_selection(self, fmt: QTextCharFormat):
        editor = self._current_editor()
        if editor is None:
            return
        cursor = editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.BlockUnderCursor)
        cursor.mergeCharFormat(fmt)
        editor.mergeCurrentCharFormat(fmt)

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Normal if self.act_bold.isChecked() is False else QFont.Bold)
        self.merge_format_on_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat(); fmt.setFontItalic(self.act_italic.isChecked()); self.merge_format_on_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat(); fmt.setFontUnderline(self.act_underline.isChecked()); self.merge_format_on_selection(fmt)

    def toggle_strike(self):
        fmt = QTextCharFormat(); fmt.setFontStrikeOut(self.act_strike.isChecked()); self.merge_format_on_selection(fmt)

    def set_font_family(self, font):
        fmt = QTextCharFormat(); fmt.setFontFamily(font.family()); self.merge_format_on_selection(fmt)

    def set_font_size_from_text(self, txt: str):
        try:
            size = float(txt.replace(',', '.'))
        except Exception:
            return
        if size <= 0:
            return
        fmt = QTextCharFormat(); fmt.setFontPointSize(size); self.merge_format_on_selection(fmt)

    def set_text_color(self):
        editor = self._current_editor()
        if editor is None:
            return
        color = QColorDialog.getColor(editor.textColor(), self, 'Textfarbe')
        if not color.isValid():
            return
        fmt = QTextCharFormat(); fmt.setForeground(color); self.merge_format_on_selection(fmt)

    def set_background_color(self):
        editor = self._current_editor()
        if editor is None:
            return
        color = QColorDialog.getColor(editor.textBackgroundColor(), self, 'Hintergrundfarbe')
        if not color.isValid():
            return
        fmt = QTextCharFormat(); fmt.setBackground(color); self.merge_format_on_selection(fmt)

    def apply_heading_style(self, name: str):
        editor = self._current_editor()
        if editor is None:
            return
        if not editor.hasFocus():
            return
        cursor = editor.textCursor()
        char_fmt = QTextCharFormat()
        if name == 'Normal':
            char_fmt.setFontPointSize(11); char_fmt.setFontWeight(QFont.Normal); char_fmt.setFontFamily('Arial')
        elif name == 'H1':
            char_fmt.setFontPointSize(22); char_fmt.setFontWeight(QFont.Bold); char_fmt.setFontFamily('Arial')
        elif name == 'H2':
            char_fmt.setFontPointSize(18); char_fmt.setFontWeight(QFont.Bold); char_fmt.setFontFamily('Arial')
        elif name == 'H3':
            char_fmt.setFontPointSize(15); char_fmt.setFontWeight(QFont.Bold); char_fmt.setFontFamily('Arial')
        elif name == 'H4':
            char_fmt.setFontPointSize(13); char_fmt.setFontWeight(QFont.Bold); char_fmt.setFontFamily('Arial')
        elif name == 'Code':
            char_fmt.setFontPointSize(10); char_fmt.setFontFamily('Consolas'); char_fmt.setFontFixedPitch(True)
        cursor.select(QTextCursor.BlockUnderCursor)
        cursor.mergeCharFormat(char_fmt)
        editor.mergeCurrentCharFormat(char_fmt)

    def insert_bullet_list(self):
        editor = self._current_editor()
        if editor is not None:
            editor.textCursor().insertList(QTextListFormat.ListDisc)

    def insert_numbered_list(self):
        editor = self._current_editor()
        if editor is not None:
            editor.textCursor().insertList(QTextListFormat.ListDecimal)

    def insert_link(self):
        editor = self._current_editor()
        if editor is None:
            return
        cursor = editor.textCursor()
        selected_text = cursor.selectedText() or 'Linktext'
        url, ok = QInputDialog.getText(self, 'Hyperlink', 'URL:')
        if not ok or not url.strip():
            return
        text, ok = QInputDialog.getText(self, 'Hyperlink', 'Anzeigetext:', text=selected_text)
        if not ok or not text.strip():
            return
        cursor.insertHtml(f'<a href="{url.strip()}">{text.strip()}</a>')

    def remove_link(self):
        fmt = QTextCharFormat()
        fmt.setAnchor(False)
        fmt.setAnchorHref('')
        self.merge_format_on_selection(fmt)

    def insert_image(self):
        editor = self._current_editor()
        if editor is None:
            return
        path, _ = QFileDialog.getOpenFileName(self, 'Bild einfügen', '', 'Bilder (*.png *.jpg *.jpeg *.bmp *.gif *.svg *.webp);;Alle Dateien (*.*)')
        if not path:
            return
        editor.textCursor().insertHtml(f'<img src="{path}" alt="{os.path.basename(path)}">')

    def insert_table(self):
        editor = self._current_editor()
        if editor is None:
            return
        dlg = TableInsertDialog(self)
        if dlg.exec_() != QDialog.Accepted:
            return
        spec = dlg.spec()
        fmt = QTextTableFormat()
        fmt.setBorder(spec.border)
        fmt.setCellPadding(spec.cell_padding)
        fmt.setCellSpacing(spec.cell_spacing)
        fmt.setWidth(QTextLength(QTextLength.PercentageLength, spec.width_percent))
        fmt.setHeaderRowCount(1)
        table = editor.textCursor().insertTable(spec.rows, spec.cols, fmt)
        cell_fmt = QTextTableCellFormat()
        cell_fmt.setPadding(spec.cell_padding)
        for r in range(spec.rows):
            for c in range(spec.cols):
                table.cellAt(r, c).setFormat(cell_fmt)

    def _current_table(self):
        editor = self._current_editor()
        return editor.textCursor().currentTable() if editor is not None else None

    def table_add_row(self):
        table = self._current_table()
        if table is not None:
            table.appendRows(1)

    def table_add_column(self):
        table = self._current_table()
        if table is not None:
            table.appendColumns(1)

    def table_remove_row(self):
        editor = self._current_editor()
        table  = self._current_table()
        if table is None or editor is None:
            return
        cell = table.cellAt(editor.textCursor())
        if cell.isValid():
            table.removeRows(cell.row(), 1)

    def table_remove_column(self):
        editor = self._current_editor()
        table  = self._current_table()
        if table is None or editor is None:
            return
        cell = table.cellAt(editor.textCursor())
        if cell.isValid():
            table.removeColumns(cell.column(), 1)

    def table_merge_cells(self):
        editor = self._current_editor()
        table  = self._current_table()
        if table is None or editor is None:
            return
        try:
            table.mergeCells(editor.textCursor())
        except Exception:
            QMessageBox.information(self, 'Tabelle', 'Bitte einen rechteckigen Bereich über mehrere Zellen markieren.')

    def table_split_cell(self):
        editor = self._current_editor()
        table  = self._current_table()
        if table is None or editor is None:
            return
        cell = table.cellAt(editor.textCursor())
        if not cell.isValid():
            return
        try:
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:
                table.splitCell(cell.row(), cell.column(), 1, 1)
        except Exception as e:
            QMessageBox.warning(self, 'Tabelle', f'Zelle konnte nicht geteilt werden:\n{e}')

    def table_set_cell_background(self):
        editor = self._current_editor()
        table  = self._current_table()
        if table is None or editor is None:
            return
        cell = table.cellAt(editor.textCursor())
        if not cell.isValid():
            return
        color = QColorDialog.getColor(QColor('#ffffff'), self, 'Zellhintergrund')
        if not color.isValid():
            return
        fmt = cell.format()
        if not isinstance(fmt, QTextTableCellFormat):
            cfmt = QTextTableCellFormat()
            cfmt.merge(fmt)
            fmt = cfmt
        fmt.setBackground(color)
        cell.setFormat(fmt)

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

    @staticmethod
    def open_in_mdi(main_window):
        if main_window is None or not hasattr(main_window, 'mdi'):
            raise RuntimeError("main_window benötigt ein Attribut 'mdi' (QMdiArea).")

        editor = HelpAuthoringEditor(parent=main_window)
        sub = main_window.mdi.addSubWindow(editor)
        sub.setWindowTitle('Help Authoring')
        try:
            settings = QSettings(editor._ini_path(), QSettings.IniFormat)
            settings.setFallbacksEnabled(False)
            sub_geom = settings.value('help_authoring/sub_geom')
            if sub_geom is not None:
                sub.restoreGeometry(sub_geom)
            else:
                sub.resize(900, 800)
        except Exception:
            sub.resize(900, 800)
        editor.show()
        sub.show()
        try:
            main_window.mdi.setActiveSubWindow(sub)
        except Exception:
            pass
        return sub

def run_standalone():
    app = QApplication(sys.argv)
    w = HelpAuthoringEditor()
    w.show()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(run_standalone())
