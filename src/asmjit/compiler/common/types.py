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
        
        self.asm_lines           : list = []
        
        self.InputFiles          : list = []
        self.UnitFiles           : list = []
        self.IncludePaths        : list = []
        
        self.link_object_files   = []
        self.link_archive_files  = []
        
        self.link_library_paths  = []
        self.link_object_paths   = []
        
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
                ( "_jit_print_int",                   52 ),
                ( "_jit_print_text",                  53 ),
                ( "_jit_print_newline",               54 ),
                ( "_jit_print_double",                55 ),
                ( "_jit_print_char",                  56 ),

                ( "_jit_new_memory",                 41 ),
                ( "_jit_dispose_memory",             42 ),

                ( "_jit_malloc",                     43 ),
                ( "_jit_realloc",                    44 ),
                ( "_jit_free",                       45 ),

                ( "_jit_memcpy",                     46 ),
                ( "_jit_memset",                     47 ),
                ( "_jit_memcmp",                     48 ),
                ( "_jit_memmove",                    49 ),

                ( "_jit_strdup",                     50 ),
                ( "_jit_strlen",                     51 ),

                ( "_jit_debug_break",                16 ),

                ( "_jit_error_runtime",              31 ),
                ( "_jit_error_array_bounds",         32 ),
                ( "_jit_error_string_range",         33 ),
                ( "_jit_error_nil_pointer",          34 ),
                ( "_jit_error_out_of_memory",        35 ),

                ( "_jit_disk_free",                  17 ),
                ( "_jit_disk_total",                 18 ),
                ( "_jit_disk_label",                 19 ),
                ( "_jit_disk_serial",                20 ),
                ( "_jit_disk_filesystem",            21 ),
                ( "_jit_disk_type",                  22 ),
                ( "_jit_disk_share",                 23 ),
                ( "_jit_disk_used",                  24 ),
                ( "_jit_disk_exists",                25 ),
                ( "_jit_disk_ready",                 26 ),
                ( "_jit_disk_iscdrom",               27 ),
                ( "_jit_disk_isnetwork",             28 ),
                ( "_jit_disk_isremovable",           29 ),
                ( "_jit_disk_isfixed",               30 ),

                ( "_jit_dynarray_setlength",        1 ),
                
                ( "_jit_dynstring_setlength",       57 ),
                ( "_jit_dynstring_from_cstr",       58 ),
                ( "_jit_dynstring_length",          59 ),
                ( "_jit_dynstring_concat",          60 ),
                ( "_jit_dynstring_copy",            61 ),
                ( "_jit_dynstring_pos",             62 ),

                ( "_jit_exception_push",            36 ),
                ( "_jit_exception_pop",             37 ),
                ( "_jit_setjmp",                    38 ),
                ( "_jit_longjmp",                   39 ),
                
                ( "_jit_read_int",                  2 ),
                ( "_jit_read_string",               3 ),
                
                ( "_jit_ExitProcess",               40 ),
                
                ( "_jit_blake2", 4 ),
                ( "_jit_crc16" , 5 ),
                ( "_jit_crc32" , 6 ),
                ( "_jit_crc32c", 7 ),
                ( "_jit_crc64" , 8 ),
                ( "_jit_md5"   , 9 ),
                ( "_jit_sha1"  , 10 ),
                ( "_jit_sha3"  , 11 ),
                ( "_jit_sha224", 12 ),
                ( "_jit_sha256", 13 ),
                ( "_jit_sha384", 14 ),
                ( "_jit_sha512", 15 ),
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
