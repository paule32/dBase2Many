#!/usr/bin/env python3
from __future__ import annotations

import argparse
import py_compile
import shutil
import time
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)

    if count != 1:
        raise RuntimeError(
            f"{label}: expected exactly one match, found {count}"
        )

    return text.replace(old, new, 1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Adds PE/COFF long section-name support to pe32.py."
        )
    )
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    path = args.file.resolve()
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        """        reader.read_header()
        reader.read_sections()
        reader.read_symbols()
""",
        """        reader.read_header()
        reader.read_string_table()
        reader.read_sections()
        reader.read_symbols()
"""
    )

    old = """    def section_name(self, raw):
        raw = raw.rstrip(b"\\x00")
        return raw.decode("ascii", errors="replace")

    def read_sections(self):
"""

    new = """    def read_string_table(self):
        symtab = int(self.pointer_to_symbol_table)
        strtab_offset = symtab + int(self.number_of_symbols) * 18

        if symtab > 0 and strtab_offset + 4 <= len(self.data):
            size = struct.unpack_from("<L", self.data, strtab_offset)[0]

            if size < 4:
                raise RuntimeError("invalid COFF string table size")

            strtab_end = strtab_offset + size

            if strtab_end > len(self.data):
                raise RuntimeError(
                    "COFF string table exceeds object file"
                )

            self.string_table = self.data[
                strtab_offset:
                strtab_end
            ]
        else:
            self.string_table = b"\\x04\\x00\\x00\\x00"

    def section_name(self, raw):
        raw = raw.rstrip(b"\\x00")

        if raw.startswith(b"/") and raw[1:].isdigit():
            string_offset = int(raw[1:], 10)

            if (
                string_offset < 4
                or string_offset >= len(self.string_table)
            ):
                raise RuntimeError(
                    "invalid COFF long section-name "
                    f"offset: {string_offset}"
                )

            name = self.get_string_from_table(string_offset)

            if not name:
                raise RuntimeError(
                    "empty COFF long section name at "
                    f"offset {string_offset}"
                )

            return name

        return raw.decode("ascii", errors="replace")

    def read_sections(self):
"""

    text = replace_once(
        text,
        old,
        new,
        "section-name reader"
    )

    old_symbols = """    def read_symbols(self):
        symtab = self.pointer_to_symbol_table
        strtab_offset = symtab + self.number_of_symbols * 18

        if strtab_offset + 4 <= len(self.data):
            size = struct.unpack_from("<L", self.data, strtab_offset)[0]
            self.string_table = self.data[strtab_offset:strtab_offset + size]
        else:
            self.string_table = b"\\x04\\x00\\x00\\x00"

        i = 0
"""

    new_symbols = """    def read_symbols(self):
        symtab = self.pointer_to_symbol_table

        if not self.string_table:
            self.read_string_table()

        i = 0
"""

    text = replace_once(
        text,
        old_symbols,
        new_symbols,
        "symbol string table"
    )

    backup = path.with_name(
        path.name + ".bak-" + time.strftime("%Y%m%d-%H%M%S")
    )
    shutil.copy2(path, backup)
    path.write_text(text, encoding="utf-8", newline="\n")
    py_compile.compile(str(path), doraise=True)

    print(f"Korrigiert: {path}")
    print(f"Sicherung : {backup}")
    print("Python-Syntaxprüfung erfolgreich.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
