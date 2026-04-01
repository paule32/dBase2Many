from __future__ import annotations

import sys

from share import run_language_app
# -----------------------------------------------------------------------
# LISP interpreter lexer + parser ...
# -----------------------------------------------------------------------
from parse.lisp.lispLexer           import lispLexer
from parse.lisp.lispParser          import lispParser
from parse.lisp.lispParserVisitor   import lispParserVisitor


if __name__ == "__main__":
    sys.exit(run_language_app("lisp"))
