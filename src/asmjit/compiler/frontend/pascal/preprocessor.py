# ---------------------------------------------------------------------------
# File: preprocessor.py - Pascal pre-Processor
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import os
import re
import sys

from datetime import datetime
from typing   import TextIO

class PascalPreprocessorError(Exception):
    pass

class ConditionalExpressionError(PascalPreprocessorError):
    pass
    
# wird durch {$ERROR ...} ausgelöst.
class PascalDirectiveAbort(Exception):
    def __init__(
        self,
        filename: str,
        line: int,
        column: int,
        message: str
    ):
        message = str(message)
        super().__init__(message)

        self.filename = filename
        self.line = int(line)
        self.column = int(column)
        self.message = message

# ---------------------------------------------------------------------------
#  Unterstützt:
#
#      {$INFO ...}
#      {$WARN ...}
#      {$WARNING ...}
#      {$NOTE ...}
#      {$ERROR ...}
#
#      {$__LINE__}
#      {$__FILE__}
#      {$__DATE__}
#      {$__TIME__}
#
#  Intrinsics dürfen auch innerhalb einer Meldung stehen:
#
#      {$INFO Datei {$__FILE__}, Zeile {$__LINE__}}
# ---------------------------------------------------------------------------
class PascalCompilerDirectiveExpander:
    _DIAGNOSTIC_LEVELS = {
        "info": "INFO",
        "warn": "WARN",
        "warning": "WARN",
        "note": "NOTE",
        "error": "ERROR"
    }

    _DIRECTIVE_RE = re.compile(
        r"\s*([A-Za-z_][A-Za-z0-9_]*)",
        re.DOTALL
    )

    def __init__(
        self,
        output: TextIO | None = None
    ):
        self.output = output or sys.stderr

    def process(
        self,
        source  : str,
        filename: str  | None = None,
        macros  : dict | None = None
    ) -> str:
        if source is None:
            return ""

        if filename:
            filename = os.path.normpath(
                os.path.abspath(filename)
            )
        else:
            filename = "<unknown>"

        macro_values = {
            str(name).upper(): value
            for name, value in (macros or {}).items()
        }

        compile_datetime = datetime.now()
        compile_date = compile_datetime.strftime("%Y-%m-%d")
        compile_time = compile_datetime.strftime("%H:%M:%S")

        result: list[str] = []

        index = 0
        line = 1
        column = 1
        length = len(source)

        while index < length:
            # Pascal-String überspringen.
            if source[index] in ("'", '"'):
                end = self._scan_pascal_string(
                    source,
                    index
                )

                fragment = source[index:end]
                result.append(fragment)

                line, column = self._advance_position(
                    fragment,
                    line,
                    column
                )

                index = end
                continue

            # //-Kommentar überspringen.
            if source.startswith("//", index):
                end = source.find("\n", index)

                if end < 0:
                    end = length

                fragment = source[index:end]
                result.append(fragment)

                line, column = self._advance_position(
                    fragment,
                    line,
                    column
                )

                index = end
                continue

            # (* ... *)-Kommentar überspringen.
            if source.startswith("(*", index):
                end = source.find("*)", index + 2)

                if end < 0:
                    end = length
                else:
                    end += 2

                fragment = source[index:end]
                result.append(fragment)

                line, column = self._advance_position(
                    fragment,
                    line,
                    column
                )

                index = end
                continue

            # Compiler-Direktive.
            if source.startswith("{$", index):
                directive_line = line
                directive_column = column

                raw_directive, end = self._read_brace_directive(
                    source,
                    index,
                    filename=filename,
                    line=line,
                    column=column
                )

                replacement = self._handle_directive(
                    raw_directive   = raw_directive,
                    filename        = filename,
                    line            = directive_line,
                    column          = directive_column,
                    compile_date    = compile_date,
                    compile_time    = compile_time,
                    macros          = macro_values
                )

                result.append(replacement)

                line, column = self._advance_position(
                    raw_directive,
                    line,
                    column
                )

                index = end
                continue

            # Normaler {...}-Kommentar.
            if source[index] == "{":
                end = source.find("}", index + 1)

                if end < 0:
                    end = length
                else:
                    end += 1

                fragment = source[index:end]
                result.append(fragment)

                line, column = self._advance_position(
                    fragment,
                    line,
                    column
                )

                index = end
                continue

            char = source[index]
            result.append(char)

            if char == "\n":
                line += 1
                column = 1
            else:
                column += 1

            index += 1

        return "".join(result)

    def _handle_directive(
        self,
        raw_directive: str,
        filename     : str,
        line         : int,
        column       : int,
        compile_date : str,
        compile_time : str,
        macros       : dict
    ) -> str:
        if not (
            raw_directive.startswith("{$")
            and raw_directive.endswith("}")
        ):
            return raw_directive

        body = raw_directive[2:-1]
        match = self._DIRECTIVE_RE.match(body)

        if match is None:
            return raw_directive

        name = match.group(1).lower()
        rest = body[match.end():]

        # Intrinsics im normalen Pascal-Quelltext.
        if name == "__line__":
            return str(line)

        if name == "__file__":
            return self._pascal_string_literal(
                filename
            )

        if name == "__date__":
            return self._pascal_string_literal(
                compile_date
            )

        if name == "__time__":
            return self._pascal_string_literal(
                compile_time
            )

        level = self._DIAGNOSTIC_LEVELS.get(name)

        # --------------------------------------------------------------
        # Benutzerdefiniertes Makro
        #
        # Beispiel:
        #
        #     {$define VERSION 1}
        #     WriteLn({$VERSION});
        #
        # Der Makroname ist nicht fest programmiert. Jeder Eintrag aus
        # dem Makro-Wörterbuch kann verwendet werden.
        # --------------------------------------------------------------
        if level is None:
            macro_name = name.upper()

            # Ein Wertmakro darf keinen weiteren Text enthalten.
            #
            # {$VERSION}       -> gültig
            # {$VERSION abc}   -> bleibt eine unbekannte Direktive
            if (
                not rest.strip()
                and macro_name in macros
            ):
                return self._macro_to_pascal_source(
                    macros[macro_name]
                )

            # Andere Compiler-Direktiven, etwa {$LINK ...}, bleiben
            # unverändert.
            return raw_directive

        message_line = (
            line
            + body[:match.end()].count("\n")
        )

        message = self._expand_message_intrinsics(
            text=rest.strip(),
            filename=filename,
            start_line=message_line,
            compile_date=compile_date,
            compile_time=compile_time,
            macros=macros
        )

        if not message:
            message = "(no message)"

        display_filename = os.path.basename(
            filename
        )

        formatted = (
            f"{display_filename}:"
            f"{line}:"
            f"{column}: "
            f"{level}: "
            f"{message}"
        )

        print(
            formatted,
            file=self.output
        )

        if level == "ERROR":
            raise PascalDirectiveAbort(
                filename=filename,
                line=line,
                column=column,
                message=message
            )

        return self._blank_preserving_lines(
            raw_directive
        )

    def _macro_to_pascal_source(
        self,
        value
    ) -> str:
        """
        Wandelt einen Python-Makrowert in gültigen Pascal-Quelltext um.

        Beispiele:

            1           -> 1
            3.14        -> 3.14
            True        -> True
            False       -> False
            "Community" -> 'Community'
        """

        # bool muss vor int geprüft werden, weil bool in Python von int
        # abgeleitet ist.
        if isinstance(value, bool):
            return (
                "True"
                if value
                else "False"
            )

        if isinstance(value, int):
            return str(value)

        if isinstance(value, float):
            return format(
                value,
                ".17g"
            )

        if isinstance(value, str):
            return self._pascal_string_literal(
                value
            )

        raise TypeError(
            "unsupported macro value type: "
            f"{type(value).__name__}"
        )

    def _expand_message_intrinsics(
        self,
        text        : str,
        filename    : str,
        start_line  : int,
        compile_date: str,
        compile_time: str,
        macros      : dict
    ) -> str:
        result: list[str] = []

        index = 0
        line = start_line
        length = len(text)

        while index < length:
            if text.startswith("{$", index):
                raw_directive, end = self._read_brace_directive(
                    text,
                    index,
                    filename = filename,
                    line     = line,
                    column   = index + 1
                )

                body  = raw_directive[2:-1]
                match = self._DIRECTIVE_RE.match(body)

                name = match.group(1).lower()
                rest = body[match.end():].strip()

                if name == "__line__":
                    result.append(
                        str(line)
                    )

                elif name == "__file__":
                    result.append(
                        filename
                    )

                elif name == "__date__":
                    result.append(
                        compile_date
                    )

                elif name == "__time__":
                    result.append(
                        compile_time
                    )

                elif (
                    not rest
                    and name.upper() in macros
                ):
                    result.append(
                        self._macro_to_message_text(
                            macros[name.upper()]
                        )
                    )

                else:
                    result.append(
                        raw_directive
                    )

                line += raw_directive.count("\n")
                index = end
                continue

            char = text[index]
            result.append(char)

            if char == "\n":
                line += 1

            index += 1

        return "".join(result).strip()

    @staticmethod
    def _macro_to_message_text(value) -> str:
        # -----------------------------------------------------------------
        # Wandelt einen Makrowert in normalen Meldungstext um.
        # Hier werden bei Strings keine Pascal-Anführungszeichen erzeugt.
        # -----------------------------------------------------------------
        if isinstance(value, bool):
            return (
                "True"
                if value
                else "False"
            )

        if isinstance(value, float):
            return format(
                value,
                ".17g"
            )

        return str(value)
    
    def _read_brace_directive(
        self,
        source   : str,
        start    : int,
        filename : str = "<unknown>",
        line     : int = 1,
        column   : int = 1
    ) -> tuple[str, int]:
        if not source.startswith("{$", start):
            raise ValueError(
                "directive must start with {$"
            )

        index = start
        depth = 0
        length = len(source)

        while index < length:
            if source.startswith("{$", index):
                depth += 1
                index += 2
                continue

            if source[index] == "}":
                depth -= 1
                index += 1

                if depth == 0:
                    return (
                        source[start:index],
                        index
                    )

                continue

            index += 1

        raise PascalDirectiveAbort(
            filename=filename,
            line=line,
            column=column,
            message="unterminated compiler directive"
        )

    @staticmethod
    def _scan_pascal_string(
        source: str,
        start: int
    ) -> int:
        quote = source[start]
        index = start + 1
        length = len(source)

        while index < length:
            if source[index] != quote:
                index += 1
                continue

            if (
                index + 1 < length
                and source[index + 1] == quote
            ):
                index += 2
                continue

            return index + 1

        return length

    @staticmethod
    def _blank_preserving_lines(
        text: str
    ) -> str:
        return "".join(
            char if char in ("\r", "\n") else " "
            for char in text
        )

    @staticmethod
    def _pascal_string_literal(
        value: str
    ) -> str:
        escaped = str(value).replace(
            "'",
            "''"
        )

        return "'" + escaped + "'"

    @staticmethod
    def _advance_position(
        text: str,
        line: int,
        column: int
    ) -> tuple[int, int]:
        newline_count = text.count("\n")

        if newline_count == 0:
            return (
                line,
                column + len(text)
            )

        line += newline_count

        last_newline = text.rfind("\n")
        column = len(text) - last_newline

        return line, column

