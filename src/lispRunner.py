# ---------------------------------------------------------------------------
# \file  : lispRunner.py
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
from share.editors.lisp   import *

# -----------------------------------------------------------------------
# LISP interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.lisp.lispLexer         import lispLexer
from parse.lisp.lispParser        import lispParser
from parse.lisp.lispParserVisitor import lispParserVisitor


if __name__ == "__main__":
    sys.exit(run_language_app("lisp"))
