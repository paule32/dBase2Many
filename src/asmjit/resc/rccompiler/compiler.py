from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import json
import os

from antlr4 import CommonTokenStream, InputStream

from .ast_builder import ResourceAstBuilder
from .coff import CoffBuildInfo, write_coff32_resource_object
from .diagnostics import RaisingErrorListener
from .encoders import ResourceEncoder
from .preprocessor import PreprocessedSource, RcPreprocessor
from .resource_tree import ResourceSection, build_resource_section
from .generated.ResourceLexer import ResourceLexer
from .generated.ResourceParser import ResourceParser


@dataclass
class ResourceCompilerResult:
    source: PreprocessedSource
    records_count: int
    section: ResourceSection
    coff: CoffBuildInfo


def compile_resource_script(
    source_file: str | os.PathLike[str],
    output_file: str | os.PathLike[str],
    *,
    include_paths: Iterable[str | os.PathLike[str]] = (),
    defines: Iterable[str] = (),
    codepage: int = 65001,
    dump_preprocessed: str | os.PathLike[str] | None = None,
    dump_records: str | os.PathLike[str] | None = None,
) -> ResourceCompilerResult:
    source_path = Path(source_file).resolve()
    preprocessor = RcPreprocessor(
        include_paths=include_paths,
        defines=defines,
        codepage=codepage,
    )
    source = preprocessor.process(source_path)

    if dump_preprocessed is not None:
        Path(dump_preprocessed).write_text(
            source.text,
            encoding="utf-8",
        )

    lexer = ResourceLexer(
        InputStream(source.text)
    )
    lexer.removeErrorListeners()
    lexer.addErrorListener(
        RaisingErrorListener(str(source_path))
    )

    tokens = CommonTokenStream(lexer)
    parser = ResourceParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(
        RaisingErrorListener(str(source_path))
    )
    tree = parser.resourceScript()

    builder = ResourceAstBuilder(
        filename=source_path,
    )
    unit = builder.visit(tree)

    records = ResourceEncoder(
        codepage=source.codepage,
    ).encode(unit)

    if dump_records is not None:
        serializable = [
            {
                "type": record.type_id,
                "name": record.name_id,
                "language": record.language,
                "codepage": record.codepage,
                "size": len(record.data),
            }
            for record in records
        ]
        Path(dump_records).write_text(
            json.dumps(serializable, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    section = build_resource_section(records)
    coff = write_coff32_resource_object(
        output_file,
        section,
    )

    return ResourceCompilerResult(
        source=source,
        records_count=len(records),
        section=section,
        coff=coff,
    )
