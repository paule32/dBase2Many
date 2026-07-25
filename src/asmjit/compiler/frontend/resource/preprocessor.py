from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import os
import re


class PreprocessorError(RuntimeError):
    pass


@dataclass
class PreprocessedSource:
    text: str
    filename: Path
    codepage: int
    dependencies: list[Path]
    macros: dict[str, str]


_TOKEN_RE = re.compile(
    r"\s+|"
    r"0[xX][0-9A-Fa-f]+[uUlL]*|"
    r"0[oO][0-7]+[uUlL]*|"
    r"[0-9]+[uUlL]*|"
    r"[A-Za-z_$][A-Za-z0-9_$]*|"
    r"&&|\|\||==|!=|<=|>=|<<|>>|"
    r"[()!~+\-*/%<>&^|]"
)


class _IfExpression:
    def __init__(self, text: str, macros: dict[str, str]):
        self.macros = macros
        self.tokens = [
            token
            for token in _TOKEN_RE.findall(text)
            if not token.isspace()
        ]
        self.index = 0

    def peek(self) -> str | None:
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]

    def take(self, expected: str | None = None) -> str:
        token = self.peek()
        if token is None:
            raise PreprocessorError("unexpected end of #if expression")
        if expected is not None and token != expected:
            raise PreprocessorError(
                f"expected {expected!r} in #if expression, got {token!r}"
            )
        self.index += 1
        return token

    def parse(self) -> int:
        value = self.logical_or()
        if self.peek() is not None:
            raise PreprocessorError(
                f"unexpected token in #if expression: {self.peek()!r}"
            )
        return int(value)

    def logical_or(self) -> int:
        value = self.logical_and()
        while self.peek() == "||":
            self.take()
            right = self.logical_and()
            value = int(bool(value) or bool(right))
        return value

    def logical_and(self) -> int:
        value = self.bit_or()
        while self.peek() == "&&":
            self.take()
            right = self.bit_or()
            value = int(bool(value) and bool(right))
        return value

    def bit_or(self) -> int:
        value = self.bit_xor()
        while self.peek() == "|":
            self.take()
            value |= self.bit_xor()
        return value

    def bit_xor(self) -> int:
        value = self.bit_and()
        while self.peek() == "^":
            self.take()
            value ^= self.bit_and()
        return value

    def bit_and(self) -> int:
        value = self.equality()
        while self.peek() == "&":
            self.take()
            value &= self.equality()
        return value

    def equality(self) -> int:
        value = self.relational()
        while self.peek() in ("==", "!="):
            op = self.take()
            right = self.relational()
            value = int(value == right if op == "==" else value != right)
        return value

    def relational(self) -> int:
        value = self.shift()
        while self.peek() in ("<", "<=", ">", ">="):
            op = self.take()
            right = self.shift()
            value = int({
                "<": value < right,
                "<=": value <= right,
                ">": value > right,
                ">=": value >= right,
            }[op])
        return value

    def shift(self) -> int:
        value = self.additive()
        while self.peek() in ("<<", ">>"):
            op = self.take()
            right = self.additive()
            value = value << right if op == "<<" else value >> right
        return value

    def additive(self) -> int:
        value = self.multiplicative()
        while self.peek() in ("+", "-"):
            op = self.take()
            right = self.multiplicative()
            value = value + right if op == "+" else value - right
        return value

    def multiplicative(self) -> int:
        value = self.unary()
        while self.peek() in ("*", "/", "%"):
            op = self.take()
            right = self.unary()
            if right == 0:
                raise PreprocessorError("division by zero in #if expression")
            if op == "*":
                value *= right
            elif op == "/":
                value = int(value / right)
            else:
                value %= right
        return value

    def unary(self) -> int:
        token = self.peek()
        if token in ("!", "~", "+", "-"):
            self.take()
            value = self.unary()
            if token == "!":
                return int(not value)
            if token == "~":
                return ~value
            if token == "-":
                return -value
            return value
        return self.primary()

    def primary(self) -> int:
        token = self.take()
        if token == "(":
            value = self.logical_or()
            self.take(")")
            return value

        if token.lower() == "defined":
            if self.peek() == "(":
                self.take("(")
                name = self.take()
                self.take(")")
            else:
                name = self.take()
            return int(name in self.macros)

        if re.fullmatch(r"0[xX][0-9A-Fa-f]+[uUlL]*", token):
            return int(re.sub(r"[uUlL]+$", "", token), 16)
        if re.fullmatch(r"0[oO][0-7]+[uUlL]*", token):
            return int(re.sub(r"[uUlL]+$", "", token)[2:], 8)
        if re.fullmatch(r"[0-9]+[uUlL]*", token):
            raw = re.sub(r"[uUlL]+$", "", token)
            if len(raw) > 1 and raw.startswith("0"):
                return int(raw, 8)
            return int(raw, 10)

        if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", token):
            replacement = self.macros.get(token, "0")
            if replacement == token:
                return 0
            try:
                return _IfExpression(replacement, self.macros).parse()
            except PreprocessorError:
                return 0

        raise PreprocessorError(
            f"invalid token in #if expression: {token!r}"
        )


