# ---------------------------------------------------------------------------
# File: types..py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations
from dataclasses import dataclass, field

from compiler.common.constants import *

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
        self.args_target         : str  = ""
        self.args_backend        : str  = ""
        self.ExeOutputDir        : str  = ""
        self.InputFiles          : list = []
        self.UnitFiles           : list = []
        self.IncludePaths        : list = []
        
        self.imports = {
            "kernel32.dll": [
                "ExitProcess",
            ],
            "user32.dll": [
                "MessageBoxA",
            ],
            "mpr.dll": [
                "WNetGetConnectionA@12"
            ],
            "libdbase2many.32.dll": [
                ( "_jit_print_int",                   20 ),
                ( "_jit_print_text",                  21 ),
                ( "_jit_print_newline",               22 ),
                ( "_jit_print_double",                23 ),
                ( "_jit_print_char",                  24 ),

                ( "_jit_new_memory",                 200 ),
                ( "_jit_dispose_memory",             201 ),

                ( "_jit_malloc",                     210 ),
                ( "_jit_realloc",                    211 ),
                ( "_jit_free",                       212 ),

                ( "_jit_memcpy",                     220 ),
                ( "_jit_memset",                     221 ),
                ( "_jit_memcmp",                     222 ),
                ( "_jit_memmove",                    223 ),

                ( "_jit_strdup",                     230 ),
                ( "_jit_strlen",                     231 ),

                ( "_jit_debug_break",                300 ),

                ( "_jit_runtime_error",              400 ),
                ( "_jit_array_bounds_error",         401 ),
                ( "_jit_string_range_error",         402 ),
                ( "_jit_nil_pointer_error",          403 ),
                ( "_jit_out_of_memory_error",        404 ),

                ( "_jit_disk_free",                  500 ),
                ( "_jit_disk_total",                 501 ),
                ( "_jit_disk_label",                 502 ),
                ( "_jit_disk_serial",                503 ),
                ( "_jit_disk_filesystem",            504 ),
                ( "_jit_disk_type",                  505 ),
                ( "_jit_disk_share",                 506 ),
                ( "_jit_disk_used",                  507 ),
                ( "_jit_disk_exists",                508 ),
                ( "_jit_disk_ready",                 509 ),
                ( "_jit_disk_iscdrom",               510 ),
                ( "_jit_disk_isnetwork",             511 ),
                ( "_jit_disk_isremovable",           512 ),
                ( "_jit_disk_isfixed",               513 ),

                ( "_jit_dynarray_setlength",        1000 ),
                
                ( "_jit_dynstring_setlength",       2000 ),
                ( "_jit_dynstring_from_cstr",       2001 ),
                ( "_jit_dynstring_length",          2002 ),
                ( "_jit_dynstring_concat",          2003 ),
                ( "_jit_dynstring_copy",            2004 ),
                ( "_jit_dynstring_pos",             2005 ),

                ( "_jit_exception_push",            4100 ),
                ( "_jit_exception_pop",             4101 ),
                ( "_jit_setjmp",                    4102 ),
                ( "_jit_longjmp",                   4103 ),
                
                ( "_jit_read_int",                  5000 ),
                ( "_jit_read_string",               5001 ),
                
                ( "_jit_ExitProcess",               8000 ),
                
                ( "_jit_blake2", 9000 ),
                ( "_jit_crc16" , 9002 ),
                ( "_jit_crc32" , 9003 ),
                ( "_jit_crc32c", 9004 ),
                ( "_jit_crc64" , 9005 ),
                ( "_jit_md5"   , 9006 ),
                ( "_jit_sha1"  , 9007 ),
                ( "_jit_sha3"  , 9008 ),
                ( "_jit_sha224", 9009 ),
                ( "_jit_sha256", 9010 ),
                ( "_jit_sha384", 9011 ),
                ( "_jit_sha512", 9012 ),
            ],
        }

global CDATA
CDATA = CommonData()

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
    properties  : dict = field(default_factory=dict)
