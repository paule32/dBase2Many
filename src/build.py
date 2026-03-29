#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from pathlib    import Path
from typing     import Set

import sys
import shutil
import subprocess
import argparse
import re

# Marker: #[:: <filepath> ::]
MARK_RE = re.compile(r"#\s*\[\s*::\s*(?P<path>[^:\]]+?)\s*::\s*\]")


# 1) deine bisherigen Spezialblöcke (sys.version_info / "." in __name__) kannst du behalten
#    (ich lasse sie hier weg, weil du sie schon hast)

# 2) Entfernt den Qt-RCC Versions/Init Block (qt_version... bis qInitResources())
_QT_RCC_BLOCK_RE = re.compile(
    r"""
    ^[ \t]*qt_version[ \t]*=[^\r\n]*\r?\n
    ^[ \t]*if[ \t]+qt_version[ \t]*<[ \t]*\[[^\]]+\][ \t]*:\s*\r?\n
    (?:^[ \t].*\r?\n)*?
    ^[ \t]*else[ \t]*:\s*\r?\n
    (?:^[ \t].*\r?\n)*?
    ^[ \t]*def[ \t]+qInitResources\(\)\s*:\s*\r?\n
    (?:^[ \t].*\r?\n)*?
    ^[ \t]*def[ \t]+qCleanupResources\(\)\s*:\s*\r?\n
    (?:^[ \t].*\r?\n)*?
    ^[ \t]*qInitResources\(\)\s*\r?\n
    """,
    re.MULTILINE | re.VERBOSE,
)

_QT_RCC_BLOCK_REPLACEMENT = (
    "rcc_version = 2\n"
    "qt_resource_struct = qt_resource_struct_v2\n\n"
    "def qInitResources():\n"
    "    qRegisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)\n\n"
    "def qCleanupResources():\n"
    "    qUnregisterResourceData(rcc_version, qt_resource_struct, qt_resource_name, qt_resource_data)\n\n"
    "qInitResources()\n"
)

def strip_import_lines(text: str) -> str:
    out_lines = []
    for line in text.splitlines(True):
        stripped = line.lstrip()

        # 1) ANTLR Generator-Kommentar entfernen
        if re.match(r'^[ \t]*#\s*Generated\s+from\s+.*\s+by\s+ANTLR\s+\d+(\.\d+)*\s*$', stripped):
            continue

        # 2) if "." in __name__: entfernen
        if re.match(r'^[ \t]*if[ \t]+["\']\.[\"\']?[ \t]*in[ \t]+__name__[ \t]*:\s*$', stripped):
            continue

        # 3) deine sys.version_info Kontrollzeilen entfernen
        if re.match(r'^[ \t]*if[ \t]+sys\.version_info\[1\][ \t]*>[ \t]*5[ \t]*:\s*$', stripped):
            continue
        if re.match(r'^[ \t]*else[ \t]*:\s*$', stripped):
            continue

        # 4) einzelne unerwünschte Zeilen
        if stripped.startswith("from PyQt5 import QtCore"):
            continue
        if stripped.startswith("del dBaseParser"):
            continue

        # 5) alle import/from Zeilen entfernen
        if stripped.startswith("import ") or stripped.startswith("from "):
            continue

        out_lines.append(line)
        
        # QtCore. überall entfernen
        text = re.sub(r"\bQtCore\.", "", text)

        out_lines = []
        for line in text.splitlines(True):
            stripped = line.lstrip()
            # ... deine continue-Filter ...
            out_lines.append(line)

    return "".join(out_lines)

