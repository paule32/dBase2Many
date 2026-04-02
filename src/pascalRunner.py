# ---------------------------------------------------------------------------
# \file  : pascalRunner.py
# \author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# \note  : All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import sys

from share import run_language_app

# -----------------------------------------------------------------------
# graphical widgets for user interface ...
# -----------------------------------------------------------------------
from share.widgets.button import *
from share.editors.pascal import *

# -----------------------------------------------------------------------
# Pascal / Delphi interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.pascal.pascalLexer         import pascalLexer
from parse.pascal.pascalParser        import pascalParser
from parse.pascal.pascalParserVisitor import pascalParserVisitor

if __name__ == "__main__":
    sys.exit(run_language_app("pascal"))
