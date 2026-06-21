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

from os          import linesep   as NL
from datetime    import datetime  as dt
from dataclasses import dataclass
from pathlib     import PureWindowsPath, Path
from typing      import Union

from antlr4      import *

from parsers.pascal.MiniPascalLexer          import MiniPascalLexer
from parsers.pascal.MiniPascalParser         import MiniPascalParser
from parsers.pascal.MiniPascalParserVisitor  import MiniPascalParserVisitor

# ---------------------------------------------------------------------------
# we support the following backend's:
# - nasm
# - asmjit
# ---------------------------------------------------------------------------
BACKEND_ASMJIT  = "asmjit"
BACKEND_NASM    = "nasm"
BACKEND_OBJFILE = "objfile"

@dataclass
class LastError:
    NO_ERROR                : int =    0
    NO_MEMORY               : int =    1
    NO_SOURCE               : int =    2
    NO_TARGET               : int =    3
    NO_FILE                 : int =    4
    NO_DIRECTORY            : int =    5
    NO_FILE_OR_DIRECTORY    : int =    6
    FILE_NOT_FOUND          : int =    7
    FILE_EXISTS             : int =    8
    FILE_LOCKED             : int =    9
    IS_FILE                 : int =   10
    IS_DIRECTORY            : int =   11
    PATH_NO_DIRECTORY       : int = 1000
    DIRECTORY_DONT_EXISTS   : int = 1001
    DIRECTORY_NOT_READABLE  : int = 1002
    DIRECTORY_NOT_WRITEABLE : int = 1003

@dataclass
class LastError:
    NO_ERROR                : int =    0
    NO_MEMORY               : int =    1
    NO_SOURCE               : int =    2
    NO_TARGET               : int =    3
    NO_FILE                 : int =    4
    NO_DIRECTORY            : int =    5
    NO_FILE_OR_DIRECTORY    : int =    6
    FILE_NOT_FOUND          : int =    7
    FILE_EXISTS             : int =    8
    FILE_LOCKED             : int =    9
    IS_FILE                 : int =   10
    IS_DIRECTORY            : int =   11
    PATH_NO_DIRECTORY       : int = 1000
    DIRECTORY_DONT_EXISTS   : int = 1001
    DIRECTORY_NOT_READABLE  : int = 1002
    DIRECTORY_NOT_WRITEABLE : int = 1003

# ---------------------------------------------------------------------------
# 16-bit register placeholder ...
# ---------------------------------------------------------------------------
REG_AL     = "al"       # low register
REG_AH     = "ah"       # high register

REG_AX     = "ax"       # alround / return code register
REG_BX     = "bx"       # backup register
REG_CX     = "cx"       # counter register
REG_DX     = "dx"       # decrement register
REG_BP     = "bp"       # base pointer register
REG_SP     = "sp"       # stack pointer register
REG_SI     = "si"       # source index register
REG_DI     = "di"       # destination index register
# ---------------------------------------------------------------------------
# 32-bit register placeholder ...
# ---------------------------------------------------------------------------
REG_EAX     = "eax"     # alround / return code register
REG_EBX     = "ebx"     # backup register
REG_ECX     = "ecx"     # counter register
REG_RDX     = "edx"     # decrement register
REG_EBP     = "ebp"     # extended base pointer register
REG_ESP     = "esp"     # extended stack pointer register
REG_ESI     = "esi"     # extended source index register
REG_EDI     = "edi"     # extended destination index register
# ---------------------------------------------------------------------------
# 64-bit register placeholder ...
# ---------------------------------------------------------------------------
REG_RAX     = "rax"     # alround / return code register
REG_RBX     = "rbx"     # backup register
REG_RCX     = "rcx"     # counter register
REG_RDX     = "rdx"     # decrement register
REG_RBP     = "rbp"     # 64-bit base pointer register
REG_RSP     = "rsp"     # stack pointer register
REG_RSI     = "rsi"     # source index register
REG_RDI     = "rdi"     # destination index register

# ---------------------------------------------------------------------------
# misc. placeholder's ...
# ---------------------------------------------------------------------------
ASM_OUT_PH  = "asm_out << "

# ---------------------------------------------------------------------------
# coff writer constants:
# ---------------------------------------------------------------------------
IMAGE_FILE_MACHINE_AMD64        = 0x8664

IMAGE_SCN_CNT_CODE              = 0x00000020
IMAGE_SCN_CNT_INITIALIZED_DATA  = 0x00000040

IMAGE_SCN_MEM_EXECUTE           = 0x20000000
IMAGE_SCN_MEM_READ              = 0x40000000
IMAGE_SCN_MEM_WRITE             = 0x80000000

IMAGE_SYM_CLASS_EXTERNAL        = 2
IMAGE_SYM_CLASS_STATIC          = 3

IMAGE_SYM_DTYPE_FUNCTION        = 0x20

IMAGE_REL_AMD64_ADDR64          = 0x0001
IMAGE_REL_AMD64_REL32           = 0x0004

# ---------------------------------------------------------------------------
# backend assembly ...
# ---------------------------------------------------------------------------
class BackEndInfo():
    def __init__(self):
        self.asmjit  = BACKEND_ASMJIT
        self.nasm    = BACKEND_NASM
        self.lines   = ""
        self.current = ""

class CommonData():
    def __init__(self):
        self.LastErrorCode       : int  = 0
        self.BackEnd             = BackEndInfo()
        self.CurrentWorkingDir   : str  = ""
        self.src_file            : str  = ""
        self.asm_file            : str  = ""
        self.cpp_file            : str  = ""
        self.exe_file            : str  = ""
        self.obj_file            : str  = ""
        self.ExeOutputDir        : str  = ""
        self.InputFiles          : list = []
        self.IncludeDirs         : list = []

global CDATA
CDATA = CommonData()
# ---------------------------------------------------------------------------
# used error code to information text map ...
# ---------------------------------------------------------------------------
ERROR_MAP = {
    "E0001": "Identifier not found: {name}",
    "E0002": "Duplicate identifier: {name}",
    "E0003": "Variable not declared: {name}",
    "E0004": "Unknown type: {name}",
    "E0005": "Incompatible types: got {got}, expected {expected}",
    "E0006": "Illegal assignment",
    "E0007": "Variable identifier expected",
    "E0008": "Unknown type",
    "E0009": "Duplicate variable declaration",
    "E0010": "Constant cannot be assigned",
    "E0011": "Unsupported local variable type: {typ}",
    "E0012": "Local variable not found: {name}",
    "E0013": "Unsupported assignment type: {var_type}",
    "E0014": "Unsupported variable type: {var_type}",
    "E0015": "Unsupported factor: {text}",
    "E0016": "Duplicate enum type: {name}",
    "E0017": "Duplicate enum value: {value_name}",
    "E0018": "Enum value name expected",
    "E0019": "{text}",
}

COMMENT_REPL = ('-' * 77)

# ---------------------------------------------------------------------------
# data classes as record workaround ...
# ---------------------------------------------------------------------------
@dataclass
class EnumInfo:
    name        : str
    values      : dict[str, int]

@dataclass
class RecordFieldInfo:
    name        : str
    type        : str
    offset      : int
    size        : int
    visibility  : str = "public"

@dataclass
class RecordInfo:
    name        : str
    fields      : dict[str, RecordFieldInfo]
    size        : int

@dataclass
class ArrayInfo:
    name        : str
    index_min   : int
    index_max   : int
    element_type: str
    element_size: int
    size        : int
    init_values : list
    dimensions  : list
    is_dynamic  : bool = False

@dataclass
class ClassMethodInfo:
    name        : str
    kind        : str
    label       : str
    params      : list
    owner       : str
    return_type : str | None = None
    implemented : bool = False
    mangled     : str | None = None
    visibility  : str = "public"

@dataclass
class ClassInfo:
    name        : str
    fields      : dict[str, RecordFieldInfo]
    methods     : dict[str, list[ClassMethodInfo]]
    size        : int
    parent      : str | None = None

# ---------------------------------------------------------------------------
# locales (gnu gettext) support ...
# Loads GNU gettext .mo files from a zip and provides tr().
# ---------------------------------------------------------------------------
class TranslationManager:
    def get_default_lang(self) -> str:
        loc = locale.getlocale()
        if loc is None: return "en"
        
        lang = loc[0]
        if not lang: return "en"
        return lang
    
    def add_trans(self, trans: gettext.GNUTranslations):
        self.translations.append(trans)
        
    def __init__(self, mode: int = 0):
        self.lang         = self.get_default_lang().split("_")[0].lower()
        self.mode         = mode
        self.translations = []
        self.filename     = ""
        self.trans        = gettext.NullTranslations()
        
        self._langSwitch(self.lang)
    
    def _trres(self, msgid:str) -> str:
        for trans in self.translations:
            text = trans.gettext(msgid)
            if text != msgid:
                return text
        return msgid
    
    def _langSwitch(self, lang: str):
        self.lang = lang
        self.translations.clear()
        self.filename = f"locales/{lang}/pascal.mo"
        try:
            self.trans = self.load_mo(self.filename)
            self.add_trans(self.trans)
            
        except FileNotFoundError as e:
            app = self.ensure_app()
            print(f"File not found Error:")
            print(f"The requested file: {self.filename} could not be found.")
            return
            
        except PermissionError as e:
            print(f"File Permission Error:")
            print(f"You have not enough permissions to open file: {self.filename}.")
            return
            
        except RuntimeError as e:
            print(f"Runtime Error:")
            print(f"The Python Library throws a Runtime Error on opening file: {self.filename}.")
            return
            
        except OSError as e:
            print(f"Operating System Error:")
            print(f"The System is not able to open file: {self.filename}.")
            return
            
        except Exception as e:
            print(f"Common Exception Error:")
            print(f"Common Exception throwed on open file: {self.filename}.")
            return
        return
    
    def load_mo(self, filename: str) -> gettext.GNUTranslations:
        with open(filename, "rb") as f:
            data = f.read()
        return gettext.GNUTranslations(fp = io.BytesIO(data))
    
    def _tr(self, msgid: str) -> str:
        try:
            return self._trres(msgid)
        except Exception:
            return msgid

# ---------------------------------------------------------------------------
# Global translation hook used by UI code: tr("File") -> "Datei" if de loaded
# ---------------------------------------------------------------------------
I18N = TranslationManager()

# ---- Standard-Locale beim Start setzen ----
def tr(msgid: str) -> str: return I18N._trres(msgid)
def LangSwitch(lang: str): return I18N._langSwitch(lang)


# ---------------------------------------------------------------------------
# we build our own argument parser exception ...
# ---------------------------------------------------------------------------
class ArgumentParserError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)

def ask_yes_no(question, default=False):
    while True:
        answer = input(question + " (y/N): ").strip().lower()
        
        if answer in ("j", "y", "ja", "yes"):
            return True
        
        if answer in ("n", "no", "nein"):
            return False
        
        if answer == "":
            return default
        
        print("Enter [Y]es or [N]o .")

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

def validate_output_path(value: str):
    if value == ".":
        if sys.platform.startswith("win"):
            value = os.getcwd() + "\\x64"
        elif sys.platform.startswith("linux"):
            value = os.getcwd() + "/x64"
    else:
        if sys.platform.startswith("win"):
            value += "\\x64"
        elif sys.platform.startswith("linux"):
            value += "/x64"
    
    output_dir = Path(value)
    output_dir.mkdir(parents=True, exist_ok=True)
        
    CDATA.CurrentWorkingDir = value
    CDATA.exe_file = value
    print(CDATA.CurrentWorkingDir)
    path = Path(value)
    #print(path)

    # Existierendes Verzeichnis
    if path.exists() and path.is_dir():
        if not path.drive and os.name == "nt":
            raise RuntimeError("no drive given.")

        if not path.exists():
            CDATA.LastErrorCode = LastError.DIRECTORY_DONT_EXISTS
            raise RuntimeError("directory does not exists.")

        if not os.access(path, os.R_OK):
            CDATA.LastErrorCode = LastError.DIRECTORY_NOT_READABLE
            raise RuntimeError("directory not readable.")

        if not os.access(path, os.W_OK):
            CDATA.LastErrorCode = LastError.DIRECTORY_NOT_WRITEABLE
            raise RuntimeError("directory not writeable.")

        #print(">>",path)
        return {
            "kind": "directory",
            "path": path
        }
    
    # Datei oder noch nicht existierende Datei
    parent = path.parent if path.parent != Path("") else Path(".")
    
    if not parent.exists():
        CDATA.LastErrorCode = LastError.DIRECTORY_DONT_EXISTS
        raise RuntimeError(f"target directory does not exists: {parent}")
    
    if not parent.is_dir():
        CDATA.LastErrorCode = LastError.PATH_NO_DIRECTORY
        raise RuntimeError(f"target path is not a directory: {parent}")
    
    if not os.access(parent, os.R_OK):
        CDATA.LastErrorCode = LastError.DIRECTORY_NOT_READABLE
        raise RuntimeError(f"target directory is not readable: {parent}")
    
    if not os.access(parent, os.W_OK):
        CDATA.LastErrorCode = LastError.DIRECTORY_NOT_WRITEABLE
        raise RuntimeError(f"target directory is not writeable: {parent}")
    
    if path.exists():
        if path.is_dir():
            CDATA.LastErrorCode = LastError.IS_DIRECTORY
            raise RuntimeError("target is a directory, not a file.")
        
        if not path.is_file():
            CDATA.LastErrorCode = LastError.NO_FILE_OR_DIRECTORY
            raise RuntimeError("target exists, but it is not a normal file.")
        
        if not ask_yes_no(f"file '{path}' already exists. Overwrite?"):
            CDATA.LastErrorCode = LastError.FILE_EXISTS
            raise RuntimeError("Canceled.")
        
        if not can_write_file(path):
            CDATA.LastErrorCode = LastError.FILE_LOCKED
            raise RuntimeError(
                f"File can not be overwrite. "
                f"The file is blocked by other Process: {path}"
            )
    
    return {
        "kind": "file",
        "path": path
    }

# ---------------------------------------------------------------------------
# console argument parser from overgiven application command arguments ...
# ---------------------------------------------------------------------------
def args_func():
    args_parser     = ThrowingArgumentParser(
        prog        = "pas2asmjit",
        description = "Pascal to AsmJit/NASM compiler"
    )
    
    args_parser.add_argument(
        "source",
        nargs   = "?",
        default = None,
        help    = "Pascal source file (.pas/.pp)"
    )
    
    args_parser.add_argument(
        "-o",
        "--output",
        default = None,
        help    = "Output directory"
    )
    
    # -------------------------------------------------------------
    # emitter for nasm compatible assembly code
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--asm",
        action  = "store_true",
        dest    = "asmoutput",
        help    = "Generate NASM compatible assembly output"
    )
    
    # -------------------------------------------------------------
    # emitter for AsmJIT C++ code ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--asmjit",
        action  = "store_true",
        dest    = "asmjitoutput",
        help    = "Generate AsmJIT C++ output"
    )
    
    # -------------------------------------------------------------
    # emitter for creating a Windows dll ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--dll",
        action  = "store_true",
        dest    = "dlloutputt",
        help    = "Build as DLL"
    )
    
    # -------------------------------------------------------------
    # emitter for creating a Windows exe ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--exe",
        action  = "store_true",
        dest    = "exeoutput",
        help    = "Build as EXE"
    )
    
    # -------------------------------------------------------------
    # --define=<macro>
    # Example: pas.exe -D DLL_API test.pas
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-D",
        "--define",
        dest    = "define",
        action  = "append",
        default = [],
        help    = "Define preprocessor symbol, e.g. -D DLL_API"
    )

    # -------------------------------------------------------------
    # -T<target>
    # Common Target OS identifiers
    # Example: pas.exe -T       win64 test.pas
    #          pas.exe --target win64 test.pas
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-T",
        "--target",
        dest    = "target",
        choices = [ "dos"       , # compile for MS-Dos 16-bit
                    "windows"   , # placeholder for win64
                    "win16"     , # compile for Windows 3.1 16-bit
                    "win32"     , # compile for Windows     32-bit
                    "win64"     , # compile for Windows     64-bit
        ],
        default = "win64",
        help    = "Target OS Platform"
    )
    
    # -------------------------------------------------------------
    # --fpcsignature=<str>
    # Beispiel: pas.exe --signature="MyApp 1.2.3 (build 4567)"
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--signature",
        default = "PAS 0.0.1 win64",
        dest    = "signature",
        help    = ("Replace the ident string in the .fpc_version section "
                   "of produced object.")
    )
    
    # -------------------------------------------------------------
    # --linkerversion=<Major.Minor>
    # Beispiel: pas.exe --linkerversion=8
    #
    # Name    | Major | Minor
    # --------|-------|-------
    # 95      |    4  |  0
    # 98      |    4  | 10
    # NE      |    4  | 90
    # 2000    |    5  |  0
    # XP      |    5  |  1
    # 2003    |    5  |  2
    # Vista   |    6  |  0
    # 7       |    6  |  1
    # 8       |    6  |  2
    # 8.1     |    6  |  3
    # 10 / 11 |   10  |  0
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--linkerversion",
        dest    = "linkerversion",
        help    = ("Sets the minimum OS version fields in the PE optional "
                   "header."),
        choices = [ "3"   , "3.1" , "3.11",
                    "4"   , "4.0" , "4.10", "4.90" ,
                    "5"   , "5.0" , "5.1" , "5.2"  ,
                    "6"   , "6.0" , "6.1" , "6.2"  , "6.3",
                    "7"   ,
                    "8"   , "8.1" ,
                    "10"  , "10.0",
                    "11"  ,
                    "95"  ,
                    "98"  , "ME"  ,
                    "2000", "XP"  ,
                    "2003", "Vista"
        ],
        default = "10"
    )
    
    # -------------------------------------------------------------
    # emitter backend ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "--backend",
        dest     = "backend",
        choices  = ["c++", "asmjit",
                    "asm", "nasm",
                    "obj", "objfile",
                    "exe", "exefile",
        ],
        default  = "asmjit",
        help     = "Code backend: asmjit, nasm, objfile."
    )
    
    # -------------------------------------------------------------
    # modules include path
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-Fi",
        dest    = "includepath",
        action  = "append",
        default = [],
        help    = "Add include file search path."
    )
    
    # -------------------------------------------------------------
    # executable output path ...
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-FE",
        dest    = "exe_output_dir",
        default = ".",
        help    = "Set output directory for executables."
    )
    
    # -------------------------------------------------------------
    # --info V  -> informations about the compiler
    # Example: pas.exe --info V
    # -------------------------------------------------------------
    args_parser.add_argument(
        "-i",
        "--info",
        dest    =   "information",
        nargs   =   "?",
        const   =   "",
        choices = [ "",
                    "V",    # version information's
                    "W",
                    "TP"
        ],
        default = None,
        help    = "Help informations about the compiler"
    )
    return args_parser

def handle_args(args):
    if args.exe_output_dir is not None:
        CDATA.ExeOutputDir = args.exe_output_dir
        #print("==> ", CDATA.CurrentWorkingDir)

    result = validate_output_path(args.exe_output_dir)
    if result["kind"] == "directory":
        return args
    if result["kind"] == "file":
        CDATA.LastErrorCode = LastError.NO_DIRECTORY
        raise Exception("executable output is not a directory or does not exists.")
            
    if args.info is not None:
        if args.info == "":
            print("Common Info")
        elif args.info == "V":
            print("Version")
        elif args.info == "W":
            print("Warning")
        elif args.info == "TP":
            print("Target platform")
    
    return args

# ---------------------------------------------------------------------------
# Compiler Exception to mark errors in compilation unit ...
# ---------------------------------------------------------------------------
class CompileError(Exception):
    def __init__(self, ctx, code, **params):
        token       = ctx.start if hasattr(ctx, "start") else ctx
        
        self.line   = token.line
        self.column = token.column
        self.code   = code
        self.params = params
        
        super().__init__(code)

# ---------------------------------------------------------------------------
# currently, we support:
# - asmjit for GNU C++ compatible Code
# - nasm   for NASM Assembly Code
# ---------------------------------------------------------------------------
def double_to_bits(value):
    return struct.unpack(
        "<Q",
        struct.pack("<d", float(value))
    )[0]

class CodeBackend:
    def __init__(self, name: str = "asmjit"):
        self.lines = []
        self.name = name
        CDATA.BackEnd.current = name
    
    def emit(self, line):
        self.lines.append("    " + line)
    
    def get_lines(self):
        return self.lines
    
    def emit_new_label_decl(self, name, comment=""): raise NotImplementedError
    
    def emit_add(self, reg, value, comment=""): raise NotImplementedError
    def emit_imul(self, dst, src, value=None, comment=""): raise NotImplementedError
    def emit_cmp(self, dst, value, comment=""): raise NotImplementedError
    def emit_cmp_dword(self, dst, base, field, comment=""): raise NotImplementedError

    def emit_jl(self, label, comment=""): raise NotImplementedError
    def emut_jl(self, label, comment=""): return self.emit_jl(label, comment)
    def emit_jg(self, label, comment=""): raise NotImplementedError
    def emit_jz(self, label, comment=""): raise NotImplementedError
    def emit_jb(self, label, comment=""): raise NotImplementedError
    def emit_ja(self, label, comment=""): raise NotImplementedError
    def emit_jae(self, label, comment=""): raise NotImplementedError
    def emit_jbe(self, label, comment=""): raise NotImplementedError
    def emit_je(self, label, comment=""): raise NotImplementedError
    def emit_jle(self, label, comment=""): raise NotImplementedError
    def emit_jge(self, label, comment=""): raise NotImplementedError
    def emit_jne(self, label, comment=""): raise NotImplementedError
    def emit_jnz(self, label, comment=""): raise NotImplementedError
    def emit_jmp(self, label, comment=""): raise NotImplementedError

    def emit_lea_byte(self, dst, base, offset, comment=""): raise NotImplementedError
    def emit_lea_dword(self, dst, base, offset, comment=""): raise NotImplementedError
    def emit_lea_qword(self, dst, base, offset, comment=""): raise NotImplementedError

    def emit_mov_byte(self, dst, base, field, comment=""): raise NotImplementedError
    def emit_mov_dword(self, dst, base, field, comment=""): raise NotImplementedError
    def emit_mov_qword(self, dst, base, field, comment=""): raise NotImplementedError

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""): raise NotImplementedError
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""): raise NotImplementedError
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""): raise NotImplementedError

    def emit_mov_reg_byte(self, dst, base, comment=""): raise NotImplementedError
    def emit_mov_reg_dword(self, dst, base, comment=""): raise NotImplementedError
    def emit_mov_reg_qword(self, dst, base, comment=""): raise NotImplementedError

    def emit_mov_imm(self, dst, value, comment=""): raise NotImplementedError
    def emit_mov(self, dst, src, comment=""): raise NotImplementedError
    def emit_movzx(self, dst, src, comment=""): raise NotImplementedError
    def emit_movsxd(self, dst, src, comment=""): raise NotImplementedError
    def emit_movq(self, dst, src, comment=""): raise NotImplementedError
    def emit_movsd_load(self, dst, base, offset=0, comment=""): raise NotImplementedError
    def emit_movsd_load_field(self, dst, base, field, comment=""): raise NotImplementedError
    def emit_movsd_store(self, base, offset, src, comment=""): raise NotImplementedError
    def emit_ucomisd(self, dst, src, comment=""): raise NotImplementedError
    def emit_cvtsi2sd(self, dst, src, comment=""): raise NotImplementedError
    def emit_movapd(self, dst, src, comment=""): raise NotImplementedError
    def emit_addsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_subsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_mulsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_divsd(self, dst, src, comment=""): raise NotImplementedError
    def emit_cdq(self, comment=""): raise NotImplementedError
    def emit_idiv(self, reg, comment=""): raise NotImplementedError

    def emit_xor(self, dst, src, comment=""): raise NotImplementedError
    def emit_push(self, reg, comment=""): raise NotImplementedError
    def emit_pop(self, reg, comment=""): raise NotImplementedError
    def emit_sub(self, reg, value, comment=""): raise NotImplementedError
    def emit_setne(self, reg, comment=""): raise NotImplementedError
    def emit_test(self, reg1, reg2, comment=""): raise NotImplementedError

    def emit_call(self, target, comment=""): raise NotImplementedError
    def emit_call_reg(self, target, comment=""): return self.emit_call(target, comment)
    def emit_call_lbl(self, target, comment=""): raise NotImplementedError
    def emit_ret(self, comment=""): raise NotImplementedError
    def emit_bind_label(self, label, comment=""): raise NotImplementedError


