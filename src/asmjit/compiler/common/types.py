# ---------------------------------------------------------------------------
# File: types..py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations
from dataclasses import dataclass, field

from compiler.common.constants import *
from compiler.common.packed_loader_imports import (
    install_packed_dll_loader_imports
)
from compiler.common.runtime_imports import (
    initialize_commondata_imports
)

# ---------------------------------------------------------------------------
# backend assembly ...
# ---------------------------------------------------------------------------
class BackEndInfo():
    def __init__(self):
        self.asmjit  = BACKEND_ASMJIT
        self.nasm    = BACKEND_NASM
        self.lines   = ""
        self.current = ""

@dataclass
class SubrangeTypeInfo:
    name: str
    base_type: str

    min_value: int
    max_value: int

    size: int
    signed: bool

class CommonData():
    def __init__(self):
        self.LastErrorCode       : int  = 0
        self.BackEnd             = BackEndInfo()
        self.CurrentWorkingDir   : str  = ""
        
        self.code_page           : int  = 65001
        
        self.src_file            : str  = ""
        self.asm_file            : str  = ""
        self.cpp_file            : str  = ""
        
        self.exe_file            : str  = ""
        self.dll_file            : str  = ""
        
        self.obj_file            : str  = ""
        self.pui_file            : str  = ""
        
        self.inc_file            : list = []
        self.res_file            : str  = ""
        
        self.args_target         : str  = ""
        self.args_backend        : str  = ""
        
        self.ExeOutputDir        : str  = ""
        
        self.asm_lines           : list = []
        
        self.InputFiles          : list = []
        self.UnitFiles           : list = []
        self.IncludePaths        : list = []
        
        self.force_write         : str  = ""
        self.debug_mode          : bool = False
        self.args_verbose        : False
        
        self.link_object_files   = []
        self.link_archive_files  = []
        
        self.link_library_paths  = []
        self.link_object_paths   = []
        
        self.packed_runtime = False
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
        }
        
        initialize_commondata_imports(self)

        install_packed_dll_loader_imports(
            self.imports
        )

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
    packed      : bool = False
    alignment   : int  = 1

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
    label       : str | None
    params      : list
    owner       : str
    return_type : str | None = None
    implemented : bool = False
    mangled     : str | None = None
    visibility  : str = "public"

    is_virtual  : bool = False
    is_override : bool = False

    vmt_slot    : int | None = None
    vmt_offset  : int | None = None

@dataclass
class ClassInfo:
    name       : str
    fields     : dict[str, RecordFieldInfo]
    methods    : dict[str, list[ClassMethodInfo]]
    size       : int
    parent     : str | None = None
    properties : dict = field(default_factory=dict)

    vmt_symbol        : str | None = None
    class_name_symbol : str | None = None

    vmt_slots   : list[ClassMethodInfo] = field(
        default_factory=list
    )

    vmt_destroy : ClassMethodInfo | None = None

@dataclass
class PE32Export:
    name         : str
    target_label : str
    ordinal      : int | None = None