# -------------------------------------------------------------------------
# Sicherer Ausdrucksparser für:
#
#   VERSION == 1
#   MINOR >= 2 AND MINOR <= 3
#   DEFINED(DEBUG)
#   NOT DEFINED(RELEASE)
#  (VERSION == 1) OR (VERSION == 2)
# -------------------------------------------------------------------------
class ConditionalExpressionParser:
    TOKEN_RE = re.compile(
        r"""
        (?P<SPACE>       \s+)
      | (?P<HEX>         \$[0-9A-Fa-f]+ | 0[xX][0-9A-Fa-f]+)
      | (?P<NUMBER>      [0-9]+)
      | (?P<STRING>      '(?:''|[^'])*' | "(?:""|[^"])*")
      | (?P<OP>          == | != | <> | >= | <= | = | > | < |
                         \( | \) | \+ | -)
      | (?P<IDENT>       [A-Za-z_][A-Za-z0-9_]*)
      | (?P<MISMATCH>    .)
        """,
        re.VERBOSE
    )

    def __init__(
        self,
        expression,
        macros
    ):
        self.expression = str(expression)
        self.macros = macros
        self.tokens = self.tokenize(
            self.expression
        )
        self.position = 0

    def tokenize(
        self,
        expression
    ):
        tokens = []

        for match in self.TOKEN_RE.finditer(
            expression
        ):
            kind = match.lastgroup
            value = match.group(0)

            if kind == "SPACE":
                continue

            if kind == "MISMATCH":
                raise ConditionalExpressionError(
                    f"invalid character in condition: {value!r}"
                )

            tokens.append(
                (kind, value, match.start())
            )

        tokens.append(
            ("EOF", "", len(expression))
        )

        return tokens

    def peek(self):
        return self.tokens[self.position]

    def consume(self):
        token = self.peek()
        self.position += 1
        return token

    def accept_operator(
        self,
        operator
    ):
        kind, value, _ = self.peek()

        if kind == "OP" and value == operator:
            self.position += 1
            return True

        return False

    def accept_word(
        self,
        word
    ):
        kind, value, _ = self.peek()

        if (
            kind == "IDENT"
            and value.upper() == word.upper()
        ):
            self.position += 1
            return True

        return False

    def expect_operator(
        self,
        operator
    ):
        if self.accept_operator(operator):
            return

        _, value, position = self.peek()

        raise ConditionalExpressionError(
            f"expected {operator!r} at position {position}, "
            f"found {value!r}"
        )

    def expect_identifier(self):
        kind, value, position = self.peek()

        if kind != "IDENT":
            raise ConditionalExpressionError(
                f"expected identifier at position {position}, "
                f"found {value!r}"
            )

        self.position += 1
        return value

    def parse(self):
        if not self.expression.strip():
            raise ConditionalExpressionError(
                "empty conditional expression"
            )

        result = self.parse_or()

        kind, value, position = self.peek()

        if kind != "EOF":
            raise ConditionalExpressionError(
                f"unexpected token {value!r} "
                f"at position {position}"
            )

        return self.to_boolean(result)

    def parse_or(self):
        value = self.parse_and()

        while self.accept_word("OR"):
            right = self.parse_and()

            value = (
                self.to_boolean(value)
                or self.to_boolean(right)
            )

        return value

    def parse_and(self):
        value = self.parse_not()

        while self.accept_word("AND"):
            right = self.parse_not()

            value = (
                self.to_boolean(value)
                and self.to_boolean(right)
            )

        return value

    def parse_not(self):
        if self.accept_word("NOT"):
            return not self.to_boolean(
                self.parse_not()
            )

        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_primary()

        kind, operator, _ = self.peek()

        if (
            kind != "OP"
            or operator not in (
                "=",
                "==",
                "!=",
                "<>",
                "<",
                "<=",
                ">",
                ">="
            )
        ):
            return left

        self.consume()
        right = self.parse_primary()

        try:
            if operator in ("=", "=="):
                return left == right

            if operator in ("!=", "<>"):
                return left != right

            if operator == "<":
                return left < right

            if operator == "<=":
                return left <= right

            if operator == ">":
                return left > right

            if operator == ">=":
                return left >= right

        except TypeError as exc:
            raise ConditionalExpressionError(
                f"cannot compare {left!r} and {right!r}"
            ) from exc

        raise ConditionalExpressionError(
            f"unsupported comparison operator: {operator}"
        )

    def parse_primary(self):
        if self.accept_operator("("):
            value = self.parse_or()
            self.expect_operator(")")
            return value

        if self.accept_operator("+"):
            value = self.parse_primary()

            if not isinstance(value, int):
                raise ConditionalExpressionError(
                    "unary + requires an integer"
                )

            return value

        if self.accept_operator("-"):
            value = self.parse_primary()

            if not isinstance(value, int):
                raise ConditionalExpressionError(
                    "unary - requires an integer"
                )

            return -value

        if self.accept_word("DEFINED"):
            if self.accept_operator("("):
                name = self.expect_identifier()
                self.expect_operator(")")
            else:
                name = self.expect_identifier()

            return name.upper() in self.macros

        kind, value, position = self.consume()

        if kind == "NUMBER":
            return int(value, 10)

        if kind == "HEX":
            if value.startswith("$"):
                return int(value[1:], 16)

            return int(value, 16)

        if kind == "STRING":
            quote = value[0]
            content = value[1:-1]

            return content.replace(
                quote + quote,
                quote
            )

        if kind == "IDENT":
            upper_name = value.upper()

            if upper_name == "TRUE":
                return True

            if upper_name == "FALSE":
                return False

            return self.macros.get(
                upper_name,
                0
            )

        raise ConditionalExpressionError(
            f"expected value at position {position}, "
            f"found {value!r}"
        )

    @staticmethod
    def to_boolean(
        value
    ):
        if isinstance(value, str):
            return len(value) > 0

        return bool(value)

