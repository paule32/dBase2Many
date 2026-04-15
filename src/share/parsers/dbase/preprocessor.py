# ---------------------------------------------------------------------------
# File:   preprocessor.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

import share.common
from   share.common import *

class Preprocessor:
    include_re = re.compile(r'^\s*#include\s+"([^"]+)"\s*$')
    define_re  = re.compile(r'^\s*#define\s+([A-Za-z_]\w*)(.*)\s*$')
    ifdef_re   = re.compile(r'^\s*#ifdef\s+([A-Za-z_]\w*)\s*$')
    ifndef_re  = re.compile(r'^\s*#ifndef\s+([A-Za-z_]\w*)\s*$')
    else_re    = re.compile(r'^\s*#else\s*$')
    endif_re   = re.compile(r'^\s*#endif\s*$')

    def __init__(self, *, include_paths: list[Path] | None = None):
        self.include_paths = include_paths or []
        self.macros: dict[str, share.common.Macro] = {}
        self.defined: set[str] = set()
        self._include_stack: list[Path] = []

    def _rewrite_use_line(self, raw_line: str) -> str:
        # keep original newline (if any)
        nl = ""
        if raw_line.endswith("\r\n"):
            raw, nl = raw_line[:-2], "\r\n"
        elif raw_line.endswith("\n"):
            raw, nl = raw_line[:-1], "\n"
        else:
            raw = raw_line

        stripped = raw.lstrip()
        if not stripped or stripped.startswith("#"):
            return raw_line

        m = re.match(r"^(\s*)USE\b(.*)$", raw, flags=re.IGNORECASE)
        if not m:
            return raw_line

        indent = m.group(1)
        rest = m.group(2).strip()

        if rest.startswith("("):   # already USE(...)
            return raw_line

        code_part, comment_part = self._split_comment_outside(raw)
        work = code_part.strip()
        rest = re.sub(r"^USE\b", "", work, count=1, flags=re.IGNORECASE).strip()

        exclusive = False
        m_ex = re.match(r"^(.*?)(\s+EXCLUSIVE\s*)$", rest, flags=re.IGNORECASE)
        if m_ex:
            rest = m_ex.group(1).rstrip()
            exclusive = True

        index_part = ""
        idx_pos = self._find_keyword_outside(rest, "INDEX")
        if idx_pos >= 0:
            index_part = rest[idx_pos + len("INDEX"):].strip()
            rest = rest[:idx_pos].strip()

        comment_suffix = "" if not comment_part else " " + comment_part.lstrip()
        ex_flag = "1" if exclusive else "0"

        if not rest:
            return f"{indent}__DBASE_USE__(\"\", \"\" , {ex_flag}){comment_suffix}{nl}"

        return f"{indent}__DBASE_USE__({self._quote_builtin_arg(rest)}, {self._quote_builtin_arg(index_part)}, {ex_flag}){comment_suffix}{nl}"
    
    def _split_args(self, s: str) -> list[str]:
        # s ist Inhalt zwischen den äußeren (...) eines Calls
        args = []
        cur = []
        depth = 0
        i = 0
        while i < len(s):
            ch = s[i]
            if ch == "(":
                depth += 1
                cur.append(ch)
            elif ch == ")":
                depth -= 1
                cur.append(ch)
            elif ch == "," and depth == 0:
                args.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
            i += 1
        if cur or s.strip() == "":
            args.append("".join(cur).strip())
        return args

    def _stringize(self, arg_text: str) -> str:
        # Whitespace normalisieren wie C-ish
        norm = " ".join(arg_text.split())
        norm = norm.replace("\\", "\\\\").replace('"', '\\"')
        return f"\"{norm}\""

    def _expand_function_macro(self, macro: share.common.Macro, call_args: list[str]) -> str:
        if macro.params is None:
            raise share.common.PreprocessorError("internal: not a function macro")

        if len(call_args) != len(macro.params):
            raise share.common.PreprocessorError(
                f"macro {macro.name} expects {len(macro.params)} args, got {len(call_args)}"
            )

        argmap = dict(zip(macro.params, call_args))

        # body als Arbeitsstring
        body = macro.body

        # 1) stringize: #param  (nur wenn param direkt folgt)
        #    Beispiel: #x
        for p in macro.params:
            body = re.sub(rf'#\s*{re.escape(p)}\b',
                          lambda m, p=p: self._stringize(argmap[p]),
                          body)

        # 2) token paste: a ## b  (pragmatisch: Strings zusammenkleben)
        #    Wir machen das iterativ, solange es '##' gibt.
        #    Dabei erlauben wir links/rechts: param oder direktes Wort/Token
        while "##" in body:
            m = re.search(r'(\S+)\s*##\s*(\S+)', body)
            if not m:
                break
            left = m.group(1)
            right = m.group(2)

            # param ersetzen, falls es param ist
            left_val = argmap.get(left, left)
            right_val = argmap.get(right, right)

            # Wenn left_val ein Stringliteral ist ("..."), quotes entfernen und concat
            if left_val.startswith('"') and left_val.endswith('"'):
                left_inner = left_val[1:-1]
                # right_val: wenn auch string, ohne quotes
                if right_val.startswith('"') and right_val.endswith('"'):
                    right_part = right_val[1:-1]
                else:
                    right_part = right_val
                glued = f"\"{left_inner}{right_part}\""
            else:
                glued = f"{left_val}{right_val}"

            body = body[:m.start()] + glued + body[m.end():]

        # 3) normale param substitution (für verbleibende params im body)
        for p in macro.params:
            body = re.sub(rf'\b{re.escape(p)}\b', argmap[p], body)

        return body

    def _expand_macros_in_line(self, line: str) -> str:
        # Sehr einfache, iterative Expansion (mit Limit gegen Endlosschleifen)
        out = line
        for _ in range(50):
            changed = False

            # 1) function-like macros: NAME(...)
            #    Suche NAME( ... ) und expandiere
            for name, macro in list(self.macros.items()):
                if macro.params is None:
                    continue

                # finde "name(" in der Zeile
                idx = out.find(name + "(")
                while idx != -1:
                    # parse bis passendes ')'
                    j = idx + len(name) + 1
                    depth = 1
                    while j < len(out) and depth > 0:
                        if out[j] == "(":
                            depth += 1
                        elif out[j] == ")":
                            depth -= 1
                        j += 1
                    if depth != 0:
                        # unbalanciert -> abbrechen
                        break

                    inside = out[idx + len(name) + 1 : j - 1]
                    args = self._split_args(inside)
                    repl = self._expand_function_macro(macro, args)

                    out = out[:idx] + repl + out[j:]
                    changed = True

                    idx = out.find(name + "(", idx + len(repl))
                # next macro

            # 2) object-like macros: \bNAME\b
            for name, macro in list(self.macros.items()):
                if macro.params is not None:
                    continue
                # ganzes Wort ersetzen
                new_out = re.sub(rf'\b{re.escape(name)}\b', macro.body, out)
                if new_out != out:
                    out = new_out
                    changed = True

            if not changed:
                break

        return out

    def process(self, filename: str | Path) -> str:
        #data = Path(filename).read_text(encoding="utf-8")
        #data = re.sub(r'(?i)\bNEW(?=[A-Za-z_])', 'NEW ', data)
        #data = re.sub(r'(?i)\bCALL(?=[A-Za-z_])', 'CALL ', data)
        #with open(filename,"w",encoding="utf-8") as f:
        #    f.write(data)
        #    f.close()
            
        entry = Path(filename).resolve()
        data = self._process_file(entry)
        data = self._rewrite_text_blocks(data)
        data = self._rewrite_note_comments(data)
        data = self._rewrite_dot_logical_keywords(data)
        data = self._rewrite_do_case_blocks(data)
        data = self._rewrite_input_statements(data)
        data = self._rewrite_erase_statements(data)
        data = self._rewrite_set_output_statements(data)
        data = self._rewrite_memvar_statements(data)
        data = self._rewrite_dbf_statements(data)
        return data

    def _rewrite_do_case_blocks(self, text: str) -> str:
        def split_header_and_inline(rest: str):
            rest = (rest or "").strip()
            if not rest:
                return "", ""
            in_quote = None
            i = 0
            n = len(rest)
            while i < n:
                ch = rest[i]
                if in_quote is not None:
                    if ch == in_quote:
                        if i + 1 < n and rest[i + 1] == in_quote:
                            i += 2
                            continue
                        in_quote = None
                    i += 1
                    continue
                if ch in ("'", '"'):
                    in_quote = ch
                    i += 1
                    continue
                if ch.isspace():
                    tail = rest[i:].lstrip()
                    head = rest[:i].rstrip()
                    upper_tail = tail.upper()
                    stmt_starters = (
                        "WRITE", "?", "@", "IF", "DO", "FOR", "SCAN", "STORE", "REPLACE",
                        "CASE", "ENDCASE", "OTHERWISE",
                        "APPEND", "INSERT", "DELETE", "GOTO", "LOOP", "EXIT", "RETURN",
                        "THIS.", "SUPER.", "SET", "USE", "SELECT", "WAIT", "MESSAGEBOX",
                        "BROWSE", "COUNT", "SUM", "AVERAGE", "LIST", "DISPLAY", "ASSERT",
                        "SAVE", "RESTORE", "RELEASE"
                    )
                    if upper_tail.startswith(stmt_starters) or re.match(r'^[A-Za-z_]\w*\s*=.*$', tail):
                        return head, tail
                i += 1
            return rest, ""

        def normalize_body(body_lines, branch_indent: str):
            normalized = []
            for line in body_lines:
                stripped = line.strip()
                if not stripped:
                    normalized.append(line)
                    continue
                raw_no_nl = line.rstrip('')
                content = raw_no_nl.lstrip()
                line_nl = "\n"
                if line.endswith("\r\n"):
                    line_nl = "\r\n"
                elif line.endswith("\n"):
                    line_nl = "\n"
                normalized.append(branch_indent + content + line_nl)
            return normalized

        def render_branches(branches, indent=""):
            def render_at(i: int, cur_indent: str):
                kind, cond, body = branches[i]
                out = []
                if kind == "CASE":
                    out.append(f"{cur_indent}IF {cond}")
                    out.extend(normalize_body(body, cur_indent + "    "))
                    if i + 1 < len(branches):
                        out.append(f"{cur_indent}ELSE")
                        out.extend(render_at(i + 1, cur_indent + "    "))
                    out.append(f"{cur_indent}ENDIF")
                else:
                    out.extend(normalize_body(body, cur_indent))
                return out
            return render_at(0, indent) if branches else []

        def nesting_delta(s: str) -> int:
            delta = 0
            if re.match(r'^IF\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^ENDIF\b', s, flags=re.IGNORECASE):
                delta -= 1

            if re.match(r'^DO\s+CASE\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^ENDCASE\b', s, flags=re.IGNORECASE):
                delta -= 1

            if re.match(r'^DO\s+WHILE\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^ENDDO\b', s, flags=re.IGNORECASE):
                delta -= 1

            if re.match(r'^FOR\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^(ENDFOR|NEXT)\b', s, flags=re.IGNORECASE):
                delta -= 1

            if re.match(r'^SCAN\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^ENDSCAN\b', s, flags=re.IGNORECASE):
                delta -= 1

            if re.match(r'^WITH\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^ENDWITH\b', s, flags=re.IGNORECASE):
                delta -= 1

            if re.match(r'^TRY\b', s, flags=re.IGNORECASE):
                delta += 1
            elif re.match(r'^ENDTRY\b', s, flags=re.IGNORECASE):
                delta -= 1

            return delta

        def rewrite_lines(lines):
            out = []
            i = 0
            n = len(lines)
            while i < n:
                raw = lines[i]
                stripped = raw.strip()
                if re.match(r'^DO\s+CASE\b', stripped, flags=re.IGNORECASE):
                    base_indent = raw[:len(raw) - len(raw.lstrip())]
                    depth = 1
                    j = i + 1
                    block_lines = []
                    while j < n:
                        s = lines[j].strip()
                        if re.match(r'^DO\s+CASE\b', s, flags=re.IGNORECASE):
                            depth += 1
                        elif re.match(r'^ENDCASE\b', s, flags=re.IGNORECASE):
                            depth -= 1
                            if depth == 0:
                                break
                        block_lines.append(lines[j])
                        j += 1
                    if depth != 0:
                        out.append(raw)
                        i += 1
                        continue

                    branches = []
                    cur_kind = None
                    cur_cond = None
                    cur_body = []
                    nested_depth = 0

                    def flush_branch():
                        nonlocal cur_kind, cur_cond, cur_body
                        if cur_kind is not None:
                            rewritten_body = rewrite_lines(cur_body)
                            branches.append((cur_kind, cur_cond, rewritten_body))
                        cur_kind = None
                        cur_cond = None
                        cur_body = []

                    for inner in block_lines:
                        s = inner.strip()

                        if nested_depth == 0:
                            m_case = re.match(r'^CASE\b(.*)$', s, flags=re.IGNORECASE)
                            m_other = re.match(r'^OTHERWISE\b(.*)$', s, flags=re.IGNORECASE)
                            if m_case:
                                flush_branch()
                                cond, inline_stmt = split_header_and_inline(m_case.group(1))
                                cur_kind = "CASE"
                                cur_cond = cond.strip()
                                if inline_stmt:
                                    cur_body.append(base_indent + "    " + inline_stmt.rstrip() + "")
                                continue
                            if m_other:
                                flush_branch()
                                inline_stmt = (m_other.group(1) or "").strip()
                                cur_kind = "OTHERWISE"
                                cur_cond = None
                                if inline_stmt:
                                    cur_body.append(base_indent + "    " + inline_stmt.rstrip() + "")
                                continue

                        cur_body.append(inner)
                        nested_depth += nesting_delta(s)
                        if nested_depth < 0:
                            nested_depth = 0

                    flush_branch()

                    if branches:
                        out.extend(render_branches(branches, base_indent))
                    else:
                        out.append(raw)
                        out.extend(block_lines)
                        out.append(base_indent + "ENDCASE")
                    i = j + 1
                    continue

                out.append(raw)
                i += 1
            return out

        return "".join(rewrite_lines(text.splitlines(keepends=True)))

    def _find_note_comment_start(self, s: str) -> int:
        if s is None:
            return -1

        up = s.upper()
        kw = "NOTE"
        i = 0
        n = len(s)
        in_quote = None
        in_bracket = False

        while i < n:
            ch = s[i]

            if in_quote is not None:
                if ch == in_quote:
                    if i + 1 < n and s[i + 1] == in_quote:
                        i += 2
                        continue
                    in_quote = None
                i += 1
                continue

            if in_bracket:
                if ch == ']':
                    if i + 1 < n and s[i + 1] == ']':
                        i += 2
                        continue
                    in_bracket = False
                i += 1
                continue

            if ch in ("'", '"'):
                in_quote = ch
                i += 1
                continue

            if ch == '[':
                in_bracket = True
                i += 1
                continue

            if up.startswith(kw, i):
                prev_ok = i == 0 or not (up[i - 1].isalnum() or up[i - 1] == '_')
                next_pos = i + len(kw)
                next_ok = next_pos >= n or s[next_pos].isspace()
                if prev_ok and next_ok:
                    return i

            i += 1

        return -1

    def _rewrite_note_comments(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ""
            line = raw_line
            if line.endswith("\r\n"):
                line = line[:-2]
                nl = "\r\n"
            elif line.endswith("\n"):
                line = line[:-1]
                nl = "\n"

            pos = self._find_note_comment_start(line)
            if pos < 0:
                out.append(raw_line)
                continue

            out.append(line[:pos] + "//" + line[pos + 4:] + nl)

        return ''.join(out)

    def _split_comment_outside(self, s: str) -> tuple[str, str]:
        if s is None:
            return "", ""

        out = []
        i = 0
        n = len(s)
        in_quote = None
        in_bracket = False

        while i < n:
            ch = s[i]

            if in_quote is not None:
                out.append(ch)
                if ch == in_quote:
                    if i + 1 < n and s[i + 1] == in_quote:
                        out.append(s[i + 1])
                        i += 2
                        continue
                    in_quote = None
                i += 1
                continue

            if in_bracket:
                out.append(ch)
                if ch == ']':
                    if i + 1 < n and s[i + 1] == ']':
                        out.append(s[i + 1])
                        i += 2
                        continue
                    in_bracket = False
                i += 1
                continue

            if ch in ("'", '"'):
                in_quote = ch
                out.append(ch)
                i += 1
                continue

            if ch == '[':
                in_bracket = True
                out.append(ch)
                i += 1
                continue

            two = s[i:i+2]
            if two in ("&&", "**", "//", "/*"):
                return "".join(out), s[i:]

            if self._find_note_comment_start(s[i:]) == 0:
                return "".join(out), s[i:]

            out.append(ch)
            i += 1

        return "".join(out), ""

    def _find_keyword_outside(self, s: str, keyword: str) -> int:
        up = s.upper()
        kw = keyword.upper()
        i = 0
        n = len(s)
        in_quote = None
        in_bracket = False
        paren_depth = 0

        while i < n:
            ch = s[i]

            if in_quote is not None:
                if ch == in_quote:
                    if i + 1 < n and s[i + 1] == in_quote:
                        i += 2
                        continue
                    in_quote = None
                i += 1
                continue

            if in_bracket:
                if ch == ']':
                    if i + 1 < n and s[i + 1] == ']':
                        i += 2
                        continue
                    in_bracket = False
                i += 1
                continue

            if ch in ("'", '"'):
                in_quote = ch
                i += 1
                continue

            if ch == '[':
                in_bracket = True
                i += 1
                continue

            if ch == '(':
                paren_depth += 1
                i += 1
                continue

            if ch == ')':
                paren_depth = max(0, paren_depth - 1)
                i += 1
                continue

            if paren_depth == 0 and up.startswith(kw, i):
                prev_ok = i == 0 or not (up[i - 1].isalnum() or up[i - 1] == '_')
                next_pos = i + len(kw)
                next_ok = next_pos >= n or not (up[next_pos].isalnum() or up[next_pos] == '_')
                if prev_ok and next_ok:
                    return i

            i += 1

        return -1

    def _rewrite_input_statements(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ""
            line = raw_line
            if line.endswith("\r\n"):
                line = line[:-2]
                nl = "\r\n"
            elif line.endswith("\n"):
                line = line[:-1]
                nl = "\n"

            indent = line[:len(line) - len(line.lstrip())]
            stripped = line.strip()
            if not stripped:
                out.append(raw_line)
                continue

            if not re.match(r'^INPUT\b', stripped, flags=re.IGNORECASE):
                out.append(raw_line)
                continue

            code_part, comment_part = self._split_comment_outside(line)
            work = code_part.strip()

            if not re.match(r'^INPUT\b', work, flags=re.IGNORECASE):
                out.append(raw_line)
                continue

            rest = re.sub(r'^INPUT\b', '', work, count=1, flags=re.IGNORECASE).strip()
            if rest.startswith('('):
                out.append(raw_line)
                continue

            to_pos = self._find_keyword_outside(rest, 'TO')
            if to_pos < 0:
                out.append(raw_line)
                continue

            prompt_expr = rest[:to_pos].strip()
            target_name = rest[to_pos + 2:].strip()

            if not target_name:
                out.append(raw_line)
                continue

            target_escaped = target_name.replace('\\', '\\\\').replace(chr(34), '\\"')

            if prompt_expr:
                rewritten = f'{indent}INPUT({prompt_expr}, "{target_escaped}")'
            else:
                rewritten = f'{indent}INPUT("", "{target_escaped}")'

            comment_suffix = "" if not comment_part else " " + comment_part.lstrip()
            out.append(rewritten + comment_suffix + nl)

        return ''.join(out)

    def _rewrite_erase_statements(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ""
            line = raw_line
            if line.endswith("\r\n"):
                line = line[:-2]
                nl = "\r\n"
            elif line.endswith("\n"):
                line = line[:-1]
                nl = "\n"

            indent = line[:len(line) - len(line.lstrip())]
            stripped = line.strip()
            if not stripped:
                out.append(raw_line)
                continue

            code_part, comment_part = self._split_comment_outside(line)
            work = code_part.strip()

            if not re.match(r'^ERASE\b', work, flags=re.IGNORECASE):
                out.append(raw_line)
                continue

            rest = re.sub(r'^ERASE\b', '', work, count=1, flags=re.IGNORECASE).strip()
            if rest:
                out.append(raw_line)
                continue

            comment_suffix = "" if not comment_part else " " + comment_part.lstrip()
            out.append(f'{indent}__DBASE_ERASE__(){comment_suffix}{nl}')

        return ''.join(out)

    def _rewrite_set_output_statements(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ""
            line = raw_line
            if line.endswith("\r\n"):
                line = line[:-2]
                nl = "\r\n"
            elif line.endswith("\n"):
                line = line[:-1]
                nl = "\n"

            stripped = line.strip()
            if not stripped:
                out.append(raw_line)
                continue

            indent = line[:len(line) - len(line.lstrip())]
            code_part, comment_part = self._split_comment_outside(line)
            work = code_part.strip()
            comment_suffix = "" if not comment_part else " " + comment_part.lstrip()

            m = re.match(r'^SET\s+FORMAT\s+(?:TO\s+)?(SCREEN|PRINT)\s*$', work, flags=re.IGNORECASE)
            if m:
                mode = m.group(1).upper()
                out.append(f'{indent}__DBASE_SET_FORMAT__("{mode}"){comment_suffix}{nl}')
                continue

            m = re.match(r'^SET\s+PRINT\s+(ON|OFF)\s*$', work, flags=re.IGNORECASE)
            if m:
                enabled = '1' if m.group(1).upper() == 'ON' else '0'
                out.append(f'{indent}__DBASE_SET_PRINT__({enabled}){comment_suffix}{nl}')
                continue

            m = re.match(r'^SET\s+ESCAPE\s+(ON|OFF)\s*$', work, flags=re.IGNORECASE)
            if m:
                enabled = '1' if m.group(1).upper() == 'ON' else '0'
                out.append(f'{indent}__DBASE_SET_ESCAPE__({enabled}){comment_suffix}{nl}')
                continue

            m = re.match(r'^SET\s+CONFIRM\s+(ON|OFF)\s*$', work, flags=re.IGNORECASE)
            if m:
                enabled = '1' if m.group(1).upper() == 'ON' else '0'
                out.append(f'{indent}__DBASE_SET_CONFIRM__({enabled}){comment_suffix}{nl}')
                continue

            m = re.match(r'^SET\s+DELETE\s+(ON|OFF)\s*$', work, flags=re.IGNORECASE)
            if m:
                enabled = '1' if m.group(1).upper() == 'ON' else '0'
                out.append(f'{indent}__DBASE_SET_DELETE__({enabled}){comment_suffix}{nl}')
                continue

            m = re.match(r'^SET\s+MARGIN\s+TO(?:\s+(.*?))?\s*$', work, flags=re.IGNORECASE)
            if m:
                tail = (m.group(1) or '').strip()
                if not tail:
                    out.append(f'{indent}__DBASE_SET_MARGIN__(){comment_suffix}{nl}')
                    continue

                args = [a.strip() for a in self._split_args(tail) if a.strip()]
                rewritten_args = []
                for arg in args:
                    if re.fullmatch(r'[+-]?\d+(?:\.\d+)?\s*(?:px|cm|pt)?', arg, flags=re.IGNORECASE):
                        q = arg.replace('\\', '\\\\').replace('\"', '\\\"')
                        rewritten_args.append(f'"{q}"')
                    else:
                        rewritten_args.append(arg)
                out.append(f"{indent}__DBASE_SET_MARGIN__(" + ", ".join(rewritten_args) + f"){comment_suffix}{nl}")
                continue

            m = re.match(r'^SET\s+COLOR\s+TO(?:\s+(.*?))?\s*$', work, flags=re.IGNORECASE)
            if m:
                tail = (m.group(1) or '').strip()
                if not tail:
                    out.append(f'{indent}__DBASE_SET_COLOR__(){comment_suffix}{nl}')
                    continue
                out.append(f"{indent}__DBASE_SET_COLOR__({tail}){comment_suffix}{nl}")
                continue

            out.append(raw_line)

        return ''.join(out)

    def _tokenize_space_separated(self, s: str) -> list[str]:
        if s is None:
            return []

        tokens = []
        cur = []
        i = 0
        n = len(s)
        in_quote = None
        in_bracket = False

        while i < n:
            ch = s[i]

            if in_quote is not None:
                cur.append(ch)
                if ch == in_quote:
                    if i + 1 < n and s[i + 1] == in_quote:
                        cur.append(s[i + 1])
                        i += 2
                        continue
                    in_quote = None
                i += 1
                continue

            if in_bracket:
                cur.append(ch)
                if ch == ']':
                    if i + 1 < n and s[i + 1] == ']':
                        cur.append(s[i + 1])
                        i += 2
                        continue
                    in_bracket = False
                i += 1
                continue

            if ch in ('"', "'"):
                in_quote = ch
                cur.append(ch)
                i += 1
                continue

            if ch == '[':
                in_bracket = True
                cur.append(ch)
                i += 1
                continue

            if ch.isspace():
                if cur:
                    tokens.append(''.join(cur))
                    cur = []
                i += 1
                while i < n and s[i].isspace():
                    i += 1
                continue

            cur.append(ch)
            i += 1

        if cur:
            tokens.append(''.join(cur))
        return tokens

    def _quote_builtin_arg(self, s: str) -> str:
        s = '' if s is None else str(s)
        s = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{s}"'

    def _parse_mem_destination(self, s: str) -> tuple[str, str]:
        tokens = self._tokenize_space_separated(s)
        if not tokens:
            return '', ''
        if len(tokens) >= 2 and re.fullmatch(r'[A-Za-z]:?', tokens[0]):
            drive = tokens[0].rstrip(':')
            filename = ' '.join(tokens[1:]).strip()
            return drive, filename
        return '', ' '.join(tokens).strip()

    def _rewrite_memvar_statements(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ''
            line = raw_line
            if line.endswith('\r\n'):
                line = line[:-2]
                nl = '\r\n'
            elif line.endswith('\n'):
                line = line[:-1]
                nl = '\n'

            stripped = line.strip()
            if not stripped:
                out.append(raw_line)
                continue

            indent = line[:len(line) - len(line.lstrip())]
            code_part, comment_part = self._split_comment_outside(line)
            work = code_part.strip()
            comment_suffix = '' if not comment_part else ' ' + comment_part.lstrip()

            if re.match(r'^STORE', work, flags=re.IGNORECASE):
                rest = re.sub(r'^STORE', '', work, count=1, flags=re.IGNORECASE).strip()
                to_pos = self._find_keyword_outside(rest, 'TO')
                if to_pos >= 0:
                    expr_text = rest[:to_pos].strip()
                    target_name = rest[to_pos + 2:].strip()
                    if expr_text and target_name:
                        out.append(f"{indent}__DBASE_STORE__({expr_text}, {self._quote_builtin_arg(target_name)}){comment_suffix}{nl}")
                        continue

            if re.match(r'^SAVE', work, flags=re.IGNORECASE):
                rest = re.sub(r'^SAVE', '', work, count=1, flags=re.IGNORECASE).strip()
                mode = 'ALL'
                mask = ''
                dest_part = ''

                if re.match(r'^TO', rest, flags=re.IGNORECASE):
                    dest_part = re.sub(r'^TO', '', rest, count=1, flags=re.IGNORECASE).strip()
                else:
                    to_pos = self._find_keyword_outside(rest, 'TO')
                    if to_pos >= 0:
                        sel_part = rest[:to_pos].strip()
                        dest_part = rest[to_pos + 2:].strip()
                        m_sel = re.match(r'^ALL(?:\s+(LIKE|EXCEPT)\s+(.*))?$', sel_part, flags=re.IGNORECASE)
                        if m_sel:
                            if m_sel.group(1):
                                mode = m_sel.group(1).upper()
                                mask = (m_sel.group(2) or '').strip()
                            else:
                                mode = 'ALL'
                        else:
                            dest_part = ''

                drive, filename = self._parse_mem_destination(dest_part)
                if filename or drive:
                    out.append(f"{indent}__DBASE_SAVE__({self._quote_builtin_arg(filename)}, {self._quote_builtin_arg(mode)}, {self._quote_builtin_arg(mask)}, {self._quote_builtin_arg(drive)}){comment_suffix}{nl}")
                    continue

            if re.match(r'^RESTORE', work, flags=re.IGNORECASE):
                rest = re.sub(r'^RESTORE', '', work, count=1, flags=re.IGNORECASE).strip()
                m_from = re.match(r'^FROM(.*)$', rest, flags=re.IGNORECASE)
                if m_from:
                    tail = (m_from.group(1) or '').strip()
                    additive = '0'
                    if re.search(r'ADDITIVE', tail, flags=re.IGNORECASE):
                        additive = '1'
                        tail = re.sub(r'ADDITIVE', '', tail, flags=re.IGNORECASE).strip()
                    drive, filename = self._parse_mem_destination(tail)
                    if filename or drive:
                        out.append(f"{indent}__DBASE_RESTORE__({self._quote_builtin_arg(filename)}, {additive}, {self._quote_builtin_arg(drive)}){comment_suffix}{nl}")
                        continue

            if re.match(r'^RELEASE', work, flags=re.IGNORECASE):
                rest = re.sub(r'^RELEASE', '', work, count=1, flags=re.IGNORECASE).strip()
                if re.match(r'^ALL', rest, flags=re.IGNORECASE):
                    tail = re.sub(r'^ALL', '', rest, count=1, flags=re.IGNORECASE).strip()
                    mode = 'ALL'
                    mask = ''
                    m_mode = re.match(r'^(LIKE|EXCEPT)\s+(.*)$', tail, flags=re.IGNORECASE)
                    if m_mode:
                        mode = m_mode.group(1).upper()
                        mask = (m_mode.group(2) or '').strip()
                    out.append(f"{indent}__DBASE_RELEASE__('', {self._quote_builtin_arg(mode)}, {self._quote_builtin_arg(mask)}){comment_suffix}{nl}")
                    continue
                if rest:
                    out.append(f"{indent}__DBASE_RELEASE__({self._quote_builtin_arg(rest)}, 'LIST', ''){comment_suffix}{nl}")
                    continue

            out.append(raw_line)

        return ''.join(out)


    def _replace_dot_logical_tokens(self, code: str) -> str:
        if not code:
            return code

        out = []
        i = 0
        n = len(code)
        in_quote = None
        in_bracket = False

        while i < n:
            ch = code[i]

            if in_quote is not None:
                out.append(ch)
                if ch == in_quote:
                    if i + 1 < n and code[i + 1] == in_quote:
                        out.append(code[i + 1])
                        i += 2
                        continue
                    in_quote = None
                i += 1
                continue

            if in_bracket:
                out.append(ch)
                if ch == ']':
                    if i + 1 < n and code[i + 1] == ']':
                        out.append(code[i + 1])
                        i += 2
                        continue
                    in_bracket = False
                i += 1
                continue

            if ch in ('"', "'"):
                in_quote = ch
                out.append(ch)
                i += 1
                continue

            if ch == '[':
                in_bracket = True
                out.append(ch)
                i += 1
                continue

            rem = code[i:].upper()
            if rem.startswith('.NOT.'):
                out.append('NOT')
                i += 5
                continue
            if rem.startswith('.AND.'):
                out.append('AND')
                i += 5
                continue
            if rem.startswith('.OR.'):
                out.append('OR')
                i += 4
                continue

            out.append(ch)
            i += 1

        return ''.join(out)

    def _rewrite_dot_logical_keywords(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ''
            line = raw_line
            if line.endswith('\r\n'):
                line = line[:-2]
                nl = '\r\n'
            elif line.endswith('\n'):
                line = line[:-1]
                nl = '\n'

            if not line.strip():
                out.append(raw_line)
                continue

            code_part, comment_part = self._split_comment_outside(line)
            rewritten = self._replace_dot_logical_tokens(code_part)
            if comment_part:
                rewritten += (' ' if rewritten and not rewritten.endswith(' ') else '') + comment_part.lstrip()
            out.append(rewritten + nl)

        return ''.join(out)

    def _rewrite_dbf_statements(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        for raw_line in lines:
            nl = ''
            line = raw_line
            if line.endswith('\r\n'):
                line = line[:-2]
                nl = '\r\n'
            elif line.endswith('\n'):
                line = line[:-1]
                nl = '\n'

            if not line.strip():
                out.append(raw_line)
                continue

            indent = line[:len(line) - len(line.lstrip())]
            code_part, comment_part = self._split_comment_outside(line)
            work = code_part.strip()
            comment_suffix = '' if not comment_part else ' ' + comment_part.lstrip()

            m = re.match(r'^SELECT\s+TO(?:\s+(.*?))?\s*$', work, flags=re.IGNORECASE)
            if m:
                expr = (m.group(1) or '').strip()
                if not expr:
                    expr = '0'
                out.append(f"{indent}__DBASE_SELECT__({expr}){comment_suffix}{nl}")
                continue

            m = re.match(r'^RENAME\b(.*)$', work, flags=re.IGNORECASE)
            if m:
                rest = (m.group(1) or '').strip()
                to_pos = self._find_keyword_outside(rest, 'TO')
                if to_pos >= 0:
                    old_name = rest[:to_pos].strip()
                    new_name = rest[to_pos + 2:].strip()
                    if old_name and new_name:
                        out.append(f"{indent}__DBASE_RENAME__({self._quote_builtin_arg(old_name)}, {self._quote_builtin_arg(new_name)}){comment_suffix}{nl}")
                        continue

            if re.match(r'^CLEAR\s+ALL\s*$', work, flags=re.IGNORECASE):
                out.append(f"{indent}__DBASE_CLEAR_ALL__(){comment_suffix}{nl}")
                continue

            m = re.match(r'^SKIP(?:\s+(.*?))?\s*$', work, flags=re.IGNORECASE)
            if m:
                expr = (m.group(1) or '').strip()
                if not expr:
                    expr = '1'
                out.append(f"{indent}__DBASE_SKIP__({expr}){comment_suffix}{nl}")
                continue

            m = re.match(r'^(?:GO|GOTO)(?:\s+(.*?))?\s*$', work, flags=re.IGNORECASE)
            if m:
                tail = (m.group(1) or '').strip()
                if not tail:
                    out.append(raw_line)
                    continue
                if tail.upper() in ('TOP', 'BOTTOM'):
                    out.append(f"{indent}__DBASE_GOTO__({self._quote_builtin_arg(tail.upper())}){comment_suffix}{nl}")
                else:
                    out.append(f"{indent}__DBASE_GOTO__({tail}){comment_suffix}{nl}")
                continue

            if re.match(r'^DELETE\s*$', work, flags=re.IGNORECASE):
                out.append(f"{indent}__DBASE_DELETE_RECORD__(){comment_suffix}{nl}")
                continue

            if re.match(r'^PACK\s*$', work, flags=re.IGNORECASE):
                out.append(f"{indent}__DBASE_PACK__(){comment_suffix}{nl}")
                continue

            if re.match(r'^(?:ZIP|ZAP)\s*$', work, flags=re.IGNORECASE):
                out.append(f"{indent}__DBASE_ZAP__(){comment_suffix}{nl}")
                continue

            if re.match(r'^COUNT', work, flags=re.IGNORECASE):
                rest = re.sub(r'^COUNT', '', work, count=1, flags=re.IGNORECASE).strip()
                range_part = ''
                mode = ''
                cond = ''
                to_var = ''

                if rest:
                    pos_to = self._find_keyword_outside(rest, 'TO')
                    if pos_to >= 0:
                        before_to = rest[:pos_to].strip()
                        to_var = rest[pos_to + 2:].strip()
                    else:
                        before_to = rest

                    pos_for = self._find_keyword_outside(before_to, 'FOR')
                    pos_while = self._find_keyword_outside(before_to, 'WHILE')
                    picks = [(p, 'FOR') for p in [pos_for] if p >= 0] + [(p, 'WHILE') for p in [pos_while] if p >= 0]
                    if picks:
                        p, kw = sorted(picks, key=lambda x: x[0])[0]
                        range_part = before_to[:p].strip()
                        mode = kw
                        cond = before_to[p + len(kw):].strip()
                    else:
                        range_part = before_to.strip()

                out.append(f"{indent}__DBASE_COUNT__({self._quote_builtin_arg(range_part)}, {self._quote_builtin_arg(mode)}, {self._quote_builtin_arg(cond)}, {self._quote_builtin_arg(to_var)}){comment_suffix}{nl}")
                continue

            out.append(raw_line)

        return ''.join(out)

    def _rewrite_text_blocks(self, text: str) -> str:
        lines = text.splitlines(keepends=True)
        out = []

        in_text = False
        text_indent = ""
        text_lines = []
        text_start_line = 0

        def flush_text_block():
            flushed = []
            for payload, payload_nl in text_lines:
                escaped = payload.replace(']', ']]')
                flushed.append(f"{text_indent}WRITE [{escaped}]{payload_nl or '\n'}")
            return flushed

        for line_no, raw_line in enumerate(lines, start=1):
            nl = ""
            line = raw_line
            if line.endswith("\r\n"):
                line = line[:-2]
                nl = "\r\n"
            elif line.endswith("\n"):
                line = line[:-1]
                nl = "\n"

            if not in_text:
                code_part, _comment_part = self._split_comment_outside(line)
                stripped_code = code_part.strip()

                if re.match(r'^TEXT\b', stripped_code, flags=re.IGNORECASE):
                    rest = re.sub(r'^TEXT\b', '', stripped_code, count=1, flags=re.IGNORECASE).strip()
                    if rest == "":
                        in_text = True
                        text_indent = line[:len(line) - len(line.lstrip())]
                        text_lines = []
                        text_start_line = line_no
                        continue

                out.append(raw_line)
                continue

            stripped_line = line.strip()
            if re.match(r'^ENDTEXT\b', stripped_line, flags=re.IGNORECASE):
                rest = re.sub(r'^ENDTEXT\b', '', stripped_line, count=1, flags=re.IGNORECASE).strip()
                if rest == "":
                    out.extend(flush_text_block())
                    in_text = False
                    text_indent = ""
                    text_lines = []
                    text_start_line = 0
                    continue

            text_lines.append((line, nl))

        if in_text:
            raise share.common.PreprocessorError(f"unterminated TEXT block starting at line {text_start_line}")

        return ''.join(out)

    def _resolve_include(self, current_file: Path, name: str) -> Path:
        # 1) relativ zum aktuellen file
        cand = (current_file.parent / name).resolve()
        if cand.exists():
            return cand

        # 2) include_paths
        for base in self.include_paths:
            cand2 = (base / name).resolve()
            if cand2.exists():
                return cand2

        raise share.common.PreprocessorError(f'include file not found: "{name}" (from {current_file})')
        
    # Schneidet trailing Kommentare ab: NOTE, &&, **, //, /* ...
    # (Nur bis Zeilenende; Blockkommentar-Mehrzeiligkeit ist für Direktiven egal,
    # weil nach der Direktive sowieso nichts mehr ausgewertet werden soll.)
    def _strip_trailing_comment(self, s: str) -> str:
        if s is None:
            return s

        out = []
        i = 0
        n = len(s)
        in_quote = None

        while i < n:
            ch = s[i]

            if in_quote is not None:
                out.append(ch)
                if ch == in_quote:
                    if i + 1 < n and s[i + 1] == in_quote:
                        out.append(s[i + 1])
                        i += 2
                        continue
                    in_quote = None
                i += 1
                continue

            if ch in ("'", '"'):
                in_quote = ch
                out.append(ch)
                i += 1
                continue

            two = s[i:i+2]
            if two in ("&&", "**", "//", "/*"):
                break

            if self._find_note_comment_start(s[i:]) == 0:
                break

            out.append(ch)
            i += 1

        return "".join(out)

    def _process_file(self, path: Path) -> str:
        if path in self._include_stack:
            chain = " -> ".join(str(p) for p in self._include_stack + [path])
            raise share.common.PreprocessorError(f"circular include detected: {chain}")

        self._include_stack.append(path)
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            out_lines: list[str] = []
            frames: list[share.common.PPFrame] = [share.common.PPFrame(parent_active=True, this_active=True)]

            def active() -> bool:
                return frames[-1].parent_active and frames[-1].this_active

            lines = text.splitlines(keepends=True)
            for i, line in enumerate(lines, start=1):
                # Direktiven erkennen (immer), aber nur ausführen wenn "active"
                raw_line = line
                raw_line = self._rewrite_use_line(raw_line)
                line_for_directive = self._strip_trailing_comment(raw_line).rstrip("\r\n")

                m = self.include_re.match(line_for_directive)
                if m:
                    if active():
                        inc_name = m.group(1)
                        inc_path = self._resolve_include(path, inc_name)
                        out_lines.append(f'**line 1 "{inc_path}"*/\n')
                        out_lines.append(self._process_file(inc_path))
                        out_lines.append(f'**line {i+1} "{path}"*/\n')
                    continue

                m = self.define_re.match(line_for_directive)
                if m:
                    if active():
                        name = m.group(1)
                        tail = (m.group(2) or "").strip()

                        # function-like: direkt nach Name "("
                        if tail.startswith("("):
                            close = tail.find(")")
                            if close == -1:
                                raise share.common.PreprocessorError(f"{path}:{i}: malformed function-like #define")
                            params_part = tail[1:close].strip()
                            body = tail[close+1:].lstrip()

                            params = [p.strip() for p in params_part.split(",")] if params_part else []
                            self.macros[name] = share.common.Macro(name=name, params=params, body=body)
                        else:
                            self.macros[name] = share.common.Macro(name=name, params=None, body=tail)

                        self.defined.add(name)
                    continue
                
                m = self.ifdef_re.match(line_for_directive)
                if m:
                    name = m.group(1)
                    parent = active()
                    cond = name in self.defined
                    frames.append(share.common.PPFrame(
                        parent_active=parent,
                        this_active=cond,
                        start_file=path,
                        start_line=i,
                        kind="#ifdef",
                        name=name
                    ))
                    continue

                m = self.ifndef_re.match(line_for_directive)
                if m:
                    name = m.group(1)
                    parent = active()
                    cond = name not in self.defined
                    frames.append(share.common.PPFrame(
                        parent_active=parent,
                        this_active=cond,
                        start_file=path,
                        start_line=i,
                        kind="#ifndef",
                        name=name
                    ))
                    continue

                if self.else_re.match(line_for_directive):
                    if len(frames) == 1:
                        raise share.common.PreprocessorError(f"{path}:{i}: #else without #if")
                    top = frames[-1]
                    if top.saw_else:
                        raise share.common.PreprocessorError(f"{path}:{i}: multiple #else")
                    top.saw_else = True
                    # else invertiert nur die "this_active" Ebene, parent bleibt gleich
                    top.this_active = not top.this_active
                    continue

                if self.endif_re.match(line_for_directive):
                    if len(frames) == 1:
                        raise share.common.PreprocessorError(f"{path}:{i}: #endif without #if")
                    frames.pop()
                    continue

                # Normale Zeile: nur ausgeben wenn aktiv
                if active():
                     out_lines.append(self._expand_macros_in_line(raw_line))

            if len(frames) != 1:
                top = frames[-1]
                raise share.common.PreprocessorError(
                    f"{path}: EOF: missing #endif for {top.kind} {top.name} "
                    f"(opened at {top.start_file}:{top.start_line})"
                )
                
            return "".join(out_lines)
        finally:
            self._include_stack.pop()
