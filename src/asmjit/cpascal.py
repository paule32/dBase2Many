# ---------------------------------------------------------------------------
# File:   cpascal.py - pascal compiler
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__ import annotations

import sys
import os
import re
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
from dataclasses import dataclass, field
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

from compiler.frontend.pascal.generator  import *

from compiler.writer.pe64coff    import *

from compiler.writer.mz16 import *
from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.cli import *
from antlr4       import *

from compiler.frontend.pascal.preprocessor   import (
    ConditionalExpressionError,
    PascalPreprocessorError,
    PascalDirectiveAbort,
    PascalPreprocessor
)
from parsers.pascal.PascalLexer          import PascalLexer
from parsers.pascal.PascalParser         import PascalParser
from parsers.pascal.PascalParserVisitor  import PascalParserVisitor

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
    
    if getattr(sys, "frozen", False):
        CDATA.CurrentWorkingDir = Path(sys.executable).resolve().parent
    else:
        CDATA.CurrentWorkingDir = Path(__file__).resolve().parent
    
    try:
        # -----------------------------------------
        # 0. prepare pascal file ...
        # -----------------------------------------
        args = args_parser.parse_args()
        
        CDATA.args_target  = args.target
        CDATA.args_backend = args.backend
        
        args = handle_args(args)
        
        CDATA.force_write  = args.forcewrite
        
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
        
        if CDATA.debug_mode:
            print("back: ", CDATA.args_backend)
        # -----------------------------------------
        if CDATA.args_backend in ["c++", "asmjit"]:
            if args.target in ["win32", "win64"]:
                backend    = AsmJitBackend()
                writer     = CppOutputWriter()
                
        elif CDATA.args_backend in ["asm", "nasm"]:
            if args.target in ["win32", "win64"]:
                backend    = NasmBackend()
                writer     = NasmOutputWriter()
        
        elif CDATA.args_backend in ["obj", "objfile"]:
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                writer     = PE32Writer()
                backend    = Coff32Backend(writer)
                target_obj = writer
                
            elif CDATA.args_target in ["win64"]:
                target_obj = PE64CoffWriter()
                backend    = Coff64Backend(target_obj)
                writer     = CoffObjectWriter(target_obj)
        
        elif CDATA.args_backend in ["dll", "dllfile"]:
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                writer     = PE32Writer()
                backend    = Coff32Backend(writer)
                target_obj = writer
                
            elif CDATA.args_target in ["win64"]:
                pass
                
        elif CDATA.args_backend in ["exe", "exefile"]:
            if CDATA.args_target in ["nt35", "winnt", "win32"]:
                writer     = PE32Writer()
                target_obj = NT32Writer(writer)
                backend    = Coff32Backend(writer)
            
            elif CDATA.args_target in ["dos", "dos16"]:
                target_obj = MZ16Writer()
                backend    = DosBackend(target_obj)
                writer     = DosExeWriter(target_obj)
            
            elif CDATA.args_target in ["win64"]:
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
        
        if CDATA.debug_mode:
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
        CDATA.pui_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".pui")
        CDATA.dll_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".dll")
        CDATA.exe_file = PureWindowsPath(CDATA.CurrentWorkingDir) / (name + ".exe")
        
        if CDATA.debug_mode:
            print("Compile-Run ...")
            print("---------------------------")
            print("input : ", CDATA.src_file)
            print("output: ", CDATA.exe_file)
            print("")
            print("nasm  : ", CDATA.asm_file)
            print("asmjit: ", CDATA.cpp_file)
            print("object: ", CDATA.obj_file)
            print("pui32 : ", CDATA.pui_file)
            print("dll32 : ", CDATA.dll_file)
            print("win64 : ", CDATA.exe_file)
            print("---------------------------")
        
        # -----------------------------------------
        # open source file and read contents
        # -----------------------------------------
        with open(CDATA.src_file, "r", encoding="utf-8") as f:
            source = f.read()
            f.close()
        
        # -----------------------------------------
        # 1. Makros verwendeter Units aus PUI laden
        # -----------------------------------------
        raw_source = source
        
        imported_unit_macros = collect_used_unit_macros(
            raw_source  = raw_source,
            source_file = CDATA.src_file
        )

        # Optional zum Testen:
        if CDATA.debug_mode:
            print("Imported PUI macros:",imported_unit_macros)
        
        # -----------------------------------------
        # 2. Preprocessor erstellen
        #
        # Priorität:
        #
        #   PUI-Makros
        #   CDATA.Defines
        #   Kommandozeilen-Defines
        #   lokale {$DEFINE}-Anweisungen
        #
        # Lokale Definitionen haben damit die höchste Priorität.
        # -----------------------------------------
        pre = PascalPreprocessor(
            defines=imported_unit_macros
        )

        pre.add_initial_defines(
            getattr(
                CDATA,
                "Defines",
                []
            )
        )

        pre.add_initial_defines(
            getattr(
                args,
                "define",
                []
            ) or []
        )

        # -----------------------------------------
        # 3. Hauptdatei bzw. Unit präprozessieren
        # -----------------------------------------
        source = pre.process(
            raw_source,
            filename=CDATA.src_file
        )

        stream = InputStream(
            source
        )

        # Nur die Makros speichern, die in der aktuellen Quelldatei
        # selbst durch {$DEFINE ...} definiert wurden.
        CDATA.unit_source_macros = dict(
            pre.source_macros
        )

        # Importierte Werte können getrennt gespeichert werden.
        CDATA.imported_unit_macros = dict(
            imported_unit_macros
        )
        
        # -----------------------------------------
        # 2. lexical analyse pascal file ...
        # -----------------------------------------
        lexer   = PascalLexer(stream)
        tokens  = CommonTokenStream(lexer)
        
        # -----------------------------------------
        # 3. parse pascal file ...
        # -----------------------------------------
        parser  = PascalParser(tokens)
        tree    = parser.sourceFile()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            return 1
            raise Exception(tr("source code have syntax errors."))
        
        # -----------------------------------------
        # 4. generate asmjit c++ / nasm code  ...
        # -----------------------------------------
        generator = PascalGenerator(backend, writer=target_obj)
        generator.source_file = os.path.abspath(source_file)
        generator.source_dir  = os.path.dirname(generator.source_file)
        
        # ----------------------------------------------------------
        # Die im Preprocessor gefundenen Unit-Makros an den
        # Generator übergeben.
        #
        # write_unit_pui() liest später self.unit_source_macros.
        # ----------------------------------------------------------
        generator.unit_source_macros = dict(
            pre.source_macros
        )
        
        text = generator.visit(tree)
        
        if CDATA.debug_mode:
            print(generator.backend.asm_lines)
        
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
            if CDATA.args_backend.lower() in ["exe", "exefile"]:
                module_kind = getattr(
                    generator,
                    "root_module_kind",
                    None
                )
                requested_backend = str(
                    getattr(
                        args,
                        "backend",
                        ""
                    )
                ).lower()
                if module_kind == "unit" and requested_backend not in ("", "obj", "object"):
                    raise RuntimeError(
                        tr("Pascal units can only be compiled as COFF objects; "
                        "use -Bobj")
                    )
                outfile = Path(CDATA.exe_file)
                check   = ['j','y']
                if outfile.exists():
                    if CDATA.force_write == False:
                        check = []
                        check = input(f"{CDATA.exe_file}: {overwrite}").strip().lower()
                    else:
                        check = ['j', 'y']
                if ('y' in check) or ('j' in check):
                    generator.write_string_literals_to_coff()
                    generator.write_double_literals_to_coff()
                    writer.write(CDATA.exe_file)
                else:
                    print(tr("no files written"))
                    
            elif CDATA.args_backend.lower() in ["obj", "objfile"]:
                outfile = Path(CDATA.obj_file)
                check   = ['j','y']
                if outfile.exists():
                    if CDATA.force_write == False:
                        check = []
                        check = input(f"{CDATA.obj_file}: {overwrite}").strip().lower()
                if ('y' in check) or ('j' in check):
                    generator.write_string_literals_to_coff()
                    generator.write_double_literals_to_coff()
                    writer.write_object(CDATA.obj_file,
                        embedded_objects=(
                            generator.root_embedded_objects
                            if generator.root_module_kind == "unit"
                            else []
                        )
                    )
                    if generator.root_module_kind == "unit":
                        CDATA.pui_file = generator.write_unit_pui(CDATA.obj_file)
                        if CDATA.args_verbose == False:
                            print(f"COFF32 unit object: {CDATA.obj_file}")
                            print(f"Pascal unit interface: {CDATA.pui_file}")
                else:
                    print(tr("no files written"))
                    
            elif CDATA.args_backend.lower() in ["dll", "dllfile"]:
                outfile = Path(CDATA.dll_file)
                check   = ['j','y']
                if outfile.exists():
                    if CDATA.force_write == False:
                        check = []
                        check = input(f"{CDATA.dll_file}: {overwrite}").strip().lower()
                if ('y' in check) or ('j' in check):
                    generator.write_string_literals_to_coff()
                    generator.write_double_literals_to_coff()
                    writer.write(CDATA.dll_file)
                else:
                    print(tr("no files written"))
                
        elif CDATA.args_target.lower() == "win64":
            if CDATA.args_backend in ["asmjit"]:
                if not CDATA.cpp_file:
                    CDATA.cpp_file = "aout.cc"
                outfile = Path(CDATA.cpp_file)
                if outfile.exists():
                    if CDATA.force_write == False:
                        check = input(f"{CDATA.cpp_file}: {overwrite}").strip().lower()
                    else:
                        check = ['j','y']
                if ('y' in check) or ('j' in check):
                    with open(CDATA.cpp_file, "w", encoding="utf-8") as f:
                        f.write(text)
                        f.close()
                else:
                    print(tr("no files written"))
                    
            elif CDATA.args_backend in ["asm", "nasm"]:
                if not CDATA.asm_file:
                    CDATA.asm_file = "aout.asm"
                outfile = Path(CDATA.asm_file)
                if outfile.exists():
                    if CDATA.force_write == False:
                        check = input(f"{CDATA.asm_file}: {overwrite}").strip().lower()
                    else:
                        check = ['j','y']
                if ('y' in check) or ('j' in check):
                    with open(CDATA.asm_file, "w", encoding="utf-8") as f:
                        f.write(text)
                        f.close()
                else:
                    print(tr("no files written"))

            elif CDATA.args_backend in ["exe", "exefile"]:
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

    except FileNotFoundError as e:
        print(e)
        return 1
        
    except NotADirectoryError as e:
        print(e)
        return 1
        
    except ConditionalExpressionError as e:
        print("-------------------------------------")
        print(e)
        return 1
    
    except PascalPreprocessorError as e:
        print(e)
        return 1
        
    except PascalDirectiveAbort as e:
        #print(e)
        return 1
        
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
        if CDATA.args_verbose:
            import traceback
            traceback.print_exc()
        return 2
        
    except ArgumentParserError as e:
        print(f"{tr('Error')}: {tr('Invalid argument(s)')}")
        print(f"Text : {e.message}")
        if CDATA.args_verbose:
            import traceback
            traceback.print_exc()
        return 2
        
    except AttributeError as e:
        print(f"{tr('Error')}: {tr('Attribute Error')}")
        print(f"Text : {str(e)}")
        if CDATA.args_verbose == False:
            import traceback
            traceback.print_exc()
        return 2
        
    except FileNotFoundError as e:
        print(f"{tr('Error')}: {tr('File not found')} '{e.filename}'")
        print(f"Text : {e.strerror}")
        print(f"Code : {e.errno}")
        if CDATA.args_verbose:
            import traceback
            traceback.print_exc()
        return 2
        
    except TypeError as e:
        print(f"{tr('Error')}: {tr('Type error')}")
        print(f"Text : {str(e)}")
        if CDATA.args_verbose:
            import traceback
            traceback.print_exc()
        return 2
        
    except ArithmeticError as e:
        print(f"{tr('Error')}: {tr('Arithmetic Error')}")
        print(f"Text : {tr('Division through 0')}")
        if CDATA.args_verbose:
            import traceback
            traceback.print_exc()
        return 2
        
    except Exception as e:
        print(f"{tr('Error')}: {str(e)}")
        if CDATA.args_verbose:
            import traceback
            traceback.print_exc()
        return 1
        
# ---------------------------------------------------------------------------
# entry point für start-up the application
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())

# ---------------------------------------------------------------------------
# E O F  -  End Of File.
# ---------------------------------------------------------------------------
