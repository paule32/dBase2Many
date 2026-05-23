# ---------------------------------------------------------------------------
# File:   theme.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__    import annotations

from share.common  import *
from share.locales import *

def apply_theme_global(w: QWidget):
    app = QApplication.instance()
    pal = QPalette()
    print(w)
    w.dark_mode = True
    if w.dark_mode:
        pal.setColor(QPalette.Window, QColor(40, 40, 40))
        pal.setColor(QPalette.WindowText, Qt.black)
        pal.setColor(QPalette.Base, QColor(34, 34, 34))
        pal.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        pal.setColor(QPalette.Text, Qt.white)
        pal.setColor(QPalette.Button, QColor(45, 45, 45))
        pal.setColor(QPalette.ButtonText, Qt.white)
        pal.setColor(QPalette.Highlight, QColor(80, 120, 200))
        pal.setColor(QPalette.HighlightedText, Qt.white)
    else:
        pal = app.style().standardPalette()
    
    app.setPalette(pal)
    
    if w.dark_mode: w.setStyleSheet(share.locales.tr("runner_dark_css" ))
    else:           w.setStyleSheet(share.locales.tr("runner_light_css"))
