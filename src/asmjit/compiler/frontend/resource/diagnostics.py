from __future__ import annotations

from antlr4.error.ErrorListener import ErrorListener


class RcSyntaxError(RuntimeError):
    pass


class RaisingErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def syntaxError(
        self,
        recognizer,
        offendingSymbol,
        line,
        column,
        msg,
        e,
    ):
        raise RcSyntaxError(
            f"{self.filename}:{line}:{column + 1}: {msg}"
        )
