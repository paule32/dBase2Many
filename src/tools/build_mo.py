#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# File:   dBaseRunner.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations
from pathlib    import Path

import os
import sys
import zipfile
import shutil
import subprocess
import polib

# ---------------------------------------------------------------------------
#    Kompiliert eine .po Datei nach .mo.
#    Reihenfolge:
#      1. msgfmt.exe / msgfmt
#      2. polib Fallback
#    
#    Rückgabe:
#      True  -> erfolgreich
#      False -> fehlgeschlagen
# ---------------------------------------------------------------------------
def compile_po_to_mo(po_file: str | Path, mo_file: str | Path | None = None) -> bool:
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

def build_all_styles(style_root: str | Path, domain: str = "default") -> None:
    style_root = Path(style_root)
    
    for style_dir in style_root.iterdir():
        if not style_dir.is_dir():
            continue
            
        po_file = style_dir / f"{domain}.po"
        mo_file = style_dir / f"{domain}.mo"
        
        if po_file.exists():
            compile_po_to_mo(po_file, mo_file)

if __name__ == "__main__":
    build_all_locales("data/po/locales", "dbase")
    build_all_locales("data/po/locales", "cc")
    build_all_locales("data/po/locales", "lisp")
    build_all_locales("data/po/locales", "pascal")
    
    build_all_styles ("data/po/styles", "light")
    build_all_styles ("data/po/styles", "dark")
    
    base    = Path("data/po")

    loc_dir = base / "locales"
    css_dir = base / "styles"
    
    zip_out = Path("data/locales.zip")
    css_out = Path("data/styles.zip")
    
    dat_mo  = [ "cc.mo", "dbase.mo", "pascal.mo", "lisp.mo" ]
    loc_files = [
        base / "locales" / "de" / "LC_MESSAGES",
        base / "locales" / "en" / "LC_MESSAGES",
    ]
    css_files = [
        base / "styles" / "default" / "light.mo",
        base / "styles" / "default" / "dark.mo",
    ]
    
    out_zip = Path("data/locales.zip")
    out_css = Path("data/styles.zip")
    
    if out_zip.exists(): out_zip.unlink()
    if out_css.exists(): out_css.unlink()

    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in loc_files:
            for dat in dat_mo:
                mo = f / dat
                if not mo.exists():
                    raise SystemExit(f"Missing file for zip: {mo}")
                zf.write(mo, mo.relative_to("data").as_posix())
        zf.close()
    print(f"Created {out_zip}")
    
    with zipfile.ZipFile(out_css, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in css_files:
            if not f.exists():
                raise SystemExit(f"Missing file for zip: {f}")
            zf.write(f, f.relative_to("data").as_posix())
        zf.close()
    print(f"Created {out_css}")
