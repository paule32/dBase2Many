# ---------------------------------------------------------------------------------------
# file: drives.py
# author: (c) 2026 Jens Kallup - paule32
# all rights reserved.
# ---------------------------------------------------------------------------------------
import os
from PyQt5.QtCore import Qt, QSettings, QDir
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTreeView,
    QFileSystemModel, QSplitter, QLineEdit,
    QPushButton, QMessageBox, QLabel
)
import share.modules.locales
from   share.modules.locales import *

# ---------------------------------------------------------------------------------------
# \brief checks if a given share exists then return true, else false ...
# ---------------------------------------------------------------------------------------
def share_exists(path: str) -> bool:
    return is_unc_path(path) and os.path.exists(path)

# ---------------------------------------------------------------------------------------
# \brief returns true if path is a windows unc path, else false.
# ---------------------------------------------------------------------------------------
def is_unc_path(path: str) -> bool:
    path = os.path.normpath(path)
    return path.startswith("\\\\")

# ---------------------------------------------------------------------------------------
# \brief joins a share base path with an optional folder.
# ---------------------------------------------------------------------------------------
def build_share_path(path: str, folder: str) -> str:
    path   = (path   or "").strip()
    folder = (folder or "").strip().strip("\\/")

    if not path:
        return ""

    if folder:
        return os.path.normpath(os.path.join(path, folder))

    return os.path.normpath(path)

def load_shared(ini_file):
    settings = QSettings(ini_file, QSettings.IniFormat)
    result   = []
    count    = settings.value("shares/count", 0, type=int)
    
    for index in range(count):
        group = f"share_{index}"
        
        name   = settings.value(f"{group}/name"  , "")
        path   = settings.value(f"{group}/path"  , "")
        folder = settings.value(f"{group}/folder", "")
        
        share_path = build_share_path(path, folder)
        
        if not name:
            name = folder or share_path
        
        result.append({
            "name"  : name,
            "path"  : share_path,
            "folder": folder,
        })
    return result

