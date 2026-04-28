import os
import sys
import subprocess
from pathlib import Path

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QTabWidget, QPushButton, QLabel, QLineEdit,
    QCheckBox,
    QListWidget, QListWidgetItem, QAbstractItemView,
    QPlainTextEdit, QScrollArea, QMessageBox,
    QSplitter
)


FILTERS = {
    "ALL": None,
    "ICO": [".ico"],
    "PNG": [".png"],
    "JPG": [".jpg", ".jpeg"],
    "XML": [".xml", ".qrc"],
    "JSON": [".json"],
    "HTML": [".html", ".htm"],
    "CSS": [".css"],
    "JS": [".js"],
    "MO": [".mo"],
}


class AliasRow(QWidget):
    def __init__(self, file_path: Path, base_dir: Path, parent=None):
        super().__init__(parent)

        self.file_path = Path(file_path)
        self.base_dir = Path(base_dir)

        self.label = QLabel(self.file_path.name)
        self.label.setToolTip(str(self.file_path))
        self.label.setMinimumWidth(120)
        self.label.setMaximumWidth(220)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.alias_edit = QLineEdit()
        self.alias_edit.setText(self.file_path.name)
        self.alias_edit.setPlaceholderText("Alias, z.B. baz.ico")

        self.dir_edit = QLineEdit()
        self.dir_edit.setText(self.default_dir_name())
        self.dir_edit.setPlaceholderText("Verzeichnis, z.B. bar")

        line1 = QHBoxLayout()
        line1.setContentsMargins(0, 0, 0, 0)
        line1.setSpacing(6)
        line1.addWidget(self.label)
        line1.addWidget(self.alias_edit, 1)

        line2 = QHBoxLayout()
        line2.setContentsMargins(0, 0, 0, 0)
        line2.setSpacing(6)

        dir_label = QLabel("Pfad:")
        dir_label.setMinimumWidth(120)
        dir_label.setMaximumWidth(220)
        dir_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        line2.addWidget(dir_label)
        line2.addWidget(self.dir_edit, 1)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(2, 2, 2, 4)
        lay.setSpacing(2)
        lay.addLayout(line1)
        lay.addLayout(line2)

    def default_dir_name(self) -> str:
        parent = self.file_path.parent

        if parent == self.base_dir:
            return ""

        return parent.name

    def alias_name(self) -> str:
        return self.alias_edit.text().strip()

    def dir_name(self) -> str:
        return self.dir_edit.text().strip().replace("\\", "/").strip("/")

    def file_name(self) -> str:
        return self.file_path.name

    def resource_file_name(self) -> str:
        directory = self.dir_name()
        file_name = self.file_name()

        if directory:
            return f"{directory}/{file_name}"

        return file_name

    def relative_file_name(self) -> str:
        try:
            rel = self.file_path.relative_to(self.base_dir)
        except ValueError:
            rel = self.file_path
        return str(rel).replace("\\", "/")


