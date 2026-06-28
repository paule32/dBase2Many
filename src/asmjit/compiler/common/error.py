# ---------------------------------------------------------------------------
# File: error.py
# Author: (c) 2024, 2025, 2026 Jens Kallup - paule32
# All rights reserved
# ---------------------------------------------------------------------------
from __future__  import annotations
from dataclasses import dataclass

@dataclass
class LastError:
    NO_ERROR                : int =    0
    NO_MEMORY               : int =    1
    NO_SOURCE               : int =    2
    NO_BACKEND              : int =    3
    NO_TARGET               : int =    4
    NO_FILE                 : int =    5
    NO_DIRECTORY            : int =    6
    NO_FILE_OR_DIRECTORY    : int =    7
    FILE_NOT_FOUND          : int =    8
    FILE_EXISTS             : int =    9
    FILE_LOCKED             : int =   10
    IS_FILE                 : int =   11
    IS_DIRECTORY            : int =   12
    PATH_NO_DIRECTORY       : int = 1000
    DIRECTORY_DONT_EXISTS   : int = 1001
    DIRECTORY_NOT_READABLE  : int = 1002
    DIRECTORY_NOT_WRITEABLE : int = 1003

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
