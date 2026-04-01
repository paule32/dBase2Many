from __future__ import annotations

import sys

from share import run_language_app
# -----------------------------------------------------------------------
# Pascal / Delphi interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.pascal.pascalLexer             import pascalLexer
from parse.pascal.pascalParser            import pascalParser
from parse.pascal.pascalParserVisitor     import pascalParserVisitor


if __name__ == "__main__":
    sys.exit(run_language_app("pascal"))