class ResourceAliasBuilder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Qt5 Resource Alias Builder")
        self.resize(1120, 680)

        self.current_dir = Path.cwd()
        self.current_filter = "ALL"
        self.alias_rows = []

        self._build_ui()
        self._load_directory(self.current_dir)

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_lay = QHBoxLayout(central)
        main_lay.setContentsMargins(6, 6, 6, 6)

        splitter = QSplitter(Qt.Horizontal)
        main_lay.addWidget(splitter)

        self.left_tabs = QTabWidget()
        self.middle_widget = QWidget()
        self.right_tabs = QTabWidget()

        splitter.addWidget(self.left_tabs)
        splitter.addWidget(self.middle_widget)
        splitter.addWidget(self.right_tabs)
        splitter.setSizes([420, 130, 560])

        self._build_left_tabs()
        self._build_middle_buttons()
        self._build_right_tabs()

    def _build_left_tabs(self):
        tab_dir = QWidget()
        dir_lay = QVBoxLayout(tab_dir)

        self.dir_edit = QLineEdit()
        self.dir_edit.setText(str(self.current_dir))

        btn_choose = QPushButton("Verzeichnis wählen")
        btn_choose.clicked.connect(self._choose_directory)

        btn_reload = QPushButton("Neu laden")
        btn_reload.clicked.connect(lambda: self._load_directory(Path(self.dir_edit.text())))

        dir_lay.addWidget(QLabel("Aktuelles Verzeichnis:"))
        dir_lay.addWidget(self.dir_edit)
        dir_lay.addWidget(btn_choose)
        dir_lay.addWidget(btn_reload)
        dir_lay.addStretch()

        self.left_tabs.addTab(tab_dir, "Verzeichnis")

        tab_data = QWidget()
        data_lay = QVBoxLayout(tab_data)

        filter_lay = QGridLayout()
        filter_lay.setSpacing(3)

        for index, name in enumerate(FILTERS.keys()):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self._set_filter(n))
            filter_lay.addWidget(btn, index // 5, index % 5)
            if name == "ALL":
                btn.setChecked(True)
            setattr(self, f"filter_btn_{name}", btn)

        self.icon_view = QListWidget()
        self.icon_view.setViewMode(QListWidget.IconMode)
        self.icon_view.setIconSize(QSize(32, 32))
        self.icon_view.setGridSize(QSize(96, 76))
        self.icon_view.setResizeMode(QListWidget.Adjust)
        self.icon_view.setMovement(QListWidget.Static)
        self.icon_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.icon_view.setWordWrap(True)

        data_lay.addLayout(filter_lay)
        data_lay.addWidget(self.icon_view, 1)

        self.left_tabs.addTab(tab_data, "Daten")

    def _build_middle_buttons(self):
        lay = QVBoxLayout(self.middle_widget)
        lay.setContentsMargins(4, 24, 4, 4)
        lay.setSpacing(8)

        self.btn_apply = QPushButton("Übernehmen")
        self.btn_clear_all = QPushButton("Alle Löschen")
        self.btn_delete = QPushButton("Löschen")
        self.btn_xml = QPushButton("XML schreiben")
        self.btn_py = QPushButton("PY schreiben")

        self.chk_root_only = QCheckBox("nur Root")
        self.chk_root_only.setToolTip(
            "Wenn aktiv, werden Dateien im gleichen Verzeichnis als <file>name</file> geschrieben."
        )

        self.btn_apply.clicked.connect(self._apply_selected_files)
        self.btn_clear_all.clicked.connect(self._clear_all_aliases)
        self.btn_delete.clicked.connect(self._delete_focused_alias)
        self.btn_xml.clicked.connect(self._write_xml_to_editor)
        self.btn_py.clicked.connect(self._write_py_resource)

        for btn in [self.btn_apply, self.btn_clear_all, self.btn_delete, self.btn_xml, self.btn_py]:
            btn.setMinimumHeight(32)
            lay.addWidget(btn)

        lay.addWidget(self.chk_root_only)
        lay.addStretch()

    def _build_right_tabs(self):
        tab_alias = QWidget()
        alias_lay = QVBoxLayout(tab_alias)

        self.alias_scroll = QScrollArea()
        self.alias_scroll.setWidgetResizable(True)

        self.alias_host = QWidget()
        self.alias_lay = QVBoxLayout(self.alias_host)
        self.alias_lay.setContentsMargins(2, 2, 2, 2)
        self.alias_lay.setSpacing(2)
        self.alias_lay.addStretch()

        self.alias_scroll.setWidget(self.alias_host)
        alias_lay.addWidget(self.alias_scroll)

        self.right_tabs.addTab(tab_alias, "Aliases")

        tab_xml = QWidget()
        xml_lay = QVBoxLayout(tab_xml)

        self.xml_edit = QPlainTextEdit()
        self.xml_edit.setFont(QFont("Consolas", 10))
        self.xml_edit.setPlaceholderText("Hier wird das .qrc XML erzeugt...")

        xml_lay.addWidget(self.xml_edit)
        self.right_tabs.addTab(tab_xml, "XML")

    def _choose_directory(self):
        path = QFileDialog.getExistingDirectory(self, "Verzeichnis wählen", str(self.current_dir))
        if path:
            self._load_directory(Path(path))
            self.left_tabs.setCurrentIndex(1)

    def _set_filter(self, filter_name: str):
        self.current_filter = filter_name

        for name in FILTERS:
            btn = getattr(self, f"filter_btn_{name}", None)
            if btn:
                btn.setChecked(name == filter_name)

        self._load_directory(Path(self.dir_edit.text()))

    def _load_directory(self, directory: Path):
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            QMessageBox.warning(self, "Fehler", f"Verzeichnis existiert nicht:\n{directory}")
            return

        self.current_dir = directory
        self.dir_edit.setText(str(directory))
        self.icon_view.clear()

        suffixes = FILTERS.get(self.current_filter)

        try:
            files = sorted([p for p in directory.iterdir() if p.is_file()], key=lambda p: p.name.lower())
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))
            return

        for path in files:
            suffix = path.suffix.lower()

            if suffixes is not None and suffix not in suffixes:
                continue

            item = QListWidgetItem()
            item.setText(path.name)
            item.setToolTip(str(path))
            item.setData(Qt.UserRole, str(path))

            icon = self._icon_for_file(path)
            item.setIcon(icon)

            self.icon_view.addItem(item)

    def _icon_for_file(self, path: Path) -> QIcon:
        if path.suffix.lower() in [".png", ".jpg", ".jpeg", ".ico", ".bmp", ".gif"]:
            icon = QIcon(str(path))
            if not icon.isNull():
                return icon
        return QIcon.fromTheme("text-x-generic")

    def _apply_selected_files(self):
        selected = self.icon_view.selectedItems()

        if not selected:
            QMessageBox.information(self, "Hinweis", "Keine Dateien ausgewählt.")
            return

        existing_files = {str(row.file_path) for row in self.alias_rows}

        for item in selected:
            path = Path(item.data(Qt.UserRole))

            if str(path) in existing_files:
                continue

            row = AliasRow(path, self.current_dir)
            self.alias_lay.insertWidget(self.alias_lay.count() - 1, row)
            self.alias_rows.append(row)

        self.right_tabs.setCurrentIndex(0)

    def _clear_all_aliases(self):
        for row in self.alias_rows:
            row.setParent(None)
            row.deleteLater()

        self.alias_rows.clear()
        self.xml_edit.clear()

    def _delete_focused_alias(self):
        focus = QApplication.focusWidget()

        for row in list(self.alias_rows):
            if focus is row.alias_edit or focus is row.dir_edit:
                self.alias_rows.remove(row)
                row.setParent(None)
                row.deleteLater()
                return

        QMessageBox.information(
            self,
            "Hinweis",
            "Setze den Fokus zuerst in die Alias-Eingabezeile, die gelöscht werden soll."
        )

    def _create_xml(self) -> str:
        lines = [
            "<RCC>",
            '    <qresource prefix="/icons">',
        ]

        root_only = self.chk_root_only.isChecked()

        for row in self.alias_rows:
            alias = row.alias_name()
            directory = row.dir_name()
            file_name = row.file_name()

            if root_only:
                if directory:
                    resource_file = f"{directory}/{file_name}"
                    alias = alias or file_name
                    lines.append(
                        f'        <file alias="{self._xml_escape(alias)}">{self._xml_escape(resource_file)}</file>'
                    )
                else:
                    lines.append(
                        f'        <file>{self._xml_escape(file_name)}</file>'
                    )
            else:
                resource_file = row.resource_file_name()

                if directory:
                    alias = alias or file_name
                    lines.append(
                        f'        <file alias="{self._xml_escape(alias)}">{self._xml_escape(resource_file)}</file>'
                    )
                else:
                    lines.append(
                        f'        <file>{self._xml_escape(resource_file)}</file>'
                    )

        lines.extend([
            "    </qresource>",
            "</RCC>",
            "",
        ])

        return "\n".join(lines)

    def _write_xml_to_editor(self):
        if not self.alias_rows:
            QMessageBox.information(self, "Hinweis", "Es sind keine Aliase vorhanden.")
            return

        self.xml_edit.setPlainText(self._create_xml())
        self.right_tabs.setCurrentIndex(1)

    def _write_py_resource(self):
        xml_text = self.xml_edit.toPlainText().strip()

        if not xml_text:
            self._write_xml_to_editor()
            xml_text = self.xml_edit.toPlainText().strip()

        if not xml_text:
            return

        qrc_file, _ = QFileDialog.getSaveFileName(
            self,
            "QRC-Datei speichern",
            str(self.current_dir / "images.qrc"),
            "Qt Resource (*.qrc);;XML (*.xml);;Alle Dateien (*.*)"
        )

        if not qrc_file:
            return

        qrc_path = Path(qrc_file)
        qrc_path.write_text(xml_text + "\n", encoding="utf-8")

        py_file, _ = QFileDialog.getSaveFileName(
            self,
            "Resource-Python-Datei speichern",
            str(qrc_path.with_name(qrc_path.stem + "_rc.py")),
            "Python (*.py);;Alle Dateien (*.*)"
        )

        if not py_file:
            return

        py_path = Path(py_file)
        cmd = ["pyrcc5", str(qrc_path), "-o", str(py_path)]

        try:
            proc = subprocess.run(
                cmd,
                cwd=str(self.current_dir),
                capture_output=True,
                text=True,
                shell=False,
            )
        except FileNotFoundError:
            QMessageBox.critical(
                self,
                "pyrcc5 nicht gefunden",
                "pyrcc5 wurde nicht gefunden.\n\n"
                "Alternative:\npython -m PyQt5.pyrcc_main images.qrc -o images_rc.py"
            )
            return
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))
            return

        if proc.returncode != 0:
            QMessageBox.critical(
                self,
                "pyrcc5 Fehler",
                f"Befehl:\n{' '.join(cmd)}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
            )
            return

        QMessageBox.information(
            self,
            "Fertig",
            f"Resource-Dateien wurden geschrieben:\n\n{qrc_path}\n{py_path}"
        )

    @staticmethod
    def _xml_escape(text: str) -> str:
        return (
            text.replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )


def main():
    app = QApplication(sys.argv)
    win = ResourceAliasBuilder()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
