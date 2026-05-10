# ---------------------------------------------------------------------------
# File:   resource_builder.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__   import annotations

from share.common import *

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
        self.alias_edit.setPlaceholderText("Alias, e.g. baz.ico")

        self.dir_edit = QLineEdit()
        self.dir_edit.setText(self.default_dir_name())
        self.dir_edit.setPlaceholderText(share.locales.tr("Directory, e.g. bar"))

        line1 = QHBoxLayout()
        line1.setContentsMargins(0, 0, 0, 0)
        line1.setSpacing(6)
        line1.addWidget(self.label)
        line1.addWidget(self.alias_edit, 1)

        line2 = QHBoxLayout()
        line2.setContentsMargins(0, 0, 0, 0)
        line2.setSpacing(6)

        dir_label = QLabel(share.locales.tr("Path:"))
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


class ResourceBuilderToolWindow(QWidget):
    FILTERS = {
        "ALL" : None,
        "ICO" : [".ico"],
        "PNG" : [".png"],
        "JPG" : [".jpg", ".jpeg"],
        "XML" : [".xml", ".qrc"],
        "JSON": [".json"],
        "HTML": [".html", ".htm"],
        "CSS" : [".css"],
        "JS"  : [".js"],
        "MO"  : [".mo"],
    }
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window

        self.setWindowTitle("Qt5 Resource Alias Builder")
        self.resize(1000, 460)

        self.current_dir = Path.cwd()
        self.current_filter = "ALL"
        self.alias_rows = []

        self._build_ui()
        self._load_directory(self.current_dir)

    def _build_ui(self):
        main_lay = QHBoxLayout(self)
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

        btn_choose = QPushButton(share.locales.tr("Select Directory"))
        btn_choose.clicked.connect(self._choose_directory)

        btn_reload = QPushButton(share.locales.tr("Load New"))
        btn_reload.clicked.connect(lambda: self._load_directory(Path(self.dir_edit.text())))

        dir_lay.addWidget(QLabel(share.locales.tr("Actual Directory:")))
        dir_lay.addWidget(self.dir_edit)
        dir_lay.addWidget(btn_choose)
        dir_lay.addWidget(btn_reload)
        dir_lay.addStretch()

        self.left_tabs.addTab(tab_dir, share.locales.tr("Directory"))

        tab_data = QWidget()
        data_lay = QVBoxLayout(tab_data)

        filter_lay = QGridLayout()
        filter_lay.setSpacing(3)

        for index, name in enumerate(self.FILTERS.keys()):
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=name: self._set_filter(n))
            filter_lay.addWidget(btn, index // 5, index % 5)
            if name == "ALL":
                btn.setChecked(True)
            setattr(self, f"filter_btn_{name}", btn)

        self.view_stack = QStackedWidget()
        
        self.icon_view = QListWidget()
        self.icon_view.setViewMode(QListWidget.IconMode)
        self.icon_view.setIconSize(QSize(32, 32))
        self.icon_view.setGridSize(QSize(96, 76))
        self.icon_view.setResizeMode(QListWidget.Adjust)
        self.icon_view.setMovement(QListWidget.Static)
        self.icon_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.icon_view.setWordWrap(True)
        self.icon_view.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.icon_view.customContextMenuRequested.connect(self._on_resource_view_context_menu)
        self.icon_view.itemDoubleClicked         .connect(self._on_icon_view_double_clicked)

        self.detail_view = QTreeWidget()
        self.detail_view.setColumnCount(3)
        self.detail_view.setHeaderLabels([
            share.locales.tr("Name"),
            share.locales.tr("Size"),
            share.locales.tr("Date")]
        )
        self.detail_view.setRootIsDecorated(False)
        self.detail_view.setAlternatingRowColors(True)
        self.detail_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.detail_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.detail_view.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.detail_view.setSortingEnabled(True)
        
        self.detail_view.sortByColumn(2, Qt.AscendingOrder)
        self.detail_view.sortByColumn(0, Qt.AscendingOrder)
        
        self.detail_view.customContextMenuRequested.connect(self._on_resource_view_context_menu)
        self.detail_view.itemDoubleClicked         .connect(self._on_detail_view_double_clicked)
        
        self.detail_view.header().setStretchLastSection(False)
        self.detail_view.header().setSectionsMovable(True)
        self.detail_view.header().setSectionsClickable(True)
        
        self.detail_view.header().setSectionResizeMode(0, QHeaderView.Interactive)
        self.detail_view.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.detail_view.header().setSectionResizeMode(2, QHeaderView.Interactive)
        
        self.detail_view.setColumnWidth(0, 130)
        self.detail_view.setColumnWidth(1,  79)
        self.detail_view.setColumnWidth(2, 150)

        self.view_stack.addWidget(self.icon_view)
        self.view_stack.addWidget(self.detail_view)

        self.current_view_mode = "icon"

        button_lay = QHBoxLayout()
        self.button_view_a = QPushButton(share.locales.tr("Icon View"))
        self.button_view_b = QPushButton(share.locales.tr("List View"))
        self.button_view_c = QPushButton(share.locales.tr("Detail View"))
        
        self.button_view_a.clicked.connect(self._on_button_view_a)
        self.button_view_b.clicked.connect(self._on_button_view_b)
        self.button_view_c.clicked.connect(self._on_button_view_c)
        
        button_lay.addWidget(self.button_view_a)
        button_lay.addWidget(self.button_view_b)
        button_lay.addWidget(self.button_view_c)
        
        data_lay.addLayout(filter_lay)
        data_lay.addWidget(self.view_stack, 1)
        data_lay.addLayout(button_lay)
        
        self.left_tabs.addTab(tab_data, share.locales.tr("Data"))

    def _build_middle_buttons(self):
        lay = QVBoxLayout(self.middle_widget)
        lay.setContentsMargins(4, 24, 4, 4)
        lay.setSpacing(8)

        self.btn_apply     = QPushButton(share.locales.tr("Apply"))
        self.btn_clear_all = QPushButton(share.locales.tr("Delete All"))
        self.btn_delete    = QPushButton(share.locales.tr("Delete"))
        self.btn_xml       = QPushButton(share.locales.tr("Write XML"))
        self.btn_py        = QPushButton(share.locales.tr("Write PY"))

        self.chk_root_only = QCheckBox(share.locales.tr("only Root"))
        self.chk_root_only.setToolTip(
            share.locales.tr(
                "When active, the files will be write to the same Directory:\n"
                "<file>name</file>."
            )
        )

        self.btn_apply     .clicked.connect(self._apply_selected_files)
        self.btn_clear_all .clicked.connect(self._clear_all_aliases)
        self.btn_delete    .clicked.connect(self._delete_focused_alias)
        self.btn_xml       .clicked.connect(self._write_xml_to_editor)
        self.btn_py        .clicked.connect(self._write_py_resource)

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
        self.xml_edit.setPlaceholderText(
            share.locales.tr("the .qrc XML will be created hehe..."))

        xml_lay.addWidget(self.xml_edit)
        self.right_tabs.addTab(tab_xml, "XML")

    def _on_icon_view_context_menu(self, pos):
        menu = QMenu(self.icon_view)

        act_icon   = menu.addAction(share.locales.tr("Icon"   ))
        act_list   = menu.addAction(share.locales.tr("List"   ))
        act_detail = menu.addAction(share.locales.tr("Details"))

        act_icon   .setCheckable(True)
        act_list   .setCheckable(True)
        act_detail .setCheckable(True)

        view_mode = self.icon_view.viewMode()
        if view_mode == QListWidget.IconMode:
            act_icon.setChecked(True)
        elif view_mode == QListWidget.ListMode:
            if self.icon_view.gridSize().width() > 0:
                act_detail.setChecked(True)
            else:
                act_list.setChecked(True)

        act = menu.exec_(self.icon_view.viewport().mapToGlobal(pos))

        if   act == act_icon:   self._set_icon_view_mode("icon")
        elif act == act_list:   self._set_icon_view_mode("list")
        elif act == act_detail: self._set_icon_view_mode("detail")

    def _set_icon_view_mode(self, mode: str):
        if mode == "icon":
            self.icon_view.setViewMode(QListWidget.IconMode)
            self.icon_view.setIconSize(QSize(32, 32))
            self.icon_view.setGridSize(QSize(96, 76))
            self.icon_view.setResizeMode(QListWidget.Adjust)
            self.icon_view.setMovement(QListWidget.Static)
            self.icon_view.setWordWrap(True)

        elif mode == "list":
            self.icon_view.setViewMode(QListWidget.ListMode)
            self.icon_view.setIconSize(QSize(24, 24))
            self.icon_view.setGridSize(QSize())
            self.icon_view.setResizeMode(QListWidget.Adjust)
            self.icon_view.setMovement(QListWidget.Static)
            self.icon_view.setWordWrap(False)

        elif mode == "detail":
            self.icon_view.setViewMode(QListWidget.ListMode)
            self.icon_view.setIconSize(QSize(32, 32))
            self.icon_view.setGridSize(QSize(260, 42))
            self.icon_view.setResizeMode(QListWidget.Adjust)
            self.icon_view.setMovement(QListWidget.Static)
            self.icon_view.setWordWrap(False)
            
    def _choose_directory(self):
        path = QFileDialog.getExistingDirectory(self,
            share.locales.tr("Select Directory"),
            str(self.current_dir))
        if path:
            self._load_directory(Path(path))
            self.left_tabs.setCurrentIndex(1)

    def _set_filter(self, filter_name: str):
        self.current_filter = filter_name

        for name in self.FILTERS:
            btn = getattr(self, f"filter_btn_{name}", None)
            if btn:
                btn.setChecked(name == filter_name)

        self._load_directory(Path(self.dir_edit.text()))

    def _load_directory(self, directory: Path):
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            msg = share.locales.tr("Verzeichnis existiert nicht")
            QMessageBox.warning(self, "Fehler", f"{msg}:\n{directory}")
            return

        self.current_dir = directory
        self.dir_edit.setText(str(directory))

        self.icon_view  .clear()
        self.detail_view.clear()

        suffixes = self.FILTERS.get(self.current_filter)

        try:
            files = sorted([p for p in directory.iterdir() if p.is_file()], key=lambda p: p.name.lower())
        except Exception as e:
            QMessageBox.critical(self,
                share.locales.tr("Error"),
                str(e))
            return

        for path in files:
            suffix = path.suffix.lower()

            if suffixes is not None and suffix not in suffixes:
                continue

            icon = self._icon_for_file(path)

            item = QListWidgetItem()
            item.setText(path.name)
            item.setToolTip(str(path))
            item.setData(Qt.UserRole, str(path))
            item.setIcon(icon)
            
            self.icon_view.addItem(item)

            try:
                stat = path.stat()
                size_text = self._format_file_size(stat.st_size)
                date_text = QDateTime.fromSecsSinceEpoch(int(stat.st_mtime)).toString("yyyy-MM-dd HH:mm:ss")
            except Exception:
                size_text = ""
                date_text = ""

            tree_item = QTreeWidgetItem()
            tree_item.setText(0, path.name)
            tree_item.setText(1, size_text)
            tree_item.setText(2, date_text)
            tree_item.setTextAlignment(1, Qt.AlignRight | Qt.AlignVCenter)
            tree_item.setToolTip(0, str(path))
            tree_item.setData(0, Qt.UserRole, str(path))
            tree_item.setIcon(0, icon)
            
            self.detail_view.addTopLevelItem(tree_item)

    def _icon_for_file(self, path: Path) -> QIcon:
        if path.suffix.lower() in [".png", ".jpg", ".jpeg", ".ico", ".bmp", ".gif"]:
            icon = QIcon(str(path))
            if not icon.isNull():
                return icon
                
        icon = QIcon.fromTheme("text-x-generic")
        if not icon.isNull():
            return icon
        
        return self.style().standardIcon(QStyle.SP_FileIcon)

    def _apply_selected_files(self):
        selected_paths = self._selected_resource_paths()

        if not selected_paths:
            QMessageBox.information(self,
                share.locales.tr("Note"),
                share.locales.tr("No Files selected."))
            return

        existing_files = {str(row.file_path) for row in self.alias_rows}

        for path in selected_paths:
            path = Path(path)

            if str(path) in existing_files:
                continue

            row = AliasRow(path, self.current_dir)
            self.alias_lay.insertWidget(self.alias_lay.count() - 1, row)
            self.alias_rows.append(row)

        self.right_tabs.setCurrentIndex(0)

    def _on_icon_view_double_clicked(self, item):
        self._apply_selected_files()
    
    def _on_detail_view_double_clicked(self, item, column):
        self._apply_selected_files()
    
    def _on_resource_view_context_menu(self, pos):
        sender = self.sender()

        menu = QMenu(self)

        act_icon   = menu.addAction(share.locales.tr("Icon"  ))
        act_list   = menu.addAction(share.locales.tr("List"  ))
        act_detail = menu.addAction(share.locales.tr("Detail"))

        act_icon.setCheckable(True)
        act_list.setCheckable(True)
        act_detail.setCheckable(True)

        act_icon.setChecked  (self.current_view_mode == "icon"  )
        act_list.setChecked  (self.current_view_mode == "list"  )
        act_detail.setChecked(self.current_view_mode == "detail")

        if sender is self.detail_view:
            global_pos = self.detail_view.viewport().mapToGlobal(pos)
        else:
            global_pos = self.icon_view.viewport().mapToGlobal(pos)

        act = menu.exec_(global_pos)

        if   act == act_icon:   self._set_resource_view_mode("icon")
        elif act == act_list:   self._set_resource_view_mode("list")
        elif act == act_detail: self._set_resource_view_mode("detail")

    def _on_button_view_a(self): self._set_resource_view_mode("icon")
    def _on_button_view_b(self): self._set_resource_view_mode("list")
    def _on_button_view_c(self): self._set_resource_view_mode("detail")
    
    def _set_resource_view_mode(self, mode: str):
        self.current_view_mode = mode

        if mode == "detail":
            self.view_stack.setCurrentWidget(self.detail_view)
            return

        self.view_stack.setCurrentWidget(self.icon_view)

        if mode == "icon":
            self.icon_view.setViewMode(QListWidget.IconMode)
            self.icon_view.setIconSize(QSize(32, 32))
            self.icon_view.setGridSize(QSize(96, 76))
            self.icon_view.setResizeMode(QListWidget.Adjust)
            self.icon_view.setMovement(QListWidget.Static)
            self.icon_view.setWordWrap(True)

        elif mode == "list":
            self.icon_view.setViewMode(QListWidget.ListMode)
            self.icon_view.setIconSize(QSize(24, 24))
            self.icon_view.setGridSize(QSize())
            self.icon_view.setResizeMode(QListWidget.Adjust)
            self.icon_view.setMovement(QListWidget.Static)
            self.icon_view.setWordWrap(False)

    def _selected_resource_paths(self):
        result = []

        if self.current_view_mode == "detail":
            for item in self.detail_view.selectedItems():
                path = item.data(0, Qt.UserRole)
                if path:
                    result.append(Path(path))
        else:
            for item in self.icon_view.selectedItems():
                path = item.data(Qt.UserRole)
                if path:
                    result.append(Path(path))

        return result

    def _format_file_size(self, size: int) -> str:
        units = ["B", "KB", "MB", "GB", "TB"]
        value = float(size)

        for unit in units:
            if value < 1024.0 or unit == units[-1]:
                if unit == "B":
                    return f"{int(value)} {unit}"
                return f"{value:.1f} {unit}"
            value /= 1024.0

        return f"{size} B"
        
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

        QMessageBox.information(self,
            share.locales.tr("Note"),
            share.locales.tr("To delete, set the focus into the Alias EditLine."))

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
            QMessageBox.information(self,
                share.locales.tr("Note"),
                share.locales.tr("No Aliases found."))
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

        msg = share.locales.tr("All Files")
        qrc_file, _ = QFileDialog.getSaveFileName(self,
            share.locales.tr("Save QRC-File"),
            str(self.current_dir / "images.qrc"),
            f"Qt Resource (*.qrc);;XML (*.xml);;{msg} (*.*)"
        )

        if not qrc_file:
            return

        qrc_path = Path(qrc_file)
        qrc_path.write_text(xml_text + "\n", encoding="utf-8")

        msg = share.locales.tr("All Files")
        py_file, _ = QFileDialog.getSaveFileName(
            self,
            share.locales.tr("Save Resource-Python-File"),
            str(qrc_path.with_name(qrc_path.stem + "_rc.py")),
            f"Python (*.py);;{msg} (*.*)"
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
                share.locales.tr("pyrcc5 not found."),
                share.locales.tr("pyrcc5 could not found") + ".\n\n"
                "Alternative:\npython -m PyQt5.pyrcc_main images.qrc -o images_rc.py"
            )
            return
        except Exception as e:
            QMessageBox.critical(self, share.locales.tr("Error"), str(e))
            return
        
        if proc.returncode != 0:
            cmd = share.locales.tr("Command")
            QMessageBox.critical(
                self,
                share.locales.tr("pyrcc5 Error"),
                f"{cmd}:\n{' '.join(cmd)}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
            )
            return
        
        msg = share.locales.tr("Resource File successfully writen")
        QMessageBox.information(
            self,
            "Fertig",
            f"{msg}:\n\n{qrc_path}\n{py_path}"
        )
    
    @staticmethod
    def _xml_escape(text: str) -> str:
        return (
            text.replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
        )
