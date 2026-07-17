# ---------------------------------------------------------------------------
# File:   cbasic.py - BASIC compiler
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

from compiler.frontend.basic.generator  import *

from compiler.writer.pe64coff    import *

from compiler.writer.mz16 import *
from compiler.writer.nt32 import *
from compiler.writer.pe32 import *
from compiler.writer.pe64 import *

from compiler.cli import *

from antlr4 import CommonTokenStream
from antlr4 import FileStream
from antlr4 import InputStream
from antlr4 import ParserRuleContext

from antlr4.error.ErrorListener import ErrorListener
from antlr4.tree.Tree    import TerminalNode

from parsers.basic.BasicLexer          import BasicLexer
from parsers.basic.BasicParser         import BasicParser
from parsers.basic.BasicParserVisitor  import BasicParserVisitor

class NoSourceException(Exception):          pass
class NoCompilerModeException(Exception):    pass
class NoEntryRefinementException(Exception): pass

def parse_basic_source(source: str, source_name: str = "<memory>") -> dict[str, Any]:
    input_stream = InputStream(source)

    lexer = BasicLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(BasicErrorListener(source_name))

    token_stream = CommonTokenStream(lexer)

    parser = BasicParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(BasicErrorListener(source_name))

    tree = parser.program()

    builder = BasicAstBuilder()
    return builder.visit(tree)

def parse_basic_file(filename: str | Path) -> dict[str, Any]:
    path   = Path(filename)
    source = path.read_text(encoding = "utf-8")
    return parse_basic_source(source, str(path))

# ---------------------------------------------------------------------------
# the main definition 
# ---------------------------------------------------------------------------
def main() -> int:
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
        # 0. prepare BASIC file ...
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
            raise NoSourceException(tr("no source file given."))
            
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
        
        if CDATA.args_backend in ["asm", "nasm"]:
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
        
        if ext.lower() in [".basic", ".bas", ".b"]:
            CDATA.args_compilermode = args.compilermode
            source_file = name + ext
        else:
            CDATA.args_compilermode = args.compilermode
            if args.compilermode in ["b", "bas", "basic"]:
                if not ext or len(ext) < 2:
                    source_file = name + ".bas"
            else:
                raise NoCompilerModeException(tr("compiler mode unknown."))
        
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
        
        stream = InputStream(source)
        
        # -----------------------------------------
        # 2. lexical analyse BASIC file ...
        # -----------------------------------------
        lexer   = BasicLexer(stream)
        tokens  = CommonTokenStream(lexer)
        
        # -----------------------------------------
        # 3. parse BASIC file ...
        # -----------------------------------------
        parser  = BasicParser(tokens)
        tree    = parser.program()
        
        if parser.getNumberOfSyntaxErrors() > 0:
            return 1
            raise Exception(tr("source code have syntax errors."))
        
        # -----------------------------------------
        # 4. generate asmjit c++ / nasm code  ...
        # -----------------------------------------
        generator = BasicGenerator(backend, writer=target_obj)
        generator.source_file = os.path.abspath(source_file)
        generator.source_dir  = os.path.dirname(generator.source_file)
        
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
                if not generator.main_emitted:
                    pass
                    #raise NoEntryRefinementException(
                    #    "BASIC source does not contain a 'program:' refinement"
                    #)
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
                    
                    writer.add_jit_context32("ctx")
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
                    writer.write_object(CDATA.obj_file)
                    if generator.root_module_kind == "unit":
                        CDATA.pui_file = generator.write_unit_pui(CDATA.obj_file)
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
        
    except CompileError as e:
        if generator is not None:
            print(generator.format_error(CDATA.src_file, e), file = sys.stderr)
            return 3
        else:
            print(e, file = sys.stderr)
            return 3

    except NoSourceException as e:
        print(tr("Parameter Error:"))
        print(tr("no source given. Use --help to display the help."))
        return 2

    except NoEntryRefinementException as e:
        print(tr("Entry point Error:"))
        print(tr("No start refinement symbol given."))
        return 2
        
    except NoCompilerModeException as e:
        print(tr("Compiler Mode Error:"))
        print(tr("unknown compiler syntax for given file."))
        return 2
        
    except PermissionError as e:
        print(f"{tr('Error')}: {tr('Permission Error')}")
        print(f"Text : {e.message}")
        return 2
        
    except ModuleNotFoundError as e:
        print(f"{tr('Error')}: {tr('Module not found')}")
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
        import traceback
        traceback.print_exc()
        return 2
        
    except FileNotFoundError as e:
        print(f"{tr('Error')}: {tr('File not found')} '{e.filename}'")
        print(f"Text : {e.strerror}")
        print(f"Code : {e.errno}")
        return 2
        
    except TypeError as e:
        print(f"{tr('Error')}: {tr('Type error')}")
        print(f"Text : {str(e)}")
        import traceback
        traceback.print_exc()
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
        
    return 0

# ---------------------------------------------------------------------------
# entry point für start-up the application
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    raise SystemExit(main())

# ---------------------------------------------------------------------------
# E O F  -  End Of File.
# ---------------------------------------------------------------------------
