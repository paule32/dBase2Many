import re

class PascalPreprocessor:
    def __init__(self, defines=None):
        self.defines = set(d.upper() for d in (defines or []))

    def is_defined(self, name):
        return name.upper() in self.defines

    def define(self, name):
        self.defines.add(name.upper())

    def undef(self, name):
        self.defines.discard(name.upper())

    def process(self, text):
        lines = text.splitlines()
        out = []

        active_stack = [True]

        for line in lines:
            stripped = line.strip()

            m = re.match(r"^\{\$([A-Za-z]+)\s*([^}]*)\}", stripped)

            if m:
                cmd = m.group(1).upper()
                arg = m.group(2).strip()

                if cmd == "DEFINE":
                    if active_stack[-1]:
                        self.define(arg)
                    continue

                if cmd == "UNDEF":
                    if active_stack[-1]:
                        self.undef(arg)
                    continue

                if cmd == "IFDEF":
                    active_stack.append(active_stack[-1] and self.is_defined(arg))
                    continue

                if cmd == "IFNDEF":
                    active_stack.append(active_stack[-1] and not self.is_defined(arg))
                    continue

                if cmd == "ELSE":
                    if len(active_stack) <= 1:
                        raise RuntimeError("{$ELSE} without {$IFDEF}")

                    parent_active = active_stack[-2]
                    active_stack[-1] = parent_active and not active_stack[-1]
                    continue

                if cmd == "ENDIF":
                    if len(active_stack) <= 1:
                        raise RuntimeError("{$ENDIF} without {$IFDEF}")

                    active_stack.pop()
                    continue

                # unbekannte Direktiven erstmal ignorieren
                continue

            if active_stack[-1]:
                out.append(line)

        if len(active_stack) != 1:
            raise RuntimeError("missing {$ENDIF}")

        return "\n".join(out) + "\n"