# ---------------------------------------------------------------------------
# AsmJit backend ...
# ---------------------------------------------------------------------------
class AsmJitBackend(CodeBackend):
    def __init__(self, name="asmjit"):
        super().__init__(name)

    def make_comment(self, comment):
        return f"  // {comment}" if comment else ""

    def emit_new_label_decl(self, name, comment=""):
        self.emit(
            f"Label {name} = a.new_label();{self.make_comment(comment)}"
        )
    
    def _imm(self, value):
        s = str(value)
        if s.startswith("imm("):
            return s
        if s.startswith("&"):
            return f"imm((uint64_t){s})"
        if s.startswith("_") or s.startswith("str_") or s.startswith("dbl_"):
            return f"imm((uint64_t)&{s})"
        return s

    def _operand(self, value):
        if isinstance(value, str) and value.isidentifier():
            return f"x86::{value}"
        return str(value)

    def emit_add(self, reg, value, comment=""):
        self.emit(f"a.add(x86::{reg}, {self._operand(value)});{self.make_comment(comment)}")

    def emit_imul(self, dst, src, value=None, comment=""):
        if value is None:
            self.emit(f"a.imul(x86::{dst}, {self._operand(src)});{self.make_comment(comment)}")
        else:
            self.emit(f"a.imul(x86::{dst}, {self._operand(src)}, {value});{self.make_comment(comment)}")

    def emit_cmp(self, dst, value, comment=""):
        if isinstance(value, str) and value.isidentifier():
            self.emit(f"a.cmp(x86::{dst}, x86::{value});{self.make_comment(comment)}")
        else:
            self.emit(f"a.cmp(x86::{dst}, {value});{self.make_comment(comment)}")
    def emit_cmp_dword(self, dst, base, field, comment=""):
        self.emit(f"a.cmp(x86::{dst}, x86::dword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")

    def emit_jl(self, label, comment=""): self.emit(f"a.jl({label});{self.make_comment(comment)}")
    def emit_jg(self, label, comment=""): self.emit(f"a.jg({label});{self.make_comment(comment)}")
    def emit_jz(self, label, comment=""): self.emit(f"a.jz({label});{self.make_comment(comment)}")
    def emit_jb(self, label, comment=""): self.emit(f"a.jb({label});{self.make_comment(comment)}")
    def emit_ja(self, label, comment=""): self.emit(f"a.ja({label});{self.make_comment(comment)}")
    def emit_jae(self, label, comment=""): self.emit(f"a.jae({label});{self.make_comment(comment)}")
    def emit_jbe(self, label, comment=""): self.emit(f"a.jbe({label});{self.make_comment(comment)}")
    def emit_je(self, label, comment=""): self.emit(f"a.je({label});{self.make_comment(comment)}")
    def emit_jle(self, label, comment=""): self.emit(f"a.jle({label});{self.make_comment(comment)}")
    def emit_jge(self, label, comment=""): self.emit(f"a.jge({label});{self.make_comment(comment)}")
    def emit_jne(self, label, comment=""): self.emit(f"a.jne({label});{self.make_comment(comment)}")
    def emit_jnz(self, label, comment=""): self.emit(f"a.jnz({label});{self.make_comment(comment)}")
    def emit_jmp(self, label, comment=""): self.emit(f"a.jmp({label});{self.make_comment(comment)}")

    def emit_lea_byte(self, dst, base, offset, comment=""):
        self.emit(f"a.lea(x86::{dst}, x86::byte_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_lea_dword(self, dst, base, offset, comment=""):
        self.emit(f"a.lea(x86::{dst}, x86::dword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_lea_qword(self, dst, base, offset, comment=""):
        self.emit(f"a.lea(x86::{dst}, x86::qword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")

    def emit_mov_byte(self, dst, base, field, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::byte_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")
    def emit_mov_dword(self, dst, base, field, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::dword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")
    def emit_mov_qword(self, dst, base, field, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::qword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::byte_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::dword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::qword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"a.mov(x86::qword_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"a.mov(x86::dword_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"a.mov(x86::byte_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")

    def emit_mov_reg_byte(self, dst, base, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::byte_ptr(x86::{base}));{self.make_comment(comment)}")
    def emit_mov_reg_dword(self, dst, base, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::dword_ptr(x86::{base}));{self.make_comment(comment)}")
    def emit_mov_reg_qword(self, dst, base, comment=""):
        self.emit(f"a.mov(x86::{dst}, x86::qword_ptr(x86::{base}));{self.make_comment(comment)}")

    def emit_mov_imm(self, dst, value, comment=""):
        self.emit(f"a.mov(x86::{dst}, {self._imm(value)});{self.make_comment(comment)}")

    def emit_mov(self, dst, src, comment=""):
        if isinstance(src, int) or (isinstance(src, str) and (src.lstrip('-').isdigit() or src.startswith('&') or src.startswith('imm('))):
            self.emit_mov_imm(dst, src, comment)
        else:
            self.emit(f"a.mov(x86::{dst}, x86::{src});{self.make_comment(comment)}")

    def emit_movzx(self, dst, src, comment=""):
        s = str(src)
        if s.startswith("byte_ptr(") and s.endswith(")"):
            base = s[len("byte_ptr("):-1]
            self.emit(f"a.movzx(x86::{dst}, x86::byte_ptr(x86::{base}));{self.make_comment(comment)}")
        else:
            self.emit(f"a.movzx(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movsxd(self, dst, src, comment=""):
        self.emit(f"a.movsxd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movq(self, dst, src, comment=""):
        self.emit(f"a.movq(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movsd_load(self, dst, base, offset=0, comment=""):
        self.emit(f"a.movsd(x86::{dst}, x86::qword_ptr(x86::{base}, {offset}));{self.make_comment(comment)}")
    def emit_movsd_load_field(self, dst, base, field, comment=""):
        self.emit(f"a.movsd(x86::{dst}, x86::qword_ptr(x86::{base}, offsetof(JitContext, {field})));{self.make_comment(comment)}")
    def emit_movsd_store(self, base, offset, src, comment=""):
        self.emit(f"a.movsd(x86::qword_ptr(x86::{base}, {offset}), x86::{src});{self.make_comment(comment)}")
    def emit_ucomisd(self, dst, src, comment=""):
        self.emit(f"a.ucomisd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_cvtsi2sd(self, dst, src, comment=""):
        self.emit(f"a.cvtsi2sd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_movapd(self, dst, src, comment=""):
        self.emit(f"a.movapd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_addsd(self, dst, src, comment=""):
        self.emit(f"a.addsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_subsd(self, dst, src, comment=""):
        self.emit(f"a.subsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_mulsd(self, dst, src, comment=""):
        self.emit(f"a.mulsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_divsd(self, dst, src, comment=""):
        self.emit(f"a.divsd(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_cdq(self, comment=""):
        self.emit(f"a.cdq();{self.make_comment(comment)}")
    def emit_idiv(self, reg, comment=""):
        self.emit(f"a.idiv(x86::{reg});{self.make_comment(comment)}")

    def emit_xor(self, dst, src, comment=""):
        self.emit(f"a.xor_(x86::{dst}, x86::{src});{self.make_comment(comment)}")
    def emit_push(self, reg, comment=""):
        self.emit(f"a.push(x86::{reg});{self.make_comment(comment)}")
    def emit_pop(self, reg, comment=""):
        self.emit(f"a.pop(x86::{reg});{self.make_comment(comment)}")
    def emit_sub(self, reg, value, comment=""):
        self.emit(f"a.sub(x86::{reg}, {value});{self.make_comment(comment)}")
    def emit_setne(self, reg, comment=""):
        self.emit(f"a.setne(x86::{reg});{self.make_comment(comment)}")
    def emit_test(self, reg1, reg2, comment=""):
        self.emit(f"a.test(x86::{reg1}, x86::{reg2});{self.make_comment(comment)}")

    def emit_call(self, target, comment=""):
        self.emit_sub("rsp", 32, comment="Windows x64 shadow space")
        self.emit(f"a.call(x86::{target});{self.make_comment(comment)}")
        self.emit_add("rsp", 32)
    def emit_call_reg(self, target, comment=""):
        self.emit_call(target, comment)
    def emit_call_lbl(self, target, comment=""):
        self.emit_sub("rsp", 32, comment="Windows x64 shadow space")
        self.emit(f"a.call({target});{self.make_comment(comment)}")
        self.emit_add("rsp", 32)
    def emit_ret(self, comment=""):
        self.emit(f"a.ret();{self.make_comment(comment)}")
    def emit_bind_label(self, label, comment=""):
        self.emit(f"a.bind({label});{self.make_comment(comment)}")


# ---------------------------------------------------------------------------
# NASM backend ...
# ---------------------------------------------------------------------------
class NasmBackend(CodeBackend):
    def __init__(self, name: str = "nasm"):
        super().__init__(name)

    def make_comment(self, comment):
        return f"  ; {comment}" if comment else ""

    def emit_new_label_decl(self, name, comment=""):
        # NASM braucht keine vorherige Label-Deklaration
        return
    
    def _mem(self, base, offset=0):
        if offset in (None, "", 0, "0"):
            return f"[{base}]"
        off = str(offset)
        if off.startswith("-"):
            return f"[{base} - {off[1:]}]"
        return f"[{base} + {off}]"

    def _symbol(self, value):
        s = str(value)
        if s.startswith("&"):
            return s[1:]
        if s.startswith("imm((uint64_t)&") and s.endswith(")"):
            return s[len("imm((uint64_t)&"):-1]
        return s

    def emit_add(self, reg, value, comment=""):
        self.emit(f"add {reg}, {value}{self.make_comment(comment)}")
    def emit_imul(self, dst, src, value=None, comment=""):
        if value is None:
            self.emit(f"imul {dst}, {src}{self.make_comment(comment)}")
        else:
            self.emit(f"imul {dst}, {src}, {value}{self.make_comment(comment)}")
    def emit_cmp(self, dst, value, comment=""):
        self.emit(f"cmp {dst}, {value}{self.make_comment(comment)}")
    def emit_cmp_dword(self, dst, base, field, comment=""):
        self.emit(f"cmp {dst}, dword [{base} + JitContext.{field}]{self.make_comment(comment)}")

    def emit_jl(self, label, comment=""): self.emit(f"jl {label}{self.make_comment(comment)}")
    def emit_jg(self, label, comment=""): self.emit(f"jg {label}{self.make_comment(comment)}")
    def emit_jz(self, label, comment=""): self.emit(f"jz {label}{self.make_comment(comment)}")
    def emit_jb(self, label, comment=""): self.emit(f"jb {label}{self.make_comment(comment)}")
    def emit_ja(self, label, comment=""): self.emit(f"ja {label}{self.make_comment(comment)}")
    def emit_jae(self, label, comment=""): self.emit(f"jae {label}{self.make_comment(comment)}")
    def emit_jbe(self, label, comment=""): self.emit(f"jbe {label}{self.make_comment(comment)}")
    def emit_je(self, label, comment=""): self.emit(f"je {label}{self.make_comment(comment)}")
    def emit_jle(self, label, comment=""): self.emit(f"jle {label}{self.make_comment(comment)}")
    def emit_jge(self, label, comment=""): self.emit(f"jge {label}{self.make_comment(comment)}")
    def emit_jne(self, label, comment=""): self.emit(f"jne {label}{self.make_comment(comment)}")
    def emit_jnz(self, label, comment=""): self.emit(f"jnz {label}{self.make_comment(comment)}")
    def emit_jmp(self, label, comment=""): self.emit(f"jmp {label}{self.make_comment(comment)}")

    def emit_lea_byte(self, dst, base, offset, comment=""):
        self.emit(f"lea {dst}, {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_lea_dword(self, dst, base, offset, comment=""):
        self.emit(f"lea {dst}, {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_lea_qword(self, dst, base, offset, comment=""):
        self.emit(f"lea {dst}, {self._mem(base, offset)}{self.make_comment(comment)}")

    def emit_mov_byte(self, dst, base, field, comment=""):
        self.emit(f"mov {dst}, byte [{base} + JitContext.{field}]{self.make_comment(comment)}")
    def emit_mov_dword(self, dst, base, field, comment=""):
        self.emit(f"mov {dst}, dword [{base} + JitContext.{field}]{self.make_comment(comment)}")
    def emit_mov_qword(self, dst, base, field, comment=""):
        self.emit(f"mov {dst}, qword [{base} + JitContext.{field}]{self.make_comment(comment)}")

    def emit_mov_byte_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"mov {dst}, byte {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"mov {dst}, dword {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""):
        self.emit(f"mov {dst}, qword {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"mov qword {self._mem(base, offset)}, {src}{self.make_comment(comment)}")
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"mov dword {self._mem(base, offset)}, {src}{self.make_comment(comment)}")
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""):
        self.emit(f"mov byte {self._mem(base, offset)}, {src}{self.make_comment(comment)}")

    def emit_mov_reg_byte(self, dst, base, comment=""):
        self.emit(f"mov {dst}, byte [{base}]{self.make_comment(comment)}")
    def emit_mov_reg_dword(self, dst, base, comment=""):
        self.emit(f"mov {dst}, dword [{base}]{self.make_comment(comment)}")
    def emit_mov_reg_qword(self, dst, base, comment=""):
        self.emit(f"mov {dst}, qword [{base}]{self.make_comment(comment)}")

    def emit_mov(self, dst, src, comment=""):
        self.emit(f"mov {dst}, {src}{self.make_comment(comment)}")
    def emit_mov_imm(self, dst, value, comment=""):
        self.emit(f"mov {dst}, {self._symbol(value)}{self.make_comment(comment)}")
    def emit_movzx(self, dst, src, comment=""):
        s = str(src)
        if s.startswith("byte_ptr(") and s.endswith(")"):
            base = s[len("byte_ptr("):-1]
            self.emit(f"movzx {dst}, byte [{base}]{self.make_comment(comment)}")
        else:
            self.emit(f"movzx {dst}, {src}{self.make_comment(comment)}")
    def emit_movsxd(self, dst, src, comment=""):
        self.emit(f"movsxd {dst}, {src}{self.make_comment(comment)}")
    def emit_movq(self, dst, src, comment=""):
        self.emit(f"movq {dst}, {src}{self.make_comment(comment)}")
    def emit_movsd_load(self, dst, base, offset=0, comment=""):
        self.emit(f"movsd {dst}, qword {self._mem(base, offset)}{self.make_comment(comment)}")
    def emit_movsd_load_field(self, dst, base, field, comment=""):
        self.emit(f"movsd {dst}, qword [{base} + JitContext.{field}]{self.make_comment(comment)}")
    def emit_movsd_store(self, base, offset, src, comment=""):
        self.emit(f"movsd qword {self._mem(base, offset)}, {src}{self.make_comment(comment)}")
    def emit_ucomisd(self, dst, src, comment=""):
        self.emit(f"ucomisd {dst}, {src}{self.make_comment(comment)}")
    def emit_cvtsi2sd(self, dst, src, comment=""):
        self.emit(f"cvtsi2sd {dst}, {src}{self.make_comment(comment)}")
    def emit_movapd(self, dst, src, comment=""):
        self.emit(f"movapd {dst}, {src}{self.make_comment(comment)}")
    def emit_addsd(self, dst, src, comment=""):
        self.emit(f"addsd {dst}, {src}{self.make_comment(comment)}")
    def emit_subsd(self, dst, src, comment=""):
        self.emit(f"subsd {dst}, {src}{self.make_comment(comment)}")
    def emit_mulsd(self, dst, src, comment=""):
        self.emit(f"mulsd {dst}, {src}{self.make_comment(comment)}")
    def emit_divsd(self, dst, src, comment=""):
        self.emit(f"divsd {dst}, {src}{self.make_comment(comment)}")
    def emit_cdq(self, comment=""):
        self.emit(f"cdq{self.make_comment(comment)}")
    def emit_idiv(self, reg, comment=""):
        self.emit(f"idiv {reg}{self.make_comment(comment)}")

    def emit_xor(self, dst, src, comment=""):
        self.emit(f"xor {dst}, {src}{self.make_comment(comment)}")
    def emit_push(self, reg, comment=""):
        self.emit(f"push {reg}{self.make_comment(comment)}")
    def emit_pop(self, reg, comment=""):
        self.emit(f"pop {reg}{self.make_comment(comment)}")
    def emit_sub(self, reg, value, comment=""):
        self.emit(f"sub {reg}, {value}{self.make_comment(comment)}")
    def emit_setne(self, reg, comment=""):
        self.emit(f"setne {reg}{self.make_comment(comment)}")
    def emit_test(self, reg1, reg2, comment=""):
        self.emit(f"test {reg1}, {reg2}{self.make_comment(comment)}")

    def emit_call(self, target, comment=""):
        self.emit_sub("rsp", 32, comment="Windows x64 shadow space")
        self.emit(f"call {target}{self.make_comment(comment)}")
        self.emit_add("rsp", 32)
    def emit_call_reg(self, target, comment=""):
        self.emit_call(target, comment)
    def emit_call_lbl(self, target, comment=""):
        self.emit_call(target, comment)
    def emit_ret(self, comment=""):
        self.emit(f"ret{self.make_comment(comment)}")
    def emit_bind_label(self, label, comment=""):
        self.lines.append(f"{label}:{self.make_comment(comment)}")

# ---------------------------------------------------------------------------
# win64 pe coff writer ...
# ---------------------------------------------------------------------------
class PECoffWriter:
    def __init__(self):
        self.regs = {
            "al"  :  0, "cl"  :  1, "dl"  :  2, "bl"  :  3,
            "spl" :  4, "bpl" :  5, "sil" :  6, "dil" :  7,
            "r8b" :  8, "r9b" :  9, "r10b": 10, "r11b": 11,
            "r12b": 12, "r13b": 13, "r14b": 14, "r15b": 15,

            "rax" :  0, "rcx" :  1, "rdx" :  2, "rbx" :  3,
            "rsp" :  4, "rbp" :  5, "rsi" :  6, "rdi" :  7,
            "r8"  :  8, "r9"  :  9, "r10" : 10, "r11" : 11,
            "r12" : 12, "r13" : 13, "r14" : 14, "r15" : 15,
            
            "eax" :  0, "ecx" :  1, "edx" :  2, "ebx" :  3,
            "esp" :  4, "ebp" :  5, "esi" :  6, "edi" :  7,
            "r8d" :  8, "r9d" :  9, "r10d": 10, "r11d": 11,
            "r12d": 12, "r13d": 13, "r14d": 14, "r15d": 15,
        }
        
        self.text               = bytearray()
        self.data               = bytearray()
        
        self.text_relocations   = []
        self.data_relocations   = []

        self.symbols            = []
        self.labels             = {}
        self.fixups             = []
        
        self.string_table       = bytearray()
        self.string_offsets     = {}
    
    def begin_function(self, name, local_size=0, public=True):
        offset = len(self.text)
        self.bind_label(name)
        self.add_symbol(
            name            = name,
            value           = offset,
            section_number  = 1
        )
        self.emit_function_prolog(local_size)
        return offset

    def end_function(self):
        self.emit_function_epilog()
        
    def align_data(self, alignment):
        while len(self.data) % alignment != 0:
            self.data.append(0)

    def add_data_i32(self, name, value=0):
        return self.add_data_bytes(name,
            int(value).to_bytes(4, "little", signed=True),
            alignment = 4
        )

    def add_data_qword(self, name, value=0):
        return self.add_data_bytes(name,
            int(value).to_bytes(8, "little", signed=False),
            alignment = 8
        )

    def add_data_double(self, name, value=0.0):
        bits = double_to_bits(value)
        return self.add_data_bytes(name,
            int(bits).to_bytes(8, "little", signed=False),
            alignment = 8
        )

    def add_data_bytes(self, name, data_bytes, alignment=1):
        self.align_data(alignment)

        offset = len(self.data)
        self.data += data_bytes

        self.add_symbol(
            name=name,
            value=offset,
            section_number = 2
        )
        return offset

    def add_data_zeros(self, name, size, alignment=8):
        return self.add_data_bytes(name,
            b"\x00" * size,
            alignment
        )
    
    def add_data_qword_symbol_ref(self, target_symbol):
        sym_index   = self.find_or_add_symbol(target_symbol)
        offset      = len(self.data)
        self.data  += b"\x00" * 8

        self.data_relocations.append({
            "offset": offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_ADDR64
        })
        return offset
        
    def add_data_i32_array   (self, name, count): return self.add_data_zeros(name, count * 4, alignment=4)
    def add_data_qword_array (self, name, count): return self.add_data_zeros(name, count * 8, alignment=8)
    def add_data_double_array(self, name, count): return self.add_data_zeros(name, count * 8, alignment=8)
    
    def add_jit_context( self,
        name          = "ctx",
        int_count     =   256,
        double_count  =   256,
        string_count  =   256,
        record_bytes  =  4096,
        arrays_bytes  =  4096,
        pointer_count =   256):
        
        self.add_data_i32_array     ("int_vars"   , int_count)
        self.add_data_double_array  ("double_vars", double_count)
        self.add_data_qword_array   ("string_vars", string_count)
        self.add_data_zeros         ("record_vars", record_bytes, alignment = 8)
        self.add_data_zeros         ("arrays_vars", arrays_bytes, alignment = 8)
        self.add_data_qword_array   ("pointr_vars", pointer_count)

        self.align_data(8)
        ctx_offset = len(self.data)

        self.add_symbol(
            name           = name,
            value          = ctx_offset,
            section_number = 2
        )

        self.add_data_qword_symbol_ref("int_vars")
        self.add_data_qword_symbol_ref("double_vars")
        self.add_data_qword_symbol_ref("string_vars")
        self.add_data_qword_symbol_ref("record_vars")
        self.add_data_qword_symbol_ref("arrays_vars")
        self.add_data_qword_symbol_ref("pointr_vars")

        self.data += b"\x00" * 4   # print_int_tmp
        self.data += b"\x00" * 4   # padding
        self.data += b"\x00" * 8   # print_double_tmp

        return ctx_offset
    
    def add_data_i32(self, name, value = 0):
        return self.add_data_bytes(name,
            int(value).to_bytes(4, "little", signed = True),
            alignment=4
        )

    def add_data_qword(self, name, value = 0):
        return self.add_data_bytes(name,
            int(value).to_bytes(8, "little", signed = False),
            alignment=8
        )
    
    def _is_ext_reg(self, reg): return self._reg_id(reg) >= 8
    def _reg_low3  (self, reg): return self._reg_id(reg)  & 7
    
    def _reg_id(self, reg):
        if reg not in self.regs:
            raise RuntimeError(f"unsupported register: {reg}")
        return self.regs[reg]
    
    def _xmm_id(self, reg):
        if not isinstance(reg, str):
            raise RuntimeError(f"unsupported xmm register: {reg}")

        reg = reg.lower()

        if not reg.startswith("xmm"):
            raise RuntimeError(f"unsupported xmm register: {reg}")
        try:
            n = int(reg[3:])
        except ValueError:
            raise RuntimeError(f"unsupported xmm register: {reg}")

        if n < 0 or n > 15:
            raise RuntimeError(f"unsupported xmm register: {reg}")

        return n
    
    def _emit_rex_xmm_mem(self, xmm_id, base):
        base_id = self._reg_id(base)

        rex = 0x48
        if xmm_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        self.text.append(rex)

    def emit_mov_r32_data_label(self, dst, label):
        dst_id    = self._reg_id(dst)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text.append(0x8B)  # mov r32, r/m32

        # RIP-relative: mod=00, reg=dst, rm=101
        self.text.append(0x05 | ((dst_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset"        : reloc_offset,
            "symbol_index"  : sym_index,
            "type"          : IMAGE_REL_AMD64_REL32
        })

    def emit_mov_data_label_r32(self, label, src):
        src_id    = self._reg_id(src)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x40
        if src_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text.append(0x89)  # mov r/m32, r32

        # RIP-relative: mod=00, reg=src, rm=101
        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset"        : reloc_offset,
            "symbol_index"  : sym_index,
            "type"          : IMAGE_REL_AMD64_REL32
        })

    def emit_mov_r64_data_label(self, dst, label):
        dst_id = self._reg_id(dst)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x48
        if dst_id >= 8:
            rex |= 0x04

        self.text.append(rex)
        self.text.append(0x8B)

        self.text.append(0x05 | ((dst_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })

    def emit_mov_data_label_r64(self, label, src):
        src_id = self._reg_id(src)
        sym_index = self.find_or_add_symbol(label)

        rex = 0x48
        if src_id >= 8:
            rex |= 0x04

        self.text.append(rex)
        self.text.append(0x89)

        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })
    
    def emit_movsd_data_label(self, dst, label):
        dst_id = self._xmm_id(dst)
        sym_index = self.find_or_add_symbol(label)

        self.text += b"\xF2"

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text += b"\x0F\x10"
        self.text.append(0x05 | ((dst_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })

    def emit_movsd_data_label_store(self, label, src):
        src_id = self._xmm_id(src)
        sym_index = self.find_or_add_symbol(label)

        self.text += b"\xF2"

        rex = 0x40
        if src_id >= 8: rex |= 0x04
        if rex != 0x40: self.text.append(rex)

        self.text += b"\x0F\x11"
        self.text.append(0x05 | ((src_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })
    
    ##
    def emit_movsd_load(self, dst, base, offset=0):
        dst_id = self._xmm_id(dst)

        self.text += b"\xF2"
        self._emit_rex_xmm_mem(dst_id, base)
        self.text += b"\x0F\x10"

        self._emit_modrm_mem(dst_id, base, offset)

    def emit_movsd_store(self, base, offset, src):
        src_id = self._xmm_id(src)

        self.text += b"\xF2"
        self._emit_rex_xmm_mem(src_id, base)
        self.text += b"\x0F\x11"

        self._emit_modrm_mem(src_id, base, offset)
    
    def _emit_modrm_mem(self, reg_id, base, offset=0):
        base_id = self._reg_id(base)

        reg = reg_id  & 7
        rm  = base_id & 7

        needs_sib  = rm == 4          # rsp / r12
        needs_disp = base in ("rbp", "r13") and offset == 0

        if offset == 0 and not needs_disp: mod = 0x00
        elif -128 <= offset <= 127:        mod = 0x40
        else:                              mod = 0x80

        if needs_disp:
            mod = 0x40
            offset = 0

        if needs_sib:
            self.text.append(mod | (reg << 3) | 0x04)

            # SIB: scale=0, index=none(4), base=rm
            self.text.append(0x20 | rm)
        else:
            self.text.append(mod | (reg << 3) | rm)

        if mod == 0x40:
            self.text.append(offset & 0xFF)
        elif mod == 0x80:
            self.text += int(offset).to_bytes(4, "little", signed=True)

    def _emit_xmm_xmm(self, prefix, opcode, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._xmm_id(src)

        if prefix is not None:
            self.text.append(prefix)

        rex = 0x40
        if dst_id >= 8:
            rex |= 0x04
        if src_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text += b"\x0F"
        self.text.append(opcode)
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_addsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x58, dst, src)
    def emit_subsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x5C, dst, src)
    def emit_mulsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x59, dst, src)
    def emit_divsd(self, dst, src): self._emit_xmm_xmm(0xF2, 0x5E, dst, src)

    def emit_ucomisd(self, left, right):
        self._emit_xmm_xmm(0x66, 0x2E, left, right)

    def emit_cvtsi2sd(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._reg_id(src)
        
        self.text += b"\xF2"
        
        rex = 0x48
        if dst_id >= 8: rex |= 0x04
        if src_id >= 8: rex |= 0x01
        
        self.text.append(rex)
        self.text += b"\x0F\x2A"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_sub_r64_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x48
        if reg_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x81)
        self.text.append(0xE8 | (reg_id & 7))  # /5 SUB
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_add_r64_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x48
        if reg_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x81)
        self.text.append(0xC0 | (reg_id & 7))  # /0 ADD
        self.text += int(value).to_bytes(4, "little", signed=True)
        
    # --------------------------------
    # Label definieren
    # --------------------------------
    def bind_label(self, name):
        self.labels[name] = len(self.text)

        pending = [
            f for f in self.fixups
            if f["label"] == name
        ]

        for fix in pending:
            self.patch_rel32(
                fix["patch_pos"],
                self.labels[name]
            )

        self.fixups = [
            f for f in self.fixups
            if f["label"] != name
        ]
    
    # --------------------------------
    # add r32, r32
    # --------------------------------
    def emit_add_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40

        if src_id >= 8:
            rex |= 0x04  # REX.R

        if dst_id >= 8:
            rex |= 0x01  # REX.B

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x01)  # add r/m32, r32
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # and r32, r32
    # --------------------------------
    def emit_and_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        if src_id >= 8 or dst_id >= 8:
            rex = 0x40
            if src_id >= 8:
                rex |= 0x04
            if dst_id >= 8:
                rex |= 0x01
            self.text.append(rex)

        self.text.append(0x21)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    def emit_add_r32_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x40
        if reg_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x81)
        self.text.append(0xC0 | (reg_id & 7))  # /0 ADD
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_sub_r32_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        rex = 0x40
        if reg_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x81)
        self.text.append(0xE8 | (reg_id & 7))  # /5 SUB
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_add_r32_imm(self, reg, value): self.emit_add_r32_imm32(reg, value)
    def emit_sub_r32_imm(self, reg, value): self.emit_sub_r32_imm32(reg, value)
    
    def emit_add_r64_r64(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x48
        if src_id >= 8:
            rex |= 0x04
        if dst_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x01)  # add r/m64, r64
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))

    def emit_sub_r64_r64(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x48
        if src_id >= 8:
            rex |= 0x04
        if dst_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x29)  # sub r/m64, r64
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # or r32, r32
    # --------------------------------
    def emit_or_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        if src_id >= 8 or dst_id >= 8:
            rex = 0x40
            if src_id >= 8:
                rex |= 0x04
            if dst_id >= 8:
                rex |= 0x01
            self.text.append(rex)

        self.text.append(0x09)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # xor r32, r32
    # --------------------------------
    def emit_xor_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        if src_id >= 8 or dst_id >= 8:
            rex = 0x40
            if src_id >= 8:
                rex |= 0x04
            if dst_id >= 8:
                rex |= 0x01
            self.text.append(rex)

        self.text.append(0x31)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
        
    # --------------------------------
    # sub r32, r32
    # --------------------------------
    def emit_sub_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40

        if src_id >= 8:
            rex |= 0x04

        if dst_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x29)  # sub r/m32, r32
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    # --------------------------------
    # imul r32, r32
    # --------------------------------
    def emit_imul_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40

        if dst_id >= 8:
            rex |= 0x04  # REX.R

        if src_id >= 8:
            rex |= 0x01  # REX.B

        if rex != 0x40:
            self.text.append(rex)

        self.text += b"\x0F\xAF"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))
    
    def emit_imul_r32_r32_imm32(self, dst, src, value):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if src_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x69)  # imul r32, r/m32, imm32
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))
        self.text += int(value).to_bytes(4, "little", signed=True)

    def emit_imul(self, dst, src, value=None):
        if value is None:
            self.emit_imul_r32_r32(dst, src)
        else:
            self.emit_imul_r32_r32_imm32(dst, src, value)
    
    def emit_external_call(self, symbol_name):
        self.emit_call_rel32(symbol_name)

    def emit_runtime_call(self, symbol_name, arg_regs=None):
        if arg_regs is None:
            arg_regs = []

        # Windows x64:
        # 32 Byte Shadow Space + 8 Byte Alignment-Ausgleich
        self.emit_sub_rsp_imm8(40)
        self.emit_external_call(symbol_name)
        self.emit_add_rsp_imm8(40)
    
    def emit_call_rel32(self, symbol_name):
        sym_index = self.find_or_add_external(symbol_name)
        self.text.append(0xE8)

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset"        : reloc_offset,
            "symbol_index"  : sym_index,
            "type"          : IMAGE_REL_AMD64_REL32
        })
    
    def emit_call_r64(self, reg):
        reg_id = self._reg_id(reg)

        rex = 0x40
        if reg_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0xFF)
        self.text.append(0xD0 | (reg_id & 7))  # /2 call r64
    
    def emit_call(self, target):
        if target.startswith("_") or target in self.labels:
            self.emit_runtime_call(target)
        else:
            self.emit_sub_rsp_imm8(40)
            self.emit_call_r64(target)
            self.emit_add_rsp_imm8(40)

    def emit_call_lbl(self, target):
        self.emit_runtime_call(target)

    def emit_call_reg(self, target):
        self.emit_sub_rsp_imm8(40)
        self.emit_call_r64(target)
        self.emit_add_rsp_imm8(40)

    def emit_call_label(self, label):
        self.text.append(0xE8)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    def emit_cdq(self):
        self.text.append(0x99)
    
    # --------------------------------
    # idiv r32
    # --------------------------------
    def emit_idiv_r32(self, reg):
        reg_id = self._reg_id(reg)

        if reg_id >= 8:
            self.text.append(0x41)

        self.text.append(0xF7)
        self.text.append(0xF8 | (reg_id & 7))  # /7 idiv
    
    # --------------------------------
    # Vergleichsoperator abbilden
    # --------------------------------
    def emit_compare_result_eax_ebx(self, op):
        self.emit_cmp_r32_r32("eax", "ebx")

        set_map = {
            "=":  "sete",
            "<>": "setne",
            "<":  "setl",
            "<=": "setle",
            ">":  "setg",
            ">=": "setge",
        }

        if op not in set_map:
            raise RuntimeError(f"unsupported compare operator: {op}")

        self.emit_setcc_al(set_map[op])
        self.emit_movzx_eax_al()
    
    # --------------------------------
    # Sprung auf Label
    # --------------------------------
    def emit_jmp_label(self, label):
        patch_pos = self.emit_jmp_placeholder()

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    # --------------------------------
    # Bedingter Sprung auf Label
    # --------------------------------
    def emit_jcc_label(self, cc, label):
        patch_pos = self.emit_jcc_placeholder(cc)

        if label in self.labels:
            self.patch_rel32(patch_pos, self.labels[label])
        else:
            self.fixups.append({
                "patch_pos": patch_pos,
                "label": label
            })
    
    # --------------------------------
    # Am Ende prüfen
    # --------------------------------
    def check_unresolved_labels(self):
        if self.fixups:
            names = ", ".join(f["label"] for f in self.fixups)
            raise RuntimeError(f"Unresolved labels: {names}")
    
    def emit_cmp(self, left, right):
        if isinstance(right, int):
            if left.startswith("r") and not left.endswith("d"):
                self.emit_cmp_r64_imm32(left, right)
            else:
                self.emit_cmp_r32_imm32(left, right)
            return

        if left.startswith("r") and not left.endswith("d") and right.startswith("r") and not right.endswith("d"):
            self.emit_cmp_r64_r64(left, right)
        else:
            self.emit_cmp_r32_r32(left, right)

    def emit_test(self, left, right):
        if left.startswith("r") and not left.endswith("d") and right.startswith("r") and not right.endswith("d"):
            self.emit_test_r64_r64(left, right)
        else:
            self.emit_test_r32_r32(left, right)

    def emit_jmp(self, label): self.emit_jmp_label(label)
    def emit_je (self, label): self.emit_jcc_label("je" , label)
    def emit_jne(self, label): self.emit_jcc_label("jne", label)
    def emit_jz (self, label): self.emit_jcc_label("je" , label)
    def emit_jnz(self, label): self.emit_jcc_label("jne", label)
    def emit_jl (self, label): self.emit_jcc_label("jl" , label)
    def emit_jle(self, label): self.emit_jcc_label("jle", label)
    def emit_jg (self, label): self.emit_jcc_label("jg" , label)
    def emit_jge(self, label): self.emit_jcc_label("jge", label)
    
    # --------------------------------
    # cmp r32, imm32
    # --------------------------------
    def emit_cmp_r32_imm32(self, reg, value):
        reg_id = self._reg_id(reg)

        if reg_id >= 8:
            self.text.append(0x41)  # REX.B für r8d-r15d

        self.text.append(0x81)

        # /7 = CMP
        modrm = 0xF8 | (reg_id & 7)
        self.text.append(modrm)

        self.text += int(value).to_bytes(4, "little", signed=True)
    
    # --------------------------------
    # cmp r32, r32
    # --------------------------------
    def emit_cmp_r32_r32(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x40

        if right_id >= 8:
            rex |= 0x04  # REX.R

        if left_id >= 8:
            rex |= 0x01  # REX.B

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x39)  # cmp r/m32, r32

        modrm = 0xC0 | ((right_id & 7) << 3) | (left_id & 7)
        self.text.append(modrm)
    
    # --------------------------------
    # cmp r64, r64
    # --------------------------------
    def emit_cmp_r64_r64(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x48

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x39)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    def emit_cmp_r64_imm32(self, reg, value):
        reg_id = self._reg_id(reg)
        
        rex = 0x48
        
        if reg_id >= 8:
            rex |= 0x01
        
        self.text.append(rex)
        self.text.append(0x81)
        
        # /7 = cmp
        self.text.append(0xF8 | (reg_id & 7))
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_cmp_r64_r64(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x48

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x39)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    def emit_nil_check_rax(self, ok_label, fail_label):
        self.emit_test_r64_r64("rax", "rax")
        self.emit_jcc_label("jne", ok_label)
        self.emit_jmp_label(fail_label)
    
    # --------------------------------
    # Relativer Sprung mit Patch-Liste
    # --------------------------------
    def emit_jcc_placeholder(self, cc):
        opcodes = {
            "je":  b"\x0F\x84",
            "jne": b"\x0F\x85",
            "jl":  b"\x0F\x8C",
            "jle": b"\x0F\x8E",
            "jg":  b"\x0F\x8F",
            "jge": b"\x0F\x8D",
        }

        if cc not in opcodes:
            raise RuntimeError(f"unsupported condition jump: {cc}")

        self.text += opcodes[cc]

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        return patch_pos
    
    # --------------------------------
    # Operator jump
    # --------------------------------
    def emit_jump_by_op(self, op, label):
        jump_map = {
            "=":  "je",
            "<>": "jne",
            "<":  "jl",
            "<=": "jle",
            ">":  "jg",
            ">=": "jge",
        }

        if op not in jump_map:
            raise RuntimeError(f"unsupported jump op: {op}")

        self.emit_jcc_label(jump_map[op], label)
    
    # --------------------------------
    # Unbedingter Sprung
    # --------------------------------
    def emit_jmp_placeholder(self):
        self.text.append(0xE9)

        patch_pos = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        return patch_pos
    
    # --------------------------------
    # Sprung patcher
    # --------------------------------
    def patch_rel32(self, patch_pos, target_pos):
        # rel32 ist relativ zum nächsten Befehl,
        # also patch_pos + 4
        rel = target_pos - (patch_pos + 4)

        self.text[patch_pos:patch_pos + 4] = int(rel).to_bytes(
            4,
            "little",
            signed=True
        )
    
    def emit_lea_rcx_data_label(self, label):
        self.emit_lea_reg_data_label("rcx", label)
        
    def emit_lea_r64_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x48

        if dst_id >= 8:
            rex |= 0x04

        if base_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x8D)  # LEA r64, m

        self._emit_modrm_mem(dst_id, base, offset)
    
    def emit_lea_byte (self, dst, base, offset): self.emit_lea_r64_mem(dst, base, offset)
    def emit_lea_dword(self, dst, base, offset): self.emit_lea_r64_mem(dst, base, offset)
    def emit_lea_qword(self, dst, base, offset): self.emit_lea_r64_mem(dst, base, offset)

    # --------------------------------
    # lea reg, [rel data_label]
    # --------------------------------
    def emit_lea_reg_data_label(self, reg, label):
        reg_id = self._reg_id(reg)

        rex = 0x48
        if reg_id >= 8:
            rex |= 0x04

        sym_index = self.find_or_add_symbol(label)

        self.text.append(rex)
        self.text += b"\x8D"

        # RIP-relative: mod=00, r/m=101
        self.text.append(0x05 | ((reg_id & 7) << 3))

        reloc_offset = len(self.text)
        self.text += b"\x00\x00\x00\x00"

        self.text_relocations.append({
            "offset": reloc_offset,
            "symbol_index": sym_index,
            "type": IMAGE_REL_AMD64_REL32
        })

    def emit_mov_eax_imm32(self, value):
        self.text.append(0xB8)
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_rax_imm64(self, value):
        self.text += b"\x48\xB8"
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    def emit_mov_ecx_imm32(self, value):
        self.text.append(0xB9)  # mov ecx, imm32
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_reg_imm32(self, reg, value):
        reg_id = self._reg_id(reg)
        
        if reg_id >= 8:
            self.text.append(0x41)
        
        self.text.append(0xB8 + (reg_id & 7))
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_r8_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x40
        if dst_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x8A)  # mov r8, r/m8
        self._emit_modrm_mem(dst_id, base, offset)

    def emit_mov_mem_r8(self, base, offset, src):
        src_id  = self._reg_id(src)
        base_id = self._reg_id(base)

        rex = 0x40
        if src_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x88)  # mov r/m8, r8
        self._emit_modrm_mem(src_id, base, offset)
    
    def emit_mov_r32_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40
        if src_id >= 8: rex |= 0x04
        if dst_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x89)
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))
    
    def emit_movsxd_r64_r32(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x48
        if dst_id >= 8:
            rex |= 0x04
        if src_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x63)
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))
    
    def emit_mov_eax_ebx   (self): self.emit_mov_r32_r32   ("eax", "ebx")
    def emit_mov_ebx_eax   (self): self.emit_mov_r32_r32   ("ebx", "eax")
    
    def emit_movsxd_rax_eax(self): self.emit_movsxd_r64_r32("rax", "eax")
    
    # --------------------------------
    # mov r64, imm64
    # --------------------------------
    def emit_mov_reg_imm64(self, reg, value):
        reg_id = self._reg_id(reg)
        rex    = 0x48
        
        if reg_id >= 8:
            rex |= 0x01
            
        self.text.append(rex)
        self.text.append(0xB8 + (reg_id & 7))
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    # --------------------------------
    # mov eax, dword [rax + 8]
    # --------------------------------
    def emit_mov_r32_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x40
        if dst_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x8B)
        self._emit_modrm_mem(dst_id, base, offset)
    
    # --------------------------------
    # mov r64, [base + offset]
    # --------------------------------
    def emit_mov_r64_mem(self, dst, base, offset=0):
        dst_id  = self._reg_id(dst)
        base_id = self._reg_id(base)

        rex = 0x48

        if dst_id >= 8:
            rex |= 0x04  # REX.R

        if base_id >= 8:
            rex |= 0x01  # REX.B

        self.text.append(rex)
        self.text.append(0x8B)  # mov r64, r/m64

        self._emit_modrm_mem(dst_id, base, offset)
    
    # --------------------------------
    # mov dword [base + offset], r32
    # --------------------------------
    def emit_mov_mem_r32(self, base, offset, src):
        src_id  = self._reg_id(src)
        base_id = self._reg_id(base)

        rex = 0x40
        if src_id  >= 8: rex |= 0x04
        if base_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x89)
        self._emit_modrm_mem(src_id, base, offset)
    
    # --------------------------------
    # mov [base + offset], r64
    # --------------------------------
    def emit_mov_mem_r64(self, base, offset, src):
        src_id  = self._reg_id(src)
        base_id = self._reg_id(base)

        rex = 0x48

        if src_id >= 8:
            rex |= 0x04  # REX.R

        if base_id >= 8:
            rex |= 0x01  # REX.B

        self.text.append(rex)
        self.text.append(0x89)  # mov r/m64, r64

        self._emit_modrm_mem(src_id, base, offset)
    
    def emit_mov_r8d_imm32(self, value):
        self.text += b"\x41\xB8"
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_r9d_imm32(self, value):
        self.text += b"\x41\xB9"
        self.text += int(value).to_bytes(4, "little", signed=True)
    
    def emit_mov_r8_imm64(self, value):
        self.text += b"\x49\xB8"
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    def emit_mov_r9_imm64(self, value):
        self.text += b"\x49\xB9"
        self.text += int(value).to_bytes(8, "little", signed=False)
    
    # --------------------------------
    # mov r64, r64
    # --------------------------------
    def emit_mov_r64_r64(self, dst, src):
        ##
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)
        
        rex = 0x48
        
        if src_id >= 8:
            rex |= 0x04   # REX.R
        
        if dst_id >= 8:
            rex |= 0x01   # REX.B
        
        self.text.append(rex)
        self.text.append(0x89)
        
        modrm = 0xC0 | ((src_id & 7) << 3) | (dst_id & 7)
        self.text.append(modrm)
    
    # --------------------------------
    # movzx eax, al
    # --------------------------------
    def emit_movzx_eax_al(self):
        self.text += b"\x0F\xB6\xC0"
    
    def emit_movq_xmm_r64(self, dst, src):
        dst_id = self._xmm_id(dst)
        src_id = self._reg_id(src)

        self.text += b"\x66"

        rex = 0x48
        if dst_id >= 8:
            rex |= 0x04
        if src_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text += b"\x0F\x6E"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_movzx_r32_r8(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._reg_id(src)

        rex = 0x40
        if dst_id >= 8: rex |= 0x04
        if src_id >= 8: rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text += b"\x0F\xB6"
        self.text.append(0xC0 | ((dst_id & 7) << 3) | (src_id & 7))

    def emit_movq_r64_xmm(self, dst, src):
        dst_id = self._reg_id(dst)
        src_id = self._xmm_id(src)

        self.text += b"\x66"

        rex = 0x48
        if src_id >= 8: rex |= 0x04
        if dst_id >= 8: rex |= 0x01

        self.text.append(rex)
        self.text += b"\x0F\x7E"
        self.text.append(0xC0 | ((src_id & 7) << 3) | (dst_id & 7))

    def emit_mov_xmm_imm64_double_bits(self, xmm, bits):
        self.emit_mov_reg_imm64("rax", bits)
        self.emit_movq_xmm_r64(xmm, "rax")

    def emit_movzx(self, dst, src):
        if dst == "eax" and src == "al":
            self.emit_movzx_eax_al()
            return

        self.emit_movzx_r32_r8(dst, src)
    
    def emit_mov(self, dst, src):
        if isinstance(src, int):
            if dst.startswith("r") and not dst.endswith("d"):
                self.emit_mov_reg_imm64(dst, src)
            else:
                self.emit_mov_reg_imm32(dst, src)
            return

        if dst.startswith("xmm"):
            raise RuntimeError("use XMM-specific mov methods")

        if dst.startswith("r") and not dst.endswith("d") and src.startswith("r") and not src.endswith("d"):
            self.emit_mov_r64_r64(dst, src)
        else:
            self.emit_mov_r32_r32(dst, src)

    def emit_add(self, dst, src):
        if isinstance(src, int):
            if dst.startswith("r") and not dst.endswith("d"):
                self.emit_add_r64_imm32(dst, src)
            else:
                self.emit_add_r32_imm32(dst, src)
            return

        if dst.startswith("r") and not dst.endswith("d") and src.startswith("r") and not src.endswith("d"):
            self.emit_add_r64_r64(dst, src)
        else:
            self.emit_add_r32_r32(dst, src)

    def emit_setne(self, reg):
        if reg != "al":
            raise RuntimeError("currently only setne al supported")
        self.emit_setcc_al("setne")

    def emit_sub(self, dst, src):
        if isinstance(src, int):
            if dst.startswith("r") and not dst.endswith("d"):
                self.emit_sub_r64_imm32(dst, src)
            else:
                self.emit_sub_r32_imm32(dst, src)
            return

        if dst.startswith("r") and not dst.endswith("d") and src.startswith("r") and not src.endswith("d"):
            self.emit_sub_r64_r64(dst, src)
        else:
            self.emit_sub_r32_r32(dst, src)
    
    def emit_push_r64(self, reg):
        ##
        reg_id = self._reg_id(reg)
        
        if reg_id >= 8:
            self.text.append(0x41)
        
        self.text.append(0x50 + (reg_id & 7))
    
    def emit_pop_r64(self, reg):
        ##
        reg_id = self._reg_id(reg)
        
        if reg_id >= 8:
            self.text.append(0x41)
        
        self.text.append(0x58 + (reg_id & 7))
        
    def emit_ret(self):
        self.text.append(0xC3)
    
    def emit_setcc_al(self, cc):
        opcodes = {
            "sete":  b"\x0F\x94",
            "setne": b"\x0F\x95",
            "setl":  b"\x0F\x9C",
            "setle": b"\x0F\x9E",
            "setg":  b"\x0F\x9F",
            "setge": b"\x0F\x9D",
        }

        if cc not in opcodes:
            raise RuntimeError(f"unsupported setcc: {cc}")

        self.text += opcodes[cc]
        self.text.append(0xC0)  # al
    
    def emit_sub_rsp_imm8(self, value):
        self.text += b"\x48\x83\xEC"
        self.text.append(value & 0xFF)

    def emit_add_rsp_imm8(self, value):
        self.text += b"\x48\x83\xC4"
        self.text.append(value & 0xFF)

    # --------------------------------
    # test r32, r32
    # --------------------------------
    def emit_test_r32_r32(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x40

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        if rex != 0x40:
            self.text.append(rex)

        self.text.append(0x85)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    # --------------------------------
    # test r64, r64
    # --------------------------------
    def emit_test_r64_r64(self, left, right):
        left_id  = self._reg_id(left)
        right_id = self._reg_id(right)

        rex = 0x48

        if right_id >= 8:
            rex |= 0x04

        if left_id >= 8:
            rex |= 0x01

        self.text.append(rex)
        self.text.append(0x85)
        self.text.append(0xC0 | ((right_id & 7) << 3) | (left_id & 7))
    
    def emit_function_prolog(self, local_size=256):
        self.emit_push_r64("rbp")
        self.emit_mov_r64_r64("rbp", "rsp")

        if local_size:
            self.emit_sub_r64_imm32("rsp", local_size)

    def emit_function_epilog(self):
        self.emit_mov_r64_r64("rsp", "rbp")
        self.emit_pop_r64("rbp")
        self.emit_ret()
    
    def add_data_string(self, name, text):
        offset = len(self.data)
        self.data += text.encode("utf-8") + b"\x00"
        self.add_symbol(
            name            = name,
            value           = offset,
            section_number  = 2
        )
        return offset
    
    def add_symbol(self, name, value, section_number=1):
        self.symbols.append({
            "name"      : name,
            "value"     : value,
            "section"   : section_number,
            "type"      : IMAGE_SYM_DTYPE_FUNCTION,
            "storage"   : IMAGE_SYM_CLASS_EXTERNAL,
            "aux"       : 0
        })
    
    # boolean
    def emit_normalize_bool_eax(self):
        self.emit_test_r32_r32("eax", "eax")
        self.emit_setcc_al("setne")
        self.emit_movzx_eax_al()
        
    def emit_bool_not_eax(self):
        self.emit_test_r32_r32("eax", "eax")
        self.emit_setcc_al("sete")
        self.emit_movzx_eax_al()
        
    def write_symbol(self, sym):
        name = sym["name"].encode("ascii")
        
        if len(name) <= 8:
            name_field = name.ljust(8, b"\x00")
        else:
            offset = self.get_string_offset(sym["name"])
            
            # Long name:
            # first 4 bytes = 0
            # next  4 bytes = offset into string table
            name_field = struct.pack("<II", 0, offset)
        
        return (
            name_field +
            struct.pack(
                "<IhHBB",
                sym["value"],
                sym["section"],
                sym["type"],
                sym["storage"],
                sym["aux"]
            )
        )
    
    def add_external_symbol(self, name):
        index = len(self.symbols)
        self.symbols.append({
            "name": name,
            "value": 0,
            "section": 0,
            "type": 0,
            "storage": IMAGE_SYM_CLASS_EXTERNAL,
            "aux": 0
        })
        return index

    def get_string_offset(self, name):
        if name in self.string_offsets:
            return self.string_offsets[name]

        # Offset zählt ab Anfang der String Table.
        # Die ersten 4 Bytes sind später die Größenangabe.
        offset = 4 + len(self.string_table)

        self.string_table += name.encode("ascii") + b"\x00"
        self.string_offsets[name] = offset

        return offset

    def find_symbol_index(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index
        return None

    def find_or_add_symbol(self, name):
        index = self.find_symbol_index(name)

        if index is None:
            raise RuntimeError(f"Symbol not defined: {name}")

        return index
    
    def find_or_add_external(self, name):
        for index, sym in enumerate(self.symbols):
            if sym["name"] == name:
                return index
        
        return self.add_external_symbol(name)
    
    def write(self, filename):
        number_of_sections  = 2

        coff_header_size    = 20
        section_header_size = 40

        header_size = coff_header_size + number_of_sections * section_header_size
        
        text_size = len(self.text)
        data_size = len(self.data)
        
        text_ptr  = header_size
        data_ptr  = text_ptr + text_size
        
        text_reloc_ptr   = data_ptr + data_size
        text_reloc_count = len(self.text_relocations)
        text_reloc_size  = text_reloc_count * 10
        
        text_reloc_data  = bytearray()
        for reloc in self.text_relocations:
            text_reloc_data += struct.pack(
                "<IIH",
                reloc["offset"],
                reloc["symbol_index"],
                reloc["type"]
            )
        
        data_reloc_ptr   = text_reloc_ptr + text_reloc_size
        data_reloc_count = len(self.data_relocations)
        data_reloc_size  = data_reloc_count * 10
        
        data_reloc_data  = bytearray()
        for reloc in self.data_relocations:
            data_reloc_data += struct.pack(
                "<IIH",
                reloc["offset"],
                reloc["symbol_index"],
                reloc["type"]
            )
        
        symbol_table_ptr  = data_reloc_ptr + data_reloc_size
        number_of_symbols = len(self.symbols)

        coff_header = struct.pack(
            "<HHIIIHH",
            IMAGE_FILE_MACHINE_AMD64,
            number_of_sections,
            int(time.time()),
            symbol_table_ptr,
            number_of_symbols,
            0,
            0
        )
        
        text_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".text\x00\x00\x00",
            0,
            0,
            text_size,
            text_ptr,
            text_reloc_ptr if text_reloc_count else 0,
            0,
            text_reloc_count,
            0,
            IMAGE_SCN_CNT_CODE | IMAGE_SCN_MEM_EXECUTE | IMAGE_SCN_MEM_READ
        )

        data_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".data\x00\x00\x00",
            0,
            0,
            data_size,
            data_ptr if data_size else 0,
            data_reloc_ptr if data_reloc_count else 0,
            0,
            data_reloc_count,
            0,
            IMAGE_SCN_CNT_INITIALIZED_DATA | IMAGE_SCN_MEM_READ | IMAGE_SCN_MEM_WRITE
        )

        symbol_data = bytearray()
        for sym in self.symbols:
            symbol_data += self.write_symbol(sym)

        string_table = (
            struct.pack("<I", 4 + len(self.string_table)) +
            self.string_table
        )

        print("text_relocations:", self.text_relocations)
        print("text_reloc_count:", text_reloc_count)
        print("text_reloc_ptr:", text_reloc_ptr)
        
        self.check_unresolved_labels()
        
        with open(filename, "wb") as f:
            f.write(coff_header)
            f.write(text_section_header)
            f.write(data_section_header)
            
            f.write(self.text)
            f.write(self.data)
            
            f.write(text_reloc_data)
            f.write(data_reloc_data)
            
            f.write(symbol_data)
            f.write(string_table)

# ---------------------------------------------------------------------------
# Windows 10 64-Bit PE executable writer
# ---------------------------------------------------------------------------
class PEWriter64:
    IMAGE_BASE     = 0x140000000
    FILE_ALIGNMENT = 0x200
    SECTION_ALIGN  = 0x1000

    def __init__(self, coff):
        self.coff = coff
        
        self.imports = {
            "kernel32.dll": [
                "ExitProcess"
            ],
            "dbase2many.dll": [
                "_jit_print_int",
                "_jit_print_text"
            ]
        }

    @property
    def text(self):
        return self.coff.text
    
    @property
    def code(self):
        return self.coff.code
    
    @property
    def data(self):
        return self.coff.data

    def find_entrypoint(self):
        for sym in self.coff.symbols:
            if sym["name"] in ("main", "_main"):
                return sym["value"]
        raise RuntimeError("entry point not found: main/_main")

    def align(self, value, alignment):
        return (value + alignment - 1) & ~(alignment - 1)

    def pad_to(self, data, size):
        while len(data) < size:
            data.append(0)
    
    def emit_ret(self):
        self.text.append(0xC3)

    def all_import_functions(self):
        funcs = []
        for dll_name, names in self.imports.items():
            for name in names:
                if name not in funcs:
                    funcs.append(name)
        return funcs

    def build_text_with_import_thunks(self):
        text_image = bytearray(self.text)
        self.import_thunk_offsets = {}

        for name in self.all_import_functions():
            self.import_thunk_offsets[name] = len(text_image)

            # jmp qword [rip + disp32]
            # FF 25 xx xx xx xx
            text_image += b"\xFF\x25\x00\x00\x00\x00"

        return text_image

    def patch_external_call_relocations(self, text_image, text_rva):
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]
            name = sym["name"]

            if name not in self.import_thunk_offsets:
                continue

            patch_pos = reloc["offset"]
            thunk_off = self.import_thunk_offsets[name]

            target_rva = text_rva + thunk_off
            next_rva   = text_rva + patch_pos + 4

            rel32 = target_rva - next_rva

            text_image[patch_pos:patch_pos + 4] = int(rel32).to_bytes(
                4,
                "little",
                signed=True
            )

    def patch_import_thunks(self, text_image, text_rva):
        for name, thunk_off in self.import_thunk_offsets.items():
            if name not in self.import_iat_rvas:
                raise RuntimeError(f"IAT RVA missing for import: {name}")

            iat_rva = self.import_iat_rvas[name]

            thunk_rva = text_rva + thunk_off
            next_rva  = thunk_rva + 6

            disp32 = iat_rva - next_rva

            text_image[thunk_off:thunk_off + 6] = (
                b"\xFF\x25" +
                int(disp32).to_bytes(4, "little", signed=True)
            )

    def symbol_rva(self, sym, text_rva, data_rva):
        if sym["section"] == 1:
            return text_rva + sym["value"]

        if sym["section"] == 2:
            return data_rva + sym["value"]

        raise RuntimeError(f"unsupported symbol section: {sym}")

    def patch_internal_relocations(self, text_image, data_image, text_rva, data_rva):
        # .text Relocations, z.B. lea rcx, [rel str_0]
        for reloc in self.coff.text_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            # externe Imports werden separat über Thunks behandelt
            if sym["section"] == 0:
                continue

            if reloc["type"] == IMAGE_REL_AMD64_REL32:
                patch_pos = reloc["offset"]
                target_rva = self.symbol_rva(sym, text_rva, data_rva)
                next_rva = text_rva + patch_pos + 4

                rel32 = target_rva - next_rva

                text_image[patch_pos:patch_pos + 4] = int(rel32).to_bytes(
                    4,
                    "little",
                    signed=True
                )
            else:
                raise RuntimeError(f"unsupported text relocation type: {reloc['type']}")

        # .data Relocations, z.B. ctx enthält qword-Adresse von int_vars
        for reloc in self.coff.data_relocations:
            sym = self.coff.symbols[reloc["symbol_index"]]

            if reloc["type"] == IMAGE_REL_AMD64_ADDR64:
                patch_pos = reloc["offset"]
                target_va = self.IMAGE_BASE + self.symbol_rva(sym, text_rva, data_rva)

                data_image[patch_pos:patch_pos + 8] = int(target_va).to_bytes(
                    8,
                    "little",
                    signed=False
                )
            else:
                raise RuntimeError(f"unsupported data relocation type: {reloc['type']}")

    def build_import_section(self, idata_rva):
        imports = self.imports
        self.import_iat_rvas = {}

        descriptor_size = 20
        descriptors_size = (len(imports) + 1) * descriptor_size

        data = bytearray(b"\x00" * descriptors_size)

        cursor = descriptors_size
        descriptors = []

        for dll_name, funcs in imports.items():
            ilt_rva = idata_rva + cursor

            ilt_offsets = []
            for func in funcs:
                ilt_offsets.append(cursor)
                data += b"\x00" * 8
                cursor += 8

            data += b"\x00" * 8
            cursor += 8

            iat_rva = idata_rva + cursor

            iat_offsets = []
            for func in funcs:
                iat_offsets.append(cursor)
                self.import_iat_rvas[func] = idata_rva + cursor
                data += b"\x00" * 8
                cursor += 8

            data += b"\x00" * 8
            cursor += 8

            hint_name_rvas = []

            for func in funcs:
                hint_name_rva = idata_rva + cursor
                hint_name_rvas.append(hint_name_rva)

                data += struct.pack("<H", 0)
                data += func.encode("ascii") + b"\x00"
                cursor = len(data)

            dll_name_rva = idata_rva + cursor
            data += dll_name.encode("ascii") + b"\x00"
            cursor = len(data)

            for off, hn_rva in zip(ilt_offsets, hint_name_rvas):
                struct.pack_into("<Q", data, off, hn_rva)

            for off, hn_rva in zip(iat_offsets, hint_name_rvas):
                struct.pack_into("<Q", data, off, hn_rva)

            descriptors.append((ilt_rva, dll_name_rva, iat_rva))

        for index, (ilt_rva, dll_name_rva, iat_rva) in enumerate(descriptors):
            struct.pack_into(
                "<IIIII",
                data,
                index * descriptor_size,
                ilt_rva,
                0,
                0,
                dll_name_rva,
                iat_rva
            )

        return data

    def write(self, filename):
        dos_header = bytearray(64)
        dos_header[0:2] = b"MZ"
        struct.pack_into("<I", dos_header, 0x3C, 0x80)

        dos_stub = bytearray(0x80 - len(dos_header))

        pe_sig = b"PE\x00\x00"

        number_of_sections      = 3
        size_of_optional_header = 0xF0
        section_header_size     = 40

        file_header = struct.pack(
            "<HHIIIHH",
            0x8664,
            number_of_sections,
            int(time.time()),
            0,
            0,
            size_of_optional_header,
            0x0022
        )

        headers_size = self.align(0x80 + 4 + 20 +
            size_of_optional_header + number_of_sections * section_header_size,
            self.FILE_ALIGNMENT
        )

        text_image          = self.build_text_with_import_thunks()

        text_rva            = self.SECTION_ALIGN
        entry_rva           = text_rva + self.find_entrypoint()

        text_raw            = headers_size
        text_raw_size       = self.align(len(text_image), self.FILE_ALIGNMENT)
        text_virtual_size   = len(text_image)
        
        data_rva            = self.align(text_rva + text_virtual_size, self.SECTION_ALIGN)
        data_raw            = text_raw + text_raw_size
        data_raw_size       = self.align(len(self.data), self.FILE_ALIGNMENT)
        data_virtual_size   = len(self.data)
        
        idata_rva           = self.align(data_rva + data_virtual_size, self.SECTION_ALIGN)
        idata_raw           = data_raw + data_raw_size
        idata               = self.build_import_section(idata_rva)

        data_image = bytearray(self.data)

        idata = self.build_import_section(idata_rva)

        self.patch_internal_relocations(
            text_image,
            data_image,
            text_rva,
            data_rva
        )

        self.patch_external_call_relocations(text_image, text_rva)
        self.patch_import_thunks(text_image, text_rva)
        
        idata_raw_size      = self.align(len(idata), self.FILE_ALIGNMENT)
        idata_virtual_size  = len(idata)
        
        size_of_image = self.align(
            idata_rva + idata_virtual_size,
            self.SECTION_ALIGN
        )

        optional_header     = bytearray()

        optional_header += struct.pack("<H", 0x20B)      # PE32+
        optional_header += struct.pack("<BB", 14, 0)     # linker version
        optional_header += struct.pack("<III",
            text_raw_size, 0, 0
        )

        optional_header += struct.pack("<I", entry_rva)  # AddressOfEntryPoint
        optional_header += struct.pack("<I", text_rva)   # BaseOfCode
        optional_header += struct.pack("<Q", self.IMAGE_BASE)

        optional_header += struct.pack("<II",
            self.SECTION_ALIGN,
            self.FILE_ALIGNMENT
        )

        optional_header += struct.pack("<HHHHHH",
            6, 0,    # OS version
            0, 0,    # Image version
            6, 0     # Subsystem version
        )

        optional_header += struct.pack("<I", 0)          # Win32VersionValue
        optional_header += struct.pack("<I", size_of_image)
        optional_header += struct.pack("<I", headers_size)
        optional_header += struct.pack("<I", 0)          # Checksum

        optional_header += struct.pack("<HH",
            3,       # Windows CUI
            0x8160   # DLL characteristics
        )

        optional_header += struct.pack("<QQQQ",
            0x100000,  # SizeOfStackReserve
            0x1000,    # SizeOfStackCommit
            0x100000,  # SizeOfHeapReserve
            0x1000     # SizeOfHeapCommit
        )

        optional_header += struct.pack("<II",
            0,      # LoaderFlags
            16      # NumberOfRvaAndSizes
        )

        data_directories = bytearray(16 * 8)
        struct.pack_into(
            "<II",
            data_directories,
            1 * 8,        # Import Directory
            idata_rva,
            len(idata)
        )
        
        optional_header += data_directories

        if len(optional_header) != size_of_optional_header:
            raise RuntimeError(len(optional_header))

        text_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".text\x00\x00\x00",
            text_virtual_size,
            text_rva,
            text_raw_size,
            text_raw,
            0,
            0,
            0,
            0,
            0x60000020
        )

        data_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".data\x00\x00\x00",
            data_virtual_size,
            data_rva,
            data_raw_size,
            data_raw,
            0,
            0,
            0,
            0,
            0xC0000040
        )
        
        idat_section_header = struct.pack(
            "<8sIIIIIIHHI",
            b".idata\x00\x00",
            idata_virtual_size,
            idata_rva,
            idata_raw_size,
            idata_raw,
            0,
            0,
            0,
            0,
            0xC0000040
        )
        
        image  = bytearray()
        image += dos_header
        image += dos_stub
        
        image += pe_sig
        image += file_header
        image += optional_header
        
        image += text_section_header
        image += data_section_header
        image += idat_section_header

        self.pad_to(image, text_raw)
        
        image += text_image; self.pad_to( image,  text_raw +  text_raw_size )
        image += data_image; self.pad_to( image,  data_raw +  data_raw_size )
        image +=      idata; self.pad_to( image, idata_raw + idata_raw_size )

        with open(filename, "wb") as f:
            f.write(image)

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
# the transpiler generator for Pascal->Assembly
# ---------------------------------------------------------------------------
class AsmJitGenerator(MiniPascalParserVisitor):
    def __init__(self, backend=None):
        self.backend = backend or AsmJitBackend()   # default backend
        self.lines   = self.backend.lines
        
        self.vars               = {}
        self.next_slot          = 0
        self.program_name       = "Program"
        self.var_types          = {}
        self.cpp_print_lines    = []
        
        self.source_file       = None
        self.source_dir        = None
        
        self.loaded_units      = {}
        self.loading_units     = set()
        self.unit_init_labels  = []
        self.current_unit      = None
        
        self.vars               = {}
        self.var_types          = {}

        self.int_slots          = {}
        self.double_slots       = {}

        self.next_int_slot      = 0
        self.next_double_slot   = 0
        self.next_string_slot   = 0
        self.next_record_slot   = 0
        self.next_arrays_slot   = 0
        self.next_pointr_slot   = 0
        
        self.label_id           = 0
        
        self.string_literals    = []
        self.double_literals    = []
        
        self.procedures         = {}
        self.functions          = {}
        self.constants          = {}
        self.variables          = []
        self.enums              = {}
        self.records            = {}
        self.arrays             = {}
        self.classes            = {}
        
        self.current_class  = None
        self.current_method = None
        
        self.type_aliases       = {}
        self.pointer_types      = {}
        
        self.scope_stack        = []
        
        self.local_var_stack    = []
        self.local_const_stack  = []
        self.exit_label_stack   = []
        self.try_except_stack   = []
        
        self.break_label_stack    = []
        self.continue_label_stack = []

        self.asm_label_mappings = []
        
        self.current_function   = None
        self.current_proc_params= {}
        
        self.section_text = []
        self.section_data = []
        
        self.constants["true"] = {
            "name": "True",
            "type": "integer",
            "value": 1
        }

        self.constants["false"] = {
            "name": "False",
            "type": "integer",
            "value": 0
        }

        self.asm_file               = CDATA.asm_file
        self.emit_local_string_data = True
        
        self.module_kind        = "program"
        self.module_kind_value  = 1
        
        self.exports = []
    
    def format_error(self, filename, err):
        template = ERROR_MAP.get(err.code, err.code)
        message  = template.format(**err.params)
        
        return f"{err.code}: {os.path.basename(filename)} {err.line}:{err.column} {message}"
    
    def format_method_signature(self, params):
        if not params:
            return "()"
            
        types = []
        
        for p in params:
            types.append(self.resolve_type(p["type"]))
            
        return "(" + ", ".join(types) + ")"
    
    def current_except_label(self):
        if not self.try_except_stack:
            return None
        return self.try_except_stack[-1]["except_label"]
    
    def is_double(self, typ):
        return typ.lower() == "double"

    def is_integer(self, typ):
        return typ.lower() == "integer"
    
    def push_const_scope(self):
        self.local_const_stack.append({})

    def pop_const_scope(self):
        self.local_const_stack.pop()

    def current_const_scope(self):
        if not self.local_const_stack:
            return None
        return self.local_const_stack[-1]

    def push_local_scope(self):
        self.local_var_stack.append({
            "vars": {},
            "next_offset": 0
        })

    def pop_local_scope(self):
        self.local_var_stack.pop()

    def current_local_scope(self):
        if not self.local_var_stack:
            return None
        return self.local_var_stack[-1]

    def class_instance_size(self, ctx, class_type):
        key = class_type.lower()

        if key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_type)

        return self.classes[key].size
    
    def method_signature(self, params):
        return tuple(self.resolve_type(p["type"]) for p in params)
    
    def type_size(self, ctx, typ):
        typ = self.resolve_type(typ)
        
        if isinstance(typ, dict):
            if typ.get("kind") == "array":
                return typ["size"]
        
        if isinstance(typ, str) and typ in self.classes:
            return typ
        
        if isinstance(typ, str) and typ.startswith("^"):
            return 8
        
        if typ == "integer":
            return 4
            
        if typ == "double":
            return 8
            
        if typ == "string":
            return 8

        if isinstance(typ, str) and typ in self.records:
            return self.records[typ].size
        
        if isinstance(typ, str) and typ in self.arrays:
            return self.arrays[typ].size

        raise CompileError(ctx, "E0004", name=typ)

    def actual_param_variable_ref(self, ctx, arg):
        expr = arg.expr()

        if expr is None:
            raise CompileError(ctx, "E0005", got="empty", expected="pointer variable")

        refs = []

        def walk(node):
            if node is None:
                return

            if isinstance(node, MiniPascalParser.VariableRefContext):
                refs.append(node)
                return

            if hasattr(node, "children") and node.children:
                for child in node.children:
                    walk(child)

        walk(expr)

        if len(refs) != 1:
            raise CompileError(ctx, "E0005", got=expr.getText(), expected="single variable")

        if refs[0].getText() != expr.getText():
            raise CompileError(ctx, "E0005", got=expr.getText(), expected="single variable")

        return refs[0]
    
    def declare_record(self, ctx, name, fields):
        key = name.lower()

        if key in self.records:
            raise CompileError(ctx, "E0002", name=name)

        offset = 0
        record_fields = {}

        for field_name, field_type in fields:
            field_key = field_name.lower()
            resolved_type = self.resolve_type(field_type)
            size = self.type_size(ctx, resolved_type)

            record_fields[field_key] = RecordFieldInfo(
                name    = field_name,
                type    = resolved_type,
                offset  = offset,
                size    = size
            )

            offset += size

        self.records[key] = RecordInfo(
            name    = name,
            fields  = record_fields,
            size    = offset
        )
    
    def declare_class(self, ctx, name, fields, methods, parent_name=None):
        key = name.lower()
        
        parent_key      = None
        parent_size     = 0
        parent_fields   = {}
        parent_methods  = {}
        
        if parent_name:
            parent_key = parent_name.lower()

            if parent_key not in self.classes:
                raise CompileError(ctx, "E0004", name=parent_name)

            parent_cls    = self.classes[parent_key]
            parent_size   = parent_cls.size

            parent_fields = dict(parent_cls.fields)

            for mname, overloads in parent_cls.methods.items():
                parent_methods[mname] = list(overloads)
        
        if key in self.classes:
            raise CompileError(ctx, "E0002", name=name)
        
        offset = parent_size
        class_fields = dict(parent_fields)
        
        for field_name, field_type, visibility in fields:
            field_key = field_name.lower()
            resolved_type = self.resolve_type(field_type)
            size = self.type_size(ctx, resolved_type)
            
            class_fields[field_key] = RecordFieldInfo(
                name        = field_name,
                type        = resolved_type,
                offset      = offset,
                size        = size,
                visibility  = visibility
            )
            
            offset += size
        
        class_methods = dict(parent_methods)
        
        for method in methods:
            method_key = method["name"].lower()
            
            info = ClassMethodInfo(
                name        = method["name"],
                kind        = method["kind"],
                label       = method["label"],
                params      = method.get("params", []),
                owner       = key,
                return_type = method.get("return_type", None),
                implemented = False,
                mangled     = method.get("mangled", None),
                visibility  = method.get("visibility", "public")
            )
            
            class_methods.setdefault(method_key, [])
            sig = self.method_signature(info.params)
            
            # gleiche Signatur aus Parent-Klasse entfernen:
            # Kindklasse überschreibt diese Methode
            class_methods[method_key] = [
                old for old in class_methods[method_key]
                if self.method_signature(old.params) != sig
            ]
            
            class_methods[method_key].append(info)
        
        has_create  = "create"  in class_methods
        has_destroy = "destroy" in class_methods
        
        if not has_create:
            raise CompileError(
                ctx,
                "E0019",
                text = f"class {name} requires constructor Create"
            )
        
        if not has_destroy:
            raise CompileError(
                ctx,
                "E0019",
                text = f"class {name} requires destructor Destroy"
            )
        
        if "create" not in class_methods:
            raise CompileError(ctx, "E0019", text = f"class {name} requires constructor Create")
        
        if "destroy" not in class_methods:
            raise CompileError(ctx, "E0019", text = f"class {name} requires destructor Destroy")
        
        self.classes[key] = ClassInfo(
            name    = name,
            fields  = class_fields,
            methods = class_methods,
            size    = offset,
            parent  = parent_key
        )
    
    def validate_class_methods(self, ctx):
        for class_key, cls in self.classes.items():
            for method_name, overloads in cls.methods.items():
                for method in overloads:
                    
                    # geerbte Methode gehört nicht zu dieser Klasse
                    if method.owner != class_key:
                        continue
                    
                    if not method.implemented:
                        raise CompileError(
                            ctx,
                            "E0019",
                            text = (
                                f"class {cls.name} method "
                                f"{method.name}{self.format_method_signature(method.params)} "
                                f"is declared but not implemented"
                            )
                        )
    
    def normalize_bool_eax(self):
        self.emit_cmp   (REG_EAX, 0)
        self.emit_setne (REG_AL)
        self.emit_movzx (REG_EAX, REG_AL)
    
    def normalize_unit_name(self, unit_name):
        return unit_name.lower().replace(".", "_")

    def unit_scoped_name(self, name):
        if self.current_unit:
            return self.normalize_unit_name(self.current_unit) + "_" + name

        return name
    
    def qualified_ident_text(self, ctx):
        return ctx.getText()
    
    def declare_array(self, ctx, name, index_min, index_max, element_type, init_values=None, dimensions=None):
        key = name.lower()

        if key in self.arrays:
            raise CompileError(ctx, "E0002", name=name)

        resolved_type = self.resolve_type(element_type)
        element_size  = self.type_size(ctx, resolved_type)
        
        if isinstance(resolved_type, str) and resolved_type in self.arrays:
            nested_array = self.arrays[resolved_type]

            if dimensions is None:
                dimensions = [
                    {
                        "min": index_min,
                        "max": index_max
                    }
                ]

            dimensions    = dimensions + nested_array.dimensions
            resolved_type = nested_array.element_type
        
        count = index_max - index_min + 1

        if count <= 0:
            raise CompileError(ctx, "E0005", got=str(index_max), expected=f">= {index_min}")

        if init_values is None:
            init_values = []

        if len(init_values) > count:
            raise CompileError(ctx, "E0005", got=str(len(init_values)), expected=f"max {count}")
        
        if dimensions is None:
            dimensions = [
                {
                    "min": index_min,
                    "max": index_max
                }
            ]

        count = 1
        for dim in dimensions:
            count *= dim["max"] - dim["min"] + 1
    
        self.arrays[key] = ArrayInfo(
            name            = name,
            index_min       = index_min,
            index_max       = index_max,
            element_type    = resolved_type,
            element_size    = element_size,
            size            = count * element_size,
            init_values     = init_values,
            dimensions      = dimensions
        )
    
    def declare_array_type(self, name, dimensions, element_type):
        element_type = self.resolve_type(element_type)

        # Array von Array erkennen
        if isinstance(element_type, dict) and element_type.get("kind") == "array":
            full_dimensions = dimensions + element_type["dimensions"]
            base_type = element_type["base_type"]
        else:
            full_dimensions = dimensions
            base_type = element_type

        self.types[name.lower()] = {
            "kind": "array",
            "name": name,
            "dimensions": full_dimensions,
            "base_type": base_type
        }
    
    def declare_const(self, ctx, name, value, typ):
        key = name.lower()

        scope = self.current_const_scope()

        if scope is not None:
            if key in scope:
                raise CompileError(ctx, "E0002", name=name)

            scope[key] = {
                "name": name,
                "type": typ.lower(),
                "value": value
            }
            return

        if key in self.constants:
            raise CompileError(ctx, "E0002", name=name)

        self.constants[key] = {
            "name": name,
            "type": typ,
            "value": value
        }
    
    def declare_type_alias(self, ctx, name, target_type):
        key = name.lower()

        if key in self.type_aliases:
            raise CompileError(ctx, "E0002", name=name)

        self.type_aliases[key] = target_type.lower()
    
    def declare_local_var(self, ctx, name, vtype):
        scope = self.current_local_scope()
        
        if scope is None:
            self.declare_var(ctx, name, vtype)
            return
        
        key = name.lower()
        typ = self.resolve_type(vtype)
        
        if key in scope["vars"]:
            raise CompileError(ctx, "E0002", name=name)
        
        if typ == "integer":
            size = 8
        
        elif typ == "double":
            size = 8
        
        elif typ == "string":
            size = 8
        
        elif isinstance(typ, str) and typ.startswith("^"):
            size = 8
        
        elif isinstance(typ, str) and typ in self.records:
            size = self.records[typ].size
        
        elif isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]

            if getattr(array_info, "is_dynamic", False):
                slot = self.next_pointr_slot
                self.next_pointr_slot += 1
            else:
                slot = self.next_arrays_slot
                self.next_arrays_slot += array_info.size
        
        elif isinstance(typ, str) and typ in self.enums:
            typ = "integer"
            size = 8
        
        else:
            raise CompileError(
                ctx,
                "E0005",
                got=typ,
                expected="integer/double/string/pointer/record/array/enum"
            )
        
        scope["next_offset"] += size
        offset = -scope["next_offset"]
        
        scope["vars"][key] = {
            "name": name,
            "type": typ,
            "offset": offset,
            "size": size
        }
    
    def declare_var(self, ctx, name, vtype):
        key = name.lower()
        typ = self.resolve_type(vtype)
        
        if key in self.vars:
            raise CompileError(ctx, "E0002", name=name)
        
        symbol = None
        use_direct_coff_globals = (
            hasattr(self, "coff")
            and self.backend.name == BACKEND_OBJFILE
        )
        
        if typ == "integer":
            slot = self.next_int_slot
            self.next_int_slot += 1
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_i32(symbol)
        
        elif typ == "double":
            slot = self.next_double_slot
            self.next_double_slot += 1
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_double(symbol)
        
        elif typ == "string":
            slot = self.next_string_slot
            self.next_string_slot += 1
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
        
        elif isinstance(typ, str) and typ in self.records:
            slot = self.next_record_slot
            self.next_record_slot += self.records[typ].size
        
        elif isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]

            if getattr(array_info, "is_dynamic", False):
                slot = self.next_pointr_slot
                self.next_pointr_slot += 1
            else:
                slot = self.next_arrays_slot
                self.next_arrays_slot += array_info.size
        
        elif isinstance(typ, str) and typ in self.classes:
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
            
        elif isinstance(typ, str) and typ.startswith("^"):
            slot = self.next_pointr_slot
            self.next_pointr_slot += 1
            
            if use_direct_coff_globals:
                symbol = f"_var_{name}"
                self.coff.add_data_qword(symbol)
            
        else:
            raise CompileError(ctx, "E0004", name=vtype)
        
        self.vars[key] = {
            "name": name,
            "type": typ,
            "slot": slot,
        }
        
        if symbol is not None:
            self.vars[key]["symbol"] = symbol
            
        self.var_types[key] = typ

    def identifier_exists(self, name):
        if name in self.enums:
            return True

        if name in self.type_aliases:
            return True

        if name in self.constants:
            return True

        if name in self.variables:
            return True

        if hasattr(self, "functions") and name in self.functions:
            return True

        if hasattr(self, "procedures") and name in self.procedures:
            return True

        return False

    def declare_enum(self, ctx, name, values):
        key = name.lower()

        if key in self.enums:
            raise CompileError(ctx, "E0016", name=name)

        enum_values = {}

        for value_name, value_int in values:
            value_key = value_name.lower()

            if value_key in enum_values:
                raise CompileError(ctx, "E0017", value_name=value_name)

            enum_values[value_key] = value_int
            self.declare_const(ctx, value_name, value_int, "integer")

        self.enums[key] = EnumInfo(name, enum_values)
        self.declare_type_alias(ctx, name, "integer")
    
    def resolve_class_field_path(self, ctx, parts):
        var_name = parts[0]
        var_info = self.var_info(ctx, var_name)

        class_type = var_info["type"]

        if class_type not in self.classes:
            raise CompileError(ctx, "E0005", got=class_type, expected="class")

        cls = self.classes[class_type]

        field_name = parts[1].lower()

        if field_name not in cls.fields:
            raise CompileError(ctx, "E0001", name=parts[1])

        return var_info, cls.fields[field_name]
    
    def resolve_record_path(self, ctx, parts):
        var_name = parts[0]
        var_key  = var_name.lower()

        if var_key not in self.vars:
            raise CompileError(ctx, "E0001", name=var_name)

        var_info = self.vars[var_key]
        current_type = var_info["type"]

        if current_type not in self.records:
            raise CompileError(ctx, "E0005", got=current_type, expected="record")

        offset = var_info["slot"]
        field = None

        for field_name in parts[1:]:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=".".join(parts))

            field = record.fields[field_key]
            offset += field.offset
            current_type = field.type

            if field_name != parts[-1]:
                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        return offset, field

    def pascal_import_type(self, typ):
        typ = self.resolve_type(typ)

        if typ == "integer":
            return "Integer"

        if typ == "double":
            return "Double"

        if typ == "string":
            return "AnsiString"

        if isinstance(typ, str) and typ.startswith("^"):
            return "Pointer"

        return str(typ)

    def render_asm_export_thunks(self):
        out  = []
        seen = set()

        for item in self.exports:
            mangled = item["mangled"]

            if mangled in seen:
                continue
            seen.add(mangled)

            # normale Funktionen sind bereits direkt gemappt:
            # _ADD$INTEGER$INTEGER:
            if item.get("kind") == "function":
                continue

            # Prozeduren später genauso behandeln, wenn sie direkt gemappt sind
            if item.get("kind") == "procedure":
                continue

            if item.get("kind") != "class_method":
                continue

            class_name  = item["class_name"].lower()
            method_name = item["method_name"].lower()

            cls = self.classes[class_name]
            overloads = cls.methods[method_name]

            method = self.find_export_method_overload(
                None,
                overloads,
                [
                    self.resolve_type(p["type"])
                    for p in item.get("params", [])
                ]
            )

            target = method.label

            # Sicherheitsbremse gegen Selbstaufruf
            if target == mangled:
                continue

            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"{mangled}:" << std::endl;')
                out.append(f'{ASM_OUT_PH}"    call {target}" << std::endl;')
                out.append(f'{ASM_OUT_PH}"    ret" << std::endl << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'{mangled}:')
                out.append(f'    call {target}')
                out.append(f'    ret')

        return "\n".join(out)

    def render_import_params(self, params):
        if not params:
            return ""

        parts = []

        for p in params:
            prefix = "var " if p.get("is_var", False) else ""
            parts.append(
                f"{prefix}{p['name']}: {self.pascal_import_type(p['type'])}"
            )

        return "; ".join(parts)

    def render_call_args(self, params):
        return ", ".join(p["name"] for p in params)

    def render_external_decl(self, item):
        params = self.render_import_params(item.get("params", []))
        lines = []

        if item.get("return_type"):
            ret = self.pascal_import_type(item["return_type"])

            if params:
                lines.append(
                    f"function {item['name']}({params}): {ret}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
            else:
                lines.append(
                    f"function {item['name']}: {ret}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
        else:
            if params:
                lines.append(
                    f"procedure {item['name']}({params}); "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
            else:
                lines.append(
                    f"procedure {item['name']}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )

        return lines

    def render_class_external_decl(self, item, handle_type):
        lines = []

        raw_name = item["export_name"]
        params   = list(item.get("params", []))
        mk       = item["method_kind"].lower()

        if mk == "constructor":
            params_text = self.render_import_params(params)

            if params_text:
                lines.append(
                    f"function {raw_name}({params_text}): {handle_type}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )
            else:
                lines.append(
                    f"function {raw_name}: {handle_type}; "
                    f"external DLL_NAME name '{item['mangled']}';"
                )

            return lines

        if mk == "destructor":
            lines.append(
                f"procedure {raw_name}(Self: {handle_type}); "
                f"external DLL_NAME name '{item['mangled']}';"
            )
            return lines

        params_text = self.render_import_params(params)

        if params_text:
            params_text = "Self: " + handle_type + "; " + params_text
        else:
            params_text = "Self: " + handle_type

        if item.get("return_type"):
            ret = self.pascal_import_type(item["return_type"])
            lines.append(
                f"function {raw_name}({params_text}): {ret}; "
                f"external DLL_NAME name '{item['mangled']}';"
            )
        else:
            lines.append(
                f"procedure {raw_name}({params_text}); "
                f"external DLL_NAME name '{item['mangled']}';"
            )

        return lines

    def render_fpc_import_unit(self):
        lib_name  = self.program_name.lower()
        unit_name = "import_" + lib_name
        dll_name  = lib_name + ".dll"

        class_exports = {}
        normal_exports = []

        for item in self.exports:
            if item.get("kind") == "class_method":
                class_exports.setdefault(item["class_name"], [])
                class_exports[item["class_name"]].append(item)
            else:
                normal_exports.append(item)

        lines = []
        lines.append("{$mode objfpc}{$H+}")
        lines.append(f"unit {unit_name};")
        lines.append("")
        lines.append("interface")
        lines.append("")
        lines.append("const")
        lines.append(f"  DLL_NAME = '{dll_name}';")
        lines.append("")

        # normale Funktionen / Prozeduren
        for item in normal_exports:
            lines.extend(self.render_external_decl(item))
            lines.append("")

        # rohe Klassen-Imports
        for class_name, methods in class_exports.items():
            handle_type = class_name + "Handle"

            lines.append("type")
            lines.append(f"  {handle_type} = Pointer;")
            lines.append("")

            for item in methods:
                lines.extend(self.render_class_external_decl(item, handle_type))
                lines.append("")

        # Wrapper-Klassen
        if class_exports:
            lines.append("type")

        for class_name, methods in class_exports.items():
            handle_type = class_name + "Handle"

            lines.append(f"  {class_name} = class")
            lines.append("  private")
            lines.append(f"    FHandle: {handle_type};")
            lines.append("  public")

            for item in methods:
                mk = item["method_kind"].lower()

                if mk == "constructor":
                    params = self.render_import_params(item.get("params", []))
                    
                    if params:
                        lines.append(f"    constructor Create({params});")
                    else:
                        lines.append("    constructor Create;")
                
                elif mk == "destructor":
                    lines.append("    destructor Destroy; override;")
                
                elif mk == "function":
                    params = self.render_import_params(item.get("params", []))
                    ret = self.pascal_import_type(item["return_type"])

                    if params:
                        lines.append(f"    function {item['method_name']}({params}): {ret};")
                    else:
                        lines.append(f"    function {item['method_name']}: {ret};")

                elif mk == "procedure":
                    params = self.render_import_params(item.get("params", []))

                    if params:
                        lines.append(f"    procedure {item['method_name']}({params});")
                    else:
                        lines.append(f"    procedure {item['method_name']};")

            lines.append("  end;")
            lines.append("")

        lines.append("implementation")
        lines.append("")

        # Wrapper-Implementierungen
        for class_name, methods in class_exports.items():
            handle_type = class_name + "Handle"

            for item in methods:
                mk = item["method_kind"].lower()
                method_name = item["method_name"]
                export_name = item["export_name"]

                if mk == "constructor":
                    params = self.render_import_params(item.get("params", []))
                    call_args = self.render_call_args(item.get("params", []))

                    if params:
                        lines.append(f"constructor {class_name}.Create({params});")
                    else:
                        lines.append(f"constructor {class_name}.Create;")

                    lines.append("begin")
                    lines.append("  inherited Create;")

                    if call_args:
                        lines.append(f"  FHandle := {export_name}({call_args});")
                    else:
                        lines.append(f"  FHandle := {export_name};")

                    lines.append("end;")
                    lines.append("")

                elif mk == "destructor":
                    lines.append(f"destructor {class_name}.Destroy;")
                    lines.append("begin")
                    lines.append("  if FHandle <> nil then")
                    lines.append("  begin")
                    lines.append(f"    {export_name}(FHandle);")
                    lines.append("    FHandle := nil;")
                    lines.append("  end;")
                    lines.append("")
                    lines.append("  inherited Destroy;")
                    lines.append("end;")
                    lines.append("")

                elif mk == "function":
                    params = self.render_import_params(item.get("params", []))
                    ret = self.pascal_import_type(item["return_type"])
                    call_args = self.render_call_args(item.get("params", []))

                    if params:
                        lines.append(f"function {class_name}.{method_name}({params}): {ret};")
                    else:
                        lines.append(f"function {class_name}.{method_name}: {ret};")

                    lines.append("begin")

                    if call_args:
                        lines.append(f"  Result := {export_name}(FHandle, {call_args});")
                    else:
                        lines.append(f"  Result := {export_name}(FHandle);")

                    lines.append("end;")
                    lines.append("")

                elif mk == "procedure":
                    params = self.render_import_params(item.get("params", []))
                    call_args = self.render_call_args(item.get("params", []))

                    if params:
                        lines.append(f"procedure {class_name}.{method_name}({params});")
                    else:
                        lines.append(f"procedure {class_name}.{method_name};")

                    lines.append("begin")

                    if call_args:
                        lines.append(f"  {export_name}(FHandle, {call_args});")
                    else:
                        lines.append(f"  {export_name}(FHandle);")

                    lines.append("end;")
                    lines.append("")

        lines.append("begin")
        lines.append("end.")
        lines.append("")

        return "\n".join(lines)

    def write_fpc_import_unit(self):
        if self.module_kind != "library":
            return

        if not self.exports:
            return
        
        # todo !!!
        self.output_dir = "testout"
        
        imports_dir = os.path.join(
            self.output_dir,
            "imports"
        )
        
        os.makedirs(imports_dir, exist_ok=True)
        
        lib_name = self.program_name.lower()
        filename = os.path.join(
            imports_dir,
            f"import_{lib_name}.pas"
        )
        
        # todo !!!
        #print("WRITE IMPORT UNIT:", filename)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(self.render_fpc_import_unit())
    
    def resolve_pointer_record_path(self, ctx, parts):
        ptr_name = parts[0]
        ptr_key  = ptr_name.lower()

        ptr_info = self.find_local_var(ptr_name)
        is_local = ptr_info is not None

        if ptr_info is None:
            if ptr_key not in self.vars:
                raise CompileError(ctx, "E0001", name=ptr_name)

            ptr_info = self.vars[ptr_key]

        ptr_type = self.resolve_type(ptr_info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        record_type = ptr_type[1:]

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        offset = 0
        field = None
        current_type = record_type

        for field_name in parts[1:]:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=".".join(parts))

            field = record.fields[field_key]
            offset += field.offset
            current_type = self.resolve_type(field.type)

            if field_name != parts[-1]:
                if isinstance(current_type, str) and current_type.startswith("^"):
                    current_type = current_type[1:]

                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        ptr_info = dict(ptr_info)
        ptr_info["is_local"] = is_local
        ptr_info["type"] = ptr_type

        return ptr_info, offset, field
    
    def resolve_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)

        element_type = array_info.element_type

        if element_type not in self.records:
            raise CompileError(ctx, "E0005", got=element_type, expected="record array")

        # Index berechnen
        #index_type = self.visit(index_expr_ctx)
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        if not getattr(array_info, "is_dynamic", False):
            self.emit_array_bounds_check(ctx, var_name, array_info)

        if array_info.index_min != 0:
            self.emit_sub(REG_EAX, array_info.index_min)

        self.emit_imul(REG_EAX, REG_EAX, array_info.element_size)
        self.emit_add (REG_EAX, var_info["slot"])

        # Array-Basis holen
        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd(REG_RAX, REG_EAX)
        self.emit_add("r11", REG_RAX)

        # Jetzt zeigt R11 auf points[index]
        current_type = element_type
        field = None
        field_offset = 0

        for field_name in field_parts:
            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[field_key]
            field_offset += field.offset
            current_type = field.type

            if field_name != field_parts[-1]:
                if current_type not in self.records:
                    raise CompileError(ctx, "E0005", got=current_type, expected="record")

        if field_offset != 0:
            self.emit_add("r11", field_offset)

        return field
    
    def resolve_type(self, type_name):
        if not isinstance(type_name, str):
            return type_name

        typ = type_name.lower()

        if typ.startswith("^"):
            base = typ[1:]
            
            while base in self.type_aliases:
                base = self.type_aliases[base].lower()
                
                if base.startswith("^"):
                    return base
                    
            return "^" + base

        while typ in self.type_aliases:
            typ = self.type_aliases[typ].lower()

        if typ == "boolean":
            return "integer"
        
        if typ in self.enums:
            return "integer"

        if isinstance(typ, str) and typ in self.records:
            return typ

        if isinstance(typ, str) and typ in self.arrays:
            return typ

        return typ
    
    def load_unit(self, ctx, unit_name):
        unit_key = unit_name.lower()

        if unit_key in self.loaded_units:
            return

        if unit_key in self.loading_units:
            raise CompileError(
                ctx,
                "E0019",
                text=f"circular unit reference detected: {unit_name}"
            )

        unit_file = self.find_unit_file(ctx, unit_name)

        self.loading_units.add(unit_key)

        old_source_file = self.source_file
        old_source_dir  = self.source_dir
        old_unit        = self.current_unit

        self.source_file  = unit_file
        self.source_dir   = os.path.dirname(unit_file)
        self.current_unit = unit_key

        stream = FileStream(unit_file, encoding="utf-8")
        lexer  = MiniPascalLexer(stream)
        tokens = CommonTokenStream(lexer)
        parser = MiniPascalParser(tokens)

        tree = parser.sourceFile()

        if parser.getNumberOfSyntaxErrors() > 0:
            raise CompileError(
                ctx,
                "E0019",
                text=f"syntax error in unit {unit_name}"
            )

        self.visit(tree)

        self.current_unit = old_unit
        self.source_file  = old_source_file
        self.source_dir   = old_source_dir

        self.loading_units.remove(unit_key)
        self.loaded_units[unit_key] = unit_file

    def find_current_class_field(self, name):
        if self.current_class is None:
            return None

        cls = self.classes[self.current_class]
        key = name.lower()

        if key not in cls.fields:
            return None

        return cls.fields[key]
    
    def find_export_method_overload(self, ctx, overloads, wanted_types):
        for method in overloads:
            method_types = [
                self.resolve_type(p["type"])
                for p in method.params
            ]

            if method_types == wanted_types:
                return method

        raise CompileError(
            ctx,
            "E0019",
            text=f"export overload not found"
        )
    
    def export_wrapper_suffix(self, params):
        if not params:
            return ""

        return "_" + "_".join(
            self.pascal_import_type(p["type"])
            for p in params
        ).replace(" ", "")

    def find_export_function_overload(self, name, wanted_types):
        key = name.lower()

        if key not in self.functions:
            return None

        func = self.functions[key]

        func_types = [
            self.resolve_type(p["type"])
            for p in func.get("params", [])
        ]

        if func_types == wanted_types:
            return func

        return None
    
    def find_unit_file(self, ctx, unit_name):
        candidates = [
            unit_name + ".pas",
            unit_name + ".pp",
            unit_name.lower() + ".pas",
            unit_name.lower() + ".pp"
        ]
        
        search_dirs = []
        
        if self.source_dir:
            search_dirs.append(self.source_dir)
        
        search_dirs.append(os.getcwd())
        
        for directory in search_dirs:
            for filename in candidates:
                path = os.path.abspath(os.path.join(directory, filename))
                
                if os.path.exists(path):
                    return path
        
        raise CompileError(
            ctx,
            "E0019",
            text=f"unit {unit_name} not found"
        )
    
    def find_const(self, name):
        key = name.lower()

        for scope in reversed(self.local_const_stack):
            if key in scope:
                return scope[key]

        if key in self.constants:
            return self.constants[key]

        return None
    
    def find_function(self, name):
        for i in range(len(self.scope_stack), -1, -1):
            scoped = "_".join(self.scope_stack[:i] + [name])
            key = scoped.lower()

            if key in self.functions:
                return self.functions[key]

        return None
    
    def find_param(self, name):
        key = name.lower()

        if key in self.current_proc_params:
            return self.current_proc_params[key]

        return None
    
    def find_local_var(self, name):
        key = name.lower()

        for scope in reversed(self.local_var_stack):
            if key in scope["vars"]:
                return scope["vars"][key]

        return None
    
    def find_class_method_export(self, qualified_name):
        parts = qualified_name.split(".")

        if len(parts) != 2:
            return None

        class_name  = parts[0]
        method_name = parts[1]

        cls = self.classes.get(class_name.lower())

        if not cls:
            return None

        for m in cls.methods:
            if m.name.lower() == method_name.lower():
                return cls, m

        return None
    
    def find_class_method_overload(self, ctx, cls, method_name, actual_types):
        key = method_name.lower()
        
        if key not in cls.methods:
            raise CompileError(
                ctx,
                "E0019",
                text=f"class {cls.name} has no method {method_name}"
            )
        
        candidates = cls.methods[key]
        
        for method in candidates:
            params = method.params
            
            if len(params) != len(actual_types):
                continue
            
            ok = True
            
            for p, actual_type in zip(params, actual_types):
                formal_type = self.resolve_type(p["type"])
                
                if formal_type != actual_type:
                    ok = False
                    break
            
            if ok:
                return method
        
        raise CompileError(
            ctx,
            "E0019",
            text = f"no matching overload for {cls.name}.{method_name}"
        )
    
    def find_class_method_recursive(self, ctx, class_name, method_name, actual_types):
        if isinstance(class_name, ClassInfo):
            class_key = class_name.name.lower()
        else:
            class_key = class_name.lower()
        
        if class_key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_name)
        
        cls = self.classes[class_key]
        method_key = method_name.lower()
        
        if method_key in cls.methods:
            for method in cls.methods[method_key]:
                params = method.params
                
                if len(params) != len(actual_types):
                    continue
                
                ok = True
                
                for p, actual_type in zip(params, actual_types):
                    formal_type = self.resolve_type(p["type"])
                    
                    if formal_type != actual_type:
                        ok = False
                        break
                
                if ok:
                    return method, cls
        
        if cls.parent:
            return self.find_class_method_recursive(
                ctx,
                cls.parent,
                method_name,
                actual_types
            )
        
        raise CompileError(
            ctx,
            "E0019",
            text=f"no matching inherited overload for {class_name}.{method_name}"
        )
    
    def get_record_field(self, ctx, var_name, field_name):
        var_key   = var_name.lower()
        field_key = field_name.lower()

        if var_key not in self.vars:
            raise CompileError(ctx, "E0001", name=var_name)

        var_info = self.vars[var_key]
        record_type = var_info["type"]

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        record = self.records[record_type]

        if field_key not in record.fields:
            raise CompileError(ctx, "E0001", name=f"{var_name}.{field_name}")

        return var_info, record.fields[field_key]
    
    def get_array_info(self, ctx, var_name):
        key = var_name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=var_name)

        var_info = self.vars[key]
        array_type = var_info["type"]

        if array_type not in self.arrays:
            raise CompileError(ctx, "E0005", got=array_type, expected="array")

        return var_info, self.arrays[array_type]
        
    def collect_formal_params(self, ctx):
        params = []

        if not ctx.formalParamList():
            return params

        for p in ctx.formalParamList().formalParam():
            typ = self.resolve_type(p.typeName().getText())
            is_var = p.VAR() is not None

            for ident in p.identList().IDENT():
                params.append({
                    "name": ident.getText(),
                    "type": typ,
                    "is_var": is_var
                })

        return params
    
    def scoped_name(self, name):
        if self.scope_stack:
            return "_".join(self.scope_stack + [name])
        return name

    def variable_ref_has_caret(self, ref):
        return any(s.CARET() for s in ref.variableSuffix())
    
    def add_asm_label_mapping(self, asmjit_label, target_label):
        self.asm_label_mappings.append({
            "asmjit": asmjit_label,
            "target": target_label
        })
    
    def fpc_mangle_type(self, typ):
        typ = self.resolve_type(typ)

        if typ == "integer":
            return "INTEGER"

        if typ == "double":
            return "DOUBLE"

        if typ == "string":
            return "ANSISTRING"

        if isinstance(typ, str) and typ.startswith("^"):
            return "POINTER"

        return str(typ).upper()

    def fpc_mangle_params(self, params):
        if not params:
            return ""

        return "".join(
            "$" + self.fpc_mangle_type(p["type"])
            for p in params
        )

    def fpc_mangle_unit(self, unit_name):
        return self.normalize_unit_name(unit_name).upper()

    def fpc_mangle_routine(self, name, params=None, unit_name=None):
        params = params or []

        routine = name.upper()
        suffix  = self.fpc_mangle_params(params)

        if unit_name:
            unit = self.fpc_mangle_unit(unit_name)
            return f"_{unit}$$_{routine}{suffix}"

        if self.current_unit:
            unit = self.fpc_mangle_unit(self.current_unit)
            return f"_{unit}$$_{routine}{suffix}"

        return f"_{routine}{suffix}"

    def fpc_mangle_class_method(self, class_name, method_name, params=None, unit_name=None):
        params = params or []

        cls    = class_name.upper()
        method = method_name.upper()
        suffix = self.fpc_mangle_params(params)

        if unit_name:
            unit = self.fpc_mangle_unit(unit_name)
            return f"_{unit}$$_$$_{cls}_$$_{method}{suffix}"

        if self.current_unit:
            unit = self.fpc_mangle_unit(self.current_unit)
            return f"_{unit}$$_$$_{cls}_$$_{method}{suffix}"

        return f"_$$_{cls}_$$_{method}{suffix}"
    
    def emit_class_constructor_call(self, ctx, class_name, method_name):
        class_key = class_name.lower()
        
        if class_key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_name)
        
        cls = self.classes[class_key]
        
        args = self.function_call_args(ctx)
        
        actual_types = []
        
        # Argumente auswerten und pushen
        for arg in reversed(args):
            arg_type = self.visit(arg)
            actual_types.insert(0, arg_type)
            
            if arg_type == "integer":
                self.emit_movsxd(REG_RAX, REG_EAX)
                self.emit_push(REG_RAX, comment='ctor integer arg')
            
            elif arg_type == "string":
                self.emit_push(REG_RAX, comment='ctor string arg')
            
            elif isinstance(arg_type, str) and arg_type.startswith("^"):
                self.emit_push(REG_RAX, comment='ctor pointer arg')
            
            else:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"unsupported constructor argument type {arg_type}"
                )
        
        method, owner_cls = self.find_class_method_recursive(
            ctx,
            cls,
            method_name,
            actual_types
        )
        
        size = cls.size
        
        self.emit_mov("rcx", size)
        self.emit_mov_imm("rax", "&_jit_new_memory")
        self.emit_call("rax")
        
        param_regs = ["rdx", "r8", "r9"]
        
        # Self zuerst setzen, aber NICHT sofort pushen
        self.emit_mov("rcx", "rax", comment="self") # "a.mov(x86::rcx, x86::rax); // Self")
        
        # Constructor-Parameter aus dem temporären Stack holen
        for index in range(len(args)):
            self.emit_pop(f"{param_regs[index]}", comment="ctor arg {index + 1}")
            #self.emit(f"a.pop(x86::{param_regs[index]});")
        
        # Self über den Call retten
        self.emit_push("rcx", comment="save constructor result object")
        
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label)
        self.emit_add("rsp", 32)
        self.emit_pop("rax", comment = "constructor result")
        
        return class_key
    
    def emit_class_free_call(self, ctx, obj_name):
        info = self.var_info(ctx, obj_name)
        class_type = info["type"]

        if class_type not in self.classes:
            raise CompileError(ctx, "E0005", got=class_type, expected="class")

        cls = self.classes[class_type]

        self.emit_load_object_var(ctx, obj_name, info)

        null_label = self.new_named_label("free_nil")
        end_label  = self.new_named_label("free_end")

        self.emit_test("rax", "rax")
        self.emit_jz(null_label)

        self.emit_push("rax", comment='save object for dispose')

        if "destroy" in cls.methods:
            method, owner_cls = self.find_class_method_recursive(
                ctx,
                class_type,
                "Destroy",
                []
            )
            
            self.emit_mov("rcx", "rax", comment='Self')
            self.emit_sub("rsp", 32)
            self.emit_call_lbl(method.label)
            self.emit_add("rsp", 32)

        self.emit_pop("rcx")
        self.emit_mov_imm("rax", "&_jit_dispose_memory")
        self.emit_call("rax")

        # foo := nil
        self.emit_xor("rax", "rax")
        self.emit_store_object_var(ctx, obj_name, info)

        self.emit_jmp(end_label)
        self.emit_bind_label(null_label)
        self.emit_bind_label(end_label)

        return None
    
    def emit_soft_runtime_error(self, message):
        except_label = self.current_except_label()

        if except_label is None:
            label = self.add_string_literal(message)
            self.emit_mov_imm("rcx", label)
            self.emit_mov_imm("rax", "&_jit_runtime_error")
            self.emit_call("rax")
            return

        label = self.add_string_literal(message)

        self.emit_mov("rcx", "r12", comment='ctx')
        self.emit_mov_imm("rdx", label)
        self.emit_mov_imm("rax", "&_jit_set_exception")
        self.emit_call("rax")
        self.emit_jmp(except_label)
    
    def emit_nil_pointer_check(self, ptr_name):
        ok_label = self.new_named_label("ptr_not_nil")
        name_label = self.add_string_literal(ptr_name)

        self.emit_test("rax", "rax")
        self.emit_jnz(ok_label)

        self.emit_soft_runtime_error(
            f"Nil pointer error: {ptr_name}"
        )

        self.emit_bind_label(ok_label)
    
    def emit_builtin_debug_break(self):
        self.emit_mov_imm("rax", "&_jit_debug_break")
        self.emit_call("rax")
        return None
    
    def emit_builtin_readln(self, ctx):
        actuals = []

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        ref = self.actual_param_variable_ref(ctx, actuals[0])
        name = ref.IDENT().getText()

        info = self.find_local_var(name)
        is_local = info is not None

        if info is None:
            info = self.var_info(ctx, name)

        typ = self.resolve_type(info["type"])

        if typ == "integer":
            self.emit_mov_imm("rax", "&_jit_read_int")
            self.emit_call("rax")

            if is_local:
                self.emit_store_local_var(ctx, name, "integer")
            else:
                self.emit_store_var(ctx, name, info)

            return None

        if typ == "string":
            self.emit_mov_imm("rax", "&_jit_read_string")
            self.emit_call("rax")

            if is_local:
                self.emit_store_local_var(ctx, name, "string")
            else:
                self.emit_store_var(ctx, name, info)

            return None

        raise CompileError(
            ctx,
            "E0005",
            got=typ,
            expected="integer/string"
        )
    
    def emit_builtin_assigned(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 1:
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="1")

        expr_type = self.visit(args[0])

        if not isinstance(expr_type, str) or not expr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=expr_type, expected="pointer")

        self.emit_test (REG_RAX, REG_RAX)
        self.emit_setne(REG_AL)
        self.emit_movzx(REG_EAX, REG_AL)

        return "integer"
    
    def emit_builtin_new(self, ctx):
        actuals = []

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        ref  = self.actual_param_variable_ref(ctx, actuals[0])

        name = ref.IDENT().getText()
        info = self.find_local_var(name)
        
        is_local = info is not None

        if info is None:
            info = self.var_info(ctx, name)

        ptr_type = self.resolve_type(info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        base_type = ptr_type[1:]
        size = self.type_size(ctx, base_type)

        self.emit_mov("rcx", size)
        self.emit_mov_imm("rax", "&_jit_new_memory")
        self.emit_call("rax")

        if is_local:
            self.emit_store_local_var(ctx, name, ptr_type)
        else:
            self.emit_store_var(ctx, name, info)
        
        return None
    
    def emit_builtin_length(self, ctx):
        actuals = []

        if ctx.argumentList():
            actuals = list(ctx.argumentList().expr())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        expr_type = self.visit(actuals[0])

        if expr_type != "string":
            raise CompileError(ctx, "E0005", got=expr_type, expected="string")

        self.emit_mov("rcx", "rax")
        self.emit_mov_imm("rax", "&_jit_dynstring_length")
        self.emit_call("rax")

        return "integer"
    
    def emit_builtin_setlength(self, ctx):
        actuals = []

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 2:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="2")

        target_ctx = actuals[0].expr()
        length_ctx = actuals[1].expr()

        name = target_ctx.getText()

        local_var = self.find_local_var(name)

        if local_var:
            var_type = local_var["type"]
        else:
            var_info = self.var_info(ctx, name)
            var_type = var_info["type"]

        if var_type == "string":
            self.emit_builtin_string_setlength(ctx, name, length_ctx)
            return None

        if isinstance(var_type, str) and var_type in self.arrays:
            array_info = self.arrays[var_type]

            if getattr(array_info, "is_dynamic", False):
                self.emit_builtin_array_setlength(ctx, name, length_ctx)
                return None

        raise CompileError(
            ctx,
            "E0014",
            var_type="SetLength only supports dynamic arrays and strings"
        )
    
    def function_call_args(self, ctx):
        if hasattr(ctx, "actualParamList") and ctx.actualParamList():
            return list(ctx.actualParamList().actualParam())

        if hasattr(ctx, "argumentList") and ctx.argumentList():
            return list(ctx.argumentList().expr())

        if hasattr(ctx, "expr"):
            exprs = ctx.expr()
            if isinstance(exprs, list):
                return list(exprs)
            if exprs:
                return [exprs]

        return []
        
    # ----------------------------------------
    # rcx = Quellstring
    # rdx = Startposition
    # r8  = Anzahl
    # rax = neuer DynString
    # ----------------------------------------
    def emit_builtin_copy(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 3:
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="3")

        t1 = self.visit(args[0])
        if t1 != "string":
            raise CompileError(ctx, "E0005", got=t1, expected="string")

        self.emit_push("rax", comment='Copy source')

        t2 = self.visit(args[1])
        if t2 != "integer":
            raise CompileError(ctx, "E0005", got=t2, expected="integer")

        self.emit_movsxd(REG_RAX, REG_EAX)
        self.emit_push  (REG_RAX, comment='Copy start')

        t3 = self.visit(args[2])
        if t3 != "integer":
            raise CompileError(ctx, "E0005", got=t3, expected="integer")

        self.emit_movsxd(REG_RAX, REG_EAX)
        self.emit_push  (REG_RAX, comment='Copy count')

        self.emit_pop("r8")
        self.emit_pop(REG_RBX)
        self.emit_pop(REG_RCX)

        self.emit_sub     (REG_RSP, 32)
        self.emit_mov_imm (REG_RAX, "&_jit_dynstring_copy")
        self.emit_call    (REG_RAX)
        self.emit_add     (REG_RSP, 32)

        return "string"
    
    # ----------------------------------------
    # rcx = Suchstring
    # rdx = Quellstring
    # eax = Position oder 0
    # ----------------------------------------
    def emit_builtin_pos(self, ctx):
        args = self.function_call_args(ctx)

        if len(args) != 2:
            raise CompileError(ctx, "E0005", got=str(len(args)), expected="2")

        t1 = self.visit(args[0])
        if t1 != "string":
            raise CompileError(ctx, "E0005", got=t1, expected="string")

        self.emit_push(REG_RAX, comment='Pos needle')

        t2 = self.visit(args[1])
        if t2 != "string":
            raise CompileError(ctx, "E0005", got=t2, expected="string")

        self.emit_push("rax", comment='Pos haystack')

        self.emit_pop(REG_RDX)
        self.emit_pop(REG_RCX)

        self.emit_sub     (REG_RSP, 32)
        self.emit_mov_imm (REG_RAX, "&_jit_dynstring_pos")
        self.emit_call    (REG_RAX)
        self.emit_add     (REG_RSP, 32)

        return "integer"
    
    def add_double_literal(self, value):
        value_text = str(value)

        safe = (
            value_text
            .replace(".", "_")
            .replace("-", "minus_")
        )

        name = f"dbl_{safe}_{len(self.double_literals)}"
        self.double_literals.append((name, value_text))
        return name
    
    def emit_builtin_dispose(self, ctx):
        actuals = []

        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())

        if len(actuals) != 1:
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected="1")

        ref = self.actual_param_variable_ref(ctx, actuals[0])

        name = ref.IDENT().getText()

        info = self.find_local_var(name)
        if info is None:
            info = self.var_info(ctx, name)

        ptr_type = self.resolve_type(info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        is_local = self.find_local_var(name) is not None

        if is_local:
            self.emit_load_local_var(ctx, name, info)
        else:
            self.emit_load_var(name, info)

        self.emit_mov("rcx", "rax")
        self.emit_mov_imm("rax", "&_jit_dispose_memory")
        self.emit_call("rax")

        self.emit_xor("rax", "rax")

        if is_local:
            self.emit_store_local_var(ctx, name, ptr_type)
        else:
            self.emit_store_var(ctx, name, info)

        return None

    def emit_builtin_array_setlength(self, ctx, name, length_ctx):
        var_info = self.var_info(ctx, name)
        array_info = self.arrays[var_info["type"]]

        self.visit(length_ctx)

        self.emit_movsxd("rdx", "eax")
        self.emit_mov("r8", array_info.element_size)

        self.emit_load_var(name, var_info)
        self.emit_mov("rcx", "rax")

        self.emit_mov_imm("rax", "&_jit_dynarray_setlength")
        self.emit_call("rax")

        self.emit_store_var(ctx, name, var_info)
    
    def emit_multi_array_index_offset(self, ctx, var_name, array_info, index_exprs):
        dims = array_info.dimensions

        if len(index_exprs) != len(dims):
            raise CompileError(
                ctx,
                "E0005",
                got=str(len(index_exprs)),
                expected=str(len(dims))
            )

        self.emit_xor("ebx", "ebx", comment="linear array index")

        for i, expr in enumerate(index_exprs):
            index_type = self.visit(expr)

            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            dim = dims[i]

            self.emit_array_bounds_check_dimension(
                ctx,
                var_name,
                dim["min"],
                dim["max"]
            )

            if dim["min"] != 0:
                self.emit_sub("eax", dim["min"])

            factor = 1
            for next_dim in dims[i + 1:]:
                factor *= next_dim["max"] - next_dim["min"] + 1

            if factor != 1:
                self.emit_imul("eax", "eax", factor)

            self.emit_add("ebx", "eax")

        #self.emit_mov("eax", "ebx", comment='final linear index')
        self.emit_mov_eax_ebx()

    def emit_array_bounds_check_dimension(self, ctx, var_name, min_value, max_value):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        array_label = self.add_string_literal(var_name)

        self.emit_mov("r10d", "eax", comment = "// save dimension index")

        self.emit_cmp("eax", min_value)
        self.emit_jl(fail_label)

        self.emit_cmp("eax", max_value)
        self.emit_jg(fail_label)

        self.emit_jmp(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rcx", array_label)
        self.emit_mov("edx", "r10d")
        self.emit_mov("r8d", min_value)
        self.emit_mov("r9d", max_value)
        self.emit_mov_imm("rax", "&_jit_array_bounds_error")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)
        self.emit_mov("eax", "r10d", comment = "restore dimension index")
    
    def emit_array_bounds_check_for_dimension(self, dim):
        min_value = dim["min"]
        max_value = dim["max"]

        self.emit_push("rax")

        self.emit_cmp("eax", min_value)
        self.emit_jl("array_bounds_error")

        self.emit_cmp("eax", max_value)
        self.emit_jg("array_bounds_error")

        self.emit_pop("rax")
    
    def emit_address_of_var(self, ctx, name):
        local_var = self.find_local_var(name)

        if local_var:
            typ    = local_var["type"]
            offset = local_var["offset"]

            if typ == "integer":
                self.emit_lea_dword("rax", "rbp", offset, comment = "@{name}")
                return "^integer"

            if typ == "double":
                self.emit_lea_qword("rax", "rbp", offset, comment = "@{name}")
                return "^double"

            if typ == "string":
                self.emit_lea_qword("rax", "rbp", offset, comment = "@{name}")
                return "^string"

            if isinstance(typ, str) and typ.startswith("^"):
                self.emit_lea_qword("rax", "rbp", offset, comment = "@{name}")
                return "^" + typ

            if isinstance(typ, str) and typ in self.records:
                self.emit_lea_byte("rax", "rbp", offset, comment = "@{name}")
                return "^" + typ

            if isinstance(typ, str) and typ in self.arrays:
                self.emit_lea_byte("rax", "rbp", offset, comment = "@{name}")
                return "^" + typ

            raise CompileError(ctx, "E0014", var_type=typ)

        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ  = info["type"]
        slot = info["slot"]

        if typ == "integer":
            self.emit_mov_qword("rax", "r12", "int_vars")
            self.emit_add("rax", slot * 4, comment=f"@{name}")
            return "^integer"

        if typ == "double":
            self.emit_mov_qword("rax", "r12", "double_vars")
            self.emit_add("rax", slot * 8, comment=f"@{name}")
            return "^double"

        if typ == "string":
            self.emit_mov_qword("rax", "r12", "string_vars")
            self.emit_add("rax", slot * 8, comment=f"@{name}")
            return "^string"

        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword("rax", "r12", "pointr_vars")
            self.emit_add("rax", slot * 8, comment=f"@{name}")
            return "^" + typ

        if isinstance(typ, str) and typ in self.records:
            self.emit_mov_qword("rax", "r12", "record_vars")
            self.emit_add("rax", slot, comment=f"@{name}")
            return "^" + typ

        if isinstance(typ, str) and typ in self.arrays:
            self.emit_mov_qword("rax", "r12", "arrays_vars")
            self.emit_add("rax", slot, comment=f"@{name}")
            return "^" + typ

        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_address_of_array_element(self, ctx, var_name, index_exprs):
        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("rax", "r11", comment="@array[index]")

        return "^" + array_info.element_type
        
    def emit_array_bounds_check(self, ctx, var_name, array_info):
        ok_label    = self.new_named_label("array_bounds_ok")
        fail_label  = self.new_named_label("array_bounds_fail")
        array_label = self.add_string_literal(var_name)

        # Originalindex in EBX sichern
        self.emit_mov("ebx", "eax", comment = "save array index")

        self.emit_cmp("eax", array_info.index_min)
        self.emit_jl(fail_label)

        self.emit_cmp("eax", array_info.index_max)
        self.emit_jg(fail_label)

        self.emit_jmp(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rcx", array_label)
        self.emit_mov("edx", "ebx")
        self.emit_mov("r8d", array_info.index_min)
        self.emit_mov("r9d", array_info.index_max)
        self.emit_mov_imm("rax", "&_jit_array_bounds_error")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)

        # Index wiederherstellen
        self.emit_mov("eax", "ebx", comment='restore array index')
    
    def emit_load_self_field(self, ctx, name):
        if self.current_class is None:
            return None

        cls = self.classes[self.current_class]
        key = name.lower()

        if key not in cls.fields:
            return None

        field = cls.fields[key]

        self.emit_mov_qword_ptr("rax", "rbp", -8, comment='Self')

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "rax", field.offset, comment=f"Self.{name}")
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "rax", field.offset, comment=f"Self.{name}")
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"Self.{name}")
            return "string"

        return field.type
    
    def emit_load_object_var(self, ctx, name, info):
        slot = info["slot"]

        self.emit_mov_qword("rax", "r12", "pointr_vars")
        self.emit_mov_qword_ptr("rax", "rax", slot * 8, comment=f"object {name}")
    
    def emit_load_string_char(self, ctx, name, index_exprs):
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
        
        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")
        
        index_type = self.visit(index_exprs[0])
        
        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")
        
        self.emit_sub("eax", 1)
        self.emit_mov("r10d", "eax")
        
        var_info = self.var_info(ctx, name)
        self.emit_load_var(name, var_info)
        
        self.emit_movsxd("r11", "r10d")
        self.emit_add("r11", "rax")
        self.emit_movzx("eax", "byte_ptr(r11)")
        
        return "char"
    
    def emit_load_class_field(self, ctx, parts):
        var_info, field = self.resolve_class_field_path(ctx, parts)

        path = ".".join(parts)

        self.emit_load_object_var(ctx, parts[0], var_info)
        self.emit_nil_pointer_check(parts[0])

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "rax", field.offset, comment=f"{path}")
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "rax", field.offset, comment=path)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"{path}")
            return "string"

        return field.type
    
    def emit_load_const(self, ctx, name):
        c = self.find_const(name)

        if not c:
            raise CompileError(ctx, "E0001", name=name)

        typ = c["type"]
        val = c["value"]

        if typ == "integer":
            self.emit_mov("eax", val)
            return "integer"

        if typ == "double":
            return self.emit_load_double_literal(val)

        if typ == "string":
            label = self.add_string_literal(val)
            self.emit_mov_imm("rax", label)
            return "string"

        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_load_double_literal(self, value):
        value_text = str(value)

        self.add_double_literal(value_text)

        self.emit_mov_imm("rax", double_to_bits(float(value_text)))
        self.emit_movq("xmm0", "rax")

        return "double"
    
    def emit_load_string_var_to_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rax", "r12", "string_vars")
        self.emit_mov_qword_ptr("rax", "rax", slot * 8)
    
    def emit_load_pointer_var_to_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rax", "r12", "pointr_vars")
        self.emit_mov_qword_ptr("rax", "rax", slot * 8)
    
    def emit_load_pointer_deref(self, ctx, name):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ = info["type"]

        if not isinstance(typ, str) or not typ.startswith("^"):
            raise CompileError(ctx, "E0005", got=typ, expected="pointer")

        base_type = typ[1:]

        self.emit_load_var(name, info)

        if base_type == "integer":
            self.emit_mov_reg_dword("eax", "rax", comment='p^')
            return "integer"

        if base_type == "double":
            self.emit_movsd_load("xmm0", "rax", 0, comment="p^")
            return "double"

        if base_type == "string":
            self.emit_mov_reg_qword("rax", "rax", comment='p^')
            return "string"

        raise CompileError(ctx, "E0014", var_type=base_type)
    
    def emit_load_param(self, ctx, name):
        param = self.find_param(name)

        if not param:
            raise CompileError(ctx, "E0001", name=name)
            
        typ    = self.resolve_type(param["type"])
        offset = param["stack_offset"]
        
        if param.get("is_var", False):
            self.emit_mov_qword_ptr("r11", "rbp", offset, comment=f"var param address {name}")
            
            if typ == "integer":
                self.emit_mov_reg_dword("eax", "r11")
                return "integer"
            
            if isinstance(typ, str) and typ.startswith("^"):
                self.emit_mov_reg_qword("rax", "r11")
                return typ
            
            raise CompileError(ctx, "E0014", var_type=typ)
        
        if typ == "integer":
            self.emit_mov_dword_ptr("eax", "rbp", offset)
            return "integer"
        
        if typ == "string":
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return "string"
        
        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword_ptr("rax", "rbp", offset)
            return typ
            
        raise CompileError(ctx, "E0014", var_type=typ)
    
    def emit_load_record_field(self, ctx, parts):
        field_offset, field = self.resolve_record_path(ctx, parts)
        path = ".".join(parts)

        self.emit_mov_qword("r11", "r12", "record_vars")

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "r11", field_offset, comment=f"{path}")
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "r11", field_offset, comment=path)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "r11", field_offset, comment=f"{path}")
            return "string"

        return field.type
    
    def emit_load_pointer_record_field(self, ctx, parts):
        ptr_name = parts[0]
        ptr_key  = ptr_name.lower()

        ptr_info = self.find_local_var(ptr_name)
        is_local = ptr_info is not None

        if ptr_info is None:
            if ptr_key not in self.vars:
                raise CompileError(ctx, "E0001", name=ptr_name)

            ptr_info = self.vars[ptr_key]

        ptr_type = self.resolve_type(ptr_info["type"])

        if not isinstance(ptr_type, str) or not ptr_type.startswith("^"):
            raise CompileError(ctx, "E0005", got=ptr_type, expected="pointer")

        current_type = ptr_type[1:]

        # Startpointer laden: n1
        if is_local:
            self.emit_load_local_var(ctx, ptr_name, ptr_info)
        else:
            self.emit_load_var(ptr_name, ptr_info)
            
        self.emit_nil_pointer_check(ptr_name)
        
        for index, field_name in enumerate(parts[1:]):
            if current_type not in self.records:
                raise CompileError(ctx, "E0005", got=current_type, expected="record")

            record = self.records[current_type]
            field_key = field_name.lower()

            if field_key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[field_key]
            is_last = index == len(parts[1:]) - 1

            if is_last:
                if field.type == "integer":
                    self.emit_mov_dword_ptr("eax", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return "integer"

                if field.type == "double":
                    self.emit_movsd_load("xmm0", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return "double"

                if field.type == "string":
                    self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return "string"

                if field.type.startswith("^"):
                    self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"{'.'.join(parts)}")
                    return field.type

                return field.type

            # Weiter in der Kette:
            # Next ist Pointer -> Pointerwert laden
            if field.type.startswith("^"):
                self.emit_mov_qword_ptr("rax", "rax", field.offset, comment=f"follow pointer {field_name}")
                current_type = field.type[1:]
                continue

            # eingebetteter Record
            if field.type in self.records:
                if field.offset != 0:
                    self.emit_add("rax", field.offset, comment=f"nested record {field_name}")
                current_type = field.type
                continue

            raise CompileError(ctx, "E0005", got=field.type, expected="record/pointer")
    
    def emit_load_local_var(self, ctx, name, info):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name=name)

        typ    = var["type"]
        offset = var["offset"]

        if typ == "integer":
            self.emit_mov_dword_ptr("eax", "rbp", offset, comment=f"local {name}")
            return "integer"

        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword_ptr("rax", "rbp", offset, comment=f"local pointer {name}")
            return typ

        raise CompileError(ctx, "E0011", typ=typ)

    def emit_builtin_string_setlength(self, ctx, name, length_ctx):
        self.visit(length_ctx)
        self.emit_movsxd("rdx", "eax")
        self.emit_load_string_var_to_rax(ctx, name)
        self.emit_mov("rcx", "rax")
        self.emit_mov_imm("rax", "&_jit_dynstring_setlength")
        self.emit_call("rax")
        self.emit_store_string_var_from_rax(ctx, name)
    
    def emit_store_self_field(self, ctx, name, expr_type):
        field = self.find_current_class_field(name)

        if field is None:
            return False

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if expr_type == "integer":
            self.emit_mov("ebx", "eax")
            self.emit_mov_qword_ptr("rax", "rbp", -8, comment='Self')
            self.emit_mov_dword_ptr_store("rax", field.offset, "ebx", comment=f"Self.{name} :=")
            return True

        if expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")
            self.emit_mov_qword_ptr("rax", "rbp", -8, comment='Self')
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", field.offset, "xmm0", comment=f"Self.{name} :=")
            return True

        if expr_type == "string":
            self.emit_push("rax")
            self.emit_mov_qword_ptr("rax", "rbp", -8, comment='Self')
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", field.offset, "r11", comment=f"Self.{name} :=")
            return True

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_object_var(self, ctx, name, info):
        slot = info["slot"]

        self.emit_mov_qword("r11", "r12", "pointr_vars")
        self.emit_mov_qword_ptr_store("r11", slot * 8, "rax", comment=f"object {name}")
    
    def emit_store_class_field(self, ctx, parts, expr_type):
        var_info, field = self.resolve_class_field_path(ctx, parts)
        
        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)
        
        # rechten Wert sichern, bevor RAX für Objektpointer benutzt wird
        if expr_type == "integer":
            self.emit_mov("ebx", "eax", comment='save class field value')
        
        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")
        
        elif expr_type == "string":
            self.emit_push("rax", comment='save string field value')
        
        else:
            raise CompileError(ctx, "E0013", var_type=field.type)
        
        self.emit_load_object_var(ctx, parts[0], var_info)
        self.emit_nil_pointer_check(parts[0])
        
        if field.type == "integer":
            self.emit_mov_dword_ptr_store("rax", field.offset, "ebx", comment=f"{'.'.join(parts)} :=")
            return
        
        if field.type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", field.offset, "xmm0", comment=f"{'.'.join(parts)} :=")
            return
        
        if field.type == "string":
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", field.offset, "r11", comment=f"{'.'.join(parts)} :=")
            return
        
        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_string_var_from_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rdx", "r12", "string_vars")
        self.emit_mov_qword_ptr_store("rdx", slot * 8, "rax")
    
    def emit_store_string_char(self, ctx, name, index_exprs, expr_type):
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        if expr_type != "char":
            raise CompileError(ctx, "E0005", got=expr_type, expected="char")

        # Zeichenwert sichern: RAX zeigt auf Stringliteral, erstes Zeichen laden
        self.emit_movzx("ebx", "byte_ptr(rax)", comment="char value")

        # Index berechnen
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        # Pascal: s[1] -> data[0]
        self.emit_sub("eax", 1)
        self.emit_mov("r10d", "eax", comment='zero based string index')

        # String-Datenpointer laden
        var_info = self.var_info(ctx, name)
        self.emit_load_var(name, var_info)  # RAX = char*

        # nil check
        nil_ok = self.new_named_label("string_not_nil")
        self.emit_test("rax", "rax")
        self.emit_jnz(nil_ok)
        self.emit_mov_imm("rax", "&_jit_string_range_error")
        self.emit_call("rax")
        self.emit_bind_label(nil_ok)

        # length aus Header laden: header liegt 16 Bytes vor data
        self.emit_mov("r11", "rax")
        self.emit_sub("r11", 16)
        self.emit_mov_reg_qword("r11", "r11", comment='string length')

        # Range Check:
        # r10d darf nicht negativ sein und muss < length sein
        ok_label = self.new_named_label("string_index_ok")
        fail_label = self.new_named_label("string_index_fail")

        self.emit_cmp("r10d", 0)
        self.emit_jl(fail_label)

        self.emit_cmp("r10", "r11")
        self.emit_jb(ok_label)

        self.emit_bind_label(fail_label)
        self.emit_mov_imm("rax", "&_jit_string_range_error")
        self.emit_call("rax")

        self.emit_bind_label(ok_label)

        # Adresse berechnen und schreiben
        self.emit_movsxd("r11", "r10d")
        self.emit_add("r11", "rax")
        self.emit_mov_byte_ptr_store("r11", 0, "bl", comment="s[index] :=")
    
    def emit_store_pointer_var_from_rax(self, ctx, name):
        var_info = self.var_info(ctx, name)
        slot = var_info["slot"]

        self.emit_mov_qword("rdx", "r12", "pointr_vars")
        self.emit_mov_qword_ptr_store("rdx", slot * 8, "rax")
    
    def emit_store_pointer_deref(self, ctx, name, expr_type):
        key = name.lower()

        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)

        info = self.vars[key]
        typ = info["type"]

        if not isinstance(typ, str) or not typ.startswith("^"):
            raise CompileError(ctx, "E0005", got=typ, expected="pointer")

        base_type = typ[1:]

        if base_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=base_type)

        if expr_type == "integer":
            self.emit_mov("ebx", "eax")

        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

        elif expr_type == "string":
            self.emit_push("rax")

        self.emit_load_var(name, info)

        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("rax", 0, "ebx", comment="p^ :=")
            return

        if expr_type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", 0, "xmm0", comment="p^ :=")
            return

        if expr_type == "string":
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", 0, "r11", comment="p^ :=")
            return
        
    def emit_store_record_field(self, ctx, parts, expr_type):
        field_offset, field = self.resolve_record_path(ctx, parts)

        if field.type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        path = ".".join(parts)

        self.emit_mov_qword("r11", "r12", "record_vars")

        if field.type == "integer":
            self.emit_mov_dword_ptr_store("r11", field_offset, "eax", comment=path)
            return

        if field.type == "double":
            self.emit_movsd_store("r11", field_offset, "xmm0", comment=path)
            return

        if field.type == "string":
            self.emit_mov_qword_ptr_store("r11", field_offset, "rax", comment=path)
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_param(self, ctx, name, expr_type):
        param = self.find_param(name)

        if not param:
            raise CompileError(ctx, "E0001", name=name)

        if not param.get("is_var", False):
            raise CompileError(ctx, "E0006")

        typ    = self.resolve_type(param["type"])
        offset = param["stack_offset"]

        if typ != expr_type and expr_type != "^nil":
            raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

        self.emit_mov_qword_ptr("r11", "rbp", offset, comment=f"var param address {name}")

        if typ == "integer":
            self.emit_mov_dword_ptr_store("r11", 0, "eax")
            return

        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword_ptr_store("r11", 0, "rax")
            return

        raise CompileError(ctx, "E0013", var_type=typ)
    
    def emit_store_pointer_record_field(self, ctx, parts, expr_type):
        ptr_info, field_offset, field = self.resolve_pointer_record_path(ctx, parts)
        ptr_name = parts[0]
        path = "^.".join([ptr_name, ".".join(parts[1:])])

        is_nil_pointer = (
            isinstance(field.type, str)
            and field.type.startswith("^")
            and expr_type in ("integer", "^nil")
        )
        
        if isinstance(field.type, str) and field.type.startswith("^"):
            if is_nil_pointer:
                self.emit_xor("rax", "rax", comment="nil pointer")

        if field.type != expr_type and not is_nil_pointer:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        # Pointer-Feld zuerst behandeln!
        if isinstance(field.type, str) and field.type.startswith("^"):
            if is_nil_pointer:
                self.emit_xor("rax", "rax", comment="nil pointer")

            self.emit_push("rax", comment='save right pointer value')

            if ptr_info.get("is_local", False):
                self.emit_load_local_var(ctx, ptr_name, ptr_info)
            else:
                self.emit_load_var(ptr_name, ptr_info)

            if field_offset != 0:
                self.emit_add("rax", field_offset, comment="field offset")

            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", 0, "r11", comment=f"{path} :=")
            return

        if field.type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if expr_type == "integer":
            self.emit_mov("ebx", "eax")

        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

        elif expr_type == "string":
            self.emit_push("rax")

        if ptr_info.get("is_local", False):
            self.emit_load_local_var(ctx, ptr_name, ptr_info)
        else:
            self.emit_load_var(ptr_name, ptr_info)
            
        self.emit_nil_pointer_check(ptr_name)

        if field_offset != 0:
            self.emit_add("rax", field_offset, comment="field offset")

        if field.type == "integer":
            self.emit_mov_dword_ptr_store("rax", 0, "ebx", comment=f"{path} :=")
            return

        if field.type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("rax", 0, "xmm0", comment=f"{path} :=")
            return

        if field.type == "string":
            self.emit_pop("r11")
            self.emit_mov_qword_ptr_store("rax", 0, "r11", comment=f"{path} :=")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_array_element(self, ctx, var_name, index_expr_ctx, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)
        
        if getattr(array_info, "is_dynamic", False):
            if array_info.element_type == "double" and expr_type == "integer":
                self.emit_cvtsi2sd("xmm0", "eax")
                expr_type = "double"

            if array_info.element_type != expr_type:
                raise CompileError(ctx, "E0005", got=expr_type, expected=array_info.element_type)

            if expr_type == "integer":
                self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")
            elif expr_type == "double":
                self.emit_movsd_store("r12", "offsetof(JitContext, print_double_tmp)", "xmm0")
            elif expr_type == "string":
                self.emit_push("rax")

            index_exprs = index_expr_ctx
            if not isinstance(index_exprs, list):
                index_exprs = [index_exprs]

            if len(index_exprs) != 1:
                raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

            index_type = self.visit(index_exprs[0])

            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("r10d", "eax", comment='save dynamic array byte offset')

            self.emit_load_var(var_name, var_info)   # RAX = data pointer
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax", comment="dynamic array element address")

            if array_info.element_type == "integer":
                self.emit_mov_dword("eax", "r12", "print_int_tmp")
                self.emit_mov_dword_ptr_store("r11", 0, "eax")
                return

            if array_info.element_type == "double":
                self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
                self.emit_movsd_store("r11", 0, "xmm0")
                return

            if array_info.element_type == "string":
                self.emit_pop("rax")
                self.emit_mov_qword_ptr_store("r11", 0, "rax")
                return

            raise CompileError(ctx, "E0013", var_type=array_info.element_type)

        if array_info.element_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if array_info.element_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=array_info.element_type)

        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")

        elif expr_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

        elif expr_type == "string":
            self.emit_push("rax")

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        if array_info.element_type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", 0, "eax")
            return

        if array_info.element_type == "double":
            self.emit_movsd_load("xmm0", "rsp")
            self.emit_add("rsp", 8)
            self.emit_movsd_store("r11", 0, "xmm0")
            return

        if array_info.element_type == "string":
            self.emit_pop("rax")
            self.emit_mov_qword_ptr_store("r11", 0, "rax")
            return

        raise CompileError(ctx, "E0013", var_type=array_info.element_type)

    def emit_load_array_element(self, ctx, var_name, index_expr_ctx):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        var_info, array_info = self.get_array_info(ctx, var_name)
        
        if getattr(array_info, "is_dynamic", False):
            index_exprs = index_expr_ctx
            if not isinstance(index_exprs, list):
                index_exprs = [index_exprs]

            if len(index_exprs) != 1:
                raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

            index_type = self.visit(index_exprs[0])

            if index_type != "integer":
                raise CompileError(ctx, "E0005", got=index_type, expected="integer")

            self.emit_imul("eax", "eax", array_info.element_size)
            self.emit_mov("r10d", "eax", comment='save dynamic array byte offset')

            self.emit_load_var(var_name, var_info)   # RAX = data pointer
            self.emit_movsxd("r11", "r10d")
            self.emit_add("r11", "rax", comment="dynamic array element address")

            if array_info.element_type == "integer":
                self.emit_mov_reg_dword("eax", "r11")
                return "integer"

            if array_info.element_type == "double":
                self.emit_movsd_load("xmm0", "r11")
                return "double"

            if array_info.element_type == "string":
                self.emit_mov_reg_qword("rax", "r11")
                return "string"

            raise CompileError(ctx, "E0014", var_type=array_info.element_type)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("r11", "rax")

        if array_info.element_type == "integer":
            self.emit_mov_reg_dword("eax", "r11")
            return "integer"

        if array_info.element_type == "double":
            self.emit_movsd_load("xmm0", "r11")
            return "double"

        if array_info.element_type == "string":
            self.emit_mov_reg_qword("rax", "r11")
            return "string"

        raise CompileError(ctx, "E0014", var_type=array_info.element_type)
        
    def emit_store_result(self, ctx, expr_type):
        if self.current_function is None:
            raise CompileError(ctx, "E0006")

        return_type = self.resolve_type(
            self.current_function["return_type"]
        )

        if return_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"

        if return_type == "integer" and expr_type == "char":
            expr_type = "integer"

        if return_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=return_type)

        if return_type == "integer":
            return None

        if return_type == "double":
            return None

        if return_type == "string":
            return None

        raise CompileError(
            ctx,
            "E0005",
            got=return_type,
            expected="integer/string/double"
        )

    def emit_load_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        field = self.resolve_array_record_field(
            ctx,
            var_name,
            index_expr_ctx,
            field_parts
        )

        path = var_name + "[...]." + ".".join(field_parts)

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "r11", 0, comment=path)
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "r11", 0, comment=path)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "r11", 0, comment=path)
            return "string"

        return field.type

    def emit_store_array_record_field(self, ctx, var_name, index_expr_ctx, field_parts, expr_type):
        index_exprs = index_expr_ctx
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]
            
        # Wert sichern, bevor Index/Adresse berechnet wird
        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")

        elif expr_type == "double":
            self.emit_movsd_store("r12", "offsetof(JitContext, print_double_tmp)", "xmm0")

        else:
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer/double")

        field = self.resolve_array_record_field(
            ctx,
            var_name,
            index_expr_ctx,
            field_parts
        )

        if field.type == "double" and expr_type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_cvtsi2sd("xmm0", "eax")
            self.emit_movsd_store("r11", 0, "xmm0", comment=f"{var_name}[...].{'.'.join(field_parts)} :=")
            return

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if field.type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", 0, "eax", comment=f"{var_name}[...].{'.'.join(field_parts)} :=")
            return

        if field.type == "double":
            self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
            self.emit_movsd_store("r11", 0, "xmm0", comment=f"{var_name}[...].{'.'.join(field_parts)} :=")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)

    def emit_store_dynamic_array_element(self, ctx, name, index_ctx, value_ctx):
        arr = self.lookup_var(name)

        self.visit(index_ctx)                  # eax = index
        self.emit_mov("r10d", "eax")

        self.emit_load_var_value(name)         # rax = data pointer
        self.emit_test("rax", "rax")
        self.emit_jz("label_array_nil_error")

        # Bounds Check
        self.emit_mov("r11", "rax")
        self.emit_sub("r11", 16)      # Header
        self.emit_mov_reg_qword("r11", "r11")  # length
        self.emit_cmp("r10", "r11")
        self.emit_jae("label_array_bounds_error")

        self.visit(value_ctx)                  # eax = value

        self.emit_load_var_value(name)         # rax = data pointer
        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", 4)
        self.emit_add("r11", "rax")
        self.emit_mov_dword_ptr_store("r11", 0, "eax")
    
    def emit_store_dynamic_array_record_field(self,
        ctx,
        var_name,
        index_exprs,
        field_parts,
        expr_type):
        
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        var_info, array_info = self.get_array_info(ctx, var_name)

        record_type = array_info.element_type

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        # Wert sichern
        if expr_type == "integer":
            self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, print_int_tmp)", "eax")
        elif expr_type == "double":
            self.emit_movsd_store("r12", "offsetof(JitContext, print_double_tmp)", "xmm0")
        elif expr_type == "string":
            self.emit_push("rax")
        else:
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer/double/string")

        # Index berechnen
        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        self.emit_mov("r10d", "eax", comment='dynamic record array index')

        # Datenpointer laden
        self.emit_load_var(var_name, var_info)  # RAX = data pointer

        # Elementadresse: data + index * record_size
        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", array_info.element_size)
        self.emit_add("r11", "rax", comment="record element address")

        # Feldoffset berechnen
        current_type = record_type
        field = None
        field_offset = 0

        for field_name in field_parts:
            record = self.records[current_type]
            key = field_name.lower()

            if key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[key]
            field_offset += field.offset
            current_type = field.type

        if field is None:
            raise CompileError(ctx, "E0005", got="field", expected="record field")

        if field.type == "double" and expr_type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_cvtsi2sd("xmm0", "eax")
            self.emit_movsd_store("r11", field_offset, "xmm0")
            return

        if field.type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=field.type)

        if field.type == "integer":
            self.emit_mov_dword("eax", "r12", "print_int_tmp")
            self.emit_mov_dword_ptr_store("r11", field_offset, "eax")
            return

        if field.type == "double":
            self.emit_movsd_load_field("xmm0", "r12", "print_double_tmp")
            self.emit_movsd_store("r11", field_offset, "xmm0")
            return

        if field.type == "string":
            self.emit_pop("rax")
            self.emit_mov_qword_ptr_store("r11", field_offset, "rax")
            return

        raise CompileError(ctx, "E0013", var_type=field.type)
    
    def emit_store_local_var(self, ctx, name, expr_type):
        var = self.find_local_var(name)

        if not var:
            raise CompileError(ctx, "E0012", name=name)

        typ    = var["type"]
        offset = var["offset"]

        if typ == "integer":
            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

            self.emit_mov_dword_ptr_store("rbp", offset, "eax", comment=f"local {name} :=")
            return

        if isinstance(typ, str) and typ.startswith("^"):
            if expr_type != typ and expr_type != "^nil":
                raise CompileError(ctx, "E0005", got=expr_type, expected=typ)

            self.emit_mov_qword_ptr_store("rbp", offset, "rax", comment=f"local pointer {name} :=")
            return

        raise CompileError(ctx, "E0011", typ=typ)
        
    def emit_call_rax(self):
        self.backend.emit_call("rax")
    
    def emit_load_var(self, name, info):
        typ  = info["type"]
        slot = info["slot"]
        
        # -------------------------------------------------
        # Neues COFF-Backend:
        # direkte globale Variable per Symbol laden
        # -------------------------------------------------
        if hasattr(self, "coff") and "symbol" in info:
            symbol = info["symbol"]

            if typ == "integer":
                self.coff.emit_mov_r32_data_label("eax", symbol)
                return

            if typ == "double":
                self.coff.emit_movsd_data_label("xmm0", symbol)
                return

            if typ == "string":
                self.coff.emit_mov_r64_data_label("rax", symbol)
                return

            if isinstance(typ, str) and typ.startswith("^"):
                self.coff.emit_mov_r64_data_label("rax", symbol)
                return
        
        # -------------------------------------------------
        # Altes System über JitContext / r12
        # -------------------------------------------------
        if isinstance(typ, str) and typ.startswith("^"):
            self.emit_mov_qword("rax", "r12", "pointr_vars")
            self.emit_mov_qword_ptr("rax", "rax", slot * 8, comment=f"{name}")
            return
        
        if isinstance(typ, str) and typ in self.classes:
            return self.emit_load_object_var(None, name, info)
        
        if isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]
            
            if getattr(array_info, "is_dynamic", False):
                self.emit_mov_qword("rax", "r12", "pointr_vars")
                self.emit_mov_qword_ptr("rax", "rax", slot * 8, comment=f"dynamic array {name}")
                return
        
        if typ == "integer":
            self.emit_mov_qword("rax", "r12", "int_vars")
            self.emit_mov_dword_ptr("eax", "rax", slot * 4, comment=f"{name}")
            return
        
        if typ == "double":
            self.emit_mov_qword("rax", "r12", "double_vars")
            self.emit_movsd_load("xmm0", "rax", slot * 8, comment=f"{name}")
            return
        
        if typ == "string":
            self.emit_mov_qword("rax", "r12", "string_vars")
            self.emit_mov_qword_ptr("rax", "rax", slot * 8, comment=f"{name}")
            return
        
        raise CompileError(None, "E0014", var_type=typ)
    
    def emit_load_dynamic_array_element(self, ctx, name, index_ctx):
        arr = self.lookup_var(name)

        self.visit(index_ctx)
        self.emit_mov("r10d", "eax")

        self.emit_load_var_value(name)         # rax = data pointer

        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", 4)
        self.emit_add("r11", "rax")
        self.emit_mov_reg_dword("eax", "r11")

        return "integer"
    
    def emit_load_dynamic_array_record_field(self,
        ctx,
        var_name,
        index_exprs,
        field_parts):
        
        if not isinstance(index_exprs, list):
            index_exprs = [index_exprs]

        if len(index_exprs) != 1:
            raise CompileError(ctx, "E0005", got=str(len(index_exprs)), expected="1")

        var_info, array_info = self.get_array_info(ctx, var_name)

        record_type = array_info.element_type

        if record_type not in self.records:
            raise CompileError(ctx, "E0005", got=record_type, expected="record")

        index_type = self.visit(index_exprs[0])

        if index_type != "integer":
            raise CompileError(ctx, "E0005", got=index_type, expected="integer")

        self.emit_mov("r10d", "eax", comment='dynamic record array index')

        self.emit_load_var(var_name, var_info)  # RAX = data pointer

        self.emit_movsxd("r11", "r10d")
        self.emit_imul("r11", "r11", array_info.element_size)
        self.emit_add("r11", "rax", comment="record element address")

        current_type = record_type
        field = None
        field_offset = 0

        for field_name in field_parts:
            record = self.records[current_type]
            key = field_name.lower()

            if key not in record.fields:
                raise CompileError(ctx, "E0001", name=field_name)

            field = record.fields[key]
            field_offset += field.offset
            current_type = field.type

        if field.type == "integer":
            self.emit_mov_dword_ptr("eax", "r11", field_offset)
            return "integer"

        if field.type == "double":
            self.emit_movsd_load("xmm0", "r11", field_offset)
            return "double"

        if field.type == "string":
            self.emit_mov_qword_ptr("rax", "r11", field_offset)
            return "string"

        raise CompileError(ctx, "E0014", var_type=field.type)
    
    def emit_store_var(self, ctx, name, info):
        typ  = info["type"]
        slot = info["slot"]

        if hasattr(self, "coff") and "symbol" in info:
            symbol = info["symbol"]

            if typ == "integer":
                self.coff.emit_mov_data_label_r32(symbol, "eax")
                return

            if typ == "double":
                self.coff.emit_movsd_data_label_store(symbol, "xmm0")
                return

            if typ == "string":
                self.coff.emit_mov_data_label_r64(symbol, "rax")
                return

            if isinstance(typ, str) and typ.startswith("^"):
                self.coff.emit_mov_data_label_r64(symbol, "rax")
                return

        if typ.startswith("^"):
            self.emit_mov_qword("r11", "r12", "pointr_vars")
            self.emit_mov_qword_ptr_store("r11", slot * 8, "rax", comment=f"{name}")
            return
        
        if isinstance(typ, str) and typ in self.arrays:
            array_info = self.arrays[typ]
            
            if getattr(array_info, "is_dynamic", False):
                self.emit_mov_qword("r11", "r12", "pointr_vars")
                self.emit_mov_qword_ptr_store("r11", slot * 8, "rax", comment=f"dynamic array {name}")
                return
                
        if typ == "integer":
            self.emit_mov("ebx", "eax")
            self.emit_mov_qword("rax", "r12", "int_vars")
            self.emit_mov_dword_ptr_store("rax", slot * 4, "ebx", comment=f"{name}")
            return

        if typ == "double":
            self.emit_mov_qword("r11", "r12", "double_vars")
            self.emit_movsd_store("r11", slot * 8, "xmm0", comment=f"{name}")
            return

        if typ == "string":
            self.emit_mov_qword("r11", "r12", "string_vars")
            self.emit_mov_qword_ptr_store("r11", slot * 8, "rax", comment=f"{name}")
            return

        raise CompileError(ctx, "E0013", var_type=typ)
    
    def emit_procedure_declaration(self, ctx):
        proc_name = ctx.IDENT().getText()

        end_label = self.new_label(f"endproc_{proc_name}")

        self.emit_jmp(end_label)
        self.emit_bind_label(proc_name)

        self.emit_push("rbp")
        self.emit_mov("rbp", "rsp")
        self.emit_sub("rsp", 256, comment="local variables")

        self.push_local_scope()

        # lokale var-Deklarationen einsammeln
        for child in ctx.children:
            cname = type(child).__name__

            if "VarSectionContext" in cname:
                self.visit(child)

        # eigentlichen Procedure-Block erzeugen
        block = ctx.block()
        if block:
            self.visit(block)

        self.pop_local_scope()

        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()

        self.emit_bind_label(end_label)
    
    def emit_address_of_array_element(self, ctx, var_name, index_exprs):
        var_info, array_info = self.get_array_info(ctx, var_name)

        self.emit_multi_array_index_offset(ctx, var_name, array_info, index_exprs)

        self.emit_imul("eax", "eax", array_info.element_size)
        self.emit_add("eax", var_info["slot"])

        self.emit_mov_qword("r11", "r12", "arrays_vars")
        self.emit_movsxd("rax", "eax")
        self.emit_add("rax", "r11", comment="@array[index]")

        return "^" + array_info.element_type
    
    def emit_function_declaration(self, ctx, name, return_type):
        #return_type = self.resolve_type(return_type)
        key         = name.lower()
        scoped      = self.scoped_name(name)

        label       = self.functions[key]["label"]
        end_label   = self.new_named_label("endfunc_" + name)

        self.functions[scoped.lower()]["label"] = label

        params = self.collect_formal_params(ctx)
        self.functions[scoped.lower()]["params"] = params

        param_regs = ["rcx", "rdx", "r8", "r9"]

        if len(params) > len(param_regs):
            raise CompileError(
                ctx,
                "E0005",
                got="too many params",
                expected="max 4 params"
            )
        
        self.emit_jmp(end_label)
        self.emit_bind_label(label)
        
        self.emit_push("rbp",        comment="epilog")
        self.emit_mov ("rbp", "rsp", comment="stack frame")
        self.emit_push("rbx",        comment="preserve non-volatile RBX")
        
        old_params   = self.current_proc_params
        old_function = self.current_function
        
        self.current_proc_params = {}
        self.current_function = {
            "name": name,
            "return_type": return_type.lower(),
            "scoped_name": scoped
        }
        
        for index, p in enumerate(params):
            reg = param_regs[index]
            pname = p["name"]
            
            self.emit_push(reg, comment=f"save function param {pname}")
            
            self.current_proc_params[pname.lower()] = {
                "type": p["type"],
                "reg": reg,
                "stack_offset": -8 * (index + 2)
            }
            
        if len(params) % 2 == 0:
            self.emit_sub("rsp", 8, comment="align stack in function")
        
        self.scope_stack.append(name)
        self.emit_sub("rsp", 256, comment="local variables")
        
        self.push_local_scope()
        self.push_const_scope()
        
        self.exit_label_stack.append(end_label)
        self.visit(ctx.block())
        self.exit_label_stack.pop()

        self.pop_const_scope()
        self.pop_local_scope()
        
        self.scope_stack.pop()

        self.current_function = old_function
        self.current_proc_params = old_params

        if return_type.lower() not in ["integer", "string", "double"]:
            raise CompileError(ctx, "E0005", got=return_type, expected="integer/string/double")

        self.emit_mov_qword_ptr("rbx", "rbp", -8)
        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()

        self.emit_bind_label(end_label)
    
    def emit_self_method_call(self, ctx, method_name, actual_types=None):
        if actual_types is None:
            actual_types = []

        if self.current_class is None:
            return None

        method, owner_cls = self.find_class_method_recursive(
            ctx,
            self.current_class,
            method_name,
            actual_types
        )

        if method.kind not in ("function", "constructor"):
            raise CompileError(
                ctx,
                "E0019",
                text=f"{method_name} is not a function"
            )

        self.emit_mov_qword_ptr("rcx", "rbp", -8, comment='Self')
        self.emit_sub("rsp", 32)
        self.emit_call_lbl(method.label, comment=f"Self.{method.name}")
        self.emit_add("rsp", 32)

        return self.resolve_type(method.return_type)
    
    def emit_init_array_var(self, ctx, name, info):
        array_type = info["type"]

        if array_type not in self.arrays:
            return

        array_info = self.arrays[array_type]

        if not array_info.init_values:
            return

        base_offset = info["slot"]

        self.emit_mov_qword("r11", "r12", "arrays_vars")

        for index, value in enumerate(array_info.init_values):
            offset = base_offset + index * array_info.element_size

            if array_info.element_type == "integer":
                self.emit_mov_dword_ptr_store("r11", offset, value, comment=f"init {name}[{index + array_info.index_min}]")

            elif array_info.element_type == "double":
                self.emit_mov_imm("rax", double_to_bits(float(value)))
                self.emit_movq("xmm0", "rax")
                self.emit_movsd_store("r11", offset, "xmm0", comment=f"init {name}[{index + array_info.index_min}]")

            elif array_info.element_type == "string":
                label = self.add_string_literal(value)
                self.emit_mov_imm("rax", label)
                self.emit_mov_qword_ptr_store("r11", offset, "rax", comment=f"init {name}[{index + array_info.index_min}]")
                
    def emit_if_statement(self, ctx):
        else_name = self.new_named_label("else")
        end_name  = self.new_named_label("endif")

        self.emit_condition_jump_false(ctx.condition(), else_name)

        self.visit(ctx.statement(0))

        if ctx.ELSE():
            self.emit_jmp(end_name)
            self.emit_bind_label(else_name)
            self.visit(ctx.statement(1))
            self.emit_bind_label(end_name)
        else:
            self.emit_bind_label(else_name)
        
    def emit_int_to_double(self):
        self.emit_cvtsi2sd("xmm0", "eax")
    
    def emit_condition_jump_false(self, ctx, false_label):
        # Boolean-Ausdruck ohne Vergleich:
        # if a and not b then
        if ctx.compareOp() is None:
            expr_type = self.visit(ctx.expr(0))

            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_je(false_label)
            return

        left_ctx  = ctx.expr(0)
        right_ctx = ctx.expr(1)
        op        = ctx.compareOp().getText()

        left_type = self.visit(left_ctx)
        
        if isinstance(left_type, str) and left_type.startswith("^"):
            self.emit_push("rax", comment='save left pointer')

            right_type = self.visit(right_ctx)

            if right_type != left_type and right_type != "^nil":
                raise CompileError(
                    ctx,
                    "E0005",
                    got=right_type,
                    expected=left_type + "/nil"
                )

            self.emit_mov("rbx", "rax", comment='right pointer')
            self.emit_pop("rax", comment="left pointer")
            self.emit_cmp("rax", "rbx")

            if op == "=":
                self.emit_jne(false_label)
                return

            if op == "<>":
                self.emit_je(false_label)
                return

            raise CompileError(
                ctx,
                "E0005",
                got=op,
                expected="= or <>"
            )

        if left_type == "integer":
            self.emit_push("rax")
        elif left_type == "double":
            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")
        else:
            raise CompileError(ctx, "E0005", got=left_type, expected="integer/double")

        right_type = self.visit(right_ctx)

        if left_type == "double" or right_type == "double":
            if right_type == "integer":
                self.emit_cvtsi2sd("xmm0", "eax")
            elif right_type != "double":
                raise CompileError(ctx, "E0005", got=right_type, expected="integer/double")

            self.emit_movapd("xmm1", "xmm0")

            if left_type == "integer":
                self.emit_pop("rax")
                self.emit_cvtsi2sd("xmm0", "eax")
            else:
                self.emit_movsd_load("xmm0", "rsp")
                self.emit_add("rsp", 8)

            self.emit_ucomisd("xmm0", "xmm1")

            jump_map = {
                "=":  self.emit_jne,
                "<>": self.emit_je,
                "<":  self.emit_jae,
                "<=": self.emit_ja,
                ">":  self.emit_jbe,
                ">=": self.emit_jb,
            }

            jump_map[op](false_label)
            return

        self.emit_mov("ebx", "eax")
        self.emit_pop("rax")
        self.emit_cmp("eax", "ebx")

        jump_map = {
            "=":  self.emit_jne,
            "<>": self.emit_je,
            "<":  self.emit_jge,
            "<=": self.emit_jg,
            ">":  self.emit_jle,
            ">=": self.emit_jl,
        }

        jump_map[op](false_label)
    
    def emit_expr_as_double(self, ctx):
        expr_type = self.visit(ctx)

        if expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")

        elif expr_type != "double":
            raise CompileError(ctx, "E0005", got=expr_type, expected="double")

        return "double"

    def emit_while_statement(self, ctx):
        start_name = self.new_named_label("while")
        end_name   = self.new_named_label("endwhile")

        self.emit_bind_label(start_name)
        self.emit_condition_jump_false(ctx.condition(), end_name)

        self.visit(ctx.statement())

        self.emit_jmp(start_name)
        self.emit_bind_label(end_name)
    
    def emit_repeat_statement(self, ctx):
        start_label = self.new_label_name("repeat")
        end_label   = self.new_label_name("endrepeat")

        self.emit_label(start_label)

        # Body
        for stmt in ctx.statement():
            self.visit(stmt)

        # Bedingung am Ende auswerten
        # Wichtig: Springe zurück, wenn Bedingung FALSE ist
        self.emit_condition_jump_false(ctx.condition(), start_label)
        self.emit_label(end_label)
    
    def require_var(self, ctx, name):
        key = name.lower()
        
        if key not in self.vars:
            raise CompileError(ctx, "E0003", name=key)  # Variable not declared
        
        return self.vars[key]
    
    def emit_repeat_statement(self, ctx):
        start_name = self.new_named_label("repeat")
        end_name   = self.new_named_label("endrepeat")

        self.emit_bind_label(start_name)

        for stmt in ctx.statementList().statement():
            self.visit(stmt)

        self.emit_condition_jump_false(ctx.condition(), start_name)

        self.emit_bind_label(end_name)
    
    def emit_for_statement(self, ctx):
        var_name = ctx.IDENT().getText()
        info = self.var_info(ctx, var_name)

        if info["type"] != "integer":
            raise CompileError(ctx, "E0005", got=info["type"], expected="integer")

        start_name    = self.new_named_label("for")
        continue_name = self.new_named_label("for_continue")
        end_name      = self.new_named_label("endfor")

        # Startwert auswerten
        start_type = self.visit(ctx.expr(0))

        if start_type != "integer":
            raise CompileError(ctx, "E0005", got=start_type, expected="integer")

        self.emit_store_var(ctx, var_name, info)

        # Endwert auswerten
        end_type = self.visit(ctx.expr(1))

        if end_type != "integer":
            raise CompileError(ctx, "E0005", got=end_type, expected="integer")

        self.emit_mov_dword_ptr_store("r12", "offsetof(JitContext, _print_int_tmp)", "eax", comment="for end value")

        self.emit_bind_label(start_name)

        self.emit_load_var(var_name, info)

        direction = ctx.getChild(4).getText().lower()

        if direction == "to":
            self.emit_cmp_dword("eax", "r12", "_print_int_tmp")
            self.emit_jg(end_name)
        else:
            self.emit_cmp_dword("eax", "r12", "_print_int_tmp")
            self.emit_jl(end_name)

        self.break_label_stack.append(end_name)
        self.continue_label_stack.append(continue_name)

        self.visit(ctx.statement())

        self.continue_label_stack.pop()
        self.break_label_stack.pop()

        self.emit_bind_label(continue_name)

        self.emit_load_var(var_name, info)

        if direction == "to":
            self.emit_add("eax", 1)
        else:
            self.emit_sub("eax", 1)

        self.emit_store_var(ctx, var_name, info)

        self.emit_jmp(start_name)
        self.emit_bind_label(end_name)
    
    # typen überprüfung ...
    def var_info(self, ctx, name):
        key = name.lower()
        
        if key not in self.vars:
            raise CompileError(ctx, "E0001", name=name)
        
        return self.vars[key]
        
    def var_type_of(self, ctx, name):
        return self.var_info(ctx, name)["type"]
    
    def variable_ref_has_dot(self, ref):
        return any(s.DOT() for s in ref.variableSuffix())
    
    def variable_ref_has_index(self, ref):
        return any(s.LBRACK() for s in ref.variableSuffix())
    
    def slot_for(self, ctx, name):
        return self.var_info(ctx, name)["slot"]
    
    def emit(self, line):
        self.backend.emit(line)
    
    def emit_add(self, reg, value, comment=""):
        self.backend.emit_add(reg, value, comment)

    def emit_imul(self, dst, src, value=None, comment=""):
        self.backend.emit_imul(dst, src, value, comment)
    
    def emit_bind_label(self, label, comment=""):
        self.backend.emit_bind_label(label, comment)

    def emit_new_label_decl(self, name, comment=""):
        self.backend.emit_new_label_decl(name, comment)
    
    def emit_call(self, dst, comment=""):
        self.backend.emit_call(dst, comment)

    def emit_cmp(self, reg, value, comment=""):
        self.backend.emit_cmp(reg, value, comment)

    def emit_cmp_dword(self, reg, base, field, comment=""):
        self.backend.emit_cmp_dword(reg, base, field, comment)

    def emit_jg(self, label, comment=""): self.backend.emit_jg(label, comment)
    def emit_jl(self, label, comment=""): self.backend.emit_jl(label, comment)
    def emit_jz(self, label, comment=""): self.backend.emit_jz(label, comment)
    def emit_jb(self, label, comment=""): self.backend.emit_jb(label, comment)
    def emit_ja(self, label, comment=""): self.backend.emit_ja(label, comment)
    def emit_jae(self, label, comment=""): self.backend.emit_jae(label, comment)
    def emit_jbe(self, label, comment=""): self.backend.emit_jbe(label, comment)
    def emit_je(self, label, comment=""): self.backend.emit_je(label, comment)
    def emit_jle(self, label, comment=""): self.backend.emit_jle(label, comment)
    def emit_jge(self, label, comment=""): self.backend.emit_jge(label, comment)
    def emit_jne(self, label, comment=""): self.backend.emit_jne(label, comment)
    def emit_jnz(self, label, comment=""): self.backend.emit_jnz(label, comment)

    def emit_jmp(self, target, comment=""):
        self.backend.emit_jmp(target, comment)
    
    def emit_lea_byte (self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_byte(reg1, reg2, offset, comment)
        
    def emit_lea_dword(self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_dword(reg1, reg2, offset, comment)
        
    def emit_lea_qword(self, reg1, reg2, offset, comment=""):
        self.backend.emit_lea_qword(reg1, reg2, offset, comment)
    
    def emit_mov_byte (self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_byte(reg1, reg2, vars, comment)
    
    def emit_mov_dword(self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_dword(reg1, reg2, vars, comment)
        
    def emit_mov_qword(self, reg1, reg2, vars, comment=""):
        self.backend.emit_mov_qword(reg1, reg2, vars, comment)
    
    def emit_new_label_decl(self, name, comment=""):
        self.backend.emit_new_label_decl(name, comment)
        
    def emit_mov    (self, dst, src, comment=""): self.backend.emit_mov    (dst, src, comment)
    def emit_mov_imm(self, dst, src, comment=""): self.backend.emit_mov_imm(dst, src, comment)
    def emit_movzx  (self, dst, src, comment=""): self.backend.emit_movzx  (dst, src, comment)
    def emit_movsxd (self, dst, src, comment=""): self.backend.emit_movsxd (dst, src, comment)
    def emit_movq(self, dst, src, comment=""): self.backend.emit_movq(dst, src, comment)
    def emit_movsd_load(self, dst, base, offset=0, comment=""): self.backend.emit_movsd_load(dst, base, offset, comment)
    def emit_movsd_load_field(self, dst, base, field, comment=""): self.backend.emit_movsd_load_field(dst, base, field, comment)
    def emit_movsd_store(self, base, offset, src, comment=""): self.backend.emit_movsd_store(base, offset, src, comment)
    def emit_ucomisd(self, dst, src, comment=""): self.backend.emit_ucomisd(dst, src, comment)
    def emit_cvtsi2sd(self, dst, src, comment=""): self.backend.emit_cvtsi2sd(dst, src, comment)
    def emit_movapd(self, dst, src, comment=""): self.backend.emit_movapd(dst, src, comment)
    def emit_addsd(self, dst, src, comment=""): self.backend.emit_addsd(dst, src, comment)
    def emit_subsd(self, dst, src, comment=""): self.backend.emit_subsd(dst, src, comment)
    def emit_mulsd(self, dst, src, comment=""): self.backend.emit_mulsd(dst, src, comment)
    def emit_divsd(self, dst, src, comment=""): self.backend.emit_divsd(dst, src, comment)
    def emit_cdq(self, comment=""): self.backend.emit_cdq(comment)
    def emit_idiv(self, reg, comment=""): self.backend.emit_idiv(reg, comment)
    def emit_mov_byte_ptr (self, dst, base, offset=0, comment=""): self.backend.emit_mov_byte_ptr (dst, base, offset, comment)
    def emit_mov_dword_ptr(self, dst, base, offset=0, comment=""): self.backend.emit_mov_dword_ptr(dst, base, offset, comment)
    def emit_mov_qword_ptr(self, dst, base, offset=0, comment=""): self.backend.emit_mov_qword_ptr(dst, base, offset, comment)
    def emit_mov_qword_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_qword_ptr_store(base, offset, src, comment)
    def emit_mov_dword_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_dword_ptr_store(base, offset, src, comment)
    def emit_mov_byte_ptr_store(self, base, offset, src, comment=""): self.backend.emit_mov_byte_ptr_store(base, offset, src, comment)
    def emit_mov_reg_byte (self, dst, base, comment=""): self.backend.emit_mov_reg_byte (dst, base, comment)
    def emit_mov_reg_dword(self, dst, base, comment=""): self.backend.emit_mov_reg_dword(dst, base, comment)
    def emit_mov_reg_qword(self, dst, base, comment=""): self.backend.emit_mov_reg_qword(dst, base, comment)
    def emit_test(self, reg1, reg2, comment=""): self.backend.emit_test(reg1, reg2, comment)
    def emit_call_reg(self, target, comment=""): self.backend.emit_call_reg(target, comment)
    def emit_call_lbl(self, target, comment=""): self.backend.emit_call_lbl(target, comment)
    
    def emit_xor(self, dst, src, comment=""):
        self.backend.emit_xor(dst, src, comment)
    
    def emit_push(self, reg, comment=""): self.backend.emit_push(reg, comment)
    def emit_pop (self, reg, comment=""): self.backend.emit_pop (reg, comment)
    
    def emit_sub (self, reg, value, comment=""):
        self.backend.emit_sub(reg, value, comment)
    
    def emit_ret(self, comment=""):
        self.backend.emit_ret(comment)
    
    def emit_backend_jmp(self, label):
        self.backend.emit_jmp(label)
    
    def emit_backend_label(self, label):
        self.backend.emit_bind_label(label)
    
    def emit_load_integer_const(self, value):
        self.backend.emit_mov_imm("eax", value)
        return "integer"
    
    def new_label_name(self, prefix):
        self.label_id += 1
        return f"{prefix}_{self.label_id}"
    
    # de-dupplizierer - doppelte Zeichen ignorieren
    def add_string_literal(self, text):
        for name, existing_text in self.string_literals:
            if existing_text == text:
                return name

        name = f"str_{len(self.string_literals)}"
        self.string_literals.append((name, text))
        return name
    
    def visit(self, tree):
        if tree is None:
            return None

        return super().visit(tree)
    
    def visit_actual_param_expr(self, arg):
        if arg is None:
            return None

        if arg.expr():
            return self.visit(arg.expr())

        if arg.STRING():
            value = arg.STRING().getText()[1:-1]
            label = self.add_string_literal(value)

            self.emit_mov("rax", label)

            if len(value) == 1:
                return "char"

            self.emit_mov("rcx", "rax")
            self.emit_mov_imm("rax", "&_jit_dynstring_from_cstr")
            self.emit_call_rax()

            return "string"

        raise CompileError(arg, "E0015", text=arg.getText())
    
    def visitSourceFile(self, ctx):
        if ctx.programFile():
            return self.visit(ctx.programFile())

        if ctx.unitFile():
            return self.visit(ctx.unitFile())
        
        if ctx.libraryFile():
            return self.visit(ctx.libraryFile())

        return None
    
    def visitUsesClause(self, ctx):
        for ident in ctx.qualifiedIdentList().qualifiedIdent():
            self.load_unit(ctx, ident.getText())
        
        return None
    
    def visitProgramFile(self, ctx):
        self.program_name       = ctx.IDENT().getText()
        self.module_kind        = "program"
        self.module_kind_value  = 1
        
        if ctx.usesClause():
            self.visit(ctx.usesClause())
        
        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)

        self.validate_class_methods(ctx)
        
        self.emit_push("r12")
        self.emit_push("rbx")
        self.emit_sub("rsp", 8, comment="align stack")
        self.emit_mov("r12", "rcx", comment="ctx")
        
        for init_label in self.unit_init_labels:
            self.emit_call_lbl(init_label, comment="unit init")
        
        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)
        
        self.visit(ctx.block())
        return self.render_cpp()
    
    def visitLibraryFile(self, ctx):
        self.program_name       = ctx.IDENT().getText()
        self.module_kind        = "library"
        self.module_kind_value  = 3

        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.declarationPart():
            if decl is not None:
                self.visit(decl)
        
        if ctx.exportsClause():
            self.visit(ctx.exportsClause())
            
        self.validate_class_methods(ctx)

        self.emit_push("r12")
        self.emit_push("rbx")
        self.emit_sub("rsp", 8, comment="align stack")
        self.emit_mov("r12", "rcx", comment="ctx")

        for init_label in self.unit_init_labels:
            self.emit_call_lbl(init_label, comment="unit init")

        for name, info in self.vars.items():
            if info["type"] in self.arrays:
                self.emit_init_array_var(ctx, name, info)

        self.visit(ctx.block())

        return self.render_cpp()
    
    def visitUnitFile(self, ctx):
        unit_name = ctx.qualifiedIdent().getText()
        unit_key  = self.normalize_unit_name(unit_name)
        old_unit  = self.current_unit
        
        old_kind        = self.module_kind
        old_kind_value  = self.module_kind_value
        
        self.module_kind        = "unit"
        self.module_kind_value  = 2
        
        self.current_unit       = unit_key

        self.visit(ctx.interfaceSection())
        self.visit(ctx.implementationSection())

        if ctx.unitInitBlock():
            safe_unit_name = self.normalize_unit_name(unit_name)

            init_label = self.new_named_label("unit_init_" + safe_unit_name)
            skip_label = self.new_named_label("skip_unit_init_" + safe_unit_name)

            self.unit_init_labels.append(init_label)

            self.emit_jmp(skip_label)
            self.emit_bind_label(init_label)
            self.visit(ctx.unitInitBlock())
            self.emit_ret()
            self.emit_bind_label(skip_label)

        self.module_kind        = old_kind
        self.module_kind_value  = old_kind_value
        self.current_unit       = old_unit
        
        return None
    
    def visitInterfaceDeclarationPart(self, ctx):
        if ctx.constSection():
            return self.visit(ctx.constSection())
        
        if ctx.typeSection():
            return self.visit(ctx.typeSection())
        
        if ctx.varSection():
            return self.visit(ctx.varSection())
        
        if ctx.procedureHeader():
            return self.visit(ctx.procedureHeader())
        
        if ctx.functionHeader():
            return self.visit(ctx.functionHeader())
        
        return None
    
    def visitImplementationDeclarationPart(self, ctx):
        if ctx.constSection():
            return self.visit(ctx.constSection())
        
        if ctx.typeSection():
            return self.visit(ctx.typeSection())
        
        if ctx.varSection():
            return self.visit(ctx.varSection())
        
        if ctx.procedureDeclaration():
            return self.visit(ctx.procedureDeclaration())
        
        if ctx.functionDeclaration():
            return self.visit(ctx.functionDeclaration())
        
        if ctx.classMethodImplementation():
            return self.visit(ctx.classMethodImplementation())
        
        return None
    
    def visitInterfaceSection(self, ctx):
        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.interfaceDeclarationPart():
            self.visit(decl)

        return None
    
    def visitImplementationSection(self, ctx):
        if ctx.usesClause():
            self.visit(ctx.usesClause())

        for decl in ctx.implementationDeclarationPart():
            self.visit(decl)

        return None
    
    def visitExitStatement(self, ctx):
        if not self.exit_label_stack:
            raise CompileError(ctx, "E0006")

        self.emit_jmp(self.exit_label_stack[-1], comment="Exit")
        return None
    
    def visitConstSection(self, ctx):
        for decl in ctx.constDeclaration():
            self.visit(decl)
        return None

    def visitInheritedStatement(self, ctx):
        if self.current_class is None or self.current_method is None:
            raise CompileError(
                ctx,
                "E0019",
                text="inherited used outside class method"
            )

        cls = self.classes[self.current_class]

        if not cls.parent:
            raise CompileError(
                ctx,
                "E0019",
                text=f"class {cls.name} has no parent class"
            )

        # inherited;
        # inherited Create;
        if ctx.IDENT():
            method_name = ctx.IDENT().getText()
        else:
            method_name = self.current_method.name

        args = self.function_call_args(ctx)
        actual_types = []

        for arg in reversed(args):
            arg_type = self.visit_actual_param_expr(arg)
            actual_types.insert(0, arg_type)
            
            if arg_type == "integer":
                self.emit_movsxd("rax", "eax")
                self.emit_push("rax", comment="inherited integer arg")
            
            elif arg_type == "string":
                self.emit_push("rax", comment="inherited string arg")
            
            elif isinstance(arg_type, str) and arg_type.startswith("^"):
                self.emit_push("rax", comment="inherited pointer arg")
            
            else:
                raise CompileError(
                    ctx,
                    "E0019",
                    text=f"unsupported inherited argument type {arg_type}"
                )
        
        method, owner_cls = self.find_class_method_recursive(
            ctx,
            cls.parent,
            method_name,
            actual_types
        )

        param_regs = ["rdx", "r8", "r9"]

        # Parameter 4..N bleiben als Stack-Parameter liegen
        stack_count = 0

        for index in range(len(args) - 1, 2, -1):
            stack_count += 1

        # Self laden
        self.emit_mov_qword_ptr("rcx", "rbp", -8, comment='inherited Self')

        # Parameter 1..3 aus temporärem Stack holen
        reg_count = min(3, len(args))

        for index in range(reg_count):
            self.emit_pop(param_regs[index], comment=f"inherited arg {index + 1}")

        align_pad = 0

        if stack_count % 2 == 1:
            self.emit_sub("rsp", 8, comment = "align stack before inherited call")
            align_pad = 8

        self.emit_call(method.label, comment = f"inherited {owner_cls.name}.{method.name}")

        if align_pad:
            self.emit_add("rsp", 8, comment = "remove inherited alignment padding")

        if stack_count > 0:
            self.emit_add("rsp", stack_count * 8, comment = "remove inherited stack args")

        return None
    
    def visitClassMethodImplementation(self, ctx):
        class_name  = ctx.IDENT(0).getText()
        method_name = ctx.IDENT(1).getText()
        
        class_key   = class_name.lower()
        method_key  = method_name.lower()
        
        if class_key not in self.classes:
            raise CompileError(ctx, "E0004", name=class_name)
        
        cls = self.classes[class_key]
        
        if method_key not in cls.methods:
            raise CompileError(
                ctx,
                "E0019",
                text=f"class {class_name} has no declared method {method_name}"
            )
        
        params = self.collect_formal_params(ctx)
        method = self.find_class_method_overload(
            ctx,
            cls,
            method_name,
            [p["type"] for p in params]
        )

        if method.owner != class_key:
            raise CompileError(
                ctx,
                "E0019",
                text=(
                    f"cannot implement inherited method "
                    f"{class_name}.{method_name}; "
                    f"declare it in {class_name} first"
                )
            )

        method.implemented = True
        
        skip_label = self.new_named_label(
            "skip_class_" + class_name + "_" + method_name
        )
        
        self.emit_jmp(skip_label)
        self.emit_bind_label(method.label)
        
        # rcx = Self
        self.emit_push("rbp")
        self.emit_mov("rbp", "rsp")
        self.emit_push("rcx", comment = "Self")
        
        old_params = self.current_proc_params
        self.current_proc_params = {
            "self": {
                "type"          : "^" + class_key,
                "reg"           : "rcx",
                "stack_offset"  : -8,
                "is_var"        : False
            }
        }
        
        param_regs = ["rdx", "r8", "r9"]
        
        for index, p in enumerate(params):
            pname = p["name"]
            ptype = self.resolve_type(p["type"])
            
            if index < len(param_regs):
                reg = param_regs[index]
                self.emit_push(reg, comment=f"save class method param {pname}")
                stack_offset = -8 * (index + 2)
            else:
                reg = None
                
                # Win64:
                # [rbp +  8] = return address
                # [rbp + 16] = shadow rcx
                # [rbp + 24] = shadow rdx
                # [rbp + 32] = shadow r8
                # [rbp + 40] = shadow r9
                # [rbp + 48] = erster echter Stack-Parameter
                stack_offset = 48 + ((index - len(param_regs)) * 8)
            
            self.current_proc_params[pname.lower()] = {
                "type"          : ptype,
                "reg"           : reg,
                "stack_offset"  : stack_offset,
                "is_var"        : p.get("is_var", False)
            }
        
        self.emit_sub("rsp", 256, comment = "class method locals")
        
        self.push_local_scope()
        self.push_const_scope()
        
        old_class    = self.current_class
        old_method   = self.current_method
        old_function = self.current_function

        self.current_class  = class_key
        self.current_method = method

        if method.kind == "function":
            self.current_function = {
                "name": method.name,
                "return_type": method.return_type,
                "scoped_name": class_name + "_" + method.name
            }
        
        self.visit(ctx.block())

        self.current_class    = old_class
        self.current_method   = old_method
        self.current_function = old_function
        
        self.pop_const_scope()
        self.pop_local_scope()
        
        self.current_proc_params = old_params
        
        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()
        
        self.emit_bind_label(skip_label)
        
        return None
    
    def visitDeclarationPart(self, ctx):
        if ctx is None:
            return None
        
        if hasattr(ctx, "classMethodImplementation") and ctx.classMethodImplementation():
            return self.visit(ctx.classMethodImplementation())
        
        if hasattr(ctx, "typeSection") and ctx.typeSection():
            return self.visit(ctx.typeSection())
        
        if hasattr(ctx, "constDeclaration") and ctx.constDeclaration():
            return self.visit(ctx.constDeclaration())
        
        if hasattr(ctx, "constSection") and ctx.constSection():
            return self.visit(ctx.constSection())
        
        if hasattr(ctx, "varSection") and ctx.varSection():
            return self.visit(ctx.varSection())
        
        if hasattr(ctx, "procedureDeclaration") and ctx.procedureDeclaration():
            return self.visit(ctx.procedureDeclaration())
        
        if hasattr(ctx, "functionDeclaration") and ctx.functionDeclaration():
            return self.visit(ctx.functionDeclaration())
        
        return None
    
    def visitExportsClause(self, ctx):
        for item in ctx.exportItem():
            name  = item.qualifiedIdent().getText()
            parts = name.split(".")
            
            wanted_types = []
            
            if item.exportSignature():
                lst = item.exportSignature().exportTypeList()
                
                if lst:
                    for t in lst.typeName():
                        wanted_types.append(
                            self.resolve_type(t.getText())
                        )
            
            # Klassenmethode: TFoo.Create / TFoo.Create(String) / TFoo.Add(Integer,Integer)
            if len(parts) == 2:
                class_name  = parts[0]
                method_name = parts[1]
                
                cls = self.classes.get(class_name.lower())
                
                if not cls:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"export class not found: {class_name}"
                    )
                
                overloads = cls.methods.get(method_name.lower(), [])
                
                if not overloads:
                    raise CompileError(
                        ctx,
                        "E0019",
                        text=f"export method not found: {name}"
                    )
                
                if item.exportSignature():
                    methods_to_export = [
                        self.find_export_method_overload(
                            ctx,
                            overloads,
                            wanted_types
                        )
                    ]
                else:
                    methods_to_export = overloads
                
                for method in methods_to_export:
                    export_name = (
                        class_name
                        + "_"
                        + method.name
                        + self.export_wrapper_suffix(method.params)
                    )
                    
                    self.exports.append({
                        "kind"          : "class_method",
                        "name"          : name,
                        "class_name"    : class_name,
                        "method_name"   : method.name,
                        "method_kind"   : method.kind,
                        "mangled"       : method.mangled,
                        "export_name"   : export_name,
                        "return_type"   : method.return_type,
                        "params"        : method.params
                    })
                
                continue
            
            # Normale Funktion: Add / Add(Integer,Integer)
            if wanted_types:
                func = self.find_export_function_overload(name, wanted_types)
            else:
                func = self.find_function(name)
            
            if func:
                self.exports.append({
                    "kind"          : "function",
                    "name"          : name,
                    "mangled"       : func["mangled"],
                    "export_name"   : name,
                    "return_type"   : func["return_type"],
                    "params"        : func.get("params", [])
                })
                continue
            
            key = name.lower()
            
            if key in self.procedures:
                proc = self.procedures[key]
                
                self.exports.append({
                    "kind"          : "procedure",
                    "name"          : name,
                    "mangled"       : proc["mangled"],
                    "export_name"   : name,
                    "return_type"   : None,
                    "params"        : proc.get("params", [])
                })
                continue
            
            raise CompileError(
                ctx,
                "E0019",
                text=f"export symbol not found: {name}"
            )
        
        return None
    
    def visitBlock(self, ctx):
        if ctx is None:
            return None

        local_decls = ctx.localDeclaration()

        if local_decls:
            for decl in local_decls:
                if decl is not None:
                    self.visit(decl)

        stmt_list = ctx.statementList()

        if stmt_list is not None:
            return self.visit(stmt_list)

        return None
    
    def visitBoolOrExpr(self, ctx):
        parts = list(ctx.boolXorExpr())

        if len(parts) == 1:
            return self.visit(parts[0])

        true_label = self.new_named_label("or_true")
        end_label  = self.new_named_label("or_end")

        for part in parts:
            expr_type = self.visit(part)

            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_jne(true_label)

        self.emit_xor("eax", "eax")
        self.emit_jmp(end_label)

        self.emit_bind_label(true_label)
        self.emit_mov("eax", 1)

        self.emit_bind_label(end_label)

        return "integer"
    
    def visitBoolXorExpr(self, ctx):
        result_type = self.visit(ctx.boolAndExpr(0))

        for i in range(1, len(ctx.boolAndExpr())):
            if result_type != "integer":
                raise CompileError(ctx, "E0005", got=result_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_push("rax")

            right_type = self.visit(ctx.boolAndExpr(i))

            if right_type != "integer":
                raise CompileError(ctx, "E0005", got=right_type, expected="boolean/integer")

            self.normalize_bool_eax()

            self.emit_pop("rbx")
            self.emit_mov("eax", "ebx")
            self.normalize_bool_eax()

            result_type = "integer"

        return result_type
    
    def visitBoolAndExpr(self, ctx):
        parts = list(ctx.compareExpr())

        if len(parts) == 1:
            return self.visit(parts[0])

        false_label = self.new_named_label("and_false")
        end_label   = self.new_named_label("and_end")

        for part in parts:
            expr_type = self.visit(part)

            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")

            self.normalize_bool_eax()
            self.emit_cmp("eax", 0)
            self.emit_je(false_label)

        self.emit_mov("eax", 1)
        self.emit_jmp(end_label)

        self.emit_bind_label(false_label)
        self.emit_xor("eax", "eax")

        self.emit_bind_label(end_label)

        return "integer"

    def visitBreakStatement(self, ctx):
        if not self.break_label_stack:
            raise CompileError(ctx, "E0006")
        
        self.emit_jmp(self.break_label_stack[-1], comment="break")
        return None

    def visitContinueStatement(self, ctx):
        if not self.continue_label_stack:
            raise CompileError(ctx, "E0006")
        
        self.emit_jmp(self.continue_label_stack[-1], comment="continue")
        return None

    def visitCompareExpr(self, ctx):
        left_type = self.visit(ctx.addExpr(0))

        if len(ctx.addExpr()) == 1:
            return left_type

        op = ctx.compareOp().getText()

        if left_type == "integer":
            self.emit_push("rax")
        elif isinstance(left_type, str) and left_type.startswith("^"):
            self.emit_push("rax")
        else:
            raise CompileError(ctx, "E0005", got=left_type, expected="integer/pointer")

        right_type = self.visit(ctx.addExpr(1))

        if isinstance(left_type, str) and left_type.startswith("^"):
            if right_type != left_type and right_type != "^nil":
                raise CompileError(ctx, "E0005", got=right_type, expected=left_type + "/nil")

            self.emit_mov("rbx", "rax")
            self.emit_pop("rax")
            self.emit_cmp("rax", "rbx")
        else:
            if right_type != "integer":
                raise CompileError(ctx, "E0005", got=right_type, expected="integer")

            self.emit_mov("ebx", "eax")
            self.emit_pop("rax")
            self.emit_cmp("eax", "ebx")

        true_label = self.new_named_label("cmp_true")
        end_label  = self.new_named_label("cmp_end")

        jump_map = {
            "=":  self.emit_je,
            "<>": self.emit_jne,
            "<":  self.emit_jl,
            "<=": self.emit_jle,
            ">":  self.emit_jg,
            ">=": self.emit_jge,
        }

        jump_map[op](true_label)
        self.emit_xor("eax", "eax")
        self.emit_jmp(end_label)
        self.emit_bind_label(true_label)
        self.emit_mov("eax", 1)
        self.emit_bind_label(end_label)

        return "integer"
    
    def visitRecordDeclaration(self, ctx):
        record_name = ctx.IDENT().getText()

        fields = []

        for field_ctx in ctx.recordFieldDeclaration():
            field_type = field_ctx.typeName().getText()

            for ident in field_ctx.identList().IDENT():
                fields.append((ident.getText(), field_type))

        self.declare_record(ctx, record_name, fields)
        return None
    
    def visitArrayType(self, ctx):
        dimensions = []

        if ctx.arrayRange():
            for r in ctx.arrayRange():
                min_value = int(r.expr(0).getText())
                max_value = int(r.expr(1).getText())

                dimensions.append({
                    "min": min_value,
                    "max": max_value
                })

            is_dynamic = False
        else:
            is_dynamic = True

        element_type = ctx.typeName().getText()

        return {
            "kind": "array",
            "dimensions": dimensions,
            "element_type": element_type,
            "is_dynamic": is_dynamic
        }
        
    def array_total_count(self, array_info):
        total = 1
        for dim in array_info["dimensions"]:
            total *= (dim["max"] - dim["min"] + 1)
        return total
    
    def visitArrayDeclaration(self, ctx):
        array_name = ctx.IDENT().getText()

        array_type = self.visit(ctx.arrayType())

        dimensions   = array_type["dimensions"]
        element_type = array_type["element_type"]

        # vorerst Kompatibilität für alte eindimensionale Funktionen
        index_min = dimensions[0]["min"]
        index_max = dimensions[0]["max"]

        resolved_type = self.resolve_type(element_type)

        init_values = []

        if ctx.arrayInitializer():
            value_list = ctx.arrayInitializer().arrayValueList()

            if value_list:
                for value_ctx in value_list.constValue():
                    text = value_ctx.getText()

                    if resolved_type == "integer":
                        init_values.append(int(text, 0))
                    elif resolved_type == "double":
                        init_values.append(float(text))
                    elif resolved_type == "string":
                        init_values.append(text[1:-1])
                    else:
                        raise CompileError(ctx, "E0014", var_type=resolved_type)

        self.declare_array(
            ctx,
            array_name,
            index_min,
            index_max,
            element_type,
            init_values,
            dimensions
        )

        return None
    
    def visitConstDeclaration(self, ctx):
        for item in ctx.constItem():
            self.visit(item)

        return None
    
    def visitConstItem(self, ctx):
        name = ctx.IDENT().getText()
        value_text = ctx.constValue().getText()

        if value_text.startswith("'") and value_text.endswith("'"):
            value = value_text[1:-1]
            typ = "string"

        elif "." in value_text:
            value = value_text
            typ = "double"

        else:
            value = int(value_text)
            typ = "integer"

        self.declare_const(ctx, name, value, typ)
        return None
    
    def visitEnumDeclaration(self, ctx):
        enum_name = ctx.IDENT().getText()

        values = []
        current_value = 0

        for enum_ctx in ctx.enumValueList().enumValue():
            name        = enum_ctx.IDENT().getText()
            number_node = enum_ctx.NUMBER()

            if number_node is not None:
                current_value = int(number_node.getText(), 0)

            values.append((name, current_value))
            current_value += 1

        self.declare_enum(ctx, enum_name, values)
        return None
    
    def visitTryStatement(self, ctx):
        if ctx.FINALLY():
            self.visit(ctx.statementList(0))
            self.visit(ctx.statementList(1))
            return None

        if ctx.EXCEPT():
            except_label = self.new_named_label("except")
            end_label    = self.new_named_label("endtry")

            self.try_except_stack.append({
                "except_label": except_label,
                "end_label": end_label
            })

            # try-block
            self.visit(ctx.statementList(0))

            self.try_except_stack.pop()

            # kein Fehler -> except überspringen
            self.emit_jmp(end_label)

            # except-block
            self.emit_bind_label(except_label)
            self.visit(ctx.statementList(1))

            self.emit_bind_label(end_label)
            return None

        return None
    
    def case_label_value(self, ctx, label_ctx):
        if label_ctx.NUMBER():
            return int(label_ctx.NUMBER().getText(), 0)

        if label_ctx.IDENT():
            name = label_ctx.IDENT().getText()
            const_info = self.find_const(name)

            if const_info is None:
                raise CompileError(label_ctx, "E0001", name=name)

            if const_info["type"] != "integer":
                raise CompileError(label_ctx, "E0005", got=const_info["type"], expected="integer")

            return int(const_info["value"])

        raise CompileError(label_ctx, "E0015", text=label_ctx.getText())
    
    def visitCaseStatement(self, ctx):
        end_label  = self.new_named_label("case_end")
        else_label = self.new_named_label("case_else")

        item_labels = []

        expr_type = self.visit(ctx.expr())

        if expr_type != "integer":
            raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

        self.emit_mov("ebx", "eax", comment='case selector')

        items = list(ctx.caseItem())

        for index, item in enumerate(items):
            item_label = self.new_named_label(f"case_item_{index}")
            item_labels.append((item, item_label))

            for label_ctx in item.caseLabelList().caseLabel():
                value = self.case_label_value(ctx, label_ctx)

                self.emit_cmp("ebx", value)
                self.emit_je(item_label)

        if ctx.caseElse():
            self.emit_jmp(else_label)
        else:
            self.emit_jmp(end_label)

        for item, item_label in item_labels:
            self.emit_bind_label(item_label)
            self.visit(item.statement())
            self.emit_jmp(end_label)

        if ctx.caseElse():
            self.emit_bind_label(else_label)
            self.visit(ctx.caseElse().statementList())

        self.emit_bind_label(end_label)
        return None
    
    def visitStatementList(self, ctx):
        if ctx is None:
            return None
        
        for st in ctx.statement():
            if st is not None:
                self.visit(st)
        
        return None
    
    def visitStatement(self, ctx):
        if ctx.procedureCallStatement():
            return self.visit(ctx.procedureCallStatement())
        
        if ctx.inheritedStatement():
            return self.visit(ctx.inheritedStatement())
        
        if ctx.tryStatement():
            return self.visit(ctx.tryStatement())
        
        if ctx.assignment():
            return self.visit(ctx.assignment())
        
        if ctx.writeLnStatement():
            return self.visit(ctx.writeLnStatement())
        
        if ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        
        if ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        
        if ctx.repeatStatement():
            return self.visit(ctx.repeatStatement())
        
        if ctx.forStatement():
            return self.visit(ctx.forStatement())
        
        if ctx.exitStatement():
            return self.visit(ctx.exitStatement())
        
        if ctx.caseStatement():
            return self.visit(ctx.caseStatement())
        
        if ctx.breakStatement():
            return self.visit(ctx.breakStatement())
        
        if ctx.continueStatement():
            return self.visit(ctx.continueStatement())
        
        if ctx.compoundStatement():
            return self.visit(ctx.compoundStatement())
        
        return None
    
    def visitFunctionHeader(self, ctx):
        name    = ctx.IDENT().getText()
        scoped  = self.unit_scoped_name(name)
        key     = name.lower()

        if key not in self.functions:
            self.functions[key] = {
                "name"       : name,
                "scoped_name": scoped,
                "return_type": self.resolve_type(ctx.typeName().getText()),
                "label"      : None,
                "params"     : self.collect_formal_params(ctx)
            }
        
        # zusätzlich unqualifizierter Alias für uses
        self.functions[name.lower()] = self.functions[key]
        return None
    
    def visitProcedureHeader(self, ctx):
        name    = ctx.IDENT().getText()
        scoped  = self.unit_scoped_name(name)
        key     = name.lower()

        if key not in self.procedures:
            self.procedures[key] = {
                "name"       : name,
                "scoped_name": scoped,
                "label"      : None,
                "params"     : self.collect_formal_params(ctx)
            }
            
        self.procedures[name.lower()] = self.procedures[key]
        return None
    
    def visitTypeSection(self, ctx):
        for decl in ctx.typeDeclaration():
            self.visit(decl)

        return None
        
    def visitVarSection(self, ctx):
        for decl in ctx.varDeclaration():
            self.visit(decl)
        return None
    
    def visitVarDeclaration(self, ctx):
        vtype_ctx = ctx.varType()

        if vtype_ctx.arrayType():
            array_type = self.visit(vtype_ctx.arrayType())

            dimensions   = array_type["dimensions"]
            element_type = array_type["element_type"]
            is_dynamic   = array_type.get("is_dynamic", False)

            for ident in ctx.identList().IDENT():
                name = ident.getText()

                if is_dynamic:
                    # anonymen dynamischen Array-Typ anlegen
                    array_type_name = "$dynarray_" + name.lower()
                    resolved_element_type = self.resolve_type(element_type)
                    
                    self.arrays[array_type_name] = ArrayInfo(
                        name         = array_type_name,
                        index_min    = 0,
                        index_max    = -1,
                        element_type = resolved_element_type,
                        element_size = self.type_size(ctx, resolved_element_type),
                        size         = 8,
                        init_values  = [],
                        dimensions   = [],
                        is_dynamic   = True
                    )

                    if self.local_var_stack:
                        self.declare_local_var(ctx, name, array_type_name)
                    else:
                        self.declare_var(ctx, name, array_type_name)
                else:
                    raise CompileError(ctx, "E0005", got="static inline array", expected="named array type")
            
            return None

        vtype = vtype_ctx.typeName().getText()

        for ident in ctx.identList().IDENT():
            name = ident.getText()

            if self.local_var_stack:
                self.declare_local_var(ctx, name, vtype)
            else:
                self.declare_var(ctx, name, vtype)

        return None
    
    def visitClassDeclaration(self, ctx):
        class_name = ctx.IDENT().getText()
        
        fields  = []
        methods = []
        
        parent_name         = None
        current_visibility  = "public"
        
        if ctx.classParent():
            parent_name = ctx.classParent().IDENT().getText()
        
        for member in ctx.classBody().classMember():
            
            if member.visibilitySection():
                current_visibility = member.visibilitySection().getText().lower()
                continue
                
            if member.classFieldDeclaration():
                field_ctx = member.classFieldDeclaration()
                field_type = field_ctx.typeName().getText()
                
                for ident in field_ctx.identList().IDENT():
                    fields.append((ident.getText(), field_type, current_visibility))
            
            elif member.constructorDeclaration():
                ctor = member.constructorDeclaration()
                method_name = ctor.IDENT().getText()
                
                params  = self.collect_formal_params(ctor)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )
                
                methods.append({
                    "name"      : method_name,
                    "kind"      : "constructor",
                    "label"     : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"   : mangled,
                    "params"    : params,
                    "visibility": current_visibility
                })
            
            elif member.destructorDeclaration():
                dtor = member.destructorDeclaration()
                method_name = dtor.IDENT().getText()

                params  = self.collect_formal_params(dtor)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )

                methods.append({
                    "name"      : method_name,
                    "kind"      : "destructor",
                    "label"     : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"   : mangled,
                    "params"    : params,
                    "visibility": current_visibility
                })
            
            elif member.classFunctionDeclaration():
                fn = member.classFunctionDeclaration()
                method_name = fn.IDENT().getText()
                
                params  = self.collect_formal_params(fn)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )

                methods.append({
                    "name"       : method_name,
                    "kind"       : "function",
                    "label"      : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"    : mangled,
                    "params"     : params,
                    "return_type": self.resolve_type(fn.typeName().getText()),
                    "visibility" : current_visibility
                })
            
            elif member.classProcedureDeclaration():
                proc = member.classProcedureDeclaration()
                method_name = proc.IDENT().getText()
                
                params  = self.collect_formal_params(proc)
                mangled = self.fpc_mangle_class_method(
                    class_name,
                    method_name,
                    params,
                    self.current_unit if self.current_unit else self.program_name
                )

                methods.append({
                    "name"       : method_name,
                    "kind"       : "procedure",
                    "label"      : self.new_named_label("class_" + class_name + "_" + method_name),
                    "mangled"    : mangled,
                    "params"     : params,
                    "return_type": None,
                    "visibility" : current_visibility
                })
        
        self.declare_class(ctx, class_name, fields, methods, parent_name=parent_name)
        return None
    
    def visitTypeDeclaration(self, ctx):
        if ctx.enumDeclaration():
            return self.visit(ctx.enumDeclaration())
        
        if ctx.recordDeclaration():
            return self.visit(ctx.recordDeclaration())
        
        if ctx.arrayDeclaration():
            return self.visit(ctx.arrayDeclaration())
        
        if ctx.classDeclaration():
            return self.visit(ctx.classDeclaration())
        
        type_name  = ctx.IDENT().getText()
        alias_name = ctx.typeName().getText()
        
        self.declare_type_alias(ctx, type_name, alias_name)
        return None
    
    def visitFunctionDeclaration(self, ctx):
        name = ctx.IDENT().getText()

        return_type = self.resolve_type(
            ctx.typeName().getText()
        )

        params  = self.collect_formal_params(ctx)
        
        scoped  = self.unit_scoped_name(self.scoped_name(name))
        key     = scoped.lower()

        asmjit_label = self.new_named_label("func_" + scoped)
        fpc_name     = self.fpc_mangle_routine(
            name,
            params,
            self.current_unit if self.current_unit else None)

        self.add_asm_label_mapping(
            asmjit_label,
            fpc_name
        )
        
        self.functions[key] = {
            "name": name,
            "scoped_name": scoped,
            "return_type": return_type,
            "label": asmjit_label,      # für a.bind(...)
            "mangled": fpc_name,        # für NASM / Export / Mapping
            "params": params
        }

        # globaler Alias, damit "Add" gefunden wird
        self.functions[name.lower()] = self.functions[key]

        old_function = self.current_function
        self.emit_function_declaration(ctx, scoped, return_type)
        self.current_function = old_function
        
        return None
    
    def visitAssignment(self, ctx):
        target_ctx = ctx.variableRef()
        target     = target_ctx.getText()
        expr_type  = self.visit(ctx.expr())

        if target.lower() == "result":
            self.emit_store_result(ctx, expr_type)
            return None
        
        if "." not in target and "[" not in target and "^" not in target:
            if self.emit_store_self_field(ctx, target, expr_type):
                return None
        
        param = self.find_param(target)
        if param and param.get("is_var", False):
            self.emit_store_param(ctx, target, expr_type)
            return None
        
        suffixes = target_ctx.variableSuffix()
        if suffixes:
            first     = suffixes[0]
            has_caret = any(s.CARET() for s in suffixes)
            has_dot   = any(s.DOT()   for s in suffixes)
            
            if has_caret and has_dot:
                parts = [target_ctx.IDENT().getText()]
                
                after_caret = False
                for s in suffixes:
                    if s.CARET():
                        after_caret = True
                        continue
                    
                    if after_caret and s.DOT():
                        parts.append(s.IDENT().getText())
                
                self.emit_store_pointer_record_field(ctx, parts, expr_type)
                return None
                
            if first.CARET():
                var_name = target_ctx.IDENT().getText()
                self.emit_store_pointer_deref(ctx, var_name, expr_type)
                return None
            
            if first.LBRACK():
                var_name = target_ctx.IDENT().getText()
                
                # dynamisches Array: a[0] := ...
                arr_info = self.var_info(ctx, var_name)
                arr_type = arr_info["type"]
                
                # String-Index
                if arr_type == "string":
                    self.emit_store_string_char(
                        ctx,
                        var_name,
                        list(first.expr()),
                        expr_type
                    )
                    return None
                
                # points[0].X
                if len(suffixes) > 1 and suffixes[1].DOT():
                    field_parts = []

                    for s in suffixes[1:]:
                        if s.DOT():
                            field_parts.append(s.IDENT().getText())

                    var_info, array_info = self.get_array_info(ctx, var_name)

                    if getattr(array_info, "is_dynamic", False):
                        self.emit_store_dynamic_array_record_field(
                            ctx,
                            var_name,
                            list(first.expr()),
                            field_parts,
                            expr_type
                        )
                        return None

                    self.emit_store_array_record_field(
                        ctx,
                        var_name,
                        list(first.expr()),
                        field_parts,
                        expr_type
                    )
                    return None
                
                # dynamisches Array: a[0] := ...
                if getattr(arr_type, "is_dynamic", False):
                    self.emit_store_dynamic_array_element(
                        ctx,
                        var_name,
                        list(first.expr()),
                        expr_type
                    )
                    return None
                
                # statisches Array: a[0] := ...
                self.emit_store_array_element(
                    ctx,
                    var_name,
                    list(first.expr()),
                    expr_type
                )
                return None
            
            if first.DOT():
                parts = [target_ctx.IDENT().getText()]

                for s in suffixes:
                    if s.DOT():
                        parts.append(s.IDENT().getText())

                var_name = parts[0]
                var_info = self.var_info(ctx, var_name)
                var_type = self.resolve_type(var_info["type"])

                # Klasse: foo.field := ...
                if isinstance(var_type, str) and var_type in self.classes:
                    self.emit_store_class_field(ctx, parts, expr_type)
                    return None
                
                # Record: rec.field := ...
                self.emit_store_record_field(ctx, parts, expr_type)
                return None
        
        if self.find_const(target):
            raise CompileError(ctx, "E0010", name=target)
        
        local_var = self.find_local_var(target)
        if local_var:
            self.emit_store_local_var(ctx, target, expr_type)
            return None
        
        var_info = self.var_info(ctx, target)
        var_type = var_info["type"]
        
        if isinstance(var_type, str) and var_type.startswith("^"):
            if expr_type == var_type or expr_type == "^nil":
                self.emit_store_var(ctx, target, var_info)
                return None
        
        if var_type in self.classes:
            if expr_type != var_type:
                raise CompileError(ctx, "E0005", got=expr_type, expected=var_type)
            
            self.emit_store_object_var(ctx, target, var_info)
            return None
        
        if var_type == "double" and expr_type == "integer":
            self.emit_cvtsi2sd("xmm0", "eax")
            expr_type = "double"
            
        if var_type != expr_type:
            raise CompileError(ctx, "E0005", got=expr_type, expected=var_type)

        self.emit_store_var(ctx, target, var_info)
        return None
    
    def visitExpr(self, ctx):
        return self.visit(ctx.boolOrExpr())
    
    def visitAddExpr(self, ctx):
        result_type = self.visit(ctx.term(0))

        for i in range(1, len(ctx.term())):
            op = ctx.getChild(2 * i - 1).getText()

            # String-Verkettung nur mit +
            if result_type == "string":
                if op != "+":
                    raise CompileError(ctx, "E0005", got="string -", expected="string + string")

                self.emit_push("rax", comment='save left string')

                right_type = self.visit(ctx.term(i))

                if right_type != "string":
                    raise CompileError(ctx, "E0005", got=right_type, expected="string")

                self.emit_mov("rdx", "rax", comment="right string")
                self.emit_pop(rcx         , comment="left string")
                self.emit_mov_imm("rax", "&_jit_dynstring_concat")
                self.emit_call_rax()

                result_type = "string"
                continue

            if result_type == "integer":
                self.emit_push("rax")

                right_type = self.visit(ctx.term(i))

                # 'test' + S
                if right_type == "string":
                    if op != "+":
                        raise CompileError(ctx, "E0005", got="integer/string", expected="string + string")

                    self.emit_mov("rdx", "rax", comment = "right string")
                    self.emit_pop("rcx"       , comment = "left string/char literal")

                    self.emit_mov_imm("rax", "&_jit_dynstring_concat")
                    self.emit_call_rax()

                    result_type = "string"
                    continue

                if right_type == "integer":
                    self.emit_mov("ebx", "eax")
                    self.emit_pop("rax")

                    if op == "+":
                        self.emit_add("eax", "ebx")
                    elif op == "-":
                        self.emit_sub("eax", "ebx")

                    result_type = "integer"
                    continue

                self.emit_pop("rax")
                self.emit_cvtsi2sd("xmm1", "eax")
                result_type = "double"

            self.emit_sub("rsp", 8)
            self.emit_movsd_store("rsp", 0, "xmm0")

            right_type = self.visit(ctx.term(i))

            if right_type == "integer":
                self.emit_cvtsi2sd("xmm0", "eax")

            self.emit_movsd_load("xmm1", "rsp", 0)
            self.emit_add("rsp", 8)

            if op == "+":
                self.emit_addsd("xmm0", "xmm1")
            elif op == "-":
                self.emit_movapd("xmm2", "xmm0")
                self.emit_movapd("xmm0", "xmm1")
                self.emit_subsd("xmm0", "xmm2")

            result_type = "double"

        return result_type
    
    def visitTerm(self, ctx):
        result_type = self.visit(ctx.factor(0))

        for i in range(1, len(ctx.factor())):
            op = ctx.getChild(2 * i - 1).getText()

            if result_type == "integer":
                self.emit_push("rax")

                right_type = self.visit(ctx.factor(i))

                if right_type == "integer":
                    self.emit_mov("ebx", "eax")
                    self.emit_pop("rax")

                    if op == "*":
                        self.emit_imul("eax", "ebx")
                        result_type = "integer"

                    elif op == "/":
                        self.emit_cdq()
                        self.emit_idiv("ebx")
                        result_type = "integer"

                    continue

                self.emit_pop("rax")
                self.emit_cvtsi2sd("xmm1", "eax")
                result_type = "double"

            else:
                self.emit_sub("rsp", 8)
                self.emit_movsd_store("rsp", 0, "xmm0")

                right_type = self.visit(ctx.factor(i))

                self.emit_movsd_load("xmm1", "rsp", 0)
                self.emit_add("rsp", 8)

            if result_type == "double":
                if right_type == "integer":
                    self.emit_cvtsi2sd("xmm0", "eax")

                if op == "*":
                    self.emit_mulsd("xmm0", "xmm1")

                elif op == "/":
                    self.emit_movapd("xmm2", "xmm0")
                    self.emit_movapd("xmm0", "xmm1")
                    self.emit_divsd("xmm0", "xmm2")

                result_type = "double"

        return result_type
    
    def visitFactor(self, ctx):
        text = ctx.getText()
        key  = text.lower()
        
        if ctx.NOT():
            expr_type = self.visit(ctx.factor())
            
            if expr_type != "integer":
                raise CompileError(ctx, "E0005", got=expr_type, expected="boolean/integer")
                
            self.normalize_bool_eax()
            self.emit_xor("eax", 1, comment = "not")
            return "integer"
        
        if key in self.constants:
            c = self.constants[key]
            
            if c["type"] == "integer":
                self.emit_mov("eax", f"{c['value']}")
                return "integer"
                
            if c["type"] == "double":
                return self.emit_load_double_literal(c["value"])
                
            if c["type"] == "string":
                label = self.add_string_literal(c["value"])
                self.emit_mov_imm("rax", label)
                return "string"
        
        if ctx.AT():
            ref = ctx.variableRef()
            name = ref.IDENT().getText()
            suffixes = ref.variableSuffix()
            
            if suffixes:
                first = suffixes[0]
                
                if first.LBRACK():
                    return self.emit_address_of_array_element(
                        ctx,
                        name,
                        list(first.expr())
                    )
            
            return self.emit_address_of_var(ctx, name)
        
        # Function call zuerst
        if ctx.functionCallExpr():
            return self.visit(ctx.functionCallExpr())
        
        if ctx.variableRef():
            ref      = ctx.variableRef()
            suffixes = ref.variableSuffix()
            name     = ref.IDENT().getText()

            if not suffixes:
                self_field_type = self.emit_load_self_field(ctx, name)
                if self_field_type is not None:
                    return self_field_type
            
            if suffixes:
                first     = suffixes[0]
                has_caret = any(s.CARET() for s in suffixes)
                has_dot   = any(s.DOT()   for s in suffixes)
                
                if has_caret and has_dot:
                    parts = [ref.IDENT().getText()]
                    
                    after_caret = False
                    for s in suffixes:
                        if s.CARET():
                            after_caret = True
                            continue
                        
                        if after_caret and s.DOT():
                            parts.append(s.IDENT().getText())
                    
                    return self.emit_load_pointer_record_field(ctx, parts)
                
                if first.CARET():
                    var_name = ref.IDENT().getText()
                    return self.emit_load_pointer_deref(ctx, var_name)
                
                if first.LBRACK():
                    var_name = ref.IDENT().getText()
                    var_info = self.var_info(ctx, var_name)
                    var_type = var_info["type"]
                    
                    # Spezialfall: s[0] = ganzer String
                    if var_type == "string":
                        index_exprs = list(first.expr())
                        
                        if len(index_exprs) == 1 and index_exprs[0].getText() == "0":
                            self.emit_load_var(var_name, var_info)   # RAX = char*
                            return "string"
                        
                        return self.emit_load_string_char(
                            ctx,
                            var_name,
                            index_exprs
                        )
                    
                    # points[0].X
                    if len(suffixes) > 1 and suffixes[1].DOT():
                        field_parts = []
                        
                        for s in suffixes[1:]:
                            if s.DOT():
                                field_parts.append(s.IDENT().getText())
                        
                        var_info, array_info = self.get_array_info(ctx, var_name)
                        
                        if getattr(array_info, "is_dynamic", False):
                            return self.emit_load_dynamic_array_record_field(
                                ctx,
                                var_name,
                                list(first.expr()),
                                field_parts
                            )
                        
                        return self.emit_load_array_record_field(
                            ctx,
                            var_name,
                            list(first.expr()),
                            field_parts
                        )
                    
                    # normales a[0]
                    return self.emit_load_array_element(
                        ctx,
                        var_name,
                        list(first.expr())
                    )
                
                if first.DOT():
                    parts = [ref.IDENT().getText()]
                    
                    for s in suffixes:
                        if s.DOT():
                            parts.append(s.IDENT().getText())
                    
                    # TFoo.Create
                    if len(parts) == 2:
                        class_name  = parts[0]
                        method_name = parts[1]
                        
                        if (
                            class_name.lower() in self.classes
                            and method_name.lower() == "create"
                        ):
                            return self.emit_class_constructor_call(
                                ctx,
                                class_name,
                                method_name
                            )
                    
                    var_name = parts[0]
                    var_info = self.var_info(ctx, var_name)
                    var_type = self.resolve_type(var_info["type"])
                    
                    if isinstance(var_type, str) and var_type in self.classes:
                        return self.emit_load_class_field(ctx, parts)
                    
                    return self.emit_load_record_field(ctx, parts)
            
            name = ref.IDENT().getText()
            
            local_var = self.find_local_var(name)
            if local_var:
                return self.emit_load_local_var(ctx, name, local_var)
            
            param = self.find_param(name)
            if param:
                return self.emit_load_param(ctx, name)
            
            const_info = self.find_const(name)
            if const_info:
                return self.emit_load_const(ctx, name)
            
            key = name.lower()
            if key in self.vars:
                info = self.var_info(ctx, name)
                self.emit_load_var(name, info)
                return info["type"]
            
            if self.current_class is not None:
                try:
                    return self.emit_self_method_call(ctx, name, [])
                except CompileError:
                    pass
            
            func = self.find_function(name)
            if func:
                params = func.get("params", [])
                
                if len(params) == 0:
                    self.emit_sub("rsp", 32, comment = "shadow space for parameterless function call")
                    self.emit_call(f"{func['label']}")
                    self.emit_add("rsp", 32)
                    return func["return_type"].lower()
                
                raise CompileError(ctx, "E0005", got="0", expected=str(len(params)))
            
            raise CompileError(ctx, "E0001", name=name)
        
        # Klammerausdruck nur wenn wirklich vorhanden
        expr_list = ctx.expr()
        if expr_list:
            if isinstance(expr_list, list):
                if len(expr_list) > 0:
                    return self.visit(expr_list[0])
            else:
                return self.visit(expr_list)
        
        if ctx.NIL():
            self.emit_xor("rax", "rax", comment = "nil")
            return "^nil"
        
        # Integer
        if ctx.NUMBER():
            value = ctx.NUMBER().getText()
            self.emit_mov_imm("eax", value)
            #self.emit(f"a.mov(x86::eax, {value});")
            return "integer"
        
        # Double
        if ctx.FLOATNUMBER():
            value = ctx.FLOATNUMBER().getText()
            return self.emit_load_double_literal(value)
        
        # String
        if ctx.STRING():
            value = ctx.STRING().getText()[1:-1]
            label = self.add_string_literal(value)
            
            self.emit_mov_imm("rax", label)
            #self.emit_mov_imm("rax", label)
            
            if len(value) == 1:
                return "char"
            
            self.emit_mov("rcx", "rax")
            self.emit_mov_imm("rax", "&_jit_dynstring_from_cstr")
            self.emit_call_rax()
            
            return "string"
        
        # Identifier
        if ctx.IDENT():
            name = ctx.IDENT().getText()
            
            local_var = self.find_local_var(name)
            if local_var:
                return self.emit_load_local_var(ctx, name, local_var)
            
            param = self.find_param(name)
            if param:
                return self.emit_load_param(ctx, name)
            
            self_field_type = self.emit_load_self_field(ctx, name)
            if self_field_type is not None:
                return self_field_type
            
            const_info = self.find_const(name)
            if const_info:
                return self.emit_load_const(ctx, name)
            
            key = name.lower()
            if key in self.vars:
                info = self.var_info(ctx, name)
                self.emit_load_var(name, info)
                return info["type"]
            
            func      = self.find_function(name)
            local_var = self.find_local_var(name)
            
            if local_var:
                return self.emit_load_local_var(ctx, name, local_var)
            
            param = self.find_param(name)
            if param:
                return self.emit_load_param(name)
            
            # globale Variable
            key = name.lower()
            if key in self.vars:
                info = self.var_info(ctx, name)
                self.emit_load_var(name, info)
                return info["type"]
            
            if self.current_class is not None:
                try:
                    return self.emit_self_method_call(ctx, name, [])
                except CompileError:
                    pass
            
            # parameterlose Funktion ohne Klammern:
            func = self.find_function(name)
            if func:
                params = func.get("params", [])
                
                if len(params) == 0:
                    self.emit_sub("rsp", 32, comment = "shadow space for parameterless function call")
                    self.emit_call(f"{func['label']}")
                    self.emit_add("rsp", 32)
                    return func["return_type"].lower()
                
                raise CompileError(ctx, "E0005", got="0", expected=str(len(params)))
            
            raise CompileError(ctx, "E0001", name=name)
        
        raise CompileError(ctx, "E0015", text=text)
    
    def visitFunctionCallExpr(self, ctx):
        idents = list(ctx.IDENT())

        if len(idents) >= 2:
            left_name   = idents[0].getText()
            method_name = idents[1].getText()

            if method_name.lower() == "create":
                return self.emit_class_constructor_call(
                    ctx,
                    left_name,
                    method_name
                )
        
        name = ctx.IDENT().getText()
        key  = name.lower()
        
        if key == "assigned":
            return self.emit_builtin_assigned(ctx)
        
        if key == "length":
            return self.emit_builtin_length(ctx)
        
        if key == "copy":
            return self.emit_builtin_copy(ctx)
        
        if key == "pos":
            return self.emit_builtin_pos(ctx)
        
        func = self.find_function(name)

        if func is None:
            raise CompileError(ctx, "E0001", name=name)
        
        params = func.get("params", [])

        actuals = []
        if ctx.argumentList():
            actuals = list(ctx.argumentList().expr())

        if len(actuals) != len(params):
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected=str(len(params)))

        int_regs = ["ecx", "edx", "r8d", "r9d"]

        for index, arg_expr in enumerate(actuals):
            formal = params[index]

            if formal["type"] == "integer":
                expr_type = self.visit(arg_expr)

                if expr_type != "integer":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

                self.emit_mov(int_regs[index], "eax")
            else:
                raise CompileError(ctx, "E0005", got=formal["type"], expected="integer")

        self.emit_sub("rsp", 32, comment = "shadow space for function call")
        self.emit_call_lbl(func["label"])
        self.emit_add("rsp", 32)

        return func["return_type"].lower()
    
    def visitProcedureDeclaration(self, ctx):
        name = ctx.IDENT().getText()
        key  = name.lower()

        label      = self.new_named_label("proc_"     + name)
        skip_label = self.new_named_label("skipproc_" + name)
        exit_label = self.new_named_label("exitproc_" + name)

        params = self.collect_formal_params(ctx)

        self.procedures[key] = {
            "name"  : name,
            "label" : label,
            "params": params
        }

        param_regs = ["rcx", "rdx", "r8", "r9"]
        
        if len(params) > 64:
            raise CompileError(ctx, "E0005", got=str(len(params)), expected="max 64 params")
            
        #if len(params) > len(param_regs):
        #    raise CompileError(ctx,
        #        "E0005",
        #        got="too many params",
        #        expected="max 4 params")
        
        self.emit_jmp(skip_label)
        self.emit_bind_label(label)
        
        self.emit_push("rbp")
        self.emit_mov("rbp", "rsp")
        
        old_params = self.current_proc_params
        self.current_proc_params = {}
        
        #for index, p in enumerate(params):
        #    reg = param_regs[index]
        #    pname = p["name"]
        #    self.emit_push(reg, comment=f"save param {pname}")
        #    
        #    self.current_proc_params[p["name"].lower()] = {
        #        "type": p["type"],
        #        "reg": param_regs[index],
        #        "stack_offset": -8 * (index + 1),
        #        "is_var": p.get("is_var", False)
        #    }
        
        for index, p in enumerate(params):
            pname = p["name"]
            ptype = self.resolve_type(p["type"])
            
            
            if index < 4:
                reg = param_regs[index]
                self.emit_push(reg, comment=f"save param {pname}")
                stack_offset = -8 * (index + 1)
            else:
                reg = None
                stack_offset = 48 + ((index - 4) * 8)

            self.current_proc_params[pname.lower()] = {
                "type": ptype,
                "reg": reg,
                "stack_offset": stack_offset,
                "is_var": p.get("is_var", False)
            }
        
        saved_param_count = min(len(params), 4)
        
        if saved_param_count % 2 == 1:
            self.emit_sub("rsp", 8, comment = "align stack after odd param saves")
    
        self.emit_sub("rsp", 512, comment = "local variables")
        
        self.exit_label_stack.append(exit_label)
        self.push_local_scope()
        
        saved_param_count = min(len(params), 4)
        self.current_local_scope()["next_offset"] = saved_param_count * 8
        
        block_ctx = ctx.block()
        if block_ctx is None:
            raise CompileError(ctx, "E0015", text="procedure block missing")

        self.visit(block_ctx)
        
        self.pop_local_scope()
        self.exit_label_stack.pop()
        
        self.emit_bind_label(exit_label)
        self.current_proc_params = old_params
        
        self.emit_mov("rsp", "rbp")
        self.emit_pop("rbp")
        self.emit_ret()
        
        self.emit_bind_label(skip_label)
        return None
    
    def visitProcedureCallStatement(self, ctx):
        idents     = list(ctx.IDENT())
        name       = idents[0].getText()
        key        = name.lower()
        param_regs = ["rcx", "rdx", "r8", "r9"]

        if ctx.DOT():
            obj_name    = idents[0].getText()
            method_name = idents[1].getText()

            if method_name.lower() == "free":
                return self.emit_class_free_call(ctx, obj_name)
                
        if key == "new":
            return self.emit_builtin_new(ctx)

        if key == "dispose":
            return self.emit_builtin_dispose(ctx)

        if key == "setlength":
            return self.emit_builtin_setlength(ctx)
        
        if key == "readln":
            return self.emit_builtin_readln(ctx)
        
        if key == "__debug_break":
            return self.emit_builtin_debug_break()
        
        if key not in self.procedures:
            raise CompileError(ctx, "E0001", name=name)
        
        proc    = self.procedures[key]
        params  = proc["params"]
        actuals = []
        
        if ctx.actualParamList():
            actuals = list(ctx.actualParamList().actualParam())
        
        if len(actuals) != len(params):
            raise CompileError(ctx, "E0005", got=str(len(actuals)), expected=str(len(params)))
        
        def emit_push_argument(index):
            arg         = actuals[index]
            formal      = params[index]
            formal_type = self.resolve_type(formal["type"])

            if formal.get("is_var", False):
                ref = self.actual_param_variable_ref(ctx, arg)

                if ref is None:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got="expression",
                        expected="addressable variable"
                    )

                # einfache Variable: Head
                var_name = ref.IDENT(0).getText()

                info = self.find_local_var(var_name)
                if info is None:
                    info = self.var_info(ctx, var_name)

                actual_type = self.resolve_type(info["type"])

                if actual_type != formal_type:
                    raise CompileError(
                        ctx,
                        "E0005",
                        got      = actual_type,
                        expected = formal_type
                    )

                self.emit_address_of_var(ctx, var_name)
                self.emit_push("rax", comment='var parameter')
                return

            expr_type = self.visit_actual_param_expr(arg)

            if formal_type == "integer":
                if expr_type != "integer":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="integer")

                self.emit_movsxd("rax", "eax")
                self.emit_push("rax", comment = "integer parameter")
                return

            if formal_type == "string":
                if expr_type != "string":
                    raise CompileError(ctx, "E0005", got=expr_type, expected="string")

                self.emit_push("rax", comment='string parameter')
                return

            if isinstance(formal_type, str) and formal_type.startswith("^"):
                if expr_type != formal_type and expr_type != "^nil":
                    raise CompileError(ctx, "E0005", got=expr_type, expected=formal_type)

                self.emit_push("rax", comment='pointer parameter')
                return

            raise CompileError(ctx, "E0005", got=formal_type, expected="integer/string/pointer")

        # Parameter 5..N rückwärts auf Stack legen
        stack_count = 0
        for index in range(len(actuals) - 1, 3, -1):
            emit_push_argument(index)
            stack_count += 1

        # Parameter 1..4 rückwärts auswerten und temporär sichern
        reg_count = min(4, len(actuals))
        for index in range(reg_count - 1, -1, -1):
            emit_push_argument(index)

        for index in range(reg_count):
            self.emit_pop(param_regs[index], comment=f"load parameter {index + 1}")

        align_pad = 0

        if stack_count % 2 == 1:
            self.emit_sub("rsp", 8, comment="align stack before procedure call")
            align_pad = 8

        self.emit_sub("rsp", 32, comment = "Windows x64 shadow space")
        self.emit_call(f"{proc['label']}")
        self.emit_add("rsp", 32)

        if align_pad:
            self.emit_add("rsp", 8, comment = "remove stack alignment padding")

        if stack_count > 0:
            self.emit_add(f"rsp", {stack_count * 8}, comment = "remove stack parameters")

        return None
    
    def visitIfStatement(self, ctx):
        self.emit_if_statement(ctx)
        return None
    
    def visitCompoundStatement(self, ctx):
        return self.visit(ctx.statementList())
    
    def visitWhileStatement(self, ctx):
        self.emit_while_statement(ctx)
        return None
    
    def visitRepeatStatement(self, ctx):
        return self.emit_repeat_statement(ctx)
    
    def visitForStatement(self, ctx):
        return self.emit_for_statement(ctx)
    
    def visitWriteLnStatement(self, ctx):
        args = ctx.writeArgList()
        
        if args:
            for arg in args.writeArg():
                if arg.STRING():
                    value = arg.STRING().getText()[1:-1]
                    label = self.add_string_literal(value)

                    self.emit_mov_imm("rcx", f"{label}")
                    self.emit_mov_imm("rax", "&_jit_print_text")
                    self.emit_call_rax()
                    
                else:
                    if arg.expr() and arg.expr().getText().lower() in self.current_proc_params:
                        pname = arg.expr().getText().lower()
                        pinfo = self.current_proc_params[pname]
                        
                        if pinfo["type"] == "integer":
                            offset = pinfo["stack_offset"]
                            offset = pinfo["stack_offset"]
                            self.emit_mov_dword_ptr("eax", "rbp", offset, comment=f"load integer parameter")
                            self.emit_mov("ecx", "eax")
                            self.emit_mov_imm("rax", "&_jit_print_int")
                            self.emit_call_rax()
                            continue
                            
                        if pinfo["type"] == "string":
                            offset = pinfo["stack_offset"]
                            self.emit_mov_qword_ptr("rcx", "rbp", offset, comment=f"load string parameter")
                            self.emit_mov_imm("rax", "&_jit_print_text")
                            self.emit_call_rax()
                            continue
                    
                    expr_type = self.visit(arg.expr())
                    
                    if expr_type == "char":
                        self.emit_mov("ecx", "eax")
                        self.emit_mov_imm("rax", "&_jit_print_char")
                        self.emit_call_rax()
                    
                    if expr_type == "string":
                        self.emit_mov("rcx", "rax")
                        self.emit_mov_imm("rax", "&_jit_print_text")
                        self.emit_call_rax()
                    
                    if expr_type == "integer":
                        self.emit_mov("ecx", "eax")
                        self.emit_mov_imm("rax", "&_jit_print_int")
                        self.emit_call_rax()
                    
                    elif expr_type == "double":
                        # Windows x64: double-Argument liegt in xmm0
                        self.emit_mov_imm("rax", "&_jit_print_double")
                        self.emit_call_rax()
        
        self.emit_mov_imm("rax", "&_jit_print_newline")
        self.emit_call_rax()
        
        return None
    
    def cpp_escape(self, text):
        return (
            text
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
    
    def new_named_label(self, prefix):
        name = self.new_label_name(prefix)
        asmjit_label = f"L{len(self.asm_label_mappings)}"

        self.emit_new_label_decl(name)

        self.add_asm_label_mapping(
            asmjit_label,
            name
        )

        return name
    
    def render_asm_exports(self):
        out = []

        for item in self.exports:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"global {item["mangled"]}" << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'global {item["mangled"]}')

        if out:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append('{ASM_OUT_PH}std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(NL)

        return "\n".join(out)
    
    def render_asm_double_replacements(self):
        out = []
        for name, value in self.double_literals:
            out.append(
                f'replace_all(asm_text, std::to_string(_double_to_bits({value})), "{name}");'
            )
        return "\n    ".join(out)
        
    def render_asm_string_replacements(self):
        out = []
        for name, text in self.string_literals:
            out.append(
                f'replace_all(asm_text, std::to_string((uint64_t)&{name}), "_{name}");'
            )
        return "\n    ".join(out)
    
    def render_string_literals(self):
        out = []

        for name, text in self.string_literals:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'static const char {name}[] = "{self.cpp_escape(text)}";')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'{name}: db "{self.cpp_escape(text)}", 0')

        return "\n".join(out)
    
    def render_asm_double_symbols(self):
        out = []
        for name, value in self.double_literals:
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"{name} equ " << std::to_string(_double_to_bits({value})) << " ; {value}" << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'{name} equ {value}' + NL)
        return "\n    ".join(out)
    
    def render_asm_nasm_header(self):
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            return (
                f'{ASM_OUT_PH}std::endl << "; {COMMENT_REPL}"' + NL +
                f'{ASM_OUT_PH}std::endl << "; GENERATED WITH PYTHON 3.14 ON: {dt.now().strftime("%Y-%m-%d")}"' + NL +
                f'{ASM_OUT_PH}std::endl << "; Copyright (c) 2026 by Jens Kallup - paule32"' + NL +
                f'{ASM_OUT_PH}std::endl << "; all rights reserved."' + NL +
                f'{ASM_OUT_PH}std::endl << "; {COMMENT_REPL}"'  + NL + NL +
                f'')
        elif CDATA.BackEnd.current == BACKEND_NASM:
            return ""
    
    def render_asm_nasm_structs(self):
        result = ""
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = (
                f'{ASM_OUT_PH}"struc JitContext\n";'                         + NL +
                f'{ASM_OUT_PH}"    .int_vars:         resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .double_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .string_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .record_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .arrays_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .pointr_vars:      resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .print_int_tmp:    resd 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"    .print_double_tmp: resq 1" << std::endl;' + NL +
                f'{ASM_OUT_PH}"endstruc" << std::endl << std::endl;'         + NL +
                f'')
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = (
                f'struc JitContext'            + NL +
                f'  .int_vars:         resq 1' + NL +
                f'  .double_vars:      resq 1' + NL +
                f'  .string_vars:      resq 1' + NL +
                f'  .record_vars:      resq 1' + NL +
                f'  .arrays_vars:      resq 1' + NL +
                f'  .pointr_vars:      resq 1' + NL +
                f'  .print_int_tmp:    resd 1' + NL +
                f'  .print_double_tmp: resq 1' + NL +
                f'endstruc'                    + NL +
                f''
            )
        return result

    def render_asm_context_data(self,
        int_count,
        double_count,
        string_count,
        record_count,
        arrays_count,
        pointr_count):
        
        std_end = " << std::endl"
        result  = ""
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = [
                f'{ASM_OUT_PH}std::endl << "section .data"{std_end};',
                f'{ASM_OUT_PH}"ctx:"{std_end};',
                f'{ASM_OUT_PH}"    istruc JitContext"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.int_vars,         dq int_vars"   {std_end};',
                f'{ASM_OUT_PH}"        at JitContext.double_vars,      dq double_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.string_vars,      dq string_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.record_vars,      dq record_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.arrays_vars,      dq arrays_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.pointr_vars,      dq pointr_vars"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.print_int_tmp,    dd 0"{std_end};',
                f'{ASM_OUT_PH}"        at JitContext.print_double_tmp, dq 0"{std_end};',
                f'{ASM_OUT_PH}"    iend"{std_end};',
                f'{ASM_OUT_PH}std::endl;',
                f'{ASM_OUT_PH}"int_vars:    times {int_count} dd 0" {std_end};',
                f'{ASM_OUT_PH}"double_vars: times {double_count} dq 0"{std_end};',
                f'{ASM_OUT_PH}"string_vars: times {string_count} dq 0"{std_end};',
                f'{ASM_OUT_PH}"record_vars: times {record_count} db 0"{std_end};',
                f'{ASM_OUT_PH}"arrays_vars: times {arrays_count} db 0"{std_end};',
                f'{ASM_OUT_PH}"pointr_vars: times {pointr_count} dq 0"{std_end};',
                f'{ASM_OUT_PH}std::endl;',
                f'']
            result = NL.join(result) + NL
            return result
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = [
                f"section .data",
                f"ctx:",
                f"istruc JitContext",
                f"  at JitContext.int_vars,         dq int_vars",
                f"  at JitContext.double_vars,      dq double_vars",
                f"  at JitContext.string_vars,      dq string_vars",
                f"  at JitContext.record_vars,      dq record_vars",
                f"  at JitContext.arrays_vars,      dq arrays_vars",
                f"  at JitContext.pointr_vars,      dq pointr_vars",
                f"  at JitContext.print_int_tmp,    dd 0",
                f"  at JitContext.print_double_tmp, dq 0",
                f"iend",
                f"",
                f"",
                f"int_vars:    times {int_count} dd 0",
                f"double_vars: times {double_count} dq 0",
                f"string_vars: times {string_count} dq 0",
                f"record_vars: times {record_count} db 0",
                f"arrays_vars: times {arrays_count} db 0",
                f"pointr_vars: times {pointr_count} dq 0",
                f""]
            result = NL.join(result) + NL
            return result
        else:
            return "<unknown backend>"

    def render_asm_context_replacements(self):
        result = ""
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = (
                r'replace_all(asm_text, "[r12]",     "[r12 + JitContext.int_vars]"        );' + NL +
                r'replace_all(asm_text, "[r12+8]",   "[r12 + JitContext.double_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+16]",  "[r12 + JitContext.string_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+24]",  "[r12 + JitContext.record_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+32]",  "[r12 + JitContext.arrays_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+40]",  "[r12 + JitContext.pointr_vars]"     );' + NL +
                r'replace_all(asm_text, "[r12+48]",  "[r12 + JitContext.print_int_tmp]"   );' + NL +
                r'replace_all(asm_text, "[r12+56]",  "[r12 + JitContext.print_double_tmp]");' + NL +
                r""
            )
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = ""
        return result
    
    def render_asm_extern_symbols(self):
        out = []

        if not self.emit_local_string_data:
            for name, text in self.string_literals:
                if CDATA.BackEnd.current == BACKEND_ASMJIT:
                    out.append(f'{ASM_OUT_PH}"extern _{name}"; << std::endl')
                elif CDATA.BackEnd.current == BACKEND_NASM:
                    out.append(f'extern _{name}')

            if self.string_literals:
                if CDATA.BackEnd.current == BACKEND_ASMJIT:
                    out.append(f'{ASM_OUT_PH}std::endl;')
                elif CDATA.BackEnd.current == BACKEND_NASM:
                    out.append(NL)

        func_list = [
            "print_text",
            "print_int",
            "print_double",
            "print_newline",
            "",
            "new_memory",
            "dispose_memory",
            "",
            "dynarray_setlength",
            "",
            "dynstring_from_cstr",
            "dynstring_setlength",
            "dynstring_length",
            "dynstring_concat",
            "dynstring_copy",
            "dynstring_pos",
            "",
            "set_exception",
            "runtime_error",
            "",
            "nil_pointer_error",
            "out_of_memory_error",
            "array_bounds_error",
            "string_range_error",
            "",
            "debug_break",
            "",
            "ExitProcess"
        ]
        for fun in func_list:
            if len(fun) > 1:
                if CDATA.BackEnd.current == BACKEND_ASMJIT:
                    out.append(f'{ASM_OUT_PH}"extern _jit_{fun}" << std::endl;')
                    continue
                elif CDATA.BackEnd.current == BACKEND_NASM:
                    out.append(f'extern _jit_{fun}')
                    continue
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append('{ASM_OUT_PH}std::endl;')

        return NL.join(out) + NL
    
    def render_asm_symbol_mappings(self):
        out = []

        for name, text in self.string_literals:
            out.append(
                f'symbols.add(std::to_string((uint64_t)&{name}), "_{name}");'
            )
        out.append("")
        out.append(f'_jit_symbols_add(symbols);')

        return "\n    ".join(out)
        
    def render_asm_string_data(self):
        if not self.emit_local_string_data:
            return ""

        out = []
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            out.append('{ASM_OUT_PH}std::endl << "section .data" << std::endl;')
        elif CDATA.BackEnd.current == BACKEND_NASM:
            out.append('section .data' + NL)

        for name, text in self.string_literals:
            escaped = self.cpp_escape(text)
            if CDATA.BackEnd.current == BACKEND_ASMJIT:
                out.append(f'{ASM_OUT_PH}"_{name} db \\"{escaped}\\", 0" << std::endl;')
            elif CDATA.BackEnd.current == BACKEND_NASM:
                out.append(f'_{name} db \"{escaped}\", 0' + NL)
        
        return "\n    ".join(out)
    
    def render_asm_label_mappings(self):
        out = []
        for item in self.asm_label_mappings:
            out.append(f'labels.add("{item["asmjit"]}", "{item["target"]}");')
        return "\n    ".join(out)
        
    def render_cpp(self):
        body            = "\n".join(self.lines)
        
        var_count       = max(257, self.next_slot)
        int_count       = max(  1, self.next_int_slot)
        
        double_count    = max(  1, self.next_double_slot)
        string_count    = max(  1, self.next_string_slot)
        record_count    = max(  1, self.next_record_slot)
        arrays_count    = max(  1, self.next_arrays_slot)
        pointr_count    = max(  1, self.next_pointr_slot)
        
        # todo !!!
        self.func_name  = "main"
        self.date_str   = dt.now().strftime("%Y-%m-%d")
        
        module_kind     = self.module_kind_value
        
        src_comment     = ('-' * 77)
        src_linecom     = ""
        
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            src_linecom = "//"
        else:
            src_linecom = ";"
        
        output_header   = (
            f"{src_linecom} {src_comment}"                                                    + NL +
            f"{src_linecom} AUTOMATIC GENERATED WITH Python 3.14 SCRIPT ON: {self.date_str}"  + NL +
            f"{src_linecom}"                                                                  + NL +
            f"{src_linecom} DON'T MODIFIED THIS CODE. ALL CHANGES WILL BE LOST BY NEXT RUN !" + NL +
            f"{src_linecom} Copyright (c) 2026 by Jens Kallup - paule32"                      + NL +
            f"{src_linecom} all rights reserved."                                             + NL +
            f"{src_linecom} {src_comment}"                                                    + NL +
            f""
        )
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            result = [
                output_header,
                '# include "runtime/dbase2many.hpp"',
                '',
                'using namespace std;' ,
                'using namespace asmjit;' ,
                '' ,
                f'static constexpr int DBASE2MANY_MODULE_KIND = {self.module_kind_value};',
                '' ,
                f'{self.render_string_literals()}' ,
                '' ,
                'int main() {{' ,
                '  JitRuntime rt;',
                '',
                '   CodeHolder code;',
                '  code.init(rt.environment());',
                '',
                '  StringLogger logger;',
                '',
                '  logger.options().set_indentation(FormatIndentationGroup::kCode, 1);',
                '  logger.options().set_padding(FormatPaddingGroup::kMachineCode, 0);',
                '',
                '  code.set_logger(&logger);',
                '  x86::Assembler a(&code);',
                '',
                f'{body}',
                '  a.add(x86::rsp, 8); // undo alignment',
                '  a.pop(x86::rbx);',
                '  a.pop(x86::r12);',
                '',
                '  a.xor_(x86::ecx, x86::ecx);',
                '  a.sub(x86::rsp, 32);',
                '  a.mov(x86::rax, imm((uint64_t)&_jit_ExitProcess));',
                '  a.call(x86::rax);',
                '  a.ret();        // never reach',
                '',
                '  JitFunc fn = nullptr;',
                '  Error err = rt.add(&fn, &code);',
                '  if (err != Error::kOk) {{',
                '      std::cerr << \"AsmJit error: \" << DebugUtils::error_as_string(err) << std::endl;',
                '      return 1;',
                '  }}',
                '',
                '  std::ostringstream asm_out;',
                '  std::string asm_text = logger.data();',
                '',
                '  replace_all_fun(asm_text);',
                '',
                '  SymbolMappings symbols;',
                f'  {self.render_asm_symbol_mappings()}',
                '  symbols.apply(asm_text);',
                '',
                '  LabelMappings labels;',
                f'  {self.render_asm_label_mappings()}',
                '  labels.apply(asm_text);',
                '',
                '  replace_all_ptr(asm_text);',
                '  replace_all(asm_text, "mov r12, rcx", "lea r12, [rel ctx]");',
                '',
                f'  {self.render_asm_context_replacements()}',
                '',
                f'  {self.render_asm_nasm_header()}',
                f'  {self.render_asm_nasm_structs()}',
                '',
                f'  {self.render_asm_double_replacements()}',
                f'  {ASM_OUT_PH}std::endl;',
                f'  {ASM_OUT_PH}std::endl;',
                '',
                f'  {self.render_asm_double_symbols()}',
                f'  {self.render_asm_extern_symbols()}',
                '',
                f'  {self.render_asm_context_data(
                        int_count,
                        double_count,
                        string_count,
                        record_count,
                        arrays_count,
                        pointr_count)}',
                f'',
                f'    {ASM_OUT_PH}std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind dq {self.module_kind_value}" << std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind_program  equ 1" << std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind_unit     equ 2" << std::endl;',
                f'    {ASM_OUT_PH}"dbase2many_module_kind_library  equ 3" << std::endl << std::endl;',
                f'',
                f'    {ASM_OUT_PH}std::endl;',
                f'    {ASM_OUT_PH}"section .text" << std::endl;',
                f'    {ASM_OUT_PH}"global " << "_{self.func_name}" << std::endl;',
                f'    {self.render_asm_exports()}',
                f'    {ASM_OUT_PH}"_{self.func_name}" << ":" << std::endl;',
                f'',
                f'    asm_out << asm_text;',
                f'',
                f'    {self.render_asm_export_thunks()}',
                f'    {self.render_asm_string_data()}',
                f'',
                f'    std::string final_asm_text = asm_out.str();',
                f'',
                f'    if (!write_formatted_asm_file(',
                f'        final_asm_text.c_str(),',
                f'        \"{self.asm_file}\")) {{',
                f'        std::cerr << "Could not write ASM file: {self.asm_file}" << std::endl;',
                f'    }}',
                f'',
                f'    std::array<int,      {int_count}> int_vars{{}};',
                f'    std::array<double,   {double_count}> double_vars{{}};',
                f'    std::array<char*,    {string_count}> string_vars{{}};',
                f'    std::array<uint8_t,  {record_count}> record_vars{{}};',
                f'    std::array<uint8_t,  {arrays_count}> arrays_vars{{}};',
                f'    std::array<uint64_t, {pointr_count}> pointr_vars{{}};',
                '',
                '    JitContext ctx{};',
                '    ctx.int_vars    = int_vars.data();',
                '',
                '    ctx.double_vars = double_vars.data();',
                '    ctx.string_vars = string_vars.data();',
                '    ctx.record_vars = record_vars.data();',
                '    ctx.arrays_vars = arrays_vars.data();',
                '    ctx.pointr_vars = pointr_vars.data();',
                '',
                '    try {',
                '        fn(&ctx);',
                '    }',
                '    catch (const JitRuntimeError& e) {',
                '        std::cerr << "JIT runtime error: " << e.what() << std::endl;',
                '        rt.release(fn);',
                '        return 2;',
                '    }',
                '    catch (const std::exception& e) {',
                '        std::cerr << "C++ exception: " << e.what() << std::endl;',
                '        rt.release(fn);',
                '        return 3;',
                '    }',
                '    catch (...) {',
                '        std::cerr << "Unknown JIT exception" << std::endl;',
                '        rt.release(fn);',
                '        return 4;',
                '   }',
                '',
                '    rt.release(fn);',
                '    return 0;',
                '}',
                '']
            result = NL.join(result) + NL
            return result
        elif CDATA.BackEnd.current == BACKEND_NASM:
            result = [
                output_header,
                f'section .text',
                f'{self.render_asm_exports()}',
                f'{self.render_asm_export_thunks()}',
                #f'{self.render_asm_string_data()}',
                f'',
                f'section .text',
                f'global _{self.func_name}',
                f'_{self.func_name}:',
                f'{body}',
                '  add rsp, 8  ; undo alignment',
                '  pop rbx',
                '  pop r12',
                '',
                '  xor ecx, ecx',
                '  sub rsp, 32',
                '  lea rax, [rel _jit_ExitProcess]',
                '  call rax',
                '  ret      ; never reach',
                '',
                f'{self.render_asm_nasm_structs()}',
                f'{self.render_asm_context_data(
                    int_count,
                    double_count,
                    string_count,
                    record_count,
                    arrays_count,
                    pointr_count)}',
                f'',
                f'{self.render_string_literals()}' ,
                f'',
                f'{self.render_asm_double_symbols()}',
                f'{self.render_asm_extern_symbols()}',
                f''
                f'DBASE2MANY_MODULE_KIND: db {self.module_kind_value}'
            ]            
            result = NL.join(result) + NL
            return result
        else:
            return "<unknown backend>"
        
    def render_variable_output(self):
        out = []
        
        for key, info in sorted(self.vars.items(), key=lambda x: x[1]["slot"]):
            name = info["name"]
            typ  = info["type"]
            slot = info["slot"]
            
            if typ == "integer":
                out.append(
                    f'    std::cout << "{name} = " << int_vars[{slot}] << std::endl;'
                )
            elif typ == "double":
                out.append(
                    f'    std::cout << "{name} = " << double_vars[{slot}] << std::endl;'
                )
        
        return "\\n".join(out)
        
    def render_print_output(self):
        return "\n".join(self.cpp_print_lines)