class ShareOpenDialog(QDialog):
    def __init__(self, ini_file, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle(share.locales.tr("Open File from Share"))
        self.resize(650, 320)
        
        self.ini_file       = ini_file
        self.selected_file  = ""
        self.allowed_roots  = []
        self.current_root   = ""
        
        self.share_list     = QListWidget()
        self.tree           = QTreeView()
        self.path_edit      = QLineEdit()
        
        self.open_button    = QPushButton(share.locales.tr("Open"))
        self.cancel_button  = QPushButton(share.locales.tr("Cancel"))
        
        self.model = QFileSystemModel(self)
        self.model.setFilter(
            QDir.AllDirs | QDir.Files | QDir.NoDotAndDotDot
        )
        
        self.tree.setRootIsDecorated(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setEnabled(False)

        self.tree.doubleClicked                     .connect(self.on_tree_double_clicked)
        self.share_list         .itemDoubleClicked  .connect(self.on_share_double_clicked)
        self.share_list         .currentItemChanged .connect(self.on_share_current_changed)
        self.share_list         .clicked            .connect(self.on_share_double_clicked)
        self.open_button        .clicked            .connect(self.on_open_clicked)
        self.cancel_button      .clicked            .connect(self.reject)

        self.path_edit.returnPressed.connect(self.on_path_entered)
        self.path_edit.textChanged  .connect(self.on_path_text_changed)

        self.build_ui()
        self.load_shares()

    def build_ui(self):
        main_layout = QVBoxLayout(self)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.share_list)
        splitter.addWidget(self.tree)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        main_layout.addWidget(splitter)

        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel(share.locales.tr("Path:")))
        path_layout.addWidget(self.path_edit)

        main_layout.addLayout(path_layout)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

    def load_shares(self):
        self.share_list.clear()
        self.allowed_roots.clear()

        shares = load_shared(self.ini_file)

        for share in shares:
            name = share.get("name", "")
            path = share.get("path", "")

            if not path:
                continue

            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, path)
            item.setToolTip(path)

            self.share_list.addItem(item)
            self.allowed_roots.append(os.path.normcase(os.path.normpath(path)))

        if self.share_list.count() > 0:
            self.share_list.setCurrentRow(0)
            self.try_open_share(self.share_list.item(0), show_error=False)

    def on_share_current_changed(self, current, previous):
        if current is None:
            return

        if not self.path_edit.text().strip():
            self.try_open_share(current, show_error=False)

    def on_share_double_clicked(self, item):
        self.try_open_share(item, show_error=True)

    def try_open_share(self, item, show_error=True):
        share_path = item.data(Qt.UserRole)

        if not share_path:
            return False

        if not is_unc_path(share_path):
            msg:str = share.locales.tr("Invalid Share")
            txt:str = share.locales.tr("The path is not a valide UNC-Share")
            if show_error:
                QMessageBox.warning(self, msg, f"{txt}:\n{share_path}")
            return False

        if not os.path.exists(share_path):
            msg:str = share.locales.tr("Share not reachable")
            txt:str = share.locales.tr("The share is not reachable")
            if show_error:
                QMessageBox.warning(self, msg, f"{txt}:\n{share_path}")
            return False

        self.open_path(share_path)
        return True

    def open_path(self, path):
        path = os.path.normpath(path)
        
        if self.tree.model() is None:
            self.tree.setModel(self.model)
        
        index = self.model.setRootPath(path)
        self.tree.setRootIndex(index)
        self.tree.setEnabled(True)
        
        self.current_root = path
        
        self.path_edit.blockSignals(True)
        self.path_edit.setText(path)
        self.path_edit.blockSignals(False)

    def on_path_text_changed(self, text):
        # --------------------------------------------
        # Sobald der Benutzer manuell etwas eingibt,
        # wird die Share-Auswahl links deaktiviert.
        # Dadurch kann nicht versehentlich auf andere
        # Laufwerke umgeschaltet werden.
        # --------------------------------------------
        self.share_list.setEnabled(text.strip() == "")
    
    def on_path_entered(self):
        path = self.path_edit.text().strip()
        if not path:
            self.share_list.setEnabled(True)
            return
            
        path = os.path.normpath(path)
        if not self.is_allowed_path(path):
            txt:str = share.locales.tr("Path is out of share range.")
            msg:str = share.locales.tr("Path not allowed")
            QMessageBox.warning(self, msg, f"{txt}:\n{path}")
            return
            
        if not os.path.exists(path):
            txt:str = share.locales.tr("The path could not be found")
            msg:str = share.locales.tr("Path not found")
            QMessageBox.warning(self, msg, f"{txt}:\n{path}")
            return
            
        self.open_path(path)
    
    def is_allowed_path(self, path):
        path = os.path.normpath(path)
        if is_unc_path(path):
            return True
        check_path = os.path.normcase(path)
        for root in self.allowed_roots:
            if check_path == root:
                return True
            if check_path.startswith(root + os.sep):
                return True
        return False
    
    def on_tree_double_clicked(self, index):
        path = self.model.filePath(index)
        if os.path.isdir(path):
            self.tree.setExpanded(index, not self.tree.isExpanded(index))
        else:
            self.selected_file = path
            self.accept()
    
    def on_open_clicked(self):
        index = self.tree.currentIndex()

        if not index.isValid():
            return

        path = self.model.filePath(index)

        if os.path.isdir(path):
            self.tree.expand(index)
            self.tree.scrollTo(index)
            self.open_path(path)
            return

        self.selected_file = path
        self.accept()

    def reject(self):
        self.selected_file = ""
        super().reject()

    def get_selected_file(self):
        return self.selected_file

def open_share_file_dialog(parent=None):
    dlg = ShareOpenDialog("dBaseRunner.ini", parent)

    if dlg.exec_() == QDialog.Accepted:
        return dlg.get_selected_file()

    return ""
