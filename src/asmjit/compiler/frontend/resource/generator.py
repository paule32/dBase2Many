# ---------------------------------------------------------------------------
# File: generator.py - Resource Compiler
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import os
import sys
import re
import json

from pathlib     import Path
from dataclasses import dataclass, field
from antlr4      import *

from compiler.frontend.pascal.preprocessor   import PascalPreprocessor
from compiler.frontend.dllimports            import *

from parsers.resrc.ResourceLexer          import ResourceLexer
from parsers.resrc.ResourceParser         import ResourceParser
from parsers.resrc.ResourceParserVisitor  import ResourceParserVisitor

from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.constants import *

from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.frontend.generatorbase import *

from compiler.common.constants import (
    LIBDBASE2MANY32_IMPORT_ORDINALS
)

class ResourceGenerator(CodeGeneratorBase, ResourceParserVisitor):
    def __init__(self, backend, writer):
        CodeGeneratorBase    .__init__(self, backend)
        ResourceParserVisitor.__init__(self)

        self.backend   = backend
        self.writer    = backend.writer
        self.coff      = backend.writer

        result = self.compile_resource_script(
            CDATA.src_file,
            CDATA.out_dir,
            include_paths = CDATA.inc_dir,
            defines       = CDATA.Defines,
            codepage      = CDATA.code_page
        )

    def compile_resource_script(
        self,
        src_file     : str,
        out_dir      : str,
        include_paths: list,
        defines      : list,
        codepage     : int):
        
        pass
