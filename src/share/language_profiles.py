from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class LanguageProfile:
    key: str
    display_name: str
    app_title: str
    program_extensions: tuple[str, ...]
    program_name_filter: str
    default_source_extension: str
    new_file_template: str = ""
    program_tab_title: str = "Programme"
    enable_compile_menu: bool = False
    notes: str = ""

    def matches_extension(self, ext: str) -> bool:
        return (ext or "").lower() in {e.lower() for e in self.program_extensions}

    @property
    def program_extensions_label(self) -> str:
        return ", ".join(self.program_extensions)


def _normalize_extensions(values: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        value = (value or "").strip().lower()
        if not value:
            continue
        if not value.startswith("."):
            value = "." + value
        if value not in result:
            result.append(value)
    return tuple(result)


_PROFILES: dict[str, LanguageProfile] = {
    "dbase": LanguageProfile(
        key="dbase",
        display_name="dBase",
        app_title="dBase Runner 2026 - (c) Jens Kallup - paule32",
        program_extensions=_normalize_extensions([".prg", ".wfm", ".frm"]),
        program_name_filter="dBase Quellcode (*.prg *.wfm *.frm)",
        default_source_extension=".prg",
        new_file_template=(
            "** END HEADER - do not delete this line\n\n"
            "CLASS Form1 OF FORM\n"
            "  // TODO\n"
            "ENDCLASS\n"
        ),
        notes="UI-Basis stammt noch aus dBaseRunner.py; Parser/Lexer werden später ersetzt.",
    ),
    "pascal": LanguageProfile(
        key="pascal",
        display_name="Pascal",
        app_title="Pascal Runner 2026 - (c) Jens Kallup - paule32",
        program_extensions=_normalize_extensions([".pas", ".pp", ".ppr", ".lpr", ".dpr"]),
        program_name_filter="Pascal Quellcode (*.pas *.pp *.ppr *.lpr *.dpr)",
        default_source_extension=".pas",
        new_file_template=(
            "program Unbenannt;\n\n"
            "begin\n"
            "  { TODO }\n"
            "end.\n"
        ),
        notes="UI-Basis stammt noch aus dBaseRunner.py; Parser/Lexer werden später ersetzt.",
    ),
    "cc": LanguageProfile(
        key="cc",
        display_name="C/C++",
        app_title="C/C++ Runner 2026 - (c) Jens Kallup - paule32",
        program_extensions=_normalize_extensions([".c", ".cc", ".cpp", ".cxx", ".h", ".hpp", ".hxx"]),
        program_name_filter="C/C++ Quellcode (*.c *.cc *.cpp *.cxx *.h *.hpp *.hxx)",
        default_source_extension=".cpp",
        new_file_template=(
            "#include <iostream>\n\n"
            "int main()\n"
            "{\n"
            "    // TODO\n"
            "    return 0;\n"
            "}\n"
        ),
        notes="UI-Basis stammt noch aus dBaseRunner.py; Parser/Lexer werden später ersetzt.",
    ),
    "lisp": LanguageProfile(
        key="lisp",
        display_name="LISP",
        app_title="LISP Runner 2026 - (c) Jens Kallup - paule32",
        program_extensions=_normalize_extensions([".lisp", ".lsp", ".l", ".cl", ".scm"]),
        program_name_filter="LISP Quellcode (*.lisp *.lsp *.l *.cl *.scm)",
        default_source_extension=".lisp",
        new_file_template=(
            ";;; unbenannt.lisp\n\n"
            "(defun main ()\n"
            "  ;; TODO\n"
            "  (format t \"Hallo Welt~%\"))\n\n"
            "(main)\n"
        ),
        notes="UI-Basis stammt noch aus dBaseRunner.py; Parser/Lexer werden später ersetzt.",
    ),
}


def get_language_profile(key: str) -> LanguageProfile:
    lookup = (key or "").strip().lower()
    if lookup not in _PROFILES:
        valid = ", ".join(sorted(_PROFILES))
        raise KeyError(f"Unbekanntes Sprachprofil: {key!r}. Erlaubt: {valid}")
    return _PROFILES[lookup]
