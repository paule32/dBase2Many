from __future__ import annotations

import sys

from share import run_language_app
# -----------------------------------------------------------------------
# C / C++ interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.cc.ccLexer             import ccLexer
from parse.cc.ccParser            import ccParser
from parse.cc.ccParserVisitor     import ccParserVisitor

if __name__ == "__main__":
    sys.exit(run_language_app("cc"))