# ---------------------------------------------------------------------------
# generator class
# ---------------------------------------------------------------------------
class GeneratorClass(AsmJitGenerator):
    def __init__(self, backend, format):
        super().__init__(backend)
        self.coff = None
        
        if format is not None:
            if isinstance(format, PECoffWriter):
                self.coff       = format
        else:
            raise RuntimError("executable format invalid")
            
        self.coff_context_done  = False
        self.coff_main_done     = False
        
        #self.main_offset = len(self.coff.text)
        #
        #self.coff.emit_lea_rcx_data_label("str_0")
        #self.coff.emit_sub_rsp_imm8(40)
        #self.coff.emit_call_rel32("_jit_print_text")
        #self.coff.emit_add_rsp_imm8(40)
        #
        #self.coff.emit_mov_ecx_imm32(123)
        #self.coff.emit_sub_rsp_imm8(40)
        #self.coff.emit_call_rel32("_jit_print_int")
        #self.coff.emit_add_rsp_imm8(40)
        #self.coff.emit_ret()
        
        #self.coff.add_symbol("_main", self.main_offset, section_number = 1)

    def finalize_coff_context(self):
        if getattr(self, "coff_context_done", False):
            return
        
        self.coff.add_jit_context(
            int_count     = max(1, self.next_int_slot),
            double_count  = max(1, self.next_double_slot),
            string_count  = max(1, self.next_string_slot),
            record_bytes  = max(8, self.next_record_slot),
            arrays_bytes  = max(8, self.next_arrays_slot),
            pointer_count = max(1, self.next_pointr_slot)
        )
        self.coff_context_done = True
        
    def coff_main(self):
        if getattr(self, "coff_main_done", False):
            return
        
        self.finalize_coff_context()
        
        self.coff.begin_function("_main", local_size = 0)
        self.coff.emit_lea_reg_data_label("r12", "ctx")
        self.coff.emit_lea_rcx_data_label("str_0")
        self.coff.emit_runtime_call("_jit_print_text")
        self.coff.emit_mov_reg_imm32("ecx", 123)
        self.coff.emit_runtime_call("_jit_print_int")
        self.coff.end_function()
        
        self.coff_main_done = True
        
    def write_main(self, obj_file, exe_file):
        if self.coff.find_symbol_index("str_0") is None:
            self.coff.add_data_string("str_0", "Hallo aus COFF")
            
        self.coff_main()
        self.coff.write(obj_file)
        
        pe = PEWriter64(self.coff)
        pe.emit_ret()
        pe.write(exe_file)

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
        args = handle_args(args)
        
        if not args.source:
            CDATA.LastErrorCode = LastError.NO_SOURCE
            raise Exception("no source file given.")
        
        source_file = args.source
        name, ext   = os.path.splitext(source_file)
        found       = False
        
        if ext.lower() in [".pas", ".pp"]:
            source_file = name + ext
        else:
            if not ext or len(ext) < 2:
                source_file = name + ".pas"
            else:
                source_file = name + ext
        
        # todo !!!
        CDATA.InputFiles.append(source_file)
        
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
            raise Exception("source code have syntax errors.")
        
        # -----------------------------------------
        # 4. generate asmjit c++ / nasm code  ...
        # -----------------------------------------
        backend = None
        if args.backend == "nasm":
            backend = NasmBackend()
            backend.current = "nasm"
        else:
            backend = AsmJitBackend()
            backend.current = "asmjit"
        
        if backend is None:
            raise Exception("could not create backend")
        
        generator = GeneratorClass(backend, PECoffWriter())
        generator.source_file = os.path.abspath(source_file)
        generator.source_dir  = os.path.dirname(generator.source_file)
        
        text = generator.visit(tree)
        generator.write_fpc_import_unit()
        
        # -----------------------------------------
        # 5. finalize: create c++ output file ...
        # -----------------------------------------
        if CDATA.BackEnd.current == BACKEND_ASMJIT:
            if not CDATA.cpp_file:
                CDATA.cpp_file = "aout.cc"
            outfile = Path(CDATA.cpp_file)
            if outfile.exists():
                check = input(f"{cpp_file}: exists. Overwrite? (Y/N): ").strip().lower()
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
                check = input(f"{CDATA.asm_file}: exists. Overwrite? (Y/N): ").strip().lower()
                if check in ('j', 'y'):
                    with open(CDATA.asm_file, "w", encoding="utf-8") as f:
                        f.write(text)
                        f.close()
                    CDATA.BackEnd.current = BACKEND_OBJFILE
            else:
                with open(CDATA.asm_file, "w", encoding="utf-8") as f:
                    f.write(text)
                    f.close()
                CDATA.BackEnd.current = BACKEND_OBJFILE
                    
        if CDATA.BackEnd.current == BACKEND_OBJFILE:
            if not CDATA.obj_file:
                CDATA.obj_file = "aout.o"
            outfile = Path(CDATA.obj_file)
            if outfile.exists():
                check = input(f"{CDATA.obj_file}: exists. Overwrite? (Y/N): ").strip().lower()
                if check in ('j', 'y'):
                    generator.write_main(CDATA.obj_file, CDATA.exe_file)
                    #with open(CDATA.obj_file, "w", encoding="utf-8") as f:
                    #    f.write(text)
                    #    f.close()
            else:
                generator.write_main(CDATA.obj_file, CDATA.exe_file)
                #with open(CDATA.obj_file, "w", encoding="utf-8") as f:
                #    f.write(text)
                #    f.close()
        else:
            print(text)
        
        return 0
        
    except CompileError as e:
        if generator is not None:
            print(generator.format_error(source_file, e), file = sys.stderr)
            return 3
        else:
            print(e, file = sys.stderr)
            return 3
    except ArgumentParserError as e:
        print(f"Error: Invalid argument(s)")
        print(f"Text : {e.message}")
        #print(f"Code : {e.errno}")
        return 2
    except FileNotFoundError as e:
        print(f"Error: File not found '{e.filename}'")
        print(f"Text : {e.strerror}")
        print(f"Code : {e.errno}")
        return 2
    except Exception as e:
        #print(f"Error: {str(e)}")
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
