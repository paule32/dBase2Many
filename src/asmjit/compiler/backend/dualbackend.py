# ---------------------------------------------------------------------------
# File: dualbackend.py - backend for Assembler + Object
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations

from compiler.writer.nt32      import *

from compiler.backend.code     import *
from compiler.backend.coff32   import *
from compiler.backend.nasm     import NasmBackend

class DualBackend(CodeBackend):
    def __init__(self, *backends):
        super().__init__("dual")
        
        if len(backends) == 0:
            raise RuntimeError("No backend specified")
        
        self.backends = list(backends)
        self.backend  = None
        self.logger   = self
        
        if isinstance(backends[0], Coff32Backend):
            self.backend        = backends[0]
            
        if isinstance(backends[1], NT32Writer):
            self.backend.logger = backends[1]
        else:
            raise RuntimeError("unknown code writer.")
            
        #if isinstance(backends[2], NasmBackend):
        #    self.writer = backends[2]
        #else:
        #    raise RuntimeError("unknown backend.")

    def write(self, filename):
        print(str(filename))
        print(self.backend.lines)
        
    def __getattr__(self, name):
        if not name.startswith("emit_"):
            raise AttributeError(name)

        def wrapper(*args, **kwargs):
            result = None

            for backend in self.backends:
                fn = getattr(backend, name, None)
                if fn:
                    r = fn(*args, **kwargs)
                    if result is None:
                        result = r

            return result

        return wrapper

    def save_asm(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("bits 32\n")
            f.write("section .text\n\n")
            f.write("\n".join(self.asm.lines))
            f.write("\n")