class RcPreprocessor:
    def __init__(
        self,
        *,
        include_paths: Iterable[str | os.PathLike[str]] = (),
        defines: Iterable[str] = (),
        codepage: int = 65001,
        max_include_depth: int = 64,
    ) -> None:
        self.include_paths = [
            Path(os.path.expandvars(os.path.expanduser(os.fspath(path)))).resolve()
            for path in include_paths
        ]
        self.macros: dict[str, str] = {
            "RC_INVOKED": "1",
            "_WIN32": "1",
        }
        self.codepage = int(codepage)
        self.max_include_depth = int(max_include_depth)
        self.dependencies: list[Path] = []
        self._include_stack: list[Path] = []
        self._in_block_comment = False

        for define in defines:
            self.define_from_command_line(define)

    def define_from_command_line(self, define: str) -> None:
        define = str(define).strip()
        if not define:
            return
        if "=" in define:
            name, value = define.split("=", 1)
        else:
            name, value = define, "1"
        name = name.strip()
        if not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name):
            raise PreprocessorError(f"invalid macro name: {name!r}")
        self.macros[name] = value.strip() or "1"

    def process(self, filename: str | os.PathLike[str]) -> PreprocessedSource:
        source = Path(filename).resolve()
        text = self._process_file(source, 0)
        return PreprocessedSource(
            text=text,
            filename=source,
            codepage=self.codepage,
            dependencies=list(self.dependencies),
            macros=dict(self.macros),
        )

    def _read_text(self, path: Path) -> str:
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            return data[3:].decode("utf-8")
        if data.startswith(b"\xff\xfe"):
            return data[2:].decode("utf-16le")
        if data.startswith(b"\xfe\xff"):
            return data[2:].decode("utf-16be")

        encoding = "utf-8" if self.codepage == 65001 else f"cp{self.codepage}"
        try:
            return data.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            return data.decode("latin-1")

    def _logical_lines(self, text: str) -> list[str]:
        physical = text.splitlines(keepends=True)
        logical: list[str] = []
        current = ""
        for line in physical:
            stripped = line.rstrip("\r\n")
            newline = line[len(stripped):]
            if stripped.endswith("\\"):
                current += stripped[:-1]
                continue
            logical.append(current + stripped + (newline or "\n"))
            current = ""
        if current:
            logical.append(current + "\n")
        return logical

    def _process_file(self, path: Path, depth: int) -> str:
        if depth >= self.max_include_depth:
            raise PreprocessorError("maximum include depth exceeded")
        if path in self._include_stack:
            chain = " -> ".join(str(item) for item in self._include_stack + [path])
            raise PreprocessorError(f"recursive #include: {chain}")
        if not path.is_file():
            raise FileNotFoundError(f"resource source not found: {path}")

        if path not in self.dependencies:
            self.dependencies.append(path)
        self._include_stack.append(path)

        try:
            lines = self._logical_lines(self._read_text(path))
            output: list[str] = []
            # Each frame: parent-active, any-branch-taken, this-branch-active.
            stack: list[list[bool]] = []
            active = True

            for line_number, line in enumerate(lines, 1):
                match = re.match(r"^[ \t]*#\s*([A-Za-z_][A-Za-z0-9_]*)\b(.*)$", line)
                if not match:
                    output.append(self._expand_line(line) if active else "\n")
                    continue

                directive = match.group(1).lower()
                argument = match.group(2).strip()

                if directive in ("if", "ifdef", "ifndef"):
                    parent = active
                    if directive == "ifdef":
                        condition = argument.split()[0] in self.macros if argument else False
                    elif directive == "ifndef":
                        condition = argument.split()[0] not in self.macros if argument else False
                    else:
                        condition = bool(_IfExpression(argument, self.macros).parse()) if parent else False
                    branch = parent and condition
                    stack.append([parent, branch, branch])
                    active = branch
                    output.append("\n")
                    continue

                if directive == "elif":
                    if not stack:
                        raise PreprocessorError(f"{path}:{line_number}: #elif without #if")
                    parent, taken, _ = stack[-1]
                    branch = parent and not taken and bool(_IfExpression(argument, self.macros).parse())
                    stack[-1][1] = taken or branch
                    stack[-1][2] = branch
                    active = branch
                    output.append("\n")
                    continue

                if directive == "else":
                    if not stack:
                        raise PreprocessorError(f"{path}:{line_number}: #else without #if")
                    parent, taken, _ = stack[-1]
                    branch = parent and not taken
                    stack[-1][1] = True
                    stack[-1][2] = branch
                    active = branch
                    output.append("\n")
                    continue

                if directive == "endif":
                    if not stack:
                        raise PreprocessorError(f"{path}:{line_number}: #endif without #if")
                    stack.pop()
                    active = stack[-1][2] if stack else True
                    output.append("\n")
                    continue

                if not active:
                    output.append("\n")
                    continue

                if directive == "include":
                    include_path = self._parse_include(argument, path.parent)
                    output.append(self._process_file(include_path, depth + 1))
                    continue

                if directive == "define":
                    parts = argument.split(None, 1)
                    if not parts:
                        raise PreprocessorError(f"{path}:{line_number}: empty #define")
                    name = parts[0]
                    if "(" in name:
                        raise PreprocessorError(
                            f"{path}:{line_number}: function-like macros are not supported: {name}"
                        )
                    if not re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", name):
                        raise PreprocessorError(f"{path}:{line_number}: invalid macro name {name!r}")
                    self.macros[name] = parts[1].strip() if len(parts) > 1 else "1"
                    output.append("\n")
                    continue

                if directive == "undef":
                    self.macros.pop(argument.split()[0], None) if argument else None
                    output.append("\n")
                    continue

                if directive == "pragma":
                    codepage = re.match(r"code_page\s*\(\s*([0-9]+)\s*\)", argument, re.I)
                    if codepage:
                        self.codepage = int(codepage.group(1))
                    output.append("\n")
                    continue

                if directive == "error":
                    raise PreprocessorError(f"{path}:{line_number}: {argument}")

                if directive in ("line",):
                    output.append("\n")
                    continue

                raise PreprocessorError(
                    f"{path}:{line_number}: unsupported preprocessor directive #{directive}"
                )

            if stack:
                raise PreprocessorError(f"{path}: unterminated conditional directive")
            return "".join(output)
        finally:
            self._include_stack.pop()

    def _parse_include(self, argument: str, current_directory: Path) -> Path:
        match = re.match(r'([<"])(.*?)[>"]$', argument.strip())
        if not match:
            raise PreprocessorError(f"invalid #include syntax: {argument!r}")
        opener, name = match.groups()
        candidates: list[Path] = []
        if opener == '"':
            candidates.append(current_directory / name)
        candidates.extend(path / name for path in self.include_paths)
        for candidate in candidates:
            candidate = candidate.resolve()
            if candidate.is_file():
                return candidate
        raise FileNotFoundError(
            f"include file not found: {name}\nsearched:\n"
            + "\n".join(f"  {item}" for item in candidates)
        )

    def _expand_line(self, line: str) -> str:
        result: list[str] = []
        i = 0
        in_string = False
        quote = ""

        while i < len(line):
            if self._in_block_comment:
                end = line.find("*/", i)
                if end < 0:
                    result.append(line[i:])
                    return "".join(result)
                result.append(line[i:end + 2])
                i = end + 2
                self._in_block_comment = False
                continue

            if not in_string and line.startswith("//", i):
                result.append(line[i:])
                break
            if not in_string and line.startswith("/*", i):
                self._in_block_comment = True
                result.append("/*")
                i += 2
                continue

            ch = line[i]
            if in_string:
                result.append(ch)
                i += 1
                if ch == "\\" and i < len(line):
                    result.append(line[i])
                    i += 1
                elif ch == quote:
                    in_string = False
                continue

            if ch in ('"', "'"):
                in_string = True
                quote = ch
                result.append(ch)
                i += 1
                continue

            identifier = re.match(r"[A-Za-z_$][A-Za-z0-9_$]*", line[i:])
            if identifier:
                name = identifier.group(0)
                result.append(self._expand_macro(name, set()))
                i += len(name)
                continue

            result.append(ch)
            i += 1

        return "".join(result)

    def _expand_macro(self, name: str, seen: set[str]) -> str:
        if name not in self.macros:
            return name
        if name in seen:
            return name
        replacement = self.macros[name]
        seen = set(seen)
        seen.add(name)

        def replace(match: re.Match[str]) -> str:
            token = match.group(0)
            return self._expand_macro(token, seen)

        return re.sub(r"[A-Za-z_$][A-Za-z0-9_$]*", replace, replacement)
