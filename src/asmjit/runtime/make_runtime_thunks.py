#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# File:   make_runtime_thunks.py
# Purpose:
#   Read a Win32 .def file and generate one NASM/COFF32 thunk object per
#   exported ordinal. The resulting archive allows the linker to pull only
#   the thunks that are actually referenced.
#
# Example:
#   python make_runtime_thunks.py libruntime_all.def
#
# Output:
#   runtime_thunks/
#       thunk_001_jit_dynarray_setlength.asm
#       thunk_001_jit_dynarray_setlength.o
#       ...
#       libdll_runtime_thunks.a
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


SECTION_KEYWORDS = {
    "LIBRARY",
    "NAME",
    "DESCRIPTION",
    "STACKSIZE",
    "HEAPSIZE",
    "CODE",
    "DATA",
    "SECTIONS",
    "VERSION",
    "IMPORTS",
    "EXPORTS",
}

EXPORT_RE = re.compile(
    r"""
    ^\s*
    (?P<symbol>
        "(?:[^"]|"")*"
        |
        '(?:[^']|'')*'
        |
        \S+
    )
    \s+
    @(?P<ordinal>\d+)
    (?P<flags>(?:\s+.*)?)
    $
    """,
    re.VERBOSE | re.IGNORECASE,
)


@dataclass(frozen=True)
class DefExport:
    symbol: str
    ordinal: int
    flags: tuple[str, ...]
    source_line: int


def strip_def_comment(line: str) -> str:
    """Remove a DEF ';' comment while respecting quoted strings."""
    quote: str | None = None

    for index, char in enumerate(line):
        if quote is None:
            if char in ("'", '"'):
                quote = char
            elif char == ";":
                return line[:index]
        elif char == quote:
            # DEF files commonly escape a quote by doubling it.
            if index + 1 < len(line) and line[index + 1] == quote:
                continue
            quote = None

    return line


def unquote_def_name(value: str) -> str:
    value = value.strip()

    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        quote = value[0]
        return value[1:-1].replace(quote * 2, quote)

    return value


def exported_symbol_name(value: str) -> str:
    """
    DEF aliases may look like:
        public_name=internal_name

    The thunk must define the public symbol referenced by generated code,
    therefore the left-hand side is used.
    """
    value = unquote_def_name(value)

    if "=" in value:
        value = value.split("=", 1)[0].strip()

    if not value:
        raise ValueError("empty exported symbol")

    return value


def parse_def_file(def_file: Path) -> tuple[str | None, list[DefExport]]:
    library_name: str | None = None
    exports: list[DefExport] = []
    in_exports = False

    text = def_file.read_text(encoding="utf-8-sig")

    for line_number, original_line in enumerate(text.splitlines(), start=1):
        line = strip_def_comment(original_line).strip()

        if not line:
            continue

        first_word = line.split(None, 1)[0].upper()

        if first_word == "LIBRARY":
            remainder = line[len(line.split(None, 1)[0]):].strip()
            if remainder:
                library_name = unquote_def_name(remainder.split(None, 1)[0])
            continue

        if first_word == "EXPORTS":
            in_exports = True
            continue

        if in_exports and first_word in SECTION_KEYWORDS:
            in_exports = first_word == "EXPORTS"
            continue

        if not in_exports:
            continue

        match = EXPORT_RE.match(line)
        if match is None:
            raise ValueError(
                f"{def_file}:{line_number}: unsupported EXPORTS line:\n"
                f"    {original_line}"
            )

        symbol = exported_symbol_name(match.group("symbol"))
        ordinal = int(match.group("ordinal"), 10)

        if not 1 <= ordinal <= 0xFFFF:
            raise ValueError(
                f"{def_file}:{line_number}: ordinal {ordinal} is outside 1..65535"
            )

        flags = tuple(
            token.upper()
            for token in match.group("flags").split()
        )

        exports.append(
            DefExport(
                symbol=symbol,
                ordinal=ordinal,
                flags=flags,
                source_line=line_number,
            )
        )

    if not exports:
        raise ValueError(f"{def_file}: no ordinal exports found")

    seen_symbols: dict[str, DefExport] = {}
    seen_ordinals: dict[int, DefExport] = {}

    for item in exports:
        symbol_key = item.symbol.casefold()

        if symbol_key in seen_symbols:
            previous = seen_symbols[symbol_key]
            raise ValueError(
                f"{def_file}:{item.source_line}: duplicate symbol {item.symbol!r}; "
                f"first declared on line {previous.source_line}"
            )

        if item.ordinal in seen_ordinals:
            previous = seen_ordinals[item.ordinal]
            raise ValueError(
                f"{def_file}:{item.source_line}: duplicate ordinal @{item.ordinal}; "
                f"first used by {previous.symbol!r} on line "
                f"{previous.source_line}"
            )

        seen_symbols[symbol_key] = item
        seen_ordinals[item.ordinal] = item

    exports.sort(key=lambda item: item.ordinal)
    return library_name, exports


def filename_component(symbol: str) -> str:
    value = symbol.lstrip("_")
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value)
    value = value.strip("._")

    return value or "symbol"


