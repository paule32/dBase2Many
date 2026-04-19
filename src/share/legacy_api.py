# ---------------------------------------------------------------------------
# Schmale Kompatibilitätsschicht über dBaseRunner.py.
#
# Der Sinn dieses Moduls ist nicht, Logik zu duplizieren, sondern einen
# zentralen Importpunkt zu schaffen. Sobald einzelne Klassen aus dem
# Monolithen extrahiert werden, können die Re-Exports hier angepasst werden,
# ohne dass alle Runner-Dateien geändert werden müssen.
# ---------------------------------------------------------------------------

from __future__ import annotations

import uiRunner as legacy

# Direkter Zugriff auf das Legacy-Modul, falls später Monkey-Patching oder
# ein schrittweiser Austausch notwendig ist.
module = legacy

# Wiederverwendete Basisbausteine
ErrorMessage = legacy.ErrorMessage
CollectProgressDialog = legacy.CollectProgressDialog
CodeEditor = legacy.CodeEditor
MiniMap = legacy.MiniMap
EditorWidget = legacy.EditorWidget
FileEditorWindow = legacy.FileEditorWindow
TableDesignerDialog = legacy.TableDesignerDialog
TableRecordEditorDialog = legacy.TableRecordEditorDialog
RegieCenter = legacy.RegieCenter
IconTab = legacy.IconTab
FormDesignerWindow = legacy.FormDesignerWindow
ObjectInspectorDock = legacy.ObjectInspectorDock
ObjectPaletteDock = legacy.ObjectPaletteDock
DoxyGenToolWindow = legacy.DoxyGenToolWindow
SqlBuilderWindow = legacy.SqlBuilderWindow
SqlCanvas = legacy.SqlCanvas
SqlConnection = legacy.SqlConnection
SqlTableProxy = legacy.SqlTableProxy
MainWindow = legacy.MainWindow
parse = legacy.parse
center_on_screen = legacy.center_on_screen
ensure_qt_app = legacy.ensure_qt_app
LOG = legacy.LOG

__all__ = [
    "module",
    "ErrorMessage",
    "CollectProgressDialog",
    "CodeEditor",
    "MiniMap",
    "EditorWidget",
    "FileEditorWindow",
    "TableDesignerDialog",
    "TableRecordEditorDialog",
    "RegieCenter",
    "IconTab",
    "FormDesignerWindow",
    "DoxyGenToolWindow",
    "ObjectInspectorDock",
    "ObjectPaletteDock",
    "SqlBuilderWindow",
    "SqlCanvas",
    "SqlConnection",
    "SqlTableProxy",
    "MainWindow",
    "parse",
    "center_on_screen",
    "ensure_qt_app",
    "LOG",
]
