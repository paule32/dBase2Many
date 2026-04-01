from __future__ import annotations

import os
from typing import Final

LANGUAGE_ALIASES: Final[dict[str, str]] = {
    "pascal": "pascal",
    "cc": "cc",
    "cpp": "cc",
    "c++": "cc",
    "lisp": "lisp",
    "dbase": "dbase",
}


def run_language_app(language: str) -> int:
    """
    Startet die gemeinsame Runner-Oberfläche auf Basis von dBaseRunner.py.

    Die konkrete Sprache wird aktuell über eine Environment-Variable signalisiert,
    damit die gemeinsame GUI später sprachspezifische Parser/Lexer, Dateifilter,
    Templates und Compile-Ziele umschalten kann.
    """
    normalized = LANGUAGE_ALIASES.get((language or "").strip().lower(), "dbase")
    os.environ["DBASERUNNER_LANGUAGE"] = normalized

    import dBaseRunner

    try:
        dBaseRunner.main()
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else 0
    return 0
