# ---------------------------------------------------------------------------
# File:   help.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import os
import sys

from   dataclasses import dataclass
from   share.common import *

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

class HelpAuthoringEditor(QMainWindow):
    contentChanged = pyqtSignal()

    def __init__(self, parent=None, initial_html: str = '', file_path: str = ''):
        super().__init__(parent)
        self.current_path = file_path or ''
        self._is_dirty = False
        self.setWindowTitle('Help Authoring')
        self.resize(800, 620)

        self.editor = QTextEdit()
        self.editor.setAcceptRichText(True)
        self.editor.textChanged.connect(self._on_text_changed)
        self.editor.cursorPositionChanged.connect(self._sync_toolbar_state)

        central = QWidget()
        lay = QVBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.editor)
        self.setCentralWidget(central)

        self._build_toolbar()
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.lbl_status = QLabel('Bereit')
        sb.addPermanentWidget(self.lbl_status)

        self._settings = QSettings(self._ini_path(), QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

        if initial_html:
            self.editor.setHtml(initial_html)
            self._is_dirty = False
        else:
            self.editor.setHtml(self._default_document_html())

        self._sync_toolbar_state()
        self._update_window_title()
        self._update_status()
        self._restore_window_state()

    def _build_toolbar(self):
        tb_file = QToolBar('Datei', self)
        tb_file.setIconSize(QSize(16, 16))
        self.addToolBar(tb_file)

        act_new     = QAction('Neu'               , self); act_new    .triggered.connect(self.file_new)
        act_open    = QAction('Öffnen'            , self); act_open   .triggered.connect(self.file_open)
        act_save    = QAction('Speichern'         , self); act_save   .triggered.connect(self.file_save)
        act_save_as = QAction('Speichern unter...', self); act_save_as.triggered.connect(self.file_save_as)
        act_source  = QAction('HTML'              , self); act_source .triggered.connect(self.edit_html_source)

        tb_file.addAction(act_new)
        tb_file.addAction(act_open)
        tb_file.addAction(act_save)
        tb_file.addAction(act_save_as)
        tb_file.addSeparator()
        tb_file.addAction(act_source)

        tb_fmt = QToolBar('Format', self)
        self.addToolBar(tb_fmt)

        self.act_bold      = QAction('F', self); self.act_bold     .setCheckable(True); self.act_bold     .triggered.connect(self.toggle_bold)
        self.act_italic    = QAction('K', self); self.act_italic   .setCheckable(True); self.act_italic   .triggered.connect(self.toggle_italic)
        self.act_underline = QAction('U', self); self.act_underline.setCheckable(True); self.act_underline.triggered.connect(self.toggle_underline)
        self.act_strike    = QAction('S', self); self.act_strike   .setCheckable(True); self.act_strike   .triggered.connect(self.toggle_strike)

        tb_fmt.addAction(self.act_bold)
        tb_fmt.addAction(self.act_italic)
        tb_fmt.addAction(self.act_underline)
        tb_fmt.addAction(self.act_strike)
        tb_fmt.addSeparator()

        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.set_font_family)
        tb_fmt.addWidget(self.font_combo)

        self.size_combo = QComboBox()
        for s in [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 48, 72]:
            self.size_combo.addItem(str(s))
            
        self.size_combo.setEditable(True)
        self.size_combo.setCurrentText('11')
        self.size_combo.currentTextChanged.connect(self.set_font_size_from_text)
        tb_fmt.addWidget(self.size_combo)

        self.heading_combo = QComboBox()
        self.heading_combo.addItems(['Normal', 'H1', 'H2', 'H3', 'H4', 'Code'])
        self.heading_combo.currentTextChanged.connect(self.apply_heading_style)
        tb_fmt.addWidget(self.heading_combo)

        act_fg = QAction('Textfarbe', self); act_fg.triggered.connect(self.set_text_color)
        act_bg = QAction('Marker', self); act_bg.triggered.connect(self.set_background_color)
        tb_fmt.addAction(act_fg)
        tb_fmt.addAction(act_bg)

        tb_para = QToolBar('Absatz', self)
        self.addToolBar(tb_para)
        for title, align in [('Links', Qt.AlignLeft), ('Zentriert', Qt.AlignHCenter), ('Rechts', Qt.AlignRight), ('Blocksatz', Qt.AlignJustify)]:
            act = QAction(title, self)
            act.triggered.connect(lambda _=False, a=align: self.editor.setAlignment(a))
            tb_para.addAction(act)

        act_bullets = QAction('Liste'         , self); act_bullets.triggered.connect(self.insert_bullet_list)
        act_numbers = QAction('Nummeriert'    , self); act_numbers.triggered.connect(self.insert_numbered_list)
        act_link    = QAction('Link'          , self); act_link   .triggered.connect(self.insert_link)
        act_unlink  = QAction('Link entfernen', self); act_unlink .triggered.connect(self.remove_link)
        act_image   = QAction('Bild'          , self); act_image  .triggered.connect(self.insert_image)

        tb_para.addSeparator()
        tb_para.addAction(act_bullets)
        tb_para.addAction(act_numbers)
        tb_para.addSeparator()
        tb_para.addAction(act_link)
        tb_para.addAction(act_unlink)
        tb_para.addAction(act_image)

        tb_table = QToolBar('Tabelle', self)
        self.addToolBar(tb_table)
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
            act = QAction(title, self); act.triggered.connect(fn); tb_table.addAction(act)

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

    def _save_window_state(self):
        try:
            parent = self.parentWidget()
            if parent is not None and parent.__class__.__name__ == 'QMdiSubWindow':
                self._settings.setValue('help_authoring/sub_geom', parent.saveGeometry())
        except Exception:
            pass
        try:
            self._settings.setValue('help_authoring/main_geom', self.saveGeometry())
            self._settings.setValue('help_authoring/main_state', self.saveState())
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

    def _on_text_changed(self):
        self._is_dirty = True
        self._update_window_title()
        self._update_status()
        self.contentChanged.emit()

    def _update_window_title(self):
        name = os.path.basename(self.current_path) if self.current_path else 'Unbenannt'
        star = ' *' if self._is_dirty else ''
        self.setWindowTitle(f'Help Authoring - {name}{star}')

    def _update_status(self):
        plain = self.editor.toPlainText()
        words = len([w for w in plain.split() if w.strip()])
        chars = len(plain)
        self.lbl_status.setText(f'Wörter: {words} | Zeichen: {chars}')

    def _sync_toolbar_state(self):
        fmt = self.editor.currentCharFormat()
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

    def maybe_save(self) -> bool:
        if not self._is_dirty:
            return True
        ret = QMessageBox.question(self,
            'Änderungen speichern?',
            'Das Dokument wurde geändert.\nSoll es gespeichert werden?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.Yes)
        if ret == QMessageBox.Cancel:
            return False
        if ret == QMessageBox.Yes:
            return self.file_save()
        return True

    def file_new(self):
        if not self.maybe_save():
            return
        self.current_path = ''
        self.editor.setHtml(self._default_document_html())
        self._is_dirty = False
        self._update_window_title()
        self._update_status()

    def file_open(self):
        if not self.maybe_save():
            return
        path, _ = QFileDialog.getOpenFileName(self,
            'HTML-Datei öffnen', '',
            'HTML Dateien (*.html *.htm);;Alle Dateien (*.*)')
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                html = f.read()
            self.editor.setHtml(html)
            self.current_path = path
            self._is_dirty = False
            self._update_window_title()
            self._update_status()
        except Exception as e:
            QMessageBox.warning(self,
                'Öffnen',
                f'Datei konnte nicht gelesen werden:\n{e}')

    def file_save(self) -> bool:
        if not self.current_path:
            return self.file_save_as()
        try:
            with open(self.current_path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(self.editor.toHtml())
            self._is_dirty = False
            self._update_window_title()
            return True
        except Exception as e:
            QMessageBox.warning(self,
                'Speichern',
                f'Datei konnte nicht gespeichert werden:\n{e}')
            return False

    def file_save_as(self) -> bool:
        suggested = self.current_path or 'help_page.html'
        path, _ = QFileDialog.getSaveFileName(self,
            'HTML-Datei speichern',
            suggested,
            'HTML Dateien (*.html *.htm);;Alle Dateien (*.*)')
        if not path:
            return False
        self.current_path = path
        return self.file_save()

    def closeEvent(self, event):
        if self.maybe_save():
            self._save_window_state()
            event.accept()
        else:
            event.ignore()

    def merge_format_on_selection(self, fmt: QTextCharFormat):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)

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
        color = QColorDialog.getColor(self.editor.textColor(), self, 'Textfarbe')
        if not color.isValid():
            return
        fmt = QTextCharFormat(); fmt.setForeground(color); self.merge_format_on_selection(fmt)

    def set_background_color(self):
        color = QColorDialog.getColor(self.editor.textBackgroundColor(), self, 'Hintergrundfarbe')
        if not color.isValid():
            return
        fmt = QTextCharFormat(); fmt.setBackground(color); self.merge_format_on_selection(fmt)

    def apply_heading_style(self, name: str):
        if not self.editor.hasFocus():
            return
        cursor = self.editor.textCursor()
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
        self.editor.mergeCurrentCharFormat(char_fmt)

    def insert_bullet_list(self):
        self.editor.textCursor().insertList(QTextListFormat.ListDisc)

    def insert_numbered_list(self):
        self.editor.textCursor().insertList(QTextListFormat.ListDecimal)

    def insert_link(self):
        cursor = self.editor.textCursor()
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
        path, _ = QFileDialog.getOpenFileName(self, 'Bild einfügen', '', 'Bilder (*.png *.jpg *.jpeg *.bmp *.gif *.svg *.webp);;Alle Dateien (*.*)')
        if not path:
            return
        self.editor.textCursor().insertHtml(f'<img src="{path}" alt="{os.path.basename(path)}">')

    def insert_table(self):
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
        table = self.editor.textCursor().insertTable(spec.rows, spec.cols, fmt)
        cell_fmt = QTextTableCellFormat()
        cell_fmt.setPadding(spec.cell_padding)
        for r in range(spec.rows):
            for c in range(spec.cols):
                table.cellAt(r, c).setFormat(cell_fmt)

    def _current_table(self):
        return self.editor.textCursor().currentTable()

    def table_add_row(self):
        table = self._current_table()
        if table is not None:
            table.appendRows(1)

    def table_add_column(self):
        table = self._current_table()
        if table is not None:
            table.appendColumns(1)

    def table_remove_row(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt(self.editor.textCursor())
        if cell.isValid():
            table.removeRows(cell.row(), 1)

    def table_remove_column(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt(self.editor.textCursor())
        if cell.isValid():
            table.removeColumns(cell.column(), 1)

    def table_merge_cells(self):
        table = self._current_table()
        if table is None:
            return
        try:
            table.mergeCells(self.editor.textCursor())
        except Exception:
            QMessageBox.information(self, 'Tabelle', 'Bitte einen rechteckigen Bereich über mehrere Zellen markieren.')

    def table_split_cell(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt(self.editor.textCursor())
        if not cell.isValid():
            return
        try:
            if cell.rowSpan() > 1 or cell.columnSpan() > 1:
                table.splitCell(cell.row(), cell.column(), 1, 1)
        except Exception as e:
            QMessageBox.warning(self, 'Tabelle', f'Zelle konnte nicht geteilt werden:\n{e}')

    def table_set_cell_background(self):
        table = self._current_table()
        if table is None:
            return
        cell = table.cellAt(self.editor.textCursor())
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
        dlg = HtmlSourceDialog(self.editor.toHtml(), self)
        if dlg.exec_() != QDialog.Accepted:
            return
        self.editor.setHtml(dlg.html())

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