# ---------------------------------------------------------------------------
#  Unterstützt:
#
#    {$DEFINE NAME}
#    {$DEFINE VERSION 1}
#    {$DEFINE VERSION = 1}
#    {$UNDEF NAME}
#
#    {$IFDEF NAME}
#    {$IFNDEF NAME}
#
#    {$IF VERSION == 1}
#    {$IF MINOR >= 2 AND MINOR <= 3}
#    {$ELSEIF VERSION == 2}
#    {$ELIF VERSION == 3}
#    {$ELSE}
#    {$ENDIF}
# ---------------------------------------------------------------------------
class PascalPreprocessor:
    CONTROL_DIRECTIVE_RE = re.compile(
        r"""
        ^\s*
        \{\$
        \s*
        (
            DEFINE
          | UNDEF
          | IFDEF
          | IFNDEF
          | IF
          | ELSEIF
          | ELIF
          | ELSE
          | ENDIF
        )
        \b
        (.*?)
        \}
        \s*
        (?://.*)?
        (?:\r?\n)?
        $
        """,
        re.IGNORECASE | re.VERBOSE
    )

    def __init__(self, defines=None):
        # Makroname -> Makrowert
        #
        # Beispiele:
        #
        #     VERSION -> 1
        #     PRODUCT -> "dBase2Many"
        #     DEBUG   -> True
        self.macros = {}

        # Für Kompatibilität mit bestehendem Code.
        self.defines = set()

        # Nur Makros, die durch {$DEFINE ...} in dieser Datei
        # definiert wurden.
        self.source_macros = {}

        self.compiler_directives = (
            PascalCompilerDirectiveExpander()
        )

        self.add_initial_defines(
            defines or []
        )

    def add_initial_defines(self, defines):
        if isinstance(defines, dict):
            for name, value in defines.items():
                self.define(
                    name,
                    value
                )
            return

        for item in defines:
            text = str(item).strip()

            if not text:
                continue

            if "=" in text:
                name, value = text.split(
                    "=",
                    1
                )
                self.define(
                    name.strip(),
                    self.parse_macro_value(
                        value.strip()
                    )
                )
            else:
                self.define(text, True)

    def is_defined(self, name):
        return str(name).upper() in self.macros

    def get_macro(
        self,
        name,
        default=0
    ):
        return self.macros.get(
            str(name).upper(),
            default
        )

    def define(self, name, value = True, source_defined = False):
        name = str(name).strip()

        if not name:
            raise RuntimeError(
                "macro name must not be empty"
            )

        key = name.upper()

        self.macros[key] = value
        self.defines.add(key)

        if source_defined:
            self.source_macros[key] = value

    def undef(self, name):
        key = str(name).strip().upper()

        self.macros       .pop(key, None)
        self.source_macros.pop(key, None)
        
        self.defines.discard(key)

    def process_define_argument(
        self,
        argument,
        filename,
        line_number
    ):
        match = re.match(
            r"^([A-Za-z_][A-Za-z0-9_]*)(.*)$",
            argument.strip()
        )

        if match is None:
            raise PascalPreprocessorError(
                f"{filename}:{line_number}: "
                "invalid {$DEFINE} directive"
            )

        name = match.group(1)
        value_text = match.group(2).strip()

        if value_text.startswith(":="):
            value_text = value_text[2:].strip()

        elif value_text.startswith("="):
            value_text = value_text[1:].strip()

        if not value_text:
            value = True
        else:
            value = self.parse_macro_value(
                value_text
            )

        self.define(
            name,
            value,
            source_defined = True
        )

    @staticmethod
    def parse_macro_value(
        text
    ):
        text = str(text).strip()

        if not text:
            return True

        upper_text = text.upper()

        if upper_text == "TRUE":
            return True

        if upper_text == "FALSE":
            return False

        if re.fullmatch(r"[+-]?[0-9]+", text):
            return int(
                text,
                10
            )

        if re.fullmatch(r"\$[0-9A-Fa-f]+", text):
            return int(
                text[1:],
                16
            )

        if re.fullmatch(r"0[xX][0-9A-Fa-f]+", text):
            return int(
                text,
                16
            )

        if (
            len(text) >= 2
            and text[0] == text[-1]
            and text[0] in ("'", '"')
        ):
            quote = text[0]

            return text[1:-1].replace(
                quote + quote,
                quote
            )

        return text

    def evaluate_condition(
        self,
        expression,
        filename,
        line_number
    ):
        try:
            parser = ConditionalExpressionParser(
                expression,
                self.macros
            )

            return parser.parse()

        except ConditionalExpressionError as exc:
            raise PascalPreprocessorError(
                f"{filename}:{line_number}: "
                f"invalid {{$IF}} condition: {exc}"
            ) from exc

    @staticmethod
    def blank_line(
        line
    ):
        return "".join(
            char if char in ("\r", "\n") else " "
            for char in line
        )

    def process(
        self,
        source  : str,
        filename: str  | None = None,
        macros  : dict | None = None
    ) -> str:
        if source is None:
            return ""

        if filename:
            filename = os.path.normpath(
                os.path.abspath(filename)
            )
        else:
            filename = "<unknown>"

        macro_values = {
            str(name).upper(): value
            for name, value in (macros or {}).items()
        }

        compile_datetime = datetime.now()
        compile_date = compile_datetime.strftime("%Y-%m-%d")
        compile_time = compile_datetime.strftime("%H:%M:%S")

        result: list[str] = []

        lines = source.splitlines(
            keepends = True
        )

        output = []
        conditional_stack = []
        current_active = True

        for line_number, line in enumerate(
            lines,
            start=1
        ):
            match = self.CONTROL_DIRECTIVE_RE.match(
                line
            )

            if match is None:
                if current_active:
                    output.append(line)
                else:
                    output.append(
                        self.blank_line(line)
                    )

                continue

            command = (
                match.group(1)
                .strip()
                .upper()
            )

            argument = (
                match.group(2)
                .strip()
            )

            if command == "DEFINE":
                if current_active:
                    self.process_define_argument(
                        argument,
                        filename,
                        line_number
                    )

                output.append(
                    self.blank_line(line)
                )

                continue

            if command == "UNDEF":
                if current_active:
                    if not argument:
                        raise PascalPreprocessorError(
                            f"{filename}:{line_number}: "
                            "{$UNDEF} requires a symbol"
                        )

                    macro_name = argument.split()[0]
                    self.undef(macro_name)

                output.append(
                    self.blank_line(line)
                )

                continue

            if command in (
                "IFDEF",
                "IFNDEF",
                "IF"
            ):
                if not argument:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        f"{{${command}}} requires an expression"
                    )

                parent_active = current_active

                if not parent_active:
                    condition = False

                elif command == "IFDEF":
                    condition = self.is_defined(
                        argument
                    )

                elif command == "IFNDEF":
                    condition = not self.is_defined(
                        argument
                    )

                else:
                    condition = self.evaluate_condition(
                        argument,
                        filename,
                        line_number
                    )

                current_active = (
                    parent_active
                    and condition
                )

                conditional_stack.append({
                    "command": command,
                    "line": line_number,
                    "parent_active": parent_active,
                    "branch_taken": bool(
                        parent_active
                        and condition
                    ),
                    "else_seen": False,
                    "current_active": current_active
                })

                output.append(
                    self.blank_line(line)
                )

                continue

            if command in (
                "ELSEIF",
                "ELIF"
            ):
                if not conditional_stack:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        "{$ELSEIF} without {$IF}"
                    )

                state = conditional_stack[-1]

                if state["else_seen"]:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        "{$ELSEIF} after {$ELSE}"
                    )

                if not argument:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        "{$ELSEIF} requires an expression"
                    )

                if not state["parent_active"]:
                    condition = False

                elif state["branch_taken"]:
                    condition = False

                else:
                    condition = self.evaluate_condition(
                        argument,
                        filename,
                        line_number
                    )

                current_active = (
                    state["parent_active"]
                    and not state["branch_taken"]
                    and condition
                )

                if current_active:
                    state["branch_taken"] = True

                state["current_active"] = current_active

                output.append(
                    self.blank_line(line)
                )

                continue

            if command == "ELSE":
                if not conditional_stack:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        "{$ELSE} without {$IF}"
                    )

                state = conditional_stack[-1]

                if state["else_seen"]:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        "duplicate {$ELSE}"
                    )

                state["else_seen"] = True

                current_active = (
                    state["parent_active"]
                    and not state["branch_taken"]
                )

                state["branch_taken"] = True
                state["current_active"] = current_active

                output.append(
                    self.blank_line(line)
                )

                continue

            if command == "ENDIF":
                if not conditional_stack:
                    raise PascalPreprocessorError(
                        f"{filename}:{line_number}: "
                        "{$ENDIF} without {$IF}"
                    )

                state = conditional_stack.pop()

                current_active = state[
                    "parent_active"
                ]

                output.append(
                    self.blank_line(line)
                )

                continue

        if conditional_stack:
            state = conditional_stack[-1]

            raise PascalPreprocessorError(
                f"{filename}:{state['line']}: "
                f"missing {{$ENDIF}} for "
                f"{{${state['command']}}}"
            )

        intermediate_text = "".join(
            output
        )

        return self.compiler_directives.process(
            intermediate_text,
            filename = filename,
            macros   = self.macros
        )
