from __future__ import annotations

from pathlib import Path
import argparse
import sys

from .compiler import compile_resource_script


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dbm-rc",
        description=(
            "ANTLR-based Windows resource compiler: "
            ".rc to i386 COFF .o"
        ),
    )
    parser.add_argument("source", help="input .rc file")
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="output COFF32 .o file",
    )
    parser.add_argument(
        "-I", "--include",
        action="append",
        default=[],
        help="add include/resource search directory",
    )
    parser.add_argument(
        "-D", "--define",
        action="append",
        default=[],
        help="define a preprocessor macro NAME or NAME=VALUE",
    )
    parser.add_argument(
        "--codepage",
        type=int,
        default=65001,
        help="source codepage; default: UTF-8 (65001)",
    )
    parser.add_argument(
        "--dump-preprocessed",
        default=None,
        metavar="FILE",
    )
    parser.add_argument(
        "--dump-records",
        default=None,
        metavar="FILE",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    try:
        result = compile_resource_script(
            args.source,
            args.output,
            include_paths=args.include,
            defines=args.define,
            codepage=args.codepage,
            dump_preprocessed=args.dump_preprocessed,
            dump_records=args.dump_records,
        )
    except Exception as exc:
        print(f"dbm-rc: error: {exc}", file=sys.stderr)
        return 1

    if args.verbose:
        print(f"source       : {Path(args.source).resolve()}")
        print(f"output       : {result.coff.filename}")
        print(f"resources    : {result.records_count}")
        print(f".rsrc bytes  : {result.coff.section_size}")
        print(f"relocations  : {result.coff.relocation_count}")
        print(f"object bytes : {result.coff.file_size}")
        for dependency in result.source.dependencies:
            print(f"dependency   : {dependency}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
