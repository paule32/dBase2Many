#!/usr/bin/env python3
from __future__ import annotations

import argparse
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

MODULE_TEXT = r'''# ---------------------------------------------------------------------------
# File: packed_loader_imports.py
# ---------------------------------------------------------------------------
from __future__ import annotations

PACKED_DLL_LOADER_IMPORTS = {
    "kernel32.dll": [
        {"symbol": "__imp__CloseHandle@4",       "name": "CloseHandle"},
        {"symbol": "__imp__CreateFileA@28",      "name": "CreateFileA"},
        {"symbol": "__imp__DeleteFileA@4",       "name": "DeleteFileA"},
        {"symbol": "__imp__FindResourceA@12",    "name": "FindResourceA"},
        {"symbol": "__imp__FreeLibrary@4",       "name": "FreeLibrary"},
        {"symbol": "__imp__GetLastError@0",      "name": "GetLastError"},
        {"symbol": "__imp__GetProcessHeap@0",    "name": "GetProcessHeap"},
        {"symbol": "__imp__GetTempFileNameA@16", "name": "GetTempFileNameA"},
        {"symbol": "__imp__GetTempPathA@8",      "name": "GetTempPathA"},
        {"symbol": "__imp__HeapAlloc@12",        "name": "HeapAlloc"},
        {"symbol": "__imp__HeapFree@12",         "name": "HeapFree"},
        {"symbol": "__imp__LoadLibraryA@4",      "name": "LoadLibraryA"},
        {"symbol": "__imp__LoadResource@8",      "name": "LoadResource"},
        {"symbol": "__imp__LockResource@4",      "name": "LockResource"},
        {"symbol": "__imp__SetLastError@4",      "name": "SetLastError"},
        {"symbol": "__imp__SizeofResource@8",    "name": "SizeofResource"},
        {"symbol": "__imp__WriteFile@20",        "name": "WriteFile"},
        {"symbol": "__imp__lstrcpynA@12",        "name": "lstrcpynA"},
    ],
    "zlib1.dll": [
        {"symbol": "__imp__uncompress", "name": "uncompress"},
        {"symbol": "_crc32",            "name": "crc32"},
    ],
}


def install_packed_dll_loader_imports(imports: dict) -> None:
    for dll_name, descriptors in PACKED_DLL_LOADER_IMPORTS.items():
        target = imports.setdefault(dll_name, [])
        known = set()

        for item in target:
            if isinstance(item, dict):
                known.add(item.get("symbol") or item.get("internal_name") or item.get("name"))
            elif isinstance(item, tuple) and item:
                known.add(item[0])
            elif isinstance(item, str):
                known.add(item)

        for descriptor in descriptors:
            symbol = descriptor["symbol"]
            if symbol not in known:
                target.append(dict(descriptor))
                known.add(symbol)
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("types_file", type=Path)
    args = parser.parse_args()

    target = args.types_file.resolve()
    if not target.is_file():
        parser.error(f"Datei nicht gefunden: {target}")

    raw = target.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8")

    backup = target.with_name(
        target.name + ".bak-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    )
    shutil.copy2(target, backup)

    import_block = (
        "from compiler.common.packed_loader_imports import (" + newline
        + "    install_packed_dll_loader_imports" + newline
        + ")" + newline
    )

    if "install_packed_dll_loader_imports" not in text:
        anchor = "from compiler.common.constants import *" + newline
        if anchor not in text:
            raise RuntimeError("Import-Anker in types.py nicht gefunden")
        text = text.replace(anchor, anchor + import_block, 1)

    call_block = (
        "        install_packed_dll_loader_imports(" + newline
        + "            self.imports" + newline
        + "        )" + newline + newline
    )

    if call_block.strip() not in text:
        anchor = "global CDATA" + newline
        if anchor not in text:
            raise RuntimeError("global CDATA-Anker in types.py nicht gefunden")
        text = text.replace(anchor, call_block + anchor, 1)

    target.write_text(text, encoding="utf-8", newline="")

    module_path = target.parent / "packed_loader_imports.py"
    module_path.write_text(
        MODULE_TEXT.replace("\n", newline),
        encoding="utf-8",
        newline=""
    )

    py_compile.compile(str(target), doraise=True)
    py_compile.compile(str(module_path), doraise=True)

    print(f"Korrigiert: {target}")
    print(f"Erzeugt   : {module_path}")
    print(f"Sicherung : {backup}")
    print("Python-Syntaxprüfung erfolgreich.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