def read_text_file(path: Path) -> str:
    """Liest Textdatei als UTF-8 (mit BOM), Fallback bei Encoding-Problemen."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text()


def expand_marks(master_text: str, base_dir: Path, *, recursive: bool, _seen: Set[Path] | None = None) -> str:
    """
    Ersetzt alle #[:: filepath ::]-Marker im Text durch den gefilterten Inhalt der Datei.
    base_dir: relativ aufgelöste Pfade werden hiervon ausgehend interpretiert.
    recursive: wenn True, werden Marker im eingefügten Inhalt ebenfalls expandiert.
    """
    if _seen is None:
        _seen = set()

    def repl(match: re.Match) -> str:
        raw = match.group("path").strip()

        inc_path = (base_dir / raw).expanduser().resolve()

        if not inc_path.exists() or not inc_path.is_file():
            raise FileNotFoundError(f"Eingabedatei nicht gefunden: {raw}  ->  {inc_path}")

        if inc_path in _seen:
            raise RuntimeError(f"Zirkuläres Include erkannt: {inc_path}")

        _seen.add(inc_path)
        included = read_text_file(inc_path)
        included = strip_import_lines(included)

        if recursive:
            included = expand_marks(included, inc_path.parent, recursive=True, _seen=_seen)

        _seen.remove(inc_path)

        if included and not included.endswith("\n"):
            included += "\n"
        return included

    return MARK_RE.sub(repl, master_text)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Ersetzt #[:: filepath ::]-Marker durch Dateiinhalt (ohne import/from Zeilen)."
    )
    ap.add_argument("input", type=Path, help="Masterdatei")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Ausgabedatei (default: stdout)")
    ap.add_argument(
        "-r", "--recursive", action="store_true",
        help="Auch Marker in eingefügten Dateien expandieren (mit Zirkelschluss-Schutz)."
    )
    args = ap.parse_args()

    master_path: Path = args.input.expanduser().resolve()
    if not master_path.exists() or not master_path.is_file():
        raise FileNotFoundError(f"Masterdatei nicht gefunden: {master_path}")

    master_text = read_text_file(master_path)
    result = expand_marks(master_text, master_path.parent, recursive=args.recursive)

    if args.output:
        out_path = args.output.expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
    
    return 0


def compile_po_to_mo(po_file: str | Path, mo_file: str | Path | None = None) -> bool:
    """
    Kompiliert eine .po Datei nach .mo.
    Reihenfolge:
      1. msgfmt.exe / msgfmt
      2. polib Fallback
    
    Rückgabe:
      True  -> erfolgreich
      False -> fehlgeschlagen
    """
    po_path = Path(po_file)
    if mo_file is None:
        mo_path = po_path.with_suffix(".mo")
    else:
        mo_path = Path(mo_file)
    
    if not po_path.exists():
        print(f"PO-Datei nicht gefunden: {po_path}")
        return False
    
    mo_path.parent.mkdir(parents=True, exist_ok=True)
    
    msgfmt = shutil.which("msgfmt")
    if msgfmt:
        try:
            cmd = [msgfmt, "-o", str(mo_path), str(po_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[OK] msgfmt: {po_path} -> {mo_path}")
                return True
            
            print("[WARN] msgfmt fehlgeschlagen:")
            if result.stdout.strip():
                print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
        
        except Exception as e:
            print(f"[WARN] Fehler beim Start von msgfmt: {e}")
    
    try:
        import polib
        po = polib.pofile(str(po_path))
        po.save_as_mofile(str(mo_path))
        print(f"[OK] polib : {po_path} -> {mo_path}")
        return True
    
    except ModuleNotFoundError as e:
        if e.name == "polib":
            print("[ERROR] Weder msgfmt noch polib verfügbar.")
            print("Installiere polib mit: pip install polib")
            return False
        raise

def build_all_locales(locale_root: str | Path, domain: str = "messages") -> None:
    locale_root = Path(locale_root)

    for lang_dir in locale_root.iterdir():
        if not lang_dir.is_dir():
            continue

        po_file = lang_dir / "LC_MESSAGES" / f"{domain}.po"
        mo_file = lang_dir / "LC_MESSAGES" / f"{domain}.mo"

        if po_file.exists():
            compile_po_to_mo(po_file, mo_file)

if __name__ == "__main__":
    build_all_locales("data/po/locales", "dbase")
    
#if __name__ == "__main__":
#    raise SystemExit(main())
