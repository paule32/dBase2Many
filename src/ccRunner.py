# ---------------------------------------------------------------------------
# \file  : ccRunner.py
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
from share.editors.cc     import *

# -----------------------------------------------------------------------
# C / C++ interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.cc.ccLexer         import ccLexer
from parse.cc.ccParser        import ccParser
from parse.cc.ccParserVisitor import ccParserVisitor

if __name__ == "__main__":
    sys.exit(run_language_app("cc"))
