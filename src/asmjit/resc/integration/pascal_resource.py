from __future__ import annotations

from pathlib import Path
from typing import Iterable
import os
import re
import zlib

from rccompiler.compiler import compile_resource_script


_RESOURCE_DIRECTIVE = re.compile(
    r"\{\$\s*(?:R|RESOURCE)\s+([^}]+)\}",
    re.IGNORECASE,
)


def collect_pascal_resource_directives(source: str) -> list[str]:
    result: list[str] = []
    for match in _RESOURCE_DIRECTIVE.finditer(source):
        value = match.group(1).strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in "'\""
        ):
            value = value[1:-1]
        if value and value not in result:
            result.append(value)
    return result


def _resolve_resource(
    value: str | os.PathLike[str],
    source_directory: Path,
    search_paths: Iterable[str | os.PathLike[str]],
) -> Path:
    raw = Path(
        os.path.expandvars(
            os.path.expanduser(
                os.fspath(value)
            )
        )
    )
    candidates: list[Path] = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append(source_directory / raw)
        candidates.extend(Path(path) / raw for path in search_paths)
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "resource script not found: "
        + os.fspath(value)
        + "\nsearched:\n"
        + "\n".join(f"  {candidate}" for candidate in candidates)
    )


def compile_pascal_resources(
    *,
    raw_pascal_source: str,
    source_file: str | os.PathLike[str],
    output_directory: str | os.PathLike[str],
    command_line_resources: Iterable[str] = (),
    include_paths: Iterable[str | os.PathLike[str]] = (),
    defines: Iterable[str] = (),
    codepage: int = 65001,
    verbose: bool = False,
) -> list[Path]:
    source_path = Path(source_file).resolve()
    source_directory = source_path.parent
    output_directory = Path(output_directory).resolve()
    output_directory.mkdir(parents=True, exist_ok=True)

    requested: list[str] = []
    for value in command_line_resources:
        if value not in requested:
            requested.append(value)
    for value in collect_pascal_resource_directives(raw_pascal_source):
        if value not in requested:
            requested.append(value)

    objects: list[Path] = []
    for value in requested:
        resource_file = _resolve_resource(
            value,
            source_directory,
            include_paths,
        )
        checksum = zlib.crc32(
            str(resource_file).encode("utf-8")
        ) & 0xFFFFFFFF
        object_file = output_directory / (
            f"{resource_file.stem}.{checksum:08x}.res.o"
        )
        result = compile_resource_script(
            resource_file,
            object_file,
            include_paths=[source_directory, *include_paths],
            defines=defines,
            codepage=codepage,
        )
        objects.append(result.coff.filename)
        if verbose:
            print(
                "RESOURCE:",
                resource_file,
                "->",
                result.coff.filename,
                f"({result.records_count} entries, "
                f"{result.coff.file_size} bytes)",
            )
    return objects
