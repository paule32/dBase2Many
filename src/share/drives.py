# ---------------------------------------------------------------------------------------
# file: drives.py
# author: (c) 2026 Jens Kallup - paule32
# all rights reserved.
# ---------------------------------------------------------------------------------------
from __future__   import annotations

def load_shared(ini_file):
    settings = QSettings(ini_file, QSettings.IniFormat)
    result   = []
    count    = settings.value("Shares/Count", 0, type=int)

    for index in range(count):
        group = f"Share_{index}"

        path   = settings.value(f"{group}/Path"  , "")
        folder = settings.value(f"{group}/Folder", "")

        result.append({
            "path"  : path  ,
            "folder": folder,
        })

    return result
