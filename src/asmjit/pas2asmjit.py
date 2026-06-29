# ---------------------------------------------------------------------------
# File:   pascal2asmjit.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import sys
import os
import io
import argparse
import struct
import time

# ---------------------------------------------------------------------------
# i18n / gettext (mo inside zip: <lang>/LC_MESSAGES/dbase.mo)
# ---------------------------------------------------------------------------
import locale
import gettext
import polib

# ---------------------------------------------------------------------------
from os          import linesep   as NL
from datetime    import datetime  as dt
from dataclasses import dataclass
from pathlib     import PureWindowsPath, Path
from typing      import Union

from compiler.common.config    import *
from compiler.common.types     import *
from compiler.common.constants import *
from compiler.common.error     import *
from compiler.common.types     import *
from compiler.common.locale    import *

from compiler.backend.code     import *
from compiler.backend.coff32   import Coff32Backend
from compiler.backend.coff64   import Coff64Backend
from compiler.backend.dos16    import *

from compiler.backend.asmjit   import *
from compiler.backend.nasm     import *

from compiler.frontend.pascal.generator import *
from compiler.frontend.basic .generator import *
from compiler.frontend.c     .generator import *
from compiler.frontend.dbase .generator import *

from compiler.writer.pe64coff    import *

from compiler.writer.mz16 import *
from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.cli import *
from antlr4       import *

from parsers.pascal.MiniPascalLexer          import MiniPascalLexer
from parsers.pascal.MiniPascalParser         import MiniPascalParser
from parsers.pascal.MiniPascalParserVisitor  import MiniPascalParserVisitor

COMMENT_REPL = ('-' * 77)

def ask_yes_no(question, default=False):
    while True:
        answer = input(question + " (y/N): ").strip().lower()
        
        if answer in ("j", "y", "ja", "yes"):
            return True
        
        if answer in ("n", "no", "nein"):
            return False
        
        if answer == "":
            return default
        
        print(tr("Enter [Y]es or [N]o ."))

def is_windows_drive(path: Path) -> bool:
    resolved = path.resolve()
    anchor = Path(resolved.anchor)

    return resolved == anchor

def can_write_file(path: Path) -> bool:
    try:
        with open(path, "a+b"):
            pass
        return True
    except PermissionError:
        return False
    except OSError:
        return False

# ---------------------------------------------------------------------------
# the pre-processor class ...
# ---------------------------------------------------------------------------
class PascalPreprocessor:
    def __init__(self):
        self.defines = set()
    
    def process(self, text):
        lines   = text.splitlines()
        
        output  = []
        stack   = []
        enabled = True
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.lower() == "{$break}":
                if enabled:
                    output.append("__debug_break;")
                    output.append("")
                else:
                    output.append("")
                continue
            
            if stripped.startswith("{$define"):
                output.append("")
                name = stripped[8:-1].strip()
                self.defines.add(name.upper())
                continue
            
            if stripped.startswith("{$undef"):
                output.append("")
                name = stripped[7:-1].strip()
                self.defines.discard(name.upper())
                continue
            
            if stripped.startswith("{$ifdef"):
                output.append("")
                name = stripped[7:-1].strip()
                cond = name.upper() in self.defines
                
                stack.append(enabled)
                enabled = enabled and cond
                continue
            
            if stripped.startswith("{$ifndef"):
                output.append("")
                name = stripped[8:-1].strip()
                cond = name.upper() not in self.defines
                
                stack.append(enabled)
                enabled = enabled and cond
                continue
            
            if stripped.startswith("{$else"):
                output.append("")
                parent  = stack[-1]
                enabled = parent and not enabled
                continue
            
            if stripped.startswith("{$endif"):
                output.append("")
                enabled = stack.pop()
                continue
            
            if enabled:
                output.append(line)
        
        return "\n".join(output)



# ---------------------------------------------------------------------------
# generic output writer's ...
# ---------------------------------------------------------------------------
class OutputWriter:
    def write(self, filename):    raise NotImplementedError