def make_asm_source(
    item: DefExport,
    table_symbol: str,
    section_alignment: int,
) -> str:
    return f"""; Auto-generated from a DEF file. Do not edit.
bits 32

section .text align={section_alignment}

global {item.symbol}
extern {table_symbol}

{item.symbol}:
    jmp dword [{table_symbol} + {item.ordinal} * 4]
"""


def run_command(command: list[str], cwd: Path | None = None) -> None:
    printable = subprocess.list2cmdline(command)
    print(f"> {printable}")

    subprocess.run(
        command,
        cwd=str(cwd) if cwd is not None else None,
        check=True,
    )


def resolve_program(program: str) -> str:
    path = shutil.which(program)

    if path is None:
        raise FileNotFoundError(
            f"program not found: {program!r}"
        )

    return path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate one NASM win32 thunk object per ordinal export "
            "and combine them into a static archive."
        )
    )
    parser.add_argument(
        "def_file",
        type=Path,
        help="input DEF file",
    )
    parser.add_argument(
        "-o",
        "--output-directory",
        type=Path,
        default=Path("runtime_thunks"),
        help="directory for generated ASM and object files",
    )
    parser.add_argument(
        "-a",
        "--archive",
        type=Path,
        default=None,
        help=(
            "archive output path; default: "
            "<output-directory>/libdll_runtime_thunks.a"
        ),
    )
    parser.add_argument(
        "--nasm",
        default="nasm.exe",
        help="NASM executable (default: nasm.exe)",
    )
    parser.add_argument(
        "--ar",
        default="ar.exe",
        help="archiver executable (default: ar.exe)",
    )
    parser.add_argument(
        "--table-symbol",
        default="_dbm_runtime_proc_table",
        help=(
            "COFF symbol of the ordinal-indexed function table "
            "(default: _dbm_runtime_proc_table)"
        ),
    )
    parser.add_argument(
        "--section-alignment",
        type=int,
        default=1,
        choices=(1, 2, 4, 8, 16),
        help=".text section alignment in generated NASM files",
    )
    parser.add_argument(
        "--keep-asm",
        action="store_true",
        help="keep generated .asm files after successful assembly",
    )
    parser.add_argument(
        "--asm-only",
        action="store_true",
        help="generate .asm files, but do not assemble or archive",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="remove the output directory before generation",
    )

    args = parser.parse_args()

    def_file = args.def_file.resolve()
    output_directory = args.output_directory.resolve()

    if not def_file.is_file():
        parser.error(f"DEF file not found: {def_file}")

    if args.clean and output_directory.exists():
        shutil.rmtree(output_directory)

    output_directory.mkdir(parents=True, exist_ok=True)

    library_name, exports = parse_def_file(def_file)

    archive = (
        args.archive.resolve()
        if args.archive is not None
        else output_directory / "libdll_runtime_thunks.a"
    )

    asm_files: list[Path] = []
    object_files: list[Path] = []
    manifest_exports: list[dict[str, object]] = []

    for item in exports:
        stem = (
            f"thunk_{item.ordinal:05d}_"
            f"{filename_component(item.symbol)}"
        )

        asm_file = output_directory / f"{stem}.asm"
        object_file = output_directory / f"{stem}.o"

        asm_file.write_text(
            make_asm_source(
                item=item,
                table_symbol=args.table_symbol,
                section_alignment=args.section_alignment,
            ),
            encoding="ascii",
            newline="\n",
        )

        asm_files.append(asm_file)
        object_files.append(object_file)

        manifest_exports.append(
            {
                "symbol": item.symbol,
                "ordinal": item.ordinal,
                "flags": list(item.flags),
                "asm": asm_file.name,
                "object": object_file.name,
            }
        )

    manifest = {
        "source_def": str(def_file),
        "library": library_name,
        "table_symbol": args.table_symbol,
        "export_count": len(exports),
        "exports": manifest_exports,
    }

    manifest_file = output_directory / "runtime_thunks.json"
    manifest_file.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"DEF file : {def_file}")
    print(f"Library  : {library_name or '(not specified)'}")
    print(f"Exports  : {len(exports)}")
    print(f"Output   : {output_directory}")

    if args.asm_only:
        print("ASM-only mode: no object files or archive were created.")
        return 0

    nasm = resolve_program(args.nasm)
    ar = resolve_program(args.ar)

    for asm_file, object_file in zip(asm_files, object_files):
        run_command(
            [
                nasm,
                "-f",
                "win32",
                asm_file.name,
                "-o",
                object_file.name,
            ],
            cwd=output_directory,
        )

    archive.parent.mkdir(parents=True, exist_ok=True)

    if archive.exists():
        archive.unlink()

    # 153 short object names remain comfortably below the Windows command-line
    # limit. Using only member filenames also keeps the command compact.
    run_command(
        [
            ar,
            "rcs",
            str(archive),
            *[object_file.name for object_file in object_files],
        ],
        cwd=output_directory,
    )

    if not args.keep_asm:
        for asm_file in asm_files:
            asm_file.unlink(missing_ok=True)

    print(f"Archive  : {archive}")
    print(f"Manifest : {manifest_file}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
