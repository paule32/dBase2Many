# ---------------------------------------------------------------------------
# File: types..py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations
from dataclasses import dataclass

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
        self.IncludeDirs         : list = []
        
        self.imports = {
            "kernel32.dll": [
                "ExitProcess",
            ],
            "user32.dll": [
                "MessageBoxA",
            ],
            "libdbase2many.32.dll": [
                ( "_jit_print_int",                   20 ),
                ( "_jit_print_text",                  21 ),
                ( "_jit_print_newline",               22 ),
                ( "_jit_print_double",                23 ),
                ( "_jit_print_char",                  24 ),

                ( "_jit_new_memory",                 200 ),
                ( "_jit_dispose_memory",             201 ),

                ( "_jit_debug_break",                300 ),

                ( "_jit_runtime_error",              400 ),
                ( "_jit_array_bounds_error",         401 ),
                ( "_jit_string_range_error",         402 ),
                ( "_jit_nil_pointer_error",          403 ),
                ( "_jit_out_of_memory_error",        404 ),

                ( "_jit_dynarray_setlength",        1000 ),
                
                ( "_jit_dynstring_setlength",       2000 ),
                ( "_jit_dynstring_from_cstr",       2001 ),
                ( "_jit_dynstring_length",          2002 ),
                ( "_jit_dynstring_concat",          2003 ),
                ( "_jit_dynstring_copy",            2004 ),
                ( "_jit_dynstring_pos",             2005 ),

                ( "_jit_set_exception",             4000 ),
                
                ( "_jit_read_int",                  5000 ),
                ( "_jit_read_string",               5001 ),
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