class PE32ExeWriter(OutputWriter):
    def __init__(self, coff):
        self.coff = coff
    
    def write(self, filename):
        pe = PE32Writer(self.coff)
        pe.write(filename)
        
class PE64ExeWriter(OutputWriter):
    def __init__(self, coff):
        self.coff = coff
        
    def write(self, filename):
        pe = PE64Writer(self.coff)
        pe.write(filename)

class CoffObjectWriter(OutputWriter):
    def __init__(self,  coff):
        self.coff = coff
        
    def write(self, filename):
        self.coff.write(filename)
        
class DosExeWriter(OutputWriter):
    def __init__(self, mz):
        self.mz = mz
        
    def write(self, filename):
        self.mz.write(filename)

# ---------------------------------------------------------------------------
# the main definition 
# ---------------------------------------------------------------------------
def main():
    #if len(sys.argv) != 2:
    #    print("Usage: python pascal_to_asmjit.py file.pas", file=sys.stderr)
    #    return 1
    
    generator   = None
    source_file = ""
    
    args_parser = args_func()
    args        = None
    
    CDATA.InputFiles = []
    CDATA.CurrentWorkingDir = os.getcwd()
    try:
        # -----------------------------------------
        # 0. prepare pascal file ...
        # -----------------------------------------
        args = args_parser.parse_args()
        
        CDATA.args_target = args.target
        
        args = handle_args(args)
        
        # -----------------------------------------
        # get input source file
        # -----------------------------------------
        if not args.source:
            CDATA.LastErrorCode = LastError.NO_SOURCE
            raise Exception(tr("no source file given."))
        
        # -----------------------------------------
        # get target platform ...
        # -----------------------------------------
        if not args.target:
            CDATA.LastErrorCode = LastError.NO_TARGET
            raise Exception(tr("no target platform given."))
        
        if args.target in ["dos", "dos16", "nt35", "winnt", "win32", "win64"]:
            CDATA.args_target = args.target
        else:
            CDATA.LastErrorCode = LastError.NO_TARGET
            raise Exception(tr("given target is not supported."))
        
        # -----------------------------------------
        # set backend
        # -----------------------------------------
        backend    = None
        writer     = None
        target_obj = None
        # -----------------------------------------
        if   args.backend in ["c++", "asmjit"]:
            CDATA.args_backend = BACKEND_ASMJIT
            if args.target in ["win32", "win64"]:
                backend    = AsmJitBackend()
                writer     = CppOutputWriter()
                
        elif args.backend in ["asm", "nasm"]:
            CDATA.args_backend = BACKEND_NASM
            if args.target in ["win32", "win64"]:
                backend    = NasmBackend()
                writer     = NasmOutputWriter()
        
        elif args.backend in ["obj", "objfile"]:
            CDATA.args_backend = BACKEND_OBJFILE
            if args.target in ["win32", "win64"]:
                target_obj = PE64CoffWriter()
                backend    = Coff64Backend(target_obj)
                writer     = CoffObjectWriter(target_obj)
        
        elif args.backend in ["exe", "exefile"]:
            CDATA.args_backend = BACKEND_EXEFILE
            if args.target in ["nt35", "winnt", "win32"]:
                writer     = PE32Writer()
                target_obj = NT32Writer(writer)
                backend    = Coff32Backend(writer)
            
            elif args.target in ["dos", "dos16"]:
                target_obj = MZ16Writer()
                backend    = DosBackend(target_obj)
                writer     = DosExeWriter(target_obj)
            
            elif args.target in ["win64"]:
                target_obj = PE64CoffWriter()
                backend    = Coff64Backend(target_obj)
                writer     = PE64ExeWriter(target_obj)
        else:
            CDATA.LastErrorCode = LastError.NO_BACKEND
            raise Exception(tr("backend not supported."))
            
        if backend is None:
            CDATA.LastErrorCode = LastError.NO_BACKEND
            raise Exception(tr("could not create backend"))
        
        source_file = args.source
        name, ext   = os.path.splitext(source_file)
        found       = False
        
        if ext.lower() in [".pas", ".pp", ".c", ".cc", ".cpp"]:
            CDATA.args_compilermode = args.compilermode
            source_file = name + ext
        else:
            CDATA.args_compilermode = args.compilermode
            if args.compilermode in ["pp", "pas", "pascal"]:
                if not ext or len(ext) < 2:
                    source_file = name + ".pas"
            elif args.compilermode in ["c", "cc", "cpp"]:
                if not ext or len(ext) < 2:
                    source_file = name + ".cc"
            else:
                raise Exception(tr("compiler mode unknown."))
        
        print('T: ' + CDATA.args_target)
        print('B: ' + CDATA.args_backend)
        
        # todo !!!
        CDATA.InputFiles.append(source_file)
        
        # -----------------------------------------
        # tackle file + path
        # -----------------------------------------
        name, _  = os.path.splitext(os.path.basename(source_file))
        CDATA.src_file = CDATA.InputFiles[0]
        CDATA.asm_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".asm")
        CDATA.cpp_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".cc" )
        CDATA.obj_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".o"  )
        CDATA.exe_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".exe")
        
        print("Compile-Run ...")
        print("---------------------------")
        print("input : ", CDATA.src_file)
        print("output: ", CDATA.exe_file)
        print("")
        print("nasm  : ", CDATA.asm_file)
        print("asmjit: ", CDATA.cpp_file)
        print("object: ", CDATA.obj_file)
        print("win64 : ", CDATA.exe_file)
        print("---------------------------")
        
        # -----------------------------------------
        # open source file and read contents
        # -----------------------------------------
        with open(CDATA.src_file, "r", encoding="utf-8") as f:
            source = f.read()
            f.close()
        
        # -----------------------------------------
        # 1. pre-process pascal file ...
        # -----------------------------------------
        pre     = PascalPreprocessor()
        
        for define in args.define:
            pre.defines.add(define.upper())
        
        source  = pre.process(source)
        stream  = InputStream(source)
        
        # -----------------------------------------
        # 2. lexical analyse pascal file ...
        # -----------------------------------------
        lexer   = MiniPascalLexer(stream)
        tokens  = CommonTokenStream(lexer)
        
        # -----------------------------------------
        # 3. parse pascal file ...
        # -----------------------------------------
        parser  = MiniPascalParser(tokens)
        tree    = parser.sourceFile()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            return 1
            raise Exception(tr("source code have syntax errors."))
        
        # -----------------------------------------
        # 4. generate asmjit c++ / nasm code  ...
        # -----------------------------------------
        generator = GeneratorClass(backend, target_obj)
        generator.source_file = os.path.abspath(source_file)
        generator.source_dir  = os.path.dirname(generator.source_file)
        
        text = generator.visit(tree)
        
        # -----------------------------------------
        # 5. finalize: create c++ output file ...
        # -----------------------------------------
        overwrite = "exists. Overwrite? (Y/N): "
        
        if CDATA.args_target.lower() in ["dos", "dos16"]:
            if CDATA.args_backend.lower() == BACKEND_EXEFILE:
                outfile = Path(CDATA.exe_file)
                if outfile.exists():
                    check = input(f"{CDATA.exe_file}: {overwrite}").strip().lower()
                    if check in ('j', 'y'):
                        target_obj.write(CDATA.exe_file)
                else:   target_obj.write(CDATA.exe_file)
        
        elif CDATA.args_target.lower() in ["nt35", "winnt", "win32"]:
            if CDATA.args_backend.lower() == BACKEND_EXEFILE:
                outfile = Path(CDATA.exe_file)
                if outfile.exists():
                    check = input(f"{CDATA.exe_file}: {overwrite}").strip().lower()
                    if check in ('j', 'y'):
                        generator.write_string_literals_to_coff()
                        generator.write_double_literals_to_coff()
                        writer.write(CDATA.exe_file)
                else:
                    generator.write_string_literals_to_coff()
                    generator.write_double_literals_to_coff()
                    writer.write(CDATA.exe_file)
                
        elif CDATA.args_target.lower() == "win64":
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                if not CDATA.cpp_file:
                    CDATA.cpp_file = "aout.cc"
                outfile = Path(CDATA.cpp_file)
                if outfile.exists():
                    check = input(f"{cpp_file}: {overwrite}").strip().lower()
                    if check in ('j', 'y'):
                        with open(CDATA.cpp_file, "w", encoding="utf-8") as f:
                            f.write(text)
                            f.close()
                else:
                    with open(CDATA.cpp_file, "w", encoding="utf-8") as f:
                        f.write(text)
                        f.close()
            elif CDATA.BackEnd.current == BACKEND_NASM:
                if not CDATA.asm_file:
                    CDATA.asm_file = "aout.asm"
                outfile = Path(CDATA.asm_file)
                if outfile.exists():
                    check = input(f"{CDATA.asm_file}: {overwrite}").strip().lower()
                    if check in ('j', 'y'):
                        with open(CDATA.asm_file, "w", encoding="utf-8") as f:
                            f.write(text)
                            f.close()
                        CDATA.BackEnd.current = CDATA.args_backend
                else:
                    with open(CDATA.asm_file, "w", encoding="utf-8") as f:
                        f.write(text)
                        f.close()
            elif CDATA.BackEnd.current == BACKEND_EXEFILE:
                if not CDATA.obj_file:
                    CDATA.obj_file = "aout.o"
                outfile = Path(CDATA.obj_file)
                if outfile.exists():
                    check = input(f"{CDATA.obj_file}: {overwrite}").strip().lower()
                    if check in ('j', 'y'):
                        generator.write_string_literals_to_coff()
                        generator.write_fpc_import_unit()
                        target_obj.write(CDATA.exe_file)
                        #pe = PEWriter64(target_obj)
                        #pe.write(CDATA.exe_file)
                        ##generator.write_main(CDATA.obj_file, CDATA.exe_file)
                        #with open(CDATA.obj_file, "w", encoding="utf-8") as f:
                        #    f.write(text)
                        #    f.close()
                else:
                    generator.write_string_literals_to_coff()
                    generator.write_fpc_import_unit()
                    target_obj.write()
                    #pe = PEWriter64(target_obj)
                    #pe.write(CDATA.exe_file)
                    ##generator.write_main(CDATA.obj_file, CDATA.exe_file)
                    #with open(CDATA.obj_file, "w", encoding="utf-8") as f:
                    #    f.write(text)
                    #    f.close()
        else:
            #print(text)
            raise Exception(tr("backend not given or not supported."))
        
        return 0
    
    except CompileError as e:
        if generator is not None:
            print(generator.format_error(source_file, e), file = sys.stderr)
            return 3
        else:
            print(e, file = sys.stderr)
            return 3
    except PermissionError as e:
        print(f"{tr('Error')}: {tr('Permission Error')}")
        print(f"Text : {e.message}")
        return 2
    except ArgumentParserError as e:
        print(f"{tr('Error')}: {tr('Invalid argument(s)')}")
        print(f"Text : {e.message}")
        #print(f"Code : {e.errno}")
        return 2
    except AttributeError as e:
        print(f"{tr('Error')}: {tr('Attribute Error')}")
        print(f"Text : {str(e)}")
        return 2
    except FileNotFoundError as e:
        print(f"{tr('Error')}: {tr('File not found')} '{e.filename}'")
        print(f"Text : {e.strerror}")
        print(f"Code : {e.errno}")
        return 2
    except TypeError as e:
        print(f"{tr('Error')}: {tr('Type error')}")
        print(f"Text : {str(e)}")
        return 2
    except ArithmeticError as e:
        print(f"{tr('Error')}: {tr('Arithmetic Error')}")
        print(f"Text : {tr('Division through 0')}")
        return 2
    except Exception as e:
        print(f"{tr('Error')}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    #except Exception as e:
    #    print(e, file=sys.stderr)
    #    return 1

# ---------------------------------------------------------------------------
# entry point für start-up the application
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())

# ---------------------------------------------------------------------------
# E O F  -  End Of File.
# ---------------------------------------------------------------------------
